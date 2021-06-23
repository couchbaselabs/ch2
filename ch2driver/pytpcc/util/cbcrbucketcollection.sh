#!/bin/bash

echo Delete Buckets

Url=${1:-127.0.0.1}
Auth=${2:-Administrator:password}
replica=${3:-0}
Site=http://$Url:8091/pools/default/buckets/
bucket_memory=(25600)
bucket=(bench)
collections=(customer district history item neworder orders stock warehouse supplier nation region)

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
port=${4:-11224}
low=${4:-3}
high=${4:-8}

# Create bucket
for ((i=0; i < 1 ; i++))
do
	echo curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none $Site -d threadsNumber=$high -d replicaNumber=$replica
let port\+=1
curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none  $Site -d threadsNumber=$high -d replicaNumber=$replica
let port\+=1
done

echo "sleep 30 seconds"
sleep 30
#create scope
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create scope bench.ch2'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create scope bench.ch2'

sleep 30
#create collections
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.CUSTOMER'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.CUSTOMER'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.DISTRICT'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.DISTRICT'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.HISTORY'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.HISTORY'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.ITEM'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.ITEM'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.NEW_ORDER'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.ORDERS'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.ORDER_LINE'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.ORDER_LINE'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.STOCK'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.STOCK'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.WAREHOUSE'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.WAREHOUSE'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.ORDERS'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.NEW_ORDER'
