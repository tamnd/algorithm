---
title: The auxiliary program finds a feasible basis or a Farkas certificate
proves: [correctness, termination]
status: full
---

**Statement.** Let $A \in \mathbb{Q}^{m \times n}$ and $b \in \mathbb{Q}^m$. INITIAL-BFS$(A, b)$ with Bland's rule stops. If it returns a basis $B$, then $B$ is a list of $m$ columns of $[A \mid I]$ with $[A \mid I]_B$ nonsingular and $[A \mid I]_B^{-1} b \ge 0$. If it returns $y$, then $y \ge 0$, $y^\top A \ge 0$ and $y^\top b < 0$, and the system $Ax \le b$, $x \ge 0$ has no solution.

**Setup.** Write $\hat A = [A \mid I \mid -\mathbf 1]$ for the matrix of the auxiliary program, with the columns $x$, $s$ and $x_0$. The auxiliary program is $\min\{x_0 : \hat A (x, s, x_0) = b,\ (x, s, x_0) \ge 0\}$.

**Step 1 (line L1).** If $b \ge 0$, the slack columns form $I$, and $I^{-1} b = b \ge 0$. So the slack basis is a feasible basis.

**Step 2 (line L3 gives a feasible basis).** Now $b_k < 0$ for the row $k$ with the least $b_k$. The entry of $x_0$ in row $k$ of the slack tableau is $-1 \ne 0$, so the pivot on $(k, x_0)$ gives a basis: the slack columns of the rows $i \ne k$ and the column $x_0$. After the pivot, row $k$ reads $x_0 = -b_k + (\text{nonbasic terms})$, so the basic value of $x_0$ is $-b_k > 0$. Row $i \ne k$ is the old row $i$ minus the old row $k$, so the basic value of $s_i$ is $b_i - b_k \ge 0$. Hence the new basis is feasible.

**Step 3 (line L4 stops at an optimum).** Each feasible point has $x_0 \ge 0$, so the auxiliary program is not unbounded below: an UNBOUNDED answer would give a direction $w \ge 0$ with $\hat A w = 0$ and objective $w_{x_0} < 0$, which contradicts $w \ge 0$. By the correctness theorem of the [simplex method](/simplex-method/), the run of line L4 with Bland's rule stops at an optimal basis, with value $v^* \ge 0$ and a dual vector $u$ with $\hat A^\top u \le e_{x_0}$ and $b^\top u = v^*$. In the tableau, the reduced cost of the slack column $s_i$ is $0 - u_i$.

**Step 4 (line L5).** Assume $v^* > 0$. If some $x \ge 0$ had $Ax \le b$, then $(x, b - Ax, 0)$ would be feasible for the auxiliary program with value $0 < v^*$, which contradicts optimality. So the system is infeasible. Let $y = -u$, the vector of the reduced costs of the slack columns. Dual feasibility at the slack column $i$ is $u_i \le 0$, so $y \ge 0$. At the column $x_j$ it is $u^\top A_j \le 0$, so $y^\top A \ge 0$. And $y^\top b = -u^\top b = -v^* < 0$.

**Step 5 (line L6).** Assume $v^* = 0$, so the basic value of $x_0$ is $0$ if $x_0$ is basic. Let row $p$ of the tableau have $x_0$ as its basic variable. Row $p$ is $g \hat A$ for the row $g$ of the inverse of the basis matrix, and $g \ne 0$. Its restriction to the columns of $[A \mid I]$ is $g [A \mid I]$, and this is not $0$, because the identity block gives the entries $g$ itself. So line L6 finds an entry $\ne 0$ in a column $q$ of $[A \mid I]$. The pivot on $(p, q)$ gives a basis, since the pivot entry is not $0$. The right-hand side of row $p$ is $0$, so the pivot does not change any basic value, and the basis stays feasible. Now $x_0$ is nonbasic.

**Step 6 (line L7).** After Step 5 all $m$ basic columns are columns of $[A \mid I]$, and $x_0 = 0$. The basic solution satisfies $\hat A(x, s, 0) = [A \mid I](x, s) = b$ with $(x, s) \ge 0$ and zeros outside $B$. The columns of $B$ are independent as columns of $\hat A$, so $[A \mid I]_B$ is nonsingular, and its basic solution is the one above, which is $\ge 0$. $\blacksquare$
