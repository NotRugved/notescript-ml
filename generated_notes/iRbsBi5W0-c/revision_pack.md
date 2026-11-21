# Revision Pack: Principle Component Analysis  (PCA) | Part 1 | Geometric Intuition

**One-Line Summary:** Gradient Descent ek iterative optimization technique hai jo loss ko minimize karne ke liye parameters ko learning rate ke saath opposite gradient direction mein update karti hai.

## Cheat Sheet

- **Goal**: Minimize loss J(θ) (e.g., MSE)\
- **Update rule**: θ ← θ - α ∇_θ J(θ)\
- **Key symbols**: θ = parameters, α = learning rate, ∇ = gradient, m = #samples, t = iteration\
- **Steps**: Initialize θ → Compute gradient → Update θ → Repeat until convergence\
- **Learning rate effects**:\
  | α value | Effect |
  |---|---|
  | Very small (0.001) | Slow convergence |
  | Moderate (0.01‑0.1) | Stable, steady loss drop |
  | Very large (≥1) | Divergence / oscillation |
- **Variants**:\
  - **Batch GD**: gradient over whole dataset (stable, costly)\
  - **Stochastic GD**: gradient on one sample (fast, noisy)\
  - **Mini‑batch GD**: gradient on small batch (32‑256) – practical default\
- **Common pitfalls**: wrong α, missing negative sign, no feature scaling, assuming global optimum for non‑convex loss.

## Flashcards

### Card 1
**Q:** Gradient Descent ka primary objective kya hota hai?

**A:** Loss function ko minimum tak le jaana, yaani model ki error ko kam se kam karna.

### Card 2
**Q:** Update rule ka formula kya hai?

**A:** θ = θ - α * ∇_θ J(θ)

### Card 3
**Q:** Learning rate (α) ka role kya hota hai?

**A:** Har iteration mein gradient ke magnitude ko scale karta hai; chhota α slow, bada α overshoot ya diverge karta hai.

### Card 4
**Q:** MSE loss ka expression kya hai?

**A:** J(θ) = (1/2m) Σ_{i=1}^{m} (h_θ(x^{(i)}) - y^{(i)})^2

### Card 5
**Q:** Batch Gradient Descent aur Stochastic Gradient Descent mein main difference kya hai?

**A:** Batch poore dataset ka gradient use karta hai, SGD ek single example ka gradient use karta hai.

### Card 6
**Q:** Mini‑batch GD ka typical batch size range kya hota hai?

**A:** Usually 32, 64, 128 ya 256 samples per batch.

### Card 7
**Q:** Gradient vector ka matlab kya hota hai?

**A:** Loss function ke respect mein sabhi parameters ke partial derivatives ka collection; steepest increase direction.

### Card 8
**Q:** Convex loss function ka kya significance hai?

**A:** Convex hone par Gradient Descent guaranteed global minimum tak pahunchta hai.

### Card 9
**Q:** Negative sign update rule mein kyun zaroori hai?

**A:** Taaki hum loss ke steepest increase ke opposite direction mein move karein, loss ko kam karein.

### Card 10
**Q:** Feature scaling ka Gradient Descent par kya effect hota hai?

**A:** Scaling se gradient ki magnitude sab features ke liye similar hoti hai, convergence fast hota hai.

### Card 11
**Q:** Learning rate schedule ka ek example batao.

**A:** Step decay: α_t = α_0 / (1 + decay_rate * epoch) ya exponential decay: α_t = α_0 * exp(-k*t).

### Card 12
**Q:** Gradient Descent ka convergence criteria kya ho sakta hai?

**A:** Loss change < ε for consecutive iterations, ya max iterations reached.

### Card 13
**Q:** SGD ka ek advantage kya hai?

**A:** Har iteration fast hota hai aur noisy updates local minima se bahar nikal sakte hain.

### Card 14
**Q:** Gradient Descent ka ek disadvantage kya hai?

**A:** Learning rate tuning critical; wrong α se diverge ya bahut slow ho sakta hai.

### Card 15
**Q:** Python mein gradient compute karne ke liye kaunse matrix operation ka use hota hai?

**A:** gradient = (X.T.dot(error)) / m, jahan X.T is transpose of feature matrix.

## Quiz

#### Question 1: Gradient Descent ka update rule kya hai?
- [0] θ = θ + α ∇J
- [1] θ = θ - α ∇J
- [2] θ = θ - α / ∇J
- [3] θ = θ * α ∇J

#### Question 2: MSE loss me 1/2 factor ka purpose kya hota hai?
- [0] Loss ko half karna
- [1] Derivative me 2 cancel karna
- [2] Learning rate ko halve karna
- [3] Gradient ko double karna

#### Question 3: Agar learning rate bahut chhota ho, to training ka result kya hoga?
- [0] Fast convergence
- [1] Divergence
- [2] Very slow convergence
- [3] Immediate convergence

