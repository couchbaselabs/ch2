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
NUM_LOAD_RETRIES = 10

TABLE_COLUMNS = {
    constants.MONGO_TABLENAME_ITEM: [
        "i_id", # INTEGER
        "i_im_id", # INTEGER
        "i_name", # VARCHAR
        "i_price", # FLOAT
        "i_data", # VARCHAR
        "i_extra", # Extra unused fields
    ],
    constants.MONGO_TABLENAME_WAREHOUSE: [
        "w_id", # SMALLINT
        "w_name", # VARCHAR
        "w_street_1", # VARCHAR
        "w_street_2", # VARCHAR
        "w_city", # VARCHAR
        "w_state", # VARCHAR
        "w_zip", # VARCHAR
        "w_tax", # FLOAT
        "w_ytd", # FLOAT
    ],
    constants.MONGO_TABLENAME_DISTRICT: [
        "d_id", # TINYINT
        "d_w_id", # SMALLINT
        "d_name", # VARCHAR
        "d_street_1", # VARCHAR
        "d_street_2", # VARCHAR
        "d_city", # VARCHAR
        "d_state", # VARCHAR
        "d_zip", # VARCHAR
        "d_tax", # FLOAT
        "d_ytd", # FLOAT
        "d_next_o_id", # INT
    ],
    constants.MONGO_TABLENAME_CUSTOMER:   [
        "c_id", # INTEGER
        "c_d_id", # TINYINT
        "c_w_id", # SMALLINT
        "c_first", # VARCHAR
        "c_middle", # VARCHAR
        "c_last", # VARCHAR
        "c_street_1", # VARCHAR
        "c_street_2", # VARCHAR
        "c_city", # VARCHAR
        "c_state", # VARCHAR
        "c_zip", # VARCHAR
        "c_phone", # VARCHAR
        "c_since", # TIMESTAMP
        "c_credit", # VARCHAR
        "c_credit_lim", # FLOAT
        "c_discount", # FLOAT
        "c_balance", # FLOAT
        "c_ytd_payment", # FLOAT
        "c_payment_cnt", # INTEGER
        "c_delivery_cnt", # INTEGER
        "c_data", # VARCHAR
        "c_extra", # Extra unused fields
    ],
    constants.MONGO_TABLENAME_STOCK:      [
        "s_i_id", # INTEGER
        "s_w_id", # SMALLINT
        "s_quantity", # INTEGER
        "s_dist_01", # VARCHAR
        "s_dist_02", # VARCHAR
        "s_dist_03", # VARCHAR
        "s_dist_04", # VARCHAR
        "s_dist_05", # VARCHAR
        "s_dist_06", # VARCHAR
        "s_dist_07", # VARCHAR
        "s_dist_08", # VARCHAR
        "s_dist_09", # VARCHAR
        "s_dist_10", # VARCHAR
        "s_ytd", # INTEGER
        "s_order_cnt", # INTEGER
        "s_remote_cnt", # INTEGER
        "s_data", # VARCHAR
    ],
    constants.MONGO_TABLENAME_ORDERS:     [
        "o_id", # INTEGER
        "o_c_id", # INTEGER
        "o_d_id", # TINYINT
        "o_w_id", # SMALLINT
        "o_entry_d", # TIMESTAMP
        "o_carrier_id", # INTEGER
        "o_ol_cnt", # INTEGER
        "o_all_local", # INTEGER
        "o_extra", # Extra unused fields
        "o_orderline", # ARRAY
    ],
    constants.MONGO_TABLENAME_NEWORDER:  [
        "no_o_id", # INTEGER
        "no_d_id", # TINYINT
        "no_w_id", # SMALLINT
    ],
    constants.MONGO_TABLENAME_ORDERLINE: [
#        "ol_o_id", # INTEGER
#        "ol_d_id", # TINYINT
#        "ol_w_id", # SMALLINT
        "ol_number", # INTEGER
        "ol_i_id", # INTEGER
        "ol_supply_w_id", # SMALLINT
        "ol_delivery_d", # TIMESTAMP
        "ol_quantity", # INTEGER
        "ol_amount", # FLOAT
        "ol_dist_info", # VARCHAR
    ],
    constants.MONGO_TABLENAME_HISTORY:    [
        "h_c_id", # INTEGER
        "h_c_d_id", # TINYINT
        "h_c_w_id", # SMALLINT
        "h_d_id", # TINYINT
        "h_w_id", # SMALLINT
        "h_date", # TIMESTAMP
        "h_amount", # FLOAT
        "h_data", # VARCHAR
    ],
    constants.MONGO_TABLENAME_SUPPLIER:    [
        "su_suppkey", # INTEGER
        "su_name", # VARCHAR
        "su_address", # VARCHAR
        "su_nationkey", # INTEGER
        "su_phone", # VARCHAR
        "su_acctbal", # FLOAT
        "su_comment", # VARCHAR
    ],
    constants.MONGO_TABLENAME_NATION:    [
        "n_nationkey", # INTEGER
        "n_name", # VARCHAR
        "n_regionkey", # INTEGER
        "n_comment", # VARCHAR
    ],
    constants.MONGO_TABLENAME_REGION:    [
        "r_regionkey", # INTEGER
        "r_name", # VARCHAR
        "r_comment", # VARCHAR
    ],
}

