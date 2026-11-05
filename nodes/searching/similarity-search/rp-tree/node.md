---
tag: 58J4K4
kind: data-structure
slug: rp-tree
name: Random projection tree
aliases:
- RP-tree
area: searching/similarity-search
level: research
summary: A space-partitioning tree that splits along random directions and adapts to low intrinsic dimension.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of points, D: the ambient dimension, n0: the largest leaf size, k: the number of neighbors asked}
  time: {build: O(n (D + log n) log n), defeatist query: O(D log(n/n0) + n0 D), exact query: O(n D + n log k)}
  space: {tree: Θ(n + (n/n0) D)}
properties: {deterministic: false, online: false}
history:
  year: 2008
  people: [Sanjoy Dasgupta, Yoav Freund]
  note: Dasgupta and Freund introduced RP-trees at STOC 2008 and proved that they adapt to the Assouad dimension of the data.
prereqs: [kd-tree, random-projection]
see_also: [kd-tree, random-projection, johnson-lindenstrauss-lemma, intrinsic-dimensionality, ball-tree, nn-descent, lsh-forest, vantage-point-tree]
sources:
  - paper: doi:10.1145/1374376.1374452
    title: Sanjoy Dasgupta and Yoav Freund, Random projection trees and low dimensional manifolds, Proceedings of the 40th Annual ACM Symposium on Theory of Computing (STOC 2008)
    locator: pages 537 to 546 (the RPTree-Max rule with a jittered median split along a random direction, the RPTree-Mean rule, the theorem that the radius of cells halves every O(d log d) levels for data of Assouad dimension d, and the bound for local covariance dimension)
  - paper: "Sanjoy Dasgupta and Kaushik Sinha, Randomized partition trees for exact nearest neighbor search, Proceedings of the 26th Annual Conference on Learning Theory (COLT 2013), JMLR Workshop and Conference Proceedings 30"
    locator: pages 317 to 337 (RP-trees with median splits and spill trees used for defeatist nearest neighbor search, and bounds on the probability that the search misses the nearest neighbor)
---

A random projection tree, or RP-tree, is a binary space-partitioning tree on points of $\mathbb{R}^D$ in which every internal node cuts its cell by a hyperplane orthogonal to a *random* direction, near the median of the projections of its points. It is the [k-d tree](/kd-tree/) with the coordinate axes replaced by random directions. The change matters when the data has low intrinsic dimension inside a high ambient dimension, for example points on a curve or a low-dimensional manifold: a k-d tree may need about $D$ levels to halve the diameter of its cells, while Dasgupta and Freund proved in 2008 that an RP-tree halves the radius of its cells every $O(d \log d)$ levels with probability at least $1/2$, where $d$ is the Assouad dimension of the data and does not involve $D$. RP-trees are used for exact and approximate [nearest neighbor search](/nearest-neighbor-search/), for vector quantization, and to seed [NN-Descent](/nn-descent/).

## In plain words

To find things fast in a big pile of points, cut the pile in two halves, then cut each half in two, and so on, until each piece is small. A query only looks inside the piece it falls into, and maybe a few neighboring pieces.

A k-d tree always cuts straight across one of the axes. If the points lie along a slanted thread or a curved sheet, axis cuts can slice the same thin shape over and over without making the pieces much smaller.

An RP-tree picks the direction of each cut at random. Each random cut is a little worse than the best cut, but it is never stuck with bad directions, so the pieces shrink at a rate that depends on how complicated the shape of the data is, not on how many coordinates the points have.

## The abstract type

A static [similarity index](/similarity-index/) on $n$ points of $\mathbb{R}^D$ with the Euclidean distance. BUILD$(P, n_0)$ makes the tree; QUERY$(q, k)$ returns the $k$ points of $P$ nearest to $q$, exactly, in order of distance (ties broken by index); LEAF$(q)$ returns the points of the leaf cell that contains $q$, the candidates of a fast approximate search. The model is the real RAM, with $O(D)$ time for an inner product or a distance.

## Representation

Each internal node stores a unit vector $v \in \mathbb{R}^D$ and a threshold $t$, and two children: the left child holds the points $x$ of the node with $v \cdot x \le t$, the right child those with $v \cdot x > t$. Each leaf stores the indices of its points. The cell of a node is the intersection of the half-spaces on its path from the root, a convex polytope.

**Invariants.** (I1) The leaves partition the indices $\{0, \ldots, n - 1\}$. (I2) At a node with $(v, t)$, every point of the left subtree has $v \cdot x \le t$ and every point of the right subtree has $v \cdot x > t$; both subtrees are nonempty. (I3) A leaf has at most $n_0$ points, unless all its points have the same projection on the direction drawn for it.

