# Revision Pack: Outlier Detection and Removal using the IQR Method | Handing Outliers Part 3

**One-Line Summary:** Machine Learning ke fundamentals: data preprocessing, model types, training, evaluation metrics, regularization aur popular algorithms ka short overview.

## Cheat Sheet

- **Data**: Collect → Clean → Feature Engineer → Split (train/val/test)
- **Supervised Learning**: Regression (MSE, RMSE) & Classification (Accuracy, Precision, Recall, F1)
- **Unsupervised Learning**: Clustering (K‑means), Dimensionality Reduction (PCA)
- **Model Training**: Loss function → Gradient Descent (SGD, Mini‑batch) → Learning Rate & Epochs
- **Regularization**: L1 (Lasso), L2 (Ridge), Dropout (NN), Early Stopping
- **Evaluation**: Cross‑validation, Confusion Matrix, ROC‑AUC
- **Key Algorithms**: Linear Regression, Logistic Regression, Decision Trees, Random Forest, SVM, K‑NN, Naïve Bayes, Neural Networks
- **Bias‑Variance Trade‑off**: High bias = underfit, High variance = overfit

## Flashcards

### Card 1
**Q:** Supervised learning ka main goal kya hota hai?

**A:** Input features se label predict karna, yaani mapping function learn karna.

### Card 2
**Q:** MSE ka full form aur use kya hai?

**A:** Mean Squared Error; regression models ki prediction error ko quantify karta hai.

### Card 3
**Q:** K‑means clustering mein 'K' ka matlab kya hota hai?

**A:** Number of clusters jo user define karta hai.

### Card 4
**Q:** L1 regularization ka effect kya hota hai on features?

**A:** Sparse solution deta hai, kuch coefficients ko zero kar deta hai.

### Card 5
**Q:** Gradient Descent ka learning rate bahut high ho to kya hota hai?

**A:** Updates overshoot karte hain, loss diverge ho sakta hai.

### Card 6
**Q:** Decision Tree me impurity measure ka ek example batao.

**A:** Gini impurity ya Entropy.

### Card 7
**Q:** Random Forest ka main advantage kya hai?

**A:** Bagging se variance reduce hoti hai, overfitting kam hota hai.

### Card 8
**Q:** SVM me kernel trick ka purpose kya hota hai?

**A:** Non‑linear data ko higher dimension me map karke linear separation enable karta hai.

### Card 9
**Q:** Neural Network me 'Dropout' technique ka kaam kya hai?

**A:** Random neurons ko training ke dauran disable karke overfitting prevent karta hai.

### Card 10
**Q:** Cross‑validation ka sabse common form kaun sa hai?

**A:** k‑fold cross‑validation, usually k=5 ya 10.

### Card 11
**Q:** Precision aur Recall ka trade‑off kaise visualize hota hai?

**A:** Precision‑Recall curve ya ROC curve ke through.

### Card 12
**Q:** PCA ka primary objective kya hota hai?

**A:** High‑dimensional data ki variance ko retain karte hue dimensions reduce karna.

### Card 13
**Q:** Mini‑batch Gradient Descent ka benefit kya hai?

**A:** Full batch ki stability aur SGD ki speed ka balance provide karta hai.

### Card 14
**Q:** Overfitting ko detect karne ke liye kaun si metric useful hai?

**A:** Validation loss ya accuracy; training se alag trend indicate karta hai.

### Card 15
**Q:** Logistic Regression me output kis range me hota hai?

**A:** 0 se 1 ke beech, sigmoid activation ke through.

## Quiz

#### Question 1: Which metric is most appropriate for imbalanced binary classification?
- [0] Accuracy
- [1] Mean Squared Error
- [2] F1 Score
- [3] R-squared

#### Question 2: In K‑means, what happens if you set K equal to the number of data points?
- [0] All points form one cluster
- [1] Each point becomes its own cluster
- [2] Algorithm fails to converge
- [3] Clusters become empty

#### Question 3: Which regularization adds a penalty equal to the absolute value of coefficients?
- [0] L1
- [1] L2
- [2] Elastic Net
- [3] Dropout

#### Question 4: What is the main purpose of early stopping during neural network training?
- [0] Speed up inference
- [1] Prevent vanishing gradients
- [2] Avoid overfitting
- [3] Increase model size

