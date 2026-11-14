---
title: The manifold harmonic basis is M-orthonormal, its frequencies are real and not negative, and the transform is exactly invertible
proves: [correctness]
status: full
---

**Setup.** A triangle mesh has vertices $p_1, \ldots, p_n$. Every vertex is in at least one triangle, and every triangle has positive area. For a vector $u \in \mathbb{R}^n$ of values at the vertices, $u$ also names the piecewise linear function that has these values at the vertices and is linear on each triangle. Let $\varphi_a$ be the hat function of vertex $a$, so $u = \sum_a u_a \varphi_a$.

The stiffness matrix is $C$ with $C_{ab} = -\tfrac12(\cot\alpha_{ab} + \cot\beta_{ab})$ for an edge $ab$, where $\alpha_{ab}$ and $\beta_{ab}$ are the angles opposite the edge (one angle for a boundary edge), $C_{ab} = 0$ when $ab$ is not an edge, and $C_{aa} = -\sum_{b \ne a} C_{ab}$. The mass matrix $M$ is one of these:

- the lumped mass, a diagonal matrix whose entry $M_{aa}$ is a sum of positive parts of the triangles at $a$ (one third of each area, or the mixed Voronoi area);
- the consistent mass $M_{ab} = \int \varphi_a \varphi_b$.

The template solves $C\phi = \lambda M \phi$ and uses the transform $\tilde x = \Phi^{\mathsf T} M x$, where the columns of $\Phi$ are the eigenvectors $\phi_k$.

**Lemma 1 (the stiffness matrix is the Dirichlet energy).** $C$ is symmetric and $u^{\mathsf T} C u = \int |\nabla u|^2 \ge 0$ for every $u$.

*Proof.* Take a triangle $T$ with vertices $a, b, c$, area $A$ and unit normal $\nu$. The hat function $\varphi_a$ is $1$ at $a$ and $0$ on the edge $bc$, so on $T$ its gradient is perpendicular to $bc$, in the plane of $T$, with length $1/h_a$, where $h_a = 2A/|c - b|$ is the height from $a$. This is $\nabla\varphi_a = \nu \times (c - b)/(2A)$. In the same way $\nabla\varphi_b = \nu \times (a - c)/(2A)$. Both vectors $c - b$ and $a - c$ lie in the plane, so $(\nu \times v) \cdot (\nu \times w) = v \cdot w$ for them, and

$$\int_T \nabla\varphi_a \cdot \nabla\varphi_b = A\,\frac{(c - b)\cdot(a - c)}{4A^2} = -\frac{(b - c)\cdot(a - c)}{4A}.$$

With $\gamma$ the angle at $c$, $(b - c)\cdot(a - c) = |b - c||a - c|\cos\gamma$ and $2A = |b - c||a - c|\sin\gamma$, so the integral is $-\tfrac12\cot\gamma$. An edge $ab$ is in one or two triangles, and $\gamma$ is the angle opposite $ab$ in each, so $\int \nabla\varphi_a \cdot \nabla\varphi_b = C_{ab}$ for $a \ne b$. Since $\sum_b \varphi_b = 1$ on every triangle, $\sum_b \nabla\varphi_b = 0$, so $\int \nabla\varphi_a \cdot \nabla\varphi_a = -\sum_{b \ne a}\int \nabla\varphi_a \cdot \nabla\varphi_b = C_{aa}$. Thus $C_{ab} = \int \nabla\varphi_a \cdot \nabla\varphi_b$ for all $a, b$. This is symmetric in $a$ and $b$, and $u^{\mathsf T} C u = \int |\sum_a u_a \nabla\varphi_a|^2 = \int |\nabla u|^2$. $\square$

**Lemma 2 (the kernel of the stiffness matrix).** $Cu = 0$ exactly when $u$ is constant on each connected component of the mesh.

*Proof.* If $u$ is constant on each component, then $\nabla u = 0$ on every triangle, so $u^{\mathsf T}Cu = 0$; and if $u^{\mathsf T}Cu = 0$, then $Cu = 0$, because $C$ is symmetric positive semidefinite (Lemma 1): with $C = R^{\mathsf T}R$, $|Ru|^2 = 0$ gives $Ru = 0$ and $Cu = 0$. Conversely, $Cu = 0$ gives $\int|\nabla u|^2 = 0$. Each triangle has positive area and $\nabla u$ is constant on it, so $\nabla u = 0$ there, and $u$ takes the same value at the three vertices. Two triangles that share a vertex give the same value to it, so the value is the same on each connected component. $\square$

