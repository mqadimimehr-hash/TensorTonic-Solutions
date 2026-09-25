# Linear Regression with Gradient Descent, from Scratch

**Level:** Beginner · **Time:** 7 min · **Code:** [`linear_regression.py`](linear_regression.py)

## 1. The problem
Given data points `(x, y)`, find the line `ŷ = w·x + b` that fits them best.
Example: study hours → exam score.

## 2. What does "best" mean? The loss
We use **mean squared error (MSE)**, the average of the squared mistakes:

$$L(w, b) = \frac{1}{n}\sum_{i=1}^{n} (\hat{y}_i - y_i)^2$$

Squaring makes all errors positive and punishes big misses more than small ones.

## 3. Gradient descent: walk downhill
Picture the loss as a valley. The **gradient** points uphill, so we step the opposite way:

$$w \leftarrow w - \eta\,\frac{\partial L}{\partial w}, \qquad b \leftarrow b - \eta\,\frac{\partial L}{\partial b}$$

`η` (eta) is the **learning rate**, the step size. For MSE the gradients are:

$$\frac{\partial L}{\partial w} = \frac{2}{n}\sum (\hat{y}_i - y_i)\,x_i, \qquad \frac{\partial L}{\partial b} = \frac{2}{n}\sum (\hat{y}_i - y_i)$$

In words: *error times input* for `w`, and *just the error* for `b`.

## 4. The code
```python
for epoch in range(epochs):
    err = X @ w + b - y          # prediction error
    dw = (2 / n) * X.T @ err     # gradient for w
    db = (2 / n) * err.sum()     # gradient for b
    w -= lr * dw
    b -= lr * db
```
The data was generated from `y = 3x + 2` plus noise, and training learns **`y = 2.97x + 2.01`**.
That matches the exact least-squares answer, so gradient descent found the right line.

## 5. The bug: learning rate too big
With `lr = 1.5`, every step **overshoots** the bottom of the valley and lands higher on the other side.
The loss grows to around `10^285` instead of shrinking.

- Loss going **up** or becoming `inf`/`nan` → lower the learning rate.
- Loss going down **very slowly** → raise it a bit.
- Common starting points: `0.1`, `0.01`, `0.001`.

## 6. Check yourself
1. Why do we square the errors instead of just adding them? *(Positive and negative errors would cancel out.)*
2. If every `x` is multiplied by 100, what should happen to a good learning rate? *(It must get much smaller, which is why we normalize features.)*
3. Linear regression has an exact formula. Why learn gradient descent? *(The same loop trains logistic regression and neural networks, where no exact formula exists.)*

## Key takeaways
- Model: `ŷ = Xw + b`. Loss: MSE. Optimizer: gradient descent.
- The gradient for each weight is roughly *error × input*.
- A learning rate that's too large makes training explode. Lower it.
