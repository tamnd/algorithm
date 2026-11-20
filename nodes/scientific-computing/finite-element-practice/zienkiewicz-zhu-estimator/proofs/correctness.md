---
title: The ZZ indicators are computed exactly, vanish on linear solutions, and are asymptotically exact when the recovery superconverges
proves: [correctness]
status: full
---

**Setting.** $\mathcal{T}$ is a conforming triangulation of a polygon $\Omega$, and $u_h$ is a continuous piecewise linear function on it with nodal values $U$. Its gradient $\nabla u_h$ is constant on each triangle. A recovery returns one vector $G(z) \in \mathbb{R}^2$ for each vertex $z$, and $G$ also denotes the continuous piecewise linear vector field with these nodal values. The indicator is $\eta_K = \|G - \nabla u_h\|_{L^2(K)}$, and the total is $\eta = (\sum_K \eta_K^2)^{1/2} = \|G - \nabla u_h\|_{L^2(\Omega)}$. ZZ-ESTIMATE is lines L1 to L5 of the main page, and SPR-RECOVER is lines L6 to L11. Arithmetic is exact (real-RAM).

We prove four claims.

1. *(Exact integration.)* Line L3 computes $\eta_K^2$ exactly.
2. *(Linear fit.)* If the points of a patch do not all lie on one line and the data are the values of a linear polynomial $q$ at these points, the least squares fit at line L7 returns $q$.
3. *(Consistency.)* If $u_h$ is linear on all of $\Omega$, then both the SPR and the averaging recovery give $G = \nabla u_h$, and every $\eta_K$ is 0.
4. *(Asymptotic exactness.)* Let $u$ be the exact solution and $e = \|\nabla u - \nabla u_h\|_{L^2(\Omega)}$. Then $|\eta - e| \le \|\nabla u - G\|_{L^2(\Omega)}$. So if $\|\nabla u - G\| / e \to 0$ on a sequence of meshes, the effectivity index $\eta / e$ tends to 1.

**Proof of 1.** On $K$, $G$ is linear and $\nabla u_h$ is constant, so each component of $G - \nabla u_h$ is a linear function and $|G - \nabla u_h|^2$ is a polynomial of degree 2. The edge midpoint rule $\int_K p \approx \tfrac{|K|}{3}\sum_{r=1}^{3} p(m_r)$, with $m_r$ the midpoints of the edges, is exact for all polynomials of degree 2 on a triangle. (Check it on $1$, on $\lambda_i$ and on $\lambda_i\lambda_j$ in barycentric coordinates: the integrals are $|K|$, $|K|/3$, $|K|/12$ for $i \ne j$ and $|K|/6$ for $i = j$, and the rule gives the same numbers.) A linear function at the midpoint of an edge is the mean of its values at the two ends, which is the formula used at line L3. Line L4 takes the square root. $\square$

**Proof of 2.** The fit minimizes $\sum_t (a + b x_t + c y_t - d_t)^2$ over $(a, b, c)$. The value 0 is the smallest possible, and $(a, b, c)$ equal to the coefficients of $q$ reaches it. The minimizer is unique: two minimizers $p_1$ and $p_2$ would both reach 0, so $p_1 - p_2$ is a linear polynomial that is 0 at all points. A nonzero linear polynomial is 0 only on a line, and the points do not all lie on one line. So $p_1 = p_2 = q$. The same condition makes the $3 \times 3$ normal matrix regular, so Cramer's rule in the code finds this minimizer. $\square$

**Proof of 3.** Let $\nabla u_h = c$ on every triangle. *Averaging.* Each nodal value is a weighted mean of copies of $c$ with positive weights, so it is $c$. *SPR.* At an interior vertex the data at line L7 are the constant $c$, which is a linear polynomial. If the centroids do not lie on one line, claim 2 gives the fit $q = c$, and line L8 sets $G(v) = c$. If they lie on one line, the code uses the averaging value, which is also $c$. At line L9 every evaluation of a fit is $c$, so the mean at line L10 is $c$. A boundary vertex that no interior patch reaches also takes the averaging value $c$. So $G \equiv c$, and $G - \nabla u_h = 0$ on every triangle. $\square$

**Proof of 4.** By the triangle inequality in $L^2(\Omega)^2$,
$$\eta = \|G - \nabla u_h\| \le \|G - \nabla u\| + \|\nabla u - \nabla u_h\| = \|\nabla u - G\| + e,$$
and in the same way $e \le \|\nabla u - G\| + \eta$. So $|\eta - e| \le \|\nabla u - G\|$. Divide by $e > 0$: $|\eta/e - 1| \le \|\nabla u - G\|/e$, and the right side tends to 0 by the hypothesis. $\square$

**Remarks.** Claim 4 is the theorem of Zienkiewicz and Zhu. Its hypothesis is a superconvergence property: the recovered gradient must be closer to $\nabla u$ than the raw gradient by more than a constant factor. For P1 elements and smooth $u$ it is known on meshes with a structure, for example uniform meshes and meshes that are close to uniform in a precise sense. On general meshes, Carstensen and Bartels proved that averaging estimators are reliable and efficient up to constants and higher order terms, but the effectivity then does not have to tend to 1. The test file checks claims 2 and 3 on random data and random perturbed meshes, and it measures an effectivity within 2 percent of 1 on uniform meshes.

**Cost.** Each triangle sends its gradient to its three vertices. Each interior vertex solves one $3 \times 3$ system with a patch of bounded size, and each triangle then does a fixed amount of work at lines L2 to L4. For a mesh with bounded vertex degree this is $O(M)$ operations for $M$ triangles.
