---
title: On a Laman-sparse graph the Fudos-Hoffmann reduction finds a merge whenever one exists, its final clusters do not depend on the order, and the construction gives every solution up to proper motion
proves: [correctness, invariant, confluence, running time]
status: full
---

Let $G = (V, E)$ be a graph with $n$ vertices and $m$ edges, and for $X \subseteq V$ let $i(X)$ be the number of edges with both ends in $X$. Call $G$ *sparse* if $i(X) \le 2|X| - 3$ for every $X$ with $|X| \ge 2$. A state of the reduction is a family $S$ of clusters; each cluster $C$ is a vertex set together with the set $E_C$ of the edges that were merged into it. Three clusters $A, B, C$ form a *valid triple* if $A \cap B = \{p\}$, $A \cap C = \{q\}$, $B \cap C = \{r\}$ with $p, q, r$ distinct. A state is *terminal* if it has no valid triple. Line numbers refer to the pseudocode on the main page.

**Lemma 1 (cluster invariant).** Let $G$ be sparse. At every step, the sets $E_C$ partition $E$, every cluster has $|E_C| = 2|C| - 3$ and $E_C = E(C)$, the set of edges inside $C$, and two clusters share at most one vertex. Lines L6 and L7 never fail.

*Proof.* First, two clusters $X \ne Y$ with $|E_X| = 2|X| - 3$, $|E_Y| = 2|Y| - 3$ and disjoint edge sets share at most one vertex. If $|X \cap Y| \ge 2$, then
$$ i(X \cup Y) \ge |E_X| + |E_Y| = 2|X| + 2|Y| - 6 = 2|X \cup Y| + 2|X \cap Y| - 6 \ge 2|X \cup Y| - 2, $$
which contradicts sparsity. Second, $E_C \subseteq E(C)$ and $|E_C| = 2|C| - 3 \ge i(C)$ give $E_C = E(C)$.

Line L1 makes one cluster per edge, with $|E_C| = 1 = 2 \cdot 2 - 3$, and the edge sets partition $E$. Consider a merge of a valid triple. No vertex lies in all three clusters, since such a vertex would equal $p$, $q$ and $r$. So $|A \cup B \cup C| = |A| + |B| + |C| - 3$, and the new cluster $N$ gets the edge set $E_A \cup E_B \cup E_C$, of size $2(|A| + |B| + |C|) - 9 = 2|N| - 3$. The partition of $E$ stays, and the first claim gives the bound on shared vertices for the new state.

Line L6 fails only if $A$ and $B$ share two vertices. Line L7 fails only if $B$ and $C$ share $s(B) = s(C)$ and the vertex $x \ne s(B)$, again two vertices. By the first claim, neither happens. $\square$

So a failure in line L6 or L7 proves that $G$ is not sparse. From now on $G$ is sparse.

**Lemma 2 (line L7 finds a merge exactly when one exists).** Let $A$ be a current cluster. Lines L5 to L8 find a valid triple that contains $A$ if one exists, and every triple that they return is valid.

*Proof.* If $A, B, C$ is a valid triple, then $B$ and $C$ meet $A$, and they share $r$, which is not in $A$, since $r \in A$ would put $r$ in all three clusters. So the search of line L7 finds some pair. Conversely, let line L7 return $B$ and $C$ that meet $A$ in the single points $s(B) \ne s(C)$ and share $x \notin A$. By Lemma 1, $B \cap C = \{x\}$, and $x$ differs from $s(B)$ and $s(C)$, since these lie in $A$. So the triple is valid. $\square$

**Lemma 3 (no merge is missed).** At every step, every valid triple of the current state has a member that is on the stack $W$.

*Proof.* At the start every cluster is on $W$. A pop of a cluster that is no longer current changes nothing. Let line L4 pop a current cluster $A$. If line L8 continues, then by Lemma 2 no valid triple contains $A$, and every other valid triple keeps its member on $W$, which is not $A$. If lines L9 and L10 merge $A, B, C$ into $N$ and push $N$, then a valid triple of the new state either contains $N$, which is on $W$, or consists of three clusters other than $A$, $B$ and $C$. Those three clusters did not change, so they formed a valid triple before the merge, with a member on $W$, and that member is still on $W$. $\square$

