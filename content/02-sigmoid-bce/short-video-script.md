# Short-Video Script: "Why PyTorch Wants Logits, Not Probabilities" (~55 s)

| Time | On screen | Voice-over |
|------|-----------|-----------|
| 0–3 s | Terminal showing `loss = inf` | "Your loss just became infinity. Here's the bug." |
| 3–13 s | Sigmoid curve + formula | "For yes-or-no problems, sigmoid squashes any score into a probability between zero and one." |
| 13–25 s | BCE formula, highlight `-log p` | "Binary cross-entropy takes minus log of the probability you gave the right answer. Confidently wrong? Huge loss." |
| 25–35 s | `sigmoid(800)` → `1.0` exactly, then `log(1 - 1.0)` → `-inf` | "But floats round. Sigmoid of 800 is exactly 1, log of zero is minus infinity, and training explodes." |
| 35–48 s | The logits formula | "The fix: never compute the probability first. Compute the loss straight from the logit with this stable formula. That's what BCEWithLogitsLoss does." |
| 48–55 s | Text: "Code + notes in description" | "So always pass logits. Follow for one ML algorithm from scratch every week." |

**Caption:** Sigmoid + binary cross-entropy from scratch, and why your loss hits infinity ♾️ #machinelearning #pytorch #python #deeplearning
