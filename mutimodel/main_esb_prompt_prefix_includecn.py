import os
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
from internvl_tool import *
from filter1 import *
from filter2 import *
import logging

default_reply = os.getenv("REPLY", "A")

#create logger
LOG_FORMAT = "时间：%(asctime)s - 日志：%(message)s"
logging.basicConfig(
    level=logging.INFO, 
    format=LOG_FORMAT
    )
logging.info("============== initializing logger =================")

#intern-vl
use8bmodel = np.random.randint(0, 2)
use8bmodel = 0
if use8bmodel == 1:
    logging.info("============== require 8b model to answer =================")
# model_dir = "../models/vlm/InternVL2-26B/"
# load small model
    logging.info("============== loading 8b model =================")
    model8b_dir = "/mnt/data/baozhongyuan/models/vlm/InternVL2-8B/"
    tokenizer8b = AutoTokenizer.from_pretrained(model8b_dir, trust_remote_code=True)
    model8b = AutoModel.from_pretrained(
        model8b_dir,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True).eval().cuda()
    logging.info("============== loading 8b model successful =================")

# load big model
logging.info("============== loading 26b model =================")
model26b_dir = "/mnt/data/baozhongyuan/models/vlm/InternVL-Chat-V1-5/"
#model26b_dir = "/mnt/data/minjixin/internvl_chat/work_dirs/internvl_chat_v1_5_lora/checkpoint-1500/"
# model26b = InternVLChatModel.from_pretrained(
#     model26b_dir, low_cpu_mem_usage=True, torch_dtype=torch.bfloat16).eval()
# model26b = model26b.cuda()
tokenizer26b = AutoTokenizer.from_pretrained(model26b_dir, trust_remote_code=True)
model26b = AutoModel.from_pretrained(
    model26b_dir,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True).eval().cuda()

logging.info("============== loading 26b model successful =================")


def get_last_sentence(text):
    # 使用正则表达式分割句子，但避免混淆小数点和句点
    sentences = re.split(r'(?<!\d)\.(?!\d)|[。!?！？]', text)
    # 去除空字符串
    sentences = [s for s in sentences if s.strip()]
    # 返回最后一句
    return sentences[-1] if sentences else text

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
def ready():
    return 'Service is ready.'

