---
title: Correctness of the de Fraysseix-Pach-Pollack algorithm
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is maximal planar with $n \ge 4$ vertices (for $n = 3$ the output is the triangle $(0,0)$, $(2,0)$, $(1,1)$), embedded by a rotation system with outer face $v_1, v_2, v_n$ counterclockwise, and $v_1, \ldots, v_n$ is a canonical ordering. $G_k$ is the plane graph induced by $v_1, \ldots, v_k$, and its contour is $c_1 = v_1, \ldots, c_t = v_2$. By the definition of a canonical ordering, $G_k$ is 2-connected, its bounded faces are triangles, and its outer boundary is the cycle formed by the contour and the edge $v_1 v_2$. We write $M_k(c)$ for the set $M(c)$ after step $k$, with $M_k(c_{t+1}) = \emptyset$.

**Termination.** The loop of line L3 runs $n - 3$ times, and each iteration does a finite amount of work. The canonical ordering exists and is computed by a terminating procedure (see the canonical ordering page). So the algorithm terminates.

## Facts about the sets $M$

**Lemma 1.** For every $k \ge 3$: $M_k(c_1) \supsetneq M_k(c_2) \supsetneq \cdots \supsetneq M_k(c_t)$, $M_k(c_1) = V(G_k)$, $c_i \in M_k(c_i)$, and $c_j \in M_k(c_i)$ exactly when $j \ge i$.

*Proof.* For $k = 3$: $M(v_1) = \{v_1, v_3, v_2\}$, $M(v_3) = \{v_3, v_2\}$, $M(v_2) = \{v_2\}$. Step $k$ (line L8) adds $v_k$ to $M(c_i)$ for $i \le p$, sets $M(v_k) = \{v_k\} \cup M(w_{p+1})$, and keeps $M(w_i)$ for $i \ge q$. Since $M(w_{p+1}) \supseteq M(w_q)$ and $w_{p+1} \notin M(w_q)$, the chain for the new contour $c_1, \ldots, w_p, v_k, w_q, \ldots$ is again strictly decreasing, contains $v_k$ exactly in the sets up to $M(v_k)$, and $M(c_1)$ gains $v_k$. $\square$

So a sequence $0 \le \delta_1 \le \cdots \le \delta_t$ defines a **monotone shift** of $G_k$: move each vertex of $M_k(c_i) \setminus M_k(c_{i+1})$ by $\delta_i$ to the right. Lines L5 and L6 perform the monotone shift of $G_{k-1}$ with $\delta_i = 0$ for $c_i$ up to $w_p$, $\delta_i = 1$ for $w_{p+1}, \ldots, w_{q-1}$ and $\delta_i = 2$ from $w_q$ on.

**Lemma 2 (shifts restrict).** Let $k \ge 4$ and let $\delta$ be a monotone shift of $G_k$. Then the movement of the vertices of $G_{k-1}$ is a monotone shift $\delta'$ of $G_{k-1}$; moreover $v_k$ moves by some amount $d$, the vertex $w_p$ by at most $d$, the vertices $w_{p+1}, \ldots, w_{q-1}$ by exactly $d$, and $w_q$ by at least $d$.

*Proof.* Let $\delta'$ give $c_i$ the value of $\delta$ at $c_i$ for contour vertices of $G_{k-1}$ up to $w_p$ and from $w_q$ on, and the value $d = \delta(v_k)$ to $w_{p+1}, \ldots, w_{q-1}$. It is nondecreasing because $v_k$ lies between $w_p$ and $w_q$ on the contour of $G_k$. By line L8, $M_k(c) = M_{k-1}(c) \cup \{v_k\}$ for $c$ up to $w_p$, $M_k(v_k) \setminus \{v_k\} = M_{k-1}(w_{p+1})$, and $M_k(c) = M_{k-1}(c)$ from $w_q$ on. So a vertex $u$ of $G_{k-1}$ lies in $M_k(c_i) \setminus M_k(c_{i+1})$ for the same contour position under both descriptions, with $w_{p+1}, \ldots, w_{q-1}$ and their sets merged into the class of $v_k$. Hence $u$ moves by the same amount under $\delta$ and $\delta'$. The statements about $w_p$, $w_q$ and the covered vertices follow from monotonicity. $\square$

## The invariants

For $k \ge 3$, after step $k$ (and after any later shifts, which restrict to monotone shifts of $G_k$ by Lemma 2), consider:

- **(A)** $x(c_1) < x(c_2) < \cdots < x(c_t)$, $y(c_1) = y(c_t) = 0$, and $y(c_i) > 0$ for $1 < i < t$; every contour edge satisfies $|y(c_{i+1}) - y(c_i)| \le x(c_{i+1}) - x(c_i)$.
- **(B)** Right after step $k$, every contour edge has slope exactly $+1$ or $-1$.
- **(C)** Every bounded face $a, b, c$ of $G_k$, listed counterclockwise in the embedding, is drawn as a positively oriented triangle: $\det(b - a, c - a) > 0$. This holds after step $k$ and after any monotone shift of $G_k$.

