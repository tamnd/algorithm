---
tag: 5G1W22
kind: problem
slug: smoothing
name: Smoothing
aliases:
- fixed-interval smoothing
- Bayesian smoothing
area: machine-learning/probabilistic-inference
level: core
summary: "Compute p(x_t | y_1..T), the distribution of a past hidden state of a state-space model given observations before and after it. Fixed-interval, fixed-lag and fixed-point."
history:
  year: 1965
  people: [Herbert E. Rauch, F. Tung, Charlotte T. Striebel]
  note: Rauch, Tung and Striebel gave the forward-backward smoother for linear Gaussian models. The forward-backward recursion for hidden Markov models came from Baum and his coworkers in the late 1960s.
prereqs: [filtering]
see_also: [filtering, rauch-tung-striebel-smoother, forward-backward-algorithm, viterbi-algorithm, particle-filter, expectation-maximization, state-space-model, baum-welch-algorithm]
sources:
  - book: isbn:9781107619289
    title: "Simo Särkkä, Bayesian Filtering and Smoothing, Cambridge University Press, 2013"
    locator: "Chapter 8 (the Bayesian smoothing equations and the RTS smoother), Chapter 9 (extended and unscented smoothers) and Chapter 11 (particle smoothing)"
  - book: isbn:9780387402642
    title: "Olivier Cappé, Eric Moulines and Tobias Rydén, Inference in Hidden Markov Models, Springer, 2005"
    locator: "Chapter 3 (forward-backward smoothing and the backward decomposition on general state spaces)"
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: "Section 13.2.2 (the forward-backward algorithm) and Section 13.3 (inference in linear dynamical systems)"
  - paper: doi:10.2514/3.3166
    title: "H. E. Rauch, F. Tung and C. T. Striebel, Maximum likelihood estimates of linear dynamic systems, AIAA Journal 3(8), 1965, pages 1445 to 1450"
    locator: the fixed-interval smoother for linear Gaussian models
  - paper: doi:10.1109/5.18626
    title: "L. R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286"
    locator: "Section III.A (the forward and backward procedures) and Section III.B (state posteriors)"
---

Smoothing is the problem of computing $p(x_t \mid y_1, \ldots, y_T)$ for a time $t$ in the past, $t < T$, in a [state-space model](/state-space-model/). Unlike [filtering](/filtering/), which uses only the observations up to time $t$, smoothing also uses the observations that came after $t$. So it can be done only with a delay or offline. It has three forms. Fixed-interval smoothing computes the posterior of every state $x_0, \ldots, x_T$ given a whole fixed record $y_{1:T}$. Fixed-lag smoothing reports the state $L$ steps back as each observation arrives. Fixed-point smoothing refines the estimate of one fixed state as more data comes in. The solvers are a filter followed by a backward pass: the [forward-backward algorithm](/forward-backward-algorithm/) for finite states, the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) for linear Gaussian models, and their extended, unscented and particle versions for the rest.

## In plain words

A filter tells you where something is now, using the readings you have so far. Smoothing looks back. Once you have the readings that came later, you can give a better answer about where the thing was at an earlier time.

Think of a ship's log. At noon the navigator wrote a guess of the position. At six in the evening the ship sights a lighthouse. Now the navigator knows where the ship is, and also, by going back along the course, where it must have been at noon. The noon estimate gets better and more certain. A smoother does this for every time in the log at once, with one pass forward and one pass back.

## Definition

**Input.** A [state-space model](/state-space-model/) with initial distribution $p(x_0)$, transition model $p(x_t \mid x_{t-1})$ and observation model $p(y_t \mid x_t)$, and observations $y_1, \ldots, y_T$.

**Output (fixed interval).** The marginals $p(x_t \mid y_{1:T})$ for $t = 0, \ldots, T$. Many uses also need the pairwise marginals $p(x_{t-1}, x_t \mid y_{1:T})$, for example the E-step of [expectation maximization](/expectation-maximization/), or samples from the joint posterior $p(x_{0:T} \mid y_{1:T})$.

**The backward recursion.** Run the filter to get $p(x_t \mid y_{1:t})$ and $p(x_{t+1} \mid y_{1:t})$ for all $t$. Then for $t = T-1$ down to $0$:

$$p(x_t \mid y_{1:T}) = p(x_t \mid y_{1:t}) \int \frac{p(x_{t+1} \mid x_t)\, p(x_{t+1} \mid y_{1:T})}{p(x_{t+1} \mid y_{1:t})}\, dx_{t+1}.$$

