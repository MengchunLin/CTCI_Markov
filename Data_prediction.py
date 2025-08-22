import numpy as np
import pandas as pd
import json
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox


# 打開現存鑽孔
with open('created_file.json', 'r') as file:
    file_path_list = json.load(file)

with open('20-22-3.txt', 'r') as file:
    predict_borehole = file.read().splitlines()


def predict_data(file_path_list, predict_borehole):
    # 預測鑽孔的土壤類型
    predict_location_soiltype = predict_borehole
    # 初始化預測鑽孔的df
    predict_df = pd.DataFrame({
        "SoilType": predict_location_soiltype,
        "Test length[1]": np.arange(len(predict_location_soiltype)) * 0.02,
        "Cone resistance[2]": np.zeros(len(predict_location_soiltype)),
        "Local friction[3]": np.zeros(len(predict_location_soiltype)),
        "Pore pressure u2[6]": np.zeros(len(predict_location_soiltype)),
    })

    # 讀取所有鑽孔文件
    dfs = []
    for file_path in file_path_list:
        df = pd.read_excel(file_path)
        # 重組df
        df = df[['Test length[1]', '合併後', 'Cone resistance[2]', 'Local friction[3]', 'Pore pressure u2[6]']]
        dfs.append(df)

    # 讀取所有鑽孔文件
    for i in range(len(predict_location_soiltype)):
        qc = []
        fs = []
        u2 = []
        # 讀取所有鑽孔文件內的i列
        for df in dfs:
            # 如果df沒有i列
            if i >= len(df):
                continue
            # 如果i列的SoilType是predict_location_soiltype[i]
            # 印出df.loc[i, '合併後']的數據種類
            # 印出predict_location_soiltype[i]
            if df.loc[i, '合併後'] == int(predict_location_soiltype[i]):
                # 將i列的數據填入qc, fs, u2
                qc.append(df.loc[i, 'Cone resistance[2]'])
                fs.append(df.loc[i, 'Local friction[3]'])
                u2.append(df.loc[i, 'Pore pressure u2[6]'])
        # 如果qc, fs, u2都有值
        # 隨機選取一個值填入predict_df
        if qc and fs and u2:
            predict_df.loc[i, 'Cone resistance[2]'] = np.random.choice(qc)
            predict_df.loc[i, 'Local friction[3]'] = np.random.choice(fs)
            predict_df.loc[i, 'Pore pressure u2[6]'] = np.random.choice(u2)
        # 如果qc, fs, u2都沒有值
        # 填入0
        else:
            predict_df.loc[i, 'Cone resistance[2]'] = 0
            predict_df.loc[i, 'Local friction[3]'] = 0
            predict_df.loc[i, 'Pore pressure u2[6]'] = 0
    return predict_df
                
# 資料填空
def fill_data(predict_df):
    # 紀錄包含 0 的行位置
    zero_rows = predict_df[(predict_df == 0).any(axis=1)].index

    # 將所有 0 替換為 NaN，方便插值
    predict_df = predict_df.replace(0, np.nan)

    # 逐列進行線性插值
    for column in predict_df.columns:
        # 確保列為數值型別，避免類型錯誤
        predict_df[column] = pd.to_numeric(predict_df[column], errors='coerce')
        # 線性插值
        predict_df[column] = predict_df[column].interpolate()

    # 對原本包含 0 的行進行 ±1% 隨機調整（僅限垂直軸，例如 "Cone resistance[2]"）
    for row_idx in zero_rows:
        if "Cone resistance[2]" in predict_df.columns:
            predict_df.loc[row_idx, "Cone resistance[2]"] = (
                predict_df.loc[row_idx, "Cone resistance[2]"]
                * np.random.uniform(0.8, 1.4)
            )
        if "Local friction[3]" in predict_df.columns:
            predict_df.loc[row_idx, "Local friction[3]"] = (
                predict_df.loc[row_idx, "Local friction[3]"]
                * np.random.uniform(0.8, 1.4)
            )
        if "Pore pressure u2[6]" in predict_df.columns:
            predict_df.loc[row_idx, "Pore pressure u2[6]"] = (
                predict_df.loc[row_idx, "Pore pressure u2[6]"]
                * np.random.uniform(0.8, 1.4)
            )
    
    return predict_df







predict_df = predict_data(file_path_list, predict_borehole)
print('predict_df:', predict_df)
predict_df = fill_data(predict_df)
print('predict_df:', predict_df)
# 將預測的df存入excel
predict_df.to_excel('predict_data.xlsx', index=False)

print('done')

