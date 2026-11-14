---
tag: 9NC28F
kind: theorem
slug: fieller-theorem
name: Fieller's theorem
aliases:
- Fieller interval
- Fieller's method
area: statistics-and-inference/hypothesis-testing
level: advanced
summary: Gives an exact confidence set for the ratio of two normal means by inverting a t-test. The set can be an interval, the union of two rays, or the whole line.
prereqs: [pivotal-quantity, test-interval-duality, student-t-test]
see_also: [delta-method, errors-in-variables-regression, t-confidence-interval, confidence-interval, total-variation-distance, prediction-interval, bootstrap-t-interval, welch-t-test]
sources:
  - paper: doi:10.1111/j.2517-6161.1954.tb00159.x
    title: E. C. Fieller, Some problems in interval estimation, Journal of the Royal Statistical Society, Series B 16(2), 1954
    locator: pp. 175 to 185 (the confidence set for a ratio and its three shapes)
  - paper: doi:10.1214/aos/1176350597
    title: Leon Jay Gleser and Jiunn T. Hwang, The nonexistence of 100(1 - alpha)% confidence sets of finite expected diameter in errors-in-variables and related models, Annals of Statistics 15(4), 1987
    locator: pp. 1351 to 1362 (no confidence interval with positive confidence has finite expected length)
  - paper: doi:10.2307/2171740
    title: Jean-Marie Dufour, Some impossibility theorems in econometrics with applications to structural and dynamic models, Econometrica 65(6), 1997
    locator: pp. 1365 to 1387 (valid confidence sets for locally almost unidentified parameters must be unbounded with positive probability)
---

Fieller's theorem gives an exact confidence set for a ratio $\rho = \mu_1/\mu_2$ of two normal means. Instead of studying the estimate $\hat\rho = a/b$, whose law has no mean and depends on the unknown values, it uses the fact that $a - \rho b$ is normal with mean 0 at the true $\rho$. Studentizing gives a t-distributed [pivotal quantity](/pivotal-quantity/), and the set of $\rho$ where its square is at most $t^2$ is the solution of a quadratic inequality. That set is a bounded interval when the denominator mean is clearly away from zero, and two rays or the whole line when it is not. The coverage is exactly $1 - \alpha$ in every case.

## Statement

Let $(a, b)$ be jointly normal with mean $(\mu_1, \mu_2)$, $\mu_2 \neq 0$, and an unknown positive definite covariance matrix $\Sigma$. Let $W = (w_{ij})$ be a random symmetric $2 \times 2$ matrix that is positive definite with probability 1, independent of $(a, b)$, and such that for every fixed vector $c$, $\nu\, c^\top W c / c^\top \Sigma c$ has the chi-square law with $\nu$ degrees of freedom. Two common cases are:

- **Paired data.** $(X_i, Y_i)$, $i = 1, \ldots, n$, iid bivariate normal, $a = \bar X$, $b = \bar Y$, $W$ the sample covariance matrix divided by $n$, and $\nu = n - 1$. Then $a - \rho b$ is the mean of the differences $X_i - \rho Y_i$.
- **Known structure.** $\Sigma = \sigma^2 V$ with $V$ known and positive definite, $W = S^2 V$, and $\nu S^2/\sigma^2$ chi-square with $\nu$ degrees of freedom, as for two independent samples with a pooled variance or for two coefficients of a [least squares](/ordinary-least-squares/) fit.

Let $t = t_{(\nu, 1 - \alpha/2)}$ be the lower $1 - \alpha/2$ quantile of the t law with $\nu$ degrees of freedom, and define

$$C = \big\{\rho \in \mathbb R : (a - \rho b)^2 \le t^2 (w_{11} - 2\rho w_{12} + \rho^2 w_{22})\big\}.$$

Put $A = b^2 - t^2 w_{22}$, $B = ab - t^2 w_{12}$, $D = B^2 - A(a^2 - t^2 w_{11})$, and $\hat\rho = a/b$.

**Theorem.**

