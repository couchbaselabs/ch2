-- Query 1
-- This query reports the total amount and quantity of all shipped orderlines 
-- given by a specific time period. Additionally it informs about the average 
-- amount and quantity plus the total count of all these orderlines ordered by 
-- the individual orderline number.

define DAYS = random(180, 240, uniform);
define START_DATE = "2014-01-01";

SELECT   ol.ol_number,
         SUM(ol.ol_quantity) AS sum_qty,
         SUM(ol.ol_amount) AS sum_amount,
         AVG(ol.ol_quantity) AS avg_qty,
         AVG(ol.ol_amount) AS avg_amount,
         COUNT(*) AS count_order
FROM     orders o, o.o_orderline ol
WHERE    ol.ol_delivery_d > DATE_ADD_STR('[START_DATE]', [DAYS], 'day')
GROUP BY ol.ol_number 
ORDER BY ol.ol_number;
