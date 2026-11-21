# Revision Pack: Power Transformer | Box - Cox Transform | Yeo - Johnson Transform

**One-Line Summary:** Machine Learning ka core idea hai data se patterns seekhkar predictions ya decisions automate karna.

## Cheat Sheet

- **Supervised Learning**: Labeled data → Regression (MSE, Linear Regression) & Classification (Logistic Regression, SVM, k-NN)
- **Unsupervised Learning**: Unlabeled data → Clustering (k-Means, Hierarchical), Dimensionality Reduction (PCA, t-SNE)
- **Model Evaluation**: Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix
- **Bias-Variance Tradeoff**: High bias = underfit, high variance = overfit; use regularization & more data.
- **Regularization**: L1 (Lasso) → sparsity, L2 (Ridge) → weight decay, Elastic Net = combo.
- **Gradient Descent**: Batch, Stochastic (SGD), Mini-batch; learning rate, momentum, Adam optimizer.
- **Ensemble Methods**: Bagging (Random Forest), Boosting (AdaBoost, XGBoost), Stacking.
- **Cross-Validation**: k-fold, stratified k-fold, leave-one-out for robust error estimate.
- **Feature Engineering**: Scaling (Standard/MinMax), Encoding (One-Hot, Label), Interaction terms, Polynomial features.
- **Hyperparameter Tuning**: Grid Search, Random Search, Bayesian Optimization.
- **Model Deployment**: Serialization (pickle, joblib), REST API, monitoring drift.

## Flashcards

### Card 1
**Q:** Supervised learning mein label ka kya role hota hai?

**A:** Label model ko ground truth provide karta hai jisse loss compute karke parameters update hote hain.

### Card 2
**Q:** Linear regression ka loss function kaun sa hota hai?

**A:** Mean Squared Error (MSE) ya Sum of Squared Errors (SSE).

### Card 3
**Q:** Logistic regression output ko kaun si function se map karta hai probability me?

**A:** Sigmoid function.

### Card 4
**Q:** SVM ka primary objective kya hota hai?

**A:** Maximum margin hyperplane find karna jo classes ko separate kare.

### Card 5
**Q:** k-NN algorithm ki prediction time complexity kaise hoti hai?

**A:** O(N * d) where N = training points, d = dimensions, kyunki sab points distance compute karte hain.

### Card 6
**Q:** PCA ka main goal kya hota hai?

**A:** Data ki dimensionality reduce karna while maximum variance retain karna.

### Card 7
**Q:** L1 regularization ka effect kya hota hai on features?

**A:** Sparse weights produce karta hai, yani kuch features ki coefficients zero ho jati hain.

### Card 8
**Q:** Random Forest me bagging ka matlab kya hota hai?

**A:** Har tree ko random subset of data (with replacement) aur random subset of features se train karna.

### Card 9
**Q:** Cross-validation me stratified k-fold ka use kab karte hain?

**A:** Jab class distribution imbalance ho, taki har fold me same proportion of classes ho.

### Card 10
**Q:** Gradient descent me learning rate bahut high ho to kya hota hai?

**A:** Overshooting, loss diverge ho sakta hai ya oscillate karega.

### Card 11
**Q:** AdaBoost me weak learners ko kaise combine karte hain?

**A:** Har weak learner ko weight assign karte hain based on error, aur final prediction weighted vote hoti hai.

### Card 12
**Q:** ROC curve ka x-axis aur y-axis kya represent karte hain?

**A:** X-axis = False Positive Rate, Y-axis = True Positive Rate.

### Card 13
**Q:** Overfitting ko detect karne ke liye kaun se metric useful hai?

**A:** Training vs validation loss gap; agar validation loss higher, overfitting ho sakta hai.

### Card 14
**Q:** Batch gradient descent me ek iteration me kitne samples use hote hain?

**A:** Pure training set ke sabhi samples.

### Card 15
**Q:** One-hot encoding me dummy variable trap ka kya issue hota hai?

**A:** Collinearity introduce hoti hai; ek column drop karna chahiye.

## Quiz

#### Question 1: Which loss function is most appropriate for binary classification?
- [0] Mean Squared Error
- [1] Cross-Entropy Loss
- [2] Hinge Loss
- [3] Huber Loss

#### Question 2: In k-means clustering, what does the 'k' represent?
- [0] Number of features
- [1] Number of clusters
- [2] Number of iterations
- [3] Number of dimensions

#### Question 3: Which regularization technique can set some coefficients exactly to zero?
- [0] L2 (Ridge)
- [1] L1 (Lasso)
- [2] Elastic Net
- [3] Dropout

