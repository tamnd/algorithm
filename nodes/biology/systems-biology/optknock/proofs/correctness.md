---
title: The single-level LP equals the optimistic OptKnock value for each knockout set
proves: [correctness]
status: full
---

Fix an $n \times m$ matrix $S$, bounds $lb \le ub$ (entries may be infinite), a biomass index $b$, a product index $p$, a growth floor $\mu_{\min}$, a candidate list $C$ and a limit $K$. For a knockout set $D \subseteq C$ let $lb^D, ub^D$ be the bounds with $lb^D_j = ub^D_j = 0$ for $j \in D$, and let

$$\text{(IN}_D\text{)} \qquad \max \; v_b \quad \text{subject to} \quad S v = 0, \quad lb^D \le v \le ub^D$$

be the inner FBA problem. Let $O_D$ be the set of optimal solutions of (IN$_D$), empty if (IN$_D$) is infeasible or unbounded. The optimistic OptKnock value of $D$ is

$$\phi(D) = \max \{ v_p : v \in O_D, \; v_b \ge \mu_{\min} \},$$

with $\phi(D) = -\infty$ if this set is empty. OptKnock asks for $D$ with $|D| \le K$ that maximizes $\phi(D)$. We assume that $v_p$ is bounded above on $O_D$ for each $D$; this holds, for example, when the bounds make the flux polyhedron bounded. (If it fails for some $D$, solve_lp reports "unbounded" for that $D$ and the code skips it.)

For fixed bounds $lb, ub$ (we drop the index $D$), let $U = \{j : ub_j < \infty\}$ and $L = \{j : lb_j > -\infty\}$. The dual of the inner LP is

$$\text{(DU)} \qquad \min \; \sum_{j \in U} ub_j \alpha_j - \sum_{j \in L} lb_j \beta_j \quad \text{subject to} \quad S^{\mathsf T} \lambda + \alpha - \beta = e_b, \quad \alpha, \beta \ge 0,$$

with $\lambda \in \mathbb{R}^n$ free, $\alpha_j$ present only for $j \in U$ and $\beta_j$ only for $j \in L$. single_level_lp builds the LP

$$\text{(SL)} \qquad \max \; v_p \quad \text{subject to} \quad S v = 0, \; lb \le v \le ub, \; v_b \ge \mu_{\min}, \; (\lambda, \alpha, \beta) \text{ feasible for (DU)}, \; v_b = ub^{\mathsf T} \alpha - lb^{\mathsf T} \beta .$$

**Lemma 1 (weak duality).** For every $v$ feasible for the inner LP and every $(\lambda, \alpha, \beta)$ feasible for (DU), $v_b \le ub^{\mathsf T} \alpha - lb^{\mathsf T} \beta$.

*Proof.* $v_b = e_b^{\mathsf T} v = (S^{\mathsf T} \lambda + \alpha - \beta)^{\mathsf T} v = \lambda^{\mathsf T} S v + \sum_{j \in U} \alpha_j v_j - \sum_{j \in L} \beta_j v_j$. The first term is 0. For $j \in U$, $\alpha_j \ge 0$ and $v_j \le ub_j$, so $\alpha_j v_j \le \alpha_j ub_j$. For $j \in L$, $\beta_j \ge 0$ and $v_j \ge lb_j$, so $-\beta_j v_j \le -\beta_j lb_j$. $\square$

**Lemma 2 (the projection of (SL)).** A vector $v$ is the $v$ part of a feasible point of (SL) if and only if $v \in O$ and $v_b \ge \mu_{\min}$, where $O$ is the set of optimal solutions of the inner LP.

