# Revision Pack: Outlier Detection using the Percentile Method | Winsorization Technique

**One-Line Summary:** MSE loss guides gradient descent to minimise prediction error in linear regression.

## Cheat Sheet

| Concept | Key Point |
|---|---|
| MSE Loss | \(\frac{1}{N}\sum_{i=1}^{N}(y^{(i)}-\hat{y}^{(i)})^2\) |
| Gradient w.r.t w | \(-\frac{1}{N}\sum_{i=1}^{N}(y^{(i)}-\hat{y}^{(i)})x^{(i)}\) |
| Gradient w.r.t b | \(-\frac{1}{N}\sum_{i=1}^{N}(y^{(i)}-\hat{y}^{(i)})\) |
| Update Rule | \(\theta^{(t+1)}=\theta^{(t)}-\alpha\frac{\partial L}{\partial \theta}\) |
| Learning Rate (α) | Controls step size; too large → divergence, too small → slow learning |
| Feature Scaling | Needed for stable gradients; e.g., min‑max or z‑score |
| Convergence | Stop when loss change < ε (e.g., 1e‑5) |
| Common Mistake 1 | Forget negative sign → move uphill |
| Common Mistake 2 | Large α → loss diverges or oscillates |
| Common Mistake 3 | Unnormalised features → huge gradients |
| Common Mistake 4 | Stopping too early/late → under/over‑fit |
| Initialisation | Small random values near zero |
| Code Example | Minimal Python implementing loss, gradients, and updates |

## Flashcards

### Card 1
**Q:** What does MSE measure?

**A:** The average of squared differences between true target y and predicted ŷ.

### Card 2
**Q:** Why do we square the error in MSE?

**A:** To prevent positive and negative errors from cancelling each other.

### Card 3
**Q:** What is the gradient of MSE w.r.t w?

**A:** ‑(1/N) ∑(y‑ŷ) x.

### Card 4
**Q:** What is the gradient of MSE w.r.t b?

**A:** ‑(1/N) ∑(y‑ŷ).

### Card 5
**Q:** In gradient descent, which direction do we move parameters?

**A:** Opposite to the gradient (downhill).

### Card 6
**Q:** What is the role of learning rate α?

**A:** It determines the step size; too large causes divergence, too small slows learning.

### Card 7
**Q:** What happens if we forget the negative sign in the update rule?

**A:** Parameters move uphill, increasing loss instead of decreasing it.

### Card 8
**Q:** Why is feature scaling important for gradient descent?

**A:** It keeps feature ranges similar, preventing huge gradients and unstable updates.

### Card 9
**Q:** How do we know when gradient descent has converged?

**A:** When the change in loss between successive epochs falls below a small threshold (e.g., 1e‑5).

### Card 10
**Q:** What is the purpose of the 1/2 factor in L = (1/2N)∑(y‑ŷ)^2?

**A:** It simplifies the derivative by cancelling the 2 from squaring.

### Card 11
**Q:** Which mistake involves a large learning rate?

**A:** Choosing α too large causing loss to diverge or oscillate.

### Card 12
**Q:** What is the initialisation recommendation for w and b?

**A:** Small random values near zero to start near the optimal region.

### Card 13
**Q:** How many terms are in the gradient w.r.t w?

**A:** One summation term over N examples.

### Card 14
**Q:** What does the negative sign in the gradient indicate?

**A:** It indicates the direction of steepest decrease, so we subtract the gradient.

## Quiz

#### Question 1: What is the formula for MSE?
- [0] (1/N)∑(y-ŷ)
- [1] (1/N)∑(y-ŷ)^2
- [2] ∑(y-ŷ)^2 / N^2
- [3] (1/2N)∑(y-ŷ)

#### Question 2: Why do we include the factor 1/2 in L = (1/2N)∑(y-ŷ)^2?
- [0] To make loss larger
- [1] To simplify the derivative
- [2] To normalize loss
- [3] To weight outliers

#### Question 3: Which expression represents the gradient of MSE with respect to w?
- [0] (1/N)∑(y-ŷ)
- [1] -(1/N)∑(y-ŷ)x
- [2] (1/N)∑(y-ŷ)x
- [3] -(1/N)∑(y-ŷ)

