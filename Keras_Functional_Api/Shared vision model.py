from keras.layers import Conv2D, MaxPooling2D, Input, Dense, Flatten
from  keras.models import Model
import keras

'''
该模型在两个输入上重复使用同一个图像处理模块，以判断两个 MNIST 数字是否为相同的数字。
'''

# 首先，定义视觉模型
digit_input = Input(shape=(27, 27, 1))
x = Conv2D(64, (3, 3))(digit_input)
x = Conv2D(64, (3, 3,))(x)
x = MaxPooling2D(2, 2)(x)
out = Flatten()(x)

vision_model = Model(digit_input, out)

# 然后，定义区分数字的模型
digit_a = Input(shape=(27, 27, 1))
digit_b = Input(shape=(27, 27, 1))

# 视觉模型将被共享，包括权重和其他所有
out_a = vision_model(digit_a)
out_b = vision_model(digit_b)

concatenated = keras.layers.concatenate([out_a, out_b])
out = Dense(1, activation='sigmoid')(concatenated)

classification_model = Model([digit_a, digit_b], out)
classification_model.summary()

'''
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to
==================================================================================================
input_2 (InputLayer)            (None, 27, 27, 1)    0
__________________________________________________________________________________________________
input_3 (InputLayer)            (None, 27, 27, 1)    0
__________________________________________________________________________________________________
model_1 (Model)                 (None, 7744)         37568       input_2[0][0]
                                                                 input_3[0][0]
__________________________________________________________________________________________________
concatenate_1 (Concatenate)     (None, 15488)        0           model_1[1][0]
                                                                 model_1[2][0]
__________________________________________________________________________________________________
dense_1 (Dense)                 (None, 1)            15489       concatenate_1[0][0]
==================================================================================================
Total params: 53,057
Trainable params: 53,057
Non-trainable params: 0
__________________________________________________________________________________________________

'''
