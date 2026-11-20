---
tag: R4B3XS
kind: algorithm
slug: expectation-propagation-detection
name: Expectation propagation detection
aliases:
- EP detector
area: communications/mimo-communications
level: research
summary: Approximates the posterior of the symbol vector by a Gaussian that expectation propagation refines one symbol at a time, then decides each symbol. It starts from the MMSE estimate.
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {n: the number of transmitted streams, m: the number of receive antennas, M: the constellation size, T: the number of iterations}
  time: {worst: O(n^2 m + T (n^3 + n M))}
  space: {extra: O(n^2 + n m)}
properties: {deterministic: true, exact_ml: false, needs_noise_level: true, needs_matrix_inverse: true, first_iterate: "the linear MMSE estimate", exact_marginals_when: "H^H H is diagonal and every update is kept"}
history:
  year: 2014
  people: [Javier Céspedes, Pablo M. Olmos, Matilde Sánchez-Fernández, Fernando Pérez-Cruz]
  note: "Minka introduced expectation propagation in 2001. Céspedes, Olmos, Sánchez-Fernández and Pérez-Cruz used it for MIMO detection with high-order constellations in 2014."
prereqs: [mimo-detection, mmse-mimo-detector, expectation-propagation]
see_also: [expectation-propagation, amp-mimo-detection, mmse-mimo-detector, belief-propagation, kullback-leibler-divergence, soft-demapping, turbo-equalization, massive-mimo]
sources:
  - paper: "Javier Céspedes, Pablo M. Olmos, Matilde Sánchez-Fernández and Fernando Pérez-Cruz, Expectation propagation detection for high-order high-dimensional MIMO systems, IEEE Transactions on Communications 62(8), 2840-2849, 2014"
    locator: "the EP detector for the real-valued MIMO model: the Gaussian site factors, the cavity and moment-matching updates, the rule that keeps the old site when the new precision is negative, the damping, and the comparison with MMSE and other detectors"
  - paper: "Thomas P. Minka, Expectation propagation for approximate Bayesian inference, Proc. 17th Conference on Uncertainty in Artificial Intelligence (UAI), 2001"
    locator: "the general EP algorithm: exponential-family approximation, removal of one site, moment matching and the site update"
---

Expectation propagation (EP) detection solves the [MIMO detection](/mimo-detection/) problem by an approximation of the posterior distribution of the transmitted vector. The true posterior is a Gaussian likelihood times a discrete prior, one factor for each symbol. EP replaces each discrete prior factor by a Gaussian factor and then improves the Gaussian factors one at a time. For each symbol it removes that symbol's Gaussian factor, puts in the true discrete factor, computes the mean and variance of the result, and picks the new Gaussian factor that gives the same mean and variance. The first approximation is the linear MMSE estimate, and the next ones use the constellation. The detector of this page is the one of Céspedes, Olmos, Sánchez-Fernández and Pérez-Cruz (2014). The general method, for any model with factors, is on the [expectation propagation](/expectation-propagation/) page. This page gives the MIMO form, with the cavity and moment formulas for a PAM alphabet, the safeguards that the detector needs, and the results that are true for this model. [AMP detection](/amp-mimo-detection/) has a similar aim and costs less per step, but it needs a large channel with i.i.d. entries.

## In plain words

The receiver wants to know which symbol vector was sent. It can compute the best Gaussian guess, which is what the MMSE detector does. But the true symbols are not Gaussian: each one is one of a few points. EP corrects the Gaussian guess one symbol at a time. For symbol $i$, it asks what the rest of the system says about $x_i$. This is a Gaussian bump, the cavity. It then multiplies the bump by the true rule "$x_i$ is one of the points" and gets a small discrete distribution. It makes the Gaussian factor of symbol $i$ agree with the mean and the variance of that distribution. After a few rounds, the means of the Gaussian are usually much closer to the true symbols than the MMSE estimate.

## The problem

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$ known, $x \in \mathcal{S}^n$ for a square QAM constellation $\mathcal{S}$ of $M$ equally likely points with energy $E_s$, and $w \sim \mathcal{CN}(0, N_0 I)$. EP works on the real form $y_r = H_r x_r + w_r$ with