**Theorem 1 (termination and terminal state).** The reduction stops after at most $m + \lfloor (m - 1)/2 \rfloor$ pops, and its final state is terminal.

*Proof.* Each merge lowers the number of clusters by 2, from $m$ at the start, so there are at most $\lfloor (m - 1)/2 \rfloor$ merges and as many pushes after line L2. Each pop removes one entry of $W$. When $W$ is empty, Lemma 3 says that no valid triple exists. $\square$

**Theorem 2 (confluence).** Let $T$ be any terminal state reached from $G$, and consider any run of the reduction, with any order of the stack. Every cluster formed in that run lies inside a cluster of $T$. Consequently all runs end with the same family of clusters.

*Proof.* By induction over the order of formation. An edge cluster $\{u, v\}$: the edge $uv$ lies in $E_C$ for some cluster $C$ of $T$ (Lemma 1), and $E_C = E(C)$, so $u, v \in C$. A merge $N = A \cup B \cup C$ of a valid triple with $A \cap B = \{p\}$, $A \cap C = \{q\}$, $B \cap C = \{r\}$: by induction $A \subseteq T_a$, $B \subseteq T_b$ and $C \subseteq T_c$ for clusters of $T$. Then $p \in T_a \cap T_b$, $q \in T_a \cap T_c$ and $r \in T_b \cap T_c$.

- If $T_a$, $T_b$ and $T_c$ are pairwise different, then by Lemma 1 their pairwise intersections are exactly $\{p\}$, $\{q\}$ and $\{r\}$, which are distinct. They form a valid triple of $T$, which contradicts that $T$ is terminal.
- If exactly two are equal, say $T_a = T_b \ne T_c$, then $T_a$ contains $q \in A$ and $r \in B$, and $T_c$ contains both as well. So $T_a$ and $T_c$ share the two vertices $q \ne r$, which contradicts Lemma 1. The cases $T_a = T_c \ne T_b$ (shared $p, r$) and $T_b = T_c \ne T_a$ (shared $p, q$) are the same.

So $T_a = T_b = T_c$, and $N$ lies inside it.

Now let $T$ and $T'$ be two final states. Each is terminal by Theorem 1. A cluster $X$ of $T'$ lies in a cluster $Y$ of $T$, and $Y$ lies in a cluster $X'$ of $T'$. If $X' \ne X$, then $X \subseteq X'$ shares $|X| \ge 2$ vertices with $X'$, which contradicts Lemma 1. So $X = Y = X'$, every cluster of $T'$ is a cluster of $T$, and by symmetry $T = T'$. $\square$

In particular, whether the final state is $\{V\}$, that is, whether $G$ is triangle-decomposable, does not depend on the order. If it is, then the number of merges is $(m - 1)/2$, and since $|E_V| = 2n - 3$, this is $n - 2$.

For the construction, let $d(uv) > 0$ be the lengths, and say that a placement $x$ of a cluster $C$ *satisfies* $C$ if $\lvert x(u) - x(v) \rvert = d(uv)$ for all $uv \in E_C$. Two placements of a set $C$ are *properly congruent* if a rotation followed by a translation takes one to the other.

**Lemma 4 (each step keeps the constraints).** If no merge fails in line L17, then after each merge the coordinates of $N$ satisfy $N$.

*Proof.* Line L13 places each edge cluster at the distance $d(uv)$. In a merge, by induction $A$, $B$ and $C$ are satisfied in their own frames. Line L17 gives a point $R$ with $\lvert p_A R \rvert = \lvert p_B r_B \rvert$ and $\lvert q_A R \rvert = \lvert q_C r_C \rvert$, where the subscript names the frame. Since these lengths are equal, the proper motion of line L18 takes $p_B$ to $p_A$ and $r_B$ exactly to $R$, and it keeps all distances inside $B$. The same holds for $C$ in line L19, with $q_C \mapsto q_A$ and $r_C \mapsto R$. The vertices that lie in two of the clusters are $p$, $q$ and $r$, and they get the same coordinates from both clusters. Every edge of $E_N = E_A \cup E_B \cup E_C$ lies inside one of the three clusters and holds there. $\square$

