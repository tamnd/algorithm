---
tag: 2746FY
kind: data-structure
slug: gnat
name: Geometric near-neighbor access tree
aliases:
- GNAT
- geometric near-neighbor access tree
- GNAT
area: searching/similarity-search
level: research
summary: A metric index that splits each node by several well-spread split points and stores distance ranges.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of points, m: the number of split points per node, h: the height of the tree, E: the time of one distance evaluation}
  time: {build: O(n m h E), range: O(n E), nearest: O(n E)}
  space: {total: O(n m)}
history:
  year: 1995
  people: [Sergey Brin]
  note: Brin described the geometric near-neighbor access tree at VLDB 1995 as a generalization of the generalized hyperplane tree to m split points per node, with a table of distance ranges between split points and subtrees.
prereqs: [metric-space, triangle-inequality]
see_also: [ball-tree, vantage-point-tree, cover-tree, m-tree, bk-tree, pivot-based-indexing, metric-space-indexing, fixed-radius-near-neighbors]
sources:
  - url: https://www.vldb.org/conf/1995/P574.PDF
    title: Sergey Brin, Near neighbor search in large metric spaces, Proceedings of the 21st International Conference on Very Large Data Bases (VLDB), 1995
    locator: pages 574 to 584 (the GNAT, the choice of split points far apart, the range table range(p_i, D_j), and the search that removes split points whose range interval does not meet [d − r, d + r])
  - paper: doi:10.1016/0020-0190(91)90074-R
    title: Jeffrey K. Uhlmann, Satisfying general proximity/similarity queries with metric trees, Information Processing Letters 40(4), 1991
    locator: pages 175 to 179 (the generalized hyperplane tree, which splits by the nearer of two pivots)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 5, GNAT among the indexes based on clustering, with its range table and search)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, Section 4.5 (distance-based indexing, with generalized hyperplane partitioning and GNAT)
---

A geometric near-neighbor access tree (GNAT) is a tree for points of a [metric space](/metric-space/) in which each node picks $m$ split points far apart, assigns every other point to its nearest split point, and stores for every pair $(i, j)$ the interval of distances from split point $p_i$ to the points of group $j$. A query at distance $d$ from $p_i$ discards group $j$ when the interval $[d - r, d + r]$ misses the stored interval, which is safe by the [triangle inequality](/triangle-inequality/). It generalizes the two-pivot generalized hyperplane tree of Uhlmann to $m$ pivots and was introduced by Brin in 1995. Storage is $O(nm)$ for the $m^2$ ranges per node, and searches take $O(n)$ distance evaluations in the worst case but far fewer when the data have low [intrinsic dimension](/intrinsic-dimensionality/).

## In plain words

Pick a few points that are far apart from each other, the split points. Every other point joins the team of its closest split point. Then, for each split point and each team, write down how far the split point is from the nearest and the farthest member of that team.

To find all points close to a query, measure the distance from the query to one split point. If a team's recorded band of distances from that split point is far from the query's distance, no member of that team can be close to the query, and the whole team is skipped. Measure the next split point and skip more teams. Search inside the teams that are left in the same way.

## The abstract type

A static similarity index over a finite set $S$ in a metric space $(M, \delta)$, with:

- **range**$(q, r)$: all $x \in S$ with $\delta(q, x) \le r$, exactly, as in [fixed-radius near neighbors](/fixed-radius-near-neighbors/).
- **nearest**$(q)$: a point of $S$ nearest to $q$, exactly.

Only the distance function is used; no coordinates are needed.

## Representation

A node holds either a bucket of at most $b$ points (a leaf), or:

- split points $p_1, \dots, p_k$ with $k = \min(m, |S|)$;
- the groups $D_1, \dots, D_k$: each other point $x$ is in the group $D_j$ of its nearest split point (ties to the smaller $j$);
- the range table: for all $i, j$,
$$\text{range}(i, j) = \Big[\min_{x \in D_j \cup \{p_j\}} \delta(p_i, x),\ \max_{x \in D_j \cup \{p_j\}} \delta(p_i, x)\Big];$$
- a child subtree for each nonempty $D_j$.

