---
title: Breadth-first search computes the shortest-path distances
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed or undirected graph and $s \in V$. For an undirected graph, read each edge $\{u, v\}$ as the two directed edges $(u, v)$ and $(v, u)$. Let $\delta(s, v)$ be the least number of edges on a path from $s$ to $v$, and $\delta(s, v) = \infty$ if there is no path. We use $\infty + 1 = \infty$.

**Lemma 1 (edge bound).** For each edge $(u, v) \in E$, $\delta(s, v) \le \delta(s, u) + 1$.

*Proof.* If $\delta(s, u) = \infty$, there is nothing to prove. Else take a path from $s$ to $u$ with $\delta(s, u)$ edges, and add the edge $(u, v)$. This is a walk from $s$ to $v$ with $\delta(s, u) + 1$ edges. A walk contains a path with at most as many edges, so $\delta(s, v) \le \delta(s, u) + 1$. $\square$

**Lemma 2 (upper bound and single entry).** At each moment of the run:

1. $\mathrm{dist}[v] \ge \delta(s, v)$ for each $v \in V$;
2. a finite value of $\mathrm{dist}[v]$ never changes;
3. each vertex enters the queue at most one time, and it enters exactly when its distance becomes finite.

*Proof.* Lines L1 and L2 set $\mathrm{dist}[s] = 0 = \delta(s, s)$ and $\mathrm{dist}[v] = \infty$ for $v \ne s$, so statement 1 holds, and line L3 puts $s$, the only vertex with a finite distance, in the queue. After that, only line L8 writes to $\mathrm{dist}$. It runs only if $\mathrm{dist}[v] = \infty$ (line L7), so it never changes a finite value, which is statement 2. It sets $\mathrm{dist}[v] = \mathrm{dist}[u] + 1$ for an edge $(u, v)$, and by the induction hypothesis and Lemma 1, $\mathrm{dist}[u] + 1 \ge \delta(s, u) + 1 \ge \delta(s, v)$, which keeps statement 1. Line L10 enqueues $v$ exactly when line L8 makes its distance finite. Because this happens at most one time for each $v$ by statement 2, statement 3 holds. $\square$

**Lemma 3 (the queue is sorted).** While the loop body of lines L5 to L10 handles a vertex $u$, let $\langle u, v_1, \ldots, v_r \rangle$ be $u$ followed by the queue from front to back. Outside the loop body, let $\langle v_1, \ldots, v_r \rangle$ be the queue. In both cases, write $x_1, x_2, \ldots, x_k$ for the sequence. Then

$$\mathrm{dist}[x_1] \le \mathrm{dist}[x_2] \le \cdots \le \mathrm{dist}[x_k] \le \mathrm{dist}[x_1] + 1.$$

*Proof.* By induction on the steps of the run. After line L3, the sequence is $\langle s \rangle$, and the claim holds. There are three kinds of steps.

- *Line L5.* The sequence $\langle v_1, \ldots, v_r \rangle$ becomes $\langle u, v_2, \ldots, v_r \rangle$ with $u = v_1$. This is the same sequence of vertices, so the claim still holds.
- *Line L10.* The vertex $v$ goes to the back, with $\mathrm{dist}[v] = \mathrm{dist}[u] + 1$ and $u = x_1$. Before the step, $\mathrm{dist}[x_k] \le \mathrm{dist}[x_1] + 1 = \mathrm{dist}[v]$, so the sequence stays sorted. The new last value is $\mathrm{dist}[x_1] + 1$, so the last inequality still holds.
- *End of the loop body.* The vertex $u = x_1$ leaves the sequence. A sorted sequence stays sorted when its first item is removed. If the rest is not empty, $\mathrm{dist}[x_k] \le \mathrm{dist}[x_1] + 1 \le \mathrm{dist}[x_2] + 1$, and $x_2$ is the new first item.

No other line changes the queue or a finite distance, by Lemma 2. $\square$

