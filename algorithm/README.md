## 利用 RAG 技术和 Prompt 工程实现精准问答验证

**摘要**

本项目批量读取 PDF 文档并将它们转换为基于双栏布局的 TXT 索引。 然后使用 FAISS 索引计算高度相似的内容，通过 Prompt 工程与同义千问模型进行对话以获取结果，最后将结果保存到 CSV 文件中。

**项目概览**

QueryMaster 能够帮助您高效处理 PDF 文档的问答验证任务，通过以下步骤完成：

1. **文档预处理** 将 PDF 文档批量转换为基于双栏布局的 TXT 文档
2. **索引构建** 利用 FAISS 对文本进行高效相似度检索
3. **问答验证** 基于 Prompt 工程与同义千问模型进行交互，获取问答验证结果
4. **结果输出** 将问答验证结果保存到易于分析的 CSV 文件

**目录结构**

```
A:
├── algorithm
│   ├── 代码文件 
│   │   ├── compute_graph.py
│   │   ├── kws_config.json
│   │   ├── main.py
│   │   ├── organize_text.py
│   │   ├── path.py
│   │   ├── pdf2txt.py
│   │   ├── requirements.txt
│   │   └── txt2embadding.py
│   ├── 算法说明文档 
│   │   ├── 算法设计.md
│   │   └── 算法设计.pdf 
│   └── 算法运行说明文档 
│       ├── README.md
│       └── README.pdf
└── data
    └── sample_result.csv
```

**环境依赖**

运行本项目需要安装以下依赖库：

- Python 3.x
- faiss
- pandas
- numpy
- argparse
- tqdm
- pdfplumber

推荐使用 requirements.txt 文件一键安装：

```bash
pip install -r requirements.txt
```

**运行程序**

```bash
python main.py --convert_pdfs True --prepare_index True --convert_index True --batch_size 4 --query_answer True
```

**参数说明**

- `--convert_pdfs`：是否将 PDF 文件转换为 TXT 文档，默认为 `False`
- `--prepare_index`：是否预处理索引文件，默认为 `False`
- `--convert_index`：是否转换索引向量，默认为 `False`
- `--batch_size`：文本向量化的批处理大小，默认为 `4`
- `--query_answer`：是否使用同义千问模型 API 进行问答查询，默认为 `False`


**附加信息**

* **m3e-base**

m3e-base 是一个用于高效文本向量化的多语言嵌入模型。 它支持多种语言，并针对创建适合各种自然语言处理任务的高质量文本嵌入进行了优化。 您可以在 huggingface 官网了解更多信息并获取模型 [https://huggingface.co/moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base)。

* **同义千问 API**

同义千问是阿里云开发的一款功能强大的语言模型 API，能够理解和生成类人文本回复。 它广泛用于问答系统、聊天机器人等各种应用。 详细信息和 API 访问指南请参考 [https://help.aliyun.com/zh/dashscope/developer-reference/api-details](https://help.aliyun.com/zh/dashscope/developer-reference/api-details)。

