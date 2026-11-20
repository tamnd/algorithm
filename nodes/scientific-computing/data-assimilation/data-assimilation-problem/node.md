---
tag: 15TTYD
kind: problem
slug: data-assimilation-problem
name: Data assimilation problem
aliases:
- data assimilation
area: scientific-computing/data-assimilation
level: intro
summary: "Estimate the state of a large dynamical system, such as the atmosphere, from a forecast model and sparse noisy observations over time."
model: real-ram
prereqs: [state-space-model, bayes-theorem]
see_also: [filtering, smoothing, kalman-filter, bayesian-inverse-problem, observation-operator, background-error-covariance, lorenz-96-model, observing-system-simulation-experiment]
sources:
  - book: isbn:9780521796293
    title: Eugenia Kalnay, Atmospheric Modeling, Data Assimilation and Predictability, Cambridge University Press, 2003
    locator: Chapter 5 (data assimilation)
  - book: isbn:9783319203249
    title: K. Law, A. Stuart and K. Zygalakis, Data Assimilation, A Mathematical Introduction, Springer, 2015
    locator: Chapter 2 (the smoothing problem in Section 2.3 and the filtering problem in Section 2.4)
  - book: isbn:9781611974539
    title: M. Asch, M. Bocquet and M. Nodet, Data Assimilation, Methods, Algorithms, and Applications, SIAM, 2016
    locator: Chapter 1 (introduction to data assimilation and inverse problems)
  - book: isbn:9783642037108
    title: Geir Evensen, Data Assimilation, The Ensemble Kalman Filter, second edition, Springer, 2009
    locator: the formulation of the problem as Bayesian estimation
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

The data assimilation problem asks for the state of a dynamical system, such as the atmosphere or the ocean, given a model of its evolution, a prior estimate of its initial state, and a stream of observations that are noisy, indirect and far too few to fix the state on their own. The model fills the gaps between observations in space and time, and the observations correct the drift of the model. In probabilistic form the answer is the distribution of the state given all observations so far (filtering) or over a whole time window (smoothing). In practice the state has $10^7$ to $10^9$ components, so every operational method computes an approximation: a point estimate with an error covariance that is modeled, sampled by an ensemble, or never formed. Weather prediction centers solve this problem several times a day to start their forecasts.

## In plain words

A weather model can predict tomorrow from today, but only if it knows today exactly, and nobody does. There are measurements from stations, balloons, aircraft and satellites, but they cover only a small part of the atmosphere, they have errors, and many of them measure something other than what the model uses, such as the radiation that reaches a satellite. Data assimilation combines the last forecast with the new measurements to get the best picture of the present. It weighs each source by how much it can be trusted. The result starts the next forecast, which is then combined with the next measurements, and so on, in a cycle.

## Definition

**Notation.** We use the notation of Ide, Courtier, Ghil and Lorenc (1997). The state at time $t_k$ is $x_k \in \mathbb R^n$, and $p_k$ is the number of observations at that time. In the letters of the [Kalman filter](/kalman-filter/) page, $M_k$ is its $A$, $H_k$ is its $C$, the forecast $x^f_k, P^f_k$ is its predicted value, and the analysis $x^a_k, P^a_k$ is its filtered value.

**Input.**

- A model $x_k = M_k(x_{k-1}) + \eta_k$, with model errors $\eta_k$ of covariance $Q_k$ ($Q_k = 0$ for a perfect model).
- Observations $y^o_k = H_k(x_k) + \varepsilon^o_k$ at times $k = 1, \ldots, K$, with an [observation operator](/observation-operator/) $H_k : \mathbb R^n \to \mathbb R^{p_k}$ and observation errors $\varepsilon^o_k$ of covariance $R_k$.
- A prior for the initial state, usually a background $x^b$ with the [background error covariance](/background-error-covariance/) $B$, so $x_0 \sim \mathcal N(x^b, B)$ in the Gaussian case.
- The errors $x_0 - x^b$, $\eta_k$ and $\varepsilon^o_k$ are independent of each other.

