-- Query 10
-- Query for analyzing the expenses of all customers listing their living country,
-- some detail of them and the amount of money which they have used to take their
-- orders since a specific date. The whole list is sorted by the amount of the
-- customers’ orders.

define STARTYEAR = 2014;
define ORDERYEAR = random([STARTYEAR]+1, [STARTYEAR]+3, uniform);
define ORDERMONTH = text({"01", 1}, {"02", 1}, {"03", 1}, {"04", 1}, {"05", 1},
                         {"06", 1}, {"07", 1}, {"08", 1}, {"09", 1}, {"10", 1},
                         {"11", 1}, {"12", 1});
define ORDERDAY = "01";
define SQBRB = "[";
define SQBRE = "]";

SELECT   c.c_id, c.c_last, SUM(ol.ol_amount) AS revenue, c.c_city, c.c_phone, n.n_name
FROM     customer c, orders o, o.o_orderline ol, nation n
WHERE    c.c_id = o.o_c_id
  AND    c.c_w_id = o.o_w_id
  AND    c.c_d_id = o.o_d_id
  AND    o.o_entry_d >= '[ORDERYEAR]-[ORDERMONTH]-[ORDERDAY] 00:00:00.000000'
  AND    o.o_entry_d < DATE_ADD_STR('[ORDERYEAR]-[ORDERMONTH]-[ORDERDAY] 00:00:00.000000', 3, 'month')
  AND    n.n_nationkey = string_to_codepoint(c.c_state)[SQBRB]0[SQBRE]
GROUP BY c.c_id, c.c_last, c.c_city, c.c_phone, n.n_name
ORDER BY revenue DESC
LIMIT    20;
