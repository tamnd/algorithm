---
tag: R82NR4
kind: algorithm
slug: prediction-error-method
name: Prediction error method
aliases:
- PEM
- prediction error identification
area: control/modeling-and-identification
level: core
summary: "Estimates model parameters by minimizing the sum of squared one-step prediction errors; for Gaussian white noise, with start-up effects ignored, this is maximum likelihood."
solves: [system-identification]
model: real-ram
complexity:
  vars: {N: the number of samples, d: the number of parameters, I: the number of iterations}
  time: {worst: O(I (N d^2 + d^3))}
  space: {extra: O(N d + d^2)}
properties: {deterministic: true, online: false, recursive: false, exact: false}
history:
  year: 1965
  people: [Karl Johan Åström, Torsten Bohlin]
  note: "Åström and Bohlin fitted ARMAX models to plant records by maximum likelihood with a numerical search in 1965; Ljung recast the method as the minimization of prediction errors for any model structure in the 1970s."
prereqs: [armax-model, output-error-model, least-squares-arx-identification, gauss-newton-algorithm]
see_also: [system-identification, instrumental-variable-identification, maximum-likelihood-estimation, levenberg-marquardt, nonlinear-least-squares, closed-loop-identification, cramer-rao-bound, kalman-filter]
sources:
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 7 (prediction error methods and their relation to maximum likelihood), Chapter 8 (convergence and consistency), Chapter 9 (asymptotic distribution) and Chapter 10 (computing the estimate: Gauss-Newton search and the gradient filters)"
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: the chapter on prediction error methods
  - paper: doi:10.1109/TAC.1978.1101840
    title: "Lennart Ljung, Convergence analysis of parametric identification methods, IEEE Transactions on Automatic Control 23(5), 770-783, 1978"
    locator: the convergence of prediction error estimates for general model structures
  - paper: "Karl Johan Åström and Torsten Bohlin, Numerical identification of linear dynamic systems from normal operating records, IFAC Symposium on Self-Adaptive Systems, Teddington, 1965; in P. H. Hammond (editor), Theory of Self-Adaptive Control Systems, Plenum Press, 1966, pp. 96-111"
    locator: the maximum likelihood fit of ARMAX models by a numerical search
---

The prediction error method (PEM) estimates the parameters $\theta$ of a dynamical model from measured inputs $u$ and outputs $y$ by choosing the $\theta$ whose one-step-ahead predictions of the output are best. For each candidate $\theta$, the model gives a predictor $\hat y(k \mid \theta)$ built from the data before time $k$; the method minimizes the mean of the squared prediction errors $\varepsilon(k, \theta) = y(k) - \hat y(k \mid \theta)$ over the record. The idea covers every linear black-box structure, including the [ARX](/arx-model/), [ARMAX](/armax-model/), [output error](/output-error-model/) and Box-Jenkins models, and it also applies to state-space and nonlinear models. When the noise is Gaussian and white with a fixed variance and the start-up effects are ignored, the estimate is the [maximum likelihood estimate](/maximum-likelihood-estimation/). Except in the ARX case, the criterion is not convex, so it is minimized by a local search, most often a damped [Gauss-Newton](/gauss-newton-algorithm/) iteration from a least squares start.

## In plain words

Take a model with some unknown numbers in it. For any choice of the numbers, the model can make a guess of the next output from everything measured so far. Compare each guess with what really came out, square the misses and average them. Good numbers give small misses. The method searches for the numbers that make the average miss smallest. It starts from a quick least squares answer and improves it step by step: at each step it works out which way to move each number, moves, and checks that the misses really got smaller before it keeps the move.

## The problem

**Input.** Samples $y(0), \ldots, y(N-1)$ and $u(0), \ldots, u(N-1)$, and orders $n_a, n_c, n_d, n_f \ge 0$, $n_b \ge 1$, $n_k \ge 0$ of the general linear model

$$A(q)\, y(k) = \frac{B(q)}{F(q)}\, u(k) + \frac{C(q)}{D(q)}\, e(k),$$

