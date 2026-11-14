---
title: Henderson's equations give the GLS estimate of b with V = ZGZ^T + R and the best linear unbiased predictor of u
proves: [correctness, termination]
status: full
---

The arithmetic is exact. $X$ is $n \times p$ of rank $p$, $Z$ is $n \times q$, $G$ ($q \times q$) and $R$ ($n \times n$) are symmetric positive definite, $V = ZGZ^\top + R$, $M = Z^\top R^{-1}Z + G^{-1}$, $A = X^\top V^{-1}X$ and $P = V^{-1} - V^{-1}XA^{-1}X^\top V^{-1}$. The vector $b$ holds the fixed-effect coefficients. The coefficient matrix and right-hand side built by lines L1 to L5 are

$$C = \begin{pmatrix} X^\top R^{-1}X & X^\top R^{-1}Z \\ Z^\top R^{-1}X & M \end{pmatrix}, \qquad r = \begin{pmatrix} X^\top R^{-1}y \\ Z^\top R^{-1}y \end{pmatrix}.$$

**Lemma 1 (C is positive definite).** $C$ is symmetric positive definite, so every pivot of the $LDL^\top$ factor in line L6 is positive, line L7 returns the unique solution, and the algorithm stops after a fixed number of steps.

*Proof.* With $W = [X\ Z]$, $C = W^\top R^{-1}W + \operatorname{diag}(0, G^{-1})$. For $v = (v_1, v_2) \ne 0$, $v^\top Cv = w^\top R^{-1}w + v_2^\top G^{-1}v_2$ with $w = Xv_1 + Zv_2$. Both terms are at least 0. If $v_2 \ne 0$ the second is positive. If $v_2 = 0$ then $v_1 \ne 0$, $w = Xv_1 \ne 0$ because $X$ has rank $p$, and the first is positive. The pivots of $LDL^\top$ are ratios of consecutive leading principal minors of $C$, which are positive for a positive definite matrix. $V$ is positive definite too, as the sum of the positive semidefinite $ZGZ^\top$ and the positive definite $R$, and $M$ is positive definite, as $G^{-1}$ plus a positive semidefinite matrix; so $V^{-1}$, $M^{-1}$ and $A^{-1}$ below exist. $\square$

**Lemma 2 (push-through and the inverse of V).** $M^{-1}Z^\top R^{-1} = GZ^\top V^{-1}$ and $V^{-1} = R^{-1} - R^{-1}ZM^{-1}Z^\top R^{-1}$.

*Proof.* $Z^\top R^{-1}V = Z^\top R^{-1}ZGZ^\top + Z^\top = (Z^\top R^{-1}Z + G^{-1})GZ^\top = MGZ^\top$. Multiplying on the left by $M^{-1}$ and on the right by $V^{-1}$ gives the first identity. For the second, $(R^{-1} - R^{-1}ZM^{-1}Z^\top R^{-1})V = R^{-1}V - R^{-1}ZM^{-1}(MGZ^\top) = (R^{-1}ZGZ^\top + I) - R^{-1}ZGZ^\top = I$. This is the [Woodbury identity](/woodbury-identity/) for this $V$. $\square$

**Theorem 1 (the fixed effects are GLS).** The solution $(\hat b, \tilde u)$ of $Cs = r$ satisfies $A\hat b = X^\top V^{-1}y$, so $\hat b = (X^\top V^{-1}X)^{-1}X^\top V^{-1}y$, and $\tilde u = GZ^\top V^{-1}(y - X\hat b)$.

*Proof.* The second block row is $Z^\top R^{-1}X\hat b + M\tilde u = Z^\top R^{-1}y$, so $\tilde u = M^{-1}Z^\top R^{-1}(y - X\hat b) = GZ^\top V^{-1}(y - X\hat b)$ by Lemma 2. Put $\tilde u = M^{-1}Z^\top R^{-1}(y - X\hat b)$ into the first block row $X^\top R^{-1}X\hat b + X^\top R^{-1}Z\tilde u = X^\top R^{-1}y$ and collect terms:

$$X^\top(R^{-1} - R^{-1}ZM^{-1}Z^\top R^{-1})X\hat b = X^\top(R^{-1} - R^{-1}ZM^{-1}Z^\top R^{-1})y.$$

By Lemma 2 the matrix in parentheses is $V^{-1}$, which gives $A\hat b = X^\top V^{-1}y$. $\square$

So $\hat b$ is the [generalized least squares](/generalized-least-squares/) estimate for $\operatorname{Cov}(y) = V$, which is the best linear unbiased estimator of $b$ by Aitken's theorem. Note also that $V^{-1}(y - X\hat b) = Py$, so $\tilde u = GZ^\top Py$.

