# Handling Mixed Variables | Feature Engineering

**Video Link:** [https://www.youtube.com/watch?v=9xiX-I5_LQY](https://www.youtube.com/watch?v=9xiX-I5_LQY)

**Summary:** Linear Regression mein hum MSE cost function ko minimize karne ke liye Gradient Descent use karte hain, jahan learning rate aur feature scaling convergence ki speed aur stability decide karte hain.

## Theory

### Linear Regression kya hai ([00:00](https://youtu.be/9xiX-I5_LQY?t=0))

### What it is
Linear regression ek supervised learning model hai jismein input features (X) ko linearly combine karke target variable (y) ki prediction ki jaati hai.

### Why it is needed
- To model the linear relationship between one or more features and a continuous target.
- Provides a simple baseline for more complex models.

### Step‑by‑step working
1. **Define hypothesis**: \( h_\theta(x) = \theta_0 + \theta_1 x \) (for single feature) or \( h_\theta(x) = \theta^T x \) (for multiple features). 
2. **Parameter vector**: \( \theta = [\theta_0, \theta_1, \dots, \theta_n] \) where \( \theta_0 \) is the intercept (bias) and \( \theta_i \) are the weights for each feature.
3. **Learning**: Use training data \( (X^{(i)}, y^{(i)}) \) to adjust \( \theta \) so that predictions match the true targets.

### Math with meaning of every symbol
- \( h_\theta(x) \) – the model's prediction for input \( x \).
- \( \theta_0 \) – bias term (intercept) that shifts the line up/down.
- \( \theta_1 \) – slope (weight) indicating how much y changes per unit change in x.
- \( x \) – feature vector (could be a single number or multiple numbers).
- \( y \) – actual target value observed in the data.
- \( \theta \) – vector of learnable parameters that the algorithm will optimize.

### Cost Function (Loss) definition ([01:30](https://youtu.be/9xiX-I5_LQY?t=90))

### What it is
Cost function \( J(\theta) \) quantifies the error between predicted and true values. For linear regression we use Mean Squared Error (MSE):

\( J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})^2 \)

### Why it is needed
- Provides a single scalar measure of how well the model fits the data.
- The learning algorithm (gradient descent) aims to **minimize** this cost.

### Step‑by‑step
1. Compute prediction \( h_\theta(x^{(i)}) \) for each training example.
2. Subtract the true target \( y^{(i)} \) to get the error.
3. Square the error to penalize large deviations.
4. Sum all squared errors and divide by \( 2m \) (average over examples).

### Math with meaning of every symbol
- \( m \) – number of training examples.
- \( \theta \) – model parameters being optimized.
- \( h_\theta(x^{(i)}) \) – predicted value for the i‑th example.
- \( y^{(i)} \) – actual target value for the i‑th example.
- \( (h_\theta(x^{(i)}) - y^{(i)})^2 \) – squared error for example i.
- \( \frac{1}{2m} \) – scaling factor to keep the gradient values manageable.

### Gradient Descent intuition ([03:00](https://youtu.be/9xiX-I5_LQY?t=180))

### What it is
Gradient descent ek iterative optimization algorithm hai jismein hum \( \theta \) ko step‑by‑step update karte hain jisse cost \( J(\theta) \) kam ho.

### Why it is needed
- For many models the cost function is not easily minimized analytically, so we use an iterative numeric method.

### Plain‑language 'samajh'
Jaise koi chhote‑chhote qadam chalakar chhaye ki taraf chalta hai, wahi yahan hum \( \theta \) ko chhote‑chhote adjustments karte hain – har qadam se hum uss direction mein jate hain jismein loss kam ho.

### Step‑by‑step
1. Compute the gradient \( \nabla J(\theta) \) – direction of steepest **increase** of the cost.
2. Move opposite to this gradient: \( \theta \leftarrow \theta - \alpha \nabla J(\theta) \).
3. Repeat until the change in \( \theta \) (or the cost) becomes negligible.

### Math with meaning of every symbol
- \( \nabla J(\theta) \) – vector of partial derivatives \( \frac{\partial J}{\partial \theta_j} \) for each parameter.
- \( \alpha \) – learning rate (step size); controls how big each update is.
- \( \theta_j \) – the j‑th parameter of the model.
- Update rule: \( \theta_j \leftarrow \theta_j - \alpha \frac{\partial J}{\partial \theta_j} \).

