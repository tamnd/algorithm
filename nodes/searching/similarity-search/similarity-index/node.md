---
tag: PYYQQH
kind: abstract-type
slug: similarity-index
name: Similarity index
aliases:
- nearest neighbor index
- metric index
area: searching/similarity-search
level: intro
summary: An abstract structure supporting insertion of objects and nearest or range queries under a distance.
prereqs: [metric-space, spatial-index]
see_also: [similarity-range-query, k-nearest-neighbor-search, metric-space-indexing, vantage-point-tree, m-tree, locality-sensitive-hashing, hnsw, triangle-inequality]
sources:
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 2, the range query and the k nearest neighbor query; the cost model that counts distance evaluations; the survey of the index families)
  - book: isbn:9780387291468
    title: Pavel Zezula, Giuseppe Amato, Vlastislav Dohnal and Michal Batko, Similarity Search, The Metric Space Approach, Springer, 2006
    locator: Chapter 1 (the similarity queries, range, nearest neighbor, reverse nearest neighbor and similarity join) and Chapter 2, Survey of Existing Approaches
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data (Sections 4.1 and 4.2 on k nearest neighbor finding, and Section 4.5 on distance-based indexing)
  - paper: doi:10.1145/1143844.1143857
    title: Alina Beygelzimer, Sham Kakade and John Langford, Cover trees for nearest neighbor, Proceedings of the 23rd International Conference on Machine Learning (ICML), 2006
    locator: the bounds on insertion and query time in terms of the expansion constant
---

A similarity index is an abstract data type that holds a finite set of objects from a [metric space](/metric-space/) and answers queries by distance: report the objects within a radius of a query (a [similarity range query](/similarity-range-query/)), and report the $k$ objects nearest to a query ([k-nearest neighbor search](/k-nearest-neighbor-search/)). It is the [spatial index](/spatial-index/) without coordinates: the only thing it may do with two objects is compute their distance. Tree indexes such as the [vantage-point tree](/vantage-point-tree/) and the [M-tree](/m-tree/) answer exactly, and hashing and graph indexes such as [locality-sensitive hashing](/locality-sensitive-hashing/) and [HNSW](/hnsw/) answer approximately and faster.

## In plain words

A photo service holds millions of photos. For a new photo, it must find the photos that look most like it, or all photos that look almost the same. It has a program that says how different two photos are, as a number. It has no other way to compare photos.

A similarity index is the part of the system that does this job. You add objects to it. Later you give it an object and ask for the few most similar objects, or for all objects that are closer than some limit. A good index answers by measuring only a small part of the collection. Some indexes always give the exact answer. Others are faster but sometimes miss a correct object, and they report how often this happens.

## Operations

Fix a metric space $(M, d)$. An index value $S$ is a finite set of objects of $M$, each with an identifier; two objects may be equal as points of $M$ and still have different identifiers. For a query $q \in M$, write $r_k(q)$ for the $k$-th smallest value of $d(q, x)$ over $x \in S$, when $k \le |S|$.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}(d) \to S$ | the empty index for the distance $d$ |
| `insert` | $\text{insert}(S, x) \to S$ | adds the object $x$, with a new identifier |
| `delete` | $\text{delete}(S, x) \to S$ | removes the object with the identifier of $x$, if there is one |
| `range` | $\text{range}(S, q, r) \to$ set | $\{x \in S : d(q, x) \le r\}$ for a radius $r \ge 0$ |
| `knn` | $\text{knn}(S, q, k) \to$ list | $\min(k, \lvert S \rvert)$ objects in order of distance from $q$, with no object left out closer than one in the list |
| `size` | $\text{size}(S) \to \mathbb{N}$ | $\lvert S \rvert$ |

The nearest neighbor query is $\text{knn}(S, q, 1)$; the page [nearest neighbor search](/nearest-neighbor-search/) treats it. A *static* index is built once from a list and has no `insert` or `delete`. Many indexes add a bulk `build`, a [reverse nearest neighbor](/reverse-nearest-neighbor-search/) query, or a similarity join of two indexes.

**Approximate forms.** An approximate index replaces `knn` by one of these:

