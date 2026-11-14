---
tag: E9ZZA5
kind: algorithm
slug: two-way-anova
name: Two-way analysis of variance
aliases:
- two-way ANOVA
- two-factor ANOVA
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Tests the main effects of two factors and their interaction by F ratios of nested residual sums of squares. Exact F laws under normal errors; unbalanced data need type I, II or III.
model: real-ram
complexity:
  vars: {n: the total number of observations, p: "the number of cells, a times b"}
  time: {worst: Θ(n p^2), best: Θ(n p^2)}
  space: {extra: Θ(n p)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1925
  people: [Ronald A. Fisher, Frank Yates]
  note: Fisher analysed two-way field trials at Rothamsted in the 1920s. Yates (1934) treated unequal cell numbers and gave the weighted squares of means, the ancestor of the type III sums of squares.
prereqs: [one-way-anova, regression-f-test, ordinary-least-squares]
see_also: [randomized-block-design, factorial-design, latin-square-design, tukey-hsd, linear-mixed-model, friedman-test, hat-matrix, qr-decomposition]
sources:
  - paper: doi:10.1080/01621459.1934.10502686
    title: "Frank Yates, The analysis of multiple classifications with unequal numbers in the different classes, Journal of the American Statistical Association 29(185), 1934"
    locator: pp. 51 to 66 (fitting constants and the weighted squares of means for unbalanced two-way data)
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: Chapter 5 (introduction to factorial designs, the two-factor factorial design and its analysis of variance)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 8 (analysis of variance, two-way classifications with equal and unequal numbers per cell; chapter-level locator)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Chapter 11 (analysis of variance and regression; chapter-level locator)
  - url: https://psychclassics.yorku.ca/Fisher/Methods/
    title: Ronald A. Fisher, Statistical Methods for Research Workers, Oliver and Boyd, 1925, online text of the first edition
    locator: Chapter VIII (further applications of the analysis of variance)
---

Two-way analysis of variance tests the effects of two factors on a response, for example a fertilizer (factor A) and a crop variety (factor B), measured in every combination. It tests three null hypotheses: no effect of A, no effect of B, and no interaction, which means that the effect of A is the same at every level of B. Each test is a [regression F-test](/regression-f-test/): the drop in the residual sum of squares when the term is added to a smaller model, per degree of freedom, over the residual mean square of the full model. Under normal errors with a common variance each statistic has an exact F law. When every cell has the same number of observations, the sums of squares are orthogonal and the analysis has one answer. When the cells are unbalanced, the sum of squares of a term depends on which other terms are in the smaller model, and there are three standard choices, called type I, II and III. They test different hypotheses, so a report must say which one it used.

## In plain words

You grow plants under two treatments at once, say fertilizer and watering, in every combination. You want to know whether fertilizer matters, whether watering matters, and whether the best fertilizer depends on the watering. Two-way ANOVA answers the three questions from one experiment, each by comparing the spread it explains with the noise between plants that got the same treatment pair. If every combination has the same number of plants, the three questions separate cleanly. If some combinations have more plants than others, the factors overlap. The part of the variation that fertilizer "explains" then depends on whether watering was taken into account first, and different programs report different numbers. Say which convention you used.

## The problem

**Model.** Factor A has levels $i = 1, \dots, a$ and factor B has levels $j = 1, \dots, b$. Cell $(i, j)$ holds $n_{ij} \ge 1$ observations $y_{ijl}$, $l = 1, \dots, n_{ij}$, with $n = \sum n_{ij} > ab$. The model is

$$y_{ijl} = \mu_{ij} + e_{ijl} = m + \alpha_i + \beta_j + \gamma_{ij} + e_{ijl},$$

with iid $N(0, \sigma^2)$ errors and the sum-to-zero constraints $\sum_i\alpha_i = \sum_j\beta_j = 0$ and $\sum_i\gamma_{ij} = \sum_j\gamma_{ij} = 0$. Then $m$ is the mean of the $ab$ cell means, $\alpha_i = \bar\mu_{i\cdot} - m$ is the deviation of the unweighted row mean of the cell means, $\beta_j$ the same for columns, and $\gamma_{ij}$ the interaction. The additive model sets every $\gamma_{ij} = 0$.

**Hypotheses.** $H_{AB}$: all $\gamma_{ij} = 0$ (no interaction); $H_A$: no A effect; $H_B$: no B effect. With an interaction, "no A effect" needs a definition, and the types define it differently (below).

**Statistics.** For column sets $S \subset L$ let $RSS(S)$ be the residual sum of squares of the least squares fit of $y$ on the columns of $S$. The columns are the intercept $1$, the $a - 1$ effect-coded columns of A (level $i < a$ gets $+1$, level $a$ gets $-1$), the $b - 1$ columns of B, and the $(a-1)(b-1)$ products AB. The term's sum of squares is $SS = RSS(S) - RSS(L)$ on $d = |L| - |S|$ degrees of freedom, and

$$F = \frac{SS/d}{SSE/(n - ab)}, \qquad SSE = RSS(\{1, A, B, AB\}).$$

| term | type I (A first) | type II | type III |
|---|---|---|---|
| A | $RSS(1) - RSS(1, A)$ | $RSS(1, B) - RSS(1, A, B)$ | $RSS(1, B, AB) - SSE$ |
| B | $RSS(1, A) - RSS(1, A, B)$ | $RSS(1, A) - RSS(1, A, B)$ | $RSS(1, A, AB) - SSE$ |
| AB | $RSS(1, A, B) - SSE$ | same | same |

Type III with effect coding tests $H_A: \bar\mu_{1\cdot} = \dots = \bar\mu_{a\cdot}$, equal unweighted marginal means of the cell means. Type II tests "no A effect" in the additive model; with an interaction its hypothesis is a weighted one whose weights depend on the cell counts. Type I is sequential and depends on the order of the factors.

**Null distribution.** Exact: each $F$ has the $F_{d, n-ab}$ law when the term's hypothesis holds, for every $n$ (Lemma 2 of the correctness proof). Under the alternative it is noncentral F.

**Rejection rule, size and p-value.** Reject when $F \ge F_{(d, n-ab, 1-\alpha)}$, with size exactly $\alpha$ for each test. The p-value is the upper tail $P(F_{d, n-ab} > F)$. The three tests together are not a family with error rate $\alpha$.

**Sensitivity.** Each test reacts only to its own term. The interaction test reacts to non-parallel profiles of the cell means. When the interaction is large, the main effects average over effects of different sizes or signs, and the main effect tests can miss real effects or show effects that hold at no single level.

## The algorithm

```pseudo id=main
TWO-WAY-ANOVA(y[1..n], A-labels, B-labels, type)   ▷ every cell nonempty, n > a·b
L1  build the columns: 1, the effect columns of A and B, their products AB
L2  SSE ← RSS(1, A, B, AB)                ▷ RSS by modified Gram-Schmidt, two passes
L3  if type = I:  SS_A ← RSS(1) - RSS(1, A);       SS_B ← RSS(1, A) - RSS(1, A, B)
L4  if type = II: SS_A ← RSS(1, B) - RSS(1, A, B); SS_B ← RSS(1, A) - RSS(1, A, B)
L5  if type = III: SS_A ← RSS(1, B, AB) - SSE;     SS_B ← RSS(1, A, AB) - SSE
L6  SS_AB ← RSS(1, A, B) - SSE
L7  for each term: F ← (SS / d) / (SSE / (n - a·b)); p ← F̄(F; d, n - a·b)
L8  return the table of SS, d, F and p
```

$RSS(S)$ orthogonalizes the columns of $S$ one by one with modified Gram-Schmidt, each twice, and removes the component of $y$ along each new unit vector; what is left is the residual. This is the [QR decomposition](/qr-decomposition/) without storing $R$. The normal equations $X^\top X b = X^\top y$ are never formed. An empty cell makes the interaction columns linearly dependent, and the code raises an error. For balanced data the code also has the closed forms of the correctness proof.

## Example

**Balanced.** A 2 x 3 layout with $n_{ij} = 2$:

| | $B_1$ | $B_2$ | $B_3$ | row mean |
|---|---|---|---|---|
| $A_1$ | 12, 14 | 18, 16 | 21, 23 | 17.333 |
| $A_2$ | 15, 13 | 24, 22 | 30, 28 | 22 |
| column mean | 13.5 | 20 | 25.5 | 19.667 |

| source | SS | d | F | p |
|---|---|---|---|---|
| A | $196/3 = 65.333$ | 1 | 32.667 | 0.00124 |
| B | $866/3 = 288.667$ | 2 | 72.167 | 0.0000636 |
| AB | $62/3 = 20.667$ | 2 | 5.1667 | 0.04957 |
| error | 12 | 6 | | |

The critical values are $F_{(1, 6, 0.95)} = 5.9874$ and $F_{(2, 6, 0.95)} = 5.1433$, so all three terms are significant at 5%, the interaction just. The cell means 13, 17, 22 in row 1 and 14, 23, 29 in row 2 show why: the A difference grows from 1 to 7 across the levels of B. Types I, II and III give the same table, in either order.

**Unbalanced.** A 2 x 2 layout with cells $(1,1) = \{3, 5\}$, $(1,2) = \{7\}$, $(2,1) = \{6\}$ and $(2,2) = \{10, 12, 11\}$, cell means 4, 7, 6 and 11, and $SSE = 4$ on 3 degrees of freedom:

| test of | SS | F | p |
|---|---|---|---|
| A, type I with A first | $1083/28 = 38.679$ | 29.01 | 0.0125 |
| A, type II (= type I with B first) | $676/51 = 13.255$ | 9.941 | 0.0511 |
| A, type III | $216/17 = 12.706$ | 9.529 | 0.0538 |
| B, type I with A first (= type II) | $1587/68 = 23.338$ | 17.50 | 0.0249 |
| B, type I with B first | $1024/21 = 48.762$ | 36.57 | 0.0091 |
| B, type III | $384/17 = 22.588$ | 16.94 | 0.0260 |
| AB, every type | $24/17 = 1.412$ | 1.059 | 0.3792 |

The test of A is significant at 5% by type I with A first and not by types II and III. Type I with A first credits A with the variation it shares with B, because the large cell $(2, 2)$ is at the high levels of both factors. The type III value is the squared marginal contrast: $\hat\psi = \frac12(4 + 7) - \frac12(6 + 11) = -3$, with $\sum c^2/n_{ij} = \frac14(\frac12 + 1 + 1 + \frac13) = 17/24$, and $9/(17/24) = 216/17$. With treatment (0/1) coding instead of effect coding, the same "type III" comparison gives $SS_A = 8/3$ and $SS_B = 6$. On the balanced data above it gives $SS_A = 1$ instead of $196/3$ and $SS_B = 244/3$ instead of $866/3$. It tests the A difference at the reference level $B_1$ only, where the cell means are 13 and 14, and the B differences at $A_1$ only.

## Correctness

Each sum of squares is $RSS(S) - RSS(L) = \|(P_L - P_S)y\|^2$ for nested column spaces, where $P$ is an orthogonal projection, and $SSE = \|(I - P_F)y\|^2$ for the full model. The two projections have orthogonal ranges, so under normal errors the two squared lengths are independent chi-square variables, and the F ratio has an exact F law when $(P_L - P_S)\mu = 0$. With effect coding this condition for type III A is equal unweighted marginal means. In a balanced layout the subspaces of A, B and AB are mutually orthogonal, because every inner product factors into a sum of a zero-sum vector. So each difference is the projection onto the term's own subspace, whatever the order, and all types agree. The proofs and the exact unbalanced computation are in the correctness proof below.

## Complexity

On a [real RAM](/real-ram/), one RSS orthogonalizes at most $p = ab$ columns of length $n$, each against all earlier ones, twice: $O(np^2)$ operations. The code computes at most five RSS values, so the time is $\Theta(np^2)$ and the extra space is $\Theta(np)$ for the orthonormal basis. For balanced data the closed forms cost $\Theta(n)$. A sparse or structured solver can do better for many levels, but $p$ is small in practice.

**Numerical stability.** Modified Gram-Schmidt with one reorthogonalization pass keeps the computed basis orthogonal to working precision, so the RSS values have small relative error even when the columns are nearly dependent (few observations in some cells). Solving the normal equations squares the condition number of the column matrix. The closed forms subtract means before squaring, as in [one-way ANOVA](/one-way-anova/). Differences of two RSS values can cancel when the term explains little; the result is then small in absolute terms, which is the right answer.

## Properties

- **Exact.** Each F test has size exactly $\alpha$ under the normal model with equal variances.
- **Balanced means orthogonal.** With equal cell counts the sums of squares do not depend on the order or the type. With proportional counts, $n_{ij} = n_{i\cdot}n_{\cdot j}/n$, the A and B columns are still orthogonal after the mean is removed, so types I and II agree in either order, but type III still differs.
- **Additive model.** Without the AB term the error has $n - a - b + 1$ degrees of freedom. With one observation per cell the interaction cannot be separated from the error, and the additive model is the [randomized block design](/randomized-block-design/) analysis.
- **Invariance of type II.** Types I and II depend only on the column spaces, so any full-rank coding gives the same values. Type III depends on the coding of the interaction; with effect coding it tests equal unweighted marginal means.
- **Hierarchy.** Type II respects marginality: it never tests a main effect after an interaction that contains it.

## Variants and improvements

- **More factors.** The same nested comparisons give k-way ANOVA. With two-level factors this is the [factorial design](/factorial-design/) analysis, where Yates's algorithm computes all effects at once.
- **Random and mixed effects.** If the levels of B are a sample (subjects, batches), B and AB are random, and the F test of A uses the AB mean square as the denominator in the balanced case. The general tool is the [linear mixed model](/linear-mixed-model/) fitted by [restricted maximum likelihood](/restricted-maximum-likelihood/).
- **Rank methods.** The [Friedman test](/friedman-test/) handles the additive layout with one observation per cell without normality.
- **Multiple comparisons.** [Tukey's test](/tukey-hsd/) on the marginal means of a balanced layout, with the error mean square of the full model.

## When to use it

Use two-way ANOVA when two crossed factors are applied in every combination and the errors are close to normal with equal variances. Look at the interaction test and the profile plot of the cell means first. If the interaction is clear, interpret the effects of A within each level of B. In unbalanced data, prefer type II when there is no interaction, and type III with effect coding when you want equal-weight marginal means; never use type III with treatment coding.

## Pitfalls

- **Not saying which type.** In the unbalanced example, A has p = 0.0125, 0.0511 or 0.0538 depending on the type.
- **Type III with treatment coding.** It silently tests a simple effect at the reference level, $SS_A = 1$ instead of $65.333$ on the balanced data.
- **Main effects in the presence of interaction.** A main effect averages over the levels of the other factor and can be zero while every simple effect is large.
- **One observation per cell with an interaction term.** The full model then has no error degrees of freedom.
- **Empty cells.** With an empty cell the interaction model is not of full rank, and the type III hypothesis is not defined.
- **Treating repeated measures as independent.** Use a block or mixed model analysis instead.

## Implementations

## History

Fisher developed the analysis of variance for crossed classifications in the agricultural experiments at Rothamsted in the 1920s, and described it in Statistical Methods for Research Workers (1925) and The Design of Experiments (1935). Yates (1934) treated tables with unequal numbers in the cells. He proposed the method of fitting constants, which corresponds to type II, and the method of weighted squares of means, which corresponds to type III. The names type I to type IV come from the SAS GLM procedure of the 1970s.

## References
