---
tag: TFE3FX
kind: definition
slug: lax-entropy-condition
name: Lax entropy condition
aliases:
- entropy admissibility condition
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Picks the physical weak solution by requiring characteristics to run into each shock, which rules out expansion shocks.
prereqs: [rankine-hugoniot-conditions]
see_also: [weak-solution-of-conservation-law, hyperbolic-conservation-law, lax-wendroff-theorem, riemann-problem, harten-hyman-entropy-fix, entropy-stable-scheme, burgers-equation, roe-solver]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 11.13 (nonuniqueness, admissibility and entropy conditions), Section 11.14 (entropy functions), Section 12.11 (the entropy condition for numerical methods), Section 13.7 (Hugoniot loci and the entropy condition for shallow water), Section 16.1 (scalar laws with nonconvex fluxes)
  - paper: doi:10.1002/cpa.3160100406
    title: P. D. Lax, Hyperbolic systems of conservation laws II, Communications on Pure and Applied Mathematics 10 (1957) 537-566
    locator: the shock inequalities for genuinely nonlinear fields and the solution of the Riemann problem
  - paper: doi:10.1070/SM1970v010n02ABEH002156
    title: S. N. Kruzkov, First order quasilinear equations in several independent variables, Mathematics of the USSR-Sbornik 10(2) (1970) 217-243
    locator: the entropy inequalities and uniqueness of the entropy solution for scalar laws
---

The Lax entropy condition is the extra condition on a jump in a [weak solution](/weak-solution-of-conservation-law/) that selects the physical shocks. A jump of field $p$ from $U_L$ to $U_R$ with speed $s$ is admissible when $\lambda_p(U_L) > s > \lambda_p(U_R)$: the characteristics of that field run into the shock from both sides. Weak solutions are not unique, and the [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/) accept jumps of both kinds. The Lax condition removes the expansion shocks, in which the characteristics leave the jump. The four pages of this group differ as follows. The [hyperbolic conservation law](/hyperbolic-conservation-law/) is the equation, the weak solution is the meaning of a discontinuous solution, the Rankine-Hugoniot conditions fix the speed of a jump, and this page decides which jumps are allowed. The [Lax-Wendroff theorem](/lax-wendroff-theorem/) does not give this condition: a convergent conservative scheme can still converge to a weak solution that fails it.

## Definition

**Scalar laws.** Let $u_t + f(u)_x = 0$ with $f$ of class $C^1$. A discontinuity of a weak solution from $u_L$ to $u_R$ with Rankine-Hugoniot speed $s = (f(u_R) - f(u_L))/(u_R - u_L)$ satisfies the **Lax entropy condition** if

$$f'(u_L) > s > f'(u_R).$$

For a convex flux, $f'' > 0$, this is the same as $u_L > u_R$.

**Systems.** Let $U_t + F(U)_x = 0$ be strictly hyperbolic with eigenvalues $\lambda_1 < \dots < \lambda_m$ of $F'(U)$, and let field $p$ be genuinely nonlinear. A discontinuity from $U_L$ to $U_R$ in field $p$, with speed $s$ from the Rankine-Hugoniot conditions, satisfies the Lax entropy condition if

$$\lambda_p(U_L) > s > \lambda_p(U_R),$$

and also $\lambda_{p - 1}(U_L) < s < \lambda_{p + 1}(U_R)$. The second pair says that the other fields do not run into the shock. Counted together, $m + 1$ characteristics enter the shock and $m - 1$ leave it, which is the count that makes the jump determined by the data on its two sides (Lax 1957; LeVeque 2002, Section 11.13).

A piecewise smooth weak solution is **admissible** in the sense of Lax when every jump either satisfies this condition or is a contact discontinuity of a linearly degenerate field, where $\lambda_p(U_L) = s = \lambda_p(U_R)$.

## Examples and non-examples

