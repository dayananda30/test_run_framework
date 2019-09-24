#!/bin/bash

dir=$(pwd)

mnt="${dir}/mnt"
cp config.yaml docker/
cd docker
docker build -t worker_test_run .

value=$(grep -A3 'WORKERS:' config.yaml); value=$(echo $value|cut -d ':' -f 2);value=$(echo $value | tr -d ':') value=$(echo $value | tr -d ' ' | tr -d '\r')
echo "Number of workers : "$value

for i in `seq 1 $value`
do
   sudo docker run -d -v ${mnt}:/mnt --name test_${i} worker_test_run
done
