# Column Transformer in Machine Learning | How to use ColumnTransformer in Sklearn

**Video Link:** [https://www.youtube.com/watch?v=5TVj6iEBR4I](https://www.youtube.com/watch?v=5TVj6iEBR4I)

**Summary:** ColumnTransformer Scikit-Learn ki ek powerful class hai jo heterogeneous dataset ke alag-alag columns par parallel transformations apply karke manual concatenation aur data leakage ko khatam karti hai.

## Theory

### Motivation behind Column Transformer ([00:11](https://youtu.be/5TVj6iEBR4I?t=11))

Real-world machine learning datasets me alag-alag tarah ke features (columns) hote hain. Kuch columns numerical hote hain, kuch nominal categorical, kuch ordinal categorical, aur kisi me missing values hoti hain.

### Why it is needed:
Traditional feature engineering me har column type ke liye alag se transformation apply karna padta hai:
1. Missing values ko impute karne ke liye `SimpleImputer` use karna.
2. Nominal categorical variables ke liye `OneHotEncoder` lagana.
3. Ordinal categorical variables ke liye `OrdinalEncoder` apply karna.
4. Untransformed features (jaise raw age) ko alag extract karna.

Is process me har step ek naya NumPy array generate karta hai. End me in sabhi arrays ko `np.concatenate` karke ek final feature array banana padta hai. Ye process bahut tedious, inefficient, aur code-heavy hoti hai.

`ColumnTransformer` (Scikit-Learn) is problem ka solution hai. Ye ek single class hai jo alag-alag columns par unke respective transformers bind karti hai aur directly single line me complete feature array return karti hai.

### Dataset Structure & Exploratory Breakdown ([02:56](https://youtu.be/5TVj6iEBR4I?t=176))

Lecture me preprocessing demonstrate karne ke liye ek synthetic dataset `covid_toy.csv` use kiya gaya hai jisme total 100 rows aur 6 columns hain.

### Column Breakdown:
- **`age`**: Numerical column (No preprocessing applied in this lesson, extracted directly).
- **`gender`**: Nominal categorical column (Male / Female) -> Requires **OneHotEncoder**.
- **`fever`**: Numerical column containing 10 missing values (`df.isnull().sum()`) -> Requires **SimpleImputer** (mean imputation).
- **`cough`**: Ordinal categorical column (`Mild`, `Strong`) -> Requires **OrdinalEncoder**.
- **`city`**: Nominal categorical column (Kolkata, Bangalore, Delhi, Mumbai) -> Requires **OneHotEncoder**.
- **`has_covid`**: Target label (Yes / No) -> Used for `y_train` / `y_test` split.

### Traditional Preprocessing Pipeline ("Aam Zindagi") ([06:20](https://youtu.be/5TVj6iEBR4I?t=380))

Traditional approach me har transformation ko individually fit aur transform kiya jata hai:

### Step-by-Step Working:
1. **Train-Test Split**: `train_test_split` se dataset ko 80% train (80 rows) aur 20% test (20 rows) me divide kiya jata hai.
2. **Fever Imputation**: `SimpleImputer()` ko `X_train[['fever']]` par fit_transform karke missing values replace karte hain -> Resultant shape: `(80, 1)`.
3. **Cough Ordinal Encoding**: `OrdinalEncoder(categories=[['Mild', 'Strong']])` apply karke `Mild` ko 0 aur `Strong` ko 1 assign karte hain -> Resultant shape: `(80, 1)`.
4. **Gender & City One-Hot Encoding**: `OneHotEncoder(drop='first', sparse=False)` apply karte hain. Gender (2 categories - 1 dropped = 1 col) aur City (4 categories - 1 dropped = 3 cols) combine ho kar -> Resultant shape: `(80, 4)`.
5. **Age Extraction**: Untransformed `age` column ko DataFrame se drop karke NumPy array banaya jata hai -> Resultant shape: `(80, 1)`.

In saare intermediate arrays (`X_train_age`, `X_train_fever`, `X_train_gender_city`, `X_train_cough`) ko manually track karna padta hai.

### Limitations of Manual Preprocessing (Aam Zindagi) ([10:00](https://youtu.be/5TVj6iEBR4I?t=600))

Manual feature preprocessing ('Aam Zindagi') mein hum har column ya column group ko alag-alag encode/impute karte hain (`SimpleImputer`, `OrdinalEncoder`, `OneHotEncoder`). Untouched columns (jaise `age`) ko `.drop()` aur `.values` ke saath extract karna padta hai, aur aakhir mein saare separate NumPy arrays ko `np.concatenate(..., axis=1)` se jodhna padta hai.

### Limitations:
1. **High Complexity**: Agar dataset mein 50+ columns hon, toh har group ke liye variables maintain karna aur unhe sahi sequence mein concatenate karna bohot tedious aur error-prone hota hai.
2. **Repetitive Code**: Same transformations train aur test sets dono par alag-alag array operations ke through repeat karni padti hain.
3. **Data Leakage Risk**: Train aur test arrays ko alag-alag handle karne se manual errors aur data leakage ki probability badh jaati hai.

### Introduction to ColumnTransformer (Mentos Zindagi) ([10:52](https://youtu.be/5TVj6iEBR4I?t=652))

Scikit-Learn ka `ColumnTransformer` (`sklearn.compose.ColumnTransformer`) ek streamlined technique hai jo multi-column heterogenous dataset par alag-alag preprocessing steps ko ek saath define aur apply karne ki permission deti hai.

### Structure & Parameters of ColumnTransformer:
`ColumnTransformer(transformers=[...], remainder='passthrough'|'drop')`

1. **`transformers`**: A list of tuples. Har tuple mein exactly 3 items hote hain:
   - **Name (String)**: Transformer ka arbitrary unique identifier (e.g., `'tnf1'`, `'tnf2'`).
   - **Transformer Object**: Applied class ka instance (e.g., `SimpleImputer()`, `OrdinalEncoder()`, `OneHotEncoder()`).
   - **Columns List**: Input feature names jin par ye transformer apply hona hai (e.g., `['fever']`, `['gender', 'city']`).
2. **`remainder`**:
   - `'drop'` *(default)*: Jin columns par koi transformation define nahi ki gayi (e.g., `age`), unhe final output array se hata diya jata hai.
   - `'passthrough'`: Jin columns par koi transformation nahi lagi, unhe bina kisi badlaav ke output array ke end mein concatenate kar diya jata hai.

### Fitting and Transforming Train/Test Sets ([13:45](https://youtu.be/5TVj6iEBR4I?t=825))

Ek baar `ColumnTransformer` ka object define ho jaane ke baad, poore preprocessing sequence ko execute karne ke liye standard Scikit-Learn API methods use kiye jaate hain:

1. **`transformer.fit_transform(X_train)`**: Training data se parameters learn karta hai (e.g., mean/median for imputer, category levels for encoders) aur transformation apply karke final NumPy array return karta hai.
2. **`transformer.transform(X_test)`**: Training data par fitted transformer rules ko bina dubara fit kiye direct test data `X_test` par apply karta hai to prevent data leakage.

## Intuition

- ([00:48](https://youtu.be/5TVj6iEBR4I?t=48)) Samajhne wali baat ye hai ki agar ek ghar banane ke liye 4 alag-alag contractors ko alag-alag rooms ka kaam diya jaye, aur badme saare rooms ko jodna pade, toh chaos hoga. Pehle ek array fever ka banao, fir ek gender-city ka, fir cough ka, fir age alag nikaalo... ye 'Aam Zindagi' (hard way) hai. ColumnTransformer ek single project manager ki tarah hai jo saare rooms ko ek saath design karke final building ready karke deta hai.
- ([10:53](https://youtu.be/5TVj6iEBR4I?t=653)) Manual preprocessing 'Aam Zindagi' hai - jahan har ek feature ke liye alag se array banana, slice karna aur concatenate karna padta hai. `ColumnTransformer` 'Mentos Zindagi' hai - jahan aap ek blueprint ready kar dete ho ki kis column par kya operation chalega, aur fit_transform call karte hi saari processing backend par automatically combine ho kar ready array de deti hai.

## Code

### Imports and Data Loading [official] ([02:56](https://youtu.be/5TVj6iEBR4I?t=176))
Required libraries import karke `covid_toy.csv` file load ki gayi hai.

```python
import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder

df = pd.read_csv('covid_toy.csv')
df.head()
```

### Missing Value Check and Train-Test Split [official] ([05:28](https://youtu.be/5TVj6iEBR4I?t=328))
Dataset me null values check karne ke baad `has_covid` ko drop karke input/target features split kiye gaye hain.

```python
df.isnull().sum()

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(df.drop(columns=['has_covid']),df['has_covid'],
                                                test_size=0.2)
```

### Aam Zindagi Step 1: Missing Value Imputation on Fever [official] ([07:13](https://youtu.be/5TVj6iEBR4I?t=433))
SimpleImputer ka use karke `fever` column ki 10 missing values ko mean value se impute kiya gaya.

```python
# adding simple imputer to fever col
si = SimpleImputer()
X_train_fever = si.fit_transform(X_train[['fever']])

# also the test data
X_test_fever = si.fit_transform(X_test[['fever']])
                                 
X_train_fever.shape
```

### Aam Zindagi Step 2: Ordinal Encoding on Cough Column [official] ([08:11](https://youtu.be/5TVj6iEBR4I?t=491))
OrdinalEncoder ka use karke `cough` column ke categories `Mild` aur `Strong` ko ordered integer values me transform kiya gaya.

```python
# Ordinalencoding -> cough
oe = OrdinalEncoder(categories=[['Mild','Strong']])
X_train_cough = oe.fit_transform(X_train[['cough']])

# also the test data
X_test_cough = oe.fit_transform(X_test[['cough']])

X_train_cough.shape
```

### Aam Zindagi Step 3: One-Hot Encoding on Gender and City [official] ([08:48](https://youtu.be/5TVj6iEBR4I?t=528))
OneHotEncoder me `drop='first'` set karke dummy variable trap/multicollinearity avoid karte hue `gender` aur `city` ko encode kiya gaya.

```python
# OneHotEncoding -> gender,city
ohe = OneHotEncoder(drop='first',sparse=False)
X_train_gender_city = ohe.fit_transform(X_train[['gender','city']])

# also the test data
X_test_gender_city = ohe.fit_transform(X_test[['gender','city']])

X_train_gender_city.shape
```

### Aam Zindagi Step 4: Extracting Age Feature [official] ([09:41](https://youtu.be/5TVj6iEBR4I?t=581))
Raw `age` feature ko baaki saare columns drop karke direct NumPy array ke form me extract kiya gaya.

```python
# Extracting Age
X_train_age = X_train.drop(columns=['gender','fever','cough','city']).values

# also the test data
X_test_age = X_test.drop(columns=['gender','fever','cough','city']).values

X_train_age.shape
```

### Manual Concatenation Approach (Aam Zindagi) [official] ([10:00](https://youtu.be/5TVj6iEBR4I?t=600))
Manual method mein har encoded transformer ka output slice lekar np.concatenate se manual join karna padta hai.

```python
# Concatenating transformed arrays manually
X_train_transformed = np.concatenate((X_train_age, X_train_fever, X_train_gender_city, X_train_cough), axis=1)
X_test_transformed = np.concatenate((X_test_age, X_test_fever, X_test_gender_city, X_test_cough), axis=1)

print(X_train_transformed.shape)  # Output: (80, 7)
```

### ColumnTransformer Implementation (Mentos Zindagi) [official] ([10:52](https://youtu.be/5TVj6iEBR4I?t=652))
ColumnTransformer import karke saare transformers ko tuples ki form mein column mapping ke saath define karna aur fit_transform apply karna.

```python
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
```

## Analogies

- ([06:48](https://youtu.be/5TVj6iEBR4I?t=408)) **Analogy:** Aam Zindagi vs Mentos Zindagi — *Explains:* Aam Zindagi (Traditional Approach) me har column ko manually isolate karke preprocess karna padta hai aur alag-alag arrays ko track karke concatenate karna padta hai. Mentos Zindagi (ColumnTransformer) me ek hi transformer saare columns par alag-alag rules ek line me apply kar deta hai.
- ([10:53](https://youtu.be/5TVj6iEBR4I?t=653)) **Analogy:** Aam Zindagi vs Mentos Zindagi — *Explains:* Aam Zindagi manual feature handling ko represent karti hai jahan bohot sara messy code likhna padta hai. Mentos Zindagi ColumnTransformer ko represent karti hai jo smart, concise aur single-line efficient automation provide karta hai.

## Common Mistakes

- **Mistake [added]:** Data leakage caused by fitting imputers/encoders on test data separately using fit_transform. ([07:25](https://youtu.be/5TVj6iEBR4I?t=445))
  - *Why:* Test data par `.fit_transform()` call karne se test data ki information leaks ho sakti hai. Test set par sirf `.transform()` hona chahiye.
  - *Fix:* Always use `.fit_transform()` on training data and only `.transform()` on test data.
- **Mistake [added]:** Passing 1D Series instead of 2D DataFrame to Scikit-Learn Transformers (e.g. `X_train['fever']` vs `X_train[['fever']]`). ([07:26](https://youtu.be/5TVj6iEBR4I?t=446))
  - *Why:* Scikit-Learn transformers input shape `(n_samples, n_features)` (2D array/DataFrame) expect karte hain.
  - *Fix:* Use double brackets `X_train[['column_name']]` to retain a 2D structure.
- **Mistake [teacher]:** DataFrame column name mein Case Sensitivity mistake (e.g., 'Fever' vs 'fever') ([14:00](https://youtu.be/5TVj6iEBR4I?t=840))
  - *Why:* Pandas DataFrame column names case-sensitive hote hain. Agar ColumnTransformer mein capital letter 'Fever' paas karenge jabki DataFrame mein 'fever' ho, toh pandas KeyLookup fail ho jata hai.
  - *Fix:* DataFrame ke exact column names (`X_train.columns`) check karke lowercase/uppercase exact string pass karein.
- **Mistake [teacher]:** remainder='passthrough' skip kar dena ([11:22](https://youtu.be/5TVj6iEBR4I?t=682))
  - *Why:* Default `remainder='drop'` hone ki wajah se jin columns par transformation apply nahi hoti (jaise 'age'), wo final output array se drop ho jaate hain.
  - *Fix:* Untouched features ko retain karne ke liye `remainder='passthrough'` explicitly set karein.
- **Mistake [added]:** Test data par transformer.fit_transform(X_test) call karna ([14:48](https://youtu.be/5TVj6iEBR4I?t=888))
  - *Why:* Test data par fit call karne se model testing phase mein test distribution ke parameters seekh leta hai, jisse Data Leakage hoti hai.
  - *Fix:* Always use `fit_transform()` on `X_train` and only `transform()` on `X_test`.

## Formulas & Key Terms

### Formulas
- **Mean Imputation Formula:** `\bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_i` — SimpleImputer missing values ko numeric column ke available non-null values ke mean (average) se replace karta hai.
- **ColumnTransformer Structure:** `ColumnTransformer(transformers=[(name, transformer_object, column_list)], remainder='passthrough')` — List of tuples where each tuple binds a transformer to specific columns, with a remainder strategy for unmentioned features.

### Key Terms
- **ColumnTransformer:** Scikit-Learn ka feature transformation tool jo dataset ke alag-alag columns par parallel me different transformers apply karne ki permission deta hai.
- **SimpleImputer:** Missing values ko strategy (mean, median, mode) ke base par fill karne wali Scikit-Learn class.
- **OneHotEncoder:** Nominal categorical data ko binary (0/1) dummy variables me convert karne ka encoder.
- **OrdinalEncoder:** Ordered categorical features (e.g., Mild, Strong) ko sequence-based integers (0, 1, 2) me convert karne ka encoder.
- **Multicollinearity (Dummy Variable Trap):** OneHotEncoder me redundant columns ki wajah se aane wali problem, jise avoid karne ke liye `drop='first'` specify kiya jata hai.
- **remainder:** ColumnTransformer ka argument jo un-transformed columns ki handling define karta hai ('passthrough' to keep, 'drop' to delete).
- **passthrough:** Value of remainder parameter jo untransformed columns ko directly output mein include karne ki permission deti hai.
- **fit_transform:** Method jo training data se transformation rules learn (fit) karta hai aur use array par apply (transform) karta hai.