1. **Exact coverage.** $P(\mu_1/\mu_2 \in C) = 1 - \alpha$ for every $\mu_1$, every $\mu_2 \neq 0$ and every $\Sigma$.
2. **Shape.** With probability 1, exactly one of these holds:
   - $A > 0$. Then $D > 0$ and $C = [(B - \sqrt D)/A,\; (B + \sqrt D)/A]$, a bounded interval that contains $\hat\rho$.
   - $A < 0$ and $D > 0$. Then $C = (-\infty, r_1] \cup [r_2, \infty)$ with $r_1 = (B + \sqrt D)/A < r_2 = (B - \sqrt D)/A$, the union of two rays.
   - $A < 0$ and $D < 0$. Then $C = \mathbb R$.
3. **When it is bounded.** $C$ is bounded if and only if $\lvert b \rvert / \sqrt{w_{22}} > t$, that is, if and only if the two-sided level-$\alpha$ t-test of $H_0: \mu_2 = 0$ rejects. $C = \mathbb R$ if and only if $Q = (a, b)\, W^{-1} (a, b)^\top < t^2$.
4. **No bounded method is exact.** Every confidence set procedure $C'(a, b, W)$ that is bounded with probability 1 has $\inf P(\mu_1/\mu_2 \in C') = 0$, the infimum taken over $\mu_1$, $\mu_2 \neq 0$ and $\Sigma$. In particular this holds for the [delta-method](/delta-method/) interval $\hat\rho \pm t\, \widehat{\mathrm{se}}(\hat\rho)$.

When $A > 0$, the ends can be written with $g = t^2 w_{22}/b^2 < 1$ as

$$\frac{1}{1 - g}\left(\hat\rho - g\frac{w_{12}}{w_{22}} \pm \frac{t}{\lvert b \rvert}\sqrt{w_{11} - 2\hat\rho w_{12} + \hat\rho^2 w_{22} - g\Big(w_{11} - \frac{w_{12}^2}{w_{22}}\Big)}\right),$$

which is the form in Fieller's papers. As $g \to 0$ it tends to the delta-method interval.

## In plain words

Do not divide by $b$. For a trial value $\rho$, the number $a - \rho b$ should be near zero if $\rho$ is right, and its standard error is known up to the usual t-scaling. So test "$\mu_1 - \rho\mu_2 = 0$" with a t-test, and keep every $\rho$ that passes. Squaring the condition gives a quadratic in $\rho$. If the denominator is clearly not zero, the quadratic opens upward and the set is an ordinary interval. If the data cannot rule out a zero denominator, the ratio could be huge with either sign, so the set must reach out to infinity. This is a property of the problem, not a fault of the method: part 4 says that any method that always gives a finite interval must fail badly for some parameter values.

## Proof

**Part 1.** Fix the true values and put $\rho = \mu_1/\mu_2$ and $c = (1, -\rho)^\top$. Then $a - \rho b = c^\top (a, b)^\top$ is normal with mean $\mu_1 - \rho\mu_2 = 0$ and variance $\tau^2 = c^\top \Sigma c > 0$, since $\Sigma$ is positive definite. Also $\nu\, c^\top W c/\tau^2$ is chi-square with $\nu$ degrees of freedom and independent of $(a, b)$. So

$$T = \frac{a - \rho b}{\sqrt{c^\top W c}} = \frac{(a - \rho b)/\tau}{\sqrt{(\nu\, c^\top W c/\tau^2)/\nu}}$$

is a standard normal over the root of an independent chi-square divided by its degrees of freedom, so $T \sim t_\nu$. The unknown $\tau$ cancels, so $T$ is a pivot. Since $c^\top W c = w_{11} - 2\rho w_{12} + \rho^2 w_{22}$, the event $\rho \in C$ is the event $T^2 \le t^2$, which has probability $P(\lvert T \rvert \le t) = 1 - \alpha$ because the t law is continuous and symmetric. $\square$

**Part 2.** Expanding the defining inequality and collecting powers of $\rho$ gives

$$q(\rho) = A\rho^2 - 2B\rho + (a^2 - t^2 w_{11}) \le 0.$$

*The discriminant.* Expanding $D = B^2 - A(a^2 - t^2 w_{11})$, the terms $a^2 b^2$ cancel and

$$D = t^2\big(a^2 w_{22} - 2ab\, w_{12} + b^2 w_{11}\big) - t^4 (w_{11} w_{22} - w_{12}^2) = t^2 \det W\, (Q - t^2),$$

because $(a, b) W^{-1} (a, b)^\top = (a^2 w_{22} - 2ab\, w_{12} + b^2 w_{11})/\det W$. Here $\det W > 0$.

