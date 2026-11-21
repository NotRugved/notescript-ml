"""Code extracted from: Binning and Binarization | Discretization | Quantile Binning | KMeans Binning"""

#======================================================================
# Block 1: Calculating Confusion Matrix and Classification Report | Label: on-screen | Timestamp: 18:15
#======================================================================
from sklearn.metrics import confusion_matrix, classification_report

# Calculate Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Calculate Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

