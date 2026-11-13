---
title: REDUCE computes the separable 2D sum, keeps constants, stops after ceil(log2 max(W, H)) steps, and the levels have the stated total size
proves: [correctness]
status: full
---

The image $g$ has $W \times H$ real samples, $W, H \ge 1$. The kernel $\hat w(-2), \ldots, \hat w(2)$ is real. The border map $\rho_n$ sends every integer to $\{0, \ldots, n-1\}$. Write $W' = \lceil W/2 \rceil$ and $H' = \lceil H/2 \rceil$.

**Claim 1 (the two passes give the 2D sum).** For $0 \le i < W'$ and $0 \le j < H'$, lines L1 to L6 return

$$
g'[j][i] = \sum_{m=-2}^{2} \sum_{n=-2}^{2} \hat w(m)\, \hat w(n)\, g\big[\rho_H(2j + n)\big]\big[\rho_W(2i + m)\big].
$$

*Proof.* Line L3 sets $r[y][i] = \sum_m \hat w(m)\, g[y][\rho_W(2i + m)]$ for every row $y$ in $0 .. H-1$ and every $i < W'$. Line L5 reads $r$ at the row $\rho_H(2j + n)$, which lies in $0 .. H-1$, so that value exists. Substituting,

$$
g'[j][i] = \sum_{n} \hat w(n) \sum_{m} \hat w(m)\, g\big[\rho_H(2j + n)\big]\big[\rho_W(2i + m)\big],
$$

and the two finite sums can be exchanged and their factors multiplied out, which gives the formula. $\square$

**Claim 2 (constants and range).** If $\sum_m \hat w(m) = 1$ and $g$ is the constant $c$, then $g' = c$. If also $\hat w(m) \ge 0$ for all $m$, then every value of $g'$ lies between the minimum and the maximum of $g$. For the Burt and Adelson kernel $\hat w = (1/4 - a/2, 1/4, a, 1/4, 1/4 - a/2)$, the taps are nonnegative exactly when $0 \le a \le 1/2$.

*Proof.* By Claim 1, $g'[j][i]$ is a sum of values of $g$ with the weights $\hat w(m) \hat w(n)$, and $\sum_{m,n} \hat w(m) \hat w(n) = (\sum_m \hat w(m))^2 = 1$. For a constant $c$ the sum is $c \cdot 1 = c$. When the weights are nonnegative and sum to 1, the sum is a convex combination of values of $g$, so it lies between their minimum and maximum. The taps of the Burt and Adelson kernel are $a$, $1/4$ and $1/4 - a/2$; they are all nonnegative exactly when $a \ge 0$ and $a \le 1/2$. By induction on $l$, both statements hold for every level of BUILD: each level is REDUCE of the one before, and the range of $G_{l+1}$ lies inside the range of $G_l$. $\square$

**Claim 3 (termination and the number of levels).** BUILD calls REDUCE exactly $\lceil \log_2 \max(W, H) \rceil$ times, and the last level is $1 \times 1$.

*Proof.* Let $M_l = \max(W_l, H_l)$. Since $\lceil \cdot / 2 \rceil$ is monotone, $M_{l+1} = \lceil M_l / 2 \rceil$. Define $k(M) = \lceil \log_2 M \rceil$ for $M \ge 1$, the least $k \ge 0$ with $M \le 2^k$. If $M \ge 2$ and $2^{k-1} < M \le 2^k$ with $k \ge 1$, then $2^{k-2} < M/2 \le \lceil M/2 \rceil \le 2^{k-1}$, where the step $\lceil M/2 \rceil \le 2^{k-1}$ holds because $2^{k-1}$ is an integer at least $M/2$. If $k = 1$ then $M = 2$ and $\lceil M/2 \rceil = 1$, so $k$ drops to 0. In all cases $k(M_{l+1}) = k(M_l) - 1$ while $M_l \ge 2$: the quantity $k$ drops by exactly 1 per loop pass. Line L8 continues while a level has more than one sample, that is while $M_l \ge 2$, and $M_l = 1$ means a $1 \times 1$ level. So the loop runs exactly $k(M_0) = \lceil \log_2 \max(W, H) \rceil$ times. $\square$

**Claim 4 (the size of the levels).** Let $S = \sum_{l=0}^{N} W_l H_l$ with $N = \lceil \log_2 \max(W, H) \rceil$.

1. If $W = H = 2^N$, then $S = (4WH - 1)/3$.
2. If sizes round down instead, $W_{l+1} = \lfloor W_l / 2 \rfloor$, and the chain stops before a size reaches 0, then $S < \frac{4}{3} WH$.
3. With sizes rounding up, $S \le \frac{4}{3}(W - 1)(H - 1) + 2(W + H - 2) + (N + 1)$, and $2^l (W_l - 1) \le W - 1$ for every $l$.

*Proof.* (1) For a power of two, $\lceil 2^k / 2 \rceil = 2^{k-1}$, so $W_l = H_l = 2^{N-l}$ and $S = \sum_{l=0}^{N} 4^{N-l} = \sum_{k=0}^{N} 4^k = (4^{N+1} - 1)/3$ by the geometric sum. Since $4^{N+1} = 4 \cdot 2^N \cdot 2^N = 4WH$, this is $(4WH - 1)/3$.

(2) By induction, $W_l \le W / 2^l$: it holds for $l = 0$, and $W_{l+1} = \lfloor W_l / 2 \rfloor \le W_l / 2 \le W / 2^{l+1}$. The same holds for $H_l$. So $W_l H_l \le WH / 4^l$, and summing over the finitely many levels gives $S \le WH \sum_{l=0}^{N'} 4^{-l} < WH \cdot \frac{1}{1 - 1/4} = \frac{4}{3} WH$, where the inequality is strict because the sum is finite.

(3) For an integer $n \ge 1$, $\lceil n/2 \rceil - 1 = \lfloor (n - 1)/2 \rfloor$: if $n = 2q$ both sides are $q - 1$, and if $n = 2q + 1$ both sides are $q$. So $W_{l+1} - 1 = \lfloor (W_l - 1)/2 \rfloor \le (W_l - 1)/2$, and by induction $W_l - 1 \le (W - 1)/2^l$, which is the second statement after a multiplication by $2^l$. The same holds for $H$. So

$$
W_l H_l \le \Big(\frac{W - 1}{2^l} + 1\Big)\Big(\frac{H - 1}{2^l} + 1\Big) = \frac{(W-1)(H-1)}{4^l} + \frac{W + H - 2}{2^l} + 1.
$$

Summing over $l = 0, \ldots, N$ and bounding the two geometric sums by their infinite values $\frac{4}{3}$ and $2$ (the terms are nonnegative) gives the bound. $\square$

**Why rounding up can exceed 4/3.** For $W = H = 2^k + 1$, $W_l = 2^{k-l} + 1$ for $l \le k$, so $S = \sum_{l=0}^{k} (2^{k-l} + 1)^2 + 1 = \frac{4^{k+1} - 1}{3} + 2(2^{k+1} - 1) + (k + 1) + 1$. For $k = 8$ this is $87381 + 1022 + 9 + 1 = 88413$, while $\frac{4}{3} \cdot 257^2 = 88065\frac{1}{3}$. The excess comes from the $2(W + H - 2)$ term, which the plain $4/3$ rule omits.
