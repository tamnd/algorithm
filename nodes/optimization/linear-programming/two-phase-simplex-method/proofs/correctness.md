---
title: The two-phase method decides feasibility and returns a correct answer
proves: [correctness, termination]
status: full
---

**Statement.** Let $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$ and $c \in \mathbb{Q}^n$, with no assumption on the rank of $A$. TWO-PHASE$(A, b, c)$ with Bland's rule stops, and:

1. If it returns INFEASIBLE$(z)$, then $A^\top z \le 0$ and $b^\top z > 0$, so $\{x : Ax = b,\ x \ge 0\}$ is empty.
2. Otherwise the original program is feasible, and the rows that line L7 deletes are implied by the kept rows. Line L9 starts the simplex method from a feasible basis of the kept rows, and these rows have full row rank. So the answer of line L9 (optimal or unbounded) is correct for the original program.

**Setup.** Let $D$ be the diagonal matrix with $D_{ii} = -1$ if $b_i < 0$ and $D_{ii} = 1$ otherwise. Line L1 replaces $A$ by $\bar A = DA$ and $b$ by $\bar b = Db \ge 0$. Since $D$ is invertible, $\bar A x = \bar b$ if and only if $Ax = b$. The auxiliary program is $\min\{\mathbf 1^\top a : \bar A x + a = \bar b,\ x \ge 0,\ a \ge 0\}$, with the $m \times (n + m)$ matrix $[\bar A \mid I]$.

**Step 1 (phase one stops at an optimum).** The artificial columns form the matrix $I$, and $I^{-1} \bar b = \bar b \ge 0$, so line L2 gives a feasible basis. For each feasible point, $\mathbf 1^\top a \ge 0$, so the auxiliary program is not unbounded: by Step 4 of the simplex proof, an UNBOUNDED answer would give a ray $w$ with $\mathbf 1^\top w_a < 0$ and $w \ge 0$, which is not possible. Under Bland's rule no basis repeats, so phase one stops after finitely many pivots at an optimal basis $B$ with value $v^* \ge 0$ and an optimal dual vector $u$, with $[\bar A \mid I]^\top u \le (0, \mathbf 1)$ and $\bar b^\top u = v^*$.

**Step 2 (claim 1).** If $Ax = b$ and $x \ge 0$ for some $x$, then $(x, 0)$ is feasible for the auxiliary program with value $0$, so $v^* = 0$. Hence $v^* > 0$ implies that the original program is infeasible. In that case let $z = D u$. The first $n$ dual constraints give $\bar A^\top u \le 0$, that is $A^\top D u = A^\top z \le 0$. Also $b^\top z = b^\top D u = \bar b^\top u = v^* > 0$. In the tableau, the reduced cost of the artificial column $i$ is $1 - u_i$, so $u_i = 1 - r_{n+i}$; this is how the implementation reads $z$.

**Step 3 (driving out the artificials).** Now $v^* = 0$, so every artificial variable is $0$ at the basic solution of $B$. Let $T = A_B^{-1} [\bar A \mid I \mid \bar b]$ be the tableau, where $A_B$ is the basis matrix of $[\bar A \mid I]$. The artificial part of row $i$ of $T$ is row $i$ of $A_B^{-1}$, call it $g_i$. So row $i$ of $T$ is $(g_i \bar A,\ g_i,\ g_i \bar b)$.

Take a row $i$ whose basic variable is the artificial $a_k$. Its right-hand side is $g_i \bar b = a_k = 0$.

- If $g_i \bar A$ has an entry $\ne 0$ in an original column $j$, the pivot on $(i, j)$ makes $x_j$ basic in row $i$ and $a_k$ nonbasic. The new basis is a basis because the pivot entry is not $0$. The right-hand side of row $i$ is $0$, so the pivot subtracts multiples of a zero right-hand side from the other rows and leaves all basic values unchanged. The basis stays feasible, with the same basic solution.
- If $g_i \bar A = 0$, then the column of $a_k$ is the unit vector $e_i$ of the tableau, so $(g_i)_k = 1$. Hence $\bar A_k = -\sum_{l \ne k} (g_i)_l \bar A_l$ (rows of $\bar A$) and $\bar b_k = -\sum_{l \ne k} (g_i)_l \bar b_l$, since $g_i \bar b = 0$. So the constraint $k$ is a combination of the other constraints, with the same combination of the right-hand sides, and deleting it does not change the solution set of $\bar A x = \bar b$.

Each pivot of the first case keeps the artificials that are still basic in other rows basic, so the loop treats every row once. If $a_{k'}$ was deleted in an earlier row $i'$, then column $a_{k'}$ is the unit vector $e_{i'}$, so $(g_i)_{k'} = 0$ for every other row $i$. Thus every combination above uses only the constraints that are kept, and the deleted constraints are implied by the kept ones together.

**Step 4 (the start of phase two).** After the loop, let $K$ be the kept tableau rows and $R$ the kept constraints, $|K| = |R| = s$. Every basic variable of a row in $K$ is an original column. By Step 3, each kept tableau row is $g_i \bar A$ with $(g_i)_{k'} = 0$ for every deleted constraint $k'$, so the $s$ kept tableau rows are $M \bar A_R$ for an $s \times s$ matrix $M$ (the restriction of the $g_i$ to $R$). The kept tableau rows contain the identity matrix in the basic columns, so they are independent, and so $M$ is invertible and the rows of $\bar A_R$ are independent. The basis matrix $(\bar A_R)_{B}$ satisfies $M (\bar A_R)_B = I$, so it is nonsingular, and its basic solution is the kept right-hand side, which is $\ge 0$. By Step 3, $\{x : \bar A_R x = \bar b_R\} = \{x : Ax = b\}$. Line L8 deletes only nonbasic columns at value $0$.

**Step 5 (claim 2).** Phase two is SIMPLEX on $\min\{c^\top x : \bar A_R x = \bar b_R,\ x \ge 0\}$ from the feasible basis of Step 4. This program has the same feasible set as the original one, and its matrix has full row rank. By the correctness theorem of the [simplex method](/simplex-method/), phase two stops under Bland's rule, and an OPTIMAL$(x, y_R)$ answer has $\bar A_R^\top y_R \le c$ and $\bar b_R^\top y_R = c^\top x$. Let $y$ have $y_k = D_{kk} (y_R)_k$ for $k \in R$ and $y_k = 0$ for the deleted rows. Then $A^\top y = \bar A_R^\top y_R \le c$ and $b^\top y = \bar b_R^\top y_R = c^\top x$, so $y$ is a dual certificate for the original program. An UNBOUNDED answer gives $w \ge 0$ with $\bar A_R w = 0$ and $c^\top w < 0$; since the deleted rows are combinations of the kept rows, also $Aw = 0$. $\blacksquare$

**Remark.** The implementation does not form $D$ for the dual of phase two: it solves $y^\top A_B = c_B$ on the kept original rows directly, which gives the same $y$.
