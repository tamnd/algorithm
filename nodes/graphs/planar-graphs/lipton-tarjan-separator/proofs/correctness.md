---
title: The Lipton-Tarjan algorithm returns a balanced separator of size at most 2 sqrt(2) sqrt(n)
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple planar graph with $n \ge 1$ vertices and a planar rotation system $\rho$. We show that LT-SEPARATOR stops and returns a partition $(A, B, S)$ of $V$ with no edge between $A$ and $B$, $|A|, |B| \le 2n/3$, and $|S| \le 2\sqrt{2}\sqrt{n}$. Every loop of the algorithm runs over a finite set and every search visits each vertex once, so the algorithm stops. We prove the three properties.

**Step 1 (it suffices that every component of $G - S$ has at most $2n/3$ vertices).** Line L13 groups the components. If one component has at least $n/3$ vertices, it alone forms $A$, which has at most $2n/3$ vertices, and $B$ has at most $n - n/3 = 2n/3$. Otherwise, components are added to $A$ while $|A| < n/3$; each has fewer than $n/3$ vertices, so $|A| < 2n/3$ at the end, and $B$, if nonempty, is formed only after $|A| \ge n/3$, so $|B| \le 2n/3$. No edge joins two components, so no edge joins $A$ and $B$.

**Step 2 (line L1).** If the largest component has at most $2n/3$ vertices, then $S = \emptyset$ satisfies Step 1. Otherwise all later lines work in $K$, with $|K| > 2n/3$. Every other component has fewer than $n/3$ vertices. So it suffices that every component of $K - S$ has at most $2|K|/3 \le 2n/3$ vertices and that $|S| \le 2\sqrt{2}\sqrt{|K|}$.

**Step 3 (levels).** In a breadth-first search every edge joins two vertices whose levels differ by at most 1. So after removing all vertices of a level $L_i$, no edge joins a vertex below $L_i$ to a vertex above it. By the choice of $\ell_1$, the levels below $\ell_1$ hold fewer than $|K|/2$ vertices and the levels above $\ell_1$ hold $|K| - k \le |K|/2$. If line L3 stops, $S = L_{\ell_1}$ has at most $2\sqrt{2}\sqrt{|K|}$ vertices, and every component of $K - S$ lies on one side of $L_{\ell_1}$, so it has at most $|K|/2$ vertices.

**Step 4 (lines L4 and L5 find levels).** The claim in the proof of the [planar separator theorem](/planar-separator-theorem/) shows that some $\ell \in [\ell_1 - \lfloor\sqrt{k}\rfloor, \ell_1]$ satisfies the test of line L4, and that some $\ell \ge \ell_1 + 1$ satisfies the test of line L5, with $\ell = r + 1$ as the last resort. So both scans stop, and

$$|L_{\ell_0}| + |L_{\ell_2}| + 2(\ell_2 - \ell_0 - 1) \le 2\sqrt{k} + 2\sqrt{|K| - k} \le 2\sqrt{2}\sqrt{|K|}, \tag{1}$$

because $\sqrt{k} + \sqrt{|K| - k}$ is largest at $k = |K|/2$. After removing $L_{\ell_0} \cup L_{\ell_2}$, each component of $K - S$ lies in the levels below $\ell_0$ (fewer than $|K|/2$ vertices, since $\ell_0 \le \ell_1$), or above $\ell_2$ (at most $|K|/2$, since $\ell_2 > \ell_1$), or in $M$. If line L6 stops, $|M| \le 2|K|/3$, and the bound on $|S|$ follows from (1).

**Step 5 (line L7 builds a plane graph $H$ with a tree of small radius).** Let $R$ be the levels $0, \ldots, \ell_0$. The search tree restricted to $R$ is a tree $T_R$ rooted at $q$. Contracting one edge $uv$ of a plane graph merges $u$ and $v$, and the rotation of the merged vertex is $\rho_u$ with $v$ replaced by the neighbours of $v$ in the order of $\rho_v$, starting after $u$ and stopping before $u$; the result is again a plane graph, possibly with parallel edges and loops. Contracting the edges of $T_R$ one at a time, children into parents, gives exactly the order of the Euler tour of line L7: at each vertex, scan its rotation counterclockwise starting after the parent, and descend into each child where it occurs. Edges inside $R$ become loops and are dropped, edges to levels $\ell_2$ and above are deleted with those vertices, and of each set of parallel edges at $x$ one is kept. Deleting edges and vertices keeps a plane graph plane. So $H$ is a simple plane graph with rotation $\rho_H$.

$H$ is connected: each vertex of $M$ has a search-tree path down to level $\ell_0 + 1$, and from there one edge to $x$ (or, if $\ell_0 = -1$, the path down to $q \in M$). Let $T_H$ be these paths. Every vertex of $M$ has depth at most $\ell_2 - 1 - \ell_0$ in $T_H$.

