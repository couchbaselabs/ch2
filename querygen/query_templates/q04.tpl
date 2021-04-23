-- Query 4
-- This query is listing all orders with orderlines or just parts of them shipped
-- after the entry date of their booking.

define STARTYEAR = 2014;
define ORDERYEAR = random([STARTYEAR]+1, [STARTYEAR]+5, uniform);
define ORDERMONTH = text({"01", 1}, {"02", 1}, {"03", 1}, {"04", 1}, {"05", 1},
                         {"06", 1}, {"07", 1}, {"08", 1}, {"09", 1}, {"10", 1},
                         {"11", 1}, {"12", 1});
define ORDERDAY = "01";

SELECT   o.o_ol_cnt, COUNT(*) AS order_count
FROM     orders o
WHERE    o.o_entry_d >= '[ORDERYEAR]-[ORDERMONTH]-[ORDERDAY] 00:00:00.000000'
  AND    o.o_entry_d < DATE_ADD_STR('[ORDERYEAR]-[ORDERMONTH]-[ORDERDAY] 00:00:00.000000', 3, 'month')
  AND    EXISTS (SELECT VALUE 1
                 FROM   o.o_orderline ol
                 WHERE  ol.ol_delivery_d >= DATE_ADD_STR(o.o_entry_d, 1, 'week'))
GROUP BY o.o_ol_cnt
ORDER BY o.o_ol_cnt;
