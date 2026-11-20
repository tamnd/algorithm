---
tag: J6DH87
kind: theorem
slug: rankine-hugoniot-conditions
name: Rankine-Hugoniot conditions
aliases:
- jump conditions
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: A discontinuity in a weak solution moves with speed s such that s times the jump in u equals the jump in the flux f(u).
prereqs: [weak-solution-of-conservation-law]
see_also: [lax-entropy-condition, hyperbolic-conservation-law, riemann-problem, exact-riemann-solver, euler-equations-of-gas-dynamics, shallow-water-equations, burgers-equation, roe-solver]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 11.8 (the shock speed), Section 11.9 (the Rankine-Hugoniot conditions for systems), Section 11.11 (weak solutions), Section 13.7 (Hugoniot loci for shallow water), Section 14.8 onwards (the Riemann problem for the Euler equations)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Section 2.4 (conservation laws; 2.4.1 integral forms, 2.4.2 shock formation), Section 3.1.3 (elementary waves of the Euler equations)
  - paper: doi:10.1098/rstl.1870.0015
    title: W. J. M. Rankine, On the thermodynamic theory of waves of finite longitudinal disturbance, Philosophical Transactions of the Royal Society of London 160 (1870) 277-288
    locator: the conditions of mass, momentum and energy across a wave of permanent form
  - paper: "H. Hugoniot, Mémoire sur la propagation du mouvement dans les corps et spécialement dans les gaz parfaits, Journal de l'École Polytechnique 57 (1887) and 58 (1889)"
    locator: the energy condition across a shock in a perfect gas
---

The Rankine-Hugoniot conditions are the theorem that fixes the speed of a jump in a [weak solution](/weak-solution-of-conservation-law/) of a [conservation law](/hyperbolic-conservation-law/) $U_t + F(U)_x = 0$. If the solution jumps from $U_L$ to $U_R$ along a curve with speed $s$, then $s(U_R - U_L) = F(U_R) - F(U_L)$. The conditions follow from the integral form of the law, and they hold for every weak solution, physical or not. They do not select the physical jump: an expansion shock satisfies them too. The [Lax entropy condition](/lax-entropy-condition/) is the extra condition that makes that choice. The definition of a weak solution is the setting, this theorem is what the definition says at a jump, and the [Lax-Wendroff theorem](/lax-wendroff-theorem/) is the reason that conservative schemes put their shocks at the speed given here.

## Statement

**Setting.** Let $F : \Omega \to \mathbb{R}^m$ be continuous on an open set of states $\Omega \subseteq \mathbb{R}^m$. Let $x = \xi(t)$ be a $C^1$ curve in an open set $D$ of the $(x, t)$ plane, with speed $s(t) = \xi'(t)$. Let $U$ be bounded on $D$, of class $C^1$ on each side of the curve, with limits $U_L(t)$ from the left and $U_R(t)$ from the right at each point of the curve, and let $U$ satisfy $U_t + F(U)_x = 0$ pointwise on each side.

**Theorem.** $U$ is a weak solution of $U_t + F(U)_x = 0$ in $D$ if and only if, at every point of the curve,

$$s\,(U_R - U_L) = F(U_R) - F(U_L).$$

For a system this is $m$ scalar equations with one speed $s$. For a scalar law with $u_L \ne u_R$ it gives

$$s = \frac{f(u_R) - f(u_L)}{u_R - u_L}.$$

The theorem is in LeVeque (2002), Section 11.8 for scalar laws and Section 11.9 for systems, and in Toro (2009), Section 2.4.

## In plain words

Look at a short piece of road that a shock crosses. Whatever is conserved, for example mass, can enter or leave the piece only through its two ends. While the shock moves across the piece, the part behind the shock grows and the part in front shrinks. The change of the total inside must be equal to what flows in at one end less what flows out at the other end. If you write this balance, you get one equation that connects the speed of the shock, the jump in the amount, and the jump in the flow. So a jump cannot move at any speed it likes. Its speed is fixed by the two states on its sides.

## Proof

**From the integral form, for a straight shock.** Take a constant speed $s$ and a short time $\Delta t$. Take the box $[x_1, x_2] \times [t_1, t_1 + \Delta t]$ with $x_1 = st_1 - M$ and $x_2 = st_1 + M$, where $M > |s|\Delta t$, so the shock stays inside the box. Assume that $U$ is constant on each side, $U = U_L$ to the left and $U = U_R$ to the right. The integral form

$$\int_{x_1}^{x_2}U(x, t_1 + \Delta t)\,dx - \int_{x_1}^{x_2}U(x, t_1)\,dx = \int_{t_1}^{t_1 + \Delta t}\big(F(U(x_1, t)) - F(U(x_2, t))\big)\,dt$$

has on the left side $s\Delta t\,U_L - s\Delta t\,U_R$, because the shock moves a distance $s\Delta t$ and the part of length $s\Delta t$ changes from $U_R$ to $U_L$. The right side is $\Delta t\,(F(U_L) - F(U_R))$. Divide by $\Delta t$ and change the sign: $s(U_R - U_L) = F(U_R) - F(U_L)$. For a curved shock and smooth states on each side, do the same in a box of size $\Delta x \times \Delta t$ around a point of the curve, and let both sizes go to zero. The variation of $U$ inside the box gives only terms of higher order (LeVeque 2002, Section 11.8).

**From the weak form, both directions.** Let $\varphi$ be a $C^1$ test function with compact support in $D$. Split $D$ into the parts $D_L$ and $D_R$ to the left and to the right of the curve. On $D_L$, $U$ is $C^1$ and satisfies the equation, so the divergence theorem gives

