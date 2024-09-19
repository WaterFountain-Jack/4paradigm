from transformers import AutoTokenizer, AutoModel
import torch
import torchvision.transforms as T
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from internvl.model.internvl_chat import InternVLChatModel

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform


def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio


def dynamic_preprocess(image, min_num=1, max_num=6, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # calculate the existing image aspect ratio
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # find the closest aspect ratio to the target
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # calculate the target width and height
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # resize the image
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images


def load_image(image_file, input_size=448, max_num=6):
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values




# path = "/mnt/data/minjixin/model/InternVL-Chat-V1-5"
# # If you have an 80G A100 GPU, you can put the entire model on a single GPU.
# # model = AutoModel.from_pretrained(
# #     path,
# #     torch_dtype=torch.bfloat16,
# #     low_cpu_mem_usage=True,
# #     trust_remote_code=True).eval().cuda()
# # Otherwise, you need to set device_map='auto' to use multiple GPUs for inference.
# import os
# os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
# model = AutoModel.from_pretrained(
#     path,
#     torch_dtype=torch.bfloat16,
#     low_cpu_mem_usage=True,
#     trust_remote_code=True,
#     device_map='auto').eval()

# tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
# # set the max number of tiles in `max_num`
# pixel_values = load_image('./example/images/1.jpg', max_num=6).to(torch.bfloat16).cuda()

# generation_config = dict(
#     num_beams=2,
#     max_new_tokens=1024,
#     do_sample=False,
#     temperature = 1
# )

# text_prompt = "In 2005, 80% of the Central City School Districts total expenditures came from local property taxes, and the rest came from the state government`s Aid to Schools Program. If the state had reduced its aid to the district by 50%, by what percentage would local property taxes have had to be increased in order for the district to maintain the same level of expenditures? options:'A':0.1,'B':0.125,'C':0.2,'D':0.5."
# question = "Take a deep breath" + text_prompt + "Before answering the question, let's think step by step." 
# initial_response = model.chat(tokenizer, pixel_values, question, generation_config)
# print(question, initial_response)

# # Assuming initial_response contains the analysis
# analysis_based_question = f"Based on the analysis: '{initial_response}', extract and directly answer the options."
# placeholder_pixel_values = torch.zeros_like(pixel_values)
# # Generate the final response based on the analysis
# final_response = model.chat(tokenizer, placeholder_pixel_values, analysis_based_question, generation_config)
# print(final_response)

# path = '/mnt/data/minjixin/internvl_chat/work_dirs/internvl_chat_v1_5_lora/checkpoint-1000/'
# # path = '/mnt/data/minjixin/internvl_chat/work_dirs/internvl_chat_v1_5_lora/'
# path = "/mnt/data/minjixin/model/InternVL-Chat-V1-5"
# #path = '/mnt/data/minjixin/model/vlm/InternVL2-26B/'
# #path = '/mnt/data/guanyandong/models/InternVL2-40B/'
# model = AutoModel.from_pretrained(
#     path,
#     torch_dtype=torch.bfloat16,
#     low_cpu_mem_usage=True,
#     trust_remote_code=True,
#     device_map='auto').eval()

# # model = InternVLChatModel.from_pretrained(
# #     path, low_cpu_mem_usage=True, torch_dtype=torch.bfloat16).eval()
# # model = model.cuda()
# tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
# # set the max number of tiles in `max_num`
# pixel_values = load_image('./example/images/15.png', max_num=6).to(torch.bfloat16).cuda()

# # generation_config = dict(
# #     num_beams=1,
# #     max_new_tokens=1024,
# #     do_sample=False,
# # )

# # # # # pure-text conversation (纯文本对话)
# # # # question = 'Hello, who are you?'
# # # # response, history = model.chat(tokenizer, None, question, generation_config, history=None, return_history=True)
# # # # print(f'User: {question}')
# # # # print(f'Assistant: {response}')

# # # # single-image single-round conversation (单图单轮对话)
# # # # question = "You are very good at mathematical analysis, 请回答图片中的问题, Before answering the question, let's think step by step." 
# # # # question = "如图,AB是⊙O的直径,C,D两点在⊙O上,如果∠C=40°,那么∠ABD的度数为()\nA. 40°\nB. 50°\nC. 70°\nD. 80°"

# # # #question = "请回答图片中的问题，请先一步一步思考，最后再回答问题"

# # # #text_prompt1 = "In 2005, 80% of the Central City School Districts total expenditures came from local property taxes, and the rest came from the state government`s Aid to Schools Program. If the state had reduced its aid to the district by 50%, by what percentage would local property taxes have had to be increased in order for the district to maintain the same level of expenditures? options:'A':0.1,'B':0.125,'C':0.2,'D':0.5."
# # # #text_prompt3 = "The revenue from lottery ticket sales is divided between prize money and the various uses shown in the graph labeled \"Proceeds.\" In 2009, what percent of the money spent on tickets was returned to the purchasers in the form of prize money? options: A:0.235, B:0.5, C:0.6, D: 0.66."
# # # #text_prompt6 = "In how many years from 2001 through 2008, inclusive, did the sales of ABC Mega Stores exceed the average of the annual sales during that period? options: A:3, B:4, C:5, D:6."
# # # #text_prompt9 = "In which of the following pairs of years were the ratios of Republican receipts to Democratic receipts most nearly equal? options: A:1981-82 and 1985-86, B:1983-84 and 1995-96, C:1987-88 and 1989-90, D:1987-88 and 1995-96."
# text_prompt15 = "Based on the figure, which statements are true?\nChoose all that apply. options: A:The median value of the popular vote for Clinton was less than the median value of the popular vote for Bush., B:The range of the popular vote for Bush was greater than the range of the popular vote for Clinton., C:The percent of the popular vote received by Bush in each state was less than the percent received by Clinton in each state., D:The popular vote received by Perot in each state was at least half of the popular vote received by Bush in each state."
# question = "Take a deep breath." + text_prompt15 + "Before answering the question, let's think step by step." 
# response = model.chat(tokenizer, pixel_values, question, generation_config)
# print(f'User: {question}')
# print(f'Assistant: {response}')


# # Assuming initial_response contains the analysis
# analysis_based_question = f"Based on the analysis: '{response}', extract and directly answer the options."
# placeholder_pixel_values = torch.zeros_like(pixel_values)
# # Generate the final response based on the analysis
# final_response = model.chat(tokenizer, placeholder_pixel_values, analysis_based_question, generation_config)
# print(f'final response: {final_response}')