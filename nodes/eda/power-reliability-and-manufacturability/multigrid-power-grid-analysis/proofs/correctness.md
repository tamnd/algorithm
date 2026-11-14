---
title: The one-pass coarse solve is the energy-norm best approximation in the range of the interpolation
proves: [correctness]
status: full
---

**Setting.** $A$ is an $N \times N$ symmetric positive definite matrix, as the conductance matrix of a power grid is when every connected part has a pad (see the [power grid analysis](/power-grid-analysis/) page). The exact drop is $x = A^{-1} b$. $P$ is an $N \times N_c$ matrix. The energy inner product is $\langle u, v \rangle_A = u^T A v$, with the norm $\|u\|_A = \sqrt{u^T A u}$.

**Lemma 1 ($P$ has full column rank).** The interpolation of line L2 has full column rank, and its rows sum to 1.

*Proof.* Each coarse node $q$ is a K node $m(q)$ of the fine grid, and row $m(q)$ of $P$ is the unit row $e_q^T$. So the rows of the K nodes form the identity of size $N_c$, and $P y = 0$ forces $y = 0$. For the sums: a K row sums to 1. An H or V row is a combination of K rows with nonnegative weights that sum to 1, so it sums to 1. A C row is a combination of H and V rows with weights that sum to 1, so it sums to 1. (When all weights of a node are 0, the code uses equal weights, which also sum to 1.) $\square$

**Lemma 2 (the coarse matrix).** $A_c = P^T A P$ is symmetric and positive definite.

*Proof.* $A_c^T = P^T A^T P = A_c$. For $y \ne 0$, $P y \ne 0$ by Lemma 1, so $y^T A_c y = (P y)^T A (P y) > 0$. $\square$

So line L4 solves a nonsingular system at every level, and by induction every coarse matrix of the recursion is symmetric positive definite.

**Theorem 1 (Galerkin best approximation, one level).** Let $x_c = A_c^{-1} P^T b$ and $\hat{x} = P x_c$. Then $P^T A (x - \hat{x}) = 0$, and for every $y \in \mathbb{R}^{N_c}$,

$$ \|x - \hat{x}\|_A \le \|x - P y\|_A, $$

with equality only for $y = x_c$.

*Proof.* $P^T A \hat{x} = A_c x_c = P^T b = P^T A x$, which is the first claim. So the error $e = x - \hat{x}$ is $A$-orthogonal to every $P z$. For any $y$, write $x - P y = e + P(x_c - y)$. Then

$$ \|x - P y\|_A^2 = \|e\|_A^2 + 2 \langle e, P(x_c - y) \rangle_A + \|P(x_c - y)\|_A^2 = \|e\|_A^2 + \|P(x_c - y)\|_A^2, $$

and the last term is positive unless $y = x_c$, by Lemma 1. $\square$

**Theorem 2 (several levels).** Let the recursion use the interpolations $P_1, P_2, \ldots, P_\ell$, end with an exact solve at line L1, and let $Q = P_1 P_2 \cdots P_\ell$. Then the answer of line L5 at the top is $\hat{x} = Q (Q^T A Q)^{-1} Q^T b$, and Theorem 1 holds with $Q$ in place of $P$.

*Proof.* By induction on $\ell$. For $\ell = 0$, $Q = I$ and the answer is $A^{-1} b$. For $\ell \ge 1$, the call at line L4 works on $A_1 = P_1^T A P_1$ and $b_1 = P_1^T b$ with the interpolations $P_2, \ldots, P_\ell$, so by the induction hypothesis it returns $Q' (Q'^T A_1 Q')^{-1} Q'^T b_1$ with $Q' = P_2 \cdots P_\ell$. Line L5 multiplies by $P_1$. Since $Q = P_1 Q'$, we get $Q'^T A_1 Q' = Q^T A Q$ and $Q'^T b_1 = Q^T b$, so the answer is $Q (Q^T A Q)^{-1} Q^T b$. $Q$ has full column rank as a product of matrices with full column rank, so the proof of Theorem 1 applies with $Q$. $\square$

