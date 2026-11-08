---
title: Andrew's monotone chain returns the hull vertices in counterclockwise order
proves: [correctness, termination]
status: full
---

**Claim.** Let $S = \{p[1], \ldots, p[n]\}$ be the distinct points after line L1, with $n \ge 3$, sorted so that $p[1] < p[2] < \cdots < p[n]$ in lexicographic order. Write $a = p[1]$ and $b = p[n]$. If the points of $S$ are not all on one line, ANDREW-HULL returns the extreme points of $S$ (the vertices of $\mathrm{conv}(S)$), each once, as a cycle that makes a strict left turn at each vertex and has all of $S$ on or to the left of each of its edges. If all points of $S$ are on one line, it returns $a, b$. For $n \le 2$, line L2 returns the distinct points, which is the specification.

**Notation.** For vectors $u, w$ let $u \times w = u_x w_y - u_y w_x$, so $\mathrm{orient}(p, q, r)$ has the sign of $(q - p) \times (r - p)$. Call a nonzero vector $u$ *forward* if $u_x > 0$, or $u_x = 0$ and $u_y > 0$. Then $q - p$ is forward if and only if $p < q$, and for each nonzero $u$ exactly one of $u$ and $-u$ is forward. Each forward vector has a unique angle $\theta(u) \in (-\pi/2, \pi/2]$ with $u = |u| (\cos \theta(u), \sin \theta(u))$.

**Lemma A (angles).** For forward vectors $u, w$: $u \times w > 0 \iff \theta(w) > \theta(u)$, and $u \times w = 0 \iff \theta(w) = \theta(u)$.

*Proof.* $u \times w = |u||w| \sin(\theta(w) - \theta(u))$, and $\theta(w) - \theta(u) \in (-\pi, \pi)$. On this interval the sine is positive exactly on $(0, \pi)$ and zero exactly at $0$. $\square$

**Lemma B (the lower scan).** Before each test of line L4, when the points $p[1 \ldots i-1]$ have been processed ($i \ge 2$), the stack $v_1, \ldots, v_k$ satisfies:

- (I1) $v_1 = p[1]$, $v_k = p[i-1]$ and $v_1 < v_2 < \cdots < v_k$;
- (I2) $\mathrm{orient}(v_{j-1}, v_j, v_{j+1}) > 0$ for $1 < j < k$;
- (I3) $\mathrm{orient}(v_j, v_{j+1}, s) \ge 0$ for each edge $1 \le j < k$ and each $s \in \{p[1], \ldots, p[i-1]\}$.

*Proof.* Write $d_j = v_{j+1} - v_j$. By (I1) each $d_j$ is forward, and by (I2) and Lemma A, $\theta(d_1) < \theta(d_2) < \cdots < \theta(d_{k-1})$.

1. *Initialization.* After the first iteration the stack is $p[1]$ alone. (I1) holds, and (I2) and (I3) have no cases.

2. *Maintenance: what the loop of line L5 does.* Let $p = p[i]$. The loop pops $v_k, v_{k-1}, \ldots$ and stops at the first $t$ with $t = 1$ or $\mathrm{orient}(v_{t-1}, v_t, p) > 0$. A point $v_j$ with $j > t$ was popped, and when it was popped its predecessor was $v_{j-1}$, so $\mathrm{orient}(v_{j-1}, v_j, p) \le 0$. In particular, if $t < k$ then $\mathrm{orient}(v_t, v_{t+1}, p) \le 0$. Line L7 pushes $p$, so the new stack is $v_1, \ldots, v_t, p$. The loop stops because each pop shrinks the stack by one and it stops at size 1.

3. *(I1) and (I2) for the new stack.* $p > p[i-1] \ge v_t$, so the stack is increasing and ends at $p[i]$. The inner turns $v_{j-1}, v_j, v_{j+1}$ with $j < t$ are old. The new turn at $v_t$ (when $t \ge 2$) is strict by the stop condition.

