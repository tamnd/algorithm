---
tag: 421ZWN
kind: algorithm
slug: ensemble-kalman-inversion
name: Ensemble Kalman inversion
aliases:
- EKI
area: scientific-computing/data-assimilation
level: research
summary: Solves inverse problems by repeated ensemble Kalman updates in an artificial time, with no derivatives of the forward model.
model: real-ram
complexity:
  vars: {d: the number of unknowns, p: the number of data, N: the ensemble size, K: the number of steps}
  time: {worst: "Θ(K (N p (d + p) + p^3))"}
  space: {extra: "Θ(K N d + N p + p^2)"}
properties: {derivative_free: true, deterministic: "in the modes none and sqrt", subspace: "the members stay in the affine span of the initial ensemble", exact: "mode sqrt with a linear G, exact initial moments and K h = 1", tempering: "K steps of size h = 1/K use the likelihood in K equal parts"}
history:
  year: 2013
  people: [Marco A. Iglesias, Kody J. H. Law, Andrew M. Stuart]
  note: "Iglesias, Law and Stuart proposed the ensemble Kalman method for general inverse problems in 2013. Schillings and Stuart analysed its continuous time limit in 2017."
prereqs: [ensemble-kalman-filter, bayesian-inverse-problem]
see_also: [ensemble-transform-kalman-filter, ensemble-kalman-smoother, gauss-newton-algorithm, landweber-iteration, tikhonov-regularization, four-dimensional-variational-assimilation, covariance-inflation]
sources:
  - paper: doi:10.1088/0266-5611/29/4/045001
    title: "M. A. Iglesias, K. J. H. Law and A. M. Stuart, Ensemble Kalman methods for inverse problems, Inverse Problems 29(4) (2013) 045001"
    locator: the iterative ensemble Kalman method for inverse problems and the property that the members stay in the span of the initial ensemble
  - paper: doi:10.1137/16M105959X
    title: "C. Schillings and A. M. Stuart, Analysis of the ensemble Kalman filter for inverse problems, SIAM Journal on Numerical Analysis 55(3) (2017) 1264-1290"
    locator: the continuous time limit, its gradient flow structure and the results for linear forward models
  - paper: doi:10.1016/j.cageo.2012.03.011
    title: "A. A. Emerick and A. C. Reynolds, Ensemble smoother with multiple data assimilation, Computers & Geosciences 55 (2013) 3-15"
    locator: the same data assimilated several times with the error covariance multiplied by factors whose inverses add up to one
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation of the data assimilation pages
---

Ensemble Kalman inversion (EKI) uses the analysis step of the [ensemble Kalman filter](/ensemble-kalman-filter/) to solve an inverse problem $y = G(u) + e$. An ensemble of candidate parameters is moved towards the data by repeated Kalman updates with the same data, in an artificial time. Each step calls the forward model $G$ once for each member and needs no derivative of $G$ and no adjoint. The members always stay in the span of the initial ensemble. For a linear $G$, the square root form with $K$ steps of size $h = 1/K$ gives the exact Gaussian posterior. For a nonlinear $G$ the method is a derivative-free optimizer of the data misfit.

## In plain words

You want the parameters of a model that make its output match some data. You cannot differentiate the model, but you can run it. Start with a cloud of guesses and run the model for each. Where the guesses differ, compare how their outputs differ. This tells you which way to move each guess to bring its output closer to the data. Move every guess part of the way, run the model again and repeat. The cloud shrinks around the parameters that fit the data. The cloud only moves inside the space spanned by the first guesses, so these must be chosen with care.

## The problem

**Input.** A forward model $G: \mathbb R^d \to \mathbb R^p$ that can be evaluated, data $y \in \mathbb R^p$ with a noise covariance $\Gamma$ (symmetric positive definite), an initial ensemble $u_1, \ldots, u_N \in \mathbb R^d$ drawn from a prior, a step size $h > 0$ and a number of steps $K$. The notation follows Ide, Courtier, Ghil and Lorenc (1997), with the unknown $u$ in place of the state $x$ and $G$ in place of $H$. In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, the model $M$ is its $A$, the forecast $x^f$ and $P^f$ are its predicted $m^-$ and $P^-$, and the analysis $x^a$ and $P^a$ are its filtered $m$ and $P$.

**Output.** The ensembles after each step. For a linear $G$, a Gaussian prior whose mean and covariance the initial ensemble matches exactly, and $Kh = 1$, the square root form ends with the mean and the covariance of the posterior of the [Bayesian inverse problem](/bayesian-inverse-problem/). In the other cases the ensemble mean is an estimate of $u$ and the spread a rough measure of its uncertainty.

## The algorithm

$\bar u$ and $\bar g$ are the ensemble means of the $u_i$ and the $g_i$, and $C^{ug}$ and $C^{gg}$ the sample covariances with the divisor $N - 1$.

