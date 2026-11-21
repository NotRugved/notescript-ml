# Revision Pack: Handling missing data | Numerical Data | Simple Imputer

**One-Line Summary:** Model evaluation ke liye confusion matrix se precision, recall, F1 aur ROC‑AUC ko samjho, especially imbalanced data mein.

## Cheat Sheet

- **Confusion Matrix**: TP, TN, FP, FN counts
- **Accuracy**: (TP+TN)/(TP+TN+FP+FN) – overall correctness, par imbalance pe misleading
- **Precision**: TP/(TP+FP) – predicted positives ki quality (high FP penalty)
- **Recall (Sensitivity)**: TP/(TP+FN) – actual positives ko kitna pakda (high FN penalty)
- **F1‑Score**: 2*(Precision*Recall)/(Precision+Recall) – precision‑recall ka balance, harmonic mean
- **Specificity**: TN/(TN+FP) – true negative rate
- **ROC Curve**: TPR (Recall) vs FPR (1‑Specificity) across thresholds
- **AUC**: ROC ka area, 1 = perfect, 0.5 = random
- **When to use**: Imbalanced data → prefer Precision, Recall, F1, AUC over Accuracy; high FP cost → Precision; high FN cost → Recall.

## Flashcards

### Card 1
**Q:** Confusion Matrix ke 4 components kaunse hain?

**A:** True Positive (TP), True Negative (TN), False Positive (FP), False Negative (FN)

### Card 2
**Q:** Accuracy ka formula kya hai?

**A:** (TP + TN) / (TP + TN + FP + FN)

### Card 3
**Q:** Precision kis cheez ko measure karta hai?

**A:** Predicted positives ki correctness, i.e., TP/(TP+FP)

### Card 4
**Q:** Recall ka doosra naam kya hai?

**A:** Sensitivity ya True Positive Rate

### Card 5
**Q:** Recall ka formula kya hai?

**A:** TP / (TP + FN)

### Card 6
**Q:** F1‑Score kaise calculate karte hain?

**A:** 2 * (Precision * Recall) / (Precision + Recall)

### Card 7
**Q:** ROC curve ka x‑axis kya dikhata hai?

**A:** False Positive Rate (FPR) = FP/(FP+TN)

### Card 8
**Q:** AUC ka ideal value kya hota hai?

**A:** 1.0, jo perfect classifier ko indicate karta hai

### Card 9
**Q:** Imbalanced dataset mein Accuracy kyun misleading ho sakti hai?

**A:** Kyuki model majority class ko hamesha predict karke high accuracy de sakta hai, lekin minority class ko miss kar sakta hai

### Card 10
**Q:** Spam detection mein high precision ka kya fayda hai?

**A:** Galat email ko spam mark karne ki error (FP) kam hoti hai

### Card 11
**Q:** Medical diagnosis mein high recall ka kyun importance hai?

**A:** False negatives (missed disease) ko minimize karta hai

### Card 12
**Q:** Specificity ka formula kya hai?

**A:** TN / (TN + FP)

### Card 13
**Q:** ROC curve banane ke liye sklearn ka kaunsa function use hota hai?

**A:** roc_curve

### Card 14
**Q:** AUC ko calculate karne ke liye sklearn ka kaunsa function use hota hai?

**A:** auc

### Card 15
**Q:** F1‑Score low hone ka sabse common reason kya hota hai?

**A:** Precision aur Recall me se koi ek bahut low ho, kyunki harmonic mean dono ko punish karta hai

## Quiz

#### Question 1: Agar ek model sabhi samples ko 'No Cancer' predict karta hai aur dataset me 95% patients healthy hain, to model ki accuracy kya hogi?
- [0] 95%
- [1] 5%
- [2] 100%
- [3] 0%

#### Question 2: Precision ka high value indicate karta hai:
- [0] Few false positives
- [1] Few false negatives
- [2] High overall accuracy
- [3] High recall

#### Question 3: Recall ka high value indicate karta hai:
- [0] Few false positives
- [1] Few false negatives
- [2] High specificity
- [3] High precision

#### Question 4: F1‑Score ka value 0.0 hone ka sabse likely scenario kya hai?
- [0] Precision = 0, Recall = 0
- [1] Precision = 1, Recall = 0
- [2] Precision = 0, Recall = 1
- [3] Precision = 0.5, Recall = 0.5

#### Question 5: ROC curve ka diagonal line (0,0) se (1,1) tak kya represent karta hai?
- [0] Random classifier
- [1] Perfect classifier
- [2] Worst classifier
- [3] Threshold = 0.5

#### Question 6: AUC = 0.5 ka matlab hai:
- [0] Model random guessing karta hai
- [1] Model perfect hai
- [2] Model overfitting hai
- [3] Model underfitting hai

