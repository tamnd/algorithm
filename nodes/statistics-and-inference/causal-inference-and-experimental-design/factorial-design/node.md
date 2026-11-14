---
tag: NCP43N
kind: definition
slug: factorial-design
name: Factorial design
aliases:
- full factorial experiment
- 2^k factorial design
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: An experiment that runs every combination of the levels of several factors, so that main effects and all interactions can be estimated.
prereqs: [two-way-anova, randomized-experiment]
see_also: [fractional-factorial-design, plackett-burman-design, orthogonal-array, fast-walsh-hadamard-transform, walsh-hadamard-transform, kronecker-product, response-surface-methodology, optimal-experimental-design]
sources:
  - book: isbn:9780471718130
    title: George E. P. Box, J. Stuart Hunter and William G. Hunter, Statistics for Experimenters, second edition, Wiley, 2005
    locator: Chapter 5 (factorial designs at two levels), starting on p. 173; Section 5.16 (blocking the 2^k designs), starting on p. 211
  - book: "Frank Yates, The Design and Analysis of Factorial Experiments, Technical Communication No. 35, Imperial Bureau of Soil Science, Harpenden, 1937"
    title: The Design and Analysis of Factorial Experiments
    locator: the tabular method for the effects of a 2^n experiment (general locator, page not confirmed)
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: the chapters on factorial designs, the 2^k design and blocking in the 2^k design (chapter-level locator)
---

A factorial design runs every combination of the levels of several factors. With $k$ factors at two levels each it has $2^k$ runs and is called a $2^k$ design. Fisher and Yates used factorial designs at Rothamsted for two reasons. First, every run is used to estimate every effect, so a factorial experiment gets the precision of a one-factor-at-a-time experiment with fewer runs. Second, it estimates interactions, which tell whether the effect of one factor depends on the level of another. In a two-level design the contrast columns are orthogonal $\pm 1$ vectors, so the effects are estimated independently, and Yates's algorithm computes all $2^k$ of them in $k \cdot 2^k$ additions. That algorithm is the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/).

## Definition

Let factors $F_1, \dots, F_k$ have $s_1, \dots, s_k$ levels. A **full factorial design** runs each of the $s_1 s_2 \cdots s_k$ treatment combinations $m \ge 1$ times, in an order chosen at random as in a [randomized experiment](/randomized-experiment/). A [two-way ANOVA](/two-way-anova/) with equal cell counts is the analysis of a full factorial design with two factors.

**Two-level designs.** Code the low level of each factor as $-1$ and the high level as $+1$, and name the factors $A, B, C, \dots$. A run is named by the lower-case letters of its factors at the high level, and $(1)$ is the run with all factors low. In **standard order** the $N = 2^k$ runs are numbered $x = 0, \dots, N - 1$, and factor $i$ (with $A$ as $i = 0$) is high in run $x$ when bit $i$ of $x$ is 1. So the order is $(1), a, b, ab, c, ac, bc, abc, \dots$. Write $x_i \in \{-1, +1\}$ for the level of factor $i$ in run $x$, and $y_x$ for the response of run $x$ (the mean of its $m$ replicates).

For a set $S$ of factors, with bit mask $s$, the **contrast column** $x_S$ has the entry $\prod_{i \in S} x_i$ in run $x$, and $x_\emptyset = 1$. The **contrast** and the **effect** of $S$ are

$$c_S = \sum_x x_S(x)\, y_x, \qquad \hat E_S = \frac{c_S}{N/2} \quad (S \ne \emptyset),$$

and $c_\emptyset / N$ is the grand mean. In the order of the masks $s = 0, 1, 2, \dots$ the effects are $I, A, B, AB, C, AC, BC, ABC, \dots$. The main effect $\hat E_A$ is the mean response at high $A$ minus the mean response at low $A$. The two-factor interaction $\hat E_{AB}$ is half of the difference between the $A$ effect at high $B$ and the $A$ effect at low $B$. Higher interactions repeat this one level up.

