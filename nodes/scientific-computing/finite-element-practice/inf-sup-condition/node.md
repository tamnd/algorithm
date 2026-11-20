---
tag: 6XK9XM
kind: theorem
slug: inf-sup-condition
name: "Babuska-Brezzi inf-sup condition"
aliases:
- LBB condition
- inf-sup condition
- Ladyzhenskaya-Babuska-Brezzi condition
area: scientific-computing/finite-element-practice
level: core
summary: A saddle point problem has one stable solution when a is coercive on the kernel of b and b has an inf-sup bound beta > 0. A discretization is stable when beta does not depend on h.
prereqs: [lax-milgram-theorem, sobolev-space, weak-formulation]
see_also: [mixed-finite-element-method, taylor-hood-element, raviart-thomas-element, finite-element-locking, lax-milgram-theorem, cea-lemma, schur-complement, navier-stokes-equations]
sources:
  - paper: doi:10.1007/BF02165003
    title: Ivo Babuška, Error-bounds for finite element method, Numerische Mathematik 16(4) (1971) 322-333
    locator: the inf-sup bound for a bilinear form on two different Hilbert spaces and the error bound of the Galerkin approximation with different trial and test spaces
  - paper: doi:10.1051/m2an/197408R201291
    title: Franco Brezzi, On the existence, uniqueness and approximation of saddle-point problems arising from Lagrangian multipliers, RAIRO Analyse Numérique 8(R2) (1974) 129-151
    locator: the existence and uniqueness theorem for saddle point problems and the error estimate of their approximation
  - book: isbn:9783642365188
    title: Daniele Boffi, Franco Brezzi and Michel Fortin, Mixed Finite Element Methods and Applications, Springer Series in Computational Mathematics 44, Springer, 2013
    locator: Chapter 3 (algebraic aspects of saddle point problems), Chapter 4 (saddle point problems in Hilbert spaces) and Chapter 5 (approximation of saddle point problems)
  - paper: doi:10.1051/m2an/1985190101111
    title: L. R. Scott and M. Vogelius, Norm estimates for a maximal right inverse of the divergence operator in spaces of piecewise polynomials, ESAIM Mathematical Modelling and Numerical Analysis 19(1) (1985) 111-143
    locator: the stability of continuous velocities of degree k with discontinuous pressures of degree k - 1 on meshes without singular vertices
---

## Statement

Let $V$ and $Q$ be real Hilbert spaces, and let $a : V \times V \to \mathbb{R}$ and $b : V \times Q \to \mathbb{R}$ be bounded bilinear forms with norms $\|a\|$ and $\|b\|$. For $f \in V'$ and $g \in Q'$ the saddle point problem is: find $(u, p) \in V \times Q$ with

$$a(u, v) + b(v, p) = f(v) \quad \text{for all } v \in V, \qquad b(u, q) = g(q) \quad \text{for all } q \in Q. \tag{P}$$

Let $Z = \{v \in V : b(v, q) = 0 \text{ for all } q \in Q\}$ be the kernel of $b$.

**Theorem (Brezzi 1974).** Assume

- (H1) there is $\alpha > 0$ with $a(z, z) \ge \alpha\|z\|_V^2$ for all $z \in Z$, and
- (H2) there is $\beta > 0$ with $\displaystyle\inf_{q \in Q,\, q \ne 0}\ \sup_{v \in V,\, v \ne 0}\frac{b(v, q)}{\|v\|_V\|q\|_Q} \ge \beta$.

Then (P) has exactly one solution for every $f \in V'$ and $g \in Q'$, and

$$\|u\|_V \le \frac{\|f\|}{\alpha} + \Bigl(1 + \frac{\|a\|}{\alpha}\Bigr)\frac{\|g\|}{\beta}, \qquad \|p\|_Q \le \frac{\|f\| + \|a\|\,\|u\|_V}{\beta}.$$

**Discrete version.** Let $V_h \subset V$ and $Q_h \subset Q$ be finite-dimensional subspaces, let (P$_h$) be (P) with $V, Q$ replaced by $V_h, Q_h$, and let $Z_h = \{v_h \in V_h : b(v_h, q_h) = 0 \text{ for all } q_h \in Q_h\}$. In general $Z_h \not\subset Z$. If (H1) holds on $Z_h$ with a constant $\alpha_h > 0$ and (H2) holds with $\inf$ over $Q_h$ and $\sup$ over $V_h$ with a constant $\beta_h > 0$, then (P$_h$) has exactly one solution $(u_h, p_h)$, and

