-- Query 11
-- Most important items (items which are often involved in orders and therefore
-- often bought by customers) supplied by supplier of a given nation.

define NNAME =
	text({"Algeria", 1}, {"Argentina", 1}, {"Brazil", 1}, {"Canada", 1}, 
             {"Egypt", 1}, {"Ethiopia", 1}, {"France", 1}, {"Germany", 1},
             {"India", 1}, {"Indonesia", 1}, {"Iran", 1}, {"Iraq", 1}, {"Japan", 1},
             {"Jordan", 1}, {"Kenya", 1}, {"Morocco", 1}, {"Mozambique", 1},
             {"Peru", 1}, {"China", 1}, {"Kuwait", 1}, {"Saudi Arabia", 1},
             {"Vietnam", 1}, {"Russia", 1}, {"United Kingdom", 1},
	     {"United States", 1}, {"Lebanon", 1}, {"Oman", 1}, {"Qatar", 1},
             {"Mexico", 1}, {"Turkey", 1}, {"Chile", 1}, {"Italy", 1}, 
             {"South Africa", 1}, {"South Korea", 1}, {"Colombia", 1}, {"Spain", 1},
             {"Ukraine", 1}, {"Ecuador", 1}, {"Sudan", 1}, {"Uzbekistan", 1},
             {"Malaysia", 1}, {"Venezuela", 1}, {"Tanzania", 1}, {"Afghanistan", 1},
             {"North Korea", 1}, {"Taiwan", 1}, {"Ghana", 1}, {"Ivory Coast", 1}, 
             {"Syria", 1}, {"Madagascar", 1}, {"Cameroon", 1}, {"Nigeria", 1},
             {"Bolivia", 1}, {"Netherlands", 1}, {"Cambodia", 1}, {"Belgium", 1},
             {"Greece", 1}, {"Uruguay", 1}, {"Israel", 1}, {"Finland", 1}, 
             {"Singapore", 1}, {"Norway", 1});

define FRACTION = 5;
define _SCALE = 100;
define SQBRB = "[";
define SQBRE = "]";

SELECT   s.s_i_id, SUM(s.s_order_cnt) AS ordercount
FROM     stock s, supplier su, nation n
WHERE    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey
  AND    su.su_nationkey = n.n_nationkey
  AND    n.n_name = '[NNAME]'
GROUP BY s.s_i_id
HAVING   SUM(s.s_order_cnt) >
             (SELECT VALUE SUM(s1.s_order_cnt) * 0.00[FRACTION]/[_SCALE]
              FROM   stock s1, supplier su1, nation n1
              WHERE  s1.s_w_id * s1.s_i_id MOD 10000 = su1.su_suppkey
                AND  su1.su_nationkey = n1.n_nationkey
                AND  n1.n_name = '[NNAME]')[SQBRB]0[SQBRE]
ORDER BY ordercount DESC; 
