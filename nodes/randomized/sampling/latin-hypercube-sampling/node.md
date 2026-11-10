---
tag: RGZS45
kind: technique
slug: latin-hypercube-sampling
name: Latin hypercube sampling
aliases:
- LHS
- Latin hypercube design
- Latin hypercube
area: randomized/sampling
level: intro
summary: Sample so that each variable's range is split into equal strata with exactly one point per stratum.
prereqs: [stratified-sampling, random-permutation, monte-carlo-integration]
see_also: [stratified-sampling, monte-carlo-integration, fisher-yates-shuffle, inverse-transform-sampling, sobol-sequence, halton-sequence, importance-sampling, random-permutation]
sources:
  - paper: doi:10.1080/00401706.1979.10489755
    title: Michael D. McKay, Richard J. Beckman and William J. Conover, A comparison of three methods for selecting values of input variables in the analysis of output from a computer code, Technometrics 21(2), 239 to 245, 1979
    locator: the definition of Latin hypercube sampling, the unbiasedness of the estimate, and the theorem that the variance is not larger than for random sampling when the output is monotone in each input
  - paper: doi:10.1080/00401706.1987.10488205
    title: Michael Stein, Large sample properties of simulations using Latin hypercube sampling, Technometrics 29(2), 143 to 151, 1987
    locator: the asymptotic variance of the Latin hypercube estimate, which removes the variance of the additive main effects, and a method for dependent input variables
  - book: isbn:9780387004518
    title: Paul Glasserman, Monte Carlo Methods in Financial Engineering, Springer, 2003
    locator: Chapter 4 (Variance Reduction Techniques), the section on Latin hypercube sampling
---

Latin hypercube sampling (LHS) chooses $n$ random points in the unit cube $[0, 1)^d$ so that, for each coordinate on its own, the $n$ intervals $[k/n, (k+1)/n)$ each hold exactly one point. It is [stratified sampling](/stratified-sampling/) of every coordinate at once with only $n$ points, where a full grid of strata would need $n^d$. McKay, Beckman and Conover introduced it in 1979 to choose the inputs of expensive computer codes. Each point is still uniform on the cube, so the estimate of a mean is unbiased, and Stein (1987) showed that the variance of the additive part of the function is removed as $n$ grows. The name comes from the Latin square, where each symbol appears once in each row and each column.

## In plain words

You want the average output of a slow computer model with several inputs, and you can afford only $n$ runs. With plain random inputs, some ranges of an input may get many runs and others none.

Latin hypercube sampling cuts the range of every input into $n$ equal slices and makes sure that each slice of each input is used by exactly one run. Picture rooks on a chessboard: no two share a row or a column. The runs then cover the whole range of every single input evenly.

This helps most when the output depends on each input mostly on its own. It does not help with effects that come only from inputs acting together.

## When it applies

- The goal is a mean $\mu = E[f(X)]$ over $d$ independent inputs, or an integral over the unit cube, and each evaluation of $f$ is expensive.
- The inputs are independent, or can be made independent, so that each one is a transformed uniform variable. An input with distribution function $F_j$ is set to $F_j^{-1}(x_j)$, as in [inverse transform sampling](/inverse-transform-sampling/).
- The number of runs $n$ is fixed in advance.
- The function is close to additive, or monotone in each input. Then the gain over independent points is large.

## The template

```pseudo id=main
LATIN-HYPERCUBE(n, d, rng)
L1  for j ← 1 to d do
L2      π_j ← a uniform random permutation of 0, ..., n − 1, drawn with rng   ▷ Fisher-Yates
L3      for i ← 1 to n do
L4          U ← a uniform number in [0, 1) from rng                         ▷ U = 1/2 gives midpoint LHS
L5          X[i][j] ← (π_j(i) + U) / n
L6  return X
LHS-ESTIMATE(f, n, d, rng)
L7  X ← LATIN-HYPERCUBE(n, d, rng)
L8  return (1/n) · (f(X[1]) + ... + f(X[n]))
```

