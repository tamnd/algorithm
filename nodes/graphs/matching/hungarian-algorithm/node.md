---
tag: N33C44
kind: algorithm
slug: hungarian-algorithm
name: Hungarian algorithm
aliases:
- Kuhn-Munkres algorithm
- Munkres algorithm
area: graphs/matching
level: core
summary: Solves the assignment problem in O(n²m) time, O(n³) for a square matrix, using vertex potentials and augmenting paths.
solves: [assignment-problem]
model: word-ram
complexity:
  vars: {n: the number of rows, m: the number of columns (n ≤ m)}
  time: {worst: O(n^2 m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1955
  people: [Harold W. Kuhn, James Munkres, Jack Edmonds, Richard M. Karp, Nobuaki Tomizawa]
  note: Kuhn published the method in 1955 and named it after Kőnig and Egerváry; Munkres proved a polynomial bound in 1957; the O(n^3) form with shortest paths and potentials is due to Tomizawa (1971) and to Edmonds and Karp (1972).
prereqs: [assignment-problem, kuhn-algorithm, potential-function-reduced-costs, dijkstra]
see_also: [jonker-volgenant-algorithm, auction-algorithm, konig-theorem, successive-shortest-path, min-cost-flow-problem, minimum-weight-perfect-matching, lp-duality, complementary-slackness]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 25.3, The Hungarian algorithm for the assignment problem
  - paper: doi:10.1002/nav.3800020109
    title: Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2(1-2), 83 to 97 (1955)
    locator: the whole paper
  - paper: doi:10.1137/0105003
    title: James Munkres, Algorithms for the assignment and transportation problems, Journal of the Society for Industrial and Applied Mathematics 5(1), 32 to 38 (1957)
    locator: the whole paper (the matrix form of the method and its polynomial bound)
  - paper: doi:10.1145/321694.321699
    title: Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2), 248 to 264 (1972)
    locator: the section on minimum cost flow (shortest augmenting paths with nonnegative reduced costs from vertex potentials)
  - book: isbn:9780898716634
    title: Rainer Burkard, Mauro Dell'Amico and Silvano Martello, Assignment Problems, SIAM
    locator: Chapter 4, Linear sum assignment problem (the Hungarian algorithm, its O(n^3) implementation, and shortest path methods)
  - paper: "Nobuaki Tomizawa, On some techniques useful for solution of transportation network problems, Networks 1(2) (1971)"
    locator: the whole paper (shortest paths with vertex potentials for the transportation and assignment problems)
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 596 to 615 (1987)
    locator: the section on applications (the assignment problem in O(nm + n^2 log n) time)
  - paper: "Harold N. Gabow and Robert E. Tarjan, Faster scaling algorithms for network problems, SIAM Journal on Computing 18(5), 1013 to 1036 (1989)"
    locator: the section on the assignment problem (O(m sqrt(n) log(nN)) time)
---

The Hungarian algorithm solves the [assignment problem](/assignment-problem/): given an $n \times m$ cost matrix with $n \le m$, give each row its own column so that the total cost is least. It works on the weighted [bipartite graph](/bipartite-graph/) of rows and columns. It keeps a price on each row and each column, the [potentials](/potential-function-reduced-costs/), and adds the rows one at a time, each by an [augmenting path](/augmenting-path/) of least reduced cost. The version here runs in $O(n^2 m)$ time, which is $O(n^3)$ for a square matrix, and the final potentials prove that the answer is optimal.

## In plain words

Rows are workers, columns are jobs, and an entry is the cost of that worker on that job. Give each worker a wage and each job a bonus, and keep one rule: a worker's wage plus a job's bonus is never more than the cost of that pair. A pair where the two are equal is called tight. If all workers get different jobs along tight pairs, the total cost equals the sum of all wages and bonuses, and no assignment costs less.

The algorithm adds workers one at a time. The new worker tries to reach a free job along tight pairs, moving other workers as in [Kuhn's algorithm](/kuhn-algorithm/). When it gets stuck, it raises the wages and lowers the bonuses of the workers and jobs it has reached, by the smallest amount that makes one more pair tight, and goes on until it reaches a free job.

## The problem

The input is a matrix $C = (c_{ij})$ with $n$ rows and $m \ge n$ columns, of integers, rationals or reals, which may be negative. The rows and the columns are the two sides of a complete [weighted bipartite graph](/weighted-graph/), and $c_{ij}$ is the weight of the edge $ij$. The output is an injective map $\sigma$ from rows to columns with least total cost $\sum_i c_{i\sigma(i)}$. A missing edge has cost $+\infty$. If each assignment uses a missing edge, the graph has no matching that covers all rows, and the answer is "none". For $n = 0$ the answer is the empty assignment with cost 0. To maximize the total, negate the matrix. If $n > m$, transpose it.

The linear program and its dual are

$$\min \sum_{i,j} c_{ij} x_{ij} \ \text{ s.t. } \sum_j x_{ij} = 1, \ \sum_i x_{ij} \le 1, \ x \ge 0, \qquad \max \sum_i u_i + \sum_j v_j \ \text{ s.t. } u_i + v_j \le c_{ij}, \ v \le 0.$$

The algorithm finds an optimal solution of both, with $x$ integral.

## The algorithm

Rows are $1 \ldots n$ and columns $1 \ldots m$. Column 0 is a dummy that holds the row being added. The array $p[j]$ is the row matched to column $j$, or 0 if column $j$ is free. The reduced cost of $ij$ is $c_{ij} - u_i - v_j$.

```pseudo id=main
HUNGARIAN(C)                               ▷ C has n rows and m ≥ n columns
L1  u[0..n] ← 0, v[0..m] ← 0, p[0..m] ← 0
L2  for i ← 1 to n do                      ▷ add row i
L3      p[0] ← i, j0 ← 0, minv[0..m] ← ∞, used[0..m] ← false
L4      repeat
L5          used[j0] ← true, i0 ← p[j0], δ ← ∞
L6          for each column j ≥ 1 with used[j] = false do
L7              r ← C[i0, j] − u[i0] − v[j]
L8              if r < minv[j] then minv[j] ← r, way[j] ← j0
L9              if minv[j] < δ then δ ← minv[j], j1 ← j
L10         for j ← 0 to m do
L11             if used[j] then u[p[j]] ← u[p[j]] + δ, v[j] ← v[j] − δ
L12             else minv[j] ← minv[j] − δ
L13         j0 ← j1
L14     until p[j0] = 0                    ▷ column j0 is free
L15     repeat j1 ← way[j0], p[j0] ← p[j1], j0 ← j1 until j0 = 0
L16 return the pairs (p[j], j) with p[j] ≠ 0
```

Each round of lines L3 to L15 is one search, a [Dijkstra](/dijkstra/)-like growth of an alternating tree from row $i$. The *used* columns are the columns in the tree, and their rows are the rows in the tree. The value $\text{minv}[j]$ is the least reduced cost from a tree row to the column $j$ outside the tree, and $\text{way}[j]$ is the tree column whose row gives it. Line L9 picks the outside column $j_1$ with the least such value $\delta$. Lines L10 to L12 change the potentials by $\delta$: tree rows go up, tree columns go down, so the tree edges stay tight and the edge to $j_1$ becomes tight. If $j_1$ is matched, its row joins the tree at the next pass. If $j_1$ is free, line L15 walks the way pointers back to column 0 and shifts each row one column along the path. This is the augmentation.

## Example

Take the $4 \times 4$ matrix

$$C = \begin{pmatrix} 9 & 2 & 7 & 8 \\ 6 & 4 & 3 & 7 \\ 5 & 8 & 1 & 8 \\ 7 & 6 & 9 & 4 \end{pmatrix}.$$

| round | tree growth (row, then the new tight column and $\delta$) | augmenting path | $u$ after | $v$ after |
|---|---|---|---|---|
| row 1 | row 1: column 2, $\delta = 2$, free | $1 \to 2$ | 2 0 0 0 | 0 0 0 0 |
| row 2 | row 2: column 3, $\delta = 3$, free | $2 \to 3$ | 2 3 0 0 | 0 0 0 0 |
| row 3 | row 3: column 3, $\delta = 1$, held by row 2; row 2: column 2, $\delta = 1$, held by row 1; row 1: column 1, $\delta = 2$, free | $3 \to 3$, $2 \to 1$ | 4 6 4 0 | 0 −2 −3 0 |
| row 4 | row 4: column 4, $\delta = 4$, free | $4 \to 4$ | 4 6 4 4 | 0 −2 −3 0 |

In round 3, row 3 wants column 3 (reduced cost 1), which row 2 holds. From row 2 the cheapest outside columns are 2 (reduced cost 1 after the first shift) and 1. Column 2 is held by row 1, so row 1 joins the tree. Now the cheapest outside column is column 1, at $\delta = 2$, and its way pointer is column 3, as row 2 gives the least reduced cost to it. So the path is row 3 to column 3, row 2 to column 1, and row 1 keeps column 2.

The result is row 1 to column 2, row 2 to column 1, row 3 to column 3, row 4 to column 4, with cost $2 + 6 + 1 + 4 = 13$. The final potentials give $\sum u + \sum v = 18 - 5 = 13$, and $u_i + v_j \le c_{ij}$ for all 16 entries, so 13 is the minimum.

**No perfect matching.** If rows 1 and 2 can use only column 1, all other entries of these rows being $+\infty$, every assignment uses a missing edge, and the answer is "none". The implementation replaces $+\infty$ by a cost larger than any assignment of finite entries, runs the same code, and reports "none" if the result uses such an entry.

## Correctness

Between rounds the algorithm keeps two invariants. *Dual feasibility*: $u_i + v_j \le c_{ij}$ for each row $i$ added so far and each column $j$, and $v_j \le 0$. *Tightness*: $u_{p[j]} + v_j = c_{p[j], j}$ for each matched column $j$, and $v_j = 0$ for each free column. With these, each assignment $\sigma$ costs $\sum_i c_{i\sigma(i)} \ge \sum_i u_i + \sum_i v_{\sigma(i)} \ge \sum_i u_i + \sum_j v_j$, and the final matching costs exactly $\sum_i u_i + \sum_j v_j$. So it is optimal. This is [weak duality](/weak-duality/) and [complementary slackness](/complementary-slackness/) for the linear program above. Each round ends because each pass of lines L5 to L13 puts one more column in the tree, and at most $i - 1$ columns are matched. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/) with exact arithmetic on the costs; for real costs, the real RAM.

- **One pass of lines L5 to L13.** Lines L6 to L9 and L10 to L12 take $O(m)$ time each.
- **One round.** Row $i$ meets at most $i - 1$ matched columns, so its tree gets at most $i - 1$ matched columns before a free one is reached. The round makes at most $i$ passes, and line L15 takes $O(i)$. So round $i$ takes $O(i \cdot m)$.
- **Total.** $\sum_{i=1}^{n} O(i m) = O(n^2 m)$, which is $O(n^3)$ for $n = m$.
- **Space.** $\Theta(n + m)$ for $u$, $v$, $p$, `way`, `minv` and `used`, besides the matrix.

For a sparse graph with $N$ vertices and $m'$ edges, the same search done by Dijkstra's algorithm with a [Fibonacci heap](/fibonacci-heap/) gives $O(N m' + N^2 \log N)$ time; this is the [successive shortest path](/successive-shortest-path/) method on the assignment network. With integer costs at most $W$ in absolute value, Gabow and Tarjan's cost scaling takes $O(m' \sqrt N \log(NW))$.

## Properties

- **Exact and integral.** With integer costs, all potentials stay integers, as each $\delta$ is a difference of integers.
- **Certificate of optimality.** The final $u$ and $v$ are an optimal dual solution. Checking $u_i + v_j \le c_{ij}$ for all entries and the equality on the matched entries takes $O(nm)$ time.
- **Incremental.** After round $i$, the matching is an optimal assignment of the first $i$ rows. A new row can be added in $O(i m)$ time.
- **Negative costs.** No shift is needed. The potentials start at 0, and the first $\delta$ of each round can be negative; the proof does not use the sign of the costs.
- **Bipartite only.** For the minimum-weight perfect matching of a general graph, see [minimum-weight perfect matching](/minimum-weight-perfect-matching/) and [Edmonds' blossom algorithm](/edmonds-blossom/).

## Variants and improvements

- **The matrix form.** The 1955 and 1957 versions subtract row and column minima, then cover all zeros with the fewest lines, then shift the uncovered entries by their minimum, and repeat. With a careless choice of the line covers, this takes $O(n^4)$ time. It is the same method on the same dual.
- **[Jonker-Volgenant](/jonker-volgenant-algorithm/).** Start with column reduction and an augmenting row reduction that assigns most rows cheaply, then finish with shortest augmenting paths. It has the same $O(n^3)$ worst case and is much faster in practice; it is the solver behind many library routines.
- **[Auction algorithm](/auction-algorithm/).** Rows bid for columns and prices rise. With $\varepsilon$-scaling it is fast on sparse and parallel machines.
- **Min-cost flow.** The assignment problem is a [min-cost flow problem](/min-cost-flow-problem/) on a unit network, and the Hungarian algorithm is its successive shortest path method with the potentials kept from round to round.

## When to use it

Use this $O(n^3)$ code for dense cost matrices with up to some thousands of rows. It has no tuning, works with negative and real costs, and returns a dual certificate. For large sparse graphs, use the Dijkstra form with a heap, or a cost-scaling or auction code. For speed on large dense matrices, use [Jonker-Volgenant](/jonker-volgenant-algorithm/). If the costs do not matter and only a matching of largest size is wanted, use [Kuhn's algorithm](/kuhn-algorithm/) or [Hopcroft-Karp](/hopcroft-karp/).

## Pitfalls

- **Maximizing with the minimizing code.** For a maximum-weight assignment, run the code on $-C$ (or on $W - C$ for a constant $W$). Running it on $C$ gives the cheapest assignment.
- **Forgetting line L12.** The values $\text{minv}[j]$ of the columns outside the tree must drop by $\delta$, because the reduced costs from tree rows dropped by $\delta$. Without this, the next pass picks a wrong column and the potentials stop being feasible.
- **Infinite costs in the arithmetic.** With $+\infty$ for a missing edge, line L7 can compute $\infty - \infty$, which is not a number in floating point. Replace a missing entry by a finite cost $B$ larger than $n \cdot (\max c - \min c) + |\min c|$, over the finite entries, and reject the result if it uses $B$. A very large $B$ in a 64-bit integer type can overflow; Python integers do not.
- **More rows than columns.** The loop of line L4 never finds a free column for the last rows, and it does not stop. Transpose the matrix first.
- **Floating point tightness.** Do not test $u_i + v_j = c_{ij}$ with `==` on floats. This version never tests tightness; it compares reduced costs, so rounding changes the cost only by rounding errors.

## Implementations

The Python version takes the matrix as a list of rows, with `math.inf` for a missing edge, and returns the total cost and the column of each row, or `None`. It accepts `int`, `Fraction` and `float` costs.

## History

Harold Kuhn published the method in 1955 and called it the Hungarian method, because it rests on the work of Dénes Kőnig and Jenő Egerváry from 1931. James Munkres gave a matrix version in 1957 and proved that it runs in polynomial time. Nobuaki Tomizawa in 1971, and Jack Edmonds and Richard Karp in 1972, showed that with vertex potentials each augmentation is a shortest path search with nonnegative reduced costs, which gives the $O(n^3)$ bound. Fredman and Tarjan's Fibonacci heaps of 1987 gave the $O(Nm + N^2 \log N)$ bound for sparse graphs, and Gabow and Tarjan's cost scaling of 1989 gave the bound for integer costs.

## References
