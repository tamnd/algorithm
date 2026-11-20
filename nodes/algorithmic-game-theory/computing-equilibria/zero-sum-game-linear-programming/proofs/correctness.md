---
title: The LP of a matrix game gives its value and optimal strategies for both players
proves: [correctness]
status: full
---

Let $M$ be an $m \times n$ matrix, let $k = 1 - \min_{i,j} M_{ij}$ (line L1) and let $M'_{ij} = M_{ij} + k$ (line L2), so $M'_{ij} \ge 1$ for all $i$ and $j$. Write (P) for the LP of lines L3 to L5 and (D) for its dual.

**Lemma 1 (the shift).** For $x \in \Delta_m$ and $y \in \Delta_n$, $x^{\mathsf T} M' y = x^{\mathsf T} M y + k$.

*Proof.* $x^{\mathsf T} M' y = \sum_{i,j} x_i y_j (M_{ij} + k) = x^{\mathsf T} M y + k \left(\sum_i x_i\right)\left(\sum_j y_j\right) = x^{\mathsf T} M y + k$. $\square$

**Lemma 2 (the dual).** The dual of (P) is (D): minimize $w$ subject to $\sum_j M'_{ij} y_j \le w$ for each $i$, $\sum_j y_j \ge 1$, $y \ge 0$, $w$ free.

*Proof.* (P) is: maximize $c^{\mathsf T} z$ over $z = (x, v) \ge 0$ subject to $v - \sum_i M'_{ij} x_i \le 0$ for each $j$ and $\sum_i x_i = 1$, with $c = (0, \ldots, 0, 1)$. The dual of a maximization in this form has one variable $y_j \ge 0$ per inequality, one free variable $w$ per equation, objective $\min (0 \cdot y + 1 \cdot w)$, and one constraint $\ge c_\ell$ per primal variable $z_\ell$. For the variable $x_i$ the constraint is $-\sum_j M'_{ij} y_j + w \ge 0$. For $v$ it is $\sum_j y_j \ge 1$. $\square$

**Lemma 3 (both LPs have optimal solutions).** (P) is feasible: $x = (1, 0, \ldots, 0)$ and $v = 0$ satisfy every constraint, because $M' \ge 1 > 0$. (P) is bounded: for every feasible point, $v \le \sum_i x_i M'_{i1} \le \max_i M'_{i1}$. By the fundamental theorem of linear programming, (P) has an optimal basic solution, and the simplex method with Bland's rule finds one in a finite number of pivots. By strong duality, (D) has an optimal solution $(y^*, w^*)$ with $w^* = v^*$.

**Lemma 4 ($y^*$ is a mixed strategy).** $\sum_j y^*_j = 1$.

*Proof.* For any $x \in \Delta_m$, the point $(x, v)$ with $v = \min_j (x^{\mathsf T} M')_j$ is feasible, and this minimum is at least 1 because $M' \ge 1$. So $v^* \ge 1 > 0$. By complementary slackness, a primal variable that is positive at an optimum has a tight dual constraint at every dual optimum. The variable $v$ is positive, so its dual constraint $\sum_j y^*_j \ge 1$ holds with equality. Also $y^* \ge 0$, so $y^* \in \Delta_n$. $\square$

**Theorem.** Let $(x^*, v^*)$ be optimal for (P) and $(y^*, w^*)$ optimal for (D), as in line L6, and let $v = v^* - k$ (line L7). Then $x^* \in \Delta_m$, $y^* \in \Delta_n$, and

$$\min_j (x^{*\mathsf T} M)_j = v = \max_i (M y^*)_i .$$

So $v$ is the value of the game, $x^*$ is an optimal (maximin) strategy of the row player, $y^*$ is an optimal (minimax) strategy of the column player, and $(x^*, y^*)$ is a Nash equilibrium of the bimatrix game $(M, -M)$.

*Proof.* The constraints of (P) give $x^* \ge 0$ and $\sum_i x^*_i = 1$, so $x^* \in \Delta_m$, and Lemma 4 gives $y^* \in \Delta_n$.

Primal feasibility gives $(x^{*\mathsf T} M')_j \ge v^*$ for every column $j$. Dual feasibility gives $(M' y^*)_i \le w^* = v^*$ for every row $i$. Apply Lemma 1 with $y = e_j$ (column $j$ as a pure strategy) and with $x = e_i$: $(x^{*\mathsf T} M)_j = (x^{*\mathsf T} M')_j - k \ge v$ and $(M y^*)_i = (M' y^*)_i - k \le v$. Hence $\min_j (x^{*\mathsf T} M)_j \ge v \ge \max_i (M y^*)_i$.

For the reverse, $x^{*\mathsf T} M y^*$ is an average of the entries of $x^{*\mathsf T} M$ with the weights $y^*$, so $x^{*\mathsf T} M y^* \ge \min_j (x^{*\mathsf T} M)_j$; and it is an average of the entries of $M y^*$ with the weights $x^*$, so $x^{*\mathsf T} M y^* \le \max_i (M y^*)_i$. Together with the chain above, all these numbers are equal to $v$.

For any $x \in \Delta_m$, $x^{\mathsf T} M y^* \le \max_i (M y^*)_i = v$, so no strategy of the row player earns more than $v$ against $y^*$; for any $y \in \Delta_n$, $x^{*\mathsf T} M y \ge v$. So $\max_x \min_y x^{\mathsf T} M y \ge v \ge \min_y \max_x x^{\mathsf T} M y$, and the general inequality $\max_x \min_y \le \min_y \max_x$ makes both equal to $v$. In the game $(M, -M)$, no pure deviation of the row player gains against $y^*$ and no pure deviation of the column player gains against $x^*$, and checking pure deviations is enough because a payoff that is linear in a player's own mixed strategy is maximized at a pure strategy. $\blacksquare$

**Termination.** The LP has finitely many bases. Bland's rule never visits a basis twice (Bland 1977), so each phase of the simplex method ends after at most as many pivots as there are bases, a fixed finite number for the given $m$ and $n$. The algorithm has no loop of its own.
