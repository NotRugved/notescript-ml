# Revision Pack: Missing Indicator | Random Sample Imputation | Handling Missing Data Part 4

**One-Line Summary:** No lecture notes provided, so a generic ML revision pack is generated.

## Cheat Sheet

- **No specific lecture content available.**
- **General ML Concepts:**
  - Supervised Learning: Labeled data (e.g., Regression, Classification).
  - Unsupervised Learning: Unlabeled data (e.g., Clustering, Dimensionality Reduction).
  - Reinforcement Learning: Agent learns via rewards/punishments.
- **Key Algorithms:**
  - Linear Regression: Minimizes Mean Squared Error (MSE).
  - Decision Trees: Splits data based on feature importance.
  - Neural Networks: Layers of interconnected nodes.

## Flashcards

### Card 1
**Q:** What is Supervised Learning?

**A:** Learning from labeled data to predict outputs.

### Card 2
**Q:** What is Unsupervised Learning?

**A:** Finding patterns in unlabeled data.

### Card 3
**Q:** What is Reinforcement Learning?

**A:** Learning through trial and error with rewards.

### Card 4
**Q:** What is Overfitting?

**A:** Model performs well on training data but poorly on unseen data.

### Card 5
**Q:** What is Underfitting?

**A:** Model is too simple to capture data patterns.

### Card 6
**Q:** What is Cross-Validation?

**A:** A technique to evaluate model performance by splitting data into folds.

### Card 7
**Q:** What is a Loss Function?

**A:** A function that measures how wrong the model's predictions are.

### Card 8
**Q:** What is Gradient Descent?

**A:** An optimization algorithm to minimize the loss function.

### Card 9
**Q:** What is a Feature?

**A:** An individual measurable property of an observation.

### Card 10
**Q:** What is a Label?

**A:** The target variable in supervised learning.

### Card 11
**Q:** What is Bias in ML?

**A:** Error due to overly simplistic assumptions in the model.

### Card 12
**Q:** What is Variance in ML?

**A:** Error due to sensitivity to fluctuations in the training data.

### Card 13
**Q:** What is Regularization?

**A:** A technique to prevent overfitting by adding a penalty to the loss function.

### Card 14
**Q:** What is a Hyperparameter?

**A:** A parameter set before the learning process begins.

### Card 15
**Q:** What is a Parameter?

**A:** A value learned by the model during training.

## Quiz

#### Question 1: Which type of learning uses labeled data?
- [0] Supervised
- [1] Unsupervised
- [2] Reinforcement
- [3] Semi-supervised

#### Question 2: What is the primary goal of a loss function?
- [0] Maximize accuracy
- [1] Minimize error
- [2] Increase complexity
- [3] Reduce data size

#### Question 3: Overfitting occurs when a model:
- [0] Is too simple
- [1] Performs well on training but poorly on test data
- [2] Has high bias
- [3] Lacks features

#### Question 4: Which algorithm is used for optimization in neural networks?
- [0] K-Means
- [1] Gradient Descent
- [2] PCA
- [3] Apriori

#### Question 5: What is a hyperparameter?
- [0] A learned value
- [1] A set before training
- [2] A data feature
- [3] A label

#### Question 6: Which technique helps prevent overfitting?
- [0] Increasing model complexity
- [1] Regularization
- [2] Reducing data
- [3] Removing labels

#### Question 7: What is the purpose of cross-validation?
- [0] To increase data size
- [1] To evaluate model performance
- [2] To reduce features
- [3] To label data

#### Question 8: Which of the following is an unsupervised learning task?
- [0] Classification
- [1] Regression
- [2] Clustering
- [3] Prediction

#### Question 9: What does high variance indicate?
- [0] Model is too simple
- [1] Model is sensitive to training data
- [2] Model has high bias
- [3] Model is underfit

#### Question 10: What is a parameter in ML?
- [0] Set before training
- [1] Learned during training
- [2] A data feature
- [3] A label

### Quiz Answers & Explanations

- **Q1 Answer:** Option 0 — Supervised learning relies on labeled data to train models.
- **Q2 Answer:** Option 1 — A loss function quantifies the error, and the goal is to minimize it.
- **Q3 Answer:** Option 1 — Overfitting means the model memorizes training data instead of generalizing.
- **Q4 Answer:** Option 1 — Gradient Descent is commonly used to minimize the loss in neural networks.
- **Q5 Answer:** Option 1 — Hyperparameters are configured before the learning process starts.
- **Q6 Answer:** Option 1 — Regularization adds a penalty to the loss function to simplify the model.
- **Q7 Answer:** Option 1 — Cross-validation provides a robust estimate of model performance.
- **Q8 Answer:** Option 2 — Clustering groups data without labels, making it unsupervised.
- **Q9 Answer:** Option 1 — High variance means the model changes significantly with different training data.
- **Q10 Answer:** Option 1 — Parameters are values the model learns from the data.

## Interview Questions

### Q1: Explain the bias-variance tradeoff.

**Answer:** The bias-variance tradeoff is the balance between a model's ability to fit training data (low bias) and generalize to new data (low variance). High bias leads to underfitting, while high variance leads to overfitting. The goal is to find a model with an optimal balance.

### Q2: How does regularization prevent overfitting?

**Answer:** Regularization adds a penalty term to the loss function, discouraging the model from becoming too complex. This helps the model generalize better by reducing the impact of less important features.

### Q3: What is the difference between a parameter and a hyperparameter?

**Answer:** Parameters are learned by the model during training (e.g., weights in a neural network), while hyperparameters are set before training begins (e.g., learning rate, number of layers).

### Q4: Describe the process of gradient descent.

**Answer:** Gradient descent is an iterative optimization algorithm that updates model parameters in the direction of the negative gradient of the loss function. The learning rate controls the step size, and the process continues until convergence.

### Q5: Why is cross-validation important?

**Answer:** Cross-validation provides a more reliable estimate of model performance by averaging results over multiple train-test splits. It helps detect overfitting and ensures the model generalizes well to unseen data.
