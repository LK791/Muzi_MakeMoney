# -*- coding: gbk -*-
import random
import win32com.client as win32
import os
import pyautogui
import pandas as pd
import pyperclip
import time
import os
import numpy as np
from tensorflow.keras.utils import Sequence
def  MOFA_读取xlsx到df ( 基础xlsx路径 ):
    df888 = pd.DataFrame()
    aaa = 0
    # 遍历文件夹中的所有文件，读取到df
    for file_name in os.listdir(基础xlsx路径):
        # 检查文件是否以.xlsx结尾
        if file_name.endswith('.xlsx'):
            # 将完整路径添加到列表中
            完整路径 = os.path.join(基础xlsx路径, file_name)
            file_path = file_name  # 修改为您的文件路径
            parts = file_path.split('.')
            股票代码 = parts[0]
            print(完整路径)
            df = pd.read_excel(完整路径, header=None)
            # 删除不需要的行，并设置新的列名
            df.drop(index=[0, 1, 3, df.index[-1]], inplace=True)  # 删除指定行
            df.columns = df.iloc[0]  # 第三行设为列名
            df.drop(index=df.index[0], inplace=True)  # 删除原第三行
            # 将第一列转换为时间格式并保存
            df.iloc[:, 0] = (pd.to_datetime(df.iloc[:, 0]).dt.strftime('%Y%m%d').astype(int))
            # 将除时间列外的所有列转换为数值类型
            df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
            # 删除包含两个或更多空值的行
            df.dropna(thresh=df.shape[1] - 0, inplace=True)
            df.insert(loc=1, column='代码', value=int(股票代码)/1000000 )
            # 重置索引，使行号从0开始
            df.reset_index(drop=True, inplace=True)
            df888 = pd.concat([df888, df], axis=0)
            df888.reset_index(drop=True, inplace=True)
            aaa = aaa + 1
            print('读取' + str(aaa)+'只股票')
    df888.columns = df888.columns.str.strip()
    print('df全部读取成功')
    print('* ' * 30)
    return  df888
def MOFA_删除里面所有文件除了文件夹(AA88 ) :
    # 删除目标文件夹下所有文件,只留空文件夹
    for root, dirs, files in os.walk(AA88):
        # 删除文件夹里的文件
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    print('清理导出目录')
    print('* ' * 30)
def MOFA_转换xls(未处理xlsx路径, 已经处理xlsx路径) :
    aaa = -1
    # 另存为xlsx的文件路径（GBK编码）
    已经处理xlsx路径 = r"D:\00ruanjian\tongdaxin\T0002\export\xlsx"
    未处理xlsx路径 = r"D:\00ruanjian\tongdaxin\T0002\export"
    for file in os.scandir(未处理xlsx路径):
        suffix = file.name.split(".")[-1]
        if file.is_dir():
            pass
        else:
            if suffix == "xls":
                excel = win32.gencache.EnsureDispatch('Excel.Application')
                wb = excel.Workbooks.Open(file.path)
                # 将文件路径转换为GBK编码
                xlsx_path = 已经处理xlsx路径.encode('gbk')
                # xlsx文件夹路径\\文件名x
                wb.SaveAs(xlsx_path.decode('gbk') + "\\" + file.name + "x", FileFormat=51)
                wb.Close()
                excel.Application.Quit()
        aaa = aaa+1
        print( 'ok '+str(aaa)   )
    print('xls转换xlsx完成 ')
    print('* '*30)
def MOFA_导出() :
    time.sleep(0.2)
    pyautogui.click(415, 175)
    pyautogui.press('3')
    time.sleep(0.1)
    pyautogui.press('4')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)
    识别器 = 0
    while 识别器 == 0 :
        image_path = 'base001/daochu.png'
        region = (670,800,400,400)
        # 在指定区域内查找图片
        for i in range(15):
            try:
                location = pyautogui.locateOnScreen(image_path, region=region)
                if location is not None:
                    # print( '完成')
                    识别器 = 1
                    left, top, width, height = location
                    center_x = left + width / 2
                    center_y = top + height / 2
                    pyautogui.click(center_x, center_y)
                    break
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.2)  # 等待1秒再次尝试
            print('再等0.2秒')
    time.sleep(0.1)
    识别器1 = 0
    while 识别器1 == 0:
        image_path = 'base001/quxiao.png'
        region = (470, 670, 500, 500)
        # 在指定区域内查找图片
        for i in range(15):
            try:
                location = pyautogui.locateOnScreen(image_path, region=region)
                if location is not None:
                    # print('完成')
                    识别器1 = 1
                    left, top, width, height = location
                    center_x = left + width / 2
                    center_y = top + height / 2
                    pyautogui.click(center_x, center_y)
                    break
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.2)  # 等待1秒再次尝试
            print('再等0.2秒')
    pyautogui.press('pgdn')
