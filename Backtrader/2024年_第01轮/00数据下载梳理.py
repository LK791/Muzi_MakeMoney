import random
import numpy as np
import pyautogui
import pandas as pd
import pyperclip
import time
import os
import win32com.client as win32
import pickle
# import h5py
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
def MOFA_删除里面所有文件除了文件夹(AA88 ) :
    # 删除目标文件夹下所有文件,只留空文件夹
    for root, dirs, files in os.walk(AA88):
        # 删除文件夹里的文件
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    print('清理导出目录')
    print('* ' * 30)
def MOFA_导出股票(导出股票个数 ):
    print('开始通达信导出股票 ')
    for i in range(int(导出股票个数 )):
        MOFA_导出()
        print( str(i+1) + '/'+str(导出股票个数)   )
        pass
    print('股票excel导出完成 ')
    print('* '*30)
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
            # df.dropna(thresh=df.shape[1] - 0, inplace=True)
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



# 定义数据 ###############################################
导出股票个数 = 1
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
df888.to_csv('数据保存\output.csv', index=False)
print('成功导出csv')
# 假设您的DataFrame名为df，并且要将其导出到名为output.xlsx的Excel文件中
# 如果不希望导出索引，可以设置index=False
# df888.to_excel('output.xlsx', index=False)
exit()





































