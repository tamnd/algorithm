---
title: Capacity scaling returns a maximum flow and a minimum cut
proves: [correctness, termination]
status: full
---

Let $N = (G, c, s, t)$ be a flow network with integer capacities $c(e) \ge 0$, $m$ edges and $s \ne t$, and $U = \max_e c(e)$. Write $c_f$ for the residual capacities, $f(e) = c_f(e^-)$, $G_f$ for the residual graph of arcs with $c_f > 0$, and $G_f(\Delta)$ for the arcs with $c_f \ge \Delta$.

**Claim 1 (invariant).** Before and after each augmentation, $f$ is an s-t flow, every $c_f$ is a nonnegative integer, and $c_f(e^+) + c_f(e^-) = c(e)$ for each edge.

*Proof.* True after line L1. Line L4 finds a path $P$ of $G_f(\Delta) \subseteq G_f$ from $s$ to $t$; BFS marks each vertex once, so $P$ is simple. Line L5 sets $\delta$ to the least $c_f$ on $P$, an integer with $\delta \ge \Delta \ge 1$. Line L6 is an augmentation along $P$ by its bottleneck, which keeps the invariant by the augmentation lemma of [augmenting path](/augmenting-path-flow/), and raises $|f|$ by $\delta$. $\square$

**Claim 2 (termination).** Each augmentation raises $|f|$ by at least 1, and $|f| \le c(\{s\}, V \setminus \{s\})$, so there are finitely many augmentations. Line L7 halves $\Delta$, so the loop of line L3 runs $\lfloor \log_2 U \rfloor + 1$ times, or not at all if $U = 0$.

**Claim 3 (no augmenting path at the end).** If $U \ge 1$, the last phase has $\Delta = 1$ and ends when BFS over the arcs with $c_f \ge 1$ does not reach $t$. Since all $c_f$ are integers, $c_f \ge 1$ means $c_f > 0$, so $t$ is not reachable in $G_f$. If $U = 0$, $G_f$ has no arcs at all.

**Claim 4 (optimality).** Line L8 computes the set $S$ of vertices reachable from $s$ in $G_f$, with $s \in S$ and, by Claim 3, $t \notin S$. Each edge $e = (u, v)$ with $u \in S$, $v \notin S$ has $c_f(e^+) = 0$, so $f(e) = c(e)$; each edge $(v, u)$ with $v \notin S$, $u \in S$ has $c_f(e^-) = 0$, so $f(e) = 0$. By conservation, $|f| = f(S, \bar S) - f(\bar S, S) = c(S, \bar S)$. Every s-t flow has value at most $c(S, \bar S)$ and every s-t cut has capacity at least $|f|$, so the flow is maximum and the cut is minimum. $\blacksquare$