**The model.** In the regression notation $y = Xb + e$ of [ordinary least squares](/ordinary-least-squares/), let $X$ have the $N$ columns $x_S$, so $n = N$ rows and $N$ columns including the intercept $x_\emptyset$. This is the saturated model: it fits every run mean exactly. The coefficient $b_S$ is half the effect $E_S$, because a factor moves two units from $-1$ to $+1$.

**Theorem 1 (orthogonality).** For all sets $S$ and $T$, $x_S^\top x_T = N$ if $S = T$ and $0$ otherwise. So $X^\top X = NI$ and the least squares estimates are $\hat b_S = c_S/N$. With $m$ replicates of each run and independent errors of variance $\sigma^2$, the effect estimates are uncorrelated and $\operatorname{Var}(\hat E_S) = 4\sigma^2/(mN)$. The sum of squares of effect $S$ is $SS_S = m c_S^2/N$, and

$$m \sum_x (y_x - \bar y)^2 = \sum_{S \ne \emptyset} SS_S .$$

*Proof.* Since $x_i^2 = 1$, $x_S(x)\,x_T(x) = x_{S \triangle T}(x)$, where $S \triangle T$ is the symmetric difference. Let $U$ be nonempty and pick $i \in U$. The map that changes the level of factor $i$ is a bijection on the runs, and it changes the sign of $x_U$, so $\sum_x x_U(x) = 0$. With $U = S \triangle T$ this gives $x_S^\top x_T = 0$ for $S \ne T$, and $x_S^\top x_S = \sum_x 1 = N$. Stack the $m$ replicates: the full model matrix has $X^\top X$ replaced by $mNI$ and $X^\top y$ by $m X^\top \bar y$, where $\bar y$ is the vector of run means. So $\hat b = X^\top \bar y / N$, that is $\hat b_S = c_S/N$, with covariance $\sigma^2 I/(mN)$, and $\hat E_S = 2\hat b_S$ has variance $4\sigma^2/(mN)$. Because $X$ is square and invertible, the fitted values are the run means, so the between-run sum of squares is $m(\lVert X\hat b\rVert^2 - N\bar y^2) = m\big(N \sum_S \hat b_S^2 - N \hat b_\emptyset^2\big) = \sum_{S \ne \emptyset} m c_S^2/N$. $\square$

Three consequences follow.

- Each $SS_S$ is the drop in the residual sum of squares when $x_S$ is added to any model that contains other columns $x_T$, because the columns are orthogonal. So the type I, II and III sums of squares of the [two-way ANOVA](/two-way-anova/) agree, and with $m \ge 2$ each effect has the [regression F-test](/regression-f-test/) $F = SS_S/\text{MSE}$ on $(1, N(m - 1))$ degrees of freedom.
- Every effect uses all $N$ runs. With $k = 3$ and $m = 1$, $\operatorname{Var}(\hat E_A) = \sigma^2/2$ from 8 runs. A one-factor-at-a-time experiment that runs $(1), a, b, c$ each $r$ times estimates $A$ by the mean of $a$ minus the mean of $(1)$, with variance $2\sigma^2/r$. It needs $r = 4$, so 16 runs, for the same precision, and it estimates no interaction.
- $X$ is the Sylvester-Hadamard matrix with some columns negated (Theorem 2), so its columns are the codewords of the [Hadamard code](/hadamard-code/) in $\pm 1$ form, and $X$ is a [Walsh-Hadamard transform](/walsh-hadamard-transform/) matrix.