with $A, C, D, F$ monic polynomials in $q^{-1}$ and $B(q) = q^{-n_k}(b_1 + \cdots + b_{n_b} q^{-n_b+1})$. ARX has $n_c = n_d = n_f = 0$, ARMAX has $n_d = n_f = 0$, OE has $n_a = n_c = n_d = 0$, and Box-Jenkins has $n_a = 0$.

**Predictor.** With all signals taken as 0 before time 0,

$$w(k) = \frac{B(q)}{F(q)}\, u(k), \qquad v(k) = A(q)\, y(k) - w(k), \qquad \varepsilon(k, \theta) = \frac{D(q)}{C(q)}\, v(k).$$

**Admissible set.** $\theta = (a, b, c, d, f) \in \mathbb{R}^d$ with $C$ and $F$ Schur, so the filters $1/C$ and $1/F$ are BIBO stable.

**Output.** A local minimizer in the admissible set of

$$V(\theta) = \frac{1}{N - n_0} \sum_{k=n_0}^{N-1} \varepsilon(k, \theta)^2, \qquad n_0 = \max(n_a, n_k + n_b - 1, n_c, n_d, n_f).$$

## The algorithm

```pseudo id=main
PEM(y, u, orders, θ0)
L1  θ ← θ0, or the least squares ARX fit with c = d = 0 if no θ0 is given
L2  repeat
L3      compute ε(k, θ) and ψ(k, θ) = -∂ε(k, θ)/∂θ for k = n0, ..., N - 1 by filtering
L4      R ← Σ ψ(k) ψ(k)ᵀ;  g ← Σ ψ(k) ε(k)
L5      δ ← the solution of R δ = g  (fail if R is singular: the data are not informative)
L6      μ ← 1
L7      while C or F of θ + μ δ is not Schur, or V(θ + μ δ) ≥ V(θ), do μ ← μ/2  (stop after 40 halvings)
L8      θ ← θ + μ δ
L9  until the relative decrease of V is at most tol, or no step was accepted
L10 return θ and V(θ)
```

**The gradient filters (L3).** Differentiating the predictor equations gives, with $\psi = -\partial \varepsilon / \partial \theta$,

$$\psi_{a_i} = -\frac{D}{C}\, y(k-i), \quad \psi_{b_j} = \frac{D}{CF}\, u(k - n_k - j + 1), \quad \psi_{c_i} = \frac{1}{C}\, \varepsilon(k-i), \quad \psi_{d_i} = -\frac{1}{C}\, v(k-i), \quad \psi_{f_i} = -\frac{D}{CF}\, w(k-i).$$

So one pass of six filters gives all $d$ components. For ARMAX this reduces to $\psi = \varphi(k, \theta)/C$, the pseudo-regressor of past outputs, inputs and prediction errors filtered through $1/C$.

**The step (L4, L5).** The gradient of $V$ is $-\frac{2}{N - n_0} g$, and $\frac{2}{N - n_0} R$ is the Gauss-Newton approximation of its Hessian, which drops the second derivatives of $\varepsilon$. So $\delta = R^{-1} g$ is the Gauss-Newton direction. $R$ is positive semidefinite, and it is nonsingular when the data are informative and the parametrization is identifiable at $\theta$.

**The line search (L6, L7).** The full step can leave the admissible set or raise $V$ far from the minimum. L7 halves the step until both $C$ and $F$ stay Schur and $V$ strictly decreases. The Schur test uses the roots of $C$ and $F$, or the [Schur-Cohn test](/schur-cohn-test/).

## Example

Data: the ARMAX system $A = 1 - 1.5 q^{-1} + 0.7 q^{-2}$, $B = q^{-1} + 0.5 q^{-2}$, $C = 1 - q^{-1} + 0.2 q^{-2}$, with a white $\pm 1$ input, white Gaussian $e$ of unit variance and $N = 2000$ samples (seed 1). The model has $n_a = n_b = n_c = 2$ and $n_k = 1$, so $d = 6$. L1 starts from the least squares ARX fit with $c = 0$.

