---
tag: ZXNRMC
kind: concept
slug: shallow-cutting
name: Shallow cutting
aliases:
- Matousek shallow cutting
- shallow cutting lemma
- k-shallow cutting
area: geometry/range-searching
level: research
summary: Cutting of size linear in the number of shallow hyperplanes, used for halfspace range reporting.
prereqs: [geometric-cutting, halfspace-range-searching]
see_also: [geometric-cutting, halfspace-range-searching, circular-range-searching, k-nearest-neighbor-search, epsilon-net-theorem, partition-theorem, range-emptiness-query, dominance-counting]
sources:
  - paper: doi:10.1016/0925-7721(92)90006-E
    title: Jiří Matoušek, Reporting points in halfspaces, Computational Geometry, Theory and Applications 2(3), 1992, pages 169 to 186
    locator: the shallow cutting lemma, size O(r^floor(d/2)) for the (<= n/r)-level, and halfspace reporting in d dimensions
  - paper: doi:10.1007/BF02187740
    title: Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4, 1989, pages 387 to 421
    locator: the bound O(n^floor(d/2) k^ceil(d/2)) on the number of vertices of level at most k (DOI to be checked)
  - paper: doi:10.1137/S0097539798349188
    title: Timothy M. Chan, Random sampling, halfspace range reporting, and construction of (<= k)-levels in three dimensions, SIAM Journal on Computing 30(2), 2000, pages 561 to 575
    locator: halfspace reporting in three dimensions with shallow cuttings at all scales (DOI to be checked)
  - paper: doi:10.1137/1.9781611973068.21
    title: Peyman Afshani and Timothy M. Chan, Optimal halfspace range reporting in three dimensions, Proceedings of the 20th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2009, pages 180 to 186
    locator: O(n) space and O(log n + k) query from shallow cuttings in three dimensions (DOI to be checked)
  - paper: doi:10.1007/s00454-016-9784-4
    title: Timothy M. Chan and Konstantinos Tsakalidis, Optimal deterministic algorithms for 2-d and 3-d shallow cuttings, Discrete and Computational Geometry 56(4), 2016, pages 866 to 881
    locator: deterministic construction of shallow cuttings in three dimensions in O(n log n) time for all scales (DOI to be checked)
---

A shallow cutting covers only the part of an arrangement of hyperplanes that lies near the bottom, and in exchange it is much smaller than an ordinary [cutting](/geometric-cutting/). For a set $H$ of $n$ hyperplanes in $\mathbb{R}^d$, the points with at most $k$ hyperplanes below them form the $(\le k)$-level. Matoušek's shallow cutting lemma says that this region can be covered by $O((n/k)^{\lfloor d/2 \rfloor})$ simplices, each crossed by $O(k)$ hyperplanes, while covering all of space needs $\Theta((n/k)^{d})$. In three dimensions the size is $O(n/k)$, linear in $n/k$. By duality, reporting the points of a set in a halfspace becomes reporting the hyperplanes below a point of level $k$, where $k$ is the output size; so shallow cuttings give [halfspace range reporting](/halfspace-range-searching/) in $O(\log n + k)$ time in $\mathbb{R}^3$ and, through lifting, [disk range reporting](/circular-range-searching/) and [k-nearest neighbor search](/k-nearest-neighbor-search/) in the plane.

## In plain words

Picture many flat sheets in space, each tilted a little. Pick a spot and count how many sheets lie below it; that number is how deep the spot is. Often only spots with a low count matter, for example when the answer to a question is a short list.

An ordinary cutting splits all of space into pieces that few sheets pass through. A shallow cutting does this only near the bottom, for spots with a low count. That region is much simpler than the whole of space, so far fewer pieces are needed. In space of three dimensions, the number of pieces is about the number of sheets divided by the allowed count. For a spot inside a piece, the sheets below it are all among the few that pass through that piece, so they can be found by looking only at that piece's short list.

## The idea

**Levels.** Let $H$ be a set of $n$ non-vertical hyperplanes in $\mathbb{R}^d$. The **level** of a point $q$ is the number of hyperplanes of $H$ that pass strictly below $q$. The **$(\le k)$-level** is the set of points of level at most $k$. Clarkson and Shor (1989) proved that the number of vertices of the arrangement of $H$ with level at most $k$ is $O(n^{\lfloor d/2 \rfloor} (k + 1)^{\lceil d/2 \rceil})$, while the whole arrangement has $\Theta(n^d)$ vertices in general position. So the bottom of an arrangement is much simpler than the rest when $d \ge 2$.

**Shallow cuttings.** Let $1 \le r \le n$ and $k = n/r$. A **shallow $(1/r)$-cutting** for $H$ is a set of simplices with disjoint interiors whose union contains the $(\le k)$-level, such that each simplex is crossed by at most $n/r$ hyperplanes of $H$. The set of hyperplanes crossing a simplex is its **conflict list**.

**The shallow cutting lemma (Matoušek 1992).** For each fixed $d$ there is a constant $C$ such that for every set $H$ of $n$ hyperplanes in $\mathbb{R}^d$ and every $1 \le r \le n$, there is a shallow $(1/r)$-cutting for $H$ covering the $(\le n/r)$-level with at most $C r^{\lfloor d/2 \rfloor}$ simplices.

