import http
from sentence_transformers import SentenceTransformer
from path import model_path, qanwen_api_key
import numpy as np
import faiss
import requests
from tqdm import tqdm
import random
from http import HTTPStatus
from tqdm import tqdm
import dashscope
from dashscope import Generation

dashscope.api_key = qanwen_api_key

model = SentenceTransformer(model_path)

def query_graphs(querys, index):
    output_parts = []

    # 使用 tqdm 显示进度条
    with tqdm(total=len(querys), desc='Processing queries') as pbar:
        for query in querys:
            input_sentence = query[1]  # 获取 querys 的第二列，即问题字符串

            # 对输入的句子进行编码
            input_embedding = model.encode([input_sentence])

            # 使用FAISS索引进行搜索
            Distances, Indices = index.search(input_embedding, 5)  # 搜索最近的5个邻居

            # 将问题和搜索结果的索引添加到输出列表
            output_parts.append([input_sentence, Indices[0].tolist()])

            # 更新进度条
            pbar.update(1)

    return output_parts

# 调用通义千问 API 的函数
def call_tongyi_qianwen_api(prompt):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               seed=random.randint(1, 10000),
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        return response["output"]["choices"][0]["message"]["content"]
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return "Error: API request failed"

# 按行读取txt文件的函数
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def query_answers(result, txt_file_path):
    # 读取txt文件内容
    txt_lines = read_txt_file(txt_file_path)
    answers = []

    # 使用 tqdm 显示进度条
    with tqdm(total=len(result), desc='Querying API') as pbar:
        for item in result:
            question = item[0]
            indices = item[1]

            # 根据行号获取对应的段落
            materials = ' '.join([txt_lines[i] for i in indices])

            print(f'{materials}')

            prompt = (f"你好，我这里有一个问题需要你阅读材料后按照格式回答这个问题是否正确。"
                      f"材料：“{materials}”。"
                      f"问题：“{question}”。"
                      f"回答格式实例1：“正确$T$”。"
                      f"回答格式实例1：“错误$F$”。")

            # 调用通义千问的 API
            answer = call_tongyi_qianwen_api(prompt)
            answers.append(answer.strip())

            # 更新进度条
            pbar.update(1)

    return answers