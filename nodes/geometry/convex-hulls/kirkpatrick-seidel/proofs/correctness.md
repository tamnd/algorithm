---
title: The Kirkpatrick-Seidel algorithm returns the hull vertices in counterclockwise order
proves: [correctness, termination]
status: full
---

**Claim.** Let $S$ be the set of distinct points after line L1. KIRKPATRICK-SEIDEL returns the extreme points of $S$, each once, in counterclockwise order from the lexicographically smallest point. If $S$ is collinear with $|S| \ge 2$, it returns the two end points.

**Notation.** $D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$. For a finite set $T$ of points with distinct $x$-coordinates and at least two points, a **lower hull edge** of $T$ is a pair $(l, r)$ with $l_x < r_x$ such that every $p \in T$ satisfies $D(l, r, p) \ge 0$ (on or above the line $lr$), and $l$ and $r$ are the leftmost and the rightmost points of $T$ on that line. The **lower hull** of $T$ is the chain of the end points of its lower hull edges, from the leftmost point of $T$ to the rightmost. Its edges have strictly increasing slopes, every point of $T$ is on or above each edge line, and for each $m$ with $\min_T x \le m < \max_T x$ exactly one lower hull edge $(l, r)$ has $l_x \le m < r_x$: the **bridge over** $m$. Its slope is written $s^*$, and its line $\ell^*$.

**Fact 1 (contact of a line of slope $K$).** For a slope $K$, let $M$ be the set of points of $T$ that minimize $y - Kx$, with leftmost point $l$ and rightmost point $r$. Then $M$ is the set of points of $T$ on the lower supporting line of slope $K$. If $K = s^*$, then $l_x \le m < r_x$. If $K < s^*$, then $r_x \le m$. If $K > s^*$, then $l_x > m$.

*Proof.* The lower hull edges left of the bridge have slopes less than $s^*$, and those right of it have slopes greater than $s^*$. A line of slope $K$ supports $T$ from below at the vertex where the edge slopes pass $K$, or along an edge of slope $K$. If $K = s^*$ the contact is the bridge, from $l$ to $r$ with $l_x \le m < r_x$. If $K < s^*$, the contact is at a vertex or an edge left of the bridge, ending at or before its left end, so $r_x \le l^*_x \le m$ where $l^*$ is the left end of the bridge. If $K > s^*$, the contact starts at or after the right end $r^*$ of the bridge, so $l_x \ge r^*_x > m$. $\square$

**Fact 2 (safe pruning).** Let $(p, q)$ be a pair of points of $T$ with $p_x < q_x$. If $\operatorname{slope}(p, q) < s^*$, then $p$ is not on $\ell^*$. If $\operatorname{slope}(p, q) > s^*$, then $q$ is not on $\ell^*$.

*Proof.* If $p$ is on $\ell^*$, then $q$, which is on or above $\ell^*$ and to the right of $p$, gives $\operatorname{slope}(p, q) \ge s^*$. If $q$ is on $\ell^*$, then $p$, on or above $\ell^*$ and to the left of $q$, gives $\operatorname{slope}(p, q) \le s^*$. $\square$

**Lemma 1 (BRIDGE).** Let $T$ have distinct $x$-coordinates and $\min_T x \le m < \max_T x$. Then BRIDGE$(T, m)$ returns the bridge $(l^*, r^*)$ of $T$ over $m$.

*Proof.* Invariant: $C \subseteq T$, and $C$ contains every point of $T$ on $\ell^*$. It holds at line L12. Assume it holds at the start of a round. Then $C$ contains $l^*$ and $r^*$, so $|C| \ge 2$, all points of $C$ are on or above $\ell^*$, and $(l^*, r^*)$ is also the bridge of $C$ over $m$, with the same slope $s^*$. Apply Fact 1 to $C$ and the slope $K$ of line L16.

- If $l_x \le m < r_x$ at line L18, then by Fact 1 $K = s^*$, and $M$ is the set of points of $C$ on $\ell^*$, which by the invariant are all the points of $T$ on $\ell^*$. So $l = l^*$, $r = r^*$, and the result is correct.
- If $r_x \le m$, Fact 1 gives $K < s^*$. Line L19 drops only the left point $p$ of pairs with $\operatorname{slope}(p, q) \le K < s^*$, which by Fact 2 is not on $\ell^*$. The invariant holds.
- Otherwise $l_x > m$, and Fact 1 gives $K > s^*$. Line L20 drops only the right point $q$ of pairs with $\operatorname{slope}(p, q) \ge K > s^*$, which by Fact 2 is not on $\ell^*$. The invariant holds.

If line L14 finds $|C| = 2$, the invariant gives $C = \{l^*, r^*\}$, and the result is correct.

