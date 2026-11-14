---
tag: AWGX1V
kind: problem
slug: topology-optimization
name: Topology optimization
aliases:
- structural topology optimization
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Distribute material within a design domain to minimize compliance or another response under loads and a volume bound, by solving finite element models.
prereqs: [finite-element-method]
see_also: [simp-method, level-set-topology-optimization, support-structure-generation, infill-pattern, level-set-method, convex-function, semidefinite-programming, kkt-conditions]
sources:
  - paper: doi:10.1016/0045-7825(88)90086-2
    title: Martin P. Bendsøe and Noboru Kikuchi, Generating optimal topologies in structural design using a homogenization method, Computer Methods in Applied Mechanics and Engineering 71(2), 1988, 197 to 224
    locator: the formulation of the layout of a structure as the distribution of material, with microstructures of holes in each point
  - paper: doi:10.1007/BF01214002
    title: Ole Sigmund and Joakim Petersson, Numerical instabilities in topology optimization, a survey on procedures dealing with checkerboards, mesh-dependencies and local minima, Structural Optimization 16(1), 1998, 68 to 75
    locator: the descriptions of checkerboards, mesh dependence and local minima, and of the restrictions that remove them
  - book: isbn:978-3-540-42992-0
    title: Martin P. Bendsøe and Ole Sigmund, Topology Optimization, Theory, Methods and Applications, Springer, 2003
    locator: the chapter on the minimum compliance problem and the discussion of existence of solutions and relaxation
---

Topology optimization is the problem of deciding where material goes inside a design domain so that a structure carries its loads as well as possible with a given amount of material. Unlike sizing, which changes the thickness of fixed members, and shape optimization, which moves a boundary that is already there, topology optimization may also create holes and join or remove members. The standard form is minimum compliance: make the structure as stiff as possible under fixed loads and supports, with a bound on the volume. The response is computed with the [finite element method](/finite-element-method/), so every evaluation of a design is the solution of a linear system. Bendsøe and Kikuchi (1988) posed the problem as a distribution of material. In its pure 0/1 form the continuous problem has in general no solution, and on a mesh the answers show checkerboards and depend on the mesh, so every practical formulation adds a restriction such as a filter or a perimeter bound (Sigmund and Petersson 1998).

## In plain words

You have a block of space where a part may go, the points where it is held, and the forces that act on it. You may only use a part of the block, for example half of it. Which half should you keep so that the part bends as little as possible?

A computer splits the block into many small cells and asks, for each cell, whether it should be solid or empty. To judge a choice it computes how the whole part bends. The best answers often look like bones or bridges, with bars and holes, and nobody draws them by hand. Without extra rules the answers break into finer and finer patterns, so the rules must say how small a bar may be.

## Definition

**Continuous form.** A design domain $\Omega \subset \mathbb{R}^d$, with $d = 2$ or 3, supports on a part of its boundary, a load $f$, a solid material with elasticity tensor $E_0$, and a volume bound $V < |\Omega|$. A design is a set $\Omega_s \subseteq \Omega$ of solid material, or its indicator function $\chi$ with values in $\{0, 1\}$. The displacement $u$ solves the equations of linear elasticity with the tensor $\chi E_0$. The problem is

$$\min_{\chi}\ c(\chi) = \int f \cdot u \quad\text{subject to}\quad \int_\Omega \chi \le V,\quad \chi(x) \in \{0, 1\}.$$

The compliance $c$ is the work done by the load. A smaller compliance means a stiffer structure.

**Discrete form.** Divide $\Omega$ into $n$ finite elements with element stiffness matrices $K_e$. A design is a vector $x \in \{0, 1\}^n$, with a small $x_{\min} > 0$ in place of 0 so that the stiffness matrix stays invertible. Then

$$\min_x\ c(x) = f^{\mathsf T} K(x)^{-1} f \quad\text{subject to}\quad \sum_e x_e \le V,\quad x_e \in \{x_{\min}, 1\},$$

with $K(x) = \sum_e x_e K_e$ restricted to the free degrees of freedom. This is a nonlinear integer program.

**Why the pure problem is ill posed.** For the continuous form, a sequence of designs with finer and finer holes can lower the compliance toward an infimum that no 0/1 design reaches, so in general no optimal $\chi$ exists. Bendsøe and Sigmund (2003) explain the two ways out: relax the problem by allowing composite materials with a microstructure at each point, or restrict it, for example by a bound on the perimeter, a minimum length scale, or a filter. On a mesh this shows as two numerical faults: checkerboards, patterns of solid and void elements that the bilinear element models as too stiff, and mesh dependence, where a finer mesh gives a different design with finer members.

## Variants

