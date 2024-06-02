#! /bin/bash

port=$1
is_error=$2
count=0
time_out=1

# 模拟server进程启动
while [ $count -lt $time_out ]
do
    sleep 1
    echo "starting server ${count}"
    ((count++))
done
echo "server ready"

# 模拟server工作
sleep 5
count=0
while [ $count -lt $time_out ]
do
    sleep 1
    echo "server running ${count}, QPS=${RANDOM}, time=${RANDOM}.${RANDOM}"
    ((count++))
done

# 模拟server报错
if [ ${is_error} -eq 1 ]; then
    echo "server error">&2
    exit 1
fi

# 模拟server工作
count=0
while true
do
    if [ ${RANDOM} -lt 1000 ]; then
        echo "server error">&2
        exit 1
    fi
    sleep 1
    echo "server running ${count}, QPS=${RANDOM}, time=${RANDOM}.${RANDOM}"
    ((count++))
done