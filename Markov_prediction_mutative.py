import numpy as np
import pandas as pd
import operator as op
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import subprocess
import json
import tkinter as tk
import time
import tkinter.messagebox as messagebox
import matplotlib.colors as mcolors
# -----------testing file----------------
Matrix4D = "test.csv"
Matrix5D = '5DMatrix.csv'
sixHole = '6Hole.csv'
test='test - 複製.csv'
eightSoil='8soil.csv'
CECI='markov_matrix.csv'
CTCI='CTCI.csv'
# -----------testing file----------------
# 記錄開始時間
start_time = time.time()
# -----------call simplify_data.py----------------


# -----------call simplify_data.py----------------
# file preprocessing
entire_file = pd.read_csv('markov_matrix.csv', delimiter=",",header=None).fillna(0).values # 讀取文件空值全部補0
# entire_file沒有標題，所以第一行是數據
entire_matrix = entire_file[2:, :]  # skip first column 第一行是名稱
# 取得標題作為孔洞名稱
Hole_name = entire_file[0]
Hole_distance = entire_file[1]
# 把 entire_matrix 拆成三個部分
entire_matrix_1 = entire_matrix[:2250, :]
# print('entire_matrix_1:', entire_matrix_1)

entire_matrix_2 = entire_matrix[1750:3250,:]
# # print('entire_matrix_2:', entire_matrix_2)

entire_matrix_3 = entire_matrix[2750:4250, :]
# print('entire_matrix_3:', entire_matrix_3)

entire_matrix_4 = entire_matrix[3750:, :]
# print('entire_matrix_4:', entire_matrix_4)
# 取得初始狀態
initial_array_1 = entire_matrix_1[0]
initial_array_2 = entire_matrix_2[0]
initial_array_3 = entire_matrix_3[0]
initial_array_4 = entire_matrix_4[0]

result_matrix = []

