FROM harbor.4pd.io/lab-platform/pk_platform/model_services/mjxvl2:0706
WORKDIR /root/workdir
ADD . /root/workdir
EXPOSE 80
SHELL [ "/bin/bash", "--login", "-c"]
ENV PATH /root/miniconda3/bin:$PATH
CMD source activate dev && python main_esb.py
