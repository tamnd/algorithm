---
tag: CNGG0W
kind: data-structure
slug: partition-tree
name: Partition tree
aliases:
- Willard partition tree
- Matousek partition tree
- simplicial partition tree
area: geometry/range-searching
level: research
summary: Tree whose nodes split the point set into simplicial cells, giving sublinear simplex range queries.
implements: [range-query-structure]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension (fixed), k: the number of reported points, r: the fan-out}
  time: {build: O(n log n) expected, query_count: O(n^(1-1/d)) worst case, query_report: O(n^(1-1/d) + k) worst case}
  space: {total: O(n) worst case}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1982
  people: [Dan E. Willard, Jiří Matoušek, Timothy M. Chan]
  note: Willard built the first partition tree in 1982 with O(n^0.774) query time in the plane; Matoušek's partition theorem (1992) gave O(n^(1-1/d) log^(O(1)) n), and Chan (2012) removed the logarithmic factors.
prereqs: [partition-theorem, simplex-range-searching, convex-hull]
see_also: [partition-tree-query, partition-theorem, simplex-range-searching, halfspace-range-searching, geometric-cutting, kd-tree, range-searching-lower-bound, decomposable-searching-problem]
sources:
  - paper: doi:10.1137/0211012
    title: Dan E. Willard, Polygon retrieval, SIAM Journal on Computing 11(1), 1982, pages 149 to 165
    locator: the first partition tree, with linear space and O(n^0.774) query time for polygon queries in the plane (DOI to be checked)
  - paper: doi:10.1007/BF02293051
    title: Jiří Matoušek, Efficient partition trees, Discrete and Computational Geometry 8, 1992, pages 315 to 334
    locator: the partition theorem, its construction by reweighting a test set, and partition trees with O(n) space and O(n^(1-1/d) log^(O(1)) n) query time (DOI to be checked)
  - paper: doi:10.1007/s00454-012-9410-z
    title: Timothy M. Chan, Optimal partition trees, Discrete and Computational Geometry 47(4), 2012, pages 661 to 690
    locator: partition trees with O(n) space, O(n^(1-1/d)) query time and O(n log n) expected preprocessing (DOI to be checked)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 16, Section 16.1, Partition Trees (fine simplicial partitions in the plane, SELECTINHALFPLANE and the O(n^(1/2+epsilon)) analysis)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.3, partition trees and the space and query trade-off
---