(A) and (C) are preserved by monotone shifts: shifts keep y-coordinates, never decrease $x(c_{i+1}) - x(c_i)$, and (C) is stated for all monotone shifts.

**Base, $k = 3$.** The triangle $(0,0)$, $(1,1)$, $(2,0)$: (A) and (B) hold. The only bounded face is $v_1, v_2, v_3$, counterclockwise; under a monotone shift $v_1$ moves by $\delta_1$, $v_3$ by $\delta_2$, $v_2$ by $\delta_3$, and $\det(v_2 - v_1, v_3 - v_1) = (x_2 - x_1) \cdot 1 - 0 \cdot (x_3 - x_1) = x_2 - x_1 \ge 2 > 0$.

**Step $k \ge 4$.** Assume the invariants for $G_{k-1}$. Lines L5 and L6 apply a monotone shift, after which (A) and (C) hold for $G_{k-1}$, contour edges outside $w_p, \ldots, w_q$ keep slope $\pm 1$ (both ends move by the same amount), and the edges $w_p w_{p+1}$ and $w_{q-1} w_q$ have gained 1 in width.

*Claim 1: every covered vertex $w_j$ ($p < j < q$) satisfies $y_j - y_p < x_j - x_p$ and $y_j - y_q < x_q - x_j$, and also $|y_q - y_p| < x_q - x_p$.* By (A) summed along the contour, $|y_j - y_i| \le x_j - x_i$ for contour positions $i < j$ before the shift. The shift adds at least 1 to $x_j - x_p$ for $j > p$ and at least 1 to $x_q - x_j$ for $j < q$, without changing y-coordinates. This gives strict inequalities.

*Placement.* Line L7 sets $x_v - x_p = y_v - y_p = (x_q - x_p + y_q - y_p)/2$ and $x_q - x_v = y_v - y_q = (x_q - x_p - y_q + y_p)/2$. By Claim 1 both are positive, so $x_p < x_v < x_q$, and they are integers because, by (B) before the shift, $x_q - x_p + y_q - y_p$ was a sum of even numbers $(x_{i+1} - x_i) \pm (y_{i+1} - y_i)$, and the shift added 2. So the new contour satisfies (A), and its two new edges have slopes $+1$ and $-1$, so (B) holds. Also $y_v > 0$.

*Claim 2: $y_v - y_j > |x_v - x_j|$ for every covered $w_j$.* From Claim 1, $y_j < y_p + (x_j - x_p)$ and $y_j < y_q + (x_q - x_j)$. The point $v$ lies on both lines $y = y_p + (x - x_p)$ and $y = y_q + (x_q - x)$, so $y_v - y_j > (x_v - x_p) - (x_j - x_p) = x_v - x_j$ and $y_v - y_j > (x_q - x_j) - (x_q - x_v) = x_j - x_v$.

*The new faces.* The bounded faces of $G_k$ not in $G_{k-1}$ are the triangles $w_j, w_{j+1}, v_k$ for $p \le j < q$, counterclockwise, since $w_j$ lies left of $w_{j+1}$ and $v_k$ is above. Write $D_j = \det(w_{j+1} - w_j, v - w_j) = (x_{j+1} - x_j)(y_v - y_j) - (y_{j+1} - y_j)(x_v - x_j)$.

- If $p < j$ and $j + 1 < q$, both $w_j$ and $w_{j+1}$ are covered. Write $\Delta x = x_{j+1} - x_j > 0$ (by (A)) and $\Delta y = y_{j+1} - y_j$, with $|\Delta y| \le \Delta x$. By Claim 2, $y_v - y_j > |x_v - x_j|$, so $D_j > \Delta x \, |x_v - x_j| - |\Delta y| \, |x_v - x_j| \ge 0$.
- If $j = p$: $v$ is on the line of slope $+1$ through $w_p$, so $D_p = (x_{p+1} - x_p)(x_v - x_p) - (y_{p+1} - y_p)(x_v - x_p) = (x_v - x_p)\big((x_{p+1} - x_p) - (y_{p+1} - y_p)\big) > 0$ by Claim 1 (or by $|y_q - y_p| < x_q - x_p$ when $p + 1 = q$).
- If $j + 1 = q$: symmetric, with the line of slope $-1$ through $w_q$.