$$y_r = \begin{pmatrix} \mathrm{Re}\, y \\ \mathrm{Im}\, y \end{pmatrix}, \quad H_r = \begin{pmatrix} \mathrm{Re}\, H & -\mathrm{Im}\, H \\ \mathrm{Im}\, H & \mathrm{Re}\, H \end{pmatrix}, \quad x_r = \begin{pmatrix} \mathrm{Re}\, x \\ \mathrm{Im}\, x \end{pmatrix}.$$

Now $x_r$ has $d = 2n$ entries, each in the PAM alphabet $\mathcal{A}$ of $\sqrt M$ levels with energy $e_s = E_s/2$, and $w_r$ has i.i.d. $\mathcal{N}(0, \sigma^2)$ entries with $\sigma^2 = N_0/2$. For real symbols (BPSK or PAM), $x_r = x$ and $H_r = (\mathrm{Re}\, H; \mathrm{Im}\, H)$. The posterior is

$$p(x_r \mid y_r) \propto \exp\Big(-\frac{\|y_r - H_r x_r\|^2}{2\sigma^2}\Big) \prod_{i=1}^{d} \mathbb{1}[x_i \in \mathcal{A}].$$

The detector returns one decision in $\mathcal{S}$ for each stream and, for soft output, the mean and variance of each real symbol.

## The algorithm

EP replaces each factor $\mathbb{1}[x_i \in \mathcal{A}]$ by a Gaussian site $\exp(\gamma_i x_i - \Lambda_i x_i^2 / 2)$ with $\Lambda_i > 0$. The approximation is then the Gaussian $q(x_r) = \mathcal{N}(\mu, \Sigma)$ with

$$\Sigma = \big(\sigma^{-2} H_r^T H_r + \mathrm{diag}(\Lambda)\big)^{-1}, \qquad \mu = \Sigma \big(\sigma^{-2} H_r^T y_r + \gamma\big).$$

For a site $i$, the cavity is the marginal of $q$ divided by site $i$. It is $\mathcal{N}(t_i, h_i^2)$ with

$$h_i^2 = \frac{\Sigma_{ii}}{1 - \Sigma_{ii} \Lambda_i}, \qquad t_i = h_i^2 \Big(\frac{\mu_i}{\Sigma_{ii}} - \gamma_i\Big).$$

The tilted distribution puts the weight $\propto \exp(-(a - t_i)^2 / (2 h_i^2))$ on each $a \in \mathcal{A}$. Let $\mu_{p}$ and $\sigma_{p}^2$ be its mean and variance.

```pseudo id=main
EP-DETECT(y_r, H_r, A, σ², T, β, ε)
L1  γ ← 0;  Λ ← (1/e_s, ..., 1/e_s)
L2  for t ← 1 to T
L3      Σ ← (Hᵀ H / σ² + diag Λ)⁻¹;  μ ← Σ (Hᵀ y / σ² + γ)
L4      for each i: h²_i ← Σ_ii / (1 - Σ_ii Λ_i);  t_i ← h²_i (μ_i / Σ_ii - γ_i)
L5          (μ_p, σ²_p) ← mean and variance of the tilted distribution on A;  σ²_p ← max(σ²_p, ε)
L6          Λ' ← 1/σ²_p - 1/h²_i;  γ' ← μ_p/σ²_p - t_i/h²_i
L7          if Λ' > 0: Λ_i ← β Λ' + (1 - β) Λ_i;  γ_i ← β γ' + (1 - β) γ_i
L8  for each stream k: decide the level of A nearest to μ_k (and to μ_{n+k} for the imaginary part)
L9  return the decisions
```

Line L1 sets every site to the prior variance $e_s$ with mean 0, so the first $q$ is the linear MMSE estimate. Line L3 is one solve with a $d \times d$ symmetric positive definite matrix. Line L4 forms the cavity. Line L5 computes $\sqrt M$ weights per real symbol, with the largest exponent subtracted first so that nothing underflows. Line L6 gives the site that makes the marginal of $q$ have the tilted mean and variance. Line L7 keeps the old site when the new precision is not positive, and damps the update with a factor $\beta \in (0, 1]$. All sites in one iteration use the same $q$; this is a parallel schedule. The implementation uses $\beta = 0.7$, $\varepsilon = 10^{-9}$ and $T = 10$ by default. Céspedes et al. also use damping, a variance floor and a fixed small number of iterations; their exact values are not repeated here. Line L8 rounds each mean to the nearest level.

## Example

**A small channel, where EP corrects MMSE.** Take BPSK, $m = n = 2$,

