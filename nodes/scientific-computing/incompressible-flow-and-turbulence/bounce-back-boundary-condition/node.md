---
tag: 0VQN3N
kind: technique
slug: bounce-back-boundary-condition
name: Bounce-back boundary condition
aliases:
- halfway bounce-back
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: Imposes no slip in lattice Boltzmann by sending distributions that hit a wall back along their incoming direction. The wall sits about halfway between a fluid node and a solid node.
prereqs: [lattice-boltzmann-method, bgk-collision-operator]
see_also: [multiple-relaxation-time-lattice-boltzmann, chapman-enskog-expansion, boundary-conditions, immersed-boundary-method, order-of-accuracy, navier-stokes-equations]
sources:
  - book: isbn:9783319446479
    title: "Timm Krüger, Halim Kusumaatmaja, Alexandr Kuzmin, Orest Shardt, Goncalo Silva and Erlend Magnus Viggen, The Lattice Boltzmann Method: Principles and Practice, Springer, 2017"
    locator: "Chapter 5 (boundary and initial conditions: bounce-back, moving walls, the Poiseuille slip)"
  - paper: doi:10.1007/BF02181482
    title: "Xiaoyi He, Qisu Zou, Li-Shi Luo and Micah Dembo, Analytic solutions of simple flows and analysis of nonslip boundary conditions for the lattice Boltzmann BGK model, Journal of Statistical Physics 87 (1997) 115-136"
  - paper: doi:10.1103/PhysRevE.68.066614
    title: "Irina Ginzburg and Dominique d'Humières, Multireflection boundary conditions for lattice Boltzmann models, Physical Review E 68 (2003) 066614"
  - paper: doi:10.1017/S0022112094001771
    title: "Anthony J. C. Ladd, Numerical simulations of particulate suspensions via a discretized Boltzmann equation. Part 1. Theoretical foundation, Journal of Fluid Mechanics 271 (1994) 285-309"
    locator: "the moving-wall bounce-back rule and the momentum exchange force"
  - paper: doi:10.1063/1.1399290
    title: "M'hamed Bouzidi, Mouaouia Firdaouss and Pierre Lallemand, Momentum transfer of a Boltzmann-lattice fluid with boundaries, Physics of Fluids 13 (2001) 3452-3459"
---

Bounce-back is the standard wall condition of the [lattice Boltzmann method](/lattice-boltzmann-method/). A population that would stream from a fluid node into a solid node is sent back to the node it came from, with the opposite velocity. In the halfway form used here, the reflection happens within the same time step, and the wall sits halfway between the last fluid node and the first solid node. It works with any collision operator, [BGK](/bgk-collision-operator/) or [MRT](/multiple-relaxation-time-lattice-boltzmann/). With BGK the exact wall position moves with the relaxation time $\tau$; with MRT or TRT the free rates can fix it.

## In plain words

In a lattice Boltzmann simulation, small packets of fluid hop from node to node along fixed directions. At a wall, some packets would hop into the solid. Bounce-back catches each such packet and sends it straight back the way it came, so it arrives at its own node again, now moving away from the wall. Nothing passes through the wall, and the packets that came in toward the wall go back out with the reversed velocity, so on average the fluid next to the wall does not slide along it. The rule needs no geometry other than a flag that says which nodes are solid. That is why it is easy to use in porous rock or around complex shapes, where walls are a staircase of cells.

## When it applies

- A lattice Boltzmann scheme with a collision step followed by a streaming step, on any lattice (D2Q9, D3Q19, D3Q27) whose velocity set contains $-c_i$ with each $c_i$.
- No-slip walls, at rest or moving tangentially. A wall is described by a flag on each node, fluid or solid; the wall is the set of links between a fluid node and a solid node.
- The method is accurate to second order when the wall is a straight line along the grid and lies halfway between nodes (He, Zou, Luo and Dembo 1997, for BGK). For a curved wall represented as a staircase, the wall position has an error of the order of the grid spacing, so the result is first order in the wall position.
- It is not for open boundaries (inflow, outflow, pressure) or for walls through which fluid passes.

