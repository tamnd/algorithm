---
tag: QNVPYX
kind: data-structure
slug: sweep-representation
name: Sweep representation of solids
aliases:
- swept solid representation
- extrusion and revolution solids
area: cad/solid-modeling
level: core
summary: Represents a solid by a planar profile and a motion, as in extrusions and revolutions, and decides membership as a union over the sweep parameter.
model: word-ram
complexity:
  vars:
    n: the number of vertices of the profile polygon
  time:
    worst: O(n)
  space:
    extra: Θ(n)
prereqs: [r-set, point-in-polygon]
see_also: [swept-volume, sweep-surface, surface-of-revolution, constructive-solid-geometry, boundary-representation, minkowski-sum-of-polyhedra, mass-properties-of-solids, feature-based-modeling]
sources:
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the section on sweep representations, translational and rotational sweeps, and their limited domain
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: the chapter on representation schemes, the part on sweeping
  - paper: doi:10.1016/0010-4485(90)90051-D
    title: Ralph R. Martin and P. C. Stephenson, Sweeping of three-dimensional objects, Computer-Aided Design 22(4), 223 to 234, 1990
    locator: the sweep of a solid along a general path, built from the sweeps of its faces and their silhouette curves
  - paper: "W. P. Wang and K. K. Wang, Geometric modeling for swept volume of moving solids, IEEE Computer Graphics and Applications 6(12), 1986, 8 to 17"
    locator: the envelope of a moving solid and the self-intersection problems of general sweeps
---

A sweep representation describes a solid by a set $X$ and a motion $M(t)$, $t \in [0, 1]$: the solid is every point that $X$ occupies at some time. The two common cases are the *extrusion*, where a plane profile moves along a straight vector, and the *revolution*, where a profile in a half-plane turns a full circle about an axis. A shaft, a washer, a bolt head and a pocket outline are all of this kind, and every mechanical CAD system starts a part from such sweeps. The representation is very small and close to the way people draw, but it is not closed under Boolean operations: the union of two extrusions in different directions is not an extrusion. So a modeler stores a sweep as a primitive of a [CSG tree](/constructive-solid-geometry/) or converts it to a [B-rep](/boundary-representation/). This page gives the data structure for extrusions and full revolutions of a simple polygon, and an exact classification of a point as inside, on the boundary of or outside the solid.

## In plain words

Draw a shape on paper, then imagine pulling it straight up out of the paper, maybe at a slant. The paper shape leaves a trail, and the trail is a solid. That is an extrusion. Or stand the drawing up next to a pole and spin it once around the pole, like a lathe. The trail is a round solid, such as a ring or a cup. That is a revolution.

To ask if a point is in the trail, ask the reverse question: where was the drawing when it passed through this point? For an extrusion, the height of the point gives the moment, so slide the point back and test it against the drawing. For a revolution, turn the point back into the plane of the drawing and test it there. A point on the pole needs one more look.

## The abstract type

A sweep is a pair $(X, M)$, where $X$ is a bounded set and $M(t)$ is a rigid motion or an affine map for each $t$ in a parameter interval $I$. Its solid is the union over the parameter:

$$\mathrm{Sw}(X, M) = \bigcup_{t \in I} M(t) X, \qquad p \in \mathrm{Sw}(X, M) \iff \exists\, t \in I : M(t)^{-1} p \in X.$$

The general problem of computing this union for any solid and any path is the [swept volume](/swept-volume/) problem. This page uses the two cases that Requicha's survey of 1980 calls translational and rotational sweeps:

- **Extrusion.** $X$ is a simple polygon in the plane $z = 0$, $d = (d_x, d_y, d_z)$ is a vector with $d_z \neq 0$, $I = [0, 1]$ and $M(t) x = x + t d$. The solid is a prism, upright if $d_x = d_y = 0$ and slanted if not.
- **Revolution.** $X$ is a simple polygon in the half-plane $\{(r, z) : r \ge 0\}$, placed in space as the half-plane $y = 0$, $x \ge 0$. $I = [0, 2\pi]$ and $M(\theta)$ turns by $\theta$ about the $z$ axis. The solid is the set of points $(x, y, z)$ with $(\sqrt{x^2 + y^2}, z) \in X$.

