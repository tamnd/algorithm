---
tag: CZCVDR
kind: abstract-type
slug: spatial-index
name: Spatial index
aliases:
- spatial access method
- multidimensional index
area: data-structures/spatial-structures
level: intro
summary: Abstract interface for storing geometric objects and answering spatial queries such as range, point and nearest-neighbor queries.
prereqs: [dictionary, asymptotic-notation]
see_also: [kd-tree, quadtree, r-tree, uniform-grid, range-tree, orthogonal-range-searching, nearest-neighbor-search, spatial-join]
sources:
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998, pp. 170 to 231
    locator: Section 2 (the basic queries, exact match, point query, window query, intersection, enclosure, containment, nearest neighbor and spatial join) and the classification into point access methods and spatial access methods
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Preface and Chapter 1, Multidimensional Point Data (the query types and the point structures), and Chapter 2, Object-Based and Image-Based Image Representations (structures for objects with extent)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Orthogonal Range Searching (k-d trees and range trees, and the Notes and Comments with the lower bounds)
  - paper: doi:10.1145/77600.77614
    title: Bernard Chazelle, Lower bounds for orthogonal range searching, I. The reporting case, Journal of the ACM 37(2), 1990, pp. 200 to 212
    locator: the main theorem (the space lower bound on the pointer machine for a query time of O(polylog n + k))
  - paper: doi:10.1145/1007568.1007608
    title: Lars Arge, Mark de Berg, Herman J. Haverkort and Ke Yi, The priority R-tree, a practically efficient and worst-case optimal R-tree, Proceedings of ACM SIGMOD 2004
    locator: the window query bound of the PR-tree and the lower bound for any R-tree
---

A spatial index is an abstract data type that holds a finite set of geometric objects, each with an identifier, and answers queries about where the objects are: which objects meet a query window, which objects contain a query point, and which objects are nearest to a query point. It is the [dictionary](/dictionary/) of geometry: the keys are points or regions of $\mathbb{R}^d$, and the queries ask about position instead of equality. The [k-d tree](/kd-tree/), the [quadtree](/quadtree/), the [R-tree](/r-tree/), the [uniform grid](/uniform-grid/) and [spatial hashing](/spatial-hashing/) all implement it, with different costs. Databases, map services, games and machine learning libraries use one under the name of spatial index or spatial access method.

## In plain words

A map application holds millions of shops, roads and parks. When you look at a part of the map, it must find the things in that part quickly, without looking at every thing it knows. When you ask for the closest coffee shop, it must find it without measuring the distance to every shop.

A spatial index is the part of the program that does this. You give it things with a shape and a name. It keeps them in some clever order. Later you ask it questions: what is inside this box, what covers this spot, what is closest to this spot. The index answers each question by looking only at a small part of what it holds. Many different structures can do this job. They differ in speed, in memory, and in how well they handle data that changes.

## Operations

Fix a dimension $d \ge 1$. An *object* is a pair $(id, g)$ of an identifier and a nonempty closed bounded set $g \subset \mathbb{R}^d$, its geometry. A point index allows only one-point sets $g = \{p\}$. A *box* is a set $[\ell_1, h_1] \times \cdots \times [\ell_d, h_d]$ with $\ell_i \le h_i$. A spatial index value $S$ is a finite set of objects with distinct identifiers. The distance from a point $q$ to a set $g$ is $\operatorname{dist}(q, g) = \min_{x \in g} \lVert q - x \rVert$ for a fixed norm, usually the Euclidean one.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to S$ | the empty index |
| `insert` | $\text{insert}(S, (id, g)) \to S$ | $S$ becomes $S \cup \{(id, g)\}$; $id$ is not yet in $S$ |
| `delete` | $\text{delete}(S, id) \to S$ | removes the object with identifier $id$, if there is one |
| `window` | $\text{window}(S, Q) \to$ set | for a box $Q$: $\{id : (id, g) \in S,\ g \cap Q \ne \emptyset\}$ |
| `point` | $\text{point}(S, q) \to$ set | $\{id : (id, g) \in S,\ q \in g\}$, the objects that a point stabs |
| `contained` | $\text{contained}(S, Q) \to$ set | $\{id : (id, g) \in S,\ g \subseteq Q\}$ |
| `nearest` | $\text{nearest}(S, q, k) \to$ list | $\min(k, |S|)$ identifiers in order of $\operatorname{dist}(q, g)$, such that no object left out is closer than one in the list |
| `size` | $\text{size}(S) \to \mathbb{N}$ | $|S|$ |

