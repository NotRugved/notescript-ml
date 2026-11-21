# Handling missing data | Numerical Data | Simple Imputer

**Video Link:** [https://www.youtube.com/watch?v=mCL2xLBDw8M](https://www.youtube.com/watch?v=mCL2xLBDw8M)

**Summary:** Model evaluation ke liye confusion matrix se precision, recall, F1 aur ROC‑AUC ko samjho, especially imbalanced data mein.

## Theory

### Introduction to Model Evaluation & Metrics ([10:00](https://youtu.be/mCL2xLBDw8M?t=600))

Teacher explains that once we train a model, we need to evaluate how well it performs. We cannot just look at the training accuracy; we need to check generalization. The segment introduces the concept of splitting data into training and testing sets to get an unbiased estimate of model performance. It emphasizes that metrics like accuracy, precision, recall, and F1-score are crucial for understanding different aspects of model behavior, especially in imbalanced datasets.

### Confusion Matrix ([11:30](https://youtu.be/mCL2xLBDw8M?t=690))

The Confusion Matrix is a table used to describe the performance of a classification information system. It has four components:
1. **True Positives (TP)**: Actual Positive, Predicted Positive.
2. **True Negatives (TN)**: Actual Negative, Predicted Negative.
3. **False Positives (FP)**: Actual Negative, Predicted Positive (Type I Error).
4. **False Negatives (FN)**: Actual Positive, Predicted Negative (Type II Error).

The teacher walks through a medical diagnosis example: Predicting cancer (Positive) vs No Cancer (Negative). A False Positive means telling a healthy person they have cancer (scary but maybe less fatal than missing it), while a False Negative means telling a sick person they are healthy (dangerous). The matrix helps visualize these trade-offs.

### Accuracy ([13:00](https://youtu.be/mCL2xLBDw8M?t=780))

Accuracy is the ratio of correct predictions to total predictions.
Formula: $Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$

The teacher warns that accuracy can be misleading in imbalanced datasets. For example, if 95% of patients are healthy and 5% have cancer, a model that predicts 'No Cancer' for everyone will have 95% accuracy but is useless because it misses all cancer cases. This is the 'Accuracy Paradox'.

### Precision ([14:30](https://youtu.be/mCL2xLBDw8M?t=870))

Precision measures how many of the predicted positives were actually positive.
Formula: $Precision = \frac{TP}{TP + FP}$

It answers: 'Of all the cases I predicted as positive, how many were correct?' High precision means few False Positives. This is important when the cost of a False Positive is high (e.g., spam detection, where marking a real email as spam is bad).

### Recall (Sensitivity) ([15:30](https://youtu.be/mCL2xLBDw8M?t=930))

Recall measures how many of the actual positives were correctly identified.
Formula: $Recall = \frac{TP}{TP + FN}$

It answers: 'Of all the actual positive cases, how many did I catch?' High recall means few False Negatives. This is critical in medical diagnosis or fraud detection, where missing a positive case (False Negative) is very costly.

### F1-Score ([17:00](https://youtu.be/mCL2xLBDw8M?t=1020))

The F1-Score is the harmonic mean of Precision and Recall. It provides a single metric that balances both.
Formula: $F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}$

The teacher explains that if Precision is high but Recall is low (or vice versa), the F1-score will be low. It is the best metric to use when you need a balance between Precision and Recall, especially in imbalanced datasets.

### ROC Curve and AUC ([18:30](https://youtu.be/mCL2xLBDw8M?t=1110))

The ROC (Receiver Operating Characteristic) curve plots the True Positive Rate (Recall) against the False Positive Rate (1 - Specificity) at various threshold settings.
- **TPR (Sensitivity)**: $\frac{TP}{TP + FN}$
- **FPR**: $\frac{FP}{FP + TN}$

The AUC (Area Under the Curve) summarizes the ROC curve into a single value. An AUC of 1.0 is a perfect classifier, while 0.5 is equivalent to random guessing. The teacher shows how to plot this using `roc_curve` and `auc` from sklearn.

## Intuition

