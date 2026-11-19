---
title: Every SIMPLE iteration conserves mass exactly, and the fixed points of SIMPLE are the discrete steady solutions for every choice of under-relaxation
proves: [correctness, termination]
status: full
---

**Setting.** The grid is the staggered grid of the main page: periodic in $x$, and in $y$ either periodic or closed by no-slip walls, where $v = 0$ on the wall faces. The unknown faces are all $u$ faces and the $v$ faces that are not on a wall. $D$ maps face values to cell centers, $(D\mathbf{w})_c = (u_{i+1,j} - u_{i,j})/\Delta x + (v_{i,j+1} - v_{i,j})/\Delta y$ with wall values zero, and $G$ maps cell values to the unknown faces, $(Gq)_f = (q_{\text{right}} - q_{\text{left}})/h_f$ with $h_f = \Delta x$ or $\Delta y$. The discrete steady equations are

$$M(\mathbf{u})\,\mathbf{u} = \mathbf{f} - Gp, \qquad D\mathbf{u} = 0,$$

where row $f$ of $M(\mathbf{u})$ reads $a_P u_f - \sum a_{nb} u_{nb}$, the central difference form of $(\mathbf{u}\cdot\nabla)\mathbf{u} - \nu\Delta\mathbf{u}$ with coefficients computed from $\mathbf{u}$ itself. Write $A = \operatorname{diag}(a_P)$ and $N = A - M$. One SIMPLE iteration from $(\mathbf{u}^m, p^m)$, with $0 < \alpha_u \le 1$, $\alpha_p > 0$ and $s \ge 1$ sweeps, is:

1. compute $A$ and $N$ from $\mathbf{u}^m$ (line L2);
2. $\mathbf{u}^* = S^s(\mathbf{u}^m)$, where $S$ is one Gauss-Seidel sweep on the relaxed system $(A/\alpha_u - N)\mathbf{x} = \mathbf{f} - Gp^m + (1 - \alpha_u)(A/\alpha_u)\mathbf{u}^m$ (line L3);
3. $d = \alpha_u/a_P$ on each unknown face (line L4);
4. solve $Bp' = -D\mathbf{u}^*$ with $B = -D\operatorname{diag}(d)G$ (line L5);
5. $p^{m+1} = p^m + \alpha_p p'$ and $\mathbf{u}^{m+1} = \mathbf{u}^* - \operatorname{diag}(d)Gp'$ (lines L6 and L7).

Assume $a_P > 0$ on every unknown face; this holds when $\nu > 0$, because $a_P$ contains $2\nu/\Delta x^2 + 2\nu/\Delta y^2$ and the wall ghost terms add nonnegative amounts when the cell Péclet number is at most 2. Then $d > 0$.

**Lemma 1 (summation by parts).** For every face vector $\mathbf{w}$ with zero wall values and every cell vector $q$, $\sum_c q_c (D\mathbf{w})_c = -\sum_f w_f (Gq)_f$, the sum over the unknown faces. As matrices, $G^T = -D$.

*Proof.* Collect the terms of the left side by faces. A $u$ face $f$ between the cells $\ell$ (left) and $r$ (right) appears with $+u_f/\Delta x$ in cell $\ell$ and $-u_f/\Delta x$ in cell $r$, so it contributes $u_f(q_\ell - q_r)/\Delta x = -u_f(Gq)_f$. The $v$ faces are the same with $\Delta y$. Periodicity makes every face have two cells. A wall face has $w_f = 0$ and contributes nothing on either side. $\square$

**Lemma 2 (the correction matrix).** $B = G^T\operatorname{diag}(d)G$ is symmetric positive semidefinite. Its null space is the constant vectors, and its range is the vectors with zero sum.

*Proof.* Lemma 1 gives $B = -D\operatorname{diag}(d)G = G^T\operatorname{diag}(d)G$, which is symmetric. For any $q$, $q^TBq = \sum_f d_f (Gq)_f^2 \ge 0$, with equality exactly when $Gq = 0$ on every unknown face, because every $d_f > 0$. $Gq = 0$ means that $q$ is equal across every unknown face; the cells and the unknown faces form a connected graph, so $q$ is constant. For a symmetric matrix the range is the orthogonal complement of the null space, which is the zero-sum vectors. $\square$

The test file checks $B = -D\operatorname{diag}(d)G$, the symmetry and the zero row sums in exact rational arithmetic, with random $d$.

**Lemma 3 (solvability).** For every face vector $\mathbf{w}$ with zero wall values, $\sum_c (D\mathbf{w})_c = 0$. So the equation $Bp' = -D\mathbf{u}^*$ has a solution, unique up to a constant.

*Proof.* Lemma 1 with $q = 1$ gives $\sum_c (D\mathbf{w})_c = -\sum_f w_f (G1)_f = 0$. By Lemma 2 the right side is in the range of $B$, and two solutions differ by an element of the null space. $\square$

**Theorem 1 (mass conservation at every iteration).** If line L5 solves $Bp' = -D\mathbf{u}^*$ exactly, then $D\mathbf{u}^{m+1} = 0$ after every iteration, whatever $\mathbf{u}^m$, $p^m$, $\alpha_u$, $\alpha_p$ and $s$ are.

*Proof.* $D\mathbf{u}^{m+1} = D\mathbf{u}^* - D\operatorname{diag}(d)Gp' = D\mathbf{u}^* + Bp' = D\mathbf{u}^* - D\mathbf{u}^* = 0$. $\square$

