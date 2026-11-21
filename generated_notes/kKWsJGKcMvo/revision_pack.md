# Revision Pack: Binning and Binarization | Discretization | Quantile Binning | KMeans Binning

**One-Line Summary:** Precision, Recall, aur F1-score confusion matrix se derive hote hain, jo imbalanced binary classification me accuracy se behtar insight dete hain.

## Cheat Sheet

| Metric | Formula | Meaning | Typical Use |
|--------|---------|---------|-------------|
| Precision | TP / (TP + FP) | Predicted positives me se kitne sahi hain | Jab false positives costly ho (spam filter) |
| Recall (Sensitivity) | TP / (TP + FN) | Actual positives me se kitne pakde gaye | Jab false negatives dangerous ho (cancer detection) |
| F1-Score | 2 * (Precision * Recall) / (Precision + Recall) | Precision aur Recall ka harmonic mean | Balanced performance chahiye, especially imbalanced data |
| Confusion Matrix | - | 2x2 table: TP, FP, FN, TN | Sab metrics calculate karne ki base |
| Accuracy | (TP+TN) / (TP+FP+FN+TN) | Overall correct predictions | Balanced datasets ke liye theek, lekin imbalance me misleading |

## Flashcards

### Card 1
**Q:** Confusion matrix me rows aur columns kis cheez ko represent karte hain?

**A:** Rows = Actual labels, Columns = Predicted labels.

### Card 2
**Q:** Precision ka formula kya hai?

**A:** Precision = TP / (TP + FP).

### Card 3
**Q:** Recall ka formula kya hai?

**A:** Recall = TP / (TP + FN).

### Card 4
**Q:** F1-score ka formula kya hai?

**A:** F1 = 2 * (Precision * Recall) / (Precision + Recall).

### Card 5
**Q:** Precision aur Recall ka trade‑off kya hota hai?

**A:** Recall badhane se FP badh sakta hai, isse Precision girti hai; Precision badhane se FN badh sakta hai, isse Recall girti hai.

### Card 6
**Q:** Kis scenario me Recall ko prioritize karna chahiye?

**A:** Jab false negative bahut costly ho, jaise medical diagnosis ya fraud detection.

### Card 7
**Q:** Kis scenario me Precision ko prioritize karna chahiye?

**A:** Jab false positive bahut costly ho, jaise spam filter ya ad targeting.

### Card 8
**Q:** Harmonic mean use karne ka reason F1-score me kya hai?

**A:** Ye extreme low values ko penalize karta hai, isse dono Precision aur Recall balanced rehna zaroori hota hai.

### Card 9
**Q:** Imbalanced dataset me accuracy kyun misleading ho sakti hai?

**A:** Model majority class predict karke high accuracy de sakta hai, lekin minority class ko miss kar sakta hai (low Recall).

### Card 10
**Q:** sklearn me confusion_matrix function ka correct argument order kya hai?

**A:** confusion_matrix(y_true, y_pred) – pehle actual, phir predicted.

### Card 11
**Q:** Classification report me 'support' ka matlab kya hai?

**A:** Har class ke actual instances ki count.

### Card 12
**Q:** True Negative (TN) ka matlab kya hai?

**A:** Actual negative ko model ne correctly negative predict kiya.

### Card 13
**Q:** False Positive (FP) ko kaun sa error type kaha jata hai?

**A:** Type I error.

### Card 14
**Q:** False Negative (FN) ko kaun sa error type kaha jata hai?

**A:** Type II error.

### Card 15
**Q:** Agar Precision = 1.0 aur Recall = 0.1 ho, to F1-score approx kitna hoga?

**A:** F1 ≈ 0.18 (2*1*0.1/(1+0.1)).

## Quiz

#### Question 1: Ek model ka confusion matrix [[50, 10], [5, 35]] hai (rows=actual, cols=predicted). TP kya hai?
- [0] 50
- [1] 35
- [2] 10
- [3] 5

#### Question 2: Agar TP=40, FP=20, FN=10, TN=30, to Precision kya hoga?
- [0] 0.66
- [1] 0.57
- [2] 0.8
- [3] 0.4

#### Question 3: Upar ke numbers se Recall kya hoga?
- [0] 0.8
- [1] 0.57
- [2] 0.4
- [3] 0.66

#### Question 4: Precision=0.7 aur Recall=0.5 hone par F1-score kya hoga?
- [0] 0.58
- [1] 0.6
- [2] 0.65
- [3] 0.55

