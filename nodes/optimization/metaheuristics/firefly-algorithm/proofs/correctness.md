---
title: The firefly algorithm keeps its points in the box, moves a point only toward a better one, never raises the best current value, returns the best point it evaluated, and is a pull toward better points plus noise
proves: [correctness]
status: full
---

We use the pseudocode of the page for minimizing $f$ on the box $B = \prod_{k=1}^D [\ell_k, u_k]$ with $\ell_k < u_k$ and $n \ge 2$. The values $f(x_i)$ are always the current values, as in line L5. Write $\beta(r) = \beta_0 e^{-\gamma r^2}$ with $\beta_0 \ge 0$ and $\gamma \ge 0$.

**Claim 1 (feasibility).** Every point and every proposal lies in $B$.

*Proof.* Line L1 draws the points in $B$, and line L6 clips every proposal to $B$. A point is only ever set to a start point or to a clipped proposal. $\square$

**Claim 2 (moves go toward better points).** Firefly $i$ moves at step $(i, j)$ only if $f(x_j) < f(x_i)$ at that time.

*Proof.* This is the test of line L5. $\square$

**Claim 3 (the best current value never increases).** Let $\mu = \min_i f(x_i)$. No move raises $\mu$. In particular, a firefly whose value equals $\mu$ at the start of its turn in line L3 does not move during that turn.

*Proof.* Consider a move of firefly $i$ at step $(i, j)$. By Claim 2, $f(x_i) > f(x_j) \ge \mu$, so $i$ is not a firefly with value $\mu$. Let $m$ be a firefly with $f(x_m) = \mu$. Then $m \ne i$, and the move does not change $x_m$, so the minimum after the move is at most $f(x_m) = \mu$. For the second statement, if $f(x_i) = \mu$ at the start of the turn of $i$, then no $j$ has $f(x_j) < f(x_i)$. During the turn only $x_i$ can change, and it does not change unless a move occurs, so the condition of line L5 stays false for every $j$. $\square$

So the population is elitist even without the stored best point, although a single move can raise the value of the firefly that moves.

**Claim 4 (the best point).** After line L1 and after each move, $f(g) = \min\{f(z) : z \text{ evaluated so far}\}$, and $g$ is one of these points.

*Proof.* After line L1, $g$ is the best start point. Each move evaluates exactly one new point $y$ in line L7, and $g$ is replaced by $y$ when $f(y) < f(g)$, so the property holds after the move by induction. $\square$

**Claim 5 (the move is a pull plus noise).** Before clipping, the proposal of line L6 is
$$y = x_i + \beta(\lVert x_i - x_j \rVert)\,(x_j - x_i) + \alpha\,(u - \tfrac12) \odot w,$$
where $u$ is uniform on $[0, 1]^D$ and $w_k = u_k - \ell_k$ is the width of the box. If $\gamma = 0$, this is the position update $x_i + v$ of [particle swarm optimization](/particle-swarm-optimization/) with the velocity $v = \beta_0 (x_j - x_i) + \alpha (u - \frac12) \odot w$: inertia weight 0, no personal-best term, a social term with the coefficient fixed to $\beta_0$ and the attractor $x_j$, and an added uniform perturbation. If $\alpha = 0$ and $\beta_0 \le 1$, the move does not increase the distance to $x_j$ and multiplies it by $1 - \beta(r)$ before clipping.

*Proof.* The formula is line L6. With $\gamma = 0$, $\beta(r) = \beta_0$ for every $r$, which gives the PSO form. With $\alpha = 0$, $y - x_j = (1 - \beta(r))(x_i - x_j)$, and $0 \le 1 - \beta(r) \le 1$ when $0 \le \beta(r) \le \beta_0 \le 1$. Clipping is the projection onto the convex set $B$, which contains $x_j$, so it does not increase the distance to $x_j$. $\square$

**Claim 6 (collapse without noise).** Let $\alpha = 0$, $\gamma = 0$ and $\beta_0 = 1$, and suppose that one start point $b$ has a strictly smaller value than all other start points. After the first iteration, all $n$ points equal $b$, and no move happens after that.

*Proof.* With these values the proposal is $y = x_j$, which is in $B$, so every move copies a current point. By induction every current point is a start point, so no current value is below $f(b)$, and the points with value $f(b)$ are exactly the copies of $b$. By Claim 3, the firefly that starts at $b$ never moves. Take any other firefly $i$ in its turn of the first iteration. If its value is $f(b)$ when the scan of line L4 reaches the firefly at $b$, it is already a copy of $b$. Otherwise its value is larger and it moves onto $b$. After that, no value is smaller than $f(b)$, so it does not move again. Hence every firefly equals $b$ after the first iteration, and then line L5 is false for every pair. $\square$

**Remark.** No claim here says that $g$ approaches a global minimizer. With $\beta_0 \le 1$, a pull keeps a point inside the coordinate ranges of the current points, so only the noise term can extend these ranges. With $\alpha_t = \alpha_0 \delta^t$ and $\delta < 1$, the total noise is bounded: each move adds at most $\alpha_t w_k / 2$ in coordinate $k$, and an iteration has at most $n(n - 1)$ moves, so every point ever evaluated lies within $n(n - 1)\,\alpha_0 w_k / (2(1 - \delta))$ of the coordinate range of the start points. When this bound is smaller than the box, a minimizer far from all start points is never reached. Claim 6 shows the other limit, in which the points stop at the best start point. $\blacksquare$
