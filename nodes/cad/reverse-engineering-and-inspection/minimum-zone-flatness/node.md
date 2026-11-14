---
tag: 5ZWKK1
kind: algorithm
slug: minimum-zone-flatness
name: Minimum zone flatness
aliases:
- minimum zone straightness and flatness
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Finds the two closest parallel planes that hold all measured points, which is the width of the set, by testing face-vertex and edge-edge pairs of the convex hull exactly.
solves: [form-error-evaluation]
model: real-ram
complexity:
  vars: {n: the number of points, h: the number of hull vertices}
  time: {worst: Θ(n²), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1988
  people: [Michael E. Houle, Godfried T. Toussaint]
  note: Houle and Toussaint showed that the width of a set in three dimensions is attained by a face and a vertex or by two edges of its convex hull, and computed it from the antipodal pairs. Traband, Joshi, Wysk and Cavalier gave minimum zone methods for straightness and flatness in 1989.
prereqs: [convex-hull-3d, polygon-width, support-function]
see_also: [form-error-evaluation, minimum-zone-cylindricity, minimum-width-annulus, least-squares-reference-feature, antipodal-pairs, rotating-calipers, lp-type-problem, geometric-dimensioning-and-tolerancing]
sources:
  - paper: doi:10.1109/34.6790
    title: Michael E. Houle and Godfried T. Toussaint, Computing the width of a set, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(5), 1988, 761 to 765
    locator: the characterization of the width in three dimensions by antipodal vertex-face and edge-edge pairs of the convex hull, the algorithm in O(n log n + I) time for I antipodal edge pairs, and the minimax plane fit
  - paper: "Mark T. Traband, Sanjay Joshi, Richard A. Wysk and Tom M. Cavalier, Evaluation of straightness and flatness tolerances using the minimum zone, Manufacturing Review 2(3), 1989, 189 to 195"
    locator: the minimum zone evaluation of straightness and flatness from measured points
  - paper: doi:10.1007/BF02573973
    title: Bernard Chazelle, Herbert Edelsbrunner, Leonidas J. Guibas and Micha Sharir, Diameter, width, closest line pair, and parametric searching, Discrete and Computational Geometry 10(2), 1993, 183 to 196
    locator: the width of a point set in three dimensions in O(n^(8/5+ε)) time
  - paper: doi:10.1007/BF02712871
    title: Pankaj K. Agarwal and Micha Sharir, Efficient randomized algorithms for some geometric optimization problems, Discrete and Computational Geometry 16(4), 1996, 317 to 337
    locator: the width of a point set in three dimensions in O(n^(3/2+ε)) expected time
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 11, Convex Hulls (the incremental construction of a three-dimensional hull and the horizon of a new point)
  - url: https://www.iso.org/standard/66777.html
    title: ISO 1101:2017, Geometrical product specifications (GPS), Geometrical tolerancing, Tolerances of form, orientation, location and run-out, fourth edition
    locator: the standard as a whole (the flatness and straightness tolerance zones); no clause is quoted
---

Minimum zone flatness computes the flatness of a measured surface as the distance between the two closest parallel planes that hold all the measured points. That distance is the width of the point set. The width is attained by a pair of parallel supporting planes of the convex hull that touch a face and a vertex, or two edges, so the algorithm builds the hull and tests these pairs. With exact arithmetic the answer is exact. In two dimensions the same method gives straightness: the thinnest strip between two parallel lines, attained by an edge of the hull and the farthest vertex, which is the [polygon width](/polygon-width/). This page is a method; the problem, with all the forms (straightness, flatness, roundness, cylindricity) and the choice of the reference, is [form error evaluation](/form-error-evaluation/), and the method for cylindricity is [minimum zone cylindricity](/minimum-zone-cylindricity/).

## In plain words

A machine touches many points on a surface that should be flat. To grade the surface, we hold it between two parallel sheets of glass and push the sheets together until they touch the points. The gap left between the sheets is the flatness. We may tilt the sheets any way we like, and we want the tilt that makes the gap smallest.

Only a few tilts can be the best one. Wrap the points in the tightest convex shell. At the best tilt, one sheet lies flat on a face of the shell and the other touches a corner, or each sheet touches an edge of the shell, and the two edges cross. So we test each face against the farthest corner, and each pair of edges that can face each other, and keep the smallest gap.

## The problem

The input is a finite set $P$ of points in $\mathbb{R}^3$. A zone is a slab $\{x : \ell \le u \cdot x \le \ell + t\}$ with a unit normal $u$, and its width is $t$. The zone shape for flatness is the region between two parallel planes, and the objective is the least width of a zone that holds $P$:
$$ F(P) = \min_{\lvert u \rvert = 1} \Bigl( \max_{x \in P} u \cdot x - \min_{x \in P} u \cdot x \Bigr). $$
This is the minimum zone, or Chebyshev, flatness. The output is $F(P)$ and the two planes. For straightness of points in a plane, replace the planes by lines.

A [least-squares plane](/least-squares-reference-feature/) is not the minimum zone plane. The two planes parallel to it through the extreme points form a zone, so its width is never smaller than $F(P)$, and it is often larger. Standards such as ISO 1101 define flatness by the minimum zone.

## The algorithm

```pseudo id=main
MIN-ZONE-FLATNESS(P)
L1  if P lies in one plane then return that plane, width 0
L2  T ← triangles of the convex hull of P, with outward normals
L3  best ← ∞
L4  for each triangle t with normal N and a vertex a of t
L5      best ← min(best, (N·a − min over vertices v of N·v) / |N|)
L6  for each pair of hull edges e, f with directions d_e, d_f not parallel
L7      n ← d_e × d_f
L8      for s in {+1, −1}
L9          if s·n is in the normal cone of e and −s·n is in the normal cone of f
L10             best ← min(best, s·n·(a_e − a_f) / |n|)     ▷ a_e on e, a_f on f
L11 return best and the planes that attain it
```

**Line L2.** The hull is built incrementally from a tetrahedron. A triangle is visible from a new point if the point is strictly on its outer side; the visible triangles are removed and the horizon edges are joined to the new point. A point in the plane of a triangle does not see it, so adjacent triangles may be coplanar. All signs are computed with integers or fractions.

**Line L5, face and vertex.** The plane of the triangle supports the hull, and the parallel plane through the lowest vertex closes the zone.

**Lines L6 to L10, edge and edge.** The normal cone of an edge is the set of directions spanned by the outward normals $N_1$, $N_2$ of its two triangles; these are the directions in which the edge is highest. A direction normal to both edges is parallel to $n = d_e \times d_f$. If it is in the cone of $e$ and its opposite is in the cone of $f$, the planes through $e$ and $f$ normal to $n$ hold all points between them. With $t = \det(N_1, N_2, d)$, a vector $u$ normal to $d$ is in the cone when $\det(N_1, u, d)$ and $\det(u, N_2, d)$ are each zero or have the sign of $t$; when $t = 0$ the cone is the ray of $N_1$.

Every candidate is a true zone, so the minimum is never below $F(P)$, and the optimum is among the candidates.

## Example

**Edge and edge.** The regular tetrahedron $(0,0,0), (1,1,0), (1,0,1), (0,1,1)$ has edge length $\sqrt 2$. Each face is at the height $2/\sqrt 3 \approx 1.1547$ from the opposite vertex, but the opposite edges $(0,0,0)(1,1,0)$ and $(1,0,1)(0,1,1)$ lie in the planes $z = 0$ and $z = 1$. The flatness is $1$, attained by two edges. A method that tests faces only gives $1.1547$.

**Tilted surface.** The points $(0,0,0), (2,0,2), (0,2,0), (2,2,2), (1,1,2)$ lie on and above the plane $z = x$, tilted $45$ degrees. The minimum zone is the face $z = x$ and the parallel plane through $(1,1,2)$, so $F = 1/\sqrt 2 \approx 0.7071$. The vertical deviation from that plane is $1$, which overstates the flatness by $1/\cos 45°$.

**The vertical Chebyshev fit is a different plane.** Minimizing $t$ subject to $\lvert z_i - a x_i - b y_i - c \rvert \le t$ is a [linear program](/linear-programming-problem/), and it is often used for flatness. It measures the zone along $z$, not along the normal. For the points $(1,2,2), (0,0,1), (4,3,10), (3,3,7), (1,3,4)$ it has the unique optimum $a = 2$, $b = 1/3$, with vertical thickness $5/3$. The orthogonal width of that zone is $(5/3)/\sqrt{1 + 4 + 1/9} \approx 0.7372$. The minimum zone has the normal $(-12, -1, 5)$, is attained by two edges, and has $F^2 = 81/170$, so $F \approx 0.6903$. The tests check these values with exact arithmetic.

## Correctness

The [correctness file](proofs/correctness.md) proves:

- **The face-vertex and edge-edge characterization.** On a cell of the overlay of the Gaussian map of the hull with its antipodal image, the extent is $u \cdot c$ for a fixed $c$. This function has no local minimum with a positive value on an open region or an open great circle arc of the sphere, so the minimum is at a facet normal or at a crossing of two edge arcs. This is the result of Houle and Toussaint.
- **The hull.** The incremental hull with exact orientation tests bounds the hull and has no degenerate triangle.
- **The cone test** above, and that every candidate is a zone that holds all points.
- **The vertical fit only bounds flatness.** If $(a^*, b^*)$ solves the vertical fit with value $V^*$ and the minimum zone plane has slope $g$, then $F \le V^*/\sqrt{1 + \lvert (a^*, b^*) \rvert^2} \le V^* \le F \sqrt{1 + \lvert g \rvert^2}$. So the vertical fit is close only when the part is nearly level, and the example shows that the first inequality can be strict.

The tests compare the result with a brute force over every plane through three points and every direction normal to two segments, in exact arithmetic, on random sets with many coplanar points. They also compare it with a search over a one-degree grid of normals, using the fact that the extent changes by at most the diameter of the set times the change of the unit normal.

## Complexity

The incremental hull tests each new point against every current triangle, which is $O(n h)$ and $\Theta(n^2)$ in the worst case. Testing each triangle against all vertices is $O(h n)$, and the pairs of edges are $O(h^2)$ with $O(1)$ work each. So the time is $\Theta(n^2)$ in the worst case on the [real RAM](/real-ram/), and $\Theta(n)$ when the hull has a bounded size. A faster hull, the randomized incremental hull in expected $O(n \log n)$ time or [quickhull](/quickhull/), which is fast in practice, reduces the first term, but the edge pairs stay $O(h^2)$. The space is $\Theta(n)$. In exact arithmetic the numbers grow: for integer input of $b$ bits, the normals and dot products have $O(b)$ bits.

Houle and Toussaint list the antipodal pairs in $O(n \log n + I)$ time, with $I$ the number of antipodal edge pairs, which is $\Theta(n^2)$ in the worst case. Chazelle, Edelsbrunner, Guibas and Sharir computed the width in $O(n^{8/5 + \varepsilon})$ time, and Agarwal and Sharir in $O(n^{3/2 + \varepsilon})$ expected time. Those methods are not practical for inspection data, where $n$ is at most a few thousand.

## Properties

- **Exact.** With integer or rational input, every comparison is exact, and the result is the true minimum zone of the measured points.
- **Invariant.** The width does not change under rigid motions of the data, unlike the vertical fit.
- **Depends on the extreme points only.** Only hull vertices matter, so one outlier changes the result. That is the definition of the tolerance, not a defect, but it makes the method sensitive to spikes in the data.
- **Global.** No starting plane is needed and there is no local minimum.

## Variants and improvements

- **Straightness.** In two dimensions the width is attained by a hull edge and a vertex, and [rotating calipers](/rotating-calipers/) list the [antipodal pairs](/antipodal-pairs/) in linear time after the hull. The code checks each hull edge against all hull vertices.
- **Linear programming.** With a reference direction fixed near the normal, the vertical fit is a small [LP](/linear-programming-problem/) in three variables, and it is an [LP-type problem](/lp-type-problem/), solvable in expected linear time. It is exact for the vertical measure only, and the theorem above bounds its error.
- **Repeated linear programs.** Solving the vertical fit, rotating the data so that the found normal is vertical, and solving again gives a sequence of zones that does not get wider. Each zone is a true zone, so this gives an upper bound at each step.
- **Approximation.** A grid or an iterative search over normals gives upper bounds, and the Lipschitz bound of the extent gives an error estimate.

## When to use it

Use it to report flatness or straightness under a standard that defines them by the minimum zone, and to check software that reports flatness. Use a least-squares plane when a stable reference with a smooth dependence on the data is needed, and say that its zone width is an upper bound. Use the vertical linear program only when the surface is nearly level, and convert its value to an orthogonal width.

## Pitfalls

- **Testing faces only.** The width of a tetrahedron is attained by two edges. Methods that only rest a plane on a face of the hull overstate flatness.
- **Vertical distances.** A Chebyshev fit of $z$ against $x$ and $y$ measures thickness along $z$, which overstates flatness by $1/\cos$ of the tilt and can pick a different plane.
- **Floating point orientation tests.** Rounded signs on nearly coplanar points give hulls with holes or folded triangles. Use exact predicates, or adaptive ones.
- **Too few points.** The minimum zone of the sample is a lower bound of the flatness of the surface, since the true extreme points may not be measured. A larger or better spread sample, for example [Hammersley sampling](/hammersley-sampling-for-cmm/), reduces the gap.
- **Probe radius.** The points must be corrected for the probe radius before the evaluation.

## Implementations

## History

Houle and Toussaint gave the characterization of the width of a set by antipodal pairs of the convex hull in 1985 at the Symposium on Computational Geometry, and in the journal in 1988. Traband, Joshi, Wysk and Cavalier gave minimum zone methods for straightness and flatness for inspection in 1989, when coordinate measuring machine software still used least-squares fits. Later work in computational geometry reduced the time to subquadratic bounds by parametric search and randomization. The ISO and ASME standards define flatness by the zone between two parallel planes.

## References
