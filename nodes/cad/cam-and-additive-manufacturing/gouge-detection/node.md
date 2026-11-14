---
tag: PGS3NK
kind: problem
slug: gouge-detection
name: Gouge detection and avoidance
aliases:
- gouge avoidance
- interference checking in machining
area: cad/cam-and-additive-manufacturing
level: core
summary: Detect and remove places where the tool cuts into the design surface, by local curvature checks and global tests against the rest of the part.
prereqs: [cutter-location-data, surface-curvature]
see_also: [inverse-tool-offset, nc-verification, z-map-model, offset-surface, swept-volume, collision-detection, bounding-volume-hierarchy, accessibility-cone]
sources:
  - paper: doi:10.1115/1.2901627
    title: J. H. Oliver, D. A. Wysocki and E. D. Goodman, Gouge detection algorithms for sculptured surface NC generation, Journal of Engineering for Industry 115(1), 1993, 139 to 144
    locator: the two methods, one from surface normals and the tool shape for the chordal deviation of a move, one over a whole pass for gouges in regions of high curvature variation
  - paper: "R. B. Jerard, R. L. Drysdale, K. Hauck, B. Schaudt and J. Magewick, Methods for detecting errors in numerically controlled machining of sculptured surfaces, IEEE Computer Graphics and Applications 9(1), 1989, 26 to 39"
    locator: the detection of gouges and of material left by simulation of the cut on vectors normal to the surface
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: the chapters on the fundamentals of tool-path generation and on gouge and collision
---

A gouge is a place where the cutting part of a tool removes material that belongs to the finished part. Gouge detection asks, for a given toolpath, where the tool cuts into the design surface and how deep. Gouge avoidance changes the path so that it does not. A gouge is *local* when the tool cuts into the surface near the point it is meant to touch, which happens on a concave surface whose radius of curvature is smaller than the tool radius. It is *global* when the tool hits some other part of the surface, such as a wall next to the point. A local test at each contact point, from the [curvature](/surface-curvature/) of the surface, finds the first kind but misses the second. A global test needs the distance from the tool to all of the part. This is a check on [cutter location data](/cutter-location-data/) in mechanical manufacturing: it is not the interference or overlap check of chip layout. When the shank, the holder or the spindle hits the part, the event is called a collision, and the same tests apply to those bodies.

## In plain words

A milling tool is meant to touch the finished surface of a part at one point at a time and remove everything above it. If the tool is too big for a hollow in the surface, its sides dig into the surface around that point. If a wall stands next to the point, the side of the tool can cut into the wall. In both cases the part is damaged, and the damage cannot be undone.

The check takes the planned tool positions and the shape of the part, and reports each position where the tool goes inside the part. A quick check compares the tool radius with how sharply the surface curves at the contact point. It finds the first kind of damage. The second kind needs a check of the tool against the whole part.

## Definition

**Input.**

- A part $P$, a closed regular solid, given by its boundary surface $S$: parametric patches or a triangle mesh with $n$ triangles.
- A tool: a solid of revolution $T$ about its axis, for example a ball end mill of radius $r$, a flat end mill, or a torus (bull-nose) cutter. $T(c, a)$ is the tool placed with reference point $c$ and axis $a$.
- A toolpath: CL points $(c_k, a_k)$, $k = 1, \dots, m$, with straight moves between consecutive ones (or a finer interpolation of the axis on a five-axis machine).
- A tolerance $\varepsilon \ge 0$.

**Output (detection).** For each position, or each move, whether the tool cuts into the part, and the depth. The tool at $(c, a)$ gouges when
$$ \operatorname{int} T(c, a) \cap \operatorname{int} P \ne \emptyset, $$
and the depth is the largest distance from a point of $T(c, a) \cap P$ to the boundary $S$. A move gouges when the [swept volume](/swept-volume/) of the tool over it meets $\operatorname{int} P$. A gouge is reported when its depth exceeds $\varepsilon$.

**Output (avoidance).** A new toolpath with no gouge deeper than $\varepsilon$, as close as possible to the given one: for example each $c_k$ lifted along $a_k$ by the least amount, or a change of the axis $a_k$ on a five-axis machine, or a smaller tool for some regions.

