---
tag: 4489K1
kind: concept
slug: signed-distance-function
name: Signed distance function
aliases:
- SDF
area: graphics-and-signals/ray-tracing
level: intro
summary: A function of space whose value is the distance to a surface, negative inside the solid and positive outside. It is 1-Lipschitz, and its gradient has length 1 where it exists.
prereqs: [euclidean-distance]
see_also: [implicit-surface, sphere-tracing, ray-marching, eikonal-equation, fast-marching-method, level-set-method, distance-transform, medial-axis]
sources:
  - book: isbn:9780387954820
    title: Stanley Osher and Ronald Fedkiw, Level Set Methods and Dynamic Implicit Surfaces, Springer, 2003
    locator: Chapter 2, Signed Distance Functions (the definition, the property |∇φ| = 1, and the union, intersection and complement of solids)
  - paper: doi:10.1007/s003710050084
    title: John C. Hart, Sphere tracing, a geometric method for the antialiased ray tracing of implicit surfaces, The Visual Computer 12(10), 1996, pages 527 to 545
    locator: Section 2.1 (Definitions 1 to 3, signed distance bounds and Theorem 1), Section 2.5 (union, complement and Theorem 3 on intersection) and Appendix A (distances to the plane, sphere, cylinder, cone and torus)
  - paper: doi:10.1109/TVCG.2006.56
    title: Mark W. Jones, J. Andreas Bærentzen and Milos Sramek, 3D distance fields, a survey of techniques and applications, IEEE Transactions on Visualization and Computer Graphics 12(4), 2006, pages 581 to 599
    locator: the definition of the signed distance field, its properties, and the methods that compute it on a grid
  - paper: doi:10.1145/344779.344899
    title: Sarah F. Frisken, Ronald N. Perry, Alyn P. Rockwood and Thouis R. Jones, Adaptively sampled distance fields, a general representation of shape for computer graphics, SIGGRAPH 2000, pages 249 to 254
    locator: the whole paper (distance fields stored in an octree with cells refined where the field is not well approximated)
---

A signed distance function of a solid $A$ with surface $S = \partial A$ is the function $d : \mathbb{R}^3 \to \mathbb{R}$ with $|d(x)|$ equal to the [Euclidean distance](/euclidean-distance/) from $x$ to $S$, and with the sign negative inside $A$ and positive outside. The surface is the zero set of $d$, so a signed distance function is one special way to describe an [implicit surface](/implicit-surface/). It is special because the value tells you more than inside or outside: it tells you how far you can move in any direction before you can touch the surface. [Sphere tracing](/sphere-tracing/) uses exactly this to step along a ray, and [ray marching](/ray-marching/) uses it to refine its fixed steps. Some sign conventions put the negative values outside; this page uses negative inside, as Osher and Fedkiw and Hart do.

## In plain words

Pick a point in space and ask the shape one question: how far is your nearest surface point? The answer is a number. Put a minus sign on it when the point is inside the shape. That number, for every point in space, is the signed distance function.

The useful part is what the number promises. If it says 3, then a ball of radius 3 around the point does not touch the shape. You can jump 3 units in any direction and still not cross the surface. Programs that draw these shapes use this promise to take large, safe steps through empty space and small steps near the surface. Two shapes combine with a minimum (put them together) or a maximum (keep only what they share), but the combined number is sometimes only a safe underestimate, not the exact distance.

## The idea

Let $A \subset \mathbb{R}^3$ be a closed solid with boundary surface $S$. Write $\operatorname{dist}(x, S) = \min_{y \in S} \lVert x - y \rVert$. The signed distance function is

$$d(x) = \begin{cases} -\operatorname{dist}(x, S) & x \in A, \\ \phantom{-}\operatorname{dist}(x, S) & x \notin A. \end{cases}$$

So $d = 0$ exactly on $S$. Four properties make it useful.

**It is 1-Lipschitz.** For all $x, y$, $|d(x) - d(y)| \le \lVert x - y \rVert$. If $x$ and $y$ are on the same side, this is the triangle inequality for the distance to a set. If they are on opposite sides, the segment from $x$ to $y$ meets $S$ at some point $z$, and $|d(x) - d(y)| = \operatorname{dist}(x,S) + \operatorname{dist}(y,S) \le \lVert x - z \rVert + \lVert z - y \rVert = \lVert x - y \rVert$. The open ball of radius $|d(x)|$ around $x$ contains no point of $S$. Hart calls it an *unbounding sphere*; it is the whole reason that sphere tracing works.

