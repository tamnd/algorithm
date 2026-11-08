---
title: Graham's scan returns the hull vertices in counterclockwise order
proves: [correctness, termination]
status: full
---

**Claim.** Let $S$ be the set of distinct points after line L1, with $|S| \ge 1$, and let $p_0$ be the pivot of line L3. GRAHAM-SCAN returns the extreme points of $S$ (the vertices of $\operatorname{conv} S$), each once, in counterclockwise order, starting at $p_0$. If $S$ lies on one line and $|S| \ge 2$, it returns $p_0$ and the end point of $S$ farthest from $p_0$.

**Notation.** $\mathrm{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, where $u \times w = u_x w_y - u_y w_x$. Let $H$ be the set of points $q \ne p_0$ with $q_y > p_{0,y}$, or $q_y = p_{0,y}$ and $q_x > p_{0,x}$. By the choice of $p_0$, $S \setminus \{p_0\} \subseteq H$. For $q \in H$ let $\theta(q) \in [0, \pi)$ be the angle of $q - p_0$. For $a, b \in H$, $(a - p_0) \times (b - p_0) = |a - p_0|\,|b - p_0| \sin(\theta(b) - \theta(a))$ and $\theta(b) - \theta(a) \in (-\pi, \pi)$, so

$$\mathrm{orient}(p_0, a, b) > 0 \iff \theta(a) < \theta(b), \qquad \mathrm{orient}(p_0, a, b) = 0 \iff \theta(a) = \theta(b).$$

So the comparator of line L4 sorts by $\theta$, and points with equal $\theta$ (which lie on one ray from $p_0$) by increasing distance from $p_0$. It is a strict total order on $H$. Write $s_1, \ldots, s_m$ for the sorted list and $Q_k = \{p_0, s_1, \ldots, s_k\}$.

**Lemma F (fans are convex).** Let $w_0 = p_0$ and $w_1, \ldots, w_r \in H$ with $r \ge 2$, $\theta(w_1) < \cdots < \theta(w_r)$, and $\mathrm{orient}(w_{i-1}, w_i, w_{i+1}) > 0$ for $1 \le i \le r - 1$. Then for each edge $(w_i, w_{i+1})$, indices modulo $r + 1$, every other $w_m$ lies strictly to the left of the directed line from $w_i$ to $w_{i+1}$. Consequently $w_0, \ldots, w_r$ are the vertices of the convex polygon $\operatorname{conv}\{w_0, \ldots, w_r\}$ in counterclockwise order, and a point of that polygon on the line of an edge lies on the edge.

*Proof.* Write $L_i$ for the directed line from $w_i$ to $w_{i+1}$.

1. *Edges at $p_0$.* For $L_0$: $\mathrm{orient}(p_0, w_1, w_m) > 0$ for $m \ge 2$, since $\theta(w_1) < \theta(w_m)$. For $L_r$ (from $w_r$ to $p_0$): $\mathrm{orient}(w_r, p_0, w_m) = \mathrm{orient}(p_0, w_m, w_r) > 0$ for $1 \le m < r$.
2. *$p_0$ and the other edges.* For $1 \le i \le r - 1$, $\mathrm{orient}(w_i, w_{i+1}, p_0) = \mathrm{orient}(p_0, w_i, w_{i+1}) > 0$.
3. *A step to the left.* Let $1 \le i$ and $i + 2 \le r$, and let $x \in H$ with $\theta(x) > \theta(w_{i+1})$ lie strictly to the left of $L_{i+1}$. We show that $x$ lies strictly to the left of $L_i$. Put the origin at $b = w_{i+1}$ and let $a = w_i - b$, $c = w_{i+2} - b$, $z = p_0 - b$ and $y = x - b$. The hypotheses read: $a \times c < 0$ (the left turn at $w_{i+1}$), $a \times z < 0$ and $c \times z > 0$ (step 2 for $L_i$ and $L_{i+1}$), $c \times y > 0$ (the hypothesis on $x$), and $z \times y < 0$ (from $\mathrm{orient}(p_0, w_{i+1}, x) > 0$). Suppose $a \times y \ge 0$. Measure angles of directions from $a$, counterclockwise. Then $c$ has angle $-\gamma$ with $0 < \gamma < \pi$, and $z$ has angle $-\zeta$ with $0 < \zeta < \gamma$, because $z$ is clockwise from $a$ and counterclockwise from $c$, both by less than $\pi$. From $a \times y \ge 0$ the angle of $y$ lies in $[0, \pi]$. From $c \times y > 0$ it lies in $(-\gamma, \pi - \gamma)$, so in $[0, \pi - \gamma)$. From $z \times y < 0$ it lies in $(-\zeta - \pi, -\zeta)$ modulo $2\pi$, so in $(\pi - \zeta, \pi]$. Since $\zeta < \gamma$, these two intervals are disjoint, a contradiction. So $a \times y < 0$, which says $\mathrm{orient}(w_i, w_{i+1}, x) > 0$.
4. *Later vertices.* Let $1 \le i \le r - 1$ and $m \ge i + 2$, $m \le r$. The left turn at $w_{m-1}$ puts $w_m$ strictly left of $L_{m-2}$. Applying step 3 to $x = w_m$ for $i' = m - 3, m - 4, \ldots, i$ (each time $\theta(w_m) > \theta(w_{i'+1})$) moves this to $L_i$.
5. *Earlier vertices.* For $1 \le i \le r - 1$ and $1 \le m \le i - 1$ the same computation as in step 3, with the roles of $w_i$ and $w_{i+1}$ and of the two directions of rotation exchanged, shows: if $x \in H$ with $\theta(x) < \theta(w_i)$ lies strictly left of $L_{i-1}$, it lies strictly left of $L_i$. The left turn at $w_{m+1}$ puts $w_m$ strictly left of $L_{m+1}$, and induction moves it up to $L_i$. With steps 1 and 2 this covers every pair.