**Lemma 3 (the mass matrix is positive definite).** $M$ is symmetric and $u^{\mathsf T} M u > 0$ for $u \ne 0$.

*Proof.* The lumped mass is diagonal, and each vertex has a positive entry because it is in a triangle and each triangle gives it a positive part. Then $u^{\mathsf T}Mu = \sum_a M_{aa}u_a^2 > 0$ for $u \ne 0$. The consistent mass is symmetric by definition and $u^{\mathsf T}Mu = \int u^2 \ge 0$. If $\int u^2 = 0$, then $u = 0$ on every triangle, because $u$ is continuous and each triangle has positive area, so $u_a = 0$ at every vertex. $\square$

**Lemma 4 (eigenvectors of different eigenvalues are M-orthogonal).** If $C\phi = \lambda M\phi$ and $C\psi = \mu M\psi$ with $\lambda \ne \mu$, then $\psi^{\mathsf T} M \phi = 0$.

*Proof.* By the symmetry of $C$ and $M$, $\lambda\,\psi^{\mathsf T}M\phi = \psi^{\mathsf T}C\phi = \phi^{\mathsf T}C\psi = \mu\,\phi^{\mathsf T}M\psi = \mu\,\psi^{\mathsf T}M\phi$. So $(\lambda - \mu)\,\psi^{\mathsf T}M\phi = 0$, and $\psi^{\mathsf T}M\phi = 0$. $\square$

**Theorem 1 (the basis).** There are real numbers $\lambda_1 \le \cdots \le \lambda_n$ and a matrix $\Phi$ with columns $\phi_1, \ldots, \phi_n$ such that

$$C\Phi = M\Phi\Lambda, \qquad \Phi^{\mathsf T} M \Phi = I, \qquad \Lambda = \operatorname{diag}(\lambda_1, \ldots, \lambda_n).$$

Each $\lambda_k = \phi_k^{\mathsf T}C\phi_k \ge 0$. The number of zero eigenvalues is the number of connected components, and on a connected mesh $\lambda_1 = 0$ with $\phi_1 = \mathbf 1/\sqrt{\mathbf 1^{\mathsf T}M\mathbf 1}$, up to sign. Any set of eigenvectors that is M-orthonormal inside each eigenspace is M-orthonormal as a whole.

*Proof.* By Lemma 3, $M$ has a Cholesky factorization $M = LL^{\mathsf T}$ with $L$ invertible. Let $K = L^{-1}CL^{-\mathsf T}$. It is symmetric, because $C$ is. By the spectral theorem, $K = Y\Lambda Y^{\mathsf T}$ with $Y$ orthogonal and $\Lambda$ real diagonal; order the diagonal increasingly. Set $\Phi = L^{-\mathsf T}Y$. Then

$$C\Phi = L K L^{\mathsf T} L^{-\mathsf T} Y = L K Y = L Y \Lambda = L L^{\mathsf T} L^{-\mathsf T} Y \Lambda = M\Phi\Lambda,$$

$$\Phi^{\mathsf T}M\Phi = Y^{\mathsf T}L^{-1}LL^{\mathsf T}L^{-\mathsf T}Y = Y^{\mathsf T}Y = I.$$

Column $k$ of the first identity is $C\phi_k = \lambda_k M\phi_k$. Multiply by $\phi_k^{\mathsf T}$ and use $\phi_k^{\mathsf T}M\phi_k = 1$: $\lambda_k = \phi_k^{\mathsf T}C\phi_k \ge 0$ by Lemma 1.

The eigenvectors of $\lambda = 0$ satisfy $C\phi = 0$, so by Lemma 2 they are the functions that are constant on each component. This space has dimension equal to the number of components $c$, and the columns of $\Phi$ for $\lambda = 0$ are linearly independent (they are M-orthonormal) and lie in it. A vector $u$ in this space with $u^{\mathsf T}M\phi_k = 0$ for all $k$ with $\lambda_k = 0$ is M-orthogonal to all columns of $\Phi$ (Lemma 4 for the others), and since $\Phi$ is invertible ($\Phi^{\mathsf T}M\Phi = I$), $u = \Phi\Phi^{\mathsf T}Mu = 0$. So the columns for $\lambda = 0$ span the space, and there are exactly $c$ of them. On a connected mesh the space is spanned by $\mathbf 1$, and its M-unit vectors are $\pm\mathbf 1/\sqrt{\mathbf 1^{\mathsf T}M\mathbf 1}$.

