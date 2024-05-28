import numpy as np
import pandas as pd


def costfunction(X, y, r, theta, Lambda):
    predictions = np.dot(X, theta.T)
    err = predictions-y
    J = 1/2 * np.sum((err**2) * r)
    reg_x = Lambda/2 * np.sum(np.sum(theta**2))
    reg_theta = Lambda/2 * np.sum(np.sum(X**2))
    grad = J + reg_x + reg_theta
    return J, grad

def gradientDescent(X, y, r, theta, Lambda, num_iter, alpha):
    J_hist = []
    for i in range(num_iter):
        cost, grad = costfunction(X, y, r, theta, Lambda)
        X = X -  alpha*(np.dot(np.dot(X, theta.T) - y, theta) + Lambda*X)
        theta = theta - alpha*(np.dot((np.dot(X, theta.T) - y).T, X) + Lambda*theta)
        J_hist.append(cost)
    return X, theta, J_hist

def normalizeRatings(y, r):
    ymean = np.sum(y, axis=1)/np.sum(r, axis=1)
    ynorm = np.sum(y, axis=1)*np.sum(r, axis=1) - ymean
    return ymean, ynorm

def get_X_theta(num_users):
    X = pd.read_csv("../preprocess/feature_vector.csv")
    Theta1 = np.random.randn(num_users, X.columns)
    return X,Theta1

def get_y(df):
    df.set_index(df.columns[0],inplace=True)
    return df
def get_r(df):
    df.replace(np.NAN,False,inplace=True)
    df.replace(regex="^\d$",value=True,inplace=True)
    for i in range(len(df.columns)):
        df[i] = df[i].replace({True: 1, False: 0})
    return df
df=pd.read_csv('../preprocess/data.csv')
y=get_y(df)
r=get_r(df)
ymean, ynorm = normalizeRatings(y, r)