- ([11:45](https://youtu.be/mCL2xLBDw8M?t=705)) Socho aap ek doctor ho. Agar aap har patient ko 'Cancer hai' bol do, toh aapki accuracy high hogi agar zyada log healthy hain, lekin aap useless ho kyunki aapne kisi ko sahi diagnose nahi kiya. Confusion Matrix aapko batata hai ki aapne kitne sahi pakde (TP), kitne galat pakde (FP), kitne miss kiye (FN), aur kitne sahi chhod diye (TN).
- ([14:40](https://youtu.be/mCL2xLBDw8M?t=880)) Precision ka matlab hai 'Kitne bharosemand hain aapke positive predictions?' Agar aap 10 logon ko spam mark karte ho aur 9 mein se 9 spam hain, toh precision high hai. Recall ka matlab hai 'Kitne sachche positives aapne pakde?' Agar 100 spam emails aayi aur aapne 90 pakdi, toh recall high hai.
- ([17:15](https://youtu.be/mCL2xLBDw8M?t=1035)) F1-Score jaise ek balance hai. Agar aap sirf precision dekhoge toh aap kam se kam predict karoge taaki galat na ho, lekin miss ho jayenge. Agar sirf recall dekhoge toh aap sabko positive bol doge. F1 dono ko balance karta hai.

## Code

### Calculating Classification Metrics [on-screen] ([12:00](https://youtu.be/mCL2xLBDw8M?t=720))
Code snippet showing how to calculate accuracy, precision, recall, and F1-score using sklearn.metrics.

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Assuming y_true and y_pred are defined
print('Accuracy:', accuracy_score(y_true, y_pred))
print('Precision:', precision_score(y_true, y_pred))
print('Recall:', recall_score(y_true, y_pred))
print('F1-Score:', f1_score(y_true, y_pred))
print('Confusion Matrix:')
print(confusion_matrix(y_true, y_pred))
```

### Plotting ROC Curve [on-screen] ([19:00](https://youtu.be/mCL2xLBDw8M?t=1140))
Code to plot the ROC curve and calculate AUC.

```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Assuming y_true and y_score (probabilities) are defined
fpr, tpr, thresholds = roc_curve(y_true, y_score)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()
```

## Analogies

- ([11:45](https://youtu.be/mCL2xLBDw8M?t=705)) **Analogy:** Doctor diagnosing cancer. False Positive = Telling a healthy person they have cancer. False Negative = Telling a sick person they are healthy. — *Explains:* Illustrates the real-world cost of different types of errors in classification, helping to understand why Precision and Recall are important in different contexts.
- ([14:40](https://youtu.be/mCL2xLBDw8M?t=880)) **Analogy:** Spam email detection. Precision = How many of the emails marked as spam were actually spam? Recall = How many of the actual spam emails were caught? — *Explains:* Simplifies the abstract concepts of Precision and Recall using a common everyday example.

## Common Mistakes

- **Mistake [teacher]:** Relying solely on Accuracy for imbalanced datasets. ([13:15](https://youtu.be/mCL2xLBDw8M?t=795))
  - *Why:* Accuracy can be high even if the model is useless (e.g., predicting the majority class always).
  - *Fix:* Use Precision, Recall, F1-Score, or AUC-ROC instead.
- **Mistake [added]:** Confusing Precision and Recall. ([15:00](https://youtu.be/mCL2xLBDw8M?t=900))
  - *Why:* Both involve TP, but Precision divides by (TP+FP) while Recall divides by (TP+FN).
  - *Fix:* Remember: Precision is about the quality of positive predictions, Recall is about the quantity of actual positives caught.

## Formulas & Key Terms

### Formulas
- **Accuracy:** `(TP + TN) / (TP + TN + FP + FN)` — Proportion of correct predictions out of total predictions.
- **Precision:** `TP / (TP + FP)` — Proportion of positive predictions that were actually positive.
- **Recall:** `TP / (TP + FN)` — Proportion of actual positives that were correctly identified.
- **F1-Score:** `2 * (Precision * Recall) / (Precision + Recall)` — Harmonic mean of Precision and Recall, balancing both.
- **AUC-ROC:** `Area under the ROC curve` — Summary of the model's ability to distinguish between classes across all thresholds.

### Key Terms
- **Confusion Matrix:** A table showing TP, TN, FP, FN counts.
- **True Positive (TP):** Correctly predicted positive.
- **False Positive (FP):** Incorrectly predicted positive (Type I Error).
- **False Negative (FN):** Incorrectly predicted negative (Type II Error).
- **Precision:** Quality of positive predictions.
- **Recall:** Quantity of actual positives caught.
- **F1-Score:** Balance between Precision and Recall.
- **ROC Curve:** Plot of TPR vs FPR at various thresholds.
- **AUC:** Area Under the ROC Curve, a single value summarizing model performance.
