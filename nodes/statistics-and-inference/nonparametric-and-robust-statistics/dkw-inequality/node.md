---
tag: MS1Y6V
kind: theorem
slug: dkw-inequality
name: Dvoretzky-Kiefer-Wolfowitz inequality
aliases:
- DKW inequality
- Massart's inequality
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: The probability that the empirical CDF is more than epsilon from the true CDF anywhere is at most 2 exp(-2 n epsilon^2), with Massart's tight constant. It gives a confidence band.
prereqs: [empirical-distribution-function, glivenko-cantelli-theorem, hoeffding-inequality]
see_also: [kolmogorov-smirnov-test, chernoff-bound, confidence-interval, quantile, bootstrap-method, vc-dimension, rademacher-complexity, anderson-darling-test]
sources:
  - paper: doi:10.1214/aoms/1177728174
    title: A. Dvoretzky, J. Kiefer and J. Wolfowitz, Asymptotic minimax character of the sample distribution function and of the classical multinomial estimator, Annals of Mathematical Statistics 27(3), 1956
    locator: pp. 642 to 669 (the bound C exp(-2 n epsilon^2) with an unspecified constant C)
  - paper: doi:10.1214/aop/1176990746
    title: P. Massart, The tight constant in the Dvoretzky-Kiefer-Wolfowitz inequality, Annals of Probability 18(3), 1990
    locator: pp. 1269 to 1283 (the two-sided bound with C = 2, and the one-sided bound with C = 1 when exp(-2 n epsilon^2) is at most 1/2)
  - paper: doi:10.1080/01621459.1963.10500830
    title: Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301), 1963
    locator: the bound exp(-2 n delta^2) for the mean of n independent variables with values in [0, 1], used at each grid point
  - url: https://arxiv.org/abs/2403.16651
    title: Henry W. J. Reeve, A short proof of the Dvoretzky-Kiefer-Wolfowitz-Massart inequality, arXiv:2403.16651, 2024
    locator: the abstract (the one-sided bound with no restriction on the failure probability, a conjecture of Birnbaum and McCarty)
---

