---
tag: ERC7WZ
kind: problem
slug: approximate-pareto-set
name: Approximate Pareto set
aliases:
- epsilon-Pareto set
- Pareto set approximation
- epsilon-approximate Pareto curve
area: optimization/multi-objective
level: advanced
summary: Find a small set of feasible points such that each feasible point is epsilon-dominated by one of them. A set of polynomial size always exists, even when the Pareto front is exponential.
prereqs: [epsilon-dominance, pareto-front, pareto-optimality]
see_also: [epsilon-indicator, multi-objective-shortest-path, multi-objective-knapsack, fptas, pareto-front-computation, multi-objective-evolutionary-algorithm, benson-algorithm]
sources:
  - paper: doi:10.1109/SFCS.2000.892068
    title: Christos H. Papadimitriou and Mihalis Yannakakis, On the approximability of trade-offs and optimal access of Web sources, Proceedings of the 41st IEEE FOCS, 2000, 86-92
    locator: the existence of an epsilon-Pareto set of polynomial size, and the theorem that one can be built in polynomial time if and only if the GAP problem can be solved in polynomial time
  - paper: doi:10.1162/106365602760234108
    title: Marco Laumanns, Lothar Thiele, Kalyanmoy Deb and Eckart Zitzler, Combining convergence and diversity in evolutionary multiobjective optimization, Evolutionary Computation 10(3), 2002, 263-282
    locator: the box archives for epsilon-approximate and epsilon-Pareto sets, with their convergence and size bounds
  - paper: "Sergei Vassilvitskii and Mihalis Yannakakis, Efficiently computing succinct trade-off curves, Theoretical Computer Science 348(2-3), 2005, 334-356"
    locator: the algorithms for two objectives that return an epsilon-Pareto set at most three times larger than the smallest one
  - paper: "Pierre Hansen, Bicriterion path problems, in Multiple Criteria Decision Making Theory and Application, Lecture Notes in Economics and Mathematical Systems 177, Springer, 1980, 109-127"
    locator: the instance family of the bicriteria shortest path problem with an exponential number of Pareto-optimal paths
---

An approximate Pareto set is a small set of feasible points such that each feasible point is [epsilon-dominated](/epsilon-dominance/) by one of them. The exact [Pareto front](/pareto-front/) of a combinatorial problem can have exponentially many points, but Papadimitriou and Yannakakis (2000) proved that a set of polynomial size always gives a factor $1 + \varepsilon$ in each objective. The problem asks how to find such a set, and how small it can be. Evolutionary methods use the same idea in the box archive of Laumanns, Thiele, Deb and Zitzler (2002), which keeps a bounded set that covers every point seen so far.

## In plain words

Many problems have so many best trade-offs that nobody can list them all, and nobody could read such a list anyway. So we accept a little error. We pick a short list of options such that for each possible option there is one on the list that is almost as good in every cost, within a chosen small tolerance.

Such a short list always exists. Cut each cost range into slices that grow by the tolerance, and keep one good option for each slice of all but one cost. The number of slices grows only slowly with the range of the costs, so the list stays short even when the full set of trade-offs is huge.

The hard parts are to build the list fast, from a description of the problem and not from a list of all options, and to make it as short as possible.

## Definition

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is a population or input size, and $y = f(x) \in \mathbb{R}^p$ is the image of a solution $x$.

**Input.** A feasible set $X$, given implicitly (for example the paths of a graph or the subsets of items of a knapsack), a map $f : X \to \mathbb{R}^p$, and an error $\varepsilon > 0$. Let $Y = f(X)$.

**Output.** A set $A \subseteq X$ such that for each $x \in X$ some $a \in A$ satisfies

$$f_i(a) \le (1 + \varepsilon)\, f_i(x) \quad \text{for } i = 1, \ldots, p$$

in the multiplicative form, for positive objectives. In the additive form the condition is $f_i(a) - \varepsilon \le f_i(x)$. Such a set is an $\varepsilon$-Pareto set. The images $f(A)$ form an $\varepsilon$-approximate Pareto curve.

**Goals.** (1) Find an $\varepsilon$-Pareto set in time polynomial in the input size and in $1/\varepsilon$. (2) Make $\lvert A \rvert$ small: the smallest size over all $\varepsilon$-Pareto sets is $\mathrm{OPT}_\varepsilon$.

## Variants

