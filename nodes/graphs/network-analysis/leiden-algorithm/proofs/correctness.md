---
title: The deterministic Leiden algorithm stops, never lowers modularity, and returns connected communities in which no single vertex gains by moving
proves: [correctness, termination]
status: full
---

The proof is for the deterministic version of the page, with the check of line L18. The stronger guarantees of Traag, Waltman and van Eck ($\gamma$-separation, uniform $\gamma$-density and subset optimality) are not proved here.

Let $G$ be an undirected graph on $V$ with positive integer weights $A_{ij} = A_{ji}$, where $A_{ii}$ is the weight of the self-loop at $i$, and total weight $W > 0$. For a graph $H$, use the conventions of the Louvain page: $k_x$ counts a self-loop twice, $\mathrm{in}(C)$ is the weight inside $C$, $\mathrm{tot}(C) = \sum_{x \in C} k_x$, and $Q_H(\mathcal{C}) = \sum_C (\mathrm{in}(C)/W - (\mathrm{tot}(C)/2W)^2)$. Every graph $H$ that the algorithm builds has $W_H = W$.

Three facts come from [the proof of the Louvain method](/louvain-method/): **(gain)** if $\{v\}$ is a part of a partition and $D$ is another part, merging $v$ into $D$ changes $Q_H$ by $\Delta Q(v, D) = k_{v,D}/W - \mathrm{tot}(D) k_v/(2W^2)$, and $\Delta Q(v, \emptyset) = 0$; **(aggregation)** if $H'$ is built from $H$ and a partition $R$ as in line L8, then $Q_{H'}$ of a partition of the vertices of $H'$ equals $Q_H$ of the matching partition of the vertices of $H$; **(integrality)** for integer weights, $4W^2 Q$ is an integer and $-1 \le Q < 1$. By the aggregation fact and induction, $Q_H$ of the current partition $P$ of $H$ always equals $Q_G$ of the matching partition of $V$.

**Lemma 1 (moves raise Q).** Each execution of lines L14 to L16 that changes the community of $v$ raises $Q_G$ of the current partition of $V$ by a positive amount.

*Proof.* Let $\mathcal{C}^-$ be the partition with $v$ alone. By the gain fact, putting $v$ into a community $D$ gives $Q_H(\mathcal{C}^-) + \Delta Q(v, D)$, and putting it into an empty community gives $Q_H(\mathcal{C}^-)$. Line L15 leaves $old$ only for a choice whose gain is strictly larger than the gain of $old$. $\square$

**Lemma 2 (local optimality at the end of MOVE-NODES-FAST).** When MOVE-NODES-FAST returns, no vertex $v$ of $H$ has a community $D$ of a neighbour, or the empty community, with a gain larger than that of its own community.

*Proof.* It returns only when line L18 finds no vertex that line L15 would move, and line L15 would move $v$ exactly when such a $D$ exists. $\square$

**Lemma 3 (termination of the moves).** In the whole run there are fewer than $8W^2$ moves.

*Proof.* Lines L7 to L9 and the start of a pass do not change the partition of $V$, and refinement only changes $R$. So by Lemma 1 the integer $4W^2 Q_G$ rises by at least 1 at each move and never falls. It takes fewer than $8W^2$ values. $\square$

Each call of MOVE-NODES-FAST ends: every pop either moves a vertex, which happens finitely often by Lemma 3, or removes a vertex from $Q$; a vertex enters $Q$ only after a move (line L17) or at a check that found a vertex to move, and the first vertex that such a check finds moves when it is popped, because nothing changes between the check and that pop.

**Lemma 4 (well-connected vertices).** Let MOVE-NODES-FAST return $P$ and let $C \in P$. Every $v \in C$ is well connected in $C$.

