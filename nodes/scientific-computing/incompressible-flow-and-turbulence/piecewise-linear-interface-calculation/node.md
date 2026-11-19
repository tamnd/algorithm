---
tag: AZM3X0
kind: algorithm
slug: piecewise-linear-interface-calculation
name: Piecewise linear interface calculation
aliases:
- PLIC
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: Reconstructs the interface in each cell as a plane with normal from the volume fraction gradient, placed so it cuts off the cell's fraction.
solves: [advection-equation]
model: real-ram
complexity:
  vars: {N: "the number of cells along each side of the grid", K: "the number of time steps"}
  time: {worst: "Θ(K N^2)"}
  space: {extra: "Θ(N^2)"}
properties: {deterministic: true, eulerian: true, conserves_volume_exactly: true, reconstruction_keeps_volume: true, geometric_fluxes: true, normal_order: "first order with Youngs normals, second order with ELVIRA"}
history:
  year: 1982
  people: [David L. Youngs]
  note: "Youngs (1982) put a straight line with a normal from the neighboring fractions in each mixed cell. Scardovelli and Zaleski (2000) gave closed forms that link the line position and the volume fraction. Pilliod and Puckett (2004) gave normals that are second order."
prereqs: [volume-of-fluid-method, polygon-clipping, shoelace-formula]
see_also: [level-set-method, front-tracking-method, continuum-surface-force, sutherland-hodgman, marching-squares, particle-level-set, operator-splitting, ghost-fluid-method]
sources:
  - paper: "D. L. Youngs, Time-dependent multi-material flow with large fluid distortion, in K. W. Morton and M. J. Baines (eds.), Numerical Methods for Fluid Dynamics, Academic Press, 1982, 273-285"
    locator: "the straight-line interface in each mixed cell and its normal from the neighboring volume fractions"
  - paper: doi:10.1006/jcph.2000.6567
    title: "Ruben Scardovelli and Stéphane Zaleski, Analytical relations connecting linear interfaces and volume fractions in rectangular grids, Journal of Computational Physics 164 (2000) 228-237"
    locator: "the closed-form relations between the line constant and the volume fraction"
  - paper: doi:10.1146/annurev.fluid.31.1.567
    title: "Ruben Scardovelli and Stéphane Zaleski, Direct numerical simulation of free-surface and interfacial flow, Annual Review of Fluid Mechanics 31 (1999) 567-603"
    locator: "the review of VOF interface reconstruction and advection"
  - paper: doi:10.1016/j.jcp.2003.12.023
    title: "James E. Pilliod and Elbridge G. Puckett, Second-order accurate volume-of-fluid algorithms for tracking material interfaces, Journal of Computational Physics 199 (2004) 465-502"
    locator: "the LVIRA and ELVIRA normals and the comparison of reconstruction orders"
  - paper: doi:10.1006/jcph.1998.5906
    title: "William J. Rider and Douglas B. Kothe, Reconstructing volume tracking, Journal of Computational Physics 141 (1998) 112-152"
---

Piecewise linear interface calculation (PLIC) is the reconstruction step of the [volume of fluid method](/volume-of-fluid-method/). The grid stores only the fraction $F$ of each cell filled with liquid, and PLIC turns these numbers into a surface: in each cell that is partly full it draws a straight line (a plane in 3D) with its normal taken from the change of $F$ across the neighbors, and slides the line until it cuts off exactly the fraction $F$. The fluxes between cells are then areas of polygons, not guesses. The result is a sharp interface at most one cell thick, with the liquid volume kept to rounding error.

## In plain words

Look at one cell of the grid that is 30% full of water. The number 30% does not say where the water is in the cell. The neighbors do: if the cells to the left are full and the cells to the right are empty, the water is on the left. PLIC finds the direction in which $F$ falls fastest, from a block of 3 by 3 cells, and takes that as the direction out of the water. It draws a line across the cell at right angles to that direction and moves it until the water side has exactly 30% of the cell. To move water to the next cell, it cuts out the strip that crosses the face and measures the water in it. That amount moves. Since water only moves from one cell to the next, none is lost.

## The problem

Given volume fractions $F_{ij} \in [0, 1]$ on an $N \times N$ periodic grid of cells of side $\Delta x = 1/N$, and a divergence-free velocity, advect $F$ by $\partial_tF + u\,\partial_xF + v\,\partial_yF = 0$ for $K$ steps of size $\Delta t$, keeping the total volume $\sum F_{ij}\Delta x^2$ and the bounds $0 \le F \le 1$, and keeping the interface sharp. As on the [VOF page](/volume-of-fluid-method/), the face velocity is $u(y)$ on the faces normal to $x$ and $v(x)$ on the faces normal to $y$, which covers solid body rotation and translation and makes each split sweep divergence free.

The reconstruction subproblem is this. In the cell coordinates $(x, y) \in [0, 1]^2$, given a normal $n = (n_x, n_y) \ne 0$ that points out of the fluid and a fraction $f$, find $\beta$ so that the part of the cell with $n_xx + n_yy \le \beta$ has area $f$.

