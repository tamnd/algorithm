---
title: The grid geomorph equals the coarse surface at alpha 0 and the fine surface at alpha 1, and every surface point moves linearly in alpha
proves: [correctness]
status: full
---

We use the setup of the page. The fine mesh has the grid points $(x, y)$ with $0 \le x, y \le m$ and $m$ even, and each unit cell is cut by the diagonal from $(x, y)$ to $(x + 1, y + 1)$. The coarse mesh has the even grid points, and each cell of side 2 is cut by the diagonal in the same direction. The heights $h$ are given at all fine vertices. For a mesh and vertex values $g$, the surface $S_g$ is the function that is affine on each triangle and takes the value $g(v)$ at each vertex $v$. The arithmetic is exact.

**Lemma 1.** Each fine vertex that is not a coarse vertex is the midpoint of exactly the coarse edge that `coarse_edge` returns. Each coarse triangle is the union of four fine triangles, whose vertices are the three corners of the coarse triangle and the midpoints of its three edges.

*Proof.* A fine vertex $(x, y)$ with $x$ odd and $y$ even is the midpoint of the horizontal coarse edge from $(x - 1, y)$ to $(x + 1, y)$; with $x$ even and $y$ odd, of the vertical edge from $(x, y - 1)$ to $(x, y + 1)$; with both odd, of the diagonal from $(x - 1, y - 1)$ to $(x + 1, y + 1)$, which is a coarse edge because the coarse diagonals have the direction $(1, 1)$. These are the three cases of the code. Take the coarse triangle with the corners $(x_0, y_0)$, $(x_0 + 2, y_0)$ and $(x_0 + 2, y_0 + 2)$, with $x_0$ and $y_0$ even. Its edge midpoints are $(x_0 + 1, y_0)$, $(x_0 + 2, y_0 + 1)$ and $(x_0 + 1, y_0 + 1)$. The fine triangles in it are the lower triangle of the cell at $(x_0, y_0)$, both triangles of the cell at $(x_0 + 1, y_0)$, and the lower triangle of the cell at $(x_0 + 1, y_0 + 1)$, and their vertices are these six points. The other coarse triangle of the cell is the same after the exchange of $x$ and $y$. $\square$

**Theorem 2.** Let $g_\alpha$ be the vertex values of lines L1 to L4. On the fine mesh, $S_{g_0}$ equals the coarse surface $S^c_h$ (the coarse mesh with the values $h$ at the coarse vertices) at every point of the domain, $S_{g_1}$ equals the fine surface $S_h$, and for each point $p$, $S_{g_\alpha}(p) = (1 - \alpha) S_{g_0}(p) + \alpha S_{g_1}(p)$.

*Proof.* At $\alpha = 1$, line L3 gives $g_1(v) = h(v)$, and line L2 gives $h(v)$ at the coarse vertices, so $g_1 = h$.

At $\alpha = 0$, a coarse vertex keeps $h(v) = S^c_h(v)$. A vertex $v$ of the other kind gets the mean of $h$ at the two ends of the coarse edge through it (Lemma 1). The coarse surface is affine along that edge, so this mean is $S^c_h(v)$. So $g_0(v) = S^c_h(v)$ at every fine vertex. Now take a fine triangle $t$. By Lemma 1 it lies in one coarse triangle, on which $S^c_h$ is affine. Both $S_{g_0}$ and $S^c_h$ are affine on $t$ and agree at its three vertices, so they agree on $t$.

For the last claim, the value $S_g(p)$ is $\sum_v \beta_v(p)\, g(v)$ over the three vertices of the fine triangle that holds $p$, with barycentric coordinates $\beta_v(p)$ that do not depend on $g$. Each $g_\alpha(v)$ is $(1 - \alpha) g_0(v) + \alpha g_1(v)$, so the sum is affine in $\alpha$ in the same way. $\square$

The morph keeps the fine connectivity for all $\alpha$, so it never has a crack or a T-junction: it is one conforming triangulation whose vertex heights move. A coarse vertex does not move. The other vertices move only in height, along the vertical line through their domain point. This is the vertical form of the geomorph that terrain methods use. The geomorph of Hoppe moves the two vertices of a vertex split from the position of their parent, which is a different start position; the linear blend of the positions is the same.

**Corollary 3.** If the blend factor $\alpha$ goes from 0 to 1 over a time or a distance range, the height of each surface point is continuous in that time or distance, and the largest jump at the start or the end of the range is 0.

*Proof.* $S_{g_\alpha}(p)$ is affine in $\alpha$ by Theorem 2, so it is continuous in any parameter on which $\alpha$ depends continuously. At $\alpha = 0$ it is the surface that was drawn before the change, and at $\alpha = 1$ the surface that is drawn after it. $\square$
