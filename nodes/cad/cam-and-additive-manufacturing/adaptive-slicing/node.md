---
tag: BT4MQH
kind: algorithm
slug: adaptive-slicing
name: Adaptive slicing
aliases:
- adaptive layer thickness
area: cad/cam-and-additive-manufacturing
level: core
summary: Chooses each layer thickness from the local slope of the surface so the cusp height stays below a bound, thin layers on sloped parts and thick ones elsewhere.
solves: [slicing-for-additive-manufacturing]
model: real-ram
complexity:
  vars: {n: number of facets, L: number of layers, r: number of allowed thicknesses}
  time: {worst: "O(L r n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1994
  people: [Atanas Dolenc, Ismo Mäkelä]
  note: Dolenc and Mäkelä defined the cusp height and chose each layer thickness to keep it under a bound. Sabourin, Houser and Bøhn refined thick slabs in 1996, and Tyberg and Bøhn made the thickness local to each part of a layer in 1998.
prereqs: [staircase-effect, triangle-mesh-slicing]
see_also: [slicing-for-additive-manufacturing, scallop-height, build-orientation, surface-curvature, greedy-choice-property, principle-of-optimality]
sources:
  - paper: doi:10.1016/0010-4485(94)90032-9
    title: Atanas Dolenc and Ismo Mäkelä, Slicing procedures for layered manufacturing techniques, Computer-Aided Design 26(2), 1994, 119 to 126
    locator: the definition of the cusp height and the choice of the layer thickness from it
  - paper: doi:10.1108/13552549610153370
    title: Emmanuel Sabourin, Scott A. Houser and Jan Helge Bøhn, Adaptive slicing using stepwise uniform refinement, Rapid Prototyping Journal 2(4), 1996, 20 to 26
    locator: the method that slices at the largest thickness and then reslices the slabs that need it
  - paper: doi:10.1108/13552549810222993
    title: Justin Tyberg and Jan Helge Bøhn, Local adaptive slicing, Rapid Prototyping Journal 4(3), 1998, 118 to 127
    locator: the layer thickness chosen separately for each part of a layer
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the chapters on the process chain and on design for additive manufacturing (layer thickness and stair stepping)
---

Adaptive slicing chooses the thickness of each layer of a printed part from the slope of the surface at that height. On a surface that is close to horizontal, a thick layer leaves a large step, so the layer must be thin. On a vertical wall, the step is zero, so the layer can be as thick as the machine allows. The measure is the cusp height $t\,|\cos\theta|$ of Dolenc and Mäkelä (1994), where $t$ is the layer thickness and $\theta$ is the angle between the surface normal and the build direction (see [staircase effect](/staircase-effect/)). The method on this page goes up from the bottom of a triangle mesh and gives each layer the largest allowed thickness for which every facet in the layer has cusp height at most a bound $c$. The layers it returns are then cut by [triangle mesh slicing](/triangle-mesh-slicing/).

## In plain words

A printer builds a part as a stack of flat layers. Where the surface slopes gently, each layer sticks out past the one above it, and the surface looks like a flight of stairs. Thin layers make small stairs but take a long time to print. Thick layers are fast but rough.

Adaptive slicing uses thin layers only where they help. At each height it looks at the part of the surface that the next layer would cover. It tries the thickest layer first. If any piece of surface in that layer would have a step that is too tall, it tries the next thinner layer, and so on. On steep walls it can use thick layers, and near the top of a dome it uses thin ones.

## The problem

The input is a closed triangle mesh with outward facet normals $n_f$ (not necessarily of unit length), a finite set of allowed thicknesses $t_1 < t_2 < \dots < t_r$, and a cusp bound $c > 0$. The build direction is $+z$. The output is a sequence of layer boundaries $z_0 < z_1 < \dots < z_L$ with $z_0$ the lowest point of the mesh, $z_L$ at or above the highest point, and each $z_i - z_{i-1}$ an allowed thickness.

A facet $f$ lies in the layer from $z$ to $z + t$ if it meets the open slab $z < Z < z + t$, that is, if $z_{\min}(f) < z + t$ and $z_{\max}(f) > z$. Its cusp height in that layer is
$$\text{cusp}(f, t) = t\,|\cos\theta_f| = t\,\frac{|n_{f,z}|}{\|n_f\|}.$$
A layer is feasible if every facet in it has $\text{cusp}(f, t) \le c$. Both sides are non-negative, so the test is the same as
$$t^2\, n_{f,z}^2 \le c^2\, \|n_f\|^2,$$
which uses no square root and is exact for integer or rational input. A facet that only touches the slab at $z$ or at $z + t$ does not count. A horizontal facet that lies at a layer boundary is reproduced exactly, but a horizontal facet strictly inside a layer has cusp height $t$.

## The algorithm

```pseudo id=main
ADAPTIVE-SLICE(M, T, c)          ▷ mesh M, thicknesses t_1 < ... < t_r, bound c
L1  z ← zmin(M)
L2  while z < zmax(M) do
L3      t ← t_1                                   ▷ fallback if nothing is feasible
L4      for s ← t_r, t_(r-1), ..., t_1 do
L5          if FEASIBLE(z, s) then t ← s; break
L6      z ← z + t; output z                       ▷ one layer from z − t to z
L7  return the outputs

FEASIBLE(z, s)
L8  for each facet f with normal n do
L9      if zmin(f) < z + s and zmax(f) > z and s² n_z² > c² |n|² then
L10         return false
L11 return true
```

Line L4 tries the thicknesses from the largest down. Line L5 stops at the first feasible one, which is the largest feasible one, because feasibility is monotone in the thickness (see Correctness). If even $t_1$ is not feasible, for example because a horizontal facet lies inside the layer and $t_1 > c$, line L3 keeps $t_1$. The layer then breaks the bound, and a slicer should report it. The last layer can end above the top of the part.

**Exact arithmetic.** The only decision is the comparison of line L9. With integer or rational vertices, the normal $n$ is exact, and so are $n_z^2$ and $\|n\|^2$. In floating point, the usual code computes $|\cos\theta| = |n_z| / \|n\|$ with a square root and compares $t\,|\cos\theta|$ with $c$. When the two sides are equal or nearly equal, as for a facet whose slope exactly allows a given thickness, rounding can pick the next thinner layer or accept a layer that breaks the bound by one rounding error. The squared form decides these ties exactly.

## Example

Take a house: the box $[0, 4] \times [0, 4] \times [0, 2]$ with a pyramid roof whose apex is $(2, 2, 3)$, as 14 triangles. The allowed thicknesses are $\tfrac14, \tfrac12, 1$, and $c = \tfrac14$. The walls have $n_z = 0$. The bottom face is horizontal at $z = 0$ and never lies inside a slab. A roof facet such as $(0, 0, 2), (4, 0, 2), (2, 2, 3)$ has $n = (0, -4, 8)$, so $n_z^2 = 64$, $\|n\|^2 = 80$ and $|\cos\theta| = 2/\sqrt5 \approx 0.894$.

| $z$ | $s$ tried | facets in the slab | test of line L9 | layer |
|---|---|---|---|---|
| $0$ | $1$ | walls | $0 \le \tfrac1{16} \cdot 64$ | $0$ to $1$ |
| $1$ | $1$ | walls (the roof starts at $z = 2$, so it does not meet $(1, 2)$) | holds | $1$ to $2$ |
| $2$ | $1$ | walls, roof | $1 \cdot 64 = 64 > \tfrac1{16} \cdot 80 = 5$ | no |
| $2$ | $\tfrac12$ | walls, roof | $\tfrac14 \cdot 64 = 16 > 5$ | no |
| $2$ | $\tfrac14$ | walls, roof | $\tfrac1{16} \cdot 64 = 4 \le 5$ | $2$ to $\tfrac94$ |
| $\tfrac94$, $\tfrac52$, $\tfrac{11}4$ | $1$, $\tfrac12$, $\tfrac14$ | roof | as at $z = 2$ | three layers of $\tfrac14$ |

The output is $1, 2, \tfrac94, \tfrac52, \tfrac{11}4, 3$: six layers. The cusp height on the roof is $\tfrac14 \cdot 0.894 \approx 0.224 \le 0.25$. Uniform layers of $\tfrac14$ would need 12 layers for the same bound, and uniform layers of 1 would need 3 layers but leave a cusp of $0.894$ on the roof.

On a mesh of a sphere of radius 10 with 168 facets and all vertices exactly on the sphere (rational points), with $c = \tfrac1{20}$ and the thicknesses $\tfrac1{20}, \tfrac1{10}, \tfrac15, \tfrac3{10}$, the code of this page returns 243 layers: 160 of $\tfrac1{20}$ near the poles, 64 of $\tfrac1{10}$, one of $\tfrac15$ and 18 of $\tfrac3{10}$ near the equator. Uniform layers of $\tfrac1{20}$ would need 400. This is a measurement on one toy mesh, not a general ratio.

## Correctness

*Monotonicity.* If the layer from $z$ with thickness $s$ is feasible and $s' < s$, then the layer from $z$ with thickness $s'$ is feasible. The open slab $(z, z + s')$ is inside $(z, z + s)$, so it meets fewer facets, and each of them has $s'^2 n_z^2 \le s^2 n_z^2 \le c^2 \|n\|^2$.

*Each layer.* FEASIBLE$(z, s)$ returns true exactly when no facet meets the open slab with a cusp height above $c$, because line L9 is the exact squared form of the definition. Line L4 tries the thicknesses in decreasing order, and line L5 stops at the first feasible one. So the chosen $t$ is the largest feasible thickness. If none is feasible, then $t = t_1$, and by monotonicity no thickness smaller than $t_1$ would have helped among the allowed ones.

*Termination.* Each pass of line L2 adds at least $t_1 > 0$ to $z$, so the loop stops after at most $\lceil (z_{\max} - z_{\min}) / t_1 \rceil$ layers, and the last output is at or above $z_{\max}$.

So every layer has cusp height at most $c$ on every facet in it, except the layers of thickness $t_1$ where no allowed thickness meets the bound, and each layer is as thick as the bound allows at its start. The full proof is below.

*Not a minimum.* The greedy rule does not always give the fewest layers, because the problem lacks the [greedy choice property](/greedy-choice-property/): a thinner layer now can put the next layer start at a better height. Take thicknesses $1, 2, 4$, $c = 1$, a part of height 9 with vertical walls and two bands of facets with $|\cos\theta| = \tfrac13$ at heights 2 to 3 and 7 to 8. A layer of 4 that meets a band has cusp $\tfrac43 > 1$. Greedy takes $2, 2, 2, 2, 4$, which is 5 layers. The sequence $2, 1, 4, 2$ is feasible: the layer from 3 to 7 meets neither band, since both only touch its boundary. It has 4 layers. The tests find such cases by comparing the greedy count with an exhaustive search.

## Complexity

FEASIBLE scans all $n$ facets in $O(n)$ time. Each layer calls it at most $r$ times, so the total time is $O(L r n)$, with $\lceil H / t_r \rceil \le L \le \lceil H / t_1 \rceil$ for the height $H$ of the part. The extra space is $O(n)$ for the heights and the squared normals of the facets.

Two changes make it faster. Sort the facets by $z_{\min}$ and keep an active list, as in triangle mesh slicing, so that FEASIBLE looks only at the facets near $z$. And give each facet its own largest allowed thickness, the largest $t_i$ with $t_i^2 n_z^2 \le c^2 \|n\|^2$. Then a layer of thickness $s$ is feasible if $s$ is at most the minimum of these values over the facets in the slab, which a sweep can maintain.

## Properties

- **Bound per layer.** Every layer meets the cusp bound unless no allowed thickness does, and then it has the smallest thickness.
- **Largest step.** Each layer is the thickest feasible layer at its start.
- **Not minimal.** The number of layers is not always the minimum (see the example above).
- **Exact.** The only test is an exact comparison of squared integers or rationals.
- **Uses only normals.** The test looks at facet normals and heights, not at the true curvature of the design surface.

## Variants and improvements

- **Fewest layers.** If all thicknesses are multiples of a unit $q$, the heights that a layer can start at are $z_{\min} + jq$. Dynamic programming over these heights, from the top down, by the [principle of optimality](/principle-of-optimality/), gives the fewest feasible layers in $O((H/q)\, r\, n)$ time. The tests of this page use this as the exhaustive reference.
- **Stepwise uniform refinement.** Sabourin, Houser and Bøhn (1996) slice first at the largest thickness and then reslice each thick slab uniformly into thinner layers where the surface needs it.
- **Local adaptive slicing.** Tyberg and Bøhn (1998) let different parts of the same layer have different thicknesses, so a steep part next to a flat part does not force thin layers on both.
- **Other error measures.** Some methods bound the area or the volume between the staircase and the surface, not the cusp height. Others use the curvature of the CAD surface, see [surface curvature](/surface-curvature/), so that the thickness changes before a slope change, not after.
- **Machine limits.** Real printers have a range of thicknesses and can have rules on how fast the thickness can change from one layer to the next. These add constraints to line L4.

## When to use it

Use it when a part has both steep walls and gentle slopes, and print time matters. On a part that is all vertical walls, uniform thick layers are as good. On a part that is all gentle slopes, adaptive slicing gives thin layers everywhere and saves little. The cusp height is a geometric measure. It does not include the rounding of the edges of real beads, so it is an upper bound on one kind of surface error, not a model of the printed surface. The choice of [build orientation](/build-orientation/) changes the slopes, so the two decisions interact.

## Pitfalls

- **Facets that only touch the slab.** A facet whose top is at $z$ does not lie in the layer above $z$. With a closed slab, every layer would see the facets of the layer below, and the thickness would drop one layer too early.
- **Horizontal facets.** A horizontal face inside a layer has cusp height $t$. If $t_1 > c$, no thickness works there. The fallback must be visible to the user.
- **Square roots in the test.** Ties between $t\,|\cos\theta|$ and $c$ are common, because both come from round numbers. Compare the squares.
- **Small sloped facets.** A tiny facet with a gentle slope forces a thin layer, even if it is a meshing artifact. Clean or merge such facets first, or weight the test by facet area.
- **The last layer.** It can go above the top of the part. Either accept that or let the last layer be thinner if the machine allows it.

## Implementations

## History

Dolenc and Mäkelä published the cusp height and an adaptive choice of the layer thickness in Computer-Aided Design in 1994. Sabourin, Houser and Bøhn published stepwise uniform refinement in the Rapid Prototyping Journal in 1996, and Tyberg and Bøhn published local adaptive slicing in the same journal in 1998. Later work changed the error measure and the source of the slope (the mesh or the exact CAD surface), and many current slicers have an adaptive layer height option.

## References
