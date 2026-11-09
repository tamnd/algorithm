---
tag: YBVPG7
kind: technique
slug: well-separated-pair-decomposition
name: Well-separated pair decomposition
aliases:
- WSPD
- Callahan-Kosaraju decomposition
- well-separated pairs
area: geometry/proximity
level: research
summary: Decomposition of all point pairs into O(n) well-separated pairs; yields near-linear spanners and fast proximity algorithms.
prereqs: [kd-tree, quadtree, euclidean-distance]
see_also: [geometric-spanner, yao-graph, closest-pair-of-points, all-nearest-neighbors, euclidean-minimum-spanning-tree, bichromatic-closest-pair, approximate-nearest-neighbor, farthest-pair]
sources:
  - paper: doi:10.1145/200836.200853
    title: Paul B. Callahan and S. Rao Kosaraju, A decomposition of multidimensional point sets with applications to k-nearest-neighbors and n-body potential fields, Journal of the ACM 42(1), 1995, 67-90
    locator: the definition of well-separated sets, the fair split tree, the construction of a decomposition with O(s^d n) pairs in O(n log n + s^d n) time, and the applications to all nearest neighbors and n-body simulation
  - book: isbn:9780521815130
    title: Giri Narasimhan and Michiel Smid, Geometric Spanner Networks, Cambridge University Press, 2007
    locator: the chapter on the well-separated pair decomposition (the spanner with stretch (s + 4)/(s - 4), closest pairs, and minimum spanning trees from bichromatic closest pairs)
  - book: isbn:9780821849118
    title: Sariel Har-Peled, Geometric Approximation Algorithms, American Mathematical Society, 2011
    locator: the chapter on well-separated pairs decomposition (construction from a compressed quadtree, spanners, approximate diameter and approximate nearest neighbors)
  - paper: "Paul B. Callahan and S. Rao Kosaraju, Faster algorithms for some geometric graph problems in higher dimensions, Proceedings of the 4th Annual ACM-SIAM Symposium on Discrete Algorithms, 1993, 291-300"
    locator: spanners and minimum spanning trees from the decomposition
---

A well-separated pair decomposition (WSPD) of a set $P$ of $n$ points in $\mathbb{R}^d$ with separation $s > 0$ is a list of pairs of subsets $\{A_1, B_1\}, \ldots, \{A_m, B_m\}$ such that every pair of distinct points $p, q$ is split by exactly one pair, $p \in A_i$ and $q \in B_i$ or the other way round, and in every pair the two sets are far apart compared with their size: they fit in two balls of the same radius $\rho$ whose distance is at least $s\rho$. Callahan and Kosaraju (1995) showed that a decomposition with only $m = O(s^d n)$ pairs always exists and can be built from a split tree in $O(n \log n + s^d n)$ time. So the $\binom{n}{2}$ distances among $n$ points collapse into $O(n)$ groups, and inside each group all distances are equal up to a factor $1 + O(1/s)$. Many proximity problems then reduce to one cheap computation per pair: a [geometric spanner](/geometric-spanner/) with stretch $(s+4)/(s-4)$ from one edge per pair, the [closest pair](/closest-pair-of-points/), [all nearest neighbors](/all-nearest-neighbors/), and the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/).

## In plain words

A cloud of points has a huge number of pairs, growing with the square of the number of points. Seen from far away, a tight group of points looks like a single point: the distance from any point of one far-away group to any point of another is almost the same.

A WSPD lists pairs of clusters that are far apart compared with their own size, so that every pair of points is covered by exactly one listed pair of clusters. Surprisingly, the number of cluster pairs needed grows only in proportion to the number of points.

To answer a question about all point pairs, ask it once per cluster pair instead. For example, linking one point of each cluster to one point of the other gives a network in which every trip is only a little longer than the straight line.

## When it applies

- **Fixed, low dimension.** The number of pairs is $O(s^d n)$; the hidden constant grows exponentially with $d$, so the method is practical for $d$ up to about 3 or 4 and theoretical beyond.
- **Questions that tolerate grouping.** It fits problems where a pair of far, small clusters can be handled by one representative distance (spanners, approximate diameter, approximate distances), or where the answer is forced to lie in a singleton pair or a bichromatic closest pair (closest pair, nearest neighbours, minimum spanning tree).
- **Static point sets.** The decomposition is built once; dynamic and kinetic versions exist but are more involved.