A partition tree stores a set $P$ of $n$ points in $\mathbb{R}^d$ for [simplex range searching](/simplex-range-searching/) in linear space. Each node splits its points into $r$ classes of nearly equal size, each enclosed in a simple cell (a simplex in the theory), such that any hyperplane crosses only a few of the cells. A query simplex is answered by descending the tree: a cell inside the range is counted whole, a cell outside it is skipped, and only the cells that a boundary hyperplane crosses are opened. By Matoušek's [partition theorem](/partition-theorem/) a hyperplane crosses $O(r^{1 - 1/d})$ of the $r$ cells, and this gives query time close to $n^{1 - 1/d}$, so $O(\sqrt{n})$ in the plane with $O(n)$ space; Chan's optimal partition trees reach $O(n^{1 - 1/d})$ exactly, which matches [Chazelle's lower bound](/range-searching-lower-bound/).

## In plain words

A city map has many houses, and someone keeps asking how many houses lie inside a triangle drawn on the map. Checking every house each time is slow.

The partition tree groups the houses into a few neighbourhoods of about the same size, chosen so that any straight road passes through only a few of them. Each neighbourhood is again split into smaller neighbourhoods the same way, and so on.

For a triangle, a neighbourhood that lies fully inside counts all at once, and one fully outside is ignored. Only the neighbourhoods that the edges of the triangle pass through are looked at more closely. Since a straight edge passes through only a few neighbourhoods at each step, the search looks at far fewer groups than there are houses.

## The abstract type

The partition tree is a [range query structure](/range-query-structure/) for a multiset $P$ of $n$ points in $\mathbb{R}^d$. It is static and answers:

- **COUNT$(\Delta)$**: the number of points of $P$ in a closed range $\Delta$, each copy counted;
- **REPORT$(\Delta)$**: those points; with semigroup weights, their sum.

The ranges are simplices, halfspaces, and more generally intersections of $\ell$ closed halfspaces $\{x : a \cdot x \le c\}$, with $\ell = O(1)$.

**Notation.** $n = |P|$; $r$ the fan-out; $b$ the leaf size; $S(v)$ the points stored under node $v$; $C(v)$ the cell of $v$, a convex set containing $S(v)$. A hyperplane $h$ **crosses** a closed convex set $C$ if $h$ meets $C$ and does not contain it. The **crossing number** of a partition into classes with cells $C_1, \dots, C_r$ is the largest number of cells crossed by one hyperplane. The model is the [real RAM](/real-ram/).

**Degenerate input.** No general position is assumed. Points may coincide or be collinear, and the ranges are closed.

## Representation

- **Shape.** A rooted tree. The root holds all of $P$. An internal node $v$ has between $2$ and $r$ children, and the sets $S(w)$ of its children partition $S(v)$ into classes of $s = \lceil |S(v)| / r \rceil$ points, except the last, which has between $s$ and $2s - 1$; when $|S(v)| < 2s$, which happens only for $r < 4$, the node is split into two halves instead. A leaf holds at most $b$ points.
- **Cells.** Each node stores its cell $C(v)$ and the count $|S(v)|$. In Matoušek's tree the cells of the children are simplices, so a node takes $O(1)$ words. The implementation here stores the [convex hull](/convex-hull/) of $S(v)$, as its lower and upper chains, which is the smallest convex cell and lets a cell be tested against a halfplane in $O(\log n)$ time by [binary search](/binary-search/).
- **Points.** The points are kept in one array in the order of a depth-first traversal, so $S(v)$ is a contiguous block and can be reported without walking the subtree.

**Invariant.** (1) The children of $v$ partition $S(v)$, and their blocks partition the block of $v$. (2) $S(v) \subseteq C(v)$, and $C(v)$ is convex. (3) Each class is smaller than its parent, so the depth is $O(\log_{r/2} n)$ for $r \ge 4$.

The quality of the tree is the crossing number of the partition at each node. The [partition theorem](/partition-theorem/) shows that classes with simplicial cells and crossing number $O(r^{1 - 1/d})$ exist. Matoušek finds them by **reweighting**: keep a small test set $T$ of hyperplanes, all with weight $1$; choose each class inside a cell crossed by little weight; then double the weights of the test hyperplanes that cross it. A hyperplane that crosses many classes would have its weight doubled many times, more than the total weight can grow, so no test hyperplane crosses many classes, and every hyperplane is close to a test hyperplane.

## Operations

```pseudo id=main
BUILD(P, r, b)
L1  make the root holding all of P
L2  for each node v with point set S, taken from a stack do
L3      store the cell of v: the convex hull of S
L4      if |S| ≤ b then v is a leaf that keeps S; continue
L5      T ← a test set of lines through pairs of points of S, each with weight 1; s ← ⌈|S|/r⌉, q ← ⌊|S|/s⌋; if q < 2 then s ← ⌊|S|/2⌋, q ← 2
L6      while fewer than q − 1 classes have been made do
L7          draw t lines from T by weight and group the remaining points by their cell in the arrangement of the drawn lines, halving t until some cell holds s points
L8          in each cell holding s points take s points near each other, and keep the set whose hull is crossed by the least total weight of T
L9          double the weight of every line of T that crosses the hull of the kept set; it becomes a class
L10     the remaining points form the last class
L11     make a child of v for each class and push it
```

```pseudo id=query
QUERY(v, Δ)
L12 if the cell of v lies outside one of the halfplanes of Δ then return 0
L13 if the cell of v lies inside Δ then return |S(v)|
L14 if v is a leaf then return the number of points of S(v) in Δ
L15 return the sum of QUERY(w, Δ) over the children w of v
```

The sample size starts at $t = \lfloor \sqrt{m/s} \rfloor$ for $m$ remaining points, so the arrangement of the drawn lines has about $m/s$ cells, each holding about $s$ points; this follows Matoušek, who uses a cutting of the test set. Reporting replaces the count at line L13 by the block of $v$. The query is analysed on its own page, [partition tree query](/partition-tree-query/).

## Example

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ with $r = 4$, $b = 2$ and seed $0$. Here $s = 2$, and BUILD gives a root with four leaf children:

| class | points | cell |
|---|---|---|
| $A$ | $(2,3), (5,4)$ | the segment between them |
| $B$ | $(7,2), (8,1)$ | the segment between them |
| $C$ | $(6,6), (9,6)$ | the segment between them |
| $D$ | $(3,8), (4,7)$ | the segment between them |

Among the $28$ lines through two points of $P$, $3$ cross no class, $3$ cross one class, and $22$ cross two; none crosses three. Of the $105$ ways to split $P$ into four pairs, this is the only one with crossing number $2$ on these lines; $33$ have crossing number $3$ and $71$ have $4$. Pairing the points in order of $x$, $\{(2,3),(3,8)\}, \{(4,7),(5,4)\}, \{(6,6),(7,2)\}, \{(8,1),(9,6)\}$, gives crossing number $4$: a horizontal line crosses all four strips. All these counts were checked by the tests.

COUNT for the closed halfplane $x - y \ge 1$ classifies the four cells:

- $A$ is crossed, since $(2,3)$ has $x - y = -1$ and $(5,4)$ has $x - y = 1$; the leaf is scanned and $(5,4)$, on the boundary line, is counted;
- $B$ is inside, with $x - y = 5$ and $7$; both points count at once;
- $C$ is crossed, with $x - y = 0$ and $3$; the scan counts $(9,6)$;
- $D$ is outside, with $x - y = -5$ and $-3$.

The answer is $4$: the points $(5,4), (7,2), (8,1), (9,6)$, found with $5$ node visits.

**Larger inputs.** For $256$ random points with integer coordinates below $1000$ (seed $20251109$), one partition into $r = 16$ classes of $16$ points by reweighting had crossing number $10$ on $3000$ random lines through two points, $5.6$ on average; sorting by $x$ into $16$ vertical strips gives $16$. On random points with $r = 16$ and $b = 16$, a halfplane query with a boundary line through two random points cost on average $191$ node visits and scanned points for $n = 1024$ and $2443$ for $n = 65536$: a factor $12.8$ for $64$ times as many points, where $\sqrt{64} = 8$.

## Correctness

**Key invariant.** Every point of $S(v)$ lies in the cell $C(v)$, and the children's sets partition $S(v)$. If $C(v)$ lies outside a halfplane of $\Delta$, so do all points of $S(v)$, and line L12 is right to return $0$; if $C(v)$ lies inside $\Delta$, so does $S(v)$, and line L13 is right to return $|S(v)|$. Otherwise the answer is the sum over the children, by the partition property, or a direct count at a leaf. Each class is smaller than its parent, so BUILD terminates. The test of a cell against a halfplane needs the smallest and largest value of a linear function over a convex polygon, which binary search on the upper or lower chain finds. The full proof, with the bound on the number of visited nodes, is in [the correctness proof](proofs/correctness/).

## Complexity

| structure or operation | cost | case |
|---|---|---|
| space, Matoušek and Chan (simplicial cells) | $O(n)$ | worst case |
| build, Matoušek (1992) | $O(n \log n)$ for the structure with $O(n^{1 - 1/d} \log^{O(1)} n)$ query | worst case |
| build, Chan (2012) | $O(n \log n)$ | expected |
| COUNT, Matoušek (1992) | $O(n^{1 - 1/d} \log^{O(1)} n)$ | worst case |
| COUNT, Chan (2012) | $O(n^{1 - 1/d})$, so $O(\sqrt{n})$ in the plane | worst case |
| REPORT | the COUNT bound plus $O(k)$ | worst case |
| space, this implementation | $O(n)$ nodes and $O(n \log_r n)$ hull vertices | worst case |
| build, this implementation, $r \ge 4$ fixed | $O(r n \log_r n \, (\lvert T \rvert + \log n))$ | worst case |
| COUNT, this implementation, crossing number at most $\kappa \ge 2$ at every node | $O(r (n/b)^{\log(\ell \kappa) / \log(r/2)} \ell \log n)$ plus $b$ per scanned leaf | worst case |

The query bound comes from a recurrence. A visited node that is neither inside nor outside $\Delta$ has a cell crossed by one of the $\ell$ boundary lines, and each line crosses at most $\kappa$ children of a node, so at most $\ell \kappa$ children are opened, each with fewer than $2 \lceil m/r \rceil$ points. Hence $V(m) \le 1 + r + \ell \kappa \, V(2 \lceil m/r \rceil)$, and with $\kappa = O(\sqrt{r})$ in the plane the exponent $\log(\ell \kappa) / \log(r/2)$ tends to $1/2$ as $r$ grows: for every $\varepsilon > 0$ a large enough constant $r$ gives $O(n^{1/2 + \varepsilon})$, the bound in de Berg et al. Matoušek takes $r$ growing with $n$ to reach $n^{1/2} \log^{O(1)} n$, and Chan builds the partitions of all levels together so that the crossing numbers of the levels multiply without loss.

## Variants

- **Willard's tree.** Two lines split the plane into four quadrants with $n/4$ points each (a ham sandwich cut), and any line misses one quadrant, which gives $O(n^{\log_4 3})$; Willard refined this to $O(n^{0.774})$.
- **Conjugation trees and spanning trees.** Edelsbrunner and Welzl improved the exponent in the plane with conjugation trees; Chazelle and Welzl used spanning trees with low crossing number, which lead to $O(\sqrt{n} \log n)$ in the plane.
- **Optimal partition trees.** Chan (2012) builds the whole hierarchy at once, with a refinement step that keeps the crossing number of every hyperplane under control level by level, and reaches $O(n^{1 - 1/d})$ query time in linear space with a randomized $O(n \log n)$ construction.
- **Multi-level trees.** A node stores a secondary structure on its set $S(v)$, for example a partition tree on another coordinate system; this answers simplex queries one halfspace per level, and queries on segments and triangles, at a polylogarithmic factor.
- **Trade-offs.** Replacing the top levels by [cuttings](/geometric-cutting/) gives $O((n / m^{1/d}) \log^{O(1)} (m/n))$ query time with $O(m)$ space.
- **Dynamic.** Counting is a decomposable problem, so the [logarithmic method](/decomposable-searching-problem/) supports insertions with an $O(\log n)$ factor on the update time, and partial rebuilding handles deletions; see [dynamic range searching](/dynamic-range-searching/).

## When to use it

Use a partition tree for counting or reporting points in triangles, halfplanes or other polygonal ranges when the space must be linear and the queries are not axis-parallel; for boxes use a [range tree](/range-tree/) or a [kd-tree](/kd-tree/). A kd-tree also answers slanted queries correctly and is simpler, and on typical data it is often fast enough, but its $O(n^{1 - 1/d})$ guarantee holds for axis-parallel boundaries only. For halfplane reporting in the plane, convex layers or [shallow cuttings](/shallow-cutting/) give $O(\log n + k)$ instead, and with much more space [cuttings](/geometric-cutting/) give logarithmic query time.

## Pitfalls

- **Open cells.** The ranges are closed and points may lie on the boundary of a cell. A cell must be tested in the closed sense: it is outside only if every point of it violates the constraint strictly, as at line L12.
- **Larger cells.** Matoušek's simplices may be much larger than the hulls of their classes; the analysis counts crossings of the simplices, so a structure with bigger cells is correct but may visit more nodes.
- **A node that does not split.** If $|S| < 2s$, taking classes of $s$ points would leave the node with one child equal to itself, an endless loop; line L5 splits such a node into two halves.
- **Point sets in convex position.** The hull of a class can have as many vertices as the class, so testing it by scanning its vertices costs $O(n)$ at the root. Test cells by binary search on the chains, or store triangles.
- **Expecting the crossing bound from a heuristic.** A greedy choice of classes without reweighting, or with a poor test set, can produce cells that every line of a family crosses, as the vertical strips in the example show.

## Implementations

## History

Dan Willard (1982) introduced partition trees in his paper on polygon retrieval, with linear space and $O(n^{0.774})$ query time in the plane. Edelsbrunner and Welzl (1986) improved the exponent with conjugation trees. Haussler and Welzl (1987) used [epsilon-nets](/epsilon-net-theorem/) to build partition trees in every dimension, and Chazelle and Welzl (1989) introduced spanning trees with low crossing number. Matoušek (1992) proved the [partition theorem](/partition-theorem/) and gave linear-space trees with $O(n^{1 - 1/d} \log^{O(1)} n)$ query time; together with Chazelle's lower bound this settled the problem up to logarithmic factors. Chan (2012) removed those factors with optimal partition trees.

## References
