---
tag: 3E4H4P
kind: algorithm
slug: westfall-young-procedure
name: Westfall-Young procedure
aliases:
- maxT procedure
- permutation step-down procedure
area: statistics-and-inference/hypothesis-testing
level: advanced
summary: Compare each statistic, largest first, with the permutation law of the maximum over the hypotheses not yet rejected. This controls the FWER strongly and gains power from the dependence.
model: real-ram
complexity:
  vars: {m: the number of hypotheses, B: the number of permutations used, n: the number of units}
  time: {worst: Θ(B m n + m log m), table_given: Θ(B m + m log m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1993
  people: [Peter H. Westfall, S. Stanley Young]
  note: Westfall and Young set out the resampling-based step-down maxT and minP adjustments and the subset pivotality condition in their 1993 book. Ge, Dudoit and Speed (2003) made minP fast enough for microarray data.
prereqs: [permutation-test, closed-testing-principle]
see_also: [holm-bonferroni-method, bonferroni-correction, family-wise-error-rate, multiple-comparisons-problem, benjamini-hochberg-procedure, bootstrap-method, tukey-hsd, fisher-yates-shuffle]
sources:
  - book: isbn:9780471557616
    title: Peter H. Westfall and S. Stanley Young, Resampling-Based Multiple Testing, Examples and Methods for p-Value Adjustment, Wiley, 1993
    locator: the step-down resampling adjustments based on the maximum statistic and the minimum p-value, and the subset pivotality condition
  - paper: doi:10.1007/BF02595811
    title: Youngchao Ge, Sandrine Dudoit and Terence P. Speed, Resampling-based multiple testing for microarray data analysis, Test 12(1) (2003), pages 1 to 77
    locator: the step-down maxT and minP algorithms, and the fast minP algorithm that avoids the double resampling of the naive method
  - paper: doi:10.1198/016214504000000539
    title: Joseph P. Romano and Michael Wolf, Exact and approximate stepdown methods for multiple hypothesis testing, Journal of the American Statistical Association 100(469) (2005), pages 94 to 108
    locator: the general step-down method with monotone critical values, exact for randomization tests and approximate with the bootstrap, without subset pivotality
---

The Westfall-Young procedure controls the [family-wise error rate](/family-wise-error-rate/) for $m$ tests computed on the same data, and it uses the dependence between the tests instead of a worst-case bound. Each test has a statistic $t_j$, large when $H_j$ looks false. Sort them so that $t_{(1)} \ge \dots \ge t_{(m)}$. Recompute all $m$ statistics on every relabeling of the data in a [permutation test](/permutation-test/) group $G$ of size $B$, the identity included. The hypothesis of rank $k$ is compared with the permutation law of the maximum of the statistics of ranks $k, \dots, m$, the ones not yet rejected. Its adjusted p-value is
$$\tilde p_{(k)} = \max_{j \le k}\frac{\#\{g \in G : \max_{l \ge j}T_{(l)}(g) \ge t_{(j)}\}}{B}.$$
This is the maxT method. When the tests are independent its thresholds are close to those of [Holm's method](/holm-bonferroni-method/); when they are strongly correlated, the maximum of $m$ statistics is not much larger than one statistic, and the method rejects nearly as much as unadjusted tests would.

## In plain words

When many tests use the same data, they often move together. A Bonferroni-type correction ignores this and assumes the worst case. The Westfall-Young method measures it. It shuffles the group labels many times, and for each shuffle it records the largest test result over all the tests. This shows how large the largest result can be when nothing is real. A result is called real only if it beats that largest value often enough. Then the method removes that result and repeats with the tests that remain, which makes the bar a little lower each time. If the tests move together, the largest result over all of them is not much bigger than a single result, so the bar stays low and more real effects are found.

## The problem

**Input.** Data $Z$, a finite group $G$ of $B$ transformations of the data (in the two-sample case, the relabelings of the units into two groups of sizes $n_1$ and $n_2$), and statistics $T_1, \dots, T_m$ with observed values $t_j = T_j(Z)$. A level $\alpha \in (0, 1)$. The set of true nulls is $I_0$, with $m_0$ elements.

**Output.** The adjusted p-values $\tilde p_1, \dots, \tilde p_m$, and the rejected set $\{j : \tilde p_j \le \alpha\}$.

**Error rate controlled.** Strong control of the family-wise error rate: $P(V \ge 1) \le \alpha$ for every set $I_0$ of true nulls.

**Dependence assumption.** No assumption on the dependence between the statistics. The assumption is on the data: the joint law of the true-null part of the data is invariant under $G$. In the two-sample case this means that the vectors of the null variables of the units are exchangeable across the two groups. It is the randomization hypothesis of the permutation test, applied to all true nulls together. Westfall and Young state a closely related condition, subset pivotality.

**Exact or asymptotic.** Exact in finite samples, as an inequality, when $G$ is enumerated or sampled at random with the identity added. With bootstrap resampling instead of permutations the control is only asymptotic.

## The algorithm

The input is the table $T_j(g)$, one row per element of $G$, the identity among them.

```pseudo id=main
MAXT-STEP-DOWN(t₁, …, t_m, rows T(g) for g ∈ G)
L1  sort so that t_(1) ≥ … ≥ t_(m); count[1..m] ← 0
L2  for each g ∈ G do u ← -∞
L3      for k ← m down to 1 do            ▷ successive maxima, from the bottom
L4          u ← max(u, T_(k)(g))          ▷ u = max over ranks ≥ k
L5          if u ≥ t_(k) then count[k] ← count[k] + 1
L6  run ← 0; for k ← 1 to m do
L7      run ← max(run, count[k] / B); p̃_(k) ← run
L8  return p̃
```

Line L2 starts each row with $u = -\infty$. One pass from the bottom computes all the maxima over tails at once, so a row costs $\Theta(m)$. The running maximum at line L7 enforces the step-down order: a hypothesis is rejected only if all those with larger statistics are rejected.

The **single-step** version compares every $t_j$ with the maximum over all $m$ statistics: $\#\{g : \max_lT_l(g) \ge t_j\}/B$. The step-down version is never larger. The **minP** version replaces each statistic by its marginal permutation p-value and uses the minimum p-value instead of the maximum statistic. It puts the tests on a common scale, at the cost of a second level of resampling.

## Example

**A hand example.** Eight units, the first four in group 1, and three integer variables:

| unit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| variable 1 | 12 | 15 | 11 | 14 | 6 | 8 | 5 | 9 |
| variable 2 | 30 | 33 | 29 | 35 | 25 | 27 | 24 | 26 |
| variable 3 | 7 | 9 | 2 | 8 | 6 | 4 | 5 | 3 |

The statistic is $|n_2S_1 - n_1S_2|$, where $S_1$ and $S_2$ are the group sums, an integer multiple of the difference of the means. The observed values are $t = (96, 100, 32)$. The group $G$ is the set of all $\binom84 = 70$ splits. Variables 1 and 2 separate the groups completely, so only the observed split and its mirror reach their observed values, and their marginal permutation p-values are $2/70 = 0.0286$. Variable 3 has marginal p-value $24/70$.

| rank $k$ | variable | $t_{(k)}$ | maximum over | count | count / 70 | $\tilde p_{(k)}$ |
|---|---|---|---|---|---|---|
| 1 | 2 | 100 | variables 2, 1, 3 | 2 | 0.0286 | 0.0286 |
| 2 | 1 | 96 | variables 1, 3 | 2 | 0.0286 | 0.0286 |
| 3 | 3 | 32 | variable 3 | 24 | 0.343 | 0.343 |

At $\alpha = 0.05$ the procedure rejects variables 1 and 2. [Holm's method](/holm-bonferroni-method/) on the marginal permutation p-values compares $2/70$ with $0.05/3 = 0.0167$ and rejects nothing; so does the [Bonferroni correction](/bonferroni-correction/). The single-step maxT p-value of variable 3 is $48/70 = 0.686$, twice its step-down value.

**Two copies of one variable.** If the data hold the same perfectly separated variable twice, the maximum of the two statistics is the statistic itself, so both adjusted p-values are $2/70$ and both are rejected at 0.05. Holm gives $4/70 = 0.057$ to both and rejects nothing. This is the extreme case of the gain from dependence.

**A small simulation.** In the tests, each of 8 units has a common random effect, so four integer variables are correlated about 0.9. Variables 3 and 4 are shifted in group 1, variables 1 and 2 are not. Over 500 data sets, with all 70 splits enumerated in each, the maxT step-down procedure has measured FWER 0.030 at $\alpha = 0.05$ and rejects 28% of the false nulls. Holm on the marginal permutation p-values never rejects, because the smallest possible p-value is $2/70$ and $4 \cdot 2/70 = 0.114 > 0.05$. This shows a practical point: with few units, only a method that uses the joint permutation law can reject anything.

## Correctness

Two facts carry the proof. First, the maxT step-down procedure is a shortcut of the [closed testing principle](/closed-testing-principle/). For a set $I$ of hypotheses, test the intersection $H_I$ with the permutation test of $\max_{j \in I}T_j$. If $j$ is the smallest rank in $I$, then $I$ is contained in the tail $S_j$ of ranks $j, \dots, m$, the maximum of the observed values over $I$ is $t_{(j)}$, and so the local p-value of $I$ is at most that of $S_j$. So the largest local p-value over the sets that contain rank $k$ is attained at a tail, which is the formula above. The tests check this equality, in exact rational arithmetic, against closed testing over all $2^m - 1$ subsets.

Second, the error event is a single permutation test. If a true null is rejected, the true null with the largest statistic, at rank $k^*$, is rejected, and its count is computed over a tail $S_{k^*}$ that contains every true null. So the permutation p-value of $\max_{j \in I_0}T_j$ is at most $\alpha$. This statistic depends only on the true-null part of the data, and by the exact level of the permutation test (Claim 2 in the proof for the [permutation test](/permutation-test/)), it is at most $\alpha$ with probability at most $\alpha$. The behavior of the false nulls under permutation never enters. The [correctness proof](proofs/correctness.md) gives the details.

## Complexity

On a [real RAM](/real-ram/), given the $B \times m$ table, line L1 sorts in $\Theta(m\log m)$, lines L2 to L5 take $\Theta(Bm)$ and lines L6 and L7 take $\Theta(m)$. Building the table dominates: each two-sample statistic costs $\Theta(n)$ per variable and permutation, so the total is $\Theta(Bmn + m\log m)$. Rows can be streamed, so the extra space is $\Theta(m)$ for the counts; the reference code keeps the table for clarity.

With full enumeration $B = \binom{n}{n_1}$, which grows fast; in practice $B$ random permutations are drawn with a [shuffle](/fisher-yates-shuffle/) and the identity is added, which keeps the level exact. The naive minP version needs a permutation p-value for each statistic in each row, $\Theta(B^2m)$ comparisons, or $\Theta(Bm\log B)$ if each column is sorted once. Ge, Dudoit and Speed (2003) give an algorithm that avoids the double resampling.

## Properties

- **Strong FWER control under the randomization hypothesis for the true nulls**, in finite samples, with no assumption on the dependence between the statistics. Proved.
- **Closed testing.** The step-down adjusted p-values equal those of closed testing with maxT permutation local tests. Proved and tested.
- **Order.** For each hypothesis, marginal permutation p-value $\le$ step-down $\le$ single-step. Proved and tested.
- **Adapts to dependence.** Under independence the gain over Holm is small; under strong positive dependence the adjusted p-values approach the marginal ones. The size of the gain is measured, not proved.
- **Monotone in the statistic.** A larger observed statistic never gets a larger adjusted p-value.
- **Discreteness.** Adjusted p-values are multiples of $1/B$. With $B$ small, as in the hand example, some levels cannot be reached exactly and the FWER is below $\alpha$.

## Variants and improvements

- **minP.** Use $\min_j$ of the marginal permutation p-values in place of $\max_j T_j$. It weighs the tests equally when the statistics have different null scales; maxT with unstandardized statistics lets variables with a large spread dominate the maximum.
- **Bootstrap version.** Resample from a null-centered empirical distribution instead of permuting. This works when no permutation group fits the null, but the control is only asymptotic; Romano and Wolf (2005) give the theory.
- **Romano-Wolf step-down.** Any family of intersection tests with critical values that decrease as hypotheses are removed gives a valid step-down method; maxT is the case of a permutation test of the maximum.
- **FDR and other error rates.** Resampling estimates of the null law of the number of false rejections give FDR methods and procedures for $k$-FWER and false discovery proportions; see the [false discovery rate](/false-discovery-rate/).

## When to use it

Use it when you have the raw data, a permutation group that matches the null, and many correlated tests, such as the genes of a microarray, the voxels of an image or the end points of a trial measured on the same subjects. Under independence it is close to Holm on the same statistics, and under strong correlation or with few units it is much more powerful. When the tests are nearly independent and $m$ is large, the gain is small and [Holm's method](/holm-bonferroni-method/) is cheaper. When many true effects are expected, control the FDR with the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) instead.

## Pitfalls

- **Permuting variables one at a time.** The method must permute whole units, so that every row of the table uses the same relabeling for all $m$ statistics. Separate permutations for each test destroy the dependence that the method uses.
- **A null that does not fit the group.** Permutation tests the equality of the whole joint distribution of the null variables in the two groups. If the null hypotheses are about means only and the variances or correlations differ between the groups, the randomization hypothesis fails and the guarantee is lost. Equal marginal laws are not enough; the joint law of the null variables must be the same.
- **Leaving out the identity.** With random permutations, add the observed labeling to the set of rows, or use $(1 + c)/(1 + B)$. A count that can be 0 is not a valid p-value.
- **Too few units.** With $n = 8$ the smallest attainable p-value is $2/70$. No method can reject at a level below that.
- **Statistics on different scales.** With maxT, use studentized statistics, or use minP.

## Implementations

## History

Westfall and Young collected resampling-based p-value adjustments in their 1993 book, including the step-down maxT and minP methods and the subset pivotality condition under which they control the family-wise error rate strongly. The methods became standard in genomics after Ge, Dudoit and Speed (2003) analyzed them for microarray data and gave a fast algorithm for minP, implemented with maxT in the Bioconductor package multtest. Romano and Wolf (2005) took the step-down idea apart into intersection tests with monotone critical values, which gave exact control for randomization tests and asymptotic control for bootstrap tests without subset pivotality.

## References
