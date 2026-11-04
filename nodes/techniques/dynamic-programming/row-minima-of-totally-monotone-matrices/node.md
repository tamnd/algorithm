---
tag: 84YFJJ
kind: problem
slug: row-minima-of-totally-monotone-matrices
name: Row minima of totally monotone matrices
aliases:
- row minima of Monge arrays
- matrix searching
area: techniques/dynamic-programming
level: research
summary: Find the minimum entry of every row of a totally monotone matrix, which need not be fully read.
prereqs: [monge-property]
see_also: [smawk-algorithm, monge-property, divide-and-conquer-optimization, knuth-optimization, optimal-text-wrapping, convex-hull-trick]
sources:
  - paper: doi:10.1007/BF01840359
    title: Alok Aggarwal, Maria M. Klawe, Shlomo Moran, Peter Shor and Robert Wilber, Geometric applications of a matrix-searching algorithm, Algorithmica 2, 195-208, 1987
    locator: the definitions of monotone and totally monotone matrices, the linear-time algorithm, and the geometric applications
  - paper: doi:10.1016/0166-218X(95)00103-X
    title: Rainer E. Burkard, Bettina Klinz and Rüdiger Rudolf, Perspectives of Monge properties in optimization, Discrete Applied Mathematics 70(2), 95-161, 1996
    locator: the sections on Monge arrays and row minima
  - paper: doi:10.1016/0196-6774(88)90032-6
    title: Robert Wilber, The concave least-weight subsequence problem revisited, Journal of Algorithms 9(3), 418-425, 1988
    locator: the online use of matrix searching for the concave least weight subsequence problem
  - paper: doi:10.1016/0020-0190(90)90215-J
    title: Zvi Galil and Kunsoo Park, A linear-time algorithm for concave one-dimensional dynamic programming, Information Processing Letters 33(6), 309-311, 1990
    locator: the whole paper
  - paper: doi:10.1137/0403009
    title: Maria M. Klawe and Daniel J. Kleitman, An almost linear time algorithm for generalized matrix searching, SIAM Journal on Discrete Mathematics 3(1), 81-97, 1990
    locator: the row minima of partial (staircase) totally monotone matrices
  - paper: doi:10.1137/0216043
    title: Daniel S. Hirschberg and Lawrence L. Larmore, The least weight subsequence problem, SIAM Journal on Computing 16(4), 628-638, 1987
    locator: the definition of the problem and the O(n log n) algorithm for concave weights
  - paper: doi:10.1109/SFCS.1988.21965
    title: David Eppstein, Zvi Galil and Raffaele Giancarlo, Speeding up dynamic programming, 29th FOCS, 488-496, 1988
    locator: sequence comparison with convex and concave gap costs
---

The row minima problem asks for the position of the minimum of every row of a matrix whose entries are computed on demand. For a general $n \times m$ matrix this needs all $nm$ entries. For a totally monotone matrix, which includes every [Monge matrix](/monge-property/), the [SMAWK algorithm](/smawk-algorithm/) solves it with $O(n + m)$ evaluations, and this is optimal. The problem is the inner step of many fast [dynamic programs](/divide-and-conquer-optimization/) and of algorithms on convex polygons.

## In plain words

You have a big table of numbers. You do not store it: you can ask for any one cell, and each question costs time. You want the smallest number in each row.

In a general table, the smallest number of a row can hide in any cell, so you must ask about every cell. But many tables from real problems have an order. The place of the smallest number moves only to the right as you go down. A stronger form of this order holds for every pair of rows and every pair of columns. With that order, one question can rule out a whole column for many rows at once. Then a small number of questions, about the number of rows plus the number of columns, is enough.

## Definition

Let $A$ be an $n \times m$ matrix, with $n, m \ge 1$, with entries in a totally ordered set. For row $i$, let $j(i)$ be the leftmost column of a minimum entry of row $i$:

$$j(i) = \min \{\, j : A[i][j] = \min_{1 \le k \le m} A[i][k] \,\}.$$

