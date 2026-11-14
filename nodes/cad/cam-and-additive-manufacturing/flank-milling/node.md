---
tag: 825AAT
kind: problem
slug: flank-milling
name: Five-axis flank milling
aliases:
- swarf milling
- side milling of ruled surfaces
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Machine a ruled or nearly ruled surface with the side of a cylindrical or conical tool in one pass, choosing the tool axes that minimise the geometric error.
prereqs: [ruled-surface, developable-surface, five-axis-tool-orientation]
see_also: [offset-surface, swept-volume, principal-axis-method, gouge-detection, iso-parametric-toolpath, collision-free-tool-orientation, toolpath-planning, cutter-location-data]
sources:
  - paper: doi:10.1016/0010-4485(95)00005-4
    title: Xiong-Wei Liu, Five-axis NC cylindrical milling of sculptured surfaces, Computer-Aided Design 27(12), 887-894, 1995
    locator: the placement of a cylindrical tool along the rulings of a ruled surface by offsets of points of the ruling
  - paper: "Sanjeev Bedi, Stephen Mann and Cornelia Menzel, Flank milling with flat end milling cutters, Computer-Aided Design 35(3), 293-300, 2003"
    locator: the placement of the tool tangent to the two boundary curves of a ruled surface
  - paper: "Cornelia Menzel, Sanjeev Bedi and Stephen Mann, Triple tangent flank milling of ruled surfaces, Computer-Aided Design 36(3), 289-296, 2004"
    locator: the placement of the tool tangent at three points and the reduction of the error by moving the tangent points
  - book: isbn:9783540420583
    title: Helmut Pottmann and Johannes Wallner, Computational Line Geometry, Springer, 2001
    locator: the chapters on ruled surfaces and developable surfaces, where the tangent plane along a ruling is constant exactly for developable surfaces
---

Five-axis flank milling cuts a surface with the side of a cylindrical or conical tool instead of its end. The tool axis lies along, or close to, the straight lines of a [ruled surface](/ruled-surface/), and one sweep of the tool along the surface finishes a strip as high as the cutting length of the tool. Flank milling is the standard way to finish the blades of impellers and the walls of aircraft parts, because it is much faster than point milling with a ball and leaves a smoother surface. The problem is to choose the axis positions so that the surface that the tool sweeps is as close as possible to the design. This is the manufacturing side of mechanical CAD, about the motion of a cutter, not the routing of a circuit. A clean dividing line runs through the problem: on a [developable surface](/developable-surface/) a cylinder that rolls along the rulings can cut the surface exactly, and on a surface that is ruled but not developable a cylinder cannot touch a whole ruling, so every method must trade some error.

## In plain words

Think of a ruler held against a curved wall. If the wall is part of a cylinder or a cone, or any surface you can roll out of a flat sheet, the ruler lies on it along a full straight line. A round bar held the same way does too. Slide the bar along, and it wipes the whole surface.

Now take a surface that is made of straight lines but is twisted, like a fan blade or a saddle. Along each of its straight lines the surface turns a little, so it faces a different way at the top than at the bottom. A round bar cannot follow this turn. It can lie flat at one point of the line only. Elsewhere it either cuts in a little or stands off a little. The job is to place the bar so that these small errors stay small.

## Definition

**Input.** A ruled surface $S(u, v) = a(u) + v\, w(u)$ with $|w(u)| = 1$, $u \in [u_0, u_1]$ and $v \in [0, H]$, with unit normal $n$ pointing out of the material. A tool: a cylinder of radius $R$, or a cone, whose cutting part covers the height $H$. A tolerance.

**Tool positions.** A motion of the tool is a family of axis lines $\ell(t)$, $t \in [0, 1]$, each given by a point and a direction. The tool at time $t$ is the solid set of points within distance $R$ of $\ell(t)$, cut to its length. The machined surface is the boundary of the material left after all positions, which near the part is the envelope of the tool surfaces.

**Error.** At a point $x$ of $S$, the error is the signed distance from $x$ to the machined surface along $n$: positive where material is left (undercut), negative where the tool went into the part (overcut or gouge).

**Goal.** Choose the motion so that the error is zero, or, where that is not possible, so that the largest absolute error is least, often with the side condition that there is no overcut. Smoothness of the axis motion and collisions with the rest of the part are further constraints, as in the general [tool orientation problem](/five-axis-tool-orientation/).

