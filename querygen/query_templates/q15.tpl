-- Query 15
-- This query finds the top supplier or suppliers who contributed the most to the
-- overall revenue for items shipped during a given period of time.

define STARTYEAR = 2014;
define ORDERLINEYEAR = random([STARTYEAR]+1, [STARTYEAR]+5, uniform);
define ORDERLINEMONTH = text({"01", 1}, {"02", 1}, {"03", 1}, {"04", 1}, {"05", 1},
                         {"06", 1}, {"07", 1}, {"08", 1}, {"09", 1}, {"10", 1},
                         {"11", 1}, {"12", 1});
define ORDERLINEDAY = "01";
define SQBRB = "[";
define SQBRE = "]";

WITH     revenue AS (
           SELECT   s.s_w_id * s.s_i_id MOD 10000 AS supplier_no,
                    SUM(ol.ol_amount) AS total_revenue
           FROM     orders o, o.o_orderline ol, stock s
           WHERE    ol.ol_i_id = s.s_i_id 
             AND    ol.ol_supply_w_id = s.s_w_id
             AND    ol.ol_delivery_d >= '[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000'
             AND    ol.ol_delivery_d < DATE_ADD_STR('[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000', 3, 'month')
           GROUP BY s.s_w_id * s.s_i_id MOD 10000)
SELECT   su.su_suppkey, su.su_name, su.su_address, su.su_phone, r.total_revenue
FROM     supplier su, revenue r
WHERE    su.su_suppkey = r.supplier_no
  AND    r.total_revenue = (SELECT VALUE max(r1.total_revenue) FROM revenue r1)[SQBRB]0[SQBRE]
ORDER BY su.su_suppkey;
