---
title: Kahn's algorithm returns a topological ordering or detects a cycle
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph with $n$ vertices, possibly with parallel edges and self-loops, where each copy of an edge is one entry of an adjacency list. For a set $S \subseteq V$, write $\mathrm{in}_S(v)$ for the number of edges $(u, v)$ with $u \notin S$. Let $L$ also stand for the set of vertices in the list $L$.

**Invariant.** At the start of each iteration of the loop of line L5, and when the loop ends:

1. $\mathrm{in}[v] = \mathrm{in}_L(v)$ for each $v \notin L$;
2. $Q$ holds, each one time, exactly the vertices $v \notin L$ with $\mathrm{in}[v] = 0$;
3. for each edge $(u, v)$ with $v \in L$, also $u \in L$, and $u$ is before $v$ in $L$.

*Initialization.* After line L2, $\mathrm{in}[v]$ is the number of entries $v$ in all lists, the in-degree of $v$, and $L$ is empty, so part 1 holds. Line L4 enqueues each vertex with $\mathrm{in}[v] = 0$ once, so part 2 holds. Part 3 holds because $L$ is empty.

*Maintenance.* Let one iteration dequeue $u$. By part 2, $u \notin L$ and $\mathrm{in}[u] = 0$, so by part 1 each edge into $u$ comes from a vertex in $L$. Line L6 appends $u$ to $L$. Part 3 holds for the new $L$: for edges $(x, u)$, $x$ is in the old $L$ and so before $u$, and $u \ne x$ because a self-loop $(u, u)$ would give $\mathrm{in}_L(u) \ge 1$. Edges into older vertices of $L$ are unchanged. For part 1, the new value of $\mathrm{in}_L(v)$ for $v \notin L$ is the old value minus the number of edges $(u, v)$, and lines L7 and L8 decrease $\mathrm{in}[v]$ one time for each such entry of $\mathrm{Adj}[u]$. Entries $v$ that are already in $L$ are decreased too, but their counts are not used again. For part 2, a vertex $v \notin L$ whose count becomes zero in this iteration had a positive count before, so it was not in $Q$, and line L9 enqueues it once, at the decrease that makes the count zero. A count that is already zero is never decreased again for $v \notin L$, because a decrease of $v$ comes from an edge $(u, v)$ with $u \notin L$, which part 1 counts. So no vertex is enqueued twice. The vertex $u$ left $Q$ and joined $L$. So part 2 holds.

**Termination.** By part 2, each dequeued vertex joins $L$ and never returns to $Q$, so the loop of line L5 runs at most $n$ times, and each iteration scans one finite list.

**Lemma (remaining vertices).** When the loop ends, let $R = V \setminus L$. If $R$ is not empty, then $G$ has a directed cycle all of whose vertices are in $R$.

*Proof.* The queue is empty, so by part 2 each $v \in R$ has $\mathrm{in}[v] \ne 0$, and by part 1 there is an edge $(u, v)$ with $u \notin L$, that is, $u \in R$. Start at some $w_0 \in R$, and choose $w_{i+1} \in R$ with $(w_{i+1}, w_i) \in E$. Among $w_0, \ldots, w_{|R|}$ some vertex repeats, $w_i = w_j$ with $i < j$, and $w_j, w_{j-1}, \ldots, w_{i+1}$ with the edge $(w_{i+1}, w_i)$ is a directed cycle in $R$. $\square$

**Theorem.** KAHN$(G)$ terminates. If $G$ is acyclic, it returns a topological ordering. If $G$ has a directed cycle, it reports a cycle.

*Proof.* Termination was shown above.

If $G$ is acyclic, the lemma shows that $R$ is empty when the loop ends. So $|L| = n$, line L10 does not report, and $L$ holds each vertex once, by part 2. By part 3, applied with $L = V$, each edge $(u, v)$ has $u$ before $v$. So $L$ is a topological ordering.

If $G$ has a directed cycle $C$, no vertex of $C$ is in $L$ at the end. Assume otherwise, and let $x$ be the vertex of $C$ appended to $L$ first, and $w$ the vertex before $x$ on $C$, so $(w, x) \in E$. By part 3, at the iteration after $x$ joined $L$, $w$ is in $L$ and before $x$. If $w = x$, this says $x$ is before itself, which is false. Otherwise $w$ is a vertex of $C$ appended before $x$, which contradicts the choice of $x$. So $|L| \le n - |C| < n$, and line L10 reports a cycle. $\blacksquare$