## The algorithm

```pseudo id=main
PLIC-ADVECT(F, Δt, K, u, v)
L1  for k ← 0 to K - 1
L2      for each sweep, x then y if k is even, else y then x
L3          for each mixed cell: n ← -∇F by Youngs' 3 × 3 stencil
L4          β ← the line constant with area{n·x ≤ β} = F, in closed form
L5          for each face: D ← upstream cell, A ← downstream cell, c ← |w| Δt / Δx
L6              q ← area of the fluid polygon of D in the strip of width c at the face
L7              F_D ← F_D - q;  F_A ← F_A + q        ▷ with all q from the old F
L8  return F
```

**The normal (line L3).** Youngs' stencil differences the fractions across the cell in each direction, with weights 1, 2, 1 across the other direction:

$$n_x = -\bigl[(F_{i+1,j+1} + 2F_{i+1,j} + F_{i+1,j-1}) - (F_{i-1,j+1} + 2F_{i-1,j} + F_{i-1,j-1})\bigr],$$

and $n_y$ is the same with the roles of $i$ and $j$ exchanged. The common factor $1/(8\Delta x)$ does not matter, since only the direction is used.

**The line constant (line L4).** Reflect the cell so that both components are nonnegative and scale them so that $m_1 + m_2 = 1$ with $m_1 \le m_2$. The area cut off by $m_1x + m_2y \le a$ is

$$A(a) = \begin{cases} a^2/(2m_1m_2), & 0 \le a \le m_1, \\ (a - m_1/2)/m_2, & m_1 \le a \le m_2, \\ 1 - (1 - a)^2/(2m_1m_2), & m_2 \le a \le 1, \end{cases}$$

the closed form of Scardovelli and Zaleski (2000). It is easy to invert: for $f \le \frac12$, $a = \sqrt{2m_1m_2f}$ if $f \le m_1/(2m_2)$ and $a = m_2f + m_1/2$ otherwise, and $f > \frac12$ follows from $A(1 - a) = 1 - A(a)$. Undoing the scaling and the reflection gives $\beta = (|n_x| + |n_y|)\,a + \min(n_x, 0) + \min(n_y, 0)$. In 3D the same idea gives a closed form with a cubic, and on other cell shapes an iteration is used.

**The flux (line L6).** For a face on the right of the donor, the fluid that crosses in one step is the fluid in the strip $1 - c \le x \le 1$ of the donor. The code clips the strip rectangle with the half-plane $n \cdot x \le \beta$ (the [Sutherland-Hodgman](/sutherland-hodgman/) step) and takes the area of the result by the [shoelace formula](/shoelace-formula/). Full and empty cells use $q = cF$. Lines L5 and L7 and the alternating sweeps are as on the [VOF page](/volume-of-fluid-method/).

## Example

**A line constant, by hand.** Let $n = (1, 2)$ and $f = 0.3$. Then $m_1 = \frac13$, $m_2 = \frac23$ and $m_1/(2m_2) = 0.25 < 0.3$, so $a = \frac23 \cdot 0.3 + \frac16 = 0.3667$ and $\beta = 3a = 1.1$. Check: the line $x + 2y = 1.1$ meets the side $x = 0$ at $y = 0.55$ and the side $x = 1$ at $y = 0.05$, so the fluid below it is a trapezoid of area $\frac12(0.55 + 0.05) = 0.3$.

**A flux, by hand.** Let a cell have $f = \frac18$ and $n = (1, 1)$, so the fluid is the triangle $x + y \le \frac12$ in the lower left corner. With $c = 0.3$ the strip $0.7 \le x \le 1$ at the right face holds no fluid, so $q = 0$; the upwind flux $cF$ would move 0.0375. With $c = 0.6$ the strip $0.4 \le x \le 1$ cuts off the corner $0.4 \le x \le 0.5$ of the triangle, a triangle with legs 0.1, so $q = 0.005$, against 0.075 for upwind.

**Rotation of a disk.** The same test as on the [VOF page](/volume-of-fluid-method/): a disk of radius 0.15 at $(0.5, 0.75)$ turns once with $\omega = 2\pi$, at a Courant number of at most about 0.48. The error is $\sum|F - F_0|\Delta x^2$ divided by the disk area, and a cell is smeared if $0.01 < F < 0.99$.

| $N$ | steps | method | relative $L^1$ error | smeared cells, start and end |
|---|---|---|---|---|
| 32 | 201 | donor-acceptor | 0.238 | 36, 50 |
| 32 | 201 | PLIC (Youngs) | 0.018 | 36, 36 |
| 64 | 402 | donor-acceptor | 0.123 | 76, 153 |
| 64 | 402 | PLIC (Youngs) | 0.0058 | 76, 74 |

PLIC is 13 to 21 times more accurate, the interface stays exactly one cell thick, and the error falls by a factor of 3.2 when the grid is refined. Translating the same disk along the diagonal for one period at $N = 32$ ($c = 0.5$) gives a relative error of 0.0091, against 0.181 for donor-acceptor. In all runs the volume stayed constant to $10^{-16}$ and every $F$ stayed in $[0, 1]$. The run at $N = 64$ took about 2 s in pure Python.