# 建立迴圈分析三個部分
for i in range(1,5):
    if i == 1:
        entire_matrix = entire_matrix_1
        initial_array = initial_array_1
    elif i == 2:
        entire_matrix = entire_matrix_2
        initial_array = initial_array_2
    elif i == 3:
        entire_matrix = entire_matrix_3
        initial_array = initial_array_3
    else:
        entire_matrix = entire_matrix_4
        initial_array = initial_array_4
    # 取得土壤種類
    unique_numbers = np.unique(entire_matrix)
    # 從unique_numbers過濾掉0
    unique_numbers = unique_numbers[unique_numbers != 0]
    typenumber = len(unique_numbers)
    # 建立土壤代號對應的數字
    mapping = {value: index+1 for index, value in enumerate(unique_numbers)}
    resever_mapping = {v: k for k, v in mapping.items()}
    # 將公司土壤代號轉換為 1 ~ ...
    def map_value(value):
        return mapping.get(value, value)  # 如果 value 在 mapping 中有對應的值，則映射；否則保持原值
    entire_matrix =  np.vectorize(map_value)(entire_matrix)
    transitionName = np.arange(1,typenumber+1)
    # file preprocessing

    # 參考前後土層厚度
    refer_depth = 5/0.02  # 假設每層厚度為100

    # 定義模型的間隔、寬度、深度、面積、孔洞數量和地質類型數量等參數
    W = int(int(Hole_distance.max())) + 1
    D = int(entire_matrix.shape[0]- refer_depth) 
    # print('D:',D)
    # print('W:',W)


    denominator = 0
    molecular = 0
    A = W * D
    # print('A:',A)
    HoleLocation_entire=(Hole_distance).astype(int)
    HoleLocation_entire[0]=0

    # 計算轉移概率矩陣的函數
    def calculate_transition_matrix(matrix,hole_location):
        group_number = np.zeros((D , W))

        for location in Hole_distance:
            for type in initial_array:
                for i in range(W):
                    if i<location:
                        group_number[0][i] = mapping[type]
                    else:
                        continue
        
        for i in range(D):
            for j in range(len(hole_location)):
                group_number[i][(hole_location[j])] = matrix[i][j]
        T_t_V = np.zeros(len(matrix))
        soiltype_V = {}
                
        soiltype_V = Counter(matrix.flatten())
        del soiltype_V[0]  # Remove count of zeros, if necessary
        soiltype_V = sorted(soiltype_V.items(), key=op.itemgetter(0), reverse=False)
        # print('soiltype_V:',soiltype_V)
        VPCM = np.zeros((typenumber, typenumber))
        Tmatrix_V = np.zeros((typenumber, typenumber))

        for i in range(np.size(matrix, 1)):
            for j in range(len(matrix)):
                T_t_V[j] = matrix[j][i]

            for k in range(len(T_t_V) - 1):
                if T_t_V[k]==0 or T_t_V[k+1]==0:
                    break
                for m in range(typenumber):
                    for n in range(typenumber):
                        if T_t_V[k] == soiltype_V[m][0] and T_t_V[k + 1] == soiltype_V[n][0]:
                            VPCM[m][n] += 1
                            Tmatrix_V[m][n] += 1
        # 正規化
        count_V = np.sum(Tmatrix_V, axis=1)
        for i in range(np.size(Tmatrix_V, 1)):
            for j in range(np.size(Tmatrix_V, 1)):
                Tmatrix_V[i][j] = Tmatrix_V[i][j] / count_V[i]

        K = 9
        HPCM = np.zeros([len(count_V), len(count_V)])
        Tmatrix_H = np.zeros([len(count_V), len(count_V)])

        for i in range(np.size(Tmatrix_H, 1)):
            for j in range(np.size(Tmatrix_H, 1)):
                if i == j:
                    HPCM[i][j] = K * VPCM[i][j]
                    Tmatrix_H[i][j] = K * VPCM[i][j]
                else:
                    HPCM[i][j] = VPCM[i][j]
                    Tmatrix_H[i][j] = VPCM[i][j]

        count_H = np.sum(Tmatrix_H, axis=1)
        for i in range(np.size(Tmatrix_H, 1)):
            for j in range(np.size(Tmatrix_H, 1)):
                Tmatrix_H[i][j] = Tmatrix_H[i][j] / count_H[i]
                
        return Tmatrix_V, Tmatrix_H ,group_number

    # 計算 HoleLocation_entire 的轉移矩陣
    Tmatrix_V_entire, Tmatrix_H_entire ,group_number_entire= calculate_transition_matrix(entire_matrix,HoleLocation_entire)

    # 預測地質類型的函數
    def predict_geological_types(Tmatrix_V, Tmatrix_H, HoleLocation,group_number):
        L_state = 0
        M_state = 0
        Q_state = 0
        Nx = 0
        current_matrix = np.zeros(len(transitionName))

        conditions = {}
        for j in range(1, len(HoleLocation)):
            conditions[(HoleLocation[j - 1], HoleLocation[j])] = HoleLocation[j]
        for layer in range(1,D):
            for i in range(W):
                # 若為位置是有資料的就跳過(為鑽孔位置)
                if group_number[layer][i] :
                    continue
                
                L_state = 0
                M_state = 0
                Q_state = 0
                Nx_TH = Tmatrix_H
                f_sum = 0
                k_sum = 0
                Nx=0
                if i in HoleLocation:
                    if i!=0:
                        holekey=np.where(HoleLocation == i)[0][0]
                        for holeIndex in range(holekey,-1,-1):
                            if HoleLocation[holeIndex] != 0:
                                Nx = HoleLocation[holeIndex]
                                break
                        # 矩陣乘法更新Nx_TH
                        for _ in range(1, Nx - i):
                            Nx_TH = np.dot(Nx_TH, Tmatrix_H)
                else:
                    for (lower, upper), nx in conditions.items():
                        if lower < i < upper:
                            Nx = nx
                            break
                Nx_TH = np.eye(Tmatrix_H.shape[0])
                for _ in range(Nx - i):
                    Nx_TH = np.dot(Nx_TH, Tmatrix_H)

                L_state = group_number[layer][i-1] - 1
                M_state = group_number[layer-1][i] - 1
                Q_state = group_number[layer][Nx] - 1          
            
                
                for f in range(typenumber):
                    f_item1 = Tmatrix_H[int(L_state)][f]
                    f_item2 = Nx_TH[f][int(Q_state)]
                    f_item3 = Tmatrix_V[int(M_state)][f]
                    f_sum += f_item1 * f_item2 * f_item3
                if f_sum == 0 :
                    current_matrix= np.ones(typenumber) / typenumber
                    # print('current_matrix:',current_matrix)
                else:
                    for k in range(typenumber):
                        k_item1 = Tmatrix_H[int(L_state)][k]
                        k_item2 = Nx_TH[k][int(Q_state)]
                        k_item3 = Tmatrix_V[int(M_state)][k]
                        k_sum = k_item1 * k_item2 * k_item3

                        current_matrix[k] = k_sum / f_sum

                # 進行預測
                predict_type = np.random.choice(transitionName, replace=True, p=current_matrix)
                # if i in HoleLocation:
                #     print('k_sum:',k_sum,'f_sum:',f_sum,'Nx:',Nx)
                group_number[layer][i] = predict_type
        return group_number
    print('predicting...')

    # 預測地質類型
    predict_result_entire = predict_geological_types(
        Tmatrix_V_entire, Tmatrix_H_entire, HoleLocation_entire, group_number_entire
    )
    # print('predict_result_entire:',predict_result_entire.shape)
    mapped_results = []
    # 使用 for 迴圈進行映射
    for row in predict_result_entire:
        mapped_row = []
        for value in row:
            if isinstance(value, np.ndarray):  # 如果是 numpy.ndarray，提取標量
                value = value.item()
            if value in resever_mapping:  # 確保值存在於 mapping 中
                mapped_row.append(resever_mapping[value])
            else:
                mapped_row.append(None)  # 如果無法映射，填充一個默認值（例如 None）
        mapped_results.append(mapped_row)
    # 把預測結果儲存到
    result_matrix.append(mapped_results)