**Corollary 4 (order of scanning).** The vertices are dequeued in non-decreasing order of $\mathrm{dist}$. If $x$ is dequeued before $y$, then $\mathrm{dist}[x] \le \mathrm{dist}[y]$.

*Proof.* When $u$ is dequeued, it is the first item of the sequence of Lemma 3, so $\mathrm{dist}[u]$ is at most the distance of each vertex in the queue at that moment. The next vertex dequeued is in the queue at that moment, or is enqueued later during the scan of $u$ with distance $\mathrm{dist}[u] + 1$. In both cases its distance is at least $\mathrm{dist}[u]$. Distances do not change after they are finite (Lemma 2), so the claim follows by induction along the order of dequeues. $\square$

**Termination.** By Lemma 2, at most $n$ vertices enter the queue. Each pass of the loop of line L4 removes one of them. So the loop runs at most $n$ times, and each pass runs the loop of line L6 over a finite list. When the loop stops, the queue is empty, so each vertex that was discovered has also been dequeued and scanned.

**Theorem.** When BFS$(G, s)$ returns, $\mathrm{dist}[v] = \delta(s, v)$ for each $v \in V$. For each $v$ with $v \ne s$ and $\delta(s, v) < \infty$, $(\pi[v], v) \in E$ and $\delta(s, \pi[v]) = \delta(s, v) - 1$.

*Proof.* Assume that some vertex has $\mathrm{dist}[v] \ne \delta(s, v)$ at the end. Among these vertices, choose $v$ with the least $\delta(s, v)$. By Lemma 2, $\mathrm{dist}[v] > \delta(s, v)$, so $\delta(s, v)$ is finite. Also $v \ne s$, because $\mathrm{dist}[s] = 0 = \delta(s, s)$. Take a shortest path from $s$ to $v$, and let $u$ be the vertex just before $v$ on it. Then $(u, v) \in E$ and $\delta(s, u) = \delta(s, v) - 1$. By the choice of $v$, $\mathrm{dist}[u] = \delta(s, u)$, which is finite. So $u$ was discovered, and by the termination argument it was dequeued and scanned. Thus

$$\mathrm{dist}[v] > \delta(s, v) = \delta(s, u) + 1 = \mathrm{dist}[u] + 1. \tag{1}$$

Look at the moment when the scan of $u$ reaches $v$ in line L7. There are three cases.

- $\mathrm{dist}[v] = \infty$ at this moment. Then line L8 sets $\mathrm{dist}[v] = \mathrm{dist}[u] + 1$, and by Lemma 2 this value stays to the end. This contradicts (1).
- $v$ was already dequeued. Then $v$ was dequeued before $u$, and Corollary 4 gives $\mathrm{dist}[v] \le \mathrm{dist}[u]$. This contradicts (1).
- $v$ is in the queue. Then $v$ is in the sequence of Lemma 3, whose first item is $u$, so $\mathrm{dist}[v] \le \mathrm{dist}[u] + 1$. This contradicts (1).

A vertex with a finite distance was enqueued by Lemma 2, so it is in the queue or already dequeued, and the three cases cover all possibilities. So no such $v$ exists, and $\mathrm{dist}[v] = \delta(s, v)$ for each $v$.

For the parents, let $v \ne s$ be reachable. Then $\mathrm{dist}[v] = \delta(s, v)$ is finite, so line L8 ran for $v$ during the scan of some $u$, and line L9 set $\pi[v] = u$ at the same time, with $(u, v) \in E$ and $\mathrm{dist}[v] = \mathrm{dist}[u] + 1$. No later step changes $\pi[v]$, because line L9 runs together with line L8. With the first part, $\delta(s, \pi[v]) = \delta(s, v) - 1$. By induction on $\delta(s, v)$, the chain $v, \pi[v], \pi[\pi[v]], \ldots$ reaches $s$ after exactly $\delta(s, v)$ steps, and read backwards it is a path from $s$ to $v$ with $\delta(s, v)$ edges, which is a shortest path. $\blacksquare$
