---
tag: BZ95E9
kind: algorithm
slug: three-dimensional-variational-assimilation
name: Three-dimensional variational assimilation
aliases:
- 3D-Var
area: scientific-computing/data-assimilation
level: core
summary: "Finds the analysis by minimizing the distance to the background weighted by B^-1 plus the distance to the observations weighted by R^-1, at one time."
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the state dimension, p: the number of observations, k: the number of outer loops, m: the number of conjugate gradient steps per outer loop}
  time: {worst: "Θ(n^3 + p^3 + k m (n^2 + n p + p^2))"}
  space: {extra: "Θ(n^2 + n p + p^2)"}
properties: {deterministic: true, exact_for_linear_h: "one outer loop with an exact inner solve", equals_oi_and_kalman_update: "for a linear observation operator", minimizer: Gauss-Newton outer loop with conjugate gradient inner loop, covariances: B fixed in time}
history:
  year: 1986
  people: [Andrew C. Lorenc, David F. Parrish, John C. Derber]
  note: Lorenc gave the Bayesian variational form of the analysis in 1986, and Parrish and Derber made 3D-Var the operational analysis at the US National Meteorological Center in the early 1990s.
prereqs: [optimal-interpolation, background-error-covariance]
see_also: [four-dimensional-variational-assimilation, incremental-4d-var, control-variable-transform, gauss-newton-algorithm, conjugate-gradient-method, maximum-a-posteriori-estimation, tikhonov-regularization, kalman-filter]
sources:
  - paper: doi:10.1002/qj.49711247414
    title: A. C. Lorenc, Analysis methods for numerical weather prediction, Quarterly Journal of the Royal Meteorological Society 112(474) (1986) 1177-1194
    locator: the Bayesian derivation of the variational cost and its equivalence with optimal interpolation
  - paper: doi:10.1175/1520-0493(1992)120<1747:TNMCSS>2.0.CO;2
    title: D. F. Parrish and J. C. Derber, The National Meteorological Center's spectral statistical-interpolation analysis system, Monthly Weather Review 120(8) (1992) 1747-1763
    locator: the first operational 3D-Var, with B modeled in spectral space
  - book: isbn:9780521796293
    title: Eugenia Kalnay, Atmospheric Modeling, Data Assimilation and Predictability, Cambridge University Press, 2003
    locator: Section 5.5 (3D-Var, the physical space analysis scheme, and their relation to OI)
  - book: isbn:9783319203249
    title: K. Law, A. Stuart and K. Zygalakis, Data Assimilation, A Mathematical Introduction, Springer, 2015
    locator: Section 4.2.1 (3DVAR as a filter) and Section 4.4.2 (the 3DVAR filter for the Lorenz models)
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

Three-dimensional variational assimilation (3D-Var) computes the analysis $x^a$ as the minimizer of a cost function $J(x)$ with two terms: the distance from the background $x^b$, weighted by the inverse of the [background error covariance](/background-error-covariance/) $B$, and the distance from the observations $y^o$, weighted by the inverse of the observation error covariance $R$. All observations of a time window are treated as valid at one time, hence "three-dimensional". For a linear [observation operator](/observation-operator/) the minimizer is the same analysis as global [optimal interpolation](/optimal-interpolation/) and the analysis step of the [Kalman filter](/kalman-filter/), but 3D-Var uses all observations at once without local selection, accepts a nonlinear operator such as a radiative transfer model for satellite radiances, and needs only products with $B$, $H$ and $H^\top$, never the inverse of a large matrix. If the errors are Gaussian, $J$ is the negative logarithm of the posterior density, so $x^a$ is the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/).

## In plain words

A weather center has a forecast and a large set of new measurements. It looks for the state of the atmosphere that agrees as well as possible with both. Each disagreement is counted with a weight: a large departure from the forecast costs much where the forecast is known to be good, and a large departure from a measurement costs much where the measurement is known to be good. The total cost is a single number, and the method searches for the state with the smallest total. It does this in steps. In each step it replaces the curved link between the state and the measured quantities by a straight one, solves that easier problem, and moves to its solution. For measurements that depend on the state in a straight way, one step is enough.

## The problem

**Input.** A background $x^b \in \mathbb R^n$ with error covariance $B$, observations $y^o \in \mathbb R^p$ with error covariance $R$ (both symmetric positive definite), and an observation operator $h : \mathbb R^n \to \mathbb R^p$ with Jacobian $H(x)$. Here $n$ is the state dimension and $p$ the number of observations. This is the notation of Ide, Courtier, Ghil and Lorenc (1997). In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, and $x^b$ and $B$ are its predicted values $\hat x$ and $P$.

**Output.** A minimizer, or for a nonlinear $h$ a stationary point, of

$$J(x) = \tfrac12 (x - x^b)^\top B^{-1}(x - x^b) + \tfrac12 \big(y^o - h(x)\big)^\top R^{-1}\big(y^o - h(x)\big).$$

