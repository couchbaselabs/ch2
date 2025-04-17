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

MONEY_DECIMALS = 2

#  Item constants
NUM_ITEMS = 100000
MIN_IM = 1
MAX_IM = 10000
MIN_PRICE = 1.00
MAX_PRICE = 100.00
MIN_I_NAME = 14
MAX_I_NAME = 24
MIN_I_DATA = 26
MAX_I_DATA = 50

#  Warehouse constants
MIN_TAX = 0
MAX_TAX = 0.2000
TAX_DECIMALS = 4
INITIAL_W_YTD = 300000.00
MIN_NAME = 6
MAX_NAME = 10
MIN_STREET = 10
MAX_STREET = 20
MIN_CITY = 10
MAX_CITY = 20
STATE = 2
ZIP_LENGTH = 9
ZIP_SUFFIX = "11111"

# Warehouse constants
STARTING_WAREHOUSE = 1

#  Stock constants
MIN_QUANTITY = 10
MAX_QUANTITY = 100
DIST = 24
STOCK_PER_WAREHOUSE = 100000

#  District constants
DISTRICTS_PER_WAREHOUSE = 10
INITIAL_D_YTD = 30000.00  #  different from Warehouse
INITIAL_NEXT_O_ID = 3001

#  Customer constants
CUSTOMERS_PER_DISTRICT = 3000
INITIAL_CREDIT_LIM = 50000.00
MIN_DISCOUNT = 0.0000
MAX_DISCOUNT = 0.5000
DISCOUNT_DECIMALS = 4
INITIAL_BALANCE = -10.00
MIN_BALANCE = -50.00
MAX_BALANCE = 50.00
INITIAL_YTD_PAYMENT = 10.00
INITIAL_PAYMENT_CNT = 1
INITIAL_DELIVERY_CNT = 0
MIN_FIRST = 6
MAX_FIRST = 10
MIDDLE = "OE"
PHONE = 16
MIN_C_DATA = 300
MAX_C_DATA = 500
GOOD_CREDIT = "GC"
BAD_CREDIT = "BC"

#  Order constants
MIN_CARRIER_ID = 1
MAX_CARRIER_ID = 10
#  HACK: This is not strictly correct, but it works
NULL_CARRIER_ID = 0
#  o_id < than this value, carrier != null, >= -> carrier == null
NULL_CARRIER_LOWER_BOUND = 2101
MIN_OL_CNT = 5
MAX_OL_CNT = 15
INITIAL_ALL_LOCAL = 1
INITIAL_ORDERS_PER_DISTRICT = 3000

#  Used to generate initial orderline quantities and new order orderline amounts
MIN_OL_QUANTITY = 1
MAX_OL_QUANTITY = 50

#  Order line constants
INITIAL_QUANTITY = 5
MIN_AMOUNT = 0.01

#  History constants
MIN_DATA = 12
MAX_DATA = 24
INITIAL_AMOUNT = 10.00

#  New order constants
INITIAL_NEW_ORDERS_PER_DISTRICT = 900

# Supplier constants
NUM_SUPPLIERS = 10000
NUM_LEADING_ZEROS = 9
MIN_SUPPLIER_ADDRESS = 10
MAX_SUPPLIER_ADDRESS = 40
MIN_SUPPLIER_ACCTBAL = -999.99
MAX_SUPPLIER_ACCTBAL = 9999.99
MIN_SUPPLIER_COMMENT = 25
MAX_SUPPLIER_COMMENT = 100

# Nation constants
NUM_NATIONS = 62
MIN_NATION_COMMENT = 31
MAX_NATION_COMMENT = 114

# Region constants
NUM_REGIONS = 5
MIN_REGION_COMMENT = 31
MAX_REGION_COMMENT = 115

#  TPC-C 2.4.3.4 (page 31) says this must be displayed when new order rolls back.
INVALID_ITEM_MESSAGE = "Item number is not valid"

#  Used to generate stock level transactions
MIN_STOCK_LEVEL_THRESHOLD = 10
MAX_STOCK_LEVEL_THRESHOLD = 20

#  Used to generate payment transactions
MIN_PAYMENT = 1.0
MAX_PAYMENT = 5000.0

#  Indicates "brand" items and stock in i_data and s_data.
ORIGINAL_STRING = "ORIGINAL"

CH2_NAMESPACE = "default"
CH2_BUCKET = "bench"

NUM_LOAD_RETRIES = 10
CH2_DRIVER_LOAD_MODE = {
    "NOT_SET": -1,
    "DATASVC_BULKLOAD": 0,
    "DATASVC_LOAD": 1,
    "QRYSVC_LOAD": 2,
    "DOCGEN_LOAD": 3,
}
CH2_DRIVER_LOAD_FORMAT = {
    "JSON":0,
    "CSV":1
}
CH2_DRIVER_SCHEMA = {
    "CH2":"ch2",
    "CH2P":"ch2p",
    "CH2PP":"ch2pp",
    "CH2PPF":"ch2ppf"
}
CH2_DRIVER_ANALYTICAL_QUERIES = {
    "HAND_OPTIMIZED_QUERIES":0,
    "NON_OPTIMIZED_QUERIES":1
}

MAX_EXTRA_FIELDS = 128
CH2_CUSTOMER_EXTRA_FIELDS = {
    "NOT_SET":-1,
    CH2_DRIVER_SCHEMA["CH2"]:0,
    CH2_DRIVER_SCHEMA["CH2P"]:0,
    CH2_DRIVER_SCHEMA["CH2PP"]:128,
    CH2_DRIVER_SCHEMA["CH2PPF"]:128,
}
CH2_ORDERS_EXTRA_FIELDS = {
    "NOT_SET":-1,
    CH2_DRIVER_SCHEMA["CH2"]:0,
    CH2_DRIVER_SCHEMA["CH2P"]:0,
    CH2_DRIVER_SCHEMA["CH2PP"]:128,
    CH2_DRIVER_SCHEMA["CH2PPF"]:128,
}
CH2_ITEM_EXTRA_FIELDS = {
    "NOT_SET":-1,
    CH2_DRIVER_SCHEMA["CH2"]:0,
    CH2_DRIVER_SCHEMA["CH2P"]:0,
    CH2_DRIVER_SCHEMA["CH2PP"]:128,
    CH2_DRIVER_SCHEMA["CH2PPF"]:128,
}

CH2_DATAGEN_SEED_NOT_SET = -1

CH2_DRIVER_KV_TIMEOUT = 10
CH2_DRIVER_BULKLOAD_BATCH_SIZE = 1024 * 256 # 256K

# Table Names
TABLENAME_ITEM       = "item"
TABLENAME_ITEM_CATEGORIES_FLAT = "item_categories"
TABLENAME_WAREHOUSE  = "warehouse"
TABLENAME_DISTRICT   = "district"
TABLENAME_CUSTOMER   = "customer"
TABLENAME_STOCK      = "stock"
TABLENAME_ORDERS     = "orders"
TABLENAME_NEWORDER   = "neworder"
TABLENAME_ORDERLINE  = "orderline_nested"
TABLENAME_ORDERLINE_FLAT  = "orders_orderline"
TABLENAME_HISTORY    = "history"
TABLENAME_SUPPLIER   = "supplier"
TABLENAME_NATION     = "nation"
TABLENAME_REGION     = "region"
TABLENAME_WAREHOUSE_ADDRESS  = "warehouse_address_nested"
TABLENAME_DISTRICT_ADDRESS  = "district_address_nested"
TABLENAME_CUSTOMER_NAME  = "customer_name_nested"
TABLENAME_CUSTOMER_ADDRESSES  = "customer_addresses_nested"
TABLENAME_CUSTOMER_ADDRESSES_FLAT  = "customer_addresses"
TABLENAME_CUSTOMER_PHONES  = "customer_phones_nested"
TABLENAME_CUSTOMER_PHONES_FLAT  = "customer_phones"
TABLENAME_CUSTOMER_ITEM_CATEGORIES_FLAT = "customer_item_categories"
TABLENAME_SUPPLIER_ADDRESS  = "supplier_address_nested"

COLLECTIONS_DICT = {
    TABLENAME_ITEM:"item",
    TABLENAME_ITEM_CATEGORIES_FLAT:"item_categories",
    TABLENAME_WAREHOUSE:"warehouse",
    TABLENAME_DISTRICT:"district",
    TABLENAME_CUSTOMER:"customer",
    TABLENAME_STOCK:"stock",
    TABLENAME_ORDERS:"orders",
    TABLENAME_NEWORDER:"neworder",
    TABLENAME_ORDERLINE:"orderline_nested",
    TABLENAME_ORDERLINE_FLAT:"orders_orderline",
    TABLENAME_HISTORY:"history",
    TABLENAME_SUPPLIER:"supplier",
    TABLENAME_NATION:"nation",
    TABLENAME_REGION:"region",
    TABLENAME_CUSTOMER_ADDRESSES_FLAT:"customer_addresses",
    TABLENAME_CUSTOMER_PHONES_FLAT:"customer_phones",
    TABLENAME_CUSTOMER_ITEM_CATEGORIES_FLAT:"customer_item_categories"}

ALL_TABLES = [
    TABLENAME_ITEM,
    TABLENAME_ITEM_CATEGORIES_FLAT,
    TABLENAME_WAREHOUSE,
    TABLENAME_DISTRICT,
    TABLENAME_CUSTOMER,
    TABLENAME_CUSTOMER_ADDRESSES_FLAT,
    TABLENAME_CUSTOMER_PHONES_FLAT,
    TABLENAME_CUSTOMER_ITEM_CATEGORIES_FLAT,
    TABLENAME_STOCK,
    TABLENAME_ORDERS,
    TABLENAME_ORDERLINE,
    TABLENAME_ORDERLINE_FLAT,
    TABLENAME_NEWORDER,
    TABLENAME_HISTORY,
    TABLENAME_SUPPLIER,
    TABLENAME_NATION,
    TABLENAME_REGION
]

NATIONS = [
    [48, "Algeria", 0],
    [49, "Argentina", 1],
    [50, "Brazil", 1],
    [51, "Canada", 1],
    [52, "Egypt", 4],
    [53, "Ethiopia", 0],
    [54, "France", 3],
    [55, "Germany", 3],
    [56, "India", 2],
    [57, "Indonesia", 2],

    [65, "Iran", 4],
    [66, "Iraq", 4],
    [67, "Japan", 2],
    [68, "Jordan", 4],
    [69, "Kenya", 0],
    [70, "Morocco", 0],
    [71, "Mozambique", 0],
    [72, "Peru", 1],
    [73, "China", 2],
    [74, "Kuwait", 4],
    [75, "Saudi Arabia", 4],
    [76, "Vietnam", 2],
    [77, "Russia", 3],
    [78, "United Kingdom", 3],
    [79, "United States", 1],
    [80, "Lebanon", 4],
    [81, "Oman", 4],
    [82, "Qatar", 4],
    [83, "Mexico", 1],
    [84, "Turkey", 4],
    [85, "Chile", 1],
    [86, "Italy", 3],
    [87, "South Africa", 0],
    [88, "South Korea", 2],
    [89, "Colombia", 1],
    [90, "Spain", 3],

    [97, "Ukraine", 3],
    [98, "Ecuador", 1],
    [99, "Sudan", 0],
    [100, "Uzbekistan", 2],
    [101, "Malaysia", 2],
    [102, "Venezuela", 1],
    [103, "Tanzania", 0],
    [104, "Afghanistan", 2],
    [105, "North Korea", 2],
    [106, "Taiwan", 2],
    [107, "Ghana", 0],
    [108, "Ivory Coast", 0],
    [109, "Syria", 4],
    [110, "Madagascar", 0],
    [111, "Cameroon", 0],
    [112, "Nigeria", 0],
    [113, "Bolivia", 1],
    [114, "Netherlands", 3],
    [115, "Cambodia", 2],
    [116, "Belgium", 3],
    [117, "Greece", 3],
    [118, "Uruguay", 1],
    [119, "Israel", 4],
    [120, "Finland", 3],
    [121, "Singapore", 2],
    [122, "Norway", 3]
]

REGIONS = ["Africa", "America", "Asia", "Europe", "Middle East"]

KEYNAMES = {
        TABLENAME_ITEM:         [0],  # INTEGER
        TABLENAME_ITEM_CATEGORIES_FLAT: [0, 1],
        TABLENAME_WAREHOUSE:    [0],  # INTEGER
        TABLENAME_DISTRICT:     [1, 0],  # INTEGER
        TABLENAME_CUSTOMER:     [2, 1, 0], # INTEGER
        TABLENAME_STOCK:        [1, 0],  # INTEGER
        TABLENAME_ORDERS:       [3, 2, 0], # INTEGER
        TABLENAME_NEWORDER:     [2, 1, 0], # INTEGER
        TABLENAME_ORDERLINE:    [2, 1, 0, 3], # INTEGER
        TABLENAME_ORDERLINE_FLAT: [2, 1, 0, 3], # INTEGER
        TABLENAME_HISTORY:      [2, 1, 0], # INTEGER
        TABLENAME_SUPPLIER:     [0],  # INTEGER
        TABLENAME_NATION:       [0],  # INTEGER
        TABLENAME_REGION:       [0],  # INTEGER
        TABLENAME_CUSTOMER_ADDRESSES_FLAT: [2, 1, 0, 3],
        TABLENAME_CUSTOMER_PHONES_FLAT: [2, 1, 0, 4],
        TABLENAME_CUSTOMER_ITEM_CATEGORIES_FLAT: [2, 1, 0, 3],
}

