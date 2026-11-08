---
title: The P1 finite element system is assembled correctly, uniquely solvable, and its solution is the energy-norm best approximation
proves: [correctness, termination]
status: full
---

**Setting.** $\Omega \subset \mathbb{R}^2$ is a bounded polygon with a conforming triangulation $\mathcal{T}_h$: triangles with nonzero area whose union is $\bar\Omega$ and any two of which meet in a common vertex, a common edge, or not at all. Nodes are the vertices $x_1, \ldots, x_N$; boundary nodes lie on $\partial\Omega$, the others are interior. $V_h$ is the space of continuous functions that are linear on each triangle, with nodal basis $\varphi_i(x_j) = \delta_{ij}$, and $V_{h,0} = \operatorname{span}\{\varphi_i : i \text{ interior}\}$. We write $a(u, v) = \int_\Omega \nabla u \cdot \nabla v\,dx$, $|v|_1 = a(v, v)^{1/2}$, and $\ell_h(v)$ for the load functional computed by quadrature, $\ell_h(\varphi_i) = F_i$.

**Lemma 1 (element matrices).** Let a triangle $e$ have vertices $(x_k, y_k)$, $k = 1, 2, 3$, $D = (x_2 - x_1)(y_3 - y_1) - (x_3 - x_1)(y_2 - y_1) \ne 0$, and $b_1 = y_2 - y_3$, $c_1 = x_3 - x_2$, with $b_2, c_2, b_3, c_3$ obtained by cyclic shifts of the indices. The linear function equal to 1 at vertex $k$ and 0 at the other two has gradient $(b_k, c_k)/D$, and

$$\int_e \nabla\varphi_k \cdot \nabla\varphi_l \, dx = \frac{b_kb_l + c_kc_l}{2|D|}.$$

*Proof.* Let $\psi_1(x, y) = \big(x_2y_3 - x_3y_2 + b_1x + c_1y\big)/D$. At $(x_2, y_2)$ the numerator is $x_2y_3 - x_3y_2 + (y_2 - y_3)x_2 + (x_3 - x_2)y_2 = 0$, and similarly at $(x_3, y_3)$. At $(x_1, y_1)$ it is $x_2y_3 - x_3y_2 + y_2x_1 - y_3x_1 + x_3y_1 - x_2y_1$, which expands to $D$. So $\psi_1 = \varphi_1$ on $e$ and $\nabla\varphi_1 = (b_1, c_1)/D$; the other two follow by symmetry. The gradients are constant and the area is $|D|/2$, which gives the integral. $\square$

The implementation computes exactly this (with `2 * abs(det)` in the denominator), so the orientation of the vertex list does not matter.

**Lemma 2 (assembly).** After lines L1 to L5, $K_{ij} = a(\varphi_j, \varphi_i)$ for all $i, j$, and $F_i = \sum_e Q_e(f\varphi_i)$, where $Q_e$ is the edge-midpoint rule on $e$.

*Proof.* $a(\varphi_j, \varphi_i) = \sum_{e \in \mathcal{T}_h}\int_e \nabla\varphi_j \cdot \nabla\varphi_i$. On a triangle $e$, the global $\varphi_i$ is the local basis function of vertex $i$ if $i$ is a vertex of $e$ and is zero otherwise (it is linear on $e$ and its values at the three vertices are those of the local function or all zero). So the integral over $e$ is $K^e_{kl}$ (Lemma 1) when $i = v_k$ and $j = v_l$ are vertices of $e$, and zero otherwise. Line L4 adds exactly the nonzero terms. For the load, the edge-midpoint rule $Q_e(w) = \frac{|e|}{3}\sum_{\text{edges}} w(m)$ evaluated at $w = f\varphi_k$ uses $\varphi_k(m) = \tfrac12$ at the midpoints of the two edges at vertex $k$ and $0$ at the third midpoint, which gives $F^e_k = \frac{|e|}{6}(f(m_{kl}) + f(m_{km}))$, added at line L5. $\square$

The edge-midpoint rule is exact for polynomials of degree 2, so $F_i = \ell(\varphi_i)$ exactly when $f$ is linear on each triangle.

**Lemma 3 (positive definiteness).** If every connected component of $\Omega$ contains a boundary node (always true for a bounded domain), then $K_{II} = (K_{ij})_{i,j \text{ interior}}$ is symmetric positive definite.

*Proof.* Symmetry is clear from Lemma 2. For a real vector $\xi$ indexed by interior nodes, let $v = \sum_i \xi_i\varphi_i \in V_{h,0}$. Then $\xi^TK_{II}\xi = a(v, v) = \int_\Omega |\nabla v|^2 \ge 0$. If it is zero, $\nabla v = 0$ on every triangle, so $v$ is constant on each triangle; being continuous, $v$ is constant on each connected component of $\bar\Omega$. Each component has a boundary node, where $v = 0$, so $v \equiv 0$ and $\xi = 0$. $\square$

