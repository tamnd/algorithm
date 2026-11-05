---
title: The cluster method keeps the minimum spanning forest, and the topology tree is a valid hierarchy
proves: [correctness]
status: full
---

Order the edges by the key (weight, smaller end, larger end); all keys are distinct, so every graph $G$ has a unique minimum spanning forest $\mathrm{MSF}(G)$. We use two standard facts for distinct keys.

- **Cycle property.** An edge $e$ is not in $\mathrm{MSF}(G)$ if and only if $G$ has a cycle on which $e$ is the heaviest edge; equivalently, for $e = \{u, v\}$, the path between $u$ and $v$ in $\mathrm{MSF}(G - e)$ exists and has only lighter edges.
- **Cut property.** For any cut of $G$, the lightest edge crossing it is in $\mathrm{MSF}(G)$.

**Invariants.** After every update:

- (F) $F = \mathrm{MSF}(G)$;
- (C) the clusters partition $V$, each cluster is connected in $F$, and the cluster tree has one edge per forest edge between two distinct clusters;
- (T) the table holds exactly the edges of $G - F$, each under the pair of clusters of its two ends.

Initially $G$ and $F$ are empty and the clusters are single vertices, so all three hold.

**Lemma 1 (walks on the cluster tree).** Under (C), two vertices are in the same tree of $F$ if and only if their clusters are connected in the cluster tree, and the clusters met on the forest path from $u$ to $v$ are exactly the clusters on the path from $C(u)$ to $C(v)$ in the cluster tree.

*Proof.* Contracting each cluster of a forest to one node, when each cluster is connected, gives a forest (a cycle of clusters would lift to a cycle in $F$, since each cluster is connected) whose edges are the forest edges between clusters. Contraction preserves connectivity. A forest path from $u$ to $v$ maps to a walk from $C(u)$ to $C(v)$; it never re-enters a cluster it left, since that would give two paths in $F$ between two vertices of a connected cluster. So it maps to the unique path in the cluster tree. $\square$

**Lemma 2 (cluster maintenance).** The operations on clusters keep (C) and (T).

*Proof.* Adding a forest edge between two clusters adds one cluster tree edge, and joining two clusters $a$ and $b$ joined by a forest edge gives a connected set. Removing a forest edge inside a cluster $c$ splits $c$, which was connected by a subtree of $F$, into exactly the two parts reachable from $u$ and from $v$ inside $c$; each is connected, and line L4 makes the smaller one a new cluster. Removing a forest edge between two clusters removes one cluster tree edge. When vertices move to a new cluster, the cluster tree edges at those vertices are removed and added again with the new names, and every non-tree edge at those vertices is removed from its old table pair and added under its new pair; non-tree edges at other vertices keep their pair. Re-clustering in line L7 builds each cluster as a union of connected pieces joined through forest edges, so each cluster is connected, and it rebuilds the cluster tree and the table from $F$ and $G - F$. $\square$

**Lemma 3 (monotonicity).** Let $e$ be an edge. (a) $\mathrm{MSF}(G + e) \subseteq \mathrm{MSF}(G) + e$. (b) $\mathrm{MSF}(G) - e \subseteq \mathrm{MSF}(G - e)$. (c) A minimum spanning forest of a graph with $c$ components on $n$ vertices has $n - c$ edges.

*Proof.* (a) An edge $f \neq e$ outside $\mathrm{MSF}(G)$ is the heaviest edge of a cycle of $G$, which is also a cycle of $G + e$, so $f \notin \mathrm{MSF}(G + e)$. (b) If $f \in \mathrm{MSF}(G)$, $f \neq e$, were the heaviest edge of a cycle of $G - e$, that cycle would be in $G$. (c) It is a spanning forest. $\square$

**Lemma 4 (insertion).** If (F), (C), (T) hold before INSERT$(u, v, w)$, they hold after it.

*Proof.* Let $e = \{u, v\}$ and $G' = G + e$. By Lemma 3(a), $\mathrm{MSF}(G') \subseteq F + e$.

