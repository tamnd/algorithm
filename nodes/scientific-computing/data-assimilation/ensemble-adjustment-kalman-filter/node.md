---
tag: NP9ZCK
kind: algorithm
slug: ensemble-adjustment-kalman-filter
name: Ensemble adjustment Kalman filter
aliases:
- EAKF
area: scientific-computing/data-assimilation
level: advanced
summary: Adjusts the ensemble members by a linear map so the analysis ensemble has exactly the Kalman posterior mean and covariance of the sample prior.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the size of the state, N: the ensemble size, p: the number of observations}
  time: {worst: "Θ(p N (n + p))"}
  space: {extra: "Θ(N (n + p))"}
properties: {deterministic: true, perturbed_observations: false, exact_kalman_moments: "for a linear H, without localization", serial: "one scalar observation at a time, in observation space", same_members_as: "the serial EnSRF, for a linear H and a diagonal R"}
history:
  year: 2001
  people: [Jeffrey L. Anderson]
  note: "Anderson gave the adjustment matrix in 2001 and the two step serial form, an update in observation space followed by a regression, in 2003."
prereqs: [ensemble-square-root-filter]
see_also: [ensemble-kalman-filter, ensemble-transform-kalman-filter, local-ensemble-transform-kalman-filter, kalman-filter, covariance-localization, covariance-inflation, gaspari-cohn-function, lorenz-96-model]
sources:
  - paper: doi:10.1175/1520-0493(2001)129<2884:AEAKFF>2.0.CO;2
    title: "J. L. Anderson, An ensemble adjustment Kalman filter for data assimilation, Monthly Weather Review 129(12) (2001) 2884-2903"
    locator: "the adjustment matrix A, and Appendix A for its existence and its computation with singular value decompositions"
  - paper: doi:10.1175/1520-0493(2003)131<0634:ALLSFF>2.0.CO;2
    title: "J. L. Anderson, A local least squares framework for ensemble filtering, Monthly Weather Review 131(4) (2003) 634-642"
    locator: "the two step update: the scalar update in observation space and the regression onto the state"
  - paper: doi:10.1175/1520-0493(2003)131<1485:ESRF>2.0.CO;2
    title: "M. K. Tippett, J. L. Anderson, C. H. Bishop, T. M. Hamill and J. S. Whitaker, Ensemble square root filters, Monthly Weather Review 131(7) (2003) 1485-1490"
    locator: the EAKF as a square root filter and the nonuniqueness of the square root
  - paper: arxiv:2006.02941
    title: "I. Grooms, A note on the formulation of the ensemble adjustment Kalman filter, arXiv:2006.02941 (2020)"
    locator: the adjustment matrix when the forecast covariance is singular
  - paper: doi:10.1137/140965363
    title: "E. Kwiatkowski and J. Mandel, Convergence of the square root ensemble Kalman filter in the large ensemble limit, SIAM/ASA Journal on Uncertainty Quantification 3(1) (2015) 1-17"
    locator: convergence of the EAKF to the Kalman filter as N goes to infinity, for linear models
  - book: isbn:9783642037108
    title: "Geir Evensen, Data Assimilation: The Ensemble Kalman Filter, 2nd edition, Springer, 2009"
    locator: "Chapter 13, Square root analysis schemes"
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation used here
---

The ensemble adjustment Kalman filter (EAKF) of Anderson (2001) is an ensemble Kalman filter without perturbed observations. It moves the ensemble mean with the Kalman gain and maps each forecast perturbation to an analysis perturbation with one linear map, the adjustment matrix $A$. The map is chosen so that the analysis ensemble has exactly the Kalman mean and covariance for the sample covariance of the forecast. In practice the filter is used in the serial two step form of Anderson (2003): for each scalar observation it first adjusts the ensemble of the predicted observation, and then it carries the increments to the state by linear regression. It is one of the [ensemble square root filters](/ensemble-square-root-filter/), and for a linear $H$ the serial form gives the same members as the serial EnSRF.

## In plain words

Look at one observed number. Each member predicts a value for it, so the members give a small cloud of predicted values. The filter first moves this cloud to where Bayes' rule says it should be: it shifts the centre towards the data and shrinks the cloud about the new centre by a fixed factor. It does not add noise, and the order of the members stays the same. Then each member changes every other value by the amount that a straight line fit from the observed value predicts. A value that varies together with the observed one moves a lot, and a value with no relation to it does not move.

## The problem

**Input.** A forecast ensemble $x_1, \ldots, x_N \in \mathbb R^n$, observations $y^o \in \mathbb R^p$ with an observation operator $H$, and the error variances $r_k$ of independent observation errors (a diagonal $R$) for the serial form, or a full error covariance $R$ and a linear $H$ for the joint form. The serial form takes optional localization weights. The notation is that of Ide, Courtier, Ghil and Lorenc (1997). In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, the model $M$ is its $A$, the forecast $x^f$ and $P^f$ are its predicted $m^-$ and $P^-$, and the analysis $x^a$ and $P^a$ are its filtered $m$ and $P$. The adjustment matrix $A$ of this page is not the model.