**Corollary 1 (energy split and low average).** $x^T A x = \hat{x}^T A \hat{x} + \|x - \hat{x}\|_A^2$, and $b^T \hat{x} \le b^T x$, with equality only when $\hat{x} = x$.

*Proof.* $\hat{x} = Q y$ for some $y$, and $x - \hat{x}$ is $A$-orthogonal to it, so the first identity is the Pythagorean theorem in the energy inner product. From $Q^T A (x - \hat{x}) = 0$ we get $\hat{x}^T A \hat{x} = \hat{x}^T A x = \hat{x}^T b$, and $x^T A x = x^T b$. So $b^T x - b^T \hat{x} = \|x - \hat{x}\|_A^2 \ge 0$. $\square$

**Corollary 2 (exact cases).** $\hat{x} = x$ if and only if $x$ is in the range of $Q$.

*Proof.* If $x = Q y$, then Theorem 1 gives $\|x - \hat{x}\|_A \le \|x - Q y\|_A = 0$. The converse is clear. $\square$

**Corollary 3 (the total load).** The total coarse load equals the total fine load, $\mathbf{1}^T P^T b = \mathbf{1}^T b$, and the pad currents of $\hat{x}$ add up to the total load.

*Proof.* $P \mathbf{1} = \mathbf{1}$ by Lemma 1, so $\mathbf{1}^T P^T b = (P \mathbf{1})^T b = \mathbf{1}^T b$. For the pad currents: $A = \mathcal{L} + \mathrm{diag}(g^{\mathrm{pad}})$ with $\mathcal{L} \mathbf{1} = 0$, so the total pad current of a drop vector $z$ is $\sum_k g^{\mathrm{pad}}_k z_k = \mathbf{1}^T A z$. Since $\mathbf{1} = Q \mathbf{1}$ is in the range of $Q$, the Galerkin condition gives $\mathbf{1}^T A \hat{x} = \mathbf{1}^T A x = \mathbf{1}^T b$. $\square$

**Theorem 3 (the variant never increases the energy error and converges).** In lines L6 to L11, let $e = x - x_{\text{current}}$. Each Gauss-Seidel sweep and each coarse correction of line L10 gives $\|e_{\text{new}}\|_A \le \|e\|_A$, and the iterates converge to $x$.

*Proof.* Coarse correction: the new error is $e - P A_c^{-1} P^T A e = (I - \Pi) e$, where $\Pi = P A_c^{-1} P^T A$ is the $A$-orthogonal projection onto the range of $P$. By the Pythagorean theorem, $\|e\|_A^2 = \|\Pi e\|_A^2 + \|(I - \Pi) e\|_A^2$, so the norm does not grow.

Gauss-Seidel: one update of coordinate $k$ sets $x_k$ so that equation $k$ holds. Among all changes of coordinate $k$ alone, this one minimizes $\|x - x_{\text{current}}\|_A^2$, because that quadratic in the new value of $x_k$ has the derivative $-2 (A e)_k$, which vanishes exactly when equation $k$ holds. The old value is one of the candidates, so the norm does not grow. A sweep is $N$ such updates.

Convergence: for a symmetric positive definite $A$, the forward Gauss-Seidel iteration matrix $M$ satisfies $\|M\|_A < 1$, the classical theorem of Reich and Ostrowski on the [Gauss-Seidel method](/gauss-seidel-method/). So each cycle multiplies $\|e\|_A$ by at most $\|M\|_A^2 < 1$, with the coarse correction in between not increasing it, and $e \to 0$. $\square$

The rate $\|M\|_A^2$ can be close to 1 on a large grid, and the coarse correction is what makes the measured rate fast. How fast it is on a given grid is measured, not proved here. The tests check Theorem 1 exactly in rational arithmetic for one and two levels, compare $\hat{x}$ with random coarse vectors, check Corollary 2 on a uniform line, and check that the energy error of the variant never grows.
