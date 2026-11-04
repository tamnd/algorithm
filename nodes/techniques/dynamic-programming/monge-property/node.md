---
tag: VGQV3T
kind: definition
slug: monge-property
name: Monge property
aliases:
- Monge array
- Monge matrix
- quadrangle inequality
area: techniques/dynamic-programming
level: advanced
summary: A matrix inequality under which the positions of row minima are monotone.
prereqs: [convex-function]
see_also: [row-minima-of-totally-monotone-matrices, smawk-algorithm, knuth-optimization, divide-and-conquer-optimization, aliens-trick, optimal-text-wrapping, submodular-function]
sources:
  - paper: doi:10.1016/0166-218X(95)00103-X
    title: Rainer E. Burkard, Bettina Klinz and Rüdiger Rudolf, Perspectives of Monge properties in optimization, Discrete Applied Mathematics 70(2), 95-161, 1996
    locator: the introduction (definitions, the adjacent 2 by 2 test, history from Monge and Hoffman) and the sections on algebraic properties and on row minima
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 4, end-of-chapter problem Monge arrays
  - paper: doi:10.1145/800141.804691
    title: F. Frances Yao, Efficient dynamic programming using quadrangle inequalities, Proceedings of the 12th ACM STOC, 429-435, 1980
    locator: the quadrangle inequality and the monotonicity condition for interval costs
  - paper: doi:10.1007/BF01840359
    title: Alok Aggarwal, Maria M. Klawe, Shlomo Moran, Peter Shor and Robert Wilber, Geometric applications of a matrix-searching algorithm, Algorithmica 2, 195-208, 1987
    locator: the definition of totally monotone matrices
---

A matrix $A$ has the Monge property when $A[i][j] + A[i'][j'] \le A[i][j'] + A[i'][j]$ for all rows $i < i'$ and columns $j < j'$. In words: for any two rows and two columns, the two entries on the main diagonal of the $2 \times 2$ submatrix cost no more than the two on the other diagonal. A Monge matrix is [totally monotone](/row-minima-of-totally-monotone-matrices/), so the leftmost minima of its rows move only to the right, and all row minima can be found with $O(n + m)$ evaluations by the [SMAWK algorithm](/smawk-algorithm/). The same inequality for a cost $w(i, j)$ of an interval is called the quadrangle inequality, and it is the condition of the [Knuth optimization](/knuth-optimization/) and of the [divide and conquer optimization](/divide-and-conquer-optimization/).

## Definition

Let $A$ be an $n \times m$ matrix with real entries, or with entries in $\mathbb{R} \cup \{+\infty\}$ under the usual rules.

**Monge.** $A$ is a Monge matrix when

$$A[i][j] + A[i'][j'] \le A[i][j'] + A[i'][j] \quad \text{for all } 1 \le i < i' \le n \text{ and } 1 \le j < j' \le m.$$

**Inverse Monge.** $A$ is an inverse Monge matrix when the inequality holds in the other direction, that is, when $-A$ is Monge. Inverse Monge matrices have the same theory with maxima in place of minima.

**Adjacent test.** For a real matrix, $A$ is Monge if and only if

$$A[i][j] + A[i+1][j+1] \le A[i][j+1] + A[i+1][j] \quad \text{for all } 1 \le i < n \text{ and } 1 \le j < m.$$

*Proof.* The adjacent inequalities are special cases of the full ones. For the converse, let $\Delta(i, j) = A[i][j+1] + A[i+1][j] - A[i][j] - A[i+1][j+1]$, which is $\ge 0$ by the adjacent test. For $i < i'$ and $j < j'$, the sum $\sum_{r=i}^{i'-1} \sum_{s=j}^{j'-1} \Delta(r, s)$ telescopes: summing over $s$ first gives $A[r][j'] + A[r+1][j] - A[r][j] - A[r+1][j']$, and summing this over $r$ gives $A[i][j'] + A[i'][j] - A[i][j] - A[i'][j']$. A sum of numbers that are $\ge 0$ is $\ge 0$, which is the Monge inequality. $\square$

