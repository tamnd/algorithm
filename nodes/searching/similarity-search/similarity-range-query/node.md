---
tag: M07D5S
kind: problem
slug: similarity-range-query
name: Similarity range query
aliases:
- metric range query
- range query in metric space
area: searching/similarity-search
level: core
summary: Report all objects whose distance to the query is at most a threshold.
prereqs: [metric-space, nearest-neighbor-search]
see_also: [fixed-radius-near-neighbors, nearest-neighbor-search, pivot-based-indexing, metric-space-indexing, similarity-index, bk-tree, vantage-point-tree, set-similarity-join]
sources:
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 2, the range query (q, r) and the cost model that counts distance evaluations, and the survey of pivot-based and clustering-based indexes)
  - book: isbn:9780387291468
    title: Pavel Zezula, Giuseppe Amato, Vlastislav Dohnal and Michal Batko, Similarity Search, The Metric Space Approach, Springer, 2006
    locator: Chapter 1, Foundations of Metric Space Searching (the range query and its relation to the nearest neighbor query)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, Section 4.5, Distance-Based Indexing Methods (range search in vp-trees, gh-trees, GNAT and M-trees)
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005
    locator: pages 357 to 365 (the reduction from CNF satisfiability to orthogonal vectors, the source of the orthogonal vectors hypothesis under SETH)
---

A similarity range query asks, for a finite set $P$ of $n$ objects in a [metric space](/metric-space/) $(U, d)$, a query object $q \in U$ and a radius $r \ge 0$, for every object of $P$ within distance $r$ of $q$: the set $P \cap B(q, r)$. It is the second basic query of [similarity search](/similarity-index/), next to [nearest neighbor search](/nearest-neighbor-search/). A scan answers it with $n$ distance evaluations, and for a general metric no index can do better in the worst case; indexes based on the [triangle inequality](/triangle-inequality/), such as [pivot tables](/pivot-based-indexing/), [vantage-point trees](/vantage-point-tree/) and [M-trees](/m-tree/), do much better on data of low [intrinsic dimension](/intrinsic-dimensionality/).

## In plain words

You type a word with a typo, and the spell checker should list every dictionary word that is at most one or two edits away. You have a photo and want every stored photo that looks almost the same. In both cases there is a way to measure how far apart two objects are, and a limit. The answer is every object closer than the limit.

The simple way is to measure the distance from the query to every object. Faster methods prepare the collection in advance so that whole groups of objects can be skipped, because some measurement already shows that the group is too far away.

## Definition

Let $(U, d)$ be a metric space, and $P \subseteq U$ a finite set of $n$ objects, given in advance. A **range query** $(q, r)$, with $q \in U$ and $r \ge 0$, asks for

$$R(q, r) = \{\, x \in P : d(q, x) \le r \,\},$$

the objects of $P$ in the closed ball $B(q, r)$. Write $\kappa = |R(q, r)|$ for the output size. The radius is part of the query, unlike in the [fixed-radius near neighbors](/fixed-radius-near-neighbors/) problem, where it is fixed when the index is built.

**Cost model.** In the metric setting, the index may store anything computed from $P$ and the distances between its objects, but at query time it learns about $q$ only through evaluations of $d(q, \cdot)$, and the cost of a query is the number of these evaluations. This is the model of Chávez, Navarro, Baeza-Yates and Marroquín, for distances that are expensive, such as the [edit distance](/edit-distance/). In $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/), the model is the [real RAM](/real-ram/), and the cost is the time.

## Variants

