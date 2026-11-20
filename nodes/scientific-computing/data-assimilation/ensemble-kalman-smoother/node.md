---
tag: G9PNFT
kind: algorithm
slug: ensemble-kalman-smoother
name: Ensemble Kalman smoother
aliases:
- EnKS
area: scientific-computing/data-assimilation
level: advanced
summary: Updates past states as well as the current one with each new observation, using ensemble cross covariances in time.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the size of the state, N: the ensemble size, p: the number of observations at one time, T: the number of time steps, L: the lag}
  time: {worst: "Θ(T (p^3 + p^2 N + N^3 + N^2 n (L + 1)))"}
  space: {extra: "Θ(N n (L + 1) + N^2 + p (p + N))"}
properties: {deterministic: true, fixed_lag: "a state is final after the data up to L steps later", exact: "for a linear model without model noise and a linear H, given exact initial moments", same_weights: "the weights of the filter analysis are applied to every stored time", filter_case: "L = 0 gives the ETKF"}
history:
  year: 2000
  people: [Geir Evensen, Peter Jan van Leeuwen]
  note: "Evensen and van Leeuwen gave the ensemble Kalman smoother in 2000, and Evensen wrote it in 2003 as one linear combination of the forecast members applied at all times."
prereqs: [ensemble-kalman-filter, rauch-tung-striebel-smoother]
see_also: [ensemble-transform-kalman-filter, ensemble-square-root-filter, smoothing, four-dimensional-variational-assimilation, covariance-inflation, lorenz-96-model, ensemble-kalman-inversion]
sources:
  - paper: doi:10.1175/1520-0493(2000)128<1852:AEKSFN>2.0.CO;2
    title: "G. Evensen and P. J. van Leeuwen, An ensemble Kalman smoother for nonlinear dynamics, Monthly Weather Review 128(6) (2000) 1852-1867"
    locator: the sequential smoother that updates past states with ensemble cross covariances in time
  - paper: doi:10.1007/s10236-003-0036-9
    title: "G. Evensen, The ensemble Kalman filter: theoretical formulation and practical implementation, Ocean Dynamics 53(4) (2003) 343-367"
    locator: "the analysis as a combination of the forecast members, E^a = E^f X5, and its use for the smoother"
  - paper: doi:10.1175/MWR-D-10-05025.1
    title: "E. Cosme, J. Verron, P. Brasseur, J. Blum and D. Auroux, Smoothing problems in a Bayesian framework and their linear Gaussian solutions, Monthly Weather Review 140(2) (2012) 683-695"
    locator: the fixed interval and fixed lag smoothing problems and their linear Gaussian solutions
  - paper: doi:10.1016/j.physd.2006.11.008
    title: "B. R. Hunt, E. J. Kostelich and I. Szunyogh, Efficient data assimilation for spatiotemporal chaos: a local ensemble transform Kalman filter, Physica D 230(1-2) (2007) 112-126"
    locator: the weights in ensemble space and the symmetric square root used here
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation used here
---

The ensemble Kalman smoother (EnKS) of Evensen and van Leeuwen (2000) estimates past states as well as the current one. An [ensemble Kalman filter](/ensemble-kalman-filter/) uses each observation to correct only the state at the time of the observation. The smoother also corrects the stored ensembles of earlier times, through the sample covariances between the earlier states and the predicted observations. Each analysis of the filter writes the new members as linear combinations of the forecast members. The smoother applies the same combinations to the stored ensembles of the last $L$ times. This page uses the deterministic weights of the [ETKF](/ensemble-transform-kalman-filter/). For a linear model without model noise the result is the exact [smoothing](/smoothing/) distribution, the one the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) computes.

## In plain words

A filter answers the question "where is the system now, given the data so far". A smoother answers "where was the system then, given the data that came later as well". The ensemble keeps a set of possible histories, one for each member. When a new observation arrives, the filter decides how much to trust each member now. A member that fits the new data well was probably also right a little earlier, so the smoother gives its past states the same extra weight. It keeps the past states for $L$ steps, then stops changing them.

## The problem

