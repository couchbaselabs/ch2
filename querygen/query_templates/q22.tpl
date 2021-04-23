-- Query 22
-- This query lists how many customers within a specific range of country codes
-- have not bought anything for the whole period of time and who have a greater
-- than average balance on their account. The county code is represented by the
-- first two characters of the phone number.

define CCA = ulist(random(1, 10, uniform), 7);
define CCB = ulist(random(1, 10, uniform), 7);
define SQBRB = "[";
define SQBRE = "]";

SELECT   SUBSTR1(c.c_state,1,1) AS country,
         COUNT(*) AS numcust,
         SUM(c.c_balance) AS totacctbal
FROM     customer c
WHERE    SUBSTR1(c.c_phone,1,1) in [SQBRB]'[CCA.1]','[CCA.2]','[CCA.3]','[CCA.4]','[CCA.5]','[CCA.6]','[CCA.7]'[SQBRE]
  AND    c.c_balance > (SELECT VALUE AVG(c1.c_balance)
                        FROM customer c1
                        WHERE c1.c_balance > 0.00
                          AND SUBSTR1(c1.c_phone,1,1) in [SQBRB]'[CCB.1]','[CCB.2]','[CCB.3]','[CCB.4]','[CCB.5]','[CCB.6]','[CCB.7]'[SQBRE])[SQBRB]0[SQBRE]
  AND    NOT EXISTS (SELECT VALUE 1
                     FROM orders o
                     WHERE o.o_c_id = c.c_id
                       AND o.o_w_id = c.c_w_id
                       AND o.o_d_id = c.c_d_id)
GROUP BY SUBSTR1(c.c_state,1,1)
ORDER BY SUBSTR1(c.c_state,1,1);