The code solves line L5 with conjugate gradients to a relative residual of $10^{-12}$; conjugate gradients from a zero start on a consistent symmetric positive semidefinite system stay in the range of $B$, so they converge as on a definite system. The test file checks $\max|D\mathbf{u}^{m+1}| < 10^{-10}$ after every iteration of a full run. Theorem 1 does not use $\alpha_p$: the velocity correction uses all of $p'$, and only the pressure is under-relaxed. This is what makes every SIMPLE iterate mass conserving, unlike the iterates of [artificial compressibility](/artificial-compressibility-method/).

**Lemma 4 (fixed points of Gauss-Seidel).** Let $C\mathbf{x} = \mathbf{b}$ have a nonzero diagonal and a unique solution $\hat{\mathbf{x}}$. One sweep $S$ maps $\hat{\mathbf{x}}$ to itself. If the iteration matrix $T$ of $S$ has no eigenvalue $\lambda$ with $\lambda^s = 1$ (true when Gauss-Seidel converges, so $\rho(T) < 1$), then $S^s(\mathbf{x}) = \mathbf{x}$ implies $\mathbf{x} = \hat{\mathbf{x}}$.

*Proof.* In a sweep from $\hat{\mathbf{x}}$, row $i$ sets $x_i = (b_i - \sum_{j \ne i} c_{ij}x_j)/c_{ii}$ with all other entries still equal to $\hat{\mathbf{x}}$, which gives $\hat{x}_i$ because $\hat{\mathbf{x}}$ satisfies row $i$. For the second claim, $S(\mathbf{x}) - \hat{\mathbf{x}} = T(\mathbf{x} - \hat{\mathbf{x}})$, so $S^s(\mathbf{x}) = \mathbf{x}$ means $(T^s - I)(\mathbf{x} - \hat{\mathbf{x}}) = 0$, and $T^s - I$ is invertible by the assumption. $\square$

The assumption holds, for example, when the relaxed matrix $A/\alpha_u - N$ is strictly diagonally dominant. That is the case when $\alpha_u < 1$ and every $a_{nb} \ge 0$ (cell Péclet number $|u|h/\nu \le 2$), because then $\sum|a_{nb}| \le a_P < a_P/\alpha_u$.

**Theorem 2 (fixed points).** Assume the hypothesis of Lemma 4 for the relaxed system at $\mathbf{u}$. Then $(\mathbf{u}, p)$ is a fixed point of the SIMPLE iteration if and only if $M(\mathbf{u})\mathbf{u} = \mathbf{f} - Gp$ and $D\mathbf{u} = 0$. The set of fixed points does not depend on $\alpha_u$, $\alpha_p$ or $s$.

*Proof.* Suppose $(\mathbf{u}, p)$ solves the steady equations. The relaxed system at $\mathbf{u}^m = \mathbf{u}$ reads $(A/\alpha_u - N)\mathbf{x} = M(\mathbf{u})\mathbf{u} + (1 - \alpha_u)(A/\alpha_u)\mathbf{u}$, which $\mathbf{x} = \mathbf{u}$ satisfies, because $(A/\alpha_u - N)\mathbf{u} = M(\mathbf{u})\mathbf{u} + (1/\alpha_u - 1)A\mathbf{u}$. By Lemma 4, $\mathbf{u}^* = \mathbf{u}$. Then $-D\mathbf{u}^* = 0$, line L5 returns $p' = 0$ (conjugate gradients from zero with a zero right side), and $(\mathbf{u}^{m+1}, p^{m+1}) = (\mathbf{u}, p)$.

Conversely, let $(\mathbf{u}, p)$ be a fixed point. From $p^{m+1} = p$ and $\alpha_p > 0$ we get $p' = 0$, so $\mathbf{u} = \mathbf{u}^{m+1} = \mathbf{u}^*$, and Theorem 1 gives $D\mathbf{u} = 0$. Now $\mathbf{u}^* = S^s(\mathbf{u})$ equals $\mathbf{u}$, so by Lemma 4 $\mathbf{u}$ solves the relaxed system: $(A/\alpha_u - N)\mathbf{u} = \mathbf{f} - Gp + (1 - \alpha_u)(A/\alpha_u)\mathbf{u}$. Subtract $(1/\alpha_u - 1)A\mathbf{u}$ from both sides to get $(A - N)\mathbf{u} = M(\mathbf{u})\mathbf{u} = \mathbf{f} - Gp$. No step used the values of $\alpha_u$, $\alpha_p$ or $s$. $\square$

So if SIMPLE converges, the limit solves the discrete steady incompressible equations, and the under-relaxation factors change only the path. The coefficients $d = \alpha_u/a_P$ in the correction are an approximation (SIMPLE drops the neighbor terms $\sum a_{nb}u'_{nb}$ of the velocity correction), but Theorem 2 shows that this approximation does not reach the converged answer. On the staggered grid the converged answer also does not depend on $d$ through any interpolation; on a collocated grid with [Rhie-Chow interpolation](/rhie-chow-interpolation/) it can. Line L8 checks the residual of the full discrete equations (the momentum equations, evaluated by separate code, and $D\mathbf{u}$) directly, so a return from line L9 certifies $\max|\text{residual}| \le$ tol.

**Termination.** The loop of line L1 runs at most maxit times. Each iteration does a fixed number $s$ of Gauss-Seidel sweeps and one conjugate gradient solve, which stops after at most its own iteration limit. So the procedure always ends. It ends at line L9 with a certified residual, or after maxit iterations without one.

**What is not proved.** Theorems 1 and 2 say nothing about convergence. SIMPLE has no general convergence theorem for the nonlinear equations, and the right under-relaxation factors are rules of thumb. The tests show a case where $\alpha_u = 0.7$ with $\alpha_p = 1$ diverges and $\alpha_p = 0.3$ converges. Theorem 2 also does not say that the discrete steady equations have a unique solution; on a fully periodic grid they do not fix the mean velocity, and the tests find two different converged states from two starts.
