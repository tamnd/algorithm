---
tag: DQP8F6
kind: algorithm
slug: least-trimmed-squares
name: Least trimmed squares
aliases:
- LTS regression
- FAST-LTS
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Regression that minimizes the sum of the h smallest squared residuals. FAST-LTS finds it by random starts and concentration steps that never increase the objective.
model: real-ram
complexity:
  vars: {n: the number of rows, p: the number of coefficients, S: the number of random starts, c: the number of C-steps for each start}
  time: {worst: O(S c (n p^2 + p^3 + n log n))}
  space: {extra: O(n p + p^2)}
properties: {deterministic: false, randomized: true, exact: false, regression_equivariant: true, in_place: false, online: false}
history:
  year: 1984
  people: [Peter J. Rousseeuw, Katrien Van Driessen, Annick M. Leroy, Jan Ámos Víšek]
  note: Rousseeuw proposed least trimmed squares in 1984 together with least median of squares. FAST-LTS by Rousseeuw and Van Driessen, with the concentration step, made it practical for large data.
prereqs: [ordinary-least-squares, least-median-of-squares, breakdown-point, normal-equations]
see_also: [minimum-covariance-determinant, mm-estimator, trimmed-mean, ransac, repeated-median-regression, trimmed-icp, iteratively-reweighted-least-squares, robust-model-fitting]
sources:
  - paper: doi:10.1080/01621459.1984.10477105
    title: Peter J. Rousseeuw, Least median of squares regression, Journal of the American Statistical Association 79(388), 1984
    locator: pp. 871 to 880 (least trimmed squares is proposed there next to LMS)
  - book: isbn:9780471852339
    title: Peter J. Rousseeuw and Annick M. Leroy, Robust Regression and Outlier Detection, Wiley, 1987
    locator: Chapter 3 (the breakdown point of LTS for the coverage h, and its asymptotic efficiency) and Chapter 4 (properties of LTS)
  - paper: doi:10.1007/s10618-005-0024-4
    title: Peter J. Rousseeuw and Katrien Van Driessen, Computing LTS regression for large data sets, Data Mining and Knowledge Discovery 12(1), 2006
    locator: pp. 29 to 45 (the C-step theorem, the FAST-LTS algorithm with random p-subsets, selective iteration and nested extensions)
  - paper: "Jan Ámos Víšek, The least trimmed squares. Part III: Asymptotic normality, Kybernetika 42(2), 2006, pp. 203 to 224"
    locator: The whole paper (root-n consistency and asymptotic normality of LTS)
---

Least trimmed squares (LTS) fits a regression by least squares on the best part of the data. For a coverage $h$, usually a little more than $n/2$, it chooses the coefficients that make the sum of the $h$ smallest squared residuals as small as possible. The other $n - h$ points, the worst fitted ones, do not count at all. So LTS has a [breakdown point](/breakdown-point/) near 1/2, like [least median of squares](/least-median-of-squares/), but it converges at the usual rate $n^{-1/2}$. The exact fit needs a search over subsets. FAST-LTS finds a good one by random starts and concentration steps (C-steps): each C-step refits least squares on the $h$ best fitted points, and it never makes the objective larger.

## In plain words

Pick a line, any line. Look at the points closest to it, just over half of them, and fit ordinary least squares to those points only. The new line fits those points at least as well as the old one, so the total squared error of its closest half can only go down. Repeat until the chosen points stop changing.

This walk downhill can stop at the wrong place: if it starts on a line through bad points, it may settle on a fit of the bad points. So we start many times, from lines through a few random points, and keep the best result. If more than half of the points are good, some starts will use only good points, and those lead to a good fit.

## The problem

The input is a design $X$ with rows $x_1, \ldots, x_n \in \mathbb{R}^p$ and responses $y$, in the notation $y = X b + e$, and a coverage $h$ with $n/2 < h \le n$. For coefficients $b$, let $r_i(b) = y_i - x_i^\top b$, and let $r^2_{(1)}(b) \le \cdots \le r^2_{(n)}(b)$ be the squared residuals in order. The LTS fit minimizes
$$Q(b) = \sum_{k=1}^{h} r^2_{(k)}(b).$$
The usual choice is $h = \lfloor (n + p + 1)/2 \rfloor$, which gives the highest breakdown point. A larger $h$, such as $0.75 n$, gives more efficiency and a lower breakdown point. With $h = n$, LTS is [ordinary least squares](/ordinary-least-squares/).

## The algorithm

