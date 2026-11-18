---
tag: CSEPNJ
kind: technique
slug: modal-reduction
name: Modal deformable models
aliases:
- modal analysis for animation
- reduced deformable models
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: "Simulate a deformable body in a basis of its r lowest vibration modes. Each mode is an independent oscillator, so a step costs O(r), plus O(nr) when the full shape is rebuilt."
prereqs: [generalized-eigenvalue-problem, finite-element-method, st-venant-kirchhoff-model]
see_also: [rayleigh-ritz-method, model-order-reduction, jacobi-eigenvalue-algorithm, mass-lumping, finite-element-assembly, symplectic-euler-method, corotational-fem, principal-component-analysis]
sources:
  - paper: doi:10.1145/74334.74355
    title: Alex Pentland and John Williams, Good vibrations, modal dynamics for graphics and animation, SIGGRAPH 1989, Computer Graphics 23(3)
    locator: the use of a few vibration modes of a finite element model as the degrees of freedom of an animated object (general locator)
  - paper: doi:10.1145/1073204.1073300
    title: Jernej Barbič and Doug L. James, Real-time subspace integration for St. Venant-Kirchhoff deformable models, ACM Transactions on Graphics 24(3), 2005, 982 to 990
    locator: the basis of linear modes and modal derivatives, and the reduced internal forces that are cubic polynomials of the reduced coordinates (general locator)
  - paper: doi:10.1145/2343483.2343501
    title: Eftychios Sifakis and Jernej Barbič, FEM simulation of 3D deformable solids, a practitioner's guide to theory, discretization and model reduction, SIGGRAPH 2012 Courses
    locator: the part on model reduction (general locator)
---

A modal deformable model describes the shape of an elastic body by a few numbers, the amplitudes of its lowest vibration modes, instead of the positions of all mesh nodes.
For a mesh with $n$ degrees of freedom, the [finite element method](/finite-element-method/) gives the stiffness matrix $K$ at rest and the mass matrix $M$.
The modes are the solutions of the [generalized eigenvalue problem](/generalized-eigenvalue-problem/) $K\phi = \lambda M\phi$, scaled so that $\phi^TM\phi = 1$.
With the $r$ modes of smallest $\lambda$ as the columns of $U$, the shape is $u = Uq$, and the equation $M\ddot u = -Ku + f$ becomes $r$ oscillators $\ddot q_i = -\omega_i^2q_i + \phi_i^Tf$ with $\omega_i^2 = \lambda_i$, which do not interact.
Pentland and Williams (1989) used this for animation; Barbič and James (2005) extended the basis and the forces so that the reduced model has large deformations.

## In plain words

A plate or a beam vibrates in a few typical patterns. The slowest pattern is a long, soft bend. Faster patterns have more waves and are stiffer.

Most of the visible motion of an elastic body is made of the slowest patterns. So we compute these patterns once, before the animation. Then each frame only has to say how much of each pattern is present.

Each pattern moves like its own spring with its own weight, and it does not push the other patterns. So one frame is a few small updates, one per pattern, however fine the mesh is. To draw the body, we add up the patterns.

The price is that the patterns come from small motions near rest. They do not know that a large rotation should not stretch the body.

## When it applies

- **Small deformations near one rest shape.** The modes come from the linear system at rest, so the method is exact for that linear system and has errors when the material leaves the linear range.
- **Forces that are known or cheap to project.** The external force enters as $U^Tf$; a force at a few nodes costs $O(r)$ per node.
- **Many frames for one mesh.** The eigenproblem is solved once before the animation, which pays off when the same body moves for many steps.
- **Low modes carry the motion.** A load that excites mostly high modes, for example an impact at one node, needs many modes.

## The template

```pseudo id=template
MODAL-REDUCTION(mesh, fixed, r, f, h, steps)
L1  assemble the linear stiffness K at rest and the lumped mass M, and remove the fixed degrees of freedom
L2  solve the generalized eigenproblem K φ = λ M φ and scale each φ so that φᵀ M φ = 1
L3  keep the r modes with the smallest λ, as the columns of U, and set ω_i² = λ_i
L4  project the external force: g = Uᵀ f
L5  each step, advance each mode as its own oscillator: v_i ← v_i + h (g_i - ω_i² q_i), q_i ← q_i + h v_i
L6  rebuild the shape when it is needed: u = U q
```

The code uses [mass lumping](/mass-lumping/), so $M$ is diagonal, and it solves L2 with the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/) on $M^{-1/2}KM^{-1/2}$.
L5 is the [symplectic Euler method](/symplectic-euler-method/) on each mode.

**Diagonal form (proved).** With all $n$ modes, $U^TMU = I$ and $U^TKU = \operatorname{diag}(\omega^2)$, so $M^{-1} = UU^T$. See the [proof](proofs/correctness.md), Steps 2 and 3.

**Same steps as the full system (proved).** With all $n$ modes, the steps of L5 and L6 give the same shapes as symplectic Euler on $M\ddot u = -Ku + f$, from the initial values $q_0 = U^TMu_0$ and $v_0 = U^TM\dot u_0$. Proof, Step 4.

**Truncation keeps its modes (proved).** The modes do not interact, so with $r$ modes the code computes exactly the first $r$ modal coordinates of the full solution, and the error is the part of the full solution in the dropped modes. For a static load the error in the $M$-norm does not increase with $r$. Proof, Step 5.

