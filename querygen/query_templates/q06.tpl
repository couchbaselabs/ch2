-- Query 6
-- Query lists the total amount of archived revenue from orderlines which were
-- delivered in a specific period and a certain quantity.

define STARTYEAR = 2014;
define ORDERLINEYEAR = random([STARTYEAR]+1, [STARTYEAR]+5, uniform);
define ORDERLINEMONTH = "01";
define ORDERLINEDAY = "01";
define OLAMOUNT = random(500, 700, uniform);

SELECT SUM(ol.ol_amount) AS revenue
FROM   orders o, o.o_orderline ol
WHERE  ol.ol_delivery_d >= '[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000'
  AND  ol.ol_delivery_d < DATE_ADD_STR('[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000', 1, 'year')
  AND  ol.ol_amount > [OLAMOUNT];
