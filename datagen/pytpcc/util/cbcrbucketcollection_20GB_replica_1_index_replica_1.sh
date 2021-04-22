#!/bin/bash

echo Delete Buckets

Url=${1:-127.0.0.1}
Site=http://$Url/pools/default/buckets/
Auth=${2:-Administrator:password}
#memory = (512 100 128 128 256 1024 1024 512 '218)#@memory = ("512" "100" "128" "128" "256" "1024" "1024" "512" "218")
#bucket_memory=(512 100 128 128 256 1024 1024 512 218)
bucket_memory=(20480)
bucket=(default)
collections=(CUSTOMER DISTRICT HISTORY ITEM NEW_ORDER ORDERS ORDER_LINE STOCK WAREHOUSE)
#bucket_memory = (100 100 100 100 100 100 100 100 100)

numberOfBuckets=${#bucket[@]}
echo POST /pools/default/buckets

echo "Deleting Buckets"

for i in "${collections[@]}"
do
echo curl -u $Auth $Site$i
curl -X DELETE -u $Auth $Site$i
done
for i in "${bucket[@]}"
do
echo curl -u $Auth $Site$i
curl -X DELETE -u $Auth $Site$i
done

# echo rm -rf /run/data/
# rm -rf /run/data/

echo "Creating Buckets"

# Bucket Params
Site=http://$Url:8091/pools/default/buckets
port=${3:-11224}
low=${3:-3}
high=${3:-8}

# Create bucket
for ((i=0; i < 1 ; i++))
do
	echo curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none $Site -d threadsNumber=$high -d replicaNumber=1 -d replicaIndex=2
let port\+=1
curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none  $Site -d threadsNumber=$high -d replicaNumber=1 -d replicaIndex=1
let port\+=1
done

echo "sleep 30 seconds"
sleep 30
#create scope
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create scope default.tpcc'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create scope default.tpcc'

sleep 30
#create collections
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.CUSTOMER'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.CUSTOMER'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.DISTRICT'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.DISTRICT'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.HISTORY'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.HISTORY'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.ITEM'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.ITEM'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.NEW_ORDER'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.ORDERS'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.ORDER_LINE'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.ORDER_LINE'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.STOCK'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.STOCK'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.WAREHOUSE'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.WAREHOUSE'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.ORDERS'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.NEW_ORDER'

