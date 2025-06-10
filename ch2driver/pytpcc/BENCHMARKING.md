# Benchmarking Couchbase Capella with CH2++

## Deploy Infrastructure

### Workload Driver Node

Deploy an AWS EC2 instance on which the CH2 benchmark code will be installed and executed.

>[!NOTE]
> These instructions talk about AWS infrastructure, but everything here can be done equivalently on GCP and Azure too.

Recommendations:

- Use a compute-optimized instance type with >=16vCPUs for faster data loading
- Use a recent OS like Debian 12, Ubuntu 24 or Amazon Linux 2023
- Only a small amount of disk space is necessary so there is no need to provision an extra data disk. Using a 20GB boot disk only will be sufficient.

### Couchbase Capella

Two Couchbase Capella clusters need to be deployed:

- One Capella Operational cluster into which data will be loaded and which will run transactions.
- One Capella Columnar cluster which will be ingesting data from the Operational cluster and running analytical queries.

Deployment instructions (using example cluster configurations):

1. Create a new Capella Project
2. Create a Capella Operational cluster in the Project:
   - “Custom” cluster option
   - 1 service group:
     - Data, Query and Index services
     - 4 nodes, 8vCPUs 32GB RAM
     - GP3 disk, 500GB, 16000 IOPS
3. Create a Capella Columnar cluster in the Project:
   - 4 nodes, 8vCPUs 32GB RAM

Both clusters should be deployed in the **same AWS region as the driver node**.

## Configure Database

### Capella Operational

#### Configure Allowed IPs

Add the IP address of the driver node as an Allowed IP. This will allow connections (e.g. through an SDK) to the cluster from the driver node.

