---
title: The grid search returns only Hylland-Zeckhauser equilibria and stops
proves: [correctness, termination]
status: full
---

This proof is about the toy on the page. It shows that every answer of the grid search is an equilibrium, that the search finds one whenever some equilibrium has its normalized prices on the grid, and that it stops. It does not prove that an equilibrium exists, which is the theorem of Hylland and Zeckhauser (1979), and it does not prove Pareto efficiency.

Fix $n$ agents and $n$ objects and utilities $u_{ij} \ge 0$. Let $\Delta = \{y \in \mathbb{R}^n : y \ge 0,\ \sum_j y_j = 1\}$. For prices $p \ge 0$ the budget set is $B(p) = \{y \in \Delta : p \cdot y \le 1\}$. A pair $(p, x)$ is an equilibrium when (1) every row $x_i$ is in $\Delta$ and every column of $x$ sums to 1, (2) $x_i \in B(p)$ and $u_i \cdot x_i = \max_{y \in B(p)} u_i \cdot y$, and (3) $p \cdot x_i \le p \cdot y$ for every $y \in B(p)$ with $u_i \cdot y = u_i \cdot x_i$.

**Claim 1 (the demand values exist).** If some price is at most 1, then $B(p)$ is a nonempty compact polytope, and the values $U_i = \max_{y \in B(p)} u_i \cdot y$ and $C_i = \min \{ p \cdot y : y \in B(p),\ u_i \cdot y = U_i \}$ exist. Every grid vector of line L1 has a price 0, so lines L3 and L4 are always feasible. *Proof.* If $p_j \le 1$, the unit vector $e_j$ is in $B(p)$. $B(p)$ is a closed subset of the compact set $\Delta$, defined by finitely many linear constraints. A linear function attains its maximum on a nonempty polytope, so $U_i$ exists, and the set of maximizers is a nonempty polytope, on which $p \cdot y$ attains its minimum $C_i$. $\square$

**Claim 2 (the demand set is a face).** Let $D_i(p) = \{y \in \Delta : u_i \cdot y = U_i,\ p \cdot y = C_i\}$. A row $y$ satisfies conditions 2 and 3 for agent $i$ exactly when $y \in D_i(p)$. *Proof.* If $y$ satisfies 2 and 3, then $y \in \Delta$, $u_i \cdot y = U_i$, and $y$ is a cheapest maximizer, so $p \cdot y = C_i$. Conversely, let $y \in D_i(p)$. Then $p \cdot y = C_i \le 1$, because $C_i$ is the cost of a point of $B(p)$, so $y \in B(p)$. Its utility is $U_i$, the maximum, so condition 2 holds. Every maximizer in $B(p)$ costs at least $C_i = p \cdot y$, so condition 3 holds. $\square$

**Claim 3 (soundness).** If the search returns $(p, x)$, then $(p, x)$ is an equilibrium. *Proof.* Line L5 returns $x \ge 0$ with $\sum_j x_{ij} = 1$, $u_i \cdot x_i = U_i$ and $p \cdot x_i = C_i$ for every $i$, and $\sum_i x_{ij} = 1$ for every $j$. So every row is in $D_i(p)$, which gives conditions 2 and 3 by Claim 2, and the row and column sums give condition 1. $\square$

**Claim 4 (normalization).** If $(p, x)$ is an equilibrium, then there is an equilibrium $(p', x)$ with the same allocation and $\min_j p'_j = 0$. *Proof.* Let $m = \min_j p_j$. Every row $x_i$ is in $B(p)$, so $m \le p \cdot x_i \le 1$. If $m = 0$, take $p' = p$. If $0 < m < 1$, let $p' = (p - m \mathbf{1})/(1 - m)$, so $p' \ge 0$ and $\min_j p'_j = 0$. For $y \in \Delta$ we have $p' \cdot y = (p \cdot y - m)/(1 - m)$, because $\sum_j y_j = 1$. This map is increasing in $p \cdot y$ and sends 1 to 1, so $B(p') = B(p)$, and it orders the costs of the bundles in $\Delta$ in the same way. So conditions 2 and 3 hold for $p'$ when they hold for $p$, and condition 1 does not depend on the prices. If $m = 1$, then every row costs at least 1 and at most 1, so $x_{ij} > 0$ only for $p_j = 1$. Every column sums to 1, so every object $j$ has some $x_{ij} > 0$, and all prices are 1. Then $B(p) = \Delta$ and every bundle costs 1. Take $p' = 0$: again $B(p') = \Delta$ and every bundle costs 0, so conditions 2 and 3 hold for the same rows. $\square$

**Claim 5 (grid completeness).** If some equilibrium $(p, x)$ has $\min_j p_j = 0$ and every $p_j$ in $\{0, 1/k, \dots, \text{pmax}\}$, then the search does not return none. *Proof.* The loop of line L1 reaches $p$ unless it returned earlier. At $p$, every row $x_i$ satisfies conditions 2 and 3, so $x_i \in D_i(p)$ by Claim 2, and $x$ is a feasible point of the linear program of line L5. So line L6 returns. $\square$

By Claim 4, every equilibrium allocation has a price vector with smallest entry 0, so restricting line L1 to such vectors only loses equilibria whose normalized prices are off the grid. Such equilibria exist: an instance can have only irrational equilibrium prices (Vazirani and Yannakakis 2021). So an answer of none does not mean that no equilibrium exists.

**Termination.** The grid has $(k \cdot \text{pmax} + 1)^n$ vectors, so line L1 runs a finite number of times. Each pass solves $2n + 1$ linear programs, and the exact simplex method with Bland's rule never repeats a basis, so each one stops. So the search stops.

**The checker.** The function `is_equilibrium` computes $U_i$ and $C_i$ by Claim 1 (it first rejects negative prices and price vectors whose smallest entry is above 1, for which $B(p)$ is empty), and accepts exactly when every row is in $\Delta$, every column sums to 1, and every row has utility $U_i$ and cost $C_i$. By Claim 2 this is exactly conditions 1 to 3. All values are exact rationals, so the comparisons are exact.

**Envy-freeness of every answer.** For an equilibrium $(p, x)$ and agents $i, k$, the row $x_k$ is in $B(p)$, so $u_i \cdot x_i = U_i \ge u_i \cdot x_k$. $\blacksquare$