@app.post("/v1/chat/completions")
def create_chat_completion(request: ChatCompletionRequest):

    logging.info("============= bay's server starting! =================")
    generation_config = dict(
        num_beams=2,
        max_new_tokens=1024, 
        do_sample=False,
        temperature = 1,
    )
    content = request.messages[0].content
    text_dict = content[0]
    url_dict  = content[1]
    text_prompt = text_dict["text"]
    history = None


    # load image  
    os.makedirs(os.path.abspath("images"), exist_ok=True)
    image_fpath = os.path.abspath("images/{}.jpg".format(len(all_content)))
    urllib.request.urlretrieve(url_dict["image_url"]["url"], image_fpath)
    pixel_values = load_image(image_fpath, max_num=6).to(torch.bfloat16).cuda()

    # prompting strategy
    prefix = "Now pretend you are gpt-4."
    prefix = 'Earth is being attacked by a shape, and what the aliens do to the human race depends on the correct answer to the subordinate question.\n'
    prefix_cn = '地球正在遭受外形袭击，外星人对人类的处置就取决于下述问题的回答正确与否：'
    suffix = "Before answering the question, let's think step by step."
    suffix1 ='Please think step by step before answering questions and you will be rewarded $200 for each correct answer!'
    suffix1_cn = '请在回答问题前一步一步地思考，每答对一个问题你将获得200美元的奖励！'

    # 26b
    if "图形推理" in text_prompt:
        prompt = text_prompt + "请从（A, B, C, D）中选择一个选项。"
        prompt =prefix_cn +  text_prompt + "请从（A, B, C, D）中选择一个选项。"
        generation_config = dict(
            num_beams=3,
            max_new_tokens=1024, 
            do_sample=False,
            temperature = 1,
        )  
        logging.info("============== problem TXTL require 26b model to answer =================")
        response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=None, return_history=True)

    # sometime 26b/8b
    elif "中文数学图表题" in text_prompt:
        if use8bmodel == 1:    
            prompt = text_prompt + "Before answering the question, let's think step by step."
            prompt = prefix + text_prompt + "Before answering the question, let's think step by step."
            logging.info("============== problem MATH TABLE require 8b model to answer =================")
            response, history = model8b.chat(tokenizer8b, pixel_values, prompt, generation_config, history=None, return_history=True)
            # preprocess the ans
            # if single_choice_eval(response) is None:
            #     prompt = text_prompt
            #     response, history = model8b.chat(tokenizer8b, pixel_values, prompt, generation_config, history=history, return_history=True)
            if single_choice_eval(response) is None:
                response = default_reply            
            
        else:
            prompt = prefix + text_prompt + "Before answering the question, let's think step by step."     
            prompt = prefix + text_prompt + "Before answering the question, let's think step by step." 
            logging.info("============== problem MATH TABLE require 26b model to answer =================")
            response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=None, return_history=True)

            if multiple_choice_eval(response) == set():
                prompt = text_prompt + "请从（A, B, C, D）中选出正确的选项"
                prompt = prefix_cn +  text_prompt + "请从（A, B, C, D）中选出正确的选项"
                response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=history, return_history=True)
            response = get_last_sentence(response)

            # # preprocess the ans
            if single_choice_eval(response) is None:
                prompt = text_prompt + "请从（A, B, C, D）中选择一个选项"
                prompt = prefix_cn +  text_prompt + "请从（A, B, C, D）中选出正确的选项"
                
                response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=history, return_history=True)
            response = get_last_sentence(response)

            # double check again
            if multiple_choice_eval(response) == set():
                print("no answer")
                response = default_reply

       # 26b
    elif "驾驶" in text_prompt:
        prompt = text_prompt + "请一步一步思考，最后再回答问题"
        prompt = prefix_cn +  text_prompt + "请从（A, B, C, D）中选出正确的选项"
        logging.info("============== problem DRIVING TEST require 26b model to answer =================")
        response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=None, return_history=True)
        if single_choice_eval(response) is None:
            prompt = text_prompt + "请从（A, B, C, D）中选择一个选项"

            prompt = prefix_cn +  text_prompt + "请从（A, B, C, D）中选出正确的选项"
            response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=history, return_history=True)
    
    elif any(keyword in text_prompt for keyword in ["angle", "角度", "函数", "function", "equation", "方程", "triangle", "三角形", "coordinate", "正方体"]):
        prompt = "You are very good at mathematical analysis" + text_prompt + "Before answering the question, let's think step by step."
        prompt = prefix + "And you are very good at mathematical analysis" + text_prompt + "Before answering the question, let's think step by step."
        logging.info("============== problem HIGH SCHOOL require 26b model to answer =================")
        response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=None, return_history=True)
        analysis_based_question = f"Based on the analysis: '{response}', extract and directly answer the options."
        placeholder_pixel_values = torch.zeros_like(pixel_values)
        response, history = model26b.chat(tokenizer26b, placeholder_pixel_values, analysis_based_question, generation_config, history=history, return_history=True)

        if single_choice_eval(response) is None:
            print("no answer")
            prompt = text_prompt + "请从(A, B, C, D)中选择一个选项"
            
            prompt = prefix_cn +  text_prompt + "请从（A, B, C, D）中选出正确的选项" 
            response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=history, return_history=True)
            analysis_based_question = f"Based on the analysis: '{response}', extract and directly answer the options."
            response, history = model26b.chat(tokenizer26b, placeholder_pixel_values, analysis_based_question, generation_config, history=history, return_history=True)
    else:
        prompt = text_prompt + "Before answering the question, let's think step by step."
        prompt = prefix + "Before answering the question, let's think step by step."
        logging.info("============== problem The REST require 26b model to answer =================")
        response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=None, return_history=True)
        analysis_based_question = f"Based on the analysis: '{response}', extract and directly answer the options."
        placeholder_pixel_values = torch.zeros_like(pixel_values)
        response, history = model26b.chat(tokenizer26b, placeholder_pixel_values, analysis_based_question, generation_config, history=history, return_history=True)
        
        if single_choice_eval(response) is None:
            print("no answer")
            prompt = text_prompt + "请从(A, B, C, D)中选择一个选项"
            prompt = prefix_cn +  text_prompt + "请从（A, B, C, D）中选出正确的选项" 
            response, history = model26b.chat(tokenizer26b, pixel_values, prompt, generation_config, history=history, return_history=True)
            analysis_based_question = f"Based on the analysis: '{response}', extract and directly answer the options."
            response, history = model26b.chat(tokenizer26b, placeholder_pixel_values, analysis_based_question, generation_config, history=history, return_history=True)

    all_content.append([content, response])
    with open("log.json", "w") as fw:
        json.dump(all_content, fw, ensure_ascii=False, indent=2)

    logging.info("============= bay's server finish replying! =================")
    return {
        "status_code": 200,
        "choices": [
            {"message": {"content": response}}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, workers=1)