**Output.** One of the following, for the posterior distribution given by [Bayes' theorem](/bayes-theorem/):

- *Filtering.* The distribution $p(x_k \mid y^o_1, \ldots, y^o_k)$ at each time $k$, or its mean $x^a_k$ and covariance $P^a_k$.
- *Smoothing.* The distribution $p(x_0, \ldots, x_K \mid y^o_1, \ldots, y^o_K)$ of the whole trajectory, or its mode.

**The cycle.** The filtering solution is a recursion of two steps. The *forecast step* pushes the analysis distribution at time $k - 1$ through the model to get the forecast distribution at time $k$. The *analysis step* combines the forecast with $y^o_k$ by Bayes' theorem, $p(x_k \mid y^o_{1:k}) \propto p(y^o_k \mid x_k)\,p(x_k \mid y^o_{1:k-1})$. The innovation $d_k = y^o_k - H_k(x^f_k)$ measures the new information.

## Variants

- **Linear Gaussian.** $M_k$ and $H_k$ are linear and all errors are Gaussian. Then all distributions are Gaussian and the [Kalman filter](/kalman-filter/) and the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) solve the problem exactly.
- **One analysis time (three-dimensional).** Only the analysis step, with the forecast as the background: find $x^a$ from $x^b$, $B$, $y^o$ and $R$. This is a Bayesian [inverse problem](/bayesian-inverse-problem/).
- **Strong constraint (perfect model).** $Q_k = 0$, so the trajectory is fixed by $x_0$, and smoothing is an estimate of $x_0$ alone. This is the problem of strong constraint [4D-Var](/four-dimensional-variational-assimilation/).
- **Weak constraint.** $Q_k \ne 0$, and the model errors are unknowns too, as in [weak constraint 4D-Var](/weak-constraint-4d-var/).
- **Parameter estimation.** Unknown model parameters are added to the state and estimated with it.
- **Point estimate or distribution.** Some methods return a single estimate, the posterior mode or mean, and others return a sample of the posterior, as ensemble methods do.

## Examples

**One scalar analysis.** The prior is $x \sim \mathcal N(0, 1)$, and one observation $y^o = 1$ of $x$ has the error variance $R = 1$. The posterior is $\mathcal N(1/2, 1/2)$: the analysis is halfway between background and observation, and its variance is half of each.

**A scalar cycle.** The model is a random walk $x_k = x_{k-1} + \eta_k$ with $Q = 1$, the prior is $x_0 \sim \mathcal N(0, 1)$, and $x_k$ is observed with $R = 1$. With $y^o_1 = 1$ and $y^o_2 = 0$:

| $k$ | forecast mean | forecast variance | gain | observation | analysis mean | analysis variance |
|---|---|---|---|---|---|---|
| 1 | 0 | 2 | 2/3 | 1 | 2/3 | 2/3 |
| 2 | 2/3 | 5/3 | 5/8 | 0 | 1/4 | 5/8 |

Each forecast step adds the model error variance, and each analysis step reduces the variance by the factor $1 - \text{gain}$.

**A twin experiment.** A truth run of the [Lorenz-96 model](/lorenz-96-model/) with 40 variables is observed every 0.05 time units with errors of standard deviation 1. A method is judged by the root mean square error of its analysis against the truth after a spin-up. An error well below 1 means that the model has carried information between observations. This is the standard test of new methods (see [observing system simulation experiment](/observing-system-simulation-experiment/)).

**Weather prediction.** A global center has a state of about $10^9$ numbers and assimilates of the order of $10^7$ observations per day, most of them satellite radiances whose observation operator is a radiative transfer model. These figures are rough orders of magnitude, not exact values.

## Known algorithms

