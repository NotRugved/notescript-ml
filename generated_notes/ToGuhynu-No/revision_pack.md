# Revision Pack: Curse of Dimensionality

**One-Line Summary:** Machine Learning ke core concepts, algorithms, bias-variance tradeoff, regularization, aur model evaluation ko samajhkar real-world problems solve karo.

## Cheat Sheet

### Cheat Sheet

| Concept | Key Points | Example Algorithms |
|---|---|---|
| Supervised Learning | Labeled data, predict target | Linear Regression, Logistic Regression, SVM, Decision Trees |
| Unsupervised Learning | No labels, find structure | K-Means, PCA, DBSCAN |
| Regression | Continuous output, loss = MSE | Linear Regression, Ridge, Lasso |
| Classification | Discrete classes, loss = Cross-Entropy | Logistic Regression, SVM, Random Forest |
| Bias-Variance Tradeoff | High bias = underfit, high variance = overfit | Model complexity, regularization |
| Regularization | Penalize large weights, reduce overfitting | L1 (Lasso), L2 (Ridge), Elastic Net |
| Gradient Descent | Iterative optimization, learning rate crucial | Batch GD, Stochastic GD, Mini-batch GD |
| Cross-Validation | Reliable performance estimate, avoid data leakage | k-Fold CV, Stratified CV |
| Ensemble Methods | Combine weak learners, improve accuracy | Bagging, Boosting (AdaBoost, XGBoost), Stacking |
| Neural Networks | Layers of neurons, backpropagation | MLP, CNN, RNN |
| Evaluation Metrics | Choose metric per task | RMSE, Accuracy, Precision, Recall, F1, ROC-AUC |
| Feature Engineering | Transform raw data to useful features | Scaling, Encoding, Polynomial features |
| Hyperparameter Tuning | Optimize model settings | Grid Search, Random Search, Bayesian Opt |
| Model Deployment | Serve model in production | REST API, Docker, CI/CD |

## Flashcards

### Card 1
**Q:** Supervised learning ka main requirement kya hota hai?

**A:** Labeled training data jisme input-output pairs hote hain.

### Card 2
**Q:** Bias-variance tradeoff ka matlab samjhao.

**A:** Model complexity increase se bias kam hota hai par variance badhta hai; balance karna zaroori hai.

### Card 3
**Q:** L1 regularization kya karta hai?

**A:** Weights ki absolute values ko penalize karta hai, sparsity (feature selection) promote karta hai.

### Card 4
**Q:** k-Fold cross-validation me data ko kaise split kiya jata hai?

**A:** Data ko k equal folds me divide karte hain, har fold ek baar test set aur baaki training set bante hain.

### Card 5
**Q:** Decision tree me impurity measure ka use hota hai?

**A:** Gini impurity ya Entropy se best split decide ki jati hai.

### Card 6
**Q:** Gradient descent me learning rate ka effect kya hota hai?

**A:** Bahut high se overshoot, bahut low se slow convergence.

### Card 7
**Q:** Bagging ka main advantage kya hai?

**A:** Variance reduce hota hai by training multiple models on bootstrapped samples.

### Card 8
**Q:** ROC-AUC metric kis scenario me useful hai?

**A:** Imbalanced classification problems me model ki ranking ability evaluate karta hai.

### Card 9
**Q:** PCA ka primary goal kya hota hai?

**A:** High-dimensional data ko lower dimensions me project karna while maximum variance retain karna.

### Card 10
**Q:** Overfitting ko kaise detect kar sakte hain?

**A:** Training accuracy high but validation/test accuracy low ho to overfitting hota hai.

### Card 11
**Q:** Stochastic Gradient Descent (SGD) me batch size kya hota hai?

**A:** Ek iteration me ek sample use hota hai weight update ke liye.

### Card 12
**Q:** AdaBoost me weak learners ko kaise combine karte hain?

**A:** Har iteration me misclassified samples ko higher weight dete hain, final prediction weighted vote hota hai.

### Card 13
**Q:** Feature scaling ka importance kya hai?

**A:** Algorithms jo distance ya gradient use karte hain unki convergence aur performance improve hoti hai.

### Card 14
**Q:** What is the difference between precision and recall?

**A:** Precision = TP/(TP+FP) (false positives ko penalize), Recall = TP/(TP+FN) (false negatives ko penalize).

### Card 15
**Q:** Neural network me backpropagation ka role kya hai?

**A:** Loss gradient ko layers ke through propagate karke weights update karta hai.

## Quiz

#### Question 1: Which algorithm is primarily used for dimensionality reduction?
- [0] K-Means
- [1] PCA
- [2] Logistic Regression
- [3] Random Forest

#### Question 2: In a binary classification problem, which metric is best when false negatives are very costly?
- [0] Accuracy
- [1] Precision
- [2] Recall
- [3] F1-Score

#### Question 3: What does L2 regularization penalize?
- [0] Sum of absolute weights
- [1] Sum of squared weights
- [2] Number of features
- [3] Depth of tree

#### Question 4: Which cross-validation technique ensures class distribution is preserved in each fold?
- [0] k-Fold CV
- [1] Leave-One-Out CV
- [2] Stratified k-Fold CV
- [3] Monte Carlo CV

