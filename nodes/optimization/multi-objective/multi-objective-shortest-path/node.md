---
tag: BMDG74
kind: problem
slug: multi-objective-shortest-path
name: Multi-objective shortest path
aliases:
- Multi-criteria shortest path
- Pareto shortest paths
- bicriteria shortest path
- constrained shortest path
- multicriteria shortest path
- bi-objective shortest path
area: optimization/multi-objective
level: advanced
summary: Find all Pareto optimal paths between two vertices when edges carry several costs.
prereqs: [shortest-path, dijkstra, pareto-front]
see_also: [constrained-shortest-path, multi-objective-minimum-spanning-tree, multi-objective-knapsack, approximate-pareto-set, k-shortest-paths, weighted-sum-method, pareto-front-computation]
sources:
  - paper: doi:10.1007/978-3-642-48782-8_9
    title: Pierre Hansen, Bicriterion path problems, in Multiple Criteria Decision Making Theory and Application, Lecture Notes in Economics and Mathematical Systems 177, Springer, 1980
    locator: pages 109 to 127 (a family of graphs with an exponential number of efficient paths, and approximation)
  - paper: doi:10.1016/0377-2217(84)90077-8
    title: Ernesto Queirós Vieira Martins, On a multicriteria shortest path problem, European Journal of Operational Research 16(2), 1984
    locator: pages 236 to 245 (the label-setting algorithm for all efficient paths)
  - paper: doi:10.1287/opre.35.1.70
    title: Arthur Warburton, Approximation of Pareto optima in multiple-objective, shortest-path problems, Operations Research 35(1), 1987
    locator: pages 70 to 79 (fully polynomial approximation schemes for the Pareto set)
  - paper: doi:10.1109/SFCS.2000.892068
    title: Christos H. Papadimitriou and Mihalis Yannakakis, On the approximability of trade-offs and optimal access of Web sources, FOCS 2000
    locator: pages 86 to 92 (epsilon-approximate Pareto sets of polynomial size, and their construction for shortest paths)
  - paper: doi:10.1016/j.cor.2008.02.002
    title: Andrea Raith and Matthias Ehrgott, A comparison of solution strategies for biobjective shortest path problems, Computers and Operations Research 36(4), 2009
    locator: pages 1299 to 1331 (label-setting, label-correcting and two-phase methods compared)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: problem ND30 in the appendix (shortest weight-constrained path)
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 9 (multicriteria shortest path problems, intractability and label algorithms)
---

