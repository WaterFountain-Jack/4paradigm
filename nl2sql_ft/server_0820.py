import sys

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from loguru import logger
from nl2sql_hub.datasource import DataSource, get_url
from langchain.sql_database import SQLDatabase
from sentence_transformers import SentenceTransformer
import numpy as np
import random
from sklearn.cluster import KMeans
from utils_self.sql_prompt import (build_ft_sql_prompt,
                                   build_summary_prompt,
                                   build_cot_ft_sql_prompt)
import os
import uvicorn
import json
import openai
from openai import OpenAI
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import time

logger.remove()
logger.add(sys.stdout, level="ERROR")
logger.critical("*****************************************This is a critical message***************************")

app = FastAPI()

temp_path=os.getenv('NL2SQL_WORK_DIR', default="/tmp/")
keep_path=os.path.join(temp_path, "temp.json")

#用于测试不同的模型链接
logger.critical("***********加载m3e模型ing************")
path=("/app/m3e-small")
m3e_model=SentenceTransformer(path)
logger.critical("***********加载m3e模型成功************")


port = int(os.getenv('PORT', '18080'))  # 服务端口
model_name = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')  # 模型名称
model_url=os.getenv('OPENAI_API_BASE')

db_tool = None
# 数据库类型
db_type = None

# 表名
table_names = None
table_info = None
table_names_embedding = None




has_train_data = False
# train_data_dict = dict()
train_data_list = []

chroma_client = chromadb.Client()

class NL2SQLEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:      
            cur_embedding = m3e_model.encode(text).tolist()
            embeddings.append(cur_embedding)
        return embeddings

train_data_collection = chroma_client.get_or_create_collection(name="nl2sql_collection", embedding_function=NL2SQLEmbeddingFunction())


class DataSourceRequest(BaseModel):
    data_source: DataSource


class Message(BaseModel):
    role: str
    content: str


class PredictRequest(BaseModel):
    model: str | None = None
    messages: list[Message]
    stream: bool = True
    stop: str
    max_tokens: int = 4096


class Choices(BaseModel):
    index: int = 0
    delta: Message
    finish_reason: str | None = None


class TrainData(BaseModel):
    query: str
    sql: str
    order: bool


class TrainDataRequest(BaseModel):
    data: list[TrainData]


class PredictResponse(BaseModel):
    id: str = ""
    object: str = ""
    created: int = 1715674796
    model: str = ""
    choices: list[Choices]


class PostProcessRequest(BaseModel):
    content: str


class PostProcessResponse(BaseModel):
    sql: str


class SuccessResponse(BaseModel):
    success: bool

def get_similaruty(qry,train_data):
    cos_similarities = [np.dot(qry, x) / (np.linalg.norm(qry) * np.linalg.norm(x)) for x in train_data]
    return cos_similarities
def top_n_indices(lst, n=5):
    # 使用 enumerate 获取列表的索引和值，并按值降序排列
    sorted_indices = sorted(enumerate(lst), key=lambda x: x[1], reverse=True)
    
    # 提取前 n 个值的索引
    top_indices = [index for index, value in sorted_indices[:n]]
    
    return top_indices

def get_similar_train_data(query,train_data_collection = train_data_collection,train_data_list = train_data_list):
    # query_embedding=np.array(m3e_model.encode(query))
    results = train_data_collection.query(
    query_texts=[query],
    n_results=3  # 获取最接近的5个结果
    )
    logger.critical(f"*********查询到的result的类型为{type(results)},长度为:{len(results)}****************")
    
    logger.critical(f"*********查询到与当前query最近的索引为{results['ids'][0]}****************")
    logger.critical(f"*********train_data_list的长度为{len(train_data_list)}****************")
    
    return [train_data_list[int(i)] for i in results['ids'][0]]

