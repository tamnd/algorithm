---
title: The pCN chain stops after the given number of steps and leaves the posterior invariant
proves: [correctness, termination]
status: full
---

**Setting.** $\mu_0 = N(m_0, C)$ is a Gaussian prior on $\mathbb{R}^n$ with $C$ symmetric positive definite, $\Phi: \mathbb{R}^n \to \mathbb{R}$ is measurable, and $Z = \int\exp(-\Phi)\,d\mu_0$ is finite and positive. The target is the posterior $\mu^y(du) = Z^{-1}\exp(-\Phi(u))\,\mu_0(du)$. Fix $\beta \in (0, 1]$ and put $\rho = \sqrt{1 - \beta^2}$. The proposal kernel $q(u, \cdot)$ is the law of $v = m_0 + \rho(u - m_0) + \beta\xi$ with $\xi \sim N(0, C)$, which is line L4. The proofs below use only Gaussian measures and densities with respect to $\mu_0$, so they hold word for word on a separable Hilbert space with a trace-class $C$.

**Claim 1 (termination and output).** For $N \ge 1$ steps, the procedure stops after exactly $N$ passes of lines L3 to L8, returns a list of $N$ states, and an acceptance rate in $[0, 1]$.

*Proof.* Line L2 runs a loop of fixed length $N$. Each pass draws one prior sample (L3), forms one proposal (L4), evaluates $\Phi$ once (L5), and does a constant amount of other work, so it ends if $\Phi$ ends. Line L8 appends one state per pass, and the counter of accepted moves is between $0$ and $N$. Line L9 returns. $\square$

**Claim 2 (the proposal keeps the prior and is reversible for it).** If $u \sim \mu_0$ and $v \sim q(u, \cdot)$, then $(u, v)$ and $(v, u)$ have the same law. In particular $v \sim \mu_0$, and $\mu_0(du)\,q(u, dv) = \mu_0(dv)\,q(v, du)$.

*Proof.* Put $u' = u - m_0$ and $v' = v - m_0 = \rho u' + \beta\xi$, with $u' \sim N(0, C)$ and $\xi \sim N(0, C)$ independent. The pair $(u', v')$ is jointly Gaussian with mean zero, and

$$\mathrm{Cov}(u') = C, \qquad \mathrm{Cov}(v') = \rho^2C + \beta^2C = C, \qquad \mathrm{Cov}(u', v') = \rho C.$$

The last matrix is symmetric, so $(v', u')$ has the same covariance blocks as $(u', v')$. A centred Gaussian law is fixed by its covariance, so the two pairs have the same law. Shifting by $m_0$ gives the claim. $\square$

**Claim 3 (the acceptance test).** Given $u$ and $v$, line L6 accepts with probability $a(u, v) = \min\{1, \exp(\Phi(u) - \Phi(v))\}$.

*Proof.* `rng.random()` is uniform on $[0, 1)$, so $U = 1 - $ `rng.random()` is uniform on $(0, 1]$ and $\log U$ is finite. With $d = \Phi(u) - \Phi(v)$, the test $\log U < d$ is the event $U < e^d$, whose probability is $\min\{1, e^d\}$. $\square$

**Claim 4 (detailed balance and invariance).** The transition kernel of one pass,

$$P(u, dv) = a(u, v)\,q(u, dv) + r(u)\,\delta_u(dv), \qquad r(u) = 1 - \int a(u, w)\,q(u, dw),$$

satisfies $\mu^y(du)P(u, dv) = \mu^y(dv)P(v, du)$. So if the state has law $\mu^y$ before a pass, it has law $\mu^y$ after it.

*Proof.* For the moving part,

$$\mu^y(du)\,a(u, v)\,q(u, dv) = Z^{-1}e^{-\Phi(u)}\min\{1, e^{\Phi(u) - \Phi(v)}\}\,\mu_0(du)\,q(u, dv) = Z^{-1}\min\{e^{-\Phi(u)}, e^{-\Phi(v)}\}\,\mu_0(du)\,q(u, dv).$$

The scalar factor is symmetric in $(u, v)$, and by Claim 2 so is the measure $\mu_0(du)\,q(u, dv)$. Hence the moving part is symmetric. The staying part $\mu^y(du)\,r(u)\,\delta_u(dv)$ lives on the diagonal $u = v$ and is symmetric too. Integrating the detailed balance relation over $u$ gives $\int\mu^y(du)P(u, B) = \mu^y(B)$ for every measurable $B$. $\square$

By Claim 3, lines L4 to L7 draw from $P(u_k, \cdot)$, and line L8 stores the new state, so the stored chain is a Markov chain with kernel $P$ and invariant law $\mu^y$. The prior density never enters the acceptance ratio. This is why the method is defined on a function space, where $\mu_0$ has no Lebesgue density.

**Claim 5 (averages converge in finite dimension).** Let $n$ be finite and $\Phi$ be finite everywhere. Then for every $\mu^y$-integrable $f$ and $\mu^y$-almost every start $u_0$, $\frac1N\sum_{k=1}^Nf(u_k) \to \int f\,d\mu^y$ almost surely.

*Proof.* The proposal $q(u, \cdot)$ has a Gaussian density that is positive everywhere, because $\beta > 0$ and $C$ is positive definite, and $a(u, v) > 0$ for all $u, v$ because $\Phi$ is finite. So for every set $B$ with $\mu^y(B) > 0$, which has positive Lebesgue measure, $P(u, B) > 0$ from every $u$. The chain is $\mu^y$-irreducible. It has the invariant probability measure $\mu^y$ by Claim 4. A $\mu^y$-irreducible chain with an invariant probability measure satisfies the law of large numbers for $\mu^y$-almost every start; this is a standard theorem on Markov chains (Tierney 1994, Meyn and Tweedie). $\square$

The theorem says nothing about the speed. The speed is what distinguishes pCN from random-walk Metropolis: Hairer, Stuart and Vollmer (2014) prove a spectral gap for pCN that does not depend on the dimension, under conditions on $\Phi$. That result is cited, not proved here, and the test of the dimension effect in the implementation is a measurement.
