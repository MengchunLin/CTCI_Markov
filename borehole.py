import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# tkinter 選擇多個檔案
def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames()
    print(f"Selected files: {file_paths}")
    return file_paths

# 繪製多個檔案資料於同一圖形，不同 x 位置
def plot_multiple_files(file_paths):
    
    # 12-15
    # labels = ['F4-T12', 'F4-T14', 'F4-T15']
    # position_labels = ['0', '1837', '2845']
    # x_positions = [0, 1837, 2845]
    # 20-22
    # labels = ['F4-T20', 'F4-T21', 'F4-T22']
    # position_labels = ['0', '882', '1793']
    # x_positions = [0, 882, 1793]
    # 31-33
    labels = ['F4-T31', 'F4-T32', 'F4-T33']
    position_labels = ['0', '1054', '2112']
    x_positions = [0, 1054, 2112]

    fig, ax = plt.subplots(figsize=(6, 12))
    # plt.xlim(0, 20)
    plt.ylim(0, 110)  # 設定 y 軸範圍
    plt.yticks(fontsize=20)  # 設定 y 軸刻度字體大小為 20


    # ax.set_xticks([])
    # ax.set_xticklabels([])

    def get_color(plot_type_value):
        if plot_type_value == 1:
            return 'lightsalmon'
        elif plot_type_value == 2:
            return 'lightsteelblue'
        elif plot_type_value == 3:
            return 'plum'
        elif plot_type_value == 4:
            return 'darkkhaki'
        else:
            return 'burlywood'

    for idx, file_path in enumerate(file_paths):
        df = pd.read_excel(file_path)
        plot_depth = df['Test length[1]']
        plot_type = df['合併後']

        for i in range(len(plot_type) - 1):
            color = get_color(plot_type.iloc[i])
            x = x_positions[idx]
            ax.plot([x, x], plot_depth.iloc[i:i+2], color=color, lw=20)

        # 加上自訂名稱文字
        min_depth = plot_depth.min()
        ax.text(x_positions[idx], min_depth, labels[idx], ha='center', va='bottom', fontsize=20)

    # 圖例及其他設定（省略）

    plt.gca().invert_yaxis()

    red_patch = mpatches.Patch(color='lightsalmon', label='Sand(1)')
    orange_patch = mpatches.Patch(color='lightsteelblue', label='Silty Sand(2)')
    green_patch = mpatches.Patch(color='plum', label='Sandy Silt(3)')
    blue_patch = mpatches.Patch(color='darkkhaki', label='Clayey Silt(4)')
    black_patch = mpatches.Patch(color='burlywood', label='Caly(5)')

    plt.legend(handles=[red_patch, orange_patch, green_patch, blue_patch, black_patch],
               loc='center left', bbox_to_anchor=(1, 0.5), fontsize=20)
    # fig.tight_layout()
    fig.subplots_adjust(right=0.75, top=0.9, bottom=0.1, left=0.2)

    plt.xlabel('Distance (m)', fontsize=25)
    plt.ylabel('Depth (m)', fontsize=25)
    
    # 標上position_labels = [0, 1837, 2845]，在x軸上，顏色用紅色字體
    plt.xticks(x_positions, position_labels, fontsize=20)
    # title position above labels
    
    plt.title('Borehole', fontsize=25, pad=25)

    # 

    plt.grid(linestyle='-', linewidth=0.5)
    
    plt.show()



if __name__ == "__main__":
    file_paths = select_files()  # 選擇多個檔案
    if len(file_paths) == 3:
        plot_multiple_files(file_paths)
    else:
        print("請選擇三個檔案進行繪圖。")
     
    # 儲存圖形
    