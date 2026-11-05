---
title: Cycle canceling returns a minimum-cost maximum flow
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph with integer capacities $c(e) \ge 0$, integer costs $w(e)$ and $s \ne t$. Write $c_f$ for the residual capacities, $f(e) = c_f(e^-)$, $G_f$ for the residual graph of arcs with $c_f > 0$, with $w(e^+) = w(e)$ and $w(e^-) = -w(e)$, and $w(f) = \sum_e w(e) f(e)$.

**Claim 1 (canceling keeps a maximum flow and lowers the cost).** Let $C$ be a cycle of $G_f$ and $0 < \delta \le \min_{a \in C} c_f(a)$. Pushing $\delta$ around $C$ as in line L8 gives residual capacities that are nonnegative and satisfy $c_f(e^+) + c_f(e^-) = c(e)$, so $f$ stays within its bounds. At each vertex of $C$ one arc of $C$ enters and one leaves, so the net flow at every vertex, including $s$ and $t$, is unchanged: $f$ is still a maximum flow. Pushing $\delta$ on $e^+$ raises $f(e)$ by $\delta$ and changes the cost by $\delta w(e)$; on $e^-$ it lowers $f(e)$ by $\delta$ and changes the cost by $-\delta w(e) = \delta w(e^-)$. So the cost changes by $\delta \cdot w(C)$. $\square$

**Claim 2 (negative cycle optimality).** A maximum flow $f$ has least cost among maximum flows if and only if $G_f$ has no cycle of negative cost.

*Proof.* If $G_f$ has a negative cycle, Claim 1 gives a cheaper maximum flow. Conversely, let $f^*$ be any maximum flow and set $g(e^+) = \max(f^*(e) - f(e), 0)$ and $g(e^-) = \max(f(e) - f^*(e), 0)$. Then $0 \le g \le c_f$ arc by arc, $g$ is positive only on arcs of $G_f$, and since $f$ and $f^*$ have the same net flow at every vertex (0 inside, and $\pm$ the common maximum value at $s$ and $t$), $g$ is a circulation. Its cost is $\sum_e w(e)(f^*(e) - f(e)) = w(f^*) - w(f)$. By [flow decomposition](/flow-decomposition/), a circulation is a sum of positive multiples of cycles in its support, so $w(f^*) - w(f)$ is a nonnegative combination of costs of cycles of $G_f$. If none is negative, $w(f^*) \ge w(f)$. $\square$

**Claim 3 (line L4 to L7 find a negative cycle exactly when one exists).** Line L4 is Bellman-Ford on $G_f$ from a virtual source joined to every vertex by an arc of cost 0. If $G_f$ has no negative cycle, a shortest path from the virtual source has at most $n$ arcs, the first of which is a virtual arc of cost 0, so after $n - 1$ rounds over the real arcs all values are final and round $n$ changes nothing. If $G_f$ has a negative cycle, the values along it cannot all be final, since summing $d(v) \le d(u) + w(u, v)$ around the cycle would give $0 \le w(C) < 0$; so some round changes a value, and every round up to $n$ does. By the standard lemma for Bellman-Ford (see [negative cycle detection](/negative-cycle-detection/)), when a value changes in round $n$, the predecessor graph contains a cycle reachable backward from the changed vertex within $n$ steps, and every cycle of the predecessor graph has negative cost. Line L6 walks $n$ predecessor steps, which is enough to enter that cycle, and line L7 reads it. Each predecessor arc was set while it had $c_f > 0$, and Bellman-Ford does not change $c_f$, so the cycle lies in $G_f$.

**Claim 4 (termination).** All data are integers, so each $c_f$ is an integer, $\delta \ge 1$, and a negative cycle has $w(C) \le -1$. By Claim 1 each cancellation lowers $w(f)$ by at least 1. Every $f$ with $0 \le f \le c$ has $w(f) \ge -\sum_e |w(e)| c(e)$, so the loop ends.

**Claim 5 (optimality).** Line L2 gives a maximum flow, Claim 1 keeps it maximum, and the loop ends (Claim 4) when, by Claim 3, $G_f$ has no negative cycle. By Claim 2 the flow returned has least cost among maximum flows. $\blacksquare$
