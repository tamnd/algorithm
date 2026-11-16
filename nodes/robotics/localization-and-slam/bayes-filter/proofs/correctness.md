---
title: The Bayes filter computes the posterior p(x_t | z_1:t, u_1:t)
proves: [correctness]
status: full
---

**Setting.** The states $x_0, x_1, \ldots$ take values in a finite set $X$ with $g$ elements. For a continuous state with densities, replace each sum over $X$ by an integral; the steps are the same. The data at time $t \ge 1$ are a control $u_t$ and a measurement $z_t$. Write $d_t = (z_{1:t}, u_{1:t})$ for the data up to time $t$, with $d_0$ empty. The model gives $p(x_0)$, the motion model $p(x_t \mid u_t, x_{t-1})$ and the measurement model $p(z_t \mid x_t)$.

**Assumptions.**

- (M1) State completeness for motion: $p(x_t \mid x_{0:t-1}, z_{1:t-1}, u_{1:t}) = p(x_t \mid u_t, x_{t-1})$.
- (M2) State completeness for measurement: $p(z_t \mid x_{0:t}, z_{1:t-1}, u_{1:t}) = p(z_t \mid x_t)$.
- (C) The control carries no news about the past state: $p(x_{t-1} \mid d_{t-1}, u_t) = p(x_{t-1} \mid d_{t-1})$. This holds when $u_t$ is a function of $d_{t-1}$ and of randomness that is independent of all states and measurements, because then, given $d_{t-1}$, the control is independent of $x_{t-1}$.
- (P) Each measurement that occurs has positive probability: $p(z_t \mid d_{t-1}, u_t) > 0$.

**Claim.** Let $\mathrm{bel}_0(x) = p(x_0 = x)$, and let $\mathrm{bel}_t$ be the output of BAYES-FILTER$(\mathrm{bel}_{t-1}, u_t, z_t)$. Then for every $t \ge 0$ and every $x \in X$,

$$\mathrm{bel}_t(x) = p(x_t = x \mid d_t).$$

*Proof.* By induction on $t$. For $t = 0$ the claim is the definition of $\mathrm{bel}_0$.

Let $t \ge 1$ and assume $\mathrm{bel}_{t-1}(x') = p(x_{t-1} = x' \mid d_{t-1})$ for all $x'$.

*Prediction (lines L1 and L2).* By the law of total probability over $x_{t-1}$, and then by the product rule,

$$p(x_t \mid d_{t-1}, u_t) = \sum_{x' \in X} p(x_t \mid x_{t-1} = x', d_{t-1}, u_t)\, p(x_{t-1} = x' \mid d_{t-1}, u_t).$$

In the first factor, (M1) removes the older states and data. Summing (M1) over $x_{0:t-2}$ shows that $p(x_t \mid x_{t-1}, d_{t-1}, u_t) = p(x_t \mid u_t, x_{t-1})$. In the second factor, (C) removes $u_t$, and the induction hypothesis gives $\mathrm{bel}_{t-1}(x')$. So

$$p(x_t \mid d_{t-1}, u_t) = \sum_{x' \in X} p(x_t \mid u_t, x_{t-1} = x')\, \mathrm{bel}_{t-1}(x'),$$

which is the value $\overline{\mathrm{bel}}(x_t)$ that line L2 computes.

*Correction (lines L3 to L5).* Bayes' theorem with the data $d_{t-1}, u_t$ held fixed gives

$$p(x_t \mid z_t, d_{t-1}, u_t) = \frac{p(z_t \mid x_t, d_{t-1}, u_t)\, p(x_t \mid d_{t-1}, u_t)}{p(z_t \mid d_{t-1}, u_t)}.$$

The left side is $p(x_t \mid d_t)$. In the numerator, (M2) summed over $x_{0:t-1}$ gives $p(z_t \mid x_t, d_{t-1}, u_t) = p(z_t \mid x_t)$, and the second factor is $\overline{\mathrm{bel}}(x_t)$. So the numerator is the value $\mathrm{bel}'(x_t)$ of line L3. The denominator does not depend on $x_t$. It equals $\sum_{x} p(z_t \mid x_t = x)\, \overline{\mathrm{bel}}(x) = \sum_x \mathrm{bel}'(x)$ by the law of total probability, and it is positive by (P). So $\eta$ of line L4 is $1 / p(z_t \mid d_{t-1}, u_t)$, and line L5 gives $\mathrm{bel}_t(x) = p(x_t = x \mid d_t)$. This completes the induction. $\square$

**The steps with missing data.** If no control is applied at time $t$, the state does not change, so $p(x_t \mid d_{t-1}) = \mathrm{bel}_{t-1}$ and skipping lines L1 and L2 is correct. If no measurement arrives, $d_t$ adds only $u_t$, and the prediction $\overline{\mathrm{bel}}$ is already $p(x_t \mid d_t)$, so skipping lines L3 to L5 is correct. The same induction covers both cases.

**The likelihood.** Let the controls be fixed in advance, so that they are not random. Then $p(z_t \mid d_{t-1}, u_t) = p(z_t \mid z_{1:t-1}; u_{1:T})$, and the chain rule gives $\prod_{t=1}^{T} p(z_t \mid d_{t-1}, u_t) = p(z_{1:T}; u_{1:T})$. So the product of the values $1/\eta$ is the likelihood of the measurements under the given controls. If a control depends on earlier measurements, a later control carries information about those measurements, and the product is the likelihood of the measurements only in the sense of the sequential decisions that were made.

**Termination and exactness.** Each call does $g$ sums of $g$ terms, $g$ products and one division, so it ends after $O(g^2)$ operations. With exact rational arithmetic (the Python implementation accepts fractions) every operation is exact, and the output equals the posterior with no error.

**What fails without the assumptions.** If (M2) fails, for example when two measurements share a noise term, the factor $p(z_t \mid x_t, d_{t-1}, u_t)$ differs from $p(z_t \mid x_t)$, and line L3 uses the wrong likelihood. The output is then still a probability distribution but not the posterior. If (P) fails, line L4 divides by zero.
