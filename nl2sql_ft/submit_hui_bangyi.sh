
echo "### 正在提交到榜单... ###"

read -p "输入策略描述(test)：" DESCRIPTION
DESCRIPTION=${DESCRIPTION:-"test"}

curl --location --request POST 'http://contest.4pd.io:8080/submit' \
--header 'Authorization: Bearer b9f5343e4ef99ef49e4e18afdc5648c3' \
--form-string 'benchmark=nl2sql_ft' \
--form-string 'contributors=qiaosiyao,xutao' \
--form-string "description=basemodel:$DESCRIPTION" \
--form-string 'product_avaliable=1' \
--form-string 'source_code=https://gitlab.4pd.io/' \
--form 'config_file=@"/home/qiaosiyao/qiaosiyao_sql_change_embedding/config_hui_bangyi.yaml"' 