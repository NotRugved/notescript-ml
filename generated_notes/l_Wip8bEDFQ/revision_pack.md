# Revision Pack: Handling Missing Categorical Data | Simple Imputer | Most Frequent Imputation | Missing Category Imp

**One-Line Summary:** Machine Learning ka core idea hai data se patterns seekhna aur unhe future predictions ya decisions ke liye use karna.

## Cheat Sheet

### Key Concepts
| Concept | Key Points | Common Algorithms |
|---|---|---|
| Supervised Learning | Labeled data, train-test split, loss minimization | Linear Regression, Logistic Regression, SVM, Decision Trees |
| Unsupervised Learning | No labels, find hidden structure | K-Means, PCA, Autoencoders |
| Overfitting | Model fits noise, high variance | Use regularization, cross‑validation |
| Regularization | Penalize large weights, control complexity | L1 (Lasso), L2 (Ridge) |
| Gradient Descent | Iterative optimization, learning rate η | Batch GD, Stochastic GD, Mini‑batch GD |
| Evaluation Metrics | Regression: RMSE, MAE; Classification: Accuracy, Precision, Recall, F1, ROC‑AUC |
| Hyperparameter Tuning | Grid Search, Random Search, Bayesian Opt |
| Feature Engineering | Scaling, Encoding, Interaction terms |
| Model Selection | Bias‑Variance trade‑off, validation curves |
| Ensemble Methods | Combine weak learners for stronger performance | Bagging, Boosting (AdaBoost, XGBoost), Stacking |

## Flashcards

### Card 1
**Q:** Supervised learning ka main requirement kya hota hai?

**A:** Labeled training data jisme input-output pairs hote hain.

### Card 2
**Q:** Linear regression ka loss function kaun sa hota hai?

**A:** Mean Squared Error (MSE) ya Sum of Squared Errors (SSE).

### Card 3
**Q:** Logistic regression me output kis range me hota hai?

**A:** 0 se 1 ke beech, sigmoid activation ke through.

### Card 4
**Q:** Overfitting ko detect karne ka simple tarika kya hai?

**A:** Training error low aur validation/test error high hona.

### Card 5
**Q:** L1 regularization ka effect kya hota hai?

**A:** Weight sparsity create hoti hai, feature selection hoti hai.

### Card 6
**Q:** Gradient descent me learning rate bahut high ho to kya hota hai?

**A:** Updates overshoot karega, loss diverge ho sakta hai.

### Card 7
**Q:** K-Means clustering ka objective function kya minimize karta hai?

**A:** Within‑cluster sum of squares (WCSS).

### Card 8
**Q:** Decision tree me impurity measure kaun se use hote hain?

**A:** Gini impurity ya Entropy (Information Gain).

### Card 9
**Q:** Cross‑validation ka sabse common form kaun sa hai?

**A:** k‑fold cross‑validation, usually k=5 ya 10.

### Card 10
**Q:** ROC‑AUC metric kya measure karta hai?

**A:** True positive rate vs false positive rate ka trade‑off across thresholds.

### Card 11
**Q:** Bagging ka main advantage kya hai?

**A:** Variance reduction through averaging multiple models.

### Card 12
**Q:** Boosting me weak learners ko kaise improve kiya jata hai?

**A:** Har iteration me previous errors ko weight diya jata hai.

### Card 13
**Q:** PCA ka purpose kya hota hai?

**A:** Dimensionality reduction by projecting data on top principal components.

### Card 14
**Q:** Feature scaling kyu zaroori hai?

**A:** Gradient descent aur distance‑based algorithms ko stable banata hai.

### Card 15
**Q:** Hyperparameter tuning me validation set ka role kya hota hai?

**A:** Model ke hyperparameters ko evaluate karne ke liye unbiased estimate provide karta hai.

## Quiz

#### Question 1: Which loss function is typically used for binary classification?
- [0] Mean Squared Error
- [1] Cross‑Entropy Loss
- [2] Hinge Loss
- [3] Huber Loss

#### Question 2: A model with high bias and low variance will most likely:
- [0] Underfit the data
- [1] Overfit the data
- [2] Generalize well
- [3] Require more features

#### Question 3: In k‑fold cross‑validation with k=5, how many times is the model trained?
- [0] 1
- [1] 5
- [2] 10
- [3] k‑1

