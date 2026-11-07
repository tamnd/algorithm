---
title: Cost of the Kaczmarz method
proves: [time.expected, space.extra, steps.expected, flops.per_sweep]
status: full
---

$A$ is stored by rows (CSR) with $z$ nonzeros, $z_i$ in row $i$, so $\sum_i z_i = z$.

**Setup (line L1).** The squared row norms cost $2 z$ flops, and for the randomized order their cumulative sums $m$ more additions. $O(z + m)$ time and $m$ words.

**Flops per sweep.** In a row step, $b_i - a_i^T x$ costs $z_i$ multiplications and $z_i$ additions or subtractions, line L6 one multiplication and one division (with $\|a_i\|^2$ precomputed), and line L7 $z_i$ multiplications and $z_i$ additions. So $4 z_i + 2$ flops, and $4 z + 2 m$ for the $m$ steps of a sweep. The residual at line L8 costs $2 z$ flops for $A x$, $m$ subtractions, and $2m$ for the norm, so a full sweep costs $6 z + O(m)$ flops.

**Steps for accuracy $\varepsilon$.** By Theorem 5 of the correctness proof, $\mathbb{E}\|e_k\|^2 \le (1 - \kappa^{-2})^k \|e_0\|^2 \le e^{-k/\kappa^2}\|e_0\|^2$, using $1 - t \le e^{-t}$. So $k = \lceil \kappa^2 \ln(1/\varepsilon) \rceil$ steps give $\mathbb{E}\|e_k\|^2 \le \varepsilon \|e_0\|^2$.

**Expected time.** A randomized step draws one uniform number and finds the row by binary search in the cumulative sums, $O(\log m)$, then costs $O(z_i + 1) \subseteq O(n)$ for the row update. With the setup, $k$ steps cost $O(z + m + (n + \log m) k)$, which with the $k$ above is $O(z + m + (n + \log m)\kappa^2 \log(1/\varepsilon))$ (the residual test of line L8 is excluded from this count, since the bound concerns the error, not the stopping rule).

**Space.** The iterate takes $n$ words, the row norms and cumulative sums $2m$ words, and the residual $m$ words: $\Theta(m + n)$ extra space besides $A$ and $b$. $\blacksquare$
