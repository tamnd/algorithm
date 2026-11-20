---
title: Semblance lies between 0 and 1, equals 1 exactly when the moveout-corrected traces agree in the window, equals 1/N for one live trace, and has expected numerator over expected denominator 1/N for independent noise
proves: [correctness]
status: full
---

**Setting.** A gather has $N$ traces with offsets $x_i$. For a zero-offset index $j$, a trial velocity $v$ and a half window $W$, lines L4 and L5 read the samples $a_i(k) = d_i\big(\sqrt{(k\,\Delta t)^2 + x_i^2/v^2}\big)$ for $k = j - W, \ldots, j + W$ (by linear interpolation; $0$ outside the record). Lines L3 and L6 accumulate
$$A = \sum_k \Big(\sum_i a_i(k)\Big)^2, \qquad B = \sum_k \sum_i a_i(k)^2,$$
and line L7 returns $S = A/(N B)$, or $0$ when $B = 0$. The window and the velocity are fixed in each claim.

**Claim 1 (bounds).** $0 \le S \le 1$.

*Proof.* $A \ge 0$ and $B \ge 0$ as sums of squares. If $B = 0$, line L7 returns $0$. Otherwise, for each $k$ the Cauchy-Schwarz inequality for the vectors $(a_1(k), \ldots, a_N(k))$ and $(1, \ldots, 1)$ gives $\big(\sum_i a_i(k)\big)^2 \le N \sum_i a_i(k)^2$. Summing over $k$ gives $A \le N B$, so $S \le 1$. $\square$

**Claim 2 (when $S = 1$).** If $B > 0$, then $S = 1$ if and only if, at every time $k$ of the window, all $N$ samples $a_i(k)$ are equal.

*Proof.* $S = 1$ means $A = N B$, that is $\sum_k \big(N \sum_i a_i(k)^2 - (\sum_i a_i(k))^2\big) = 0$. Each term is at least $0$ by Claim 1, so each term is $0$. Equality in Cauchy-Schwarz holds exactly when $(a_i(k))_i$ is a multiple of $(1, \ldots, 1)$, that is when all $a_i(k)$ are equal for that $k$. $\square$

So $S = 1$ means that the moveout correction with $v$ made the traces identical in the window. For a reflection on the hyperbola of velocity $v$ the peak lines up on all traces (Claim 2 of the NMO proof), but the NMO stretch makes the far traces wider, so the samples next to the peak differ a little and $S$ is close to, not equal to, 1.

**Claim 3 (one live trace).** If exactly one trace is not zero in the window, then $S = 1/N$. If the samples at each time have opposite values in pairs (for example $N = 2$ and $a_2(k) = -a_1(k)$), then $S = 0$.

*Proof.* With only trace $p$ live, $\sum_i a_i(k) = a_p(k)$, so $A = \sum_k a_p(k)^2 = B$ and $S = 1/N$. With $a_2 = -a_1$ and $N = 2$ the sums $\sum_i a_i(k)$ are all $0$, so $A = 0$ and $S = 0$ when $B > 0$; line L7 returns $0$ also when $B = 0$. $\square$

**Claim 4 (scale invariance).** Multiplying all samples by the same $c \ne 0$ does not change $S$.

*Proof.* $A$ and $B$ both get the factor $c^2$. $\square$

A scale that differs from trace to trace does change $S$, so a gather with strong amplitude decay with offset has a lower semblance than the same gather after gain.

**Claim 5 (independent noise).** If the $a_i(k)$ are independent random variables with mean $0$ and the same variance $\sigma^2 > 0$, then $\mathbb{E} A / (N\,\mathbb{E} B) = 1/N$.

*Proof.* For each $k$, $\mathbb{E}\big(\sum_i a_i(k)\big)^2 = \sum_i \mathbb{E} a_i(k)^2 + \sum_{i \ne i'} \mathbb{E} a_i(k)\,\mathbb{E} a_{i'}(k) = N\sigma^2$, and $\mathbb{E} \sum_i a_i(k)^2 = N\sigma^2$. With $L = 2W + 1$ window samples, $\mathbb{E} A = L N \sigma^2$ and $\mathbb{E} B = L N \sigma^2$. $\square$

The claim is about the ratio of the expectations; the mean of the ratio $S$ is close to $1/N$ when the window is long, which the tests measure. So $1/N$ is the level of pure noise, and a peak well above it marks coherent energy.

**Claim 6 (the scan).** Lines L1, L2 and L8 return the matrix $S[j][\ell]$ with one entry for each scanned time $j$ and each trial velocity $v_\ell$, each computed as above. With $n_t$ times, $n_v$ velocities, $N$ traces and a window of $L$ samples, the cost is $O(n_t\, n_v\, N L)$.

*Proof.* The double loop calls the semblance once for each pair $(j, \ell)$. Each call reads $N L$ samples, each with a square root and an interpolation of fixed cost, and does $O(N L)$ additions and multiplications. $\square$
