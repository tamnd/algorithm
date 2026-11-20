---
title: Zonal least squares returns the minimum norm phase, and the null space is piston (and waffle for Fried)
proves: [correctness]
status: full
---

**Setting.** The phase $\varphi$ is a real vector indexed by the points $(i, j)$ of an $n \times n$ grid, $n \ge 2$. The data $s$ are real, and $G$ is the difference matrix of the Hudgin or the Fried geometry, as defined on the page. The algorithm is lines L1 to L10: conjugate gradients (CG) on $G^TG\varphi = G^Ts$ from $\varphi_0 = 0$, then the removal of the null space component.

**Claim 1 (normal equations).** $\varphi$ minimizes $f(\varphi) = \lVert G\varphi - s\rVert^2$ if and only if $G^TG\varphi = G^Ts$.

*Proof.* $f$ is a convex quadratic with gradient $2G^T(G\varphi - s)$. A convex differentiable function has its minimum exactly where the gradient is zero. $\square$

**Claim 2 (Hudgin normal matrix).** For the Hudgin geometry, $(G^TG\varphi)_{i,j} = \sum_{(k,l) \sim (i,j)} (\varphi_{i,j} - \varphi_{k,l})$, the sum over the grid neighbors of $(i,j)$. So $G^TG$ is the graph Laplacian of the grid, which is the 5-point Laplacian with Neumann boundary.

*Proof.* $\varphi^TG^TG\varphi = \lVert G\varphi\rVert^2 = \sum_{\text{edges } \{p,q\}} (\varphi_p - \varphi_q)^2$, since each row of $G$ is one edge difference. The quadratic form $\sum_{\text{edges}}(\varphi_p - \varphi_q)^2$ is the form of the graph Laplacian $D - W$, with $D$ the diagonal of degrees and $W$ the adjacency matrix. Two symmetric matrices with the same quadratic form are equal. $\square$

**Claim 3 (Hudgin null space).** For Hudgin, $G\varphi = 0$ if and only if $\varphi$ is constant.

*Proof.* If $G\varphi = 0$, then $\varphi_p = \varphi_q$ for every edge. The grid graph is connected, so $\varphi$ takes one value on all points. Conversely a constant gives zero differences. $\square$

The Southwell geometry uses the Hudgin matrix with other data, so it has the same null space.

**Claim 4 (Fried null space).** For Fried with $n \ge 2$, $G\varphi = 0$ if and only if $\varphi = a\,\mathbf 1 + b\,w$ with $w_{i,j} = (-1)^{i+j}$.

*Proof.* Take one square with the corners $\varphi_{i,j} = A$, $\varphi_{i,j+1} = B$, $\varphi_{i+1,j} = C$ and $\varphi_{i+1,j+1} = D$. Its two measurements are zero when $B + D - A - C = 0$ and $C + D - A - B = 0$. The sum gives $2D - 2A = 0$ and the difference gives $2B - 2C = 0$. So in every square the two diagonal corners are equal: $\varphi_{i,j} = \varphi_{i+1,j+1}$ and $\varphi_{i,j+1} = \varphi_{i+1,j}$. These are steps $(\pm1, \pm1)$ on the grid, and they keep the parity of $i + j$. Any two points of the same parity are joined by a path of such steps inside the grid (move diagonally, and zigzag where a border is reached; $n \ge 2$). So $\varphi$ is constant, say $p$, on the points with $i + j$ even, and constant, say $q$, on the points with $i + j$ odd. This is $a\mathbf 1 + bw$ with $a = (p + q)/2$ and $b = (p - q)/2$. Conversely, the computation on the page shows that $w$ gives zero for every square, and so does $\mathbf 1$. $\square$

The vectors $\mathbf 1$ and $w$ are orthogonal for even $n$. For odd $n$ the sum of $w$ is $1$, so the code uses $w - \mathbf 1/n^2$, which spans the same plane with $\mathbf 1$ and is orthogonal to it.

**Claim 5 (CG returns the minimum norm solution).** Let $M = G^TG$ and $b = G^Ts$. In exact arithmetic CG from $0$ stops after at most $t$ steps, where $t$ is the number of distinct nonzero eigenvalues of $M$, with $\varphi_t = G^\dagger s$.