**Cost (proved).** L1 to L3 run once; the code solves the dense eigenproblem in $O(n^3)$ per Jacobi sweep. A step of L5 costs $O(r)$, and L6 costs $O(nr)$ for each frame that is drawn.

## Classic examples

**A cantilever plate.** A $5 \times 3$ grid of nodes on $[0, 2] \times [0, 1]$, two triangles per cell, $E_Y = 1$, $\nu = 0.3$, density 1, and the left edge fixed, has 24 free degrees of freedom.
The code gives these lowest eigenvalues; the largest of all 24 is $\omega^2 = 44.959584$.

| mode | $\omega^2$ | $\omega$ |
|---|---|---|
| 1 | 0.082265 | 0.286818 |
| 2 | 0.696038 | 0.834289 |
| 3 | 0.858783 | 0.926705 |
| 4 | 3.051315 | 1.746801 |
| 5 | 4.596023 | 2.143834 |
| 6 | 5.163225 | 2.272273 |

For the weight $f = -0.01M$ in the $y$ direction, the static shape has the largest deflection 0.162985.
The relative error in the $M$-norm of the static shape with $r$ modes is a measurement on this mesh:

| $r$ | 1 | 2 | 3 | 6 | 12 | 24 |
|---|---|---|---|---|---|---|
| relative error | 0.056257 | 0.054433 | 0.006409 | 0.000545 | 0.000138 | 0 |

Mode 2 adds little because the load does not excite it much: $g_2 = 0.001346$, against $g_1 = -0.011176$ and $g_3 = 0.006316$.

**A free body.** The same grid with no fixed node has three eigenvalues 0, for the two translations and the linearized rotation $(-y, x)$ (proved, Step 6). The fourth is $\omega^2 = 1.355218$.

**A large rotation.** The rotation mode with amplitude $\theta$ has zero linear energy, but it is not a rotation: it multiplies the area by $1 + \theta^2$, and its [St. Venant-Kirchhoff](/st-venant-kirchhoff-model/) energy is $A(\mu + \lambda)\theta^4/2$ (proved, Step 7). For the free grid, $A = 2$, and $\theta = 0.5$ gives the area 2.5 and the energy 0.060096. This is the main error of linear modes for large motion.

## Variations

- **Modal derivatives.** Barbič and James (2005) add to the linear modes their derivatives, the second-order change of the static shape when two modes are present together. With a St. Venant-Kirchhoff material, the reduced internal force is a cubic polynomial in $q$, and they evaluate it in a cost that does not depend on $n$. This page states that result from the paper and does not check it.
- **Damping.** With Rayleigh damping $C = aM + bK$, $U^TCU$ is diagonal too, and mode $i$ gets the damping $a + b\omega_i^2$ (proved by the same argument as Step 3).
- **Rotation of the frame.** A reduced body can move with a rigid frame and use the modes only for the deformation relative to the frame. This removes the error of the large-rotation example for the rigid part of the motion (heuristic: the error comes back when the deformation itself rotates parts of the body).
- **Other bases.** A basis from [principal component analysis](/principal-component-analysis/) of example shapes, or from a [Rayleigh-Ritz](/rayleigh-ritz-method/) projection with other vectors, uses the same steps L4 to L6 with a reduced $K$ that is not diagonal. See also [model order reduction](/model-order-reduction/).
- **Iterative eigensolvers.** For a large mesh, only the $r$ lowest pairs are needed, and [Lanczos](/lanczos-algorithm/) or [subspace iteration](/subspace-iteration/) find them without a dense solve.

## Pitfalls

- **Zero modes.** A free body has rigid modes with $\omega = 0$. Integrate them as free motion, and do not divide by $\omega^2$ for a static solve.
- **Mass scaling.** The modes must be $M$-orthonormal, not orthonormal in the usual sense. With unit vectors, $U^TMU$ is not $I$ and the modes interact through the mass.
- **Initial values.** The modal coordinates of a full shape are $U^TMu$, not $U^Tu$. Only for $r = n$ is the shape rebuilt exactly.
- **Time step.** Symplectic Euler on one mode is stable only for $h\omega_i < 2$. Truncation removes the stiff high modes, so the reduced model can use a larger step than the full one. For the cantilever plate, the full model needs $h < 2/6.705$, while 6 modes allow $h < 2/2.272$.
- **Large rotations.** Linear modes stretch the body when it rotates. A rigid frame, modal derivatives or a [corotational](/corotational-fem/) step is needed for large motion.
- **Load shapes.** A load at one node excites high modes. A few low modes give a shape that is too smooth near the load.

## Exercises

1. Show that a square matrix $U$ with $U^TMU = I$ satisfies $M^{-1} = UU^T$.
2. With Rayleigh damping $C = aM + bK$, write the damped modal equation of mode $i$ and its critical damping.
3. Show that for a static load the $M$-norm error with $r$ modes is $\bigl(\sum_{i > r}(g_i/\omega_i^2)^2\bigr)^{1/2}$.
4. Show that symplectic Euler on $\ddot q = -\omega^2q$ is stable for $0 < h\omega < 2$ and unstable for $h\omega > 2$.
5. For the field $u = \theta(-y, x)$, compute the deformation gradient, its determinant and the Green strain, and find the St. Venant-Kirchhoff energy per unit area.
6. Two triangles share an edge. Show that if the linear energy of a displacement is zero, then the displacement is one rigid motion on both triangles.

## References
