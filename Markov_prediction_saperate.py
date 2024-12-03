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

# 紀錄時間
start_time = time.time()

# 打開鑽孔檔案
entire_file = pd.read_csv('markov_matrix.csv', delimiter=",",header=None).fillna(0).values # 讀取文件空值全部補0
entire_matrix = entire_file[2:, :]  # 用來預測的矩陣
Hole_name = entire_file[0] # 鑽孔名稱
Hole_distance = entire_file[1] # 鑽孔距離
initial_array = entire_file[2] # 初始矩陣

# 取得土壤種類
unique_numbers = np.unique(entire_matrix)
unique_numbers = unique_numbers[unique_numbers != 0] # 從unique_numbers過濾掉0
typenumber = len(unique_numbers) # 土壤種類數量
mapping = {value: index+1 for index, value in enumerate(unique_numbers)}# 建立土壤代號對應的數字
# 將公司土壤代號轉換為 1 ~ ...
def map_value(value):
    return mapping.get(value, value)  # 如果 value 在 mapping 中有對應的值，則映射；否則保持原值
entire_matrix =  np.vectorize(map_value)(entire_matrix)
transitionName = np.arange(1,typenumber+1)

# 定義模型的間隔、寬度、深度、面積、孔洞數量和地質類型數量等參數
W = int(int(Hole_distance.max())) + 1
D = int(entire_matrix.shape[0])
print('D:',D)
print('W:',W)
A = W * D
print('A:',A)
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

    K = 9.3
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