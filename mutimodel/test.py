import torch
from PIL import Image
from modelscope import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained('/mnt/data/minjixin/model/MiniCPM-Llama3-V-2_5', trust_remote_code=True, torch_dtype=torch.float16)
model = model.to(device='cuda')

tokenizer = AutoTokenizer.from_pretrained('/mnt/data/minjixin/model/MiniCPM-Llama3-V-2_5', trust_remote_code=True)
model.eval()

image = Image.open('./example/image3.jpg').convert('RGB')
#question = "Take a deep breath, 请回答图片中的问题, Before answering the question, let's think step by step."
question = "如图,AB是⊙O的直径,C,D两点在⊙O上,如果∠C=40°,那么∠ABD的度数为()\nA. 40°\nB. 50°\nC. 70°\nD. 80°"
msgs = [{'role': 'user', 'content': question}]

res = model.chat(
    image=image,
    msgs=msgs,
    tokenizer=tokenizer,
    sampling=True, # if sampling=False, beam_search will be used by default
    temperature=0.7,
    # system_prompt='' # pass system_prompt if needed
)
print(res)

## if you want to use streaming, please make sure sampling=True and stream=True
## the model.chat will return a generator
# res = model.chat(
#     image=image,
#     msgs=msgs,
#     tokenizer=tokenizer,
#     sampling=True,
#     temperature=0.7,
#     stream=True
# )

# generated_text = ""
# for new_text in res:
#     generated_text += new_text
#     print(new_text, flush=True, end='')