- `knn_c(S, q, k)` returns $L = [x_1, \ldots, x_m]$ with $m = \min(k, |S|)$ and $d(q, x_i) \le c \cdot r_i(q)$ for each $i$, for a fixed factor $c \ge 1$. This is the [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/) guarantee.
- A randomized index returns a correct answer with probability at least $1 - \delta$ for each query, over its own random choices, for a fixed $\delta$.
- A heuristic index, such as a graph index, gives no guarantee, and is judged by its *recall*: the fraction of the true $k$ nearest objects that it returns, averaged over a test set of queries.

### Example

Let $M$ be the strings with the unit-cost [edit distance](/edit-distance/), and insert the six strings cat, cart, card, dart, dog and coat.

| query | answer | why |
|---|---|---|
| $\text{range}(S, \text{cat}, 1)$ | $\{\text{cat}, \text{cart}, \text{coat}\}$ | the distances from cat are 0, 1, 2, 2, 3 and 1 in the order of insertion |
| $\text{knn}(S, \text{cat}, 2)$ | $[\text{cat}, \text{cart}]$ or $[\text{cat}, \text{coat}]$ | $r_2(\text{cat}) = 1$, and two objects are at distance 1 |
| $\text{knn}(S, \text{dot}, 1)$ | $[\text{dog}]$ | the distances from dot are 2, 3, 4, 2, 1 and 2 |
| after $\text{delete}(S, \text{dog})$, $\text{knn}(S, \text{dot}, 1)$ | $[\text{cat}]$, $[\text{dart}]$ or $[\text{coat}]$ | three objects are at distance 2 |

## Laws

For each index $S$, each object $x$ whose identifier is not in $S$, each query $q$, each radius $r \ge 0$ and each $k \ge 1$:

$$\begin{aligned}
&(\text{I1})\quad \text{range}(\text{new}(d), q, r) = \emptyset, \qquad \text{knn}(\text{new}(d), q, k) = [\,],\\
&(\text{I2})\quad \text{range}(\text{insert}(S, x), q, r) = \text{range}(S, q, r) \cup \{x\} \text{ if } d(q, x) \le r, \text{ and } \text{range}(S, q, r) \text{ otherwise},\\
&(\text{I3})\quad \text{range}(\text{delete}(\text{insert}(S, x), x), q, r) = \text{range}(S, q, r),\\
&(\text{I4})\quad r \le r' \implies \text{range}(S, q, r) \subseteq \text{range}(S, q, r'),\\
&(\text{I5})\quad \text{if } L = \text{knn}(S, q, k), \text{ then } |L| = \min(k, |S|),\ d(q, L_1) \le \cdots \le d(q, L_{|L|}), \text{ and } d(q, a) \le d(q, b) \text{ for } a \in L,\ b \in S \setminus L,\\
&(\text{I6})\quad \text{if } k \le |S| \text{ and } L = \text{knn}(S, q, k), \text{ then } \text{range}(S, q, r) \subseteq L \text{ for each } r < r_k(q), \text{ and } L \subseteq \text{range}(S, q, r_k(q)),\\
&(\text{I7})\quad \text{size}(\text{insert}(S, x)) = \text{size}(S) + 1, \qquad \text{size}(\text{delete}(\text{insert}(S, x), x)) = \text{size}(S).
\end{aligned}$$

Laws (I1) to (I3) fix `range` on every sequence of updates by induction on its length: the answer equals the answer of a plain list of the objects that are present. Law (I5) fixes the distances in the answer of `knn` but not the objects when several are at distance $r_k(q)$; an implementation may break such ties in any way, as the example shows. Law (I6) ties the two queries together. Its first half holds because an object $y \notin L$ with $d(q, y) < r_k(q)$ would be closer than $L_k$, against (I5). For an approximate index, (I5) is replaced by the guarantee of its form above, and (I6) does not hold.

**Order of inserts.** The answers depend only on the set of objects, not on the order of the inserts. The shape of a structure such as an [M-tree](/m-tree/) depends on the order, and so does its speed, but not its answers.

## Implementations

The costs count evaluations of $d$ for $n$ objects, in the worst case unless the table says otherwise; $m$ is the number of answers of a range query.

