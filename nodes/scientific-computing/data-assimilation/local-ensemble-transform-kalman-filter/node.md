---
tag: HEPB83
kind: algorithm
slug: local-ensemble-transform-kalman-filter
name: Local ensemble transform Kalman filter
aliases:
- LETKF
area: scientific-computing/data-assimilation
level: advanced
summary: "Runs an ETKF independently at each grid point with only nearby observations, which localizes and parallelizes the analysis."
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the number of grid values, N: the ensemble size, p: the number of observations, s: "the largest number of local observations of one grid value, written p_l in the text"}
  time: {worst: "Θ(N p + n (p + s^2 N + s^3))"}
  space: {extra: "Θ(N (n + p) + s N + s^2)"}
properties: {deterministic: true, perturbed_observations: false, localization: "R-localization with a Gaspari-Cohn weight", exact_local_kalman_moments: "for a linear H", parallel: "over grid points", mean_preserving: true}
history:
  year: 2007
  people: [Brian R. Hunt, Eric J. Kostelich, Istvan Szunyogh]
  note: "Ott and coauthors gave the local ensemble Kalman filter in 2004, and Hunt, Kostelich and Szunyogh gave the transform form, the LETKF, in Physica D in 2007."
prereqs: [ensemble-transform-kalman-filter, covariance-localization]
see_also: [gaspari-cohn-function, covariance-inflation, ensemble-adjustment-kalman-filter, ensemble-kalman-filter, local-particle-filter, lorenz-96-model, four-dimensional-ensemble-variational, hybrid-ensemble-variational]
sources:
  - paper: doi:10.1016/j.physd.2006.11.008
    title: "B. R. Hunt, E. J. Kostelich and I. Szunyogh, Efficient data assimilation for spatiotemporal chaos: a local ensemble transform Kalman filter, Physica D 230(1-2) (2007) 112-126"
    locator: "the derivation in ensemble space, the symmetric square root, the local analysis and the smooth increase of R with distance"
  - paper: doi:10.3402/tellusa.v56i5.14462
    title: "E. Ott, B. R. Hunt, I. Szunyogh, A. V. Zimin, E. J. Kostelich, M. Corazza, E. Kalnay, D. J. Patil and J. A. Yorke, A local ensemble Kalman filter for atmospheric data assimilation, Tellus A 56(5) (2004), from page 415"
    locator: the local ensemble Kalman filter, the predecessor of the LETKF
  - paper: doi:10.1111/j.1600-0870.2007.00274.x
    title: "I. Szunyogh, E. J. Kostelich, G. Gyarmati, E. Kalnay, B. R. Hunt, E. Ott, E. Satterfield and J. A. Yorke, A local ensemble transform Kalman filter data assimilation system for the NCEP global model, Tellus A 60(1) (2008), from page 113"
    locator: the application to a global weather model
  - paper: doi:10.1175/2010MWR3328.1
    title: "S. J. Greybush, E. Kalnay, T. Miyoshi, K. Ide and B. R. Hunt, Balance and ensemble Kalman filter localization techniques, Monthly Weather Review 139(2) (2011) 511-522"
    locator: the comparison of R-localization and B-localization
  - paper: doi:10.1002/qj.49712555417
    title: "G. Gaspari and S. E. Cohn, Construction of correlation functions in two and three dimensions, Quarterly Journal of the Royal Meteorological Society 125(554) (1999) 723-757"
    locator: "eq. (4.10), the compactly supported weight"
  - paper: doi:10.1137/140965363
    title: "E. Kwiatkowski and J. Mandel, Convergence of the square root ensemble Kalman filter in the large ensemble limit, SIAM/ASA Journal on Uncertainty Quantification 3(1) (2015) 1-17"
    locator: the large ensemble limit of the ETKF and other square root filters for linear models
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation used here
---

The local ensemble transform Kalman filter (LETKF) is the analysis step of an ensemble filter that works one grid point at a time. For each grid value it takes only the observations within a fixed distance, gives the far ones less weight by increasing their error variance, and solves the [ETKF](/ensemble-transform-kalman-filter/) problem in the $N$-dimensional space of the ensemble. The result at each point is a set of weights for the forecast members. Neighbouring points use almost the same observations, so their weights are almost the same and the analysis is smooth. Because the points are independent, the analysis runs in parallel on any number of processors, and the cost grows linearly with the size of the grid. It is one of the two standard ways to localize an ensemble filter, with the Schur product of [covariance localization](/covariance-localization/).

