---
tag: GX5W9T
kind: algorithm
slug: stepwise-regression
name: Stepwise regression
aliases:
- forward selection
- backward elimination
area: statistics-and-inference/regression-and-diagnostics
level: intro
summary: "Chooses the columns of a regression by adding or dropping one column at a time while a criterion such as AIC improves. It is fast and greedy, and it can miss the best subset."
model: real-ram
complexity:
  vars: {n: the number of observations, m: the number of candidate columns, s: the number of steps taken}
  time: {worst: "Θ(n m^2 + s m^2)", best: "Θ(n m^2)"}
  space: {extra: "Θ(m^2)"}
  flops: {worst: "n m^2 + 2 s m^2 + O(n m + s m)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1960
  people: [M. A. Efroymson]
  note: Efroymson gave the stepwise method with partial F-tests to enter and to remove variables, computed by Gauss-Jordan pivots on the cross-product matrix, for the early electronic computers.
prereqs: [ordinary-least-squares, akaike-information-criterion, regression-f-test, greedy-algorithm]
see_also: [leaps-and-bounds, bayesian-information-criterion, feature-selection, lasso-regression, post-selection-inference, cross-validation, variance-inflation-factor, gaussian-elimination]
sources:
  - paper: "M. A. Efroymson, Multiple regression analysis, in A. Ralston and H. S. Wilf (eds.), Mathematical Methods for Digital Computers, Wiley, New York, 1960, pp. 191 to 203"
    locator: The whole chapter (the stepwise method with F-to-enter and F-to-remove, computed by pivots on the correlation matrix)
  - paper: doi:10.1080/00031305.1979.10482685
    title: "James H. Goodnight, A tutorial on the SWEEP operator, The American Statistician 33(3), 1979, pp. 149 to 158"
    locator: The whole paper (the sweep operator, its inverse and the regression statistics it leaves in the swept matrix)
  - paper: doi:10.2307/2529336
    title: "R. R. Hocking, The analysis and selection of variables in linear regression, Biometrics 32(1), 1976, pp. 1 to 49"
    locator: Sections on stepwise methods and their comparison with all-subsets methods
  - paper: doi:10.1093/biomet/54.3-4.357
    title: "E. M. L. Beale, M. G. Kendall and D. W. Mann, The discarding of variables in multivariate analysis, Biometrika 54(3/4), 1967, pp. 357 to 366"
    locator: The examples in which forward and backward stepwise methods miss the best subset
  - paper: doi:10.1080/00031305.1983.10482729
    title: "David A. Freedman, A note on screening regression equations, The American Statistician 37(2), 1983, pp. 152 to 155"
    locator: The whole paper (screening pure noise columns and refitting gives a significant overall F-test)
  - paper: doi:10.1080/01621459.2015.1108848
    title: "Ryan J. Tibshirani, Jonathan Taylor, Richard Lockhart and Robert Tibshirani, Exact post-selection inference for sequential regression procedures, Journal of the American Statistical Association 111(514), 2016, pp. 600 to 620"
    locator: The part on forward stepwise regression (its path and signs after a fixed number of steps as a polyhedral event in y)
  - book: isbn:9781584881711
    title: Alan Miller, Subset Selection in Regression, second edition, Chapman and Hall/CRC, 2002
    locator: Chapter 3 (forward selection, backward elimination, Efroymson's algorithm and their failures) and Chapter 6 (selection bias in the estimates)
  - book: isbn:9783319194240
    title: "Frank E. Harrell, Jr., Regression Modeling Strategies, second edition, Springer, 2015"
    locator: Section 4.3 (the problems of stepwise variable selection)
---

Stepwise regression chooses which of $m$ candidate columns to keep in a linear regression by local moves. Forward selection starts from the model with only the intercept and adds one column at a time. Backward elimination starts from all $m$ columns and drops one at a time. The bidirectional form allows both moves at each step. Each step takes the single move that most improves a criterion, either a penalized likelihood such as the [Akaike information criterion](/akaike-information-criterion/) or a partial F-test, and the method stops when no single move improves it. With the sweep operator each step costs $\Theta(m^2)$ after one pass over the data. The method is a [greedy algorithm](/greedy-algorithm/): it finds a subset that no single move can improve, which need not be the best subset, and the usual tests and intervals of the chosen model are not valid.

## In plain words

Many candidate predictors are available and only some help. Trying every combination is slow when there are many. Stepwise regression grows or shrinks the model one predictor at a time: at each step it looks at every predictor that could come in or go out, takes the one that helps most, and stops when no single change helps. This is quick and easy to explain. But two predictors that are only useful together can both be left out, because neither one looks useful alone. And because the method picked the predictors that looked best in this sample, the chosen model looks better than it is.

## The problem

**Input.** An $n \times m$ matrix $X$ of candidate columns, a response $y \in \mathbb R^n$, a direction (forward, backward or both) and a rule: a criterion $c(\mathrm{RSS}, |S|)$, or two levels $\alpha_{\text{enter}} \le \alpha_{\text{remove}}$ for partial F-tests.

**Model for a subset.** For $S \subseteq \{1, \dots, m\}$ the model is $y = b_0\mathbf 1 + X_Sb_S + \varepsilon$, with the coefficient vector written $b$. The intercept is always in, so the model has $p = |S| + 1$ columns, and $\mathrm{RSS}(S)$ is its least squares residual sum of squares. With normal errors and $\hat\sigma^2 = \mathrm{RSS}(S)/n$, the criteria are

$$\mathrm{AIC}(S) = n\log\frac{2\pi\,\mathrm{RSS}(S)}{n} + n + 2(|S| + 2), \qquad \mathrm{BIC}(S) = n\log\frac{2\pi\,\mathrm{RSS}(S)}{n} + n + (|S| + 2)\log n,$$

where $|S| + 2$ counts the slopes, the intercept and $\sigma^2$.

**Neighborhood.** The moves from $S$ are $S \cup \{j\}$ for $j \notin S$ (forward) and $S \setminus \{j\}$ for $j \in S$ (backward).

**Output.** A subset $S$ that no allowed move improves, its RSS and the path of moves. The best subset of each size is a different problem, solved exactly by [leaps and bounds](/leaps-and-bounds/).

## The algorithm

All fits come from one $(m + 1) \times (m + 1)$ matrix $A$: the centered cross-products of the columns of $X$ and of $y$, with $y$ as the last index. Centering takes care of the intercept. The **sweep** on index $k$ with pivot $d = a_{kk} \ne 0$ is

$$a_{kk} \leftarrow -\frac1d, \quad a_{ik} \leftarrow \frac{a_{ik}}{d}, \quad a_{kj} \leftarrow \frac{a_{kj}}{d}, \quad a_{ij} \leftarrow a_{ij} - \frac{a_{ik}a_{kj}}{d} \quad (i, j \ne k),$$

and the reverse sweep is the same with $a_{ik} \leftarrow -a_{ik}/d$ and $a_{kj} \leftarrow -a_{kj}/d$. It undoes the sweep. When $A$ has been swept on the indices of $S$, $a_{yy} = \mathrm{RSS}(S)$, and the RSS after the move that toggles column $j$ (adds it if $j \notin S$, drops it if $j \in S$) is $a_{yy} - a_{jy}^2/a_{jj}$, for every $j$ at once.

```pseudo id=main
STEPWISE(X[1..n, 1..m], y[1..n], direction, c)
L1  A ← centered cross-products of the columns (x_1, ..., x_m, y)      ▷ (m + 1) × (m + 1), one pass over the data
L2  S ← ∅ (forward, both) or {1, ..., m} (backward); sweep A on each j ∈ S
L3  loop
L4      best ← c(A[y,y], |S|);  j* ← none                              ▷ A[y,y] = RSS(S)
L5      for each column j whose move is allowed by direction
L6          if j ∉ S and A[j,j] ≈ 0 then skip j                       ▷ x_j lies in the span of S
L7          r ← A[y,y] - A[j,y]² / A[j,j]                              ▷ RSS after toggling j
L8          if c(r, |S| ± 1) < best then best ← c(r, |S| ± 1);  j* ← j
L9      if j* = none then return (S, A[y,y])
L10     if j* ∉ S then sweep A on j*;  S ← S ∪ {j*}
L11     else reverse sweep A on j*;  S ← S \ {j*}
```

**Partial F-tests.** Efroymson's original rule replaces lines L4 to L11 by two tests. Let $r_j$ be the value from line L7. For $j \notin S$ the F-to-enter is $F_j = (a_{yy} - r_j)/(r_j/(n - |S| - 2))$ on 1 and $n - |S| - 2$ degrees of freedom. Add the column with the largest $F_j$ if its p-value is below $\alpha_{\text{enter}}$. Then, for $j \in S$, the F-to-remove is $F_j = (r_j - a_{yy})/(a_{yy}/(n - |S| - 1))$ on 1 and $n - |S| - 1$ degrees of freedom. Drop the column with the smallest $F_j$ while its p-value is above $\alpha_{\text{remove}}$. Each F statistic is the square of the t statistic of the column in the larger of the two models, so this is the [regression F-test](/regression-f-test/) for one coefficient. With $\alpha_{\text{enter}} > \alpha_{\text{remove}}$ the two tests can undo each other and cycle, so the implementation keeps the set of visited subsets and stops at the first repeat.

## Example

Take $n = 10$ and three candidate columns:

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $x_1$ | 1 | -3 | 3 | -2 | 2 | -2 | 1 | 1 | -2 | 3 |
| $x_2$ | -1 | -1 | 3 | -4 | 0 | -4 | -1 | 2 | -4 | 3 |
| $x_3$ | -2 | -1 | -3 | 3 | 1 | -2 | -1 | -1 | -3 | -2 |
| $y$ | -1 | -3 | -1 | 4 | 3 | 0 | 2 | -2 | 0 | -1 |

The correlation of $x_1$ and $x_2$ is 0.833. The exact RSS values and the criteria of all eight subsets are:

| $S$ | RSS | AIC | BIC |
|---|---|---|---|
| $\emptyset$ | 449/10 = 44.900 | 47.397 | 48.002 |
| $\{1\}$ | 10237/228 = 44.899 | 49.397 | 50.305 |
| $\{2\}$ | 25148/681 = 36.928 | 47.443 | 48.350 |
| $\{3\}$ | 2354/103 = 22.854 | 42.644 | 43.552 |
| $\{1, 2\}$ | 184367/9524 = 19.358 | 42.984 | 44.194 |
| $\{1, 3\}$ | 7036/321 = 21.919 | 44.226 | 45.437 |
| $\{2, 3\}$ | 79043/3886 = 20.340 | 43.479 | 44.689 |
| $\{1, 2, 3\}$ | 1130812/271239 = 4.169 | 29.630 | 31.143 |

**Forward with AIC.** From $\emptyset$ (AIC 47.397), line L7 gives the three RSS values of the one-column models, and $x_3$ gives the smallest AIC, 42.644. From $\{3\}$ the moves to $\{1, 3\}$ and $\{2, 3\}$ give 44.226 and 43.479, both worse, so the method stops at $\{3\}$. The bidirectional method takes the same path, since dropping $x_3$ again is worse.

**Backward with AIC.** From $\{1, 2, 3\}$ (AIC 29.630) each drop gives 42.984 or more, so backward elimination stops at once with all three columns, which is the best subset by a margin of 13 units of AIC.

**Partial F-tests** with $\alpha_{\text{enter}} = 0.05$ and $\alpha_{\text{remove}} = 0.10$. At the first step the F-to-enter values on 1 and 8 degrees of freedom are 0.000, 1.727 and 7.717, with p-values 0.990, 0.225 and 0.024, so $x_3$ enters. At the second step, on 1 and 7 degrees of freedom, $x_1$ gives 0.299 ($p = 0.602$) and $x_2$ gives 0.865 ($p = 0.383$), so nothing enters and the method stops at $\{3\}$. In the full model the F-to-remove values on 1 and 6 degrees of freedom are 23.27, 25.55 and 21.86, with p-values between 0.002 and 0.004: all three columns are clearly needed.

The full fit is $\hat b_S = (1.076, -0.939, 0.730)$. The columns $x_1$ and $x_2$ act together: alone, $x_1$ removes nothing and $x_2$ little, but their difference predicts $y$ well. A one-move search from $\emptyset$ never sees the pair. Here backward elimination finds the best subset; with other data it fails in the same way that forward selection fails here (Beale, Kendall and Mann 1967).

**Measured selection bias.** With $n = 50$, $m = 10$ noise columns and a noise response, 2000 data sets from `random.Random(20261114)` gave a first-step F-to-enter with $p < 0.05$ in 39.1% of the data sets, against the nominal 5%. This is close to $1 - 0.95^{10} = 0.401$, the rate for 10 independent tests: the first step reports the best of 10 tests as if it were one.

## Correctness

The proof in this folder shows that after the sweeps on $S$ the matrix holds $-(\tilde X_S^\top\tilde X_S)^{-1}$, the coefficients $\hat b_S$ and $\mathrm{RSS}(S)$ in its blocks, where $\tilde X_S$ is the centered $X_S$, and that the sweeps on a set give the same result in any order. It then shows that $a_{yy} - a_{jy}^2/a_{jj}$ is the RSS after the toggle of $j$ for both adds and drops, so line L7 scores every neighbor exactly, and that the partial F statistics are the squared t statistics. With a criterion each move strictly lowers $c$, so no subset is visited twice, the loop ends after at most $2^m$ moves, and the result is a local minimum: no single allowed move lowers $c$. With F-tests the set of visited subsets ends the loop. Nothing more is proved. The result is not in general the best subset, and the example above is a counterexample.

## Complexity

Line L1 costs about $nm^2$ flops for the $(m + 1)(m + 2)/2$ distinct cross-products. Each step scores all $m$ moves in $O(m)$ and does one sweep in about $2m^2$ flops, so $s$ steps cost $\Theta(sm^2)$ after the pass over the data, and the space is $\Theta(m^2)$. Forward selection without drops takes at most $m$ steps, and backward elimination at most $m$, so they cost $\Theta(nm^2 + m^3)$. The bidirectional method has only the bound $s \le 2^m$ from the strict decrease. Refitting each candidate model by QR instead of sweeping would cost $\Theta(n|S|^2)$ per candidate and $\Theta(nm^4)$ for a forward path.

## Properties

- **Local, not global.** The result cannot be improved by one add or one drop. Forward, backward and bidirectional searches can end at different subsets, as in the example.
- **Unstable.** A small change of the data can change an early choice and so the whole path. The chosen subset varies a lot under resampling.
- **Biased estimates.** A column enters because its estimated effect was large in this sample, so its $\hat b_j$ is biased away from 0, and the residual variance of the chosen model is biased down.
- **Invalid tests.** The F and t tests of the chosen model ignore the search. Freedman (1983) screened 50 noise columns at $p < 0.25$, refitted, and got a significant overall F-test. The nominal levels $\alpha_{\text{enter}}$ and $\alpha_{\text{remove}}$ are not error rates of anything.
- **Exact arithmetic.** The sweep uses only field operations, so with rational data the path and the RSS values are exact, as in the table above.

## Variants and improvements

- **Penalized criteria.** AIC, its small-sample form AICc, [BIC](/bayesian-information-criterion/) and Mallows' $C_p$ change only the function $c$ of line L8. BIC stops earlier.
- **Best subset search.** [Leaps and bounds](/leaps-and-bounds/) uses the same sweeps inside a branch and bound search and finds the best subset of each size exactly, for $m$ up to about 30 to 40.
- **Forward stagewise and the lasso.** Taking many tiny steps toward the most correlated column instead of whole moves leads to least angle regression and the [lasso](/lasso-regression/) path, which shrink the coefficients and are more stable.
- **Selective inference.** Valid p-values and intervals after a forward path are given by the truncated normal laws of the [polyhedral lemma](/polyhedral-lemma/), since the event that forward selection with a fixed number of steps takes a given path with given signs is a polyhedron in $y$ (Tibshirani, Taylor, Lockhart and Tibshirani 2016). See [post-selection inference](/post-selection-inference/).
- **Feature selection in learning.** The same greedy search with cross-validated error as the criterion is the wrapper method of [feature selection](/feature-selection/).

## When to use it

Use stepwise regression for a quick screen of a moderate number of candidate columns when the purpose is a first look or a prediction checked on new data, and report it as a search, not as a test. For prediction, the lasso or [cross-validation](/cross-validation/) of the whole procedure is usually better. For inference about effects, prespecify the model from subject knowledge; if selection is unavoidable, use sample splitting or selective inference. When $m$ is at most about 30 to 40 and the best subset is wanted, use leaps and bounds instead.

## Pitfalls

- **Reporting the chosen model as if it were prespecified.** The p-values, intervals and $R^2$ of the final fit are too optimistic, as the measured 39% rate above shows for one step.
- **Correlated candidates.** A pair or group that works only together can be missed by forward selection, and the order of entry among correlated columns is close to arbitrary. Check the [variance inflation factors](/variance-inflation-factor/).
- **Collinear columns.** A column in the span of the current model has pivot $a_{jj} = 0$; dividing by a tiny rounded pivot gives nonsense. The implementation refuses such a column (line L6) with a relative tolerance.
- **Small samples.** The F-to-enter needs $n - |S| - 2 > 0$, and with few residual degrees of freedom the criteria favor too many columns; use AICc or stop earlier.
- **Categorical predictors.** A factor with several dummy columns should enter or leave as a group; moving single dummy columns makes the model depend on the coding.
- **Missing values.** Programs that drop rows with missing values per model compare criteria on different rows. Fix the rows before the search.

## Implementations

## History

Efroymson (1960) described stepwise regression with F-to-enter and F-to-remove for the computers of the time, and the method spread through the statistical program libraries of the 1960s and 1970s. Beale, Kendall and Mann (1967) and Hocking (1976) showed with examples that stepwise methods can miss the best subset and compared them with all-subsets methods. Goodnight (1979) wrote out the sweep operator that these programs use. Freedman (1983) showed that screening noise columns and refitting produces significant tests, and Miller's book (first edition 1990) made the bias of the estimates after selection a central topic.

## References
