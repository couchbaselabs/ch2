-- Query 21 determines the suppliers which have shipped some required items of an
-- order not in a timely manner for a given nation.

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

define STARTYEAR = 2014;
define ENDYEAR = 2020;
define ORDERYEAR = random([STARTYEAR], [ENDYEAR], uniform);
define ORDERMONTH = "12";
define STARTORDERDAY = "01";
define ENDORDERDAY = "31";
define NUMDAYS = 150;

SELECT   su.su_name, COUNT(*) AS numwait
FROM     supplier su, orders o1, o1.o_orderline ol1, stock s, nation n
WHERE    o1.o_w_id = s.s_w_id
  AND    ol1.ol_i_id = s.s_i_id
  AND    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey
  AND    o1.o_entry_d between '[ORDERYEAR]-[ORDERMONTH]-[STARTORDERDAY] 00:00:00' AND '[ORDERYEAR]-[ORDERMONTH]-[ENDORDERDAY] 00:00:00'
  AND    ol1.ol_delivery_d > DATE_ADD_STR(o1.o_entry_d, [NUMDAYS], 'day')
  AND    NOT EXISTS (SELECT VALUE 1
	             FROM   orders o2, o2.o_orderline ol2
	             WHERE  o2.o_id = o1.o_id
		       AND  o2.o_w_id = o1.o_w_id
		       AND  o2.o_d_id = o1.o_d_id
		       AND  ol2.ol_delivery_d > ol1.ol_delivery_d)
  AND    su.su_nationkey = n.n_nationkey
  AND    n.n_name = '[NNAME]'
GROUP BY su.su_name
ORDER BY numwait DESC, su.su_name
LIMIT    100;
