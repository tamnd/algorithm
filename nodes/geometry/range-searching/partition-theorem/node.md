---
tag: M5946F
kind: theorem
slug: partition-theorem
name: Partition theorem
aliases:
- Matousek partition theorem
- simplicial partition theorem
- simplicial partition with low crossing number
area: geometry/range-searching
level: research
summary: Any n points in R^d can be split into r balanced simplicial cells so that a hyperplane crosses only O(r^(1-1/d)) of them.
prereqs: [geometric-cutting, multiplicative-weights-update]
see_also: [partition-tree, partition-tree-query, simplex-range-searching, halfspace-range-searching, geometric-cutting, epsilon-net-theorem, range-searching-lower-bound, shallow-cutting]
sources:
  - paper: doi:10.1007/BF02293051
    title: Jiří Matoušek, Efficient partition trees, Discrete and Computational Geometry 8, 1992, pages 315 to 334
    locator: the partition theorem (simplicial partitions with classes of size between s and 2s and crossing number O(r^(1-1/d))), the test set lemma, and the partition tree built from them
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 16, Section 16.1, Partition trees (fine simplicial partitions in the plane with crossing number O(sqrt r))
  - paper: doi:10.1007/s00454-012-9410-z
    title: Timothy M. Chan, Optimal partition trees, Discrete and Computational Geometry 47(4), 2012, pages 661 to 690
    locator: the hierarchical form of the partition theorem and partition trees with O(n^(1-1/d)) query time
  - paper: doi:10.1007/BF02187743
    title: Bernard Chazelle and Emo Welzl, Quasi-optimal range searching in spaces of finite VC-dimension, Discrete and Computational Geometry 4, 1989, pages 467 to 489
    locator: spanning trees with crossing number O(n^(1-1/d)) built by iterative reweighting (DOI to be checked)
  - paper: doi:10.1145/73393.73397
    title: Emo Welzl, Partition trees for triangle counting and other range searching problems, Proceedings of the 4th Annual Symposium on Computational Geometry, 1988, pages 23 to 33
    locator: spanning paths with low crossing number in the plane and their use for triangle counting (DOI to be checked)
  - paper: doi:10.1145/197405.197408
    title: Jiří Matoušek, Geometric range searching, ACM Computing Surveys 26(4), 1994, pages 421 to 461
    locator: the survey section on simplicial partitions and partition trees (DOI to be checked)
---

The partition theorem of Matoušek (1992) says that any $n$ points in $\mathbb{R}^d$ can be split into about $r$ groups of nearly equal size, each wrapped in a simplex, so that every hyperplane crosses only $O(r^{1-1/d})$ of the simplices. In the plane a line crosses $O(\sqrt{r})$ of the $r$ cells, which is the best possible up to a constant. Applied recursively, the theorem gives the [partition tree](/partition-tree/), a linear space structure for [simplex range searching](/simplex-range-searching/) with query time close to $n^{1-1/d}$. Its proof combines a [cutting](/geometric-cutting/) of a small set of test hyperplanes with iterative reweighting, the geometric form of [multiplicative weights](/multiplicative-weights-update/).

## Statement

**Definitions.** Let $P$ be a set of $n$ points in $\mathbb{R}^d$. A **simplicial partition** of $P$ is a family $\Pi = \{(P_1, \Delta_1), \dots, (P_m, \Delta_m)\}$ in which the classes $P_1, \dots, P_m$ partition $P$ and each $\Delta_i$ is a relatively open simplex, of any dimension from $0$ to $d$, with $P_i \subseteq \Delta_i$. The simplices may overlap. A hyperplane $h$ **crosses** $\Delta_i$ if $h \cap \Delta_i \ne \emptyset$ and $\Delta_i \not\subseteq h$. The **crossing number** of $\Pi$ is the largest number of simplices $\Delta_i$ crossed by one hyperplane.

**Theorem (Matoušek 1992).** For each fixed $d \ge 2$ there is a constant $c_d$ with the following property. Let $P$ be a set of $n$ points in $\mathbb{R}^d$, let $s$ be an integer with $2 \le s < n$, and put $r = n/s$. Then $P$ has a simplicial partition whose classes satisfy
$$s \le |P_i| < 2s \quad \text{for every } i,$$
so that there are $m = \lfloor n/s \rfloor \le r$ classes, and whose crossing number is at most $c_d \, r^{1 - 1/d}$.

