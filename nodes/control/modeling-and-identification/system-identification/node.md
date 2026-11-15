---
tag: MM6501
kind: problem
slug: system-identification
name: System identification
aliases:
- identification of dynamical systems
- plant identification
area: control/modeling-and-identification
level: core
summary: Build a model of a dynamical system from measured inputs and outputs, by choosing a model set and the member that best predicts the data.
model: real-ram
complexity:
  vars: {N: the number of samples, d: the number of parameters}
  time: {worst: O(N d^2 + d^3)}
prereqs: [linear-time-invariant-system, transfer-function, least-squares-problem]
see_also: [arx-model, prediction-error-method, least-squares-arx-identification, empirical-transfer-function-estimate, subspace-identification, persistent-excitation, closed-loop-identification, maximum-likelihood-estimation]
sources:
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 1 (the identification loop), Chapter 4 (models of linear time-invariant systems), Chapter 7 (parameter estimation methods), Chapter 8 (convergence and consistency) and Chapter 9 (asymptotic distribution of parameter estimates)"
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: "the chapters on linear regression, prediction error methods and instrumental variable methods"
  - paper: doi:10.1016/0005-1098(71)90059-8
    title: "Karl Johan Åström and Pieter Eykhoff, System identification: a survey, Automatica 7(2), 123-162, 1971"
    locator: the whole paper (least squares, maximum likelihood and instrumental variables as they stood in 1971)
  - paper: doi:10.1109/TAC.1978.1101840
    title: "Lennart Ljung, Convergence analysis of parametric identification methods, IEEE Transactions on Automatic Control 23(5), 770-783, 1978"
    locator: the convergence of prediction error estimates to the minimizers of the limit criterion, without the assumption that the true system is in the model set
---

System identification is the problem of building a mathematical model of a dynamical system from measured data: records of the input $u$ that drives the system and of the output $y$ it produces. In the parametric form, the user fixes a model set, for example the [ARX models](/arx-model/) of given orders, and the method picks the member that best explains the data, most often the one with the smallest sum of squared one-step prediction errors. In the nonparametric form, the method estimates a curve such as the [frequency response](/frequency-response/) or the [impulse response](/impulse-response/) directly. There is no complexity class to state; what is known is which criterion each method minimizes, when the minimizer converges to the true system, and how large its variance is.

## In plain words

You have a machine, a motor or a chemical reactor or a building, and you want an equation that tells how its output reacts to its input. You cannot take it apart, but you can push it and watch. So you apply an input signal, record what comes out, and choose an equation from a family of candidates that fits the record best. The family can be simple, such as "the next output is a weighted sum of the last few outputs and inputs", and then fitting is a least squares problem. A richer family also models the noise, and fitting then needs an iterative search. Two things decide the quality. The input must shake the machine in enough different ways, and the family must be rich enough to contain something close to the truth.

## Definition

Time is discrete, $k = 1, 2, \ldots, N$, with sampling period $h$. The data are $Z^N = \{u(1), y(1), \ldots, u(N), y(N)\}$. Write $q$ for the forward shift, $q\, u(k) = u(k+1)$.

**The model set.** A model structure is a map from a parameter set $D \subset \mathbb{R}^d$ to pairs of transfer functions,

$$y(k) = G(q, \theta)\, u(k) + H(q, \theta)\, e(k), \qquad \theta \in D,$$

where $e$ is white noise with variance $\sigma^2$, $H$ is monic ($H(\infty, \theta) = 1$), and $H$ and $H^{-1}$ are BIBO stable. The model gives the one-step-ahead predictor

$$\hat y(k \mid \theta) = H^{-1}(q, \theta)\, G(q, \theta)\, u(k) + \big(1 - H^{-1}(q, \theta)\big)\, y(k),$$

which uses only data up to time $k - 1$, and the prediction error $\varepsilon(k, \theta) = y(k) - \hat y(k \mid \theta) = H^{-1}(q, \theta)\big(y(k) - G(q, \theta) u(k)\big)$.

**The question.** Given $Z^N$ and the structure, return