```pseudo id=main
EKI(u_1..u_N, G, y, Gamma, h, K)
L1  for k <- 1 to K do
L2      g_i <- G(u_i) for each member
L3      compute ubar, gbar, C^ug and C^gg
L4      y_i <- y, or y + eta_i with eta_i ~ N(0, Gamma / h) for perturbed data
L5      S <- C^gg + Gamma / h; u_i <- u_i + C^ug S^-1 (y_i - g_i) for each member
L6  return the ensembles of all steps
```

Line L5 is the analysis step of the EnKF with the observation error covariance $\Gamma/h$, where $G$ plays the role of the observation operator. The matrix $C^{ug}S^{-1}$ is a Kalman gain built from the ensemble. It replaces the derivative of $G$ by a linear regression of $u$ on $G(u)$ over the members. A small $h$ makes $\Gamma/h$ large, so each step moves the members a short way.

The code has three modes. Mode "perturbed" uses the perturbed targets of line L4. Mode "none" uses $y_i = y$ for all members. Mode "sqrt" replaces line L5 by the deterministic weights of the [ETKF](/ensemble-transform-kalman-filter/) with $R = \Gamma/h$.

## Example

Take $d = p = 1$, $G(u) = u$, $y = 1$, $\Gamma = 1$, two members $u = (-1, 1)$ (mean $0$, variance $2$) and two steps of size $h = 1/2$, so $\Gamma/h = 2$.

In mode "none", the first step has $C^{ug} = C^{gg} = 2$ and $S = 4$, so the gain is $1/2$ and each member moves halfway to $1$: the ensemble is $(0, 1)$ with the variance $1/2$. The second step has the gain $(1/2)/(1/2 + 2) = 1/5$, so $0$ moves to $1/5$ and $1$ stays. The ensemble $(1/5, 1)$ has the mean $3/5$ and the variance $0.32$.

The posterior for the prior $N(0, 2)$ has the variance $(1/2 + 1)^{-1} = 2/3$ and the mean $2/3$. Mode "sqrt" gives exactly these values after the two steps (Theorem 3 of the proof). Mode "none" gives a smaller mean and a much smaller variance: at each step it removes $K(\Gamma/h)K^\top$ more spread than the Kalman update (Proposition 4).

For the check value of the page group: with two members $\mp 1/\sqrt 2$, $y = 1$, $\Gamma = 1$ and one step with $h = 1$, mode "sqrt" gives the mean $1/2$ and the variance $1/2$, and mode "none" gives the mean $1/2$ and the variance $1/4$.

**A measurement.** For the nonlinear model $G(u) = (u_1 + u_2^2/2,\ e^{0.3u_1} - u_2)$ with the data $y = G(0.7, -0.4)$ without noise, $\Gamma = 0.01I$, $h = 1$ and initial members drawn from $N(0, I)$ with seed 3, the misfit $|G(\bar u) - y|$ of the ensemble mean after $k$ steps was:

| mode | $N$ | $k = 0$ | $k = 1$ | $k = 5$ | $k = 40$ |
|---|---|---|---|---|---|
| none | 5 | 1.25 | 0.160 | 0.0702 | 0.0275 |
| none | 20 | 1.06 | 0.513 | 0.0149 | 0.0063 |
| perturbed | 5 | 1.25 | 0.165 | 0.0830 | 0.0134 |
| perturbed | 20 | 1.06 | 0.525 | 0.0357 | 0.0070 |
| sqrt | 5 | 1.25 | 0.160 | 0.0369 | 0.0049 |
| sqrt | 20 | 1.06 | 0.513 | 0.0076 | 0.0011 |

With $N = 20$ the final mean was within $0.007$ of $(0.7, -0.4)$ in all three modes. The misfit falls quickly at first and then slowly, because the spread, and with it the step, shrinks. The 40 steps took 2 to 3 ms in modes "none" and "perturbed" and 300 ms in mode "sqrt" with $N = 20$, where the $N \times N$ eigendecomposition dominates. With perturbed data, $N = 4000$, $G(u) = u$, $y = 1$, $\Gamma = 1$ and four steps of $h = 1/4$, a prior sample with the mean $0.006$ and the variance $0.981$ ended with the mean $0.489$ and the variance $0.483$, near the posterior values $0.5$ and $0.5$.

## Correctness

