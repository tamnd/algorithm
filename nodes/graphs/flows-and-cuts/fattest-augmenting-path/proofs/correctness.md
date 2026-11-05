---
title: The fattest augmenting path algorithm returns a maximum flow in at most m ln F + 1 rounds
proves: [correctness, termination]
status: full
---

Let $N = (G, c, s, t)$ be a flow network with integer capacities $c(e) \ge 0$, $m$ edges and $s \ne t$, and let $F$ be its maximum flow value. Write $c_f$ for the residual capacities, $f(e) = c_f(e^-)$, and $G_f$ for the residual graph of arcs with $c_f > 0$. The *width* of a path in $G_f$ is the least $c_f$ on it, and $W(v)$ is the largest width of an s-v path, or 0 if there is none; $W(s) = \infty$.

**Claim 1 (the search finds widest paths).** In a search of lines L3 to L7, each vertex $u$ is marked done at most once, and at that moment $b[u] = W(u)$, and $\pi$ gives an s-u path of that width.

*Proof.* Always $b[v] \le W(v)$, because $b[v]$ is set only to the width of the walk $\pi$ to $u$ and then $x$, and the vertices on the parent chain are done, so this walk is a path. Suppose $u$ is the first vertex marked done with $b[u] < W(u)$, and let $P$ be an s-u path of width $W(u)$. Let $(y, z)$ be the first arc of $P$ with $y$ done and $z$ not done before $u$; it exists since $s$ is done first and $u$ is not done before. When $y$ was done, $b[y] = W(y) \ge W(u)$ by the choice of $u$, so line L7 set $b[z] \ge \min(W(y), c_f(y, z)) \ge W(u)$ and put $z$ in the heap with that key. The heap returned $u$ with key $b[u] < W(u) \le b[z]$ before $z$, a contradiction with extracting the largest key first, unless $z = u$, in which case $b[u] \ge W(u)$. Either way, a contradiction. $\square$

**Claim 2 (each round augments by a widest path).** If $t$ is done, line L9 sets $\Delta = W(t) > 0$, and line L10 augments along an s-t path of $G_f$ by its bottleneck. By the invariant proved for [Ford-Fulkerson](/ford-fulkerson/), $f$ stays an s-t flow, the residual capacities stay nonnegative integers, and the value grows by $\Delta$. If $t$ is not done when the heap is empty, the search has extracted every vertex reachable from $s$ in $G_f$, each with $b > 0$, and no other vertex gets $b > 0$; so $W(t) = 0$ and $t$ is not reachable.

**Claim 3 (share lemma).** Let $r = F - |f|$. Then $W(t) \ge r/m$.

*Proof.* Let $f^*$ be a maximum flow of $N$. Put $g(e^+) = \max(f^*(e) - f(e), 0)$ and $g(e^-) = \max(f(e) - f^*(e), 0)$. Then $g \le c_f$ on each arc, $g$ is positive on at most one arc of each edge, and $g$ satisfies conservation at each $v \ne s, t$ in $G_f$ with value $|f^*| - |f| = r$. By [flow decomposition](/flow-decomposition/), $g$ is a sum of at most $m$ positive flows along s-t paths and cycles, each path inside the support of $g$ and thus inside $G_f$. The paths carry $r$ in total, so one path carries at least $r/m$, and since it carries at most $g \le c_f$ on each arc, its width is at least $r/m$. $\square$

**Claim 4 (termination).** Let $r_k$ be the missing value after $k$ rounds. By Claims 2 and 3, $r_{k+1} \le r_k (1 - 1/m)$, so $r_k \le F (1 - 1/m)^k < F e^{-k/m}$ for $k \ge 1$. Each $r_k$ is a nonnegative integer. If $F = 0$ there is no round. Otherwise for $k > m \ln F$ we get $r_k < 1$, so $r_k = 0$, and the next search finds no path. So there are at most $\lfloor m \ln F \rfloor + 1$ rounds.

**Claim 5 (optimality).** When the loop stops, $S = \{v : b[v] > 0\}$ is the set of vertices reachable from $s$ in $G_f$ (Claim 2), with $t \notin S$. Each edge leaving $S$ has $c_f(e^+) = 0$, so it is full, and each edge entering $S$ has $c_f(e^-) = 0$, so it is empty. By conservation $|f| = c(S, V \setminus S)$, which bounds every flow value, so $f$ is maximum and the cut is minimum. $\blacksquare$