*Proof.* If $C = \{v\}$, both sides of the inequality are 0. Otherwise, by Lemma 2, the gain of staying in $C$ is at least the gain 0 of the empty community: $k_{v, C \setminus v}/W - (\mathrm{tot}(C) - k_v) k_v/(2W^2) \ge 0$. Multiplying by $W$ gives $E(\{v\}, C \setminus \{v\}) \ge k_v (\mathrm{tot}(C) - k_v)/2W$, which is the definition. $\square$

**Lemma 5 (refinement makes progress).** If $P$ has a community $C$ with at least two vertices of $H$, then REFINE merges at least one vertex of $C$ into another part.

*Proof.* By Lemma 4, line L22 gives $A = C$. Let $v$ be the first vertex of $C$ in index order. When line L24 reaches it, no vertex of $C$ has been touched, so all parts of $R$ inside $C$ are singletons, and each $\{u\}$ with $u \in C$ is well connected by Lemma 4. Every vertex $x$ of $C$ has $k_x > 0$: a vertex of $H$ with $k_x = 0$ has no neighbour, so it never joins another community and no vertex joins its community (lines L15 and L25 only offer communities of neighbours, besides the empty one), and so its community is a singleton. By the inequality of Lemma 4 for $v$, $k_{v, C \setminus v} \ge k_v (\mathrm{tot}(C) - k_v)/2W > 0$, so $v$ has a neighbour in $C$ and $T$ is not empty. Since $k_{v,D}$ and $\mathrm{tot}(D)$ are additive in $D$,
$$\sum_{u \in C \setminus v} \Delta Q(v, \{u\}) = \Delta Q(v, C \setminus \{v\}) \ge 0$$
by Lemma 2 again. A term with $u$ not adjacent to $v$ is $-k_u k_v/(2W^2) < 0$, so the terms of the neighbours of $v$ in $C$, which are the members of $T$, sum to a non-negative number, and the largest of them is non-negative. Line L27 merges $v$. $\square$

**Lemma 6 (parts are connected).** At every moment, each vertex of $H$ stands for a set of vertices of $G$ that induces a connected subgraph, and each part of $R$ is a set of vertices of $H$ whose union is connected in $G$.

*Proof.* At the start of each pass, $H = G$ and its vertices are single vertices. A part of $R$ starts as one vertex of $H$ and grows only at line L27, by a vertex $v$ of $H$ that is adjacent in $H$ to the part $S$. An edge of $H$ between $v$ and a vertex of $S$ comes from an edge of $G$ between their sets; so if the union for $S$ and the set of $v$ are connected, so is their union. Line L8 makes each part of $R$ a vertex of the next $H$. $\square$

**Theorem.** LEIDEN($G$) stops. It returns a partition $P$ of $V$ such that
1. every community of $P$ induces a connected subgraph of $G$;
2. $Q_G(P) \ge Q_G(\text{singletons of } V)$;
3. no vertex of $G$ raises $Q_G$ by moving into the community of a neighbour or into a community of its own.

*Proof.* Termination. Each call of MOVE-NODES-FAST ends (above). If line L6 does not exit, some community has two vertices of $H$, so by Lemma 5 the refinement merges something, $R$ has fewer parts than $H$ has vertices, and the next $H$ is smaller. So the loop of lines L4 to L9 runs at most $n$ times. A pass that ends with $P \ne P_{old}$ made a move, so by Lemma 3 there are fewer than $8W^2 + 1$ passes.

Property 1. The pass returns from line L6, when each community of $P$ is one vertex of $H$; by Lemma 6 it is connected in $G$.

Property 2. $Q_G$ starts at the singletons and never falls (Lemma 1 and the aggregation fact).

Property 3. In the last pass, $P$ equals $P_{old}$ at the end. Any move in the pass would raise $Q_G$ by Lemma 1, and nothing lowers it, so the pass ends with a different partition; hence no move happened. In particular, the first call of MOVE-NODES-FAST, on $H = G$, made no move and returned $P_{old}$, and by Lemma 2 no vertex of $G$ has a better community among those of its neighbours and the empty one. By the gain fact, the gain of a move is the change of $Q_G$. $\square$

∎
