---
title: The power test is exact, pumping keeps the triangulation regular and never lowers the smallest dihedral angle, and the Sliver Theorem gives a dihedral angle bound
proves: [correctness]
status: full
---

**Claim.** Assume general position: no five lifted weighted points lie on a common hyperplane, and no candidate weight equals a critical weight.

1. The test of L11 returns $-\pi\, |\mathrm{orient3d}(a, b, c, d)|$, where $\pi$ is the power distance from $(e, w_e)$ to the orthosphere of the four weighted points $a, b, c, d$. So it is positive exactly when $(e, w_e)$ conflicts with the tetrahedron, and with all weights $0$ it is the insphere test. The critical weight of L4 is the power distance from $(u, 0)$ to the orthosphere, and $(u, w)$ conflicts with $t$ exactly when $w > w_t$.
2. For each weight $w$, the set $(T_u \setminus \{t : w_t < w\}) \cup \mathrm{star}(w)$ is the weighted Delaunay triangulation with $u$ at weight $w$, as long as $(u, w)$ is a vertex of it.
3. The smallest dihedral angle of the mesh after the pump of L9 is at least the one before.
4. Every tetrahedron with shortest edge $L$, longest edge $D$ and volume $V$ has every dihedral angle $\theta$ with $\sin\theta \ge 8\Sigma / \lambda^4$, where $\Sigma = V / L^3$ and $\lambda = D / L$.
5. If the weights have the Weight Property $[\Omega_0]$, every tetrahedron of the weighted Delaunay triangulation with orthoradius $Z$ has $D^2 (1 - 4\Omega_0^2) \le 4 Z^2$.
6. Hence, for the weights of the Sliver Theorem, every dihedral angle of the weighted Delaunay triangulation satisfies $\sin\theta \ge \Sigma_0 (1 - 4\Omega_0^2)^2 / (2 \rho_1^4)$.

**What is cited.** Part 6 uses the Sliver Theorem (Section 6.5 of Cheng, Dey, Edelsbrunner, Facello and Teng, J. ACM 2000), which gives $\Sigma > \Sigma_0$, and their Claim 7 (Section 5.1), which gives $Z / L \le \rho_1$; neither proof is repeated, and the paper gives no number for $\Sigma_0$ or $\rho_1$. Part 2 uses the standard fact that the weighted Delaunay triangulation is the projection of the lower convex hull of the lifted points (Chapter 7 of Cheng, Dey and Shewchuk) and the beneath-beyond rule for adding a point to a convex hull. The fact that every point stays a vertex under the Weight Property is from the paper (Section 4.2).

**Step 1: the lifting.** Lift a weighted point $(p, w_p)$ to $p^+ = (p, \ell_p)$ in $\mathbb{R}^4$ with $\ell_p = |p|^2 - w_p$. The orthosphere $(z, Z^2)$ of $a, b, c, d$ satisfies $|p - z|^2 - Z^2 = w_p$, which expands to $\ell_p = 2 z \cdot p - |z|^2 + Z^2$. So the four lifted points lie on the graph of the affine function $h(x) = 2 z \cdot x - |z|^2 + Z^2$. For any weighted point $(e, w_e)$,
$$|e - z|^2 - Z^2 - w_e = \ell_e - h(e),$$
so the power distance $\pi$ of $(e, w_e)$ to the orthosphere is the height of $e^+$ above that graph. Conflict, $\pi < 0$, means that $e^+$ lies below the hyperplane through $a^+, b^+, c^+, d^+$.

**Step 2: the determinant (part 1).** Let $M$ be the $4 \times 4$ matrix with rows $(p - e,\ |p - e|^2 - w_p + w_e)$ for $p = a, b, c, d$. Since
$$|p - e|^2 - w_p + w_e = (\ell_p - \ell_e) - 2 e \cdot (p - e),$$
subtracting $2 e_k$ times column $k$ from column 4, for $k = 1, 2, 3$, gives rows $(p - e,\ \ell_p - \ell_e)$ with the same determinant. Now $\ell_p = h(p)$ for the four vertices, and $h(p) - \ell_e = 2 z \cdot (p - e) + h(e) - \ell_e = 2 z \cdot (p - e) - \pi$. Subtracting $2 z_k$ times column $k$ from column 4 gives rows $(p - e,\ -\pi)$. Factor out $-\pi$: the determinant of the rows $(p - e, 1)$ is, after subtracting the first row from the others, the determinant of the rows $(a - e, 1), (b - a, 0), (c - a, 0), (d - a, 0)$, which by expansion along the last column is $-\det[b - a, c - a, d - a] = -\mathrm{orient3d}(a, b, c, d)$. So
$$\det M = (-\pi)(-\mathrm{orient3d}) = \pi \cdot \mathrm{orient3d}(a, b, c, d).$$
The implementation returns $-\det M$ times the sign of orient3d, which is $-\pi\, |\mathrm{orient3d}|$: positive exactly when $\pi < 0$. With all weights $0$, $M$ is the insphere matrix and the orthosphere is the circumsphere. For the critical weight, put $w_e = 0$: the implementation divides $\det M$ by orient3d and gets $\pi_0 = |u - z|^2 - Z^2$. With weight $w$ the power distance is $\pi_0 - w$, negative exactly when $w > \pi_0 = w_t$.

