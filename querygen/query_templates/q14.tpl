-- Query 14
-- The query result represents the percentage of the revenue in a period of time
-- which has been realized from promotional campaigns.

define STARTYEAR = 2014;
define ORDERLINEYEAR = random([STARTYEAR]+1, [STARTYEAR]+5, uniform);
define ORDERLINEMONTH = text({"01", 1}, {"02", 1}, {"03", 1}, {"04", 1}, {"05", 1},
                         {"06", 1}, {"07", 1}, {"08", 1}, {"09", 1}, {"10", 1},
                         {"11", 1}, {"12", 1});
define ORDERLINEDAY = "01";

SELECT 100.00 * SUM(CASE WHEN i.i_data LIKE 'PR%' THEN  
                    ol.ol_amount ELSE 0 END) / 
                    (1+SUM(ol.ol_amount)) AS promo_revenue
FROM   orders o, o.o_orderline ol, item i
WHERE  ol.ol_i_id = i.i_id
  AND  ol.ol_delivery_d >= '[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000'
  AND  ol.ol_delivery_d < DATE_ADD_STR('[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000', 1, 'month');
