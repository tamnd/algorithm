---
tag: 4J3GZH
kind: algorithm
slug: generalized-interpolation-material-point
name: Generalized interpolation material point method
aliases:
- GIMP
area: scientific-computing/n-body-and-particle-methods
level: research
summary: Gives each material point a finite domain and averages the grid shape functions over it, which reduces the cell crossing noise of the original MPM.
model: real-ram
complexity:
  vars: {N: the number of material points, M: the number of grid nodes}
  time: {worst: "Θ(N + M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, conservative: true, order: "1"}
history:
  year: 2004
  people: [Scott G. Bardenhagen, Edward M. Kober]
  note: Bardenhagen and Kober derived GIMP in 2004 from a weak form in which each material point owns a region of space, and so explained the cell crossing noise of MPM.
prereqs: [material-point-method]
see_also: [cloud-in-cell-assignment, b-spline, affine-particle-in-cell, fluid-implicit-particle, finite-element-method, smoothed-particle-hydrodynamics]
sources:
  - paper: doi:10.3970/cmes.2004.005.477
    title: Scott G. Bardenhagen and Edward M. Kober, The generalized interpolation material point method, Computer Modeling in Engineering and Sciences 5(6), 2004, 477-495
    locator: the weak form with particle characteristic functions, the GIMP weights and the cell crossing noise
  - paper: doi:10.1002/nme.2360
    title: Michael Steffen, Robert M. Kirby and Martin Berzins, Analysis and reduction of quadrature errors in the material point method (MPM), International Journal for Numerical Methods in Engineering 76(6), 2008, 922-948
    locator: the quadrature errors of MPM and GIMP and their effect on convergence
  - paper: doi:10.1016/0045-7825(94)90112-0
    title: Deborah Sulsky, Zhen Chen and Howard L. Schreyer, A particle method for history-dependent materials, Computer Methods in Applied Mechanics and Engineering 118(1-2), 1994, 179-196
    locator: the original MPM that GIMP changes
---

The generalized interpolation material point method (GIMP) is a version of the [material point method](/material-point-method/) in which each material point is not a point but a small region of the body, its domain. The weight that connects a point to a grid node is the average of the node's shape function over the domain, and the force uses the gradient of that average. With the linear hats of the original method, the force on a node jumps each time a point crosses a cell boundary; with GIMP the weights and their gradients change continuously, so the jumps go away and the stress noise is much smaller. The cost per step is the same order as MPM.

## In plain words

In the plain material point method each bead of material talks only to the two grid points around its centre. When a bead moves across a grid point, its pull on that grid point changes all at once, and the forces in the material jump. In GIMP each bead is a short piece of material with a width. Its pull on a grid point is the average pull over its whole width. When the piece slides over a grid point, part of it is on each side for a while, so the pull changes smoothly. If the pieces fit together with no gaps, a material under even tension feels no false forces inside at all, only at its two ends.

## The problem

The input is the same as for [MPM](/material-point-method/): $N$ material points with mass $m_p$, initial volume $V_p^0$, position $x_p$, velocity $v_p$, deformation gradient $F_p$ and stress $\sigma_p$; the stress rule (here 1D linear elasticity, $\dot\sigma = E \dot\varepsilon$); a grid of nodes $x_i = i \Delta x$ with the hats $N_i(x) = \max(0, 1 - |x - x_i| / \Delta x)$; the supports; and a step $h$. In addition each point has a half width $l_p$, here $l_p = F_p l_p^0$, so in 1D the domain $\Omega_p = [x_p - l_p, x_p + l_p]$ stretches with the material (the contiguous particle form, cpGIMP). The GIMP weight and its gradient are

$$S_{ip} = \frac{1}{2 l_p} \int_{x_p - l_p}^{x_p + l_p} N_i(x)\, dx, \qquad S_{ip}' = \frac{\partial S_{ip}}{\partial x_p} = \frac{N_i(x_p + l_p) - N_i(x_p - l_p)}{2 l_p}.$$

With the antiderivative $\Phi$ of the unit hat, $\Phi(t) = 0$ for $t \le -1$, $(t + 1)^2 / 2$ for $-1 \le t \le 0$, $1 - (1 - t)^2 / 2$ for $0 \le t \le 1$, and $1$ for $t \ge 1$, the weight is $S_{ip} = \Delta x \bigl(\Phi((x_p + l_p - x_i)/\Delta x) - \Phi((x_p - l_p - x_i)/\Delta x)\bigr) / (2 l_p)$. The rest of the step is the update stress last MPM step with $S_{ip}$ and $S_{ip}'$ in place of $N_i(x_p)$ and $N_i'(x_p)$.

## The algorithm

```pseudo id=main
GIMP-STEP(points, grid, E, h)
L1  for each material point p do                       ▷ points to grid
L2      l_p ← F_p l_p^0;  for each node i whose hat meets [x_p - l_p, x_p + l_p] do
L3          S_ip ← (1 / (2 l_p)) ∫ N_i over [x_p - l_p, x_p + l_p]
L4          S′_ip ← (N_i(x_p + l_p) - N_i(x_p - l_p)) / (2 l_p)
L5          m_i += S_ip m_p;  (mv)_i += S_ip m_p v_p
L6  f_i ← -Σ_p V_p σ_p S′_ip for every node i          ▷ internal force, V_p = F_p V_p^0
L7  v_i ← (mv)_i / m_i;  v_i^new ← v_i + h f_i / m_i;  v_i^new ← 0 at fixed nodes;  a_i ← (v_i^new - v_i) / h
L8  for each material point p do                       ▷ grid to points
L9      v_p ← v_p + h Σ_i S_ip a_i;  x_p ← x_p + h Σ_i S_ip v_i^new
L10     ε̇_p ← Σ_i S′_ip v_i^new;  F_p ← (1 + h ε̇_p) F_p;  σ_p ← σ_p + E h ε̇_p
L11 return the points; clear the grid
```

Lines L2 to L4 are the only change from MPM. With $l_p \le \Delta x$, a domain meets at most 3 hats in 1D, so line L2 visits at most 3 nodes, against 2 for MPM. Line L7 is the lumped explicit grid update with the supports, and lines L9 and L10 are the FLIP update and the stress update at the points, as in MPM.

## Example

Take the cell crossing example of the [MPM page](/material-point-method/): $\Delta x = 1$, 8 points at $x = 0.3, 0.9, \ldots, 4.5$, each with $V_p = 0.6$ and $\sigma = 1$. Give each point the half width $l_p = 0.3$, so the domains $[0, 0.6], [0.6, 1.2], \ldots, [4.2, 4.8]$ fill the body $[0, 4.8]$ with no gaps.

The point at $0.9$ has the domain $[0.6, 1.2]$. On it, $N_0$ has the mean $0.08 / 0.6 = 2/15$, $N_1$ has the mean $0.5 / 0.6 = 5/6$ and $N_2$ has the mean $0.02 / 0.6 = 1/30$; the three add up to 1. The gradients are $S_0' = (0 - 0.4) / 0.6 = -2/3$, $S_1' = (0.8 - 0.6)/0.6 = 1/3$ and $S_2' = (0.2 - 0)/0.6 = 1/3$.

Line L6 then gives the nodal forces $f = (1, 0, 0, 0, -0.2, -0.8, 0)$ at nodes 0 to 6. The interior nodes 1, 2 and 3 get no force, where MPM gave $-0.6, 0.6, 0$ at nodes 1 to 3. The only forces are the traction of the stress at the two ends of the body: $+1$ at the left end $x = 0$, and $-1$ at the right end $x = 4.8$, shared by nodes 4 and 5 in the ratio $N_4(4.8) : N_5(4.8) = 0.2 : 0.8$.

A measurement with the code on this page shows the effect on a run. Take the vibrating bar of the MPM page ($E = 100$, $\rho = 1$, 20 cells, 2 points per cell, $h = 0.1 \Delta x / c$, 800 steps, one period), started with $v_0 = 1$. The displacement amplitude $v_0 / \omega_1 \approx 0.064$ is larger than $\Delta x = 0.05$, so points cross cells. The largest second difference of the stress along the points, divided by $E v_0 / c$, is 0.044 with GIMP and 2.7 with MPM, and the energy error is 6 percent with GIMP and 26 percent with MPM. At $v_0 = 0.1$, where no point crosses a cell, the two methods agree.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It proves these facts (theorems, in exact arithmetic):

- The weights form a partition of unity and reproduce linear functions: $\sum_i S_{ip} = 1$, $\sum_i S_{ip} x_i = x_p$ and $\sum_i S_{ip}' = 0$. So the transfer of mass and momentum is exact, momentum is conserved without supports, and a rigid translation is exact, by the same arguments as for MPM.
- $S_{ip}'$ is the derivative of $S_{ip}$ with respect to $x_p$, and for $l_p > 0$ it is a Lipschitz continuous function of $x_p$ with constant $1 / (l_p \Delta x)$. So no nodal force jumps when a point crosses a node or a cell boundary.
- If the domains tile an interval $[a, b]$ and $V_p = 2 l_p$ (unit cross section), a uniform stress $\sigma$ gives $f_i = \sigma (N_i(a) - N_i(b))$: zero at every node whose hat does not reach an end of the body.

The last fact holds for any tiling, with points of any sizes and at any positions. For MPM the same force is the stress times the difference of the particle volumes in two cells, which is zero only for special positions.

GIMP does not make the method exact. When the domains do not tile the body, for example after a 2D or 3D deformation that the axis aligned domains of the simple form cannot follow, the quadrature error comes back, usually smaller than in MPM (a heuristic, not a bound); Steffen, Kirby and Berzins (2008) analyse these errors.

## Complexity

In the [real-RAM](/real-ram/) model, with $l_p \le \Delta x$ each point meets at most 3 hats per axis, so $3^d$ nodes in $d$ dimensions, against $2^d$ for MPM with linear hats. Each weight costs $O(1)$ through $\Phi$. So one step costs $\Theta(N + M)$ time and $\Theta(M)$ extra space, a constant factor of about $(3/2)^d$ above MPM for the transfers. The explicit step has the same [CFL limit](/courant-friedrichs-lewy-condition/) as MPM.

## Properties

- **Continuous weights and gradients.** $S_{ip}$ is continuously differentiable in $x_p$, so the forces change smoothly as points move.
- **Conservation.** Mass is exact, and momentum is conserved without supports, as in MPM.
- **No interior force from a uniform stress** when the domains tile the body (a theorem in 1D).
- **The MPM limit.** As $l_p \to 0$, $S_{ip} \to N_i(x_p)$ and $S_{ip}' \to N_i'(x_p)$ away from the nodes, so MPM is the limit of GIMP.
- **Wider stencil.** A point reaches nodes up to $\Delta x + l_p$ away, so the grid needs one more layer of nodes at the edges of the body.

## Variants and improvements

- **uGIMP.** The domain size stays $l_p^0$ for the whole run. This is cheap and is the form used in many codes, but the domains stop tiling the body under large stretch or compression.
- **cpGIMP.** The domain follows the stretch of the material along each axis, as in the code on this page ($l_p = F_p l_p^0$).
- **CPDI.** The convected particle domain interpolation of Sadeghirad, Brannon and Burghardt (2011) follows the domain as a parallelogram or a tetrahedron under the full deformation gradient, which also handles shear and rotation.
- **B-spline MPM.** Quadratic or cubic [B-spline](/b-spline/) shape functions on the grid have continuous gradients, which removes the jumps without particle domains. Computer graphics codes for snow and sand, for example those built on [APIC](/affine-particle-in-cell/), usually take this route; they use quadratic B-spline weights and do not use GIMP domains, and they aim at visual plausibility rather than at convergent stresses.

## When to use it

Use GIMP when an MPM solid moves more than a cell and the stress matters, for example in impact, soil and other geomechanics problems, or in any MPM run where the stress shows noise from cell crossing. If the deformation is small, so that the points stay in their cells, plain MPM gives the same answer at less cost. If shear and rotation are large in 2D or 3D, prefer CPDI or B-spline shape functions.

## Pitfalls

- **Domains that leave the grid.** A point near the edge of the body reaches one more node than in MPM; the grid must have that node.
- **The wrong domain size at the start.** For the zero interior force result, the domains must tile the body: with $n_c$ points per cell in 1D, $l_p^0 = \Delta x / (2 n_c)$ and the points at the centres of their domains.
- **Mixing uGIMP and the tiling claim.** With fixed domain sizes, a stretched body has gaps between domains and a compressed one has overlaps, and the force from a uniform stress is no longer zero.
- **Tiny nodal masses.** As in MPM, a node with a very small mass gets a huge acceleration; skip or threshold such nodes.
- **Boundary conditions.** A support acts on nodes, and the domain of a point next to a fixed node also overlaps the next node; check that the boundary is where the domains end.

## Implementations

## History

Bardenhagen and Kober (2004) wrote the weak form of the momentum equation with a characteristic function for the region of each material point. With a Dirac delta as the characteristic function they got the original MPM of Sulsky, Chen and Schreyer (1994), and with the indicator function of a box they got GIMP. They showed that the noise of MPM comes from the jumps of the hat gradients at cell boundaries. Steffen, Kirby and Berzins (2008) analysed the quadrature errors of both methods and their effect on convergence in space. CPDI followed in 2011.

## References
