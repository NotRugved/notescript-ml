# Revision Pack: What are Outliers | Outliers in Machine Learning

**One-Line Summary:** Decision Trees use greedy splitting based on Gini Impurity or Entropy to classify data, but require pruning to prevent overfitting.

## Cheat Sheet

| Concept | Formula/Key Point | Intuition |
| :--- | :--- | :--- |
| **Gini Impurity** | `1 - Σ(p_i)^2` | Box of colored balls. 0 = Pure (all same color), 1 = Max Impurity. |
| **Entropy** | `-Σ(p_i * log2(p_i))` | Uncertainty. 0 = Certain, Max = 50-50 doubt. |
| **Information Gain** | `Entropy(parent) - Weighted Entropy(children)` | How much uncertainty a split removes. Higher is better. |
| **Tree Structure** | Root -> Internal Nodes (Splits) -> Leaf Nodes (Prediction) | Like asking Yes/No questions to identify an object. |
| **Overfitting Fix** | `max_depth`, `min_samples_split`, `min_samples_leaf` | Don't memorize practice questions (training); learn concepts (generalization). |
| **Sklearn Params** | `criterion='gini'` or `'entropy'` | Choose the impurity measure for splitting. |
| **Pros** | Interpretable, handles non-linear, no feature scaling needed. | Easy to visualize and explain. |
| **Cons** | Unstable, prone to overfitting, greedy (not globally optimal). | Small data change can change the whole tree. |

## Flashcards

### Card 1
**Q:** Decision Tree ka structure kaisa hota hai?

**A:** Root node, internal nodes (jo split karte hain), aur leaf nodes (jo final prediction dete hain).

### Card 2
**Q:** Gini Impurity ka formula kya hai?

**A:** Gini = 1 - Σ(p_i)^2, jahan p_i class i ki probability hai.

### Card 3
**Q:** Entropy ka formula kya hai?

**A:** Entropy = -Σ(p_i * log2(p_i)).

### Card 4
**Q:** Information Gain kaise calculate hota hai?

**A:** Entropy(parent) minus weighted sum of Entropy(children). Yeh batata hai split ne kitni uncertainty kam ki.

### Card 5
**Q:** Decision Tree greedy approach kyun follow karta hai?

**A:** Kyunki yeh har step par locally best split choose karta hai jo impurity ko sabse zyada kam kare, globally optimal solution nahi dhundhta.

### Card 6
**Q:** Overfitting ko rokne ke liye kaunse parameters use karte hain?

**A:** max_depth, min_samples_split, aur min_samples_leaf.

### Card 7
**Q:** Sklearn mein Decision Tree visualize karne ke liye kaunsa function use hota hai?

**A:** plot_tree() function.

### Card 8
**Q:** Gini Impurity 0 hone ka matlab kya hai?

**A:** Node 'pure' hai, matlab saare samples ek hi class ke hain.

### Card 9
**Q:** Decision Tree numerical aur categorical features dono handle kar sakta hai?

**A:** Haan, lekin sklearn mein categorical features ko numeric encode karna padta hai (One-hot/Label encoding).

### Card 10
**Q:** Feature Importance kaise measure hota hai?

**A:** Har feature ke liye Gini impurity reduction ko sum karke.

### Card 11
**Q:** Pre-pruning aur Post-pruning mein kya difference hai?

**A:** Pre-pruning tree banate waqt limits lagata hai (jaise max_depth), Post-pruning banne ke baad tree ko chhota karta hai.

### Card 12
**Q:** Decision Tree ka ek major disadvantage kya hai?

**A:** Unstable hai - chhota sa data change se poora tree badal sakta hai.

### Card 13
**Q:** Iris dataset par Decision Tree banane ke liye pehle kya karna chahiye?

**A:** Data ko load karna aur train/test split karna (train_test_split).

### Card 14
**Q:** criterion parameter mein 'gini' aur 'entropy' ka kya role hai?

**A:** Yeh decide karta hai ki split karte waqt kaunsa impurity measure use karna hai.

### Card 15
**Q:** Agar tree bahut deep ho jaye toh kya hota hai?

**A:** Overfitting hoti hai, model training data par 100% accuracy de sakta hai lekin test data par fail ho jata hai.

## Quiz

#### Question 1: Gini Impurity formula mein agar saare samples ek hi class ke hain, toh value kya hogi?
- [0] 1
- [1] 0
- [2] 0.5
- [3] Infinity

#### Question 2: Decision Tree building process kaisi hoti hai?
- [0] Iterative
- [1] Recursive
- [2] Random
- [3] Linear

#### Question 3: Information Gain maximize karna kaunsa split choose karta hai?
- [0] Woh jo sabse zyada data ko split kare
- [1] Woh jo entropy ko sabse zyada kam kare
- [2] Woh jo sabse zyada features use kare
- [3] Woh jo sabse deep ho

