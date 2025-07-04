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
import re
import socket
import subprocess
from pprint import pprint,pformat

import json
import requests
import time
import urllib3
from urllib3.poolmanager import PoolManager

import constants
from .abstractdriver import *
import time
from datetime import timedelta
import sys
import traceback
import couchbase.collection
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, ClusterTimeoutOptions
from couchbase.auth import PasswordAuthenticator

CH2_TXN_QUERIES = {
    "DELIVERY": {
        "beginWork": "BEGIN WORK",
        "rollbackWork":"ROLLBACK WORK",
        "commitWork":"COMMIT WORK",
        "getNewOrder": "SELECT no_o_id FROM default:bench.ch2.neworder WHERE no_d_id = $1 AND no_w_id = $2 AND no_o_id > -1 LIMIT 1", #
        "deleteNewOrder": "DELETE FROM default:bench.ch2.neworder WHERE no_d_id = $1 AND no_w_id = $2 AND no_o_id = $3", # d_id, w_id, no_o_id
        "getCId": "SELECT o_c_id FROM default:bench.ch2.orders WHERE o_id = $1 AND o_d_id = $2 AND o_w_id = $3", # no_o_id, d_id, w_id
        "updateOrders": "UPDATE default:bench.ch2.orders SET o_carrier_id = $1 WHERE o_id = $2 AND o_d_id = $3 AND o_w_id = $4", # o_carrier_id, no_o_id, d_id, w_id
        "updateOrderLine": "UPDATE default:bench.ch2.orders SET ol.ol_delivery_d = $1 FOR ol IN o_orderline END WHERE o_id = $2 AND o_d_id = $3 AND o_w_id = $4", # o_entry_d, no_o_id, d_id, w_id
        "sumOLAmount": "SELECT VALUE (SELECT SUM(ol.ol_amount) as sum_ol_amount FROM o.o_orderline ol)[0] FROM default:bench.ch2.orders o where o.o_id = $1 and o.o_d_id = $2 and o.o_w_id = $3",
        "updateCustomer": "UPDATE default:bench.ch2.customer USE KEYS [(to_string($4) || '.' || to_string($3) || '.' ||  to_string($2))] SET c_balance = c_balance + $1 ", # ol_total, c_id, d_id, w_id
    },
    "NEW_ORDER": {
        "beginWork": "BEGIN WORK",
        "rollbackWork":"ROLLBACK WORK",
        "commitWork":"COMMIT WORK",
        "getWarehouseTaxRate": "SELECT w_tax FROM default:bench.ch2.warehouse WHERE w_id = $1", # w_id
        "getDistrict": "SELECT d_tax, d_next_o_id FROM default:bench.ch2.district WHERE d_id = $1 AND d_w_id = $2", # d_id, w_id
        "incrementNextOrderId": "UPDATE default:bench.ch2.district SET d_next_o_id = $1 WHERE d_id = $2 AND d_w_id = $3", # d_next_o_id, d_id, w_id
        "getCustomer": "SELECT c_discount, c_last, c_credit FROM default:bench.ch2.customer USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3))]", # w_id, d_id, c_id
        "createOrder": "INSERT INTO default:bench.ch2.orders (KEY, VALUE) VALUES (TO_STRING($3) || '.' ||  TO_STRING($2) || '.' ||  TO_STRING($1), {\\\"o_id\\\":$1, \\\"o_d_id\\\":$2, \\\"o_w_id\\\":$3, \\\"o_c_id\\\":$4, \\\"o_entry_d\\\":$5, \\\"o_carrier_id\\\":$6, \\\"o_ol_cnt\\\":$7, \\\"o_all_local\\\":$8})", # d_next_o_id, d_id, w_id, c_id, o_entry_d, o_carrier_id, o_ol_cnt, o_all_local
        "createNewOrder": "INSERT INTO default:bench.ch2.neworder(KEY, VALUE) VALUES(TO_STRING($2)|| '.' || TO_STRING($3)|| '.' || TO_STRING($1), {\\\"no_o_id\\\":$1,\\\"no_d_id\\\":$2,\\\"no_w_id\\\":$3})",
        "getItemInfo": "SELECT i_price, i_name, i_data FROM default:bench.ch2.item USE KEYS [to_string($1)]", # ol_i_id
        "getStockInfo": "SELECT s_quantity, s_data, s_ytd, s_order_cnt, s_remote_cnt, s_dist_%02d FROM default:bench.ch2.stock USE KEYS [TO_STRING($2)|| '.' || TO_STRING($1)]", # d_id, ol_i_id, ol_supply_w_id
        "updateStock": "UPDATE default:bench.ch2.stock USE KEYS [to_string($6) || '.' || to_string($5)] SET s_quantity = $1, s_ytd = $2, s_order_cnt = $3, s_remote_cnt = $4 ", # s_quantity, s_order_cnt, s_remote_cnt, ol_i_id, ol_supply_w_id
        "createOrderLine": "UPSERT INTO default:bench.ch2.orders(KEY, VALUE) VALUES(TO_STRING($3)|| '.' || TO_STRING($2)|| '.' || TO_STRING($1), { \\\"o_id\\\":$1, \\\"o_d_id\\\":$2, \\\"o_w_id\\\":$3, \\\"o_orderline\\\": [{\\\"ol_number\\\":$4, \\\"ol_i_id\\\":$5, \\\"ol_supply_w_id\\\":$6, \\\"ol_delivery_d\\\":$7, \\\"ol_quantity\\\":$8, \\\"ol_amount\\\":$9, \\\"ol_dist_info\\\":$10}]})"
    },

    "ORDER_STATUS": {
        "beginWork": "BEGIN WORK",
        "rollbackWork":"ROLLBACK WORK",
        "commitWork":"COMMIT WORK",
        "getCustomerByCustomerId": "SELECT c_id, c_first, c_middle, c_last, c_balance FROM default:bench.ch2.customer USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3)) ]", # w_id, d_id, c_id
        "getCustomersByLastName": "SELECT c_id, c_first, c_middle, c_last, c_balance FROM default:bench.ch2.customer WHERE c_w_id = $1 AND c_d_id = $2 AND c_last = $3 ORDER BY c_first", # w_id, d_id, c_last
        "getLastOrder": "SELECT o_id, o_carrier_id, o_entry_d FROM default:bench.ch2.orders WHERE o_w_id = $1 AND o_d_id = $2 AND o_c_id = $3 ORDER BY o_id DESC LIMIT 1", # w_id, d_id, c_id
        "getOrderLines": "SELECT ol.ol_supply_w_id, ol.ol_i_id, ol.ol_quantity, ol.ol_amount, ol.ol_delivery_d FROM default:bench.ch2.orders o unnest o.o_orderline ol WHERE o.o_w_id = $1 AND o.o_d_id = $2 AND o.o_id = $3", # w_id, d_id, o_id
    },

    "PAYMENT": {
        "beginWork": "BEGIN WORK",
        "rollbackWork":"ROLLBACK WORK",
        "commitWork":"COMMIT WORK",
        "getWarehouse": "SELECT w_name, w_street_1, w_street_2, w_city, w_state, w_zip FROM default:bench.ch2.warehouse WHERE w_id = $1", # w_id
        "updateWarehouseBalance": "UPDATE default:bench.ch2.warehouse SET w_ytd = w_ytd + $1 WHERE w_id = $2", # h_amount, w_id
        "getDistrict": "SELECT d_name, d_street_1, d_street_2, d_city, d_state, d_zip FROM default:bench.ch2.district WHERE d_w_id = $1 AND d_id = $2", # w_id, d_id
        "updateDistrictBalance": "UPDATE default:bench.ch2.district SET d_ytd = d_ytd + $1 WHERE d_w_id  = $2 AND d_id = $3", # h_amount, d_w_id, d_id
        "getCustomerByCustomerId": "SELECT c_id, c_first, c_middle, c_last, c_street_1, c_street_2, c_city, c_state, c_zip, c_phone, c_since, c_credit, c_credit_lim, c_discount, c_balance, c_ytd_payment, c_payment_cnt, c_data FROM default:bench.ch2.customer USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3)) ]", # w_id, d_id, c_id
        "getCustomersByLastName": "SELECT c_id, c_first, c_middle, c_last, c_street_1, c_street_2, c_city, c_state, c_zip, c_phone, c_since, c_credit, c_credit_lim, c_discount, c_balance, c_ytd_payment, c_payment_cnt, c_data FROM default:bench.ch2.customer WHERE c_w_id = $1 AND c_d_id = $2 AND c_last = $3 ORDER BY c_first", # w_id, d_id, c_last
        "updateBCCustomer": "UPDATE default:bench.ch2.customer USE KEYS [(to_string($6) || '.' ||  to_string($6) || '.' ||  to_string($7)) ] SET c_balance = $1, c_ytd_payment = $2, c_payment_cnt = $3, c_data = $4 ", # c_balance, c_ytd_payment, c_payment_cnt, c_data, c_w_id, c_d_id, c_id
        "updateGCCustomer": "UPDATE default:bench.ch2.customer USE KEYS [(to_string($4) || '.' ||  to_string($5) || '.' ||  to_string($6)) ] SET c_balance = $1, c_ytd_payment = $2, c_payment_cnt = $3 ", # c_balance, c_ytd_payment, c_payment_cnt, c_w_id, c_d_id, c_id
        "insertHistory": "INSERT INTO default:bench.ch2.history(KEY, VALUE) VALUES (TO_STRING($6), {\\\"h_c_id\\\":$1, \\\"h_c_d_id\\\":$2, \\\"h_c_w_id\\\":$3, \\\"h_d_id\\\":$4, \\\"h_w_id\\\":$5, \\\"h_date\\\":$6, \\\"h_amount\\\":$7, \\\"h_data\\\":$8})"
    },

    "STOCK_LEVEL": {
        "getOId": "SELECT d_next_o_id FROM default:bench.ch2.district WHERE d_w_id = $1 AND d_id = $2",
          "getStockCount": " SELECT COUNT(DISTINCT(ol.ol_i_id)) AS cnt_ol_i_id FROM default:bench.ch2.orders o UNNEST o.o_orderline ol INNER JOIN bench.ch2.stock s ON KEYS (TO_STRING(o.o_w_id) || '.' ||  TO_STRING(ol.ol_i_id)) WHERE o.o_w_id = $1 AND o.o_d_id = $2 AND o.o_id < $3 AND o.o_id >= $4 AND s.s_quantity < $6 "
    },
}

