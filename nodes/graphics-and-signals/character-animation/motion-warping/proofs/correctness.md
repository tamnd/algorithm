---
title: A motion warp meets its keys, leaves a motion unchanged when the keys already hold, and keeps the order of the poses
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.
One channel is a function $\theta(t)$, sampled at the frames and read between frames by linear interpolation.
The keys are pairs $(t_k, v_k)$ with $t_1 < \dots < t_m$ in new time.
The scale curve $c$ is 1, or a natural cubic spline through its own keys.
The time warp $g$ is the identity, or the piecewise linear map through pairs $(t'_l, t_l)$ with both lists strictly increasing, with slope 1 outside the pairs.
Lines L1 to L4 compute $\theta'(t) = c(t)\,\theta(g(t)) + b(t)$, where $b$ is the natural cubic spline through the points $(t_k, \beta_k)$ with $\beta_k = v_k - c(t_k)\,\theta(g(t_k))$.

## The natural cubic spline

**Lemma 1.** For $m \ge 2$ points $(t_k, \beta_k)$ with increasing $t_k$, there is exactly one function $b$ that is a cubic on each $[t_k, t_{k+1}]$, is $C^2$ on $[t_1, t_m]$, has $b(t_k) = \beta_k$, and has $b'' = 0$ at $t_1$ and $t_m$.
Its second derivatives $M_k = b''(t_k)$ solve a tridiagonal system that is strictly diagonally dominant, and the Thomas algorithm solves it without pivoting.

*Proof.*
On $[t_k, t_{k+1}]$ with $h_k = t_{k+1} - t_k$, the cubic with values $\beta_k, \beta_{k+1}$ and second derivatives $M_k, M_{k+1}$ at the ends is
$b(t) = A \beta_k + B \beta_{k+1} + ((A^3 - A) M_k + (B^3 - B) M_{k+1}) h_k^2 / 6$ with $A = (t_{k+1} - t)/h_k$ and $B = 1 - A$; this is the formula in the code.
It has the right values and second derivatives, so $b$ is $C^0$ and its second derivative is continuous for any $M$.
Continuity of $b'$ at each inner key $t_k$ is the equation
$h_{k-1} M_{k-1} + 2 (h_{k-1} + h_k) M_k + h_k M_{k+1} = 6 \left( \frac{\beta_{k+1} - \beta_k}{h_k} - \frac{\beta_k - \beta_{k-1}}{h_{k-1}} \right)$,
and the natural ends set $M_1 = M_m = 0$.
The diagonal $2(h_{k-1} + h_k)$ is larger than the sum $h_{k-1} + h_k$ of the off diagonal entries, so the matrix is strictly diagonally dominant, nonsingular, and the Thomas algorithm has no zero pivot. $\square$

For $m = 1$ the code uses the constant $b = \beta_1$.
Outside $[t_1, t_m]$ the code holds the end values; this is a choice of the code and is part of the definition of $b$.

**Lemma 2.** If the $\beta_k$ are values of a linear function $\beta_k = r + s t_k$, then $b(t) = r + s t$ on $[t_1, t_m]$.

*Proof.*
$M = 0$ solves the system, because the right side is $6(s - s) = 0$, and by Lemma 1 the solution is unique.
With $M = 0$ the formula is the linear interpolation of the values, which is $r + s t$. $\square$

## The keys

**Theorem 1.** $\theta'(t_k) = v_k$ for every key.

*Proof.*
$\theta'(t_k) = c(t_k)\,\theta(g(t_k)) + b(t_k) = c(t_k)\,\theta(g(t_k)) + v_k - c(t_k)\,\theta(g(t_k)) = v_k$, by Lemma 1 for $m \ge 2$ and by the constant for $m = 1$. $\blacksquare$

**Theorem 2.** If every key already holds, that is $v_k = c(t_k)\,\theta(g(t_k))$, then $\theta' = c \cdot (\theta \circ g)$: the displacement is zero.

*Proof.*
All $\beta_k = 0$, so $b = 0$ by Lemma 2 with $r = s = 0$, and by the constant hold outside. $\blacksquare$

**Theorem 3.** If the scale is 1 and the wanted change is linear, $v_k = \theta(g(t_k)) + r + s t_k$, then $\theta'(t) = \theta(g(t)) + r + s t$ on $[t_1, t_m]$.

*Proof.*
$\beta_k = r + s t_k$, and Lemma 2 applies. $\blacksquare$

**Theorem 4.** The displacement $b$ is $C^2$ on $[t_1, t_m]$, so it adds no corner to the motion; where $\theta \circ g$ and $c$ are smooth, $\theta'$ is as smooth as they are.

*Proof.*
Lemma 1. $\blacksquare$

## The time warp

**Theorem 5.** $g$ is continuous and strictly increasing, and $g(t'_l) = t_l$.
So the warped motion $\theta \circ g$ shows the poses of $\theta$ in the same order, and never plays a part of the motion backward.

*Proof.*
On each piece $[t'_l, t'_{l+1}]$, $g$ is linear from $t_l$ to $t_{l+1}$ with slope $(t_{l+1} - t_l)/(t'_{l+1} - t'_l) > 0$.
Outside the pairs the slope is 1, and the pieces meet at the pairs.
The code raises an error if a list is not strictly increasing. $\blacksquare$
