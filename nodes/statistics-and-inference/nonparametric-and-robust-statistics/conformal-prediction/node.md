---
tag: 83RAAM
kind: technique
slug: conformal-prediction
name: Conformal prediction
aliases:
- conformal inference
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Turns any predictor into prediction sets with coverage at least 1 - alpha, assuming only exchangeable data, by ranking a nonconformity score of a new point among those of the data.
prereqs: [prediction-interval, permutation-test, quantile, order-statistic]
see_also: [split-conformal-prediction, cross-validation, quantile-regression, k-nearest-neighbors, linear-regression, de-finetti-theorem, jackknife-resampling, random-permutation]
sources:
  - book: isbn:9780387001524
    title: Vladimir Vovk, Alex Gammerman and Glenn Shafer, Algorithmic Learning in a Random World, Springer, 2005
    locator: Chapter 2 (conformal predictors, nonconformity measures, validity under exchangeability, smoothed conformal predictors, the nearest neighbour and ridge regression examples)
  - book: isbn:9783031066481
    title: Vladimir Vovk, Alex Gammerman and Glenn Shafer, Algorithmic Learning in a Random World, second edition, Springer, 2022
    locator: Chapter 2 (conformal prediction), general locator
  - paper: doi:10.1080/01621459.2017.1307116
    title: Jing Lei, Max G'Sell, Alessandro Rinaldo, Ryan J. Tibshirani and Larry Wasserman, Distribution-free predictive inference for regression, Journal of the American Statistical Association 113(523), 2018
    locator: Section 2.1 and Theorem 2.1 (full conformal coverage, at least 1 - alpha and at most 1 - alpha + 1/(n + 1) for continuous scores)
  - paper: doi:10.1214/20-AOS1965
    title: Rina Foygel Barber, Emmanuel J. Candès, Aaditya Ramdas and Ryan J. Tibshirani, Predictive inference with the jackknife+, The Annals of Statistics 49(1), 2021
    locator: pp. 486 to 507 (the jackknife+ and CV+, coverage at least 1 - 2 alpha)
  - paper: doi:10.1093/imaiai/iaaa017
    title: Rina Foygel Barber, Emmanuel J. Candès, Aaditya Ramdas and Ryan J. Tibshirani, The limits of distribution-free conditional predictive inference, Information and Inference 10(2), 2021
    locator: pp. 455 to 482 (distribution-free coverage conditional on x is not possible with sets of finite expected length)
  - paper: doi:10.1561/2200000101
    title: Anastasios N. Angelopoulos and Stephen Bates, Conformal prediction, a gentle introduction, Foundations and Trends in Machine Learning 16(4), 2023
    locator: pp. 494 to 591 (a survey with scores for classification and regression)
---

Conformal prediction turns any predictive model into prediction sets with a coverage guarantee that needs no model assumptions. For each candidate value $y$ of the new response it adds $(x_{n+1}, y)$ to the data, computes a nonconformity score for every point, and keeps $y$ if the new score is not among the largest fraction $\alpha$ of the $n + 1$ scores. If the $n + 1$ points are exchangeable, the set contains the true response with probability at least $1 - \alpha$, for every sample size, every distribution and every model. The guarantee is marginal, averaged over the new $x$; it is not a guarantee for each $x$.

## In plain words

You have past examples of inputs and answers, and a new input whose answer you want to bound. Try a possible answer. Put it into the data as if it were true, fit your model to all the points, and measure how badly each point fits. If the trial answer fits worse than nearly all the old points, it is implausible, so reject it. Keep every trial answer that is not rejected. The kept answers form the prediction set.

Why does this work? If the new point comes from the same source as the old ones, and the order of the points carries no information, then the true answer is equally likely to have any rank among the misfit values. So it falls in the worst few ranks only rarely, and the set holds it as often as you asked. A wrong model gives a wide set that still holds.

## When it applies