Docs: [Configure Allowed IP Addresses | Couchbase Docs](https://docs.couchbase.com/cloud/clusters/allow-ip-address.html#add-allowed-ip)

#### Configure Cluster Access Credentials

Create a set of cluster access credentials with Read/Write access to all buckets and all scopes. These will be used for authentication when the CH2++ driver connects to the cluster to load data.

Docs: [Configure Cluster Access Credentials | Couchbase Docs](https://docs.couchbase.com/cloud/clusters/manage-database-users.html#create-database-credentials)

#### Create Bucket, Scopes and Collections

Create a bucket with the following settings:

- Name: **bench**
- Memory quota: **maximum possible**
- Bucket type: **Memory and Disk**
- Storage Backend: **Magma**
- Conflict Resolution: **Sequence Number**
- Minimum Durability Level: **None**
- Number of Replicas: **1**
- Flush: **On**
- Time to Live: **Off**

Docs: [Manage Buckets | Couchbase Docs](https://docs.couchbase.com/cloud/clusters/data-service/manage-buckets.html#add-bucket)

Create the following scopes and collections in the bucket **bench**:

- Scope: **ch2pp**
  - Collections:
    - **item**
    - **warehouse**
    - **district**
    - **customer**
    - **stock**
    - **orders**
    - **neworder**
    - **history**
    - **supplier**
    - **nation**
    - **region**

This can be done via the UI or by running the following SQL++ for Query statements Query Workbench:

```sql
CREATE SCOPE bench.ch2pp;
CREATE COLLECTION bench.ch2pp.item;
CREATE COLLECTION bench.ch2pp.warehouse;
...
```

Docs:

- [Manage Scopes and Collections | Couchbase Docs](https://docs.couchbase.com/cloud/clusters/data-service/scopes-collections.html)
- [CREATE SCOPE | Couchbase Docs](https://docs.couchbase.com/cloud/n1ql/n1ql-language-reference/createscope.html)
- [CREATE COLLECTION | Couchbase Docs](https://docs.couchbase.com/cloud/n1ql/n1ql-language-reference/createcollection.html)

#### [Optional] Create Secondary Indexes

In the Query Workbench, run the following index creation statements separately:

```sql
CREATE INDEX cu_w_id_d_id_last
    ON bench.ch2pp.customer(c_w_id, c_d_id, c_last) USING GSI;

CREATE INDEX di_id_w_id ON bench.ch2pp.district(d_id, d_w_id) USING GSI;

CREATE INDEX no_o_id_d_id_w_id
    ON bench.ch2pp.neworder(no_o_id, no_d_id, no_w_id) USING GSI;

CREATE INDEX or_id_d_id_w_id_c_id
    ON bench.ch2pp.orders(o_id, o_d_id, o_w_id, o_c_id) USING GSI;

CREATE INDEX or_w_id_d_id_c_id
    ON bench.ch2pp.orders(o_w_id, o_d_id, o_c_id) USING GSI;

CREATE INDEX wh_id ON bench.ch2pp.warehouse(w_id) USING GSI;
```

### Capella Columnar

#### Configure Allowed IPs

Add the IP address of the driver node as an Allowed IP. This will allow connections (e.g. through an SDK) to the cluster from the driver node.

Docs: [Configure Allowed IP Addresses | Couchbase Docs](https://docs.couchbase.com/columnar/admin/ip-allowed-list.html#add-allowed-ip)

#### Create an Access Control Account

Create a new access control account for the cluster and assign it the **sys_data_admin** role. The credentials for this account will be used for authentication when the CH2++ driver connects to the cluster to run analytical queries.

Docs: [Manage Access to Cluster Data | Couchbase Docs](https://docs.couchbase.com/columnar/admin/auth/auth-data.html)

#### Set up Remote Link to the Capella Operational cluster

This allows data to be streamed from the Capella Operational cluster to the Columnar cluster so that analytical queries can be executed on it.

Create the remote link by following the instructions in the docs: [Stream Data from Couchbase Capella](https://docs.couchbase.com/columnar/sources/remote-cb-capella.html)

Create a new database called **bench** and a new scope called **ch2pp** on the Columnar cluster. Then create one linked collection for each collection in bucket **bench**, scope **ch2pp** on the Capella Operational cluster.

Finally, **connect the link**.

#### [Optional] Create Secondary Indexes

If using analytics secondary indexes for the benchmark, these can be created now and will be updated incrementally as documents are loaded later.

In the Columnar Workbench UI, run the following index creation statements separately:

```sql
CREATE INDEX customer_c_balance ON customer(c_balance:DOUBLE);

CREATE INDEX orders_entry_d ON orders(o_entry_d:STRING);

CREATE INDEX orderline_i_id
    ON orders(UNNEST o_orderline SELECT ol_i_id:BIGINT)
    EXCLUDE UNKNOWN KEY;

CREATE INDEX orderline_delivery_d
    ON orders(UNNEST o_orderline SELECT ol_delivery_d:STRING)
    EXCLUDE UNKNOWN KEY;
```

## Install CH2++ Driver

All commands executed in this section must be executed **on the driver node**.

For the commands themselves, see [`./README.md`](./README.md#installation)

## Load Data

All commands executed in this section must be executed **on the driver node**.

First, change into the directory where the CH2++ driver executable is:

```bash
cd ch2/ch2driver/pytpcc
```

### Run Data Loading Command

Run the following command (correctly replacing any placeholder values specified with <>) to load data into the Capella Operational cluster. We use nohup here and run it in the background as this could take several hours if the dataset is large (e.g. 1000's of warehouses):

```none
nohup python ./tpcc.py nestcollections \
    --tls \
    --userid <OPERATIONAL CLUSTER USERNAME> \
    --password <OPERATIONAL CLUSTER PASSWORD> \
    --data-url <OPERATIONAL DATA NODE HOSTNAME 1> \
    --multi-data-url <COMMA-SEPARATED LIST OF DATA NODE HOSTNAMES> \
    --starting_warehouse 1 \
    --warehouses 1000 \
    --datagenSeed 12345 \
    --tclients <NUMBER OF LOCAL CPUS> \
    --no-execute \
    --datasvc-bulkload \
    --ch2pp \
    --customerExtraFields 64 \
    --ordersExtraFields 64 \
    --itemExtraFields 64 > ch2_load.log &
```

Explanation:

- `nestcollections` refers to the CH2 driver implementation that should be used to load documents or run analytical queries. This is the one that must be used for running the benchmark against Couchbase clusters with nested JSON data.
- `--tls` specifies that TLS connections should be made to the Couchbase clusters. This is necessary when connecting to Capella clusters.
- `--userid` and --password specify the credentials for the cluster running the Data service, which in our case is the Capella Operational cluster.
- `--userid-analytics` and `--password-analytics` specify the credentials for the cluster to which analytical queries will be sent. In our case this is the Capella Columnar cluster.
- `--data-url` and `--multi-data-url` specify the hostnames/IPs of the Data service nodes.
- The CH2 data schema imitates that of an inventory management system, and the primary way to control the size of the dataset is by setting the number of warehouses. This is done with the `--starting_warehouse` and `--warehouses` flags. We recommend keeping `--starting_warehouse` at 1 and varying `--warehouses`.
- `--datagenSeed` sets the random seed for data generation. For consistency and reproducibility, we recommend using the same seed value for all benchmark runs.
- `--tclients` controls the number of “transactional” clients which, in this case, are used to load data. A new subprocess is created for each client. We recommend setting this to the number of CPU cores on the driver node.
- `--no-execute` specifies that the driver should not execute the benchmark. By default, the driver will load data and then execute the benchmark, so specifying this by itself tells the driver to only load data.
- `--ch2pp` specifies that the full CH2++ data schema should be used (as opposed to the CH2 schema).
- `--datasvc-bulkload` specifies the loading method where documents are loaded in batches into the Data service. This is the fastest method.
- `--customerExtraFields`, `--ordersExtraFields` and `--itemExtraFields` specify the number of extra, unused fields that should be added in the documents of the customer, orders and item collections respectively. In other words, it controls the width of the schemas for these collections. We recommend setting each of these to 64.

### Verify Data

Verify that the correct number of documents have been loaded into the Capella Operational cluster and have been subsequently ingested by the Capella Columnar cluster.

The following table shows the number of documents expected in each of the collections, depending on the number of warehouses W:

| Collection | Documents   |
|------------|------------|
| warehouse  | W          |
| district   | 10 * W     |
| history    | 30K * W    |
| neworder   | 9K * W     |
| stock      | 100K * W   |
| customer   | 30K * W    |
| orders     | 30K * W    |
| item       | 100K       |
| supplier   | 10K        |
| nation     | 62         |
| region     | 5          |

For the Capella Operational cluster, the number of documents in each collection is shown in the Capella UI in the Data Tools > Documents tab.

For the Capella Columnar cluster, these numbers can be verified by running the following analytical query for each collection:

```sql
SELECT COUNT(*) FROM `<collection>`
```

If the document counts are correct on the Capella Operational cluster but less than expected on the Columnar cluster, this may be because data ingestion is still in progress. This can be verified by checking the document count again to see if it is increasing. Wait until all the data is ingested before continuing to the next step (running the benchmark).

## Run Benchmark

### Analyze Analytics Collections for CBO

For the Columnar Cost-Based Optimizer to be used, all the analytics collections need to be “analyzed” to collect the statistics that the optimizer will use to tune queries.

In the Columnar Workbench UI, run the following ANALYZE statements separately for each collection:

```sql
ANALYZE ANALYTICS COLLECTION `item` WITH { "sample": "high" };
ANALYZE ANALYTICS COLLECTION `warehouse` WITH { "sample": "high" };
...
```

### Run Benchmark Command

All commands executed in this section must be executed **on the driver node**.

First, change into the directory where the CH2++ driver executable is:

```bash
cd ch2/ch2driver/pytpcc
```

Run the following command (correctly replacing any placeholder values specified with <>) to run the analytics-only CH2++ benchmark. We use nohup here and run it in the background as this could take several hours if the dataset is large (e.g. 1000's of warehouses). We also direct the output to a file to save the benchmark results:

```none
nohup python ./tpcc.py nestcollections \
    --tls \
    --userid <OPERATIONAL CLUSTER USERNAME> \
    --password <OPERATIONAL CLUSTER PASSWORD> \
    --userid-analytics <COLUMNAR CLUSTER USERNAME> \
    --password-analytics <COLUMNAR CLUSTER PASSWORD> \
    --query-url <OPERATIONAL QUERY NODE HOSTNAME 1>:18093 \
    --multi-query-url <OPERATIONAL QUERY NODE HOSTNAME 1>:18093,<OPERATIONAL QUERY NODE HOSTNAME 2>:18093,<...> \
    --analytics-url <COLUMNAR NODE HOSTNAME>:18095 \
    --warehouses 1000 \
    --tclients 16 \
    --aclients 1 \
    --query-iterations 2 \
    --warmup-query-iterations 1 \
    --no-load \
    --ch2pp \
    --nonOptimizedQueries > ch2_mixed.log &
```

Explanation (for arguments not already explained in [Run Data Loading Command](#run-data-loading-command)):

- `--analytics-url` specifies the hostname/IP and port combination to use as the target for submitting analytical queries. For Capella Columnar, the relevant port is 18095, and the hostname is that of one of the cluster nodes. The hostnames of all the cluster nodes look something like `svc-da-node-001.abcdefghij123456.cloud.couchbase.com` and can be found by running one of the following commands, where `<CONNECTION STRING HOSTNAME>` is the part of the cluster connection string that comes after `couchbases://` (this looks like `cb.abcdefghij123456.cloud.couchbase.com`):

    ```bash
    nslookup -type=SRV _couchbases._tcp.<CONNECTION STRING HOSTNAME>

    dig -t SRV +short _couchbases._tcp.<CONNECTION STRING HOSTNAME>
    ```

- `--tclients` specifies the number of “transactional” clients which in this case will submit transactional queries on the Capella Operational cluster.
- `--aclients` specifies the number of “analytical” clients which will submit analytical queries to the target database. This can be set to >1 to investigate how the target database handles concurrent query requests.
- `--query-iterations` and `--warmup-query-iterations` specify how many times the 22 analytical queries will be executed, and which executions count towards the final benchmark results. The queries are executed in “loops”, where each loop comprises all 22 queries. This loop is repeated `--query-iterations` times. We suggest keeping `--query-iterations 2` `--warmup-query-iterations 1` which means that 2 query loops will be executed in total, and the first one is a “warmup” loop and will not count towards the final results.
- `--no-load` specifies that the driver should not load data. By default the driver will load data and then execute the benchmark, so specifying this by itself tells the driver to only execute the benchmark.
- `--nonOptimizedQueries` specifies that the driver should submit non-hand-optimized (“naive”) analytical queries to the cluster. These queries will be optimized automatically by the Cost-Based Optimizer.

After the benchmark has finished, the results can be viewed in the `ch2_mixed.log` file that the above command pipes its output to.