**Theorem.** Let $g_h$ be the function in $V_h$ with $g_h(x_v) = g(x_v)$ at boundary nodes and $0$ at interior nodes.

1. (Well posed and computed.) There is exactly one $u_h \in g_h + V_{h,0}$ with $a(u_h, w) = \ell_h(w)$ for all $w \in V_{h,0}$, and FEM-POISSON returns its nodal values (up to the tolerance of conjugate gradients, or exactly with the direct solver in exact arithmetic).
2. (Céa's lemma.) Suppose the quadrature is exact ($\ell_h = \ell$ on $V_{h,0}$) and $g$ is linear on each boundary edge, and let $u \in H^1(\Omega)$ be the weak solution. Then for every $v \in g_h + V_{h,0}$,

$$|u - v|_1^2 = |u - u_h|_1^2 + |u_h - v|_1^2, \qquad\text{so}\qquad |u - u_h|_1 = \min_{v \in g_h + V_{h,0}}|u - v|_1.$$

   If moreover $g = 0$, then $|u - u_h|_1^2 = |u|_1^2 - |u_h|_1^2$.
3. (Patch test.) If $u$ is linear, $f = 0$ and $g = u$, then $u_h = u$ for every mesh.

*Proof.* (1) Write $u_h = g_h + \sum_{i \text{ interior}}U_i\varphi_i$. Testing with $w = \varphi_i$ for interior $i$ and using Lemma 2 gives $\sum_{j \text{ interior}}K_{ij}U_j = F_i - \sum_{v \text{ boundary}}K_{iv}g(x_v)$, which is the system formed at lines L6 and L7; conversely, if it holds for each basis function, it holds for all $w \in V_{h,0}$ by linearity. By Lemma 3 the matrix is nonsingular, so the solution exists and is unique. Line L8 solves it. Conjugate gradients on a symmetric positive definite system of order $n$ reaches the exact solution in at most $n$ steps in exact arithmetic, and the implementation stops at a residual tolerance or an iteration cap, so it terminates. Gaussian elimination without pivoting succeeds on a symmetric positive definite matrix because each Schur complement is again symmetric positive definite, so every pivot is positive.

(2) Since $g$ is linear on boundary edges, $g_h = g$ on $\partial\Omega$, so $u - v \in H^1_0(\Omega)$ for every $v \in g_h + V_{h,0}$, and $V_{h,0} \subset H^1_0(\Omega)$. Subtracting the discrete equation from the weak form tested with $w \in V_{h,0}$ gives Galerkin orthogonality $a(u - u_h, w) = 0$. With $w = u_h - v \in V_{h,0}$,

$$|u - v|_1^2 = |(u - u_h) + (u_h - v)|_1^2 = |u - u_h|_1^2 + 2a(u - u_h, u_h - v) + |u_h - v|_1^2 = |u - u_h|_1^2 + |u_h - v|_1^2.$$

The minimum is attained at $v = u_h$. If $g = 0$, take $v = 0$: then $|u|_1^2 = |u - u_h|_1^2 + |u_h|_1^2$.

(3) A linear $u$ lies in $V_h$, and $u - g_h \in V_{h,0}$ because $g_h$ agrees with $u$ at boundary nodes. For $w \in V_{h,0}$, integrating by parts on $\Omega$ gives $a(u, w) = \int_\Omega(-\Delta u)w = 0$ because $\Delta u = 0$ and $w = 0$ on $\partial\Omega$; and $\ell_h(w) = 0$ for $f = 0$. So $u$ satisfies the discrete equations, and by uniqueness in (1), $u_h = u$. $\blacksquare$

**Error estimates (cited, not proved here).** For a family of shape-regular triangulations and $u \in H^2(\Omega)$, the nodal interpolant satisfies $|u - I_hu|_1 \le Ch|u|_2$ (Bramble-Hilbert lemma; Brenner and Scott 2008, Chapter 4). With part (2) and $v = I_hu$ this gives $|u - u_h|_1 \le Ch|u|_2$. If $\Omega$ is convex, the solution of $-\Delta z = e$ with $z = 0$ on $\partial\Omega$ satisfies $|z|_2 \le \|e\|_{L^2}$, and the Aubin-Nitsche argument (apply orthogonality to $a(u - u_h, z - I_hz)$ with $e = u - u_h$) gives $\|u - u_h\|_{L^2} \le Ch^2|u|_2$ (Brenner and Scott 2008, Chapter 5; Ciarlet 2002, Chapter 3). Quadrature errors in $\ell_h$ add a term of the same orders for smooth $f$ (Strang's first lemma). These are asymptotic bounds with unspecified constants; the rates in the Example of the main page are observed.
