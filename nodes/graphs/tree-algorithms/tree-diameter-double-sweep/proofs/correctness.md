---
title: The double sweep returns the diameter of a tree with non-negative lengths
proves: [correctness, termination]
status: full
---

Let $T$ be a tree on $n \ge 1$ vertices with edge lengths $w \ge 0$. For two vertices $u, v$, $d(u, v)$ is the total length of the unique path between them, $\mathrm{ecc}(v) = \max_u d(v, u)$, and $D = \max_v \mathrm{ecc}(v)$.

**Lemma 1 (DISTANCES).** DISTANCES$(T, s)$ terminates, marks every vertex, and returns $d[v] = d(s, v)$ for each $v$, with $par$ links that lead from each $v \ne s$ back to $s$ along the path from $s$ to $v$.

*Proof.* A vertex is pushed only when it is marked, and it is marked only once (line L13 skips marked vertices), so at most $n$ pushes and $n$ pops happen, and the loop of line L10 ends. Every pushed vertex is popped before the loop ends. If some vertex were not marked, then, since $T$ is connected, some edge would join a marked vertex $x$ to an unmarked vertex $y$. When $x$ was popped, line L12 would have found $y$ unmarked and marked it, a contradiction. So all vertices are marked.

Order the vertices by the time they are marked. For $v \ne s$, $par[v]$ was marked before $v$. So the chain $v, par[v], par[par[v]], \ldots$ has strictly decreasing mark times, has no repeated vertex, and ends at $s$, the only vertex with $par = -1$. Consecutive vertices of the chain are adjacent. So the chain, read backwards, is a simple path from $s$ to $v$, and it is the only one in a tree. By induction on the mark time, $d[v] = d[par[v]] + w(par[v], v)$ is the length of this path, which is $d(s, v)$. $\square$

**Projection.** Fix a diametral path $P$ with ends $x, y$, so $d(x, y) = D$. For each vertex $v$, let $\pi(v)$ be the vertex of $P$ with the smallest number of edges to $v$, and $h(v) = d(v, \pi(v))$.

**Lemma 2.** For each vertex $v$ and each vertex $z$ of $P$, the path from $v$ to $z$ is the path from $v$ to $\pi(v)$ followed by the part of $P$ from $\pi(v)$ to $z$. So $d(v, z) = h(v) + d(\pi(v), z)$. Moreover, if a vertex $u$ lies on the path from $v$ to $\pi(v)$, then $\pi(u) = \pi(v)$.

*Proof.* The path $Q$ from $v$ to $\pi(v)$ meets $P$ only at $\pi(v)$: an earlier vertex of $Q$ on $P$ would be closer to $v$. So $Q$ followed by the part of $P$ from $\pi(v)$ to $z$ has no repeated vertex, and it is a path from $v$ to $z$, the unique one. Its length is $h(v) + d(\pi(v), z)$. For $u$ on $Q$, the part of $Q$ from $u$ to $\pi(v)$ meets $P$ only at its end, and by the first part (applied to $u$) the path from $u$ to each vertex of $P$ starts with the path to $\pi(u)$. The path from $u$ to $\pi(v)$ meets $P$ first at $\pi(v)$, so $\pi(u) = \pi(v)$. $\square$

**Lemma 3 (the farthest vertex is an end).** Let $s$ be any vertex and $a$ a vertex with $d(s, a) = \mathrm{ecc}(s)$. Then $\mathrm{ecc}(a) = D$.

*Proof.* Let $t = \pi(s)$ and $t_a = \pi(a)$. Since $a$ is farthest from $s$, Lemma 2 gives

$$d(s, a) \ge d(s, x) = h(s) + d(t, x), \qquad d(s, a) \ge d(s, y) = h(s) + d(t, y). \tag{1}$$

