---
tag: NYXCZF
kind: algorithm
slug: corotational-fem
name: Corotational finite elements
aliases:
- corotated linear elasticity
- stiffness warping
area: graphics-and-signals/deformable-body-simulation
level: core
summary: Extract the rotation of each element by polar decomposition and apply linear elasticity in the rotated frame, which removes the ghost forces of linear FEM under rotation.
model: real-ram
complexity:
  vars: {n: "the number of nodes", m: "the number of elements", k: "the number of CG iterations per step"}
  time: {forces_per_step: "Θ(m)", implicit_step_with_cg: "O(m + k (n + m))"}
  space: {extra: "Θ(n + m)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 2002
  people: [Matthias Müller, Julie Dorsey, Leonard McMillan, Robert Jagnow, Barbara Cutler]
  note: Müller et al. warped the linear stiffness matrix by a rotation per vertex in 2002. Müller and Gross used one rotation per element in 2004.
prereqs: [deformation-gradient, hyperelastic-material, finite-element-method]
see_also: [invertible-finite-elements, st-venant-kirchhoff-model, stable-neo-hookean, finite-element-assembly, finite-element-locking, backward-euler-method, meshless-shape-matching, as-rigid-as-possible-deformation]
sources:
  - paper: doi:10.1145/545261.545269
    title: Matthias Müller, Julie Dorsey, Leonard McMillan, Robert Jagnow and Barbara Cutler, Stable real-time deformations, ACM SIGGRAPH/Eurographics Symposium on Computer Animation (SCA 2002), 49-54
    locator: the whole paper (stiffness warping with a rotation per vertex and an implicit step)
  - paper: "Matthias Müller and Markus Gross, Interactive virtual materials, Proceedings of Graphics Interface 2004, 239-246"
    locator: the corotational formulation with a rotation per element, plus plasticity and fracture (general locator)
  - paper: doi:10.1145/2343483.2343501
    title: Eftychios Sifakis and Jernej Barbič, FEM simulation of 3D deformable solids, a practitioner's guide to theory, discretization and model reduction, SIGGRAPH 2012 Courses, article 20
    locator: the corotated linear material and its stress (general locator)
---

Corotational finite elements simulate an elastic solid with the cheap linear stiffness matrix of each element, but measured in a frame that turns with the element.
For each element the method finds the rotation $R$ of the [deformation gradient](/deformation-gradient/) $F = R S$, turns the nodes back by $R^T$, applies the linear force there, and turns the force forward by $R$:

$$f_e = -R\, K_e\, (R^T x_e - X_e).$$

Plain linear elasticity sees a rotation as a strain and makes the body grow when it turns.
The corotational force is zero for every rigid motion, and it is the exact negative gradient of the corotated energy $\mu|F - R|_F^2 + \frac{\lambda}{2}\operatorname{tr}(R^T F - I)^2$.
The method is a standard way to simulate large rotations with small strains in games and interactive tools.

## In plain words

Linear elasticity is simple and fast, because the force is a fixed matrix times the displacement.
But it measures the displacement in a fixed frame.
When a body turns, its points move a long way, so linear elasticity sees a large strain and pushes the body out of shape.
The corotational method fixes this for each element.
It finds how much the element has turned.
It turns the element back, computes the linear force in the rest frame, and turns that force forward again.
The turning no longer counts as strain, so only the real change of shape makes a force.
The stiffness matrix of each element is computed once.
At each step the method only needs the rotations.

## The problem

The input is a mesh of linear elements: triangles in 2D or tetrahedra in 3D, with the rest positions $X$ of the $n$ nodes and the $m$ elements.
The material has the Lamé parameters $\mu$ and $\lambda$, from Young's modulus $E$ and Poisson's ratio $\nu$ by $\mu = E / (2(1 + \nu))$ and $\lambda = E\nu / ((1 + \nu)(1 - 2\nu))$.
These are the 3D formulas, and in 2D they give the plane strain values; this page uses them in both cases.
The state is the node positions $x$ and velocities $v$, and the lumped node masses $M$ come from the rest areas (see [mass lumping](/mass-lumping/)).

The output is the elastic force on every node and a time step.
The force must be zero for every rigid motion $x = QX + t$ with a rotation $Q$, so that a turning body keeps its shape.
For small strains it must agree with linear elasticity.

Each element has the edge matrix $D_m$ with the rest edge vectors as columns, and $D_s$ with the current ones, so $F = D_s D_m^{-1}$ and the rest area or volume is $V_0 = |\det D_m| / 2$ in 2D and $/ 6$ in 3D.
Its linear stiffness matrix $K_e$ gives the force $-K_e(x_e - X_e)$ of the energy $V_0(\mu|\varepsilon|_F^2 + \frac{\lambda}{2}(\operatorname{tr}\varepsilon)^2)$ with the small strain $\varepsilon = \frac12(F + F^T) - I$.
It is computed once, before the simulation.

## The algorithm

```pseudo id=main
COROTATIONAL-STEP(x, v, Δt, f_ext)               ▷ K_e, D_m^(-1), X_e precomputed per element
L1  f ← 0 on every node
L2  for each element e with nodes a_0, ..., a_d do
L3      D_s ← [x_(a_1) - x_(a_0), ..., x_(a_d) - x_(a_0)]
L4      F ← D_s D_m^(-1)
L5      R ← the rotation factor of the polar decomposition F = R S
L6      y_a ← R^T x_a for each node a of e        ▷ turn the element back
L7      g ← -K_e (y - X_e)                        ▷ the linear force in the rest frame
L8      f_a ← f_a + R g_a for each node a of e    ▷ turn the force forward
L9  K_w ← Σ_e R_e K_e R_e^T, assembled             ▷ the warped stiffness
L10 solve (M + Δt² K_w) v' = M v + Δt (f + f_ext)
L11 x' ← x + Δt v'
return x', v'
```

Lines L1 to L8 compute the forces.
Line L5 uses the polar decomposition with $\det R = +1$; in 2D it has the closed form $R = \operatorname{rot}(\theta)$ with $\theta = \operatorname{atan2}(F_{10} - F_{01}, F_{00} + F_{11})$.
Lines L6 to L8 apply the precomputed linear stiffness in the frame of the element.
Lines L9 to L11 are one linearized [backward Euler](/backward-euler-method/) step, as in Müller et al. (2002): the force at the end of the step is approximated by $f - \Delta t\, K_w v'$.
Fixed nodes get $v' = 0$ by replacing their rows of the system.
The explicit variant replaces lines L9 to L11 by a [symplectic Euler](/symplectic-euler-method/) step, $v' = v + \Delta t M^{-1}(f + f_{ext})$ and then $x' = x + \Delta t v'$.

## Example

Take one triangle with the rest nodes $(0, 0)$, $(1, 0)$ and $(0, 1)$ in m, $E = 1$ Pa and $\nu = 0.3$, so $\mu = 0.384615$ N/m and $\lambda = 0.576923$ N/m, and $V_0 = 0.5$ m².
Node 0 stays at the origin.

| State | $F$ | $R$ | Linear force on node 1 (N) | Corotational force on node 1 (N) |
|---|---|---|---|---|
| rest | $I$ | $I$ | $(0, 0)$ | $(0, 0)$ |
| turned by 90 degrees | $\operatorname{rot}(\pi/2)$ | $\operatorname{rot}(\pi/2)$ | $(0.961538, 0)$ | $(0, 0)$ |
| stretched by 1.2 along $x$, then turned by 90 degrees | $\operatorname{rot}(\pi/2)\operatorname{diag}(1.2, 1)$ | $\operatorname{rot}(\pi/2)$ | $(0.961538, -0.038462)$ | $(0, -0.134615)$ |

In the turned state, node 1 is at $(0, 1)$.
Linear elasticity sees the strain $\varepsilon = -I$ and pushes node 1 sideways with 0.96 N, so the triangle grows.
The corotational force is zero.
In the stretched state, node 1 is at $(0, 1.2)$, and the corotational force $(0, -0.134615)$ pulls it back toward node 0 along the stretched edge.
It is the linear force of the unturned stretch, $-V_0 P_{lin}(\operatorname{diag}(1.2, 1))$ in its first column, turned by 90 degrees.
The element energy is $V_0(\mu \cdot 0.04 + \frac{\lambda}{2} \cdot 0.04) = 0.013462$ J.

## Correctness

The statement: for $\det F > 0$, lines L2 to L8 return $f = -\nabla E_{cr}(x)$, the negative gradient of $E_{cr} = \sum_e V_0 \Psi_{cr}(F_e)$ with

$$\Psi_{cr}(F) = \mu|F - R|_F^2 + \tfrac{\lambda}{2}\operatorname{tr}(R^T F - I)^2, \qquad P_{cr} = \frac{\partial \Psi_{cr}}{\partial F} = 2\mu(F - R) + \lambda\operatorname{tr}(R^T F - I)\, R.$$

The key step: turning the element back gives the deformation gradient $R^T F = S$, which is symmetric, so the linear stress there is $2\mu(S - I) + \lambda\operatorname{tr}(S - I) I$, and turning it forward gives $P_{cr}$.
The derivative of $R$ drops out of $\partial\Psi_{cr}/\partial F$, because $\operatorname{tr}(dR^T F) = -\operatorname{tr}(WS) = 0$ for the skew matrix $W = R^T dR$.
So the force is exact, it is zero for rigid motions, and the net force and torque of each element are zero.

The stiffness $K_w$ of line L9 leaves out the derivative of $R$.
It equals the true Hessian of $E_{cr}$ at a turned rest shape, but not at a stretched and turned shape; in 2D the missing part of the stress change is $(\mu + \lambda)\operatorname{tr}(S - I)\, dR$.
So line L10 is an approximate Newton step, not the exact linearization of backward Euler.
The [proof](proofs/correctness.md) gives every step.

## Complexity

The force loop does a constant amount of work per element: one small polar decomposition (closed form in 2D, a few Newton iterations in 3D) and one product with a $3(d + 1)$ by $3(d + 1)$ matrix, at most 12 by 12.
So the forces cost $\Theta(m)$ per step.
Assembling $K_w$ costs $\Theta(m)$ and gives a sparse matrix with $O(n + m)$ nonzeros.
Solving line L10 with $k$ iterations of the [conjugate gradient method](/conjugate-gradient-method/) costs $O(k(n + m))$; the matrix $M + \Delta t^2 K_w$ is symmetric positive definite when $K_w$ is positive semidefinite, which holds because each $K_e$ is.
The value of $k$ for a given tolerance is a measurement, and it grows with the stiffness and the mesh size.
The test code uses a dense Gaussian elimination, $O(n^3)$, which is fine for its small meshes.
Memory is $\Theta(n + m)$: the precomputed $K_e$, $D_m^{-1}$ and $V_0$ per element, and the state per node.

## Properties

- **Rotation invariant.** $\Psi_{cr}(QF) = \Psi_{cr}(F)$ for every rotation $Q$, and the force is zero for every rigid motion. This is proved.
- **Exact force.** The force is the gradient of an energy, so with no damping and an energy conserving integrator the total energy is a conserved quantity of the semi-discrete system. This is proved.
- **Momentum.** The net force and the net torque of the internal forces are zero. Under symplectic Euler with no external force, the total momentum and angular momentum stay constant up to rounding. This is proved.
- **Linear for small strain.** Near the rest shape $\Psi_{cr}$ agrees with linear elasticity to second order.
- **Inexact stiffness.** $K_w$ omits the derivative of $R$, so the implicit step is not an exact Newton step. It is symmetric and positive semidefinite, which keeps the linear solve simple.
- **Not invertible.** At $\det F = 0$ the polar decomposition is not unique, and for $\det F < 0$ the rotation with $\det R = +1$ does not give a symmetric positive $S$. The element can stay inverted.
- **Model, not law.** The corotated energy is a constitutive model chosen for speed. It is not a law of physics, and for large strains it differs from the [St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/) and the [neo-Hookean model](/neo-hookean-model/).

## Variants and improvements

- **Per vertex rotations.** Müller et al. (2002) took a rotation per vertex from the rotation of the vertex neighbourhood and warped the global stiffness matrix with it. This is the original stiffness warping. Neighbouring vertices use different rotations, so in general the internal forces are not the gradient of one energy, and their sum and their torque need not be zero.
- **Per element rotations.** Müller and Gross (2004) used one rotation per element, which is the method of this page. They also added plasticity and a simple fracture rule from the principal stresses.
- **Exact Hessian.** The derivative of $R$ has a closed form, and adding it gives the true Hessian of $\Psi_{cr}$, as in Sifakis and Barbič (2012). The true Hessian can be indefinite, so it is usually projected to be positive definite before the solve.
- **Invertible elements.** The [invertible finite elements](/invertible-finite-elements/) of Irving, Teran and Fedkiw (2004) work in the diagonal frame of the [singular value decomposition](/singular-value-decomposition/) with $\det U = \det V = +1$. With the linear stress in that frame they extend the corotated model to inverted elements.
- **Shape matching and ARAP.** [Meshless shape matching](/meshless-shape-matching/) takes one rotation for a cluster of particles, and [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/) minimizes $\sum |F - R|_F^2$ over meshes. Both use the same idea of a best fit rotation.

## When to use it

Use corotational elements when the body turns a lot but each element stretches by a few percent, for example soft props, muscles under small strain and interactive tools.
It costs about as much as linear FEM, with one polar decomposition per element.
For large strains or strong compression, use a nonlinear model such as the [stable neo-Hookean model](/stable-neo-hookean/).
If elements can invert, use [invertible finite elements](/invertible-finite-elements/).
For a cheaper and less accurate model, use [position based dynamics](/position-based-dynamics/) or [projective dynamics](/projective-dynamics/).

## Pitfalls

- **Rotation from the wrong factor.** Line L5 must use the polar rotation. A QR factor of $F$ depends on the order of the edges, so the result changes with the node numbering of the element.
- **A reflection in place of a rotation.** The orthogonal polar factor of an inverted element has $\det = -1$. Line L5 must return $\det R = +1$; a reflection flips the element frame and gives wrong forces.
- **Rotating only the displacement.** The force is $-R K_e(R^T x - X)$. Writing $-R K_e R^T (x - X)$ in line L7 is not the same, because $R^T X \ne X$, and it brings back ghost forces under rotation.
- **Treating $K_w$ as exact.** The stiffness of line L9 is exact only at the rest shape. A Newton solver that relies on it can converge slowly at large strains; add a line search or the exact Hessian.
- **Stable is not accurate.** The implicit step is stable for large $\Delta t$, but it damps the motion: on a harmonic oscillator, backward Euler multiplies the energy by $1 / (1 + (\omega\Delta t)^2)$ per step. Large steps make the body look too soft and too damped.
- **Locking.** Linear triangles and tetrahedra are too stiff in bending on coarse meshes. A cantilever of 1 m by 0.25 m made of 8 triangles, with $E = 1000$ Pa, $\nu = 0.3$ and 1 kg/m² under gravity, settles at a tip deflection of 0.059 m, about a quarter of the 0.235 m of Euler-Bernoulli beam theory (a measurement on this toy). See [finite element locking](/finite-element-locking/).

## Implementations

## History

The idea of a frame that turns with each element comes from structural mechanics, where corotational formulations of beams and shells are old.
In computer graphics, Müller, Dorsey, McMillan, Jagnow and Cutler (2002) brought it in as stiffness warping, with a rotation per vertex, linear stiffness and an implicit step, for real time deformation.
Müller and Gross (2004) changed to a rotation per element and added plasticity and fracture.
Irving, Teran and Fedkiw (2004) extended the corotated model to inverted elements, and Sifakis and Barbič (2012) wrote it as the energy $\mu|F - R|_F^2 + \frac{\lambda}{2}\operatorname{tr}(R^T F - I)^2$ with its exact gradient.

## References
