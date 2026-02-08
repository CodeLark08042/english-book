import pandas as pd

try:
    file_path = r'd:\考研学习\英语\绿皮书单词\绿皮书1-50.xlsx'
    df = pd.read_excel(file_path)
    print("Columns:", df.columns.tolist())
    print("First 3 rows:", df.head(3).to_dict('records'))
except Exception as e:
    print(f"Error: {e}")