This holds because $x_t$ is independent of $y_{t+1:T}$ given $x_{t+1}$. It is the form behind the Rauch-Tung-Striebel smoother.

**The two-filter form.** Equivalently, with the backward likelihood $\beta_t(x_t) = p(y_{t+1:T} \mid x_t)$,

$$p(x_t \mid y_{1:T}) \propto p(x_t \mid y_{1:t})\, \beta_t(x_t), \qquad \beta_t(x_t) = \int p(x_{t+1} \mid x_t)\, p(y_{t+1} \mid x_{t+1})\, \beta_{t+1}(x_{t+1})\, dx_{t+1},$$

with $\beta_T \equiv 1$. This holds because $y_{t+1:T}$ is independent of $y_{1:t}$ given $x_t$. It is the form behind the forward-backward algorithm and the two-filter smoothers. The backward pass needs no filter output, so the two passes can run in parallel.

## Variants

- **Fixed-interval smoothing.** All of $p(x_t \mid y_{1:T})$, $t = 0, \ldots, T$, for one fixed record. This is the usual meaning of "smoothing" and the offline problem.
- **Fixed-lag smoothing.** At each time $t$, report $p(x_{t-L} \mid y_{1:t})$ for a fixed lag $L$. It is an online method with a delay of $L$ steps. When the model forgets its past quickly, a small $L$ gives almost the fixed-interval answer.
- **Fixed-point smoothing.** For one fixed time $j$, update $p(x_j \mid y_{1:t})$ for $t = j, j+1, \ldots$ as data arrives. An example is estimating an initial condition.
- **Joint smoothing.** The whole path $p(x_{0:T} \mid y_{1:T})$, through samples or a factored form. Sampling paths is called forward filtering backward sampling, and is a step of [Gibbs sampling](/gibbs-sampling/) for the parameters.
- **MAP path.** The single most likely path $\arg\max p(x_{0:T} \mid y_{1:T})$. This is a different question: the path of the most likely states can differ from the most likely path. For finite states it is solved by the [Viterbi algorithm](/viterbi-algorithm/).

## Examples

**A two-state model.** The state is $0$ or $1$, $P(x_0 = 1) = 1/4$, the state stays the same with probability $3/4$, the observation equals the state with probability $3/4$, and $y = (1, 0)$. The [filtering](/filtering/) page gives $P(x_1 = 1 \mid y_1) = 9/14$ and $P(x_2 = 1 \mid y_{1:2}) = 4/13$. The backward likelihoods at $t = 1$ are $\beta_1(1) = p(y_2 = 0 \mid x_1 = 1) = \frac34 \cdot \frac14 + \frac14 \cdot \frac34 = \frac38$ and $\beta_1(0) = \frac34 \cdot \frac34 + \frac14 \cdot \frac14 = \frac58$. So

$$P(x_1 = 1 \mid y_{1:2}) = \frac{\frac{9}{14} \cdot \frac38}{\frac{9}{14} \cdot \frac38 + \frac{5}{14} \cdot \frac58} = \frac{27}{52} \approx 0.519.$$

The later reading $y_2 = 0$ makes $x_1 = 1$ less likely than the filter said, $0.643$. For the first state, the fixed-point estimates of $P(x_0 = 1 \mid y_{1:t})$ are $1/4$, $5/14$ and $4/13$ for $t = 0, 1, 2$.

**A random walk with Gaussian noise.** Take $x_t = x_{t-1} + q_t$, $y_t = x_t + r_t$ with unit noise variances, $x_0 \sim \mathcal N(0, 1)$, and $y = (1, 2, 0)$. All three forms of smoothing give exact Gaussian answers. The table lists means, with variances in brackets.

| $t$ | filter, $y_{1:t}$ | fixed interval, $y_{1:3}$ | fixed lag $L = 1$, $y_{1:t+1}$ | fixed point $j = 1$ |
|---|---|---|---|---|
| 0 | 0 (1) | 3/7 (13/21) | 1/3 (2/3) | |
| 1 | 2/3 (2/3) | 6/7 (10/21) | 1 (1/2) | 2/3 (2/3) |
| 2 | 3/2 (5/8) | 8/7 (10/21) | 8/7 (10/21) | 1 (1/2) |
| 3 | 4/7 (13/21) | 4/7 (13/21) | | 6/7 (10/21) |

The fixed-point column follows the estimate of $x_1$ as $y_1$, $y_2$ and $y_3$ arrive. The fixed-lag value at $t = 2$ equals the fixed-interval value because both use $y_{1:3}$. The fixed-interval variance is never larger than the filter variance, and the two agree at $t = T$. The [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) page works through the fixed-interval column step by step.