**Theorem 2 (Yates's algorithm is the fast Walsh-Hadamard transform).** The algorithm below returns the contrasts $c_S$ in the order of the masks $s$. In matrix form $c = D H_N y$, where $H_N = H_2^{\otimes k}$ is the Sylvester-Hadamard matrix, a [Kronecker product](/kronecker-product/) power with $(H_N)_{sx} = (-1)^{\operatorname{popcount}(s \wedge x)}$, and $D = \operatorname{diag}\big((-1)^{|s|}\big)$. It does $k \cdot N$ additions and subtractions, against $N^2 = 4^k$ for the direct sums.

```pseudo id=main
YATES(y[0..N-1])   ▷ N = 2^k, runs in standard order
L1  col ← y
L2  repeat k times:
L3      sums  ← (col[2i] + col[2i+1]   for i = 0, ..., N/2 - 1)
L4      diffs ← (col[2i+1] - col[2i]   for i = 0, ..., N/2 - 1)
L5      col ← sums followed by diffs
L6  return col      ▷ col[s] = c_S; effect = col[s]/(N/2), mean = col[0]/N
```

*Proof.* First the matrix form. If $\beta_i$ is bit $i$ of $x$, then $x_i = 2\beta_i - 1 = -(-1)^{\beta_i}$, so $x_S(x) = (-1)^{|S|} (-1)^{\operatorname{popcount}(s \wedge x)}$ and $c = DH_N y$.

Now the passes. A pass reads positions $2i$ and $2i + 1$ and writes position $i$ (the sum) and position $i + N/2$ (the difference). In bits, it removes the lowest bit $\beta$ of the position, moves the other bits down by one, and puts a new top bit $t$. The value written is $\sum_{\beta \in \{0, 1\}} (2\beta - 1)^t\, \text{col}[2i + \beta]$: for $t = 0$ the sum, for $t = 1$ the second minus the first. Claim: after $p$ passes, the entry at the position whose bits, from low to high, are $(\beta_p, \dots, \beta_{k-1}, t_0, \dots, t_{p-1})$ equals

$$\sum_{\beta_0, \dots, \beta_{p-1} \in \{0, 1\}} \ \prod_{j < p} (2\beta_j - 1)^{t_j}\; y_{(\beta_0, \dots, \beta_{k-1})}.$$

For $p = 0$ this is $y$ itself. Pass $p + 1$ removes the lowest bit $\beta_p$, sums over it with the weight $(2\beta_p - 1)^{t_p}$, and puts $t_p$ on top, which is the claim for $p + 1$. After $k$ passes the position is $s = (t_0, \dots, t_{k-1})$ and the entry is $\sum_x \prod_{j \in S} x_j\, y_x = c_S$. Each pass does $N/2$ additions and $N/2$ subtractions. $\square$

Each pass is one sparse factor of $H_2^{\otimes k}$ followed by a perfect shuffle, with the same read and write pattern in every pass. The in-place form on the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) page uses butterflies at distances $1, 2, 4, \dots$ instead. Since $D^2 = I$ and $H_N^2 = NI$, the data come back as $y = H_N D c/N$, so setting small contrasts to zero before this inverse gives fitted values. On integer data all the arithmetic is exact. The test file checks Theorem 2 against the direct sums for $k \le 8$ in exact arithmetic, and checks $c = DH_N y$ for $k \le 6$.

**Without replication.** With $m = 1$ the model is saturated and no degrees of freedom are left for error. The usual answers are to replicate, to pool high-order interactions that are assumed zero, or to plot the effects on normal probability paper, where pure noise lies on a line (Daniel, 1959; cited, not proved here).

**Blocking.** When a block holds only half of the runs, the experimenter confounds a high-order interaction with the blocks: in a $2^3$ design, the runs with $x_{ABC} = -1$ go in one block and the runs with $x_{ABC} = +1$ in the other. Then $ABC$ cannot be estimated, but by Theorem 1 every other column is orthogonal to the block column, so the other effects are unchanged. To run only one of the blocks is to run a [fractional factorial design](/fractional-factorial-design/).

## Examples and non-examples

**Example: a $2^3$ pilot plant experiment.** This is the pilot plant example of Box, Hunter and Hunter, Chapter 5, with temperature ($A$), concentration ($B$) and catalyst ($C$). The yields in standard order are $60, 72, 54, 68, 52, 83, 45, 80$, and Yates's algorithm gives:

