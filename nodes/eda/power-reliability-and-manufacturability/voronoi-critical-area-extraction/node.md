---
tag: VXSKTK
kind: algorithm
slug: voronoi-critical-area-extraction
name: Voronoi critical area extraction
aliases:
- Papadopoulou-Lee critical area
- L-infinity Voronoi critical area
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Papadopoulou and Lee's method that computes critical area for all defect sizes at once from an L-infinity Voronoi diagram of the layout polygons.
model: word-ram
complexity:
  vars: {n: the number of rectangles, F: the number of faces built, k: the largest number of vertices of a face}
  time: {build: "O(n^5)", query: "O(F k)", average: "O(F k^2)"}
  space: {extra: "O(F k)"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1999
  people: [Evanthia Papadopoulou, D. T. Lee]
  note: Papadopoulou and Lee showed in IEEE TCAD in 1999 that, for square defects, the critical radius of a point is its L-infinity distance to the second nearest polygon, so that the second order L-infinity Voronoi diagram of the layout gives the critical area for shorts at every defect size and its average in closed form.
prereqs: [critical-area, voronoi-diagram, order-k-voronoi-diagram]
see_also: [weighted-voronoi-diagram, minkowski-sum, poisson-yield-model, negative-binomial-yield-model, monte-carlo-integration, design-rule-checking, fortunes-algorithm]
sources:
  - paper: "Evanthia Papadopoulou and D. T. Lee, Critical area computation via Voronoi diagrams, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 18(4), 463 to 474, April 1999"
    locator: the square defect model, the critical radius as the L-infinity distance to the second nearest polygon, the second order L-infinity Voronoi diagram of rectilinear polygons, its construction by plane sweep, and the integration of the critical area over its regions
  - paper: "Evanthia Papadopoulou and D. T. Lee, The L-infinity Voronoi diagram of segments and VLSI applications, International Journal of Computational Geometry and Applications 11(5), 503 to 528, 2001"
    locator: the L-infinity Voronoi diagram of segments of any orientation, which extends the method beyond rectilinear layouts
  - paper: doi:10.1147/rd.276.0549
    title: C. H. Stapper, Modeling of integrated circuit defect sensitivities, IBM Journal of Research and Development 27(6), 549 to 557, November 1983
    locator: the critical area as a function of defect size and its average over the defect size distribution, the quantity that the method computes
---

Voronoi critical area extraction computes the [critical area](/critical-area/) for shorts of a layout layer at every defect size at once. Papadopoulou and Lee observed in 1999 that, for square defects, a point is a critical centre for radius $r$ exactly when its $L_\infty$ distance to the second nearest net is at most $r$. That distance is a piecewise linear function over the second order $L_\infty$ [Voronoi diagram](/voronoi-diagram/) of the layout, so one diagram gives $A(r)$ for all $r$, and the average critical area under the defect size density in closed form. This page builds the needed structure for axis-parallel rectangles by incremental insertion, proves that it is exact, and cites Papadopoulou and Lee for the plane sweep that handles general rectilinear polygons.

## In plain words

A particle of dust that lands on a chip can join two wires that should stay apart. Whether it does depends on where its centre falls and how big it is. The critical area is the size of the set of landing spots that cause a short.

The direct way is to pick a size, grow every wire by that size, and measure where grown wires of different nets overlap, again for every size.

This method asks instead, for each point of the chip, how big a particle centred there must be to touch two different nets. That number is the distance to the second closest net. The method cuts the chip once into pieces where that distance is a simple slope. Then the critical area for any size is a sum of clipped piece areas, and the average over all sizes is a sum of exact integrals.

## The problem

**Input.** Axis-parallel rectangles $R_i = [a_i, b_i] \times [c_i, d_i]$, $i = 1, \dots, n$, each with a net label $\nu_i$, at least two nets, and a window $W$ that is an axis-parallel rectangle. Rectangles may overlap; rectangles of the same net count as connected. The defect of radius $r$ at $p$ is the square $p + r[-1, 1]^2$, and defect radii have Stapper's density $f$ with peak $r_0$ (on the [critical area](/critical-area/) page), with survival function $S(t) = P(\text{radius} \ge t)$, which is $1 - t^2/(2r_0^2)$ for $t \le r_0$ and $r_0^2/(2t^2)$ for $t > r_0$.

**Distances.** The $L_\infty$ distance from $p = (x, y)$ to $R_i$ is

$$ \delta_i(p) = \max(a_i - x,\ x - b_i,\ c_i - y,\ y - d_i,\ 0), $$

because a point of a product of intervals can be chosen coordinate by coordinate. The distance to a net is $d_N(p) = \min_{\nu_i = N} \delta_i(p)$, and the *critical radius* $t(p)$ is the second smallest value among the $d_N(p)$, one value per net.

**Output.** The function $A(r) = \operatorname{area}\{p \in W : t(p) \le r\}$, which is the critical area for shorts, as a structure that answers each $r$ exactly, and the average

$$ \bar A = \int_0^\infty A(r) f(r)\, dr = \int_W S\big(t(p)\big)\, dp, $$

where the second form follows by exchanging the two integrals (Tonelli's theorem, the integrand is nonnegative).

## The algorithm

A *face* is a convex polygon $P \subseteq W$ with a state $(\nu, h_1, h_2)$: $\nu$ is the nearest net on $P$, and $h_1$ and $h_2$ are affine functions of $p$, or $+\infty$, equal on $P$ to the distance to the nearest net and to the second nearest net. Splitting a face by an affine function $u$ means cutting its polygon by the line $u = 0$ into the parts with $u \le 0$ and $u \ge 0$.

```pseudo id=main
VORONOI-CRITICAL-AREA(rectangles, W, r0)
L1  faces ← {(W, none, +∞, +∞)}
L2  for each rectangle R of net M, in any order
L3      g_1, …, g_5 ← a − x, x − b, c − y, y − d, 0          ▷ δ_R = max of these
L4      for each face (P, ν, h1, h2)
L5          if some g_k ≥ (M = ν ? h1 : h2) at every vertex of P then keep the face; continue
L6          split P into parts Q on which one g_k is the maximum; let g be that piece on Q
L7          if ν = none: the state of Q is (M, g, +∞)
L8          else if M = ν: split Q by g − h1; where g ≤ h1 set h1 ← g
L9          else split Q by g − h1 and g − h2:
L10              where g ≤ h1:        (ν, h1, h2) ← (M, g, h1)
L11              where h1 ≤ g ≤ h2:   h2 ← g
L12              where g ≥ h2:        no change
L13 A(r) = Σ over faces of area(P ∩ {h2 ≤ r})                 ▷ one clip per face
L14 Ā = Σ over faces of ∫ area(P ∩ {h2 ≤ r}) f(r) dr           ▷ quadratic pieces, closed form
L15 return faces, A, Ā
```

Line L6 splits $P$ by $g_2 - g_1$, then each part by $g_3$ minus the current maximum, and so on, which leaves at most 16 parts, usually one or two. Line L5 is a quick test: if one piece is already at least $h$ at all vertices, then $\delta_R \ge h$ on all of $P$, because an affine function that is nonnegative at the vertices of a convex polygon is nonnegative on it.

Line L14 uses one fact about a convex polygon $P$ and an affine $h$: between two consecutive values of $h$ at the vertices of $P$, the area of $P \cap \{h \le r\}$ is a quadratic in $r$. So three exact areas fix each quadratic, and $\int (c_0 + c_1 r + c_2 r^2) f(r)\, dr$ has a closed form: on $r \le r_0$ the integrand is a polynomial, and on $r > r_0$ the terms are $c_0 r_0^2 r^{-3}$, $c_1 r_0^2 r^{-2}$ and $c_2 r_0^2 r^{-1}$, whose integrals are rational functions and a logarithm. Above the largest vertex value the whole face counts, with weight $S(\cdot)$ at that value.

The implementation works in exact rational arithmetic. All lines it cuts by are differences of two affine pieces with coefficients in $\{-1, 0, 1\}$, so the vertices have small denominators.

## Example

The layout is $A = [0, 6] \times [0, 1]$, $B = [0, 6] \times [2, 3]$ and $C = [7, 8] \times [0, 3]$, three nets, in the window $W = [0, 8] \times [0, 3]$ of area 24. The build leaves 42 faces, and the values of $h_2$ at their vertices are $\frac{1}{2}$, $1$, $\frac{3}{2}$ and $2$.

Some critical radii: at $(3, 1.5)$, in the middle of the gap between $A$ and $B$, the distances to $A$, $B$ and $C$ are $0.5$, $0.5$ and $4$, so $t = 0.5$. At $(3, 0.5)$, inside $A$, they are $0$, $1.5$ and $4$, so $t = 1.5$: a defect centred on a wire must reach the next net. At $(7.5, 1.5)$, inside $C$, $t = 1.5$ as well.

The structure gives $A(r) = 0$ for $r \le \frac{1}{2}$, and

| $r$ | $\frac{3}{4}$ | $1$ | $\frac{3}{2}$ | $2$ | $3$ |
|---|---|---|---|---|---|
| $A(r)$ | $\frac{37}{8}$ | $9$ | $17$ | $24$ | $24$ |

These fit one formula. The pair regions are $A$ with $B$: $[0, 6 + r] \times [2 - r, 1 + r]$, $A$ with $C$: $[7 - r, 6 + r] \times [0, 1 + r]$, and $B$ with $C$: $[7 - r, 6 + r] \times [2 - r, 3]$, inside $W$ for $\frac{1}{2} \le r \le 2$. Each of the three pairwise overlaps and the triple overlap is the square $[7 - r, 6 + r] \times [2 - r, 1 + r]$ of area $(2r - 1)^2$, so inclusion and exclusion gives

$$ A(r) = (6 + r)(2r - 1) + 2(1 + r)(2r - 1) - 3(2r - 1)^2 + (2r - 1)^2 = (2r - 1)(10 - r), \qquad \tfrac{1}{2} \le r \le 2, $$

and $A(r) = 24$ for $r \ge 2$. With $r_0 \le \frac{1}{2}$ only the tail of $f$ is used:

$$ \bar A = r_0^2 \int_{1/2}^{2} \frac{-2r^2 + 21r - 10}{r^3}\, dr + 24 \cdot \frac{r_0^2}{2 \cdot 2^2} = r_0^2 \big( 12.75 - 4 \ln 2 + 3 \big) \approx 12.9774\, r_0^2. $$

For $r_0 = 0.25$ this is $0.81109$ and for $r_0 = 0.5$ it is $3.24435$, the values the program returns.

## Correctness

The [full proof](proofs/correctness.md) shows the following.

**Squares and distances.** The square $p + r[-1,1]^2$ meets $R_i$ if and only if $\delta_i(p) \le r$. So it meets net $N$ if and only if $d_N(p) \le r$, and it shorts two nets if and only if $t(p) \le r$. Hence $A(r) = \operatorname{area}\{p \in W : t(p) \le r\}$ is the critical area of the definition. This is the observation of Papadopoulou and Lee.

**Invariant.** After the first $k$ rectangles are inserted, the faces are convex, have disjoint interiors and cover $W$, and on each face $h_1 = d_\nu = \min_N d_N$ and $h_2 = \min_{N \ne \nu} d_N$, where the distances use only the inserted rectangles. A new rectangle of net $M$ changes only $d_M$, to $\min(d_M, g)$. The proof checks the three cases of lines L8 to L12, using that $d_M \ge h_2$ before the insertion when $M \ne \nu$.

**Exact output.** After all insertions $h_2 = t$ on every face, so line L13 is the exact area. Line L14 is exact up to the floating point evaluation of the closed forms, by the quadratic lemma: the area of $P \cap \{h \le r\}$ grows at a rate equal to the length of the chord $P \cap \{h = r\}$ divided by $|\nabla h|$, and that chord length is affine between consecutive vertex values.

**What is not proved here.** Papadopoulou and Lee build the second order $L_\infty$ diagram of general rectilinear polygons by a plane sweep and integrate over trapezoids. This page proves only the rectangle case with the incremental build. For their construction and its bounds, see their paper.

## Complexity

Every line the build cuts by is the zero set of a difference of two functions from the set of the $4n + 1$ affine pieces of the distance functions, so there are $O(n^2)$ such lines. The faces are unions of cells of their arrangement inside $W$, so $F = O(n^4)$, and an insertion touches each face once, at a cost proportional to its size. The sum of the face sizes is at most the number of edges of the arrangement, $O(n^4)$, so the build takes $O(n^5)$ operations on rationals of bounded size in the worst case. This bound is crude. On random layouts with $n = 5, 10, 20$ and $40$ rectangles the implementation leaves $F = 183$, $445$, $1294$ and $3990$ faces, about $n^{1.6}$; most of them are fragments of larger regions of the diagram, which could be merged when their states are equal.

Once built, $A(r)$ at one radius costs one clip per face, $O(F k)$. The average costs $O(k)$ clips per face, $O(F k^2)$. The method answers all radii from one build, where direct shape expansion pays a full union of rectangles for every radius.

## Properties

- **Exact.** $A(r)$ is a rational number computed without error for rational inputs. Only the logarithms of the average are floating point.
- **All sizes at once.** The structure does not depend on $r$ or on $f$; a new size distribution needs only line L14.
- **Square defects.** The result is the critical area for square defects. A disk of radius $r$ lies inside the square of radius $r$ and contains the square of radius $r/\sqrt{2}$, so the disk critical area lies between $A(r/\sqrt{2})$ and $A(r)$.
- **Union, not sum.** A centre that shorts three nets is counted once, as the definition requires; summing pair areas would count it three times.
- **Shorts only.** Opens need a different distance, the size a defect needs to cut a net, which Papadopoulou treated in later work.

## Variants and improvements

- **Plane sweep.** Papadopoulou and Lee compute the second order $L_\infty$ diagram by a sweep line and split its regions into trapezoids where the distance is linear, then integrate per trapezoid.
- **Segments of any orientation.** Their 2001 paper on the $L_\infty$ Voronoi diagram of segments extends the method to non-rectilinear layouts.
- **Higher order diagrams.** Papadopoulou's later work uses higher order and Hausdorff Voronoi diagrams for defects that must touch several shapes, such as via blocks and opens.
- **Monte Carlo.** Dropping random defects and counting faults estimates $\bar A$ with error that shrinks as the inverse square root of the sample size; it handles any defect shape and any fault rule but gives no exact $A(r)$. See [Monte Carlo integration](/monte-carlo-integration/).
- **Shape expansion.** Growing all shapes by $r$ and intersecting nets, as in the union test of the implementation, gives $A(r)$ for one $r$ at a time. Its cost grows with the number of radii sampled.

## When to use it

Use it when the critical area for shorts is needed for many defect sizes or for several size distributions, on rectilinear layouts, and the square defect model is acceptable. Use Monte Carlo when the defect shape or the fault rule is unusual, and shape expansion when only one or two radii matter.

## Pitfalls

- **Disks versus squares.** The square model overestimates the disk critical area, by at most the factor between $A(r/\sqrt{2})$ and $A(r)$. Calibrate the defect density with the same model.
- **Nets, not shapes.** The second nearest *net* matters, not the second nearest rectangle. Two touching rectangles of one net would give $t = 0$ everywhere near them if treated as different sites.
- **Window edges.** Shapes just outside $W$ still count as near nets. Include them, or the area near the border is too small.
- **Divergent averages.** With Stapper's $r^{-3}$ tail, a formula for one pair extended to all $r$ diverges; the window cap $A(r) \le \operatorname{area}(W)$ keeps the average finite. The structure applies that cap by itself.
- **Fragmented faces.** Without merging, the incremental build leaves many more faces than the diagram has regions. That costs time, not accuracy.

## Implementations

## History

Stapper defined the critical area and its average in 1983 at IBM. Before Voronoi methods, it was computed by shape expansion at sampled sizes or by Monte Carlo defect simulation. Papadopoulou and Lee published the Voronoi formulation for shorts in 1999, with the second order $L_\infty$ diagram and closed form integration, and extended the diagram to segments of any orientation in 2001. Papadopoulou continued the line with methods for opens and via blocks based on higher order and Hausdorff Voronoi diagrams.

## References
