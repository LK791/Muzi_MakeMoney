### 此版本更新，使用数据流的方法读取样本，输入进去


from 通达信爬数据deep学习.base001.引用函数1 import *
import tensorflow as tf
import os
import h5py
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Dropout, Flatten, Dense
from tensorflow.keras import Model
from tensorflow.keras.utils import Sequence
np.set_printoptions(threshold=np.inf)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号






















# 删除之前的训练结果
删除模型训练结果()


# 从HDF5文件中读取数据
with h5py.File('data.h5', 'r') as h5f:
    特征集 = h5f['features'][:]
    标签集 = h5f['labels'][:]
    print('已读取张量')

特征集  = np.concatenate([特征集] * 3, axis=-1)
标签集  = 标签集.reshape(-1, 1)

# 设置2/3为训练集
分割点 = (len(特征集)//3)*2
x_train = 特征集[:分割点]
y_train = 标签集[:分割点]
x_test  = 特征集[分割点:]
y_test  = 标签集[分割点:]

print( '训练——特征集： '+ str(x_train.shape))
print( '训练——标签集： '+ str(y_train.shape))
print( '测试——特征集： '+ str(x_test.shape))
print( '测试——标签集： '+ str(y_test.shape))




# 把模型切小，数据流输入
batch_size = 8
train_generator = DataGenerator(x_train, y_train, batch_size)
test_generator = DataGenerator(x_test, y_test, batch_size)













#### 模型区 ###################################


class Baseline(Model):
    def __init__(self):
        super(Baseline, self).__init__()
        self.c1 = Conv2D(filters=1, kernel_size=(32,1), padding='same')  # 卷积层
        self.b1 = BatchNormalization()  # BN层
        self.a1 = Activation('relu')  # 激活层
        self.p1 = MaxPool2D(pool_size=(2, 2), strides=2, padding='same')  # 池化层
        self.d1 = Dropout(0.2)  # dropout层

        self.flatten = Flatten()
        self.f1 = Dense(128, activation='relu')
        self.d2 = Dropout(0.2)
        self.f2 = Dense(2, activation='softmax') # 进行2分类

    def call(self, x):
        x = self.c1(x)
        print(":", x.shape)
        x = self.b1(x)
        print(":", x.shape)
        x = self.a1(x)
        print(":", x.shape)
        x = self.p1(x)
        print(":", x.shape)
        x = self.d1(x)
        print(":", x.shape)
        x = self.flatten(x)
        print(":", x.shape)
        x = self.f1(x)
        print(":", x.shape)
        x = self.d2(x)
        print(":", x.shape)
        y = self.f2(x)
        print(":", x.shape)
        return y












#####################################































model = Baseline()

model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                metrics=['sparse_categorical_accuracy'])


checkpoint_save_path = "./checkpoint/Baseline.ckpt"
if os.path.exists(checkpoint_save_path + '.index'):
    print('-------------load the model-----------------')
    model.load_weights(checkpoint_save_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path,
                                                save_weights_only=True,
                                                save_best_only=True)

history = model.fit(train_generator, epochs=10, validation_data=test_generator ,validation_freq=1, callbacks=[cp_callback])

model.summary()

# print(model.trainable_variables)
file = open('./weights.txt', 'w')
for v in model.trainable_variables:
    file.write(str(v.name) + '\n')
    file.write(str(v.shape) + '\n')
    file.write(str(v.numpy()) + '\n')
file.close()

###############################################    show   ###############################################

# 显示训练集和验证集的acc和loss曲线
acc = history.history['sparse_categorical_accuracy']
val_acc = history.history['val_sparse_categorical_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

plt.subplot(1, 2, 1)
plt.plot(acc, label='训练集 Accuracy')
plt.plot(val_acc, label='测试集 Accuracy')
plt.title('训练集与测试集 Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(loss, label='训练集 Loss')
plt.plot(val_loss, label='测试集 Loss')
plt.title('训练集与测试集 Loss')
plt.legend()
plt.show()



# 删除之前的训练结果
删除模型训练结果()