"""Softmax from scratch, with the numerically stable version.

Run:  python softmax.py
"""
import numpy as np


def softmax_naive(z):
    """Direct formula. Breaks (overflow -> nan) for large inputs."""
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def softmax(z):
    """Stable softmax: subtracting the max doesn't change the answer,
    but keeps every exponent <= 0, so exp() never overflows."""
    z = np.asarray(z, dtype=float)
    shifted = z - z.max(axis=-1, keepdims=True)
    e = np.exp(shifted)
    return e / e.sum(axis=-1, keepdims=True)


if __name__ == "__main__":
    logits = np.array([2.0, 1.0, 0.1])
    print("softmax([2, 1, 0.1]) =", softmax(logits).round(3))
    print("sums to", softmax(logits).sum())

    big = np.array([1000.0, 1001.0, 1002.0])
    with np.errstate(over="ignore", invalid="ignore"):
        print("naive  on big numbers:", softmax_naive(big))
    print("stable on big numbers:", softmax(big).round(3))

    batch = np.array([[1.0, 2.0, 3.0], [1.0, 1.0, 1.0]])
    print("batch (row-wise):\n", softmax(batch).round(3))
