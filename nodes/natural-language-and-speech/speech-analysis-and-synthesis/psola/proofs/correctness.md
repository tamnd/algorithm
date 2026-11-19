---
title: Correctness of TD-PSOLA
proves: [correctness]
status: full
---

PSOLA has no exact specification for real speech, so we prove the three exact statements of the page: the identity for equal spacing, the spectrum of the output for a periodic input, and the duration.

## Setup

The segment of mark $i$ is $g_i[j] = w_i[j]\, x[t_i - P_i + j]$ for $j = 0, \dots, 2P_i$, with $x[n] = 0$ outside the signal and the symmetric Hann window $w_i[j] = \tfrac12 - \tfrac12 \cos(\pi j / P_i)$ of length $2P_i + 1$. The output is $y[n] = \sum_m g_{i_m}[n - s_m + P_{i_m}]$, summed over the synthesis marks $s_m$ (rounded) and their analysis indices $i_m$, where terms with the index outside $0 .. 2P_{i_m}$ are 0.

## Lemma 1 (the Hann windows add to 1)

Let $w[j] = \tfrac12 - \tfrac12\cos(\pi j / P)$ for $0 \le j \le 2P$ and 0 otherwise. Then for every integer $n$ with $c \le n \le c + P$, $w[n - c + P] + w[n - c] = 1$; that is, two windows centered at $c$ and $c + P$ add to 1 between their centers.

*Proof.* Put $j = n - c \in [0, P]$. Then $w[j + P] + w[j] = 1 - \tfrac12 (\cos(\pi j / P + \pi) + \cos(\pi j / P)) = 1$, since $\cos(\theta + \pi) = -\cos\theta$. Both indices $j$ and $j + P$ are in $[0, 2P]$. $\square$

## Theorem 1 (identity)

If $t_{i+1} - t_i = P$ for all $i$ and $\alpha = \beta = 1$, then $y[n] = x[n]$ for $t_1 \le n \le t_K$.

*Proof.* Every local period is $P$. The synthesis marks start at $s = t_1$ and advance by $P$, so they are $t_1, t_2, \dots, t_K$, and the nearest analysis mark to $s_m = t_m$ is $t_m$ itself. So $y[n] = \sum_m w[n - t_m + P]\, x[n]$. For $t_m \le n \le t_{m+1}$, only the windows centered at $t_m$ and $t_{m+1}$ are nonzero at $n$ (the others are centered at least $P$ away from both ends of this interval, and they vanish at distance $P$), and by Lemma 1 they add to 1. So $y[n] = x[n]$. $\square$

## Theorem 2 (pitch change of a periodic signal)

Let $x[n + P] = x[n]$ for all $n$ in the signal, let $t_{i+1} - t_i = P$, let every segment lie inside the signal, let $\alpha = 1$, and let $Q = P / \beta$ be an integer. Then:

1. All segments are equal to one sequence $g$ of length $2P + 1$.
2. Let $s_1 < \dots < s_M$ be the synthesis marks. For $s_1 + P \le n$ and $n + Q \le s_M - P$, $y[n + Q] = y[n]$.
3. For any $n_0$ such that $[n_0, n_0 + Q - 1]$ lies in that range, $\frac{1}{Q} \left|\sum_{n = n_0}^{n_0 + Q - 1} y[n]\, e^{-2\pi i k n / Q}\right| = \frac{1}{Q} |G(2\pi k / Q)|$, where $G(\omega) = \sum_j g[j]\, e^{-i \omega j}$.

*Proof.* (1) $g_i[j] = w[j]\, x[t_1 + (i - 1) P - P + j] = w[j]\, x[t_1 - P + j]$ by the periodicity, for every $i$.

(2) The synthesis marks are $s_m = s_1 + (m - 1) Q$, an arithmetic sequence, since each step adds $P / \beta = Q$. So $y[n] = \sum_m g[n - s_m + P]$. For $n$ in the range, every $m$ with $g[n - s_m + P] \ne 0$ satisfies $|n - s_m| \le P$, so $s_m$ lies in $[s_1, s_M]$ and the sum runs over all terms of the infinite sequence $s_1 + \mathbb{Z} Q$ that can contribute. The same holds at $n + Q$, and the substitution $m \to m + 1$ maps one sum to the other. Hence $y[n + Q] = y[n]$.

(3) On the range, $y[n] = \sum_{m \in \mathbb{Z}} g[n - s_1 - mQ + P]$ (the extra terms are 0, as in (2)). Then

$$\sum_{n = n_0}^{n_0 + Q - 1} y[n]\, e^{-2\pi i k n / Q} = \sum_{m} \sum_{n = n_0}^{n_0 + Q - 1} g[n - s_1 - mQ + P]\, e^{-2\pi i k n / Q}.$$

Put $j = n - s_1 - mQ + P$. As $m$ runs over $\mathbb{Z}$ and $n$ over one period, $j$ runs over every integer exactly once, and $e^{-2\pi i k n / Q} = e^{-2\pi i k (j + s_1 - P) / Q}$ because $e^{-2\pi i k m} = 1$. So the sum is $e^{-2\pi i k (s_1 - P) / Q} \sum_j g[j]\, e^{-2\pi i k j / Q} = e^{-2\pi i k (s_1 - P)/Q}\, G(2\pi k / Q)$, whose modulus is $|G(2\pi k / Q)|$. $\square$

For comparison, by the same argument with $Q = P$ and Theorem 1, the input itself has Fourier coefficients $\frac{1}{P} G(2\pi k / P)$ over one period, since it is the periodization of $g$ at spacing $P$. So input and output sample the same function $G$ at the harmonics of their own pitch, and the ratio of levels near a fixed frequency is $P / Q = \beta$.

## Theorem 3 (duration)

The output has $\text{round}(\alpha |x|)$ samples, every synthesis mark lies in $[\alpha t_1, \alpha t_K]$, and consecutive synthesis marks are at least $\min_i P_i / \beta$ apart.

*Proof.* The length is set on line L2. The loop starts at $\alpha t_1$, stops before passing $\alpha t_K$, and adds $P_i / \beta \ge \min_i P_i / \beta$ at each step. $\square$

## Remarks

The tests check Theorem 1 on random noise (error below $10^{-12}$), Theorem 2 on a random periodic signal with $P = 50$ and $Q = 40$ by comparing all 40 Fourier coefficients with the DTFT of one segment, and the spacing of Theorem 3. Rounding of $s$ makes the spacing an integer only when $P_i / \beta$ is one; otherwise the spacing alternates between the two nearest integers, and the pitch is right on average.
