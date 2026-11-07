---
title: Steffensen's method ends and converges quadratically near a simple root
proves: [correctness, termination, local-convergence]
status: full
---

We write $x_k$ for the value of $x$ at the start of pass $k + 1$, $y_k = x_k + f(x_k)$, $e_k = x_k - x^*$, and $d_k = f[x_k, y_k]$. The arithmetic is exact except in Claim 1.

## Claim 1: termination and the flags

Each pass returns or increases $k$, and $k \le k_{\max}$, so the loop ends after at most $k_{\max}$ passes, each with at most two evaluations. The flags record the tests of lines L3, L5 and L10. In floating point, $y = x$ in line L5 happens exactly when the computed $x + f(x)$ rounds to $x$, which implies $|f(x)| \le u|x|$ in round-to-nearest.

## Claim 2: the error identity

Assume $f(x_k) \ne 0$, so $y_k \ne x_k$, and $d_k \ne 0$. Then
$$e_{k+1} = e_k - \frac{f(x_k)}{d_k} = \frac{e_k\,(d_k - f[x^*, x_k])}{d_k},$$
because $f(x_k) = f(x_k) - f(x^*) = f[x^*, x_k]\,e_k$. By the definition of the second divided difference, $d_k - f[x^*, x_k] = f[x_k, y_k] - f[x^*, x_k] = f[x^*, x_k, y_k]\,(y_k - x^*)$, and $y_k - x^* = e_k + f(x_k)$. Hence
$$e_{k+1} = \frac{f[x^*, x_k, y_k]}{f[x_k, y_k]}\,e_k\,(e_k + f(x_k)).$$

## Claim 3: local quadratic convergence

Let $f \in C^2$ on $I = [x^* - r, x^* + r]$ with $f(x^*) = 0$, and let $L = \max_I |f'|$, $\mu = \min_I |f'| > 0$, $M = \max_I |f''|$ and $K = M(1 + L)/(2\mu)$. Suppose $(1 + L)|e_k| \le r$ and $K|e_k| \le \frac12$.

By the mean value theorem $|f(x_k)| \le L|e_k|$, so $|y_k - x^*| \le (1 + L)|e_k| \le r$ and $y_k \in I$. On $I$, $|f[x_k, y_k]| \ge \mu$ because it equals $f'$ at a point of $I$, and $|f[x^*, x_k, y_k]| \le M/2$ because it equals $f''/2$ at a point of $I$. So $d_k \ne 0$, and Claim 2 gives
$$|e_{k+1}| \le \frac{M}{2\mu}|e_k|\,(|e_k| + L|e_k|) = K|e_k|^2 \le \tfrac12|e_k|.$$
Then $(1 + L)|e_{k+1}| \le r$ and $K|e_{k+1}| \le \frac12$, so by induction the hypotheses hold for all $k$, $e_k \to 0$, and $K|e_k| \le (K|e_0|)^{2^k}$. If $f(x_k) = 0$ at some step, then $x_k = x^*$ because $f' \ne 0$ on $I$.

**The constant.** As $e_k \to 0$, $f[x^*, x_k, y_k] \to f''(x^*)/2$, $f[x_k, y_k] \to f'(x^*)$ and $(e_k + f(x_k))/e_k \to 1 + f'(x^*)$, so
$$\frac{e_{k+1}}{e_k^2} \to \frac{f''(x^*)\,(1 + f'(x^*))}{2f'(x^*)}.$$
If $f'(x^*) = -1$ this limit is $0$; with $f \in C^3$ the identity then gives $|e_{k+1}| = O(|e_k|^3)$.

## Claim 4: the fixed-point form

For $x = g(x)$ with $g \in C^2$ and $g'(x^*) \ne 1$, put $f(x) = g(x) - x$. Then $f'(x^*) = g'(x^*) - 1 \ne 0$, $x_k + f(x_k) = g(x_k) = y$ and $f(y) = g(y) - y = z - y$, so the root step is $-(y - x_k)^2/(z - 2y + x_k)$, the Aitken step. Claim 3 applies to $f$, so the fixed-point form converges quadratically from close starts, whatever the size of $|g'(x^*)|$.

## What is not proved

The behaviour far from the root, at multiple roots, and the pass counts of the examples are observations.
