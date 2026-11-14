---
tag: HTBSV1
kind: definition
slug: accessibility-cone
name: Accessibility cone
aliases:
- visibility cone
- visibility map
area: cad/cam-and-additive-manufacturing
level: advanced
summary: The set of directions on the Gauss sphere from which a point or a face can be reached by a tool or a probe, used for setups and five-axis orientation.
prereqs: [convex-polytope, visibility-polygon]
see_also: [mold-parting-direction, gouge-detection, cutter-location-data, farkas-lemma, linear-programming-problem, set-cover, art-gallery-problem, offset-surface]
sources:
  - paper: "Tony C. Woo, Visibility maps and spherical algorithms, Computer-Aided Design 26(1), 1994, 6 to 16"
    locator: the visibility map of a surface as a region of the sphere of directions, the hemisphere of a face and the intersection for a set of faces, and its use for machining setups
  - paper: doi:10.1016/0010-4485(93)90103-U
    title: Lin-Lin Chen, Shuo-Yan Chou and Tony C. Woo, Parting directions for mould and die design, Computer-Aided Design 25(12), 1993, 762 to 768
    locator: complete and partial visibility, the visibility map of a surface as a convex region of the unit sphere, the division of a part into pockets, and the choice of a pair of opposite parting directions with the fewest cores
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: the chapters on gouge and collision and on multi-axis machining, where the tool axis must avoid the part
---

The accessibility cone of a point on a part is the set of directions along which the point can be reached from far away without passing through the part. Directions are unit vectors, points of the unit sphere, which in this use is often called the Gauss sphere, so the cone is drawn as a region on the sphere. For a face or a set of faces, it is the set of directions that reach all of their points. Machining uses it to choose the setups of a three-axis machine (one fixed direction per setup) and the axis of a five-axis tool at each point. Inspection uses it to aim a probe, and mold design uses it to find directions in which the halves of a mold can be pulled off. Woo (1994) calls the region on the sphere a visibility map. There are two notions that this page keeps apart: *ray accessibility*, where a ray of no width must miss the part, and *tool accessibility*, where a tool of some width must. The second is a subset of the first.

## Definition

Let $P \subset \mathbb{R}^3$ be a solid, closed and equal to the closure of its interior, and let $S^2$ be the unit sphere of directions.

**Accessibility of a point.** For $p \in \partial P$, the direction $d \in S^2$ is *accessible* at $p$ if the open ray from $p$ along $d$ misses the interior of $P$:
$$ A(p) = \{ d \in S^2 : p + s d \notin \operatorname{int} P \text{ for all } s > 0 \}. $$
$A(p)$ is the accessibility cone of $p$. (A cone in $\mathbb{R}^3$ is the set $\{ s d : s \ge 0, d \in A(p) \}$, and its trace on the sphere is $A(p)$.) It is closed: if $d_k \to d$ and the open ray along $d$ met the open set $\operatorname{int} P$ at some point, the rays along $d_k$ for large $k$ would meet it too.

**Accessibility of a set.** For a set $F \subseteq \partial P$, such as a face,
$$ A(F) = \bigcap_{p \in F} A(p). $$
A setup with direction $d$ reaches all of $F$ if and only if $d \in A(F)$.

**The local bound.** If $p$ is in the relative interior of a planar face with outward unit normal $n$, then $A(p)$ is contained in the closed hemisphere
$$ H(n) = \{ d \in S^2 : d \cdot n \ge 0 \}, $$
because a direction with $d \cdot n < 0$ enters the part right away. For a convex polytope, $A(p) = H(n)$ exactly: a convex solid lies on the inner side of the plane of each face, so the open ray along a direction with $d \cdot n \ge 0$ stays out of its interior. So for a set $F$ of faces of a convex polytope with normals $n_1, \dots, n_k$,
$$ A(F) = H(n_1) \cap \dots \cap H(n_k), $$
an intersection of hemispheres, a convex region of the sphere. For a nonconvex part, the other faces cut more directions away, and this formula is only an upper bound.

**Theorem (common direction).** There is a direction $d$ with $d \cdot n_i > 0$ for all $i$ if and only if $0$ is not in the convex hull of $n_1, \dots, n_k$. *Proof.* If such a $d$ exists and $0 = \sum_i \lambda_i n_i$ with $\lambda_i \ge 0$ and $\sum \lambda_i = 1$, then $0 = d \cdot 0 = \sum_i \lambda_i (d \cdot n_i) > 0$, a contradiction. Conversely, if $0$ is not in the compact convex hull $K$, let $d$ be the point of $K$ nearest to $0$. For every $x \in K$, the segment from $d$ to $x$ lies in $K$, so $|d + s(x - d)|^2 \ge |d|^2$ for small $s > 0$, which gives $d \cdot x \ge |d|^2 > 0$. In particular $d \cdot n_i > 0$. $\square$ This is Gordan's theorem, a form of the [Farkas lemma](/farkas-lemma/). Finding such a $d$, or deciding that none exists, is a [linear program](/linear-programming-problem/) in three variables, solvable in $O(k)$ time.

