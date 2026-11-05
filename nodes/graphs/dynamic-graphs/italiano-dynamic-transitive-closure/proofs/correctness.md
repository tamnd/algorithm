---
title: Italiano's reachability trees stay exact under insertions, and under deletions in a DAG
proves: [correctness]
status: full
---

Write $R(x)$ for the set of vertices reachable from $x$ in the current graph, with $x \in R(x)$. The invariant is:

**(T)** For every $x$, $\mathrm{desc}(x)$ is a tree rooted at $x$ with vertex set $R(x)$, and every tree edge from a parent $p$ to a child $w$ is an edge $(p, w)$ of the graph.

If (T) holds, line L5 is correct, and line L6 returns a path of graph edges from $x$ to $y$, because following parents from $y$ in a rooted tree ends at the root. For the empty graph, every tree is the single vertex $x$, and (T) holds.

## Insertions

**Lemma 1.** Let $G'$ be $G$ with the new edge $(i, j)$, and $R'$ the reachable sets in $G'$. If $i \in R(x)$, then $R'(x) = R(x) \cup R(j)$. Otherwise $R'(x) = R(x)$.

*Proof.* A path in $G'$ that does not use $(i, j)$ is a path in $G$. A path from $x$ to $y$ that uses $(i, j)$ reaches $i$ in $G$ before its first use, so $i \in R(x)$, and after its last use it is a path in $G$ from $j$ to $y$, so $y \in R(j)$. So $R'(x) \subseteq R(x) \cup R(j)$ when $i \in R(x)$, and $R'(x) = R(x)$ when no path from $x$ reaches $i$, since then the new edge is never used. The reverse inclusion is clear. $\square$

Note that $R(j)$ does not change in the insertion when it matters: by Lemma 1 with $x = j$, $R'(j) = R(j) \cup R(j)$ if $i \in R(j)$, so $R'(j) = R(j)$ in all cases. Line L2 never picks $x = j$, because $j \in \mathrm{desc}(j)$, so $\mathrm{desc}(j)$ is not changed while it is read.

**Lemma 2.** If (T) holds before INSERT$(i, j)$, then it holds after it.

*Proof.* Fix $x$. If $i \notin \mathrm{desc}(x)$, then $i \notin R(x)$ and $R'(x) = R(x)$ by Lemma 1, and $\mathrm{desc}(x)$ is not changed. If $j \in \mathrm{desc}(x)$, then $R(j) \subseteq R(x)$, since reachability is transitive, so again $R'(x) = R(x)$ and nothing changes.

Otherwise line L3 walks $\mathrm{desc}(j)$ from $j$. We claim that after the walk the vertex set of $\mathrm{desc}(x)$ is $R(x) \cup R(j)$. Every vertex added is in $\mathrm{desc}(j)$, so in $R(j)$. Conversely let $w \in R(j) \setminus R(x)$. Its path in $\mathrm{desc}(j)$ from $j$ is $j = w_0, w_1, \ldots, w_k = w$. No $w_t$ is in $R(x)$: otherwise $w$, which is reachable from $w_t$ by tree edges, would be in $R(x)$ by transitivity. So none of $w_0, \ldots, w_k$ was in $\mathrm{desc}(x)$ before the walk. The walk reaches $w_0$ first. When the walk reaches $w_t$, it is not yet in $\mathrm{desc}(x)$, because each vertex of the tree $\mathrm{desc}(j)$ is reached only from its parent, at most once; so it is added and its children, including $w_{t+1}$, are pushed. By induction, $w$ is added. Pruned vertices are in $\mathrm{desc}(x)$ already, and every vertex is added at most once since the walk skips vertices already present.

Each added vertex $w$ gets as parent a vertex already in $\mathrm{desc}(x)$: $i$ for $w = j$, and otherwise its parent in $\mathrm{desc}(j)$, which was added just before $w$ was pushed. So the parents point to earlier vertices, and $\mathrm{desc}(x)$ is still a tree rooted at $x$. The new tree edges are $(i, j)$, a graph edge, and edges of $\mathrm{desc}(j)$, graph edges by (T). With Lemma 1, the vertex set is $R'(x)$, and (T) holds for $x$. $\square$

## Deletions in a DAG

