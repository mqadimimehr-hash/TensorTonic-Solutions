"""Linear regression with gradient descent, from scratch.

Run:  python linear_regression.py
"""
import numpy as np


def predict(X, w, b):
    return X @ w + b


def mse(y, y_hat):
    return np.mean((y_hat - y) ** 2)


def gradients(X, y, w, b):
    """d(MSE)/dw and d(MSE)/db."""
    n = len(y)
    err = predict(X, w, b) - y
    dw = (2 / n) * X.T @ err
    db = (2 / n) * err.sum()
    return dw, db


def fit(X, y, lr=0.1, epochs=500):
    w = np.zeros(X.shape[1])
    b = 0.0
    for epoch in range(epochs):
        dw, db = gradients(X, y, w, b)
        w -= lr * dw
        b -= lr * db
        if epoch % 100 == 0:
            print(f"epoch {epoch:3d}  loss {mse(y, predict(X, w, b)):.4g}")
    return w, b


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    X = rng.uniform(0, 1, size=(200, 1))
    y = 3 * X[:, 0] + 2 + rng.normal(0, 0.1, size=200)  # true line: y = 3x + 2

    w, b = fit(X, y)
    print(f"learned: y = {w[0]:.2f}x + {b:.2f}   (true: y = 3x + 2)")

    # sanity check against the closed-form least-squares solution
    A = np.hstack([X, np.ones((len(X), 1))])
    exact = np.linalg.lstsq(A, y, rcond=None)[0]
    print(f"exact:   y = {exact[0]:.2f}x + {exact[1]:.2f}")

    print("\nlearning rate too big (lr=1.5):")
    fit(X, y, lr=1.5, epochs=301)