### Update Rule derivation ([05:00](https://youtu.be/9xiX-I5_LQY?t=300))

### What it is
Derivation of the gradient for linear regression cost to obtain the exact update rule for each parameter.

### Why it is needed
- Shows precisely how each parameter influences the loss, ensuring the update moves in the correct direction.

### Step‑by‑step
1. Write the cost for linear regression: \( J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} (\theta_0 + \theta_1 x^{(i)} - y^{(i)})^2 \).
2. Partial derivative w.r.t \( \theta_0 \): \( \frac{\partial J}{\partial \theta_0} = \frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)}) \).
3. Partial derivative w.r.t \( \theta_1 \): \( \frac{\partial J}{\partial \theta_1} = \frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)}) x^{(i)} \).
4. Plug these into the gradient descent update.

### Math with meaning of every symbol
- \( \frac{\partial J}{\partial \theta_0} \) – how much the cost changes if we tweak the intercept.
- \( \frac{\partial J}{\partial \theta_1} \) – how much the cost changes if we tweak the slope.
- \( \alpha \) – learning rate controlling step magnitude.
- Update for \( \theta_0 \): \( \theta_0 \leftarrow \theta_0 - \alpha \frac{1}{m} \sum (h_\theta(x) - y) \).
- Update for \( \theta_1 \): \( \theta_1 \leftarrow \theta_1 - \alpha \frac{1}{m} \sum (h_\theta(x) - y) x \).

### Code implementation (on-screen) ([06:30](https://youtu.be/9xiX-I5_LQY?t=390))

### What it is
Python code using NumPy to perform gradient descent on a simple linear regression model.

### Why it is needed
- To see a concrete implementation of the math derived earlier.
- Helps verify that the algorithm works on real data.

### Step‑by‑step explanation
1. **Import** NumPy for array operations.
2. **Define** sample feature matrix `X` (including a column of 1s for the intercept) and target vector `y`.
3. **Initialize** parameter vector `theta` to zeros – start with no knowledge.
4. Set **hyperparameters**: learning rate `alpha` and number of iterations `epochs`.
5. **Loop** over epochs:
   - Compute predictions: `predictions = X @ theta`.
   - Compute error: `error = predictions - y`.
   - Compute gradient: `(1/m) * X.T @ error` (vectorized form of the derivative).
   - Update `theta` using the gradient.
6. Print the learned parameters after training.

### Code (on-screen)
```python
import numpy as np

# Sample data
X = np.array([[1, 2],   # bias term + feature
               [2, 3],
               [4, 5]])

y = np.array([5, 7, 9])

# Initialize parameters (theta0, theta1)
theta = np.zeros(2)

# Hyperparameters
alpha = 0.01          # learning rate
m = X.shape[0]      # number of training examples
epochs = 1000

for _ in range(epochs):
    predictions = X @ theta               # h_the(x)
    error = predictions - y               # residuals
    gradient = (1/m) * X.T @ error        # ∂J/∂θ
    theta = theta - alpha * gradient        # θ ← θ - α∇J

print("Learned theta:", theta)
```

## Intuition

