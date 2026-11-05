---
title: Reverse-delete returns a minimum spanning forest
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite undirected graph with a real weight $w(e)$ on each edge. Weights may tie and may be negative, $G$ may have parallel edges and self-loops, and $G$ need not be connected. Then REVERSE-DELETE$(G, w)$ stops, and the set $F$ that it returns is a minimum spanning forest of $G$: a forest with the same connected components as $G$, of least total weight among all such forests.

**Setup.** Let $e_1, e_2, \ldots, e_m$ be the edges in the order of line L2, so $w(e_1) \ge w(e_2) \ge \cdots \ge w(e_m)$. Let $F_k$ be the set $F$ after $e_k$ is processed, with $F_0 = E$. An edge $e \in F$ is a *bridge* of $(V, F)$ if its two ends are not connected in $(V, F \setminus \{e\})$. A self-loop is never a bridge. An edge lies on a cycle of $(V, F)$ if and only if it is not a bridge: if its ends $u \ne v$ are connected without it, a simple path from $u$ to $v$ and the edge form a cycle, and a self-loop is a cycle by itself; conversely, the rest of a cycle through $e$ connects its ends. Each spanning forest of $G$ has $n - c$ edges, where $c$ is the number of components of $G$ ([spanning forest](/spanning-forest/)).

**Lemma 1 (bridges stay bridges).** If $e$ is a bridge of $(V, F)$ and $F' \subseteq F$ with $e \in F'$, then $e$ is a bridge of $(V, F')$.

*Proof.* A path in $(V, F' \setminus \{e\})$ is also a path in $(V, F \setminus \{e\})$. So if the ends of $e$ are not connected in the second graph, they are not connected in the first. $\square$

**Invariant.** For each $k$ from $0$ to $m$:

- **(C)** $(V, F_k)$ has the same connected components as $G$.
- **(K)** Each edge $e_j$ with $j \le k$ and $e_j \in F_k$ is a bridge of $(V, F_k)$.
- **(M)** There is a minimum spanning forest $F^*_k$ of $G$ with $F^*_k \subseteq F_k$.

*Initialization.* $F_0 = E$, so (C) holds, (K) is empty, and any minimum spanning forest is a subset of $E$, so (M) holds.

*Maintenance, $e_k$ kept.* Then $F_k = F_{k-1}$, and (C) and (M) carry over. The test of line L4 failed, so $e_k$ is a bridge of $(V, F_k)$. The edges $e_j$ with $j < k$ in $F_k$ were bridges of $(V, F_{k-1}) = (V, F_k)$ by (K). So (K) holds.

*Maintenance, $e_k = uv$ deleted.* Then $u$ and $v$ are connected in $(V, F_{k-1} \setminus \{e_k\})$.

1. (C): any path of $(V, F_{k-1})$ that uses $e_k$ can replace it by a path from $u$ to $v$ in $(V, F_k)$. So connectivity does not change.
2. (K): each $e_j$ with $j < k$ in $F_k$ was a bridge of $(V, F_{k-1})$ by (K), and it is a bridge of $(V, F_k)$ by Lemma 1.
3. (M): if $e_k \notin F^*_{k-1}$, then $F^*_{k-1} \subseteq F_k$ and we take $F^*_k = F^*_{k-1}$. So assume $e_k \in F^*_{k-1}$. A self-loop is in no forest, so $u \ne v$. Let $P$ be a simple path from $u$ to $v$ in $(V, F_k)$. Then $C = P \cup \{e_k\}$ is a cycle in $(V, F_{k-1})$.

   Each edge $f \in P$ is $e_j$ for some $j$. If $j < k$, then by (K) $f$ is a bridge of $(V, F_{k-1})$, but $f$ lies on the cycle $C$ of $(V, F_{k-1})$, so it is not a bridge. Hence $j > k$, and $w(f) \le w(e_k)$ by the order of the sort.

   Removing $e_k$ from $F^*_{k-1}$ splits its tree that holds $u$ and $v$ into a part $X \ni u$ and a part $Y \ni v$. The path $P$ starts in $X$ and ends in $Y$, so it has an edge $g$ with one end in $X$ and the other in $Y$. Then $g \notin F^*_{k-1}$, since the only edge of $F^*_{k-1}$ between $X$ and $Y$ is $e_k$, and $g \ne e_k$. Let $F^*_k = F^*_{k-1} \setminus \{e_k\} \cup \{g\}$. Adding $g$ joins $X$ and $Y$ again, so $F^*_k$ is a forest with the components of $F^*_{k-1}$, which are those of $G$. Its weight is $w(F^*_{k-1}) - w(e_k) + w(g) \le w(F^*_{k-1})$, since $g \in P$. So $F^*_k$ is a minimum spanning forest, and $F^*_k \subseteq F_k$, because $F^*_{k-1} \setminus \{e_k\} \subseteq F_k$ and $g \in P \subseteq F_k$.

**Termination.** The loop of line L3 runs once for each of the $m$ edges, and each test of line L4 is a graph search on a finite graph, which stops. So the algorithm stops after $m$ steps.

**Conclusion.** Let $F = F_m$. By (K) with $k = m$, every edge of $F$ is a bridge of $(V, F)$, so no edge of $F$ lies on a cycle, and $F$ is a forest. By (C), its components are those of $G$, so $F$ is a spanning forest with $n - c$ edges. By (M), $F$ contains a minimum spanning forest $F^*_m$, which also has $n - c$ edges, so $F = F^*_m$. Therefore $F$ is a minimum spanning forest, and a minimum spanning tree when $G$ is connected. $\blacksquare$
