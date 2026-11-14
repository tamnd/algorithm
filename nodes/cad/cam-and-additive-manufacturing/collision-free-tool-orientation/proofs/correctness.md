---
title: The shadow test marks exactly the directions whose ray meets a box, and the layered dynamic program returns a cheapest choice of free grid directions
proves: [correctness]
status: full
---

**Setting.** A box is a closed set $B = [x_0, x_1] \times [y_0, y_1] \times [z_0, z_1]$. A tool center is a point $p$ that lies in no box. A direction above the horizon is written $d(q) = (q_x, q_y, 1)$ with $q \in \mathbb{R}^2$, and the box blocks $q$ at $p$ when the ray $\{p + t\, d(q) : t > 0\}$ meets $B$. Write $T_0 = \max(z_0 - p_z, 0)$, $T_1 = z_1 - p_z$, and $\bar R = [x_0 - p_x, x_1 - p_x] \times [y_0 - p_y, y_1 - p_y]$. The grid is a finite set $G \subset \mathbb{Z}^2$ with a step $h > 0$, and the grid point $g$ stands for $q = h g$. The planner gets tool centers $p_1, \dots, p_m$, boxes $\mathcal{B}$, preferred grid points $\pi_1, \dots, \pi_m$ and a weight $w \ge 0$, and minimizes
$$
J(g_1, \dots, g_m) = w \sum_{i=1}^m |g_i - \pi_i|^2 + \sum_{i=2}^m |g_i - g_{i-1}|^2
$$
over the choices with $g_i \in F_i$, the free grid points at $p_i$.

**Lemma 1 (the C-space image of a box).** $B$ blocks $q$ at $p$ if and only if $T_1 > 0$ and the closed segment from $T_0 q$ to $T_1 q$ meets $\bar R$.

*Proof.* The point $p + t\, d(q)$ has height $p_z + t$, so it is in the slab $z_0 \le z \le z_1$ exactly for $t \in [z_0 - p_z, z_1 - p_z]$. With $t > 0$ this is the set $I = [T_0, T_1] \setminus \{0\}$, which is empty when $T_1 \le 0$. For $t \in I$, the point is in $B$ exactly when its horizontal part $p_{xy} + t q$ is in the rectangle, that is when $t q \in \bar R$. So $B$ blocks $q$ if and only if $t q \in \bar R$ for some $t \in I$. The points $t q$ for $t \in [T_0, T_1]$ form the segment of the lemma. It remains to see that excluding $t = 0$ changes nothing. If $T_0 > 0$, then $0 \notin [T_0, T_1]$. If $T_0 = 0$, then $z_0 \le p_z$, and $T_1 > 0$ gives $p_z < z_1$, so $p$ lies in the slab; as $p \notin B$, $p_{xy}$ is not in the rectangle, that is $0 \cdot q = 0 \notin \bar R$, and the point $t = 0$ of the segment is not in $\bar R$. $\square$

The function `segment_meets_rect` is Liang and Barsky clipping: it intersects the parameter interval $[0, 1]$ with the closed interval of parameters for which each coordinate lies in its range, and reports a hit when the result is not empty. With rational inputs every step is exact, so the test decides Lemma 1 without rounding.

**Lemma 2 (growing boxes is safe).** Let $B_r$ be $B$ grown by $r \ge 0$ on each side. If $B_r$ does not block $q$ at $p$, then every point of the ray is at Euclidean distance more than $r$ from $B$.

*Proof.* A point $x$ outside $B_r$ has some coordinate more than $r$ outside the range of $B$, so its distance to $B$ in the maximum norm exceeds $r$, and the Euclidean distance is at least the maximum norm distance. $\square$

So a cylinder of radius $r$ about the ray does not meet $B$: the test is conservative, and it can reject directions that are in fact free for the cylinder, near the edges of the box.

**Lemma 3 (the dynamic program).** For $i \ge 1$ and $g \in F_i$ let
$$
C_i(g) = \min \{ J_i(g_1, \dots, g_i) : g_j \in F_j,\ g_i = g \},\quad J_i = w \sum_{j \le i} |g_j - \pi_j|^2 + \sum_{2 \le j \le i} |g_j - g_{j-1}|^2 .
$$
Then line L4 sets `cost` to $C_1$, and after the pass of line L6 for layer $i$, `cost` equals $C_i$.

*Proof.* For $i = 1$, $J_1 = w|g_1 - \pi_1|^2$, which line L4 computes. Let $i \ge 2$ and assume `cost` $= C_{i-1}$. Every feasible $(g_1, \dots, g_i)$ with $g_i = g$ splits as a feasible prefix ending in some $h \in F_{i-1}$ and the last step, and $J_i = J_{i-1}(g_1, \dots, g_{i-1}) + w|g - \pi_i|^2 + |g - h|^2$. Minimizing first over the prefixes that end in $h$ gives $C_{i-1}(h)$, and then over $h$ gives $C_i(g) = w|g - \pi_i|^2 + \min_h \big(C_{i-1}(h) + |g - h|^2\big)$, which line L6 computes. $\square$

**Theorem.** If every $F_i$ is nonempty, `plan_orientations` returns $\min J$ over all choices of free grid points and a choice that attains it. Every direction of the choice is free at its point, by Lemma 1 exactly for the given boxes, and by Lemma 2 with clearance $r$ when the boxes were grown by $r$. If some $F_i$ is empty, line L3 reports it, and no choice exists.

*Proof.* Line L2 builds $F_i$ by Lemma 1. By Lemma 3, after the last layer `cost` $= C_m$, and $\min J = \min_g C_m(g)$, which line L7 takes. The back pointers record, for each $g$ in layer $i$, an $h$ that attains the minimum of Lemma 3, so following them from the best $g$ in layer $m$ gives a choice $(g_1, \dots, g_m)$ whose cost adds up, step by step, to $C_m(g_m)$. All $F_i$ are finite, so all loops end. $\blacksquare$

**Remarks.** (1) The optimality is over the grid and for this cost. A finer grid, or another cost, such as a bound on the angle between neighbors or the cost of the rotary axes of a machine, can change the answer. (2) The tool is a half-line, or a cylinder after growing the boxes. The holder, the spindle, and the swept volume between two tool positions are not checked. (3) The tests compare the shadow test with a direct slab test of the ray against each box, with exact fractions, on random boxes and on directions aimed exactly at the edges and corners of boxes, and they compare the dynamic program with a search over all choices.