- $A$ is **monotone** when $j(1) \le j(2) \le \cdots \le j(n)$.
- $A$ is **totally monotone** when each $2 \times 2$ submatrix is monotone. An equivalent form: for all $i < i'$ and $j < j'$, $A[i][j] > A[i][j'] \implies A[i'][j] > A[i'][j']$.

The two forms are equivalent because a $2 \times 2$ matrix with rows $(a, b)$ and $(c, d)$ fails to be monotone exactly when its first row has its leftmost minimum on the right, $b < a$, and its second row on the left, $c \le d$.

Each totally monotone matrix is monotone. Take rows $i < i'$ with $j' = j(i') < j = j(i)$. Then $A[i][j'] > A[i][j]$ since $j$ is the leftmost minimum of row $i$, and the condition gives $A[i'][j'] > A[i'][j]$, so $j'$ is not a minimum of row $i'$. Each submatrix of a totally monotone matrix is totally monotone. A matrix with the [Monge property](/monge-property/), $A[i][j] + A[i'][j'] \le A[i][j'] + A[i'][j]$, is totally monotone: if $A[i][j] > A[i][j']$, then $A[i'][j] \ge A[i][j] - A[i][j'] + A[i'][j'] > A[i'][j']$.

**Problem.** Given $n$, $m$ and an oracle that returns $A[i][j]$ in $O(1)$ time, where $A$ is totally monotone, output $j(1), \ldots, j(n)$. The cost is the number of oracle calls plus the other work, in the [word RAM](/word-ram/) model.

## Variants

- **Monotone matrices.** Only the monotone condition holds, not the condition on each $2 \times 2$ submatrix. The answer is still well defined, but fewer columns can be ruled out at once.
- **Row maxima.** The maxima of $A$ are the minima of $-A$. The conditions apply to $-A$.
- **Rightmost minima.** For a Monge matrix, reverse both the rows and the columns. The result is again Monge, and its leftmost minima are the rightmost minima of $A$.
- **Online, or dynamic programming, version.** Find $E[j] = \min_{0 \le i < j} \bigl( D[i] + w(i, j) \bigr)$ for $j = 1, \ldots, n$, where $D[i]$ is computed from $E[i]$. The matrix $A[j][i] = D[i] + w(i, j)$ for $i < j$ is known only one row at a time. This is the least weight subsequence problem of [optimal text wrapping](/optimal-text-wrapping/).
- **Partial matrices.** Some entries are undefined, for example $A[j][i]$ with $i \ge j$ in the online version, so the defined part has a staircase shape.

## Examples

**A Monge matrix.** Let $x = (1, 3, 6, 8)$ be points on a line and $y = (0, 2, 4, 5, 9)$ be sites, both sorted, and let $A[i][j] = |x_i - y_j|$. The row minimum is the nearest site.

| | $y = 0$ | $y = 2$ | $y = 4$ | $y = 5$ | $y = 9$ | $j(i)$ |
|---|---|---|---|---|---|---|
| $x = 1$ | **1** | 1 | 3 | 4 | 8 | 0 |
| $x = 3$ | 3 | **1** | 1 | 2 | 6 | 1 |
| $x = 6$ | 6 | 4 | 2 | **1** | 3 | 3 |
| $x = 8$ | 8 | 6 | 4 | 3 | **1** | 4 |

The columns are numbered from 0. The first two rows have ties, and the leftmost minima are $(0, 1, 3, 4)$. The matrix is Monge because $|t|$ is a convex function and both lists are sorted. See the [Monge property](/monge-property/) for the proof of this rule.

**A monotone matrix that is not totally monotone.** The rows $(0, 3, 3)$, $(1, 4, 1)$ and $(4, 2, 3)$ have leftmost minima in columns 0, 0 and 1, so the matrix is monotone. But rows 1 and 2 with columns 1 and 2 form the submatrix with rows $(4, 1)$ and $(2, 3)$, whose leftmost minima are columns 2 and 1, so it is not totally monotone. On this matrix, the column elimination step of SMAWK removes column 1 and gives a wrong answer for the last row.

