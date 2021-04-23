-- Query 19
-- The query is for reporting the revenue achieved by some specific attributes, as
-- the price, the detailed information of the item and the quantity of the ordered
-- amount of them.

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
define IDATAC = text({"a", 1}, {"b", 1}, {"c", 1}, {"d", 1}, {"e", 1}, {"f", 1},
                    {"g", 1}, {"h", 1}, {"i", 1}, {"j", 1}, {"k", 1}, {"l", 1},
                    {"m", 1}, {"n", 1}, {"o", 1}, {"p", 1}, {"q", 1}, {"r", 1},
                    {"s", 1}, {"t", 1}, {"u", 1}, {"v", 1}, {"w", 1}, {"x", 1},
                    {"y", 1}, {"z", 1});
define OLQUANTITYASTART = random(1, 10, uniform);
define OLQUANTITYAEND = [OLQUANTITYASTART] + 10;
define OLQUANTITYBSTART = random(10, 20, uniform);
define OLQUANTITYBEND = [OLQUANTITYBSTART] + 10;
define OLQUANTITYCSTART = random(20, 30, uniform);
define OLQUANTITYCEND = [OLQUANTITYCSTART] + 10;
define _SCALE = 100;
define OLWID = list(random(1, [_SCALE], uniform), 9);

define SQBRB = "[";
define SQBRE = "]";

SELECT SUM(ol.ol_amount) AS revenue
FROM   orders o, o.o_orderline ol, item i
WHERE  (
         ol.ol_i_id = i.i_id
         AND i.i_data LIKE '%[IDATAA]'
         AND ol.ol_quantity >= [OLQUANTITYASTART]
         AND ol.ol_quantity <= [OLQUANTITYAEND]
         AND i.i_price between 1 AND 5
         AND o.o_w_id IN [SQBRB][OLWID.1], [OLWID.2], [OLWID.3][SQBRE]
       ) OR (
         ol.ol_i_id = i.i_id
         AND i.i_data LIKE '%[IDATAB]'
         AND ol.ol_quantity >= [OLQUANTITYBSTART]
         AND ol.ol_quantity <= [OLQUANTITYBEND]
         AND i.i_price between 1 AND 10
         AND o.o_w_id IN [SQBRB][OLWID.4], [OLWID.5], [OLWID.6][SQBRE]
       ) OR (
         ol.ol_i_id = i.i_id
         AND i.i_data LIKE '%[IDATAC]'
         AND ol.ol_quantity >= [OLQUANTITYCSTART]
         AND ol.ol_quantity <= [OLQUANTITYCEND]
         AND i.i_price between 1 AND 15
         AND  o.o_w_id IN [SQBRB][OLWID.7], [OLWID.8], [OLWID.9][SQBRE]
       );
