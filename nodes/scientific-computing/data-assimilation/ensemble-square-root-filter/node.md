---
tag: W0YQYW
kind: algorithm
slug: ensemble-square-root-filter
name: Ensemble square root filter
aliases:
- EnSRF
- deterministic ensemble Kalman filter
area: scientific-computing/data-assimilation
level: advanced
summary: "Updates the ensemble mean by the Kalman gain and the perturbations by a deterministic transform, with no perturbed observations."
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the size of the state, N: the ensemble size, p: the number of observations}
  time: {worst: "Θ(p N (n + p))"}
  space: {extra: "Θ(N (n + p))"}
properties: {deterministic: true, perturbed_observations: false, exact_kalman_moments: "for a linear H and a diagonal R, without localization", serial: "one scalar observation at a time", reduced_gain: "alpha = 1/(1 + sqrt(r/(s + r)))"}
history:
  year: 2002
  people: [Jeffrey S. Whitaker, Thomas M. Hamill]
  note: "Whitaker and Hamill gave the serial ensemble square root filter in 2002, and Tippett and coauthors put it with the ETKF and the EAKF into one family of square root filters in 2003."
prereqs: [ensemble-kalman-filter]
see_also: [ensemble-transform-kalman-filter, ensemble-adjustment-kalman-filter, local-ensemble-transform-kalman-filter, covariance-localization, covariance-inflation, kalman-filter, cholesky-decomposition, lorenz-96-model]
sources:
  - paper: doi:10.1175/1520-0493(2002)130<1913:EDAWPO>2.0.CO;2
    title: "J. S. Whitaker and T. M. Hamill, Ensemble data assimilation without perturbed observations, Monthly Weather Review 130(7) (2002) 1913-1924"
    locator: "the serial square root update with the reduced gain alpha K, and the sampling error that perturbed observations add"
  - paper: doi:10.1175/1520-0493(2003)131<1485:ESRF>2.0.CO;2
    title: "M. K. Tippett, J. L. Anderson, C. H. Bishop, T. M. Hamill and J. S. Whitaker, Ensemble square root filters, Monthly Weather Review 131(7) (2003) 1485-1490"
    locator: the common form of the square root filters and the nonuniqueness of the square root
  - paper: doi:10.1175/1520-0493(2003)131<0634:ALLSFF>2.0.CO;2
    title: "J. L. Anderson, A local least squares framework for ensemble filtering, Monthly Weather Review 131(4) (2003) 634-642"
    locator: serial processing of scalar observations by regression on the observed variable
  - paper: doi:10.1175/1520-0493(2001)129<0123:ASEKFF>2.0.CO;2
    title: "P. L. Houtekamer and H. L. Mitchell, A sequential ensemble Kalman filter for atmospheric data assimilation, Monthly Weather Review 129(1) (2001) 123-137"
    locator: sequential processing of batches of observations with a localized gain
  - paper: doi:10.1111/j.1600-0870.2007.00299.x
    title: "P. Sakov and P. R. Oke, A deterministic formulation of the ensemble Kalman filter: an alternative to ensemble square root filters, Tellus A 60(2) (2008), from page 361"
    locator: "the DEnKF, a different scheme that uses the name deterministic EnKF"
  - paper: doi:10.1137/140965363
    title: "E. Kwiatkowski and J. Mandel, Convergence of the square root ensemble Kalman filter in the large ensemble limit, SIAM/ASA Journal on Uncertainty Quantification 3(1) (2015) 1-17"
    locator: convergence of the square root filters to the Kalman filter as N goes to infinity, for linear models
  - book: isbn:9783642037108
    title: "Geir Evensen, Data Assimilation: The Ensemble Kalman Filter, 2nd edition, Springer, 2009"
    locator: "Chapter 13, Square root analysis schemes"
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation used here
---

An ensemble square root filter is an ensemble Kalman filter that does not perturb the observations. It moves the ensemble mean with the Kalman gain, like the [EnKF](/ensemble-kalman-filter/), and it changes the perturbations about the mean by a deterministic linear map, chosen so that their sample covariance is exactly the Kalman analysis covariance. The name comes from that map: it is a square root of the analysis covariance written in terms of the forecast perturbations. This page gives the serial form of Whitaker and Hamill (2002), which takes one scalar observation at a time and needs only one extra scalar, the reduced gain factor $\alpha$. The [ETKF](/ensemble-transform-kalman-filter/) and the [EAKF](/ensemble-adjustment-kalman-filter/) are other members of the same family.

## In plain words

Think of the ensemble as a cloud of points around its centre. An observation should move the centre towards the data and should make the cloud smaller, because we now know more. The perturbed observation EnKF does this by giving each point its own noisy copy of the data, which adds random noise to the result. The square root filter moves the centre by the usual Kalman amount and then shrinks the cloud by an exact factor, the same for every member, so the cloud has the right size without any added noise. With one number observed at a time, the shrink factor is a simple formula in the spread of the ensemble at the observation and the error of the observation.

## The problem

