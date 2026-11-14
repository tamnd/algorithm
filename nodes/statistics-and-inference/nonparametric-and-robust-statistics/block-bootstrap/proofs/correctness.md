---
title: Exact bootstrap moments of the block bootstrap mean
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The series $x_1, \ldots, x_n$ is fixed, $P^*$ and $E^*$ refer to the resampling only, $N = n - l + 1$, $k = \lceil n/l \rceil$, and $\bar B_i = \frac1l\sum_{t=i}^{i+l-1} x_t$ is the mean of the block that starts at $i$. Lines L1 to L7 build the resample from $k$ blocks whose start indices are independent and uniform on $\{1, \ldots, N\}$, and line L8 evaluates $s$ on it. So the algorithm samples from the moving block bootstrap law, and it remains to compute that law for the mean.

This file proves exact identities given the data. It does not prove that the block bootstrap is consistent; that needs conditions on the process (Künsch 1989), and the page measures it.

**Claim 1 (moving blocks, l divides n).** If $n = k l$, then $\bar x^* = \frac1k\sum_{q=1}^k \bar B_{I_q}$, and

$$E^*\bar x^* = \bar B := \frac1N\sum_{i=1}^N \bar B_i, \qquad \mathrm{Var}^*(\bar x^*) = \frac1k \cdot \frac1N\sum_{i=1}^N (\bar B_i - \bar B)^2.$$

*Proof.* When $l$ divides $n$, line L7 removes nothing, and the resample consists of exactly $k$ whole blocks of $l$ values each. Its mean is the average of the $k$ block means. The $\bar B_{I_q}$ are independent and each is uniform on the multiset $\{\bar B_1, \ldots, \bar B_N\}$, so each has mean $\bar B$ and variance $\frac1N\sum_i(\bar B_i - \bar B)^2$. The mean of $k$ independent copies has the same mean and $1/k$ of the variance. $\square$

With $l = 1$, $N = n$, $k = n$ and $\bar B_i = x_i$, so the claim gives $E^*\bar x^* = \bar x$ and $\mathrm{Var}^*(\bar x^*) = \frac{1}{n^2}\sum_i(x_i - \bar x)^2$, the iid bootstrap. Line L5 with $l = 1$ draws exactly the indices of the iid bootstrap, and the tests check that both give the same resample from the same seed.

**Claim 2 (end effects).** $\bar B = \sum_{t=1}^n w_t x_t$ with $w_t = \frac{m_t}{N l}$, where $m_t$ is the number of blocks that contain position $t$: $m_t = \min(t, l, N, n - t + 1)$. So $\bar B = \bar x$ for all data only if $l = 1$.

*Proof.* Each block mean gives weight $1/l$ to each of its $l$ positions, and $\bar B$ averages $N$ block means, so position $t$ gets weight $m_t/(N l)$. Position $t$ lies in the block that starts at $i$ exactly when $\max(1, t - l + 1) \le i \le \min(t, N)$, which gives the count $m_t$. For $1 < l < n$, $m_1 = 1 < l = m_l$ when $l \le N$, or $m_1 = 1 < N = m_l$ otherwise, so the weights are not all equal and some data give $\bar B \ne \bar x$. $\square$

The tests use $x = (10, 0, 0, 0, 0, 0)$ with $l = 2$, where $\bar B = 1$ and $\bar x = 5/3$.

**Claim 3 (circular blocks are centred).** In the circular block bootstrap, each start is uniform on $\{1, \ldots, n\}$ and the block wraps around, so every resampled value $x^*_t$ is uniform on the multiset $\{x_1, \ldots, x_n\}$. Hence $E^*\bar x^* = \bar x$.

*Proof.* Position $j$ inside a block that starts at a uniform $I$ holds $x_{((I + j - 2) \bmod n) + 1}$, and a uniform index shifted modulo $n$ is uniform. Linearity of expectation gives the result, also when line L7 cuts the last block. $\square$

