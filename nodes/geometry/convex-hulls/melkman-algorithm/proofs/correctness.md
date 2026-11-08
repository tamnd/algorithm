---
title: Melkman's algorithm keeps the convex hull of every prefix of a simple polyline
proves: [correctness, termination]
status: full
---

**Claim.** Let $V = v_0, \ldots, v_{n-1}$ be a simple polyline after line L1. If all its vertices lie on one line, line L2 returns the two end points of $V$ (or its one point). Otherwise, after each step $i \ge k$ of the loop, the deque $Q = \langle d_b, \ldots, d_t \rangle$ satisfies $d_b = d_t$, and $d_b, \ldots, d_{t-1}$ are the vertices of $\operatorname{conv}\{v_0, \ldots, v_i\}$, each once, in counterclockwise order, with no three consecutive vertices collinear. So line L11 returns the vertices of the hull of $V$. Each step ends, and the whole run takes $O(n)$ time.

**Notation.** $D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$; $D > 0$ means that $r$ is strictly left of the directed line $pq$. $P_i$ is the polyline $v_0, \ldots, v_i$ as a closed set of points, $s_i$ is its segment $[v_{i-1}, v_i]$, and $H_i = \operatorname{conv}\{v_0, \ldots, v_i\}$. **Simple** means that consecutive vertices differ and two segments $s_a, s_b$ with $a < b$ meet only if $b = a + 1$, and then only at $v_a$. In particular $s_i \cap P_{i-1} = \{v_{i-1}\}$, and $v_i \notin P_{i-1}$. While $Q$ represents a convex polygon $H$, its **top** is $\tau = d_t = d_b$, its **top edges** are $e_t = (d_{t-1}, \tau)$ and $e_b = (\tau, d_{b+1})$, and the **cone** at $\tau$ is the set of points $p$ with $D(d_{t-1}, \tau, p) \ge 0$ and $D(\tau, d_{b+1}, p) \ge 0$. For a convex polygon $H$ and a closed set $P \subseteq H$, a **face** of $H \setminus P$ is a connected component of $H \setminus P$.

**Fact 1 (collinear prefix).** If $v_0, \ldots, v_m$ lie on one line, they are in monotone order along it, so their hull is the segment $[v_0, v_m]$.

*Proof.* If the direction reversed at some $v_j$, then $s_j$ and $s_{j+1}$ would lie on the same line on the same side of $v_j$, and they would share more than $v_j$. $\square$

**Fact 2 (hull vertices are on the polyline).** Every vertex of $H_i$ is one of $v_0, \ldots, v_i$, so it lies on $P_i$.

**Lemma A (one opening per face).** Let $H$ be a convex polygon with nonempty interior and $P \subseteq H$ a closed connected set that contains every vertex of $H$. Then for every face $\Phi$ of $H \setminus P$, the set $\Phi \cap \partial H$ lies inside one edge of $H$, without its end points.

*Proof.* The vertices of $H$ are in $P$, so each component of $\partial H \setminus P$ lies in one open edge. Suppose $a, b \in \Phi \cap \partial H$ lie in different components. Then each of the two arcs of $\partial H$ from $a$ to $b$ contains a point of $P$; call them $p$ and $q$. The set $\Phi$ is open in $H$ and connected, and near each of its boundary points it contains a half-disc of $H$, so $a$ and $b$ can be joined by a simple polygonal path $\gamma \subseteq \Phi$ that meets $\partial H$ only at $a$ and $b$. Such a cross-cut divides the disc $H$ into two parts, one containing the open arc through $p$ and the other the open arc through $q$. The connected set $P$ contains $p$ and $q$ and does not meet $\gamma$, which is impossible. $\square$

**Invariant.** For $i \ge k$, after step $i$ (with step $k$ being lines L2 and L3):

- (a) $Q$ represents $H_i$ as in the claim, and $H_i$ has nonempty interior;
- (b) for every face $\Phi$ of $H_i \setminus P_i$ whose closure contains $v_i$, the set $\Phi \cap \partial H_i$ lies in a top edge of $H_i$.

