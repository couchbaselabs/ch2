-- Query 17
-- The query determines the yearly loss in revenue if orders just with a quantity
-- of more than the average quantity of all orders in the system would be taken
-- and shipped to customers.

define IDATA = text({"a", 1}, {"b", 1}, {"c", 1}, {"d", 1}, {"e", 1}, {"f", 1},
                    {"g", 1}, {"h", 1}, {"i", 1}, {"j", 1}, {"k", 1}, {"l", 1},
                    {"m", 1}, {"n", 1}, {"o", 1}, {"p", 1}, {"q", 1}, {"r", 1},
                    {"s", 1}, {"t", 1}, {"u", 1}, {"v", 1}, {"w", 1}, {"x", 1},
                    {"y", 1}, {"z", 1});

SELECT SUM(ol.ol_amount) / 2.0 AS avg_yearly
FROM   orders o, o.o_orderline ol, (SELECT   i.i_id, AVG(ol1.ol_quantity) AS a
                                    FROM     item i, orders o1, o1.o_orderline ol1
                                    WHERE    i.i_data LIKE '%[IDATA]'
                                      AND    ol1.ol_i_id = i.i_id
                                    GROUP BY i.i_id) t 
WHERE  ol.ol_i_id = t.i_id
  AND  ol.ol_quantity < t.a;
