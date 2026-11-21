# Revision Pack: Column Transformer in Machine Learning | How to use ColumnTransformer in Sklearn

**One-Line Summary:** ColumnTransformer Scikit-Learn ki ek powerful class hai jo heterogeneous dataset ke alag-alag columns par parallel transformations apply karke manual concatenation aur data leakage ko khatam karti hai.

## Cheat Sheet

### ColumnTransformer Quick Reference

| Feature / Parameter | Detail / Usage | Syntax / Value |
| :--- | :--- | :--- |
| **Module Import** | Import path from sklearn | `from sklearn.compose import ColumnTransformer` |
| **Transformers Parameter** | List of 3-element tuples `(name, transformer, columns)` | `[('imputer', SimpleImputer(), ['fever']), ...]` |
| **Remainder Strategy** | Handles untransformed features | `'drop'` (default - deletes unlisted features) or `'passthrough'` (retains untransformed features) |
| **Fit & Transform (Train)**| Learns parameters and transforms training data | `ct.fit_transform(X_train)` |
| **Transform Only (Test)** | Applies learned parameters without refitting (Prevents Data Leakage) | `ct.transform(X_test)` |

### Key Scikit-Learn Encoders & Imputers
- **SimpleImputer**: Fills missing values (`strategy='mean'`, `'median'`, etc.).
- **OneHotEncoder**: Nominal categorical columns, uses `drop='first'` to avoid multicollinearity / dummy variable trap.
- **OrdinalEncoder**: Ordered categorical columns, requires explicit order via `categories=[['Mild', 'Strong']]`.

## Flashcards

### Card 1
**Q:** ColumnTransformer ka main purpose kya hai?

**A:** Dataset ke alag-alag feature columns par unke types ke according alag-alag transformers (e.g., SimpleImputer, OneHotEncoder) ek saath apply karna.

### Card 2
**Q:** Traditional manual preprocessing ('Aam Zindagi') mein kya main drawbacks hain?

**A:** Code complexity, manual numpy array tracking, redundant code, aur train-test handling me Data Leakage ka high risk.

### Card 3
**Q:** ColumnTransformer ke `transformers` list parameter ka internal tuple structure kya hota hai?

**A:** Ek tuple me 3 elements hote hain: `(Name_string, Transformer_object, Columns_list)`.

### Card 4
**Q:** `remainder='drop'` parameter ka kya effect hota hai?

**A:** Ye un columns ko drop kar deta hai jin par transformer definition me koi rule apply nahi kiya gaya.

### Card 5
**Q:** `remainder='passthrough'` parameter kya karta hai?

**A:** Ye un un-transformed columns (jaise raw age) ko bina kisi change ke output array ke end mein pass/concatenate kar deta hai.

### Card 6
**Q:** Test dataset par `.fit_transform()` ki jagah `.transform()` kyun apply karna chahiye?

**A:** Test dataset par `.fit()` call karne se test data ki information distribution leaks ho sakti hai (Data Leakage). Test data par Hamesha sirf `.transform()` lagana chahiye.

### Card 7
**Q:** Scikit-Learn transformers (e.g., SimpleImputer) single column input ke liye `X_train[['fever']]` 2D DataFrame format kyun expect karte hain?

**A:** Scikit-Learn transformers input shape `(n_samples, n_features)` expect karte hain. Single bracket `X_train['fever']` 1D Series deta hai jo error throw karega.

### Card 8
**Q:** OneHotEncoder me `drop='first'` set karne ka main motive kya hai?

**A:** Dummy Variable Trap aur multicollinearity issue ko avoid karne ke liye.

### Card 9
**Q:** OrdinalEncoder me categories custom order me kaise assign ki jaati hain?

**A:** `categories` parameter mein list pass karke, jaise: `OrdinalEncoder(categories=[['Mild', 'Strong']])`.

### Card 10
**Q:** ColumnTransformer fit_transform karne ke baad kaun sa data-structure return karta hai?