CH2PP_TABLE_COLUMNS = {
    constants.MONGO_TABLENAME_ITEM: [
        "i_id", # INTEGER
        "i_name", # VARCHAR
        "i_price", # FLOAT
        "i_extra", # Extra unused fields
        "i_categories", # ARRAY
        "i_data", # VARCHAR
        "i_im_id", # INTEGER
    ],
    constants.MONGO_TABLENAME_WAREHOUSE: [
        "w_id", # SMALLINT
        "w_ytd", # FLOAT
        "w_tax", # FLOAT
        "w_name", # VARCHAR
        "w_address", # JSON
    ],
    constants.MONGO_TABLENAME_DISTRICT: [
        "d_id", # TINYINT
        "d_w_id", # SMALLINT
        "d_ytd", # FLOAT
        "d_tax", # FLOAT
        "d_next_o_id", # INT
        "d_name", # VARCHAR
        "d_address", # JSON
    ],
    constants.MONGO_TABLENAME_CUSTOMER:   [
        "c_id", # INTEGER
        "c_d_id", # TINYINT
        "c_w_id", # SMALLINT
        "c_discount", # FLOAT
        "c_credit", # VARCHAR
        "c_name", # JSON OBJECT
        "c_credit_lim", # FLOAT
        "c_balance", # FLOAT
        "c_ytd_payment", # FLOAT
        "c_payment_cnt", # INTEGER
        "c_delivery_cnt", # INTEGER
        "c_extra", # Extra unused fields
        "c_addresses", # ARRAY
        "c_phones", # ARRAY
        "c_since", # TIMESTAMP
        "c_item_categories", # ARRAY
        "c_data", # VARCHAR
    ],
    constants.MONGO_TABLENAME_STOCK:      [
        "s_i_id", # INTEGER
        "s_w_id", # SMALLINT
        "s_quantity", # INTEGER
        "s_ytd", # INTEGER
        "s_order_cnt", # INTEGER
        "s_remote_cnt", # INTEGER
        "s_data", # VARCHAR
        "s_dists", # ARRAY
    ],
    constants.MONGO_TABLENAME_ORDERS:     [
        "o_id", # INTEGER
        "o_c_id", # INTEGER
        "o_d_id", # TINYINT
        "o_w_id", # SMALLINT
        "o_carrier_id", # INTEGER
        "o_ol_cnt", # INTEGER
        "o_all_local", # INTEGER
        "o_entry_d", # TIMESTAMP
        "o_extra", # Extra unused fields
        "o_orderline", # ARRAY
    ],
    constants.MONGO_TABLENAME_NEWORDER:  [
        "no_o_id", # INTEGER
        "no_d_id", # TINYINT
        "no_w_id", # SMALLINT
    ],
    constants.MONGO_TABLENAME_ORDERLINE: [
#        "ol_o_id", # INTEGER
#        "ol_d_id", # TINYINT
#        "ol_w_id", # SMALLINT
        "ol_number", # INTEGER
        "ol_i_id", # INTEGER
        "ol_supply_w_id", # SMALLINT
        "ol_delivery_d", # TIMESTAMP
        "ol_quantity", # INTEGER
        "ol_amount", # FLOAT
        "ol_dist_info", # VARCHAR
    ],
    constants.MONGO_TABLENAME_HISTORY:    [
        "h_c_id", # INTEGER
        "h_c_d_id", # TINYINT
        "h_c_w_id", # SMALLINT
        "h_d_id", # TINYINT
        "h_w_id", # SMALLINT
        "h_date", # TIMESTAMP
        "h_amount", # FLOAT
        "h_data", # VARCHAR
    ],
    constants.MONGO_TABLENAME_SUPPLIER:    [
        "su_suppkey", # INTEGER
        "su_name", # VARCHAR
        "su_address", # JSON
        "su_nationkey", # INTEGER
        "su_phone", # VARCHAR
        "su_acctbal", # FLOAT
        "su_comment", # VARCHAR
    ],
    constants.MONGO_TABLENAME_NATION:    [
        "n_nationkey", # INTEGER
        "n_name", # VARCHAR
        "n_regionkey", # INTEGER
        "n_comment", # VARCHAR
    ],
    constants.MONGO_TABLENAME_REGION:    [
        "r_regionkey", # INTEGER
        "r_name", # VARCHAR
        "r_comment", # VARCHAR
    ],
    constants.MONGO_TABLENAME_WAREHOUSE_ADDRESS:    [
        "w_street_1", # VARCHAR
        "w_street_2", # VARCHAR
        "w_city", # VARCHAR
        "w_state", # VARCHAR
        "w_zip", # VARCHAR
    ],
    constants.MONGO_TABLENAME_DISTRICT_ADDRESS:    [
        "d_street_1", # VARCHAR
        "d_street_2", # VARCHAR
        "d_city", # VARCHAR
        "d_state", # VARCHAR
        "d_zip", # VARCHAR
    ],
    constants.MONGO_TABLENAME_CUSTOMER_NAME:    [
        "c_last", # VARCHAR
        "c_first", # VARCHAR
        "c_middle", # VARCHAR
    ],
    constants.MONGO_TABLENAME_CUSTOMER_ADDRESSES:    [
        "c_address_kind", # VARCHAR
        "c_street_1", # VARCHAR
        "c_street_2", # VARCHAR
        "c_city", # VARCHAR
        "c_state", # VARCHAR
        "c_zip", # VARCHAR
    ],
    constants.MONGO_TABLENAME_CUSTOMER_PHONES:    [
        "c_phone_kind", # VARCHAR
        "c_phone_number", # VARCHAR
    ],
    constants.MONGO_TABLENAME_SUPPLIER_ADDRESS:    [
        "su_street_1", # VARCHAR
        "su_street_2", # VARCHAR
        "su_city", # VARCHAR
        "su_state", # VARCHAR
        "su_zip", # VARCHAR
    ],
}

