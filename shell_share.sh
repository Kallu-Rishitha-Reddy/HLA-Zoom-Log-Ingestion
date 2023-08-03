#!/bin/bash

# Change these variables to match your servers and ports
SERVERS=("10.230.130.20")
PORTS=(6100)

# Read data from file
DATA=$(cat /home/local/SERVICE-NOW/rishitha.reddy.adm/hla_zoom_scripts/data.txt)

# Send data over TCP to each server and port
for SERVER in "${SERVERS[@]}"
do
    for PORT in "${PORTS[@]}"
    do
        echo $DATA | nc $SERVER $PORT
    done
done
