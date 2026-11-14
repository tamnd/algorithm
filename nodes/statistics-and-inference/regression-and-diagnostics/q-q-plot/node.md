---
tag: XSYFTG
kind: technique
slug: q-q-plot
name: Q-Q plot
aliases:
- quantile-quantile plot
- normal probability plot
area: statistics-and-inference/regression-and-diagnostics
level: intro
summary: Plots the ordered sample against the matching quantiles of a reference distribution. Points near a line mean the distributions agree up to location and scale.
prereqs: [quantile, empirical-distribution-function]
see_also: [order-statistic, shapiro-wilk-test, kolmogorov-smirnov-test, anderson-darling-test, studentized-residual, box-cox-transformation, kernel-density-estimation, fractional-factorial-design]
sources:
  - paper: doi:10.1093/biomet/55.1.1
    title: "M. B. Wilk and R. Gnanadesikan, Probability plotting methods for the analysis of data, Biometrika 55(1), 1968, pp. 1 to 17"
    locator: The whole paper (Q-Q and P-P plots, their reading for location, scale and shape, and the two-sample Q-Q plot)
  - paper: doi:10.1080/00401706.1975.10489279
    title: "James J. Filliben, The probability plot correlation coefficient test for normality, Technometrics 17(1), 1975, pp. 111 to 117"
    locator: The whole paper (the correlation of the normal probability plot as a test statistic, the median plotting positions and the table of critical values)
---

A Q-Q plot compares a sample with a reference distribution, or two samples with each other, by plotting quantile against quantile. The sorted data $x_{(1)} \le \dots \le x_{(n)}$ go on one axis and the reference quantiles $F^{-1}(p_i)$ at matching probabilities $p_i \approx i/n$ on the other. If the data come from $F$ up to a location $\mu$ and a scale $\sigma$, the points lie near a straight line with intercept $\mu$ and slope $\sigma$, so one plot checks the shape of the distribution without estimating $\mu$ or $\sigma$ first. The ways the points leave the line show how the distributions differ: curvature for skewness, an S shape for tail weight, isolated points for outliers, steps for ties. The normal Q-Q plot of the residuals is the standard check of the normality assumption in regression.

## In plain words

Sort the data. If there are 8 values, the smallest should sit near the point that cuts off the lowest sixteenth of the reference curve, the next near the point that cuts off three sixteenths, and so on. Plot each sorted value against the place where it "should" be. If the guess about the shape is right, the points form a straight line. Its height and steepness are the center and the spread, which we did not need to know. If the points bend, the shape is wrong, and the bend says how: a curve means the data lean to one side, an S means the extremes are farther out (or closer in) than the guess allows. A plot is a picture, not a proof. With few points, even data from the right curve wobble a lot.

## When it applies

- The question is about the *shape* of a distribution: normal or not, heavy tails or not, skewed or not, the same shape in two groups or not.
- The reference distribution $F$ is continuous with a quantile function $F^{-1}$ that can be computed, and the candidate model is a location-scale family $\{F((x - \mu)/\sigma)\}$. For a family with a shape parameter (gamma, Weibull), fix the shape or estimate it first.
- The observations are roughly independent and identically distributed. For regression residuals, use [studentized residuals](/studentized-residual/), which have equal variances; raw residuals do not, and they are also correlated, so a Q-Q plot of them is only approximate.
- The sample is not tiny. Below about 10 points, random wiggle hides all but large departures.

## The template

The plot takes the sample $x_1, \dots, x_n$, a reference quantile function $F^{-1}$ and a plotting constant $a \in [0, 1)$.

```pseudo id=main
QQ-PLOT(x[1..n], F⁻¹, a)                          ▷ a = 1/2 (Hazen), 3/8 (Blom), 0 (Weibull)
L1  sort x into x(1) ≤ x(2) ≤ ... ≤ x(n)
L2  for i = 1 to n do
L3      p_i ← (i − a) / (n + 1 − 2a)                  ▷ plotting position
L4      q_i ← F⁻¹(p_i)                                ▷ reference quantile
L5      draw the point (q_i, x(i))
L6  Q1, Q3 ← the lower and upper sample quartiles of x
L7  draw the line through (F⁻¹(1/4), Q1) and (F⁻¹(3/4), Q3)
L8  r ← sample correlation of (q_1, ..., q_n) and (x(1), ..., x(n))   ▷ optional numeric summary
```