**Input.** An initial ensemble $x_1, \ldots, x_N \in \mathbb R^n$ at time $0$, a model $M$, observations $y^o_t$ for $t = 1, \ldots, T$ (some times may have none) with an observation operator $H$ and an error covariance $R$, a lag $L \ge 0$ and an optional inflation factor $\rho$. The notation is that of Ide, Courtier, Ghil and Lorenc (1997). In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, the model $M$ is its $A$, the forecast $x^f$ and $P^f$ are its predicted $m^-$ and $P^-$, and the analysis $x^a$ and $P^a$ are its filtered $m$ and $P$.

**Output.** For every time $s$, a filtered ensemble that has used the data up to time $s$ and a smoothed ensemble that has used the data up to time $\min(s + L, T)$. For a linear model without noise, a linear $H$ and an initial ensemble with the exact prior moments, their moments are those of $x_s$ given these data.

## The algorithm

$\bar s$ and $S$ are the mean and the perturbations of a stored ensemble, and $W_i$ is column $i$ of $W$.

```pseudo id=main
EnKS(x_1..x_N, M, H, R, y^o_1..y^o_T, L)
L1  for t <- 1 to T do
L2      x_i <- M(x_i) for each member; inflate; add time t to the window
L3      if there are observations at time t then
L4          y_i <- H(x_i); Y <- perturbations; d <- y^o_t - ybar
L5          P~ <- ((N - 1) I + Y^T R^-1 Y)^-1; wbar <- P~ Y^T R^-1 d; W <- sqrt(N - 1) P~^(1/2)
L6          for each time s in the window: s_i <- sbar + S (wbar + W_i)
L7      drop the times s < t - L + 1 from the window      ▷ their ensembles are final
L8  return the filtered and the smoothed ensembles
```

Lines L4 and L5 are the ETKF analysis at time $t$. Line L6 applies its weights to the current ensemble, which gives the filter, and to the stored ensembles of the window, which gives the smoother. The weights depend only on the predicted observations, so the past states need no model run and no observation operator. The filtered ensemble of time $t$ is saved right after line L6, before later analyses change it.

## Example

Take the scalar model $x_1 = 2x_0$, two members $x_0 = (-1, 1)$ with the sample variance $2$, and one observation $y^o_1 = 4$ of $x_1$ with $R = 8$ and the lag $L = 1$. The forecast is $(-2, 2)$ with the variance $8$, so the Kalman gain is $1/2$. The filter moves $x_1$ to the mean $2$ with the variance $4$, and the members to $2 \mp \sqrt 2$.

The sample covariance of $x_0$ and $x_1$ is $4$, so the gain for $x_0$ is $4/16 = 1/4$. The smoothed $x_0$ has the mean $0 + \tfrac14\cdot 4 = 1$ and the variance $2 - 4\cdot 4/16 = 1$, and the members are $1 \mp 1/\sqrt 2$. These are exactly half the members of $x_1$: the same weights act on both times, so the model relation $x_1 = 2x_0$ holds member by member (Corollary 4 of the proof).

For the check value of the page group: with two members $\mp 1/\sqrt 2$, the model $x_1 = x_0$, $y^o_1 = 1$, $R = 1$ and $L = 1$, the smoothed ensemble of time $0$ has the mean $1/2$ and the variance $1/2$, while the filtered ensemble of time $0$ keeps the mean $0$ and the variance $1$.

**A measurement.** On the [Lorenz-96 model](/lorenz-96-model/) with $n = 40$, $F = 8$, RK4 with step $0.05$, every other variable observed every step with $R = I$, $N = 20$ and multiplicative inflation $\rho = 1.2$ of the forecast covariance, without localization, the mean RMSE of the smoothed ensemble mean over cycles 501 to 1500 was (about 25 ms for each cycle with $L = 8$ in pure Python):

| lag $L$ | 0 (filter) | 1 | 2 | 4 | 8 |
|---|---|---|---|---|---|
| seed 1 | 0.481 | 0.439 | 0.405 | 0.363 | 0.331 |
| seed 2 | 0.421 | 0.384 | 0.354 | 0.315 | 0.282 |

The filter with $L = 0$ is the ETKF. On the [ETKF](/ensemble-transform-kalman-filter/) page the same filter gave $0.409$ with seed 1. There the inflation is applied inside the transform, which gives the same members in exact arithmetic, so the gap shows how much one chaotic run depends on rounding. With both seeds the lag of $8$ steps lowered the error by about a third.

## Correctness

