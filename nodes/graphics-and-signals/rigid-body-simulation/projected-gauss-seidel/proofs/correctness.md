---
title: Projected Gauss-Seidel converges for a symmetric positive definite matrix with fixed bounds, and sequential impulses compute the same iterates
proves: [correctness, termination]
status: full
---

The input is a symmetric $n \times n$ matrix $A$ with $A_{ii} > 0$, a vector $b$, and bounds $lo_i \le hi_i$ (with $lo_i = -\infty$ or $hi_i = +\infty$ allowed). Write $B = \prod_i [lo_i, hi_i]$ for the box, $w = A\lambda + b$, and

$$q(\lambda) = \tfrac12 \lambda^T A \lambda + b^T \lambda.$$

The target is a point $\lambda \in B$ with $w_i \ge 0$ where $\lambda_i = lo_i < hi_i$, $w_i \le 0$ where $\lambda_i = hi_i > lo_i$, and $w_i = 0$ where $lo_i < \lambda_i < hi_i$. Call this the box condition. Line numbers refer to the pseudocode of the page.

**Termination.** The loops of lines L2 and L3 run a fixed number $K$ of sweeps over $n$ rows, and each update (lines L4 to L6) is a finite computation. So the algorithm stops after $K n$ updates, whatever the input. The rest of this note is about what the iterates approach.

**Lemma 1 (one update solves its row).** Fix all coordinates except $\lambda_i$. Line L6 sets $\lambda_i$ to the minimizer of $q$ over $\lambda_i \in [lo_i, hi_i]$. The new value satisfies the box condition for row $i$.

*Proof.* As a function of $\lambda_i$ alone, $q = \tfrac12 A_{ii} (\lambda_i - x^*)^2 + \text{const}$, with $x^* = \lambda_i - r / A_{ii}$, where $r = w_i$ is the value of line L4. A convex parabola has its minimum over an interval at the projection of its vertex, which is $\text{clamp}(x^*, lo_i, hi_i)$. After the update, $w_i = A_{ii}(\lambda_i - x^*)$. If the clamp did not act, $w_i = 0$; if $\lambda_i = lo_i > x^*$, then $w_i > 0$; if $\lambda_i = hi_i < x^*$, then $w_i < 0$. $\square$

**Lemma 2 (sufficient decrease).** If $\lambda_i \in [lo_i, hi_i]$ before the update and $\delta$ is the change of $\lambda_i$, then $q$ decreases by at least $\tfrac12 A_{ii} \delta^2$.

*Proof.* Let $x$ be the old value, $y = \text{clamp}(x^*)$ the new one. Since $y$ is the projection of $x^*$ onto the interval and $x$ is in the interval, $(x - y)(x^* - y) \le 0$. Hence $(x - x^*)^2 = (x - y)^2 + (y - x^*)^2 - 2(x - y)(x^* - y) \ge (x - y)^2 + (y - x^*)^2$. The decrease of $q$ is $\tfrac12 A_{ii} [(x - x^*)^2 - (y - x^*)^2] \ge \tfrac12 A_{ii} (x - y)^2$. $\square$

After the first update of row $i$, $\lambda_i$ stays in its interval, so Lemma 2 applies to every later update of that row. If $\lambda^0 \in B$, it applies to every update.

**Lemma 3 (the box condition is the optimality condition).** Let $A$ be symmetric positive semidefinite. A point $\lambda \in B$ satisfies the box condition if and only if it minimizes $q$ over $B$.

*Proof.* $q$ is convex, and $B$ is a box, so $\lambda$ is a minimizer exactly when no feasible direction decreases $q$, that is, when $\nabla q(\lambda)^T (\mu - \lambda) \ge 0$ for all $\mu \in B$. Since $\nabla q = w$ and $B$ is a product of intervals, this splits into one condition per coordinate: $w_i (\mu_i - \lambda_i) \ge 0$ for all $\mu_i \in [lo_i, hi_i]$. This holds if and only if $w_i = 0$ for an interior $\lambda_i$, $w_i \ge 0$ at $lo_i$, and $w_i \le 0$ at $hi_i$. These are the [KKT conditions](/kkt-conditions/) of the box-constrained program. $\square$

**Theorem 1 (convergence for a positive definite matrix).** Let $A$ be symmetric positive definite, $B$ nonempty, and $\lambda^0 \in B$. Then the iterates of projected Gauss-Seidel converge to the unique point $\lambda^*$ that satisfies the box condition.

*Proof.* $q$ is strictly convex and $q(\lambda) \ge \tfrac12 \sigma |\lambda|^2 - |b| |\lambda|$, where $\sigma > 0$ is the smallest eigenvalue of $A$. So $q$ has a unique minimizer $\lambda^*$ over the closed set $B$, and its sublevel sets are bounded. By Lemma 3, $\lambda^*$ is the only point with the box condition.

