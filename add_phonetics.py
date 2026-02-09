import pandas as pd
import eng_to_ipa as ipa
import os

file_path = r"d:\考研学习\英语\绿皮书单词\单词书\绿皮书1-50（音标版）.xlsx"

def add_phonetics():
    print(f"Reading {file_path}...")
    try:
        df = pd.read_excel(file_path, header=None)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Create a list to store phonetics
    phonetics = []

    print("Generating phonetics...")
    total_rows = len(df)
    
    for index, row in df.iterrows():
        word = str(row[1]).strip() if pd.notna(row[1]) else ""
        
        # Simple check if it's a word (not empty and not a header like 'list')
        # Row 1 is usually the word column based on inspection
        if word and not word.lower().startswith('list') and pd.notna(row[0]):
             # Get IPA
             # convert returns IPA string. If not found, it returns the word with *
             phonetic = ipa.convert(word)
             # Remove * if it's just the word itself marked as unknown, or keep it?
             # eng_to_ipa returns "word*" if not found.
             if "*" in phonetic:
                 # Try to clean it up or just leave it. 
                 # Let's keep it but maybe wrap in [] if it looks like IPA.
                 pass
             phonetics.append(f"[{phonetic}]")
        else:
            phonetics.append("")
        
        if index % 100 == 0:
            print(f"Processed {index}/{total_rows} rows...")

    # Insert the new column at index 2
    df.insert(2, 'Phonetic', phonetics)

    print("Saving to file...")
    new_file_path = file_path.replace(".xlsx", "_completed.xlsx")
    try:
        # Save to a new file to avoid permission errors if the original is open
        df.to_excel(new_file_path, index=False, header=False)
        print(f"Done! Phonetics added to {new_file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    add_phonetics()
