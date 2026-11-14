---
tag: DRZ1M4
kind: algorithm
slug: friedman-test
name: Friedman test
aliases:
- Friedman rank test
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: A rank test for k treatments in a randomized block design. It ranks within each block and compares the treatment rank sums.
model: real-ram
complexity:
  vars: {b: the number of blocks, k: the number of treatments}
  time: {worst: Θ(b k log k), best: Θ(b k log k)}
  space: {extra: Θ(b k)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1937
  people: [Milton Friedman]
  note: Friedman replaced the observations in each row of a two-way table by their ranks and gave the chi-square approximation for the spread of the rank sums.
prereqs: [kruskal-wallis-test, sign-test, statistical-hypothesis-test]
see_also: [randomized-block-design, two-way-anova, wilcoxon-signed-rank-test, permutation-test, multiple-comparisons-problem, spearman-rank-correlation, latin-square-design, balanced-incomplete-block-design]
sources:
  - book: isbn:9780470387375
    title: Myles Hollander, Douglas A. Wolfe and Eric Chicken, Nonparametric Statistical Methods, third edition, Wiley, 2014
    locator: Chapter 7 (the two-way layout), the section on the Friedman test for general alternatives
  - book: isbn:9780387352121
    title: E. L. Lehmann, Nonparametrics, Statistical Methods Based on Ranks, revised edition, Springer, 2006
    locator: The chapter on blocked comparisons of several treatments (the Friedman test and its ties)
  - paper: doi:10.1080/01621459.1937.10503522
    title: Milton Friedman, The use of ranks to avoid the assumption of normality implicit in the analysis of variance, Journal of the American Statistical Association 32(200), 1937
    locator: pp. 675 to 701 (the rank statistic for a two-way table and its chi-square approximation)
---

The Friedman test compares $k$ treatments in a [randomized block design](/randomized-block-design/): each of $b$ blocks (subjects, judges, fields, data sets) gives one response to every treatment. It ranks the $k$ responses within each block, adds the ranks of each treatment over the blocks, and measures how far these rank sums are from their common null mean $b(k+1)/2$. Ranking within blocks removes the block effects completely, so large differences between blocks cost nothing. Under the null hypothesis that the treatments do not matter, the ranks in each block are a random permutation, and the statistic is approximately chi-square with $k - 1$ degrees of freedom. For $k = 2$ the test is the [sign test](/sign-test/).

## In plain words

Eight judges taste three wines and give each one a score. Some judges give high scores to everything, others are harsh. So, for each judge, replace the scores by places: 1 for the wine that judge liked least, 3 for the one liked most. Then add up the places of each wine over all judges.

If the wines are equally good, every order of places is equally likely for every judge, and the three totals should be close to each other. If one wine gets the top place from almost every judge, its total is far above the others. The test measures how far apart the totals are, and asks how often random orders for each judge would spread them this far.

## The problem

**Model.** The responses are $X_{ij}$ for block $i = 1, \ldots, b$ and treatment $j = 1, \ldots, k$, with $k \ge 2$. The blocks are independent. A common model is $X_{ij} = \mu + \beta_i + \tau_j + E_{ij}$, with any block effects $\beta_i$ and errors that are exchangeable within each block.

**Hypotheses.** $H_0$: within each block, the vector $(X_{i1}, \ldots, X_{ik})$ is exchangeable, that is, its law does not change when the treatments are permuted. In the additive model this is $\tau_1 = \cdots = \tau_k$. The alternative is that some treatments tend to give larger responses than others.

**Statistic.** Let $r_{ij}$ be the midrank of $X_{ij}$ among $X_{i1}, \ldots, X_{ik}$, and $R_j = \sum_i r_{ij}$. The tie-corrected statistic is
$$Q = \frac{(k-1) \sum_{j=1}^{k} \left(R_j - \frac{b(k+1)}{2}\right)^2}{\sum_{i,j} r_{ij}^2 - \frac{b k (k+1)^2}{4}},$$
which without ties equals $\frac{12}{bk(k+1)} \sum_j R_j^2 - 3b(k+1)$.

**Null distribution.** Under $H_0$, given the multiset of values in each block, the assignment of each block's values to the treatments is uniform over its $k!$ permutations, independently across blocks. This conditional law of $Q$ is exact and gives the same probability $(k!)^{-b}$ to each of the $(k!)^b$ outcomes. As $b \to \infty$ with $k$ fixed, $Q$ converges in law to chi-square with $k - 1$ degrees of freedom (asymptotic).

**P-values.** Large $Q$ is evidence against $H_0$, so the p-value is one upper tail: $P(\chi^2_{k-1} \ge Q)$ for the asymptotic test, or the share of the $(k!)^b$ outcomes with $Q$ at least the observed value for the exact test. For $k = 2$ the upper tail of $Q$ is the two-sided sign test.

**Rejection rule and size.** Reject at level $\alpha$ when $p \le \alpha$. The exact p-value gives size at most $\alpha$. The chi-square p-value can be liberal or conservative for small $b$: for $k = 3$, the exact probability $P(Q \ge 5.991)$ is $0.0694$ for $b = 4$, $0.0521$ for $b = 6$ and $0.0278$ for $b = 3$.

**Sensitivity and power.** The test detects treatment effects that are consistent across blocks. It uses only the order within each block, so it ignores how large the differences are, and for $k = 2$ it has the low efficiency of the sign test: $2/\pi$ against the paired t-test for normal errors. Its efficiency against two-way ANOVA grows with $k$: for normal errors it is $(3/\pi) \cdot k/(k+1)$, which is $2/\pi$ at $k = 2$ and $0.716$ at $k = 3$. A Monte Carlo run with $b = 10$, $k = 3$, block effects with standard deviation 3, unit normal errors, a shift of 1 for one treatment, $r = 2000$ samples and seed 53 gave power $0.442$ at $\alpha = 0.05$, against $0.005$ for the [Kruskal-Wallis test](/kruskal-wallis-test/) that ignores the blocks.

## The algorithm

```pseudo id=main
FRIEDMAN(blocks X_1, ..., X_b, each of length k, method)
L1  r_i ← midranks of the k values of block i, for i = 1, ..., b
L2  R_j ← r_1j + ... + r_bj, for j = 1, ..., k
L3  A ← Σ_ij r_ij^2; D ← A - b k (k + 1)^2 / 4
L4  Q ← (k - 1) · Σ_j (R_j - b(k + 1)/2)^2 / D   (Q ← 0 if D = 0)
L5  if method = asymptotic then return Q, P(χ²_{k-1} ≥ Q)
L6  count the (k!)^b outcomes by their vector of rank sums, one block at a time
L7  p ← (number of outcomes with Σ_j R_j^2 ≥ the observed value) / (k!)^b
L8  return Q, p
```

The code keeps doubled midranks, so $Q$ is an exact fraction. Line L6 is a dynamic program: its state is the vector of column rank sums after the first $i$ blocks, and block $i + 1$ moves each state in $k!$ ways, one for each permutation of its ranks. Given the tie pattern in every block, the denominator $D$ and the total $\sum_j R_j = bk(k+1)/2$ are fixed, so $Q$ increases with $\sum_j R_j^2$, and line L7 compares integers.

## Example

**Eight judges, three wines.** The scores, one row per judge with wines 1, 2 and 3, are $(8.2, 7.1, 9.0)$, $(6.5, 6.1, 7.4)$, $(7.9, 7.0, 8.8)$, $(5.5, 5.9, 6.8)$, $(9.1, 8.0, 8.7)$, $(6.8, 6.0, 7.7)$, $(7.2, 6.9, 7.0)$ and $(8.0, 7.5, 8.5)$. The within-judge ranks are $(2, 1, 3)$ for five judges, $(1, 2, 3)$ for one and $(3, 1, 2)$ for two. So $R = (17, 9, 22)$, against the null mean $b(k+1)/2 = 16$. Without ties,
$$Q = \frac{12}{8 \cdot 3 \cdot 4}(17^2 + 9^2 + 22^2) - 3 \cdot 8 \cdot 4 = 106.75 - 96 = 10.75.$$
The chi-square tail with 2 degrees of freedom gives $p = 0.00463$. The exact count over the $6^8 = 1679616$ outcomes gives $p = 221/93312 = 0.00237$. Kendall's coefficient of concordance is $W = Q/(b(k-1)) = 0.672$. The Kruskal-Wallis test on the same 24 numbers, ignoring the judges, gives $p = 0.097$, because the differences between judges hide the differences between wines.

**Ties.** For the blocks $(1, 2, 2)$, $(3, 3, 1)$, $(2, 1, 3)$, $(1, 2, 3)$ and $(1, 1, 2)$, the tie-corrected statistic is $Q = 42/17 = 2.471$. The chi-square p-value is $0.291$ and the exact conditional p-value is $29/81 = 0.358$.

**Two treatments.** For $k = 2$ without ties, $Q = (S - b/2)^2/(b/4)$, where $S$ is the number of blocks in which treatment 2 is larger, so $Q$ is the square of the sign-test $z$ without the continuity correction. For 7 blocks with $S = 5$ the exact Friedman p-value is $29/64$, the same as the two-sided sign test.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Under $H_0$ each block's values are assigned to the treatments by a uniform random permutation, independently across blocks, so each of the $(k!)^b$ outcomes has the same probability given the values. The dynamic program of line L6 counts these outcomes by their rank-sum vectors by induction on the number of blocks. The statistic is an increasing function of $\sum_j R_j^2$ given the tie pattern, so the exact p-value is the upper tail of a discrete law and is valid. The chi-square limit follows from the central limit theorem for the sum over blocks of the independent rank vectors.

## Complexity

Line L1 sorts each block: $\Theta(b k \log k)$. Lines L2 to L4 take $\Theta(bk)$. The asymptotic test therefore costs $\Theta(b k \log k)$ time and $\Theta(bk)$ space. The exact count is far more expensive: each rank sum is at most $bk$ and the sums add up to a known total, so there are at most $(bk + 1)^{k-1}$ states, each updated in $k!$ ways per block, for $O(b \cdot k! \cdot (bk+1)^{k-1})$ time. For $b = 10$ and $k = 4$ the code kept 17561 states and took $0.68$ s of CPU time.

## Properties

- **Block effects vanish.** Ranks within a block do not change when a constant is added to the whole block, or when the block is transformed by any increasing function.
- **Distribution-free.** Given the tie pattern of each block, the exact null law depends only on $b$ and $k$.
- **Kendall's W.** $W = Q / (b(k-1))$ lies in $[0, 1]$ and measures the agreement of the $b$ rankings: $W = 1$ when all blocks give the same order. Without ties, the mean of the [Spearman correlations](/spearman-rank-correlation/) over all pairs of blocks is $(bW - 1)/(b - 1)$.
- **Chi-square accuracy.** Monte Carlo runs with $k = 3$, normal data and $r = 4000$ samples gave chi-square sizes at $\alpha = 0.05$ of $0.0428$ for $b = 5$ (seed 51) and $0.0485$ for $b = 20$ (seed 52).

## Variants and improvements

- **Exact tables and Monte Carlo.** For small $b$ and $k$ use the exact count. Otherwise draw random within-block permutations; the share of draws with $Q$ at least the observed value, with one added to the numerator and the denominator, is a valid [permutation test](/permutation-test/) p-value.
- **The F form.** Iman and Davenport (1980) proposed $F = (b - 1) Q / (b(k-1) - Q)$ referred to an F distribution, which is usually closer to the exact law than the chi-square.
- **Aligned ranks.** Subtracting a block estimate (such as the block mean) and ranking all $bk$ aligned values together uses the information between blocks and gains power when $k$ is small.
- **Ordered alternatives.** Page's test adds $j R_j$ over the treatments and has more power against a monotone trend.
- **Incomplete blocks.** Durbin's test extends the method to [balanced incomplete block designs](/balanced-incomplete-block-design/).
- **Follow-up comparisons.** After a significant result, pairwise comparisons of rank sums need a [multiple-comparison](/multiple-comparisons-problem/) correction.

## When to use it

Use it for repeated measures or blocked experiments with three or more treatments when the responses are ordinal, skewed, or on scales that differ from block to block: judges with their own scale, subjects with different baselines, algorithms compared over many data sets. For two treatments use the [signed-rank test](/wilcoxon-signed-rank-test/), which also uses the size of each difference. For independent groups use the Kruskal-Wallis test. When the errors are close to normal, two-way ANOVA is more powerful, especially for small $k$.

## Pitfalls

- **Ignoring the blocks.** Analyzing blocked data with the Kruskal-Wallis test lost almost all power in the Monte Carlo run above ($0.005$ against $0.442$).
- **Small $b$.** The chi-square approximation gave $P(Q \ge 5.991) = 0.0694$ for $k = 3$ and $b = 4$, above the nominal $0.05$. Use the exact count.
- **Ties.** Without the tie correction in the denominator, $Q$ is too small and the test conservative.
- **Low efficiency for small $k$.** With two or three treatments the test discards much information; for $k = 2$ it is only the sign test.
- **Missing values.** The test needs a complete table. Dropping incomplete blocks can bias the result; designs with planned missing cells need Durbin's test or a model.

## Implementations

## History

Milton Friedman, then a young economist, published the test in 1937. He replaced each row of a two-way table by its ranks and proposed the chi-square approximation for the spread of the rank sums; a short correction followed in 1939. Kendall and Babington Smith (1939) studied the same statistic as a measure of agreement among rankers, the coefficient of concordance $W$.

## References
