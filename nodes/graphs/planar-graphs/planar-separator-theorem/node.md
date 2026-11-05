---
tag: RH0N4B
kind: theorem
slug: planar-separator-theorem
name: Planar separator theorem
aliases:
- Lipton-Tarjan separator theorem
area: graphs/planar-graphs
level: core
summary: Every planar graph on n vertices has a set of O(sqrt n) vertices whose removal splits it into pieces of at most 2n/3 vertices.
prereqs: [planar-graph, breadth-first-search, maximal-planar-graph, planar-dual-graph]
see_also: [lipton-tarjan-separator, planar-separator-finding, r-division, nested-dissection, treewidth, fundamental-cycle, baker-planar-ptas, divide-and-conquer-paradigm]
sources:
  - paper: doi:10.1137/0136016
    title: Richard J. Lipton and Robert Endre Tarjan, A separator theorem for planar graphs, SIAM Journal on Applied Mathematics 36(2), 177 to 189 (1979)
    locator: the lemma on fundamental cycles in a triangulation with a spanning tree of small radius, and the main theorem with the bound 2 sqrt(2) sqrt(n)
  - paper: doi:10.1137/0209046
    title: Richard J. Lipton and Robert Endre Tarjan, Applications of a planar separator theorem, SIAM Journal on Computing 9(3), 615 to 627 (1980)
    locator: the uses of the theorem in divide-and-conquer algorithms and approximation schemes
  - paper: doi:10.1137/0603022
    title: Hristo N. Djidjev, On the problem of partitioning planar graphs, SIAM Journal on Algebraic and Discrete Methods 3(2), 229 to 240 (1982)
    locator: the improved constant and the lower bound for grids
  - paper: doi:10.1016/0022-0000(86)90030-9
    title: Gary L. Miller, Finding small simple cycle separators for 2-connected planar graphs, Journal of Computer and System Sciences 32(3), 265 to 279 (1986)
    locator: the simple cycle separator theorem
---

The planar separator theorem says that every [planar graph](/planar-graph/) with $n$ vertices has a set $S$ of at most $2\sqrt{2}\sqrt{n} \approx 2.83\sqrt{n}$ vertices whose removal leaves no connected piece with more than $2n/3$ vertices. The pieces can be grouped into two sides, $A$ and $B$, each with at most $2n/3$ vertices and with no edge between them. Lipton and Tarjan proved it in 1979 with [breadth-first search](/breadth-first-search/) levels and one [fundamental cycle](/fundamental-cycle/) of a triangulation, and the proof gives an $O(n)$ algorithm, the [Lipton-Tarjan separator](/lipton-tarjan-separator/). The theorem is the base of [divide and conquer](/divide-and-conquer-paradigm/) on planar graphs.

## Statement

**Theorem (Lipton and Tarjan, 1979).** Let $G = (V, E)$ be a planar graph with $n$ vertices. Then $V$ has a partition into three sets $A$, $B$ and $S$ such that

1. no edge joins a vertex of $A$ to a vertex of $B$,
2. $|A| \le 2n/3$ and $|B| \le 2n/3$, and
3. $|S| \le 2\sqrt{2}\sqrt{n}$.

The set $S$ is a *separator*, and the factor $2/3$ is its *balance*. The statement does not mention an embedding. The proof fixes one planar embedding, given as a [rotation system](/rotation-system/), and uses its [faces](/planar-face/).

Lipton and Tarjan also prove a weighted form: if the vertices have nonnegative weights with sum 1, the same bound on $|S|$ holds with $w(A), w(B) \le 2/3$ in place of $|A|, |B| \le 2n/3$.

**Small cases.**

- A single vertex: $A = B = \emptyset$ and $S = V$, since $|A| \le 2/3$ forces $A = \emptyset$.
- A [tree](/tree/): one centroid vertex is a separator, and every piece has at most $n/2$ vertices.
- $K_4$: every two vertices are adjacent, so one side is empty, the other has at most $8/3$ vertices, and $|S| = 2$ is the least possible. The bound allows $2\sqrt{2} \cdot 2 \approx 5.7$.
- $K_5$ and $K_{3,3}$ are not planar, but they are small, so they have small separators anyway. The theorem fails for large non-planar graphs: in $K_n$ the two sides cannot both be nonempty, so $|S| \ge n/3$, which is more than $2\sqrt{2}\sqrt{n}$ for $n > 72$.

## In plain words

Take a large map of roads with no bridges or tunnels, so that roads meet only at crossings. You can always close a small number of crossings so that the map falls apart into regions, and no region keeps more than two thirds of all the crossings. The number you must close grows only like the square root of the total number of crossings.

