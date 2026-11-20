---
title: The grid search finds every friend pair, so the disjoint sets are the connected components
proves: [correctness]
status: full
---

Let $x_1, \ldots, x_N \in \mathbb{R}^D$ and $b > 0$. The friendship graph $F$ has the vertices $1, \ldots, N$ and an edge $\{i, j\}$ when $i \ne j$ and $|x_i - x_j| \le b$. The output should be the connected components of $F$ (with at least $n_{\min}$ vertices). The cell of a point is $c(x) = (\lfloor x_1 / b \rfloor, \ldots, \lfloor x_D / b \rfloor)$.

**Lemma 1 (friends are in neighboring cells).** If $|x - y| \le b$, then $|c(x)_k - c(y)_k| \le 1$ for each coordinate $k$.

*Proof.* $|x_k - y_k| \le |x - y| \le b$. For reals $s, t$ with $|s - t| \le 1$, $\lfloor s \rfloor - \lfloor t \rfloor < s - (t - 1) \le 2$, and the difference of the floors is an integer, so it is at most 1; by symmetry it is at least $-1$. Apply this with $s = x_k / b$ and $t = y_k / b$. $\square$

**Lemma 2 (the loops union exactly the edges).** Lines L3 to L6 call UNION$(i, j)$ for each edge $\{i, j\}$ of $F$, with $i < j$, and for no other pair.

*Proof.* Line L1 puts each point in the list of its cell. Take an edge with $i < j$. By Lemma 1, $c(x_j) = c(x_i) + o$ for some $o \in \{-1, 0, 1\}^D$, so when the loop of line L3 is at $i$, the loop of line L4 reaches the cell of $j$ and line L5 finds $j$. Then $j > i$ and the distance test of line L6 is true. Conversely, line L6 calls UNION only when the distance is at most $b$ and $j > i$, that is, for an edge. $\square$

**Lemma 3 (disjoint sets).** After a sequence of UNION calls on the edges of a graph $H$, two vertices are in the same set exactly when they are connected in $H$.

*Proof.* Invariant: each set is connected in the graph of the edges seen so far, and the two ends of each edge seen so far are in one set. It holds at the start, when each set is one vertex (line L2) and no edge is seen. UNION$(i, j)$ for an edge merges the set of $i$ and the set of $j$, which are joined by that edge, so the merged set is connected and the new edge has both ends in it; if the two ends were already in one set nothing changes. After all edges, the second part says that each path of $H$ stays in one set, so each connected component lies in one set, and the first part says that no set holds two components. Path halving (line L9) and union by size (line L10) change the shape of the trees, not the sets. $\square$

**Theorem.** The output of line L8 is the set of connected components of $F$ with at least $n_{\min}$ vertices.

*Proof.* By Lemma 2 the unions are exactly the edges of $F$, and by Lemma 3 the sets are the components of $F$. Line L7 groups the vertices by the root of their set, and line L8 keeps the groups that are large enough. $\square$

**Cost.** Let $P$ be the number of pairs $(i, j)$ that line L5 visits, the pairs in neighboring cells. With a hash grid that has $O(1)$ expected time per access, lines L1 to L6 cost $O(3^D N + P)$ expected time, and the disjoint-set operations cost $O((N + P)\, \alpha(N))$, where $\alpha$ is the inverse Ackermann function. Points in a cell of side $b$ are at distance at most $b \sqrt{D}$, so if at most $q$ points lie in any cell, $P \le 3^D q N$. In the worst case all points share one cell and $P = \Theta(N^2)$. $\square$