The operations are CLASSIFY($S$, $p$), which returns IN, ON or OUT for a point $p$ with rational coordinates, VOLUME($S$), and CHECK($S$), which tests that the stored data give an [r-set](/r-set/).

## Representation

An extrusion stores the vertex list of $X$, in either orientation, and the three numbers of $d$. A revolution stores the vertex list of $X$ in $(r, z)$ coordinates. All coordinates are integers or fractions, so that every test below is exact.

The representation is *valid*, that is the solid is an r-set, under these conditions, which CHECK tests in $O(n^2)$ time:

- $X$ is a simple polygon: at least three vertices, nonzero area, and no two edges that meet except neighbours at their common vertex.
- For an extrusion, $d_z \neq 0$. If $d_z = 0$, the profile slides in its own plane and the result is flat, with no volume.
- For a revolution, every vertex has $r \ge 0$. A profile that crosses the axis sweeps some points twice, and the part on the far side is not a mirror image of the near side, so the stored data do not describe the solid that the user drew.

The representation is *unambiguous*: a pair $(X, d)$ or a profile $X$ gives one solid. It is not *unique*: a cylinder is the extrusion of a disk and also the revolution of a rectangle, and the same prism is the extrusion of its bottom face along $d$ or of its top face along $-d$.

## Operations

The point $p = (p_x, p_y, p_z)$ has rational coordinates. CLASSIFY-PROFILE($X$, $q$) is the classification of a point of the plane against a closed polygon as IN, ON or OUT, as on the [point in polygon](/point-in-polygon/) page, with the even-odd crossing rule for IN and OUT and an exact test of whether $q$ lies on an edge.

```pseudo id=main
CLASSIFY-EXTRUSION(X, d, p)
L1  t ← p_z / d_z                       ▷ the only time at which the plane of X passes through p
L2  if t < 0 or t > 1 then return OUT
L3  q ← (p_x − t·d_x, p_y − t·d_y)      ▷ p moved back to time 0
L4  c ← CLASSIFY-PROFILE(X, q)
L5  if c ≠ OUT and (t = 0 or t = 1) then return ON   ▷ bottom or top face
L6  return c

CLASSIFY-REVOLUTION(X, p)
L7  s ← p_x² + p_y²                    ▷ the square of the distance to the axis
L8  c ← CLASSIFY-PROFILE(X, (√s, p_z)), comparing √s with each rational number by squares
L9  if s > 0 or c = OUT then return c
L10 if the edges of X on the axis r = 0 contain (0, p_z) and reach above and below it then return IN
L11 return ON
```

Line L8 never computes $\sqrt{s}$. The crossing rule needs only two kinds of test: whether the point is left or right of the crossing $r_c$ of an edge with the line $z = p_z$, and whether it lies on a horizontal edge between two rational ends. Both compare $\sqrt{s}$ with a rational number $q$, and $\sqrt{s} < q$ holds exactly when $q > 0$ and $s < q^2$. So all signs are computed with integers and fractions, as the [orientation test](/orientation-test/) page asks for every geometric predicate.

The volumes follow from Cavalieri's principle and from Pappus's centroid theorem:

```pseudo id=volume
VOLUME(S)
V1  if S is an extrusion then return |area(X)| · |d_z|
V2  m ← |Σ_i (r_i + r_{i+1}) (r_i z_{i+1} − r_{i+1} z_i)| / 6     ▷ the first moment of X about the axis
V3  return 2π · m
```

Here $(r_i, z_i)$ are the vertices of $X$ in order, with indices taken modulo $n$. Line V2 is the polygon form of $\iint_X r \, dA$; Pappus's theorem says that the volume of the revolution is $2\pi$ times this moment, the area of $X$ times the length of the circle traced by its centroid.

## Example

Take the square $X$ with corners $(0,0), (2,0), (2,2), (0,2)$ and the slanted vector $d = (1, 0, 3)$. The prism has volume $4 \cdot 3 = 12$.