Every point is a split point at one node or in one leaf bucket. A node with $k_t$ split points stores $k_t^2 \le m k_t$ intervals, and $\sum_t k_t \le n$, so the range tables take $O(nm)$ space in all.

## Operations

```pseudo id=main
BUILD(S)
L1  if |S| ≤ b then return a leaf with the bucket S
L2  choose split points p_1, ..., p_k: p_1 is any point, then repeatedly the point farthest from those chosen
L3  put each other x ∈ S into D_j for the j with the least δ(x, p_j)
L4  for all i, j: range(i, j) ← [min, max] of δ(p_i, x) over x ∈ D_j ∪ {p_j}
L5  for each j, child_j ← BUILD(D_j)
```

Line L2 is the farthest-first traversal: it spreads the split points so that the groups are compact. Line L3 reuses the distances of line L2 and computes the rest, $O(|S| m)$ evaluations. Line L4 needs no new distances except between split points.

```pseudo id=range
RANGE(t, q, r)
L6  if t is a leaf then report each x in the bucket with δ(q, x) ≤ r; return
L7  P ← {1, ..., k}                                          ▷ the groups still alive
L8  for each i ∈ P, in order: d_i ← δ(q, p_i); report p_i if d_i ≤ r
L9    remove from P every j with [d_i − r, d_i + r] ∩ range(i, j) = ∅
L10 for each j ∈ P: RANGE(child_j, q, r)
```

When $j$ is removed at line L9, both the group $D_j$ and the split point $p_j$ are skipped, since the range covers $p_j$ too. So a removed split point is never measured at line L8.

**Nearest neighbor** runs the same procedure with $r$ equal to the best distance found so far, which shrinks during the search:

```pseudo id=nearest
NEAREST(t, q)                                                 ▷ best = (δ*, x*), starting at (∞, none)
L11 as lines L7 to L9, with r ← δ* updated after each measured split point
L12 visit the live groups in increasing order of d_j; skip group j if max over measured i of (d_i − max range(i, j), min range(i, j) − d_i) > δ*
```

The test of line L12 is a lower bound on $\delta(q, x)$ for every $x$ in group $j$, recomputed with the current $\delta^*$, which may have shrunk since line L11.

## Example

Ten points in the plane with the Euclidean distance, $m = 3$ and buckets of at most $b = 2$ points:

$$(0,0), (1,1), (9,0), (8,1), (0,9), (1,8), (5,5), (9,9), (2,3), (7,6).$$

Line L2 starts at $(0, 0)$, then takes the farthest point $(9, 9)$, then the point farthest from both, $(9, 0)$ at distance 9. The groups are $D_1 = \{(1,1), (0,9), (1,8), (2,3)\}$ (the point $(0, 9)$ is at distance 9 from both $(0, 0)$ and $(9, 9)$, and the tie goes to $j = 1$), $D_2 = \{(5,5), (7,6)\}$ and $D_3 = \{(8,1)\}$. The range table, rounded to two places:

| | $D_1 \cup \{p_1\}$ | $D_2 \cup \{p_2\}$ | $D_3 \cup \{p_3\}$ |
|---|---|---|---|
| $p_1 = (0,0)$ | [0, 9] | [7.07, 12.73] | [8.06, 9] |
| $p_2 = (9,9)$ | [8.06, 12.73] | [0, 5.66] | [8.06, 9] |
| $p_3 = (9,0)$ | [7.62, 12.73] | [6.32, 9] | [0, 1.41] |

$D_1$ has four points, so it becomes a node with split points $(1,1)$, $(0,9)$, $(2,3)$ and a leaf $\{(1, 8)\}$; $D_2$ and $D_3$ are leaves. The build uses 84 distance evaluations.

**Range query** $q = (6, 4)$, $r = 2$. Measure $p_1$: $d_1 = 7.21$, so the interval is $[5.21, 9.21]$, which meets all three ranges in the first row. Measure $p_2$: $d_2 = 5.83$, interval $[3.83, 7.83]$; it misses $[8.06, 12.73]$ and $[8.06, 9]$, so groups 1 and 3 are removed, and $p_3$ is never measured. Group 2 is a leaf: $(5, 5)$ at distance 1.41 is reported, $(7, 6)$ at 2.24 is not. In all 4 distance evaluations instead of 10.

