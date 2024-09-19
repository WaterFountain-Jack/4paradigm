import re
import string

multiple_choice_answer_conjunct_chars=r';,/，、。，和与\.\'`| :：'
multiple_choice_answer_pattern = [re.compile(p) for p in [
        r"{?'?answer'?:'?([A-Z%s]+)'?.*?$" % multiple_choice_answer_conjunct_chars,
        r"^\s*([A-Z%s]+)\s*[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"([A-Z%s]+)\s?是正确的" % multiple_choice_answer_conjunct_chars,
        r"([A-Z%s]+)\s?是正确答案" % multiple_choice_answer_conjunct_chars,
        r"[\s，：:,]([A-Z%s]+)[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"[\s，,：:]因此([A-Z%s]+)[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"[\s，,：:][故即]([A-Z%s]+)[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"只有选?项?\s?([A-Z%s]+)\s?是?对" % multiple_choice_answer_conjunct_chars,
        r"因此\s?([A-Z%s]+)[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"所以\s?([A-Z%s]+)[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"所以答\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"所有\s?([A-Z%s]+)[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"显然\s?([A-Z%s]+)[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"正确的一项是\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"正确的?选?项?是?\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"答案[:：]?\s?选?项?\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"答案为[:：]?\s?选?项?\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"答案应为[:：]?\s?选?项?\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"答案应该是[:：]?\s?选?项?\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"答案应该?[是选]\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"答案是?\s?[:：]?\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"答案是[:：]?\s?选?项?\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"答案选\s?选?项?\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"^选([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"^故选([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"选\s?([A-Z%s]+)[。\.]?$" % multiple_choice_answer_conjunct_chars,
        r"选择\s?([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r'选择答案([A-Z%s]+)' % multiple_choice_answer_conjunct_chars,
        r"^选项([A-Z%s]+)" % multiple_choice_answer_conjunct_chars,
        r"选项\s?([A-Z%s]+)\s?正确" % multiple_choice_answer_conjunct_chars,
        r"正确答案是\s?([A-Z%s]+)\s?都有可能" % multiple_choice_answer_conjunct_chars,
        # 摘英文结果的时候，目前暂时只摘[A,B,C,D]
        r"[Tt]hecorrectansweris:?([A-D%s]+)\s?" % multiple_choice_answer_conjunct_chars,
        r"[Tt]hecorrectstatementis:?([A-D%s]+)\s?" % multiple_choice_answer_conjunct_chars,
        r"[Tt]hecorrectoptionis:?([A-D%s]+)\s?" % multiple_choice_answer_conjunct_chars,
        r"[Tt]hecorrectstatementis:?([A-D%s]+)\s?" % multiple_choice_answer_conjunct_chars,
        r"[Tt]hecorrectconclusionis:?([A-D%s]+)\s?" % multiple_choice_answer_conjunct_chars,
        r"([A-D%s]+)\s?isthecorrectanswer" % multiple_choice_answer_conjunct_chars,
        r"[Yy]our_Answer:?([A-D%s]+)\s?" % multiple_choice_answer_conjunct_chars,
        r"{?'?correct'?:'?([A-D%s]+)'?.*?$" % multiple_choice_answer_conjunct_chars,
    ]]

anslist=['ABCD','ABC','ABD','ACD','BCD','AB','AC','AD','BD','BC','CD']

def normalize_answer(s):
    def white_space_fix(text):
        return ''.join(text.split())
    def remove_punc(text):
        exclude=set(list(string.punctuation))
        return ''.join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return white_space_fix(remove_punc(lower(s))) if s is not None else None

# def get_last_sentence(text):
#     # 使用正则表达式分割句子，但避免混淆小数点和句点
#     sentences = re.split(r'(?<!\d)\.(?!\d)|[。!?！？]', text)
#     # 去除空字符串
#     sentences = [s for s in sentences if s.strip()]
#     # 返回最后一句
#     return sentences[-1] if sentences else text

def multiple_choice_eval(predict, options=None):

    def get_last_sentence(text):
        # 使用正则表达式分割句子，但避免混淆小数点和句点
        sentences = re.split(r'(?<!\d)\.(?!\d)|[。!?！？]', text)
        # 去除空字符串
        sentences = [s for s in sentences if s.strip()]
        # 返回最后一句
        return sentences[-1] if sentences else text

    if predict is None or len(predict) == 0:
        return ''
    try:
        pred_str = ''.join(predict)
    except Exception as e:
        print(f"Error joining predict: {e}")
        return ''
    
    # 预处理预测结果字符串
    pred_str = pred_str.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('"', "'").replace(']', '').replace('[', '').replace('，', ',').replace('、', ',')
    #print(f"Processed pred_str: {pred_str}")
    
    # 获取最后一句话
    last_sentence = get_last_sentence(pred_str)
    print(f"Last sentence: {last_sentence}")

    choices = None
    for regex in multiple_choice_answer_pattern:
        match = regex.search(last_sentence)
        if match:
            choices = list(filter(lambda x: x != '', re.split(r'[%s]*' % multiple_choice_answer_conjunct_chars, match.group(1))))
            print(f"Matched choices: {choices}")
            break
    
    if choices is None:
        if options is not None:
            choices = []
            norm_pred_str = normalize_answer(pred_str)
            for opt in options:
                if norm_pred_str.find(normalize_answer(options[opt]).strip(',.;?!，。；？！、')) > 0:
                    choices.append(opt)
            #print(f"Choices from options: {choices}")

    if choices is None:
        s = last_sentence.replace(',', '').replace('，', '').replace(';', '').replace('.', '').replace(' ', '').replace('、', '')
        if '不正确' in s:
            s = s[s.rfind('不正确') + 3:]
        for i in anslist:
            if i in s:
                choices = i
                break
        if choices is None:
            for x in s:
                if x in [chr(i) for i in range(ord('A'), ord('D') + 1)]:
                    choices = str(x)
                    break
        #print(f"Choices from additional processing: {choices}")

    t = []
    if choices is not None:
        for i in choices:
            if i not in multiple_choice_answer_conjunct_chars and i != "'":
                t.append(i)
    choices = t
    # print(f"多选题大模型返回结果处理前:\n{pred_str}\n")
    # print(f"多选题大模型返回结果处理后:\n{set([normalize_answer(x) for x in choices])}\n")
    return set([normalize_answer(x) for x in choices])


# predict = "选项A,B和D都是错误的,因为它们与表格中的数据不符"

# print(multiple_choice_eval(predict, options = None))