$$\hat\theta_N = \arg\min_{\theta \in D} V_N(\theta), \qquad V_N(\theta) = \frac{1}{N} \sum_{k=1}^{N} \varepsilon(k, \theta)^2,$$

or, in the nonparametric form, return an estimate $\hat G_N(e^{i\omega})$ of the frequency response on a grid of frequencies $\omega \in [0, \pi]$.

**The true system.** The analysis assumes that the data come from $y = G_0(q)\, u + H_0(q)\, e_0$. The model set contains the system if $G(q, \theta_0) = G_0$ and $H(q, \theta_0) = H_0$ for some $\theta_0 \in D$. The data are informative for the set if two models of the set that give the same predictions on the data have the same $G$ and $H$; for an open-loop experiment this is a condition on the input, see [persistent excitation](/persistent-excitation/).

## Variants

- **Choice of structure.** [ARX](/arx-model/), [ARMAX](/armax-model/), [output error](/output-error-model/) and Box-Jenkins models are the common linear black-box sets. State-space models of a given order are the set for [subspace identification](/subspace-identification/). A grey-box model has parameters with a physical meaning, for example a mass or a resistance.
- **Parametric or nonparametric.** A nonparametric estimate is a curve: the [empirical transfer function estimate](/empirical-transfer-function-estimate/) in frequency, or a long FIR model in time, possibly regularized as in [kernel-based identification](/kernel-based-identification/).
- **Open or closed loop.** In [closed-loop identification](/closed-loop-identification/) the input depends on past outputs through a controller, which changes which models can be told apart and which methods remain consistent.
- **Batch or recursive.** The batch problem uses the whole record. The recursive problem updates the estimate at each sample, as the [RLS algorithm](/rls-algorithm/) does for ARX models; this is the core of adaptive control.
- **Order selection.** The orders are part of the question: choose them by a criterion such as the [Akaike information criterion](/akaike-information-criterion/) or by [cross-validation](/cross-validation/) on fresh data.
- **Experiment design.** Choose the input, within limits on its amplitude or power, to make the estimate as accurate as possible; a [PRBS](/prbs-input/) is the classic choice.

## Examples

1. **A first-order ARX fit.** With the six samples $u = (1, 1, -1, 1, -1, -1)$ and $y = (0, 1, 1.4, -0.2, 0.9, -0.6)$, the model $y(k) + a\, y(k-1) = b\, u(k-1) + e(k)$ has the least squares estimate $\hat a = -163/336 \approx -0.4851$ and $\hat b = 5407/5600 \approx 0.9655$. The computation is on the page [least-squares identification of ARX models](/least-squares-arx-identification/).
2. **An input that is too poor.** For $y(k) + a\, y(k-1) = b_1 u(k-1) + b_2 u(k-2)$ and the constant input $u \equiv 1$, the data depend on $b_1$ and $b_2$ only through $b_1 + b_2$. Every pair with the same sum predicts the data equally well, so the minimizer of $V_N$ is not unique. A constant is persistently exciting of order 1 only, and this model needs order 2 in $u$.
3. **Feedback without an external signal.** For $y(k) + a\, y(k-1) = b\, u(k-1) + e(k)$ under the controller $u(k) = -c\, y(k)$, the output obeys $y(k) + (a + bc)\, y(k-1) = e(k)$. All pairs $(a, b)$ with the same $a + bc$ give the same predictor, so the open-loop system cannot be recovered. With $a = -0.8$, $b = 1$ and $c = 0.5$ the data show only $a + bc = -0.3$. An added reference signal removes the ambiguity.

## Known algorithms