## Known algorithms

| model class | solver | what it computes | time |
|---|---|---|---|
| finite states (HMM) | [forward-backward algorithm](/forward-backward-algorithm/) | exact marginals and pairwise marginals | $O(TK^2)$ |
| linear Gaussian | [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) | exact means and covariances | $O(T n^3)$ |
| linear Gaussian | two-filter smoother (Fraser and Potter) | exact, with a backward information filter | $O(T n^3)$ |
| nonlinear, Gaussian noise | extended and unscented RTS smoothers | Gaussian fits | $O(T n^3)$ plus model calls |
| any model | forward filtering backward smoothing with particles | Monte Carlo marginals | $O(T N^2)$ |
| any model | forward filtering backward simulation | Monte Carlo paths | $O(T N^2)$ for $N$ paths |
| any model | genealogy of a [particle filter](/particle-filter/) | Monte Carlo paths | $O(T N)$, but degenerate for early $t$ |

The RTS cost assumes the observation dimension $m$ is at most of order $n$. Fixed-lag and fixed-point smoothers for linear Gaussian models can be built by adding the lagged or fixed state to the state vector and running a Kalman filter on the larger model.

## Bounds

**Time and memory for finite states.** The forward-backward algorithm takes $O(TK^2)$ time and stores $O(TK)$ numbers. When memory is short, checkpointing keeps only some of the forward messages and recomputes the others: $O(K\sqrt T)$ memory with about twice the time, or $O(K \log T)$ memory with $O(TK^2 \log T)$ time (Binder, Murphy and Russell, 1997).

**Smoothing never hurts on average.** By the law of total variance, $\mathbb E[\mathrm{Var}(x_t \mid y_{1:T})] \le \mathbb E[\mathrm{Var}(x_t \mid y_{1:t})]$, so the mean squared error of the smoothed mean is at most that of the filtered mean. In a linear Gaussian model the covariances do not depend on the data, and $P_{t \mid T} \preceq P_{t \mid t}$ holds for every record. In nonlinear models the inequality holds on average but can fail for a single record.

**Particle path degeneracy.** A particle filter that keeps the ancestral path of each particle gives an estimate of the joint smoothing distribution for free. But [resampling](/resampling/) makes the paths merge: after enough steps all $N$ particles share one ancestor at early times, so the estimate of $p(x_t \mid y_{1:T})$ for $t \ll T$ rests on very few distinct values. Backward smoothing passes avoid this at a cost of order $N^2$ per step.

## Reductions

- **Smoothing is two message passes.** On the chain graph of the model, smoothing is [belief propagation](/belief-propagation/) with one forward and one backward sweep. The marginal at $t$ is the product of the forward message (the [filter](/filtering/)) and the backward message $\beta_t$.
- **Linear Gaussian smoothing is a banded linear solve.** The posterior of $(x_0, \ldots, x_T)$ is Gaussian with a block tridiagonal precision matrix. The smoothed means solve one block tridiagonal linear system, and the RTS smoother is block [Gaussian elimination](/gaussian-elimination/) on it.
- **Learning reduces to smoothing.** The E-step of [expectation maximization](/expectation-maximization/) needs the smoothed marginals and pairwise marginals: the [Baum-Welch algorithm](/baum-welch-algorithm/) uses the forward-backward algorithm, and EM for a linear dynamical system uses the RTS smoother (Shumway and Stoffer, 1982).
- **Gaussian process regression in time.** For a [Gaussian process](/gaussian-process/) with a covariance that has a state space form, such as a Matérn covariance of half-integer order, the posterior at the inputs is a Kalman smoother output. This brings the cost from $O(T^3)$ to $O(T)$.

## Applications

- **Offline trajectory estimation.** Reconstruct the path of a vehicle, an aircraft or a satellite after the fact, from all the logged measurements.
- **Learning model parameters.** The E-step of EM for hidden Markov models in speech and biology, and for linear dynamical systems in econometrics and neuroscience.
- **Signal processing.** Denoise a recorded signal, for example trend extraction in time series, where the Hodrick-Prescott filter is a Kalman smoother for a particular model.
- **Labeling of sequences.** Posterior state probabilities in HMMs, such as the chance that a DNA position lies in a gene, use smoothing rather than the single Viterbi path.
- **Reanalysis in weather science.** Past states of the atmosphere are recomputed with the data from after each time, which is smoothing with very large models.

## References
