## Precise Question-Answer Validation using RAG Technology and Prompt Engineering

**Abstract**

This project bulk reads PDF documents and converts them into TXT indexes based on dual-column layout. It then calculates highly similar content using FAISS indexing, interacts with the Tongyi Qianwen model through prompt engineering to obtain results, and finally saves the results to a CSV file.

**Project Overview**

QueryMaster efficiently handles question-answer validation tasks for PDF documents through the following steps:

1. **Document Preprocessing**: Batch conversion of PDF documents into TXT documents based on dual-column layout.
2. **Index Building**: Efficient similarity retrieval of text using FAISS.
3. **Question-Answer Validation**: Interaction with the Tongyi Qianwen model through prompt engineering to obtain validation results.
4. **Result Output**: Saving question-answer validation results to a CSV file for easy analysis.

**Directory Structure**

```
├── algorithm
│   ├── code files 
│   │   ├── compute_graph.py
│   │   ├── kws_config.json
│   │   ├── main.py
│   │   ├── organize_text.py
│   │   ├── path.py
│   │   ├── pdf2txt.py
│   │   ├── requirements.txt
│   │   └── txt2embedding.py
│   └── algorithm execution documentation 
│       ├── README.md
│       └── README.pdf
└── data
    └── sample_result.csv
```

**Environment Dependencies**

Running this project requires installation of the following libraries:

- Python 3.x
- faiss
- pandas
- numpy
- argparse
- tqdm
- pdfplumber

It is recommended to install dependencies via `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Running the Program**

```bash
python main.py --convert_pdfs True --prepare_index True --convert_index True --batch_size 4 --query_answer True
```

**Parameter Descriptions**

- `--convert_pdfs`: Whether to convert PDF files to TXT documents, default is `False`
- `--prepare_index`: Whether to preprocess index files, default is `False`
- `--convert_index`: Whether to convert index vectors, default is `False`
- `--batch_size`: Batch size for text vectorization, default is `4`
- `--query_answer`: Whether to query answers using the Tongyi Qianwen model API, default is `False`

**Additional Information**

* **m3e-base**

m3e-base is a multilingual embedding model designed for efficient text vectorization. It supports multiple languages and is optimized for creating high-quality text embeddings suitable for various natural language processing tasks. You can find more information and obtain the model at [https://huggingface.co/moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base).

* **Tongyi Qianwen API**

Tongyi Qianwen is a powerful language model API developed by Alibaba Cloud, capable of understanding and generating human-like text replies. It is widely used in question-answer systems, chatbots, and various applications. For detailed information and API access guidelines, please refer to [https://help.aliyun.com/zh/dashscope/developer-reference/api-details](https://help.aliyun.com/zh/dashscope/developer-reference/api-details).