**Why a straight line.** Let $X = \mu + \sigma Z$ with $Z \sim F$ continuous. The quantile of $X$ at $p$ is $\mu + \sigma F^{-1}(p)$. The sample quantile $x_{(i)}$ estimates the quantile of $X$ at about $i/n$, and by the Glivenko-Cantelli theorem for the [empirical distribution function](/empirical-distribution-function/) these estimates converge almost surely at every $p$ where the quantile of $X$ is unique. So the points $(F^{-1}(p_i), x_{(i)})$ approach the line $x = \mu + \sigma q$. If $X$ has another distribution $G$, they approach the curve $q \mapsto G^{-1}(F(q))$, which is a straight line only when $G$ is in the location-scale family of $F$.

**Plotting positions.** $F(X_{(i)})$ has the Beta$(i, n + 1 - i)$ law, with mean $i/(n + 1)$ (Weibull, $a = 0$) and median close to $(i - 1/3)/(n + 1/3)$. Blom's $a = 3/8$ makes $F^{-1}(p_i)$ close to $E[Z_{(i)}]$ for the normal law. Hazen's $a = 1/2$ is the midpoint of the $i$th of $n$ equal cells. All choices are symmetric around $1/2$ and agree as $n$ grows; they differ mostly in the two extreme points. For $n = 5$ and the normal reference, the quantiles are $\pm 1.2816, \pm 0.5244, 0$ (Hazen), $\pm 1.1798, \pm 0.4972, 0$ (Blom) and $\pm 0.9674, \pm 0.4307, 0$ (Weibull).

**The reference line.** The line in L7 goes through the quartiles and is robust: a few wild points do not move it. A least squares line through all points would be pulled by the very tails that the plot should show.

**Reading the shapes.** With the reference on the horizontal axis:

| pattern | meaning |
|---|---|
| straight line | same shape as $F$; intercept $\approx \mu$, slope $\approx \sigma$ |
| convex (both ends above the line) | right skew: long upper tail, short lower tail |
| concave | left skew |
| S shape, low end below and high end above | heavier tails than $F$ |
| reversed S | lighter tails than $F$ |
| a few points far off the line at the ends | outliers |
| horizontal steps | ties, rounding or a discrete distribution |
| two straight pieces | a mixture of two populations |

**Cost.** Sorting dominates: $O(n \log n)$ time and $O(n)$ space.

**Example.** The eight values $x = (0.1, 0.2, 0.4, 0.5, 0.9, 1.3, 2.0, 3.6)$ with Hazen positions $p_i = (i - 1/2)/8$:

| $i$ | $x_{(i)}$ | normal $q_i$ | exponential $q_i = -\log(1 - p_i)$ |
|---|---|---|---|
| 1 | 0.1 | $-1.5341$ | 0.0645 |
| 2 | 0.2 | $-0.8871$ | 0.2076 |
| 3 | 0.4 | $-0.4888$ | 0.3747 |
| 4 | 0.5 | $-0.1573$ | 0.5754 |
| 5 | 0.9 | 0.1573 | 0.8267 |
| 6 | 1.3 | 0.4888 | 1.1632 |
| 7 | 2.0 | 0.8871 | 1.6740 |
| 8 | 3.6 | 1.5341 | 2.7726 |

Against the normal quantiles the points are convex: with the quartile line $x = 0.9125 + 0.834q$ (sample quartiles 0.35 and 1.475), the lowest two and the highest two points lie above the line, the middle four lie below it, and the top point is 1.41 above it. That is right skew. The correlation is $r = 0.9146$. Against the exponential quantiles the points are close to a line, $r = 0.9966$. The logarithms of the data against normal quantiles give $r = 0.9960$, so a log-normal model also fits. In a simulation with 20000 normal samples of size 8 (seed 11), 6.9% of the correlations were below 0.9146 and the 5% point was 0.906. So the normal plot looks skewed, but a test at the 5% level based on $r$ does not reject normality with only 8 points. The plot suggests; it does not decide.

