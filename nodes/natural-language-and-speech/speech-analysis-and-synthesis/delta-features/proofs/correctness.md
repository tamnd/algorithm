---
title: Deltas are least squares slopes, ignore offsets, and give 39 numbers from 13
proves: [correctness]
status: full
---

We work in the real RAM. Fix $\Theta \ge 1$ and a sequence $c_0, \ldots, c_{T-1}$ of vectors of dimension $D$ with $T \ge 1$. Every step works on each coordinate on its own, so we write $c_t$ for one coordinate. Let $\bar c_t = c_{\min(\max(t, 0), T-1)}$ be the sequence with the edge frames repeated, and $S = \sum_{n=1}^{\Theta} n^2$.

**Lemma 1 (lines L1 to L4 compute the formula).** DELTAS returns $d_t = \sum_{n=1}^{\Theta} n(\bar c_{t+n} - \bar c_{t-n}) / (2S)$ for $0 \le t \le T - 1$.

*Proof.* Line L1 sets $den = 2S$ and every $s[t][j]$ to 0. Line L2 reads $a = \bar c_{t+n}$ and $b = \bar c_{t-n}$, because $\min(t + n, T - 1) = \min(\max(t+n, 0), T-1)$ for $t + n \ge 0$, and similarly for $t - n \le T - 1$. Line L3 adds $n(a - b)$ once for each $n$ from 1 to $\Theta$, and line L4 divides by $den > 0$. $\square$

**Lemma 2 (least squares slope).** For each $t$, $d_t$ is the slope $\beta$ of the line $\alpha + \beta n$ that minimizes $\sum_{n=-\Theta}^{\Theta} (\bar c_{t+n} - \alpha - \beta n)^2$.

*Proof.* The objective is a convex quadratic in $(\alpha, \beta)$. Setting the derivatives to 0 gives $\sum_n (\bar c_{t+n} - \alpha - \beta n) = 0$ and $\sum_n n(\bar c_{t+n} - \alpha - \beta n) = 0$. Since $\sum_{n=-\Theta}^{\Theta} n = 0$ and $\sum_{n=-\Theta}^{\Theta} n^2 = 2S > 0$, the second equation gives $\beta = \sum_n n\, \bar c_{t+n} / (2S)$, and the system has this unique solution. The terms for $n$ and $-n$ combine to $n(\bar c_{t+n} - \bar c_{t-n})$, and the term $n = 0$ is 0, so $\beta = d_t$ by Lemma 1. $\square$

**Lemma 3 (lines and constants).** If $c_t = \alpha + \beta t$ for all $t$, then $d_t = \beta$ for $\Theta \le t \le T - 1 - \Theta$. If $c_t = \alpha$ for all $t$, then $d_t = 0$ for all $t$.

*Proof.* For those $t$ no index is clamped, so $\bar c_{t+n} - \bar c_{t-n} = 2 \beta n$ and $d_t = \sum_n 2\beta n^2 / (2S) = \beta$. For a constant, $\bar c$ is the same constant, every difference is 0, and $d_t = 0$. $\square$

**Lemma 4 (offsets).** If $c'_t = c_t + v$ for all $t$, then $d'_t = d_t$ and $dd'_t = dd_t$ for all $t$.

*Proof.* $\bar c'_t = \bar c_t + v$, so every difference in Lemma 1 is unchanged, hence $d' = d$. The delta-deltas are DELTAS applied to $d' = d$, so they are unchanged too. $\square$

**Lemma 5 (the output of ADD-DELTAS).** Line L5 computes $d$ and line L6 computes $dd$ by Lemma 1 on the sequence $d$, which also has $T$ frames of dimension $D$. Each output frame is the concatenation of $c_t$, $d_t$ and $dd_t$, so it has $3D$ coordinates; for $D = 13$ this is 39.

*Proof.* Lemma 1 shows that DELTAS returns $T$ frames of $D$ values, and line L6 concatenates three such frames. $\square$

**Theorem.** ADD-DELTAS returns for each frame the static features, their least squares slopes over $2\Theta + 1$ frames with the edges repeated, and the slopes of those slopes. The result does not change when a constant vector is added to every frame, and a straight line gives its slope away from the edges.

*Proof.* Lemmas 1 to 5. $\square$

The tests check Lemma 3 on a ramp and a constant, Lemma 2 against a direct least squares fit on random data with a fixed seed, the delta-delta of a quadratic away from the edges, the edge values against the repeated frames, and Lemma 5 with 13 coefficients.