| step | $a_1$ | $a_2$ | $b_1$ | $b_2$ | $c_1$ | $c_2$ | $V$ |
|---|---|---|---|---|---|---|---|
| 0 | -1.2639 | 0.4873 | 1.0498 | 0.7262 | 0 | 0 | 1.80043 |
| 1 | -1.4436 | 0.6338 | 1.0413 | 0.5290 | -0.4280 | -0.1328 | 1.34242 |
| 2 | -1.5081 | 0.7001 | 1.0325 | 0.4461 | -0.7097 | -0.0954 | 1.13271 |
| 3 | -1.5070 | 0.7089 | 1.0368 | 0.4711 | -0.9414 | 0.1496 | 1.04266 |
| 4 | -1.5130 | 0.7130 | 1.0328 | 0.4597 | -0.9792 | 0.1876 | 1.04079 |
| final | -1.5129 | 0.7130 | 1.0326 | 0.4604 | -0.9801 | 0.1883 | 1.04079 |

The start is the biased ARX estimate. After four steps the estimate is within a few hundredths of the true $(-1.5, 0.7, 1, 0.5, -1, 0.2)$, and the search stops after eight accepted steps. The final $V = 1.04079$ is below $V$ at the true parameters, $1.04675$, which equals the mean of $e(k)^2$ over the samples: the minimizer fits the particular noise sequence slightly better than the truth does.

## Correctness

**Claim.** PEM returns an admissible $\theta$ with $V(\theta) \le V(\theta_0)$; every accepted step keeps $C$ and $F$ Schur and strictly lowers $V$. If the search stops because no step lowers $V$, then either $g = 0$, so $\theta$ is a stationary point of $V$, or no step $\mu \delta$ with $\mu \ge 2^{-39}$ lowers $V$. When $\varepsilon$ is affine in $\theta$, as for ARX, the first step lands exactly on the least squares solution.

**Key invariant.** At the start of each pass of L2, $\theta$ is admissible and $V(\theta)$ is at most every earlier value of $V$. The vector $\psi(k)$ of L3 is the exact negative gradient of $\varepsilon(k, \theta)$ for the recursions from rest, so $\delta$ is a descent direction whenever $g \ne 0$: $\nabla V^T \delta = -\frac{2}{N - n_0}\, g^T R^{-1} g < 0$.

Since the admissible set is open and $V$ is differentiable on it, a small enough $\mu$ gives a strict decrease, which is what L7 searches for. The full proof is below.

## Complexity

L3 runs a fixed number of linear filters of order $O(d)$ over the data, $O(N d)$. L4 costs $O(N d^2)$, and L5 costs $O(d^3)$ by Gaussian elimination. Each trial of L7 costs $O(N d)$ for $V$ and $O(d^3)$ for the roots of $C$ and $F$, and there are at most 40 trials. One iteration is therefore $O(N d^2 + d^3)$ in the [real RAM](/real-ram/), and $I$ iterations cost $O(I (N d^2 + d^3))$. The extra space is $O(N d + d^2)$ for the filtered signals and $R$. The number of iterations has no general bound. Near a minimum with small residuals Gauss-Newton converges fast; in the example eight steps were enough.

## Properties

- **Local, not global.** For ARMAX, OE and Box-Jenkins structures $V$ is not convex, and the search finds a local minimum near the start. For ARX it is convex and one step suffices.
- **Consistent (theorem).** If the model set contains the true system, the data are informative, and the global minimizer is found, then $\hat\theta_N \to \theta_0$ with probability 1 (Ljung 1999, Chapter 8). In open loop, structures with an independent noise model, such as OE and Box-Jenkins, give a consistent $G$ even when the noise model is wrong.
- **Asymptotically efficient (theorem).** Under the same conditions $\sqrt{N}(\hat\theta_N - \theta_0)$ is asymptotically normal with covariance $\sigma^2 (\mathbb{E}\, \psi \psi^T)^{-1}$, and for Gaussian $e$ this equals the [Cramér-Rao bound](/cramer-rao-bound/) (Ljung 1999, Chapter 9). The matrix $R$ of L4 at the end gives the estimate $\hat\sigma^2 R^{-1}$ of the covariance of $\hat\theta$.
- **Maximum likelihood (theorem).** If $e$ is Gaussian and white with a fixed variance, and the start-up effect of the zero initial conditions is ignored, then the log-likelihood is a decreasing function of $V$, so the minimizer of $V$ is the maximum likelihood estimate. With the variance unknown, maximizing over it gives the same $\theta$. Without these conditions, PEM is still defined, but it is not the likelihood.
- **Approximation (theorem).** When the true system is not in the model set, the estimate converges to the minimizer of the limit criterion, which in the frequency domain is a fit of $G$ weighted by the input spectrum and the inverse noise model (Ljung 1999, Chapter 8).

