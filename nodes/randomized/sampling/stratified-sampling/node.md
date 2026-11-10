---
tag: TAW83D
kind: technique
slug: stratified-sampling
name: Stratified sampling
aliases:
- stratification
- stratified random sampling
- Neyman allocation
area: randomized/sampling
level: intro
summary: Partition the population into strata and sample within each to reduce variance.
prereqs: [uniform-random-subset, variance, linearity-of-expectation]
see_also: [uniform-random-subset, latin-hypercube-sampling, systematic-sampling, importance-sampling, monte-carlo-integration, probability-proportional-to-size-sampling, cross-validation, random-sampling]
sources:
  - book: isbn:9780471162407
    title: William G. Cochran, Sampling Techniques, third edition, Wiley, 1977
    locator: Chapter 2 (the variance of the mean in simple random sampling) and Chapter 5 (Stratified Random Sampling, the estimate and its variance, proportional allocation, optimum and Neyman allocation, and the comparison with simple random sampling)
  - book: isbn:9780387004518
    title: Paul Glasserman, Monte Carlo Methods in Financial Engineering, Springer, 2003
    locator: Chapter 4 (Variance Reduction Techniques), the section on stratified sampling (proportional and optimal allocation for Monte Carlo estimates)
---

Stratified sampling splits a population into disjoint groups, the *strata*, draws a separate random sample in each group, and combines the group means with the group sizes as weights. When the strata are more alike inside than the population as a whole, the estimate has a smaller variance than a simple random sample of the same size, because the part of the variance that comes from differences between the strata is removed. The technique is old and general: it is the standard design of survey sampling, where Neyman (1934) found the best way to split the sample among the strata, and the same idea reduces the variance of Monte Carlo integration.

## In plain words

Suppose you want the average income of a country from 1000 interviews. Cities and villages differ a lot. A plain random sample may by chance get too many city people, and the estimate moves around.

Instead, split the country into cities and villages first, and interview a fixed number of people in each part. Combine the two averages with the true share of each part. The chance mix-up between the parts is gone, so the estimate moves around less.

You can do even better. Put more interviews where incomes vary most, because a part where everyone earns the same needs only a few.

## When it applies

- The population or the domain can be split into strata whose sizes or weights $W_h$ are known exactly, and one can sample inside each stratum.
- The quantity of interest, $y$, varies less within strata than overall, so the strata are built from a variable that is related to $y$, such as region for income or a subinterval of the domain for an integral.
- The goal is a mean or a total, or an integral, which is a mean over the domain.

## The template

The population has $N$ units with values $y_i$, split into strata $U_1, \ldots, U_H$ of sizes $N_h$ with weights $W_h = N_h/N$. Write $\bar Y_h$ for the mean of stratum $h$ and $S_h^2 = \frac{1}{N_h - 1}\sum_{i \in U_h}(y_i - \bar Y_h)^2$ for its variance, and $\bar Y$ and $S^2$ for the whole population.

```pseudo id=main
STRATIFIED-MEAN(U_1, ..., U_H, n, rng)
L1  N ← N_1 + ... + N_H, and W_h ← N_h / N for each h
L2  choose sizes n_1, ..., n_H with n_1 + ... + n_H = n and 1 ≤ n_h ≤ N_h   ▷ proportional, Neyman, or given
L3  for h ← 1 to H do
L4      A_h ← a uniform random n_h-subset of U_h, drawn with rng        ▷ independent across strata
L5      ȳ_h ← mean of y over A_h, and s_h² ← sample variance of y over A_h
L6  ȳ_st ← W_1 ȳ_1 + ... + W_H ȳ_H
L7  v ← Σ_h W_h² (1 − n_h / N_h) s_h² / n_h                              ▷ needs n_h ≥ 2
L8  return ȳ_st and v
```

Line L4 is the [uniform random subset](/uniform-random-subset/) problem, which is simple random sampling (SRS) without replacement inside the stratum.

**Lemma (SRS).** A simple random sample of size $n$ from $N$ units has mean $\bar y$ with $E[\bar y] = \bar Y$ and $\operatorname{Var}[\bar y] = (1 - n/N)\, S^2 / n$.