**Lemma 5 (the signs of a solution reproduce it).** Let $G$ be triangle-decomposable, and let $y : V \to \mathbb{R}^2$ be any placement with $\lvert y(u) - y(v) \rvert = d(uv)$ for every edge and $y(p) \ne y(q)$ for the points $p, q$ of every merge. Run lines L14 to L20 with the sign of merge $i$ equal to the sign of $\mathrm{ORIENT}(y(p), y(q), y(r))$ for that merge, with 0 counted as $+1$. Then no merge fails, and after each merge the placement of $N$ is properly congruent to $y$ restricted to $N$.

*Proof.* By induction. Any two placements of an edge cluster at the same distance are properly congruent. In a merge, let $g$ be the proper motion with $x_A = g \circ y$ on $A$. The point $g(y(r))$ has distance $\lvert y(p) y(r) \rvert$ from $x_A(p) = g(y(p))$ and $\lvert y(q) y(r) \rvert$ from $g(y(q))$, and these are the lengths that $B$ and $C$ measure, because $B$ and $C$ are properly congruent to $y$. So the circles of line L17 meet, and their centers differ because $y(p) \ne y(q)$. If the triangle $y(p), y(q), y(r)$ is not flat, the two meeting points are mirror images in the line $pq$, and the one on the side of the sign is $g(y(r))$, because $g$ keeps orientations. If it is flat, the circles touch in one point, which is $g(y(r))$. So $R = g(y(r))$. A proper motion is fixed by the images of two distinct points, so the motion of line L18 is $g \circ h^{-1}$, where $x_B = h \circ y$ on $B$, and it moves $B$ to $g \circ y$. The same holds for $C$, and so $x_N = g \circ y$ on $N$. $\square$

**Theorem 3 (the construction).** Let $G$ be triangle-decomposable.

1. Every placement that FH-SOLVE returns satisfies all constraints.
2. If the lengths are measured on an integer draft $\hat x$ and no merge triangle is flat in $\hat x$, FH-SOLVE returns a placement properly congruent to $\hat x$.
3. Every real solution $y$ with $y(p) \ne y(q)$ for the points $p, q$ of every merge is properly congruent to the output for one of the $2^{n-2}$ sign vectors. So the system has at most $2^{n-2}$ such solutions up to proper motion.

*Proof.* Part 1 is Lemma 4 for the cluster $V$. Part 2 is Lemma 5 with $y = \hat x$: no merge triangle is flat in $\hat x$, so $\hat x(p) \ne \hat x(q)$, and line L16 computes the sign of $\mathrm{ORIENT}$ exactly from the integer coordinates, so the signs are those of Lemma 5. Part 3 is Lemma 5 for the solution $y$, with $n - 2$ merges. $\square$

A solution with $y(p) = y(q)$ for some merge is degenerate: the circles of line L17 are then concentric, and the implementation stops with an error instead of choosing a point on a circle.

**Theorem 4 (running time).** FH-REDUCE runs in $O(m(n + m))$ time and FH-SOLVE in $O(m(n + m) + n^2)$ time, so both run in $O(n^2)$ time for a sparse graph.

*Proof.* By Lemma 1 the clusters are edge-disjoint, and a cluster with $k \ge 2$ points has $2k - 3 \ge k/2$ edges, so the sizes of all current clusters add up to at most $2m$. One pop of line L4 scans the clusters that meet $A$ and their vertices, with a table from vertices to clusters, in $O(n + m)$ time, and by Theorem 1 there are $O(m)$ pops. In FH-SOLVE, each of the $n - 2$ merges moves at most $n$ points in lines L18 and L19 and does $O(1)$ other work. Sparsity gives $m \le 2n - 3$. $\blacksquare$
