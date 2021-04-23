-- Query 16
-- This query finds out how many suppliers are able to supply items with given
-- attributes sorted in descending order of them. The result is grouped by the
-- identifier of the item.

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
define SU_COMMENT_PREFIX = "Customer";
define SU_COMMENT_SUFFIX = "Complaints";

SELECT	 i.i_name,
	 SUBSTR1(i.i_data, 1, 3) AS brand,
	 i.i_price,
	 COUNT(DISTINCT(s.s_w_id * s.s_i_id MOD 10000)) AS supplier_cnt
FROM	 stock s, item i
WHERE	 i.i_id = s.s_i_id
	 AND i.i_data NOT LIKE '[IDATAA][IDATAB]%'
	 AND s.s_w_id * s.s_i_id MOD 10000 NOT IN
             (SELECT su.su_suppkey
	      FROM   supplier su
	      WHERE  su.su_comment LIKE '%[SU_COMMENT_PREFIX]%[SU_COMMENT_SUFFIX]%')
GROUP BY i.i_name, SUBSTR1(i.i_data, 1, 3), i.i_price
ORDER BY supplier_cnt DESC;