CH2PP_TXN_QUERIES = {
    "DELIVERY": {
        "beginWork": "BEGIN WORK",
        "rollbackWork":"ROLLBACK WORK",
        "commitWork":"COMMIT WORK",
        "getNewOrder": "SELECT no_o_id FROM default:bench.ch2pp.neworder WHERE no_d_id = $1 AND no_w_id = $2 AND no_o_id > -1 LIMIT 1", #
        "deleteNewOrder": "DELETE FROM default:bench.ch2pp.neworder WHERE no_d_id = $1 AND no_w_id = $2 AND no_o_id = $3", # d_id, w_id, no_o_id
        "getCId": "SELECT o_c_id FROM default:bench.ch2pp.orders WHERE o_id = $1 AND o_d_id = $2 AND o_w_id = $3", # no_o_id, d_id, w_id
        "updateOrders": "UPDATE default:bench.ch2pp.orders SET o_carrier_id = $1 WHERE o_id = $2 AND o_d_id = $3 AND o_w_id = $4", # o_carrier_id, no_o_id, d_id, w_id
        "updateOrderLine": "UPDATE default:bench.ch2pp.orders SET ol.ol_delivery_d = $1 FOR ol IN o_orderline END WHERE o_id = $2 AND o_d_id = $3 AND o_w_id = $4", # o_entry_d, no_o_id, d_id, w_id
        "sumOLAmount": "SELECT VALUE (SELECT SUM(ol.ol_amount) as sum_ol_amount FROM o.o_orderline ol)[0] FROM default:bench.ch2pp.orders o where o.o_id = $1 and o.o_d_id = $2 and o.o_w_id = $3",
        "updateCustomer": "UPDATE default:bench.ch2pp.customer USE KEYS [(to_string($4) || '.' || to_string($3) || '.' ||  to_string($2))] SET c_balance = c_balance + $1 ", # ol_total, c_id, d_id, w_id
    },
    "NEW_ORDER": {
        "beginWork": "BEGIN WORK",
        "rollbackWork":"ROLLBACK WORK",
        "commitWork":"COMMIT WORK",
        "getWarehouseTaxRate": "SELECT w_tax FROM default:bench.ch2pp.warehouse WHERE w_id = $1", # w_id
        "getDistrict": "SELECT d_tax, d_next_o_id FROM default:bench.ch2pp.district WHERE d_id = $1 AND d_w_id = $2", # d_id, w_id
        "incrementNextOrderId": "UPDATE default:bench.ch2pp.district SET d_next_o_id = $1 WHERE d_id = $2 AND d_w_id = $3", # d_next_o_id, d_id, w_id
        "getCustomer": "SELECT c_discount, c_name.c_last, c_credit FROM default:bench.ch2pp.customer USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3))]", # w_id, d_id, c_id
        "createOrder": "INSERT INTO default:bench.ch2pp.orders (KEY, VALUE) VALUES (TO_STRING($3) || '.' ||  TO_STRING($2) || '.' ||  TO_STRING($1), {\\\"o_id\\\":$1, \\\"o_d_id\\\":$2, \\\"o_w_id\\\":$3, \\\"o_c_id\\\":$4, \\\"o_entry_d\\\":$5, \\\"o_carrier_id\\\":$6, \\\"o_ol_cnt\\\":$7, \\\"o_all_local\\\":$8})", # d_next_o_id, d_id, w_id, c_id, o_entry_d, o_carrier_id, o_ol_cnt, o_all_local
        "createNewOrder": "INSERT INTO default:bench.ch2pp.neworder(KEY, VALUE) VALUES(TO_STRING($2)|| '.' || TO_STRING($3)|| '.' || TO_STRING($1), {\\\"no_o_id\\\":$1,\\\"no_d_id\\\":$2,\\\"no_w_id\\\":$3})",
        "getItemInfo": "SELECT i_price, i_name, i_data FROM default:bench.ch2pp.item USE KEYS [to_string($1)]", # ol_i_id
        "getStockInfo": "SELECT s_quantity, s_data, s_ytd, s_order_cnt, s_remote_cnt, s_dists FROM default:bench.ch2pp.stock USE KEYS [TO_STRING($2)|| '.' || TO_STRING($1)]", # d_id, ol_i_id, ol_supply_w_id
        "updateStock": "UPDATE default:bench.ch2pp.stock USE KEYS [to_string($6) || '.' || to_string($5)] SET s_quantity = $1, s_ytd = $2, s_order_cnt = $3, s_remote_cnt = $4 ", # s_quantity, s_order_cnt, s_remote_cnt, ol_i_id, ol_supply_w_id
        "createOrderLine": "UPSERT INTO default:bench.ch2pp.orders(KEY, VALUE) VALUES(TO_STRING($3)|| '.' || TO_STRING($2)|| '.' || TO_STRING($1), { \\\"o_id\\\":$1, \\\"o_d_id\\\":$2, \\\"o_w_id\\\":$3, \\\"o_orderline\\\": [{\\\"ol_number\\\":$4, \\\"ol_i_id\\\":$5, \\\"ol_supply_w_id\\\":$6, \\\"ol_delivery_d\\\":$7, \\\"ol_quantity\\\":$8, \\\"ol_amount\\\":$9, \\\"ol_dist_info\\\":$10}]})"
    },

    "ORDER_STATUS": {
        "beginWork": "BEGIN WORK",
        "rollbackWork":"ROLLBACK WORK",
        "commitWork":"COMMIT WORK",
        "getCustomerByCustomerId": "SELECT c_id, c_name.c_first, c_name.c_middle, c_name.c_last, c_balance FROM default:bench.ch2pp.customer USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3)) ]", # w_id, d_id, c_id
        "getCustomersByLastName": "SELECT c_id, c_name.c_first, c_name.c_middle, c_name.c_last, c_balance FROM default:bench.ch2pp.customer WHERE c_w_id = $1 AND c_d_id = $2 AND c_name.c_last = $3 ORDER BY c_name.c_first", # w_id, d_id, c_last
        "getLastOrder": "SELECT o_id, o_carrier_id, o_entry_d FROM default:bench.ch2pp.orders WHERE o_w_id = $1 AND o_d_id = $2 AND o_c_id = $3 ORDER BY o_id DESC LIMIT 1", # w_id, d_id, c_id
        "getOrderLines": "SELECT ol.ol_supply_w_id, ol.ol_i_id, ol.ol_quantity, ol.ol_amount, ol.ol_delivery_d FROM default:bench.ch2pp.orders o unnest o.o_orderline ol WHERE o.o_w_id = $1 AND o.o_d_id = $2 AND o.o_id = $3", # w_id, d_id, o_id
    },

    "PAYMENT": {
        "beginWork": "BEGIN WORK",
        "rollbackWork":"ROLLBACK WORK",
        "commitWork":"COMMIT WORK",
        "getWarehouse": "SELECT w_name, w_address.w_street_1, w_address.w_street_2, w_address.w_city, w_address.w_state, w_address.w_zip FROM default:bench.ch2pp.warehouse WHERE w_id = $1", # w_id
        "updateWarehouseBalance": "UPDATE default:bench.ch2pp.warehouse SET w_ytd = w_ytd + $1 WHERE w_id = $2", # h_amount, w_id
        "getDistrict": "SELECT d_name, d_address.d_street_1, d_address.d_street_2, d_address.d_city, d_address.d_state, d_address.d_zip FROM default:bench.ch2pp.district WHERE d_w_id = $1 AND d_id = $2", # w_id, d_id
        "updateDistrictBalance": "UPDATE default:bench.ch2pp.district SET d_ytd = d_ytd + $1 WHERE d_w_id  = $2 AND d_id = $3", # h_amount, d_w_id, d_id
        "getCustomerByCustomerId": "SELECT c.c_id, c.c_name.c_first, c.c_name.c_middle, c.c_name.c_last, ca.c_street_1, ca.c_street_2, ca.c_city, ca.c_state, ca.c_zip, cp.c_phone_number, c.c_since, c.c_credit, c.c_credit_lim, c.c_discount, c.c_balance, c.c_ytd_payment, c.c_payment_cnt, c.c_data FROM default:bench.ch2pp.customer AS c USE KEYS [(to_string($1) || '.' ||  to_string($2) || '.' ||  to_string($3))] UNNEST c.c_addresses AS ca UNNEST c.c_phones AS cp WHERE ca.c_address_kind = 'shipping' AND cp.c_phone_kind = 'contact'", # w_id, d_id, c_id
        "getCustomersByLastName": "SELECT c.c_id, c.c_name.c_first, c.c_name.c_middle, c.c_name.c_last, ca.c_street_1, ca.c_street_2, ca.c_city, ca.c_state, ca.c_zip, cp.c_phone_number, c.c_since, c.c_credit, c.c_credit_lim, c.c_discount, c.c_balance, c.c_ytd_payment, c.c_payment_cnt, c.c_data FROM default:bench.ch2pp.customer AS c UNNEST c.c_addresses AS ca UNNEST c.c_phones AS cp WHERE ca.c_address_kind = 'shipping' AND cp.c_phone_kind = 'contact' AND c.c_w_id = $1 AND c.c_d_id = $2 AND c.c_name.c_last = $3 ORDER BY c.c_name.c_first", # w_id, d_id, c_last
        "updateBCCustomer": "UPDATE default:bench.ch2pp.customer USE KEYS [(to_string($6) || '.' ||  to_string($6) || '.' ||  to_string($7)) ] SET c_balance = $1, c_ytd_payment = $2, c_payment_cnt = $3, c_data = $4 ", # c_balance, c_ytd_payment, c_payment_cnt, c_data, c_w_id, c_d_id, c_id
        "updateGCCustomer": "UPDATE default:bench.ch2pp.customer USE KEYS [(to_string($4) || '.' ||  to_string($5) || '.' ||  to_string($6)) ] SET c_balance = $1, c_ytd_payment = $2, c_payment_cnt = $3 ", # c_balance, c_ytd_payment, c_payment_cnt, c_w_id, c_d_id, c_id
        "insertHistory": "INSERT INTO default:bench.ch2pp.history(KEY, VALUE) VALUES (TO_STRING($6), {\\\"h_c_id\\\":$1, \\\"h_c_d_id\\\":$2, \\\"h_c_w_id\\\":$3, \\\"h_d_id\\\":$4, \\\"h_w_id\\\":$5, \\\"h_date\\\":$6, \\\"h_amount\\\":$7, \\\"h_data\\\":$8})"
    },

    "STOCK_LEVEL": {
        "getOId": "SELECT d_next_o_id FROM default:bench.ch2pp.district WHERE d_w_id = $1 AND d_id = $2",
          "getStockCount": " SELECT COUNT(DISTINCT(ol.ol_i_id)) AS cnt_ol_i_id FROM default:bench.ch2pp.orders o UNNEST o.o_orderline ol INNER JOIN bench.ch2pp.stock s ON KEYS (TO_STRING(o.o_w_id) || '.' ||  TO_STRING(ol.ol_i_id)) WHERE o.o_w_id = $1 AND o.o_d_id = $2 AND o.o_id < $3 AND o.o_id >= $4 AND s.s_quantity < $6 "
    },
}

