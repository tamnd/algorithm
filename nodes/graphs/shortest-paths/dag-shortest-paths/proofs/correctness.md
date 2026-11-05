---
title: Relaxing in topological order gives shortest paths in a DAG
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a directed acyclic graph with real weights $w$ and a source $s$. DAG-SHORTEST-PATHS$(G, w, s)$ ends, and at the end $d[v] = \delta(s, v)$ for each $v \in V$. For each $v \ne s$ with $d[v] < \infty$, $\pi[v] \ne$ nil and $d[v] = d[\pi[v]] + w(\pi[v], v)$.

**Termination.** Line L1 ends (Kahn's algorithm makes at most $n$ passes of its loop). The loop of line L4 visits each of the $n$ vertices once, and the inner loop visits each edge out of the current vertex once. So the algorithm ends.

**Setup.** Let $v_1, v_2, \ldots, v_n$ be the order from line L1: for each edge $(v_i, v_j)$, $i < j$. Since $G$ has no cycle, every walk is a path, so $\delta(s, v)$ is the least weight of a path from $s$ to $v$ (there are finitely many), or $\infty$ if there is none. A path visits vertices in increasing position, because each edge goes forward. We use the [upper-bound property](/edge-relaxation/): $d[v] \ge \delta(s, v)$ at all times, and $d[v]$ never increases.

**Invariant.** For $1 \le j \le n + 1$: when the loop of line L4 is about to visit $v_j$ (or has ended, for $j = n + 1$), $d[v_i] = \delta(s, v_i)$ for each $i \le j$ (for $i \le n$).

We prove the stronger statement $P(j)$: at the moment the loop starts the visit of $v_j$, $d[v_j] = \delta(s, v_j)$. Values do not change after they equal $\delta$ (they cannot go lower), and a vertex is visited before all later ones, so $P(1), \ldots, P(n)$ give the invariant and the claim.

**Proof of $P(j)$, by strong induction on $j$.** Assume $P(i)$ for all $i < j$.

*Case $\delta(s, v_j) = \infty$.* By the upper-bound property $d[v_j] = \infty$.

*Case $v_j = s$.* No path from $s$ to $s$ has an edge, because a nonempty one would be a cycle; so $\delta(s, s) = 0$. $d[s] = 0$ by line L3, and it never drops below $\delta(s, s) = 0$.

*Case $v_j \ne s$ and $\delta(s, v_j) < \infty$.* Take a shortest path $s \leadsto v_i \to v_j$. Its last edge goes forward, so $i < j$, and its prefix $s \leadsto v_i$ is a shortest path to $v_i$: a shorter path to $v_i$ plus the edge would give a shorter path to $v_j$, and it would still be a path, since $G$ has no cycle. So $\delta(s, v_j) = \delta(s, v_i) + w(v_i, v_j)$ and $\delta(s, v_i) < \infty$. By $P(i)$, $d[v_i] = \delta(s, v_i) < \infty$ when $v_i$ is visited, so line L5 lets the inner loop run, and line L7 relaxes $(v_i, v_j)$. After it, $d[v_j] \le d[v_i] + w(v_i, v_j) = \delta(s, v_j)$. Later steps before the visit of $v_j$ only lower $d[v_j]$, and the upper-bound property gives $d[v_j] \ge \delta(s, v_j)$. So $d[v_j] = \delta(s, v_j)$ when the visit of $v_j$ starts. This proves $P(j)$.

**Predecessors.** Let $v \ne s$ with $d[v] < \infty$. Then $d[v]$ was set by line L8, which also set $\pi[v] = u$ with $d[v] = d[u] + w(u, v)$ at that time, and $u$ was being visited, so $d[u] = \delta(s, u)$ was already final. Later, $d[v]$ changes only together with $\pi[v]$. So at the end $d[v] = d[\pi[v]] + w(\pi[v], v)$. Each predecessor comes earlier in the order, so following $\pi$ from $v$ ends, and it ends at $s$, the only reachable vertex without a predecessor. Thus the predecessor edges form a shortest-path tree. $\blacksquare$

**Where acyclicity is used.** Twice: a shortest path to $v_j$ enters it from an earlier vertex, and the prefix of a shortest path, extended by an edge, is still a path. With a cycle, both steps fail; this is why line L1 must check for one.