The [proof](proofs/correctness.md) shows that one analysis of the smoother is the ETKF analysis of the state stacked over the window (Lemma 1). For a linear $H$ it changes the moments of every stored state by the Gaussian conditioning formulas with the ensemble cross covariances (Lemma 2). For a linear model without model noise, a linear $H$ and an initial ensemble with the exact prior mean and covariance, the smoothed ensembles have exactly the moments of $x_s$ given the data up to time $s + L$ (Theorem 3, by induction over time). With $L \ge T$ these are the moments of the fixed interval smoother. With model noise, nonlinear models, or inflation, the result is an approximation that is measured, not proved.

## Complexity

The weights of line L5 cost $\Theta(p^3 + p^2N)$ for the solve with $R$, $\Theta(N^2p)$ for $Y^\top R^{-1}Y$ and $\Theta(N^3)$ for the eigendecomposition. Line L6 costs $\Theta(N^2n)$ for each of the at most $L + 1$ stored times. So $T$ steps cost $\Theta(T(p^3 + p^2N + N^3 + N^2n(L + 1)))$ plus $NT$ model runs and $NT$ calls of $H$. The extra space is the window of $L + 1$ ensembles, $\Theta(Nn(L + 1))$, plus $\Theta(N^2 + p(p + N))$ for the weights. The model runs are the same as for the filter, so the smoother costs little more than the filter when $L$ is small.

## Properties

- **No extra model runs.** The past states are updated with the weights of the filter, so the smoother needs no backward model and no adjoint.
- **Filter included.** With $L = 0$ the algorithm is the ETKF. The last time is always the same in the filter and the smoother.
- **Exact for linear models.** Without model noise and for a linear $H$, the moments are those of the Gaussian smoothing distribution.
- **Model relation kept.** For a linear model the smoothed members of two times in the window differ by the model, member by member.
- **Deterministic.** With the square root weights the result does not depend on random draws. With perturbed observations, the same smoother applies the matrix $X_5$ of the EnKF.

## Variants and improvements

- **Perturbed observations.** Evensen (2003) writes the EnKF analysis as $E^a = E^fX_5$ for an $N \times N$ matrix $X_5$, and the smoother multiplies the stored ensembles by the same $X_5$.
- **Fixed interval.** Take $L \ge T$ to keep all times. The memory then grows with $T$.
- **Local weights.** With the [LETKF](/local-ensemble-transform-kalman-filter/), each grid point has its own weights, and the smoother applies them to the past values at the same grid point.
- **Ensemble smoother.** The ensemble smoother updates the whole trajectory once with all the data, without the sequential filter. Evensen and van Leeuwen (2000) found the sequential EnKS more accurate with a nonlinear model.
- **Iterative smoothers.** For strongly nonlinear models the update can be repeated, which is related to [ensemble Kalman inversion](/ensemble-kalman-inversion/) and to [4D-Var](/four-dimensional-variational-assimilation/).

## When to use it

Use the EnKS when an estimate of past states is needed, for example for a reanalysis or to estimate initial conditions and parameters, and when an ensemble filter already runs. The extra cost is small. Choose the lag from the time over which the errors stay correlated: beyond that, longer lags only add sampling noise. For linear Gaussian models of small size the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) gives the exact answer directly.

## Pitfalls

- **Too long a lag (line L7).** With a nonlinear model and few members the sample cross covariances between distant times are mostly noise. Updating states with them can make the estimate worse. The lag must be tuned.
- **Using the smoothed ensemble for the next forecast (line L2).** The forecast must start from the filtered ensemble at the current time, which is also the smoothed one at that time. Older smoothed states are not used again for forecasts.
- **Stale weights (line L6).** All stored ensembles must use the weights of the same analysis. Recomputing weights from a past ensemble does not work, because the predicted observations belong to the current time.
- **Inflation of the past (line L2).** Inflation changes only the current forecast. Inflating the stored ensembles as well makes their spread grow at every analysis in the window, with no model step to justify it.
- **Localization in time.** Covariance localization in space does not remove spurious correlations in time. A shorter lag does this.

## Implementations

## History

Evensen and van Leeuwen introduced the ensemble Kalman smoother in 2000 and showed with a nonlinear model that the sequential smoother improves on the ensemble smoother, which uses all the data at once. In 2003 Evensen wrote the EnKF analysis as a combination of the forecast members, which makes the smoother a matter of applying the same matrix at all stored times. Cosme and coauthors gave the linear Gaussian solutions of the fixed interval and fixed lag problems in 2012.

## References
