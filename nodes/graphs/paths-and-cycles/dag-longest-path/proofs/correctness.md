---
title: DAG-LONGEST-PATH computes the heaviest path from the source
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed multigraph with real weights $w$ and a source $s$. For $v \in V$ let $\lambda(v)$ be the largest weight of a directed path from $s$ to $v$, and $\lambda(v) = -\infty$ if there is none.

**Termination and cycles.** Kahn's algorithm stops, and it returns an order of all $n$ vertices if and only if $G$ is acyclic (see [Kahn's algorithm](/kahns-algorithm/)). If $G$ has a cycle, line L1 stops the run. From now on $G$ is acyclic, and $T = (t_1, \ldots, t_n)$ is a topological order: each arc $(u, v)$ has $u$ before $v$. The loops of lines L4 and L6 are finite, so the run stops.

**$\lambda$ is finite or $-\infty$.** In an acyclic graph a directed walk never repeats a vertex, since the part between two visits of the same vertex would be a cycle. So there are finitely many paths from $s$, and the maximum exists when the set is not empty.

**Lemma 1 (the recurrence).** $\lambda(s) = 0$, and for $v \ne s$, $\lambda(v) = \max_{(u, v) \in E} (\lambda(u) + w(u, v))$, with the convention that the maximum over an empty set is $-\infty$ and $-\infty + w = -\infty$.

*Proof.* The only path from $s$ to $s$ is the path of one vertex, since any other would be a cycle, so $\lambda(s) = 0$. For $v \ne s$, a path $P$ from $s$ to $v$ has a last arc $(u, v)$, and $P$ without this arc is a path from $s$ to $u$ of weight at most $\lambda(u)$. So $w(P) \le \lambda(u) + w(u, v)$, and $\lambda(v)$ is at most the right-hand side. Conversely, for an arc $(u, v)$ with $\lambda(u) > -\infty$, take a path $Q$ from $s$ to $u$ of weight $\lambda(u)$. The vertex $v$ is not on $Q$: if it were, the part of $Q$ from $v$ to $u$ with the arc $(u, v)$ would be a cycle. So $Q$ followed by $(u, v)$ is a path from $s$ to $v$ of weight $\lambda(u) + w(u, v)$, and $\lambda(v)$ is at least the right-hand side. $\square$

**Lemma 2 (values are always weights of paths).** At each moment, if $L[v] > -\infty$, then following $\pi$ from $v$ gives a path from $s$ to $v$ of weight $L[v]$. In particular, $L[v] \le \lambda(v)$.

*Proof.* Initially only $L[s] = 0$ is finite, and the path of one vertex $s$ has weight 0. Line L8 sets $L[v] = L[u] + w(u, v)$ and $\pi[v] = u$ while $u$ is the vertex being processed. By the induction hypothesis there is a path from $s$ to $u$ of weight $L[u]$, and $u$ is before $v$ in $T$. After $u$ is processed, $L[u]$ and $\pi[u]$ never change, because line L8 only changes vertices that are heads of arcs out of the vertex being processed, and those are later in $T$ than it, while $u$ is already passed. So the parent chain of $u$ stays a path of weight $L[u]$, and adding the arc $(u, v)$ gives a walk of weight $L[v]$, which is a path because $G$ is acyclic. $\square$

**Lemma 3 (invariant of line L4).** When the loop of line L4 reaches $t_k$, $L[t_k] = \lambda(t_k)$.

*Proof.* By induction on $k$. Assume it for $t_1, \ldots, t_{k-1}$, and let $v = t_k$. Every arc $(u, v)$ has $u = t_i$ with $i < k$. When $u$ was processed, $L[u] = \lambda(u)$ by the induction hypothesis. If $\lambda(u) > -\infty$, line L5 let $u$ pass, and line L7 at the arc $(u, v)$ made $L[v] \ge \lambda(u) + w(u, v)$; values only go up afterwards. If $\lambda(u) = -\infty$, this arc does not count in Lemma 1. So, for $v \ne s$, $L[v] \ge \max_{(u, v)} (\lambda(u) + w(u, v)) = \lambda(v)$ by Lemma 1, and for $v = s$, $L[s] \ge 0 = \lambda(s)$ by line L3. With Lemma 2, $L[v] \le \lambda(v)$, so $L[v] = \lambda(v)$. $\square$

**Theorem.** If $G$ has a cycle, DAG-LONGEST-PATH reports it. Otherwise it stops with $L[v] = \lambda(v)$ for every vertex $v$, and for each $v$ with $L[v] > -\infty$ the parent pointers give a path from $s$ to $v$ of the largest weight.

*Proof.* The first part is the statement on line L1. A vertex keeps its value after its turn in the loop, as the proof of Lemma 2 shows, so the final $L[v]$ is the value of Lemma 3, which is $\lambda(v)$. Lemma 2 then gives the path. $\blacksquare$
