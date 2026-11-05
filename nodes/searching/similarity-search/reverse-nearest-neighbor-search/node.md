---
tag: 95S34Y
kind: problem
slug: reverse-nearest-neighbor-search
name: Reverse nearest neighbor search
aliases:
- RNN query
- reverse k-NN
area: searching/similarity-search
level: advanced
summary: Find all points that have the query as one of their nearest neighbors.
prereqs: [nearest-neighbor-search, metric-space]
see_also: [nearest-neighbor-search, reverse-nearest-neighbor, all-nearest-neighbors, voronoi-diagram, similarity-range-query, k-nearest-neighbors, r-tree, delaunay-triangulation]
sources:
  - paper: doi:10.1145/342009.335415
    title: Flip Korn and S. Muthukrishnan, Influence sets based on reverse nearest neighbor queries, Proceedings of the 2000 ACM SIGMOD International Conference on Management of Data
    locator: pages 201 to 212 (the monochromatic and bichromatic RNN queries, influence sets, the bound of six answers in the plane, and the RNN-tree of nearest neighbor disks)
  - paper: "Ioana Stanoi, Divyakant Agrawal and Amr El Abbadi, Reverse nearest neighbor queries for dynamic databases, ACM SIGMOD Workshop on Research Issues in Data Mining and Knowledge Discovery (DMKD 2000)"
    locator: pages 44 to 53 (the six 60-degree regions around the query and the search with no precomputed nearest neighbor distances)
  - paper: "Yufei Tao, Dimitris Papadias and Xiang Lian, Reverse kNN search in arbitrary dimensionality, Proceedings of the 30th International Conference on Very Large Data Bases (VLDB 2004)"
    locator: pages 744 to 755 (the TPL algorithm, pruning by perpendicular bisectors for reverse k nearest neighbors in any dimension)
  - book: isbn:9780387291468
    title: Pavel Zezula, Giuseppe Amato, Vlastislav Dohnal and Michal Batko, Similarity Search, The Metric Space Approach, Springer, 2006
    locator: Chapter 1, Section 4, Similarity queries (the reverse nearest neighbor query among the query types of metric search)
---

A reverse nearest neighbor (RNN) query asks, for a set $P$ of $n$ points in a [metric space](/metric-space/) and a query point $q$, for the points of $P$ that would have $q$ as their [nearest neighbor](/nearest-neighbor-search/): the points $p$ for which no other point of $P$ is closer to $p$ than $q$ is. It measures the *influence* of $q$, for example the customers who would choose a new store over every existing one. The relation is not symmetric: the nearest neighbor of $q$ need not count $q$ as its nearest, and $q$ can have many reverse neighbors or none. In the Euclidean plane there are at most 6 answers, and an RNN query reduces to 6 nearest neighbor queries and 6 checks. In a general metric there can be $n$ answers, and an exact algorithm needs $n$ distance evaluations in the worst case.

## In plain words

A town has some cafes, and each person walks to the closest one. A new cafe wants to know who would switch to it: the people for whom the new cafe would be closer than their current favorite. Those people are the reverse nearest neighbors of the new cafe.

This is not the same as the people close to the new cafe. Someone who lives next door to an old cafe stays there, even if the new one is also near. Someone far away may switch if no cafe is near them at all. So the question is about each person's own best option, not about the new cafe's neighborhood. In the flat plane a point can be the closest one for at most six others, which gives a fast method: look in six directions around the new cafe and check one candidate in each.

## Definition

Let $(U, d)$ be a metric space and $P \subseteq U$ a finite set of $n$ points, given in advance. For $p \in P$ write $r_p = \min_{p' \in P \setminus \{p\}} d(p, p')$ for its nearest neighbor distance, with $r_p = \infty$ when $n = 1$. For a query $q \in U \setminus P$, the **monochromatic RNN query** asks for

$$\mathrm{RNN}(q) = \{\, p \in P : d(p, q) \le r_p \,\},$$

the points that would have $q$ as a nearest neighbor if $q$ were added to $P$, ties included. The **reverse $k$ nearest neighbor query** replaces $r_p$ by the distance from $p$ to its $k$-th nearest neighbor in $P \setminus \{p\}$; then $q$ would be among the $k$ nearest neighbors of each answer.

In the **bichromatic** version the points are of two kinds, sites $S$ and clients $C$, and the query is a site $q$, not in $S$:

$$\mathrm{BRNN}(q) = \{\, c \in C : d(c, q) \le d(c, s) \text{ for all } s \in S \,\},$$