**Input.** A forecast ensemble $x_1, \ldots, x_N \in \mathbb R^n$, observations $y^o \in \mathbb R^p$ whose errors are independent with variances $r_k$ (a diagonal $R$), an observation operator $H$, and optional localization weights between each observation and each state value or other observation. The notation is that of Ide, Courtier, Ghil and Lorenc (1997). In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, the model $M$ is its $A$, the forecast $x^f$ and $P^f$ are its predicted $m^-$ and $P^-$, and the analysis $x^a$ and $P^a$ are its filtered $m$ and $P$.

**Output.** An analysis ensemble with mean $\bar x + K(y^o - H\bar x)$ and sample covariance $(I - KH)P^f$, where $P^f$ is the sample covariance of the forecast and $K = P^f H^\top (H P^f H^\top + R)^{-1}$ (for a linear $H$ and no localization).

## The algorithm

$X$ and $Y$ hold the unscaled perturbations of the state and of the predicted observations, one row per variable. A correlated $R$ can first be made diagonal by a change of variables of the observations.

```pseudo id=main
EnSRF(x_1..x_N, y^o, H, r)
L1  xbar, X <- mean and perturbations of x_i; ybar, Y <- of y_i = H(x_i)
L2  for k <- 1 to p do                                ▷ one scalar observation at a time
L3      s <- Y_k Y_k^T / (N - 1)                      ▷ forecast variance of observation k
L4      b <- X Y_k^T / (N - 1); c <- Y Y_k^T / (N - 1) ▷ covariances with observation k (localized)
L5      K <- b / (s + r_k); K_y <- c / (s + r_k)
L6      alpha <- 1 / (1 + sqrt(r_k / (s + r_k)))
L7      d <- y^o_k - ybar_k
L8      xbar <- xbar + K d; ybar <- ybar + K_y d
L9      X <- X - alpha K Y_k; Y <- Y - alpha K_y Y_k
L10 return x^a_i <- xbar + X_i for each member i
```

Line L1 is the only place where the observation operator is used. After that the filter updates the predicted observations together with the state, which is exact for a linear $H$ and avoids running $H$ again. Lines L3 to L5 form the scalar Kalman gain from the ensemble. Line L6 is the factor that makes the perturbations shrink by the right amount. Line L8 moves the means with the full gain and line L9 moves the perturbations with the reduced gain $\alpha K$. With localization, line L4 multiplies $b$ and $c$ entry by entry by the weights of observation $k$.

## Example

Take a state with two values, two members $x_1 = (-1, 0)$ and $x_2 = (1, 2)$, both values observed, $y^o = (1, 2)$ and $r = (1, 1)$. The forecast mean is $(0, 1)$ and both values have the perturbations $\mp 1$, so $P^f = \begin{pmatrix} 2 & 2 \\ 2 & 2 \end{pmatrix}$.

The first observation has $s = 2$, $K = (2/3, 2/3)$, $d = 1$ and $\alpha = 1/(1 + 1/\sqrt 3)$. The mean moves to $(2/3, 5/3)$ and all perturbations shrink by the factor $1 - \alpha\cdot 2/3 = 1/\sqrt 3$. The predicted second observation moves to $5/3$ in the same step. The second observation then has $s = 2/3$, $K = (2/5, 2/5)$ and $d = 1/3$, so the mean moves to $(4/5, 9/5)$ and the perturbations shrink by $\sqrt{3/5}$ to $\mp 1/\sqrt 5$. The analysis covariance is $\tfrac25\begin{pmatrix} 1 & 1 \\ 1 & 1\end{pmatrix}$. The batch Kalman update with $P^f$ gives $K = \tfrac25 \begin{pmatrix} 1 & 1 \\ 1 & 1\end{pmatrix}$, the same mean and the same covariance, as Theorem 3 of the proof says.

For the check value of the page group: with two members $\mp 1/\sqrt 2$ (sample mean $0$, variance $1$), $y^o = 1$ and $r = 1$, the filter returns the mean $1/2$ and the variance $1/2$ to rounding.

**A measurement.** On the [Lorenz-96 model](/lorenz-96-model/) with $n = 40$, $F = 8$, RK4 with step $0.05$, every other variable observed every $0.05$ time units with $R = I$, $N = 20$, multiplicative inflation $\rho$ of the forecast covariance and a [Gaspari-Cohn](/gaspari-cohn-function/) weight with half-width $c$ grid units, the mean analysis RMSE over cycles 501 to 1500 was (one seed, about 3 ms for each analysis in pure Python):

| $c$ | 4 | 6 | 8 | 10 | 15 | none |
|---|---|---|---|---|---|---|
| $\rho = 1.02$ | 0.373 | 0.321 | 0.314 | 0.303 | 0.292 | 4.52 |

With $c = 4$ and $\rho = 1.05$ the RMSE was again $0.373$, and $N = 10$ with $c = 4$ and $\rho = 1.05$ gave $0.367$. Without localization the filter needed $\rho = 1.2$ to reach $0.409$, the same value as the [ETKF](/ensemble-transform-kalman-filter/) on the same run, as it should be, since both filters give the same mean and covariance.

