---
tag: CV2R4Y
kind: algorithm
slug: meshless-shape-matching
name: Meshless shape matching
aliases:
- shape matching deformation
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Pull particles toward goal positions given by the best rigid or linear transform of the rest shape, found by polar decomposition each step.
model: real-ram
complexity:
  vars: {n: "the number of particles of a body"}
  time: {step: "Θ(n)", precompute: "Θ(n)"}
  space: {step: "Θ(n)"}
properties: {deterministic: true, exact: false, needs_mesh: false, linear_momentum_conserving: true, angular_momentum_conserving: true}
history:
  year: 2005
  people: [Matthias Müller, Bruno Heidelberger, Matthias Teschner, Markus Gross]
  note: Müller, Heidelberger, Teschner and Gross presented the method at SIGGRAPH 2005 as a fast, unconditionally stable deformation model for games that needs no mesh.
prereqs: [particle-system, kabsch-algorithm, symplectic-euler-method]
see_also: [position-based-dynamics, extended-position-based-dynamics, as-rigid-as-possible-deformation, corotational-fem, projective-dynamics, singular-value-decomposition, least-squares-problem, rigid-body-simulation-problem]
sources:
  - paper: doi:10.1145/1073204.1073216
    title: "Matthias Müller, Bruno Heidelberger, Matthias Teschner and Markus Gross, Meshless deformations based on shape matching, ACM Transactions on Graphics 24(3), 471-478, 2005 (SIGGRAPH 2005)"
    locator: "Section 3.3 (the optimal rotation, equations (5) to (8)), Section 3.4 (the integration, equations (9) to (11)), Section 4 (linear and quadratic deformations, clusters and plasticity)"
---

Meshless shape matching moves a soft body made of particles without a mesh and without elastic forces. In each step it finds the rotation and translation that best map the rest shape onto the current particles, in the mass weighted [least squares](/least-squares-problem/) sense, and pulls each particle a fraction $\alpha$ of the way toward its place in that rigid copy. Müller, Heidelberger, Teschner and Gross (2005) proposed it for games: a step costs $\Theta(n)$, the pull never overshoots the goal, and with a fixed goal the motion neither grows nor decays for any $\Delta t$. A linear or quadratic fit instead of the rotation gives softer bodies.

## In plain words

Keep a photo of the object in its rest shape. In each frame, lay the photo over the particles: slide it and turn it until it covers them as well as possible, with heavy particles counting more. The place of each particle on the photo is its goal. Then give each particle a push toward its goal, so that it would cover the fraction $\alpha$ of the gap in one frame, and let it move. A dent pops back out because the photo has no dent. With $\alpha = 1$ the body snaps back at once and acts rigid. With a small $\alpha$ it wobbles like jelly. If the photo may also stretch and shear, not only slide and turn, the body can keep some of its deformation.

## The problem

The input is one body with $n$ particles: masses $m_i$, rest positions $\mathbf x^0_i$, current positions $\mathbf x_i$ and velocities $\mathbf v_i$, external forces $\mathbf f_i$, a stiffness $\alpha \in [0, 1]$ and a step $\Delta t$. The output is the state after one step. The rest shape must not lie on a line, so that $S_0 = \sum m_i \mathbf q_i \mathbf q_i^T$ is invertible. There is no material law to solve: the method is a model of its own, chosen for speed and robustness. The page uses 2D, $y$ up and $\mathbf g = (0, -9.81)$ m/s²; the paper works in 3D, and the 2D code is a version of it.

## The algorithm

Let $\mathbf q_i = \mathbf x^0_i - \mathbf x^0_{cm}$ be the rest positions about the rest center of mass, computed once with $S_0^{-1}$.

```pseudo id=main
SHAPE-MATCH-STEP(x, v, m, q, S0⁻¹, α, Δt, mode, β)
L1  x_cm <- Σ m_i x_i / Σ m_i;  p_i <- x_i - x_cm
L2  A_pq <- Σ m_i p_i q_iᵀ                                   ▷ 2 by 2
L3  R <- rotation factor of the polar decomposition of A_pq
L4  G <- R, or in the linear mode G <- β A~ + (1 - β) R      ▷ A~ = A/√det A, A = A_pq S0⁻¹
L5  for each particle i: g_i <- G q_i + x_cm                ▷ goal
L6  for each particle i: v_i <- v_i + α (g_i - x_i)/Δt + Δt f_i/m_i
L7  for each particle i: x_i <- x_i + Δt v_i
```