**A matrix that is not monotone.** The rows $(1, 0)$ and $(0, 1)$ have minima in columns 1 and 0. No method that relies on monotone minima applies.

## Known algorithms

| algorithm | condition | evaluations and time |
|---|---|---|
| scan each row | none | $nm$ |
| divide and conquer on the middle row | monotone | $O(m \log n + n)$ |
| [SMAWK](/smawk-algorithm/) | totally monotone | $O(n + m)$ |
| Wilber; Galil and Park; Larmore and Schieber | online version, concave cost | $O(n)$ |
| Klawe and Kleitman | partial (staircase) totally monotone | almost linear, within an inverse Ackermann factor |

**Divide and conquer.** Scan the middle row and find its leftmost minimum $j^*$. The rows above have their minima in columns at most $j^*$, and the rows below in columns at least $j^*$. Recurse on both halves with these column ranges. At one level of the recursion, the column ranges of the calls overlap only at their ends, so a level reads at most $m$ plus the number of calls entries. There are $\lceil \lg (n+1) \rceil$ levels, which gives $O(m \log n + n)$. This is the method of [divide and conquer optimization](/divide-and-conquer-optimization/).

**SMAWK.** The [SMAWK algorithm](/smawk-algorithm/) first removes columns until at most $n$ remain, by a stack pass that uses the condition on $2 \times 2$ submatrices. Then it solves the rows at odd positions by recursion and fills in the others by short scans.

## Bounds

- **Upper bound.** $O(n + m)$ evaluations and time, by SMAWK, in the oracle model on a word RAM.
- **Lower bound.** $\Omega(n + m)$. The output has $n$ entries. For the term $m$: if all rows but the first are strictly decreasing, the matrix is totally monotone for every first row, and an algorithm that does not read an entry of the first row can miss its only minimum. The full argument is in the complexity proof of SMAWK.
- **General matrices.** Without a condition, $nm$ evaluations are needed: an unread entry can be the only minimum of its row.

So the problem has complexity $\Theta(n + m)$, with SMAWK optimal up to a constant factor.

## Reductions

- **From one layer of a layered dynamic program.** For $f_t(j) = \min_{i} \bigl( f_{t-1}(i) + w(i, j) \bigr)$ with a Monge cost $w$, the matrix $A[j][i] = f_{t-1}(i) + w(i, j)$ is Monge, since adding a term that depends only on the column keeps the Monge property. One layer is then one row minima problem. This is how SMAWK speeds up the [divide and conquer optimization](/divide-and-conquer-optimization/) setting from $O(n \log n)$ to $O(n)$ per layer.
- **From the concave least weight subsequence problem.** Hirschberg and Larmore defined the least weight subsequence problem and solved the concave case in $O(n \log n)$ time. With the online variant above, the time drops to $O(n)$.
- **From all farthest neighbors of a convex polygon.** For the vertices of a convex polygon in order, the distances, after cutting the cyclic order at the right places, form totally monotone matrices for row maxima. So all the farthest vertices are found in $O(n)$ time. This was one of the first applications given by Aggarwal, Klawe, Moran, Shor and Wilber.

## Applications

- **Line breaking.** [Optimal text wrapping](/optimal-text-wrapping/) with a convex penalty of the slack is a concave least weight subsequence problem, so it is solvable in linear time.
- **Speed-ups of dynamic programs.** The [Monge property](/monge-property/), the [Knuth optimization](/knuth-optimization/) and the [divide and conquer optimization](/divide-and-conquer-optimization/) all rely on monotone row minima.
- **Geometry.** All farthest neighbors and other problems on the vertices of a convex polygon.
- **Sequence comparison.** Eppstein, Galil, Giancarlo and others use matrix searching for alignment with convex or concave gap costs.

## References
