---
title: LSCM minimizes twice the Dirichlet energy minus the area, and two pins make the minimizer unique unless a development maps them to one point
proves: [correctness, termination]
status: full
---

**Setting.** $M$ is a triangle mesh whose dual graph (triangles, adjacent when they share an edge) is connected, and every triangle has positive area. Each triangle $T$ has a frame: corner positions $q_0, q_1, q_2 \in \mathbb{C}$ that form a counterclockwise triangle congruent to $T$, with area $A_T > 0$. Write $\varepsilon_j = q_{j+2} - q_{j+1}$ (indices mod 3). A map assigns $U_v \in \mathbb{C}$ to each vertex, and $f_T$ is the affine map of the frame of $T$ with $f_T(q_j) = U_{v_j}$. The energy is

$$E(U) = \sum_T \frac{|s_T|^2}{4 A_T}, \qquad s_T = \sum_{j=0}^{2} \varepsilon_j U_{v_j}.$$

Two distinct vertices $p$ and $q$ are pinned to given values. LSCM returns the solution of the normal equations of $E$ in the free values.

**Claim.**

1. $E(U) = \sum_T A_T \big((u_x - v_y)^2 + (u_y + v_x)^2\big) = 2 E_D(U) - 2\,\mathcal{A}(U)$, where $U = u + iv$, $E_D = \frac12 \sum_T A_T (|\nabla u|^2 + |\nabla v|^2)$ and $\mathcal{A}(U)$ is the signed area of the image.
2. $s_T = 0$ if and only if $f_T(z) = a z + b$ for complex $a, b$, that is, $f_T$ is a similarity that keeps the orientation, or a constant.
3. The minimizer with the two pins is unique if and only if there is no development of $M$ that maps $p$ and $q$ to the same point. A *development* is a map that is, on every triangle, a rotation and translation of its frame.
4. If $M$ is planar, with its own coordinates as frames, and $p$ and $q$ have different positions, the minimizer is the similarity of the plane that takes $p$ and $q$ to their pins, and $E = 0$ there.

**Step 1 (the gradient of a corner function).** Let $\varphi_j$ be the affine function on the frame with $\varphi_j(q_j) = 1$ and $\varphi_j = 0$ on the opposite edge, from $q_{j+1}$ to $q_{j+2}$. Its gradient is perpendicular to that edge, points to $q_j$, and has length $1/h_j$, where $h_j = 2A_T / |\varepsilon_j|$ is the height. Multiplying by $i$ turns a complex number by $+90°$. For a counterclockwise triangle, $i \varepsilon_j$ points from the edge into the triangle. So, as a complex number $\partial_x \varphi_j + i\, \partial_y \varphi_j$, the gradient is $i \varepsilon_j / (2 A_T)$.

**Step 2 (part 1).** On $T$, $f = \sum_j U_{v_j} \varphi_j$, so with $\partial_{\bar z} = \frac12 (\partial_x + i \partial_y)$,

$$\partial_{\bar z} f = \sum_j U_{v_j}\, \partial_{\bar z} \varphi_j = \frac{i}{4 A_T} \sum_j \varepsilon_j U_{v_j} = \frac{i\, s_T}{4 A_T}.$$

So $|s_T|^2 / (4 A_T) = 4 A_T |\partial_{\bar z} f|^2$. With $f_x = u_x + i v_x$ and $f_y = u_y + i v_y$, $2 \partial_{\bar z} f = (u_x - v_y) + i (u_y + v_x)$, which gives the first form. Expanding the squares, $(u_x - v_y)^2 + (u_y + v_x)^2 = |\nabla u|^2 + |\nabla v|^2 - 2 (u_x v_y - u_y v_x)$. The last bracket is the determinant of the Jacobian of $f$, and $A_T$ times it is the signed area of the image of $T$. Summing over $T$ gives $E = 2 E_D - 2 \mathcal{A}$.

**Step 3 (part 2).** An affine map of the plane is $f(z) = a z + c \bar z + b$, and $\partial_{\bar z} f = c$. So $s_T = 0$ if and only if $c = 0$. In particular $E \ge 0$, and $E(U) = 0$ if and only if every $f_T$ has the form $a_T z + b_T$.

