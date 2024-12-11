import pandas as pd
from tkinter import filedialog

# 讀取一個excel檔案
# 建立視窗選取檔案
file_path = filedialog.askopenfilename()
df = pd.read_excel(file_path)

# 確保 'Soil Type' 列存在
if '合併後' in df.columns:
    original = df['合併後']
    # 線性補值
    original = original.interpolate(method='linear')
else:
    raise ValueError("Excel 檔案中沒有 'Soil Type' 列")

# 讀取一個csv檔案
result = pd.read_csv('predict_borehole.txt')
result = result.values.flatten()

# 計算正確率
correct_rate = 0
start = 2000
end = 3000
for i in range(start, end):
    if original[i] == result[i]:
        correct_rate += 1
y = correct_rate / (end - start) * 100
print(f"Correct Rate: {y:.2f}%")

