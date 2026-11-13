---
title: Owen's decomposition splits a Laman graph down to triangles, for any choice of separation pairs, exactly when the graph is triangle-decomposable, and the solve gives every nondegenerate solution
proves: [correctness, split lemma, separation pair existence, running time]
status: full
---

A *part* is a graph $H = (P, F)$ whose edges may include virtual edges; a virtual edge is an ordinary edge for all counts. For $X \subseteq P$ let $F(X)$ be the set of edges with both ends in $X$ and $i(X) = |F(X)|$. $H$ is *sparse* if $i(X) \le 2|X| - 3$ for all $X$ with $|X| \ge 2$, and *Laman* if it is sparse and $|F| = 2|P| - 3$. A set $X$ with $|X| \ge 2$ is *rigid* in $H$ if $i(X) = 2|X| - 3$. $H$ is *triangle-decomposable* (TD) if the [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) on $H$ ends with the single cluster $P$; by the confluence theorem of that reduction, this does not depend on the order of the merges. Line numbers refer to the pseudocode on the main page. Three facts are used often.

- **(F1)** A Laman graph with at least 3 points is 2-connected. If $v$ were a cut vertex, with $P = P' \cup P''$, $P' \cap P'' = \{v\}$ and no edge between $P' - v$ and $P'' - v$, then $|F| \le (2|P'| - 3) + (2|P''| - 3) = 2|P| - 4$.
- **(F2)** In a sparse graph, if $X$ and $Y$ are rigid and $|X \cap Y| \ge 2$, then $X \cap Y$ is rigid. Each edge inside $X$ or inside $Y$ lies inside $X \cup Y$, and each edge inside both lies inside $X \cap Y$, so $i(X \cup Y) + i(X \cap Y) \ge i(X) + i(Y) = 2|X \cup Y| - 3 + 2|X \cap Y| - 3$. Both terms on the left are at most their bounds, so both are equal to them.
- **(F3)** In a run of the reduction on a sparse graph, every cluster $C$ is rigid, its edge set is $F(C)$, and two clusters share at most one point (Lemma 1 of the reduction's proof).

**Lemma 1 (one merge at the top).** Let $H = (P, F)$ be Laman with $|P| \ge 3$. Then $H$ is TD if and only if $P = A \cup B \cup C$, where $A \cap B = \{p\}$, $A \cap C = \{q\}$, $B \cap C = \{r\}$ with $p, q, r$ distinct, the sets $F(A)$, $F(B)$, $F(C)$ partition $F$, and each of $(A, F(A))$, $(B, F(B))$, $(C, F(C))$ is a single edge or TD.

*Proof.* If $H$ is TD, take the last merge of a run; by (F3) its three clusters have these properties. Conversely, the merges that reduce $(A, F(A))$ to one cluster are merges of $H$, since validity depends only on the three clusters involved. Do them, then those of $B$ and $C$. The edge sets partition $F$, so the clusters $A$, $B$, $C$ are the whole state, and they form a valid triple. Merging them gives $P$, and by confluence every run ends there. $\square$

Now fix a Laman part $H = (P, F)$ with $|P| \ge 4$ and a separation pair $\{a, b\}$, and let $P_1$, $P_2$, $F_1$, $F_2$ be the sets of lines L5 to L7, after the swap of line L6. Write $H_1 = (P_1, F_1)$ and $H_2 = (P_2, F_2 \cup \{ab\})$, and let $Q_i = P_i \setminus \{a, b\}$. The graph on $P \setminus \{a, b\}$ has no edge between $Q_1$ and $Q_2$, and both are nonempty.

**Lemma 2 (the split keeps Laman graphs).** $H_1$ and $H_2$ are Laman, $3 \le |P_i| < |P|$, and $F_1 = F(P_1)$, the set of all edges of $H$ inside $P_1$. In particular, line L1 never fails on a part of a Laman graph.

*Proof.* $|P_i| = |Q_i| + 2$ with $1 \le |Q_i| \le |P| - 3$. Before the swap, line L6 puts in the first side all edges inside $P_1$, the edge $ab$ included if $ab \in F$, and in the second side all other edges, which lie inside $P_2$. Let $\delta_i = 2|P_i| - 3 - |F_i|$. Sparsity of $H$ gives $\delta_1 \ge 0$ and $\delta_2 \ge 0$, and if $ab \in F$, then $|F_2| + 1 = i(P_2) \le 2|P_2| - 3$, so $\delta_2 \ge 1$. Since $|P_1| + |P_2| = |P| + 2$,
$$ \delta_1 + \delta_2 = 2|P_1| + 2|P_2| - 6 - (2|P| - 3) = 1. $$
So exactly one side has $\delta = 0$. If $ab \in F$, it is the first side, and there is no swap. If $ab \notin F$, line L6 swaps the sides when $\delta_1 = 1$; in both cases $F_1 = F(P_1)$. So after line L6, $|F_1| = 2|P_1| - 3$, and $H_1$ is sparse as a subgraph of $H$, so it is Laman. Line L7 gives $H_2$ the count $2|P_2| - 3$. For sparsity, let $X \subseteq P_2$ with $|X| \ge 2$. If $X$ does not hold both $a$ and $b$, its edges in $H_2$ are edges of $H$, and $i(X) \le 2|X| - 3$. If it does, suppose $|F_2(X)| \ge 2|X| - 3$. The edges of $F_1$ and of $F_2(X)$ are distinct edges of $H$ inside $X \cup P_1$, and $|X \cap P_1| = 2$, so
$$ i(X \cup P_1) \ge 2|P_1| - 3 + 2|X| - 3 = 2|X \cup P_1| - 2, $$
which contradicts sparsity of $H$. So $|F_2(X)| \le 2|X| - 4$, and with $ab$ the set $X$ has at most $2|X| - 3$ edges. $\square$

For $Y \subseteq P_i$, let $F'_i(Y)$ be the set of edges of $H_i$ inside $Y$ and $i'_i(Y) = |F'_i(Y)|$. Write $H_i[Y] = (Y, F'_i(Y))$.

