import chromadb
import numpy as np
from chromadb.utils.embedding_functions import CustomEmbeddingFunction

# 自定义embedding函数
class MyCustomEmbeddingFunction(CustomEmbeddingFunction):
    def __call__(self, texts):
        # 这是一个简单的例子，将每个文本转为一个简单的数值表示
        # 实际中你可能会使用更复杂的模型，如BERT或GPT
        return np.array([np.array([len(text)]) for text in texts])

# 初始化ChromaDB客户端
client = chromadb.Client()

# 创建一个新的集合
collection = client.create_collection(
    name="my_collection",
    embedding_function=MyCustomEmbeddingFunction()
)

# 插入内容
documents = ["Hello world", "ChromaDB is cool", "Embedding functions are powerful"]
metadatas = [{"index": i} for i in range(len(documents))]
ids = [f"id_{i}" for i in range(len(documents))]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

# 查找相似的内容
query_text = "Hello"
results = collection.query(
    query_texts=[query_text],
    n_results=3
)

# 输出查找结果
for i, result in enumerate(results['documents'][0]):
    print(f"Result {i+1}:")
    print(f"Document: {result}")
    print(f"Metadata: {results['metadatas'][0][i]}")
    print(f"ID: {results['ids'][0][i]}")
    print("----------")