## Operations

```pseudo id=main
BUILD(S)                                       ▷ S is a set of points, n0 the leaf size
L1  if |S| ≤ n0 then return a leaf holding S
L2  v ← a random unit vector (a normalized standard Gaussian vector)
L3  t ← the lower median of {v · x : x ∈ S}
L4  L ← {x ∈ S : v · x ≤ t}; R ← S \ L
L5  if R = ∅ then return a leaf holding S        ▷ all projections are equal
L6  return the node (v, t, BUILD(L), BUILD(R))

QUERY(node, q, k, H)                            ▷ H holds the best k pairs (distance, index) so far
L7  if node is a leaf then offer (‖q − x‖, x) to H for each x of the leaf; return
L8  g ← v · q − t
L9  (near, far) ← (left, right) if g ≤ 0, else (right, left)
L10 QUERY(near, q, k, H)
L11 if |H| < k or |g| ≤ the largest distance in H then QUERY(far, q, k, H)
```

The lower median at line L3 is the value of rank $\lceil |S|/2 \rceil$, so when the projections are distinct, line L4 sends $\lceil |S|/2 \rceil$ points to the left and $\lfloor |S|/2 \rfloor$ to the right. LEAF$(q)$ follows the sign of $g$ from the root to a leaf, without line L11: this is the *defeatist* search, which costs one inner product per level and may miss the nearest neighbor.

QUERY is the branch and bound search of the k-d tree, with one change: the distance from $q$ to the cell on the far side is at least $|g| = |v \cdot q - t|$, the distance from $q$ to the cutting hyperplane, since $v$ has unit length. Line L11 skips the far side when even this lower bound is larger than the current $k$-th best distance.

Dasgupta and Freund's rule **RPTree-Max** jitters the median: it picks a point $x$ of $S$, the point $y$ of $S$ farthest from $x$, and a number $\delta$ uniform in $[-6\|x - y\|/\sqrt{D},\, 6\|x - y\|/\sqrt{D}]$, and cuts at $t$ equal to the median plus $\delta$. The jitter is what their proof needs. The plain median of line L3 keeps the tree balanced, and is the version used by Dasgupta and Sinha and by most implementations.

## Example

In the plane, take $n_0 = 2$ and the points $a = (0, 0)$, $b = (1, 1)$, $c = (2, 1)$, $d = (3, 2)$, $e = (4, 4)$, $f = (5, 4)$, $g = (6, 5)$, $h = (7, 7)$, which lie near a line at 45°. To keep the arithmetic readable, the three directions drawn by line L2 are fixed: $(0.6, 0.8)$ at the root, $(0.8, -0.6)$ at its left child and $(0, 1)$ at its right child.

| node | points | projections $v \cdot x$ | $t$ | left | right |
|---|---|---|---|---|---|
| root | a to h | 0, 1.4, 2, 3.4, 5.6, 6.2, 7.6, 9.8 | 3.4 | a, b, c, d | e, f, g, h |
| left child | a, b, c, d | 0, 0.2, 1, 1.2 | 0.2 | a, b | c, d |
| right child | e, f, g, h | 4, 4, 5, 7 | 4 | e, f | g, h |

The tree has depth 2 and four leaves $\{a, b\}$, $\{c, d\}$, $\{e, f\}$, $\{g, h\}$. The left child cuts across the line of the data, while the axis $x$ or $y$ would cut along the same direction as the root.

Query $q = (4.5, 3)$ with $k = 1$. At the root $g = 0.6 \cdot 4.5 + 0.8 \cdot 3 - 3.4 = 1.7 > 0$, so the search goes right; at the right child $g = 3 - 4 = -1$, so it goes left, to the leaf $\{e, f\}$, where both are at distance $\sqrt{1.25} \approx 1.1180$, and $e$ wins on its index. Back at the right child, $|g| = 1 \le 1.1180$, so it visits $\{g, h\}$, at distances 2.5 and 4.7170, with no change. Back at the root, $|g| = 1.7 > 1.1180$, so the whole left subtree is skipped. The answer is $e$ after 4 distance evaluations out of 8, and LEAF$(q) = \{e, f\}$ already holds it. With $k = 2$ the answer is $e, f$, again with 4 evaluations.

## Correctness

The following holds for every input and every choice of directions; the proof is in [the correctness proof](proofs/correctness.md).

1. **Structure.** BUILD terminates and its tree satisfies (I1) to (I3). If all projections at every node are distinct, which happens with probability 1 for Gaussian directions and distinct points, every leaf has at most $n_0$ points and the depth is exactly $\lceil \log_2(n/n_0) \rceil$ for $n > n_0$.
2. **Exact search.** QUERY$(root, q, k, \emptyset)$ returns the $\min(k, n)$ points nearest to $q$, in order of (distance, index).

