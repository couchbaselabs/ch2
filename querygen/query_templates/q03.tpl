-- Query 3
-- Undelivered orders with the highest price amount for a customer will be listed
-- within a given state and as of a specific timestamp. This list will be sorted
-- by the descending amount.

define CSTATE = text({"a", 1}, {"b", 1}, {"c", 1}, {"d", 1}, {"e", 1}, {"f", 1},
                     {"g", 1}, {"h", 1}, {"i", 1}, {"j", 1}, {"k", 1}, {"l", 1},
                     {"m", 1}, {"n", 1}, {"o", 1}, {"p", 1}, {"q", 1}, {"r", 1},
                     {"s", 1}, {"t", 1}, {"u", 1}, {"v", 1}, {"w", 1}, {"x", 1},
                     {"y", 1}, {"z", 1},
		     {"A", 1}, {"B", 1}, {"C", 1}, {"D", 1}, {"E", 1}, {"F", 1},
                     {"G", 1}, {"H", 1}, {"I", 1}, {"J", 1}, {"K", 1}, {"L", 1},
                     {"M", 1}, {"N", 1}, {"O", 1}, {"P", 1}, {"Q", 1}, {"R", 1},
                     {"S", 1}, {"T", 1}, {"U", 1}, {"V", 1}, {"W", 1}, {"X", 1},
                     {"Y", 1}, {"Z", 1},
		     {"0", 1}, {"1", 1}, {"2", 1}, {"3", 1}, {"4", 1}, {"5", 1},
                     {"6", 1}, {"7", 1}, {"8", 1}, {"9", 1});
define ENDYEAR = 2020;
define STARTYEAR = 2014;
define YEAR = [STARTYEAR]+[ENDYEAR];
define ORDERYEAR = [YEAR]/2;
define ORDERMONTH = "03";
define ORDERDAY = text({"01", 1}, {"02", 1}, {"03", 1}, {"04", 1}, {"05", 1},
                       {"06", 1}, {"07", 1}, {"08", 1}, {"09", 1}, {"10", 1},
                       {"11", 1}, {"12", 1}, {"13", 1}, {"14", 1}, {"15", 1},
                       {"16", 1}, {"17", 1}, {"18", 1}, {"19", 1}, {"20", 1},
                       {"21", 1}, {"22", 1}, {"23", 1}, {"24", 1}, {"25", 1},
                       {"26", 1}, {"27", 1}, {"28", 1}, {"29", 1}, {"30", 1},
                       {"31", 1});

SELECT   o.o_id, o.o_w_id, o.o_d_id,
         SUM(ol.ol_amount) AS revenue, o.o_entry_d
FROM     customer c,  neworder no, orders o, o.o_orderline ol
WHERE    c.c_state LIKE '[CSTATE]%'
  AND    c.c_id = o.o_c_id
  AND    c.c_w_id = o.o_w_id
  AND    c.c_d_id = o.o_d_id
  AND    no.no_w_id = o.o_w_id
  AND    no.no_d_id = o.o_d_id
  AND    no.no_o_id = o.o_id
  AND    o.o_entry_d < '[ORDERYEAR]-[ORDERMONTH]-[ORDERDAY] 00:00:00.000000'
GROUP BY o.o_id, o.o_w_id, o.o_d_id, o.o_entry_d
ORDER BY revenue DESC, o.o_entry_d
LIMIT    10;