The [proof](proofs/correctness.md) shows that in every mode and for every $G$ the members stay in the affine span of the initial ensemble (Lemma 1, the subspace property of Iglesias, Law and Stuart). For a linear $G$, one step of mode "sqrt" conditions the sample Gaussian on the data with the noise $\Gamma/h$ (Lemma 2), so $k$ steps give the posterior with the likelihood raised to the power $kh$, which is the exact posterior when $kh = 1$ (Theorem 3). Mode "none" has the Kalman mean but a covariance smaller than the Kalman one by $K(\Gamma/h)K^\top$ (Proposition 4). For small $h$, mode "none" is an Euler step of a gradient flow of the misfit preconditioned by the ensemble covariance, which Schillings and Stuart (2017) analyse. For a nonlinear $G$ the result is not the posterior, and convergence is measured, not proved.

## Complexity

In modes "none" and "perturbed", line L3 costs $\Theta(N(d + p)p)$ for $C^{ug}$ and $C^{gg}$, line L4 costs $\Theta(p^3 + Np^2)$ for the Cholesky factor and the draws, and line L5 costs $\Theta(p^3 + p^2N)$ for the solve with $N$ right sides and $\Theta(Ndp)$ for the update. $K$ steps cost $\Theta(K(Np(d + p) + p^3))$ plus $KN$ runs of $G$, which usually dominate. Mode "sqrt" adds $\Theta(N^2(p + d) + N^3)$ for each step. The code keeps all $K + 1$ ensembles, $\Theta(KNd)$ space, plus $\Theta(Np + p^2)$ for one step. Keeping only the last ensemble needs $\Theta(Nd)$.

## Properties

- **Derivative free.** Only evaluations of $G$ are needed, and the $N$ runs of one step are independent and can run in parallel.
- **Subspace property.** The solution is a combination of the initial members. With $N - 1 < d$ the method searches a space of dimension $N - 1$ only.
- **Tempering.** $K$ steps of size $h = 1/K$ split the likelihood into $K$ equal parts. With perturbed data this is the ensemble smoother with multiple data assimilation (ES-MDA) of Emerick and Reynolds (2013) with all factors equal to $K$.
- **Collapse.** Without perturbations of the data the spread shrinks at every step for a linear $G$, so the ensemble collapses towards one point as the steps go on.
- **Invariance.** If $u$ is replaced by $Tu$ for an invertible matrix $T$ and $G$ by $G \circ T^{-1}$, the members are replaced by $Tu_i$ at every step, because the update depends on $G$ only through the outputs of the members.

## Variants and improvements

- **Different step sizes.** Steps $h_1, \ldots, h_K$ with $\sum_k h_k = 1$ also give the exact posterior in mode "sqrt" for a linear $G$, by the same proof. ES-MDA allows unequal factors $1/h_k$.
- **Continuous time.** Letting $h \to 0$ gives a system of coupled ordinary differential equations for the members (Schillings and Stuart 2017).
- **Regularization.** Adding the prior term to the misfit, or stopping the steps when the misfit reaches the noise level, prevents fitting the noise. The second option is the discrepancy principle of [Landweber iteration](/landweber-iteration/) and similar methods.
- **Localization and inflation.** As in the filters, [covariance inflation](/covariance-inflation/) keeps the spread from collapsing too early, and localization changes the gain so that the members can leave the span of the initial ensemble.

## When to use it

Use EKI when the forward model is a black box that is expensive to run, has no adjoint, and can be run many times in parallel, as with the reservoir models of Emerick and Reynolds. With a derivative and a few hundred unknowns, the [Gauss-Newton algorithm](/gauss-newton-algorithm/) or [4D-Var](/four-dimensional-variational-assimilation/) usually converge in fewer runs. For a linear $G$ of moderate size, solve the Gaussian posterior or the [Tikhonov](/tikhonov-regularization/) problem directly.

## Pitfalls

- **Full weight at every step (line L5).** Using $\Gamma$ instead of $\Gamma/h$ with $K$ steps counts the data $K$ times, and the spread becomes too small.
- **Too few members (line L3).** With $N - 1 < d$ the answer stays in the span of the initial ensemble. If the true parameter has a part outside this span, the method cannot find it.
- **Fitting the noise (line L1).** With noisy data, running too many steps in mode "none" drives the misfit below the noise level. Stop at the noise level, or use $Kh = 1$.
- **Reading the spread as uncertainty.** For a nonlinear $G$, and for mode "none" in any case, the final spread is not the posterior spread.
- **Strong nonlinearity (line L5).** The gain is a linear regression over the whole ensemble. If $G$ is far from linear over the spread of the ensemble, the step can point the wrong way, and smaller steps help.

## Implementations

## History

Iglesias, Law and Stuart proposed in 2013 to use the ensemble Kalman update as a general method for inverse problems, iterated with the same data, and noted that the members stay in the span of the initial ensemble. In the same year Emerick and Reynolds published the ensemble smoother with multiple data assimilation for reservoir models, which assimilates the same data several times with an inflated error covariance. Schillings and Stuart derived the continuous time limit in 2017 and analysed it for linear forward models.

## References