| $p$ | L1: $t$ | L3: $q$ | L4: $c$ | result |
|---|---|---|---|---|
| $(2, 1, 3/2)$ | $1/2$ | $(3/2, 1)$ | IN | IN |
| $(3, 1, 3)$ | $1$ | $(2, 1)$ | ON | ON at L5 |
| $(1/5, 1, 3/2)$ | $1/2$ | $(-3/10, 1)$ | OUT | OUT |
| $(1, 1, 0)$ | $0$ | $(1, 1)$ | IN | ON at L5, bottom face |
| $(1, 1, -1)$ | $-1/3$ | | | OUT at L2 |

Now revolve two profiles: the rectangle $R_1$ with $r \in [1, 2]$, $z \in [0, 1]$, which gives a ring, and the rectangle $R_2$ with $r \in [0, 2]$, $z \in [0, 1]$, which gives a cylinder.

| profile | $p$ | L7: $s$ | L8: $c$ | result |
|---|---|---|---|---|
| $R_1$ | $(1, 1, 1/2)$ | $2$ | IN, since $1 < \sqrt 2 < 2$ | IN |
| $R_1$ | $(3/5, 4/5, 1/2)$ | $1$ | ON, on the edge $r = 1$ | ON |
| $R_1$ | $(0, 0, 1/2)$ | $0$ | OUT | OUT |
| $R_2$ | $(0, 0, 1/2)$ | $0$ | ON, on the edge $r = 0$ | IN at L10 |
| $R_2$ | $(0, 0, 1)$ | $0$ | ON, at a corner | ON at L11 |
| $R_2$ | $(1, 1, 1)$ | $2$ | ON, on the top edge, $0 \le \sqrt 2 \le 2$ | ON |
| $R_2$ | $(2, 1, 1/2)$ | $5$ | OUT, since $\sqrt 5 > 2$ | OUT |

The point $(0, 0, 1/2)$ is on the boundary of the profile $R_2$ but in the interior of the cylinder: the edge on the axis is glued to itself by the full turn. That is why lines L10 and L11 exist. For the volumes, V2 gives $m = 3/2$ for $R_1$, so the ring has volume $3\pi$, which is $\pi(2^2 - 1^2) \cdot 1$. For $R_2$ it gives $m = 2$ and the volume $4\pi$. The triangle with corners $(0, 0), (1, 0), (0, 1)$ revolves to a cone of volume $\pi/3$.

## Correctness

By the definition of the sweep, $p$ is in the solid exactly when some parameter value takes $p$ back into $X$. For an extrusion, $M(t)^{-1} p = p - t d$ lies in the plane $z = 0$ only for $t = p_z / d_z$, so there is one candidate time, and lines L1 to L4 test it. The map $(x, y, t) \mapsto (x + t d_x, y + t d_y, t d_z)$ is an affine bijection from $X \times [0, 1]$ onto the solid, and an affine bijection keeps interiors, so $p$ is interior exactly when $q$ is interior to $X$ and $0 < t < 1$. This gives line L5. For a revolution, the turn that brings $p$ into the half-plane of $X$ brings it to $(\sqrt{s}, 0, p_z)$, for any angle if $p$ is on the axis. Off the axis, the map from $(r, \theta, z)$ to space is a local diffeomorphism, so interior and boundary points of $X$ give interior and boundary points of the solid. On the axis, a small ball around $p$ is in the solid exactly when a small half-disk around $(0, p_z)$ is in $X$, which is the test of line L10. The full proof is in the proof file.

The tests check CLASSIFY against the definition. The oracle takes a finite sample of the sweep parameter, the times $k/20$ for extrusions and 20 rational rotations from Pythagorean triples and quarter turns for revolutions, and tests whether $M(t)^{-1}p$ is in $X$ for some sample, with a winding number test that is independent of the crossing rule of the code. The test points are built so that their own parameter is in the sample, so the sampled union gives the exact answer for them. IN and ON are checked by small probes around the point in all lattice directions up to 8, at distance $1/1000$, and by probes along $d$ or along the circle. Points with an irrational radius $\sqrt s$ are checked against floating-point classification when they are more than $10^{-6}$ from the profile boundary, and the volumes against a grid count.