the clients that would choose $q$ over every existing site. In the Euclidean plane this is the set of clients inside the cell of $q$ in the [Voronoi diagram](/voronoi-diagram/) of $S \cup \{q\}$. Costs are measured as in nearest neighbor search: in distance evaluations for a general metric, and in the real RAM for $\mathbb{R}^d$.

## Variants

- **Strict or tied.** With $d(p, q) < r_p$ instead of $\le$, the answers are the points whose unique nearest neighbor would be $q$. The bounds below hold for both.
- **Reverse $k$ nearest neighbors.** The answer set can have up to $6k$ points in the plane, and the threshold $r_p$ becomes the $k$-th nearest neighbor distance.
- **Bichromatic RNN.** Sites and clients, as above. This is the form used in facility planning.
- **Dynamic data.** Points are inserted and deleted between queries, which changes the values $r_p$ of the neighbors of the changed point. Precomputed thresholds then need maintenance.
- **Query in the data set.** If $q \in P$, take $r_p$ over $P \setminus \{p, q\}$ in the definition, so that each answer has $q$ as its nearest neighbor among the other points.

## Examples

Let $P = \{a, b, c, d, e, f\}$ in the plane with $a = (0, 0)$, $b = (4, 0)$, $c = (5, 3)$, $d = (1, 5)$, $e = (8, 1)$, $f = (9, 6)$, and $q = (3, 2)$.

| point | nearest in $P$ | $r_p$ | $d(p, q)$ | answer | angle around $q$ |
|---|---|---|---|---|---|
| a | b | 4 | 3.6056 | yes | 213.7° |
| b | c | 3.1623 | 2.2361 | yes | 296.6° |
| c | b | 3.1623 | 2.2361 | yes | 26.6° |
| d | c | 4.4721 | 3.6056 | yes | 123.7° |
| e | c | 3.6056 | 5.0990 | no | 348.7° |
| f | c | 5 | 7.2111 | no | 33.7° |

So $\mathrm{RNN}(q) = \{a, b, c, d\}$. The nearest neighbor of $q$ is $b$ or $c$, both at 2.2361. The point $e$ is no answer although its nearest neighbor $c$ is far from $e$; $q$ is farther still.

The six-region method splits the plane around $q$ into the half-open cones of angles $[0°, 60°)$, $[60°, 120°)$, and so on. The cone $[0°, 60°)$ holds $c$ and $f$, and its nearest point to $q$ is $c$; the cones $[120°, 180°)$, $[180°, 240°)$, $[240°, 300°)$ and $[300°, 360°)$ give $d$, $a$, $b$ and $e$; the cone $[60°, 120°)$ is empty. Checking the five candidates against their $r_p$ yields the four answers, and $f$ is never examined: as the lemma below shows, $c$ is closer to $f$ than $q$ is.

**A metric with $n$ answers.** Take $n$ points at pairwise distance 2 and a query at distance 1 from each, a metric since every triangle has sides 1, 1, 2 or 2, 2, 2 or 1, 2, 2. Every point has $r_p = 2 > 1$, so $\mathrm{RNN}(q) = P$.

## Known algorithms

- **Scan with thresholds.** Compute every $r_p$ in preprocessing, by an [all nearest neighbors](/all-nearest-neighbors/) algorithm, in $O(n \log n)$ time in the plane or $n(n-1)/2$ evaluations in a general metric. A query evaluates $d(p, q)$ for each $p$ and reports those with $d(p, q) \le r_p$: $n$ evaluations, exact, in any metric.
- **Disk stabbing (Korn and Muthukrishnan).** $p \in \mathrm{RNN}(q)$ if and only if $q$ lies in the closed ball $B(p, r_p)$. So index the $n$ balls, for example in an [R-tree](/r-tree/) of their bounding boxes (the RNN-tree), and report the balls that contain $q$. The thresholds must be updated when points change.
- **Six regions (Stanoi, Agrawal and El Abbadi).** In the Euclidean plane, for each of the six cones around $q$, find the nearest point of $P$ to $q$ in the cone with a constrained nearest neighbor search, and check each of the at most 6 candidates $p$ by one nearest neighbor query for $p$. With a nearest neighbor index of query time $T(n)$, this costs $O(T(n))$ and needs no thresholds, so it suits dynamic data.
- **Bisector pruning (TPL, Tao, Papadias and Lian).** Visit points in order of distance from $q$ with a best-first search on an R-tree. Each point $p$ found cuts away the half-space of points closer to $p$ than to $q$, by the perpendicular bisector of $pq$; a region of the index that lies in $k$ such half-spaces holds no reverse $k$ nearest neighbor and is skipped. It works in any dimension and for every $k$, and verifies the remaining candidates.
- **Bichromatic, by Voronoi cells.** Compute the Voronoi cell of $q$ among $S \cup \{q\}$ and report the clients in it, with a range search over the clients for the cell, a convex polygon in the plane.

