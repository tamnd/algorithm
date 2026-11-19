---
tag: TBCGQZ
kind: algorithm
slug: volume-of-fluid-method
name: Volume of fluid method
aliases:
- VOF method
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: Tracks a free surface by the fraction of each cell filled with one fluid, advected conservatively and reconstructed as an interface.
solves: [advection-equation]
model: real-ram
complexity:
  vars: {N: "the number of cells along each side of the grid", K: "the number of time steps"}
  time: {worst: "Θ(K N^2)"}
  space: {extra: "Θ(N^2)"}
properties: {deterministic: true, eulerian: true, conserves_volume_exactly: true, bounded: "0 <= F <= 1 for divergence-free sweeps with Courant number at most 1", operator_split: true}
history:
  year: 1981
  people: [Cyril W. Hirt, Billy D. Nichols]
  note: "Hirt and Nichols (1981) named the method and gave the donor-acceptor flux in the SOLA-VOF code. Noh and Woodward (1976) had used cell fractions with interfaces aligned with the grid (SLIC). Youngs (1982) put a sloped line in each cell, which led to PLIC."
prereqs: [advection-equation, finite-volume-method, upwind-scheme, operator-splitting]
see_also: [piecewise-linear-interface-calculation, level-set-method, front-tracking-method, continuum-surface-force, marker-and-cell-method, particle-level-set, ghost-fluid-method, marching-squares]
sources:
  - paper: doi:10.1016/0021-9991(81)90145-5
    title: "C. W. Hirt and B. D. Nichols, Volume of fluid (VOF) method for the dynamics of free boundaries, Journal of Computational Physics 39 (1981) 201-225"
    locator: "the fractional volume function, the donor-acceptor flux and the choice between the acceptor and donor fraction"
  - paper: doi:10.1006/jcph.1998.5906
    title: "William J. Rider and Douglas B. Kothe, Reconstructing volume tracking, Journal of Computational Physics 141 (1998) 112-152"
    locator: "the review of volume tracking methods and the rotation and shear test problems"
  - paper: doi:10.1146/annurev.fluid.31.1.567
    title: "Ruben Scardovelli and Stéphane Zaleski, Direct numerical simulation of free-surface and interfacial flow, Annual Review of Fluid Mechanics 31 (1999) 567-603"
    locator: "the section on volume of fluid methods"
---

The volume of fluid (VOF) method follows the surface of a liquid on a fixed grid by storing, in each cell, the fraction $F$ of the cell that is filled with liquid: 1 in the liquid, 0 in the air, and a value in between in the cells that the surface cuts. Each time step moves liquid between cells through their faces, so no liquid is created or lost. In fluid animation the surface is more often tracked with a [level set](/level-set-method/) or with marker particles, because they give a smooth surface for rendering, and VOF is the usual choice in engineering codes. What the accurate method adds is exact conservation of the liquid volume to rounding error, the bound $0 \le F \le 1$ by construction, and geometric fluxes that keep the surface within one or two cells instead of letting it spread.

## In plain words

Think of a grid laid over a glass of water. For every square of the grid, write down how full it is with water, from 0 to 1. That table of numbers is all the method stores. To move the water, look at each wall between two squares and ask how much water crosses it in one time step. The squares far from the surface are full or empty, so that is easy. Near the surface the answer depends on where the water is inside the square, which the numbers alone do not say. The donor-acceptor rule of Hirt and Nichols guesses the shape from the neighbors: if the surface faces the flow, the water at the front leaves only after the air in front of it has gone. Water moves only from one square to the next, so the total is exact.

## The problem

Given volume fractions $F_{ij} \in [0, 1]$ on an $N \times N$ periodic grid of cells of side $\Delta x = 1/N$ over the unit square, and a velocity field $(u, v)$ with zero divergence, approximate the solution of the [advection equation](/advection-equation/)

$$\partial_tF + u\,\partial_xF + v\,\partial_yF = 0$$

for $F$ the indicator of the liquid, after $K$ steps of size $\Delta t$. The output must keep $\sum F_{ij}\Delta x^2$, the liquid volume, and stay in $[0, 1]$. The velocity is given on cell faces as $u(y)$ on the faces normal to $x$ and $v(x)$ on the faces normal to $y$. Solid body rotation $u = -\omega(y - \frac12)$, $v = \omega(x - \frac12)$ and uniform translation are of this form. The grid index $i$ is along $x$ and $j$ along $y$.

## The algorithm

```pseudo id=main
VOF-ADVECT(F, Δt, K, u, v)
L1  for k ← 0 to K - 1
L2      for each sweep, x then y if k is even, else y then x   ▷ operator splitting
L3          for each face: D ← upstream cell, A ← downstream cell   ▷ donor and acceptor
L4          c ← |w| Δt / Δx                              ▷ w is the face velocity, c ≤ 1
L5          F_AD ← F_A if the interface in D is normal to the sweep, else F_D
L6          q ← min(F_AD c + max((1 - F_AD) c - (1 - F_D), 0), F_D)
L7          F_D ← F_D - q;  F_A ← F_A + q               ▷ with all q from the old F
L8  return F
```