- The data $Z_i = (X_i, Y_i)$, $i = 1, \ldots, n$, and the new point $Z_{n+1}$ are **exchangeable**: their joint law does not change when they are permuted. Independent and identically distributed points are exchangeable. Time series, data with a shift between training and use, and data chosen after looking at the new point are not.
- You can compute a **nonconformity score** $A$ that maps a bag of $n + 1$ points to $n + 1$ numbers, $R_i$ for point $i$, and that treats the points symmetrically: permuting the bag permutes the scores in the same way. The usual way is to fit a model on all $n + 1$ points and set $R_i = \lvert y_i - \hat\mu(x_i) \rvert$.
- You can afford one model fit for each candidate $y$, or the score has a structure that gives the set in closed form, as for least squares below. If not, use [split conformal prediction](/split-conformal-prediction/), which fits once.

## The template

The holes are the score $A$, the candidate values $\mathcal Y$ and the level $\alpha$.

```pseudo id=main
FULL-CONFORMAL(z_1, ..., z_n, x, Y, A, α)
L1  C ← ∅
L2  for each candidate y ∈ Y do
L3      z_(n+1) ← (x, y)
L4      (R_1, ..., R_(n+1)) ← A(z_1, ..., z_(n+1))     ▷ refit on all n + 1 points
L5      π(y) ← #{i ≤ n + 1 : R_i ≥ R_(n+1)} / (n + 1)
L6      if π(y) > α then C ← C ∪ {y}
L7  return C
```

The number $\pi(y)$ is the **conformal p-value** of $y$. It is the p-value of a [permutation test](/permutation-test/) of the hypothesis that $(x, y)$ is exchangeable with the data, with the score as test statistic. The set $C$ is the set of $y$ that this test does not reject at level $\alpha$, so the coverage statement is the level of the test, turned around.

**Coverage theorem.** Let $Z_1, \ldots, Z_{n+1}$ be exchangeable and let $A$ treat the points symmetrically. Then

$$P\bigl(Y_{n+1} \in C\bigr) \ge 1 - \frac{\lfloor \alpha(n+1) \rfloor}{n+1} \ge 1 - \alpha,$$

and if the scores are almost surely distinct, $P(Y_{n+1} \in C) = \lceil (1 - \alpha)(n + 1) \rceil/(n + 1) < 1 - \alpha + 1/(n + 1)$ (Vovk, Gammerman and Shafer, Chapter 2; Lei et al. 2018, Theorem 2.1).

*Proof.* Take $y = Y_{n+1}$. Then the bag is the true data, and by symmetry of $A$ and exchangeability, the vector $(R_1, \ldots, R_{n+1})$ is exchangeable. Let $K_j = \#\{i : R_i \ge R_j\}$ and $k = \lfloor \alpha(n+1) \rfloor$, so that $\pi(Y_{n+1}) \le \alpha$ exactly when $K_{n+1} \le k$. If $K_j \le k$, then $R_j$ is strictly larger than the $(k+1)$-th largest score, because otherwise the $k + 1$ largest scores are all at least $R_j$. At most $k$ indices have a score strictly larger than the $(k+1)$-th largest, and exactly $k$ when the scores are distinct. So $\#\{j : K_j \le k\} \le k$, with equality for distinct scores. By exchangeability, $P(K_j \le k)$ is the same for every $j$, so $P(K_{n+1} \le k) = E\,\#\{j : K_j \le k\}/(n + 1)$, which is at most $k/(n + 1)$, with equality for distinct scores. Finally $1 - k/(n + 1) = \lceil (1 - \alpha)(n + 1) \rceil/(n + 1)$. $\square$

The proof uses nothing about the model, so a bad model only makes the set larger. If $\alpha < 1/(n + 1)$, then $k = 0$ and $C$ is the whole space: $n$ points cannot support a smaller error rate.

