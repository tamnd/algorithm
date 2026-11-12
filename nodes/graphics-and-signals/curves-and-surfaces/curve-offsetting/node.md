---
tag: JW2MQQ
kind: problem
slug: curve-offsetting
name: Curve offsetting
aliases:
- offset curve computation
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Given a plane curve, a distance and a tolerance, compute a curve in a fixed form, such as a B-spline, that lies within the tolerance of the trimmed offset of the curve.
model: real-ram
prereqs: [offset-curve]
see_also: [b-spline-fitting, hermite-spline, de-casteljau-algorithm, curve-intersection, bentley-ottmann-algorithm, minkowski-sum, medial-axis, voronoi-diagram]
sources:
  - paper: doi:10.1109/MCG.1984.275995
    title: Wayne Tiller and Eric G. Hanson, Offsets of two-dimensional profiles, IEEE Computer Graphics and Applications 4(9), 36-46 (1984)
    locator: offsetting the legs of the control polygon and intersecting them, with subdivision
  - paper: doi:10.1109/38.586019
    title: Gershon Elber, In-Kwon Lee and Myung-Soo Kim, Comparing offset curve approximation methods, IEEE Computer Graphics and Applications 17(3), 62-71 (1997)
    locator: the methods compared, and the error measure from the squared distance to the generator
  - paper: doi:10.1016/0010-4485(92)90059-J
    title: Binh Pham, Offset curves and surfaces, a brief survey, Computer-Aided Design 24(4), 223-229 (1992)
    locator: approximation methods for offset curves and the problem of self-intersections
  - paper: doi:10.1147/rd.345.0736
    title: Rida T. Farouki and Takis Sakkalis, Pythagorean hodographs, IBM Journal of Research and Development 34(5), 736-752 (1990)
    locator: polynomial curves with exact rational offsets
---

Curve offsetting is the problem of computing the [offset curve](/offset-curve/) of a plane curve $C$ at a distance $d$ in a form that a CAD or graphics system can store, usually a B-spline or a sequence of Bézier pieces, lines and arcs. The exact offset $C + dN$ cannot be stored in that form: for a polynomial or rational curve it is not polynomial or rational in general, because the unit normal $N$ contains a square root. So the problem is an approximation problem with a tolerance $\varepsilon$. It has two parts. The first is to approximate the offset of each regular piece. The second is to trim it: where $d$ exceeds the radius of curvature on the concave side the offset has cusps and loops, and where distant parts of $C$ come closer than $2|d|$ it crosses itself, and those parts are not at distance $|d|$ from $C$. Offsetting is the base of tool paths for milling, of shelling and thickening in solid modeling, and of the outlines of stroked paths in vector graphics.

## In plain words

You have a curve, and you want the curve that runs beside it at a fixed distance, like the path of the center of a round cutter that follows a contour. Each point of the new curve is easy to find: walk from the old curve straight sideways by the distance. But the result is usually not a curve of the kind your program can store, so you have to build a curve of that kind that stays very close to it.

There is a second trap. Where the old curve bends more sharply than the distance allows, the sideways points fold over and form small loops. Where two parts of the old curve come close to each other, the new curve runs into itself. These parts must be found and cut away.

## Definition

**Input.**

- A regular plane curve $C : [a, b] \to \mathbb{R}^2$, given as a polynomial, B-spline or NURBS curve, open or closed.
- A signed distance $d \ne 0$, with the side fixed by the unit normal $N$ (left of the direction of travel for $d > 0$).
- A tolerance $\varepsilon > 0$ and a target class of curves, for example cubic B-splines or Bézier curves of degree $p$.

**Output.** A curve $\hat C$ in the target class, possibly in several pieces, with

$$\operatorname{dist}_H\bigl(\hat C, O_d\bigr) \le \varepsilon,$$

where $O_d$ is the trimmed offset: the set of points of $C + dN$ whose distance to $C$ is exactly $|d|$, and $\operatorname{dist}_H$ is the Hausdorff distance. Without trimming the target is the full offset $C + dN$.

**Error measures in practice.** The Hausdorff distance is expensive. Most methods keep a parametric correspondence $\hat C(t) \approx C(t) + dN(t)$ and measure