*Proof.* The null space of $M$ equals the null space of $G$, since $M\varphi = 0$ gives $\lVert G\varphi\rVert^2 = \varphi^T M\varphi = 0$. The vector $b = G^Ts$ is in the range of $G^T$, which is the orthogonal complement of the null space of $G$. Let $V$ be this range; $M$ maps $V$ into $V$ and is positive definite on $V$. Every CG quantity ($r$, $p$, $q$, $\varphi$) is a linear combination of $b, Mb, M^2b, \dots$, so all of them stay in $V$. On $V$, CG is the standard method for a symmetric positive definite matrix, and the standard theory applies: $\varphi_k$ minimizes the $M$-norm of the error over the Krylov space $\mathrm{span}\{b, \dots, M^{k-1}b\}$, and the Krylov space stops growing after at most $t$ steps, when it contains the solution. So CG reaches the unique solution $\varphi^\ast \in V$ of $M\varphi = b$, and the residual becomes $0$. By Claim 1, $\varphi^\ast$ is a least squares solution. Every least squares solution is $\varphi^\ast + z$ with $z$ in the null space, and $\lVert\varphi^\ast + z\rVert^2 = \lVert\varphi^\ast\rVert^2 + \lVert z\rVert^2$ because $\varphi^\ast \perp z$. So $\varphi^\ast$ is the one of minimum norm, which is $G^\dagger s$. Line L9 subtracts the projection on the null space, which is zero in exact arithmetic. $\square$

**Claim 6 (exact data).** If $s = G\varphi^\ast$, the output is $\varphi^\ast - P\varphi^\ast$, with $P$ the orthogonal projection on the null space of $G$.

*Proof.* $\varphi^\ast - P\varphi^\ast$ is in $V$ and has $G(\varphi^\ast - P\varphi^\ast) = s$, so it is a least squares solution with zero residual, in $V$. By Claim 5 it is the output. $\square$

**Claim 7 (Southwell is exact for quadratic phases).** Let $\varphi(x, y)$ be a polynomial of degree at most 2, sampled at the grid points with spacing $h$, and let $s^x = \partial\varphi/\partial x$ and $s^y = \partial\varphi/\partial y$ at the points. Then the Southwell data are the exact Hudgin differences of the samples, and the output is the samples minus their mean.

*Proof.* Along one grid row, $\varphi(x + h, y) - \varphi(x, y) = \int_x^{x+h} \partial_x\varphi(t, y)\, dt$. The integrand is linear in $t$, and the trapezoid rule $\tfrac h2(\partial_x\varphi(x, y) + \partial_x\varphi(x + h, y))$ is exact for linear functions. The same holds along columns. So the data are $G\varphi^\ast$ for the Hudgin $G$, and Claim 6 gives the result. $\square$

**Claim 8 (noise).** If $s = G\varphi^\ast + e$ with $e$ white of variance $\sigma^2$, the error $G^\dagger e$ of the Hudgin output (on the part outside the null space) has the total variance $\sigma^2 \operatorname{trace}((G^TG)^\dagger) = \sigma^2 \sum_{\lambda \ne 0} 1/\lambda$, the sum over the nonzero eigenvalues of the Neumann Laplacian, $\lambda_{p,q} = 4\sin^2(\pi p/(2n)) + 4\sin^2(\pi q/(2n))$ for $0 \le p, q < n$.

*Proof.* The covariance of $G^\dagger e$ is $\sigma^2 G^\dagger (G^\dagger)^T = \sigma^2 (G^TG)^\dagger$, a standard identity of the pseudoinverse. Its trace is the sum of the inverse nonzero eigenvalues. The 1D Neumann path Laplacian has the eigenvectors $\cos(\pi p(j + 1/2)/n)$ with eigenvalues $4\sin^2(\pi p/(2n))$, and the grid Laplacian is the Kronecker sum of two of them, so its eigenvalues are the sums. $\square$

The tests check Claims 2, 3 and 4 (by the eigenvalues of the dense normal matrix), Claim 5 (against a dense solve of $(M + \sum_z zz^T/\lVert z\rVert^2)\varphi = b$, whose unique solution is $G^\dagger s$, and on the exact rational example of the page), Claim 6 for both geometries, Claim 7, and the adjoint pair $G$, $G^T$.
