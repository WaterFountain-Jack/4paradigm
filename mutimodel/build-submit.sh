#!/bin/bash
# harbor-contest.4pd.io/qiaosiyao/qiaosiyao_duomotai_include_26b:0.1
# 处理变量
var_docker_image_name="qiaosiyao_duomotai_varification_prompt"
var_docker_image_version=$(date +%s%3N) # 毫秒级时间戳

# build & push docker image
echo '### 开始构建docker镜像并推动至harbor... ###'
set -e
docker build -t ${var_docker_image_name}:${var_docker_image_version} .
docker login harbor-contest.4pd.io -u qiaosiyao -p Qsy123456@
docker tag ${var_docker_image_name}:${var_docker_image_version} harbor-contest.4pd.io/qiaosiyao/${var_docker_image_name}:${var_docker_image_version}
docker push harbor-contest.4pd.io/qiaosiyao/${var_docker_image_name}:${var_docker_image_version}

# 写 submit config.yaml
{
    echo "image: harbor-contest.4pd.io/qiaosiyao/${var_docker_image_name}:${var_docker_image_version}"
    tail -n +2 ./config.yaml
} > ./temp.file
mv ./temp.file ./config.yaml


# submit
echo "### 正在提交到榜单... ###"

read -p "输入策略描述(test)：" DESCRIPTION
DESCRIPTION=${DESCRIPTION:-"test"}

curl --location --request POST 'http://contest.4pd.io:8080/submit' \
--header 'Authorization: Bearer b9f5343e4ef99ef49e4e18afdc5648c3' \
--form-string 'benchmark=multi-modality' \
--form-string 'contributors=qiaosiyao,xutao' \
--form-string "description=basemodel:$DESCRIPTION" \
--form-string 'product_avaliable=1' \
--form-string 'source_code=https://gitlab.4pd.io/' \
--form 'config_file=@"/home/qiaosiyao/qiaosiyao_duomotai_varification_prompt/config.yaml"' 