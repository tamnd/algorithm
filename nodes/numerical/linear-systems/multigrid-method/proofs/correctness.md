---
title: The V-cycle is a consistent linear iteration whose error operator is a contraction in the energy norm
proves: [correctness, termination]
status: full
---

Setting: the model problem of the page. Level $l$ has $n_l = 2^l - 1$ unknowns and $A_l = h_l^{-2}\,\mathrm{tridiag}(-1, 2, -1)$ with $h_l = 2^{-l}$, which is symmetric positive definite. $P_l : \mathbb{R}^{n_{l-1}} \to \mathbb{R}^{n_l}$ is linear interpolation and $R_l$ is full weighting. The smoother $S$ is weighted Jacobi with $0 < \omega \le 1$ or forward Gauss-Seidel, applied $\nu_1$ times before and $\nu_2$ times after the coarse-grid correction, with $\nu_1 + \nu_2 \ge 1$. Arithmetic is exact. For SPD $B$, $\|v\|_B = (v^T B v)^{1/2}$.

**Lemma 1 (transfer operators).** $R_l = \tfrac12 P_l^T$ and $R_l A_l P_l = A_{l-1}$.

*Proof.* Column $j$ of $P_l$ has entries $\tfrac12, 1, \tfrac12$ in fine rows $2j, 2j+1, 2j+2$ (0-based), so row $j$ of $\tfrac12 P_l^T$ is $(\tfrac14, \tfrac12, \tfrac14)$ in those columns, which is full weighting. For the product: $h_l^2 A_l P_l e_j$ has $-\tfrac12$ in rows $2j - 1$ and $2j + 3$, $0$ in rows $2j$ and $2j+2$, and $1$ in row $2j+1$. Full weighting gives $\tfrac12 h_l^{-2} = 2 h_{l-1}^{-2}$ at coarse position $j$ and $-\tfrac14 h_l^{-2} = -h_{l-1}^{-2}$ at positions $j \pm 1$, which is column $j$ of $A_{l-1}$. $\square$

**Lemma 2 (the V-cycle is a linear iteration).** Let $u^\ast_l = A_l^{-1} f_l$. One V-cycle on level $l$, lines L3 to L9, maps $u$ to $u'$ with
$$u' - u^\ast_l = M_l\,(u - u^\ast_l), \qquad M_1 = 0, \qquad M_l = S_l^{\nu_2}\big(I - P_l (I - M_{l-1}) A_{l-1}^{-1} R_l A_l\big) S_l^{\nu_1},$$
where $S_l$ is the error operator of one smoothing sweep: $I - \tfrac{\omega h_l^2}{2} A_l$ for weighted Jacobi and $I - (D_l - E_l)^{-1} A_l$ for Gauss-Seidel.

*Proof.* By induction on $l$. On level 1, line L6 computes $u_1 = f_1/(2 h_1^{-2}) = A_1^{-1} f_1$ exactly, so $M_1 = 0$. On level $l \ge 2$: each smoothing sweep is a splitting iteration $u \leftarrow u + B(f - A u)$, so the error is multiplied by $I - B A = S_l$, and after line L4 the error is $S_l^{\nu_1} e$. Line L5 sets $f_{l-1} = R_l(f_l - A_l u) = R_l A_l (u^\ast_l - u)$, whose exact coarse solution is $A_{l-1}^{-1} R_l A_l (u^\ast_l - u)$. The levels below run, by the induction hypothesis, one V-cycle from $0$ for that coarse system, so they return $(I - M_{l-1}) A_{l-1}^{-1} R_l A_l (u^\ast_l - u)$. Line L8 adds $P_l$ times this, which multiplies the error by $I - P_l (I - M_{l-1}) A_{l-1}^{-1} R_l A_l$, and line L9 multiplies it by $S_l^{\nu_2}$. The two loops of the implementation visit the levels in exactly this nested order. $\square$

**Consistency.** By Lemma 2, $u = u^\ast_l$ is a fixed point of the V-cycle, so if the iterates converge, their limit solves $A_L u = f$.

