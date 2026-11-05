---
tag: H61XQ8
kind: technique
slug: pivot-based-indexing
name: Pivot-based indexing
aliases:
- pivot technique
- pivot filtering
area: searching/similarity-search
level: core
summary: Precompute distances from data objects to a few pivots and use them to filter candidates by the triangle inequality.
prereqs: [triangle-inequality, metric-space]
see_also: [triangle-inequality, metric-space-indexing, similarity-range-query, vantage-point-tree, mvp-tree, m-tree, bk-tree, similarity-index]
sources:
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (the pivot-based family of algorithms, AESA and LAESA, the mapping to the L-infinity distance on pivot distances, and the analysis of the number of pivots)
  - paper: "Enrique Vidal, An algorithm for finding nearest neighbours in (approximately) constant average time, Pattern Recognition Letters 4(3), 1986"
    locator: pages 145 to 157 (AESA, all objects used as pivots with the full distance matrix)
  - paper: "María Luisa Micó, José Oncina and Enrique Vidal, A new version of the nearest-neighbour approximating and eliminating search algorithm (AESA) with linear preprocessing time and memory requirements, Pattern Recognition Letters 15(1), 1994"
    locator: pages 9 to 17 (LAESA, a fixed set of base prototypes with linear memory)
  - book: isbn:9780387291468
    title: Pavel Zezula, Giuseppe Amato, Vlastislav Dohnal and Michal Batko, Similarity Search, The Metric Space Approach, Springer, 2006
    locator: Chapter 1 (the pivot filtering constraints and pivot selection) and Chapter 2, Survey of Existing Approaches (the distance matrix methods)
---

Pivot-based indexing is the technique of storing, for every object $x$ of a data set in a [metric space](/metric-space/), its distances $d(x, p_1), \ldots, d(x, p_t)$ to a few fixed objects called *pivots*, and using them at query time to exclude objects by the [triangle inequality](/triangle-inequality/): $d(q, x) \ge \max_j |d(q, p_j) - d(x, p_j)|$. A query then computes $t$ distances to the pivots and the distance to the few objects that survive the filter. Vidal's AESA (1986) uses every object as a pivot; LAESA (1994) uses a fixed small set, with linear memory. The same bound drives the pruning of the [vantage-point tree](/vantage-point-tree/), the [MVP-tree](/mvp-tree/) and the [M-tree](/m-tree/).

## In plain words

You have a big collection, and measuring how far two objects are is slow. Pick a few objects as landmarks. When you build the index, measure the distance from each object to each landmark, and write the numbers in a table.

When a query comes, measure its distance to the landmarks only. For each object, look up its numbers in the table. If the query is 10 away from a landmark and the object is 3 away from the same landmark, the object is at least 7 away from the query. If you want objects within 2 of the query, you can drop this object without measuring it. Check every landmark the same way. Only the objects that no landmark could drop are measured for real. With good landmarks, most of the collection is dropped by table lookups, which are cheap.

## When it applies

- The distance is a true metric, so the triangle inequality holds, and it is expensive: an [edit distance](/edit-distance/), a distance between images, a distance on graphs or trees.
- The objects have no coordinates, or the coordinates are not useful, so a [k-d tree](/kd-tree/) or an [R-tree](/r-tree/) is not available.
- There is memory for $t$ numbers per object, and time to compute $nt$ distances once.
- The queries are [range queries](/similarity-range-query/) or [nearest neighbor](/nearest-neighbor-search/) queries with a small radius compared to the spread of the distances.

## The template

