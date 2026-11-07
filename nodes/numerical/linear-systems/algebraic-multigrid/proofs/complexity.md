---
title: Cost of an AMG V-cycle
proves: [time.per_cycle, space.extra]
status: full
---

Assume the coarsest level has at most a fixed number $n_{\min}$ of unknowns, so its dense solve costs $O(n_{\min}^3) = O(1)$, and every row of every $A_l$ has a nonzero diagonal, so $n_l \le z_l$.

**Level $l$, not the coarsest.** A Gauss-Seidel sweep visits every off-diagonal nonzero once with one multiplication and one subtraction, and divides once per row: $2(z_l - n_l) + n_l \le 2 z_l$ flops. There are $\nu$ sweeps. The residual of line L4 costs $2 z_l$ flops. Restriction (line L5) and prolongation (line L7) cost $2 \operatorname{nnz}(P_l)$ each. A C row of $P_l$ has one entry; an F row $i$ has entries only for $j \in C \cap S_i$, a subset of the off-diagonal nonzeros of row $i$ of $A_l$. So $\operatorname{nnz}(P_l) \le n_l + z_l \le 2 z_l$. The level costs at most $(2\nu + 2) z_l + 8 z_l = (2\nu + 10) z_l$ flops.

**All levels.** Each level is visited once per V-cycle, so the total is at most $(2\nu + 10) \sum_l z_l + O(1) = (2 \nu + 10) c z + O(1)$, which is $O(\nu c z)$ time since $\nu \ge 1$ and the remaining bookkeeping is $O(\sum_l n_l) \le O(c z)$.

**Space.** The hierarchy stores $\sum_l z_l = c z$ matrix entries and $\sum_l \operatorname{nnz}(P_l) \le 2 c z$ interpolation weights; the recursion keeps one residual and one correction per level, $O(\sum_l n_l) = O(c z)$. In total $O(c z)$. $\blacksquare$