def get_similar_train_data_cluster(query,dic_clusters,list_encoder,train_data_list):
    query_encoder = m3e_model.encode(query)
    
    list_clusters_daibiao_encode = []
    for key,value in dic_clusters.items():
        list_clusters_daibiao_encode.append(list_encoder[value[0]])#用第一个代表这个族
    list_cluster_daibiao_simlar = get_similaruty(query_encoder,list_clusters_daibiao_encode)
    
    logger.critical(f"相似度列表为:{list_cluster_daibiao_simlar}")
    
    #现在获取了最相近的一个族的index
    most_simlar_cluster_idx = list_cluster_daibiao_simlar.index(max(list_cluster_daibiao_simlar))
    logger.critical(f"现在获取了最相近的一个族的index:{most_simlar_cluster_idx}")
    
    logger.critical(f"dic_clusters:{dic_clusters}")
    most_simlar_cluster = dic_clusters[most_simlar_cluster_idx]
    logger.critical(f"*********与当前qry最接近的cluster为: {most_simlar_cluster}****************")
    
    #从最接近的一个族里面再选出最接近的5个
    list_simlar_with_most_simlar_cluster = get_similaruty(query_encoder,most_simlar_cluster)
    tok_k_simlar_idx = top_n_indices(list_simlar_with_most_simlar_cluster,5)
    top_k_simlar_train_data_list_index = [most_simlar_cluster[i] for i in tok_k_simlar_idx]
    logger.critical(f"*********与当前qry最接train_data的idx为: {top_k_simlar_train_data_list_index}****************")
    top_k_simlar_train_data = [train_data_list[i] for i in top_k_simlar_train_data_list_index]
    
    return top_k_simlar_train_data
# results:    [
#     {
#         "ids": ["id1", "id2", "id3"],  # 最接近的几个向量的ID列表
#         "embeddings": [[...], [...], [...]],  # 最接近的向量本身
#         "distances": [0.1, 0.2, 0.3]  # 查询向量到这些最接近向量的距离
#     }
# ]
    # for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
    #     print(f"Document: {doc}, Original Index: {meta['index']}")




# def get_matched_table(table_recall_embedding,tables_name_embedding,tables_name):
#     max_index = np.argmax(get_similaruty(table_recall_embedding,tables_name_embedding ))
#     return tables_name[max_index]

# def get_similarity(query_embedding,embeddings):
#     cos_similarities = np.dot(query_embedding, embeddings) / (np.linalg.norm(query_embedding) * np.linalg.norm(embeddings))
#     return cos_similarities


#对单项query进行embedding,如果是多项，就把query放第一个，sql放第二个
def get_select_samples(json_path,total_query,single_type=True):
    # path=("/app/m3e-small")
    logger.critical("##############开始get_select_samples##################")
    logger.critical(json_path)
    
    logger.critical("##############加载m3e结束##################")
    if single_type:
        query_embedding=np.array(m3e_model.encode(total_query))
    else:
        query_embedding=np.array(m3e_model.encode(total_query[0]))
        sql_embedding=np.array(m3e_model.encode(total_query[1]))
    
    logger.critical("##############m3e模型计算结束##################")
    similarities = []
    with open(json_path, "r",encoding='utf-8') as f:
        fewshot_data = json.load(f)
        logger.critical("##############fewshot_data##################")
        # logger.critical(fewshot_data)
    for item in fewshot_data:
        if single_type:
            similarity = get_similarity(np.array(item["embedding"]), query_embedding)
        else:
            query_similarity=  get_similarity(np.array(item["query_embedding"]), query_embedding) 
            sql_similarit=get_similarity(np.array(item["sql_embedding"]), sql_embedding)
            similarity=query_similarity+sql_similarit
        similarities.append(similarity)
    most_similar_indices = np.argsort(similarities)[-3:]
    #print(most_similar_indices)
    most_similar_data = [fewshot_data[i] for i in most_similar_indices]
    logger.critical("##############结束get_select_samples##################")
    return most_similar_data

def get_select_samples_v1(nl_query):
    results = train_data_collection.query(query_texts=[nl_query], n_results=3)
    most_similar_data = []
    for m in results["documents"]:
        for query in m:
            most_similar_data.append(train_data_dict[query])
    return most_similar_data


# 将prompt分割成system和usr
def split_prompt(prompt,split_words=None):
    # 找到 "today". 的位置
    if split_words is None:
        index = prompt.find('Database schema information:')
    else:
        index = prompt.find(split_words)
    # 分割字符串
    part1 = prompt[:index]
    part2 = prompt[index:]
    return part1,part2


