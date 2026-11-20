---
title: The arc-length steps keep the constraint, and the bordered system is regular at limit points
proves: [correctness]
status: partial
---

**Setting.** $f_{\rm int} : \mathbb R^n \to \mathbb R^n$ is twice continuously differentiable with tangent $K_T(u)$, $P \ne 0$ is fixed, and $G(u, \lambda) = f_{\rm int}(u) - \lambda P$. The equilibrium path is the set where $G = 0$. A point of the path is *regular* if the $n \times (n + 1)$ matrix $[K_T(u), -P]$ has rank $n$. Near a regular point the path is a smooth curve by the implicit function theorem, and its tangent $t = (\dot u, \dot\lambda)$ spans the null space of $[K_T, -P]$. The status is partial because the local convergence of Crisfield's quadratic form is only sketched (Remark 6).

**Lemma 1 (recorded points are in equilibrium).** Every point recorded at line L10 satisfies $\|G(u, \lambda)\| \le$ tol.

*Proof.* The loop of line L5 exits only through the test of line L6, which checks this inequality for $(u + \Delta u, \lambda + \Delta\lambda)$, and line L10 records exactly this pair. In the reference code a step whose loop ends in another way is not recorded; it is repeated with half the arc length. $\square$

**Lemma 2 (the predictor).** If $K_T(u)$ is nonsingular, line L3 gives the tangent of the path at $(u, \lambda)$, and the increment of line L4 satisfies $\Delta u^\top \Delta u + \psi^2 \Delta\lambda^2 P^\top P = \Delta l^2$.

*Proof.* $K_T u_t = P$ means $[K_T, -P]\,(u_t, 1) = 0$, so $(u_t, 1)$ spans the null space, which is the tangent direction. With $\Delta u = \Delta\lambda\,u_t$ the left side of the constraint is $\Delta\lambda^2 (u_t^\top u_t + \psi^2 P^\top P)$, which is $\Delta l^2$ for $\Delta\lambda = \pm \Delta l / \sqrt{u_t^\top u_t + \psi^2 P^\top P}$. $\square$

**Lemma 3 (the corrector keeps the constraint).** Let $(\Delta u, \Delta\lambda)$ satisfy the constraint or not, and let $u_r$, $u_t$ be the solutions of line L7. For every real root $d$ of $a d^2 + b d + c = 0$ with the coefficients of the page, the new increment $(\Delta u + u_r + d\,u_t, \Delta\lambda + d)$ satisfies the constraint exactly. It also satisfies the linearized equilibrium equation: $G(u + \Delta u, \lambda + \Delta\lambda) + K_T\,(u_r + d\,u_t) - d\,P = 0$.

*Proof.* Put $w = \Delta u + u_r$. Then $|w + d u_t|^2 + \psi^2(\Delta\lambda + d)^2 P^\top P - \Delta l^2 = d^2(u_t^\top u_t + \psi^2 P^\top P) + 2d(u_t^\top w + \psi^2\Delta\lambda P^\top P) + (w^\top w + \psi^2\Delta\lambda^2 P^\top P - \Delta l^2) = a d^2 + b d + c$, which is zero at a root. For the second claim, $K_T u_r = -G$ and $K_T u_t = P$, so $G + K_T u_r + d\,K_T u_t - d P = G - G + dP - dP = 0$. $\square$

So every iterate, and hence every recorded increment, lies exactly on the sphere (or cylinder for $\psi = 0$) of radius $\Delta l$ around the last converged point. The reference test `test_arc_length_constraint_holds_for_each_step` checks this to $10^{-12}$.

**Lemma 4 (the bordered matrix).** Let $(u, \lambda)$ be a regular point of the path with tangent $t = (\dot u, \dot\lambda)$, and let $r = (r_u, r_\lambda) \in \mathbb R^{n+1}$. The matrix

$$J = \begin{pmatrix} K_T & -P \\ r_u^\top & r_\lambda \end{pmatrix}$$

is nonsingular exactly when $r^\top t = r_u^\top \dot u + r_\lambda \dot\lambda \ne 0$.

*Proof.* Since $[K_T, -P]$ has rank $n$, its null space is spanned by $t$. If $J z = 0$ for $z \in \mathbb R^{n+1}$, then $[K_T, -P] z = 0$, so $z = \mu t$, and the last row gives $\mu\,r^\top t = 0$. If $r^\top t \ne 0$, then $\mu = 0$ and $z = 0$, so $J$ is nonsingular. If $r^\top t = 0$, then $J t = 0$ and $J$ is singular. $\square$

