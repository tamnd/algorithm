---
title: The recovered features are maximal rectangles in the delta area, their union is the delta area, the stock minus them is the part, and their number is minimum
proves: [correctness, termination]
status: full
---

We use the notation and the pseudocode of the page. $P$ is a closed region bounded by a simple rectilinear polygon with integer vertices. Since the polygon is simple, $P$ is regular, so $P = \overline{\operatorname{int} P}$. Let $x_0 < \dots < x_a$ and $y_0 < \dots < y_b$ be the distinct vertex coordinates (line L1), and let $W = [x_0, x_a] \times [y_0, y_b]$ be the bounding box. The grid lines are the lines $x = x_i$ and $y = y_j$, and $G$ is their union restricted to $W$. The open cell $(i, j)$ is $C_{ij} = (x_i, x_{i+1}) \times (y_j, y_{j+1})$. The delta area is
$$D = W -^* P = \overline{\operatorname{int}(W \setminus P)}.$$
For a set $S$ of cells we write $|S| = \overline{\bigcup_{(i,j) \in S} C_{ij}}$.

**Lemma 1 (cells are pure).** Each open cell lies in $\operatorname{int} P$ or in $\mathbb{R}^2 \setminus P$, and line L2 puts it in $D$ exactly in the second case.

*Proof.* Each edge of the polygon is horizontal or vertical, and its two endpoints are vertices, so the edge lies on a grid line. Hence $\partial P \subseteq G$, and an open cell $C$ misses $\partial P$. Then $C = (C \cap \operatorname{int} P) \cup (C \setminus P)$ is a split of the connected set $C$ into two disjoint open sets, so one of them is empty. The centre of $C$ is not on $\partial P$, so the crossing number test decides correctly whether it is in $P$, and that decides the whole cell. $\square$

Let $S_P$ be the set of cells in $\operatorname{int} P$ and $S_D$ the rest.

**Lemma 2.** $P = |S_P|$ and $D = |S_D|$.

*Proof.* The cells and $G$ partition $W$, and $G$ is a finite union of segments, closed with empty interior. For any open set $U$, $\overline{U \setminus G} = \overline{U}$: every neighbourhood of a point of $U$ meets $U$ in a nonempty open set, which is not inside $G$. Take $U = \operatorname{int} P$. By Lemma 1, $U \setminus G = \bigcup_{S_P} C_{ij}$, so $|S_P| = \overline{\operatorname{int} P} = P$. Take $U = \operatorname{int}(W \setminus P)$, which equals $\operatorname{int} W \setminus P$. By Lemma 1, $U \setminus G = \bigcup_{S_D} C_{ij}$, so $|S_D| = \overline{U} = D$. $\square$

A *block* is $\beta = [i_0, i_1) \times [j_0, j_1)$, its cell set is $\operatorname{cells}(\beta)$, and its rectangle is $R(\beta) = [x_{i_0}, x_{i_1}] \times [y_{j_0}, y_{j_1}] = |\operatorname{cells}(\beta)|$. Line L3 keeps $\beta$ only if $\operatorname{cells}(\beta) \subseteq S_D$. Line L4 drops it if one of the four blocks that add a row or column on one side is inside the grid and has all its cells in $S_D$. Let $B$ be the list that is built.

**Lemma 3 (rectangles in $D$).** Let $R$ be a closed axis-parallel rectangle with nonempty interior. Then $R \subseteq D$ exactly when $R \subseteq W$ and every cell that meets $\operatorname{int} R$ is in $S_D$. Then the smallest block $\hat\beta$ with $R \subseteq R(\hat\beta)$ has all its cells in $S_D$.

*Proof.* Suppose $R \subseteq D$ and a cell $C$ meets $\operatorname{int} R$. Then $C \cap \operatorname{int} R$ is a nonempty open subset of $D$. If $C$ were in $S_P$, this set would lie in $\operatorname{int} P$. But $D = \overline{\operatorname{int} W \setminus P}$ meets the open set $\operatorname{int} P$ nowhere, a contradiction. Conversely, if every cell that meets $\operatorname{int} R$ is in $S_D$, then $\operatorname{int} R \setminus G$ lies in the union of $S_D$ cells, and $R = \overline{\operatorname{int} R \setminus G} \subseteq |S_D| = D$. For the second claim, the cells of $\hat\beta$ are exactly the cells whose open interval in $x$ meets the open $x$ range of $R$, and the same in $y$. Each such cell meets $\operatorname{int} R$, so it is in $S_D$. $\square$

**Lemma 4 (maximality).** For $\beta \in B$, no closed axis-parallel rectangle $R' \subseteq D$ contains $R(\beta)$ strictly.

*Proof.* Suppose $R(\beta) \subsetneq R' \subseteq D$. Then $R'$ reaches beyond $R(\beta)$ on some side, say the right, so $R' \subseteq W$ forces $i_1 < a$. Then $R'$ meets the interior of each cell $C_{i_1 j}$ for $j_0 \le j < j_1$, since it contains a strip $[x_{i_1}, x_{i_1} + \epsilon] \times [y_{j_0}, y_{j_1}]$ for some $\epsilon > 0$. By Lemma 3, those cells are in $S_D$, so the block grown by one column on the right has all its cells in $S_D$, and line L4 would have dropped $\beta$. The other three sides are the same. $\square$

**Lemma 5 (the search).** MIN-COVER$(S_D, B)$ returns a subfamily of $B$ whose cells cover $S_D$, and no smaller subfamily of $B$ covers $S_D$.

