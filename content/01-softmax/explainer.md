# Softmax from Scratch (and the Bug Most Students Miss)

**Level:** Beginner · **Time:** 5 min · **Code:** [`softmax.py`](softmax.py)

## 1. The problem
A classifier outputs raw scores called **logits**, for example `[2.0, 1.0, 0.1]` for cat, dog and bird.
We want **probabilities**: every value between 0 and 1, and all values adding up to 1.

## 2. The idea
1. Make every score positive → use `exp(z)`.
2. Make them add up to 1 → divide by the total.

$$\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

Worked example with `[2.0, 1.0, 0.1]`:

| class | z   | e^z   | ÷ 11.21 |
|-------|-----|-------|---------|
| cat   | 2.0 | 7.39  | **0.659** |
| dog   | 1.0 | 2.72  | **0.242** |
| bird  | 0.1 | 1.11  | **0.099** |

Bigger scores get a much bigger share, which is why it's called a *soft* max.

## 3. The naive code, and why it breaks
```python
def softmax_naive(z):
    e = np.exp(z)
    return e / e.sum()
```
Try `z = [1000, 1001, 1002]`. `exp(1000)` is too large for a float → `inf / inf` → **`nan`**.
Real models can produce large logits, so this bug really happens.

## 4. The fix: subtract the max
Adding or subtracting the same number from every logit **doesn't change softmax**:

$$\frac{e^{z_i - c}}{\sum_j e^{z_j - c}} = \frac{e^{z_i} e^{-c}}{e^{-c}\sum_j e^{z_j}} = \text{softmax}(z_i)$$

Choose `c = max(z)`. Then every exponent is ≤ 0, so `exp()` stays between 0 and 1 and never overflows.

```python
def softmax(z):
    shifted = z - z.max(axis=-1, keepdims=True)
    e = np.exp(shifted)
    return e / e.sum(axis=-1, keepdims=True)
```
`axis=-1, keepdims=True` makes it work on a whole **batch** (one row per sample).

## 5. Check yourself
1. What is `softmax([5, 5, 5])`? *(Answer: `[1/3, 1/3, 1/3]`.)*
2. Why is `c = max(z)` a better choice than `c = mean(z)`? *(Hint: which one guarantees every exponent is ≤ 0?)*
3. What happens to the output if you multiply all logits by 10? *(It gets "sharper", closer to one-hot.)*

## Key takeaways
- Softmax = exponentiate, then normalize.
- Always subtract the max for numerical stability.
- Use `axis=-1, keepdims=True` for batches.
