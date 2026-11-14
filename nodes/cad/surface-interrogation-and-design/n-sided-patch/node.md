---
tag: PFHCJJ
kind: problem
slug: n-sided-patch
name: N-sided patch
aliases:
- multi-sided patch
- n-sided hole filling
area: cad/surface-interrogation-and-design
level: advanced
summary: Fill a hole bounded by n curves, n other than four, with a smooth surface that meets the surrounding patches with tangent or curvature continuity.
prereqs: [coons-patch, bezier-patch, tangent-plane-continuity]
see_also: [gregory-patch, generalized-bezier-patch, vertex-blend, coons-patch, tangent-plane-continuity, twist-compatibility, hole-filling, floater-mean-value-coordinates]
sources:
  - paper: doi:10.1016/0167-8396(84)90006-2
    title: "Peter Charrot and John A. Gregory, A pentagonal surface patch for computer aided geometric design, Computer Aided Geometric Design 1(1), 87 to 94, 1984"
    locator: an interpolant over a pentagon that is compatible with patches on rectangular domains
  - paper: doi:10.1145/77055.77059
    title: "Charles T. Loop and Tony D. DeRose, A multisided generalization of Bézier surfaces, ACM Transactions on Graphics 8(3), 204 to 234, 1989"
    locator: S-patches over a convex polygon, defined with generalized barycentric coordinates
  - paper: doi:10.1111/cgf.12833
    title: "Tamás Várady, Péter Salvi and György Karikó, A multi-sided Bézier patch with a simple control structure, Computer Graphics Forum 35(2), 307 to 317, 2016"
    locator: the Generalized Bézier patch and its tangent plane continuous connection to adjacent Bézier surfaces
  - paper: doi:10.1016/j.cagd.2024.102286
    title: "Tamás Várady, Péter Salvi and Márton Vaitkus, Genuine multi-sided parametric surface patches, a survey, Computer Aided Geometric Design 110, 102286, 2024"
    locator: survey of single patch representations over multi-sided domains (general locator)
---

The n-sided patch problem asks for a surface that fills a region bounded by $n$ curves, where $n$ is three, five or more, so that it joins the surfaces around it smoothly. Such regions appear in every network of curves that is not a grid: at a corner of a solid where three rounded edges meet, at the end of a feature line, and where a designer draws a curve network with five sided faces. For $n = 4$ the problem is solved by [Coons patches](/coons-patch/) and tensor product patches, which is why the case of other $n$ has its own name. There is no single best answer: the problem fixes the boundary and the tangent planes along it, and leaves the interior free, so each method is a choice of interior shape. This page is about parametric surfaces with given boundary curves, not about the [filling of holes in triangle meshes](/hole-filling/), which adds triangles to close a gap in a mesh.

## In plain words

Picture a frame made of bent wire with three, five or six sides, and the smooth panels of a car body all around it. The task is to stretch a skin over the frame so that the skin touches each wire and meets the panels next to it without a crease. Four sided frames are easy, because the standard surface patches of design software have four sides. Other frames do not fit those patches directly. One can cut the frame into four sided pieces and fill each piece, or one can use a special patch that has as many sides as the frame. Either way, the corners need care: where two wires meet, the skin has one tangent plane, and the data from the two wires must agree there.

## Definition

**Input.** An integer $n \ge 3$. Boundary curves $c_1, \dots, c_n : [0, 1] \to \mathbb{R}^3$, with indices modulo $n$, that form a closed loop: $c_i(1) = c_{i+1}(0)$. For the tangent version, a cross boundary field $r_i : [0, 1] \to \mathbb{R}^3$ along each curve, with $r_i(s)$ not parallel to $c_i'(s)$. The pair of $c_i$ and $r_i$ is the *ribbon* of side $i$, and it usually comes from the adjacent surface.

