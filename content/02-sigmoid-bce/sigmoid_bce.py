"""Sigmoid and binary cross-entropy from scratch, with the stable versions.

Run:  python sigmoid_bce.py
"""
import numpy as np


def sigmoid(z):
    """Stable sigmoid: never calls exp() on a large positive number."""
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def bce_naive(y, p):
    """Direct formula on probabilities. log(0) -> -inf when p hits 0 or 1."""
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


def bce(y, p, eps=1e-12):
    """BCE on probabilities, clipped so log() never sees exactly 0."""
    p = np.clip(p, eps, 1 - eps)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


def bce_with_logits(y, z):
    """BCE straight from logits (what PyTorch's BCEWithLogitsLoss does):
    max(z, 0) - z*y + log(1 + exp(-|z|)). Stable for any z."""
    z = np.asarray(z, dtype=float)
    return np.mean(np.maximum(z, 0) - z * y + np.log1p(np.exp(-np.abs(z))))


if __name__ == "__main__":
    z = np.array([-2.0, 0.0, 3.0])
    print("sigmoid([-2, 0, 3]) =", sigmoid(z).round(3))

    y = np.array([0.0, 1.0, 1.0])
    print("BCE (probs)  =", round(bce(y, sigmoid(z)), 4))
    print("BCE (logits) =", round(bce_with_logits(y, z), 4))

    big = np.array([-800.0, 800.0])
    y2 = np.array([1.0, 0.0])  # confidently wrong on both
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        print("naive BCE on big logits:", bce_naive(y2, 1 / (1 + np.exp(-big))))
    print("stable BCE with logits: ", bce_with_logits(y2, big))