## Bounds

**At most six in the plane.** *Lemma.* In the Euclidean plane, for $q \notin P$, each half-open cone of angle $60°$ with apex $q$ contains at most one point of $\mathrm{RNN}(q)$, so $|\mathrm{RNN}(q)| \le 6$; for reverse $k$ nearest neighbors the bound is $6k$.

*Proof.* Let $p \ne p'$ be in the same cone with $d(q, p) \le d(q, p')$, and let $\theta < 60°$ be the angle $pqp'$, so $\cos \theta > 1/2$. With $x = d(q, p) > 0$ and $y = d(q, p')$, the law of cosines gives $d(p, p')^2 = x^2 + y^2 - 2xy \cos\theta < x^2 + y^2 - xy \le y^2$, since $x \le y$. So $d(p', p) < d(p', q)$, and $r_{p'} < d(p', q)$: $p'$ is not an answer. For $k$, order the points of one cone by their distance to $q$. A point $p'$ after the first $k$ has $k$ points of its cone at distance less than $d(p', q)$ from it, by the same computation, so its $k$-th nearest neighbor distance is below $d(p', q)$ and it is not an answer. So each cone holds at most $k$ answers. $\square$

The bound is tight: the six vertices of a regular hexagon around its center $q$ all have $r_p = d(p, q)$, so they are all answers with ties. In $\mathbb{R}^d$ the same argument with caps of angular radius less than $30°$ bounds $|\mathrm{RNN}(q)|$ by the number of such cones needed to cover the sphere, which is finite for fixed $d$ but grows exponentially with $d$.

**Unbounded in a general metric.** The example of $n$ points at pairwise distance 2 has $n$ answers, so any algorithm that lists them takes $\Omega(n)$ time.

**$n$ evaluations in the worst case.** In the model that counts distance evaluations, every exact algorithm, even with an index built in advance and even randomized, evaluates $d(q, p)$ for all $n$ points on some input. Let the points be at pairwise distance 2, so $r_p = 2$ for all $p$, and for $X \subseteq P$ let $d(q, p) = 1$ for $p \in X$ and $d(q, p) = 3$ otherwise. Every triangle has sides in $\{1, 2, 3\}$ with $2$ between two points of $P$, and $1 + 2 \ge 3$, so this is a metric. The answer is $X$, and an algorithm that never evaluates $d(q, p)$ cannot tell $X$ from $X \triangle \{p\}$.

## Reductions

- **RNN to ball stabbing.** With the thresholds $r_p$ precomputed, $\mathrm{RNN}(q) = \{p : q \in B(p, r_p)\}$, a stabbing query on $n$ balls. It is a [range query](/similarity-range-query/) in which each data point carries its own radius.
- **Six regions to nearest neighbor search.** In the plane, the lemma reduces one RNN query to 6 constrained nearest neighbor queries from $q$ and at most 6 nearest neighbor queries from the candidates.
- **Bichromatic RNN to point location in a Voronoi cell.** $c \in \mathrm{BRNN}(q)$ if and only if $c$ lies in the Voronoi cell of $q$ in the diagram of $S \cup \{q\}$; in the plane, the cell is found from the [Delaunay triangulation](/delaunay-triangulation/) by inserting $q$.
- **All nearest neighbors to RNN.** The thresholds $r_p$ are the output of the [all nearest neighbors](/all-nearest-neighbors/) problem, and the [reverse nearest neighbor](/reverse-nearest-neighbor/) relation of the whole set is the reversed nearest neighbor graph.

## Applications

- **Facility location and marketing.** The bichromatic query gives the customers a new store would win from the existing ones, the influence set of Korn and Muthukrishnan.
- **Resource allocation.** A new server, base station or ambulance depot takes over the users for which it is nearest.
- **Outlier and hub detection.** In the $k$ nearest neighbor graph of a data set, points with no reverse neighbors are outliers, and points with many reverse neighbors are hubs; in high dimension, hubs spoil [k-nearest neighbor](/k-nearest-neighbors/) classification.
- **Document and profile matching.** A new document is relevant to the users whose profiles have it among their $k$ nearest documents.

## References