**Claim 4 (the stationary bootstrap).** Let $J_1, \ldots, J_n$ be the indices of the stationary bootstrap: $J_1$ is uniform, and $J_{t+1}$ is uniform with probability $p$ and $J_t + 1 \bmod n$ otherwise. Then $(J_t)$ is a stationary Markov chain with uniform marginal law, $E^*\bar x^* = \bar x$, and

$$\mathrm{Var}^*(\bar x^*) = \frac{\hat c(0)}{n} + \frac{2}{n}\sum_{i=1}^{n-1}\Bigl(1 - \frac in\Bigr)(1 - p)^i\, \hat c(i), \qquad \hat c(i) = \frac1n\sum_{j=1}^n (x_j - \bar x)(x_{j+i} - \bar x),$$

with the index $j + i$ taken modulo $n$.

*Proof.* The transition probability is $P(a, c) = p/n + (1 - p)\,[c = a + 1 \bmod n]$. Each column of $P$ sums to $p + (1 - p) = 1$, so the uniform law is stationary, and the chain starts in it. So every $J_t$ is uniform, $E^* x^*_t = \bar x$, and $\mathrm{Var}^* x^*_t = \hat c(0)$.

For $s < t$ with $t - s = i$, condition on whether a new block starts at one of the steps $s + 1, \ldots, t$. With probability $(1 - p)^i$ no new block starts, and then $J_t = J_s + i \bmod n$ with $J_s$ uniform, so the covariance is $\hat c(i)$. Otherwise, after the last new start the index is uniform and independent of $J_s$, so $x^*_t$ is independent of $x^*_s$, and the covariance is 0. Since $E^* x^*_t = \bar x$ in both cases, the two cases combine to $\mathrm{Cov}^*(x^*_s, x^*_t) = (1 - p)^i \hat c(i)$. Then

$$\mathrm{Var}^*(\bar x^*) = \frac{1}{n^2}\Bigl(n\,\hat c(0) + 2\sum_{i=1}^{n-1}(n - i)(1 - p)^i \hat c(i)\Bigr),$$

because $n - i$ pairs $(s, t)$ have $t - s = i$. This is the stated formula. $\square$

The independence step needs care: given that a new block starts at step $r \le t$, the index $J_r$ is a fresh uniform draw, independent of everything before, and the later steps up to $t$ depend only on $J_r$ and fresh random numbers. So $J_t$ is uniform and independent of $J_s$.

The tests compute the exact law of $\bar x^*$ by listing all $n^n$ index paths with their probabilities as fractions, for $n \le 5$, and compare its mean and variance with $\bar x$ and with the formula.

**Why the iid bootstrap fails, as a computation.** With $l = 1$, $\mathrm{Var}^*(\bar x^*) = \hat c(0)/n$. For a stationary process with autocovariances $\gamma(i)$, $\mathrm{Var}(\bar X) = \frac{\gamma(0)}{n} + \frac{2}{n}\sum_{i=1}^{n-1}(1 - \frac in)\gamma(i)$. The iid bootstrap keeps only the first term. For AR(1), $\gamma(i) = \phi^i\gamma(0)$, and $n\mathrm{Var}(\bar X) \to \gamma(0)\frac{1 + \phi}{1 - \phi}$, so the ratio tends to $\frac{1 - \phi}{1 + \phi}$, which is $\frac13$ for $\phi = 0.5$. The stationary bootstrap keeps the other terms with the weights $(1 - p)^i$, which tend to 1 for each fixed $i$ as $p \to 0$. Making this into a consistency proof needs $p \to 0$, $n p \to \infty$ and summable autocovariances; we do not give it here.

**Cost.** Lines L4 to L7 copy $k l < n + l$ values, so one resample costs $\Theta(n)$, and with a linear-time statistic the $b$ replicates cost $\Theta(b n)$ time. The resample and the replicates need $\Theta(n + b)$ space.
