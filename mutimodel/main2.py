import os
import argparse
import json
from tqdm import tqdm
from PIL import Image
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, LlamaTokenizer
from transformers import AutoModel
import math
import torch
import torchvision.transforms as T
from torchvision.transforms.functional import InterpolationMode
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Literal, Optional, Union
import numpy as np
import pandas as pd
from transformers.trainer_utils import set_seed
from transformers.generation import GenerationConfig
import re
import base64
import urllib
import logging
from internvl_tool import *
from filter1 import *
from filter2 import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

#intern-vl
index = np.random.randint(0, 2)
print(index)

flag = False
# path = "/root/workdir/model/InternVL2-26B/"
path = "/root/workdir/model/InternVL2-40B/"
model = AutoModel.from_pretrained(
    path,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True,
    device_map='auto').eval()

tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
flag = True

async def lifespan(app: FastAPI):  # collects GPU memory
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: List[dict]


class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: Optional[int] = None
    frequency_penalty: Optional[float] = None
    temperature: Optional[float] = None
    presence_penalty: Optional[float] = None
    top_p: Optional[float] = None
    stop: Optional[str] = None

all_content = []

@app.get("/ready")
async def check_ready():
    
    if flag == False:
        return {"status_code": 400}
    logging.info('Model ready')

    return {"status_code": 200}

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):

    global model, tokenizer, index
    generation_config = dict(
    num_beams=2,
    max_new_tokens=1024, #1024
    do_sample=False,
    temperature = 1,
    )
    content = request.messages[0].content
    text_dict = content[0]
    url_dict  = content[1]
    text_prompt = text_dict["text"]
    history = None

    prefix_template = ["Now pretend you are gpt-4.", "Take a deep breath\n"]   
    prefix = prefix_template[index]
    print(prefix)

    # prompting strategy
    if "图形推理" in text_prompt:
        prompt = text_prompt + "请仔细观察图形，并选择最符合规律的选项。"
 
    elif "中文数学图表题" in text_prompt:
        prompt = prefix + text_prompt + "Before answering the question, let's think step by step."   

    elif "驾驶" in text_prompt:
        prompt = text_prompt + "请先一步一步思考，最后再回答问题"

    elif any(keyword in text_prompt for keyword in ["angle", "角度", "函数", "function", "equation", "方程", "triangle", "三角形", "coordinate", "正方体"]):
        prompt = "You are very good at mathematical analysis" + text_prompt + "Before answering the question, let's think step by step."

    else:
        prompt = text_prompt + "Before answering the question, let's think step by step."

    os.makedirs(os.path.abspath("images"), exist_ok=True)
    image_fpath = os.path.abspath("images/{}.jpg".format(len(all_content)))
    urllib.request.urlretrieve(url_dict["image_url"]["url"], image_fpath)

    pixel_values = load_image(image_fpath, max_num=6).to(torch.bfloat16).cuda()
    response, history = model.chat(tokenizer, pixel_values, prompt, generation_config, history=None, return_history=True)

    #analysis_based_question = f"Based on the analysis: '{response}', extract and directly answer the options."
    generation_config2 = dict(
    num_beams=2,
    max_new_tokens=128, 
    do_sample=False,
    temperature = 1,
    )   

    generation_prompt = """"
    角色：你是一个智能助手帮助人类提取答案
    目标：根据你的分析过程提取出回答中的正确答案的字母。尽量只返回字母，不用返回选项内容
    输出要求：单选题给出一个字母，多选题可能只有一个正确的选项，也可能有多个，只返回你确定正确的选项。如果你的分析中认为每个选项都是错误的，仅返回一个最可能是正确的选项
    单选输出示例：C
    多选输出示例：ABC或C
    ---
    请直接输出答案
    """
    placeholder_pixel_values = torch.zeros_like(pixel_values)
    final_response, history = model.chat(tokenizer, placeholder_pixel_values, generation_prompt, generation_config2, history=history, return_history=True)
    print(final_response)
    
    if single_choice_eval(final_response) is None:
        print("no answer")
        prompt = text_prompt + "请从(A, B, C, D)中选择一个选项"
        response2, history = model.chat(tokenizer, pixel_values, prompt, generation_config, history=history, return_history=True)
        #analysis_based_question = f"Based on the analysis: '{response2}', extract and directly answer the options."
        final_response, history = model.chat(tokenizer, placeholder_pixel_values, generation_prompt, generation_config2, history=history, return_history=True)
        print(final_response)
    
    all_content.append([content, final_response])
    with open("log.json", "w") as fw:
        json.dump(all_content, fw, ensure_ascii=False, indent=2)

    return {
        "status_code": 200,
        "choices": [
            {"message": {"content": final_response}}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, workers=1)






