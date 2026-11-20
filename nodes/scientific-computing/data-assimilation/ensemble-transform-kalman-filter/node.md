---
tag: 5GQ96N
kind: algorithm
slug: ensemble-transform-kalman-filter
name: Ensemble transform Kalman filter
aliases:
- ETKF
area: scientific-computing/data-assimilation
level: advanced
summary: "Computes the analysis in the space spanned by the ensemble perturbations, with a symmetric square root transform of the ensemble."
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the size of the state, N: the ensemble size, p: the number of observations}
  time: {worst: "Θ(p^3 + p^2 N + p N^2 + N^3 + n N^2)"}
  space: {extra: "Θ(N^2 + p N + n N)"}
properties: {deterministic: true, perturbed_observations: false, exact_kalman_moments: "for a linear H, with the sample covariance", mean_preserving: "with the symmetric square root", analysis_in_ensemble_span: true}
history:
  year: 2001
  people: [Craig H. Bishop, Brian J. Etherton, Sharanya J. Majumdar]
  note: "Bishop, Etherton and Majumdar gave the ETKF in 2001 for adaptive sampling, and Wang, Bishop and Julier (2004) and Hunt, Kostelich and Szunyogh (2007) gave the mean preserving symmetric form."
prereqs: [ensemble-square-root-filter]
see_also: [local-ensemble-transform-kalman-filter, ensemble-adjustment-kalman-filter, ensemble-kalman-filter, covariance-inflation, kalman-filter, jacobi-eigenvalue-algorithm, sherman-morrison-formula, lorenz-96-model]
sources:
  - paper: doi:10.1175/1520-0493(2001)129<0420:ASWTET>2.0.CO;2
    title: "C. H. Bishop, B. J. Etherton and S. J. Majumdar, Adaptive sampling with the ensemble transform Kalman filter. Part I: Theoretical aspects, Monthly Weather Review 129(3) (2001) 420-436"
    locator: the transformation matrix of the ensemble perturbations from an eigendecomposition in ensemble space
  - paper: doi:10.1175/1520-0493(2004)132<1590:WIBAEO>2.0.CO;2
    title: "X. Wang, C. H. Bishop and S. J. Julier, Which is better, an ensemble of positive-negative pairs or a centered spherical simplex ensemble?, Monthly Weather Review 132(7) (2004) 1590-1605"
    locator: the condition that the transform keeps the ensemble mean, and a centered form of the ETKF
  - paper: doi:10.1016/j.physd.2006.11.008
    title: "B. R. Hunt, E. J. Kostelich and I. Szunyogh, Efficient data assimilation for spatiotemporal chaos: a local ensemble transform Kalman filter, Physica D 230(1-2) (2007) 112-126"
    locator: "the analysis in ensemble space with P~ = ((N - 1)I/rho + Y^T R^-1 Y)^-1 and the symmetric square root"
  - paper: doi:10.1175/1520-0493(2003)131<1485:ESRF>2.0.CO;2
    title: "M. K. Tippett, J. L. Anderson, C. H. Bishop, T. M. Hamill and J. S. Whitaker, Ensemble square root filters, Monthly Weather Review 131(7) (2003) 1485-1490"
    locator: the ETKF as one of the ensemble square root filters
  - paper: doi:10.1175/2007MWR2021.1
    title: "P. Sakov and P. R. Oke, Implications of the form of the ensemble transformation in the ensemble square root filters, Monthly Weather Review 136(3) (2008) 1042-1053"
    locator: the transforms that keep the mean, and the symmetric solution
  - paper: doi:10.1137/140965363
    title: "E. Kwiatkowski and J. Mandel, Convergence of the square root ensemble Kalman filter in the large ensemble limit, SIAM/ASA Journal on Uncertainty Quantification 3(1) (2015) 1-17"
    locator: convergence of the ETKF to the Kalman filter as N goes to infinity, for linear models
  - book: isbn:9783642037108
    title: "Geir Evensen, Data Assimilation: The Ensemble Kalman Filter, 2nd edition, Springer, 2009"
    locator: "Chapter 13, Square root analysis schemes"
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation used here
---

