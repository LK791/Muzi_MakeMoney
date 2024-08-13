from 通达信爬数据deep学习.base001.引用函数1 import *

import random
import numpy as np
import pyautogui
import pandas as pd
import pyperclip
import time
import os
import pickle
import h5py
np.set_printoptions(precision=None, suppress=True)
np.set_printoptions(threshold=np.inf)

# 设置输出右对齐
pd.set_option('display.unicode.east_asian_width', True)
# 显示所有的列
pd.set_option('expand_frame_repr', False)
# 最多显示数据的行数
pd.set_option('display.max_rows', 8000)
# 取消科学计数法,显示完整,可调整小数点后显示位数
pd.set_option('display.float_format', '{:.8f}'.format)



























### 一开始定义数据 ###############################################
导出股票个数 = 9
单样本天数 = 32
未处理xls路径 = r'D:\00ruanjian\tongdaxin\T0002\export'
已处理xlsx路径 = r'D:\00ruanjian\tongdaxin\T0002\export\xlsx'
#########################################################
MOFA_删除里面所有文件除了文件夹(未处理xls路径)
MOFA_导出股票(导出股票个数 )
MOFA_转换xls(未处理xls路径, 已处理xlsx路径)
df888 = MOFA_读取xlsx到df(已处理xlsx路径)
print(df888)
# 导出csv
df888.to_csv('output.csv', index=False)
print('成功导出csv')
# 假设您的DataFrame名为df，并且要将其导出到名为output.xlsx的Excel文件中
# 如果不希望导出索引，可以设置index=False
# df888.to_excel('output.xlsx', index=False)

exit()



半成品CSV路径 = 'output.csv'  # 请确保这是正确的文件路径
# 处理原始股票数据文件，将其转换为CNN适用的格式
未标准化素材 = 数据通过代码groupby分组处理(半成品CSV路径 ,单样本天数 )

# 对每个样本的特征进行归一化或标准化处理
丹药素材 = 归一化或标准化处理数据( 未标准化素材  ,  单样本天数 )












# 平衡标签样本
random.seed(7)
random.shuffle(丹药素材)
# 统计标签为1的样本数量
标签为1的数量 = sum(1 for _, label in 丹药素材 if label == 1)
# 统计标签为0的样本数量，并且删除多余的标签为0的样本
标签为0的数量 = sum(1 for _, label in 丹药素材 if label == 0)
要删除的数量 = 标签为0的数量 - 标签为1的数量
if 要删除的数量 > 0:
    丹药素材 = [样本 for 样本 in 丹药素材 if not (样本[1] == 0 and 要删除的数量 > 0 and (要删除的数量 := 要删除的数量 - 1) >= 0)]

random.seed(90)
random.shuffle(丹药素材)





# 将数据转换成输入cnn的格式，准备好特征集，标签集
特征集, 标签集 = prepare_data_for_cnn_dynamic(丹药素材 , 单样本天数 )
# 删除样本前两列，日期与代码
特征集 = 特征集[:, :, 2:, :]

print(特征集.shape)
print(标签集.shape)


with h5py.File('data.h5', 'w') as h5f:
    h5f.create_dataset('features', data=特征集)
    h5f.create_dataset('labels', data=标签集)
    print('已保存张量')


# 从HDF5文件中读取数据
with h5py.File('data.h5', 'r') as h5f:
    特征集 = h5f['features'][:]
    标签集 = h5f['labels'][:]
    print('已读取张量')



print(特征集.shape)
print(标签集.shape)


























