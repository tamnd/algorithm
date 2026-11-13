---
title: HPA* returns a valid path whose cost is at most the optimum plus twice the gap for each border crossing
proves: [correctness, termination]
status: full
---

We use the pseudocode and the model of the page: a 4-connected grid of free and blocked cells with unit move costs, square clusters of side $c$ (the clusters at the right and bottom edges can be smaller), and one level of abstraction. A *crossing* of a grid path is a move between two cells in different clusters. Let $C^*$ be the length of a shortest grid path from $s$ to $t$.

An *entrance* is a maximal run of pairs $(a_1, b_1), \dots, (a_L, b_L)$ along one border segment between two clusters $A$ and $B$, where $a_i \in A$ and $b_i \in B$ are neighbours, both are free, and consecutive pairs are next to each other along the border. Line L4 chooses the middle pair $L / 2$ (rounded down, counting from 0) when $L < 6$, and the two end pairs otherwise. The *gap* of the abstraction is the largest distance, counted in pairs along the border, from a pair of an entrance to the nearest chosen pair of that entrance.

**Lemma 1 (the gap).** The gap is at most $\max(2, \lfloor (c - 1)/2 \rfloor)$.

*Proof.* An entrance has $L \le c$ pairs, because a border segment has at most $c$ pairs. If $L < 6$, the middle index $m = \lfloor L/2 \rfloor$ is at distance at most $\max(m, L - 1 - m) = m \le 2$ from each index. If $L \ge 6$, the index $i$ is at distance $\min(i, L - 1 - i) \le \lfloor (L - 1)/2 \rfloor \le \lfloor (c - 1)/2 \rfloor$ from an end. $\square$

**Lemma 2 (abstract edges are real paths).** For each edge of weight $w$ between abstract nodes $u$ and $v$, including the edges that line L8 adds for $s$ and $t$, there is a grid path from $u$ to $v$ of length $w$, and line L11 produces one.

*Proof.* An edge between nodes in different clusters comes from line L5, so it joins the two neighbouring free cells of a chosen pair and has weight 1. Line L11 adds the single move. Every other edge joins two cells of one cluster, and its weight is the breadth-first distance inside that cluster (lines L6, L7 and L8). Breadth-first search inside the cluster from $u$ gives a path of that length to $v$, and the distance is symmetric because the moves are symmetric. Line L11 follows the parents of this search from $v$ back to $u$. $\square$

**Lemma 3 (the search on the abstract graph).** The heuristic $h(u) = |u_x - t_x| + |u_y - t_y|$ is consistent on the abstract graph, so line L9 returns an abstract path of least weight from $s$ to $t$ if one exists.

*Proof.* By Lemma 2 an edge of weight $w$ from $u$ to $v$ is a grid path of length $w$, and each move changes the Manhattan distance to $t$ by at most 1, so $h(u) \le w + h(v)$. Also $h(t) = 0$. The rest is the optimality of [A*](/a-star-search/) with a consistent heuristic on a finite graph with positive weights. $\square$

**Lemma 4 (rerouting).** Let $P$ be any shortest grid path from $s$ to $t$, with $X$ crossings. Then the abstract graph with $s$ and $t$ inserted has a path from $s$ to $t$ of weight at most $C^* + 2 \cdot \mathrm{gap} \cdot X$.

*Proof.* Take a crossing of $P$, a move from $a_i$ to $b_i$. The two cells are free and neighbours across a border, so the pair $(a_i, b_i)$ belongs to an entrance. Let $(a_k, b_k)$ be its nearest chosen pair, with $\delta = |i - k| \le \mathrm{gap}$. Replace the move by the walk $a_i, \dots, a_k$ along the border on the side of $A$, the move to $b_k$, and the walk $b_k, \dots, b_i$ on the side of $B$. All these cells are free because they belong to the entrance, the first walk stays in $A$ and the last walk stays in $B$. The walk has length $2\delta + 1$ instead of 1. Do this for every crossing and call the result $P'$. Its length is at most $C^* + 2 \cdot \mathrm{gap} \cdot X$, and its crossings are exactly the moves of chosen pairs.

Cut $P'$ at its crossings. Between two consecutive crossings, and before the first and after the last, $P'$ makes only moves inside one cluster. So $P'$ is $s \leadsto p_1 \to q_1 \leadsto p_2 \to q_2 \leadsto \dots \to q_X \leadsto t$, where each $p_j \to q_j$ is the move of a chosen pair and each $\leadsto$ stays in one cluster. Each $p_j$ and $q_j$ is an abstract node and each move $p_j \to q_j$ is an edge of weight 1 (line L5). A part $q_j \leadsto p_{j+1}$ inside one cluster has length at least the breadth-first distance inside the cluster, which is the weight of the edge of lines L6 and L7, or 0 if $q_j = p_{j+1}$. The first part $s \leadsto p_1$ and the last part $q_X \leadsto t$ have the edges of line L8, of weight at most their lengths. If $X = 0$, the path stays in the cluster of $s$, which is also the cluster of $t$, and line L8 adds the edge from $s$ to $t$ of weight at most $C^*$. In all cases the abstract path has weight at most the length of $P'$. $\square$

**Theorem 5 (correctness and the bound).** HPA* stops. If $t$ can be reached from $s$ on the grid, it returns a grid path from $s$ to $t$ whose length equals the returned cost, and
$$ C^* \le \mathrm{cost} \le C^* + 2 \cdot \mathrm{gap} \cdot X \le C^* + 2 \max\bigl(2, \lfloor (c-1)/2 \rfloor\bigr) X $$
for every shortest grid path with $X$ crossings. If $t$ cannot be reached, it returns no path.

*Proof.* The preprocessing makes finitely many searches on a finite grid, the abstract graph is finite with positive weights, so A* in line L9 stops, and the refinement in line L11 has one finite piece for each abstract edge. If $t$ can be reached, Lemma 4 gives an abstract path, so by Lemma 3 line L9 finds one of least weight $W \le C^* + 2 \cdot \mathrm{gap} \cdot X$. By Lemma 2 its refinement is a grid path of length $W$, so it is no shorter than $C^*$. The last inequality is Lemma 1. If $t$ cannot be reached, an abstract path would give a grid path by Lemma 2, so there is none, A* empties its open list, and line L10 returns no path. $\square$

**Remarks.** The bound is tight: on the open 10 by 10 grid of the page with $c = 5$, the gap is 2, the shortest path has one crossing and length 9, and HPA* returns a path of length $13 = 9 + 2 \cdot 2 \cdot 1$. The refined path is not smoothed here. Smoothing can only make it shorter, and it stays a valid path if each shortcut is checked on the grid. The proof uses that every crossing of a shortest path belongs to an entrance and that each entrance has a transition, so the same argument works for other rules that choose at least one transition per entrance, with the gap of that rule.
