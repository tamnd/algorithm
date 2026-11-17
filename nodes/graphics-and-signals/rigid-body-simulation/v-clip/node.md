---
tag: D7J6QE
kind: algorithm
slug: v-clip
name: V-Clip
aliases:
- Voronoi-clip algorithm
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: A robust closest-feature algorithm for convex polyhedra that clips edges against Voronoi regions and also handles penetration.
solves: [convex-collision-detection]
model: real-ram
complexity:
  vars: {n: the number of vertices of A, m: the number of vertices of B, s: the number of moves of one call}
  time: {call: O(s (n + m)), moves_worst: O(n m), step: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, recursive: false, exact: true}
history:
  year: 1998
  people: [Brian Mirtich]
  note: Mirtich described V-Clip in a 1997 MERL technical report and in ACM Transactions on Graphics in 1998, as a closest feature walk in the spirit of Lin-Canny that needs no tolerances and detects penetration.
prereqs: [lin-canny-closest-features, convex-polygon, voronoi-diagram]
see_also: [gjk-algorithm, convex-collision-detection, penetration-depth, expanding-polytope-algorithm, separating-axis-theorem, sweep-and-prune, polygon-clipping, minkowski-sum]
sources:
  - paper: doi:10.1145/285857.285860
    title: Brian Mirtich, V-Clip, fast and robust polyhedral collision detection, ACM Transactions on Graphics 17(3), 1998, 177 to 208
    locator: the feature states, the clipping of edges against Voronoi regions, the derivative checks, the local minimum handler, and the termination and robustness claims
  - paper: doi:10.1109/ROBOT.1991.131723
    title: Ming C. Lin and John F. Canny, A fast algorithm for incremental distance calculation, Proceedings of the 1991 IEEE International Conference on Robotics and Automation, 1008 to 1014
    locator: the closest feature walk that V-Clip refines
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 9, Convex-based Methods (the closest-features algorithms and V-Clip)
---

V-Clip finds the closest pair of features of two convex polyhedra, or reports that they penetrate. Like the [Lin-Canny algorithm](/lin-canny-closest-features/), it keeps a pair of features (vertices, edges or faces) and moves to a neighbor while a Voronoi region test fails, and it starts from the pair of the last time step. The difference is in the tests. V-Clip clips an edge against the Voronoi region of the other feature and uses the sign of the derivative of the distance at the clip points to choose the next feature. A vertex that lies behind a face goes to a special handler, which finds a closer face or reports penetration. The method needs no tolerances, and it cannot cycle.

## In plain words

Two convex objects are near each other. Each corner, side and face owns a zone of space: the points that are closest to it. You keep one part of each object and check if each part sits in the zone of the other.

V-Clip cuts a side where it leaves the zone of the other part. At a cut point it asks: does the side come closer to the other part past the cut? If yes, the neighbor past that wall is a better part. If no, you are done.

If a corner is behind a face of the other object, it may be inside the object. Then V-Clip looks at all faces. If the corner is behind all of them, the objects overlap, and V-Clip says so.

## The problem

The input is two convex polygons $A$ and $B$ with $n$ and $m$ vertices, strictly convex and counterclockwise, and a start pair of features. This page works in 2D: the features are vertices and closed edges, and each edge plays the role of a face of 3D, with the polygon behind it. The 1998 method is for convex polyhedra in 3D, with face states and clipping against face regions in addition. The output is either DISJOINT with a pair of features and points $p, q$ with $|p - q| = d(A, B) > 0$, or PENETRATION with features that witness an intersection. Touching counts as penetration here. V-Clip does not compute a [penetration depth](/penetration-depth/); for that, use the [expanding polytope algorithm](/expanding-polytope-algorithm/).

The Voronoi region of a vertex $v$ is the wedge between the two lines through $v$ perpendicular to its edges. Each of the two planes (lines, in 2D) has the edge on its other side as its neighbor. The region of an edge $e = [e_0, e_1]$ is the half strip on its outer side. Its two end planes have the end vertices as neighbors, and its base plane, the line of $e$, has the polygon behind it.

## The algorithm

