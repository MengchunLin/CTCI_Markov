import pandas as pd
from tkinter import filedialog

# 讀取一個excel檔案
# 建立視窗選取檔案
# file_path = filedialog.askopenfilename()
file_path = 'C:\\Users\\Love_U\Desktop\\CTCI_Markov\\CTCI_Markov\\萬鼎全部鑽孔\\F4-T32_modified_processed.xlsx'

df = pd.read_excel(file_path)

# 確保 'Soil Type' 列存在
if '合併後' in df.columns:
    original = df['合併後']   
    # 線性補值
    original = original.interpolate(method='linear')
else:
    raise ValueError("Excel 檔案中沒有 'Soil Type' 列")

# 讀取一個csv檔案
result = pd.read_csv('C:\\Users\\Love_U\\Desktop\\CTCI_predict_result\\Mutative_31-33_1m_2.txt')
result = result.values.flatten()

# 計算正確率
correct_rate = 0
start = 0
if len(original) < len(result):
    end = len(original)
else:
    end = len(result)
print('len original:', len(original))
print('len result:', len(result))
for i in range(start, end):
    if original[i] == result[i]:
        correct_rate += 1

y = correct_rate / (end - start) * 100
y = round(y, 2)
print(y)

correct_rate = 0
start = 1000
if len(original) < len(result):
    end = len(original)
else:
    end = len(result)

for i in range(start, end):
    if original[i] == result[i]:
        correct_rate += 1
y = correct_rate / (end - start) * 100
y = round(y, 2)
print(y)


correct_rate = 0
start = 1000
end = 2000
for i in range(start, end):
    if original[i] == result[i]:
        correct_rate += 1
y = correct_rate / (end - start) * 100
y = round(y, 2)
print(y)


correct_rate = 0
start = 2000
end = 3000
for i in range(start, end):
    if original[i] == result[i]:
        correct_rate += 1
y = correct_rate / (end - start) * 100
y = round(y, 2)
print(y)


correct_rate = 0
start = 3000
end = 4000
for i in range(start, end):
    if original[i] == result[i]:
        correct_rate += 1
y = correct_rate / (end - start) * 100
y = round(y, 2)
print(y)

correct_rate = 0
start = 4000
if len(original) < len(result):
    end = len(original)
else:
    end = len(result)

for i in range(start, end):
    if original[i] == result[i]:
        correct_rate += 1
y = correct_rate / (end - start) * 100
y = round(y, 2)
print(y)

