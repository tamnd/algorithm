---
title: Sutherland-Hodgman keeps the winding number inside the window and zeroes it outside
proves: [correctness]
status: full
---

**Setup.** The subject $S$ is a closed polygon with vertex list $u_0, \ldots, u_{n-1}$, any shape, possibly self-intersecting. The clip polygon $C$ is convex with nonzero area, with vertices $c_0, \ldots, c_{m-1}$ in counterclockwise order (the code reverses a clockwise list first). For the edge $c_k c_{k+1}$ (indices mod $m$) let $\ell_k$ be its line, $\sigma_k(x) = \mathrm{orient}(c_k, c_{k+1}, x)$, and $H_k = \{x : \sigma_k(x) \ge 0\}$ the closed half-plane to its left. For a closed polygon $Q$ and a point $q$ not on $Q$, $\operatorname{wind}(Q, q)$ is the winding number. Write $\operatorname{int} C$ for the interior of $C$.

**Claim.** Let $Q^\ast$ be the output of SUTHERLAND-HODGMAN$(S, C)$. For every point $q$ that lies neither on $S$ nor on the boundary of $C$,

$$\operatorname{wind}(Q^\ast, q) = \begin{cases} \operatorname{wind}(S, q) & \text{if } q \in \operatorname{int} C, \\ 0 & \text{otherwise.} \end{cases}$$

In particular, for a simple subject the points with nonzero winding number in $Q^\ast$ are exactly the points of $S \cap C$, off the boundaries, and the signed area of $Q^\ast$ is the signed area of $S \cap C$.

## Step 1: what one pass emits

Fix one pass, with line $\ell = \ell_k$, $\sigma = \sigma_k$, $H = H_k$, and input $Q = (p_0, \ldots, p_{r-1})$. For each $i$, lines L5 to L7 emit a block $B_i$: first the point $X_i = e_i \cap \ell$ if $\sigma(p_{i-1})$ and $\sigma(p_i)$ are nonzero with opposite signs (line L6), then $p_i$ if $\sigma(p_i) \ge 0$ (line L7). The output $Q'$ is the concatenation $B_0 B_1 \cdots B_{r-1}$, read as a closed polygon. Write $e_i = p_{i-1} p_i$. The set $e_i \cap H$ is a segment, a point, or empty, since $e_i$ and $H$ are convex.

**Lemma 1.** If $Q'$ is not empty, its edges are of two kinds:

- (a) for each $i$ such that $e_i \cap H$ is not empty, at most one edge, which is $e_i \cap H$ traversed in the direction of $e_i$, and none when $e_i \cap H$ is a single point;
- (b) other edges, each with both endpoints on $\ell$, and so contained in $\ell$.

*Proof.* Let $L$ be the point emitted last before the block $B_i$, reading the output cyclically. If $\sigma(p_{i-1}) \ge 0$, then $B_{i-1}$ ends with $p_{i-1}$, so $L = p_{i-1}$. If $\sigma(p_{i-1}) < 0$, then $L$ is on $\ell$: the block $B_{i-1}$ is either $(X_{i-1})$, which is on $\ell$, or empty. It is empty only when $\sigma(p_{i-2}) \le 0$; if $\sigma(p_{i-2}) = 0$, then $B_{i-2}$ ends with $p_{i-2}$, which is on $\ell$, and if $\sigma(p_{i-2}) < 0$, the same argument goes one block further back. Since $Q'$ is not empty, this search ends at a point on $\ell$.

Every edge of $Q'$ either joins $L$ to the first point of a nonempty block $B_i$ or joins the two points of a block $B_i$ of size two. Write $p = p_{i-1}$, $s = p_i$ and go through the signs.

1. $\sigma(p) \ge 0$ and $\sigma(s) \ge 0$. Then $B_i = (s)$ and the edge is $ps = e_i = e_i \cap H$, of kind (a).
2. $\sigma(p) > 0 > \sigma(s)$. Then $B_i = (X_i)$ and the edge is $p X_i = e_i \cap H$, of kind (a).
3. $\sigma(p) < 0 < \sigma(s)$. Then $B_i = (X_i, s)$. The edge $L X_i$ has both endpoints on $\ell$, of kind (b), and the edge $X_i s = e_i \cap H$ is of kind (a).
4. $\sigma(p) < 0 = \sigma(s)$. Then $B_i = (s)$ and the edge $L s$ is of kind (b). Here $e_i \cap H = \{s\}$.
5. $\sigma(s) < 0$ and $\sigma(p) \le 0$. Then $B_i$ is empty and $e_i \cap H$ is $\{p\}$ or empty.

Each $i$ gives at most one edge of kind (a), and it is $e_i \cap H$ in the direction of $e_i$. $\square$

**Lemma 2.** $Q' \subseteq H$, and if $Q$ lies in a convex set $K$, then $Q' \subseteq K \cap H$.

*Proof.* Every emitted point is in $H$: line L7 emits only points with $\sigma \ge 0$, and line L6 emits points of $\ell$. Edges of kind (a) are parts of edges of $Q$, so they are in $K \cap H$. An edge of kind (b) joins two emitted points, which are points of $Q$ and so of $K$, both on $\ell$; by convexity the edge is in $K \cap \ell \subseteq K \cap H$. $\square$

## Step 2: one pass and the winding number