```pseudo id=main
BUILD(P, t)                                ▷ P is the data set, t the number of pivots
L1  p1, ..., pt ← SELECT-PIVOTS(P, t)        ▷ hole: random, far apart, or tuned on sample queries
L2  for each x in P and each j ← 1 to t do D[x][j] ← d(x, pj)

RANGE(q, r)                                 ▷ report {x ∈ P : d(q, x) ≤ r}
L3  for j ← 1 to t do Q[j] ← d(q, pj)
L4  R ← ∅
L5  for each x in P do
L6      lb ← max over j of |Q[j] − D[x][j]|
L7      if lb > r then continue              ▷ excluded without a distance evaluation
L8      if min over j of (Q[j] + D[x][j]) ≤ r then R ← R ∪ {x}; continue    ▷ included without one
L9      if d(q, x) ≤ r then R ← R ∪ {x}
L10 return R

KNN(q, k)                                   ▷ the k objects nearest to q
L11 compute Q as in L3 and lb(x) as in L6 for each x in P
L12 H ← an empty max-heap of (distance, object), of size at most k
L13 for each x in P in order of increasing lb(x) do
L14     if |H| = k and lb(x) ≥ the largest distance in H then stop
L15     insert (d(q, x), x) into H; if |H| > k then remove the largest
L16 return the objects of H in order of distance
```

BUILD fills a table of $n \times t$ distances. RANGE computes $t$ distances in line L3. Line L6 is the lower bound of the [triangle inequality](/triangle-inequality/) page, taken over all pivots; it is the $\ell_\infty$ distance between the vectors $(Q[j])_j$ and $(D[x][j])_j$. Line L7 excludes $x$ when even this lower bound exceeds $r$. Line L8 uses the upper bound $d(q, x) \le d(q, p_j) + d(p_j, x)$ to accept $x$ with no evaluation. Only the objects that reach line L9 cost a distance evaluation.

KNN visits the objects in order of their lower bound. Once the lower bound of the next object is at least the $k$-th best distance so far, every later object has a lower bound at least as large, so its distance cannot be smaller, and line L14 stops.

**Correctness.** Both procedures are exact. By the two-sided bound, $\max_j |Q[j] - D[x][j]| \le d(q, x) \le \min_j (Q[j] + D[x][j])$ for each $x$, so line L7 excludes only objects with $d(q, x) > r$, and line L8 accepts only objects with $d(q, x) \le r$; every other object is tested exactly in line L9. In KNN, when line L14 stops at $x$, each object $y$ not yet visited has $d(q, y) \ge lb(y) \ge lb(x) \ge$ the largest distance in $H$, so $H$ holds $k$ nearest objects.

**Cost.** BUILD takes $nt$ distance evaluations and $\Theta(nt)$ space. A query takes $t$ evaluations for the pivots, plus one for each object that reaches line L9 (for RANGE) or line L15 (for KNN), plus $\Theta(nt)$ other work to compute the bounds, and $O(n \log n)$ more for the sort of KNN. When $d$ is expensive, the evaluations dominate, and the extra arithmetic is the price of the method. The worst case is $t + n$ evaluations, for example in the discrete metric where all distances are equal and no bound excludes anything.

### Example

In the plane with the Euclidean distance, take eight objects and the two pivots $p_1 = (0, 0)$ and $p_2 = (10, 0)$. The query is $q = (5, 5)$, so $Q = (7.0711, 7.0711)$, and the radius is $r = 2$.

| object | $x$ | $D[x]$ | lower bound (L6) | decision | true $d(q, x)$ |
|---|---|---|---|---|---|
| a | (1, 1) | (1.4142, 9.0554) | 5.6569 | excluded | 5.6569 |
| b | (2, 6) | (6.3246, 10) | 2.9289 | excluded | 3.1623 |
| c | (4, 4) | (5.6569, 7.2111) | 1.4142 | evaluated, answer | 1.4142 |
| d | (5, 1) | (5.0990, 5.0990) | 1.9720 | evaluated, not an answer | 4 |
| e | (6, 7) | (9.2195, 8.0623) | 2.1485 | excluded | 2.2361 |
| f | (8, 3) | (8.5440, 3.6056) | 3.4655 | excluded | 3.6056 |
| g | (9, 8) | (12.0416, 8.0623) | 4.9705 | excluded | 5 |
| h | (3, 9) | (9.4868, 11.4018) | 4.3307 | excluded | 4.4721 |

RANGE reports $\{c\}$ with 4 distance evaluations (two pivots, c and d) instead of 8. For KNN with $k = 1$, the order of the lower bounds is c, d, e, and so on. The search evaluates c, at distance 1.4142, then stops at d, whose lower bound 1.9720 is larger: 3 evaluations in total.

