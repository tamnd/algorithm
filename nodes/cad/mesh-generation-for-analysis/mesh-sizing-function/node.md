---
tag: NF3354
kind: definition
slug: mesh-sizing-function
name: Mesh sizing function
aliases:
- mesh size field
- element size function
area: cad/mesh-generation-for-analysis
level: core
summary: A function giving the desired element size at each point, from curvature, local feature size and error, limited in gradient so sizes change gradually.
prereqs: [lipschitz-condition, triangulation]
see_also: [mesh-quality-measures, advancing-front-mesh-generation, delaunay-refinement, ruppert-algorithm, anisotropic-mesh-adaptation, quadtree-mesh-generation, medial-axis, polynomial-interpolation-error-theorem]
sources:
  - paper: "Houman Borouchaki, Frédéric Hecht and Pascal J. Frey, Mesh gradation control, International Journal for Numerical Methods in Engineering 43(6), 1998, 1143 to 1165"
    locator: the reduction of a size field so that sizes vary within a prescribed gradation, by size and by metric (general locator)
  - paper: doi:10.1006/jagm.1995.1021
    title: Jim Ruppert, A Delaunay refinement algorithm for quality 2-dimensional mesh generation, Journal of Algorithms 18(3), 548 to 585 (1995)
    locator: the definition of local feature size, its Lipschitz property, and the size optimality of the output with respect to it
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 6, Delaunay refinement in the plane (local feature size and the proof of size optimality and optimal grading)
  - paper: doi:10.1002/fld.1650081003
    title: Rainald Löhner and Paresh Parikh, Generation of three-dimensional unstructured grids by the advancing-front method, International Journal for Numerical Methods in Fluids 8(10), 1988, 1135 to 1149
    locator: the element size specified by a background grid and by point and line sources (general locator)
---

A mesh sizing function assigns to each point of the domain the edge length that the mesh should have near that point. Mesh generators read it to decide where to place vertices, and the user, the geometry and the solution error all contribute to it. It is usually limited in slope, as a Lipschitz function, so that neighboring elements have similar sizes. Size and shape are separate requirements: the sizing function says how big an element should be, and [mesh quality measures](/mesh-quality-measures/) say how well shaped it is.

## Definition

**Sizing function.** Let $\Omega \subset \mathbb{R}^d$ be the domain. A sizing function is a function $h : \Omega \to (0, \infty)$. A mesh **conforms** to $h$ with constants $0 < c_1 \le c_2$ if every edge $pq$ satisfies

$$c_1 h(p) \le |pq| \le c_2 h(p) \quad \text{and} \quad c_1 h(q) \le |pq| \le c_2 h(q).$$

Generators state this in different ways, for example by measuring each edge in the unit $h$, as $\int_{pq} ds / h$, and asking for values near 1. The constants are not part of the function.

**Gradation.** The function $h$ has gradation $L \ge 0$ if it is $L$-Lipschitz ([Lipschitz condition](/lipschitz-condition/)):

$$|h(x) - h(y)| \le L |x - y| \quad \text{for all } x, y \in \Omega.$$

A small $L$ forces sizes to change slowly. $L = 0$ means a uniform mesh.

**Sources of size.** A sizing function is usually the minimum of several parts.

- *User size.* A maximum size $H$, and point or line sources with small sizes near given places.
- *Local feature size.* For a planar input made of vertices and segments, $\operatorname{lfs}(x)$ is the radius of the smallest closed disk centered at $x$ that meets two disjoint input features. It is small where two features come close, for example in a thin slot, and Ruppert's algorithm builds meshes whose sizes are within constant factors of it.
- *Curvature.* A chord of length $\ell$ on a circle of radius $R$ deviates from the arc by the sagitta $s = R - \sqrt{R^2 - \ell^2/4}$, by the theorem of Pythagoras on the half chord. To keep $s \le \delta$ with $\delta < R$, the chord must satisfy $\ell \le 2 \sqrt{2 R \delta - \delta^2}$. With $R$ the local radius of curvature of the boundary, this gives $h_{\mathrm{curv}}(x) = 2\sqrt{2 R(x) \delta - \delta^2}$.
- *Error.* For linear interpolation on an interval of length $\ell$, the [interpolation error theorem](/polynomial-interpolation-error-theorem/) gives $|u - \Pi u| \le \ell^2 \max |u''| / 8$. To keep the error below $\varepsilon$, take $h = \sqrt{8 \varepsilon / |u''|}$. In several dimensions the Hessian gives a size that depends on direction, which is the metric of [anisotropic mesh adaptation](/anisotropic-mesh-adaptation/).

**Theorem (local feature size is 1-Lipschitz).** For all $x, y$, $\operatorname{lfs}(x) \le \operatorname{lfs}(y) + |x - y|$.

*Proof.* The closed disk with center $y$ and radius $\operatorname{lfs}(y)$ meets two disjoint features. It is contained in the disk with center $x$ and radius $\operatorname{lfs}(y) + |x - y|$, by the triangle inequality, so that disk also meets them. $\blacksquare$

**Theorem (the Lipschitz envelope).** Let $h_0 : \Omega \to [h_{\min}, \infty)$ with $h_{\min} > 0$, and let $L > 0$. Define

$$h(x) = \inf_{y \in \Omega} \big( h_0(y) + L |x - y| \big).$$

