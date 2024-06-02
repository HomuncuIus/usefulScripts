#! /bin/bash

port=$1
is_error=$2
count=0
time_out=10

# 模拟client进程启动
while [ $count -lt $time_out ]
do
    sleep 1
    echo "starting client ${count}"
    ((count++))
done
echo "client ready"

# 模拟client工作
sleep 5
count=0
while [ $count -lt $time_out ]
do
    sleep 1
    echo "client running ${count}"
    ((count++))
done

# 模拟client报错
if [ ${is_error} -eq 1 ]; then
    echo "client error">&2
    exit 1
fi

# 模拟client工作
count=0
while true
do
    if [ ${RANDOM} -lt 100 ]; then
        echo "client error">&2
        exit 1
    fi
    sleep 1
    echo "client running ${count}"
    ((count++))
done