## Classic examples

- **[Similarity range query](/similarity-range-query/)** and **[nearest neighbor search](/nearest-neighbor-search/)** in a general metric space: the pivot table is the simplest exact index for both.
- **AESA.** Vidal uses every object as a pivot, with the full matrix of $n(n-1)/2$ distances. A nearest neighbor query picks the next pivot among the surviving objects, the one with the least lower bound, and updates all bounds with its distance. In experiments the number of evaluations is almost constant in $n$, but the quadratic memory and build time limit it to small sets.
- **LAESA.** Micó, Oncina and Vidal fix $t$ base pivots chosen far apart, which gives the linear memory of the template above.
- **[Vantage-point tree](/vantage-point-tree/).** One pivot per node, and the data split by its distance to the pivot; the tree stores only the cut radius instead of all distances.
- **[MVP-tree](/mvp-tree/).** Several pivots per node, and in the leaves the precomputed distances of each object to the pivots of its path, which the search uses as a pivot table.
- **[M-tree](/m-tree/).** Each entry stores its distance to the routing object of its parent node, a pivot that the search uses to skip entries before it computes their distance.
- **[BK-tree](/bk-tree/).** For integer distances, the children of a node are grouped by their exact distance to it, which is a pivot test with rings of width 1.

## Variations

- **Pivot selection.** Random pivots are the baseline. Pivots far from each other and from most objects, found by a farthest-first walk, give larger values of $|Q[j] - D[x][j]|$ and so better bounds. An incremental method adds the pivot that best raises the mean lower bound over a sample of pairs.
- **The number of pivots.** More pivots give tighter bounds but cost $t$ evaluations per query and $nt$ memory. The best $t$ grows with the [intrinsic dimensionality](/intrinsic-dimensionality/) of the data; in high intrinsic dimension no number of pivots helps much.
- **Sorted columns.** Keep each column $D[\cdot][j]$ sorted, so that the objects with $|Q[j] - D[x][j]| \le r$ form an interval found by [binary search](/binary-search/), and intersect the intervals; this saves the $\Theta(nt)$ scan of lines L5 and L6.
- **Mapping to a vector space.** The map $x \mapsto (d(x, p_j))_j$ embeds the data in $\mathbb{R}^t$ with the $\ell_\infty$ distance as a lower bound of $d$. A [k-d tree](/kd-tree/) or an [R-tree](/r-tree/) on these vectors replaces the scan of the candidates.
- **Permutation-based indexing.** Keep only the order of the pivots by distance for each object. Objects whose order is close to that of the query are likely close. This is approximate.

## Pitfalls

- **A distance that is not a metric.** With the squared Euclidean distance, a cosine distance or a learned distance, line L7 can exclude true answers. Use the root of the squared distance, the angle instead of $1 - \cos$, or test the triangle inequality on samples.
- **Pivots close together.** Two pivots near each other give almost the same bound, and the second pivot adds cost without pruning. Choose pivots far apart.
- **Pivots inside the data set.** A pivot that is also a data object has distance 0 to itself; its row should not be evaluated again in line L9. Skip objects already evaluated in line L3.
- **Floating point.** Distances computed with rounding can make $lb$ slightly larger than the true distance. Compare with a small tolerance in line L7 when the answers must be exact.
- **Counting only evaluations.** The scan of lines L5 and L6 costs $\Theta(nt)$ arithmetic per query. When $d$ is cheap, for example the Euclidean distance in 10 dimensions, this scan can be slower than the brute force.

## Exercises

1. Take the discrete metric ($d(x, y) = 1$ for $x \ne y$), one pivot from the data set, and a query that is not a data object. Show that for $0 \le r < 1$ RANGE evaluates every object except the pivot, and that for $r \ge 2$ it evaluates none.
2. Prove that the lower bound of line L6 cannot decrease when a pivot is added.
3. In the example, add the pivot $p_3 = (5, 0)$ and recompute the lower bound of d. Does RANGE still evaluate d?

## References
