# Outlier Detection using the Percentile Method | Winsorization Technique

**Video Link:** [https://www.youtube.com/watch?v=bcXA4CqRXvM](https://www.youtube.com/watch?v=bcXA4CqRXvM)

**Summary:** MSE loss guides gradient descent to minimise prediction error in linear regression.

## Theory

### Unclear ([00:00](https://youtu.be/bcXA4CqRXvM?t=0))

unclear in video

### Mean Squared Error (MSE) Loss Function ([10:00](https://youtu.be/bcXA4CqRXvM?t=600))

### What it is
- MSE is a **loss function** used to measure how far the predicted values \(\hat{y}\) are from the true target values \(y\).
- It squares the error so that positive and negative errors do not cancel each other out.

### Why it is needed
- Provides a single scalar value to optimise the model parameters (\(w\) and \(b\)).
- The goal of training is to **minimise** this loss.

### Step‑by‑step
1. For a single data point, error = \(y - \hat{y}\).
2. Square the error: \((y - \hat{y})^2\).
3. Average over the whole training set of \(N\) points:
   \[\text{MSE} = \frac{1}{N}\sum_{i=1}^{N}(y^{(i)} - \hat{y}^{(i)})^2\]

### Math with meaning of symbols
- \(y^{(i)}\): actual target value for the \(i\)-th example.
- \(\hat{y}^{(i)} = wx^{(i)} + b\): model prediction for the \(i\)-th example.
- \(N\): total number of training examples.
- The summation \(\sum\) adds the squared errors across all examples.
- Division by \(N\) gives the average error.

---

### Partial Derivative of MSE w.r.t Parameters \(w\) and \(b\) ([10:30](https://youtu.be/bcXA4CqRXvM?t=630))

### What it is
- To apply **gradient descent**, we need the gradient of the loss w.r.t each parameter.
- The gradient is a vector of partial derivatives.

### Derivation (step‑by‑step)
1. Write MSE without the averaging constant (constant factor does not affect optimisation):
   \[L(w,b) = \frac{1}{2N}\sum_{i=1}^{N}(y^{(i)} - (wx^{(i)} + b))^2\]
   (the \(\frac{1}{2}\) makes the derivative cleaner).
2. Partial derivative w.r.t \(w\):
   \[\frac{\partial L}{\partial w} = \frac{1}{N}\sum_{i=1}^{N}(y^{(i)} - (wx^{(i)} + b))\cdot(-x^{(i)})\]
   = \(-\frac{1}{N}\sum_{i=1}^{N}(y^{(i)} - \hat{y}^{(i)})x^{(i)}\)
3. Partial derivative w.r.t \(b\):
   \[\frac{\partial L}{\partial b} = \frac{1}{N}\sum_{i=1}^{N}(y^{(i)} - (wx^{(i)} + b))\cdot(-1)\)
   = \(-\frac{1}{N}\sum_{i=1}^{N}(y^{(i)} - \hat{y}^{(i)})\)

### Meaning of symbols
- \(\frac{\partial L}{\partial w}\): how the loss changes if we increase \(w\) a little.
- \(x^{(i)}\): input feature for the \(i\)-th example.
- The negative sign shows that we move **opposite** to the direction of increase.

---

### Gradient Descent Update Rule ([11:00](https://youtu.be/bcXA4CqRXvM?t=660))

### What it is
- Gradient descent is an **optimization algorithm** that iteratively updates parameters to reduce the loss.

### Update equations
- For parameter \(\theta\) (could be \(w\) or \(b\)):
   \[\theta^{(t+1)} = \theta^{(t)} - \alpha \cdot \frac{\partial L}{\partial \theta}\bigg|_{\theta = \theta^{(t)}}\]
- \(\alpha\) is the **learning rate** (step size).

### Step‑by‑step
1. Initialise \(w\) and \(b\) (e.g., random small values).
2. Compute the gradients \(\frac{\partial L}{\partial w}\) and \(\frac{\partial L}{\partial b}\) using the formulas above.
3. Update:
   \[w^{(t+1)} = w^{(t)} - \alpha \frac{\partial L}{\partial w}\]
   \[b^{(t+1)} = b^{(t)} - \alpha \frac{\partial L}{\partial b}\]
4. Repeat until convergence (loss stops decreasing significantly).

### Meaning of symbols
- \(\theta^{(t)}\): value of the parameter at iteration \(t\).
- \(\alpha\): learning rate, controls how big each step is.
- \(\frac{\partial L}{\partial \theta}\) is the gradient at the current parameters.

---

### Intuition behind Gradient Descent ([12:00](https://youtu.be/bcXA4CqRXvM?t=720))

### Teacher's plain‑language explanation
- **Analogy**: Imagine you are standing on a hilly terrain and want to reach the lowest valley (minimum loss). The **slope** under your feet tells you which direction is downhill. You take steps **opposite** to the slope (downhill) with a certain **step size** (\(\alpha\)).
- If the step is too big, you might **overshoot** the valley and bounce around. If the step is too small, you **wander** for a long time.
- The process continues until the slope becomes almost zero – that's when the loss stops improving, meaning we have **converged**.

---

### Implementation of Gradient Descent for Linear Regression (on‑screen code) ([13:00](https://youtu.be/bcXA4CqRXvM?t=780))



### Common Mistakes in Gradient Descent ([14:30](https://youtu.be/bcXA4CqRXvM?t=870))

### Mistake 1: Forgetting the negative sign in the update rule
- **Why it happens**: Learners copy the derivative but overlook that gradient descent moves **opposite** to the gradient.
- **Fix**: Always subtract the gradient (i.e., `param = param - alpha * grad`).

### Mistake 2: Choosing a learning rate \(\alpha\) that is too large
- **Why it happens**: Expecting fast progress, they set a big \(\alpha\), causing the loss to diverge or oscillate.
- **Fix**: Start with a small \(\alpha\) (e.g., 0.01) and increase only if loss plateaus.

### Mistake 3: Not normalising input features
- **Why it happens**: Features with large ranges cause huge gradients, making updates unstable.
- **Fix**: Apply feature scaling (e.g., divide by max value) before training.

### Mistake 4: Stopping too early or too late
- **Why it happens**: No convergence criterion; either quit prematurely (under‑fitting) or run forever (wasteful).
- **Fix**: Monitor the loss curve; stop when the change in loss between epochs falls below a tiny threshold (e.g., 1e‑5).

---

## Intuition

- ([00:00](https://youtu.be/bcXA4CqRXvM?t=0)) unclear in video
- ([12:00](https://youtu.be/bcXA4CqRXvM?t=720)) Gradient descent is like rolling a ball down a hill: you look at the slope (gradient) and take steps opposite to it, with the step size controlled by the learning rate.

## Code

### Simple Gradient Descent for Linear Regression [on-screen] ([13:00](https://youtu.be/bcXA4CqRXvM?t=780))
Python implementation shown on screen. It defines a loss function, computes gradients analytically, and updates parameters using the learning rate. The code is minimal and directly reflects the formulas derived earlier.

```python
import numpy as np

def compute_loss(X, y, w, b):
    N = len(y)
    preds = w * X + b
    loss = np.sum((y - preds) ** 2) / (2 * N)
    return loss

def gradient_descent(X, y, w_init, b_init, alpha, epochs):
    w, b = w_init, b_init
    for i in range(epochs):
        preds = w * X + b
        dw = -np.sum((y - preds) * X) / len(X)
        db = -np.sum(y - preds) / len(X)
        w = w - alpha * dw
        b = b - alpha * db
    return w, b

# Example usage
X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])
w_init, b_init = 0.0, 0.0
alpha = 0.01
epochs = 1000
w_final, b_final = gradient_descent(X, y, w_init, b_init, alpha, epochs)
print('Learned w:', w_final, 'b:', b_final)
```

## Analogies

- ([12:30](https://youtu.be/bcXA4CqRXvM?t=750)) **Analogy:** Rolling a ball down a hill to reach the lowest point (minimum loss). — *Explains:* The slope of the hill at any position is the gradient; moving opposite to the slope (downhill) with an appropriate step size (learning rate) leads to the valley (optimal parameters).

## Common Mistakes

- **Mistake [teacher]:** Forgetting the negative sign in the update rule ([14:30](https://youtu.be/bcXA4CqRXvM?t=870))
  - *Why:* Learners overlook that gradient descent moves opposite to the gradient direction.
  - *Fix:* Always subtract the gradient: `param = param - alpha * grad`.
- **Mistake [teacher]:** Choosing a learning rate that is too large ([14:45](https://youtu.be/bcXA4CqRXvM?t=885))
  - *Why:* A big step size causes the loss to diverge or oscillate, preventing convergence.
  - *Fix:* Start with a small learning rate (e.g., 0.01) and adjust only after checking the loss curve.
- **Mistake [teacher]:** Not normalising input features ([15:00](https://youtu.be/bcXA4CqRXvM?t=900))
  - *Why:* Large‑scale features produce large gradients, making updates unstable and slow.
  - *Fix:* Scale inputs (e.g., divide by max value) before training.
- **Mistake [teacher]:** Stopping too early or too late ([15:15](https://youtu.be/bcXA4CqRXvM?t=915))
  - *Why:* Without a convergence criterion, you may quit before the model has learned or waste time on unnecessary epochs.
  - *Fix:* Monitor loss change; stop when the decrease between consecutive epochs is below a small threshold (e.g., 1e‑5).

## Formulas & Key Terms

### Formulas
- **Mean Squared Error (MSE) Loss:** `\(\text{MSE} = \frac{1}{N}\sum_{i=1}^{N}(y^{(i)} - \hat{y}^{(i)})^2\)` — Average of squared differences between true target \(y\) and predicted \(\hat{y}\).
- **Gradient of MSE w.r.t w:** `\(\frac{\partial L}{\partial w} = -\frac{1}{N}\sum_{i=1}^{N}(y^{(i)} - (wx^{(i)} + b))x^{(i)}\)` — How loss changes with respect to weight \(w\); negative sign indicates descent direction.
- **Gradient of MSE w.r.t b:** `\(\frac{\partial L}{\partial b} = -\frac{1}{N}\sum_{i=1}^{N}(y^{(i)} - (wx^{(i)} + b))\)` — How loss changes with respect to bias \(b\); again negative for descent.
- **Gradient Descent Update Rule:** `\(\theta^{(t+1)} = \theta^{(t)} - \alpha \frac{\partial L}{\partial \theta}\bigg|_{\theta = \theta^{(t)}}\)` — Update each parameter \(\theta\) by moving opposite to the gradient scaled by learning rate \(\alpha\).

### Key Terms
- **Loss function:** A numeric measure (e.g., MSE) that quantifies how well a model's predictions match the true targets; we aim to minimise it.
- **Gradient:** A vector of partial derivatives of the loss with respect to each parameter; points in the direction of steepest increase.
- **Learning rate (α):** Step size for each gradient descent update; controls how quickly parameters move toward the minimum.
- **Convergence:** When the loss stops decreasing significantly, indicating that the parameters have reached (or approximated) the optimum.
- **Feature scaling:** Normalising input features to a similar range to ensure stable and fast gradient descent.
