---
tag: PNJ37X
kind: algorithm
slug: brittle-fracture
name: O'Brien-Hodgins brittle fracture
aliases:
- graphical modeling of brittle fracture
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Split the stress of each finite element into tensile and compressive parts, form a separation tensor at each node, and cut the mesh there when its largest eigenvalue exceeds the toughness.
model: real-ram
complexity:
  vars: {n: "the number of nodes", m: "the number of elements"}
  time: {forces_and_tensors: "Θ(n + m)", step: "Θ(n + m)"}
  space: {extra: "Θ(n + m)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1999
  people: [James F. O'Brien, Jessica K. Hodgins]
  note: O'Brien and Hodgins split the nodal forces of a finite element mesh into tensile and compressive parts, built a separation tensor at each node from them, and cut the mesh locally where it exceeded the toughness.
prereqs: [st-venant-kirchhoff-model, eigenvalue]
see_also: [peridynamics, corotational-fem, invertible-finite-elements, finite-element-method, mass-lumping, symplectic-euler-method, material-point-method, mass-spring-system]
sources:
  - paper: doi:10.1145/311535.311550
    title: James F. O'Brien and Jessica K. Hodgins, Graphical modeling and animation of brittle fracture, Proceedings of SIGGRAPH 99, 137-146
    locator: Section 4.1 (Eq. 28 to 31, the tensile and compressive parts of the stress and the forces), Section 4.2 (Eq. 32, the separation tensor and the toughness test), Section 4.3 (local remeshing and the snapping thresholds of 5 mm and 0.1 radians)
  - paper: doi:10.1145/2343483.2343501
    title: Eftychios Sifakis and Jernej Barbič, FEM simulation of 3D deformable solids, a practitioner's guide to theory, discretization and model reduction, SIGGRAPH 2012 Courses, article 20
    locator: the St. Venant-Kirchhoff model and the nodal forces of a linear element (general locator)
---

O'Brien-Hodgins brittle fracture lets a finite element mesh crack where it is pulled apart.
At every step it splits the stress of each element into a tensile part and a compressive part, and it computes the nodal forces of each part.
At each node it combines these forces into a symmetric separation tensor $\varsigma$.
If the largest eigenvalue of $\varsigma$ is above the toughness $\tau$, the mesh is cut through the node along the line (in 3D, the plane) normal to the eigenvector, and the node is duplicated.
O'Brien and Hodgins (1999) gave the method for tetrahedra; this page and its code use triangles in 2D.

## In plain words

Think of a slab of glass made of many small triangles.
Each triangle pulls and pushes on its corners.
At each corner the method asks a simple question: do the triangles around this corner pull it apart in two opposite directions?
A corner that the whole slab drags in one direction is not being torn, and a corner that is only squeezed is not being torn either.
Only a pull from two sides counts.
When the tearing pull is stronger than a chosen strength, the method cuts the mesh through that corner.
It gives the corner a twin, so the triangles on one side of the cut use the old corner and the triangles on the other side use the new one.
Then the two sides can move apart.
A crack grows one corner at a time, step by step.

## The problem

The input is a triangle mesh with rest positions $X$, current positions $x$, velocities $v$, the Lamé parameters $\mu$ and $\lambda$, a density, the toughness $\tau$ and a time step $\Delta t$.
Each element has the rest edge matrix $D_m$ with $\det D_m > 0$, the current edge matrix $D_s$, $F = D_s D_m^{-1}$, the Green strain $E = (F^T F - I)/2$ and the rest area $V_0 = \det D_m/2$.
The material is the [St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/) with the stress $S = 2\mu E + \lambda\operatorname{tr}(E)I$, as in the paper, which uses an isotropic linear stress of the Green strain.

The output of one step is the new state, and possibly a new mesh in which one node has been split.
The method must decide where the material breaks and in which direction, from the local state only.
It must not break a body that is only compressed or only translated as a whole, and the result must not depend on the orientation of the body in the world.

## The algorithm

```pseudo id=main
FRACTURE-STEP(mesh, Δt, τ)              ▷ m(a) = a a^T / |a| and m(0) = 0
L1  for each element: F ← D_s D_m^(-1), E ← (F^T F - I)/2, S ← 2μE + λ tr(E) I
L2      S+ ← Σ_i max(0, v_i) n_i n_i^T over the eigenpairs (v_i, n_i) of S, and S- ← S - S+
L3      f ← the nodal forces of S, f+ ← the nodal forces of S+, f- ← f - f+
L4  for each node a: ς_a ← ½(-m(Σ f+) + Σ m(f+) + m(Σ f-) - Σ m(f-)), the sums over the elements at a
L5  (a*, v+, n̂) ← the node with the largest eigenvalue v+ of ς_a, and its unit eigenvector
L6  if v+ > τ then SPLIT-NODE(a*, n̂)
L7  recompute f; v ← v + Δt f / mass; x ← x + Δt v

SPLIT-NODE(a, n̂)
L8  for each of the two rays from x_a normal to n̂: unless the ray snaps to an existing edge, cut the element it crosses and the neighbor across the crossed edge
L9  sort the elements at a by the side of the line on which their centroid lies
L10 if both sides have elements: add a copy a' of a with the same rest position, position and velocity, and give a' the elements on the negative side
L11 recompute D_m^(-1), V_0 and the lumped masses
```

Lines L1 to L3 are Eq. 28 to 31 of the paper.
The nodal forces of a stress $\Sigma$ on the nodes 1 and 2 of an element are the columns of $-V_0 F\Sigma D_m^{-T}$, and node 0 gets minus their sum.
These are linear in $\Sigma$, so $f^+ + f^- = f$.
Line L4 is Eq. 32.
At each node $f^+$ and $f^-$ come as sets with one force per element at the node.
Line L5 is the fracture test of Section 4.2, and line L6 does at most one split per step in the code of this page.
The paper also handles several eigenvalues above $\tau$ by splitting for the largest one, remeshing and computing again.

Lines L8 to L10 are the local remeshing of Section 4.3.
A cut through an element $(a, b, c)$ from its vertex $a$ meets the opposite edge $bc$ at a new node $p$ with $x_p = (1 - s)x_b + s x_c$; the rest position and the velocity of $p$ use the same $s$.
The element becomes two elements, and the neighbor across $bc$ is also cut at $p$, so the mesh stays conforming.
The ray snaps to an existing edge when an edge from $a$ is within 0.1 radians of it, and the new node snaps to $b$ or $c$ when $s < 0.05$ or $s > 0.95$; the paper uses 5 mm and 0.1 radians.
These thresholds are tuning choices.
They stop tiny and thin elements, which would need a tiny time step.
The new crack tips $p$ are not duplicated, so the crack grows one node per split.

Line L7 is [symplectic Euler](/symplectic-euler-method/) with a velocity damping factor in the code; the paper uses explicit integrators and a damping stress.

## Example

Take a square of 2 m by 2 m made of 2 by 2 cells of 1 m, each cut into two triangles, so 8 triangles meet at the center node.
Use $E = 1$ Pa and $\nu = 0.3$, so $\mu = 0.384615$ N/m and $\lambda = 0.576923$ N/m, and $\tau = 0.1$ N.
Each row maps the rest square by a uniform deformation; so the stress is the same in every element and the net force on the center node is zero.

| Deformation $x = \varphi(X)$ | eigenvalues of $S$ | eigenvalues of $\varsigma$ at the center | $\hat n$ | split? |
|---|---|---|---|---|
| $(1.1X_1, X_2)$ | $0.141346$, $0.060577$ | $0.155481$, $0.060577$ | $(1, 0)$ | yes |
| $(1.1X_1, 1.1X_2)$ | $0.201923$, $0.201923$ | $0.222115$, $0.222115$ | $(1, 0)$, any direction | yes |
| $(0.9X_1, X_2)$ | $-0.054808$, $-0.127885$ | $-0.054808$, $-0.115096$ | $(0, 1)$ | no |
| $(X_1 + 0.2X_2, X_2)$ | $0.096537$, $-0.058076$ | $0.150671$, $-0.074236$ | $(0.741453, 0.671005)$ | yes |
| $R(1.1X_1, X_2)$ with $R$ the rotation with $\cos = 0.8$ | $0.141346$, $0.060577$ | $0.155481$, $0.060577$ | $(0.8, 0.6)$ | yes |

In the first row the pull is along $x$, so the crack runs vertically through the center, across the pull.
In the third row all stresses are compressive, so $f^+ = 0$ and $\varsigma = -\frac12\sum m(f^-)$ has no positive eigenvalue, and nothing breaks.
In the fourth row, a shear, only one principal stress is tensile, and the crack normal is the principal direction of the stretch, about 42 degrees from the $x$ axis.
In the last row the body of the first row is rotated by about 36.87 degrees: the eigenvalues of $\varsigma$ are the same and $\hat n$ turns with the body.

For a measurement, take a strip of 3 m by 1 m with 6 by 2 cells whose end nodes are pulled apart at 0.05 m/s each, with $\Delta t = 0.02$ s and damping 0.5.
In the test code the first split comes at step 47, 114, 212 and 364 for $\tau = 0.02$, $0.05$, $0.1$ and $0.2$ N, and the strip is in two pieces at step 87, 196, 310 and 509.
So a tougher material breaks later, at a larger stretch.

## Correctness

The [proof](proofs/correctness.md) shows these facts, each a proved property.

- Line L2 gives $S^+ + S^- = S$ with $S^+$ positive semidefinite, $S^-$ negative semidefinite and $S^+S^- = 0$, and line L3 gives $f^+ + f^- = f$.
- The nodal forces of line L3 are the exact negative gradient of the St. Venant-Kirchhoff energy $\sum_e V_0\bigl(\mu|E|_F^2 + \frac{\lambda}{2}\operatorname{tr}(E)^2\bigr)$.
- $\varsigma$ is symmetric. Under a rigid motion $x \mapsto Qx + t$ it becomes $Q\varsigma Q^T$, so the eigenvalues do not change and the crack direction turns with the body.
- At a node of only one element $\varsigma = 0$: a force that is not balanced by an opposite force does not open a crack.
- If all elements at an interior node have a negative definite stress, then $\varsigma$ is negative semidefinite, so a compressed body does not break. If they all have a positive definite stress, $\varsigma$ is positive semidefinite.
- Lines L8 to L11 keep the mesh conforming with every element positively oriented. They keep the positions, the total rest area, the total mass, the linear momentum and the elastic energy unchanged, so a split adds no energy.

The key step is that each term $m(f)$ is positive semidefinite and $m(Qf) = Qm(f)Q^T$: line L4 compares the forces one by one with their sum, so it measures pulls that cancel at the node and ignores the net force.

## Complexity

Lines L1 to L3 cost a constant amount of work per element, and line L4 a constant amount per incident element of each node, so lines L1 to L5 cost $\Theta(n + m)$ for $n$ nodes and $m$ elements.
A split changes a constant number of elements near the node if the mesh stores the elements around each node; the code of this page scans the element list, which costs $\Theta(m)$ per split.
Line L11 is local too in a careful code; the code of this page recomputes all elements, which is also $\Theta(m)$.
So a step costs $\Theta(n + m)$, and memory is $\Theta(n + m)$.
Each split adds one node and, for each of the up to two cut edges, one node and up to two elements.

## Properties

- **Local and direction aware.** The test at a node uses only the forces of its elements, and it gives the crack direction as well as the decision. This is proved.
- **Frame invariant.** Rigid motions do not change the decision, and the direction turns with the body. This is proved.
- **No breaking in compression or in rigid motion.** Proved for uniform states at interior nodes. Boundary nodes of a compressed body can have small positive eigenvalues, because their forces are not balanced; this is a measurement of the example code.
- **Conservation in the split.** The split adds no energy, no area and no mass, and it keeps the linear momentum $\sum m_i v_i$, because the new velocities interpolate the old piecewise linear velocity field and a lumped mass is the integral of the density times the hat function of the node. This is proved.
- **Mesh dependent.** The crack follows the mesh within the snapping thresholds and moves at most one node per step, so its speed depends on $\Delta t$ and on the element size. This is a heuristic of the method, not a law.
- **Toughness is a tuning value.** $\tau$ is a force, not a material constant from a test, and the right value depends on the mesh. This is a tuning choice.

## Variants and improvements

- **3D.** The paper works on tetrahedra, where a cut plane through a node crosses its tetrahedra, and a cut tetrahedron usually becomes three. The decomposition and the separation tensor are the same.
- **Ductile fracture.** O'Brien, Bargteil and Hodgins (2002) added plastic flow before the fracture, so metals bend and tear.
- **Particles and nonlocal models.** [Peridynamics](/peridynamics/) breaks bonds between particles instead of cutting elements, and the [material point method](/material-point-method/) lets material separate on a background grid with no remeshing.
- **Other materials.** The decomposition works for any stress tensor, so the elastic model can be the [corotational](/corotational-fem/) or an [invertible](/invertible-finite-elements/) model, if its stress is written in the same frame as the forces.
- **Spring models.** A [mass-spring system](/mass-spring-system/) can break a spring when it stretches past a limit. It is simpler, but the crack direction then depends on the springs, not on the stress.

## When to use it

Use it for animation of brittle objects such as glass, ceramics, stone or frozen material, where the crack pattern should come from the stress and not from a precomputed pattern.
It suits explicit simulations with small time steps, because the crack grows one node per step.
For real time breaking of rigid objects, a precomputed fracture pattern is much cheaper.
For engineering predictions of crack growth, use a method from fracture mechanics with a calibrated toughness; this method is a model for animation.

## Pitfalls

- **Separating the stress in the wrong frame.** Line L2 must split the same stress that line L3 maps to forces. Splitting a world frame stress and mapping it with $F S D_m^{-T}$ mixes two frames and gives a wrong $f^+$ for a rotated body.
- **Forgetting the term $m(\sum f)$.** Without the first and the third terms of line L4 every node of a pulled body looks torn, including a node that the body only drags along, such as a node with one element.
- **Using $ff^T$ in place of $m(f)$ in line L4.** $m(f) = ff^T/|f|$ is linear in the size of the force. With $ff^T$ the test is quadratic in the force, and $\tau$ then has the wrong units.
- **No snapping.** If line L8 always cuts, a crack near an existing edge makes very thin elements, and the explicit step of line L7 then needs a tiny $\Delta t$ or becomes unstable.
- **Cutting a crossed element but not its neighbor.** If line L8 cuts only the element, the new node lies inside an edge of the neighbor, the mesh is no longer conforming, and the neighbor does not move with it.
- **Duplicating the crack tips.** If line L10 also duplicates the new nodes $p$, the crack opens along the whole cut at once, not one node per step, and an element can lose its connection to the rest.
- **Not recomputing after a split.** If line L7 uses the forces from before line L6, the new nodes have no force, and the old masses do not match the new mesh.

## Implementations

## History

Terzopoulos and Fleischer (1988) let a deformable model break where its deformation passed a limit.
O'Brien and Hodgins (1999) introduced the separation tensor on a finite element mesh, with the split of the stress into tensile and compressive parts and a local remesh, and they showed examples such as an adobe wall that breaks.
O'Brien, Bargteil and Hodgins (2002) extended it to ductile fracture with plasticity.
Later work in graphics replaced the remesh by virtual nodes, by particles or by nonlocal models, and moved the expensive work to a precomputation for interactive use.

## References
