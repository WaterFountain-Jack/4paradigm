import re
import string

single_choice_answer_pattern = [re.compile(p) for p in [
        r"{?'?answer'?:'?([A-Z])'?.*?$",
        r"^\s*([A-Z])\s*[。\.]?$",
        r"([A-Z])\s?是正确的",
        r"([A-Z])\s?[是为]正确答案",
        r"[\s，：:,]([A-Z])[。，,\.]?$",
        r"[\s，,：:]因此([A-Z])[。\.]?$",
        r"[\s，,：:][故即]([A-Z])[。\.]?$",
        r"只有选?项?\s?([A-Z])\s?是?对",
        r"因此\s?([A-Z])[。\.]?$",
        r"所以\s?([A-Z])[。\.]?$",
        r"所以答\s?([A-Z])",
        r"所有\s?([A-Z])[。\.]?$",
        r"显然\s?([A-Z])[。\.]?$",
        r"正确的一项是\s?([A-Z])",
        r"正确的?选?项?是?\s?([A-Z])",
        r"答案[:：]?\s?选?项?\s?([A-Z])",
        r"答案为[:：]?\s?选?项?\s?([A-Z])",
        r"答案应为[:：]?\s?选?项?\s?([A-Z])",
        r"答案应该是[:：]?\s?选?项?\s?([A-Z])",
        r"答案应该?[是选]\s?([A-Z])",
        r"答案是?\s?[:：]?\s?([A-Z])",
        r"答案是[:：]?\s?选?项?\s?([A-Z])",
        r"答案选\s?选?项?\s?([A-Z])",
        r"^选([A-Z])",
        r"故?选[:：]?\s?([A-Z])[。\.]?$",
        r"选择\s?([A-Z])",
        r'选择答案([A-Z])',
        r"^选项([A-Z])",
        r"选项\s?([A-Z])\s?正确",
        # 下面摘英文结果的时候，暂时先是用之摘[A,B,C,D]
        r"[Tt]hecorrectansweris:?([A-D])\s?",
        r"[Tt]hecorrectstatementis:?([A-D])\s?",
        r"[Tt]hecorrectoptionis:?([A-D])\s?",
        r"[Tt]hecorrectstatementis:?([A-D])\s?",
        r"[Tt]hecorrectconclusionis:?([A-D])\s?",
        r"[Tt]hecorrectanswerisoption:?([A-D])\s?",
        r"[Tt]heansweris:?([A-D])\s?",
        r"([A-D])\s?isthecorrectanswer",
        r"[Yy]our_Answer:?([A-D])\s?",
        r"{?'?correct'?:'?([A-D])'?.*?$",
    ]]
def normalize_answer(s):
    def white_space_fix(text):
        return ''.join(text.split())
    def remove_punc(text):
        exclude=set(list(string.punctuation))
        return ''.join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return white_space_fix(remove_punc(lower(s))) if s is not None else None

def single_choice_eval(predict, options = None):
    if predict is None or len(predict) == 0:
        return ''
    try:
        pred_str = ''.join(predict)
    except Exception as e:
        return ''
    pred_str = pred_str.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('"',"'").replace(']','').replace('[', '').replace('，', ',').replace('、', ',')
    choice = None
    for regex in single_choice_answer_pattern:
        match = regex.search(pred_str)
        if match:
            choice = match.group(1)
            break
    if choice is None:
        if options is not None:
            for k,v in options.items():
                if normalize_answer(pred_str).strip(',.;?!，。；？！、') == \
                          normalize_answer(v).strip(',.;?!，。；？！、'):
                    choice = k
    if choice is None:
        if pred_str != None:
            for x in pred_str:
                if x in [chr(i) for i in range(ord('A'), ord('E') + 1)]:
                    choice = x;break;

    if normalize_answer(choice) == None:
        return None
        
    return normalize_answer(choice).upper()

 
predict = "Noneoftheoptionscanbeconfirmedascorrectbasedontheinformationprovidedinthetable."
print(single_choice_eval(predict, options = None))