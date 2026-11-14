---
tag: H8FVX0
kind: algorithm
slug: level-set-topology-optimization
name: Level set topology optimization
aliases:
- level set structural optimization
area: cad/cam-and-additive-manufacturing
level: research
summary: Allaire's and Wang's method that moves the boundary of the structure as the zero set of a level set function with the shape derivative as speed.
solves: [topology-optimization]
model: real-ram
complexity:
  vars: {n: number of elements, h: number of elements across the short side, k: number of iterations}
  time: {worst: "O(k n (h^2 + n))"}
  space: {extra: "O(n h)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2003
  people: [Michael Yu Wang, Xiaoming Wang, Dongming Guo, Grégoire Allaire, François Jouve, Anca-Maria Toader]
  note: Wang, Wang and Guo (2003) and Allaire, Jouve and Toader (2004) moved the boundary of a structure with the level set method and a speed from the shape derivative, on a fixed mesh.
prereqs: [topology-optimization, level-set-method, finite-element-method]
see_also: [simp-method, upwind-scheme, signed-distance-function, fast-marching-method, eikonal-equation, bisection-method, lagrange-multiplier]
sources:
  - paper: doi:10.1016/S0045-7825(02)00559-5
    title: Michael Yu Wang, Xiaoming Wang and Dongming Guo, A level set method for structural topology optimization, Computer Methods in Applied Mechanics and Engineering 192(1-2), 2003, 227 to 246
    locator: the boundary as the zero set of a level set function, the speed from the strain energy, and the upwind Hamilton-Jacobi step on a fixed grid
  - paper: doi:10.1016/j.jcp.2003.09.032
    title: Grégoire Allaire, François Jouve and Anca-Maria Toader, Structural optimization using sensitivity analysis and a level-set method, Journal of Computational Physics 194(1), 2004, 363 to 393
    locator: the shape derivative of the compliance, the ersatz material on a fixed mesh, the reinitialization, and the remark that the method does not create new holes in 2D
  - book: isbn:978-3-540-42992-0
    title: Martin P. Bendsøe and Ole Sigmund, Topology Optimization, Theory, Methods and Applications, Springer, 2003
    locator: the minimum compliance problem that the method solves (general locator)
---

Level set topology optimization represents a structure by a function $\phi$ on the design domain: the structure is the set where $\phi < 0$, and its boundary is the zero set of $\phi$. To improve the structure, the method moves the boundary in its normal direction with a speed that comes from the shape derivative of the objective. Moving the boundary with a normal speed is the same as solving a Hamilton-Jacobi equation for $\phi$, which the [level set method](/level-set-method/) does on a fixed grid. Holes can merge, split from the boundary or vanish, so the topology changes without any special code. The response is computed with the [finite element method](/finite-element-method/) on the same fixed mesh, with a weak ersatz material in the holes. Wang, Wang and Guo (2003) and Allaire, Jouve and Toader (2004) proposed this approach for [topology optimization](/topology-optimization/). Unlike the [SIMP method](/simp-method/), every design has a crisp boundary and no gray elements. The method finds a local optimum that depends on the start, and in 2D it does not create new holes inside solid regions. This page gives a toy version on a grid of square elements, as a demonstration.

## In plain words

Think of the part as an island on a map. The coastline is the edge of the part. The method keeps a height for every point of the map: below 0 is land, above 0 is water. The coastline is where the height is 0.

Each round, the method computes how the part bends under its load. Where the material near the coast works hard, the land grows into the water. Where it does little, the water eats into the land. One rule keeps the total land area within its limit. Changing the heights moves the coastline, and two lakes can join, or a lake can open to the sea. Every few rounds, the heights are reset to the distance from the coast, so that they stay well behaved.

## The problem

The input is a design domain divided into $n = n_x n_y$ unit square bilinear plane stress elements, a load $f$, supports, and a bound $B$ on the number of solid elements. A design is the set $\Omega = \{e : \phi_e < 0\}$ for a level set function $\phi$ with one value per element. The element stiffness is $s_e = 1$ in $\Omega$ and $s_e = \varepsilon = 10^{-3}$ outside, the ersatz material, so that $K(s) = \sum_e s_e K_e$ is always invertible. The goal is a design with $|\Omega| \le B$ and a small compliance $c = f^{\mathsf T} u$, where $K(s)\, u = f$.

**The shape derivative.** Allaire, Jouve and Toader (2004) show that, if a part of the boundary that carries no load moves with the normal velocity $\theta \cdot n$, then the compliance changes by

$$c'(\Omega)(\theta) = -\int_{\partial\Omega} A e(u) : e(u)\ \theta \cdot n \, ds,$$

where $A e(u) : e(u)$ is twice the strain energy density. For the Lagrangian $c + \ell\, |\Omega|$ with a multiplier $\ell$, the derivative is $\int_{\partial\Omega} (\ell - A e(u) : e(u))\, \theta \cdot n \, ds$. So the normal speed $V = A e(u) : e(u) - \ell$ is a descent direction: the boundary moves out where the energy density is above $\ell$, and in where it is below.

**The level set equation.** If the zero set of $\phi$ moves with the normal speed $V$, with $\phi < 0$ inside, then $\phi$ satisfies the Hamilton-Jacobi equation

$$\frac{\partial \phi}{\partial t} + V\, |\nabla \phi| = 0.$$

## The algorithm

The code uses the element energies $w_e = u_e^{\mathsf T} k_0 u_e$, where $k_0$ is the element matrix for $E = 1$, as the values of $A e(u) : e(u)$ on the element. In the holes it uses the same formula with the ersatz displacement, which extends the speed off the boundary. It smooths $w$ once with the mean over the 4 neighbours and divides it by its maximum, so that $0 \le w_e \le 1$. The multiplier is $\ell \in [0, 1]$, so $|V| \le 1$, and the time step is $\Delta t = 1/2$.

```pseudo id=main
LEVEL-SET-TO(grid, f, supports, B, φ₀)       ▷ at most B elements with φ₀ < 0
L1  φ ← φ₀
L2  for it = 1 to iters do
L3      s_e ← 1 if φ_e < 0, else ε
L4      solve K(s) u = f; c ← fᵀu
L5      w_e ← u_eᵀ k₀ u_e, smoothed and divided by its maximum
L6      ℓ ← the smallest ℓ in [0, 1], by bisection, with #{e : STEP(φ, w − ℓ)_e < 0} ≤ B
L7      φ ← STEP(φ, w − ℓ)
L8      if it is a multiple of R then φ ← REINIT(φ)
L9  return φ

STEP(φ, V)                                   ▷ grid spacing 1
L10 D⁻x, D⁺x, D⁻y, D⁺y ← one-sided differences of φ, with edge values repeated
L11 ∇⁺ ← (max(D⁻x,0)² + min(D⁺x,0)² + max(D⁻y,0)² + min(D⁺y,0)²)^½; ∇⁻ likewise with max and min swapped
L12 φ_e ← φ_e − Δt (max(V_e, 0) ∇⁺_e + min(V_e, 0) ∇⁻_e)

REINIT(φ)
L13 P ← the zero crossings of φ on the segments between the centers of neighbouring elements
L14 φ_e ← min over q ∈ P of |center_e − q|, with the sign of φ_e
```

Lines L10 to L12 are the first order [upwind scheme](/upwind-scheme/) of Osher and Sethian for the Hamilton-Jacobi equation. Where the boundary moves out ($V > 0$), information comes from the inside, so $\nabla^+$ takes the differences from the side of smaller $\phi$. The step is stable when $\Delta t\, \max|V|\, (1/\Delta x + 1/\Delta y) \le 1$, which holds with equality here.

Line L6 keeps the volume bound. A larger $\ell$ lowers every speed, so it can only remove solid elements. With $\ell = 1$ every speed is at most 0 and nothing grows. So if the current design meets the bound, a feasible $\ell$ exists, and the [bisection](/bisection-method/) finds the smallest one up to $2^{-40}$. The real methods use a [Lagrange multiplier](/lagrange-multiplier/) that is updated from step to step, or an augmented Lagrangian.

Line L14 makes $\phi$ close to a [signed distance function](/signed-distance-function/) again. The upwind steps make $\phi$ steep or flat near the boundary, and a flat $\phi$ moves its zero set too fast. The code finds the distance by brute force over all zero crossings. Real codes solve the [eikonal equation](/eikonal-equation/) $|\nabla \phi| = 1$, for example with the [fast marching method](/fast-marching-method/), or a reinitialization equation.

## Example

**A cantilever.** A $24 \times 12$ grid is clamped on its left edge and has a unit load down at the middle of its right edge. The bound is $B = 144$, half of the elements. Because the method in 2D does not create holes, the start has a regular pattern of holes, shifted so that exactly 144 elements are solid. The pictures show the solid elements, top row first.

```
start                       after 40 iterations
##....####....####....##    ##################......
..####....####....####..    .##################.....
..####....####....####..    ...###...#####...###....
..####....####....####..    ....##....#.##....####..
##....####....####....##    ......####....####...###
##....####....####....##    .......###.....###....##
##....####....####....##    .......###.....###....##
..####....####....####..    ......####.....###...##.
..####....####....####..    .....#....#..##...####..
..####....####....####..    ...###....####....##....
##....####....####....##    .##################.....
##....####....####....##    #################.......
```

The final design has a top and a bottom chord and diagonals that carry the load to the clamp, with 144 solid elements.

| iteration | 1 | 2 | 6 | 11 | 21 | 31 | 40 |
|---|---|---|---|---|---|---|---|
| compliance | 237.4 | 2637.2 | 1525.0 | 199.5 | 125.2 | 82.0 | 72.0 |

The compliance is not monotone. The blocks of the start touch only at corners, the first steps move them, and the compliance jumps to 2637.2 in the second iteration. It first falls below the start value in iteration 11. The run takes about 2 s of Python. All these numbers are measured on this one case.

**Against brute force.** A $5 \times 2$ cantilever is clamped on the left and loaded at the bottom right corner, with $B = 5$ and void stiffness $10^{-3}$. The test computes all 638 designs with at most 5 solid elements: the best is the bottom row, with compliance 344.52. From three different start patterns, every design that the method visits has a compliance of at least 344.52, as it must. One start reaches 344.52 during the run but ends at 3938.45, and another ends with the top row, at 2804.6. On a grid this coarse the boundary moves a whole element at a time, and the result depends on the start.

## Correctness

The method is a descent heuristic, and its descent is not proved for the discrete code. What is proved is the bookkeeping: if the start has at most $B$ solid elements, every design has at most $B$ solid elements. The reason is that the update of line L12 is monotone in the speed, so the number of solid elements after a step does not increase with $\ell$, and $\ell = 1$ never adds a solid element. Line L14 keeps the sign of every element, so reinitialization does not change the design. On a linear $\phi$, both upwind gradients equal $|\nabla\phi|$ exactly away from the edges of the grid, so the scheme moves a straight boundary at the right speed. The loop stops after iters iterations. The full proof is below.

The shape derivative of Allaire, Jouve and Toader is a statement about smooth boundaries and exact solutions. On a grid of 0/1 elements with an ersatz material, the speed is only an estimate of it, and the measured compliance can go up, as the example shows.

## Complexity

One finite element solve with a band of width $O(h)$ takes $O(n h^2)$ time and $O(n h)$ space. One STEP takes $O(n)$ time, and line L6 calls it about 40 times. The brute force reinitialization compares $n$ elements with $O(n)$ crossings, $O(n^2)$ time. So $k$ iterations take $O(k\, n (h^2 + n))$ time. With a fast marching reinitialization the second term drops to $O(n \log n)$.

The number of iterations is chosen by the user. The method has no proved rate, and in the example the compliance settles after about 30 iterations.

## Properties

- **Crisp designs.** Every design is a set of elements, with no gray densities.
- **Topology changes.** Holes merge, open to the outside, or vanish, with no special code.
- **No new holes in 2D.** The zero set only moves, so a solid region without a hole cannot get one. The result depends on the holes of the start.
- **Feasible iterates.** In this code every design meets the volume bound, given a feasible start.
- **Not monotone.** The compliance of the iterates can rise, sometimes by a large factor.
- **Local.** The method finds a local optimum, and different starts give different designs.

## Variants and improvements

- **Topological derivative.** Adds a term that predicts where a small new hole lowers the objective, and nucleates holes there. This removes the dependence on the holes of the start.
- **Velocity extension and regularization.** Smooth the speed in a Sobolev space or extend it off the boundary with the eikonal equation, for more stable steps.
- **Parametric level sets.** Write $\phi$ as a sum of radial basis functions and optimize their weights with a standard optimizer, in place of the Hamilton-Jacobi step.
- **Reaction-diffusion and phase field updates.** Replace the transport equation by a diffusion equation for $\phi$, which also nucleates holes.
- **Body fitted meshes.** Remesh along the zero set in each iteration in place of the ersatz material, for an exact boundary in the finite element model.
- **Other objectives.** Eigenfrequencies, stress, compliant mechanisms and multiple materials, each with its own shape derivative.

## When to use it

Use a level set method when a crisp boundary matters during the optimization: for loads or conditions on the boundary itself, such as pressure, contact or flow, or when the result goes straight to a CAD model. For plain minimum compliance on a fixed mesh, the [SIMP method](/simp-method/) is simpler and less sensitive to the start. The method needs a start with many holes in 2D, or a topological derivative.

## Pitfalls

- **Too few holes in the start.** The method cannot add holes in 2D, so a full start stays a block with a moved outer edge.
- **Flat or steep $\phi$.** Without reinitialization, $\phi$ loses its distance property and the boundary moves at the wrong speed.
- **Large time steps.** A step above the stability limit makes the scheme oscillate. Even at the limit, as here, the boundary can jump a whole element per step.
- **Cutting a member.** A thin member can disappear in one step, and the compliance jumps up, as in the example. Keep the best design seen, or use smaller steps.
- **Ersatz stiffness too large or too small.** A large $\varepsilon$ lets holes carry load, and a tiny one makes the stiffness matrix badly conditioned.
- **Speed in the holes.** The energy in the ersatz material is not the energy that the solid would carry there. The extension of the speed off the boundary is a modeling choice.

## Implementations

## History

The level set method of Osher and Sethian (1988) tracks moving fronts with an implicit function. Sethian and Wiegmann (2000) used it for structural boundaries. Wang, Wang and Guo (2003) proposed a level set method for structural topology optimization with a speed from the strain energy. Allaire, Jouve and Toader (2004) gave the method its form based on the shape derivative, with an ersatz material on a fixed mesh. Later work added the topological derivative to nucleate holes, parametric level sets, and body fitted meshes.

## References
