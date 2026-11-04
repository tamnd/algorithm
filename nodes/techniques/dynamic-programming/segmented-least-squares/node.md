---
tag: 3E1N9J
kind: problem
slug: segmented-least-squares
name: Segmented least squares
aliases:
- Segmented Least Squares Problem
area: techniques/dynamic-programming
level: core
summary: Fits a sequence of points with several line segments, trading off squared error against a penalty per segment, and is solved by dynamic programming.
prereqs: [ordinary-least-squares, optimal-substructure, prefix-sums]
see_also: [linear-regression, least-squares-problem, weighted-interval-scheduling, knuth-plass-line-breaking, ramer-douglas-peucker, histogram, traceback, dp-on-dag]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 6.3 (segmented least squares, multi-way choices)
  - paper: doi:10.1145/366573.366611
    title: Richard Bellman, On the approximation of curves by line segments using dynamic programming, Communications of the ACM 4(6), 1961
    locator: p. 284
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Chapter 6 (dynamic programming, subproblems on prefixes and shortest paths in a DAG)
---

Segmented least squares is the problem of fitting a sequence of points, sorted by $x$, with a chain of line segments, where each segment fits a contiguous run of points by [least squares](/ordinary-least-squares/). The objective adds the total squared error to a fixed penalty $C$ for each segment, so the number of segments is chosen by the algorithm and not given in advance. A dynamic program over prefixes solves it in $O(n^2)$ time after the errors of all runs are known, and the errors themselves take $O(n^2)$ time with prefix sums. Bellman used dynamic programming for this kind of curve fitting in 1961, and Kleinberg and Tardos use it to introduce DP with a multi-way choice.

## In plain words

You have measurements over time, and the data seems to follow straight lines that change slope now and then. You want to describe it with a few line pieces. Each piece covers a run of neighbouring points and is the best straight line for that run.

More pieces always fit the data better: with one piece for every two points, the fit is perfect. But that tells you nothing. So each piece costs a fixed fee, and you look for the plan with the least total of fees plus fitting error. A large fee gives a few long pieces; a small fee gives many short ones. The trick is to ask where the last piece begins. Whatever that answer is, the points before it must be split in the best possible way, and that is a smaller problem of the same kind.

## Definition

**Input.** Points $(x_1, y_1), \ldots, (x_n, y_n)$ with $x_1 < x_2 < \cdots < x_n$, and a penalty $C > 0$.

**Segments.** A *segmentation* is a partition of $\{1, \ldots, n\}$ into runs of consecutive indices $\{i, i+1, \ldots, j\}$. For a run, let
$$e_{i,j} = \min_{a, b \in \mathbb{R}} \sum_{t=i}^{j} (y_t - a x_t - b)^2$$
be the least squared error of a single line fitted to the points $i$ to $j$.

**Objective.** For a segmentation $S$ with $L$ runs, minimize
$$\mathrm{cost}(S) = L \cdot C + \sum_{\{i, \ldots, j\} \in S} e_{i,j}.$$

**Output.** The least cost and a segmentation that achieves it.

**The error of one run.** Let $m = j - i + 1$, and let $\bar x$ and $\bar y$ be the means of the run. Put $S_{xx} = \sum (x_t - \bar x)^2$, $S_{xy} = \sum (x_t - \bar x)(y_t - \bar y)$ and $S_{yy} = \sum (y_t - \bar y)^2$, all sums over the run. If $m = 1$ then $e_{i,j} = 0$. If $m \ge 2$ then $S_{xx} > 0$ because the $x_t$ are distinct, and
$$e_{i,j} = S_{yy} - \frac{S_{xy}^2}{S_{xx}}, \qquad a = \frac{S_{xy}}{S_{xx}}, \qquad b = \bar y - a \bar x .$$

*Proof.* For a fixed slope $a$, the error is a quadratic in $b$ with its minimum at $b = \bar y - a \bar x$. With this $b$, the error is $\sum \bigl((y_t - \bar y) - a (x_t - \bar x)\bigr)^2 = S_{yy} - 2a S_{xy} + a^2 S_{xx}$. This quadratic in $a$ has its minimum at $a = S_{xy}/S_{xx}$, with the value $S_{yy} - S_{xy}^2/S_{xx}$. ∎

**The recurrence.** Let $\mathrm{OPT}(j)$ be the least cost for the first $j$ points, with $\mathrm{OPT}(0) = 0$. Then for $j \ge 1$
$$\mathrm{OPT}(j) = \min_{1 \le i \le j} \bigl( e_{i,j} + C + \mathrm{OPT}(i - 1) \bigr).$$

*Proof.* In any segmentation of points 1 to $j$, the last run is $\{i, \ldots, j\}$ for some $i$, and the other runs form a segmentation of points 1 to $i - 1$. So the cost is $e_{i,j} + C$ plus the cost of that segmentation, which is at least $\mathrm{OPT}(i-1)$. This shows $\mathrm{OPT}(j) \ge$ the minimum. For each $i$, an optimal segmentation of points 1 to $i - 1$ followed by the run $\{i, \ldots, j\}$ is a segmentation of points 1 to $j$ with cost $e_{i,j} + C + \mathrm{OPT}(i-1)$. This shows $\mathrm{OPT}(j) \le$ the minimum. ∎

This is the step that Kleinberg and Tardos call a multi-way choice: the last segment can start at any of $j$ places, while in [weighted interval scheduling](/weighted-interval-scheduling/) the last decision has only two options. The segmentation is rebuilt by [traceback](/traceback/) of the $i$ that achieves each minimum.

## Variants