Each step is split into two one-dimensional sweeps, and the order of the sweeps alternates between steps (line L2), which removes the bias of a fixed order. In a sweep, every face has a donor cell upstream and an acceptor cell downstream (line L3). The quantity $c$ of line L4 is the Courant number of the face, the fraction of a cell width that crosses the face in one step.

Line L5 decides how the fluid is laid out in the donor. The donor-acceptor rule compares the change of $F$ across the donor in the two directions, using the neighbors on both sides. If $F$ changes more along the sweep, the interface is roughly normal to the flow, and the acceptor fraction $F_A$ is used; this makes the flux depend on what lies downstream, so a front moves as a sharp step. If $F$ changes more across the sweep, the interface is parallel to the flow, and the donor fraction $F_D$ is used, as in the [upwind scheme](/upwind-scheme/).

Line L6 is the flux of Hirt and Nichols, as a fraction of the cell volume. The term $F_{AD}c$ is the guess. The term $\max((1 - F_{AD})c - (1 - F_D), 0)$ adds the fluid that must cross if the void that the guess sends, $(1 - F_{AD})c$, is more than the void the donor holds. The minimum with $F_D$ stops the donor from giving more fluid than it has. Line L7 moves $q$ from the donor to the acceptor. All fluxes of a sweep are computed from the fractions before the sweep.

## Example

**A band, by hand.** Take $N = 20$, so $\Delta x = 0.05$, and liquid in the band $0.2 < x < 0.5$ for all $y$. Cells $i = 4$ to $9$ are full and the rest are empty. Let $u = 1$, $v = 0$ and $\Delta t = 0.015$, so $c = 0.3$. In the first sweep every donor is full or empty, so $q = 0.3$ for faces with a full donor and $q = 0$ for faces with an empty one. Cell 4 gives 0.3 and gets nothing, cell 10 gets 0.3 from cell 9, and the row of cells 3 to 11 becomes

$$0,\ 0.7,\ 1,\ 1,\ 1,\ 1,\ 1,\ 0.3,\ 0.$$

The second step shows the difference from upwind. At the front face between cells 10 and 11, the donor has $F_D = 0.3$ and $F$ changes along $x$, so line L5 takes the empty acceptor, $F_{AD} = 0$. Line L6 gives $q = \min(0 + \max(0.3 - 0.7, 0), 0.3) = 0$: the cell holds 0.7 of void ahead of its liquid, and only 0.3 of a cell crosses the face. At the back face between cells 4 and 5, $F_D = 0.7$ and the acceptor is full, so $q = \min(0.3, 0.7) = 0.3$. The row becomes

$$0,\ 0.4,\ 1,\ 1,\ 1,\ 1,\ 1,\ 0.6,\ 0,$$

the exact fractions of the band $0.23 < x < 0.53$. Upwind fluxes $q = cF_D$ give $0, 0.49, 0.91, 1, 1, 1, 1, 0.51, 0.09$ instead: liquid already leaks into cell 11 and the band spreads. The tests check that donor-acceptor moves the band exactly for 7 steps in both directions.

**Rotation of a disk.** A disk of radius 0.15 at $(0.5, 0.75)$ turns once around the center of the unit square with $\omega = 2\pi$, the Courant number is at most about 0.48, and the result is compared with the start. The error is the $L^1$ distance $\sum|F - F_0|\Delta x^2$ divided by the disk area, and a cell is counted as smeared if $0.01 < F < 0.99$.

| $N$ | steps | scheme | relative $L^1$ error | smeared cells, start and end |
|---|---|---|---|---|
| 32 | 201 | donor-acceptor | 0.238 | 36, 50 |
| 32 | 201 | upwind | 1.314 | 36, 898 |
| 64 | 402 | donor-acceptor | 0.123 | 76, 153 |
| 64 | 402 | upwind | 1.041 | 76, 2187 |

Donor-acceptor keeps the surface within a band one to two cells wide, and the error halves when the grid is refined, first order. Upwind smears the disk over most of the domain; an error above 1 means that more liquid is out of place than the disk holds. Translating the same disk along the diagonal for one period at $N = 32$ ($c = 0.5$, 64 steps) gives a relative error of 0.181 with donor-acceptor, with 36 smeared cells at both ends, and 1.103 with upwind, with 540 smeared cells. In all runs the volume stayed constant to $10^{-14}$ and every $F$ stayed in $[0, 1]$.

## Correctness

The [proof file](proofs/correctness/) shows three exact facts for $0 \le c \le 1$. First, the flux of line L6 lies between $\max(0, c - (1 - F_D))$ and $\min(c, F_D)$: the donor never gives more liquid than it holds or more void than it holds. Second, when the velocity along each line of cells is constant, as for $u = u(y)$ and $v = v(x)$, a sweep keeps the sum of the fractions and keeps every fraction in $[0, 1]$, so the whole run conserves volume and stays bounded. Third, a band whose width and gap are both at least $2\Delta x$ is moved exactly. The accuracy for curved shapes is measured, not proved.