#### Question 4: Which regularization technique can set some coefficients exactly to zero?
- [0] L2 (Ridge)
- [1] Dropout
- [2] L1 (Lasso)
- [3] Early Stopping

#### Question 5: What does the 'C' parameter control in an SVM with linear kernel?
- [0] Kernel width
- [1] Regularization strength
- [2] Learning rate
- [3] Number of support vectors

#### Question 6: Which algorithm is an example of a boosting method?
- [0] Random Forest
- [1] AdaBoost
- [2] K‑Nearest Neighbors
- [3] PCA

#### Question 7: If you observe that training loss keeps decreasing but validation loss starts increasing, you should:
- [0] Increase model complexity
- [1] Decrease learning rate
- [2] Apply early stopping
- [3] Add more training data

#### Question 8: Which metric is most appropriate for imbalanced binary classification?
- [0] Accuracy
- [1] Precision
- [2] Recall
- [3] F1‑Score

#### Question 9: In PCA, the principal components are:
- [0] Features with highest variance
- [1] Features with lowest variance
- [2] Random linear combinations
- [3] Original features after scaling

#### Question 10: Which of the following is NOT a hyperparameter?
- [0] Learning rate
- [1] Number of trees in Random Forest
- [2] Weights of a trained model
- [3] Maximum depth of a decision tree

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Cross‑Entropy (log loss) directly models probability of binary classes and penalizes confident wrong predictions.
- **Q2 Answer:** Option 0 — High bias means the model is too simple, leading to underfitting despite low variance.
- **Q3 Answer:** Option 1 — The dataset is split into 5 folds; each fold serves once as validation, so the model is trained 5 times.
- **Q4 Answer:** Option 2 — L1 regularization adds absolute value penalty, encouraging sparsity and zeroing out some weights.
- **Q5 Answer:** Option 1 — C is the inverse of regularization strength; a small C means strong regularization.
- **Q6 Answer:** Option 1 — AdaBoost sequentially trains weak learners, focusing on previously misclassified samples.
- **Q7 Answer:** Option 2 — Early stopping halts training when validation loss worsens, preventing overfitting.
- **Q8 Answer:** Option 3 — F1‑Score balances precision and recall, making it suitable when classes are imbalanced.
- **Q9 Answer:** Option 0 — Principal components are orthogonal directions that capture maximum variance in the data.
- **Q10 Answer:** Option 2 — Weights are learned parameters, not hyperparameters set before training.

## Interview Questions

### Q1: Explain the bias‑variance trade‑off and how it influences model selection.

**Answer:** Bias is error due to overly simplistic assumptions (underfitting), variance is error due to sensitivity to training data fluctuations (overfitting). A good model balances both: low enough bias to capture patterns, low enough variance to generalize. Techniques like regularization, cross‑validation, and ensemble methods help navigate this trade‑off.

### Q2: How does L1 regularization lead to feature selection, and when would you prefer it over L2?

**Answer:** L1 adds the absolute value of weights to the loss, encouraging many weights to become exactly zero, effectively selecting a subset of features. It's preferred when you suspect many irrelevant features or need a sparse model, whereas L2 shrinks weights but rarely zeroes them, useful for multicollinearity handling.

### Q3: Describe the steps of gradient descent and the impact of learning rate scheduling.

**Answer:** Gradient descent iteratively updates parameters: w := w - η * ∇L(w). The learning rate η controls step size; too large causes divergence, too small slows convergence. Scheduling (e.g., decay, cosine annealing) reduces η over time, allowing fast initial progress and fine‑tuned convergence, improving stability and avoiding local minima.

### Q4: What are the differences between bagging and boosting, and when would you use each?

**Answer:** Bagging builds multiple independent models on bootstrapped samples and averages predictions, reducing variance (e.g., Random Forest). Boosting builds models sequentially, each focusing on previous errors, reducing bias and improving accuracy (e.g., AdaBoost, XGBoost). Use bagging when variance is high and models are unstable; use boosting when you need higher predictive power and can tolerate longer training.

### Q5: Explain how ROC‑AUC is computed and why it is a better metric than accuracy for imbalanced datasets.

**Answer:** ROC plots TPR vs FPR at various thresholds. AUC is the area under this curve, representing the probability that a randomly chosen positive instance ranks higher than a negative one. Unlike accuracy, which can be misleading when one class dominates, AUC evaluates ranking quality across all thresholds, making it robust to class imbalance.
