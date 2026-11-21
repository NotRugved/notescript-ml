# Principle Component Analysis  (PCA) | Part 1 | Geometric Intuition

**Video Link:** [https://www.youtube.com/watch?v=iRbsBi5W0-c](https://www.youtube.com/watch?v=iRbsBi5W0-c)

**Summary:** Gradient Descent ek iterative optimization technique hai jo loss ko minimize karne ke liye parameters ko learning rate ke saath opposite gradient direction mein update karti hai.

## Theory

### What is Gradient Descent? ([10:00](https://youtu.be/iRbsBi5W0-c?t=600))

### Definition
Gradient Descent ek **optimization algorithm** hai jo ek **loss function** (cost function) ko **minimize** karne ke liye iteratively **parameters** (θ) ko update karta hai.

### Why it is needed
- In supervised learning humein ek model milana chahiye jo **minimum error** (loss) wala ho.
- Directly solving loss ke samane mein (jaise closed-form solution) general case mein mushkil ya asambhal hai, isliye hum iterative method use karte hain.

### Step‑by‑step working
1. **Initialize** parameters θ (random ya zero).
2. **Compute** gradient of loss J(θ) w.r.t each parameter: \(\nabla_\theta J(θ)\).
3. **Update** parameters in the direction opposite to gradient:
   \[θ \leftarrow θ - α \nabla_\theta J(θ)\]
4. **Repeat** steps 2‑3 until convergence (loss stops decreasing significantly).

### Mathematics
- **Loss function** (Mean Squared Error example):
  \[J(θ) = \frac{1}{m} \sum_{i=1}^{m} (h_θ(x^{(i)}) - y^{(i)})^2\]
- **Gradient** (for a single parameter θ_j):
  \[\frac{\partial J(θ)}{\partial θ_j} = \frac{1}{m} \sum_{i=1}^{m} 2 (h_θ(x^{(i)}) - y^{(i)}) \frac{\partial h_θ(x^{(i)})}{\partial θ_j}\]
- **Update rule**:
  \[θ_j^{(t+1)} = θ_j^{(t)} - α \frac{\partial J(θ^{(t)})}{\partial θ_j}\]

### Meaning of symbols
- \(θ\): model parameters (weights).
- \(α\): learning rate (step size).
- \(\nabla_\theta J(θ)\): gradient of loss w.r.t parameters (points toward steepest increase).
- \(t\): iteration number.
- \(m\): number of training examples.
- \(h_θ(x)\): hypothesis/prediction for input \(x\).

### Loss Function and Cost ([11:30](https://youtu.be/iRbsBi5W0-c?t=690))

### What is a Loss / Cost Function?
- **Loss function** ek scalar value hai jo **model ke predictions** aur **true labels** ke beech ka fark dikhata hai.
- Purpose: **quantify error** so that hum isse minimize kar sakte hain.

### Common choices (teacher covered)
- **Mean Squared Error (MSE)** – use for regression.
- **Logistic Loss** – use for classification.

### Why we need it
- Bina kisi scalar metric ke, hum **gradient** compute nahi kar sakte.
- Cost function humein **objective** deta hai jo optimization algorithm (gradient descent) ko guide karta hai.

### Mathematics
- General form:
  \[J(θ) = \frac{1}{m} \sum_{i=1}^{m} L(h_θ(x^{(i)}), y^{(i)})\]
- For MSE, \(L = (h_θ(x) - y)^2\) (square loss).
- The factor \(\frac{1}{2}\) is often added (as in many textbooks) to cancel the 2 from the square, making derivative cleaner:
  \[J(θ) = \frac{1}{2m} \sum_{i=1}^{m} (h_θ(x^{(i)}) - y^{(i)})^2\]

### Meaning of symbols
- \(m\): total number of training samples.
- \(h_θ(x)\): model prediction for input \(x\) given parameters \(θ\).
- \(L\): loss term for a single example (e.g., squared error).

### Update Rule and Mathematics ([13:00](https://youtu.be/iRbsBi5W0-c?t=780))

### Gradient Descent Update Rule
- **Core idea**: parameters move **opposite** to the direction of greatest increase of loss (steepest descent).

### Derivation (step‑by‑step)
1. Compute gradient \(\nabla_θ J(θ)\) – vector of partial derivatives.
2. Choose learning rate \(α\) (step size).
3. Update each parameter:
   \[θ_j^{(t+1)} = θ_j^{(t)} - α \frac{∂J(θ^{(t)})}{∂θ_j}\]
4. Repeat until convergence.

### Mathematics details
- For a single parameter \(θ\):
  \[θ^{(t+1)} = θ^{(t)} - α ∇_θ J(θ^{(t)})\]
- In vector form (used in code):
  \[θ \leftarrow θ - α ∇_θ J(θ)\]

### Meaning of symbols
- \(θ_j^{(t)}\): value of parameter \(θ_j\) at iteration \(t\).
- \(α\): learning rate, controls step magnitude.
- \(\frac{∂J}{∂θ_j}\): how much loss changes if we increase \(θ_j\) a little.
- The **negative sign** ensures we move **down** the loss surface.

### Why this works
- If loss is convex, this iterative step guarantees that each update reduces (or at least does not increase) the loss, leading to a minimum.

### Learning Rate and its Effect ([15:00](https://youtu.be/iRbsBi5W0-c?t=900))

### Learning Rate (α) – what it is
- \(α\) **step size** hyperparameter that decides how far we move in the direction of the negative gradient.

### Effects of different values
| α (learning rate) | Effect on training |
|-------------------|-------------------|
| **Very small** (e.g., 0.001) | Very slow convergence; may take many iterations to reach minimum. |
| **Moderate** (e.g., 0.01‑0.1) | Reasonable speed; loss decreases steadily. |
| **Very large** (e.g., 1.0) | Loss may **diverge** (oscillate or go to infinity) because steps are too big and overshoot the minimum. |

### How to choose
1. Start with a small value (e.g., 0.01).
2. Observe loss curve:
   - If loss plateaus quickly → increase α.
   - If loss spikes or becomes NaN → decrease α.
3. Optionally use **learning rate schedules** (decrease α over time).

### Mathematics reminder
- Update rule still contains α:
  \[θ^{(t+1)} = θ^{(t)} - α ∇_θ J(θ^{(t)})\]
- α multiplies the gradient; larger α → larger step.

### Why it matters
- α controls **speed vs stability** trade‑off; picking right value is crucial for convergence.

### Batch vs Stochastic Gradient Descent ([17:30](https://youtu.be/iRbsBi5W0-c?t=1050))

### Batch Gradient Descent
- **Definition**: Compute gradient using **entire training dataset**.
- **Pros**: Exact gradient → more stable, often faster convergence per iteration.
- **Cons**: Computationally expensive for large datasets (need to pass through all data each iteration).

### Stochastic Gradient Descent (SGD)
- **Definition**: Compute gradient using **a single randomly selected training example** (or a small mini‑batch).
- **Pros**: Noisy but **faster per iteration**, can escape shallow local minima, less memory.
- **Cons**: Gradient estimate is noisy → convergence may be slower or oscillatory.

### Mini‑batch Gradient Descent (often used)
- Compromise: use a small batch (e.g., 32‑256 examples) to get a slightly less noisy gradient while still being efficient.

### Mathematics
- **Batch gradient**:
  \[∇_θ J_{batch}(θ) = \frac{1}{m} \sum_{i=1}^{m} ∂/∂θ (h_θ(x_i) - y_i)^2\]
- **Stochastic gradient** (for example i):
  \[∇_θ J_{stoch}(θ) = ∂/∂θ (h_θ(x_i) - y_i)^2\]

### Meaning of symbols
- \(m\): total number of training examples.
- \(i\): index of a particular training example.
- The **difference** between batch and stochastic is the **scale** of the sum (full sum vs single term).

### Introduction to Gradient Descent ([30:00](https://youtu.be/iRbsBi5W0-c?t=1800))

Gradient descent ek optimization algorithm hai jo machine learning models mein loss function ko minimize karne ke liye use hota hai. Iska main goal hai weights aur biases ko aise update karna ki prediction aur actual value ke beech ka difference (loss) kam ho jaye. Ye algorithm iterative process hai, jisme har step par parameters thode thode adjust kiye jate hain.

### Understanding the Gradient ([30:45](https://youtu.be/iRbsBi5W0-c?t=1845))

Gradient ek vector hai jo loss function ke respect mein parameters (weights) ke partial derivatives ko represent karta hai. Mathematically, gradient = [dL/dw1, dL/dw2, ..., dL/dwn]. Ye batata hai ki loss function kis direction mein sabse tez badh raha hai. Gradient descent mein hum gradient ke opposite direction mein move karte hain taaki loss kam ho sake. Isse descent direction kehte hain.

### Learning Rate Concept ([31:30](https://youtu.be/iRbsBi5W0-c?t=1890))

Learning rate (alpha) ek hyperparameter hai jo har step mein weights kitne update honge, ye decide karta hai. Update rule hai: w_new = w_old - alpha * gradient. Agar learning rate bahut chhota hai, toh convergence slow hogi. Agar bahut bada hai, toh model loss function ke minimum ko cross karke diverge ho sakta hai. Ideal learning rate aisa hona chahiye jo stable aur fast convergence de.

### Batch vs Mini-batch vs Stochastic Gradient Descent ([32:15](https://youtu.be/iRbsBi5W0-c?t=1935))

Gradient descent ke 3 main variants hain: 1. Batch GD: Poore dataset par gradient calculate karte hain har epoch mein. Ye slow hai lekin stable. 2. Mini-batch GD: Dataset ko chhote batches mein divide karte hain. Ye balance hai speed aur stability ke beech. 3. Stochastic GD: Har single sample par gradient calculate karte hain. Ye fast hai lekin noisy convergence deta hai. Practical mein mini-batch GD sabse zyada use hota hai.

### Convergence and Loss Curve ([33:00](https://youtu.be/iRbsBi5W0-c?t=1980))

Convergence ka matlab hai ki loss function ek stable value par pahunch jaye aur further improvement na ho. Loss curve plot karke hum dekh sakte hain ki model sahi direction mein converge ho raha hai ya nahi. Agar loss curve oscillate kar raha hai, toh learning rate zyada hai. Agar loss curve bahut slowly kam ho raha hai, toh learning rate kam hai. Proper tuning se hum smooth convergence achieve kar sakte hain.

## Intuition

- ([10:30](https://youtu.be/iRbsBi5W0-c?t=630)) Gradient descent ko samajhna hai jaise kisi ghat (hill) ke niche chalte hue; aap apni chalti ki direction feel karte hain aur uske opposite direction mein qadam uthe hain.
- ([13:20](https://youtu.be/iRbsBi5W0-c?t=800)) Learning rate ko walking ki qadam ki tarah samajhiye; bohot badi qadam (large α) se aap niche se utha kar niche tak pahunch sakte hain lekin overshoot ho kar wapas uth kar nikal sakte hain, jaldi kam qadam (small α) se aap dheere dheere niche tak pahunchte hain.
- ([16:00](https://youtu.be/iRbsBi5W0-c?t=960)) Batch gradient descent tarah hai jaise poore hill ki suraksha ki tarah, jisme har qadam full data se nikalta hai, jismein stochastic tarah hai jaise har qadam ek pair ki feel se nikalta hai.
- ([30:15](https://youtu.be/iRbsBi5W0-c?t=1815)) Socho aap andhere mein ek pahadi se neeche utar rahe ho. Aap sirf apne pairon ke neeche ki slope feel kar sakte ho. Gradient descent bilkul waisa hi hai - hum loss function ki surface par khade hain aur gradient humein batata hai ki kis direction mein slope sabse tez neeche ja raha hai. Hum usi direction mein chhota sa step lete hain aur baar baar repeat karte hain jab tak hum valley (minimum) tak na pahunch jayein.
- ([31:45](https://youtu.be/iRbsBi5W0-c?t=1905)) Learning rate ko aap apne step size se compare kar sakte ho. Agar aap bahut chhote steps lete ho, toh valley tak pahunchne mein bahut time lagega. Agar aap bahut bade steps lete ho, toh aap valley ko cross karke doosri taraf chala jaoge aur phir wapas aana padega. Ideal step size aisa hona chahiye jo aapko efficiently valley tak le jaye bina oscillate kiye.

## Code

### Gradient Descent Implementation [on-screen] ([18:00](https://youtu.be/iRbsBi5W0-c?t=1080))
```python
import numpy as np

def compute_loss(X, y, theta):
    """Calculate Mean Squared Error loss."""
    m = len(y)
    predictions = X.dot(theta)          # hθ(x) = X·θ
    loss = np.sum((predictions - y) ** 2) / (2 * m)  # 1/2 factor for cleaner derivative
    return loss

def gradient_descent(X, y, theta, alpha, iterations):
    """Perform batch gradient descent."""
    m = len(y)
    for _ in range(iterations):
        predictions = X.dot(theta)          # forward pass
        error = predictions - y            # residuals
        gradient = (X.T.dot(error)) / m    # ∂J/∂θ
        theta = theta - alpha * gradient    # parameter update
    return theta
```

```python
import numpy as np

def compute_loss(X, y, theta):
    """Calculate Mean Squared Error loss."""
    m = len(y)
    predictions = X.dot(theta)          # hθ(x) = X·θ
    loss = np.sum((predictions - y) ** 2) / (2 * m)  # 1/2 factor for cleaner derivative
    return loss

def gradient_descent(X, y, theta, alpha, iterations):
    """Perform batch gradient descent."""
    m = len(y)
    for _ in range(iterations):
        predictions = X.dot(theta)          # forward pass
        error = predictions - y            # residuals
        gradient = (X.T.dot(error)) / m    # ∂J/∂θ
        theta = theta - alpha * gradient    # parameter update
    return theta
```

### Simple Gradient Descent Implementation [reconstructed] ([32:30](https://youtu.be/iRbsBi5W0-c?t=1950))
Ye ek basic example hai jisme gradient descent manually implement kiya gaya hai. Line 1: Initial weight set karna. Line 2: Learning rate define karna. Line 3: Loop mein har iteration par gradient calculate karna. Line 4: Weight update karna using learning rate. Line 5: Loss calculate karna for monitoring.

```python
import numpy as np

# Initial parameters
w = 0.0
alpha = 0.01

# Sample data
X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# Gradient descent loop
for i in range(1000):
    y_pred = w * X
    error = y_pred - y
    cost = np.mean(error ** 2)
    gradient = 2 * np.mean(X * error)
    w = w - alpha * gradient
    
    if i % 100 == 0:
        print(f'Iteration {i}, Cost: {cost:.4f}, Weight: {w:.4f}')

print(f'Final Weight: {w:.4f}')
```

## Analogies

- ([12:15](https://youtu.be/iRbsBi5W0-c?t=735)) **Analogy:** Rolling a ball down a hill — *Explains:* A ball naturally rolls down the steepest slope; gradient descent works the same way — parameters move opposite to the gradient (steepest increase) of the loss, which is the slope of the error surface.
- ([15:45](https://youtu.be/iRbsBi5W0-c?t=945)) **Analogy:** Learning rate as step size in walking — *Explains:* If you take big steps (high learning rate) you may jump over the valley (minimum) and keep walking back and forth. Small steps (low learning rate) let you carefully find the bottom, though it takes longer.
- ([30:15](https://youtu.be/iRbsBi5W0-c?t=1815)) **Analogy:** Andhere mein pahadi se neeche utarna - aap sirf apne pairon ke neeche ki slope feel kar sakte ho aur usi direction mein step lete ho. — *Explains:* Ye analogy gradient descent ka local nature explain karti hai. Hum global minimum nahi dekh sakte, sirf local gradient use karke direction decide karte hain. Har step par hum sirf current point ki information use karte hain.
- ([31:45](https://youtu.be/iRbsBi5W0-c?t=1905)) **Analogy:** Step size analogy - chhote steps slow hote hain, bade steps oscillate karte hain, ideal steps efficient hote hain. — *Explains:* Ye analogy learning rate ka effect explain karti hai. Chhota learning rate = slow convergence, bada learning rate = divergence/oscillation, optimal learning rate = fast aur stable convergence.

## Common Mistakes

- **Mistake [teacher]:** Choosing a learning rate that is too high, causing the loss to diverge. ([15:30](https://youtu.be/iRbsBi5W0-c?t=930))
  - *Why:* A large α makes each update too big, overshooting the minimum and causing the loss to increase instead of decrease.
  - *Fix:* Reduce the learning rate or use a learning‑rate schedule that decreases α over time.
- **Mistake [teacher]:** Forgetting the negative sign in the update rule (adding instead of subtracting). ([13:45](https://youtu.be/iRbsBi5W0-c?t=825))
  - *Why:* Adding the gradient moves parameters toward higher loss, diverging from the optimum.
  - *Fix:* Always update as θ = θ - α·gradient; ensure the minus sign is present.
- **Mistake [added]:** Assuming gradient descent will always converge to the global minimum. ([17:50](https://youtu.be/iRbsBi5W0-c?t=1070))
  - *Why:* Only guaranteed for convex loss functions; non‑convex problems may trap the optimizer in local minima or saddle points.
  - *Fix:* Use proper initialization, momentum, or second‑order methods; verify loss landscape if possible.
- **Mistake [teacher]:** Learning rate bahut bada set karna ([31:50](https://youtu.be/iRbsBi5W0-c?t=1910))
  - *Why:* Jab learning rate bahut bada hota hai, toh weights bahut zyada update hote hain aur loss function ke minimum ko cross karke doosri side chala jaate hain. Isse loss curve oscillate karta hai ya diverge ho jata hai.
  - *Fix:* Learning rate ko chhota karo (e.g., 0.01 se 0.001 tak). Loss curve monitor karo - agar oscillation ho raha hai toh learning rate kam karo. Grid search ya learning rate finder use karo optimal value dhundhne ke liye.
- **Mistake [teacher]:** Learning rate bahut chhota set karna ([31:55](https://youtu.be/iRbsBi5W0-c?t=1915))
  - *Why:* Jab learning rate bahut chhota hota hai, toh har step mein weights bahut kam update hote hain. Isse convergence bahut slow ho jati hai aur training time bahut zyada lagta hai.
  - *Fix:* Learning rate ko thoda bada karo. Learning rate schedule use karo jo initial mein bada ho aur gradually kam ho jaye. Early stopping criteria set karo taaki unnecessary iterations na ho.
- **Mistake [added]:** Feature scaling na karna ([32:45](https://youtu.be/iRbsBi5W0-c?t=1965))
  - *Why:* Agar features ki scale alag alag hai (e.g., age 0-100 aur income 0-100000), toh gradient descent elliptical path follow karta hai instead of straight line to minimum. Isse convergence slow ho jati hai.
  - *Fix:* Har feature ko normalize ya standardize karo (e.g., mean=0, std=1). Isse loss function ki surface symmetric ho jati hai aur gradient descent faster converge karta hai.
- **Mistake [added]:** Batch size select karna bina understanding ke ([32:20](https://youtu.be/iRbsBi5W0-c?t=1940))
  - *Why:* Chhota batch size noisy gradients deta hai, bada batch size slow hota hai. Galat batch size selection se convergence affected hota hai.
  - *Fix:* Mini-batch size 32, 64, 128 ya 256 try karo. GPU memory ke hisaab se batch size choose karo. Generally 32-256 range mein achha balance milta hai.

## Formulas & Key Terms

### Formulas
- **Gradient Descent Update Rule:** `θ = θ - α ∇_θ J(θ)` — θ (parameters) are updated by moving opposite to the gradient of the loss function, scaled by the learning rate α.
- **Mean Squared Error (MSE):** `J(θ) = (1/m) Σ_{i=1}^{m} (h_θ(x^{(i)}) - y^{(i)})²` — Average of squared differences between predicted values h_θ(x) and true targets y across m training examples.
- **Mean Squared Error Loss:** `L = (1/n) * sum((y_pred - y_actual)^2)` — Loss function jo prediction aur actual value ke beech ke squared difference ka average hai. Gradient descent is loss ko minimize karta hai.
- **Gradient Calculation:** `dL/dw = 2 * (1/n) * sum(X * (y_pred - y_actual))` — Loss function ke respect mein weight ka derivative. Ye batata hai ki weight ko kis direction mein kitna update karna hai.

### Key Terms
- **Gradient:** Vector of partial derivatives of the loss function w.r.t. parameters; points in the direction of steepest increase.
- **Learning Rate (α):** Step‑size hyperparameter that scales how much we move in the direction of the negative gradient.
- **Convergence:** When the loss stops decreasing significantly over iterations, indicating the parameters have reached a (local) minimum.
- **Convex Function:** A function where any line segment between two points on the graph lies above the graph; for convex loss, gradient descent is guaranteed to find the global minimum.
- **Gradient Descent:** Ek optimization algorithm jo loss function ko minimize karne ke liye parameters ko iteratively update karta hai using gradient information.
- **Learning Rate:** Hyperparameter jo har step mein parameters kitne update honge, ye control karta hai. Bahut bada = divergence, bahut chhota = slow convergence.
- **Batch Gradient Descent:** Gradient descent ka variant jisme poore dataset par gradient calculate kiya jata hai har epoch mein. Slow lekin stable.
- **Mini-batch Gradient Descent:** Gradient descent ka variant jisme dataset ko chhote batches mein divide kiya jata hai. Balance hai speed aur stability ke beech. Practical mein sabse zyada use hota hai.
- **Stochastic Gradient Descent:** Gradient descent ka variant jisme har single sample par gradient calculate kiya jata hai. Fast lekin noisy convergence deta hai.
- **Loss Function:** Function jo model ki prediction aur actual value ke beech ka difference measure karta hai. Gradient descent is function ko minimize karta hai.