#### Question 5: In Gradient Descent, if the learning rate is set too high, what typically happens?
- [0] Converges faster
- [1] Oscillates or diverges
- [2] Stops after one iteration
- [3] Finds global optimum

#### Question 6: Which ensemble method reduces bias more than variance?
- [0] Bagging
- [1] Boosting
- [2] Stacking
- [3] Voting

#### Question 7: What is the main purpose of the activation function in a neural network?
- [0] Initialize weights
- [1] Introduce non-linearity
- [2] Compute loss
- [3] Perform backpropagation

#### Question 8: Which loss function is appropriate for multi-class classification?
- [0] Mean Squared Error
- [1] Hinge Loss
- [2] Cross-Entropy Loss
- [3] Huber Loss

#### Question 9: What does the term 'underfitting' indicate?
- [0] Model performs well on training data
- [1] Model captures noise
- [2] Model is too simple to learn patterns
- [3] Model has high variance

#### Question 10: Which hyperparameter tuning method evaluates a random subset of the search space?
- [0] Grid Search
- [1] Random Search
- [2] Bayesian Optimization
- [3] Manual Tuning

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — PCA (Principal Component Analysis) data ke variance ko maximize karte hue dimensions reduce karta hai.
- **Q2 Answer:** Option 2 — Recall focuses on capturing all actual positives, minimizing false negatives.
- **Q3 Answer:** Option 1 — L2 adds the sum of squared weight values to the loss, encouraging smaller weights.
- **Q4 Answer:** Option 2 — Stratified k-Fold maintains the same proportion of classes in every fold.
- **Q5 Answer:** Option 1 — A high learning rate can cause the updates to overshoot the minimum, leading to divergence.
- **Q6 Answer:** Option 1 — Boosting sequentially focuses on errors, reducing bias by creating strong learners.
- **Q7 Answer:** Option 1 — Activation functions allow the network to learn complex, non-linear relationships.
- **Q8 Answer:** Option 2 — Cross-Entropy (softmax) measures the difference between predicted probability distribution and true labels.
- **Q9 Answer:** Option 2 — Underfitting occurs when the model is too simple, leading to poor performance on both training and test data.
- **Q10 Answer:** Option 1 — Random Search samples random combinations, often more efficient than exhaustive Grid Search.

## Interview Questions

### Q1: Explain the bias-variance tradeoff with a practical example.

**Answer:** Bias-variance tradeoff model ki complexity aur data fit ke beech ka balance hai. High bias (underfit) models simple hote hain, jaise linear regression on non-linear data, jisse training aur test error dono high hote hain. High variance (overfit) models complex hote hain, jaise deep decision tree, jo training data ko perfectly fit kar leta hai (low training error) lekin unseen data pe performance gir jati hai (high test error). Practical example: Housing price prediction me simple linear model may miss interactions (high bias), while a deep tree may memorize outliers (high variance). Regularization, cross-validation, aur appropriate model selection se is tradeoff ko manage karte hain.

### Q2: What is regularization and how do L1 and L2 differ in effect?

**Answer:** Regularization loss function me ek penalty term add karta hai jo large weights ko discourage karta hai, isse overfitting kam hota hai. L1 (Lasso) penalty absolute weight values ka sum hota hai, jo kuch weights ko zero kar deta hai, isse feature selection hoti hai. L2 (Ridge) penalty squared weight values ka sum hota hai, jo sab weights ko chhota karta hai lekin zero nahi karta, isse model smooth hota hai. Elastic Net dono penalties ka combination hota hai.

### Q3: Describe how Gradient Descent works and the differences between Batch, Stochastic, and Mini-batch variants.

**Answer:** Gradient Descent loss function ka gradient compute karke weights ko opposite direction me move karta hai: w = w - lr * gradient. Batch GD poore training set ka gradient ek step me calculate karta hai, jo accurate hota hai lekin slow. Stochastic GD har training example ke liye gradient compute karta hai, fast updates milti hain lekin noisy convergence hoti hai. Mini-batch GD batch size (e.g., 32, 64) ke groups me gradient calculate karta hai, jo speed aur stability ka behtar tradeoff deta hai.

### Q4: How does a Confusion Matrix help in evaluating classification models?

**Answer:** Confusion Matrix actual vs predicted classes ko tabular form me dikhata hai: True Positives (TP), False Positives (FP), True Negatives (TN), False Negatives (FN). Isse precision, recall, F1-score, specificity, aur accuracy calculate kar sakte hain. Especially imbalanced datasets me accuracy misleading ho sakta hai, lekin precision/recall se model ki strength aur weakness samajh aati hai.

### Q5: Explain the concept of ensemble learning and give examples of bagging vs boosting.

**Answer:** Ensemble learning multiple weak learners ko combine karke strong predictor banata hai. Bagging (Bootstrap Aggregating) independent models ko different bootstrapped samples se train karta hai aur predictions ko average/vote karta hai; example: Random Forest. Bagging variance reduce karta hai. Boosting sequentially weak learners train karta hai, har iteration me previous errors ko weight deta hai; example: AdaBoost, Gradient Boosting, XGBoost. Boosting bias reduce karta hai aur strong learners banata hai, lekin overfitting risk bhi hota hai if not regularized.
