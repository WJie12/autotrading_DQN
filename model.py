# import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


def mlp(n_obs, n_action, n_hidden_layer=1, n_neuron_per_layer=32,
        activation='relu', loss='mse'):
    """ A multi-layer perceptron """
    print(n_action)
    model = Sequential()

    model.add(Dense(n_neuron_per_layer, input_dim=n_obs, activation=activation))
    for _ in range(n_hidden_layer):
        model.add(Dense(n_neuron_per_layer, activation=activation))
    model.add(Dense(n_action, activation='linear'))
    model.compile(loss=loss, optimizer=Adam())
    print(model.summary())
    return model

    # model.add(Dense(units=64, input_dim=n_obs, activation="relu"))
    # model.add(Dense(units=64, input_dim=n_obs, activation="relu"))
    # model.add(Dense(units=32, activation="relu"))
    # model.add(Dense(units=8, activation="relu"))
    # model.add(Dense(n_action, activation="linear"))
    # model.compile(loss="mse", optimizer=Adam(lr=0.001))
    # print(model.summary())
    # return model