The proof grows rings around a start point, ring by ring. Two thin rings cut the map into an inner disc, a middle band and an outer part. If the middle band is still too big, one closed loop through it cuts it in two, and this loop is short because the band is narrow.

## Proof

We prove a lemma about triangulations first, then the theorem.

**Setup.** Adding edges only makes it harder to separate a graph, so a separator for a planar supergraph of $G$ on the same vertices is a separator for $G$. If $n \le 8$, then $n \le 2\sqrt{2}\sqrt{n}$, and $S = V$ works. So let $n \ge 9$ and let $G$ be a [maximal planar graph](/maximal-planar-graph/) with a fixed plane embedding. Then $G$ is connected and every face is a triangle.

**Lemma (cycle separator).** Let $H$ be a plane triangulation with at least 3 vertices, with nonnegative vertex weights $w$ of sum 1, and let $T$ be a spanning tree of $H$ with a root $q$ such that every vertex has depth at most $r$ in $T$. Then some edge $e \notin T$ has a fundamental cycle $C_e$ such that the vertices strictly inside $C_e$ have weight at most $2/3$, and the vertices strictly outside $C_e$ have weight at most $2/3$. The cycle $C_e$ has at most $2r + 1$ vertices.

*Proof of the lemma.* For a non-tree edge $e = uv$, the cycle $C_e$ is $e$ plus the tree path from $u$ to $v$. That path goes up from $u$ to the lowest common ancestor and down to $v$, so it has at most $2r + 1$ vertices.

Let $H^*$ be the [planar dual](/planar-dual-graph/) of $H$, and let $T^*$ be the set of duals of the edges not in $T$. By the tree-cotree property, $T^*$ is a spanning tree of $H^*$. Choose one face $f_0$ of $H$ as the outer face and root $T^*$ at $f_0$. For $e \notin T$, removing $e^*$ splits $T^*$ into two subtrees. Let $F(e)$ be the set of faces in the subtree without $f_0$. The cycle $C_e$ corresponds to a bond of $H^*$, the cut between the faces inside $C_e$ and the faces outside it. The only edge of $T^*$ in this bond is $e^*$, because all other edges of $C_e$ are in $T$. So each subtree of $T^* - e^*$ lies on one side of $C_e$, and $F(e)$ is exactly the set of faces inside $C_e$, the side without $f_0$.

Let $D(e)$ be the set of vertices that lie on a face of $F(e)$. This is the set of vertices on $C_e$ or strictly inside it. Call $e$ a *candidate* if $w(D(e)) \ge 1/3$.

*A candidate exists.* Every vertex lies on some face other than $f_0$, and every face other than $f_0$ lies in $F(e)$ for some edge $e^*$ of $T^*$ at the root $f_0$. The root has at most 3 such edges, because $f_0$ is a triangle. So the sets $D(e)$ for these at most 3 edges cover $V$, and one of them has weight at least $1/3$.

Choose a candidate $e = xy$ with $|F(e)|$ as small as possible. The vertices strictly outside $C_e$ are the vertices not in $D(e)$, so their weight is $1 - w(D(e)) \le 2/3$. Let $I(e) = D(e) \setminus V(C_e)$ be the set of vertices strictly inside $C_e$. We show that $w(I(e)) \le 2/3$. Assume the opposite, $w(I(e)) > 2/3$.

Let $g$ be the face of $F(e)$ that has $e$ on its boundary, which is the root of the subtree $F(e)$. It is a triangle $x, y, z$. The children of $g$ in $T^*$ are the duals of the non-tree edges among $xz$ and $yz$, and their subtrees partition $F(e) \setminus \{g\}$. Each vertex of $I(e)$ lies only on faces of $F(e)$. A vertex of $I(e)$ other than $z$ is not on $g$, because $x$ and $y$ are on $C_e$, so it lies on a face of $F(e) \setminus \{g\}$, and hence in $D(c)$ for a child edge $c$ of $g$. So

$$I(e) \subseteq \{z\} \cup \bigcup_{c \text{ child of } g} D(c).$$

- *No child.* Then $xz, yz \in T$, the tree path from $x$ to $y$ is $x, z, y$, and $C_e$ is the triangle $g$. Then $I(e) = \emptyset$, a contradiction.
- *One child $c$.* Then $z$ is an end of $c$, so $z \in D(c)$, and $w(D(c)) \ge w(I(e)) > 2/3 \ge 1/3$. So $c$ is a candidate with $|F(c)| < |F(e)|$, a contradiction.
- *Two children $c_1 = xz$ and $c_2 = yz$.* Then $z \in D(c_1)$. Both have fewer faces than $e$, so neither is a candidate, and $w(I(e)) \le w(D(c_1)) + w(D(c_2)) < 1/3 + 1/3$, a contradiction.

