set -e
image_name=multi-ft
version=0720
docker build -t ${image_name}:${version} .
docker login harbor.4pd.io -u test -p Harbor@test01
docker tag ${image_name}:${version} harbor.4pd.io/lab-platform/pk_platform/model_services/${image_name}:${version}
docker push harbor.4pd.io/lab-platform/pk_platform/model_services/${image_name}:${version}