**Least squares in closed form.** For the score $\lvert y_i - \hat a - \hat b x_i \rvert$ of a least squares line fitted on the bag, every residual is an affine function $a_i + b_i y$ of the candidate, with $a$ and $b$ given by the hat matrix of the $n + 1$ design points. The p-value changes only where $\lvert a_i + b_i y \rvert = \lvert a_{n+1} + b_{n+1} y \rvert$, at most $2n$ values. Evaluating $\pi$ at these roots and once between each pair gives the exact set as a finite union of closed intervals. This is the ridge regression confidence machine of Vovk, Gammerman and Shafer with the ridge penalty set to zero. The implementation does this in $O(n^2)$ time, and the tests check it against lines L1 to L7 on a dense grid of candidates.

**Worked example.** Ten points $(x_i, y_i)$ with $x_i = 1, \ldots, 10$ and $y$ = 2.9, 5.5, 4.6, 5.1, 5.1, 5.4, 6.2, 6.0, 5.8, 6.1 have least squares line $3.887 + 0.2515x$. For a new point at $x = 5.5$, where the line predicts $5.27$:

| $\alpha$ | $x$ | rank rule: keep $y$ if $\#\{R_i \ge R_{11}\} \ge$ | exact conformal set |
|---|---|---|---|
| 0.2 | 5.5 | 3 | $[4.03, 6.38]$ |
| 0.1 | 5.5 | 2 | $[3.91, 6.78]$ |
| 0.1 | 20 | 2 | $[-5.70, 19.01]$ |

The candidate loop on the grid $0, 0.01, \ldots, 12$ at $\alpha = 0.2$ keeps the 235 values from $4.04$ to $6.38$, which agrees with the exact set. With $n + 1 = 11$, the guaranteed coverage is $\lceil 0.8 \cdot 11\rceil/11 = 9/11 = 0.818$ for $\alpha = 0.2$ and $10/11 = 0.909$ for $\alpha = 0.1$. At $x = 20$, far outside the data, the set is wide and not centred on the prediction $8.92$. The new point has high leverage: a candidate $y$ pulls the fitted line toward itself, so its own residual stays small for a large range of $y$.

**Coverage, measured.** The theorem is exact, so a simulation only checks the code. With Cauchy errors, for which least squares is a poor fit, $y = 1 + 0.5x + \varepsilon$, $x$ uniform on $[0, 10]$, $\alpha = 0.1$ and 4000 data sets each, the coverage was $0.9005$ for $n = 19$ (theory $18/20 = 0.900$, seed 5) and $0.911$ for $n = 10$ (theory $10/11 = 0.909$, seed 6).

## Classic examples

- **Regression with a fitted model.** Score $\lvert y_i - \hat\mu(x_i) \rvert$ with $\hat\mu$ fitted on the bag: least squares, ridge regression, a [nearest-neighbour](/k-nearest-neighbors/) average or any other learner. For linear smoothers the set has closed form as above; for other learners use a grid of candidates.
- **Classification.** The candidates are the finitely many labels, so lines L1 to L7 are exact with no grid. The nearest-neighbour score of Vovk, Gammerman and Shafer is the distance to the nearest point with the same label over the distance to the nearest point with another label. The set can hold one label, several labels when the case is ambiguous, or none.
- **The distribution-free prediction bound.** With no $x$ and the score $R_i = y_i$, the conformal set is $(-\infty, y_{(n+1-k)}]$ with $k = \lfloor \alpha(n+1) \rfloor \ge 1$, a bound at an order statistic of the sample. This is the one-sided case of the order-statistic [prediction interval](/prediction-interval/).
- **Outlier detection.** The conformal p-value of a new point measures how unusual it is among reference data. Under exchangeability $P(\pi \le t) \le t$ for every $t$, with $\pi$ uniform on $\{1/(n+1), \ldots, 1\}$ when the scores are distinct, so it is a valid p-value for a test of each new point.

## Variations

