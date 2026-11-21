"""Code extracted from: Principle Component Analysis  (PCA) | Part 1 | Geometric Intuition"""

#======================================================================
# Block 1: Gradient Descent Implementation | Label: on-screen | Timestamp: 18:00
#======================================================================
import numpy as np

def compute_loss(X, y, theta):
    """Calculate Mean Squared Error loss."""
    m = len(y)
    predictions = X.dot(theta)          # hθ(x) = X·θ
    loss = np.sum((predictions - y) ** 2) / (2 * m)  # 1/2 factor for cleaner derivative
    return loss

def gradient_descent(X, y, theta, alpha, iterations):
    """Perform batch gradient descent."""
    m = len(y)
    for _ in range(iterations):
        predictions = X.dot(theta)          # forward pass
        error = predictions - y            # residuals
        gradient = (X.T.dot(error)) / m    # ∂J/∂θ
        theta = theta - alpha * gradient    # parameter update
    return theta


#======================================================================
# Block 2: Simple Gradient Descent Implementation | Label: reconstructed | Timestamp: 32:30
# VERIFY: Reconstructed from verbal description only
#======================================================================
import numpy as np

# Initial parameters
w = 0.0
alpha = 0.01

# Sample data
X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# Gradient descent loop
for i in range(1000):
    y_pred = w * X
    error = y_pred - y
    cost = np.mean(error ** 2)
    gradient = 2 * np.mean(X * error)
    w = w - alpha * gradient
    
    if i % 100 == 0:
        print(f'Iteration {i}, Cost: {cost:.4f}, Weight: {w:.4f}')

print(f'Final Weight: {w:.4f}')

