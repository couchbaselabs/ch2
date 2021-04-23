-- Query 2
-- Query for listing suppliers and their distributed items having the lowest stock
-- level for a certain item and certain region.

define RNAME = text({"Africa", 1}, {"America", 1}, {"Asia", 1}, {"Europe", 1}, {"Middle East", 1});
define IDATA = text({"a", 1}, {"b", 1}, {"c", 1}, {"d", 1}, {"e", 1}, {"f", 1},
                    {"g", 1}, {"h", 1}, {"i", 1}, {"j", 1}, {"k", 1}, {"l", 1},
                    {"m", 1}, {"n", 1}, {"o", 1}, {"p", 1}, {"q", 1}, {"r", 1},
                    {"s", 1}, {"t", 1}, {"u", 1}, {"v", 1}, {"w", 1}, {"x", 1},
                    {"y", 1}, {"z", 1});

SELECT   su.su_suppkey, su.su_name, n.n_name, i.i_id, i.i_name,
         su.su_address, su.su_phone, su.su_comment 
FROM     item i, supplier su, stock s, nation n, region r,
         (SELECT   s1.s_i_id AS m_i_id, MIN(s1.s_quantity) AS m_s_quantity
          FROM     stock s1, supplier su1, nation n1, region r1  
          WHERE    s1.s_w_id*s1.s_i_id MOD 10000 = su1.su_suppkey
            AND    su1.su_nationkey=n1.n_nationkey
            AND    n1.n_regionkey=r1.r_regionkey
            AND    r1.r_name LIKE '[RNAME]%'
          GROUP BY s1.s_i_id) m
WHERE    i.i_id = s.s_i_id
  AND    s.s_w_id * s.s_i_id MOD 10000 = su.su_suppkey
  AND    su.su_nationkey = n.n_nationkey
  AND    n.n_regionkey = r.r_regionkey
  AND    i.i_data LIKE '%[IDATA]'
  AND    r.r_name LIKE '[RNAME]%'
  AND    i.i_id=m.m_i_id
  AND    s.s_quantity = m.m_s_quantity
ORDER BY n.n_name, su.su_name, i.i_id
LIMIT    100;
