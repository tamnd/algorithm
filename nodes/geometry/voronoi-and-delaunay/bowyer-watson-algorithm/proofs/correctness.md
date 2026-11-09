---
title: The Bowyer-Watson algorithm returns a Delaunay triangulation
proves: [correctness, termination]
status: full
---

**Claim.** Let $S$ be the distinct points of $P$ after line L1. If $S$ lies on one line, BOWYER-WATSON returns the empty list. Otherwise it returns a triangulation of $S$ (its vertex set is $S$ and its triangles tile $\operatorname{conv} S$) in which no point of $S$ lies strictly inside the circumcircle of a triangle.

**Notation.** For a point $q$ write $|q|^2 = q_x^2 + q_y^2$. For a real triangle $t = (a, b, c)$, counterclockwise and not degenerate, let $f_t$ be the unique affine function $f_t(q) = \alpha_x q_x + \alpha_y q_y + \beta$ with $f_t = |\cdot|^2$ at $a$, $b$ and $c$. This is the [lifting map](/paraboloid-lifting-map/) view: $f_t$ is the plane through the three lifted points. Expanding $|q - o|^2 < r^2$ for the circumcircle with center $o$ and radius $r$ gives $|q|^2 < 2 o \cdot q + r^2 - |o|^2$, and the right side is $f_t(q)$, because it is affine and equals $|q|^2$ at the vertices. So

$$\mathrm{incircle}(a, b, c, q) > 0 \iff |q|^2 < f_t(q), \qquad \mathrm{incircle}(a, b, c, q) = 0 \iff |q|^2 = f_t(q).$$

We use two facts about the strictly convex function $|\cdot|^2$.

- **(F1)** If $q$ is in the closed triangle $t$ and is not a vertex, then $|q|^2 < f_t(q)$. (Write $q$ as a convex combination of the vertices with at least two positive weights, and use strict convexity.)
- **(F2)** If $q$ is on the line through two vertices $x, y$ of $t$, then $|q|^2 < f_t(q)$ when $q$ is strictly between $x$ and $y$, and $|q|^2 > f_t(q)$ when $q$ is on the line outside the closed segment. (On the line, $f_t(q) - |q|^2$ is a quadratic in the line parameter with negative leading coefficient and roots at $x$ and $y$.)

A triangle $t$ is **in conflict** with $p$ as defined on the page: a real $t$ when $|p|^2 < f_t(p)$, a ghost $(u, v, G)$ when $\mathrm{orient}(u, v, p) > 0$, or $\mathrm{orient}(u, v, p) = 0$ and $p$ is strictly between $u$ and $v$.

**Invariant.** Before each iteration of line L4, with $S'$ the set of inserted points: (I1) the real triangles of $T$ are counterclockwise, their vertex set is $S'$ and they tile $\operatorname{conv} S'$ with disjoint interiors, meeting edge to edge; (I2) every real $t$ satisfies $|q|^2 \ge f_t(q)$ for all $q \in S'$; (I3) for each counterclockwise boundary edge $v \to u$ of the tiling there is exactly one ghost $(u, v, G)$, and each directed edge of a triangle has its reverse in exactly one other triangle. After line L3 this holds, because $S' = \{a, b, c\}$ and $\mathrm{orient}(a, b, c) > 0$. Fix one iteration that inserts $p \notin S'$ and let $K$ be the set of triangles in conflict with $p$.

