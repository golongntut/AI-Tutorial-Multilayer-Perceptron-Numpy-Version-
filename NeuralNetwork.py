# -*- coding: utf-8 -*-

#  @about A 3-layer-sigmoid-MLP Neural Network using Numpy

#  @auth whuang022ai


import numpy as np

import math as mh
import matplotlib.pyplot as plt
import random

LR = []
 
class NeuralNetwork():

    def __init__(self, hidden_layer_size, lr, trainset_path):

        # Load Dataset

        self.dataset = np.genfromtxt(trainset_path, delimiter=',')
        self.hidden_layer_size = hidden_layer_size
        self.input_layer_size = self.dataset.shape[1] - 1
        self.output_layer_size = 1
        self.lr = lr

        # Init Weights

        np.random.seed(1)

        self.input_hidden_weight = np.random.random(
            (self.hidden_layer_size, self.input_layer_size + 1))

        self.hidden_output_weight = np.random.random(
            (self.output_layer_size, self.hidden_layer_size + 1))

    def sigmoid(self, x):

        return 1 / (1 + mh.exp(-x))

    def sigmoid_div(self, y):

        return y * (1 - y)

    def test_forward(self):

        input_data = np.arange(self.input_layer_size)

        for x in range(self.input_layer_size):

            input_data[x] = float(input('Enter the feature: '))

        self.forward(input_data)
        print(self.output_layer)

    def forward(self, input_data=[]):

        # process input data

        # size of input dim

        size = input_data.shape[0]

        # traspose

        input_data = np.reshape(input_data, (size, 1))

        # insert a row of value =1  (bias)

        self.input_layer = np.insert(input_data, size, 1, axis=0)

        # pass data from input to hidden

        sum_hidden_layer = np.dot(self.input_hidden_weight, self.input_layer)

        sigmoid_vec = np.vectorize(self.sigmoid)

        self.hidden_layer = sigmoid_vec(sum_hidden_layer)

        # insert a a row of value =1 (bias)

        self.hidden_layer_tmp = np.insert(
            self.hidden_layer, self.hidden_layer_size, 1, axis=0)

        # pass data from hidden to output

        sum_output_layer = np.dot(
            self.hidden_output_weight,
            self.hidden_layer_tmp)

        self.output_layer = sigmoid_vec(sum_output_layer)

    def backward(self, desire_output_data=[]):

        sigmoid_div_vec = np.vectorize(self.sigmoid_div)

        delta_output = desire_output_data - self.output_layer

        delta_act = sigmoid_div_vec(self.output_layer)

        # delta pass from error to output layer

        self.delta_output_layer = np.multiply(delta_output, delta_act)

        # slice hidden_output weight (remove bias weight)

        hidden_output_weight = self.hidden_output_weight[:,
                                                         :self.hidden_layer_size]

        # delta pass from output layer to hidden layer

        hidden_output_weight_trans = hidden_output_weight.transpose()

        delta_sum_hidden_layer = np.dot(
            hidden_output_weight_trans,
            self.delta_output_layer)

        delta_act_hidden = sigmoid_div_vec(self.hidden_layer)

        self.delta_hidden_layer = np.multiply(
            delta_sum_hidden_layer, delta_act_hidden)

        # delta hidden to output layer weight

        hidden_layer_trans = self.hidden_layer_tmp.transpose()

        self.delta_hidden_output_weight =  \
            np.dot(self.delta_output_layer, hidden_layer_trans)

        # delta input to hidden layer weight

        input_layer_trans = self.input_layer.transpose()

        self.delta_input_hidden_weight =  \
            np.dot(self.delta_hidden_layer, input_layer_trans)

        return delta_output
    
    def update(self,update_strategy,arg=[]):
        

        if (update_strategy=='SGD'):

            LR .append(self.lr)
            self.input_hidden_weight += self.lr *self.delta_input_hidden_weight
            self.hidden_output_weight += self.lr *self.delta_hidden_output_weight

        elif (update_strategy=='SGD-Sigmoid-Annealing'):

            t= arg[0]
            tmax= arg[1]
            lr_min= arg[2]
            lr_max= arg[3]
            self.lr = lr_min+((lr_max-lr_min)*((1 / (1 + mh.exp(t/tmax)))))
            LR .append(self.lr)
            self.input_hidden_weight += self.lr *self.delta_input_hidden_weight
            self.hidden_output_weight += self.lr *self.delta_hidden_output_weight
            
        elif   (update_strategy=='SGD-Momentum'):

            beta= arg[0]
            
            if getattr(self, "input_hidden_weight_vt_old", None) is not None:

                self.input_hidden_weight_vt_new = beta * self.input_hidden_weight_vt_old+self.delta_input_hidden_weight
                self.input_hidden_weight_vt_new = self.lr *self.delta_input_hidden_weight
                self.input_hidden_weight_vt_old = self.input_hidden_weight_vt_new
                
            else:
                
                self.input_hidden_weight_vt_new = self.delta_input_hidden_weight
                self.input_hidden_weight_vt_new = self.lr *self.delta_input_hidden_weight
                self.input_hidden_weight_vt_old = self.input_hidden_weight_vt_new

            if getattr(self, "hidden_output_weight_vt_old", None) is not None:

                self.hidden_output_weight_vt_new =  beta * self.hidden_output_weight_vt_old+self.delta_hidden_output_weight
                self.hidden_output_weight_vt_new = self.delta_hidden_output_weight
                self.hidden_output_weight_vt_old = self.hidden_output_weight_vt_new
                
            else:
                
               self.hidden_output_weight_vt_new =  self.delta_hidden_output_weight
               self.hidden_output_weight_vt_new = self.delta_hidden_output_weight
               self.hidden_output_weight_vt_old = self.hidden_output_weight_vt_new

            LR .append(self.lr)
            self.input_hidden_weight += self.lr *self.input_hidden_weight_vt_new
            self.hidden_output_weight += self.lr *self.hidden_output_weight_vt_new  
             
# define the neural network

learning_rate =  1.5

hidden_layer_neural_numbers = 6

# define the training times

epochMax = 500

lossMin = 0.001

# define the trainset

trainset_col = 5

# 'Xor.csv'

trainset_path = 'Iris-setosa.csv'

# new a neural network

# define the training strategy

update_strategy = 'SGD-Momentum'

MLP = NeuralNetwork(hidden_layer_neural_numbers, learning_rate, trainset_path)

# do training , count mse

MSES = []

for epoch in range(epochMax):

    error_square_sum = 0
    
    # creat traing seqense

    traing_seqense= np.arange(len(MLP.dataset))

    # randomlize seqense

    random.shuffle(traing_seqense)
    
    for x in range(len(MLP.dataset)):
        
        MLP.forward(MLP.dataset[traing_seqense[x], :trainset_col - 1])
        error = MLP.backward(MLP.dataset[traing_seqense[x], trainset_col - 1:trainset_col])
        error_square_sum += np.square(error)
        #arg = np.array([(epoch-1)*len(MLP.dataset)+x,epochMax,0.75,1.5,0.7])
        arg = np.array([0.7])
        MLP.update(update_strategy,arg)
        #MLP.update(update_strategy)
        
    MSE = error_square_sum / len(MLP.dataset)

    print('Epoch ' + str(epoch) + ' loss : ' + str(MSE))

    MSES.append(MSE[0][0])

    if(MSE < lossMin):

        break

plt.plot(MSES)
plt.show()

plt.plot(LR)
plt.show()

# testing the neural netwok by user input

test_times = 5

for i in range(test_times):
    MLP.test_forward()
