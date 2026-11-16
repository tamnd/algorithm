---
title: QUEST finds the largest eigenvalue by a monotone Newton iteration and the optimal quaternion by an adjugate column
proves: [correctness]
status: full
---

**Setting.** The notation is that of the [q-method](/davenport-q-method/): unit vectors $b_i, r_i$, weights $a_i > 0$, $\lambda_0 = \sum_i a_i$, $B = \sum_i a_i b_i r_i^T$, $\sigma = \operatorname{tr} B$, $S = B + B^T$, $z = (B_{23} - B_{32}, B_{31} - B_{13}, B_{12} - B_{21})^T$, and

$$K = \begin{pmatrix} \sigma & z^T \\ z & S - \sigma I \end{pmatrix}.$$

The proof of the q-method shows that the optimal attitude is given by a unit eigenvector $q$ of $K$ for its largest eigenvalue $\lambda_{\max}$, and that the minimum loss is $\lambda_0 - \lambda_{\max}$. Let $\kappa = \operatorname{tr} \operatorname{adj} S$ and $\Delta = \det S$, so that $\det(\mu I - S) = \mu^3 - 2 \sigma \mu^2 + \kappa \mu - \Delta$. For a real $\lambda$ put $\mu = \lambda + \sigma$ and

$$\alpha = \lambda^2 - \sigma^2 + \kappa, \quad \beta = \lambda - \sigma, \quad \gamma = (\lambda + \sigma) \alpha - \Delta, \quad x = (\alpha I + \beta S + S^2) z ,$$

$$\psi(\lambda) = \lambda^4 - (a + b) \lambda^2 - c \lambda + (a b + c \sigma - d),$$

with $a = \sigma^2 - \kappa$, $b = \sigma^2 + z^T z$, $c = \Delta + z^T S z$ and $d = z^T S^2 z$.

**Assumptions.**

- (D) $|b_i| = |r_i| = 1$ and $a_i > 0$.
- (U) $\lambda_{\max}$ is a simple eigenvalue of $K$. This holds when the data fix the attitude; see the remarks of the q-method proof.
- (X) Arithmetic is exact. The remarks discuss rounding.

**Claim.**

1. $\psi(\lambda) = \det(\lambda I - K)$, and $(\gamma, x)$ is the first column of $\operatorname{adj}(\lambda I - K)$, for every real $\lambda$.
2. Newton's method on $\psi$ from $\lambda_0$ (lines L2 to L4) gives a nonincreasing sequence that converges to $\lambda_{\max}$.
3. At $\lambda = \lambda_{\max}$, $(\gamma, x) = \psi'(\lambda_{\max}) \, q_0 \, q$. So when $q_0 \ne 0$, $(\gamma, x) / |(\gamma, x)| = \pm q$ (line L8), and $|(\gamma, x)| = |\psi'(\lambda_{\max})| \, |q_0|$.
4. At least one of the four frames of line L5 has $|(\gamma, x)| \ge \tfrac{1}{2} |\psi'(\lambda_{\max})| > 0$, and the quaternion of line L8 in that frame gives the optimal attitude.

*Proof.*

*Claim 1.* Write $M = \lambda I - K$ in blocks: $M_{11} = \lambda - \sigma$, $M_{21} = -z$, $M_{22} = \mu I - S$. First, $\gamma = \det M_{22}$, because $\mu^3 - 2 \sigma \mu^2 + \kappa \mu - \Delta = \mu (\mu^2 - 2 \sigma \mu + \kappa) - \Delta$ and $\mu^2 - 2 \sigma \mu = \lambda^2 - \sigma^2$. Next, by the Cayley-Hamilton theorem for $S$, $S^3 = 2 \sigma S^2 - \kappa S + \Delta I$. Then

$$M_{22} (\alpha I + \beta S + S^2) = \mu \alpha I + (\mu \beta - \alpha) S + (\mu - \beta) S^2 - S^3 .$$

Here $\mu - \beta = 2 \sigma$, so the last two terms are $2 \sigma S^2 - S^3 = \kappa S - \Delta I$, and $\mu \beta - \alpha + \kappa = (\lambda^2 - \sigma^2) - (\lambda^2 - \sigma^2 + \kappa) + \kappa = 0$. So $M_{22} (\alpha I + \beta S + S^2) = \gamma I$, which means $\alpha I + \beta S + S^2 = \operatorname{adj} M_{22}$. Now compute $M (\gamma, x)$. The lower block is $-\gamma z + M_{22} x = -\gamma z + \gamma z = 0$. The top entry is

$$\phi(\lambda) = (\lambda - \sigma) \gamma - z^T (\alpha I + \beta S + S^2) z .$$

Expanding, with $z^T z$, $z^T S z = c - \Delta$ and $d$:

$$\phi = (\lambda^2 - \sigma^2)(\lambda^2 - \sigma^2 + \kappa) - (\lambda - \sigma) \Delta - (\lambda^2 - \sigma^2 + \kappa) z^T z - (\lambda - \sigma) z^T S z - d .$$

