---
title: Parallel Borůvka returns the minimum spanning forest within ceil(log2 n) rounds
proves: [correctness, termination, complexity]
status: full
---

**Setting.** Edge $i$ of $G$ has the key $(w_i, i)$; keys are compared in lexicographic order, so all keys differ. $M$ is the minimum spanning forest for these keys. It is unique, and it satisfies the cut property: for every set $S$ of vertices, the edge of least key among the edges with exactly one end in $S$, if there is one, is in $M$. The proof uses the cut property and does not prove it. In a round, $V$ and $E$ denote the sets at the start of the round, and each edge of $E$ keeps the key and the index of the edge of $G$ it came from.

**Invariant.** At the start of each round: (a) $F \subseteq M$; (b) every vertex of $G$ has a supervertex, the supervertices are the vertex sets of the components of the graph $(V(G), F)$, and each is named by one of its vertices; (c) $E$ holds, renamed to supervertex names, exactly the edges of $G$ whose ends are in different supervertices; (d) $V$ is the set of supervertices that are ends of an edge of $E$.

At the start, $F = \emptyset$, each vertex is its own supervertex, and $E$ and $V$ are those of $G$ (with the vertices of degree 0 left out of $V$), so the invariant holds.

**Lemma 1 (the picks).** For $v \in V$, $best[v]$ is the edge of $G$ of least key with exactly one end in the supervertex $v$. So $best[v] \in M$.

*Proof.* By (c), the edges of $E$ at $v$ are exactly the edges of $G$ with one end in $v$ and the other end in another supervertex. The cut property applies with $S$ the supervertex $v$. $\square$

**Lemma 2 (the pointer forest).** After line L5, $P$ restricted to $V$ is a forest, and every tree has at least two vertices.

*Proof.* After line L4, $P[v]$ is the other end of $best[v]$, which is in $V$ and differs from $v$. Let $u = P[v]$. The edge $best[v]$ is an edge of $E$ at $u$, so $key(best[u]) \le key(best[v])$, with equality only if $best[u] = best[v]$, since keys differ. Along a walk $v_0, v_1 = P[v_0], v_2 = P[v_1], \ldots$ the keys of the picks never grow. On a cycle of $P$ they must all be equal, so all vertices of the cycle picked one edge, which has two ends; so the cycle has length 2. Every vertex has one pointer, so each component of $P$ has exactly one cycle, and line L4 leaves only 2-cycles. Line L5 reads the values of line L4. For a 2-cycle $\{u, v\}$ with $u < v$, it makes $u$ a root and leaves $P[v] = u$. A vertex not on a cycle has $P[P[v]] \ne v$ and keeps its pointer. So every component now has exactly one root and no cycle, and the root $u$ of each tree has its partner $v$ in the tree. A vertex that is not a root points to another vertex of its tree. So every tree has at least two vertices. $\square$

**Lemma 3 (one round keeps the invariant).** If the invariant holds at the start of a round with $E \ne \emptyset$, it holds at the start of the next round, and $|V_{\text{next}}| \le \lfloor |V| / 2 \rfloor$.

*Proof.* Line L6 adds $best[v]$ for every non-root $v$. These edges are in $M$ by Lemma 1, so (a) holds. Each added edge $best[v]$ joins the supervertex $v$ to the supervertex $P[v]$, its other end. An edge of a 2-cycle is added once, by the larger end, since the smaller end is a root. So the new edges join the supervertices exactly along the trees of $P$, one edge for each non-root, and the new components of $(V(G), F)$ are the unions of the supervertices of each tree, together with the supervertices outside $V$, which gain nothing. Line L7 makes $P[v]$ the root of the tree of $v$, by the pointer jumping property: each step replaces a pointer by the pointer two levels up and leaves roots fixed, so it ends when all vertices point to their roots. The new supervertex is named by that root. So (b) holds. Line L8 renames the ends of each edge of $E$ to the new names and keeps exactly the edges whose ends are in different new supervertices; the edges of $G$ whose ends were already in one supervertex were not in $E$ and stay out. So (c) holds, and line L9 gives (d).

By Lemma 2 each tree of $P$ has at least two vertices of $V$, so the new supervertices that hold a vertex of $V$ number at most $\lfloor |V| / 2 \rfloor$, and $V_{\text{next}}$ is a subset of them. $\square$

**Theorem.** The algorithm stops after at most $\lceil \log_2 n \rceil$ rounds for $n \ge 1$, and it returns $M$.

*Proof.* If $E \ne \emptyset$, then $|V| \ge 2$. By Lemma 3, after $t$ rounds $|V| \le n / 2^t$. If round $t + 1$ runs, then $2 \le n / 2^t$, so $t + 1 \le \log_2 n$. So the number of rounds is at most $\lfloor \log_2 n \rfloor \le \lceil \log_2 n \rceil$. When the loop stops, $E = \emptyset$, so by (c) no edge of $G$ joins two components of $(V(G), F)$. Let $e \in M$. If $e \notin F$, its ends are in different components of $F$: if they were in one, the path in $F \subseteq M$ between them together with $e$ would be a cycle in $M$. Then $e$ joins two components of $F$, which is impossible. So $M \subseteq F$, and with (a), $F = M$. $\blacksquare$