## The template

```pseudo id=main
STREAM-WITH-BOUNCE-BACK(f*, solid, u_w)
L1  for each fluid node x and each velocity index i
L2      y ← x + c_i
L3      if solid(y) then
L4          f_ī(x, t + 1) ← f*_i(x, t) - 2 w_i ρ(x) (c_i · u_w(y)) / c_s^2     ▷ ī: the index with c_ī = -c_i
L5      else f_i(y, t + 1) ← f*_i(x, t)
L6  return f
```

The holes are the solid flag `solid(y)`, which describes the geometry, and the wall velocity `u_w`, which is zero for a wall at rest. Line L2 finds the node that population $i$ would reach. Line L3 tests whether that link crosses a wall. Line L4 is the bounce: the population returns to its own node $x$ in the slot of the opposite velocity, at the next time. The second term on line L4 is Ladd's correction for a moving wall: it adds the momentum that a wall moving at $u_w$ gives to the population. For a wall at rest it is zero, and line L4 reads $f_{\bar\imath}(x, t+1) = f_i^*(x, t)$. Line L5 is ordinary streaming. The density $\rho(x)$ on line L4 is the density of the fluid node; with $\rho \approx 1$ many codes use the reference density.

Because each population that reaches a wall is put back into the same node, the map from post-collision populations to new populations is a permutation (for a wall at rest). So the total mass is conserved exactly; the [MRT correctness proof](/multiple-relaxation-time-lattice-boltzmann/) gives the argument in full. Momentum is not conserved, because the wall exerts a force. The force on the wall from one link is the momentum exchange $(f_i^* + f_{\bar\imath}) c_i$ (Ladd 1994), summed over all wall links.

**Hand example.** Take a top wall moving with $u_w = (0.01, 0)$, in lattice units, above a node at rest with $\rho = 1$ and equilibrium populations. The populations that hit the top wall are $i = 2$, $5$ and $6$, with $c_2 = (0,1)$, $c_5 = (1,1)$ and $c_6 = (-1,1)$. Line L4 with $c_s^2 = \frac13$ and $w_5 = w_6 = \frac1{36}$ gives

$$f_4 = f_2^* = \tfrac19, \qquad f_7 = f_5^* - 6 \cdot \tfrac1{36} \cdot 0.01 = \tfrac1{36} - \tfrac1{600}, \qquad f_8 = f_6^* + \tfrac1{600}.$$

The populations $f_7$ (velocity $(-1,-1)$) and $f_8$ (velocity $(1,-1)$) now differ, so the node gets the $x$ momentum $-f_7 + f_8 = \frac1{300}$ from the wall in one step. Their sum is still $\frac1{18}$, so no mass is created.

## Classic examples

**Poiseuille flow (a wall at rest).** A channel of $n_y$ nodes, periodic in $x$, with walls at $y = -\frac12$ and $y = n_y - \frac12$ and a body force $g$ along $x$. The exact profile is $u(y) = \frac{g}{2\nu}(y + \frac12)(n_y - \frac12 - y)$. With BGK the computed steady profile is this parabola plus a constant slip $s$, the same at every node. Runs with $n_y = 8$ and $g = 10^{-6}$ gave $s/g = -3.55$ at $\tau = 0.6$, $-0.65$ at $\tau = 0.8$ and $0.25$ at $\tau = 1$, which matches $s = g\bigl(2(\tau - \frac12) - \frac3{8(\tau - \frac12)}\bigr)$, the formula on the [lattice Boltzmann page](/lattice-boltzmann-method/). The slip vanishes at $\tau = \frac12 + \frac{\sqrt3}4 \approx 0.933$. With $\tau = 0.8$ fixed and $g$ fixed, the relative max error was 0.0325, 0.00813 and 0.00203 for $n_y = 4$, 8 and 16: the slip is a constant in lattice units, the velocity grows like $n_y^2$, and the observed order is 2.00. This is the second order of halfway bounce-back. The analysis of He, Zou, Luo and Dembo (1997) explains the slip for BGK.

