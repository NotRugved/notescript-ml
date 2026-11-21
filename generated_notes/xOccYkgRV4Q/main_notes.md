# Machine Learning Pipelines A-Z | Day 29 | 100 Days of Machine Learning

**Video Link:** [https://www.youtube.com/watch?v=xOccYkgRV4Q](https://www.youtube.com/watch?v=xOccYkgRV4Q)

**Summary:** Classification evaluation mein Accuracy par rely mat karo; Confusion Matrix se Precision, Recall, F1, aur AUC-ROC use karo taaki imbalanced data mein model ki true performance pata chale.

## Theory

### Introduction to Model Evaluation & Metrics ([20:00](https://youtu.be/xOccYkgRV4Q?t=1200))

Teacher discusses the importance of evaluating machine learning models. He explains that after training a model, we need to measure its performance. The segment covers the basics of how we assess if a model is good or bad using various metrics. He emphasizes that different problems (classification vs regression) require different evaluation strategies.

### Confusion Matrix Basics ([22:15](https://youtu.be/xOccYkgRV4Q?t=1335))

The teacher introduces the Confusion Matrix as a fundamental tool for classification problems. He explains it is a table that summarizes the performance of a classification algorithm on a set of observations for which the true values are known. It contains four key components: True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN). He walks through what each term means in the context of a binary classification problem.

### Accuracy, Precision, Recall, and F1-Score ([25:30](https://youtu.be/xOccYkgRV4Q?t=1530))

The lecture moves on to specific metrics derived from the confusion matrix. 
1. **Accuracy**: The ratio of correct predictions to total predictions. Formula: (TP + TN) / (TP + TN + FP + FN). Teacher notes it is not always the best metric, especially in imbalanced datasets.
2. **Precision**: The ratio of true positives to all predicted positives. Formula: TP / (TP + FP). It answers: 'Of all the positive predictions, how many were actually correct?'
3. **Recall (Sensitivity)**: The ratio of true positives to all actual positives. Formula: TP / (TP + FN). It answers: 'Of all the actual positives, how many did we correctly identify?'
4. **F1-Score**: The harmonic mean of precision and recall. Formula: 2 * (Precision * Recall) / (Precision + Recall). It provides a balance between precision and recall.

### ROC Curve and AUC ([28:00](https://youtu.be/xOccYkgRV4Q?t=1680))

The teacher introduces the Receiver Operating Characteristic (ROC) curve. He explains it is a plot of the True Positive Rate (Recall) against the False Positive Rate (1 - Specificity) at various threshold settings. The Area Under the Curve (AUC) is a single number that summarizes the ROC curve. An AUC of 1.0 indicates a perfect classifier, while 0.5 indicates a random guess. He explains how to interpret the curve and why AUC is preferred over accuracy for imbalanced datasets.

### Introduction to Model Evaluation Metrics ([40:00](https://youtu.be/xOccYkgRV4Q?t=2400))

Is segment mein teacher ne discuss kiya ki classification models ko evaluate karne ke liye sirf accuracy kaafi nahi hoti, khaaskar jab data imbalanced ho. Unhone bataya ki humein confusion matrix ke through precision, recall, F1-score, aur ROC-AUC curve samajhna hoga. Teacher ne stress diya ki interview mein accuracy ke alawa in metrics ke baare mein poocha jaata hai kyunki real-world problems mein false positives aur false negatives ka impact alag-alag hota hai.

### Confusion Matrix Deep Dive ([40:45](https://youtu.be/xOccYkgRV4Q?t=2445))

Teacher ne confusion matrix ke 4 components ko detail mein samjhaya: True Positives (TP), True Negatives (TN), False Positives (FP), aur False Negatives (FN). Unhone explain kiya ki TP tab hota hai jab model ne positive class ko sahi se predict kiya, TN jab negative class sahi predict hui, FP jab model ne negative ko positive samajh liya (Type I error), aur FN jab model ne positive ko negative samajh liya (Type II error). Yeh matrix hi baaki sab metrics ka base hai.

### Precision and Recall ([41:30](https://youtu.be/xOccYkgRV4Q?t=2490))

Precision ka formula hai TP / (TP + FP). Iska matlab hai ki jo samples model ne positive predict kiye, unmein se kitne actually positive the. Recall ka formula hai TP / (TP + FN). Iska matlab hai ki jo actually positive the, unmein se kitne ko model ne sahi se pakda. Teacher ne bataya ki precision aur recall mein trade-off hota hai. Agar threshold change karo toh ek badhega aur doosra ghatega. High precision matlab kam false alarms, high recall matlab kam missed cases.

### F1-Score ([42:15](https://youtu.be/xOccYkgRV4Q?t=2535))

