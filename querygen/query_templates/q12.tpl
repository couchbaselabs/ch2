-- Query 12
-- This query counts the amount of orders grouped by the number of orderlines in
-- each order attending the number of orders which are shipped with a higher or
-- lower order priority.

define STARTYEAR = 2014;
define ORDERLINEYEAR = random([STARTYEAR]+1, [STARTYEAR]+5, uniform);
define ORDERLINEMONTH = "01";
define ORDERLINEDAY = "01";
define SQBRB = "[";
define SQBRE = "]";

SELECT   o.o_ol_cnt,
         SUM (CASE WHEN o.o_carrier_id = 1 OR o.o_carrier_id = 2 
              THEN 1 ELSE 0 END) AS high_line_count,
         SUM (CASE WHEN o.o_carrier_id <> 1 AND o.o_carrier_id <> 2 
              THEN 1 ELSE 0 END) AS low_line_count
FROM     orders o, o.o_orderline ol
WHERE    o.o_entry_d <= ol.ol_delivery_d 
  AND    ol.ol_delivery_d >= '[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000' 
  AND    o.ol_delivery_d < DATE_ADD_STR('[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000', 1, 'year')
GROUP BY o.o_ol_cnt
ORDER BY o.o_ol_cnt;