# 將預測結果與原始矩陣結合
combined_matrix = np.vstack(result_matrix)

# ===【在這裡記錄結束時間和計算預測流程運行時間】===
end_time = time.time()
execution_time = end_time - start_time
print(f"程式運行時間（預測流程）: {execution_time:.2f} 秒")
# ===========================================
    

def irregular_shift(combined_matrix, max_shift):
    """
    根據線性規則將矩陣逐列向下移動，形成不規則矩陣。
    
    Args:
        predict_result_entire (ndarray): 原始矩陣，大小為 (D, W)
        max_shift (int): 最大移動深度（最右列的移動量）
    
    Returns:
        ndarray: 不規則矩陣
    """
    D, W = combined_matrix.shape  # 原矩陣大小

    # 計算新矩陣的高度
    new_height = D + max_shift

    # 初始化新矩陣，填充為 NaN 或其他佔位符
    irregular_matrix = np.full((new_height, W), np.nan)

    # 設定線性移動規則，移動量從 0 到 max_shift
    shift_values = np.linspace(0, max_shift, W, dtype=int)

    # 逐列移動
    for col in range(W):
        shift = shift_values[col]  # 當前列的移動深度
        irregular_matrix[shift:shift + D, col] = combined_matrix[:, col]

    return irregular_matrix

# 不規則矩陣
max_shift = 0  # 最大移動深度
irregular_matrix = irregular_shift(combined_matrix, max_shift)
# print('irregular_matrix:\n',irregular_matrix)

D=irregular_matrix.shape[0]

def predict_location_input():
    def submit():
        # Get input from the entry widget
        location = entry.get()
        # Store it in a variable and close the GUI
        nonlocal user_input
        user_input = location
        root.destroy()

    root = tk.Tk()
    root.title("預測位置輸入")
    root.geometry("300x150")

    # Label
    label = tk.Label(root, text="請輸入預測位置:")
    label.pack(pady=10)

    # Entry widget for user input
    entry = tk.Entry(root, width=25)
    entry.pack(pady=5)

    # Button to submit the input
    button = tk.Button(root, text="確認", command=submit)
    button.pack(pady=10)

    # Variable to store user input
    user_input = None

    # Start the Tkinter event loop
    root.mainloop()

    return user_input 

