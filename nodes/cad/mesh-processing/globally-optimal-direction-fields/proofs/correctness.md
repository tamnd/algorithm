---
title: The smoothest field of the relaxed problem is the eigenvector of the smallest eigenvalue, inverse iteration finds it, and the face indices add up to the Euler characteristic
proves: [correctness, termination]
status: full
---

**Setting.** $M$ is a connected, oriented triangle mesh with vertices $1, \dots, V$, faces oriented by the right-hand rule, and an integer $n \ge 1$. The frame angles $\varphi_i(j)$, the transports $r_{ij}$, the weights $w_{ij}$, the matrix $A$ and the diagonal matrix $M$ of vertex areas are as on the page, and the algorithm is lines L1 to L11 of the page. Every vertex is in a triangle of positive area, so every diagonal entry $m_i$ of $M$ is positive. $R(u) = u^* A u / u^* M u$ for $u \ne 0$. Eigenvalues of $Au = \lambda Mu$ are listed with repetition as $\lambda_1 \le \lambda_2 \le \dots \le \lambda_V$.

**Claim.**

1. $E(u) = u^* A u$ with $A$ Hermitian. If all $w_{ij} > 0$, then $A$ is positive semidefinite.
2. $\min_{u \ne 0} R(u) = \lambda_1$, and $R(u) = \lambda_1$ exactly when $u$ is an eigenvector for $\lambda_1$. Every local minimizer of $R$ is such an eigenvector.
3. If $A$ is positive semidefinite and $\sigma > 0$, line L5 succeeds. If the start of line L6 has a nonzero component in the eigenspace of $\lambda_1$, the iterates of lines L7 and L8 converge to that eigenspace, and the residual of line L10 tends to 0.
4. The algorithm terminates. A returned pair has $u^* M u = 1$, $\lambda = u^* A u \ge \lambda_1$, and some eigenvalue $\lambda_k$ with $\lvert \lambda_k - \lambda \rvert \le \delta \max(1, \lambda)$.
5. Each face index $I(f)$ is a multiple of $1/n$. On a closed mesh, $\sum_f I(f) = \chi$, when no $u_i$ is zero and no turn $\tau$ is exactly $\pi$.

**Proof of 1.** For one edge, with $a = u_i$ and $b = u_j$,

$$\lvert b - r a \rvert^2 = (b - ra)^*(b - ra) = \lvert a\rvert^2 + \lvert b\rvert^2 - \bar b\, r\, a - \bar a\, \bar r\, b,$$

because $\lvert r\rvert = 1$. Multiplied by $w_{ij}$, these are the four entries $A_{ii} \mathrel{+}= w_{ij}$, $A_{jj} \mathrel{+}= w_{ij}$, $A_{ji} \mathrel{-}= w_{ij} r_{ij}$ and $A_{ij} \mathrel{-}= w_{ij} \bar r_{ij}$ of line L3. Summing over the edges gives $E(u) = u^* A u$. The diagonal is real, and $A_{ij} = \overline{A_{ji}}$, so $A$ is Hermitian. If all $w_{ij} > 0$, $E$ is a sum of nonnegative terms, so $u^* A u \ge 0$ for all $u$. $\square$

**Proof of 2.** $M$ is diagonal with positive entries, so $M^{1/2}$ and $M^{-1/2}$ exist. Put $v = M^{1/2} u$ and $B = M^{-1/2} A M^{-1/2}$. $B$ is Hermitian, $u^* M u = v^* v$ and $u^* A u = v^* B v$, so $R(u) = v^* B v / v^* v$. Also $Au = \lambda M u$ exactly when $B v = \lambda v$, so $B$ has the eigenvalues $\lambda_k$. By the spectral theorem, $B$ has an orthonormal basis of eigenvectors $q_1, \dots, q_V$ with $B q_k = \lambda_k q_k$. Write $v = \sum_k c_k q_k$. Then

$$R(u) = \frac{\sum_k \lambda_k \lvert c_k\rvert^2}{\sum_k \lvert c_k\rvert^2} \ge \lambda_1,$$

with equality exactly when $c_k = 0$ for every $k$ with $\lambda_k > \lambda_1$, that is, when $v$ is in the eigenspace of $\lambda_1$. The value $\lambda_1$ is reached at $v = q_1$.

For the local minimizers: let $u$ be a local minimizer and $v = M^{1/2} u$. The quotient is smooth at $v \ne 0$, and its derivative in the direction $h$ is $2\,\mathrm{Re}(h^*(Bv - R v)) / v^* v$. At a local minimizer it vanishes for all $h$, so $B v = R(u) v$: $v$ is an eigenvector, for some eigenvalue $\mu$. If $\mu > \lambda_1$, take a unit eigenvector $q$ of $\lambda_1$; it is orthogonal to $v$ because they belong to different eigenvalues of a Hermitian matrix. For $v_t = v + t\lVert v\rVert q$, the quotient is $(\mu + t^2 \lambda_1)/(1 + t^2) < \mu$ for every $t \ne 0$, so $v$ is not a local minimizer. Hence $\mu = \lambda_1$. $\square$

**Proof of 3.** $\max_i A_{ii} > 0$ because some weight is positive in a mesh with a triangle, so $\sigma > 0$. For $u \ne 0$, $u^*(A + \sigma M)u = u^* A u + \sigma u^* M u > 0$, so $A + \sigma M$ is Hermitian positive definite and has a Cholesky factor $L L^*$. In the coordinates $v$ of claim 2, line L7 computes $y = (A + \sigma M)^{-1} M u$, which is $M^{1/2} y = (B + \sigma I)^{-1} v$. So in these coordinates one step of lines L7 and L8 is $v \mapsto (B + \sigma I)^{-1} v$ followed by scaling to length 1. After $k$ steps,

