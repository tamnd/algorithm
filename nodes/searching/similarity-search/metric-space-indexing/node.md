---
tag: XGBGSS
kind: concept
slug: metric-space-indexing
name: Metric space indexing
aliases:
- Metric tree
- metric access methods
- metric space index
- metric trees
area: searching/similarity-search
level: advanced
summary: Indexing points using only the triangle-inequality distance, the common basis of VP-trees, ball trees and cover trees.
prereqs: [metric-space, triangle-inequality, similarity-index]
see_also: [pivot-based-indexing, vantage-point-tree, mvp-tree, m-tree, gnat, cover-tree, ball-tree, intrinsic-dimensionality]
sources:
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (the unifying model of an index as a partition into equivalence classes, the split into pivot-based and clustering-based algorithms, the pruning rules, the cost model, and the intrinsic dimensionality μ²/2σ² of the histogram of distances)
  - book: isbn:9780387291468
    title: Pavel Zezula, Giuseppe Amato, Vlastislav Dohnal and Michal Batko, Similarity Search, The Metric Space Approach, Springer, 2006
    locator: Chapter 1, Foundations of Metric Space Searching (partitioning principles, ball and generalized hyperplane partitioning, filtering by pivots) and Chapter 2, Survey of Existing Approaches
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, Section 4.5, Distance-Based Indexing Methods (ball partitioning, generalized hyperplane partitioning, the M-tree and the methods that use distance matrices)
---

Metric space indexing is the design of search structures that know nothing about the objects except a [metric](/metric-space/) $d$ that can be evaluated on any two of them. Coordinates, keys and orders are not available; the only tool for pruning is the [triangle inequality](/triangle-inequality/), which turns stored distances into lower bounds on distances to the query. Every such index precomputes some distances between data objects and chosen reference objects, partitions the data by them, and at query time excludes the parts whose lower bound exceeds the search radius. [Pivot tables](/pivot-based-indexing/), [vantage-point trees](/vantage-point-tree/), [MVP-trees](/mvp-tree/), [GNAT](/gnat/), [M-trees](/m-tree/), [ball trees](/ball-tree/) and [cover trees](/cover-tree/) are all instances.

## In plain words

Suppose you can only ask one kind of question about your data: how far apart are these two things? You cannot sort them, you cannot look at their parts, and each question is slow. How do you find the things near a new item without asking about every one?

The trick is to ask some questions in advance. Pick a few reference items and measure how far everything is from them. Later, measure how far the new item is from the same references. If the new item is 10 away from a reference and some old item is 3 away from it, the two must be at least 7 apart. Whole groups of old items can be ruled out this way, and only the rest need to be measured for real. All the structures in this area are different ways of choosing the references and grouping the items around them.

## The idea

**The model.** A metric space $(U, d)$ and a finite set $P \subseteq U$ of $n$ objects. An index may store anything computed from $P$. At query time it learns about the query $q$ only through evaluations $d(q, x)$, and the main cost of a query is the number of such evaluations. Two other costs matter in practice: the extra arithmetic, and the number of disk pages read when the index is on disk.

**The pruning rules.** With $t = d(q, p)$ for a reference object $p$, the triangle inequality gives, for every object $x$,

$$|d(q, p) - d(x, p)| \le d(q, x) \le d(q, p) + d(x, p).$$

From this follow the three tests that all indexes use, for a query ball of radius $r$:

1. **Pivot test.** If $|t - d(x, p)| > r$, then $x$ is not an answer. One stored distance per object and pivot is needed.
2. **Ball test.** If every object of a set $S$ lies within $\rho$ of a center $c$, and $d(q, c) > r + \rho$, then no object of $S$ is an answer. If the objects lie at distance at least $\rho'$ from $c$, and $d(q, c) < \rho' - r$, none is an answer either; this excludes the outside of a ring.
3. **Hyperplane test.** If every object of $S$ is at least as close to $c_1$ as to $c_2$, and $d(q, c_1) - d(q, c_2) > 2r$, then no object of $S$ is an answer.

**Two families.** Chávez, Navarro, Baeza-Yates and Marroquín describe every index as a partition of $P$ into classes, together with a test that excludes classes.