The ensemble transform Kalman filter (ETKF) is an [ensemble square root filter](/ensemble-square-root-filter/) that does all of its algebra in the space of the ensemble. It writes each analysis member as the forecast mean plus a combination of the $N$ forecast perturbations, and it finds the coefficients from one $N \times N$ symmetric eigenproblem. The coefficients of the mean give the Kalman update of the mean, and a symmetric square root gives perturbations with exactly the Kalman analysis covariance of the sample prior. It uses no perturbed observations. Because $N$ is usually much smaller than the size of the state, the cost of the analysis is small, and the form is the basis of the [LETKF](/local-ensemble-transform-kalman-filter/).

## In plain words

Run a model $N$ times from slightly different starts. Every forecast is the average forecast plus a difference. The ETKF says that the corrected forecasts should be the average plus mixes of these same differences. It then only has to find $N$ numbers for the new average and an $N \times N$ table of numbers for the new members, which is a small problem even when each forecast has millions of values. The table is chosen in a special symmetric way, so that the new members are spread out by exactly the right amount and their average stays where the Kalman filter puts it.

## The problem

**Input.** A forecast ensemble $x_1, \ldots, x_N \in \mathbb R^n$, observations $y^o \in \mathbb R^p$ with error covariance $R$, an observation operator $H$ (it may be nonlinear), and a multiplicative inflation $\rho \ge 1$ of the covariance. The notation is that of Ide, Courtier, Ghil and Lorenc (1997). In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, the model $M$ is its $A$, the forecast $x^f$ and $P^f$ are its predicted $m^-$ and $P^-$, and the analysis $x^a$ and $P^a$ are its filtered $m$ and $P$.

**Output.** An analysis ensemble $x^a_1, \ldots, x^a_N$ whose mean is $\bar x + K(y^o - H\bar x)$ and whose sample covariance is $(I - KH)\rho P^f$, where $P^f$ is the sample covariance of the forecast and $K = \rho P^f H^\top(H\rho P^f H^\top + R)^{-1}$ (for a linear $H$).

## The algorithm

$X$ and $Y$ are the unscaled perturbations, so $P^f = X X^\top/(N - 1)$.

```pseudo id=main
ETKF(x_1..x_N, y^o, H, R, rho)
L1  xbar <- mean of x_i; X <- [x_1 - xbar, ..., x_N - xbar]
L2  y_i <- H(x_i); ybar <- mean of y_i; Y <- [y_1 - ybar, ..., y_N - ybar]
L3  C <- Y^T R^-1                                   ▷ N x p
L4  A <- (N - 1)/rho I + C Y                        ▷ N x N, symmetric positive definite
L5  Q, Λ <- eigendecomposition of A
L6  P~ <- Q Λ^-1 Q^T; W <- Q ((N - 1) Λ^-1)^(1/2) Q^T
L7  wbar <- P~ C (y^o - ybar)
L8  x^a_i <- xbar + X (wbar + W_i) for each member i
L9  return x^a_1..x^a_N
```

Line L2 is the only place that uses the observation operator, and it calls it once for each member. Line L4 is the inverse of the analysis covariance in ensemble space: the prior part $(N - 1)/\rho\, I$ plus the information from the observations. Line L6 takes the inverse and the symmetric square root from the same eigenpairs. Line L7 gives the weights of the mean and line L8 the members. The code uses the cyclic Jacobi method for line L5. With a diagonal $R$, line L3 is a scaling of the rows of $Y$.

## Example

Take one variable, two members $x_1 = -1$ and $x_2 = 1$, $H = 1$, $R = 1$, $\rho = 1$ and $y^o = 1$. Then $\bar x = 0$, $X = Y = (-1, 1)$, $P^f = 2$ and the Kalman gain is $K = 2/3$.

