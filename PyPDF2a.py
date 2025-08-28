from PyPDF2 import PdfMerger

merger = PdfMerger()

# 結合したいPDFファイルを追加
merger.append("履歴書(平野　裕也).pdf")
merger.append("職務経歴書(平野　裕也).pdf")

# 出力ファイル
merger.write("履歴書_職務経歴書(平野　裕也).pdf")
merger.close()