$$\varepsilon(t) = \Bigl|\, \lVert \hat C(t) - C(t) \rVert - |d| \,\Bigr| .$$

Elber, Lee and Kim (1997) work with the squared form $\delta(t) = \lVert \hat C(t) - C(t) \rVert^2 - d^2$, which is a polynomial or rational function of $t$ when $\hat C$ and $C$ are. Its Bernstein coefficients bound it from both sides, so a bound on $|\delta|$ is certified, not sampled. A small $\varepsilon(t)$ gives $\operatorname{dist}(\hat C(t), C) \le |d| + \varepsilon(t)$, an upper bound only. For a lower bound the vector $\hat C(t) - C(t)$ must also be close to normal to $C$.

## Variants

- *Untrimmed or trimmed.* Approximate $C + dN$ as a parametric curve, or approximate only the part at distance $|d|$. Trimming removes local loops, which come from cusps where $d k = 1$, and global loops, which come from parts of $C$ that are close in the plane.
- *Open or closed curves.* For a closed curve the trimmed offset is the boundary of the region grown or shrunk by $|d|$, the boundary of a [Minkowski sum](/minkowski-sum/) with a disc. Its number of components can change with $d$.
- *Profiles.* A profile is a chain of lines, arcs and free-form pieces with corners. At a convex corner the offsets of the two pieces leave a gap that is closed with an arc of radius $|d|$ (round join) or by extending the pieces (miter join). At a concave corner they overlap and are trimmed.
- *Exact offsets.* For lines, circles and Pythagorean-hodograph curves the offset is exactly representable, as a line, a circle or a rational curve, and the problem has an exact answer.
- *Variable distance.* $d$ is a function along the curve, as for a brush stroke whose width changes.
- *Repeated offsets.* Pocket milling needs the offsets at the distances $d, 2d, 3d, \dots$ inside a region until it is empty.

## Examples

**Two methods on a parabola.** Let $C$ be the parabola $y = x^2$ on $[-1, 1]$, the quadratic Bézier curve with control points $(-1, 1)$, $(0, -1)$, $(1, 1)$, and $d = 0.25$ toward the inside. The smallest radius of curvature is $1/2$ at the vertex, so the offset has no cusps, but its curvature there is $k/(1 - dk) = 4$. Two methods, with the error measured as the largest difference between $|d|$ and the true distance from $\hat C$ to the parabola over 101 samples per piece:

- *Control polygon offset (Tiller and Hanson).* Move each leg of the control polygon by $d$ along its normal and intersect the moved legs to get the new control points. Split the Bézier curve at the middle with the [de Casteljau algorithm](/de-casteljau-algorithm/) and repeat on the pieces.
- *Hermite interpolation.* On each of $n$ equal pieces in $x$, take the cubic [Hermite](/hermite-spline/) segment through the exact offset points at the two ends, with the exact offset tangents $(1 - dk)C'$.

| pieces | Tiller-Hanson, quadratic | Hermite, cubic |
|---|---|---|
| 1 | $8.5 \times 10^{-2}$ | $9.3 \times 10^{-2}$ |
| 2 | $5.2 \times 10^{-3}$ | $5.2 \times 10^{-3}$ |
| 4 | $2.0 \times 10^{-4}$ | $7.1 \times 10^{-4}$ |
| 8 | $5.4 \times 10^{-5}$ | $2.1 \times 10^{-4}$ |
| 16 | $6.2 \times 10^{-6}$ | $2.0 \times 10^{-5}$ |

The errors are largest at the vertex, where the offset bends most. With 32 pieces the Hermite error is $1.4 \times 10^{-6}$, a factor 14 below 16 pieces, near the factor 16 of a fourth-order method. For coarse pieces the high curvature at the vertex dominates and the factors are irregular. On this curve the quadratic control polygon method needs fewer pieces for the same tolerance than the cubic Hermite method.

**A cusp that must be trimmed.** For the same parabola with $d = 1$, the offset has cusps at $x = \pm 0.38321$ and crosses itself at $(0, 5/4)$, the image of $x = \pm\sqrt3/2$ (see [offset curve](/offset-curve/)). An approximation that follows $C + dN$ also follows the swallowtail between these parameters. A trimming step finds the crossing by [curve intersection](/curve-intersection/), cuts both pieces there and drops the part between, which leaves a curve with a corner at $(0, 5/4)$.

