from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class BmiTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None, k=29.999):
        self.columns = columns 
        self.k = k
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X0):
        X = pd.DataFrame(X0)
        if self.columns == "bmi":
            bins = [0, self.k, 100] 
            labels = [0, 1]
            X["bmi_category"] = pd.cut(X['bmi'], bins=bins, labels=labels, right=False)
        else:
            raise ValueError("Vous devez spécifier les colonnes à transformer.")
        return X
    

class AgeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None, k=35):
        self.columns = columns 
        self.k = k
    
    def fit(self, X, y=None):
        # Pas de calcul particulier nécessaire pour cette transformation
        return self
    
    def transform(self, X0):
        X = pd.DataFrame(X0)
        if self.columns == "age":
            bins = [0, self.k, 100]  # Tranches d'age
            labels = [0, 1]
            X["age_category"] = pd.cut(X['age'], bins=bins, labels=labels, right=False)
        else:
            raise ValueError("Vous devez spécifier les colonnes à transformer.")
        return X