## Correctness

The [proof](proofs/correctness.md) shows three facts for a linear $H$ and no localization. For one scalar observation, the factor $\alpha$ of line L6 is the root in $[1/2, 1)$ of $\alpha^2 s - 2\alpha(s + r) + (s + r) = 0$, which is exactly the condition for the new perturbations to have the covariance $(I - Kh)P$ (Lemma 1). The predicted observations stay equal to $H$ applied to the state ensemble (Lemma 2). With a diagonal $R$, taking the observations one at a time gives the same mean and covariance as the batch Kalman update (Theorem 3, a theorem). As $N \to \infty$ for a linear Gaussian model the filter converges to the Kalman filter (Kwiatkowski and Mandel 2015). With localization the update is no longer exact and the order of the observations matters a little; this is a heuristic.

## Complexity

Each pass of the loop costs $\Theta(N(n + p))$ for lines L4 and L9, and $\Theta(N)$ for the rest, so the analysis costs $\Theta(p N (n + p))$ plus $N$ applications of $H$. With localization only the state values and observations with a nonzero weight need work, which brings the cost of one pass down to $\Theta(N(n_l + p_l))$ for $n_l$ and $p_l$ local values. The extra space is the two perturbation matrices. Updating the observation ensemble costs $\Theta(p^2 N)$ in total, which can dominate when $p$ is much larger than $n$.

## Properties

- **No perturbed observations.** The analysis is deterministic. Whitaker and Hamill (2002) showed that the perturbed observations of the EnKF add sampling error, and the square root form removes it.
- **Exact second moments.** For a linear $H$ and a diagonal $R$, without localization, the mean and covariance are the Kalman values for the sample covariance.
- **Serial.** Each observation is a rank one update, so no matrix is inverted and localization by distance is easy to apply.
- **Low rank.** The analysis stays in the span of the forecast perturbations.
- **Same moments as the other square root filters.** The ETKF and the EAKF give the same mean and covariance; the members differ by an orthogonal transform in ensemble space (Tippett et al. 2003).

## Variants and improvements

- **Batch square root.** Process all observations together with an $N \times N$ transform: the [ETKF](/ensemble-transform-kalman-filter/), or a square root of $I - Y^\top(YY^\top + (N - 1)R)^{-1}Y$ computed in another way.
- **EAKF.** Anderson's ensemble adjustment Kalman filter does the same scalar update in observation space and regresses the increments onto the state; for one scalar observation the members are the same (see the [EAKF](/ensemble-adjustment-kalman-filter/)).
- **Localized serial filter.** Multiply $b$ and $c$ by a [Gaspari-Cohn](/gaspari-cohn-function/) weight of the distance, which is [covariance localization](/covariance-localization/) applied to the gain.
- **Batches.** Houtekamer and Mitchell (2001) split the observations into batches and processed one batch at a time, which is between the serial and the batch forms.
- **The DEnKF of Sakov and Oke.** Sakov and Oke (2008) give a scheme that uses half the gain for the perturbations, $X - \tfrac12 K H X$. It is not exactly a square root filter: it matches the Kalman covariance only up to a term of second order in $KH$.

## When to use it

Use the serial EnSRF when the observation errors are independent or can be made so, when localization by distance is needed, and when the code should be simple. It is a good choice for models of moderate size and for research systems. For very many observations on a parallel computer, the serial loop is a bottleneck, and the [LETKF](/local-ensemble-transform-kalman-filter/) is easier to run in parallel.

## Pitfalls

- **The wrong root (line L6).** The equation for $\alpha$ has two roots. The other one, $1/(1 - \sqrt{r/(s + r)})$, gives the right covariance but flips the sign of the observed part of the perturbations.
- **Stale predicted observations (line L9).** The observation ensemble must be updated with each observation. Using the original $Y$ for all observations counts the information of the earlier observations twice.
- **Correlated errors.** The serial form needs a diagonal $R$. For correlated errors, first transform the observations with a square root of $R$.
- **The serial order with localization (line L4).** With localization the result depends a little on the order of the observations. The effect is usually small, but it makes runs with different orders differ.
- **Spread collapse.** Like every ensemble filter with few members, the filter underestimates its error. Without [inflation](/covariance-inflation/) or localization it can stop using the data, as the measurement without localization shows.

## Implementations

## History

Square root forms of the Kalman filter were used in engineering long before ensembles, to keep the covariance positive definite in finite precision. For ensembles, Burgers, van Leeuwen and Evensen showed in 1998 that the EnKF needs perturbed observations to give the right analysis spread. Anderson's ensemble adjustment filter of 2001, the ETKF of Bishop, Etherton and Majumdar of 2001, and the serial filter of Whitaker and Hamill of 2002 did without them. Tippett, Anderson, Bishop, Hamill and Whitaker showed in 2003 that these filters are all square root filters and differ only in the choice of the square root.

## References
