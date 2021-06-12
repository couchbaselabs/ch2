ch2 query generator

Download the tpcds-tools from http://tpc.org/tpc_documents_current_versions/download_programs/tools-download-request5.asp?bm_type=TPC-DS&bm_vers=3.1.0&mode=CURRENT-ONLY into a directory named tpcds

Modify tpcds/tools/expr.h line 95 to:
#define MAX_ARGS        63

Use the templates specified in ch2/querygen/query_templates
Copy the templates to tpcds/query_templates

cd tpcds/tools
./dsqgen -RNGSEED <number> -DIRECTORY ../query_templates -TEMPLATE <QUERY>.tpl -FILTER Y
  This will generate the sql query specified in <query>.tpl
  
 ./dsqgen -help for details on all the options