**Output.** A domain $D \subset \mathbb{R}^2$ with $n$ sides, usually a convex polygon with corners $q_1, \dots, q_n$, maps $\ell_i(s) = (1 - s) q_{i-1} + s q_i$ onto its sides, and a surface $S : D \to \mathbb{R}^3$ that is continuously differentiable and regular, $S_u \times S_v \ne 0$, with

1. $S(\ell_i(s)) = c_i(s)$ for all $s$ and $i$ (position);
2. for the tangent version, the tangent plane of $S$ at $\ell_i(s)$ is spanned by $c_i'(s)$ and $r_i(s)$ for all $s$ and $i$, which is [tangent plane continuity](/tangent-plane-continuity/) with the adjacent surfaces;
3. for the curvature version, also equal normal curvatures with the adjacent surfaces along the boundary.

The problem has infinitely many solutions when it has one, since any small change of $S$ that vanishes to first order along the boundary keeps the conditions. A method picks one, and its quality is judged by fairness measures, which are design criteria and not part of the statement. No formal objective is accepted by all authors.

## Variants

- **Positional only.** Only the boundary curves are given. A transfinite blend of the curves, such as a generalized Coons scheme, is enough.
- **Tangent continuous.** The usual case in CAD, with the ribbons of condition 2.
- **Curvature continuous.** Condition 3 is added, for class A surfaces in car design.
- **Single patch or split.** Some applications require one patch with $n$ sides; others accept a set of four sided or three sided patches inside the hole.
- **Representation.** The result may be required to be polynomial, rational, a B-spline surface for exchange with other systems, or any parametric surface.
- **Concave or curved domains.** When the boundary loop is far from convex, a convex polygon domain gives a poor parametrization, and curved domains are used.

## Examples

**The octant of a sphere.** The hole is bounded by three quarter circles of the unit sphere in the coordinate planes, and the ribbons are the tangent planes of the sphere. The octant is a solution. No solution is a polynomial surface, because its restriction to a side of the polygon would be a polynomial curve that runs along a quarter circle, and no such curve exists. Proof: in the plane of the circle, let $x(t)^2 + y(t)^2 = 1$ for all $t$ in an interval, with real polynomials $x$ and $y$ that are not both constant. A polynomial that is zero on an interval is zero everywhere, so the equation holds for all $t$. Let $d \ge 1$ be the larger degree, with leading coefficients $a$ and $b$ of $t^d$, one of which is not zero. The coefficient of $t^{2d}$ on the left is $a^2 + b^2 > 0$, but on the right it is $0$. So exact solutions need rational patches, and a polynomial patch can only approximate this hole.

**The corner of a box.** Round the three edges at a corner of a box with three blend surfaces. The blends overlap near the corner, and a hole remains whose boundary consists of curves on the blends and, if the blends are set back, curves on the faces. The [vertex blend](/vertex-blend/) page treats this case.

**A five sided face.** A designer draws a curve network for a car body, and one face of the network has five sides. Charrot and Gregory gave an interpolant over a pentagon for this situation in 1984.

**Corner data that does not fit.** If $c_i'(1)$ and $c_{i+1}'(0)$ are parallel at a corner, no solution over a polygon domain exists, by the theorem in the section on bounds.

## Known algorithms

| Method | Pieces | Continuity with neighbours | Notes |
| --- | --- | --- | --- |
| Central split into $n$ four sided patches | $n$ | $G^1$ between all patches | standard patches, but inner joins need extra conditions |
| [Gregory patches](/gregory-patch/) in the split | $n$ | $G^1$ | rational corner blends remove the need for compatible twists |
| Charrot and Gregory pentagon | 1 | matches the side data | interpolant over a pentagon that fits a rectangular patch layout |
| S-patch of Loop and DeRose | 1 | $C^k$ joins of S-patches | Bézier type control net over a polygon, many control points |
| Transfinite ribbon schemes | 1 | $G^1$, some $G^2$ | blend the $n$ ribbons with weights over a polygon domain |
| [Generalized Bézier patch](/generalized-bezier-patch/) | 1 | $G^1$ to Bézier neighbours | control net with layers, like a tensor product net |
| Subdivision surfaces | many | $G^1$ at extraordinary points | [Catmull-Clark](/catmull-clark-subdivision/) or [Doo-Sabin](/doo-sabin-subdivision/) around a point of valence $n$ |
| Energy minimization | any | as constrained | [energy-based fairing](/energy-based-surface-fairing/) picks the interior |