globpool = None
gcreds = '[{"user":"' + os.environ["USER_ID"] + '","pass":"' + os.environ["PASSWORD"] + '"}]'

def pysdk_init(self):
    pa = PasswordAuthenticator(os.environ["USER_ID"], os.environ["PASSWORD"])
    str_data_node = str(self.data_node)
    timeout_opts = ClusterTimeoutOptions(kv_timeout=timedelta(seconds=self.kv_timeout))
    cluster_opts = ClusterOptions(pa, timeout_options=timeout_opts)
    endpoint = 'couchbase://{}'.format(str_data_node)
    if bool(int(os.environ['TLS'])):
        endpoint = 'couchbases://{}?ssl=no_verify'.format(str_data_node)
    cluster = Cluster(endpoint, cluster_opts)
    bucket = cluster.bucket(constants.CH2_BUCKET)
    scope = bucket.scope(self.schema)
    self.collections = {}
    for tableName in constants.ALL_TABLES:
        self.collections[tableName] = scope.collection(constants.COLLECTIONS_DICT[tableName])

def TxTimeoutFactor(txtimeout, factor):
    tx = float(txtimeout)
    if tx == 0 or factor == 0:
        return "3s"
    tx = tx * factor
    return str(tx) + "s"

def retvalN1QLQuery(prefix, rj):
    if 'status' not in rj:
         return rj, "assert"
    status = rj['status']
    if status != "success" :
        if rj['errors'][0]["code"] == 17010 :
            status = "timeout"
        elif ( (rj['errors'][0]["code"] == 17007) and
             ("cause" in rj['errors'][0]) and
             ("cause" in rj['errors'][0]['cause']) ) :
             if  rj['errors'][0]['cause']['cause'] == "found existing document: document already exists" :
                  status = "duplicates"
             elif "msg" in rj['errors'][0]['cause']['cause'] and  rj['errors'][0]['cause']['cause']['msg'] == "write write conflict":
                  status = "wwconflict"
             elif ("error_description" in rj['errors'][0]['cause']['cause'])  :
                  status = rj['errors'][0]['cause']['cause']['error_description']
                  if status == "key already exists, or CAS mismatch" :
                      status = "casmismatch"

