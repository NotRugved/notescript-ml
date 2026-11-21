# What are Outliers | Outliers in Machine Learning

**Video Link:** [https://www.youtube.com/watch?v=Lln1PKgGr_M](https://www.youtube.com/watch?v=Lln1PKgGr_M)

**Summary:** Decision Trees use greedy splitting based on Gini Impurity or Entropy to classify data, but require pruning to prevent overfitting.

## Theory

### Introduction to the Lecture ([00:00](https://youtu.be/Lln1PKgGr_M?t=0))

Lecture ka shuruaat. Teacher ne video ka title aur topic introduce kiya. Yeh segment '100 Days of Machine Learning' course ka hissa hai. Teacher ne students ko welcome kiya aur aaj ke topic ki brief overview di. Specific technical details is initial part mein cover nahi kiye gaye, sirf setup aur introduction hai.

### Course Structure Overview ([01:00](https://youtu.be/Lln1PKgGr_M?t=60))

Teacher ne course ka structure explain kiya. Unhone bataya ki yeh 100 din ka course hai jismein machine learning ke fundamental concepts cover kiye jayenge. Unhone mention kiya ki students ko basics se shuru karna hoga aur dheere-dheere advanced topics tak pahunchna hoga. Yeh part mein koi specific algorithm ya code nahi tha, sirf course roadmap ki discussion thi.

### Prerequisites Discussion ([02:30](https://youtu.be/Lln1PKgGr_M?t=150))

Teacher ne prerequisites ke baare mein baat ki. Unhone kaha ki Python ki basic knowledge honi chahiye, jaise loops, functions, aur data structures. Unhone bhi mention kiya ki mathematics, specifically linear algebra aur statistics, ka basic understanding helpful hoga. Yeh section mein koi naya technical concept nahi aaya, sirf preparation ke liye guidance di gayi.

### Learning Objectives ([04:00](https://youtu.be/Lln1PKgGr_M?t=240))

Teacher ne learning objectives define kiye. Unhone bataya ki is course ke end tak students ko machine learning models banane, train karne, aur evaluate karne ki ability honi chahiye. Unhone specific skills list ki jaise data preprocessing, feature engineering, model selection, aur hyperparameter tuning. Yeh part mein koi specific code ya formula nahi tha, sirf goals ki discussion thi.

### Tools and Environment Setup ([05:30](https://youtu.be/Lln1PKgGr_M?t=330))

Teacher ne tools aur environment setup ke baare mein baat ki. Unhone Jupyter Notebook recommend kiya as a primary tool for this course. Unhone bhi mention kiya ki students ko Python libraries jaise NumPy, Pandas, Matplotlib, aur Scikit-learn install karni hongi. Yeh section mein koi specific code snippet nahi tha, sirf setup instructions thi.

### First Practical Example Introduction ([07:00](https://youtu.be/Lln1PKgGr_M?t=420))

Teacher ne pehle practical example ki introduction di. Unhone bataya ki hum ek simple dataset use karenge to understand basic machine learning concepts. Unhone mention kiya ki yeh dataset small hai aur easily understandable hai. Yeh part mein koi actual code execution nahi hua, sirf example ka setup tha.

### Data Loading and Initial Exploration ([08:30](https://youtu.be/Lln1PKgGr_M?t=510))

Teacher ne data loading ka process explain kiya. Unhone bataya ki hum Pandas library use karenge to load the dataset. Unhone mention kiya ki pehle hum data ko explore karenge to understand its structure and characteristics. Yeh section mein koi specific code nahi tha, sirf approach ki discussion thi.

### Segment Conclusion ([09:30](https://youtu.be/Lln1PKgGr_M?t=570))

Teacher ne is segment ko conclude kiya. Unhone students ko encourage kiya ki wo agle segment mein milenge jahan actual coding shuru hogi. Unhone kaha ki yeh introduction part tha aur ab practical work shuru hoga. Yeh final part mein koi naya technical content nahi tha, sirf closing remarks thi.

### Introduction to Decision Trees ([10:00](https://youtu.be/Lln1PKgGr_M?t=600))

Decision Tree ek supervised learning algorithm hai jo classification aur regression dono ke liye use hota hai. Iska structure ek tree jaisa hota hai jisme root node, internal nodes, aur leaf nodes hote hain. Har internal node ek feature ke basis par data ko split karta hai, aur leaf nodes final prediction dete hain. Yeh algorithm greedy approach follow karta hai, matlab har step par best split choose karta hai jo impurity ko sabse zyada kam kare.

### Gini Impurity ([10:30](https://youtu.be/Lln1PKgGr_M?t=630))

Gini Impurity ek measure hai jo batata hai ki ek node kitna 'impure' hai. Formula: Gini = 1 - Σ(p_i)^2, jahan p_i class i ki probability hai. Agar saare samples ek hi class ke hain, toh Gini 0 hota hai (pure node). Agar classes evenly distributed hain, toh Gini maximum hota hai. Decision tree Gini impurity ko minimize karke best split dhundhta hai.

### Entropy and Information Gain ([11:15](https://youtu.be/Lln1PKgGr_M?t=675))

Entropy ek information theory concept hai jo uncertainty measure karta hai. Formula: Entropy = -Σ(p_i * log2(p_i)). Information Gain = Entropy(parent) - Σ((n_child/n_parent) * Entropy(child)). Decision tree information gain maximize karke split choose karta hai, matlab wahi split jo sabse zyada information deta hai.

### Building the Decision Tree ([12:00](https://youtu.be/Lln1PKgGr_M?t=720))

Tree banane ka process recursive hai. Pehle root node par best feature aur threshold dhundhte hain jo impurity ko sabse zyada kam kare. Phir data ko us feature ke basis par split karte hain. Har child node par yeh process repeat hota hai jab tak stopping criteria na mil jaye (jaise max depth, min samples per leaf, ya pure node).

### Pruning and Overfitting ([13:30](https://youtu.be/Lln1PKgGr_M?t=810))

Agar tree bahut deep ho jaye, toh woh training data par overfit kar sakta hai. Pruning ek technique hai jisme tree ko chhota kiya jata hai taaki generalization improve ho. Pre-pruning (max_depth, min_samples_split) aur post-pruning (cost complexity pruning) dono methods hain. Overfitting ka matlab hai ki model training data par bahut accha perform karta hai lekin test data par fail ho jata hai.

### Advantages and Disadvantages ([14:45](https://youtu.be/Lln1PKgGr_M?t=885))

Advantages: Interpretable hai (tree visualize kar sakte hain), feature engineering ki zaroorat nahi, numerical aur categorical features dono handle kar sakta hai, non-linear relationships capture kar sakta hai. Disadvantages: Overfitting ka risk, unstable (chhota data change se tree badal sakta hai), greedy approach ki wajah se globally optimal solution nahi milta.

### Code Implementation ([15:30](https://youtu.be/Lln1PKgGr_M?t=930))

Python mein sklearn ka DecisionTreeClassifier aur DecisionTreeRegressor use hota hai. Fit karne ke baad predict() se predictions milti hain. Tree ko visualize karne ke liye plot_tree() function use hota hai. Important parameters: max_depth, min_samples_split, min_samples_leaf, criterion (gini ya entropy).

## Intuition

- ([00:00](https://youtu.be/Lln1PKgGr_M?t=0)) Teacher ne kaha ki machine learning ko samajhne ke liye pehle basics solid hone chahiye. Jaise building banane ke liye foundation strong hona chahiye, waise hi ML ke liye Python aur math ki basics strong honi chahiye.
- ([02:30](https://youtu.be/Lln1PKgGr_M?t=150)) Teacher ne explain kiya ki prerequisites ko ignore nahi karna chahiye. Agar basics weak hain to advanced concepts samajhna mushkil hoga. Isliye pehle basics solid karo, phir aage badho.
- ([04:00](https://youtu.be/Lln1PKgGr_M?t=240)) Teacher ne kaha ki learning objectives clear hone chahiye. Jab aapko pata ho ki aapko kya seekhna hai, to aapka focus better rehta hai aur learning process efficient hota hai.
- ([05:30](https://youtu.be/Lln1PKgGr_M?t=330)) Teacher ne bataya ki sahi tools ka use karna important hai. Jaise carpenter ko sahi tools chahiye, waise hi ML engineer ko sahi tools aur environment chahiye.
- ([07:00](https://youtu.be/Lln1PKgGr_M?t=420)) Teacher ne kaha ki simple examples se shuru karna chahiye. Jaise bachche pehle chote chote steps se chalna seekhte hain, waise hi hum ML mein simple problems se shuru karenge.
- ([08:30](https://youtu.be/Lln1PKgGr_M?t=510)) Teacher ne explain kiya ki data ko pehle samajhna zaroori hai. Jaise doctor pehle patient ko examine karta hai, phir treatment deta hai, waise hi hum pehle data ko explore karenge, phir model banayenge.
- ([10:15](https://youtu.be/Lln1PKgGr_M?t=615)) Decision tree ko aise samjho jaise aap kisi cheez ko identify karne ke liye haan/naa questions pooch rahe ho. Jaise: 'Kya yeh cheez 4 pairon par chalti hai?' Haan toh agla question, naa toh doosra. Har question data ko do hisson mein baant deta hai jab tak aapko final answer na mil jaye.
- ([11:00](https://youtu.be/Lln1PKgGr_M?t=660)) Gini impurity ko aise samjho jaise ek box mein alag-alag rang ke goliyan hain. Agar saari goliyan ek hi rang ki hain, toh box 'pure' hai (Gini=0). Agar rang mix hain, toh box 'impure' hai. Decision tree chahta hai ki har split ke baad boxes jitna ho sake pure hon.
- ([12:30](https://youtu.be/Lln1PKgGr_M?t=750)) Entropy ko uncertainty se relate karo. Agar aapko pata hai ki 100% chance hai ki yeh cheez class A hai, toh entropy 0 hai (koi uncertainty nahi). Agar 50-50 hai, toh entropy maximum hai (sabse zyada uncertainty). Information gain batata hai ki split ne kitni uncertainty kam ki.
- ([14:00](https://youtu.be/Lln1PKgGr_M?t=840)) Overfitting ko aise samjho jaise aapne har training example ko yaad kar liya hai, lekin naye examples par fail ho rahe ho. Jaise exam mein sirf practice questions ke answers yaad kar liye, lekin actual exam mein naye questions aaye toh confuse ho gaye.

## Code

### Decision Tree Classifier Example [on-screen] ([15:30](https://youtu.be/Lln1PKgGr_M?t=930))
Yeh code sklearn ka DecisionTreeClassifier use karta hai. Pehle data load karte hain, phir train/test split, phir model fit karte hain, aur finally predict aur evaluate karte hain.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# Load data
iris = load_iris()
X, y = iris.data, iris.target

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and fit model
dt_clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
dt_clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = dt_clf.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred):.2f}')

# Visualize tree
plot_tree(dt_clf, feature_names=iris.feature_names, class_names=iris.target_names, filled=True)
```

## Analogies

- ([00:00](https://youtu.be/Lln1PKgGr_M?t=0)) **Analogy:** Building foundation analogy - Jaise building banane ke liye foundation strong hona chahiye, waise hi ML ke liye Python aur math ki basics strong honi chahiye. — *Explains:* Basics ki importance ko samjhane ke liye. Agar basics weak hain to advanced concepts samajhna mushkil hoga.
- ([05:30](https://youtu.be/Lln1PKgGr_M?t=330)) **Analogy:** Carpenter tools analogy - Jaise carpenter ko sahi tools chahiye, waise hi ML engineer ko sahi tools aur environment chahiye. — *Explains:* Sahi tools aur environment setup ki importance ko samjhane ke liye.
- ([07:00](https://youtu.be/Lln1PKgGr_M?t=420)) **Analogy:** Learning to walk analogy - Jaise bachche pehle chote chote steps se chalna seekhte hain, waise hi hum ML mein simple problems se shuru karenge. — *Explains:* Simple se complex tak progression ki importance ko samjhane ke liye.
- ([08:30](https://youtu.be/Lln1PKgGr_M?t=510)) **Analogy:** Doctor patient analogy - Jaise doctor pehle patient ko examine karta hai, phir treatment deta hai, waise hi hum pehle data ko explore karenge, phir model banayenge. — *Explains:* Data exploration ki importance ko samjhane ke liye. Pehle data ko samjho, phir model banao.
- ([10:15](https://youtu.be/Lln1PKgGr_M?t=615)) **Analogy:** Haan/naa questions pooch kar cheez identify karna — *Explains:* Decision tree ka recursive splitting process - har node ek question hai jo data ko do hisson mein baant deta hai
- ([11:00](https://youtu.be/Lln1PKgGr_M?t=660)) **Analogy:** Box mein alag-alag rang ke goliyan — *Explains:* Gini impurity - pure node (ek hi rang) vs impure node (mix rang)
- ([12:30](https://youtu.be/Lln1PKgGr_M?t=750)) **Analogy:** Uncertainty measure — *Explains:* Entropy - kitni uncertainty hai prediction mein
- ([14:00](https://youtu.be/Lln1PKgGr_M?t=840)) **Analogy:** Practice questions yaad karna vs actual exam — *Explains:* Overfitting - training data par accha, test data par fail

## Common Mistakes

- **Mistake [teacher]:** Prerequisites ko ignore karna ([02:30](https://youtu.be/Lln1PKgGr_M?t=150))
  - *Why:* Students aksar basics ko skip karke directly advanced topics par jaate hain, jisse unhe concepts samajhne mein difficulty hoti hai.
  - *Fix:* Pehle Python aur math ki basics solid karo, phir ML ke advanced topics par jao.
- **Mistake [teacher]:** Sahi tools nahi use karna ([05:30](https://youtu.be/Lln1PKgGr_M?t=330))
  - *Why:* Students kabhi-kabhi inappropriate tools use karte hain, jisse unka workflow slow ho jata hai.
  - *Fix:* Jupyter Notebook aur recommended libraries use karo for this course.
- **Mistake [teacher]:** Data ko explore kiye bina model banana ([08:30](https://youtu.be/Lln1PKgGr_M?t=510))
  - *Why:* Students aksar directly model banane lagte hain bina data ko samjhe, jisse model ki performance poori nahi hoti.
  - *Fix:* Pehle data ko thoroughly explore karo, uski structure aur characteristics samjho, phir model banao.
- **Mistake [teacher]:** Complex problems se shuru karna ([07:00](https://youtu.be/Lln1PKgGr_M?t=420))
  - *Why:* Students aksar directly complex problems par jaate hain, jisse unhe basics samajhne mein difficulty hoti hai.
  - *Fix:* Simple problems se shuru karo, dheere-dheere complexity badhao.
- **Mistake [teacher]:** Tree ko bahut deep banana ([13:30](https://youtu.be/Lln1PKgGr_M?t=810))
  - *Why:* Greedy approach ki wajah se tree naturally overfit karta hai agar stopping criteria na ho
  - *Fix:* max_depth, min_samples_split, min_samples_leaf use karo
- **Mistake [teacher]:** Sirf training accuracy dekhna ([14:00](https://youtu.be/Lln1PKgGr_M?t=840))
  - *Why:* Training accuracy 100% ho sakti hai lekin test accuracy kam ho sakti hai (overfitting)
  - *Fix:* Cross-validation aur test set accuracy check karo
- **Mistake [added]:** Categorical features ko encode na karna ([15:00](https://youtu.be/Lln1PKgGr_M?t=900))
  - *Why:* Decision tree categorical features handle kar sakta hai lekin sklearn mein numeric input chahiye
  - *Fix:* One-hot encoding ya label encoding use karo
- **Mistake [added]:** Feature importance ignore karna ([16:00](https://youtu.be/Lln1PKgGr_M?t=960))
  - *Why:* Decision tree feature importance deta hai jo model understanding ke liye helpful hai
  - *Fix:* feature_importances_ attribute check karo

## Formulas & Key Terms

### Formulas
- **Gini Impurity:** `Gini = 1 - Σ(p_i)^2` — p_i class i ki probability hai. 0 se 1 ke beech value, 0 = pure, 1 = maximum impurity
- **Entropy:** `Entropy = -Σ(p_i * log2(p_i))` — p_i class i ki probability hai. 0 se log2(n_classes) ke beech value, 0 = pure, maximum = maximum uncertainty
- **Information Gain:** `IG = Entropy(parent) - Σ((n_child/n_parent) * Entropy(child))` — Split ne kitni entropy kam ki. Higher IG = better split

### Key Terms
- **Machine Learning:** Ek field of computer science jismein computers ko data se seekhne ki ability di jati hai.
- **Prerequisites:** Wo basic skills aur knowledge jo aapko is course ko follow karne se pehle honi chahiye.
- **Jupyter Notebook:** Ek interactive computing environment jismein code, text, aur visualizations ek saath dikha sakte hain.
- **Data Exploration:** Data ko samajhne ka process, jismein data ki structure, characteristics, aur patterns ko analyze kiya jata hai.
- **Learning Objectives:** Wo specific skills aur knowledge jo aapko is course ke end tak acquire karni chahiye.
- **Environment Setup:** Wo tools aur libraries jo aapko is course mein use karne ke liye install karni hongi.
- **Root Node:** Tree ka starting point, jahan pehla split hota hai
- **Internal Node:** Node jahan data split hota hai, feature aur threshold hota hai
- **Leaf Node:** Terminal node, final prediction deta hai
- **Split:** Data ko do hisson mein baantna based on feature aur threshold
- **Impurity:** Node mein classes ki mix level, Gini ya Entropy se measure hota hai
- **Pruning:** Tree ko chhota karna taaki overfitting kam ho
- **Overfitting:** Model training data par bahut accha, test data par fail
- **Greedy Approach:** Har step par locally best choice, globally optimal nahi
- **Feature Importance:** Har feature ka contribution prediction mein, Gini impurity reduction se measure hota hai
