---
tag: FB22MJ
kind: data-structure
slug: line-arrangement
name: Line arrangement
aliases:
- hyperplane-arrangement
- arrangement of lines
area: geometry/intersections
level: core
summary: The subdivision of the plane by n lines into vertices, edges and faces, at most n(n-1)/2, n^2 and (n^2+n+2)/2 of them, stored as a doubly connected edge list.
model: real-ram
complexity:
  vars: {n: the number of lines}
  time: {worst: Θ(n^2 log n)}
  space: {extra: Θ(n^2)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [line-line-intersection, planar-subdivision, doubly-connected-edge-list, euler-formula]
see_also: [line-arrangement-construction, edelsbrunner-o-rourke-seidel-algorithm, general-position, trapezoidal-map, half-plane-intersection, all-segment-intersections, randomized-incremental-construction, angular-sort]
sources:
  - book: isbn:9783540137221
    title: Herbert Edelsbrunner, Algorithms in Combinatorial Geometry, Springer, 1987
    locator: Chapter 1, Fundamental concepts in combinatorial geometry (counting faces of arrangements), and Chapter 7, Constructing arrangements (the incremental algorithm and the zone theorem)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 8, Arrangements and Duality, Section 8.3 (the bounding box, the doubly connected edge list of an arrangement, the face counts and the zone theorem)
  - paper: doi:10.1137/0215024
    title: Herbert Edelsbrunner, Joseph O'Rourke and Raimund Seidel, Constructing arrangements of lines and hyperplanes with applications, SIAM Journal on Computing 15(2), 1986, 341-363
    locator: the construction of an arrangement of n lines in O(n^2) time and space, and of hyperplanes in d dimensions in O(n^d) time
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: the chapter Arrangements, by Dan Halperin and Micha Sharir (combinatorial bounds, zones and construction algorithms)
---

The arrangement of a set $L$ of $n$ lines in the plane is the subdivision of the plane that the lines induce: its vertices are the crossing points, its edges are the pieces of the lines between vertices, and its faces are the connected parts of the plane that remain after the lines are removed. An arrangement has at most $\binom{n}{2}$ vertices, $n^2$ edges and $\binom{n}{2} + n + 1$ faces, with equality when the lines are in general position. It is stored as a [doubly connected edge list](/doubly-connected-edge-list/) clipped to a large box, built here in $O(n^2 \log n)$ time, or in optimal $O(n^2)$ time by the [incremental algorithm](/edelsbrunner-o-rourke-seidel-algorithm/) that uses the zone theorem.

## In plain words

Draw a few straight lines across a sheet of paper, as long as the sheet allows. The lines cut the sheet into pieces. The arrangement is the full picture: the points where lines cross, the pieces of lines between those points, and the pieces of paper.

Each new line adds one piece of paper more than the number of places where it crosses the earlier lines, because each part of the new line cuts one old piece in two. So many lines make many pieces, about half the square of their number. To store the picture, keep for every piece of line its two ends and which pieces of paper are on its two sides, and for every piece of paper the loop of line pieces around it.

## The abstract type

A static structure over a list of distinct lines, built once:

- `build(L)`: compute the arrangement $\mathcal{A}(L)$.
- `counts()`: the numbers of vertices, edges and faces of $\mathcal{A}(L)$.
- `face_boundary(f)`: the vertices of face $f$ in counterclockwise order, clipped to the box.
- `locate(p)`: the face that holds the point $p$, or NIL if $p$ lies on a line.

A full structure also walks from a face to its neighbours across each edge and around each vertex, which the doubly connected edge list gives in $O(1)$ time per step.

## Representation

**Notation.** A line is $\ell_i = \{(x, y) : a_i x + b_i y = c_i\}$ with integers $a_i, b_i, c_i$ and $(a_i, b_i) \ne (0, 0)$, and no two lines are equal. For a vertex $v$, $m_v \ge 2$ is the number of lines through $v$. The arrangement is *simple* if no two lines are parallel and no three lines pass through one point.

**The box.** Faces and edges of an arrangement can be unbounded. Let $M = 1 + \max(\max_i |c_i|, \max |x|, \max |y|)$, where the inner maxima run over the crossing points $(x, y)$, rounded down to an integer. The box $B = [-M, M]^2$ holds every vertex strictly inside, and every line passes through its interior, since the point of $\ell_i$ next to the origin has coordinates of absolute value at most $|c_i|$. Clipping to $B$ cuts each unbounded edge at a point on $\partial B$ and adds the box edges, but it keeps one face in $B$ for every face of $\mathcal{A}(L)$.

**The edge list.** Each edge is two twin half-edges with opposite directions. A half-edge $e$ stores its origin, its twin, the next and the previous half-edge on the boundary of the face to its left, the face itself, and the line it lies on, or $-1$ for a box edge. A vertex stores its point and its outgoing half-edges in counterclockwise order. Face $0$ is the outer face, outside $B$. All points are exact rationals: a crossing of two lines has coordinates that are quotients of $2 \times 2$ determinants of the input.

**Invariant.**

1. $\mathrm{twin}(\mathrm{twin}(e)) = e$, $\mathrm{next}(\mathrm{prev}(e)) = e$, and $\mathrm{next}(e)$ starts where $e$ ends and has the same face as $e$.
2. Every vertex strictly inside $B$ has $2 m_v$ outgoing half-edges, all on lines.
3. Every face other than face $0$ is a strictly convex polygon, with its boundary counterclockwise; face $0$ is bounded by $\partial B$ clockwise.
4. $V - E + F = 2$ for the counts of the clipped structure, with the outer face included.

**Counts.** For any set of $n \ge 1$ distinct lines,

$$ V \le \binom{n}{2}, \qquad E = n + \sum_v m_v, \qquad F = 1 + n + \sum_v (m_v - 1), $$

so $E \le n^2$ and $F \le \binom{n}{2} + n + 1$, with equality exactly for simple arrangements. The face count follows from the insertion argument: a line that meets the earlier lines in $k$ distinct points is cut into $k + 1$ edges, and each of them splits one face in two.

## Operations

```pseudo id=main
BUILD(ℓ_1, …, ℓ_n)                        ▷ ℓ_i : a_i x + b_i y = c_i
L1  reject a line with a_i = b_i = 0, and two equal lines
L2  M ← 1 + max(|c_i|, |x|, |y| for every crossing (x, y) of two lines), B ← [−M, M]²
L3  for each line ℓ_i do sort its crossings and its two hits with ∂B along ℓ_i, and add a segment between each two neighbours
L4  sort the four corners and all hits around ∂B, and add a segment between each two neighbours, cyclically
L5  for each segment pq create the twin half-edges p→q and q→p
L6  at each vertex v sort the half-edges that leave v by angle
L7  for each half-edge e = u→v do next(e) ← the half-edge that leaves v just clockwise of twin(e), prev(next(e)) ← e
L8  follow next to collect the face cycles; the one cycle of negative area is the outer face 0

FACE-BOUNDARY(f)
L9  return the origins of the half-edges on the cycle of f

LOCATE(p)                                 ▷ p strictly inside B
L10 if p lies on a line then return NIL
L11 return the face f ≥ 1 such that p is strictly left of every half-edge of f
```

Line L3 makes the segments of each line meet other segments only at their end points, because every crossing on $\ell_i$ is a split point. Line L7 is the face rule of a doubly connected edge list: when a walk with the face on its left arrives at $v$ along $e$, it leaves along the next half-edge clockwise from the way back. LOCATE is the simple scan over all faces; a fast query needs a separate point location structure such as a [trapezoidal map](/trapezoidal-map/).

## Example

Take the five lines $y = 0$, $x = 0$, $y = x$, $x + y = 2$ and $y = 2$. The lines $y = 0$ and $y = 2$ are parallel, and two points have three lines, so the arrangement is not simple.

| vertex | lines through it | $m_v$ | outgoing half-edges |
| --- | --- | --- | --- |
| $(0, 0)$ | $y = 0$, $x = 0$, $y = x$ | 3 | 6 |
| $(0, 2)$ | $x = 0$, $x + y = 2$, $y = 2$ | 3 | 6 |
| $(2, 0)$ | $y = 0$, $x + y = 2$ | 2 | 4 |
| $(1, 1)$ | $y = x$, $x + y = 2$ | 2 | 4 |
| $(2, 2)$ | $y = x$, $y = 2$ | 2 | 4 |

So $V = 5$, $E = n + \sum_v m_v = 5 + 12 = 17$ and $F = 1 + n + \sum_v (m_v - 1) = 1 + 5 + 7 = 13$. A simple arrangement of five lines would have $10$, $25$ and $16$. Three faces are bounded, the triangles $(0,0), (2,0), (1,1)$, then $(0,2), (0,0), (1,1)$, and $(1,1), (2,2), (0,2)$, and the other ten are unbounded.

BUILD finds $M = 3$, so $B = [-3, 3]^2$. The line $y = x$ hits $\partial B$ at the corners $(-3, -3)$ and $(3, 3)$, and the other four lines hit it at eight more points, so the clipped structure has $5 + 8 + 4 = 17$ vertices, $29$ edges and $14$ faces, and $17 - 29 + 14 = 2$. LOCATE$((1/2, 1/4))$ returns the triangle $(0,0), (2,0), (1,1)$.

## Correctness

After line L3 the segments cover every line inside $B$, and two segments meet only at a common end point: two segments on one line are consecutive pieces, and a segment of $\ell_i$ and a segment of $\ell_j$ can share only the point $\ell_i \cap \ell_j$, which is an end point of both. With the box edges of line L4, the segments form a connected plane graph that covers $L \cap B$ and $\partial B$. Lines L5 to L8 then build its faces by the rotation rule, which is correct for any connected plane graph with straight edges. Each face inside $B$ is a face of $\mathcal{A}(L)$ cut by the convex box, so it is convex and connected, and every face of $\mathcal{A}(L)$ meets the interior of $B$. The full proof, with the count formulas, is in the proof file.

## Complexity

- **Build.** Line L2 computes $\binom{n}{2}$ crossings. Line L3 sorts $n$ lists of at most $n + 1$ points, and line L6 sorts the half-edges at each vertex, $\sum_v 2 m_v \log(2 m_v) = O(n^2 \log n)$ in total. Lines L5, L7 and L8 take $O(n^2)$ time. So the build takes $\Theta(n^2 \log n)$ time in the worst case. The [Edelsbrunner-O'Rourke-Seidel algorithm](/edelsbrunner-o-rourke-seidel-algorithm/) avoids the sorts and takes $\Theta(n^2)$ time.
- **Face boundary.** $O(k)$ time for a face with $k$ edges.
- **Locate.** $O(n^2)$ time by the scan of line L11.
- **Space.** $\Theta(n^2)$ for a simple arrangement, $O(n + V + E)$ in general. Each coordinate is a quotient of two determinants, so with input numbers of absolute value at most $U$ its numerator and denominator are at most $2U^2$.

## Variants

- **Hyperplane arrangements.** $n$ hyperplanes in $\mathbb{R}^d$ give $\Theta(n^d)$ faces of all dimensions in the simple case, built in $O(n^d)$ time by the same incremental method, using the zone theorem in $d$ dimensions.
- **Arrangements of segments and curves.** For $n$ segments, the arrangement has $O(n + k)$ size for $k$ crossings and is built by [Bentley-Ottmann](/bentley-ottmann-algorithm/) or by [randomized incremental construction](/randomized-incremental-construction/). For curves with at most $s$ crossings per pair, the size is $O(s n^2)$.
- **Zones and levels.** The zone of an extra line is the set of faces that it meets; the zone theorem bounds its total size by $O(n)$. The $k$-level is the set of points with exactly $k$ lines strictly above, a central object in the study of $k$-sets.
- **Projective form.** Adding a line at infinity makes every pair of lines meet and every face bounded; the arrangement then lives on the projective plane.
- **Topological sweep.** Edelsbrunner and Guibas (1989) visit all faces of the arrangement in $O(n^2)$ time with only $O(n)$ working space, without storing the whole structure.

## When to use it

Use a line arrangement when a problem about $n$ points becomes, by point-line duality, a problem about all the ways that a line can pass through them: the minimum-area triangle, the ham-sandwich cut, the discrepancy of a point set or the depth of a point. All these are answered by a walk over the $O(n^2)$ faces. If only one face or one level is needed, compute that part alone: one face is a [half-plane intersection](/half-plane-intersection/), in $O(n \log n)$ time.

## Pitfalls

- **Unbounded edges.** A doubly connected edge list needs every edge to have two end points. Without the box of line L2, or a vertex at infinity, the unbounded edges and faces have no consistent boundary cycle.
- **A box that is too small.** If a crossing lies on $\partial B$ or outside, line L3 drops it and two faces merge. The bound of line L2 must be strict, which the $+1$ ensures.
- **Assuming general position.** With three lines through one point, a vertex has $6$ outgoing half-edges, not $4$, and line L6 must sort them all by angle; code that pairs each vertex with exactly two lines breaks. Parallel lines have no crossing, so `meet` must report None and not divide by zero.
- **Floating-point crossings.** Two crossings that are equal in exact arithmetic can round to two distinct points, which creates a tiny face and breaks the counts. Line L3 compares points exactly, with rationals, so equal points are merged.
- **Equal lines.** Two input lines with proportional $(a, b, c)$ are the same line, and line L1 must reject or merge them; otherwise the edges overlap.

## Implementations

## History

Counting the faces of an arrangement of lines goes back to Jakob Steiner (1826), who found $\binom{n}{2} + n + 1$ for lines in general position. Arrangements became a main tool of computational geometry through duality in the early 1980s. Edelsbrunner, O'Rourke and Seidel (1986) built the arrangement of $n$ hyperplanes in $\mathbb{R}^d$ in $O(n^d)$ time by inserting one hyperplane at a time and walking its zone; the zone theorem that they used was later corrected and proved again by Edelsbrunner, Seidel and Sharir (1993). Edelsbrunner's book of 1987 made arrangements a central subject of the field.

## References