**Lemma 3 (clusters meet the sides in rigid sets).** Let $X$ be a cluster of a run of the reduction on $H$, and let $X_i = X \cap P_i$ with $|X_i| \ge 2$. Then $i'_i(X_i) = 2|X_i| - 3$. Also, if $X$ meets both $Q_1$ and $Q_2$, then $a, b \in X$.

*Proof.* For the last claim: an edge cluster cannot meet both, since no edge joins $Q_1$ to $Q_2$. A larger cluster is rigid by (F3), so $H[X]$ is Laman with at least 3 points and 2-connected by (F1). Every path from $Q_1$ to $Q_2$ in it passes through $a$ or $b$. If $X$ missed one of them, the other would be a cut vertex of $H[X]$, or $H[X]$ would not be connected.

Side 1: $P_1$ and $X$ are rigid in $H$ by Lemma 2 and (F3), so $X_1$ is rigid by (F2), and its edges in $H$ are those of $H_1$ because $F_1 = F(P_1)$.

Side 2, in three cases. If $X \cap Q_1 = \emptyset$, then $X = X_2$. Its edges in $H_2$ are its edges in $H$, except that the edge $ab$, if both its ends are in $X$, is counted once in either graph. If $a, b \in X$ and $ab \notin F$, then $i'_2(X) = 2|X| - 2$, which contradicts Lemma 2. Otherwise $i'_2(X) = i(X) = 2|X| - 3$. If $X$ meets $Q_1$ and $Q_2$, then $a, b \in X$, and $X_1 \supseteq \{a, b\}$ is rigid with $|X_1| \ge 3$. Each edge inside $X$ lies inside $X_1$ or is an edge of $F_2$ inside $X_2$, so $|F_2(X_2)| = 2|X| - 3 - (2|X_1| - 3) = 2|X_2| - 4$, using $|X| = |X_1| + |X_2| - 2$. Adding $ab$ gives $2|X_2| - 3$. If $X$ meets $Q_1$ but not $Q_2$, then $X_2 \subseteq \{a, b\}$, so $X_2 = \{a, b\}$ with the one edge $ab$. $\square$

**Lemma 4 (split lemma).** $H$ is TD if and only if $H_1$ and $H_2$ are TD.

*Proof.* ($\Leftarrow$) Since $F_1 = F(P_1)$, the merges that reduce $H_1$ to the cluster $P_1$ are merges of $H$. Now replay a run of $H_2$ that ends in $P_2$, with one change: a cluster $X$ of $H_2$ whose edge set holds $ab$ becomes $X \cup P_1$, with the edges of $F_1$ in place of $ab$. At each step at most one cluster holds $ab$, and it contains $a$ and $b$. Any other cluster $Y \subseteq P_2$ meets $P_1$ only inside $\{a, b\} \subseteq X$, so $Y \cap (X \cup P_1) = Y \cap X$. The pairwise intersections do not change, so every merge stays valid, and the run ends with $P_2 \cup P_1 = P$.

($\Rightarrow$) Take a run on $H$ that ends with $P$. We show by induction over the order of formation: for each cluster $X$ and each side $i$ with $|X_i| \ge 2$, $H_i[X_i]$ is a single edge or TD. For $X = P$ this gives the claim.

