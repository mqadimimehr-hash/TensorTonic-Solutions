# Short-Video Script: "Your Softmax Is Broken" (~50 s, TikTok / Reels / Shorts)

**Format:** screen recording of code + your voice (face-cam optional).

| Time | On screen | Voice-over |
|------|-----------|-----------|
| 0–3 s | Terminal showing `[nan nan nan]` in red | "Your softmax function is probably broken. Here's why." |
| 3–12 s | Formula `e^zi / Σ e^zj` | "Softmax turns model scores into probabilities: exponentiate each score, then divide by the total." |
| 12–20 s | Naive code, input `[1000, 1001, 1002]` | "But feed it big numbers, and e to the 1000 is infinity. Infinity divided by infinity? Not a number." |
| 20–35 s | Add the line `z = z - z.max()` | "The fix is one line: subtract the max first. Shifting all scores by the same amount doesn't change softmax, but now every exponent is zero or less, so nothing overflows." |
| 35–45 s | Run it → `[0.09 0.245 0.665]` | "Same correct answer, no crash. PyTorch and NumPy-based libraries do this for you under the hood." |
| 45–50 s | Text: "Full notes + code in bio" | "Follow for one ML algorithm from scratch every week." |

**Caption:** Softmax from scratch, plus the one-line fix most students miss 🧠 #machinelearning #python #deeplearning #coding #studytok

**Tips:** record in 1080×1920, use big font (24pt+), and put the hook in the first 2 seconds.
