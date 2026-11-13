---
title: The pebble game accepts exactly the edges that are independent of the earlier accepted edges, finds the rigid components, and runs in O(nm) time
proves: [correctness, invariant, rigid components, running time]
status: full
---

Let $G = (V, E)$ have $n \ge 2$ vertices and a list of $m$ edges $uv$ with $u \ne v$; repeated edges are allowed. For a set $F$ of edges and $X \subseteq V$, let $i_F(X)$ be the number of edges of $F$ with both ends in $X$. Call $F$ *sparse* if $i_F(X) \le 2|X| - 3$ for every $X$ with $|X| \ge 2$. By [Laman's theorem](/laman-theorem/), the sparse sets are the independent sets of the generic rigidity matroid of the plane, and a vertex set $X$ with $|X| \ge 2$ is *rigid* when $G[X]$ is generically rigid, which means that $E(X)$, the edges of $G$ inside $X$, has rank $2|X| - 3$ in this matroid.

During the game, $B$ is the set of accepted edges and $D$ is its orientation. For $X \subseteq V$ let $\mathrm{peb}(X) = \sum_{x \in X} \mathrm{peb}[x]$, and let $\mathrm{out}(X)$ be the number of arcs of $D$ from $X$ to $V \setminus X$. Call $X$ *closed* if $\mathrm{out}(X) = 0$. Line numbers refer to the pseudocode on the main page.

**Lemma 1 (invariant).** At every step, $\mathrm{peb}[v] \ge 0$ and $\mathrm{peb}[v] + \mathrm{outdeg}_D(v) = 2$ for every vertex $v$. Hence $\mathrm{peb}[v] \le 2$, and for every $X \subseteq V$,
$$ 2|X| = \mathrm{peb}(X) + i_B(X) + \mathrm{out}(X). \qquad (*) $$

*Proof.* Line L1 sets $\mathrm{peb}[v] = 2$ with no arcs. Consider a move in line L11 along the path $x = v_0 \to v_1 \to \cdots \to v_k = w$, $k \ge 1$. After the reversal, $x$ has one out-arc less and one pebble more. Each inner vertex $v_i$ loses the arc $v_i \to v_{i+1}$ and gains the arc $v_i \to v_{i-1}$, and its count stays. The vertex $w$ gains one out-arc and loses one pebble, and $\mathrm{peb}[w] > 0$ before, so it stays at least 0. Line L6 runs only when $\mathrm{peb}[u] + \mathrm{peb}[v] = 4$, so $\mathrm{peb}[u] = 2$; it takes one pebble from $u$ and adds one out-arc at $u$. So the invariant holds. Summing it over $X$ gives $2|X| = \mathrm{peb}(X) + \sum_{x \in X} \mathrm{outdeg}(x)$, and each arc with its tail in $X$ either has its head in $X$, which gives $i_B(X)$, or leaves $X$, which gives $\mathrm{out}(X)$. $\square$

Moves only reverse arcs, so they never change $B$ as a set of edges.

**Lemma 2 (accepted edges are independent).** $B$ is sparse at every step.

*Proof.* At the start $B$ is empty. Moves do not change $B$. When line L6 accepts $uv$, then $\mathrm{peb}[u] + \mathrm{peb}[v] = 4$ just before, so for every $X$ that contains $u$ and $v$, $(*)$ gives $i_B(X) \le 2|X| - \mathrm{peb}(X) \le 2|X| - 4$. After the edge is added, $i_B(X) \le 2|X| - 3$. Sets that do not contain both ends do not change. $\square$

In particular, $|B| = i_B(V) \le 2n - 3$, so $D$ has at most $2n - 3$ arcs.

**Lemma 3 (pebbles of the partner stay).** During the search from $x$ with partner $y$ (line L9), $\mathrm{peb}[y]$ does not change.

*Proof.* The search never takes a pebble from $y$. If the path passes through $y$, then $y$ is an inner vertex, and its count stays, as in Lemma 1. $\square$

So in lines L3 and L4, each successful search adds one pebble to $x$, and the searches for the second end do not lower the count of the first end. Each loop of line L4 ends when $\mathrm{peb}[x] = 2$ or when a search fails.

**Lemma 4 (a failed search gives a closed set).** Suppose that at some state the search from $x$ with partner $y$ fails, and let $R$ be the set of vertices that $x$ reaches in $D$. Then $R$ is closed, every free pebble in $R$ lies on $x$ or $y$, and $y \in R$. This stays true while further searches with the ends $x$ and $y$ are made.

*Proof.* The set reached by a search is closed by definition, and a free pebble on a vertex of $R$ other than $x$ and $y$ would have been found. Now let a later search start at $y$ with partner $x$ (a search from $x$ fails again, since nothing has changed). If $y \in R$, the search stays in the closed set $R$ and finds no pebble, so nothing changes. If $y \notin R$, a path from $y$ that entered $R$ could not leave it again, and it would end at a vertex of $R$ with a free pebble other than $x$ and $y$, which does not exist. So the path avoids $R$, and reversing it changes no arc with an end in $R$. So $R$ keeps its properties. It remains to show $y \in R$. If not, $R$ is closed and $\mathrm{peb}(R) = \mathrm{peb}[x] \le 1$, because the search was made with $\mathrm{peb}[x] < 2$. By $(*)$, $i_B(R) = 2|R| - \mathrm{peb}(R) \ge 2|R| - 1$. For $|R| = 1$ this says $0 \ge 1$, and for $|R| \ge 2$ it contradicts Lemma 2. $\square$

**Lemma 5 (rejected edges are dependent).** If line L7 rejects $uv$, then $B + uv$ is not sparse. More precisely, there is a set $R \ni u, v$ with $i_B(R) = 2|R| - 3$.

*Proof.* Line L5 fails, so after lines L3 and L4 some end $x \in \{u, v\}$ has $\mathrm{peb}[x] < 2$, and its loop ended with a failed search. By Lemma 4 that failure persists to the end of line L4, so the set $R$ that $x$ reaches is closed, contains $u$ and $v$, and has $\mathrm{peb}(R) = \mathrm{peb}[u] + \mathrm{peb}[v] \le 3$. By $(*)$, $i_B(R) = 2|R| - \mathrm{peb}(R) \ge 2|R| - 3$, and by Lemma 2 equality holds. Adding $uv$ gives $2|R| - 2$ edges inside $R$. $\square$

**Theorem 1 (correctness of PEBBLE-GAME).** The game marks an edge independent exactly when it is independent of the edges accepted before it, so the accepted edges are the basis that the [matroid greedy algorithm](/matroid-greedy-algorithm/) picks in the given order. The number of accepted edges is the rank of $E$ in the planar generic rigidity matroid.

*Proof.* By Lemma 2, an accepted edge keeps $B$ sparse. By Lemma 5, a rejected edge would break sparsity. Sparsity is independence in the matroid, so the game is the greedy algorithm. Each rejected edge lies in the span of $B$ at the time it is rejected, and $B$ only grows, so at the end $B$ spans $E$ and is a basis: $|B| = \operatorname{rank}(E)$. $\square$

So $G$ is generically rigid in the plane if and only if $|B| = 2n - 3$, and $G$ is a Laman graph if and only if $m = 2n - 3$ and no edge is rejected.

**Lemma 6 (every edge is spanned).** After the game, every edge $uv$ of $E$ lies in a set $R \ni u, v$ with $i_B(R) = 2|R| - 3$. Hence, at every later state, $\mathrm{peb}[u] + \mathrm{peb}[v] \le 3$.

*Proof.* For an accepted edge take $R = \{u, v\}$, since $i_B(R) \ge 1$ and $i_B(R) \le 1$ by Lemma 2. For a rejected edge take the set of Lemma 5; $B$ only grows after it, and Lemma 2 keeps the equality. Then $(*)$ gives $\mathrm{peb}(R) + \mathrm{out}(R) = 3$ at every state, so $\mathrm{peb}[u] + \mathrm{peb}[v] \le \mathrm{peb}(R) \le 3$. $\square$

**Lemma 7 (three pebbles).** For every edge $uv$ of $E$, line L15 ends with $\mathrm{peb}[u] + \mathrm{peb}[v] = 3$.

*Proof.* The loops stop at a total of 3 or at a failed search. In the second case, Lemma 4 gives a closed set $R \ni u, v$ with $\mathrm{peb}(R) = \mathrm{peb}[u] + \mathrm{peb}[v] \le 2$, so $i_B(R) \ge 2|R| - 2$ by $(*)$, against Lemma 2. $\square$

**Lemma 8 (union of rigid sets).** If $X$ and $Y$ are rigid and $|X \cap Y| \ge 2$, then $X \cup Y$ is rigid. So for each edge $uv$ there is exactly one largest rigid set that contains $u$ and $v$, its *rigid component*, and two rigid components share at most one vertex.

*Proof.* Take a generic placement $p$, so the points are distinct. At $p$, rigid sets give infinitesimally rigid subframeworks (Asimow and Roth). Let $a$ be an infinitesimal motion of $G[X \cup Y]$. It is an infinitesimal motion of $G[X]$ and of $G[Y]$, so on $X$ it is a trivial motion $T_1$ and on $Y$ a trivial motion $T_2$. A trivial motion of the plane has the form $q \mapsto \omega J q + b$ with $J$ the rotation by a right angle. The difference $T_1 - T_2$ vanishes at two distinct points $p_s$ and $p_t$ of $X \cap Y$, so $\omega J (p_s - p_t) = 0$, hence $\omega = 0$ and then $b = 0$. So $a$ is trivial on $X \cup Y$, the subframework is infinitesimally rigid, and $G[X \cup Y]$ is generically rigid. The set $\{u, v\}$ is rigid, because it spans the edge $uv$. So the union of all rigid sets that contain $u$ and $v$ is rigid, and it is the unique largest one. Two different components that share two vertices would have a rigid union larger than both. $\square$

**Lemma 9 (the component is tight in $B$).** Let $C$ be the rigid component of an edge $uv$ of $E$. Then $i_B(C) = 2|C| - 3$.

*Proof.* It suffices to show that $B \cap E(C)$ spans $E(C)$ in the matroid, because then $i_B(C) = \operatorname{rank} E(C) = 2|C| - 3$. Edges of $B$ in $E(C)$ are spanned trivially. Let $e \in E(C)$ be rejected. Then $B + e$ contains a unique circuit $Z$ through $e$, and $Z \setminus e \subseteq B$. The vertex set $W$ of $Z$ is rigid: $Z$ has $2|W| - 2$ edges (shown below), and $Z \setminus e$ is independent, so $E(W)$ has rank at least $2|W| - 3$. The sets $W$ and $C$ share the two ends of $e$, so $W \cup C$ is rigid by Lemma 8, and by maximality $W \subseteq C$. So $Z \setminus e \subseteq B \cap E(C)$, and $e$ is spanned by $B \cap E(C)$. $\square$

The circuit count in this proof is the standard fact for the count matroid: a circuit $Z$ on vertex set $W$ has $|Z| = 2|W| - 2$, because $Z$ is not sparse, so some $X \subseteq W$ has $i_Z(X) \ge 2|X| - 2$, and by minimality $Z$ lies inside $X$, so $X = W$, and $Z \setminus e$ is sparse, so $|Z| - 1 \le 2|W| - 3$.

**Theorem 2 (correctness of RIGID-COMPONENTS).** For each edge $uv$ handled in line L14, the set $S = V \setminus X$ of line L17 is the rigid component $C$ of $uv$. The list $\mathcal{C}$ holds every rigid component exactly once.

*Proof.* By Lemma 7, $\mathrm{peb}[u] + \mathrm{peb}[v] = 3$ after line L15.

*$u, v \in S$.* Suppose $u$ reaches a vertex $w \notin \{u, v\}$ with a free pebble. Then $\mathrm{outdeg}(u) \ge 1$, so $\mathrm{peb}[u] \le 1$ by Lemma 1, and reversing the path gives $u$ one more pebble, so $\mathrm{peb}[u] + \mathrm{peb}[v] = 4$, against Lemma 6. The same holds for $v$.

*$S$ is rigid.* If a vertex $z \in S$ had an arc to a vertex of $X$, then $z$ would reach a free pebble off $\{u, v\}$, so $z \in X$. So $S$ is closed. A vertex $w \in S \setminus \{u, v\}$ with a free pebble would reach itself, so the only free pebbles in $S$ are on $u$ and $v$, and $\mathrm{peb}(S) = 3$. By $(*)$, $i_B(S) = 2|S| - 3$. These edges of $B$ are independent and lie in $E(S)$, so $E(S)$ has rank $2|S| - 3$ and $S$ is rigid. Hence $S \subseteq C$.

*$C \subseteq S$.* By Lemma 9 and $(*)$, $\mathrm{peb}(C) + \mathrm{out}(C) = 3$. Since $u, v \in C$, $\mathrm{peb}(C) \ge 3$, so $\mathrm{out}(C) = 0$ and $C$ has no free pebble except on $u$ and $v$. A vertex of $C$ reaches only vertices of $C$, so it reaches no free pebble off $\{u, v\}$, and $C \cap X = \emptyset$.

So $S = C$. The moves of line L15 do not change $B$, and Lemmas 1 to 9 hold at every state, so later edges are handled correctly too. Every rigid component $C$ has $|C| \ge 2$ and rank $2|C| - 3 \ge 1$, so it contains an edge, and the first such edge reached in line L14 is not yet covered (by Lemma 8 no other component contains both its ends), so $C$ is added. Later edges of $E(C)$ are covered and skipped, so no component is added twice. $\square$

**Theorem 3 (running time).** PEBBLE-GAME takes $O(nm)$ time, the Laman test with early stop takes $O(n^2)$ time, RIGID-COMPONENTS takes $O(nm)$ time, and the space is $\Theta(n + m)$.

*Proof.* $D$ has at most $2n - 3$ arcs (Lemma 2), so one depth-first search and one path reversal take $O(n)$ time. For one edge, each loop of line L4 has at most two successful searches, because each adds one pebble to $x$, Lemma 3 protects that count from the other loop, and $\mathrm{peb}[x] \le 2$. Each loop has at most one failed search. So each edge costs at most six searches, $O(n)$ time, and PEBBLE-GAME takes $O(nm)$. The Laman test first checks $m = 2n - 3$ and stops at the first rejected edge, so it handles at most $2n - 3$ edges, in $O(n^2)$ time.

For the components: each component $C$ has $i_B(C) = 2|C| - 3 \ge 1$ edges of $B$ (Lemma 9), and two components share no edge (Lemma 8), so there are at most $|B| \le \min(m, 2n - 3)$ of them. Each one costs $O(n)$ for line L15 (at most five searches) and $O(n)$ for the backward search of line L16 over the $O(n)$ arcs, so $O(nm)$ for all of them. For line L14, keep for each vertex the list of components that contain it, stored as hash sets; testing an edge looks at the at most $2n - 3$ components of $u$, in $O(n)$ time. So the total is $O(n + nm)$, which is $O(nm)$ when $m \ge 1$. The arrays $\mathrm{peb}$, the adjacency lists of $D$ and the marks take $\Theta(n + m)$ space, and the component lists take $O(n + \sum_C |C|) = O(n)$ more, because $2|C| - 3 \ge |C|/2$ for $|C| \ge 2$ and $\sum_C (2|C| - 3) \le 2n - 3$. $\square$
