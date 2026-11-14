---
title: Each implicit fairing step has a unique solution, it is the backward Euler step of M x' = -C x, it damps every mode for every time step, it obeys a maximum principle for nonnegative weights, and it keeps a planar mesh fixed
proves: [correctness, termination]
status: full
---

**Setup.** The mesh has vertices $1, \ldots, n$, every vertex lies on a face of positive area, and $F$ is the set of fixed vertices, $R$ the free ones. For one coordinate, $u \in \mathbb{R}^n$. Let $\phi_i$ be the hat function of vertex $i$: linear on each triangle, 1 at $i$ and 0 at the other vertices. The interpolant of $u$ is $\sum_i u_i \phi_i$, and its Dirichlet energy is $E(u) = \frac{1}{2}\sum_T \operatorname{area}(T)\,|\nabla u|_T|^2$. The loop of line L2 runs $K$ times, and each step does three solves, so the algorithm stops if each solve stops, which Lemma 2 shows.

**Lemma 1 (the stiffness matrix).** $E(u) = \frac{1}{2}u^\top C u$, where $C$ is the cotangent matrix of line L3. So $C$ is symmetric positive semidefinite, and $Cu = 0$ exactly when $u$ is constant on each connected part of the mesh.

*Proof.* On a triangle $T$ with vertices $a, b, c$ and angles $\alpha_a, \alpha_b, \alpha_c$, $\operatorname{area}(T)\,|\nabla u|^2 = \frac{1}{2}\big(\cot\alpha_c (u_a - u_b)^2 + \cot\alpha_a (u_b - u_c)^2 + \cot\alpha_b (u_c - u_a)^2\big)$. This is the cotangent formula of Pinkall and Polthier, proved on the [cotangent Laplacian](/cotangent-laplacian/) page. Summing over the triangles gives $E(u) = \frac{1}{2}\sum_{ij} w_{ij}(u_i - u_j)^2 = \frac{1}{2}u^\top C u$ with $w_{ij} = \frac{1}{2}(\cot\alpha_{ij} + \cot\beta_{ij})$. Since $E \ge 0$, $C$ is positive semidefinite. $E(u) = 0$ means $\nabla u = 0$ on every triangle of positive area, so $u$ is constant along every edge and on each connected part. $\square$

The tests check $C_{ii} = 2E(e_i)$ and $C_{ij} = E(e_i + e_j) - E(e_i) - E(e_j)$ with the energy computed from the Gram matrix of each triangle.

**Lemma 2 (the system is solvable).** $A = M_{RR} + \Delta t\, C_{RR}$ is symmetric positive definite for every $\Delta t > 0$. So line L5 has a unique solution, and conjugate gradients reach it in at most $|R|$ iterations in exact arithmetic.

*Proof.* $C_{RR}$ is a principal submatrix of a positive semidefinite matrix, so it is positive semidefinite. $M_{RR}$ is diagonal with positive entries. So $y^\top A y \ge y^\top M_{RR} y > 0$ for $y \ne 0$. Conjugate gradients on a symmetric positive definite matrix of size $m$ find the solution in at most $m$ steps (see [conjugate gradient method](/conjugate-gradient-method/)). $\square$

**Lemma 3 (backward Euler).** The new positions satisfy $M_{RR}\frac{x^{\text{new}}_R - x_R}{\Delta t} = -(C x^{\text{new}})_R$ with $x^{\text{new}}_F = x_F$, where $C$ and $M$ are taken at the old positions.

*Proof.* Line L5 solves $(M_{RR} + \Delta t C_{RR})y = M_{RR}x_R - \Delta t C_{RF}x_F$, and line L6 sets $x^{\text{new}}_R = y$. Move the terms: $M_{RR}(y - x_R) = -\Delta t(C_{RR}y + C_{RF}x_F) = -\Delta t (Cx^{\text{new}})_R$. $\square$

**Theorem 1 (unconditional stability).** Fix $C$ and $M$. Let $k_1 \le \cdots \le k_m$ be the eigenvalues of the generalized problem $C_{RR}v = k M_{RR}v$, all real and nonnegative. With $x_F = 0$, one step multiplies the coordinate of $x_R$ along $v_j$ by $\frac{1}{1 + \Delta t k_j} \in (0, 1]$, so $x_R^\top M_{RR} x_R$ does not increase, for every $\Delta t > 0$. The explicit step $x_R \leftarrow x_R - \Delta t M_{RR}^{-1}C_{RR}x_R$ multiplies the same coordinate by $1 - \Delta t k_j$, which is less than $-1$ when $\Delta t > 2/k_j$.