$$v_k \propto \sum_j \frac{c_j}{(\lambda_j + \sigma)^k}\, q_j.$$

Let $P$ be the indices with $\lambda_j = \lambda_1$, and let $\lambda'$ be the smallest eigenvalue larger than $\lambda_1$ (if there is none, $v_0$ is already an eigenvector of $B$ after the first step). The ratio of the part outside $P$ to the part in $P$ is at most

$$\Big(\frac{\lambda_1 + \sigma}{\lambda' + \sigma}\Big)^k \frac{\big(\sum_{j \notin P} \lvert c_j\rvert^2\big)^{1/2}}{\big(\sum_{j \in P} \lvert c_j\rvert^2\big)^{1/2}},$$

because $\lambda_j + \sigma \ge \lambda' + \sigma$ for $j \notin P$ and the factors are positive. The denominator is nonzero by assumption, and the first factor is below 1 and tends to 0. So the distance from $v_k$ to the eigenspace of $\lambda_1$ tends to 0. The Rayleigh quotient and the residual $\lVert (B - R) v_k \rVert$ are continuous in $v_k$, and they are $\lambda_1$ and 0 on the unit vectors of that eigenspace, so they tend to $\lambda_1$ and to 0. $\square$

**Proof of 4.** The loop of lines L7 to L10 runs at most a fixed number of times (the code allows `max_steps`, and fails after that), so the algorithm terminates. When it returns at line L11, line L8 has set $u^* M u = 1$, and line L9 has set $\lambda = u^* A u = R(u) \ge \lambda_1$ by claim 2. The residual of line L10 is $\rho = \big(\sum_i \lvert (Au - \lambda M u)_i\rvert^2 / m_i\big)^{1/2} = \lVert M^{-1/2}(Au - \lambda Mu)\rVert = \lVert (B - \lambda I) v\rVert$, with $\lVert v\rVert = 1$. In the basis of claim 2,

$$\rho^2 = \sum_k (\lambda_k - \lambda)^2 \lvert c_k\rvert^2 \ge \min_k (\lambda_k - \lambda)^2 \sum_k \lvert c_k\rvert^2 = \min_k (\lambda_k - \lambda)^2.$$

So some eigenvalue lies within $\rho \le \delta\max(1, \lambda)$ of $\lambda$. Claim 4 does not say that this eigenvalue is $\lambda_1$; that follows from claim 3 when the iteration has converged, and the tests compare $\lambda$ with $\lambda_1$ from a dense eigenvalue computation. $\square$

**Proof of 5.** Let $f$ have the corners $p_0, p_1, p_2$ in counterclockwise order, and let $\alpha_c$ be the angle at $p_c$. At the corner $p_c$ the face lies between the edges to $p_{c+1}$ and to $p_{c+2} = p_{c-1}$ (indices mod 3), in this counterclockwise order around $p_c$, so line L1 gives $\varphi_{p_c}(p_{c-1}) \equiv \varphi_{p_c}(p_{c+1}) + s_{p_c}\alpha_c \pmod{2\pi}$. Then, summing the exponents of the three transports $r_{p_c p_{c+1}}$ and grouping the terms by vertex,

$$\sum_c \big(\varphi_{p_{c+1}}(p_c) + \pi - \varphi_{p_c}(p_{c+1})\big) = 3\pi + \sum_c \big(\varphi_{p_c}(p_{c-1}) - \varphi_{p_c}(p_{c+1})\big) \equiv 3\pi + \sum_c s_{p_c}\alpha_c = 4\pi + K_f \equiv K_f \pmod{2\pi}.$$

Multiplying by $n$, $\prod_c r_{p_c p_{c+1}} = e^{inK_f}$. Each turn satisfies $e^{i\tau_c} = u_{p_{c+1}} / (r_{p_c p_{c+1}} u_{p_c})$, and the product of the three quotients telescopes:

$$e^{i\sum_c \tau_c} = \frac{1}{\prod_c r_{p_c p_{c+1}}} = e^{-inK_f}.$$

So $nK_f + \sum_c \tau_c$ is a multiple of $2\pi$, and $I(f) = (nK_f + \sum_c\tau_c)/(2\pi n)$ is a multiple of $1/n$.

Now let the mesh be closed, with $V$ vertices, $E$ edges and $F$ faces. Every vertex is inner, so the scaled angles at each vertex add up to $2\pi$, and

$$\sum_f K_f = \sum_v 2\pi - \pi F = 2\pi V - \pi F = 2\pi (V - E + F) = 2\pi\chi,$$

because each face has three edges and each edge two faces, so $3F = 2E$ and $\pi F = 2\pi(E - F)$. For the turns, each edge $pq$ is crossed once as $p \to q$ in one face and once as $q \to p$ in the other. From the definition, $r_{pq} r_{qp} = e^{in \cdot 2\pi} = 1$. So

$$\frac{u_p}{r_{qp} u_q} = \frac{r_{pq} u_p}{u_q} = \Big(\frac{u_q}{r_{pq} u_p}\Big)^{-1},$$

and the two turns are $\tau$ and $-\tau$, since the argument in $(-\pi, \pi]$ of $1/z$ is minus that of $z$ when $\arg z \ne \pi$. So all turns add up to 0, and $\sum_f I(f) = n \cdot 2\pi\chi / (2\pi n) = \chi$. $\square$

Claims 1 to 5 together give the statement of the page: the eigenvector is the exact optimum of the relaxed problem, inverse iteration reaches it from almost every start, the returned pair is certified by its residual, and the singularities it shows obey the index sum $\chi$. $\blacksquare$