**Remarks.** The points need not be in general position. The simplices are relatively open so that a hyperplane that only touches a cell on its boundary does not count; for a relatively open simplex, crossing is the same as having points of the simplex strictly on both sides of $h$. In the plane the bound is $O(\sqrt{r})$. For $d = 1$ the statement is trivial: splitting the sorted points into intervals gives crossing number $1$. Matoušek also showed how to compute such a partition efficiently; see History.

## In plain words

Scatter many dots on a sheet of paper and split them into groups of about the same size, then draw a triangle around each group. A straight line drawn across the sheet passes through some of the triangles. The theorem says that the groups and triangles can always be chosen so that no line, wherever it is drawn, passes through more than a small number of them. With a hundred groups, a line passes through only about ten.

Cutting the sheet into thin vertical strips is a bad choice, because a horizontal line passes through every strip. Squarish groups are much better. The proof builds the groups one at a time and keeps a weight on a few test lines. When a line passes through a new triangle its weight doubles, so later groups learn to avoid the lines that have already been crossed often.

## Proof

Fix $d \ge 2$. Write $C_d$ for the constant of the [cutting lemma](/geometric-cutting/): every multiset of $N$ hyperplanes has, for every $1 \le t \le N$, a $(1/t)$-cutting of size at most $C_d t^d$, that is, at most $C_d t^d$ closed $d$-simplices, possibly unbounded, with disjoint interiors covering $\mathbb{R}^d$ (or a given simplex), each of whose interiors meets at most $N/t$ of the hyperplanes. The proofs of the lemma never use that the hyperplanes are distinct, so they apply to multisets, and hence to hyperplanes with positive integer weights: replacing a hyperplane of weight $w$ by $w$ copies, the interior of each simplex meets hyperplanes of total weight at most $W/t$, where $W$ is the total weight.