4. *(I3) for the old edges $j < t$ and the new point $p$.* We show $d_j \times (p - v_j) > 0$ for $1 \le j < t$, by induction downward on $j$. For $j = t - 1$ this is the stop condition. Assume it for $j + 1 \le t - 1$. Since $d_{j+1} \times (p - v_{j+1}) > 0$ and $p - v_{j+1}$ is forward, Lemma A gives $\theta(p - v_{j+1}) > \theta(d_{j+1}) > \theta(d_j)$, so $d_j \times (p - v_{j+1}) > 0$. Then $d_j \times (p - v_j) = d_j \times \big((p - v_{j+1}) + d_j\big) = d_j \times (p - v_{j+1}) > 0$. The old points satisfy (I3) for these edges by the hypothesis.

5. *(I3) for the new edge $v_t \to p$.* Let $e = p - v_t$, a forward vector. Take $s \in \{p[1], \ldots, p[i-1]\}$; we show $e \times (s - v_t) \ge 0$. If $s = v_t$ the value is 0.
   - If $s > v_t$, then $t < k$, because $v_k = p[i-1]$ is the largest old point. The point $s$ is on or left of the old edge $v_t \to v_{t+1}$, so $d_t \times (s - v_t) \ge 0$ and $\theta(s - v_t) \ge \theta(d_t)$. Step 2 gives $d_t \times (p - v_t) \le 0$, so $\theta(e) \le \theta(d_t)$. Hence $\theta(s - v_t) \ge \theta(e)$, and Lemma A gives $e \times (s - v_t) \ge 0$.
   - If $s < v_t$, then $t \ge 2$, because $v_1 = p[1]$ is the smallest point. Let $w = v_t - s$, a forward vector. The point $s$ is on or left of the old edge $v_{t-1} \to v_t$: $d_{t-1} \times (s - v_{t-1}) \ge 0$. Since $s - v_{t-1} = d_{t-1} - w$, this gives $d_{t-1} \times w \le 0$, so $\theta(w) \le \theta(d_{t-1})$. The stop condition gives $\theta(e) > \theta(d_{t-1})$. So $\theta(w) < \theta(e)$, hence $e \times w < 0$ and $e \times (s - v_t) = -(e \times w) > 0$.

   The new point $p$ is on the new edge line. This proves (I3) for $\{p[1], \ldots, p[i]\}$. $\square$

At the exit of the loop, Lemma B with $i = n + 1$ says that the lower chain $L = v_1, \ldots, v_k$ goes from $a$ to $b$, is increasing, turns strictly left at each inner point, and has all of $S$ on or left of each edge.

**The upper scan.** Lines L9 to L12 run the same loop on the order $p[n], \ldots, p[1]$. This is the increasing order of the reflected set $-S = \{-s : s \in S\}$, and $\mathrm{orient}(-p, -q, -r) = \mathrm{orient}(p, q, r)$ because the determinant has degree 2. So Lemma B applied to $-S$ and reflected back gives: the upper chain $U = u_1, \ldots, u_m$ goes from $u_1 = b$ to $u_m = a$, is decreasing, turns strictly left at each inner point, and has all of $S$ on or left of each edge.

**The output.** Line L13 returns $C = v_1, \ldots, v_{k-1}, u_1, \ldots, u_{m-1}$, a cyclic sequence whose edges are the edges of $L$ and of $U$.

1. *All points on a line.* If $S$ lies on one line, every orientation is 0, so the loop of line L5 pops down to one point at each step, and $L = a, b$. In the same way $U = b, a$, and $C = a, b$.

2. *Not all on a line: strict turns at $a$ and $b$.* Suppose that the turn at $b$, from $v_{k-1}$ through $b$ to $u_2$, is not strictly left. Both $v_{k-1}$ and $u_2$ are smaller than $b$. By (I3) for $L$, $\mathrm{orient}(v_{k-1}, b, u_2) \ge 0$, so it is 0, and $v_{k-1}$ and $u_2$ lie on one ray from $b$ (the ray must be the same, since both points are smaller than $b$). If $u_2 = v_{k-1}$, all of $S$ is on or left of the line $v_{k-1} \to b$ and on or left of the reverse line $b \to v_{k-1}$, so all of $S$ is on that line, a contradiction. If $u_2$ is strictly between $b$ and $v_{k-1}$: when $m = 2$, $u_2 = a$ and $v_{k-1} < a$, a contradiction; when $m \ge 3$, the points $b$ and $v_{k-1}$ are both on or left of the edge $u_2 \to u_3$ and lie on opposite sides of $u_2$ on one line, so both orientations are 0, and $u_3$ is on the line through $b$ and $u_2$, which contradicts the strict turn of $U$ at $u_2$. If $v_{k-1}$ is strictly between $b$ and $u_2$, the same argument with the roles of $L$ and $U$ exchanged gives a contradiction. The turn at $a$ is handled in the same way. So $C$ turns strictly left at each vertex.