So (C) holds right after step $k$. For a later monotone shift of $G_k$, Lemma 2 says that the movement restricted to $G_{k-1}$ is a monotone shift (so the old faces stay positive by the invariant for $G_{k-1}$), and that relative to $v_k$, the vertex $w_p$ moves left by some $d_1 \ge 0$, $w_q$ moves right by some $d_2 \ge 0$, and the covered vertices do not move. Each $D_j$ is an affine function of $(d_1, d_2)$. Its partial derivative in $d_1$ (when $w_p$ is a corner) is $y_v - y_{j+1}$ or $y_v - y_q$, and in $d_2$ (when $w_q$ is a corner) is $y_v - y_j$ or $y_v - y_p$; all are positive by Claim 2 and by $y_v > y_p, y_q$. So the $D_j$ only grow and stay positive. This proves (C) for $G_k$.

## No crossings

**Lemma 3.** Let $H$ be a 2-connected plane graph whose bounded faces are triangles, and suppose a straight-line drawing of $H$ (not assumed plane) draws every bounded face, listed counterclockwise, as a positively oriented triangle, and draws the outer boundary cycle, listed counterclockwise, as a simple polygon $P$. Then the drawing has no crossings.

*Proof.* For a point $z$ that lies on no drawn edge and is not a vertex, let $N(z)$ be the number of drawn bounded faces that contain $z$. A positively oriented triangle has winding number 1 around its interior points and 0 around exterior points, so $N(z) = \sum_F w(\partial F, z)$. Each inner edge appears in two bounded faces with opposite directions, so the sum telescopes to the winding number of the outer boundary: $N(z) = w(P, z)$, which is 1 inside $P$ and 0 outside. If two edges crossed at an interior point, or a vertex lay in the interior of a drawn edge or face, then points near it would lie in two drawn faces: each edge has a drawn face on each side locally (or on one side for an edge of $P$), and the faces at an interior vertex cover a neighbourhood with total angle $2\pi$ times a positive integer. That gives $N(z) \ge 2$ for some $z$, which is impossible. $\square$

**Theorem.** The output is a straight-line drawing of $G$ without crossings, with integer coordinates in $[0, 2n - 4] \times [0, n - 2]$, that realizes the given rotation system.

*Proof.* After step $n$, $G_n = G$, every bounded face is a positively oriented triangle by (C), and the outer boundary is the triangle $v_1 = (0,0)$, $v_n$, $v_2 = (x, 0)$ with $v_n$ above, which is a simple counterclockwise polygon. Lemma 3 gives a plane drawing. Since every face, including the outer one, keeps its cyclic order and orientation, the counterclockwise order of neighbours at each vertex is the input rotation. The coordinates are integers by the placement argument. Each step adds 2 to $x(v_2)$, so $x(v_2) = 2 + 2(n - 3) = 2n - 4$; $v_n$ attaches to $w_p = v_1$, $w_q = v_2$, so $y(v_n) = (2n - 4)/2 = n - 2$; and (A) puts every contour vertex, hence every vertex, inside the triangle $(0,0)$, $(2n - 4, 0)$, $(n - 2, n - 2)$. $\square$

## The offset implementation computes the same coordinates

Let the shift tree have root $v_1$, with the next contour vertex as a child of each contour vertex, the first covered vertex as a child of the vertex that covers it, and each covered vertex's successor in its covered chain as its child. Each vertex stores its x-offset to its parent, and $x$ is the sum of offsets on the path from the root.

**Lemma 4.** After every step, for each contour vertex $c$, the descendants of $c$ in the shift tree are exactly $M(c)$, and the stored offsets give the same x-coordinates as the explicit shifts.

*Proof.* For $k = 3$ the tree is the path $v_1, v_3, v_2$ with offsets $0, 1, 1$, and the descendant sets are $M(v_1), M(v_3), M(v_2)$. At step $k$: adding 1 to the offset of $w_{p+1}$ moves exactly its descendants $M(w_{p+1})$ by 1, and adding 1 to the offset of $w_q$ moves $M(w_q)$ by 1 more, as in lines L5 and L6. The sum of the offsets of $w_{p+1}, \ldots, w_q$ is $x_q - x_p$. Then $v_k$ becomes the child of $w_p$ with offset $x_v - x_p$, $w_q$ becomes a child of $v_k$ with offset $x_q - x_v$, and $w_{p+1}$, if covered, becomes a child of $v_k$ with its offset reduced by $x_v - x_p$; the covered chain keeps its internal offsets. No absolute coordinate changes in this rewiring. The descendants of $v_k$ are $\{v_k\}$, the covered chain with its subtrees, and $w_q$ with its subtree, which is $\{v_k\} \cup M(w_{p+1})$; the descendants of the vertices up to $w_p$ gain $v_k$; the others are unchanged. This is line L8. $\square$

So the implementation outputs the coordinates of the explicit method, which are correct by the theorem. $\blacksquare$
