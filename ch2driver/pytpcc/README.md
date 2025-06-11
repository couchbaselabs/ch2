# Getting Started

Examples use Couchbase as the target database as the Couchbase driver is the most up-to-date and maintained.

## Installation

Requirements:

- Python >= 3.9

Clone the CH2++ git repository:

```bash
git clone https://github.com/couchbaselabs/ch2.git
```

**[Optional, recommended]** Create a Python virtual environment in the repo directory:

```bash
python -m venv venv
source venv/bin/activate
```

Install Python module dependencies:

```bash
python -m pip install -r requirements.txt
```

***

## Cluster Setup (Couchbase Capella)

For running the benchmark with Couchbase Capella you will need to set up a Capella Operational cluster with the Data, Query and Index services as well as a Capella Columnar cluster.

After deploying the two clusters, you will need to:

1. On the Operational cluster, create the necessary bucket, scope and collections.
2. **[Optional, highly recommended]** On the Operational cluster, create secondary indexes.
3. On the Columnar cluster, create a link to the Operational cluster.
4. On the Columnar cluster, create the necessary analytics collections.
5. **[Optional, recommended]** On the Columnar cluster, create secondary indexes.

For the specific setup details for running the benchmark with Couchbase Capella, read [`BENCHMARKING.md`](./BENCHMARKING.md).

## Loading data

Example command to load data (CH2++64 with 10 warehouses) into a Couchbase Capella Operational cluster with 4 processes:

```[bash]
python ./tpcc.py nestcollections \
    --userid <USERNAME> \
    --password '<PASSWORD>' \
    --tls \
    --data-url <CLUSTER NODE HOSTNAME 1> \
    --multi-data-url <CLUSTER NODE HOSTNAME 1>,<CLUSTER NODE HOSTNAME 2>,<...> \
    --starting_warehouse 1 \
    --warehouses 10 \
    --tclients 4 \
    --no-execute \
    --datasvc-bulkload \
    --ch2pp \
    --customerExtraFields 64 \
    --ordersExtraFields 64 \
    --itemExtraFields 64
```

## Running the benchmark

Example command to run the full CH2++ benchmark against a Couchbase Capella Operational cluster connected to a Couchbase Capella Columnar cluster:

```[bash]
python ./tpcc.py nestcollections \
    --userid <OPERATIONAL CLUSTER USERNAME> \
    --password '<OPERATIONAL CLUSTER PASSWORD>' \
    --userid-analytics <COLUMNAR CLUSTER USERNAME> \
    --password-analytics '<COLUMNAR CLUSTER PASSWORD>' \
    --tls \
    --query-url <OPERATIONAL QUERY NODE HOSTNAME 1>:18093 \
    --multi-query-url <OPERATIONAL QUERY NODE HOSTNAME 1>:18093,<OPERATIONAL QUERY NODE HOSTNAME 2>:18093,<...> \
    --analytics-url <COLUMNAR NODE HOSTNAME 1>:18095 \
    --warehouses 10 \
    --tclients 4 \
    --no-load \
    --ch2pp \
    --query-iterations 2 \
    --warmup-query-iterations 1
```

This command will run both the transactional and analytical parts of the benchmark:

- The transactional part is run with 4 client processes (`--tclients 4`)
- The analytical part is run with 1 client process (`--aclients 1`).
- The benchmark will run until all the 22 analytical queries have been executed twice each, where the first run of each query is a warmup (`--query-iterations 2 --warmup-query-iterations 1`).

## Further Information for Benchmarking

For more in-depth information on running the benchmark yourself, see [`BENCHMARKING.md`](./BENCHMARKING.md).

***

## Transaction and Query Definitions

For the Couchbase driver (`nestcollections`):

- Transaction statements are defined in [`./drivers/nestcollectionsdriver.py`](./drivers/nestcollectionsdriver.py) for both CH2 and CH2++.
- Analytical queries are defined in [`./constants.py`](./constants.py). This includes hand-optimized and "naive" versions of all 22 queries for both CH2 and CH2++.
