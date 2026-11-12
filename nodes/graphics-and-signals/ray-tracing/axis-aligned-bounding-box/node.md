---
tag: CTW9KH
kind: concept
slug: axis-aligned-bounding-box
name: Axis-aligned bounding box
aliases: [AABB]
area: graphics-and-signals/ray-tracing
level: intro
summary: The smallest box with faces parallel to the coordinate planes that contains an object. Graphics stores it as two corners, grows it by union, rates it by surface area and tests rays on it by slabs.
prereqs: [bounding-volume]
see_also: [minimum-bounding-rectangle, slab-method, bounding-volume-hierarchy, surface-area-heuristic, bvh-refitting, ieee-754, separating-axis-theorem, rectangle-intersection-reporting]
sources:
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 2.6 Bounding Boxes (the two corners, the empty box with inverted bounds, union, surface area and offset), Section 2.8 on applying a transformation to a box, and Section 3.9 on conservative rounding
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 4, Bounding Volumes, the section on axis-aligned bounding boxes (min-max, min-width and center-radius forms, overlap tests, and updating the box of a rotated object)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 22, Intersection Test Methods, the sections on bounding volume creation and on box tests
  - paper: doi:10.1145/15886.15916
    title: Timothy L. Kay and James T. Kajiya, Ray tracing complex scenes, SIGGRAPH 1986, Computer Graphics 20(4), 269 to 278
    locator: slab volumes, of which the box with the three coordinate normals is the simplest case
---

An axis-aligned bounding box (AABB) of an object is the smallest box with faces parallel to the coordinate planes that contains it. It is the [minimum bounding rectangle](/minimum-bounding-rectangle/) of the object, which defines it with its union, overlap and distance operations; this page covers what graphics adds. A renderer stores the box as two corners, starts from an empty box with inverted bounds, grows it by unions, rates it by its surface area for the [surface area heuristic](/surface-area-heuristic/), moves it under affine maps by a cheap rule that makes it larger, and tests a ray against it with the [slab method](/slab-method/).

## In plain words

Take an object and slide six walls toward it until they touch it: two from the left and right, two from the front and back, one from above and one from below. The walls must stay square to the room. The space between the walls is the axis-aligned bounding box.

You can write it down with only six numbers: the lowest and highest point on each of the three directions. Two such boxes join into a new one by taking the lower of the low numbers and the higher of the high numbers. A ray test needs only a few subtractions and products.

The price is that the box follows the room, not the object. A thin stick that lies on a slant gets a big, mostly empty box, and when the object turns, its box changes shape.

## The idea

**Two forms.** In the *min-max* form a box is the pair of corners $lo, hi \in \mathbb{R}^3$, the set $\{p : lo_a \le p_a \le hi_a\}$. In the *center-extent* form it is a center $c = (lo + hi)/2$ and the half widths $e = (hi - lo)/2$. The min-max form suits the [slab method](/slab-method/) and unions. The center-extent form suits transforms and overlap tests, since two boxes overlap exactly when $|c_a - c'_a| \le e_a + e'_a$ on each axis.

**The box of a primitive.** The box of a polytope, for example a triangle, is the per-axis minimum and maximum of its vertices, because a linear function on a polytope takes its extreme values at vertices. A sphere with center $m$ and radius $r$ has the box $[m - r, m + r]$. A vertex that moves on a line from $p$ to $q$ during a frame stays in the box of $p$ and $q$, so the box of a triangle with linear motion is the union of its boxes at the two ends of the frame.

**The empty box.** Set $lo = (+\infty, +\infty, +\infty)$ and $hi = (-\infty, -\infty, -\infty)$. It contains no point, and the union with any box $B$ gives $B$, so it is the identity of union. A build loop starts from it and adds primitives one at a time with no special first case, as PBRT does. The surface area of the empty box must be defined as 0 rather than computed from the formula, which would give $+\infty$ or NaN.

**Surface area.** With $w = hi - lo$, the surface area is $S = 2(w_x w_y + w_y w_z + w_z w_x)$. Under uniform random lines, the probability that a line meeting a box $A$ also meets a box $B \subseteq A$ is $S(B)/S(A)$ (see [bounding volume](/bounding-volume/)). This is why the [SAH](/surface-area-heuristic/) uses areas and not volumes. A flat box with one width 0 has a positive area, as it should: a ray can still hit it, while its volume is 0.

**Axis and offset.** The longest axis $\arg\max_a w_a$ is the usual split axis of a top-down build. The offset of a point $p$ is $(p - lo)/w$ per axis, which is in $[0, 1]$ inside the box; binned builds use it to map a centroid to a bin, and the [LBVH](/lbvh-construction/) uses it to quantize a centroid for its Morton code.

