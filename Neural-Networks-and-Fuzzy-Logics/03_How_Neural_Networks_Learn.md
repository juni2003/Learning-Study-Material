# How Neural Networks Learn

## Core Idea

Training = Adjusting Importance.

Weights represent importance.

If prediction is wrong:
→ Adjust weights
→ Reduce error
→ Repeat

This process is called optimization.

---

## Intuitive Example

Spam detection:

Input: email words  
Output: spam or not spam  

Model sees:
- "Free"
- "Win"
- "Lottery"

It increases importance (weights) of those words.

---

## Learning Steps

1. Forward pass (make prediction)
2. Compute error
3. Adjust weights
4. Repeat

This process is called backpropagation.

---

## Limitation of Neural Networks

- Need large datasets
- Hard to explain
- Act like black boxes
