import numpy as np
from sklearn.datasets import load_boston
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


class SimpleLinearRegression:
    def __init__(self):
        self.theta_0 = None
        self.theta = None

    def fit(self, X_train, y_train):
        X = np.hstack([np.ones((len(X_train), 1)), X_train])
        self.theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y_train)
        self.theta_0 = self.theta[0]
        return self

    def predict(self, X_predict):
        assert self.theta is not None and self.theta_0 is not None
        assert X_predict is not None
        X = np.hstack([np.ones((len(X_predict), 1)), X_predict])
        return X.dot(self.theta)

    def score(self, X_test, y_test):
        X = np.hstack([np.ones((len(X_test), 1)), X_test])
        y_predict = X.dot(self.theta)
        return r2_score(y_test, y_predict)

    def __repr__(self):
        return "SimpleLinearRegression"


boston = load_boston()
X_train, X_test, y_train, y_test = train_test_split(boston.data, boston.target, test_size=0.2)
reg = SimpleLinearRegression()
reg.fit(X_train, y_train)
reg.predict(X_test)
