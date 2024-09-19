from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from train_data_ft import table_info,train_data,test_data,db_type
from prompt import get_system_prompt,get_role_prompt
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

tokenizer = AutoTokenizer.from_pretrained("/app1/deepseek-coder-33b-instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("/app1/deepseek-coder-33b-instruct", trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()


for a_test_data in test_data:
    system_prompt = get_system_prompt(db_type)
    example = train_data[0:5]
    role_prompt = get_role_prompt(table_info,a_test_data,example,db_type)
    messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": role_prompt}],

    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model.device)
    # tokenizer.eos_token_id is the id of <|EOT|> token
    outputs = model.generate(inputs, max_new_tokens=512, do_sample=False, top_k=50, top_p=0.95, num_return_sequences=1, eos_token_id=tokenizer.eos_token_id)
    print(tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True))