## In plain words

A forecast is made $N$ times with small changes, and the $N$ forecasts disagree a little. At one grid point, the filter looks at the observations close to that point and asks which mix of the $N$ forecasts matches them best. Observations that are a bit further away count less. The answer is a list of $N$ weights, and the new value at the point is the weighted mix of the forecasts. The filter also makes a new set of $N$ values, spread out by the right amount for the error that is left. Then it goes to the next point and does the same with the observations close to it. A far observation can not change the point, even if the small ensemble shows a false link between the two places.

## The problem

**Input.** A forecast ensemble $x_1, \ldots, x_N \in \mathbb R^n$ (the background, in the notation of Ide, Courtier, Ghil and Lorenc 1997), observations $y^o \in \mathbb R^p$ with independent errors of variances $r_k$ (a diagonal $R$), an observation operator $H$ that may be nonlinear, the positions of the grid values and of the observations, a distance, the half-width $c$ of the [Gaspari-Cohn](/gaspari-cohn-function/) weight, and a multiplicative inflation $\rho \ge 1$ of the covariance. In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, the model $M$ is its $A$, the forecast mean and covariance $x^f$ and $P^f$ are its predicted $m^-$ and $P^-$, and the analysis $x^a$ and $P^a$ are its filtered $m$ and $P$.

**Output.** An analysis ensemble $x^a_1, \ldots, x^a_N$. Component $j$ of its mean and of its sample variance should be the Kalman analysis of grid value $j$ from its local observations, with the inflated sample covariance $\rho P^f$ and the error variances $r_k / w_k$.

## The algorithm

$X$ and $Y$ hold the unscaled perturbations $x_i - \bar x$ and $H(x_i) - \bar y$, so $P^f = X X^\top/(N - 1)$. Write $\gamma = (N - 1)/\rho$. The matrix $S$ has one row for each local observation and $N$ columns.

```pseudo id=main
LETKF(x_1..x_N, y^o, H, r, c, rho)
L1  y_i <- H(x_i) for each i; ybar <- mean of y_i; Y <- [y_i - ybar]
L2  xbar <- mean of x_i; X <- [x_i - xbar]
L3  for each grid point j do
L4      L <- {k : dist(j, k) < 2c}; w_k <- GC(dist(j, k) / c) for k in L
L5      S <- rows sqrt(w_k / r_k) Y_k for k in L; d <- entries sqrt(w_k / r_k)(y^o_k - ybar_k)
L6      eigenpairs (σ_m, v_m) of S S^T; u_m <- S^T v_m / sqrt(σ_m) for σ_m > 0
L7      wbar <- P~ S^T d, where P~ = (γ I + S^T S)^-1 = I/γ + Σ_m (1/(γ + σ_m) - 1/γ) u_m u_m^T
L8      W <- sqrt(N - 1) P~^(1/2) = sqrt(ρ) I + Σ_m (sqrt((N - 1)/(γ + σ_m)) - sqrt(ρ)) u_m u_m^T
L9      x^a_{j,i} <- xbar_j + X_j (wbar + W_i) for each member i
L10 return x^a_1..x^a_N
```

Lines L1 and L2 apply the observation operator to each member once and form the perturbations. Line L4 picks the local observations. Line L5 scales each one by $\sqrt{w_k / r_k}$, which is the same as dividing its error variance by the weight $w_k \in (0, 1]$: a far observation looks less accurate, and it has no effect at distance $2c$ or more. This is R-localization. Lines L6 to L8 are the ETKF in ensemble space. Hunt, Kostelich and Szunyogh (2007) form the $N \times N$ matrix $\gamma I + Y_L^\top \tilde R^{-1} Y_L$ and find its eigenpairs. The code finds the eigenpairs of the smaller $p_l \times p_l$ matrix $S S^\top$ instead and applies $\tilde P$ and $W$ through them, which gives the same result. Line L9 is the only line that touches the state: row $j$ of $X$ times the weights.

## Example

