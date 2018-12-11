# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Libraries
import numpy as np
import matplotlib.pyplot as plt
import pickle

from cso import Cso
import matplotlib.pyplot as plt

# Data Set -- Fashon Mnist
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images,
                               test_labels) = fashion_mnist.load_data()

# Preprocess Dataset
validation_images = train_images[:10000]
validation_labels = train_labels[:10000]
training_images = train_images[10000:20000]
training_labels = train_labels[10000:20000]
# normalize
training_images = training_images / 255.0
validation_images = validation_images / 255.0
test_images = test_images / 255.0
# class name
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

search_table = {}
def objectfunction(param):

    """
    Compute the fitness for each partical accroding the error rate on validation set.
    Input:
        param : the particle's position, so is the architecture of nn;
    Return:
        fitness : the error rate of this architecture on validation set.
    """
    param = 100 * param
    param = [int(i) for i in param]

    # Check if in search table or not
    if str(param)  in search_table:
        return search_table[str(param)]

    print(param)
    # Initial Model
    params = [keras.layers.Flatten(input_shape=(28, 28))]
    for num_units in param:
        params.append(keras.layers.Dense(num_units, activation=tf.nn.relu))
    # last layer
    params.append(keras.layers.Dense(10, activation=tf.nn.softmax))

    model = keras.Sequential(params)
    # Compile model
    model.compile(optimizer=tf.train.AdamOptimizer(),
                                loss = 'sparse_categorical_crossentropy',
                                metrics=['accuracy'])
    # Train the model
    model.fit(training_images, training_labels, epochs=5)
    # Evaluation on validation data
    _, validation_acc = model.evaluate(validation_images, validation_labels)

    error = 1.0 - validation_acc
    
    search_table[str(param)] = error
    return error

cso = Cso(10, objectfunction, 0,1,2,20, mr = 5,smp =2)

result = (cso.get_agents(), cso.get_Gbest())
print(result)
with open('result_cso.pkl', 'wb') as f:
    pickle.dump(result, f, 0)