The permutations of line L2 come from the [Fisher-Yates shuffle](/fisher-yates-shuffle/), so one design takes $O(nd)$ time and $nd$ uniform numbers plus the shuffles.

**Theorem (the design).** In each coordinate $j$, each interval $[k/n, (k+1)/n)$ holds exactly one of the $n$ points. Each single point $X_i$ is uniform on $[0, 1)^d$, so $E[\hat\mu] = \mu$ for the estimate $\hat\mu$ of line L8.

*Proof.* $X_{ij}$ lies in the interval with index $\pi_j(i)$, and $\pi_j$ is a permutation, so each index is used once. For a fixed $i$, $\pi_j(i)$ is uniform on $\{0, \ldots, n-1\}$, and with the independent $U$ the value $X_{ij}$ is uniform on $[0, 1)$. The coordinates use independent permutations and independent $U$, so $X_i$ is uniform on the cube. Linearity of expectation gives $E[\hat\mu] = \mu$. $\blacksquare$

**The variance.** The points are exchangeable but not independent. With $\sigma^2 = \operatorname{Var}[f(X)]$ for one uniform $X$,
$$\operatorname{Var}[\hat\mu] = \frac{\sigma^2}{n} + \frac{n - 1}{n}\operatorname{Cov}\big[f(X_1), f(X_2)\big],$$
since the $n$ variances are equal and the $n(n-1)$ covariances are equal. LHS helps exactly when two points of the design give negatively correlated outputs.

**Additive functions.** Let $f(x) = \mu + \sum_j f_j(x_j)$. Then $\hat\mu - \mu = \sum_j \frac1n \sum_i f_j(X_{ij})$, and the inner sum depends only on column $j$, which is a stratified sample of $[0, 1)$ with one uniform point in each of the $n$ intervals. The columns are independent, so
$$\operatorname{Var}[\hat\mu] = \sum_j \frac{1}{n^2}\sum_{k=0}^{n-1} \operatorname{Var}\big[f_j(U) \mid U \in [k/n, (k+1)/n)\big].$$
For $f_j(x) = x$ each term is $1/(12n^2)$, so each coordinate adds $1/(12n^3)$, against $1/(12n)$ for $n$ independent points. For smooth $f_j$ the order is the same, $O(n^{-3})$.

**Theorem (Stein 1987).** Write $f = \mu + \sum_j f_j(x_j) + r(x)$, where $f_j(x_j) = E[f(X) \mid X_j = x_j] - \mu$ are the main effects and $r$ is the rest. If $E[f(X)^2] < \infty$, then
$$\operatorname{Var}[\hat\mu] = \frac{\sigma^2}{n} - \frac{1}{n}\sum_j \operatorname{Var}[f_j(X_j)] + o\Big(\frac1n\Big) = \frac{\operatorname{Var}[r(X)]}{n} + o\Big(\frac1n\Big).$$
So for large $n$ LHS removes the variance of the main effects and keeps the variance of the interactions.

**Theorem (McKay, Beckman and Conover 1979).** If $f$ is monotone in each of its arguments, then $\operatorname{Var}[\hat\mu] \le \sigma^2/n$, the variance with $n$ independent points.

**No large loss.** Owen (1997) showed that $\operatorname{Var}[\hat\mu] \le \sigma^2/(n - 1)$ for every square integrable $f$, so LHS with $n$ points is never worse than independent sampling with $n - 1$ points.

**Example, measured.** For $n = 5$ and $d = 2$, one design from `random.Random(1)` has the points $(0.499, 0.539)$, $(0.690, 0.853)$, $(0.930, 0.360)$, $(0.158, 0.718)$, $(0.219, 0.020)$, in the cells $(2, 2), (3, 4), (4, 1), (0, 3), (1, 0)$: each row index and each column index appears once. The variance of $\hat\mu$, measured over seeded runs (`random.Random(2025)`), compared with independent points:

