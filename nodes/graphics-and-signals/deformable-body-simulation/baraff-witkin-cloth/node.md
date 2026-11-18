---
tag: 7F3XVP
kind: algorithm
slug: baraff-witkin-cloth
name: Baraff-Witkin implicit cloth
aliases:
- large steps in cloth simulation
area: graphics-and-signals/deformable-body-simulation
level: core
summary: Simulate triangle cloth with one linearized implicit Euler step per time step, solved by a conjugate gradient method that filters constraints, with energies built from triangle conditions.
solves: [cloth-simulation]
model: real-ram
complexity:
  vars: {n: "the number of particles", t: "the number of triangles", e: "the number of interior edges", k: "the number of conjugate gradient iterations in a step"}
  time: {assembly: "Θ(n + t + e)", iteration: "Θ(n + t + e)", step: "Θ(k (n + t + e))"}
  space: {matrix: "Θ(n + t + e)"}
properties: {deterministic: true, exact: false, implicit: true, constraints_exact: true}
history:
  year: 1998
  people: [David Baraff, Andrew Witkin]
  note: Baraff and Witkin showed at SIGGRAPH 1998 that a linearized implicit Euler step with a filtered conjugate gradient solve lets cloth take steps near one frame long.
prereqs: [mass-spring-system, backward-euler-method, conjugate-gradient-method]
see_also: [fast-mass-spring, provot-strain-limiting, robust-cloth-collision, discrete-shells, quadratic-bending-model, st-venant-kirchhoff-model, projective-dynamics, optimization-time-integration]
sources:
  - paper: doi:10.1145/280814.280821
    title: "David Baraff and Andrew Witkin, Large steps in cloth simulation, Proceedings of SIGGRAPH 98, pages 43 to 54, 1998"
    locator: "Section 2.2 (masses), Section 3, equations (4) to (6) (the implicit step), Section 4, equations (7) to (12) (conditions, forces, Jacobians and damping), Section 5, equations (13) to (16) and the procedure modified-pcg (constraints), Section 6 (collisions), Section 7 (adaptive steps), Section 8 (timings)"
  - paper: doi:10.1145/1198555.1198573
    title: "Robert Bridson, Sebastian Marino and Ronald Fedkiw, Simulation of clothing with folds and wrinkles, ACM SIGGRAPH 2005 Courses (first published at the Symposium on Computer Animation 2003)"
    locator: "the gradient of the dihedral angle used by the bend condition of the code"
---

Baraff and Witkin (1998) made cloth simulation fast by taking large steps. Cloth resists stretch much more than it resists bending, so the equations of motion are stiff, and an explicit integrator needs many tiny steps per frame. Their simulator takes one step of [backward Euler](/backward-euler-method/), linearized at the start of the step, so each step is one sparse linear solve. The forces come from simple *conditions* on each triangle and edge: stretch, shear and bend. The linear system is solved by a [conjugate gradient method](/conjugate-gradient-method/) that also keeps particle constraints exactly, for example a particle that is pinned or that slides on a floor.

## In plain words

Cloth is easy to bend and very hard to stretch. If you simulate it by small pushes forward in time, the hard-to-stretch part forces you to take thousands of tiny steps every second, or the cloth explodes.

Baraff and Witkin instead ask, at each step: "what velocities at the end of the step are consistent with the forces at the end of the step?" They answer an approximate form of this question with one large but sparse system of equations, so the step can be as long as a frame of animation.

The forces come from three simple measurements on the cloth: how much each triangle is stretched, how much it is sheared, and how much two neighbouring triangles are folded. A particle that is held, or that rests on a surface, is handled inside the solver so that it stays exactly where it must.

## The problem

Given a triangle mesh with rest coordinates $(u, v)$ for each vertex, positions $\mathbf x_0$, velocities $\mathbf v_0$, masses $M$, external forces and a step $h$, find $\mathbf v_1$ and $\mathbf x_1$ of one backward Euler step,

$$\mathbf v_1 = \mathbf v_0 + h M^{-1} \mathbf f(\mathbf x_1, \mathbf v_1), \qquad \mathbf x_1 = \mathbf x_0 + h \mathbf v_1,$$

with some particles constrained: the change $\Delta \mathbf v_i = \mathbf v_1 - \mathbf v_0$ of particle $i$ has a given value $\mathbf z_i$ in zero, one, two or three directions. This is one way to solve [cloth simulation](/cloth-simulation/).