**Output.** An analysis ensemble with mean $\bar x + K(y^o - H\bar x)$ and sample covariance $(I - KH)P^f$, where $P^f$ is the sample covariance of the forecast and $K = P^f H^\top(HP^fH^\top + R)^{-1}$ (for a linear $H$ and no localization).

## The algorithm

The serial form keeps an ensemble of predicted observations $y_i$ next to the state ensemble and processes one scalar observation at a time.

```pseudo id=main
EAKF-SERIAL(x_1..x_N, y^o, H, r)
L1  y_i <- H(x_i) for each member i                   ▷ the only use of H
L2  for k <- 1 to p do
L3      ybar <- mean of y_ik; s <- sample variance of y_ik
L4      s^a <- 1 / (1/s + 1/r_k); y^a <- s^a (ybar/s + y^o_k/r_k)
L5      Δy_i <- y^a + sqrt(s^a/s) (y_ik - ybar) - y_ik     ▷ adjust in observation space
L6      b_x <- cov(x, y_k) / s; x_i <- x_i + b_x Δy_i       ▷ regression onto the state
L7      b_y <- cov(y, y_k) / s; y_i <- y_i + b_y Δy_i       ▷ and onto the other observations
L8  return x_1..x_N
```

Line L4 is the posterior of a scalar Gaussian prior $N(\bar y, s)$ after an observation with error variance $r_k$. Line L5 moves the predicted values so that they have exactly this mean and variance, by a shift and a shrink about the mean. Lines L6 and L7 compute the regression coefficients from the values before the update. With localization, $b_x$ and $b_y$ are multiplied entry by entry by the weights of observation $k$. An observation with $s = 0$ carries no information about the ensemble and is skipped.

The joint form of Anderson (2001) treats all observations together for a linear $H$ and any positive definite $R$.

```pseudo id=joint
EAKF-JOINT(x_1..x_N, y^o, H, R)
J1  xbar, X <- mean and perturbations of x_i; P <- X X^T / (N - 1)
J2  P = F D F^T with the positive eigenvalues only; G <- D^(1/2)
J3  M <- G F^T H^T R^-1 H F G = U Λ U^T
J4  A <- F G U (I + Λ)^(-1/2) U^T G^-1 F^T             ▷ the adjustment matrix
J5  x^a <- xbar + P H^T (H P H^T + R)^-1 (y^o - H xbar)
J6  return x^a_i <- x^a + A X_i for each member i
```

Line J2 keeps only the positive eigenvalues of $P$, so that $G$ can be inverted. This matters because $P$ has rank at most $N - 1$, which is usually smaller than $n$.

## Example

Take three members with two values each, $x_1 = (0, 1)$, $x_2 = (1, 3)$ and $x_3 = (2, 2)$. The first value is observed, $y^o = 2$ with $r = 1/3$. The predicted values are $(0, 1, 2)$, so $\bar y = 1$ and $s = 1$. Line L4 gives $s^a = 1/4$ and $y^a = \tfrac14(1 + 6) = 7/4$, and the shrink factor is $\sqrt{1/4} = 1/2$. Line L5 moves the predicted values to $(5/4, 7/4, 9/4)$, so the increments are $\Delta y = (5/4, 3/4, 1/4)$.

The second value $(1, 3, 2)$ has the covariance $1/2$ with the first value, so $b_x = (1, 1/2)$. The analysis members are $(5/4, 13/8)$, $(7/4, 27/8)$ and $(9/4, 17/8)$. The second value has the mean $19/8$ and the variance $13/16$. The Kalman update with the sample covariance gives the gain $K = (3/4, 3/8)$, the same mean $2 + 3/8 = 19/8$ and the same variance $1 - \tfrac38\cdot\tfrac12 = 13/16$.

For the check value of the page group: with two members $\mp 1/\sqrt 2$, $y^o = 1$ and $r = 1$, both forms return the mean $1/2$ and the variance $1/2$ to rounding.

**A measurement.** On the [Lorenz-96 model](/lorenz-96-model/) with $n = 40$, $F = 8$, RK4 with step $0.05$, every other variable observed every $0.05$ time units with $R = I$, $N = 20$, multiplicative inflation $\rho = 1.02$ of the forecast covariance and a [Gaspari-Cohn](/gaspari-cohn-function/) weight with half-width $4$ grid units on $b_x$ and $b_y$, the serial EAKF had the mean analysis RMSE $0.373$ over cycles 501 to 1500 (one seed). In every cycle its members differed from those of the serial EnSRF, run from the same forecast, by at most $1.3 \cdot 10^{-14}$. This is Lemma 2 of the proof, which also holds with localization.

## Correctness

