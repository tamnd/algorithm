---
title: The two systems of the heat method have unique solutions, the divergence of line L5 is the weak divergence, and the Poisson step returns the piecewise linear function whose gradient is closest to the unit field
proves: [correctness, termination]
status: full
---

**Setup.** The mesh is connected, every face has positive area, and the faces are oriented. $\varphi_i$ is the hat function of vertex $i$, linear on each face, 1 at $i$ and 0 at the other vertices. A function $u$ on the vertices has the piecewise linear interpolant $\sum_i u_i\varphi_i$. $C_{ij} = \int \nabla\varphi_i \cdot \nabla\varphi_j\,dA$ is the cotangent stiffness matrix, as on the [cotangent Laplacian](/cotangent-laplacian/) page, and $M$ is the diagonal lumped mass with positive entries. The algorithm does one pass over the faces and two linear solves, so it stops once the solves stop, which Lemma 1 shows. What it computes is an approximation; the claims below are about the exact parts.

**Lemma 1 (unique solutions).** $M + tC$ is symmetric positive definite for $t > 0$. For any vertex $s$, the matrix $C'$ obtained from $C$ by deleting row and column $s$ is symmetric positive definite. So lines L3 and L6 have unique solutions, and conjugate gradients reach them in finitely many steps in exact arithmetic.

*Proof.* $u^\top C u = \int |\nabla u|^2\,dA \ge 0$, so $C$ is positive semidefinite, and $u^\top(M + tC)u \ge u^\top M u > 0$ for $u \ne 0$. For $C'$, let $y \ne 0$ and let $z$ be $y$ with $z_s = 0$ inserted. Then $y^\top C' y = z^\top C z = \int |\nabla z|^2\,dA$. If this is 0, then $\nabla z = 0$ on every face, so $z$ is constant on the connected mesh, and $z_s = 0$ gives $z = 0$, a contradiction. $\square$

**Lemma 2 (gradient of a hat function).** On a face $f$ with area $A_f$, unit normal $N$, and $e_i$ the edge opposite $i$ in the order of the face, $\nabla\varphi_i = \frac{1}{2A_f}N \times e_i$. So the formula of line L4 is the gradient of the interpolant.

*Proof.* $N \times e_i$ lies in the plane of $f$, is perpendicular to $e_i$, has length $|e_i|$, and points from $e_i$ toward $i$ because the face is oriented by $N$. $\varphi_i$ is 0 on the line of $e_i$ and 1 at $i$, at the height $2A_f/|e_i|$ above it. So its gradient is perpendicular to $e_i$, points toward $i$, and has length $|e_i|/(2A_f)$. $\square$

**Lemma 3 (the divergence is the weak divergence).** For any face vectors $X_f$ in the planes of the faces, the value of line L5 is $b_i = -\sum_{f \ni i} A_f\,\nabla\varphi_i|_f \cdot X_f = -\int X \cdot \nabla\varphi_i\,dA$.

*Proof.* Fix a face with vertices $i, j, l$ in order, and let $e_1 = p_j - p_i$, $e_2 = p_l - p_i$, $a = |e_1|$, $b = |e_2|$, $c = e_1 \cdot e_2$. The angle at $l$ is opposite $e_1$ and the angle at $j$ is opposite $e_2$, and
$\cot\theta_l = \frac{(-e_2)\cdot(e_1 - e_2)}{2A_f} = \frac{b^2 - c}{2A_f}$, $\cot\theta_j = \frac{(-e_1)\cdot(e_2 - e_1)}{2A_f} = \frac{a^2 - c}{2A_f}$.
Let $V = \cot\theta_l\, e_1 + \cot\theta_j\, e_2$ and $W = -N \times (p_l - p_j) = -N \times e_i$. Both lie in the plane of the face, which $e_1$ and $e_2$ span, so it is enough to compare their dot products with $e_1$ and $e_2$. First, $V \cdot e_1 = \frac{(b^2 - c)a^2 + (a^2 - c)c}{2A_f} = \frac{a^2b^2 - c^2}{2A_f} = \frac{(2A_f)^2}{2A_f} = 2A_f$, and by symmetry $V \cdot e_2 = 2A_f$. Second, with $p_l - p_j = e_2 - e_1$, $W \cdot e_1 = (N \times e_1)\cdot e_1 - (N \times e_2)\cdot e_1 = N \cdot (e_1 \times e_2) = 2A_f$, and in the same way $W \cdot e_2 = (N \times e_1) \cdot e_2 = N \cdot (e_1 \times e_2) = 2A_f$. So $V = W$, and the term of this face in line L5 is $\frac{1}{2}V \cdot X_f = -\frac{1}{2}(N \times e_i)\cdot X_f = -A_f\,\nabla\varphi_i \cdot X_f$ by Lemma 2. $\square$

**Lemma 4 (the pinned system solves the full system).** The solution $\varphi$ of line L6 satisfies $C\varphi = -b$ in every row, including row $s$.

*Proof.* By Lemma 3, $\sum_i b_i = -\int X \cdot \nabla(\sum_i \varphi_i)\,dA = 0$, because $\sum_i \varphi_i = 1$. The rows of $C$ also sum to the zero vector, since $C\mathbf{1} = 0$ and $C$ is symmetric. So row $s$ of $C\varphi + b$ is minus the sum of the other rows, which are 0. $\square$

**Theorem 1 (the Poisson step inverts the gradient).** If $X_f = \nabla\psi|_f$ for a piecewise linear $\psi$, then lines L5 to L7 return $\psi - \min_{s \in S}\psi_s$.

*Proof.* By Lemma 3, $b_i = -\sum_f A_f\,\nabla\varphi_i \cdot \nabla\psi = -\sum_j C_{ij}\psi_j$, so $b = -C\psi$. The vector $\psi - \psi_s\mathbf{1}$ is 0 at $s$ and satisfies $C(\psi - \psi_s\mathbf{1}) = C\psi = -b$, so by Lemma 1 it is the solution of line L6. Line L7 subtracts the smallest value at a source. $\square$

**Theorem 2 (least squares).** For any face vectors $X$, the result of line L6 minimizes $Q(\varphi) = \int |\nabla\varphi - X|^2\,dA$ over all piecewise linear $\varphi$ with $\varphi_s = 0$, and so, up to a constant, over all piecewise linear $\varphi$.

*Proof.* $Q(\varphi) = \varphi^\top C\varphi - 2\int X \cdot \nabla\varphi\,dA + \int |X|^2 = \varphi^\top C\varphi + 2b^\top\varphi + \text{const}$ by Lemma 3. This is a convex quadratic, and its gradient is $2(C\varphi + b)$, which is 0 exactly at the solution of $C\varphi = -b$. $\square$

So the computed $\varphi$ is the exact distance whenever the unit field $X$ is the gradient of a piecewise linear function, and in general it is the best fit to $X$. The error of the method is the error of $X$ as a gradient of the distance.

**What is not proved here.** That $X$ is close to the gradient of the true distance rests on Varadhan's formula $-4t\log k_t(x, y) \to d(x, y)^2$ for smooth surfaces, and on the analysis of Crane, Weischedel and Wardetzky for meshes. The errors on the flat grid and on the icosphere are measured.
