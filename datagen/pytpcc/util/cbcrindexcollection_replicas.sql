drop index CUSTOMER.CU_W_ID_D_ID_LAST USING GSI
drop index DISTRICT.DI_ID_W_ID USING GSI
drop index NEW_ORDER.D_ID_W_ID_O_ID USING GSI
drop index ORDERS.OR_O_ID_D_ID_W_ID USING GSI
drop index ORDERS.OR_W_ID_D_ID_C_ID USING GSI
drop index ORDER_LINE.OL_O_ID_D_ID_W_ID USING GSI
drop index WAREHOUSE.WH_ID USING GSI
drop primary index on CUSTOMER USING GSI
drop primary index on DISTRICT USING GSI
drop primary index on HISTORY USING GSI
drop primary index on ITEM USING GSI
drop primary index on NEW_ORDER USING GSI
drop primary index on ORDERS USING GSI
drop primary index on ORDER_LINE USING GSI
drop primary index on STOCK USING GSI
drop primary index on WAREHOUSE USING GSI
CREATE INDEX CU_W_ID_D_ID_LAST on CUSTOMER(C_W_ID, C_D_ID, C_LAST) USING GSI WITH {"defer_build": true, "num_replica":replicas}
CREATE INDEX DI_ID_W_ID on DISTRICT(D_ID, D_W_ID) USING GSI WITH {"defer_build": true, "num_replica":replicas}
CREATE INDEX D_ID_W_ID_O_ID on NEW_ORDER(NO_D_ID, NO_W_ID, NO_O_ID) USING GSI WITH {"defer_build": true, "num_replica":replicas}
CREATE INDEX OR_DID_WID_ID_CID on ORDERS(O_D_ID, O_W_ID, O_ID, O_C_ID) USING GSI WITH {"defer_build": true, "num_replica":replicas}
CREATE INDEX OR_CID_DID_WID_ID_CAID_EID on ORDERS(O_C_ID, O_D_ID, O_W_ID, O_ID DESC, O_CARRIER_ID, O_ENTRY_D) USING GSI WITH {"defer_build": true, "num_replica":replicas}
CREATE INDEX OL_O_ID_D_ID_W_ID on ORDER_LINE(OL_O_ID, OL_D_ID, OL_W_ID) USING GSI WITH {"defer_build": true, "num_replica":replicas}
CREATE INDEX WH_ID on WAREHOUSE(W_ID) USING GSI WITH {"defer_build": true, "num_replica":replicas}
select keyspace_id, state from system:indexes
select keyspace_id, state from system:indexes where state != 'online'