**Its gradient has length 1 where it is differentiable.** If $d$ is differentiable at $x \notin S$, let $y$ be a nearest surface point. Along the segment from $x$ toward $y$, $d$ changes at rate exactly 1, so the directional derivative in that direction is 1 in absolute value; the Lipschitz bound gives $\lVert \nabla d \rVert \le 1$. So $\lVert \nabla d(x) \rVert = 1$, and $\nabla d(x)$ points from $y$ to $x$. This makes $d$ a solution of the [eikonal equation](/eikonal-equation/) $\lVert \nabla d \rVert = 1$ with $d = 0$ on $S$. More precisely, the unsigned distance is the viscosity solution, so grid methods for the eikonal equation such as the [fast marching method](/fast-marching-method/) compute distance fields, and the [level set method](/level-set-method/) uses them to reset a drifting level set function back to a signed distance. On the surface itself, $\nabla d$ is the outward unit normal, which is how renderers get normals from an SDF.

**It is not differentiable everywhere.** At a point with two or more nearest surface points, $d$ has a kink. These points form the [medial axis](/medial-axis/) of the solid, for example the center of a sphere or the diagonal planes inside a box. For a smooth closed surface, $d$ is smooth in a thin shell around $S$ whose thickness is the distance from $S$ to the medial axis. A function that satisfies $\lVert \nabla f \rVert = 1$ almost everywhere is not always a distance function: the eikonal equation has many almost-everywhere solutions, and the distance is the one selected by the viscosity condition.

**Combinations by min and max.** If $d_A$ and $d_B$ are the signed distance functions of solids $A$ and $B$, then

- union: $\min(d_A, d_B)$. Exact outside $A \cup B$, because the nearest point of the union boundary is then the nearer of the two nearest points. Inside, it can be too small in absolute value: it is only a bound.
- intersection: $\max(d_A, d_B)$. Exact inside $A \cap B$; outside, it is only a lower bound of the distance (Hart, Theorem 3).
- complement: $-d_A$. Exact.
- subtraction $A \setminus B$: $\max(d_A, -d_B)$, a bound.

The minimum and the maximum of 1-Lipschitz functions are again 1-Lipschitz, and they have the right sign everywhere. So the combined function is always a *signed distance bound*: $|f(x)| \le \operatorname{dist}(x, f^{-1}(0))$. Hart's Definition 2 makes this the weaker object that sphere tracing needs. Any Lipschitz function $f$ with constant $L$ becomes a distance bound after division by $L$ (Hart, Theorem 1). Smooth blends, twists and non-uniform scales give bounds of this kind, not exact distances.

**Closed forms for primitives.** All of these are exact everywhere:

| primitive | signed distance at $p$ |
|---|---|
| sphere, center $c$, radius $r$ | $\lVert p - c \rVert - r$ |
| half space $n \cdot p + h \le 0$, $\lVert n \rVert = 1$ | $n \cdot p + h$ |
| box centered at 0, half extents $b$ | $\lVert \max(q, 0) \rVert + \min(\max(q_x, q_y, q_z), 0)$, with $q = \lvert p \rvert - b$ per axis |
| torus around the $y$ axis, radii $R$ and $r$ | $\lVert (\sqrt{p_x^2 + p_z^2} - R,\ p_y) \rVert - r$ |

For the box, outside, $\max(q, 0)$ is the offset from the nearest point of the box; inside, all $q_i < 0$ and the nearest face is at distance $-\max_i q_i$.

**How it differs from close ideas.** An [implicit surface](/implicit-surface/) is the zero set of any function $f$; the values of $f$ away from the surface carry no metric meaning, and $f(x) = 0.1$ can be far from or near to the surface. A signed distance function is the one function among all of these whose values are distances. A [distance transform](/distance-transform/) computes distances on the pixels or voxels of a grid, from a set of marked cells; a stored grid of signed distances, often called a distance field, is a sampled SDF. [Sphere tracing](/sphere-tracing/) is an algorithm that needs an SDF or a distance bound. [Ray marching](/ray-marching/) with fixed steps works with any function, but it can use an SDF to know that no surface lies between two samples.

## Examples