## Correctness

The [proof file](proofs/correctness/) shows three exact facts. The line constant of line L4 cuts off exactly the area $F$, for every normal and every $F \in [0, 1]$, so the reconstruction keeps the volume of every cell. The geometric flux lies in $[\max(0, c - (1 - F)), \min(c, F)]$, since the strip is part of the cell; with divergence-free sweeps this gives exact conservation and $0 \le F \le 1$, as for donor-acceptor. A band at least two cells wide is moved exactly, because the stencil then finds the exact normal. The tests also check the closed form against the polygon area to $10^{-14}$ on 3000 random cases.

## Complexity

Each mixed cell costs $O(1)$: a 9-point stencil, a square root, and the clipping of a 4-vertex polygon. Full and empty cells cost a multiplication. So a sweep costs $\Theta(N^2)$ and a run $\Theta(KN^2)$, with $\Theta(N^2)$ memory; the constant is several times that of donor-acceptor, but only the $O(N)$ mixed cells pay it. In 3D the polyhedron clipping is more costly, and it is often the most expensive part of the VOF step.

## Properties

- **Exact volume.** Each reconstruction holds exactly the fraction $F$ of its cell, and the fluxes move volume between neighbors, so the total is kept to rounding.
- **Sharp.** The interface stays one cell thick, as the rotation table shows.
- **Not continuous.** The lines of neighboring cells do not meet in general. The interface is a set of separate segments, which is enough for fluxes but not for curvature.
- **Order of the normal.** Youngs' normal does not reproduce a straight line at every angle, so the reconstruction is first order in the sense of Pilliod and Puckett (2004). Methods that fit the line to the $3 \times 3$ block, such as ELVIRA, reproduce every straight line and are second order.
- **Bounded** for divergence-free sweeps with $c \le 1$, as for donor-acceptor.

## Variants and improvements

- **Better normals.** ELVIRA of Pilliod and Puckett (2004) tries several candidate normals from the $3 \times 3$ block and keeps the one whose extended line best matches the neighbor fractions; LVIRA minimizes the same error by iteration. Mixed Youngs-centered schemes are used in 3D codes.
- **Unsplit advection.** Rider and Kothe (1998) trace the region that crosses each face in a step back along the velocity and intersect it with the reconstruction, which removes the splitting error.
- **Lagrangian-explicit sweeps.** Some codes move the reconstructed line with the flow in each sweep instead of cutting strips, and combine the two kinds of sweeps so that the volume is kept for any divergence-free velocity.
- **Moment of fluid.** The cell stores the centroid of the fluid as well as its volume, which fixes the normal without the neighbors and resolves thin films.
- **Curvature.** The PLIC lines are not used for curvature. Codes compute it from height functions, sums of $F$ along columns, or from a coupled [level set](/level-set-method/), and add surface tension by the [continuum surface force](/continuum-surface-force/) model.

## When to use it

Use PLIC whenever a VOF code needs a sharp interface: breaking waves, jets, sprays and bubbly flows with surface tension. It is the standard reconstruction in geometric VOF codes. Algebraic VOF schemes, which compress the profile of $F$ without a line, are simpler on unstructured meshes and are used where some smearing is acceptable. If smooth normals and curvature are the main need, a [level set](/level-set-method/) or [front tracking](/front-tracking-method/) is easier.

## Pitfalls

- **Isolated and thin features.** A filament thinner than a cell has fluid on both sides of the cell, which one line cannot represent. Youngs' stencil then gives a poor normal, and the filament breaks into small pieces.
- **A zero normal.** A mixed cell with symmetric neighbors gives $\nabla F = 0$. Fall back to an upwind flux, as the code does.
- **Rounding at the limits.** Fractions such as $10^{-15}$ or $1 - 10^{-15}$ give lines at the edge of the cell. Treat them as empty or full, and clamp the flux to its exact bounds.
- **Splitting error.** With a general divergence-free velocity, each split sweep has a divergence, and $F$ can leave $[0, 1]$ unless the sweep includes a divergence correction.
- **Normal sign.** The normal must point out of the fluid, $n = -\nabla F$. With the other sign the line cuts off the void instead of the fluid, and the volume of the cell is still right, so the error does not show in a volume check. The band test catches it.

## Implementations

## History

The SLIC method of Noh and Woodward (1976) used lines aligned with the grid. Youngs (1982) gave the first widely used method with a sloped line in each cell and a normal from the $3 \times 3$ block, for multi-material flows with large distortion. Rider and Kothe (1998) and Scardovelli and Zaleski (1999) reviewed the field and made PLIC with geometric fluxes the standard. Scardovelli and Zaleski (2000) published the closed-form link between the line position and the volume fraction, which replaced iterative searches, and Pilliod and Puckett (2004) showed which normals give second-order reconstructions.

## References
