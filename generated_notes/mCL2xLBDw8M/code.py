"""Code extracted from: Handling missing data | Numerical Data | Simple Imputer"""

#======================================================================
# Block 1: Calculating Classification Metrics | Label: on-screen | Timestamp: 12:00
#======================================================================
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Assuming y_true and y_pred are defined
print('Accuracy:', accuracy_score(y_true, y_pred))
print('Precision:', precision_score(y_true, y_pred))
print('Recall:', recall_score(y_true, y_pred))
print('F1-Score:', f1_score(y_true, y_pred))
print('Confusion Matrix:')
print(confusion_matrix(y_true, y_pred))


#======================================================================
# Block 2: Plotting ROC Curve | Label: on-screen | Timestamp: 19:00
#======================================================================
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