- ([04:30](https://youtu.be/9xiX-I5_LQY?t=270)) Gradient descent ko chhote-chhote qadam chalakar chhaye ki taraf chalta hai, jaise koi hilly terrain mein chhote-chhote qadam chalakar neeche ki taraf ja raha ho. Har qadam se hum uss side se jismein zyada drop hua, is tarah hi hum θ ko uss direction mein update karte hain jismein loss kam ho.

## Code

### Linear regression gradient descent (on-screen) [on-screen] ([06:30](https://youtu.be/9xiX-I5_LQY?t=390))
Python code using NumPy to perform gradient descent on linear regression. Each line is explained in the preceding text.

```python
import numpy as np

# Sample data
X = np.array([[1, 2],   # bias term + feature
               [2, 3],
               [4, 5]])

y = np.array([5, 7, 9])

# Initialize parameters (theta0, theta1)
theta = np.zeros(2)

# Hyperparameters
alpha = 0.01          # learning rate
m = X.shape[0]      # number of training examples
epochs = 1000

for _ in range(epochs):
    predictions = X @ theta               # h_the(x)
    error = predictions - y               # residuals
    gradient = (1/m) * X.T @ error        # ∂J/∂θ
    theta = theta - alpha * gradient        # θ ← θ - α∇J

print("Learned theta:", theta)
```

## Analogies

- ([04:30](https://youtu.be/9xiX-I5_LQY?t=270)) **Analogy:** Gradient descent ko chhote-chhote qadam chalakar chhaye ki taraf chalta hai, jaise koi hilly terrain mein chhote-chhote qadam chalakar neeche ki taraf ja raha ho. Har qadam se uss side se jismein zyada drop hua. — *Explains:* Is tarah samajh aata hai ki humko cost ki higher side (steepest ascent) ki taraf nahi, balki uski opposite direction (steepest descent) mein jaana hai, jismein har step se hum loss kam kar rahe hain.

## Common Mistakes

- **Mistake [teacher]:** Learning rate (α) bohot zyada rakhna ([08:30](https://youtu.be/9xiX-I5_LQY?t=510))
  - *Why:* Bade step size se parameter values bohot jaldi change karte hain, is wajah se cost diverge ho jata hai ya NaN mil jata hai.
  - *Fix:* Learning rate ko kam karo (e.g., 0.001 ya 0.01) ya use adaptive learning rate techniques jaisi learning rate decay.
- **Mistake [teacher]:** Feature scaling nahi karna ([08:50](https://youtu.be/9xiX-I5_LQY?t=530))
  - *Why:* Jab koi feature ki scale doosre se bahut alag ho, gradient descent ki convergence bahut slow hoti hai ya phir kabhi kabhi fail bhi ho jata hai.
  - *Fix:* Features ko normalize ya standardize karo (mean=0, std=1) ya use min-max scaling, jisse gradient descent faster converge kare.
- **Mistake [teacher]:** θ ko sirf zero initialize karna ([09:10](https://youtu.be/9xiX-I5_LQY?t=550))
  - *Why:* Zero initialization se sabhi parameter ek hi direction mein update hote hain, is wajah se algorithm slow converge karta hai ya local minimum mein phas jata hai.
  - *Fix:* θ ko small random values se initialize karo (e.g., np.random.randn * 0.01) تاکि har parameter ko alag-alag direction se seekhne ki opportunity milti rahe.

## Formulas & Key Terms

### Formulas
- **Mean Squared Error (MSE) cost function:** `J(θ) = \frac{1}{2m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})^2` — J(θ) ek scalar value hai jo model ke predictions aur actual targets ke beech ki average squared error ko measure karta hai; lower value matlab better model.
- **Gradient descent update rule:** `θ_j ← θ_j - α \frac{∂J}{∂θ_j}` — Har parameter θ_j ko uss direction mein update karte hain jismein uski derivative (gradient) negative ho, aur α learning rate step size control karta hai.
- **Partial derivative of MSE w.r.t θ_0:** `∂J/∂θ_0 = \frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})` — Yeh derivative dikhata hai ki agar intercept (bias) badhaya jaye toh cost kitni barh jayegi.
- **Partial derivative of MSE w.r.t θ_1:** `∂J/∂θ_1 = \frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)}) x^{(i)}` — Yeh derivative dikhata hai ki agar slope (weight) badhaya jaye toh har example ki error ko uske x se multiply karke cost badh jayegi.

### Key Terms
- **Linear regression:** Ek supervised learning model jismein target variable ko input features ke linear combination se predict ki jaati hai.
- **Hypothesis (h_θ):** Model ki function jo input ko output me convert kare, general form h_θ(x) = θ^T x.
- **Cost function (J):** Ek scalar measure jo model ke predictions aur actual targets ke beech ki error ko quantify karta hai.
- **Gradient descent:** Iterative optimization algorithm jo parameters ko opposite direction of gradient jaakar cost ko minimize karta hai.
- **Learning rate (α):** Gradient descent mein step size control karta hai; bohot bada ya bohot chhota hona algorithm ki convergence ko affect karta hai.
- **Feature scaling:** Features ko same scale mein laana (normalize/standardize) jisse gradient descent faster aur stable converge kare.
- **Parameter (θ):** Model ki seekhne lablee value, jaise weight ya bias, jo algorithm by update process ke through adjust hota hai.
