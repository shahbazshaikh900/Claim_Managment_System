from utils.excel_reader import read_excel

df = read_excel("Claim Register NDS 52000959 (2).XLSX")

if df is not None:
    print(df.head())