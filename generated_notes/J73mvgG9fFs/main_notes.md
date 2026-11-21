# Handling Date and Time Variables | Day 34 | 100 Days of Machine Learning

**Video Link:** [https://www.youtube.com/watch?v=J73mvgG9fFs](https://www.youtube.com/watch?v=J73mvgG9fFs)

**Summary:** Confusion matrix se precision, recall, F1, ROC‑AUC tak, imbalanced data mein accuracy se aage ka model evaluation.

## Theory

### Introduction to Model Evaluation & Metrics ([10:00](https://youtu.be/J73mvgG9fFs?t=600))

Is segment mein teacher ne model evaluation ke concepts par baat shuru ki. Jab hum kisi machine learning model ko train karte hain, toh humein yeh jaanna hota hai ki model kitna accha hai. Iske liye humein evaluation metrics chahiye hote hain. Teacher ne explain kiya ki accuracy ke alawa bhi kai aur metrics hote hain jo specific scenarios mein zyada useful hote hain, especially jab data imbalanced ho.

### Confusion Matrix ([10:45](https://youtu.be/J73mvgG9fFs?t=645))

Confusion Matrix ek 2x2 table hai jo classification model ki performance ko detail mein dikhata hai. Isme 4 values hoti hain:
1. **True Positives (TP)**: Jo positive cases the aur model ne unhe positive predict kiya.
2. **False Positives (FP)**: Jo negative cases the lekin model ne unhe positive predict kiya (Type I error).
3. **True Negatives (TN)**: Jo negative cases the aur model ne unhe negative predict kiya.
4. **False Negatives (FN)**: Jo positive cases the lekin model ne unhe negative predict kiya (Type II error).

Teacher ne stress diya ki confusion matrix se humein pata chalta hai ki model kahan galti kar raha hai, sirf overall accuracy nahi.

### Precision and Recall ([11:30](https://youtu.be/J73mvgG9fFs?t=690))

**Precision** batata hai ki jab model ne positive predict kiya, toh kitne actually positive the.
Formula: Precision = TP / (TP + FP)

**Recall** (ya Sensitivity) batata hai ki actual positive cases mein se kitne ko model ne pakda.
Formula: Recall = TP / (TP + FN)

Teacher ne example diya ki agar hum cancer detection model bana rahe hain, toh Recall zyada important hai kyunki kisi cancer patient ko miss karna (False Negative) bahut dangerous hai. Lekin agar hum spam email filter bana rahe hain, toh Precision zyada important hai kyunki important email ko spam mark karna (False Positive) bura hai.

### F1 Score ([12:15](https://youtu.be/J73mvgG9fFs?t=735))

F1 Score hai Precision aur Recall ka harmonic mean. Jab humein dono metrics ka balance chahiye, toh F1 score use karte hain.
Formula: F1 = 2 * (Precision * Recall) / (Precision + Recall)

Teacher ne explain kiya ki F1 score tab best hota hai jab positive aur negative classes mein imbalance ho. Agar precision high hai lekin recall low hai, ya vice versa, toh F1 score low aayega, jo humein batata hai ki model balanced nahi hai.

### ROC Curve and AUC ([13:00](https://youtu.be/J73mvgG9fFs?t=780))

ROC (Receiver Operating Characteristic) Curve ek graph hai jo True Positive Rate (Recall) ko False Positive Rate ke against plot karta hai, different threshold values par.

**AUC (Area Under Curve)** ROC curve ke neeche ka area hai. 
- AUC = 1: Perfect classifier.
- AUC = 0.5: Random guess (no better than coin flip).
- AUC < 0.5: Worse than random.

Teacher ne bataya ki AUC ek single number hai jo model ki overall discriminative ability ko measure karta hai, threshold independent.

## Intuition

- ([11:30](https://youtu.be/J73mvgG9fFs?t=690)) Teacher ne kaha ki Precision aur Recall ko aise samjho: Precision 'kitne sahi positive the' hai, aur Recall 'kitne positive pakde gaye' hai. Cancer test mein Recall zyada chahiye kyunki miss karna fatal hai. Spam filter mein Precision zyada chahiye kyunki important mail miss karna bura hai.
- ([13:00](https://youtu.be/J73mvgG9fFs?t=780)) ROC Curve ko aise samjho ki aap ek dial ghuma rahe ho (threshold change kar rahe ho). Har position par aap dekhte ho ki kitne sahi positive pakde (TPR) aur kitne galat positive mark kiye (FPR). AUC batata hai ki overall yeh dial kitna accha kaam kar raha hai.

## Code

*No code blocks identified.*

## Analogies

- ([11:30](https://youtu.be/J73mvgG9fFs?t=690)) **Analogy:** Cancer detection vs Spam filter example — *Explains:* Yeh analogy explain karti hai ki different use cases mein Precision vs Recall ka trade-off kaise hota hai. Medical diagnosis mein False Negative (miss karna) zyada costly hai, isliye Recall optimize karte hain. Spam filter mein False Positive (important mail spam mark karna) costly hai, isliye Precision optimize karte hain.

## Common Mistakes

- **Mistake [teacher]:** Sirf Accuracy par rely karna imbalanced data mein ([10:45](https://youtu.be/J73mvgG9fFs?t=645))
  - *Why:* Agar 95% data negative hai, toh model har baar 'negative' predict karega aur 95% accuracy dega, lekin koi positive case catch nahi karega.
  - *Fix:* Precision, Recall, F1 Score, aur AUC use karo imbalanced datasets ke liye.
- **Mistake [added]:** F1 Score ko simple average samajhna ([12:15](https://youtu.be/J73mvgG9fFs?t=735))
  - *Why:* F1 harmonic mean hai, arithmetic mean nahi. Isliye agar ek metric 0 hai, toh F1 bhi 0 hoga, chahe doosra kitna bhi high ho.
  - *Fix:* Harmonic mean ki property samjho: 2*(P*R)/(P+R).

## Formulas & Key Terms

### Formulas
- **Precision:** `TP / (TP + FP)` — Predicted positives mein se kitne actually positive the.
- **Recall (Sensitivity):** `TP / (TP + FN)` — Actual positives mein se kitne ko model ne predict kiya.
- **F1 Score:** `2 * (Precision * Recall) / (Precision + Recall)` — Precision aur Recall ka harmonic mean, balanced measure.
- **AUC (Area Under ROC Curve):** `Integral of TPR w.r.t FPR` — Model ki overall discriminative ability, threshold independent.

### Key Terms
- **Confusion Matrix:** 2x2 table showing TP, FP, TN, FN counts.
- **True Positive (TP):** Correctly predicted positive case.
- **False Positive (FP):** Incorrectly predicted positive case (Type I error).
- **True Negative (TN):** Correctly predicted negative case.
- **False Negative (FN):** Incorrectly predicted negative case (Type II error).
- **Precision:** Proportion of predicted positives that are actually positive.
- **Recall:** Proportion of actual positives that are correctly predicted.
- **F1 Score:** Harmonic mean of Precision and Recall.
- **ROC Curve:** Plot of TPR vs FPR at various thresholds.
- **AUC:** Area Under the ROC Curve, single metric for model performance.
