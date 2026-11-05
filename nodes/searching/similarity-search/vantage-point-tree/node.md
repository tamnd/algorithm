---
tag: ET45HH
kind: data-structure
slug: vantage-point-tree
name: Vantage-point tree
aliases:
- VP-tree
- vp-tree
area: searching/similarity-search
level: advanced
summary: Binary metric tree that splits points by distance from a chosen vantage point.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of objects, h: the height of the tree}
  time: {build: O(n log n), range: O(n), nearest: O(n), height: O(log n)}
  space: {total: Θ(n)}
properties: {deterministic: true, recursive: true}
history:
  year: 1991
  people: [Jeffrey K. Uhlmann, Peter N. Yianilos]
  note: Uhlmann described metric trees split by the distance to one point in 1991; Yianilos named them vantage-point trees and studied the choice of the vantage point and their search cost in 1993.
prereqs: [metric-space, triangle-inequality, pivot-based-indexing]
see_also: [mvp-tree, m-tree, ball-tree, gnat, bk-tree, metric-space-indexing, similarity-range-query, kd-tree]
sources:
  - paper: "Peter N. Yianilos, Data structures and algorithms for nearest neighbor search in general metric spaces, Proceedings of the 4th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1993"
    locator: pages 311 to 321 (the vp-tree with the median split, the choice of vantage points far from the data, nearest neighbor search with a shrinking radius, and the vps- and vpsb-tree variants)
  - paper: doi:10.1016/0020-0190(91)90074-R
    title: Jeffrey K. Uhlmann, Satisfying general proximity/similarity queries with metric trees, Information Processing Letters 40(4), 1991
    locator: pages 175 to 179 (ball decomposition by the median distance to a point, and generalized hyperplane decomposition)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 5, the vantage-point tree among the pivot-based tree indexes, with its pruning rules for range queries)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, Section 4.5, Distance-Based Indexing Methods (the vp-tree, its construction and search)
---

A vantage-point tree stores a finite set of objects of a [metric space](/metric-space/) in a balanced binary tree. Each node holds one object $v$, the *vantage point*, and the median $\mu$ of the distances from $v$ to the other objects of its subtree; the objects at distance at most $\mu$ go to the inside child, the others to the outside child. A [range query](/similarity-range-query/) or a [nearest neighbor](/nearest-neighbor-search/) query computes the distance $t$ from the query to $v$ and skips a child when the [triangle inequality](/triangle-inequality/) shows it is too far: the inside when $t - r > \mu$, the outside when $t + r < \mu$. The tree has height $\lceil \log_2(n+1) \rceil$, linear size, and $O(n \log n)$ distance evaluations to build. Uhlmann (1991) and Yianilos (1993) introduced it.

## In plain words

Pick one object of the collection as a landmark. Measure how far every other object is from it, and find the middle distance. Put the closer half in one group, the "inside", and the farther half in another, the "outside". Then do the same inside each group, with a new landmark each time, until every group has one object. The result is a tree of landmarks.

To find all objects close to a query, measure the distance from the query to the top landmark. If the query is far beyond the middle distance, nothing inside can be close to it, so skip the inside group. If it is well within the middle distance, skip the outside. Go down only into groups that might hold an answer. The same walk, with a limit that shrinks as better answers turn up, finds the nearest object.

## The abstract type

The tree is a static [similarity index](/similarity-index/) for a metric space $(U, d)$: it is built once from a finite set $P \subseteq U$ and answers range queries $R(q, r) = \{x \in P : d(q, x) \le r\}$ and nearest neighbor queries for any $q \in U$. It needs only a function that computes $d$; it never looks inside the objects. Cost is counted in evaluations of $d$, the expensive step for distances such as the [edit distance](/edit-distance/).

## Representation

A node is a record $(v, \mu, \mathit{in}, \mathit{out})$ with an object $v \in P$, a radius $\mu \ge 0$, and two children, possibly empty. Each object of $P$ is the vantage point of exactly one node. For a node with subtree set $S$, the other objects $S \setminus \{v\}$ are sorted by $d(v, \cdot)$, the first $m = \lceil (|S| - 1)/2 \rceil$ go to $\mathit{in}$ and the rest to $\mathit{out}$, and $\mu$ is the distance of the $m$-th. So

$$d(v, x) \le \mu \text{ for every } x \text{ in } \mathit{in}, \qquad d(v, x) \ge \mu \text{ for every } x \text{ in } \mathit{out}.$$

Ties at distance $\mu$ may go to both sides; the split by rank keeps the tree balanced even when many distances are equal.

## Operations