**A box.** Let $b = (1, 1, 1)$. At $p = (2, 3, 0.5)$, $q = (1, 2, -0.5)$, the positive part is $(1, 2, 0)$, and $d = \sqrt 5 \approx 2.236$: the nearest point is the box edge point $(1, 1, 0.5)$. At $p = (0.5, 0.2, 0)$, $q = (-0.5, -0.8, -1)$, all negative, so $d = -0.5$, the distance to the face $x = 1$. At $(2, 2, 2)$, $d = \sqrt 3 \approx 1.732$, the distance to the corner. At the center of a box with $b = (1, 0.6, 0.4)$, $d = -0.4$; the center lies on the medial axis, and the gradient does not exist there.

**A torus.** With $R = 1$ and $r = 0.25$, the point $(2, 0, 0)$ has $d = \lvert 2 - 1 \rvert - 0.25 = 0.75$, and the origin also has $d = 0.75$: it is at distance 1 from every point of the center circle.

**Union is exact only outside.** Take two unit spheres with centers $(\pm 0.75, 0, 0)$. At $(0, 2, 0)$, $\min(d_A, d_B) = \sqrt{0.75^2 + 4} - 1 \approx 1.1360$, and the nearest point of sphere $A$ is outside sphere $B$, so this is the true distance to the union. At the origin, $\min(d_A, d_B) = -0.25$. But the nearest point of each sphere is inside the other sphere, so it is not on the boundary of the union. The nearest boundary point is on the circle where the two spheres meet, at distance $\sqrt{1 - 0.75^2} \approx 0.6614$. The true value is $-0.6614$, and $-0.25$ is only a bound.

**Intersection is exact only inside.** Take two unit spheres with centers $(\pm 0.5, 0, 0)$. Their intersection is a lens. At $(0, 2, 0)$, $\max(d_A, d_B) = \sqrt{0.25 + 4} - 1 \approx 1.0616$. The lens is nearest at its rim, a circle of radius $\sqrt{0.75}$ in the plane $x = 0$, so the true distance is $2 - \sqrt{0.75} \approx 1.1340$. The max underestimates by about 0.07. A sphere tracer that uses the max is still safe; it takes a few more steps.

**Subtraction.** A unit cube $b = (1, 1, 1)$ minus a sphere of radius 1.2 at its center: at the center, $\max(d_{\text{box}}, -d_{\text{sphere}}) = \max(-1, 1.2) = 1.2$, outside the result, which is right because the sphere removed the center. At $(0.9, 0.9, 0.9)$, near a corner, the value is $\max(-0.1, -0.3588) = -0.1$: inside the solid, 0.1 from the nearest cube face.

The implementation checks each exact primitive against the minimum distance to tens of thousands of points sampled on its surface, with the known covering radius of the sample grid as the tolerance. It checks that the union is exact outside and a bound inside, that the intersection is exact inside and a bound outside, that all combinations are 1-Lipschitz, and that the numerical gradient of the box SDF has length 1 away from its medial axis.

## Where it is used

- **Rendering implicit shapes.** [Sphere tracing](/sphere-tracing/) steps along each ray by the SDF value and needs no root bracketing. Scenes built from primitives with min, max and smooth blends are the usual content of SDF renderers and of the demo scene.
- **Normals and offsets.** The gradient of $d$ on the surface is the unit normal. The offset surface at distance $r$ is the zero set of $d - r$, which rounds a shape, and $|d| - r$ turns a solid into a shell of thickness $2r$.
- **Collision and proximity.** A stored distance field answers "how deep is this point inside" in constant time, which physics engines and robot motion planners use for [collision detection](/collision-detection/).
- **Surface reconstruction and meshing.** Fitting a distance field to scan data and then extracting its zero set with [marching cubes](/marching-cubes/) or [dual contouring](/dual-contouring/) is a standard path from points to a mesh. [Isosurface extraction](/isosurface-extraction/) needs only the sign, but the distance values place vertices well.
- **Level set methods.** The [level set method](/level-set-method/) moves a front by evolving a function whose zero set is the front, and periodically reinitializes the function to a signed distance so that its gradient stays near length 1.
- **Fonts and 2D graphics.** Glyphs stored as low resolution distance textures stay sharp under magnification, because bilinear interpolation of a distance gives a good approximation of the edge.
- **Adaptive storage.** Adaptively sampled distance fields store the SDF in an [octree](/octree/) that is fine only where the field bends. Jones, Bærentzen and Sramek survey the ways to compute and store 3D distance fields.

## References
