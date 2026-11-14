---
tag: KJZYAX
kind: algorithm
slug: bayesian-online-changepoint-detection
name: Bayesian online change-point detection
aliases:
- BOCPD
- Adams-MacKay algorithm
area: statistics-and-inference/time-series-and-sequential-analysis
level: research
summary: Adams and MacKay's recursion for the posterior of the run length since the last change, from a hazard rate and a conjugate model for each segment.
solves: [change-point-detection]
model: real-ram
complexity:
  vars: {n: "the number of observations read, with O(1) work per conjugate update; step t costs Θ(t)"}
  time: {worst: Θ(n²)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2007
  people: [Ryan P. Adams, David J. C. MacKay]
  note: Adams and MacKay published the run-length recursion in 2007. Fearnhead and Liu gave an equivalent online filter for the time of the last change in the same year, with resampling to bound the cost.
prereqs: [change-point-detection, conjugate-prior, bayes-theorem]
see_also: [cusum, pelt-algorithm, binary-segmentation, hidden-markov-model, forward-algorithm, particle-filter, kalman-filter, sequential-monte-carlo]
sources:
  - paper: arxiv:0710.3742
    title: Ryan Prescott Adams and David J. C. MacKay, Bayesian online changepoint detection, arXiv preprint 0710.3742 (2007)
    locator: the run-length model with a hazard function, the recursion for the joint of the run length and the data, and the conjugate exponential family updates
  - paper: doi:10.1111/j.1467-9868.2007.00601.x
    title: Paul Fearnhead and Zhen Liu, On-line inference for multiple changepoint problems, Journal of the Royal Statistical Society Series B 69(4) (2007)
    locator: the online recursion for the time of the most recent change point and the resampling step that bounds the number of stored values
  - paper: doi:10.1016/j.sigpro.2019.107299
    title: Charles Truong, Laurent Oudre and Nicolas Vayatis, Selective review of offline change point detection methods, Signal Processing 167 (2020)
    locator: the parts on the Bayesian formulation and on the comparison of online and offline methods
---

Bayesian online change-point detection keeps, after each new observation, the posterior distribution of the run length $r_t$: the number of observations since the last change, the new one included. The model is a renewal process: a segment that has lasted $r$ points ends with probability $H(r)$, the hazard, and each segment draws a new parameter from a prior. With a [conjugate prior](/conjugate-prior/), the predictive density of the next point given the last $r$ points costs $O(1)$, and the posterior at time $t$ follows from the one at time $t - 1$ by one growth step and one change step. Each step costs $O(t)$ time and memory, or $O(1)$ when small posterior values are dropped. A sharp rise of $P(r_t = 1)$, or a fall of the most probable run length, signals a change.

## In plain words

At each moment you ask: how long ago did the current regime start? You keep a probability for every possible answer. When a new value arrives, every answer either grows by one, if the regime goes on, or resets to "it started just now", if a new regime begins. You compare how well the new value fits each regime. If it fits the old regime well, the long answers keep their weight. If it fits only a fresh start, the weight moves to the short answer. The probability of each answer is updated with the rules of chance, so you also get a measure of how sure you are.

## The problem

Observations $x_1, x_2, \ldots$ arrive one at a time. The model is:

1. **Segments.** The series is cut into segments by a renewal process. A segment that has run for $r$ points ends after its $r$-th point with probability $H(r)$. The first segment starts at $t = 1$. A constant hazard $H(r) = 1/\lambda$ gives geometric segment lengths with mean $\lambda$.
2. **Parameters.** Each segment has its own parameter $\theta$, drawn from a prior $\pi$, independently of the other segments and of the segmentation.
3. **Data.** Given the segments and their parameters, the points are independent, and a point of a segment with parameter $\theta$ has density $p(x \mid \theta)$.

The run length $r_t \in \{1, \ldots, t\}$ is the number of points of the current segment up to and including $x_t$. The task is to compute $P(r_t = r \mid x_{1..t})$ for each $t$ as $x_t$ arrives, and the evidence $p(x_{1..t})$. The predictive density of a point given the $r$ points before it in its segment is
$$\pi_t^{(r)} = p(x_t \mid x_{t-r..t-1}) = \int p(x_t \mid \theta)\,\pi(\theta \mid x_{t-r..t-1})\,d\theta,$$
and $\pi_t^{(0)} = \int p(x_t \mid \theta)\,\pi(\theta)\,d\theta$. See [change-point detection](/change-point-detection/) for the other formulations.

## The algorithm

```pseudo id=main
BOCPD(x_1, x_2, ..., H, prior)
L1  P ← empty map; stats ← empty map; Z_all ← 1           ▷ P(r) = P(r_{t-1} = r | x_{1..t-1})
L2  for t ← 1, 2, ... as x_t arrives do
L3      π(r) ← predictive of x_t from stats(r), for each r in P; π_0 ← predictive of x_t from the prior
L4      J(r + 1) ← P(r) π(r) (1 - H(r)), for each r in P          ▷ the segment goes on
L5      J(1) ← π_0 Σ_r P(r) H(r), and J(1) ← π_0 when t = 1       ▷ a new segment starts at x_t
L6      stats(r + 1) ← update(stats(r), x_t) for each r in P; stats(1) ← update(empty, x_t)
L7      Z ← Σ_r J(r); Z_all ← Z_all · Z; P ← J / Z               ▷ P(r) = P(r_t = r | x_{1..t})
L8  return the posteriors P after each step and the evidence Z_all
```

Line L3 uses the sufficient statistics of the last $r$ points, so it costs $O(1)$ per run length for a conjugate model. For a normal mean with known variance $\sigma^2$ and prior $N(\mu_0, \sigma_0^2)$, the statistics are the count $r$ and the sum $S$, and the predictive is normal with precision-weighted mean $(\mu_0/\sigma_0^2 + S/\sigma^2)/(1/\sigma_0^2 + r/\sigma^2)$ and variance $1/(1/\sigma_0^2 + r/\sigma^2) + \sigma^2$. Lines L4 and L5 are the growth and change steps. Line L7 normalizes and keeps the evidence $p(x_{1..t}) = \prod_s Z_s$.

## Example

Let $\sigma = 1$, the prior be $N(0, 3^2)$, the hazard $H = 1/10$, and the data $0.2, -0.5, 0.4, 3.9, 4.3, 3.6$. The run-length posteriors, rounded to 4 decimals, are:

| $t$ | $x_t$ | $r = 1$ | $r = 2$ | $r = 3$ | $r = 4$ | $r = 5$ | $r = 6$ | most probable $r$ |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.2 | 1 | | | | | | 1 |
| 2 | $-0.5$ | 0.0513 | 0.9487 | | | | | 2 |
| 3 | 0.4 | 0.0451 | 0.0398 | 0.9151 | | | | 3 |
| 4 | 3.9 | **0.7985** | 0.0588 | 0.0081 | 0.1347 | | | 1 |
| 5 | 4.3 | 0.0270 | **0.9533** | 0.0165 | 0.0004 | 0.0027 | | 2 |
| 6 | 3.6 | 0.0226 | 0.0237 | **0.9394** | 0.0136 | 0.0001 | 0.0006 | 3 |

At $t = 4$ the predictive density of $3.9$ under the old segment, after 3 points with sum 0.1, is about 0.0012. Under a fresh segment it is about 0.059, because the prior is wide. Weighted by the hazard, the change step wins, and $P(r_4 = 1) \approx 0.80$. After that the run length grows again from the change at $t = 4$. The most probable run lengths $1, 2, 3, 1, 2, 3$ give one change point, before $x_4$. The evidence is $p(x_{1..6}) \approx 3.39 \times 10^{-6}$.

## Correctness

The recursion is exact for the model. The proof is in full below. In outline, let $J_t(r) = p(r_t = r, x_{1..t})$.

1. **The run length is a Markov chain.** Given $r_{t-1} = r$, the next run length is $1$ with probability $H(r)$ and $r + 1$ with probability $1 - H(r)$, whatever the earlier data. This holds because the end of a segment is decided by the renewal process, which is independent of the parameters and of the data given the segmentation.
2. **The predictive depends only on the current segment.** Given the whole segmentation up to $t$, $x_t$ is independent of all points outside the current segment, because the parameters of different segments are independent. So $p(x_t \mid x_{1..t-1}, r_t = r) = \pi_t^{(r-1)}$.
3. **The recursion.** By the chain rule and facts 1 and 2,
$$J_t(r + 1) = J_{t-1}(r)\,(1 - H(r))\,\pi_t^{(r)}, \qquad J_t(1) = \pi_t^{(0)}\sum_r J_{t-1}(r)\,H(r),$$
with $J_1(1) = \pi_1^{(0)}$. Dividing by $p(x_{1..t-1})$ gives lines L4 and L5, the normalizer of line L7 is $p(x_t \mid x_{1..t-1})$, and the product of the normalizers is the evidence by [Bayes' theorem](/bayes-theorem/).

## Complexity

At time $t$ there are $t$ run lengths, so lines L3 to L7 cost $\Theta(t)$ time with $O(1)$ conjugate updates, and $\Theta(n^2)$ for $n$ observations. The memory is $\Theta(t)$: one probability and one set of sufficient statistics per run length. Dropping run lengths whose posterior is below a small threshold, or keeping only a fixed number of them, makes each step $O(1)$ at the price of an approximation.

## Properties

- **Exact Bayesian filter.** Without pruning, the posteriors are exact for the model, including the uncertainty about the change times.
- **A hidden Markov model.** The run length is the hidden state of a [hidden Markov model](/hidden-markov-model/) whose state space grows with $t$, and the recursion is its [forward algorithm](/forward-algorithm/).
- **Evidence for free.** The product of normalizers is the marginal likelihood, so the hazard and the prior can be tuned or compared by evidence.
- **Unknown parameters handled.** Unlike the [CUSUM](/cusum/), it needs no known pre-change or post-change density, only a prior.
- **Model dependent.** The answer is only as good as the segment model and the hazard. Outliers under a light-tailed model look like changes.

## Variants and improvements

- **Pruning and resampling.** Fearnhead and Liu (2007) keep a bounded number of values with a resampling step from [particle filtering](/particle-filter/), so the cost of each step stays bounded and the error is controlled. The simplest form drops run lengths with small posterior probability.
- **Hazard learning.** A hazard with unknown parameters can be learned from the evidence, or by placing a prior on it.
- **Non-conjugate models.** When no conjugate prior exists, the predictive can be approximated per run length by [sequential Monte Carlo](/sequential-monte-carlo/) or by Gaussian approximations; linear Gaussian state-space segments use a [Kalman filter](/kalman-filter/) per run length.
- **Robust segments.** Student-t or mixture likelihoods reduce false alarms from outliers.
- **Offline exact segmentation.** When the whole series is available and only a point estimate is wanted, [PELT](/pelt-algorithm/) gives the penalized optimum.

## When to use it

Use BOCPD for streams where the parameters of each regime are unknown, changes may be many, and a probability of a change is more useful than a yes or no answer, for example in monitoring of sensors or of financial series. Use the CUSUM when the pre-change and post-change densities are known and a guaranteed false alarm rate matters, and an offline method when the whole series is at hand.

## Pitfalls

- **Run-length convention.** Some texts let $r_t = 0$ mean that a change happened at $t$, so their $r_t$ is one smaller. Mixing the two shifts all change estimates by one.
- **Underflow.** The joint probabilities and the evidence shrink geometrically. Normalize at each step, as in line L7, and keep the log evidence.
- **Prior too wide or too narrow.** A very wide prior makes the predictive under a fresh segment small, so changes are found late. A very narrow prior makes every point look like a change.
- **Reading the most probable run length as a decision.** The posterior can split its mass, as at $t = 4$ in the example. Use a decision rule, such as $P(r_t \le w) > 1/2$ for a small window $w$, and state it.
- **Unbounded cost.** Without pruning, the cost grows with $t$, so a long stream needs pruning or resampling.

## Implementations

## History

Adams and MacKay (2007) published the run-length recursion with a hazard function and conjugate exponential family models. In the same year, Fearnhead and Liu (2007) gave an online filter for the time of the most recent change point, which is the same quantity, and added resampling to bound the cost. Both build on earlier Bayesian work on the exact posterior of multiple change points in offline data.

## References
