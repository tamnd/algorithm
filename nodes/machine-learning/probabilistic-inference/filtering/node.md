---
tag: HFAHM5
kind: problem
slug: filtering
name: Filtering
aliases:
- Bayesian filtering
- online state estimation
area: machine-learning/probabilistic-inference
level: core
summary: "Compute p(x_t | y_1..t), the distribution of the current hidden state of a state-space model given the observations so far, and update it at each new observation."
history:
  year: 1960
  people: [Rudolf E. Kalman, Ruslan L. Stratonovich]
  note: Kalman gave the exact recursive filter for linear Gaussian models in 1960. Stratonovich and, for continuous time, Kushner wrote the general nonlinear filtering equations around the same years.
prereqs: [state-space-model, bayes-theorem]
see_also: [smoothing, kalman-filter, forward-algorithm, particle-filter, extended-kalman-filter, unscented-kalman-filter, sequential-monte-carlo, online-algorithm]
sources:
  - book: isbn:9781107619289
    title: "Simo Särkkä, Bayesian Filtering and Smoothing, Cambridge University Press, 2013"
    locator: "Chapter 4 (the Bayesian filtering equations and the Kalman filter), Chapters 5 and 6 (Gaussian approximations) and Chapter 7 (particle filtering)"
  - book: isbn:9780387402642
    title: "Olivier Cappé, Eric Moulines and Tobias Rydén, Inference in Hidden Markov Models, Springer, 2005"
    locator: "Chapter 3 (filtering and smoothing recursions on general state spaces)"
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: "Section 13.2 (the forward recursion for hidden Markov models) and Section 13.3 (the Kalman filter for linear dynamical systems)"
  - paper: doi:10.1115/1.3662552
    title: "R. E. Kalman, A new approach to linear filtering and prediction problems, Journal of Basic Engineering 82(1), 1960, pages 35 to 45"
    locator: the recursive solution of the linear filtering problem
  - paper: doi:10.1109/5.18626
    title: "L. R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286"
    locator: "Section III.A (the forward procedure)"
---