**Lemma 3 (smoothers contract in the energy norm).** $\|S_l\|_{A_l} < 1$.

*Proof.* Weighted Jacobi: $S_l = I - \tfrac{\omega h_l^2}{2} A_l$ is symmetric in the $A_l$ inner product, with eigenvalues $1 - \omega \lambda h_l^2/2$ where $\lambda h_l^2 = 4\sin^2(k\pi h_l/2) \in (0, 4)$, so they lie in $(1 - 2\omega, 1) \subseteq (-1, 1)$ for $0 < \omega \le 1$. Gauss-Seidel: for SPD $A$ with $M = D - E$, $\|e\|_A^2 - \|(I - M^{-1}A)e\|_A^2 = (M^{-1} A e)^T D (M^{-1} A e) > 0$ for $e \ne 0$, the identity used in the [Ostrowski-Reich theorem](/ostrowski-reich-theorem/) with $\omega = 1$. $\square$

**Lemma 4 (coarse-grid correction does not increase the energy).** Let $C_l = I - P_l (I - M_{l-1}) A_{l-1}^{-1} R_l A_l$. If $\|M_{l-1}\|_{A_{l-1}} \le 1$, then $\|C_l\|_{A_l} \le 1$.

*Proof.* By Lemma 1, $\Pi = P_l A_{l-1}^{-1} R_l A_l = P_l (P_l^T A_l P_l)^{-1} P_l^T A_l$ is the $A_l$-orthogonal projector onto $\mathrm{range}(P_l)$. For an error $e$ write $y = A_{l-1}^{-1} R_l A_l e$, so $\Pi e = P_l y$, and $e_1 = e - P_l y$, which is $A_l$-orthogonal to $\mathrm{range}(P_l)$. Then $C_l e = e_1 + P_l M_{l-1} y$. Since $\|P_l z\|_{A_l}^2 = z^T P_l^T A_l P_l z = 2\|z\|_{A_{l-1}}^2$ by Lemma 1,
$$\|C_l e\|_{A_l}^2 = \|e_1\|_{A_l}^2 + 2\|M_{l-1} y\|_{A_{l-1}}^2 \le \|e_1\|_{A_l}^2 + 2\|y\|_{A_{l-1}}^2 = \|e_1\|_{A_l}^2 + \|P_l y\|_{A_l}^2 = \|e\|_{A_l}^2. \qquad \square$$

**Theorem (convergence).** For every $l$, $\|M_l\|_{A_l} < 1$. Hence the iterates of line L2 satisfy $\|u_k - u^\ast\|_{A} \le \|M_L\|_{A}^k\,\|u_0 - u^\ast\|_{A} \to 0$.

*Proof.* Induction: $M_1 = 0$. For $l \ge 2$, $\|M_l\|_{A_l} \le \|S_l\|_{A_l}^{\nu_1}\,\|C_l\|_{A_l}\,\|S_l\|_{A_l}^{\nu_2} < 1$ by Lemmas 3 and 4 and $\nu_1 + \nu_2 \ge 1$. $\square$

This proves convergence on every grid, but the contraction factor it gives may approach $1$ as $h \to 0$. That the factor is bounded away from $1$ uniformly in $h$ is a deeper result: the smoothing and approximation properties of Hackbusch, or, for this model problem, an exact Fourier analysis of the two-grid operator (Briggs, Henson and McCormick, Chapter 5), and for the V-cycle the theory of Braess and Hackbusch.

**Termination.** The loop at line L2 runs at most `maxiter` times. Each V-cycle runs two loops over $L - 1$ levels with a fixed number of sweeps on each, so it terminates. The algorithm returns `converged` only when the test at line L10 holds.

**What fails outside the hypotheses.** For weighted Jacobi with $\omega > 1$, the highest mode has smoothing factor $1 - 2\omega\sin^2(n\pi h/2)$ close to $1 - 2\omega < -1$, so $\|S_l\|_{A_l} > 1$ and the V-cycle can diverge; the tests observe this for $\omega = 1.5$.