CH2_TABLE_COLUMNS = {
    TABLENAME_ITEM: [
        "i_id", # INTEGER
        "i_name", # VARCHAR
        "i_price", # FLOAT
        "i_extra", # Extra unused fields
        "i_categories", # ARRAY
        "i_data", # VARCHAR
        "i_im_id", # INTEGER
    ],
    TABLENAME_WAREHOUSE: [
        "w_id", # SMALLINT
        "w_ytd", # FLOAT
        "w_tax", # FLOAT
        "w_name", # VARCHAR
        "w_street_1", # VARCHAR
        "w_street_2", # VARCHAR
        "w_city", # VARCHAR
        "w_state", # VARCHAR
        "w_zip", # VARCHAR
    ],
    TABLENAME_DISTRICT: [
        "d_id", # TINYINT
        "d_w_id", # SMALLINT
        "d_ytd", # FLOAT
        "d_tax", # FLOAT
        "d_next_o_id", # INT
        "d_name", # VARCHAR
        "d_street_1", # VARCHAR
        "d_street_2", # VARCHAR
        "d_city", # VARCHAR
        "d_state", # VARCHAR
        "d_zip", # VARCHAR
    ],
    TABLENAME_CUSTOMER:   [
        "c_id", # INTEGER
        "c_d_id", # TINYINT
        "c_w_id", # SMALLINT
        "c_discount", # FLOAT
        "c_credit", # VARCHAR
        "c_first", # VARCHAR
        "c_middle", # VARCHAR
        "c_last", # VARCHAR
        "c_credit_lim", # FLOAT
        "c_balance", # FLOAT
        "c_ytd_payment", # FLOAT
        "c_payment_cnt", # INTEGER
        "c_delivery_cnt", # INTEGER
        "c_extra", # Extra unused fields
        "c_street_1", # VARCHAR
        "c_street_2", # VARCHAR
        "c_city", # VARCHAR
        "c_state", # VARCHAR
        "c_zip", # VARCHAR
        "c_phone", # VARCHAR
        "c_since", # TIMESTAMP
        "c_item_categories", # ARRAY
        "c_data", # VARCHAR
    ],
    TABLENAME_STOCK:      [
        "s_i_id", # INTEGER
        "s_w_id", # SMALLINT
        "s_quantity", # INTEGER
        "s_ytd", # INTEGER
        "s_order_cnt", # INTEGER
        "s_remote_cnt", # INTEGER
        "s_data", # VARCHAR
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
    ],
    TABLENAME_ORDERS:     [
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
    TABLENAME_NEWORDER:  [
        "no_o_id", # INTEGER
        "no_d_id", # TINYINT
        "no_w_id", # SMALLINT
    ],
    TABLENAME_ORDERLINE: [
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
    TABLENAME_HISTORY:    [
        "h_c_id", # INTEGER
        "h_c_d_id", # TINYINT
        "h_c_w_id", # SMALLINT
        "h_d_id", # TINYINT
        "h_w_id", # SMALLINT
        "h_date", # TIMESTAMP
        "h_amount", # FLOAT
        "h_data", # VARCHAR
    ],
    TABLENAME_SUPPLIER:    [
        "su_suppkey", # INTEGER
        "su_name", # VARCHAR
        "su_address", # VARCHAR
        "su_nationkey", # INTEGER
        "su_phone", # VARCHAR
        "su_acctbal", # FLOAT
        "su_comment", # VARCHAR
    ],
    TABLENAME_NATION:    [
        "n_nationkey", # INTEGER
        "n_name", # VARCHAR
        "n_regionkey", # INTEGER
        "n_comment", # VARCHAR
    ],
    TABLENAME_REGION:    [
        "r_regionkey", # INTEGER
        "r_name", # VARCHAR
        "r_comment", # VARCHAR
    ],
}

CH2PP_TABLE_COLUMNS = {
    TABLENAME_ITEM: [
        "i_id", # INTEGER
        "i_name", # VARCHAR
        "i_price", # FLOAT
        "i_extra", # Extra unused fields
        "i_categories", # ARRAY
        "i_data", # VARCHAR
        "i_im_id", # INTEGER
    ],
    TABLENAME_ITEM_CATEGORIES_FLAT:    [
        "i_id", # INTEGER
        "i_category", # VARCHAR
    ],
    TABLENAME_WAREHOUSE: [
        "w_id", # SMALLINT
        "w_ytd", # FLOAT
        "w_tax", # FLOAT
        "w_name", # VARCHAR
        "w_address", # JSON
    ],
    TABLENAME_DISTRICT: [
        "d_id", # TINYINT
        "d_w_id", # SMALLINT
        "d_ytd", # FLOAT
        "d_tax", # FLOAT
        "d_next_o_id", # INT
        "d_name", # VARCHAR
        "d_address", # JSON
    ],
    TABLENAME_CUSTOMER:   [
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
    TABLENAME_STOCK:      [
        "s_i_id", # INTEGER
        "s_w_id", # SMALLINT
        "s_quantity", # INTEGER
        "s_ytd", # INTEGER
        "s_order_cnt", # INTEGER
        "s_remote_cnt", # INTEGER
        "s_data", # VARCHAR
        "s_dists", # ARRAY
    ],
    TABLENAME_ORDERS:     [
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
    TABLENAME_NEWORDER:  [
        "no_o_id", # INTEGER
        "no_d_id", # TINYINT
        "no_w_id", # SMALLINT
    ],
    TABLENAME_ORDERLINE: [
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
    TABLENAME_ORDERLINE_FLAT: [
        "o_id", # INTEGER
        "o_d_id", # TINYINT
        "o_w_id", # SMALLINT
        "ol_number", # INTEGER
        "ol_i_id", # INTEGER
        "ol_supply_w_id", # SMALLINT
        "ol_delivery_d", # TIMESTAMP
        "ol_quantity", # INTEGER
        "ol_amount", # FLOAT
        "ol_dist_info", # VARCHAR
    ],
    TABLENAME_HISTORY:    [
        "h_c_id", # INTEGER
        "h_c_d_id", # TINYINT
        "h_c_w_id", # SMALLINT
        "h_d_id", # TINYINT
        "h_w_id", # SMALLINT
        "h_date", # TIMESTAMP
        "h_amount", # FLOAT
        "h_data", # VARCHAR
    ],
    TABLENAME_SUPPLIER:    [
        "su_suppkey", # INTEGER
        "su_name", # VARCHAR
        "su_address", # JSON
        "su_nationkey", # INTEGER
        "su_phone", # VARCHAR
        "su_acctbal", # FLOAT
        "su_comment", # VARCHAR
    ],
    TABLENAME_NATION:    [
        "n_nationkey", # INTEGER
        "n_name", # VARCHAR
        "n_regionkey", # INTEGER
        "n_comment", # VARCHAR
    ],
    TABLENAME_REGION:    [
        "r_regionkey", # INTEGER
        "r_name", # VARCHAR
        "r_comment", # VARCHAR
    ],
    TABLENAME_WAREHOUSE_ADDRESS:    [
        "w_street_1", # VARCHAR
        "w_street_2", # VARCHAR
        "w_city", # VARCHAR
        "w_state", # VARCHAR
        "w_zip", # VARCHAR
    ],
    TABLENAME_DISTRICT_ADDRESS:    [
        "d_street_1", # VARCHAR
        "d_street_2", # VARCHAR
        "d_city", # VARCHAR
        "d_state", # VARCHAR
        "d_zip", # VARCHAR
    ],
    TABLENAME_CUSTOMER_NAME:    [
        "c_first", # VARCHAR
        "c_middle", # VARCHAR
        "c_last", # VARCHAR
    ],
    TABLENAME_CUSTOMER_ADDRESSES:    [
        "c_address_kind", # VARCHAR
        "c_street_1", # VARCHAR
        "c_street_2", # VARCHAR
        "c_city", # VARCHAR
        "c_state", # VARCHAR
        "c_zip", # VARCHAR
    ],
    TABLENAME_CUSTOMER_ADDRESSES_FLAT:    [
        "c_id", # INTEGER
        "c_d_id", # TINYINT
        "c_w_id", # SMALLINT
        "c_address_kind", # VARCHAR
        "c_street_1", # VARCHAR
        "c_street_2", # VARCHAR
        "c_city", # VARCHAR
        "c_state", # VARCHAR
        "c_zip", # VARCHAR
    ],
    TABLENAME_CUSTOMER_PHONES:    [
        "c_phone_kind", # VARCHAR
        "c_phone_number", # VARCHAR
    ],
    TABLENAME_CUSTOMER_PHONES_FLAT:    [
        "c_id", # INTEGER
        "c_d_id", # TINYINT
        "c_w_id", # SMALLINT
        "c_phone_kind", # VARCHAR
        "c_phone_number", # VARCHAR
    ],
    TABLENAME_CUSTOMER_ITEM_CATEGORIES_FLAT:    [
        "c_id", # INTEGER
        "c_d_id", # TINYINT
        "c_w_id", # SMALLINT
        "c_item_category", # VARCHAR
    ],
    TABLENAME_SUPPLIER_ADDRESS:    [
        "su_street_1", # VARCHAR
        "su_street_2", # VARCHAR
        "su_city", # VARCHAR
        "su_state", # VARCHAR
        "su_zip", # VARCHAR
    ],
}

TABLE_INDEXES = {
    TABLENAME_ITEM: [
        "i_id",
    ],
    TABLENAME_ITEM_CATEGORIES_FLAT: [
        "i_id",
        "i_category",
    ],
    TABLENAME_WAREHOUSE: [
        "w_id",
    ],
    TABLENAME_DISTRICT: [
        "d_id",
        "d_w_id",
    ],
    TABLENAME_CUSTOMER:   [
        "c_id",
        "c_d_id",
        "c_w_id",
    ],
    TABLENAME_CUSTOMER_ADDRESSES_FLAT:   [
        "c_id",
        "c_d_id",
        "c_w_id",
        "c_address_kind",
    ],
    TABLENAME_CUSTOMER_PHONES_FLAT:   [
        "c_id",
        "c_d_id",
        "c_w_id",
        "c_phone_number",
    ],
    TABLENAME_CUSTOMER_ITEM_CATEGORIES_FLAT:   [
        "c_id",
        "c_d_id",
        "c_w_id",
        "c_item_category",
    ],
    TABLENAME_STOCK:      [
        "s_i_id",
        "s_w_id",
    ],
    TABLENAME_ORDERS:     [
        "o_id",
        "o_d_id",
        "o_w_id",
        "o_c_id",
    ],
    TABLENAME_NEWORDER:  [
        "no_o_id",
        "no_d_id",
        "no_w_id",
    ],
    TABLENAME_ORDERLINE: [
        "ol_o_id",
        "ol_d_id",
        "ol_w_id",
    ],
    TABLENAME_ORDERLINE_FLAT: [
        "ol_o_id",
        "ol_d_id",
        "ol_w_id",
        "ol_number",
    ],
    TABLENAME_SUPPLIER:    [
        "su_suppkey",
    ],
    TABLENAME_NATION:    [
        "n_nationkey",
    ],
    TABLENAME_REGION:    [
        "r_regionkey",
    ],
}

# Transaction Types
def enum(*sequential, **named):
    enums = dict(map(lambda x: (x, x), sequential))
    # dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
TransactionTypes = enum(
    "DELIVERY",
    "NEW_ORDER",
    "ORDER_STATUS",
    "PAYMENT",
    "STOCK_LEVEL",
)
QueryTypes = enum(
    "CH2",
)

NUM_CH2_QUERIES = 22
CH2_QUERIES = {
    "Q01": "SELECT ol.ol_number ,"\
                   "SUM(ol.ol_quantity) as sum_qty ,"\
                   "SUM(ol.ol_amount) as sum_amount ,"\
                   "AVG(ol.ol_quantity) as avg_qty ,"\
                   "AVG(ol.ol_amount) as avg_amount ,"\
                   "COUNT(*) as COUNT_order "\
           "FROM     orders o, o.o_orderline ol "\
           "WHERE ol.ol_delivery_d /*+ skip-index */ > '2014-07-01 00:00:00' "\
           "GROUP BY ol.ol_number "\
           "ORDER BY ol.ol_number",

    "Q02": "SELECT su.su_suppkey, su.su_name, n.n_name, i.i_id, i.i_name, su.su_address, su.su_phone, su.su_comment "\
            "FROM (SELECT s1.s_i_id as m_i_id, MIN(s1.s_quantity) as m_s_quantity "\
                   "FROM stock s1, "\
                         "(SELECT su1.su_suppkey "\
                           "FROM supplier su1, (SELECT n1.n_nationkey from nation n1, region r1 "\
                                                "WHERE n1.n_regionkey=r1.r_regionkey AND r1.r_name LIKE 'Europ%') t1 "\
                           "WHERE su1.su_nationkey=t1.n_nationkey) t2 "\
                    "WHERE s1.s_w_id*s1.s_i_id MOD 10000 = t2.su_suppkey "\
                    "GROUP BY s1.s_i_id) m,  item i, stock s, supplier su, nation n, region r "\
             "WHERE i.i_id = s.s_i_id "\
               "AND s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "\
               "AND su.su_nationkey = n.n_nationkey "\
               "AND n.n_regionkey = r.r_regionkey "\
               "AND i.i_data LIKE '%b' "\
               "AND r.r_name LIKE 'Europ%' "\
               "AND i.i_id=m.m_i_id "\
               "AND s.s_quantity = m.m_s_quantity "\
              "ORDER BY n.n_name, su.su_name, i.i_id limit 100",

    "Q03": "WITH co as "\
           "(SELECT o.o_id, o.o_w_id, o.o_d_id, o.o_entry_d, o.o_orderline "\
            "FROM orders o, customer c "\
            "WHERE  c.c_state LIKE 'a%' "\
              "AND c.c_id = o.o_c_id AND c.c_w_id = o.o_w_id AND c.c_d_id = o.o_d_id "\
              "AND o.o_entry_d /*+ skip-index */ < '2017-03-15 00:00:00.000000') "\
           "SELECT co.o_id, co.o_w_id, co.o_d_id, SUM(ol.ol_amount) as revenue, co.o_entry_d "\
           "FROM   co, co.o_orderline ol, neworder no "\
           "WHERE no.no_w_id = co.o_w_id AND no.no_d_id = co.o_d_id AND no.no_o_id = co.o_id "\
           "GROUP BY co.o_id, co.o_w_id, co.o_d_id, co.o_entry_d "\
           "ORDER BY revenue DESC, co.o_entry_d",

    "Q04": "SELECT o.o_ol_cnt, COUNT(*) as order_COUNT "\
           "FROM   orders o "\
           "WHERE  o.o_entry_d >= '2015-07-01 00:00:00.000000' AND o.o_entry_d < '2015-10-01 00:00:00.000000' "\
           "AND EXISTS (SELECT VALUE 1 "\
                        "FROM o.o_orderline ol "\
                        "WHERE ol.ol_delivery_d >= date_add_str(o.o_entry_d, 1, 'week')) "\
           "GROUP BY o.o_ol_cnt "\
           "ORDER BY o.o_ol_cnt ",

    "Q05": "SELECT cnros.n_name, ROUND(sum (cnros.ol_amount),2) as revenue "\
           "FROM (SELECT cnro.ol_amount, cnro.n_name, cnro.n_nationkey, s.s_w_id, s.s_i_id "\
                 "FROM stock s JOIN "\
                          "(SELECT o.o_w_id, ol.ol_amount, ol.ol_i_id, cnr.n_name, cnr.n_nationkey "\
                           "FROM orders o, o.o_orderline ol JOIN "\
                              "(SELECT c.c_id, c.c_w_id, c.c_d_id, nr.n_name, nr.n_nationkey "\
                               "FROM customer c JOIN "\
                                    "(SELECT n.n_nationkey, n.n_name "\
                                     "FROM nation n, region r "\
                                     "WHERE n.n_regionkey = r.r_regionkey AND r.r_name = 'Asia') nr "\
                                   "ON string_to_codepoint(c.c_state)[0] = nr.n_nationkey) cnr "\
                               "ON o.o_entry_d >= '2016-01-01 00:00:00.000000' AND o.o_entry_d < '2017-01-01 00:00:00.000000' "\
                               "AND cnr.c_id = o.o_c_id AND cnr.c_w_id = o.o_w_id AND cnr.c_d_id = o.o_d_id) cnro "\
                         "ON cnro.o_w_id = s.s_w_id AND cnro.ol_i_id = s.s_i_id) cnros JOIN supplier su "\
                       "ON cnros.s_w_id * cnros.s_i_id MOD 10000 = su.su_suppkey AND su.su_nationkey = cnros.n_nationkey "\
           "GROUP BY cnros.n_name "\
           "ORDER BY revenue DESC",

    "Q06": "SELECT SUM(ol.ol_amount) as revenue "\
           "FROM   orders o, o.o_orderline ol "\
           "WHERE  ol.ol_delivery_d >= '2016-01-01 00:00:00.000000' "\
             "AND  ol.ol_delivery_d < '2017-01-01 00:00:00.000000' "\
             "AND  ol.ol_amount > 600",

    "Q07": "SELECT su.su_nationkey as supp_nation, SUBSTR1(n1n2cools.c_state,1,1) as cust_nation, DATE_PART_STR(n1n2cools.o_entry_d, 'year') as l_year, ROUND(SUM(n1n2cools.ol_amount),2) as revenue "\
           "FROM "\
           "(select n1n2cool.c_state, n1n2cool.o_entry_d, n1n2cool.ol_amount, n1n2cool.n1key, s.s_w_id, s.s_i_id "\
             "FROM stock s JOIN "\
              "(SELECT o.o_entry_d, ol.ol_supply_w_id, ol.ol_i_id, n1n2c.c_state, ol.ol_amount, n1n2c.n1key "\
              "FROM orders o, o.o_orderline ol JOIN "\
                "(SELECT c.c_id, c.c_w_id, c.c_d_id, c.c_state, n1n2.n1key "\
                  "FROM customer c JOIN "\
                      "(SELECT n1.n_nationkey n1key, n2.n_nationkey n2key "\
                        "FROM nation n1, nation n2 "\
                        "WHERE (n1.n_name = 'Germany' AND n2.n_name = 'Cambodia') OR (n1.n_name = 'Cambodia' AND n2.n_name = 'Germany') "\
                        ")n1n2 "\
               "ON string_to_codepoint(c.c_state)[0] = n1n2.n2key) n1n2c "\
              "ON n1n2c.c_id = o.o_c_id AND n1n2c.c_w_id = o.o_w_id AND n1n2c.c_d_id = o.o_d_id "\
              "AND ol.ol_delivery_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000') n1n2cool "\
           "ON n1n2cool.ol_supply_w_id = s.s_w_id AND n1n2cool.ol_i_id = s.s_i_id)  n1n2cools JOIN supplier su "\
           "ON n1n2cools.s_w_id * n1n2cools.s_i_id MOD 10000 = su.su_suppkey AND su.su_nationkey = n1n2cools.n1key "\
           "GROUP BY su.su_nationkey, SUBSTR1(n1n2cools.c_state,1,1), DATE_PART_STR(n1n2cools.o_entry_d, 'year') "\
           "ORDER BY su.su_nationkey, cust_nation, l_year",

    "Q08": "SELECT DATE_PART_STR(rn1coolis.o_entry_d, 'year') as l_year, "\
           "ROUND((SUM(case when sun2.n_name = 'Germany' then rn1coolis.ol_amount else 0 end) / SUM(rn1coolis.ol_amount)),2) as mkt_share "\
           "FROM "\
             "(SELECT rn1cooli.o_entry_d,  rn1cooli.ol_amount, s.s_w_id, s.s_i_id "\
              "FROM stock s JOIN "\
                 "(SELECT o.o_entry_d, ol.ol_i_id, ol.ol_amount, ol.ol_supply_w_id "\
                   "FROM orders o, o.o_orderline ol, item i JOIN "\
                     "(SELECT c.c_id, c.c_w_id, c.c_d_id "\
                       "FROM customer c JOIN "\
                         "(SELECT n1.n_nationkey "\
                           "FROM nation n1, region r "\
                           "WHERE n1.n_regionkey = r.r_regionkey AND r.r_name = 'Europe') nr "\
                         "ON nr.n_nationkey = string_to_codepoint(c.c_state)[0]) cnr "\
                     "ON cnr.c_id = o.o_c_id AND cnr.c_w_id = o.o_w_id AND cnr.c_d_id = o.o_d_id "\
                     "AND i.i_data LIKE '%b' AND i.i_id = ol.ol_i_id "\
                     "AND ol.ol_i_id < 1000 "\
                     "AND o.o_entry_d /*+ skip-index */ BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000') rn1cooli "\
                "ON rn1cooli.ol_i_id = s.s_i_id "\
                "AND rn1cooli.ol_supply_w_id = s.s_w_id) rn1coolis JOIN "\
              "(SELECT su.su_suppkey, n2.n_name "\
               "FROM supplier su, nation n2 "\
               "WHERE su.su_nationkey = n2.n_nationkey) sun2 "\
             "ON rn1coolis.s_w_id * rn1coolis.s_i_id MOD 10000 = sun2.su_suppkey "\
             "GROUP BY DATE_PART_STR(rn1coolis.o_entry_d, 'year') "\
             "ORDER BY l_year",

    "Q09": "SELECT sun.n_name, DATE_PART_STR(oolis.o_entry_d, 'year') as l_year, round (SUM(oolis.ol_amount), 2) as SUM_profit "\
           "FROM "\
            "(SELECT s.s_w_id, s.s_i_id, ooli.o_entry_d, ooli.ol_amount "\
             "FROM stock s JOIN "\
                "(SELECT ol.ol_i_id, ol.ol_supply_w_id, ol.ol_amount, o.o_entry_d "\
                 "FROM orders o,  o.o_orderline ol, item i "\
                 "WHERE  i.i_data LIKE '%bb' and ol.ol_i_id = i.i_id) ooli "\
              "ON ooli.ol_i_id = s.s_i_id and ooli.ol_supply_w_id = s.s_w_id) oolis JOIN "\
             "(SELECT su.su_suppkey, n.n_name "\
              "FROM supplier su, nation n "\
              "WHERE su.su_nationkey = n.n_nationkey) sun "\
             "ON oolis.s_w_id * oolis.s_i_id MOD 10000 = sun.su_suppkey "\
            "GROUP BY sun.n_name, DATE_PART_STR(oolis.o_entry_d, 'year') "\
            "ORDER BY sun.n_name, l_year DESC",

    "Q10": "SELECT c.c_id, c.c_last, SUM(ol.ol_amount) as revenue, c.c_city, c.c_phone, n.n_name "\
           "FROM nation n, customer c, orders o, o.o_orderline ol "\
           "WHERE  c.c_id = o.o_c_id "\
             "AND  c.c_w_id = o.o_w_id "\
             "AND  c.c_d_id = o.o_d_id "\
             "AND  o.o_entry_d >= '2015-10-01 00:00:00.000000' "\
             "AND o.o_entry_d < '2016-01-01 00:00:00.000000' "\
             "AND  n.n_nationkey = string_to_codepoint(c.c_state)[0] "\
            "GROUP BY c.c_id, c.c_last, c.c_city, c.c_phone, n.n_name "\
            "ORDER BY revenue DESC "\
            "LIMIT 20",

    "Q11": "SELECT s.s_i_id, SUM(s.s_order_cnt) as ordercount "\
           "FROM   nation n, supplier su, stock s "\
           "WHERE  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "\
             "AND  su.su_nationkey = n.n_nationkey "\
             "AND  n.n_name = 'Germany' "\
            "GROUP BY s.s_i_id "\
            "HAVING SUM(s.s_order_cnt) > "\
              "(SELECT VALUE SUM(s1.s_order_cnt) * 0.00005 "\
                "FROM nation n1, supplier su1, stock s1 "\
                "WHERE s1.s_w_id * s1.s_i_id MOD 10000 = su1.su_suppkey "\
                  "AND su1.su_nationkey = n1.n_nationkey "\
                  "AND n1.n_name = 'Germany')[0] "\
             "ORDER BY ordercount DESC",

    "Q12": "SELECT o.o_ol_cnt, "\
                   "SUM (case when o.o_carrier_id = 1 or o.o_carrier_id = 2 "\
                   "THEN 1 ELSE 0 END) AS high_line_COUNT, "\
                   "SUM (case when o.o_carrier_id <> 1 AND o.o_carrier_id <> 2 "\
                   "THEN 1 ELSE 0 END) AS low_line_COUNT "\
           "FROM orders o, o.o_orderline ol "\
           "WHERE  o.o_entry_d <= ol.ol_delivery_d "\
             "AND  ol.ol_delivery_d >= '2016-01-01 00:00:00.000000' AND  ol.ol_delivery_d < '2017-01-01 00:00:00.000000' "\
           "GROUP BY o.o_ol_cnt "\
           "ORDER BY o.o_ol_cnt",

    "Q13": "SELECT c_orders.c_count, COUNT(*) as custdist "\
           "FROM  (SELECT c.c_id, COUNT(o.o_id) as c_count "\
                   "FROM customer c LEFT OUTER JOIN orders o ON ( "\
                         "c.c_w_id = o.o_w_id "\
                         "AND c.c_d_id = o.o_d_id "\
                         "AND c.c_id = o.o_c_id "\
                         "AND o.o_carrier_id > 8) "\
                   "GROUP BY c.c_id) as c_orders "\
            "GROUP BY c_orders.c_count "\
            "ORDER BY custdist DESC, c_orders.c_count DESC",

    "Q14": "SELECT 100.00 * SUM(CASE WHEN i.i_data LIKE 'pr%' "\
                                "THEN ol.ol_amount ELSE 0 END) / "\
                                "(1+SUM(ol.ol_amount)) AS promo_revenue "\
           "FROM item i, orders o, o.o_orderline ol "\
           "WHERE ol.ol_i_id = i.i_id "\
             "AND ol.ol_delivery_d >= '2017-09-01 00:00:00.000000' AND ol.ol_delivery_d < '2017-10-01 00:00:00.000000'",

    "Q15": "WITH revenue AS ( "\
           "SELECT s.s_w_id * s.s_i_id MOD 10000 as supplier_no, SUM(ol.ol_amount) AS total_revenue "\
           "FROM   stock s, orders o, o.o_orderline ol "\
           "WHERE ol.ol_i_id = s.s_i_id "\
             "AND ol.ol_supply_w_id = s.s_w_id "\
             "AND ol.ol_delivery_d >= '2018-01-01 00:00:00.000000' AND ol.ol_delivery_d < '2018-04-01 00:00:00.000000' "\
           "GROUP BY s.s_w_id * s.s_i_id MOD 10000) "\
           "SELECT su.su_suppkey, su.su_name, su.su_address, su.su_phone, r.total_revenue "\
           "FROM revenue r,  supplier su "\
           "WHERE  su.su_suppkey = r.supplier_no "\
             "AND  r.total_revenue = (SELECT VALUE max(r1.total_revenue) FROM revenue r1)[0] "\
           "ORDER BY su.su_suppkey",

    "Q16": "SELECT i.i_name, SUBSTR1(i.i_data, 1, 3) AS brand, i.i_price, "\
           "COUNT(DISTINCT (s.s_w_id * s.s_i_id MOD 10000)) AS supplier_cnt "\
           "FROM stock s, item i "\
           "WHERE i.i_id = s.s_i_id "\
             "AND i.i_data not LIKE 'zz%' "\
             "AND (s.s_w_id * s.s_i_id MOD 10000 NOT IN "\
                        "(SELECT VALUE su.su_suppkey "\
                        "FROM supplier su "\
                        "WHERE su.su_comment LIKE '%Customer%Complaints%')) "\
            "GROUP BY i.i_name, SUBSTR1(i.i_data, 1, 3), i.i_price "\
            "ORDER BY supplier_cnt DESC",

    "Q17": "SELECT SUM(ol.ol_amount) / 2.0 AS AVG_yearly "\
           "FROM  (SELECT i.i_id, AVG(ol1.ol_quantity) AS a "\
                  "FROM   item i, orders o1, o1.o_orderline ol1 "\
                  "WHERE  i.i_data LIKE '%b' "\
                    "AND  ol1.ol_i_id = i.i_id "\
                  "GROUP BY i.i_id) t, orders o, o.o_orderline ol "\
           "WHERE ol.ol_i_id = t.i_id "\
             "AND ol.ol_quantity < t.a",

    "Q18": "SELECT c.c_last, c.c_id o_id, o.o_entry_d, o.o_ol_cnt, SUM(ol.ol_amount) "\
           "FROM orders o, o.o_orderline ol, customer c "\
           "WHERE  c.c_id = o.o_c_id AND  c.c_w_id = o.o_w_id AND  c.c_d_id = o.o_d_id "\
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, c.c_id, c.c_last, o.o_entry_d, o.o_ol_cnt "\
           "HAVING SUM(ol.ol_amount) > 200 "\
           "ORDER BY SUM(ol.ol_amount) DESC, o.o_entry_d "\
           "LIMIT 100",

    "Q19": "SELECT SUM(ol.ol_amount) AS revenue "\
           "FROM orders o, o.o_orderline ol, item i "\
           "WHERE  (( "\
                 "i.i_data LIKE '%h' "\
                 "AND ol.ol_quantity >= 7 AND ol.ol_quantity <= 17 "\
                 "AND i.i_price between 1 AND 5 "\
                 "AND o.o_w_id IN [37, 29, 70] "\
                 ") OR ( "\
                 "i.i_data LIKE '%t' "\
                 "AND ol.ol_quantity >= 16 AND ol.ol_quantity <= 26 "\
                 "AND i.i_price between 1 AND 10 "\
                 "AND o.o_w_id IN [78, 17, 6] "\
                 ") OR ( "\
                 "i.i_data LIKE '%m' "\
                 "AND ol.ol_quantity >= 24 AND ol.ol_quantity <= 34 "\
                 "AND i.i_price between 1 AND 15 "\
                 "AND  o.o_w_id IN [91, 95, 15] "\
                 ")) "\
              "AND ol.ol_i_id = i.i_id "\
              "AND i.i_price between 1 AND 15",

    "Q20": "SELECT su.su_name, su.su_address "\
           "FROM   supplier su, nation n "\
           "WHERE  su.su_suppkey IN "\
               "(SELECT VALUE s.s_i_id * s.s_w_id MOD 10000 "\
                "FROM   stock s, orders o, o.o_orderline ol "\
                "WHERE  s.s_i_id IN "\
                   "(SELECT VALUE i.i_id "\
                    "FROM item i "\
                    "WHERE i.i_data LIKE 'co%') "\
                  "AND ol.ol_i_id=s.s_i_id "\
                  "AND ol.ol_delivery_d >= '2016-01-01 12:00:00' "\
                  "AND ol.ol_delivery_d < '2017-01-01 12:00:00' "\
                "GROUP BY s.s_i_id, s.s_w_id, s.s_quantity "\
                "HAVING 20*s.s_quantity > SUM(ol.ol_quantity)) "\
             "AND su.su_nationkey = n.n_nationkey "\
             "AND n.n_name = 'Germany'  "\
             "ORDER BY su.su_name",

    "Q21": "SELECT z.su_name, count (*) AS numwait "\
           "FROM (SELECT x.su_name "\
                  "FROM (SELECT o1.o_id, o1.o_w_id, o1.o_d_id, ol1.ol_delivery_d,  "\
                                "n.n_nationkey, su.su_suppkey, s.s_w_id, s.s_i_id, su.su_name "\
                         "FROM nation n, supplier su, stock s, orders o1, o1.o_orderline ol1 "\
                         "WHERE  o1.o_w_id = s.s_w_id "\
                           "AND ol1.ol_i_id = s.s_i_id "\
                           "AND s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "\
                           "AND ol1.ol_delivery_d > date_add_str(o1.o_entry_d, 150, 'day') "\
                           "AND o1.o_entry_d between '2017-12-01 00:00:00' and '2017-12-31 00:00:00' "\
                           "AND su.su_nationkey = n.n_nationkey "\
                           "AND n.n_name = 'Peru') x "\
                          "LEFT OUTER JOIN "\
                          "(SELECT o2.o_id, o2.o_w_id, o2.o_d_id, ol2.ol_delivery_d "\
                            "FROM orders o2, o2.o_orderline ol2 "\
                            "WHERE o2.o_entry_d BETWEEN '2017-12-01 00:00:00' AND '2017-12-31 00:00:00') y "\
                        "ON y.o_id = x.o_id AND y.o_w_id = x.o_w_id AND y.o_d_id = x.o_d_id "\
                         "AND y.ol_delivery_d > x.ol_delivery_d "\
                  "GROUP BY x.o_w_id, x.o_d_id, x.o_id, x.n_nationkey, x.su_suppkey, x.s_w_id, x.s_i_id, x.su_name "\
                  "HAVING COUNT (y.o_id) = 0) z "\
           "GROUP BY z.su_name "\
           "LIMIT 100",

    "Q22": "SELECT SUBSTR1(c.c_state,1,1) AS country, COUNT(*) AS numcust, SUM(c.c_balance) AS totacctbal "\
           "FROM customer c "\
           "WHERE SUBSTR1(c.c_phone,1,1) IN ['1','2','3','4','5','6','7'] "\
             "AND c.c_balance > (SELECT VALUE AVG(c1.c_balance) "\
                                "FROM customer c1 "\
                                "WHERE c1.c_balance > 0.00 "\
                                  "AND SUBSTR1(c1.c_phone,1,1) IN ['1','2','3','4','5','6','7'])[0] "\
             "AND NOT EXISTS (SELECT VALUE 1 "\
                             "FROM orders o "\
                             "WHERE o.o_c_id = c.c_id AND o.o_w_id = c.c_w_id AND o.o_d_id = c.c_d_id "\
                               "AND o.o_entry_d BETWEEN '2013-12-01 00:00:00' AND '2013-12-31 00:00:00') "\
             "GROUP BY SUBSTR1(c.c_state,1,1) "\
             "ORDER BY SUBSTR1(c.c_state,1,1)"
}

CH2PP_QUERIES = {
    "Q01": "SELECT ol.ol_number ,"\
                   "SUM(ol.ol_quantity) as sum_qty ,"\
                   "SUM(ol.ol_amount) as sum_amount ,"\
                   "AVG(ol.ol_quantity) as avg_qty ,"\
                   "AVG(ol.ol_amount) as avg_amount ,"\
                   "COUNT(*) as COUNT_order "\
           "FROM     orders o, o.o_orderline ol "\
           "WHERE ol.ol_delivery_d /*+ skip-index */ > '2014-07-01 00:00:00' "\
           "GROUP BY ol.ol_number "\
           "ORDER BY ol.ol_number",

    "Q02": "SELECT su.su_suppkey, su.su_name, n.n_name, i.i_id, i.i_name, su.su_address, su.su_phone, su.su_comment "\
            "FROM (SELECT s1.s_i_id as m_i_id, MIN(s1.s_quantity) as m_s_quantity "\
                   "FROM stock s1, "\
                         "(SELECT su1.su_suppkey "\
                           "FROM supplier su1, (SELECT n1.n_nationkey from nation n1, region r1 "\
                                                "WHERE n1.n_regionkey=r1.r_regionkey AND r1.r_name LIKE 'Europ%') t1 "\
                           "WHERE su1.su_nationkey=t1.n_nationkey) t2 "\
                    "WHERE s1.s_w_id*s1.s_i_id MOD 10000 = t2.su_suppkey "\
                    "GROUP BY s1.s_i_id) m,  item i, stock s, supplier su, nation n, region r "\
             "WHERE i.i_id = s.s_i_id "\
               "AND s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "\
               "AND su.su_nationkey = n.n_nationkey "\
               "AND n.n_regionkey = r.r_regionkey "\
               "AND i.i_data LIKE '%b' "\
               "AND r.r_name LIKE 'Europ%' "\
               "AND i.i_id=m.m_i_id "\
               "AND s.s_quantity = m.m_s_quantity "\
              "ORDER BY n.n_name, su.su_name, i.i_id limit 100",

    "Q03": "WITH co as "\
           "(SELECT o.o_id, o.o_w_id, o.o_d_id, o.o_entry_d, o.o_orderline "\
            "FROM orders o, customer c, c.c_addresses ca "\
            "WHERE ca.c_address_kind = 'shipping' "\
            "AND ca.c_state LIKE 'a%' "\
            "AND c.c_id = o.o_c_id AND c.c_w_id = o.o_w_id AND c.c_d_id = o.o_d_id "\
              "AND o.o_entry_d /*+ skip-index */ < '2017-03-15 00:00:00.000000') "\
           "SELECT co.o_id, co.o_w_id, co.o_d_id, SUM(ol.ol_amount) as revenue, co.o_entry_d "\
           "FROM   co, co.o_orderline ol, neworder no "\
           "WHERE no.no_w_id = co.o_w_id AND no.no_d_id = co.o_d_id AND no.no_o_id = co.o_id "\
           "GROUP BY co.o_id, co.o_w_id, co.o_d_id, co.o_entry_d "\
           "ORDER BY revenue DESC, co.o_entry_d",

    "Q04": "SELECT o.o_ol_cnt, COUNT(*) as order_COUNT "\
           "FROM   orders o "\
           "WHERE  o.o_entry_d >= '2015-07-01 00:00:00.000000' AND o.o_entry_d < '2015-10-01 00:00:00.000000' "\
           "AND EXISTS (SELECT VALUE 1 "\
                        "FROM o.o_orderline ol "\
                        "WHERE ol.ol_delivery_d >= date_add_str(o.o_entry_d, 1, 'week')) "\
           "GROUP BY o.o_ol_cnt "\
           "ORDER BY o.o_ol_cnt ",

    "Q05": "SELECT cnros.n_name, ROUND(sum (cnros.ol_amount),2) as revenue "\
           "FROM (SELECT cnro.ol_amount, cnro.n_name, cnro.n_nationkey, s.s_w_id, s.s_i_id "\
                 "FROM stock s JOIN "\
                          "(SELECT o.o_w_id, ol.ol_amount, ol.ol_i_id, cnr.n_name, cnr.n_nationkey "\
                           "FROM orders o, o.o_orderline ol JOIN "\
                              "(SELECT c.c_id, c.c_w_id, c.c_d_id, nr.n_name, nr.n_nationkey "\
                               "FROM customer c, c.c_addresses ca JOIN "\
                                    "(SELECT n.n_nationkey, n.n_name "\
                                     "FROM nation n, region r "\
                                     "WHERE n.n_regionkey = r.r_regionkey AND r.r_name = 'Asia') nr "\
                                   "ON ca.c_address_kind = 'shipping' "\
                                    "AND string_to_codepoint(ca.c_state)[0] = nr.n_nationkey) cnr "\
                               "ON o.o_entry_d >= '2016-01-01 00:00:00.000000' AND o.o_entry_d < '2017-01-01 00:00:00.000000' "\
                               "AND cnr.c_id = o.o_c_id AND cnr.c_w_id = o.o_w_id AND cnr.c_d_id = o.o_d_id) cnro "\
                         "ON cnro.o_w_id = s.s_w_id AND cnro.ol_i_id = s.s_i_id) cnros JOIN supplier su "\
                       "ON cnros.s_w_id * cnros.s_i_id MOD 10000 = su.su_suppkey AND su.su_nationkey = cnros.n_nationkey "\
           "GROUP BY cnros.n_name "\
           "ORDER BY revenue DESC",

    "Q06": "SELECT SUM(ol.ol_amount) as revenue "\
           "FROM   orders o, o.o_orderline ol "\
           "WHERE  ol.ol_delivery_d >= '2016-01-01 00:00:00.000000' "\
             "AND  ol.ol_delivery_d < '2017-01-01 00:00:00.000000' "\
             "AND  ol.ol_amount > 600",

    "Q07": "SELECT su.su_nationkey as supp_nation, SUBSTR1(n1n2cools.c_state,1,1) as cust_nation, DATE_PART_STR(n1n2cools.o_entry_d, 'year') as l_year, ROUND(SUM(n1n2cools.ol_amount),2) as revenue "\
           "FROM "\
           "(select n1n2cool.c_state, n1n2cool.o_entry_d, n1n2cool.ol_amount, n1n2cool.n1key, s.s_w_id, s.s_i_id "\
             "FROM stock s JOIN "\
              "(SELECT o.o_entry_d, ol.ol_supply_w_id, ol.ol_i_id, n1n2c.c_state, ol.ol_amount, n1n2c.n1key "\
              "FROM orders o, o.o_orderline ol JOIN "\
                "(SELECT c.c_id, c.c_w_id, c.c_d_id, ca.c_state, n1n2.n1key "\
                  "FROM customer c, c.c_addresses ca JOIN "\
                      "(SELECT n1.n_nationkey n1key, n2.n_nationkey n2key "\
                        "FROM nation n1, nation n2 "\
                        "WHERE (n1.n_name = 'Germany' AND n2.n_name = 'Cambodia') OR (n1.n_name = 'Cambodia' AND n2.n_name = 'Germany') "\
                        ")n1n2 "\
               "ON ca.c_address_kind = 'shipping' "\
                "AND string_to_codepoint(ca.c_state)[0] = n1n2.n2key) n1n2c "\
              "ON n1n2c.c_id = o.o_c_id AND n1n2c.c_w_id = o.o_w_id AND n1n2c.c_d_id = o.o_d_id "\
              "AND ol.ol_delivery_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000') n1n2cool "\
           "ON n1n2cool.ol_supply_w_id = s.s_w_id AND n1n2cool.ol_i_id = s.s_i_id)  n1n2cools JOIN supplier su "\
           "ON n1n2cools.s_w_id * n1n2cools.s_i_id MOD 10000 = su.su_suppkey AND su.su_nationkey = n1n2cools.n1key "\
           "GROUP BY su.su_nationkey, SUBSTR1(n1n2cools.c_state,1,1), DATE_PART_STR(n1n2cools.o_entry_d, 'year') "\
           "ORDER BY su.su_nationkey, cust_nation, l_year",

    "Q08": "SELECT DATE_PART_STR(rn1coolis.o_entry_d, 'year') as l_year, "\
           "ROUND((SUM(case when sun2.n_name = 'Germany' then rn1coolis.ol_amount else 0 end) / SUM(rn1coolis.ol_amount)),2) as mkt_share "\
           "FROM "\
             "(SELECT rn1cooli.o_entry_d,  rn1cooli.ol_amount, s.s_w_id, s.s_i_id "\
              "FROM stock s JOIN "\
                 "(SELECT o.o_entry_d, ol.ol_i_id, ol.ol_amount, ol.ol_supply_w_id "\
                   "FROM orders o, o.o_orderline ol, item i JOIN "\
                     "(SELECT c.c_id, c.c_w_id, c.c_d_id "\
                       "FROM customer c, c.c_addresses ca JOIN "\
                         "(SELECT n1.n_nationkey "\
                           "FROM nation n1, region r "\
                           "WHERE n1.n_regionkey = r.r_regionkey AND r.r_name = 'Europe') nr "\
                         "ON ca.c_address_kind = 'shipping' "\
                          "AND nr.n_nationkey = string_to_codepoint(ca.c_state)[0]) cnr "\
                     "ON cnr.c_id = o.o_c_id AND cnr.c_w_id = o.o_w_id AND cnr.c_d_id = o.o_d_id "\
                     "AND i.i_data LIKE '%b' AND i.i_id = ol.ol_i_id "\
                     "AND ol.ol_i_id < 1000 "\
                     "AND o.o_entry_d /*+ skip-index */ BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000') rn1cooli "\
                "ON rn1cooli.ol_i_id = s.s_i_id "\
                "AND rn1cooli.ol_supply_w_id = s.s_w_id) rn1coolis JOIN "\
              "(SELECT su.su_suppkey, n2.n_name "\
               "FROM supplier su, nation n2 "\
               "WHERE su.su_nationkey = n2.n_nationkey) sun2 "\
             "ON rn1coolis.s_w_id * rn1coolis.s_i_id MOD 10000 = sun2.su_suppkey "\
             "GROUP BY DATE_PART_STR(rn1coolis.o_entry_d, 'year') "\
             "ORDER BY l_year",

    "Q09": "SELECT sun.n_name, DATE_PART_STR(oolis.o_entry_d, 'year') as l_year, round (SUM(oolis.ol_amount), 2) as SUM_profit "\
           "FROM "\
            "(SELECT s.s_w_id, s.s_i_id, ooli.o_entry_d, ooli.ol_amount "\
             "FROM stock s JOIN "\
                "(SELECT ol.ol_i_id, ol.ol_supply_w_id, ol.ol_amount, o.o_entry_d "\
                 "FROM orders o,  o.o_orderline ol, item i "\
                 "WHERE  i.i_data LIKE '%bb' and ol.ol_i_id = i.i_id) ooli "\
              "ON ooli.ol_i_id = s.s_i_id and ooli.ol_supply_w_id = s.s_w_id) oolis JOIN "\
             "(SELECT su.su_suppkey, n.n_name "\
              "FROM supplier su, nation n "\
              "WHERE su.su_nationkey = n.n_nationkey) sun "\
             "ON oolis.s_w_id * oolis.s_i_id MOD 10000 = sun.su_suppkey "\
            "GROUP BY sun.n_name, DATE_PART_STR(oolis.o_entry_d, 'year') "\
            "ORDER BY sun.n_name, l_year DESC",

    "Q10": "SELECT c.c_id, c.c_name.c_last, SUM(ol.ol_amount) as revenue, ca.c_city, cp.c_phone_number, n.n_name "\
           "FROM nation n, customer c, c.c_addresses ca, c.c_phones cp, orders o, o.o_orderline ol "\
           "WHERE  c.c_id = o.o_c_id "\
             "AND  c.c_w_id = o.o_w_id "\
             "AND  c.c_d_id = o.o_d_id "\
             "AND  o.o_entry_d >= '2015-10-01 00:00:00.000000' "\
             "AND o.o_entry_d < '2016-01-01 00:00:00.000000' "\
             "AND  ca.c_address_kind = 'shipping' "\
	     "AND  cp.c_phone_kind = 'contact' "\
             "AND  n.n_nationkey = string_to_codepoint(ca.c_state)[0] "\
            "GROUP BY c.c_id, c.c_name.c_last, ca.c_city, cp.c_phone_number, n.n_name "\
            "ORDER BY revenue DESC "\
            "LIMIT 20",

    "Q11": "SELECT s.s_i_id, SUM(s.s_order_cnt) as ordercount "\
           "FROM   nation n, supplier su, stock s "\
           "WHERE  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "\
             "AND  su.su_nationkey = n.n_nationkey "\
             "AND  n.n_name = 'Germany' "\
            "GROUP BY s.s_i_id "\
            "HAVING SUM(s.s_order_cnt) > "\
              "(SELECT VALUE SUM(s1.s_order_cnt) * 0.00005 "\
                "FROM nation n1, supplier su1, stock s1 "\
                "WHERE s1.s_w_id * s1.s_i_id MOD 10000 = su1.su_suppkey "\
                  "AND su1.su_nationkey = n1.n_nationkey "\
                  "AND n1.n_name = 'Germany')[0] "\
             "ORDER BY ordercount DESC",

    "Q12": "SELECT o.o_ol_cnt, "\
                   "SUM (case when o.o_carrier_id = 1 or o.o_carrier_id = 2 "\
                   "THEN 1 ELSE 0 END) AS high_line_COUNT, "\
                   "SUM (case when o.o_carrier_id <> 1 AND o.o_carrier_id <> 2 "\
                   "THEN 1 ELSE 0 END) AS low_line_COUNT "\
           "FROM orders o, o.o_orderline ol "\
           "WHERE  o.o_entry_d <= ol.ol_delivery_d "\
             "AND  ol.ol_delivery_d >= '2016-01-01 00:00:00.000000' AND  ol.ol_delivery_d < '2017-01-01 00:00:00.000000' "\
           "GROUP BY o.o_ol_cnt "\
           "ORDER BY o.o_ol_cnt",

    "Q13": "SELECT c_orders.c_count, COUNT(*) as custdist "\
           "FROM  (SELECT c.c_id, COUNT(o.o_id) as c_count "\
                   "FROM customer c LEFT OUTER JOIN orders o ON ( "\
                         "c.c_w_id = o.o_w_id "\
                         "AND c.c_d_id = o.o_d_id "\
                         "AND c.c_id = o.o_c_id "\
                         "AND o.o_carrier_id > 8) "\
                   "GROUP BY c.c_id) as c_orders "\
            "GROUP BY c_orders.c_count "\
            "ORDER BY custdist DESC, c_orders.c_count DESC",

    "Q14": "SELECT 100.00 * SUM(CASE WHEN i.i_data LIKE 'pr%' "\
                                "THEN ol.ol_amount ELSE 0 END) / "\
                                "(1+SUM(ol.ol_amount)) AS promo_revenue "\
           "FROM item i, orders o, o.o_orderline ol "\
           "WHERE ol.ol_i_id = i.i_id "\
             "AND ol.ol_delivery_d >= '2017-09-01 00:00:00.000000' AND ol.ol_delivery_d < '2017-10-01 00:00:00.000000'",

    "Q15": "WITH revenue AS ( "\
           "SELECT s.s_w_id * s.s_i_id MOD 10000 as supplier_no, SUM(ol.ol_amount) AS total_revenue "\
           "FROM   stock s, orders o, o.o_orderline ol "\
           "WHERE ol.ol_i_id = s.s_i_id "\
             "AND ol.ol_supply_w_id = s.s_w_id "\
             "AND ol.ol_delivery_d >= '2018-01-01 00:00:00.000000' AND ol.ol_delivery_d < '2018-04-01 00:00:00.000000' "\
           "GROUP BY s.s_w_id * s.s_i_id MOD 10000) "\
           "SELECT su.su_suppkey, su.su_name, su.su_address, su.su_phone, r.total_revenue "\
           "FROM revenue r,  supplier su "\
           "WHERE  su.su_suppkey = r.supplier_no "\
             "AND  r.total_revenue = (SELECT VALUE max(r1.total_revenue) FROM revenue r1)[0] "\
           "ORDER BY su.su_suppkey",

    "Q16": "SELECT i.i_name, SUBSTR1(i.i_data, 1, 3) AS brand, i.i_price, "\
           "COUNT(DISTINCT (s.s_w_id * s.s_i_id MOD 10000)) AS supplier_cnt "\
           "FROM stock s, item i "\
           "WHERE i.i_id = s.s_i_id "\
             "AND i.i_data not LIKE 'zz%' "\
             "AND (s.s_w_id * s.s_i_id MOD 10000 NOT IN "\
                        "(SELECT VALUE su.su_suppkey "\
                        "FROM supplier su "\
                        "WHERE su.su_comment LIKE '%Customer%Complaints%')) "\
            "GROUP BY i.i_name, SUBSTR1(i.i_data, 1, 3), i.i_price "\
            "ORDER BY supplier_cnt DESC",

    "Q17": "SELECT SUM(ol.ol_amount) / 2.0 AS AVG_yearly "\
           "FROM  (SELECT i.i_id, AVG(ol1.ol_quantity) AS a "\
                  "FROM   item i, orders o1, o1.o_orderline ol1 "\
                  "WHERE  i.i_data LIKE '%b' "\
                    "AND  ol1.ol_i_id = i.i_id "\
                  "GROUP BY i.i_id) t, orders o, o.o_orderline ol "\
           "WHERE ol.ol_i_id = t.i_id "\
             "AND ol.ol_quantity < t.a",

    "Q18": "SELECT c.c_name.c_last, c.c_id o_id, o.o_entry_d, o.o_ol_cnt, SUM(ol.ol_amount) "\
           "FROM orders o, o.o_orderline ol, customer c "\
           "WHERE  c.c_id = o.o_c_id AND  c.c_w_id = o.o_w_id AND  c.c_d_id = o.o_d_id "\
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, c.c_id, c.c_name.c_last, o.o_entry_d, o.o_ol_cnt "\
           "HAVING SUM(ol.ol_amount) > 200 "\
           "ORDER BY SUM(ol.ol_amount) DESC, o.o_entry_d "\
           "LIMIT 100",

    "Q19": "SELECT SUM(ol.ol_amount) AS revenue "\
           "FROM orders o, o.o_orderline ol, item i "\
           "WHERE  (( "\
                 "i.i_data LIKE '%h' "\
                 "AND ol.ol_quantity >= 7 AND ol.ol_quantity <= 17 "\
                 "AND i.i_price between 1 AND 5 "\
                 "AND o.o_w_id IN [37, 29, 70] "\
                 ") OR ( "\
                 "i.i_data LIKE '%t' "\
                 "AND ol.ol_quantity >= 16 AND ol.ol_quantity <= 26 "\
                 "AND i.i_price between 1 AND 10 "\
                 "AND o.o_w_id IN [78, 17, 6] "\
                 ") OR ( "\
                 "i.i_data LIKE '%m' "\
                 "AND ol.ol_quantity >= 24 AND ol.ol_quantity <= 34 "\
                 "AND i.i_price between 1 AND 15 "\
                 "AND  o.o_w_id IN [91, 95, 15] "\
                 ")) "\
              "AND ol.ol_i_id = i.i_id "\
              "AND i.i_price between 1 AND 15",

    "Q20": "SELECT su.su_name, su.su_address "\
           "FROM   supplier su, nation n "\
           "WHERE  su.su_suppkey IN "\
               "(SELECT VALUE s.s_i_id * s.s_w_id MOD 10000 "\
                "FROM   stock s, orders o, o.o_orderline ol "\
                "WHERE  s.s_i_id IN "\
                   "(SELECT VALUE i.i_id "\
                    "FROM item i "\
                    "WHERE i.i_data LIKE 'co%') "\
                  "AND ol.ol_i_id=s.s_i_id "\
                  "AND ol.ol_delivery_d >= '2016-01-01 12:00:00' "\
                  "AND ol.ol_delivery_d < '2017-01-01 12:00:00' "\
                "GROUP BY s.s_i_id, s.s_w_id, s.s_quantity "\
                "HAVING 20*s.s_quantity > SUM(ol.ol_quantity)) "\
             "AND su.su_nationkey = n.n_nationkey "\
             "AND n.n_name = 'Germany'  "\
             "ORDER BY su.su_name",

    "Q21": "SELECT z.su_name, count (*) AS numwait "\
           "FROM (SELECT x.su_name "\
                  "FROM (SELECT o1.o_id, o1.o_w_id, o1.o_d_id, ol1.ol_delivery_d,  "\
                                "n.n_nationkey, su.su_suppkey, s.s_w_id, s.s_i_id, su.su_name "\
                         "FROM nation n, supplier su, stock s, orders o1, o1.o_orderline ol1 "\
                         "WHERE  o1.o_w_id = s.s_w_id "\
                           "AND ol1.ol_i_id = s.s_i_id "\
                           "AND s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "\
                           "AND ol1.ol_delivery_d > date_add_str(o1.o_entry_d, 150, 'day') "\
                           "AND o1.o_entry_d between '2017-12-01 00:00:00' and '2017-12-31 00:00:00' "\
                           "AND su.su_nationkey = n.n_nationkey "\
                           "AND n.n_name = 'Peru') x "\
                          "LEFT OUTER JOIN "\
                          "(SELECT o2.o_id, o2.o_w_id, o2.o_d_id, ol2.ol_delivery_d "\
                            "FROM orders o2, o2.o_orderline ol2 "\
                            "WHERE o2.o_entry_d BETWEEN '2017-12-01 00:00:00' AND '2017-12-31 00:00:00') y "\
                        "ON y.o_id = x.o_id AND y.o_w_id = x.o_w_id AND y.o_d_id = x.o_d_id "\
                         "AND y.ol_delivery_d > x.ol_delivery_d "\
                  "GROUP BY x.o_w_id, x.o_d_id, x.o_id, x.n_nationkey, x.su_suppkey, x.s_w_id, x.s_i_id, x.su_name "\
                  "HAVING COUNT (y.o_id) = 0) z "\
           "GROUP BY z.su_name "\
           "LIMIT 100",

    "Q22": "SELECT SUBSTR1(ca.c_state,1,1) AS country, COUNT(*) AS numcust, SUM(c.c_balance) AS totacctbal "\
           "FROM customer c, c.c_addresses ca, c.c_phones cp "\
           "WHERE SUBSTR1(cp.c_phone_number,1,1) IN ['1','2','3','4','5','6','7'] "\
             "AND  ca.c_address_kind = 'shipping' "\
             "AND  cp.c_phone_kind = 'contact' "\
             "AND c.c_balance > (SELECT VALUE AVG(c1.c_balance) "\
                                "FROM customer c1, c1.c_phones cp1 "\
                                "WHERE c1.c_balance > 0.00 "\
                                  "AND  cp1.c_phone_kind = 'contact' "\
                                  "AND SUBSTR1(cp1.c_phone_number,1,1) IN ['1','2','3','4','5','6','7'])[0] "\
             "AND NOT EXISTS (SELECT VALUE 1 "\
                             "FROM orders o "\
                             "WHERE o.o_c_id = c.c_id AND o.o_w_id = c.c_w_id AND o.o_d_id = c.c_d_id "\
                               "AND o.o_entry_d BETWEEN '2013-12-01 00:00:00' AND '2013-12-31 00:00:00') "\
             "GROUP BY SUBSTR1(ca.c_state,1,1) "\
             "ORDER BY SUBSTR1(ca.c_state,1,1)"
}

CH2_QUERIES_NON_OPTIMIZED = {
    # Q01: This query reports the total amount and quantity of all shipped orderlines
    # given by a specific time period. Additionally it informs about the average
    # amount and quantity plus the total count of all these orderlines ordered
    # by the individual orderline number.
    "Q01": "SELECT ol.ol_number, "
                  "SUM(ol.ol_quantity) AS sum_qty, "
                  "SUM(ol.ol_amount) AS sum_amount, "
                  "AVG(ol.ol_quantity) AS avg_qty, "
                  "AVG(ol.ol_amount) AS avg_amount, "
                  "COUNT(*) AS count_order "
           "FROM   orders o, o.o_orderline ol "
           "WHERE  ol.ol_delivery_d  > '2014-07-01 00:00:00' "
           "GROUP BY ol.ol_number "
           "ORDER BY ol.ol_number;",

    # Q02: Query for listing suppliers and their distributed items having the lowest
    # stock level for a certain item and certain region.
    "Q02": "SELECT su.su_suppkey, su.su_name, n.n_name, i.i_id, i.i_name, su.su_address, su.su_phone, su.su_comment "
           "FROM   item i,  supplier su, stock s, nation n, region r, "
                   "(SELECT s1.s_i_id as m_i_id, MIN(s1.s_quantity) AS m_s_quantity "
                    "FROM stock s1, supplier su1, nation n1, region r1 "
                    "WHERE s1.s_w_id*s1.s_i_id MOD 10000 = su1.su_suppkey "
                      "AND su1.su_nationkey=n1.n_nationkey "
                      "AND n1.n_regionkey=r1.r_regionkey "
                      "AND r1.r_name LIKE 'Europ%' "
                    "GROUP BY s1.s_i_id) m "
           "WHERE i.i_id = s.s_i_id "
             "AND s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND su.su_nationkey = n.n_nationkey "
             "AND n.n_regionkey = r.r_regionkey "
             "AND i.i_data LIKE '%b' "
             "AND r.r_name LIKE 'Europ%' "
             "AND i.i_id=m.m_i_id "
             "AND s.s_quantity = m.m_s_quantity "
           "ORDER BY n.n_name, su.su_name, i.i_id limit 100;",

    # Q03: Unshipped orders with the highest price amount for a customer will be
    # listed within a given state and with orders newer than a specific timestamp.
    # This list will be sorted by the descending amount.
    "Q03": "SELECT o.o_id, o.o_w_id, o.o_d_id, SUM(ol.ol_amount) AS revenue, o.o_entry_d "
           "FROM   customer c, neworder no, orders o, o.o_orderline ol "
           "WHERE  c.c_state LIKE 'a%' "
             "AND c.c_id = o.o_c_id "
             "AND c.c_w_id = o.o_w_id "
             "AND c.c_d_id = o.o_d_id "
             "AND no.no_w_id = o.o_w_id "
             "AND no.no_d_id = o.o_d_id "
             "AND no.no_o_id = o.o_id "
             "AND o.o_entry_d < '2017-03-15 00:00:00.000000' "
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, o.o_entry_d "
           "ORDER BY revenue DESC, o.o_entry_d;",

    # Q04: This query is listing all orders with orderlines or just parts of them
    # shipped after the entry date of their booking.
    "Q04": "SELECT o.o_ol_cnt, COUNT(*) as order_count "
           "FROM   orders o "
           "WHERE  o.o_entry_d >= '2015-07-01 00:00:00.000000' AND o.o_entry_d < '2015-10-01 00:00:00.000000' "
           "AND EXISTS (SELECT VALUE 1 "
                       "FROM o.o_orderline ol "
                       "WHERE ol.ol_delivery_d >= DATE_ADD_STR(o.o_entry_d, 1, 'week')) "
           "GROUP BY o.o_ol_cnt "
           "ORDER BY o.o_ol_cnt;",

    # Q05: Query result for getting information about achieved revenues of nations
    # within a given region. All nations are sorted by the total amount of revenue
    # gained since the given date.
    "Q05": "SELECT n.n_name, "
                  "ROUND(SUM(ol.ol_amount), 2) AS revenue "
           "FROM   customer c, orders o, o.o_orderline ol, stock s, supplier su, nation n, region r "
           "WHERE  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  o.o_w_id = s.s_w_id "
             "AND  ol.ol_i_id = s.s_i_id "
             "AND  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND  string_to_codepoint(c.c_state)[0] = su.su_nationkey "
             "AND  string_to_codepoint(c.c_state)[0] = n.n_nationkey "
             "AND  su.su_nationkey = n.n_nationkey "
             "AND  n.n_regionkey = r.r_regionkey "
             "AND  r.r_name = 'Asia' "
             "AND  o.o_entry_d >= '2016-01-01 00:00:00.000000' AND o.o_entry_d < '2017-01-01 00:00:00.000000' "
           "GROUP BY n.n_name "
           "ORDER BY revenue DESC;",

    # Q06: Query lists the total amount of archived revenue from orderlines which
    # were delivered in a specific period and a certain quantity.
    "Q06": "SELECT SUM(ol.ol_amount) as revenue "
           "FROM   orders o, o.o_orderline ol "
           "WHERE  ol.ol_delivery_d >= '2016-01-01 00:00:00.000000' "
             "AND  ol.ol_delivery_d < '2017-01-01 00:00:00.000000' "
             "AND  ol.ol_amount > 600;",

    # Q07: Query for showing the bi-directional trade volume between two given
    # nations sorted by their names and the considered years.
    "Q07": "SELECT su.su_nationkey as supp_nation, "
                  "SUBSTR1(c.c_state,1,1) as cust_nation, "
                  "DATE_PART_STR(o.o_entry_d, 'year') AS l_year, "
                  "ROUND(SUM(ol.ol_amount),2) AS revenue "
           "FROM   supplier su, stock s, orders o, o.o_orderline ol, customer c, nation n1, nation n2 "
           "WHERE  ol.ol_supply_w_id = s.s_w_id "
             "AND  ol.ol_i_id = s.s_i_id "
             "AND  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  su.su_nationkey = n1.n_nationkey "
             "AND  string_to_codepoint(c.c_state)[0] = n2.n_nationkey "
             "AND  ("
                    "(n1.n_name = 'Germany' and n2.n_name = 'Cambodia') "
                      "OR "
                    "(n1.n_name = 'Cambodia' and n2.n_name = 'Germany') "
                  ") "
             "AND  ol.ol_delivery_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000' "
           "GROUP BY su.su_nationkey, SUBSTR1(c.c_state,1,1), DATE_PART_STR(o.o_entry_d, 'year') "
           "ORDER BY su.su_nationkey, cust_nation, l_year;",

    # Q08: This query lists the market share of a given nation for customers from
    # a certain region in which kinds of items are "produced".
    "Q08": "SELECT DATE_PART_STR(o.o_entry_d, 'year') AS l_year, "
                  "ROUND((SUM(CASE WHEN n2.n_name = 'Germany' THEN ol.ol_amount ELSE 0 END) / SUM(ol.ol_amount)),2) AS mkt_share "
           "FROM   item i, supplier su, stock s, orders o, o.o_orderline ol, customer c, nation n1, nation n2, region r "
           "WHERE  i.i_id = s.s_i_id "
             "AND  ol.ol_i_id = s.s_i_id "
             "AND  ol.ol_supply_w_id = s.s_w_id "
             "AND  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  n1.n_nationkey = string_to_codepoint(c.c_state)[0] "
             "AND  n1.n_regionkey = r.r_regionkey "
             "AND  ol.ol_i_id < 1000 "
             "AND  r.r_name = 'Europe' "
             "AND  su.su_nationkey = n2.n_nationkey "
             "AND  o.o_entry_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000' "
             "AND  i.i_data LIKE '%b' "
             "AND  i.i_id = ol.ol_i_id "
           "GROUP BY DATE_PART_STR(o.o_entry_d, 'year') "
           "ORDER BY l_year;",

    # Q09: This query describes how much profit has been made on a selection of
    # items for each nation and each year. The result list will be sorted by the
    # name of the nation and the financial year.
    "Q09": "SELECT   n.n_name, DATE_PART_STR(o.o_entry_d, 'year') AS l_year, SUM(ol.ol_amount) AS sum_profit "
           "FROM     item i, stock s, supplier su, orders o, o.o_orderline ol, nation n "
           "WHERE    ol.ol_i_id = s.s_i_id "
             "AND    ol.ol_supply_w_id = s.s_w_id "
             "AND    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND    ol.ol_i_id = i.i_id "
             "AND    su.su_nationkey = n.n_nationkey "
             "AND    i.i_data like '%bb' "
           "GROUP BY n.n_name, DATE_PART_STR(o.o_entry_d, 'year') "
           "ORDER BY n.n_name, l_year DESC;",
    # Q10: Query for analyzing the expenses of all customers listing their living
    # country, some detail of them and the amount of money which they have used
    # to take their orders since a specific date. The whole list is sorted by the
    # amount of the customers’ orders.
    "Q10": "SELECT c.c_id, c.c_last, SUM(ol.ol_amount) AS revenue, c.c_city, c.c_phone, n.n_name "
           "FROM customer c, orders o, o.o_orderline ol, nation n  "
           "WHERE  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  o.o_entry_d >= '2015-10-01 00:00:00.000000' "
             "AND  o.o_entry_d < '2016-01-01 00:00:00.000000' "
             "AND  n.n_nationkey = string_to_codepoint(c.c_state)[0] "
           "GROUP BY c.c_id, c.c_last, c.c_city, c.c_phone, n.n_name "
           "ORDER BY revenue DESC "
           "LIMIT 20;",

    # Q11: Most important items (items which are often involved in orders and
    # therefore often bought by customers) supplied by supplier of a given nation.
    "Q11": "SELECT s.s_i_id, SUM(s.s_order_cnt) as ordercount "
           "FROM   stock s,  supplier su, nation n  "
           "WHERE  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND  su.su_nationkey = n.n_nationkey "
             "AND  n.n_name = 'Germany' "
           "GROUP BY s.s_i_id "
           "HAVING SUM(s.s_order_cnt) > "
                    "(SELECT VALUE SUM(s1.s_order_cnt) * 0.00005 "
                     "FROM stock s1,  supplier su1, nation n1 "
                     "WHERE s1.s_w_id * s1.s_i_id MOD 10000 = su1.su_suppkey "
                       "AND su1.su_nationkey = n1.n_nationkey "
                       "AND n1.n_name = 'Germany')[0] "
           "ORDER BY ordercount DESC;",

    # Q12: This query counts the amount of orders grouped by the number of
    # orderlines in each order attending the number of orders which are shipped
    # with a higher or lower order priority.
    "Q12": "SELECT o.o_ol_cnt, "
                  "SUM (CASE WHEN o.o_carrier_id = 1 OR o.o_carrier_id = 2 "
                       "THEN 1 ELSE 0 END) AS high_line_COUNT, "
                  "SUM (CASE WHEN o.o_carrier_id <> 1 AND o.o_carrier_id <> 2 "
                       "THEN 1 ELSE 0 END) AS low_line_COUNT "
           "FROM orders o, o.o_orderline ol "
           "WHERE  o.o_entry_d <= ol.ol_delivery_d "
             "AND  ol.ol_delivery_d >= '2016-01-01 00:00:00.000000' AND  ol.ol_delivery_d < '2017-01-01 00:00:00.000000' "
           "GROUP BY o.o_ol_cnt "
           "ORDER BY o.o_ol_cnt;",

    # Q13: The query lists the number of customers grouped and sorted by the size
    # of orders they made. The result set of the relation between customers and
    # the size of their orders is sorted by the size of orders and counts how
    # many customers have dealt the same way.
    "Q13": "SELECT c_orders.c_count, COUNT(*) AS custdist "
           "FROM  (SELECT c.c_id, COUNT(o.o_id) AS c_count "
                  "FROM customer c LEFT OUTER JOIN orders o "
                              "ON (c.c_w_id = o.o_w_id "
                             "AND c.c_d_id = o.o_d_id "
                             "AND c.c_id = o.o_c_id "
                             "AND o.o_carrier_id > 8) "
                  "GROUP BY c.c_id) as c_orders "
           "GROUP BY c_orders.c_count "
           "ORDER BY custdist DESC, c_orders.c_count DESC;",

    # Q14: The query result represents the percentage of the revenue in a period
    # of time which has been realized from promotional campaigns.
    "Q14": "SELECT 100.00 * SUM(CASE WHEN i.i_data LIKE 'pr%' "
                               "THEN ol.ol_amount ELSE 0 END) / "
                               "(1+SUM(ol.ol_amount)) AS promo_revenue "
           "FROM orders o, o.o_orderline ol, item i "
           "WHERE ol.ol_i_id = i.i_id "
             "AND ol.ol_delivery_d >= '2017-09-01 00:00:00.000000' AND ol.ol_delivery_d < '2017-10-01 00:00:00.000000';",

    # Q15: This query finds the top supplier or suppliers who contributed the
    # most to the overall revenue for items shipped during a given period of time.
    "Q15": "WITH revenue AS ( "
                "SELECT s.s_w_id * s.s_i_id MOD 10000 as supplier_no, SUM(ol.ol_amount) AS total_revenue "
                "FROM   orders o, o.o_orderline ol, stock s "
                "WHERE ol.ol_i_id = s.s_i_id "
                  "AND ol.ol_supply_w_id = s.s_w_id "
                  "AND ol.ol_delivery_d >= '2018-01-01 00:00:00.000000' AND ol.ol_delivery_d < '2018-04-01 00:00:00.000000' "
                "GROUP BY s.s_w_id * s.s_i_id MOD 10000) "
           "SELECT su.su_suppkey, su.su_name, su.su_address, su.su_phone, r.total_revenue "
           "FROM   supplier su, revenue r "
           "WHERE  su.su_suppkey = r.supplier_no "
             "AND  r.total_revenue = (SELECT VALUE max(r1.total_revenue) FROM revenue r1)[0] "
           "ORDER BY su.su_suppkey;",

    # Q16: This query finds out how many suppliers are able to supply items with
    # given attributes sorted in descending order of them. The result is grouped
    # by the identifier of the item.
    "Q16": "SELECT i.i_name, SUBSTR1(i.i_data, 1, 3) AS brand, i.i_price, "
                  "COUNT(DISTINCT (s.s_w_id * s.s_i_id MOD 10000)) AS supplier_cnt "
           "FROM stock s, item i "
           "WHERE i.i_id = s.s_i_id "
             "AND i.i_data not LIKE 'zz%' "
             "AND (s.s_w_id * s.s_i_id MOD 10000 NOT IN "
                                         "(SELECT VALUE su.su_suppkey "
                                          "FROM supplier su "
                                          "WHERE su.su_comment LIKE '%Customer%Complaints%')) "
           "GROUP BY i.i_name, SUBSTR1(i.i_data, 1, 3), i.i_price "
           "ORDER BY supplier_cnt DESC;",

    # Q17: The query determines the yearly loss in revenue if orders just with a
    # quantity of more than the average quantity of all orders in the system
    # would be taken and shipped to customers.
    "Q17": "SELECT SUM(ol.ol_amount) / 2.0 AS avg_yearly "
           "FROM  orders o, o.o_orderline ol, (SELECT i.i_id, AVG(ol1.ol_quantity) AS a "
                                              "FROM   item i, orders o1, o1.o_orderline ol1 "
                                              "WHERE  i.i_data LIKE '%b' "
                                                "AND  ol1.ol_i_id = i.i_id "
                                              "GROUP BY i.i_id) t "
           "WHERE ol.ol_i_id = t.i_id "
             "AND ol.ol_quantity < t.a;",

    # Q18: Query 18 is ranking all customers who have ordered for more than a
    # specific amount of money.
    "Q18": "SELECT c.c_last, c.c_id o_id, o.o_entry_d, o.o_ol_cnt, SUM(ol.ol_amount) "
           "FROM customer c, orders o, o.o_orderline ol "
           "WHERE  c.c_id = o.o_c_id AND  c.c_w_id = o.o_w_id AND  c.c_d_id = o.o_d_id "
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, c.c_id, c.c_last, o.o_entry_d, o.o_ol_cnt "
           "HAVING SUM(ol.ol_amount) > 200 "
           "ORDER BY SUM(ol.ol_amount) DESC, o.o_entry_d "
           "LIMIT 100;",

    # Q19: The query is for reporting the revenue achieved by some specific
    # attributes, as the price, the detailed information of the item and the
    # quantity of the ordered amount of them.
    "Q19": "SELECT SUM(ol.ol_amount) AS revenue "
           "FROM orders o, o.o_orderline ol, item i "
           "WHERE  (( "
                    "i.i_data LIKE '%h' "
                    "AND ol.ol_quantity >= 7 AND ol.ol_quantity <= 17 "
                    "AND i.i_price between 1 AND 5 "
                    "AND o.o_w_id IN [37, 29, 70] "
                   ") OR ( "
                    "i.i_data LIKE '%t' "
                    "AND ol.ol_quantity >= 16 AND ol.ol_quantity <= 26 "
                    "AND i.i_price between 1 AND 10 "
                    "AND o.o_w_id IN [78, 17, 6] "
                   ") OR ( "
                    "i.i_data LIKE '%m' "
                    "AND ol.ol_quantity >= 24 AND ol.ol_quantity <= 34 "
                    "AND i.i_price between 1 AND 15 "
                    "AND  o.o_w_id IN [91, 95, 15] "
                    ")) "
                  "AND ol.ol_i_id = i.i_id "
                  "AND i.i_price between 1 AND 15;",

    # Q20: Suppliers in a particular nation having selected parts that may be
    # candidates for a promotional offer if the quantity of these items is more
    # than 50 percent of the total quantity which has been ordered since a certain date.
    "Q20": "SELECT su.su_name, su.su_address "
           "FROM   supplier su, nation n "
           "WHERE  su.su_suppkey IN "
                         "(SELECT VALUE s.s_i_id * s.s_w_id MOD 10000 "
                          "FROM   stock s, orders o, o.o_orderline ol "
                          "WHERE  s.s_i_id IN "
                              "(SELECT VALUE i.i_id "
                               "FROM item i "
                              "WHERE i.i_data LIKE 'co%') "
                            "AND ol.ol_i_id=s.s_i_id "
                            "AND ol.ol_delivery_d >= '2016-01-01 12:00:00' "
                            "AND ol.ol_delivery_d < '2017-01-01 12:00:00' "
                           "GROUP BY s.s_i_id, s.s_w_id, s.s_quantity "
                           "HAVING 20*s.s_quantity > SUM(ol.ol_quantity)) "
             "AND su.su_nationkey = n.n_nationkey "
             "AND n.n_name = 'Germany' "
           "ORDER BY su.su_name;",

    # Q21: Query 21 determines the suppliers which have shipped some required
    # items of an order not in a timely manner for a given nation.
    "Q21": "SELECT z.su_name, COUNT (*) AS numwait "
            "FROM (SELECT x.su_name "
                  "FROM (SELECT o1.o_id, o1.o_w_id, o1.o_d_id, ol1.ol_delivery_d, "
                                           "n.n_nationkey, su.su_suppkey, s.s_w_id, s.s_i_id, su.su_name "
                        "FROM nation n, supplier su, stock s, orders o1, o1.o_orderline ol1 "
                        "WHERE o1.o_w_id = s.s_w_id "
                          "AND ol1.ol_i_id = s.s_i_id "
                          "AND s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
                          "AND ol1.ol_delivery_d > date_add_str(o1.o_entry_d, 150, 'day') "
                          "AND o1.o_entry_d between '2017-12-01 00:00:00' and '2017-12-31 00:00:00' "
                          "AND su.su_nationkey = n.n_nationkey "
                          "AND n.n_name = 'Peru') x "
                       "LEFT OUTER JOIN "
                       "(SELECT o2.o_id, o2.o_w_id, o2.o_d_id, ol2.ol_delivery_d "
                        "FROM orders o2, o2.o_orderline ol2 "
                        "WHERE o2.o_entry_d BETWEEN '2017-12-01 00:00:00' AND '2017-12-31 00:00:00') y "
                   "ON y.o_id = x.o_id AND y.o_w_id = x.o_w_id AND y.o_d_id = x.o_d_id "
                  "AND y.ol_delivery_d > x.ol_delivery_d "
                  "GROUP BY x.o_w_id, x.o_d_id, x.o_id, x.n_nationkey, x.su_suppkey, x.s_w_id, x.s_i_id, x.su_name "
                  "HAVING COUNT (y.o_id) = 0) z "
           "GROUP BY z.su_name "
           "LIMIT 100;",

    # Q22: This query lists how many customers within a specific range of country
    # codes have not bought anything for the whole period of time and who have a
    # greater than average balance on their account. The county code is represented
    # by the first two characters of the phone number.
    "Q22": "SELECT SUBSTR1(c.c_state,1,1) AS country, COUNT(*) AS numcust, SUM(c.c_balance) AS totacctbal "
           "FROM customer c "
           "WHERE SUBSTR1(c.c_phone,1,1) IN ['1','2','3','4','5','6','7'] "
             "AND c.c_balance > (SELECT VALUE AVG(c1.c_balance) "
                                "FROM customer c1 "
                                "WHERE c1.c_balance > 0.00 "
                                  "AND SUBSTR1(c1.c_phone,1,1) IN ['1','2','3','4','5','6','7'])[0] "
             "AND NOT EXISTS (SELECT VALUE 1 "
                             "FROM orders o "
                             "WHERE o.o_c_id = c.c_id AND o.o_w_id = c.c_w_id AND o.o_d_id = c.c_d_id "
                               "AND o.o_entry_d BETWEEN '2013-12-01 00:00:00' AND '2013-12-31 00:00:00') "
           "GROUP BY SUBSTR1(c.c_state,1,1) "
           "ORDER BY SUBSTR1(c.c_state,1,1);"
}

CH2PP_QUERIES_NON_OPTIMIZED = {
    # Q01: This query reports the total amount and quantity of all shipped orderlines
    # given by a specific time period. Additionally it informs about the average
    # amount and quantity plus the total count of all these orderlines ordered
    # by the individual orderline number.
    "Q01": "SELECT ol.ol_number, "
                  "SUM(ol.ol_quantity) AS sum_qty, "
                  "SUM(ol.ol_amount) AS sum_amount, "
                  "AVG(ol.ol_quantity) AS avg_qty, "
                  "AVG(ol.ol_amount) AS avg_amount, "
                  "COUNT(*) AS count_order "
           "FROM   orders o, o.o_orderline ol "
           "WHERE  ol.ol_delivery_d  > '2014-07-01 00:00:00' "
           "GROUP BY ol.ol_number "
           "ORDER BY ol.ol_number;",

    # Q02: Query for listing suppliers and their distributed items having the lowest
    # stock level for a certain item and certain region.
    "Q02": "SELECT su.su_suppkey, su.su_name, n.n_name, i.i_id, i.i_name, su.su_address, su.su_phone, su.su_comment "
           "FROM   item i,  supplier su, stock s, nation n, region r, "
                   "(SELECT s1.s_i_id as m_i_id, MIN(s1.s_quantity) AS m_s_quantity "
                    "FROM stock s1, supplier su1, nation n1, region r1 "
                    "WHERE s1.s_w_id*s1.s_i_id MOD 10000 = su1.su_suppkey "
                      "AND su1.su_nationkey=n1.n_nationkey "
                      "AND n1.n_regionkey=r1.r_regionkey "
                      "AND r1.r_name LIKE 'Europ%' "
                    "GROUP BY s1.s_i_id) m "
           "WHERE i.i_id = s.s_i_id "
             "AND s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND su.su_nationkey = n.n_nationkey "
             "AND n.n_regionkey = r.r_regionkey "
             "AND i.i_data LIKE '%b' "
             "AND r.r_name LIKE 'Europ%' "
             "AND i.i_id=m.m_i_id "
             "AND s.s_quantity = m.m_s_quantity "
           "ORDER BY n.n_name, su.su_name, i.i_id limit 100;",

    # Q03: Unshipped orders with the highest price amount for a customer will be
    # listed within a given state and with orders newer than a specific timestamp.
    # This list will be sorted by the descending amount.
    "Q03": "SELECT o.o_id, o.o_w_id, o.o_d_id, SUM(ol.ol_amount) AS revenue, o.o_entry_d "
           "FROM   customer c, c.c_addresses ca, neworder no, orders o, o.o_orderline ol "
           "WHERE ca.c_address_kind = 'shipping' "
             "AND ca.c_state LIKE 'a%' "
             "AND c.c_id = o.o_c_id "
             "AND c.c_w_id = o.o_w_id "
             "AND c.c_d_id = o.o_d_id "
             "AND no.no_w_id = o.o_w_id "
             "AND no.no_d_id = o.o_d_id "
             "AND no.no_o_id = o.o_id "
             "AND o.o_entry_d < '2017-03-15 00:00:00.000000' "
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, o.o_entry_d "
           "ORDER BY revenue DESC, o.o_entry_d;",

    # Q04: This query is listing all orders with orderlines or just parts of them
    # shipped after the entry date of their booking.
    "Q04": "SELECT o.o_ol_cnt, COUNT(*) as order_count "
           "FROM   orders o "
           "WHERE  o.o_entry_d >= '2015-07-01 00:00:00.000000' AND o.o_entry_d < '2015-10-01 00:00:00.000000' "
           "AND EXISTS (SELECT VALUE 1 "
                       "FROM o.o_orderline ol "
                       "WHERE ol.ol_delivery_d >= DATE_ADD_STR(o.o_entry_d, 1, 'week')) "
           "GROUP BY o.o_ol_cnt "
           "ORDER BY o.o_ol_cnt;",

    # Q05: Query result for getting information about achieved revenues of nations
    # within a given region. All nations are sorted by the total amount of revenue
    # gained since the given date.
    "Q05": "SELECT n.n_name, "
                  "ROUND(SUM(ol.ol_amount), 2) AS revenue "
           "FROM   customer c, c.c_addresses ca, orders o, o.o_orderline ol, stock s, supplier su, nation n, region r "
           "WHERE  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  o.o_w_id = s.s_w_id "
             "AND  ol.ol_i_id = s.s_i_id "
             "AND  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND  ca.c_address_kind = 'shipping' "
             "AND  string_to_codepoint(ca.c_state)[0] = su.su_nationkey "
             "AND  string_to_codepoint(ca.c_state)[0] = n.n_nationkey "
             "AND  su.su_nationkey = n.n_nationkey "
             "AND  n.n_regionkey = r.r_regionkey "
             "AND  r.r_name = 'Asia' "
             "AND  o.o_entry_d >= '2016-01-01 00:00:00.000000' AND o.o_entry_d < '2017-01-01 00:00:00.000000' "
           "GROUP BY n.n_name "
           "ORDER BY revenue DESC;",

    # Q06: Query lists the total amount of archived revenue from orderlines which
    # were delivered in a specific period and a certain quantity.
    "Q06": "SELECT SUM(ol.ol_amount) as revenue "
           "FROM   orders o, o.o_orderline ol "
           "WHERE  ol.ol_delivery_d >= '2016-01-01 00:00:00.000000' "
             "AND  ol.ol_delivery_d < '2017-01-01 00:00:00.000000' "
             "AND  ol.ol_amount > 600;",

    # Q07: Query for showing the bi-directional trade volume between two given
    # nations sorted by their names and the considered years.
    "Q07": "SELECT su.su_nationkey as supp_nation, "
                  "SUBSTR1(ca.c_state,1,1) as cust_nation, "
                  "DATE_PART_STR(o.o_entry_d, 'year') AS l_year, "
                  "ROUND(SUM(ol.ol_amount),2) AS revenue "
           "FROM   supplier su, stock s, orders o, o.o_orderline ol, customer c, c.c_addresses ca, nation n1, nation n2 "
           "WHERE  ol.ol_supply_w_id = s.s_w_id "
             "AND  ol.ol_i_id = s.s_i_id "
             "AND  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  su.su_nationkey = n1.n_nationkey "
             "AND  ca.c_address_kind = 'shipping' "
             "AND  string_to_codepoint(ca.c_state)[0] = n2.n_nationkey "
             "AND  ("
                    "(n1.n_name = 'Germany' and n2.n_name = 'Cambodia') "
                      "OR "
                    "(n1.n_name = 'Cambodia' and n2.n_name = 'Germany') "
                  ") "
             "AND  ol.ol_delivery_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000' "
           "GROUP BY su.su_nationkey, SUBSTR1(ca.c_state,1,1), DATE_PART_STR(o.o_entry_d, 'year') "
           "ORDER BY su.su_nationkey, cust_nation, l_year;",

    # Q08: This query lists the market share of a given nation for customers from
    # a certain region in which kinds of items are "produced".
    "Q08": "SELECT DATE_PART_STR(o.o_entry_d, 'year') AS l_year, "
                  "ROUND((SUM(CASE WHEN n2.n_name = 'Germany' THEN ol.ol_amount ELSE 0 END) / SUM(ol.ol_amount)),2) AS mkt_share "
           "FROM   item i, supplier su, stock s, orders o, o.o_orderline ol, customer c, c.c_addresses ca, nation n1, nation n2, region r "
           "WHERE  i.i_id = s.s_i_id "
             "AND  ol.ol_i_id = s.s_i_id "
             "AND  ol.ol_supply_w_id = s.s_w_id "
             "AND  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  ca.c_address_kind = 'shipping' "
             "AND  n1.n_nationkey = string_to_codepoint(ca.c_state)[0] "
             "AND  n1.n_regionkey = r.r_regionkey "
             "AND  ol.ol_i_id < 1000 "
             "AND  r.r_name = 'Europe' "
             "AND  su.su_nationkey = n2.n_nationkey "
             "AND  o.o_entry_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000' "
             "AND  i.i_data LIKE '%b' "
             "AND  i.i_id = ol.ol_i_id "
           "GROUP BY DATE_PART_STR(o.o_entry_d, 'year') "
           "ORDER BY l_year;",

    # Q09: This query describes how much profit has been made on a selection of
    # items for each nation and each year. The result list will be sorted by the
    # name of the nation and the financial year.
    "Q09": "SELECT   n.n_name, DATE_PART_STR(o.o_entry_d, 'year') AS l_year, SUM(ol.ol_amount) AS sum_profit "
           "FROM     item i, stock s, supplier su, orders o, o.o_orderline ol, nation n "
           "WHERE    ol.ol_i_id = s.s_i_id "
             "AND    ol.ol_supply_w_id = s.s_w_id "
             "AND    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND    ol.ol_i_id = i.i_id "
             "AND    su.su_nationkey = n.n_nationkey "
             "AND    i.i_data like '%bb' "
           "GROUP BY n.n_name, DATE_PART_STR(o.o_entry_d, 'year') "
           "ORDER BY n.n_name, l_year DESC;",
    # Q10: Query for analyzing the expenses of all customers listing their living
    # country, some detail of them and the amount of money which they have used
    # to take their orders since a specific date. The whole list is sorted by the
    # amount of the customers’ orders.
    "Q10": "SELECT c.c_id, c.c_name.c_last, SUM(ol.ol_amount) AS revenue, ca.c_city, cp.c_phone_number, n.n_name "
           "FROM customer c, c.c_addresses ca, c.c_phones cp, orders o, o.o_orderline ol, nation n  "
           "WHERE  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  o.o_entry_d >= '2015-10-01 00:00:00.000000' "
             "AND  o.o_entry_d < '2016-01-01 00:00:00.000000' "
             "AND  ca.c_address_kind = 'shipping' "
             "AND  cp.c_phone_kind = 'contact' "
             "AND  n.n_nationkey = string_to_codepoint(ca.c_state)[0] "
           "GROUP BY c.c_id, c.c_name.c_last, ca.c_city, cp.c_phone_number, n.n_name "
           "ORDER BY revenue DESC "
           "LIMIT 20;",

    # Q11: Most important items (items which are often involved in orders and
    # therefore often bought by customers) supplied by supplier of a given nation.
    "Q11": "SELECT s.s_i_id, SUM(s.s_order_cnt) as ordercount "
           "FROM   stock s,  supplier su, nation n  "
           "WHERE  s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
             "AND  su.su_nationkey = n.n_nationkey "
             "AND  n.n_name = 'Germany' "
           "GROUP BY s.s_i_id "
           "HAVING SUM(s.s_order_cnt) > "
                    "(SELECT VALUE SUM(s1.s_order_cnt) * 0.00005 "
                     "FROM stock s1,  supplier su1, nation n1 "
                     "WHERE s1.s_w_id * s1.s_i_id MOD 10000 = su1.su_suppkey "
                       "AND su1.su_nationkey = n1.n_nationkey "
                       "AND n1.n_name = 'Germany')[0] "
           "ORDER BY ordercount DESC;",

    # Q12: This query counts the amount of orders grouped by the number of
    # orderlines in each order attending the number of orders which are shipped
    # with a higher or lower order priority.
    "Q12": "SELECT o.o_ol_cnt, "
                  "SUM (CASE WHEN o.o_carrier_id = 1 OR o.o_carrier_id = 2 "
                       "THEN 1 ELSE 0 END) AS high_line_COUNT, "
                  "SUM (CASE WHEN o.o_carrier_id <> 1 AND o.o_carrier_id <> 2 "
                       "THEN 1 ELSE 0 END) AS low_line_COUNT "
           "FROM orders o, o.o_orderline ol "
           "WHERE  o.o_entry_d <= ol.ol_delivery_d "
             "AND  ol.ol_delivery_d >= '2016-01-01 00:00:00.000000' AND  ol.ol_delivery_d < '2017-01-01 00:00:00.000000' "
           "GROUP BY o.o_ol_cnt "
           "ORDER BY o.o_ol_cnt;",

    # Q13: The query lists the number of customers grouped and sorted by the size
    # of orders they made. The result set of the relation between customers and
    # the size of their orders is sorted by the size of orders and counts how
    # many customers have dealt the same way.
    "Q13": "SELECT c_orders.c_count, COUNT(*) AS custdist "
           "FROM  (SELECT c.c_id, COUNT(o.o_id) AS c_count "
                  "FROM customer c LEFT OUTER JOIN orders o "
                              "ON (c.c_w_id = o.o_w_id "
                             "AND c.c_d_id = o.o_d_id "
                             "AND c.c_id = o.o_c_id "
                             "AND o.o_carrier_id > 8) "
                  "GROUP BY c.c_id) as c_orders "
           "GROUP BY c_orders.c_count "
           "ORDER BY custdist DESC, c_orders.c_count DESC;",

    # Q14: The query result represents the percentage of the revenue in a period
    # of time which has been realized from promotional campaigns.
    "Q14": "SELECT 100.00 * SUM(CASE WHEN i.i_data LIKE 'pr%' "
                               "THEN ol.ol_amount ELSE 0 END) / "
                               "(1+SUM(ol.ol_amount)) AS promo_revenue "
           "FROM orders o, o.o_orderline ol, item i "
           "WHERE ol.ol_i_id = i.i_id "
             "AND ol.ol_delivery_d >= '2017-09-01 00:00:00.000000' AND ol.ol_delivery_d < '2017-10-01 00:00:00.000000';",

    # Q15: This query finds the top supplier or suppliers who contributed the
    # most to the overall revenue for items shipped during a given period of time.
    "Q15": "WITH revenue AS ( "
                "SELECT s.s_w_id * s.s_i_id MOD 10000 as supplier_no, SUM(ol.ol_amount) AS total_revenue "
                "FROM   orders o, o.o_orderline ol, stock s "
                "WHERE ol.ol_i_id = s.s_i_id "
                  "AND ol.ol_supply_w_id = s.s_w_id "
                  "AND ol.ol_delivery_d >= '2018-01-01 00:00:00.000000' AND ol.ol_delivery_d < '2018-04-01 00:00:00.000000' "
                "GROUP BY s.s_w_id * s.s_i_id MOD 10000) "
           "SELECT su.su_suppkey, su.su_name, su.su_address, su.su_phone, r.total_revenue "
           "FROM   supplier su, revenue r "
           "WHERE  su.su_suppkey = r.supplier_no "
             "AND  r.total_revenue = (SELECT VALUE max(r1.total_revenue) FROM revenue r1)[0] "
           "ORDER BY su.su_suppkey;",

    # Q16: This query finds out how many suppliers are able to supply items with
    # given attributes sorted in descending order of them. The result is grouped
    # by the identifier of the item.
    "Q16": "SELECT i.i_name, SUBSTR1(i.i_data, 1, 3) AS brand, i.i_price, "
                  "COUNT(DISTINCT (s.s_w_id * s.s_i_id MOD 10000)) AS supplier_cnt "
           "FROM stock s, item i "
           "WHERE i.i_id = s.s_i_id "
             "AND i.i_data not LIKE 'zz%' "
             "AND (s.s_w_id * s.s_i_id MOD 10000 NOT IN "
                                         "(SELECT VALUE su.su_suppkey "
                                          "FROM supplier su "
                                          "WHERE su.su_comment LIKE '%Customer%Complaints%')) "
           "GROUP BY i.i_name, SUBSTR1(i.i_data, 1, 3), i.i_price "
           "ORDER BY supplier_cnt DESC;",

    # Q17: The query determines the yearly loss in revenue if orders just with a
    # quantity of more than the average quantity of all orders in the system
    # would be taken and shipped to customers.
    "Q17": "SELECT SUM(ol.ol_amount) / 2.0 AS avg_yearly "
           "FROM  orders o, o.o_orderline ol, (SELECT i.i_id, AVG(ol1.ol_quantity) AS a "
                                              "FROM   item i, orders o1, o1.o_orderline ol1 "
                                              "WHERE  i.i_data LIKE '%b' "
                                                "AND  ol1.ol_i_id = i.i_id "
                                              "GROUP BY i.i_id) t "
           "WHERE ol.ol_i_id = t.i_id "
             "AND ol.ol_quantity < t.a;",

    # Q18: Query 18 is ranking all customers who have ordered for more than a
    # specific amount of money.
    "Q18": "SELECT c.c_name.c_last, c.c_id o_id, o.o_entry_d, o.o_ol_cnt, SUM(ol.ol_amount) "
           "FROM customer c, orders o, o.o_orderline ol "
           "WHERE  c.c_id = o.o_c_id AND  c.c_w_id = o.o_w_id AND  c.c_d_id = o.o_d_id "
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, c.c_id, c.c_name.c_last, o.o_entry_d, o.o_ol_cnt "
           "HAVING SUM(ol.ol_amount) > 200 "
           "ORDER BY SUM(ol.ol_amount) DESC, o.o_entry_d "
           "LIMIT 100;",

    # Q19: The query is for reporting the revenue achieved by some specific
    # attributes, as the price, the detailed information of the item and the
    # quantity of the ordered amount of them.
    "Q19": "SELECT SUM(ol.ol_amount) AS revenue "
           "FROM orders o, o.o_orderline ol, item i "
           "WHERE  (( "
                    "i.i_data LIKE '%h' "
                    "AND ol.ol_quantity >= 7 AND ol.ol_quantity <= 17 "
                    "AND i.i_price between 1 AND 5 "
                    "AND o.o_w_id IN [37, 29, 70] "
                   ") OR ( "
                    "i.i_data LIKE '%t' "
                    "AND ol.ol_quantity >= 16 AND ol.ol_quantity <= 26 "
                    "AND i.i_price between 1 AND 10 "
                    "AND o.o_w_id IN [78, 17, 6] "
                   ") OR ( "
                    "i.i_data LIKE '%m' "
                    "AND ol.ol_quantity >= 24 AND ol.ol_quantity <= 34 "
                    "AND i.i_price between 1 AND 15 "
                    "AND  o.o_w_id IN [91, 95, 15] "
                    ")) "
                  "AND ol.ol_i_id = i.i_id "
                  "AND i.i_price between 1 AND 15;",

    # Q20: Suppliers in a particular nation having selected parts that may be
    # candidates for a promotional offer if the quantity of these items is more
    # than 50 percent of the total quantity which has been ordered since a certain date.
    "Q20": "SELECT su.su_name, su.su_address "
           "FROM   supplier su, nation n "
           "WHERE  su.su_suppkey IN "
                         "(SELECT VALUE s.s_i_id * s.s_w_id MOD 10000 "
                          "FROM   stock s, orders o, o.o_orderline ol "
                          "WHERE  s.s_i_id IN "
                              "(SELECT VALUE i.i_id "
                               "FROM item i "
                              "WHERE i.i_data LIKE 'co%') "
                            "AND ol.ol_i_id=s.s_i_id "
                            "AND ol.ol_delivery_d >= '2016-01-01 12:00:00' "
                            "AND ol.ol_delivery_d < '2017-01-01 12:00:00' "
                           "GROUP BY s.s_i_id, s.s_w_id, s.s_quantity "
                           "HAVING 20*s.s_quantity > SUM(ol.ol_quantity)) "
             "AND su.su_nationkey = n.n_nationkey "
             "AND n.n_name = 'Germany' "
           "ORDER BY su.su_name;",

    # Q21: Query 21 determines the suppliers which have shipped some required
    # items of an order not in a timely manner for a given nation.
    "Q21": "SELECT z.su_name, COUNT (*) AS numwait "
            "FROM (SELECT x.su_name "
                  "FROM (SELECT o1.o_id, o1.o_w_id, o1.o_d_id, ol1.ol_delivery_d, "
                                           "n.n_nationkey, su.su_suppkey, s.s_w_id, s.s_i_id, su.su_name "
                        "FROM nation n, supplier su, stock s, orders o1, o1.o_orderline ol1 "
                        "WHERE o1.o_w_id = s.s_w_id "
                          "AND ol1.ol_i_id = s.s_i_id "
                          "AND s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey "
                          "AND ol1.ol_delivery_d > date_add_str(o1.o_entry_d, 150, 'day') "
                          "AND o1.o_entry_d between '2017-12-01 00:00:00' and '2017-12-31 00:00:00' "
                          "AND su.su_nationkey = n.n_nationkey "
                          "AND n.n_name = 'Peru') x "
                       "LEFT OUTER JOIN "
                       "(SELECT o2.o_id, o2.o_w_id, o2.o_d_id, ol2.ol_delivery_d "
                        "FROM orders o2, o2.o_orderline ol2 "
                        "WHERE o2.o_entry_d BETWEEN '2017-12-01 00:00:00' AND '2017-12-31 00:00:00') y "
                   "ON y.o_id = x.o_id AND y.o_w_id = x.o_w_id AND y.o_d_id = x.o_d_id "
                  "AND y.ol_delivery_d > x.ol_delivery_d "
                  "GROUP BY x.o_w_id, x.o_d_id, x.o_id, x.n_nationkey, x.su_suppkey, x.s_w_id, x.s_i_id, x.su_name "
                  "HAVING COUNT (y.o_id) = 0) z "
           "GROUP BY z.su_name "
           "LIMIT 100;",

    # Q22: This query lists how many customers within a specific range of country
    # codes have not bought anything for the whole period of time and who have a
    # greater than average balance on their account. The county code is represented
    # by the first two characters of the phone number.
    "Q22": "SELECT SUBSTR1(ca.c_state,1,1) AS country, COUNT(*) AS numcust, SUM(c.c_balance) AS totacctbal "
           "FROM customer c, c.c_addresses ca, c.c_phones cp "
           "WHERE SUBSTR1(cp.c_phone_number,1,1) IN ['1','2','3','4','5','6','7'] "
             "AND   ca.c_address_kind = 'shipping' "
             "AND   cp.c_phone_kind = 'contact' "
             "AND c.c_balance > (SELECT VALUE AVG(c1.c_balance) "
                                "FROM customer c1, c1.c_phones cp1 "
                                "WHERE c1.c_balance > 0.00 "
                                  "AND cp1.c_phone_kind = 'contact' "
                                  "AND SUBSTR1(cp1.c_phone_number,1,1) IN ['1','2','3','4','5','6','7'])[0] "
             "AND NOT EXISTS (SELECT VALUE 1 "
                             "FROM orders o "
                             "WHERE o.o_c_id = c.c_id AND o.o_w_id = c.c_w_id AND o.o_d_id = c.c_d_id "
                               "AND o.o_entry_d BETWEEN '2013-12-01 00:00:00' AND '2013-12-31 00:00:00') "
           "GROUP BY SUBSTR1(ca.c_state,1,1) "
           "ORDER BY SUBSTR1(ca.c_state,1,1);"
}


CH2_MONGO_QUERIES ={
    # Q01: This query reports the total amount and quantity of all shipped orderlines
    # given by a specific time period. Additionally it informs about the average
    # amount and quantity plus the total count of all these orderlines ordered
    # by the individual orderline number.
    "Q01": "SELECT ol_number, "
                  "SUM(o.o_orderline.ol_quantity) AS sum_qty, "
                  "SUM(o.o_orderline.ol_amount) AS sum_amount, "
                  "AVG(o.o_orderline.ol_quantity) AS avg_qty, "
                  "AVG(o.o_orderline.ol_amount) AS avg_amount, "
                  "COUNT(*) AS count_order "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE o.o_orderline.ol_delivery_d  > '2014-07-01 00:00:00' "
           "GROUP BY o_orderline.ol_number AS ol_number "
           "ORDER BY ol_number ",

    # Q02: Query for listing suppliers and their distributed items having the lowest
    # stock level for a certain item and certain region.
    "Q02": "SELECT su.su_suppkey, su.su_name, n.n_name, i.i_id, i.i_name, "
                   "su.su_address, su.su_phone, su.su_comment "
           "FROM   item i,  supplier su, stock s, nation n, region r, "
                  "(SELECT s1.s_i_id as m_i_id, MIN(s1.s_quantity) AS m_s_quantity "
                   "FROM stock s1, supplier su1, nation n1, region r1 "
                   "WHERE MOD(s1.s_w_id * s1.s_i_id, 10000) = su1.su_suppkey "
                     "AND su1.su_nationkey=n1.n_nationkey "
                     "AND n1.n_regionkey=r1.r_regionkey "
                     "AND r1.r_name LIKE 'Europ%' "
                   "GROUP BY s1.s_i_id) m "
           "WHERE i.i_id = s.s_i_id "
             "AND MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND su.su_nationkey = n.n_nationkey "
             "AND n.n_regionkey = r.r_regionkey "
             "AND i.i_data LIKE '%b' "
             "AND r.r_name LIKE 'Europ%' "
             "AND i.i_id=m.m_i_id "
             "AND s.s_quantity = m.m_s_quantity "
           "ORDER BY n.n_name, su.su_name, i.i_id "
           "LIMIT 100 ",


    # Q03: Unshipped orders with the highest price amount for a customer will be
    # listed within a given state and with orders newer than a specific timestamp.
    # This list will be sorted by the descending amount.
    "Q03": "SELECT o.o_id, o.o_w_id, o.o_d_id, "
                  "SUM(o.o_orderline.ol_amount) AS revenue, o.o_entry_d "
           "FROM customer c, neworder no, "
                "UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE c.c_state LIKE 'a%' "
             "AND c.c_id = o.o_c_id "
             "AND c.c_w_id = o.o_w_id "
             "AND c.c_d_id = o.o_d_id "
             "AND no.no_w_id = o.o_w_id "
             "AND no.no_d_id = o.o_d_id "
             "AND no.no_o_id = o.o_id "
             "AND o.o_entry_d < '2017-03-15 00:00:00.000000' "
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, o.o_entry_d "
           "ORDER BY revenue DESC, o.o_entry_d ",

    # Q04: This query is listing all orders with orderlines or just parts of them
    # shipped after the entry date of their booking.
    "Q04": "SELECT ol_cnt, COUNT(*) as order_count "
           "FROM   orders o "
           "WHERE  o.o_entry_d >= '2015-07-01 00:00:00.000000' "
             "AND o.o_entry_d < '2015-10-01 00:00:00.000000' "
             "AND EXISTS (SELECT 1 "
                         "FROM UNWIND (orders AS o WITH PATH => o_orderline) "
                         "WHERE o.o_orderline.ol_delivery_d >= "
                                "CAST(DATEADD(week, 1, CAST(o.o_entry_d AS TIMESTAMP)) AS STRING)) "
           "GROUP BY o.o_ol_cnt AS ol_cnt "
           "ORDER BY ol_cnt ",

    # Q05: Query result for getting information about achieved revenues of nations
    # within a given region. All nations are sorted by the total amount of revenue
    # gained since the given date.
    "Q05": "SELECT  nname, ROUND(SUM(o.o_orderline.ol_amount), 2) AS revenue "
           "FROM    customer c, "
                   "UNWIND (orders AS o WITH PATH => o_orderline), "
                   "stock s, supplier su, nation n, region r "
           "WHERE    c.c_id = o.o_c_id "
             "AND    c.c_w_id = o.o_w_id "
             "AND    c.c_d_id = o.o_d_id "
             "AND    o.o_w_id = s.s_w_id "
             "AND    o.o_orderline.ol_i_id = s.s_i_id "
             "AND    MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND    POSITION(SUBSTRING(c.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') = su.su_nationkey "
             "AND    POSITION(SUBSTRING(c.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') = n.n_nationkey "
             "AND    su.su_nationkey = n.n_nationkey "
             "AND    n.n_regionkey = r.r_regionkey "
             "AND    r.r_name = 'Asia' "
             "AND    o.o_entry_d >= '2016-01-01 00:00:00.000000' "
             "AND    o.o_entry_d < '2017-01-01 00:00:00.000000' "
           "GROUP BY n.n_name AS nname "
           "ORDER BY revenue DESC ",

    # Q06: Query lists the total amount of archived revenue from orderlines which
    # were delivered in a specific period and a certain quantity.
    "Q06": "SELECT SUM(o.o_orderline.ol_amount) as revenue "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE  o.o_orderline.ol_delivery_d >= '2016-01-01 00:00:00.000000' "
             "AND  o.o_orderline.ol_delivery_d < '2017-01-01 00:00:00.000000' "
             "AND  o.o_orderline.ol_amount > 600 ",

    # Q07: Query for showing the bi-directional trade volume between two given
    # nations sorted by their names and the considered years.
    "Q07": "SELECT supp_nation, cust_nation, l_year, "
	           "ROUND(SUM(o.o_orderline.ol_amount),2) AS revenue "
           "FROM   supplier su, stock s, "
                   "UNWIND (orders AS o WITH PATH => o_orderline), "
                   "customer c, nation n1, nation n2 "
           "WHERE    o.o_orderline.ol_supply_w_id = s.s_w_id "
             "AND    o.o_orderline.ol_i_id = s.s_i_id "
             "AND    MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
              "AND    c.c_id = o.o_c_id "
             "AND    c.c_w_id = o.o_w_id "
             "AND    c.c_d_id = o.o_d_id "
             "AND    su.su_nationkey = n1.n_nationkey "
             "AND    POSITION(SUBSTRING(c.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') = n2.n_nationkey "
             "AND    ((n1.n_name = 'Germany' and n2.n_name = 'Cambodia') OR "
                     "(n1.n_name = 'Cambodia' and n2.n_name = 'Germany')) "
             "AND    o.o_orderline.ol_delivery_d BETWEEN '2017-01-01 00:00:00.000000' "
                                         "AND '2018-12-31 00:00:00.000000' "
           "GROUP BY su.su_nationkey AS supp_nation, "
                     "SUBSTRING(c.c_state,0,1) AS cust_nation, "
                     "EXTRACT(YEAR FROM CAST(o.o_entry_d AS TIMESTAMP)) AS l_year "
           "ORDER BY supp_nation, cust_nation, l_year ",

    # Q08: This query lists the market share of a given nation for customers from
    # a certain region in which kinds of items are "produced".
    "Q08": "SELECT l_year, "
                  "ROUND((SUM(CASE WHEN n2.n_name = 'Germany' "
                  "THEN o.o_orderline.ol_amount "
                  "ELSE 0 END) / SUM(o.o_orderline.ol_amount)),2) AS mkt_share "
           "FROM  item i, supplier su, stock s, "
                 "UNWIND (orders AS o WITH PATH => o_orderline), "
                 "customer c, nation n1, nation n2, region r "
           "WHERE i.i_id = s.s_i_id "
             "AND o.o_orderline.ol_i_id = s.s_i_id "
             "AND o.o_orderline.ol_supply_w_id = s.s_w_id "
             "AND MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND c.c_id = o.o_c_id "
             "AND c.c_w_id = o.o_w_id "
             "AND c.c_d_id = o.o_d_id "
             "AND n1.n_nationkey = POSITION(SUBSTRING(c.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') "
             "AND n1.n_regionkey = r.r_regionkey "
             "AND o.o_orderline.ol_i_id < 1000 "
             "AND r.r_name = 'Europe' "
             "AND su.su_nationkey = n2.n_nationkey "
             "AND o.o_entry_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000' "
             "AND i.i_data LIKE '%b' "
             "AND i.i_id = o.o_orderline.ol_i_id "
           "GROUP BY EXTRACT(YEAR FROM CAST(o.o_entry_d AS TIMESTAMP)) AS l_year "
           "ORDER BY l_year ",

    # Q09: This query describes how much profit has been made on a selection of
    # items for each nation and each year. The result list will be sorted by the
    # name of the nation and the financial year.
    "Q09": "SELECT  n_name, l_year, "
                   "SUM(o.o_orderline.ol_amount) AS sum_profit "
           "FROM    item i, stock s, supplier su, "
                   "UNWIND (orders AS o WITH PATH => o_orderline), nation n "
           "WHERE   o.o_orderline.ol_i_id = s.s_i_id "
             "AND    o.o_orderline.ol_supply_w_id = s.s_w_id "
             "AND    MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND    o.o_orderline.ol_i_id = i.i_id "
             "AND    su.su_nationkey = n.n_nationkey "
             "AND    i.i_data like '%bb' "
           "GROUP BY n.n_name AS n_name, "
                     "EXTRACT(YEAR FROM CAST(o.o_entry_d AS TIMESTAMP)) AS l_year "
           "ORDER BY n_name, l_year DESC ",
    # Q10: Query for analyzing the expenses of all customers listing their living
    # country, some detail of them and the amount of money which they have used
    # to take their orders since a specific date. The whole list is sorted by the
    # amount of the customers’ orders.
    "Q10": "SELECT cid, clast, SUM(o.o_orderline.ol_amount) AS revenue, "
                   "ccity, cphone, nname "
           "FROM customer c, "
                "UNWIND (orders AS o WITH PATH => o_orderline), nation n "
           "WHERE  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  o.o_entry_d >= '2015-10-01 00:00:00.000000' "
             "AND  o.o_entry_d < '2016-01-01 00:00:00.000000' "
             "AND n.n_nationkey = POSITION(SUBSTRING(c.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') "
           "GROUP BY c.c_id AS cid, c.c_last AS clast, c.c_city AS ccity, "
                    "c.c_phone AS cphone, n.n_name AS nname "
           "ORDER BY revenue DESC "
           "LIMIT 20 ",

    # Q11: Most important items (items which are often involved in orders and
    # therefore often bought by customers) supplied by supplier of a given nation.
    "Q11": "SELECT s.s_i_id, SUM(s.s_order_cnt) as ordercount "
           "FROM   stock s,  supplier su, nation n "
           "WHERE  MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND  su.su_nationkey = n.n_nationkey "
             "AND  n.n_name = 'Germany' "
           "GROUP BY s.s_i_id "
           "HAVING SUM(s.s_order_cnt) > "
                  "(SELECT SUM(s1.s_order_cnt) * 0.00005 "
                   "FROM stock s1, supplier su1, nation n1 "
                   "WHERE MOD(s1.s_w_id * s1.s_i_id, 10000) = su1.su_suppkey "
                     "AND su1.su_nationkey = n1.n_nationkey "
                     "AND n1.n_name = 'Germany') "
           "ORDER BY ordercount DESC ",

    # Q12: This query counts the amount of orders grouped by the number of
    # orderlines in each order attending the number of orders which are shipped
    # with a higher or lower order priority.
    "Q12": "SELECT ol_cnt, "
                   "SUM (CASE WHEN o.o_carrier_id = 1 OR o.o_carrier_id = 2 "
                         "THEN 1 ELSE 0 END) AS high_line_COUNT, "
                   "SUM (CASE WHEN o.o_carrier_id <> 1 AND o.o_carrier_id <> 2 "
                         "THEN 1 ELSE 0 END) AS low_line_COUNT "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE  o.o_entry_d <= o.o_orderline.ol_delivery_d "
             "AND  o.o_orderline.ol_delivery_d >= '2016-01-01 00:00:00.000000' "
             "AND  o.o_orderline.ol_delivery_d < '2017-01-01 00:00:00.000000' "
           "GROUP BY o.o_ol_cnt AS ol_cnt "
           "ORDER BY ol_cnt ",

    # Q13: The query lists the number of customers grouped and sorted by the size
    # of orders they made. The result set of the relation between customers and
    # the size of their orders is sorted by the size of orders and counts how
    # many customers have dealt the same way.
    "Q13": "SELECT c_count, COUNT(*) AS custdist "
           "FROM  (SELECT c.c_id, COUNT(o.o_id) AS c_count "
                   "FROM customer c LEFT OUTER JOIN orders o "
                     "ON (c.c_w_id = o.o_w_id "
                    "AND c.c_d_id = o.o_d_id "
                    "AND c.c_id = o.o_c_id "
                    "AND o.o_carrier_id > 8) "
                   "GROUP BY c.c_id) as c_orders "
           "GROUP BY c_orders.c_count AS c_count "
           "ORDER BY custdist DESC, c_count DESC ",

    # Q14: The query result represents the percentage of the revenue in a period
    # of time which has been realized from promotional campaigns.
    "Q14": "SELECT 100.00 * SUM(CASE WHEN i.i_data LIKE 'pr%' "
                                "THEN o.o_orderline.ol_amount ELSE 0 END) / "
                                "(1+SUM(o.o_orderline.ol_amount)) AS promo_revenue "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline), item i "
           "WHERE o.o_orderline.ol_i_id = i.i_id "
             "AND o.o_orderline.ol_delivery_d >= '2017-09-01 00:00:00.000000' "
             "AND o.o_orderline.ol_delivery_d < '2017-10-01 00:00:00.000000' ",

    # Q15: This query finds the top supplier or suppliers who contributed the
    # most to the overall revenue for items shipped during a given period of time.
    "Q15": "SELECT su.su_suppkey, su.su_name, su.su_address, su.su_phone, r.total_revenue "
           "FROM supplier su, "
                "(SELECT supplier_no, SUM(o.o_orderline.ol_amount) AS total_revenue "
                 "FROM   UNWIND (orders AS o WITH PATH => o_orderline), stock s "
                 "WHERE o.o_orderline.ol_i_id = s.s_i_id "
                   "AND o.o_orderline.ol_supply_w_id = s.s_w_id "
                   "AND o.o_orderline.ol_delivery_d >= '2018-01-01 00:00:00.000000' "
                   "AND o.o_orderline.ol_delivery_d < '2018-04-01 00:00:00.000000' "
                 "GROUP BY MOD(s.s_w_id * s.s_i_id, 10000) AS supplier_no) AS r "
           "WHERE su.su_suppkey = r.supplier_no "
             "AND r.total_revenue = "
                  "(SELECT MAX(r1.total_revenue) "
                  "FROM (SELECT supplier_no, SUM(o.o_orderline.ol_amount) AS total_revenue "
                        "FROM UNWIND (orders AS o WITH PATH => o_orderline), stock s "
                        "WHERE o.o_orderline.ol_i_id = s.s_i_id "
                          "AND o.o_orderline.ol_supply_w_id = s.s_w_id "
                          "AND o.o_orderline.ol_delivery_d >= '2018-01-01 00:00:00.000000' "
                          "AND o.o_orderline.ol_delivery_d < '2018-04-01 00:00:00.000000' "
                        "GROUP BY MOD(s.s_w_id * s.s_i_id, 10000) AS supplier_no) AS r1) "
           "ORDER BY su.su_suppkey ",

    # Q16: This query finds out how many suppliers are able to supply items with
    # given attributes sorted in descending order of them. The result is grouped
    # by the identifier of the item.
    "Q16": "SELECT iname, brand, iprice, "
                   "COUNT(DISTINCT MOD((s.s_w_id * s.s_i_id), 10000)) AS supplier_cnt "
           "FROM stock s, item i "
           "WHERE i.i_id = s.s_i_id "
             "AND i.i_data NOT LIKE 'zz%' "
             "AND (MOD((s.s_w_id * s.s_i_id), 10000) NOT IN "
                                  "(SELECT su.su_suppkey "
                                   "FROM supplier su "
                                   "WHERE su.su_comment LIKE '%Customer%Complaints%')) "
           "GROUP BY i.i_name AS iname, "
                     "SUBSTRING(i.i_data, 0, 3) AS brand, i.i_price AS iprice "
           "ORDER BY supplier_cnt DESC ",

    # Q17: The query determines the yearly loss in revenue if orders just with a
    # quantity of more than the average quantity of all orders in the system
    # would be taken and shipped to customers.
    "Q17": "SELECT SUM(o.o_orderline.ol_amount) / 2.0 AS avg_yearly "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline), "
               "(SELECT iid, AVG(o1.o_orderline.ol_quantity) AS a "
                "FROM   item i, UNWIND (orders AS o1 WITH PATH => o_orderline) "
                "WHERE  i.i_data LIKE '%b' AND  o1.o_orderline.ol_i_id = i.i_id "
                "GROUP BY i.i_id AS iid) t "
           "WHERE o.o_orderline.ol_i_id = t.iid "
             "AND o.o_orderline.ol_quantity < t.a ",

    # Q18: Query 18 is ranking all customers who have ordered for more than a
    # specific amount of money.
    "Q18": "SELECT clast, c.c_id, o.o_id, o.o_entry_d, o.o_ol_cnt, "
                  "SUM(o.o_orderline.ol_amount) AS ol_sum "
           "FROM customer c, UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND c.c_d_id = o.o_d_id "
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, c.c_id, c.c_name.c_last AS clast, o.o_entry_d, o.o_ol_cnt "
           "HAVING SUM(o.o_orderline.ol_amount) > 200 "
           "ORDER BY ol_sum DESC, o.o_entry_d  "
           "LIMIT 100 ",

    # Q19: The query is for reporting the revenue achieved by some specific
    # attributes, as the price, the detailed information of the item and the
    # quantity of the ordered amount of them.
    "Q19": "SELECT SUM(o.o_orderline.ol_amount) AS revenue "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline), item i "
           "WHERE  (( "
                   "i.i_data LIKE '%h' "
                   "AND o.o_orderline.ol_quantity >= 7 "
                   "AND o.o_orderline.ol_quantity <= 17 "
                   "AND i.i_price between 1 AND 5 "
                   "AND o.o_w_id IN (37, 29, 70) "
                   ") OR ( "
                   "i.i_data LIKE '%t' "
                   "AND o.o_orderline.ol_quantity >= 16 "
                   "AND o.o_orderline.ol_quantity <= 26 "
                   "AND i.i_price between 1 AND 10 "
                   "AND o.o_w_id IN (78, 17, 6) "
                   ") OR ( "
                   "i.i_data LIKE '%m' "
                   "AND o.o_orderline.ol_quantity >= 24 "
                   "AND o.o_orderline.ol_quantity <= 34 "
                   "AND i.i_price between 1 AND 15 "
                   "AND  o.o_w_id IN (91, 95, 15) "
                   ")) "
             "AND o.o_orderline.ol_i_id = i.i_id "
             "AND i.i_price between 1 AND 15 ",

    # Q20: Suppliers in a particular nation having selected parts that may be
    # candidates for a promotional offer if the quantity of these items is more
    # than 50 percent of the total quantity which has been ordered since a certain date.
    "Q20": "SELECT su.su_name, su.su_address "
           "FROM   supplier su, nation n "
           "WHERE  su.su_suppkey IN "
                  "(SELECT MOD(s.s_i_id * s.s_w_id, 10000) "
                   "FROM   stock s, UNWIND (orders AS o WITH PATH => o_orderline) "
                   "WHERE  s.s_i_id IN (SELECT i.i_id "
                                       "FROM item i "
                                       "WHERE i.i_data LIKE 'co%') "
                     "AND  o.o_orderline.ol_i_id = s.s_i_id "
                     "AND  o.o_orderline.ol_delivery_d >= '2016-01-01 12:00:00' "
                     "AND  o.o_orderline.ol_delivery_d < '2017-01-01 12:00:00' "
                   "GROUP BY s.s_i_id, s.s_w_id, s.s_quantity "
                   "HAVING 20*s.s_quantity > SUM(o.o_orderline.ol_quantity)) "
             "AND su.su_nationkey = n.n_nationkey "
             "AND n.n_name = 'Germany' "
           "ORDER BY su.su_name ",

    # Q21: Query 21 determines the suppliers which have shipped some required
    # items of an order not in a timely manner for a given nation.
    "Q21": "SELECT z.su_name, COUNT (*) AS numwait "
           "FROM (SELECT x.su_name "
                 "FROM (SELECT o1.o_id, o1.o_w_id, o1.o_d_id, o1.o_orderline.ol_delivery_d, "
                              "n.n_nationkey, su.su_suppkey, s.s_w_id, s.s_i_id, su.su_name "
                       "FROM nation n, supplier su, stock s, "
                            "UNWIND (orders AS o1 WITH PATH => o_orderline) "
                       "WHERE o1.o_w_id = s.s_w_id "
                         "AND o1.o_orderline.ol_i_id = s.s_i_id "
                         "AND MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
                         "AND o1.o_orderline.ol_delivery_d > "
                             "CAST(DATEADD(day, 150, CAST(o1.o_entry_d AS TIMESTAMP)) AS STRING) "
                         "AND o1.o_entry_d BETWEEN '2017-12-01 00:00:00' "
                                              "AND '2017-12-31 00:00:00' "
                         "AND su.su_nationkey = n.n_nationkey "
                         "AND n.n_name = 'Peru' ) x "
                     "LEFT OUTER JOIN "
                      "(SELECT o2.o_id, o2.o_w_id, o2.o_d_id, o2.o_orderline.ol_delivery_d "
                       "FROM UNWIND (orders AS o2 WITH PATH => o_orderline) "
                       "WHERE o2.o_entry_d BETWEEN '2017-12-01 00:00:00' "
                                              "AND '2017-12-31 00:00:00' ) y "
                     "ON y.o_id = x.o_id "
                     "AND y.o_w_id = x.o_w_id "
                     "AND y.o_d_id = x.o_d_id "
                     "AND y.ol_delivery_d > x.ol_delivery_d "
                  "GROUP BY x.o_w_id, x.o_d_id, x.o_id, x.n_nationkey, "
                           "x.su_suppkey, x.s_w_id, x.s_i_id, x.su_name "
                  "HAVING COUNT (y.o_id) = 0) z "
           "GROUP BY z.su_name "
           "LIMIT 100 ",

    # Q22: This query lists how many customers within a specific range of country
    # codes have not bought anything for the whole period of time and who have a
    # greater than average balance on their account. The county code is represented
    # by the first two characters of the phone number.
    "Q22": "SELECT country, COUNT(*) AS numcust, SUM(c.c_balance) AS totacctbal "
           "FROM customer c"
           "WHERE SUBSTRING(c.c_phone,0,1) IN "
                                             "('1','2','3','4','5','6','7') "
             "AND c.c_balance > (SELECT AVG(c1.c_balance) "
                                "FROM customer c1"
                                "WHERE c1.c_balance > 0.00 "
                                  "AND SUBSTRING(c1.c_phone,0,1) IN "
                                        "('1','2','3','4','5','6','7') ) "
             "AND NOT EXISTS (SELECT 1 "
                             "FROM orders o "
                             "WHERE o.o_c_id = c.c_id "
                               "AND o.o_w_id = c.c_w_id "
                               "AND o.o_d_id = c.c_d_id "
                               "AND o.o_entry_d BETWEEN '2013-12-01 00:00:00' AND '2013-12-31 00:00:00') "
           "GROUP BY SUBSTRING(c.c_state,0,1) AS country "
           "ORDER BY country "
}

CH2PP_MONGO_QUERIES = {
    # Q01: This query reports the total amount and quantity of all shipped orderlines
    # given by a specific time period. Additionally it informs about the average
    # amount and quantity plus the total count of all these orderlines ordered
    # by the individual orderline number.
    "Q01": "SELECT ol_number, "
                  "SUM(o.o_orderline.ol_quantity) AS sum_qty, "
                  "SUM(o.o_orderline.ol_amount) AS sum_amount, "
                  "AVG(o.o_orderline.ol_quantity) AS avg_qty, "
                  "AVG(o.o_orderline.ol_amount) AS avg_amount, "
                  "COUNT(*) AS count_order "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE o.o_orderline.ol_delivery_d  > '2014-07-01 00:00:00' "
           "GROUP BY o_orderline.ol_number AS ol_number "
           "ORDER BY ol_number ",

    # Q02: Query for listing suppliers and their distributed items having the lowest
    # stock level for a certain item and certain region.
    "Q02": "SELECT su.su_suppkey, su.su_name, n.n_name, i.i_id, i.i_name, "
                   "su.su_address, su.su_phone, su.su_comment "
           "FROM   item i,  supplier su, stock s, nation n, region r, "
                  "(SELECT s1.s_i_id as m_i_id, MIN(s1.s_quantity) AS m_s_quantity "
                   "FROM stock s1, supplier su1, nation n1, region r1 "
                   "WHERE MOD(s1.s_w_id * s1.s_i_id, 10000) = su1.su_suppkey "
                     "AND su1.su_nationkey=n1.n_nationkey "
                     "AND n1.n_regionkey=r1.r_regionkey "
                     "AND r1.r_name LIKE 'Europ%' "
                   "GROUP BY s1.s_i_id) m "
           "WHERE i.i_id = s.s_i_id "
             "AND MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND su.su_nationkey = n.n_nationkey "
             "AND n.n_regionkey = r.r_regionkey "
             "AND i.i_data LIKE '%b' "
             "AND r.r_name LIKE 'Europ%' "
             "AND i.i_id=m.m_i_id "
             "AND s.s_quantity = m.m_s_quantity "
           "ORDER BY n.n_name, su.su_name, i.i_id "
           "LIMIT 100 ",


    # Q03: Unshipped orders with the highest price amount for a customer will be
    # listed within a given state and with orders newer than a specific timestamp.
    # This list will be sorted by the descending amount.
    "Q03": "SELECT o.o_id, o.o_w_id, o.o_d_id, "
                  "SUM(o.o_orderline.ol_amount) AS revenue, o.o_entry_d "
           "FROM UNWIND (customer AS c WITH PATH => c_addresses), "
                "neworder no, "
                "UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE c.c_addresses.c_address_kind = 'shipping' "
             "AND c.c_addresses.c_state LIKE 'a%' "
             "AND c.c_id = o.o_c_id "
             "AND c.c_w_id = o.o_w_id "
             "AND c.c_d_id = o.o_d_id "
             "AND no.no_w_id = o.o_w_id "
             "AND no.no_d_id = o.o_d_id "
             "AND no.no_o_id = o.o_id "
             "AND o.o_entry_d < '2017-03-15 00:00:00.000000' "
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, o.o_entry_d "
           "ORDER BY revenue DESC, o.o_entry_d ",

    # Q04: This query is listing all orders with orderlines or just parts of them
    # shipped after the entry date of their booking.
    "Q04": "SELECT ol_cnt, COUNT(*) as order_count "
           "FROM   orders o "
           "WHERE  o.o_entry_d >= '2015-07-01 00:00:00.000000' "
             "AND o.o_entry_d < '2015-10-01 00:00:00.000000' "
             "AND EXISTS (SELECT 1 "
                         "FROM UNWIND (orders AS o WITH PATH => o_orderline) "
                         "WHERE o.o_orderline.ol_delivery_d >= "
                                "CAST(DATEADD(week, 1, CAST(o.o_entry_d AS TIMESTAMP)) AS STRING)) "
           "GROUP BY o.o_ol_cnt AS ol_cnt "
           "ORDER BY ol_cnt ",

    # Q05: Query result for getting information about achieved revenues of nations
    # within a given region. All nations are sorted by the total amount of revenue
    # gained since the given date.
    "Q05": "SELECT  nname, ROUND(SUM(o.o_orderline.ol_amount), 2) AS revenue "
           "FROM    UNWIND (customer AS c WITH PATH => c_addresses), "
                   "UNWIND (orders AS o WITH PATH => o_orderline), "
                   "stock s, supplier su, nation n, region r "
           "WHERE    c.c_addresses.c_address_kind = 'shipping' "
             "AND    c.c_id = o.o_c_id "
             "AND    c.c_w_id = o.o_w_id "
             "AND    c.c_d_id = o.o_d_id "
             "AND    o.o_w_id = s.s_w_id "
             "AND    o.o_orderline.ol_i_id = s.s_i_id "
             "AND    MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND    POSITION(SUBSTRING(c.c_addresses.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') = su.su_nationkey "
             "AND    POSITION(SUBSTRING(c.c_addresses.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') = n.n_nationkey "
             "AND    su.su_nationkey = n.n_nationkey "
             "AND    n.n_regionkey = r.r_regionkey "
             "AND    r.r_name = 'Asia' "
             "AND    o.o_entry_d >= '2016-01-01 00:00:00.000000' "
             "AND    o.o_entry_d < '2017-01-01 00:00:00.000000' "
           "GROUP BY n.n_name AS nname "
           "ORDER BY revenue DESC ",

    # Q06: Query lists the total amount of archived revenue from orderlines which
    # were delivered in a specific period and a certain quantity.
    "Q06": "SELECT SUM(o.o_orderline.ol_amount) as revenue "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE  o.o_orderline.ol_delivery_d >= '2016-01-01 00:00:00.000000' "
             "AND  o.o_orderline.ol_delivery_d < '2017-01-01 00:00:00.000000' "
             "AND  o.o_orderline.ol_amount > 600 ",

    # Q07: Query for showing the bi-directional trade volume between two given
    # nations sorted by their names and the considered years.
    "Q07": "SELECT supp_nation, cust_nation, l_year, "
	           "ROUND(SUM(o.o_orderline.ol_amount),2) AS revenue "
           "FROM   supplier su, stock s, "
                   "UNWIND (orders AS o WITH PATH => o_orderline), "
                   "UNWIND (customer AS c WITH PATH => c_addresses), "
                   "nation n1, nation n2 "
           "WHERE    o.o_orderline.ol_supply_w_id = s.s_w_id "
             "AND    o.o_orderline.ol_i_id = s.s_i_id "
             "AND    MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND    c.c_addresses.c_address_kind = 'shipping' "
             "AND    c.c_id = o.o_c_id "
             "AND    c.c_w_id = o.o_w_id "
             "AND    c.c_d_id = o.o_d_id "
             "AND    su.su_nationkey = n1.n_nationkey "
             "AND    POSITION(SUBSTRING(c.c_addresses.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') = n2.n_nationkey "
             "AND    ((n1.n_name = 'Germany' and n2.n_name = 'Cambodia') OR "
                     "(n1.n_name = 'Cambodia' and n2.n_name = 'Germany')) "
             "AND    o.o_orderline.ol_delivery_d BETWEEN '2017-01-01 00:00:00.000000' "
                                         "AND '2018-12-31 00:00:00.000000' "
           "GROUP BY su.su_nationkey AS supp_nation, "
                     "SUBSTRING(c.c_addresses.c_state,0,1) AS cust_nation, "
                     "EXTRACT(YEAR FROM CAST(o.o_entry_d AS TIMESTAMP)) AS l_year "
           "ORDER BY supp_nation, cust_nation, l_year ",

    # Q08: This query lists the market share of a given nation for customers from
    # a certain region in which kinds of items are "produced".
    "Q08": "SELECT l_year, "
                  "ROUND((SUM(CASE WHEN n2.n_name = 'Germany' "
                  "THEN o.o_orderline.ol_amount "
                  "ELSE 0 END) / SUM(o.o_orderline.ol_amount)),2) AS mkt_share "
           "FROM  item i, supplier su, stock s, "
                 "UNWIND (orders AS o WITH PATH => o_orderline), "
                 "UNWIND (customer AS c WITH PATH => c_addresses), "
                 "nation n1, nation n2, region r "
           "WHERE i.i_id = s.s_i_id "
             "AND o.o_orderline.ol_i_id = s.s_i_id "
             "AND o.o_orderline.ol_supply_w_id = s.s_w_id "
             "AND MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND c.c_id = o.o_c_id "
             "AND c.c_w_id = o.o_w_id "
             "AND c.c_d_id = o.o_d_id "
             "AND c.c_addresses.c_address_kind = 'shipping' "
             "AND n1.n_nationkey = POSITION(SUBSTRING(c.c_addresses.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') "
             "AND n1.n_regionkey = r.r_regionkey "
             "AND o.o_orderline.ol_i_id < 1000 "
             "AND r.r_name = 'Europe' "
             "AND su.su_nationkey = n2.n_nationkey "
             "AND o.o_entry_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000' "
             "AND i.i_data LIKE '%b' "
             "AND i.i_id = o.o_orderline.ol_i_id "
           "GROUP BY EXTRACT(YEAR FROM CAST(o.o_entry_d AS TIMESTAMP)) AS l_year "
           "ORDER BY l_year ",

    # Q09: This query describes how much profit has been made on a selection of
    # items for each nation and each year. The result list will be sorted by the
    # name of the nation and the financial year.
    "Q09": "SELECT  n_name, l_year, "
                   "SUM(o.o_orderline.ol_amount) AS sum_profit "
           "FROM    item i, stock s, supplier su, "
                   "UNWIND (orders AS o WITH PATH => o_orderline), nation n "
           "WHERE   o.o_orderline.ol_i_id = s.s_i_id "
             "AND    o.o_orderline.ol_supply_w_id = s.s_w_id "
             "AND    MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND    o.o_orderline.ol_i_id = i.i_id "
             "AND    su.su_nationkey = n.n_nationkey "
             "AND    i.i_data like '%bb' "
           "GROUP BY n.n_name AS n_name, "
                     "EXTRACT(YEAR FROM CAST(o.o_entry_d AS TIMESTAMP)) AS l_year "
           "ORDER BY n_name, l_year DESC ",
    # Q10: Query for analyzing the expenses of all customers listing their living
    # country, some detail of them and the amount of money which they have used
    # to take their orders since a specific date. The whole list is sorted by the
    # amount of the customers’ orders.
    "Q10": "SELECT cid, clast, SUM(o.o_orderline.ol_amount) AS revenue, "
                   "ccity, cphone, nname "
           "FROM UNWIND ((SELECT * FROM "
                "UNWIND (customer AS ca WITH PATH => c_addresses)) "
                        "AS c WITH PATH => c_phones), "
                "UNWIND (orders AS o WITH PATH => o_orderline), nation n "
           "WHERE  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND  c.c_d_id = o.o_d_id "
             "AND  o.o_entry_d >= '2015-10-01 00:00:00.000000' "
             "AND  o.o_entry_d < '2016-01-01 00:00:00.000000' "
             "AND  c.c_addresses.c_address_kind = 'shipping' "
             "AND  c.c_phones.c_phone_kind = 'contact' "
             "AND n.n_nationkey = POSITION(SUBSTRING(c.c_addresses.c_state,0,1) IN '##########%%%%%%%%%%##########%%%%%%%%%%########0123456789#######ABCDEFGHIJKLMNOPQRSTUVWXYZ%%%%%%abcdefghijklmnopqrstuvwxyz') "
           "GROUP BY c.c_id AS cid, c.c_name.c_last AS clast, c.c_addresses.c_city AS ccity, "
                    "c.c_phones.c_phone_number AS cphone, n.n_name AS nname "
           "ORDER BY revenue DESC "
           "LIMIT 20 ",

    # Q11: Most important items (items which are often involved in orders and
    # therefore often bought by customers) supplied by supplier of a given nation.
    "Q11": "SELECT s.s_i_id, SUM(s.s_order_cnt) as ordercount "
           "FROM   stock s,  supplier su, nation n "
           "WHERE  MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
             "AND  su.su_nationkey = n.n_nationkey "
             "AND  n.n_name = 'Germany' "
           "GROUP BY s.s_i_id "
           "HAVING SUM(s.s_order_cnt) > "
                  "(SELECT SUM(s1.s_order_cnt) * 0.00005 "
                   "FROM stock s1, supplier su1, nation n1 "
                   "WHERE MOD(s1.s_w_id * s1.s_i_id, 10000) = su1.su_suppkey "
                     "AND su1.su_nationkey = n1.n_nationkey "
                     "AND n1.n_name = 'Germany') "
           "ORDER BY ordercount DESC ",

    # Q12: This query counts the amount of orders grouped by the number of
    # orderlines in each order attending the number of orders which are shipped
    # with a higher or lower order priority.
    "Q12": "SELECT ol_cnt, "
                   "SUM (CASE WHEN o.o_carrier_id = 1 OR o.o_carrier_id = 2 "
                         "THEN 1 ELSE 0 END) AS high_line_COUNT, "
                   "SUM (CASE WHEN o.o_carrier_id <> 1 AND o.o_carrier_id <> 2 "
                         "THEN 1 ELSE 0 END) AS low_line_COUNT "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE  o.o_entry_d <= o.o_orderline.ol_delivery_d "
             "AND  o.o_orderline.ol_delivery_d >= '2016-01-01 00:00:00.000000' "
             "AND  o.o_orderline.ol_delivery_d < '2017-01-01 00:00:00.000000' "
           "GROUP BY o.o_ol_cnt AS ol_cnt "
           "ORDER BY ol_cnt ",

    # Q13: The query lists the number of customers grouped and sorted by the size
    # of orders they made. The result set of the relation between customers and
    # the size of their orders is sorted by the size of orders and counts how
    # many customers have dealt the same way.
    "Q13": "SELECT c_count, COUNT(*) AS custdist "
           "FROM  (SELECT c.c_id, COUNT(o.o_id) AS c_count "
                   "FROM customer c LEFT OUTER JOIN orders o "
                     "ON (c.c_w_id = o.o_w_id "
                    "AND c.c_d_id = o.o_d_id "
                    "AND c.c_id = o.o_c_id "
                    "AND o.o_carrier_id > 8) "
                   "GROUP BY c.c_id) as c_orders "
           "GROUP BY c_orders.c_count AS c_count "
           "ORDER BY custdist DESC, c_count DESC ",

    # Q14: The query result represents the percentage of the revenue in a period
    # of time which has been realized from promotional campaigns.
    "Q14": "SELECT 100.00 * SUM(CASE WHEN i.i_data LIKE 'pr%' "
                                "THEN o.o_orderline.ol_amount ELSE 0 END) / "
                                "(1+SUM(o.o_orderline.ol_amount)) AS promo_revenue "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline), item i "
           "WHERE o.o_orderline.ol_i_id = i.i_id "
             "AND o.o_orderline.ol_delivery_d >= '2017-09-01 00:00:00.000000' "
             "AND o.o_orderline.ol_delivery_d < '2017-10-01 00:00:00.000000' ",

    # Q15: This query finds the top supplier or suppliers who contributed the
    # most to the overall revenue for items shipped during a given period of time.
    "Q15": "SELECT su.su_suppkey, su.su_name, su.su_address, su.su_phone, r.total_revenue "
           "FROM supplier su, "
                "(SELECT supplier_no, SUM(o.o_orderline.ol_amount) AS total_revenue "
                 "FROM   UNWIND (orders AS o WITH PATH => o_orderline), stock s "
                 "WHERE o.o_orderline.ol_i_id = s.s_i_id "
                   "AND o.o_orderline.ol_supply_w_id = s.s_w_id "
                   "AND o.o_orderline.ol_delivery_d >= '2018-01-01 00:00:00.000000' "
                   "AND o.o_orderline.ol_delivery_d < '2018-04-01 00:00:00.000000' "
                 "GROUP BY MOD(s.s_w_id * s.s_i_id, 10000) AS supplier_no) AS r "
           "WHERE su.su_suppkey = r.supplier_no "
             "AND r.total_revenue = "
                  "(SELECT MAX(r1.total_revenue) "
                  "FROM (SELECT supplier_no, SUM(o.o_orderline.ol_amount) AS total_revenue "
                        "FROM UNWIND (orders AS o WITH PATH => o_orderline), stock s "
                        "WHERE o.o_orderline.ol_i_id = s.s_i_id "
                          "AND o.o_orderline.ol_supply_w_id = s.s_w_id "
                          "AND o.o_orderline.ol_delivery_d >= '2018-01-01 00:00:00.000000' "
                          "AND o.o_orderline.ol_delivery_d < '2018-04-01 00:00:00.000000' "
                        "GROUP BY MOD(s.s_w_id * s.s_i_id, 10000) AS supplier_no) AS r1) "
           "ORDER BY su.su_suppkey ",

    # Q16: This query finds out how many suppliers are able to supply items with
    # given attributes sorted in descending order of them. The result is grouped
    # by the identifier of the item.
    "Q16": "SELECT iname, brand, iprice, "
                   "COUNT(DISTINCT MOD((s.s_w_id * s.s_i_id), 10000)) AS supplier_cnt "
           "FROM stock s, item i "
           "WHERE i.i_id = s.s_i_id "
             "AND i.i_data NOT LIKE 'zz%' "
             "AND (MOD((s.s_w_id * s.s_i_id), 10000) NOT IN "
                                  "(SELECT su.su_suppkey "
                                   "FROM supplier su "
                                   "WHERE su.su_comment LIKE '%Customer%Complaints%')) "
           "GROUP BY i.i_name AS iname, "
                     "SUBSTRING(i.i_data, 0, 3) AS brand, i.i_price AS iprice "
           "ORDER BY supplier_cnt DESC ",

    # Q17: The query determines the yearly loss in revenue if orders just with a
    # quantity of more than the average quantity of all orders in the system
    # would be taken and shipped to customers.
    "Q17": "SELECT SUM(o.o_orderline.ol_amount) / 2.0 AS avg_yearly "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline), "
               "(SELECT iid, AVG(o1.o_orderline.ol_quantity) AS a "
                "FROM   item i, UNWIND (orders AS o1 WITH PATH => o_orderline) "
                "WHERE  i.i_data LIKE '%b' AND  o1.o_orderline.ol_i_id = i.i_id "
                "GROUP BY i.i_id AS iid) t "
           "WHERE o.o_orderline.ol_i_id = t.iid "
             "AND o.o_orderline.ol_quantity < t.a ",

    # Q18: Query 18 is ranking all customers who have ordered for more than a
    # specific amount of money.
    "Q18": "SELECT clast, c.c_id, o.o_id, o.o_entry_d, o.o_ol_cnt, "
                  "SUM(o.o_orderline.ol_amount) AS ol_sum "
           "FROM customer c, UNWIND (orders AS o WITH PATH => o_orderline) "
           "WHERE  c.c_id = o.o_c_id "
             "AND  c.c_w_id = o.o_w_id "
             "AND c.c_d_id = o.o_d_id "
           "GROUP BY o.o_id, o.o_w_id, o.o_d_id, c.c_id, c.c_name.c_last AS clast, o.o_entry_d, o.o_ol_cnt "
           "HAVING SUM(o.o_orderline.ol_amount) > 200 "
           "ORDER BY ol_sum DESC, o.o_entry_d  "
           "LIMIT 100 ",

    # Q19: The query is for reporting the revenue achieved by some specific
    # attributes, as the price, the detailed information of the item and the
    # quantity of the ordered amount of them.
    "Q19": "SELECT SUM(o.o_orderline.ol_amount) AS revenue "
           "FROM UNWIND (orders AS o WITH PATH => o_orderline), item i "
           "WHERE  (( "
                   "i.i_data LIKE '%h' "
                   "AND o.o_orderline.ol_quantity >= 7 "
                   "AND o.o_orderline.ol_quantity <= 17 "
                   "AND i.i_price between 1 AND 5 "
                   "AND o.o_w_id IN (37, 29, 70) "
                   ") OR ( "
                   "i.i_data LIKE '%t' "
                   "AND o.o_orderline.ol_quantity >= 16 "
                   "AND o.o_orderline.ol_quantity <= 26 "
                   "AND i.i_price between 1 AND 10 "
                   "AND o.o_w_id IN (78, 17, 6) "
                   ") OR ( "
                   "i.i_data LIKE '%m' "
                   "AND o.o_orderline.ol_quantity >= 24 "
                   "AND o.o_orderline.ol_quantity <= 34 "
                   "AND i.i_price between 1 AND 15 "
                   "AND  o.o_w_id IN (91, 95, 15) "
                   ")) "
             "AND o.o_orderline.ol_i_id = i.i_id "
             "AND i.i_price between 1 AND 15 ",

    # Q20: Suppliers in a particular nation having selected parts that may be
    # candidates for a promotional offer if the quantity of these items is more
    # than 50 percent of the total quantity which has been ordered since a certain date.
    "Q20": "SELECT su.su_name, su.su_address "
           "FROM   supplier su, nation n "
           "WHERE  su.su_suppkey IN "
                  "(SELECT MOD(s.s_i_id * s.s_w_id, 10000) "
                   "FROM   stock s, UNWIND (orders AS o WITH PATH => o_orderline) "
                   "WHERE  s.s_i_id IN (SELECT i.i_id "
                                       "FROM item i "
                                       "WHERE i.i_data LIKE 'co%') "
                     "AND  o.o_orderline.ol_i_id = s.s_i_id "
                     "AND  o.o_orderline.ol_delivery_d >= '2016-01-01 12:00:00' "
                     "AND  o.o_orderline.ol_delivery_d < '2017-01-01 12:00:00' "
                   "GROUP BY s.s_i_id, s.s_w_id, s.s_quantity "
                   "HAVING 20*s.s_quantity > SUM(o.o_orderline.ol_quantity)) "
             "AND su.su_nationkey = n.n_nationkey "
             "AND n.n_name = 'Germany' "
           "ORDER BY su.su_name ",

    # Q21: Query 21 determines the suppliers which have shipped some required
    # items of an order not in a timely manner for a given nation.
    "Q21": "SELECT z.su_name, COUNT (*) AS numwait "
           "FROM (SELECT x.su_name "
                 "FROM (SELECT o1.o_id, o1.o_w_id, o1.o_d_id, o1.o_orderline.ol_delivery_d, "
                              "n.n_nationkey, su.su_suppkey, s.s_w_id, s.s_i_id, su.su_name "
                       "FROM nation n, supplier su, stock s, "
                            "UNWIND (orders AS o1 WITH PATH => o_orderline) "
                       "WHERE o1.o_w_id = s.s_w_id "
                         "AND o1.o_orderline.ol_i_id = s.s_i_id "
                         "AND MOD(s.s_w_id * s.s_i_id, 10000) = su.su_suppkey "
                         "AND o1.o_orderline.ol_delivery_d > "
                             "CAST(DATEADD(day, 150, CAST(o1.o_entry_d AS TIMESTAMP)) AS STRING) "
                         "AND o1.o_entry_d BETWEEN '2017-12-01 00:00:00' "
                                              "AND '2017-12-31 00:00:00' "
                         "AND su.su_nationkey = n.n_nationkey "
                         "AND n.n_name = 'Peru' ) x "
                     "LEFT OUTER JOIN "
                      "(SELECT o2.o_id, o2.o_w_id, o2.o_d_id, o2.o_orderline.ol_delivery_d "
                       "FROM UNWIND (orders AS o2 WITH PATH => o_orderline) "
                       "WHERE o2.o_entry_d BETWEEN '2017-12-01 00:00:00' "
                                              "AND '2017-12-31 00:00:00' ) y "
                     "ON y.o_id = x.o_id "
                     "AND y.o_w_id = x.o_w_id "
                     "AND y.o_d_id = x.o_d_id "
                     "AND y.ol_delivery_d > x.ol_delivery_d "
                  "GROUP BY x.o_w_id, x.o_d_id, x.o_id, x.n_nationkey, "
                           "x.su_suppkey, x.s_w_id, x.s_i_id, x.su_name "
                  "HAVING COUNT (y.o_id) = 0) z "
           "GROUP BY z.su_name "
           "LIMIT 100 ",

    # Q22: This query lists how many customers within a specific range of country
    # codes have not bought anything for the whole period of time and who have a
    # greater than average balance on their account. The county code is represented
    # by the first two characters of the phone number.
    "Q22": "SELECT country, COUNT(*) AS numcust, SUM(c.c_balance) AS totacctbal "
           "FROM UNWIND ((SELECT * "
                         "FROM UNWIND (customer AS ca WITH PATH => c_addresses)) AS c WITH PATH => c_phones) "
           "WHERE SUBSTRING(c.c_phones.c_phone_number,0,1) IN "
                                             "('1','2','3','4','5','6','7') "
             "AND  c.c_addresses.c_address_kind = 'shipping' "
             "AND  c.c_phones.c_phone_kind = 'contact' "
             "AND c.c_balance > (SELECT AVG(c1.c_balance) "
                                "FROM UNWIND (customer AS c1 WITH PATH => c_phones) "
                                "WHERE c1.c_balance > 0.00 "
                                  "AND c1.c_phones.c_phone_kind = 'contact' "
                                  "AND SUBSTRING(c1.c_phones.c_phone_number,0,1) IN "
                                        "('1','2','3','4','5','6','7') ) "
             "AND NOT EXISTS (SELECT 1 "
                             "FROM orders o "
                             "WHERE o.o_c_id = c.c_id "
                               "AND o.o_w_id = c.c_w_id "
                               "AND o.o_d_id = c.c_d_id "
                               "AND o.o_entry_d BETWEEN '2013-12-01 00:00:00' AND '2013-12-31 00:00:00') "
           "GROUP BY SUBSTRING(c.c_addresses.c_state,0,1) AS country "
           "ORDER BY country "
}