## The algorithm

**Masses (Section 2.2).** Each triangle gives one third of its mass to each of its vertices.

**Conditions and forces (Section 4).** A condition $C(\mathbf x)$, zero at rest, with stiffness $k$ has the energy $\frac k2 C^2$, the force $\mathbf f_i = -k\, C\, \partial C/\partial \mathbf x_i$ (equation (7)) and the Jacobian $K_{ij} = -k(\frac{\partial C}{\partial \mathbf x_i}\frac{\partial C}{\partial \mathbf x_j}^{\!\top} + \frac{\partial^2 C}{\partial \mathbf x_i \partial \mathbf x_j} C)$ (equation (8)). For a triangle, the map from $(u, v)$ to the world has the derivatives $(\mathbf w_u\ \mathbf w_v) = (\Delta \mathbf x_1\ \Delta \mathbf x_2)\begin{pmatrix} \Delta u_1 & \Delta u_2 \\ \Delta v_1 & \Delta v_2 \end{pmatrix}^{-1}$ (equation (9)), which are linear in the three vertex positions. With $a$ the rest area of the triangle:

- **stretch**, $C = a\,(|\mathbf w_u| - b_u,\ |\mathbf w_v| - b_v)$, two conditions, with $b_u = b_v = 1$ for no stretch at rest (equation (10));
- **shear**, $C = a\, \mathbf w_u \cdot \mathbf w_v$;
- **bend**, $C = \theta$, the angle between the normals of the two triangles at an interior edge.

**Damping (Section 4.5).** Each condition also has a damping force $\mathbf d_i = -k_d\, \dot C\, \partial C/\partial \mathbf x_i$ (equation (11)), with $\dot C$ the rate of change of $C$.

**The step (Sections 3 and 5).** Linearize the forces at the start of the step. Then backward Euler becomes one linear system $A\, \Delta \mathbf v = \mathbf b$ (equations (15) and (16)), which is solved by modified-pcg. The filter $S_i$ of a particle removes the constrained directions: $S_i = I$ for a free particle, $I - \mathbf p \mathbf p^\top$ for a particle that cannot move along $\mathbf p$, $I - \mathbf p \mathbf p^\top - \mathbf q \mathbf q^\top$ for two such directions, and $0$ for a pinned particle (equation (13)). $\text{filter}(\mathbf a)$ applies $S_i$ to each block $\mathbf a_i$. $Q$ is the diagonal matrix with the entries $1/A_{ii}$.

```pseudo id=main
BARAFF-WITKIN-STEP(x0, v0, h, {(S_i, z_i)})
L1  f, df/dx, df/dv <- sums over the stretch, shear and bend conditions, with damping
L2  A <- M - h df/dv - h^2 df/dx ;  b <- h (f + f_ext + h (df/dx) v0)
L3  dv <- z                                        ▷ constrained parts are right from the start
L4  delta0 <- filter(b)^T Q filter(b) ;  r <- filter(b - A dv)
L5  c <- filter(Q r) ;  delta_new <- r^T c
L6  while delta_new > eps^2 delta0:
L7      q <- filter(A c) ;  alpha <- delta_new / (c^T q)
L8      dv <- dv + alpha c ;  r <- r - alpha q
L9      s <- Q r ;  delta_old <- delta_new ;  delta_new <- r^T s
L10     c <- filter(s + (delta_new / delta_old) c)
L11 v1 <- v0 + dv ;  x1 <- x0 + h v1
```

Lines L3 to L10 are the procedure modified-pcg of Section 5.3. Without constraints it is the standard preconditioned conjugate gradient method. The filter keeps every search direction $\mathbf c$ in the free directions, so the constrained components of $\Delta \mathbf v$ stay equal to $\mathbf z$ at every iteration.

**Damping Jacobian (Section 4.5).** $\partial \mathbf d / \partial \mathbf x$ has a term $\frac{\partial C}{\partial \mathbf x_i} \frac{\partial \dot C}{\partial \mathbf x_j}^{\!\top}$ that is not symmetric. The paper drops it so that $A$ stays symmetric; the code does the same. The paper says that dropping all of equation (12) causes serious problems.

