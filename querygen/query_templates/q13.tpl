-- Query 13
-- The query lists the number of customers grouped and sorted by the size of orders
-- they made. The result set of the relation between customers and the size of their
-- orders is sorted by the size of orders and counts how many customers have dealt
-- the same way.

define OCARRIERID = random(5, 10, uniform);

SELECT   c_orders.c_count, COUNT(*) AS custdist
FROM     (SELECT c.c_id, COUNT(o.o_id) AS c_count
          FROM customer c LEFT OUTER JOIN orders o ON (
                 c.c_w_id = o.o_w_id
                 AND c.c_d_id = o.o_d_id
                 AND c.c_id = o.o_c_id
                 AND o.o_carrier_id > [OCARRIERID])
          GROUP BY c.c_id) AS c_orders 
GROUP BY c_orders.c_count
ORDER BY custdist DESC, c_orders.c_count DESC;
