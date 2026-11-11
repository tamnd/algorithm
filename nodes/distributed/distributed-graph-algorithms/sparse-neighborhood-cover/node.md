---
tag: FFF7KM
kind: concept
slug: sparse-neighborhood-cover
name: Sparse neighborhood cover
aliases:
- Awerbuch-Peleg sparse covers
area: distributed/distributed-graph-algorithms
level: research
summary: A family of clusters such that every ball of radius r lies inside one cluster, each cluster has diameter O(kr), and each node is in O(k n^(1/k)) clusters (Awerbuch and Peleg).
prereqs: [local-model, network-decomposition]
see_also: [network-decomposition, low-diameter-decomposition, synchronizer, ruling-set, frt-tree-embedding, distributed-shortest-paths]
sources:
  - paper: doi:10.1109/FSCS.1990.89571
    title: Baruch Awerbuch and David Peleg, Sparse partitions, FOCS 1990
    locator: pp. 503 to 513 (the coarsening theorem for covers, with radius O(k r) and overlap O(k n^(1/k)), and its uses)
  - book: doi:10.1137/1.9780898719772
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: the chapters on sparse covers and their constructions (the kernel growing algorithm and its analysis)
  - paper: doi:10.1145/135419.135456
    title: Baruch Awerbuch, Bonnie Berger, Lenore Cowen and David Peleg, Fast network decomposition, PODC 1992
    locator: distributed constructions of decompositions, from which covers follow
  - paper: doi:10.1007/BF01303516
    title: Nathan Linial and Michael Saks, Low diameter graph decompositions, Combinatorica 13(4), 1993
    locator: pp. 441 to 454 (randomized decompositions with O(log n) colours and O(log n) diameter, which give covers as on this page)
---

A sparse neighbourhood cover of a graph for a radius $r$ is a family of clusters, which may overlap, such that the ball of radius $r$ around every node lies entirely inside some cluster. It is sparse when every cluster has small diameter and every node is in few clusters. Awerbuch and Peleg (1990) showed that for every integer $k \ge 1$ there is a cover with diameter $O(k r)$ in which each node is in $O(k n^{1/k})$ clusters; with $k = \log n$ both costs are $O(\log n)$ factors.

Notation on this page: $G = (V, E)$ is an undirected graph with $n$ nodes, $\mathrm{dist}$ is the shortest path distance, and $B(v, r) = \{x : \mathrm{dist}(v, x) \le r\}$ is the ball of radius $r$ around $v$. A **cover** is a family $\mathcal{C}$ of sets of nodes. It **covers the $r$-neighbourhoods** if every $B(v, r)$ is a subset of some $C \in \mathcal{C}$. Its **radius** is the largest strong radius of a cluster, measured inside the cluster from a chosen start node, and its **overlap** is the largest number of clusters that contain one node.

## In plain words

A city wants local offices so that every person's whole neighbourhood is served by one office. One office per person would do it, but then a busy street is inside hundreds of office areas, and each resident must deal with all of them.

The fix is to merge offices. Start with one neighbourhood and keep adding the neighbourhoods that touch the area, as long as this makes the set of touching neighbourhoods much larger. When adding stops paying off, close the area. Each area grows only a few times, so it stays small, and the rule for stopping keeps the number of areas that share one street small.

There is a trade-off: allow larger areas, and each street is in fewer of them.

## The idea

**The trade-off.** There are two trivial covers. The family of all balls $B(v, r)$ has radius $r$ but overlap up to $n$. The single cluster $V$ has overlap 1 but radius up to the diameter of $G$. A sparse cover sits between them, and the parameter $k$ chooses the point: radius $(2k - 1) r$ and overlap at most $k n^{1/k}$.

**The construction (kernel growing).** Let $R$ be the set of centres whose balls are not covered yet; at first $R = V$. Work in phases. At the start of a phase let $N = |R|$, and call every centre of $R$ free. While a free centre $v$ exists:

1. Set $Y = \{v\}$.
2. Let $Z$ be the set of free centres $u$ whose ball $B(u, r)$ meets the kernel $\bigcup_{y \in Y} B(y, r)$.
3. If $|Z| > N^{1/k} |Y|$, set $Y = Z$ and go to step 2.
4. Otherwise output the kernel $\bigcup_{y \in Y} B(y, r)$ as a cluster with start node $v$, remove $Y$ from $R$, and make every centre of $Z$ not free until the phase ends.

*Claim.* The clusters cover the $r$-neighbourhoods, every cluster has strong radius at most $(2k - 1) r$ around its start node, and every node is in at most $k n^{1/k}$ clusters.

*Proof.* **Cover.** A centre leaves $R$ only as a member of some $Y$, and then its ball is a subset of the output cluster.

**Radius.** Each repeat of step 3 multiplies $|Y|$ by more than $N^{1/k}$, and $|Y| \le N$, so step 3 repeats at most $k - 1$ times. A centre added in the $j$-th repeat has a ball that meets the ball of a centre added before, so it is reached from $v$ by a chain of at most $j$ overlapping balls, along paths that stay inside these balls. Hence every centre of the final $Y$ is within $2 r (k - 1)$ of $v$ inside the cluster, and every node of the cluster is within $2 r (k - 1) + r = (2k - 1) r$.