If $u$ and $v$ are in different trees of $F$, which line L1 tests by Lemma 1, then $G'$ has one component less than $G$, so by Lemma 3(c) $\mathrm{MSF}(G')$ has $|F| + 1$ edges and equals $F + e$.

Otherwise $G'$ has the same components as $G$, so $\mathrm{MSF}(G')$ has $|F|$ edges. Let $P$ be the forest path from $u$ to $v$, which line L2 finds inside the clusters of the cluster path by Lemma 1, and $x$ its heaviest edge. The edges $P + e$ form a cycle of $G'$. If $e$ is heavier than $x$, it is the heaviest edge of that cycle, so $e \notin \mathrm{MSF}(G')$, hence $\mathrm{MSF}(G') \subseteq F$, and by size $\mathrm{MSF}(G') = F$; line L3 puts $e$ in the table. If $e$ is lighter than $x$, then $x$ is the heaviest edge of that cycle, so $\mathrm{MSF}(G') \subseteq F - x + e$, and both sides have $|F|$ edges, so they are equal; line L3 makes this change and puts $x$ in the table.

The cluster and table changes keep (C) and (T) by Lemma 2. $\square$

**Lemma 5 (deletion).** If (F), (C), (T) hold before DELETE$(u, v)$, they hold after it.

*Proof.* Let $e = \{u, v\}$ and $G' = G - e$. By Lemma 3(b), $F - e \subseteq \mathrm{MSF}(G')$.

If $e \notin F$, the components do not change, so $\mathrm{MSF}(G')$ has $|F|$ edges and contains $F$; it is $F$, and only the table entry is removed.

If $e \in F$, removing it splits a tree into $T_u$ and $T_v$. If no edge of $G'$ joins $T_u$ and $T_v$, then $G'$ has one component more, $\mathrm{MSF}(G')$ has $|F| - 1$ edges and contains $F - e$, so it is $F - e$. Otherwise the lightest edge $r$ of $G'$ between $T_u$ and $T_v$ is in $\mathrm{MSF}(G')$ by the cut property, the components do not change, and $F - e + r \subseteq \mathrm{MSF}(G')$ has $|F|$ edges, so it is $\mathrm{MSF}(G')$.

It remains to see that lines L5 and L6 find $r$. After line L4, (C) holds by Lemma 2, so by Lemma 1 the walks on the cluster tree from $C(u)$ and $C(v)$ give exactly the clusters of $T_u$ and of $T_v$. Every edge of $G'$ between $T_u$ and $T_v$ is a non-tree edge, so by (T) it is in the table under a pair $(a, b)$ with $a$ a cluster of $T_u$ and $b$ one of $T_v$, and every edge under such a pair joins the two sides. So the minimum over these pairs is $r$, or there is none. Line L6 moves $r$ from the table to $F$, and Lemma 2 keeps (C) and (T). $\square$

By induction on the updates, Lemmas 4 and 5 give (F) after every update.

**Lemma 6 (topology tree).** BUILD-TOPOLOGY-TREE on a tree of maximum degree three returns levels in which every cluster is connected, has at most three edges leaving it, and is the union of one or two clusters of the level below; the last level is the whole tree.

*Proof.* Level 0 has single vertices, with external degree at most three. A pair joined at line L9 is two adjacent clusters, so the union is connected. Between two adjacent clusters of a tree there is exactly one edge, so the union has external degree $d_1 + d_2 - 2$; the allowed pairs have $d_1 = 1$, giving at most $3 - 1 = 2$, or $d_1, d_2 \le 2$, giving at most 2. Unpaired clusters are copied. The loop stops only when no adjacent pair is allowed. If the level has two or more clusters, the cluster tree is a tree with at least two nodes and so has a leaf, of external degree 1, which may be paired with its neighbor; so the loop stops only at a single cluster, the whole tree. Each level with at least two clusters joins at least one pair, so the loop ends. $\blacksquare$