**Choices of this code.** The bend Jacobian keeps only $-k\,\frac{\partial \theta}{\partial \mathbf x_i}\frac{\partial \theta}{\partial \mathbf x_j}^{\!\top}$. That is exact where $\theta = 0$ and keeps the bend part of $A$ positive semidefinite. The bend force itself is exact, with the angle gradient of Bridson, Marino and Fedkiw. The paper writes $P_{ii} = 1/A_{ii}$ and then uses $P$ in $\delta_0$ but $P^{-1}$ in $P^{-1}\mathbf r$, which read literally puts the two in different norms. The code uses the one diagonal matrix $Q$ in all three places, which is the standard diagonal preconditioner. The code has no collisions, and the caller gives the constraints.

## Example

**A particle on a floor, by hand.** One particle of $1$ kg rests on a floor with the normal $\mathbf p = (0, 1, 0)$, so $S = I - \mathbf p \mathbf p^\top$ and $z = 0$. It feels gravity and a side force of $5$ N, and $h = 0.01$ s. With no elastic forces, $A = M = I$ and $\mathbf b = h \mathbf f = (0.05, -0.0981, 0)$. Line L4 gives $\mathbf r = \text{filter}(\mathbf b) = (0.05, 0, 0)$, line L5 gives $\mathbf c = (0.05, 0, 0)$ and $\delta_{\text{new}} = 0.0025$. One iteration gives $\alpha = 1$, $\Delta \mathbf v = (0.05, 0, 0)$ and $\mathbf r = 0$, so the loop stops. The particle slides sideways and does not sink. The residual $A\Delta \mathbf v - \mathbf b = (0, 0.0981, 0)$ is $h$ times the force that the floor must supply, $9.81$ N upward. Section 5.3 of the paper uses this residual to find contact forces.

**A stiff hanging sheet, measured.** A 5 by 5 sheet with spacing $0.1$ m (32 triangles, 40 interior edges), density $0.4$ kg/m², stretch stiffness $10^6$, shear stiffness $10^5$ and bend stiffness $10^{-4}$, no damping, hangs from two pinned corners with $h = 1/30$ s and $\varepsilon = 10^{-6}$. The solve has 69 unknowns.

| step | 1 | 2 | 5 | 10 | 20 |
|---|---|---|---|---|---|
| modified-pcg iterations | 42 | 43 | 39 | 42 | 43 |
| largest speed (m/s) | 0.009 | 4.2e-4 | 3.7e-6 | 4.6e-10 | 4.1e-15 |

The sheet comes to rest in about ten steps although there is no damping force: this is the numerical damping of backward Euler, so the step is stable, and stable is not accurate. Explicit Euler with the same forces and step gives the elastic energies $0.33$, $3.1$ and $1.4 \times 10^9$ J after steps 2, 3 and 4.

**Timings, measured by the authors.** Baraff and Witkin (Section 8) report $0.23$, $0.46$, $2.23$ and $10.3$ seconds per frame for cloths of 500, 899, 2,602 and 7,359 particles on an SGI Octane R10000 at 195 MHz, slightly better than $O(n^{1.5})$. They also report 50 to 100 iterations for a 6,000 node cloth (Section 1.1) and usually two to three steps per frame at 30 Hz.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Forces (proved).** Each condition force is minus the gradient of $\frac k2 C^2$, and $K$ is symmetric. The stretch and shear Jacobians of the code are exact; the bend Jacobian is exact where $\theta = 0$.
2. **Rest and rigid motion (proved).** All internal forces are zero at rest and after a rigid motion, and they sum to zero.
3. **modified-pcg (proved).** If $A$ is symmetric positive definite, modified-pcg is the standard preconditioned conjugate gradient method on the free directions. The constrained components equal $\mathbf z$ after any number of iterations, and in exact arithmetic it reaches the solution of equation (14) in at most as many iterations as free directions.
4. **Momentum (proved).** Without constraints, the change of linear momentum differs from $h \sum \mathbf f_{\text{ext}}$ by the sum of the residual blocks, so an exact solve keeps momentum exactly.
5. **Positive definiteness (model).** The paper calls $A$ positive definite. That is true near rest, but compressed or sheared triangles add terms of either sign, so it is an assumption, not a theorem.
6. **Large steps (measured).** The step is one Newton iteration of backward Euler. For nonlinear cloth this page claims no stability theorem; the bounded run above and in the tests is a measurement.

The tests check the bend gradient and the forces against central differences, zero force at rest and after a rotation, the stretch and shear Jacobians and their symmetry, the bend Jacobian at $\theta = 0$, both damping Jacobians, the dissipation of damping, modified-pcg against a dense solve with and without constraints, the constrained components after 0, 1, 2 and 5 iterations, the momentum to $10^{-10}$ relative, and the stiff sheet against explicit Euler.