The gradient is $\nabla J(x) = B^{-1}(x - x^b) - H(x)^\top R^{-1}(y^o - h(x))$. For a linear $h(x) = Hx$ the minimizer is $x^a = x^b + K(y^o - Hx^b)$ with $K = BH^\top(HBH^\top + R)^{-1}$.

## The algorithm

The reference code uses the incremental form: an outer loop of Gauss-Newton steps, each of which minimizes the cost with $h$ linearized at the current point, and an inner [conjugate gradient](/conjugate-gradient-method/) solve.

```pseudo id=main
3DVAR(x^b, B, y^o, h, H(.), R)
L1  x <- x^b
L2  for outer <- 1 to max_outer do
L3      d <- y^o - h(x)                                   ▷ departures from the current point
L4      H <- H(x)                                         ▷ Jacobian of h at x
L5      A <- B^-1 + H^T R^-1 H                            ▷ Gauss-Newton Hessian, as a function
L6      g <- B^-1 (x - x^b) - H^T R^-1 d                  ▷ gradient of J at x
L7      dx <- solve A dx = -g by conjugate gradients
L8      x <- x + dx
L9      if |dx| <= tol (1 + |x|) then break
L10 return x
```

Line L5 never forms $A$: conjugate gradients only need the product $Av$, which is one solve with $B$, one product with $H$, one solve with $R$ and one product with $H^\top$. Line L6 is the gradient of $J$ (Lemma 1 of the proof). The code applies $B^{-1}$ and $R^{-1}$ through Cholesky factors. Operational codes do not apply $B^{-1}$ at all. They minimize over a [control variable](/control-variable-transform/) $v$ with $x - x^b = Uv$ and $B = UU^\top$, which turns the background term into $\tfrac12 v^\top v$ and makes the inner problem much better conditioned.

## Example

**One scalar observation.** With $n = p = 1$, $x^b = 0$, $B = 1$, $y^o = 1$, $R = 1$ and $h(x) = x$, line L6 gives $g = -1$, line L5 gives $A = 2$, so $x^a = 1/2$, and the analysis error variance $A^{-1}$ is $1/2$.

**Wind speed.** The state is a wind $x = (u, v)$ with the background $x^b = (3, 4)$, so the background speed is 5. One instrument measures the speed only, $h(x) = \sqrt{u^2 + v^2}$, with $y^o = 6$ and $R = 1$. This $h$ is nonlinear.

With $B = I$ the minimum lies on the ray through $x^b$, at the speed $(5 + 6)/2 = 5.5$, so $x^a = (3.3, 4.4)$. Along that ray $h$ is linear, and the first outer loop lands on $x^a$ exactly.

With $B = \mathrm{diag}(1, 4)$ the background $v$ is less certain than $u$, so the analysis changes $v$ more. The outer iterates, from the reference code, are:

| outer loop | $u$ | $v$ | speed | $J(x)$ | distance to $x^a$ |
|---|---|---|---|---|---|
| 0 | 3.000000 | 4.000000 | 5.000000 | 0.500000000 | 8.4e-1 |
| 1 | 3.153061 | 4.816327 | 5.756631 | 0.124626817 | 2.1e-2 |
| 2 | 3.134954 | 4.824572 | 5.753645 | 0.124441540 | 1.3e-3 |
| 3 | 3.134090 | 4.825439 | 5.753901 | 0.124441010 | 8.0e-5 |
| 4 | 3.134038 | 4.825493 | 5.753918 | 0.124441008 | 4.9e-6 |
| 5 | 3.134035 | 4.825496 | 5.753920 | 0.124441008 | 3.0e-7 |

The distance shrinks by a factor of about 0.06 per outer loop (a measurement). This is linear, not quadratic, convergence: the final speed 5.754 does not match the observation 6, and $h$ is curved, so the Gauss-Newton Hessian of line L5 misses a term of the true Hessian. A grid search over the square $[2, 4] \times [3, 5]$ in the tests confirms that the limit is the global minimum.

## Correctness

The [proof](proofs/correctness.md) shows that $A$ is symmetric positive definite, so line L7 has a unique solution, and that line L8 moves to the exact minimizer of the cost with $h$ linearized at $x$. For a linear $h$ this is the cost itself, so the first outer loop returns $x^b + K(y^o - Hx^b)$, the Kalman and optimal interpolation analysis, and $A^{-1}$ is the analysis error covariance (a theorem). For a nonlinear $h$ each increment is a descent direction, and the loop stops with a zero increment only at a stationary point of $J$. It need not be the global minimum, and convergence from a poor background is not guaranteed.

## Complexity

