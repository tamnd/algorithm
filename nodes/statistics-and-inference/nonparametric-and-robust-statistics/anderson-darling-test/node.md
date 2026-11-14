---
tag: 7ZCNKW
kind: algorithm
slug: anderson-darling-test
name: Anderson-Darling test
aliases:
- Anderson-Darling statistic
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: A goodness-of-fit test by a weighted squared distance between the empirical and the model CDF, with weights that stress the tails.
model: real-ram
complexity:
  vars: {n: the sample size, b: the number of simulated samples for the Monte Carlo p-value}
  time: {worst: Θ(b n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1952
  people: [Theodore W. Anderson, Donald A. Darling]
  note: Anderson and Darling (1952) defined weighted distances between the empirical and the model distribution function and found their limit laws. In 1954 they gave the computing formula for the statistic with the tail weight and a table of its limit law.
prereqs: [kolmogorov-smirnov-test, empirical-distribution-function, statistical-hypothesis-test]
see_also: [shapiro-wilk-test, chi-squared-goodness-of-fit-test, q-q-plot, parametric-bootstrap, permutation-test, karhunen-loeve-theorem, legendre-polynomials, simpsons-rule]
sources:
  - paper: doi:10.1214/aoms/1177729437
    title: T. W. Anderson and D. A. Darling, Asymptotic theory of certain goodness of fit criteria based on stochastic processes, Annals of Mathematical Statistics 23(2), 1952
    locator: pp. 193 to 212 (the weighted criteria, the weight 1/(F(1 - F)), and the limit law as a weighted sum of chi-square variables)
  - paper: "T. W. Anderson and D. A. Darling, A test of goodness of fit, Journal of the American Statistical Association 49, 1954, pages 765 to 769"
    locator: the computing formula for A^2 from the sorted values and the series for the limit law with its percentage points
  - paper: doi:10.18637/jss.v009.i02
    title: George Marsaglia and John Marsaglia, Evaluating the Anderson-Darling distribution, Journal of Statistical Software 9(2), 2004
    locator: the accurate evaluation of the limit law and its percentiles, and a correction for finite n
---

The Anderson-Darling test checks whether a sample $x_1, \ldots, x_n$ comes from a given continuous distribution function $F_0$. Its statistic is

$$A^2 = n \int_{-\infty}^{\infty} \frac{(F_n(t) - F_0(t))^2}{F_0(t)(1 - F_0(t))} \, dF_0(t),$$

the squared distance between the [empirical distribution function](/empirical-distribution-function/) $F_n$ and $F_0$, with each point weighted by the inverse of the variance of $F_n(t)$. The weight is large in both tails, so the test reacts to differences in the tails that the [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/) misses. After sorting, $A^2$ is a sum of $n$ logarithms. Its null law does not depend on $F_0$, and the page takes the p-value from the limit law or from a Monte Carlo simulation of uniform samples.

## In plain words

A model says how the data should spread out. Compare the share of data below each point with the share that the model expects. A gap of a given size is more surprising in the tails than in the middle, because few points fall in the tails, so the shares there should match closely. The test squares each gap, divides it by how much the gap usually varies at that point, and adds the results over the whole range.

A large total means that the data and the model disagree somewhere, often in a tail. The same table serves every continuous model, because a fixed change of scale turns any such model into the uniform model. For a small sample one can also simulate many uniform samples and count how often their total is at least as large.

## The problem

**Model.** $X_1, \ldots, X_n$ are independent with an unknown distribution function $F$. $F_0$ is a fully specified continuous distribution function.

**Hypotheses.** $H_0$: $F = F_0$. $H_1$: $F \ne F_0$.

**Statistic.** With $u_i = F_0(x_{(i)})$ for the sorted data,

$$A^2 = -n - \frac{1}{n} \sum_{i=1}^{n} (2i - 1) \left[\ln u_i + \ln(1 - u_{n+1-i})\right].$$

It equals the integral above. If some $u_i$ is 0 or 1, the integral is infinite.

**Null distribution.** Under $H_0$, $u_1, \ldots, u_n$ are the order statistics of $n$ independent uniforms, so the law of $A^2$ depends on $n$ and not on $F_0$. For $n = 1$, $A^2 = -1 - \ln u - \ln(1 - u)$ and $P(A^2 \le a) = \sqrt{1 - 4e^{-(1+a)}}$ for $a \ge \ln 4 - 1 = 0.3863$. For larger $n$ the exact law has no closed form. As $n \to \infty$, $A^2$ converges in law to $A^2_\infty = \sum_{j \ge 1} Z_j^2 / (j(j+1))$ with independent standard normal $Z_j$; its mean is 1. The page uses this limit, which is asymptotic, or a Monte Carlo estimate of the exact law.

**P-values.** The test is one-sided in $A^2$: large values speak against $H_0$, and no doubling rule applies. The asymptotic p-value is $1 - \mathrm{ADINF}(A^2)$, with $\mathrm{ADINF}$ the distribution function of $A^2_\infty$. The Monte Carlo p-value is $(1 + c)/(1 + b)$, where $c$ is the number of $b$ simulated uniform samples of size $n$ whose statistic is at least the observed one.

**Rejection rule and size.** Reject at level $\alpha$ when $p \le \alpha$. The Monte Carlo p-value gives size at most $\alpha$ for every $n$ and $b$. The percentiles of the limit law are $0.7742$ (50%), $1.933$ (90%), $2.4924$ (95%), $3.0775$ (97.5%) and $3.8781$ (99%). The limit test is close to the exact one already for small $n$. In a Monte Carlo run with $r = 20000$ uniform samples per case, the simulated 95% points were $2.4973$, $2.5313$ and $2.5402$ for $n = 5$, $10$ and $20$ (seeds 71, 72 and 73), and the limit test at $5\%$ rejected $5.04\%$, $5.26\%$ and $5.275\%$ of the samples.

**Sensitivity and power.** The test is consistent against every fixed $F \ne F_0$. The weight $1/(F_0(1 - F_0))$ makes it more sensitive than the Kolmogorov-Smirnov test to differences in the tails and in spread. In a Monte Carlo run against $F_0 = N(0, 1)$ with $n = 20$, $r = 2000$ samples per case and $\alpha = 0.05$, both tests on the same samples gave these rejection rates:

| Data | Seed | Anderson-Darling | Kolmogorov-Smirnov |
|---|---|---|---|
| $N(0.5, 1)$ | 62 | $0.604$ | $0.5155$ |
| $N(0, 1.5^2)$ | 63 | $0.4805$ | $0.175$ |
| Student $t$ with 3 degrees of freedom | 65 | $0.3295$ | $0.066$ |
| $N(0, 0.6^2)$ | 66 | $0.068$ | $0.099$ |

The last row shows a weak point: against a smaller spread, a sample of 20 points has no values far in the tails, and the test has almost no power.

## The algorithm

```pseudo id=main
ANDERSON-DARLING(x_1, ..., x_n, F_0, method, b)
L1  u ← the values F_0(x_i), sorted
L2  if u_1 = 0 or u_n = 1 then return ∞, 0
L3  S ← sum over i = 1, ..., n of (2i - 1) · (ln u_i + ln(1 - u_(n+1-i)))
L4  A² ← -n - S/n
L5  if method = asymptotic then return A², 1 - ADINF(A²)
L6  c ← number of j = 1, ..., b where A² of a sorted sample of n uniforms ≥ A²
L7  return A², (1 + c)/(1 + b)
```

Lines L1 to L4 compute the statistic. The code uses `log1p` for $\ln(1 - u)$, so values of $u$ near 0 keep their digits, and a compensated sum for $S$. $\mathrm{ADINF}$ evaluates the series of Anderson and Darling (1954) in the form of Marsaglia and Marsaglia (2004),

$$\mathrm{ADINF}(z) = \frac{\sqrt{2\pi}}{z} \sum_{j \ge 0} \binom{-1/2}{j} (4j + 1) e^{-a_j} \int_0^\infty \exp\left(\frac{z}{8(w^2 + 1)} - a_j w^2\right) dw, \qquad a_j = \frac{(4j+1)^2 \pi^2}{8z}.$$

The terms fall fast, and the code stops when a term is below $10^{-17}$. Each integral uses [Simpson's rule](/simpsons-rule/) on $[0, W]$, where $W$ is chosen so that the integrand is below $e^{-40}$ beyond $W$. Lines L6 and L7 simulate the exact null law with a seeded generator; this is a Monte Carlo test, and the p-value has a random part of standard deviation about $\sqrt{p(1-p)/b}$.

## Example

The model is the exponential law with mean 1, $F_0(t) = 1 - e^{-t}$, and the data are those of the Kolmogorov-Smirnov page: $0.42, 0.06, 1.95, 0.88, 0.13, 3.10, 0.27, 0.71, 0.09, 0.35$. Line L1 gives

$$u = (0.0582, 0.0861, 0.1219, 0.2366, 0.2953, 0.3430, 0.5084, 0.5852, 0.8577, 0.9550).$$

The first term of $S$ is $1 \cdot (\ln 0.0582 + \ln(1 - 0.9550))$, which pairs the smallest and the largest value. In total $S = -107.9589$, so $A^2 = -10 + 10.7959 = 0.7959$. The limit law gives $p = 0.4840$. The Monte Carlo p-value with $b = 9999$ and seed 7 is $0.4813$. The Kolmogorov-Smirnov test gave $p = 0.4493$ on the same data, so both tests accept the model. Against the exponential law with mean $0.5$, $A^2 = 0.8448$ and $p = 0.4498$.

**One observation.** For $n = 1$ the smallest value of $A^2$ is $\ln 4 - 1 = 0.3863$, at $u = 1/2$. The formula above gives $P(A^2 \le 1) = 0.6772$ and $P(A^2 \le 2) = 0.8949$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). On each interval between two sorted values, $F_n$ is a constant $c$, and the integrand is $c^2/t + (1 - c)^2/(1 - t) - 1$ in the variable $t = F_0$. Integrating these pieces and collecting the logarithms by summation by parts gives the formula of lines L3 and L4. The probability integral transform shows that the null law of $A^2$ is that of uniform samples, so the simulated values in line L6 have the exact null law. The observed and the $b$ simulated values are then exchangeable, and the rank argument gives $P(p \le \alpha) \le \alpha$ for the p-value of line L7. The asymptotic p-value relies on the limit law, which we cite.

## Complexity

Line L1 sorts in $\Theta(n \log n)$ and lines L2 to L4 are linear, so the statistic costs $\Theta(n \log n)$ time and $\Theta(n)$ space. The asymptotic p-value costs a fixed amount of work for a given accuracy: a few terms of the series, each with a fixed number of Simpson steps. The Monte Carlo p-value sorts $b$ samples of size $n$, which costs $\Theta(b n \log n)$ time and $\Theta(n)$ extra space.

## Properties

- **Distribution-free.** For continuous $F_0$ the null law of $A^2$ depends only on $n$.
- **Invariant.** $A^2$ does not change under an increasing transformation applied to both the data and the model.
- **Tail weight.** The variance of $F_n(t)$ is $F_0(t)(1 - F_0(t))/n$ under $H_0$. Dividing by it gives every point the same null variance, so a gap in a tail counts as much as a gap of the same number of standard deviations in the middle.
- **Structure of the limit.** The limit $\sum_j Z_j^2/(j(j+1))$ comes from the [Karhunen-Loeve](/karhunen-loeve-theorem/) expansion of the weighted Brownian bridge $B(t)/\sqrt{t(1-t)}$, whose eigenfunctions are built from [Legendre polynomials](/legendre-polynomials/).
- **Parameters must be fixed in advance.** In a Monte Carlo run with normal data, $n = 20$, $r = 2000$ samples and seed 67, the test with the estimated mean and standard deviation and the limit 95% point rejected none of the samples.

## Variants and improvements

- **Estimated parameters.** For normal, exponential and other families, tables for $A^2$ with estimated parameters exist, often for a modified statistic, $A^2$ times a factor that depends on $n$. A [parametric bootstrap](/parametric-bootstrap/) gives the null law for any model.
- **Finite-n correction.** Marsaglia and Marsaglia (2004) give a correction to the limit law for finite $n$.
- **Cramer-von Mises.** The same integral without the weight gives the Cramer-von Mises statistic $W^2$, which is closer to the Kolmogorov-Smirnov test in where it looks.
- **k samples.** Scholz and Stephens extended the statistic to compare several samples, with a permutation null law as for a [permutation test](/permutation-test/).
- **Other tests.** For normality the [Shapiro-Wilk test](/shapiro-wilk-test/) is a strong alternative; for counts in classes, the [chi-squared goodness-of-fit test](/chi-squared-goodness-of-fit-test/).

## When to use it

Use it to test a fully specified continuous model when differences in the tails matter, as in risk models, reliability, or before a method that relies on the tails of a model. With estimated parameters, use the matching table or a parametric bootstrap. Look at a [Q-Q plot](/q-q-plot/) as well, to see where the data and the model differ.

## Pitfalls

- **Estimated parameters.** Using the standard table after estimating the parameters makes the test far too conservative; in the run above it never rejected at $5\%$.
- **Values at the edge of the support.** If $F_0(x_i)$ is 0 or 1, as for a value outside the support of the model, $A^2$ is infinite. In floating point a value far in a tail can round $F_0$ to 1; compute $1 - F_0$ directly from the survival function of the model when possible.
- **Discrete data.** Ties and jumps in $F_0$ change the null law; the continuous tables do not apply.
- **Little power against a smaller spread.** With $n = 20$ the test rejected $N(0, 0.6^2)$ against $N(0, 1)$ in only $6.8\%$ of samples.
- **Old tables.** Older tables list $3.857$ for the 1% point of the limit law. The series gives $\mathrm{ADINF}(3.857) = 0.98976$, and the 99% point is $3.8781$ (Marsaglia and Marsaglia 2004).

## Implementations

## History

Theodore Anderson and Donald Darling (1952) studied a family of distances between the empirical and the model distribution function, weighted by a function of $F_0$, and found their limit laws through the eigenvalues of the weighted Brownian bridge. In a short paper in 1954 they singled out the weight $1/(F_0(1 - F_0))$, gave the computing formula with logarithms, and gave a table of the limit law from a series. Stephens later gave modified statistics and tables for the case of estimated parameters. Marsaglia and Marsaglia (2004) gave an accurate program for the limit law and a correction for finite samples.

## References