- **Additive or multiplicative.** A logarithm in each coordinate turns the multiplicative form into the additive form with error $\log(1 + \varepsilon)$, so the two are equal in power for positive objectives. Combinatorial results use the multiplicative form; evolutionary archives often use the additive one on normalized objectives.
- **Explicit input.** $Y$ is a finite list of $N$ points. For $p = 2$ the smallest $\varepsilon$-Pareto subset can then be found exactly (see Known algorithms).
- **Online or stream.** Points arrive one at a time, as the offspring of an evolutionary algorithm, and the method keeps an archive with a size bound that covers all points seen so far.
- **Only Pareto-optimal points.** Some authors ask that $A$ hold only Pareto-optimal solutions. Others accept any feasible solutions in $A$.
- **Smallest set.** Find an $\varepsilon$-Pareto set of size close to $\mathrm{OPT}_\varepsilon$, with a known factor.

## Examples

**A line of points.** Take $Y = \{(t, 10 - t) : t = 0, 1, \ldots, 10\}$, all Pareto-optimal, and the additive error $\varepsilon = 2$. A point $a$ covers $y$ when $a_1 - 2 \le y_1$ and $a_2 - 2 \le y_2$, that is, when $\lvert a_1 - y_1 \rvert \le 2$. Each point covers at most five points, so at least three points are necessary. The set $\{(2, 8), (7, 3), (10, 0)\}$ covers all eleven, so $\mathrm{OPT}_2 = 3$.

**The box archive on the same points.** Feed the eleven points in the order $t = 0, \ldots, 10$ to the box archive of the next section, with $\ell = (0, 0)$ and box index $b(y) = (\lfloor y_1 / 2 \rfloor, \lfloor y_2 / 2 \rfloor)$.

| $t$ | $y$ | $b(y)$ | step | archive after the step |
|---|---|---|---|---|
| 0 | (0, 10) | (0, 5) | L9 | (0, 10) |
| 1 | (1, 9) | (0, 4) | L8 removes (0, 10), L9 | (1, 9) |
| 2 | (2, 8) | (1, 4) | L3, box (0, 4) dominates | (1, 9) |
| 3 | (3, 7) | (1, 3) | L9 | (1, 9), (3, 7) |
| 4 | (4, 6) | (2, 3) | L3 | (1, 9), (3, 7) |
| 5 | (5, 5) | (2, 2) | L9 | (1, 9), (3, 7), (5, 5) |
| 6 to 10 | | | the same pattern | (1, 9), (3, 7), (5, 5), (7, 3), (9, 1) |

The archive ends with five points, one for each box on the anti-diagonal. Each input point $y$ has an archive point $a$ with $a_i < y_i + 2$, but the set is not the smallest: it has five points where three suffice. The archive works without knowing the whole input, and the price is this extra size. With $K = \lfloor 10/2 \rfloor + 1 = 6$ boxes per axis, the size bound below gives $K^{p-1} = 6$.

**An exponential front.** Hansen (1980) gave graphs for the bicriteria [shortest path](/multi-objective-shortest-path/) problem in which the number of Pareto-optimal paths grows exponentially with the number of nodes. In the same way, in a bi-objective [knapsack](/multi-objective-knapsack/) with item $i$ of weight $2^i$ and value $2^i$, each of the $2^n$ subsets has a different image $(w, -v)$ with $w = v$, and no image dominates another. An $\varepsilon$-Pareto set for these instances has polynomial size by the theorem below.

## Known algorithms

**The grid construction (Papadimitriou and Yannakakis, 2000).** Assume that each objective value lies in $[L, U]$ with $0 < L \le U$. Cut $[L, U]$ into the intervals $[L(1 + \varepsilon)^k, L(1 + \varepsilon)^{k+1})$, $k = 0, \ldots, K - 1$, with $K = \lfloor \log_{1+\varepsilon}(U/L) \rfloor + 1$. For each cell of the grid on the first $p - 1$ objectives that holds some image, keep one solution of that cell with the smallest value of $f_p$.

*Proof that this is an $\varepsilon$-Pareto set.* Take $x \in X$, and let $a$ be the solution kept for the cell of $x$. For $i < p$, $f_i(a)$ and $f_i(x)$ lie in one interval, whose ends have the ratio $1 + \varepsilon$, so $f_i(a) < (1 + \varepsilon) f_i(x)$. And $f_p(a) \le f_p(x)$ by the choice of $a$. The set has at most $K^{p-1}$ members. For a combinatorial problem whose objective values are positive rationals with at most $m$ bits, $U / L \le 2^{2m}$ and $K = O(m / \varepsilon)$, so the size is $O((m / \varepsilon)^{p-1})$, which is polynomial for a fixed $p$.

This proves existence. To build the set, one needs to find a good solution in a cell without listing $X$. Papadimitriou and Yannakakis reduce this to the GAP problem; see Reductions.

