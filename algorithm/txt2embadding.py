from sentence_transformers import SentenceTransformer
from path import model_path
from tqdm import tqdm
import numpy as np
import faiss

model = SentenceTransformer(model_path)
print(f'---------------model loaded---------------')


def txt2embedding(input_txt, batch_size, output_file_name):
    sentences = input_txt
    batch_size = batch_size
    total_batches = (len(sentences) + batch_size - 1) // batch_size  # 计算总批次数，向上取整

    embeddings = []

    # 使用 tqdm 显示进度条
    with tqdm(total=total_batches, desc='Encoding sentences') as pbar:
        for i in range(0, len(sentences), batch_size):
            batch_sentences = sentences[i:i + batch_size]  # 获取当前批次的句子列表
            batch_embeddings = model.encode(batch_sentences)  # 编码当前批次的句子
            embeddings.extend(batch_embeddings)  # 将当前批次的结果添加到总列表中
            pbar.update(1)  


    # 将所有批次的编码结果合并
    encoded_paragraphs = np.vstack(embeddings)

    print(f"Encoded paragraphs shape: {encoded_paragraphs.shape}")

    # 构建和保存FAISS索引，并显示进度条
    dimension = encoded_paragraphs.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(encoded_paragraphs)

    faiss.write_index(index, f"{output_file_name}.faiss")
    print(output_file_name)
    return output_file_name
