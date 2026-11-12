---
title: The LLE weights and embedding solve their least squares problems
proves: [correctness]
status: full
---

Fix a point $i$ with neighbors $N(i) = \{j_1, \dots, j_k\}$, and let $z_s = x_{j_s} - x_i$ and $C_{st} = z_s^\top z_t$ as in line L3. Let $\mathbf{1}$ be the all-ones vector and $U = \{u : \mathbf{1}^\top u = 0\}$.

**Lemma 1 (the local cost).** For $w$ with $\mathbf{1}^\top w = 1$, $\|x_i - \sum_s w_s x_{j_s}\|^2 = w^\top C w$.

*Proof.* Since $\sum_s w_s = 1$, $x_i - \sum_s w_s x_{j_s} = -\sum_s w_s (x_{j_s} - x_i) = -\sum_s w_s z_s$, whose squared norm is $\sum_{s,t} w_s w_t z_s^\top z_t = w^\top C w$. $\square$

**Lemma 2 (the weights).** Let $C' = C + rI$ with $r \ge 0$ be the matrix after line L4, and suppose $u^\top C' u > 0$ for all nonzero $u \in U$. Then the bordered system of line L5 has a unique solution $(w, \mu)$, and $w$ is the unique minimizer of $w^\top C' w$ subject to $\mathbf{1}^\top w = 1$. If $C'$ is invertible, $w = C'^{-1}\mathbf{1} / (\mathbf{1}^\top C'^{-1}\mathbf{1})$.

*Proof.* $C'$ is positive semidefinite, as a Gram matrix plus $rI$. The feasible set is $w_0 + U$ for any feasible $w_0$, and on it $f(w) = w^\top C' w$ is a convex quadratic that is strictly convex along $U$, so it has a unique minimizer. The Lagrange condition at the minimizer is $2C'w + \mu'\mathbf{1} = 0$ with $\mathbf{1}^\top w = 1$, which is the bordered system with $\mu = \mu'/2$. If the bordered matrix sent a nonzero $(u, \nu)$ to 0, then $\mathbf{1}^\top u = 0$ and $C'u = -\nu\mathbf{1}$, so $u^\top C' u = -\nu\,\mathbf{1}^\top u = 0$, hence $u = 0$ by the assumption, and then $\nu\mathbf{1} = 0$ gives $\nu = 0$. So the system is nonsingular. If $C'$ is invertible, $w = -\mu C'^{-1}\mathbf{1}$, and the constraint fixes $\mu$, which gives the formula. $\square$

The assumption holds when $r > 0$ and $C \ne 0$, because then $C'$ is positive definite. With $r = 0$ it holds exactly when the neighbors are affinely independent: $u^\top C u = \|\sum_s u_s z_s\|^2 = \|\sum_s u_s x_{j_s}\|^2$ for $u \in U$, which is 0 only if the $x_{j_s}$ satisfy an affine dependence.

**Lemma 3 (invariance).** The weights do not change when every point is mapped by $x \mapsto aQx + b$ with $a \ne 0$, $Q$ orthogonal and $b$ a vector, as long as $r$ is a fixed multiple of $\operatorname{tr}(C)$.

*Proof.* Each $z_s$ becomes $aQz_s$, so $C$ becomes $a^2 C$ and $\operatorname{tr}(C)$ becomes $a^2\operatorname{tr}(C)$. Then $C'$ becomes $a^2 C'$, and the minimizer of $w^\top C' w$ on the constraint set does not change when the cost is multiplied by $a^2 > 0$. $\square$

**Theorem 1 (exact reconstruction on flat data).** Suppose $x_i = Az_i + b$ for points $z_i \in \mathbb{R}^m$, a matrix $A$ and a vector $b$, and suppose each point is reconstructed exactly by its weights: $x_i = \sum_j w_{ij} x_j$. If $A$ has full column rank, then each coordinate vector $z^{(l)} = (z_1[l], \dots, z_n[l])$ satisfies $Mz^{(l)} = 0$. Also $M\mathbf{1} = 0$ for every weight matrix.