**Corollary 5 (limit points).** Let $(u^*, \lambda^*)$ be a point where $K_T$ has a one-dimensional null space spanned by $\phi$ and $\phi^\top P \ne 0$ (here $K_T$ is symmetric, as for a conservative internal force). Then the point is regular, its tangent is $(\phi, 0)$, and the bordered matrix of the Riks iteration, with $r = (\Delta u_0, \psi^2 \Delta\lambda_0 P^\top P)$ from the predictor, is nonsingular as long as $\Delta u_0^\top \phi \ne 0$.

*Proof.* The range of $K_T$ is the orthogonal complement of $\phi$, and $P$ is not in it because $\phi^\top P \ne 0$. So the columns of $[K_T, -P]$ span $\mathbb R^n$, and the point is regular. $K_T \phi = 0$ gives $[K_T, -P](\phi, 0) = 0$, so the tangent is $(\phi, 0)$: at a limit point the load is stationary. Lemma 4 with $r^\top t = \Delta u_0^\top \phi$ gives the last claim. $\square$

The Riks iteration solves $G = 0$ together with the linear constraint $\Delta u_0^\top(\Delta u - \Delta u_0) + \psi^2\Delta\lambda_0 (\Delta\lambda - \Delta\lambda_0) P^\top P = 0$ by Newton's method, and the Jacobian of this system of $n + 1$ equations is $J$ with $r = (\Delta u_0, \psi^2\Delta\lambda_0 P^\top P)$. When the predictor is close enough to the path, $r$ is close to a multiple of $t$, so $r^\top t \ne 0$. By Lemma 4, $J$ is nonsingular near the solution, and the standard local theorem for [Newton's method for systems](/newton-method-for-systems/) (for example the [Kantorovich theorem](/kantorovich-theorem/)) gives local quadratic convergence, at limit points as well as at ordinary points. Load control is the case $r = (0, 1)$, and $r^\top t = \dot\lambda = 0$ at a limit point. So by Lemma 4 its bordered matrix is singular there, which is why load control fails.

**Bifurcation points.** If $\phi^\top P = 0$, then $[K_T, -P]$ has rank $n - 1$ at the point, the point is not regular, and $J$ is singular for every $r$. Lemma 4 does not apply, and the method gives no guarantee about which branch it follows.

**Remark 6 (Crisfield's quadratic form, sketch).** Crisfield's iteration replaces the linear constraint by the exact sphere and picks the root $d$ that keeps the direction of the increment. Near a regular point on the path the two roots are well separated: one is close to the Newton correction of the Riks form, the other moves the increment to the opposite side of the sphere, where its inner product with the old increment is negative. With the rule of line L8, each iteration differs from a Newton step on the bordered system by a term of second order in the correction, so local convergence follows as for Newton's method. Crisfield (1981) gives the method and its use on snap-through problems. We do not give a full proof here.

**Lemma 7 (the limit point of the two-bar truss).** For $f_{\rm int}(w) = 2\,EA\,y\,(1/l - 1/l_0)$ with $y = H - w$, $l = \sqrt{L^2 + y^2}$ and $l_0 = \sqrt{L^2 + H^2}$, the load has a stationary point at $l^3 = L^2 l_0$ with $0 < y < H$.

*Proof.* With $dl/dy = y/l$, $\tfrac{d}{dy}\big(y/l\big) = 1/l - y^2/l^3 = L^2/l^3$, so $\tfrac{d f_{\rm int}}{dy} = 2\,EA\,(L^2/l^3 - 1/l_0)$. This is zero at $l^3 = L^2 l_0$. At $y = H$ it is $2EA(L^2/l_0^3 - 1/l_0) = -2EA\,H^2/l_0^3 < 0$, and at $y = 0$ it is $2EA(1/L - 1/l_0) > 0$. It is monotone in $l$, hence in $y \ge 0$, so there is exactly one zero in $(0, H)$. Since $dw = -dy$, the load rises with $w$ from $w = 0$ to this point and falls after it. $\square$

For $EA = L = 1$ and $H = \tfrac12$ this gives $w = 0.22212$ and the limit load $0.038384$, which the reference test `test_limit_load_against_closed_form` compares with the arc-length path.
