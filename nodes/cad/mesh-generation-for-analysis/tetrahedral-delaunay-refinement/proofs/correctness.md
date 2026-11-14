---
title: With B = 2 and input angles of at least 90 degrees, DELAUNAY-REFINE stops with a conforming Delaunay mesh of radius-edge ratio at most 2 and every edge at least half the smallest local feature size
proves: [correctness, termination]
status: full
---

**Claim.** Let $X$ be a piecewise linear complex that satisfies Shewchuk's projection condition (no two incident segments or facets meet at an angle below $90°$), let $B = 2$, and assume exact arithmetic. Let $\mathrm{lfs}_{\min}$ be the infimum of the local feature size over the domain. Then:

1. $\mathrm{lfs}_{\min} \ge d_{\min}/2 > 0$, where $d_{\min}$ is the smallest distance between two features of $X$ that do not intersect;
2. every vertex that DELAUNAY-REFINE inserts or rejects has insertion radius at least $\mathrm{lfs}_{\min}/2$, and every edge of every intermediate mesh has length at least $\mathrm{lfs}_{\min}/2$;
3. the loop of L2 stops, and the output is a Delaunay tetrahedralization that conforms to $X$ and has radius-edge ratio at most $2$ for every tetrahedron.

**What is cited.** Part 2 uses Lemma 3 of Shewchuk (1998) for the subsegment and subfacet cases. Its case analysis, which is where the projection condition is used, is not repeated here; we prove the tetrahedron case and show where the factor $1/\sqrt2$ comes from. The full proof is in Shewchuk (1998), Sections 5 and 6, and in Chapter 8 of Cheng, Dey and Shewchuk, *Delaunay Mesh Generation*. The proof also says nothing about dihedral angles, and slivers survive; see the last step.

**Step 1: the local feature size is bounded below.** A ball that meets two disjoint closed sets has diameter at least their distance. So every ball centered anywhere that meets two non-intersecting features has radius at least $d_{\min}/2$, and $\mathrm{lfs}(x) \ge d_{\min}/2$ for every $x$. Since $X$ has finitely many features, all closed, $d_{\min} > 0$. For the box $[0, a] \times [0, b] \times [0, c]$ with inner input vertices, the pairs that do not intersect are opposite faces, a face and an edge or corner it misses, two edges that do not meet, an inner vertex and any face, edge or corner, and two inner vertices; the smallest of their distances is $\min(a, b, c)$ or the distance from an inner vertex to a face or to another inner vertex.

**Step 2: the insertion radius of a circumcenter.** Let $t$ be a skinny tetrahedron of the current Delaunay mesh, with circumcenter $v$, circumradius $R$ and shortest edge $pq$ of length $\ell$, so $R > B \ell$. The circumsphere of $t$ has no vertex strictly inside, and the four vertices of $t$ lie on it, so the nearest vertex to $v$ is at distance exactly $R$: $r_v = R$, whether $v$ is then inserted or rejected. Say $q$ was inserted after $p$. When $q$ was inserted, $p$ was already there, so $\ell \ge r_q$, and $r_v = R > B r_q$. If $p$ and $q$ are both input vertices, they are two features that do not intersect, so $\ell \ge d_{\min} \ge \mathrm{lfs}_{\min}$, hence $r_v > B\, \mathrm{lfs}_{\min}$. This is the case $C = B$ of Lemma 3.

**Step 3: where $1/\sqrt2$ comes from.** Let a rejected circumcenter $p$ encroach a subsegment $ab$ with midpoint $v$ and half-length $\rho$, and suppose for this illustration that no vertex lies in the closed diametral ball of $ab$, so that $r_v = \rho$. The angle $apb$ is at least $90°$, so $|pa|^2 + |pb|^2 \le |ab|^2 = 4\rho^2$, and the nearer of $a, b$ is within $\sqrt2\,\rho$ of $p$. Then $r_p \le \sqrt2\,\rho$ and $r_v \ge r_p/\sqrt2$.

Let $p$ instead encroach a subfacet $f$ with circumcenter $v$ and circumradius $\rho$, where $f$ contains the orthogonal projection $p'$ of $p$ onto its plane. Every point of a triangle is within its circumradius of the nearest corner: the largest distance to the nearest corner over the triangle is attained at the circumcenter if it lies in the triangle, and otherwise at the midpoint of a side, at most half that side away. So $|p' - x| \le \rho$ for some corner $x$. And $|p - p'|^2 + |p' - v|^2 = |p - v|^2 \le \rho^2$, so $|p - p'| \le \rho$, and $|p - x|^2 = |p - p'|^2 + |p' - x|^2 \le 2\rho^2$. Again $r_p \le \sqrt2\,\rho = \sqrt2\, r_v$ when the equatorial ball holds no other vertex.

