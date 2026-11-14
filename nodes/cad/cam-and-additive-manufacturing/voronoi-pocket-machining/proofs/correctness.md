---
title: The wavefront builds the medial axis of a convex polygon, and the offsets read from it are exact
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a strictly convex polygon with edges $1, \dots, n$, $n \ge 3$, unit outward normals $n_i$ and $f_i(x) = c_i - n_i \cdot x$, so $P = \{x : f_i(x) \ge 0 \text{ for all } i\}$. By the convex offset lemma of the [contour-parallel proof](/contour-parallel-toolpath/), the depth of $x \in P$ is $\delta(x) = \min_i f_i(x)$ and $P_t = \{x : f_i(x) \ge t \text{ for all } i\}$. For a set $F$ of edges let $Q_F(t) = \{x : f_i(x) \ge t \text{ for all } i \in F\}$, and let $L_i(t)$ be the line $f_i = t$. $M$ is the closure of the set of points of the interior of $P$ where at least two indices reach $\min_i f_i$. For two adjacent edges $p, q$ of a polygon, $X_{pq}(t)$ is the meeting point of $L_p(t)$ and $L_q(t)$.

**Assumption (G), the generic case.** In each pass of line L3, exactly one edge has the smallest meeting time.

**Claim.** Under (G), MEDIAL-AXIS stops after $n - 3$ passes. Its arcs are segments whose union is $M$, the clearance $\delta$ along each arc is affine in its parameter and runs from $t_0$ to $t_1$, and the deepest node has clearance $\delta_{\max} = \max_P \delta$. For every $d \ge 0$, OFFSET$(A, d) = P_d$.

**Termination.** Each pass of the loop of line L2 removes one edge from $F$ in line L7, so the loop runs exactly $n - 3$ times.

**Lemma 1 (erosion).** If $Q_F(\tau) = Q_G(\tau)$, then $Q_F(t) = Q_G(t)$ for all $t \ge \tau$. *Proof.* Let $\rho = t - \tau \ge 0$. For $|v| \le \rho$, $f_i(x + v) = f_i(x) - n_i \cdot v \ge f_i(x) - \rho$, with equality at $v = \rho n_i$. So the closed disk of radius $\rho$ around $x$ lies in $\{f_i \ge \tau\}$ if and only if $f_i(x) \ge t$. Hence $x \in Q_F(t)$ if and only if this disk lies in $Q_F(\tau)$, and the same holds for $G$. $\square$

**Lemma 2 (edge lengths).** Let $R$ be a convex polygon with nonempty interior whose edges, in counterclockwise order, lie on the lines $L_i(\tau)$, $i \in F$, each with positive length. For consecutive edges $p, e, q$, the length of edge $e$ of the polygon bounded by the lines $L_i(t)$ is $\ell_e(t) = \ell_e(\tau) - (t - \tau)(\tan\tfrac{\beta}{2} + \tan\tfrac{\gamma}{2})$, where $\beta, \gamma \in (0, \pi)$ are the exterior angles of $R$ at the two ends of $e$. *Proof.* Rotate so that $n_e = (0, -1)$ and the edge runs in the direction $(1, 0)$. The left end $X_{pe}(t)$ moves with a constant velocity $v$ with $n_e \cdot v = -1$ and $n_p \cdot v = -1$. Here $n_p = (-\sin\beta, -\cos\beta)$, so $v_y = 1$ and $v_x = (1 - \cos\beta)/\sin\beta = \tan\tfrac{\beta}{2} > 0$. The right end moves left at speed $\tan\tfrac{\gamma}{2}$ by symmetry. $\square$

So $\ell_e$ is affine and strictly decreasing, and it is zero exactly when $X_{pe}(t) = X_{eq}(t)$, that is, when $L_p(t)$, $L_e(t)$ and $L_q(t)$ meet in one point. The system of line L3 has rows $(n_i, 1)$ for three distinct unit vectors, which are not collinear points of the circle, so it has one solution $t_e$, and $t_e > \tau$ is the zero of $\ell_e$.

**Invariant.** At each test of line L2, with $\tau$ the clearance of the last event ($\tau = 0$ at the start):

- (I1) $P_t = Q_F(t)$ for all $t \ge \tau$;
- (I2) $P_\tau$ is a convex polygon with nonempty interior whose edges, in order, lie on $L_i(\tau)$ for $i \in F$, each with positive length;
- (I3) for each pair $(p, q)$ of consecutive edges of $F$ there is one open arc, which starts at $X_{pq}(\tau)$ with clearance $\tau$, and every closed arc runs from $X_{pq}(t_0)$ to $X_{pq}(t_1)$ for the pair $(p, q)$ that was consecutive in $F$ during $[t_0, t_1]$.

