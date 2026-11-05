---
title: The two-level Infomap search lowers the map equation at every move, stops, and ends where no module gains by joining a neighbouring module
proves: [correctness, termination]
status: full
---

The proof is for the search of the page: undirected graphs without self-loops, the two-level map equation, and local moves with aggregation. The fine-tuning and coarse-tuning steps, teleportation and the multilevel map equation are not covered.

Let $G$ be an undirected graph on $V$ with positive integer weights $A_{uv} = A_{vu}$, no self-loops, $k_u = \sum_v A_{uv}$ and $W = \frac12 \sum_u k_u > 0$. For a partition $\mathcal{M}$ of $V$, let $\mathrm{cut}(i)$ be the weight of the edges with exactly one end in the module $i$, $\mathrm{tot}(i) = \sum_{u \in i} k_u$, and $f(a) = a \log_2 a$ with $f(0) = 0$.

**Lemma 1 (the exact form).** With $p_u = k_u/2W$, $q_i = \mathrm{cut}(i)/2W$, $p_i = \mathrm{tot}(i)/2W$ and $q = \sum_i q_i$,
$$2W \, L(\mathcal{M}) = f\Bigl(\sum_i \mathrm{cut}(i)\Bigr) - 2 \sum_i f(\mathrm{cut}(i)) - \sum_u f(k_u) + \sum_i f(\mathrm{cut}(i) + \mathrm{tot}(i)).$$

*Proof.* First, $q_i$ is the exit rate: the walker is at $u$ with probability $k_u/2W$ and takes the edge to $v$ with probability $A_{uv}/k_u$, so the rate of the steps from $u \in i$ to $v \notin i$ is $A_{uv}/2W$, and summing over these pairs gives $\mathrm{cut}(i)/2W$. Now, for an integer $a \ge 0$, $\mathrm{plogp}(a/2W) = (f(a) - a \log_2 2W)/2W$. Applying this to every term of the expanded map equation, the coefficients of $\log_2 2W / 2W$ are $-C$ for $\mathrm{plogp}(q)$, $+2C$ for $-2\sum_i \mathrm{plogp}(q_i)$, $+2W$ for $-\sum_u \mathrm{plogp}(p_u)$ and $-(C + 2W)$ for $\sum_i \mathrm{plogp}(q_i + p_i)$, where $C = \sum_i \mathrm{cut}(i)$ and $\sum_i \mathrm{tot}(i) = 2W$. They add up to 0. $\square$

So $L$ depends on $\mathcal{M}$ only through the pairs $(\mathrm{cut}(i), \mathrm{tot}(i))$, and $2^{2W L}$ is a ratio of products of integers $a^a$; comparing two values of $L$ exactly is comparing two such fractions, which is what the code does.

**Lemma 2 (aggregation keeps L).** Let $H$ be a graph built by the algorithm, whose vertex $x$ stands for a set $S_x \subseteq V$, with self-loop weight $s_x = \mathrm{in}_G(S_x)$ and edge weights $B_{xy} = \sum_{u \in S_x, v \in S_y} A_{uv}$. Let $k_x = 2 s_x + \sum_{y \ne x} B_{xy}$. For a set $X$ of vertices of $H$, let $\mathrm{cut}_H(X) = \sum_{x \in X, y \notin X} B_{xy}$ and $\mathrm{tot}_H(X) = \sum_{x \in X} k_x$. Then, with $S_X = \bigcup_{x \in X} S_x$, $\mathrm{cut}_H(X) = \mathrm{cut}_G(S_X)$ and $\mathrm{tot}_H(X) = \mathrm{tot}_G(S_X)$.

*Proof.* By induction over the levels, $k_x = \mathrm{tot}_G(S_x)$: the edges of $G$ inside $S_x$ are counted twice in $2 s_x$, and those leaving $S_x$ once in $\sum_y B_{xy}$, which is how they are counted in $\mathrm{tot}_G(S_x)$. Summing over $X$ gives the second claim. For the first, $\sum_{x \in X, y \notin X} B_{xy}$ is the weight of the edges of $G$ from $S_X$ to the sets of the other vertices of $H$, which cover $V \setminus S_X$. $\square$

By Lemma 1 and Lemma 2, define $L_H$ of a partition of the vertices of $H$ by the exact form with $\mathrm{cut}_H$, $\mathrm{tot}_H$ and the constant $\sum_u f(k_u)$ of $G$; it equals $L$ of the matching partition of $V$. This is the quantity that line L8 compares, with the cut of a vertex $x$ alone being $k_x - 2s_x$.

**Lemma 3 (each move lowers L).** If lines L7 to L9 take $v$ from $old$ to $M \ne old$, then $L$ of the partition of $V$ after the step is smaller than before it.

*Proof.* After line L7, every placement of $v$ is a partition of the vertices of $H$, and line L8 compares their $L_H$. It leaves $old$ only for a module with strictly smaller $L_H$, since it keeps $old$ on ties. By Lemma 2, $L_H$ is $L$ of the matching partition of $V$. $\square$

**Lemma 4 (termination).** The run makes finitely many moves and has at most $n$ levels.

*Proof.* By Lemma 3, every move strictly lowers $L$ of the current partition of $V$, and line L13 does not change it (Lemma 2). So no partition of $V$ appears twice after a move, and there are finitely many partitions of $V$. A sweep without a move ends a level. A level that reaches line L12 made a move; its partition of $H$ has smaller $L_H$ than the singletons of $H$ by Lemma 3, so it is not the partition into singletons, and the next $H$ has fewer vertices. $\square$

**Theorem.** INFOMAP($G$) stops and returns a partition $P$ of $V$ such that $L(P) \le L$ of every partition reached before, including the singletons of $V$, and such that no part of $P$, moved as a whole into another part of $P$ that it has an edge to, lowers $L$.

*Proof.* Termination is Lemma 4, and the first claim follows from Lemma 3 and Lemma 2. The algorithm returns at line L11 after a level in which nothing moved. In its last sweep, line L8 kept every vertex $x$ of $H$ in its own singleton module, so no module of a neighbour of $x$ gave a smaller $L_H$. The vertices of $H$ are the parts of $P$, a neighbour of $x$ in $H$ is a part with an edge to $S_x$, and by Lemma 2 the values compared are the values of $L$ on $V$. $\square$

∎