- *Pivot-based indexes* fix reference objects, the pivots, and classify objects by their distances to them: the pivot table (AESA, LAESA), the [BK-tree](/bk-tree/), the [vantage-point tree](/vantage-point-tree/), the [MVP-tree](/mvp-tree/), and the fixed-queries trees. They use the pivot test and the ring form of the ball test.
- *Clustering-based indexes*, or compact partitions, pick centers and put each object with a nearby center, keeping a covering radius or the Voronoi-like rule: the generalized hyperplane tree, [GNAT](/gnat/), the [M-tree](/m-tree/), the list of clusters, the spatial approximation tree. They use the ball test and the hyperplane test.

**The curse of intrinsic dimension.** All tests compare differences of distances with $r$. When the distances from a pivot to the data are concentrated near their mean, almost every difference $|t - d(x, p)|$ is small, and few objects are excluded. Chávez and his coauthors measure this by the **intrinsic dimensionality** $\rho = \mu^2 / (2\sigma^2)$, where $\mu$ and $\sigma^2$ are the mean and the variance of the histogram of distances, and show that the cost of pivot-based and clustering-based search grows with it. For uniform random vectors in $[0, 1]^D$ with the Euclidean distance, the mean distance grows like $\sqrt{D/6}$ while the standard deviation stays near 0.24, so $\rho$ grows linearly in $D$.

**A lower bound.** In this model no index can beat $n$ evaluations in the worst case: the adversary on the [range query](/similarity-range-query/) page builds $2^n$ queries, indistinguishable to any index, with different answers. All guarantees better than $n$ are either for restricted metrics, such as those of bounded expansion or doubling dimension (the [cover tree](/cover-tree/)), or for average cases, or are approximate.

## Examples

**Distance concentration.** For 400 random points uniform in $[0, 1]^D$, the pairwise Euclidean distances have, in one sample, the following mean, standard deviation and $\rho$:

| $D$ | mean $\mu$ | standard deviation $\sigma$ | $\sigma / \mu$ | $\rho = \mu^2 / 2\sigma^2$ |
|---|---|---|---|---|
| 2 | 0.525 | 0.250 | 0.475 | 2.2 |
| 10 | 1.281 | 0.246 | 0.192 | 13.6 |
| 100 | 4.086 | 0.246 | 0.060 | 137.7 |

In dimension 100 almost every distance is within $4.09 \pm 0.5$. A pivot test with radius $r$ excludes an object only if its distance to the pivot differs from the query's by more than $r$, and a radius large enough to contain the nearest neighbor is a large fraction of the spread, so a pivot excludes little.

**The same tests in four indexes.**

| index | stored per object | partition | test at query time |
|---|---|---|---|
| [pivot table](/pivot-based-indexing/) | $t$ distances to pivots | none | pivot test with all $t$ pivots |
| [vantage-point tree](/vantage-point-tree/) | the median distance at each node | by the median of $d(\cdot, v)$ | ring form of the ball test |
| [GNAT](/gnat/) | distance ranges between split points and classes | nearest of $m$ split points | ranges, a pivot test on classes |
| [M-tree](/m-tree/) | covering radius and distance to the parent center | nearest center, with splits | ball test, and the pivot test with the parent center |

**Non-metric failure.** With the squared Euclidean distance on the line, the points $0$, $1$ and $2$ have $d(0, 2) = 4 > d(0, 1) + d(1, 2) = 2$. A ball test with center $1$ and radius $\rho = 1$ (which covers $0$ and $2$), a query at $q = 4$ and $r = 4$, computes $d(q, 1) = 9 > r + \rho = 5$ and excludes the ball, although $d(q, 2) = 4 \le r$.

## Where it is used

- **Strings and sequences** with the [edit distance](/edit-distance/): spelling correction, deduplication of names, search in sequence data, with [BK-trees](/bk-tree/) and pivot tables.
- **Images, audio and video** with perceptual or learned distances, in content-based retrieval; the M-tree and the MVP-tree were designed for this.
- **Sets and documents** with the Jaccard distance, and **trees and graphs** with edit distances, where no vector representation is natural.
- **Vectors of moderate dimension** where a [k-d tree](/kd-tree/) is not suitable because the distance is not a coordinate distance: [ball trees](/ball-tree/) and [cover trees](/cover-tree/) are used for [k-nearest neighbors](/k-nearest-neighbors/) classification and for density estimation.
- **As a filter** before an exact but expensive comparison, for example a cheap metric lower bound used as a pivot distance.

## References