*A Cauchy-Schwarz bound.* For $u = (a, b)^\top$ and $e = (0, 1)^\top$, $b^2 = (e^\top u)^2 = (e^\top W^{1/2} W^{-1/2} u)^2 \le (e^\top W e)(u^\top W^{-1} u) = w_{22} Q$. So $Q \ge b^2/w_{22}$.

*Case $A > 0$.* Then $b^2 > t^2 w_{22}$, so $Q \ge b^2/w_{22} > t^2$ and $D > 0$. The quadratic opens upward with two distinct real roots, and $q \le 0$ exactly between them. If $b \neq 0$, then $q(\hat\rho)$ equals $-t^2(w_{11} - 2\hat\rho w_{12} + \hat\rho^2 w_{22}) \le 0$, because the left side of the defining inequality is 0 at $\hat\rho$ and $W$ is positive definite; so $\hat\rho \in C$.

*Case $A < 0$.* The quadratic opens downward. If $D > 0$ it has two real roots and $q \le 0$ outside the open interval between them, which gives the two rays. Since $A < 0$, the root $(B + \sqrt D)/A$ is the smaller one. If $D < 0$ it has no real root and $q < 0$ everywhere, so $C = \mathbb R$.

*Null events.* $A = 0$ or $D = 0$ is an equation in the continuous variables $(a, b, W)$; given $W$, each is a set of Lebesgue measure zero in $(a, b)$ (a pair of lines or an ellipse), and $(a, b)$ has a density, so each has probability 0. $\square$

**Part 3.** By Part 2, $C$ is bounded exactly in the case $A > 0$, which is $b^2 > t^2 w_{22}$, that is $\lvert b \rvert/\sqrt{w_{22}} > t$. This statistic is the t statistic for $H_0: \mu_2 = 0$: $b/\sqrt{w_{22}}$ is $T$ from Part 1 with $c = (0, 1)^\top$ and $\mu_2 = 0$. The whole line occurs exactly when $A < 0$ and $D < 0$; by the formula for $D$, $D < 0$ means $Q < t^2$, and $Q < t^2$ forces $b^2/w_{22} \le Q < t^2$, so $A < 0$ holds automatically. $\square$

