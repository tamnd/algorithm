---
title: The eigenvector of the largest eigenvalue of K minimizes Wahba's loss
proves: [correctness]
status: full
---

**Setting.** The data are unit vectors $b_i$ (body frame) and $r_i$ (reference frame) with weights $a_i > 0$, $i = 1, \ldots, n$. The loss of a rotation $A$ is

$$L(A) = \tfrac{1}{2} \sum_i a_i |b_i - A r_i|^2 .$$

Line L1 forms $B = \sum_i a_i b_i r_i^T$ and $\lambda_0 = \sum_i a_i$. Lines L2 and L3 form $\sigma = \operatorname{tr} B$, $S = B + B^T$, $z = (B_{23} - B_{32}, B_{31} - B_{13}, B_{12} - B_{21})^T$ and

$$K = \begin{pmatrix} \sigma & z^T \\ z & S - \sigma I \end{pmatrix}.$$

A unit quaternion $q = (q_0, e)$, scalar first, gives the rotation $R(q) = (q_0^2 - e^T e) I + 2 e e^T + 2 q_0 [e]_\times$ in the Hamilton convention. The algorithm returns $q$, and the attitude is $A(q) = R(q)^T$.

**Assumptions.**

- (D) $|b_i| = |r_i| = 1$. The code normalizes its input, so this holds for any nonzero input.
- (S) Line L4 returns an orthonormal basis of eigenvectors of $K$ with their eigenvalues. This is exact in the claim. The cyclic Jacobi method of the code converges to such a basis for every real symmetric matrix; see [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/).

**Claim.** Let $\lambda_{\max}$ be the largest eigenvalue of $K$ and $q$ a unit eigenvector for it. Then $A(q)$ minimizes $L$ over $SO(3)$, and the minimum is $\lambda_0 - \lambda_{\max}$. If $\lambda_{\max}$ is a simple eigenvalue, the minimizer is unique. Also $\operatorname{tr} K = 0$ and $\lambda_{\max} \le \lambda_0$.

*Proof.*

*Step 1: the loss is linear in $A$.* By (D), $|b_i - A r_i|^2 = 2 - 2 b_i^T A r_i$, so

$$L(A) = \lambda_0 - \sum_i a_i b_i^T A r_i = \lambda_0 - \operatorname{tr}(A B^T),$$

because $b_i^T A r_i = \operatorname{tr}(A r_i b_i^T)$ and $\sum_i a_i r_i b_i^T = B^T$.

*Step 2: the gain is a quadratic form in $q$.* With $A = R(q)^T = (q_0^2 - e^T e) I + 2 e e^T - 2 q_0 [e]_\times$,

- $\operatorname{tr}((q_0^2 - e^T e) B^T) = (q_0^2 - e^T e) \sigma$,
- $\operatorname{tr}(2 e e^T B^T) = 2 e^T B e = e^T S e$,
- $\operatorname{tr}(-2 q_0 [e]_\times B^T) = -2 q_0 \sum_{j,k} ([e]_\times)_{jk} B_{jk}$. Written out, the sum is $e_1 (B_{32} - B_{23}) + e_2 (B_{13} - B_{31}) + e_3 (B_{21} - B_{12}) = -z^T e$, so the term is $2 q_0 z^T e$.

The sum is $q_0^2 \sigma + 2 q_0 z^T e + e^T (S - \sigma I) e = q^T K q$. So for every unit $q$,

$$L(A(q)) = \lambda_0 - q^T K q .$$

*Step 3: maximize the quadratic form.* The map $q \mapsto R(q)$ from the unit sphere in $\mathbb{R}^4$ onto $SO(3)$ is onto (every rotation has an axis $u$ and an angle $\theta$, and $q = (\cos(\theta/2), \sin(\theta/2) u)$ maps to it). So minimizing $L$ over $SO(3)$ is the same as maximizing $q^T K q$ over unit $q$. $K$ is real and symmetric, so by the spectral theorem it has an orthonormal eigenbasis $q^{(1)}, \ldots, q^{(4)}$ with eigenvalues $\lambda_1 \le \cdots \le \lambda_4 = \lambda_{\max}$. For a unit $q = \sum_k c_k q^{(k)}$, $q^T K q = \sum_k \lambda_k c_k^2 \le \lambda_{\max} \sum_k c_k^2 = \lambda_{\max}$, with equality exactly when $c_k = 0$ for every $k$ with $\lambda_k < \lambda_{\max}$. So the eigenvector of line L6 is a maximizer, the minimum loss is $\lambda_0 - \lambda_{\max}$ (line L7), and when $\lambda_{\max}$ is simple the maximizers are $\pm q^{(4)}$, which give the same rotation. Line L6 picks the sign with $q_0 \ge 0$; it does not change $A$.

*Step 4: the two facts about $K$.* $\operatorname{tr} K = \sigma + \operatorname{tr} S - 3 \sigma = \sigma + 2 \sigma - 3 \sigma = 0$. And $L \ge 0$ for every $A$, so $\lambda_0 - \lambda_{\max} \ge 0$. $\blacksquare$

**Remarks.**

- If $\lambda_{\max}$ is not simple, every unit vector in its eigenspace is optimal, and the problem has many solutions. This happens when the data do not fix the attitude, for example when all $b_i$ are parallel. With two or more non-parallel pairs and exact data, $\lambda_{\max} = \lambda_0$ is simple.
- In floating point, the Jacobi method returns eigenvalues with an absolute error of a small multiple of $\varepsilon \|K\|$ for unit roundoff $\varepsilon$. The eigenvector error is that amount divided by the gap $\lambda_4 - \lambda_3$. A small gap means the attitude is poorly fixed by the data, so this error is of the same size as the statistical uncertainty of the answer.