For a point index, `window` is [orthogonal range searching](/orthogonal-range-searching/) in its reporting form, `point` is an exact-match lookup, and `nearest` is [k-nearest neighbor search](/k-nearest-neighbor-search/). Some indexes add a *counting* form of `window` that returns only the number of answers, a *range of radius* query $\{id : \operatorname{dist}(q, g) \le r\}$, and a [spatial join](/spatial-join/) of two indexes. A *static* index has only a build operation from a list of objects, and no `insert` or `delete`.

Gaede and Günther call an index that stores only points a *point access method*, and an index that stores objects with extent a *spatial access method*. Most spatial access methods store each object by its [minimum bounding rectangle](/minimum-bounding-rectangle/) and answer a query in two steps: a *filter* step on the rectangles in the index, and a *refinement* step that tests the exact geometry of each candidate.

### Example

Insert five points: A at $(1, 1)$, B at $(4, 2)$, C at $(2, 5)$, D at $(6, 6)$ and E at $(5, 3)$.

| query | answer | why |
|---|---|---|
| $\text{window}(S, [2, 5] \times [1, 4])$ | $\{B, E\}$ | A has $x = 1 < 2$; C and D have $y > 4$ |
| $\text{point}(S, (4, 2))$ | $\{B\}$ | only B is at that point |
| $\text{nearest}(S, (3, 3), 2)$ | $[B, E]$ | the distances are B 1.414, E 2, C 2.236, A 2.828, D 4.243 |
| after $\text{delete}(S, B)$, $\text{nearest}(S, (3, 3), 1)$ | $[E]$ | B is gone, and E is the next closest |

## Laws

For each index $S$, each object $o = (id, g)$ with $id$ not in $S$, each box $Q$, each point $q$ and each $k \ge 1$:

$$\begin{aligned}
&(\text{S1})\quad \text{window}(\text{new}(), Q) = \emptyset, \qquad \text{nearest}(\text{new}(), q, k) = [\,],\\
&(\text{S2})\quad \text{window}(\text{insert}(S, o), Q) = \text{window}(S, Q) \cup \{id : g \cap Q \ne \emptyset\},\\
&(\text{S3})\quad \text{window}(\text{delete}(\text{insert}(S, o), id), Q) = \text{window}(S, Q),\\
&(\text{S4})\quad \text{point}(S, q) = \text{window}(S, [q, q]),\\
&(\text{S5})\quad \text{insert}(\text{insert}(S, o), o') = \text{insert}(\text{insert}(S, o'), o) \text{ for objects } o, o' \text{ with distinct identifiers},\\
&(\text{S6})\quad \text{if } L = \text{nearest}(S, q, k), \text{ then } |L| = \min(k, |S|) \text{ and } \operatorname{dist}(q, g_a) \le \operatorname{dist}(q, g_b) \text{ for each } a \in L,\ b \notin L,\\
&(\text{S7})\quad \text{size}(\text{insert}(S, o)) = \text{size}(S) + 1, \qquad \text{size}(\text{delete}(\text{insert}(S, o), id)) = \text{size}(S).
\end{aligned}$$

Here $[q, q]$ is the box that holds only the point $q$, and $g_a$ is the geometry of the object with identifier $a$. Laws (S1) to (S3) fix the answer of `window` on each sequence of updates, by induction on the length of the sequence: each answer equals the answer of a plain list of the objects that are still present. Law (S5) says the index is a set, so the order of the inserts does not change any answer, even though it can change the shape of a structure such as a [point quadtree](/point-quadtree/) or an R-tree. Law (S6) fixes the distances in the answer of `nearest`, but not the identifiers when two objects are at the same distance: an implementation may break such ties in any way.