**Nearest neighbor** of the same $q$: after the three split points, the best is $(9, 0)$ at 5. Group 3 (bound $5 - 1.41 = 3.59 \le 5$) gives $(8, 1)$ at 3.61; group 2 (bound $5.83 - 5.66 = 0.17$) gives $(5, 5)$ at 1.41; group 1 has the bound $8.06 - 5.83 = 2.23 > 1.41$ from $p_2$ and is skipped. The answer $(5, 5)$ costs 6 evaluations.

## Correctness

The proof is in the proof file. The key fact: if $x \in D_j \cup \{p_j\}$ and $\delta(q, x) \le r$, then by the triangle inequality $|\delta(q, p_i) - \delta(p_i, x)| \le \delta(q, x) \le r$, so $\delta(p_i, x) \in [d_i - r, d_i + r]$, and since $\delta(p_i, x) \in \text{range}(i, j)$ the two intervals meet. So line L9 never removes a group that holds an answer, and by induction on the tree RANGE reports exactly the points within $r$. For NEAREST, the same argument with $r = \delta^*$ shows that a skipped group has no point nearer than the current best.

## Complexity

Model: real RAM where a distance evaluation costs $E$.

| operation | distance evaluations | notes |
|---|---|---|
| build | $O(n m h)$ | $h$ is the height; each level costs $O(m)$ per point, plus $O(m^2)$ per node for the split-to-split distances |
| range$(q, r)$ | at most $n$ | each point is measured at most once; plus $O(m^2)$ interval tests per visited node |
| nearest$(q)$ | at most $n$ | same |
| space | $O(nm)$ | $k_t^2 \le m k_t$ intervals at a node with $k_t$ split points, and $\sum_t k_t \le n$ |

The farthest-first rule does not balance the groups: one group can receive almost all points at every level, so nothing bounds $h$ below $n/m$ in the worst case, and the build can take $\Theta(n^2)$ evaluations. There is no worst-case query bound better than the scan in a general metric; the savings depend on the data and on $m$, and a larger $m$ trades a costlier build and more memory for more pruning per node.

## Variants

- **Generalized hyperplane tree** (Uhlmann): $m = 2$ and no range table; prune group $j$ when $\delta(q, p_j) - \delta(q, p_i) > 2r$, which follows from the bisector between the two pivots.
- **Varying arity.** Let the number of split points vary by node, giving more split points to larger groups, to keep the tree more balanced.
- **Disk-based and dynamic versions.** The [M-tree](/m-tree/) stores covering radii instead of range tables and supports insertions in pages on disk.
- **Pivot tables.** Keeping the distances from every point to a fixed set of pivots, as in [pivot-based indexing](/pivot-based-indexing/), gives the same interval test with no tree.

## When to use it

- Exact range and nearest neighbor search with an expensive distance (edit distance, distances between images or sets) when the build can be paid once and memory for $O(nm)$ intervals is available.
- When the data have low intrinsic dimension; in high intrinsic dimension the intervals overlap and little is pruned.
- Prefer the [cover tree](/cover-tree/) when provable bounds or insertions are needed, and a [BK-tree](/bk-tree/) for small integer distances.

## Pitfalls

- **Removing a split point by mistake.** The range must include $p_j$ itself; otherwise a removed group could hide its own split point, which is an answer when $\delta(q, p_j) \le r$.
- **Stale bounds in nearest search.** Pruning decisions made with a large $\delta^*$ are safe but weak. Recheck the bound of each group with the current $\delta^*$ before descending, as line L12 does.
- **Duplicates.** Several copies of one point all join the group of the first; a node whose points are all equal has range $[0, 0]$ everywhere. The tree remains correct, but its height grows with the number of copies unless the bucket size absorbs them.
- **Non-metric distances.** The pruning needs the triangle inequality. Cosine distance $1 - \cos$ and squared Euclidean distance violate it.

## Implementations

## History

Uhlmann described the generalized hyperplane tree, with two pivots per node, in 1991. Brin generalized it to $m$ split points per node with the range table in 1995 and called it GNAT, with split points chosen greedily to be far apart.

## References