**Overlap within a phase.** A centre $u$ that is still free after a cluster is output has a ball that does not meet that cluster, since otherwise $u$ would be in $Z$. The next kernels of the phase are built only from free centres, so the clusters of one phase are disjoint, and each node is in at most one of them.

**Number of phases.** Every free centre ends in exactly one $Z$, so the sets $Z$ of a phase split the $N$ centres, and $\sum |Y| \ge \sum |Z| / N^{1/k} = N^{1 - 1/k}$. So a phase takes $R$ from $N$ to at most $N - N^{1 - 1/k}$. The function $x \mapsto x^{1/k}$ is concave, so $N^{1/k} - (N - N^{1-1/k})^{1/k} \ge \frac{1}{k} N^{1/k - 1} \cdot N^{1 - 1/k} = \frac{1}{k}$. The quantity $|R|^{1/k}$ starts at $n^{1/k}$ and falls by at least $\frac{1}{k}$ per phase, so there are at most $k n^{1/k}$ phases, and a node is in at most one cluster per phase. $\blacksquare$

**From a network decomposition.** Let $(\mathcal{P}, \text{colours})$ be a $(C, D)$ [network decomposition](/network-decomposition/) of the power graph $G^{2r}$, where nodes at distance at most $2r$ are adjacent. For each part $P$, output the cluster $P^{+r} = \{x : \mathrm{dist}(x, P) \le r\}$. The ball $B(v, r)$ lies in the cluster of the part of $v$. A node $x$ in $P^{+r}$ and $Q^{+r}$ for two parts $P$, $Q$ of one colour would give nodes of $P$ and $Q$ at distance at most $2r$, which are adjacent in $G^{2r}$; this is not allowed. So the overlap is at most $C$, and the weak diameter is at most $2rD + 2r$. With the randomized [Linial-Saks](/network-decomposition/) decomposition, $C$ and $D$ are $O(\log n)$, which gives the case $k = \log n$ in $O(r \log^2 n)$ rounds of the [LOCAL](/local-model/) model, since each round on $G^{2r}$ costs $2r$ rounds on $G$.

**The view of a node.** A node is in few clusters, so it can afford to keep a little state for each of them, and for every $v$ some cluster sees the whole $r$-neighbourhood of $v$. This is the property that the uses below need: a local event near $v$ can be handled inside one cluster of small diameter.

## Examples

- **A path.** On a path of $n$ nodes with $r = 1$ and $k = \log_2 n$, $N^{1/k} \le 2$, and the construction merges neighbouring balls while the set of touching balls more than doubles. With $v = 0$: $Y = \{0\}$ meets 3 balls, so $Y = \{0, 1, 2\}$, whose kernel $\{0, 1, 2, 3\}$ meets 5 balls, which is not more than $2 \cdot 3$; so the first cluster is $\{0, 1, 2, 3\}$. The clusters are short subpaths, and the code on this page finds overlap 3 for $n = 32$ and 2 for $n = 64$ and $n = 128$, well below the bound $k n^{1/k} = 2 \log_2 n$.
- **$k = 1$.** Then $N^{1/k} = N \ge |Z|$, so $Y$ never grows; the clusters are exactly the balls $B(v, r)$, the radius is $r$, and the overlap is the largest ball size, which can be $n$ on a star.
- **A grid.** On a two-dimensional grid with radius $r$, squares of side about $4r$ placed in four shifted copies of a tiling cover every ball with overlap 4 and radius $O(r)$. On such graphs of bounded growth, much better covers than the general bound exist; the general bound matters on graphs such as expanders, where balls grow fast.
- **Partition versus cover.** A partition into clusters of radius $O(kr)$ cannot cover all balls in general, since a ball that meets two parts lies in neither; a cover allows overlap for this reason.

## Where it is used

- **Synchronizers.** Covers and partitions with small diameter and few edges between clusters give the cluster structure of [synchronizer](/synchronizer/) $\gamma$ and its relatives.
- **Tracking and directories.** Awerbuch and Peleg used covers for the tracking of mobile users and for distributed directories: a user that moves a short distance changes only the clusters near it, and a search for it looks in the clusters of growing radius around the searcher.
- **Compact routing and distance oracles.** Hierarchies of covers with radii $r = 2^i$ give routing schemes with small tables and small stretch, and related distance data structures.
- **Local algorithms in power graphs.** A problem that looks at distance $r$ can be solved inside clusters of a cover for radius $r$, with the overlap bounding the extra load per node. In this role, covers and [network decompositions](/network-decomposition/) can be built from each other.
- **Probabilistic versions.** A [low-diameter decomposition](/low-diameter-decomposition/) is a random partition in which each ball of radius $r$ is inside one cluster with good probability; repeating it gives covers.

## References
