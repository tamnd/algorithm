---
tag: 24Z82C
kind: definition
slug: randomized-block-design
name: Randomized complete block design
aliases:
- RCBD
- randomized block design
area: statistics-and-inference/causal-inference-and-experimental-design
level: intro
summary: Groups similar units into blocks of t and randomizes each of t treatments once within every block, so differences between blocks drop out of the treatment comparisons.
prereqs: [randomized-experiment, one-way-anova]
see_also: [two-way-anova, latin-square-design, balanced-incomplete-block-design, friedman-test, linear-mixed-model, tukey-hsd, fisher-yates-shuffle, cuped]
sources:
  - book: "Ronald A. Fisher, The Design of Experiments, Oliver and Boyd, Edinburgh, 1935"
    title: The Design of Experiments
    locator: the chapters on field experiments in randomized blocks (general locator, chapter not confirmed)
  - book: isbn:9780471718130
    title: George E. P. Box, J. Stuart Hunter and William G. Hunter, Statistics for Experimenters, second edition, Wiley, 2005
    locator: Section 4.2 (randomized block designs), starting on p. 145
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: Chapter 4 (randomized blocks, Latin squares and related designs; chapter-level locator)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Chapter 11 (analysis of variance and the partition of sums of squares; chapter-level locator)
---

A randomized complete block design (RCBD) is the simplest way to remove a known source of variation from a comparison of treatments. The experimental units are first sorted into blocks of similar units, such as plots in the same strip of a field, batches of the same raw material or measurements on the same day. Each block holds exactly as many units as there are treatments, every treatment is given to exactly one unit of each block, and the order inside each block is randomized separately. The treatments are then compared inside blocks, so the differences between blocks leave the error. It is a [randomized experiment](/randomized-experiment/) with a restricted randomization, and its standard analysis is a [two-way ANOVA](/two-way-anova/) with one observation per cell and no interaction.

## Definition

Let there be $t \ge 2$ treatments and $b \ge 2$ blocks of $t$ units each, $tb$ units in all. A **randomized complete block design** assigns the treatments by an independent, uniformly random permutation of $\{1, \dots, t\}$ to the units of each block, for example by a [Fisher-Yates shuffle](/fisher-yates-shuffle/) per block. So each of the $(t!)^b$ plans has probability $(t!)^{-b}$, and every treatment occurs exactly once in every block.

Write $y_{ij}$ for the response of treatment $i$ in block $j$. The usual model is additive:

$$y_{ij} = \mu + \tau_i + \beta_j + e_{ij}, \qquad \sum_i\tau_i = 0, \quad \sum_j\beta_j = 0,$$

with iid $N(0, \sigma^2)$ errors. With the treatment means $\bar y_{i\cdot}$, the block means $\bar y_{\cdot j}$ and the grand mean $\bar y$, the analysis is

| source | sum of squares | degrees of freedom |
|---|---|---|
| treatments | $SS_T = b\sum_i(\bar y_{i\cdot} - \bar y)^2$ | $t - 1$ |
| blocks | $SS_B = t\sum_j(\bar y_{\cdot j} - \bar y)^2$ | $b - 1$ |
| error | $SSE = \sum_{i,j}(y_{ij} - \bar y_{i\cdot} - \bar y_{\cdot j} + \bar y)^2$ | $(t - 1)(b - 1)$ |

and the test of $H_0: \tau_1 = \dots = \tau_t$ uses $F = \frac{SS_T/(t-1)}{SSE/((t-1)(b-1))}$.

**Theorem (the analysis is exact).** $SST = SS_T + SS_B + SSE$, the three terms are squared lengths of projections onto orthogonal subspaces, and under the model $F \sim F_{t-1,(t-1)(b-1)}$ when all $\tau_i = 0$, whatever the block effects are.

*Proof.* In $\mathbb R^{tb}$ let $V_0$ be the constant vectors, $V_T$ the vectors $v_{ij} = a_i$ with $\sum_i a_i = 0$, and $V_B$ the vectors $v_{ij} = c_j$ with $\sum_j c_j = 0$. For $a \in V_T$ and $c \in V_B$, $\langle a, c\rangle = \sum_i\sum_j a_ic_j = (\sum_i a_i)(\sum_j c_j) = 0$, and both are orthogonal to the constants because their entries sum to zero. This is the only place where completeness is used: every treatment meets every block exactly once. Let $V_E$ be the orthogonal complement of $V_0 \oplus V_T \oplus V_B$, of dimension $tb - 1 - (t - 1) - (b - 1) = (t-1)(b-1)$. The projection of $y$ onto $V_T$ is $\bar y_{i\cdot} - \bar y$ at $(i, j)$, because $y - (\bar y_{i\cdot} - \bar y)$ is orthogonal to $V_T$; in the same way for $V_B$ and $V_0$. The remainder $y_{ij} - \bar y_{i\cdot} - \bar y_{\cdot j} + \bar y$ is the projection onto $V_E$. Pythagoras gives the decomposition. The mean vector $\mu + \tau_i + \beta_j$ lies in $V_0 \oplus V_T \oplus V_B$, so its projection onto $V_E$ is 0, and its projection onto $V_T$ is $\tau$. By the lemma on projections of a normal vector in the [one-way ANOVA](/one-way-anova/) proof, $SS_T/\sigma^2$ and $SSE/\sigma^2$ are independent, $SSE/\sigma^2 \sim \chi^2_{(t-1)(b-1)}$, and $SS_T/\sigma^2 \sim \chi^2_{t-1}$ when $\tau = 0$. $\square$

