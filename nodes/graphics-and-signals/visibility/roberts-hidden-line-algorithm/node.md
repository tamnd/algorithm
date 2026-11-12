---
tag: T1KFDC
kind: algorithm
slug: roberts-hidden-line-algorithm
name: Roberts' hidden line algorithm
aliases:
- Roberts' algorithm
area: graphics-and-signals/visibility
level: core
summary: Remove hidden lines in a scene of convex polyhedra. Drop the edges of back faces, then clip each other edge against each body by solving linear inequalities in the edge parameter.
solves: [hidden-line-removal]
model: real-ram
complexity:
  vars: {n: the total number of edges and faces in the scene, f: the largest number of faces of one body}
  time: {worst: O(n^2 (f + log n))}
  space: {extra: O(n)}
properties: {deterministic: true, in_place: false, online: false}
history:
  year: 1963
  people: [Lawrence G. Roberts]
  note: Roberts gave the first hidden line method in his 1963 MIT PhD thesis on machine perception of three-dimensional solids.
prereqs: [hidden-line-removal, back-face-culling, convex-polytope]
see_also: [hidden-line-removal, appel-hidden-line-algorithm, silhouette-edge, back-face-culling, hidden-surface-removal, object-space-vs-image-space, half-plane-intersection, warnock-algorithm]
sources:
  - url: https://dspace.mit.edu/handle/1721.1/11589
    title: Lawrence G. Roberts, Machine Perception of Three-Dimensional Solids, PhD thesis, Massachusetts Institute of Technology, 1963 (also MIT Lincoln Laboratory Technical Report 315)
    locator: the part on displaying the solids from a new viewpoint with the hidden lines removed
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the description of Roberts' algorithm among the object space algorithms
  - book: isbn:9780070535480
    title: David F. Rogers, Procedural Elements for Computer Graphics, second edition, McGraw-Hill, 1998
    locator: Chapter 4, the section on the Roberts algorithm (volume matrices and the parametric test of an edge against a body)
---

Roberts' hidden line algorithm draws a scene of convex polyhedra with the hidden parts of the edges removed. It works in object space with exact geometry: for each edge and each body, it solves a small system of linear inequalities that gives the part of the edge behind the body. Lawrence G. Roberts gave it in his 1963 MIT thesis, and it is the first published solution of [hidden line removal](/hidden-line-removal/). It needs convex bodies; for general meshes, [Appel's algorithm](/appel-hidden-line-algorithm/) counts how many faces cover each point of an edge instead. This page is the line drawing method. Methods that find the visible part of each surface or the color of each pixel are on the [hidden surface removal](/hidden-surface-removal/) page.

## In plain words

Each object in the scene is a convex solid, such as a box or a pyramid. First, each object hides its own back: an edge where two faces meet that both point away from you is behind the object, so you drop it. Then you test each other edge against each other object. For a point on the edge, draw the line from that point toward your eye. The point is hidden if that line passes through the inside of the object. Because the object is convex, the inside is the set of points that are on the inner side of every face. Each face gives one simple condition, and together the conditions give the hidden part of the edge as one piece. Remove all the hidden pieces, and what is left of the edge is drawn.

## The problem

The input is a list of convex polyhedra $B_1, \dots, B_m$ and a viewer. Body $B_j$ is given by its vertices, its edges and its faces. Face $k$ of $B_j$ lies in the plane $a_k \cdot x = b_k$ with the outward normal $a_k$, so

$$B_j = \{x : f_k(x) = a_k \cdot x - b_k \le 0 \text{ for every face } k\}.$$

The viewer is a homogeneous point $e = (e_x, e_y, e_z, e_w)$: with $e_w = 1$ it is an eye at the point $(e_x, e_y, e_z)$, and with $e_w = 0$ it is a direction toward the viewer for a parallel (orthographic) view. Extend $f_k$ to homogeneous points by $f_k(x, w) = a_k \cdot x - b_k w$. A point $p$ is *hidden* if the segment from $p$ toward the viewer contains a point in the interior of some body. The output is, for each edge, the list of its visible parts as parameter ranges $[t_0, t_1] \subseteq [0, 1]$.

## The algorithm

The points on the way from $p$ to the viewer are, in homogeneous form, $p + \alpha e$ with $\alpha > 0$; for an eye point this is the point $(p + \alpha e_{xyz})/(1 + \alpha)$ of the segment from $p$ to the eye. Since $f_k$ is linear and $1 + \alpha > 0$, the sign of $f_k$ at that point is the sign of $f_k(p) + \alpha f_k(e)$. On the edge $p(t) = p_0 + t (p_1 - p_0)$, the condition "$p(t) + \alpha e$ is inside $B_j$" is

