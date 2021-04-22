#/ -*- coding: utf-8 -*-
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
import logging
import commands
from pprint import pprint,pformat

import json
import requests
import time

import constants
from abstractdriver import *
from random import randint


QUERY_URL = "127.0.0.1:8093"
USER_ID = "Administrator"
PASSWORD = "password"
TXN_QUERIES = {
    "DELIVERY": {
        "getNewOrder": "SELECT NO_O_ID FROM NEW_ORDER WHERE NO_D_ID = $1 AND NO_W_ID = $2 AND NO_O_ID > -1 LIMIT 1", #
        "deleteNewOrder": "DELETE FROM NEW_ORDER WHERE NO_D_ID = $1 AND NO_W_ID = $2 AND NO_O_ID = $3", # d_id, w_id, no_o_id
        "getCId": "SELECT O_C_ID FROM ORDERS WHERE O_ID = $1 AND O_D_ID = $2 AND O_W_ID = $3", # no_o_id, d_id, w_id
        "updateOrders": "UPDATE ORDERS SET O_CARRIER_ID = $1 WHERE O_ID = $2 AND O_D_ID = $3 AND O_W_ID = $4", # o_carrier_id, no_o_id, d_id, w_id
        "updateOrderLine": "UPDATE ORDER_LINE SET OL_DELIVERY_D = $1 WHERE OL_O_ID = $2 AND OL_D_ID = $3 AND OL_W_ID = $4", # o_entry_d, no_o_id, d_id, w_id
        "sumOLAmount": "SELECT SUM(OL_AMOUNT) AS SUM_OL_AMOUNT FROM ORDER_LINE WHERE OL_O_ID = $1 AND OL_D_ID = $2 AND OL_W_ID = $3", # no_o_id, d_id, w_id
        "updateCustomer": "UPDATE CUSTOMER USE KEYS [(to_string($4) || '.' || to_string($3) || '.' ||  to_string($2))] SET C_BALANCE = C_BALANCE + $1 ", # ol_total, c_id, d_id, w_id
    },
    "NEW_ORDER": {
        "getWarehouseTaxRate": "SELECT W_TAX FROM WAREHOUSE WHERE W_ID = $1", # w_id
        "getDistrict": "SELECT D_TAX, D_NEXT_O_ID FROM DISTRICT WHERE D_ID = $1 AND D_W_ID = $2", # d_id, w_id
        "incrementNextOrderId": "UPDATE DISTRICT SET D_NEXT_O_ID = $1 WHERE D_ID = $2 AND D_W_ID = $3", # d_next_o_id, d_id, w_id
        "getCustomer": "SELECT C_DISCOUNT, C_LAST, C_CREDIT FROM CUSTOMER USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3)) ] ", # w_id, d_id, c_id
        "createOrder": "INSERT INTO ORDERS (KEY, VALUE) VALUES (TO_STRING($3) || '.' ||  TO_STRING($2) || '.' ||  TO_STRING($1), {\\\"O_ID\\\":$1, \\\"O_D_ID\\\":$2, \\\"O_W_ID\\\":$3, \\\"O_C_ID\\\":$4, \\\"O_ENTRY_D\\\":$5, \\\"O_CARRIER_ID\\\":$6, \\\"O_OL_CNT\\\":$7, \\\"O_ALL_LOCAL\\\":$8})", # d_next_o_id, d_id, w_id, c_id, o_entry_d, o_carrier_id, o_ol_cnt, o_all_local
        "createNewOrder": "INSERT INTO NEW_ORDER(KEY, VALUE) VALUES(TO_STRING($2)|| '.' || TO_STRING($3)|| '.' || TO_STRING($1), {\\\"NO_O_ID\\\":$1,\\\"NO_D_ID\\\":$2,\\\"NO_W_ID\\\":$3})",
        "getItemInfo": "SELECT I_PRICE, I_NAME, I_DATA FROM ITEM USE KEYS [to_string($1)]", # ol_i_id
        "getStockInfo": "SELECT S_QUANTITY, S_DATA, S_YTD, S_ORDER_CNT, S_REMOTE_CNT, S_DIST_%02d FROM STOCK USE KEYS [TO_STRING($2)|| '.' || TO_STRING($1)]", # d_id, ol_i_id, ol_supply_w_id
        "updateStock": "UPDATE STOCK USE KEYS [to_string($6) || '.' || to_string($5)] SET S_QUANTITY = $1, S_YTD = $2, S_ORDER_CNT = $3, S_REMOTE_CNT = $4 ", # s_quantity, s_order_cnt, s_remote_cnt, ol_i_id, ol_supply_w_id
        "createOrderLine": "INSERT INTO ORDER_LINE(KEY, VALUE) VALUES(TO_STRING($3)|| '.' || TO_STRING($2)|| '.' || TO_STRING($1)|| '.' || TO_STRING($4), { \\\"OL_O_ID\\\":$1, \\\"OL_D_ID\\\":$2, \\\"OL_W_ID\\\":$3, \\\"OL_NUMBER\\\":$4, \\\"OL_I_ID\\\":$5, \\\"OL_SUPPLY_W_ID\\\":$6, \\\"OL_DELIVERY_D\\\":$7, \\\"OL_QUANTITY\\\":$8, \\\"OL_AMOUNT\\\":$9, \\\"OL_DIST_INFO\\\":$10})" # o_id, d_id, w_id, ol_number, ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_dist_info        
    },
    
    "ORDER_STATUS": {
        "getCustomerByCustomerId": "SELECT C_ID, C_FIRST, C_MIDDLE, C_LAST, C_BALANCE FROM CUSTOMER USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3)) ]", # w_id, d_id, c_id
        "getCustomersByLastName": "SELECT C_ID, C_FIRST, C_MIDDLE, C_LAST, C_BALANCE FROM CUSTOMER WHERE C_W_ID = $1 AND C_D_ID = $2 AND C_LAST = $3 ORDER BY C_FIRST", # w_id, d_id, c_last
        "getLastOrder": "SELECT O_ID, O_CARRIER_ID, O_ENTRY_D FROM ORDERS WHERE O_W_ID = $1 AND O_D_ID = $2 AND O_C_ID = $3 ORDER BY O_ID DESC LIMIT 1", # w_id, d_id, c_id
        "getOrderLines": "SELECT OL_SUPPLY_W_ID, OL_I_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D FROM ORDER_LINE WHERE OL_W_ID = $1 AND OL_D_ID = $2 AND OL_O_ID = $3", # w_id, d_id, o_id        
    },
    
    "PAYMENT": {
        "getWarehouse": "SELECT W_NAME, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP FROM WAREHOUSE WHERE W_ID = $1", # w_id
        "updateWarehouseBalance": "UPDATE WAREHOUSE SET W_YTD = W_YTD + $1 WHERE W_ID = $2", # h_amount, w_id
        "getDistrict": "SELECT D_NAME, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP FROM DISTRICT WHERE D_W_ID = $1 AND D_ID = $2", # w_id, d_id
        "updateDistrictBalance": "UPDATE DISTRICT SET D_YTD = D_YTD + $1 WHERE D_W_ID  = $2 AND D_ID = $3", # h_amount, d_w_id, d_id
        "getCustomerByCustomerId": "SELECT C_ID, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT, C_DATA FROM CUSTOMER USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3)) ]", # w_id, d_id, c_id
        "getCustomersByLastName": "SELECT C_ID, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT, C_DATA FROM CUSTOMER WHERE C_W_ID = $1 AND C_D_ID = $2 AND C_LAST = $3 ORDER BY C_FIRST", # w_id, d_id, c_last
        "updateBCCustomer": "UPDATE CUSTOMER USE KEYS [(to_string($6) || '.' ||  to_string($6) || '.' ||  to_string($7)) ] SET C_BALANCE = $1, C_YTD_PAYMENT = $2, C_PAYMENT_CNT = $3, C_DATA = $4 ", # c_balance, c_ytd_payment, c_payment_cnt, c_data, c_w_id, c_d_id, c_id
        "updateGCCustomer": "UPDATE CUSTOMER USE KEYS [(to_string($4) || '.' ||  to_string($5) || '.' ||  to_string($6)) ] SET C_BALANCE = $1, C_YTD_PAYMENT = $2, C_PAYMENT_CNT = $3 ", # c_balance, c_ytd_payment, c_payment_cnt, c_w_id, c_d_id, c_id
        "insertHistory": "INSERT INTO HISTORY(KEY, VALUE) VALUES (TO_STRING($6), {\\\"H_C_ID\\\":$1, \\\"H_C_D_ID\\\":$2, \\\"H_C_W_ID\\\":$3, \\\"H_D_ID\\\":$4, \\\"H_W_ID\\\":$5, \\\"H_DATE\\\":$6, \\\"H_AMOUNT\\\":$7, \\\"H_DATA\\\":$8})"
    },
    
    "STOCK_LEVEL": {
        "getOId": "SELECT D_NEXT_O_ID FROM DISTRICT WHERE D_W_ID = $1 AND D_ID = $2",
        "getStockCount": " SELECT COUNT(DISTINCT(o.OL_I_ID)) AS CNT_OL_I_ID FROM  ORDER_LINE o INNER JOIN STOCK s ON KEYS (TO_STRING(o.OL_W_ID) || '.' ||  TO_STRING(o.OL_I_ID)) WHERE o.OL_W_ID = $1 AND o.OL_D_ID = $2 AND o.OL_O_ID < $3 AND o.OL_O_ID >= $4 AND s.S_QUANTITY < $6 ",
        "ansigetStockCount": " SELECT COUNT(DISTINCT(o.OL_I_ID)) AS CNT_OL_I_ID FROM  ORDER_LINE o INNER JOIN STOCK s ON (o.OL_W_ID == s.S_W_ID AND o.OL_I_ID ==  s.S_I_ID) WHERE o.OL_W_ID = $1 AND o.OL_D_ID = $2 AND o.OL_O_ID < $3 AND o.OL_O_ID >= $4 AND s.S_QUANTITY < $6 ",
        "getOrdersByDistrict": "SELECT * FROM  DISTRICT d INNER JOIN ORDERS o ON d.D_ID == o.O_D_ID where d.D_ID = $1",
        "getCustomerOrdersByDistrict": "SELECT COUNT(DISTINCT(c.C_ID)) FROM  CUSTOMER c INNER JOIN ORDERS o USE HASH(BUILD) ON c.C_ID == o.O_C_ID WHERE c.C_D_ID = $1" # d_ID
    },
}

