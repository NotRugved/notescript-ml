# Principle Component Analysis (PCA) | Part 2 | Problem Formulation and Step by Step Solution

**Video Link:** [https://www.youtube.com/watch?v=tXXnxjj2wM4](https://www.youtube.com/watch?v=tXXnxjj2wM4)

**Summary:** Balance model complexity using the Bias-Variance Tradeoff, Regularization (L1/L2), and Cross-Validation to prevent Overfitting and Underfitting.

## Theory

### Introduction to Overfitting and Underfitting ([20:00](https://youtu.be/tXXnxjj2wM4?t=1200))

In this segment, the instructor discusses the concepts of overfitting and underfitting in machine learning models. Overfitting occurs when a model learns the training data too well, including noise and outliers, leading to poor performance on unseen data. Underfitting happens when the model is too simple to capture the underlying pattern in the data, resulting in high bias and poor performance on both training and test sets. The instructor emphasizes the importance of finding a balance between model complexity and generalization ability.

### Bias-Variance Tradeoff ([22:15](https://youtu.be/tXXnxjj2wM4?t=1335))

The bias-variance tradeoff is a fundamental concept in machine learning. Bias refers to the error introduced by approximating a real-world problem with a simplified model. Variance refers to the sensitivity of the model to fluctuations in the training data. High bias leads to underfitting, while high variance leads to overfitting. The goal is to find a model that has low bias and low variance, which can be achieved by adjusting model complexity, using regularization techniques, or increasing the amount of training data.

### Regularization Techniques ([24:30](https://youtu.be/tXXnxjj2wM4?t=1470))

Regularization is a technique used to prevent overfitting by adding a penalty term to the loss function. The two most common types of regularization are L1 (Lasso) and L2 (Ridge). L1 regularization adds the absolute value of the coefficients to the loss function, which can lead to sparse models where some coefficients become zero. L2 regularization adds the square of the coefficients to the loss function, which shrinks the coefficients but does not set them to zero. The instructor explains how to choose the regularization strength using cross-validation.

### Cross-Validation ([26:45](https://youtu.be/tXXnxjj2wM4?t=1605))

Cross-validation is a resampling procedure used to evaluate machine learning models on a fixed data set. The most common type is k-fold cross-validation, where the data is divided into k subsets. The model is trained on k-1 subsets and validated on the remaining subset. This process is repeated k times, with each subset used exactly once as the validation data. The average performance across all k folds is used as the estimate of the model's performance. This helps in assessing the model's generalization ability and selecting hyperparameters.

## Intuition

- ([20:30](https://youtu.be/tXXnxjj2wM4?t=1230)) Imagine you are studying for an exam. If you memorize the textbook word for word, you might do well on the exact questions from the book but fail on new questions that test the same concepts. This is like overfitting. On the other hand, if you only skim the surface and don't understand the core concepts, you will struggle with both the textbook questions and new questions. This is like underfitting. The ideal approach is to understand the concepts deeply so you can apply them to new problems.
- ([25:00](https://youtu.be/tXXnxjj2wM4?t=1500)) Regularization is like adding a constraint to your study time. If you study too much, you might burn out and not retain information well. If you study too little, you won't be prepared. Regularization helps you find the right balance by penalizing excessive complexity, ensuring you focus on the most important concepts.

## Code

*No code blocks identified.*

## Analogies

- ([20:30](https://youtu.be/tXXnxjj2wM4?t=1230)) **Analogy:** Studying for an exam by memorizing the textbook word for word vs. understanding the concepts. — *Explains:* This analogy explains the difference between overfitting (memorizing) and underfitting (not understanding). It highlights the importance of generalization ability in machine learning models.
- ([25:00](https://youtu.be/tXXnxjj2wM4?t=1500)) **Analogy:** Adding a constraint to study time to avoid burnout or insufficient preparation. — *Explains:* This analogy explains how regularization works by adding a penalty to the loss function, preventing the model from becoming too complex and overfitting the training data.

## Common Mistakes

- **Mistake [teacher]:** Choosing a model that is too complex for the dataset. ([21:00](https://youtu.be/tXXnxjj2wM4?t=1260))
  - *Why:* A complex model may overfit the training data, leading to poor performance on unseen data.
  - *Fix:* Use regularization techniques or choose a simpler model. Evaluate the model using cross-validation to ensure it generalizes well.
- **Mistake [teacher]:** Ignoring the bias-variance tradeoff when selecting a model. ([23:00](https://youtu.be/tXXnxjj2wM4?t=1380))
  - *Why:* Focusing only on training accuracy can lead to overfitting, while focusing only on simplicity can lead to underfitting.
  - *Fix:* Balance model complexity and generalization ability by using techniques like cross-validation and regularization.

## Formulas & Key Terms

### Formulas
- **L1 Regularization (Lasso):** `Loss = Original Loss + λ * Σ|w_i|` — Adds the absolute value of the coefficients to the loss function, promoting sparsity.
- **L2 Regularization (Ridge):** `Loss = Original Loss + λ * Σw_i^2` — Adds the square of the coefficients to the loss function, shrinking the coefficients.

### Key Terms
- **Overfitting:** When a model learns the training data too well, including noise, leading to poor performance on unseen data.
- **Underfitting:** When a model is too simple to capture the underlying pattern in the data, resulting in poor performance on both training and test sets.
- **Bias-Variance Tradeoff:** The balance between the error introduced by simplifying the model (bias) and the sensitivity to fluctuations in the training data (variance).
- **Regularization:** A technique used to prevent overfitting by adding a penalty term to the loss function.
- **Cross-Validation:** A resampling procedure used to evaluate machine learning models on a fixed data set, helping to assess generalization ability.
