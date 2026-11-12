---
title: The Galerkin system of Poisson reconstruction has a unique solution, and its level set is a closed oriented 2-manifold
proves: [correctness]
status: full
---

We use the names of the pseudocode. Let $W$ be the span of the hat functions $\varphi_o$ of the interior nodes, that is, the continuous functions that are trilinear on each cell of the grid and zero on the border of the grid. For $\chi \in W$ let $\Phi(\chi) = \int \lVert \nabla \chi - V \rVert^2$, the integral over the box.

**Claim.** (1) $\Phi$ has a unique minimizer on $W$, and its coefficient vector $x$ is the unique solution of $L x = b$, with $L$ symmetric positive definite. (2) Conjugate gradients, started at $x = 0$, give this solution after at most $N$ steps in exact arithmetic, where $N$ is the number of interior nodes. (3) If $\gamma > 0$, the mesh of line L6 is a closed, oriented 2-manifold, and it is the level set $\{\ell = \gamma\}$ of the function $\ell$ that is linear on each tetrahedron of the Kuhn subdivision of the grid and equals $\chi$ at the nodes.

**Step 1: the energy.** For $\chi = \sum_o x_o \varphi_o$,
$$\Phi(\chi) = x^{\mathsf T} L x - 2 b^{\mathsf T} x + \int \lVert V \rVert^2, \qquad L_{o o'} = \int \nabla \varphi_o \cdot \nabla \varphi_{o'},\quad b_o = \int V \cdot \nabla \varphi_o,$$
by expanding the square. $L$ is symmetric. For $x \ne 0$, $x^{\mathsf T} L x = \int \lVert \nabla \chi \rVert^2$. If this were 0, $\chi$ would be constant on the box, because it is continuous and piecewise smooth with zero gradient, and it is zero on the border, so $\chi = 0$ and $x = 0$, a contradiction. So $L$ is positive definite, $\Phi$ is a strictly convex quadratic in $x$, and its unique minimizer is where its gradient $2 (L x - b)$ is zero. This proves (1). The stencils of line L4 are the values of these integrals: each $\varphi_o$ is a product of 1D hat functions, so each integral is a sum of products of 1D integrals, and on spacing $h$ these are $\int \varphi_i \varphi_j = h \cdot \tfrac23$ or $h \cdot \tfrac16$, $\int \varphi_i' \varphi_j' = \tfrac2h$ or $-\tfrac1h$, and $\int \varphi_i \varphi_j' = 0$ or $\pm\tfrac12$, for $j = i$ or $|j - i| = 1$, and 0 otherwise.

**Step 2: the solver.** For a symmetric positive definite matrix, conjugate gradients from $x = 0$ produce search directions that are $L$-orthogonal, and after $k$ steps the iterate minimizes $x^{\mathsf T} L x - 2 b^{\mathsf T} x$ over the Krylov space $\operatorname{span}\{b, L b, \ldots, L^{k-1} b\}$. This space has dimension at most $N$, so after at most $N$ steps it contains the solution, which is then reached. In floating point the method is stopped when the residual is small relative to $\lVert b \rVert$. This proves (2).

**Step 3: the level set.** Line L6 runs marching tetrahedra on the values $-x_o$ with the iso value $-\gamma$, so a node is inside when $-x_o < -\gamma$, that is, when $x_o > \gamma$. The border values are 0, and $0 > \gamma$ is false when $\gamma > 0$, so every border node is outside. By the correctness of [marching tetrahedra](/marching-tetrahedra/), when no node value equals the iso value, the mesh is then a closed, oriented 2-manifold, and it is the level set of the piecewise linear interpolant of the node values on the Kuhn tetrahedra; negating the values and the iso value does not change this set. The triangles are oriented toward the outside of the field $-\chi$, which is where $\chi \le \gamma$, the outside of the solid. This proves (3). The interpolant $\ell$ is not $\chi$ itself: $\chi$ is trilinear on each cell, and $\ell$ agrees with it at the nodes.

**Termination.** Lines L2, L3, L5 and L6 are loops over the samples and the grid, and line L4 stops after at most $N$ steps, or at the tolerance. $\blacksquare$