So a test of all $(n-1)(m-1)$ adjacent pairs decides the property in $O(nm)$ time. The test needs finite entries: with $+\infty$ entries, the differences are not defined, and the full inequality must be checked, or the infinite entries must form a shape that the theory of partial Monge matrices allows.

**Quadrangle inequality.** Let $w(i, j)$ be defined for $0 \le i \le j \le n$, as the cost of an interval. Yao calls $w$ a function that satisfies the quadrangle inequality when

$$w(i, j) + w(i', j') \le w(i, j') + w(i', j) \quad \text{for all } i \le i' \le j \le j'.$$

This is the Monge property of the upper triangular matrix $W[i][j] = w(i, j)$ on the entries where it is defined. The [Knuth optimization](/knuth-optimization/) also needs $w$ to be monotone on the inclusion of intervals: $w(i', j) \le w(i, j')$ when $[i', j] \subseteq [i, j']$.

**Consequence: monotone row minima.** Let $j(i)$ be the leftmost column of a minimum of row $i$. If $A$ is Monge and $i < i'$, then $j(i) \le j(i')$. More strongly, $A$ is totally monotone: for $i < i'$ and $j < j'$, $A[i][j] > A[i][j'] \implies A[i'][j] > A[i'][j']$, because the Monge inequality gives $A[i'][j] - A[i'][j'] \ge A[i][j] - A[i][j'] > 0$. The [row minima page](/row-minima-of-totally-monotone-matrices/) proves that total monotonicity gives monotone minima.

## Examples and non-examples

**A convex function of a difference.** Let $x_1 \le \cdots \le x_n$ and $y_1 \le \cdots \le y_m$, let $f : \mathbb{R} \to \mathbb{R}$ be [convex](/convex-function/), and let $A[i][j] = f(x_i - y_j)$. Then $A$ is Monge.

*Proof.* Take $i < i'$ and $j < j'$, and put $a = x_i - y_{j'}$, $b = x_i - y_j$, $c = x_{i'} - y_{j'}$ and $d = x_{i'} - y_j$. Then $a \le b \le d$, $a \le c \le d$ and $b + c = a + d$. If $a = d$, all four are equal. Otherwise write $b = \lambda a + (1 - \lambda) d$ with $\lambda \in [0, 1]$; then $c = a + d - b = (1 - \lambda) a + \lambda d$. Convexity gives $f(b) \le \lambda f(a) + (1-\lambda) f(d)$ and $f(c) \le (1-\lambda) f(a) + \lambda f(d)$. Adding, $f(b) + f(c) \le f(a) + f(d)$, which is $A[i][j] + A[i'][j'] \le A[i][j'] + A[i'][j]$. $\square$

With $x = (1, 3, 6, 8)$, $y = (0, 2, 4, 5, 9)$ and $f(t) = |t|$, this gives the nearest-site matrix of the [row minima page](/row-minima-of-totally-monotone-matrices/).

**The cost of a segment.** Let $S_0 \le S_1 \le \cdots \le S_n$ be prefix sums of nonnegative numbers and $w(i, j) = (S_j - S_i)^2$ for $i \le j$. This is $f(S_i - S_j)$ with the convex $f(t) = t^2$, so $w$ satisfies the quadrangle inequality. For $S = (0, 2, 3, 7, 8)$ the upper triangle is

| $w(i, j)$ | $j = 0$ | $j = 1$ | $j = 2$ | $j = 3$ | $j = 4$ |
|---|---|---|---|---|---|
| $i = 0$ | 0 | 4 | 9 | 49 | 64 |
| $i = 1$ | | 0 | 1 | 25 | 36 |
| $i = 2$ | | | 0 | 16 | 25 |
| $i = 3$ | | | | 0 | 1 |
| $i = 4$ | | | | | 0 |

For example, $w(0, 2) + w(1, 3) = 9 + 25 = 34 \le w(0, 3) + w(1, 2) = 49 + 1 = 50$. This $w$ is also monotone on the inclusion of intervals. Costs of this kind appear in the partition of an array into parts with a cost per part.

