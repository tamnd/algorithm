---
title: The planar ASV tree is exact and finite, convex inputs end in one step, and the 3D series can cycle until a cut is made
proves: [correctness, termination]
status: full
---

We use the notation and the pseudocode of the page. A polygon $R$ is simple, given counterclockwise as $R[0], \dots, R[s-1]$ with indices modulo $s$, has positive area, and has no three consecutive collinear vertices. We write $R$ also for the closed region it bounds. $H = \mathrm{CH}(R)$ is a convex polygon whose corners are vertices of $R$. $T$ is the set of indices of vertices on $\partial H$ (line L2), listed in increasing order. Since $H$ has at least three corners, $|T| \ge 3$. For consecutive $i, j$ in $T$ (cyclically), the *chain* $\gamma_{ij}$ is the boundary path $R[i], R[i+1], \dots, R[j]$, and the *lid* $\lambda_{ij}$ is the directed segment from $R[i]$ to $R[j]$. For a closed polygonal curve $c$ and a point $p$ not on it, $w_c(p)$ is the winding number. For a simple closed polygon, $w_c(p)$ is $\pm 1$ inside and $0$ outside, with $+1$ for counterclockwise orientation.

## The planar tree

**Lemma 1 (order).** The vertices $R[t]$, $t \in T$, appear along $\partial H$ counterclockwise in the same cyclic order as along $R$.

*Proof.* Suppose not. Then there are four of them $a, b, c, d$, in this cyclic order along $\partial H$, that appear along $R$ in the order $a, c, b, d$. So $\partial R$ splits into four arcs between them, and the arc $\alpha$ from $a$ to $c$ and the arc $\beta$ from $b$ to $d$ are disjoint. Both lie in the closed disc $H$, with endpoints on its boundary circle in the interleaved order $a, b, c, d$. Two such paths in a closed disc must meet: $\alpha$ splits the disc into two parts, and $b$ and $d$ lie in different ones. That contradicts disjointness. Since $R$ is counterclockwise and $H \supseteq R$, the orientations agree. $\square$

**Lemma 2 (lids and chains).** For consecutive $i, j$ in $T$:
(a) $\lambda_{ij}$ lies in one edge of $H$, and it is the arc of $\partial H$ from $R[i]$ to $R[j]$ counterclockwise;
(b) if $\gamma_{ij}$ has at least two edges, then all its points except $R[i]$ and $R[j]$ are in $\operatorname{int} H$;
(c) if $\gamma_{ij}$ has one edge, it equals $\lambda_{ij}$.

*Proof.* (a) By Lemma 1, no touching vertex lies strictly between $R[i]$ and $R[j]$ on the counterclockwise arc of $\partial H$. Every corner of $H$ is a touching vertex, so that arc contains no corner in its interior. It is therefore a straight piece of one hull edge, and it equals the segment $\lambda_{ij}$. (b) The vertices strictly inside the chain are not on $\partial H$, so they are in $\operatorname{int} H$. A segment with one endpoint in $\operatorname{int} H$ and the other in $H$ has all its points except possibly the second endpoint in $\operatorname{int} H$, by convexity. Every edge of a chain with two or more edges has an endpoint inside the chain. (c) is the definition. $\square$

So for a chain with two or more edges, the closed curve $\pi_{ij}$ that goes along $\lambda_{ij}$ and then back along $\gamma_{ij}$ reversed is simple. The lid lies on $\partial H$, and the rest of the curve lies in $\operatorname{int} H$. This is the pocket of lines L3 to L5: the reversed chain $R[j], \dots, R[i]$, closed by the edge from $R[i]$ to $R[j]$. Its vertices are vertices of $R$. Let $\Sigma$ be the union of $\partial R$ and $\partial H$, a finite union of segments.

**Lemma 3 (tiling).** Every pocket is counterclockwise. For every point $p \notin \Sigma$: if $p \in \operatorname{int} H$, then $p$ is in exactly one of $\operatorname{int} R$ and the interiors of the pockets; if $p \notin H$, it is in none of them.