**Central split.** Choose a centre point and a curve from it to a point on each side, which cuts the hole into $n$ four sided regions. Fill each with a four sided patch. The patches must meet each other with tangent plane continuity along the inner curves, and at the centre all $n$ of them share one tangent plane. [Twist compatibility](/twist-compatibility/) at the corners of the small patches is the main difficulty, which Gregory patches avoid with rational blends.

**Single patch over a polygon.** Map each point of a convex polygon domain to local parameters for each side: a parameter along the side and a distance from it. These can come from generalized barycentric coordinates, such as Wachspress or [mean value coordinates](/floater-mean-value-coordinates/). Each side defines a ribbon surface in its own local parameters, which meets the side data exactly. A weighted sum of the ribbons, with weights that make each ribbon dominant near its own side, gives the patch. The weights must be chosen so that the first derivatives across each side come from that side alone, which is what keeps condition 2.

## Bounds

The problem has no lower bound on running time in the usual sense: each method evaluates a closed form or solves a fixed linear system, and its cost depends on the representation. What the problem does have is necessary conditions on the input.

**Theorem (corner conditions).** Let $S$ be a solution with tangent continuity over a convex polygon domain, regular and continuously differentiable up to the corner $q_i$, where sides $i$ and $i + 1$ meet. Then $c_i'(1)$ and $c_{i+1}'(0)$ are not parallel, the tangent plane at the corner is the plane $T$ that they span, and $r_i(1)$ and $r_{i+1}(0)$ lie in $T$.

*Proof.* By condition 1 and the chain rule, $c_i'(1) = DS(q_i) \, \ell_i'(1)$ and $c_{i+1}'(0) = DS(q_i) \, \ell_{i+1}'(0)$. The vectors $\ell_i'(1) = q_i - q_{i-1}$ and $\ell_{i+1}'(0) = q_{i+1} - q_i$ are independent, because the polygon is convex and the corner is a real corner. Since $S$ is regular, $DS(q_i)$ is injective, so the images are independent, and they span the image of $DS(q_i)$, which is the tangent plane. By condition 2, $r_i(s)$ lies in the tangent plane at $\ell_i(s)$, and the tangent plane is continuous, so $r_i(1)$ lies in the plane at $q_i$. The same holds for $r_{i+1}(0)$. $\square$

If $S$ is also twice continuously differentiable at the corner, the mixed derivatives defined by the two ribbons must agree, which is the condition of [twist compatibility](/twist-compatibility/). Rational schemes such as the Gregory patch drop the second derivative continuity at the corner and so drop this condition.

## Reductions

- **To four sided patches.** The central split reduces one $n$ sided hole to $n$ four sided holes, plus conditions between them. For $n = 4$ the problem is the [Coons patch](/coons-patch/) problem.
- **To triangles.** Splitting from a centre point into $n$ triangles reduces the problem to [Bézier triangles](/bezier-triangle/) with $G^1$ conditions between them.
- **From vertex blends.** The corner where several blends meet in a solid is an instance, which is how [vertex blends](/vertex-blend/) are built.
- **From curve networks.** Surfacing a curve network with faces of any number of sides is a set of instances that share ribbons along common curves.

## Applications

- Vertex blends and corner fills in [boundary representation](/boundary-representation/) solid modelers.
- Surfacing curve networks in car body and product design, where faces with three or five sides are common.
- Closing the region around a point where three or more surfaces meet after a trim, for example in [blending surfaces](/blending-surface/).
- Converting subdivision surfaces or meshes with extraordinary vertices into patches for CAD exchange.

## References