**Fully polynomial schemes for single problems.** Many [FPTAS](/fptas/) designs for one objective extend to an $\varepsilon$-Pareto set: round the values of the objectives to the grid and run a [dynamic program](/dynamic-programming/) that keeps, for each state, the non-dominated rounded vectors. Warburton (1987) did this for the multi-objective shortest path problem, and Erlebach, Kellerer and Pferschy (2002) for the multi-objective knapsack problem.

**The smallest set for an explicit list, $p = 2$.** Sort the Pareto-optimal points of the list by $y_1$; then $y_2$ decreases. A point $a$ covers the points $y$ with $y_1 \ge a_1 - \varepsilon$ and $y_2 \ge a_2 - \varepsilon$, which is a contiguous run of the sorted list that holds $a$. Both ends of the run move to the right as $a$ moves to the right. So this is interval covering: take the first point not yet covered, and add the point whose run holds it and reaches farthest to the right. The usual exchange argument for interval covering shows that this greedy choice gives $\mathrm{OPT}_\varepsilon$. A dominated input point is covered by any point that covers its dominator, so it needs no care. The cost is $O(N \log N)$ for the sort and $O(N)$ for the scan.

**Smallest set with an oracle, $p = 2$.** Vassilvitskii and Yannakakis (2005) give polynomial algorithms that use a GAP routine and return an $\varepsilon$-Pareto set of size at most $3\, \mathrm{OPT}_\varepsilon$ for two objectives.

**The box archive (Laumanns, Thiele, Deb and Zitzler, 2002).** This is the online method for a stream of points, in the additive form. Fix lower bounds $\ell_i \le y_i$ and let $b(y)_i = \lfloor (y_i - \ell_i)/\varepsilon \rfloor$. Let $g(y)$ be the squared distance from $y$ to the lower corner $\ell + \varepsilon\, b(y)$ of its own box. The archive keeps at most one point per box.

```pseudo id=main
EPS-ARCHIVE-ADD(A, y)
L1  b ← b(y)
L2  if some a ∈ A has b(a) dominating b then
L3      return A                                     ▷ y is covered by a better box
L4  if some a ∈ A has b(a) = b then
L5      if y dominates a, or (a does not dominate y and g(y) < g(a)) then
L6          return A with a replaced by y
L7      return A                                     ▷ keep the old point of the box
L8  remove from A each a with b dominating b(a)
L9  return A ∪ {y}
```

The archive keeps these invariants after each call, for the set $S$ of all points offered so far.