Line L4 gives $A = \begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$, with the eigenvalue $1$ on $(1, 1)/\sqrt 2$ and $3$ on $(1, -1)/\sqrt 2$. So $\tilde P = \tfrac13\begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}$ and line L7 gives $\bar w = (-1/3, 1/3)$, so the mean is $X\bar w = 2/3$. Line L6 gives

$$W = \frac12\begin{pmatrix} 1 + 1/\sqrt 3 & 1 - 1/\sqrt 3 \\ 1 - 1/\sqrt 3 & 1 + 1/\sqrt 3\end{pmatrix},$$

and the members are $2/3 \mp 1/\sqrt 3 \approx 0.089$ and $1.244$, with the sample variance $2/3 = (1 - K)P^f$. The rows of $W$ sum to $1$, so the mean stays at $2/3$. If $W$ is replaced by the Cholesky factor of $\tilde P$, the members become $2/3 - 1/\sqrt 6$ and $2/3 + 1/\sqrt 2$, and their mean moves to about $0.816$. With $x = \mp 1/\sqrt 2$ (sample mean $0$, variance $1$) the analysis has the mean $1/2$ and the variance $1/2$, the check value of the posterior of a $N(0, 1)$ prior with $y = 1$ and $R = 1$.

**A measurement.** On the [Lorenz-96 model](/lorenz-96-model/) with $n = 40$, $F = 8$, RK4 with step $0.05$, every other variable observed every $0.05$ time units with $R = I$, the reference code without localization gave these mean analysis RMSE values over cycles 501 to 1500 (one seed):

| $N$ | $\rho = 1.02$ | $1.05$ | $1.1$ | $1.2$ | $1.3$ | $1.5$ |
|---|---|---|---|---|---|---|
| 20 | 4.54 | 4.21 | 1.21 | 0.409 | 0.472 | 0.606 |
| 40 | 0.275 | 0.298 | | | | |

With $N = 20$ the filter loses the truth unless the inflation is large, and the RMSE of $4.5$ is worse than the $3.7$ of the mean of a free ensemble. With $N = 40$ it works with little inflation. The LETKF with $N = 20$ reached $0.33$ with localization on the same problem.

## Correctness

The [proof](proofs/correctness.md) shows that $A$ is positive definite with eigenvalues at least $(N - 1)/\rho$, so every step is defined (Lemma 1). The symmetric square root maps the vector of ones to $\sqrt\rho$ times itself, so the members keep the mean (Lemma 2). For a linear $H$ the analysis ensemble has exactly the mean $\bar x + K d$ and the sample covariance $(I - KH)\rho P^f$ (Theorem 4, a theorem), and every member stays in $\bar x$ plus the span of the forecast perturbations. For a linear Gaussian model the ETKF converges to the Kalman filter as $N \to \infty$ (Kwiatkowski and Mandel 2015). For finite $N$ and a nonlinear model there is no such guarantee.

## Complexity

Line L3 costs $\Theta(p^3 + p^2 N)$ with a dense $R$ (one factorization and $N$ solves) and $\Theta(p N)$ with a diagonal $R$. Line L4 costs $\Theta(p N^2)$, line L5 $\Theta(N^3)$ for a fixed number of Jacobi sweeps, line L6 $\Theta(N^3)$, line L7 $\Theta(p N + N^2)$ and line L8 $\Theta(n N^2)$. The total is $\Theta(p^3 + p^2 N + p N^2 + N^3 + n N^2)$, without the $N$ model runs and the $N$ applications of $H$. The cost is linear in $n$ and in $p$ for a diagonal $R$, which is why the method suits large models. The extra space is $\Theta(N^2 + pN + nN)$ for $A$, $W$, $Y$ and $X$.

## Properties