**Step 1 (duality).** Write $x = (x', x_d)$ with $x' \in \mathbb{R}^{d-1}$. Map a point $p$ to the hyperplane $p^* = \{y : y_d = p' \cdot y' - p_d\}$, and a non-vertical hyperplane $h = \{x : x_d = a' \cdot x' - a_d\}$ to the point $h^* = a$. For a point $x$ define the affine function $\varphi_x(y) = y_d - x' \cdot y' + x_d$. Then $x$ lies strictly above $h$ exactly when $\varphi_x(h^*) > 0$, that is, when $h^*$ lies strictly above $x^*$, and $x$ lies strictly below $h$ exactly when $\varphi_x(h^*) < 0$. The linear part of $\varphi_x$ is $\psi_x(u) = u_d - x' \cdot u'$.

**Step 2 (the test set lemma).** *Let $1 \le r \le n$. There is a set $T$ of at most $(d + 1) C_d \, r$ hyperplanes such that every simplicial partition $\Pi$ of $P$ whose classes all have at least $n/r$ points satisfies, for every hyperplane $h$,*
$$\kappa_\Pi(h) \le (d + 1) \max_{g \in T} \kappa_\Pi(g) + r^{1 - 1/d},$$
*where $\kappa_\Pi(h)$ is the number of simplices of $\Pi$ crossed by $h$.*

Let $t = r^{1/d}$, so $1 \le t \le n$, and take a $(1/t)$-cutting $\Xi$ of the $n$ dual hyperplanes $P^* = \{p^* : p \in P\}$ of size at most $C_d r$. Each simplex $\sigma$ of $\Xi$ can be written as $\sigma = \{\sum_j \lambda_j v_j + \sum_k \mu_k u_k : \lambda_j, \mu_k \ge 0, \sum_j \lambda_j = 1\}$ with vertices $v_j$ and, if it is unbounded, directions $u_k$; there are at most $d + 1$ of them in all. Put into $T$ the primal hyperplane $v_j^*$ of every vertex, and for every direction $u_k$ with $u_k' \ne 0$ the vertical hyperplane $\{x : u_k' \cdot x' = u_{k,d}\}$, on which $\psi_x(u_k)$ vanishes. This gives at most $(d + 1) C_d r$ hyperplanes.

First let $h$ be non-vertical, and let $\sigma$ be a simplex of $\Xi$ containing $h^*$. Write $h^* = \sum_j \lambda_j v_j + \sum_k \mu_k u_k$, so that $\varphi_x(h^*) = \sum_j \lambda_j \varphi_x(v_j) + \sum_k \mu_k \psi_x(u_k)$ for every $x$. Count the simplices $\Delta_i$ crossed by $h$ in two groups.

- If $\Delta_i$ is crossed by one of the at most $d + 1$ test hyperplanes of $\sigma$, it is counted by the first term.
- Otherwise each test hyperplane $g$ of $\sigma$ either contains $\Delta_i$ or has $\Delta_i$ strictly on one side, because $\Delta_i$ is convex and relatively open. So the sign of each $\varphi_x(v_j)$ and of each $\psi_x(u_k)$ is the same for all $x \in \Delta_i$. Since $h$ crosses $\Delta_i$, there are $x, \bar{x} \in \Delta_i$ with $\varphi_x(h^*) > 0 > \varphi_{\bar{x}}(h^*)$. If none of the constant signs were positive, the combination $\varphi_x(h^*)$ would be at most $0$; so one of them is positive, and likewise one is negative. Hence for every $y \in \Delta_i$ the function $\varphi_y$ takes both signs on $\sigma$: at a vertex $v_j$ with positive sign, or far along a direction $u_k$ with positive sign from any point of $\sigma$, and similarly for the negative sign. By continuity it takes both signs on the interior of $\sigma$, which is convex, so $y^*$ meets the interior of $\sigma$. This holds in particular for every point of $P_i \subseteq \Delta_i$.

At most $n/t$ hyperplanes of $P^*$ meet the interior of $\sigma$, the classes are disjoint, and each has at least $n/r$ points, so the second group has at most $(n/t) / (n/r) = r^{1 - 1/d}$ simplices. This proves the inequality for non-vertical $h$.

If $h$ is vertical, rotate it slightly about a $(d-2)$-flat inside it to a non-vertical $h'$ that keeps every point of the finite set $V$ of all vertices of all $\Delta_i$ that is strictly on one side of $h$ strictly on the same side. A relatively open simplex is crossed by a hyperplane exactly when it has vertices strictly on both sides, so every simplex crossed by $h$ is crossed by $h'$, and $\kappa_\Pi(h) \le \kappa_\Pi(h')$. This proves the lemma.

**Step 3 (the construction).** Let $m = \lfloor n/s \rfloor$, let $T$ be the test set of Step 2 for this $r$, and give every $g \in T$ the weight $w(g) = 1$. Fix a closed simplex $\Sigma$ that contains $P$ in its interior, and put $K = 2^{d+1} C_d$. Set $P' = P$ and repeat for $i = 1, \dots, m - 1$:

1. Let $n_i = |P'| = n - (i - 1) s$ and $W_i = \sum_{g \in T} w(g)$.
2. If $n_i < K s$, let $\Delta_i$ be the interior of $\Sigma$ and $t_i = 1$. Otherwise let $t_i = (n_i / (K s))^{1/d}$ and take a $(1/t_i)$-cutting of $\Sigma$ for $T$ with weights $w$, of at most $C_d t_i^d = n_i/(2^{d+1} s)$ simplices (if $t_i$ exceeds the total weight, a triangulation of the whole arrangement of $T$ inside $\Sigma$ serves, since no hyperplane crosses its cells). Assign each point $p$ of $P'$ to one closed simplex $\sigma$ of the cutting that contains it and to the face $F$ of $\sigma$ whose relative interior contains $p$. There are at most $2^{d+1}$ faces per simplex, so at most $n_i/s$ pairs $(\sigma, F)$, and some pair receives at least $s$ points. Let $\Delta_i$ be the relative interior of that $F$.
3. Let $P_i$ be $s$ points of $P'$ in $\Delta_i$, and remove them from $P'$.
4. Double the weight of every $g \in T$ that crosses $\Delta_i$.

Finally let $P_m = P'$ and $\Delta_m$ the interior of $\Sigma$. The loop leaves $n_m = n - (m - 1) s$ points, and $s \le n_m < 2s$ because $ms \le n < (m + 1) s$; every other class has exactly $s$ points.

**Step 4 (weights).** A test hyperplane that crosses a relatively open $\Delta_i \subseteq \sigma$ has points of $\sigma$ strictly on both sides, so it meets the interior of $\sigma$; when $\Delta_i$ is the interior of $\Sigma$ the bound below is trivial. So the hyperplanes doubled in round $i$ weigh at most $W_i / t_i$ together, and $W_{i+1} \le W_i (1 + 1/t_i)$. In both cases of item 2, $1/t_i \le (K s / n_i)^{1/d}$, and $n_i \ge (m - i + 1) s$. Hence
$$\sum_{i=1}^{m-1} \frac{1}{t_i} \le K^{1/d} \sum_{j=2}^{m} j^{-1/d} \le K^{1/d} \frac{d}{d - 1} \left( m^{1 - 1/d} - 1 \right) \le K^{1/d} \frac{d}{d - 1} \, r^{1 - 1/d},$$
comparing the sum with $\int_1^m x^{-1/d} \, dx$. If $g \in T$ crosses $\kappa$ of $\Delta_1, \dots, \Delta_{m-1}$, its weight at the end is $2^{\kappa}$, and it is at most the final total
$$W_m \le |T| \prod_{i=1}^{m-1} \left( 1 + \frac{1}{t_i} \right) \le |T| \exp\left( \sum_{i=1}^{m-1} \frac{1}{t_i} \right).$$
So $\kappa \le \log_2 |T| + K^{1/d} \frac{d}{d-1} (\log_2 e) \, r^{1 - 1/d}$, and with the last class, every test hyperplane crosses at most $1 + \log_2 ((d+1) C_d r) + K^{1/d} \frac{d}{d-1} (\log_2 e) \, r^{1-1/d} = O(r^{1 - 1/d})$ simplices, since $\log r = O(r^{1 - 1/d})$ for $d \ge 2$.

**Step 5 (all hyperplanes).** Every class has at least $s = n/r$ points, so Step 2 applies and every hyperplane crosses at most $(d + 1) \cdot O(r^{1-1/d}) + r^{1 - 1/d} = O(r^{1 - 1/d})$ simplices. $\blacksquare$

The same proof works for multisets, using the cutting lemma for multisets in Step 2. The only randomness or search is in choosing cuttings, and the cutting lemma has deterministic constructions, which is how Matoušek turns the proof into an algorithm.

## Consequences

- **Partition trees.** Apply the theorem to $P$, then recursively to each class, and store the simplices. A query simplex is bounded by $d + 1$ hyperplanes, so it opens $O(r^{1-1/d})$ children of a node and decides the others at once. With a constant $r$, the visited nodes satisfy $V(n) \le O(r) + c \, r^{1-1/d} V(2n/r)$, which gives $O(n^{1 - 1/d + \varepsilon})$ query time for any fixed $\varepsilon > 0$ with $O(n)$ space; larger $r$ brings the exponent down to $1 - 1/d$ up to polylogarithmic factors. See [partition tree](/partition-tree/) and [the query](/partition-tree-query/).
- **Optimal query time.** Chan (2012) proved a hierarchical version in which the crossing numbers are controlled at all levels at once, and obtained $O(n^{1 - 1/d})$ query time with $O(n)$ space, which matches Chazelle's [lower bound](/range-searching-lower-bound/) $\Omega(n / \sqrt{m})$ in the semigroup model for $m = n$ in the plane, and his bound in higher dimensions up to a logarithmic factor.
- **Spanning trees with low crossing number.** Iterating the theorem down to classes of size $2$ and connecting the classes gives a spanning tree of $P$ in which every hyperplane crosses $O(n^{1 - 1/d})$ edges, the structure of Welzl (1988) and Chazelle and Welzl (1989), who built it directly by the same reweighting.
- **Space and query trade-offs.** Combined with [cuttings](/geometric-cutting/) at the top levels, partition trees give query time about $n / m^{1/d}$ with space $m$ between $n$ and $n^d$, for [simplex](/simplex-range-searching/) and [halfspace](/halfspace-range-searching/) range searching.

## Tightness

**The exponent.** The bound $O(r^{1-1/d})$ cannot be improved in general. Let $n = g^d$ and let $P$ be the grid $\{1, \dots, g\}^d$, and use only the $d g$ axis-parallel hyperplanes $x_k = c$ with $c \in \{1, \dots, g\}$. Take any simplicial partition with classes of size at least $s \ge 2$ and fewer than $2s$. A class whose points take $a_k$ distinct values in coordinate $k$ has $\prod_k a_k \ge s$, so some $a_k \ge s^{1/d}$, and that $a_k \ge 2$. Each of the $a_k$ hyperplanes $x_k = c$ with $c$ between the smallest and largest of these values meets $\Delta_i$ and has points of $\Delta_i$ on both sides, so it crosses $\Delta_i$: for $c$ strictly inside the range, $\Delta_i$ has points on both sides; for $c$ at an end, $\Delta_i$ has a point $p$ with $x_k = c$ and a point beyond it, and since $\Delta_i$ is relatively open the segment from that point through $p$ continues inside $\Delta_i$ to the other side. There are more than $n / (2s)$ classes, so the total number of crossings is more than $(n / (2s)) \, s^{1/d}$, and some one of the $d g = d n^{1/d}$ hyperplanes crosses more than
$$\frac{n^{1 - 1/d} \, s^{1/d - 1}}{2d} = \frac{r^{1-1/d}}{2d}$$
simplices. For the $16 \times 16$ grid with $s = 16$, cutting into $16$ blocks of $4 \times 4$ points gives crossing number $4$ on the axis-parallel lines and $7$ on all $14946$ lines through two grid points (a diagonal), while $16$ vertical strips give $16$.

**The class sizes.** Some slack in the sizes is needed when $s$ does not divide $n$; the theorem keeps it below a factor $2$. Without a lower bound on the class sizes the statement would be empty, since singleton classes in $0$-dimensional simplices are never crossed.

**What the bound looks like.** The constants in the proof are large, and the counts below come from the heuristic builder of the [partition tree](/partition-tree/) page, which uses the reweighting of Step 3 with test lines through pairs of points instead of a cutting. They were computed exactly by script, with closed cells, where a line that touches a cell counts as crossing it; for relatively open cells the counts can only be smaller.

| point set | partition | crossing number | lines tested |
|---|---|---|---|
| $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$, $s = 2$ | reweighting, seed $0$: $\{(2,3), (5,4)\}, \{(7,2), (8,1)\}, \{(6,6), (9,6)\}, \{(3,8), (4,7)\}$ | $2$ | all $28$ through two points |
| the same | sorted by $x$ into pairs | $4$ | all $28$ |
| $256$ random points below $1000$, seed $20251109$, $s = 16$ | reweighting | $10$ (average $5.65$) | $3000$ random lines through two points |
| the same | $4 \times 4$ grid of quantiles | $7$ (average $4.22$) | the same |
| the same | $16$ vertical strips | $16$ (average $10.18$) | the same |
| the same | random classes | $16$ (average $15.2$) | the same |

For the $8$ points, $1$ of the $105$ ways to split them into $4$ pairs has crossing number $2$, the one found by reweighting; $33$ have $3$ and $71$ have $4$. Here $\sqrt{r} = 2$. For the random points, $\sqrt{r} = 4$, and on random points in the plane the simple quantile grid does a little better than the heuristic. The theorem matters for inputs where no fixed grid works, since its bound holds for every point set and every hyperplane.

## History

Willard (1982) introduced partition trees in the plane, with query time about $n^{0.774}$, by cutting the plane with lines into a constant number of regions. Haussler and Welzl (1987) used [epsilon-nets](/epsilon-net-theorem/) to reach query exponents depending on the VC dimension, and Welzl (1988) introduced spanning paths with low crossing number and the iterative reweighting idea, which Chazelle and Welzl (1989) extended to spanning trees with crossing number $O(n^{1-1/d})$ for points and hyperplanes in $\mathbb{R}^d$, and to more general range spaces of finite VC dimension. Matoušek (1992) formulated simplicial partitions, proved the partition theorem with the test set lemma and [cuttings](/geometric-cutting/), and showed how to compute such partitions efficiently, which gave linear space partition trees with query time $n^{1-1/d}$ up to polylogarithmic factors. Chan (2012) proved the hierarchical version and removed the extra factors, with a simple randomized construction in $O(n \log n)$ expected time.

## References
