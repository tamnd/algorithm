---
title: Depth-first search visits each vertex once and finds the reachable set
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed or undirected graph with $n$ vertices, where an undirected edge is in both adjacency lists. We say that a call DFS-VISIT$(u)$ is *active* from its start at line L5 to its end at line L10. A call that starts while another call is active ends before that call ends, because calls nest as on any call stack.

**Lemma 1 (one call for each vertex).** During DFS$(G)$, DFS-VISIT$(u)$ is called exactly one time for each $u \in V$. A vertex is white before its call, gray while its call is active, and black after it. The run stops, and the times $d[u]$ and $f[u]$ over all $u$ are the numbers $1, 2, \ldots, 2n$, each used one time, with $d[u] < f[u]$.

*Proof.* Only line L5 makes a vertex gray, only line L10 makes it black, and no line makes a vertex white after line L1. So the colour of each vertex goes from white to gray to black, and never back. A call DFS-VISIT$(u)$ is made at line L4 or line L9 only after the test that $u$ is white, and its first line makes $u$ gray. So there is at most one call for each $u$. The loop of line L3 tests each vertex, and it calls DFS-VISIT on each vertex that is still white. So after the loop, each vertex had its call, and there are exactly $n$ calls.

Each call does a finite loop over $\mathrm{Adj}[u]$ besides its own nested calls, and there are only $n$ calls in total, so the run stops. Each call increases $time$ by 1 at line L5 and by 1 at line L10, and it stores the new value in $d[u]$ and $f[u]$. Nothing else changes $time$, which starts at 0. So the $2n$ increases give the values $1, \ldots, 2n$, each stored one time. In each call, line L5 runs before line L10, so $d[u] < f[u]$. $\square$

**Lemma 2 (the gray vertices).** At each moment, the gray vertices are exactly the vertices with an active call. If they are $g_1, \ldots, g_k$ in the order of their calls, then $g_1$ was called at line L4, and $\pi[g_{i+1}] = g_i$ for $1 \le i < k$.

*Proof.* The first statement is Lemma 1. The active calls are the calls on the call stack, from the bottom $g_1$ to the top $g_k$. The bottom call comes from line L4, because a call from line L9 is made while another call is active. For $i < k$, the call of $g_{i+1}$ was made at line L9 of the call of $g_i$, which is the call just below it on the stack, and line L8 set $\pi[g_{i+1}] = g_i$ just before. $\square$

**Lemma 3 (the forest).** When DFS$(G)$ stops, $\pi[v] = $ NIL exactly for the vertices $v$ called at line L4. For each other vertex $v$, $(\pi[v], v) \in E$ and $d[\pi[v]] < d[v]$. So the edges $(\pi[v], v)$ form a forest, and each of its trees has one root called at line L4.

*Proof.* Line L1 sets each parent to NIL, and only line L8 changes $\pi[v]$. Line L8 runs for $v$ only when $v$ is white, just before the call of $v$ at line L9, so it runs at most one time for each $v$, and exactly for the vertices called at line L9. These are the vertices not called at line L4, by Lemma 1. At that moment, the call of $u = \pi[v]$ is active and $v \in \mathrm{Adj}[u]$, so $(u, v) \in E$, and $d[u]$ is already set while $d[v]$ is set later, so $d[u] < d[v]$. Along the chain $v, \pi[v], \pi[\pi[v]], \ldots$ the discovery time decreases strictly, so the chain has no repeated vertex and it ends at a vertex with parent NIL. So the parent edges contain no cycle, and each vertex is joined to exactly one root. $\square$

**Lemma 4 (reachability).** Let all vertices be white, and call DFS-VISIT$(s)$. Let $D$ be the set of vertices discovered during this call, and let $R$ be the set of vertices reachable from $s$. Then $D = R$.

*Proof.* First $D \subseteq R$. We use induction on the order of discovery. The first vertex of $D$ is $s \in R$. A later vertex $v \in D$ is discovered at line L9 in the call of some vertex $u$ with $v \in \mathrm{Adj}[u]$. This call of $u$ is active during the call of $s$, so it started during the call of $s$ or it is the call of $s$. So $u \in D$, and $u$ was discovered before $v$. By the induction hypothesis $u \in R$, and the edge $(u, v)$ gives $v \in R$.

Now $R \subseteq D$. Assume that some $w \in R$ is not in $D$. Take a path $s = x_0, x_1, \ldots, x_k = w$ in $G$, and let $i$ be the least index with $x_i \notin D$. Then $i \ge 1$ because $s \in D$, and $x_{i-1} \in D$. The call of $x_{i-1}$ started during the call of $s$, or is it, so it ends before the call of $s$ ends. In this call, the loop of line L6 reaches $x_i$, because $x_i \in \mathrm{Adj}[x_{i-1}]$. If $x_i$ is white at that moment, line L9 calls DFS-VISIT$(x_i)$ during the call of $s$, so $x_i \in D$. If $x_i$ is not white, it was discovered before that moment. All vertices were white when the call of $s$ began, so $x_i$ was discovered after that, and before the moment, which is during the call of $s$. So $x_i \in D$ again. Both cases contradict the choice of $i$. $\square$

**Theorem.** DFS$(G)$ stops after $n$ calls of DFS-VISIT. It gives each vertex one discovery time and one finish time, the times are $1, \ldots, 2n$, and the parent pointers form a forest of edges of $G$ whose roots are the vertices picked at line L4. A single call DFS-VISIT$(s)$ on a graph with all vertices white discovers exactly the vertices reachable from $s$, and the parent pointers then give a path of $G$ from $s$ to each of them.

*Proof.* The first part is Lemmas 1 and 3. The second part is Lemma 4. For the paths, follow the parent pointers from a vertex $v \in D$. By Lemma 3, each step goes back along an edge of $G$ to a vertex with a smaller discovery time, and by the first half of the proof of Lemma 4 each such vertex is in $D$. The chain ends at the only vertex of $D$ with parent NIL, which is $s$. Read backwards, it is a path from $s$ to $v$. $\blacksquare$

The [white-path theorem](/white-path-theorem/) extends Lemma 4 to each call of DFS-VISIT, also when some vertices are no longer white, and the [parenthesis theorem](/parenthesis-theorem/) describes how the intervals $[d[u], f[u]]$ nest.