**The best rotation (L1 to L3).** The rotation $R$ and translation $\mathbf t$ that minimize $\sum m_i |R\mathbf q_i + \mathbf t - \mathbf x_i|^2$ are $\mathbf t = \mathbf x_{cm}$ and the rotation that maximizes $\operatorname{tr}(R^T A_{pq})$. This is the weighted orthogonal Procrustes problem that the [Kabsch algorithm](/kabsch-algorithm/) solves, and its answer is the rotation factor of the polar decomposition $A_{pq} = RS$ (Section 3.3, equations (5) to (8)). The paper computes $S = (A_{pq}^T A_{pq})^{1/2}$ by a diagonalization and $R = A_{pq} S^{-1}$. In 2D there is a closed form, $R = R(\theta)$ with $\theta = \operatorname{atan2}(a_{10} - a_{01}, a_{00} + a_{11})$, which the code uses through the shared `polar` helper. It is always a rotation; the formula $A_{pq} S^{-1}$ is a reflection when $\det A_{pq} < 0$, for example after a body is pushed inside out. In 3D, a [singular value decomposition](/singular-value-decomposition/) gives the same rotation with a sign fix.

**Linear deformation (L4).** The best linear map is $A = A_{pq} S_0^{-1}$ (Section 4.2). Dividing by $\sqrt{\det A}$ in 2D, or by $\sqrt[3]{\det A}$ in 3D, keeps the area or the volume. The blend $\beta\tilde A + (1 - \beta)R$ lets the body keep a part of its stretch and shear. The code falls back to $R$ when $\det A \le 0$.

**Integration (L6, L7).** Equation (9) of the paper adds the pull $\alpha(\mathbf g_i - \mathbf x_i)/\Delta t$ to the velocity and then moves the particles with the new velocity, as in [symplectic Euler](/symplectic-euler-method/). The pull is a velocity, not a force, so it does not depend on the mass, and with $\alpha \le 1$ a particle at rest never passes its goal in one step.

## Example

**A stretched square by hand.** Four particles of mass 1 rest at $(\pm 1, \pm 1)$. Now they are at $(\pm 2, \pm 1)$, stretched along $x$, at rest. The center of mass is the origin, so $\mathbf p_i = (2a, b)$ for $\mathbf q_i = (a, b)$ with $a, b = \pm 1$, and $A_{pq} = \sum \mathbf p_i \mathbf q_i^T = \operatorname{diag}(8, 4)$. Then $\theta = \operatorname{atan2}(0, 12) = 0$ and $R = I$, so the goals are the rest positions. With $\alpha = 0.5$, $\Delta t = 0.1$ and no gravity, the corner at $(2, 1)$ gets the velocity $0.5 \cdot (1 - 2)/0.1 = -5$ along $x$ and moves to $(1.5, 1)$. In the linear mode, $S_0 = \operatorname{diag}(4, 4)$, so $A = \operatorname{diag}(2, 1)$, $\det A = 2$ and $\tilde A = \operatorname{diag}(\sqrt 2, 1/\sqrt 2)$. With $\beta = 1$ the goal of that corner is $(1.414, 0.707)$: the stretch is turned into an area preserving shape.

**The oscillation does not decay (measured).** The same square, started at $(\pm 2, \pm 1)$ with $\Delta t = 0.01$ in the rigid mode, oscillates about its rest shape. Over 3000 steps:

| $\alpha$ | period in steps (measured) | $2\pi / \arccos(1 - \alpha/2)$ | largest gap, steps 1 to 300 | largest gap, steps 2701 to 3000 |
|---|---|---|---|---|
| 0.05 | 28.04 | 28.04 | 1.0062 | 1.0056 |
| 0.2 | 13.93 | 13.93 | 1.0260 | 1.0260 |
| 0.5 | 8.69 | 8.69 | 1.0690 | 1.0690 |

The gap is the distance of the corner from its goal along $x$. The period in steps matches the eigenvalue angle of the fixed goal model (claim 6), and the size of the oscillation stays the same. The period does not depend on $\Delta t$ when it is counted in steps, so in seconds it is proportional to $\Delta t$: the stiffness that $\alpha$ gives changes with the step size.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Best rigid fit (proved).** The translation $\mathbf x_{cm}$ and the rotation of L3 minimize $\sum m_i |R\mathbf q_i + \mathbf t - \mathbf x_i|^2$ over all rotations. The test compares the rotation with a scan of 720 angles.
2. **Best linear fit (proved).** $A = A_{pq} S_0^{-1}$ is the least squares linear map, and it recovers $F$ exactly when $\mathbf x_i = F\mathbf x^0_i + \mathbf t$. The test checks $\tilde A = F/\sqrt{\det F}$ for random $F$.
3. **No pull at a rigid pose (proved).** If the particles are a rotated and moved copy of the rest shape, every goal equals its particle, in all modes.
4. **Momentum (proved).** With no external force, a step keeps the linear and the angular momentum exactly, in the rigid and the linear mode, because the pull sums to zero and has zero torque. The test checks both to $10^{-10}$ over 200 steps.
5. **Snap to the goals (proved).** With $\alpha = 1$ and zero velocity, one step puts every particle on its goal.
6. **Fixed goal model (proved).** For a particle with a fixed goal the step is the matrix of equation (11), whose eigenvalues have magnitude 1 for $0 < \alpha < 4$. This is the sense in which the paper calls the method unconditionally stable. It does not cover the real case, where the goals move with the particles; the table above measures that case for one body.
7. **Gravity (proved).** Under gravity the center of mass moves by symplectic Euler; the test checks the value $-5.3955$ m after 10 steps of $0.1$ s.