*Proof.* Let $(v, \lambda, \alpha, \beta)$ be feasible for (SL). For any inner feasible $u$, Lemma 1 gives $u_b \le ub^{\mathsf T} \alpha - lb^{\mathsf T} \beta = v_b$. So $v$ is optimal, and $v_b \ge \mu_{\min}$ is a row of (SL). Conversely, let $v \in O$ with $v_b \ge \mu_{\min}$. The inner LP has a finite optimum, so by the strong duality theorem of linear programming, (DU) has an optimal solution $(\lambda, \alpha, \beta)$ with the same value $ub^{\mathsf T} \alpha - lb^{\mathsf T} \beta = v_b$. (The inner LP is in the form $\max \{e_b^{\mathsf T} v : S v = 0, \; v_j \le ub_j \; (j \in U), \; -v_j \le -lb_j \; (j \in L)\}$, and (DU) is its dual: $\lambda$ for the equations, $\alpha_j$ for the rows $v_j \le ub_j$, and $\beta_j$ for the rows $-v_j \le -lb_j$. A free variable $v_j$ gives the equation $(S^{\mathsf T}\lambda + \alpha - \beta)_j = (e_b)_j$.) So $(v, \lambda, \alpha, \beta)$ is feasible for (SL). $\square$

**Lemma 3 (the value for one set).** For each $D$, single_level_lp on the bounds $lb^D, ub^D$ returns "optimal" with $v_p = \phi(D)$ and some $v \in O_D$ when $\phi(D) > -\infty$, and "infeasible" when $\phi(D) = -\infty$.

*Proof.* By Lemma 2 the set of $v$ parts of the feasible points of (SL) is $\{v \in O_D : v_b \ge \mu_{\min}\}$, and the objective of (SL) is $v_p$. If this set is empty, (SL) is infeasible, and $\phi(D) = -\infty$. Otherwise the maximum of $v_p$ over it is $\phi(D)$, finite by the assumption, and attained, since $O_D$ is a polyhedron (a face of the inner polyhedron) and a linear function bounded above on a non-empty polyhedron attains its maximum. solve_lp returns the correct status and an optimum (Lemma 1 of the proof on the flux variability analysis page). The code sets the lower bound of $v_b$ in (SL) to $\max(lb_b, \mu_{\min})$, which is the same as the two rows $v_b \ge lb_b$ and $v_b \ge \mu_{\min}$. $\square$

**Theorem.** optknock returns None if $\phi(D) = -\infty$ for every $D \subseteq C$ with $|D| \le K$. Otherwise it returns $(D^*, v^*)$ with $|D^*| \le K$, $\phi(D^*) = \max_{|D| \le K} \phi(D)$, $v^* \in O_{D^*}$, $v^*_b \ge \mu_{\min}$ and $v^*_p = \phi(D^*)$.

*Proof.* Lines L2 and L3 visit every $D \subseteq C$ with $|D| \le K$ exactly once, by size and then in the order of combinations. For each, line L4 computes $\phi(D)$ and an optimal $v$ by Lemma 3, and line L5 skips the sets with $\phi(D) = -\infty$. Line L6 keeps a set with the largest $v_p$ seen so far and replaces it only on a strict increase, so at line L7 it holds a maximizer of $\phi$, the first one in the visiting order. If no set passes line L5, best stays None. $\square$

**Remark (the optimistic value).** For a fixed $D$, the inner LP may have many optimal $v$ with different $v_p$. (SL) picks the one with the largest product, so $\phi(D)$ is the best case for the engineer. The worst case $\min \{v_p : v \in O_D\}$ is also an LP of the same form with the objective reversed; it is the guaranteed product of the design. The test with one respiration route shows a set $D$ where the two values are 5 and 0.

**Remark (the MILP).** Burgard, Pharkya and Maranas write the same problem with binary variables $y_j$ ($y_j = 0$ if $j \in D$), the bounds $lb_j y_j \le v_j \le ub_j y_j$, and the dual variables of the bounds switched off by big constants when $y_j = 0$. For each fixed $y$, that MILP is the LP (SL) for the corresponding $D$, so the enumeration here and the MILP have the same optimum, provided the big constants are large enough not to cut off the optimal dual solutions.