- **A Burgers shock.** $f(u) = u^2/2$, $u_L = 1$, $u_R = 0$, so $s = \frac12$. Then $f'(u_L) = 1 > \frac12 > 0 = f'(u_R)$. Admissible. See [Burgers' equation](/burgers-equation/).
- **A Burgers expansion shock.** $u_L = 0$, $u_R = 1$, $s = \frac12$. The jump satisfies the Rankine-Hugoniot condition, but $f'(u_L) = 0 < \frac12$. Not admissible. The admissible solution for these data is the rarefaction $u = x/t$ for $0 \le x \le t$.
- **The shock of the Sod problem.** For the [Euler equations](/euler-equations-of-gas-dynamics/) with $\gamma = 1.4$, the right shock of the Sod problem is a 3-shock with $s = 1.75216$. Behind it, $(\rho, u, p) = (0.26557, 0.92745, 0.30313)$, so $\lambda_3 = u + c = 0.92745 + \sqrt{1.4 \cdot 0.30313/0.26557} = 2.19157$. In front of it, $\lambda_3 = 0 + \sqrt{1.4 \cdot 0.1/0.125} = 1.05830$. So $2.19157 > 1.75216 > 1.05830$, and also $\lambda_2 = u = 0.92745 < s$ behind the shock. Admissible. The values come from the [exact Riemann solver](/exact-riemann-solver/); this is a measurement to five digits.
- **A contact discontinuity.** In the middle field of the Euler equations, the density jumps and the velocity and pressure do not. The speed is $s = u$ on both sides. It is not a shock, and the Lax inequalities do not apply; it is admissible as a linearly degenerate jump.
- **A nonconvex flux, both tests fail.** $f(u) = u^3$, $u_L = 1$, $u_R = -1$, so $s = 1$ and $f'(u_L) = f'(u_R) = 3$. The jump is not admissible. The entropy solution is a shock from 1 to $-\frac12$ at speed $\frac34 = f'(-\frac12)$, then a fan $u = -\sqrt{x/(3t)}$ for $\frac34 \le x/t \le 3$.
- **A nonconvex flux where the Lax test is not enough.** For $f(u) = \sin u$, $u_L = -7.75$ and $u_R = 3.25$, the Lax inequalities hold ($0.10379 > 0.08058 > -0.99413$), but the Oleinik chord condition below fails at points between the two states. This is a numerical check with a grid of 2000 points between the states. For a flux with inflection points the Lax condition is only a necessary condition (LeVeque 2002, Section 16.1).

## Related definitions

- **Oleinik's chord condition.** A jump of a scalar law is admissible if, for every $u$ strictly between $u_L$ and $u_R$,
$$\frac{f(u) - f(u_L)}{u - u_L} \ge s \ge \frac{f(u) - f(u_R)}{u - u_R}.$$
Geometrically, the chord from $u_L$ to $u_R$ lies on the correct side of the graph of $f$. For a convex flux it is the same as the Lax condition. For a nonconvex flux it is the correct condition, and it gives the convex hull construction of the [Riemann problem](/riemann-problem/) (LeVeque 2002, Sections 11.13 and 16.1).
- **Entropy pair and entropy inequality.** A convex $\eta(u)$ with flux $\psi$, $\psi' = \eta'f'$. A weak solution is admissible if $\eta(u)_t + \psi(u)_x \le 0$ in the weak sense. At a jump this reads $s(\eta(u_R) - \eta(u_L)) \ge \psi(u_R) - \psi(u_L)$. For a scalar convex law, one strictly convex entropy is enough to rule out the expansion shocks. For the Euler equations, $\eta = -\rho S$ with the physical entropy $S$ gives the physical condition that entropy increases across a shock (LeVeque 2002, Section 11.14).
- **Kruzkov's entropy solution.** The entropy inequality for all $\eta(u) = |u - k|$, $k \in \mathbb{R}$. For a scalar law with $C^1$ flux and bounded data, there is exactly one such solution, and it agrees with the Oleinik condition at jumps (Kruzkov 1970). See [weak solution of a conservation law](/weak-solution-of-conservation-law/).
- **Liu's condition.** The extension of Oleinik's chord condition to systems whose fields are not genuinely nonlinear.
- **Vanishing viscosity.** The physical solution is the limit as $\epsilon \to 0$ of $u_t + f(u)_x = \epsilon u_{xx}$. All the conditions above are ways to state at a jump what this limit selects.
- **Entropy fix and entropy stable schemes.** A numerical scheme can converge to a solution that fails the Lax condition. The [Roe solver](/roe-solver/) without a fix keeps a stationary expansion shock. The [Harten-Hyman entropy fix](/harten-hyman-entropy-fix/) and [entropy stable schemes](/entropy-stable-scheme/) are the remedies.

## References