Now the graph is acyclic, and $\pi$ is a topological numbering: $\pi(z) < \pi(w)$ for every edge $(z, w)$. Edges are only deleted, so $\pi$ stays a topological numbering, and reachable sets only shrink. For deletions we add a second invariant.

**(P)** For every $x$ and every $w \in R(x) \setminus \{x\}$, the pointer of $w$ in $\mathrm{desc}(x)$ is at its tree parent $p$, the edge $(p, w)$ is present, and every in-edge of $w$ before the pointer either is deleted or comes from a vertex $z \notin R(x)$.

The construction sets every pointer at the first present in-edge from a vertex of $R(x)$, so (P) holds at the start. The resulting parent pointers go from larger to smaller $\pi$, so they form a tree rooted at $x$, and (T) holds.

**Lemma 3.** If (T) and (P) hold before DELETE$(u, v)$, then they hold after it.

*Proof.* Let $R'$ be the new reachable sets. Fix $x$. If $u$ is not the parent of $v$ in $\mathrm{desc}(x)$, the tree uses no deleted edge, so it is still a tree of graph edges and spans a set of vertices reachable in the new graph; since $R'(x) \subseteq R(x)$, it spans $R'(x)$. The pointers do not move, and the edges before them still satisfy (P), since sets only shrink. So assume $u = \mathrm{par}_x(v)$.

Call a vertex **settled** when it is taken from $Q$ and processed. We prove, by induction in the order of processing, that when $w$ is taken from $Q$:

- (a) every vertex $z$ with $\pi(z) < \pi(w)$ that is marked reachable in $\mathrm{desc}(x)$ is in $R'(x)$, and every vertex not marked reachable is not in $R'(x)$;
- (b) $w$ is hooked again if and only if $w \in R'(x)$.

The vertices put into $Q$ are $v$ and the children of removed vertices. Each child has a larger number than its parent, and $Q$ returns the least number, so the numbers taken from $Q$ increase. A vertex is marked not reachable when it enters $Q$, and its descendants keep their marks until their own turn.

For (a): a vertex $z$ with $\pi(z) < \pi(w)$ that is marked reachable is either settled and hooked, so in $R'(x)$ by (b) for $z$, or it was never an orphan. In the second case its whole tree path from $x$ consists of vertices that were never orphans, since an orphan's descendants all become orphans until the orphan is hooked again, and a hooked orphan is in $R'(x)$. So its tree path uses only present edges and $z \in R'(x)$. A vertex marked not reachable is either outside $R(x)$, and so outside $R'(x)$, or it was settled and removed, so outside $R'(x)$ by (b).

For (b): the in-neighbors $z$ of $w$ have $\pi(z) < \pi(w)$, so by (a) the test $z \in \mathrm{desc}(x)$ of line L9 is exactly $z \in R'(x)$. If $w \in R'(x)$, a path from $x$ to $w$ in the new graph ends with a present edge $(z, w)$ with $z \in R'(x)$. That edge is at or after the pointer: every edge before it, by (P), was deleted or came from a vertex outside $R(x) \supseteq R'(x)$. So line L9 finds an edge and hooks $w$. If $w \notin R'(x)$, every present in-edge comes from a vertex outside $R'(x)$, so no edge is found and $w$ is removed. Every edge passed by the pointer is deleted or comes from outside $R'(x)$, so (P) holds for $w$ afterwards.

When $Q$ is empty, every orphan has been settled. A vertex of $R(x)$ that never became an orphan keeps its tree path, which uses present edges, so it is in $R'(x)$. Every vertex of $R(x) \setminus R'(x)$ lies below the deleted tree edge, so it became an orphan and was removed by (b). So the marked vertices are exactly $R'(x)$. The parents of hooked vertices have smaller numbers and are in $R'(x)$, so the parent pointers again form a tree rooted at $x$ of present edges. Hence (T) and (P) hold. $\square$

**Theorem.** Under insertions in any digraph, and under deletions in a DAG, every query REACHABLE$(x, y)$ returns whether $y \in R(x)$, and PATH$(x, y)$ returns a path of graph edges from $x$ to $y$ when there is one.

*Proof.* By induction on the updates, (T) holds after each insertion by Lemma 2, and (T) and (P) hold after each deletion by Lemma 3. Queries read $\mathrm{desc}(x)$, which by (T) has vertex set $R(x)$ and consists of graph edges. $\blacksquare$
