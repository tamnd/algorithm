---
tag: AX0ZM2
kind: algorithm
slug: material-point-method
name: Material point method
aliases:
- MPM
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: Carries mass, momentum and history on particles and solves the momentum equation on a background grid each step, for large deformations of solids.
model: real-ram
complexity:
  vars: {N: the number of material points, M: the number of grid nodes}
  time: {worst: "Θ(N + M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, conservative: true, order: "1"}
history:
  year: 1994
  people: [Deborah Sulsky, Zhen Chen, Howard L. Schreyer]
  note: Sulsky, Chen and Schreyer extended the FLIP particle-in-cell method of fluid dynamics to solids with history-dependent materials in 1994.
prereqs: [finite-element-method, cloud-in-cell-assignment]
see_also: [generalized-interpolation-material-point, particle-in-cell, fluid-implicit-particle, affine-particle-in-cell, smoothed-particle-hydrodynamics, deformation-gradient, hyperelastic-material, invertible-finite-elements]
sources:
  - paper: doi:10.1016/0045-7825(94)90112-0
    title: Deborah Sulsky, Zhen Chen and Howard L. Schreyer, A particle method for history-dependent materials, Computer Methods in Applied Mechanics and Engineering 118(1-2), 1994, 179-196
    locator: the method, the weak form on the grid and the update of stress at the material points
  - paper: doi:10.3970/cmes.2004.005.477
    title: Scott G. Bardenhagen and Edward M. Kober, The generalized interpolation material point method, Computer Modeling in Engineering and Sciences 5(6), 2004, 477-495
    locator: the cell crossing noise of MPM and its reduction with particle domains
  - paper: doi:10.1002/nme.2360
    title: Michael Steffen, Robert M. Kirby and Martin Berzins, Analysis and reduction of quadrature errors in the material point method (MPM), International Journal for Numerical Methods in Engineering 76(6), 2008, 922-948
    locator: the quadrature error of the particle integration and the error when points cross cell boundaries
---

The material point method (MPM) simulates solids, and also granular media and fluids, that move and deform a great deal. The material is a set of particles, the material points, that carry everything that belongs to the material: mass, velocity, the deformation gradient, stress, and history such as plastic strain. In each time step the particles send their mass and momentum to a fixed background grid, the momentum equation is solved on the grid as in the [finite element method](/finite-element-method/), and the grid velocity moves the particles and updates their strain; then the grid is thrown away. Because the grid never deforms, MPM handles very large strains, contact, fracture and flow without remeshing. In computer graphics the same method animates snow, sand and foam, usually with [APIC](/affine-particle-in-cell/) transfers and plasticity models chosen for the look; this page treats MPM as a method of solid mechanics, its accuracy and its cell crossing error.

## In plain words

Picture a block of rubber made of many small beads. Each bead remembers its own mass, speed and how much it is stretched. Beside the beads there is a fixed grid, like graph paper laid over the work.

In each step the beads tell the grid points near them how much mass and speed they bring. The grid points then work out how the stretch of the beads pushes and pulls on them, and how fast they will move next. The beads read the new speeds from the same grid points, move, and update how much they are stretched. The grid is wiped clean and the next step starts again. The grid makes the force calculation simple, and the beads keep the memory, so the material can twist, split or flow and the grid never gets tangled.

## The problem

The input is a body in the reference state, cut into $N$ material points with mass $m_p$, initial volume $V_p^0$, position $x_p$, velocity $v_p$, deformation gradient $F_p$ and stress $\sigma_p$; a stress update rule (here 1D linear elasticity, $\dot\sigma = E \dot\varepsilon$ with Young's modulus $E$); a grid of nodes $x_i = i \Delta x$ with shape functions $N_i$; the supports; and a step $h$. The goal is to approximate the solution of the momentum balance $\rho \dot v = \partial_x \sigma$ in the weak form, with the particles as the quadrature points:

$$\sum_p m_p N_i(x_p) \, \dot v(x_p) = -\sum_p V_p \, \sigma_p \, N_i'(x_p) + (\text{traction terms}), \qquad V_p = F_p V_p^0.$$

The code on this page uses the linear hats $N_i(x) = \max(0, 1 - |x - x_i| / \Delta x)$ in 1D, a lumped mass matrix, the explicit Euler step on the grid, and the update stress last (USL) order with the FLIP velocity update.

## The algorithm

```pseudo id=main
MPM-STEP(particles, grid, E, h)
L1  for each material point p do                   ▷ particles to grid
L2      m_i += N_i(x_p) m_p;  (mv)_i += N_i(x_p) m_p v_p   for the nodes i near x_p
L3  f_i ← -Σ_p V_p σ_p N_i′(x_p) for every node i   ▷ internal force
L4  v_i ← (mv)_i / m_i;  v_i^new ← v_i + h f_i / m_i   for every node with m_i > 0
L5  v_i^new ← 0 at fixed nodes;  a_i ← (v_i^new - v_i) / h
L6  for each material point p do                   ▷ grid to particles
L7      v_p ← v_p + h Σ_i N_i(x_p) a_i              ▷ FLIP update
L8      x_p ← x_p + h Σ_i N_i(x_p) v_i^new
L9      ε̇_p ← Σ_i N_i′(x_p) v_i^new                ▷ strain rate from the new grid velocity
L10     F_p ← (1 + h ε̇_p) F_p;  V_p ← F_p V_p^0
L11     σ_p ← σ_p + E h ε̇_p
L12 return the particles; clear the grid
```

Lines L1 and L2 are the particle to grid transfer, with the same weights as [cloud-in-cell assignment](/cloud-in-cell-assignment/). Line L3 is the internal force of the weak form, computed with the particles as quadrature points. Lines L4 and L5 solve the lumped momentum equation and apply the supports. Line L7 adds the change of the grid velocity to the particle velocity (FLIP); using $v_p \leftarrow \sum_i N_i v_i^{new}$ instead is the PIC update, which is more dissipative. Lines L9 to L11 update the strain and stress at the points; with a nonlinear or plastic material, line L11 calls its stress update.

## Example

**The cell crossing error.** Take $\Delta x = 1$ and 8 points at $x = 0.3, 0.9, 1.5, \ldots, 4.5$ (spacing 0.6), each with $V_p = 0.6$ and the same stress $\sigma = 1$. A uniform stress has no divergence, so the true internal force at every interior node is 0. With the hats, $N_i' = +1$ on the cell left of node $i$ and $-1$ on the cell to its right, so line L3 gives

$$f_i = \sigma \Bigl(\sum_{x_p \in [x_i, x_{i+1})} V_p - \sum_{x_p \in [x_{i-1}, x_i)} V_p\Bigr) / \Delta x.$$

The cells $[0, 1), [1, 2), \ldots, [4, 5)$ hold 2, 1, 2, 2 and 1 points, so the interior forces at nodes 1 to 4 are $-0.6, 0.6, 0, -0.6$ instead of 0. When a point crosses a cell boundary, one of these sums jumps by $V_p$, and the nodal force jumps with it. Bardenhagen and Kober (2004) call this the cell crossing noise.

**A vibrating bar.** A bar on $[0, 1]$ with $E = 100$ and $\rho = 1$ (wave speed $c = 10$) is fixed at $x = 0$ and free at $x = 1$. Its first mode has $\omega_1 = \pi c / 2$, period 0.4, and starting from $v = v_0 \sin(\pi x / 2)$ the velocity of the centre of mass is $(2 / \pi) v_0 \cos(\omega_1 t)$. With 20 cells, 2 points per cell, $v_0 = 0.1$ and $h = 0.1 \Delta x / c$, the code on this page stays within 0.7 percent of this value over one period (a measurement).

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It proves four facts about one step (theorems, in exact arithmetic):

- Lines L1 and L2 put all the particle mass and momentum on the grid: $\sum_i m_i = \sum_p m_p$ and $\sum_i (mv)_i = \sum_p m_p v_p$, because the hats form a partition of unity.
- Without supports, the step conserves the total particle momentum, because $\sum_i N_i' = 0$ makes $\sum_i f_i = 0$.
- A rigid translation with zero stress is reproduced exactly: every point moves by $h u$, and $F$ and $\sigma$ do not change.
- The internal force at an interior node is the stress times the difference of the particle volumes in the two cells next to the node, which is the formula of the example and the source of the cell crossing error.

Convergence is weaker than for the finite element method. The particle quadrature in line L3 is exact only for special particle positions, and Steffen, Kirby and Berzins (2008) show that the error from points crossing cell boundaries spoils the convergence in space of the original method with linear hats; with smoother shape functions, such as GIMP or B-splines, the error decreases with $\Delta x$. The order "1" in the front matter is the order of the explicit time step.

## Complexity

In the [real-RAM](/real-ram/) model, each point touches 2 nodes in 1D, $2^d$ nodes in $d$ dimensions with linear hats, and $3^d$ with quadratic B-splines. So lines L1 to L2 and L6 to L11 cost $\Theta(N)$ (with a factor $2^d$), lines L3 to L5 cost $\Theta(N + M)$ for $M$ nodes, and one step costs $\Theta(N + M)$ time and $\Theta(M)$ extra space. The explicit step needs $h \le C \Delta x / (c + |v|)$ with $c$ the wave speed and $C < 1$ (the [CFL condition](/courant-friedrichs-lewy-condition/)), so a run to time $T$ costs $\Theta((N + M) T c / \Delta x)$.

## Properties

- **Mass is exact.** Each point keeps its mass, so there is no mass error and no continuity equation to solve.
- **Linear momentum is conserved** by the transfers and the grid update, without supports.
- **Angular momentum is lost** by the PIC and FLIP transfers in general; the APIC transfer of the graphics literature conserves it.
- **No mesh distortion.** The grid is reset each step, so large strains and rotations cause no tangling.
- **History on the points.** Plastic strain, damage and other internal variables stay with the material.
- **Automatic contact.** Bodies that share grid nodes interact through the grid without a contact search. With one velocity per node they stick to each other, so sliding, friction and separation need a separate algorithm with one velocity field per body.
- **Cell crossing error.** With linear hats, the force on a node jumps when a point crosses a cell boundary.
- **Numerical fracture.** If neighbouring points move more than one cell apart, they no longer share a node, and the body separates without a physical cause.

## Variants and improvements

- **GIMP and CPDI.** [GIMP](/generalized-interpolation-material-point/) gives each point a finite domain and integrates the shape functions over it, which smooths the weights and reduces the cell crossing noise. CPDI follows the shape of the domain as it deforms.
- **B-spline MPM.** Quadratic or cubic B-splines on the grid have continuous gradients, which also removes the jumps.
- **Update stress first (USF) and modified USL.** The stress may be updated with the old grid velocity before the momentum solve, or with a velocity mapped back from the updated particles; the variants differ in energy behaviour.
- **APIC and PolyPIC transfers.** These store an affine or polynomial velocity on each point, which reduces dissipation and conserves angular momentum.
- **Implicit MPM.** A Newton solve on the grid allows steps above the CFL limit for slow or quasi-static problems.
- **Two-phase and multi-material MPM.** Several sets of points on one grid for soil with water, or for bodies in contact.

## When to use it

Use MPM for problems with very large deformation, flow of solids, fragmentation or many contacts: landslides and soil, impact and penetration, snow and ice, granular flow, and metal forming. Use the [finite element method](/finite-element-method/) on a Lagrangian mesh instead when the deformation is moderate and accurate stresses near boundaries matter, since MPM is less accurate per degree of freedom. For fluids without strength, [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) or grid methods are more common; MPM is useful when the material changes between solid-like and fluid-like.

## Pitfalls

- **Dividing by a tiny nodal mass.** A node that gets a small mass from a point near the far end of its support gets a huge acceleration in line L4, while its force is not small. Skip nodes with zero mass, and many codes also skip nodes whose mass is below a small threshold.
- **Cell crossing noise.** With linear hats and points that cross cells often, the stress shows spurious oscillations. Use GIMP or B-splines, or several points per cell.
- **Strain from the wrong velocity.** USL needs the updated grid velocity in line L9; using the old one with the stress update last changes the method.
- **Too large a step.** The explicit step is stable only below the CFL limit, which also depends on the particle speed.
- **Boundary conditions on the grid only.** Supports act on nodes, not on the physical boundary of the body, which lies between nodes; traction and contact conditions on curved boundaries need extra work.
- **Too few points per cell.** With one point per cell in 1D, the particle quadrature is poor and the zero energy modes of the grid are not controlled.

## Implementations

## History

The particle-in-cell method of fluid dynamics carried mass on particles and moved them with a grid solution, and FLIP added the full velocity on the particles to reduce its dissipation. Sulsky, Chen and Schreyer (1994) turned FLIP into a method for solids, with the stress and history variables on the points and the weak form of the momentum equation on the grid, and the method became known as the material point method. Bardenhagen and Kober (2004) identified the cell crossing noise and introduced GIMP, and Steffen, Kirby and Berzins (2008) analysed the quadrature errors. Since about 2013 the method has also been used widely in computer graphics for snow, sand and other materials.

## References
