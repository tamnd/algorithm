---
tag: SQSS70
kind: algorithm
slug: edelsbrunner-o-rourke-seidel-algorithm
name: Edelsbrunner-O'Rourke-Seidel algorithm
aliases:
- eos-algorithm
- incremental-arrangement-construction
- incremental construction of a line arrangement
area: geometry/intersections
level: advanced
summary: Build the arrangement of n lines by inserting one line at a time and walking only the faces it crosses; the zone theorem bounds each walk by O(n), so the total is optimal Θ(n^2).
solves: [line-arrangement-construction]
model: real-ram
complexity:
  vars: {n: the number of lines}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n^2)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1986
  people: [Herbert Edelsbrunner, Joseph O'Rourke, Raimund Seidel]
  note: The incremental construction of arrangements of lines and hyperplanes with the zone theorem appeared at FOCS 1983 and in SIAM Journal on Computing in 1986; Edelsbrunner, Seidel and Sharir proved the zone theorem again in 1993 after a gap was found in the original proof for higher dimensions.
prereqs: [line-arrangement-construction, line-arrangement, doubly-connected-edge-list, line-line-intersection]
see_also: [randomized-incremental-construction, bentley-ottmann-algorithm, half-plane-intersection, trapezoidal-map, general-position, planar-subdivision, euler-formula, angular-sort]
sources:
  - paper: doi:10.1137/0215024
    title: Herbert Edelsbrunner, Joseph O'Rourke and Raimund Seidel, Constructing arrangements of lines and hyperplanes with applications, SIAM Journal on Computing 15(2), 1986, 341-363
    locator: the incremental algorithm, the zone theorem, O(n^2) time for lines and O(n^d) for hyperplanes in d dimensions, and the applications by duality
  - paper: doi:10.1137/0222031
    title: Herbert Edelsbrunner, Raimund Seidel and Micha Sharir, On the zone theorem for hyperplane arrangements, SIAM Journal on Computing 22(2), 1993, 418-429
    locator: the corrected proof of the zone theorem, O(n^(d-1)) for a hyperplane in an arrangement of n hyperplanes in d dimensions
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 8, Section 8.3, Arrangements of lines (the algorithm ConstructArrangement, the bounding box, the zone theorem with its bound of 6m edges, and the O(n^2) analysis)
  - book: isbn:9783540137221
    title: Herbert Edelsbrunner, Algorithms in Combinatorial Geometry, Springer, 1987
    locator: Chapter 7, Constructing arrangements (the incremental algorithm and the zone theorem)
  - paper: doi:10.1016/0022-0000(89)90038-x
    title: Herbert Edelsbrunner and Leonidas J. Guibas, Topologically sweeping an arrangement, Journal of Computer and System Sciences 38(1), 1989, 165-194
    locator: the topological sweep, which visits all faces in O(n^2) time with O(n) working space
---

The Edelsbrunner-O'Rourke-Seidel algorithm builds the [arrangement](/line-arrangement/) of $n$ lines in $\Theta(n^2)$ time and space, which is optimal because the arrangement can have $\Theta(n^2)$ faces. It is incremental, not a sweep: it inserts the lines one at a time into a [doubly connected edge list](/doubly-connected-edge-list/), and for each new line it walks only through the faces that the line crosses, splitting each of them in two. These faces form the zone of the line, and the zone theorem says that the zone of a line in an arrangement of $m$ lines has $O(m)$ edges, so each insertion costs $O(n)$ time and no sorting is needed.

## In plain words

Draw the lines one by one on a sheet of paper that is already cut into pieces by the earlier lines. A new line starts at the edge of the sheet and runs across it. Each time it crosses a piece, it cuts that piece in two.

To find where the line leaves a piece, walk around the border of that piece until you reach the point where the line crosses it. Then go to the piece on the other side and do the same. You never look at the pieces that the line misses. A theorem says that the borders of all the pieces that one line crosses have only a few edges in total, about as many as the number of lines. So each line costs time in proportion to the number of lines, and all of them together cost about the square of that number.

## The problem

**Input.** A list of $n$ distinct lines $\ell_i : a_i x + b_i y = c_i$ with integers and $(a_i, b_i) \ne (0, 0)$. Lines can be parallel, and many lines can pass through one point.

**Output.** The [line arrangement](/line-arrangement/) $\mathcal{A}(L)$ as a doubly connected edge list, clipped to a box $B = [-M, M]^2$ that holds every vertex strictly inside, as described on that page.

**Notation.** Line $\ell : a x + b y = c$ is directed by $d = (b, -a)$, so a point is left of $\ell$ when $a x + b y - c > 0$ and right of it when the value is negative. A half-edge has its face on its left. The zone of $\ell$ in $\mathcal{A}(L)$ is the set of faces whose closure meets $\ell$; its complexity is the total number of edges of these faces. $m$ is the number of lines inserted so far.

**Model.** The [real RAM](/real-ram/). With integer input every test is the sign of a polynomial of degree at most $3$ in the input, and every point is a pair of rationals, so the implementation is exact with `Fraction`.

## The algorithm

```pseudo id=main
EOS(ℓ_1, …, ℓ_n)
L1  M ← 1 + max(|c_i|, |x|, |y| for every crossing (x, y)), and A ← the edge list of the box B = [−M, M]² alone
L2  for i ← 1 to n do INSERT(A, ℓ_i)
L3  return A

INSERT(A, ℓ)                              ▷ ℓ directed by d
L4  p ← the point where ℓ enters B; walk along ∂B to the edge or the vertex at p
L5  u ← the vertex at p, after splitting the box edge at p if p is inside it
L6  repeat
L7      h ← the half-edge out of u such that d lies strictly between h and the next half-edge out of u counterclockwise
L8      g ← h; while the head of g is strictly right of ℓ do g ← next(g)
L9      if the head of g is on ℓ then w ← head(g) else split the edge of g at its crossing with ℓ, and let w be the new vertex
L10     add the twin half-edges u→w and w→u, which split face(h) into the part right of ℓ and a new face left of ℓ
L11     u ← w
L12 until u lies on ∂B
```

Line L1 computes $\binom{n}{2}$ crossings for the box, as on the [arrangement](/line-arrangement/) page. Line L7 picks the face that $\ell$ enters at $u$: the wedge between two neighbouring half-edges at $u$ that contains the direction $d$. Since $\ell$ is different from every line through $u$, $d$ never points along an edge. Line L8 walks counterclockwise around that face, starting with the half-edge $h$ whose head is right of $\ell$, until it reaches the first head that is on $\ell$ or left of it; that is where $\ell$ leaves the face. Line L10 sets four next pointers and gives the new face to the half-edges of the left part. The loop of lines L6 to L12 ends when $\ell$ reaches $\partial B$ again.

## Example

Insert the five lines $y = 0$, $x = 0$, $y = x$, $x + y = 2$ and $y = 2$ in this order. Line L1 gives $M = 3$. The table lists, for each insertion, where the line enters $B$, the vertices $w$ of line L9 on its way, and the number of faces of the arrangement after the insertion. "New" marks a vertex made by a split in line L5 or L9.

| step | line | $d$ | enters at | vertices on its way | leaves at | faces |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | $y = 0$ | $(1, 0)$ | $(-3, 0)$, new | none | $(3, 0)$, new | $1 \to 2$ |
| 2 | $x = 0$ | $(0, -1)$ | $(0, 3)$, new | $(0, 0)$, new | $(0, -3)$, new | $2 \to 4$ |
| 3 | $y = x$ | $(1, 1)$ | corner $(-3, -3)$ | $(0, 0)$, old | corner $(3, 3)$ | $4 \to 6$ |
| 4 | $x + y = 2$ | $(1, -1)$ | $(-1, 3)$, new | $(0, 2)$, $(1, 1)$, $(2, 0)$, all new | $(3, -1)$, new | $6 \to 10$ |
| 5 | $y = 2$ | $(1, 0)$ | $(-3, 2)$, new | $(0, 2)$, old; $(2, 2)$, new | $(3, 2)$, new | $10 \to 13$ |

In step 3 the line $y = x$ passes through the old vertex $(0, 0)$, which has degree $4$; line L7 finds the wedge between the edge toward $(3, 0)$ and the edge toward $(0, 3)$, so the line goes into the quadrant $x, y > 0$. In step 5, the line $y = 2$ reaches $(0, 2)$, where $x = 0$ and $x + y = 2$ already cross, and the vertex gets degree $6$. Each insertion adds one face more than the number of distinct points where the line meets earlier lines. The final structure has $17$ vertices, $29$ edges and $14$ faces with the box, and $5$ vertices, $17$ edges and $13$ faces in the arrangement itself, the same as the static build.

## Correctness

The invariant is that before each insertion, $A$ is the edge list of the arrangement of the lines inserted so far, clipped to $B$, with every face inside $B$ strictly convex. Consider the insertion of $\ell$. At a vertex $u$ on $\ell$, the face $\phi$ chosen in line L7 is the face that $\ell$ enters just after $u$. Since $\phi$ is convex and $\ell$ enters its interior at $u$, the boundary of $\phi$, read counterclockwise from $u$, first has points strictly right of $\ell$ and then points strictly left of it, and switches only once, at the point $w$ where $\ell$ leaves $\phi$. So the walk of line L8 stops at the edge or the vertex that holds $w$, and the segment $uw$ is $\ell \cap \phi$. Splitting $\phi$ along $uw$ in line L10 keeps both parts convex and keeps the face cycles right. When $w$ is on $\partial B$, the whole of $\ell \cap B$ has been added, and the invariant holds for one more line. The full proof is in the proof file.

## Complexity

- **Box.** Line L1 takes $\Theta(n^2)$ time.
- **One insertion.** The walk of line L4 along $\partial B$ takes $O(m)$ time, since $\partial B$ has at most $2m + 4$ edges. Every other step of lines L7 to L10 visits an edge of a face in the zone of $\ell$: line L7 visits the edges around a vertex of such a face, line L8 visits the boundary of the face that it splits, and line L10 renames the faces of the left part. By the zone theorem, the zone of a line in an arrangement of $m$ lines has $O(m)$ edges; the proof in de Berg et al. gives at most $6m$, and the box adds $O(m)$ more. Each edge of the zone is visited $O(1)$ times per insertion. So the insertion takes $O(m)$ time.
- **Total.** $\sum_{m = 0}^{n-1} O(m + 1) = O(n^2)$ time, and $\Theta(n^2)$ in the worst case because the output can have that size. Space is $\Theta(n^2)$, all of it for the edge list that is the output.
- **Measured.** The implementation counts its steps; for random lines in general position it uses about $5.4 n^2$ steps for $n$ from $10$ to $80$.

## Properties

- **No sorting.** The algorithm never sorts the crossings along a line or the edges around a vertex, which is why it beats the $O(n^2 \log n)$ build by sorting.
- **Degeneracy.** Concurrent lines and parallel lines need no special case: a walk that meets an old vertex continues from it through line L7, and parallel lines simply never meet.
- **Exact.** Every decision is the sign of an orientation test or of $a x + b y - c$ at a rational point.
- **Order.** The result does not depend on the order of insertion, and the $O(n^2)$ bound holds for every order.

## Variants and improvements

- **Hyperplanes.** In $\mathbb{R}^d$ the same scheme inserts each hyperplane by walking its zone, whose complexity is $O(m^{d-1})$, so the arrangement of $n$ hyperplanes is built in $O(n^d)$ time. The proof of the zone bound for $d \ge 3$ in the 1986 paper had a gap, which Edelsbrunner, Seidel and Sharir closed in 1993.
- **Topological sweep.** Edelsbrunner and Guibas (1989) visit the faces of the arrangement in $O(n^2)$ time and $O(n)$ space, by sweeping a curve instead of a straight line. Use it when only a pass over the faces is needed and $\Theta(n^2)$ memory is too much.
- **Line sweep.** The [Bentley-Ottmann sweep](/bentley-ottmann-algorithm/) on the $n$ lines also builds the arrangement, in $O(n^2 \log n)$ time.
- **Randomized incremental construction.** For segments or curves, [randomized incremental construction](/randomized-incremental-construction/) with a [trapezoidal map](/trapezoidal-map/) builds the arrangement in expected $O(n \log n + k)$ time.
- **One face or one zone.** The zone of a single new line, or a single face, is found in $O(n)$ or $O(n \log n)$ time without the whole arrangement.

## When to use it

Use it when you need the whole arrangement of $n$ lines, for example after a point-line duality, and $n$ is small enough for $\Theta(n^2)$ memory, say up to a few thousand lines. For a one-time scan over all faces with little memory, use the topological sweep. For arrangements of segments with few crossings, use a sweep or randomized incremental construction, whose cost depends on the number of crossings.

## Pitfalls

- **Wrong wedge in line L7.** At an old vertex with many lines, the face is the wedge that contains the direction $d$, found by exact angle comparisons. Testing only one neighbour edge, or using floating-point angles, sends the walk into the wrong face, and the walk of line L8 then runs forever or splits the wrong edge.
- **Missing the vertex case in line L9.** The line can leave a face through a vertex. If the code splits the edge there anyway, it creates a second vertex at the same point and an edge of length zero.
- **A box that is too small in line L1.** Every crossing must lie strictly inside $B$; otherwise line L12 stops the walk too early, at a box point that is also a crossing.
- **The direction of $\ell$.** "Right of $\ell$" in line L8 must use the same direction $d$ as line L7. With $d = (b, -a)$ the left side of $\ell$ is $a x + b y > c$; mixing the two conventions makes the walk start on the wrong side.
- **The cost of line L4.** Finding the entry point by a search over all half-edges costs $O(m^2)$ per line and $O(n^3)$ in total; walk only along $\partial B$.

## Implementations

## History

Edelsbrunner, O'Rourke and Seidel presented the algorithm at FOCS 1983 and published it in SIAM Journal on Computing in 1986, together with the zone theorem and applications by duality to problems on finite point sets. A gap in their proof of the zone theorem for dimension three and higher was found later, and Edelsbrunner, Seidel and Sharir gave a correct proof in 1993; the planar case was never in doubt. Edelsbrunner and Guibas added the topological sweep in 1989. The algorithm is the standard textbook construction of line arrangements, as in Chapter 8 of de Berg et al.

## References