*Proof.* Each row of $W$ sums to 1, so $(I - W)\mathbf{1} = 0$ and $M\mathbf{1} = (I - W)^\top 0 = 0$. From $x_i = \sum_j w_{ij}x_j$ and $\sum_j w_{ij} = 1$, we get $A(z_i - \sum_j w_{ij}z_j) = 0$, and the full column rank of $A$ gives $z_i = \sum_j w_{ij} z_j$. So $(I - W)z^{(l)} = 0$ and $Mz^{(l)} = 0$. $\square$

With $r = 0$ and affinely independent neighbors that span the plane of the data, Lemma 1 and Lemma 2 give a reconstruction error of 0, which is the assumption of Theorem 1. The test suite checks this with exact rational arithmetic.

**Theorem 2 (the embedding minimizes the cost).** $M$ is symmetric positive semidefinite, and $\Phi(Y) = \operatorname{tr}(Y^\top MY)$. Let $\mu_1 \le \mu_2 \le \dots \le \mu_{n-1}$ be the eigenvalues of $M$ restricted to $\mathbf{1}^\perp$, with orthonormal eigenvectors $u_1, \dots, u_{n-1}$. Over all $Y$ with $\mathbf{1}^\top Y = 0$ and $\frac1n Y^\top Y = I$, the minimum of $\Phi$ is $n(\mu_1 + \dots + \mu_m)$, attained by $Y = \sqrt n\,[u_1, \dots, u_m]$.

*Proof.* $M = A^\top A$ with $A = I - W$, so it is symmetric and $v^\top M v = \|Av\|^2 \ge 0$. The $i$-th row of $AY$ is $y_i - \sum_j w_{ij}y_j$, so $\Phi(Y) = \|AY\|_F^2 = \operatorname{tr}(Y^\top MY)$. Since $M\mathbf{1} = 0$ and $M$ is symmetric, $M$ maps $\mathbf{1}^\perp$ into itself, so the restricted eigenvectors exist. Write $Y = \sqrt n\,P$ with $P$ having orthonormal columns in $\mathbf{1}^\perp$. Then $\Phi(Y) = n\operatorname{tr}(P^\top MP)$, and by Ky Fan's minimum principle the trace of $P^\top MP$ over orthonormal $m$-frames in $\mathbf{1}^\perp$ is at least $\mu_1 + \dots + \mu_m$, with equality for $P = [u_1, \dots, u_m]$. $\square$

**Lemma 4 (discarding the constant).** Let $c$ be larger than every eigenvalue of $M$ and $M' = M + \frac cn\mathbf{1}\mathbf{1}^\top$. Then $M'\mathbf{1} = c\mathbf{1}$, and $M'u = Mu$ for $u \in \mathbf{1}^\perp$. So the $m$ smallest eigenvectors of $M'$, for $m \le n - 1$, are $u_1, \dots, u_m$ of Theorem 2 (or another orthonormal basis of the same eigenspaces when eigenvalues repeat).

*Proof.* $\mathbf{1}^\top\mathbf{1} = n$ gives $M'\mathbf{1} = M\mathbf{1} + c\mathbf{1} = c\mathbf{1}$, and $\mathbf{1}^\top u = 0$ gives $M'u = Mu$. The eigenvalues of $M'$ are therefore $\mu_1, \dots, \mu_{n-1}$ and $c > \mu_{n-1}$, so the eigenvalue $c$ comes last. The implementation takes $c = \operatorname{tr}(M) + 1$, which is larger than each eigenvalue of the positive semidefinite $M$. $\square$

**Corollary (recovery up to an affine map).** Under Theorem 1, if the null space of $M$ is exactly the span of $\mathbf{1}, z^{(1)}, \dots, z^{(m)}$, then $\mu_1 = \dots = \mu_m = 0$, and the columns of $Y$ span the same space as the centered coordinates $Jz^{(1)}, \dots, Jz^{(m)}$. So $y_i = Gz_i + h$ for an invertible $m \times m$ matrix $G$ and a vector $h$. In the example on the page, the null space is the span of $\mathbf{1}$ and $(0, 1, 2, 3, 4)$, and the output is the centered line scaled to unit mean square.
