---
title: The ANF sketches are the Flajolet-Martin sketches of the balls
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph; an undirected graph has both arcs for each edge, and $\mathrm{Adj}[v]$ lists the heads of the arcs out of $v$. Fix the random positions $\rho_j(u)$ for each vertex $u$ and copy $j = 1, \ldots, r$. For a set $S \subseteq V$, let $M_j(S) = \bigvee_{u \in S} 2^{\rho_j(u)}$, the bitwise OR, with $M_j(\emptyset) = 0$. Let $B_h(v)$ be the set of vertices reachable from $v$ by a path of at most $h$ arcs.

**Termination.** Line L1 and each of the $h_{\max}$ rounds of line L3 are loops over finite sets of vertices, arcs and copies. So the algorithm stops.

**Lemma 1 (union).** $M_j(S \cup T) = M_j(S) \vee M_j(T)$ for all $S, T \subseteq V$.

*Proof.* Bit $i$ of $M_j(S \cup T)$ is 1 if and only if some $u \in S \cup T$ has $\rho_j(u) = i$, that is, if and only if some $u \in S$ or some $u \in T$ has it, which is the condition for bit $i$ of $M_j(S) \vee M_j(T)$. The overlap $S \cap T$ plays no role, since $1 \vee 1 = 1$. $\square$

**Lemma 2 (balls).** $B_0(v) = \{v\}$, and for $h \ge 1$,

$$B_h(v) = \{v\} \cup \bigcup_{u \in \mathrm{Adj}[v]} B_{h-1}(u).$$

*Proof.* A path of length 0 from $v$ ends at $v$. For $h \ge 1$, take $w \in B_h(v)$. If $w = v$, it is in the right side. Else a shortest path from $v$ to $w$ has between 1 and $h$ arcs; its first arc goes to some $u \in \mathrm{Adj}[v]$, and the rest is a path from $u$ to $w$ of at most $h - 1$ arcs, so $w \in B_{h-1}(u)$. Conversely, $v \in B_h(v)$, and a path of at most $h - 1$ arcs from an out-neighbour $u$ of $v$ to $w$, after the arc $(v, u)$, is a walk of at most $h$ arcs from $v$ to $w$, which contains a path of at most $h$ arcs. $\square$

**Theorem.** After line L1, and after the round $h$ of lines L4 to L6 for each $h = 1, \ldots, h_{\max}$, $M[v][j] = M_j(B_h(v))$ for all $v$ and $j$. Hence line L7 (and line L2 for $h = 0$) sets $\hat N(h) = \sum_v \mathrm{ESTIMATE}(M_1(B_h(v)), \ldots, M_r(B_h(v)))$.

*Proof.* By induction on $h$. Line L1 sets $M[v][j] = 2^{\rho_j(v)} = M_j(\{v\}) = M_j(B_0(v))$.

Assume $M[v][j] = M_j(B_{h-1}(v))$ for all $v, j$ at the start of round $h$. Line L4 sets $M'[v][j] = M_j(B_{h-1}(v))$. Line L5 reads only $M$, which does not change during the round, and ORs into $M'[v][j]$ the value $M[u][j] = M_j(B_{h-1}(u))$ for each $u \in \mathrm{Adj}[v]$. Since OR is associative, commutative and idempotent, the order of these steps and repeated arcs do not matter, and after line L5,

$$M'[v][j] = M_j(B_{h-1}(v)) \vee \bigvee_{u \in \mathrm{Adj}[v]} M_j(B_{h-1}(u)) = M_j\Bigl(B_{h-1}(v) \cup \bigcup_{u \in \mathrm{Adj}[v]} B_{h-1}(u)\Bigr)$$

by Lemma 1. For $h \ge 1$, $B_{h-1}(v) \subseteq B_h(v)$ and $v \in B_{h-1}(v)$, so by Lemma 2 the set in the brackets equals $B_h(v)$. Line L6 makes $M = M'$, which gives the claim for $h$. Line L7 applies ESTIMATE to these values. $\blacksquare$

The theorem makes $\hat N(h)$ a sum of Flajolet-Martin estimates of the true sizes $|B_h(v)|$, with the same random positions for every $v$; the statistical accuracy of each term is the one proved by Flajolet and Martin for their estimator.