**Local and global.** Let the position be built from a cutter contact (CC) point $p \in S$ with unit normal $n$ pointing out of $P$, so that the tool touches $S$ at $p$. The gouge is *local* if the tool meets $\operatorname{int} P$ at points arbitrarily close to $p$, and *global* otherwise.

**Local criterion for a ball end mill.** Let the ball of radius $r$ touch $S$ at $p$ from outside, with center $p + r n$. Measure the normal curvature $\kappa(u)$ of $S$ at $p$ in each unit tangent direction $u$ with the sign that makes it positive where $S$ bends toward the ball, that is, where the part is concave. Let $\kappa_{\max}$ be the largest of them, the larger principal curvature with this sign.

- If $\kappa_{\max} > 1/r$, the ball gouges at $p$, locally.
- If $\kappa_{\max} < 1/r$, the ball meets $P$ near $p$ only at $p$.
- If $\kappa_{\max} = 1/r$, the second-order terms do not decide.

*Proof.* Put $p$ at the origin with $n$ along the $z$ axis. Near $p$ the part is $z \le f(x)$ for $x \in \mathbb{R}^2$ small, with $f(su) = \tfrac12 \kappa(u) s^2 + o(s^2)$ for unit $u$, by the definition of normal curvature. The lower half of the ball is $z \ge g(x) = r - \sqrt{r^2 - |x|^2} = |x|^2/(2r) + O(|x|^4)$. So $f(su) - g(su) = \tfrac12 (\kappa(u) - 1/r) s^2 + o(s^2)$. If $\kappa(u) > 1/r$ for some $u$, this is positive for small $s \ne 0$, and the points $(su, z)$ with $g(su) < z < f(su)$ are inside the ball and inside the part, at distance $O(s)$ from $p$. If $\kappa(u) < 1/r$ for every $u$, then by compactness of the circle of directions $f(x) - g(x) \le -c |x|^2$ for some $c > 0$ and small $x$, so near $p$ the ball is above the part except at $p$. $\square$

The criterion is the reason a CL surface built as the [offset surface](/offset-surface/) of $S$ at distance $r$ folds over itself at concave regions with radius of curvature below $r$. It says nothing about the rest of the part.

## Variants

- **Tool shape.** A ball end mill gives the criterion above. A flat or torus cutter touches with an edge or a torus, and the local test compares the curvature of the surface with the curvature of the tool profile in each direction. These depend on the tilt of the axis.
- **Three-axis and five-axis.** On a three-axis machine the axis is fixed, and avoidance can always lift the tool. On a five-axis machine the axis also changes, and avoidance can tilt it, which brings in the [accessibility](/accessibility-cone/) of the point and collisions of the holder.
- **Positions or moves.** A check at the CL points alone misses gouges between them. A check of the moves uses the swept volume of the tool, which for a ball and a straight move is a capsule.
- **Gouge and excess.** Verification also reports the opposite error, material left above the design surface. See [NC verification](/nc-verification/).

## Examples

**A local gouge.** Take a part in the plane of the profile (extend it along the third axis): the surface is a cylindrical groove $y = 5 - \sqrt{25 - x^2}$ for $|x| \le 3$, with flat lands $y = 1$ for $|x| \ge 3$, and the part lies below. The groove has radius of curvature $5$, concave, so $\kappa_{\max} = 1/5$ at the bottom $p = (0, 0)$.

A ball of radius $r = 6$ touching at $p$ has center $(0, 6)$ and lower boundary $6 - \sqrt{36 - x^2}$. Since $1/5 > 1/6$, the criterion predicts a gouge. The vertical depth, surface minus ball:

| $x$ | surface | ball bottom | depth |
| --- | --- | --- | --- |
| 1 | 0.1010 | 0.0839 | 0.0171 |
| 2 | 0.4174 | 0.3431 | 0.0743 |
| 3 | 1.0000 | 0.8038 | 0.1962 |

