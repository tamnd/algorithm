---
title: The grid of a certified polycube map gives valid conforming hexes at every resolution
proves: [correctness, termination]
status: full
---

**Setting.** A polycube $P$ is the union of a finite set $C$ of unit voxels $c + [0, 1]^3$ with $c \in \mathbb{Z}^3$. Each integer corner $k$ of a voxel has an image $G(k) \in \mathbb{R}^3$. On the voxel $c$ the map $g_c(c + x) = \sum_{r} B_r(x)\, G(c + r)$, with $x \in [0, 1]^3$, the sum over the 8 corners $r \in \{0, 1\}^3$ and $B_r(x) = \prod_t x_t^{r_t} (1 - x_t)^{1 - r_t}$, is the trilinear map of the hex $(G(c + r))_r$. POLYCUBE-GRID($C$, $G$, $s$) rejects the input if, for some voxel, one of the 27 Bernstein coefficients of $\det Dg_c$ is at most $0$ (L1 and L2). Otherwise it maps every point $k / s$ of the grid $\frac{1}{s}\mathbb{Z}^3 \cap P$ by $g$ (L3 to L5) and returns, for every voxel $c$ and every cell $q \in \{0, \dots, s - 1\}^3$, the hex whose corners are the images of the 8 corners $c + (q + r)/s$ of the cell (L6 to L9).

**Claim.**

1. The algorithm stops after $O(|C|)$ Bernstein tests and $O(|C| s^3)$ further steps, and returns $|C| s^3$ hexes.
2. The maps $g_c$ agree on shared faces, edges and corners of voxels, so they define one continuous map $g : P \to \mathbb{R}^3$, and the image of a grid point does not depend on the voxel used in L5.
3. The trilinear map of the hex of the cell $q$ of $c$ is $H(u) = g_c(c + (q + u)/s)$ for $u \in [0, 1]^3$, and $\det DH(u) = s^{-3} \det Dg_c\big(c + (q + u)/s\big)$.
4. If the input is accepted, $\det Dg_c > 0$ on every closed voxel. So every hex has $\det J > 0$ on the whole closed unit cube, for every $s \ge 1$, and in particular its 8 corner Jacobians are positive.
5. The hexes are conforming: a face of a grid cell that lies in two voxels of $P$ is a face of exactly two hexes, with the same four corner points, and the other faces are on the boundary of $P$. The number of boundary quads is $s^2$ times the number of unit faces on the boundary of $P$.
6. The signed volumes of the hexes add up to $\sum_c \int \det Dg_c$, which does not depend on $s$.
7. If, in addition, $g$ is one to one on $P$, the hexes are the images of the grid cells under $g$ and tile $g(P)$ with disjoint interiors. So the output is a valid conforming hex mesh of $g(P)$.

**Proof of part 1.** L1 and L2 do a constant amount of work per voxel. A voxel has $(s + 1)^3$ grid points and $s^3$ cells, so L3 to L8 take $O(|C| s^3)$ steps.

**Proof of part 2.** Let two voxels share the face $x_t = 1$ of the first and $x_t = 0$ of the second. On it, $B_r$ is $0$ for the corners with $r_t \ne 1$ in the first voxel, and the remaining four terms are the bilinear interpolation of the four shared corner images. The second voxel gives the same four corners with the same bilinear weights. The same argument with fewer free variables covers shared edges and corners. So the formulas agree wherever two voxels meet.

**Proof of part 3.** The map $u \mapsto c + (q + u)/s$ is affine in each coordinate on its own. A trilinear map composed with it is again of degree at most $1$ in each $u_t$, so $H$ is trilinear. A trilinear map is fixed by its values at the 8 corners of the cube, and $H$ takes at the corner $r$ the value $g(c + (q + r)/s)$, which by part 2 is the point that L5 stores for the key $s c + q + r$. So $H$ is the trilinear map of the hex built in L8. The chain rule gives $DH(u) = \frac{1}{s} Dg_c(\cdot)$, and the determinant of a $3 \times 3$ matrix scales by $s^{-3}$.

**Proof of part 4.** The column $\partial_{x_t} g_c$ has degree $0$ in $x_t$ and at most $1$ in the other two variables. The determinant is a sum of products of one entry from each column, so it has degree at most $2$ in each variable. It is therefore a unique combination $\det Dg_c(x) = \sum_{i,j,l} b_{ijl}\, \beta_i(x_0) \beta_j(x_1) \beta_l(x_2)$ of the tensor Bernstein basis of degree $2$, with $\beta_0(t) = (1 - t)^2$, $\beta_1(t) = 2t(1 - t)$ and $\beta_2(t) = t^2$. On $[0, 1]$ these are at least $0$ and add up to $((1 - t) + t)^2 = 1$, so the 27 products are at least $0$ and add up to $1$. Hence $\det Dg_c(x) \ge \min b_{ijl} > 0$ on the closed voxel. The code finds the $b_{ijl}$ from the values at $\{0, \frac12, 1\}^3$ by the exact one-dimensional rule $b_0 = f(0)$, $b_1 = 2 f(\frac12) - \frac12 (f(0) + f(1))$, $b_2 = f(1)$, applied in each direction. Part 3 then gives $\det DH > 0$ on the closed unit cube for every cell. The corner Jacobian at a corner of a trilinear hex equals $\det DH$ at that corner, so it is positive too.

**Proof of part 5.** Grid points are named by integer keys, and L8 names the corners of the cell $q$ of $c$ by the keys $s c + q + r$. Two cells that share a face of the cubical grid use the same four keys on it, and by part 2 the same four points. A face of the cubical grid of spacing $1/s$ lies in at most two cells of the grid, and it lies in two cells of $P$ exactly when it is inside $P$ or between two voxels of $P$. A boundary face of a cell lies in a unit boundary face of $P$, and each unit face holds $s^2$ such faces.

**Proof of part 6.** The signed volume of a hex is $\int_{[0,1]^3} \det DH$. By part 3 and the change of variables $x = (q + u)/s$, this is $\int \det Dg_c$ over the cell $c + (q + [0, 1]^3)/s$. The $s^3$ cells of a voxel cover it and meet only on their faces, so the sum over the cells is $\int \det Dg_c$ over the voxel.

**Proof of part 7.** By part 3 each hex is the set $g(Q)$ for its grid cell $Q$. The grid cells tile $P$, so the images $g(Q)$ cover $g(P)$. The polycube $P$ is compact and $g$ is continuous and one to one, so $g$ is a homeomorphism from $P$ onto $g(P)$. By the invariance of domain, the interior of $g(Q)$ is $g(\operatorname{int} Q)$. The interiors of two cells are disjoint, and $g$ is one to one, so their images are disjoint. $\blacksquare$

**Remarks.** The test of L2 is sufficient, not necessary: a positive determinant can have a Bernstein coefficient at most $0$, and then the input is rejected, although subdivision of the voxel would certify it. Positive corner Jacobians of the voxel hexes are not enough. The test file has a voxel with corner Jacobians $4$ and $12$ whose determinant is $4(1 - 2w)(1 - 4w)$, which is negative for $\frac14 < w < \frac12$. Without the test, the grid of resolution $3$ has hexes with the corner Jacobian $-\frac{4}{243}$. Part 7 needs $g$ to be one to one. Local positivity alone does not give this when the image folds over itself across many voxels, so a full method must also check the boundary of $g(P)$ for self-intersections.