**Part 4.** Fix $\Sigma$ and $\mu_1 = 1$, and let $\varepsilon > 0$. Write $P_{\mu_2}$ for the law of $(a, b, W)$ with mean $(1, \mu_2)$; $W$ has the same law for every $\mu_2$ and is independent of $(a, b)$. Let $P_0$ be the law with $\mu_2 = 0$. Since $C'$ is bounded with probability 1 under $P_0$, the events $\{C' \subseteq [-M, M]\}$ increase to an event of probability 1 as $M \to \infty$, so there is an $M$ with $P_0(C' \not\subseteq [-M, M]) < \varepsilon$. The [total variation distance](/total-variation-distance/) between two normal laws with the same covariance and means $(1, 0)$ and $(1, \mu_2)$ tends to 0 as $\mu_2 \to 0$, and the $W$ part is the same, so there is $\mu_2$ with $0 < \mu_2 < 1/M$ and distance below $\varepsilon$. For this $\mu_2$ the true ratio $\rho = 1/\mu_2$ exceeds $M$, so

$$P_{\mu_2}(\rho \in C') \le P_{\mu_2}(C' \not\subseteq [-M, M]) \le P_0(C' \not\subseteq [-M, M]) + \varepsilon < 2\varepsilon.$$

Since $\varepsilon$ was arbitrary, the infimum of the coverage is 0. The delta-method interval is finite whenever $b \neq 0$, which has probability 1. $\square$

## Consequences

The examples use paired data with $n = 8$, $\nu = 7$, $t_{(7, 0.975)} = 2.364624$, and the numerator sample $X = (10.2, 8.7, 11.5, 9.9, 12.1, 10.8, 9.4, 11.0)$ with $a = 10.45$, unless they say otherwise. The numbers were computed in floating point.

- **A bounded interval.** With $Y = (5.1, 4.0, 6.2, 4.8, 6.5, 5.6, 4.3, 5.9)$, $b = 5.3$, the t statistic of $\mu_2 = 0$ is 16.64 and $g = 0.0202$. Fieller's 95% interval is $[1.8778, 2.0960]$ around $\hat\rho = 1.9717$. The delta-method interval $[1.8647, 2.0787]$ is close, because $g$ is small.
- **The two differ when $b$ is noisy.** With $Y = (1.9, 0.6, 2.6, 1.2, 2.1, 0.7, 1.8, 1.5)$, $b = 1.55$, the t statistic is 6.35 and $g = 0.139$. Fieller gives $[5.1165, 10.2329]$ and the delta method $[4.5314, 8.9525]$ around $\hat\rho = 6.742$. The Fieller interval is not symmetric about $\hat\rho$; it reaches further toward large ratios, where the data are less informative.
- **Two rays.** With $Y = (0.9, -0.4, 1.6, 0.2, 1.1, -0.3, 0.8, 0.5)$, $b = 0.55$, the t statistic of $\mu_2 = 0$ is 2.252, below 2.3646, so $A < 0$. Here $D > 0$, and $C = (-\infty, -360.08] \cup [9.708, \infty)$. The data say the ratio is at least about 9.7 in size, but cannot fix its sign or bound it. The delta-method interval $[0.0034, 37.997]$ around $\hat\rho = 19.0$ looks informative but is not valid.
- **The whole line.** With $X = (0.6, -0.8, 1.2, 0.1, -0.5, 0.9, -0.2, 0.3)$ and the same $Y$, $Q < t^2$ ($D = -0.0090$), so $C = \mathbb R$. Neither mean is clearly nonzero, and no ratio can be excluded.
- **Measured coverage.** For independent $X_i \sim N(1, 1)$ and $Y_i \sim N(\mu_2, 1)$ with $n = 8$, 20000 simulated samples (seed 4) gave the following coverage of $1/\mu_2$. The Fieller column agrees with Part 1 up to simulation error; the delta-method column shows the failure that Part 4 proves in the limit.

| $\mu_2$ | Fieller | delta method | share of bounded Fieller sets |
|---|---|---|---|
| 2 | 0.9515 | 0.9561 | 0.998 |
| 1 | 0.9492 | 0.9412 | 0.683 |
| 0.5 | 0.9483 | 0.8900 | 0.232 |
| 0.25 | 0.9526 | 0.7904 | 0.090 |

- **Other problems of the same form.** The same inversion applies to any ratio of two coefficients of a normal linear model: the x-intercept $-\beta_0/\beta_1$ of a line, the dose that gives a target response in bioassay (calibration or inverse regression), and the relative potency of two preparations. The slope in [errors-in-variables regression](/errors-in-variables-regression/) has the same difficulty.

## Tightness

- **Unbounded sets cannot be avoided.** Part 4 shows that a procedure with coverage at least $1 - \alpha > 0$ at every parameter value must give an unbounded set with positive probability. Gleser and Hwang (1987) proved the related result that no confidence interval with positive confidence has finite *expected* length in this problem and in errors-in-variables models. This page proves only the "bounded with probability 1" form; Dufour (1997) gives it in general for parameters that are almost unidentified on part of the parameter space.
- **Normality is used.** The exact law of $T$ needs $(a, b)$ normal and the chi-square property of $W$. With large samples and other laws, $T$ is only asymptotically t or normal, and the coverage is only asymptotic.
- **The chi-square condition on $W$ matters.** The proof needs $\nu\, c^\top W c / c^\top \Sigma c$ to be chi-square for every $c$, with the same $\nu$. For two independent samples with unequal unknown variances this fails, and Fieller's set with a Welch-type degrees of freedom is only approximate, as in the [Welch t-test](/welch-t-test/).
- **The coverage is over all samples.** The coverage is exactly $1 - \alpha$ over all samples, bounded sets and unbounded sets together. The theorem says nothing about the coverage among only the samples where the set is bounded, and in the table at $\mu_2 = 0.5$ the sets were bounded in only 23% of the samples.

## History

Fieller derived the confidence limits for a ratio in work on the biological standardization of insulin (1940) and in a 1944 paper on biological assay, and gave the general treatment, including the cases with unbounded sets, in "Some problems in interval estimation" (1954). Creasy (1954) discussed the same problem from a fiducial view. Gleser and Hwang (1987) showed that the unbounded sets are forced by the problem, and Dufour (1997) extended the argument to econometric models with weak identification.

## References
