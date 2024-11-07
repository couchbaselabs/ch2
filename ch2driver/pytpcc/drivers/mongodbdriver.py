# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Andy Pavlo
# http://www.cs.brown.edu/~pavlo/
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

from __future__ import with_statement

import os
import sys
import logging
import pymongo
from pprint import pprint,pformat
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import traceback
import time
import constants
from .abstractdriver import *

## ==============================================
## MongodbDriver
## ==============================================
class MongodbDriver(AbstractDriver):
    DEFAULT_CONFIG = {
        "host":         ("The hostname to mongod", "localhost" ),
        "port":         ("The port number to mongod", 27017 ),
        "name":         ("Collection name", "tpcc"),
        "denormalize":  ("If set to true, then the CUSTOMER data will be denormalized into a single document", False),
    }

    def __init__(self, ddl, clientId, TAFlag="T",
                 schema=constants.CH2_DRIVER_SCHEMA["CH2"],
                 preparedTransactionQueries={},
                 analyticalQueries=constants.CH2_DRIVER_ANALYTICAL_QUERIES["HAND_OPTIMIZED_QUERIES"],
                 customerExtraFields=constants.CH2_CUSTOMER_EXTRA_FIELDS["NOT_SET"],
                 ordersExtraFields=constants.CH2_ORDERS_EXTRA_FIELDS["NOT_SET"],
                 itemExtraFields=constants.CH2_ITEM_EXTRA_FIELDS["NOT_SET"],
                 load_mode=constants.CH2_DRIVER_LOAD_MODE["NOT_SET"],
                 kv_timeout=constants.CH2_DRIVER_KV_TIMEOUT,
                 bulkload_batch_size=constants.CH2_DRIVER_BULKLOAD_BATCH_SIZE):
        super(MongodbDriver, self).__init__("mongodb", ddl)
        try:
            user = os.environ["USER_ID"]
            password = os.environ["PASSWORD"]
            data_node = os.environ["DATA_URL"]
            cluster = data_node[0: data_node.index('.')]
            self.client_id = clientId;
            self.TAFlag = TAFlag
            self.schema = schema
            if TAFlag == "A":
                atlas_sql_node = os.environ["ATLAS_SQL_URL"]
                atlasUri = "mongodb://"+user+":"+password+"@"+atlas_sql_node+"/"+self.schema+"?ssl=true&authSource=admin"
                self.client = MongoClient(atlasUri)
            else:
                uri = "mongodb+srv://"+user+":"+password+"@"+data_node+"/?retryWrites=true&w=majority&appName="+cluster
                self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.database = self.client[self.schema]
            self.denormalize = False
            self.analyticalQueries = analyticalQueries
            self.customerExtraFields = customerExtraFields
            self.ordersExtraFields = ordersExtraFields
            self.itemExtraFields = itemExtraFields
            self.bulkload_batch_size = bulkload_batch_size

            self.collections = {}
            for tableName in constants.ALL_TABLES:
                self.__dict__[tableName.lower()] = self.database.get_collection(constants.COLLECTIONS_DICT[tableName])
                self.collections[tableName] = self.database.get_collection(constants.COLLECTIONS_DICT[tableName])

        except Exception as e:
            raise Exception(
                "The following error occurred: ", e)

        return

    ## ----------------------------------------------
    ## makeDefaultConfig
    ## ----------------------------------------------
    def makeDefaultConfig(self):
        return MongodbDriver.DEFAULT_CONFIG
    
    ## ----------------------------------------------
    ## loadConfig
    ## ----------------------------------------------
    def loadConfig(self, config):
        return

        for key in MongodbDriver.DEFAULT_CONFIG.keys():
            assert key in config, "Missing parameter '%s' in %s configuration" % (key, self.name)
        
        self.conn = pymongo.Connection(config['host'], int(config['port']))
        self.database = self.conn[str(config['name'])]
        self.denormalize = config['denormalize']
        
        if config["reset"]:
            logging.debug("Deleting database '%s'" % self.database.name)
            for name in constants.ALL_TABLES:
                if name in self.database.collection_names():
                    self.database.drop_collection(name)
                    logging.debug("Dropped collection %s" % name)
        ## IF
        
        ## Setup!
        load_indexes = ('execute' in config and not config['execute']) and \
                       ('load' in config and not config['load'])
        for name in constants.ALL_TABLES:
            ## Create member mapping to collections
            self.__dict__[name.lower()] = self.database[name]
            
            ## Create Indexes
            if load_indexes and name in constants.TABLE_INDEXES:
                logging.debug("Creating index for %s" % name)
                for index in constants.TABLE_INDEXES[name]:
                	self.database[name].create_index(index)
        ## FOR

    def tryBulkLoad(self, collection, cur_batch):
        for i in range(constants.NUM_LOAD_RETRIES):
            try:
                result = collection.insert_many(cur_batch)
                if result.acknowledged == True:
                    return True
                else:
                    time.sleep(1)
                    logging.debug("Client ID # %d failed bulk load data into KV, try %d" % (self.client_id, i))
            except:
                logging.debug("Client ID # %d exception bulk load data into KV, try %d" % (self.client_id, i))
                exc_info = sys.exc_info()
                tb = ''.join(traceback.format_tb(exc_info[2]))
                logging.debug(f'Exception info: {exc_info[1]}\nTraceback:\n{tb}')
                time.sleep(1)

        logging.debug("Client ID # %d failed bulk load data into KV after %d retries" % (self.client_id, constants.NUM_LOAD_RETRIES))
        return False

    ## ----------------------------------------------
    ## loadTuples for mongodb
    ## ----------------------------------------------
    def loadTuples(self, tableName, tuples):
        if len(tuples) == 0:
            return


        logging.debug("Loading %d tuples for tableName %s" % (len(tuples), tableName))
        assert tableName in constants.CH2_TABLE_COLUMNS, "Unexpected table %s" % tableName

        collection = self.collections[tableName]
        # For bulk load: load in batches
        cur_batch = []
        cur_size = 0
        for t in tuples:
            _, val = self.getOneDoc(tableName, t)
            cur_batch.append(val)
            cur_size += 1
            if cur_size >= 10000: #self.bulkload_batch_size:
                result = self.tryBulkLoad(collection, cur_batch)
                if result == True:
                    cur_batch = []
                    cur_size = 0
                    continue
                else:
                    logging.debug("Client ID # %d failed bulk load data into KV, aborting..." % self.client_id)
        if cur_size > 0:
            result = self.tryBulkLoad(collection, cur_batch)
            if result == False:
                logging.debug("Client ID # %d failed bulk load data into KV, aborting..." % self.client_id)
        return

    ## ----------------------------------------------
    ## loadFinishDistrict
    ## ----------------------------------------------
    def loadFinishDistrict(self, w_id, d_id):
        return

    ## ----------------------------------------------
    ## loadFinish
    ## ----------------------------------------------
    def loadFinish(self):
        logging.info("Client ID # %d Finished loading tables" % (self.client_id))
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            for name in constants.ALL_TABLES:
                logging.debug("%-12s%d records" % (name+":", self.database[name].count_documents({})))
        ## IF

    def txStatus(self):
        return self.tx_status

    ## ----------------------------------------------
    ## doDelivery
    ## ----------------------------------------------
    def doDelivery(self, params):
        self.tx_status = ""
        w_id = params["w_id"]
        o_carrier_id = params["o_carrier_id"]
        ol_delivery_d = params["ol_delivery_d"]
        
        result = [ ]
        for d_id in range(1, constants.DISTRICTS_PER_WAREHOUSE+1):
            ## getNewOrder
            no = self.neworder.find_one({"no_d_id": d_id, "no_w_id": w_id}, {"no_o_id": 1})
            if no == None:
                ## No orders for this district: skip it. Note: This must be reported if > 1%
                continue
            assert len(no) > 0
            o_id = no["no_o_id"]
            
            ## getCId
            o = self.orders.find_one({"o_id": o_id, "o_d_id": d_id, "o_w_id": w_id}, {"o_c_id": 1})
            assert o != None
            c_id = o["o_c_id"]
                
            ## sumOLAmount
            orderLines = self.orders.find({"o_id": o_id, "o_d_id": d_id, "o_w_id": w_id}, {"o_orderline.ol_amount": 1})
            assert orderLines != None

            ol_total = 0
            for oLines in orderLines:
                oLine = oLines["o_orderline"]
                for i in range(len(oLine)):
                    o_total = oLine[i]["ol_amount"]
                    ol_total += o_total
            
            ## updateOrders
            self.orders.update_one(o, {"$set": {"o_carrier_id": o_carrier_id}})
            ## updateOrderLine
            self.orders.update_one({"o_id": o_id, "o_d_id": d_id, "o_w_id": w_id}, {"$set": {"o_orderline.$[].ol_delivery_d": ol_delivery_d}})
                
            ## updateCustomer
            self.customer.update_one({"c_id": c_id, "c_d_id": d_id, "c_w_id": w_id}, {"$inc": {"c_balance": ol_total}})
            ## IF

            ## deleteNewOrder
            self.neworder.delete_one({"_id": no['_id']})

            # These must be logged in the "result file" according to TPC-C 2.7.2.2 (page 39)
            # We remove the queued time, completed time, w_id, and o_carrier_id: the client can figure
            # them out
            # If there are no order lines, SUM returns null. There should always be order lines.
            assert ol_total != None, "ol_total is NULL: there are no order lines. This should not happen"
            assert ol_total > 0.0

            result.append((d_id, o_id))
        ## FOR
        return result

    ## ----------------------------------------------
    ## doNewOrder
    ## ----------------------------------------------
    def doNewOrder(self, params):
        self.tx_status = ""
        w_id = params["w_id"]
        d_id = params["d_id"]
        c_id = params["c_id"]
        o_entry_d = params["o_entry_d"]
        i_ids = params["i_ids"]
        i_w_ids = params["i_w_ids"]
        i_qtys = params["i_qtys"]
        if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            s_dist_col = "s_dist_%02d" % d_id
        else:
            s_dist_col = "s_dists"
            
        assert len(i_ids) > 0
        assert len(i_ids) == len(i_w_ids)
        assert len(i_ids) == len(i_qtys)

        ## http://stackoverflow.com/q/3844931/
        all_local = (not i_w_ids or [w_id] * len(i_w_ids) == i_w_ids)
        
        items = self.item.find({"i_id": {"$in": i_ids}}, {"i_id": 1, "i_price": 1, "i_name": 1, "i_data": 1})
        itemsCount = self.item.count_documents({"i_id": {"$in": i_ids}})
        ## TPCC defines 1% of neworder gives a wrong itemid, causing rollback.
        ## Note that this will happen with 1% of transactions on purpose.
        #if items.count_documents({}) != len(i_ids):
        if itemsCount != len(i_ids):
            ## TODO Abort here!
            return
        ## IF
        
        ## ----------------
        ## Collect Information from WAREHOUSE, DISTRICT, and CUSTOMER
        ## ----------------
        
        # getWarehouseTaxRate
        w = self.warehouse.find_one({"w_id": w_id}, {"w_tax": 1})
        assert w
        w_tax = w["w_tax"]
        
        # getDistrict
        d = self.district.find_one({"d_id": d_id, "d_w_id": w_id}, {"d_tax": 1, "d_next_o_id": 1})
        assert d
        d_tax = d["d_tax"]
        d_next_o_id = d["d_next_o_id"]
        
        # incrementNextOrderId
        # HACK: This is not transactionally safe!
        self.district.update_one(d, {"$inc": {"d_next_o_id": 1}})
        
        # getCustomer
        if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            c = self.customer.find_one({"c_id": c_id, "c_d_id": d_id, "c_w_id": w_id}, {"c_discount": 1, "c_last": 1, "c_credit": 1})
        else:
            c = self.customer.find_one({"c_id": c_id, "c_d_id": d_id, "c_w_id": w_id}, {"c_discount": 1, "c_name.c_last": 1, "c_credit": 1})
        assert c
        c_discount = c["c_discount"]

        ## ----------------
        ## Insert Order Information
        ## ----------------
        ol_cnt = len(i_ids)
        o_carrier_id = constants.NULL_CARRIER_ID

        # createNewOrder
        self.neworder.insert_one({"no_o_id": d_next_o_id, "no_d_id": d_id, "no_w_id": w_id})

        o = {"o_id": d_next_o_id, "o_entry_d": o_entry_d, "o_carrier_id": o_carrier_id, "o_ol_cnt": ol_cnt, "o_all_local": all_local}
        o["o_d_id"] = d_id
        o["o_w_id"] = w_id
        o["o_c_id"] = c_id
            
        # createOrder
        self.orders.insert_one(o)
            
        ## ----------------
        ## OPTIMIZATION:
        ## If all of the items are at the same warehouse, then we'll issue a single
        ## request to get their information
        ## ----------------
        stockInfos = None
        if all_local and False:
            # getStockInfo
            allStocks = self.stock.find({"s_i_id": {"$in": i_ids}, "s_w_id": w_id}, {"s_i_id": 1, "s_quantity": 1, "s_data": 1, "s_ytd": 1, "s_order_cnt": 1, "s_remote_cnt": 1, s_dist_col: 1})
            allStocksCount = self.stock.count_documents({"s_i_id": {"$in": i_ids}, "s_w_id": w_id})
            assert allStocksCount == ol_cnt
            stockInfos = { }
            for si in allStocks:
                stockInfos["s_i_id"] = si # HACK
        ## IF

        ## ----------------
        ## Insert Order Item Information
        ## ----------------
        item_data = [ ]
        total = 0
        for i in range(ol_cnt):
            ol_number = i + 1
            ol_supply_w_id = i_w_ids[i]
            ol_i_id = i_ids[i]
            ol_quantity = i_qtys[i]

            itemInfo = items[i]
            i_name = itemInfo["i_name"]
            i_data = itemInfo["i_data"]
            i_price = itemInfo["i_price"]

            # getStockInfo
            if all_local and stockInfos != None:
                si = stockInfos[ol_i_id]
                assert si["s_i_id"] == ol_i_id, "s_i_id should be %d\n%s" % (ol_i_id, pformat(si))
            else:
                si = self.stock.find_one({"s_i_id": ol_i_id, "s_w_id": w_id}, {"s_i_id": 1, "s_quantity": 1, "s_data": 1, "s_ytd": 1, "s_order_cnt": 1, "s_remote_cnt": 1, s_dist_col: 1})
            assert si, "Failed to find s_i_id: %d\n%s" % (ol_i_id, pformat(itemInfo))

            s_quantity = si["s_quantity"]
            s_ytd = si["s_ytd"]
            s_order_cnt = si["s_order_cnt"]
            s_remote_cnt = si["s_remote_cnt"]
            s_data = si["s_data"]
            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
                s_dist_xx = si[s_dist_col] # Fetches data from the s_dist_[d_id] column
            else:
                s_dist_xx = si[s_dist_col][d_id-1] # Fetches data from the s_dists[d_id] column

            ## Update stock
            s_ytd += ol_quantity
            if s_quantity >= ol_quantity + 10:
                s_quantity = s_quantity - ol_quantity
            else:
                s_quantity = s_quantity + 91 - ol_quantity
            s_order_cnt += 1
            
            if ol_supply_w_id != w_id: s_remote_cnt += 1

            # updateStock
            self.stock.update_one(si, {"$set": {"s_quantity": s_quantity, "s_ytd": s_ytd, "s_order_cnt": s_order_cnt, "s_remote_cnt": s_remote_cnt}})

            if i_data.find(constants.ORIGINAL_STRING) != -1 and s_data.find(constants.ORIGINAL_STRING) != -1:
                brand_generic = 'B'
            else:
                brand_generic = 'G'
            ## Transaction profile states to use "ol_quantity * i_price"
            ol_amount = ol_quantity * i_price
            total += ol_amount

            ol = {"ol_number": ol_number, "ol_i_id": ol_i_id, "ol_supply_w_id": ol_supply_w_id, "ol_delivery_d": o_entry_d, "ol_quantity": ol_quantity, "ol_amount": ol_amount, "ol_dist_info": s_dist_xx}

            o["o_d_id"] = d_id
            o["o_w_id"] = w_id
            o["o_id"] = d_next_o_id
            o["o_orderline"] = ol
                
            # createOrderLine
            self.orders.update_one({"o_id": d_next_o_id, "o_d_id": d_id, "o_w_id": w_id}, {"$push": {"o_orderline": ol}})
            ## IF

            ## Add the info to be returned
            item_data.append( (i_name, s_quantity, brand_generic, i_price, ol_amount) )
        ## FOR
        
        ## Adjust the total for the discount
        #print "c_discount:", c_discount, type(c_discount)
        #print "w_tax:", w_tax, type(w_tax)
        #print "d_tax:", d_tax, type(d_tax)
        total *= (1 - c_discount) * (1 + w_tax + d_tax)

        ## Pack up values the client is missing (see TPC-C 2.4.3.5)
        misc = [ (w_tax, d_tax, d_next_o_id, total) ]
        
        return [ c, misc, item_data ]

    ## ----------------------------------------------
    ## doOrderStatus
    ## ----------------------------------------------
    def doOrderStatus(self, params):
        self.tx_status = ""
        w_id = params["w_id"]
        d_id = params["d_id"]
        c_id = params["c_id"]
        c_last = params["c_last"]
        
        assert w_id, pformat(params)
        assert d_id, pformat(params)

        search_fields = {"c_w_id": w_id, "c_d_id": d_id}
        if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            return_fields = {"c_id": 1, "c_first": 1, "c_middle": 1, "c_last": 1, "c_balance": 1}
        else:
            return_fields = {"c_id": 1, "c_name.c_first": 1, "c_name.c_middle": 1, "c_name.c_last": 1, "c_balance": 1}
        
        if c_id != None:
            # getCustomerByCustomerId
            search_fields["c_id"] = c_id
            c = self.customer.find_one(search_fields, return_fields)
            assert c
            
        else:
            # getCustomersByLastName
            # Get the midpoint customer's id
            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
                search_fields['c_last'] = c_last
            else:
                search_fields['c_name.c_last'] = c_last
            all_customers = self.customer.find(search_fields, return_fields)
            namecnt = self.customer.count_documents(search_fields)
            assert namecnt > 0
            index = int((namecnt-1)/2)
            c = all_customers[index]
            c_id = c["c_id"]
        assert len(c) > 0
        assert c_id != None

        orderLines = [ ]
        order = None
        
        # getLastOrder
        order = self.orders.find({"o_w_id": w_id, "o_d_id": d_id, "o_c_id": c_id}, {"o_id": 1, "o_carrier_id": 1, "o_entry_d": 1}).sort("o_id", direction=pymongo.DESCENDING).limit(1)[0]
        o_id = order["o_id"]

        if order:
            # getOrderLines
            orderLines = self.orders.find({"o_w_id": w_id, "o_d_id": d_id, "o_id": o_id}, {"o_orderline.ol_supply_w_id": 1, "o_orderline.ol_i_id": 1, "o_orderline.ol_quantity": 1, "o_orderline.ol_amount": 1, "o_orderline.ol_delivery_d": 1})
        ## IF
            
        return [ c, order, orderLines ]

    ## ----------------------------------------------
    ## doPayment
    ## ----------------------------------------------    
    def doPayment(self, params):
        self.tx_status = ""
        w_id = params["w_id"]
        d_id = params["d_id"]
        h_amount = params["h_amount"]
        c_w_id = params["c_w_id"]
        c_d_id = params["c_d_id"]
        c_id = params["c_id"]
        c_last = params["c_last"]
        h_date = params["h_date"]

        search_fields = {"c_w_id": w_id, "c_d_id": d_id}
        return_fields = {"c_balance": 0, "c_ytd_payment": 0, "c_payment_cnt": 0}
        
        if c_id != None:
            # getCustomerByCustomerId
            search_fields["c_id"] = c_id
            c = self.customer.find_one(search_fields, return_fields)
            assert c
        else:
            # getCustomersByLastName
            # Get the midpoint customer's id
            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
                search_fields['c_last'] = c_last
            else:
                search_fields['c_name.c_last'] = c_last
            all_customers = self.customer.find(search_fields, return_fields)
            namecnt = self.customer.count_documents(search_fields)
            assert namecnt > 0
            index = int((namecnt-1)/2)
            c = all_customers[index]
            c_id = c["c_id"]
        assert len(c) > 0
        assert c_id != None

        if c_id != None:
            # getCustomerByCustomerId
            c = self.customer.find_one({"c_w_id": w_id, "c_d_id": d_id, "c_id": c_id})
        else:
            # getCustomersByLastName
            # Get the midpoint customer's id
            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
                search_fields = {"c_w_id": w_id, "c_d_id": d_id, "c_last": c_last}
            else:
                search_fields = {"c_w_id": w_id, "c_d_id": d_id, "c_name.c_last": c_last}
            all_customers = self.customer.find(search_fields)
            namecnt = self.customer.count_documents(search_fields)
            assert namecnt > 0
            index = int((namecnt-1)/2)
            c = all_customers[index]
            c_id = c["c_id"]
        assert len(c) > 0
        assert c_id != None
        c_data = c["c_data"]


        # getWarehouse
        if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            w = self.warehouse.find_one({"w_id": w_id}, {"w_name": 1, "w_street_1": 1, "w_street_2": 1, "w_city": 1, "w_state": 1, "w_zip": 1})
        else:
            w = self.warehouse.find_one({"w_id": w_id}, {"w_name": 1, "w_address.w_street_1": 1, "w_address.w_street_2": 1, "w_address.w_city": 1, "w_address.w_state": 1, "w_address.w_zip": 1})
        assert w
        # updateWarehouseBalance
        self.warehouse.update_one({"_id": w["_id"]}, {"$inc": {"h_amount": h_amount}})

        # getDistrict
        if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            d = self.district.find_one({"d_w_id": w_id, "d_id": d_id}, {"d_name": 1, "d_street_1": 1, "d_street_2": 1, "d_city": 1, "d_state": 1, "d_zip": 1})
        else:
            d = self.district.find_one({"d_w_id": w_id, "d_id": d_id}, {"d_name": 1, "d_address.d_street_1": 1, "d_address.d_street_2": 1, "d_address.d_city": 1, "d_address.d_state": 1, "d_address.d_zip": 1})
        assert d
        # updateDistrictBalance
        self.district.update_one({"_id": d["_id"]},  {"$inc": {"d_ytd": h_amount}})

        # Build CUSTOMER update command 
        customer_update = {"$inc": {"c_balance": h_amount*-1, "c_ytd_payment": h_amount, "c_payment_cnt": 1}}
        
        # Customer Credit Information
        if c["c_credit"] == constants.BAD_CREDIT:
            newData = " ".join(map(str, [c_id, c_d_id, c_w_id, d_id, w_id, h_amount]))
            c_data = (newData + "|" + c_data)
            if len(c_data) > constants.MAX_C_DATA: c_data = c_data[:constants.MAX_C_DATA]
            customer_update["$set"] = {"c_data": c_data}
        ## IF
        # Concatenate w_name, four spaces, d_name
        h_data = "%s    %s" % (w["w_name"], d["d_name"])
        h = {"h_d_id": d_id, "h_w_id": w_id, "h_date": h_date, "h_amount": h_amount, "h_data": h_data}
        # updateCustomer
        self.customer.update_one({"_id": c["_id"]}, customer_update)
            
        # insertHistory
        self.history.insert_one(h)

        # TPC-C 2.5.3.3: Must display the following fields:
        # w_id, d_id, c_id, c_d_id, c_w_id, w_street_1, w_street_2, w_city, w_state, w_zip,
        # d_street_1, d_street_2, d_city, d_state, d_zip, c_first, c_middle, c_last, c_street_1,
        # c_street_2, c_city, c_state, c_zip, c_phone, c_since, c_credit, c_credit_lim,
        # c_discount, c_balance, the first 200 characters of c_data (only if c_credit = "BC"),
        # h_amount, and h_date.
        # Hand back all the warehouse, district, and customer data
        return [ w, d, c ]
        
    ## ----------------------------------------------
    ## doStockLevel
    ## ----------------------------------------------    
    def doStockLevel(self, params):
        self.tx_status = ""
        w_id = params["w_id"]
        d_id = params["d_id"]
        threshold = params["threshold"]
        
        # getOId
        d = self.district.find_one({"d_w_id": w_id, "d_id": d_id}, {"d_next_o_id": 1})
        assert d
        o_id = d["d_next_o_id"]
        
        # getStockCount
        # Outer Table: order_line
        # Inner Table: stock
        orderLines = self.orders.find({"o_w_id": w_id, "o_d_id": d_id, "o_id": {"$lt": o_id, "$gte": o_id-20}}, {"o_orderline.ol_i_id": 1})

        assert orderLines

        ol_ids = set()
        for oLines in orderLines:
            oLine = oLines["o_orderline"]
            for i in range(len(oLine)):
                olid = oLine[i]["ol_i_id"]
                ol_ids.add(olid)
        ## FOR
        result = self.stock.count_documents({"s_w_id": w_id, "s_i_id": {"$in": list(ol_ids)}, "s_quantity": {"$lt": threshold}})
        return int(result)

    def runCH2Queries(self, duration, endBenchmarkTime, queryIterNum):
        self.tx_status = ""
        qry_times = {}
        if self.TAFlag == "A":
            # ch2_queries_perm = list(constants.CH2_QUERIES.keys())
            # Pick a good seed based on client_id and query iteration number
            # to guarantee repeatibility of order between runs but still
            # good randomness for different clients and different query iterations.
            #random.seed(self.client_id*9973 + queryIterNum*19997)
            #random.shuffle(ch2_queries_perm)
            #logging.info(f"{self.schema=}")
            #logging.info(f"{self.analyticalQueries=}")

            ch2_queries_perm = constants.CH2_QUERIES_PERM[self.client_id]
            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
                ch2_queries = constants.CH2_MONGO_QUERIES
            else:
                ch2_queries = constants.CH2PP_MONGO_QUERIES

            if bool(int(os.environ.get("IGNORE_SKIP_INDEX_HINTS", 0))):
                pattern = re.compile(r"\/\*\+\sskip-index\s\*\/")
                ch2_queries = {
                    k: re.sub(pattern, "", v) for k, v in ch2_queries.items()
                }

            for qry in ch2_queries_perm:
                query_id_str = "AClient %d:Loop %d:%s:" % (self.client_id + 1, queryIterNum + 1, qry)
                query = ch2_queries[qry]
                pipeline = [ {"$sql": {"statement":query, "format":"jdbc", "dialect":"mongosql"}}]
                start = time.time()
                s = int(time.time_ns()) / 1000000
                self.database.aggregate(pipeline)
                e = int(time.time_ns()) / 1000000
                end = time.time()
                dur = str(e-s)+"ms"

                startTime = time.strftime("%H:%M:%S", time.localtime(start))

                # In benchmark run mode, if the duration has elapsed, stop executing queries
                if duration is not None:
                    if start > endBenchmarkTime:
                        logging.debug("%s started at:   %s (started after the duration of the benchmark)" % (query_id_str, startTime))
                        break

                logging.info("%s started at: %s" % (query_id_str, startTime))
                endTime = time.strftime("%H:%M:%S", time.localtime(end))

                # In benchmark run mode, if the duration has elapsed, stop reporting queries
                if duration is not None:
                    if end > endBenchmarkTime:
                        logging.debug("%s ended at:   %s (ended after the duration of the benchmark)" % (query_id_str, endTime))
                        break

                logging.info("%s ended at:   %s" % (query_id_str, endTime))

                qry_times[qry] = [
                    self.client_id + 1,
                    queryIterNum + 1,
                    startTime,
                    dur,
                    endTime,
                ]                
        return qry_times

## CLASS