*Proof.* Every block of $B$ that contains a given cell of $S_D$ lies in $B$, and each $S_D$ cell lies in some block of $B$: the one-cell block of that cell is in $S_D$, and growing it one row or column at a time while it stays in $S_D$ ends at a block of $B$, because the grid is finite. So the initial value $B$ of best is a cover. A call SEARCH(chosen, covered) keeps covered $= \bigcup_{b \in \text{chosen}} \operatorname{cells}(b)$. It sets best only when every cell is covered, so best is always a cover. Let $F^*$ be a minimum cover of size $k^*$. We claim that unless best already has size $k^*$, the search reaches a call with chosen $\subseteq F^*$ and every cell covered. Start at the root, where chosen $= [] \subseteq F^*$. At a call with chosen $\subseteq F^*$, $|\text{chosen}| < k^*$ holds if some cell $c$ is uncovered, because $F^*$ covers $c$ and chosen does not. So the bound $|\text{chosen}| \ge |\text{best}|$ cuts only if $|\text{best}| \le |\text{chosen}| < k^*$, which is impossible for a cover, or if $|\text{best}| = k^*$ already. Otherwise some $b \in F^* \setminus \text{chosen}$ contains $c$, and line L5 recurses on chosen $+ [b] \subseteq F^*$. The size grows by one at each step, so within $k^*$ steps all cells are covered and best becomes a cover of size $|\text{chosen}| \le k^*$. Best only ever shrinks, so it ends with size $k^*$. $\square$

**Theorem.** Let $R_1, \dots, R_k$ be the rectangles returned at line L6. Then

1. each $R_i$ lies in $D$ and is maximal among axis-parallel rectangles in $D$,
2. $R_1 \cup \dots \cup R_k = D$ and $W -^* (R_1 \cup \dots \cup R_k) = P$,
3. no family of fewer closed axis-parallel rectangles has union $D$,
4. for a point $p$ on no grid line, $p \in P$ exactly when $p \in \operatorname{int} W$ and $p \notin \operatorname{int} R_i$ for every $i$.

*Proof.* (1) Each $R_i = R(\beta)$ for a block $\beta \in B$. Its cells are in $S_D$, so $R_i \subseteq |S_D| = D$ by Lemma 2, and Lemma 4 gives maximality.

(2) By Lemma 5 the blocks cover $S_D$, and they hold only $S_D$ cells. So $\bigcup_i R_i = \bigcup_i |\operatorname{cells}(\beta_i)| = |S_D| = D$, since a finite union of closures is the closure of the union. Then $W -^* D = \overline{\operatorname{int}(W \setminus D)}$. The set $\operatorname{int}(W \setminus D)$ contains every $S_P$ cell, since those are open and miss $D$. It lies in $P$: a point of $W \setminus P$ in $\operatorname{int} W$ lies in $\operatorname{int} W \setminus P \subseteq D$, and a point on $\partial W$ is not interior to $W \setminus D$. So $|S_P| \subseteq W -^* D \subseteq P$, and Lemma 2 gives equality.

(3) Let $Q_1, \dots, Q_r$ be closed axis-parallel rectangles with union $D$. Drop those with empty interior. The union of the rest is closed and contains $D \setminus G'$ for a finite union $G'$ of segments, which is dense in the regular set $D$. So it is still $D$. For each remaining $Q_t$, Lemma 3 gives a block $\hat\beta_t$ with cells in $S_D$ and $Q_t \subseteq R(\hat\beta_t)$, and growing it as in Lemma 5 gives a block $\beta_t \in B$ with $Q_t \subseteq R(\beta_t) \subseteq D$. Every $S_D$ cell $C$ is an open subset of $D$, so the finitely many closed sets $Q_t$ cover it. Then one of them meets $C$ in a set with nonempty interior, since a finite union of closed sets with empty interior in $C$ has empty interior. So $C$ meets $\operatorname{int} Q_t$, which makes it a cell of $\hat\beta_t$ and of $\beta_t$. So the blocks $\beta_t$ cover $S_D$, and by Lemma 5, $k \le r$.

(4) If $p$ is on no grid line, then $p$ lies in an open cell or outside $W$. If outside, it is neither in $P$ nor in $\operatorname{int} W$. If in cell $C$, then $p \in P$ iff $C \in S_P$ (Lemma 1). Also $p \in R_i$ iff $p \in \operatorname{int} R_i$ iff $C \in \operatorname{cells}(\beta_i)$, since $p$ is not on the boundary of any block rectangle. By (2), $C \in S_D$ iff $C$ is in some $\operatorname{cells}(\beta_i)$. So $p \in P$ iff $p \in \operatorname{int} W$ and $p$ lies in no $\operatorname{int} R_i$. $\square$

**Termination.** Line L2 and the block loop are finite loops over $O(a^2 b^2)$ blocks. In SEARCH, each recursive call adds a block whose cells include an uncovered cell, so covered grows strictly and the depth is at most $|S_D|$. The branching is at most $|B|$, so the search tree is finite.

**What is not claimed.** The theorem is about the planar case with $W$ the bounding box. It says nothing about which minimum cover is returned when there are several, or that a minimum cover is the best machining plan. The open sides of a rectangle are only the sides on $\partial W$. A rectangle with no open side, like the head of a T-slot, is correct as a set but cannot be reached along an axis. In three dimensions, the cell and cover steps are the same in principle. But the faces to extend, the number of cells and the convexity of the merged cells all need the 3D treatments of the cited papers, which this proof does not cover.
