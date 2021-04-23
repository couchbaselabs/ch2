-- Query 7
-- Query for showing the bi-directional trade volume between two given nations
-- sorted by their names and the considered years.

define NNAMEA =
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
define NNAMEB =
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
define STARTORDERLINEYEAR = [STARTYEAR]+3;
define STARTORDERLINEMONTH = "01";
define STARTORDERLINEDAY = "01";
define ENDORDERLINEYEAR = [STARTYEAR]+4;
define ENDORDERLINEMONTH = "12";
define ENDORDERLINEDAY = "31";
define SQBRB = "[";
define SQBRE = "]";

SELECT   su.su_nationkey AS supp_nation,
         SUBSTR1(c.c_state,1,1) AS cust_nation,
         DATE_PART_STR(o.o_entry_d, 'year') AS l_year,
         SUM(ol.ol_amount) AS revenue
FROM     supplier su, stock s, orders o, o.o_orderline ol, customer c, nation n1, nation n2
WHERE    ol.ol_supply_w_id = s.s_w_id
  AND    ol.ol_i_id = s.s_i_id
  AND    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey
  AND    c.c_id = o.o_c_id
  AND    c.c_w_id = o.o_w_id
  AND    c.c_d_id = o.o_d_id
  AND    su.su_nationkey = n1.n_nationkey
  AND    string_to_codepoint(c.c_state)[SQBRB]0[SQBRE] = n2.n_nationkey
  AND    ((n1.n_name = '[NNAMEA]' AND n2.n_name = '[NNAMEB]')
	 OR
	  (n1.n_name = '[NNAMEB]' AND n2.n_name = '[NNAMEA]'))
  AND    ol.ol_delivery_d BETWEEN '[STARTORDERLINEYEAR]-[STARTORDERLINEMONTH]-[STARTORDERLINEDAY] 00:00:00.000000' AND '[ENDORDERLINEYEAR]-[ENDORDERLINEMONTH]-[ENDORDERLINEDAY] 00:00:00.000000' 
GROUP BY su.su_nationkey, SUBSTR1(c.c_state,1,1), DATE_PART_STR(o.o_entry_d, 'year')
ORDER BY su.su_nationkey, cust_nation, l_year;