def openai_infer(prompt, stop):
    try:
        
        client = OpenAI(api_key="EMPTY",
                        base_url=model_url)

        # 分割一下prompt：
        prompt1, prompt2 = split_prompt(prompt)
        stop_words = ["<|EOT|>", "Result:"]
        logger.critical("调用了deepseek-coder-33b-instruct用于回答问题")
        response = client.chat.completions.create(
            #model="public/codeqwen1-5-7b-chat@main",
            model="deepseek-coder-33b-instruct",
            messages=[
                {"role": "system", "content": prompt1},
                {"role": "user", "content": prompt2}],
            stop=stop_words,
            stream=True
            # max_tokens=max_new_tokens
        )
        for chunk in response:
            choices = chunk.choices
            result = choices[0].delta.content
            message = Message(role="user", content=f"{result}")
            new_choice = Choices(delta=message)
            if choices[0].finish_reason is not None and choices[0].finish_reason == "stop":
                new_choice.finish_reason = stop
            elif result is None:
                continue
            arr = [new_choice]
            response = PredictResponse(choices=arr)
            result_json = response.model_dump_json() + "\n"
            #print(result_json)
            yield result_json

    except Exception as e:
        logger.critical(f"在调用openai_infer端口的时候出错了")
        logger.critical(f"openai api error: {e}")
        raise e



#传入得到的表的名字，然后获取对应的信息，例如['table1', 'table2', 'table3']
def get_table_info_for_tables(db_tool, selected_table_names):
    db_tool._sample_rows_in_table_info=1
    # 筛选出与给定表名匹配的表的信息
    matched_table_info=""
    for table_name in selected_table_names:
        #logger.critical(f"查询的表名：{table_name}")
        if table_name in table_names:
            continue
        else:
            selected_table_names.remove(table_name)
            logger.critical("错误，没有这个表")
    matched_table_info=db_tool.get_table_info(selected_table_names)
    return matched_table_info


#生成qwen模型查询需要的表的prompt
def build_table_prompt(user_query,database_info):
    return f"""I want you to act as a {db_type} expert in front of an example database, I will provide you with a natural language query question and several SQL tables.
However,not all the provided tables are useful.
Please root out the keywords in the query question and select the tables that are most suitable as the targets involved in the query. 
Only return a set of selected table names separated by ',' without any additional text required.

Database schema information:{database_info}
The question is:{user_query}


Please use the following format to answer:

Question: Question here
Tables: The selected tables 
SQLQuery: SQL Query to run

"""


def build_prompt(user_query,table_selected_info):
    return f"""You are a {db_type} expert. I will give you an input question and ask you to help me create a syntactically correct MySQL query to run
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Database schema information:
{table_selected_info}
The question is: {user_query}

/* Some SQL examples are provided based on similar problems: */

Question: 2021年 整体乘用车销量
SQLQuery: select year, sum(passenger_car_sales) as total_passenger_car_sales from new_energy_vehicle_sales where year = 2021 group by yea
Question: 2023 Tesla 卖了多少辆
SQLQuery: select year,sum(sales) total_sales from new_energy_vehicle_model_sales where brand_name='特斯拉' and year=2023 group by year


Explanation:

The provided database schema consists of three tables: 

1. new_energy_vehicle_city_sales - It contains information about the sales of new energy vehicles in different cities. 
2. new_energy_vehicle_model_sales - It contains information about the sales of new energy vehicles by brand, model, and manufacturer. 
3. new_energy_vehicle_sales - It contains overall information about the sales of new energy vehicles, including passenger cars, BEV (Battery Electric Vehicles), PHEV (Plug-in Hybrid Electric Vehicles), and NEV (New Energy Vehicles). 

The SQL statements are generated based on the database information and natural language queries. 

For example, the first SQL statement is generated from the natural language query: "2021年整体乘用车销量". The SQL statement selects the year and the sum of passenger_car_sales from the new_energy_vehicle_sales table where the year is 2021. 
The second SQL statement is generated from the natural language query: "2023 Tesla卖了多少辆". The SQL statement selects the year and the sum of sales from the new_energy_vehicle_model_sales table where the brand_name is '特斯拉' and the year is 2023. 
These SQL statements retrieve the required information from the database based on the provided queries. The database schema and the SQL statements provide a structured way to query the data which can be used for analytical purposes.

Please use the following format for output:

Question: Question here
SQLQuery: SQL Query to run
Result: The results obtained from the query
"""



def build_prompt_train_data(user_query,table_selected_info,example):
    prompt = f"""You are a {db_type} expert. I will give you an input question and ask you to help me create a syntactically correct MySQL query to run
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Database schema information:
{table_selected_info}
The question is: {user_query}

/* Some SQL examples are provided based on similar problems: */

"""
    #random
    # for data in random.sample(example,num_example):
    #nomol
    for data in example:
        prompt = prompt + f"""Question: {data["query"]}
SQLQuery: {data["sql"]}

"""
    prompt =  prompt +'''Please use the following format for output:

Question: Question here
SQLQuery: SQL Query to run
Result: The results obtained from the query'''
    # logger.critical(f"选择的example条数为：{num_example}")
    return prompt



