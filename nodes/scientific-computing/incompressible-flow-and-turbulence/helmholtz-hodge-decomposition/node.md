---
tag: EVZZQK
kind: theorem
slug: helmholtz-hodge-decomposition
name: Helmholtz-Hodge decomposition
aliases:
- Helmholtz decomposition
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "On a bounded Lipschitz domain every L2 vector field splits orthogonally into a gradient and a divergence-free field with zero normal component. The basis of projection methods."
prereqs: [sobolev-space, poisson-equation]
see_also: [chorin-projection-method, marker-and-cell-method, stable-fluids, navier-stokes-equations, lax-milgram-theorem, weak-formulation, vorticity-streamfunction-formulation, mac-grid]
sources:
  - book: isbn:9783540157960
    title: Vivette Girault and Pierre-Arnaud Raviart, Finite Element Methods for Navier-Stokes Equations, Springer, 1986
    locator: Chapter I (the spaces H(div), the normal trace and the decomposition of vector fields)
  - book: isbn:9780387096193
    title: "Giovanni P. Galdi, An Introduction to the Mathematical Theory of the Navier-Stokes Equations: Steady-State Problems, second edition, Springer, 2011"
    locator: Chapter III (the Helmholtz-Weyl decomposition in L2 and Lq)
  - book: isbn:9780387979182
    title: Alexandre J. Chorin and Jerrold E. Marsden, A Mathematical Introduction to Fluid Mechanics, third edition, Springer, 1993
    locator: Chapter 1 (the Helmholtz-Hodge decomposition and the projection of the Euler equations)
  - paper: doi:10.1215/S0012-7094-40-00725-6
    title: Hermann Weyl, The method of orthogonal projection in potential theory, Duke Mathematical Journal 7(1) (1940) 411-444
    locator: orthogonal decomposition of square integrable vector fields
  - paper: doi:10.1515/crll.1858.55.25
    title: Hermann Helmholtz, Ueber Integrale der hydrodynamischen Gleichungen, welche den Wirbelbewegungen entsprechen, Journal fuer die reine und angewandte Mathematik 55 (1858) 25-55
    locator: the splitting of a velocity field into a potential part and a vortex part
  - paper: doi:10.1090/S0025-5718-1968-0242392-2
    title: Alexandre J. Chorin, Numerical solution of the Navier-Stokes equations, Mathematics of Computation 22(104) (1968) 745-762
    locator: the decomposition used as a numerical projection step
---