An edge cluster $\{u, v\}$ with $\{u, v\} \subseteq P_i$ is an edge of $H_i$: either $uv \in F_i$, or $uv = ab$, which is in $H_2$ by line L7 and in $F_1$ when it is real.

Let $X = A \cup B \cup C$ be a merge with $A \cap B = \{p\}$, $A \cap C = \{q\}$, $B \cap C = \{r\}$, and fix a side $i$ with $|X_i| \ge 2$. By induction, for $Y \in \{A, B, C\}$ with $|Y_i| \ge 2$, $H_i[Y_i]$ is TD or an edge, so $i'_i(Y_i) = 2|Y_i| - 3$; if $|Y_i| \le 1$, then $i'_i(Y_i) = 0$.

(a) The sets $F'_i(A_i)$, $F'_i(B_i)$, $F'_i(C_i)$ are disjoint subsets of $F'_i(X_i)$ that miss at most one edge of it. An edge of $F_i$ inside $X_i$ is an edge of $H$ inside $X$, so by (F3) it is inside exactly one of $A$, $B$, $C$, and so inside one of $A_i$, $B_i$, $C_i$. The only other edge is $ab$ on side 2. Two of $A_2, B_2, C_2$ cannot both contain $a$ and $b$, because the clusters share at most one point. Let $\varepsilon = 1$ if $i = 2$, $a, b \in X_2$ and none of $A_2, B_2, C_2$ contains both; otherwise $\varepsilon = 0$. Then
$$ 2|X_i| - 3 = i'_i(X_i) = i'_i(A_i) + i'_i(B_i) + i'_i(C_i) + \varepsilon, $$
where the first equality is Lemma 3.

(b) If $|A_i| \ge 2$ and $|B_i| \ge 2$, then $p \in P_i$. Otherwise $p$ lies in $Q_j$ for the other side $j$. Then $A$ holds $p \in Q_j$ and two points of $P_i$; either $A$ meets $Q_i$, and Lemma 3 gives $a, b \in A$, or $A_i \subseteq \{a, b\}$ with $|A_i| \ge 2$. Either way $a, b \in A$, and in the same way $a, b \in B$, so $A \cap B \supseteq \{a, b, p\}$, a contradiction. The same holds for the other two pairs.

Let $t$ be the number of $Y \in \{A, B, C\}$ with $|Y_i| \ge 2$.

- $t = 3$. By (b), $A_i \cap B_i = \{p\}$, $A_i \cap C_i = \{q\}$ and $B_i \cap C_i = \{r\}$, so $|X_i| = |A_i| + |B_i| + |C_i| - 3$, and (a) reads $2|X_i| - 3 = 2|X_i| - 3 + \varepsilon$. So $\varepsilon = 0$, the three edge sets partition $F'_i(X_i)$, and Lemma 1 shows that $H_i[X_i]$ is TD. It is Laman: its count is that of Lemma 3, and it is a subgraph of the sparse graph $H_i$.
- $t = 2$, say $|A_i|, |B_i| \ge 2 \ge |C_i| + 1$. By (b), $|A_i \cup B_i| = |A_i| + |B_i| - 1$, and (a) gives $2|X_i| - 3 = 2|A_i \cup B_i| - 4 + \varepsilon$. Since $X_i \supseteq A_i \cup B_i$, this forces $\varepsilon = 1$ and $X_i = A_i \cup B_i$. So $i = 2$, and $a$ and $b$ lie in $A_2 \cup B_2$ with neither set holding both. Neither of them is $p$, since $p$ lies in both sets; so, after renaming, $a \in A_2 \setminus B_2$ and $b \in B_2 \setminus A_2$. Then $A_2$, $B_2$ and the edge $\{a, b\}$ pairwise share $p$, $a$ and $b$, which are distinct, their edge sets partition $F'_2(X_2)$, and Lemma 1 shows that $H_2[X_2]$ is TD. The cases with another pair of clusters are the same.
- $t = 1$, say $|A_i| \ge 2$. (a) gives $2|X_i| - 3 = 2|A_i| - 3 + \varepsilon$, so $\varepsilon = 0$ and $X_i = A_i$, which is TD or an edge by induction.
- $t = 0$. (a) gives $2|X_i| - 3 = \varepsilon \le 1$, so $|X_i| = 2$ and $\varepsilon = 1$: $X_2 = \{a, b\}$, a single edge. $\square$

**Lemma 5 (a separation pair exists).** A TD Laman graph $H = (P, F)$ with $|P| \ge 4$ has a separation pair.

