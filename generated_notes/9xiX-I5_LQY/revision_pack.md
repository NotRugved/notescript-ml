# Revision Pack: Handling Mixed Variables | Feature Engineering

**One-Line Summary:** Linear Regression mein hum MSE cost function ko minimize karne ke liye Gradient Descent use karte hain, jahan learning rate aur feature scaling convergence ki speed aur stability decide karte hain.

## Cheat Sheet

| Component | Formula/Concept | Key Detail |
| :--- | :--- | :--- |
| **Hypothesis** | $h_\theta(x) = \theta^T x$ | $\theta_0$ is bias, $\theta_i$ are weights. |
| **Cost Function** | $J(\theta) = \frac{1}{2m} \sum (h_\theta(x) - y)^2$ | Mean Squared Error (MSE). Lower is better. |
| **Gradient** | $\nabla J(\theta) = \frac{1}{m} X^T (X\theta - y)$ | Direction of steepest increase. |
| **Update Rule** | $\theta \leftarrow \theta - \alpha \nabla J(\theta)$ | Move opposite to gradient. $\alpha$ is learning rate. |
| **Derivative $\theta_0$** | $\frac{1}{m} \sum (h_\theta(x) - y)$ | Sum of errors. |
| **Derivative $\theta_1$** | $\frac{1}{m} \sum (h_\theta(x) - y) x$ | Sum of errors weighted by features. |
| **Common Mistake** | High $\alpha$ or No Scaling | Causes divergence or slow convergence. |
| **Fix** | Scale features, tune $\alpha$ | Use standardization (mean=0, std=1). |

## Flashcards

### Card 1
**Q:** Linear Regression mein hypothesis function $h_\theta(x)$ ka general form kya hai?

**A:** $h_\theta(x) = \theta^T x$ ya $\theta_0 + \theta_1 x_1 + \dots + \theta_n x_n$.

### Card 2
**Q:** Linear Regression ke liye standard Cost Function kaunsa hota hai?

**A:** Mean Squared Error (MSE): $J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})^2$.

### Card 3
**Q:** Cost function mein $\frac{1}{2m}$ factor kyun use kiya jata hai?

**A:** Isse gradient values manageable rehte hain aur mathematical derivation mein 2 cancel ho jata hai, simplifying the derivative.

### Card 4
**Q:** Gradient Descent ka basic update rule kya hai?

**A:** $\theta_j \leftarrow \theta_j - \alpha \frac{\partial J}{\partial \theta_j}$.

### Card 5
**Q:** Learning rate ($\alpha$) ka role kya hai?

**A:** Yeh control karta hai ki har step mein parameters kitni door move karein. Chhota = slow, Bada = unstable/diverge.

### Card 6
**Q:** MSE cost function ka partial derivative w.r.t $\theta_0$ (bias) kya hai?

**A:** $\frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})$.

### Card 7
**Q:** MSE cost function ka partial derivative w.r.t $\theta_1$ (weight) kya hai?

**A:** $\frac{1}{m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)}) x^{(i)}$.

### Card 8
**Q:** Feature scaling kyun zaroori hai Gradient Descent mein?

**A:** Agar features ki scale alag-alag hai, toh gradient descent zig-zag karta hai aur convergence slow ho jati hai. Scaling se convergence fast aur stable hoti hai.

### Card 9
**Q:** Agar learning rate ($\alpha$) bohot zyada ho toh kya hoga?

**A:** Cost function diverge ho jayega, values NaN ban sakti hain, aur model kabhi converge nahi karega.

### Card 10
**Q:** NumPy mein vectorized gradient calculation kaise hoti hai?

**A:** `gradient = (1/m) * X.T @ (X @ theta - y)`.

### Card 11
**Q:** Gradient Descent ko real life mein kaise samjha ja sakta hai?

**A:** Jaise koi hilly terrain mein neeche ki taraf chhote-chhote qadmon se chalta hai, waise hi hum cost function ki valley (minimum) ki taraf move karte hain.

### Card 12
**Q:** Theta ($\theta$) ko initialize karne ka best practice kya hai?

**A:** Zero initialization se avoid karo (agar possible ho) ya small random values use karo taaki symmetry break ho aur convergence better ho.

### Card 13
**Q:** Linear Regression mein $m$ ka matlab kya hai?

**A:** Training examples ki total number.

### Card 14
**Q:** Hypothesis mein $\theta_0$ ko kya kehte hain?

**A:** Intercept ya Bias term. Yeh line ko upar/neeche shift karta hai.

### Card 15
**Q:** Gradient vector $\nabla J(\theta)$ ki direction kya hoti hai?

**A:** Steepest increase (sabse tez badhne) ki direction. Hum iske opposite mein move karte hain.

## Quiz

#### Question 1: Linear Regression mein cost function minimize karne ke liye kaunsa algorithm commonly use hota hai?
- [0] K-Means Clustering
- [1] Gradient Descent
- [2] Decision Tree
- [3] Naive Bayes

#### Question 2: MSE cost function mein $\frac{1}{2m}$ factor ka main mathematical fayda kya hai?
- [0] Cost ko negative banane ke liye
- [1] Derivative mein 2 cancel hone ke liye
- [2] Data ko normalize karne ke liye
- [3] Overfitting rokne ke liye

#### Question 3: Agar learning rate ($\alpha$) bohot chhota ho toh kya hoga?
- [0] Model turant converge ho jayega
- [1] Model diverge ho jayega
- [2] Convergence bahut slow hogi
- [3] NaN values aayengi

#### Question 4: Feature scaling nahi karne se Gradient Descent par kya asar padta hai?
- [0] Koi asar nahi padta
- [1] Convergence fast hoti hai
- [2] Convergence slow ya unstable hoti hai
- [3] Model overfit ho jata hai

