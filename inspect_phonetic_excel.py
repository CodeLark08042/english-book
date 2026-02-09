import pandas as pd

file_path = r"d:\考研学习\英语\绿皮书单词\单词书\绿皮书1-50（音标版）.xlsx"

try:
    df = pd.read_excel(file_path, header=None)
    print("Shape:", df.shape)
    print("First 5 rows:")
    print(df.head())
except Exception as e:
    print("Error:", e)
