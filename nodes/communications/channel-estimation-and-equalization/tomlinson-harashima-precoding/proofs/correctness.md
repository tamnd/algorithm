---
title: Tomlinson-Harashima precoding delivers each symbol plus a multiple of 2M, so a modulo and a slicer recover it, with a bounded transmit signal
proves: [correctness]
status: full
---

The alphabet on each real dimension is M-PAM with the points $M - 1 - 2i$, $i = 0, \ldots, M-1$. They lie in $(-M, M)$ at spacing 2. For a real $v$, let $\mathrm{mod}(v) = v - 2M \lfloor (v + M)/(2M) \rfloor$, and for a complex $v$ apply it to the real and the imaginary parts. The channel is $y[k] = \sum_{l=0}^{L-1} h_l\, x[k-l] + w[k]$ with $h_0 \ne 0$ and $x[k] = 0$ for $k < 0$. Let $g = h / h_0$, so $g_0 = 1$ (line L1).

The precoder (lines L2 to L5) computes $v[k] = \sum_{j=1}^{L-1} g_j\, x[k-j]$ and $x[k] = \mathrm{mod}(a[k] - v[k])$. The receiver (lines L6 to L9) computes $u[k] = y[k]/h_0$ and slices $\mathrm{mod}(u[k])$ to the nearest point on the circle of length $2M$.

**Lemma 1 (the modulo).** For every real $v$, $\mathrm{mod}(v) \in [-M, M)$ and $v - \mathrm{mod}(v) \in 2M\mathbb{Z}$. If $v - v' \in 2M\mathbb{Z}$, then $\mathrm{mod}(v) = \mathrm{mod}(v')$. If $v \in [-M, M)$, then $\mathrm{mod}(v) = v$.

*Proof.* Let $t = \lfloor (v + M)/(2M) \rfloor$. Then $t \le (v + M)/(2M) < t + 1$, so $-M \le v - 2Mt < M$. The difference $v - \mathrm{mod}(v) = 2Mt$. If $v' = v + 2Ms$ with $s$ an integer, the floor grows by exactly $s$, so the two results agree. If $v \in [-M, M)$, then $t = 0$. $\square$

**Theorem 1 (bounded transmit signal).** Every precoded sample satisfies $\mathrm{Re}\, x[k], \mathrm{Im}\, x[k] \in [-M, M)$, for every channel $h$ with $h_0 \ne 0$, including channels with zeros outside the unit circle.

*Proof.* Line L4 applies the modulo, so Lemma 1 gives the bound. $\square$

**Theorem 2 (the received signal).** For every $k$, $u[k] = a[k] + 2M\, d[k] + w[k]/h_0$ for some $d[k]$ whose real and imaginary parts are integers.

*Proof.* $u[k] = \sum_j g_j\, x[k-j] + w[k]/h_0 = x[k] + v[k] + w[k]/h_0$. By Lemma 1 on each dimension, $(a[k] - v[k]) - x[k] = -2M d[k]$ for some $d[k]$ with integer real and imaginary parts. So $x[k] + v[k] = a[k] + 2M d[k]$. $\square$

**Corollary 1 (noiseless recovery).** If $w = 0$, the receiver decides $a[k]$ for every $k$.

*Proof.* By Theorem 2 and Lemma 1, $\mathrm{mod}(u[k]) = \mathrm{mod}(a[k]) = a[k]$ on each dimension, because $a[k] \in (-M, M)$. The slicer returns the point itself. $\square$

**Corollary 2 (the error rate).** Let the noise on one real dimension of $w[k]/h_0$ be Gaussian with mean zero and standard deviation $\sigma$. The decision on that dimension is wrong with probability
$$P_e = 1 - \sum_{i \in \mathbb{Z}} \Big[\Phi\Big(\frac{2Mi + 1}{\sigma}\Big) - \Phi\Big(\frac{2Mi - 1}{\sigma}\Big)\Big],$$
the same for every point and every channel, and $P_e = 2Q(1/\sigma) - \delta$ with $0 \le \delta \le 2 \sum_{i \ge 1} Q((2Mi - 1)/\sigma)$.

*Proof.* By Theorem 2 and Lemma 1, $\mathrm{mod}(u[k]) = \mathrm{mod}(a[k] + n)$ for the noise $n$ of that dimension. On the circle of length $2M$, the $M$ points are equally spaced at distance 2, so the nearest point to $a + n$ is $a$ exactly when $n$ lies within distance 1 of a multiple of $2M$, that is, in $[2Mi - 1, 2Mi + 1)$ for some integer $i$ (the boundary has probability zero). Summing these Gaussian probabilities gives $1 - P_e$. The term $i = 0$ alone gives $1 - 2Q(1/\sigma)$. The terms with $i \ne 0$ add $\delta$, and each of the two tails $i \ge 1$ and $i \le -1$ is at most $\sum_{i \ge 1} Q((2Mi - 1)/\sigma)$. $\square$

Every point has two neighbours on the circle, so the error rate is $2Q(1/\sigma)$ for all points, against $2(1 - 1/M)\, Q(1/\sigma)$ for M-PAM without the modulo, where the two outer points have only one neighbour.

**Corollary 3 (equivalence with the ideal DFE).** The receiver of Theorem 2 sees the same noise $w[k]/h_0$ as a zero-forcing DFE with $c_0 = 1/h_0$, $b_j = g_j$ and correct feedback, with the alphabet extended periodically by $2M$.

*Proof.* The ZF-DFE with correct feedback computes $u[k] - \sum_{j \ge 1} g_j\, x_{\text{DFE}}[k-j] = a[k] + w[k]/h_0$ when the transmitted sequence is $a$ itself. The THP receiver gets $a[k] + 2M d[k] + w[k]/h_0$, the same up to a multiple of $2M$ that the modulo removes. $\square$

**Remark (transmit power, a heuristic with a measurement).** If the samples $x[k]$ are uniformly distributed on $[-M, M)$, their power is $M^2/3$ per dimension, against $(M^2-1)/3$ for M-PAM, a factor $M^2/(M^2 - 1)$. The uniform law is not a theorem for every channel: if $g_j$ is small, $x[k] \approx a[k]$. On dispersive channels it is close: for 4-PAM and 40000 symbols (seed 7303), the measured power was 5.344 on $(1, 0.9, 0.6)$, 5.328 on $(1, 0.5)$ and 5.059 on $(1, 0.1)$, against $16/3 = 5.333$ and the PAM power 5.
