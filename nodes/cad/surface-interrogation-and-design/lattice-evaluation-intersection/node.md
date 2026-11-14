---
tag: WD4243
kind: algorithm
slug: lattice-evaluation-intersection
name: Lattice evaluation for surface intersection
aliases:
- lattice method for surface intersection
area: cad/surface-interrogation-and-design
level: advanced
summary: Intersects a grid of iso-parametric curves of one surface with the other surface and links the points found into curves, simple but able to miss small loops.
solves: [surface-surface-intersection]
model: real-ram
complexity:
  vars: {N: the number of lattice intervals per parameter, D: the degree of f on one lattice line, T: the number of terms of f, k: the degree of f, b: the number of bisection steps per root}
  time: {worst: O(N (T k D^2 + b D^3) + N^2 D)}
  space: {extra: O(N D)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1987
  people: [Jarek Rossignac, Aristides Requicha]
  note: Surveys of surface intersection cite their work and that of Lien and others, both of 1987, for lattice evaluation, the reduction of a surface intersection to many curve surface intersections along parameter lines.
prereqs: [curve-surface-intersection, bezier-patch]
see_also: [marching-surface-intersection, subdivision-surface-intersection, algebraic-surface-intersection, marching-squares, sederberg-meyers-loop-detection, tangential-surface-intersection, implicit-surface, jordan-curve-theorem]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 5, Section 5.8.2.1, Lattice evaluation (intersections of isoparametric curves of one surface with the other surface, connected into branches; the risk of missing loops and the dependence on the lattice size)
  - paper: doi:10.1109/38.180122
    title: Nicholas M. Patrikalakis, Surface-to-surface intersections, IEEE Computer Graphics and Applications 13(1), 89 to 95, 1993
    locator: the whole paper (the classification of intersection methods into analytic, lattice evaluation, subdivision and marching methods)
---

Lattice evaluation computes the intersection curve of two surfaces by cutting one of them along a lattice of parameter lines, $u = i/N$ and $v = j/N$, and intersecting each line, a curve, with the other surface. Each such step is a [curve surface intersection](/curve-surface-intersection/), which is far easier than the surface problem. The points found are then linked, cell by cell of the lattice, into polylines that follow the branches of the intersection. The method is simple and finds every branch that crosses a lattice line, but a closed loop that fits inside one cell is lost, and the result is only as good as the lattice is fine.

## In plain words

Two curved sheets cross, and you want the line where they meet. That is hard to compute directly, so draw a grid of lines on the first sheet, like the lines on graph paper. Each grid line is a simple curve, and finding where one curve pierces the other sheet is an easy problem. Do it for every grid line, and you get many dots that lie on the crossing line.

Now connect the dots. Each square of the grid usually has two dots on its sides, and the crossing line enters the square at one dot and leaves at the other, so draw a segment between them. If a square has four dots, look at its middle point to decide which dots go together.

A small loop inside one square crosses no grid line, so it is missed. A finer grid finds smaller loops but costs more.

## The problem

The input is a tensor product [Bézier patch](/bezier-patch/) $r(u, v)$ on $\Omega = [0, 1]^2$, a second surface, and a lattice size $N$. In this page and its code the second surface is an [implicit surface](/implicit-surface/) $f(x, y, z) = 0$ for a polynomial $f$. Then on each lattice line the function $g = f \circ r$ is one polynomial in one unknown, and the curve surface step is exact root finding. When the second surface is a parametric patch, the step is a curve and patch intersection, three equations in three unknowns, and the rest of the method does not change.

The output is a set of polylines in the parameter plane of $r$, each with its vertices on the intersection curve $Z = \{(u, v) : g(u, v) = 0\}$, and a list of the cells that the method could not resolve. Mapping the vertices by $r$ gives points in space.

## The algorithm

```pseudo id=main
LATTICE-INTERSECT(r, f, N)
L1  for i ← 0 to N: add the roots t of f(r(i/N, t)) in [0, 1] as points (i/N, t)
L2  for j ← 0 to N: add the roots t of f(r(t, j/N)) in [0, 1] as points (t, j/N)
L3  for each cell C of the N × N lattice
L4      p0, …, p(k−1) ← the points on the boundary of C, in counterclockwise order
L5      if k = 2 then link p0 and p1
L6      else if k = 4 then if g(center of C) has the sign of g between p0 and p1 then link p1 p2 and p3 p0 else link p0 p1 and p2 p3
L7      else if k > 0 then mark C unresolved
L8  chain the links into polylines, open ones from their ends first
L9  return the polylines and the unresolved cells
```

Lines L1 and L2 are the lattice evaluation proper. The code forms the restriction of the patch to a line as a Bézier curve, converts it to the power basis, substitutes it into $f$, and finds the real roots of the result in $[0, 1]$ by splitting the interval at the roots of the derivative and bisecting. A root within $10^{-9}$ of a lattice value is moved onto it, so that a point at a lattice node is stored once. Lines L3 to L7 do for the zero set of $g$ what [marching squares](/marching-squares/) does for a sampled function, with the difference that the crossing points on the cell edges are exact roots and not linear interpolations. Line L6 resolves the four point case with the value at the center of the cell, the same rule as in marching squares.

## Example

Take the bicubic bump with control points $P_{ij} = (i, j, z_{ij})$, where $z_{ij} = 3$ at the four inner points and $0$ elsewhere, so $r(u, v) = (3u, 3v, 27 u (1 - u) v (1 - v))$. Intersect it with the plane $z = 1$, $f = z - 1$, with $N = 4$. On the line $u = \tfrac12$, $g = \tfrac{27}{4} v (1 - v) - 1$, with roots $v = \tfrac12 \pm \sqrt{\tfrac14 - \tfrac{4}{27}}$. On $u = \tfrac14$ and $u = \tfrac34$, $g = \tfrac{81}{16} v (1 - v) - 1$. On $u = 0$ and $u = 1$, $g = -1$, with no root. The lines in $v$ give the same values by symmetry.

| line | points |
|---|---|
| $u = \tfrac14$ and $u = \tfrac34$ | $v = 0.270939$, $0.729061$ |
| $u = \tfrac12$ | $v = 0.180858$, $0.819142$ |
| $v = \tfrac14$ and $v = \tfrac34$ | $u = 0.270939$, $0.729061$ |
| $v = \tfrac12$ | $u = 0.180858$, $0.819142$ |

That is $12$ points. The $12$ cells of the lattice around the center each have $2$ points on their boundary, the $4$ center cells and the $4$ corner cells have none, and line L8 chains the $12$ links into one closed polygon,

$$(0.25, 0.270939), (0.180858, 0.5), (0.25, 0.729061), (0.270939, 0.75), (0.5, 0.819142), \dots, (0.270939, 0.25),$$

and back to the start. The true curve is the closed curve $27 u (1 - u) v (1 - v) = 1$. The vertices are on it to $10^{-12}$, but the edges are chords: at their midpoints the surface height differs from $1$ by up to $0.081$.

With the plane $z = 1.68$ the true curve is a small loop around the top, with extent $u \in [\tfrac12 - \tfrac1{30}, \tfrac12 + \tfrac1{30}]$ on the line $v = \tfrac12$. For $N = 3$ the lattice values $\tfrac13$ and $\tfrac23$ miss that interval, and the method returns nothing. For $N = 4$ the line $u = \tfrac12$ meets the loop, and the method returns a closed polygon with $4$ vertices.

## Correctness

The [full proof](proofs/correctness.md) shows five facts. Lines L1 and L2 find exactly the points of the intersection curve on the lattice lines, provided no lattice line lies in the second surface. In a clean cell, one with no point at a corner and only simple roots on its edges, the number of boundary points is even, because the sign of $g$ changes at each one on the way around the cell. When $0$ is a regular value of $g$ in the cell and no closed loop lies inside it, the arcs of the curve pair up the boundary points without crossing, by the [Jordan curve theorem](/jordan-curve-theorem/), so with two points line L5 is right, and with four points there are only two possible pairings. Line L6 picks the right one when the center lies in the middle region of the cell, the one that touches two opposite pieces of the boundary.

The fact that decides what is found is simple. The projection of a connected piece of the curve on the $u$ axis is an interval, so the piece meets a lattice line exactly when that interval, or its $v$ counterpart, contains a lattice value. Every piece whose extent in $u$ or in $v$ is at least $1/N$ is found, and a piece inside one cell is lost. The small loop of the example is exactly this case.

What is not proved: that the center condition of line L6 holds, which the method cannot check, and any bound on the distance between a polyline edge and the curve. The tests compare the points on each lattice line with the sign changes of $g$ on $3000$ samples along the line, for random bicubic patches and random planes and spheres, and check that every link stays in one cell.

## Complexity

Let $f$ have degree $k$ and $T$ terms, and let $D \le k \max(m, n)$ be the degree of $g$ on a lattice line of a patch of bidegree $(m, n)$. Forming $g$ on one line takes $O(T k D^2)$ operations with schoolbook products. The root finder recurses through the derivatives, $D$ levels, and at each level makes $O(D)$ bisections of $b$ steps, each step an evaluation of cost $O(D)$, so $O(b D^3)$ per line. There are $2 (N + 1)$ lines. Each line holds at most $D$ points, and the linking scans the points of four lines per cell, $O(D)$ per cell, $O(N^2 D)$ in all. The total is $O(N (T k D^2 + b D^3) + N^2 D)$ time, with $b$ about $45$ for double precision, and $O(N D)$ space for the points.

For a bicubic patch and a quadric, $D = 6$, so each line costs a few thousand operations, and a $100 \times 100$ lattice is fast. The price is in $N$: the error of the polylines falls like $1/N^2$ for a smooth curve that crosses the lattice lines at angles bounded away from zero, as for any chord approximation, but the number of curve surface problems grows like $N$ and the number of cells like $N^2$.

## Properties

- **Exact points.** Every vertex is an intersection point, found to the precision of the root finder. Only the edges between them are approximate.
- **Independent subproblems.** The lines are separate problems, so they run in parallel and need no start point.
- **Not certified.** Loops smaller than a cell, tangential pieces and pieces close together can be lost or linked wrongly, and the method gives no signal except the unresolved cells.
- **Two sided choice.** The lattice can be put on either surface. When both are parametric, cutting both surfaces finds more loops for the same cost.

## Variants and improvements

- **Parametric second surface.** Intersect each lattice line with the second patch by subdivision, Newton or the [interval projected polyhedron](/interval-projected-polyhedron/) method. This is the form surveyed by Patrikalakis and Maekawa, where each line gives an independent system of nonlinear equations.
- **Start points for marching.** Most systems use a coarse lattice only to find one point on each branch, then trace the branch with [marching](/marching-surface-intersection/), which gives a curve with an error tolerance in place of a polyline with chords.
- **Loop detection first.** A criterion such as [Sederberg and Meyers](/sederberg-meyers-loop-detection/) proves that no closed loop exists on a piece. Subdividing until each piece has that guarantee and its boundary is cut by the lattice turns the method into a [subdivision method](/subdivision-surface-intersection/) that finds every loop.
- **Adaptive lattices.** Refine the lattice in cells with four or more points, unresolved cells, or cells where the sign of $g$ at the center does not match the links.
- **Exact substitution.** With an implicit second surface, the whole function $g(u, v)$ is one polynomial, and [algebraic surface intersection](/algebraic-surface-intersection/) uses it in place of the lattice.

## When to use it

Use it for a fast preview of an intersection, to find start points for marching, and when the second surface is implicit and of low degree, where each lattice line is a cheap univariate problem. Do not use it alone where a lost loop matters, as in Boolean operations on solids, unless a loop detection test or a size argument proves that every loop is larger than a cell.

## Pitfalls

- **Lost loops.** A closed piece of the curve inside one cell gives no lattice points. The plane $z = 1.68$ on the bump is lost with $N = 3$ and found with $N = 4$.
- **The ambiguous cell.** With four points, the value at the center decides the pairing. On the saddle $z = 9 (u - \tfrac12)(v - \tfrac12)$ cut by $z = \pm 0.1$ with $N = 1$ the rule is right, because the center lies in the middle region, but a cell where it lies in an outer region gets the wrong pairs.
- **Curves on a lattice line.** If the intersection runs along a lattice line, $g$ is the zero polynomial there, and the root finder returns no points for that line. On the saddle with $z = 0$ and $N = 2$ both branches lie on lattice lines, and the result is wrong. Shift the lattice by a small irrational amount to avoid this.
- **Lattice nodes and touching points.** A point at a corner of a cell, or a root of even multiplicity on an edge, gives an odd count, and line L7 leaves the cell unresolved. Near a tangential intersection many such cells appear.
- **Parameter versus space.** The lattice is uniform in the parameters, not in space. A patch with a strongly uneven parametrization gets cells that are large in space, and loops of moderate size in space can fit inside them.

## Implementations

## History

Lattice evaluation was one of the first general methods for intersecting sculptured surfaces, from the solid modeling work of the 1980s, and surveys cite work of 1987 by Rossignac and Requicha and by Lien and others for it. Patrikalakis (1993) named it as one of four classes of surface intersection methods, with analytic, subdivision and marching methods, and Patrikalakis and Maekawa (2002) treated it in their book, noting that its result depends on the lattice and that it can miss loops. In current systems it survives mostly as the start point search of marching methods.

## References