#### Question 7: Imbalanced dataset me kaunse metric ko sabse pehle dekhna chahiye?
- [0] Accuracy
- [1] Precision
- [2] Recall
- [3] Mean Squared Error

#### Question 8: Confusion Matrix me False Positive ka dusra naam kya hai?
- [0] Type I Error
- [1] Type II Error
- [2] False Negative
- [3] True Negative

#### Question 9: Sklearn me confusion matrix print karne ke liye kaun sa function use hota hai?
- [0] confusion_matrix()
- [1] classification_report()
- [2] accuracy_score()
- [3] roc_auc_score()

#### Question 10: Agar ek spam filter ka Precision 0.9 aur Recall 0.5 hai, to F1‑Score approx kya hoga?
- [0] 0.64
- [1] 0.75
- [2] 0.55
- [3] 0.90

### Quiz Answers & Explanations

- **Q1 Answer:** Option 0 — Model sabhi healthy cases correctly predict karta hai (95%) aur cancer cases galat, isliye accuracy = 95%.
- **Q2 Answer:** Option 0 — Precision = TP/(TP+FP); high precision means FP bahut kam, yani positive predictions reliable.
- **Q3 Answer:** Option 1 — Recall = TP/(TP+FN); high recall means FN bahut kam, yani actual positives ko zyada pakda.
- **Q4 Answer:** Option 0 — F1 = 2PR/(P+R); agar dono Precision aur Recall zero hain to F1 bhi zero hota hai.
- **Q5 Answer:** Option 0 — Diagonal line ka area 0.5 hota hai, jo random guessing ko represent karta hai.
- **Q6 Answer:** Option 0 — AUC 0.5 ka matlab hai ROC curve diagonal, jo random classifier ke barabar hota hai.
- **Q7 Answer:** Option 2 — Recall (ya F1) minority class ko capture karne ki ability batata hai, jo imbalance me crucial hota hai.
- **Q8 Answer:** Option 0 — FP ko Type I Error bhi kaha jata hai.
- **Q9 Answer:** Option 0 — sklearn.metrics.confusion_matrix() confusion matrix return karta hai.
- **Q10 Answer:** Option 0 — F1 = 2*(0.9*0.5)/(0.9+0.5) = 0.9/(1.4) ≈ 0.64.

## Interview Questions

### Q1: Explain why accuracy can be misleading for imbalanced classification problems and give an example.

**Answer:** Accuracy counts overall correct predictions, so if one class dominates, a model that always predicts the majority class can achieve high accuracy while completely ignoring the minority class. Example: In a cancer screening dataset with 95% healthy patients, a model that always predicts 'No Cancer' gets 95% accuracy but fails to detect any cancer case, making it useless.

### Q2: What is the difference between precision and recall? When would you prioritize one over the other?

**Answer:** Precision = TP/(TP+FP) measures how many predicted positives are actually correct; it penalizes false positives. Recall = TP/(TP+FN) measures how many actual positives are captured; it penalizes false negatives. Prioritize precision when the cost of a false positive is high (e.g., spam filter marking legit email as spam). Prioritize recall when missing a positive is costly (e.g., medical diagnosis, fraud detection).

### Q3: How does the F1‑Score combine precision and recall, and why is the harmonic mean used instead of the arithmetic mean?

**Answer:** F1 = 2 * (Precision * Recall) / (Precision + Recall). The harmonic mean gives more weight to low values, so if either precision or recall is low, the F1‑Score drops sharply. This property ensures that a model must perform well on both aspects to achieve a high F1, unlike the arithmetic mean which could be high even if one metric is very low.

### Q4: Describe how you would plot an ROC curve and interpret the AUC value for a binary classifier.

**Answer:** Use sklearn.metrics.roc_curve(y_true, y_score) to get false positive rates (FPR), true positive rates (TPR), and thresholds. Plot FPR on the x‑axis and TPR on the y‑axis. Compute AUC with sklearn.metrics.auc(fpr, tpr). AUC close to 1 indicates the classifier separates classes well across all thresholds; 0.5 means random performance; below 0.5 suggests the model is inversely predicting.

### Q5: What are some common pitfalls when using the confusion matrix for model evaluation, and how can you mitigate them?

**Answer:** Pitfalls include focusing only on overall accuracy, ignoring class imbalance, and misinterpreting FP vs FN costs. Mitigation: Look at per‑class metrics (precision, recall, F1), use ROC‑AUC for threshold‑independent evaluation, and choose the metric that aligns with business cost (e.g., maximize recall for disease detection). Also, consider resampling techniques or class weighting to address imbalance.