F1-score precision aur recall ka harmonic mean hai. Formula hai 2 * (Precision * Recall) / (Precision + Recall). Yeh tab use hota hai jab humein precision aur recall dono ka balance chahiye. Teacher ne explain kiya ki arithmetic mean ki jagah harmonic mean isliye use hota hai kyunki agar precision ya recall mein se koi bhi zero ho, toh F1-score bhi zero ho jayega, jo ki sahi behavior hai kyunki agar model kuch bhi sahi predict nahi kar raha toh score zero hona chahiye.

### ROC Curve and AUC ([43:00](https://youtu.be/xOccYkgRV4Q?t=2580))

ROC (Receiver Operating Characteristic) curve ek plot hai jisme x-axis par False Positive Rate (FPR) aur y-axis par True Positive Rate (TPR, jo ki recall hai) hota hai. Har threshold value ke liye ek point plot hota hai. AUC (Area Under Curve) is curve ke neeche ka area hai. AUC 1.0 matlab perfect classifier, 0.5 matlab random guess. Teacher ne bataya ki AUC threshold-independent hai, matlab yeh model ki overall ranking ability ko measure karta hai, specific threshold par performance nahi.

### Choosing the Right Metric ([44:00](https://youtu.be/xOccYkgRV4Q?t=2640))

Teacher ne examples ke through bataya ki kaunsa metric kab use karna hai. Agar false positive ka nuksan zyada hai (jaise spam filter mein innocent mail ko spam mark karna), toh precision zyada important hai. Agar false negative ka nuksan zyada hai (jaise cancer detection mein positive case ko miss karna), toh recall zyada important hai. Imbalanced datasets mein accuracy misleading ho sakti hai, isliye F1-score ya AUC zyada reliable hote hain.

## Intuition