## Complexity

Each condition touches 3 or 4 particles, so assembling the forces and $A$ costs $\Theta(n + t + e)$, and $A$ has $\Theta(n + t + e)$ nonzero $3 \times 3$ blocks. One iteration of modified-pcg is one product with $A$, a few vector operations and the filter, so it costs $\Theta(n + t + e)$. A step with $k$ iterations costs $\Theta(k (n + t + e))$. For a mesh, $t$ and $e$ are $\Theta(n)$. The number $k$ depends on the conditioning of $A$; Baraff and Witkin measured a total cost close to $O(n^{1.5})$ per frame, which they relate to the usual behaviour of the conjugate gradient method on such systems.

## Properties

- **Large steps.** In practice the step can be close to a frame long, because stiff stretch does not limit $h$ as it does for explicit methods (measured, not proved for the nonlinear case).
- **Exact constraints.** A pinned or sliding particle has its constrained velocity change exactly, whatever the number of iterations (proved).
- **Damped.** Backward Euler removes energy from fast motion, so large steps look calm. This is numerical damping, not a material property.
- **Not exact.** One linearized step is not the solution of the nonlinear backward Euler equations, and the conjugate gradient method stops at a tolerance.
- **Anisotropic material.** The stretch condition measures warp and weft separately through $b_u$ and $b_v$, so the cloth can be stiffer in one direction.

## Variants and improvements

- **Adaptive step size (Section 7).** The simulator rejects a step when the stretch changes too much and retries with a smaller step.
- **Collisions (Section 6).** Cloth-solid contact becomes a constraint in the filter, with $\mathbf z$ chosen to push the particle out. Cloth-cloth contact uses stiff damped springs.
- **Other energies.** Later work replaces the conditions by finite elements, such as [corotational FEM](/corotational-fem/) or the [St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/), and the bend condition by [discrete shells](/discrete-shells/) or the [quadratic bending model](/quadratic-bending-model/).
- **Full Newton.** Several Newton iterations with a line search solve the nonlinear step, as in [optimization time integration](/optimization-time-integration/).
- **Constant matrix.** [Fast mass-spring](/fast-mass-spring/) and [projective dynamics](/projective-dynamics/) change the splitting so that the matrix stays the same over all steps.
- **Robust collisions.** [Robust cloth collision](/robust-cloth-collision/) handles cloth-cloth contact after each step, without stiff springs in the solve.

## When to use it

Use it for cloth and other thin sheets where stretch is much stiffer than bending and steps of a frame or so are wanted: film and offline animation, and interactive tools with a few thousand particles.

Do not use it when you need accurate dynamics of fast motion with large steps, because backward Euler damps it. If the matrix can become indefinite, as under strong compression, use a Newton method with a definiteness fix. For real-time use with fixed topology, a constant-matrix method such as fast mass-spring can be cheaper.

## Pitfalls

- **Indefinite A.** Compression of stretch conditions and shear add terms of either sign to $A$. With a large step the conjugate gradient method can fail. A common fix is to drop or clamp these terms.
- **Stopping test.** $\delta_0$ comes from $\text{filter}(\mathbf b)$. If it is zero, the loop does not run, which is right only when the free part of $\mathbf b$ is zero.
- **Constraint values.** Each $\mathbf z_i$ must lie in the constrained directions, the range of $I - S_i$. A component in the free directions is changed by the iterations.
- **Dropping too much.** Dropping the whole damping Jacobian $\partial \mathbf d/\partial \mathbf x$ is not the same as dropping its asymmetric term; the paper reports serious problems with it.
- **Area scaling.** The stretch and shear conditions are multiplied by the rest area $a$, so the energy scales with $a^2$, and stiffness values do not carry over between meshes of different resolution.

## Implementations

## History

David Baraff and Andrew Witkin presented the method at SIGGRAPH 1998. Earlier cloth simulators, such as the particle model of Breen, House and Wozny and the spring model of Provot, used explicit steps, and the paper reports running times of several minutes per frame for garments of about a thousand nodes in earlier work. The combination of implicit steps, conditions on triangles and the filtered conjugate gradient method cut this to seconds per frame on the hardware of 1998. Bridson, Fedkiw and Anderson (2002) wrote that it "generated convincing results despite dropping nonsymmetric terms from their matrix".

## References
