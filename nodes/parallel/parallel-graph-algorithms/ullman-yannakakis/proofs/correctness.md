---
title: The sampled closure never adds a false pair and is exact with probability at least 1 - n^(3-c)
proves: [correctness, complexity]
status: full
---

**Setting.** $G = (V, A)$ is a directed graph with $n \ge 2$ vertices and $m$ arcs, $t \ge 1$ is the depth and $c > 0$. "$u$ reaches $v$" means that there is a directed path from $u$ to $v$, of zero or more arcs. $R(v)$ is the set of vertices at most $t$ arcs from $v$. Each vertex joins the sample $S$ independently with probability $p = \min(1, c \ln n / t)$, and $s = |S|$. $H$ is the graph on $S$ with an arc $a \to b$ when $b \in R(a)$, and $H^*$ is its reflexive transitive closure. The output row of $u$ is $C(u) = R(u) \cup \bigcup \{R(b) : b \in S, (a, b) \in H^* \text{ for some } a \in S \cap R(u)\}$.

**Lemma 1 (squaring).** After $k$ rounds of lines L4 and L5, $H(a, b) = 1$ exactly when $H$ has a path from $a$ to $b$ with at most $2^k$ arcs. So $\lceil \log_2 s \rceil$ rounds give $H^*$.

*Proof.* At the start, $H$ is reflexive, since $a \in R(a)$, so the claim holds for $k = 0$. If it holds for $k$, then $H \lor H \cdot H$ has a 1 at $(a, b)$ exactly when a path of at most $2^k$ arcs, or two such paths joined at a middle vertex, leads from $a$ to $b$, which is the claim for $k + 1$. A path in $H$ between two vertices of $S$ needs at most $s - 1 < 2^{\lceil \log_2 s \rceil}$ arcs. $\square$

**Lemma 2 (soundness).** Every pair in the output is a true pair: if $v \in C(u)$, then $u$ reaches $v$. This holds for every sample.

*Proof.* If $v \in R(u)$, this is clear. Otherwise $u$ reaches some $a \in S \cap R(u)$, $a$ reaches $b$ through arcs of $H$, each of which stands for a path in $G$, and $b$ reaches $v$. $\square$

**Lemma 3 (the window condition is enough).** Let $u$ reach $v$, and let $x_0 = u, x_1, \ldots, x_k = v$ be a shortest path. If $k \le t$, or if every set of $t$ consecutive vertices $x_i, \ldots, x_{i+t-1}$ on the path contains a vertex of $S$, then $v \in C(u)$. Moreover, the graph $G$ with the arcs of $H^*$ added has a path from $u$ to $v$ with at most $2t - 1$ arcs.

*Proof.* If $k \le t$, then $v \in R(u)$, and the path itself has $k \le t \le 2t - 1$ arcs. Let $k > t$, and let $x_{i_1}, \ldots, x_{i_r}$ with $i_1 < \cdots < i_r$ be the sampled vertices on the path. The window $x_0, \ldots, x_{t-1}$ gives $i_1 \le t - 1$, so $x_{i_1} \in R(u)$. Two consecutive sampled vertices are at most $t$ positions apart, since the $t$ vertices after $x_{i_j}$ contain a sampled one, or the path ends before them; the part of the path between them has at most $t$ arcs, so $x_{i_{j+1}} \in R(x_{i_j})$ and $H$ has the arc. The last window gives $i_r \ge k - t + 1$, so $v \in R(x_{i_r})$. So $(x_{i_1}, x_{i_r}) \in H^*$, and $v \in C(u)$. The path $u \to x_{i_1}$ along $G$, then one arc of $H^*$, then $x_{i_r} \to v$ along $G$, has at most $(t - 1) + 1 + (t - 1)$ arcs. $\square$

**Theorem 1 (correctness).** The output is a subset of the reflexive transitive closure of $G$ for every sample, and with probability at least $1 - n^{3 - c}$ it equals the closure.

*Proof.* The first part is Lemma 2. For the second, fix one shortest path for each of the at most $n^2$ pairs $(u, v)$ with $u$ reaching $v$. Each path has fewer than $n$ windows of $t$ consecutive vertices. If $p = 1$, every vertex is sampled and nothing fails. Otherwise, a fixed window misses $S$ with probability $(1 - p)^t \le e^{-pt} = n^{-c}$. By the union bound over fewer than $n^3$ windows, all windows contain a sampled vertex with probability at least $1 - n^{3 - c}$, and then Lemma 3 gives every pair. $\blacksquare$

**Theorem 2 (cost).** In the work-span model, the work is $W = O(n(n + m) + s^3 \log s + n^2 s)$ and the span is $S = O(t \log n + \log^2 n)$. The expected sample size is $E[s] = np \le c\, n \ln n / t$.

*Proof.* Line L2 runs $n$ breadth-first searches of depth $t$ at the same time. Each search visits each vertex and each arc at most once, so the work is $O(n(n + m))$; there are $t$ rounds, each with $O(\log n)$ span for the pack of the next frontiers. Line L3 costs $O(s^2)$ work and $O(1)$ span. By Lemma 1 there are $\lceil \log_2 s \rceil$ Boolean products of $s \times s$ matrices, each with $O(s^3)$ work and $O(\log s)$ span for the OR of $s$ terms. Lines L6 and L7 are two Boolean products of an $n \times s$ matrix with an $s \times s$ and an $s \times n$ matrix, with $O(n^2 s)$ work and $O(\log n)$ span. The expected sample size follows from linearity of expectation. $\blacksquare$
