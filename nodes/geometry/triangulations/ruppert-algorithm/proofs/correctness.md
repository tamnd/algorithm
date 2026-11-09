---
title: Ruppert's algorithm stops with a Delaunay mesh of quality B
proves: [correctness, termination]
status: full
---

**Setting.** The domain $\Omega$ is a strictly convex polygon, given counterclockwise, whose interior angles are all at least $90°$. Inside it lie finitely many segments and points that touch neither the boundary nor each other. The **features** are the boundary edges, the interior segments, the interior points, and the end points of all of these. The **segments** are the boundary edges and the interior segments. At every moment each segment is cut into **subsegments** by the vertices on it. A subsegment $ab$ is **encroached** by a vertex $p \ne a, b$ when $p$ lies in the closed disk with diameter $ab$, that is, when $(a - p) \cdot (b - p) \le 0$. The bound is $B \ge \sqrt 2$, given as $B^2$, and a triangle is **skinny** when its circumradius $R$ and shortest edge $\ell$ satisfy $R > B \ell$.

The **local feature size** $\mathrm{lfs}(x)$ of a point $x \in \Omega$ is the radius of the smallest closed disk centered at $x$ that meets two disjoint features. It is positive and continuous on the compact set $\Omega$, so $\lambda = \min_\Omega \mathrm{lfs} > 0$.

## Invariants

**(I1) The mesh is a Delaunay triangulation of the current vertices, and its union is $\Omega$.** Line L1 triangulates the convex boundary polygon as a fan and flips every edge whose opposite vertex lies strictly inside the circumcircle. Each flip increases the sorted vector of the triangles' angles in lexicographic order, so the flips stop, and then every edge is locally Delaunay, so the triangulation is Delaunay. After that, every vertex is inserted by Bowyer and Watson's method (lines L11 to L13). The triangles whose open circumdisk contains the new point $q$ form a connected region that is star-shaped from $q$. Removing them and joining $q$ to the boundary of that region gives the Delaunay triangulation with $q$ added. When $q$ lies on a boundary edge of the mesh, that edge is skipped, because the triangle it would give with $q$ is degenerate. Every inserted point lies in $\Omega$: midpoints of subsegments do, and circumcenters do by Lemma 2 below. So the union of the triangles stays the convex polygon $\Omega$.

**(I2) The subsegments partition the segments.** Initially the subsegments are the segments. Splitting replaces $ab$ by $am$ and $mb$, where $m$ is the midpoint.

**(I3) The queues are complete.** Every encroached subsegment is in the queue `enc`, and every skinny triangle of the mesh is in the queue `skinny`. Vertices are never removed, so a subsegment can become encroached only when a vertex is inserted, which is checked against all subsegments in `after_insert`, or when the subsegment is created, which is checked against all vertices in `check_sub`. Triangles are created only by insertion, and every new triangle is queued. A triangle whose circumcenter is rejected is queued again. Entries that have gone stale, such as split subsegments, deleted triangles, or triangles that are not skinny, are skipped.

By (I3), the test of line L5 runs only when no subsegment is encroached (line L3 comes first).

## Lemma 1: neighboring segments do not encroach

