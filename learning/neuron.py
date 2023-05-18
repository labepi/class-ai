import random

def f_step(value):
    """
    """
    if value > 0:
        return 1.0
    return 0.0

def f_rand():
    """
    """
    return 2 * random.random() - 1

class Perceptron:
    """
    """
    def __init__(self, X, Y, learning_rate=0.01, bias=1.0):
        """
        """
        self.training_set = X
        self.desired_set = Y
        self.set_size = len(self.training_set)
        self.bias = bias
        self.weights = [0] * (len(self.training_set[0]) + 1)
        self.f_activation = f_step
        self.learning_rate = learning_rate
        self.count = 0
        self.changed = True

    def rand_weights(self):
        """
        """
        for i in range(len(self.weights)):
            self.weights[i] = f_rand()

    def compute_output(self, x):
        """
        """
        v = self.bias * self.weights[0]

        for i in range(len(x)):
            v = v + x[i] * self.weights[i + 1]

        return f_step(v)

    def adjust_weights(self, error, x):
        """
        """
        self.weights[0] += self.learning_rate * error * self.bias

        for i in range(len(x)):
            self.weights[i + 1] += self.learning_rate * error * x[i]

    def learn(self):
        """
        """
        order = random.sample(list(range(self.set_size)), self.set_size)
        self.changed = False
        for i in order:
            x = self.training_set[i]
            d = self.desired_set[i]
            y = self.compute_output(x)
            self.adjust_weights(d - y, x)
            if d != y:
                self.changed = True

        self.count = self.count + 1
