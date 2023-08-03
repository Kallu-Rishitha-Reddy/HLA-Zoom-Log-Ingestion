#!/bin/bash

# Execute Python script
python3 /home/local/SERVICE-NOW/rishitha.reddy.adm/hla_zoom_scripts/hla_zoom.py
python_exit_code=$?

if [ $python_exit_code -ne 0 ]; then
    echo "Python script failed with exit code $python_exit_code"
    exit $python_exit_code
fi

# Execute shell script
sh /home/local/SERVICE-NOW/rishitha.reddy.adm/hla_zoom_scripts/shell_share.sh
shell_exit_code=$?

if [ $shell_exit_code -ne 0 ]; then
    echo "Shell script failed with exit code $shell_exit_code"
    exit $shell_exit_code
fi

if [ -f $log.txt ]; then
    rm /home/local/SERVICE-NOW/rishitha.reddy.adm/hla_zoom_scripts/log.txt
    echo "$log.txt is removed"
fi

echo "Both scripts completed successfully"