```pseudo id=main
BUILD(S)                                    ▷ S a list of objects
L1  if S is empty then return nil
L2  v ← CHOOSE(S)                             ▷ random, or a point far from the others
L3  S′ ← S without v, sorted by d(v, ·); m ← ⌈|S′| / 2⌉
L4  if S′ is empty then return (v, 0, nil, nil)
L5  μ ← d(v, S′[m])
L6  return (v, μ, BUILD(S′[1 .. m]), BUILD(S′[m + 1 .. |S′|]))

RANGE(N, q, r, out)                          ▷ adds every x in N's subtree with d(q, x) ≤ r to out
L7  if N = nil then return
L8  t ← d(q, N.v); if t ≤ r then add N.v to out
L9  if t − r ≤ N.μ then RANGE(N.in, q, r, out)
L10 if t + r ≥ N.μ then RANGE(N.out, q, r, out)

NEAREST(N, q)                                ▷ updates the global best (b, τ), with τ = ∞ at the start
L11 if N = nil then return
L12 t ← d(q, N.v); if t < τ then (b, τ) ← (N.v, t)
L13 if t ≤ N.μ then the order is (in, out), else (out, in)
L14 for each child C of N in that order do
L15     if (C = in and t − τ ≤ N.μ) or (C = out and t + τ ≥ N.μ) then NEAREST(C, q)
```

BUILD makes one distance evaluation for each object of $S'$ in line L3, and sorts them; a linear-time selection of the median works as well. RANGE prunes with the two bounds of the representation: an object $x$ inside has $d(q, x) \ge t - d(v, x) \ge t - \mu$, and an object outside has $d(q, x) \ge d(v, x) - t \ge \mu - t$. NEAREST is RANGE with the radius $\tau$ of the best object so far, which shrinks during the search; it visits first the child on the side of $q$, where a near object is more likely, so that $\tau$ is small before the other side is tested. The query for the $k$ nearest objects keeps a max-heap of $k$ candidates and uses the $k$-th distance as $\tau$.

## Example

Take seven points of the plane with the Euclidean distance, $a = (1, 1)$, $b = (2, 6)$, $c = (4, 4)$, $d = (5, 1)$, $e = (6, 7)$, $f = (8, 3)$, $g = (9, 8)$, and let CHOOSE take the first object of its list.

| step | what happens | result |
|---|---|---|
| root | distances from $a$: $d$ 4, $c$ 4.2426, $b$ 5.0990, $f$ 7.2801, $e$ 7.8102, $g$ 10.6301; $m = 3$ | $(a, 5.0990)$, inside $\{d, c, b\}$, outside $\{f, e, g\}$ |
| inside | from $d$: $c$ 3.1623, $b$ 5.8310 | $(d, 3.1623)$, inside $\{c\}$, outside $\{b\}$ |
| outside | from $f$: $e$ 4.4721, $g$ 5.0990 | $(f, 4.4721)$, inside $\{e\}$, outside $\{g\}$ |

The build makes $6 + 2 + 2 = 10$ evaluations, and the tree has height 3.

Range query $q = (8, 7)$, $r = 2$. At $a$, $t = 9.2195$; since $t - r = 7.2195 > 5.0990$, the inside subtree is skipped, and since $t + r \ge 5.0990$, the search goes outside. At $f$, $t = 4$; $t - r = 2 \le 4.4721$, so it visits $e$, at distance 2, an answer; $t + r = 6 \ge 4.4721$, so it visits $g$, at distance 1.4142, an answer. The result is $\{e, g\}$ after 4 evaluations instead of 7.

Nearest neighbor of $q = (7, 6)$. At $a$, $t = 7.8102$ and $\tau = 7.8102$; $t > \mu$, so the outside comes first. At $f$, $t = 3.1623$ and $\tau$ drops to 3.1623; $t \le 4.4721$, so the inside comes first: $e$ at 1.4142 gives $\tau = 1.4142$. Then $g$ is tested: $t + \tau = 4.5765 \ge 4.4721$, so $g$ is evaluated, at 2.8284. Back at $a$, the inside is tested with $t - \tau = 6.3960 > 5.0990$ and skipped. The answer is $e$, after 4 evaluations.

## Correctness

**Invariant of the representation.** Every node satisfies $d(v, x) \le \mu$ for $x$ in its inside subtree and $d(v, x) \ge \mu$ for $x$ in its outside subtree, because line L3 sorts by $d(v, \cdot)$ and line L5 takes $\mu$ at the boundary.

**RANGE reports exactly $R(q, r)$.** Each object is the vantage point of one node, and line L8 reports it if and only if it is visited and within $r$. A skipped inside subtree has $t - r > \mu$, so each of its objects has $d(q, x) \ge t - \mu > r$ by the triangle inequality; a skipped outside subtree has $\mu - t > r$, so $d(q, x) \ge \mu - t > r$. No answer is in a skipped subtree.

