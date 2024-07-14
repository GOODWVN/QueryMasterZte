import os
import pdfplumber
from tqdm import tqdm


def extract_text_from_column(page, left_bound, right_bound):
    """
    从页面的指定列提取文本。

    参数:
    page (pdfplumber.page.Page): PDF页面对象。
    left_bound (float): 列的左边界。
    right_bound (float): 列的右边界。

    返回:
    str: 提取的文本。
    """
    width = page.width
    height = page.height
    crop_box = (left_bound, 0, right_bound, height)
    cropped_page = page.within_bbox(crop_box)
    return cropped_page.extract_text()


def convert_pdf_to_txt(pdf_path, txt_path):
    """
    将 PDF 文件转换为 TXT 文件，考虑双栏排布。
    """
    with pdfplumber.open(pdf_path) as pdf:
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for page in pdf.pages:
                # 计算页面宽度的中间位置
                mid_point = page.width / 2
                # 提取左栏和右栏的文本
                left_text = extract_text_from_column(page, 0, mid_point)
                right_text = extract_text_from_column(page, mid_point, page.width)

                # 将左栏和右栏的文本按顺序写入 TXT 文件
                if left_text:
                    txt_file.write(left_text + '\n')
                if right_text:
                    txt_file.write(right_text + '\n')


def batch_convert_pdfs(pdf_directory, txt_directory):
    """
    批量将目录中的 PDF 文件转换为 TXT 文件。
    """
    if not os.path.exists(txt_directory):
        os.makedirs(txt_directory)

    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    for filename in tqdm(pdf_files, desc="Converting PDFs"):
        pdf_path = os.path.join(pdf_directory, filename)
        txt_filename = filename.replace('.pdf', '.txt')
        txt_path = os.path.join(txt_directory, txt_filename)
        convert_pdf_to_txt(pdf_path, txt_path)