*Proof.* As 1-cycles, $\partial R = \sum_{(i,j)} \gamma_{ij}$ over consecutive pairs. By Lemma 2(a) and Lemma 1, $\sum_{(i,j)} \lambda_{ij}$ is $\partial H$, traversed once counterclockwise. Using $\gamma = \lambda$ for one-edge chains,
$$\partial H = \partial R + \sum_{\text{pockets}} (\lambda_{ij} - \gamma_{ij}) = \partial R + \sum_{\text{pockets}} \pi_{ij},$$
so $w_{\partial H}(p) = w_R(p) + \sum w_{\pi_{ij}}(p)$ for $p \notin \Sigma$. Fix a pocket and let $m$ be the midpoint of its lid. By Lemma 2, the other chains meet $\partial H$ only at touching vertices, and the other lids are different arcs of $\partial H$. So some small disc $U$ around $m$ meets no curve other than the line of this lid. On $U$ minus the lid, $w_R$ and the winding numbers of the other pockets are constant, so they equal their value outside $H$, which is $0$. At a point of $U$ just inside $H$, the identity gives $1 = 0 + w_{\pi_{ij}}(p)$. So $\pi_{ij}$ has winding number $+1$ inside, and it is counterclockwise. Now every term is $0$ or $1$. Inside $H$ they sum to $1$, so exactly one is $1$. Outside $H$ they sum to $0$, so all are $0$. $\square$

**Theorem 1 (the expression).** For every node $v$ of the tree with region $R_v$ and hull $H_v$,
$$R_v = H_v -^* \bigcup_{\text{children } c} R_c,$$
and for every point $p$ on no edge of any region or hull in the subtree of $v$,
$$[p \in R_v] = \mathrm{CONTAINS}(v, p) = \sum_{u \text{ in the subtree of } v} (-1)^{\operatorname{depth}(u) - \operatorname{depth}(v)} [p \in \operatorname{int} H_u].$$

*Proof.* Write $R$, $H$ for $R_v$, $H_v$, and $Y$ for the union of the pockets. By Lemma 3, $\operatorname{int} H \setminus \Sigma$ is the disjoint union of $\operatorname{int} R \setminus \Sigma$ and $\operatorname{int} Y' \setminus \Sigma$, where $Y'$ ranges over the pockets. The set $\operatorname{int} R \setminus \Sigma$ is open, lies in $H$ and misses $Y$, so it lies in $\operatorname{int}(H \setminus Y)$. Conversely, a point of $\operatorname{int}(H \setminus Y) \setminus \Sigma$ lies in $\operatorname{int} H$ and in no pocket, so it is in $\operatorname{int} R$. Since $\Sigma$ is closed with empty interior, $\overline{U \setminus \Sigma} = \overline{U}$ for open $U$. So $H -^* Y = \overline{\operatorname{int}(H \setminus Y)} = \overline{\operatorname{int} R} = R$.

For the second claim, use induction on the height of $v$. For $p$ on no edge, $p \notin \Sigma$, so by Lemma 3, $p \in R$ iff $p \in \operatorname{int} H$ and $p$ is in no pocket. By induction, $p \in R_c$ iff CONTAINS$(c, p)$, which is line L7. It is also iff the signed sum over the subtree of $c$ is $1$. Since $p$ is in at most one pocket, $[p \in R] = [p \in \operatorname{int} H] - \sum_c [p \in R_c]$. Expanding each $[p \in R_c]$ by induction gives the signed sum. $\square$

All edges of all regions and hulls in the tree join two vertices of the input polygon. So the theorem holds at every point that lies on no line through two input vertices, which is how the tests choose their points.

**Theorem 2 (termination).** A pocket of a node with $s$ vertices has at most $s - 1$ vertices. So the tree has at most $n - 2$ levels for an input with $n$ vertices, and ASV returns.

*Proof.* The pocket of a chain from $i$ to $j$ has $(j - i \bmod s) + 1$ vertices. At least one index of $T$ other than $i$ and $j$ lies outside the chain, since $|T| \ge 3$. So $j - i \bmod s \le s - 2$. Every node with children has at least 4 vertices, since a triangle is convex. So along any path from the root, the number of vertices drops by at least one per level, from $n$ to at least $3$. $\square$

**Theorem 3 (convex inputs end in one step).** The tree of $R$ is a single node if and only if $R$ is convex, and then the series is $R = H_0$.