**Filter and refinement.** If an index stores the box $b(g) \supseteq g$ in place of $g$, the filter step returns $C = \{id : b(g) \cap Q \ne \emptyset\}$. Since $g \cap Q \subseteq b(g) \cap Q$, the true answer is a subset of $C$, so the refinement step that tests $g \cap Q \ne \emptyset$ for each $id \in C$ returns exactly the set of (S2). The filter step can only give false candidates, never miss an answer.

## Implementations

The costs are for $n$ points in a fixed dimension $d$ and a window query with $k$ answers. They are worst case unless the table says otherwise.

| implementation | build | insert or delete | window | nearest ($k = 1$) | space |
|---|---|---|---|---|---|
| list of all objects | $O(n)$ | $O(1)$ insert, $O(n)$ delete | $O(n)$ | $O(n)$ | $O(n)$ |
| [uniform grid](/uniform-grid/), [spatial hashing](/spatial-hashing/) | $O(n)$ expected with hashing | $O(1)$ expected | $O(k + $ cells met$)$ | depends on the data | $O(n +$ cells$)$ |
| [k-d tree](/kd-tree/) (balanced, static) | $O(n \log n)$ | not balanced by updates | $O(n^{1 - 1/d} + k)$ | $O(\log n)$ expected on random points | $O(n)$ |
| [quadtree](/quadtree/), [octree](/octree/) (point-region) | $O(n D)$ | $O(D)$ | $O(n D)$, no better bound in $n$ | depends on the data | $O(n D)$ |
| [range tree](/range-tree/), [layered range tree](/layered-range-tree/) (static) | $O(n \log^{d-1} n)$ | static | $O(\log^{d} n + k)$, or $O(\log^{d-1} n + k)$ layered | | $O(n \log^{d-1} n)$ |
| [R-tree](/r-tree/) and its variants | $O(n \log n)$ by [bulk loading](/bulk-loading/) | $O(\log n)$ nodes on the path, plus splits | $O(n)$ in the worst case | $O(n)$ in the worst case | $O(n)$ |
| [priority R-tree](/priority-r-tree/) (static) | $O(n \log n)$ | static | $O(n^{1 - 1/d} + k)$ node visits | | $O(n)$ |

Here $D$ is the number of halvings from the root cell to the smallest cell, which depends on the coordinates and not on $n$. The R-tree has no good worst-case bound, but its nodes fit disk pages, its leaves are all at one depth, and it stores objects with extent, so it is the index of most spatial databases. The k-d tree and the grid are the common choices in memory for points. In high dimensions all these structures degrade toward a scan, by the [curse of dimensionality](/curse-of-dimensionality/); [approximate nearest neighbor](/approximate-nearest-neighbor/) methods and [locality-sensitive hashing](/locality-sensitive-hashing/) are used there.

## Lower bounds

- **Comparison model.** In one dimension, a window query is a range query on a sorted set, and the exact-match query alone needs $\Omega(\log n)$ comparisons in the worst case, as [binary search](/binary-search/) does. So no comparison-based index answers `point` in $o(\log n)$ worst-case time. Hashing in the [word RAM](/word-ram/) avoids this bound for exact matches only.
- **R-trees.** An R-tree visits a node exactly when the node's rectangle meets the query, so its cost depends on how the rectangles are grouped. Arge, de Berg, Haverkort and Yi prove that each R-tree on some set of $N$ rectangles in $d$ dimensions needs $\Omega((N/B)^{1 - 1/d} + T/B)$ page reads for some window query with $T$ answers, where $B$ is the page capacity, and the [priority R-tree](/priority-r-tree/) meets this bound. For the k-d tree the matching bound $O(n^{1 - 1/d} + k)$ is on the [k-d tree range query complexity](/kd-tree-range-query-complexity/) page.
- **Pointer machine.** Chazelle proved that on the [pointer machine](/pointer-machine/), an index for orthogonal range reporting in $d$ dimensions with query time $O(\log^c n + k)$ needs $\Omega(n (\log n / \log \log n)^{d-1})$ space. So the extra space of the range trees over the linear-space trees cannot be removed while keeping polylogarithmic queries.

## References