# 預測位置輸入
user_input = predict_location_input()
user_input = int(int(user_input))

#　輸出預測位置的地質類型
predict_borehole = combined_matrix[:, user_input]
# 內容四捨五入到整數
predict_borehole = np.round(predict_borehole).astype(int)
# 儲存predict_borehole
np.savetxt('predict_borehole.txt',predict_borehole,fmt='%d')

# 可視化地質類型分布
mapping_key = list(mapping.keys())
mapping_value = list(mapping.values())
# print('mapping_key:',mapping_key)
# print('mapping_value:',mapping_value)
original_ticks = np.arange(0, int(Hole_distance.max() ), 100)
# 缩放后的 x 轴刻度标签
scaled_labels = (original_ticks ).astype(int)
# 定義自定義顏色映射
soil_colors = {
    1: 'lightsalmon',       
    2: 'lightsteelblue',      
    3: 'plum',     
    4: 'darkkhaki',      
    5: 'burlywood',   
}

# 定義名稱
soil_names = {
    1: 'Sand',
    2: 'Silty Sand',
    3: 'Sandy Silt',
    4: 'Clayey Silt',
    5: 'Clay',
}


# 創建自定義的離散顏色映射
colors = [soil_colors[i] for i in range(1, len(soil_colors) + 1)]
cmap = mcolors.ListedColormap(colors)

# 設置圖形大小
plt.figure(figsize=(8, 4), dpi=150)

# 使用自定義的顏色映射來顯示預測結果
im = plt.imshow(irregular_matrix, cmap=cmap, origin='upper', aspect='auto')

# 創建圖例
patches = [
    mpatches.Patch(color=soil_colors[i], label=f"{soil_names[i]} ({i})")
    for i in range(1, len(soil_colors) + 1)
]

plt.legend(
    handles=patches,
    loc='center left',  
    bbox_to_anchor=(1.05, 0.5), 
    title="Geological Types",
    fontsize=8,
    title_fontsize=10,
    frameon=True
)

# 繪製鑽孔位置的垂直線與標註
for i, name in zip(HoleLocation_entire, Hole_name):
    if i == 0:
        i = 0.5
        plt.axvline(x=i, color='sienna', linestyle='-', linewidth=2)
        # 標註名稱
        plt.text(i, 0, name, color='black', fontsize=8, ha='center', va='bottom')
    else:
        # print('i:',i)
        plt.axvline(x=i, color='sienna', linestyle='-', linewidth=2)
        # 標註名稱
        plt.text(i, 0, name, color='black', fontsize=8, ha='center', va='bottom')
plt.axline((user_input, 0), (user_input, D), color='red', linestyle='--', linewidth=1)   

# 設置刻度
original_ticks = np.arange(0, int(Hole_distance.max() ), 100)
scaled_labels = (original_ticks ).astype(int)

plt.xticks(
    ticks=original_ticks,
    labels=scaled_labels,
    fontsize=10
)
# 設置 y 軸的 ticks
ticks = np.arange(0, D, 500)  # 每 500 筆資料設置一個 tick

# 確保 labels 和 ticks 長度一致
labels = np.arange(0, len(ticks) * 10, 10)  # 每次以 10 增加

plt.yticks(
    ticks=ticks,
    labels=labels,
    fontsize=10
)



# 記錄結束時間
# end_time = time.time()

# 計算運行時間（以秒為單位）
execution_time = end_time - start_time
print(f"程式運行時間: {execution_time:.2f} 秒")
# 設置圖形外觀
plt.gca().set_aspect('auto')
plt.xlim(0, W)
plt.ylim(D, 0)
plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.title('Markov Prediction',pad=20)
plt.xlabel('Width (units)')
plt.ylabel('Depth (units)')
plt.tight_layout()
plt.savefig('Prediction_with_legend_side.png')
plt.show()