The count matches the Clarkson-Shor bound: each simplex holds $O((n/r)^d)$ vertices of its own conflict list, and the $O(n^{\lfloor d/2 \rfloor} (n/r)^{\lceil d/2 \rceil})$ vertices of level at most $n/r$ need $O(r^{\lfloor d/2 \rfloor})$ simplices. The proof follows the random sampling construction of ordinary cuttings: sample, triangulate only the cells of the sample arrangement near the bottom, and refine the heavy ones; the Clarkson-Shor bound limits the number of shallow cells.

**The vertical form in three dimensions.** For reporting, each cell is taken to be a vertical prism unbounded below: the set of points below a triangle. Here the conflict list of a prism is the set of planes that meet the closed prism. A non-vertical plane meets it exactly when it passes on or below some point of its top triangle, hence on or below one of the three corners; so every plane on or below a point $q$ of the prism is in its conflict list, and the list has size at most the sum of the closed levels of the three corners. With $k = n/r$, there are $O(n/k)$ such prisms covering the $(\le k)$-level, with conflict lists of size $O(k)$.

**A simple reporting structure in $\mathbb{R}^3$.** Let $P$ be a set of $n$ points. By duality the query "report the points of $P$ in a halfspace" becomes "report the planes of a set $H$ below a point $q$", and the output size is the level of $q$ (counting the planes through $q$ as below for closed ranges). For $j = 0, 1, \dots, \lceil \log_2 n \rceil$, build a vertical shallow cutting for $k_j = 2^j$, with a point location structure for its prisms and their conflict lists.

- **Space.** Level $j$ has $O(n / 2^j)$ prisms and conflict lists of size $O(2^j)$, so $O(n)$ words; over all levels, $O(n \log n)$.
- **Query.** For $j = 0, 1, \dots$: locate $q$ among the prisms of level $j$. If a prism contains $q$, scan its conflict list, report the planes below $q$, and stop. The answer is complete, because every plane below $q$ crosses that prism. If the level of $q$ is $k$, the search stops at the latest at $j = \lceil \log_2 \max(k, 1) \rceil$, since $q$ is then in the $(\le 2^j)$-level. The cost is $O(\log n)$ for each point location and $O(2^j) = O(k + 1)$ for the scan, so $O(\log n \log(k + 2) + k)$ worst case.

Afshani and Chan (2009) improved this to $O(n)$ space and $O(\log n + k)$ query time, which is optimal. In $d \ge 4$ dimensions, Matoušek's structure uses shallow cuttings in a partition tree and reports in $O(n^{1 - 1/\lfloor d/2 \rfloor} \log^{O(1)} n + k)$ time with near-linear space.

## Examples

**Sizes.** The table compares the number of cells of an ordinary $(1/r)$-cutting with that of a shallow one, for fixed $d$.

| dimension $d$ | ordinary cutting, all of $\mathbb{R}^d$ | shallow cutting, the $(\le n/r)$-level |
|---|---|---|
| 1 | $O(r)$ | $O(1)$ |
| 2 | $O(r^2)$ | $O(r)$ |
| 3 | $O(r^3)$ | $O(r)$ |
| 4 | $O(r^4)$ | $O(r^2)$ |
| 5 | $O(r^5)$ | $O(r^2)$ |

In $\mathbb{R}^1$ the hyperplanes are numbers and the $(\le k)$-level is the half-line up to the $(k+1)$-th smallest number, so a single cell crossed by $k$ hyperplanes covers it.

**A query by duality.** Map each point $(a, b)$ of $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ to the line $y = a x - b$. The point $(a, b)$ lies on or above the line $y = u x - v$ exactly when $a u - b \le v$, that is, when the dual line passes on or below the dual point $(u, v)$. For the query "points on or above $y = x + 1$", the dual point is $(1, -1)$, and the dual lines on or below it are those of $(2,3)$, $(4,7)$ and $(3,8)$, with values $-1$, $-3$ and $-5$ at $x = 1$. So the output is these three points, and the dual point has level $k = 3$ in the closed sense; a structure for this query only looks at the bottom $3$ levels of the arrangement.

**How shallow the bottom is.** The $8$ dual lines have $26$ distinct crossing points. By the number of lines strictly below them, $2$ are at level $0$, $4$ at level $1$, $6$ at level $2$, $4$ at level $3$, $5$ at level $4$, $3$ at level $5$ and $2$ at level $6$ (computed exactly with rational arithmetic). In the plane the $(\le k)$-level has $O(n (k + 1))$ vertices, linear in $n$ for fixed $k$, while the whole arrangement has $\Theta(n^2)$.

## Where it is used

- **[Halfspace range reporting](/halfspace-range-searching/)** in $\mathbb{R}^3$ with $O(n)$ space and $O(\log n + k)$ query, and in higher dimensions with Matoušek's structure. Emptiness is the case $k = 0$, see [range emptiness query](/range-emptiness-query/).
- **Disks and nearest neighbors in the plane.** By the lifting map, disk reporting and [k-nearest neighbor search](/k-nearest-neighbor-search/) become halfspace reporting in $\mathbb{R}^3$; see [circular range searching](/circular-range-searching/).
- **Dynamic convex hulls in $\mathbb{R}^3$** and dynamic nearest neighbors in the plane, by Chan's structure with polylogarithmic amortized updates.
- **Approximate counting.** A shallow cutting of the right level gives a constant factor estimate of the number of points in a halfspace.
- **Orthogonal ranges.** Shallow cuttings also exist for three-dimensional dominance ranges, and give optimal structures for three-dimensional [dominance](/dominance-counting/) reporting and approximate counting.

## References
