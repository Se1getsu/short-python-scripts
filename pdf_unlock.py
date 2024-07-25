# 【内容】
# パスワード付きのPDFファイルのパスワードを解除して保存します。
# 例: py pdf_unlock.py qwerty *.pdf
#   カレントディレクトリのPDFファイルを qwerty というパスワードで解除し、
#   その場に unlocked というディレクトリを作成して、解除したPDFファイルをそこに保存する。

import os
import sys
from PyPDF2 import PdfReader, PdfWriter

def unlock_pdf(input_pdf, output_pdf, password):
    try:
        reader = PdfReader(input_pdf)
        if reader.is_encrypted:
            reader.decrypt(password)

        writer = PdfWriter()
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

        print(f"{input_pdf} unlocked successfully.")
    except Exception as e:
        print(f"Error unlocking {input_pdf}: {e}")

def main(pdf_files, password):
    output_dir = 'unlocked'
    os.makedirs(output_dir, exist_ok=True)

    for pdf_file in pdf_files:
        output_pdf = os.path.join(output_dir, os.path.basename(pdf_file))
        unlock_pdf(pdf_file, output_pdf, password)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pdf_unlock.py <password> <file1.pdf> <file2.pdf> ...")
        sys.exit(1)

    password = sys.argv[1]
    pdf_files = sys.argv[2:]
    main(pdf_files, password)
