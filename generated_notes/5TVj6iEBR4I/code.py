"""Code extracted from: Column Transformer in Machine Learning | How to use ColumnTransformer in Sklearn"""

#======================================================================
# Block 1: Imports and Data Loading | Label: official | Timestamp: 02:56
#======================================================================
import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder

df = pd.read_csv('covid_toy.csv')
df.head()


#======================================================================
# Block 2: Missing Value Check and Train-Test Split | Label: official | Timestamp: 05:28
#======================================================================
df.isnull().sum()

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(df.drop(columns=['has_covid']),df['has_covid'],
                                                test_size=0.2)


#======================================================================
# Block 3: Aam Zindagi Step 1: Missing Value Imputation on Fever | Label: official | Timestamp: 07:13
#======================================================================
# adding simple imputer to fever col
si = SimpleImputer()
X_train_fever = si.fit_transform(X_train[['fever']])

# also the test data
X_test_fever = si.fit_transform(X_test[['fever']])
                                 
X_train_fever.shape


#======================================================================
# Block 4: Aam Zindagi Step 2: Ordinal Encoding on Cough Column | Label: official | Timestamp: 08:11
#======================================================================
# Ordinalencoding -> cough
oe = OrdinalEncoder(categories=[['Mild','Strong']])
X_train_cough = oe.fit_transform(X_train[['cough']])

# also the test data
X_test_cough = oe.fit_transform(X_test[['cough']])

X_train_cough.shape


#======================================================================
# Block 5: Aam Zindagi Step 3: One-Hot Encoding on Gender and City | Label: official | Timestamp: 08:48
#======================================================================
# OneHotEncoding -> gender,city
ohe = OneHotEncoder(drop='first',sparse=False)
X_train_gender_city = ohe.fit_transform(X_train[['gender','city']])

# also the test data
X_test_gender_city = ohe.fit_transform(X_test[['gender','city']])

X_train_gender_city.shape


#======================================================================
# Block 6: Aam Zindagi Step 4: Extracting Age Feature | Label: official | Timestamp: 09:41
#======================================================================
# Extracting Age
X_train_age = X_train.drop(columns=['gender','fever','cough','city']).values

# also the test data
X_test_age = X_test.drop(columns=['gender','fever','cough','city']).values

X_train_age.shape


#======================================================================
# Block 7: Manual Concatenation Approach (Aam Zindagi) | Label: official | Timestamp: 10:00
#======================================================================
# Concatenating transformed arrays manually
X_train_transformed = np.concatenate((X_train_age, X_train_fever, X_train_gender_city, X_train_cough), axis=1)
X_test_transformed = np.concatenate((X_test_age, X_test_fever, X_test_gender_city, X_test_cough), axis=1)

print(X_train_transformed.shape)  # Output: (80, 7)


#======================================================================
# Block 8: ColumnTransformer Implementation (Mentos Zindagi) | Label: official | Timestamp: 10:52
#======================================================================
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder

# Defining the ColumnTransformer
transformer = ColumnTransformer(transformers=[
    ('tnf1', SimpleImputer(), ['fever']),
    ('tnf2', OrdinalEncoder(categories=[['Mild', 'Strong']]), ['cough']),
    ('tnf3', OneHotEncoder(sparse=False, drop='first'), ['gender', 'city'])
], remainder='passthrough')

# Transforming training and testing data
X_train_transformed = transformer.fit_transform(X_train)
X_test_transformed = transformer.transform(X_test)

print(X_train_transformed.shape)  # Output: (80, 7)
print(X_test_transformed.shape)   # Output: (20, 7)