Termination: let $c = |C| \ge 3$ at line L15 and $k = \lfloor c/2 \rfloor \ge 1$ the number of pairs. $K$ is the lower median of $k$ slopes, so at least $\lceil k/2 \rceil$ slopes are $\le K$ and at least $\lceil k/2 \rceil$ are $\ge K$. In the case of line L19 or line L20, each such pair loses one point, so $C$ loses at least $\lceil k/2 \rceil \ge (c - 1)/4 > 0$ points. $C$ keeps at least two points by the invariant, so after finitely many rounds line L14 or line L18 returns. $\square$

**Lemma 2 (CONNECT).** Let $T$ have distinct $x$-coordinates, let $a$ and $b$ be its leftmost and rightmost points, and call CONNECT$(a, b, T)$. It returns the lower hull of $T$, from $a$ to $b$.

*Proof.* Induction on $|T|$. If $a = b$, $T = \{a\}$ and line L7 returns $[a]$. Otherwise $|T| \ge 2$. With $t = |T|$, line L8 takes the $\lceil t/2 \rceil$-th smallest $x$-coordinate, so $\min_T x \le m < \max_T x$ (the $x$-coordinates are distinct and $\lceil t/2 \rceil < t$). By Lemma 1, line L9 returns the bridge $(l, r)$ over $m$, a lower hull edge with $l$ and $r$ on the lower hull. The lower hull of $T$ is its part from $a$ to $l$, then the edge $(l, r)$, then its part from $r$ to $b$.

The part from $a$ to $l$ is the lower hull of $T_l = \{p \in T : p_x \le l_x\}$. Each lower hull edge of $T$ in this part has every point of $T$, so also of $T_l$, on or above its line, and its end points are extreme on its line within $T$, so also within $T_l$; so it is a lower hull edge of $T_l$. These edges form a chain from $a$, the leftmost point of $T_l$, to $l$, its rightmost point, and the lower hull of $T_l$ is the only such chain of lower hull edges. In the same way the part from $r$ to $b$ is the lower hull of $T_r$. Since $r \notin T_l$ and $l \notin T_r$, both sets are smaller than $T$, $a$ and $l$ are the leftmost and rightmost points of $T_l$, and $r$ and $b$ those of $T_r$. By the induction hypothesis, line L11 returns the lower hull of $T$ in order. $\square$

**Lemma 3 (LOWER-HULL).** For a nonempty set $S$ of distinct points, LOWER-HULL$(S)$ returns the extreme points of $S$ on the counterclockwise boundary path of $\operatorname{conv} S$ from $a$, the lowest point among those with the smallest $x$, to $b$, the lowest point among those with the largest $x$.

*Proof.* A point $p$ of $S$ that is not the lowest at its $x$ has a point of $S$ directly below it, so no line with all of $S$ on or above it passes through $p$ unless it is vertical. So the lower boundary path from $a$ to $b$, which consists of edges with non-vertical lines below which no point of $S$ lies (or of the single point $a$ when $a = b$), only touches points of $T$ from line L4, and it is the lower hull of $T$. Lines L5 and L6 and Lemma 2 return it. $\square$

**Main procedure.** If $|S| \le 1$, line L1 returns $S$. Otherwise let $a_0$ be the lexicographically smallest point, $(x_{\min}, y)$ with the smallest $y$. The counterclockwise boundary of $\operatorname{conv} S$ from $a_0$ is: the lower path from $a_0$ to the lowest point $b_0$ with $x = x_{\max}$ (Lemma 3, the list $L$); the vertical edge up to the highest point $b_1$ with $x = x_{\max}$, if $b_1 \ne b_0$; the upper path from $b_1$ to the highest point $a_1$ with $x = x_{\min}$; and the vertical edge down to $a_0$, if $a_1 \ne a_0$. The map $p \mapsto -p$ is a rotation by $\pi$. It keeps orientations, so it maps counterclockwise paths to counterclockwise paths. It sends the highest point at each $x$ to the lowest point at $-x$, so the upper path of $S$ from $b_1$ to $a_1$ is the negation of the lower path of $-S$ from $-b_1$ to $-a_1$, which is the list $U$ by Lemma 3. Line L3 joins $L$ and $U$. The first point of $U$ is $b_1$, which equals the last point $b_0$ of $L$ exactly when the column at $x_{\max}$ has one point, and then it is dropped; in the same way the last point $a_1$ of $U$ is dropped when it equals $a_0$. So every vertex appears once, in counterclockwise order from $a_0$. For collinear non-vertical $S$, $L = [a_0, b_0]$ and $U = [b_0, a_0]$, and the result is $a_0, b_0$; for a vertical $S$, $L = [a_0]$ and $U = [a_1]$, and the result is $a_0, a_1$.

**Termination.** Each call of CONNECT with $a \ne b$ calls BRIDGE, which terminates by Lemma 1, and then makes two calls on strictly smaller sets. $\blacksquare$