Then (1) $h_{\min} \le h \le h_0$; (2) $h$ is $L$-Lipschitz; (3) every $L$-Lipschitz function $g$ with $g \le h_0$ satisfies $g \le h$. So $h$ is the largest $L$-Lipschitz function below $h_0$.

*Proof.* (1) Take $y = x$ to get $h(x) \le h_0(x)$. Every term in the infimum is at least $h_{\min}$. (2) For any $y$, $h_0(y) + L|x - y| \le h_0(y) + L |z - y| + L |x - z|$. Taking the infimum over $y$ gives $h(x) \le h(z) + L |x - z|$, and the same with $x$ and $z$ exchanged. (3) If $g$ is $L$-Lipschitz and $g \le h_0$, then for every $y$, $g(x) \le g(y) + L |x - y| \le h_0(y) + L |x - y|$, so $g(x) \le h(x)$. $\blacksquare$

The envelope is the standard way to limit gradation: it lowers the size only where needed, never raises it, and is the least change that does the job. On a finite set of sample points, such as the vertices of a background grid, it is a shortest path problem with edge weights $L |x - y|$, solved by [Dijkstra's algorithm](/dijkstra/) started from all points at once, each with the initial label $h_0$. On a non-convex domain the distance should be measured inside $\Omega$. Otherwise a small size on one side of a thin wall lowers the size on the other side.

**Theorem (the grading bound).** Let $h$ be $L$-Lipschitz, and let a mesh conform to $h$ with constants $c_1 \le c_2$.

1. For all $x$ and all $y$ with $|x - y| \le r\, h(x)$: $(1 - L r)\, h(x) \le h(y) \le (1 + L r)\, h(x)$.
2. If $e$ and $e'$ are edges of the mesh joined by a path of $k$ edges, then $|e'| \le \frac{c_2}{c_1} (1 + L c_2)^k |e|$.

*Proof.* (1) is the Lipschitz condition with $|x - y| \le r h(x)$. For (2), let $p_0, p_1, \ldots, p_k$ be the path, with $p_0$ an end of $e$ and $p_k$ an end of $e'$. Each step has $|p_i p_{i+1}| \le c_2 h(p_i)$, so by (1) with $r = c_2$, $h(p_{i+1}) \le (1 + L c_2) h(p_i)$. Then $|e'| \le c_2 h(p_k) \le c_2 (1 + L c_2)^k h(p_0) \le \frac{c_2}{c_1} (1 + L c_2)^k |e|$. $\blacksquare$

So in a mesh that conforms to a Lipschitz size, edge lengths change at most geometrically with the number of edges between them. A mesh with a lower bound $\theta_{\min}$ on its angles has a grading of its own: by the law of sines, two edges of one triangle have a length ratio $\sin \alpha / \sin \beta \le 1/\sin \theta_{\min}$.

## Examples and non-examples

- *A point source.* Take $h_0 = 0.01$ at the origin and $h_0 = 1$ elsewhere, with $L = 0.2$. The envelope is $h(x) = \min(1, 0.01 + 0.2 |x|)$. Along a ray, edges that follow $h$ grow by a factor of $1.2$ each, so about 25 edges go from size $0.01$ to size $1$, over a distance of $4.95$. A uniform size $0.01$ would need 495 edges over the same distance.
- *A circle.* For a circle of radius $R = 1$ and a deviation tolerance $\delta = 0.01$, the curvature size is $2 \sqrt{0.02 - 0.0001} \approx 0.282$. A regular polygon with $n$ edges has sagitta $1 - \cos(\pi / n)$, which is $0.0093$ for $n = 23$ and $0.0102$ for $n = 22$, so 23 edges are needed.
- *Local feature size of a square.* For the unit square given by its 4 vertices and 4 sides, $\operatorname{lfs} = 1$ at each corner (the corner and the opposite side are disjoint features) and $\operatorname{lfs} = 1/2$ at the center (two opposite sides).
- *A thin slot.* Two parallel segments at distance $w$ give $\operatorname{lfs} \le w$ between them, so a mesh that conforms to lfs puts elements of size about $w$ across the slot, whatever the size elsewhere.
- *Non-example.* The step function $h_0 = 0.01$ on the left half of a square and $h_0 = 1$ on the right half is not Lipschitz. A mesh that follows it closely has tiny elements next to large ones at the jump, and these elements are badly shaped. Its envelope with $L = 0.2$ is a valid sizing function.

## Related definitions

- [Mesh quality measures](/mesh-quality-measures/): shape, as opposed to size.
- [Ruppert's algorithm](/ruppert-algorithm/) and [Delaunay refinement](/delaunay-refinement/): they produce meshes graded to the local feature size, with the number of triangles within a constant factor of the least possible.
- [Advancing front mesh generation](/advancing-front-mesh-generation/): places each new point at a distance given by the sizing function, usually stored on a background grid.
- [Quadtree mesh generation](/quadtree-mesh-generation/): a balanced quadtree is a discrete sizing function in which neighboring cells differ in size by a factor of at most 2.
- [Anisotropic mesh adaptation](/anisotropic-mesh-adaptation/): replaces the scalar size by a metric tensor.
- [Medial axis](/medial-axis/): for a smooth curved boundary, the local feature size of a boundary point is usually defined as its distance to the medial axis.

## References
