from PyPDF2 import PdfMerger

merger = PdfMerger()

# 結合したいPDFファイルを追加
merger.append("example1.pdf")
merger.append("example2.pdf")

# 出力ファイル
merger.write("example1_2.pdf")
merger.close()
