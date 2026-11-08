---
title: The Halton rule has error at most V_HK times the star discrepancy, and shifted replicates are unbiased
proves: [correctness]
status: full
---

Let $p_1 < \cdots < p_s$ be the first $s$ primes, $\phi_b$ the radical inverse in base $b$, and $h_i = (\phi_{p_1}(i), \ldots, \phi_{p_s}(i))$ the $i$-th Halton point. QMC with $R = 0$ returns $Q_N(f) = \frac{V}{N}\sum_{i=1}^N f(a + h_i \odot (b - a))$ with $V = \prod_k (b_k - a_k)$; with $R \ge 1$ each replicate uses $\{h_i + \Delta_r\}$, the fractional part taken coordinatewise, for an independent uniform $\Delta_r \in [0, 1)^s$. Lines refer to the pseudocode QMC.

**Lemma 1 (radical inverse).** If $i = \sum_{k=0}^{m-1} d_k b^k$ with digits $0 \le d_k < b$, lines L10 and L11 return $\phi_b(i) = \sum_{k=0}^{m-1} d_k b^{-k-1} \in [0, 1)$.

*Proof.* Before the $j$-th pass of the loop ($j = 0, 1, \ldots$), $i = \lfloor i_0 / b^j \rfloor$, $f = b^{-j-1}$ and $r = \sum_{k<j} d_k b^{-k-1}$. The pass takes $d = i \bmod b = d_j$, so the invariant holds for $j + 1$. The loop stops when $i = 0$, after $m$ passes. The sum is at most $\sum_k (b-1) b^{-k-1} = 1 - b^{-m} < 1$. $\square$

**Lemma 2 (elementary boxes).** Let $m_1, \ldots, m_s \ge 0$ and $M = \prod_k p_k^{m_k}$. Any $M$ consecutive indices $i = q, q+1, \ldots, q + M - 1$ give exactly one Halton point in each box $\prod_k [\,j_k p_k^{-m_k}, (j_k + 1) p_k^{-m_k})$, $0 \le j_k < p_k^{m_k}$.

*Proof.* By Lemma 1, the first $m_k$ base-$p_k$ digits of $\phi_{p_k}(i)$ are the last $m_k$ digits of $i$ in reverse order, so the box index $j_k$ of $\phi_{p_k}(i)$ is a bijective function of $i \bmod p_k^{m_k}$. The moduli $p_k^{m_k}$ are pairwise coprime, so by the Chinese remainder theorem $i \mapsto (i \bmod p_k^{m_k})_k$ is a bijection from any $M$ consecutive integers onto all residue tuples. $\square$

**Theorem 1 (one-dimensional discrepancy, proved).** For any $q \ge 0$ and $N \ge 1$, the points $\phi_b(q + 1), \ldots, \phi_b(q + N)$ have $N D_N^* \le (b - 1)(\lfloor \log_b N \rfloor + 1)$.

*Proof.* Write $N = \sum_{j=0}^{J} c_j b^j$ in base $b$, $J = \lfloor \log_b N \rfloor$, and cut the $N$ consecutive indices into $\sum_j c_j$ runs of consecutive indices, $c_j$ runs of length $b^j$. By Lemma 2 with $s = 1$, a run of length $b^j$ puts exactly one point into each interval $[l b^{-j}, (l+1) b^{-j})$. For $t \in [0, 1]$, $[0, t)$ contains $\lfloor t b^j \rfloor$ of these intervals entirely and meets at most one more, so the run has between $\lfloor t b^j \rfloor$ and $\lfloor t b^j \rfloor + 1$ points in $[0, t)$, while $b^j t$ lies in $[\lfloor t b^j \rfloor, \lfloor t b^j \rfloor + 1)$; the difference is less than 1 in absolute value. Summing over runs, $|A(t) - N t| < \sum_j c_j \le (b - 1)(J + 1)$. $\square$

**Theorem 2 (deterministic error).** Let $g(u) = f(a + u \odot (b - a))$ on $[0, 1]^s$, with continuous mixed partial derivatives. Then for $R = 0$,

$$\Big| Q_N(f) - \int_{[a,b]} f \Big| \le |V|\, V_{HK}(g)\, D_N^*(h_1, \ldots, h_N).$$

*Proof.* By the substitution $x = a + u \odot (b - a)$, $\int_{[a, b]} f = V \int_{[0,1]^s} g$, with $V$ signed when some $b_k < a_k$ (orientation). Lines L5 to L8 compute $Q_N(f) = \frac{V}{N}\sum_i g(h_i)$ with $h_i \in [0, 1)^s$ by Lemma 1. Apply the [Koksma-Hlawka inequality](/koksma-hlawka-inequality/), proved there for such $g$. $\square$

With Halton's bound $D_N^* = O((\log N)^s / N)$ for the Halton points (cited: Halton 1960; Niederreiter 1992, Theorem 3.6), the error is $O((\log N)^s/N)$ for fixed $g$. For $s = 1$, Theorem 1 gives this with an explicit constant.

**Theorem 3 (shifted replicates are unbiased).** If $\Delta$ is uniform on $[0, 1)^s$, then for every fixed $y \in [0, 1)^s$ the point $\{y + \Delta\}$ is uniform on $[0, 1)^s$. Hence for $f$ integrable on the box, each replicate value $Q_r$ of line L8 satisfies $\mathbb{E}[Q_r] = \int_{[a, b]} f$; if moreover $f$ is square integrable, the replicates are independent with a common finite variance, the mean of line L9 is unbiased, and the squared standard error of line L9 is an unbiased estimator of its variance.

*Proof.* In each coordinate, $u \mapsto \{y_k + u\}$ is a measure-preserving bijection of $[0, 1)$ (a rotation of the circle), and the coordinates of $\Delta$ are independent, so the product map preserves the uniform measure on $[0, 1)^s$. Then $\mathbb{E}[g(\{h_i + \Delta\})] = \int g$ for each $i$, and $\mathbb{E}[Q_r] = \frac{V}{N}\sum_i \int g = \int_{[a,b]} f$. Each $Q_r$ is a function of $\Delta_r$ alone, the $\Delta_r$ are independent, and $\operatorname{Var}(Q_r) \le V^2 \int g^2 < \infty$ by Cauchy-Schwarz. For independent identically distributed values with finite variance, the sample mean is unbiased and the sample variance with divisor $R - 1$ is unbiased for the variance; dividing by $R$ gives the variance of the mean. $\square$

**Termination and cost.** Line L2 runs $\max(R, 1)$ times and line L5 $N$ times inside, so $f$ is evaluated $N \max(R, 1)$ times. Each Halton point costs $\sum_k \lceil \log_{p_k}(i + 1) \rceil = O(s \log N)$ digit operations by Lemma 1, so the other work is $O(R N s \log N)$. $\blacksquare$

**Floating point.** $\phi_2(i)$ is computed exactly for $i < 2^{53}$, since every partial sum is a dyadic rational with at most 53 significant bits. For other bases each step rounds, and the computed value differs from $\phi_b(i)$ by a few units in the last place; the test file checks the error against exact rational digit reversal to $10^{-15}$. Such errors shift points across box edges only when a point lies exactly on an edge and do not affect the integration error at any practical $N$.
