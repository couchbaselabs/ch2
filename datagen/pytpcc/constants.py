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

# Table Names
TABLENAME_ITEM       = "default:default.tpcc.item"
TABLENAME_WAREHOUSE  = "default:default.tpcc.warehouse"
TABLENAME_DISTRICT   = "default:default.tpcc.district"
TABLENAME_CUSTOMER   = "default:default.tpcc.customer"
TABLENAME_STOCK      = "default:default.tpcc.stock"
TABLENAME_ORDERS     = "default:default.tpcc.orders"
TABLENAME_NEWORDER   = "default:default.tpcc.neworder"
TABLENAME_ORDERLINE  = "orderline"
TABLENAME_HISTORY    = "default:default.tpcc.history"
TABLENAME_SUPPLIER   = "default:default.tpcc.supplier"
TABLENAME_NATION     = "default:default.tpcc.nation"
TABLENAME_REGION     = "default:default.tpcc.region"

ALL_TABLES = [
    TABLENAME_ITEM,
    TABLENAME_WAREHOUSE,
    TABLENAME_DISTRICT,
    TABLENAME_CUSTOMER,
    TABLENAME_STOCK,
    TABLENAME_ORDERS,
    TABLENAME_NEWORDER,
    TABLENAME_ORDERLINE,
    TABLENAME_HISTORY,
    TABLENAME_SUPPLIER,
    TABLENAME_NATION,
    TABLENAME_REGION,
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