- **Objective.** Minimum compliance under one or several loads, maximum of the lowest eigenfrequency, compliant mechanisms that maximize an output displacement, heat conduction, flow, and minimum volume under stress constraints.
- **Relaxed designs.** Densities $x_e \in [x_{\min}, 1]$ with a stiffness that is a function of the density. A power law with penalization is the SIMP model, see [SIMP method](/simp-method/). Composite microstructures give the homogenization method of Bendsøe and Kikuchi (1988).
- **Boundary based.** The design is the inside of the zero set of a function on the domain, see [level set topology optimization](/level-set-topology-optimization/).
- **Ground structures.** The design is a set of bar areas in a dense truss of candidate bars, and bars of area 0 are removed.
- **Manufacturing constraints.** Minimum and maximum member size, overhang angle for additive manufacturing (see [support structure generation](/support-structure-generation/)), a casting direction, symmetry, or a lattice or [infill](/infill-pattern/) in place of solid material.
- **Uncertain loads.** Worst case or expected compliance over a set of loads.

## Examples

**A cantilever on a $5 \times 2$ grid.** The domain is 5 by 2 unit square plane stress elements with $\nu = 0.3$ and $E_0 = 1$. The left edge is clamped and a unit load points down at the bottom right corner. The volume bound is 5 elements, and void elements have $x_{\min} = 10^{-3}$ with a stiffness of $x_{\min}^3$. There are $\binom{10}{5} = 252$ designs with exactly 5 solid elements, and the tests of the SIMP page compute all of them. The best is the bottom row, a straight beam from the clamp to the load, with compliance 347.38. Every other design has a compliance above $10^9$, because its solid elements do not form a stiff path from the load to the clamp. The answer is easy to guess here. On a real mesh the number of designs is far too large to enumerate.

**The relaxed lower bound.** In the same case, allow densities between $x_{\min}$ and 1 with a stiffness that is linear in the density. Every 0/1 design is also a relaxed design, and a stiffness of $x_{\min}$ is larger than $x_{\min}^3$, so the relaxed optimum is a lower bound on 347.38. A relaxed design with compliance about 107 exists (a measured value). Its densities are gray, so it is not a 0/1 structure.

**The MBB beam.** A simply supported beam with a central load at the top is the usual benchmark. On a mesh of the half beam with half of the area as material, the standard methods give a truss with a top and a bottom flange and diagonal members. The [SIMP method](/simp-method/) page shows the result on $24 \times 8$ elements and the effect of the filter radius on the number of checkerboard blocks.

## Known algorithms

- **[SIMP method](/simp-method/).** Densities with a penalized power law, updated by optimality criteria or by a gradient method, with a filter. This is the most used method.
- **Homogenization.** Bendsøe and Kikuchi (1988) gave each point a microstructure of rectangular holes and optimized their size and angle.
- **[Level set topology optimization](/level-set-topology-optimization/).** The boundary moves with the shape derivative as its speed, after Wang, Wang and Guo (2003) and Allaire, Jouve and Toader (2004).
- **Evolutionary and hard kill methods.** Remove the elements with the lowest strain energy step by step. They are simple and have weaker theory.
- **Ground structure methods.** For trusses, the minimum compliance and some minimum weight problems become convex programs in the bar areas.

## Bounds

- **Search space.** The discrete 0/1 problem on $n$ elements with a volume of $k$ elements has $\binom{n}{k}$ candidate designs, and each evaluation is a finite element solve. No polynomial algorithm for the 0/1 problem is known, and this page cites no hardness proof.
- **A proved lower bound.** With $K(x) = \sum_e x_e K_e$ linear in $x$, the compliance $f^{\mathsf T} K(x)^{-1} f$ is a [convex function](/convex-function/) of $x$, because it equals $\max_u (2 f^{\mathsf T} u - u^{\mathsf T} K(x) u)$, a maximum of affine functions. The relaxation to $x_e \in [x_{\min}, 1]$ is a convex problem, and its optimum is a lower bound on every 0/1 design. The proof is on the [SIMP method](/simp-method/) page.
- **Monotone in material.** If $K \preceq K'$ in the positive semidefinite order, then $f^{\mathsf T} K'^{-1} f \le f^{\mathsf T} K^{-1} f$. So adding material never increases the compliance, and the relaxed problem always has an optimum at which the volume bound is tight.
- **Cost of one evaluation.** One linear solve with $O(n)$ unknowns, which dominates the cost of every method. The number of design iterations of the common methods is measured, not bounded.

## Reductions

- **To a convex program.** The relaxed minimum compliance problem with stiffness linear in $x$ is convex, and by the Schur complement $c(x) \le \tau$ holds exactly when the matrix $\begin{pmatrix} \tau & f^{\mathsf T} \\ f & K(x) \end{pmatrix}$ is positive semidefinite. So it is a [semidefinite program](/semidefinite-programming/) in $(x, \tau)$. For trusses this is the usual convex form of truss topology design.
- **To a sequence of linear solves.** All the common methods evaluate the response and its derivative with one finite element solve per iteration, and for compliance the derivative needs no extra solve.
- **To level set motion.** A boundary that moves with a normal speed is the evolution of the zero set of a function, see the [level set method](/level-set-method/).

## Applications

- Lightweight brackets and frames in aerospace and automotive design.
- Parts for additive manufacturing, where the free shapes of the results can be printed, often with overhang limits.
- The design of material microstructures with given effective properties.
- Compliant mechanisms, heat sinks and flow channels.
- Architecture and civil engineering, for the layout of frames and bridges.

## References
