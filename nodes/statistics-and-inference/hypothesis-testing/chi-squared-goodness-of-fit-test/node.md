---
tag: B43M8J
kind: algorithm
slug: chi-squared-goodness-of-fit-test
name: Pearson's chi-squared goodness-of-fit test
aliases:
- chi-squared goodness-of-fit test
- Pearson chi-squared test
area: statistics-and-inference/hypothesis-testing
level: intro
summary: Compares observed category counts with expected counts by the sum of (O - E)^2 / E, which is asymptotically chi-squared under the null.
model: real-ram
complexity:
  vars: {k: the number of categories}
  time: {worst: Θ(k), best: Θ(k)}
  space: {extra: Θ(k)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1900
  people: [Karl Pearson, Ronald A. Fisher, Herman Chernoff, Erich L. Lehmann]
  note: Pearson introduced the statistic and its chi-square reference in 1900. Fisher corrected the degrees of freedom for fitted parameters in 1922 and 1924. Chernoff and Lehmann treated estimates from ungrouped data in 1954.
prereqs: [statistical-hypothesis-test, p-value, binomial-test]
see_also: [chi-squared-test-of-independence, likelihood-ratio-test, wilks-theorem, score-test, kolmogorov-smirnov-test, anderson-darling-test, maximum-likelihood-estimation, central-limit-theorem]
sources:
  - paper: doi:10.1080/14786440009463897
    title: Karl Pearson, On the criterion that a given system of deviations from the probable in the case of a correlated system of variables is such that it can be reasonably supposed to have arisen from random sampling, Philosophical Magazine, series 5, 50(302), 1900
    locator: pp. 157 to 175 (the statistic and its chi-square reference)
  - paper: doi:10.2307/2340521
    title: Ronald A. Fisher, On the interpretation of χ² from contingency tables, and the calculation of P, Journal of the Royal Statistical Society 85(1), 1922
    locator: pp. 87 to 94 (the degrees of freedom when parameters are estimated)
  - paper: doi:10.1214/aoms/1177728726
    title: Herman Chernoff and Erich L. Lehmann, The use of maximum likelihood estimates in χ² tests for goodness of fit, Annals of Mathematical Statistics 25(3), 1954
    locator: pp. 579 to 586 (the limit law with estimates from ungrouped data)
  - book: isbn:9780470463635
    title: Alan Agresti, Categorical Data Analysis, third edition, Wiley, 2013
    locator: Chapter 1 (inference for multinomial parameters, the Pearson and likelihood-ratio statistics)
---

Pearson's chi-squared goodness-of-fit test asks whether counts in $k$ categories agree with a stated set of category probabilities. It compares each observed count $O_i$ with the count $E_i$ that the null hypothesis expects and adds up $(O_i - E_i)^2/E_i$. Under the null, for large samples, this sum has approximately the chi-square law with $k - 1$ degrees of freedom, less one for each parameter fitted from the counts. The test is approximate: its size is close to $\alpha$ only when the expected counts are not too small.

## In plain words

Roll a die 60 times. If it is fair, each face should come up about 10 times. You never get exactly 10 of each, so the question is whether the differences are larger than chance would give. For each face, square the difference between what you saw and what you expected, and divide by what you expected, so that a miss of 5 counts more when you expected 10 than when you expected 1000. Add the six numbers. A fair die gives a total near 5 on average. A total of 13.4 happens by chance only about 2% of the time.

## The problem

**Model.** $n$ independent observations, each falling in one of $k \ge 2$ categories. Category $i$ has probability $p_i$. The counts $(O_1, \ldots, O_k)$ are multinomial with $\sum_i O_i = n$.

**Hypotheses.** Simple null $H_0$: $p = p^0$ for given $p^0_i > 0$. Composite null: $p = p(\theta)$ for some $\theta$ in an $s$-dimensional family. The alternative is any other $p$. There is no direction: every kind of misfit increases the statistic.

**Statistic.** With $E_i = n p^0_i$ (or $n p_i(\hat\theta)$),

$$X^2 = \sum_{i = 1}^k \frac{(O_i - E_i)^2}{E_i}.$$

The likelihood-ratio form is $G = 2 \sum_i O_i \log(O_i/E_i)$, with $0 \log 0 = 0$.

**Null distribution.** Asymptotic only: as $n \to \infty$ with $p^0$ fixed, $X^2$ tends to $\chi^2_{k - 1}$. If $\theta$ is estimated by maximum likelihood from the grouped counts, the limit is $\chi^2_{k - 1 - s}$. If $\theta$ is estimated from the raw, ungrouped observations, the limit lies between $\chi^2_{k - 1 - s}$ and $\chi^2_{k - 1}$ (Chernoff and Lehmann 1954).

**Rejection rule and size.** Reject when $p \le \alpha$, that is when $X^2 \ge \chi^2_{(k - 1 - s,\ 1 - \alpha)}$, the upper $\alpha$ point. The size tends to $\alpha$ (proved for a simple null). For finite $n$ the size is not controlled: it can be above or below $\alpha$, as the exact computations below show.

**P-values.** $p = P(\chi^2_{k - 1 - s} > X^2)$, the upper tail only.

**Sensitivity and power.** Under a fixed alternative $p^1$, the power tends to 1. For alternatives near the null, $X^2$ is approximately noncentral chi-square with noncentrality $\lambda = n \sum_i (p^1_i - p^0_i)^2/p^0_i$. The test spreads its power over all $k - 1$ directions, so a test aimed at one kind of departure (a trend over ordered categories, for example) can be much more powerful against that departure.

## The algorithm

```pseudo id=main
CHI-SQUARED-GOF(O[1..k], p[1..k], s)
L1  n ← O[1] + ... + O[k]
L2  for i ← 1 to k do E[i] ← n · p[i]
L3  X2 ← Σ (O[i] - E[i])^2 / E[i]          ▷ or G ← 2 Σ over O[i] > 0 of O[i] log(O[i] / E[i])
L4  df ← k - 1 - s                         ▷ s = number of parameters fitted from these counts
L5  return (X2, df, P(χ²_df > X2))
```

The caller passes the null probabilities. If parameters were fitted, the caller computes $p_i(\hat\theta)$ from the grouped counts and passes $s$. Line L5 uses `chi2_sf` from the shared helper module, the regularized upper incomplete gamma function $Q(\mathrm{df}/2, X^2/2)$.

## Example

**A suspect die.** Sixty rolls give the counts $5, 8, 9, 8, 10, 20$ for faces 1 to 6. Each expected count is 10.

| face | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $O_i$ | 5 | 8 | 9 | 8 | 10 | 20 |
| $(O_i - E_i)^2/E_i$ | 2.5 | 0.4 | 0.1 | 0.4 | 0 | 10 |

$X^2 = 13.4$ on 5 degrees of freedom, and $p = P(\chi^2_5 > 13.4) = 0.0199$. The upper 5% point is $11.0705$, so the test rejects at $\alpha = 0.05$. Most of the statistic comes from face 6.

**Mendel's peas.** Mendel's dihybrid cross gave 315 round yellow, 108 round green, 101 wrinkled yellow and 32 wrinkled green seeds, 556 in all. The theory predicts the ratio 9 : 3 : 3 : 1, so the expected counts are $312.75, 104.25, 104.25, 34.75$. Then $X^2 = 0.4700$ on 3 degrees of freedom and $p = 0.9254$. The likelihood-ratio statistic gives $G = 0.4754$ and $p = 0.9243$. The data agree with the theory.

**A fitted parameter.** A sample of 1000 people has genotype counts $AA = 298$, $Aa = 489$, $aa = 213$. Under Hardy-Weinberg equilibrium the genotype probabilities are $\theta^2$, $2\theta(1 - \theta)$ and $(1 - \theta)^2$ for an unknown allele frequency $\theta$. The maximum likelihood estimate from these counts is $\hat\theta = (2 \cdot 298 + 489)/2000 = 0.5425$, so the expected counts are $294.31, 496.39, 209.31$. Then $X^2 = 0.2215$. One parameter was fitted, so there are $3 - 1 - 1 = 1$ degree of freedom, and $p = 0.638$. With the wrong count of 2 degrees of freedom the p-value would be $0.895$.

The tests check these numbers. They also check $X^2$ against exact rational arithmetic for 300 random tables.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Write the counts as a sum of $n$ iid unit vectors. The scaled vector $Y$ with entries $(O_i - E_i)/\sqrt{E_i}$ has covariance $I - uu^\top$ with $u = (\sqrt{p^0_i})_i$, a unit vector. So by the multivariate [central limit theorem](/central-limit-theorem/), $Y$ tends to a normal vector whose covariance is the projection onto the $k - 1$ dimensional subspace orthogonal to $u$. Then $X^2 = \lVert Y \rVert^2$ tends to a sum of $k - 1$ squared independent standard normals, which is $\chi^2_{k - 1}$. For $k = 2$ the statistic is exactly $z^2$, the square of the score statistic of the [binomial test](/binomial-test/). A third-order Taylor bound shows $G - X^2 \to 0$ in probability, so $G$ has the same limit, as [Wilks's theorem](/wilks-theorem/) also predicts.

## Complexity

The statistic takes $\Theta(k)$ arithmetic operations, and the expected counts take $\Theta(k)$ extra space (the code builds a list of them; a streaming version needs $\Theta(1)$). The p-value is one evaluation of the incomplete gamma function. Counting the observations into categories, if the caller has raw data, is a separate $\Theta(n)$ pass.

## Properties

- **Size for small samples (computed exactly).** Under the null the outcome is a finite multinomial, so the true size of the test at $\alpha = 0.05$ can be found by summing over all outcomes. The tests do this and also check it against a simulation.

  | $n$ | $p^0$ | smallest $E_i$ | size of $X^2$ test | size of $G$ test |
  |---|---|---|---|---|
  | 10 | $(1/3, 1/3, 1/3)$ | 3.33 | 0.0590 | 0.0565 |
  | 30 | $(1/3, 1/3, 1/3)$ | 10 | 0.0478 | 0.0597 |
  | 20 | $(1/4, 1/4, 1/4, 1/4)$ | 5 | 0.0415 | 0.0528 |
  | 20 | $(0.7, 0.1, 0.1, 0.1)$ | 2 | 0.0491 | 0.0624 |
  | 50 | $(0.7, 0.1, 0.1, 0.1)$ | 5 | 0.0513 | 0.0566 |

  The Pearson statistic stays close to 0.05 even with expected counts of 2. The $G$ statistic is more liberal in these cases.
- **Fitted parameters lower the degrees of freedom.** Each parameter fitted by maximum likelihood from the grouped counts removes one degree of freedom.
- **Estimates from raw data.** The Chernoff-Lehmann limit lies between the two chi-square laws. In a simulation (seed 5, 4000 samples of $n = 100$ standard normal values, six fixed bins, mean and standard deviation estimated from the raw values), the test with $6 - 1 - 2 = 3$ degrees of freedom rejected 5.5% of the time, and the test with 5 degrees of freedom rejected 1.1% of the time. The theory says the first is slightly liberal, and the simulation agrees within its standard error of 0.35%. The second is very conservative.
- **Power.** For the die with $n = 60$ and a loaded face 6 ($p_6 = 1/3$, the others $2/15$), the power at $\alpha = 0.05$ was 0.698 for $X^2$ and 0.663 for $G$ in a simulation (seed 9, 20000 samples). The noncentral chi-square approximation with $\lambda = 12$ gives 0.769, which is too high at this sample size.
- **Invariant to the order of the categories.** The statistic ignores any order. This is a weakness when the categories are ordered.

## Variants and improvements

- **Likelihood-ratio statistic $G$.** The code computes it with `statistic="g"`. It has the same limit, and it adds up over nested models, which $X^2$ does not do exactly.
- **Power-divergence family.** Cressie and Read (1984) put $X^2$ and $G$ in one family indexed by $\lambda$, with $X^2$ at $\lambda = 1$ and $G$ at $\lambda = 0$. They recommend $\lambda = 2/3$.
- **Exact multinomial test.** For small $n$, sum the multinomial probabilities of all outcomes at least as unlikely as the observed one, or as large in $X^2$, by enumeration as in the tests. For $k = 2$ this is the [binomial test](/binomial-test/).
- **Monte Carlo p-value.** Simulate multinomial samples under $p^0$ and use $(1 + \text{count})/(1 + B)$, where the count is the number of simulated $X^2$ values at least the observed one.
- **Continuous data.** For a fully specified continuous distribution, tests based on the empirical distribution function, such as the [Kolmogorov-Smirnov](/kolmogorov-smirnov-test/) and [Anderson-Darling](/anderson-darling-test/) tests, do not need bins and usually have more power.

## When to use it

Use it for counts in categories that have no order, with a null hypothesis that gives the category probabilities or a model with a few parameters. Typical uses are genetic ratios, checks of a random number generator, and checks of a discrete model. A common rule asks for all expected counts of at least 5. The table above shows that the Pearson test holds its size well with expected counts near 2, so Cochran's rule (no expected count below 1, and at most 20% below 5) is a better guide. For smaller counts, use the exact or Monte Carlo test.

## Pitfalls

- **Percentages instead of counts.** The statistic must use counts. Using percentages changes $n$ to 100 and gives a wrong p-value.
- **Observations that are not independent.** Repeated measurements on the same people, or clustered data, make the variance larger than the multinomial variance, and the test rejects too often.
- **Wrong degrees of freedom.** Subtract one degree of freedom for each parameter fitted from the counts. If the parameters came from the raw data, $k - 1 - s$ degrees of freedom make the test slightly liberal and $k - 1$ make it conservative.
- **Choosing bins after seeing the data.** Choosing bins to make the fit look good or bad changes the null law.
- **Reading a large p-value as proof of the model.** A large p-value means only that the test did not detect a misfit. With small $n$ the power is low. A p-value very close to 1 can also be a warning: Fisher (1936) argued that the totals of Mendel's experiments agreed with theory too well.

## Implementations

## History

Karl Pearson published the statistic in 1900 as a criterion for deciding whether a set of deviations could come from random sampling, and gave its chi-square reference law with $k - 1$ degrees of freedom. For tables with estimated margins and for fitted parameters, Pearson kept $k - 1$. Fisher showed in 1922 and 1924 that each parameter fitted efficiently from the counts removes one degree of freedom. This was a long argument with Pearson. Cramér's 1946 book gave a complete proof of the limit. Chernoff and Lehmann (1954) showed that estimates from the ungrouped data give a limit that is not chi-square. Cochran (1952, 1954) studied small expected counts and gave the rules that are still in use. Cressie and Read (1984) put the Pearson and likelihood-ratio statistics into one family.

## References