CH2_QUERIES_PERM = [
    ["Q14", "Q02", "Q09", "Q20", "Q06", "Q17", "Q18", "Q08", "Q21", "Q13", "Q03", "Q22", "Q16", "Q04", "Q11", "Q15", "Q01", "Q10", "Q19", "Q05", "Q07", "Q12"],

    ["Q21", "Q03", "Q18", "Q05", "Q11", "Q07", "Q06", "Q20", "Q17", "Q12", "Q16", "Q15", "Q13", "Q10", "Q02", "Q08", "Q14", "Q19", "Q09", "Q22", "Q01", "Q04"],

    ["Q06", "Q17", "Q14", "Q16", "Q19", "Q10", "Q09", "Q02", "Q15", "Q08", "Q05", "Q22", "Q12", "Q07", "Q13", "Q18", "Q01", "Q04", "Q20", "Q03", "Q11", "Q21"],

    ["Q08", "Q05", "Q04", "Q06", "Q17", "Q07", "Q01", "Q18", "Q22", "Q14", "Q09", "Q10", "Q15", "Q11", "Q20", "Q02", "Q21", "Q19", "Q13", "Q16", "Q12", "Q03"],

    ["Q05", "Q21", "Q14", "Q19", "Q15", "Q17", "Q12", "Q06", "Q04", "Q09", "Q08", "Q16", "Q11", "Q02", "Q10", "Q18", "Q01", "Q13", "Q07", "Q22", "Q03", "Q20"],

    ["Q21", "Q15", "Q04", "Q06", "Q07", "Q16", "Q19", "Q18", "Q14", "Q22", "Q11", "Q13", "Q03", "Q01", "Q02", "Q05", "Q08", "Q20", "Q12", "Q17", "Q10", "Q09"],

    ["Q10", "Q03", "Q15", "Q13", "Q06", "Q08", "Q09", "Q07", "Q04", "Q11", "Q22", "Q18", "Q12", "Q01", "Q05", "Q16", "Q02", "Q14", "Q19", "Q20", "Q17", "Q21"],

    ["Q18", "Q08", "Q20", "Q21", "Q02", "Q04", "Q22", "Q17", "Q01", "Q11", "Q09", "Q19", "Q03", "Q13", "Q05", "Q07", "Q10", "Q16", "Q06", "Q14", "Q15", "Q12"],

    ["Q19", "Q01", "Q15", "Q17", "Q05", "Q08", "Q09", "Q12", "Q14", "Q07", "Q04", "Q03", "Q20", "Q16", "Q06", "Q22", "Q10", "Q13", "Q02", "Q21", "Q18", "Q11"],

    ["Q08", "Q13", "Q02", "Q20", "Q17", "Q03", "Q06", "Q21", "Q18", "Q11", "Q19", "Q10", "Q15", "Q04", "Q22", "Q01", "Q07", "Q12", "Q09", "Q14", "Q05", "Q16"],

    ["Q06", "Q15", "Q18", "Q17", "Q12", "Q01", "Q07", "Q02", "Q22", "Q13", "Q21", "Q10", "Q14", "Q09", "Q03", "Q16", "Q20", "Q19", "Q11", "Q04", "Q08", "Q05"],

    ["Q15", "Q14", "Q18", "Q17", "Q10", "Q20", "Q16", "Q11", "Q01", "Q08", "Q04", "Q22", "Q05", "Q12", "Q03", "Q09", "Q21", "Q02", "Q13", "Q06", "Q19", "Q07"],

    ["Q01", "Q07", "Q16", "Q17", "Q18", "Q22", "Q12", "Q06", "Q08", "Q09", "Q11", "Q04", "Q02", "Q05", "Q20", "Q21", "Q13", "Q10", "Q19", "Q03", "Q14", "Q15"],

    ["Q21", "Q17", "Q07", "Q03", "Q01", "Q10", "Q12", "Q22", "Q09", "Q16", "Q06", "Q11", "Q02", "Q04", "Q05", "Q14", "Q08", "Q20", "Q13", "Q18", "Q15", "Q19"],

    ["Q02", "Q09", "Q05", "Q04", "Q18", "Q01", "Q20", "Q15", "Q16", "Q17", "Q07", "Q21", "Q13", "Q14", "Q19", "Q08", "Q22", "Q11", "Q10", "Q03", "Q12", "Q06"],

    ["Q16", "Q09", "Q17", "Q08", "Q14", "Q11", "Q10", "Q12", "Q06", "Q21", "Q07", "Q03", "Q15", "Q05", "Q22", "Q20", "Q01", "Q13", "Q19", "Q02", "Q04", "Q18"],

    ["Q01", "Q03", "Q06", "Q05", "Q02", "Q16", "Q14", "Q22", "Q17", "Q20", "Q04", "Q09", "Q10", "Q11", "Q15", "Q08", "Q12", "Q19", "Q18", "Q13", "Q07", "Q21"],

    ["Q03", "Q16", "Q05", "Q11", "Q21", "Q09", "Q02", "Q15", "Q10", "Q18", "Q17", "Q07", "Q08", "Q19", "Q14", "Q13", "Q01", "Q04", "Q22", "Q20", "Q06", "Q12"],

    ["Q14", "Q04", "Q13", "Q05", "Q21", "Q11", "Q08", "Q06", "Q03", "Q17", "Q02", "Q20", "Q01", "Q19", "Q10", "Q09", "Q12", "Q18", "Q15", "Q07", "Q22", "Q16"],

    ["Q04", "Q12", "Q22", "Q14", "Q05", "Q15", "Q16", "Q02", "Q08", "Q10", "Q17", "Q09", "Q21", "Q07", "Q03", "Q06", "Q13", "Q18", "Q11", "Q20", "Q19", "Q01"],

    ["Q16", "Q15", "Q14", "Q13", "Q04", "Q22", "Q18", "Q19", "Q07", "Q01", "Q12", "Q17", "Q05", "Q10", "Q20", "Q03", "Q09", "Q21", "Q11", "Q02", "Q06", "Q08"],

    ["Q20", "Q14", "Q21", "Q12", "Q15", "Q17", "Q04", "Q19", "Q13", "Q10", "Q11", "Q01", "Q16", "Q05", "Q18", "Q07", "Q08", "Q22", "Q09", "Q06", "Q03", "Q02"],

    ["Q16", "Q14", "Q13", "Q02", "Q21", "Q10", "Q11", "Q04", "Q01", "Q22", "Q18", "Q12", "Q19", "Q05", "Q07", "Q08", "Q06", "Q03", "Q15", "Q20", "Q09", "Q17"],

    ["Q18", "Q15", "Q09", "Q14", "Q12", "Q02", "Q08", "Q11", "Q22", "Q21", "Q16", "Q01", "Q06", "Q17", "Q05", "Q10", "Q19", "Q04", "Q20", "Q13", "Q03", "Q07"],

    ["Q07", "Q03", "Q10", "Q14", "Q13", "Q21", "Q18", "Q06", "Q20", "Q04", "Q09", "Q08", "Q22", "Q15", "Q02", "Q01", "Q05", "Q12", "Q19", "Q17", "Q11", "Q16"],

    ["Q18", "Q01", "Q13", "Q07", "Q16", "Q10", "Q14", "Q02", "Q19", "Q05", "Q21", "Q11", "Q22", "Q15", "Q08", "Q17", "Q20", "Q03", "Q04", "Q12", "Q06", "Q09"],

    ["Q13", "Q02", "Q22", "Q05", "Q11", "Q21", "Q20", "Q14", "Q07", "Q10", "Q04", "Q09", "Q19", "Q18", "Q06", "Q03", "Q01", "Q08", "Q15", "Q12", "Q17", "Q16"],

    ["Q14", "Q17", "Q21", "Q08", "Q02", "Q09", "Q06", "Q04", "Q05", "Q13", "Q22", "Q07", "Q15", "Q03", "Q01", "Q18", "Q16", "Q11", "Q10", "Q12", "Q20", "Q19"],

    ["Q10", "Q22", "Q01", "Q12", "Q13", "Q18", "Q21", "Q20", "Q02", "Q14", "Q16", "Q07", "Q15", "Q03", "Q04", "Q17", "Q05", "Q19", "Q06", "Q08", "Q09", "Q11"],

    ["Q10", "Q08", "Q09", "Q18", "Q12", "Q06", "Q01", "Q05", "Q20", "Q11", "Q17", "Q22", "Q16", "Q03", "Q13", "Q02", "Q15", "Q21", "Q14", "Q19", "Q07", "Q04"],

    ["Q07", "Q17", "Q22", "Q05", "Q03", "Q10", "Q13", "Q18", "Q09", "Q01", "Q14", "Q15", "Q21", "Q19", "Q16", "Q12", "Q08", "Q06", "Q11", "Q20", "Q04", "Q02"],

    ["Q02", "Q09", "Q21", "Q03", "Q04", "Q07", "Q01", "Q11", "Q16", "Q05", "Q20", "Q19", "Q18", "Q08", "Q17", "Q13", "Q10", "Q12", "Q15", "Q06", "Q14", "Q22"],

    ["Q15", "Q12", "Q08", "Q04", "Q22", "Q13", "Q16", "Q17", "Q18", "Q03", "Q07", "Q05", "Q06", "Q01", "Q09", "Q11", "Q21", "Q10", "Q14", "Q20", "Q19", "Q02"],

    ["Q15", "Q16", "Q02", "Q11", "Q17", "Q07", "Q05", "Q14", "Q20", "Q04", "Q21", "Q03", "Q10", "Q09", "Q12", "Q08", "Q13", "Q06", "Q18", "Q19", "Q22", "Q01"],

    ["Q01", "Q13", "Q11", "Q03", "Q04", "Q21", "Q06", "Q14", "Q15", "Q22", "Q18", "Q09", "Q07", "Q05", "Q10", "Q20", "Q12", "Q16", "Q17", "Q08", "Q19", "Q02"],

    ["Q14", "Q17", "Q22", "Q20", "Q08", "Q16", "Q05", "Q10", "Q01", "Q13", "Q02", "Q21", "Q12", "Q09", "Q04", "Q18", "Q03", "Q07", "Q06", "Q19", "Q15", "Q11"],

    ["Q09", "Q17", "Q07", "Q04", "Q05", "Q13", "Q21", "Q18", "Q11", "Q03", "Q22", "Q01", "Q06", "Q16", "Q20", "Q14", "Q15", "Q10", "Q08", "Q02", "Q12", "Q19"],

    ["Q13", "Q14", "Q05", "Q22", "Q19", "Q11", "Q09", "Q06", "Q18", "Q15", "Q08", "Q10", "Q07", "Q04", "Q17", "Q16", "Q03", "Q01", "Q12", "Q02", "Q21", "Q20"],

    ["Q20", "Q05", "Q04", "Q14", "Q11", "Q01", "Q06", "Q16", "Q08", "Q22", "Q07", "Q03", "Q02", "Q12", "Q21", "Q19", "Q17", "Q13", "Q10", "Q15", "Q18", "Q09"],

    ["Q03", "Q07", "Q14", "Q15", "Q06", "Q05", "Q21", "Q20", "Q18", "Q10", "Q04", "Q16", "Q19", "Q01", "Q13", "Q09", "Q08", "Q17", "Q11", "Q12", "Q22", "Q02"],

    ["Q13", "Q15", "Q17", "Q01", "Q22", "Q11", "Q03", "Q04", "Q07", "Q20", "Q14", "Q21", "Q09", "Q08", "Q02", "Q18", "Q16", "Q06", "Q10", "Q12", "Q05",  "Q19"]
]

