# Revision Pack: Handling Date and Time Variables | Day 34 | 100 Days of Machine Learning

**One-Line Summary:** Confusion matrix se precision, recall, F1, ROC‑AUC tak, imbalanced data mein accuracy se aage ka model evaluation.

## Cheat Sheet

| Metric | Formula | What it measures | When to prioritize |
|--------|---------|------------------|--------------------|
| Accuracy | (TP+TN)/(TP+FP+TN+FN) | Overall correct predictions | Balanced classes |
| Precision | TP/(TP+FP) | Correctness of predicted positives | Spam filter, low FP cost |
| Recall (Sensitivity) | TP/(TP+FN) | Coverage of actual positives | Cancer detection, low FN cost |
| F1 Score | 2·(Precision·Recall)/(Precision+Recall) | Balance between precision & recall (harmonic mean) | Imbalanced data, need single score |
| ROC‑AUC | ∫TPR dFPR (area under ROC curve) | Threshold‑independent discriminative ability | Compare models, any class distribution |
| Specificity | TN/(TN+FP) | True negative rate | When true negatives matter |
| False Positive Rate | FP/(FP+TN) | Rate of negative cases mis‑classified as positive | ROC curve axis |
| Confusion Matrix | 2×2 table of TP, FP, TN, FN | Detailed error breakdown | All classification problems |

## Flashcards

### Card 1
**Q:** Confusion matrix ke 4 components kaunse hain?

**A:** True Positive (TP), False Positive (FP), True Negative (TN), False Negative (FN)

### Card 2
**Q:** Precision ka formula kya hai?

**A:** Precision = TP / (TP + FP)

### Card 3
**Q:** Recall ko aur kya naam se bhi jaante hain?

**A:** Recall ko Sensitivity ya True Positive Rate bhi kehte hain

### Card 4
**Q:** F1 score kaise calculate karte hain?

**A:** F1 = 2 * (Precision * Recall) / (Precision + Recall)

### Card 5
**Q:** AUC ka full form aur meaning kya hai?

**A:** AUC = Area Under the ROC Curve, model ki overall discriminative ability batata hai

### Card 6
**Q:** ROC curve ka x‑axis aur y‑axis kya represent karte hain?

**A:** X‑axis = False Positive Rate (FPR), Y‑axis = True Positive Rate (Recall)

### Card 7
**Q:** Imbalanced dataset mein accuracy kyun misleading ho sakti hai?

**A:** Kyuki model majority class ko always predict karke high accuracy de sakta hai, lekin minority class ko miss kar sakta hai

### Card 8
**Q:** Precision high aur Recall low hone par F1 score kya hota hai?

**A:** F1 score low hota hai, kyunki harmonic mean dono mein se kam value ko reflect karta hai

### Card 9
**Q:** AUC = 0.5 ka matlab kya hota hai?

**A:** Model random guessing ke barabar hai

### Card 10
**Q:** True Negative Rate ka dusra naam kya hai?

**A:** Specificity

### Card 11
**Q:** Type I error kaunse metric se related hai?

**A:** False Positive (FP), jo Precision ko affect karta hai

### Card 12
**Q:** Type II error kaunse metric se related hai?

**A:** False Negative (FN), jo Recall ko affect karta hai

### Card 13
**Q:** F1 score harmonic mean hai, arithmetic mean nahi. Iska kya implication hai?

**A:** Agar ek metric zero ho, toh F1 bhi zero ho jata hai, isliye dono balanced hone chahiye

### Card 14
**Q:** ROC curve threshold change karne par kaise shift hota hai?

**A:** Threshold low karne se TPR badhta hai lekin FPR bhi badhta hai, curve ka point right‑up move karta hai

### Card 15
**Q:** AUC > 0.9 indicate karta hai kya?

**A:** Model excellent discriminative power rakhta hai

## Quiz

#### Question 1: Ek model ka confusion matrix: TP=40, FP=10, FN=20, TN=130. Is model ki precision kya hai?
- [0] 0.80
- [1] 0.67
- [2] 0.57
- [3] 0.73

#### Question 2: Recall (Sensitivity) ka formula kaun sa hai?
- [0] TP/(TP+FP)
- [1] TP/(TP+FN)
- [2] TN/(TN+FP)
- [3] FP/(FP+TN)

#### Question 3: AUC = 0.5 ka matlab hai:
- [0] Perfect classifier
- [1] Random guessing
- [2] Worse than random
- [3] Overfitting

#### Question 4: Spam filter ke liye kaunse metric ko zyada prioritize karna chahiye?
- [0] Recall
- [1] Precision
- [2] Accuracy
- [3] Specificity

#### Question 5: Cancer detection model me false negative ka impact kya hota hai?
- [0] Low cost
- [1] High cost
- [2] No impact
- [3] Improves precision

#### Question 6: F1 score ko harmonic mean kehte hain. Agar Precision=0.9 aur Recall=0.1, to F1 approx:
- [0] 0.18
- [1] 0.55
- [2] 0.20
- [3] 0.30

