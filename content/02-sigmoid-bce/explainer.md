# Sigmoid & Binary Cross-Entropy from Scratch

**Level:** Beginner · **Time:** 6 min · **Code:** [`sigmoid_bce.py`](sigmoid_bce.py)

## 1. The problem
Binary classification: spam or not spam, cat or not cat. The model outputs one raw score (a **logit**) `z`.
We need (a) a probability `p` between 0 and 1, and (b) a loss that punishes wrong, confident guesses.

## 2. Sigmoid: score → probability
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

| z  | σ(z)  | meaning |
|----|-------|---------|
| -2 | 0.119 | probably class 0 |
| 0  | 0.5   | no idea |
| 3  | 0.953 | probably class 1 |

Sigmoid is softmax with only two classes, where the other logit is fixed at 0.

## 3. Binary cross-entropy: how wrong were we?
$$\text{BCE} = -\big[\,y\log p + (1-y)\log(1-p)\,\big]$$

- If `y = 1`, the loss is `-log p`. It's small when `p ≈ 1` and huge when `p ≈ 0`.
- If `y = 0`, the loss is `-log(1-p)`, the mirror image.

Why use log? Being **confidently wrong** (p = 0.001 for a true 1) costs `-log(0.001) ≈ 6.9`,
while being unsure (p = 0.5) costs only `0.69`. The model learns not to be overconfident.

## 4. Two bugs students hit
**Bug 1: sigmoid overflow.** `np.exp(-z)` with `z = -800` → `exp(800)` = overflow.
Fix: for negative `z`, use the equivalent form `e^z / (1 + e^z)`.

**Bug 2: `log(0)`.** When sigmoid rounds to exactly 0 or 1, `log(0) = -inf` and the loss becomes `inf`/`nan`.
Fixes:
- Quick fix: clip `p` into `[1e-12, 1 - 1e-12]`.
- Better fix: compute the loss **directly from logits**:

$$\text{BCE}(y, z) = \max(z, 0) - z\,y + \log\!\big(1 + e^{-|z|}\big)$$

This is exactly what PyTorch's `BCEWithLogitsLoss` does, and why you should pass it logits, not probabilities.

```python
def bce_with_logits(y, z):
    return np.mean(np.maximum(z, 0) - z * y + np.log1p(np.exp(-np.abs(z))))
```

## 5. Check yourself
1. What is the BCE when `y = 1` and `p = 0.5`? *(Answer: `ln 2 ≈ 0.693`.)*
2. Why does PyTorch recommend `BCEWithLogitsLoss` over `Sigmoid` followed by `BCELoss`? *(Stability: see Bug 2.)*
3. The gradient of BCE with respect to `z` is surprisingly simple. What is it? *(Answer: `p - y`.)*

## Key takeaways
- Sigmoid maps any score into (0, 1).
- BCE heavily punishes confident mistakes.
- In real code, compute the loss from logits to avoid `log(0)`.
