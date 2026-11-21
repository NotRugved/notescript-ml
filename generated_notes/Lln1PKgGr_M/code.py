"""Code extracted from: What are Outliers | Outliers in Machine Learning"""

#======================================================================
# Block 1: Decision Tree Classifier Example | Label: on-screen | Timestamp: 15:30
#======================================================================
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# Load data
iris = load_iris()
X, y = iris.data, iris.target

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and fit model
dt_clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
dt_clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = dt_clf.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred):.2f}')

# Visualize tree
plot_tree(dt_clf, feature_names=iris.feature_names, class_names=iris.target_names, filled=True)

