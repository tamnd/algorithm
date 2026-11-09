---
title: The dual simplex method keeps dual feasibility and returns a correct answer
proves: [correctness]
status: full
---

**Statement.** Let $A \in \mathbb{Q}^{m \times n}$ have rank $m$, and let $B$ be a dual feasible basis: $A_B$ is nonsingular and $r = c - A^\top y \ge 0$ for $y = A_B^{-\top} c_B$. Run DUAL-SIMPLEX$(A, b, c, B)$.

1. Each basis of the run is dual feasible, and $b^\top y$ never decreases from one basis to the next.
2. If it returns OPTIMAL$(x, y)$, then $x$ and $y$ are optimal for the primal and the dual, with $c^\top x = b^\top y$.
3. If it returns INFEASIBLE$(z)$, then $A^\top z \le 0$ and $b^\top z > 0$, so the primal program is infeasible.
4. If no basis repeats, the run stops after at most $\binom{n}{m}$ pivots.

**Step 1 (one pivot).** Let $B$ be dual feasible, $p$ a row with $x_{B(p)} < 0$, $g$ row $p$ of $A_B^{-1}$, $\alpha = g A$ (so $\alpha_{B(p)} = 1$ and $\alpha_{B(i)} = 0$ for $i \ne p$), and $q$ the column of line L7, with $\alpha_q < 0$. Let $\delta = r_q / (-\alpha_q) \ge 0$ and $y' = y - \delta g^\top$. Then for every $j$,

$$r'_j := c_j - y'^\top A_j = r_j + \delta\, g A_j = r_j + \delta \alpha_j.$$

So $r'_q = r_q + \delta \alpha_q = 0$. For $i \ne p$, $r'_{B(i)} = 0 + \delta \cdot 0 = 0$. Let $B'$ be $B$ with $B(p)$ replaced by $q$. Since $A_B^{-1} A_q$ has entry $\alpha_q \ne 0$ in row $p$, the columns of $B'$ are independent, so $B'$ is a basis, and $y'$ satisfies $A_{B'}^\top y' = c_{B'}$. Hence $y'$ is the dual vector of $B'$ and $r'$ its vector of reduced costs.

Dual feasibility: if $\alpha_j \ge 0$, then $r'_j = r_j + \delta \alpha_j \ge r_j \ge 0$. If $\alpha_j < 0$, then line L7 gives $\delta \le r_j / (-\alpha_j)$, so $r'_j = r_j - \delta(-\alpha_j) \ge 0$. So $B'$ is dual feasible.

The dual value: $b^\top y' = b^\top y - \delta\, g b = b^\top y - \delta x_{B(p)} \ge b^\top y$, since $\delta \ge 0$ and $x_{B(p)} < 0$. It rises strictly if and only if $\delta > 0$. This proves claim 1 by induction on the number of pivots.

**Step 2 (claim 2).** Line L3 returns when $x_B \ge 0$, so $x$ is primal feasible. By Step 1, $y$ is dual feasible. And $c^\top x = c_B^\top x_B = c_B^\top A_B^{-1} b = y^\top b$. For each primal feasible $x'$, $c^\top x' \ge y^\top A x' = y^\top b = c^\top x$, using $x' \ge 0$ and $c - A^\top y \ge 0$. For each dual feasible $y''$, $b^\top y'' = x^\top A^\top y'' \le x^\top c = b^\top y$. So both are optimal.

**Step 3 (claim 3).** Line L6 returns when $\alpha = gA \ge 0$ and $g b = x_{B(p)} < 0$. With $z = -g^\top$, $A^\top z = -\alpha^\top \le 0$ and $b^\top z = -x_{B(p)} > 0$. If some $x \ge 0$ had $Ax = b$, then $0 < b^\top z = x^\top A^\top z \le 0$, which is false.

**Step 4 (claim 4).** Each basis of the run is a set of $m$ of the $n$ columns, and there are at most $\binom{n}{m}$ of them. If none repeats, there are at most $\binom{n}{m} - 1$ pivots. A repeated basis needs a cycle of pivots, all with $\delta = 0$, since $b^\top y$ never decreases and is a function of the basis. $\blacksquare$

**Remark.** If every pivot has $\delta > 0$ (no dual degeneracy), then no basis repeats, and the run stops. In general the dual analogues of Bland's rule and of the lexicographic rule prevent cycling; this proof does not cover them. The implementation reports a repeated basis as the status "cycle", and the tests check that the least-index rule never reaches it on the random programs.