Equivalently, LTS looks for the subset $H$ of $h$ rows whose least squares fit has the smallest residual sum of squares. FAST-LTS searches this space with C-steps. This is the core of the method; the full FAST-LTS adds the refinements listed under the variants.

```pseudo id=main
FAST-LTS(X, y, h, S)
L1  for each of S random starts do
L2      b ← the exact fit through p random rows      ▷ draw again if they are singular
L3      repeat
L4          b' ← C-STEP(b)
L5          if Q(b') ≥ Q(b) then leave the repeat loop;  b ← b'
L6      if Q(b) is the smallest so far then b* ← b
L7  return b* and Q(b*)

C-STEP(b)                                  ▷ concentration step
L8  H ← the h rows with the smallest r_i(b)²
L9  return the least squares fit on the rows of H
```

The C-step works because of one chain of inequalities. Let $H$ be the $h$ rows best fitted by $b$, and $b'$ the least squares fit on $H$. The $h$ smallest squared residuals of $b'$ sum to at most its sum over $H$; that is at most the sum of $b$ over $H$, because $b'$ is the least squares fit there; and that is $Q(b)$:
$$Q(b') \le \mathrm{RSS}_H(b') \le \mathrm{RSS}_H(b) = Q(b).$$

## Example

Ten points; the first seven lie near the line $y = 1 + 2x$, and the last three are bad.

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $x_i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| $y_i$ | 3 | 5 | 8 | 9 | 11 | 14 | 15 | 2 | 1 | 0 |

Here $p = 2$ (intercept and slope) and $h = \lfloor 13/2 \rfloor = 6$. Least squares on all ten points gives $y = 8.93 - 0.388\,x$, with the wrong sign of the slope. The exact LTS fit, found by trying all $\binom{10}{6} = 210$ subsets, uses the points $\{1, 2, 4, 5, 6, 7\}$:
$$y = \tfrac{142}{161} + \tfrac{333}{161} x \approx 0.882 + 2.068\,x, \qquad Q = \tfrac{114}{161} \approx 0.708.$$

C-steps from three starts give:

| start (line L2) | $Q$ at start | subset of the C-step | fit after it | $Q$ after it | next C-step |
|---|---|---|---|---|---|
| points 1, 2: $y = 1 + 2x$ | 1 | {1, 2, 3, 4, 5, 7} | $1.271 + 1.971x$ | 57/70 ≈ 0.814 | no change |
| points 8, 9: $y = 10 - x$ | 19 | {2, 3, 4, 8, 9, 10} | $9.856 - 0.948x$ | 1625/87 ≈ 18.68 | no change |
| points 2, 9: $y = 6.14 - 0.571x$ | 19.73 | {1, 2, 3, 8, 9, 10} | $6.183 - 0.548x$ | 1816/93 ≈ 19.53 | no change |

The objective drops at every step, as the C-step theorem says, but each run stops at a fixed point. The first start reaches a good fit with $Q = 0.814$, close to the best value 0.708 but not equal to it: the line $1 + 2x$ fits points 3 and 6 equally badly, and the tie is broken toward point 3. The other two starts stop at fits of the bad points. On these data none of the 45 starts from a pair of points reaches the global minimum; the test file checks this. FAST-LTS with 50 starts returns $Q = 57/70$, a good fit but an upper bound on the minimum. In the test file, on 30 random data sets with $n$ from 6 to 12 and a third of the points bad, 20 starts reached the exact minimum every time. These are measurements on small data, not a guarantee.

## Correctness

For any $b$, the sum of the $h$ smallest squared residuals is the least residual sum over sets of $h$ rows. So the minimum of $Q$ is the minimum over $h$-subsets of the least squares residual sum on the subset, and the exact LTS fit is least squares on the best subset. The C-step never increases $Q$, by the chain above, and while it decreases $Q$ strictly it cannot use the same subset twice, so each run stops after at most $\binom nh$ steps, and in practice after a few. The global minimizer is a fixed point of the C-step, but other fixed points exist, so FAST-LTS returns an upper bound on the minimum, which is exact when a start falls in the basin of the global minimum. The full proofs are below.

## Complexity

