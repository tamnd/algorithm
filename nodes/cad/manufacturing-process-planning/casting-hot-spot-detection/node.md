---
tag: NAYQYF
kind: algorithm
slug: casting-hot-spot-detection
name: Casting hot spot detection
aliases:
- thermal centre detection
area: cad/manufacturing-process-planning
level: advanced
summary: Finds the last regions of a casting to solidify, as maxima of a distance transform or by vector element methods, so risers can be placed to feed them.
model: real-ram
complexity:
  vars: {N: "number of cells of the grid", k: "number of axes of the grid (2 or 3)"}
  time: {worst: "O(3^k N)"}
  space: {extra: "O(N)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1996
  people: [B. Ravi, M. N. Srinivasan]
  note: Foundry engineers located hot spots by hand with the largest circle that fits in a section. Ravi and Srinivasan (1996) computed them on a solid model with the modulus vector method. The exact grid distance transform used here is the method of Felzenszwalb and Huttenlocher.
prereqs: [distance-transform, chvorinov-rule]
see_also: [felzenszwalb-distance-transform, medial-axis, riser-design-modulus-method, heat-equation, finite-difference-method, finite-element-method, conformal-cooling-design]
sources:
  - paper: doi:10.1080/13640461.1996.11819638
    title: B. Ravi and M. N. Srinivasan, Casting solidification analysis by modulus vector method, International Journal of Cast Metals Research 9(1), 1996, 1 to 7
    locator: the modulus vector at points of a casting from its geometry, and the hot spots found by following these vectors (general locator)
  - paper: doi:10.4086/toc.2012.v008a019
    title: Pedro F. Felzenszwalb and Daniel P. Huttenlocher, Distance transforms of sampled functions, Theory of Computing 8(19), 2012, 415 to 428
    locator: the lower envelope of parabolas for the one-dimensional squared distance transform in linear time, and its use one axis at a time in higher dimensions
  - book: isbn:9780444635099
    title: John Campbell, Complete Casting Handbook, 2nd edition, Butterworth-Heinemann, 2015
    locator: the chapter on feeding, the hot spots at junctions and the largest inscribed circle as a guide to them (general locator)
---

Casting hot spot detection finds the regions of a casting that solidify last. Shrinkage porosity forms there unless a riser feeds them, so they decide where the risers go. The exact answer comes from a thermal simulation, a solution of the [heat equation](/heat-equation/) with latent heat over the casting and the mold. A fast geometric proxy is the distance from each point of the casting to the mold: points far from the mold lose heat last, and the local maxima of this distance lie on the [medial axis](/medial-axis/) of the casting. This page computes the proxy on a voxel grid: an exact squared Euclidean [distance transform](/distance-transform/) by the method of [Felzenszwalb and Huttenlocher](/felzenszwalb-distance-transform/), with integer arithmetic, followed by the regional maxima of the distance. It runs in $O(N)$ time for a fixed dimension. The maxima are a geometric proxy, not a thermal solution, and the page shows where the proxy and [Chvorinov's rule](/chvorinov-rule/) disagree.

## In plain words

Metal in a mold cools from the outside in. The last spots to turn solid are the ones deepest inside the metal, far from the cold mold. Those spots shrink without any liquid left nearby to fill them, so holes form there. A foundry engineer wants to know where these spots are, to put an extra reservoir of liquid metal next to each.

The method cuts the casting into small cubes, measures for each cube how far it is from the nearest piece of mold, and reports the cubes that are farther than all cubes around them. Those are the likely last spots. It is a quick guess from the shape alone. A heat flow simulation gives the true answer.

## The problem

**Input.** A grid of cells with $k$ axes, usually $k = 3$ for a solid or $k = 2$ for a section, in which each cell is metal or mold. At least one cell is mold. In practice, the voxelized casting is surrounded by a layer of mold cells.

**Output.**

- For every cell $x$, $D(x) = \min_{y \text{ mold}} \lVert x - y \rVert^2$, the squared Euclidean distance between cell centres, as an exact integer.
- The regional maxima of $D$ over the metal cells. A *plateau* is a maximal connected set of metal cells with one value $c$ of $D$, where two cells are connected when they differ by at most 1 in every index (8 neighbours in 2D, 26 in 3D). A plateau is a *regional maximum* when every cell next to it has $D < c$. These are the hot spot candidates, sorted by $D$ from the largest.

**What the distance measures.** $\sqrt{D(x)}$ is the distance from the centre of $x$ to the centre of the nearest mold cell. The surface of the casting lies half a cell from the centres of the mold cells next to it, so the distance to the surface is about $\sqrt{D(x)} - \frac12$ cells. The squares are kept because they are integers, and taking the square root does not change the order.

## The algorithm

```pseudo id=main
HOT-SPOTS(grid)
L1  f(x) ← 0 for each mold cell x, and ∞ for each metal cell
L2  for each axis a = 1, ..., k
L3      for each line of cells along axis a: replace f on the line by LOWER-ENVELOPE(f on the line)
L4  D ← f
L5  group the metal cells into plateaus of equal D, connected under the full neighbourhood
L6  keep a plateau if every cell next to it has a smaller D
L7  return the kept plateaus with their values, the largest first
```

**LOWER-ENVELOPE at line L3.** For a line $f(0), \dots, f(n-1)$ it returns $d(q) = \min_p \bigl((q - p)^2 + f(p)\bigr)$. Each $p$ with a finite $f(p)$ gives a parabola $P_p(u) = (u - p)^2 + f(p)$, and $d$ is their lower envelope at the integers. All parabolas have the same shape, so two of them, $p < r$, cross at exactly one point,

$$s(p, r) = \frac{\bigl(f(r) + r^2\bigr) - \bigl(f(p) + p^2\bigr)}{2(r - p)},$$

and $P_r$ is lower to the right of it. The procedure goes through the points in order and keeps a stack of the parabolas of the envelope with the points where each starts. Before it pushes $r$, it pops the top parabola $v$ while $s(v, r)$ is at or before the start of $v$, since $P_r$ is then lower on the whole interval of $v$. A second pass reads off $d(q)$ from the interval that holds $q$. Each point is pushed and popped at most once, so the time is $O(n)$.

The crossing points are fractions with integer numerators and positive denominators, and the implementation compares them by cross multiplication, with no division. So the transform is exact: no rounding can change a distance or the order of two distances.

**Lines L2 to L4.** The squared distance is a sum over the axes, so the minimum over all mold cells splits into one minimum per axis. After the pass over axis 1, $f(x)$ is the squared distance to the nearest mold cell on the line of $x$ along axis 1. After the pass over axis 2, it is the distance to the nearest mold cell in the plane of $x$ spanned by axes 1 and 2, and so on.

**Lines L5 and L6.** A graph search from each metal cell not yet seen collects the cells of its plateau, and on the way looks at every neighbour. The plateau is kept if no neighbour has a larger $D$.

## Example

A 2D section with a block of $5 \times 5$ cells joined by a bar one cell thick to a boss of $3 \times 3$ cells, with mold around it (`#` is metal and `.` is mold):

```
.............
.#####.......
.#####..###..
.###########.
.#####..###..
.#####.......
.............
```

The values of $D$ on the middle row are

| column | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $D$ | 0 | 1 | 4 | 9 | 5 | 2 | 1 | 1 | 2 | 4 | 2 | 1 | 0 |

The cell $(3, 4)$ has $D = 5$: its nearest mold cells are $(2, 6)$ and $(4, 6)$, one row and two columns away, beside the start of the bar, so $1^2 + 2^2 = 5$. The algorithm returns two hot spots: $D = 9$ at $(3, 3)$, the centre of the block, and $D = 4$ at $(3, 9)$, the centre of the boss. The bar between them has $D = 1$, so it freezes first and cuts the boss off from the block. A riser on the block does not feed the boss, which needs its own riser or a thicker connection. This is the reasoning of feeding design in [riser design by the modulus method](/riser-design-modulus-method/).

## Correctness

The proof in the proofs folder has three steps. First, two parabolas of the line meet once, so the stack procedure keeps the invariant that its stack function equals the lower envelope of the parabolas seen so far, and the read-out is exact at every integer. Second, after the passes over the axes $1, \dots, a$, each cell holds the squared distance to the nearest mold cell that agrees with it in the other coordinates; for $a = k$ this is the full distance. Third, every metal cell has $D \ge 1$ and every mold cell has $D = 0$, so the graph search collects exactly the plateaus, and the test of line L6 is the definition of a regional maximum.

The tests compare the transform with a brute force minimum over all mold cells, on random grids in 1, 2, 3 and 4 dimensions. They compare the hot spots with a second definition: a metal cell is in a regional maximum if and only if the connected part of the set $\{y : D(y) \ge D(x)\}$ that holds $x$ has no cell with a larger value.

## Complexity

Each pass of lines L2 and L3 calls LOWER-ENVELOPE on lines that together hold every cell once, in $O(N)$ time, so the transform costs $O(kN)$. Lines L5 and L6 visit each metal cell once and look at its $3^k - 1$ neighbours, in $O(3^k N)$ time. The total is $O(3^k N)$, which is $O(N)$ for $k = 2$ or $3$. The extra space is the array of distances and the search stack, $O(N)$.

## Properties

- **Exact.** All values are integers, and the breakpoints of the envelope are compared by cross multiplication, so the distances and their order are exact.
- **Deterministic.** The plateaus come out sorted by value, and ties by their first cell.
- **A proxy.** The result depends only on the shape. It does not know the metal, the mold material, chills, sleeves, the gating, or the heat that a thin core receives from both sides.
- **Resolution.** The distances are between cell centres, so a feature thinner than a cell is lost, and the position of a hot spot is known to a cell.

## Variants and improvements

- **The modulus instead of the distance.** By [Chvorinov's rule](/chvorinov-rule/), freezing time grows with the modulus $V/A$, not with the distance to the mold. The two agree in their order for sections of one shape, but not across shapes. For a plate of thickness $T$, the largest distance is $T/2$ and the modulus is $T/2$. For a long square bar of side $a$, they are $a/2$ and $a/4$; for a long cylinder of radius $r$, $r$ and $r/2$; for a sphere of radius $r$, $r$ and $r/3$. So a plate with $T = 2$ cm (distance 1, modulus 1) and a sphere with $r = 1.5$ cm (distance 1.5, modulus 0.5) are ranked in opposite orders: the distance says that the sphere freezes last, and the rule says that the plate does.
- **Modulus vector method.** Ravi and Srinivasan compute at points of the casting a vector from the geometry around them, in the direction in which the local modulus grows, and follow these vectors to the hot spots. This uses more of the shape than the distance to the nearest point of the mold.
- **Thermal simulation.** A solution of the heat equation with latent heat, by the [finite difference method](/finite-difference-method/) on the same voxel grid or the [finite element method](/finite-element-method/) on a mesh, gives the last points to freeze directly, and also handles the mold, chills and the alloy. It costs much more and needs material data.
- **Other distance transforms.** A chamfer distance with integer weights is faster to code but not Euclidean, and its maxima move on diagonal sections. A distance on a tetrahedral mesh or on the solid model, through its [medial axis](/medial-axis/), avoids the voxel resolution.
- **Distance to the cooling surface only.** Faces against an insulating sleeve or another section of the casting do not cool. Marking them as metal, not mold, before the transform moves the hot spots towards them, in the same way as the modulus method leaves such faces out of $A$.

## When to use it

Use it early in casting design, on a voxel model, to see quickly where the thick regions are and which of them are cut off from each other by thin sections. It is a good start for the placement of risers and for the zones of the modulus method. Do not use it to size risers, and check the final design with a simulation.

## Pitfalls

- **Treating the maxima as the thermal answer.** The distance ignores how much metal is around a point, the heating of the mold in concave corners, cores with metal on both sides, and all process data. Inside corners and junctions are worse than their distance says.
- **No mold layer.** If the casting touches the edge of the grid, the edge is not mold, and the distances there are too large. Pad the grid with mold cells.
- **Plateaus.** Plates and long bars of even thickness give large flat plateaus or ridges of equal distance, not single points. A riser can sit anywhere along them, and a step in thickness of one cell can split or join them.
- **Small maxima from noise.** A voxelized surface has steps that make small regional maxima of low value. Ignore maxima below a threshold, or keep only those whose value is much larger than the surroundings.

## Implementations

## History

Before computers, foundry engineers found hot spots at junctions by drawing the largest circle that fits in the section, since the junction of two walls holds a larger circle than either wall. Ravi and Srinivasan (1996) computed hot spots on solid models with the modulus vector method. The squared Euclidean distance transform in linear time, by the lower envelope of parabolas one axis at a time, is due to Felzenszwalb and Huttenlocher, in a report of 2004 and in Theory of Computing in 2012.

## References
