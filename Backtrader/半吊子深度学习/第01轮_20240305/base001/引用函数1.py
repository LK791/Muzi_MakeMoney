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
def  MOFA_��ȡxlsx��df ( ����xlsx·�� ):
    df888 = pd.DataFrame()
    aaa = 0
    # �����ļ����е������ļ�����ȡ��df
    for file_name in os.listdir(����xlsx·��):
        # ����ļ��Ƿ���.xlsx��β
        if file_name.endswith('.xlsx'):
            # ������·����ӵ��б���
            ����·�� = os.path.join(����xlsx·��, file_name)
            file_path = file_name  # �޸�Ϊ�����ļ�·��
            parts = file_path.split('.')
            ��Ʊ���� = parts[0]
            print(����·��)
            df = pd.read_excel(����·��, header=None)
            # ɾ������Ҫ���У��������µ�����
            df.drop(index=[0, 1, 3, df.index[-1]], inplace=True)  # ɾ��ָ����
            df.columns = df.iloc[0]  # ��������Ϊ����
            df.drop(index=df.index[0], inplace=True)  # ɾ��ԭ������
            # ����һ��ת��Ϊʱ���ʽ������
            df.iloc[:, 0] = (pd.to_datetime(df.iloc[:, 0]).dt.strftime('%Y%m%d').astype(int))
            # ����ʱ�������������ת��Ϊ��ֵ����
            df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
            # ɾ����������������ֵ����
            df.dropna(thresh=df.shape[1] - 0, inplace=True)
            df.insert(loc=1, column='����', value=int(��Ʊ����)/1000000 )
            # ����������ʹ�кŴ�0��ʼ
            df.reset_index(drop=True, inplace=True)
            df888 = pd.concat([df888, df], axis=0)
            df888.reset_index(drop=True, inplace=True)
            aaa = aaa + 1
            print('��ȡ' + str(aaa)+'ֻ��Ʊ')
    df888.columns = df888.columns.str.strip()
    print('dfȫ����ȡ�ɹ�')
    print('* ' * 30)
    return  df888
def MOFA_ɾ�����������ļ������ļ���(AA88 ) :
    # ɾ��Ŀ���ļ����������ļ�,ֻ�����ļ���
    for root, dirs, files in os.walk(AA88):
        # ɾ���ļ�������ļ�
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    print('������Ŀ¼')
    print('* ' * 30)
def MOFA_ת��xls(δ����xlsx·��, �Ѿ�����xlsx·��) :
    aaa = -1
    # ���Ϊxlsx���ļ�·����GBK���룩
    �Ѿ�����xlsx·�� = r"D:\00ruanjian\tongdaxin\T0002\export\xlsx"
    δ����xlsx·�� = r"D:\00ruanjian\tongdaxin\T0002\export"
    for file in os.scandir(δ����xlsx·��):
        suffix = file.name.split(".")[-1]
        if file.is_dir():
            pass
        else:
            if suffix == "xls":
                excel = win32.gencache.EnsureDispatch('Excel.Application')
                wb = excel.Workbooks.Open(file.path)
                # ���ļ�·��ת��ΪGBK����
                xlsx_path = �Ѿ�����xlsx·��.encode('gbk')
                # xlsx�ļ���·��\\�ļ���x
                wb.SaveAs(xlsx_path.decode('gbk') + "\\" + file.name + "x", FileFormat=51)
                wb.Close()
                excel.Application.Quit()
        aaa = aaa+1
        print( 'ok '+str(aaa)   )
    print('xlsת��xlsx��� ')
    print('* '*30)
def MOFA_����() :
    time.sleep(0.2)
    pyautogui.click(415, 175)
    pyautogui.press('3')
    time.sleep(0.1)
    pyautogui.press('4')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)
    ʶ���� = 0
    while ʶ���� == 0 :
        image_path = 'base001/daochu.png'
        region = (670,800,400,400)
        # ��ָ�������ڲ���ͼƬ
        for i in range(15):
            try:
                location = pyautogui.locateOnScreen(image_path, region=region)
                if location is not None:
                    # print( '���')
                    ʶ���� = 1
                    left, top, width, height = location
                    center_x = left + width / 2
                    center_y = top + height / 2
                    pyautogui.click(center_x, center_y)
                    break
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.2)  # �ȴ�1���ٴγ���
            print('�ٵ�0.2��')
    time.sleep(0.1)
    ʶ����1 = 0
    while ʶ����1 == 0:
        image_path = 'base001/quxiao.png'
        region = (470, 670, 500, 500)
        # ��ָ�������ڲ���ͼƬ
        for i in range(15):
            try:
                location = pyautogui.locateOnScreen(image_path, region=region)
                if location is not None:
                    # print('���')
                    ʶ����1 = 1
                    left, top, width, height = location
                    center_x = left + width / 2
                    center_y = top + height / 2
                    pyautogui.click(center_x, center_y)
                    break
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.2)  # �ȴ�1���ٴγ���
            print('�ٵ�0.2��')
    pyautogui.press('pgdn')
