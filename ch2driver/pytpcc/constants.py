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
TABLENAME_ITEM       = "default:bench.ch2.item"
TABLENAME_WAREHOUSE  = "default:bench.ch2.warehouse"
TABLENAME_DISTRICT   = "default:bench.ch2.district"
TABLENAME_CUSTOMER   = "default:bench.ch2.customer"
TABLENAME_STOCK      = "default:bench.ch2.stock"
TABLENAME_ORDERS     = "default:bench.ch2.orders"
TABLENAME_NEWORDER   = "default:bench.ch2.neworder"
TABLENAME_ORDERLINE  = "default:bench.ch2.orderline"
TABLENAME_HISTORY    = "default:bench.ch2.history"
TABLENAME_SUPPLIER   = "default:bench.ch2.supplier"
TABLENAME_NATION     = "default:bench.ch2.nation"
TABLENAME_REGION     = "default:bench.ch2.region"

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
           "WHERE ol.ol_delivery_d > '2014-07-01 00:00:00' "\
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
            "WHERE  c.c_state LIKE 'A%' "\
              "AND c.c_id = o.o_c_id AND c.c_w_id = o.o_w_id AND c.c_d_id = o.o_d_id "\
              "AND o.o_entry_d < '2017-03-15 00:00:00.000000') "\
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
                     "AND o.o_entry_d BETWEEN '2017-01-01 00:00:00.000000' AND '2018-12-31 00:00:00.000000') rn1cooli "\
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