- **Smoothed conformal prediction.** Replace line L5 with $\bigl(\#\{R_i > R_{n+1}\} + U\,\#\{R_i = R_{n+1}\}\bigr)/(n + 1)$, where $U$ is uniform on $[0, 1]$. The coverage is then exactly $1 - \alpha$, also with ties. The tests check this exactly, for scores with ties, by enumerating all orderings of six points.
- **[Split conformal prediction](/split-conformal-prediction/).** Fit the model once on part of the data and rank the scores of the other part. It needs one fit instead of one for each candidate, and its guarantee is the same with $n$ replaced by the number of calibration points.
- **Jackknife+ and CV+.** Use leave-one-out or K-fold fits, as in [cross-validation](/cross-validation/), instead of a fit for each candidate. The coverage is at least $1 - 2\alpha$ in the worst case (Barber et al. 2021) and usually close to $1 - \alpha$ in practice. It uses all the data for fitting, unlike split conformal.
- **Label-conditional, or Mondrian, conformal prediction.** Rank the score of a candidate label only against points with the same label. The coverage then holds within each class, which helps when one class is rare.
- **Other scores.** Scaled residuals $\lvert y - \hat\mu(x) \rvert/\hat\sigma(x)$ and quantile regression scores give sets whose width changes with $x$. Coverage is the same; only the shape of the sets changes.

## Pitfalls

- **Marginal, not conditional, coverage.** The guarantee is an average over the new $x$. With errors whose spread grows with $\lvert x \rvert$ ($x$ uniform on $[-1, 1]$, standard deviation $0.1 + \lvert x \rvert$, $n = 39$, $\alpha = 0.1$, 8000 data sets, seed 9), the least squares sets covered $0.997$ of the new points with $\lvert x \rvert < 0.25$ but only $0.763$ of those with $\lvert x \rvert > 0.75$, while the overall coverage was $0.9$. No method can give coverage at each $x$ for every distribution with sets of finite expected length (Barber et al. 2021, Information and Inference).
- **A score that is not symmetric.** If the model is fitted on the $n$ data points only and the new point is scored against that fit, the old scores are in-sample residuals and the new one is out-of-sample. They are not exchangeable, and the sets are too short. Either refit on all $n + 1$ points, as in line L4, or use split conformal.
- **Exchangeability fails.** Time series, drift, and a test point chosen in a different way from the training points all break the argument. The coverage can then be far from $1 - \alpha$.
- **A grid of candidates.** The set need not be an interval, and a coarse grid can miss small pieces of it or cut its ends. Use the closed form when there is one, and report the grid step otherwise.
- **Very small $\alpha$.** If $\alpha < 1/(n + 1)$ the set is everything. This is correct, not a bug: with $n$ points no method can promise a smaller error rate without assumptions.
- **Cost.** One fit for each candidate and each new point. For a large model or many new points, split conformal or the jackknife+ is the practical choice.

## Exercises

1. Show that $\pi(Y_{n+1})$ is uniform on $\{1/(n+1), 2/(n+1), \ldots, 1\}$ when the scores are almost surely distinct, and deduce the exact coverage $\lceil (1 - \alpha)(n + 1)\rceil/(n + 1)$.
2. Show that the smoothed p-value is exactly uniform on $[0, 1]$ under exchangeability, also when the scores have ties.
3. For the least squares score, write $a$ and $b$ in terms of the hat matrix $H$ of the $n + 1$ design points, and show that $b_{n+1} = 1 - H_{n+1, n+1} > 0$ when at least two of the first $n$ design points differ.
4. With no $x$ and the score $R_i = \lvert y_i - \bar y \rvert$, where $\bar y$ is the mean of the bag, show that the conformal set is an interval and find its ends for $n = 4$ and $\alpha = 0.2$.
5. Give an example of exchangeable but not independent points for which conformal prediction is still valid, and an example of independent points that are not exchangeable.

## References
