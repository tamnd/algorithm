---
tag: GZDDD3
kind: theorem
slug: greenwood-formula
name: Greenwood's formula
aliases:
- Greenwood variance estimator
area: statistics-and-inference/survival-analysis
level: core
summary: Estimates the variance of the Kaplan-Meier estimate as S(t)^2 times the sum over event times of d / (n (n - d)), and gives pointwise confidence intervals.
prereqs: [kaplan-meier-estimator, delta-method, slutsky-theorem, central-limit-theorem]
see_also: [standard-error, confidence-interval, nelson-aalen-estimator, log-rank-test, bootstrap-method, censoring, law-of-large-numbers, binomial-distribution]
sources:
  - paper: "Major Greenwood, A Report on the Natural Duration of Cancer, Reports on Public Health and Medical Subjects No. 33, His Majesty's Stationery Office, London, 1926"
    locator: pp. 1 to 26 (the variance of the life-table survival estimate is derived in Appendix I)
  - paper: doi:10.1080/01621459.1958.10501452
    title: E. L. Kaplan and Paul Meier, Nonparametric estimation from incomplete observations, Journal of the American Statistical Association 53(282), 1958
    locator: pp. 457 to 481 (the variance of the product-limit estimate, the same formula derived again)
  - paper: doi:10.1214/aos/1176342705
    title: N. Breslow and J. Crowley, A large sample study of the life table and product limit estimates under random censorship, Annals of Statistics 2(3), 1974
    locator: pp. 437 to 453 (weak convergence of the product-limit process for continuous distributions, and consistency of the Greenwood estimate)
  - book: isbn:9780387945194
    title: Per Kragh Andersen, Ørnulf Borgan, Richard D. Gill and Niels Keiding, Statistical Models Based on Counting Processes, Springer, 1993
    locator: Chapter IV (the product-limit estimator, its asymptotic variance and the Greenwood-type estimators of it)
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 4 (Greenwood's formula and pointwise confidence intervals for the survival function, including the log-log transformation)
---

Greenwood's formula is the usual estimate of the variance of the [Kaplan-Meier estimate](/kaplan-meier-estimator/) $\hat S(t)$:

$$\widehat{\mathrm{Var}}\,\hat S(t) = \hat S(t)^2 \sum_{j:\, t_j \le t} \frac{d_j}{n_j(n_j - d_j)},$$

where $t_j$ are the distinct event times, $d_j$ the events and $n_j$ the subjects at risk at $t_j$. The theorem behind it says that, under [independent censoring](/censoring/), $\hat S(t)$ is asymptotically normal and $n$ times Greenwood's estimate converges in probability to the asymptotic variance. So $\hat S(t) \pm z_{1 - \alpha/2}\sqrt{\widehat{\mathrm{Var}}}$ is a pointwise [confidence interval](/confidence-interval/) with asymptotic coverage $1 - \alpha$. Below, the theorem is proved in full for event times on a finite grid, by the [delta method](/delta-method/). The continuous case is stated with its source and not proved here. The finite-sample behaviour of the intervals is only measured, by simulation.

## Statement

Let $(T_i, C_i)$, $i = 1, \ldots, n$, be independent copies of a pair $(T, C)$ of an event time and a censoring time, with observed $Y_i = \min(T_i, C_i)$ and $\delta_i = 1\{T_i \le C_i\}$. Fix a time $t$. Let $t_1 < \cdots < t_m$ be the points in $(0, t]$ where $T$ has positive mass, and write

$$q_j = P(T = t_j \mid T \ge t_j), \qquad \pi_j = P(Y \ge t_j), \qquad S(t) = P(T > t) = \prod_{j=1}^m (1 - q_j).$$

The Kaplan-Meier estimate is $\hat S(t) = \prod_{j=1}^m (1 - \hat q_j)$ with $\hat q_j = d_j / n_j$, $d_j = \#\{i : Y_i = t_j, \delta_i = 1\}$ and $n_j = \#\{i : Y_i \ge t_j\}$ (set $\hat q_j = 0$ when $n_j = 0$). Greenwood's estimate is $\hat V(t) = \hat S(t)^2 \sum_{j=1}^m d_j / (n_j(n_j - d_j))$, set to $0$ when some $d_j = n_j$.

**Theorem (Greenwood's formula, discrete time).** Assume:

1. the pairs $(T_i, C_i)$ are independent and identically distributed;
2. $T$ is discrete, and it has finitely many points of positive mass in $(0, t]$;
3. censoring is independent: $P(T = t_j \mid T \ge t_j, C \ge t_j) = q_j$ for $j = 1, \ldots, m$ (this holds when $T$ and $C$ are independent);
4. $\pi_j > 0$ for $j = 1, \ldots, m$: some subjects can still be under observation at $t_j$;
5. $q_j < 1$ for $j = 1, \ldots, m$, so $S(t) > 0$.

Then, as $n \to \infty$,

- (a) $\sqrt n\,(\hat S(t) - S(t)) \xrightarrow{d} N(0, \sigma^2(t))$ with $\displaystyle \sigma^2(t) = S(t)^2 \sum_{j=1}^m \frac{q_j}{\pi_j (1 - q_j)}$;
- (b) $n \hat V(t) \xrightarrow{p} \sigma^2(t)$;
- (c) if $S(t) < 1$, then $(\hat S(t) - S(t))/\sqrt{\hat V(t)} \xrightarrow{d} N(0, 1)$, so the interval $\hat S(t) \pm z_{1 - \alpha/2}\sqrt{\hat V(t)}$ has coverage tending to $1 - \alpha$.

**Continuous case (cited, not proved here).** If $T$ has a continuous distribution $F$, $T$ and $C$ are independent, $C$ has survival function $G$, and $P(Y > t) > 0$, then $\sqrt n(\hat S(t) - S(t)) \to N(0, \sigma^2(t))$ with $\sigma^2(t) = S(t)^2 \int_0^t \frac{dF(u)}{S(u)\,S(u-)\,G(u-)}$, and $n \hat V(t) \to \sigma^2(t)$ in probability (Breslow and Crowley 1974; Andersen et al. 1993, Chapter IV, with general $F$ and with counting process methods). For continuous $F$, $S(u) = S(u-)$. For discrete $T$ independent of $C$, $\pi_j = S(t_j-)\,G(t_j-)$ and $P(T = t_j) = q_j S(t_j-)$, so the integrand at $u = t_j$ becomes $q_j/(\pi_j(1 - q_j))$, the term in (a).

## In plain words

The Kaplan-Meier curve multiplies many fractions, one for each death: the fraction of the people at risk who got past that moment. Each fraction is like a coin-toss proportion, so its uncertainty is roughly the usual one for a proportion, and the fractions at different moments are uncorrelated. When you multiply fractions, their relative errors add up. Greenwood's formula adds the relative uncertainty of each fraction and scales the total back by the square of the survival estimate. Moments with few people at risk add the most uncertainty.

## Proof

Write $E_{ij} = 1\{Y_i = t_j, \delta_i = 1\}$ (subject $i$ has an observed event at $t_j$) and $R_{ij} = 1\{Y_i \ge t_j\}$ (subject $i$ is at risk at $t_j$). Then $d_j = \sum_i E_{ij}$ and $n_j = \sum_i R_{ij}$. Every event at $t_j$ is at risk at $t_j$, so $E_{ij} \le R_{ij}$ and $E_{ij}R_{ij} = E_{ij}$.

**Step 1: the centred event counts.** $E_{ij} = 1$ means $T_i = t_j$ and $C_i \ge t_j$, and $R_{ij} = 1$ means $T_i \ge t_j$ and $C_i \ge t_j$. By condition 3,

$$\mathrm E[E_{ij}] = P(T = t_j \mid T \ge t_j, C \ge t_j)\, P(T \ge t_j, C \ge t_j) = q_j \pi_j, \qquad \mathrm E[R_{ij}] = \pi_j.$$

Define $\xi_{ij} = E_{ij} - q_j R_{ij}$ and the vector $\xi_i = (\xi_{i1}, \ldots, \xi_{im})$. Then:

- $\mathrm E[\xi_{ij}] = q_j\pi_j - q_j\pi_j = 0$.
- $\mathrm E[\xi_{ij}^2] = \mathrm E[E_{ij}] - 2q_j\mathrm E[E_{ij}R_{ij}] + q_j^2\mathrm E[R_{ij}] = q_j\pi_j - 2q_j^2\pi_j + q_j^2\pi_j = q_j(1 - q_j)\pi_j$.
- For $j < l$: an event at $t_j$ means $Y_i = t_j < t_l$, so $E_{ij}E_{il} = E_{ij}R_{il} = 0$. Being at risk at $t_l$ or having an event there implies being at risk at $t_j$, so $R_{ij}R_{il} = R_{il}$ and $R_{ij}E_{il} = E_{il}$. Expanding,
$$\xi_{ij}\xi_{il} = -q_j E_{il} + q_j q_l R_{il} = -q_j \xi_{il},$$
and $\mathrm E[\xi_{ij}\xi_{il}] = -q_j\mathrm E[\xi_{il}] = 0$.

So the $\xi_i$ are independent and identically distributed with mean $0$ and covariance matrix $D = \mathrm{diag}(q_j(1 - q_j)\pi_j)$. They are bounded, so all moments are finite.

**Step 2: the hazard estimates are jointly normal.** By the multivariate [central limit theorem](/central-limit-theorem/) (the central limit theorem for each linear combination $a^{\mathsf T}\xi_i$, and the Cramér-Wold device), $Z_n = n^{-1/2}\sum_{i=1}^n \xi_i \xrightarrow{d} N_m(0, D)$. By the [law of large numbers](/law-of-large-numbers/), $n_j/n \to \pi_j > 0$ in probability (condition 4), so $P(n_j = 0) \to 0$. On the event $\{n_j > 0\}$,

$$\hat q_j - q_j = \frac{d_j - q_j n_j}{n_j} = \frac{\sum_i \xi_{ij}}{n_j}, \qquad \text{so} \qquad \sqrt n(\hat q_j - q_j) = \frac{n}{n_j}\, Z_{n,j}.$$

Let $A_n = \mathrm{diag}(n/n_j)$, which converges in probability to $A = \mathrm{diag}(1/\pi_j)$. By the vector form of [Slutsky's theorem](/slutsky-theorem/), $A_n Z_n \xrightarrow{d} A\,N_m(0, D)$, which is

$$\sqrt n(\hat q - q) \xrightarrow{d} N_m(0, \Sigma), \qquad \Sigma = A D A = \mathrm{diag}\!\left(\frac{q_j(1 - q_j)}{\pi_j}\right).$$

The events $\{n_j = 0\}$ have probability tending to $0$, so the value of $\hat q_j$ on them does not change the limit. The hazard estimates at different event times are asymptotically independent.

**Step 3: the delta method.** $\hat S(t) = g(\hat q)$ and $S(t) = g(q)$ for $g(x) = \prod_{j=1}^m (1 - x_j)$, which is a polynomial and so differentiable everywhere. Its gradient at $q$ has entries

$$\frac{\partial g}{\partial x_j}(q) = -\prod_{l \ne j}(1 - q_l) = -\frac{S(t)}{1 - q_j},$$

using condition 5. By the multivariate [delta method](/delta-method/), $\sqrt n(\hat S(t) - S(t)) \xrightarrow{d} N(0, \nabla g^{\mathsf T}\Sigma\nabla g)$ with

$$\nabla g^{\mathsf T}\Sigma\nabla g = \sum_{j=1}^m \frac{S(t)^2}{(1 - q_j)^2}\cdot\frac{q_j(1 - q_j)}{\pi_j} = S(t)^2\sum_{j=1}^m \frac{q_j}{\pi_j(1 - q_j)} = \sigma^2(t).$$

This proves (a).

**Step 4: Greenwood's estimate is consistent.** On the event that $n_j > 0$ and $d_j < n_j$ for every $j$,

$$n\hat V(t) = \hat S(t)^2 \sum_{j=1}^m \frac{n\, d_j}{n_j(n_j - d_j)} = \hat S(t)^2\sum_{j=1}^m \frac{\hat q_j}{(n_j/n)(1 - \hat q_j)}.$$

The map $(s, x, p) \mapsto s^2\sum_j x_j/(p_j(1 - x_j))$ is continuous at $(S(t), q, \pi)$ because every $\pi_j > 0$ and every $q_j < 1$. We have $\hat S(t) \xrightarrow{p} S(t)$ and $\hat q \xrightarrow{p} q$ from (a) and Step 2, and $n_j/n \xrightarrow{p} \pi_j$. By the continuous mapping theorem, $n\hat V(t) \xrightarrow{p} \sigma^2(t)$. The event that some $n_j = 0$ or some $d_j = n_j$ has probability tending to $0$, because $\hat q_j \to q_j < 1$ in probability. This proves (b).

**Step 5: the studentized statistic.** If $S(t) < 1$, then some $q_j > 0$, so $\sigma^2(t) > 0$. Write $(\hat S - S)/\sqrt{\hat V} = \sqrt n(\hat S - S)\big/\sqrt{n\hat V}$. The numerator converges in distribution to $N(0, \sigma^2)$ by (a), and the denominator converges in probability to $\sigma > 0$ by (b). Slutsky's theorem gives the limit $N(0, 1)$, and the coverage of the interval tends to $P(|N(0,1)| \le z_{1 - \alpha/2}) = 1 - \alpha$. This proves (c). $\square$

## Consequences

**No censoring: the binomial variance.** If no subject is censored, $\hat S(t) = \#\{i : Y_i > t\}/n$ is a binomial proportion, and Greenwood's estimate is exactly $\hat S(t)(1 - \hat S(t))/n$. Without censoring $n_{j+1} = n_j - d_j$, so each term telescopes:

$$\frac{d_j}{n_j(n_j - d_j)} = \frac{1}{n_j - d_j} - \frac{1}{n_j} = \frac{1}{n_{j+1}} - \frac{1}{n_j}, \qquad \sum_{j=1}^m \frac{d_j}{n_j(n_j - d_j)} = \frac{1}{n\hat S(t)} - \frac1n,$$

because $n_1 = n$ and $n_m - d_m = n\hat S(t)$. Multiplying by $\hat S(t)^2$ gives $\hat S(t)(1 - \hat S(t))/n$, the plug-in variance of a [binomial](/binomial-distribution/) proportion.

**A worked example.** In the 6-MP arm of the leukemia data on the [Kaplan-Meier page](/kaplan-meier-estimator/), the event times up to 23 weeks have $(n_j, d_j) = (21, 3), (17, 1), (15, 1), (12, 1), (11, 1), (7, 1), (6, 1)$. The sum is

$$\frac{3}{21 \cdot 18} + \frac{1}{17 \cdot 16} + \frac{1}{15 \cdot 14} + \frac{1}{12 \cdot 11} + \frac{1}{11 \cdot 10} + \frac{1}{7 \cdot 6} + \frac{1}{6 \cdot 5} = 0.09018,$$

and with $\hat S(23) = 160/357 = 0.4482$ the standard error is $0.4482\sqrt{0.09018} = 0.1346$. The plain 95% interval is $(0.184, 0.712)$.

**The log-log interval.** The plain interval can leave $[0, 1]$, and its coverage is poor when $S(t)$ is near $0$ or $1$. Apply the delta method to $\theta = \log(-\log S(t))$ for $0 < S(t) < 1$: the derivative of $s \mapsto \log(-\log s)$ is $1/(s\log s)$, so the estimated standard error of $\hat\theta$ is

$$\hat\tau = \frac{\sqrt{\hat V(t)}}{\hat S(t)\,|\log\hat S(t)|} = \frac{\sqrt{\sum_{j} d_j/(n_j(n_j - d_j))}}{|\log\hat S(t)|}.$$

Transforming $\hat\theta \pm z\hat\tau$ back with $S = \exp(-e^\theta)$ gives the interval $\left(\hat S(t)^{\exp(z\hat\tau)},\ \hat S(t)^{\exp(-z\hat\tau)}\right)$, which always lies inside $(0, 1)$. By (c) and the delta method it has the same asymptotic coverage. For the 6-MP data at 23 weeks it is $(0.188, 0.680)$. For the placebo arm at 15 weeks, where $\hat S = 1/7$ and there is no censoring, the plain interval $(-0.007, 0.293)$ goes below $0$, while the log-log interval is $(0.036, 0.321)$.

**Other uses.** The same Step 2 gives the variance of the [Nelson-Aalen estimator](/nelson-aalen-estimator/) of the cumulative hazard, $\sum_j q_j(1 - q_j)/\pi_j$, estimated by $\sum_j d_j(n_j - d_j)/n_j^3$. The asymptotic independence of the $\hat q_j$ across event times is also the reason why the [log-rank test](/log-rank-test/) adds variances over event times. Greenwood's formula gives a pointwise interval at each fixed $t$; it does not give a band that covers the whole curve with probability $1 - \alpha$. Simultaneous bands, such as the Hall-Wellner band, need the limit process of the continuous case.

## Tightness

**Each condition is needed.**
- Without independent censoring (condition 3), $\hat S$ converges to the wrong limit. Let $T$ be uniform on $\{1, 2, 3\}$, let a subject with $T = 2$ be censored at time 1.5 with probability $1/2$, and let no other subject be censored. At time 2 the risk set has limiting proportion $1/6 + 1/3 = 1/2$ of the sample, with events $1/6$, so $\hat q_2 \to 1/3$, while $q_2 = P(T = 2 \mid T \ge 2) = 1/2$. Then $\hat S(2) \to (2/3)(2/3) = 4/9$, but $S(2) = 1/3$. The observed pairs $(Y, \delta)$ alone cannot reveal this (Tsiatis 1975; see [censoring](/censoring/)).
- Without condition 4 no one is observed at $t_j$, $q_j$ does not appear in the data, and no consistent estimate of $S(t)$ exists.
- Without condition 5, $S(t) = 0$, $\hat S(t) = 0$ with probability tending to $1$, and the limit in (a) is degenerate.

**What is measured, not proved.** The theorem is about the limit. In finite samples Greenwood's estimate tends to be too small, and the plain interval undercovers. In a simulation with $T \sim$ exponential with rate 1, independent censoring $C \sim$ exponential with rate 0.5 (one third of the times censored), $t$ chosen so that $S(t) = 0.5$, $0.8$ or $0.95$, $r = 10000$ replications per row and seed 2026:

| $n$ | $S(t)$ | variance of $\hat S$ | mean of $\hat V$ | plain 95% | log-log 95% |
|---|---|---|---|---|---|
| 20 | 0.5 | 0.01562 | 0.01443 | 0.921 | 0.949 |
| 20 | 0.8 | 0.00860 | 0.00807 | 0.905 | 0.950 |
| 20 | 0.95 | 0.00242 | 0.00226 | 0.628 | 0.560 |
| 50 | 0.5 | 0.00613 | 0.00597 | 0.938 | 0.948 |
| 50 | 0.8 | 0.00337 | 0.00332 | 0.923 | 0.956 |
| 50 | 0.95 | 0.000965 | 0.000935 | 0.913 | 0.881 |
| 200 | 0.5 | 0.00152 | 0.00152 | 0.949 | 0.951 |
| 200 | 0.8 | 0.000852 | 0.000846 | 0.943 | 0.951 |
| 200 | 0.95 | 0.000243 | 0.000240 | 0.924 | 0.950 |

The log-log interval is close to 95% at $n = 20$ when $S(t)$ is not extreme. At $S(t) = 0.95$ and $n = 20$ both intervals fail: in about a third of the samples no event happens before $t$, so $\hat S(t) = 1$, $\hat V(t) = 0$, and neither interval contains the true value. The coverage tends to 95% as $n$ grows, as (c) says, but this table only measures it.

## History

Major Greenwood derived the formula in 1926, in an appendix to a report for the British Ministry of Health on the natural duration of cancer, for the actuarial life-table estimate of survival from grouped data. He treated the survival fractions of successive intervals as independent binomial proportions and combined their variances, which is the argument of Steps 2 and 3 in finite-sample form. Kaplan and Meier (1958) derived the same formula for the product-limit estimate. Breslow and Crowley (1974) gave the first rigorous large-sample proof for the product-limit estimate under random censorship with continuous $F$, and the counting process theory of the late 1970s and the 1980s, collected by Andersen, Borgan, Gill and Keiding (1993), extended it to general distributions and to the whole curve.

## References