The coefficient of $\lambda^2$ is $-2 \sigma^2 + \kappa - z^T z = -(a + b)$. The coefficient of $\lambda$ is $-\Delta - z^T S z = -c$. The constant is $\sigma^4 - \kappa \sigma^2 + \sigma^2 z^T z - \kappa z^T z + \sigma \Delta + \sigma z^T S z - d = a b + c \sigma - d$. So $\phi = \psi$. When $\gamma = \det M_{22} \ne 0$, the Schur complement gives $\det M = \det M_{22} \, (M_{11} - z^T M_{22}^{-1} z) = (\lambda - \sigma) \gamma - z^T \operatorname{adj}(M_{22}) z = \psi(\lambda)$. Both sides are polynomials in $\lambda$ that agree at all but at most three points, so $\psi(\lambda) = \det(\lambda I - K)$ for all $\lambda$. Finally, $M (\gamma, x) = \psi(\lambda) e_1 = \det(M) e_1 = M \operatorname{adj}(M) e_1$. When $M$ is invertible this gives $(\gamma, x) = \operatorname{adj}(M) e_1$, and again both sides are polynomials in $\lambda$, so the identity holds for every $\lambda$.

*Claim 2.* $K$ is real and symmetric, so $\psi$ has four real roots $\lambda_1 \le \lambda_2 \le \lambda_3 \le \lambda_4 = \lambda_{\max}$. By Rolle's theorem the roots of $\psi'$ and of $\psi''$ are real and lie in $[\lambda_1, \lambda_4]$. The leading coefficients of $\psi, \psi', \psi''$ are positive, so for $\lambda > \lambda_{\max}$ all three are positive: $\psi$ is increasing and convex on $(\lambda_{\max}, \infty)$. The proof of the q-method gives $\lambda_{\max} \le \lambda_0$. If $\lambda_0 = \lambda_{\max}$, then $\psi(\lambda_0) = 0$ and the first step is zero. Otherwise, let $\lambda > \lambda_{\max}$. The Newton step $\lambda' = \lambda - \psi(\lambda) / \psi'(\lambda)$ satisfies $\lambda' < \lambda$, since $\psi$ and $\psi'$ are positive. By convexity, the tangent line at $\lambda$ lies below $\psi$ on $[\lambda_{\max}, \lambda]$ and is negative at $\lambda_{\max}$, so its root $\lambda'$ is at least $\lambda_{\max}$. So the iterates decrease and stay at or above $\lambda_{\max}$. They converge to some $\ell \ge \lambda_{\max}$, and the step $\psi(\ell) / \psi'(\ell)$ must be $0$ at the limit, so $\psi(\ell) = 0$ and $\ell = \lambda_{\max}$. Under (U), $\psi'(\lambda_{\max}) \ne 0$ and the convergence is quadratic.

*Claim 3.* For $\lambda$ not an eigenvalue, $\operatorname{adj}(\lambda I - K) = \det(\lambda I - K) (\lambda I - K)^{-1} = \sum_k \prod_{j \ne k} (\lambda - \lambda_j) \, q^{(k)} q^{(k) T}$ in an orthonormal eigenbasis. This is a polynomial identity, so it holds at $\lambda = \lambda_4$, where every term but $k = 4$ has the factor $\lambda_4 - \lambda_4 = 0$. So $\operatorname{adj}(\lambda_{\max} I - K) = \psi'(\lambda_{\max}) \, q q^T$ with $q = q^{(4)}$, because $\psi'(\lambda_4) = \prod_{j \ne 4} (\lambda_4 - \lambda_j)$. By Claim 1, the first column is $(\gamma, x) = \psi'(\lambda_{\max}) q_0 q$. Its norm is $|\psi'(\lambda_{\max})| \, |q_0|$, since $|q| = 1$.

*Claim 4.* For $k = 1, 2, 3$, let $P_k$ be the rotation by $\pi$ about $e_k$, the diagonal matrix with $1$ in place $k$ and $-1$ in the other two places. Line L5 replaces the reference vectors by $r_i' = P_k r_i$. Since $P_k^{-1} = P_k$, $b_i = A r_i = (A P_k) r_i'$, so the new problem has the attitude $A' = A P_k$ and the profile $B' = \sum_i a_i b_i r_i'^T = B P_k$. Its loss is the same function of the data, so its $\lambda_{\max}$ is the same and the Newton result is reused. In terms of $R = A^T$, $R' = P_k R$, and the quaternion of $P_k$ is $(0, e_k)$, so $q' = (0, -e_k) \otimes q$ up to sign. The scalar part of $(0, -e_k) \otimes (q_0, e)$ is $-(-e_k) \cdot e = q_k$. So the four frames (none, $x$, $y$, $z$) have $|q_0'| = |q_0|, |q_1|, |q_2|, |q_3|$. These four numbers have squares that sum to $1$, so the largest is at least $\tfrac{1}{2}$. By Claim 3, line L7 accepts a frame exactly when its $|q_0'| \ge \tfrac{1}{2}$, so it accepts one, and in that frame $(\gamma, x) \ne 0$ because $\psi'(\lambda_{\max}) \ne 0$ under (U). Line L8 normalizes to $\pm q'$ and returns $(0, e_k) \otimes q' = \pm q$. Both signs give the same attitude, which is optimal by the q-method proof. $\blacksquare$

**Remarks.**

- With rounding, $\lambda$ is a few units of roundoff away from $\lambda_{\max}$, and $(\gamma, x)$ is computed at that $\lambda$. Claim 3 shows why a frame with $|q_0|$ near $0$ is bad: the column is then the difference of large terms that should cancel, and its direction carries a relative error of order $\varepsilon / |q_0|$. The rule $|q_0| \ge \tfrac{1}{2}$ bounds that factor by $2$.
- If $\lambda_{\max}$ is a double root, $\psi'(\lambda_{\max}) = 0$, Newton converges only linearly, and the adjugate is the zero matrix, so no frame works: every column is zero up to rounding, and its direction means nothing. The code raises an error only when all four columns are exactly zero. The problem then has a whole set of solutions, and the q-method with a full eigensolver is the right tool.
