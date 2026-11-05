---
title: Correctness of Frederickson's planar shortest-path algorithm
proves: [correctness, termination]
status: full
---

Line numbers refer to the pseudocode on the main page. All lengths are nonnegative. For a set of arcs $A$ and vertices $x, y$, $\mathrm{dist}_A(x, y)$ is the least length of a directed path from $x$ to $y$ with all arcs in $A$, or $\infty$. A division $D$ of a set of arcs $A$ is a set of pieces whose arc sets partition $A$; each piece contains the ends of its arcs, and $B(P)$ is the set of vertices of $P$ that are in another piece or are terminals. Planarity is not used anywhere below: it only bounds the sizes, and so the time.

## Paths and pieces

**Lemma 1.** Let $D$ be a division of $A$, and let $\pi = (x_0, x_1, \ldots, x_k)$ be a path with all arcs in $A$. Cut $\pi$ at every inner vertex $x_i$ ($0 < i < k$) that is a boundary vertex of some piece. Then each part has all its arcs in one piece.

*Proof.* Take two consecutive arcs $x_{i-1} x_i$ and $x_i x_{i+1}$ in the same part, so $x_i$ is not a boundary vertex of any piece. Then $x_i$ is in exactly one piece: it is in the piece of each arc at it, and if it were in two pieces it would be a boundary vertex of both. So both arcs are in that piece. By induction along the part, all its arcs are in one piece. $\square$

