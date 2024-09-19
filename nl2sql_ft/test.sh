#!/bin/bash
# docker run -it -d \
#     --ipc=host \
#     --name qwen \
#     -p 17780:8080 \
#     --gpus '"device=0,1"' \
#     -v /tmp/customer/zhangwei03/Qwen1.5-110B-Chat-AWQ:/Qwen1.5-110B-Chat-AWQ \
#     harbor.4pd.io/lab-platform/pk_platform/model_services/liyihao_base:4311 \
#     python3 -m vllm.entrypoints.openai.api_server \
#     --host 0.0.0.0 \
#     --port 8080 \
#     --served-model-name Qwen1.5-110B-Chat-AWQ \
#     --model /Qwen1.5-110B-Chat-AWQ \
#     --trust-remote-code \
#     --max-num-batched-tokens 16384 \
#     --max-model-len 16384 \
#     --tokenizer-mode auto \
#     --gpu-memory-utilization 0.7 \
#     --tensor-parallel-size 2

#执行 Python 脚本并获取输出结果
nohup python3 -m vllm.entrypoints.openai.api_server --host 0.0.0.0 --port 17780 \
    --served-model-name model-qwen2-72b-instruct-awq --model /tmp/customer/zhangwei03/deepseek-coder-33b-instruct \
    --max-model-len 16384 --gpu-memory-utilization 0.9 --tensor-parallel-size 1 --dtype auto > vllm_server.log 2>&1 &
#执行 Python 脚本并获取输出结果
# python3 -m vllm.entrypoints.openai.api_server --host 0.0.0.0 --port 17780 \
#     --served-model-name model-qwen2-72b-instruct-awq --model /tmp/customer/zhangwei03/model-qwen2-72b-instruct-awq \
#     --max-model-len 16384 --gpu-memory-utilization 0.8 --tensor-parallel-size 2 --dtype auto 


# 根据输出结果判断并输出
while true
do
    output=$(python3 test_vllm.py)
    if [ "$output" == "yes" ]; then
        echo "webSocket is running"
        break
    else
        echo "webSocket is not running!!!!!!!"
        sleep 2
    fi
done

python3 /app/server.py