#### Question 4: Batch Gradient Descent ka major drawback kya hai?
- [0] Noisy updates
- [1] High memory usage for large datasets
- [2] Cannot handle convex loss
- [3] Requires feature scaling

#### Question 5: Stochastic Gradient Descent updates parameters after:
- [0] Each epoch
- [1] Each mini‑batch
- [2] Each single training example
- [3] After convergence

#### Question 6: Which of the following guarantees global optimum with Gradient Descent?
- [0] Non‑convex loss
- [1] Convex loss
- [2] Any loss
- [3] Linear regression only

#### Question 7: Feature scaling improves Gradient Descent because:
- [0] It reduces overfitting
- [1] It makes loss convex
- [2] It makes gradient steps more uniform across dimensions
- [3] It eliminates need for learning rate

#### Question 8: Mini‑batch size of 64 is chosen mainly to:
- [0] Maximize noise
- [1] Balance speed and stability
- [2] Use whole dataset
- [3] Avoid GPU usage

#### Question 9: What happens if you forget the negative sign in the update rule?
- [0] Loss decreases faster
- [1] Loss increases, model diverges
- [2] Learning rate becomes zero
- [3] Gradient becomes zero

#### Question 10: Which learning rate schedule reduces α over time?
- [0] Constant α
- [1] Increasing α
- [2] Step decay
- [3] Random α

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Negative sign ensures movement opposite to gradient, reducing loss.
- **Q2 Answer:** Option 1 — 1/2 factor cancels the 2 that appears when differentiating the square term.
- **Q3 Answer:** Option 2 — Small α leads to tiny steps, so loss decreases very slowly.
- **Q4 Answer:** Option 1 — It needs to compute gradient over entire dataset each iteration, which is costly for big data.
- **Q5 Answer:** Option 2 — SGD computes gradient on one randomly chosen example per update.
- **Q6 Answer:** Option 1 — Convex loss functions have a single global minimum; GD will converge to it.
- **Q7 Answer:** Option 2 — Scaling puts features on similar scale, so gradient steps are balanced, speeding convergence.
- **Q8 Answer:** Option 1 — Mini‑batch provides a compromise: less noisy than SGD, faster than full batch.
- **Q9 Answer:** Option 1 — Adding the gradient moves parameters toward higher loss, causing divergence.
- **Q10 Answer:** Option 2 — Step decay reduces the learning rate as training progresses, helping fine‑tuning.

## Interview Questions

### Q1: Explain the intuition behind Gradient Descent using a real‑world analogy.

**Answer:** Socho aap ek hill ke upar khade ho aur aapko neeche valley tak jana hai. Hill ka steepest slope aapko batata hai ki loss sabse tez kaise badh raha hai (gradient). Gradient Descent us slope ke opposite direction mein chhota step leta hai – bilkul ball jo sabse steep slope par roll hoti hai. Har step par aap sirf current slope feel karte ho, poora hill dekh nahi sakte, isliye algorithm local information pe depend karta hai.

### Q2: What are the main differences between Batch, Stochastic, and Mini‑batch Gradient Descent?

**Answer:** Batch GD computes the exact gradient over the whole training set each iteration – stable but computationally heavy. Stochastic GD uses a single random example – fast per update, noisy, can escape shallow minima but may oscillate. Mini‑batch GD uses a small subset (e.g., 32‑256) – gives a smoother gradient than SGD while keeping per‑iteration cost low; it is the default in deep learning frameworks.

### Q3: How does the learning rate affect convergence, and how would you choose a good value?

**Answer:** Learning rate α scales the step size. Very small α → slow convergence, many epochs needed. Very large α → overshoot the minimum, causing loss to diverge or oscillate. A good α is found by starting with a modest value (0.01‑0.1), monitoring the loss curve, and adjusting: increase if loss plateaus early, decrease if loss spikes or becomes NaN. Advanced methods like learning‑rate schedules, warm‑up, or adaptive optimizers (Adam) can also help.

### Q4: Why is feature scaling important for Gradient Descent?

**Answer:** When features have different scales, the loss surface becomes elongated (elliptical). Gradient steps will be large in directions of high‑scale features and tiny in low‑scale ones, causing a zig‑zag path and slow convergence. Scaling (standardization or normalization) puts all features on a similar range, making the loss surface more spherical, so the same learning rate works well for all dimensions and convergence speeds up.

### Q5: Can Gradient Descent guarantee finding the global minimum for any loss function? Explain.

**Answer:** No. Guarantee exists only for convex loss functions where any local minimum is also global. For non‑convex problems (e.g., deep neural networks), GD may get stuck in local minima, saddle points, or plateaus. Techniques like random restarts, momentum, or second‑order methods can improve chances, but global optimality is not guaranteed.
