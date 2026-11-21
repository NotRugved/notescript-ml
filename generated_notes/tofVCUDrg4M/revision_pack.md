# Revision Pack: Principle Component Analysis(PCA) | Part 3 | Code Example and Visualization

**One-Line Summary:** Machine Learning ke fundamentals: models, training, evaluation, aur common pitfalls ko samjho.

## Cheat Sheet

- **Supervised Learning**: labeled data se model train hota hai (classification, regression)
- **Loss Function**: model ki prediction error ko quantify karta hai (MSE, Cross‑Entropy)
- **Gradient Descent**: loss ko minimize karne ke liye parameters update karta hai (learning rate, batch size)
- **Regularization**: overfitting ko control karta hai (L1, L2, dropout)
- **Evaluation Metrics**: classification – accuracy, precision, recall, F1; regression – RMSE, R²
- **Cross‑Validation**: data ko multiple folds me split karke robust performance estimate milta hai
- **Bias‑Variance Trade‑off**: high bias → underfit, high variance → overfit
- **Feature Engineering**: scaling, encoding, interaction terms
- **Model Selection**: grid search, random search, Bayesian optimization
- **Deployment Basics**: model export (ONNX, pickle), REST API, monitoring

## Flashcards

### Card 1
**Q:** Supervised learning ka main goal kya hota hai?

**A:** Labeled data se input-output mapping learn karna.

### Card 2
**Q:** MSE ka full form aur use kya hai?

**A:** Mean Squared Error; regression models ki error ko measure karta hai.

### Card 3
**Q:** Gradient descent me learning rate ka role kya hota hai?

**A:** Step size decide karta hai jo parameters update hone ke liye liya jata hai.

### Card 4
**Q:** L2 regularization ka effect parameters par kya hota hai?

**A:** Weights ko chhota (shrink) karta hai, overfitting kam hota hai.

### Card 5
**Q:** Cross‑entropy loss kis type ke problem ke liye use hota hai?

**A:** Classification, especially binary ya multi‑class.

### Card 6
**Q:** K‑fold cross‑validation me K ka typical value kya hoti hai?

**A:** Usually 5 ya 10, lekin data size ke hisaab se adjust hota hai.

### Card 7
**Q:** Precision aur recall me se kaunsa metric class imbalance ke case me zyada useful hota hai?

**A:** Recall, kyunki false negatives ko penalize karta hai.

### Card 8
**Q:** Dropout technique ka main purpose kya hai?

**A:** Training ke dauran random neurons ko deactivate karke model ko robust banana.

### Card 9
**Q:** Feature scaling ka ek popular method kaun sa hai?

**A:** Standardization (z‑score) ya Min‑Max scaling.

### Card 10
**Q:** Bias‑variance trade‑off me high bias ka kya effect hota hai?

**A:** Model underfit hota hai, training aur test error dono high.

### Card 11
**Q:** Grid search aur random search me se kaunsa method computationally efficient hota hai?

**A:** Random search, kyunki sab combinations explore nahi karta.

### Card 12
**Q:** Bagging technique ka ek example kya hai?

**A:** Random Forest.

### Card 13
**Q:** Ensemble learning ka main advantage kya hota hai?

**A:** Multiple weak learners ko combine karke overall accuracy improve hoti hai.

### Card 14
**Q:** Model deployment ke liye commonly used format kaun sa hai?

**A:** ONNX ya pickle (Python) format.

### Card 15
**Q:** Early stopping ka purpose kya hota hai?

**A:** Validation loss increase hone par training ko rok dena, overfitting prevent karna.

## Quiz

#### Question 1: Which loss function is most suitable for multi‑class classification?
- [0] Mean Squared Error
- [1] Huber Loss
- [2] Cross‑Entropy Loss
- [3] Hinge Loss

#### Question 2: What does a high learning rate typically cause?
- [0] Faster convergence without issues
- [1] Oscillation or divergence
- [2] Better generalization
- [3] Reduced overfitting

#### Question 3: In K‑fold cross‑validation, if K = N (number of samples), what is this method called?
- [0] Hold‑out validation
- [1] Leave‑One‑Out CV
- [2] Stratified CV
- [3] Bootstrap

#### Question 4: Which regularization adds a penalty equal to the absolute value of coefficients?
- [0] L1
- [1] L2
- [2] Elastic Net
- [3] Dropout

