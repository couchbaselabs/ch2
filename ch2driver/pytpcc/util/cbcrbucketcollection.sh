#!/bin/bash

echo Delete Buckets

Url=${1:-127.0.0.1}
Site=http://$Url:8091/pools/default/buckets/
Auth=${2:-Administrator:password}
#memory = (512 100 128 128 256 1024 1024 512 '218)#@memory = ("512" "100" "128" "128" "256" "1024" "1024" "512" "218")
#bucket_memory=(512 100 128 128 256 1024 1024 512 218)
bucket_memory=(2048)
bucket=(default)
collections=(customer district history item neworder orders stock warehouse supplier nation region)
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
	echo curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none $Site -d threadsNumber=$high -d replicaNumber=0
let port\+=1
curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none  $Site -d threadsNumber=$high -d replicaNumber=0
let port\+=1
done

echo "sleep 30 seconds"
sleep 30
#create scope
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create scope default.tpcc'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create scope default.tpcc'

sleep 30
#create collections
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.customer'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.customer'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.district'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.district'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.history'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.history'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.item'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.item'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.neworder'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.neworder'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.orders'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.orders'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.stock'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.stock'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.warehouse'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.warehouse'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.supplier'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.supplier'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.nation'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.nation'
echo curl http://$Url:9499/query/service -u $Auth -d 'statement=create collection default.tpcc.region'
curl http://$Url:8093/query/service -u $Auth -d 'statement=create collection default.tpcc.region'

