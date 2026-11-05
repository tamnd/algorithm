---
title: Ford-Fulkerson returns a maximum flow and a minimum cut
proves: [correctness, termination]
status: full
---

Let $N = (G, c, s, t)$ be a flow network with $G = (V, E)$, $c(e) \ge 0$ and $s \ne t$. For each edge $e = (u, v)$ the algorithm keeps two residual capacities: $c_f(e^+)$ on the arc $e^+ = (u, v)$ and $c_f(e^-)$ on the arc $e^- = (v, u)$. The residual graph $G_f$ has the arcs with positive residual capacity. We write $f(e) = c_f(e^-)$, $\bar S = V \setminus S$, and $|f| = \sum_{e \text{ out of } s} f(e) - \sum_{e \text{ into } s} f(e)$.

**Invariant (I).** Before each test of line L2:

1. $c_f(e^+) \ge 0$, $c_f(e^-) \ge 0$ and $c_f(e^+) + c_f(e^-) = c(e)$ for each edge $e$;
2. $f$ satisfies [flow conservation](/flow-conservation/) at each $v \ne s, t$;
3. if all capacities are integers, all residual capacities are integers.

Part 1 says $0 \le f(e) \le c(e)$, so with part 2, $f$ is an s-t flow.

**Initialization.** Line L1 sets $c_f(e^+) = c(e)$ and $c_f(e^-) = 0$. Part 1 holds, $f = 0$ conserves at every vertex, and the values are integers when $c$ is.

**Maintenance.** Let $P = x_1, \ldots, x_k$ be the arcs of the path found in line L2, from $s$ to $t$, and $\Delta = \min_i c_f(x_i) > 0$ (line L3). We may take $P$ simple: a depth-first search enters each vertex at most once, so the arcs on its current path form a simple path. Then $P$ uses at most one of $e^+, e^-$ for each edge $e$, because using both would visit $u$ and $v$ in both orders.

*Part 1.* Lines L5 and L6 lower $c_f(x_i)$ by $\Delta$ and raise the reverse arc by $\Delta$. For an edge $e$ whose arc is on $P$, the sum $c_f(e^+) + c_f(e^-)$ does not change, and the lowered arc stays $\ge 0$ since $\Delta \le c_f(x_i)$. Arcs of other edges do not change.

*Part 2.* If $x_i = e^+$, then $f(e) = c_f(e^-)$ rises by $\Delta$; if $x_i = e^-$, then $f(e)$ falls by $\Delta$. Fix $v \ne s, t$ on $P$; it is the head of $x_i$ and the tail of $x_{i+1}$ for one index $i$, since $P$ is simple. The arc $x_i$ enters $v$ in $G_f$: either $x_i = e^+$ for an edge $e$ into $v$ (flow in rises by $\Delta$) or $x_i = e^-$ for an edge $e$ out of $v$ (flow out falls by $\Delta$). Both raise the excess $f^{\text{in}}(v) - f^{\text{out}}(v)$ by $\Delta$. In the same way $x_{i+1}$ leaves $v$, and either raises the flow on an edge out of $v$ or lowers the flow on an edge into $v$; both lower the excess by $\Delta$. So the excess of $v$ stays 0. A vertex not on $P$ is touched by no arc.

*Part 3.* $\Delta$ is the minimum of integers, so it is an integer, and lines L5 and L6 keep all values integral.

*The value.* The arc $x_1$ leaves $s$ and no later arc enters or leaves $s$, since $P$ is simple. So $x_1$ either raises the flow on an edge out of $s$ or lowers the flow on an edge into $s$, and $|f|$ rises by exactly $\Delta$.

**Termination with integer capacities.** By part 3, each $\Delta \ge 1$, so each round raises $|f|$ by at least 1. For any s-t flow and the cut $(\{s\}, V \setminus \{s\})$, $|f| \le \sum_{e \text{ out of } s} c(e)$, a finite integer bound. So the loop runs at most $F$ times, where $F$ is the maximum flow value (the value after the last round is at most $F$ and it starts at 0). The same argument with capacities scaled by a common denominator covers rational capacities.

**The result is optimal.** Suppose line L2 finds no path. Let $S$ be the set of line L7, the vertices reachable from $s$ in $G_f$. Then $s \in S$ and $t \notin S$, so $(S, \bar S)$ is an s-t cut.

- For an edge $e = (u, v)$ with $u \in S$ and $v \in \bar S$: if $c_f(e^+) > 0$, the arc $(u, v)$ would make $v$ reachable. So $c_f(e^+) = 0$ and $f(e) = c(e)$.
- For an edge $e = (v, u)$ with $v \in \bar S$ and $u \in S$: if $c_f(e^-) > 0$, the arc $e^- = (u, v)$ would make $v$ reachable. So $f(e) = c_f(e^-) = 0$.

Summing the excess $f^{\text{in}}(w) - f^{\text{out}}(w)$ over $w \in S$: the excess is 0 for $w \ne s$ and $-|f|$ for $w = s$; each edge inside $S$ cancels, so $-|f| = f(\bar S, S) - f(S, \bar S)$. With the two facts above, $|f| = c(S, \bar S) - 0 = c(S, \bar S)$.

For any s-t flow $g$ and any s-t cut $(X, \bar X)$, the same sum gives $|g| = g(X, \bar X) - g(\bar X, X) \le c(X, \bar X)$. Applied to $g$ and $(S, \bar S)$: $|g| \le c(S, \bar S) = |f|$, so $f$ is a maximum flow. Applied to $f$ and any cut $(X, \bar X)$: $c(S, \bar S) = |f| \le c(X, \bar X)$, so $(S, \bar S)$ is a minimum cut. Line L8 returns $f$ and $S$. $\blacksquare$

**Remark.** The optimality part does not use integrality. So whenever the loop stops, for any capacities, the answer is correct; only termination needs integer or rational capacities, or a rule for choosing $P$ such as shortest paths.
