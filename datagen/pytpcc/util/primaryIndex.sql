# Not used for py-tpcc
create primary index PX_CUSTOMER on CUSTOMER using gsi ;
create primary index PX_DISTRICT on DISTRICT using gsi ;
create primary index PX_HISTORY on HISTORY using gsi;
create primary index PX_ITEM on ITEM using gsi ;
create primary index PX_NEW_ORDER on NEW_ORDER using gsi ;
create primary index PX_ORDERS on ORDERS using gsi ;
create primary index PX_ORDER_LINE on ORDER_LINE using gsi ;
create primary index PX_STOCK on STOCK using gsi ;
create primary index PX_WAREHOUSE on WAREHOUSE using gsi ;