- **Counting and emptiness.** Report only $\kappa$, or only whether $\kappa > 0$.
- **Open balls.** Report the objects with $d(q, x) < r$. For integer distances this is the closed query with radius $r - 1$.
- **Similarity threshold.** For a similarity $s$, report $\{x : s(q, x) \ge \tau\}$. For the [Jaccard similarity](/jaccard-similarity/) this is the range query with radius $1 - \tau$ for the Jaccard distance $1 - J$, which is a metric; for the [cosine similarity](/cosine-similarity/) it is the range query with radius $\arccos \tau$ for the angle.
- **Approximate range query.** For $\varepsilon > 0$, report every object within $r$ and possibly some within $(1 + \varepsilon) r$, but none farther.
- **Range join.** For two sets, report all pairs within distance $r$: the [similarity join](/set-similarity-join/), or for one set the [all-pairs similarity search](/all-pairs-similarity-search/).
- **Orthogonal range query.** In $\mathbb{R}^d$, report the points in an axis-parallel box. This is a different problem, solved by [k-d trees](/kd-tree/) and range trees; a box is a ball of the $\ell_\infty$ distance only when all its sides are equal.

## Examples

**Edit distance.** Let $P = \{$cart, card, dart, dog, coat, bat, cost$\}$ with the [edit distance](/edit-distance/), and $q =$ cat.

| object | cart | card | dart | dog | coat | bat | cost |
|---|---|---|---|---|---|---|---|
| $d(q, x)$ | 1 | 2 | 2 | 3 | 1 | 1 | 2 |

So $R(q, 0) = \emptyset$, $R(q, 1) = \{$cart, coat, bat$\}$ with $\kappa = 3$, and $R(q, 2)$ adds card, dart and cost, for $\kappa = 6$. A spell checker uses a radius of 1 or 2.

**The plane.** Let $P = \{(0,0), (4,0), (2,3), (5,4), (1,5)\}$ with the Euclidean distance and $q = (3, 1)$. The distances are $3.1623$, $1.4142$, $2.2361$, $3.6056$ and $4.4721$, so $R(q, 2.5) = \{(4, 0), (2, 3)\}$, and the nearest neighbor $(4, 0)$ is the only answer for $r = 2$.

## Known algorithms

| method | model | query cost | notes |
|---|---|---|---|
| scan | any metric | $n$ evaluations | exact, no index, the baseline |
| [pivot table](/pivot-based-indexing/) (LAESA) | any metric | $t$ evaluations plus one per object that passes the filter | exact; $O(nt)$ extra arithmetic per query |
| AESA | any metric | close to constant in experiments | exact; $n(n-1)/2$ stored distances |
| [vantage-point tree](/vantage-point-tree/), [MVP-tree](/mvp-tree/) | any metric | data dependent, $n$ in the worst case | exact; ball partitions |
| [GNAT](/gnat/), generalized hyperplane trees | any metric | data dependent, $n$ in the worst case | exact; hyperplane partitions |
| [M-tree](/m-tree/) | any metric | data dependent, $n$ in the worst case | exact; balanced, dynamic, paged |
| [BK-tree](/bk-tree/) | integer metric | data dependent, $n$ in the worst case | exact; children by distance |
| [k-d tree](/kd-tree/) search with pruning by the ball | $\mathbb{R}^d$, real RAM | data dependent | exact; good for small $d$ |
| [locality-sensitive hashing](/locality-sensitive-hashing/) | Hamming, angle, $\ell_2$ | sublinear expected per reported point | each answer is found with a fixed probability |

All the exact metric indexes prune with the same rule, the lower bound $d(q, x) \ge |d(q, p) - d(p, x)|$ of the [triangle inequality](/triangle-inequality/) for some precomputed pivot or center $p$: a region whose lower bound exceeds $r$ is skipped. Their query costs depend on the distribution of distances, and grow toward $n$ as the [intrinsic dimension](/intrinsic-dimensionality/) grows or as $r$ approaches the typical distance.

## Bounds