def build_prompt_train_data_part_data(user_query,table_selected_info,example):
    prompt = f"""You are a {db_type} expert. I will give you an input question and ask you to help me create a syntactically correct MySQL query to run
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Database schema information:
{table_selected_info}
The question is: {user_query}

/* Some SQL examples are provided based on similar problems: */

"""
    for data in example[0:10]:
        prompt = prompt + f"""Question: {data["query"]}
SQLQuery: {data["sql"]}


"""
    return prompt

PROMPT2="""I want you to act as a $DB_TYPE$ expert in front of an example database, I will provide you with a natural language query question and several SQL tables.
However,not all the provided tables are useful.
Please root out the keywords in the query question and select the tables that are most suitable as the targets involved in the query.
Only return a set of selected table names separated by ',' without any additional text required.

Database schema information:
$DB_TXT_CODE$

The question is: $QUERY$

/* Some SQL examples are provided based on similar problems: */
$EXAMPLES_CODE$


Please use the following format to answer:

Question: Question here
Tables: The selected tables 
SQLQuery: SQL Query to run

"""
def extract_tables_info(text):
    # 检查字符串中是否包含 "Tables: "，如果不包含则返回False
    if "Tables: " not in text:
        return False,None
    
    # 使用 split() 方法将字符串按照 "Tables: " 进行分割，取第二部分作为结果
    tables_info = text.split("Tables: ")[1].strip()
    return True,tables_info  
@retry(wait=wait_random_exponential(min=60, max=120), stop=stop_after_attempt(13))
def infer(
        sys_prompt,user_prompt,infer_way="modelhub", type="",base_url="",model="",temperature=0.0,stop_words=None, 
):
    try:
        if infer_way=="modelhub":
            client = OpenAI(api_key = "377058ca9aa547bb9904ae783d6b4170", 
                base_url="http://modelhub.4pd.io/learnware/models/openai/4pd/api/v1")
            logger.critical(f"加载模型modelhub{model}")
        else:
            openai_api_key = "EMPTY"
            openai_api_base = model_url
            client = OpenAI(api_key="xxxx",base_url=openai_api_base)
            models = client.models.list()
            model = models.data[0].id
            logger.critical(f"加载模型vllm{model}")
        

        response = client.chat.completions.create(
            model="deepseek-coder-33b-instruct", # modelhub的url
            messages=[{"role": "system", "content": sys_prompt},
                      {"role": "user", "content": user_prompt}],
            stop=["<|EOT|>"],
            temperature=temperature)
            #stop=["<|im_end|>","SQLQuery:"])
        response = response.choices[0].message.content
        
        logger.critical(f"{type}执行成功了")
        return response
        

    except Exception as e:
        logger.critical(f"{type}执行失败了")
        logger.critical(f"{infer_way}执行失败了")
        logger.critical(f"openai api error: {e}")
        raise e

# def table_infer(
#         prompt,infer_way="modelhub", model="",type="表推理",base_url="",temperature=0.0, 
#         stop_words=None, **args
# ):
#     try:  
#         final_result=[]
#         sys_prompt,user_prompt=split_prompt(prompt)
#         response=infer(sys_prompt=sys_prompt,user_prompt=user_prompt,infer_way=infer_way,type=type,
#                        base_url=base_url,model=model,temperature=temperature,stop_words=stop_words)
#         flag,raw_result=extract_tables_info(response)
#         if flag:
#             result = raw_result.split(", ")
#             logger.critical(f"{infer_way}预测完表了")
#         #logger.critical(result)
        
#         #m3e编码
#             result=m3e_model.encode(result)
#             result=result.tolist()#array变成list
#             for table in result:
#                 matched_table=get_matched_table(table,table_names_embedding,table_names)
#                 final_result.append(matched_table)
#         else:
#             final_result=table_names
#             logger.critical(f"{infer_way}选不出表，所以用全部的")
#         logger.critical(f"{infer_way}表预测成功了")
#         return final_result
        