**Sums and simple terms.** For any vectors $u$ and $v$, the matrix $A[i][j] = u_i + v_j$ is Monge with equality in each inequality. The product $x_i y_j$ of two increasing sequences is inverse Monge, since $x_i y_j + x_{i'} y_{j'} - x_i y_{j'} - x_{i'} y_j = (x_{i'} - x_i)(y_{j'} - y_j) \ge 0$. For $x = (1, 3, 4)$ and $y = (1, 2, 4)$, the matrix of products has rows $(1, 2, 4)$, $(3, 6, 12)$ and $(4, 8, 16)$, and its negation is Monge.

**Non-example: a concave function.** With $f(t) = -|t|$, $x = (0, 1)$ and $y = (0, 1)$, the matrix has rows $(0, -1)$ and $(-1, 0)$. The Monge test gives $0 + 0 \le -1 - 1$, which is false. The row minima are in columns 2 and 1, so the minima are not even monotone.

**Non-example: totally monotone but not Monge.** The rows $(0, 0)$ and $(0, 1)$ fail the Monge test, $0 + 1 \le 0 + 0$. But the first row has no strict win of the right column, so the matrix is totally monotone. Total monotonicity depends only on the order of the entries within each row, while the Monge property depends on their values. For example, $\sqrt{|x_i - y_j|}$ with $x = (0, 1, 3)$ and $y = (0, 2, 5)$ is not Monge (rows 1 and 2 with columns 2 and 3 give $\sqrt{2} + 2$ on the main diagonal, about 3.414, against $\sqrt{5} + 1$, about 3.236), but it has the same order in each row as the Monge matrix $|x_i - y_j|$, so it is totally monotone.

### Closure properties

These follow from the definition, since each Monge inequality is linear in the entries.

- The sum of two Monge matrices of the same size is Monge, and so is a nonnegative multiple of one.
- Adding $u_i + v_j$ to each entry keeps the property. So $D[i] + w(i, j)$ is Monge in $(j, i)$ when $w$ is, which is the reason why one layer of a dynamic program with a Monge cost is a [row minima problem](/row-minima-of-totally-monotone-matrices/).
- Each submatrix (some rows and some columns, in their order) of a Monge matrix is Monge.
- The transpose of a Monge matrix is Monge, and so is the matrix with both the rows and the columns in reverse order. Reversing only the rows, or only the columns, turns a Monge matrix into an inverse Monge one.
- The min-plus product $C[i][k] = \min_j (A[i][j] + B[j][k])$ of two Monge matrices is Monge. This is a theorem, not a direct consequence of linearity; see Burkard, Klinz and Rudolf.

## Related definitions

- **[Totally monotone matrix](/row-minima-of-totally-monotone-matrices/).** Each $2 \times 2$ submatrix has monotone row minima. This is weaker than Monge and is what the [SMAWK algorithm](/smawk-algorithm/) needs.
- **Monotone matrix.** The leftmost row minima are nondecreasing. Weaker again, and enough for the divide and conquer method.
- **Quadrangle inequality.** The Monge property of a cost on intervals, as above. Yao used it to prove the speed-up of [Knuth's optimization](/knuth-optimization/) for a general class of interval dynamic programs.
- **[Submodular function](/submodular-function/).** View $A$ as a function on the product of the two chains $\{1, \ldots, n\}$ and $\{1, \ldots, m\}$, with the coordinatewise min and max. Then the Monge property is exactly submodularity: $A(p \wedge q) + A(p \vee q) \le A(p) + A(q)$. For two comparable pairs it is an equality, and for $p = (i, j')$ and $q = (i', j)$ with $i < i'$ and $j < j'$ it is the Monge inequality.
- **[Convex function](/convex-function/).** A function $g$ on the integers is convex when $g(k-1) + g(k+1) \ge 2 g(k)$. The matrix $g(j - i)$ is Monge exactly when $g$ is convex on the range of differences, by the adjacent test.

### History

Gaspard Monge observed the property in 1781 in his memoir on moving earth from cuts to fills: when two transport routes cross, they can be uncrossed without a larger total cost. Alan Hoffman showed in 1963 that the northwest corner rule solves the transportation problem for every supply and demand exactly when the cost matrix has the Monge property, and credited the idea to Monge. Burkard, Klinz and Rudolf give both facts and a survey of the many later uses.

## References