Let $\lambda^{k,i}$ be the iterate after the update of row $i$ in sweep $k$. By Lemma 2, $q$ never increases, so all iterates lie in the bounded set $\{q \le q(\lambda^0)\}$, and $q$ converges to a limit $\bar q$. Summing Lemma 2 over all updates gives $\sum \tfrac12 A_{ii} \delta^2 \le q(\lambda^0) - \bar q < \infty$, so the changes $\delta$ tend to zero. Take any limit point $\bar\lambda$ of the end-of-sweep iterates $\lambda^{k,n}$, along a subsequence $k_m$. Since the changes in one sweep tend to zero, $\lambda^{k_m, i} \to \bar\lambda$ for every $i$ as well. The update of row $i$ is $\lambda^{k,i}_i = \text{clamp}(\lambda^{k,i-1}_i - w_i(\lambda^{k,i-1}) / A_{ii}, lo_i, hi_i)$, and clamp and $w$ are continuous, so in the limit $\bar\lambda_i = \text{clamp}(\bar\lambda_i - w_i(\bar\lambda)/A_{ii}, lo_i, hi_i)$. By the argument of Lemma 1, this fixed point equation is the box condition for row $i$. It holds for every $i$, so $\bar\lambda = \lambda^*$. A bounded sequence whose only limit point is $\lambda^*$ converges to $\lambda^*$. $\square$

For contact without friction, $lo_i = 0$ and $hi_i = +\infty$, and the box condition is the linear complementarity problem $\lambda \ge 0$, $w \ge 0$, $\lambda^T w = 0$. Theorem 1 is the classical convergence result for projected iterative methods on symmetric LCPs (Cottle, Pang and Stone treat these methods; Catto 2005, Section 7.2, cites them for convergence when the matrix is positive definite).

**Theorem 2 (sequential impulses compute the same iterates).** Let $A = J M^{-1} J^T$ and $b = J v^0 + \text{bias}$, where $J$ has one row per constraint and $M$ is the mass matrix. Run the matrix-free version: keep body velocities $v$, start with $v = v^0 + M^{-1} J^T \lambda^0$, and for each row compute $r = J_i v + \text{bias}_i$, set $\lambda_i^{new} = \text{clamp}(\lambda_i - r / K_{ii})$ with $K_{ii} = J_i M^{-1} J_i^T$, and apply the impulse change $(\lambda_i^{new} - \lambda_i) J_i^T$ to $v$. In exact arithmetic it produces the same sequence of $\lambda$ as the matrix version, with the same bounds and the same row order.

*Proof.* The invariant is $v = v^0 + M^{-1} J^T \lambda$. It holds at the start by construction, and an update that changes $\lambda_i$ by $\delta$ changes $v$ by $M^{-1} J_i^T \delta$, which keeps it. Under the invariant, $J_i v + \text{bias}_i = J_i v^0 + \text{bias}_i + (J M^{-1} J^T \lambda)_i = b_i + (A \lambda)_i$, which is the $r$ of line L4, and $K_{ii} = A_{ii}$. The bounds of line L5 depend only on $\lambda$, so they agree as well. By induction over the updates, both versions make the same change at every step. $\square$

The invariant needs the clamp on the total $\lambda_i$, as in line L6. A version that clamps each increment, for example $\delta \ge 0$ for a normal row, keeps $v = v^0 + M^{-1} J^T \lambda$ but solves a different problem: no impulse can ever decrease, and the limit may violate the box condition (the tipping box of the page).

**Corollary (positive semidefinite matrices: the velocities agree).** If $A$ is only positive semidefinite and $b = J v^0 + J z$ for some $z$ (always true when the bias is zero or lies in the range of $J$), every point with the box condition gives the same $w = A \lambda + b$, so the same constrained relative velocities. *Proof.* As in Theorem 3 of the proof for [Baraff's algorithm](/baraff-contact-force-algorithm/): two minimizers $\lambda, \mu$ of the convex $q$ over the convex set $B$ satisfy $(\lambda - \mu)^T A (\lambda - \mu) = 0$, so $A \lambda = A \mu$. $\square$

**What is not proved.** For a singular $A$ (redundant contacts) this note does not prove that the iterates converge; the velocities of all solutions agree, and the tests measure convergence of $w$. For box friction, where the bounds $\pm \mu \lambda_n$ move with the normal impulse, the problem is not the optimality condition of a symmetric program, and convergence is not proved. No rate of convergence is proved here: the rate depends on the matrix, and on the page it is measured, not derived, except for the two-contact example, where it is computed exactly. Warm starting is a heuristic: it changes $\lambda^0$, and Theorem 1 holds for any $\lambda^0 \in B$.
