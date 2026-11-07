---
title: Convergence of the AMG V-cycle for symmetric positive definite matrices
proves: [correctness, termination]
status: full
---

Exact arithmetic. $A_0 = A$ is symmetric positive definite, $A_{l+1} = P_l^T A_l P_l$, and $P_l$ has a unit row for every C point and no other entries in the C columns of those rows. Write $\langle u, v \rangle_l = u^T A_l v$ and $\|v\|_l = \langle v, v \rangle_l^{1/2}$.

**Lemma 1 (coarse matrices).** Each $P_l$ has full column rank and each $A_l$ is symmetric positive definite.

*Proof.* The rows of $P_l$ at the C points form the identity of order $n_{l+1}$, so $P_l c = 0$ forces $c = 0$. If $A_l$ is symmetric positive definite, $A_{l+1}$ is symmetric and $c^T A_{l+1} c = (P_l c)^T A_l (P_l c) > 0$ for $c \ne 0$. Induction on $l$. $\square$

**Lemma 2 (coarse correction).** $K_l = I - P_l A_{l+1}^{-1} P_l^T A_l$ is the $\langle \cdot, \cdot \rangle_l$-orthogonal projection onto the $A_l$-orthogonal complement of $\operatorname{range}(P_l)$.

*Proof.* $Q = P_l A_{l+1}^{-1} P_l^T A_l$ satisfies $Q^2 = P_l A_{l+1}^{-1} (P_l^T A_l P_l) A_{l+1}^{-1} P_l^T A_l = Q$, $Q P_l = P_l$, and $A_l Q = Q^T A_l$, so $Q$ is the $A_l$-orthogonal projection onto $\operatorname{range}(P_l)$ and $K_l = I - Q$ is the complementary one. $\square$

**Lemma 3 (Gauss-Seidel).** Let $A_l = D + L + L^T$ with $D$ diagonal and $L$ strictly lower triangular. The forward sweep maps the error $e$ to $S e$ with $S = I - (D + L)^{-1} A_l$, and $\|S e\|_l^2 = \|e\|_l^2 - \|D^{1/2} (D + L)^{-1} A_l e\|_2^2$. Hence $\|S\|_l < 1$. The backward sweep has error operator $S^* = I - (D + L^T)^{-1} A_l$, the $A_l$-adjoint of $S$, with $\|S^*\|_l = \|S\|_l$.

*Proof.* Put $M = D + L$ and $g = M^{-1} A_l e$. Then $\|e - g\|_l^2 = \|e\|_l^2 - 2 g^T A_l e + g^T A_l g = \|e\|_l^2 - g^T (M + M^T - A_l) g$, using $A_l e = M g$ so that $2 g^T A_l e = g^T (M + M^T) g$. And $M + M^T - A_l = D$. Since $D$ has positive entries (the diagonal of a positive definite matrix), $\|S e\|_l < \|e\|_l$ for $e \ne 0$, and by compactness of the unit sphere $\|S\|_l < 1$. For the adjoint, $A_l S = A_l - A_l M^{-1} A_l$ and $(S^*)^T A_l = A_l - A_l M^{-1} A_l$ with $S^* = I - M^{-T} A_l$, so $A_l S = (S^*)^T A_l$. $\square$

**Theorem 4 (V-cycle).** Let $E_l$ be the error propagation operator of AMG-VCYCLE on level $l$ with $\nu_1 = \nu_2 = 1$ (forward then backward sweep), so that the new error is $E_l e$. Then $E_l$ is $A_l$-self-adjoint and $\|E_l\|_l \le \|S_l\|_l^2 < 1$ on every level that is not the coarsest; on the coarsest level $E_l = 0$.

*Proof.* Induction from the coarsest level, where the solve is exact. On a finer level, the error after the presmoothing is $w = S e$. The coarse right-hand side is $P_l^T A_l w$, and the recursive call returns $(I - E_{l+1}) A_{l+1}^{-1} P_l^T A_l w$, because an iteration with error operator $E_{l+1}$ started from $0$ leaves the error $E_{l+1} y$ for the exact coarse solution $y = A_{l+1}^{-1} P_l^T A_l w$. The error after line L7 is therefore $T w$ with $T = I - P_l (I - E_{l+1}) A_{l+1}^{-1} P_l^T A_l$, and $E_l = S^* T S$.

$T$ is $A_l$-self-adjoint: $A_l T = A_l - A_l P_l (I - E_{l+1}) A_{l+1}^{-1} P_l^T A_l$, and $(I - E_{l+1}) A_{l+1}^{-1}$ is symmetric because $E_{l+1}$ is $A_{l+1}$-self-adjoint. With Lemma 3, $E_l = S^* T S$ is $A_l$-self-adjoint.

$T$ does not increase $\|\cdot\|_l$: write $w = K_l w + P_l y$ (Lemma 2). Then $T w = K_l w + P_l y - P_l (I - E_{l+1}) y = K_l w + P_l E_{l+1} y$. The two terms are $A_l$-orthogonal, so
$\|T w\|_l^2 = \|K_l w\|_l^2 + \|E_{l+1} y\|_{l+1}^2 \le \|K_l w\|_l^2 + \|y\|_{l+1}^2 = \|K_l w\|_l^2 + \|P_l y\|_l^2 = \|w\|_l^2$, using $\|P_l v\|_l = \|v\|_{l+1}$ and the induction hypothesis $\|E_{l+1}\|_{l+1} \le 1$.

So $\|E_l\|_l \le \|S^*\|_l \|T\|_l \|S\|_l \le \|S\|_l^2 < 1$. $\square$

**Corollary 5 (convergence and preconditioning).** The stand-alone iteration satisfies $\|e_k\|_A \le \|S_0\|_A^{2k} \|e_0\|_A \to 0$. One V-cycle from zero applied to a vector $r$ returns $B r$ with $I - B A = E_0$, and $B$ is symmetric positive definite.

*Proof.* The first claim is Theorem 4 applied $k$ times. With $x = 0$ the error is $A^{-1} r$ and the new error is $E_0 A^{-1} r$, so $B r = A^{-1} r - E_0 A^{-1} r$ and $B = (I - E_0) A^{-1}$. $A$-self-adjointness means $A E_0 = E_0^T A$, so $E_0 A^{-1} = A^{-1} E_0^T$ and $B^T = A^{-1} - A^{-1} E_0^T = B$. For $r = A v \ne 0$, $r^T B r = v^T A (I - E_0) v = \|v\|_A^2 - \langle v, E_0 v \rangle_A \ge (1 - \|E_0\|_A) \|v\|_A^2 > 0$. $\square$

**Termination.** AMG-SETUP stops because each pass either stops or strictly decreases $n_l$ (it continues only when $0 < n_{l+1} < n_l$), and AMG-VCYCLE recurses only to strictly smaller levels. The stand-alone solver stops at the tolerance or after its iteration limit. $\blacksquare$