#### Question 5: What is the main advantage of using a Random Forest over a single Decision Tree?
- [0] Less memory usage
- [1] Higher interpretability
- [2] Reduced variance
- [3] Faster training

#### Question 6: Which metric is best to evaluate a regression model when outliers are present?
- [0] RMSE
- [1] MAE
- [2] R²
- [3] Adjusted R²

#### Question 7: What does the term 'bias' refer to in the bias‑variance trade‑off?
- [0] Error due to model simplicity
- [1] Error due to data noise
- [2] Error due to over‑parameterization
- [3] Error due to training time

#### Question 8: Which technique helps to prevent overfitting by randomly dropping neurons during training?
- [0] Batch Normalization
- [1] Dropout
- [2] Early Stopping
- [3] Gradient Clipping

#### Question 9: In hyperparameter tuning, which method explores the search space more efficiently when the space is large?
- [0] Grid Search
- [1] Random Search
- [2] Manual Search
- [3] Exhaustive Search

#### Question 10: Which evaluation metric combines precision and recall into a single score?
- [0] Accuracy
- [1] F1‑Score
- [2] ROC‑AUC
- [3] Log‑Loss

### Quiz Answers & Explanations

- **Q1 Answer:** Option 2 — Cross‑Entropy loss directly models the probability distribution over multiple classes.
- **Q2 Answer:** Option 1 — A too‑high learning rate can make updates overshoot minima, leading to oscillations or divergence.
- **Q3 Answer:** Option 1 — When each fold contains a single sample, it is Leave‑One‑Out Cross‑Validation.
- **Q4 Answer:** Option 0 — L1 regularization (Lasso) uses absolute values, encouraging sparsity.
- **Q5 Answer:** Option 2 — Random Forest averages many trees, which reduces variance and improves generalization.
- **Q6 Answer:** Option 1 — MAE (Mean Absolute Error) is less sensitive to outliers compared to RMSE.
- **Q7 Answer:** Option 0 — Bias is the error introduced by approximating a real-world problem with a simplified model.
- **Q8 Answer:** Option 1 — Dropout randomly deactivates neurons, forcing the network to learn redundant representations.
- **Q9 Answer:** Option 1 — Random Search can cover a large space with fewer evaluations compared to exhaustive Grid Search.
- **Q10 Answer:** Option 1 — F1‑Score is the harmonic mean of precision and recall, balancing both.

## Interview Questions

### Q1: Explain the difference between L1 and L2 regularization and when you would prefer one over the other.

**Answer:** L1 adds a penalty equal to the absolute value of coefficients, encouraging sparsity (many weights become zero). It is useful when you suspect only a few features are truly relevant. L2 adds a penalty equal to the squared value of coefficients, shrinking them uniformly but rarely making them exactly zero. L2 is preferred when you want to keep all features but reduce their impact, and it often leads to more stable solutions.

### Q2: What is the bias‑variance trade‑off and how does it affect model selection?

**Answer:** Bias is error from erroneous assumptions in the learning algorithm (under‑fitting), while variance is error from sensitivity to small fluctuations in the training set (over‑fitting). A good model balances both: low enough bias to capture patterns and low enough variance to generalize. Model complexity, regularization, and data size are tools to navigate this trade‑off.

### Q3: How does early stopping work and why is it useful?

**Answer:** Early stopping monitors validation loss during training. When the loss stops improving for a predefined number of epochs (patience), training halts and the best model so far is retained. It prevents over‑fitting, reduces training time, and often yields a model with better generalization.

### Q4: Describe how cross‑validation helps in model evaluation and hyperparameter tuning.

**Answer:** Cross‑validation splits data into K folds. The model trains on K‑1 folds and validates on the remaining fold, repeating K times. This provides a robust estimate of performance across different data subsets, reduces variance of the evaluation metric, and helps select hyperparameters that generalize well rather than over‑fitting to a single train‑test split.

### Q5: What are ensemble methods and why do they often outperform single models?

**Answer:** Ensemble methods combine predictions from multiple base learners to produce a final prediction (e.g., bagging, boosting, stacking). They reduce variance (bagging), bias (boosting), or both, by leveraging the strengths of diverse models. The aggregated result is usually more accurate and robust than any individual model.