#     except Exception as e:
#         logger.critical(f"{infer_way}选表出错了")
#         logger.critical(f"{base_url}选表出错了")
#         logger.critical(f"openai api error: {e}")
#         raise e
def build_ft_table_prompt( query, table_info,db_type,examples=None):
    logger.critical("###########进入到table_prompt############")
    prompt = PROMPT2
    examples_text_code = ""
    if examples is not None and len(examples) > 0:
  
        examples_text_code = ""
        
        for example in examples:
            examples_text_code += f"""Question: {example["query"]}
SQLQuery: {' '.join(example["sql"].splitlines()).strip()}\n"""
        examples_text_code+="\n\n"
    prompt = prompt.replace("$EXAMPLES_CODE$", examples_text_code)
    prompt = prompt.replace("$DB_TXT_CODE$", table_info)
    prompt = prompt.replace("$QUERY$", query)
    prompt = prompt.replace("$DB_TYPE$", db_type)
    logger.critical("###########完成结束table_prompt############")
    return prompt

PROMPT3="""You are a $DB_TYPE$  expert. I will give you an input question and ask you to help me create a syntactically correct MySQL query to run
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".
The question is: $QUERY$

Only use the following tables:
$table_selected_info$

$EXAMPLES_CODE$
Please use the following format for output:

Question: Question here
SQLQuery: SQL Query to run
Result: The results obtained from the query
"""



