---
title: The SE-Sync certificate proves optimality for the semidefinite relaxation, the staircase step descends, and a tight relaxation gives a global optimum
proves: [correctness]
status: full
---

**Setting.** The unknowns are $R_1, \dots, R_n \in SO(2)$, written as $R = [R_1 \cdots R_n] \in \mathbb{R}^{2 \times 2n}$. Each edge $(i, j)$ has a measurement $\tilde R_{ij} \in SO(2)$ and a weight $\kappa_{ij} > 0$. The cost is $F(R) = \sum_{(i,j)} \kappa_{ij} \|R_j - R_i \tilde R_{ij}\|_F^2$. The connection Laplacian $Q \in \mathbb{R}^{2n \times 2n}$ has the diagonal blocks $Q_{ii} = \sum_{j \sim i} \kappa_{ij} I$ and, for each edge, $Q_{ij} = -\kappa_{ij} \tilde R_{ij}$ and $Q_{ji} = Q_{ij}^\top$. In SE-Sync for poses, the translations are removed in closed form, and the rotations face a problem of the same form, $\min \mathrm{tr}(\tilde Q R^\top R)$, with a different symmetric matrix $\tilde Q$. Claims 2 to 5 use only that $Q$ is symmetric, so they hold for $\tilde Q$ too.

The problems are:

- (P) $\min \mathrm{tr}(Q R^\top R)$ over $R \in SO(2)^n$;
- (SDP) $\min \mathrm{tr}(Q Z)$ over symmetric $Z \succeq 0$ with $Z_{ii} = I_2$ for each $i$;
- (BM$_r$) $\min f(Y) = \mathrm{tr}(Q Y^\top Y)$ over $Y = [Y_1 \cdots Y_n]$ with $Y_i \in \mathbb{R}^{r \times 2}$ and $Y_i^\top Y_i = I_2$.

For $Y$ in (BM$_r$), let $\Lambda(Y)$ be block diagonal with $\Lambda_{ii} = \mathrm{Sym}\big((Q Y^\top Y)_{ii}\big)$, where $\mathrm{Sym}(A) = (A + A^\top)/2$, and let $S(Y) = Q - \Lambda(Y)$.

**Assumptions.** (A1) Exact arithmetic. In the code, "zero" and "positive semidefinite" are checked with small tolerances.

**Claim 1 (the cost).** $F(R) = \mathrm{tr}(Q R^\top R)$ for $R \in O(2)^n$.

*Proof.* For one edge, $\|R_j - R_i \tilde R\|_F^2 = \mathrm{tr}(R_j^\top R_j) + \mathrm{tr}(\tilde R^\top R_i^\top R_i \tilde R) - 2\,\mathrm{tr}(R_j^\top R_i \tilde R)$. The trace form collects $\kappa\,\mathrm{tr}(R_i^\top R_i) + \kappa\,\mathrm{tr}(R_j^\top R_j)$ from the diagonal blocks, and $\mathrm{tr}(Q_{ij} R_j^\top R_i) + \mathrm{tr}(Q_{ji} R_i^\top R_j) = -2\kappa\,\mathrm{tr}(\tilde R R_j^\top R_i)$ from the two off-diagonal blocks. Since $\tilde R$ is orthogonal, $\mathrm{tr}(\tilde R^\top R_i^\top R_i \tilde R) = \mathrm{tr}(R_i^\top R_i)$, and the two sums agree term by term. $\square$

**Claim 2 (the chain of bounds).** $\min(\mathrm{SDP}) \le \min(\mathrm{P})$, and $f(Y) \ge \min(\mathrm{SDP})$ for every $Y$ in (BM$_r$).

*Proof.* For $R \in SO(2)^n$ or for any feasible $Y$, $Z = Y^\top Y$ is positive semidefinite and $Z_{ii} = Y_i^\top Y_i = I$, so it is feasible for (SDP), with the same cost. $\square$

**Claim 3 (the gradient).** The Riemannian gradient of $f$ at $Y$ is $2\,Y S(Y)$. So $Y$ is a first order critical point if and only if $Y S(Y) = 0$.

*Proof.* The Euclidean gradient of $f$ is $2 Y Q$, and its block $i$ is $\xi_i = 2 \sum_j Y_j Q_{ji}$. The tangent space of $\{Y_i^\top Y_i = I\}$ at $Y_i$ is $\{\dot Y_i : Y_i^\top \dot Y_i + \dot Y_i^\top Y_i = 0\}$, and the projection onto it is $\xi_i \mapsto \xi_i - Y_i \mathrm{Sym}(Y_i^\top \xi_i)$. Here $Y_i^\top \xi_i = 2 (Y^\top Y Q)_{ii}$, which is the transpose of $2 (Q Y^\top Y)_{ii}$, so $\mathrm{Sym}(Y_i^\top \xi_i) = 2 \Lambda_{ii}$. The projected block is $2\big((Y Q)_i - Y_i \Lambda_{ii}\big) = 2 (Y S)_i$. $\square$

**Claim 4 (the certificate).** If $Y S(Y) = 0$ and $S(Y) \succeq 0$, then $Z^\star = Y^\top Y$ solves (SDP), and $f(Y) = \min(\mathrm{SDP})$.

