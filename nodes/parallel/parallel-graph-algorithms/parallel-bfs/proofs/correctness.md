---
title: Parallel BFS computes the BFS distances and a BFS tree
proves: [correctness, termination]
status: full
---

We write $\delta(v)$ for the distance from $s$ to $v$ (the least number of edges on a path, or $\infty$), and $L_j = \{v : \delta(v) = j\}$ for the level $j$. Each `for all` loop is one synchronous step: every processor reads the state from before the step, and then all writes take place. In line L8 an arbitrary one of the concurrent writers to $parent[v]$ succeeds.

**Invariant.** At the start of the round in which the counter takes the value $d + 1$ (that is, before line L4, when the counter equals $d$):

1. $F$ lists each vertex of $L_d$ exactly once, and no other vertex;
2. $dist[v] = \delta(v)$ for each $v$ with $\delta(v) \le d$;
3. $dist[v] = \infty$ and $parent[v] = nil$ for each $v$ with $\delta(v) > d$;
4. $parent[s] = s$, and for each $v \ne s$ with $\delta(v) \le d$, $parent[v]$ is a vertex $u$ with $(u, v) \in E$ and $\delta(u) = \delta(v) - 1$.

**Initialization.** After lines L1 and L2, $d = 0$, $F = [s]$, $L_0 = \{s\}$, $dist[s] = 0$, $parent[s] = s$, and each other vertex has $dist = \infty$ and $parent = nil$. Each $v \ne s$ has $\delta(v) \ge 1 > 0$. So the four parts hold.

**Maintenance.** Assume the four parts at the start of a round, with counter $d$. Line L4 sets the counter to $d + 1$.

*Step of lines L6 to L8.* The writers are the pairs $(u, v)$ with $u \in F$, $(u, v) \in E$ and $parent[v] = nil$ before the step. By part 1, $u \in L_d$. Let $v$ be such a head. Then $parent[v] = nil$, so $v \ne s$ and, by part 4, $\delta(v) > d$. The edge $(u, v)$ gives $\delta(v) \le \delta(u) + 1 = d + 1$. So $\delta(v) = d + 1$. Conversely, let $v \in L_{d+1}$. A shortest path from $s$ to $v$ has a last edge $(u, v)$ with $\delta(u) = d$, so $u \in F$ by part 1, and $parent[v] = nil$ by part 3. So $v$ has at least one writer. The set of heads that get a write is therefore exactly $L_{d+1}$. After the step, each $v \in L_{d+1}$ has $parent[v] = u_v$ for one writer $u_v$, which is a vertex of $L_d$ with $(u_v, v) \in E$. No other cell of $parent$ changes.

*Step of lines L9 to L11.* Slot $off[j] + i$ belongs to the pair $(F[j], adj[F[j]][i])$. By line L5, the slots of different pairs differ, so the step has no concurrent writes. Fix $v$ and count the slots that write $v$. A slot $(u, v)$ writes $v$ if and only if $parent[v] = u$ and $dist[v] = \infty$ after the previous step.

- If $v \in L_{d+1}$, then $dist[v] = \infty$ by part 3, and $parent[v] = u_v$. The vertex $u_v$ is in $F$ once, and adjacency lists have no parallel edges, so exactly one slot is the pair $(u_v, v)$. Exactly one slot writes $v$.
- If $\delta(v) \le d$, then $dist[v] \ne \infty$ by part 2, and no slot writes $v$.
- If $\delta(v) > d + 1$, then $parent[v] = nil$ by part 3, since the previous step did not change it. A slot $(u, v)$ needs $parent[v] = u \ne nil$, so no slot writes $v$.

So $C$ holds each vertex of $L_{d+1}$ in exactly one slot and no other vertex.

*Lines L12 and L13.* The pack keeps the slots that are not $nil$. So the new $F$ lists each vertex of $L_{d+1}$ exactly once, and part 1 holds for $d + 1$. Line L13 sets $dist[v] = d + 1 = \delta(v)$ for $v \in L_{d+1}$ and changes no other entry, so part 2 holds for $d + 1$. For $\delta(v) > d + 1$, neither $dist[v]$ nor $parent[v]$ changed in the round, so part 3 holds for $d + 1$. For part 4, the entries of $parent$ for $\delta(v) \le d$ did not change, since those vertices had a parent and line L8 writes only a $nil$ cell. Each new entry is $u_v \in L_d$ with $(u_v, v) \in E$ and $\delta(u_v) = d = \delta(v) - 1$. So part 4 holds for $d + 1$.

**Termination.** Let $e = \max \{\delta(v) : \delta(v) < \infty\}$. Each round raises the counter by exactly 1. By part 1, when the counter reaches $e + 1$, the frontier is $L_{e+1} = \emptyset$, because a vertex at distance $e + 1$ would be reachable and farther than $e$. While the counter is at most $e$, $F = L_d$ is not empty, since a shortest path to a vertex of $L_e$ passes through each level $L_0, \ldots, L_e$. So the loop of line L3 runs exactly $e + 1 = D$ rounds and stops.

**Result.** At the exit the counter equals $e + 1$. Part 2 gives $dist[v] = \delta(v)$ for each reachable $v$. Each unreachable $v$ has $\delta(v) = \infty > e + 1$, so part 3 gives $dist[v] = \infty$ and $parent[v] = nil$. Part 4 says that each reachable $v \ne s$ has a parent that is a neighbour one level closer to $s$. Following parents from $v$ lowers $\delta$ by 1 at each step, so it reaches $s$ after $\delta(v)$ steps. The parent edges therefore form a tree rooted at $s$ in which the depth of each vertex is its distance, which is a BFS tree. $\blacksquare$