At the start, $F$ is all edges, $P_0 = P$, and line L1 starts arc $(i, i+1)$ at the vertex $X_{i,i+1}(0)$. So the invariant holds.

*A pass of the loop.* Let $\tau' = t_e$ be the smallest meeting time, for the edge $e$ between $p$ and $q$. By Lemma 2 every edge length $\ell_i$ is positive on $[\tau, \tau')$, and by (G) every $\ell_i$ with $i \ne e$ is still positive at $\tau'$. For $t \in [\tau, \tau')$ the lines $L_i(t)$, $i \in F$, with the fixed exterior angles of $R$ and positive lengths, bound a convex polygon. A convex polygon is the intersection of the half-planes of its edges, so this polygon is $Q_F(t) = P_t$. Its vertex between consecutive $p, q$ is $X_{pq}(t)$, which moves on a straight line at constant speed. At $\tau'$, edge $e$ has length 0 and $X_{pe}(\tau') = X_{eq}(\tau') = N$, the point of line L4. The polygon $P_{\tau'}$ has its other edges, all of positive length, on the lines of $F' = F \setminus \{e\}$, and at least three of them, with distinct normals, so its interior is not empty. This gives (I2) for $F'$. Also $P_{\tau'} = Q_{F'}(\tau')$, as the intersection of the half-planes of its edges, and $P_{\tau'} = Q_F(\tau')$ by (I1). By Lemma 1, $Q_F(t) = Q_{F'}(t)$ for all $t \ge \tau'$, which gives (I1). Lines L5 and L6 close the arcs of $(p, e)$ and $(e, q)$ at $N$ and open the arc of $(p, q)$ at $N = X_{pq}(\tau')$, which gives (I3).

*The last step.* When $F$ has three edges, $P_\tau$ is a triangle. The three meeting times of Lemma 2 are all the meeting time $T$ of the same three lines, so all three edges shrink to the point $N$ of line L8 at time $T$, and $\ell_i(t) < 0$ for $t > T$ means that $Q_F(t)$ is empty. So $\delta_{\max} = T$, and $N$ is the deepest node.

**Each arc lies in $M$.** A point $X_{pq}(t)$ of an arc has $f_p = f_q = t$ and lies in $P_t$, so $\delta = t$ is reached by two indices. For $t > 0$ it is an interior point of $P$. The arc starts at clearance $t_0$ and ends at $t_1$, and $\delta$ is affine along it. Arcs that start at $t_0 = 0$ start at a vertex of $P$, which is in the closure.

**Each point of $M$ lies on an arc.** Let $x$ be an interior point of $P$ where two indices $i \ne j$ reach $\delta(x) = t > 0$. Then $x \in P_t$ and $f_i(x) = f_j(x) = t$, so $L_i(t)$ and $L_j(t)$ are two supporting lines of the convex set $P_t$ through $x$, with different normals. If $t < T$, $P_t$ is a polygon with nonempty interior by the invariant, and a boundary point of such a polygon with two different supporting lines is a vertex. So $x = X_{pq}(t)$ for a consecutive pair of $F$ at time $t$, which is a point of the arc of $(p, q)$. If $t = T$, then $P_T = \{N\}$ and $x = N$. The points of $M$ on the boundary of $P$ are limits of such points, and they are vertices of $P$, where arcs start.

**OFFSET.** Let $0 \le d \le T$. Every point that line L10 collects is a point of an arc with clearance $d$, so it has depth $d$ and lies in $P_d$. Every vertex of $P_d$ lies on two edge lines $L_i(d)$, $L_j(d)$ with $i \ne j$ that support $P_d$, so it is reached by two indices: it is in $M$ with clearance $d$, and it is collected. A convex polygon is the convex hull of its vertices, so $P_d \subseteq \operatorname{hull}(\text{collected}) \subseteq P_d$. For $d > T$ no arc has clearance $d$, and $P_d = \emptyset$. $\blacksquare$

**The links.** Arc $a$ ends where $a.\mathrm{next}$ starts, with the same clearance, so the clearance along the spine does not decrease. A link from the loop at $d$ to the loop at $d + s$ is a chain of straight pieces of arcs whose points have clearance between $d$ and $d + s$, so it lies in $P_d \subseteq P_r$, and the tool does not touch the wall during it.

**What this proof does not cover.** When two edges have the same smallest meeting time, or two parallel edges become neighbours, assumption (G) fails. The code then removes the edges one at a time at the same clearance, and an arc between two parallel edges has $t_0 = t_1$. For these inputs the tests compare the medial axis and the offsets with direct computations, exactly, on rectangles and on random polygons with parallel sides. That is a check, not a proof.
