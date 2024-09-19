#!/bin/bash

# 定义变量
script_to_run="/home/qiaosiyao/qiaosiyao_sql/submit_origin.sh" # 需要运行的脚本路径
start_time="2024-08-07 11:25:00" # 开始运行时间
run_times=5 # 运行次数
interval=60 # 每次运行的间隔时间（秒）

# 将开始时间转换为时间戳
start_timestamp=$(date -d "$start_time" +%s)

# 获取当前时间戳
current_timestamp=$(date +%s)

# 计算需要等待的秒数
sleep_seconds=$((start_timestamp - current_timestamp))

# 如果等待时间大于0，则等待到指定时间
if [ $sleep_seconds -gt 0 ]; then
  echo "等待 $sleep_seconds 秒直到 $start_time..."
  sleep $sleep_seconds
fi

# 按照指定次数和间隔运行目标脚本
i=1
while [ $i -le $run_times ]
do
  echo "正在运行 $script_to_run, 第 $i 次..."
  bash $script_to_run

  # 如果还没到最后一次，则等待指定间隔时间
  if [ $i -lt $run_times ]; then
    echo "等待 $interval 秒..."
    sleep $interval
  fi

  i=$((i + 1))
done

echo "脚本运行完毕！"
