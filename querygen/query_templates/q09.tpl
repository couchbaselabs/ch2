-- Query 9
-- This query describes how much profit has been made on a selection of items for
-- each nation and each year. The result list will be sorted by the name of the
-- nation and the financial year.

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
		    
SELECT   n.n_name, DATE_PART_STR(o.o_entry_d, 'year') AS l_year, 
         SUM(ol.ol_amount) AS SUM_profit
FROM     item i, stock s, supplier su, orders o,  o.o_orderline ol, nation n
WHERE    ol.ol_i_id = s.s_i_id
  AND    ol.ol_supply_w_id = s.s_w_id
  AND    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey
  AND    ol.ol_i_id = i.i_id
  AND    su.su_nationkey = n.n_nationkey
  AND    i.i_data LIKE '%[IDATAA][IDATAB]'
GROUP BY n.n_name, DATE_PART_STR(o.o_entry_d, 'year')
ORDER BY n.n_name, l_year DESC;