So $w(I(e)) \le 2/3$. By the [Jordan curve theorem](/jordan-curve-theorem/), no edge joins a vertex strictly inside $C_e$ to a vertex strictly outside it. $\square$

**Levels.** Run breadth-first search in $G$ from any vertex $q$. Let $L_i$ be the set of vertices at distance $i$, for $0 \le i \le r$, and let $L_i = \emptyset$ for $i < 0$ and for $i > r$. Each edge joins two vertices of the same level or of adjacent levels, so each level $L_i$ separates the levels below it from the levels above it.

Let $\ell_1$ be the level such that the levels $0, \ldots, \ell_1 - 1$ have fewer than $n/2$ vertices and the levels $0, \ldots, \ell_1$ have at least $n/2$. Let $k$ be the number of vertices in the levels $0, \ldots, \ell_1$, so $n/2 \le k \le n$.

**Claim.** There is a level $\ell_0 \le \ell_1$ with $|L_{\ell_0}| + 2(\ell_1 - \ell_0) \le 2\sqrt{k}$, and a level $\ell_2 \ge \ell_1 + 1$ with $|L_{\ell_2}| + 2(\ell_2 - \ell_1 - 1) \le 2\sqrt{n - k}$.

*Proof of the claim.* Let $t = \lfloor \sqrt{k} \rfloor$. If no level $\ell_0 = \ell_1 - j$ with $0 \le j \le t$ works, then $|L_{\ell_1 - j}| > 2\sqrt{k} - 2j$ for each such $j$. These levels are nonempty, so they have indices at least 0, and they hold at most $k$ vertices together. But

$$\sum_{j=0}^{t} (2\sqrt{k} - 2j) = (t + 1)(2\sqrt{k} - t) \ge (t + 1)\sqrt{k} > \sqrt{k} \cdot \sqrt{k} = k,$$

a contradiction. The same count on the $n - k$ vertices in the levels above $\ell_1$, with $\ell_2 = \ell_1 + 1 + j$, gives $\ell_2$. If $n - k = 0$, then $\ell_2 = r + 1$ works, with $L_{\ell_2} = \emptyset$. $\square$

**The middle band.** Let $M$ be the set of vertices in the levels $\ell_0 + 1, \ldots, \ell_2 - 1$. Put $L_{\ell_0} \cup L_{\ell_2}$ into $S$. The vertices below level $\ell_0$ are fewer than $n/2$, and the vertices above level $\ell_2$ are at most $n - k \le n/2$. If $|M| \le 2n/3$, we stop. Otherwise, build a graph $H$ from $G$: delete all levels from $\ell_2$ up, and contract all levels $0, \ldots, \ell_0$ into one vertex $q'$ (if $\ell_0 \ge 0$). The contracted part is connected, because it contains the BFS tree paths down to $q$. So $H$ is planar. Its BFS tree, inherited from $G$, has radius at most $\ell_2 - \ell_0 - 1$ from $q'$. Triangulate $H$, give each vertex of $M$ the weight $1/|M|$ and $q'$ the weight 0, and apply the lemma. It gives a cycle $C$ that splits $M \setminus C$ into an inside part and an outside part, each with at most $2|M|/3 \le 2n/3$ vertices, with no edge between them. The cycle has at most $2(\ell_2 - \ell_0 - 1) + 1$ vertices, and if it has exactly that many, it passes through the root $q'$, which is not a vertex of $G$. So $C$ has at most $2(\ell_2 - \ell_0 - 1)$ vertices of $G$. Add them to $S$.

**The size of $S$.**

$$|S| \le |L_{\ell_0}| + |L_{\ell_2}| + 2(\ell_2 - \ell_0 - 1) = \big(|L_{\ell_0}| + 2(\ell_1 - \ell_0)\big) + \big(|L_{\ell_2}| + 2(\ell_2 - \ell_1 - 1)\big) \le 2\sqrt{k} + 2\sqrt{n - k}.$$

The function $\sqrt{k} + \sqrt{n - k}$ is largest at $k = n/2$, so $|S| \le 4\sqrt{n/2} = 2\sqrt{2}\sqrt{n}$.