Take two grid points at positions $0$ and $3$, two members $x_1 = (-1, -1)$ and $x_2 = (1, 1)$, one observation $y^o = 1$ of point $0$ with $r = 1$, $c = 2$ and $\rho = 1$. The sample covariance is $\begin{pmatrix} 2 & 2 \\ 2 & 2 \end{pmatrix}$: the two points look perfectly correlated, which is the kind of correlation that two members always show.

At point $0$ the weight is $1$. With $N = 2$, $\gamma = 1$, $S = (-1, 1)$, $\sigma = 2$, $u = (-1, 1)/\sqrt 2$ and $d = 1$. Then $\bar w = (-1, 1)/3$, the mean is $2/3$, and $W$ shrinks the perturbations by $1/\sqrt 3$. The members are $2/3 \mp 1/\sqrt 3 \approx 0.089$ and $1.244$, with sample variance $2/3$, which is the Kalman answer $(1 - K) P^f$ with $K = 2/3$.

At point $3$ the distance is $3 = 1.5 c$, and the Gaspari-Cohn weight is exactly $19/1152 \approx 0.0165$. The observation now acts as if its error variance were $1152/19 \approx 60.6$. The mean moves from $0$ to $19/595 \approx 0.032$ and the perturbations shrink by the factor $\sqrt{1152/1190} \approx 0.984$, so the members are about $-0.952$ and $1.016$. Without localization point $3$ would copy point $0$ exactly. The test file checks these numbers.

**A measurement.** On the [Lorenz-96 model](/lorenz-96-model/) with $n = 40$, $F = 8$, classical RK4 with step $0.05$, every other variable observed every $0.05$ time units with $R = I$, and $N = 20$ members started from states on the attractor, the reference code gives these mean analysis RMSE values over cycles 501 to 1500 (one seed, pure Python):

| half-width $c$ | $\rho = 1.02$ | $\rho = 1.05$ | $\rho = 1.1$ |
|---|---|---|---|
| 2 | 0.495 | 0.475 | 0.487 |
| 3 | 0.406 | 0.411 | 0.436 |
| 4 | 0.365 | 0.381 | 0.402 |
| 5 | 0.342 | | |
| 6 | 0.329 | | |

With $c = 4$ and no inflation the RMSE was $0.396$, and a second seed with $c = 4$, $\rho = 1.02$ gave $0.371$. The mean of the same ensemble run without observations had an RMSE of $3.71$ over the same cycles (a single free member, $5.13$), so all runs track the truth well below the target of $1$. In this setting a wider localization was better up to $c = 6$, the largest value tried. These are measurements for one model and one observing network, not general rules. The test file runs a short version with $N = 10$, $c = 2$, $\rho = 1.1$.

## Correctness

The [proof](proofs/correctness.md) shows that lines L6 to L8 compute $\tilde P$ and $W$ exactly from the small eigenproblem (Lemma 1), and that for a linear $H$ the mean and the sample variance at grid point $j$ are exactly the Kalman analysis with the inflated sample covariance and the error variances $r_k / w_k$ (Theorem 3, a theorem). The symmetric square root keeps the mean: $W \mathbf 1 = \sqrt\rho\,\mathbf 1$. A grid point with no local observations keeps $\bar x_j + \sqrt\rho\,(x_{i,j} - \bar x_j)$. Without localization the method is the global ETKF, so for a linear Gaussian model it converges to the Kalman filter as $N \to \infty$ (Kwiatkowski and Mandel 2015, a theorem). With localization there is no such result, and the benefit is a measurement.

## Complexity

Lines L1 and L2 cost $\Theta(N p)$ plus $N$ applications of $H$, and $\Theta(N n)$. For one grid point, line L4 costs $\Theta(p)$ with a plain scan (a spatial index brings this down to the number of local observations), line L6 costs $\Theta(p_l^2 N)$ to form $S S^\top$ and $\Theta(p_l^3)$ for a fixed number of Jacobi sweeps, and lines L7 to L9 cost $\Theta(p_l N)$, $\Theta(p_l N)$ and $\Theta(N)$. The total is $\Theta(N p + n(p + p_l^2 N + p_l^3))$ for one analysis, without the model runs. Forming the $N \times N$ matrices as in Hunt et al. (2007) costs $\Theta(p_l N^2 + N^3)$ for each point, which is better when $p_l > N$. The extra space is the perturbations and one local problem.

