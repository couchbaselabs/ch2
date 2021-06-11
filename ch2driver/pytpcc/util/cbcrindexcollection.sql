drop index cu_w_id_d_id_last on default.tpcc.customer USING GSI
drop index di_id_w_id on default.tpcc.district USING GSI
drop index no_o_id_d_id_w_id on default.tpcc.neworder USING GSI
drop index or_id_d_id_w_id_c_id on default.tpcc.orders USING GSI
drop index or_w_id_d_id_c_id on default.tpcc.orders USING GSI
drop index wh_id on USING GSI default.tpcc.warehouse USING GSI

drop primary index on default.tpcc.customer USING GSI
drop primary index on default.tpcc.district USING GSI
drop primary index on default.tpcc.history USING GSI
drop primary index on default.tpcc.item USING GSI
drop primary index on default.tpcc.neworder USING GSI
drop primary index on default.tpcc.orders USING GSI
drop primary index on default.tpcc.stock USING GSI
drop primary index on default.tpcc.warehouse USING GSI 
create index cu_w_id_d_id_last on default.tpcc.customer(c_w_id, c_d_id, c_last) using gsi 
create index di_id_w_id on default.tpcc.district(d_id, d_w_id) using gsi
create index no_o_id_d_id_w_id on default.tpcc.neworder(no_o_id, no_d_id, no_w_id) using gsi 
create index or_id_d_id_w_id_c_id on default.tpcc.orders(o_id, o_d_id, o_w_id, o_c_id) using gsi 
create index or_w_id_d_id_c_id on default.tpcc.orders(o_w_id, o_d_id, o_c_id) using gsi 
create index wh_id on default.tpcc.warehouse(w_id) using gsi 
select keyspace_id, state from system:indexes
select keyspace_id, state from system:indexes where state != 'online'