**Step 3: the star (part 2).** The weighted Delaunay triangulation of a set of weighted points is the vertical projection of the lower convex hull of their lifts, by Step 1: a tetrahedron is in it exactly when no lifted point lies below the hyperplane through its four lifted vertices. Adding the point $u^+ = (u, |u|^2 - w)$ to a lower convex hull removes exactly the facets whose hyperplane passes above $u^+$, the facets visible from below, and joins $u^+$ to the boundary of that region (beneath-beyond). By Step 2 these facets are the tetrahedra $t$ of $T_u$ with $w_t < w$. So the new triangulation is $T_u$ without them, plus $u$ joined to the boundary faces of the removed region, which is $\mathrm{star}(w)$ of L7. If $w$ is not a critical weight, every $w_t$ is either below or above $w$, so no tetrahedron is degenerate, and the triangulation is the same for all $w$ in one open interval between consecutive critical weights. Hence L6 tries every triangulation that a weight in $[0, W]$ can give, except those at the critical weights themselves.

**Step 4: monotonicity (part 3).** By induction, before $u$ is pumped the mesh $T$ is the weighted Delaunay triangulation with $w_u = 0$, because each pump installs the triangulation for the chosen weight (Step 3) and $u$ has not been pumped yet. Write $C(w) = \{t \in T_u : w_t < w\}$. Then $T = (T_u \setminus C(0)) \cup \mathrm{star}(0)$. Let $m$ be the smallest dihedral angle of $T$; in particular $\zeta(0) \ge m$, since $\mathrm{star}(0) \subseteq T$. The chosen weight $w^* \ge 0$ satisfies $\zeta(w^*) \ge \zeta(0)$ by L8, since $0$ is a candidate. Every $t$ with $w_t < 0$ also has $w_t < w^*$, so $C(0) \subseteq C(w^*)$ and $T_u \setminus C(w^*) \subseteq T_u \setminus C(0) \subseteq T$. The new mesh is $(T_u \setminus C(w^*)) \cup \mathrm{star}(w^*)$. Its tetrahedra of the first kind belong to $T$ and have angles at least $m$; those of the second kind have angles at least $\zeta(w^*) \ge \zeta(0) \ge m$.

**Step 5: angle, volume and edges (part 4).** Let $\theta$ be the dihedral angle at edge $e$, between the faces $F_1$ and $F_2$ of areas $A_1$ and $A_2$. The vertex of $F_2$ off $e$ is at distance $2A_2 / |e|$ from the line of $e$, and at distance $(2A_2 / |e|) \sin\theta$ from the plane of $F_1$. So
$$V = \frac13 A_1 \cdot \frac{2 A_2}{|e|} \sin\theta, \qquad \sin\theta = \frac{3 V |e|}{2 A_1 A_2}.$$
A triangle with all sides at most $D$ has area at most $\frac{\sqrt3}{4} D^2$: if $c$ is its longest side, the third corner is within $D$ of both ends of $c$, so its height over $c$ is at most $\sqrt{D^2 - c^2/4}$, and $\frac12 c \sqrt{D^2 - c^2/4}$ increases in $c$ for $c \le \sqrt2 D$, so it is largest at $c = D$. Thus $A_1 A_2 \le \frac{3}{16} D^4$, and with $|e| \ge L$,
$$\sin\theta \ge \frac{3 V L}{2 \cdot \frac{3}{16} D^4} = \frac{8 V L}{D^4} = \frac{8\, (V / L^3)}{(D / L)^4} = \frac{8\Sigma}{\lambda^4}.$$

**Step 6: the Weight Property bounds the longest edge (part 5).** Let $p, q$ be vertices of a tetrahedron of the weighted Delaunay triangulation, with orthosphere $(z, Z^2)$. Then $|p - z|^2 = Z^2 + w_p$, and the Weight Property gives $w_p = P^2 \le \Omega_0^2 |p - q|^2 \le \Omega_0^2 D^2$, and likewise for $q$. By the triangle inequality,
$$|p - q| \le |p - z| + |q - z| \le 2 \sqrt{Z^2 + \Omega_0^2 D^2}.$$
Taking $p, q$ at the ends of the longest edge, $D^2 \le 4 Z^2 + 4 \Omega_0^2 D^2$, that is $D^2 (1 - 4\Omega_0^2) \le 4 Z^2$. Since $\Omega_0 < \frac12$ the left side is positive, so in particular $Z^2 > 0$.

**Step 7: the dihedral bound (part 6).** Under the hypotheses of the Sliver Theorem, its weights give $\Sigma > \Sigma_0$ for every tetrahedron, and Claim 7 gives $Z \le \rho_1 L$. By Step 6, $\lambda = D / L \le 2 \rho_1 / \sqrt{1 - 4\Omega_0^2}$, so $\lambda^4 \le 16 \rho_1^4 / (1 - 4\Omega_0^2)^2$. By Step 5,
$$\sin\theta \ge \frac{8 \Sigma_0 (1 - 4\Omega_0^2)^2}{16 \rho_1^4} = \frac{\Sigma_0 (1 - 4\Omega_0^2)^2}{2 \rho_1^4}.$$
For $\Omega_0 = 0.45$ the factor $(1 - 4\Omega_0^2)^2 / 2$ equals $0.01805$. The bound is positive but inherits the unknown and, by the paper's own account, tiny $\Sigma_0$; it is far below the $5°$ seen in practice.

**What is not proved.** Part 6 is about the weights of the theorem. That the rule of L8, which maximizes the smallest dihedral angle rather than the smallest $\Sigma$, reaches weights at least as good is not proved here. The implementation also has a boundary, which the theorem excludes. The tests check parts 1 to 5 exactly or to floating point precision on every tetrahedron of two examples. $\blacksquare$