**Theorem 2 (BLUP).** Let $k \in \mathbb R^p$ lie in the row space of $X$ and $m \in \mathbb R^q$. Among all linear predictors $\ell^\top y$ with $E[\ell^\top y - k^\top b - m^\top u] = 0$ for every $b$, the one with the smallest mean squared error $E[(\ell^\top y - k^\top b - m^\top u)^2]$ is $k^\top\hat b + m^\top\tilde u$, and it is unique.

*Proof.* Since $E[y] = Xb$ and $E[u] = 0$, the unbiasedness condition is $(X^\top\ell - k)^\top b = 0$ for every $b$, that is $X^\top\ell = k$; this set is not empty because $k$ is in the row space of $X$. For such $\ell$ the error has mean 0, and with $\operatorname{Cov}(y, u) = \operatorname{Cov}(Zu + e, u) = ZG$,

$$\mathrm{MSE}(\ell) = \operatorname{Var}(\ell^\top y - m^\top u) = \ell^\top V\ell - 2\ell^\top ZGm + m^\top Gm.$$

Let $\ell^* = V^{-1}ZGm + V^{-1}XA^{-1}(k - X^\top V^{-1}ZGm)$. Then $X^\top\ell^* = X^\top V^{-1}ZGm + (k - X^\top V^{-1}ZGm) = k$, so $\ell^*$ is unbiased, and $V\ell^* - ZGm = X\lambda$ with $\lambda = A^{-1}(k - X^\top V^{-1}ZGm)$. Any other unbiased $\ell$ is $\ell^* + \delta$ with $X^\top\delta = 0$, and

$$\mathrm{MSE}(\ell^* + \delta) - \mathrm{MSE}(\ell^*) = 2\delta^\top(V\ell^* - ZGm) + \delta^\top V\delta = 2(X^\top\delta)^\top\lambda + \delta^\top V\delta = \delta^\top V\delta,$$

which is positive unless $\delta = 0$, because $V$ is positive definite. So $\ell^*$ is the unique best predictor. Finally,

$$\ell^{*\top}y = m^\top GZ^\top V^{-1}y + (k - X^\top V^{-1}ZGm)^\top A^{-1}X^\top V^{-1}y = m^\top GZ^\top V^{-1}y + k^\top\hat b - m^\top GZ^\top V^{-1}X\hat b,$$

using $A^{-1}X^\top V^{-1}y = \hat b$ from Theorem 1, and this is $k^\top\hat b + m^\top GZ^\top V^{-1}(y - X\hat b) = k^\top\hat b + m^\top\tilde u$. $\square$

With $k = 0$ and $m$ a unit vector, each coordinate $\tilde u_j$ is the BLUP of $u_j$; with $m = 0$, $k^\top\hat b$ is the BLUE of $k^\top b$.

**Theorem 3 (the blocks of the inverse).** Write $C^{-1}$ in blocks $C^{11}$ ($p \times p$) and $C^{22}$ ($q \times q$). Then $C^{11} = A^{-1} = \operatorname{Cov}(\hat b)$ and $C^{22} = G - GZ^\top PZG = \operatorname{Cov}(\tilde u - u)$.

*Proof.* By the block inverse formula with the [Schur complement](/schur-complement/) of the lower block $M$,

$$C^{11} = (X^\top R^{-1}X - X^\top R^{-1}ZM^{-1}Z^\top R^{-1}X)^{-1} = (X^\top V^{-1}X)^{-1} = A^{-1}$$

by Lemma 2, and $C^{22} = M^{-1} + M^{-1}Z^\top R^{-1}XA^{-1}X^\top R^{-1}ZM^{-1}$. By Lemma 2, $M^{-1}Z^\top R^{-1}X = GZ^\top V^{-1}X$, so the second term is $GZ^\top V^{-1}XA^{-1}X^\top V^{-1}ZG$. Also $M^{-1} = G - GZ^\top V^{-1}ZG$, because $G - GZ^\top V^{-1}ZG = G - M^{-1}Z^\top R^{-1}ZG = M^{-1}(M - Z^\top R^{-1}Z)G = M^{-1}G^{-1}G = M^{-1}$. Adding, $C^{22} = G - GZ^\top(V^{-1} - V^{-1}XA^{-1}X^\top V^{-1})ZG = G - GZ^\top PZG$.

For the covariances: $\hat b = A^{-1}X^\top V^{-1}y$ has $\operatorname{Cov}(\hat b) = A^{-1}X^\top V^{-1}VV^{-1}XA^{-1} = A^{-1}$. For the prediction error, $\tilde u - u = GZ^\top Py - u$. Direct multiplication gives $PVP = P$, and $\operatorname{Cov}(Py, u) = PZG$, so

$$\operatorname{Cov}(\tilde u - u) = GZ^\top PVPZG - GZ^\top PZG - GZ^\top PZG + G = G - GZ^\top PZG. \qquad \square$$

Lines L8 and L9 return exactly these quantities. The implementation checks Theorems 1 and 3 with rational arithmetic against the direct formulas with $V^{-1}$ on random problems.