## Complexity

- CLASSIFY takes $O(n)$ time: one pass over the edges of $X$ with a constant number of exact operations per edge. The fractions stay small, since each test uses only the input coordinates and the point.
- VOLUME takes $O(n)$ time and gives an exact rational number, times $\pi$ for a revolution.
- CHECK takes $O(n^2)$ time with the plain test of all pairs of edges. A sweep-line test brings it to $O(n \log n)$.
- The representation takes $\Theta(n)$ space. The B-rep of the same solid has $\Theta(n)$ faces for an extrusion, and for a revolution it has one face of revolution per edge of $X$ that is not on the axis.

## Variants

- **Partial revolution.** Turn the profile by an angle less than a full turn. The classification adds a test of whether the direction of $(p_x, p_y)$ lies in the swept sector; with rational end directions this test is an exact cross product. The axis rule of line L10 then no longer applies, since the two end faces of the sector meet on the axis.
- **Drafted and tapered extrusions.** The profile also shrinks or grows as it moves, so $M(t)$ is an affine map with a scale. A slice of the solid is still one scaled copy of $X$, and the classification has the same form.
- **Sweeps along a curve.** The profile moves along a space curve with a moving frame, which gives a pipe or a spring. The boundary surface is a [sweep surface](/sweep-surface/), and self-intersection becomes the main difficulty.
- **Sweeps of solids.** A solid moves along a path, as a cutting tool does. This is the [swept volume](/swept-volume/) problem, solved by envelopes or by sampling. When the solid only translates along a straight segment, the result is the [Minkowski sum](/minkowski-sum-of-polyhedra/) of the solid and the segment.
- **Surfaces of revolution.** Revolving only the boundary curve gives a [surface of revolution](/surface-of-revolution/), the boundary of the solid of this page.

## When to use it

Use a sweep when the shape comes from a drawing: prismatic parts, turned parts, profiles of pockets and bosses. In a feature-based or history-based modeler, each extrude or revolve step stores exactly this pair of profile and motion, and the system evaluates it to a B-rep and combines it with the rest of the part by [Boolean operations](/solid-boolean-operations/). A sweep is also a good representation for direct queries on one primitive: point classification, volume and mass properties are exact and cheap. Do not use sweeps as the only representation of a whole part, since a union of sweeps is not a sweep.

## Pitfalls

- **Points on the axis.** A point on the axis of a revolution is on the boundary of the profile but can be inside the solid. Test the edges on the axis, as lines L10 and L11 do, or the cylinder in the example has a wrong axis line.
- **Profiles that cross the axis.** If part of $X$ has $r < 0$, the revolution does not describe what the drawing shows. Reject such a profile, or cut it at the axis and keep one side.
- **Flat extrusions.** An extrusion with $d_z = 0$ has no volume. Check $d_z \neq 0$ before line L1 divides by it.
- **Computing the radius.** Computing $\sqrt{s}$ in floating point makes points on cylindrical faces fall in or out at random. Compare squares, as line L8 does.
- **Self-intersecting profiles.** A profile with crossing edges gives a set that is not the closure of its interior along the crossings, and the even-odd rule gives holes the user did not draw. Run CHECK on input.
- **Booleans.** The union, intersection or difference of two sweeps is in general not a sweep. Store the result as a CSG tree of sweeps or as a B-rep.

## Implementations

## History

Solids made by moving a profile are as old as drafting, and the volume rule for revolutions is Pappus's centroid theorem from late antiquity, found again by Guldin in the seventeenth century. In solid modeling, Requicha's survey of 1980 listed translational and rotational sweeps as one of the representation schemes, next to CSG, cell decompositions and boundary representations, and noted that their domain is small. The modelers of the 1980s used extrusions and revolutions as the main way to turn drawings into solids, and kept them as primitives or converted them to B-reps. General sweeps of solids along paths, needed for machining and motion studies, were studied with envelope theory by Wang and Wang in 1986 and by Martin and Stephenson in 1990.

## References