Filtering is the problem of computing $p(x_t \mid y_1, \ldots, y_t)$, the distribution of the hidden state $x_t$ of a [state-space model](/state-space-model/) given all observations up to and including time $t$. The answer must be updated each time a new observation arrives, without a pass over the old data. Every exact or approximate solution uses the same two-step recursion: predict the state forward with the dynamics, then correct it with the new observation by [Bayes' theorem](/bayes-theorem/). This recursion is called the Bayes filter. The solver depends on the model class: the [forward algorithm](/forward-algorithm/) for finite states, the [Kalman filter](/kalman-filter/) for linear Gaussian models, and approximations such as the [extended Kalman filter](/extended-kalman-filter/), the [unscented Kalman filter](/unscented-kalman-filter/) and the [particle filter](/particle-filter/) for the rest. The offline version of the question, which uses later data too, is [smoothing](/smoothing/).

## In plain words

Something moves, and you cannot see it directly. You get a noisy reading of it now and then. After each reading you want your best guess of where it is right now, together with how sure you are.

You do this in two moves. First you guess where it went since the last reading, using what you know about how it moves. Your guess gets less sure here. Then you look at the new reading and shift your guess toward it. How far you shift depends on how much you trust the reading compared with your guess. Your guess gets more sure here. You keep only the current guess and throw the old readings away, so each step costs the same, however long you have been tracking.

## Definition

**Input.** A [state-space model](/state-space-model/): an initial distribution $p(x_0)$, a transition model $p(x_t \mid x_{t-1})$, and an observation model $p(y_t \mid x_t)$. A stream of observations $y_1, y_2, \ldots$ that arrive one at a time.

**Output.** At each time $t$, the filtering distribution $p(x_t \mid y_{1:t})$, or a summary of it such as its mean and covariance, or the expectation of a given function under it. Most solvers also give the one-step predictive density $p(y_t \mid y_{1:t-1})$, whose product over $t$ is the likelihood $p(y_{1:T})$.

**The Bayes filter.** Start from $p(x_0 \mid y_{1:0}) = p(x_0)$. For $t = 1, 2, \ldots$:

$$\text{predict:}\quad p(x_t \mid y_{1:t-1}) = \int p(x_t \mid x_{t-1})\, p(x_{t-1} \mid y_{1:t-1})\, dx_{t-1},$$

$$\text{update:}\quad p(x_t \mid y_{1:t}) = \frac{p(y_t \mid x_t)\, p(x_t \mid y_{1:t-1})}{p(y_t \mid y_{1:t-1})}, \qquad p(y_t \mid y_{1:t-1}) = \int p(y_t \mid x_t)\, p(x_t \mid y_{1:t-1})\, dx_t.$$

For a finite state space the integrals are sums. The predict step uses that $x_t$ is independent of $y_{1:t-1}$ given $x_{t-1}$. The update step is Bayes' theorem with $p(x_t \mid y_{1:t-1})$ as the prior, and uses that $y_t$ is independent of $y_{1:t-1}$ given $x_t$. Both facts are the [conditional independence](/conditional-independence/) properties of the model.

**What makes it hard.** The recursion is exact, but each step needs an integral over the state space and a representation of a whole distribution. Only a few model classes keep the filtering distribution inside a family with a fixed number of parameters. For the others the problem is to approximate the recursion with bounded cost per step and controlled error.

## Variants

- **Prediction.** Compute $p(x_{t+k} \mid y_{1:t})$ for $k \ge 1$: run the predict step $k$ times with no update.
- **Likelihood evaluation.** Compute $p(y_{1:T}) = \prod_t p(y_t \mid y_{1:t-1})$. The filter computes the factors along the way. This is the [HMM evaluation](/hmm-evaluation/) problem in the discrete case and the prediction error decomposition of the likelihood in time series analysis.
- **Point estimation.** Report only the posterior mean, which minimizes the expected squared error, or the posterior mode.
- **Continuous time.** The state follows a stochastic differential equation and the observations arrive continuously or at discrete times. The filtering density then solves the Kushner-Stratonovich equation, or the Zakai equation in unnormalized form.
- **Filtering with unknown parameters.** The parameters $\theta$ are unknown and are estimated online, by adding them to the state or by running a separate learning step.

## Examples

**A two-state model.** The state is $0$ or $1$, with $P(x_0 = 1) = 1/4$. It stays the same with probability $3/4$. The observation equals the state with probability $3/4$. The observations are $y = (1, 0)$.

| step | $P(x_t = 1)$ | $p(y_t \mid y_{1:t-1})$ |
|---|---|---|
| prior, $t = 0$ | $1/4$ | |
| predict $t = 1$ | $\frac14 \cdot \frac34 + \frac34 \cdot \frac14 = 3/8$ | |
| update with $y_1 = 1$ | $\dfrac{\frac38 \cdot \frac34}{\frac38 \cdot \frac34 + \frac58 \cdot \frac14} = 9/14$ | $7/16$ |
| predict $t = 2$ | $\frac{9}{14} \cdot \frac34 + \frac{5}{14} \cdot \frac14 = 4/7$ | |
| update with $y_2 = 0$ | $\dfrac{\frac47 \cdot \frac14}{\frac47 \cdot \frac14 + \frac37 \cdot \frac34} = 4/13$ | $13/28$ |

The likelihood is $p(y_1, y_2) = \frac{7}{16} \cdot \frac{13}{28} = \frac{13}{64}$. The predict step pulls the probability toward $1/2$ because the state can switch. The update step pushes it toward the value that was seen.

**A random walk with Gaussian noise.** Take $x_t = x_{t-1} + q_t$ and $y_t = x_t + r_t$ with unit noise variances, $x_0 \sim \mathcal N(0, 1)$, and $y = (1, 2, 0)$. The filtering distribution stays Gaussian, so the Kalman filter tracks a mean $m_t$ and a variance $P_t$. The predicted variance is $P_{t-1} + 1$, the gain is $K_t = (P_{t-1} + 1)/(P_{t-1} + 2)$, and $m_t = m_{t-1} + K_t (y_t - m_{t-1})$.

| $t$ | $y_t$ | predicted variance | gain $K_t$ | $m_t$ | $P_t$ |
|---|---|---|---|---|---|
| 0 | | | | 0 | 1 |
| 1 | 1 | 2 | 2/3 | 2/3 | 2/3 |
| 2 | 2 | 5/3 | 5/8 | 3/2 | 5/8 |
| 3 | 0 | 13/8 | 13/21 | 4/7 | 13/21 |

The gain falls toward its steady value $(\sqrt5 - 1)/2 \approx 0.618$, where the variance stops changing.

## Known algorithms

| model class | solver | what it computes | cost per step |
|---|---|---|---|
| finite states (HMM) | [forward algorithm](/forward-algorithm/) | exact | $O(K^2)$ |
| linear Gaussian | [Kalman filter](/kalman-filter/) | exact | $O(n^3 + m^3)$ |
| nonlinear, Gaussian noise | [extended Kalman filter](/extended-kalman-filter/) | Gaussian fit by linearization | $O(n^3 + m^3)$ plus Jacobians |
| nonlinear, Gaussian noise | [unscented Kalman filter](/unscented-kalman-filter/) | Gaussian fit by sigma points | $O(n^3 + m^3)$ plus $2n + 1$ model calls |
| any model that can be simulated | [particle filter](/particle-filter/) | Monte Carlo, error $O(1/\sqrt N)$ | $O(N)$ model calls |
| any model, any proposal | [sequential Monte Carlo](/sequential-monte-carlo/) | Monte Carlo with [resampling](/resampling/) | $O(N)$ model calls |
| a DBN with many variables | factored filters, such as the Boyen-Koller method | approximate | depends on the structure |

Here $K$ is the number of states, $n$ and $m$ are the state and observation dimensions, and $N$ is the number of particles. Other solvers include grid filters, which apply the forward algorithm to a discretized state space, Gaussian sum filters, the ensemble Kalman filter used in weather forecasting, and the information filter, which runs the Kalman recursion on the inverse covariance.

## Bounds

**Cost of exact filtering.** The forward algorithm costs $O(K^2)$ per step with a dense transition matrix. Each step is a vector-matrix product, so for a general dense matrix the cost is the cost of that product. Sparse or structured transitions make it cheaper. The Kalman filter costs $O(n^3 + m^3)$ per step for dense matrices. For a time-invariant model whose filter covariance converges, the steady-state filter fixes the gain in advance and costs $O(n^2 + nm)$ per step.

**No finite summary in general.** Exact filters with a fixed number of parameters exist only for special models: finite state spaces, linear Gaussian models, and a few nonlinear families such as the Beneš filter. In general the filtering density has no finite-dimensional sufficient statistic, so an exact solver would have to store a whole function.

**Optimality.** The posterior mean $\mathbb E[x_t \mid y_{1:t}]$ has the least mean squared error among all estimators of $x_t$ that use $y_{1:t}$. The Kalman filter mean has the least mean squared error among all estimators that are linear in $y_{1:t}$, whatever the noise distribution, provided the noise has the assumed means and covariances (Kalman, 1960). For nonlinear models the posterior Cramér-Rao bound of Tichavský, Muravchik and Nehorai (1998) gives a recursive lower bound on the mean squared error of any filter.

**Monte Carlo error.** For a bounded test function $\varphi$, the particle filter estimate of $\mathbb E[\varphi(x_t) \mid y_{1:t}]$ has mean squared error at most $c_t \lVert \varphi \rVert_\infty^2 / N$. The constant $c_t$ can grow with $t$. Under strong mixing conditions on the dynamics it is bounded uniformly in $t$, so the filter does not lose accuracy over time (Del Moral, 2004).

## Reductions

- **Filtering is a forward message pass.** On the chain graph of the model, the filtering distribution is the forward message of [belief propagation](/belief-propagation/), or equally the result of [variable elimination](/variable-elimination/) of $x_0, \ldots, x_{t-1}$ in time order.
- **Smoothing uses filtering.** The [smoothing](/smoothing/) algorithms run a filter first and then a backward pass that corrects each filtered distribution with later data.
- **Likelihood and learning use filtering.** The likelihood $p(y_{1:T})$ is a by-product of the filter, so maximum likelihood fitting and model comparison call the filter as a subroutine. The E-step of [expectation maximization](/expectation-maximization/) needs smoothing, and so it calls the filter too.
- **Filtering as recursive least squares.** For a linear Gaussian model with a constant state, $x_t = x_{t-1}$, the Kalman filter is recursive least squares for [linear regression](/linear-regression/).
- **Approximate filtering as sequential importance sampling.** The particle filter is [importance sampling](/importance-sampling/) on the growing path space, with [resampling](/resampling/) to keep the weights balanced.

## Applications

- **Navigation and tracking.** Position and velocity from radar, GPS and inertial sensors. The Kalman filter and the EKF have been used in aircraft and spacecraft navigation since the 1960s.
- **Robotics.** Robot localization from odometry and range sensors, often with particle filters (Monte Carlo localization).
- **Speech and sequence labeling.** The forward recursion of hidden Markov models gives online state probabilities and the likelihood used to compare models.
- **Weather and ocean forecasting.** Data assimilation updates the state of a large numerical model with new measurements, mostly with ensemble Kalman filters and variational methods.
- **Economics and finance.** Estimation of hidden quantities such as trend, volatility or the output gap, and the likelihood of ARMA and other time series models in state space form.

## References