#        if status != "casmismatch" and status != "timeout" and status != "duplicates" and status != wwconflict" :
#            print rj
        if prefix != "" :
            status = prefix + "-" + status

    if 'results' not in rj:
        logging.debug("Results JSON: %s" % (json.JSONEncoder().encode(rj)))

    return rj.get('results', []), status


## ----------------------------------------------
## runNQuery
## ----------------------------------------------

def runNQuery(prefix, query, txid, txtimeout, randomhost):
        stmt = generate_prepared_query(query)
        stmt['durability_level'] = os.environ["DURABILITY_LEVEL"]
        stmt['scan_consistency'] = os.environ["SCAN_CONSISTENCY"]
        if txtimeout != "":
            stmt['txtimeout'] = txtimeout
        if txid != "":
            stmt['txid'] = txid
        body = n1ql_execute(randomhost, stmt)
        return retvalN1QLQuery(prefix, body)

## ----------------------------------------------
## runNQueryParam
## ----------------------------------------------

def doQueryParam(query, param, txid, randomhost):
        stmt = generate_prepared_query(query)
        if txid != "":
            stmt['txid'] = txid

        if (len(param) > 0):
             qparam = []
             for p in param:
                 if isinstance(p, (datetime)):
                     qparam.append(str(p))
                 else:
                     qparam.append(p)
             stmt['args'] = json.JSONEncoder().encode(qparam)
        body = n1ql_load(randomhost, stmt)
        return retvalN1QLQuery("", body)

def runNQueryParam(query, param, txid, randomhost):
        stmt = generate_prepared_query(query)
        if txid != "":
            stmt['txid'] = txid

        if (len(param) > 0):
             qparam = []
             for p in param:
                 if isinstance(p, (bool)):
                     qparam.append(p)
                 elif isinstance(p,(int, float)) and not isinstance(p, (bool)):
                     qparam.append(p)
                 else:
                     qparam.append(str(p))
             stmt['args'] = json.JSONEncoder().encode(qparam)
        body = n1ql_execute(randomhost, stmt)
        return retvalN1QLQuery("", body)

def generate_prepared_query (name):
    return {'prepared': '"' + name + '"'}

def n1ql_execute(node, stmt, query=1):
    global gcred
    global globpool
#    headers = urllib3.make_headers(basic_auth='Administrator:password')
    headers = urllib3.make_headers(
        basic_auth=os.environ["USER_ID_ANALYTICS"] + ":" + os.environ["PASSWORD_ANALYTICS"]
    )
    protocol = 'http://'
    if bool(int(os.environ['TLS'])):
        protocol = 'https://'
    if query:
        stmt['creds'] = gcreds
        url = "{}{}/query/service".format(protocol, node)
    else:
        url = "{}{}/analytics/service".format(protocol, node)
    try:
        if query:
            response = globpool.request('POST', url, fields=stmt, encode_multipart=False)
        else:
            response = globpool.request('POST', url, fields=stmt, headers=headers, encode_multipart=False)
        response.read(cache_content=False)
        body = json.loads(response.data.decode('utf8'))
        if body['status'] != "success":
            logging.debug("%s --- %s" % (stmt, json.JSONEncoder().encode(body)))
        return body
    except Exception as ex:
        logging.info("Exception occured when executing query: %s: %s" % (type(ex).__name__, ex))
        logging.debug(traceback.format_exc())
    return {}

def n1ql_load(query_node, stmt):
    global gcred
    global globpool

    stmt['creds'] = gcreds
#    stmt['durability_level'] = 'majorityAndPersistActive'
#    stmt['tximplicit'] = True

    protocol = 'http://'
    if bool(int(os.environ['TLS'])):
        protocol = 'https://'

    url = "{}{}/query/service".format(protocol, query_node)
## RETRY LOGIC ADDED FOR LOAD
    for i in range(constants.NUM_LOAD_RETRIES):
        try:
            response = globpool.request('POST', url, fields=stmt, encode_multipart=False)
            response.read(cache_content=False)
            body = json.loads(response.data.decode('utf8'))
            if body['status'] != "success":
                logging.debug("%s --- %s" % (stmt, json.JSONEncoder().encode(body)))
                # logging.info("%s" % (json.JSONEncoder().encode(body)))
                # return body
            else:
                break
        except:
#            pass
            logging.debug("retrying %d" %(i))
    ##FOR
    return {}

