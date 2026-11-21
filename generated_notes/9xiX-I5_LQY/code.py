"""Code extracted from: Handling Mixed Variables | Feature Engineering"""

#======================================================================
# Block 1: Linear regression gradient descent (on-screen) | Label: on-screen | Timestamp: 06:30
#======================================================================
import numpy as np

# Sample data
X = np.array([[1, 2],   # bias term + feature
               [2, 3],
               [4, 5]])

y = np.array([5, 7, 9])

# Initialize parameters (theta0, theta1)
theta = np.zeros(2)

# Hyperparameters
alpha = 0.01          # learning rate
m = X.shape[0]      # number of training examples
epochs = 1000

for _ in range(epochs):
    predictions = X @ theta               # h_the(x)
    error = predictions - y               # residuals
    gradient = (1/m) * X.T @ error        # ∂J/∂θ
    theta = theta - alpha * gradient        # θ ← θ - α∇J

print("Learned theta:", theta)