**NEAREST returns a nearest object.** The variable $\tau$ only decreases, and $b$ is always a visited object at distance $\tau$. A subtree skipped when $\tau$ had the value $\tau_0$ holds only objects at distance greater than $\tau_0 \ge \tau_{\text{final}}$, by the same two bounds. So every object at distance less than the final $\tau$ was visited, and $b$ is a nearest object. The full proofs, with the height bound, are below.

## Complexity

The model is the [real RAM](/real-ram/) with an oracle for $d$. The table counts distance evaluations, and the time when it differs.

| operation | cost | case |
|---|---|---|
| build | $O(n \log n)$ evaluations; $O(n \log^2 n)$ time with sorting, $O(n \log n)$ with selection | worst |
| height | $\lfloor \log_2 n \rfloor + 1 = \lceil \log_2(n+1) \rceil$ | worst, by the split by rank |
| range | $n$ evaluations | worst; few on data of low intrinsic dimension and small $r$ |
| nearest | $n$ evaluations | worst; logarithmic in experiments on low-dimensional data |
| space | $\Theta(n)$ | one node per object, one stored distance per node |

The build makes at most $n$ evaluations per level, since each object is compared with the vantage point of the node it passes through, and there are at most $\lceil \log_2(n+1) \rceil$ levels. The worst case of the queries cannot be improved for any index in this model: the adversary of the [range query](/similarity-range-query/) page forces $n$ evaluations. On data of low [intrinsic dimension](/intrinsic-dimensionality/), most nodes have $|t - \mu| > r$ and one child is skipped, so a query visits a few root-to-leaf paths; as the dimension grows, the distances concentrate near $\mu$, both children must be visited, and the search approaches the scan.

## Variants

- **Choice of vantage point.** Yianilos picks, among a sample, the candidate whose distances to another sample have the largest spread, which tends to be a point near the edge of the data. A point in a corner gives distances spread out, so that few queries fall near the boundary $\mu$.
- **Bounds per subtree.** The vpsb-tree of Yianilos stores, for each child, the least and greatest distance from $v$ to its objects, which gives tighter pruning than the single $\mu$.
- **Larger fan-out.** Split at several quantiles of the distances into $m$ rings, as in the [MVP-tree](/mvp-tree/), which also uses two vantage points per node and stores precomputed distances in the leaves.
- **Buckets.** Stop the recursion at sets of a few objects and scan them, which saves nodes and pointer overhead.
- **Generalized hyperplanes.** Uhlmann's other split uses two points and sends each object to the nearer one; it leads to the gh-tree and to [GNAT](/gnat/).
- **Dynamic sets.** The tree is static. For insertions and deletions use the [M-tree](/m-tree/), which is balanced and paged like a B-tree.

## When to use it

Use a vantage-point tree for exact range and nearest neighbor queries in a metric space with an expensive distance and a static data set: strings under the edit distance, images under a perceptual distance, sets under the Jaccard distance. It needs only $n$ stored distances, against $nt$ for a [pivot table](/pivot-based-indexing/), and is simple to build. For points of $\mathbb{R}^d$ with small $d$, a [k-d tree](/kd-tree/) is usually faster, because it uses the coordinates. For data of high intrinsic dimension, no exact index helps much; use an approximate method such as [HNSW](/hnsw/).

## Pitfalls

- **A distance that is not a metric.** Lines L9, L10 and L15 assume the triangle inequality. With a squared Euclidean distance, or a cosine distance $1 - \cos$, they skip true answers.
- **Strict instead of loose tests.** The tests $t - r \le \mu$ and $t + r \ge \mu$ must allow equality, because objects at distance exactly $\mu$ may lie on both sides.
- **Splitting by value with many ties.** Putting all objects with $d(v, x) \le \mu$ inside makes the tree unbalanced when many distances equal $\mu$, as with small integer distances. Split by rank, as line L3 does.
- **Fixed order in the nearest search.** Visiting the inside first in every node makes $\tau$ shrink slowly and visits many more nodes. Visit the side of $q$ first, as in line L13.
- **Floating point.** Rounding can make a computed $t - \mu$ slightly larger than the true value; use a small tolerance in the tests when exact answers are required.

## Implementations

## History

Uhlmann described two kinds of metric trees in 1991, one splitting by the median distance to a single point (ball decomposition) and one splitting by the nearer of two points (generalized hyperplane decomposition). Yianilos independently developed the first kind, named it the vantage-point tree, and analyzed its construction and search at SODA 1993, with the variants that store bounds and buckets. Bozkaya and Özsoyoglu extended it to the MVP-tree in 1997.

## References