1. *Distinct, non-dominated boxes.* A new box at L9 is not dominated (L2), not equal to an archive box (L4), and does not dominate any box that stays (L8). Line L6 keeps the box set.
2. *Mutually non-dominated points.* If $a$ dominates $a'$, then $b(a) \le b(a')$, because the floor is monotone. The boxes differ by invariant 1, so $b(a)$ dominates $b(a')$, which invariant 1 rules out.
3. *Coverage.* For each $y \in S$ some $a \in A$ has $b(a) \le b(y)$, so $a_i < \ell_i + \varepsilon(b(a)_i + 1) \le \ell_i + \varepsilon(b(y)_i + 1) \le y_i + \varepsilon$. The proof is by induction. At L3, the dominating box covers $y$. At L6 and L7 the box of $y$ stays occupied. At L8 each removed box is dominated by $b$, so a point that it covered is covered by $y$, by the transitivity of $\le$ on boxes. Points covered by boxes that stay keep their cover.
4. *Size.* If $\ell_i \le y_i \le u_i$ and $K = \lfloor (u_i - \ell_i)/\varepsilon \rfloor + 1$ for each $i$, then $\lvert A \rvert \le K^{p-1}$. Two archive boxes that agree on the first $p - 1$ indices differ in the last one, so one would dominate the other. So the projection of the boxes to the first $p - 1$ indices is one-to-one, and it has at most $K^{p-1}$ values.
5. *Only Pareto-optimal points of $S$.* No $z \in S$ dominates an archive point $a$. Two facts give the proof. First, once some archive box strictly dominates a box $B$, some archive box strictly dominates $B$ at all later times, since a box leaves only at L8, for a box that dominates it, or at L6, for the same box. Second, while a box stays occupied, $g$ of its occupant does not increase: L6 needs $g(y) < g(a)$, or $y$ dominates $a$, and then $g(y) < g(a)$ also, because all offsets from the corner are non-negative. Now let $z$ dominate $a$. If $b(z) \ne b(a)$, then $b(z)$ dominates $b(a)$, and by invariant 3 some archive box $\le b(z)$ dominates $b(a)$, against invariant 1. If $b(z) = b(a) = B$, then right after $z$ arrived, either $B$ was strictly dominated by an archive box (then forever, against $a \in A$), or the occupant of $B$ had $g \le g(z)$. Box $B$ cannot become empty later without being strictly dominated, so $g(a) \le g(z)$. But $z$ dominates $a$ with non-negative offsets, so $g(z) < g(a)$, a contradiction.

Each call compares $y$ with all archive points, so it costs $O(p \lvert A \rvert)$ time. Laumanns et al. also give a coarser version that keeps any point of a box, and the multiplicative version with $b(y)_i = \lfloor \log(y_i / \ell_i) / \log(1 + \varepsilon) \rfloor$.

## Bounds

- **Exact fronts are large.** The front can have $2^n$ points, as in the examples. No method that outputs the whole front runs in polynomial time on such instances.
- **Upper bound on size.** $\mathrm{OPT}_\varepsilon \le K^{p-1}$ with $K = \lfloor \log_{1+\varepsilon}(U/L) \rfloor + 1$, by the grid construction.
- **The bound is tight for $p = 2$.** Take $K$ points $y^k = (c^k, c^{K-1-k})$, $k = 0, \ldots, K - 1$, with $1 + \varepsilon < c < (1 + \varepsilon)^{K/(K-1)}$. If $j > k$, then $y^j_1 = c^j \ge c \cdot c^k > (1 + \varepsilon) y^k_1$, so $y^j$ does not cover $y^k$; if $j < k$, the second objective fails in the same way. So each point covers only itself, and $\mathrm{OPT}_\varepsilon = K$. The values lie in $[1, c^{K-1}]$, and the choice of $c$ gives $\lfloor (K - 1) \log_{1+\varepsilon} c \rfloor + 1 = K$, so the grid bound is met exactly.
- **The archive bound is tight for $p = 2$.** One point in each of the $K$ boxes $(k, K - 1 - k)$ of the anti-diagonal gives an archive of $K$ points, since these boxes are mutually non-dominated.
- **The archive is not minimal.** On the line example the archive has five points and $\mathrm{OPT}_2 = 3$. The size bound of invariant 4 holds for any input order, but the size can exceed $\mathrm{OPT}_\varepsilon$.

## Reductions

- **GAP.** Given a vector $r$ and $\varepsilon > 0$, GAP either returns a feasible $x$ with $f(x) \le r$, or reports that no feasible $x$ has $f(x) \le r / (1 + \varepsilon)$. Papadimitriou and Yannakakis proved that an $\varepsilon$-Pareto set can be built in time polynomial in the input size and $1/\varepsilon$ for every $\varepsilon$ if and only if GAP can be solved in such time. One direction calls GAP once per corner of the grid; the other reads the answer to GAP from an $\varepsilon$-Pareto set for a smaller error.
- **Exact versions.** For linear objectives, they also show that GAP is easy when the exact version of the single-objective problem (is there a solution of cost exactly $B$?) has a pseudo-polynomial algorithm. Shortest path, [spanning tree](/multi-objective-minimum-spanning-tree/) and knapsack fit this rule. For matching, the exact version has a randomized pseudo-polynomial algorithm, so the construction is randomized.
- **From an $\varepsilon$-Pareto set to scalar problems.** An $\varepsilon$-Pareto set holds a $(1 + \varepsilon)$-approximate optimum of each monotone function of the objectives that is homogeneous of degree one, such as a weighted sum with non-negative weights or the function $\max_i w_i f_i$ of the [weighted Tchebycheff method](/weighted-tchebycheff-method/) with the reference point at the origin. The proof is one line: $g(f(a)) \le g((1 + \varepsilon) f(x)) = (1 + \varepsilon)\, g(f(x))$.
- **To the [epsilon indicator](/epsilon-indicator/).** For a finite reference set $R$, a set $A$ is an $\varepsilon$-Pareto set of $R$ in the additive sense exactly when $I_{\varepsilon+}(A, R) \le \varepsilon$.

## Applications

- **Decision support.** A short list of options with a known error is easier to show to a decision maker than an exponential front, and the error bound tells how much the list can lose.
- **Archives in evolutionary search.** The box archive bounds the memory of a [multi-objective evolutionary algorithm](/multi-objective-evolutionary-algorithm/) and keeps its convergence guarantee in terms of the points it has seen. The epsilon-MOEA of Deb, Mohan and Mishra (2005) uses it as its archive.
- **Routing and network design.** Bicriteria routing (time and cost, or delay and loss) uses the rounding dynamic programs to get a polynomial list of good routes.
- **Database query optimization.** Papadimitriou and Yannakakis motivated their work by queries to Web sources with trade-offs between cost, time and quality.

## References
