#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : main.py
# @Time     : Tue 10 Sep 2019 01:10:28 PM CST
# @Author   : Lishuxiang
# @E-mail   : lishuxiang@cug.edu.cn
# @Function :

import os
import tensorflow as tf
import matplotlib.pyplot as plt
# Importing the required Keras modules containing model and layers
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D


def detect(index: int) -> int:
    if not os.path.exists("my_model.h5"):
        compile_fit()
    model = tf.keras.models.load_model('my_model.h5')
    plt.imshow(x_test[image_index].reshape(28, 28), cmap='Greys')
    plt.show()
    pred = model.predict(x_test[image_index].reshape(1, 28, 28, 1))
    print("The number is " + str(pred.argmax()))


def compile_fit():
    # Creating a Sequential Model and adding the layers
    model = Sequential()
    model.add(Conv2D(28, kernel_size=(3, 3), input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())  # Flattening the 2D arrays for fully connected layers
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dropout(0.2))
    model.add(Dense(10, activation=tf.nn.softmax))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x=x_train, y=y_train, epochs=10)
    model.evaluate(x_test, y_test)
    model.save('my_model.h5')


def menu() -> int:
    print('Menu:')
    print('1:Detect handwritten number.')
    print('2:Practise model.')
    print('3:Exit.')
    return int(input('Choice: '))


# init mnist databases
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
# print(x_train.shape)
# Reshaping the array to 4-dims so that it can work with the Keras API
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
input_shape = (28, 28, 1)
# Making sure that the values are float so that we can get decimal points after division
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
# Normalizing the RGB codes by dividing it to the max RGB value.
x_train /= 255
x_test /= 255

if __name__ == '__main__':
    choice = menu()
    if choice == 1:
        image_index = int(input("index(0-9999):"))
        detect(image_index)
    elif choice == 2:
        compile_fit()
    else:
        print('Bye!')
        exit(0)
