---
title: The star form of Shiloach-Vishkin keeps a forest, stops, and labels the components; with full shortcuts it stops within ceil(log2 n) + 1 iterations
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ is an undirected graph with $n$ vertices. Each edge $\{u, v\}$ gives the arcs $(u, v)$ and $(v, u)$. A step reads the state from before the step; when several processors write one cell, one of them wins. In one iteration, $Q$ is the array $P$ at the start, $P_1$ the array after line L5, $P_2$ the array after line L8, and $P_3$ the array after line L9. A pointer array is a forest when following it from any vertex reaches a vertex $r$ with $P[r] = r$, the root. A tree of height at most 1 is a star. A root $r$ is written in a line if its cell gets a new value in that line.

**Lemma 1 (star test).** If $Q$ is a forest, then after line L3, $star[v]$ is true if and only if the tree of $v$ in $Q$ is a star.

*Proof.* A clear made by $w$ goes to $w$ and to $Q[Q[w]]$, both in the tree of $w$. If the tree of $v$ is a star, every vertex $w$ of it has $Q[w] = Q[Q[w]]$, the root, so no vertex of the tree is cleared, and $star[v] \wedge star[Q[v]]$ is true. If the tree has height 2 or more, it has a vertex $w$ at depth exactly 2, whose grandparent is the root $r$; $w$ clears $star[r]$. A vertex at depth 2 or more clears itself, the root is cleared, and a vertex at depth 1 reads the cleared $star[r]$ in the third step. So every vertex of the tree ends with false. $\square$

**Lemma 2 (line L5).** If $Q$ is a forest, then $P_1$ is a forest, and every tree of $P_1$ is a union of trees of $Q$.

*Proof.* A write in line L5 comes from an arc $(u, v)$ with $star[u]$ and $Q[u] > Q[v]$. The tree of $u$ is a star, so $Q[u]$ is its root $r$, and $v$ is in another tree, since in the star of $u$ every vertex has $Q$ equal to $r$. So only roots of stars are written, each with a value $y = Q[v] < r$ that lies in another tree; every written value is smaller than the cell, so a write changes the cell. Follow $P_1$ from any vertex. Inside a tree of $Q$ it reaches the root $\rho$. If $\rho$ is not written, the walk stops. If it is written, it moves to $y = Q[v] < \rho$ in the tree of $v$. If that tree is not a star, its root is not written, and the walk stops there. If it is a star, $y$ is its root, which is smaller than $\rho$. The roots met in a walk strictly decrease, so no walk can cycle, and $P_1$ is a forest. Each write joins two trees of $Q$, so the trees of $P_1$ are unions of trees of $Q$. $\square$

**Lemma 3 (stagnant stars survive line L5).** If $stagnant[v]$ is true, the star $S$ of $v$ in $Q$ is a whole tree of $P_1$, and it is a star.

*Proof.* The root $r$ of $S$ is not written, by the definition in line L6. The other vertices of $S$ are not roots, so they are not written. A vertex $w \notin S$ that is not written has $P_1[w] = Q[w]$ in its own tree of $Q$, not in $S$. A written root $w$ with $P_1[w] \in S$ would set the flag on $Q[P_1[w]] = r$, because $Q$ maps every vertex of the star $S$ to $r$; line L6 says no flag is set on $r$. So no pointer of $P_1$ leaves $S$ or enters $S$, and the pointers inside $S$ are those of $Q$. $\square$

**Lemma 4 (no edge between stagnant stars).** If $stagnant[u]$ and $stagnant[v]$ are true and $Q[u] \ne Q[v]$, then $\{u, v\}$ is not an edge.

*Proof.* Both trees are stars, so $Q[u]$ and $Q[v]$ are their roots, and they differ. Say $Q[u] > Q[v]$. Then the arc $(u, v)$ writes the cell $Q[u]$ in line L5, and one writer wins, so the root of $u$ is written, and $u$ is not stagnant. The other order is the same with the arc $(v, u)$. $\square$

**Lemma 5 (line L8).** If $Q$ is a forest, then $P_2$ is a forest, and every tree of $P_2$ is a union of trees of $P_1$.

*Proof.* A write in line L8 comes from an arc $(u, v)$ with $stagnant[u]$ and $P_1[u] \ne P_1[v]$. By Lemma 3 the tree of $u$ in $P_1$ is its star $S$ with root $r = P_1[u]$, and the write sets $P_2[r] = P_1[v] = y$. Since $P_1[v] \ne r$, $v \notin S$. Let $T$ be the tree of $v$ in $P_1$. If $T$ held a stagnant vertex $w$, then by Lemma 3, $T$ would be the star of $w$ and $v$ would be stagnant, and Lemma 4 forbids the edge $\{u, v\}$ between two stagnant stars. So $T$ holds no stagnant vertex, and no cell of $T$ is written in line L8, because line L8 writes only the roots of stagnant stars. Follow $P_2$ from any vertex: it reaches the root of its tree of $P_1$; if that root is written, it moves once into a tree that line L8 did not change, and reaches its root, which is not written. So $P_2$ is a forest, and each write joins two trees. $\square$

