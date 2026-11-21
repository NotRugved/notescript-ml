# Revision Pack: Simple Linear Regression | Code + Intuition | Simplest Explanation in Hindi

**One-Line Summary:** Model evaluation ke liye sirf accuracy nahi, precision, recall, F1-score aur ROC-AUC ka istemal karna zaroori hai, khaaskar imbalanced datasets mein.

## Cheat Sheet

- **Confusion Matrix**: TP, TN, FP, FN
- **Accuracy**: (TP+TN)/(TP+TN+FP+FN)
- **Precision**: TP/(TP+FP) – false positives ko kam karta hai
- **Recall (Sensitivity)**: TP/(TP+FN) – false negatives ko kam karta hai
- **F1-Score**: 2*(Precision*Recall)/(Precision+Recall) – precision‑recall ka balance
- **ROC Curve**: TPR (Recall) vs FPR (1‑Specificity) across thresholds
- **AUC**: 0.5 random, 1.0 perfect
- **When to use**: Imbalanced data → prefer Precision, Recall, F1, AUC over Accuracy

## Flashcards

### Card 1
**Q:** Confusion Matrix ke 4 components kaunse hain?

**A:** True Positive (TP), True Negative (TN), False Positive (FP), False Negative (FN)

### Card 2
**Q:** Accuracy ka formula kya hai?

**A:** (TP + TN) / (TP + TN + FP + FN)

### Card 3
**Q:** Accuracy kab misleading ho sakti hai?

**A:** Jab dataset highly imbalanced ho, jaise 95% negative class.

### Card 4
**Q:** Precision ka matlab kya hota hai?

**A:** Predicted positives me se kitne actually positive hain – TP/(TP+FP).

### Card 5
**Q:** Recall (Sensitivity) ka formula kya hai?

**A:** TP / (TP + FN)

### Card 6
**Q:** Recall ka use case kaun sa scenario me important hai?

**A:** Medical diagnosis ya cancer screening jahan false negative costly hota hai.

### Card 7
**Q:** F1-Score ka formula kya hai?

**A:** 2 * (Precision * Recall) / (Precision + Recall)

### Card 8
**Q:** F1-Score kis situation me sabse useful hai?

**A:** Jab class distribution uneven ho aur precision‑recall dono ko balance karna ho.

### Card 9
**Q:** ROC curve ka X‑axis kya represent karta hai?

**A:** False Positive Rate (FPR) = 1 - Specificity

### Card 10
**Q:** ROC curve ka Y‑axis kya represent karta hai?

**A:** True Positive Rate (TPR) = Recall

### Card 11
**Q:** AUC ka ideal value kya hota hai?

**A:** 1.0 – perfect classifier

### Card 12
**Q:** AUC ka worst value kya hota hai?

**A:** 0.5 – random guessing

### Card 13
**Q:** Precision aur Recall ka denominator alag kyun hota hai?

**A:** Precision denominator includes predicted positives (TP+FP), Recall denominator includes actual positives (TP+FN).

### Card 14
**Q:** Type I error kaunse term se hota hai?

**A:** False Positive (FP)

### Card 15
**Q:** Type II error kaunse term se hota hai?

**A:** False Negative (FN)

## Quiz

#### Question 1: Aapke model ne 80 TP, 10 FP, 5 FN, aur 5 TN predict kiye. Accuracy kya hai?
- [0] 85%
- [1] 80%
- [2] 90%
- [3] 75%

#### Question 2: Ek spam filter 200 emails ko spam mark karta hai, jisme se 150 actually spam hain. Precision kya hai?
- [0] 75%
- [1] 85%
- [2] 65%
- [3] 50%

#### Question 3: Cancer screening test me 100 patients me se 20 ko disease hai. Test 18 ko correctly detect karta hai, 2 miss karta hai. Recall kya hai?
- [0] 90%
- [1] 85%
- [2] 80%
- [3] 95%

#### Question 4: Precision = 0.6 aur Recall = 0.8 hai. F1-Score kya hoga?
- [0] 0.68
- [1] 0.70
- [2] 0.75
- [3] 0.80

#### Question 5: ROC curve ka area (AUC) 0.5 hone ka kya matlab hai?
- [0] Model random guessing karta hai
- [1] Model perfect hai
- [2] Model overfitting hai
- [3] Model underfitting hai

#### Question 6: Imbalanced dataset me sabse zyada kaunse metric ko prioritize karna chahiye?
- [0] Accuracy
- [1] Precision
- [2] Recall
- [3] Mean Squared Error

