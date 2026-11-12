---
tag: X3E38Q
kind: algorithm
slug: expectation-maximization
name: Expectation-maximization algorithm
aliases:
- EM algorithm
- Dempster-Laird-Rubin EM
- expectation maximization
area: machine-learning/probabilistic-inference
level: core
summary: "Fit a latent variable model by maximum likelihood: alternate the posterior of the hidden data (E step) and a complete-data fit (M step). The likelihood never decreases."
model: real-ram
complexity:
  vars: {t: the number of iterations, c: the cost of one E step plus one M step, s: the size of the expected sufficient statistics}
  time: {worst: "O(t c)"}
  space: {extra: "O(s)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1977
  people: [Arthur Dempster, Nan Laird, Donald Rubin]
  note: Dempster, Laird and Rubin named the EM algorithm and gave its general form in 1977. Wu (1983) corrected their convergence proof.
prereqs: [maximum-likelihood-estimation, jensens-inequality, bayes-theorem]
see_also: [gaussian-mixture-model, baum-welch-algorithm, hidden-markov-model, k-means, evidence-lower-bound, variational-inference, latent-dirichlet-allocation, factor-analysis]
sources:
  - paper: "A. P. Dempster, N. M. Laird and D. B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society, Series B 39(1):1-38, 1977"
    title: Dempster, Laird and Rubin 1977
    locator: "Section 1 (the genetic linkage example, with the iterates in Table 1), Section 2 (the definition of EM and GEM for exponential families and in general), Section 3 (monotonicity and the rate of convergence)"
  - paper: "C. F. Jeff Wu, On the convergence properties of the EM algorithm, Annals of Statistics 11(1):95-103, 1983"
    title: Wu 1983
    locator: "the error in the convergence proof of Dempster, Laird and Rubin, and the conditions under which the limit points of EM are stationary points and the likelihood values converge"
  - paper: "R. A. Boyles, On the convergence of the EM algorithm, Journal of the Royal Statistical Society, Series B 45(1):47-50, 1983"
    title: Boyles 1983
    locator: a GEM sequence whose likelihood values converge while the iterates do not converge to a point
  - paper: "Radford M. Neal and Geoffrey E. Hinton, A view of the EM algorithm that justifies incremental, sparse, and other variants, in M. I. Jordan (ed.), Learning in Graphical Models, Kluwer, 1998"
    title: Neal and Hinton 1998
    locator: EM as coordinate ascent on the free energy F(q, theta), and the incremental variant
  - paper: "Chuong B. Do and Serafim Batzoglou, What is the expectation maximization algorithm?, Nature Biotechnology 26(8):897-899, 2008"
    title: Do and Batzoglou 2008
    locator: "Figure 1 (the two coin example: five sets of ten tosses, start 0.60 and 0.50, about 0.80 and 0.52 after ten iterations)"
  - book: isbn:9780471201700
    title: Geoffrey J. McLachlan and Thriyambakam Krishnan, The EM Algorithm and Extensions, second edition, Wiley, 2008
    locator: "Chapter 1 (examples, including the genetic linkage data) and Chapter 3 (monotonicity, convergence to stationary points, the rate of convergence)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 9.3 (an alternative view of EM) and Section 9.4 (the EM algorithm in general, the decomposition of the log likelihood into a lower bound and a KL divergence)"
---

The expectation-maximization (EM) algorithm fits the parameters $\theta$ of a model with hidden variables $z$ by [maximum likelihood](/maximum-likelihood-estimation/). It alternates two steps: the E step computes the posterior of the hidden variables under the current $\theta$, and the M step chooses the $\theta$ that maximizes the expected complete-data log likelihood under that posterior. Each iteration never decreases the log likelihood of the observed data, and under mild conditions the iterates go to a stationary point, which can be a local maximum or a saddle point, not always the global maximum. The [Gaussian mixture model](/gaussian-mixture-model/) and the [Baum-Welch algorithm](/baum-welch-algorithm/) are its best known cases.

## In plain words

Some data have a missing part. If you knew the missing part, the fit would be easy: you would count and average. If you knew the right parameters, you could guess the missing part well. EM does both in turns.

It starts from some guess of the parameters. Then it fills in the missing part, not with one value, but with the chance of each value under the guess. This is the E step. Then it fits the parameters as if the filled-in data were real, with each possible value counted by its chance. This is the M step. Then it repeats.

Each round makes the model explain the seen data at least as well as before. It stops when the gain is tiny. It can stop at a point that is good only nearby, so people run it from several starts.

## The problem

A model gives a joint density or mass function $p(x, z \mid \theta)$ of the observed data $x$ and the hidden data $z$, for $\theta$ in a set $\Theta$. Only $x$ is seen. The task is to find a $\theta$ with a large log likelihood

$$\ell(\theta) = \log p(x \mid \theta) = \log \sum_{z} p(x, z \mid \theta),$$

with an integral in place of the sum for a continuous $z$. The sum inside the logarithm couples the parameters, so a closed form maximizer is rare even when the *complete-data* log likelihood $\log p(x, z \mid \theta)$ is easy to maximize. For i.i.d. data $x_1, \ldots, x_n$ with hidden $z_1, \ldots, z_n$, both $\ell$ and the steps below are sums over the $n$ examples.

## The algorithm

Define the expected complete-data log likelihood

$$Q(\theta \mid \theta') = \mathbb{E}_{z \sim p(z \mid x, \theta')} \big[\log p(x, z \mid \theta)\big] = \sum_z p(z \mid x, \theta') \log p(x, z \mid \theta).$$

```pseudo id=main
EM(x, θ⁽⁰⁾, ε)
L1  t ← 0; record ℓ(θ⁽⁰⁾)
L2  repeat
L3      E step: compute q_t(z) = p(z | x, θ⁽ᵗ⁾), or the expected sufficient statistics under it
L4      M step: θ⁽ᵗ⁺¹⁾ ← argmax over θ ∈ Θ of Q(θ | θ⁽ᵗ⁾)
L5      t ← t + 1; record ℓ(θ⁽ᵗ⁾)
L6  until ℓ(θ⁽ᵗ⁾) − ℓ(θ⁽ᵗ⁻¹⁾) < ε
L7  return θ⁽ᵗ⁾
```

When the complete-data model is an [exponential family](/exponential-family-distribution/) with sufficient statistic $T(x, z)$, the E step only needs $\mathbb{E}[T(x, z) \mid x, \theta^{(t)}]$, and the M step is the complete-data maximum likelihood fit with $T$ replaced by this expectation (Dempster, Laird and Rubin, Section 2). A *generalized EM* (GEM) step only requires $Q(\theta^{(t+1)} \mid \theta^{(t)}) \ge Q(\theta^{(t)} \mid \theta^{(t)})$, not a maximum.

### The free energy view

For any distribution $q$ over $z$, define $F(q, \theta) = \mathbb{E}_q[\log p(x, z \mid \theta)] + H(q)$, where $H$ is the entropy. Then

$$\ell(\theta) = F(q, \theta) + \mathrm{KL}\big(q \,\|\, p(z \mid x, \theta)\big) \ge F(q, \theta).$$

So $F$ is a lower bound on $\ell$, the [evidence lower bound](/evidence-lower-bound/). The E step maximizes $F$ over $q$ by setting $q = p(z \mid x, \theta^{(t)})$, which makes the KL term 0 and the bound tight. The M step maximizes $F$ over $\theta$; the entropy does not depend on $\theta$, so this is the maximization of $Q$. EM is coordinate ascent on $F$ (Neal and Hinton 1998). [Variational inference](/variational-inference/) keeps the same $F$ but restricts $q$ to a family where the E step is tractable.

## Example

The [Gaussian mixture model](/gaussian-mixture-model/) page shows EM on a mixture of Gaussians. Here are two other cases.

### Genetic linkage (Dempster, Laird and Rubin, Section 1)

Of 197 animals, the counts in four classes are $y = (125, 18, 20, 34)$, with the multinomial cell probabilities

$$\Big(\tfrac12 + \tfrac{\theta}{4},\; \tfrac{1 - \theta}{4},\; \tfrac{1 - \theta}{4},\; \tfrac{\theta}{4}\Big), \qquad 0 < \theta < 1.$$

Treat the first cell as two hidden cells with the probabilities $\frac12$ and $\frac{\theta}{4}$, with counts $x_1 + x_2 = 125$. The complete data are then binomial in $\theta$: the counts $x_2 + 34$ go with $\theta$ and $18 + 20$ with $1 - \theta$. So

- E step: $x_2^{(t)} = 125 \cdot \dfrac{\theta^{(t)}/4}{1/2 + \theta^{(t)}/4}$,
- M step: $\theta^{(t+1)} = \dfrac{x_2^{(t)} + 34}{x_2^{(t)} + 18 + 20 + 34}$.

From $\theta^{(0)} = 0.5$, with $\ell$ written without the multinomial constant:

| $t$ | $\theta^{(t)}$ | $x_2^{(t)}$ | $\ell(\theta^{(t)})$ |
|---|---|---|---|
| 0 | 0.500000 | 25.0000 | $-208.470245$ |
| 1 | 0.608247 | 29.1502 | $-205.779819$ |
| 2 | 0.624321 | 29.7373 | $-205.717064$ |
| 3 | 0.626489 | 29.8159 | $-205.715908$ |
| 4 | 0.626777 | 29.8263 | $-205.715887$ |
| 5 | 0.626816 | 29.8277 | $-205.715887$ |

Setting $\ell'(\theta) = \frac{125}{2 + \theta} - \frac{38}{1 - \theta} + \frac{34}{\theta}$ to 0 gives $197 \theta^2 - 15 \theta - 68 = 0$, so the maximum is $\hat\theta = (15 + \sqrt{53809}) / 394 \approx 0.626821$. A grid search with step $10^{-5}$ on $(0, 1)$ finds its maximum at $0.62682$. The error $\theta^{(t)} - \hat\theta$ shrinks by a factor that tends to about $0.1328$ in each step: the convergence is linear.

### Two coins (Do and Batzoglou 2008)

Two coins $A$ and $B$ have the unknown head probabilities $\theta_A$ and $\theta_B$. Five times, a coin is picked at random with probability $\frac12$ each, and tossed ten times. The numbers of heads are $5, 9, 8, 4, 7$, and the coin is not recorded. The E step computes, for each set $i$ with $h_i$ heads, the responsibility $r_i = P(A \mid h_i) = \theta_A^{h_i}(1 - \theta_A)^{10 - h_i} / \big(\theta_A^{h_i}(1 - \theta_A)^{10 - h_i} + \theta_B^{h_i}(1 - \theta_B)^{10 - h_i}\big)$. The M step sets $\theta_A = \sum_i r_i h_i / \sum_i 10\, r_i$, and $\theta_B$ the same with $1 - r_i$.

From $(\theta_A, \theta_B) = (0.6, 0.5)$, the first E step gives $r = (0.449, 0.805, 0.733, 0.352, 0.647)$, and the first M step gives $(0.713, 0.581)$. After ten iterations the values are $(0.797, 0.520)$, and EM stops at $(0.7968, 0.5196)$ with $\ell \approx -31.5702$ (without the binomial coefficients).

## Correctness

**Monotonicity (Dempster, Laird and Rubin, Section 3).** For every $t$, $\ell(\theta^{(t+1)}) \ge \ell(\theta^{(t)})$. With the free energy: $\ell(\theta^{(t+1)}) \ge F(q_t, \theta^{(t+1)}) \ge F(q_t, \theta^{(t)}) = \ell(\theta^{(t)})$. The first step is the lower bound, the second is the M step, and the last is the tight bound after the E step. The same chain holds for a GEM step. So if $\ell$ is bounded above on $\Theta$, the values $\ell(\theta^{(t)})$ converge.

**Fixed points are stationary.** The gradient of $Q(\cdot \mid \theta')$ at $\theta = \theta'$ equals $\nabla \ell(\theta')$. So if $\theta^{(t+1)} = \theta^{(t)}$ is an interior point where $Q$ is differentiable, then $\nabla \ell(\theta^{(t)}) = 0$.

**Convergence of the iterates.** The convergence of the values does not by itself give the convergence of $\theta^{(t)}$. Wu (1983) showed that the convergence proof of Dempster, Laird and Rubin contains an error, and Boyles (1983) gave a GEM sequence whose iterates do not converge to a point. Wu proved the correct statement: if the set $\{\theta \in \Theta : \ell(\theta) \ge \ell(\theta^{(0)})\}$ is compact, $\ell$ is continuous there and differentiable in the interior of $\Theta$, the iterates stay in the interior, and $Q(\theta \mid \theta')$ is continuous in both arguments, then every limit point of the EM sequence is a stationary point of $\ell$, and $\ell(\theta^{(t)})$ converges monotonically to $\ell(\theta^\ast)$ for some stationary point $\theta^\ast$. With further conditions, for example a unique stationary point at that level, the iterates themselves converge. A stationary point can be a local maximum, a saddle point, or in principle a local minimum. The proofs of monotonicity and of the fixed-point statement are in the proofs file.

## Complexity

- **Per iteration.** The cost $c$ of an iteration is the cost of the E step plus the M step, and it depends on the model. For i.i.d. examples the E step is a sum over the $n$ examples of a posterior over each $z_i$: $O(n k)$ for $k$ discrete hidden values and a cheap likelihood, $O(n k d^2)$ for a Gaussian mixture with full covariances, and $O(T k^2)$ per sequence of length $T$ with the [forward-backward algorithm](/forward-backward-algorithm/) for an HMM with $k$ states. The M step is a complete-data fit, often in closed form. In the linkage example each step is $O(1)$.
- **Number of iterations.** Near a local maximum $\hat\theta$, EM converges linearly. The rate is the largest eigenvalue of the *fraction of missing information* $I_c(\hat\theta)^{-1} I_m(\hat\theta)$, the ratio of the information lost by hiding $z$ to the complete-data information (Dempster, Laird and Rubin, Section 3). In the linkage example this rate is about $0.1328$, so each iteration adds almost one decimal digit. When the hidden data carry most of the information, the rate is close to 1 and EM is slow.
- **Memory.** One set of expected sufficient statistics, for example the $n \times k$ responsibilities of a mixture.

There is no general bound on $t$: EM is a local method with no guarantee of reaching a global maximum.

## Properties

- **Monotone.** The log likelihood never decreases, with no step size to tune.
- **Stays in $\Theta$.** The M step returns a valid parameter (probabilities in $[0, 1]$, positive semidefinite covariances when the data allow) with no projection.
- **Local.** It finds a stationary point that depends on the start.
- **Linear convergence.** It is slower near the optimum than Newton's method, but each step is cheap and stable.
- **Deterministic.** Given the start and the data, the run is fixed.

## Variants and improvements

- **Generalized EM.** Any increase of $Q$ in the M step keeps monotonicity. Expectation conditional maximization replaces the M step with several conditional maximizations, each over a block of $\theta$.
- **Incremental EM.** Update the posterior of one example at a time and the parameters after each update, which is still coordinate ascent on $F$ (Neal and Hinton 1998).
- **Stochastic and Monte Carlo EM.** Replace the expectation of the E step with an average over samples of $z$, for example from [Gibbs sampling](/gibbs-sampling/), when the posterior is intractable.
- **Variational EM.** Restrict $q$ to a tractable family and maximize $F$ over it, as in [latent Dirichlet allocation](/latent-dirichlet-allocation/) and the [mean field approximation](/mean-field-approximation/).
- **Hard EM.** Replace the posterior with its most likely value. On a Gaussian mixture with equal spherical covariances this is [k-means](/k-means/); on an HMM it is Viterbi training.
- **MAP estimation.** Add $\log p(\theta)$ to $Q$ in the M step. The same proof shows that the log posterior never decreases.

## When to use it

Use EM when the complete-data maximum likelihood problem is easy, for example a closed form fit of an [exponential family](/exponential-family-distribution/), and the posterior of the hidden variables is tractable: mixtures, [hidden Markov models](/hidden-markov-model/), [factor analysis](/factor-analysis/), [probabilistic PCA](/probabilistic-pca/), and data with values missing at random. When the posterior is intractable, use its variational or Monte Carlo variants. When fast local convergence matters, switch to a quasi-Newton method near the optimum.

## Pitfalls

- **Saddle points and local maxima.** In the two coin example, a start with $\theta_A = \theta_B$ gives $r_i = \frac12$ for all sets, and the M step gives both coins the pooled frequency $33/50 = 0.66$. EM stays at $(0.66, 0.66)$ forever. This is a stationary point with $\ell \approx -32.0518$, below the $-31.5702$ found from $(0.6, 0.5)$. The Hessian of $\ell$ there has the eigenvalues about $-111.4$ along $(1, 1)$ and $+59.4$ along $(1, -1)$, so it is a saddle point. Break the symmetry, and use several starts.
- **An unbounded likelihood.** A Gaussian mixture has no global maximum: a component can collapse onto one point. See the [Gaussian mixture model](/gaussian-mixture-model/) page for the remedies.
- **Stopping too early.** A small change of $\ell$ in one step does not mean a small distance to the optimum when the rate is near 1. Check the change of $\theta$ as well, or use an acceleration.
- **The wrong posterior.** The E step must use the posterior under the current $\theta^{(t)}$. A posterior from an older $\theta$ breaks the tight bound and the monotonicity.
- **Underflow.** Compute the posteriors and $\ell$ in log space with the log-sum-exp trick.
- **Label switching.** In a mixture, permuting the components gives the same likelihood, so two runs can return the same fit with other labels.

## Implementations

## History

Special cases of EM were in use before 1977, for example in the [Baum-Welch algorithm](/baum-welch-algorithm/) for hidden Markov models. Dempster, Laird and Rubin (1977) gave the general form, the name, the proof of monotonicity, and the rate of convergence, with the genetic linkage data as a first example. Their proof that the iterates converge has an error. Wu (1983) and Boyles (1983) pointed it out, and Wu gave the correct conditions for convergence to a stationary point. Neal and Hinton (1998) described EM as coordinate ascent on a free energy, which led to the incremental and variational variants. Do and Batzoglou (2008) wrote a short primer around the two coin example.

## References