## Variants and improvements

- **[Levenberg-Marquardt](/levenberg-marquardt/).** Solve $(R + \lambda I)\, \delta = g$ in L5 instead of halving the step; this handles a nearly singular $R$.
- **Quasi-Newton.** [BFGS](/bfgs/) and other quasi-Newton methods use the exact gradient of L3 and build up curvature, which helps when the residuals are large.
- **Recursive prediction error method.** Update $\theta$ and $R^{-1}$ at each sample with the current $\psi$, as the [RLS algorithm](/rls-algorithm/) does for ARX, for online use.
- **Multivariable and state-space models.** For several outputs, minimize $\det \sum \varepsilon \varepsilon^T$; for innovations state-space models, the predictor is the steady-state [Kalman filter](/kalman-filter/).
- **Initial conditions.** Estimate the initial state together with $\theta$, or use $n_0$ large enough to let the transient die out, instead of the zero start.
- **Frequency-domain PEM.** Weight the squared errors of the discrete Fourier transforms, which allows prefiltering and band selection.
- **Better starts.** Instrumental variable estimates or high-order ARX fits followed by model reduction lower the risk of a bad local minimum.

## When to use it

Use it when an accurate low-order model with a noise model is wanted, after a quick least squares fit has given a start value. It is the method of choice for ARMAX, OE and Box-Jenkins structures in open loop, and the direct method in [closed-loop identification](/closed-loop-identification/) when the noise model can be made correct. If only a quick answer is needed or the noise is close to white equation error, least squares may be enough; if the criterion has bad local minima, start from an instrumental variable estimate.

## Pitfalls

- **Unstable predictor filters.** Taking $\theta \leftarrow \theta + \delta$ without testing $C$ and $F$ in L7 can give a $C$ with a root outside the unit circle; then $\varepsilon$ grows without bound and the next $R$ is useless. L7 must halve $\mu$ until $C$ and $F$ are Schur.
- **Steps that raise the criterion.** Accepting the full Gauss-Newton step in L8 without the test $V(\theta + \mu\delta) < V(\theta)$ of L7 can diverge when the start is far from the minimum. Keep the strict decrease test.
- **The pseudo-linear shortcut.** Using the unfiltered pseudo-regressor $\varphi(k, \theta)$ in place of $\psi$ in L3 gives the extended least squares method, which converges only under a positive real condition on $1/C$. L3 must filter through $1/C$, and through $1/F$ for the $b$ and $f$ components.
- **A poor start.** A zero start in L1 for an OE model can lead to a local minimum far from the truth. L1 should start from a least squares or instrumental variable estimate, with $F$ taken from the autoregressive part when $n_a = 0$.
- **Transients in the sum.** Summing from $k = 0$ in L4 when the system was not at rest adds start-up errors that do not shrink with $\theta$. Sum from $n_0$, and estimate the initial state if the transient is long.

## Implementations

## History

Åström and Bohlin fitted ARMAX models to normal operating records by maximum likelihood in 1965, with a numerical search on the sum of squared residuals of the predictor. In the 1970s Ljung showed that the same criterion makes sense for any model structure that defines a predictor, gave convergence results that do not assume the true system is in the model set (1978), and made the prediction error framework the basis of his textbook of 1987 and its second edition of 1999.

## References
