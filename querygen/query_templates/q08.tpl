-- Query 8
-- This query lists the market share of a given nation for customers from a certain
-- region in which kinds of items are "produced".

define STARTYEAR = 2014;
define STARTORDERYEAR = [STARTYEAR]+3;
define STARTORDERMONTH = "01";
define STARTORDERDAY = "01";
define ENDORDERYEAR = [STARTYEAR]+4;
define ENDORDERMONTH = "12";
define ENDORDERDAY = "31";
define SQBRB = "[";
define SQBRE = "]";

-- For now, until I figure out how to specify dependencies in dsqgen
define RNAME = text({"Europe", 1});
define NNAME =
	text({"France", 1}, {"Germany", 1}, {"Russia", 1}, {"United Kingdom", 1},
             {"Italy", 1},  {"Spain", 1}, {"Ukraine", 1}, {"Netherlands", 1},
	     {"Belgium", 1}, {"Greece", 1}, {"Finland", 1}, {"Norway", 1});

define IDATA = text({"a", 1}, {"b", 1}, {"c", 1}, {"d", 1}, {"e", 1}, {"f", 1},
                    {"g", 1}, {"h", 1}, {"i", 1}, {"j", 1}, {"k", 1}, {"l", 1},
                    {"m", 1}, {"n", 1}, {"o", 1}, {"p", 1}, {"q", 1}, {"r", 1},
                    {"s", 1}, {"t", 1}, {"u", 1}, {"v", 1}, {"w", 1}, {"x", 1},
                    {"y", 1}, {"z", 1});
define OLIID = 1000;

SELECT   DATE_PART_STR(o.o_entry_d, 'year') AS l_year,
         SUM(CASE WHEN n2.n_name = '[NNAME]' THEN ol.ol_amount 
             ELSE 0 END) / SUM(ol.ol_amount) AS mkt_share
FROM     item i, supplier su, stock s, orders o, o.o_orderline ol, customer c, nation n1, nation n2, region r
WHERE    i.i_id = s.s_i_id
  AND    ol.ol_i_id = s.s_i_id
  AND    ol.ol_supply_w_id = s.s_w_id
  AND    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey
  AND    c.c_id = o.o_c_id
  AND    c.c_w_id = o.o_w_id
  AND    c.c_d_id = o.o_d_id
  AND    n1.n_nationkey = string_to_codepoint(c.c_state)[SQBRB]0[SQBRE]
  AND    n1.n_regionkey = r.r_regionkey
  AND    ol.ol_i_id < [OLIID]
  AND    r.r_name = '[RNAME]'
  AND    su.su_nationkey = n2.n_nationkey
  AND    o.o_entry_d BETWEEN '[STARTORDERYEAR]-[STARTORDERMONTH]-[STARTORDERDAY]-00:00:00.000000' AND '[ENDORDERYEAR]-[ENDORDERMONTH]-[ENDORDERDAY]-00:00:00.000000'
  AND    i.i_data LIKE '%[IDATA]' 
  AND    i.i_id = ol.ol_i_id
GROUP BY DATE_PART_STR(o.o_entry_d, 'year')
ORDER BY l_year;