#### Question 5: Which kernel can map data to an infinite‑dimensional space?
- [0] Linear
- [1] Polynomial
- [2] RBF (Gaussian)
- [3] Sigmoid

#### Question 6: In a confusion matrix, which cell represents False Negatives?
- [0] Top‑left
- [1] Top‑right
- [2] Bottom‑left
- [3] Bottom‑right

#### Question 7: What does a high variance model typically exhibit?
- [0] Low training error, high test error
- [1] High training error, low test error
- [2] Both errors high
- [3] Both errors low

#### Question 8: Which algorithm is a non‑parametric, instance‑based learner?
- [0] Naïve Bayes
- [1] Decision Tree
- [2] K‑Nearest Neighbors
- [3] Linear Regression

#### Question 9: What is the effect of increasing the learning rate too much in gradient descent?
- [0] Faster convergence to global optimum
- [1] Oscillation or divergence of loss
- [2] Reduced overfitting
- [3] More regularization

#### Question 10: Which evaluation curve is best for comparing classifiers across all thresholds?
- [0] Precision‑Recall Curve
- [1] Learning Curve
- [2] ROC Curve
- [3] Loss Curve

### Quiz Answers & Explanations

- **Q1 Answer:** Option 2 — F1 Score balances precision and recall, making it suitable when classes are imbalanced.
- **Q2 Answer:** Option 1 — With K = N, each data point is assigned to a unique cluster, leading to zero intra‑cluster variance.
- **Q3 Answer:** Option 0 — L1 regularization (Lasso) uses the sum of absolute values, encouraging sparsity.
- **Q4 Answer:** Option 2 — Early stopping monitors validation loss and stops training when it stops improving, reducing overfitting.
- **Q5 Answer:** Option 2 — RBF kernel computes similarity based on distance and implicitly works in infinite dimensions.
- **Q6 Answer:** Option 2 — Bottom‑left cell counts actual positives predicted as negative, i.e., False Negatives.
- **Q7 Answer:** Option 0 — High variance means the model fits training data too well (low training error) but fails to generalize (high test error).
- **Q8 Answer:** Option 2 — K‑NN stores training instances and makes predictions based on nearest neighbors, without learning explicit parameters.
- **Q9 Answer:** Option 1 — A large learning rate can cause updates to overshoot minima, leading to loss oscillation or divergence.
- **Q10 Answer:** Option 2 — ROC curve plots TPR vs. FPR for all possible thresholds, allowing comprehensive classifier comparison.

## Interview Questions

### Q1: Explain the bias‑variance trade‑off and how it influences model selection.

**Answer:** Bias measures error due to overly simplistic assumptions (underfitting), while variance measures error from sensitivity to training data fluctuations (overfitting). A model with high bias has low variance and vice‑versa. The goal is to find a sweet spot where total error (bias² + variance + irreducible error) is minimized. Techniques like cross‑validation, regularization, and ensemble methods help balance the trade‑off.

### Q2: How does L1 regularization lead to feature selection?

**Answer:** L1 adds a penalty equal to the sum of absolute coefficient values to the loss function. During optimization, this penalty can drive some coefficients exactly to zero, effectively removing those features from the model. Hence, L1 (Lasso) performs implicit feature selection while fitting.

### Q3: What are the pros and cons of using a decision tree versus a random forest?

**Answer:** Decision Tree: Pros – easy to interpret, fast training, handles mixed data types. Cons – high variance, prone to overfitting, unstable to small data changes. Random Forest: Pros – reduces variance via bagging, better generalization, handles missing values, provides feature importance. Cons – less interpretable than a single tree, larger memory footprint, slower inference for many trees.

### Q4: Describe how the kernel trick works in Support Vector Machines.

**Answer:** The kernel trick replaces the inner product <φ(x_i), φ(x_j)> in the high‑dimensional feature space with a kernel function K(x_i, x_j) that can be computed directly in the original space. This avoids explicit mapping φ, reducing computational cost. Common kernels (linear, polynomial, RBF) allow SVM to find non‑linear decision boundaries while solving the dual optimization problem.

### Q5: When would you prefer using PCA over feature selection methods?

**Answer:** PCA is useful when you need to reduce dimensionality while preserving most variance, especially when features are highly correlated. It creates new orthogonal components rather than selecting a subset, which can improve model speed and mitigate multicollinearity. Feature selection is preferred when interpretability matters or when you want to keep original features. Use PCA when the goal is compression or noise reduction rather than interpretability.