| run | $y$ | pass 1 | pass 2 | pass 3 | effect | estimate | $SS$ |
|---|---|---|---|---|---|---|---|
| (1) | 60 | 132 | 254 | 514 | I | 64.25 (mean) | |
| a | 72 | 122 | 260 | 92 | A | 23 | 1058 |
| b | 54 | 135 | 26 | -20 | B | -5 | 50 |
| ab | 68 | 125 | 66 | 6 | AB | 1.5 | 4.5 |
| c | 52 | 12 | -10 | 6 | C | 1.5 | 4.5 |
| ac | 83 | 14 | -10 | 40 | AC | 10 | 200 |
| bc | 45 | 31 | 2 | 0 | BC | 0 | 0 |
| abc | 80 | 35 | 4 | 2 | ABC | 0.5 | 0.5 |

The sums of squares add to $1317.5$, the total sum of squares about the mean, as Theorem 1 says. The large effects are $A$, $AC$ and $B$. The temperature effect is $13$ with catalyst low and $33$ with catalyst high, and the interaction is $AC = (33 - 13)/2 = 10$. So the main effect of the catalyst, $1.5$, does not mean that the catalyst has no effect: it changes the effect of temperature. With one replicate there is no error estimate, so the decision about which effects are real needs replicates or a probability plot. The test file checks every number in the table.

**Example: the model matrix of a $2^2$ design.** In standard order the columns $I, A, B, AB$ are

$$X = \begin{pmatrix} 1 & -1 & -1 & 1 \\ 1 & 1 & -1 & -1 \\ 1 & -1 & 1 & -1 \\ 1 & 1 & 1 & 1 \end{pmatrix} = H_4 D, \qquad X^\top X = 4I,$$

with $D = \operatorname{diag}(1, -1, -1, 1)$. A balanced two-way ANOVA of two factors at two levels with $m$ observations per cell is this design, and its sums of squares are $m c_S^2/4$.

**Example: the design as a code and as an array.** The $2^k$ runs, written as 0/1 vectors, are all of $\{0, 1\}^k$, so the design is an [orthogonal array](/orthogonal-array/) of strength $k$: every set of columns contains every combination of levels equally often. A fractional design keeps only part of this strength.

**Non-example: one factor at a time.** Start at $(1)$ and change $A$ alone: the estimate is $a - (1) = 72 - 60 = 12$. In the pilot plant the temperature effect is $13$ at low catalyst and $33$ at high catalyst, so the experiment that holds $C$ low never sees the larger effect. It also needs twice the runs for the same precision (Theorem 1).

**Non-example: a lost run.** If run $abc$ is lost, the 7 remaining runs do not form a factorial design. Every column is $+1$ at $abc$, so every pair of distinct columns now has inner product $0 - 1 = -1$. The estimates are correlated, the sum of squares of an effect depends on the other terms in the model, and the analysis needs the type I, II and III choices of the unbalanced [two-way ANOVA](/two-way-anova/).

## Related definitions

- [Two-way ANOVA](/two-way-anova/): the analysis of a two-factor factorial; balance gives orthogonal sums of squares.
- [Fractional factorial design](/fractional-factorial-design/): runs a $2^{-p}$ fraction of a $2^k$ design and aliases effects in a known pattern.
- [Plackett-Burman design](/plackett-burman-design/): two-level main-effect designs whose run size is a multiple of 4, built from Hadamard matrices.
- [Orthogonal array](/orthogonal-array/): the general frame; a full $2^k$ design is an orthogonal array of strength $k$.
- [Walsh-Hadamard transform](/walsh-hadamard-transform/) and [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/): the contrasts are a Walsh-Hadamard transform, and Yates's algorithm is a fast one.
- [Response surface methodology](/response-surface-methodology/): starts with a two-level factorial, often with center points, to fit a first-order model and find the direction of improvement.
- [Optimal experimental design](/optimal-experimental-design/): for the first-order model with columns $I, A, \dots$ on the cube $[-1, 1]^k$, a two-level design of $N$ runs whose model matrix has $X^\top X = NI$, such as the $2^k$ design, is D-optimal among designs of $N$ runs. Each diagonal entry of $X^\top X$ is at most $N$, and Hadamard's inequality bounds the [determinant](/determinant/) of $X^\top X$ by the product of its diagonal entries.

## References