## Complexity

A sweep visits each of the $N^2$ faces in its direction once, and each face costs $O(1)$: a few neighbor values for line L5 and the formula of line L6. So a step costs $\Theta(N^2)$ and a run $\Theta(KN^2)$. The method keeps one extra copy of the grid, $\Theta(N^2)$ memory. In a flow solver the stable time step is set by $c \le 1$ (in practice $c \le 0.5$), so $K$ grows like $N$ for a fixed end time and a run costs $\Theta(N^3)$ in 2D. The pressure solve of the flow usually costs more than the VOF advection.

## Properties

- **Exact conservation.** Liquid moves only through faces, from one cell to its neighbor, so the total volume changes only by rounding.
- **Bounded** when each sweep is divergence free and $c \le 1$. For a general velocity, splitting makes each sweep compressible and $F$ can leave $[0, 1]$ slightly; codes then clip or redistribute.
- **Sharp but not smooth.** The surface stays within one or two cells, but the method stores no position inside the cell, so normals and curvature must be computed from the fractions.
- **Topology changes are free.** Drops merge and break without any special treatment, because only fractions are stored.
- **First-order accurate** for curved interfaces with the donor-acceptor flux, as the rotation table shows. The interface becomes ragged, with small pieces of liquid left behind (flotsam).

## Variants and improvements

- **[PLIC](/piecewise-linear-interface-calculation/).** Youngs (1982) and later work reconstruct the interface in each cell as a straight line with normal from the gradient of $F$, placed to cut off the volume $F$, and compute the fluxes as the area of the polygon that crosses each face. This is the standard in modern VOF codes and is second order for smooth interfaces.
- **SLIC.** The simple line interface calculation of Noh and Woodward (1976) places a line parallel to a cell face, chosen per sweep. It is close to the donor-acceptor rule.
- **Unsplit schemes.** Rider and Kothe (1998) trace the backward flux regions in two dimensions at once, which removes the splitting error and the compressible sweeps.
- **Algebraic VOF.** Codes such as those with compressive interface capturing do not reconstruct a line. They advect $F$ with a high-resolution scheme and add a compressive term or a limiter that steepens the profile. They are simpler on unstructured meshes but less sharp.
- **Coupled methods.** VOF is often combined with a [level set](/level-set-method/) (CLSVOF): the level set gives normals and curvature, and VOF gives conservation.
- **Surface tension** enters through the [continuum surface force](/continuum-surface-force/) model, with the curvature computed from $F$.

## When to use it

Use VOF when liquid volume must be conserved over a long run: breaking waves, sloshing, jets that break into drops, filling of molds, and boiling with many bubbles. It handles merging and breakup without bookkeeping, and it works with any grid flow solver. Use a [level set](/level-set-method/) when smooth normals and curvature matter more than exact volume, as in many surface tension problems, and [front tracking](/front-tracking-method/) when the interface must stay sharp and its shape must be known to high accuracy. For animation, level sets with particles are the usual choice because the rendered surface comes directly from a smooth function.

## Pitfalls

- **Expecting a smooth surface.** The fractions do not define a unique interface. Curvature from second differences of $F$ is very noisy; smooth $F$ first, or use height functions.
- **Courant number above 1.** The bounds of the flux need $c \le 1$, and with split sweeps the limit applies to each sweep. In practice $c \le 0.5$ is used because the velocity changes during a step.
- **Splitting a compressible sweep.** For a general divergence-free velocity, each one-dimensional sweep has a divergence, and the fractions can rise above 1. The usual fix adds a correction term $F\,\partial_xu\,\Delta t$ to each sweep, or clips and redistributes the excess.
- **Fixed sweep order.** Always sweeping $x$ first gives a bias that turns a rotating shape. Alternate the order, as on line L2.
- **Reading volume errors as success.** Exact conservation does not mean accuracy: upwind also conserves the volume exactly, but the table shows that it smears the disk over the domain.
- **Too few cells per drop.** A drop that covers only a few cells breaks into flotsam. Resolve the smallest feature with at least four to eight cells.

## Implementations

## History

Noh and Woodward (1976) advected cell fractions with interfaces aligned to the grid in their SLIC method. Hirt and Nichols (1981) introduced the name volume of fluid, the donor-acceptor flux and the SOLA-VOF code for free-surface flows at Los Alamos; it became one of the most cited papers in computational fluid dynamics. Youngs (1982) placed a sloped line in each cell, the start of PLIC. In the 1990s, papers such as Rider and Kothe (1998) and the review of Scardovelli and Zaleski (1999) made geometric VOF with PLIC reconstruction and the continuum surface force model the standard for direct simulation of flows with interfaces.

## References
