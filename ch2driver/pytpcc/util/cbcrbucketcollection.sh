#!/bin/bash

echo Delete Buckets

Url=${1:-127.0.0.1}
Auth=${2:-Administrator:password}
replica=${3:-0}
Site=http://$Url:8091/pools/default/buckets/
bucket_memory=(2560)
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
	echo curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none $Site -d threadsNumber=$high -d replicaNumber=$replica -d evictionPolicy=fullEviction
let port\+=1
curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none  $Site -d threadsNumber=$high -d replicaNumber=$replica -d evictionPolicy=fullEviction
let port\+=1
done

echo "sleep 30 seconds"
sleep 30
#create scope
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create scope bench.ch2'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create scope bench.ch2'

sleep 30
#create collections
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.customer'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.customer'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.district'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.district'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.history'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.history'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.item'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.item'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.neworder'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.neworder'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.orders'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.orders'
#echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.ORDER_LINE'
#curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.ORDER_LINE'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.stock'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.stock'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.warehouse'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.warehouse'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.supplier'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.supplier'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.nation'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.nation'
echo curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.region'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection bench.ch2.region'
