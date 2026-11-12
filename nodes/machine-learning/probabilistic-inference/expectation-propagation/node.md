---
tag: 6W6NCV
kind: algorithm
slug: expectation-propagation
name: Expectation propagation
aliases:
- EP
- expectation propagation for approximate Bayesian inference
area: machine-learning/probabilistic-inference
level: research
summary: "Approximates each factor of a posterior by an exponential family site, refined one at a time by moment matching against the true factor times the rest. Mass covering; no convergence guarantee."
solves: [marginal-inference, partition-function-computation]
model: real-ram
complexity:
  vars: {s: the number of sweeps, N: the number of sites, c: the cost of the moments of one tilted distribution, p: the number of parameters of one site}
  time: {worst: "O(s N (c + p))"}
  space: {extra: "O(N p)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Thomas P. Minka]
  note: "Minka (UAI 2001 and his MIT thesis) turned assumed-density filtering into an iterative method that revisits each factor, and showed that loopy belief propagation is a special case."
prereqs: [exponential-family-distribution, bayesian-inference, factor-graph]
see_also: [loopy-belief-propagation, variational-inference, evidence-lower-bound, bethe-free-energy, gaussian-process, kalman-filter, shannon-entropy, cross-entropy-loss]
sources:
  - paper: "Thomas P. Minka, Expectation propagation for approximate Bayesian inference, Proceedings of the 17th Conference on Uncertainty in Artificial Intelligence (UAI), 2001"
    title: Minka 2001 (UAI)
    locator: "assumed-density filtering, the iterative refinement of the site approximations, the clutter problem, and loopy belief propagation as a special case"
  - paper: "Thomas P. Minka, A family of algorithms for approximate Bayesian inference, PhD thesis, Massachusetts Institute of Technology, 2001"
    title: Minka 2001 (thesis)
    locator: "expectation propagation in full, its fixed points and energy function, and its experiments"
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: "Section 10.7 (expectation propagation, with the clutter problem as the example)"
---

Expectation propagation (EP) approximates a distribution that is a product of factors, typically a posterior $p(\theta \mid x) \propto p_0(\theta) \prod_n t_n(\theta)$, by a member $q$ of an [exponential family](/exponential-family-distribution/). Each factor $t_n$ gets an approximate *site* $\tilde t_n$ from the same family, and $q \propto p_0 \prod_n \tilde t_n$. To refine one site, EP removes it from $q$ to get the *cavity*, multiplies the cavity by the true factor to get the *tilted* distribution, and replaces $q$ by the member of the family with the same expected sufficient statistics (moments) as the tilted distribution. The new site is the new $q$ divided by the cavity. Moment matching minimizes $\mathrm{KL}(\text{tilted} \,\|\, q)$, the reverse of the divergence of [variational inference](/variational-inference/), so EP tends to cover all the mass of the target rather than lock onto one mode. It was introduced by Minka. It has no guarantee of convergence.

## In plain words

A posterior is often a product of many simple pieces, one per observation, but the product is too complicated to work with. EP replaces each piece by a simple bell-shaped stand-in, so that the product of the stand-ins is easy.

To improve one stand-in, EP takes the current overall answer and removes that stand-in. It puts the true piece back in its place and asks: what simple bell curve has the same center and the same spread as this mix? That bell curve becomes the new overall answer, and the stand-in is changed to match. EP goes through all pieces again and again until nothing changes. Because it matches center and spread, the answer tends to spread out over everything the true posterior covers. It can also fail to settle.

## The problem

**The target.** $p(\theta) \propto p_0(\theta) \prod_{n=1}^N t_n(\theta)$, where $p_0$ is in an exponential family with sufficient statistics $T(\theta)$ and the $t_n$ are arbitrary positive factors, such as likelihood terms. We want its moments, typically the mean and covariance, and its normalizer $Z$.

**The approximating family.** $q(\theta) \propto p_0(\theta) \prod_n \tilde t_n(\theta)$ with each $\tilde t_n(\theta) = \exp(\lambda_n^\top T(\theta))$ unnormalized in the same family. Products and quotients of such sites are additions and subtractions of natural parameters.

**The local projection.** For a density $\hat p$, the member of the family that minimizes $\mathrm{KL}(\hat p \,\|\, q)$ is the one with $\mathbb{E}_q[T] = \mathbb{E}_{\hat p}[T]$. For Gaussians, that is the same mean and covariance. The [Kullback-Leibler divergence](/evidence-lower-bound/) is the expected value of a log ratio; $\mathrm{KL}(\hat p \| q)$ is the [cross-entropy](/cross-entropy-loss/) of $q$ under $\hat p$ minus the [entropy](/shannon-entropy/) of $\hat p$.

**The clutter problem (Minka).** A one-dimensional $\theta$ with prior $\mathcal{N}(0, b)$, and observations that are either signal or clutter: $x_n \sim (1 - w)\mathcal{N}(\theta, 1) + w\, \mathcal{N}(0, a)$. With $w = 0.5$, $a = 10$ and $b = 100$, as in the implementation, the posterior is a product of $N$ two-part mixtures in $\theta$, which has up to $2^N$ terms.

## The algorithm

```pseudo id=main
EP(p_0, t_1..t_N, ε)
L1  every site t̃_n ← 1 (zero natural parameters); q ← p_0
L2  repeat (one sweep)
L3      for each n: cavity q_\n ← q / t̃_n; if q_\n is not a proper density, skip n
L4          compute Z_n and the moments of the tilted distribution p̂_n ∝ t_n q_\n
L5          q ← the member of the family with those moments (the projection minimizing KL(p̂_n || q))
L6          t̃_n ← q / q_\n
L7      until no site changed by more than ε
L8  return q (and the sites)
```

For the clutter problem with $q = \mathcal{N}(m, v)$ and a cavity $\mathcal{N}(m_c, v_c)$, the tilted distribution is a mixture of two Gaussians, and with $d = x_n - m_c$ its moments are

$$Z_n = (1 - w)\mathcal{N}(x_n; m_c, v_c + 1) + w \mathcal{N}(x_n; 0, a), \qquad r_n = \frac{(1 - w)\mathcal{N}(x_n; m_c, v_c + 1)}{Z_n},$$

$$m = m_c + \frac{r_n v_c d}{v_c + 1}, \qquad v = v_c - \frac{r_n v_c^2}{v_c + 1} + \frac{r_n (1 - r_n) v_c^2 d^2}{(v_c + 1)^2}.$$

Here $r_n$ is the probability, under the tilted distribution, that $x_n$ is signal. The site update in natural parameters is $1/v_n^{\mathrm{site}} = 1/v - 1/v_c$ and $m_n^{\mathrm{site}} / v_n^{\mathrm{site}} = m/v - m_c/v_c$; site precisions can be negative, and that is allowed as long as $q$ and the cavities stay proper.

## Example

Draw 20 points from the clutter model with $\theta = 2$, $w = 0.5$, $a = 10$ (seed 0):

$$x = (2.052, -3.300, 0.553, 3.113, -5.983, 0.907, 0.160, -4.386, 3.812, 1.803, -0.855, -0.123, 2.722, 2.631, 3.114, 1.763, 1.352, -3.753, 0.498, 3.108).$$

EP, starting from all sites equal to 1, converges in 13 sweeps (largest change of a site parameter below $10^{-10}$) to $q = \mathcal{N}(2.0146, 0.2561)$. The posterior moments, from the trapezoid rule on $[-20, 20]$ with 40000 steps, are mean $2.0145$ and variance $0.2503$.

On four seeded data sets of this kind on which EP converged, its mean was within $10^{-3}$ of the integrated posterior mean and its variance within $10\%$ of the integrated variance; in three of the four, the EP variance was the larger one.

On one more seeded data set (seed 1), with clutter on both sides of the signal, the posterior is wide and has several bumps (variance $2.87$). There, EP did not converge in 3000 sweeps, without damping or with damping $0.5$, $0.8$ or $0.9$, and many updates were skipped because the cavity had a negative precision.

## Correctness

- **Each step is a KL projection.** Among Gaussians, the one with the mean and variance of the tilted distribution minimizes $\mathrm{KL}(\hat p_n \| q)$. In the clutter problem, the tilted moments above are exact.
- **Gaussian factors are exact.** If every $t_n$ is itself in the family ($w = 0$ in the clutter problem), each site equals its factor after one visit, and $q$ is the exact posterior after one sweep.
- **Fixed points.** At a fixed point, $q$ has the moments of every tilted distribution $t_n q_{\setminus n}$ at once. Minka related these fixed points to the stationary points of an approximate free energy of Bethe type.
- **No convergence guarantee.** The iteration can cycle or reach improper cavities, as in the example. Double-loop methods that minimize the EP free energy directly do converge.
- **Loopy BP is a special case.** For discrete variables and a fully factorized family, EP on a factor graph sends the messages of [loopy belief propagation](/loopy-belief-propagation/) (Minka 2001).

The proofs of the first three points are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model.

- **One site update.** The tilted moments cost $c$ and the cavity and site arithmetic cost $O(p)$. In the clutter problem both are $O(1)$. For a $d$-dimensional Gaussian $q$ with sites that depend on $\theta$ through one projection, as in [Gaussian process](/gaussian-process/) classification, a rank-one update costs $O(d^2)$.
- **One sweep.** $O(N(c + p))$.
- **Sweeps.** Not bounded. In the example, 13.
- **Memory.** $O(N p)$ for the sites. Assumed-density filtering, a single pass without revisiting, needs only $q$.

## Properties

- **Mass covering.** Moment matching minimizes $\mathrm{KL}(\hat p \| q)$ locally, which is large if $q$ is small where $\hat p$ has mass. So $q$ spreads over all the mass, unlike the mode-seeking $\mathrm{KL}(q \| p)$ of [variational inference](/variational-inference/).
- **Not a bound.** The EP estimate of $\log Z$ is neither a lower nor an upper bound in general, unlike the [ELBO](/evidence-lower-bound/).
- **Often accurate.** In problems with a single-peaked posterior, such as Gaussian process classification, EP means and variances are often very close to the true ones.
- **Order matters.** The fixed point does not depend on the order of the sites, but the path, and whether it converges, can.
- **Deterministic.** No random sampling.

## Variants and improvements

- **Assumed-density filtering (ADF).** One pass, each factor used once; the result depends on the order. EP is ADF made iterative.
- **Damping.** Update the site natural parameters only part of the way; this helps in many cases, though it did not in the example.
- **Power EP and $\alpha$-divergences.** Use a fraction of the factor in the tilted distribution, which interpolates between EP and variational inference (Minka).
- **Double-loop and convergent EP.** Minimize the EP free energy directly, with guaranteed convergence at a higher cost.
- **Stochastic and distributed EP.** Share one site among many factors, or split the data among workers, to save memory for large $N$.

## When to use it

Use EP for a posterior with many non-Gaussian factors that is roughly single-peaked, where accurate means and variances matter, such as Gaussian process classification, probit regression and skill rating. Prefer variational inference when you need a guaranteed bound, a guaranteed convergence, or when the posterior has well-separated modes. For a factor graph with discrete variables and a fully factorized $q$, EP is loopy belief propagation.

## Pitfalls

- **Improper cavities.** A site precision can be so large that the cavity precision is negative. Skip the update, damp it, or restart.
- **No convergence on multimodal posteriors.** As in the example, EP can fail when the posterior has several separated bumps.
- **Tilted moments without a closed form.** They must be computed by quadrature or sampling, and errors there can break convergence.
- **Reading the $\log Z$ estimate as a bound.** It is not one.
- **Expecting the variational answer.** EP and variational inference minimize different divergences and give different answers; EP is wider.

## Implementations

## History

Assumed-density filtering, which keeps a simple approximation and projects after each new factor, has a long history in control and statistics. Opper and Winther developed related iterative methods for Gaussian processes. Minka (UAI 2001 and his MIT thesis, 2001) made the projection iterative: each factor gets its own site that is refined again and again against all the others. He named the result expectation propagation, showed that loopy belief propagation is a special case, and used the clutter problem as a running example. EP became a standard method for Gaussian process classification and for the TrueSkill rating system.

## References
