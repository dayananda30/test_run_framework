#!/bin/bash

echo "Hello"

#install rabbitmq with sudo option and yes option
#TODO:
#creating rabbitmq user 'sid' with password 'test'
sudo rabbitmqctl add_user sid test

#To verify rabbitmq username and password
sudo rabbitmqctl authenticate_user sid test

# add virtual host 'sid_vhost'
sudo rabbitmqctl add_vhost sid_vhost

# add user tag 'sid_tag' for user 'sid'
rabbitmqctl set_user_tags sid sid_tag

# set permission for user 'sid' on virtual host 'sid_vhost'
#sudo rabbitmqctl set_permissions -p sid_vhost sid ".*" ".*" ".*"
sudo rabbitmqctl set_permissions -p / sid ".*" ".*" ".*"

pip3 install requirements.txt