*Proof.* Let $\Lambda = \Lambda(Y)$ and $S = S(Y)$. For any feasible $Z$, since $\Lambda$ is block diagonal with symmetric blocks and $Z_{ii} = I$, $\mathrm{tr}(\Lambda Z) = \sum_i \mathrm{tr}(\Lambda_{ii}) = \mathrm{tr}(\Lambda)$. So $\mathrm{tr}(Q Z) = \mathrm{tr}(S Z) + \mathrm{tr}(\Lambda) \ge \mathrm{tr}(\Lambda)$, because the trace of the product of two positive semidefinite matrices is nonnegative. At $Z^\star$, $\mathrm{tr}(S Y^\top Y) = \mathrm{tr}(Y S Y^\top) = 0$, so $\mathrm{tr}(Q Z^\star) = \mathrm{tr}(\Lambda)$, the smallest value. This is weak duality with the dual variable $\Lambda$ of the constraints $Z_{ii} = I$. $\square$

**Claim 5 (the staircase step).** Let $Y$ be in (BM$_r$) with $Y S(Y) = 0$, and let $v \in \mathbb{R}^{2n}$ be a unit vector with $v^\top S v = \lambda < 0$. Let $Y^+ = [Y; 0] \in$ (BM$_{r+1}$), $\dot Y = [0; v^\top]$, and $Y'(\alpha)$ the blockwise polar factor of $Y^+ + \alpha \dot Y$. Then $f(Y'(\alpha)) = f(Y) + \alpha^2 \lambda + O(\alpha^4)$, so a small enough step decreases the cost.

*Proof.* $Y^+$ has the same cost as $Y$ and lies in (BM$_{r+1}$). Each block $\dot Y_i$ is nonzero only in the new row, where $Y^+_i$ is zero, so $(Y^+)^\top \dot Y = 0$ and $\dot Y$ is tangent. Let $v_i$ be the two entries of $v$ for block $i$, and $D$ block diagonal with $D_{ii} = v_i v_i^\top$. Then $(Y^+_i + \alpha \dot Y_i)^\top (Y^+_i + \alpha \dot Y_i) = I + \alpha^2 D_{ii}$, so the polar factor is $(Y^+ + \alpha \dot Y) M$ with $M = I - \tfrac{\alpha^2}{2} D + O(\alpha^4)$. With $W = (Y^+ + \alpha \dot Y)^\top (Y^+ + \alpha \dot Y) = Y^\top Y + \alpha^2 v v^\top$,
$$f(Y') = \mathrm{tr}(Q M W M) = f(Y) + \alpha^2 v^\top Q v - \tfrac{\alpha^2}{2}\mathrm{tr}\big(D (Y^\top Y Q + Q Y^\top Y)\big) + O(\alpha^4).$$
$D$ is block diagonal and symmetric, so the middle trace is $\sum_i \mathrm{tr}\big(D_{ii} \cdot 2\Lambda_{ii}\big) = 2 v^\top \Lambda v$. Hence $f(Y') = f(Y) + \alpha^2 v^\top (Q - \Lambda) v + O(\alpha^4) = f(Y) + \alpha^2 \lambda + O(\alpha^4)$. The line search halves $\alpha$ until the cost decreases, which happens after finitely many halvings. $\square$

**Claim 6 (rounding and global optimality).** Let $Y$ satisfy the conditions of Claim 4. If $Y$ has rank 2, let $R = U_2^\top Y$, where $U_2$ holds the two top left singular vectors of $Y$. Then $R^\top R = Y^\top Y$ and every $R_i$ is in $O(2)$. If, after the sign fix of the code, every $\det R_i = 1$, then $R$ is a global minimizer of (P) and $F(R) = f(Y)$. In all cases, $f(Y) \le \min(\mathrm{P}) \le F(\hat R)$ for the rounded $\hat R$.

*Proof.* The columns of $Y$ lie in the span of $U_2$, so $U_2 U_2^\top Y = Y$ and $R^\top R = Y^\top U_2 U_2^\top Y = Y^\top Y$. Then $R_i^\top R_i = (Y^\top Y)_{ii} = I$. Changing the sign of the second row of $R$ multiplies every $\det R_i$ by $-1$ and does not change $R^\top R$. If all determinants are 1, then $R$ is feasible for (P), and by Claims 1, 2 and 4, $F(R) = \mathrm{tr}(Q R^\top R) = f(Y) = \min(\mathrm{SDP}) \le \min(\mathrm{P}) \le F(R)$. The last statement follows from Claims 2 and 4 and the feasibility of $\hat R$. The projection of each block onto $SO(2)$ and the multiplication by $\hat R_1^\top$ keep $\hat R$ feasible and, for the second, do not change $F$. $\square$

**What this does not show.** It does not show that the relaxation is tight. Rosen et al. prove that it is tight when the noise is below a level that depends on the graph; above that level, the rank of the certified $Y$ can exceed 2, and the gap $F(\hat R) - f(Y)$ only bounds the suboptimality of $\hat R$. It does not show that the local search reaches a critical point; block coordinate descent decreases $f$ at every step, and the code checks the gradient and the eigenvalue with tolerances. It does not bound the rank at which the staircase stops; Boumal, Voroninski and Bandeira give such a bound for generic problems, and the code stops at a fixed largest rank.
