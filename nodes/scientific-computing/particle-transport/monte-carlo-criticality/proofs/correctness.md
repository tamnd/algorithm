---
title: One cycle is correct in expectation, the large-N limit is power iteration, and the naive error ignores correlation
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform random numbers. The slab, the cross sections and the lines L1 to L12 are those of the page. We assume $\Sigma_s < \Sigma_t$, so that a neutron has on average at most $\Sigma_t/(\Sigma_t - \Sigma_s)$ collisions, and $\nu\Sigma_f > 0$.

**The next-generation kernel.** For a neutron born at $x$ with an isotropic direction, let $C(x, \cdot)$ be its analog collision density: for a set $D$ of points, $\int_D C(x, y)\, dy$ is the expected number of its collisions in $D$. The expected number of fission neutrons it makes in $D$ is
$$\int_D f(x, y)\, dy, \qquad f(x, y) = \frac{\nu\Sigma_f}{\Sigma_t}\, C(x, y),$$
and the operator of the page is $(\mathcal{F}s)(y) = \int s(x) f(x, y)\, dx$.

**Lemma 1 (one cycle in expectation).** Let the source of a cycle be the sites $x_1, \ldots, x_N$, and let $k$ be the value used in line L7. Then for every set $D$,
$$E[\text{number of banked sites in } D] = \frac{1}{k} \sum_{n = 1}^{N} \int_D f(x_n, y)\, dy, \qquad E[k_g] = \frac{1}{N} \sum_{n = 1}^{N} \int_0^L f(x_n, y)\, dy.$$

*Proof.* Lines L4, L5 and L8 are the analog game, so the collisions of the neutron from $x_n$ have the density $C(x_n, \cdot)$. At a collision at $y$, line L7 banks $\lfloor a + \xi \rfloor$ sites with $a = \nu\Sigma_f/(\Sigma_t k)$. If $a = m + r$ with an integer $m$ and $0 \le r < 1$, this is $m + 1$ with probability $r$ and $m$ otherwise, so its mean is $a$. The random number $\xi$ is independent of the past, so the expected number of banked sites in $D$ is $a \int_D C(x_n, y)\, dy = (1/k) \int_D f(x_n, y)\, dy$. The sum over the $N$ neutrons gives the first formula. Line L6 adds $\nu\Sigma_f/\Sigma_t$ at each collision in the slab, so the expected total for neutron $n$ is $\int_0^L f(x_n, y)\, dy$, and line L9 divides by $N$. $\square$

So, given the source, the bank is an unbiased estimate of $\mathcal{F}$ applied to the empirical source, divided by $k$, and $k_g$ is an unbiased estimate of the number of fission neutrons per source neutron. The value of $k$ in line L7 changes only the size of the bank, not its shape.

**Theorem 1 (the limit of many neutrons is power iteration).** Let the first source be $N$ independent sites with a density $s_0$, and fix a number of cycles $G$. Write $\|s\| = \int_0^L s(x)\, dx$ and $s_{g+1} = \mathcal{F}s_g/\|\mathcal{F}s_g\|$. Then for every $g \le G$, as $N \to \infty$, $k_g \to \|\mathcal{F}s_{g-1}\|$ in probability, and the empirical distribution of the source of cycle $g + 1$ converges weakly in probability to the density $s_g$.

*Proof.* We use induction on $g$. Let $\Pi$ be the empirical distribution of the current source, and assume that $\Pi$ converges weakly in probability to a density $s$ (for $g = 1$ this is the law of large numbers for the $N$ independent first sites). Let $\varphi$ be a bounded continuous function on $[0, L]$, and let $Y_n$ be the sum of $\varphi$ over the sites that neutron $n$ banks.

Given the source, the $Y_n$ are independent. Each $|Y_n|$ is at most $\max|\varphi|$ times the number of collisions of neutron $n$ times $\lceil a \rceil$, and the number of collisions is geometric, so $E[Y_n^2 \mid \text{source}] \le M_2$, a constant that does not depend on the source. By Lemma 1, $E[Y_n \mid x_n] = (1/k) \int \varphi(y) f(x_n, y)\, dy$, and this is a bounded continuous function of $x_n$, because the collision density of a neutron in a slab depends continuously on its birth point. By Chebyshev's inequality with the bound $M_2$, $\frac{1}{N}\sum_n Y_n - \frac{1}{N}\sum_n E[Y_n \mid x_n] \to 0$ in probability, and by the weak convergence of $\Pi$, $\frac{1}{N}\sum_n E[Y_n \mid x_n] \to (1/k)\int \varphi\, \mathcal{F}s$ in probability. The same argument with $\varphi = 1$ and with the score of line L6 gives $|\text{bank}|/N \to \|\mathcal{F}s\|/k$ and $k_g \to \|\mathcal{F}s\|$. Here $k$ is the value of the previous cycle, which converges in probability by the induction (or is the fixed $k_0$ in the first cycle), and it is positive.