**Lemma 1 (neighbours).** Let $t = (x, y, w)$ and $t' = (y, x, z)$ be real triangles of $T$. Then $f_{t'} \ge f_t$ on the closed half-plane to the right of $x \to y$ (the side of $z$), and $f_{t'} \le f_t$ on the closed half-plane to the left.

*Proof.* $g = f_{t'} - f_t$ is affine and zero at $x$ and $y$, so it is zero on the line $xy$ and has one sign on each open side. By (I2) for $t$, $g(z) = |z|^2 - f_t(z) \ge 0$, and $z$ is strictly to the right. $\square$

**Lemma 2 (the conflict set is connected).** $K$ is not empty and is connected through shared edges. So line L5 succeeds and line L6 computes $C = K$.

*Proof.* Let $Q = \operatorname{conv} S'$.

1. *If $p \in Q$.* By (I1), $p$ lies in a closed real triangle, either in its interior or in the interior of an edge (it is not a vertex). Each real triangle whose closure holds $p$ is in $K$ by (F1). There are one or two of them, and they share the edge that holds $p$. If $p$ is strictly inside a boundary edge $uv$, its ghost is also in $K$ and shares that edge. No other ghost is in $K$, because $p \in Q$ is on the inner closed side of every hull edge and strictly inside at most one of them.
2. *If $p \notin Q$.* Then $p$ is strictly outside the line of at least one hull edge, so some ghost is in $K$. The hull edges with $p$ strictly outside their lines form one contiguous chain of the boundary of the convex polygon $Q$, and consecutive ghosts of the chain share their edge at $G$. No ghost has the segment rule, since $p \notin Q$.
3. *Every real $t \in K$ is joined to the triangles of step 1 or 2.* If the closure of $t$ holds $p$, we are done. Else take a point $s$ in the interior of $t$ such that the segment $sp$ passes through no vertex of $T$; this excludes only finitely many lines through $p$. Walk along $sp$ from $s$. It passes through triangles $t = t_0, t_1, \ldots$, each entered through the interior of an edge $xy$ of the one before. Stop at the first triangle whose closure holds $p$, or at the ghost of a hull edge if the walk leaves $Q$. When the walk crosses $xy$ from $t_{j-1}$ to $t_j$, the crossing point is not $p$, so $p$ is strictly on the side of $t_j$. If $t_j$ is real, Lemma 1 gives $|p|^2 < f_{t_{j-1}}(p) \le f_{t_j}(p)$, so $t_j \in K$. If $t_j$ is the ghost $(y, x, G)$, then $\mathrm{orient}(y, x, p) > 0$, so $t_j \in K$. By induction the whole walk is in $K$ and ends at a triangle of step 1 or 2.

Steps 1 and 2 give a connected set, and step 3 joins each other conflict triangle to it. $\square$

**Lemma 3 (visibility).** Let $(x, y)$ be a border edge of line L7 with $x \ne G$ and $y \ne G$. Then $\mathrm{orient}(x, y, p) > 0$.

*Proof.* The edge $(x, y)$ is in a triangle $t \in C$, and the triangle $t'$ across it is not in $C$.

- *$t$ and $t'$ real.* If $p$ were on the closed right side of $x \to y$, Lemma 1 would give $f_{t'}(p) \ge f_t(p) > |p|^2$, so $t' \in K$, a contradiction.
- *$t$ real and $t' = (y, x, G)$ a ghost.* As $t' \notin K$, $\mathrm{orient}(x, y, p) \ge 0$, and if it is $0$, then $p$ is on the line $xy$ but not strictly between $x$ and $y$. By (F2), $|p|^2 \ge f_t(p)$, so $t \notin K$, a contradiction.
- *$t = (x, y, G)$ a ghost and $t'$ real.* As $t \in K$, $\mathrm{orient}(x, y, p) > 0$, or $p$ is strictly between $x$ and $y$. In the second case (F2) puts $t'$ in $K$, a contradiction.

Two ghosts do not share an edge with two real ends. $\square$

**Lemma 4 (no point is lost).** Every $q \in S'$ is the end of a border edge, so it is a vertex after line L9.

*Proof.* By (I3) the triangles at $q$, ghosts included, form a cycle through shared edges. If none of them is in $C$, $q$ stays a vertex of old triangles. If some are in $C$ and some are not, two consecutive ones differ, and their shared edge is a border edge with end $q$. So suppose all of them are in $C$. Let $r = q + \varepsilon (q - p)$ for a small $\varepsilon > 0$.

- *If $r \in Q$.* Then $r$ is in a closed real triangle $t$ at $q$, and $r$ is not a vertex. By (F1), $f_t(r) \ge |r|^2$, and $f_t(p) > |p|^2$ because $t \in C$. As $q = (r + \varepsilon p) / (1 + \varepsilon)$ and $f_t$ is affine, $f_t(q) = \frac{f_t(r) + \varepsilon f_t(p)}{1 + \varepsilon} > \frac{|r|^2 + \varepsilon |p|^2}{1 + \varepsilon} \ge |q|^2$, by convexity of $|\cdot|^2$. But $f_t(q) = |q|^2$, a contradiction.
- *If $r \notin Q$.* Then $q$ is on the boundary of $Q$, and some hull edge $e$ at $q$ has $r$ strictly outside its line, or on its line outside $e$. In both cases $p$ is on the closed inner side of the line of $e$, and when $p$ is on that line it is on the side of $q$ away from $e$, so not strictly inside $e$. So the ghost of $e$ is not in $K$, a contradiction. $\square$

**Lemma 5 (the fan tiles the cavity).** After lines L8 and L9, (I1) and (I3) hold for $S' \cup \{p\}$.

*Proof.* Let $Q' = \operatorname{conv}(S' \cup \{p\})$, let $U$ be the union of the closed real triangles not in $C$, and let $R$ be the closure of $Q' \setminus U$. The boundary of $R$ is made of border edges with two real ends and, if $p \notin Q$, the two segments from $p$ to the ends of the visible chain of Lemma 2. Each border edge $(x, y)$ is stored with the cavity on its left, and by Lemma 3, $p$ is strictly on its left. So a ray from $p$ can cross a border edge only from the inside of $R$ to the outside, and it meets the two segments at $p$ only. Then each ray from $p$ meets $R$ in one segment that starts at $p$, because a second exit would need an entry. Hence every point of $R$ lies in exactly one triangle $(x, y, p)$ of line L9, apart from points on shared sides, and the triangles $(x, y, p)$ are counterclockwise by Lemma 3. With Lemma 4, the real triangles tile $Q'$ edge to edge with vertex set $S' \cup \{p\}$, which is (I1). For (I3): the conflict ghosts are the ghosts of the visible chain $u_0, \ldots, u_k$ (or of the one edge that holds $p$). Their border edges at $G$ are $(u_0, G)$ and $(G, u_k)$, which give the ghosts of the two new hull edges $u_0 \to p$ and $p \to u_k$, as for the [beneath-beyond](/beneath-beyond/) hull update. Each new edge $(y, p)$ meets its reverse $(p, y)$ in the triangle of the next border edge, because the border is one closed cycle around the star-shaped $R$. $\square$

