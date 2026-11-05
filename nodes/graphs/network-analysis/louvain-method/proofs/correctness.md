---
title: The Louvain method raises modularity at every move, stops, and ends at a partition that no single move of the last level improves
proves: [correctness, termination]
status: full
---

Let $G$ be an undirected graph on $V$ with non-negative weights $A_{ij} = A_{ji}$, where $A_{ii}$ is the weight of the self-loop at $i$, and total weight $W > 0$. For a graph $H$ with weights $B$, use the conventions of the page: $k_x = \sum_{y \ne x} B_{xy} + 2 B_{xx}$, $W_H = \frac12 \sum_x k_x$, $\mathrm{in}(C) = \sum_{\{x,y\} \subseteq C, x \ne y} B_{xy} + \sum_{x \in C} B_{xx}$ and $\mathrm{tot}(C) = \sum_{x \in C} k_x$, and $Q_H(\mathcal{C}) = \sum_{C} \left( \mathrm{in}(C)/W_H - (\mathrm{tot}(C)/2W_H)^2 \right)$.

**Lemma 1 (the gain formula).** Let $\mathcal{C}$ be a partition of the vertices of $H$ in which $\{v\}$ is a part, and let $D \in \mathcal{C}$ with $v \notin D$. Moving $v$ into $D$ changes $Q_H$ by $\Delta Q(v, D) = k_{v,D}/W_H - \mathrm{tot}(D) k_v / (2 W_H^2)$, where $k_{v,D} = \sum_{y \in D} B_{vy}$. If $D = \emptyset$, the change is 0.

*Proof.* Only the terms of $\{v\}$ and $D$ change. The new part $D \cup \{v\}$ has $\mathrm{in} = \mathrm{in}(D) + k_{v,D} + B_{vv}$ and $\mathrm{tot} = \mathrm{tot}(D) + k_v$. The change is
$$\frac{k_{v,D} + B_{vv}}{W_H} - \frac{(\mathrm{tot}(D) + k_v)^2 - \mathrm{tot}(D)^2}{4 W_H^2} - \frac{B_{vv}}{W_H} + \frac{k_v^2}{4 W_H^2} = \frac{k_{v,D}}{W_H} - \frac{2\,\mathrm{tot}(D) k_v}{4 W_H^2}.$$
For $D = \emptyset$, moving $v$ into it changes nothing. $\square$

**Lemma 2 (each move raises Q).** Let lines L7 to L9 take $v$ from the community $old$ to $C \ne old$. Then $Q_H$ after the step is larger than before it.

*Proof.* Line L7 gives the partition $\mathcal{C}^-$ in which $v$ is alone. By Lemma 1, the partition before the step has $Q_H(\mathcal{C}^-) + \Delta Q(v, old \setminus \{v\})$ and the one after has $Q_H(\mathcal{C}^-) + \Delta Q(v, C)$. Line L8 picks $C \ne old$ only when $\Delta Q(v, C) > \Delta Q(v, old \setminus \{v\})$, since on ties it keeps $old$. $\square$

**Lemma 3 (aggregation keeps Q).** Let $H'$ be built from $H$ and the partition $\mathrm{comm}$ by line L13, and let $\mathcal{D}$ be a partition of the vertices of $H'$. Let $\mathcal{D}^\ast$ be the partition of the vertices of $H$ that puts $x$ in the part of $\mathcal{D}$ that holds the community of $x$. Then $Q_{H'}(\mathcal{D}) = Q_H(\mathcal{D}^\ast)$.

*Proof.* The vertex $c$ of $H'$ has a self-loop of weight $\mathrm{in}_H(c)$ and an edge of weight $\sum_{x \in c, y \in c'} B_{xy}$ to $c'$. So $k_c$ in $H'$ is $2\,\mathrm{in}_H(c) + \sum_{x \in c, y \notin c} B_{xy} = \mathrm{tot}_H(c)$, and $W_{H'} = W_H$. For a part $D$ of $\mathcal{D}$, $\mathrm{in}_{H'}(D)$ adds the self-loops of its vertices and the edges between them, which is the weight of all edges of $H$ inside $D^\ast$, so $\mathrm{in}_{H'}(D) = \mathrm{in}_H(D^\ast)$, and $\mathrm{tot}_{H'}(D) = \mathrm{tot}_H(D^\ast)$. The terms of $Q$ agree. $\square$

By induction over the levels with Lemma 3, starting from $H = G$ and the singletons, the following holds at line L2: each vertex of $H$ is a part of $P$, and for every partition of the vertices of $H$, its $Q_H$ equals $Q_G$ of the matching partition of $V$; in particular, the all-singleton partition of $H$ has $Q_H = Q_G(P)$.

**Lemma 4 (termination).** For integer weights, the run makes fewer than $8W^2$ moves in all and has at most $n$ levels.

*Proof.* For integer weights, $4W^2 Q = \sum_C (4W\,\mathrm{in}(C) - \mathrm{tot}(C)^2)$ is an integer, and $W_H = W$ at every level. By Lemma 2 and the invariant, every move raises $Q_G$ of the current partition of $V$, so it raises $4W^2 Q_G$ by at least 1, and phase 2 does not change it. Since $Q_G \ge -\sum_C (\mathrm{tot}(C)/2W)^2 \ge -1$ and $Q_G < 1$, the integer $4W^2 Q_G$ takes fewer than $8W^2$ values, which bounds the number of moves. For real weights the same holds with "finitely many", because $Q_G$ strictly increases and there are finitely many partitions of $V$. A sweep without a move ends a level, so each level ends. A level that reaches line L12 made a move, so its final partition of $H$ has $Q_H$ larger than that of the singletons of $H$; hence it is not the singleton partition and has fewer parts than $H$ has vertices. So the number of vertices of $H$ drops at every level, and there are at most $n$ levels. $\square$

**Theorem.** LOUVAIN($G$) stops. It returns a partition $P$ of $V$ such that $Q_G(P) \ge Q_G$ of every partition reached before, $Q_G(P) \ge Q_G(\text{singletons of } V)$, and no move of one vertex of the last graph $H$ (one part of $P$) into the community of another part raises $Q_G$.

*Proof.* Termination is Lemma 4. Q never drops by Lemma 2 and Lemma 3. The method returns at line L11 after a level in which nobody moved; in its last sweep, line L8 kept every vertex $v$ of $H$ in its own singleton community, so $\Delta Q(v, D) \le \Delta Q(v, \emptyset) = 0$ for every community $D$ of a neighbour, by Lemma 1 and the tie rule. With the partition of $H$ into singletons, these are exactly the single moves of a part of $P$ into a neighbouring part, and by the invariant they do not raise $Q_G$. A move of a part into a part with no edge to it has $k_{v,D} = 0$, so its gain is at most 0 as well. $\square$

∎