$$H = \begin{pmatrix} 1 & 0.5 \\ 0.5 & 1 \end{pmatrix}, \qquad y = (0.2, 0.6), \qquad N_0 = 0.6.$$

The four metrics $\|y - H x\|^2$ are 2.5 for $(+1, +1)$, 1.3 for $(+1, -1)$, 0.5 for $(-1, +1)$ and 7.3 for $(-1, -1)$, so ML decides $(-1, +1)$. The real model has $\sigma^2 = 0.3$ and $e_s = 1$. With $H^T H = \begin{pmatrix} 1.25 & 1 \\ 1 & 1.25 \end{pmatrix}$ and $H^T y = (0.5, 0.7)$, line L3 gives

$$\Sigma = \frac{1}{15.583} \begin{pmatrix} 5.1667 & -3.3333 \\ -3.3333 & 5.1667 \end{pmatrix}, \qquad \mu = (0.0535, 0.4171).$$

This is the MMSE estimate, and its signs give $(+1, +1)$, which is wrong. Now take one EP iteration with $\beta = 1$. For BPSK the tilted mean is $\tanh(t_i / h_i^2)$ and the tilted variance is $1 - \tanh^2(t_i / h_i^2)$.

| site | $h_i^2$ | $t_i$ | $\mu_p$ | $\sigma_p^2$ | $\Lambda'$ | action |
|---|---|---|---|---|---|---|
| 1 | 0.4960 | 0.0800 | 0.1600 | 0.9744 | $-0.990$ | keep $\Lambda_1 = 1$, $\gamma_1 = 0$ |
| 2 | 0.4960 | 0.6240 | 0.8505 | 0.2766 | 1.599 | set $\Lambda_2 = 1.599$, $\gamma_2 = 1.817$ |

The new $q$ has $\mu = (-0.2261, 0.8505)$ and the variances $(0.3087, 0.2766)$. The site of symbol 1 did not change, but the stronger belief that $x_2 = +1$ pulls $\mu_1$ below 0 through the correlation of the columns. The decisions are $(-1, +1)$, the ML vector. More iterations do not change $q$, because site 2 already matches its tilted moments and the update of site 1 is still negative. The test checks the means and the variances of $q$ after 0 and 1 iterations within $10^{-4}$, and the decisions.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows the following, for every channel unless stated. First, the cavity formulas of line L4 are the marginal of $q$ divided by site $i$, and line L6 gives the site that makes the marginal of $q$ equal in mean and variance to the tilted distribution. Second, all $\Lambda_i$ stay positive, so $\Sigma$ always exists, and the cavity is a proper Gaussian when column $i$ of $H_r$ is not zero. Third, the first $q$ has the mean $(H^H H + (N_0/E_s) I)^{-1} H^H y$ in real form, the linear MMSE estimate. Fourth, at a fixed point where every site was kept, each marginal of $q$ has the mean and variance of its tilted distribution. Fifth, if $H^H H$ is diagonal and every update is kept, which is true when $\sigma^2 / \|h_i\|^2 > \max_a a^2$, the means and variances of $q$ converge to the exact posterior marginals. EP is not an exact ML detector in general, and it need not converge. Its good error rate on random channels is a measurement, not a theorem.

## Complexity

The Gram matrix $H_r^T H_r$ and the vector $H_r^T y_r$ cost $O(n^2 m)$ once. Each iteration inverts a $2n \times 2n$ matrix in $O(n^3)$ and computes $2n$ tilted moments of $\sqrt M$ terms each. So $T$ iterations cost $O(n^2 m + T(n^3 + n \sqrt M))$ in the [real RAM](/real-ram/), which the front matter bounds by $O(n^2 m + T(n^3 + n M))$. The space is $O(n^2 + n m)$. The cost is that of the [MMSE detector](/mmse-mimo-detector/) times $T$, and it grows only with $\sqrt M$ in the constellation size. A sphere search, by contrast, can grow fast with $M$ at low SNR. A rank-one update of $\Sigma$ after each site gives a sequential schedule at $O(n^2)$ per site, the same order per iteration.

## Properties

