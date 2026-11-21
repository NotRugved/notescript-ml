"""Code extracted from: Outlier Detection using the Percentile Method | Winsorization Technique"""

#======================================================================
# Block 1: Simple Gradient Descent for Linear Regression | Label: on-screen | Timestamp: 13:00
#======================================================================
import numpy as np

def compute_loss(X, y, w, b):
    N = len(y)
    preds = w * X + b
    loss = np.sum((y - preds) ** 2) / (2 * N)
    return loss

def gradient_descent(X, y, w_init, b_init, alpha, epochs):
    w, b = w_init, b_init
    for i in range(epochs):
        preds = w * X + b
        dw = -np.sum((y - preds) * X) / len(X)
        db = -np.sum(y - preds) / len(X)
        w = w - alpha * dw
        b = b - alpha * db
    return w, b

# Example usage
X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])
w_init, b_init = 0.0, 0.0
alpha = 0.01
epochs = 1000
w_final, b_final = gradient_descent(X, y, w_init, b_init, alpha, epochs)
print('Learned w:', w_final, 'b:', b_final)

