---
tag: 3TFVRQ
kind: problem
slug: grid-paths-with-obstacles
name: Counting paths on grids with obstacles
area: techniques/dynamic-programming
level: intro
summary: Problem of counting monotone routes across a grid while avoiding blocked cells, solved with dynamic programming.
prereqs: [binomial-coefficient, tabulation, pascal-triangle-dp]
see_also: [counting-lattice-paths, catalan-numbers, dag-dynamic-programming, rolling-array-space-reduction, breadth-first-search, binomial-coefficient-computation, overlapping-subproblems, directed-acyclic-graph]
sources:
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 5 (binomial coefficients and their basic identities)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition
    locator: Chapter 2 (sieve methods and the principle of inclusion-exclusion)
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 6.2.2, Paths in a Grid
---

Counting paths on a grid with obstacles asks for the number of routes from the top-left cell to the bottom-right cell of a rectangular grid that move only right or down and never enter a blocked cell. Without obstacles the answer is a [binomial coefficient](/binomial-coefficient/). With obstacles, a table in which each cell holds the sum of the cell above and the cell to the left gives the answer in $O(mn)$ additions for an $m \times n$ grid. When the grid is huge and the obstacles are few, inclusion and exclusion over the $k$ sorted obstacles gives the count in $O(k^2)$ operations after a precomputation of factorials.

## In plain words

A robot stands in the top-left square of a board. It can only step one square right or one square down. Some squares are walls. How many different routes reach the bottom-right square?

Every route to a square comes from the square above it or from the square to its left. So the number of routes to a square is the number of routes to the square above plus the number to the square on the left. A wall has no routes. Fill the board row by row with this rule, and the last square holds the answer.

When the board is very large but has only a few walls, count all routes with a formula, then subtract the routes that touch a wall. To avoid subtracting a route twice, sort the walls and charge each bad route to the first wall that it touches.

## Definition

**Input.** Integers $m, n \ge 1$ and a set $B \subseteq \{0, \ldots, m-1\} \times \{0, \ldots, n-1\}$ of blocked cells. Cell $(i, j)$ is in row $i$ and column $j$.

**Paths.** A monotone path is a sequence of cells $(0, 0) = u_0, u_1, \ldots, u_{m+n-2} = (m-1, n-1)$ in which each step adds $1$ to the row or to the column. It avoids $B$ when no $u_t$ is in $B$. Each monotone path has exactly $m - 1$ down steps and $n - 1$ right steps.

**Output.** The number $N$ of monotone paths that avoid $B$. Often the answer is asked modulo a prime $p$.

**Recurrence.** Let $P(i, j)$ be the number of monotone paths from $(0, 0)$ to $(i, j)$ that avoid $B$. Then $P(i, j) = 0$ if $(i, j) \in B$, $P(0, 0) = 1$ if $(0, 0) \notin B$, and otherwise

$$ P(i, j) = P(i - 1, j) + P(i, j - 1), $$

with $P = 0$ outside the grid. The last step of a path to $(i, j)$ comes from $(i - 1, j)$ or from $(i, j - 1)$. These two sets of paths are disjoint, and removing the last cell is a bijection from each set onto the paths to that neighbour. So the sum counts each path once. The answer is $N = P(m - 1, n - 1)$.

## Variants

- **No obstacles.** $N = \binom{m + n - 2}{m - 1}$: a path is fixed by choosing which $m - 1$ of the $m + n - 2$ steps go down. See [counting lattice paths](/counting-lattice-paths/).
- **Decision form.** Decide whether at least one path exists. This is reachability in a [directed acyclic graph](/directed-acyclic-graph/), solved by the same table with Boolean values or by [breadth-first search](/breadth-first-search/).
- **Weighted form.** Each cell has a value, and the task is the path of largest total value. The rule is $S(i, j) = a_{ij} + \max(S(i-1, j), S(i, j-1))$ (Laaksonen, Section 6.2.2).
- **A boundary instead of cells.** Paths from $(0, 0)$ to $(n, n)$ on lattice points that never go above the diagonal are counted by the [Catalan numbers](/catalan-numbers/). This is the case where every cell with $j > i$ is blocked.
- **More step types.** Diagonal steps or steps of other fixed shapes keep the graph acyclic, and the table takes a sum over the allowed predecessors.
- **Steps in all four directions.** The graph is no longer acyclic, the number of walks is infinite, and counting simple paths is a different and much harder problem. The table method does not apply.

## Examples

**The centre blocked.** In a $3 \times 3$ grid there are $\binom{4}{2} = 6$ paths. Blocking the centre $(1, 1)$ removes the $2 \cdot 2 = 4$ paths through it, so $N = 2$: along the top and right edges, or along the left and bottom edges.

**A table.** Take $m = 4$, $n = 5$ and $B = \{(0, 3), (1, 1), (2, 3)\}$. The table $P$, with a blocked cell shown as 0:

| | col 0 | col 1 | col 2 | col 3 | col 4 |
| --- | --- | --- | --- | --- | --- |
| row 0 | 1 | 1 | 1 | 0 | 0 |
| row 1 | 1 | 0 | 1 | 1 | 1 |
| row 2 | 1 | 1 | 2 | 0 | 1 |
| row 3 | 1 | 2 | 4 | 4 | 5 |

So $N = 5$, out of $\binom{7}{3} = 35$ paths with no obstacles. The cell $(0, 4)$ is 0 because its only possible predecessor, $(0, 3)$, is blocked.

