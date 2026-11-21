# Revision Pack: Machine Learning Pipelines A-Z | Day 29 | 100 Days of Machine Learning

**One-Line Summary:** Classification evaluation mein Accuracy par rely mat karo; Confusion Matrix se Precision, Recall, F1, aur AUC-ROC use karo taaki imbalanced data mein model ki true performance pata chale.

## Cheat Sheet

| Metric | Formula | Intuition/Use Case |
| :--- | :--- | :--- |
| **Accuracy** | (TP + TN) / Total | Overall correctness. Imbalanced data mein misleading. |
| **Precision** | TP / (TP + FP) | 'Quality' of positives. Low FP chahiye (e.g., Spam filter). |
| **Recall** | TP / (TP + FN) | 'Coverage' of positives. Low FN chahiye (e.g., Cancer detection). |
| **F1-Score** | 2 * (P * R) / (P + R) | Harmonic mean. Balance between Precision & Recall. |
| **ROC Curve** | TPR vs FPR | Plot at various thresholds. |
| **AUC-ROC** | Area under ROC | 1.0 = Perfect, 0.5 = Random. Threshold-independent ranking. |

**Key Confusion Matrix Terms:**
*   **TP**: Predicted Positive, Actual Positive.
*   **TN**: Predicted Negative, Actual Negative.
*   **FP**: Predicted Positive, Actual Negative (Type I Error).
*   **FN**: Predicted Negative, Actual Positive (Type II Error).

## Flashcards

### Card 1
**Q:** Confusion Matrix ke 4 components kya hote hain?

**A:** True Positives (TP), True Negatives (TN), False Positives (FP), aur False Negatives (FN).

### Card 2
**Q:** Precision ka formula kya hai aur yeh kya batata hai?

**A:** TP / (TP + FP). Yeh batata hai ki jo positive predictions kiye gaye, unmein se kitne actually positive the (Quality).

### Card 3
**Q:** Recall (Sensitivity) ka formula kya hai?

**A:** TP / (TP + FN). Yeh batata hai ki actual positives mein se kitne ko model ne sahi se identify kiya (Coverage).

### Card 4
**Q:** F1-Score kaise calculate hota hai?

**A:** Precision aur Recall ka harmonic mean: 2 * (Precision * Recall) / (Precision + Recall).

### Card 5
**Q:** Accuracy imbalanced dataset mein kyun misleading ho sakti hai?

**A:** Kyunki agar majority class negative hai (e.g., 95%), toh model sabko negative predict karke 95% accuracy de sakta hai, lekin koi bhi positive case catch nahi karega.

### Card 6
**Q:** ROC Curve mein x-axis aur y-axis par kya hota hai?

**A:** X-axis: False Positive Rate (FPR). Y-axis: True Positive Rate (TPR/Recall).

### Card 7
**Q:** AUC-ROC value 1.0 aur 0.5 kya represent karti hai?

**A:** 1.0 = Perfect classifier, 0.5 = Random guess (coin flip).

### Card 8
**Q:** False Positive (FP) ko kis error type se jana jaata hai?

**A:** Type I Error (False Alarm).

### Card 9
**Q:** False Negative (FN) ko kis error type se jana jaata hai?

**A:** Type II Error (Missed Case).

### Card 10
**Q:** Spam filter mein Precision ya Recall mein se kaunsa zyada important hota hai aur kyun?

**A:** Precision. Kyunki innocent email ko spam mark karna (FP) user experience kharab karta hai, jabki kuch spam miss hona (FN) kam critical hai.

### Card 11
**Q:** Cancer detection mein Precision ya Recall mein se kaunsa zyada important hota hai?

**A:** Recall. Kyunki positive case ko miss karna (FN) life-threatening ho sakta hai, jabki false alarm (FP) sirf extra test ke liye hai.

### Card 12
**Q:** AUC-ROC threshold-dependent hai ya independent?

**A:** Threshold-independent. Yeh model ki overall ranking ability ko measure karta hai, specific threshold par performance nahi.

### Card 13
**Q:** F1-Score mein arithmetic mean ki jagah harmonic mean kyun use hota hai?

**A:** Harmonic mean tab zero hota hai jab Precision ya Recall mein se koi bhi zero ho. Yeh sahi behavior hai kyunki agar model kuch bhi sahi predict nahi kar raha, toh score zero hona chahiye.

### Card 14
**Q:** sklearn mein ROC curve plot karne ke liye kaunsa function use hota hai?

**A:** roc_curve(y_true, y_score) jo fpr, tpr, aur thresholds return karta hai.

### Card 15
**Q:** Precision aur Recall mein trade-off kaise hota hai?

**A:** Jab threshold change karte hain, toh ek badhta hai aur doosra ghatta hai. High precision = kam false alarms, High recall = kam missed cases.

## Quiz

#### Question 1: Agar ek model ne 100 positive cases mein se 80 sahi se predict kiye, toh Recall kitna hoga?
- [0] 80%
- [1] 20%
- [2] 50%
- [3] 100%

#### Question 2: Imbalanced dataset (95% Negative, 5% Positive) mein kaunsa metric best hai?
- [0] Accuracy
- [1] Precision
- [2] F1-Score
- [3] Mean Squared Error

#### Question 3: AUC-ROC value 0.5 ka matlab kya hai?
- [0] Perfect Classifier
- [1] Random Guess
- [2] Worst Classifier
- [3] Overfitting

#### Question 4: False Positive (FP) kya hota hai?
- [0] Actual Positive, Predicted Negative
- [1] Actual Negative, Predicted Positive
- [2] Actual Positive, Predicted Positive
- [3] Actual Negative, Predicted Negative