**Initialization.** By the choice of $k$ in line L2, $v_0, \ldots, v_{k-1}$ are collinear and $v_k$ is not on their line. By Fact 1, $H_k$ is the triangle $v_0, v_{k-1}, v_k$, and line L3 lists it counterclockwise from $\tau = v_k$, so (a) holds. $P_k$ is the union of the two triangle edges $[v_0, v_{k-1}]$ and $[v_{k-1}, v_k]$. So $H_k \setminus P_k$ is one face, the open triangle together with the open edge from $v_k$ to $v_0$, which is a top edge. So (b) holds.

**Lemma B (the test of line L6).** Assume the invariant after step $i - 1$, and write $H = H_{i-1}$. Then line L6 skips $v_i$ exactly when $v_i \in H$.

*Proof.* $H$ lies in the cone at $\tau$, so a point of $H$ passes the test. Now let $v_i \notin H$. We show that $v_i$ is strictly right of the line of $e_t$ or of $e_b$, so the test fails. The set $s_i \cap H$ is a segment $[v_{i-1}, x]$ with $x \in \partial H$ and $x \ne v_i$, and the points of $s_i$ after $x$ are outside $H$.

- *Case $x \ne v_{i-1}$.* The set $(v_{i-1}, x]$ is connected and lies in $H \setminus P_{i-1}$ by simplicity, so it lies in one face $\Phi$ whose closure contains $v_{i-1}$. By (b) and Lemma A, $x$ lies in a top edge $e$ without its end points. The segment leaves $H$ at an inner point of $e$, so $v_i$ is strictly right of the line of $e$.
- *Case $x = v_{i-1}$ and $v_{i-1} = \tau$.* Near $\tau$, $H$ coincides with the cone at $\tau$, and the cone is invariant under scaling about $\tau$. The segment leaves $H$ at once, so $v_i$ is outside the cone.
- *Case $x = v_{i-1} \ne \tau$.* Then $v_{i-1}$ is not a vertex of $H$: a vertex of $H_{i-1}$ that is not in $H_{i-2}$ is pushed in step $i - 1$ and becomes the top, and $v_{i-1} \notin P_{i-2}$, so it is not an earlier vertex. So $v_{i-1}$ is an inner point of an edge $e$ of $H$. Near $v_{i-1}$, the set $P_{i-1}$ is only the segment $s_{i-1}$, which covers at most one of the two halves of $e$ at $v_{i-1}$. So some points of $e$ near $v_{i-1}$ lie in a face whose closure contains $v_{i-1}$, and by (b) and Lemma A, $e$ is a top edge. The segment leaves $H$ at an inner point of $e$, so $v_i$ is strictly right of its line. $\square$

**Lemma C (the update of lines L7 to L10).** Assume (a) after step $i - 1$ and $v = v_i \notin H = H_{i-1}$. Then after line L10, $Q$ represents $\operatorname{conv}(H \cup \{v\})$ as in (a), with top $v$.

*Proof.* Call an edge $(u, w)$ of $H$ **seen** if $D(u, w, v) \le 0$. The seen edges form a chain of consecutive edges, and some edge is not seen (the edge where a ray from $v$ through an interior point leaves $H$ has $v$ strictly on its inner side). By Lemma B, $e_t$ or $e_b$ is seen. A vertex $w$ of $H$ with neighbors $u$ and $w'$ stays a vertex of $H' = \operatorname{conv}(H \cup \{v\})$ exactly when one of its two edges is not seen:

- If both are seen, then $v = w + \alpha (w - u) + \beta (w - w')$ with $\alpha, \beta \ge 0$ not both zero, so $w = (v + \alpha u + \beta w') / (1 + \alpha + \beta)$ is not a vertex of $H'$.
- If, say, $D(w, w', v) > 0$, a line through $w$ obtained by turning the line of $(w, w')$ slightly outward has $H \setminus \{w\}$ and $v$ strictly on one side, so $w$ is a vertex of $H'$. The case of the other edge is the same.