$$\|u - u_h\|_V + \|p - p_h\|_Q \le C\Bigl(\inf_{v_h \in V_h}\|u - v_h\|_V + \inf_{q_h \in Q_h}\|p - q_h\|_Q\Bigr),$$

where $C$ depends only on $\alpha_h$, $\beta_h$, $\|a\|$ and $\|b\|$, and $C$ grows when $\alpha_h$ or $\beta_h$ goes to $0$. For a family of meshes, the method is stable when $\alpha_h \ge \alpha_0 > 0$ and $\beta_h \ge \beta_0 > 0$ for every mesh of the family, with $\alpha_0$ and $\beta_0$ independent of $h$. The family must be stated: a pair of spaces can satisfy the uniform bound on one family of meshes and fail it on another.

## In plain words

Many problems have two unknowns that play different roles. In slow viscous flow they are the velocity and the pressure, and the pressure is there only to enforce a constraint on the velocity. The theorem says when such a problem has exactly one answer that depends continuously on the data. Two things are needed. The energy must control the velocity among the velocities that already meet the constraint. And every pressure must be visible to the velocities: for each pressure there must be a velocity that feels it with a strength that does not go to zero. When a computer uses a finite set of velocities and pressures, the same two things must hold with constants that do not get worse when the mesh gets finer. If they do get worse, the pressure can oscillate wildly or the velocity can lock.

## Proof

Identify $Q'$ with $Q$ and $V'$ with $V$ by the Riesz representation. Define $B : V \to Q$ by $(Bv, q)_Q = b(v, q)$ and its adjoint $B^* : Q \to V$ by $(B^*q, v)_V = b(v, q)$. Then $\sup_v b(v, q)/\|v\| = \|B^*q\|$, so (H2) says $\|B^*q\| \ge \beta\|q\|$ for all $q$, and $Z$ is the kernel of $B$.

*Step 1: the range of $B^*$ is closed and equals $Z^\perp$.* If $B^*q_n \to y$, then $\|q_n - q_k\| \le \|B^*q_n - B^*q_k\|/\beta$, so $(q_n)$ is a Cauchy sequence with a limit $q$, and $B^*q = y$ because $B^*$ is bounded. So $R = \operatorname{range}B^*$ is closed and $V = R \oplus R^\perp$. A vector $v$ is in $R^\perp$ exactly when $b(v, q) = (B^*q, v) = 0$ for all $q$, that is, when $v \in Z$. So $R^\perp = Z$ and $R = Z^\perp$.

*Step 2: a lifting of $g$.* The form $c(p, q) = (B^*p, B^*q)_V$ on $Q$ is bounded and symmetric, and $c(q, q) = \|B^*q\|^2 \ge \beta^2\|q\|^2$. By the [Lax-Milgram theorem](/lax-milgram-theorem/) there is $p_g \in Q$ with $c(p_g, q) = g(q)$ for all $q$. Then $u_g = B^*p_g \in Z^\perp$ satisfies $b(u_g, q) = (B^*q, B^*p_g) = g(q)$ for all $q$. From $\|u_g\|^2 = g(p_g) \le \|g\|\,\|p_g\| \le \|g\|\,\|u_g\|/\beta$ we get $\|u_g\| \le \|g\|/\beta$.

*Step 3: a pressure for a functional that vanishes on $Z$.* Let $\ell \in V'$ with $\ell(z) = 0$ for all $z \in Z$, and let $r \in V$ be its Riesz representative. Then $r \in Z^\perp = R$, so $r = B^*p$ for a $p \in Q$, which means $b(v, p) = \ell(v)$ for all $v$. This $p$ is unique because $B^*$ is injective, and $\|p\| \le \|B^*p\|/\beta = \|\ell\|/\beta$.