## The template

The decomposition comes from a binary space partition tree $T$ on $P$, usually the fair split tree: each node $u$ holds a subset $P_u$ and its bounding box $R(u)$; an internal node splits $R(u)$ by the hyperplane through the middle of its longest side. Let $c(u)$ be the center of $R(u)$ and $r(u)$ half its diagonal, so the ball of radius $r(u)$ around $c(u)$ contains $P_u$.

```pseudo id=main
WSPD(P, s)
L1  T ← a fair split tree of P
L2  for each internal node u of T do FIND-PAIRS(u.left, u.right)

FIND-PAIRS(v, w)
L3  ρ ← max(r(v), r(w))
L4  if ‖c(v) − c(w)‖ ≥ (s + 2) ρ then
L5    report the pair {v, w}
L6  else
L7    if r(v) < r(w) then swap v and w
L8    FIND-PAIRS(v.left, w); FIND-PAIRS(v.right, w)
```

Line L4 says that the two balls of radius $\rho$ around $c(v)$ and $c(w)$ are at distance at least $s\rho$, which is the well-separation condition; comparing $\|c(v) - c(w)\|^2$ with $(s+2)^2\rho^2$ keeps it exact on rational input. A pair of leaves always passes, because a single point has $r = 0$. So when the test fails, $\rho > 0$, the node with the larger radius is internal, and line L8 can split it; each call splits a node, so the recursion ends. Every pair $p \ne q$ is reported exactly once: at their lowest common ancestor $u$ they are separated into $u.left$ and $u.right$, and each call of line L8 passes $p$ and $q$ to exactly one of its two subcalls. A pair is stored as two tree nodes, not as two lists, because the total size $\sum (|A_i| + |B_i|)$ can be quadratic.

