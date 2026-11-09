---
title: The big-M method with a symbolic M returns a correct answer
proves: [correctness, termination]
status: full
---

**Statement.** Let $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$, $c \in \mathbb{Q}^n$. Run BIG-M$(A, b, c)$ with a symbolic $M$ and Bland's rule. The run stops, and its answer (optimal, unbounded or infeasible) is correct for $\min\{c^\top x : Ax = b,\ x \ge 0\}$.

**Setup.** Let $D$ be the diagonal sign matrix of line L1, $\bar A = DA$ and $\bar b = Db \ge 0$; the original feasible set is $\{x \ge 0 : \bar A x = \bar b\}$. Let $F = \mathbb{Q}(M)$ be the field of rational functions in $M$, ordered so that $M$ is larger than every rational number: a nonzero $p(M)/q(M)$ is positive if the leading coefficients of $p$ and $q$ have the same sign. All costs in the run have the form $pM + q$ with $p, q \in \mathbb{Q}$, and $pM + q < 0$ if and only if $(p, q) <_{\text{lex}} (0, 0)$. The penalized program over $F$ has the matrix $[\bar A \mid I]$ of rank $m$ and the cost vector $(c, M\mathbf 1)$.

**Step 1 (the main run stops).** The proof of correctness of the [simplex method](/simplex-method/), including the proof that Bland's rule never repeats a basis, uses only the axioms of an ordered field: the comparisons of reduced costs, the signs of the column entries and the ratio test. The tableau entries are rationals; only the costs are in $F$. So line L3 stops after finitely many pivots, with OPTIMAL or UNBOUNDED, and its certificates hold over $F$. The basis of line L2 is feasible because $\bar b \ge 0$.

**Step 2 (optimal with $a = 0$).** Let $(x, a)$ be the final point, with $a = 0$, so $\bar A x = \bar b$ and $x$ is feasible. For each feasible $x'$, the point $(x', 0)$ is feasible for the penalized program with cost $c^\top x'$. By optimality over $F$, $c^\top x \le c^\top x'$. So $x$ is optimal.

**Step 3 (optimal with some $a_i > 0$, line L7).** At the optimum every reduced cost is $\ge 0$ in $F$, that is $p_j M + q_j \ge 0$ for each column $j$. This forces $p_j \ge 0$. The numbers $p_j$ are the reduced costs of the same basis for the cost vector $(0, \mathbf 1)$, since the reduced costs are linear in the cost vector. So the basis is optimal for $\min\{\mathbf 1^\top a : \bar A x + a = \bar b,\ x, a \ge 0\}$, with value $\mathbf 1^\top a > 0$. As in Step 2 of the proof of the [two-phase method](/two-phase-simplex-method/), the original program is infeasible: a feasible $x$ would give the value $0$. With $u$ the dual vector of this basis for the cost $(0, \mathbf 1)$, which is $u_i = 1 - p_{n+i}$, the vector $z = Du$ has $A^\top z \le 0$ and $b^\top z = \bar b^\top u > 0$.

**Step 4 (a ray, lines L4 to L6).** Line L3 returns UNBOUNDED with an entering column $q$ whose reduced cost $p_q M + r_q$ is negative, and a direction $w = (w_x, w_a) \ge 0$ with $\bar A w_x + w_a = 0$. The cost of $w$ is $c^\top w_x + M \mathbf 1^\top w_a = p_q M + r_q$, so $p_q = \mathbf 1^\top w_a \ge 0$. A negative reduced cost needs $p_q \le 0$. Hence $p_q = 0$, $w_a = 0$ (since $w_a \ge 0$ and $\mathbf 1^\top w_a = 0$), $r_q = c^\top w_x < 0$, and $\bar A w_x = 0$, so $A w_x = 0$. Thus $w_x$ is a ray of descent of the original program.

- If $a = 0$ at the last basis, the last point $x$ is feasible, $x + t w_x$ is feasible for each $t \ge 0$, and $c^\top(x + t w_x) \to -\infty$. The answer UNBOUNDED is correct.
- If some $a_i > 0$, line L6 runs the simplex method with Bland's rule for $\min \mathbf 1^\top a$ from the last basis, which is feasible. This program is bounded below by $0$, so the run stops at an optimum. If the optimum is positive, the original program is infeasible, with the Farkas vector of Step 3. If it is $0$, its final point $(x', 0)$ gives a feasible $x'$, and $x' + t w_x$ shows that the original program is unbounded.

Every case returns a correct answer, and each of the two runs stops. $\blacksquare$