- **One C-step** costs $O(np)$ for the residuals, $O(n)$ expected for selecting the $h$ smallest (or $O(n \log n)$ by sorting), and $O(np^2 + p^3)$ for least squares. Usually $c$, the number of steps until a fixed point, is small.
- **FAST-LTS** with $S$ starts takes $O(S c (np^2 + p^3 + n \log n))$ time and $O(np + p^2)$ extra space. Rousseeuw and Van Driessen use $S = 500$ starts, two C-steps for each, and full iteration only for the 10 best.
- **Exact LTS** by enumeration of $h$-subsets takes $\binom nh$ least squares fits, practical only for $n$ up to about 20. Exact methods with branch and bound reach a little further. No exact algorithm is known whose time is polynomial in both $n$ and $p$.
- **How many starts.** A start uses only good rows with probability $(1 - \varepsilon)^p$ when a fraction $\varepsilon$ is bad, so about $\log \alpha / \log(1 - (1 - \varepsilon)^p)$ starts give a clean one with probability $1 - \alpha$; see the [RANSAC iteration bound](/ransac-iteration-bound/). A clean start usually, but not always, leads to the global minimum, as the example shows.

## Properties

- **Breakdown point.** For data in general position, $(n - h + 1)/n$, which is $(\lfloor (n - p)/2 \rfloor + 1)/n$ for $h = \lfloor (n + p + 1)/2 \rfloor$, the highest possible for a regression equivariant estimator (Rousseeuw and Leroy 1987). This is cited, not proved here.
- **Root-n rate.** LTS is $\sqrt n$-consistent and asymptotically normal under regularity conditions (Víšek 2006). Its efficiency at the normal model is low for $h \approx n/2$, about 7 percent (Rousseeuw and Leroy 1987), and grows with $h$. This is cited, not proved here.
- **Exact fit.** If at least $h$ points lie exactly on one hyperplane, $Q = 0$ there, and that hyperplane is an LTS fit. The test file checks this with 6 of 10 points on a line.
- **Equivariance.** Regression, scale and affine equivariant, like least squares.
- **Monotone search.** Every C-step gives a fit at least as good as before. This makes FAST-LTS simple to check and to stop.

## Variants and improvements

- **Full FAST-LTS.** Rousseeuw and Van Driessen (2006) add three refinements: two C-steps only from each start, then full iteration from the 10 best (selective iteration); for large $n$, a run on disjoint subsamples of about 300 rows and then on their union (nested extensions); and an intercept adjustment for each candidate.
- **Reweighted LTS.** After LTS, estimate a robust scale from the $h$ residuals, give weight 0 to points with a standardized residual above about 2.5, and fit least squares to the rest. This raises the efficiency and keeps the breakdown point.
- **The same idea for covariance.** FAST-MCD uses the same C-step for the [minimum covariance determinant](/minimum-covariance-determinant/): refit the mean and covariance on the $h$ points with the smallest Mahalanobis distances. The determinant never increases.
- **Trimmed problems elsewhere.** The [trimmed mean](/trimmed-mean/) is LTS for location, where the exact solution is a window of $h$ consecutive order statistics. [Trimmed ICP](/trimmed-icp/) uses the same trimming for point cloud alignment.
- **MM-estimators.** LTS is a common starting fit for an [MM-estimator](/mm-estimator/), which then reaches high efficiency.

## When to use it

Use LTS when you need a regression that resists up to almost half bad rows, including bad leverage points, in more than one predictor. It is the standard high breakdown fit in robust statistics software, and it is the basis of robust outlier diagnostics: plot the standardized LTS residuals against robust distances of the rows. Prefer it to LMS, which converges more slowly. If the fraction of bad rows is small and leverage is not a concern, an M-estimator or [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) is cheaper.

## Pitfalls

- **Treating the FAST-LTS result as exact.** It is the best fixed point found, an upper bound on the minimum. The example shows a clean start that misses the global minimum. Use more starts when the answer matters, and check whether different seeds agree.
- **Coverage h too small or too large.** With $h$ near $n/2$ the efficiency is low; with $h$ near $n$ the breakdown point is low. $h = 0.75n$ is a common compromise.
- **Singular subsets.** With categorical or discrete predictors, many $p$-subsets are singular. Draw again, or add rows until the subset has full rank.
- **Ties in residuals.** When two rows have equal residuals at the $h$-th place, the choice changes the next fit. Results can depend on the tie rule.
- **Inference.** Standard errors from least squares on the chosen subset ignore the selection; use the reweighted fit or the bootstrap.

## Implementations

## History

Rousseeuw proposed least trimmed squares in his 1984 paper on least median of squares, and the book of Rousseeuw and Leroy (1987) studied both. LMS was used more at first, because it was easier to approximate. That changed when Rousseeuw and Van Driessen found the C-step theorem: first for the minimum covariance determinant (FAST-MCD, 1999), then for regression in FAST-LTS, published in 2006. Víšek proved the asymptotic normality of LTS in a series of papers that ended in 2006.

## References