**The two sides.** After the removal of $S$, the graph falls into at most four parts with no edges between them: the levels below $\ell_0$, the levels above $\ell_2$, and the inside and outside parts of $M$ (or $M$ itself). Each has at most $2n/3$ vertices, and they have at most $n$ vertices together. If one part has at least $n/3$ vertices, let $A$ be that part and $B$ the rest; then $|B| \le n - n/3 = 2n/3$. Otherwise all parts have fewer than $n/3$ vertices; add parts to $A$ until $|A| \ge n/3$, so $|A| < 2n/3$, and let $B$ be the rest, with $|B| \le 2n/3$. $\blacksquare$

## Consequences

- **Linear-time algorithm.** Each step of the proof runs in $O(n)$ time: breadth-first search, the choice of $\ell_0$ and $\ell_2$, triangulation, and a walk over the dual tree. This is the [Lipton-Tarjan separator](/lipton-tarjan-separator/) algorithm; see [finding planar separators](/planar-separator-finding/) for other methods.
- **Balance $1/2$.** Applying the theorem again to the larger side, $O(\log n)$ times, gives a separator of size $O(\sqrt{n})$ whose sides have at most $n/2$ vertices each. The sizes of the successive separators form a geometric series.
- **Recursive decompositions.** Separating the pieces again and again gives a separator tree, and [r-divisions](/r-division/) into $O(n/r)$ pieces with $O(\sqrt{r})$ boundary vertices each. These drive fast [planar shortest paths](/planar-shortest-paths/).
- **Treewidth.** A planar graph has [treewidth](/treewidth/) $O(\sqrt{n})$: put the separator into every bag of the two recursive [tree decompositions](/tree-decomposition/), and the sizes add up as a geometric series.
- **Exact algorithms.** Problems such as maximum independent set have $2^{O(\sqrt{n})}$-time algorithms on planar graphs, by trying all choices on the separator and recursing (Lipton and Tarjan, 1980).
- **Sparse linear systems.** [Nested dissection](/nested-dissection/) orders the unknowns of a sparse system with a planar graph by recursive separators. The [Gaussian elimination](/gaussian-elimination/) then has $O(n \log n)$ fill and $O(n^{3/2})$ arithmetic operations.
- **Approximation.** Separating into pieces of size $O(\log n)$ and solving each piece exactly gives approximation schemes for maximum independent set (Lipton and Tarjan, 1980). [Baker's technique](/baker-planar-ptas/) later gave linear-time schemes.

## Tightness

**The order $\sqrt{n}$ is tight.** Let $G$ be the $k \times k$ grid, with $n = k^2$. Let $S$ be a separator with sides $A$ and $B$ of at most $2n/3$ vertices each, and suppose $|S| < k/3$. Then more than $2k/3$ rows contain no vertex of $S$, and at least one column contains none. Each free row is a path, and it meets the free column, so all free rows lie in one connected subgraph of $G - S$. A connected subgraph of $G - S$ lies entirely in $A$ or entirely in $B$, because no edge joins $A$ to $B$. That side then has more than $(2k/3) \cdot k = 2n/3$ vertices, a contradiction. So every such separator has at least $k/3 = \sqrt{n}/3$ vertices.

**The constant.** The constant $2\sqrt{2} \approx 2.83$ is not the best possible. Djidjev (1982) lowered it to $\sqrt{6} \approx 2.45$, later work lowered it further, and Djidjev also showed that a constant of about $1.55$ is needed, with a lower-bound example. The exact best constant is not known.

**The balance.** The factor $2/3$ is a convenient choice, not a limit. By the repeated separation in the consequences above, a separator of size $O(\sqrt{n})$ with sides of at most $n/2$ vertices also exists, at the cost of a larger constant.

**Planarity is needed.** The complete graph $K_n$, and expander graphs with $O(n)$ edges, have no separators of size $o(n)$. The proof uses planarity twice: for the triangulation and for the Jordan curve argument on the cycle.

**Cycles.** Miller (1986) showed that a 2-connected plane graph whose faces have at most $d$ vertices has a separator that is a simple cycle with $O(\sqrt{dn})$ vertices. For a triangulation, $d = 3$ and the bound is $O(\sqrt{n})$, and the separator is one cycle.

## History

Lipton and Tarjan proved the theorem with the constant $2\sqrt{2}$, in the paper published in 1979, and showed in 1980 how to use it for divide-and-conquer algorithms, nested dissection and approximation schemes. Djidjev (1982) improved the constant and gave a lower bound. Miller (1986) gave cycle separators, which are the base of many later recursive decompositions of planar graphs.

## References