So the empirical distribution of the bank converges weakly in probability to $\mathcal{F}s/\|\mathcal{F}s\|$, and $\|\mathcal{F}s\| > 0$ because $\nu\Sigma_f > 0$. Line L10 draws $N$ sites independently from the bank. Given the bank, the mean of $\varphi$ over these sites has the conditional mean equal to the mean over the bank and a conditional variance at most $\max\varphi^2/N$, so it converges in probability to the same limit. This is the induction step. $\square$

So in the limit the sources are the iterates of [power iteration](/power-iteration/) on $\mathcal{F}$ with the normalization $\|s\| = 1$, and $k_g$ is the norm of $\mathcal{F}$ applied to the normalized source. If $\mathcal{F}$ has a simple positive eigenvalue $k_{\mathrm{eff}}$ that is larger in modulus than all others, with a positive eigenfunction $s^\star$ (the [k-eigenvalue problem](/k-eigenvalue-problem/) page gives this for the slab), and $s_0$ has a positive component along $s^\star$, then $s_g \to s^\star$ and $\|\mathcal{F}s_g\| \to k_{\mathrm{eff}}$, and the error in the shape falls by about the dominance ratio $|k_2|/k_{\mathrm{eff}}$ per cycle. This is the convergence theorem of power iteration. The theorem above holds for a fixed number of cycles; it does not say that a run with a finite $N$ and very many cycles has a mean equal to $k_{\mathrm{eff}}$.

**The bias for finite $N$ (cited).** With a finite $N$, the source is random, and $E[\mathcal{F}\Pi/\|\mathcal{F}\Pi\|]$ is not $\mathcal{F}E[\Pi]/\|\mathcal{F}E[\Pi]\|$, because the normalization is a nonlinear map. So the stationary mean of the source is not exactly the fundamental mode, and the mean of $k_g$ differs from $k_{\mathrm{eff}}$. Brissenden and Garlick (1986) show that this bias is of order $1/N$. We do not prove this here. In the 25 runs of the page, the mean of $k$ is $1.11931$ with a standard error of $0.00712/\sqrt{25} = 0.0014$, about half a standard error from the $S_N$ value $1.12006$, so the bias is not visible at this accuracy (a measurement).

**Theorem 2 (the variance of the mean of correlated cycles).** Let $k_{I+1}, \ldots, k_{I+A}$ be a stationary sequence with the variance $\sigma^2$ and the correlations $\rho_j = \operatorname{Corr}(k_g, k_{g+j})$. Then the mean $\bar k$ of line L12 has
$$\operatorname{Var}(\bar k) = \frac{\sigma^2}{A}\Big(1 + 2\sum_{j = 1}^{A - 1}\Big(1 - \frac{j}{A}\Big)\rho_j\Big).$$
The naive estimate of line L12, the sample variance divided by $A$, estimates $\sigma^2/A$ (up to a term of order $1/A$), so it is too small when the $\rho_j$ are positive.

*Proof.* $\operatorname{Var}(\bar k) = A^{-2}\sum_{g, h}\operatorname{Cov}(k_g, k_h)$. There are $A$ terms with $g = h$, each $\sigma^2$, and for each $j \ge 1$ there are $2(A - j)$ terms with $|g - h| = j$, each $\sigma^2\rho_j$. Adding them gives the formula. $\square$

The correlations come from the bank: a cycle with more sites in a region starts more neutrons there in the next cycle. The cited paper of Ueki, Brown, Parsons and Kornreich relates the decay of the $\rho_j$ for tallies of the source shape to the dominance ratio. The 25 independent runs of the page are a measurement of this effect: the ratio of the true spread to the naive error is $1.02$ for $k$ and $2.10$ for a local tally.
