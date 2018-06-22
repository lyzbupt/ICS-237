from numpy import concatenate
import numpy as np


class Predict:
    def __init__(self, model, input, scaler):
        self.model = model
        self.input = np.array([input])
        self.scaler = scaler

    def predict(self):
        x = self.input.reshape(self.input.shape[0], 1, self.input.shape[1])
        output = self.model.predict(x)
        x = x.reshape(x.shape[0], x.shape[2])
        output = concatenate((x, output), axis=1)
        output = self.scaler.inverse_transform(output)

        return output[0, -6:]
