FROM harbor-contest.4pd.io/qiaosiyao/qiaosiyao_sql_finetune_image:0.3

# 设置工作目录
WORKDIR /app


# 设置环境变量
ENV LANG=C.UTF-8 \
    GPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696D \
    PYTHON_VERSION=3.10.1 \
    PYTHON_PIP_VERSION=21.2.4 \
    PYTHON_SETUPTOOLS_VERSION=57.5.0 \
    PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/3cb8888cc2869620f57d5d2da64da38f516078c7/public/get-pip.py \
    PYTHON_GET_PIP_SHA256=c518250e91a70d7b20cceb15272209a4ded2a0c263ae5776f129e0d9b5674309 \
    PYTHONPATH=/app:

# 复制应用程序代码到容器中
COPY . /app

# # 安装依赖
# RUN pip install --upgrade pip==${PYTHON_PIP_VERSION} && \
#     pip install -r requirements.txt

# 暴露端口
EXPOSE 18080

# 启动容器时运行的命令
ENTRYPOINT ["python", "/app/server.py"]

# 默认命令
CMD ["/bin/bash"]