$$f_k(p_0) + t\, f_k(p_1 - p_0) + \alpha\, f_k(e) < 0 \quad \text{for every face } k \text{ of } B_j,$$

a set of linear inequalities in the two unknowns $t$ and $\alpha$. This is Roberts' observation: in homogeneous coordinates, the hidden test of an edge against a convex body is a two-variable linear system for both parallel and perspective views. Roberts stored the face planes of a body as the columns of a matrix, the *volume matrix*, so that all the values $f_k$ come from one product of a point with that matrix.

A face *faces the viewer* if $f_k(e) > 0$: the eye is on the outer side of its plane, or the view direction points to its outer side.

```pseudo id=main
ROBERTS(B_1, ..., B_m, e)        ▷ convex bodies; e the viewer in homogeneous form
L1  for each body B do
L2      for each face k of B do front(k) ← sign of f_k(e)
L3  for each body B_i and each edge p0 p1 of B_i do
L4      if both faces of the edge have front < 0 then mark the edge hidden; continue
L5      H ← empty list of open intervals
L6      for each body B_j with j ≠ i do
L7          Q ← the rectangle 0 ≤ t ≤ 1, 0 ≤ α ≤ α_max
L8          for each face k of B_j do
L9              Q ← Q ∩ { (t, α) : f_k(p0) + t f_k(p1 − p0) + α f_k(e) ≤ 0 }
L10         if Q has positive area then add (min t over Q, max t over Q) to H
L11     output [0, 1] minus the union of the intervals in H
```

Line L4 is the back face test of each body against itself (see [back-face culling](/back-face-culling/)). Line L7 needs an upper bound $\alpha_{\max}$: take a face $k$ with $f_k(e) > 0$, which exists because the viewer is outside the body; for $\alpha > \max(-f_k(p_0), -f_k(p_1))/f_k(e)$, its inequality fails on the whole edge. Lines L8 and L9 clip a convex polygon by one half-plane at a time (see [half-plane intersection](/half-plane-intersection/)). The set of pairs that satisfy the strict inequalities is the interior of $Q$, so its projection on the $t$ axis is the open interval of line L10. If $Q$ has zero area, the edge only touches the body or the line of sight only grazes it, and nothing is hidden.

## Example

The scene has a long box, the rod $[0, 10] \times [0, 1] \times [0, 1]$, and a plate $[4, 6] \times [-5, 5] \times [3, 4]$ above it. The view is parallel, from the direction $e = (1, 1, 2, 0)$.

Step L2. For each box the faces with outward normal $+x$, $+y$, $+z$ face the viewer, because $a \cdot e$ is $1$, $1$ and $2$. The faces $-x$, $-y$, $-z$ face away. Step L4 removes the three edges where two back faces meet: the edges at the corner $(0,0,0)$ of the rod and the edges at the corner $(4,-5,3)$ of the plate. Each box has 12 edges, so 9 edges of each box go on.

Step L9 for the top front edge of the rod, $p(t) = (10t, 0, 1)$, against the plate. The plate has the six inequalities $x \le 6$, $x \ge 4$, $y \le 5$, $y \ge -5$, $z \le 4$, $z \ge 3$. The point $p(t) + \alpha e$ is $(10t + \alpha, \alpha, 1 + 2\alpha)$, so the system is

| face | inequality in $t$ and $\alpha$ |
|---|---|
| $x \le 6$ | $10t + \alpha - 6 \le 0$ |
| $x \ge 4$ | $4 - 10t - \alpha \le 0$ |
| $y \le 5$ | $\alpha - 5 \le 0$ |
| $y \ge -5$ | $-5 - \alpha \le 0$ |
| $z \le 4$ | $2\alpha - 3 \le 0$ |
| $z \ge 3$ | $2 - 2\alpha \le 0$ |

The $z$ rows give $1 \le \alpha \le 3/2$, and the $x$ rows give $4 - \alpha \le 10t \le 6 - \alpha$. The polygon $Q$ is the parallelogram with corners $(t, \alpha) = (3/10, 1), (1/2, 1), (9/20, 3/2), (1/4, 3/2)$. Its projection on the $t$ axis is $(1/4, 1/2)$, so the plate hides the edge from $x = 5/2$ to $x = 5$. The visible parts are $[0, 1/4]$ and $[1/2, 1]$, that is, $x \in [0, 5/2]$ and $x \in [5, 10]$. The top back edge $(10t, 1, 1)$ gives the same interval.

For the lower back edge of the rod, $p(t) = (10t, 1, 0)$, the $z$ rows give $3/2 \le \alpha \le 2$, so the hidden range is $(1/5, 9/20)$. This edge lies between a back face ($-z$) and a front face ($+y$), so it is a [silhouette edge](/silhouette-edge/) of the rod. All 9 remaining edges of the plate are visible, because the rod is behind the plate.