TABLE_INDEXES = {
    constants.TABLENAME_ITEM: [
        "I_ID",
    ],
    constants.TABLENAME_WAREHOUSE: [
        "W_ID",
    ],    
    constants.TABLENAME_DISTRICT: [
        "D_ID",
        "D_W_ID",
    ],
    constants.TABLENAME_CUSTOMER:   [
        "C_ID",
        "C_D_ID",
        "C_W_ID",
    ],
    constants.TABLENAME_STOCK:      [
        "S_I_ID",
        "S_W_ID",
    ],
    constants.TABLENAME_ORDERS:     [
        "O_ID",
        "O_D_ID",
        "O_W_ID",
        "O_C_ID",
    ],
    constants.TABLENAME_NEWORDER:  [
        "NO_O_ID",
        "NO_D_ID",
        "NO_W_ID",
    ],
    constants.TABLENAME_ORDERLINE: [
        "OL_O_ID",
        "OL_D_ID",
        "OL_W_ID",
    ],
}

## ==============================================
## MongodbDriver
## ==============================================
class MongodbDriver(AbstractDriver):
    DEFAULT_CONFIG = {
        "host":         ("The hostname to mongod", "localhost" ),
        "port":         ("The port number to mongod", 27017 ),
        "name":         ("Collection name", "tpcc"),
        "denormalize":  ("If set to true, then the CUSTOMER data will be denormalized into a single document", True),
    }
    DENORMALIZED_TABLES = [
        constants.TABLENAME_CUSTOMER,
        constants.TABLENAME_ORDERS,
        constants.TABLENAME_ORDERLINE,
        constants.TABLENAME_HISTORY,
    ]
    
    
    def __init__(self, ddl, clientId, TAFlag="T",
                 schema=constants.CH2_DRIVER_SCHEMA["CH2"],
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
            uri = "mongodb+srv://"+user+":"+password+"@"+data_node+"/?retryWrites=true&w=majority&appName="+cluster
            #cluster0.ogw88.mongodb.net
            self.client_id = clientId;
            self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            self.database = self.client["ch2"]
            self.denormalize = False
            self.schema = schema
            self.analyticalQueries = analyticalQueries
            self.customerExtraFields = customerExtraFields
            self.ordersExtraFields = ordersExtraFields
            self.itemExtraFields = itemExtraFields
            self.bulkload_batch_size = bulkload_batch_size

            self.collections = {}
            for tableName in constants.MONGO_ALL_TABLES:
                self.collections[tableName] = self.database.get_collection(constants.MONGO_COLLECTIONS_DICT[tableName])

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
        if self.denormalize: logging.debug("Using denormalized data model")
        
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
            if self.denormalize and name in MongodbDriver.DENORMALIZED_TABLES[1:]: continue
            
            ## Create member mapping to collections
            self.__dict__[name.lower()] = self.database[name]
            
            ## Create Indexes
            if load_indexes and name in TABLE_INDEXES and \
            (self.denormalize or (self.denormalize == False and not name in MongodbDriver.DENORMALIZED_TABLES[1:])):
                logging.debug("Creating index for %s" % name)
                for index in TABLE_INDEXES[name]:
                	self.database[name].create_index(index)
        ## FOR

    def tryBulkLoad(self, collection, cur_batch):
        for i in range(NUM_LOAD_RETRIES):
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

        logging.debug("Client ID # %d failed bulk load data into KV after %d retries" % (self.client_id, NUM_LOAD_RETRIES))
        return False

    ## ----------------------------------------------
    ## loadTuples for mongodb
    ## ----------------------------------------------
    def loadTuples(self, tableName, tuples):
        if len(tuples) == 0:
            return

        tableName = tableName[18:]

        logging.debug("Loading %d tuples for tableName %s" % (len(tuples), tableName))
        
        assert tableName in TABLE_COLUMNS, "Unexpected table %s" % tableName

        collection = self.collections[tableName]
        # For bulk load: load in batches
        cur_batch = []
        cur_size = 0
        for t in tuples:
            val = self.getOneDoc(tableName, t, False)
            cur_batch.append(val)
            cur_size += 1
            if cur_size > 10000: #self.bulkload_batch_size:
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
        
    def getOneDoc(self, tableName, tuple, denorm):
        if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            return self.getOneCH2Doc(tableName, tuple, denorm)
        else:
            return self.getOneCH2PPDoc(tableName, tuple, denorm)

    def getOneCH2Doc(self, tableName, tuple, denorm):
        columns = TABLE_COLUMNS[tableName]
        if denorm:
            val = tuple
        else:
            val = {}
            for l, v in enumerate(tuple):
                v1 = tuple[l]
                if tableName == constants.MONGO_TABLENAME_ORDERS and columns[l] == "o_orderline":
                    v1 = []
                    for olv in v:
                        v1.append(self.genNestedTuple(olv, constants.MONGO_TABLENAME_ORDERLINE))
                elif tableName == constants.MONGO_TABLENAME_CUSTOMER and columns[l] == "c_extra":
                    for i in range(0, self.customerExtraFields):
                        val[columns[l]+"_"+str(format(i+1, "03d"))] = v1[i]
                    continue
                elif tableName == constants.MONGO_TABLENAME_ORDERS and columns[l] == "o_extra":
                    for i in range(0, self.ordersExtraFields):
                        val[columns[l]+"_"+str(format(i+1, "03d"))] = v1[i]
                    continue
                elif tableName == constants.MONGO_TABLENAME_ITEM and columns[l] == "i_extra":
                    for i in range(0, self.itemExtraFields):
                        val[columns[l]+"_"+str(format(i+1, "03d"))] = v1[i]
                    continue
                elif isinstance(v1,(datetime)):
                    v1 = str(v1)
                val[columns[l]] = v1

        return val

    def getOneCH2PPDoc(self, tableName, tuple, denorm):
        columns = CH2PP_TABLE_COLUMNS[tableName]
        if denorm:
            val = tuple
        else:
            val = {}
            for l, v in enumerate(tuple):
                v1 = tuple[l]
                if isinstance(v1,(datetime)):
                    v1 = str(v1)
                elif tableName == constants.MONGO_TABLENAME_ORDERS and columns[l] == "o_orderline":
                    v1 = []
                    for olv in v:
                        v1.append(self.genNestedTuple(olv, constants.MONGO_TABLENAME_ORDERLINE))
                elif (self.schema == constants.CH2_DRIVER_SCHEMA["CH2P"] and
                      (tableName == constants.MONGO_TABLENAME_ITEM and columns[l] == "i_categories" or
                       tableName == constants.MONGO_TABLENAME_CUSTOMER and columns[l] == "c_item_categories")):
                    continue
                elif tableName == constants.MONGO_TABLENAME_WAREHOUSE and columns[l] == "w_address":
                    v1 = self.genNestedTuple(v, constants.MONGO_TABLENAME_WAREHOUSE_ADDRESS)
                elif tableName == constants.MONGO_TABLENAME_DISTRICT and columns[l] == "d_address":
                    v1 = self.genNestedTuple(v, constants.MONGO_TABLENAME_DISTRICT_ADDRESS)
                elif tableName == constants.MONGO_TABLENAME_SUPPLIER and columns[l] == "su_address":
                    v1 = self.genNestedTuple(v, constants.MONGO_TABLENAME_SUPPLIER_ADDRESS)
                elif tableName == constants.MONGO_TABLENAME_CUSTOMER:
                    if columns[l] == "c_name":
                        v1 = self.genNestedTuple(v, constants.MONGO_TABLENAME_CUSTOMER_NAME)
                    elif columns[l] == "c_extra":
                        for i in range(0, self.customerExtraFields):
                            val[columns[l]+"_"+str(format(i+1, "03d"))] = v1[i]
                        continue
                    elif columns[l] == "c_addresses":
                        v1 = []
                        for clv in v:
                            v1.append(self.genNestedTuple(clv, constants.MONGO_TABLENAME_CUSTOMER_ADDRESSES))
                            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2P"]:
                                break # Load only one customer address for CH2P
                    elif columns[l] == "c_phones":
                        v1 = []
                        for clv in v:
                            v1.append(self.genNestedTuple(clv, constants.MONGO_TABLENAME_CUSTOMER_PHONES))
                            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2P"]:
                                break # Load only one customer phone for CH2P
                elif tableName == constants.MONGO_TABLENAME_ORDERS and columns[l] == "o_extra":
                    for i in range(0, self.ordersExtraFields):
                        val[columns[l]+"_"+str(format(i+1, "03d"))] = v1[i]
                    continue
                elif tableName == constants.MONGO_TABLENAME_ITEM and columns[l] == "i_extra":
                    for i in range(0, self.itemExtraFields):
                        val[columns[l]+"_"+str(format(i+1, "03d"))] = v1[i]
                    continue
                val[columns[l]] = v1
        return val

    def genNestedTuple(self, tuple, tableName):
        if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
            columns = TABLE_COLUMNS[tableName]
        else:
            columns = CH2PP_TABLE_COLUMNS[tableName]
        rval = {}
        for l, v in enumerate(tuple):
            if isinstance(v,(datetime)):
                v = str(v)
            rval[columns[l]] = v
        return rval

    ## ----------------------------------------------
    ## loadFinishDistrict
    ## ----------------------------------------------
    def loadFinishDistrict(self, w_id, d_id):
        if self.denormalize:
            logging.debug("Pushing %d denormalized CUSTOMER records for WAREHOUSE %d DISTRICT %d into MongoDB" % (len(self.w_customers), w_id, d_id))
            self.database[constants.MONGO_TABLENAME_CUSTOMER].insert(self.w_customers.values())
            self.w_customers.clear()
            self.w_orders.clear()
        ## IF

    ## ----------------------------------------------
    ## loadFinish
    ## ----------------------------------------------
    def loadFinish(self):
        logging.info("Client ID # %d Finished loading tables" % (self.client_id))
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            for name in constants.ALL_TABLES:
                if self.denormalize and name in MongodbDriver.DENORMALIZED_TABLES[1:]: continue
                logging.debug("%-12s%d records" % (name+":", self.database[name].count()))
        ## IF

    ## ----------------------------------------------
    ## doDelivery
    ## ----------------------------------------------
    def doDelivery(self, params):
        w_id = params["w_id"]
        o_carrier_id = params["o_carrier_id"]
        ol_delivery_d = params["ol_delivery_d"]
        
        result = [ ]
        for d_id in range(1, constants.DISTRICTS_PER_WAREHOUSE+1):
            ## getNewOrder
            no = self.new_order.find_one({"NO_D_ID": d_id, "NO_W_ID": w_id}, {"NO_O_ID": 1})
            if no == None:
                ## No orders for this district: skip it. Note: This must be reported if > 1%
                continue
            assert len(no) > 0
            o_id = no["NO_O_ID"]
            
            if self.denormalize:
                ## getCId
                c = self.customer.find_one({"ORDERS.O_ID": o_id, "C_D_ID": d_id, "C_W_ID": w_id}, {"C_ID": 1, "ORDERS.O_ID": 1, "ORDERS.ORDER_LINE": 1})
                assert c != None, "No customer record [O_ID=%d, D_ID=%d, W_ID=%d]" % (o_id, d_id, w_id)
                c_id = c["C_ID"]
                
                ## sumOLAmount + updateOrderLine
                ol_total = 0
                for o in c["ORDERS"]:
                    if o["O_ID"] == o_id:
                        orderLines = o["ORDER_LINE"]
                        for ol in orderLines:
                            ol_total += ol["OL_AMOUNT"]
                            ## We have to do this here because we can't update the nested array atomically
                            ol["OL_DELIVERY_D"] = ol_delivery_d
                        break
                ## FOR
                    
                if ol_total == 0:
                    pprint(params)
                    pprint(no)
                    pprint(c)
                    sys.exit(1)

                ## updateOrders + updateCustomer
                self.customer.update({"_id": c['_id'], "ORDERS.O_ID": o_id}, {"$set": {"ORDERS.$.O_CARRIER_ID": o_carrier_id, "ORDERS.$.ORDER_LINE": orderLines}, "$inc": {"C_BALANCE": ol_total}}, multi=False)

            else:
                ## getCId
                o = self.orders.find_one({"O_ID": o_id, "O_D_ID": d_id, "O_W_ID": w_id}, {"O_C_ID": 1})
                assert o != None
                c_id = o["O_C_ID"]
                
                ## sumOLAmount
                orderLines = self.order_line.find({"OL_O_ID": o_id, "OL_D_ID": d_id, "OL_W_ID": w_id}, {"OL_AMOUNT": 1})
                assert orderLines != None
                ol_total = sum([ol["OL_AMOUNT"] for ol in orderLines])
                
                ## updateOrders
                self.orders.update(o, {"$set": {"O_CARRIER_ID": o_carrier_id}}, multi=False)
            
                ## updateOrderLine
                self.order_line.update({"OL_O_ID": o_id, "OL_D_ID": d_id, "OL_W_ID": w_id}, {"$set": {"OL_DELIVERY_D": ol_delivery_d}}, multi=True)
                
                ## updateCustomer
                self.customer.update({"C_ID": c_id, "C_D_ID": d_id, "C_W_ID": w_id}, {"$inc": {"C_BALANCE": ol_total}})
            ## IF

            ## deleteNewOrder
            self.new_order.remove({"_id": no['_id']})

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
        w_id = params["w_id"]
        d_id = params["d_id"]
        c_id = params["c_id"]
        o_entry_d = params["o_entry_d"]
        i_ids = params["i_ids"]
        i_w_ids = params["i_w_ids"]
        i_qtys = params["i_qtys"]
        s_dist_col = "S_DIST_%02d" % d_id
            
        assert len(i_ids) > 0
        assert len(i_ids) == len(i_w_ids)
        assert len(i_ids) == len(i_qtys)

        ## http://stackoverflow.com/q/3844931/
        all_local = (not i_w_ids or [w_id] * len(i_w_ids) == i_w_ids)
        
        items = self.item.find({"I_ID": {"$in": i_ids}}, {"I_ID": 1, "I_PRICE": 1, "I_NAME": 1, "I_DATA": 1})
        ## TPCC defines 1% of neworder gives a wrong itemid, causing rollback.
        ## Note that this will happen with 1% of transactions on purpose.
        if items.count() != len(i_ids):
            ## TODO Abort here!
            return
        ## IF
        
        ## ----------------
        ## Collect Information from WAREHOUSE, DISTRICT, and CUSTOMER
        ## ----------------
        
        # getWarehouseTaxRate
        w = self.warehouse.find_one({"W_ID": w_id}, {"W_TAX": 1})
        assert w
        w_tax = w["W_TAX"]
        
        # getDistrict
        d = self.district.find_one({"D_ID": d_id, "D_W_ID": w_id}, {"D_TAX": 1, "D_NEXT_O_ID": 1})
        assert d
        d_tax = d["D_TAX"]
        d_next_o_id = d["D_NEXT_O_ID"]
        
        # incrementNextOrderId
        # HACK: This is not transactionally safe!
        self.district.update(d, {"$inc": {"D_NEXT_O_ID": 1}}, multi=False)
        
        # getCustomer
        c = self.customer.find_one({"C_ID": c_id, "C_D_ID": d_id, "C_W_ID": w_id}, {"C_DISCOUNT": 1, "C_LAST": 1, "C_CREDIT": 1})
        assert c
        c_discount = c["C_DISCOUNT"]

        ## ----------------
        ## Insert Order Information
        ## ----------------
        ol_cnt = len(i_ids)
        o_carrier_id = constants.NULL_CARRIER_ID

        # createNewOrder
        self.new_order.insert({"NO_O_ID": d_next_o_id, "NO_D_ID": d_id, "NO_W_ID": w_id})

        o = {"O_ID": d_next_o_id, "O_ENTRY_D": o_entry_d, "O_CARRIER_ID": o_carrier_id, "O_OL_CNT": ol_cnt, "O_ALL_LOCAL": all_local}
        if self.denormalize:
            o[constants.TABLENAME_ORDER_LINE] = [ ]
        else:
            o["O_D_ID"] = d_id
            o["O_W_ID"] = w_id
            o["O_C_ID"] = c_id
            
            # createOrder
            self.orders.insert(o)  
            
        ## ----------------
        ## OPTIMIZATION:
        ## If all of the items are at the same warehouse, then we'll issue a single
        ## request to get their information
        ## ----------------
        stockInfos = None
        if all_local and False:
            # getStockInfo
            allStocks = self.stock.find({"S_I_ID": {"$in": i_ids}, "S_W_ID": w_id}, {"S_I_ID": 1, "S_QUANTITY": 1, "S_DATA": 1, "S_YTD": 1, "S_ORDER_CNT": 1, "S_REMOTE_CNT": 1, s_dist_col: 1})
            assert allStocks.count() == ol_cnt
            stockInfos = { }
            for si in allStocks:
                stockInfos["S_I_ID"] = si # HACK
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
            i_name = itemInfo["I_NAME"]
            i_data = itemInfo["I_DATA"]
            i_price = itemInfo["I_PRICE"]

            # getStockInfo
            if all_local and stockInfos != None:
                si = stockInfos[ol_i_id]
                assert si["S_I_ID"] == ol_i_id, "S_I_ID should be %d\n%s" % (ol_i_id, pformat(si))
            else:
                si = self.stock.find_one({"S_I_ID": ol_i_id, "S_W_ID": w_id}, {"S_I_ID": 1, "S_QUANTITY": 1, "S_DATA": 1, "S_YTD": 1, "S_ORDER_CNT": 1, "S_REMOTE_CNT": 1, s_dist_col: 1})
            assert si, "Failed to find S_I_ID: %d\n%s" % (ol_i_id, pformat(itemInfo))

            s_quantity = si["S_QUANTITY"]
            s_ytd = si["S_YTD"]
            s_order_cnt = si["S_ORDER_CNT"]
            s_remote_cnt = si["S_REMOTE_CNT"]
            s_data = si["S_DATA"]
            s_dist_xx = si[s_dist_col] # Fetches data from the s_dist_[d_id] column

            ## Update stock
            s_ytd += ol_quantity
            if s_quantity >= ol_quantity + 10:
                s_quantity = s_quantity - ol_quantity
            else:
                s_quantity = s_quantity + 91 - ol_quantity
            s_order_cnt += 1
            
            if ol_supply_w_id != w_id: s_remote_cnt += 1

            # updateStock
            self.stock.update(si, {"$set": {"S_QUANTITY": s_quantity, "S_YTD": s_ytd, "S_ORDER_CNT": s_order_cnt, "S_REMOTE_CNT": s_remote_cnt}})

            if i_data.find(constants.ORIGINAL_STRING) != -1 and s_data.find(constants.ORIGINAL_STRING) != -1:
                brand_generic = 'B'
            else:
                brand_generic = 'G'
            ## Transaction profile states to use "ol_quantity * i_price"
            ol_amount = ol_quantity * i_price
            total += ol_amount

            ol = {"OL_O_ID": d_next_o_id, "OL_NUMBER": ol_number, "OL_I_ID": ol_i_id, "OL_SUPPLY_W_ID": ol_supply_w_id, "OL_DELIVERY_D": o_entry_d, "OL_QUANTITY": ol_quantity, "OL_AMOUNT": ol_amount, "OL_DIST_INFO": s_dist_xx}

            if self.denormalize:
                # createOrderLine
                o[constants.TABLENAME_ORDER_LINE].append(ol)
            else:
                ol["OL_D_ID"] = d_id
                ol["OL_W_ID"] = w_id
                
                # createOrderLine
                self.order_line.insert(ol)
            ## IF

            ## Add the info to be returned
            item_data.append( (i_name, s_quantity, brand_generic, i_price, ol_amount) )
        ## FOR
        
        ## Adjust the total for the discount
        #print "c_discount:", c_discount, type(c_discount)
        #print "w_tax:", w_tax, type(w_tax)
        #print "d_tax:", d_tax, type(d_tax)
        total *= (1 - c_discount) * (1 + w_tax + d_tax)

        # createOrder
        self.customer.update({"_id": c["_id"]}, {"$push": {"ORDERS": o}})

        ## Pack up values the client is missing (see TPC-C 2.4.3.5)
        misc = [ (w_tax, d_tax, d_next_o_id, total) ]
        
        return [ c, misc, item_data ]

    ## ----------------------------------------------
    ## doOrderStatus
    ## ----------------------------------------------
    def doOrderStatus(self, params):
        w_id = params["w_id"]
        d_id = params["d_id"]
        c_id = params["c_id"]
        c_last = params["c_last"]
        
        assert w_id, pformat(params)
        assert d_id, pformat(params)

        search_fields = {"C_W_ID": w_id, "C_D_ID": d_id}
        return_fields = {"C_ID": 1, "C_FIRST": 1, "C_MIDDLE": 1, "C_LAST": 1, "C_BALANCE": 1}
        if self.denormalize:
            for f in ['O_ID', 'O_CARRIER_ID', 'O_ENTRY_D']:
                return_fields["%s.%s" % (constants.TABLENAME_ORDERS, f)] = 1
            for f in ['OL_SUPPLY_W_ID', 'OL_I_ID', 'OL_QUANTITY']:
                return_fields["%s.%s.%s" % (constants.TABLENAME_ORDERS, constants.TABLENAME_ORDER_LINE, f)] = 1
        ## IF
        
        if c_id != None:
            # getCustomerByCustomerId
            search_fields["C_ID"] = c_id
            c = self.customer.find_one(search_fields, return_fields)
            assert c
            
        else:
            # getCustomersByLastName
            # Get the midpoint customer's id
            search_fields['C_LAST'] = c_last
            
            all_customers = self.customer.find(search_fields, return_fields)
            namecnt = all_customers.count()
            assert namecnt > 0
            index = (namecnt-1)/2
            c = all_customers[index]
            c_id = c["C_ID"]
        assert len(c) > 0
        assert c_id != None

        orderLines = [ ]
        order = None
        
        if self.denormalize:
            # getLastOrder
            if constants.TABLENAME_ORDERS in c:
                order = c[constants.TABLENAME_ORDERS][-1]
                # getOrderLines
                orderLines = order[constants.TABLENAME_ORDER_LINE]
        else:
            # getLastOrder
            order = self.orders.find({"O_W_ID": w_id, "O_D_ID": d_id, "O_C_ID": c_id}, {"O_ID": 1, "O_CARRIER_ID": 1, "O_ENTRY_D": 1}).sort("O_ID", direction=pymongo.DESCENDING).limit(1)[0]
            o_id = order["O_ID"]

            if order:
                # getOrderLines
                orderLines = self.order_line.find({"OL_W_ID": w_id, "OL_D_ID": d_id, "OL_O_ID": o_id}, {"OL_SUPPLY_W_ID": 1, "OL_I_ID": 1, "OL_QUANTITY": 1, "OL_AMOUNT": 1, "OL_DELIVERY_D": 1})
        ## IF
            

        return [ c, order, orderLines ]

    ## ----------------------------------------------
    ## doPayment
    ## ----------------------------------------------    
    def doPayment(self, params):
        w_id = params["w_id"]
        d_id = params["d_id"]
        h_amount = params["h_amount"]
        c_w_id = params["c_w_id"]
        c_d_id = params["c_d_id"]
        c_id = params["c_id"]
        c_last = params["c_last"]
        h_date = params["h_date"]

        search_fields = {"C_W_ID": w_id, "C_D_ID": d_id}
        return_fields = {"C_BALANCE": 0, "C_YTD_PAYMENT": 0, "C_PAYMENT_CNT": 0}
        
        if c_id != None:
            # getCustomerByCustomerId
            search_fields["C_ID"] = c_id
            c = self.customer.find_one(search_fields, return_fields)
            assert c
            
        else:
            # getCustomersByLastName
            # Get the midpoint customer's id
            search_fields['C_LAST'] = c_last
            all_customers = self.customer.find(search_fields, return_fields)
            namecnt = all_customers.count()
            assert namecnt > 0
            index = (namecnt-1)/2
            c = all_customers[index]
            c_id = c["C_ID"]
        assert len(c) > 0
        assert c_id != None
        
        if c_id != None:
            # getCustomerByCustomerId
            c = self.customer.find_one({"C_W_ID": w_id, "C_D_ID": d_id, "C_ID": c_id})
        else:
            # getCustomersByLastName
            # Get the midpoint customer's id
            all_customers = self.customer.find({"C_W_ID": w_id, "C_D_ID": d_id, "C_LAST": c_last})
            namecnt = all_customers.count()
            assert namecnt > 0
            index = (namecnt-1)/2
            c = all_customers[index]
            c_id = c["C_ID"]
        assert len(c) > 0
        assert c_id != None
        c_data = c["C_DATA"]

        # getWarehouse
        w = self.warehouse.find_one({"W_ID": w_id}, {"W_NAME": 1, "W_STREET_1": 1, "W_STREET_2": 1, "W_CITY": 1, "W_STATE": 1, "W_ZIP": 1})
        assert w
        
        # updateWarehouseBalance
        self.warehouse.update({"_id": w["_id"]}, {"$inc": {"H_AMOUNT": h_amount}})

        # getDistrict
        d = self.district.find_one({"D_W_ID": w_id, "D_ID": d_id}, {"D_NAME": 1, "D_STREET_1": 1, "D_STREET_2": 1, "D_CITY": 1, "D_STATE": 1, "D_ZIP": 1})
        assert d
        
        # updateDistrictBalance
        self.district.update({"_id": d["_id"]},  {"$inc": {"D_YTD": h_amount}})

        # Build CUSTOMER update command 
        customer_update = {"$inc": {"C_BALANCE": h_amount*-1, "C_YTD_PAYMENT": h_amount, "C_PAYMENT_CNT": 1}}
        
        # Customer Credit Information
        if c["C_CREDIT"] == constants.BAD_CREDIT:
            newData = " ".join(map(str, [c_id, c_d_id, c_w_id, d_id, w_id, h_amount]))
            c_data = (newData + "|" + c_data)
            if len(c_data) > constants.MAX_C_DATA: c_data = c_data[:constants.MAX_C_DATA]
            customer_update["$set"] = {"C_DATA": c_data}
        ## IF

        # Concatenate w_name, four spaces, d_name
        h_data = "%s    %s" % (w["W_NAME"], d["D_NAME"])
        h = {"H_D_ID": d_id, "H_W_ID": w_id, "H_DATE": h_date, "H_AMOUNT": h_amount, "H_DATA": h_data}
        if self.denormalize:
            # insertHistory + updateCustomer
            customer_update["$push"] = {constants.TABLENAME_HISTORY: h}
            self.customer.update({"_id": c["_id"]}, customer_update)
        else:
            # updateCustomer
            self.customer.update({"_id": c["_id"]}, customer_update)
            
            # insertHistory
            self.history.insert(h)

        # TPC-C 2.5.3.3: Must display the following fields:
        # W_ID, D_ID, C_ID, C_D_ID, C_W_ID, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP,
        # D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1,
        # C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM,
        # C_DISCOUNT, C_BALANCE, the first 200 characters of C_DATA (only if C_CREDIT = "BC"),
        # H_AMOUNT, and H_DATE.

        # Hand back all the warehouse, district, and customer data
        return [ w, d, c ]
        
    ## ----------------------------------------------
    ## doStockLevel
    ## ----------------------------------------------    
    def doStockLevel(self, params):
        w_id = params["w_id"]
        d_id = params["d_id"]
        threshold = params["threshold"]
        
        # getOId
        d = self.district.find_one({"D_W_ID": w_id, "D_ID": d_id}, {"D_NEXT_O_ID": 1})
        assert d
        o_id = d["D_NEXT_O_ID"]
        
        # getStockCount
        # Outer Table: ORDER_LINE
        # Inner Table: STOCK
        if self.denormalize:
            c = self.customer.find({"C_W_ID": w_id, "C_D_ID": d_id, "ORDERS.O_ID": {"$lt": o_id, "$gte": o_id-20}}, {"ORDERS.ORDER_LINE.OL_I_ID": 1})
            assert c
            orderLines = [ ]
            for ol in c:
                assert "ORDER_LINE" in ol["ORDERS"][0]
                orderLines.extend(ol["ORDERS"][0]["ORDER_LINE"])
        else:
            orderLines = self.order_line.find({"OL_W_ID": w_id, "OL_D_ID": d_id, "OL_O_ID": {"$lt": o_id, "$gte": o_id-20}}, {"OL_I_ID": 1})
            
        assert orderLines
        ol_ids = set()
        for ol in orderLines:
            ol_ids.add(ol["OL_I_ID"])
        ## FOR
        result = self.stock.find({"S_W_ID": w_id, "S_I_ID": {"$in": list(ol_ids)}, "S_QUANTITY": {"$lt": threshold}}).count()
        
        return int(result)
        
## CLASS