#### Question 5: Imbalanced data me accuracy 95% hai, lekin model sab negative predict karta hai. Iska Recall for positive class:
- [0] 0
- [1] 0.05
- [2] 0.95
- [3] 1.0

#### Question 6: Spam filter me sab emails ko 'spam' label karne par Recall 100% hoti hai. Precision is:
- [0] 0
- [1] 0.5
- [2] 1
- [3] Depends on dataset

#### Question 7: Confusion matrix ka transpose karne se kaun si metric galat calculate hogi?
- [0] Precision
- [1] Recall
- [2] Both
- [3] None

#### Question 8: F1-score low hone ka sabse common reason kya hai?
- [0] High precision, low recall
- [1] Low precision, high recall
- [2] Both precision and recall low
- [3] Either precision ya recall bahut low

#### Question 9: Medical test me false negative ka impact:
- [0] Less severe
- [1] More severe
- [2] Neutral
- [3] Depends on disease prevalence

#### Question 10: sklearn ka classification_report default kya return karta hai?
- [0] Precision, Recall, F1, Support per class
- [1] Only Accuracy
- [2] Confusion matrix
- [3] ROC AUC

### Quiz Answers & Explanations

- **Q1 Answer:** Option 0 — TP top‑right cell (actual positive, predicted positive) hai, jo 50 hai.
- **Q2 Answer:** Option 0 — Precision = 40/(40+20)=0.6667 ≈ 0.66.
- **Q3 Answer:** Option 0 — Recall = TP/(TP+FN)=40/(40+10)=0.8.
- **Q4 Answer:** Option 0 — F1 = 2*0.7*0.5/(0.7+0.5)=0.58.
- **Q5 Answer:** Option 0 — Positive class kabhi predict nahi hoti, isliye Recall = 0.
- **Q6 Answer:** Option 0 — Sab predicted spam, lekin bahut false positives, isliye Precision ≈ 0.
- **Q7 Answer:** Option 2 — TP, FP, FN, TN ki positions badal jati hain, dono Precision aur Recall galat ho jate hain.
- **Q8 Answer:** Option 3 — F1 harmonic mean hota hai; agar koi ek metric bahut low ho, F1 bhi low ho jata hai.
- **Q9 Answer:** Option 1 — False negative means missing a disease, jo patient ke liye bahut dangerous hota hai.
- **Q10 Answer:** Option 0 — classification_report detailed per‑class Precision, Recall, F1-score, aur support deta hai.

## Interview Questions

### Q1: Explain why accuracy can be misleading for imbalanced binary classification problems.

**Answer:** Accuracy counts overall correct predictions, so if 95% of data belongs to the negative class, a model that predicts every instance as negative will achieve 95% accuracy. However, it completely fails to identify any positive cases, giving a Recall of 0 for the minority class. In domains like fraud detection or medical diagnosis, missing the minority class is critical, so metrics like Precision, Recall, and F1-score are needed to capture the model's true performance on each class.

### Q2: How do you compute Precision, Recall, and F1-score from a confusion matrix?

**Answer:** From a 2x2 confusion matrix (rows = actual, columns = predicted):
- TP = matrix[1][1] (actual positive, predicted positive)
- FP = matrix[0][1] (actual negative, predicted positive)
- FN = matrix[1][0] (actual positive, predicted negative)
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 * (Precision * Recall) / (Precision + Recall).

### Q3: What is the intuition behind using the harmonic mean for F1-score instead of the arithmetic mean?

**Answer:** The harmonic mean penalizes extreme values more than the arithmetic mean. If either Precision or Recall is very low, the harmonic mean drops sharply, reflecting that a good model must perform well on both aspects. The arithmetic mean could hide a low value by averaging with a high one, giving a misleadingly optimistic score.

### Q4: Describe a real‑world scenario where you would prioritize Recall over Precision and why.

**Answer:** In cancer screening, missing a true cancer case (false negative) can be life‑threatening, while a false alarm (false positive) leads to additional tests but not immediate harm. Therefore, we set the decision threshold low to capture as many actual positives as possible, maximizing Recall even if Precision drops.

### Q5: How can you adjust a classifier to move along the Precision‑Recall trade‑off?

**Answer:** By changing the probability threshold used for class assignment. Lowering the threshold classifies more instances as positive, increasing Recall but potentially adding more false positives, which lowers Precision. Raising the threshold does the opposite, improving Precision at the cost of Recall. This adjustment lets you align the model with business priorities.
