---
title: Prim's algorithm returns a minimum spanning forest
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite undirected graph with a real weight $w(e)$ on each edge. Weights may tie and may be negative, $G$ may have parallel edges and self-loops, and $G$ need not be connected. Then PRIM$(G, w)$ stops, and the set $F$ that it returns is a minimum spanning forest of $G$: a forest with the same connected components as $G$, of least total weight among all such forests.

**Setup.** A vertex is *in a tree* when $inTree[v] = \text{true}$. Each run of lines L4 to L12 for one root $r$ is a *phase*. During a phase, $S$ is the set of vertices that joined in this phase, and $D$ is the set of vertices that joined in earlier phases. $U = V \setminus (S \cup D)$ is the set of outside vertices. Let $F_{\text{now}} = \{\pi[x] : x \in S \cup D, \pi[x] \ne \text{nil}\}$. Each spanning forest of $G$ has $n - c$ edges, where $c$ is the number of components ([spanning forest](/spanning-forest/)), and a minimum spanning forest exists because $E$ is finite.

**Lemma 1 (the cut step).** Let $A \subseteq F^*$ for a minimum spanning forest $F^*$. Let $X \subseteq V$ be a set such that no edge of $A$ has exactly one end in $X$. Let $e$ be an edge with exactly one end in $X$ and $w(e) \le w(f)$ for each edge $f$ with exactly one end in $X$. Then $A \cup \{e\}$ is a subset of some minimum spanning forest.

*Proof.* If $e \in F^*$, take $F^*$. Otherwise let $e = uv$ with $u \in X$ and $v \notin X$. The edge $e$ joins $u$ and $v$, so they are in one component of $G$ and so in one tree of $F^*$. The path $P$ from $u$ to $v$ in that tree starts in $X$ and ends outside $X$, so it has an edge $f$ with exactly one end in $X$, and $f \notin A$. Let $F' = F^* \setminus \{f\} \cup \{e\}$. Removing $f$ splits its tree into a tree with $u$ and a tree with $v$, since $f$ is on the only path between them, and $e$ joins them again. So $F'$ is a forest with the components of $F^*$, which are those of $G$. Its weight is $w(F^*) - w(f) + w(e) \le w(F^*)$, so $F'$ is a minimum spanning forest. It contains $A$, since $f \notin A$, and it contains $e$. $\square$

**Invariant.** Before each run of line L6, and at the end of each phase:

- **(I1)** For each $v \in U$: if some edge joins a vertex of $S$ to $v$, then $\pi[v]$ is such an edge and $key[v] = w(\pi[v])$ is the least weight of such an edge. Otherwise $key[v] = \infty$ and $\pi[v] = \text{nil}$.
- **(I2)** For each $v \in U$ with $key[v] < \infty$, the pair $(key[v], v)$ is in $Q$. Each pair $(k, v)$ in $Q$ with $v \in U$ has $k \ge key[v]$.
- **(I3)** No edge of $G$ joins a vertex of $D$ to a vertex of $S \cup U$. The vertices of $S$, with the edges $\pi[x]$ for $x \in S \setminus \{r\}$, form a tree, and $\pi[r] = \text{nil}$.
- **(I4)** There is a minimum spanning forest $F^*$ with $F_{\text{now}} \subseteq F^*$.

**Initialization of a phase.** At the start of the phase for $r$, by (I3) of the earlier phases (or trivially for the first phase), no edge joins $D$ to $U \cup \{r\}$. Line L1 set $key[v] = \infty$ for every vertex, and a key changes only in line L11, for a vertex outside all trees. A vertex $v \in U$ could have a finite key only from an edge scanned from a vertex of $D$, and no such edge reaches $U$. So before line L4, every $v \in U \cup \{r\}$ has $key[v] = \infty$ and $\pi[v] = \text{nil}$. Line L4 sets $key[r] = 0$ and $Q = \{(0, r)\}$, and at this moment $S = \emptyset$. (I1) holds since $S$ is empty and all keys of $U \setminus \{r\}$ are infinite; we treat $r$ as a member of $U$ with key $0$, and (I2) holds for it. (I3) holds for $S = \emptyset$, and (I4) holds by the earlier phases (for the first phase, $F_{\text{now}} = \emptyset$ is in every minimum spanning forest).