```pseudo id=main
V-CLIP(A, B, fA, fB)
L1  loop
L2      if fA and fB are vertices a and b then
L3          if b violates a plane of VR(a) then fA ← the neighbor edge; continue
L4          if a violates a plane of VR(b) then fB ← the neighbor edge; continue
L5          if a = b then return PENETRATION(a, b) else return DISJOINT(a, b)
L6      if fA and fB are edges then
L7          if they intersect then return PENETRATION(fA, fB)
L8          replace the pair by the vertex-edge pair with the smallest end distance; continue
L9      let v be the vertex and e the edge, with e(λ) = e0 + λ(e1 - e0)
L10     if v is beyond an end plane of VR(e) then e ← the end vertex; continue
L11     if v is behind the line of e or on it then e ← HANDLE-LOCAL-MIN(v, polygon of e); continue
L12     clip e against the planes of VR(v): the interval [λl, λu] with the neighbors Nl, Nu
L13     if one plane excludes all of e then v ← the neighbor of that plane; continue
L14     if λl > λu then v ← the neighbor of a plane that the closest point of e to v violates; continue
L15     if Nl exists and D'(λl) > 0 then v ← Nl; continue
L16     if Nu exists and D'(λu) < 0 then v ← Nu; continue
L17     return DISJOINT(v, the closest point of e to v)
```

Here $D(\lambda) = |e(\lambda) - v|^2$, so $D'(\lambda) = 2 (e(\lambda) - v) \cdot (e_1 - e_0)$. If $D$ still decreases at the upper clip point $\lambda_u$, the closest point of $e$ to $v$ is past the clip, outside the wedge of $v$, on the side of the plane $N_u$. Line L13 is a simple exclusion and line L14 a compound exclusion, where each plane removes part of the edge and nothing is left. In 2D a compound exclusion means that each end of $e$ is outside a different plane.

```pseudo id=localmin
HANDLE-LOCAL-MIN(v, Q)
L18 k ← the edge of Q with the largest signed distance to v
L19 if that distance ≤ 0 then return PENETRATION(v, Q)
L20 return k
```

The handler is the only step that looks at more than the neighbors. In 2D the edge with the largest signed distance holds the closest point of $Q$ to $v$ when $v$ is outside $Q$. In 3D, Mirtich's handler does the same with the faces of the polyhedron.

## Example

Use the polygons of the [Lin-Canny example](/lin-canny-closest-features/): $A$ is the rectangle $a_0 = (0, 0)$, $a_1 = (4, 0)$, $a_2 = (4, 3)$, $a_3 = (0, 3)$, and $B$ is the triangle $b_0 = (7, 1)$, $b_1 = (10, 2)$, $b_2 = (8, 5)$. Edge $i$ goes from vertex $i$ to vertex $i + 1$, so $e_1$ of $A$ is the side $x = 4$ and $e_2$ of $B$ is the segment from $b_2$ to $b_0$. Start from the pair ($a_2$, $e_2$ of $B$).

**Move 1.** The vertex $a_2 = (4, 3)$ passes the end planes of $VR(e_2)$, with $(a_2 - b_2) \cdot (b_0 - b_2) = 12 \ge 0$ and $(a_2 - b_0) \cdot (b_0 - b_2) = -5 \le 0$, and it is on the outer side of $e_2$. Line L12 clips $e_2$ against $VR(a_2)$. The plane toward $a_1$ has direction $u = a_1 - a_2 = (0, -3)$, and $f(\lambda) = (e_2(\lambda) - a_2) \cdot u$ goes from $-6$ at $\lambda = 0$ to $6$ at $\lambda = 1$, so it cuts at $\lambda_u = 1/2$, with $N_u$ = edge $e_1$ of $A$. The plane toward $a_3$ gives $-16$ and $-12$, so it does not cut. At $\lambda_u = 1/2$ the point is $(7.5, 3)$, and $D'(1/2) = 2\,(3.5, 0) \cdot (-1, -4) = -7 < 0$. So line L16 fires: the distance still decreases past the cut, and $f_A \leftarrow e_1$. The feature distance drops from $14/\sqrt{17} \approx 3.40$ to 3.

**Move 2.** Now both features are edges. They do not meet. The four end distances are $\sqrt{10}$ for $a_1$, $\sqrt{196/17} \approx 3.40$ for $a_2$, $\sqrt{20}$ for $b_2$ and $3$ for $b_0$, so line L8 goes to ($e_1$ of $A$, $b_0$). The feature distance stays 3, and the dimension drops.

**Move 3.** The vertex $b_0 = (7, 1)$ is in the half strip of $e_1$ of $A$. Line L12 clips $e_1$, from $(4, 0)$ to $(4, 3)$, against $VR(b_0)$. The plane toward $b_2$ has direction $(1, 4)$ and values $-7$ and $5$ at the ends, so it cuts at $\lambda_u = 7/12$, the point $(4, 7/4)$. The plane toward $b_1$ does not cut. At the cut, $D'(7/12) = 2\,(-3, 3/4) \cdot (0, 3) = 9/2 > 0$, so the distance increases past the cut and line L16 does not fire. Line L17 returns DISJOINT with the vertex $(7, 1)$ and the point $(4, 1)$ of $e_1$, at $\lambda = 1/3 \in [0, 7/12]$. The distance is 3, which a brute force over all vertex-edge pairs confirms.