For the seven points $\{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$ used on the [Gabriel graph](/gabriel-graph/) page, which have 21 point pairs, the template gives 9 pairs for $s = 1$, 13 for $s = 2$, 19 for $s = 5$ and 21 singleton pairs for $s = 8$. For $s = 5$ the spanner below has largest stretch about $1.11$, against the guaranteed $(5+4)/(5-4) = 9$.

**The three facts used by the applications.** Let $\{A, B\}$ be a pair with radius $\rho$, $p, a \in A$ and $q, b \in B$. Since $A$ and $B$ lie in balls of radius $\rho$ at distance at least $s\rho$:

1. $\|p - a\| \le 2\rho \le \frac{2}{s} \|p - q\|$: points of the same set are much closer to each other than to the other set.
2. $\|a - b\| \le \|p - q\| + 4\rho \le (1 + \frac{4}{s}) \|p - q\|$: all cross distances agree up to the factor $1 + 4/s$.
3. For $s > 2$, $\|p - a\| < \|p - q\|$.

**Spanner with stretch $(s+4)/(s-4)$.** Take one edge $\{a_i, b_i\}$ per pair, $a_i \in A_i$, $b_i \in B_i$. For $s > 4$ and $t = (s+4)/(s-4)$, every $p, q$ is joined by a path of length at most $t\|p - q\|$. By induction on the distance: let $\{A, B\}$ split $p$ and $q$ with representatives $a, b$. The pairs $p, a$ and $b, q$ are at most $2\rho < \|p - q\|$ apart, so by induction they have paths of length at most $2t\rho$ each, and the whole path $p \leadsto a \to b \leadsto q$ has length at most $4t\rho + \|p - q\| + 4\rho$. This is at most $t\|p - q\|$ when $4\rho(t + 1) \le (t - 1)\|p - q\|$; since $\|p - q\| \ge s\rho$, it suffices that $4(t+1) \le s(t-1)$, that is, $t \ge (s+4)/(s-4)$. To get stretch $1 + \varepsilon$, take $s = 4 + 8/\varepsilon$ (then $(s+4)/(s-4) = 1 + \varepsilon$), which gives $O(\varepsilon^{-d} n)$ edges.

## Classic examples

- **[Closest pair](/closest-pair-of-points/).** For $s > 2$, the closest pair $p, q$ forms a pair of singletons: if $A$ had another point $a$, fact 3 would give $\|p - a\| < \|p - q\|$. So the closest pair is the shortest singleton pair, found in $O(n)$ time after the decomposition.
- **[All nearest neighbors](/all-nearest-neighbors/).** By the same argument, if $q$ is a nearest neighbour of $p$, then the pair that splits them has $A = \{p\}$. Callahan and Kosaraju use this to compute all nearest neighbours, and all $k$ nearest neighbours, in $O(n \log n)$ time in fixed dimension.
- **[Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/).** For $s > 2$, every minimum spanning tree edge $pq$ is a [bichromatic closest pair](/bichromatic-closest-pair/) of the pair $\{A, B\}$ that splits it: otherwise a closer $a \in A$, $b \in B$ would make $pq$ the strictly longest edge of the cycle $p, a, b, q$. So the tree can be found among $O(n)$ candidate edges, and the spanner above gives a $(1 + \varepsilon)$-approximate tree directly.
- **[Geometric spanners](/geometric-spanner/).** The spanner of the template has $O(s^d n)$ edges and stretch $(s+4)/(s-4)$; refinements bound the degree and the weight.
- **Diameter.** If $p, q$ is the [farthest pair](/farthest-pair/) and $a, b$ the representatives of its pair, then $\|a - b\| \ge \|p - q\| - 4\rho \ge (1 - 4/s)\|p - q\|$, so the longest representative edge approximates the diameter within the factor $1 - 4/s$ in $O(s^d n)$ time after the decomposition.
- **n-body simulation.** The force between two far clusters is approximated by one interaction between their centers of mass, as in the fast multipole method; this was the second application in the original paper.

## Variations

- **Building the tree.** A plain fair split tree can have depth $\Theta(n)$, for example for points at positions $2^i$ on a line, and then building it naively takes $\Theta(n^2)$ time. Callahan and Kosaraju build it in $O(n \log n)$ time by a partial construction; a compressed [quadtree](/quadtree/) works as well (Har-Peled).
- **Size bound.** The proof of $O(s^d n)$ is a packing argument: each node $v$ is paired only with nodes of similar size in a region of radius $O(s \cdot r(v))$ around it, and only $O(s^d)$ disjoint such nodes fit there. In practice the constant is moderate in the plane: with the template above, 800 random points in the plane give about 10 pairs per point for $s = 2$, 20 for $s = 4$ and 45 for $s = 8$.
- **Other separation measures.** Some authors use the distance between bounding boxes, or the minimum enclosing balls, instead of the balls around the box centers; the facts change only in their constants.
- **Semi-separated decompositions.** Requiring only that the distance between the sets be large compared with the smaller of the two radii gives decompositions with $O(n)$ pairs whose total set size is $O(n \log n)$ in fixed dimension, which avoids the quadratic total size of a WSPD.
- **Metric spaces.** In [metric spaces](/metric-space/) of bounded doubling dimension, WSPDs with $O(s^{O(\dim)} n)$ pairs exist and are built with net trees.

## Pitfalls

- **Separation too small for the application.** The spanner bound needs $s > 4$ and the closest pair and MST arguments need $s > 2$; with smaller $s$ the decomposition is still valid but the facts used by the applications fail.
- **Storing the sets explicitly.** The total size of all $A_i$ and $B_i$ can be $\Theta(n^2)$, for points spread so that many pairs involve large subtrees. Store tree nodes and enumerate their points only when needed.
- **Duplicate points.** Equal points cannot be separated by any split: the bounding box of a set of equal points has zero size, the midpoint split puts all of them on one side, and the tree construction does not terminate. Remove duplicates first, or treat them separately.
- **Square roots in the separation test.** Testing $\|c(v) - c(w)\| - 2\rho \ge s\rho$ with floating-point roots can misclassify borderline pairs. Compare $\|c(v) - c(w)\|^2$ with $(s + 2)^2 \rho^2$.
- **Deep recursion.** On unbalanced split trees, both the tree construction and FIND-PAIRS recurse to depth $\Theta(n)$; use explicit stacks or the balanced constructions.
- **Exponential dependence on $d$.** The $s^d$ factor makes the decomposition impractical in high dimension, where most pairs of clusters are not well separated.

## References