**Lemma 6 (shortcut).** If $P_2$ is a forest, then $P_3$ is a forest with the same trees and the same roots, and a vertex at depth $d$ in $P_2$ has depth $\lceil d/2 \rceil$ in $P_3$.

*Proof.* $P_3[v] = P_2[P_2[v]]$ is the grandparent of $v$, or the root if $v$ has depth 1, or $v$ itself if $v$ is a root. So roots stay roots, every vertex stays in its tree, and the depth $d$ becomes $\lceil d/2 \rceil$ by induction on $d$. $\square$

**Lemma 7 (trees are connected).** At every step, the vertex set of each tree induces a connected subgraph of $G$.

*Proof.* At the start, the trees are single vertices. A write in line L5 or L8 caused by the arc $(u, v)$ joins the tree that holds $u$ to the tree that holds $v$, and $\{u, v\}$ is an edge. A new tree is a set of old trees joined by such edges, so it is connected if the old trees are. Line L9 does not change the trees. $\square$

**Theorem 1 (correctness and termination).** The algorithm stops, and at the end $P[u] = P[v]$ if and only if $u$ and $v$ are in the same connected component of $G$.

*Proof.* By Lemmas 2, 5 and 6 and induction on the iterations, $P$ is a forest at every step. Writes go only to roots and always change the cell, and no step makes a new root. If line L5 or L8 writes in an iteration, the number of trees falls, and $P_3 \ne Q$, because a written root $r$ of $Q$ is not a root of $P_3$, so $P_3[r] \ne r = Q[r]$. If neither line writes, then $P_3$ is the shortcut of $Q$, and $P_3 \ne Q$ exactly when some tree has a vertex at depth 2 or more; then the sum of the depths falls and the number of trees stays. So each iteration that does not stop lowers the pair (number of trees, sum of depths) in lexicographic order. The pair takes finitely many values, so the loop stops.

When it stops, $P_3 = Q$. Then lines L5 and L8 wrote nothing, and $Q[Q[v]] = Q[v]$ for all $v$, so every tree is a star and, by Lemma 1, $star$ is true everywhere. If an arc $(u, v)$ had $Q[u] \ne Q[v]$, then one of the arcs $(u, v)$ and $(v, u)$ would satisfy the test of line L5 and write. So every edge has both ends in one tree, every component lies inside one tree, and by Lemma 7 every tree lies inside one component. The trees are the components, and in a star $P[v]$ is the root of the tree of $v$. $\blacksquare$

**Theorem 2 (full shortcuts).** If line L9 repeats the shortcut until every tree is a star, the algorithm stops after at most $\lceil \log_2 n \rceil + 1$ iterations for $n \ge 1$, and each iteration takes $O(\log n)$ steps.

*Proof.* Every iteration then starts with all trees stars: the first because the trees are single vertices, the others because of the repeated shortcut. Take an iteration and a tree $T$ of $Q$ that is not a whole component. Some arc $(u, v)$ has $u \in T$ and $v \notin T$. One of three things happens. The root of $T$ is written in line L5, and $T$ joins another tree. Or some root written in line L5 now points into $T$, and another tree joins $T$. Or neither, and then $T$ is stagnant, since it is a star. In the last case, by Lemma 3, $T$ is a whole tree of $P_1$ with root $r = P_1[u]$, and $v$ is in another tree of $P_1$, so $P_1[v] \ne r$ and the arc $(u, v)$ writes $r$ in line L8. In all three cases $T$ ends in a tree of $P_3$ that holds at least one other tree of $Q$. So if a component holds $k \ge 2$ trees of $Q$, it holds at most $\lfloor k/2 \rfloor$ trees after the iteration, because each new tree is a union of at least two old ones.

A component $C$ starts with $|C| \le n$ trees, so after $t$ iterations it holds at most $\max(1, \lfloor n / 2^t \rfloor)$ trees. After $t = \lceil \log_2 n \rceil$ iterations, $n / 2^t \le 1$, so every component is one tree, and that tree is a star. In iteration $t + 1$, no arc joins two trees, so lines L5 and L8 write nothing, the shortcut changes nothing, and the loop stops. The repeated shortcut halves the height of every tree in each step by Lemma 6, and heights are less than $n$, so it ends after at most $\lceil \log_2 n \rceil + 1$ steps; the other lines take $O(1)$ steps. $\blacksquare$