## Classic examples

- **Residual normality in regression.** Plot the [studentized residuals](/studentized-residual/) against $t_{n-p-1}$ or normal quantiles. This checks the normality behind the exact t and [F-tests](/regression-f-test/). Heavy tails matter more than mild skew.
- **Choosing a transformation.** Q-Q plots before and after a log or a [Box-Cox transformation](/box-cox-transformation/) show whether the new scale removed the skew, as in the example.
- **Correlation tests of normality.** Filliben's (1975) test uses $r$ from L8 with median plotting positions. The Shapiro-Francia statistic is $r^2$ with $E[Z_{(i)}]$ as the positions, and the [Shapiro-Wilk test](/shapiro-wilk-test/) refines it with the covariances of the normal order statistics.
- **Comparing two samples.** Plot the quantiles of one sample against those of the other. A line through the origin with slope 1 means the same distribution; a shift or a change of spread shows as intercept or slope. The [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/) measures the largest vertical gap between the two distribution functions, which the Q-Q plot shows on the quantile scale.
- **Half-normal plots of effects.** In a two-level [factorial design](/fractional-factorial-design/), the absolute effect estimates are plotted against half-normal quantiles. The inactive effects fall on a line through 0, and the active effects stand out above it (Daniel's method).

## Variations

- **P-P plot.** Plots $F((x_{(i)} - \hat\mu)/\hat\sigma)$ against $p_i$. It needs estimates of $\mu$ and $\sigma$, is most sensitive in the center and compresses the tails; the Q-Q plot is the opposite.
- **Detrended Q-Q plot.** Plots $x_{(i)} - (\hat\mu + \hat\sigma q_i)$ against $q_i$, so small departures from the line are easier to see.
- **Confidence bands.** Pointwise bands come from the Beta$(i, n + 1 - i)$ law of $F(X_{(i)})$ (see [order statistic](/order-statistic/)). Simultaneous bands come from the Kolmogorov-Smirnov band of the empirical distribution function. Pointwise bands are much narrower, so a few points outside them are expected.
- **Discrete and censored data.** Use mid-ranks or the Kaplan-Meier estimate for the positions.
- **Tail-weighted tests.** The [Anderson-Darling test](/anderson-darling-test/) weights the tails, where the Q-Q plot shows the most and correlation tests use the least.

## Pitfalls

- **Overreading small samples.** With $n = 8$ a normal sample can look clearly skewed, as the simulation above shows. Compare with plots of simulated samples from the reference, or add bands.
- **Plotting raw residuals.** Raw regression residuals have variances $\sigma^2(1 - h_{ii})$ and are correlated. Use studentized residuals.
- **Estimating $\mu$ and $\sigma$ and then testing with fixed-parameter critical values.** The correlation $r$ does not depend on $\mu$ and $\sigma$, but a Kolmogorov-Smirnov test with estimated parameters needs adjusted critical values (Lilliefors).
- **Axis order.** Some programs put the data on the horizontal axis. Then convex and concave swap meaning. Read the axis labels before reading the shape.
- **A good line is not a proof of the model.** The plot cannot see dependence, and it has little power against close alternatives.

## Exercises

1. Show that the correlation $r$ of line L8 does not change when the data are replaced by $\alpha + \beta x_i$ with $\beta > 0$, and that it does not depend on the location and scale of $F$.
2. Prove that $E[F(X_{(i)})] = i/(n + 1)$ for a continuous $F$, using the law of uniform order statistics.
3. For $X \sim G$ and reference $F$, both continuous and strictly increasing, show that the limit curve of the Q-Q plot is $q \mapsto G^{-1}(F(q))$, and that it is a line if and only if $G(x) = F((x - \mu)/\sigma)$ for some $\mu$ and $\sigma > 0$.
4. Sketch the limit curve of a normal Q-Q plot for data from $t_3$ and from the uniform law on $(0, 1)$, and say which one is S-shaped.
5. Compute the Blom positions and the normal quantiles for $n = 4$.

## References