#### Question 7: Confusion Matrix me False Positive ka Hindi term kya hota hai?
- [0] Type I error
- [1] Type II error
- [2] False Alarm
- [3] Missed Detection

#### Question 8: AUC 0.9 hone par model ki performance kaise describe karenge?
- [0] Excellent
- [1] Good
- [2] Average
- [3] Poor

#### Question 9: Precision high but Recall low ka kya implication hota hai?
- [0] Few false positives but many false negatives
- [1] Few false negatives but many false positives
- [2] Both errors low
- [3] Both errors high

#### Question 10: Specificity ka formula kya hai?
- [0] TN/(TN+FP)
- [1] TP/(TP+FN)
- [2] TP/(TP+FP)
- [3] TN/(TN+FN)

### Quiz Answers & Explanations

- **Q1 Answer:** Option 0 — Accuracy = (TP+TN)/(TP+TN+FP+FN) = (80+5)/(80+5+10+5) = 85/100 = 85%.
- **Q2 Answer:** Option 0 — Precision = TP/(TP+FP) = 150/(150+50) = 150/200 = 75%.
- **Q3 Answer:** Option 0 — Recall = TP/(TP+FN) = 18/(18+2) = 18/20 = 90%.
- **Q4 Answer:** Option 0 — F1 = 2*(0.6*0.8)/(0.6+0.8) = 0.96/1.4 ≈ 0.686 ≈ 0.68.
- **Q5 Answer:** Option 0 — AUC=0.5 indicates the classifier performs no better than random chance.
- **Q6 Answer:** Option 2 — Recall ensures minority (positive) class is captured, reducing false negatives.
- **Q7 Answer:** Option 0 — False Positive is also called Type I error.
- **Q8 Answer:** Option 0 — AUC close to 1 (e.g., 0.9) indicates excellent discriminative ability.
- **Q9 Answer:** Option 0 — High precision → low FP; low recall → high FN.
- **Q10 Answer:** Option 0 — Specificity = True Negative Rate = TN/(TN+FP).

## Interview Questions

### Q1: Explain why accuracy is not a reliable metric for imbalanced classification problems.

**Answer:** Accuracy measures overall correct predictions, but in imbalanced data the majority class dominates. A model can predict the majority class for every instance and still achieve high accuracy while completely ignoring the minority class. This gives a false sense of performance. Metrics like Precision, Recall, F1-score, and AUC focus on the minority class and provide a more realistic picture of how well the model detects the important cases.

### Q2: How do Precision and Recall differ, and when would you prioritize one over the other?

**Answer:** Precision = TP/(TP+FP) measures the correctness of positive predictions; it penalizes false positives. Recall = TP/(TP+FN) measures the ability to capture all actual positives; it penalizes false negatives. Prioritize Precision when false positives are costly (e.g., spam filter, legal document classification). Prioritize Recall when missing a positive is dangerous (e.g., disease screening, fraud detection). Often a trade‑off is needed, and F1‑score helps balance them.

### Q3: What is the ROC curve and what does the AUC represent?

**Answer:** The ROC (Receiver Operating Characteristic) curve plots the True Positive Rate (Recall) against the False Positive Rate (1‑Specificity) for different classification thresholds. It visualizes the trade‑off between sensitivity and false alarms. AUC (Area Under the Curve) summarizes this plot into a single number: 0.5 means random guessing, 1.0 means perfect discrimination. Higher AUC indicates better overall ability of the model to rank positive instances higher than negatives across all thresholds.

### Q4: Derive the F1‑Score formula and explain why it uses the harmonic mean instead of the arithmetic mean.

**Answer:** F1 = 2 * (Precision * Recall) / (Precision + Recall). It is derived by taking the harmonic mean of Precision and Recall. The harmonic mean penalizes extreme values more than the arithmetic mean; if either Precision or Recall is low, the F1‑Score drops significantly. This property ensures that a model cannot achieve a high F1 by excelling in only one metric while performing poorly in the other, making it a balanced measure for uneven class distributions.

### Q5: Describe a real‑world scenario where you would use a confusion matrix and how you would interpret its values.

**Answer:** Consider a medical diagnostic test for a rare disease. The confusion matrix would have: TP = patients correctly identified as diseased, FN = diseased patients missed (critical error), FP = healthy patients incorrectly flagged (unnecessary anxiety), TN = healthy patients correctly identified. By examining TP, FN, FP, and TN, clinicians can assess the test's safety (low FN) and cost (low FP). Decisions on threshold adjustment, further testing, or model selection can be guided by the trade‑off shown in the matrix.