**The dense distance graph.** Given $D$ and tables $T$ with $T_P[b][b'] = \mathrm{dist}_{A(P)}(b, b')$ for all $b, b' \in B(P)$, let $H$ be the graph whose vertices are all boundary vertices and which has, for each piece $P$ and each pair $b \ne b'$ in $B(P)$ with $T_P[b][b'] < \infty$, an arc $b \to b'$ of length $T_P[b][b']$.

**Lemma 2.** For boundary vertices $b, b'$, $\mathrm{dist}_H(b, b') = \mathrm{dist}_A(b, b')$.

*Proof.* Each arc of $H$ stands for a path in $A$ of the same length, so $\mathrm{dist}_A \le \mathrm{dist}_H$. Conversely, take a shortest path $\pi$ from $b$ to $b'$ in $A$ and cut it as in Lemma 1. Every cut vertex is a boundary vertex, and so are $b$ and $b'$. Each part goes from a boundary vertex $c$ to a boundary vertex $c'$ inside one piece $P$, and $c, c'$ are in $P$, so they are in $B(P)$; its length is at least $T_P[c][c']$, which is an arc of $H$ (or $c = c'$ and the part can be dropped). So $\mathrm{dist}_H \le \mathrm{dist}_A$. $\square$

## The boundary search

**Lemma 3.** Assume the tables $T$ are correct for $D$, and that every start vertex is a boundary vertex. Then BOUNDARY-SEARCH$(D, T, \mathit{start})$ returns, for every boundary vertex $b$, $d(b) = \min_{a} (\mathit{start}(a) + \mathrm{dist}_A(a, b))$, the minimum over the start vertices $a$.

*Proof.* By Lemma 2 it suffices to show that the procedure is Dijkstra's algorithm on $H$ with several sources: it settles the vertices in order of their final labels, and when it settles $b$ it relaxes every arc of $H$ out of $b$. The second part is lines L18 and L19, which go over every piece $Q$ with $b \in B(Q)$ and every $b' \in B(Q)$; relaxing only into vertices not settled changes nothing, since a settled vertex has its final, smaller or equal label.

For the first part, we use this invariant, which holds after line L14 and after every round of the loop:

(K) Every boundary vertex $x$ that is not settled and has $d(x) < \infty$ lies in some piece $Q$ such that $H$ holds an entry of $Q$ with key equal to $\mathrm{key}(Q)$ and $\mathrm{key}(Q) \le d(x)$.

After line L14, the start vertices are the only vertices with finite labels, and each is in a piece inserted with the minimum over its boundary. In a round, a label $d(x)$ can drop only in line L19, for a piece $Q$ with $x \in B(Q)$, and line L20 then sets $\mathrm{key}(Q)$ to the minimum over the vertices of $B(Q)$ not settled, which is at most $d(x)$, and inserts $Q$ with it. A key changes only in lines L16 and L20, and both set it to the current minimum of the piece, which is at most the label of every vertex of the piece not settled. So (K) holds again.

Also, each key is at least the true minimum of its piece at the moment it is set, and labels only go down. So the key of an entry is either equal to the current minimum of its piece, or larger than a label that has since dropped (*too high*), or smaller because the vertex that gave it has since been settled (*too low*). Line L16 skips entries whose key is not $\mathrm{key}(P)$, and rescans the piece: if the true minimum $m$ differs from the key, the key was too low, $P$ is reinserted with $m$, and nothing is settled.

Now suppose line L17 settles $b$ from piece $P$ with $d(b) = k = \mathrm{key}(P)$, where $k$ is the least key in $H$ and the rescan confirmed $k$. Let $x$ be any vertex not settled with finite label. By (K), some entry in $H$ has key at most $d(x)$, so $k \le d(x)$. Hence $b$ has the least label among all vertices not settled, which is the rule of Dijkstra's algorithm. With nonnegative lengths this rule settles every vertex at its distance from the sources, by the usual proof of [Dijkstra's algorithm](/dijkstra/). Every vertex reachable from a source gets a finite label, and by (K) the loop does not end while such a vertex is not settled. $\square$

## The tables

**Lemma 4.** After line L6, $T_Q[b][b'] = \mathrm{dist}_{A(Q)}(b, b')$ for every small piece $Q$ and $b, b' \in B(Q)$. After line L8, $T_P[b][b'] = \mathrm{dist}_{A(P)}(b, b')$ for every piece $P$ of $D_1$ and $b, b' \in B(P)$.

*Proof.* The first claim is the correctness of Dijkstra's algorithm run on the arcs of $Q$. For the second, $D_2$ is a division of the arcs of $P$, and line L4 makes every vertex of $B(P)$ a boundary vertex of the small pieces that contain it. So in line L8 the start vertex $b$ and every target $b'$ are boundary vertices of $D_2$, the tables of $D_2$ are correct by the first claim, and Lemma 3, applied to $D_2$ with $A = A(P)$, gives $\delta(b') = \mathrm{dist}_{A(P)}(b, b')$. $\square$

## The final labels

**Theorem.** FREDERICKSON-SSSP returns $d(x) = \mathrm{dist}(s, x)$ for every vertex $x$.

*Proof.* By line L2, $s$ is a boundary vertex of $D_1$. By Lemma 4 the tables of $D_1$ are correct, so by Lemma 3 line L9 gives $d(b) = \mathrm{dist}(s, b)$ for every boundary vertex $b$ of $D_1$.

Now let $x$ be a vertex that is not a boundary vertex; then $x \ne s$, and $x$ lies in exactly one piece $P$. If $x$ is not reachable, every label stays $\infty$, since all labels are lengths of real paths. Otherwise take a shortest path $\pi$ from $s$ to $x$, and let $b$ be the last vertex of $\pi$ that is a boundary vertex of some piece; it exists, since $s$ is one. Every vertex after $b$ on $\pi$ is not a boundary vertex, so by the argument of Lemma 1 all arcs after $b$ are in one piece, the piece of the last arc, which contains $x$ and so is $P$. Then $b$ is in $P$, hence $b \in B(P)$. Line L11 starts Dijkstra in $P$ with the label $d(b) = \mathrm{dist}(s, b)$, so it finds a label for $x$ at most $\mathrm{dist}(s, b) + \mathrm{dist}_{A(P)}(b, x) = \mathrm{dist}(s, x)$. Every label it finds is the length of a path from $s$, so it is at least $\mathrm{dist}(s, x)$. Line L11 changes no label of a boundary vertex below its distance, by the same remark. $\square$

## Termination

Each Dijkstra run settles each vertex of its piece once. In BOUNDARY-SEARCH, each round of the loop either removes an entry from $H$ without inserting one (an outdated entry), or reinserts one piece after a rescan that found a larger key (this happens at most once per inserted entry, since the reinserted entry has the correct key until a vertex is settled), or settles a new vertex. Each settled vertex inserts at most one entry per piece that contains it. So the number of entries, and of rounds, is finite, and every loop ends. $\blacksquare$
