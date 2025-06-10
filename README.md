# CH2++: A Hybrid Operational/Analytical Processing Benchmark for NoSQL Databases

## History of CH2++

### 1. The initial CH benCHmark was proposed in 2011 to evaluate relational database systems with hybrid data management support

- CH borrows from and extends the schemas of TPC-C and TPC-H and combines the TPC-C transactions and the analytical queries of TPC-H to provide a hybrid benchmark.

### 2. CH2 was designed in 2021 as an extension of the CH benchmark to evaluate document database systems with hybrid data management support

- CH2 extends CH by introducing a document oriented schema, a data generation schema that creates a TPC-H like history, and modifying the CH analytical queries to be more along the lines of TPC-H.

### 3. CH2++ is a generalization of the CH2 schema to be more in line with JSON and analytics

- The TPC-C and TPC-H schemas have been modified to nest data where it would naturally be nested.
- CUSTOMER has been extended to have multiple addresses and phones and a set of categories.
- ITEM has been extended to have a set of categories.

***

## Usage

Further documentation and all relevant source code for running the benchmark are located in the [`ch2driver/pytpcc`](./ch2driver/pytpcc/) directory.