#### Question 5: Spam filter mein high Precision ka matlab kya hai?
- [0] Zyada spam emails miss hongi
- [1] Kam innocent emails spam mark hongi
- [2] Sab emails spam hongi
- [3] Kam spam emails catch hongi

#### Question 6: ROC Curve mein y-axis par kya hota hai?
- [0] False Positive Rate
- [1] True Positive Rate
- [2] Accuracy
- [3] F1-Score

#### Question 7: F1-Score ka formula kya hai?
- [0] (Precision + Recall) / 2
- [1] 2 * (Precision * Recall) / (Precision + Recall)
- [2] Precision * Recall
- [3] Precision / Recall

#### Question 8: Cancer detection mein high Recall kyun important hai?
- [0] Taaki kam false alarms hon
- [1] Taaki positive cases miss na hon
- [2] Taaki accuracy badhe
- [3] Taaki model fast ho

#### Question 9: AUC-ROC threshold par kya depend karta hai?
- [0] Specific threshold value
- [1] Overall ranking ability
- [2] Training time
- [3] Dataset size

#### Question 10: Agar Precision 0 hai, toh F1-Score kya hoga?
- [0] 1.0
- [1] 0.5
- [2] 0.0
- [3] Infinity

### Quiz Answers & Explanations

- **Q1 Answer:** Option 0 — Recall = TP / (TP + FN). Yahan TP=80, FN=20. Recall = 80/100 = 80%.
- **Q2 Answer:** Option 2 — Accuracy misleading ho sakti hai. F1-Score ya AUC-ROC zyada reliable hote hain kyunki yeh both classes ko consider karte hain.
- **Q3 Answer:** Option 1 — 0.5 AUC matlab model random guess jitna hi accha hai, koi discriminative power nahi hai.
- **Q4 Answer:** Option 1 — FP tab hota hai jab model ne negative class ko positive samajh liya (Type I Error).
- **Q5 Answer:** Option 1 — High Precision matlab jo emails spam mark ki gayi, unmein se zyada tar actually spam thi. Kam false alarms.
- **Q6 Answer:** Option 1 — Y-axis par True Positive Rate (TPR) ya Recall hota hai.
- **Q7 Answer:** Option 1 — F1-Score harmonic mean hai: 2PR / (P+R).
- **Q8 Answer:** Option 1 — Cancer mein FN (missed case) bahut dangerous hai, isliye Recall (catching all positives) priority hai.
- **Q9 Answer:** Option 1 — AUC threshold-independent hai, yeh model ki overall ability measure karta hai positive ko negative se alag karne ki.
- **Q10 Answer:** Option 2 — Harmonic mean mein agar koi bhi component zero ho, toh result zero hota hai.

## Interview Questions

### Q1: Accuracy aur F1-Score mein kya difference hai aur kab F1-Score prefer karte hain?

**Answer:** Accuracy total correct predictions ka ratio hai, jabki F1-Score Precision aur Recall ka harmonic mean hai. Imbalanced datasets mein Accuracy misleading ho sakti hai (e.g., 95% negative class mein 95% accuracy with 0% recall). F1-Score tab prefer karte hain jab humein Precision aur Recall dono ka balance chahiye, aur false positives aur false negatives ka cost similar hai.

### Q2: Precision aur Recall mein trade-off kaise samjhoge? Real-world example do.

**Answer:** Jab threshold change karte hain, toh Precision aur Recall inversely related hote hain. Agar threshold strict karo (high precision), toh kam false positives honge lekin kuch true positives miss ho jayenge (low recall). Spam filter example: High precision chahiye taaki innocent emails spam na hon, lekin isse kuch spam emails miss ho sakti hain. Cancer detection mein high recall chahiye taaki koi bhi patient miss na ho, lekin isse false alarms (extra tests) badh sakte hain.

### Q3: ROC Curve aur AUC-ROC kya hain? AUC 0.5 aur 1.0 kya batata hai?

**Answer:** ROC Curve TPR (Recall) vs FPR (1-Specificity) ka plot hai various thresholds par. AUC (Area Under Curve) is curve ke neeche ka area hai, jo model ki overall ranking ability ko summarize karta hai. AUC 1.0 matlab perfect classifier (sab positives ko negatives se alag kar pa raha hai). AUC 0.5 matlab random guess (model koi discriminative power nahi rakhta). AUC threshold-independent hai.

### Q4: Imbalanced dataset par model evaluate karne ke liye kaunse metrics use karoge aur kyun?

**Answer:** Accuracy avoid karunga kyunki majority class par biased ho sakti hai. Precision, Recall, F1-Score, aur AUC-ROC use karunga. Confusion Matrix dekhunga ki False Negatives kitne hain. Agar business problem mein false negatives costly hain (jaise fraud detection), toh Recall aur F1-Score par focus karunga. Agar false positives costly hain (jaise spam filter), toh Precision par focus karunga. AUC-ROC overall performance ke liye accha hai.

### Q5: False Positive aur False Negative ka business impact kaise alag hota hai? Ek example do.

**Answer:** False Positive (Type I Error) jab model ne negative ko positive samajh liya. False Negative (Type II Error) jab model ne positive ko negative samajh liya. Example: Email Spam Filter mein FP ka matlab innocent email spam folder mein jaana (user annoyance), FN ka matlab spam email inbox mein aana (minor issue). Lekin Medical Diagnosis mein FN ka matlab disease se chhoot jaana (life-threatening), FP ka matlab healthy ko sick samajhna (extra tests, manageable). Isliye metric selection business context par depend karta hai.
