-- Query 5
-- Query result for getting information about achieved revenues of nations within
-- a given region. All nations are sorted by the total amount of revenue gained
-- since the given date.

define RNAME = text({"Africa", 1}, {"America", 1}, {"Asia", 1}, {"Europe", 1}, {"Middle East", 1});
define STARTYEAR = 2014;
define ORDERYEAR = random([STARTYEAR]+1, [STARTYEAR]+5, uniform);
define ORDERMONTH = "01";
define ORDERDAY = "01";
define SQBRB = "[";
define SQBRE = "]";

SELECT   n.n_name,
         SUM(ol.ol_amount) AS revenue
FROM     customer c, orders o, o.o_orderline ol, stock s, supplier su, nation n, region r
WHERE    c.c_id = o.o_c_id
  AND    c.c_w_id = o.o_w_id
  AND    c.c_d_id = o.o_d_id
  AND    o.o_w_id = s.s_w_id
  AND    ol.ol_i_id = s.s_i_id
  AND    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey
  AND    string_to_codepoint(c.c_state)[SQBRB]0[SQBRE] = su.su_nationkey
  AND    su.su_nationkey = n.n_nationkey 
  AND    n.n_regionkey = r.r_regionkey
  AND    r.r_name = '[RNAME]'
  AND    o.o_entry_d >= '[ORDERYEAR]-[ORDERMONTH]-[ORDERDAY] 00:00:00.000000'
  AND    o.o_entry_d < DATE_ADD_STR('[ORDERYEAR]-[ORDERMONTH]-[ORDERDAY] 00:00:00.000000', 1, 'year')
GROUP BY n.n_name
ORDER BY revenue DESC;