**Lemma 6 (empty circles through new edges).** For every real vertex $x$ of a border edge there is an affine $\gamma$ with $\gamma(x) = |x|^2$, $\gamma(p) = |p|^2$ and $\gamma(q) \le |q|^2$ for all $q \in S'$.

*Proof.* First find an affine $f$ with $f(x) = |x|^2$, $f(p) > |p|^2$ and $f \le |\cdot|^2$ on $S'$. If $x$ is a vertex of a real $t \in C$, take $f = f_t$, by (I2). Else $x$ is an end of a hull edge $uv$ whose ghost $(u, v, G)$ is in $C$ with $\mathrm{orient}(u, v, p) > 0$. Let $t'$ be the real triangle on $uv$, and let $L(q)$ be the orientation determinant of $(u, v, q)$, which is $\le 0$ on $S'$, zero at $x$ and positive at $p$. Take $f = f_{t'} + \mu L$ with $\mu$ large. Next let $\tau(q) = 2 x \cdot q - |x|^2$, so $|q|^2 - \tau(q) = |q - x|^2 \ge 0$ and $\tau(p) < |p|^2$. The function $\lambda \mapsto ((1 - \lambda) f + \lambda \tau)(p) - |p|^2$ is positive at $0$ and negative at $1$, so it is zero at some $\lambda \in (0, 1)$. Take $\gamma = (1 - \lambda) f + \lambda \tau$. $\square$

**Lemma 7 (every edge is locally Delaunay).** For each edge with real triangles $t_1$, $t_2$ on both sides, the vertex of $t_2$ opposite the edge is not strictly inside the circumcircle of $t_1$.

*Proof.* There are three kinds of edges.

- *Edges of two old triangles.* Both triangles are unchanged, and (I2) held before.
- *A border edge $xy$* between a new $(x, y, p)$ and an old $t' = (y, x, z) \notin C$. Let $\sigma$ be the plane of $(x, y, p)$. Then $\sigma - f_{t'}$ is zero on the line $xy$ and $\ge 0$ at $p$, since $t' \notin K$. So it is $\le 0$ at $z$, which is on the other side: $\sigma(z) \le |z|^2$.
- *An edge $px$* between new triangles $(w, x, p)$ and $(x, y, p)$. Take $\gamma$ from Lemma 6 and let $\sigma_1$ be the plane of $(w, x, p)$. Then $\sigma_1 - \gamma$ is zero on the line $px$ and $\ge 0$ at $w$, so it is $\le 0$ at $y$, which is on the other side by Lemma 5: $\sigma_1(y) \le \gamma(y) \le |y|^2$. $\square$

**Proof of the claim.** Line L2 returns the empty list exactly when $S$ lies on one line, and then no triangle exists. Otherwise (I1) to (I3) hold after line L3. In each iteration, Lemma 2 shows that lines L5 and L6 find $C = K$, and Lemmas 5 and 7 show that the new real triangles form a triangulation of $S' \cup \{p\}$ in which every edge is locally Delaunay. By the [local Delaunay criterion](/local-delaunay-criterion/), which does not need general position, such a triangulation is Delaunay, so (I2) holds again. After the last iteration, $S' = S$, and line L10 returns the real triangles.

**Termination.** The loop of line L4 runs $|S| - 3$ times. In one iteration, the search of line L6 adds each triangle at most once to $C$, and there are finitely many triangles, so lines L5 to L9 end. $\blacksquare$
