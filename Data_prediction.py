import numpy as np
import pandas as pd
import json
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# 打開文件
predict_result_entire = np.loadtxt('predict_result_entire.csv', delimiter=",", skiprows=1)
interval = 0.5

# 打開現存鑽孔
with open('created_file.json', 'r') as file:
    file_path_list = json.load(file)

with open('predict_borehole.txt', 'r') as file:
    predict_borehole = file.read().splitlines()

print('file_path_list:', file_path_list)

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

def predict_data():
    predict_location_soiltype = predict_borehole
    print(f"Predicted soil types at location {predict_location_soiltype}")

    with open('created_file.json', 'r') as file:
        file_path_list = json.load(file)
    print('file_path_list:', file_path_list)

    predict_df = pd.DataFrame({
        "Location": np.arange(len(predict_location_soiltype)),
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
    print('dfs:', dfs)

    for i in range(len(predict_location_soiltype)):
        exist_qc, exist_fs, exist_u = [], [], []
        if i < len(df) and df['合併後'][i] == predict_location_soiltype[i]:
            exist_qc.append(df['Cone resistance[2]'][i])
            exist_fs.append(df['Local friction[3]'][i])
            exist_u.append(df['Pore pressure u2[6]'][i])

        if exist_qc:
            predict_df.loc[i, 'Cone resistance[2]'] = np.random.choice(exist_qc)
            # 寫入預測結果
                
            predict_df.loc[i, 'Local friction[3]'] = np.random.choice(exist_fs)
            predict_df.loc[i, 'Pore pressure u2[6]'] = np.random.choice(exist_u)
        else:
            depth_list, qc_list, fs_list, u_list = [], [], [], []
            for k in range(1, min(11, i + 1)):
                if predict_location_soiltype[i - k] == predict_location_soiltype[i]:
                    depth_list.append(predict_df.loc[i - k, 'Test length[1]'])
                    qc_list.append(predict_df.loc[i - k, 'Cone resistance[2]'])
                    fs_list.append(predict_df.loc[i - k, 'Local friction[3]'])
                    u_list.append(predict_df.loc[i - k, 'Pore pressure u2[6]'])

            if len(depth_list) >= 3:
                qc_trend = np.polyfit(depth_list, qc_list, 2)
                fs_trend = np.polyfit(depth_list, fs_list, 2)
                u_trend = np.polyfit(depth_list, u_list, 2)
                predict_df.loc[i, 'Cone resistance[2]'] = np.polyval(qc_trend, (i + 1) * 0.02)
                predict_df.loc[i, 'Local friction[3]'] = np.polyval(fs_trend, (i + 1) * 0.02)
                predict_df.loc[i, 'Pore pressure u2[6]'] = np.polyval(u_trend, (i + 1) * 0.02)

    print('predict_df:', predict_df)
    # 將預測結果保存為Excel文件
    predict_df.to_excel('predict_result.xlsx', index=False)
    return predict_df

predict_data = predict_data()
print('done')