| implementation | build | insert | range | knn ($k = 1$) | space | answers |
|---|---|---|---|---|---|---|
| a list with a scan ([brute force](/brute-force-nearest-neighbor-search/)) | none | $O(1)$ | $n$ | $n$ | $O(n)$ | exact |
| [pivot table](/pivot-based-indexing/) with $t$ pivots (LAESA) | $nt$ | $t$ | $t$ plus the candidates, at most $n + t$ | the same | $O(nt)$ numbers | exact |
| [vantage-point tree](/vantage-point-tree/) | $O(n \log n)$ | static | $O(n)$ | $O(n)$ | $O(n)$ | exact |
| [M-tree](/m-tree/) with node capacity $b$ | by inserts | $O(b \cdot h)$, $h$ the height | $O(n)$ | $O(n)$ | $O(n)$ | exact |
| [BK-tree](/bk-tree/), integer distances | by inserts | $O(h)$ | $O(n)$ | $O(n)$ | $O(n)$ | exact |
| [cover tree](/cover-tree/) | by inserts | $O(c^6 \log n)$ | | $O(c^{12} \log n)$ | $O(n)$ | exact |
| [locality-sensitive hashing](/locality-sensitive-hashing/), for the $(r, cr)$-near neighbor problem | $O(n^{1+\rho} \log n)$ hash values | $O(n^{\rho} \log n)$ hash values | | $O(n^{\rho} \log n)$ hash values and $O(n^{\rho})$ distance evaluations | $O(n^{1 + \rho})$ | factor $c$; correct with probability at least $1 - 1/e - 1/3 \approx 0.299$ |
| [HNSW](/hnsw/), [navigable small world](/navigable-small-world/) graphs | by inserts | no proven bound | | no proven bound | $O(n)$ edges per layer | heuristic, measured by recall |

Here $c$ in the cover tree row is the expansion constant of the data set, defined on the page [intrinsic dimensionality](/intrinsic-dimensionality/); the bounds are those of Beygelzimer, Kakade and Langford. In the LSH row, $\rho < 1$ depends on the metric and on the approximation factor; for example $\rho = 1/c$ for the Hamming distance, as on the page of [bit sampling LSH](/bit-sampling-lsh/). The success probability is that of $L = \lceil n^{\rho} \rceil$ tables with a stop after $3L$ candidates, derived on the page [random hyperplane LSH](/random-hyperplane-lsh/); independent repetitions make it as close to 1 as needed. The exact tree indexes have a linear worst case, as the lower bound below shows, and they are fast only when the data has a low intrinsic dimension. For points of $\mathbb{R}^k$ with small $k$, a [k-d tree](/kd-tree/) is also a similarity index for the $\ell_p$ distances.

## Lower bounds

**No index beats the scan in a general metric space.** Count only evaluations of $d$ at query time, and let the preprocessing be free and unlimited. Let $S$ hold $n$ objects with $d(x, y) = 1$ for all distinct $x, y \in S$. Fix any deterministic query algorithm, or a randomized one that is always correct, and a query $q$. The adversary answers $d(q, x) = 1$ for each object that the algorithm evaluates, as long as at least one object $z$ is not evaluated. Both of these metrics on $S \cup \{q\}$ are consistent with all the answers given: the one with $d(q, x) = 1$ for all $x$, and the one with $d(q, z) = \varepsilon$ for some $0 < \varepsilon < 1$ and $d(q, x) = 1$ for the others. The second one is a metric, since each triangle has sides $\{1, 1, 1\}$ or $\{\varepsilon, 1, 1\}$, and $1 \le 1 + \varepsilon$ and $\varepsilon \le 2$. In the second metric, $z$ is the unique nearest object and the only answer of $\text{range}(S, q, \varepsilon)$. So an algorithm that stops before it evaluates all $n$ objects is wrong on one of the two metrics. This holds for every approximation factor $c$, since $c \cdot \varepsilon < 1$ for small $\varepsilon$. An index can do better only on metrics with more structure, for example a low [intrinsic dimensionality](/intrinsic-dimensionality/), which the discrete metric does not have.

**Coordinates.** In $\mathbb{R}^k$ with the Euclidean distance, the lower bounds of [k-nearest neighbor search](/k-nearest-neighbor-search/) apply: $\Omega(\log n)$ per query in a decision tree model, and no exact index with total time $O(n^{2 - \varepsilon})$ for $n$ queries in dimension $c \log n$ under the Strong Exponential Time Hypothesis.

## References