#### Question 4: Sklearn mein DecisionTreeClassifier ke liye default criterion kya hota hai?
- [0] entropy
- [1] gini
- [2] log_loss
- [3] mse

#### Question 5: Overfitting ko kam karne ke liye kaunsa parameter set karna chahiye?
- [0] min_samples_leaf
- [1] max_features
- [2] n_estimators
- [3] learning_rate

#### Question 6: Decision Tree kaunsa type of learning algorithm hai?
- [0] Unsupervised
- [1] Supervised
- [2] Reinforcement
- [3] Semi-supervised

#### Question 7: Feature Importance kaise calculate hota hai?
- [0] Correlation se
- [1] Gini impurity reduction se
- [2] Covariance se
- [3] Variance se

#### Question 8: Decision Tree ka ek major disadvantage kya hai?
- [0] Slow training
- [1] Unstable to small data changes
- [2] Cannot handle categorical data
- [3] Requires feature scaling

#### Question 9: Entropy 0 hone ka matlab kya hai?
- [0] Maximum uncertainty
- [1] No uncertainty (Pure node)
- [2] 50-50 split
- [3] Invalid data

#### Question 10: Tree ko visualize karne ke liye kaunsa function use hota hai?
- [0] plot_tree()
- [1] draw_tree()
- [2] show_tree()
- [3] visualize_tree()

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Agar p_i = 1 hai, toh 1 - (1)^2 = 0. Pure node ka Gini 0 hota hai.
- **Q2 Answer:** Option 1 — Tree banane ka process recursive hai; har node par best split dhundh kar data ko do hisson mein baanta jata hai.
- **Q3 Answer:** Option 1 — Information Gain batata hai ki split ne kitni uncertainty (entropy) kam ki. Higher IG = better split.
- **Q4 Answer:** Option 1 — Sklearn mein default criterion 'gini' hota hai, lekin 'entropy' bhi use kiya ja sakta hai.
- **Q5 Answer:** Option 0 — min_samples_leaf ensure karta hai ki leaf node mein kam se kam itne samples hon, jisse tree bahut deep nahi hota.
- **Q6 Answer:** Option 1 — Decision Tree supervised learning algorithm hai kyunki yeh labeled data se seekhta hai.
- **Q7 Answer:** Option 1 — Feature importance har feature ke liye total Gini impurity reduction ko sum karke calculate hota hai.
- **Q8 Answer:** Option 1 — Decision Trees unstable hote hain; training data mein chhota sa change poore tree structure ko badal sakta hai.
- **Q9 Answer:** Option 1 — Entropy 0 hota hai jab prediction 100% certain ho, matlab node pure hai.
- **Q10 Answer:** Option 0 — Sklearn mein plot_tree() function use hota hai decision tree ko visualize karne ke liye.

## Interview Questions

### Q1: Decision Tree mein Gini Impurity aur Entropy mein kya difference hai?

**Answer:** Dono impurity measure hain. Gini Impurity (1 - Σp^2) computationally sasta hai aur zyada use hota hai. Entropy (-Σp*log2(p)) information theory par based hai aur uncertainty ko measure karta hai. Gini zyada commonly used hai kyunki yeh faster hai, lekin dono similar results dete hain.

### Q2: Decision Tree overfitting kyun karta hai aur ise kaise rok sakte hain?

**Answer:** Decision Tree greedy approach follow karta hai aur jab tak pure nodes na ban jaye, split karta rehta hai. Isse woh training data ko memorize kar leta hai (overfitting). Ise rokne ke liye pre-pruning (max_depth, min_samples_split, min_samples_leaf) ya post-pruning (cost complexity pruning) use karte hain.

### Q3: Decision Tree numerical aur categorical features dono handle kar sakta hai? Kaise?

**Answer:** Haan, theoretically dono handle kar sakta hai. Numerical features ke liye threshold based splits (e.g., age > 30) use hote hain. Categorical features ke liye multi-way splits ho sakte hain. Lekin sklearn mein categorical features ko numeric encode karna padta hai (One-hot encoding ya Label encoding) kyunki sklearn numeric input expect karta hai.

### Q4: Decision Tree ka greedy approach globally optimal solution kyun nahi deta?

**Answer:** Greedy approach har step par locally best split choose karta hai jo current node ki impurity ko sabse zyada kam kare. Yeh future splits ko consider nahi karta. Isliye, yeh globally optimal tree (jo overall impurity ko minimize kare) nahi dhundhta, sirf locally best path follow karta hai.

### Q5: Decision Tree kaunse scenarios mein best perform karta hai aur kaunse mein nahi?

**Answer:** Best: Jab data non-linear relationships rakhta hai, feature engineering ki zaroorat nahi hai, aur interpretability important hai. Not Best: Jab data mein bahut zyada noise hai (overfitting risk), features bahut zyada hain (high dimensionality), ya model stability chahiye (Random Forests better hote hain).