From the start pair ($a_0$, $b_1$), the walk takes 5 moves. At the state ($e_1$ of $A$, $b_1$) both ends of $e_1$ are outside the plane of $VR(b_1)$ toward $b_0$, with values 20 and 17. This is a simple exclusion, and line L13 moves $b_1$ to the edge $e_0$ of $B$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It uses the same potential as for Lin-Canny: the distance between the two current features, and then the sum of their dimensions. The clip lemma says that the clipped interval is exactly the part of the edge in the Voronoi region of the vertex, and that the plane that sets $\lambda_l$ is violated on all of $[0, \lambda_l)$. With the convexity of $D$, the derivative tests at lines L15 and L16 fire exactly when the closest point of the edge to the vertex is outside the clipped interval, and then the neighbor of the plane is strictly closer. So every move lowers the potential, no state repeats, and the walk ends after at most $4nm$ moves for every input and every start pair, also when the polygons overlap. A DISJOINT answer has mutual closest points, so it is the distance. A PENETRATION answer has a witness: two edges that meet, or a vertex inside the other polygon.

## Complexity

A move costs $O(1)$, except the handler of lines L18 to L20, which looks at all edges of one polygon. A call with $s$ moves costs $O(s(n + m))$ in the worst case and $O(s)$ without the handler. The proof bounds $s$ by $4nm$. Under coherent motion a call takes few moves, and the handler is rare. This is an observed behavior, as for Lin-Canny, not a proved bound. The extra space is $O(1)$, plus the feature graph of each polytope.

## Properties

- **No tolerances.** Each test is a sign of a dot product or cross product, and the proof holds for any choice at a tie. In 3D, Mirtich's method also has no tolerances. In his analysis, Lin-Canny needs tolerances and can cycle in degenerate cases.
- **Penetration.** The walk always ends, and it reports penetration with a witness instead of failing.
- **Exact with exact input.** With integer or rational coordinates the answer is exact, as the tests of this page check.
- **The same interface as Lin-Canny.** It needs the feature graph and returns closest features, which a simulator can use for contacts.

## Variants and improvements

- **3D.** The full method has the states vertex-vertex, vertex-edge, vertex-face, edge-edge and edge-face. Edges are clipped against vertex, edge and face regions, and the local minimum handler works on the face planes of the polyhedron.
- **Nonconvex objects.** Split each object into convex pieces, for example with [approximate convex decomposition](/approximate-convex-decomposition/), and run V-Clip on the pairs of pieces that the broad phase reports.
- **Penetration depth.** V-Clip gives a witness but no depth. For the depth of convex objects, use the [expanding polytope algorithm](/expanding-polytope-algorithm/) on the [Minkowski difference](/minkowski-sum/).
- **GJK.** The [GJK algorithm](/gjk-algorithm/) solves the same distance problem with a support function and no feature graph, and is the usual choice in game engines.

## When to use it

Use V-Clip when you need exact closest features of convex polyhedra under coherent motion and the objects can touch or penetrate, for example in rigid body simulation with distance based contacts. Prefer it to Lin-Canny in all new code. Prefer GJK when the shapes are curved or given by support functions, or when you need the distance only.

## Pitfalls

- **The handler is not local.** HANDLE-LOCAL-MIN looks at all faces. A version that only looks at the neighbors of $e$ can stop at a false local minimum behind a face.
- **Wrong neighbors in the clip.** Lines L15 and L16 must move to the neighbor of the plane that set $\lambda_l$ or $\lambda_u$, not to any violated plane. Keep the plane with the clip value.
- **The derivative at the ends.** If $\lambda_l = 0$ because no plane cut the start, there is no $N_l$ and no test at that end. A test at an end that was not cut moves to a wrong feature.
- **Touching.** A distance of 0 is a contact. Decide if your simulator wants it as penetration or as distance 0, and keep the closest features in both cases.
- **Orientation and convexity.** As for Lin-Canny, clockwise input or collinear vertices break the regions. Clean the input once.

## Implementations

## History

Mirtich developed V-Clip at MERL and published it as a technical report in 1997 and in ACM Transactions on Graphics in 1998. He kept the closest feature walk of Lin and Canny (1991) but replaced its point tests by the clipping of edges against Voronoi regions, added the derivative checks and the local minimum handler, and showed that the walk needs no tolerances and terminates also for penetrating objects. Later engines mostly moved to GJK, which needs no feature graph, but V-Clip remains the standard example of a robust closest feature walk.

## References