The [proof](proofs/correctness.md) shows that line L5 gives the predicted values the Gaussian posterior mean and variance (Lemma 1). The regression of lines L6 and L7 then makes exactly the update $x_i + Kd - \alpha K (Y_k)_i$ of the serial EnSRF, with $\alpha = 1/(1 + \sqrt{r/(s + r)})$ (Lemma 2). So for a linear $H$ and a diagonal $R$ the serial EAKF has the Kalman mean and covariance (Theorem 3). For the joint form, $APA^\top = (I - KH)P$ by the Woodbury identity (Lemma 4), so the members of line J6 have the Kalman mean and covariance for any positive definite $R$ (Theorem 5). For one scalar observation the two forms give the same members (Corollary 6). These are theorems. As $N \to \infty$ for a linear Gaussian model the filter converges to the Kalman filter (Kwiatkowski and Mandel 2015). With localization or a nonlinear $H$ the update is a heuristic.

## Complexity

Each pass of the serial loop costs $\Theta(N(n + p))$ for lines L6 and L7 and $\Theta(N)$ for the rest, so the analysis costs $\Theta(pN(n + p))$ plus $N$ applications of $H$. With localization only the values with a nonzero weight need work. The extra space is the observation ensemble and the copy of the state ensemble, $\Theta(N(n + p))$. The joint form needs the $n \times n$ matrix $P$ and two eigendecompositions, about $\Theta(n^3 + n^2(N + p) + p^3)$ time and $\Theta(n^2 + p^2)$ space. It is useful for checks and small problems, not for large models.

## Properties

- **No perturbed observations.** The update is deterministic, so it adds no sampling noise from random observations.
- **Exact second moments.** For a linear $H$ and no localization, the analysis mean and covariance are the Kalman values for the sample covariance. The serial form needs a diagonal $R$ for this.
- **Order of the members is kept.** Line L5 shifts and shrinks the predicted values without reordering them, so each analysis member stays close to its forecast member.
- **Same members as the serial EnSRF.** For a linear $H$ the two serial filters are the same algorithm written in two ways, also with localization of the gain.
- **A square root filter.** The EAKF, the [ETKF](/ensemble-transform-kalman-filter/) and the EnSRF give the same mean and covariance. Their members differ by an orthogonal transform in ensemble space (Tippett et al. 2003).
- **Low rank.** The analysis stays in the span of the forecast perturbations.

## Variants and improvements

- **Other adjustments in observation space.** Line L5 can be replaced by any rule that gives the predicted values new values from a scalar posterior. Anderson (2003) uses this freedom: the perturbed observation [EnKF](/ensemble-kalman-filter/) is the same two step scheme with a random update in line L5.
- **Localization.** Multiply $b_x$ and $b_y$ by a [Gaspari-Cohn](/gaspari-cohn-function/) weight of the distance between the observation and each value. This is [covariance localization](/covariance-localization/) of the gain.
- **Inflation.** The filter is usually run with [covariance inflation](/covariance-inflation/) of the forecast ensemble, as in the measurement above.
- **Joint transform in ensemble space.** The [ETKF](/ensemble-transform-kalman-filter/) computes an $N \times N$ transform instead of the $n \times n$ matrix $A$, which is much cheaper when $N \ll n$. The [LETKF](/local-ensemble-transform-kalman-filter/) does this for each grid point.

## When to use it

Use the serial EAKF when the observation errors are independent, when the observation operators are nonlinear or complex and should be run only once for each member, and when localization by distance is needed. Its update of the predicted observations makes it easy to add new kinds of observations. For problems with very many observations on a parallel computer the serial loop is a bottleneck, and the [LETKF](/local-ensemble-transform-kalman-filter/) is easier to run in parallel. Use the joint form only for small problems or to check other code.

## Pitfalls

- **Forgetting to update the predicted observations (line L7).** Without line L7, each later observation uses a prior that does not include the earlier ones, and their information is counted twice.
- **Using updated values in the regression (lines L6 and L7).** The coefficients must use the predicted values before line L5 is applied. Using the adjusted values gives the wrong increments.
- **Inverting a singular $P$ (line J2).** With $N \le n$ the forecast covariance is singular. Keep only the positive eigenvalues, or $G^{-1}$ does not exist.
- **Correlated errors in the serial form.** The serial form needs a diagonal $R$. For correlated errors, first transform the observations with a square root of $R$, or use the joint form.
- **Spread collapse.** As with every ensemble filter with few members, the filter underestimates its error. Without [inflation](/covariance-inflation/) or localization it can stop using the data.

## Implementations

## History

Anderson introduced the filter in 2001 for atmospheric models. His paper defined the adjustment matrix and showed in an appendix how to compute it with singular value decompositions. In 2003 he described the serial form as a least squares framework: a scalar update in observation space followed by a regression onto each state value. In the same year Tippett, Anderson, Bishop, Hamill and Whitaker showed that the EAKF, the ETKF and the filter of Whitaker and Hamill are all square root filters.

## References
