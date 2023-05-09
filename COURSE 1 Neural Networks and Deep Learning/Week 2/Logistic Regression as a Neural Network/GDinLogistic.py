import numpy as np
from PIL import Image
import h5py
from scipy import ndimage
from lr_utils import load_dataset
import matplotlib.pyplot as plt

train_set_x_orig, train_set_y, test_set_x_orig, test_set_y, classes = load_dataset()

train_set_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T
test_set_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T

train_set_x = train_set_x_flatten / 255
test_set_x = test_set_x_flatten / 255


def sigmoid(x):
    s = 1.0 / (1.0 + np.exp(-1.0 * x))
    return s


def initialize_with_zeros(dim):
    w = np.zeros((dim, 1))
    b = 0
    assert (w.shape == (dim, 1))
    assert (isinstance(b, float) or isinstance(b, int))
    return w, b


def propagate(w, b, X, Y):
    # Forward Propagation
    m = X.shape[1]
    z = np.dot(w.T, X) + b
    A = sigmoid(z)
    cost = -(1.0 / m) * np.sum(Y * np.log(A) + (1 - Y) * np.log(1 - A))
    # Backward Propagation
    dw = (1.0 / m) * np.dot(X, (A - Y).T)
    db = (1.0 / m) * np.sum(A - Y)

    assert (dw.shape == w.shape)
    assert (db.dtype == float)
    cost = np.squeeze(cost)
    grads = {"dw": dw, "db": db}
    return grads, cost


def optimization(w, b, X, Y, num_iterations, learning_rate, print_cost=False):
    costs = []
    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)
        dw = grads["dw"]
        db = grads["db"]
        w = w - learning_rate * dw
        b = b - learning_rate * db
        if i % 100 == 0:
            costs.append(cost)
        if print_cost and i % 100 == 0:
            print("cost after iteration %i: %f" % (i, cost))
    params = {"w": w, "b": b}
    grads = {"dw": dw, "db": db}
    return params, grads, costs


def predict(w, b, X):
    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    w = w.reshape(X.shape[0], 1)
    A = sigmoid(np.dot(w.T, X) + b)
    for i in range(A.shape[1]):
        if A[0, i] > 0.5:
            Y_prediction[0, i] = 1
        else:
            Y_prediction[0, i] = 0
    assert (Y_prediction.shape == (1, m))
    return Y_prediction


def model(X_train, Y_train, X_test, Y_test, num_iterations=2000, learning_rate=0.5, print_cost=False):
    m = X_train[1]
    # initialization with zero
    w, b = initialize_with_zeros(X_train.shape[0])
    # Gradient Descent
    parameter, grads, costs = optimization(w, b, X_train, Y_train, num_iterations, learning_rate, print_cost)
    # Get parameters from optimization
    w = parameter["w"]
    b = parameter["b"]
    # Predict Samples
    Y_prediction_train = predict(w, b, X_train)
    Y_prediction_test = predict(w, b, X_test)
    # Print train/test error
    print("train accuracy:{} %".format(100 - np.mean(np.abs(Y_prediction_train-Y_train)) * 100))
    print("test accuracy:{} %".format(100-np.mean(np.abs(Y_prediction_test-Y_test)) * 100))
    d = {"costs":costs,
         "Y_prediction_train":Y_prediction_train,
         "Y_prediction_test":Y_prediction_test,
         "w":w,
         "b":b,
         "learning_rate":learning_rate,
         "num_iterations":num_iterations}
    return d

d = model(train_set_x,train_set_y,test_set_x,test_set_y,num_iterations=2000,learning_rate=0.005,print_cost=False)

costs = np.squeeze(d['costs'])
plt.plot(costs)
plt.ylabel('cost')
plt.xlabel('iterations (per hundreds)')
plt.title("Learning rate =" + str(d["learning_rate"]))
plt.show()