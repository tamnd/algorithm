---
title: The eigenvalues of the Jacobi matrix are the Gauss nodes, and the squared first eigenvector components times the integral of w are the Gauss weights
proves: [correctness]
status: full
---

We use the notation of the page: $\pi_k$ are the monic orthogonal polynomials of the weight $w$, with $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$, $\beta_0 = \int w$; $p_k = \pi_k/\sqrt{\beta_0 \cdots \beta_k}$ are the orthonormal ones; $J_n$ is the symmetric tridiagonal matrix with diagonal $\alpha_0, \ldots, \alpha_{n-1}$ and off-diagonal $\sqrt{\beta_1}, \ldots, \sqrt{\beta_{n-1}}$; and $x_1 < \cdots < x_n$, $\lambda_1, \ldots, \lambda_n$ are the nodes and weights of the $n$-point Gauss rule for $w$.

## Claim 1: the eigenpairs of $J_n$

For each node $x_j$, the vector $\mathbf{p}(x_j) = (p_0(x_j), \ldots, p_{n-1}(x_j))^T$ satisfies $J_n \mathbf{p}(x_j) = x_j \mathbf{p}(x_j)$.

*Proof.* The orthonormal recurrence reads $x\,p_k = \sqrt{\beta_k}\,p_{k-1} + \alpha_k\, p_k + \sqrt{\beta_{k+1}}\,p_{k+1}$ for $k \ge 0$, with $p_{-1} = 0$. For $k = 0, \ldots, n-1$ these $n$ equations say $x\,\mathbf{p}(x) = J_n \mathbf{p}(x) + \sqrt{\beta_n}\,p_n(x)\,\mathbf{e}_n$. At a zero of $p_n$ the last term vanishes. The vector is nonzero because $p_0 = 1/\sqrt{\beta_0} \ne 0$. $\square$

The $n$ nodes are distinct, so these are all $n$ eigenpairs, and each eigenvalue is simple.

## Claim 2: the weights

Let $\mathbf{v}_j$ be a unit eigenvector of $J_n$ for $x_j$, and $v_{1j}$ its first component. Then $\lambda_j = \beta_0\, v_{1j}^2$.

*Proof.* The eigenvalue is simple, so $\mathbf{v}_j = \pm \mathbf{p}(x_j)/\|\mathbf{p}(x_j)\|$, and

$$v_{1j}^2 = \frac{p_0(x_j)^2}{\sum_{k<n} p_k(x_j)^2} = \frac{1}{\beta_0} \cdot \frac{1}{\sum_{k<n} p_k(x_j)^2}.$$

The Gauss rule integrates $p_k p_m$ exactly for $k, m < n$, so with $P_{kj} = p_k(x_j)$ and $\Lambda = \operatorname{diag}(\lambda_j)$ we have $P \Lambda P^T = I$, hence $P^T P = \Lambda^{-1}$, whose diagonal is $\sum_{k<n} p_k(x_j)^2 = 1/\lambda_j$. Substituting gives $v_{1j}^2 = \lambda_j/\beta_0$. $\square$

## Claim 3: the QL iteration delivers the eigenvalues and the first components

Each sweep of lines L7 to L9 applies plane rotations $G$ to the active block, $J \leftarrow G^T J G$, so after all sweeps $D = Z^T J_n Z$ for the orthogonal matrix $Z$ that is the product of all rotations. The loop of line L3 ends only when every off-diagonal entry is $0$ or has passed the test of line L5, that is $|e_m| \le u(|d_m| + |d_{m+1}|)$. Setting those entries to zero is a symmetric perturbation of norm at most $2u\|J_n\|$, so the computed $d_j$ are the exact eigenvalues of a matrix $J_n + \Delta$ with $\|\Delta\| = O(u\|J_n\|)$ (the rotations themselves are backward stable). By Weyl's inequality each $d_j$ is within $O(u\|J_n\|)$ of an eigenvalue of $J_n$. The columns of $Z$ are the eigenvectors of $J_n + \Delta$, and line L9 applies each rotation to the first row only, so the vector $z$ is $\mathbf{e}_1^T Z$, the first components of these eigenvectors. Line L10 forms $\beta_0 z_j^2$, which by Claim 2 is the Gauss weight up to the eigenvector perturbation. Line L11 sorts the pairs.

*Termination.* The implicit QL iteration with the shift of line L7 (the eigenvalue of the leading $2 \times 2$ block nearer $d_l$) converges for every symmetric tridiagonal matrix, and the convergence of the shifted iteration is ultimately cubic (Wilkinson). The implementation still caps the sweeps per eigenvalue at 60 and raises an error if the cap is reached, so it always stops. In exact arithmetic with exact deflation, the computed $d_j$ and $\beta_0 z_j^2$ are exactly the nodes and weights. $\blacksquare$