**Tool accessibility.** A real tool has a body. For a ball end mill of radius $r$ with a straight shank of the same radius, touching $p$ with its ball center at $c = p + r n$, the tool along axis $d$ is the set of points within distance $r$ of the ray $\{ c + s d : s \ge 0 \}$. It does not cut into the part if and only if every point of this ray is at distance at least $r$ from $P$, that is, the ray misses the open set $\{ y : \operatorname{dist}(y, P) < r \}$, the interior of the grown part. So tool accessibility for this tool is ray accessibility of the point $c$ with respect to the part grown by $r$, an [offset](/offset-surface/) of the part. Holders and spindles add more bodies and cut more directions away.

## Examples and non-examples

The pocket examples are in the plane of a cross section. For a square pocket the same computation in each of the two horizontal directions gives the cone.

- **A cube.** For a point inside the top face of a cube, $A(p)$ is the upper hemisphere. For the set of the top face and one side face, with normals $(0, 0, 1)$ and $(1, 0, 0)$, $A(F)$ is a quarter of the sphere, the directions with $d_x \ge 0$ and $d_z \ge 0$. The six faces have no common direction: $0 = \tfrac16 \sum n_i$ is in the hull of the normals, and indeed a cube cannot be machined from one setup.
- **A pocket, rays.** A block $y \le 0$ with a slot $-1 < x < 1$, $-1 < y \le 0$ cut out of it. At the middle of the slot floor, $p = (0, -1)$, the ray at angle $\alpha$ from the vertical, $d = (\sin \alpha, \cos \alpha)$, leaves the slot through its mouth if and only if $|\tan \alpha| \le 1$. So the accessibility cone is $|\alpha| \le 45^\circ$, much smaller than the hemisphere $|\alpha| \le 90^\circ$ of the local bound. At $|\alpha| = 45^\circ$ the ray passes through the edge $(\pm 1, 0)$ of the slot, which is allowed, since the edge is on the boundary.
- **The same pocket, a tool.** A ball end mill of radius $r = \tfrac12$ touching $p$ has its center at $c = (0, -\tfrac12)$. Its axis at angle $\alpha$ must stay at distance $\tfrac12$ from the edge $(1, 0)$. The vector from $c$ to the edge is $w = (1, \tfrac12)$, and the distance from the edge to the line of the axis is $|\cos \alpha - \tfrac12 \sin \alpha|$, which equals $\tfrac12$ at $\sin \alpha = \tfrac35$, $\cos \alpha = \tfrac45$. So the tool cone is $|\alpha| \le \arctan \tfrac34 \approx 36.87^\circ$, smaller than the ray cone of $45^\circ$. A numerical scan of the axis angle in steps of $0.01^\circ$ against the distance to the block gives the same limit.
- **An undercut.** A point on the underside of an overhang, with outward normal pointing down, has an accessibility cone in the lower hemisphere. A three-axis machine whose tool comes from above cannot reach it in any setup with the part upright.
- **Not a hemisphere test.** A face whose normal is in the hemisphere around $d$ can still be hidden from $d$ by another part of the solid, as the slot floor shows for $\alpha = 60^\circ$. The local bound is necessary, not sufficient.

## Related definitions

- **[Visibility polygon](/visibility-polygon/).** The set of points seen from one point. The accessibility cone is the set of directions from which one point is seen from infinity, a visibility question with the roles of the point and the viewer swapped.
- **[Mold parting direction](/mold-parting-direction/).** A part can be removed from a mold half along $d$ when every face of that half is reachable from $d$ in a stronger sense, along the motion of the whole part. Chen, Chou and Woo (1993) use visibility to choose such directions.
- **[Gouge detection](/gouge-detection/).** A direction $d$ is in the tool accessibility cone of $p$ exactly when the tool placed at $p$ with axis $d$ has no gouge, local or global.
- **[Set cover](/set-cover/).** Choosing the fewest setup directions such that each face is accessible from one of them is a set cover over the regions $A(F)$ of the sphere.
- **[Art gallery problem](/art-gallery-problem/).** The analogous question of guarding a region with few viewpoints, with points instead of directions.
- **[Cutter location data](/cutter-location-data/).** On a five-axis machine, the axis stored with each cutter location must be in the tool accessibility cone of its contact point.

## References