- [Least-squares identification of ARX models](/least-squares-arx-identification/): the exact minimizer of $V_N$ for ARX and FIR structures in $O(N d^2 + d^3)$ operations.
- [Prediction error method](/prediction-error-method/): minimizes $V_N$ for any structure by Gauss-Newton steps, $O(N d^2 + d^3)$ per iteration, and finds a local minimum.
- [Instrumental variable identification](/instrumental-variable-identification/): a linear estimate for the ARX parametrization of $G$ that stays consistent under colored noise, in $O(N d^2 + d^3)$.
- [Empirical transfer function estimate](/empirical-transfer-function-estimate/): the ratio of the output and input Fourier transforms, in $O(N \log N)$ with the [FFT](/fast-fourier-transform/), followed by smoothing.
- [Subspace identification](/subspace-identification/), with [N4SID](/n4sid/) and [MOESP](/moesp/): state-space models from projections of block Hankel matrices, without iterative search.
- [Ho-Kalman algorithm](/ho-kalman-algorithm/): a minimal realization from [Markov parameters](/markov-parameters/).
- [Process reaction curve method](/process-reaction-curve/): a first order plus dead time model from one step response.

## Bounds

There is no exact complexity result, because the output is an estimate, not an exact answer. The bound $O(N d^2 + d^3)$ in the header holds for model sets in which the predictor is linear in $\theta$, such as ARX and FIR; for other sets the cost depends on the number of iterations of the search. The known results are about what each criterion converges to and how fast its error falls. All operation counts are in the [real RAM](/real-ram/).

- **Cost of the linear case.** For a structure in which $\hat y(k \mid \theta)$ is linear in $\theta$, forming the normal equations costs $O(N d^2)$ and solving them $O(d^3)$. Reading the data is a lower bound of $\Omega(N)$.
- **Convergence (theorem).** If the data are quasi-stationary and the predictors are uniformly BIBO stable over a compact $D$, then $\hat\theta_N$ converges with probability 1 to the set of minimizers of $\bar V(\theta) = \lim_{N \to \infty} \mathbb{E}\, V_N(\theta)$ (Ljung 1978; Ljung 1999, Chapter 8). The true system need not be in the model set: the limit is the best approximation in the sense of $\bar V$.
- **Consistency (theorem).** If the model set contains the true system, the data are informative and the parametrization is identifiable at $\theta_0$, then $\theta_0$ is the unique minimizer of $\bar V$, so $\hat\theta_N \to \theta_0$ with probability 1 (Ljung 1999, Chapter 8).
- **Variance (theorem).** Under the same conditions, $\sqrt{N}(\hat\theta_N - \theta_0)$ is asymptotically normal with covariance $P = \sigma^2 \big(\mathbb{E}\, \psi \psi^T\big)^{-1}$, where $\psi = -\partial \varepsilon / \partial \theta$ at $\theta_0$ (Ljung 1999, Chapter 9). For Gaussian $e$ this equals the [Cramér-Rao bound](/cramer-rao-bound/), so no unbiased estimator does better asymptotically.
- **Nonconvexity.** For ARX and FIR structures $V_N$ is a convex quadratic. For ARMAX, output error and Box-Jenkins structures it is not convex, and a local search can stop at a local minimum.

## Reductions

- **ARX to linear least squares.** The ARX predictor is $\varphi(k)^T \theta$ with a regressor $\varphi(k)$ of past outputs and inputs, so the problem is an instance of the [least squares problem](/least-squares-problem/), with $O(N d)$ work to build the regressors.
- **Prediction errors to maximum likelihood.** If $e$ is Gaussian with known variance and the effect of initial conditions is ignored, minimizing $V_N$ gives the [maximum likelihood estimate](/maximum-likelihood-estimation/) of $\theta$.
- **Closed loop to open loop.** The indirect method identifies the map from the reference to the output, an open-loop problem, and then solves for the plant with the known controller.
- **Order to model selection.** Choosing the orders is a model selection problem, solved by fitting each candidate order and comparing a penalized cost.

## Applications

- Models for controller design: step tests for [PID tuning](/ziegler-nichols-tuning/), and step-response or ARX models for model predictive control in the process industry.
- Fault detection: a change in the identified parameters signals a change in the plant.
- [Adaptive control](/adaptive-control/) and the [self-tuning regulator](/self-tuning-regulator/), which identify the plant online and redesign the controller at each step.
- Vibration and modal analysis of structures, and acoustic echo paths.
- Time-series models with exogenous inputs in econometrics, in the tradition of Box and Jenkins.

## References
