---
title: One step of MCL is an unbiased importance sample of the Bayes update, and its resampling is unbiased
proves: [correctness]
status: full
---

**Setting.** One step of plain MCL takes particles $x_{t-1}^{[1]}, \dots, x_{t-1}^{[N]}$, a control $u = u_t$ and a reading $z = z_t$. Write $\pi(x \mid x')$ for the density of the motion model $p(x_t = x \mid u, x_{t-1} = x', m)$ and $\ell(x) = p(z \mid x_t = x, m)$ for the measurement model. Line L2 draws $\bar x^{[k]} \sim \pi(\cdot \mid x_{t-1}^{[k]})$, independently for each $k$. Line L3 sets $w^{[k]} = \ell(\bar x^{[k]})$. Line L6 resamples with the low variance sampler: with $W = \sum_k w^{[k]}$, $\tilde w_k = w^{[k]} / W$, $C_0 = 0$ and $C_k = \tilde w_1 + \dots + \tilde w_k$, it draws $r$ uniform in $[0, 1/N)$, and for $i = 0, \dots, N-1$ it outputs the particle $k$ with $C_{k-1} < r + i/N \le C_k$.

**Assumptions.**

- (A1) $\ell$ is measurable, $0 \le \ell \le L$ for a constant $L$.
- (A2) $W > 0$. (If $W = 0$, plain MCL stops with an error.)
- (A3) For Claim 3 only: the $x_{t-1}^{[k]}$ are independent draws of a density $b$ (the prior belief), and $\eta = \int \ell(x)\, \bar b(x)\, dx > 0$, where $\bar b(x) = \int \pi(x \mid x')\, b(x')\, dx'$ is the predicted belief.

The arithmetic is exact; rounding is not part of the claims.

**Claim.**

1. For each bounded measurable $f$, given the particles $x_{t-1}^{[\cdot]}$,
$$E\Big[\frac{1}{N} \sum_k w^{[k]} f(\bar x^{[k]})\Big] = \frac{1}{N} \sum_k \int f(x)\, \ell(x)\, \pi(x \mid x_{t-1}^{[k]})\, dx.$$
The right side is $\int f\, \ell\, \bar b_N$, the unnormalized Bayes update of the empirical belief $b_N$ that puts mass $1/N$ on each $x_{t-1}^{[k]}$, after its prediction $\bar b_N(x) = \frac{1}{N} \sum_k \pi(x \mid x_{t-1}^{[k]})$.
2. Given the weighted particles, the low variance sampler outputs particle $k$ exactly $n_k$ times with $n_k \in \{\lfloor N \tilde w_k \rfloor, \lceil N \tilde w_k \rceil\}$, and $E[n_k] = N \tilde w_k$. So for each $f$, $E[\frac{1}{N} \sum_k n_k f(\bar x^{[k]})] = \sum_k \tilde w_k f(\bar x^{[k]})$.
3. Under (A3), as $N \to \infty$,
$$\frac{\sum_k w^{[k]} f(\bar x^{[k]})}{\sum_k w^{[k]}} \to \frac{\int f(x)\, \ell(x)\, \bar b(x)\, dx}{\eta} = E[f(x_t) \mid z_{1:t}, u_{1:t}, m]$$
almost surely, where the right side is the posterior of the Bayes filter with prior $b$.

*Proof.*

*Claim 1.* Fix $k$. Given $x_{t-1}^{[k]}$, the draw $\bar x^{[k]}$ has the density $\pi(\cdot \mid x_{t-1}^{[k]})$. The function $f \ell$ is bounded by (A1), so its expectation exists and is $E[w^{[k]} f(\bar x^{[k]})] = E[\ell(\bar x^{[k]}) f(\bar x^{[k]})] = \int f(x)\, \ell(x)\, \pi(x \mid x_{t-1}^{[k]})\, dx$. Sum over $k$, divide by $N$ and use the linearity of the expectation. The last sentence of the claim is the definition of $\bar b_N$ and the update step of the [Bayes filter](/bayes-filter/) before normalization.

*Claim 2.* By (A2) the $\tilde w_k$ are defined, are $\ge 0$ and sum to 1, so the half-open intervals $I_k = (C_{k-1}, C_k]$ for $k = 1, \dots, N$ are disjoint and cover $(0, 1]$. The points $u_i = r + i/N$, $i = 0, \dots, N-1$, lie in $[0, 1)$. The point $u_i = 0$ occurs only if $r = 0$, an event of probability 0; the code then gives it to the first particle with $C_k \ge 0$, which does not change the claims below for $r > 0$. So, almost surely, each point lies in exactly one $I_k$, and $n_k$ is the number of points in $I_k$.

Let $r > 0$. The points of the infinite progression $r + i/N$, $i \in \mathbb{Z}$, that lie in $(0, 1]$ are exactly $u_0, \dots, u_{N-1}$, because $u_{-1} = r - 1/N < 0$ and $u_N = r + 1 > 1$. So $n_k$ is the number of points of the infinite progression in $I_k = (a, a + \tilde w_k]$ with $a = C_{k-1}$. The condition $a < r + i/N \le a + \tilde w_k$ is $y < i \le y + N \tilde w_k$ with $y = N(a - r)$, so

$$n_k = \lfloor y + N \tilde w_k \rfloor - \lfloor y \rfloor.$$

For real $y$ and $s \ge 0$, $\lfloor y + s \rfloor - \lfloor y \rfloor$ is $\lfloor s \rfloor$ or $\lfloor s \rfloor + 1$, and it equals $s$ if $s$ is an integer. So $n_k \in \{\lfloor N \tilde w_k \rfloor, \lceil N \tilde w_k \rceil\}$.

For the mean, $r$ is uniform in $[0, 1/N)$. The point $u_i$ is uniform in $[i/N, (i+1)/N)$, with the density $N$ there. So $P(u_i \in I_k) = N \cdot |I_k \cap [i/N, (i+1)/N)|$, and

$$E[n_k] = \sum_{i=0}^{N-1} N \cdot |I_k \cap [i/N, (i+1)/N)| = N \cdot |I_k \cap [0, 1)| = N \tilde w_k.$$

The last statement of the claim follows by linearity: $E[\frac{1}{N} \sum_k n_k f(\bar x^{[k]})] = \frac{1}{N} \sum_k N \tilde w_k f(\bar x^{[k]})$.

*Claim 3.* Under (A3), the pairs $(x_{t-1}^{[k]}, \bar x^{[k]})$ are independent and identically distributed, and each $\bar x^{[k]}$ has the density $\bar b$. The variables $w^{[k]} f(\bar x^{[k]})$ and $w^{[k]}$ are bounded by (A1), so by the strong law of large numbers

$$\frac{1}{N} \sum_k w^{[k]} f(\bar x^{[k]}) \to \int f\, \ell\, \bar b \quad \text{and} \quad \frac{1}{N} \sum_k w^{[k]} \to \int \ell\, \bar b = \eta$$

almost surely. Since $\eta > 0$, the ratio converges almost surely to $\int f\, \ell\, \bar b / \eta$. By the Bayes filter, the posterior density is $\ell(x)\, \bar b(x) / \eta$, so this limit is the posterior mean of $f$. $\blacksquare$

**What this does not show.** After a resampling step the particles are not independent, so Claim 3 does not apply to step $t + 1$ directly. Convergence over many steps is a theorem of the theory of sequential Monte Carlo, under conditions such as bounded likelihoods, and is not proved here. Augmented MCL changes the particle set on purpose, so its particles do not approximate the Bayes posterior; Claims 1 and 2 hold for its lines L1 to L6.