Let $S$ and $S'$ be segments that meet at a corner $o$ with angle at least $90°$. Write $S = \{o + s d : 0 \le s \le |S|\}$ and $S' = \{o + t e : 0 \le t \le |S'|\}$ with unit vectors $d$ and $e$, so $d \cdot e \le 0$. For a subsegment $ab$ of $S$ with $a = o + \alpha d$, $b = o + \beta d$, $0 \le \alpha < \beta$, and a vertex $p = o + t e$ with $t > 0$:

$$(a - p) \cdot (b - p) = \alpha \beta - t (\alpha + \beta)(d \cdot e) + t^2 \ge t^2 > 0 .$$

So $p$ does not encroach $ab$. A vertex on $S$ itself never encroaches a subsegment of $S$ either, since the line of $S$ meets the closed diametral disk only in the subsegment. $\square$

## Lemma 2: an accepted circumcenter lies in the domain

Suppose no subsegment is encroached, $t$ is a triangle with circumcircle $C$ and circumcenter $c$, and $c$ encroaches no subsegment. We show that $c$ lies in $\Omega$ and on no segment.

Suppose instead that the segment from an interior point $x$ of $t$ to $c$ meets a subsegment $ab$. Both $x$ and $c$ lie in the closed disk $D$ bounded by $C$. So the meeting point lies in $D$, and the line through $a$ and $b$ cuts $D$ in a chord $[l_1, l_2]$ that contains it. The vertices $a$ and $b$ are not in the open disk, because $t$ is Delaunay, so $[l_1, l_2] \subseteq [a, b]$. The center $c$ lies on the far side of the line from $x$, or on it. So the arc of $C$ on the side of $x$ is at most a semicircle, and every point of that arc lies in the closed disk with diameter $[l_1, l_2]$. That disk is contained in the closed disk with diameter $ab$. At least one vertex of $t$ is neither $a$ nor $b$, and it lies on that arc, so it encroaches $ab$. This contradicts the hypothesis. So no subsegment separates $c$ from $t$. Because $\Omega$ is convex and its boundary is covered by subsegments, $c \in \Omega$. And $c$ is on no subsegment, since a point of a subsegment encroaches it. $\square$

## Correctness of the output

When the loop of line L2 ends, both queues are empty. By (I3), no subsegment is encroached and no triangle is skinny. Take any subsegment $ab$. Its closed diametral disk contains no vertex but $a$ and $b$, so the diametral circle passes through $a$ and $b$ with every other vertex strictly outside it. Then $ab$ is an edge of every Delaunay triangulation of the vertices, in particular of the mesh. By (I2), every input segment is a union of mesh edges. By (I1), the mesh is a Delaunay triangulation that covers $\Omega$. Every triangle has $R \le B \ell$. By the law of sines, $\ell = 2 R \sin \theta_{\min}$, so its smallest angle satisfies $\sin \theta_{\min} \ge 1 / (2B)$. For $B = \sqrt 2$ this gives $\theta_{\min} \ge \arcsin(1 / (2 \sqrt 2)) \approx 20.7°$. Line L10 returns this mesh.

## Termination

The **insertion radius** $r_v$ of a vertex $v$ inserted by the loop is its distance to the nearest vertex present just before its insertion. For an input vertex, $r_v$ is its distance to the nearest other input vertex, and this is at least $\mathrm{lfs}(v)$, because the disk centered at $v$ through the nearest input vertex meets two disjoint features. We show by induction on the order of insertion that $r_v \ge \lambda$ for every vertex.

*Consequence for edges.* If $pq$ is an edge and $q$ is the newer end point, then $|pq| \ge r_q \ge \lambda$.

*A circumcenter $c$ inserted at line L9.* The circumdisk of the Delaunay triangle $t$ has no vertex inside, so $r_c = R$. Since $t$ is skinny, $R > B \ell \ge \sqrt 2 \, \ell$, where $\ell$ is its shortest edge. So $r_c > \ell \ge \lambda$.

*A midpoint $m$ of a subsegment $ab$ on a segment $S$, split at line L4.* Some vertex $p$ encroaches $ab$. The vertex $p$ is not on $S$ and not on a segment adjacent to $S$, by Lemma 1. It is not a circumcenter: an inserted circumcenter encroached no subsegment when it was inserted, and every later subsegment lies inside an earlier one, whose closed diametral disk contains the later one's. So $p$ is an input point or lies on a segment disjoint from $S$. Let $w$ be the vertex nearest to $m$. If $w \in \{a, b\}$, then $r_m = |ab| / 2 \ge |mp|$. Otherwise $|mw| < |ab| / 2$, so $w$ also encroaches $ab$, and by the same reasoning it lies on a feature disjoint from $S$. In both cases the disk centered at $m$ with radius $r_m$ meets $S$ and a feature disjoint from $S$, so $r_m \ge \mathrm{lfs}(m) \ge \lambda$.

*A midpoint $m$ split at line L8, because of a rejected circumcenter $c$ of a skinny triangle.* Line L8 runs only when no subsegment is encroached, so the closed disk with diameter $ab$ holds no vertex but $a$ and $b$, and $r_m = |ab| / 2$. The point $c$ lies in that disk of radius $r_m$ around $m$, so its distance to the nearer of $a$ and $b$ is at most $\sqrt 2 \, r_m$. That distance is at least $R$, because $a$ and $b$ are not inside the circumdisk of the triangle. So $r_m \ge R / \sqrt 2 > B \ell / \sqrt 2 \ge \ell \ge \lambda$. When several subsegments are hit, the later ones are checked again when their turn comes. Each one is still unencroached at that moment, except possibly by vertices added by the earlier splits in the same step, which lie on other segments and then fall under the previous case.

So every vertex is at distance at least $\lambda$ from every vertex inserted before it. Disks of radius $\lambda / 2$ around the vertices are therefore disjoint, and all of them lie in the $\lambda / 2$-neighborhood of $\Omega$, which has finite area. So only finitely many vertices are ever inserted. Every iteration of the loop either inserts a vertex or removes a queue entry, and each insertion adds finitely many entries. So the loop stops. $\square$

**Remark.** The bound $B \ge \sqrt 2$ is used in exactly two places: in the circumcenter case, to get $r_c > \ell$, and in the rejected case, to get $r_m > \ell$. With $B > \sqrt 2$ the same chain of inequalities gives $r_v \ge \mathrm{lfs}(v) / K$ for a constant $K$ that depends on $B$. That is the grading and size-optimality result of Ruppert, in the form proved by Shewchuk. Shewchuk also weakens the angle hypothesis to $60°$. Lemma 1 then fails for incident segments, but a vertex $p$ on a segment that meets $S$ at angle $\alpha \in [60°, 90°)$ and encroaches $ab$ gives $r_m \ge r_p / (2 \cos \alpha) \ge r_p$, and the induction goes through with the same kind of bound. The code and this proof keep Ruppert's $90°$.