def MOFA_������Ʊ(������Ʊ���� ):
    print('��ʼͨ���ŵ�����Ʊ ')
    for i in range(int(������Ʊ���� )):
        MOFA_����()
        print( str(i+1) + '/'+str(������Ʊ����)   )
        pass
    print('��Ʊexcel������� ')
    print('* '*30)
# ����ԭʼ��Ʊ�����ļ�������ת��ΪCNN���õĸ�ʽ
def ����ͨ������groupby���鴦��(file_path  , ���� ):
    df = pd.read_csv(file_path)
    ������1 = ����-1
    processed_samples = []
    for stock_code, group in df.groupby('����'):
        for i in range(������1, len(group)):
            # ��ȡÿ��������20������
            sample = group.iloc[i-������1:i+1]
            # ����Ϊ�������һ�е���������
            features = sample.iloc[:, :-1]
            # ��ǩΪ���һ������
            label = sample.iloc[-1, -1]
            # ����������ת��Ϊ�ʺ�CNN����״
            features_array = features.to_numpy().reshape((����, -1, 1))
            processed_samples.append((features_array, label))
            print('+1')
    return processed_samples
# �����������Ƿ���ڸ�ֵ�������б�׼�����ǹ�һ������
def normalize_or_standardize(data_list):
    data_array = np.array(data_list)
    # ���������е�NaNֵ
    data_array = np.nan_to_num(data_array)
    if np.any(data_array < 0):
        # ��׼������
        return (data_array - np.mean(data_array)) / np.std(data_array)
    else:
        # ������ֵ����Сֵ�Ƿ����
        min_val = np.min(data_array)
        max_val = np.max(data_array)
        if max_val - min_val == 0:
            return data_array  # �������ֵ��ͬ���򷵻�ԭ����
        else:
            # ��һ������
            return (data_array - min_val) / (max_val - min_val)
# ��ÿ���������������й�һ�����׼������
def ��һ�����׼����������(samples  , ���� ):
    processed_samples = []
    for features, label in samples:
        # ����������ת��ΪDataFrame��ʽ
        features_df = pd.DataFrame(features.reshape((����, -1)))
        # ����һ�У����ڣ�ת��ΪNumPy�����ڸ�ʽ
        # features_df[0] = pd.to_datetime(features_df[0])
        # �Գ����������ÿ�н��й�һ�����׼������
        for col in features_df.columns[1:]:
            features_df[col] = normalize_or_standardize(features_df[col].tolist())
        # ��������DataFrameת��������������״
        processed_features = features_df.values.reshape((����, -1, 1))
        processed_samples.append((processed_features, label))
        print('+1')
    return processed_samples
def prepare_data_for_cnn_dynamic(samples , tianshu):
    """
    ׼�������Թ�CNNʹ�ã��Զ�ȷ������������������
    :param samples: �������������ͱ�ǩ�������б�
    :return: ���ܺ���������ݺͱ�ǩ����
    """
    # ��ʼ�������ͱ�ǩ�б�
    features_list = []
    labels_list = []
    # ������������
    for features, label in samples:
        # ��������������ƥ��CNN������������״
        �������������� = len(samples[0][0][0])
        reshaped_features = features.reshape((tianshu, ��������������, 1))  # ���¼�������
        # ��ӵ��б�
        features_list.append(reshaped_features)
        labels_list.append(label)
    # ���б�ת��ΪNumPy����
    features_array = np.array(features_list)
    labels_array = np.array(labels_list)
    return features_array, labels_array
import os
import shutil
def ɾ��ģ��ѵ�����():
    try:
        # ��ȡ��ǰ����Ŀ¼
        current_dir = os.getcwd()
        # ����Ҫɾ�����ļ����ļ��е�����·��
        checkpoint_folder_path = os.path.join(current_dir, "checkpoint")
        weights_file_path = os.path.join(current_dir, "weights.txt")
        # ��鲢ɾ��checkpoint�ļ��м����ڲ��ļ�
        if os.path.exists(checkpoint_folder_path) and os.path.isdir(checkpoint_folder_path):
            shutil.rmtree(checkpoint_folder_path)
            print(f"��ɾ��Ŀ¼��������: {checkpoint_folder_path}")
        else:
            print(f"Ŀ¼�����ڻ��߲���һ����Ч��Ŀ¼: {checkpoint_folder_path}")
        # ��鲢ɾ��weights.txt�ļ�
        if os.path.exists(weights_file_path) and os.path.isfile(weights_file_path):
            os.remove(weights_file_path)
            print(f"��ɾ���ļ�: {weights_file_path}")
        else:
            print(f"�ļ������ڻ��߲���һ����Ч���ļ�: {weights_file_path}")
    except Exception as e:
        print(f"ɾ���ļ���Ŀ¼ʱ����: {e}")
# ������������г�С�飬���������룬��ֹ����̫�����в���
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