*Proof.* Let $Z_i$ be the indicator that unit $i$ is in the sample, so $\bar y = \frac{1}{n}\sum_i y_i Z_i$ and $E[Z_i] = n/N$, which gives $E[\bar y] = \bar Y$. Shifting all $y_i$ by a constant does not change the variance, so let $\bar Y = 0$. Write $p = n/N$. Then $\operatorname{Var}[Z_i] = p(1 - p)$, and for $i \ne j$, $\Pr[Z_i = Z_j = 1] = \frac{n(n-1)}{N(N-1)}$, so $\operatorname{Cov}[Z_i, Z_j] = -p(1-p)/(N - 1)$. Since $\sum_i y_i = 0$, $\sum_{i \ne j} y_i y_j = -\sum_i y_i^2$. So
$$\operatorname{Var}\Big[\sum_i y_i Z_i\Big] = p(1 - p)\Big(\sum_i y_i^2 + \frac{1}{N - 1}\sum_i y_i^2\Big) = p(1-p)\frac{N}{N - 1}\sum_i y_i^2 = n(1 - p) S^2,$$
and dividing by $n^2$ gives the claim. $\blacksquare$

**Theorem (the stratified estimate).** $E[\bar y_{st}] = \bar Y$, and
$$\operatorname{Var}[\bar y_{st}] = \sum_{h=1}^H W_h^2 \Big(1 - \frac{n_h}{N_h}\Big) \frac{S_h^2}{n_h}.$$
*Proof.* By the lemma, $E[\bar y_h] = \bar Y_h$, so by [linearity of expectation](/linearity-of-expectation/) $E[\bar y_{st}] = \sum_h W_h \bar Y_h = \bar Y$. The samples of different strata are independent, so the variance is the sum of $W_h^2 \operatorname{Var}[\bar y_h]$, and the lemma gives each term. $\blacksquare$

Since $s_h^2$ is an unbiased estimate of $S_h^2$ under SRS, the value $v$ of line L7 is an unbiased estimate of this variance.

**Theorem (proportional allocation).** Let $n_h = n W_h$, so every unit has inclusion probability $f = n/N$. Then
$$\operatorname{Var}_{\text{prop}} = \frac{1 - f}{n}\sum_h W_h S_h^2, \qquad \operatorname{Var}_{\text{SRS}} - \operatorname{Var}_{\text{prop}} = \frac{1 - f}{n(N - 1)}\Big[\sum_h N_h(\bar Y_h - \bar Y)^2 - \frac{1}{N}\sum_h (N - N_h) S_h^2\Big].$$
*Proof.* The first formula is the theorem above with $n_h / N_h = f$ and $W_h^2/n_h = W_h/n$. For the second, split the total sum of squares into within and between parts:
$$(N - 1) S^2 = \sum_h (N_h - 1) S_h^2 + \sum_h N_h (\bar Y_h - \bar Y)^2.$$
Divide by $N - 1$ and subtract $\sum_h W_h S_h^2$. The coefficient of $S_h^2$ is $\frac{N_h - 1}{N - 1} - \frac{N_h}{N} = -\frac{N - N_h}{N(N-1)}$. Multiplying by $(1 - f)/n$ gives the identity. $\blacksquare$

The first sum in the bracket grows with $N$, while the second is at most $\sum_h S_h^2$. So proportional allocation has variance at most that of SRS unless the stratum means are almost equal, and the gain is the between-strata part of the variance. When units are drawn with replacement, or $N$ is large, the second sum disappears and the statement is exact: by the law of total variance, $\sigma^2 = \sum_h W_h \sigma_h^2 + \sum_h W_h(\mu_h - \mu)^2$, so $\operatorname{Var}_{\text{prop}} = \frac1n\sum_h W_h\sigma_h^2 \le \frac1n\sigma^2 = \operatorname{Var}_{\text{SRS}}$. This comparison is in Cochran, Chapter 5.

**Theorem (Neyman allocation).** For a fixed total $n$, the variance is least when
$$n_h = n\,\frac{N_h S_h}{\sum_k N_k S_k},$$
if these values are at most $N_h$, and then $\operatorname{Var}_{\text{Ney}} = \frac{1}{n}\big(\sum_h W_h S_h\big)^2 - \frac{1}{N}\sum_h W_h S_h^2$. Moreover $\operatorname{Var}_{\text{prop}} - \operatorname{Var}_{\text{Ney}} = \frac1n \sum_h W_h (S_h - \bar S)^2 \ge 0$ with $\bar S = \sum_h W_h S_h$.

*Proof.* In the variance formula, $\sum_h W_h^2 S_h^2 / N_h = \frac1N\sum_h W_h S_h^2$ does not depend on the $n_h$. So we minimize $\sum_h a_h^2 / n_h$ with $a_h = W_h S_h$, subject to $\sum_h n_h = n$. By the Cauchy-Schwarz inequality,
$$\Big(\sum_h n_h\Big)\Big(\sum_h \frac{a_h^2}{n_h}\Big) \ge \Big(\sum_h a_h\Big)^2,$$
with equality exactly when $n_h$ is proportional to $a_h$. So the minimum is $(\sum_h W_h S_h)^2/n$, at $n_h \propto W_h S_h \propto N_h S_h$. For the comparison, $\sum_h W_h S_h^2 - \bar S^2 = \sum_h W_h (S_h - \bar S)^2$, the variance of $S_h$ under the weights $W_h$, and the terms in $1/N$ cancel. $\blacksquare$