3. *Each vertex of $C$ is an extreme point of $S$.* Let $v$ be a vertex of $C$ with predecessor $u$ and successor $w$. Define the affine function $f(x) = (v - u) \times (x - v) + (w - v) \times (x - v)$. Each point of $S$ is on or left of both lines $u \to v$ and $v \to w$, so both terms are $\ge 0$ on $S$. If both are 0 at $x$, then $x$ is on both lines, and the two lines meet only at $v$ because the turn at $v$ is strict. So $f(v) = 0$ and $f(x) > 0$ for $x \in S \setminus \{v\}$. If $v$ were a [convex combination](/convex-combination/) of other points of $S$, the value $f(v)$ would be the same combination of positive values, which is positive. So $v$ is extreme.

4. *Each point of $S$ lies in the convex hull of the vertices of $C$.* Let $s \in S$, so $a \le s \le b$. Since $L$ increases from $a$ to $b$, there is an edge $v_j \to v_{j+1}$ with $v_j \le s \le v_{j+1}$. In the same way there is an edge $u_{l} \to u_{l+1}$ of $U$ with $u_{l+1} \le s \le u_l$. If one of the two edges is vertical, then $s$ has its $x$-coordinate and a $y$-coordinate between its two ends, so $s$ is on that edge. Otherwise both edges are non-vertical and $x = s_x$ is in the $x$-range of both. Let $A$ and $B$ be the points of the two edges with first coordinate $s_x$. The lower edge points to the right and $s$ is on or left of it, so $s_y \ge A_y$. The upper edge points to the left and $s$ is on or left of it, so $s_y \le B_y$. So $s$ is on the segment $AB$, and $A$ and $B$ are on segments between vertices of $C$. In both cases $s \in \mathrm{conv}(\text{vertices of } C)$.

5. *No point appears twice in $C$.* The points $v_1, \ldots, v_{k-1}$ are distinct because $L$ increases, and $u_1, \ldots, u_{m-1}$ are distinct because $U$ decreases. Suppose $c = v_j = u_l$ with $j \le k - 1$ and $l \le m - 1$. Then $c \ne b$ (only $v_k$ and $u_1$ are $b$, and $l = 1$ would give $c = b = v_j$ with $j < k$) and $c \ne a$ in the same way, so $j > 1$ and $l > 1$. Let $\delta = c - v_{j-1}$ and $\beta = u_{l-1} - c$, two forward vectors. The point $u_{l-1}$ is on or left of the edge $v_{j-1} \to c$ of $L$: $\delta \times (\beta + \delta) = \delta \times \beta \ge 0$, so $\theta(\beta) \ge \theta(\delta)$. The point $v_{j-1}$ is on or left of the edge $u_{l-1} \to c$ of $U$: $(-\beta) \times (-\delta - \beta) = \beta \times \delta \ge 0$, so $\theta(\delta) \ge \theta(\beta)$. So the two edges lie on one line with opposite directions, all of $S$ is on or left of this line in both directions, and $S$ lies on the line, a contradiction.

6. *Conclusion.* By step 4, a point of $S$ that is not a vertex of $C$ is a convex combination of vertices of $C$, so it is not extreme. By step 3 each vertex of $C$ is extreme, and by step 5 each appears once. So $C$ lists the extreme points of $S$, each once, with strict left turns and all of $S$ on its left, which is the counterclockwise order.

**Termination.** Each loop of lines L4 and L9 runs $n$ times. Each iteration of the loop of line L5 or line L10 pops a point, each point is pushed once in each scan, so these loops run at most $n$ times in total in each scan. $\blacksquare$