The point $v \notin H$ is a vertex of $H'$, and the kept vertices of $H$ follow $v$ in counterclockwise order. In the order of $Q$, which starts and ends at $\tau$, the seen edges are the first $r$ edges and the last $s$ edges, with $r + s \ge 1$ and at least one edge not seen between them. Line L7 pops $d_t$ while its incoming edge is seen, so it removes the last $s$ vertices and stops at the end of the unseen chain. Line L8 pushes $v$. Line L9 removes the first $r$ vertices and stops at the start of the unseen chain, before it reaches the vertices that line L7 kept. Line L10 pushes $v$. The kept vertices are the end points and inner vertices of the unseen chain, which are the vertices with an unseen edge. If $r \ge 1$ and $s \ge 1$, both copies of $\tau$ are removed, as both of its edges are seen. If $r = 0$, the bottom copy of $\tau$ stays, which is correct as $e_b$ is not seen. The case $s = 0$ is the same. The kept vertices are exactly the vertices of $H'$, in counterclockwise order after $v$, and no three consecutive ones are collinear because they are vertices. $\square$

**Lemma D (the invariant is kept).** If the invariant holds after step $i - 1$, it holds after step $i$.

*Proof.* Line L1 makes $v_i \ne v_{i-1}$.

*Skip ($v_i \in H_{i-1}$).* $Q$ and $\tau$ do not change and $H_i = H_{i-1}$, so (a) holds. The set $s_i \setminus \{v_{i-1}\}$ is connected and lies in $H \setminus P_{i-1}$, so it lies in one face $\Phi$ of $H \setminus P_{i-1}$, and the closure of $\Phi$ contains $v_{i-1}$. By (b), $\Phi \cap \partial H$ lies in a top edge. Let $\Psi$ be a face of $H \setminus P_i$ whose closure contains $v_i$. A small disc $B$ around $v_i$ misses the closed set $P_{i-1}$, so the convex set $B \cap H$ lies in $\Phi$, and $\Psi$, which is connected and meets $B$, lies in $\Phi$. So $\Psi \cap \partial H \subseteq \Phi \cap \partial H$, which lies in a top edge.

*Add ($v_i \notin H_{i-1}$).* By Lemma B, line L6 does not skip, and by Lemma C, (a) holds with top $\tau = v_i$. Let $\Psi$ be a face of $H_i \setminus P_i$ whose closure contains $v_i$. For a small disc $B$ around $v_i$, the set $B \cap H_i$ is a circular sector with apex $v_i$ bounded by the two top edges, and $B \cap P_i = B \cap s_i$ is a radius of this sector. Removing it leaves one or two pieces, and each piece is connected and contains inner points of a top edge. $\Psi$ contains points of $B$ near $v_i$, so it contains a piece, and so an inner point of a top edge. By Fact 2 and Lemma A, $\Psi \cap \partial H_i$ lies in that edge. So (b) holds. $\square$

**Main result.** If all vertices are collinear, Fact 1 shows that the hull is the segment between the end points, which line L2 returns. Otherwise the invariant holds after step $k$ and, by Lemma D, after every later step. After step $n - 1$, (a) says that $d_b, \ldots, d_{t-1}$ are the hull vertices of $V$ in counterclockwise order, and line L11 drops the repeated top and rotates the cycle to start at the lexicographically smallest vertex. Since (a) holds after every step, the deque is the hull of every prefix, which is the online property.

**Termination and cost.** Lines L7 and L9 stop before $Q$ runs out, by Lemma C. Every vertex is pushed at most twice (lines L8 and L10) and line L3 pushes four entries, so there are at most $2n + 4$ pushes, and so at most $2n + 4$ pops in total. Every other line costs $O(1)$ per step, and line L11 costs $O(h)$. So the run takes $O(n)$ time. $\blacksquare$
