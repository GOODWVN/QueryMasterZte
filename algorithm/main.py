import json
import os
import faiss
from compute_graph import query_graphs, query_answers
import argparse
from path import txt_path, pdfs_path, model_path, query_path, txt_file_path
from txt2embadding import txt2embedding
from 知识工程.algorithm.代码文件.organize_text import process_index_txt_directory
from 知识工程.algorithm.代码文件.pdf2txt import batch_convert_pdfs
import pandas as pd
from organize_text import replace_column_content



def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--convert_pdfs',
                        default=False,
                        type=bool,
                        help='Convert pdf to txt documents')

    parser.add_argument('--prepare_index',
                        default=False,
                        type=bool,
                        help='Prepare index txt file')

    parser.add_argument('--conver_index',
                        default=False,
                        type=bool,
                        help='')

    parser.add_argument('--batch_size',
                        default=4,
                        type=int,
                        help='')

    parser.add_argument('--query_answer',
                        default=False,
                        type=bool,
                        help='')

    args = parser.parse_args()
    return args


def config(args):
    # Trim 检查args.datadir字符串的最后一个字符是否为斜杠（/），如果是将该字符从字符串中去除
    if hasattr(args, 'datadir') and args.datadir[-1] == '/':
        args.datadir = args.datadir[:-1]

    # get kwargs
    kws = vars(args)
    if hasattr(args, 'config') and args.config and os.path.exists(kws['config']):
        with open(kws['config']) as f:
            config_kws = json.load(f)
            for k, v in config_kws.items():
                if v:
                    kws[k] = v
            # kws.update(config_kws)
    return kws


def run(kws):

    pdf_directory = pdfs_path  # PDF文件目录
    output_directory = txt_path  # 输出TXT文件目录

    if kws['convert_pdfs']:
        batch_convert_pdfs(pdf_directory, output_directory)
        print(f'#---------------pdfs converted---------------#')

    if kws['prepare_index']:
        process_index_txt_directory(output_directory)
        print((f'#---------------index generated ---------------#'))

    output_file_name = ''  # faiss文件名暂存
    if kws['conver_index']:

        with open('index.txt', 'r', encoding='utf-8') as file:
            index = file.readlines()

        output_file_name = txt2embedding(input_txt=index, batch_size=kws['batch_size'], output_file_name='test_embeddings')  #同时返回faiss索引的名字


    if kws['query_answer']:
        # 加载query
        df = pd.read_csv(query_path)
        query_list = df.values.tolist()

        # 加载FAISS索引
        index = faiss.read_index('test_embeddings.faiss')

        # 返回result = [query][Indices]
        result = query_graphs(querys=query_list, index=index)  # 返回result 列表  "result [sen][]"

        index_txt_file_path = txt_file_path
        # 获取答案
        answers = query_answers(result, txt_file_path= index_txt_file_path)

        # 将答案保存为CSV文件
        output_df = pd.DataFrame({
            'id': range(1, len(answers) + 1),
            'answer': answers
        })
        output_df.to_csv('output_answers.csv', index=False)

        replace_column_content(file_path = 'output_answers.csv', output_path='result.csv')

        print("Results saved to output_answers.csv")

    replace_column_content(file_path='output_answers.csv', output_path='result.csv')

if __name__ == "__main__":
    args = parse_args()
    kws = config(args)

    # 将 kws 保存到 JSON 文件
    with open('kws_config.json', 'w') as json_file:
        json.dump(kws, json_file)

    run(kws)