## Properties

- **No perturbed observations.** The analysis is deterministic for a given forecast ensemble, so it has no extra sampling noise from the observations.
- **Exact local moments.** For a linear $H$ each grid value gets exactly the Kalman mean and variance of its local problem.
- **Smooth in space.** The weights $w_k$ go to zero smoothly at distance $2c$, so the local problems of neighbouring points change smoothly. A hard cutoff makes the analysis jump.
- **Embarrassingly parallel.** Each grid point needs only $\bar x$, $X_j$, $Y$ and the local data, so the points can go to different processors without communication.
- **Nonlinear H allowed.** Only the values $H(x_i)$ are needed, never a Jacobian or an adjoint.
- **Low rank locally.** At each point the update stays in the span of the local forecast perturbations, but different points use different weights, so the global analysis is not limited to the span of the $N - 1$ global perturbations.

## Variants and improvements

- **LEKF.** The local ensemble Kalman filter of Ott et al. (2004) did the same analysis in a local basis of the perturbations on a patch of grid points, and used the patch only for its centre.
- **Hard cutoff.** Use all observations within a radius with weight $1$. This is simpler but makes the analysis less smooth.
- **4D-LETKF.** Use observations at several times within a window, with $Y$ taken from the forecasts at those times (Hunt et al. 2007).
- **Weight interpolation.** Compute $\bar w$ and $W$ only on a coarse set of points and interpolate them, which saves most of the work for a fine grid.
- **Adaptive inflation.** Estimate $\rho$ from the innovations at each point (see [covariance inflation](/covariance-inflation/)).
- **Ensemble-variational hybrids.** Use the same ensemble in a variational analysis (see [hybrid ensemble-variational](/hybrid-ensemble-variational/) and [4DEnVar](/four-dimensional-ensemble-variational/)).

## When to use it

Use the LETKF for large spatial models with many observations, such as weather, ocean and atmospheric chemistry models, when the observations have local effects and errors that can be taken as independent. It is a good choice when a parallel analysis is needed and when the observation operator has no tangent linear code. For observations that integrate over a deep column or a long path, such as satellite radiances, the position of an observation is not well defined and R-localization is harder to set up. For a small state, the global [ETKF](/ensemble-transform-kalman-filter/) is simpler.

## Pitfalls

- **Wrong scaling of the weight (line L5).** The weight must divide the error variance, so both the row of $Y$ and the innovation are multiplied by $\sqrt{w_k / r_k}$. Scaling only one of them gives an update that is not the Kalman update for any error variance.
- **Inflation by $\rho$ or by $\sqrt\rho$ (line L7).** Here $\rho$ multiplies the covariance, so the perturbations grow by $\sqrt\rho$. Mixing the two conventions gives an inflation that is too large or too small.
- **A non-symmetric square root (line L8).** A Cholesky factor of $\tilde P$ is also a square root, but it does not map $\mathbf 1$ to a multiple of $\mathbf 1$, so the members no longer have the right mean. Use the symmetric square root.
- **Too small a half-width (line L4).** If $c$ is smaller than the distance between observations, most points see one or no observation and the analysis has gaps. In the measurement above, $c = 2$ (an observation every second grid point) was the worst value tried.
- **Ill-conditioned weights.** The eigenvalues $\sigma_m$ can be very small. The code drops those below a relative tolerance, which is exact because their terms are zero.
- **Correlated observation errors.** The scaling of line L5 assumes a diagonal $R$. With correlated errors, use the local block of $R$ and localize it with care.

## Implementations

## History

Edward Ott, Brian Hunt, Istvan Szunyogh and their coauthors at the University of Maryland published the local ensemble Kalman filter in Tellus A in 2004. Hunt, Kostelich and Szunyogh then gave the transform form in ensemble space, with the symmetric square root and the smooth increase of the observation error with distance, in Physica D in 2007, and Szunyogh and coauthors tested it with the global model of the US National Centers for Environmental Prediction in 2008. Greybush and coauthors compared its R-localization with the Schur product localization of the covariance in 2011.

## References