For the consequence: let $n_i$ be the outer normal of $L_i$ (the direction of $w_{i+1} - w_i$ turned clockwise by a right angle). Then $\langle n_i, w_m \rangle \le \langle n_i, w_i \rangle$ for all $m$, with equality only for $m \in \{i, i+1\}$. With $u = n_{i-1} + n_i$, the point $w_i$ is the only maximizer of $\langle u, \cdot \rangle$ among the $w_m$, so each $w_i$ is an extreme point. Each $L_i$ is a supporting line that meets the polygon only in the segment $w_i w_{i+1}$, so the cycle $w_0, \ldots, w_r$ runs along the boundary, and it runs counterclockwise because the turns are left turns. $\square$

**Invariant.** Before iteration $k + 1$ of the loop of line L6 ($0 \le k \le m$), the stack $v_0, \ldots, v_t$ (bottom to top) satisfies:

- (I1) $v_0 = p_0$, $t \ge \min(k, 1)$, and $v_t = s_k$ when $k \ge 1$.
- (I2) $\theta(v_1) < \cdots < \theta(v_t)$, and $\mathrm{orient}(v_{i-1}, v_i, v_{i+1}) > 0$ for $1 \le i \le t - 1$.
- (I3) $Q_k \subseteq \operatorname{conv}\{v_0, \ldots, v_t\}$, and each $v_i$ is in $Q_k$.

*Initialization* ($k = 0$). The stack is $[p_0]$ and $Q_0 = \{p_0\}$.

*Maintenance.* Let $s = s_{k+1}$. The loop of lines L7 and L8 pops until the stack is $v_0, \ldots, v_j$ with $j = 0$, or $j \ge 1$ and $\mathrm{orient}(v_{j-1}, v_j, s) > 0$. Line L9 pushes $s$.

1. *Popped points stay inside.* When $v_l$ is popped ($l \ge 1$), $\mathrm{orient}(v_{l-1}, v_l, s) \le 0$. If $l \ge 2$, then $\mathrm{orient}(p_0, v_{l-1}, v_l) > 0$ and $\mathrm{orient}(p_0, v_l, s) \ge 0$ by the angles ($\theta(s) \ge \theta(v_l)$ because $s$ comes later in the sorted order), and $\mathrm{orient}(v_{l-1}, s, v_l) = -\mathrm{orient}(v_{l-1}, v_l, s) \ge 0$. So $v_l$ lies in the closed triangle $p_0 v_{l-1} s$. If $l = 1$, then $\mathrm{orient}(p_0, v_1, s) = 0$, so $v_1$ and $s$ are on one ray from $p_0$, and $v_1$ is nearer because it comes first, so $v_1$ lies on the segment $p_0 s$. In both cases $v_l$ is in the convex hull of points that remain on the stack after its pop, together with $s$. By induction over the pops, every popped point lies in $\operatorname{conv}\{v_0, \ldots, v_j, s\}$, and with (I3) so does $Q_{k+1}$. This gives (I3) for the new stack.
2. *Strict angle at the top.* If $j \ge 1$, then $\theta(s) > \theta(v_j)$. Otherwise $\theta(s) = \theta(v_j)$ and $s = p_0 + \beta e$, $v_j = p_0 + \alpha e$ for a unit vector $e$ and $0 < \alpha < \beta$. If $j = 1$, then $\mathrm{orient}(p_0, v_1, s) = 0$ and the loop would have popped $v_1$. If $j \ge 2$, then $\mathrm{orient}(v_{j-1}, v_j, s) = \mathrm{orient}(v_j, s, v_{j-1})$ has the sign of $e \times (v_{j-1} - p_0)$, which is negative because $\theta(v_{j-1}) < \theta(v_j)$; so the loop would have popped $v_j$. Both contradict the exit condition. So (I2) holds for the new stack: the angles increase, the turns at $v_1, \ldots, v_{j-1}$ are unchanged, and the turn at $v_j$ is the exit condition. (I1) holds since $s = s_{k+1}$ is on top.

*Termination of the inner loop.* Each iteration pops a point, and the stack is finite. The outer loop runs $m$ times. So the algorithm terminates.

**Conclusion.** After the last iteration, the stack $v_0, \ldots, v_t$ satisfies (I1) to (I3) with $k = m$, so $\operatorname{conv} S = \operatorname{conv}\{v_0, \ldots, v_t\}$.

- If $t \ge 2$, then the turn at $v_t$ and at $v_0$ is also a left turn ($\mathrm{orient}(v_{t-1}, v_t, p_0) = \mathrm{orient}(p_0, v_{t-1}, v_t) > 0$), and Lemma F applies to $w_i = v_i$. So the stack is the vertex list of $\operatorname{conv} S$ in counterclockwise order, starting at $p_0$, and each extreme point of $S$ appears once. The points of $S$ not on the stack are in $\operatorname{conv} S$ but are not vertices, so they are not extreme.
- If $t = 1$, then $S \subseteq \operatorname{conv}\{p_0, v_1\}$, so $S$ is collinear and its extreme points are $p_0$ and $v_1$. If $t = 0$, then $m = 0$ and $S = \{p_0\}$. (If $S$ is not collinear, some three points of $S$ are not on a line, so $\operatorname{conv} S$ has positive area and $t \ge 2$.)

This proves the claim. $\blacksquare$