The test file checks the closed forms against exact least squares by model comparison, in rational arithmetic, on random tables. If the additive model fails because treatments and blocks interact, the interaction goes into $SSE$: $E[MSE] = \sigma^2 + \sum_{i,j}\gamma_{ij}^2/((t-1)(b-1))$ for interaction effects $\gamma_{ij}$, and the F-test loses power. The design has no replication inside cells, so it cannot separate interaction from error.

**Why blocking helps.** The difference of two treatment means is $\bar y_{i\cdot} - \bar y_{k\cdot} = \tau_i - \tau_k + \bar e_{i\cdot} - \bar e_{k\cdot}$: the block effects cancel exactly, because both treatments appear once in every block. Its variance is $2\sigma^2/b$, where $\sigma^2$ is the variation inside blocks only. A completely randomized design on the same units has the variation between blocks in its error as well. The **relative efficiency** estimates the ratio of the two error variances from the blocked analysis,

$$RE = \frac{(b - 1)MS_B + b(t - 1)MSE}{(tb - 1)MSE},$$

the number of completely randomized replicates that one block is worth.

**Randomization.** Randomizing inside each block makes the assignment independent of every unit property, including the ones that the blocks do not capture. It justifies the comparison without the normal model: under the sharp null of no effect on any unit, the distribution of $F$ over the $(t!)^b$ equally likely plans gives an exact [permutation test](/permutation-test/) (Fisher, 1935).

## Examples and non-examples

**Example: four treatments in five blocks.** Four treatments A to D are tried on five batches of material (the blocks), with each batch split into four parts:

| treatment | block 1 | block 2 | block 3 | block 4 | block 5 | mean |
|---|---|---|---|---|---|---|
| A | 20 | 26 | 30 | 18 | 28 | 24.4 |
| B | 23 | 26 | 34 | 19 | 31 | 26.6 |
| C | 18 | 24 | 31 | 17 | 25 | 23 |
| D | 24 | 29 | 34 | 22 | 31 | 28 |
| block mean | 21.25 | 26.25 | 32.25 | 19 | 28.75 | 25.5 |

| source | sum of squares | df | mean square | F | p |
|---|---|---|---|---|---|
| treatments | 74.6 | 3 | 24.867 | $746/31 = 24.065$ | $2.30 \cdot 10^{-5}$ |
| blocks | 468 | 4 | 117 | 113.23 | $2.0 \cdot 10^{-9}$ |
| error | 12.4 | 12 | $31/30 = 1.0333$ | | |
| total | 555 | 19 | | | |

The treatments differ clearly ($F_{(3,12,0.95)} = 3.4903$). The relative efficiency is $14505/589 = 24.63$: an unblocked experiment would need about 25 times as many units for the same precision. The standard error of a difference of two treatment means is $\sqrt{2MSE/5} = 0.643$.

**Non-example: the same data analysed as one-way.** Ignoring the blocks puts $SS_B$ into the error: $SSW = 468 + 12.4 = 480.4$ on 16 degrees of freedom, and the [one-way ANOVA](/one-way-anova/) gives $F = 0.8282$ on $(3, 16)$, $p = 0.4975$. The standard error of a difference becomes $3.466$. Analysing a blocked experiment as if it were completely randomized throws away the design.

**Example: matched pairs.** With $t = 2$ the design is the paired comparison, and $F = T^2$, where $T$ is the paired [Student t](/student-t-test/) statistic of the within-block differences. Treatments A and B of the example alone give $F = 242/27 = 8.963$, $T = -2.994$ on 4 degrees of freedom, and $p = 0.0402$.

**Non-example: blocks smaller than the number of treatments.** When a block holds fewer than $t$ units (a day allows only three runs, a judge can taste only four wines), the design is incomplete. The orthogonality in the theorem fails, and the treatment means must be adjusted for blocks; the [balanced incomplete block design](/balanced-incomplete-block-design/) keeps the analysis simple.

**Non-example: one randomization for all blocks.** Using the same random order in every block is not an RCBD. A trend in position inside the blocks (the east side of each strip, the last run of each day) then hits the same treatment every time. Two crossed nuisance factors such as rows and columns call for a [Latin square design](/latin-square-design/) instead.

**Example: ranks.** For data far from normal, the [Friedman test](/friedman-test/) ranks the $t$ responses inside each block and has an exact null law under the same randomization.

## Related definitions

- [Two-way ANOVA](/two-way-anova/): the RCBD analysis is the additive two-way model with one observation per cell; with replicates in each cell the interaction can be tested.
- [Latin square design](/latin-square-design/): blocks in two directions at once, rows and columns, with $t$ levels each.
- [Balanced incomplete block design](/balanced-incomplete-block-design/): blocks smaller than $t$, with every pair of treatments together equally often.
- [Linear mixed model](/linear-mixed-model/): treats the block effects as random, $\beta_j \sim N(0, \sigma_\beta^2)$. In a complete balanced design the treatment F-test is the same, and the variance components come from [restricted maximum likelihood](/restricted-maximum-likelihood/).
- [Tukey's test](/tukey-hsd/) and [Scheffé's method](/scheffe-method/): follow-up comparisons of the treatment means with $MSE$ on $(t-1)(b-1)$ degrees of freedom.
- [CUPED](/cuped/): adjusts for a pre-experiment covariate after the experiment, where blocking stratifies on it before; both remove predictable variation from the comparison.

## References