For the last claim, take eigenvectors $\phi_k$ that are M-orthonormal inside each eigenspace. Two of them from different eigenspaces are M-orthogonal by Lemma 4. So all pairs are M-orthogonal and each has M-norm $1$. $\square$

**Remark (repeated eigenvalues).** A linear combination of eigenvectors of one eigenvalue $\lambda$ is again an eigenvector of $\lambda$. So the Gram-Schmidt process in the inner product $\langle u, v\rangle_M = u^{\mathsf T}Mv$, applied inside each eigenspace, turns any basis of eigenvectors into an M-orthonormal one, and the last claim of Theorem 1 then gives the whole basis.

**Theorem 2 (transform, inverse and Parseval).** Let $\Phi$ be as in Theorem 1, $x \in \mathbb R^n$ a signal, and $\tilde x = \Phi^{\mathsf T}Mx$, so $\tilde x_k = \phi_k^{\mathsf T}Mx$. Then

1. $x = \Phi\tilde x = \sum_k \tilde x_k\phi_k$;
2. $x^{\mathsf T}Mx = \sum_k \tilde x_k^2$ and $x^{\mathsf T}Cx = \sum_k \lambda_k\tilde x_k^2$;
3. for every $m$, the vector $x_m = \sum_{k \le m}\tilde x_k\phi_k$ is the unique closest vector to $x$ in the M-norm among the combinations of $\phi_1, \ldots, \phi_m$, and $(x - x_m)^{\mathsf T}M(x - x_m) = \sum_{k > m}\tilde x_k^2$;
4. for every function $h$, the filtered signal $y = \sum_k h(\lambda_k)\tilde x_k\phi_k$ has the coefficients $\tilde y_k = h(\lambda_k)\tilde x_k$.

*Proof.* From $\Phi^{\mathsf T}M\Phi = I$, the square matrix $\Phi$ is invertible with $\Phi^{-1} = \Phi^{\mathsf T}M$, so $\Phi\Phi^{\mathsf T}M = I$ too. Then $\Phi\tilde x = \Phi\Phi^{\mathsf T}Mx = x$, which is item 1. For item 2, $x^{\mathsf T}Mx = \tilde x^{\mathsf T}\Phi^{\mathsf T}M\Phi\tilde x = \tilde x^{\mathsf T}\tilde x$, and $x^{\mathsf T}Cx = \tilde x^{\mathsf T}\Phi^{\mathsf T}C\Phi\tilde x = \tilde x^{\mathsf T}\Phi^{\mathsf T}M\Phi\Lambda\tilde x = \tilde x^{\mathsf T}\Lambda\tilde x$. For item 3, a combination $z = \sum_{k \le m}c_k\phi_k$ has the coefficients $\tilde z_k = c_k$ for $k \le m$ and $0$ for $k > m$ (because $\Phi^{\mathsf T}M\Phi = I$), so by item 2 applied to $x - z$,

$$(x - z)^{\mathsf T}M(x - z) = \sum_{k \le m}(\tilde x_k - c_k)^2 + \sum_{k > m}\tilde x_k^2.$$

This is smallest exactly when $c_k = \tilde x_k$ for all $k \le m$, which is $z = x_m$, and then it is $\sum_{k > m}\tilde x_k^2$. Item 4 is $\tilde y = \Phi^{\mathsf T}M\Phi\,\operatorname{diag}(h(\lambda_k))\,\tilde x = \operatorname{diag}(h(\lambda_k))\,\tilde x$. $\square$

**What is not proved here.** The proofs are in exact arithmetic. An eigensolver in floating point returns vectors that are M-orthonormal only up to rounding, and the size of that error depends on the solver and on the gaps between the eigenvalues. How well the discrete eigenvalues approximate the eigenvalues of the smooth surface depends on the mesh and is a result of finite element theory, not of this proof.