## Complexity

A step costs $\Theta(n)$ time: two sums over the particles (L1, L2), work on $2 \times 2$ or $3 \times 3$ matrices (L3, L4) and two maps over the particles (L5 to L7). The rest data $\mathbf q_i$ and $S_0^{-1}$ cost $\Theta(n)$ once. The memory is $\Theta(n)$. With overlapping clusters, each particle is in a bounded number of clusters and the cost is linear in the total cluster size.

## Properties

- **Robust.** The pull is toward a valid shape, so a body recovers from any deformation, even an inverted one, and a step cannot blow up with $\alpha \le 1$ in the fixed goal model.
- **No mesh.** Only the particles and their rest positions are needed; the connectivity does not matter.
- **Not a material model.** $\alpha$ is a tuning value, and the stiffness it gives depends on $\Delta t$ and on the size of the body. Measured periods depend only on $\alpha$ when counted in steps.
- **No damping of its own.** The oscillation keeps its size; damping must be added, for example by the rigid body damping of [PBD](/position-based-dynamics/).
- **Exact momentum.** Linear and angular momentum are kept exactly without external forces.
- **Global stiffness.** One cluster can only deform by a single rotation or linear map, so a long object cannot bend. Clusters fix this.

## Variants and improvements

- **Quadratic deformation.** Section 4.3 fits a $2 \times 5$ (in 3D $3 \times 9$) map on quadratic terms of $\mathbf q$, which allows bending and twisting of a single cluster.
- **Clusters.** Section 4.4 divides the particles into overlapping clusters, matches each one, and averages the goals of a particle over its clusters, so that the body can bend.
- **Plasticity.** Section 4.5 updates the rest shape from the linear part of the fit when the deformation is large, so the body keeps a dent.
- **Lattice shape matching.** Rivers and James (2007) matched many small regions of a regular lattice, with fast summation over the regions, for detailed soft bodies.
- **As a PBD constraint.** Shape matching is often projected as one constraint in a [PBD](/position-based-dynamics/) or [XPBD](/extended-position-based-dynamics/) solver, together with distance and collision constraints.
- **Related energies.** The same best rotation appears in the [as-rigid-as-possible](/as-rigid-as-possible-deformation/) energy, in [corotational FEM](/corotational-fem/) and in the local step of [projective dynamics](/projective-dynamics/).

## When to use it

Use shape matching for soft objects in games and interactive tools that must never fail and must cost little: jelly, rubber toys, soft props and objects made of many particles without a mesh. It is also a simple way to make a set of particles behave as a rigid body ($\alpha = 1$ with one cluster).

Do not use it when the material must have a physical stiffness or must behave the same at different step sizes; use [corotational FEM](/corotational-fem/) or [projective dynamics](/projective-dynamics/) then. One cluster cannot bend; use clusters or the quadratic mode for long objects.

## Pitfalls

- **Reflections.** The paper's formula $A_{pq}(A_{pq}^T A_{pq})^{-1/2}$ gives a reflection when $\det A_{pq} < 0$, which turns the body inside out. Use the best rotation, as the code does in 2D, or fix the sign of the SVD in 3D.
- **Degenerate rest shapes.** If the rest particles lie on a line (in 3D, a plane), $S_0$ is singular and the linear mode fails. The rotation can still be undefined when $A_{pq}$ is close to zero.
- **Volume normalization.** Without dividing by the root of $\det A$ the linear mode lets the body grow or shrink; with $\det A \le 0$ the root is not defined and the code falls back to $R$.
- **Step size changes the look.** Changing $\Delta t$ with the same $\alpha$ changes the period in seconds.
- **No damping.** Without added damping, a body that was hit keeps wobbling.

## Implementations

## History

Müller, Heidelberger, Teschner and Gross introduced meshless shape matching at SIGGRAPH 2005, with the rigid, linear and quadratic modes, clusters and plasticity. The best rotation of two point sets goes back to the orthogonal Procrustes problem and to Kabsch (1976). Rivers and James (2007) extended the idea to lattice shape matching, and later position based solvers took shape matching in as one more kind of constraint.

## References
