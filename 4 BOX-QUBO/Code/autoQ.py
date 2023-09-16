import numpy as np
from tensorflow.keras.layers import Input, Dense, Multiply
from tensorflow.keras.models import Model
from tensorflow import keras
from tensorflow.keras import initializers
import utils
from keras.models import load_model



class autoQ:

    def __init__(self, init_X, init_Y, ratio):
        self.X = list(init_X)
        self.Y = list(init_Y)
        self.ratio = ratio
        self.n = len(init_X[0])
        self.n_params = (self.n+1)*self.n//2

        self.D = [[init_X[i], init_Y[i]] for i in range(len(init_X))]
        self.D.sort(key=lambda x:x[1])
        self.threshold = self.D[max(0,int(len(self.D)*self.ratio)-1)][1]

        self.model = self.__create_model()

    def __create_model(self):
        p_input = Input(1, name="p_input")
        mask_input = Input(self.n_params, name="mask_input")
        predicted_Q = Dense(self.n_params, activation='linear', use_bias=False, name="Q")(p_input)
        masked_Q = Multiply()([predicted_Q, mask_input])
        predicted_E = Dense(1, activation="linear", trainable=False,
                            kernel_initializer=initializers.Ones(),
                            bias_initializer=initializers.Zeros())(masked_Q)
        predicted_E_offset = Dense(1, activation="linear", name="offset")(predicted_E)
        model = Model(inputs=[p_input, mask_input], outputs=predicted_E_offset)
        opt = keras.optimizers.Adam(learning_rate=0.001)
        model.compile(loss="mse", optimizer=opt)
        return model

    def __get_flat_upper_triangular_matrix(self, X):
        flat_upper_X = np.zeros(self.n_params)
        j = 0
        for i in range(self.n):
            flat_upper_X[j:j+self.n-i] = X[i][i:]
            j += self.n-i
        return flat_upper_X

    def get_Q(self):
        Q_flat = self.model.get_layer('Q').get_weights()[0][0]
        offset = self.model.get_layer('offset').get_weights()
        scaling = offset[0][0][0]
        bias = offset[1][0]

        Q = np.zeros((self.n, self.n))
        j = 0
        for i in range(self.n):
            Q[i][i:] = Q_flat[j:j+self.n-i]
            j += self.n-i
        Q = Q * scaling

        Q_dict = {}
        for i in range(self.n):
            for j in range(self.n):
                if Q[i][j] != 0 and i <= j:
                    Q_dict[(i,j)] = Q[i][j]

        return Q_dict, bias

    def train(self, n_cycles, n_epochs):

        p_inputs, mask_inputs = [], []
        for i in range(len(self.D)):
            p_inputs.append([1])
            mask_inputs.append(self.__get_flat_upper_triangular_matrix(np.outer(self.D[i][0], self.D[i][0])))
        p_inputs, mask_inputs = np.array(p_inputs), np.array(mask_inputs)

        min_loss = 999999

        for c in range(n_cycles):
            predicted_Y = self.model([p_inputs, mask_inputs])
            target_p_inputs = []
            target_mask_inputs = []
            target_Y = []
            for i in range(len(self.D)):
                if i < int(len(self.D)*self.ratio) and self.D[i][1] < 1:
                    target_p_inputs.append([1])
                    target_mask_inputs.append(mask_inputs[i])
                    target_Y.append([self.D[i][1]])
                elif predicted_Y[i][0] < self.threshold:
                    target_p_inputs.append([1])
                    target_mask_inputs.append(mask_inputs[i])
                    target_Y.append([self.threshold])
            target_p_inputs = np.array(target_p_inputs)
            target_mask_inputs = np.array(target_mask_inputs)
            target_Y = np.array(target_Y)

            self.model.fit({"p_input": target_p_inputs, "mask_input": target_mask_inputs}, target_Y, epochs=n_epochs,
                                    batch_size=1024, verbose=0, shuffle=True)
            loss = np.mean((self.model([target_p_inputs, target_mask_inputs]) - target_Y) ** 2)
            print("Cycle: ", c, " / ", n_cycles, "     - Loss: ", loss)
            if loss < min_loss:
                min_loss = loss
                self.model.save('best_model.h5')

        self.model = load_model('best_model.h5')

    def test(self, n_test):
        Q, bias = self.get_Q()
        for i in range(min(n_test, len(self.D))):
            predicted_y = utils.getValue(Q, self.D[i][0]) + bias
            if i < int(len(self.D)*self.ratio) and self.D[i][1] < 1:
                print("                                                                                   *** ", end='')
            else:
                print("                                                                                   ", end='')
            print(self.D[i][1], "   <=>   ", predicted_y, np.array(self.D[i][0]))
        print("len: ", len(self.D))

    def add(self, X, Y):
        for i in range(len(X)):
            new = True
            for x in self.X:
                if np.all(X[i] == x):
                    new = False
                    break
            if new:
                self.X.append(X[i])
                self.Y.append(Y[i])
                self.D.append([X[i],Y[i]])
        self.D.sort(key=lambda x: x[1])
        self.threshold = self.D[max(0,int(len(self.D)*self.ratio)-1)][1]

