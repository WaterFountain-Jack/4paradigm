curl --location --request POST 'http://contest.4pd.io:8080/submit' \
--header 'Authorization: Bearer a4c95c0a3f806aa8db78aaf25b597cea' \
--form-string 'benchmark=multi-modality' \
--form-string 'contributors=minjixin, wanghe, guanyandong, wangzhangcheng' \
--form-string 'description=0720' \
--form-string 'product_avaliable=1' \
--form-string 'source_code=https://gitlab.4pd.io/' \
--form 'config_file=@"/mnt/data/minjixin/multi-vl2/config1.yaml"'