The reference code factors $B$ and $R$ once by Cholesky in $\Theta(n^3 + p^3)$ time. Each conjugate gradient step costs one product $Av$, which is $\Theta(n^2 + np + p^2)$ with dense matrices, so $k$ outer loops of $m$ inner steps cost $\Theta(k m (n^2 + np + p^2))$ more. Operational systems, with $n$ of the order of $10^8$ or more, never store $B$. They apply $U$ with $B = UU^\top$ as a sequence of transforms (spectral or wavelet transforms, vertical modes, balance operators), each in about $\Theta(n \log n)$ time. The tangent linear $H$ and its adjoint $H^\top$ cost a small multiple of one evaluation of $h$. A few outer loops with some tens of inner steps each are usual (a rule of thumb, not a bound). With the control variable transform the inner Hessian is $I + U^\top H^\top R^{-1} H U$, whose eigenvalues are at least 1, which bounds the number of inner steps for a given accuracy in terms of the largest eigenvalue only.

## Properties

- **Same analysis as OI for a linear $H$.** The minimizer is $x^b + K d$ (a theorem). The two differ in what they compute: OI solves small systems in observation space for each grid value, and 3D-Var minimizes once over the whole state.
- **Global use of observations.** Every observation can influence every grid value through $B$, so the analysis has no jumps from data selection.
- **Nonlinear and indirect observations.** Only $h$, its tangent linear $H$ and its [adjoint](/adjoint-model/) $H^\top$ are needed, so radiances, refractivities and other indirect data can be used directly.
- **Fixed $B$.** The background covariance is the same every day, so the analysis increments do not follow the flow of the day. [4D-Var](/four-dimensional-variational-assimilation/) and hybrid ensemble methods address this.
- **Regularized least squares.** The cost is a [Tikhonov regularization](/tikhonov-regularization/) of the observation fit with the background as the prior and $B^{-1}$ as the penalty matrix.

## Variants and improvements

- **Control variable transform.** Minimize over $v$ with $x - x^b = Uv$ and $B = UU^\top$ (see [control variable transform](/control-variable-transform/)). This is how all operational 3D-Var systems are written.
- **Physical space analysis system (PSAS).** Solve $(HBH^\top + R)z = d$ in observation space and set $x^a = x^b + BH^\top z$. For a linear $H$ this is the same analysis, and it is cheaper when $p$ is much smaller than $n$ (Kalnay 2003, Section 5.5).
- **First guess at the appropriate time (FGAT).** Compute the departures of line L3 with the background at the time of each observation, while the increment stays valid at one time.
- **4D-Var.** Add the model as a link between the times of the window, so that the cost compares the model trajectory with the observations at their own times (see [4D-Var](/four-dimensional-variational-assimilation/) and [incremental 4D-Var](/incremental-4d-var/)).
- **Hybrid 3D-Var.** Replace $B$ by a weighted sum of the static $B$ and a localized ensemble covariance.

## When to use it

Use 3D-Var when the observations are many and of many kinds, some with a nonlinear operator, when a smooth global analysis is wanted, and when a good static model of $B$ exists. It is the standard choice for regional and limited area systems with short cycles and for systems where a tangent linear and adjoint of the forecast model are not available. If the errors of the day matter, use an ensemble or a four-dimensional method.

## Pitfalls

- **Inverse of $B$ in the code (line L6).** Applying $B^{-1}$ directly fails when $B$ is huge or nearly singular, and the inner problem is badly conditioned. Use the control variable transform, which needs $U$ only.
- **Wrong adjoint (line L5 and line L6).** If the code for $H^\top$ is not the exact transpose of the code for $H$, the conjugate gradient method fails to converge or converges to a wrong point. Check it with the dot product test $\langle Hv, w \rangle = \langle v, H^\top w\rangle$ to rounding error.
- **Departures from the wrong point (line L3).** In the incremental form, $d$ must be computed with the full nonlinear $h$ at the current $x$, not at $x^b$. Computing it once at $x^b$ freezes the outer loop at the first step.
- **Too few inner steps (line L7).** Stopping conjugate gradients early gives an increment that is not the minimizer of the inner problem. Then one outer loop is no longer exact for a linear $H$, and the analysis depends on the stopping rule.
- **Trusting one outer loop for a nonlinear $h$.** The first increment can be far from the minimum, and the full step can even increase $J$. Check the cost after line L8, and add outer loops or a line search.

## Implementations

## History

Sasaki proposed variational objective analysis in the late 1950s, with dynamical constraints imposed through a cost function. Lorenc showed in 1986 that the analysis of optimal interpolation is the minimizer of a cost function derived from Bayes' theorem, which opened the way to a variational method with nonlinear observation operators and without data selection. Parrish and Derber's spectral statistical interpolation, described in 1992, replaced optimal interpolation at the US National Meteorological Center, and ECMWF followed with its own 3D-Var in the mid 1990s, before moving to 4D-Var in 1997. The incremental form with outer and inner loops was proposed for 4D-Var by Courtier, Thepaut and Hollingsworth in 1994, and 3D-Var systems use the same structure.

## References