$$\iint_{D_L}\big(U\varphi_t + F(U)\varphi_x\big)\,dx\,dt = \int\big(F(U_L) - sU_L\big)\varphi(\xi(t), t)\,dt,$$

since the outward normal of $D_L$ on the curve is proportional to $(1, -s)$ in the $(x, t)$ coordinates. On $D_R$ the normal has the opposite sign, and the boundary term is $-\int(F(U_R) - sU_R)\varphi\,dt$. Add the two parts:

$$\iint_D\big(U\varphi_t + F(U)\varphi_x\big)\,dx\,dt = \int\Big(s(U_R - U_L) - \big(F(U_R) - F(U_L)\big)\Big)\varphi(\xi(t), t)\,dt.$$

$U$ is a weak solution exactly when the left side is zero for every $\varphi$. The values of $\varphi$ on the curve can be any $C^1$ function with compact support, so this holds exactly when the bracket is zero at every point of the curve. $\square$

## Consequences

- **The Burgers shock.** For $f(u) = u^2/2$ the theorem gives $s = (u_L + u_R)/2$. With $u_L = 1$ and $u_R = 0$: $s = \frac12$. Check: $s(u_R - u_L) = -\frac12$ and $f(u_R) - f(u_L) = -\frac12$. See [Burgers' equation](/burgers-equation/).
- **The Euler shock of the Sod problem.** Take the [Euler equations](/euler-equations-of-gas-dynamics/) with $\gamma = 1.4$ and the Sod data. The right shock moves into $(\rho, u, p) = (0.125, 0, 0.1)$ with speed $s = 1.75216$, and behind it the state is $(\rho, u, p) = (0.26557, 0.92745, 0.30313)$. These are the values of the [exact Riemann solver](/exact-riemann-solver/). The three conditions check as follows. Mass: $s(\rho_* - \rho_R) = 0.24631$ and $\rho_*u_* = 0.24631$. Momentum: $s\,\rho_*u_* = 0.43157$ and $(\rho_*u_*^2 + p_*) - p_R = 0.43157$. Energy: with $E = p/(\gamma - 1) + \rho u^2/2$, $s(E_* - E_R) = 1.08992$ and $u_*(E_* + p_*) = 1.08992$. This is a measurement with the reference code of the exact Riemann solver page, to five digits.
- **Hugoniot locus.** For a system and a given $U_L$, the set of $U_R$ that satisfy the conditions for some $s$ is the Hugoniot locus of $U_L$. Near $U_L$ it is made of $m$ curves, one for each characteristic field, and the curve of field $p$ is tangent to the eigenvector $r_p(U_L)$ (LeVeque 2002, Section 11.9; Section 13.7 for shallow water). Exact Riemann solvers follow these curves.
- **Shallow water.** For $U = (h, hu)$ the two conditions give, after the speed is eliminated, $u_R - u_L = \pm(h_R - h_L)\sqrt{g(h_L + h_R)/(2h_Lh_R)}$. This is the shock branch of the wave function of the [shallow water equations](/shallow-water-equations/).
- **Contact discontinuities.** In a linearly degenerate field, for example the middle field of the Euler equations, the jump moves with the characteristic speed $s = u$, and the pressure and the velocity are continuous across it.
- **Small jumps.** If $U_R \to U_L$ along the locus of field $p$, then $s \to \lambda_p(U_L)$. A weak shock moves at nearly the characteristic speed. For a scalar law, $s$ is exactly the mean of $f'$ over $[u_L, u_R]$.
- **Conservative schemes.** A scheme in conservation form puts its shocks at the speed of this theorem when it converges (see the [Lax-Wendroff theorem](/lax-wendroff-theorem/)). The [Roe solver](/roe-solver/) uses a matrix that satisfies the conditions exactly for every pair of states.

## Tightness

- **The conditions do not select the physical jump.** For Burgers' equation the jump from $u_L = 0$ to $u_R = 1$ at speed $s = \frac12$ satisfies them, but it is an expansion shock. The physical solution for the same data is a rarefaction. The [Lax entropy condition](/lax-entropy-condition/) is the extra condition that removes it.
- **The conditions depend on the conserved quantities.** For smooth solutions $u_t + uu_x = 0$ is also $(u^2/2)_t + (u^3/3)_x = 0$. For the jump from 1 to 0, the second law gives $s = \frac{1/3}{1/2} = \frac23$, not $\frac12$. The theorem applies only to the law in conservation form, with the quantities that are really conserved (LeVeque 2002, Section 11.12).
- **Non-conservative products.** For systems that cannot be written in conservation form, for example some multiphase models, there is no unique jump condition. The jump then depends on the path of the regularization.
- **Not every pair of states is joined by a jump.** For a system, $m$ equations with one unknown speed leave a set of curves, the Hugoniot locus. For most pairs $U_L$, $U_R$ there is no $s$ at all, and the [Riemann problem](/riemann-problem/) solution needs several waves.

## History

Rankine (1870) derived the conditions of mass, momentum and energy across a compressive wave of permanent form in a gas. Hugoniot (1887 and 1889) derived them independently and gave the energy relation that now carries his name, the Hugoniot curve of a gas. Stokes and Riemann had earlier studied discontinuous waves in gases, but without the energy condition. The general form for any system in conservation form, and the role of weak solutions, came with Lax (1957). The name Rankine-Hugoniot conditions is now used for the jump condition of any conservation law.

## References