*Proof.* Take the three sets of Lemma 1. Since $|P| = |A| + |B| + |C| - 3 \ge 4$, one of them, say $A$, has at least 3 points. Let $A \cap B = \{p\}$ and $A \cap C = \{q\}$. An edge from $x \in A \setminus \{p, q\}$ to $y \notin A$ would lie inside $B$ or $C$, so $x$ would lie in $A \cap B$ or $A \cap C$, which is false. So no edge leaves $A \setminus \{p, q\}$, which is not empty, in the graph on $P \setminus \{p, q\}$, and this graph also holds $r \notin A$. So $\{p, q\}$ is a separation pair. $\square$

**Theorem 1 (the decomposition).** For a Laman graph $G$ with $n \ge 3$ points, OWEN-DECOMPOSE returns a tree, for every choice of separation pairs in line L3 and of components in line L5, if and only if $G$ is TD. A tree has $n - 2$ leaves.

*Proof.* By induction on the number of points. A Laman graph with 3 points is a triangle, which is TD, and line L2 returns a leaf. Let $|P| \ge 4$. If $H$ is TD, Lemma 5 gives a separation pair, so line L3 finds one; by Lemma 2 both sides are smaller Laman graphs, by Lemma 4 both are TD, and by induction both calls return trees. If $H$ is not TD, either line L4 returns FAIL, or by Lemma 4 one side is not TD, its call returns FAIL by induction, and so does the whole call. Each split turns a part with $2k - 3$ edges into parts with $2k - 2$ edges in total, so the leaves have $2n - 3 + s$ edges for $s$ splits, and $s = L - 1$ for $L$ leaves; then $3L = 2n - 3 + L - 1$ gives $L = n - 2$. $\square$

**Theorem 2 (the solve).** Let $G$ be TD with positive lengths, and let OWEN-SOLVE run on its tree.

1. If no leaf fails in line L8, the output satisfies every constraint.
2. Let $y$ be a solution with $y(a) \ne y(b)$ for every virtual edge $ab$ of the tree. With the sign of each leaf $(u, v, w)$ taken from $\mathrm{ORIENT}(y(u), y(v), y(w))$, 0 counting as $+1$, no leaf fails, and the output is properly congruent to $y$.
3. If the lengths are measured on an integer draft $\hat x$ and no leaf triangle is flat in $\hat x$, the output is properly congruent to $\hat x$. Every solution as in part 2 comes from one of the $2^{n-2}$ sign vectors.

*Proof.* A virtual edge made at a split lies only in the second side, so line L10 sets its length before any part that holds it is solved. By induction over the tree, each part is placed so that its edges hold with these lengths. A leaf holds its three lengths by line L8. At a split, $X_1$ satisfies $F_1$; $X_2$ satisfies $F_2$ and $ab$, with $d(ab) = \lvert X_1(a) - X_1(b) \rvert$ if $ab$ is virtual and the given length, which $X_1$ also satisfies, if it is real. So $\lvert X_2(a) - X_2(b) \rvert = \lvert X_1(a) - X_1(b) \rvert$, the proper motion of line L11 takes $X_2(a)$ and $X_2(b)$ exactly to $X_1(a)$ and $X_1(b)$, and it keeps the distances in $X_2$. The two sides share only $a$ and $b$, so every edge of $F_1 \cup F_2$ holds, which proves part 1.

For part 2, show by induction that each part is placed properly congruent to $y$ on its points. A leaf: the points $y(u)$, $y(v)$, $y(w)$ have the leaf's lengths, which are positive since $y$ keeps the ends of virtual edges apart, so line L8 places $u$ and $v$ by a proper motion of $y$, and of the two points at the right distances from them it takes the one on the side of the sign of $y$; if the triangle is flat, there is only one. A split: $X_1$ is properly congruent to $y$ on $P_1$, so the measured length of a virtual $ab$ is $\lvert y(a) - y(b) \rvert$, the lengths of the second side are those of $y$, and $X_2$ is properly congruent to $y$ on $P_2$ by induction. A proper motion is fixed by the images of two distinct points, so the motion of line L11 is the one that composes the two congruences, and the glued placement is properly congruent to $y$ on $P$.

Part 3 is part 2 with $y = \hat x$, whose virtual edges have positive length since no leaf is flat, and whose signs line L8 computes exactly from the integer coordinates. A tree has $n - 2$ leaves by Theorem 1. $\square$

**Theorem 3 (running time).** With a separation pair search that takes time linear in the size of a part, OWEN-DECOMPOSE and OWEN-SOLVE take $O(n^2)$ time.

*Proof.* By Theorem 1 the tree has $n - 2$ leaves and $n - 3$ splits, and each part has at most $n$ points and $2n - 3$ edges, so the parts have $O(n^2)$ points and edges in total. Lines L1 to L7 take time linear in the size of the part, given a linear-time pair search. Each leaf of OWEN-SOLVE costs $O(1)$, and each glue moves at most $n$ points. $\blacksquare$