*Case 1: $t_a \ne t$.* The path from $s$ to $t$ and the path from $t_a$ to $a$ have no common vertex: a common vertex $u$ would have $\pi(u) = t$ and $\pi(u) = t_a$ by Lemma 2. So the path from $s$ to $t$, then the part of $P$ from $t$ to $t_a$, then the path from $t_a$ to $a$ has no repeated vertex, and it is the path from $s$ to $a$. Hence $d(s, a) = h(s) + d(t, t_a) + h(a)$. The vertex $t_a$ lies on $P$ on one side of $t$. Say that it lies between $t$ and $y$ (the other case is the same with $x$ and $y$ swapped). Then $d(t, y) = d(t, t_a) + d(t_a, y)$, and the second inequality of (1) gives $h(a) \ge d(t_a, y)$. By Lemma 2, $d(a, x) = h(a) + d(t_a, x) \ge d(t_a, y) + d(t_a, x) = D$.

*Case 2: $t_a = t$.* The walk from $s$ to $t$ and then from $t$ to $a$ has length $h(s) + h(a)$. In a tree, the path from $s$ to $a$ is obtained from this walk by deleting closed sub-walks, which have non-negative length because $w \ge 0$. So $d(s, a) \le h(s) + h(a)$. With the first inequality of (1), $h(a) \ge d(t, x)$. By Lemma 2, $d(a, y) = h(a) + d(t, y) \ge d(t, x) + d(t, y) = D$.

In both cases $\mathrm{ecc}(a) \ge D$, and $\mathrm{ecc}(a) \le D$ by the definition of $D$. $\square$

**Theorem.** DOUBLE-SWEEP$(T)$ terminates and returns $D$ and a path of length $D$.

*Proof.* By Lemma 1, line L1 computes $d(0, \cdot)$, so line L2 picks a vertex $a$ with $d(0, a) = \mathrm{ecc}(0)$. By Lemma 3 with $s = 0$, $\mathrm{ecc}(a) = D$. By Lemma 1, line L3 computes $d(a, \cdot)$, so line L4 picks $b$ with $d(a, b) = \mathrm{ecc}(a) = D$. Lines L5 to L7 follow the parent links from $b$, which by Lemma 1 reach $a$ after at most $n - 1$ steps along the path from $a$ to $b$, so the loop ends. Line L8 returns $D$ and this path, which has length $d(a, b) = D$. $\blacksquare$

**Where $w \ge 0$ is used.** Only in Case 2 of Lemma 3. On the path $0, 1, 2$ with $w(01) = -2$ and $w(12) = 1$, the vertex $a = 0$ is farthest from $s = 0$, both are projected to the same vertex of the diametral path $1, 2$, and $\mathrm{ecc}(0) = 0 < D = 1$.

**Corollary (eccentricities).** For $w \ge 0$ and each vertex $v$, $\mathrm{ecc}(v) = \max(d(v, a), d(v, b))$, where $a, b$ are the ends found by the algorithm.

*Proof.* Take $P$ to be the path from $a$ to $b$, which is diametral, and define $\pi$ and $h$ for it. First, $h(z) \le \min(d(\pi(z), a), d(\pi(z), b))$ for each vertex $z$: if $h(z) > d(\pi(z), a)$, then by Lemma 2 $d(z, b) = h(z) + d(\pi(z), b) > d(a, \pi(z)) + d(\pi(z), b) = D$, which is impossible, and the same holds with $a$ and $b$ swapped. Now let $z$ be any vertex and $t = \pi(v)$. The walk from $v$ to $t$, along $P$ to $\pi(z)$, then to $z$ has length $h(v) + d(t, \pi(z)) + h(z)$, and since $w \ge 0$ the path from $v$ to $z$ is not longer. If $\pi(z)$ lies between $t$ and $a$, then $h(z) \le d(\pi(z), a)$ gives $d(v, z) \le h(v) + d(t, a) = d(v, a)$. Otherwise $\pi(z)$ lies between $t$ and $b$, and in the same way $d(v, z) \le d(v, b)$. So $\mathrm{ecc}(v) \le \max(d(v, a), d(v, b))$, and the other inequality holds by the definition of $\mathrm{ecc}$. $\square$