*Step 4: existence.* $Z$ is a closed subspace, so it is a Hilbert space. By (H1) and the Lax-Milgram theorem on $Z$ there is $z \in Z$ with $a(z, w) = f(w) - a(u_g, w)$ for all $w \in Z$, and $\|z\| \le (\|f\| + \|a\|\,\|u_g\|)/\alpha$. Let $u = u_g + z$. Then $b(u, q) = g(q)$ for all $q$, and $\ell(v) = f(v) - a(u, v)$ vanishes on $Z$. Step 3 gives $p$ with $b(v, p) = \ell(v)$ for all $v$, which is the first equation of (P). The bounds follow: $\|u\| \le \|u_g\| + \|z\| \le \|g\|/\beta + (\|f\| + \|a\|\,\|g\|/\beta)/\alpha$, and $\|p\| \le \|\ell\|/\beta \le (\|f\| + \|a\|\,\|u\|)/\beta$.

*Step 5: uniqueness.* Let $(u, p)$ solve (P) with $f = 0$ and $g = 0$. Then $u \in Z$. Take $v = u$ in the first equation: $a(u, u) + b(u, p) = a(u, u) = 0$, so $u = 0$ by (H1). Then $b(v, p) = 0$ for all $v$, so $B^*p = 0$ and $p = 0$ by (H2).

*Discrete version.* Steps 1 to 5 use only that $V$ and $Q$ are Hilbert spaces, so they apply to $V_h$, $Q_h$, $Z_h$, $\alpha_h$ and $\beta_h$ and give a unique $(u_h, p_h)$ with the same bounds. Since $V_h \subset V$ and $Q_h \subset Q$, subtracting (P$_h$) from (P) gives $a(u - u_h, w) + b(w, p - p_h) = 0$ for $w \in V_h$ and $b(u - u_h, r) = 0$ for $r \in Q_h$. Fix $v_h \in V_h$ and $q_h \in Q_h$. Then $(u_h - v_h, p_h - q_h)$ solves (P$_h$) with the data

$$\tilde f(w) = a(u - v_h, w) + b(w, p - q_h), \qquad \tilde g(r) = b(u - v_h, r),$$

whose norms on $V_h$ and $Q_h$ are at most $\|a\|\,\|u - v_h\| + \|b\|\,\|p - q_h\|$ and $\|b\|\,\|u - v_h\|$. The discrete bounds give $\|u_h - v_h\| + \|p_h - q_h\| \le C'(\|u - v_h\| + \|p - q_h\|)$ with $C'$ depending only on $\alpha_h$, $\beta_h$, $\|a\|$ and $\|b\|$. The triangle inequality and the infimum over $v_h$ and $q_h$ give the estimate with $C = 1 + C'$. $\blacksquare$

## Consequences

**A check by hand.** Take $-u'' = f$ written as a Stokes-like problem in 1D: $V_h$ the continuous piecewise linear functions on a uniform mesh of $(0, 1)$ with $v(0) = v(1) = 0$ and the norm $\|v'\|$, $Q_h$ the piecewise constants with mean $0$ and the $L^2$ norm, and $b(v, q) = -(v', q)$. For $q \in Q_h$, the function $v(x) = -\int_0^x q$ is in $V_h$, because $q$ has mean $0$, and $b(v, q) = \|q\|^2 = \|v'\|\,\|q\|$. With the Cauchy-Schwarz inequality this gives $\beta_h = 1$ on every mesh. Now replace $Q_h$ by the continuous piecewise linear functions and take the nodal values $q_i = (-1)^i$. On every cell the integral of $q$ is $h(q_i + q_{i+1})/2 = 0$, so $q$ has mean $0$, and since $v'$ is constant on each cell, $b(v, q) = 0$ for all $v \in V_h$. So $\beta_h = 0$: the alternating pressure is a spurious mode that the equations cannot see, the 1D form of the checkerboard mode of equal-order elements.

