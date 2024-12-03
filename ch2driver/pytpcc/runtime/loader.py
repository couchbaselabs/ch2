# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Andy Pavlo
# http:##www.cs.brown.edu/~pavlo/
#
# Original Java Version:
# Copyright (C) 2008
# Evan Jones
# Massachusetts Institute of Technology
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------

import os
import sys

import logging
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pprint import pprint,pformat

import constants
from util import *

class Loader:
    
    def __init__(self, driver, scaleParameters, w_ids, needLoadItems, maxExtraFields, datagenSeed):
        self.driver = driver
        self.scaleParameters = scaleParameters
        self.w_ids = w_ids
        self.needLoadItems = needLoadItems
        self.maxExtraFields = maxExtraFields
        self.batch_size = 2500
        self.numSecsPerDay = 86400
        self.datagenSeed = datagenSeed

    ## ==============================================
    ## execute
    ## ==============================================
    def execute(self):
        
        ## Item Table
        if self.needLoadItems:
            logging.debug("Loading ITEM table")
            if self.datagenSeed != constants.CH2_DATAGEN_SEED_NOT_SET:
                self.randomGen = rand.Rand(self.datagenSeed)
            else:
                self.randomGen = rand.Rand()
            self.loadItems()
            self.driver.loadFinishItem()

            ## Load CH tables
            self.loadSupplier()        
            self.loadNation()
            self.loadRegion()
            
        ## Then create the warehouse-specific tuples
        for w_id in self.w_ids:
            if self.datagenSeed != constants.CH2_DATAGEN_SEED_NOT_SET:
                self.randomGen = rand.Rand(self.datagenSeed*w_id)
            else:
                self.randomGen = rand.Rand()
            self.loadWarehouse(w_id)
            self.driver.loadFinishWarehouse(w_id)
        ## FOR
        
        return (None)

    ## ==============================================
    ## loadItems
    ## ==============================================
    def loadItems(self):
        ## Select 10% of the rows to be marked "original"
        originalRows = self.randomGen.selectUniqueIds(self.scaleParameters.items // 10, 1, self.scaleParameters.items)

        ## Load all of the items
        item_tuples = [ ]
        total_tuples = 0
        i_categories_tuples = [ ]
        for i in range(1, self.scaleParameters.items+1):
            original = (i in originalRows)
            i_tuple, i_cat_tuples = self.generateItem(i, original)
            item_tuples.append(i_tuple)
            total_tuples += 1
            if (self.genFlatSchema()):
                for ic in i_cat_tuples:
                    i_categories_tuples.append(ic)
            if len(item_tuples) == self.batch_size:
                logging.debug("LOAD - %s: %5d / %d" % (constants.TABLENAME_ITEM, total_tuples, self.scaleParameters.items))
                self.driver.loadTuples(constants.TABLENAME_ITEM, item_tuples)
                if (self.genFlatSchema()):
                    self.driver.loadTuples(constants.TABLENAME_ITEM_CATEGORIES_FLAT, i_categories_tuples)
                item_tuples = [ ]
                i_categories_tuples = [ ]
        ## FOR
        if len(item_tuples) > 0:
            logging.debug("LOAD - %s: %5d / %d" % (constants.TABLENAME_ITEM, total_tuples, self.scaleParameters.items))
            self.driver.loadTuples(constants.TABLENAME_ITEM, item_tuples)
            if (self.genFlatSchema()):
                self.driver.loadTuples(constants.TABLENAME_ITEM_CATEGORIES_FLAT, i_categories_tuples)
    ## DEF

    ## ==============================================
    ## loadWarehouse
    ## ==============================================
    def loadWarehouse(self, w_id):
        logging.debug("LOAD - %s: %d / %d" % (constants.TABLENAME_WAREHOUSE, w_id, len(self.w_ids)))
        
        try:
            runDate = os.environ["RUN_DATE"]
        except:
            print ("Error parsing run date")

        startDate = self.computeStartDate(runDate) # runDate - 7 years
        endDate = self.computeEndDate(runDate)     # runDate - 1 day
        startOrderDate = startDate
        endOrderDate = endDate - timedelta(days=151)
        startOrderLineDayRange = 2
        endOrderLineDayRange = 151
        cum_h_amount_per_warehouse = 0
        #w_ytd
        w_ytd_idx = 1
        #d_ytd
        d_ytd_idx = 2
        ## h_amount
        h_amount_idx = 6
        #ol_amount
        ol_amount_idx = 5
        # use c_since as orderDate
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            c_balance_idx, c_ytd_payment_idx, c_since_idx = 9, 10, 20
        else:
            c_balance_idx, c_ytd_payment_idx, c_since_idx,  = 7, 8, 14

        ## WAREHOUSE
        w_tuples =  self.generateWarehouse(w_id)
        self.driver.loadTuples(constants.TABLENAME_WAREHOUSE, w_tuples)

        ## DISTRICT
        d_tuples = [ ]
        for d_id in range(1, self.scaleParameters.districtsPerWarehouse+1):
            cum_h_amount_per_district = 0
            d_next_o_id = self.scaleParameters.customersPerDistrict + 1
            d_tuples = self.generateDistrict(w_id, d_id, d_next_o_id)
            c_tuples = [ ]
            c_addresses_tuples = [ ]
            c_phones_tuples = [ ]
            c_categories_tuples = [ ]
            o_orderline_tuples = [ ]
            h_tuples = [ ]
            o_tuples = [ ]
            total_ol_amount = 0
            ## Select 10% of the customers to have bad credit
            selectedRows = self.randomGen.selectUniqueIds(self.scaleParameters.customersPerDistrict // 10, 1, self.scaleParameters.customersPerDistrict)
            
            ## TPC-C 4.3.3.1. says that o_c_id should be a permutation of [1, 3000]. But since it
            ## is a c_id field, it seems to make sense to have it be a permutation of the
            ## customers. For the "real" thing this will be equivalent
            cIdPermutation = [ ]

            for c_id in range(1, self.scaleParameters.customersPerDistrict+1):
                badCredit = (c_id in selectedRows)
                orderDate = self.computeRandomRangeDate(startOrderDate, endOrderDate)
                c_tuple, ca_tuples, cp_tuples, cc_tuples = self.generateCustomer(w_id, d_id, c_id, orderDate, badCredit, True)
                c_tuples.append(c_tuple)
                if (self.genFlatSchema()):
                    for ca in ca_tuples:
                        c_addresses_tuples.append(ca)
                    for cp in cp_tuples:
                        c_phones_tuples.append(cp)
                    for cc in cc_tuples:
                        c_categories_tuples.append(cc)
                h_tuples.append(self.generateHistory(w_id, d_id, c_id, orderDate))
                cIdPermutation.append(c_id)
                cum_h_amount_per_district += h_tuples[c_id-1][h_amount_idx]
                cum_h_amount_per_warehouse += h_tuples[c_id-1][h_amount_idx]
            ## FOR
            d_tuples[0][d_ytd_idx] = cum_h_amount_per_district
            assert cIdPermutation[0] == 1
            assert cIdPermutation[self.scaleParameters.customersPerDistrict - 1] == self.scaleParameters.customersPerDistrict
            self.randomGen.rng.shuffle(cIdPermutation)
            
            no_tuples = [ ]
            for o_id in range(1, self.scaleParameters.customersPerDistrict+1):
                o_ol_cnt = self.randomGen.number(constants.MIN_OL_CNT, constants.MAX_OL_CNT)
                
                ## The last newOrdersPerDistrict are new orders
                newOrder = ((self.scaleParameters.customersPerDistrict - self.scaleParameters.newOrdersPerDistrict) < o_id)
                orderDate = c_tuples[cIdPermutation[o_id-1]-1][c_since_idx]
                orderTime = self.computeRandomRangeTime(orderDate)
                o_tuple, ol_tuples, t_ol_amount = self.generateOrder(w_id, d_id, o_id, cIdPermutation[o_id - 1], o_ol_cnt, orderDate, orderTime, newOrder)
                if (self.genFlatSchema()):
                    for ol in ol_tuples:
                        o_orderline_tuples.append(ol)
                o_tuples.append(o_tuple)
                h_amount = h_tuples[cIdPermutation[o_id-1]-1][h_amount_idx]
                total_ol_amount += t_ol_amount
                if not newOrder:
                    c_tuples[cIdPermutation[o_id-1]-1][c_balance_idx] = total_ol_amount - h_amount
                    c_tuples[cIdPermutation[o_id-1]-1][c_ytd_payment_idx] = h_amount
                ## This is a new order: make one for it
                if newOrder: no_tuples.append([o_id, d_id, w_id])
            ## FOR
            self.driver.loadTuples(constants.TABLENAME_DISTRICT, d_tuples)
            self.driver.loadTuples(constants.TABLENAME_CUSTOMER, c_tuples)
            self.driver.loadTuples(constants.TABLENAME_ORDERS, o_tuples)
            if (self.genFlatSchema()):
                self.driver.loadTuples(constants.TABLENAME_CUSTOMER_ADDRESSES_FLAT, c_addresses_tuples)
                self.driver.loadTuples(constants.TABLENAME_CUSTOMER_PHONES_FLAT, c_phones_tuples)
                self.driver.loadTuples(constants.TABLENAME_CUSTOMER_ITEM_CATEGORIES_FLAT, c_categories_tuples)
                self.driver.loadTuples(constants.TABLENAME_ORDERLINE_FLAT, o_orderline_tuples)

            self.driver.loadTuples(constants.TABLENAME_NEWORDER, no_tuples)
            self.driver.loadTuples(constants.TABLENAME_HISTORY, h_tuples)
#            self.driver.loadFinishDistrict(w_id, d_id)
        ## FOR
        #w_ytd
        w_tuples[0][w_ytd_idx] = cum_h_amount_per_warehouse

        ## Select 10% of the stock to be marked "original"
        s_tuples = [ ]
        selectedRows = self.randomGen.selectUniqueIds(self.scaleParameters.items // 10, 1, self.scaleParameters.items)
        total_tuples = 0
        for i_id in range(1, self.scaleParameters.items+1):
            original = (i_id in selectedRows)
            s_tuples.append(self.generateStock(w_id, i_id, original))
            if len(s_tuples) >= self.batch_size:
                logging.debug("LOAD - %s [W_ID=%d]: %5d / %d" % (constants.TABLENAME_STOCK, w_id, total_tuples, self.scaleParameters.items))
                self.driver.loadTuples(constants.TABLENAME_STOCK, s_tuples)
                s_tuples = [ ]
            total_tuples += 1
        ## FOR
        if len(s_tuples) > 0:
            logging.debug("LOAD - %s [W_ID=%d]: %5d / %d" % (constants.TABLENAME_STOCK, w_id, total_tuples, self.scaleParameters.items))
            self.driver.loadTuples(constants.TABLENAME_STOCK, s_tuples)
    ## DEF

    ## ==============================================
    ## loadSupplier
    ## ==============================================
    def loadSupplier(self):
        ## Load all of the suppliers
        nkeyarr = []
        nkeyarr = [0 for i in range(constants.NUM_SUPPLIERS+1)]
        tuples = [ ]
        total_tuples = 0
        suppRecommendsCommentTuples = self.randomGen.rng.sample(list(range(1, constants.NUM_SUPPLIERS+1)), 5)
        suppComplaintsCommentTuples = self.randomGen.rng.sample(list(set(range(1, constants.NUM_SUPPLIERS+1)) - set(suppRecommendsCommentTuples)), 5)
        for i in range(1, constants.NUM_SUPPLIERS+1):
            tuples.append(self.generateSupplier(i, suppRecommendsCommentTuples, suppComplaintsCommentTuples, nkeyarr))
            total_tuples += 1
            if len(tuples) == self.batch_size:
                logging.debug("LOAD - %s: %5d / %d" % (constants.TABLENAME_SUPPLIER, total_tuples, constants.NUM_SUPPLIERS))
                self.driver.loadTuples(constants.TABLENAME_SUPPLIER, tuples)
                tuples = [ ]
        ## FOR
        if len(tuples) > 0:
            logging.debug("LOAD - %s: %5d / %d" % (constants.TABLENAME_SUPPLIER, total_tuples, constants.NUM_SUPPLIERS))
            self.driver.loadTuples(constants.TABLENAME_SUPPLIER, tuples)
    ## DEF

    ## ==============================================
    ## loadNation 
    ## ==============================================
    def loadNation(self):
        ## Load all of the nations
        tuples = [ ]
        total_tuples = 0
        for i in range(0, constants.NUM_NATIONS):
            tuples.append(self.generateNation(i))
            total_tuples += 1
            if len(tuples) == self.batch_size:
                logging.debug("LOAD - %s: %5d / %d" % (constants.TABLENAME_NATION, total_tuples, constants.NUM_NATIONS))
                self.driver.loadTuples(constants.TABLENAME_NATION, tuples)
                tuples = [ ]
        ## FOR
        if len(tuples) > 0:
            logging.debug("LOAD - %s: %5d / %d" % (constants.TABLENAME_NATION, total_tuples, constants.NUM_NATIONS))
            self.driver.loadTuples(constants.TABLENAME_NATION, tuples)
    ## DEF

    ## ==============================================
    ## loadRegion
    ## ==============================================
    def loadRegion(self):
        ## Load all of the regions
        tuples = [ ]
        total_tuples = 0
        for i in range(0, constants.NUM_REGIONS):
            tuples.append(self.generateRegion(i))
            total_tuples += 1
            if len(tuples) == self.batch_size:
                logging.debug("LOAD - %s: %5d / %d" % (constants.TABLENAME_REGION, total_tuples, constants.NUM_REGIONS))
                self.driver.loadTuples(constants.TABLENAME_REGION, tuples)
                tuples = [ ]
        ## FOR
        if len(tuples) > 0:
            logging.debug("LOAD - %s: %5d / %d" % (constants.TABLENAME_REGION, total_tuples, constants.NUM_REGIONS))
            self.driver.loadTuples(constants.TABLENAME_REGION, tuples)
    ## DEF

    ## ==============================================
    ## generateItem
    ## ==============================================
    def generateItem(self, id, original):
        i_id = id
        i_im_id = self.randomGen.number(constants.MIN_IM, constants.MAX_IM)
        i_name = self.randomGen.astring(constants.MIN_I_NAME, constants.MAX_I_NAME)
        i_price = self.randomGen.fixedPoint(constants.MONEY_DECIMALS, constants.MIN_PRICE, constants.MAX_PRICE)
        i_data = self.randomGen.astring(constants.MIN_I_DATA, constants.MAX_I_DATA)
        if original: i_data = self.fillOriginal(i_data)
        i_tuple = [i_id, i_name, i_price]
        i_tuple.append(self.generateExtraFields(self.maxExtraFields))
        i_category_num = self.randomGen.nprng.choice(range(1, 128), size=self.randomGen.nprng.integers(1,3), replace=False)
        i_categories = []
        for i in i_category_num:
            i_categories.append("category_" + str(format(i, "03d")))
        i_tuple.append(i_categories)
        i_tuple += [i_data, i_im_id]
        i_categories_flat = []
        if (self.genFlatSchema()):
            for i in i_categories:
                i_categories_flat.append([id] + [i])

        return i_tuple, i_categories_flat
    ## DEF

    ## ==============================================
    ## generateWarehouse
    ## ==============================================
    def generateWarehouse(self, w_id):
        w_ytd = constants.INITIAL_W_YTD
        w_tax = self.generateTax()
        w_name = self.randomGen.astring(constants.MIN_NAME, constants.MAX_NAME)
        w_tuple = [w_id, w_ytd, w_tax, w_name]
        w_address = self.generateStreetAddress()
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            w_tuple += w_address
        else:
            w_tuple.append(w_address)
        return [w_tuple]
    ## DEF

    ## ==============================================
    ## generateDistrict
    ## ==============================================
    def generateDistrict(self, d_w_id, d_id, d_next_o_id):
        d_ytd = constants.INITIAL_W_YTD
        d_tax = self.generateTax()
        d_name = self.randomGen.astring(constants.MIN_NAME, constants.MAX_NAME)
        d_address = self.generateStreetAddress()
        d_tuple = [d_id, d_w_id, d_ytd, d_tax, d_next_o_id, d_name]
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            d_tuple += d_address
        else:
            d_tuple.append(d_address)
        return [d_tuple]
    ## DEF

    ## ==============================================
    ## generateCustomer
    ## ==============================================
    def generateCustomer(self, c_w_id, c_d_id, c_id, sinceDate, badCredit, doesReplicateName):
        c_discount = self.randomGen.fixedPoint(constants.DISCOUNT_DECIMALS, constants.MIN_DISCOUNT, constants.MAX_DISCOUNT)
        c_credit = constants.BAD_CREDIT if badCredit else constants.GOOD_CREDIT
        c_tuple = [ c_id, c_d_id, c_w_id, c_discount, c_credit ]
        c_name = self.generateCustomerFullName(c_id)
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            c_tuple += c_name
        else:
            c_tuple.append(c_name)
        c_credit_lim = constants.INITIAL_CREDIT_LIM
        c_balance = constants.INITIAL_BALANCE
        c_ytd_payment = constants.INITIAL_YTD_PAYMENT
        c_payment_cnt = constants.INITIAL_PAYMENT_CNT
        c_delivery_cnt = constants.INITIAL_DELIVERY_CNT
        c_tuple += [c_credit_lim, c_balance, c_ytd_payment, c_payment_cnt, c_delivery_cnt]

        c_tuple.append(self.generateExtraFields(self.maxExtraFields))

        c_addresses, c_addresses_flat  = self.generateCustomerAddresses(c_id, c_d_id, c_w_id)
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            c_address = c_addresses[0][1:]
            c_tuple += c_address
        else:
            c_tuple.append(c_addresses)

        c_phones, c_phones_flat = self.generateCustomerPhones(c_id, c_d_id, c_w_id)
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            c_phone = c_phones[0][1:]
            c_tuple += c_phone
        else:
            c_tuple.append(c_phones)

        c_since = sinceDate
        c_tuple = c_tuple + [c_since]

        c_categories, c_categories_flat = self.generateCustomerCategories(c_id, c_d_id, c_w_id)

        c_tuple.append(c_categories)

        c_data = self.randomGen.astring(constants.MIN_C_DATA, constants.MAX_C_DATA)
        c_tuple.append(c_data)

        return c_tuple, c_addresses_flat, c_phones_flat, c_categories_flat
    ## DEF

    ## ==============================================
    ## generateOrder
    ## ==============================================
    def generateOrder(self, o_w_id, o_d_id, o_id, o_c_id, o_ol_cnt, orderDate, orderTime, newOrder):
        """Returns the generated o_ol_cnt value."""
        o_entry_d = orderTime
        o_carrier_id = constants.NULL_CARRIER_ID if newOrder else self.randomGen.number(constants.MIN_CARRIER_ID, constants.MAX_CARRIER_ID)
        o_all_local = constants.INITIAL_ALL_LOCAL
        o_tuple = [ o_id, o_c_id, o_d_id, o_w_id, o_carrier_id, o_ol_cnt, o_all_local, o_entry_d ]
        o_tuple.append(self.generateExtraFields(self.maxExtraFields))

        startOrderLineDayRange = 2
        endOrderLineDayRange = 151
        ol_amount_idx = 5
        ol_tuples = [ ]
        total_ol_amount = 0
        for ol_number in range(0, o_ol_cnt):
            startOrderLineDate = orderDate + timedelta(days=startOrderLineDayRange)
            endOrderLineDate = orderDate + timedelta(days=endOrderLineDayRange)
            orderLineDate = self.computeRandomRangeDate(startOrderLineDate, endOrderLineDate)
            orderLineTime = self.computeRandomRangeTime(orderLineDate)
            ol_tuple = self.generateOrderLine(o_w_id, o_d_id, o_id, ol_number, self.scaleParameters.items, orderLineTime, newOrder)
            ol_tuples.append(ol_tuple)
            total_ol_amount += ol_tuple[ol_amount_idx]
        ## FOR

        o_tuple.append(ol_tuples)
        ol_tuples_flat = []
        if (self.genFlatSchema()):
            for ol in ol_tuples:
                ol_tuples_flat.append([o_id, o_d_id, o_w_id] + ol)
        return o_tuple, ol_tuples_flat, total_ol_amount
    ## DEF

    ## ==============================================
    ## generateOrderLine
    ## ==============================================
    def generateOrderLine(self, ol_w_id, ol_d_id, ol_o_id, ol_number, max_items, orderLineTime, newOrder):
        ol_i_id = self.randomGen.number(1, max_items)
        ol_supply_w_id = ol_w_id
        ol_delivery_d = orderLineTime
        ol_quantity = self.randomGen.number(constants.MIN_OL_QUANTITY, constants.MAX_OL_QUANTITY)
        if newOrder == False:
            if ol_o_id % 5 == 0:
                ol_amount = self.randomGen.fixedPoint(constants.MONEY_DECIMALS, constants.MIN_AMOUNT, constants.MAX_PRICE * constants.MAX_OL_QUANTITY)
            else:
                ol_amount = 0.00
        else:
            ol_amount = self.randomGen.fixedPoint(constants.MONEY_DECIMALS, constants.MIN_AMOUNT, constants.MAX_PRICE * constants.MAX_OL_QUANTITY)
            ol_delivery_d = None
        ol_dist_info = self.randomGen.astring(constants.DIST, constants.DIST)

        return [ ol_number, ol_i_id, ol_supply_w_id, ol_delivery_d, ol_quantity, ol_amount, ol_dist_info ]
    ## DEF

    ## ==============================================
    ## generateStock
    ## ==============================================
    def generateStock(self, s_w_id, s_i_id, original):
        s_quantity = self.randomGen.number(constants.MIN_QUANTITY, constants.MAX_QUANTITY)
        s_ytd = 0
        s_order_cnt = self.randomGen.number(constants.DISTRICTS_PER_WAREHOUSE, constants.INITIAL_ORDERS_PER_DISTRICT)
        if len(self.w_ids) == 1:
            s_remote_cnt = 0
        else:
            s_remote_cnt = int(s_order_cnt * 0.1) # 10% of orders are remote

        s_data = self.randomGen.astring(constants.MIN_I_DATA, constants.MAX_I_DATA)
        if original: self.fillOriginal(s_data)

        s_dists = [ ]
        for i in range(0, constants.DISTRICTS_PER_WAREHOUSE):
            s_dists.append(self.randomGen.astring(constants.DIST, constants.DIST))
        s_tuple = [ s_i_id, s_w_id, s_quantity, s_ytd, s_order_cnt, s_remote_cnt, s_data ]
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            s_tuple += s_dists
        else:
            s_tuple.append(s_dists)
        return s_tuple
    ## DEF

    ## ==============================================
    ## generateHistory
    ## ==============================================
    def generateHistory(self, h_c_w_id, h_c_d_id, h_c_id, historyDate):
        h_w_id = h_c_w_id
        h_d_id = h_c_d_id
        h_date = historyDate
        h_amount = constants.INITIAL_AMOUNT
        h_data = self.randomGen.astring(constants.MIN_DATA, constants.MAX_DATA)
        return [ h_c_id, h_c_d_id, h_c_w_id, h_d_id, h_w_id, h_date, h_amount, h_data ]
    ## DEF

    ## ==============================================
    ## generateSupplier
    ## ==============================================
    def generateSupplier(self, suppkey, recommendsCommentTuples, complaintsCommentTuples, nkeyarr):
        su_suppkey = suppkey
        su_name = "Supplier#" + str(suppkey).zfill(constants.NUM_LEADING_ZEROS)
        ch2_su_address = self.generateSupplierAddress()
        ch2pp_su_address = self.generateStreetAddress()
        su_nationkey = constants.NATIONS[self.randomGen.number(0, constants.NUM_NATIONS-1)][0]
        nkeyarr[su_nationkey] += 1
        while nkeyarr[su_nationkey] > 162:
            nkeyarr[su_nationkey] -= 1
            su_nationkey = constants.NATIONS[self.randomGen.number(0, constants.NUM_NATIONS-1)][0]
            nkeyarr[su_nationkey] += 1
        su_phone = self.randomGen.nstring(constants.PHONE, constants.PHONE)
        su_acctbal = self.randomGen.fixedPoint(constants.MONEY_DECIMALS, constants.MIN_SUPPLIER_ACCTBAL, constants.MAX_SUPPLIER_ACCTBAL)
        if suppkey in recommendsCommentTuples:
            su_comment = self.randomGen.randomStringsWithEmbeddedSubstrings(constants.MIN_SUPPLIER_COMMENT, constants.MAX_SUPPLIER_COMMENT, "Customer", "Recommends")
        elif suppkey in complaintsCommentTuples:
            su_comment = self.randomGen.randomStringsWithEmbeddedSubstrings(constants.MIN_SUPPLIER_COMMENT, constants.MAX_SUPPLIER_COMMENT, "Customer", "Complaints")
        else:
            su_comment = self.randomGen.randomStringMinMax(constants.MIN_SUPPLIER_COMMENT, constants.MAX_SUPPLIER_COMMENT)
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            su_tuple = [su_suppkey, su_name, ch2_su_address, su_nationkey, su_phone, su_acctbal, su_comment]
        else:
            su_tuple = [su_suppkey, su_name, ch2pp_su_address, su_nationkey, su_phone, su_acctbal, su_comment]
        return su_tuple
    ## DEF


    ## ==============================================
    ## generateNation
    ## ==============================================
    def generateNation(self, nationkey):
        n_nationkey = constants.NATIONS[nationkey][0]
        n_name = constants.NATIONS[nationkey][1]
        n_regionkey = constants.NATIONS[nationkey][2]        
        n_comment = self.randomGen.randomStringMinMax(constants.MIN_NATION_COMMENT, constants.MAX_NATION_COMMENT)

        return [ n_nationkey, n_name, n_regionkey, n_comment ]
    ## DEF

    ## ==============================================
    ## generateRegion
    ## ==============================================
    def generateRegion(self, regionkey):
        r_regionkey = regionkey
        r_name = constants.REGIONS[regionkey]
        r_comment = self.randomGen.randomStringMinMax(constants.MIN_REGION_COMMENT, constants.MAX_REGION_COMMENT)

        return [ r_regionkey, r_name, r_comment ]
    ## DEF

    ## ==============================================
    ## generateCustomerFullName
    ## ==============================================
    def generateCustomerFullName(self, c_id):
        """
            Returns a full name (first name, middle name, and last name)
        """
        c_first = self.randomGen.astring(constants.MIN_FIRST, constants.MAX_FIRST)
        c_middle = constants.MIDDLE
        assert 1 <= c_id and c_id <= constants.CUSTOMERS_PER_DISTRICT
        if c_id <= 1000:
            c_last = self.randomGen.makeLastName(c_id - 1)
        else:
            c_last = self.randomGen.makeRandomLastName(constants.CUSTOMERS_PER_DISTRICT)
        return [ c_first, c_middle, c_last ]
    ## DEF

    ## ==============================================
    ## generateCustomerAddresses
    ## ==============================================
    def generateCustomerAddresses(self, c_id, c_d_id, c_w_id):
        """
            Returns customer addresses
        """
        c_addresses_flat = []
        c_addresses = [["shipping"] + self.generateStreetAddress()]
        c_other_addr_type = ["home", "work", "billing"]
        c_other_addr = self.randomGen.nprng.choice(c_other_addr_type, size=self.randomGen.nprng.integers(0, 4), replace=False)
        for coa in c_other_addr:
            c_addresses.append([coa] + self.generateStreetAddress())
        if (self.genFlatSchema()):
            for c in c_addresses:
                c_addresses_flat.append([c_id, c_d_id, c_w_id] + c)
        return c_addresses, c_addresses_flat
    ## DEF

    ## ==============================================
    ## generateCustomerPhones
    ## ==============================================
    def generateCustomerPhones(self, c_id, c_d_id, c_w_id):
        """
            Returns customer phones
        """
        c_phones_flat = []
        c_phones = [["contact"] + [self.randomGen.nstring(constants.PHONE, constants.PHONE)]]
        c_other_phone_type = ["home", "work", "mobile"]
        c_other_phone = self.randomGen.nprng.choice(c_other_phone_type, size=self.randomGen.nprng.integers(0, 4), replace=False)
        for cop in c_other_phone:
            c_phones.append([cop] + [self.randomGen.nstring(constants.PHONE, constants.PHONE)])
        if (self.genFlatSchema()):
            for c in c_phones:
                c_phones_flat.append([c_id, c_d_id, c_w_id] + c)
        return c_phones, c_phones_flat
    ## DEF

    ## ==============================================
    ## generateCustomerCategories
    ## ==============================================
    def generateCustomerCategories(self, c_id, c_d_id, c_w_id):
        """
            Returns customer categories
        """
        c_categories_flat = []
        c_category_num = self.randomGen.nprng.choice(range(1, 128), size=self.randomGen.nprng.integers(0,15), replace=False)
        c_categories = []
        for c in c_category_num:
            c_categories.append("category_" + str(format(c, "03d")))
        if (self.genFlatSchema()):
            for c in c_categories:
                c_categories_flat.append([c_id, c_d_id, c_w_id, c])
        return c_categories, c_categories_flat

    ## ==============================================
    ## generateExtraFields
    ## ==============================================
    def generateExtraFields(self, extraFields):
        return [uuid.UUID(int=self.randomGen.rng.getrandbits(128)).hex for _ in range(extraFields)]

    ## ==============================================
    ## generateNameAndAddress
    ## ==============================================
    def generateNameAndAddress(self):
        """
            Returns a name and a street address 
            Used by both generateWarehouse and generateDistrict.
        """
        name = self.randomGen.astring(constants.MIN_NAME, constants.MAX_NAME)
        return [ name ] + self.generateStreetAddress()
    ## DEF

    ## ==============================================
    ## generateStreetAddress
    ## ==============================================
    def generateStreetAddress(self):
        """
            Returns a list for a street address
            Used for warehouses, districts and customers.
        """
        street1 = self.randomGen.astring(constants.MIN_STREET, constants.MAX_STREET)
        street2 = self.randomGen.astring(constants.MIN_STREET, constants.MAX_STREET)
        city = self.randomGen.astring(constants.MIN_CITY, constants.MAX_CITY)
        state = self.randomGen.astring(constants.STATE, constants.STATE)
        zip = self.generateZip()

        return [ street1, street2, city, state, zip ]
    ## DEF

    ## ==============================================
    ## generateSupplierAddress
    ## ==============================================
    def generateSupplierAddress(self):
        """
            Returns address of supplier
        """
        address = self.randomGen.astring(constants.MIN_SUPPLIER_ADDRESS, constants.MAX_SUPPLIER_ADDRESS)
        return address 
    ## DEF

    ## ==============================================
    ## generateTax
    ## ==============================================
    def generateTax(self):
        return self.randomGen.fixedPoint(constants.TAX_DECIMALS, constants.MIN_TAX, constants.MAX_TAX)
    ## DEF

    ## ==============================================
    ## generateZip
    ## ==============================================
    def generateZip(self):
        length = constants.ZIP_LENGTH - len(constants.ZIP_SUFFIX)
        return self.randomGen.nstring(length, length) + constants.ZIP_SUFFIX
    ## DEF

    ## ==============================================
    ## fillOriginal
    ## ==============================================
    def fillOriginal(self, data):
        """
            a string with ORIGINAL_STRING at a random position
        """
        originalLength = len(constants.ORIGINAL_STRING)
        position = self.randomGen.number(0, len(data) - originalLength)
        out = data[:position] + constants.ORIGINAL_STRING + data[position + originalLength:]
        assert len(out) == len(data)
        return out
    ## DEF
    def computeStartDate(self, runDate):
        startDateTime = datetime.strptime(runDate,  "%Y-%m-%d %H:%M:%S") - relativedelta(years=7)
        return startDateTime 
    ## DEF

    def computeEndDate(self, runDate):
        endDateTime = datetime.strptime(runDate,  "%Y-%m-%d %H:%M:%S") - timedelta(days=1)
        return endDateTime 
    ## DEF

    def computeRandomRangeDate(self, startDate, endDate):
         delta = endDate - startDate
         deltaSecs = (delta.days * self.numSecsPerDay) + delta.seconds
         randomTime = self.randomGen.rng.randrange(deltaSecs)
         return startDate + timedelta(seconds=randomTime)
    ## DEF

    def computeRandomRangeTime(self, dateObj):
        return dateObj.strftime("%Y-%m-%d %H:%M:%S")

    def genFlatSchema(self):
        if self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2PF"] or self.driver.schema == constants.CH2_DRIVER_SCHEMA["CH2PPF"]:
            return True
        return False

    ## DEF

## CLASS

