---
title: Each step of fuzzy c-means minimizes the objective exactly over one block, so the objective does not increase
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a list of points $x_1, \ldots, x_n$ in $\mathbb{R}^d$, a number $c \ge 2$ of clusters and a fuzzifier $m > 1$. A membership matrix $U = (u_{ij})$ has $u_{ij} \ge 0$ and $\sum_{j=1}^{c} u_{ij} = 1$ for each $i$. For centers $V = (v_1, \ldots, v_c)$ the objective is

$$J_m(U, V) = \sum_{i=1}^{n} \sum_{j=1}^{c} u_{ij}^m \, D_{ij}, \qquad D_{ij} = \|x_i - v_j\|^2 = d_{ij}^2.$$

**Lemma 1 (membership step).** For fixed $V$, lines L4 to L6 give a membership matrix that minimizes $J_m(\cdot, V)$.

*Proof.* The objective is a sum over $i$ of $f_i(u_{i1}, \ldots, u_{ic}) = \sum_j u_{ij}^m D_{ij}$, and the constraints act on each row alone, so each row can be minimized on its own over the simplex $\Delta = \{u \in \mathbb{R}^c : u \ge 0, \sum_j u_j = 1\}$. Fix $i$ and write $u_j$, $D_j$.

Case 1: some $D_j = 0$. Let $Z = \{j : D_j = 0\}$. Line L5 sets $u_j = 1/|Z|$ for $j \in Z$ and $u_j = 0$ otherwise. Then every term $u_j^m D_j$ is $0$, because either $D_j = 0$ or $u_j = 0$. All terms are nonnegative for every $u \in \Delta$, so $0$ is the least value.

Case 2: all $D_j > 0$. Line L6 sets

$$u_j^\ast = \frac{1}{\sum_{l=1}^{c} (D_j / D_l)^{1/(m-1)}} = \frac{1}{\sum_{l=1}^{c} (d_j / d_l)^{2/(m-1)}} = \frac{D_j^{-1/(m-1)}}{\sum_{l} D_l^{-1/(m-1)}}.$$

These numbers are positive and sum to $1$, so $u^\ast \in \Delta$. The function $f(u) = \sum_j u_j^m D_j$ is convex on $u \ge 0$, because $t \mapsto t^m$ is convex for $m > 1$ and $D_j > 0$. Its partial derivatives at $u^\ast$ are

$$\frac{\partial f}{\partial u_j}(u^\ast) = m (u_j^\ast)^{m-1} D_j = m \Big(\sum_l D_l^{-1/(m-1)}\Big)^{-(m-1)} D_j^{-1} D_j = \lambda,$$

the same number $\lambda$ for every $j$. For a convex differentiable function, $f(u) \ge f(u^\ast) + \nabla f(u^\ast) \cdot (u - u^\ast)$ for all $u \ge 0$ (see [convex function](/convex-function/)). For $u \in \Delta$ the last term is $\lambda \sum_j (u_j - u_j^\ast) = \lambda (1 - 1) = 0$. So $f(u) \ge f(u^\ast)$ on $\Delta$. This is the condition of a [Lagrange multiplier](/lagrange-multiplier/) $\lambda$ for the constraint $\sum_j u_j = 1$. $\square$

**Lemma 2 (center step).** For fixed $U$, line L7 gives centers that minimize $J_m(U, \cdot)$. A center whose weights $u_{ij}^m$ are all $0$ does not change the objective, and the code keeps it.

*Proof.* The objective is a sum over $j$ of $g_j(v_j) = \sum_i w_{ij} \|x_i - v_j\|^2$ with $w_{ij} = u_{ij}^m \ge 0$, so each center can be found on its own. Let $W_j = \sum_i w_{ij}$. If $W_j = 0$, then $g_j = 0$ for every $v_j$. Otherwise let $\bar v_j = \sum_i w_{ij} x_i / W_j$. Expand $\|x_i - v\|^2 = \|x_i - \bar v_j\|^2 + 2 (x_i - \bar v_j) \cdot (\bar v_j - v) + \|\bar v_j - v\|^2$, multiply by $w_{ij}$ and add over $i$. The middle terms add to $2 (\sum_i w_{ij} x_i - W_j \bar v_j) \cdot (\bar v_j - v) = 0$. So $g_j(v) = g_j(\bar v_j) + W_j \|\bar v_j - v\|^2 \ge g_j(\bar v_j)$, with equality only at $v = \bar v_j$. $\square$

**Theorem (monotone objective).** Let $V^{(t)}$ be the centers at the start of pass $t$, let $U^{(t)}$ be the memberships computed from them at lines L3 to L6, and let $V^{(t+1)}$ be the centers computed from $U^{(t)}$ at line L7. Then

$$J_m(U^{(t+1)}, V^{(t+1)}) \le J_m(U^{(t)}, V^{(t+1)}) \le J_m(U^{(t)}, V^{(t)}).$$

*Proof.* The right inequality is Lemma 2 for $U = U^{(t)}$: the centers $V^{(t+1)}$ minimize $J_m(U^{(t)}, \cdot)$, so they are not worse than $V^{(t)}$. The left inequality is Lemma 1 for $V = V^{(t+1)}$: the memberships $U^{(t+1)}$ minimize $J_m(\cdot, V^{(t+1)})$, so they are not worse than $U^{(t)}$. $\square$

**Corollary (stopping and fixed points).** The values of $J_m$ after each half step form a nonincreasing sequence of nonnegative numbers, so they converge. The loop stops when the largest change of a membership is at most $\varepsilon$, or at the cap on passes. If a pass does not change $U$, then $U$ and $V$ are a fixed point of the two maps: each is optimal for the other, so $(U, V)$ satisfies the first-order conditions of $J_m$ in each block.

Bezdek (1980) used Zangwill's convergence theorem to show that every convergent subsequence of the iterates tends to such a fixed point. Bezdek, Hathaway, Sabin and Tucker (1987) showed that a fixed point can be a local minimum or a saddle point of $J_m$, so the limit is not always a local minimum. We do not prove these two results here; the page cites them. $\blacksquare$