## Correctness

Two facts make the method exact.

First, for a convex body and a point $p$ inside one of its edges, the segment from $p$ toward the viewer enters the interior of the body exactly when both faces of the edge face away from the viewer. This is the test of line L4. If one face faces the viewer, or is seen edge on, the line of sight leaves the body or runs along its surface, and convexity stops it from coming back.

Second, for another body $B_j$, a point $p(t)$ is hidden by $B_j$ exactly when some $\alpha > 0$ satisfies all the strict inequalities, that is, when $(t, \alpha)$ is in the interior of $Q$ for some $\alpha$. The interior of a convex polygon projects to an open interval, the open interval of line L10. A point is visible exactly when no body hides it, so the visible set is $[0, 1]$ minus the union of the intervals of all bodies, which is line L11. The full proof is below.

## Complexity

Let $n$ be the total number of edges and faces and $f$ the largest number of faces of a body. Line L2 costs $O(n)$. For one edge and one body $B_j$ with $f_j$ faces, the clipping of lines L8 and L9 starts with 4 corners and adds at most one corner per half-plane, so it costs $O(f_j^2)$; the sum over the bodies is at most $f \sum_j f_j \le f n$. Line L11 sorts at most $m \le n$ intervals in $O(m \log m)$ time. Over at most $n$ edges, the total is $O(n^2 (f + \log n))$. For bodies with a bounded number of faces this is $O(n^2)$: every edge is tested against every body. The extra space is $O(n)$ for the face signs, one polygon $Q$ and one list $H$ at a time.

## Properties

- **Object space, exact.** The output is a list of exact segments in scene coordinates, at any resolution. With rational input and the arithmetic of the implementation, it is exact.
- **Perspective at no extra cost.** The homogeneous form makes the system linear for an eye point as well as for a parallel view.
- **One interval per body.** A convex body hides one connected part of an edge. An edge loses at most $m - 1$ intervals.
- **No sorting of the bodies.** The bodies can be in any order, and they need not be separable by planes.

## Variants and improvements

- **Bounding box tests.** Compare the screen extents and the depth ranges of the edge and the body first. Most pairs fail this test in a typical scene.
- **Nonconvex objects.** Split each object into convex pieces first (see [convex decomposition](/convex-decomposition/) for the planar case). Edges inside the object, where two pieces touch, must then be removed as well.
- **Interpenetrating bodies.** If two bodies cut through each other, the lines where their surfaces cross are not edges of either body, so the basic method does not draw them. Compute them by intersecting the edges of each body with the faces of the other, and add them as edges.
- **Quantitative invisibility.** For general polyhedral surfaces, [Appel's algorithm](/appel-hidden-line-algorithm/) counts the faces in front of each point and updates the count only where an edge passes behind a [silhouette edge](/silhouette-edge/).

## When to use it

Use it for line drawings of a small number of convex solids, such as engineering parts made of blocks, when exact vector output is needed, for example for a plotter or for a vector file. It is short to write and has no special cases for the order of the bodies. For scenes with many bodies the quadratic number of tests is too slow; use Appel's method or a [z-buffer](/z-buffer/) based line renderer.

## Pitfalls

- **Nonconvex input.** The inequalities describe a convex set. A nonconvex body gives wrong hidden intervals.
- **Inward normals.** The signs of $f_k$ assume outward normals. Orient each plane so that an inner point, such as the center of the vertices, gives $f_k < 0$.
- **Strict versus non-strict.** A line of sight that runs along a face, or touches an edge, must not hide anything. Use the interior of $Q$, and discard $Q$ with zero area.
- **Self-hiding of silhouette edges.** An edge between a front face and a back face is visible with respect to its own body. Only edges with two back faces are dropped in line L4.
- **Floating point.** With floating point coordinates, a polygon $Q$ of tiny area can appear or disappear, which leaves small gaps or slivers. Use a tolerance, or exact arithmetic.
- **Viewer inside a body.** Then no face of that body has $f_k(e) > 0$, and the bound $\alpha_{\max}$ does not exist. The viewer must be outside all bodies.

## Implementations

## History

Roberts did the work of his thesis at MIT Lincoln Laboratory. The thesis takes a photograph of a scene of polyhedra, finds the edges, matches them to models of convex blocks, and then shows the scene from a new viewpoint with the hidden lines removed. It is usually cited as the first solution of the hidden line problem. The homogeneous coordinates that he used for the projection, and the volume matrix of each convex body, made the test linear. Sutherland, Sproull and Schumacker's 1974 survey classed it as an object space algorithm, and textbooks such as Rogers' still teach it with worked volume matrices.

## References