## Variants

- **Cylindrical tool.** The basic case, treated by the theorems below.
- **Conical tool.** A cone of revolution also has a constant normal along each of its straight lines, so the same dividing line holds. Cones are used for blades with a thick root.
- **Barrel and general tools.** A tool with a curved side can fit a non-developable surface better along a ruling, at the price of a more complex envelope.
- **Surface design for flank milling.** Change the design so it becomes developable, or so its error with a given tool is within tolerance, before any path is planned.
- **Multi-pass flank milling.** Cut a high wall in several strips, each with its own tool positions.
- **Wire cutting.** Wire EDM and hot-wire cutting move a straight wire along the rulings. The wire is a line, not a cylinder, so a ruled surface can be cut exactly along its rulings, up to the radius of the wire.

## Examples

**Exact cut of a developable surface.** Take a general cylinder, $a(u)$ a plane curve with unit normal $m(u)$ in its plane and $w = (0, 0, 1)$. The normal of $S$ is $m(u)$ at every point of the ruling. Put the tool axis at $\ell(u) = a(u) + R\, m(u) + v\, w$. Every point of the ruling is at distance $R$ from the axis in the direction $-m(u)$, which is at right angles to $w$, so the tool touches the whole ruling. If the radius of curvature of $a$ on the side of the tool is everywhere larger than $R$, the swept tool reproduces the surface with zero error. A cone, $a(u) = $ const, works in the same way with a conical tool.

**Error on a twisted surface.** The saddle $z = xy/L$ with $L = 200$ is ruled by the lines $x = $ const, with direction $(0, 1, x/L)$. Its normal is parallel to $(-y/L, -x/L, 1)$. On the ruling $x = 0$, the y axis, from $y = 0$ to $y = 40$, the normal turns about the ruling: it makes the angle $\arctan(y/200)$ with the z axis, which is $0°$ at $y = 0$, $5.71°$ at $y = 20$ and $11.31°$ at $y = 40$. Put a cylinder with $R = 5$ with its axis parallel to the ruling, tangent to the saddle at $y = 20$. It contains the whole ruling. At the ends it meets the surface at angles of $5.71°$ and $5.60°$, and a direct sampling of the cross-sections gives a gouge on one side of the ruling of depth 0.0248 at $y = 0$ and 0.0243 at $y = 40$, close to $R(1 - \cos\varphi)$ for the angle $\varphi$ between the normals. Moving the tool off the surface removes the gouge but leaves material of about the same size. Optimized placements reduce this error but, by the theorem below, cannot touch the whole ruling.

## Known algorithms

- **Offset methods.** Liu (1995) placed the cylinder from the offsets of one or two points of each ruling, often called the single point offset and double point offset methods. They are fast and smooth, and the error is zero for developable surfaces.
- **Tangency at the boundary curves.** Bedi, Mann and Menzel (2003) placed the tool tangent to the two boundary curves of the ruled surface, and Menzel, Bedi and Mann (2004) moved the tool to be tangent at three points, then moved the tangent points to reduce the error.
- **Global optimization.** Later methods choose all axis positions at once, to minimize the largest or the mean squared distance between the envelope of the tool and the design surface, with smoothness terms. Their results are measured on test blades, and the optimum depends on the error measure and the model of the envelope.
- **Envelope computation.** The machined surface is computed as the envelope of the moving tool, with the [swept volume](/swept-volume/) of the cylinder or cone, and compared with the design by [gouge detection](/gouge-detection/) methods.

## Bounds

**Theorem 1 (developable surfaces can be cut exactly).** Let $S$ be developable, so $\det(a', w, w') = 0$ for all $u$ and the unit normal $n(u)$ is constant along each ruling. Put the tool axis at $\ell(u) = \{a(u) + R\, n(u) + v\, w(u)\}$. Then the cylinder of radius $R$ about $\ell(u)$ touches $S$ along the whole ruling $u$. If moreover every point within distance $R$ of the surface $A(u, v) = S(u, v) + R\, n(u)$ lies on the outer side of $S$ near the ruling, which holds when the radius of curvature of $S$ on the tool side is larger than $R$, then the swept tool makes no gouge near $S$ and leaves no material on it: the error is zero.

