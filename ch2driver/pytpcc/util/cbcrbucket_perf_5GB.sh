#!/bin/bash

echo Delete Buckets

Url=${1:-127.0.0.1:8091}
Site=http://$Url/pools/default/buckets/
Auth=${2:-Administrator:password}
#memory = (512 100 128 128 256 1024 1024 512 '218)#@memory = ("512" "100" "128" "128" "256" "1024" "1024" "512" "218")
#bucket_memory=(512 100 128 128 256 1024 1024 512 218)
bucket_memory=(5000 5000 5000 5000 5000 5000 5000 5000 5000)
bucket=(CUSTOMER DISTRICT HISTORY ITEM NEW_ORDER ORDERS ORDER_LINE STOCK WAREHOUSE)
#bucket_memory = (100 100 100 100 100 100 100 100 100)

numberOfBuckets=${#bucket[@]}
echo POST /pools/default/buckets

echo "Deleting Buckets"

for i in "${bucket[@]}"
do
echo curl -u $Auth $Site$i
curl -X DELETE -u $Auth $Site$i
done

# echo rm -rf /run/data/
# rm -rf /run/data/

echo "Creating Buckets"

# Bucket Params
Site=http://$Url/pools/default/buckets
port=${3:-11224}
low=${3:-3}
high=${3:-8}

# Create buckets
for ((i=0; i < 9 ; i++))
do
	echo curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none -d proxyPort=$port $Site -d threadsNumber=$high
let port\+=1
curl -X POST -u $Auth -d name=${bucket[$i]} -d ramQuotaMB=${bucket_memory[$i]} -d authType=none $Site -d threadsNumber=$high -d replicaNumber=0
let port\+=1
done

echo "sleep 30 seconds"
sleep 30