**Adaptivity (Dasgupta and Freund, cited).** Let the points of a cell $C$ have Assouad dimension at most $d$: every ball of radius $r$ that they meet can be covered, as far as these points go, by $2^d$ balls of radius $r/2$. Then there is an absolute constant $c_1$ such that, for trees built by RPTree-Max and with probability at least $1/2$ over the random choices in the subtree of $C$, every cell more than $c_1 d \log d$ levels below $C$ has radius at most half the radius of $C$. For RPTree-Mean, which alternates the median cut with a cut by distance to the mean, they bound instead the average squared diameter of the cells in terms of the local covariance dimension. These statements are not proved here.

## Complexity

In the real RAM, with $O(D)$ for an inner product or a distance, and assuming distinct projections at every node so that the depth is $h = \lceil \log_2(n/n_0) \rceil$:

| operation | cost | case |
|---|---|---|
| BUILD | $O(n D h + n h \log n) = O(n (D + \log n) \log n)$ | worst; one projection of each point per level, and a sort per node. A linear-time [selection](/quickselect/) removes the $\log n$ factor |
| LEAF$(q)$ | $O(D h)$ | worst |
| defeatist search | $O(D h + n_0 D)$ | worst; may miss the nearest neighbor |
| QUERY, exact | $n$ distance evaluations and $O(n D + n \log k)$ time | worst; the bound of line L11 may prune nothing |
| space | $\Theta(n + (n/n_0) D)$ | $n$ indices in the leaves, one direction of $D$ numbers per internal node |

Like the [k-d tree](/kd-tree/), the exact search has no useful worst-case bound; its speed in practice comes from the shrinking cells, which is what the adaptivity theorem controls. Each internal node stores a full vector of $D$ numbers, not one coordinate index: this is the price over the k-d tree.

## Variants

- **RPTree-Max and RPTree-Mean.** The two rules of Dasgupta and Freund, with the guarantees cited above.
- **One direction per level.** Use the same random direction for all nodes of a level, to store $O(D \log n)$ numbers instead of $O(nD/n_0)$.
- **Spill trees.** Send the points with projection in a band around $t$ to both children. Defeatist search then misses the nearest neighbor less often, at the price of more space; Dasgupta and Sinha bound the miss probability of both kinds of tree.
- **Forests.** Build several trees with independent directions and take the union of the leaves of $q$, as in [LSH forests](/lsh-forest/). The library Annoy uses a forest of trees whose cut is the hyperplane halfway between two sampled points.
- **Seeding graphs.** The leaves of a few RP-trees give the start lists of [NN-Descent](/nn-descent/), with close points already together.
- **Projection first.** A single [random projection](/random-projection/) by the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) reduces $D$ to $O(\log n / \varepsilon^2)$ for all points at once; an RP-tree instead uses one direction per node and adapts to the local structure.

## When to use it

Use an RP-tree for nearest neighbor search or quantization in high ambient dimension when the data is believed to have low intrinsic dimension: images, audio frames, sensor data, embeddings. In low ambient dimension, a [k-d tree](/kd-tree/) is cheaper to store and as fast. For general metric spaces without coordinates, use a [vantage-point tree](/vantage-point-tree/) or a [ball tree](/ball-tree/).

## Pitfalls

- **Expecting a worst-case bound.** The adaptivity theorem bounds the shrinking of cells with probability $1/2$ per block of levels; it does not bound the time of an exact query for every input.
- **Directions not of unit length.** The pruning test of line L11 uses $|v \cdot q - t|$ as a distance. With an unnormalized $v$ it must be divided by $\|v\|$, or the search prunes true answers.
- **Many equal projections.** Duplicates make line L4 send everything left. Without the test of line L5 the recursion does not end.
- **Defeatist search near a cut.** A query close to a cutting hyperplane often has its nearest neighbor on the other side. Use spill trees, several trees, or the exact search of line L11.
- **Floating point.** The projection of $q$ and the distances are rounded; compare with a small tolerance in line L11 when the answer must be exact, as the implementation here does.

## Implementations

## History

Dasgupta and Freund introduced random projection trees at STOC 2008, to show that a simple space-partitioning tree adapts to the intrinsic dimension of the data without knowing it, in contrast with the k-d tree. Dasgupta and Sinha studied RP-trees and spill trees for nearest neighbor search at COLT 2013. Random projection forests are used in Annoy and in PyNNDescent.

## References