**Lemma 3.** For every point $q$ that lies neither on $Q$ nor on $\ell$: $\operatorname{wind}(Q', q) = \operatorname{wind}(Q, q)$ if $\sigma(q) > 0$, and $\operatorname{wind}(Q', q) = 0$ if $\sigma(q) < 0$. (An empty $Q'$ has winding number 0 everywhere.)

*Proof.* We use the ray count of the [winding number algorithm](/winding-number-algorithm/) (Lemma 2 of its correctness proof): if a ray from $q$ passes through no vertex of a closed polygon, the winding number is the number of edges that cross the ray from right to left minus the number that cross it from left to right. The proof there is written for a horizontal ray, but the winding number does not change under a rotation of the plane, so it holds for a ray in any direction. Lemma 2 shows $Q' \subseteq Q \cup \ell$, so $q$ is not on $Q'$.

*Case $\sigma(q) < 0$.* The ray from $q$ in the direction of the outer normal of $\ell$ keeps $\sigma < 0$ along its whole length, so it does not meet $Q' \subseteq H$. It passes through no vertex and crosses no edge of $Q'$, so $\operatorname{wind}(Q', q) = 0$.

*Case $\sigma(q) > 0$.* Each ray from $q$ whose direction $u$ satisfies $\sigma(q + t u) \ge \sigma(q)$ for $t \ge 0$ stays in the open half-plane $\{\sigma > 0\}$; these directions form a closed half-circle. Choose such a direction for which the ray passes through no vertex of $Q$ and no vertex of $Q'$; only finitely many directions are excluded. The ray $R$ does not meet $\ell$, so by Lemma 1 it meets no edge of kind (b), and it meets the edge $e_i \cap H$ of kind (a) exactly where it meets $e_i$, since $R \cap e_i \subseteq H$. The kind (a) edge has the direction of $e_i$, so it crosses $R$ in the same direction. If $e_i \cap H$ is a single point or empty, then $R$ does not meet $e_i$: $R$ avoids the vertices of $Q$ and of $Q'$, and a single point $e_i \cap H$ is a vertex of $Q$ on $\ell$, which $R$ does not reach. So the edges of $Q$ and of $Q'$ that cross $R$ match one to one, with the same directions, and the two signed counts are equal. If $Q'$ is empty, then all of $Q$ is in $\{\sigma < 0\}$, $R$ meets no edge of $Q$, and $\operatorname{wind}(Q, q) = 0$ as well. $\square$

## Step 3: all passes

Let $Q_0 = S$ (line L1) and let $Q_k$ be the output of the pass for the clip edge $c_{k-1} c_k$, so $Q^\ast = Q_m$ (line L8). Let $C_k = H_0 \cap \cdots \cap H_{k-1}$, a convex set, with $C_0$ the whole plane. The early stop when the output is empty does not change the result, because a pass on an empty list returns an empty list.

**Lemma 4.** For each $k$, $Q_k \subseteq C_k$, and for every point $q$ off $S$ and off the lines $\ell_0, \ldots, \ell_{k-1}$, $\operatorname{wind}(Q_k, q)$ equals $\operatorname{wind}(S, q)$ if $q$ is in the interior of $C_k$ and 0 otherwise.

*Proof.* By induction on $k$. For $k = 0$ there is nothing to show. For the step, Lemma 2 with $K = C_k$ gives $Q_{k+1} \subseteq C_{k+1}$. Let $q$ be off $S$ and off $\ell_0, \ldots, \ell_k$. Then $q$ is not on $Q_k$, since $Q_k \subseteq S \cup \ell_0 \cup \cdots \cup \ell_{k-1}$ by Lemma 1 applied to every earlier pass. If $\sigma_k(q) < 0$, Lemma 3 gives 0, and $q$ is outside $C_{k+1}$. If $\sigma_k(q) > 0$, Lemma 3 gives $\operatorname{wind}(Q_k, q)$, which by induction is $\operatorname{wind}(S, q)$ when $q$ is inside $C_k$ and 0 otherwise. A point off all the lines with $\sigma_k(q) > 0$ is in the interior of $C_{k+1}$ exactly when it is in the interior of $C_k$. $\square$

**Where convexity is used.** For a convex polygon $C$ in counterclockwise order, the intersection of the left half-planes of its edges is $C$ itself, so $C_m = C$. For a nonconvex clip polygon this intersection is only the [kernel](/polygon-kernel/) of $C$, and the passes compute $S$ clipped to the kernel, not to $C$.

**Proof of the claim.** Take $q$ off $S$ and off the boundary of $C$. If $q$ is on none of the lines $\ell_k$, Lemma 4 with $k = m$ and $C_m = C$ is the claim. If $q$ lies on some line $\ell_k$ but not on the boundary of $C$, then $q$ is outside $C$, since a convex polygon meets the line of one of its edges only in its boundary. The set $Q^\ast \subseteq C$ is closed and does not contain $q$, and $S$ does not contain $q$, so a small disk around $q$ misses $Q^\ast$, $S$ and $C$. The winding number of $Q^\ast$ is constant on that disk, and the disk contains points off all the lines, where Lemma 4 gives 0. $\blacksquare$

**The area.** The signed area of a closed polygon is the integral of its winding number (see [shoelace formula](/shoelace-formula/)). The points excluded in the claim form a set of measure zero, so the signed area of $Q^\ast$ is $\iint_{C} \operatorname{wind}(S, q)\, dq$.

**Termination.** There are $m$ passes, and each pass loops once over a finite list.