#### Question 4: What is the main advantage of using a validation set over just a training set?
- [0] It reduces training time
- [1] It helps tune hyperparameters without leaking test information
- [2] It increases model capacity
- [3] It eliminates need for cross‑validation

#### Question 5: Which ensemble method builds models sequentially, each trying to correct its predecessor?
- [0] Bagging
- [1] Random Forest
- [2] Boosting
- [3] Stacking

#### Question 6: In a confusion matrix, which metric is defined as TP / (TP + FN)?
- [0] Precision
- [1] Recall
- [2] F1‑Score
- [3] Specificity

#### Question 7: What does the 'momentum' term in gradient descent help with?
- [0] Increasing learning rate automatically
- [1] Escaping local minima and smoothing updates
- [2] Reducing model size
- [3] Normalizing features

#### Question 8: Which kernel allows SVM to create non‑linear decision boundaries without explicitly mapping data?
- [0] Linear kernel
- [1] Polynomial kernel
- [2] RBF (Gaussian) kernel
- [3] All of the above

#### Question 9: When would you prefer using stratified k‑fold cross‑validation?
- [0] When dataset is very small
- [1] When classes are imbalanced
- [2] When features are highly correlated
- [3] When training time is critical

#### Question 10: What is the purpose of the 'early stopping' technique?
- [0] To speed up training by reducing epochs
- [1] To prevent overfitting by halting when validation loss stops improving
- [2] To increase model complexity
- [3] To automatically select the best optimizer

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Cross-Entropy (log loss) directly models probability of binary outcomes and penalizes confident wrong predictions heavily.
- **Q2 Answer:** Option 1 — 'k' is the predefined number of clusters that the algorithm will partition the data into.
- **Q3 Answer:** Option 1 — L1 regularization adds absolute value penalty, leading to sparse solutions where some weights become zero.
- **Q4 Answer:** Option 1 — A validation set provides unbiased feedback for hyperparameter tuning while keeping the test set untouched for final evaluation.
- **Q5 Answer:** Option 2 — Boosting (e.g., AdaBoost, XGBoost) adds weak learners one after another, focusing on previously mis‑classified samples.
- **Q6 Answer:** Option 1 — Recall (a.k.a. Sensitivity) measures the proportion of actual positives correctly identified.
- **Q7 Answer:** Option 1 — Momentum adds a fraction of the previous update to the current one, helping accelerate across flat regions and damp oscillations.
- **Q8 Answer:** Option 3 — All listed kernels can be used; the RBF kernel is most common for non‑linear separation.
- **Q9 Answer:** Option 1 — Stratified k‑fold maintains the same class proportion in each fold, which is crucial for imbalanced datasets.
- **Q10 Answer:** Option 1 — Early stopping monitors validation performance and stops training once it no longer improves, reducing overfitting.

## Interview Questions

### Q1: Explain the bias‑variance tradeoff and how you would address high variance in a model.

**Answer:** Bias‑variance tradeoff describes how model error decomposes into bias (error from erroneous assumptions) and variance (error from sensitivity to training data). High variance means the model overfits. To reduce it, you can gather more data, simplify the model (fewer parameters), apply regularization (L1/L2), use ensemble methods like bagging, or perform feature selection to remove noisy features.

### Q2: How does the Adam optimizer differ from standard stochastic gradient descent?

**Answer:** Adam combines ideas of momentum and adaptive learning rates. It maintains per‑parameter estimates of first (mean) and second (uncentered variance) moments of gradients, updating them with decay rates (beta1, beta2). This results in faster convergence and less sensitivity to the initial learning rate compared to plain SGD, which uses a single global learning rate and optionally momentum.

### Q3: What are the pros and cons of using one‑hot encoding versus label encoding for categorical features?

**Answer:** One‑hot encoding creates binary columns for each category, preserving no ordinal relationship and works well with linear models but can increase dimensionality dramatically (curse of dimensionality). Label encoding assigns an integer to each category, which is memory efficient but introduces an artificial ordinal relationship that can mislead algorithms that assume ordering (e.g., linear regression, distance‑based models). Choose based on model type and cardinality of the feature.

### Q4: Describe how XGBoost handles missing values during training.

**Answer:** XGBoost learns default directions for each split when a feature value is missing. During tree construction, it evaluates both left and right child losses for missing entries and picks the direction that yields the best gain. At inference, if a feature is missing, the instance follows the learned default path, allowing XGBoost to handle missing data without explicit imputation.

### Q5: When would you use a ROC curve versus a Precision‑Recall curve?

**Answer:** ROC curves are useful when the classes are roughly balanced and you care about both false positives and false negatives. Precision‑Recall curves are more informative for imbalanced datasets, especially when the positive class is rare, because they focus on the performance of the positive predictions (precision) and the ability to capture all positives (recall).