#### Question 5: NumPy mein `X.T @ error` kya represent karta hai?
- [0] Prediction values
- [1] Gradient vector
- [2] Cost function value
- [3] Loss history

#### Question 6: Partial derivative $\frac{\partial J}{\partial \theta_1}$ mein $x^{(i)}$ ka role kya hai?
- [0] Error ko amplify karna
- [1] Error ko weight karna based on feature value
- [2] Bias ko adjust karna
- [3] Data ko shuffle karna

#### Question 7: Gradient Descent mein hum gradient vector ki kis direction mein move karte hain?
- [0] Same direction
- [1] Opposite direction
- [2] Random direction
- [3] Perpendicular direction

#### Question 8: Linear Regression mein $\theta_0$ ko kya kehte hain?
- [0] Slope
- [1] Bias/Intercept
- [2] Learning Rate
- [3] Feature

#### Question 9: Agar cost function ka gradient zero ho jaye, toh kya matlab hai?
- [0] Model fail ho gaya
- [1] Model maximum par hai
- [2] Model minimum (converged) par hai
- [3] Data corrupt hai

#### Question 10: NumPy code mein `theta = np.zeros(2)` kya karta hai?
- [0] Random weights set karta hai
- [1] Weights ko zero initialize karta hai
- [2] Data ko scale karta hai
- [3] Epochs set karta hai

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Gradient Descent ek iterative optimization algorithm hai jo parameters ko adjust karke cost function ko minimize karta hai.
- **Q2 Answer:** Option 1 — Square ke derivative mein 2 aata hai, jo $\frac{1}{2}$ se cancel ho jata hai, isse update rule simple ho jata hai.
- **Q3 Answer:** Option 2 — Chhota learning rate matlab chhote steps, isliye minimum tak pahunchne mein bahut zyada time/iterations lagenge.
- **Q4 Answer:** Option 2 — Alag scales wale features se gradient contour elliptical shape le leta hai, jisse algorithm zig-zag karta hai aur slow converge karta hai.
- **Q5 Answer:** Option 1 — Yeh vectorized form hai of $\frac{1}{m} \sum (h_\theta(x) - y) x$, jo gradient calculate karta hai.
- **Q6 Answer:** Option 1 — Weight $\theta_1$ ka update us feature ki value ($x$) par depend karta hai, jo error ko scale karta hai.
- **Q7 Answer:** Option 1 — Gradient steepest increase ki direction batata hai, isliye minimize karne ke liye hum opposite direction mein move karte hain.
- **Q8 Answer:** Option 1 — $\theta_0$ intercept hai jo line ko y-axis par shift karta hai.
- **Q9 Answer:** Option 2 — Zero gradient matlab cost function ki slope flat hai, jo local/global minimum indicate karta hai.
- **Q10 Answer:** Option 1 — Yeh parameter vector ko shuruwat mein zero values se initialize karta hai.

## Interview Questions

### Q1: Linear Regression mein Gradient Descent kaunse steps follow karta hai? Update rule derive karo.

**Answer:** Gradient Descent iterative hai. Pehle cost function $J(\theta) = \frac{1}{2m} \sum (h_\theta(x) - y)^2$ define karte hain. Phir gradient $\nabla J(\theta)$ calculate karte hain. Update rule hai $\theta \leftarrow \theta - \alpha \nabla J(\theta)$. Iska matlab hai ki hum har parameter ko uski partial derivative ke opposite direction mein update karte hain, jahan $\alpha$ learning rate hai. Yeh process tab tak chalta hai jab tak cost minimize na ho jaye.

### Q2: Learning rate ($\alpha$) chunna kyun critical hai? Uske effects explain karo.

**Answer:** Learning rate step size control karta hai. Agar $\alpha$ bohot chhota hai, toh convergence bahut slow hogi aur zyada compute power lagegi. Agar $\alpha$ bohot bada hai, toh algorithm minimum ko cross karke diverge ho sakta hai ya oscillate karega, resulting in NaN values. Ideal learning rate aisa hota hai jo stable aur fast convergence de. Adaptive learning rates (jaise Adam) yeh problem solve karte hain.

### Q3: Feature scaling kyun zaroori hai Gradient Descent ke liye? Bina scaling ke kya problem aati hai?

**Answer:** Agar features ki scale alag-alag hai (e.g., age 0-100 aur income 0-100000), toh cost function ka contour elliptical shape le leta hai. Gradient descent is case mein zig-zag pattern mein move karta hai, jo convergence ko bahut slow banata hai. Scaling (Standardization/Normalization) se contour circular shape ho jata hai, jisse algorithm seedha minimum ki taraf tezi se pahunchta hai.

### Q4: Vectorized implementation of Gradient Descent in NumPy kaise hoti hai? Benefits kya hain?

**Answer:** NumPy mein hum loops ki jagah matrix operations use karte hain. Predictions: `X @ theta`. Error: `predictions - y`. Gradient: `(1/m) * X.T @ error`. Update: `theta -= alpha * gradient`. Benefits: 1) Code concise hota hai. 2) NumPy internally optimized C code use karta hai, jo Python loops se kai guna fast hai. 3) Readability better hoti hai.

### Q5: Linear Regression mein Bias ($\theta_0$) aur Weight ($\theta_1$) ke gradients mein kya difference hai?

**Answer:** Bias ($\theta_0$) ka gradient sirf errors ka average hai: $\frac{1}{m} \sum (h_\theta(x) - y)$. Weight ($\theta_1$) ka gradient errors ko corresponding feature values se multiply karke average karta hai: $\frac{1}{m} \sum (h_\theta(x) - y) x$. Iska matlab hai ki weight ka update us feature ki magnitude par depend karta hai, jabki bias ka update sirf overall error par depend karta hai.