**Step 4 (the normal equations).** $E$ is a sum of squares of real linear forms in the real and imaginary parts of the $U_v$, each with the weight $1/(4 A_T) > 0$. With the pinned values fixed, $E$ is a quadratic function $x^\top N x - 2 r^\top x + c$ of the free values $x$, with $N$ symmetric and positive semidefinite. Its minimizers are exactly the solutions of $N x = r$, which always exist for a least squares problem. The minimizer is unique if and only if $N$ is nonsingular, that is, if and only if the only map with $E(U) = 0$ and $U_p = U_q = 0$ is $U = 0$, because the kernel of $N$ is the set of free values $y$ with $y^\top N y = 0$, which is $E$ of the map with the pins set to 0.

**Step 5 (part 3).** Let $U \ne 0$ with $E(U) = 0$ and $U_p = U_q = 0$. By Step 3, $f_T(z) = a_T z + b_T$ on each triangle. Let $T$ and $T'$ share the edge $xy$, of length $\ell > 0$. Both frames are congruent to the 3D triangles, so $|q^T_y - q^T_x| = |q^{T'}_y - q^{T'}_x| = \ell$, and

$$|a_T|\, \ell = |U_y - U_x| = |a_{T'}|\, \ell.$$

So $|a_T| = |a_{T'}|$, and since the dual graph is connected, $|a_T| = c$ for all $T$. If $c = 0$, every $f_T$ is constant, two triangles at an edge have the same constant, so $U$ is one constant, and $U_p = 0$ gives $U = 0$, which is false. So $c > 0$, and $U / c$ is a rotation and a translation of the frame on each triangle: a development that maps $p$ and $q$ to $0$.

Conversely, let $D$ be a development with $D(p) = D(q)$. Then $U = D - D(p)$ has $f_T(z) = a_T z + b_T$ with $|a_T| = 1$, so $E(U) = 0$ by Step 3, $U_p = U_q = 0$ and $U \ne 0$. So the kernel is not trivial. This proves part 3.

Three cases where uniqueness follows at once. (a) If $p$ and $q$ are two vertices of one triangle, a development is one to one on that triangle, so $D(p) \ne D(q)$. (b) If a development exists, the angles of the triangles around each inner vertex add up to a multiple of $2\pi$: going around the vertex, the image of the first edge turns by each angle in turn and must come back to itself. So if some inner vertex has an angle sum that is not a multiple of $2\pi$, no development exists, and the minimizer is unique for any two pins. (c) If two developments are given, on each triangle they differ by a rotation and translation, two triangles at an edge agree on its two distinct end points, and a rotation and translation is fixed by two distinct points. So all developments of a mesh with connected dual graph differ by one rigid motion of the plane.

**Step 6 (part 4).** For a planar mesh with its own coordinates as frames, the identity is a development, so by (c) every development is a rigid motion of the identity, and it maps $p$ and $q$ to different points because their positions differ. So the minimizer is unique. The similarity $S(z) = a z + b$ with $S(x_p) = $ pin of $p$ and $S(x_q) = $ pin of $q$ exists, as $x_p \ne x_q$, and has $s_T = a \sum_j \varepsilon_j q_j + b \sum_j \varepsilon_j = 0$ for every $T$, because $\sum_j \varepsilon_j = 0$ and $\sum_j (q_{j+2} - q_{j+1}) q_j = 0$ (the six products cancel in pairs). So $E(S) = 0$, which is the minimum, and the unique minimizer is $S$. With int or Fraction coordinates and pins, the normal equations have rational entries and Gaussian elimination solves them exactly, so the computed map equals $S$ exactly.

**Termination.** LSCM builds $N$ and $r$ in one pass over the triangles and solves one linear system of size $2(n - 2)$ by elimination, which stops after $O(n^3)$ operations. If $N$ is singular, by part 3 the input has a development that maps the pins to one point, and the code reports this. $\blacksquare$

**Remark (Desbrun, Meyer and Alliez).** Their discrete conformal parameterization minimizes $E_D - \mathcal{A}$, which by part 1 is $E / 2$. So with the same pins both methods give the same map.