*Proof.* If $R$ is convex, then $H = R$, so every vertex is on $\partial H$ and $T$ is all indices. Every chain has one edge, line L4 skips all of them, and the node has no children. Conversely, if there are no pockets, then by Lemma 3 every point of $\operatorname{int} H \setminus \Sigma$ is in $\operatorname{int} R$, so $R \supseteq \overline{\operatorname{int} H \setminus \Sigma} = H$, and $R = H$ is convex. $\square$

## The series in three dimensions

The plain series takes $Q_0 = Q$ and $Q_{k+1} = \mathrm{CH}(Q_k) -^* Q_k$, and it ends when some $Q_k$ is empty. Then $Q = \mathrm{CH}(Q_0) - \mathrm{CH}(Q_1) + \cdots$ as indicators, almost everywhere.

**Convex input.** If $Q$ is convex, then $\mathrm{CH}(Q) = Q$ and $Q_1 = Q -^* Q = \overline{\operatorname{int} \emptyset} = \emptyset$. The series is $Q = H_0$, one step.

**A solid on which it cycles.** Let $A = (0,0,0)$, $B = (1,1,0)$, $C = (1,0,1)$, $D = (0,1,1)$. All six distances are $\sqrt 2$, so $H = \mathrm{conv}\{A, B, C, D\}$ is a regular tetrahedron, of volume $1/3$. Let $O = (A + B + C + D)/4 = (\tfrac12, \tfrac12, \tfrac12)$, its centre. For each face $F$ of $H$ let $K_F = \mathrm{conv}(\{O\} \cup F)$. The four cones $K_{ABC}, K_{ABD}, K_{ACD}, K_{BCD}$ tile $H$. Each $x \in H \setminus \{O\}$ lies on the segment from $O$ to the point where the ray from $O$ through $x$ leaves $H$, which lies in some face. Two cones meet only in a common triangle from $O$, since their faces lie in different sectors from $O$. Each cone has volume $1/12$.

Let $P = K_{ABC} \cup K_{ACD}$. The two tetrahedra share the whole triangle $OAC$, so $P$ is a solid with five vertices and volume $1/6$. It is not convex, since its volume is less than that of its hull. By the tiling,
$$Q_1 = H -^* P = K_{ABD} \cup K_{BCD}.$$
Now $P$ contains $A, B, C$ (in $K_{ABC}$) and $D$ (in $K_{ACD}$), and $Q_1$ contains $A, B, D$ (in $K_{ABD}$) and $C$ (in $K_{BCD}$). Both lie in $H$. So $\mathrm{CH}(P) = \mathrm{CH}(Q_1) = H$, and again by the tiling, $Q_2 = H -^* Q_1 = P$. By induction $Q_{2k} = P$ and $Q_{2k+1} = Q_1$ for all $k$. Neither is empty, so the series $H - H + H - \cdots$ never ends, and no finite truncation of it equals $P$ as a sum of hulls.

**The cut.** Consider $f(x, y, z) = z - x$. It is $0$ at $O$, $A$ and $C$, $-1$ at $B$ and $+1$ at $D$. So $K_{ABC} \subseteq \{f \le 0\}$ and $K_{ACD} \subseteq \{f \ge 0\}$, and they meet in the triangle $OAC$ in the plane $f = 0$. Hence
$$P \cap^* \{f \le 0\} = K_{ABC}, \qquad P \cap^* \{f \ge 0\} = K_{ACD}, \qquad P = K_{ABC} \cup^* K_{ACD}.$$
Each piece is convex, so its series ends in one step. The edges $OA$ and $OC$ are concave edges of $P$. Around $OA$, the three cones over the faces at $A$ meet, each with dihedral angle $2\pi/3$ by symmetry, and $P$ holds two of them, an angle of $4\pi/3$. The same holds at $OC$. Cutting along the plane of the triangle $OAC$, through these concave edges, is what partitioning does in ASVP. It makes the pieces' hulls smaller than the hull of the whole. This example is ours, built for this page. Kim and Wilde's general remedy and its proof of convergence are in their paper and are not reproduced here.

## What is not claimed

The planar theorems are for simple polygons without holes. The 3D part gives one solid on which the plain series cycles, and shows that one cut ends it. It does not prove that ASVP converges in general, and it does not say which cuts Kim and Wilde's rule makes on other solids. The conversion of terms into features is not covered.