The Dvoretzky-Kiefer-Wolfowitz (DKW) inequality bounds the chance that the [empirical distribution function](/empirical-distribution-function/) $F_n$ of $n$ independent observations is far from the true distribution function $F$ anywhere on the line. In the sharp form of Massart, $P(\sup_t \lvert F_n(t) - F(t) \rvert > \varepsilon) \le 2e^{-2n\varepsilon^2}$ for every $n$, every $\varepsilon > 0$ and every $F$. This is the same bound that [Hoeffding's inequality](/hoeffding-inequality/) gives for $\lvert F_n(t) - F(t) \rvert$ at one fixed point $t$, so taking the sup over all points costs nothing. It turns the [Glivenko-Cantelli theorem](/glivenko-cantelli-theorem/) into a finite-sample statement, and it gives the confidence band $F_n \pm \sqrt{\ln(2/\alpha)/(2n)}$ for the whole function $F$.

## Statement

Let $X_1, \ldots, X_n$ be independent with distribution function $F$, let $F_n$ be their empirical distribution function, and put

$$D_n = \sup_t \lvert F_n(t) - F(t) \rvert, \qquad D_n^+ = \sup_t (F_n(t) - F(t)), \qquad D_n^- = \sup_t (F(t) - F_n(t)).$$

**Theorem (Dvoretzky, Kiefer and Wolfowitz 1956; Massart 1990).** For every $F$, every $n \ge 1$ and every $\varepsilon > 0$:

1. (two-sided) $P(D_n > \varepsilon) \le 2e^{-2n\varepsilon^2}$;
2. (one-sided) $P(D_n^+ > \varepsilon) \le e^{-2n\varepsilon^2}$ and $P(D_n^- > \varepsilon) \le e^{-2n\varepsilon^2}$, proved by Massart when $e^{-2n\varepsilon^2} \le 1/2$.

Dvoretzky, Kiefer and Wolfowitz proved part 1 with an unspecified constant $C$ in place of 2. The side condition in part 2 belongs to the one-sided bound only. Part 1 needs no condition: when $e^{-2n\varepsilon^2} > 1/2$ its right side is above 1. Reeve (2024) proved the one-sided bound with no condition on $\varepsilon$.

**Confidence band.** Setting $2e^{-2n\varepsilon^2} = \alpha$ gives $\varepsilon_\alpha = \sqrt{\ln(2/\alpha)/(2n)}$, and $P(F_n(t) - \varepsilon_\alpha \le F(t) \le F_n(t) + \varepsilon_\alpha \text{ for all } t) \ge 1 - \alpha$.

## In plain words

Draw a sample and plot the share of the sample below each value. The inequality says how likely it is that this staircase is far from the true curve at even one place. The chance falls very fast as the sample grows: doubling the sample squares a small chance, roughly.

The surprise is the size of the bound. Checking a single place already gives a bound of this form. The inequality says that checking every place at the same time costs only a factor of two. So one simple formula gives a band around the staircase that holds the whole true curve with a chosen confidence, for every distribution, with no table.

## Proof

We prove a weaker form completely: the right exponent $2n\varepsilon^2$ with an extra factor in front. The sharp constant needs a longer argument, and we cite it.

**Theorem A.** For every $F$, $n$ and $\varepsilon$ with $n\varepsilon^2 \ge 1$, $P(D_n > \varepsilon) \le 2e^4 n\varepsilon \, e^{-2n\varepsilon^2}$.

*Proof.* Take $\varepsilon \le 1$, since $D_n \le 1$. Let $k = \lfloor n\varepsilon \rfloor + 1$, so $k - 1 \le n\varepsilon < k$. Because $n\varepsilon \ge 1/\varepsilon \ge 1$, $k \ge 2$ and $1/k < \varepsilon$. Use the grid of the Glivenko-Cantelli proof: $q_j = \inf\{t : F(t) \ge j/k\}$ for $j = 1, \ldots, k - 1$, with $q_0 = -\infty$ and $q_k = +\infty$. There it is shown that $F(q_j-) - F(q_{j-1}) \le 1/k$, and that for $t \in [q_{j-1}, q_j)$,

$$F_n(t) - F(t) \le \left(F_n(q_j-) - F(q_j-)\right) + \frac{1}{k}, \qquad F(t) - F_n(t) \le \left(F(q_{j-1}) - F_n(q_{j-1})\right) + \frac{1}{k},$$

where the first bracket is 0 for $j = k$ and the second is 0 for $j = 1$. So $D_n > \varepsilon$ implies that one of the $2(k - 1)$ events $F_n(q_j-) - F(q_j-) > \delta$ or $F(q_j) - F_n(q_j) > \delta$, $1 \le j \le k - 1$, happens, with $\delta = \varepsilon - 1/k > 0$. Each $F_n(q_j-)$ and $F_n(q_j)$ is the mean of $n$ independent indicators with mean $F(q_j-)$ or $F(q_j)$, so by Hoeffding's inequality each event has probability at most $e^{-2n\delta^2}$. Now $\delta^2 \ge \varepsilon^2 - 2\varepsilon/k$, so $2n\delta^2 \ge 2n\varepsilon^2 - 4n\varepsilon/k > 2n\varepsilon^2 - 4$. The union bound gives

$$P(D_n > \varepsilon) \le 2(k - 1) e^{-2n\delta^2} \le 2n\varepsilon \cdot e^4 e^{-2n\varepsilon^2}. \qquad \blacksquare$$

**Reduction to the uniform law.** For the sharp form one may take $F$ continuous. Let $U_1, \ldots, U_n$ be independent uniforms with empirical distribution function $G_n$, and let $X_i = F^{-1}(U_i)$ with the generalized inverse $F^{-1}(u) = \inf\{t : F(t) \ge u\}$. Then $X_i \le t$ exactly when $U_i \le F(t)$, so $F_n(t) = G_n(F(t))$, and $D_n = \sup_t \lvert G_n(F(t)) - F(t) \rvert$ is a sup over a subset of $[0, 1]$. So $D_n$ is at most the statistic of the uniforms, with equality in law when $F$ is continuous. The same holds for $D_n^+$ and $D_n^-$. A bound proved for the uniform law therefore holds for every $F$.

**The sharp constant.** By the reduction, the sharp bounds are statements about uniform samples. Massart (1990) proved them in a long paper, and Reeve (2024) gave a shorter proof; we do not reproduce either argument. For uniform samples the exact law of $D_n^+$ has the finite form $P(D_n^+ \ge \varepsilon) = \varepsilon \sum_{j=0}^{\lfloor n(1-\varepsilon) \rfloor} \binom{n}{j} (1 - \varepsilon - j/n)^{n-j} (\varepsilon + j/n)^{j-1}$, and the exact two-sided law is a matrix power (see the [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/)). We checked the bounds against these exact laws, computed with the code of the Kolmogorov-Smirnov page: for $n \le 40$ and $\varepsilon$ on a grid of step $1/400$, $P(D_n^+ \ge \varepsilon)$ never exceeded $e^{-2n\varepsilon^2}$, and for $n \le 20$ and $\varepsilon$ on a grid of step $1/100$, $P(D_n \ge \varepsilon)$ never exceeded $2e^{-2n\varepsilon^2}$.

## Consequences

**A band with no table.** At $\alpha = 0.05$, $\varepsilon_\alpha = \sqrt{\ln 40/(2n)}$, which is $0.1358$ for $n = 100$ and $0.04295$ for $n = 1000$. The exact probability that the band misses $F$ for a continuous $F$ is below $0.05$, and close to it for large $n$:

| $n$ | $\varepsilon_{0.05}$ | exact $P(D_n > \varepsilon_{0.05})$ |
|---|---|---|
| 5 | 0.6074 | 0.02703 |
| 10 | 0.4295 | 0.03429 |
| 20 | 0.3037 | 0.03919 |
| 50 | 0.1921 | 0.04332 |
| 100 | 0.1358 | 0.04533 |

**Sample size.** To estimate $F$ everywhere within $\varepsilon$ with probability $1 - \alpha$, $n \ge \ln(2/\alpha)/(2\varepsilon^2)$ is enough. For $\alpha = 0.05$ this is $n \ge 738$ for $\varepsilon = 0.05$ and $n \ge 18445$ for $\varepsilon = 0.01$.

**Quantiles.** The band for $F$ gives simultaneous intervals for all [quantiles](/quantile/) at once: with probability at least $1 - \alpha$, $F^{-1}(p)$ lies between $F_n^{-1}(p - \varepsilon_\alpha)$ and $F_n^{-1}(p + \varepsilon_\alpha)$ for every $p$ where these are defined.

**Almost sure convergence with a rate.** $\sum_n 2e^{-2n\varepsilon^2} < \infty$ for each $\varepsilon > 0$, so by the Borel-Cantelli lemma $D_n > \varepsilon$ happens only finitely often. This proves the Glivenko-Cantelli theorem again, and also shows $D_n = O(\sqrt{\ln n / n})$ almost surely.

**A conservative Kolmogorov-Smirnov test.** Rejecting when $D_n > \varepsilon_\alpha$ is a valid test of level $\alpha$ with no table. It is slightly conservative: at $n = 100$ its size is $0.04533$, and the exact 5% critical value is $0.134$ against $\varepsilon_{0.05} = 0.1358$.

## Tightness

**The constant 2 and the exponent 2 cannot be improved.** By Kolmogorov's limit law, $P(\sqrt{n} D_n > \lambda) \to 2\sum_{k \ge 1} (-1)^{k-1} e^{-2k^2\lambda^2}$, and the first term of this sum is the bound $2e^{-2\lambda^2}$. The ratio of the limit to the bound is $0.7946$ at $\lambda = 0.5$, $0.9785$ at $0.8$, $0.99752$ at $1.0$, $0.999985$ at $1.36$ and $0.99999999996$ at $2.0$. So any bound $Ce^{-c n \varepsilon^2}$ that holds for all $n$ needs $C \ge 2$ when $c = 2$, and $c \le 2$.

**The 5% point.** The bound gives $\lambda = \sqrt{\ln 40/2} = 1.3581015$ for the limit, and the exact 95% point of the Kolmogorov law is $1.3580986$. The limit tail at the bound's point is $0.0499992$. For large $n$ the band is as narrow as the exact one to four digits.

**The one-sided condition.** Massart's proof of the one-sided bound used $e^{-2n\varepsilon^2} \le 1/2$. The grid check above found no exception for $n \le 40$, and Reeve (2024) proved the bound without the condition.

**Independence is needed.** If $X_i = X_1$ for all $i$ and $F$ is continuous, $D_n \ge 1/2$ always, while the bound tends to 0 for each $\varepsilon < 1/2$.

## History

Aryeh Dvoretzky, Jack Kiefer and Jacob Wolfowitz (1956) proved the bound $Ce^{-2n\varepsilon^2}$ with an unspecified constant $C$, on the way to showing that the empirical distribution function is asymptotically minimax. Birnbaum and McCarty (1958) conjectured that $C = 1$ works for the one-sided bound. Pascal Massart (1990) proved that $C = 2$ works for the two-sided bound, which is the best constant, and $C = 1$ for the one-sided bound when $e^{-2n\varepsilon^2} \le 1/2$. Henry Reeve (2024) gave a short proof and removed the condition on the one-sided bound.

## References