- [Kalman filter](/kalman-filter/): exact for the linear Gaussian case, $\Theta(n^3)$ per step with dense matrices.
- [Extended Kalman filter](/extended-kalman-filter/) and [unscented Kalman filter](/unscented-kalman-filter/): linearize or sample the nonlinear model for small $n$.
- [Optimal interpolation](/optimal-interpolation/): the analysis step with a fixed $B$ and local selection of observations.
- [3D-Var](/three-dimensional-variational-assimilation/): the analysis step as the minimization of a cost function.
- [4D-Var](/four-dimensional-variational-assimilation/) and [incremental 4D-Var](/incremental-4d-var/): the strong constraint smoothing problem over a time window, with the gradient from an [adjoint model](/adjoint-model/).
- [Ensemble Kalman filter](/ensemble-kalman-filter/) and the [ensemble Kalman smoother](/ensemble-kalman-smoother/): Monte Carlo estimates of the covariances from tens to hundreds of model runs.
- [Hybrid ensemble-variational](/hybrid-ensemble-variational/) methods and [4D-EnVar](/four-dimensional-ensemble-variational/): variational minimization with ensemble covariances.
- [Particle filter](/particle-filter/): a sample of the full posterior for small or moderate dimension.
- [Nudging](/nudging/): relaxation of the model toward the observations with a tuned gain.

## Bounds

- **Linear Gaussian, exact.** The Kalman filter needs $\Theta(n^2)$ memory for $P$ and, with dense matrices, $\Theta(n^3 + n^2 p + p^3)$ time per cycle for $p$ observations. For $n = 10^8$ the covariance alone would have $10^{16}$ entries, which is why operational methods never form it.
- **Optimality.** Among all estimators that are linear in the data, the Kalman analysis has the smallest error covariance when the model is linear and the error covariances are correct (a theorem in the sense of the [Gauss-Markov theorem](/gauss-markov-theorem/)). Gaussian errors make it optimal among all estimators.
- **Nonlinear, general.** No finite-dimensional recursion gives the exact filter in general. Standard particle filters need a number of particles that grows exponentially with the effective dimension of the observations to avoid [weight collapse](/particle-filter-weight-collapse/).
- **Predictability.** In a chaotic model, errors grow on average like $e^{\lambda_1 t}$ between analyses, so the observations must be frequent and accurate enough to hold the analysis error below the size of the attractor. In Lorenz-96 with $n = 40$ and $F = 8$, $\lambda_1$ is about 1.7 per time unit (a measurement, see the [Lorenz-96 model](/lorenz-96-model/)).

## Reductions

- **One analysis step to regularized least squares.** For a linear $H$ and Gaussian errors, the analysis is the solution of a [generalized least squares](/generalized-least-squares/) problem, the minimizer of $\|x - x^b\|^2_{B^{-1}} + \|y^o - Hx\|^2_{R^{-1}}$, which is [Tikhonov regularization](/tikhonov-regularization/) with the background as the prior. The cost of the reduction is that of forming products with $B$, $H$ and $R^{-1}$.
- **Strong constraint smoothing to nonlinear least squares.** With $Q = 0$, the smoothing problem is the minimization over $x_0$ alone of a nonlinear least squares cost, which [Gauss-Newton](/gauss-newton-algorithm/) steps solve with tangent linear and adjoint runs.
- **Smoothing to filtering.** For linear Gaussian models, a forward Kalman filter and a backward pass of the Rauch-Tung-Striebel smoother give the smoothing distribution in twice the cost of the filter.
- **From filtering to the general hidden Markov model.** Data assimilation is [filtering](/filtering/) and [smoothing](/smoothing/) for a [state-space model](/state-space-model/) with a very large state, a deterministic or almost deterministic transition and a linear or weakly nonlinear observation.

## Applications

- Initial conditions for numerical weather prediction, several times a day at every major center.
- Reanalysis: a consistent record of the past atmosphere or ocean from all historical observations and a fixed modern system.
- Ocean, sea ice, land surface, hydrology and atmospheric chemistry, where the models are partial differential equations and the observations are sparse.
- Evaluation of new observing systems before they are built, with [observing system simulation experiments](/observing-system-simulation-experiment/).
- Parameter estimation for physical models, and state estimation in engineering and epidemiology.

## References
