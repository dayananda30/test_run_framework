#!/bin/bash

dir=$(pwd)

mnt="${dir}/mnt"
cp config.yaml docker/
cd docker
docker build -t worker_test_run .
sudo docker run -d -v /home/sheetal/sid/code_space/project_space/test_framework/python-docker-app/mnt:/mnt --name test_1 worker_test_run