- ([21:00](https://youtu.be/xOccYkgRV4Q?t=1260)) Teacher uses the analogy of a medical test to explain confusion matrix. If a test says you have a disease (Positive) and you actually do (True Positive), that's good. If it says you have it but you don't (False Positive), that's a false alarm. If it says you don't have it but you actually do (False Negative), that's a dangerous miss. This helps in understanding why different metrics matter in different contexts.
- ([26:00](https://youtu.be/xOccYkgRV4Q?t=1560)) For Precision vs Recall, teacher explains: Precision is about 'quality' of positive predictions (how many of my 'yes' answers were right?). Recall is about 'quantity' or coverage (how many of the actual 'yes' cases did I catch?). In a spam filter, high precision means few non-spam emails are marked as spam. High recall means few spam emails are missed.
- ([41:45](https://youtu.be/xOccYkgRV4Q?t=2505)) Precision ko aise samjho: Agar tumne 10 logon ko 'criminal' label diya, aur unmein se 8 actually criminal the, toh precision 80% hai. Yeh tumhare 'accusations' ki quality batata hai.
- ([42:00](https://youtu.be/xOccYkgRV4Q?t=2520)) Recall ko aise samjho: Agar actually 100 criminals the, aur tumne unmein se 80 ko pakda, toh recall 80% hai. Yeh tumhari 'detection ability' batata hai.
- ([43:15](https://youtu.be/xOccYkgRV4Q?t=2595)) ROC curve ko aise samjho: Tum ek dial ghuma rahe ho (threshold change kar rahe ho). Har position par tum dekh rahe ho ki kitne innocent logon ko tum galat pakad rahe ho (FPR) aur kitne guilty logon ko tum sahi pakad rahe ho (TPR). AUC yeh batata hai ki tumhara dial kitna accha hai overall.

## Code

### Calculating Classification Metrics [on-screen] ([23:00](https://youtu.be/xOccYkgRV4Q?t=1380))
Code snippet showing how to calculate accuracy, precision, recall, and F1-score using sklearn.metrics.

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Example predictions and actuals
y_true = [0, 1, 0, 1, 1, 0, 1, 0]
y_pred = [0, 1, 1, 1, 0, 0, 1, 0]

print('Accuracy:', accuracy_score(y_true, y_pred))
print('Precision:', precision_score(y_true, y_pred))
print('Recall:', recall_score(y_true, y_pred))
print('F1-Score:', f1_score(y_true, y_pred))
```

### Plotting ROC Curve [on-screen] ([28:30](https://youtu.be/xOccYkgRV4Q?t=1710))
Code to generate and plot the ROC curve and calculate AUC.

```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Assuming y_score contains predicted probabilities
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

- ([21:00](https://youtu.be/xOccYkgRV4Q?t=1260)) **Analogy:** Medical test for disease detection. — *Explains:* Explains True Positives, False Positives, True Negatives, and False Negatives in a relatable context. Highlights the cost of different types of errors (e.g., missing a disease is worse than a false alarm in some cases).
- ([26:00](https://youtu.be/xOccYkgRV4Q?t=1560)) **Analogy:** Spam email filter. — *Explains:* Differentiates between Precision (avoiding marking good emails as spam) and Recall (catching all spam emails). Shows how the choice of metric depends on the business problem.
- ([41:45](https://youtu.be/xOccYkgRV4Q?t=2505)) **Analogy:** Criminal detection analogy: Precision = accuracy of accusations, Recall = ability to catch all criminals — *Explains:* Yeh analogy precision aur recall ke difference ko clear karti hai. Precision focus karta hai ki jo tumne pakda, wo sahi tha ya nahi. Recall focus karta hai ki jo pakda jaana chahiye tha, wo pakda gaya ya nahi.
- ([43:15](https://youtu.be/xOccYkgRV4Q?t=2595)) **Analogy:** Dial/Threshold analogy for ROC curve — *Explains:* Yeh analogy samjhati hai ki ROC curve ek single point nahi hai, balki ek range of thresholds par model ki performance ka visualization hai. AUC yeh batata hai ki overall model kitna accha ranker hai.

## Common Mistakes

- **Mistake [teacher]:** Using Accuracy as the sole metric for imbalanced datasets. ([25:45](https://youtu.be/xOccYkgRV4Q?t=1545))
  - *Why:* In a dataset with 95% negatives and 5% positives, a model that predicts all negatives will have 95% accuracy but is useless for detecting the positive class.
  - *Fix:* Use Precision, Recall, F1-Score, or AUC-ROC instead of Accuracy for imbalanced problems.
- **Mistake [added]:** Confusing Precision and Recall. ([26:10](https://youtu.be/xOccYkgRV4Q?t=1570))
  - *Why:* Both involve True Positives, but their denominators are different. Precision divides by total predicted positives, Recall divides by total actual positives.
  - *Fix:* Remember: Precision = 'How good are my positive predictions?', Recall = 'How many positives did I find?'
- **Mistake [teacher]:** Sirf accuracy par rely karna imbalanced datasets mein ([44:10](https://youtu.be/xOccYkgRV4Q?t=2650))
  - *Why:* Agar 95% samples negative hain, toh model sabko negative predict karke 95% accuracy de sakta hai, lekin koi bhi positive case catch nahi karega.
  - *Fix:* Precision, Recall, F1-score, ya AUC use karo. Confusion matrix dekho ki false negatives kitne hain.
- **Mistake [teacher]:** Precision aur Recall ko confuse karna ([41:50](https://youtu.be/xOccYkgRV4Q?t=2510))
  - *Why:* Dono mein TP hota hai, lekin denominator alag hai. Precision mein FP add hota hai, Recall mein FN add hota hai.
  - *Fix:* Yaad rakho: Precision = 'How good are my positives?', Recall = 'How many positives did I find?'
- **Mistake [added]:** AUC ko threshold-specific performance samajhna ([43:20](https://youtu.be/xOccYkgRV4Q?t=2600))
  - *Why:* AUC overall ranking ability batata hai, specific threshold par precision/recall nahi.
  - *Fix:* Agar specific threshold par performance chahiye, toh ROC curve par us threshold ka point dekho ya precision-recall curve use karo.

## Formulas & Key Terms

### Formulas
- **Accuracy:** `(TP + TN) / (TP + TN + FP + FN)` — Proportion of correct predictions out of total predictions.
- **Precision:** `TP / (TP + FP)` — Proportion of true positives among all predicted positives.
- **Recall (Sensitivity):** `TP / (TP + FN)` — Proportion of actual positives that were correctly identified.
- **F1-Score:** `2 * (Precision * Recall) / (Precision + Recall)` — Harmonic mean of Precision and Recall, providing a balanced measure.
- **AUC-ROC:** `Area under the ROC curve` — Single number summarizing the model's ability to distinguish between classes across all thresholds.
- **Recall (Sensitivity/TPR):** `TP / (TP + FN)` — Jo actually positive the, unmein se kitne ko model ne sahi se predict kiya.
- **False Positive Rate (FPR):** `FP / (FP + TN)` — Jo actually negative the, unmein se kitne ko model ne galat positive predict kiya.
- **AUC (Area Under ROC Curve):** `Integral of TPR with respect to FPR` — Model ki overall ability to rank positive instances higher than negative ones.

### Key Terms
- **Confusion Matrix:** A table used to describe the performance of a classification model on a set of test data for which the true values are known.
- **True Positive (TP):** Correctly predicted positive class.
- **False Positive (FP):** Incorrectly predicted positive class (Type I error).
- **True Negative (TN):** Correctly predicted negative class.
- **False Negative (FN):** Incorrectly predicted negative class (Type II error).
- **Precision:** Measure of how many of the predicted positives were actually positive.
- **Recall:** Measure of how many of the actual positives were correctly predicted.
- **F1-Score:** Harmonic mean of precision and recall, useful when you need a balance between the two.
- **ROC Curve:** A plot of True Positive Rate vs False Positive Rate at various thresholds.
- **AUC:** Area Under the ROC Curve, a single metric to evaluate the overall performance of a classifier.
- **Imbalanced Dataset:** Jahan classes ke samples ka ratio bahut alag hai, jaise 95:5.