The Helmholtz-Hodge decomposition says that every square integrable vector field on a bounded domain is the sum of a gradient and a divergence-free field that does not flow through the boundary, and that these two parts are orthogonal. The divergence-free part is the orthogonal projection of the field onto the incompressible fields, and the gradient part comes from a Neumann problem for the [Poisson equation](/poisson-equation/). This is the step that every projection method for incompressible flow performs, from [Chorin's projection method](/chorin-projection-method/) to the pressure solve of [stable fluids](/stable-fluids/) in graphics. The graphics version uses the result on a grid without proof; the precise statement adds the function spaces and the boundary condition, and the boundary condition matters, because a different condition gives a different projection.

## Statement

Let $\Omega \subset \mathbb{R}^d$, $d \ge 2$, be a bounded connected open set with Lipschitz boundary and outward unit normal $\mathbf{n}$. Let $L^2(\Omega)^d$ be the square integrable vector fields with the inner product $(\mathbf{u}, \mathbf{w}) = \int_\Omega \mathbf{u}\cdot\mathbf{w}\,dx$, and $H^1(\Omega)$ the [Sobolev space](/sobolev-space/) of functions with square integrable first derivatives. Define

$$G(\Omega) = \{\nabla q : q \in H^1(\Omega)\}, \qquad H(\Omega) = \Big\{\mathbf{w} \in L^2(\Omega)^d : \int_\Omega \mathbf{w}\cdot\nabla\varphi\,dx = 0 \text{ for all } \varphi \in H^1(\Omega)\Big\}.$$

A field is in $H(\Omega)$ exactly when $\nabla\cdot\mathbf{w} = 0$ in the weak sense and its normal trace $\mathbf{w}\cdot\mathbf{n}$, defined in $H^{-1/2}(\partial\Omega)$ by Green's formula, is zero. For smooth fields this is $\nabla\cdot\mathbf{w} = 0$ in $\Omega$ and $\mathbf{w}\cdot\mathbf{n} = 0$ on $\partial\Omega$.

**Theorem.** $L^2(\Omega)^d = G(\Omega) \oplus H(\Omega)$, and the sum is orthogonal. So every $\mathbf{u} \in L^2(\Omega)^d$ is uniquely $\mathbf{u} = \nabla q + \mathbf{w}$ with $\mathbf{w} \in H(\Omega)$ and $q \in H^1(\Omega)$ unique up to an additive constant, and $\|\mathbf{u}\|^2 = \|\nabla q\|^2 + \|\mathbf{w}\|^2$. The potential $q$ is the weak solution of the Neumann problem

$$\int_\Omega \nabla q\cdot\nabla\varphi\,dx = \int_\Omega \mathbf{u}\cdot\nabla\varphi\,dx \quad \text{for all } \varphi \in H^1(\Omega),$$

that is $\Delta q = \nabla\cdot\mathbf{u}$ in $\Omega$ and $\partial q/\partial n = \mathbf{u}\cdot\mathbf{n}$ on $\partial\Omega$. The map $P\mathbf{u} = \mathbf{w}$ is the orthogonal projector onto $H(\Omega)$, called the Leray projector.

## In plain words

Think of the wind inside a closed room. Some of it moves like water poured from a jug: it spreads out from some places and gathers at others. The rest only swirls around and never piles up anywhere, and it never blows through the walls. The theorem says that every wind pattern is exactly one spreading part plus one swirling part, that there is only one way to split it, and that the two parts are independent of each other, so the energy of the whole is the energy of one part plus the energy of the other. The spreading part comes from a single height map: it always flows downhill on that map. To find the map, you solve one standard equation. A fluid that cannot be squeezed keeps only the swirling part, so a simulation can remove the spreading part at each step.

## Proof

**Step 1: $G(\Omega)$ is closed.** Let $\nabla q_k \to \mathbf{g}$ in $L^2(\Omega)^d$. Subtract the mean, so that $\int_\Omega q_k = 0$; this does not change $\nabla q_k$. On a bounded connected Lipschitz domain the Poincare-Wirtinger inequality $\|q - \bar q\|_{L^2} \le C_\Omega\|\nabla q\|_{L^2}$ holds; it follows from the compact embedding of $H^1(\Omega)$ in $L^2(\Omega)$ (Rellich). So $(q_k)$ is a Cauchy sequence in $H^1(\Omega)$, with a limit $q$, and $\nabla q = \mathbf{g}$. Hence $\mathbf{g} \in G(\Omega)$.

**Step 2: the orthogonal splitting.** $L^2(\Omega)^d$ is a Hilbert space and $G(\Omega)$ is a closed subspace, so by the projection theorem $L^2(\Omega)^d = G(\Omega) \oplus G(\Omega)^\perp$, with a unique splitting and Pythagoras' identity for the norms.

**Step 3: $G(\Omega)^\perp = H(\Omega)$.** A field $\mathbf{w}$ is orthogonal to $G(\Omega)$ exactly when $\int_\Omega \mathbf{w}\cdot\nabla\varphi = 0$ for every $\varphi \in H^1(\Omega)$, which is the definition of $H(\Omega)$. Testing with $\varphi \in C_c^\infty(\Omega)$ gives $\nabla\cdot\mathbf{w} = 0$ in the sense of distributions. Then $\mathbf{w}$ is in $H(\mathrm{div})$, Green's formula $\langle \mathbf{w}\cdot\mathbf{n}, \varphi\rangle_{\partial\Omega} = \int_\Omega \mathbf{w}\cdot\nabla\varphi + \int_\Omega (\nabla\cdot\mathbf{w})\varphi$ holds on Lipschitz domains (Girault and Raviart 1986, Chapter I), and with all $\varphi \in H^1(\Omega)$ it gives $\mathbf{w}\cdot\mathbf{n} = 0$ in $H^{-1/2}(\partial\Omega)$. The converse is the same formula read backward.

**Step 4: the potential.** $\mathbf{u} - \nabla q \in H(\Omega)$ means $\int_\Omega (\mathbf{u} - \nabla q)\cdot\nabla\varphi = 0$ for all $\varphi$, which is the Neumann problem of the statement. On the quotient space $H^1(\Omega)/\mathbb{R}$ the form $\int\nabla q\cdot\nabla\varphi$ is an inner product, and by Step 1 its norm is equivalent to the $H^1$ norm, so the [Lax-Milgram theorem](/lax-milgram-theorem/) (here the Riesz theorem is enough) gives exactly one solution class. $\square$

## Consequences

- **Pressure elimination.** Apply $P$ to the incompressible [Navier-Stokes equations](/navier-stokes-equations/) with $\mathbf{u}\cdot\mathbf{n} = 0$: $P\nabla p = 0$, so $\mathbf{u}_t = P\big(-(\mathbf{u}\cdot\nabla)\mathbf{u} + \nu\Delta\mathbf{u} + \mathbf{f}\big)$ on $H(\Omega)$. The pressure is the gradient part, $\nabla p = (I - P)(\dots)$, and it is found from a Neumann problem. Here $p$ is the pressure divided by the density.
- **Projection methods.** [Chorin's method](/chorin-projection-method/) applies a discrete $P$ once per time step. On the staggered [MAC grid](/mac-grid/), the discrete divergence $D$ and gradient $G$ satisfy $G^T = -D$, so the discrete projection $\mathbf{u} \mapsto \mathbf{u} - G(DG)^{-1}D\mathbf{u}$ is orthogonal too, and the theorem holds again on the grid. On a collocated grid with wide central differences the discrete gradient has a checkerboard null space, and the discrete version fails.
- **Energy.** Because $P$ is orthogonal, $\|P\mathbf{u}\| \le \|\mathbf{u}\|$: a projection never adds kinetic energy.
- **Two dimensions.** In 2D on a simply connected domain, every $\mathbf{w} \in H(\Omega)$ is $\nabla^\perp\psi = (\partial_y\psi, -\partial_x\psi)$ for a stream function $\psi \in H^1_0(\Omega)$. This is the basis of the [vorticity-streamfunction formulation](/vorticity-streamfunction-formulation/).

**Examples to check by hand.**

1. On the unit disk, $\mathbf{u} = (x - y,\ x + y)$ splits as $\nabla(\tfrac12 r^2) = (x, y)$ plus $\mathbf{w} = (-y, x)$. The field $\mathbf{w}$ has divergence $0$, and on the circle $\mathbf{w}\cdot\mathbf{n} = (-y, x)\cdot(x, y) = 0$. The parts are orthogonal: $\int (x, y)\cdot(-y, x) = \int (-xy + xy) = 0$.
2. On the unit square, $\mathbf{u} = (1, 0)$ is divergence free, but it flows through the walls $x = 0$ and $x = 1$, so it is not in $H(\Omega)$. Its decomposition is $\mathbf{u} = \nabla x + 0$: the projection removes it completely. A divergence-free field is in $H(\Omega)$ only if its normal component on the boundary is zero.
3. On the periodic square $[0, 2\pi]^2$, where there is no boundary, $\mathbf{u} = (\sin x + \sin y,\ 0)$ has divergence $\cos x$. It splits as $\nabla(-\cos x) = (\sin x, 0)$ plus $(\sin y, 0)$, which is divergence free, and $\int\!\!\int \sin x \sin y = 0$. The constant field $(1, 0)$ is now in the divergence-free part.

## Tightness

- **The boundary condition is part of the theorem.** With $q \in H^1_0(\Omega)$ instead of $H^1(\Omega)$, the same proof gives a second orthogonal splitting, $L^2(\Omega)^d = \{\nabla q : q \in H^1_0(\Omega)\} \oplus \{\mathbf{w} : \nabla\cdot\mathbf{w} = 0\}$, with no condition on $\mathbf{w}\cdot\mathbf{n}$. Example 2 shows that the two projections differ: the second one keeps $(1, 0)$. A projection method must use the splitting that matches the wall condition of the flow.
- **Connectedness.** On a domain with $m$ connected components, the potential is unique only up to one constant per component. The splitting itself is unchanged.
- **Holes.** On a domain that is not simply connected, $H(\Omega)$ contains fields that are both divergence free and curl free. On the annulus $1 < r < 2$, the field $(-y, x)/r^2$ is such a field, and it is not $\nabla^\perp\psi$ for a $\psi$ that vanishes on the whole boundary. The full Hodge decomposition separates these harmonic fields, whose dimension is given by the topology of $\Omega$. The two-part splitting of the theorem is still true; only the description of $H(\Omega)$ by stream functions changes.
- **Smoothness.** The theorem is an $L^2$ statement. Smooth data on a smooth boundary give a smooth $q$ and $\mathbf{w}$ by elliptic regularity, but on a domain with corners $q$ can have singular derivatives at the corners even for smooth $\mathbf{u}$. In $L^p$ with $p \ne 2$ the splitting is no longer orthogonal, and on Lipschitz domains it holds only for some $p$ near 2; Galdi (2011, Chapter III) treats the $L^q$ theory.
- **Unbounded domains.** On all of $\mathbb{R}^d$ the splitting holds in $L^2$, with $q$ in a homogeneous Sobolev space instead of $H^1$, because the Poincare-Wirtinger inequality of Step 1 fails.

## History

Helmholtz (1858) split a velocity field into a potential part and a vortex part in his paper on vortex motion. Weyl (1940) gave the orthogonal decomposition of square integrable vector fields in his method of orthogonal projection, and Hodge theory extended the decomposition to differential forms on manifolds. Leray used the projection onto divergence-free fields in his work on the Navier-Stokes equations in the 1930s, and Chorin (1968) turned it into a numerical method. Girault and Raviart (1986) and Galdi (2011) give the version for Lipschitz domains used here.

## References
