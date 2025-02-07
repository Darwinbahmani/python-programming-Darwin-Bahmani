import numpy as np
from scipy.stats import f

class StatisticalMethods:
    def __init__(self, X, Y):
        #Initierar modellen och lagrar data
        self.X = np.hstack((np.ones((X.shape[0], 1)), X))  
        self.Y = Y
        self.n = X.shape[0]  
        self.d = X.shape[1]  
        self.b = None  

    def fit(self):
        #Beräknar koefficienterna med OLS
        self.b = np.linalg.inv(self.X.T @ self.X) @ self.X.T @ self.Y

    def predict(self, X_new):
        #Gör prediktioner för nya data
        X_new = np.hstack((np.ones((X_new.shape[0], 1)), X_new))
        return X_new @ self.b

    def calculate_variance(self):
        #Beräknar variansen i modellen
        residuals = self.Y - self.X @ self.b
        SSE = np.sum(residuals ** 2)
        return SSE / (self.n - self.d - 1)

    def calculate_standard_deviation(self):
        #Standardavvikelsen är roten ur variansen
        return np.sqrt(self.calculate_variance())

    def calculate_f_statistic(self):
        #Utför F-test för att kontrollera regressionens signifikans
        SSR = np.sum((self.X @ self.b - np.mean(self.Y)) ** 2)
        SSE = np.sum((self.Y - self.X @ self.b) ** 2)
        F_stat = (SSR / self.d) / (SSE / (self.n - self.d - 1))
        p_value = f.sf(F_stat, self.d, self.n - self.d - 1)
        return F_stat, p_value