The multi-objective shortest path problem asks for all [Pareto optimal](/pareto-optimality/) paths from a source $s$ to a target $t$ in a graph whose arcs carry $p \ge 2$ costs, such as travel time and price. With one cost it is the [shortest path](/shortest-path/) problem that [Dijkstra's algorithm](/dijkstra/) solves. With two costs the [Pareto front](/pareto-front/) can have exponentially many points (Hansen, 1980), so no algorithm lists it in polynomial time, and even the question whether one path meets two bounds is NP-complete. The label-setting method of Martins (1984) computes the whole front in time polynomial in its size, and [approximate Pareto sets](/approximate-pareto-set/) of polynomial size can be computed in polynomial time.

## In plain words

You want to travel from one city to another. Each road has a driving time and a toll. The fastest route has high tolls, and the cheapest route is slow. A route is a good candidate if no other route is both faster and cheaper. The task is to list all good candidates, one route for each pair of time and toll.

The list can be huge. A road network with a few dozen junctions can already have millions of good candidates. So exact methods are practical only when the list is small, and in other cases one asks for a short list that comes close to every good candidate.

## Definition

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p$, and $y = f(x)$ is the image of $x$. Here $x$ is a path and $f(x)$ is its cost vector.

**Input.** A directed graph $G = (V, A)$ with $n$ vertices and $m$ arcs, a source $s$, a target $t$, and a cost vector $c(a) \in \mathbb{R}^p$ with $c(a) \geqq 0$ for each arc $a$. The cost of a path $x$ is $f(x) = \sum_{a \in x} c(a)$.

**Output.** The nondominated set $Y_N$ of $\{f(x) : x \text{ an } s\text{-}t \text{ path}\}$, with one path $x$ for each $y \in Y_N$, so that $f(x) = y$. Some versions ask for all Pareto optimal paths, which can be more than one path for each point.

Because the costs are nonnegative, a cycle never lowers any objective. So every point of $Y_N$ is the cost of a simple path, and the answer is the same for paths and for walks. With negative costs and cycles, the problem changes; see the variants.

## Variants

- **One to all.** The front from $s$ to every vertex. The label-setting method computes it at no extra cost.
- **Bi-objective.** The case $p = 2$, studied most, with its own two-phase methods.
- **Constrained shortest path.** Minimize $f_1$ subject to $f_2(x) \le B$. This is one solve of the [epsilon-constraint method](/epsilon-constraint-method/), and a problem of its own; see [constrained shortest path](/constrained-shortest-path/). It is NP-hard (Garey and Johnson, problem ND30).
- **Weighted sum.** Minimize $\sum_i \lambda_i f_i(x)$ with $\lambda > 0$. This is a shortest path with the arc costs $\sum_i \lambda_i c_i(a)$, solved by Dijkstra's algorithm. It finds only the supported points of the front; see the [weighted sum method](/weighted-sum-method/).
- **Lexicographic.** Order the objectives and compare cost vectors lexicographically. Dijkstra's algorithm works with this order, because nonnegative vectors added to a cost never make it lexicographically smaller. See [lexicographic optimization](/lexicographic-optimization/).
- **Undirected graphs, time-dependent costs, and graphs with negative costs but no negative cycles in any objective.** Label-correcting methods handle these.

## Examples

Take the vertices $s, u, v, t$ and the arcs with these costs:

| arc | $su$ | $sv$ | $uv$ | $ut$ | $vt$ | $st$ |
|---|---|---|---|---|---|---|
| cost | $(1, 1)$ | $(4, 2)$ | $(0, 5)$ | $(7, 1)$ | $(1, 3)$ | $(9, 9)$ |

The four $s$-$t$ paths have the costs $suvt = (2, 9)$, $svt = (5, 5)$, $sut = (8, 2)$ and $st = (9, 9)$. The last one is dominated by $svt$. So $Y_N = \{(2, 9), (5, 5), (8, 2)\}$. The vertex $v$ has two nondominated labels, $(4, 2)$ from $sv$ and $(1, 6)$ from $suv$. A method that keeps one label for each vertex, as Dijkstra's algorithm does, must lose one of them and with it a point of the front.

**Exponentially many points.** Take a chain of $k$ diamonds. Diamond $i$, for $i = 0, \ldots, k-1$, joins $v_i$ to $v_{i+1}$ by two paths of two arcs each, one with total cost $(2^i, 0)$ and one with $(0, 2^i)$. An $s$-$t$ path from $v_0$ to $v_k$ picks one side in each diamond. If $S$ is the set of diamonds where it takes the first side, its cost is $(\sigma, 2^k - 1 - \sigma)$ with $\sigma = \sum_{i \in S} 2^i$. The $2^k$ subsets give $2^k$ different values of $\sigma$, and all costs lie on the line $y_1 + y_2 = 2^k - 1$, so no cost dominates another. The graph has $3k + 1$ vertices and $4k$ arcs, and its front has $2^k$ points. This is the construction of Hansen (1980), and the implementation checks it for $k \le 10$.

## Known algorithms

**Label setting.** Martins (1984) extends Dijkstra's algorithm. A label is a cost vector at a vertex with a pointer to the label it came from. Each vertex keeps a set of labels, not one value. The method always takes the temporary label that is least in the lexicographic order, makes it permanent, and extends it along the arcs out of its vertex.

```pseudo id=main
MARTINS(G, s, t)                         ▷ arc costs c(v, w) ≧ 0 in all p objectives
L1  make the label (0, s, nil) temporary; no vertex has a permanent label
L2  while some label is temporary do
L3      ℓ = (y, v, ·) ← the temporary label with the lexicographically least cost
L4      make ℓ permanent at v
L5      for each arc (v, w) do
L6          y′ ← y + c(v, w)
L7          if no label at w, permanent or temporary, has a cost ≦ y′ then
L8              delete each temporary label at w whose cost is ≧ y′
L9              make the label (y′, w, ℓ) temporary
L10 return, for each permanent label at t, its cost and the path traced back through the labels
```

On the example, the permanent labels appear in the order $s(0, 0)$, $u(1, 1)$, $v(1, 6)$, $t(2, 9)$, $v(4, 2)$, $t(5, 5)$, $t(8, 2)$. The label $t(9, 9)$ made from $s$ is deleted in line L8 when $u$ makes $t(8, 2)$.

**Why it is correct.** Two facts carry the proof. First, once a label with cost $u$ exists at a vertex $w$, some label at $w$ has a cost $\leqq u$ from then on, because line L8 deletes a label only for a new one that is $\leqq$ it. Second, let $x = (s = v_0, \ldots, v_r)$ be a path with cost $z$, and let $i$ be the last index such that some permanent label at $v_i$ has a cost $\leqq$ the cost $z_i$ of the prefix of $x$ up to $v_i$. If $i < r$, that label was extended along the arc $(v_i, v_{i+1})$, so some label at $v_{i+1}$ now has a cost $\leqq z_{i+1}$. It is not permanent by the choice of $i$, so it is temporary, and its cost is lexicographically at most $z_{i+1} \leqq z$.

Now let a label with cost $y$ at $v$ become permanent, and suppose a path to $v$ has a cost $z \leqq y$ with $z \ne y$, so $z$ is lexicographically less than $y$. If $i < r$, the temporary label above is lexicographically less than $y$, so line L3 would take it first. If $i = r$, a permanent label at $v$ has a cost $\leqq z \leqq y$, and line L7 or line L8 would have removed the label $y$. So each permanent label is nondominated, and two permanent labels at one vertex have different costs. At the end no label is temporary, so the same argument gives $i = r$ for every path: each point of $Y_N$ is the cost of a permanent label at $t$. The path traced back from a permanent label is simple, because a repeated vertex would carry a permanent label with a cost $\leqq$ the later one.

**Cost.** Each permanent label at $v$ is a different point of the front from $s$ to $v$, so the number of permanent labels is at most $\sum_v |Y_N(s, v)|$. Each permanent label creates at most one label for each arc out of its vertex, and each new label is compared with the labels at its head vertex. So the time is polynomial in $n$, $m$ and the total size of the fronts, but this size can be exponential in $n$.

**Other exact methods.**

- **Label correcting.** Take any temporary label, not the least one, as in the Bellman-Ford algorithm. A label can then be deleted after it was extended. This works with negative arc costs when no cycle has a negative cost in any objective.
- **Two-phase methods for $p = 2$.** Phase one finds the supported extreme points by a dichotomic search with weighted sums, each one a Dijkstra run. Phase two searches each triangle between two neighboring supported points, for example with [k shortest paths](/k-shortest-paths/) for the weighted sum, or with labels that are cut by the triangle. Raith and Ehrgott (2009) compare these methods with label setting and label correcting.
- **Epsilon constraint.** Solve a sequence of [constrained shortest path](/constrained-shortest-path/) problems, each one NP-hard but often easy in practice.

**Approximation.** Hansen (1980) and Warburton (1987) give fully polynomial approximation schemes: for each $\varepsilon > 0$ they find in time polynomial in the input size and $1/\varepsilon$ a set of paths such that each point of $Y_N$ is within the factor $1 + \varepsilon$ in each objective of the cost of a found path. Papadimitriou and Yannakakis (2000) show that such a set of polynomial size exists for every multi-objective problem with positive costs, and that it can be computed in polynomial time for shortest paths, because the exact version of the problem ("is there a path of cost exactly $B$?") has a pseudo-polynomial algorithm.

## Bounds

- **Size of the front.** Hansen's diamonds give $2^k$ points with $n = 3k + 1$ vertices, so $|Y_N| = 2^{\Omega(n)}$ in the worst case, for $p = 2$ already. Any exact method needs exponential time on these graphs, only to write the answer.
- **Pseudo-polynomial size.** For $p = 2$ and integer costs in $\{0, \ldots, C\}$, the points of $Y_N$ have different first coordinates, each in $\{0, \ldots, (n-1) C\}$, so $|Y_N| \le (n - 1) C + 1$. For $p$ objectives the same argument gives $|Y_N| \le ((n-1) C + 1)^{p-1}$. So the label-setting method runs in pseudo-polynomial time for a fixed $p$.
- **Hardness of one point.** The question "is there an $s$-$t$ path $x$ with $f_1(x) \le B_1$ and $f_2(x) \le B_2$?" is NP-complete (Garey and Johnson, problem ND30). So it is NP-hard to decide whether some point of the front is $\leqq$ a given vector.
- **Approximation.** For fixed $p$ and $\varepsilon > 0$, an $\varepsilon$-approximate Pareto set of size polynomial in the input size and $1/\varepsilon$ exists and can be found in polynomial time (Warburton, 1987; Papadimitriou and Yannakakis, 2000).

## Reductions

- **To single-objective shortest path.** The weighted sum and the lexicographic version are single shortest path problems with changed arc costs or a changed order. They give some points of the front, but not all.
- **From partition and knapsack.** The constrained version contains [subset sum](/subset-sum-problem/): a chain of diamonds where side $i$ costs $(a_i, 0)$ or $(0, a_i)$ has a path with cost $\leqq (T, \sum_i a_i - T)$ exactly when some subset sums to $T$. This is the same chain as in the example, with general numbers.
- **To multi-objective knapsack.** Conversely, a bi-objective 0-1 knapsack problem is a bi-objective path problem in a layered acyclic graph with one layer for each item; see [multi-objective knapsack](/multi-objective-knapsack/).
- **To finite Pareto filtering.** Each step of the label methods keeps the nondominated labels at a vertex, which is [Pareto front computation](/pareto-front-computation/) on a small set.

## Applications

- **Route planning.** Car and bicycle routing with time, distance, tolls or climb; public transport with travel time, price and number of changes.
- **Hazardous materials.** Routes that trade the length against the number of people exposed along the way.
- **Telecommunication networks.** Routes with low delay and low cost, or with many constraints on quality of service.
- **Subproblems.** Resource-constrained shortest paths in column generation for vehicle routing and crew scheduling use the same labels, with resources in place of objectives.

## References