**Couette flow (a moving wall).** The same channel with no force, a wall at rest at the bottom and a top wall moving at $U = 0.01$. The exact profile is linear, $u(y) = U(y + \frac12)/n_y$. With $n_y = 8$ the computed profile matched it to $3 \cdot 10^{-13} U$ for $\tau = 0.6$, 0.8, 1 and 1.5. A linear profile has no second derivative, so the $\tau$-dependent slip of the Poiseuille case does not appear.

**Exact Poiseuille flow with MRT.** On the [MRT page](/multiple-relaxation-time-lattice-boltzmann/), choosing the rate $s_q$ of the heat flux moments so that $(\frac1{s_\nu} - \frac12)(\frac1{s_q} - \frac12) = \frac3{16}$ puts the wall exactly halfway for any viscosity. The Poiseuille error then drops to the convergence tolerance of the run. Ginzburg and d'Humières (2003) derive this condition for two-rate schemes.

**Porous media.** In a pore-scale simulation the solid flag comes straight from a voxel image, and bounce-back on every fluid-solid link gives the no-slip condition without any surface mesh. The permeability then depends on $\tau$ under BGK, which is why such codes use MRT or TRT.

## Variations

- **Full-way bounce-back.** The population enters the solid node, is stored for one step with its velocity reversed, and comes back in the next step. It needs no special streaming code, but the reflection takes one more time step. Use the halfway form unless the code structure forbids it.
- **Moving walls.** Line L4 with the Ladd term, as in the Couette example.
- **Interpolated bounce-back.** For a curved wall that cuts a link at a fraction $q$ of its length, Bouzidi, Firdaouss and Lallemand (2001) interpolate between neighboring populations so that the reflection happens at the true wall position. This restores second order for curved walls; it is no longer an exact permutation, so mass is not exactly conserved.
- **Multireflection.** Ginzburg and d'Humières (2003) use more neighbors to reach higher accuracy and to remove the dependence of the wall position on the rates.
- **Alternatives.** Velocity and pressure boundaries that build the unknown populations from the prescribed macroscopic values (the Zou-He scheme), and the [immersed boundary method](/immersed-boundary-method/), which spreads a wall force onto the lattice and does not need wall-aligned nodes.

## Pitfalls

- **Comparing with walls on the nodes.** With halfway bounce-back the wall is at $y = -\frac12$, not at $y = 0$. Comparing with an exact solution whose wall is at the first node gives an error of order $h$ that looks like a bug in the scheme. Place the walls of the exact solution halfway, as in the Poiseuille example.
- **Writing the bounced value into the wrong slot.** Line L4 writes into slot $\bar\imath$ of node $x$. Writing into slot $i$ of $x$ (no reversal), or into slot $\bar\imath$ of the solid node, loses mass or sends it into the wall.
- **Bouncing pre-collision values.** Line L4 must use the post-collision value $f_i^*$. Using the pre-collision $f_i$ changes the effective wall position.
- **The moving wall sign.** The Ladd term on line L4 has a minus sign with the index $i$ of the incoming population. With the sign flipped, the wall drags the fluid in the wrong direction; the hand example above is a quick check.
- **Expecting a viscosity-independent wall with BGK.** With BGK the slip changes with $\tau$, so a permeability computed at two viscosities differs. This is a property of BGK bounce-back, not a bug; use MRT or TRT with a fixed $\Lambda$.
- **Diagonal links at corners.** At the outer corner of a solid block, a diagonal population can hit a solid node while its axis neighbours do not. Line L3 must test each link on its own, not each node.

## Exercises

1. Show that for a wall at rest, the streaming of lines L1 to L5 is a permutation of the post-collision values, and conclude that the total mass is conserved.
2. In the steady Couette run, sum the momentum exchange $(f_i^* + f_{\bar\imath})c_i$ over the links of one bottom wall node, and compare the $x$ component with the shear stress $\rho\nu U/n_y$.
3. Starting from the slip formula, find the value of $\tau$ at which BGK Poiseuille flow is exact, and check the value $\frac12 + \frac{\sqrt3}4$.

## References