def MOFA_导出股票(导出股票个数 ):
    print('开始通达信导出股票 ')
    for i in range(int(导出股票个数 )):
        MOFA_导出()
        print( str(i+1) + '/'+str(导出股票个数)   )
        pass
    print('股票excel导出完成 ')
    print('* '*30)
# 处理原始股票数据文件，将其转换为CNN适用的格式
def 数据通过代码groupby分组处理(file_path  , 天数 ):
    df = pd.read_csv(file_path)
    天数减1 = 天数-1
    processed_samples = []
    for stock_code, group in df.groupby('代码'):
        for i in range(天数减1, len(group)):
            # 获取每个样本的20天数据
            sample = group.iloc[i-天数减1:i+1]
            # 特征为除了最后一列的所有数据
            features = sample.iloc[:, :-1]
            # 标签为最后一列数据
            label = sample.iloc[-1, -1]
            # 将特征数据转换为适合CNN的形状
            features_array = features.to_numpy().reshape((天数, -1, 1))
            processed_samples.append((features_array, label))
            print('+1')
    return processed_samples
# 根据数据中是否存在负值决定进行标准化还是归一化处理
def normalize_or_standardize(data_list):
    data_array = np.array(data_list)
    # 处理数组中的NaN值
    data_array = np.nan_to_num(data_array)
    if np.any(data_array < 0):
        # 标准化处理
        return (data_array - np.mean(data_array)) / np.std(data_array)
    else:
        # 检查最大值和最小值是否相等
        min_val = np.min(data_array)
        max_val = np.max(data_array)
        if max_val - min_val == 0:
            return data_array  # 如果所有值相同，则返回原数组
        else:
            # 归一化处理
            return (data_array - min_val) / (max_val - min_val)
# 对每个样本的特征进行归一化或标准化处理
def 归一化或标准化处理数据(samples  , 天数 ):
    processed_samples = []
    for features, label in samples:
        # 将特征数据转换为DataFrame格式
        features_df = pd.DataFrame(features.reshape((天数, -1)))
        # 将第一列（日期）转换为NumPy的日期格式
        # features_df[0] = pd.to_datetime(features_df[0])
        # 对除日期列外的每列进行归一化或标准化处理
        for col in features_df.columns[1:]:
            features_df[col] = normalize_or_standardize(features_df[col].tolist())
        # 将处理后的DataFrame转换回特征数组形状
        processed_features = features_df.values.reshape((天数, -1, 1))
        processed_samples.append((processed_features, label))
        print('+1')
    return processed_samples
def prepare_data_for_cnn_dynamic(samples , tianshu):
    """
    准备数据以供CNN使用，自动确定特征张量的列数。
    :param samples: 包含特征张量和标签的样本列表
    :return: 重塑后的特征数据和标签数据
    """
    # 初始化特征和标签列表
    features_list = []
    labels_list = []
    # 遍历所有样本
    for features, label in samples:
        # 重塑特征张量以匹配CNN的期望输入形状
        单样本特征数量 = len(samples[0][0][0])
        reshaped_features = features.reshape((tianshu, 单样本特征数量, 1))  # 重新计算列数
        # 添加到列表
        features_list.append(reshaped_features)
        labels_list.append(label)
    # 将列表转换为NumPy数组
    features_array = np.array(features_list)
    labels_array = np.array(labels_list)
    return features_array, labels_array
import os
import shutil
def 删除模型训练结果():
    try:
        # 获取当前工作目录
        current_dir = os.getcwd()
        # 构建要删除的文件和文件夹的完整路径
        checkpoint_folder_path = os.path.join(current_dir, "checkpoint")
        weights_file_path = os.path.join(current_dir, "weights.txt")
        # 检查并删除checkpoint文件夹及其内部文件
        if os.path.exists(checkpoint_folder_path) and os.path.isdir(checkpoint_folder_path):
            shutil.rmtree(checkpoint_folder_path)
            print(f"已删除目录及其内容: {checkpoint_folder_path}")
        else:
            print(f"目录不存在或者不是一个有效的目录: {checkpoint_folder_path}")
        # 检查并删除weights.txt文件
        if os.path.exists(weights_file_path) and os.path.isfile(weights_file_path):
            os.remove(weights_file_path)
            print(f"已删除文件: {weights_file_path}")
        else:
            print(f"文件不存在或者不是一个有效的文件: {weights_file_path}")
    except Exception as e:
        print(f"删除文件或目录时出错: {e}")
# 把输入的数据切成小块，数据量输入，防止数据太大运行不了
class DataGenerator(Sequence):
    def __init__(self, features, labels, batch_size):
        self.features = features
        self.labels = labels
        self.batch_size = batch_size
    def __len__(self):
        return int(np.ceil(len(self.features) / float(self.batch_size)))
    def __getitem__(self, idx):
        batch_x = self.features[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.labels[idx * self.batch_size:(idx + 1) * self.batch_size]
        # print("Batch x type:", type(batch_x), "Batch y type:", type(batch_y))
        return batch_x, batch_y