import os
import re
import pandas as pd

def process_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

        # 去除换行符
        text = text.replace('\n', '')

        # 去除中文字符和英文字符之间的空格处理
        text = re.sub(r'([\u4e00-\u9fa5])(\s+)([a-zA-Z])', r'\1\3', text)
        text = re.sub(r'([a-zA-Z])(\s+)([\u4e00-\u9fa5])', r'\1\3', text)

        # 在句子结尾添加换行符
        text = re.sub(r'([。.;；])', r'\1\n', text)

        return text


def process_index_txt_directory(directory):

    output_file = 'index.txt'
    with open(output_file, 'w', encoding='utf-8') as out:
        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    processed_text = process_text(file_path)

                    # 分割文本为行，过滤掉小于等于3个字符的行
                    lines = processed_text.splitlines()
                    filtered_lines = [line for line in lines if len(line) > 30]

                    # 将过滤后的行写入输出文件
                    out.write('\n'.join(filtered_lines) + '\n\n')

    print(f'文件已保存：{output_file}')



def replace_column_content(file_path, output_path):
    """
    整理对话模型api返回的csv result文件
    :param file_path:  要整理的csv文件路径
    :param output_path:  输出csv文件路径
    :return:
    """
    df = pd.read_csv(file_path)

    # 定义一个函数，用于提取两个$符号之间的内容
    def extract_between_dollars(text):
        match = re.search(r'\$(.*?)\$', text)
        return match.group(1) if match else text


    df.iloc[:, 1] = df.iloc[:, 1].apply(extract_between_dollars)

    df.to_csv(output_path, index=False)

