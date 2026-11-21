# Revision Pack: Multivariate Imputation by Chained Equations for Missing Value | MICE Algorithm | Iterative Imputer

**One-Line Summary:** No lecture notes provided, so this is a placeholder revision pack for a generic ML topic.

## Cheat Sheet

- **Note**: Please provide the lecture notes to generate specific content.
- **General ML Tip**: Always normalize data before training.
- **Key Concept**: Bias-Variance Tradeoff is fundamental to model selection.

## Flashcards

### Card 1
**Q:** What is the primary goal of supervised learning?

**A:** To learn a mapping function from input data to output labels.

### Card 2
**Q:** What does 'overfitting' mean?

**A:** When a model learns the training data too well, including noise, leading to poor generalization.

### Card 3
**Q:** Name one common evaluation metric for classification.

**A:** Accuracy, Precision, Recall, or F1-Score.

### Card 4
**Q:** What is the purpose of cross-validation?

**A:** To estimate how a model will perform on unseen data by partitioning the data into subsets.

### Card 5
**Q:** What is a hyperparameter?

**A:** A parameter set before the learning process begins, not learned from data (e.g., learning rate).

### Card 6
**Q:** What is the difference between a parameter and a hyperparameter?

**A:** Parameters are learned during training; hyperparameters are set by the user.

### Card 7
**Q:** What is regularization?

**A:** A technique to prevent overfitting by adding a penalty to the loss function.

### Card 8
**Q:** What is the bias-variance tradeoff?

**A:** The tension between a model's ability to fit training data (variance) and its simplicity (bias).

### Card 9
**Q:** What is a decision boundary?

**A:** The line or surface that separates different classes in a classification model.

### Card 10
**Q:** What is the purpose of feature scaling?

**A:** To ensure that all features contribute equally to the model's learning process.

### Card 11
**Q:** What is a loss function?

**A:** A function that measures the error between predicted and actual values.

### Card 12
**Q:** What is gradient descent?

**A:** An optimization algorithm used to minimize the loss function by iteratively adjusting parameters.

### Card 13
**Q:** What is the learning rate in gradient descent?

**A:** The step size at which the algorithm updates the parameters.

### Card 14
**Q:** What is a neural network?

**A:** A machine learning model inspired by the human brain, consisting of layers of interconnected nodes.

### Card 15
**Q:** What is backpropagation?

**A:** An algorithm used to calculate the gradient of the loss function with respect to the network's parameters.

## Quiz

#### Question 1: Which of the following is a supervised learning algorithm?
- [0] K-Means Clustering
- [1] Linear Regression
- [2] PCA
- [3] Autoencoder

#### Question 2: What is the main cause of overfitting?
- [0] Too little data
- [1] Model too complex
- [2] High learning rate
- [3] Insufficient features

#### Question 3: Which metric is most appropriate for imbalanced datasets?
- [0] Accuracy
- [1] F1-Score
- [2] Mean Squared Error
- [3] R-Squared

#### Question 4: What is the purpose of a validation set?
- [0] To train the model
- [1] To tune hyperparameters
- [2] To test final performance
- [3] To generate synthetic data

#### Question 5: Which of the following is a hyperparameter?
- [0] Weights
- [1] Biases
- [2] Learning Rate
- [3] Number of epochs (if fixed)

#### Question 6: What does a high bias indicate?
- [0] Overfitting
- [1] Underfitting
- [2] Perfect fit
- [3] High variance

#### Question 7: Which technique helps prevent overfitting?
- [0] Increasing model complexity
- [1] Adding more data
- [2] Reducing regularization
- [3] Using a smaller dataset

#### Question 8: What is the role of the loss function?
- [0] To classify data
- [1] To measure prediction error
- [2] To normalize data
- [3] To select features

#### Question 9: What happens if the learning rate is too high?
- [0] Model converges faster
- [1] Model diverges
- [2] Model underfits
- [3] Model overfits

#### Question 10: Which of the following is an unsupervised learning task?
- [0] Spam detection
- [1] Image classification
- [2] Customer segmentation
- [3] Price prediction

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Linear Regression is a supervised learning algorithm because it learns from labeled data.
- **Q2 Answer:** Option 1 — Overfitting occurs when the model is too complex for the amount of data, capturing noise.
- **Q3 Answer:** Option 1 — F1-Score balances precision and recall, making it better for imbalanced datasets than accuracy.
- **Q4 Answer:** Option 1 — The validation set is used to tune hyperparameters and select the best model.
- **Q5 Answer:** Option 2 — Learning rate is a hyperparameter set before training, while weights are learned parameters.
- **Q6 Answer:** Option 1 — High bias means the model is too simple and underfits the data.
- **Q7 Answer:** Option 1 — Adding more data helps the model generalize better and reduces overfitting.
- **Q8 Answer:** Option 1 — The loss function quantifies how wrong the model's predictions are.
- **Q9 Answer:** Option 1 — A high learning rate can cause the model to overshoot the minimum and diverge.
- **Q10 Answer:** Option 2 — Customer segmentation is an unsupervised task because it groups data without labels.

## Interview Questions

### Q1: Explain the bias-variance tradeoff.

**Answer:** The bias-variance tradeoff is a fundamental concept in machine learning that describes the tension between a model's ability to fit the training data (variance) and its simplicity (bias). High bias leads to underfitting, while high variance leads to overfitting. The goal is to find a balance that minimizes the total error.

### Q2: How do you handle imbalanced datasets?

**Answer:** Imbalanced datasets can be handled using techniques like oversampling the minority class (e.g., SMOTE), undersampling the majority class, using different evaluation metrics (e.g., F1-Score), or applying class weights in the loss function.

### Q3: What is the difference between L1 and L2 regularization?

**Answer:** L1 regularization (Lasso) adds a penalty equal to the absolute value of the magnitude of coefficients, which can lead to sparse models (feature selection). L2 regularization (Ridge) adds a penalty equal to the square of the magnitude of coefficients, which shrinks coefficients but does not lead to sparsity.

### Q4: How do you choose the right model for a given problem?

**Answer:** Choosing the right model depends on the problem type (classification, regression, clustering), the size and quality of the data, the need for interpretability, and computational constraints. It's often helpful to start with simple models and gradually increase complexity while monitoring performance on a validation set.

### Q5: What is the purpose of cross-validation?

**Answer:** Cross-validation is a technique used to estimate how a model will perform on unseen data. It involves partitioning the data into subsets, training the model on some subsets, and validating on the remaining subsets. This helps to reduce overfitting and provides a more robust estimate of model performance.