- **A fixed number of segments.** Use exactly $k$ segments and minimize the error. The table becomes $\mathrm{OPT}(\ell, j)$ for $\ell$ segments over the first $j$ points, and the time becomes $O(k n^2)$.
- **An error bound.** Minimize the number of segments subject to the error of each segment, or the total error, being at most a bound.
- **Connected pieces.** Require that consecutive segments meet, so the fit is a continuous piecewise linear function. The pieces are then no longer independent, and the problem needs a different formulation.
- **Other fits per run.** Replace the line by a constant, which gives the optimal histogram of the data, or by a polynomial of fixed degree, or replace squared error by absolute error. The recurrence is unchanged; only the cost $e_{i,j}$ changes.
- **Penalty per segment that varies.** Any cost of the form $f(i, j)$ for a run works with the same recurrence, as in [line breaking](/knuth-plass-line-breaking/) where the run is a line of text.

## Examples

Take the 12 points $(t, y_t)$ for $t = 1, \ldots, 12$ with
$y = (1, 2, 4, 5, 6, 6, 7, 6, 6, 4, 3, 1)$.
The data rises, levels out and falls. A single line fits it badly: $e_{1,12} = 13687/286 \approx 47.857$. Some errors of runs:

| run | $e_{i,j}$ | best line |
|---|---|---|
| 1 to 12 | $13687/286 \approx 47.857$ | $y = (15/286)\,x + 43/11$ |
| 1 to 7 | $12/7 \approx 1.714$ | $y = x + 3/7$ |
| 8 to 12 | $11/10 = 1.1$ | $y = -1.3\,x + 17$ |
| 1 to 4, 5 to 8, 9 to 12 | $0.2$, $0.7$, $0.2$ | |

The optimal segmentation for several penalties:

| $C$ | segments | runs | total cost |
|---|---|---|---|
| 0.1 | 6 | 1 to 2, 3 to 4, 5 to 6, 7 to 8, 9 to 10, 11 to 12 | 0.6 |
| 1 | 3 | 1 to 4, 5 to 8, 9 to 12 | 4.1 |
| 2 | 2 | 1 to 7, 8 to 12 | $197/70 + 4 \approx 6.814$ |
| 100 | 1 | 1 to 12 | $147.857$ |

With $C = 0.1$ every run of two points has error 0, so the cost is $6 \times 0.1$. With $C = 2$ the cost is $2C + e_{1,7} + e_{8,12} = 4 + 12/7 + 11/10$. Between two segments and one segment the switch happens where $2C + 197/70 = C + 13687/286$, at $C = 225437/5005 \approx 45.04$.

## Known algorithms

- **Errors by direct fitting, then DP.** Fit each of the $n(n+1)/2$ runs from scratch in $O(n)$ time: $O(n^3)$ for all errors. This is the analysis in Kleinberg and Tardos.
- **Errors with prefix sums, then DP.** Keep the [prefix sums](/prefix-sums/) of $x_t$, $y_t$, $x_t^2$, $x_t y_t$ and $y_t^2$. Each of $S_{xx}$, $S_{xy}$ and $S_{yy}$ for a run is a difference of prefix sums minus a correction, for example $S_{xx} = \sum x_t^2 - (\sum x_t)^2/m$. So each $e_{i,j}$ takes $O(1)$ time, and all errors take $O(n^2)$ time. The errors can also be computed inside the DP loop, so the space is $O(n)$ without the table of errors.
- **The DP.** For each $j$, the minimum over $i$ takes $O(j)$ time, so all values take $\sum_j O(j) = O(n^2)$ time. With the traceback the space is $O(n)$ plus the space for the errors.

The total is $O(n^2)$ time and $O(n)$ extra space with the prefix-sum method. The DP is a shortest path from vertex 0 to vertex $n$ in the [DAG](/dp-on-dag/) with an edge from $i - 1$ to $j$ of weight $e_{i,j} + C$ for each $i \le j$.

## Bounds

- **Upper bound.** $O(n^2)$ time on a real RAM, as above.
- **Lower bound.** $\Omega(n)$ to read the points. The DP above looks at all $\Theta(n^2)$ edges of the DAG; faster methods must exploit more structure of the errors.
- **The answer as a function of $C$.** For each $L$, let $E_L$ be the least total error with $L$ runs. Then $\mathrm{OPT} = \min_L (L C + E_L)$, a concave piecewise linear function of $C$. As $C$ grows the optimal number of segments does not increase: if $L_1$ is optimal at $C_1$ and $L_2$ at $C_2 > C_1$, adding the two optimality inequalities gives $(L_1 - L_2)(C_2 - C_1) \ge 0$.

## Reductions

- **To shortest path in a DAG.** As above: vertices $0, \ldots, n$, an edge $(i - 1, j)$ of weight $e_{i,j} + C$, and the answer is the [shortest path](/dag-shortest-paths/) from 0 to $n$. The edges go from smaller to larger vertices, so the natural order is a topological order.
- **Same shape as line breaking.** Splitting a paragraph into lines with a cost per line has the same recurrence over prefixes. See [Knuth-Plass line breaking](/knuth-plass-line-breaking/).

## Applications

- **Change detection.** A change in the slope of a time series, such as a growth rate, marks an event. The segments locate the changes, and $C$ controls how sensitive the detection is.
- **Curve simplification.** Replace a long sequence of samples by a few line pieces for storage or display. The [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) algorithm is a fast heuristic for a related geometric task; the DP gives the optimum for this objective.
- **Histograms and summaries.** With constant pieces, the same DP builds the histogram of least squared error with a penalty per bucket, used to summarize data for databases.

## References