#### Question 4: If the learning rate α is too large, what typically happens?
- [0] Loss decreases faster
- [1] Model converges quickly
- [2] Loss diverges or oscillates
- [3] No change

#### Question 5: Which mistake involves not scaling input features?
- [0] Forgetting negative sign
- [1] Large learning rate
- [2] Not normalising features
- [3] Stopping early

#### Question 6: What is a typical stopping criterion for convergence in gradient descent?
- [0] Loss becomes zero
- [1] Parameters stop changing
- [2] Loss change < 1e‑5
- [3] Number of epochs = 1000

#### Question 7: In the gradient descent update rule, which symbol represents the step size?
- [0] y
- [1] α
- [2] N
- [3] w

#### Question 8: What does the negative sign in the gradient indicate?
- [0] Gradient points downhill
- [1] Parameter should be added
- [2] We move opposite to gradient direction
- [3] Learning rate is negative

#### Question 9: In the provided code, what does the line `dw = -np.sum((y - preds) * X) / len(X)` compute?
- [0] Gradient w.r.t b
- [1] Gradient w.r.t w
- [2] Loss value
- [3] Prediction error

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — MSE is defined as the average of squared errors, i.e., (1/N)∑(y-ŷ)^2.
- **Q2 Answer:** Option 1 — The 1/2 cancels the 2 from squaring, making the derivative cleaner.
- **Q3 Answer:** Option 1 — The gradient w.r.t w is -(1/N)∑(y-ŷ)x, derived from the chain rule.
- **Q4 Answer:** Option 2 — A large step size can cause the loss to explode or bounce, preventing convergence.
- **Q5 Answer:** Option 2 — Unnormalised features lead to large gradients and unstable updates.
- **Q6 Answer:** Option 2 — Convergence is usually declared when the loss change between epochs is below a tiny threshold.
- **Q7 Answer:** Option 1 — α is the learning rate, i.e., the step size for each parameter update.
- **Q8 Answer:** Option 2 — The negative sign shows we move opposite to the direction of steepest increase.
- **Q9 Answer:** Option 1 — This line computes the gradient of the loss with respect to the weight w.

## Interview Questions

### Q1: Explain MSE loss, its mathematical form, and why squaring the error is beneficial.

**Answer:** MSE loss is defined as (1/N)∑(y-ŷ)^2, where y is the true target and ŷ the model prediction. Squaring ensures all errors are positive, penalises larger errors more heavily, and makes the gradient derivation straightforward because the sign of the error no longer matters.

### Q2: Derive the gradient of MSE with respect to weight w and bias b, and explain the meaning of each term.

**Answer:** Starting from L = (1/2N)∑(y-(wx+b))^2, the partial derivative w.r.t w is -(1/N)∑(y-ŷ)x, and w.r.t b is -(1/N)∑(y-ŷ). Here (y-ŷ) is the residual (error) for each example; multiplying by x (or 1) shows how changing w or b influences the loss, and the negative sign indicates we move opposite to the gradient to decrease loss.

### Q3: Describe the gradient descent update rule and the significance of the learning rate α.

**Answer:** The update rule is θ^{(t+1)} = θ^{(t)} - α·∂L/∂θ|θ=θ^{(t)}. α (learning rate) controls the step size: a small α yields slow but stable convergence, while a large α can cause overshooting or divergence, so choosing α appropriately is crucial for efficient learning.

### Q4: What are typical pitfalls when implementing gradient descent for linear regression and how to avoid them?

**Answer:** Common pitfalls include forgetting the negative sign (moving uphill), using an overly large learning rate (causing divergence), not normalising features (leading to huge gradients), and stopping too early or too late. To avoid them, ensure the update subtracts the gradient, tune α carefully, apply feature scaling, and monitor loss change for convergence.

### Q5: How does feature scaling influence the performance of gradient descent and what methods are commonly used?

**Answer:** Feature scaling normalises input ranges, resulting in more balanced gradients and faster, stable convergence. Common scaling techniques are min‑max scaling (divide by max value) and z‑score normalisation (subtract mean, divide by standard deviation).
