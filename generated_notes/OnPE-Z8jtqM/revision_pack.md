# Revision Pack: Outlier Detection and Removal using Z-score Method | Handling Outliers Part 2

**One-Line Summary:** Machine Learning ka core idea hai data se patterns learn karke predictions ya decisions automate karna.

## Cheat Sheet

### ML Cheat Sheet
| Concept | Key Points | Typical Algorithms |
|---|---|---|
| Supervised Learning | Labeled data, train-test split, loss minimization | Linear Regression, Logistic Regression, SVM, Decision Trees, Random Forest, XGBoost |
| Unsupervised Learning | No labels, discover structure, clustering or dimensionality reduction | K-Means, Hierarchical Clustering, PCA, Autoencoders |
| Regression | Predict continuous value, evaluate with MSE/MAE | Linear Regression, Ridge, Lasso, SVR |
| Classification | Predict discrete class, evaluate with Accuracy, Precision, Recall, F1 | Logistic Regression, Naive Bayes, SVM, k-NN, Neural Nets |
| Loss Functions | Measure error, guide optimization | MSE, Cross-Entropy, Hinge Loss |
| Optimization | Find parameters that minimize loss, gradient based | Gradient Descent, SGD, Adam, RMSprop |
| Regularization | Prevent overfitting, add penalty | L1 (Lasso), L2 (Ridge), Dropout |
| Evaluation Metrics | Quantify model performance on test data | Accuracy, ROC-AUC, Confusion Matrix, R² |
| Cross-Validation | Robust estimate of generalization, hyperparameter tuning | k-Fold CV, Stratified CV, Leave-One-Out |
| Feature Engineering | Transform raw data to improve model | Scaling, Encoding, Interaction terms, Feature Selection |

## Flashcards

### Card 1
**Q:** Supervised learning ka main requirement kya hota hai?

**A:** Labeled training data jisme input-output pairs hote hain.

### Card 2
**Q:** Regression aur classification mein primary difference kya hai?

**A:** Regression continuous output predict karta hai, classification discrete class labels predict karta hai.

### Card 3
**Q:** Mean Squared Error (MSE) ka formula kya hai?

**A:** MSE = (1/n) * Σ(y_i - ŷ_i)^2.

### Card 4
**Q:** Gradient Descent ka learning rate kya control karta hai?

**A:** Step size of parameter update; bahut high se overshoot, bahut low se slow convergence.

### Card 5
**Q:** L1 regularization ka effect kya hota hai?

**A:** Weights ko sparsify karta hai, feature selection promote hota hai.

### Card 6
**Q:** k-Fold Cross-Validation mein 'k' ka typical value kya hoti hai?

**A:** Commonly 5 ya 10, trade-off between bias and variance.

### Card 7
**Q:** ROC-AUC metric kis scenario mein useful hota hai?

**A:** Binary classification with imbalanced classes, threshold-independent performance measure.

### Card 8
**Q:** PCA ka primary goal kya hota hai?

**A:** Data dimensionality reduce karna while preserving maximum variance.

### Card 9
**Q:** Overfitting ko detect karne ka simple tarika kya hai?

**A:** Training error low aur validation/test error high hona.

### Card 10
**Q:** Decision Tree ka impurity measure kaunse do common types hain?

**A:** Gini impurity aur Entropy (Information Gain).

### Card 11
**Q:** Support Vector Machine (SVM) ka margin kya represent karta hai?

**A:** Closest data points (support vectors) ke beech ka distance; maximize karna hota hai.

### Card 12
**Q:** Bagging technique ka main advantage kya hai?

**A:** Variance reduce hota hai by averaging multiple models trained on bootstrapped samples.

### Card 13
**Q:** Learning rate decay ka purpose kya hota hai?

**A:** Training ke later stages mein step size kam karna for finer convergence.

### Card 14
**Q:** One-hot encoding ka drawback kya hai?

**A:** High dimensionality especially with many categories.

### Card 15
**Q:** Bias-Variance tradeoff ka simple explanation kya hai?

**A:** High bias = underfit, high variance = overfit; goal hai dono ko balance karna.

## Quiz

#### Question 1: Which loss function is most suitable for binary classification?
- [0] Mean Squared Error
- [1] Cross-Entropy Loss
- [2] Huber Loss
- [3] Hinge Loss

#### Question 2: In k-means clustering, what does the 'k' represent?
- [0] Number of features
- [1] Number of clusters
- [2] Number of iterations
- [3] Number of dimensions

#### Question 3: What is the effect of increasing the regularization strength (lambda) in Ridge Regression?
- [0] Model becomes more complex
- [1] Weights shrink towards zero
- [2] Training error decreases
- [3] Feature scaling becomes unnecessary

#### Question 4: Which evaluation metric is best for imbalanced binary classification?
- [0] Accuracy
- [1] Precision
- [2] Recall
- [3] ROC-AUC