KEYNAMES = {
	constants.TABLENAME_ITEM: 	[0],  # INTEGER
	constants.TABLENAME_WAREHOUSE: 	[0],  # INTEGER
	constants.TABLENAME_DISTRICT: 	[1, 0],  # INTEGER
	constants.TABLENAME_CUSTOMER: 	[2, 1, 0], # INTEGER
	constants.TABLENAME_STOCK: 	[1, 0],  # INTEGER
	constants.TABLENAME_ORDERS: 	[3, 2, 0], # INTEGER
	constants.TABLENAME_NEW_ORDER: 	[1, 2, ], # INTEGER
	constants.TABLENAME_ORDER_LINE: [2, 1, 0, 3], # INTEGER
	constants.TABLENAME_HISTORY: 	[0],  # INTEGER
}


TABLE_COLUMNS = {
    constants.TABLENAME_ITEM: [
        "I_ID", # INTEGER
        "I_IM_ID", # INTEGER
        "I_NAME", # VARCHAR
        "I_PRICE", # FLOAT
        "I_DATA", # VARCHAR
    ],
    constants.TABLENAME_WAREHOUSE: [
        "W_ID", # SMALLINT
        "W_NAME", # VARCHAR
        "W_STREET_1", # VARCHAR
        "W_STREET_2", # VARCHAR
        "W_CITY", # VARCHAR
        "W_STATE", # VARCHAR
        "W_ZIP", # VARCHAR
        "W_TAX", # FLOAT
        "W_YTD", # FLOAT
    ],
    constants.TABLENAME_DISTRICT: [
        "D_ID", # TINYINT
        "D_W_ID", # SMALLINT
        "D_NAME", # VARCHAR
        "D_STREET_1", # VARCHAR
        "D_STREET_2", # VARCHAR
        "D_CITY", # VARCHAR
        "D_STATE", # VARCHAR
        "D_ZIP", # VARCHAR
        "D_TAX", # FLOAT
        "D_YTD", # FLOAT
        "D_NEXT_O_ID", # INT
    ],
    constants.TABLENAME_CUSTOMER:   [
        "C_ID", # INTEGER
        "C_D_ID", # TINYINT
        "C_W_ID", # SMALLINT
        "C_FIRST", # VARCHAR
        "C_MIDDLE", # VARCHAR
        "C_LAST", # VARCHAR
        "C_STREET_1", # VARCHAR
        "C_STREET_2", # VARCHAR
        "C_CITY", # VARCHAR
        "C_STATE", # VARCHAR
        "C_ZIP", # VARCHAR
        "C_PHONE", # VARCHAR
        "C_SINCE", # TIMESTAMP
        "C_CREDIT", # VARCHAR
        "C_CREDIT_LIM", # FLOAT
        "C_DISCOUNT", # FLOAT
        "C_BALANCE", # FLOAT
        "C_YTD_PAYMENT", # FLOAT
        "C_PAYMENT_CNT", # INTEGER
        "C_DELIVERY_CNT", # INTEGER
        "C_DATA", # VARCHAR
    ],
    constants.TABLENAME_STOCK:      [
        "S_I_ID", # INTEGER
        "S_W_ID", # SMALLINT
        "S_QUANTITY", # INTEGER
        "S_DIST_01", # VARCHAR
        "S_DIST_02", # VARCHAR
        "S_DIST_03", # VARCHAR
        "S_DIST_04", # VARCHAR
        "S_DIST_05", # VARCHAR
        "S_DIST_06", # VARCHAR
        "S_DIST_07", # VARCHAR
        "S_DIST_08", # VARCHAR
        "S_DIST_09", # VARCHAR
        "S_DIST_10", # VARCHAR
        "S_YTD", # INTEGER
        "S_ORDER_CNT", # INTEGER
        "S_REMOTE_CNT", # INTEGER
        "S_DATA", # VARCHAR
    ],
    constants.TABLENAME_ORDERS:     [
        "O_ID", # INTEGER
        "O_C_ID", # INTEGER
        "O_D_ID", # TINYINT
        "O_W_ID", # SMALLINT
        "O_ENTRY_D", # TIMESTAMP
        "O_CARRIER_ID", # INTEGER
        "O_OL_CNT", # INTEGER
        "O_ALL_LOCAL", # INTEGER
    ],
    constants.TABLENAME_NEW_ORDER:  [
        "NO_O_ID", # INTEGER
        "NO_D_ID", # TINYINT
        "NO_W_ID", # SMALLINT
    ],
    constants.TABLENAME_ORDER_LINE: [
        "OL_O_ID", # INTEGER
        "OL_D_ID", # TINYINT
        "OL_W_ID", # SMALLINT
        "OL_NUMBER", # INTEGER
        "OL_I_ID", # INTEGER
        "OL_SUPPLY_W_ID", # SMALLINT
        "OL_DELIVERY_D", # TIMESTAMP
        "OL_QUANTITY", # INTEGER
        "OL_AMOUNT", # FLOAT
        "OL_DIST_INFO", # VARCHAR
    ],
    constants.TABLENAME_HISTORY:    [
        "H_C_ID", # INTEGER
        "H_C_D_ID", # TINYINT
        "H_C_W_ID", # SMALLINT
        "H_D_ID", # TINYINT
        "H_W_ID", # SMALLINT
        "H_DATE", # TIMESTAMP
        "H_AMOUNT", # FLOAT
        "H_DATA", # VARCHAR
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
    constants.TABLENAME_NEW_ORDER:  [
        "NO_O_ID",
        "NO_D_ID",
        "NO_W_ID",
    ],
    constants.TABLENAME_ORDER_LINE: [
        "OL_O_ID",
        "OL_D_ID",
        "OL_W_ID",
    ],
}

globconn = 0

## ----------------------------------------------
## runNQuery
## ----------------------------------------------

def runNQuery(query, txid, txtimeout, randomhost=None):
        global globcon
        try:
            QUERY_URL = os.environ["QUERY_URL"]
            USER_ID = os.environ["USER_ID"]
            PASSWORD = os.environ["PASSWORD"]
        except Exception,ex:
            print ex
        if randomhost:
            QUERY_URL = randomhost
        stmt = '{"statement" : "' + str(query) + '"'
        if (len(txid) >  0):
                stmt = stmt + ', "txid" : "' + txid + '"'
        if (len(txtimeout) >  0):
                stmt = stmt + ', "txtimeout" : "' + txtimeout + '"'
        stmt = stmt + ', "scan_consistency" : "not_bounded"' +  '}'
        #stmt = stmt + ', "scan_consistency" : "request_plus"' +  '}'

        # print len(param)
        #print stmt
        url = "http://{0}/query".format(QUERY_URL)
        query = json.loads(stmt)
        #print query
        #r = globcon.post(url, data=query, stream=False, headers={'Connection':'close'})
        r = globcon.post(url, data=query, stream=False)
        if r.json()['status'] != 'success':
            print('Transaction BEGIN/COMMIT Failed | Query : ', query, '| txid :', txid, '| Response', r.json())
        #print r.json()
        #print r.json()['results']
        #print ('Kamini:results')
        #print r.json()['results']
        #print ('Kamini:status')
        #print r.json()['status']
        return r.json()['results']
## ----------------------------------------------
## runNQueryParam
## ----------------------------------------------

def runNQueryParam(query, param, txid, randomhost=None):
        global globcon
        try:
            QUERY_URL = os.environ["QUERY_URL"]
            USER_ID = os.environ["USER_ID"]
            PASSWORD = os.environ["PASSWORD"]
        except Exception,ex:
            print ex
        if randomhost:
            QUERY_URL = randomhost
        stmt = '{"statement" : "' + str(query) + '"'
        # print len(param)
        if (len(param) >  0):
                stmt = stmt + ', "args" : "['
        else:
                stmt = stmt + '}'
        i=0
        myarg = ""
        for p in param:
	  	if isinstance(p, (bool)):
			myarg = myarg + str.lower(str(p))
		elif isinstance(p,(int, float, long)) and not isinstance(p, (bool)):
                        myarg = myarg + str(p)
                else:
                        myarg = myarg + '\\"' + str(p) + '\\"'
                i = i + 1
                if i < len(param):
                        myarg = myarg + ","
        stmt = stmt + myarg
        stmt = stmt + ']"'
        if (len(txid) >  0):
                stmt = stmt + ', "txid" : "' + txid + '"}'
        else:
                stmt = stmt + '}'
        
        ##print ('Kamini:stmt')
        #print stmt
        url = "http://{0}/query".format(QUERY_URL)
        #print ('Kamini:query')
        query = json.loads(stmt)
        #print query
        r = globcon.post(url, data=query, stream=False)
        if r.json()['status'] != 'success':
            print('Query Failed | Query : ', query, '| txid :', txid, '| Response', r.json())
        #print r.json()
        #print ('Kamini:results')
        #print r.json()['results']
        #print ('Kamini:status')
        #print r.json()['status']
        #print ('Kamini:metrics')
        #print r.json()['metrics']
	return r.json()['results'],r.json()['status']

## ==============================================
## NestDriver
## ==============================================
class NestDriver(AbstractDriver):
    DEFAULT_CONFIG = {
        "host":         ("The hostname to N1QL service", "ec2-52-6-226-203.compute-1.amazonaws.com" ),
        "port":         ("The port number to N1QL Service", 8093 ),
        "name":         ("Not Needed for N1QL", "tpcc"),
        "denormalize":  ("If set to true, then the CUSTOMER data will be denormalized into a single document", False),
    }
    
    def __init__(self, ddl):
        global globcon
        super(NestDriver, self).__init__("nest", ddl)
        self.database = None
        s = self.conn = requests.Session()
        s.keep_alive = True
        globcon = s
        self.cursor = None
        try:
            QUERY_URL = os.environ["QUERY_URL"]
            USER_ID = os.environ["USER_ID"]
            PASSWORD = os.environ["PASSWORD"]
        except Exception,ex:
            print ex

        try:
            MUlTI_QUERY_URL = os.environ["MULTI_QUERY_URL"].split(',')
            #print('printing MUlTI_QUERY_URL', MUlTI_QUERY_URL)
            random_num = randint(0, len(MUlTI_QUERY_URL) - 1)
            #print('printing random number ', random_num)
            self.RANDOM_QUERY_URL = MUlTI_QUERY_URL[random_num]
            #print('printing RANDOM_QUERY_URL within init method', self.RANDOM_QUERY_URL)
        except ex:
            print("parsing multi url failed MUlTI_QUERY_URL=", MUlTI_QUERY_URL)
            pass
        if len(MUlTI_QUERY_URL) < 2:
            print ('entered since length is less than 1')
            self.RANDOM_QUERY_URL = QUERY_URL

        s.auth = (USER_ID, PASSWORD)

        url = "http://{0}/query/service".format(QUERY_URL)
        self.prepared_dict = {}
        for txn in TXN_QUERIES:
            for query in TXN_QUERIES[txn]:
                if query == "getStockInfo":
                    for i in range(1,11):
                        converted_district = TXN_QUERIES[txn][query] % i
                        prepare_query = "PREPARE %s_%s_%s " % (txn, i, query) + "FROM %s" % converted_district
                        stmt = '{"statement" : "' + str(prepare_query) + '"}'
                        curl_query = json.loads(stmt)
                        r = globcon.post(url, data=curl_query, stream=False)
                        r.json()
                        self.prepared_dict[txn + str(i) + query] = "EXECUTE %s_%s_%s" % (txn, i, query)
                else:
                    prepare_query = "PREPARE %s_%s " % (txn, query) + "FROM %s" % TXN_QUERIES[txn][query]
                    stmt = '{"statement" : "' + str(prepare_query) + '"}'
                    curl_query = json.loads(stmt)
                    r = globcon.post(url, data=curl_query, stream=False)
                    r.json()
                    self.prepared_dict[txn + query] = "EXECUTE %s_%s" % (txn, query)


    ## ----------------------------------------------
    ## makeDefaultConfig
    ## ----------------------------------------------
    def makeDefaultConfig(self):
        return NestDriver.DEFAULT_CONFIG
    
    ## ----------------------------------------------
    ## loadConfig
    ## ----------------------------------------------
    def loadConfig(self, config):
        #No Database creation. 
        #Connection management is via REST gateway. So, nothing to do here.
        # Add bucket creation here.  For now, simply create manually and load.
	self.database = "tpcc"
	self.denormalize = config['denormalize']
	if self.denormalize: logging.debug("Using denormalized data model")
        return
    

    ## ----------------------------------------------
    ## loadTuples for Couchbase (Adapted from MongoDB implemenetation. Only normalized version is ported to Couchbase).
    ## ----------------------------------------------
    def loadTuples(self, tableName, tuples):
        global globcon
        if len(tuples) == 0: return
        logging.debug("Loading %d tuples for tableName %s" % (len(tuples), tableName))
        
        assert tableName in TABLE_COLUMNS, "Unexpected table %s" % tableName
        columns = TABLE_COLUMNS[tableName]
        num_columns = range(len(columns))
        
        tuple_dicts = [ ]
        try:
            QUERY_URL = os.environ["QUERY_URL"]
            USER_ID = os.environ["USER_ID"]
            PASSWORD = os.environ["PASSWORD"]
        except Exception,ex:
            print ex
        url = "http://{0}/query".format(QUERY_URL)   # Update this for your installation.
        ## We want to combine all of a CUSTOMER's ORDERS, ORDER_LINE, and HISTORY records
        ## into a single document
        if self.denormalize and tableName in MongodbDriver.DENORMALIZED_TABLES:
            ## If this is the CUSTOMER table, then we'll just store the record locally for now
            if tableName == constants.TABLENAME_CUSTOMER:
                for t in tuples:
                    key = tuple(t[:3]) # C_ID, D_ID, W_ID
                    self.w_customers[key] = dict(map(lambda i: (columns[i], t[i]), num_columns))
                ## FOR
                
            ## If this is an ORDER_LINE record, then we need to stick it inside of the 
            ## right ORDERS record
            elif tableName == constants.TABLENAME_ORDER_LINE:
                for t in tuples:
                    o_key = tuple(t[:3]) # O_ID, O_D_ID, O_W_ID
                    (c_key, o_idx) = self.w_orders[o_key]
                    c = self.w_customers[c_key]
                    assert o_idx >= 0
                    assert o_idx < len(c[constants.TABLENAME_ORDERS])
                    o = c[constants.TABLENAME_ORDERS][o_idx]
                    if not tableName in o: o[tableName] = [ ]
                    o[tableName].append(dict(map(lambda i: (columns[i], t[i]), num_columns[4:])))
                ## FOR
                    
            ## Otherwise we have to find the CUSTOMER record for the other tables
            ## and append ourselves to them
            else:
                if tableName == constants.TABLENAME_ORDERS:
                    key_start = 1
                    cols = num_columns[0:1] + num_columns[4:] # Removes O_C_ID, O_D_ID, O_W_ID
                else:
                    key_start = 0
                    cols = num_columns[3:] # Removes H_C_ID, H_C_D_ID, H_C_W_ID
                    
                for t in tuples:
                    c_key = tuple(t[key_start:key_start+3]) # C_ID, D_ID, W_ID
                    assert c_key in self.w_customers, "Customer Key: %s\nAll Keys:\n%s" % (str(c_key), "\n".join(map(str, sorted(self.w_customers.keys()))))
                    c = self.w_customers[c_key]
                    
                    if not tableName in c: c[tableName] = [ ]
                    c[tableName].append(dict(map(lambda i: (columns[i], t[i]), cols)))
                    
                    ## Since ORDER_LINE doesn't have a C_ID, we have to store a reference to
                    ## this ORDERS record so that we can look it up later
                    if tableName == constants.TABLENAME_ORDERS:
                        o_key = (t[0], t[2], t[3]) # O_ID, O_D_ID, O_W_ID
                        self.w_orders[o_key] = (c_key, len(c[tableName])-1) # CUSTOMER, ORDER IDX
                ## FOR
            ## IF

        ## Otherwise just shove the tuples straight to the target collection
        else:
            i = 0
	    # print tuples
	    sql = 'INSERT INTO %s(KEY, VALUE) ' % tableName
	    for t in tuples:
                # print tableName
                # print KEYNAMES[tableName]
	        # print columns
	        # print t
		key = ""
                # print KEYNAMES[tableName]
                # Normalizing kpart with array indexing.
                kpart = len(KEYNAMES[tableName]) - 1
                l = 0
		for k in KEYNAMES[tableName]:
			if (l < kpart):
				key = key + str(t[k]) + '.'
			else:
				key = key + str(t[k])
			l = l + 1;
	        #sql = 'INSERT INTO %s(KEY, VALUE) VALUES (\\"%s\\", {' % (tableName, key)
	        if i != 0:
	            sql = sql + ',VALUES (\\"%s\\", {' % key
	        else:
	            sql = sql + 'VALUES (\\"%s\\", {' % key
	        j=0
                for x in t:
		    if isinstance(t[j],(int, float, long)):
	        	    sql = sql + '\\"%s\\":%s  ' % (columns[j],  t[j])
		    else:
	        	    sql = sql + '\\"%s\\":\\"%s\\"  ' % (columns[j],  t[j])
		    j = j + 1
		    if j < len(t):
			    sql = sql + ","
                if ( i == 3333 ):
	            sql = sql + "})"
	            nsql = '{"statement": "' + sql + '"}'
	            jsql = json.loads(nsql)
                    # r = globcon.post(url, data=jsql, stream=False, headers={'Connection':'close'})
                    r = globcon.post(url, data=jsql, stream=False)
	            # r = requests.post(url, data=jsql, auth=('Administrator', 'password'))
	            # print tableName, r, i, len(nsql)
	            # print r.json()
		    sql = 'INSERT INTO %s(KEY, VALUE) ' % tableName
	            i = 0
                else:
	            sql = sql + "})"
		    i = i + 1
	    # print nsql
	    nsql = '{"statement": "' + sql + '"}'
	    jsql = json.loads(nsql)
	    # print nsql
        r = globcon.post(url, data=jsql, stream=False, headers={'Connection':'close'})
	    # r = requests.post(url, data=jsql, auth=('Administrator', 'password'))
	    # r = globcon.post(url, data=jsql, stream=False)
	    # print tableName, r, i, len(nsql)
	    # print r.json()

        ## IF
	logging.debug("LoadTuples:%s: %s" %  (tableName, nsql))
        
        return
        

    ## ----------------------------------------------
    ## loadFinish
    ## ----------------------------------------------
    def loadFinish(self):
        logging.info("Finished loading tables")
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            for name in constants.ALL_TABLES:
                if self.denormalize and name in MongodbDriver.DENORMALIZED_TABLES[1:]: return
                logging.debug("%-12s%d records" % (name+":", self.database[name].count()))
        #Nothing to commit for N1QL

	return



    ## ----------------------------------------------
    ## doDelivery
    ## ----------------------------------------------
    def doDelivery(self, params):
	# print "Entering doDelivery"
        txn = "DELIVERY"
        q = TXN_QUERIES[txn]
        w_id = params["w_id"]
        o_carrier_id = params["o_carrier_id"]
        ol_delivery_d = params["ol_delivery_d"]

        result = [ ]
        for d_id in range(1, constants.DISTRICTS_PER_WAREHOUSE+1):
	    rs = runNQuery("BEGIN WORK","","30s", randomhost=self.RANDOM_QUERY_URL);
            txid = rs[0]['txid']
	    newOrder,status = runNQueryParam(self.prepared_dict[ txn + "getNewOrder"], [d_id, w_id], txid, randomhost=self.RANDOM_QUERY_URL)
            if len(newOrder) == 0:
                ## No orders for this district: skip it. Note: This must be reported if > 1%
                return
            assert len(newOrder) > 0
            no_o_id = newOrder[0]['NO_O_ID']
            
            rs,status = runNQueryParam(self.prepared_dict[ txn + "getCId"], [no_o_id, d_id, w_id],txid, randomhost=self.RANDOM_QUERY_URL)

            if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     continue

	    c_id = rs[0]['O_C_ID']
            
            rs2,status = runNQueryParam(self.prepared_dict[ txn + "sumOLAmount"], [no_o_id, d_id, w_id], txid, randomhost=self.RANDOM_QUERY_URL)

            if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     continue
            ol_total = rs2[0]['SUM_OL_AMOUNT']

            result,status = runNQueryParam(self.prepared_dict[ txn + "deleteNewOrder"], [d_id, w_id, no_o_id], txid, randomhost=self.RANDOM_QUERY_URL)
            
            result,status = runNQueryParam(self.prepared_dict[ txn + "updateOrders"], [o_carrier_id, no_o_id, d_id, w_id], txid, randomhost=self.RANDOM_QUERY_URL)
            if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     continue

            result,status = runNQueryParam(self.prepared_dict[ txn + "updateOrderLine"], [ol_delivery_d, no_o_id, d_id, w_id], txid, randomhost=self.RANDOM_QUERY_URL)
            if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     continue


            
            # These must be logged in the "result file" according to TPC-C 2.7.2.2 (page 39)
            # We remove the queued time, completed time, w_id, and o_carrier_id: the client can figure
            # them out
            # If there are no order lines, SUM returns null. There should always be order lines.
            # assert ol_total != None, "ol_total is NULL: there are no order lines. This should not happen"
            # assert ol_total > 0.0

            result,status = runNQueryParam(self.prepared_dict[ txn + "updateCustomer"], [ol_total, c_id, d_id, w_id], txid, randomhost=self.RANDOM_QUERY_URL)
            if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     continue

            result.append((d_id, no_o_id))
        ## FOR

	runNQuery("COMMIT WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);

        return result

    ## ----------------------------------------------
    ## doNewOrder
    ## ----------------------------------------------
    def doNewOrder(self, params):
	# print "Entering doNewOrder"
        txn = "NEW_ORDER"
        q = TXN_QUERIES[txn]
	d_next_o_id = 0
        w_id = params["w_id"]
        d_id = params["d_id"]
        c_id = params["c_id"]
        # print '#NewOrder'
        # print w_id, d_id, c_id

        o_entry_d = params["o_entry_d"]
        i_ids = params["i_ids"]
        i_w_ids = params["i_w_ids"]
        i_qtys = params["i_qtys"]

        assert len(i_ids) > 0
        assert len(i_ids) == len(i_w_ids)
        assert len(i_ids) == len(i_qtys)

        all_local = True
        items = [ ]
	rs = runNQuery("BEGIN WORK","","3s", randomhost=self.RANDOM_QUERY_URL);
        txid = rs[0]['txid']
        #print ('Kamini:txid')
        #print txid
        for i in range(len(i_ids)):
            ## Determine if this is an all local order or not
            all_local = all_local and i_w_ids[i] == w_id
            rs, status = runNQueryParam(self.prepared_dict[ txn + "getItemInfo"], [i_ids[i]], txid, randomhost=self.RANDOM_QUERY_URL)
	    #keshav added.  Needed? assert len(rs) > 0
            items.append(rs[0])
        assert len(items) == len(i_ids)
        

        ## TPCC defines 1% of neworder gives a wrong itemid, causing rollback.
        ## Note that this will happen with 1% of transactions on purpose.
        for item in items:
            if len(item) == 0:
                ## TODO Abort here!
		# print "//aborted"
		runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);
		#print "ROLLBACK 5";
		return;
        ## FOR
        
        ## ----------------
        ## Collect Information from WAREHOUSE, DISTRICT, and CUSTOMER
        ## ----------------
        # print w_id
        rs, status = runNQueryParam(self.prepared_dict[ txn + "getWarehouseTaxRate"], [w_id], txid, randomhost=self.RANDOM_QUERY_URL)
        customer_info = rs
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     return
        if len(rs) > 0:
            w_tax = rs[0]['W_TAX']
        
        district_info, status = runNQueryParam(self.prepared_dict[ txn +"getDistrict"], [d_id, w_id], txid, randomhost=self.RANDOM_QUERY_URL)
        if len(district_info) != 0:
            d_tax = district_info[0]['D_TAX']
            d_next_o_id = district_info[0]['D_NEXT_O_ID']
        
        rs, status = runNQueryParam(self.prepared_dict[ txn + "getCustomer"], [w_id, d_id, c_id], txid, randomhost=self.RANDOM_QUERY_URL)
	if len(rs) != 0:
            c_discount = rs[0]['C_DISCOUNT']

        ## ----------------
        ## Insert Order Information
        ## ----------------
        ol_cnt = len(i_ids)
        o_carrier_id = constants.NULL_CARRIER_ID
        
        rs, status = runNQueryParam(self.prepared_dict[ txn + "incrementNextOrderId"], [d_next_o_id + 1, d_id, w_id], txid, randomhost=self.RANDOM_QUERY_URL)
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     return
        
        rs, status = runNQueryParam(self.prepared_dict[ txn + "createOrder"], [d_next_o_id, d_id, w_id, c_id, o_entry_d, o_carrier_id, ol_cnt, all_local], txid, randomhost=self.RANDOM_QUERY_URL)
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     return
        
        rs,status = runNQueryParam(self.prepared_dict[ txn + "createNewOrder"], [d_next_o_id, d_id, w_id], txid, randomhost=self.RANDOM_QUERY_URL)
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     return
        
        #print "NewOrder Stage #1"

        ## ----------------
        ## Insert Order Item Information
        ## ----------------
        item_data = [ ]
        total = 0
        # print  len(i_ids);
        for i in range(len(i_ids)):
            # print "NewOrder Stage #2"
            # print "i == " + str(i)
            ol_number = i + 1
            ol_supply_w_id = i_w_ids[i]
            ol_i_id = i_ids[i]
            ol_quantity = i_qtys[i]
            itemInfo = items[i]

	    # print "itemInfo: " + str(itemInfo)
            i_name = itemInfo["I_NAME"]
            i_data = itemInfo["I_DATA"]
            i_price = itemInfo["I_PRICE"]

            # print "NewOrder Stage #3"
            stockInfo, status = runNQueryParam(self.prepared_dict[ txn + str(d_id) + "getStockInfo"], [ol_i_id, ol_supply_w_id], txid, randomhost=self.RANDOM_QUERY_URL)
            if len(stockInfo) == 0:
                logging.warn("No STOCK record for (ol_i_id=%d, ol_supply_w_id=%d)" % (ol_i_id, ol_supply_w_id))
                return

            # print "NewOrder Stage #4"
            # print "stockInfo = " + str(stockInfo)
            s_quantity = stockInfo[0]["S_QUANTITY"]
            s_ytd = stockInfo[0]["S_YTD"]
            s_order_cnt = stockInfo[0]["S_ORDER_CNT"]
            s_remote_cnt = stockInfo[0]["S_REMOTE_CNT"]
            s_data = stockInfo[0]["S_DATA"]
	    distxx = "S_DIST_" + str(d_id).zfill(2);
            # print "NewOrder Stage #4.01"
            # print distxx
            # print stockInfo[0][distxx]
            s_dist_xx = stockInfo[0][distxx] # Fetches data from the s_dist_[d_id] column

            # print "NewOrder Stage #4.1"
            ## Update stock
            s_ytd += ol_quantity
            if s_quantity >= ol_quantity + 10:
                s_quantity = s_quantity - ol_quantity
            else:
                s_quantity = s_quantity + 91 - ol_quantity
            s_order_cnt += 1
            
            if ol_supply_w_id != w_id: s_remote_cnt += 1

            # print "NewOrder Stage #5"
            rs, status = runNQueryParam(self.prepared_dict[ txn + "updateStock"], [s_quantity, s_ytd, s_order_cnt, s_remote_cnt, ol_i_id, ol_supply_w_id], txid, randomhost=self.RANDOM_QUERY_URL)
            if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL)
                     return

            if i_data.find(constants.ORIGINAL_STRING) != -1 and s_data.find(constants.ORIGINAL_STRING) != -1:
                brand_generic = 'B'
            else:
                brand_generic = 'G'

            ## Transaction profile states to use "ol_quantity * i_price"
            ol_amount = ol_quantity * i_price
            total += ol_amount

            rs, status = runNQueryParam(self.prepared_dict[ txn + "createOrderLine"], [d_next_o_id, d_id, w_id, ol_number, ol_i_id, ol_supply_w_id, o_entry_d, ol_quantity, ol_amount, s_dist_xx], txid, randomhost=self.RANDOM_QUERY_URL)
            

            ## Add the info to be returned
            item_data.append( (i_name, s_quantity, brand_generic, i_price, ol_amount) )
        ## FOR
        runNQuery("COMMIT WORK", txid, "",randomhost=self.RANDOM_QUERY_URL);
        ## Commit!
        # keshav: self.conn.commit()

        ## Adjust the total for the discount
        #print "c_discount:", c_discount, type(c_discount)
        #print "w_tax:", w_tax, type(w_tax)
        #print "d_tax:", d_tax, type(d_tax)
        total *= (1 - c_discount) * (1 + w_tax + d_tax)

        ## Pack up values the client is missing (see TPC-C 2.4.3.5)
        misc = [ (w_tax, d_tax, d_next_o_id, total) ]
        
        # print "//end of NewOrder"
        return [ customer_info, misc, item_data ]

    ## ----------------------------------------------
    ## doOrderStatus
    ## ----------------------------------------------
    def doOrderStatus(self, params):
	# print "Entering doOrderStatus"
        txn = "ORDER_STATUS"
        q = TXN_QUERIES[txn]
        w_id = params["w_id"]
        d_id = params["d_id"]
        c_id = params["c_id"]
        c_last = params["c_last"]
        
        assert w_id, pformat(params)
        assert d_id, pformat(params)

	rs = runNQuery("BEGIN WORK","","3s",randomhost=self.RANDOM_QUERY_URL);
        txid = rs[0]['txid']
        if c_id != None:
            customerlist,status = runNQueryParam(self.prepared_dict[ txn + "getCustomerByCustomerId"], [w_id, d_id, c_id], txid, randomhost=self.RANDOM_QUERY_URL)
	    customer = customerlist[0]
        else:
            # Get the midpoint customer's id
            all_customers,status = runNQueryParam(self.prepared_dict[ txn + "getCustomersByLastName"], [w_id, d_id, c_last], txid, randomhost=self.RANDOM_QUERY_URL)
            assert len(all_customers) > 0
            namecnt = len(all_customers)
            index = (namecnt-1)/2
            customer = all_customers[index]
            c_id = customer['C_ID']
        assert len(customer) > 0
        assert c_id != None

        order,status = runNQueryParam(self.prepared_dict[ txn + "getLastOrder"], [w_id, d_id, c_id], txid, randomhost=self.RANDOM_QUERY_URL)
        if len(order) > 0:
            orderLines,status = runNQueryParam(self.prepared_dict[ txn + "getOrderLines"], [w_id, d_id, order[0]['O_ID']], txid, randomhost=self.RANDOM_QUERY_URL)
        else:
            orderLines = [ ]
	runNQuery("COMMIT WORK", txid, "",randomhost=self.RANDOM_QUERY_URL);

        #Keshav: self.conn.commit()
        return [ customer, order, orderLines ]

    ## ----------------------------------------------
    ## doPayment
    ## ----------------------------------------------
    def doPayment(self, params):
	# print "Entering doPayment"
        txn = "PAYMENT"
        q = TXN_QUERIES[txn]
        w_id = params["w_id"]
        d_id = params["d_id"]
        h_amount = params["h_amount"]
        c_w_id = params["c_w_id"]
        c_d_id = params["c_d_id"]
        c_id = params["c_id"]
        c_last = params["c_last"]
        h_date = params["h_date"]

	rs = runNQuery("BEGIN WORK","","3s",randomhost=self.RANDOM_QUERY_URL);
        txid = rs[0]['txid']

        if c_id != None:
            customerlist,status = runNQueryParam(self.prepared_dict[ txn + "getCustomerByCustomerId"], [w_id, d_id, c_id], txid, randomhost=self.RANDOM_QUERY_URL)
            customer = customerlist[0]
        else:
            # Get the midpoint customer's id
            all_customers,status = runNQueryParam(self.prepared_dict[ txn + "getCustomersByLastName"], [w_id, d_id, c_last], txid, randomhost=self.RANDOM_QUERY_URL)

            assert len(all_customers) > 0
            namecnt = len(all_customers)
            index = (namecnt-1)/2
            customer = all_customers[index]
            c_id = customer['C_ID']
        assert len(customer) > 0
        c_balance = customer['C_BALANCE'] - h_amount
        c_ytd_payment = customer['C_YTD_PAYMENT'] + h_amount
        c_payment_cnt = customer['C_PAYMENT_CNT'] + 1
        c_data = customer['C_DATA']

	#print "doPayment: Stage 2"

        warehouse,status = runNQueryParam(self.prepared_dict[ txn + "getWarehouse"], [w_id], txid, randomhost=self.RANDOM_QUERY_URL)
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);
                     return

        district,status = runNQueryParam(self.prepared_dict[ txn + "getDistrict"], [w_id, d_id], txid, randomhost=self.RANDOM_QUERY_URL)
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);
                     return

        rs, status = runNQueryParam(self.prepared_dict[ txn + "updateWarehouseBalance"], [h_amount, w_id], txid, randomhost=self.RANDOM_QUERY_URL)
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);
                     return
        
        rs, status = runNQueryParam(self.prepared_dict[ txn + "updateDistrictBalance"], [h_amount, w_id, d_id], txid, randomhost=self.RANDOM_QUERY_URL)
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);
                     return

        
	#print "doPayment: Stage3"

        # Customer Credit Information
        if customer['C_CREDIT'] == constants.BAD_CREDIT:
            newData = " ".join(map(str, [c_id, c_d_id, c_w_id, d_id, w_id, h_amount]))
            c_data = (newData + "|" + c_data)
            if len(c_data) > constants.MAX_C_DATA: c_data = c_data[:constants.MAX_C_DATA]
            rs, status = runNQueryParam(self.prepared_dict[ txn + "updateBCCustomer"], [c_balance, c_ytd_payment, c_payment_cnt, c_data, c_w_id, c_d_id, c_id], txid, randomhost=self.RANDOM_QUERY_URL)
            if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);
                     return
            
        else:
            c_data = ""
            rs, status = runNQueryParam(self.prepared_dict[ txn + "updateGCCustomer"], [c_balance, c_ytd_payment, c_payment_cnt, c_w_id, c_d_id, c_id], txid, randomhost=self.RANDOM_QUERY_URL)
            if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);
                     return
            
	#print "doPayment: Stage4"
        # Concatenate w_name, four spaces, d_name
	# print "warehouse %s" % (str(warehouse))
	# print "district %s" % (str(district))
        h_data = "%s    %s" % (warehouse[0]['W_NAME'], district[0]['D_NAME'])
        # Create the history record
        rs, status = runNQueryParam(self.prepared_dict[ txn + "insertHistory"], [c_id, c_d_id, c_w_id, d_id, w_id, h_date, h_amount, h_data], txid, randomhost=self.RANDOM_QUERY_URL)
        if (status == 'errors'):
                     runNQuery("ROLLBACK WORK",txid,"",randomhost=self.RANDOM_QUERY_URL);
                     return
        

	runNQuery("COMMIT WORK", txid,"",randomhost=self.RANDOM_QUERY_URL);
        #Keshav: self.conn.commit()

        # TPC-C 2.5.3.3: Must display the following fields:
        # W_ID, D_ID, C_ID, C_D_ID, C_W_ID, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP,
        # D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1,
        # C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM,
        # C_DISCOUNT, C_BALANCE, the first 200 characters of C_DATA (only if C_CREDIT = "BC"),
        # H_AMOUNT, and H_DATE.

	# print "doPayment: Stage5"
        # Hand back all the warehouse, district, and customer data
        return [ warehouse, district, customer ]

    ## ----------------------------------------------
    ## doStockLevel
    ## ----------------------------------------------
    def doStockLevel(self, params):
	# print "Entering doStockLevel"
        txn = "STOCK_LEVEL"
        q = TXN_QUERIES[txn]

        w_id = params["w_id"]
        d_id = params["d_id"]
        threshold = params["threshold"]

	#rs = runNQuery("BEGIN WORK","","2m",randomhost=self.RANDOM_QUERY_URL);
        #txid = rs[0]['txid']
        result, status = runNQueryParam(self.prepared_dict[ txn + "getOId"], [w_id, d_id],"", randomhost=self.RANDOM_QUERY_URL)
        assert result
        o_id = result[0]['D_NEXT_O_ID']

        result, status = runNQueryParam(self.prepared_dict[ txn + "getStockCount"], [w_id, d_id, o_id, (o_id - 20), w_id, threshold], "", randomhost=self.RANDOM_QUERY_URL)

        #self.conn.commit()
        #rs, status = runNQueryParam(self.prepared_dict[ txn + "getCustomerOrdersByDistrict"], [d_id], "", randomhost=self.RANDOM_QUERY_URL)
        #rs, status = runNQueryParam(self.prepared_dict[ txn + "getOrdersByDistrict"], [d_id], "", randomhost=self.RANDOM_QUERY_URL)
        #Taking too long with 10Warehouses.So disabling 
        #rs, status = runNQueryParam(self.prepared_dict[ txn + 'ansigetStockCount'], [w_id, d_id, o_id, (o_id - 20), w_id, threshold], txid, randomhost=self.RANDOM_QUERY_URL)

	#runNQuery("COMMIT WORK", txid, "", randomhost=self.RANDOM_QUERY_URL);
        return int(result[0]['CNT_OL_I_ID'])
## CLASS