## ==============================================
## NestcollectionsDriver
## ==============================================
class NestcollectionsDriver(AbstractDriver):
    DEFAULT_CONFIG = {
        "host":         ("The hostname to N1QL service", "localhost" ),
        "port":         ("The port number to N1QL Service", 8093 ),
        "name":         ("Not Needed for N1QL", "tpcc"),
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
                 load_format=constants.CH2_DRIVER_LOAD_FORMAT["JSON"],
                 kv_timeout=constants.CH2_DRIVER_KV_TIMEOUT,
                 bulkload_batch_size=constants.CH2_DRIVER_BULKLOAD_BATCH_SIZE):
        global globpool
        super(NestcollectionsDriver, self).__init__("nestcollections", ddl)
        QUERY_URL = os.environ["QUERY_URL"]
        DATA_URL = os.environ["DATA_URL"]
        ANALYTICS_URL = os.environ["ANALYTICS_URL"]
        self.query_node = QUERY_URL
        self.MULTI_QUERY_LIST = os.environ["MULTI_QUERY_URL"].split(',')
        self.data_node = DATA_URL
        self.MULTI_DATA_LIST = os.environ["MULTI_DATA_URL"].split(',')
        self.analytics_node = ANALYTICS_URL
        self.client_id = clientId
        self.TAFlag = TAFlag
        self.schema = schema
        self.analyticalQueries = analyticalQueries
        self.load_mode = load_mode
        self.customerExtraFields = customerExtraFields
        self.ordersExtraFields = ordersExtraFields
        self.itemExtraFields = itemExtraFields
        self.kv_timeout = kv_timeout
        self.bulkload_batch_size = bulkload_batch_size
        if len(self.MULTI_QUERY_LIST) > 1 and clientId >= 0:
            self.query_node = self.MULTI_QUERY_LIST[self.client_id%len(self.MULTI_QUERY_LIST)]
        if len(self.MULTI_DATA_LIST) > 1 and clientId >= 0:
            self.data_node = self.MULTI_DATA_LIST[self.client_id%len(self.MULTI_DATA_LIST)]

        self.database = None
        self.cursor = None
        self.tx_status = ""
        self.txtimeout = TxTimeoutFactor(os.environ["TXTIMEOUT"], 1)
        self.delivery_txtimeout = TxTimeoutFactor(os.environ["TXTIMEOUT"], 10)
        self.stock_txtimeout = TxTimeoutFactor(os.environ["TXTIMEOUT"], 40)
        self.denormalize = False
        self.w_orders = {}
        if (self.load_mode == constants.CH2_DRIVER_LOAD_MODE["DATASVC_BULKLOAD"] or
            self.load_mode == constants.CH2_DRIVER_LOAD_MODE["DATASVC_LOAD"]):
            pysdk_init(self)
        if globpool == None:
            gcreds = '[{"user":"' + os.environ["USER_ID"] + '","pass":"' + os.environ["PASSWORD"] + '"}]'
            globpool = PoolManager(
                10,
                retries=urllib3.Retry(10),
                maxsize=60,
                cert_reqs="CERT_NONE",
                socket_options=[  # Set TCP keep-alive options for long running analytics queries
                    (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
#                    (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 120),
                    (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30),
                    (socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 20),
                ],
            )

        if clientId >= 0:
            self.prepared_dict = preparedTransactionQueries
            return

        if TAFlag == "L":
            return

        if TAFlag == "T":
            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
                txnQueries = CH2_TXN_QUERIES
            else:
                txnQueries = CH2PP_TXN_QUERIES
            for txn, queries in txnQueries.items():
                for query, statement in queries.items():
                    stmt = statement
                    if self.schema == constants.CH2_DRIVER_SCHEMA["CH2P"]:
                        stmt = re.sub("default:bench\.ch2pp\.", "default:bench.ch2p.", statement)
                    if query == "getStockInfo":
                        for i in range(1,11):
                            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
                                converted_district = stmt % i
                            else:
                                 converted_district = stmt
                            prepare_query = "PREPARE %s_%s_%s_%s " % (self.schema, txn, i, query) + "FROM %s" % converted_district
                            jsonStmt = json.loads('{"statement" : "' + str(prepare_query) + '"}')
                            body = n1ql_execute(self.query_node, jsonStmt)
                            preparedTransactionQueries[self.schema + txn + str(i) + query] = body['results'][0]['name']
                    else:
                        prepare_query = "PREPARE %s_%s_%s " % (self.schema, txn, query) + "FROM %s" % stmt
                        jsonStmt = json.loads('{"statement" : "' + str(prepare_query) + '"}')
                        body = n1ql_execute(self.query_node, jsonStmt)
                        preparedTransactionQueries[self.schema + txn + query] = body['results'][0]['name']
            self.prepared_dict = preparedTransactionQueries

        # wait prepare statements populate other query nodes
        if len(self.MULTI_QUERY_LIST) > 1:
            time.sleep(15)

    ## ----------------------------------------------
    ## makeDefaultConfig
    ## ----------------------------------------------
    def makeDefaultConfig(self):
        return NestcollectionsDriver.DEFAULT_CONFIG

    ## ----------------------------------------------
    ## loadConfig
    ## ----------------------------------------------
    def loadConfig(self, config):
        #No Database creation.
        #Connection management is via REST gateway. So, nothing to do here.
        # Add bucket creation here.  For now, simply create manually and load.
        self.database = "tpcc"
        self.denormalize = config['denormalize']
        return

    def txStatus(self):
        return self.tx_status

    def tryDataSvcBulkLoad(self, collection, cur_batch):
        for i in range(constants.NUM_LOAD_RETRIES):
            try:
                result = collection.upsert_multi(cur_batch)
                if result.all_ok == True:
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

    def tryDataSvcLoad(self, collection, key, val):
        for i in range(constants.NUM_LOAD_RETRIES):
            try:
                result = collection.upsert(key, val)
                if result.success == True:
                    return True
                else:
                    time.sleep(1)
                    logging.debug("Client ID # %d failed load data into KV, try %d" % (self.client_id, i))
            except:
                logging.debug("Client ID # %d exception load data into KV, try %d" % (self.client_id, i))
                exc_info = sys.exc_info()
                tb = ''.join(traceback.format_tb(exc_info[2]))
                logging.debug(f'Exception info: {exc_info[1]}\nTraceback:\n{tb}')
                time.sleep(1)

        logging.debug("Client ID # %d failed load data into KV after %d attempts" % (self.client_id, constants.NUM_LOAD_RETRIES))
        return False

    ## ----------------------------------------------
    ## loadTuples for Couchbase (Adapted from MongoDB implemenetation).
    ## ----------------------------------------------
    def loadTuples(self, tableName, tuples):
        if len(tuples) == 0:
            return

        logging.debug("Loading %d tuples for tableName %s" % (len(tuples), tableName))
        assert tableName in constants.ALL_TABLES, "Unexpected table %s" % tableName

        if (self.load_mode == constants.CH2_DRIVER_LOAD_MODE["DATASVC_BULKLOAD"] or
            self.load_mode == constants.CH2_DRIVER_LOAD_MODE["DATASVC_LOAD"]):
            collection = self.collections[tableName]
            if self.load_mode == constants.CH2_DRIVER_LOAD_MODE["DATASVC_BULKLOAD"]:
                # For bulk load: load in batches
                cur_batch = {}
                cur_size = 0
                for t in tuples:
                    key, val = self.getOneDoc(tableName, t, True)
                    cur_batch[key] = val
                    cur_size += len(key) + len(val) + 24 # 24 bytes of overhead
                    if cur_size > self.bulkload_batch_size:
                        result = self.tryDataSvcBulkLoad(collection, cur_batch)
                        if result == True:
                            cur_batch = {}
                            cur_size = 0
                            continue
                        else:
                            logging.debug("Client ID # %d failed bulk load data into KV, aborting..." % self.client_id)
                if cur_size > 0:
                    result = self.tryDataSvcBulkLoad(collection, cur_batch)
                    if result == False:
                        logging.debug("Client ID # %d failed bulk load data into KV, aborting..." % self.client_id)
            else:
                #self.load_mode == constants.CH2_DRIVER_LOAD_MODE["DATASVC_LOAD"]
                # Load one document at a time
                for t in tuples:
                    key, val = self.getOneDoc(tableName, t, True)
                    result = self.tryDataSvcLoad(collection, key, val)
                    if result == True:
                        continue
                    else:
                        logging.debug("Client ID # %d failed load data into KV, aborting..." % self.client_id)

        elif self.load_mode == constants.CH2_DRIVER_LOAD_MODE["QRYSVC_LOAD"]:
            for t in tuples:
                args = []
                args.append(constants.CH2_NAMESPACE + ":" + constants.CH2_BUCKET + "." + self.schema + "."+ tableName)
                args.append("")
                args.append("")
                args.append({})
                key, val = self.getOneDoc(tableName, t, True)
                args[1] = key
                args[2] = val

                doQueryParam("__upsert", args, "", self.query_node)
        else:
            logging.info("No data or query node specified for load")
            sys.exit(0)

        return

    ## ----------------------------------------------
    ## loadFinish
    ## ----------------------------------------------
    def loadFinish(self):
        logging.info("Client ID # %d Finished loading tables" % (self.client_id))
        return

    ## ----------------------------------------------
    ## doDelivery
    ## ----------------------------------------------
    def doDelivery(self, params):
        self.tx_status = ""
        randomhost = self.query_node

        # print ("Entering doDelivery")
        txn = self.schema + "DELIVERY"
        w_id = params["w_id"]
        o_carrier_id = params["o_carrier_id"]
        ol_delivery_d = params["ol_delivery_d"]

        result = [ ]
        for d_id in range(1, constants.DISTRICTS_PER_WAREHOUSE+1):
            rs1, status = runNQuery("begin", self.prepared_dict[txn + "beginWork"],"",self.delivery_txtimeout, randomhost)
            txid = rs1[0]['txid']

            newOrder, status = runNQueryParam(self.prepared_dict[txn + "getNewOrder"], [d_id, w_id], txid, randomhost)
            if len(newOrder) == 0:
                assert len(newOrder) > 0
                ## No orders for this district: skip it. Note: This must be reported if > 1%
                continue
            no_o_id = newOrder[0]['no_o_id']
            rs, status = runNQueryParam(self.prepared_dict[txn + "getCId"], [no_o_id, d_id, w_id],txid, randomhost)
            if (status != "success"):
                continue
            c_id = rs[0]['o_c_id']

            rs2,status = runNQueryParam(self.prepared_dict[txn + "sumOLAmount"], [no_o_id, d_id, w_id], txid, randomhost)
            if (status != "success"):
                continue
            ol_total = rs2[0]['sum_ol_amount']

            result,status = runNQueryParam(self.prepared_dict[txn + "deleteNewOrder"], [d_id, w_id, no_o_id], txid, randomhost)
            if (status != "success"):
                continue

            result,status = runNQueryParam(self.prepared_dict[txn + "updateOrders"], [o_carrier_id, no_o_id, d_id, w_id], txid, randomhost)
            if (status != "success"):
                continue

            result,status = runNQueryParam(self.prepared_dict[txn + "updateOrderLine"], [ol_delivery_d, no_o_id, d_id, w_id], txid, randomhost)
            if (status != "success"):
                continue

            # These must be logged in the "result file" according to TPC-C 2.7.2.2 (page 39)
            # We remove the queued time, completed time, w_id, and o_carrier_id: the client can figure
            # them out
            # If there are no order lines, SUM returns null. There should always be order lines.
            # assert ol_total != None, "ol_total is NULL: there are no order lines. This should not happen"
            # assert ol_total > 0.0

            result,status = runNQueryParam(self.prepared_dict[txn + "updateCustomer"], [ol_total, c_id, d_id, w_id], txid, randomhost)
            if (status != "success"):
                continue

            result.append((d_id, no_o_id))
            trs, self.tx_status = runNQuery("commit", self.prepared_dict[txn + "commitWork"],txid,"",randomhost)
        ## FOR

        return result

    ## ----------------------------------------------
    ## doNewOrder
    ## ----------------------------------------------
    def doNewOrder(self, params):

        self.tx_status = ""
        randomhost = self.query_node

        # print "Entering doNewOrder"
        txn = self.schema + "NEW_ORDER"
        d_next_o_id = 0
        w_id = params["w_id"]
        d_id = params["d_id"]
        c_id = params["c_id"]

        o_entry_d = params["o_entry_d"]
        i_ids = params["i_ids"]
        i_w_ids = params["i_w_ids"]
        i_qtys = params["i_qtys"]

        assert len(i_ids) > 0
        assert len(i_ids) == len(i_w_ids)
        assert len(i_ids) == len(i_qtys)

        all_local = True
        items = [ ]
        rs, tstatus  = runNQuery("begin", self.prepared_dict[txn + "beginWork"],"",self.txtimeout, randomhost)
        txid = rs[0]['txid']
        #print txid
        for i in range(len(i_ids)):
            ## Determine if this is an all local order or not
            all_local = all_local and i_w_ids[i] == w_id
            rs, status = runNQueryParam(self.prepared_dict[txn + "getItemInfo"], [i_ids[i]], txid, randomhost)
            if len(rs) == 0:
                trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                self.tx_status = "assert"
                return
                assert len(rs) > 0
            items.append(rs[0])


        ## TPCC defines 1% of neworder gives a wrong itemid, causing rollback.
        ## Note that this will happen with 1% of transactions on purpose.
        for item in items:
            if len(item) == 0:
                ## TODO Abort here!
                trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                return
        ## FOR

        ## ----------------
        ## Collect Information from WAREHOUSE, DISTRICT, and CUSTOMER
        ## ----------------
        rs, status = runNQueryParam(self.prepared_dict[txn + "getWarehouseTaxRate"], [w_id], txid, randomhost)
        customer_info = rs
        if (status != "success"):
             trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
             return
        if len(rs) > 0:
            w_tax = rs[0]['w_tax']

        district_info, status = runNQueryParam(self.prepared_dict[txn +"getDistrict"], [d_id, w_id], txid, randomhost)
        if len(district_info) != 0:
            d_tax = district_info[0]['d_tax']
            d_next_o_id = district_info[0]['d_next_o_id']

        rs, status = runNQueryParam(self.prepared_dict[txn + "getCustomer"], [w_id, d_id, c_id], txid, randomhost)
        if len(rs) != 0:
            c_discount = rs[0]['c_discount']

        ## ----------------
        ## Insert Order Information
        ## ----------------
        ol_cnt = len(i_ids)
        o_carrier_id = constants.NULL_CARRIER_ID

        rs, status = runNQueryParam(self.prepared_dict[txn + "incrementNextOrderId"], [d_next_o_id + 1, d_id, w_id], txid, randomhost)
        if (status != "success"):
             trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
             return

        rs, status = runNQueryParam(self.prepared_dict[txn + "createOrder"], [d_next_o_id, d_id, w_id, c_id, o_entry_d, o_carrier_id, ol_cnt, all_local], txid, randomhost)
        if (status != "success"):
             trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
             return

        rs,status = runNQueryParam(self.prepared_dict[txn + "createNewOrder"], [d_next_o_id, d_id, w_id], txid, randomhost)
        if (status != "success"):
             trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
             return

        #print "NewOrder Stage #1"

        ## ----------------
        ## Insert Order Item Information
        ## ----------------
        item_data = [ ]
        total = 0
        # print  len(i_ids)
        for i in range(len(i_ids)):
            ol_number = i + 1
            ol_supply_w_id = i_w_ids[i]
            ol_i_id = i_ids[i]
            ol_quantity = i_qtys[i]
            itemInfo = items[i]

            # print "itemInfo: " + str(itemInfo)
            i_name = itemInfo["i_name"]
            i_data = itemInfo["i_data"]
            i_price = itemInfo["i_price"]

            # print "NewOrder Stage #3"
            stockInfo, status = runNQueryParam(self.prepared_dict[txn + str(d_id) + "getStockInfo"], [ol_i_id, ol_supply_w_id], txid, randomhost)
            if len(stockInfo) == 0:
                trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                logging.warn("No STOCK record for (ol_i_id=%d, ol_supply_w_id=%d)" % (ol_i_id, ol_supply_w_id))
                return

            # print "NewOrder Stage #4"
            # print "stockInfo = " + str(stockInfo)
            s_quantity = stockInfo[0]["s_quantity"]
            s_ytd = stockInfo[0]["s_ytd"]
            s_order_cnt = stockInfo[0]["s_order_cnt"]
            s_remote_cnt = stockInfo[0]["s_remote_cnt"]
            s_data = stockInfo[0]["s_data"]

            if self.schema == constants.CH2_DRIVER_SCHEMA["CH2"]:
                distxx = "s_dist_" + str(d_id).zfill(2)
                s_dist_xx = stockInfo[0][distxx] # Fetches data from the s_dist_[d_id] column
            else:
                s_dists = stockInfo[0]["s_dists"] # Fetches data from the s_dist_[d_id] column
                s_dist_xx = s_dists[d_id-1]
            # print "NewOrder Stage #4.01"
            # print distxx
            # print stockInfo[0][distxx]
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
            rs, status = runNQueryParam(self.prepared_dict[txn + "updateStock"], [s_quantity, s_ytd, s_order_cnt, s_remote_cnt, ol_i_id, ol_supply_w_id], txid, randomhost)
            if (status != "success"):
                 trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                 return

            if i_data.find(constants.ORIGINAL_STRING) != -1 and s_data.find(constants.ORIGINAL_STRING) != -1:
                brand_generic = 'B'
            else:
                brand_generic = 'G'

            ## Transaction profile states to use "ol_quantity * i_price"
            ol_amount = ol_quantity * i_price
            total += ol_amount

            rs, status = runNQueryParam(self.prepared_dict[txn + "createOrderLine"], [d_next_o_id, d_id, w_id, ol_number, ol_i_id, ol_supply_w_id, o_entry_d, ol_quantity, ol_amount, s_dist_xx], txid, randomhost)


            ## Add the info to be returned
            item_data.append( (i_name, s_quantity, brand_generic, i_price, ol_amount) )
        ## FOR
        trs, self.tx_status = runNQuery("commit", self.prepared_dict[txn + "commitWork"], txid, "",randomhost)

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

        self.tx_status = ""
        randomhost = self.query_node

#       print ("Entering doOrderStatus")
        txn = self.schema + "ORDER_STATUS"
        w_id = params["w_id"]
        d_id = params["d_id"]
        c_id = params["c_id"]
        c_last = params["c_last"]

        assert w_id, pformat(params)
        assert d_id, pformat(params)

        rs, tstatus = runNQuery("begin", self.prepared_dict[txn + "beginWork"],"",self.txtimeout, randomhost)
        txid = rs[0]['txid']
        if c_id != None:
            customerlist,status = runNQueryParam(self.prepared_dict[txn + "getCustomerByCustomerId"], [w_id, d_id, c_id], txid, randomhost)
            if len(customerlist) == 0 :
                 trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                 self.tx_status = "assert"
                 return
                 assert len(customerlist) > 0
            customer = customerlist[0]
        else:
            # Get the midpoint customer's id
            all_customers,status = runNQueryParam(self.prepared_dict[txn + "getCustomersByLastName"], [w_id, d_id, c_last], txid, randomhost)
            if len(all_customers) == 0 :
                 trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                 self.tx_status = "assert"
                 return
                 assert len(all_customers) > 0
            namecnt = len(all_customers)
            index = int((namecnt-1)/2)
            customer = all_customers[index]
            c_id = customer['c_id']

        if len(customer) == 0 or c_id == None :
            trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
            self.tx_status = "assert"
            return
            assert (len(customer) > 0 or c_id != None)

        order,status = runNQueryParam(self.prepared_dict[txn + "getLastOrder"], [w_id, d_id, c_id], txid, randomhost)
        if len(order) > 0:
            orderLines,status = runNQueryParam(self.prepared_dict[txn + "getOrderLines"], [w_id, d_id, order[0]['o_id']], txid, randomhost)
        else:
            orderLines = [ ]
        trs, self.tx_status = runNQuery("commit", self.prepared_dict[txn + "commitWork"], txid, "",randomhost)

        #Keshav: self.conn.commit()
        return [ customer, order, orderLines ]

    ## ----------------------------------------------
    ## doPayment
    ## ----------------------------------------------
    def doPayment(self, params):
        # print "Entering doPayment"

        self.tx_status = ""
        randomhost = self.query_node

        txn = self.schema + "PAYMENT"
        w_id = params["w_id"]
        d_id = params["d_id"]
        h_amount = params["h_amount"]
        c_w_id = params["c_w_id"]
        c_d_id = params["c_d_id"]
        c_id = params["c_id"]
        c_last = params["c_last"]
        h_date = params["h_date"]

        rs, tstatus = runNQuery("begin", self.prepared_dict[txn + "beginWork"],"",self.txtimeout, randomhost)
        txid = rs[0]['txid']

        if c_id != None:
            customerlist,status = runNQueryParam(self.prepared_dict[txn + "getCustomerByCustomerId"], [w_id, d_id, c_id], txid, randomhost)
            if len(customerlist) == 0 :
                 trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                 self.tx_status = "assert"
                 return
                 assert len(customerlist) > 0

            customer = customerlist[0]
        else:
            # Get the midpoint customer's id
            all_customers,status = runNQueryParam(self.prepared_dict[txn + "getCustomersByLastName"], [w_id, d_id, c_last], txid, randomhost)
            if len(all_customers) == 0 :
                 trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                 self.tx_status = "assert"
                 return
                 assert len(all_customers) > 0

            namecnt = len(all_customers)
            index = int((namecnt-1)/2)
            customer = all_customers[index]
            c_id = customer['c_id']

        if len(customer) == 0 or c_id == None :
            trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
            self.tx_status = "assert"
            return
            assert (len(customer) > 0 or c_id != None)

        c_balance = customer['c_balance'] - h_amount
        c_ytd_payment = customer['c_ytd_payment'] + h_amount
        c_payment_cnt = customer['c_payment_cnt'] + 1
        c_data = customer['c_data']

        #print "doPayment: Stage 2"

        warehouse,status = runNQueryParam(self.prepared_dict[txn + "getWarehouse"], [w_id], txid, randomhost)
        if (status != "success"):
             trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
             return

        district,status = runNQueryParam(self.prepared_dict[txn + "getDistrict"], [w_id, d_id], txid, randomhost)
        if (status != "success"):
             trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
             return

        rs, status = runNQueryParam(self.prepared_dict[txn + "updateWarehouseBalance"], [h_amount, w_id], txid, randomhost)
        if (status != "success"):
             trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
             return

        rs, status = runNQueryParam(self.prepared_dict[txn + "updateDistrictBalance"], [h_amount, w_id, d_id], txid, randomhost)
        if (status != "success"):
             trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
             return

        #print "doPayment: Stage3"

        # Customer Credit Information
        if customer['c_credit'] == constants.BAD_CREDIT:
            newData = " ".join(map(str, [c_id, c_d_id, c_w_id, d_id, w_id, h_amount]))
            c_data = (newData + "|" + c_data)
            if len(c_data) > constants.MAX_C_DATA: c_data = c_data[:constants.MAX_C_DATA]
            rs, status = runNQueryParam(self.prepared_dict[txn + "updateBCCustomer"], [c_balance, c_ytd_payment, c_payment_cnt, c_data, c_w_id, c_d_id, c_id], txid, randomhost)
            if (status != "success"):
                 trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                 return
        else:
            c_data = ""
            rs, status = runNQueryParam(self.prepared_dict[txn + "updateGCCustomer"], [c_balance, c_ytd_payment, c_payment_cnt, c_w_id, c_d_id, c_id], txid, randomhost)
            if (status != "success"):
                 trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                 return

        #print "doPayment: Stage4"
        # Concatenate w_name, four spaces, d_name
        # print "warehouse %s" % (str(warehouse))
        # print "district %s" % (str(district))
        h_data = "%s    %s" % (warehouse[0]['w_name'], district[0]['d_name'])
        # Create the history record
        rs, status = runNQueryParam(self.prepared_dict[txn + "insertHistory"], [c_id, c_d_id, c_w_id, d_id, w_id, h_date, h_amount, h_data], txid, randomhost)
        if (status != "success"):
                 trs, self.tx_status = runNQuery("rollback", self.prepared_dict[txn + "rollbackWork"],txid,"",randomhost)
                 return

        trs, self.tx_status = runNQuery("commit", self.prepared_dict[txn + "commitWork"], txid,"",randomhost)
        #Keshav: self.conn.commit()

        # TPC-C 2.5.3.3: Must display the following fields:
        # w_id, d_id, c_id, c_d_id, c_w_id, w_street_1, w_street_2, w_city, w_state, w_zip,
        # d_street_1, d_street_2, d_city, d_state, d_zip, c_first, c_middle, c_last, c_street_1,
        # c_street_2, c_city, c_state, c_zip, c_phone, c_since, c_credit, c_credit_lim,
        # c_discount, c_balance, the first 200 characters of c_data (only if c_credit = "BC"),
        # h_amount, and h_date.

        # print "doPayment: Stage5"
        # Hand back all the warehouse, district, and customer data
        return [ warehouse, district, customer ]

    ## ----------------------------------------------
    ## doStockLevel
    ## ----------------------------------------------
    def doStockLevel(self, params):

        self.tx_status = ""
        randomhost = self.query_node

        # print "Entering doStockLevel"
        txn = self.schema + "STOCK_LEVEL"
        w_id = params["w_id"]
        d_id = params["d_id"]
        threshold = params["threshold"]

        #rs = runNQuery("BEGIN WORK","",self.stock_txtimeout, randomhost)
        #txid = rs[0]['txid']
        result, self.tx_status = runNQueryParam(self.prepared_dict[txn + "getOId"], [w_id, d_id],"", randomhost)
        assert result
        o_id = result[0]['d_next_o_id']

        result, self.tx_status = runNQueryParam(self.prepared_dict[txn + "getStockCount"], [w_id, d_id, o_id, (o_id - 20), w_id, threshold], "", randomhost)

        #self.conn.commit()
        #rs, status = runNQueryParam(self.prepared_dict[txn + "getCustomerOrdersByDistrict"], [d_id], "", randomhost)
        #rs, status = runNQueryParam(self.prepared_dict[txn + "getOrdersByDistrict"], [d_id], "", randomhost)
        #Taking too long with 10Warehouses.So disabling 
        #rs, status = runNQueryParam(self.prepared_dict[txn + 'ansigetStockCount'], [w_id, d_id, o_id, (o_id - 20), w_id, threshold], txid, randomhost)

        #runNQuery("COMMIT WORK", txid, "", randomhost)
        return int(result[0]['cnt_ol_i_id'])


    def runCH2Queries(self, duration, endBenchmarkTime, queryIterNum):
        qry_times = {}

        try:
            request_params = json.loads(os.environ.get("ACLIENT_REQUEST_PARAMS", "{}"))
        except json.JSONDecodeError:
            logging.warning("Failed to decode JSON from environment variable ACLIENT_REQUEST_PARAMS")
            request_params = {}
        logging.info("Extra request params: %s" % json.dumps(request_params))

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
                if self.analyticalQueries == constants.CH2_DRIVER_ANALYTICAL_QUERIES["HAND_OPTIMIZED_QUERIES"]:
                    ch2_queries = constants.CH2_QUERIES
                else:
                    ch2_queries = constants.CH2_QUERIES_NON_OPTIMIZED
            else:
                if self.analyticalQueries == constants.CH2_DRIVER_ANALYTICAL_QUERIES["HAND_OPTIMIZED_QUERIES"]:
                    ch2_queries = constants.CH2PP_QUERIES
                else:
                    ch2_queries = constants.CH2PP_QUERIES_NON_OPTIMIZED

            if bool(int(os.environ.get("IGNORE_SKIP_INDEX_HINTS", 0))):
                pattern = re.compile(r"\/\*\+\sskip-index\s\*\/")
                ch2_queries = {
                    k: re.sub(pattern, "", v) for k, v in ch2_queries.items()
                }

            for qry in ch2_queries_perm:
                query_id_str = "AClient %d:Loop %d:%s:" % (self.client_id + 1, queryIterNum + 1, qry)
                query = ch2_queries[qry]
                stmt = {"statement": query} | request_params

                start = time.time()
                startTime = time.strftime("%H:%M:%S", time.localtime(start))

                # In benchmark run mode, if the duration has elapsed, stop executing queries
                if duration is not None:
                    if start > endBenchmarkTime:
                        logging.debug("%s started at:   %s (started after the duration of the benchmark)" % (query_id_str, startTime))
                        break

                logging.info("%s started at: %s " % (query_id_str, startTime))
                body = n1ql_execute(self.analytics_node, stmt, 0)
                end = time.time()
                endTime = time.strftime("%H:%M:%S", time.localtime(end))

                # In benchmark run mode, if the duration has elapsed, stop reporting queries
                if duration is not None:
                    if end > endBenchmarkTime:
                        logging.debug("%s ended at:   %s (ended after the duration of the benchmark)" % (query_id_str, endTime))
                        break

                logging.info("%s ended at:   %s" % (query_id_str, endTime))
                logging.info(
                    "%s plans:\n%s"
                    % (query_id_str, body.get("plans", {}).get("optimizedLogicalPlan"))
                )
                logging.info("%s metrics:    %s" % (query_id_str, body.get("metrics")))

                qry_times[qry] = [
                    self.client_id + 1,
                    queryIterNum + 1,
                    startTime,
                    body.get("metrics", {}).get("executionTime", "infs"),
                    endTime,
                ]
        return qry_times
## CLASS
