---
tag: DWDQWW
kind: algorithm
slug: kolmogorov-smirnov-test
name: Kolmogorov-Smirnov test
aliases:
- KS test
- Kolmogorov-Smirnov statistic
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Tests whether a sample comes from a given distribution, or two samples from the same one, by the largest distance between distribution functions.
model: real-ram
complexity:
  vars: {n: the sample size, d: the observed statistic D}
  time: {worst: Θ(n^3 log n), best: Θ(n log n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1933
  people: [Andrey Kolmogorov, Nikolai Smirnov]
  note: Kolmogorov (1933) found the limit law of the largest distance between the empirical and the true distribution function. Smirnov extended the method to one-sided distances and to two samples, and published tables in 1948.
prereqs: [empirical-distribution-function, statistical-hypothesis-test, p-value]
see_also: [anderson-darling-test, dkw-inequality, glivenko-cantelli-theorem, shapiro-wilk-test, chi-squared-goodness-of-fit-test, q-q-plot, mann-whitney-u-test, ballot-theorem]
sources:
  - paper: "A. N. Kolmogorov, Sulla determinazione empirica di una legge di distribuzione, Giornale dell'Istituto Italiano degli Attuari 4, 1933, pages 83 to 91"
    locator: the statistic D_n for a continuous distribution function, the fact that its law does not depend on F, and the limit law of sqrt(n) D_n
  - paper: doi:10.1214/aoms/1177730256
    title: N. Smirnov, Table for estimating the goodness of fit of empirical distributions, Annals of Mathematical Statistics 19(2), 1948
    locator: pp. 279 to 281 (the table of the limit law and its use for one and two samples)
  - paper: doi:10.18637/jss.v008.i18
    title: George Marsaglia, Wai Wan Tsang and Jingbo Wang, Evaluating Kolmogorov's distribution, Journal of Statistical Software 8(18), 2003
    locator: the matrix H, the corrections with h, and the exact P(D_n < d) as (n!/n^n) times an entry of H^n, computed by squaring with rescaling
  - paper: doi:10.1080/01621459.1967.10482916
    title: Hubert W. Lilliefors, On the Kolmogorov-Smirnov test for normality with mean and variance unknown, Journal of the American Statistical Association 62(318), 1967
    locator: pp. 399 to 402 (the Monte Carlo table for the statistic with estimated parameters)
---

The Kolmogorov-Smirnov test checks whether a sample $x_1, \ldots, x_n$ comes from a given continuous distribution function $F_0$. Its statistic is the largest vertical distance $D_n = \sup_t \lvert F_n(t) - F_0(t) \rvert$ between the [empirical distribution function](/empirical-distribution-function/) $F_n$ and $F_0$. After sorting, $D_n$ is the largest of $2n$ simple differences. Under the null hypothesis the law of $D_n$ is the same for every continuous $F_0$, so one exact law serves all models. The page computes this law with the matrix method of Marsaglia, Tsang and Wang, and uses a one-sided finite sum when the tail is small. The two-sample form compares two empirical distribution functions and counts lattice paths for its exact p-value.

## In plain words

A model says how the data should spread out. Sort the data and draw the curve that rises by one step at each data point, from zero to one. Draw the curve of the model on the same picture. If the model is right, the two curves stay close. The test measures the largest vertical gap between them and asks how often a gap this large comes from data that really follow the model.

The answer is the same for every continuous model, because a fixed change of scale turns any such model into the uniform model on zero to one. So one table, or one exact computation, serves every model. Two samples are compared in the same way, with the curve of each sample in place of the model.

## The problem

**Model.** $X_1, \ldots, X_n$ are independent with an unknown distribution function $F$. $F_0$ is a fully specified continuous distribution function.

**Hypotheses.** $H_0$: $F = F_0$. Two-sided $H_1$: $F \ne F_0$. One-sided "greater": $F(t) > F_0(t)$ for some $t$. One-sided "less": $F(t) < F_0(t)$ for some $t$.

**Statistic.** With $u_i = F_0(x_{(i)})$ for the sorted data,

$$D^+ = \sup_t (F_n(t) - F_0(t)) = \max_i \left(\frac{i}{n} - u_i\right), \qquad D^- = \sup_t (F_0(t) - F_n(t)) = \max_i \left(u_i - \frac{i - 1}{n}\right),$$

and $D = \max(D^+, D^-)$. The one-sided tests use $D^+$ or $D^-$.

**Null distribution.** Exact. If $F_0$ is continuous, $U_i = F_0(X_i)$ is uniform on $(0, 1)$ under $H_0$, and $D$, $D^+$ and $D^-$ are functions of the $U_i$ only. So their laws depend on $n$ and not on $F_0$. $D^+$ and $D^-$ have the same law, $P(D^+ \ge d) = d \sum_{j=0}^{\lfloor n(1-d) \rfloor} \binom{n}{j} \left(1 - d - \frac{j}{n}\right)^{n-j} \left(d + \frac{j}{n}\right)^{j-1}$ for $0 < d \le 1$. The two-sided law $P(D < d)$ has no short closed form; line L8 computes it exactly. As $n \to \infty$, $P(\sqrt{n} D > \lambda) \to 2 \sum_{k \ge 1} (-1)^{k-1} e^{-2k^2\lambda^2}$, the Kolmogorov distribution, and $P(\sqrt{n} D^+ > \lambda) \to e^{-2\lambda^2}$.

**P-values.** For an observed value $d$ the two-sided p-value is $P(D \ge d)$, and the one-sided p-values are $P(D^+ \ge d^+)$ and $P(D^- \ge d^-)$. No doubling rule is needed: $D$ is already two-sided. For $d \ge 1/2$ the events $D^+ \ge d$ and $D^- \ge d$ cannot both happen, so $P(D \ge d) = 2P(D^+ \ge d)$ exactly. For every $d$, $P(D \ge d) \le 2 P(D^+ \ge d)$.

**Rejection rule and size.** Reject at level $\alpha$ when $p \le \alpha$. For continuous $F_0$ the exact p-value gives size $\alpha$ when $\alpha$ is a value of the tail function, and at most $\alpha$ always. The exact 5% critical values of $D$ are $0.5633$, $0.4092$, $0.2941$, $0.1884$ and $0.1340$ for $n = 5, 10, 20, 50, 100$. The limit gives $1.3581/\sqrt{n}$, that is $0.6074$, $0.4295$, $0.3037$, $0.1921$ and $0.1358$, so the limit test is conservative for small $n$.

**Sensitivity and power.** The test is consistent against every fixed $F \ne F_0$, because $D_n \to \sup_t \lvert F(t) - F_0(t) \rvert > 0$ by the [Glivenko-Cantelli theorem](/glivenko-cantelli-theorem/). The statistic is a sup over all $t$, and the variance of $F_n(t)$ is largest near the median of $F_0$, so the test reacts most to differences in the middle of the distribution and least to differences in the tails. In a Monte Carlo run against $F_0 = N(0, 1)$ with $n = 20$, $r = 2000$ samples per case and $\alpha = 0.05$, it rejected $51.55\%$ of samples from $N(0.5, 1)$ (seed 62) and $17.5\%$ of samples from $N(0, 1.5^2)$ (seed 63).

## The algorithm

The pseudocode gives the one-sample two-sided test. Here $\mathrm{SMIRNOV}(n, d)$ is the finite sum for $P(D^+ \ge d)$ above, and indices of the $m \times m$ matrix $H$ run from 1.

```pseudo id=main
KOLMOGOROV-SMIRNOV(x_1, ..., x_n, F_0)
L1  sort x; u_i ← F_0(x_(i)) for i = 1, ..., n
L2  D+ ← max_i (i/n - u_i); D- ← max_i (u_i - (i - 1)/n); D ← max(D+, D-)
L3  if D ≥ 1/2 or 2 · SMIRNOV(n, D) < 10^-3 then return D, min(1, 2 · SMIRNOV(n, D))
L4  k ← ⌊nD⌋ + 1; h ← k - nD; m ← 2k - 1
L5  H[i][j] ← 1/(i - j + 1)! if i - j + 1 ≥ 0, else 0, for 1 ≤ i, j ≤ m
L6  H[i][1] ← H[i][1] - h^i/i!; H[m][j] ← H[m][j] - h^(m-j+1)/(m-j+1)!; H[m][1] ← H[m][1] + max(0, 2h - 1)^m/m!
L7  T ← H^n by repeated squaring, rescaling every product by a power of 2
L8  return D, 1 - (n!/n^n) · T[k][k]
```

Lines L1 and L2 compute the statistic: between two data points $F_n$ is constant and $F_0$ is nondecreasing, so the sup of each difference is reached at a data point or just before it. Line L3 handles two cases with the one-sided sum. For $D \ge 1/2$ the doubled one-sided tail is the exact two-sided tail. For a small tail the doubled one-sided tail is an upper bound whose relative excess is tiny; the code measured $8.1 \times 10^{-12}$ at $n = 20$, $d = 0.4$ and $1.7 \times 10^{-11}$ at $n = 40$, $d = 0.3$. Line L3 avoids $1 - P(D < d)$ there, because that subtraction loses the digits of a small tail: the float error of line L8 was $1.1 \times 10^{-8}$ at $n = 40$, $d = 0.45$ and $1.1 \times 10^{-5}$ at $n = 60$, $d = 0.4$. Lines L4 to L8 are the matrix method. The state is how far the count of data points runs ahead of or behind the model line, measured at the steps $1/n$, and $H$ holds the transition weights of one step; line L6 removes the paths that leave the band inside a step. The rescaling of line L7 keeps the entries of $H^n$ in the float range. The code also returns the one-sided p-values from the sum, and the asymptotic p-value from the Kolmogorov series. By default it is exact for $n \le 100$.

**Two samples.** For samples of sizes $m$ and $n$ with distribution functions $F_m$ and $G_n$, the statistic is $D_{m,n} = \sup_t \lvert F_m(t) - G_n(t) \rvert$. Walk through the merged sorted values; after $i$ values of the first sample and $j$ values of the second, $F_m - G_n = (in - jm)/(mn)$. So $D_{m,n} = t/(mn)$ with $t$ the largest $\lvert in - jm \rvert$ at the end of each block of equal values. Under $H_0$ without ties, the order of the labels is uniform over the $\binom{m+n}{m}$ lattice paths from $(0, 0)$ to $(m, n)$. A dynamic program counts the paths that keep $\lvert in - jm \rvert < t$ at every point, and the p-value is one minus their share, in exact integers.

## Example

**One sample.** The model is the exponential law with mean 1, $F_0(t) = 1 - e^{-t}$. The data are $0.42, 0.06, 1.95, 0.88, 0.13, 3.10, 0.27, 0.71, 0.09, 0.35$, so $n = 10$. After sorting, line L1 gives

$$u = (0.0582, 0.0861, 0.1219, 0.2366, 0.2953, 0.3430, 0.5084, 0.5852, 0.8577, 0.9550).$$

Line L2 gives $D^+ = 6/10 - 0.3430 = 0.2570$ at $i = 6$ and $D^- = 0.0582$ at $i = 1$, so $D = 0.2570$. The two-sided tail is not small, so lines L4 to L8 run with $k = 3$, $h = 0.4295$ and a $5 \times 5$ matrix, and give the exact $p = 0.4493$. The one-sided p-values are $0.2267$ for "greater" and $0.9031$ for "less", and the asymptotic two-sided p-value is $0.5234$. The data are compatible with the model. Against the exponential law with mean $0.5$ the same data give $D = D^- = 0.1798$ and $p = 0.8484$, so the test does not separate the two models with ten points.

**The exact law against the limit.** For $n = 10$, $d = 0.3$, the exact tail is $0.2705$ and the limit gives $0.3291$; the bound $2 \cdot \mathrm{SMIRNOV}$ gives $0.2709$. At $n = 10$, $d = 0.41$, which is above the exact 5% point, the exact tail $0.04932$ equals $2 \cdot \mathrm{SMIRNOV}$ to the digits shown, while the limit gives $0.0693$. At $n = 100$, $d = 0.134$ the exact tail is $0.05008$ and the limit gives $0.05513$.

**Two samples.** Take $x = 1.2, 3.4, 2.2, 5.1, 4.4, 3.9$ and $y = 0.3, 1.1, 2.0, 0.9, 1.7, 2.5, 0.5$, so $m = 6$, $n = 7$. After the value $2.0$, one $x$ and six $y$ values are passed, so $G_7 - F_6 = 6/7 - 1/6 = 29/42$, the largest gap. The path count finds $116$ of the $\binom{13}{6} = 1716$ label orders with a gap of at least $29/42$, so $p = 116/1716 = 0.0676$. The limit gives $0.0919$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The probability integral transform makes the null law of $(u_1, \ldots, u_n)$ that of uniform order statistics. Lines L1 and L2 compute the sup because $F_n$ is a step function and $F_0$ is monotone. $D < d$ means that every $u_{(i)}$ lies in the open interval $(i/n - d, (i-1)/n + d)$. Embed the uniforms in a Poisson process: then this event is a band condition on a Markov chain observed at the steps $1/n$, the band has $2k - 1$ integer states, and $H$ is $e$ times the one-step transition matrix inside the band, with line L6 subtracting the paths that leave the band within a step. The sum for $D^+$ follows from the ballot theorem. For $d \ge 1/2$ the two one-sided events are disjoint, and for smaller $d$ the doubled one-sided tail is an upper bound, so every p-value is exact or conservative, and the test has size at most $\alpha$.

## Complexity

Line L1 sorts in $O(n \log n)$ and line L2 is linear. The sum in line L3 has at most $n + 1$ terms. In the matrix branch, $m = 2\lfloor nD \rfloor + 1 \le 2n + 1$, each product of $m \times m$ matrices takes $\Theta(m^3)$ operations, and repeated squaring takes $O(\log n)$ products. So the worst case is $\Theta(n^3 \log n)$ time and $\Theta(n^2)$ space, and in general $\Theta((nD)^3 \log n)$. When line L3 returns, the cost is $\Theta(n \log n)$. Under $H_0$, $D$ is of order $1/\sqrt{n}$, so typical inputs have $m$ of order $\sqrt{n}$ and cost $O(n^{3/2} \log n)$. In the Python code the matrix branch took $0.011$ s of CPU time at $n = 100$, $d = 0.134$. The two-sample statistic takes $O((m + n) \log(m + n))$, and the path count takes $\Theta(mn)$ additions of integers of at most $m + n$ bits.

## Properties

- **Distribution-free.** For continuous $F_0$ the null law of $D$ depends only on $n$.
- **Invariant.** $D$ does not change under any increasing transformation applied to both the data and the model.
- **Confidence band.** The exact critical value $c_\alpha$ gives the band $F_n(t) \pm c_\alpha$, which holds the whole of $F$ with probability at least $1 - \alpha$. The [DKW inequality](/dkw-inequality/) gives the simpler and slightly wider band $F_n(t) \pm \sqrt{\ln(2/\alpha)/(2n)}$.
- **Parameters must be fixed in advance.** If the parameters of $F_0$ are estimated from the same data, the model follows the data, $D$ becomes smaller, and the null law changes. In a Monte Carlo run with normal data, $n = 20$, $r = 2000$ samples and seed 61, the test with the estimated mean and standard deviation and the standard p-value rejected none of the 2000 samples at the nominal $5\%$. The Lilliefors test uses the correct null law for this case.
- **Discrete models.** If $F_0$ has jumps, $D$ is at most the statistic of the underlying uniforms, so the standard p-values are conservative.
- **Monte Carlo size.** With uniform data, $n = 10$, $r = 4000$ samples and seed 64, the exact test rejected $4.325\%$ of samples at $\alpha = 0.05$.

## Variants and improvements

- **One-sided tests.** $D^+$ and $D^-$ with the finite sum, or with the limit $e^{-2n d^2}$ for large $n$.
- **Two-sample test.** The lattice-path count gives the exact p-value without ties. With ties, the statistic is evaluated only at the ends of tie blocks, which can only lower it, so the same p-value is conservative.
- **Estimated parameters.** The Lilliefors test (Lilliefors 1967) keeps $D$ but takes its null law from a simulation with the parameters estimated in each simulated sample. A [parametric bootstrap](/parametric-bootstrap/) does the same for any model.
- **Weighted distances.** The [Anderson-Darling test](/anderson-darling-test/) integrates the squared difference with a weight that grows in the tails, and so has more power against differences in the tails. The Cramer-von Mises test uses the unweighted integral.
- **Normality.** For the composite hypothesis of normality the [Shapiro-Wilk test](/shapiro-wilk-test/) usually has more power.
- **Binned data.** The [chi-squared goodness-of-fit test](/chi-squared-goodness-of-fit-test/) works with counts in classes and allows estimated parameters with a change of the degrees of freedom.

## When to use it

Use it to test a fully specified continuous model, or to compare two samples against any kind of difference, when a single number with an exact p-value is wanted. It is a good first check with a direct picture: the gap between the two curves. For a location shift between two samples the [Mann-Whitney test](/mann-whitney-u-test/) has more power, and for differences in the tails the Anderson-Darling test does. Pair it with a [Q-Q plot](/q-q-plot/) to see where the data and the model differ.

## Pitfalls

- **Estimating the parameters from the same data.** The standard p-values are then much too large; in the run above the test never rejected at $5\%$.
- **Using the limit for small $n$.** At $n = 10$, $d = 0.41$ the limit gave $0.0693$ against the exact $0.0493$.
- **Discrete data.** Ties and jumps in $F_0$ make the standard p-values conservative, and sometimes very much so.
- **Low power in the tails.** A model that is wrong only in the tails is often accepted. With $n = 20$ the test detected a 50% larger standard deviation in only $17.5\%$ of samples.
- **Cancellation.** Computing a small two-sided tail as $1 - P(D < d)$ loses digits. Use the one-sided sum there, as line L3 does.
- **Conventions.** Some programs call the alternative "greater" when $F > F_0$, which means the data tend to be smaller than the model. Check which sign the program uses.

## Implementations

## History

Andrey Kolmogorov (1933) defined $D_n$ for a continuous distribution function, showed that its law does not depend on $F$, and found the limit law of $\sqrt{n} D_n$. In the same volume of the same journal, Glivenko proved that $D_n \to 0$ for continuous $F$, and Cantelli extended this to every $F$. Nikolai Smirnov studied the one-sided statistics and the two-sample statistic, and published tables of the limit laws in 1948. The finite sum for the one-sided law is due to Smirnov and to Birnbaum and Tingey (1951). Durbin wrote the exact two-sided law as a matrix power, and Marsaglia, Tsang and Wang (2003) turned it into a fast and accurate program. Lilliefors (1967) showed by simulation that estimating the parameters of a normal model changes the null law, and gave a corrected table.

## References