@app.get("/")
def read_root():
    return {"Hello": "word"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/datasource")
def tackle_data_source(request: DataSourceRequest):
    logger.critical("*************进入datasource***************")
    ds_url = get_url(request.data_source)
    logger.critical(f"datasource url: {ds_url}")
    global db_tool
    logger.critical("*************连接数据库***************")
    db_tool = SQLDatabase.from_uri(database_uri=ds_url)
    logger.critical("*************连接数据库成功***************")
    global db_type
    db_type = db_tool.dialect
    logger.critical(f"*************数据库的type是{db_type}***************")

    global has_train_data
    has_train_data = False


    # 获取表名
    global table_names
    table_names = db_tool.get_table_names()
    logger.critical(f"*************数据库的包含的表名有:{table_names}***************")

    #查询结果行的数量为1，之后查询的结果只需要一个
    db_tool._sample_rows_in_table_info=1

    logger.critical(f"*************_sample_rows_in_table_info的条数为:{db_tool._sample_rows_in_table_info}***************")
    # 获取所有表的able info
    global table_info
    table_info = db_tool.get_table_info()
    logger.critical(f"*************数据库get_table_info(不提前设定返回的查询的条数为1)的结果为:{table_info}***************")

    
    return SuccessResponse(success=True)

num_clusters = 7
dic_clusters= {}
list_encoder = []
@app.post("/train_data")
def tackle_train_data(request: TrainDataRequest):
    
    global has_train_data
    if has_train_data == True:
        return SuccessResponse(success=True)
        
    
    logger.critical("*********************进入train_data*************")
    
    global train_data_list
    train_data_list = request.model_dump()["data"]
    #before
    # train_data_list = train_data_list[:len(train_data_list)//2]
    #behind
    # train_data_list = train_data_list[len(train_data_list)//2:]
    #random
    # train_data_list = random.sample(train_data_list, len(train_data_list) // 2)
    # logger.critical(f"*********************用于训练的train_data_list:{train_data_list} len(train_data_list):{len(train_data_list)}*************")
    
    logger.critical(f"*********************用于训练的 len(train_data_list):{len(train_data_list)}   type(train_data_list):{type(train_data_list)}*************")
    logger.critical(f"********train_data_list[0] {train_data_list[0]}*******************")
    
    local_list_encoder = []
    local_dic_clusters= {}
    global num_clusters,dic_clusters,list_encoder
    #进行聚类操作
    for i in train_data_list:
        local_list_encoder.append(m3e_model.encode(i['query']))
    list_encoder = local_list_encoder
    
    logger.critical(f"*********************用于训练的 len(list_encoder):{len(list_encoder)}*************")
    


    # 创建并训练 K-means 模型
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(list_encoder)
    
    # 获取每个向量所属的聚类标签
    labels = kmeans.labels_
    logger.critical(f"********************* len(labels):{len(labels)}*************")

    # 打印聚类结果
    for i in range(num_clusters):
        cluster_items = np.where(labels == i)[0]
        local_dic_clusters[i] = cluster_items
    dic_clusters = local_dic_clusters
    logger.critical(f"分类的情况是{dic_clusters}")
    
    #确保先分类好了之后再把train_data置成true
    has_train_data = True
    
    # 分类的情况是{0: array([ 11,  15,  17,  19,  21,  34,  35,  41,  43,  45,  46,  47,  48,
    #     50,  52,  59,  71,  74,  75,  77, 107, 119]), 1: array([ 40,  42,  44,  65,  68,  69,  78,  80,  82,  84,  90,  91,  94,
    #     95,  97,  99, 101, 103, 104, 106, 108, 109, 110, 113, 115, 116,
    #    118, 120]), 2: array([  0,   1,   3,   4,   5,  14,  16,  20,  22,  24, 121]), 3: array([  2,  18,  56,  58,  66,  70,  72,  81,  83,  86,  88,  92,  96,
    #     98, 112, 114]), 4: array([  6,   7,  12,  26,  28,  38,  60,  62,  64,  67,  73,  76,  85,
    #     87,  89,  93, 100, 102, 111]), 5: array([ 23,  25,  27,  32,  36,  49,  51,  53,  54,  57,  61,  79, 105,
    #    117]), 6: array([ 8,  9, 10, 13, 29, 30, 31, 33, 37, 39, 55, 63])}

    # logger.critical(f"*********************正在将train_data embedding并保存到数据库collection中 *************")
    # embedding_type="query"
    # documents=[]
    # ids=[]
    # for index, item in enumerate(train_data_list):
    #    cur_query = item[embedding_type]
    #    documents.append(cur_query)
    #    ids.append(str(index))

    #    cur_query_embedding=m3e_model.encode(cur_query)
    #    item['cur_query_embedding']  = cur_query_embedding
    # train_data_collection.add(documents=documents, ids=ids)
    # logger.critical(f"*********************成功将train_data embedding并保存到数据库collection中 ，成功将train_data_list中的索引与collection中的相同*************")

    return SuccessResponse(success=True)


@app.post("/postprocess")
def post_process(request: PostProcessRequest):
    sql = request.content
    #print(f"raw sql{sql}")
    # logger.critical(f"Predicted sql: {sql}")
    sql = sql.strip(' \n\t\r')
    if sql.endswith("ResultNone"):
        sql = sql[:-10]
    elif sql.endswith("None"):
        sql = sql[:-4]
    sql = sql.split("SQLQuery:")[-1]
    sql = sql.replace("```", "")
    sql = sql.replace("sql", "")
    sql = sql.replace("SQL", "")
    if ("Please") in sql:
        sql = sql.split("Please")[-2]
    if ("Note") in sql:
        sql = sql.split("Note")[-2]
    if ("This") in sql:
        sql = sql.split("This")[-2]
    # 找到第一个select的位置
    min_index = sql.find("SELECT")

    # 如果找到了select，则截取字符串从select位置开始到结尾
    if min_index != -1:
        new_sql = sql[min_index:]
    else:
        new_sql = sql
    # logger.critical(f"final Predicted sql: {new_sql}")
    # print(f"final sql{new_sql}")
    return PostProcessResponse(sql=new_sql)


@app.post("/predict")
def predict(request: PredictRequest):
    try:
        nl_query = request.messages[0].content
        table_model_url = model_url  # deepseek,用于查询可能用到的表信息
        prompt = ""
        api_key = "EMPTY"
        table_selected_info = db_tool.get_table_info()
        if not has_train_data:
            logger.critical(f"###########进入predict_no_train_data############")
            logger.critical(f"选表的modelurl: {table_model_url}")
            prompt = build_prompt(nl_query, table_selected_info)
        else:

            
            logger.critical(f"###########进入predict_has_train_data############")
            logger.critical(f"选表的modelurl: {table_model_url}")
            # get_similar_train_data_test(nl_query)
            
            global train_data_list,train_data_collection,dic_clusters,list_encoder
            
            logger.critical(f"len(train_data_list):{len(train_data_list)}    ")
            # example  = get_similar_train_data(nl_query,train_data_collection,train_data_list)
            
            example = get_similar_train_data_cluster(nl_query,dic_clusters,list_encoder,train_data_list)
            prompt = build_prompt_train_data(nl_query, table_selected_info,example)
            
            
        return StreamingResponse(
            openai_infer(prompt=prompt, stop=request.stop)
        )

    except Exception as e:
        logger.error(f"Predict error: {e}")

    return PredictResponse(choices=[])


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=port)
