---
title: Edmonds-Karp returns a maximum flow and a minimum cut
proves: [correctness, termination]
status: full
---

Let $N = (G, c, s, t)$ be a flow network with real capacities $c(e) \ge 0$ and $s \ne t$. Write $c_f$ for the residual capacities, $f(e) = c_f(e^-)$, and $G_f$ for the residual graph of arcs with $c_f > 0$.

**Claim 1 (each round is a Ford-Fulkerson round).** Lines L2 to L7 are a breadth-first search in $G_f$ from $s$: line L6 follows an arc only if $c_f(x) > 0$. If it marks $t$, the parent arcs $\pi$ give a path from $s$ to $t$ in $G_f$, and each vertex on it is marked once, so the path is simple. Lines L9 and L10 augment along it by its bottleneck $\Delta > 0$. By the invariant proved for [Ford-Fulkerson](/ford-fulkerson/) (residual capacities stay nonnegative, $c_f(e^+) + c_f(e^-) = c(e)$, and conservation holds), $f$ stays an s-t flow, and its value grows by $\Delta$.

**Claim 2 (termination).** The number of rounds is at most $nm$. This is proved in the complexity proof, Theorem 2; it uses no property of the capacities other than being real and nonnegative. So the loop of line L2 ends.

**Claim 3 (the search at the end is complete).** In the last round line L8 finds $t$ unmarked. Then the loop of line L4 stopped because $Q$ was empty, so the search ran to the end, and the marked vertices are exactly the vertices reachable from $s$ in $G_f$.

**Claim 4 (optimality).** Let $S$ be the marked set of the last round, so $s \in S$ and $t \notin S$. Each edge $(u, v)$ with $u \in S$, $v \notin S$ has $c_f(e^+) = 0$, so $f(e) = c(e)$; each edge $(v, u)$ with $v \notin S$, $u \in S$ has $c_f(e^-) = 0$, so $f(e) = 0$. By conservation, $|f| = f(S, \bar S) - f(\bar S, S) = c(S, \bar S)$. Since every s-t flow $g$ has $|g| \le c(S, \bar S)$ and every s-t cut $X$ has $c(X, \bar X) \ge |f|$, the flow is maximum and the cut is minimum. $\blacksquare$