- **Stokes flow (theorem).** For the Stokes problem, $V = H^1_0(\Omega)^d$, $Q = L^2_0(\Omega)$, $a(u, v) = \nu(\nabla u, \nabla v)$ and $b(v, q) = -(\nabla\cdot v, q)$. Here $a$ is coercive on all of $V$, and (H2) holds on a bounded Lipschitz domain because the divergence maps $H^1_0(\Omega)^d$ onto $L^2_0(\Omega)$ with a bounded right inverse. The [Taylor-Hood element](/taylor-hood-element/) satisfies the discrete bound uniformly, and equal-order continuous pairs do not.
- **Mixed Poisson problem (theorem).** For $V = H(\mathrm{div})$, $Q = L^2$, $a(\sigma, \tau) = (\sigma, \tau)$ and $b(\tau, v) = (\nabla\cdot\tau, v)$, the form $a$ is coercive only on $Z$, where $\|\tau\|_{H(\mathrm{div})} = \|\tau\|$. This is why (H1) asks for coercivity on the kernel and not on $V$. The [Raviart-Thomas element](/raviart-thomas-element/) gives a uniformly stable pair.
- **Linear algebra (theorem).** In a basis, (P$_h$) is the system $\begin{pmatrix} A & B^{\mathsf T} \\ B & 0\end{pmatrix}$. It is nonsingular if $B$ has full row rank, which is $\beta_h > 0$, and $A$ is positive definite on the kernel of $B$, which is $\alpha_h > 0$. It is indefinite, so solvers use the [Schur complement](/schur-complement/) $BA^{-1}B^{\mathsf T}$ or [MINRES](/minres/). A necessary condition is $\dim Q_h \le \dim V_h$.
- **Fortin criterion (theorem).** If there is a linear map $\Pi_h : V \to V_h$ with $b(v - \Pi_h v, q_h) = 0$ for all $q_h \in Q_h$ and $\|\Pi_h v\| \le C_\Pi\|v\|$, then $\beta_h \ge \beta/C_\Pi$. The proof is one line: $\sup_{v_h} b(v_h, q_h)/\|v_h\| \ge \sup_v b(\Pi_h v, q_h)/\|\Pi_h v\| \ge \sup_v b(v, q_h)/(C_\Pi\|v\|) \ge \beta\|q_h\|/C_\Pi$. Most proofs of stability for concrete pairs build such a map.
- **Stabilized methods.** Methods such as pressure stabilized Petrov-Galerkin add terms to (P$_h$) that control the pressure directly, so that pairs with $\beta_h = 0$ can be used. The idea is the same as in [streamline upwind Petrov-Galerkin](/streamline-upwind-petrov-galerkin/).
- **A count of unknowns (heuristic).** Comparing $\dim V_h$ with $\dim Q_h$, or the number of velocity unknowns with the number of constraints per element, shows quickly when a pair must fail. It cannot prove that a pair is stable.

## Tightness

- **The bound on $u$ is attained.** Take $V = Q = \mathbb{R}$, $a = 0$, $b(v, q) = \beta vq$ and $f = 0$. Then $Z = \{0\}$, (H1) holds for every $\alpha$, the solution is $u = g/\beta$, and $\|u\| = \|g\|/\beta$.
- **(H2) is necessary.** Assume that (P) has a unique solution for all data and that $\|u\| \le C(\|f\| + \|g\|)$. For $q \in Q$ let $g = (q, \cdot)_Q$ and $f = 0$. The solution $u$ satisfies $\|q\|^2 = b(u, q) \le \|u\|\sup_v b(v, q)/\|v\| \le C\|q\|\sup_v b(v, q)/\|v\|$, so (H2) holds with $\beta = 1/C$. In finite dimensions $\beta_h = 0$ means that some $q_h \ne 0$ has $b(v_h, q_h) = 0$ for all $v_h$, and then $(u_h, p_h + q_h)$ is a second solution, as in the alternating mode above.
- **(H1) cannot be dropped.** Take $V = \mathbb{R}^2$, $Q = \mathbb{R}$, $b(v, q) = v_1q$ and $a = 0$. (H2) holds, $Z$ is the $v_2$ axis, and the second component of $u$ is not determined.
- **Uniformity depends on the mesh family (theorem).** Scott and Vogelius proved that continuous velocities of degree $k \ge 4$ with discontinuous pressures of degree $k - 1$ satisfy the uniform bound on 2D meshes without singular vertices, where a vertex is singular if its edges lie on only two straight lines. The center of each square in a criss-cross mesh is such a vertex, and there the pair has spurious pressure modes. A pair is stable or unstable on a stated family of meshes, not in general.

## History

Olga Ladyzhenskaya studied the inequality for the divergence that is (H2) for the Stokes problem in her work on viscous incompressible flow in the 1960s. Ivo Babuška gave in 1971 the general inf-sup bound for Galerkin methods with different trial and test spaces, and Franco Brezzi proved in 1974 the theorem for saddle point problems and their approximation in the form given here. For this reason the result is often given the three names together. Michel Fortin gave the criterion with a projection. The 2013 book by Boffi, Brezzi and Fortin is the standard reference.

## References
