---
title: Direction-optimizing BFS computes the BFS distances and a BFS tree
proves: [correctness, termination]
status: full
---

We write $\delta(v)$ for the distance from $s$ to $v$ in $G$ (the least number of edges on a directed path, or $\infty$), and $L_j = \{v : \delta(v) = j\}$. An in-neighbour of $v$ is a vertex $u$ with $(u, v) \in E$.

**Invariant.** At the start of each round, when the counter equals $d$ (before line L4):

1. $F$ lists each vertex of $L_d$ exactly once, and no other vertex;
2. $dist[v] = \delta(v)$ for each $v$ with $\delta(v) \le d$;
3. $dist[v] = \infty$ and $parent[v] = nil$ for each $v$ with $\delta(v) > d$;
4. $parent[s] = s$, and for each $v \ne s$ with $\delta(v) \le d$, $parent[v]$ is an in-neighbour $u$ of $v$ with $\delta(u) = \delta(v) - 1$;
5. $m_u = \sum \{ indeg(v) : \delta(v) > d \}$.

**Initialization.** After lines L1 and L2, $d = 0$, $F = [s] = L_0$, $dist[s] = 0$, $parent[s] = s$, every other vertex has $dist = \infty$ and $parent = nil$, and $m_u$ is the sum of the in-degrees of the vertices other than $s$, which are the vertices with $\delta > 0$. So the five parts hold.

**Maintenance.** Assume the five parts at the start of a round with counter $d$. Lines L4 to L8 change only $d$, $m_f$, $mode$ and $n_{prev}$, so the parts about $F$, $dist$ and $parent$ still hold after them, with $d$ replaced by the old value. We show that each of the two steps returns a list $F'$ that holds each vertex of $L_{d+1}$ exactly once and no other vertex, and that it sets $parent[v]$ to an in-neighbour of $v$ in $L_d$ for each $v \in L_{d+1}$ and changes no other cell of $parent$.

*The top-down step (lines L14 to L16).* These are lines L6 to L12 of [parallel BFS](/parallel-bfs/), and the proof of that page shows this claim under parts 1 to 4. Its proof uses only those parts.

*The bottom-up step (lines L17 to L21).* Line L17 sets $in_F[u]$ true exactly for $u \in L_d$, by part 1. The bitmap does not change during the step. Each vertex $v$ of line L18 writes only $parent[v]$ and its own mark, so the scans do not interact and there are no concurrent writes. The vertices of line L18 are those with $dist[v] = \infty$, which by parts 2 and 3 are the vertices with $\delta(v) > d$. Take such a $v$.

- If $\delta(v) = d + 1$, the last edge $(u, v)$ of a shortest path has $\delta(u) = d$, so $in_F[u]$ is true. The scan of line L19 reads the in-list in order, and it reaches $u$ unless it stops earlier at another $u'$ with $in_F[u']$ true. In both cases it stops at an in-neighbour $u^\ast \in L_d$, and line L20 sets $parent[v] = u^\ast$ and marks $v$.
- If $\delta(v) > d + 1$, then $v$ has no in-neighbour $u$ with $\delta(u) = d$: such a $u$ would give $\delta(v) \le d + 1$. So no flag is true along its scan, and $v$ is not marked and $parent[v]$ stays $nil$.

Vertices with $\delta(v) \le d$ are not scanned, so their cells do not change. Line L21 packs the marked vertices, each once, in increasing order. So $F'$ lists $L_{d+1}$ once and the claim holds.

*Lines L11 and L12.* Line L11 sets $dist[v] = d + 1 = \delta(v)$ for each $v \in L_{d+1}$ and changes no other $dist$ entry, and line L12 sets $F = F'$. So parts 1 and 2 hold for $d + 1$. For $\delta(v) > d + 1$, no step changed $dist[v]$ or $parent[v]$, so part 3 holds for $d + 1$. The parents of the vertices with $\delta \le d$ did not change, and each $v \in L_{d+1}$ got an in-neighbour in $L_d$, so part 4 holds for $d + 1$. Line L11 subtracts the in-degrees of the vertices of $L_{d+1}$ from $m_u$, so part 5 holds for $d + 1$.

The choice of the mode in lines L6 and L7 reads only $m_f$, $m_u$, $|F|$, $n_{prev}$ and $n$, and both steps keep the invariant, so the invariant holds for each sequence of modes.

**Termination.** Let $e$ be the largest finite $\delta(v)$. While the counter is at most $e$, the set $L_d$ is not empty, since a shortest path to a vertex of $L_e$ passes through every level $L_0, \ldots, L_e$. When the counter reaches $e + 1$, part 1 gives $F = L_{e+1} = \emptyset$. Each round raises the counter by exactly 1, so the loop of line L3 stops after exactly $e + 1$ rounds.

**Result.** At the exit, part 2 gives $dist[v] = \delta(v)$ for each reachable $v$, and part 3 gives $dist[v] = \infty$ and $parent[v] = nil$ for each unreachable $v$. By part 4, following parents from a reachable $v$ lowers $\delta$ by 1 at each step and reaches $s$ after $\delta(v)$ steps along edges of $G$, so the parent edges form a BFS tree rooted at $s$. $\blacksquare$