If sampling in stratum $h$ costs $c_h$ per unit and the budget is fixed, the same argument gives $n_h \propto N_h S_h / \sqrt{c_h}$.

**Example, measured.** A population of $N = 1000$ values drawn once with `random.Random(42)` has three strata: 600 values with mean $10.08$ and $S_h = 2.01$, 300 with mean $19.48$ and $S_h = 5.09$, and 100 with mean $47.56$ and $S_h = 22.06$. For $n = 50$:

| design | sizes $n_h$ | variance by the formulas | variance in 20000 seeded runs |
| --- | --- | --- | --- |
| SRS | 50 in total | 3.464 | 3.442 |
| proportional | 30, 15, 5 | 1.118 | 1.129 |
| Neyman | 12, 16, 22 | 0.429 | 0.427 |

Neyman allocation puts 22 of the 50 units in the smallest stratum, because its values vary the most. The variance falls by a factor of 8 against SRS. All three estimates were unbiased in the runs, with means $16.65$ against the true mean $16.65$.

## Classic examples

- **Survey sampling.** Strata by region, age group or company size, with sample sizes by proportional or Neyman allocation. This is the setting of Neyman (1934) and of Cochran's book.
- **Monte Carlo integration in one dimension.** To estimate $\int_0^1 f$, split $[0, 1]$ into $n$ equal intervals and take one uniform point in each, with weight $1/n$. For $f(x) = x$ each point has variance $1/(12n^2)$, so the estimate has variance $1/(12n^3)$, against $1/(12n)$ for $n$ independent points: $1/12000$ against $1/120$ for $n = 10$. For a smooth $f$ the variance is $O(n^{-3})$. See [Monte Carlo integration](/monte-carlo-integration/).
- **Jittered sampling in rendering.** A pixel is split into a grid of cells with one random point in each, which removes the clumps of independent points and lowers the noise.
- **Stratified splits in machine learning.** Training and test sets, or the folds of [cross-validation](/cross-validation/), keep the class proportions of the data, which is proportional allocation with classes as strata.
- **Latin hypercube sampling.** In many dimensions a full grid has too many cells, and [Latin hypercube sampling](/latin-hypercube-sampling/) stratifies each coordinate separately.

## Variations

- **Optimal allocation with costs.** $n_h \propto N_h S_h/\sqrt{c_h}$, as above.
- **Post-stratification.** Take an SRS first and form the strata afterward, from a variable observed on the sample. The weights $W_h$ must still be the known population shares. For large samples the variance is close to that of proportional allocation.
- **Stratified importance sampling.** Use [importance sampling](/importance-sampling/) within strata, or choose the strata so that each has equal probability under the proposal.
- **Strata with one unit sampled.** Many strata with $n_h = 1$ give the most variance reduction, but line L7 cannot be computed. Use two units per stratum, collapse pairs of strata, or repeat the whole design independently.
- **Unequal probabilities inside strata.** Each stratum can use its own design, such as [systematic sampling](/systematic-sampling/) or [probability proportional to size sampling](/probability-proportional-to-size-sampling/), with the same weighted combination of the stratum estimates.

## Pitfalls

- **Wrong weights.** The weights must be the true stratum shares $W_h$, not the shares in the sample. With Neyman allocation the sample shares are far from $W_h$, and the plain sample mean is biased: in the example above it would give the smallest stratum weight $22/50$ instead of $0.1$.
- **Neyman sizes above the stratum size.** If the formula gives $n_h > N_h$, take the whole stratum and split the rest of the sample among the other strata by the same rule.
- **Unknown $S_h$.** Neyman allocation needs the stratum standard deviations, which are not known. Use estimates from a pilot sample or past data. Errors in them cost little, since the variance is flat near the optimum, but very wrong guesses can be worse than proportional allocation.
- **Proportional allocation is not always better.** With almost equal stratum means and a small population, it can be slightly worse than SRS, as the identity above shows. For the population $\{0, 1, 2, 0, 1, 2\}$ in two strata $\{0, 1, 2\}$ and $\{0, 1, 2\}$ with $n = 2$, the variance is $1/3$ with one unit per stratum and $4/15$ with SRS.
- **Rounding.** The $n_h$ must be integers that add up to $n$. Round by the largest remainders, and check that each $n_h \ge 1$, or $n_h \ge 2$ when a variance estimate is needed.
- **One variable at a time.** An allocation that is best for one variable can be poor for another. Surveys with many variables often use proportional allocation as a safe choice.

## References