**The box of a transformed box.** Let $M$ be a $3 \times 3$ matrix and $t$ a translation. The image of the box is a parallelepiped, and its AABB has center $M c + t$ and half widths $e'_i = \sum_j |M_{ij}|\, e_j$. This rule, given by Arvo in Graphics Gems (1990), costs 9 products instead of transforming 8 corners. It is exact for the image of the box, but the image of the box is larger than the image of the object, so the box of a transformed box is looser than the box of the transformed object. Each repeat makes it larger, and a box that is transformed by a rotation and then rotated back does not come back to its original size.

**Conservative rounding.** A box computed in floating point must still contain the object. When the corners come from rounded values, such as transformed vertices, round $lo$ down and $hi$ up, for example with one step of `nextafter` toward $\mp\infty$, or widen by a bound on the error. When the inputs are floats and the box is only their minimum and maximum, no rounding occurs and the box is exact. See [IEEE 754](/ieee-754/) and [ulp](/ulp/).

## Examples

- **A triangle.** The triangle with corners $(1, 0, 2)$, $(4, 3, 2)$ and $(2, 5, -1)$ has the box $lo = (1, 0, -1)$, $hi = (4, 5, 2)$. Then $w = (3, 5, 3)$, the longest axis is y, the center is $(2.5, 2.5, 0.5)$ and the surface area is $2(15 + 15 + 9) = 78$. The centroid $(7/3, 8/3, 1)$ has the offset $(4/9, 8/15, 2/3)$.
- **A union.** The union of the box above with $[(0, 1, 0), (2, 2, 6)]$ is $[(0, 0, -1), (4, 5, 6)]$, with $w = (4, 5, 7)$ and surface area $2(20 + 35 + 28) = 166$. Starting from the empty box, the union with the first box gives the first box.
- **A rotation by a right angle.** The box $[(1, 2, 0), (3, 6, 2)]$ has center $(2, 4, 1)$ and half widths $(1, 2, 1)$. Under the rotation $(x, y, z) \mapsto (-y, x, z)$ followed by the translation $(10, 0, 0)$, the center goes to $(6, 2, 1)$ and the half widths become $(2, 1, 1)$, so the new box is $[(4, 1, 0), (8, 3, 2)]$. A rotation by a right angle maps the box onto a box, and the rule is tight.
- **A rotation that is not a right angle.** Take the unit cube $[0, 1]^3$ and the rotation about the z axis with $\cos\theta = 3/5$ and $\sin\theta = 4/5$. The center $(1/2, 1/2, 1/2)$ goes to $(-1/10, 7/10, 1/2)$, and the half widths become $(3/5 + 4/5) \cdot 1/2 = 7/10$ in x and y, and $1/2$ in z. The box is $[-4/5, 3/5] \times [0, 7/5] \times [0, 1]$, which matches the rotated corners $(0, 0)$, $(3/5, 4/5)$, $(-4/5, 3/5)$ and $(-1/5, 7/5)$ in the xy plane. Its surface area is $2(1.96 + 1.4 + 1.4) = 9.52$, against 6 for the cube. Rotating this box back by $-\theta$ with the same rule gives half widths $(3/5 + 4/5) \cdot 7/10 = 0.98$, a box of width 1.96, while the box of the cube rotated back is the cube again.
- **A flat box.** The triangle $(0, 0, 5)$, $(2, 0, 5)$, $(0, 2, 5)$ lies in the plane $z = 5$. Its box has $w_z = 0$, volume 0 and surface area $2 \cdot 2 \cdot 2 = 8$. A ray test must accept such a box; the slab method does.

## Where it is used

- [Slab method](/slab-method/): the ray test for a box, in $O(1)$.
- [Bounding volume hierarchy](/bounding-volume-hierarchy/): boxes are the usual node volumes, and [BVH construction](/bvh-construction/) and the [surface area heuristic](/surface-area-heuristic/) work with their unions and areas. [BVH refitting](/bvh-refitting/) recomputes them after motion.
- [kd-tree traversal](/kd-tree-traversal/) and [Amanatides-Woo traversal](/amanatides-woo-traversal/) clip the ray to the box of the scene before they start.
- [Collision detection](/collision-detection/): boxes in the broad phase, and the 15-axis test of the [separating axis theorem](/separating-axis-theorem/) for oriented boxes.
- [Frustum culling](/frustum-culling/): a box is tested against the six planes of the view frustum by its nearest and farthest corners.
- [Rectangle intersection reporting](/rectangle-intersection-reporting/), the [R-tree](/r-tree/) and the [loose octree](/loose-octree/) use the same boxes under the name MBR.

## References