- **MMSE start.** The first iterate is the linear MMSE estimate (theorem). So EP with $T = 0$ is the MMSE detector without the bias correction.
- **Moment matching.** At a fixed point where all sites were kept, the mean and variance of each marginal of $q$ match the tilted distribution (theorem).
- **Exact on orthogonal channels.** When $H^H H$ is diagonal and the cavity variance is above $\max_a a^2$, EP gives the exact posterior marginals. The test checks this against a sum over all 256 vectors of 16-QAM with $n = 2$, within $10^{-6}$.
- **Measured agreement with ML.** For 4-QAM, $n = m = 4$, i.i.d. $\mathcal{CN}(0, 1/m)$ entries and $E_s/N_0 = 15$ dB, the test with seed 2204 runs 100 vectors, and EP with 10 iterations agrees with brute-force ML on 97 (measurement; the test asks for at least 92).
- **Measured gain over MMSE.** For 4-QAM, $n = m = 8$ and $E_s/N_0 = 10$ dB, EP made 19 symbol errors on 320 symbols and the MMSE start made 38 (seed 2206, measurement).
- **No guarantee.** On a strongly correlated channel EP can settle on a wrong vector, as Pitfalls shows.

## Variants and improvements

- **Sequential schedule.** Update one site at a time and change $\Sigma$ by a rank-one formula. The parallel schedule of this page is simpler; the sequential one often needs fewer iterations.
- **Soft output for coding.** The pairs $(t_i, h_i^2)$ of the cavity are extrinsic values for each real symbol. They feed a [soft demapper](/soft-demapping/) and a channel decoder, and the decoder output can come back as a new prior, as in [turbo equalization](/turbo-equalization/).
- **Complex form.** EP can also work with complex Gaussian sites on the complex model. For square QAM the real form is equivalent and simpler.
- **Lower cost for large systems.** For massive MIMO, later work looks for cheaper ways to compute or approximate $\Sigma$ than the $O(n^3)$ inverse. These change the cost and the accuracy, and this page does not cover them.
- **Other site families.** EP can use a full covariance per site or a mixture, at more cost.

## When to use it

Use EP when $n$ is moderate (up to a few tens of streams), the constellation is large (16-QAM to 256-QAM), and the channel may be correlated, so that AMP is not safe and a sphere search is too slow. It costs a small multiple of the [MMSE detector](/mmse-mimo-detector/) and is often much more accurate. For small $n$ with a low-order constellation, an exact search such as [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) or the [K-best detector](/k-best-detector/) is affordable and better. For very large i.i.d. systems, [AMP detection](/amp-mimo-detection/) avoids the inverse.

## Pitfalls

- **Negative site precision.** The update $\Lambda'$ can be negative, for example when the cavity sits between two points and the tilted distribution is wider than the cavity. Then $q$ may stop being a proper Gaussian. Keep the old site, as line L7 does.
- **Too small a tilted variance.** At high SNR the tilted variance can be 0 in floating point. Without the floor $\varepsilon$ the update divides by 0.
- **No damping.** Without damping the parallel schedule can oscillate. Choose $\beta < 1$, and check the choice by measurement on the channels of interest.
- **Strong correlation.** Take BPSK, $H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$, $y = (0.5, 0.6)$ and $N_0 = 0.25$. The columns have the correlation $3/\sqrt{10} = 0.949$. ML decides $(+1, -1)$ with metric 0.61, and the exact posterior means are $(0.9993, -0.9993)$. EP with $\beta = 1$ goes to $\mu = (-1, +1)$ and decides $(-1, +1)$, with metric 2.61. The test checks this case.
- **Wrong real form.** For real symbols (BPSK, PAM), do not add imaginary parts as unknowns: they are 0, and treating them as $\pm 1$ breaks the model. The implementation uses $H_r = (\mathrm{Re}\, H; \mathrm{Im}\, H)$ in that case.
- **Wrong noise variance.** The real model has $\sigma^2 = N_0 / 2$ per real dimension, and each real level has energy $E_s/2$. Mixing the complex and the real values gives the wrong first iterate.

## Implementations

## History

Minka (2001) introduced expectation propagation as a general method for approximate Bayesian inference, an extension of assumed-density filtering that can revisit each factor. It has been used for many models since. Céspedes, Olmos, Sánchez-Fernández and Pérez-Cruz (2014) applied EP to MIMO detection with high-order constellations, with the real-valued model, the rule for negative precisions and damping. They reported a large gain over MMSE at a complexity of the same cubic order. Later work extended EP detection to massive MIMO with lower-cost inverses and to iterative receivers with channel decoding.

## References