**Inclusion and exclusion on the same grid.** Sort the obstacles by row, then column: $o_1 = (0, 3)$, $o_2 = (1, 1)$, $o_3 = (2, 3)$. Let $D_t$ be the number of paths from $(0, 0)$ to $o_t$ that touch no earlier obstacle. Then $D_1 = 1$, $D_2 = \binom{2}{1} = 2$, and $D_3 = \binom{5}{2} - D_1 \cdot 1 - D_2 \cdot \binom{3}{1} = 10 - 1 - 6 = 3$. The answer is $35 - D_1 \binom{4}{3} - D_2 \binom{5}{2} - D_3 \binom{2}{1} = 35 - 4 - 20 - 6 = 5$, as in the table.

**The Catalan case.** On the $5 \times 5$ grid with every cell $(i, j)$ with $j > i$ blocked, the table gives $14 = C_4$, the fourth Catalan number.

**Large counts.** Without obstacles, a $101 \times 101$ grid has $\binom{200}{100}$ paths, a number of 196 bits. Modulo $10^9 + 7$ it is $407336795$.

## Known algorithms

- **Row-by-row table.** Fill $P$ in row-major order. $O(mn)$ additions and $O(mn)$ space. Keeping one row and updating it in place, $P[j] \leftarrow P[j] + P[j - 1]$, cuts the space to $O(n)$; see [rolling-array space reduction](/rolling-array-space-reduction/).
- **Closed form without obstacles.** One [binomial coefficient](/binomial-coefficient-computation/), in $O(\min(m, n))$ arithmetic operations.
- **Inclusion and exclusion over $k$ obstacles.** Sort the obstacles so that whenever $o_s$ can reach $o_t$ by a monotone path, $s < t$; the order by row and then by column works. Let $\pi(a, b) = \binom{(b_1 - a_1) + (b_2 - a_2)}{b_1 - a_1}$ if $b_1 \ge a_1$ and $b_2 \ge a_2$, and $0$ otherwise. Then
$$ D_t = \pi\bigl((0,0), o_t\bigr) - \sum_{s < t} D_s \, \pi(o_s, o_t), \qquad N = \pi\bigl((0,0), (m-1, n-1)\bigr) - \sum_{t=1}^{k} D_t \, \pi\bigl(o_t, (m-1, n-1)\bigr). $$
With factorials and inverse factorials up to $m + n - 2$ precomputed modulo a prime $p > m + n - 2$, each $\pi$ costs $O(1)$, so the total is $O(m + n + k^2)$ operations, independent of the area of the grid.
- **Decision.** One pass of the Boolean table, or a breadth-first search from $(0, 0)$, in $O(mn)$ time.

## Bounds

**Correctness of inclusion and exclusion.** Call a path bad when it enters some obstacle. Each bad path has a first obstacle $o_t$ on it. Split it at $o_t$. The second part is any monotone path from $o_t$ to the target. The first part goes from $(0, 0)$ to $o_t$ and enters no obstacle before $o_t$. Any obstacle that a monotone path to $o_t$ could enter can reach $o_t$, so by the sort order it is some $o_s$ with $s < t$. So the first parts are exactly the paths to $o_t$ that avoid $o_1, \ldots, o_{t-1}$, and there are $D_t$ of them. The pair of parts determines the path, so the bad paths with first obstacle $o_t$ number $D_t \, \pi(o_t, \text{target})$. Summing over $t$ counts each bad path once, which gives the formula for $N$. The same argument with $o_t$ as the target gives the formula for $D_t$.

**Size of the numbers.** The count is at most $\binom{m + n - 2}{m - 1} < 2^{m + n - 2}$, so it has fewer than $m + n - 1$ bits. With exact integers, each addition of the table costs $O(m + n)$ bit operations, and the table costs $O(mn(m + n))$ bit operations in the worst case. With arithmetic modulo a prime of one word, the table costs $O(mn)$ word operations.

**Lower bound for the table input.** When the blocked cells are given as an $m \times n$ bitmap, every algorithm must read $\Omega(mn)$ cells in the worst case. On the grid with no obstacles, every cell lies on some path, so blocking one cell lowers the count. An algorithm that does not read some cell other than the two ends gives the same answer on both inputs, so it is wrong on one of them. So the table is optimal up to the cost of the arithmetic. With $k$ obstacles given as a list, the inclusion-exclusion method avoids the dependence on $mn$.

## Reductions

- **To path counting in a DAG.** Cells are vertices and each step is an edge. The table is the general [dynamic programming on DAGs](/dag-dynamic-programming/) with the rule "number of paths to a vertex is the sum over its predecessors".
- **From lattice paths and binomials.** With no obstacles the table is [Pascal's triangle](/pascal-triangle-dp/) turned by 45 degrees, and each entry is $\binom{i + j}{i}$.
- **To the Catalan numbers.** Blocking all cells above the diagonal gives the ballot paths, counted by the Catalan numbers.

## Applications

- **Robot and grid motion.** Counting or listing the shortest routes of a robot on a grid with walls, when it moves only toward the goal.
- **Combinatorial identities.** Many binomial identities are proved by counting lattice paths in two ways, with or without forbidden points.
- **Sequence alignment.** An alignment of two strings is a monotone path in a grid, with diagonal steps for matches. Counting or scoring alignments uses the same table with three predecessors.
- **Teaching.** The problem is a standard first example of a two-dimensional dynamic programming table, and of the trade-off between a table over the whole grid and a formula over the few obstacles.

## References