**Exact answer.** For the cubic $C(t) = (t - t^3/3, t^2)$, a Pythagorean-hodograph curve with speed $1 + t^2$, the offset

$$C_d(t) = \left(t - \tfrac{t^3}{3} - \frac{2dt}{1 + t^2},\; t^2 + d\,\frac{1 - t^2}{1 + t^2}\right)$$

is a rational curve of degree 5 for every $d$ and can be stored exactly as a rational Bézier curve, with error zero.

## Known algorithms

| method | idea | notes |
|---|---|---|
| Tiller and Hanson (1984) | offset the legs of the control polygon, intersect them, subdivide | simple and local; exact at the end points, approximate inside |
| sample and interpolate | exact offset points (and tangents) at chosen parameters, then [Hermite](/hermite-spline/) or spline interpolation | order of accuracy set by the interpolant, adaptive refinement where the error test fails |
| sample and fit | many exact offset points, then [least-squares B-spline fitting](/b-spline-fitting/) with a fixed knot vector, knots inserted where the error is large | one smooth B-spline, the knot placement decides the cost |
| approximation of the normal | replace $N$ by a polynomial or rational approximation of the unit vector, then compute $C + d\hat N$ symbolically | the error is a function of $t$ that can be bounded |
| lines and arcs | approximate $C$ by a polyline or by arcs, whose offsets are exact | used in machining; the result has only $G^1$ joins |
| PH curves (Farouki and Sakkalis 1990) | design with curves of polynomial speed | exact rational offsets, but the curve must be a PH curve from the start |
| trimming | find self-intersections of the approximation, keep the parts at distance $\ge |d|$ from $C$ | by pairwise [curve intersection](/curve-intersection/) or a sweep such as [Bentley-Ottmann](/bentley-ottmann-algorithm/) on monotone pieces |

Elber, Lee and Kim (1997) compare several of these methods by the number of control points that each needs for a given tolerance on test curves. Pham (1992) surveys the earlier methods.

## Bounds

No method has a worst-case bound in terms of the size of $C$ alone. Near a point where $dk$ approaches 1 the curvature $k/(1 - dk)$ of the offset is unbounded, so the number of pieces for a tolerance $\varepsilon$ is unbounded too. For a fixed curve whose offset is regular, with curvature bounded away from the cusp condition, an interpolant of degree $p$ on pieces of length $h$ has error $O(h^{p+1})$. So $O(\varepsilon^{-1/(p+1)})$ pieces are enough. The constant grows with the derivatives of the offset. Except for lines, circles and PH curves, no finite exact answer exists in the usual curve forms, so a tolerance cannot be avoided. Trimming $m$ pieces costs $O(m^2)$ pair tests naively, and $O((m + I) \log m)$ with a sweep over monotone pieces with $I$ crossings.

## Reductions

- *To curve fitting.* Points of the exact offset are cheap. Approximating them is [curve fitting](/curve-fitting/) or interpolation, for example [B-spline fitting](/b-spline-fitting/) with the offset points as data.
- *Trimming to curve intersection.* Local and global loops are found from the self-intersections of the approximation, a [curve intersection](/curve-intersection/) problem, and the segment version is solved by a sweep.
- *To the medial axis.* The trimmed offsets of a region at all distances are the level sets of the distance to its boundary. They change their topology only at critical values of that distance, which are radii of maximal discs centered on the [medial axis](/medial-axis/). For polygons and arcs the medial axis comes from the [Voronoi diagram](/voronoi-diagram/) of the boundary pieces, and all offsets can be read from it.
- *To the Minkowski sum.* For a closed curve the outer trimmed offset is the boundary of the [Minkowski sum](/minkowski-sum/) of the region with a disc of radius $|d|$.

## Applications

- Milling and cutting: the tool center moves on the offset of the part contour by the tool radius, and pocketing uses repeated inner offsets.
- Solid modeling: shelling and thickening of profiles, and clearances and tolerance zones.
- Vector graphics and fonts: the outline of a stroked path of width $w$ is made of the two offsets at $\pm w/2$ with joins and caps.
- Robotics: the free region for a disc-shaped robot is the complement of the obstacles grown by its radius.

## References