**Maintenance.** Consider a run of lines L6 to L12 that takes the pair $(k, u)$.

1. *A stale pair.* If $u$ is in a tree, line L7 skips it. Removing a pair whose vertex is not in $U$ changes no statement.
2. *The first pair of the phase.* Then $u = r$, $S = \emptyset$, and line L8 makes $S = \{r\}$. Lines L9 to L12 scan each edge $e = rv$. For each $v \in U$, after the scan, $key[v]$ is the least weight of an edge from $r$ to $v$ and $\pi[v]$ is that edge, because line L10 replaces the key exactly when the new edge is strictly lighter. Each new key is pushed in line L12. So (I1) and (I2) hold. (I3) holds: $S = \{r\}$ is a tree with no edge. (I4) holds since $F_{\text{now}}$ did not change.
3. *A later pair with $u \in U$.* By (I2), every pair in $Q$ with a vertex in $U$ has $k' \ge key[v']$, and the pair $(key[v], v)$ is in $Q$ for each finite key. The pair taken is the least in $Q$, so $k \le key[v]$ for each $v \in U$ with a finite key, and $k \ge key[u]$. So $key[u] \le k \le key[u]$, and $key[u] = \min_{v \in U} key[v]$. This minimum is finite, because $k$ is finite.

   By (I1), $\pi[u]$ is an edge from $S$ to $u$, with weight $key[u]$. Let $f$ be any edge with exactly one end in $S$. By (I3), its other end is not in $D$, so it is some $v \in U$, and by (I1) $w(f) \ge key[v] \ge key[u] = w(\pi[u])$. So $\pi[u]$ is a lightest edge with exactly one end in $S$. No edge of $F_{\text{now}}$ has exactly one end in $S$: the edges $\pi[x]$ with $x \in S$ lie inside $S$ by (I3), and the edges $\pi[x]$ with $x \in D$ lie inside $D$ because they were edges of earlier trees. Lemma 1 with $X = S$, $A = F_{\text{now}}$ and $e = \pi[u]$ gives a minimum spanning forest that holds $F_{\text{now}} \cup \{\pi[u]\}$. Line L8 adds $u$ to $S$, and this is (I4) after the step.

   The new $S$ is a tree, since $\pi[u]$ joins the tree $S$ to the new vertex $u$, so (I3) holds. For each $v \in U$ after the step, the edges from the new $S$ to $v$ are the old ones and the edges from $u$ to $v$. Lines L9 to L11 scan every edge $uv$ and keep the lightest, so (I1) holds. Line L12 pushes each new key, and a key only drops, so each old pair has $k \ge key[v]$, and (I2) holds.

**End of a phase.** The loop of line L5 stops when $Q$ is empty. By (I2), every $v \in U$ then has $key[v] = \infty$, and by (I1) no edge joins $S$ to $U$. By (I3), no edge joins $S$ to $D$. So $S$ is a union of components of $G$. It is connected by its tree edges, so $S$ is exactly the component of $r$. The phase moves $S$ into $D$, and (I3) holds for the next phase: no edge joins the new $D$ to the new $U$.

**Termination.** Each pair is pushed at most once per run of line L4 or line L12. Line L12 runs only when line L8 has just put a vertex in a tree, and line L8 runs at most $n$ times, since each vertex joins once; each such run pushes at most $\deg(u)$ pairs. So at most $n + 2m$ pairs are ever pushed, and each run of line L6 removes one. Each phase stops, there are at most $n$ phases, and the loop of line L2 stops.

**Conclusion.** Each vertex is in a tree at the end, because line L3 starts a phase at each vertex outside all trees. By the end-of-phase step, the trees are exactly the components of $G$, and each tree is spanned by its edges $\pi[x]$, one for each non-root vertex. So $F$ is a forest with the components of $G$, with $n - c$ edges. By (I4), $F \subseteq F^*$ for a minimum spanning forest $F^*$, which also has $n - c$ edges, so $F = F^*$. Therefore $F$ is a minimum spanning forest, and a minimum spanning tree when $G$ is connected. $\blacksquare$