The ball also cuts the lands, up to $|x| = \sqrt{11} \approx 3.317$ where its bottom reaches $y = 1$. The deepest point measured along the normal is the edge $(3, 1)$ of the groove, at distance $\sqrt{34}$ from the center, so the penetration there is $6 - \sqrt{34} \approx 0.169$.

With $r = 4$ instead, $1/5 < 1/4$, and the ball with center $(0, 4)$ stays above the groove by $0.0260$, $0.1185$ and $0.3542$ at $x = 1, 2, 3$, and its bottom at $x = 3$ is $4 - \sqrt 7 \approx 1.354$, above the lands. No gouge.

**A global gouge.** Let the part be a floor $y \le 0$ with a wall $x \ge 4$ that rises to $y = 10$. A ball of radius $6$ touching the floor at $p = (0, 0)$ has center $(0, 6)$. The floor is flat, $\kappa_{\max} = 0 < 1/6$, so the local test passes. But the ball reaches $x = 6$ at height $6$, two units into the wall. Only a test against the whole part finds this.

## Known algorithms

- **Curvature test.** At each CC point, compare $\kappa_{\max}$ with $1/r$ (or the analogous test for other tools). It costs $O(1)$ per point given the derivatives of the surface, it is exact by the criterion above when the inequality is strict, and it finds only local gouges.
- **Distance test.** For a ball end mill, the tool at center $c$ gouges the regular solid $P$ if and only if the distance from $c$ to $P$ is less than $r$, and a straight move gouges if and only if the distance from the segment to $P$ is less than $r$. Against a triangle mesh this is a point to triangle or segment to triangle distance over all $n$ triangles, plus a test of whether $c$ is inside $P$, or a [bounding volume hierarchy](/bounding-volume-hierarchy/) query that skips far triangles, as in [collision detection](/collision-detection/). It finds local and global gouges.
- **Inverse tool offset.** For three-axis paths the [inverse tool offset](/inverse-tool-offset/) computes, on a grid, the lowest height of the tool that does not cut into any sample of the part. Positions computed this way avoid gouges at the samples by construction. Between samples the part can still rise above the tool.
- **Simulation.** [NC verification](/nc-verification/) on a [z-map](/z-map-model/) or a [dexel model](/dexel-representation/) cuts the stock with the swept tool and compares the result with the design surface. Jerard et al. (1989) measure the error on short vectors normal to the surface. It finds gouges and excess material, with the precision of the grid.
- **Normals and passes.** Oliver, Wysocki and Goodman (1993) give two methods for three-axis paths: one uses the surface normals and the tool shape to find the deviation of each move, and one looks along a whole pass for gouges where the curvature changes fast, in concave and convex regions.

What is proved: the curvature criterion, and the exactness of the distance test for a ball. What is measured: the speed of hierarchy queries and of simulation, which depends on the part and the path.

## Bounds

- **One position, ball against a mesh.** $O(n)$ time by checking every triangle. For rational input the squared distance from a point to a triangle is rational, so the comparison with $r^2$ is exact.
- **A whole path.** $O(mn)$ time for $m$ moves by the brute force. A hierarchy query can be faster on typical parts, but its worst case is still $O(n)$ per move.
- **No hardness.** Detection is a polynomial distance problem. Avoidance by lifting each three-axis position is also polynomial: for a ball, each triangle forbids an interval of heights on the vertical line of the position, and the tool is free at every height above the largest top of these $n$ intervals. Avoidance that also keeps the path short or smooth is a [toolpath planning](/toolpath-planning/) problem.

## Reductions

- **To distance queries.** For a ball end mill, gouge detection is the question "is the distance from a point or a segment to the part less than $r$". For a general tool it is the question whether two solids overlap, which is [collision detection](/collision-detection/).
- **To curvature.** Local gouge detection for a ball is a comparison of the principal curvatures of the surface with $1/r$.

## Applications

- Finishing of dies, molds and turbine blades, where the surface is free-form and a gouge scraps an expensive part.
- Choice of the tool: the largest ball radius with no local gouge on a surface is at most the smallest concave radius of curvature, a quick first bound for the tool size.
- Five-axis machining, where the same tests run for each candidate axis direction.

## References