*Proof.* Each point $S(u, v)$ is at the vector $-R\, n(u)$ from the axis point $a(u) + R\, n(u) + v\, w(u)$, and $n(u) \cdot w(u) = 0$, so its distance from the axis line is exactly $R$: the ruling lies on the tool surface. The normal of the tool surface at that point is the unit vector from the axis to the point, $-n(u)$ up to sign, which is the normal of $S$ there. So the two surfaces have the same tangent plane at every point of the ruling. All tool positions lie within distance $R$ of $A$, so by the condition on $A$ they stay on the outer side of $S$ near the ruling, and every point of $S$ is reached by the tool at its own ruling. Thus no material is left on $S$ and none is taken from inside. $\square$

**Theorem 2 (no line contact on a twisted ruling).** Let $\det(a', w, w') \ne 0$ at $u = u^*$. Then no circular cylinder and no cone of revolution touches $S$ along the whole ruling $u^*$, or along any segment of it. A cylinder or cone that contains the ruling has a tangent plane different from that of $S$ at every point of the ruling but at most one.

*Proof.* The normal direction of $S$ along the ruling is $N(v) = a' \times w + v\, (w' \times w)$. Both terms are at right angles to $w$, and they are linearly independent: if $w' \times w = 0$ then $w' = 0$ (as $w' \perp w$ from $|w| = 1$) and $\det(a', w, w') = 0$; if $w' \times w \ne 0$ and $a' \times w = k\,(w' \times w)$, then $(a' - k w') \times w = 0$, so $a' - k w'$ is parallel to $w$ and the determinant is 0 again. So $N(v)$ runs along a line in the plane at right angles to $w$ that misses the origin, and its direction turns strictly as $v$ changes: no two values of $v$ give the same normal line. Now let a straight segment lie on a circular cylinder. The squared distance of the point $x_0 + t\, w$ from the axis, with unit direction $d$, is a quadratic in $t$ with leading coefficient $|w - (w \cdot d) d|^2$, so it is constant only if $w$ is parallel to $d$. So the segment is parallel to the axis, and the normal of the cylinder along it is the same radial vector at every point. On a cone of revolution, every straight segment is a generator through the apex, and the normal is again constant along it. Line contact needs equal normal lines at every point of the segment, which $N(v)$ does not allow. If the tool contains the ruling, its constant normal can equal $N(v)$ for at most one $v$. $\square$

**Consequence.** Where the tool contains a twisted ruling, at every point but one its surface crosses $S$ at an angle $\varphi(v) > 0$, so on one side of the ruling the tool goes into the part. In the plane at right angles to the ruling, a circle of radius $R$ through the point whose center is off the normal of $S$ by the angle $\varphi$ reaches $R(1 - \cos\varphi) \approx R\varphi^2/2$ past the tangent line of $S$, to first order in the curvature of $S$. This is the size of the error in the example. If the tool does not contain the ruling, it misses part of it and leaves material there, or cuts it from a position where the same argument applies.

**What is proved and what is not.** Theorem 2 rules out a cut in which each tool position touches $S$ along a ruling. It does not by itself rule out a motion whose contact curves are not rulings. The machined surface of any motion of a cylinder is, near the part, an offset at distance $R$ of the ruled surface swept by the axis, so a zero-error cut of $S$ would need the parallel surface of $S$ at distance $R$ to be ruled. Published methods for non-developable surfaces report and minimize a nonzero error, and we give no proof here that no motion at all reaches zero error.

## Reductions

- **To the envelope of a family of lines.** The envelope of the cylinders about the axis lines is, near the part, the offset at distance $R$ of the ruled surface $A$ swept by the axes, as on the [offset surface](/offset-surface/) page. So choosing the motion is choosing a ruled surface $A$ whose offset is near $S$.
- **To developability.** By the two theorems, exact flank milling of a ruled surface with a cylinder along the rulings is the same as developability, $\det(a', w, w') = 0$, which is the test of the [ruled surface](/ruled-surface/) page.
- **To curve fitting.** Placing the tool tangent to the boundary curves turns each position into a small system of equations, and global methods turn the motion into a least squares or minimax fit of a ruled surface.

## Applications

Flank milling finishes the blades of compressor and pump impellers and of blisks, the walls of aircraft structural parts, the faces of molds and dies that are ruled by design, and the sides of cams. Designers of impeller blades often restrict the blade to ruled or developable shapes so that it can be flank milled, and the theorems above say why developable shapes are the safe choice.

## References
