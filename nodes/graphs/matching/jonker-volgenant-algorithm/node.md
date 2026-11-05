---
tag: TN0EFM
kind: algorithm
slug: jonker-volgenant-algorithm
name: Jonker-Volgenant algorithm
aliases:
- LAPJV
area: graphs/matching
level: advanced
summary: A fast shortest-augmenting-path solver for the linear assignment problem.
solves: [assignment-problem]
model: word-ram
complexity:
  vars: {n: the number of rows and of columns}
  time: {worst: O(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1987
  people: [Roy Jonker, Anton Volgenant]
  note: Jonker and Volgenant combined column reduction, an auction-like row reduction and Dijkstra-style shortest augmenting paths into a code that was faster than earlier assignment codes on their dense and sparse tests.
prereqs: [assignment-problem, hungarian-algorithm, dijkstra, potential-function-reduced-costs]
see_also: [hungarian-algorithm, auction-algorithm, successive-shortest-path, min-cost-flow-problem, minimum-weight-perfect-matching, complementary-slackness, lp-duality, maximum-weight-matching]
sources:
  - paper: doi:10.1007/BF02278710
    title: Roy Jonker and Anton Volgenant, A shortest augmenting path algorithm for dense and sparse linear assignment problems, Computing 38(4), 325 to 340 (1987)
    locator: the whole paper (column reduction, reduction transfer, augmenting row reduction, and the shortest augmenting path phase)
  - book: isbn:9780898716634
    title: Rainer Burkard, Mauro Dell'Amico and Silvano Martello, Assignment Problems, SIAM
    locator: Chapter 4, Linear sum assignment problem (shortest path implementations, the Jonker-Volgenant preprocessing, and computer codes)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications, Prentice Hall
    locator: Chapter 12, Assignments and matchings (the successive shortest path algorithm for the assignment problem)
  - paper: "David F. Crouse, On implementing 2D rectangular assignment algorithms, IEEE Transactions on Aerospace and Electronic Systems 52(4), 1679 to 1696 (2016)"
    locator: the whole paper (a shortest augmenting path method in the style of Jonker and Volgenant for rectangular matrices)
---

The Jonker-Volgenant algorithm, often called LAPJV, solves the [assignment problem](/assignment-problem/): given an $n \times n$ cost matrix, assign each row to a different column with the least total cost. The graph is the complete [bipartite graph](/bipartite-graph/) of rows and columns, with a weight on each edge. Like the [Hungarian algorithm](/hungarian-algorithm/), it keeps dual prices on the columns and grows the assignment by shortest augmenting paths, found with a form of [Dijkstra's algorithm](/dijkstra/) on reduced costs. Before that, it runs three cheap initialization steps that usually assign most rows at once. Its worst case is $O(n^3)$ time, the same as the Hungarian algorithm, but it is one of the fastest assignment codes in practice.

## In plain words

Workers must each get one job, and each job has a cost for each worker. Each job also has a price, and a worker compares jobs by cost minus price.

First, each job goes to the worker who does it most cheaply, where possible. Then free workers bid, as in an auction: a worker takes its best job and lowers that job's price until it likes the job only as much as its second choice. The worker who lost the job bids next.

Each worker who is still free then gets a job by the cheapest chain of moves: it takes a job, the holder moves to another job, and so on until a free job is reached. After each chain the prices change, so that the next chain is again a shortest path. At the end, the prices prove that no assignment is cheaper.

## The problem

The input is an $n \times n$ matrix $C$ of real costs, which may be negative. Rows and columns are the two sides of a complete bipartite graph, with weight $c_{ij}$ on the edge from row $i$ to column $j$. The output is a permutation $x$ (row $i$ gets column $x_i$) of least total cost $\sum_i c_{i x_i}$. The implementation also returns dual values $u_i$ and $v_j$ with $u_i + v_j \le c_{ij}$ for all $i$, $j$ and equality on the chosen pairs, which certify that $x$ is optimal. The empty matrix has the empty assignment.

The complete bipartite graph always has a perfect matching. A missing edge is given a cost larger than the cost of any assignment that avoids missing edges; then the optimum uses such a cost exactly when the graph has no perfect matching. A rectangular matrix is made square with zero-cost dummy rows or columns.

## The algorithm

The algorithm keeps a price $v_j$ for each column, a partial assignment $x$ of rows to columns with inverse $y$, and the invariant

**(CS)** every assigned row $i$ has $c_{i x_i} - v_{x_i} = \min_j (c_{ij} - v_j)$.

Write $u_i = \min_j (c_{ij} - v_j)$, the *row price*; then $u_i + v_j \le c_{ij}$ always, and (CS) says that the assigned pairs are tight.

```pseudo id=main
LAPJV(C)                                            ▷ C is n × n
L1  x[i] ← nil, y[j] ← nil for all rows i and columns j
L2  for j ← n − 1 downto 0 do                         ▷ column reduction
L3      v[j] ← min_i c[i][j], reached at row i*
L4      if x[i*] = nil then x[i*] ← j, y[j] ← i*
L5  for each row i that was a minimum row exactly once in L3 do        ▷ reduction transfer
L6      v[x[i]] ← v[x[i]] − min_{j ≠ x[i]} (c[i][j] − v[j])
L7  repeat twice, with at most 2n bids per pass       ▷ augmenting row reduction
L8      take a free row i; j1, j2 ← columns with the least and second least c[i][j] − v[j], values a ≤ b
L9      if a < b then v[j1] ← v[j1] − (b − a) else if y[j1] ≠ nil then j1 ← j2
L10     give j1 to i; its old row i0, if any, becomes free: bid next if a < b, else in the next pass
L11 for each free row f do                            ▷ augmentation
L12     d[j] ← c[f][j] − v[j], pred[j] ← f for all j;  R ← ∅;  T ← ∅
L13     loop
L14         if T = ∅ then μ ← min{d[j] : j ∉ R};  T ← {j ∉ R : d[j] = μ}
L15             if some j ∈ T is free then end ← j; exit loop
L16         move one column j from T to R;  i ← y[j]
L17         for each j' ∉ R ∪ T: h ← d[j] + (c[i][j'] − v[j']) − (c[i][j] − v[j]); if h < d[j'] then d[j'] ← h, pred[j'] ← i, and if h = μ: if j' is free then end ← j', exit loop, else add j' to T
L18     for each j ∈ R: v[j] ← v[j] + d[j] − μ
L19     repeat i ← pred[end]; y[end] ← i; swap end and x[i] until i = f
L20 return x, with u[i] = c[i][x[i]] − v[x[i]] and v
```

**Column reduction** (lines L2 to L4) sets each price to the least cost in its column, so every reduced cost $c_{ij} - v_j$ is at least 0, and gives each column to a row that reaches its minimum, unless that row already has a column. Columns are scanned from the last, as in the paper.

**Reduction transfer** (lines L5 and L6) lowers the price of the column of each row that was chosen only once, by the gap to that row's second best column. The row's reduced cost at its own column becomes $u_i$, and the other columns become cheaper to reach in the next phases.

**Augmenting row reduction** (lines L7 to L10) is an auction without a minimum bid. A free row takes its best column and lowers the price of that column so that the row is indifferent between it and its second best column. If the column had a row, that row bids next. On a tie, the row takes its second best column instead, so that no price war starts. The cap of $2n$ bids per pass is not in the paper; it bounds the time of this phase by $O(n^2)$, and rows left over go on to the next phase.

**Augmentation** (lines L11 to L19) is a shortest path search from a free row $f$. The length of an arc from column $j$, held by row $i$, to column $j'$ is the reduced cost $c_{ij'} - v_{j'} - u_i \ge 0$, so Dijkstra's method works. The set $R$ holds the columns whose distance is final, and $T$ holds the columns at the current least distance $\mu$. The search stops as soon as a free column has distance $\mu$. Line L18 changes only the prices of the columns in $R$, and line L19 shifts the rows along the path.

## Example

Let
$$C = \begin{pmatrix} 4 & 1 & 3 \\ 2 & 0 & 5 \\ 3 & 2 & 2 \end{pmatrix},$$
with rows and columns numbered 0, 1, 2.

**Column reduction.** Column 2 has least cost 2 at row 2, so $v_2 = 2$ and row 2 gets column 2. Column 1 has least cost 0 at row 1, so $v_1 = 0$ and row 1 gets column 1. Column 0 has least cost 2 at row 1, so $v_0 = 2$, but row 1 already has a column, and column 0 stays free.

**Reduction transfer.** Row 0 was never chosen, so it is free. Row 2 was chosen once: its reduced costs outside column 2 are $3 - 2 = 1$ and $2 - 0 = 2$, so $v_2 \leftarrow 2 - 1 = 1$. Row 1 was chosen twice and is skipped. Now $v = (2, 0, 1)$.

**Augmenting row reduction.** Row 0 has reduced costs $(2, 1, 2)$: best column 1 with $a = 1$, second best $b = 2$. So $v_1 \leftarrow 0 - 1 = -1$, row 0 takes column 1, and row 1 becomes free and bids next. Row 1 has reduced costs $(2 - 2, 0 + 1, 5 - 1) = (0, 1, 4)$: best column 0 with $a = 0$, $b = 1$. So $v_0 \leftarrow 1$, and row 1 takes the free column 0.

All rows are assigned: $x = (1, 0, 2)$ with cost $1 + 2 + 2 = 5$. The prices are $v = (1, -1, 1)$ and $u = (2, 1, 1)$. The duals sum to $4 + 1 = 5$, and $u_i + v_j \le c_{ij}$ holds in all nine entries, so 5 is the minimum.

**The same matrix by augmentation alone.** Skip the row reduction. After the transfer, row 0 is free and $v = (2, 0, 1)$. The search from row 0 starts with $d = (2, 1, 2)$, so $\mu = 1$ and $T = \{1\}$. Column 1 is held by row 1, so column 1 moves to $R$, and row 1 relaxes column 0 to $d_0 = 1 + (2 - 2) - (0 - 0) = 1 = \mu$. Column 0 is free, so the search stops. Line L18 changes nothing, since $d_1 = \mu$. The path is row 0 to column 1, then row 1 to column 0, which gives the same $x = (1, 0, 2)$.

## Correctness

The full proof is below. It rests on the invariant (CS).

- The initialization phases keep (CS): column reduction makes all reduced costs nonnegative and assigns a row only at a zero; lowering the price of a column only raises the reduced costs of other rows at that column, and a bidder lowers the price only as far as its second best value.
- An augmentation keeps (CS) for the rows on the path and off it. This is the standard argument for shortest paths with potentials: after line L18, every arc on the shortest path tree from $f$ is tight, and no reduced cost becomes negative.
- Each augmentation assigns one more row, so after at most $n$ augmentations $x$ is a permutation.
- At the end, for any permutation $\sigma$, $\sum_i c_{i\sigma(i)} \ge \sum_i (u_i + v_{\sigma(i)}) = \sum_i u_i + \sum_j v_j = \sum_i c_{i x_i}$. This is [weak duality](/weak-duality/) for the assignment linear program, with [complementary slackness](/complementary-slackness/) on the chosen pairs.

## Complexity

The model is the [word RAM](/word-ram/) with real or integer costs and unit-cost arithmetic.

- **Column reduction and transfer.** $O(n^2)$: each column and each row is scanned once.
- **Row reduction.** Each bid scans one row in $O(n)$ time, and there are at most $2n$ bids in each of two passes, so $O(n^2)$.
- **One augmentation.** Each column enters $R$ at most once, and each time one row is scanned in $O(n)$ time; finding $\mu$ scans the unfinished columns in $O(n)$ time, at most once per column added to $R$. So one augmentation takes $O(n^2)$ time.
- **Total.** At most $n$ augmentations, so $O(n^3)$ in the worst case. Space $\Theta(n)$ besides the matrix.

The worst case is the same as the Hungarian algorithm's. The gain is in practice: on many random dense instances the initialization leaves few free rows, and each search stops when it first reaches a free column.

## Properties

- **Bipartite and weighted.** The graph is complete bipartite with real weights. For a general graph with weights, use [minimum-weight perfect matching](/minimum-weight-perfect-matching/) algorithms with blossoms.
- **Certificate.** The duals $u$ and $v$ prove optimality and can be checked in $O(n^2)$ time.
- **Exactness.** With integer costs all prices stay integers and the result is exact. With floating point costs the equality tests in lines L14 and L17 should allow a small tolerance.
- **Deterministic.** The result depends on tie breaking; its cost does not.

## Variants and improvements

- **Sparse version (LAPJVsp).** The paper also gives a version for sparse matrices that scans only the existing entries of each row.
- **Rectangular matrices.** Crouse describes a shortest augmenting path method in this style that works directly on $m \times n$ matrices without padding. SciPy's `linear_sum_assignment` uses such a method.
- **Without the initialization.** Lines L11 to L19 alone form the successive [shortest path](/successive-shortest-path/) form of the Hungarian algorithm, $O(n^3)$, which is also the method of [min-cost flow](/min-cost-flow-problem/) on the assignment network.
- **Auction.** The row reduction phase is a short run of Bertsekas' [auction algorithm](/auction-algorithm/) with no minimum increment. A full auction with $\varepsilon$-scaling is an alternative that parallelizes well.

## When to use it

Use it for dense assignment problems with some hundreds to some thousands of rows, such as tracking (assigning detections to tracks), image matching and scheduling. It is the method behind several widely used library routines. For sparse problems with many rows, use the sparse version or a [min-cost flow](/min-cost-flow-problem/) code. For problems where only the size of the matching matters, not its cost, use [Hopcroft-Karp](/hopcroft-karp/).

## Pitfalls

- **Assuming the initialization finishes.** The row reduction can leave free rows; the augmentation phase must always run after it.
- **Price wars on ties.** In line L9, a row that sees two equal best values must not lower a price by 0 and evict the holder; that can cycle. Taking the second column on a tie, as in the paper, avoids this.
- **The case $n = 1$.** A row has no second best column, so the transfer and the bid of lines L6 and L8 are undefined; handle $n \le 1$ apart.
- **Updating all prices.** Line L18 must change only columns in $R$. Columns with tentative distances are not final, and shifting them breaks (CS).
- **Infinite costs for missing edges.** With floating point infinities, differences such as $\infty - \infty$ are undefined. Use a large finite cost instead.

## Implementations

The Python version takes a square list of lists and returns the assignment and the two dual vectors. A parameter sets the number of row reduction passes; with 0 passes, the augmentation phase does all the work, which the tests use to check both phases. The tests compare the cost with a brute force over all permutations for $n \le 6$ and check the dual certificate on larger random matrices.

## History

Kuhn's [Hungarian algorithm](/hungarian-algorithm/) of 1955 solved the assignment problem in polynomial time, and the shortest path form with vertex potentials, due to Tomizawa and to Edmonds and Karp in the early 1970s, gave $O(n^3)$. In 1987 Roy Jonker and Anton Volgenant published LAPJV in the journal Computing. They kept the $O(n^3)$ shortest path method and added column reduction, reduction transfer and an auction-like augmenting row reduction in front of it. Their tests showed it faster than the codes of that time on dense and sparse instances, and it became a standard method for the problem.

## References