*Proof.* $M_{RR}^{-1/2}C_{RR}M_{RR}^{-1/2}$ is symmetric positive semidefinite, so the generalized eigenvectors $v_j$ can be chosen $M_{RR}$-orthonormal, with $k_j \ge 0$. With $x_F = 0$, the step is $(M_{RR} + \Delta t C_{RR})y = M_{RR}x_R$. For $x_R = v_j$, $y = v_j/(1 + \Delta t k_j)$ solves it, because $(M_{RR} + \Delta t C_{RR})v_j = (1 + \Delta t k_j)M_{RR}v_j$. By linearity, $x_R = \sum a_j v_j$ goes to $\sum \frac{a_j}{1 + \Delta t k_j} v_j$, and $x_R^\top M_{RR}x_R = \sum a_j^2$ does not increase. The explicit claim is the same computation for the forward step. $\square$

**Theorem 2 (maximum principle).** If $w_{ij} \ge 0$ for all edges, then each new free position is a convex combination of the old free positions and the fixed positions. If moreover $F = \emptyset$, then $\sum_i M_{ii}x^{\text{new}}_i = \sum_i M_{ii}x_i$, and with the uniform weights, $M = D$, this is $\sum_i d_i x_i$.

*Proof.* Let $B = M_{RR} + \Delta t C_{RR}$ and $W_{RF} = -C_{RF} \ge 0$. Then $B$ has positive diagonal and nonpositive off-diagonal entries, and row $i$ has $B_{ii} - \sum_{j \in R, j \ne i}|B_{ij}| = M_{ii} + \Delta t\sum_{j \in F}w_{ij} > 0$. So $B$ is strictly diagonally dominant with this sign pattern, a nonsingular M-matrix, and $B^{-1} \ge 0$ entrywise. The new positions are $x^{\text{new}}_R = B^{-1}M_{RR}x_R + B^{-1}\Delta t W_{RF}x_F$, with nonnegative coefficients. The rows of $C$ sum to 0, so $C_{RR}\mathbf{1} = W_{RF}\mathbf{1}$ and $B\mathbf{1} = M_{RR}\mathbf{1} + \Delta t W_{RF}\mathbf{1}$. So for all-ones input the output is $\mathbf{1}$, and the coefficients in each row sum to 1. For the second claim, $\mathbf{1}^\top C = 0$ because $C$ is symmetric with zero row sums, so $\mathbf{1}^\top(M + \Delta t C)x^{\text{new}} = \mathbf{1}^\top M x^{\text{new}}$ equals $\mathbf{1}^\top M x$. $\square$

**Theorem 3 (planar meshes are fixed).** Let the mesh lie in a plane, with every vertex of $R$ an inner vertex whose star is embedded in the plane, and let the weights be the cotangent weights. Then $x^{\text{new}} = x$ for every $\Delta t$.

*Proof.* Each coordinate $u$ of the positions is a linear function $u(p) = a \cdot p + b$ of the point, and its interpolant is that linear function. By Lemma 1, $(Cu)_i = \partial E/\partial u_i = \sum_T \operatorname{area}(T)\,\nabla u \cdot \nabla\phi_i = a \cdot \int_{\operatorname{star}(i)} \nabla\phi_i\,dA$. By the divergence theorem, this integral is $\oint \phi_i\, \nu\, ds$ over the border of the star, where $\phi_i = 0$. So $(Cu)_i = 0$ for every free $i$. Then $u_R$ itself solves $(M_{RR} + \Delta t C_{RR})y = M_{RR}u_R - \Delta t C_{RF}u_F$, since the difference is $\Delta t(Cu)_R = 0$. By Lemma 2 the solution is unique. $\square$

With the uniform weights the claim fails: $(Gu)_i = u_i - c_i$ is not 0 for an irregular star, and the tests see the vertices move in the plane.

**Example values.** On the regular octahedron with the uniform weights, $Gx = x$ for each coordinate, so the step is $x/(1 + \Delta t)$, which the tests check exactly. With the cotangent weights, every $w_{ij} = 1/\sqrt{3}$ and $M_{ii} = 2/\sqrt{3}$, so $(Cx)_i = \frac{4}{\sqrt{3}}x_i$ and the step is $x/(1 + 2\Delta t)$. After scaling by $s$, $M$ scales by $s^2$ and $C$ does not change, so the next step is $s^2/(s^2 + 2\Delta t)$.

**Lemma 4 (volume correction).** Line L7 makes the enclosed volume of a closed mesh equal to the starting volume $V_0$.

*Proof.* The signed volume $\frac{1}{6}\sum_{abc} x_a \cdot (x_b \times x_c)$ of a closed mesh does not change under translation and is homogeneous of degree 3. Scaling about the centroid by $s = (V_0/V)^{1/3}$ multiplies $V$ by $s^3 = V_0/V$. $\square$

**What is measured.** How close the icosphere is to the smooth flow, and how much radial noise one step removes, are measured in the tests, not proved.