#### Question 5: What does the term 'epoch' refer to in neural network training?
- [0] One forward pass of a single sample
- [1] One backward pass of a single sample
- [2] One full pass over the entire training dataset
- [3] Number of hidden layers

#### Question 6: Which algorithm is a type of ensemble method that reduces variance?
- [0] AdaBoost
- [1] Bagging
- [2] Gradient Boosting
- [3] Stacking

#### Question 7: In PCA, the principal components are orthogonal because they are derived from:
- [0] Covariance matrix eigenvectors
- [1] Correlation matrix diagonal
- [2] Mean vectors
- [3] Singular values only

#### Question 8: Which optimizer adapts the learning rate for each parameter individually?
- [0] SGD
- [1] Momentum
- [2] Adam
- [3] Newton's Method

#### Question 9: What is the main purpose of the validation set?
- [0] Train model parameters
- [1] Tune hyperparameters and prevent overfitting
- [2] Final performance reporting
- [3] Data preprocessing

#### Question 10: Which of the following is NOT a kernel function used in SVM?
- [0] Linear
- [1] Polynomial
- [2] RBF
- [3] Logistic

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Cross-Entropy (log loss) directly models probability of binary classes and penalizes confident wrong predictions.
- **Q2 Answer:** Option 1 — 'k' is the predefined number of clusters the algorithm will partition the data into.
- **Q3 Answer:** Option 1 — Higher lambda adds larger L2 penalty, forcing weights to shrink, which reduces variance but may increase bias.
- **Q4 Answer:** Option 3 — ROC-AUC considers true positive and false positive rates across thresholds, giving a balanced view for imbalanced data.
- **Q5 Answer:** Option 2 — An epoch means the model has seen every training example once.
- **Q6 Answer:** Option 1 — Bagging (e.g., Random Forest) builds multiple models on bootstrapped samples and averages them, reducing variance.
- **Q7 Answer:** Option 0 — Principal components are eigenvectors of the covariance matrix, guaranteeing orthogonality.
- **Q8 Answer:** Option 2 — Adam computes adaptive learning rates using first and second moments of gradients for each parameter.
- **Q9 Answer:** Option 1 — Validation set is used to evaluate model during training for hyperparameter tuning and early stopping.
- **Q10 Answer:** Option 3 — Logistic is a loss function, not a kernel. Common kernels are linear, polynomial, RBF, and sigmoid.

## Interview Questions

### Q1: Explain the bias-variance tradeoff with a practical example.

**Answer:** Bias-variance tradeoff describes how model error can be decomposed into bias (error from erroneous assumptions) and variance (error from sensitivity to training data). For example, a linear regression model on a highly non-linear dataset will have high bias (underfitting) because it cannot capture the curvature. Conversely, a deep decision tree can fit the training data perfectly (low bias) but will vary wildly with small changes in data, leading to high variance (overfitting). The goal is to choose a model complexity (or regularization) that balances both, often using cross-validation to find the sweet spot where total error is minimized.

### Q2: How does L1 regularization lead to feature selection?

**Answer:** L1 regularization adds the absolute value of coefficients to the loss function (λ∑|w_i|). During optimization, this penalty encourages many weights to become exactly zero because the cost of keeping a small non-zero weight outweighs its contribution to reducing loss. As a result, only the most informative features retain non-zero weights, effectively performing automatic feature selection while also reducing model complexity.

### Q3: What are the differences between bagging and boosting?

**Answer:** Bagging (Bootstrap Aggregating) builds multiple independent models on different bootstrapped subsets of data and aggregates their predictions (e.g., averaging for regression, majority vote for classification). It primarily reduces variance. Boosting, on the other hand, builds models sequentially where each new model focuses on the errors of the previous ones (e.g., AdaBoost, Gradient Boosting). It reduces bias by combining weak learners into a strong ensemble and can also improve variance, but is more prone to overfitting if not regularized.

### Q4: Why is feature scaling important for gradient-based algorithms?

**Answer:** Feature scaling ensures that all input dimensions have comparable magnitude. Gradient descent updates parameters proportionally to the gradient; if features are on vastly different scales, the loss surface becomes elongated, causing slow convergence along some dimensions and possible overshooting in others. Scaling (standardization or min-max) makes the loss landscape more isotropic, leading to faster and more stable convergence.

### Q5: Describe how you would handle an imbalanced classification problem.

**Answer:** Several strategies can be combined: (1) Resampling – either oversample the minority class (SMOTE) or undersample the majority class to balance class distribution. (2) Use class-weighted loss functions (e.g., setting higher weight for minority class in cross-entropy) so the model penalizes misclassifying minority samples more. (3) Choose appropriate evaluation metrics like ROC-AUC, Precision-Recall AUC, F1-score instead of accuracy. (4) Consider specialized algorithms like Balanced Random Forest or ensemble methods that incorporate sampling. Finally, validate using stratified cross-validation to preserve class ratios.