| $f$ | $n$ | independent points | LHS | prediction for LHS |
| --- | --- | --- | --- | --- |
| $x_1 + x_2 + x_3$ | 10 | $2.47 \times 10^{-2}$ | $2.52 \times 10^{-4}$ | $3/(12n^3) = 2.50 \times 10^{-4}$ |
| $x_1 x_2$ | 10 | $4.92 \times 10^{-3}$ | $8.16 \times 10^{-4}$ | Stein: $6.94 \times 10^{-4}$ |
| $x_1 x_2$ | 100 | $4.92 \times 10^{-4}$ | $7.08 \times 10^{-5}$ | Stein: $6.94 \times 10^{-5}$ |

For $f = x_1 x_2$, $\sigma^2 = 7/144$, of which $6/144$ are main effects and $1/144$ is the interaction $(x_1 - \frac12)(x_2 - \frac12)$. LHS removes the main effects, so its variance tends to $1/(144 n)$, one seventh of the variance with independent points. The runs used 20000 designs for $n = 10$ and 4000 for $n = 100$.

## Classic examples

- **Computer experiments.** McKay, Beckman and Conover compared LHS with random and stratified inputs for a computer code of a reactor safety model. LHS became the standard way to choose runs of slow simulation codes.
- **Uncertainty and risk analysis.** Inputs with known distributions are pushed through a model to get the distribution of the output, with each input set by its inverse distribution function.
- **Designs for surrogate models.** The first runs for fitting a Gaussian process or another surrogate model, and the first points of a hyperparameter search, are often a Latin hypercube design, usually with an extra spread criterion.
- **Monte Carlo pricing.** In finance, LHS stratifies the normal increments of each time step of a path, which works well when the price depends mostly on each increment separately.

## Variations

- **Midpoint LHS.** Put each point at the center of its interval, $U = 1/2$ in line L4. The design is no longer unbiased for every $f$, but its points are more even.
- **Maximin LHS.** Among many random designs, or by local search, choose one whose least distance between two points is largest, so the points do not clump in two or more dimensions.
- **Orthogonal array based LHS.** Tang (1993) and Owen (1992) built designs that are Latin in each coordinate and also balanced in each pair of coordinates, which removes part of the variance of the two-way interactions.
- **Correlation control.** Iman and Conover (1982) reorder the columns so that the sample rank correlations match a target, either zero for independent inputs or given values for dependent ones. Stein (1987) gave a related method for dependent inputs.
- **Replicated LHS.** Draw $r$ independent designs of size $n$ and use the spread of the $r$ estimates to estimate the variance.
- **Quasi-Monte Carlo.** Low-discrepancy points such as the [Sobol sequence](/sobol-sequence/) and the [Halton sequence](/halton-sequence/), and their randomized forms, balance all low-dimensional projections at once and can give smaller errors for smooth functions.

## Pitfalls

- **Interactions are not reduced.** LHS keeps the variance of the parts of $f$ that come from several inputs together. For $f = x_1 x_2$ it removes six sevenths of the variance and no more.
- **It can be worse than independent points.** For $n = 2$, $d = 2$, and $f$ the indicator of the two diagonal quarters $[0, \frac12)^2$ and $[\frac12, 1)^2$, the two points are both on the diagonal or both off it, so $\hat\mu$ is 0 or 1 with probability $1/2$ each: variance $1/4$, against $1/8$ for two independent points. This meets Owen's bound $\sigma^2/(n-1)$ exactly.
- **The naive error bar is wrong.** The points of one design are not independent, so $s^2/n$ from one design does not estimate the variance. Use replicated designs.
- **Bad projections.** A random Latin design can be poor in two dimensions, for example close to a diagonal when two permutations happen to agree. Check the design or use a maximin or orthogonal array variant when this matters.
- **Points cannot be added.** Adding one point to a Latin design of size $n$ breaks the property. If the budget can grow, use nested designs or a sequence with good projections.
- **Dependent inputs.** Transforming each coordinate by its own inverse distribution function gives independent inputs. For dependent inputs, transform after a correlation step, as in the Iman and Conover method, or use a conditional transform.

## References