**A:** A single, concatenated NumPy array.

### Card 11
**Q:** ColumnTransformer syntax mein Name parameter (e.g., 'tnf1') ka role kya hai?

**A:** Ye transformation step ka unique string identifier hota hai jo tracking aur debugging me help karta hai.

### Card 12
**Q:** Missing numerical values ko missing parameters (mean/median) se replace karne ke liye kaun se transformer ko call kiya jata hai?

**A:** `SimpleImputer` class from `sklearn.impute`.

### Card 13
**Q:** Agar DataFrame me Column Name case mismatch ho (e.g., 'Fever' vs 'fever'), toh kya error aayega?

**A:** Pandas KeyLookup error fail ho jata hai kyunki column strings case-sensitive hote hain.

### Card 14
**Q:** ColumnTransformer syntax me `passthrough` string values case-sensitive hoti hai ya nahi?

**A:** Haan, `remainder='passthrough'` lowercase string honi chahiye.

### Card 15
**Q:** Mean imputation formula kya hota hai?

**A:** Available non-null values ka average sum divided by count: \(\bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_i\).

## Quiz

#### Question 1: Manual preprocessing me multiple transformed feature arrays ko jodhne ke liye kaun sa numpy function use kiya jata hai?
- [0] np.append()
- [1] np.concatenate(..., axis=1)
- [2] np.vstack()
- [3] np.hstack()

#### Question 2: Scikit-Learn ke ColumnTransformer me `remainder` parameter ka default value kya hota hai?
- [0] 'passthrough'
- [1] 'drop'
- [2] None
- [3] 'ignore'

#### Question 3: ColumnTransformer object target features par transformers define karte waqt tuple order me lower order index index-0 par kya specify karta hai?
- [0] Transformer Object
- [1] Columns List
- [2] Transformer Custom Name String
- [3] Encoding Strategy

#### Question 4: Test dataset `X_test` par preprocessing execution ka correct Scikit-Learn syntax kya hai?
- [0] transformer.fit_transform(X_test)
- [1] transformer.fit(X_test)
- [2] transformer.transform(X_test)
- [3] transformer.predict(X_test)

#### Question 5: Agar user ne OrdinalEncoder scale `[['Mild', 'Strong']]` pass kiya hai, to 'Mild' kis integer me encode hoga?
- [0] 1
- [1] 0
- [2] -1
- [3] 2

#### Question 6: Agar 4 categories waale `city` column par `OneHotEncoder(drop='first', sparse=False)` lagaya jaye, to target output me kitni encoded columns banenge?
- [0] 4
- [1] 3
- [2] 2
- [3] 5

#### Question 7: Scikit-Learn Transformer me input single bracket `X_train['age']` dene par Python error kyun throw karta hai?
- [0] Ye 1D array/Series construct karta hai, whereas transformers 2D array expect karte hain.
- [1] Age column missing values treat nahi karta.
- [2] Pandas library error hoti hai.
- [3] ColumnTransformer integer accept nahi karta.

#### Question 8: Training dataset `X_train` par imputation / encoding rules Seekhne (learn) aur transform karne ke liye kaun sa method chalate hain?
- [0] .transform()
- [1] .fit()
- [2] .fit_transform()
- [3] .encode()

#### Question 9: ColumnTransformer execute karne ke baad operational output matrix ka format kya hota hai?
- [0] Pandas DataFrame
- [1] Python List of Lists
- [2] NumPy Array
- [3] Dictionary