**Every object, in the worst case.** In the evaluation model, every algorithm that is always correct, deterministic or randomized, uses $n$ evaluations on some input, even with an index built in advance. Let $P$ have $n$ objects at pairwise distance 2, and let $r = 1$. For each subset $S \subseteq P$, the distances $d(q, x) = 1$ for $x \in S$ and $d(q, x) = 2$ for $x \notin S$, together with those of $P$, form a metric: every triangle has sides in $\{1, 2\}$, so the longest side is at most the sum of the other two. The index sees the same $P$ for every $S$, and the answer is $R(q, 1) = S$. An algorithm that does not evaluate $d(q, x)$ for some $x$ gives the same output for $S$ and $S \triangle \{x\}$, and so is wrong for one of them.

**Output size.** Any algorithm in the real RAM that reports the answers spends $\Omega(\kappa)$ time to write them; output-sensitive bounds have the form $f(n) + O(\kappa)$.

**High dimension, conditional.** Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), for every $\varepsilon > 0$ there is a $c$ such that no algorithm answers $n$ range emptiness queries for the Hamming distance on $n$ points of $\{0,1\}^{d}$, $d = c \log n$, in total time $O(n^{2 - \varepsilon})$, preprocessing included. The reason is the reduction from [orthogonal vectors](/orthogonal-vectors/) given below; Williams showed that a fast algorithm for orthogonal vectors would refute SETH.

## Reductions

- **Orthogonal vectors to Hamming range emptiness.** For $a, b \in \{0, 1\}^d$, let $\bar b = 1 - b$. Then the [Hamming distance](/hamming-distance/) is $H(a, \bar b) = d - |a| - |b| + 2\, a \cdot b$, so $a \cdot b = 0$ if and only if $H(a, \bar b) \le d - |a| - |b|$. Split the two sets of vectors by their weights into $(d+1)^2$ pairs of classes. For the class pair of weights $(\alpha, \beta)$, build an index on $\{\bar b : |b| = \beta\}$ and query each $a$ with $|a| = \alpha$ and the radius $d - \alpha - \beta$. A nonempty answer is an orthogonal pair. So $n$ range emptiness queries per class pair decide orthogonal vectors with a factor of $(d + 1)^2 = O(\log^2 n)$.
- **Nearest neighbor to range queries.** For integer distances in $\{0, \ldots, D\}$, binary search over $r$ with emptiness queries finds the distance of the [nearest neighbor](/nearest-neighbor-search/) in $\lceil \log_2 (D + 1) \rceil$ queries, and a range query at that radius returns it.
- **Range query to nearest neighbor search, with deletions.** Repeatedly find the nearest neighbor, report it if it is within $r$, and delete it; this uses $\kappa + 1$ queries on a dynamic structure. Incremental nearest neighbor search does the same without deletions.
- **Disk in the plane to a half space in $\mathbb{R}^3$.** Map $x \in \mathbb{R}^2$ to $\hat x = (x, \lVert x \rVert^2)$. Then $\lVert q - x \rVert^2 \le r^2$ if and only if $\lVert x \rVert^2 - 2\, q \cdot x + \lVert q \rVert^2 - r^2 \le 0$, that is, $\hat x$ lies on or below the plane $z = 2\, q \cdot x - \lVert q \rVert^2 + r^2$. So circular range reporting in the plane is half-space range reporting in three dimensions.
- **Similarity to distance.** A threshold query on a similarity becomes a range query when the similarity is a decreasing function of a metric, as for the Jaccard similarity and the cosine similarity in Variants.

## Applications

- **Spelling correction and fuzzy search.** All words within edit distance 1 or 2 of a misspelled word, with a [BK-tree](/bk-tree/) or a filter by $q$-grams.
- **Near-duplicate detection.** All documents whose [MinHash](/minhash/) or [SimHash](/simhash/) fingerprints are within a threshold of a new document.
- **Density-based clustering.** DBSCAN asks, for each point, for its neighbors within a radius $\varepsilon$, and labels points with many neighbors as cores.
- **Chemistry and biology.** All molecules whose fingerprints have a Tanimoto similarity above a threshold with a query, and all sequences within a small distance of a read.
- **Record linkage.** All records whose names or addresses are within a small distance of a given record.

## References