#### Question 7: ROC curve ka x‑axis kya represent karta hai?
- [0] True Positive Rate
- [1] False Positive Rate
- [2] Precision
- [3] Recall

#### Question 8: Imbalanced dataset me accuracy 95% hai. Model sab negative predict karta hai. Iska precision kya hoga?
- [0] Undefined (0/0)
- [1] 0
- [2] 1
- [3] 0.95

#### Question 9: Specificity ka formula kya hai?
- [0] TN/(TN+FP)
- [1] TP/(TP+FN)
- [2] FP/(FP+TN)
- [3] TP/(TP+FP)

#### Question 10: AUC < 0.5 indicate karta hai:
- [0] Better than random
- [1] Worse than random
- [2] Perfect model
- [3] Insufficient data

### Quiz Answers & Explanations

- **Q1 Answer:** Option 2 — Precision = TP/(TP+FP) = 40/(40+10) = 40/50 = 0.8, lekin option 0.80 is correct. Actually 0.80 is option 0, so answer_index should be 0. Correction: answer_index 0.
- **Q2 Answer:** Option 1 — Recall = TP/(TP+FN) which measures how many actual positives were captured.
- **Q3 Answer:** Option 1 — AUC 0.5 indicates the model is no better than a random coin flip.
- **Q4 Answer:** Option 1 — Spam filter me false positives (important mail marked spam) costly hote hain, isliye precision important hai.
- **Q5 Answer:** Option 1 — Missing a cancer case (FN) can be fatal, so recall (low FN) is crucial.
- **Q6 Answer:** Option 0 — F1 = 2*(0.9*0.1)/(0.9+0.1)=0.18.
- **Q7 Answer:** Option 1 — X‑axis = False Positive Rate (FPR).
- **Q8 Answer:** Option 1 — Precision = TP/(TP+FP). Here TP=0, FP=0, so precision is undefined; commonly treated as 0.
- **Q9 Answer:** Option 0 — Specificity = True Negative Rate = TN/(TN+FP).
- **Q10 Answer:** Option 1 — AUC less than 0.5 means the model is performing worse than random guessing.

## Interview Questions

### Q1: Explain the confusion matrix and how you would derive precision, recall, and F1 score from it.

**Answer:** Confusion matrix ek 2x2 table hota hai jisme TP, FP, TN, FN counts hote hain. Precision = TP/(TP+FP) batata hai ki predicted positives me se kitne sahi hain. Recall = TP/(TP+FN) batata hai ki actual positives me se kitne capture hue. F1 score harmonic mean hai: 2*(Precision*Recall)/(Precision+Recall). Ye teen metrics milke model ki error type (FP vs FN) ko samajhne me madad karte hain, especially jab data imbalanced ho.

### Q2: Why is accuracy not a reliable metric for imbalanced classification problems? Provide an example.

**Answer:** Accuracy counts overall correct predictions, is biased towards the majority class. Agar 95% data negative hai, ek model jo hamesha 'negative' predict karega 95% accuracy dega, lekin koi positive case catch nahi karega (TP=0). Isse model ki usefulness practically zero hoti hai. Isliye precision, recall, F1, ya AUC jaise metrics use karte hain jo minority class ki performance ko highlight karte hain.

### Q3: What is the difference between ROC curve and Precision‑Recall curve? When would you prefer one over the other?

**Answer:** ROC curve plots TPR (Recall) vs FPR across thresholds, AUC‑ROC gives a threshold‑independent measure. Precision‑Recall (PR) curve plots Precision vs Recall. PR curve is more informative when the positive class is rare (high class imbalance) because ROC can present an overly optimistic view due to many true negatives. Hence, for imbalanced datasets (e.g., fraud detection) prefer PR curve; for balanced or when false positive cost is moderate, ROC‑AUC works well.

### Q4: Derive the relationship between F1 score and the harmonic mean. Why is harmonic mean preferred over arithmetic mean in this context?

**Answer:** Harmonic mean of two numbers a and b is defined as 2ab/(a+b). F1 = 2*(Precision*Recall)/(Precision+Recall), which is exactly the harmonic mean of precision and recall. Harmonic mean penalizes extreme imbalance: if either precision or recall is low, the harmonic mean drops sharply, reflecting that both aspects are needed. Arithmetic mean would give a higher value even if one metric is near zero, masking poor performance.

### Q5: How does changing the classification threshold affect the confusion matrix and derived metrics like precision, recall, and AUC?

**Answer:** Lowering the threshold makes the model predict positive more often: TP and FP increase, FN decreases, TN decreases. Consequently, recall (TP/(TP+FN)) goes up, precision (TP/(TP+FP)) may go down due to more FP. Raising the threshold does the opposite. AUC, however, integrates performance over all possible thresholds, so it remains unchanged by a single threshold change; it reflects the model's ability to separate classes irrespective of a specific cut‑off.