#### Question 10: Data Leakage kab trigger hoti hai?
- [0] Jab remainder='passthrough' skip kar diya jata hai.
- [1] Jab Test Data par `.fit()` ya `.fit_transform()` method execution run kar di jaye.
- [2] Jab OneHotEncoder me drop='first' apply kiya jaye.
- [3] Jab DataFrame NumPy array convert hota hai.

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Columns-wise feature arrays ko horizontally join karne ke liye `np.concatenate(..., axis=1)` ka use kiya jata hai.
- **Q2 Answer:** Option 1 — Default value `'drop'` hoti hai, matlab unmentioned features final output array se remove ho jate hain jab tak passthrough set na kiya jaye.
- **Q3 Answer:** Option 2 — Tuple ka structure `(name, transformer, columns)` hota hai. Index 0 par identifier string 'name' aati hai.
- **Q4 Answer:** Option 2 — Data leakage se bachne ke liye `X_test` par hamesha sirf `.transform()` method chalaya jata hai.
- **Q5 Answer:** Option 1 — List index sequence index-0 se start hoti hai, isliye 'Mild' value 0 par mapping legi.
- **Q6 Answer:** Option 1 — Total 4 categories me se 1 drop ho jayegi (`drop='first'`), resulting in 3 columns.
- **Q7 Answer:** Option 0 — Scikit-learn features ko 2D structure `(n_samples, n_features)` me expect karta hai. Single bracket 1D Series deta hai.
- **Q8 Answer:** Option 2 — Training set par learning aur encoding dono ek saath perform karne ke liye `.fit_transform()` standard practice hai.
- **Q9 Answer:** Option 2 — ColumnTransformer processing completion ke baad baseline output ek 2D NumPy array return karta hai.
- **Q10 Answer:** Option 1 — Test data par fit/fit_transform call karne se test distribution parameters models seekh leta hai, causing Data Leakage.

## Interview Questions

### Q1: Why is ColumnTransformer preferred over manual feature engineering (e.g., transforming each column separately and concatenating arrays)?

**Answer:** Manual preprocessing (Aam Zindagi) mein har transformer outcome array ko track aur `np.concatenate` se match karna padta hai, jo bohot messy aur error-prone hai. ColumnTransformer ek single architecture layout me multiple transformers parallel apply kar deta hai, code brevity improve karta hai, pipelines me directly plug-in ho sakta hai, aur Train-Test Data Leakage ke risk ko baseline minimize karta hai.

### Q2: Explain the significance of `remainder='passthrough'` vs `remainder='drop'` in ColumnTransformer.

**Answer:** Default strategy `remainder='drop'` hoti hai, jo operational tuple rules mein undefined features/columns ko final output NumPy array se permanently delete/drop kar deti hai. Non-transformed columns (jaise untouched raw numerical features) ko safely represent karne aur pipeline final matrix me retain karne ke liye explicitly `remainder='passthrough'` declare kiya jata hai.

### Q3: How does ColumnTransformer prevent Data Leakage between Train and Test sets?

**Answer:** ColumnTransformer parameters fit structure apply karte waqt single `.fit_transform(X_train)` execute hota hai. Is se imputation values (e.g., mean) ya category maps strictly `X_train` se calculate hote hain. Test set par sirf `.transform(X_test)` execute karke previous parameters re-use kiye jaate hain, test dataset statistics ka zero leakage ensure karke.

### Q4: What is the difference between OneHotEncoder and OrdinalEncoder, and how do you configure them inside a ColumnTransformer?

**Answer:** OneHotEncoder nominal categories (jinka koi internal order nahi hota, like Gender or City) ke liye discrete binary columns create karta hai (using `drop='first'` to prevent multicollinearity). OrdinalEncoder ordered categories (like Low/Medium/High ya Mild/Strong) ko ranked numbers (0, 1, 2) me convert karta hai jahan sequence define karne ke liye `categories=[['Mild', 'Strong']]` passed variable mandatory hai.

### Q5: What happens if a new un-encoded category appears in the test dataset during `transformer.transform(X_test)` for OneHotEncoder?

**Answer:** By default, OneHotEncoder `ValueError` raise kar dega kyunki test set me unseen category fit step par present nahi thi. Real-world machine learning systems me issue resolve karne ke liye OneHotEncoder me `handle_unknown='ignore'` set karte hain (jisse unexpected categories transformation ke time zero vector me default encode ho jaati hain).
