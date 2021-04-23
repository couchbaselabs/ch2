-- Query 20
-- Suppliers in a particular nation having selected parts that may be candidates
-- for a promotional offer if the quantity of these items is more than 50 percent
-- of the total quantity which has been ordered since a certain date.

define IDATAA = text({"a", 1}, {"b", 1}, {"c", 1}, {"d", 1}, {"e", 1}, {"f", 1},
                     {"g", 1}, {"h", 1}, {"i", 1}, {"j", 1}, {"k", 1}, {"l", 1},
                     {"m", 1}, {"n", 1}, {"o", 1}, {"p", 1}, {"q", 1}, {"r", 1},
                     {"s", 1}, {"t", 1}, {"u", 1}, {"v", 1}, {"w", 1}, {"x", 1},
                     {"y", 1}, {"z", 1});
define IDATAB = text({"a", 1}, {"b", 1}, {"c", 1}, {"d", 1}, {"e", 1}, {"f", 1},
                     {"g", 1}, {"h", 1}, {"i", 1}, {"j", 1}, {"k", 1}, {"l", 1},
                     {"m", 1}, {"n", 1}, {"o", 1}, {"p", 1}, {"q", 1}, {"r", 1},
                     {"s", 1}, {"t", 1}, {"u", 1}, {"v", 1}, {"w", 1}, {"x", 1},
                     {"y", 1}, {"z", 1});
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
define ORDERLINEYEAR = random([STARTYEAR]+1, [STARTYEAR]+5, uniform);
define ORDERLINEMONTH = "01";
define ORDERLINEDAY = "01";

SELECT   su.su_name, su.su_address
FROM     supplier su, nation n
WHERE    su.su_suppkey in
          (SELECT   VALUE s.s_i_id * s.s_w_id MOD 10000
           FROM     stock s, orders o, o.o_orderline ol
           WHERE    s.s_i_id in
                      (SELECT VALUE i.i_id
                       FROM item i
                       WHERE i.i_data LIKE '[IDATAA][IDATAB]%')
             AND    ol.ol_i_id=s.s_i_id
             AND    ol.ol_delivery_d >= '[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000' 
             AND    o.ol_delivery_d < DATE_ADD_STR('[ORDERLINEYEAR]-[ORDERLINEMONTH]-[ORDERLINEDAY] 00:00:00.000000', 1, 'year')
           GROUP BY s.s_i_id, s.s_w_id, s.s_quantity
           HAVING   20*s.s_quantity > SUM(ol.ol_quantity))
  AND    su.su_nationkey = n.n_nationkey
  AND    n.n_name = '[NNAME]'
ORDER BY su.su_name;
