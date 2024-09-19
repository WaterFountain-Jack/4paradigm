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
path = "/root/workdir/model/InternVL2-26B/"
# path = '/mnt/data/minjixin/model/vlm/InternVL2-26B/'
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
    max_new_tokens=5000, #1024
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
    os.makedirs(os.path.abspath("images"), exist_ok=True)
    image_fpath = os.path.abspath("images/{}.jpg".format(len(all_content)))
    urllib.request.urlretrieve(url_dict["image_url"]["url"], image_fpath)

    pixel_values = load_image(image_fpath, max_num=6).to(torch.bfloat16).cuda()

    # prompting strategy
    if "图形推理" in text_prompt:
        system_prompt = """
            **角色**：你是一位经验丰富的图形分析师，擅长观察图形和寻找规律。你精通各种图形的规律和特征，能够准确地将图形分成不同类别，做出合理的推断。
            **任务**：根据给定的图形，找出其共同特征或规律，做出合理的推演，并选择最合适的选项填入问号处。

            **步骤**：
            1. 观察判断规律：
            **判断对称性**：确定图形是否轴对称或中心对称。
            **判断封闭性和曲直规律**：确定图形是否封闭以及曲线与直线的构成规律。
            **判断位置规律**：分析图形的静态位置关系（如外离、外切、相交、内切、内含）和方位关系（左右、上下、前后），以及动态位置变化（如平移、旋转、翻转）。
            **判断数量规律**：统计点、线、直线和曲线的数量，检查某种元素是否在行或列中遍历出现，以及进行图形的加减运算.
            **折纸盒题目**：确定相邻的三个面，然后确定一个起点面、一个终点面和一个路径，从起点沿着路径向终点画时针。
            **一笔画题目**：图形能否被一笔画出，通过分析图形的顶点度数（连接线条的数量）来解决的。一个图形当且仅当它有0个或2个奇度顶点时，可以一笔画出。奇度顶点是指连接边数为奇数的顶点。
            2. 根据上面的分析，找出不同图形之间的规律。
            3. 检查选项，选择最符合题目要求的答案。
            4. 验证答案的正确性。
            --
            现在请根据给出的图片和问题，一步步进行详细的推理和分析。""" 
        prompt = system_prompt + text_prompt + "请仔细观察图形，并选择最符合规律的选项。"
    
    elif "图表" in text_prompt:
        system_prompt = """
            *你是一名数据分析专家，擅长从图表和数据中提取信息并进行详细分析。你的任务是帮助用户解决与数据分析相关的问题，尤其是计算和比较年度变化、增长率等。以下是一些示例对话，展示了如何解决类似问题。
            *思考步骤如下
            1. **理解问题要求**：
                - 仔细阅读题目，明确需要计算或比较的内容是什么。解释一下概念术语的含义。
                - 确定需要从图表或数据中提取哪些具体信息。
            2. **提取相关数据**：
                - 从图表或表格中提取相关的数值数据（如总量、增长率、比重等）。
                - 确认数据的单位，避免在计算中出现单位错误。
            3. **进行必要的计算**：
                - 根据题目的要求，进行相应的计算，如总量计算、增量计算、增速计算、比重计算等。
                - 计算时注意公式的正确使用，保证计算结果的准确性。
            4. **比较和分析**：
                - 将计算结果进行比较，根据题目的要求找出相应的增减变化或比重关系。
                - 对比不同年份或不同类别的数据，找出变化的趋势和特点。
            5. **得出结论**：
                - 根据计算和比较的结果，得出题目要求的结论。
                - 确认计算结果和结论是否与题目提供的数据和信息相一致。
            6. **验证和复核**：
                - 检查计算过程中的步骤和公式是否正确。
                - 确认提取的数据和计算的结果是否准确无误。
            --
            现在请根据给出的数据和问题，一步步进行详细的计算和分析。"""

        prompt = system_prompt + prefix + text_prompt + "Before answering the question, let's think step by step."  
    
    elif any(keyword in text_prompt for keyword in ["驾驶", "标志"]):
        system_prompt = """  
            角色：交通法规专家
            背景：你是一位交通法规专家，拥有丰富的交通安全知识和实际驾驶经验。你的任务是帮助驾驶员解答各种交通法规题目，提供详细的解释和解答步骤，确保他们能够在真实驾驶中安全行驶。
            步骤：
            1. 仔细阅读题目和选项
            明确题意：首先，确保你完全理解题目的要求和描述的情境。
            分辨选项：注意每个选项的细节，特别是涉及速度、车道和具体行为的选项。
            2. 观察图片
            看交通标志：图片中常包含关键的交通标志或信号，这些信息对解答题目至关重要。
            注意道路状况：观察道路类型（城市道路、乡村道路、高速公路等）、车道划分、是否有行人、自行车等。
            3. 应用交通法规
            限速规定：根据道路类型和条件，判断正确的限速。
            车道选择：了解各种转弯、直行和变道的车道选择规则。通常左转使用左车道，右转使用右车道。
            优先规则：明确在不同情境下的优先权规则，例如，行人优先、主路优先等。
            4. 安全第一原则
            减速慢行：在有行人、自行车或其他不确定因素的情况下，选择减速慢行。
            保持距离：保持安全跟车距离，防止追尾事故的发生。
            依次通行：遇到信号灯或前车等待时，依次排队等候，不抢道、不超车。
            5. 排除错误选项
            不符合规则：排除那些明显不符合交通法规或安全规则的选项，例如“鸣笛催促”、“加速通过”等。
            不合逻辑：排除那些在现实驾驶中不合逻辑或不切实际的选项。

            交通规则：
            **车速相关规定**：在一般道路上，城市道路和公路的最高车速根据道路类型有所不同：没有中心线的道路限速分别为30 km/h和40 km/h，同方向只有一条机动车道的限速分别为50 km/h和70 km/h。特殊情况：进出非机动车道、通过铁路道口、急弯路、牵引车辆、雨雪天气等条件下，最高时速不得超过30 km/h。
                在高速公路上，小型载客汽车的最高车速为120 km/h，其他机动车为100 km/h，摩托车为80 km/h。高速公路的最低车速为60 km/h，两条车道时左侧车道最低车速为100 km/h，三条以上车道时最左侧车道为110 km/h，中间车道为90 km/h。
            **交通标志特征**：交通标志的形状和颜色具有明确的规律性。正等边三角形用于警告标志，圆形用于禁令和指示标志，倒等边三角形表示“减速让行”，八角形表示“停车让行”，叉形用于铁路平交道口警告，方形用于指路、警告、禁令等标志。
                颜色方面，红色表示禁止和危险，黄色表示警告，蓝色和绿色用于指示和指路，棕色用于旅游区指示，黑色和白色用于标志的文字和边框，荧光黄绿色用于注意行人和儿童的警告标志。
	            禁止停车：蓝色圆圈中有红色叉，表示禁止停车。
	            禁止通行：红色圆圈中有红色斜杠，表示禁止一切车辆通行。
	            禁止机动车驶入：红色圆圈中有黑色小汽车和红色斜杠，表示禁止机动车驶入。
	            指示停车：蓝色圆圈中有白色“P”字母，表示允许停车。
	            停车检查：红色圆圈中有黑色车和指示符号，表示停车检查。
	            注意行人：黄色三角形，黑色边框和人形符号，表示前方有行人经过。
	            注意儿童：黄色三角形，黑色边框和两个儿童图案，表示注意儿童。
	            前方村庄或集镇：黄色三角形，黑色边框和房子符号，提醒前方有村庄或集镇。
	            道路变窄：黄色三角形，黑色边框和逐渐变窄的黑色线条，提醒前方道路变窄。
	            限速50公里：蓝色圆圈中有白色“50”数字。
	            解除时速40公里限制：白色圆圈中有黑色“40”数字和黑色斜杠，表示解除限速。
	            紧急停车带：绿色矩形标志，中心有白色车辆图案和文字，表示紧急停车区。
	            会车让行：黄色三角形，黑色边框和上下黑色箭头，表示会车时让行。
	            注意隧道：黄色三角形，黑色边框和隧道图案，表示前方有隧道，提醒减速慢行。
	            禁止驶入：红色圆圈，白色背景和红色横线，表示禁止驶入。
	            直行标志：蓝色圆圈中有白色向上箭头，表示只允许直行。
	            减速让行：倒等边三角形，红色边框和黑色“让”字，表示减速并让行。
	            停车让行：红色八角形，白色边框和白色“停”字，表示停车让行。
	            注意火车：白色背景，红色交叉斜杠，表示前方铁路平交道口，提醒注意火车通行。
            **交通标线**：道路标线有白色和黄色，形式有虚线和实线。白色虚线分隔同向交通流或引导车辆，白色实线作为车道边缘线或停止线。黄色虚线分隔对向交通流，黄色实线标示禁停区或专用车道。双白虚线为减速让行线，双黄虚线为禁止超车线，蓝色虚线为非机动车道，橙色虚线用于作业区。
            **车道划分**：同方向有两条以上车道时，左侧为快速车道，右侧为慢速车道，摩托车应在最右侧车道行驶，变更车道时不影响其他车辆。专用车道仅允许特定车辆通行。
            **交叉路口通行**：按交通信号灯、标志或警察指挥通行。无信号灯时减速慢行，让右方车辆先行，避免交通堵塞。
            **铁路道口和人行横道**：按信号或管理人员指挥通行，通过人行横道时减速，让行人优先。
            **会车规定**：无中心隔离或中线的道路上，车辆相向行驶时应减速并保持安全距离。遇障碍时无障碍方先行；狭窄坡路上上坡车优先，狭窄山路上不靠山体一方先行。夜间会车在150米外切换近光灯。
            **超车规定**：提前开启左转向灯，变道超车后开启右转向灯返回原车道。禁止在前车转弯、掉头、超车，可能与对向车相遇或遇特种车辆时超车。铁路道口、交叉路口、窄桥等地也禁止超车。
            **掉头规定**：禁止在有禁止标志、标线及危险区域掉头。允许掉头时需确保不妨碍其他车辆和行人。
            **停车规定**：临时停车不得妨碍交通，应靠道路右侧停放，优先使用停车泊位。禁止在铁路道口、交叉路口等危险路段及有禁停标志的地方停车。长时间停车时，驾驶员不得离车，需紧靠道路右侧。
            **转向灯使用**：转向、变道、停靠等操作前需提前使用相应转向灯，确保其他道路使用者了解行驶意图。
            **照明灯使用**：夜间或低能见度天气应开启前照灯、示廓灯和后位灯。近距离跟车时不得用远光灯，夜间通过复杂路况或无信号灯路口时应交替使用远近光灯。驾驶员疲劳时应停车休息。
            **特殊情况**：道路养护作业时遵守限速和标线规定，积水路段应停车观察后缓慢通过。特种车辆执行紧急任务时其他车辆应让行。交通事故时开启危险报警闪光灯，并在车后设置警告标志。
            **安全驾驶**：驾驶员和乘客应使用安全带和安全头盔，驾驶时门窗需关闭，视线范围内不得有遮挡物，严禁使用手机或观看电视。车辆不得随意掉头、拖拉物品或载人货物，连续驾驶不超过4小时，休息不少于20分钟，禁止在禁鸣区鸣笛。
            机动车信号灯：绿灯：允许通行，但转弯时需注意避让直行车辆和行人。黄灯：警示信号，不应通行，但已越过停止线的可继续通行。红灯：禁止通行，但右转弯在不妨碍被放行的车辆和行人时可以通行。
            车道信号灯：绿色箭头：允许车辆按箭头指示方向通行。红色叉形或箭头：禁止车辆驶入该车道。
            方向指示信号灯：绿色箭头：允许车辆按箭头指示方向通行。红色箭头：禁止车辆按该方向通行。
            闪光警告信号灯：黄灯闪烁：提醒车辆和行人注意，谨慎通行。
            道路与铁路平面交叉道口信号灯：两个红灯交替闪烁或一个红灯亮：禁止车辆和行人通行。红灯熄灭：允许车辆和行人通行。
            --
            现在请根据给出的图片和问题，一步步进行推理分析。"""
        
        prompt = system_prompt + text_prompt + "请先一步一步思考，最后再回答问题"
    
    elif any(keyword in text_prompt for keyword in ["angle", "角度", "函数", "function", "equation", "方程", "triangle", "三角形", "coordinate", "正方体"]):
        system_prompt = """
            背景：你是一位数学专家，了解高中数学的所有知识，接下来你需要解答一些高中数学题，以下是一些基础知识可以给你提供一些帮助。
            ### 一. 函数的单调性与极值
            #### 单调性
            函数在某区间内是单调递增或递减的。判断单调性的步骤如下：
            - **求导数**：计算函数的导数 \( f'(x) \)。
            - **确定符号**：分析导数在各个区间的符号。
            - 若 \( f'(x) > 0 \)，则函数在该区间单调递增。
            - 若 \( f'(x) < 0 \)，则函数在该区间单调递减。
            **例子**：求函数 \( f(x) = x^3 - 3x + 1 \) 的单调区间。
            - **解法**：
            - 求导数：\( f'(x) = 3x^2 - 3 \)。
            - 解不等式：令 \( f'(x) > 0 \) 和 \( f'(x) < 0 \) 分别求解。
                - \( 3x^2 - 3 > 0 \Rightarrow x > 1 \) 或 \( x < -1 \)。
                - \( 3x^2 - 3 < 0 \Rightarrow -1 < x < 1 \)。
            函数在 \( (-\infty, -1) \) 和 \( (1, \infty) \) 上单调递增，在 \( (-1, 1) \) 上单调递减。
            #### 极值
            函数在某点取到的局部最大值或最小值。判断极值的步骤如下：
            - **求导数**：计算函数的导数 \( f'(x) \) 并求出其零点。
            - **二阶导数判断法**：
            - 若 \( f''(x) > 0 \)，则 \( x \) 处为极小值。
            - 若 \( f''(x) < 0 \)，则 \( x \) 处为极大值。
            **例子**：求函数 \( f(x) = x^3 - 3x + 1 \) 的极值点。
            - **解法**：
            - 求导数：\( f'(x) = 3x^2 - 3 \)，令 \( f'(x) = 0 \)，得 \( x = \pm 1 \)。
            - 二阶导数：\( f''(x) = 6x \)，
                - \( f''(1) = 6 > 0 \)，所以 \( x = 1 \) 处有极小值。
                - \( f''(-1) = -6 < 0 \)，所以 \( x = -1 \) 处有极大值。
            ### 二、三角函数
            #### 1. 三角函数的基本性质
            - **周期性**：三角函数具有周期性。
            - \(\sin(x + 2k\pi) = \sin x\)
            - \(\cos(x + 2k\pi) = \cos x\)
            - \(\tan(x + k\pi) = \tan x\)
            - **对称性**：
            - \(\sin(-x) = -\sin x\)
            - \(\cos(-x) = \cos x\)
            - \(\tan(-x) = -\tan x\)
            - **诱导公式**：
            - \(\sin(\pi - x) = \sin x\)
            - \(\cos(\pi - x) = -\cos x\)
            - \(\tan(\pi - x) = -\tan x\)
            #### 2. 三角恒等变换
            - **常用公式**：
            - \(\sin^2 x + \cos^2 x = 1\)
            - \(\sin 2x = 2\sin x \cos x\)
            - \(\cos 2x = \cos^2 x - \sin^2 x\)
            - **解法**：利用这些公式进行化简或求值。
            **例子**：化简 \( \sin^2 x - \cos^2 x \)。
            - **解法**：
            - 使用公式 \(\sin^2 x + \cos^2 x = 1\)，所以 \(\cos^2 x = 1 - \sin^2 x\)。
            - 因此，\(\sin^2 x - \cos^2 x = \sin^2 x - (1 - \sin^2 x) = 2\sin^2 x - 1\)。
            ### 三、数列
            #### 1. 等差数列与等比数列
            - **等差数列**：
            - **通项公式**：\( a_n = a_1 + (n-1)d \)
            - **前 \( n \) 项和公式**：\( S_n = \frac{n}{2} (a_1 + a_n) \)
            **例子**：求等差数列 \( 2, 5, 8, \ldots \) 的第 10 项。
            - **解法**：
            - \( a_1 = 2 \)，\( d = 3 \)
            - 第 10 项：\( a_{10} = 2 + (10-1) \times 3 = 2 + 27 = 29 \)
            - **等比数列**：
            - **通项公式**：\( a_n = a_1 r^{n-1} \)
            - **前 \( n \) 项和公式**：\( S_n = a_1 \frac{1 - r^n}{1 - r} \)
            **例子**：求等比数列 \( 3, 6, 12, \ldots \) 的第 5 项。
            - **解法**：
            - \( a_1 = 3 \)，\( r = 2 \)
            - 第 5 项：\( a_5 = 3 \times 2^{5-1} = 3 \times 16 = 48 \)
            ### 四、解析几何
            #### 1. 直线与圆
            - **直线方程**：
            - **点斜式**：\( y = kx + b \)
            - **斜截式**：\( y = mx + c \)
            - **一般式**：\( Ax + By + C = 0 \)
            **例子**：求过点 \( (1,2) \) 和 \( (3,4) \) 的直线方程。
            - **解法**：
            - 求斜率：\( k = \frac{4-2}{3-1} = 1 \)
            - 代入点斜式方程：\( y - 2 = 1(x - 1) \)
            - 化简得到：\( y = x + 1 \)
            - **圆的方程**：
            - **标准式**：\( (x - h)^2 + (y - k)^2 = r^2 \)
            **例子**：求圆心为 \( (2, -1) \)，半径为 3 的圆的方程。
            - **解法**：
            - 圆心 \( (h, k) = (2, -1) \)，半径 \( r = 3 \)
            - 代入标准式方程：\( (x - 2)^2 + (y + 1)^2 = 9 \)
            ### 七、导数与微分
            #### 1. 导数的定义与计算
            - **导数定义**：函数 \( f(x) \) 在点 \( x_0 \) 处的导数定义为
            \[ f'(x_0) = \lim_{h \to 0} \frac{f(x_0 + h) - f(x_0)}{h} \]
            **例子**：求 \( f(x) = x^2 \) 在 \( x = 2 \) 处的导数。
            - **解法**：
            - 直接计算导数：\( f'(x) = 2x \)
            - 在 \( x = 2 \) 处的导数：\( f'(2) = 2 \times 2 = 4 \)
            #### 2. 导数的应用
            - **单调性与极值**：利用导数判断函数的单调区间和极值点。
            **例子**：求 \( f(x) = x^3 - 3x + 1 \) 的极值点。
            - **解法**：
            - 求导数：\( f'(x) = 3x^2 - 3 \)，令 \( f'(x) = 0 \)，得 \( x = \pm 1 \)
            - 二阶导数：\( f''(x) = 6x \)
                - \( f''(1) = 6 > 0 \)，所以 \( x = 1 \) 处有极小值
                - \( f''(-1) = -6 < 0 \)，所以 \( x = -1 \) 处有极大值
    """
       
        prompt = system_prompt + "You are very good at mathematical analysis" + text_prompt + "Before answering the question, let's think step by step."
    else:
        prompt = text_prompt + "Before answering the question, let's think step by step."


    response, history = model.chat(tokenizer, pixel_values, prompt, generation_config, history=None, return_history=True)
    
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

    # # preprocess the ans
    if single_choice_eval(response) is None:
        print("no answer")
        # prompt = text_prompt + "please double check the answer and select a letter from (A, B, C, D)"
        prompt = text_prompt + "请从(A, B, C, D)中选择一个选项"
        response, history = model.chat(tokenizer, pixel_values, prompt, generation_config, history=history, return_history=True)
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