Shewchuk's Lemma 3 handles the general case: every inserted vertex $v$ has $r_v \ge \mathrm{lfs}(v)$, or it has a parent $p$ (the vertex that caused its insertion) with $r_v \ge C r_p$, where $C = B$ if $v$ is a tetrahedron circumcenter and $C = 1/\sqrt2$ if $v$ is a subfacet circumcenter or a subsegment midpoint. The parent of a subfacet circumcenter is a rejected tetrahedron circumcenter, and the parent of a subsegment midpoint is a rejected tetrahedron or subfacet circumcenter. The projection condition is what rules out the other cases, such as a vertex on one facet encroaching a subsegment of an incident facet.

**Step 4: induction.** Order all vertices, inserted and rejected, by the time they are created, and give an input vertex the insertion radius $\mathrm{lfs}_{\min}$, a lower bound for its distance to every other input vertex by Step 1. We show:

- a tetrahedron circumcenter has $r_v \ge \mathrm{lfs}_{\min}$;
- a subfacet circumcenter has $r_v \ge \mathrm{lfs}_{\min}/\sqrt2$;
- a subsegment midpoint has $r_v \ge \mathrm{lfs}_{\min}/2$.

All three bounds are at least $\mathrm{lfs}_{\min}/2$, and the input vertices satisfy it. Take a new vertex $v$ and assume the bounds for all earlier ones. If $r_v \ge \mathrm{lfs}(v)$, then $r_v \ge \mathrm{lfs}_{\min}$ and all three hold. Otherwise:

- $v$ is a tetrahedron circumcenter: $r_v \ge 2 r_p \ge 2 \cdot \mathrm{lfs}_{\min}/2 = \mathrm{lfs}_{\min}$, by Step 2 and the weakest bound for the parent;
- $v$ is a subfacet circumcenter with a rejected tetrahedron circumcenter as parent: $r_v \ge r_p/\sqrt2 \ge \mathrm{lfs}_{\min}/\sqrt2$;
- $v$ is a subsegment midpoint with a rejected tetrahedron circumcenter as parent: $r_v \ge \mathrm{lfs}_{\min}/\sqrt2 \ge \mathrm{lfs}_{\min}/2$; with a rejected subfacet circumcenter as parent: $r_v \ge \frac{1}{\sqrt2} \cdot \frac{\mathrm{lfs}_{\min}}{\sqrt2} = \mathrm{lfs}_{\min}/2$.

This is the dataflow graph of Shewchuk's Figure 12: every cycle passes through a tetrahedron circumcenter, and the products along the cycles are $B$, $B/\sqrt2$ and $B/2$, all at least $1$ when $B \ge 2$. With $B < 2$ the last cycle can shrink the radii, and the argument fails.

**Step 5: edges and termination.** An edge $uv$ of any intermediate mesh, with $v$ inserted after $u$, has $|uv| \ge r_v \ge \mathrm{lfs}_{\min}/2$. An edge between two input vertices has length at least $d_{\min} \ge \mathrm{lfs}_{\min}$. So the open balls of radius $\mathrm{lfs}_{\min}/4$ around the vertices are disjoint, and they lie in the domain grown by $\mathrm{lfs}_{\min}/4$, a bounded set of volume $V$. Hence there are at most $V / (\frac43 \pi (\mathrm{lfs}_{\min}/4)^3)$ vertices. Each pass of L2 inserts exactly one vertex: L3, L7 and L11 insert one, and a rejection in L6 or L10 is followed in the same pass by the insertion of a midpoint or a subfacet circumcenter. So the loop stops.

**Step 6: the output.** Bowyer-Watson insertion (L13) keeps the tetrahedralization Delaunay. When the loop stops, no subsegment is encroached, so each has a diametral ball with no vertex inside or on it except its ends; such a segment is an edge of the Delaunay tetrahedralization. No subfacet is encroached, so each has an equatorial ball free of vertices off its plane, and the vertices in its plane lie outside its circumcircle because the facet triangulation is Delaunay; such a triangle is a Delaunay face. So every subsegment and subfacet is in the mesh, and the mesh conforms to $X$. No tetrahedron is skinny, so every radius-edge ratio is at most $2$.

**Step 7: what is not proved.** Nothing above mentions dihedral angles. A sliver with vertices near a great circle of its circumsphere has $R/\ell$ close to $1/\sqrt2 < 2$, so it is never skinny and L8 never looks at it, and it can be in the output. The implementation's example contains one, with ratio $1.15$ and dihedral angles of $6.3°$ and $166.5°$.

**Remark on rounding.** The implementation rounds each new vertex to a grid of spacing $2^{-20}$, which moves it by at most $\frac{\sqrt3}{2} 2^{-20}$ and changes no step of the argument by more than that amount. The tests check the bound of Step 5 with a slack of two grid units. $\blacksquare$