- **Deterministic.** For a given forecast ensemble the result is fixed, with no sampling noise from perturbed observations.
- **Exact second moments.** For a linear $H$, the mean and covariance of the members are exactly the Kalman values for the sample covariance.
- **Mean preserving.** The symmetric square root keeps the mean of the members equal to the analysis mean.
- **Low rank.** The analysis stays in the span of the forecast perturbations, so observations can only correct $N - 1$ directions.
- **Linear in the state.** Line L8 is one $n \times N$ by $N \times N$ product, so the members can be updated in place, block by block.
- **Same as the other square root filters.** The EnSRF of Whitaker and Hamill and the [EAKF](/ensemble-adjustment-kalman-filter/) give the same mean and covariance; they differ in the choice of the orthogonal factor (Tippett et al. 2003).

## Variants and improvements

- **The original form.** Bishop, Etherton and Majumdar (2001) used the eigendecomposition $C\Gamma C^\top$ of the scaled $Y^\top R^{-1} Y$ and the transform $C(\Gamma + I)^{-1/2}$. Wang, Bishop and Julier (2004) showed that it does not always keep the mean and gave a centered form. Multiplying the transform by $C^\top$ on the right gives the symmetric square root used here.
- **LETKF.** Do the analysis for each grid point with the nearby observations only ([LETKF](/local-ensemble-transform-kalman-filter/)), which adds localization at almost no cost.
- **Inflation.** Multiply $P^f$ by $\rho$ as in line L4, or use the relaxation methods of [covariance inflation](/covariance-inflation/).
- **Transforms for the smoother.** The same weights apply to past states, which gives an ensemble smoother at the cost of line L8 for each stored time (see the [ensemble Kalman smoother](/ensemble-kalman-smoother/)).
- **Random rotations.** The transform can be followed by a random orthogonal $U$ with $U\mathbf 1 = \mathbf 1$, which keeps the moments and changes the higher order statistics.

## When to use it

Use the ETKF for a model with a modest number of observations or as the building block of the LETKF, when the observation errors are known and the observation operator can be evaluated but not linearized. It is a good choice when a deterministic analysis without sampling noise is wanted. When the ensemble is small compared with the number of growing directions of the model, the global ETKF needs strong inflation or fails, as in the measurement above. Then use a localized filter such as the LETKF or the EnKF with [covariance localization](/covariance-localization/).

## Pitfalls

- **A triangular square root (line L6).** A Cholesky factor of $\tilde P$ has the right product but moves the mean of the members, as in the example. Use the symmetric square root.
- **Scaled and unscaled perturbations (line L4).** With $X$ divided by $\sqrt{N - 1}$ the prior term becomes $I/\rho$ and $W = \tilde P^{1/2}$. Mixing the two conventions gives a covariance that is wrong by the factor $N - 1$.
- **Inflation of the perturbations or of the covariance (line L4).** Here $\rho$ multiplies the covariance. If $\rho$ is meant for the perturbations, use $\rho^2$.
- **Too few members.** With $N - 1$ smaller than the number of unstable directions, the filter can diverge. The spread becomes small, the filter ignores the observations, and the error grows.
- **A nonlinear H.** The update uses the linear regression of the predicted observations on the state. For a strongly nonlinear $H$ the analysis can be poor, and an iterative ensemble method is better.

## Implementations

## History

Craig Bishop, Brian Etherton and Sharanya Majumdar introduced the ETKF in 2001 to predict how much targeted extra observations would reduce the forecast error. Tippett, Anderson, Bishop, Hamill and Whitaker (2003) showed that it, the EAKF and the EnSRF are square root filters that differ only in the choice of the square root. Wang, Bishop and Julier (2004) showed that the original transform does not always keep the mean and gave a centered form. Hunt, Kostelich and Szunyogh (2007) wrote the analysis with the symmetric square root in the form used here and made it local, and Sakov and Oke (2008) studied which transforms keep the mean.

## References