**Step 6 (line L8 gives a triangulation).** For each face $f$ of $H$ with walk of darts $d_0, \ldots, d_{k-1}$, the corner of $f$ at the tail of $d_j$ is the counterclockwise side of $d_j$, because $f$ is on the left of $d_j$. Adding $c_f$ inside $f$ and an edge from $c_f$ to each corner, in the order of the walk, splits $f$ into the $k$ triangles $c_f, \text{tail}(d_j), \text{head}(d_j)$. These have three distinct vertices, since $H$ has no loops. Inserting the new edge right after $d_j$ in the rotation of its tail, and listing the new edges at $c_f$ in walk order, which is counterclockwise around $c_f$, describes this drawing. So the result $\Delta$ is a plane graph with no loops in which every face is a triangle on three distinct vertices. The proof of the lemma of the planar separator theorem uses only these facts, the [cycle and bond duality](/planar-dual-graph/), the tree-cotree property and the Jordan curve theorem, all of which hold for such graphs with parallel edges.

**Step 7 (line L9 gives a spanning tree).** $T$ consists of $T_H$ and, for each $c_f$, the edge to the corner of $d_0$. Each $c_f$ is a leaf of $T$. A tree path between two vertices never passes through a leaf except at its ends. So a fundamental cycle $C_e$ contains at most the two ends of $e$ among the new vertices, and its vertices of $H$ form a path in $T_H$. If $C_e$ passes through $x$, it has at most $2(\ell_2 - \ell_0 - 1)$ vertices of $M$, two branches of depth at most $\ell_2 - \ell_0 - 1$ below $x$. If it does not, its top vertex $z$ has depth at least 1 and the bound is $2(\ell_2 - \ell_0 - 2) + 1$. If $\ell_0 = -1$, $q$ is the root and the vertices of $M$ have depth at most $\ell_2 - 1$, which gives at most $2(\ell_2 - 1) + 1 = 2(\ell_2 - \ell_0 - 1) - 1$. In each case, with (1),

$$|S| \le |L_{\ell_0}| + |L_{\ell_2}| + 2(\ell_2 - \ell_0 - 1) \le 2\sqrt{2}\sqrt{|K|}.$$

**Step 8 (line L11 computes the weights).** Root $T^*$ at the face $f_0$. For a non-tree edge $e$, let $g$ be the end of $e^*$ farther from $f_0$ and $d = (u, v)$ the dart of $e$ with $g$ on its left. As shown in the proof of the lemma, the faces in the subtree of $g$, $F(g)$, are exactly the faces inside $C_e$, the side without $f_0$.

For each vertex $y$, the owner face $o(y)$ is the face on the left of the dart from $y$ to its parent (for the root, the face of its first dart). A vertex strictly inside $C_e$ has all its faces inside, so $o(y) \in F(g)$; a vertex strictly outside has $o(y) \notin F(g)$. So

$$\Sigma(g) = \sum_{o(y) \in F(g)} w(y) = w(\text{inside } C_e) + \sum_{y \in C_e,\ o(y) \in F(g)} w(y).$$

Orient $C_e$ as $u \to v$, then up the tree from $v$ to $z = \text{lca}(u, v)$, then down to $u$. The face $g$ is on the left of the first dart, and the inside is on one side of the whole oriented cycle, so the inside is on the left everywhere. For $y \ne z$ on the branch from $v$, the cycle uses the dart from $y$ to its parent, whose left face $o(y)$ is inside. For $y \ne z$ on the branch from $u$, the cycle uses the dart from the parent to $y$; its left face is inside, and $o(y)$ is the face on the other side of the same edge, so it is outside. The owner of $z$ is tested directly by its position in $T^*$. Hence

$$w(\text{inside } C_e) = \Sigma(g) - \big(P(v) - P(z)\big) - [o(z) \in F(g)]\, w(z),$$

where $P(y)$ is the weight of the tree path from $y$ up to the root, and $w(C_e) = P(u) + P(v) - 2P(z) + w(z)$ sums the two branches and $z$ once. These are the formulas of line L11.

**Step 9 (line L11 finds a balanced cycle).** The weights are 1 on $M$ and 0 on $x$ and the new vertices, with total $|M|$. By the lemma of the planar separator theorem, applied to $\Delta$, $T$ and $w / |M|$, a candidate exists, and the candidate with the fewest faces inside has weight at most $2|M|/3$ strictly inside $C_e$, and weight $|M| - w(\text{inside}) - w(C_e) \le 2|M|/3$ strictly outside. By the Jordan curve theorem, no edge of $\Delta$, hence no edge of $G$ between vertices of $M$, joins the two sides. Line L12 adds the vertices of $M$ on $C_e$ to $S$. Every component of $K - S$ inside $M$ lies on one side of $C_e$ and has at most $2|M|/3 \le 2|K|/3$ vertices, and the components outside $M$ were bounded in Step 4.

**Conclusion.** In every case every component of $G - S$ has at most $2n/3$ vertices and $|S| \le 2\sqrt{2}\sqrt{|K|} \le 2\sqrt{2}\sqrt{n}$. By Step 1, the output $(A, B, S)$ is a separator with the stated properties. $\blacksquare$
