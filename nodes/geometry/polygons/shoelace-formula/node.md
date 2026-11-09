---
tag: 1ARC5T
kind: algorithm
slug: shoelace-formula
name: Shoelace formula
aliases:
- surveyor's formula
- Gauss's area formula
- trapezoid formula
area: geometry/polygons
level: intro
summary: Computes the signed area of a polygon in O(n) as half the sum of the cross products of consecutive vertices.
solves: [polygon-area]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1769
  people: [Albrecht Ludwig Friedrich Meister, Carl Friedrich Gauss]
  note: Braden's survey attributes the formula to Meister (1769) and to Gauss (1795); land surveyors used it long before computers.
prereqs: [polygon, cross-product, oriented-triangle-area, simple-polygon]
see_also: [polygon-area, polygon-orientation, picks-theorem, winding-number-algorithm, two-ears-theorem, polygon-triangulation, orientation-test, integer-overflow]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.3, Area of polygon (the area as a sum of signed triangle areas, and the code)
  - paper: doi:10.1080/07468342.1986.11972974
    title: Bart Braden, The surveyor's area formula, The College Mathematics Journal 17(4), 326 to 337 (1986)
    locator: the whole article (the formula, its proof by Green's theorem, and its history)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 1, the signed area of a triangle as a determinant, used as the orientation primitive
---

The shoelace formula computes the signed area of a [polygon](/polygon/) from its vertex list $v_0, \ldots, v_{n-1}$, with $v_i = (x_i, y_i)$, as half of the sum of the [cross products](/cross-product/) $x_i y_{i+1} - x_{i+1} y_i$ of consecutive vertices. For a [simple polygon](/simple-polygon/) the result is the area when the vertices are in counterclockwise order and minus the area when they are in clockwise order, so the same sum also gives the [orientation](/polygon-orientation/). It takes $\Theta(n)$ time and constant extra space, and on integer coordinates it is exact: twice the area is an integer. It solves the [polygon area](/polygon-area/) problem, and for a self-intersecting polygon it gives the integral of the [winding number](/winding-number-algorithm/).

## In plain words

Write the corners of the polygon in a column, in order around the polygon, and write the first corner again at the bottom. Multiply each x by the y of the next row, and add up these products. Then multiply each y by the x of the next row, and add up those products. The difference of the two totals is twice the area. The crossed multiplication pattern looks like the laces of a shoe, which gives the name.

Each product pair is twice the area of the triangle that the origin makes with one edge. Some triangles count as positive and some as negative, and the parts outside the polygon cancel. If you walk the corners clockwise instead of counterclockwise, every triangle changes sign, so the result is negative.

## The problem

The input is a closed polygon given by its vertex list $v_0, \ldots, v_{n-1}$; the edges are $v_i v_{i+1}$ for $0 \le i < n$, with indices mod $n$. The output is the signed area

$$A(P) = \frac{1}{2} \sum_{i=0}^{n-1} \left(x_i\, y_{i+1} - x_{i+1}\, y_i\right).$$

For a simple polygon, $A(P)$ is $+\operatorname{area}(P)$ in counterclockwise order and $-\operatorname{area}(P)$ in clockwise order. For any closed polygon, simple or not, $A(P) = \iint w(q)\, dq$, where $w(q)$ is the winding number of the boundary around $q$.

Notation: $n$ is the number of vertices. For points $p, q$ write $p \times q = x_p y_q - x_q y_p$; then $\mathrm{orient}(a, b, c) = (b - a) \times (c - a)$, positive for a counterclockwise turn. No general position is needed: repeated or collinear vertices are allowed, and they add no area.

## The algorithm

```pseudo id=main
SHOELACE(P)                                ▷ P = v[0 .. n − 1], v[i] = (x[i], y[i])
L1  if n < 3 then return 0
L2  s ← 0
L3  for i ← 0 to n − 1 do
L4      j ← (i + 1) mod n                   ▷ the edge from v[n − 1] closes the polygon
L5      s ← s + x[i] · y[j] − x[j] · y[i]
L6  return s / 2
```

- **Line L1.** Fewer than three vertices enclose no area. The loop would also return 0 here, since $v \times v = 0$ and $p \times q + q \times p = 0$.
- **Line L5.** The term $v_i \times v_{i+1}$ is twice the signed area of the triangle $(0, v_i, v_{i+1})$ with a corner at the origin. So the sum is a fan of triangles from the origin.
- **Line L6.** On integer input, $s$ is an exact integer, and the only fraction is the final $1/2$. The implementation returns $s$ itself from `twice_signed_area`, and the half as a `Fraction`.

The origin is not special. Replacing $v_i$ by $v_i - c$ for any point $c$ does not change the sum, since the extra terms $-c \times v_{i+1} - v_i \times c$ telescope to zero around the cycle. A common choice is $c = v_0$, which gives the fan $\sum_{i=1}^{n-2} \mathrm{orient}(v_0, v_i, v_{i+1})$ with $n - 2$ terms.

## Example

Take the hexagon $v_0 = (1,0)$, $v_1 = (4,1)$, $v_2 = (5,4)$, $v_3 = (2,5)$, $v_4 = (3,2)$, $v_5 = (0,3)$. It is simple and counterclockwise, and $v_4$ is a reflex vertex: $\mathrm{orient}(v_3, v_4, v_5) = -8$.

| $i$ | $v_i$ | $v_{i+1}$ | $x_i y_{i+1} - x_{i+1} y_i$ | running sum $s$ |
|---|---|---|---|---|
| 0 | (1, 0) | (4, 1) | $1 - 0 = 1$ | 1 |
| 1 | (4, 1) | (5, 4) | $16 - 5 = 11$ | 12 |
| 2 | (5, 4) | (2, 5) | $25 - 8 = 17$ | 29 |
| 3 | (2, 5) | (3, 2) | $4 - 15 = -11$ | 18 |
| 4 | (3, 2) | (0, 3) | $9 - 0 = 9$ | 27 |
| 5 | (0, 3) | (1, 0) | $0 - 3 = -3$ | 24 |

So $s = 24$ and the area is 12. [Pick's theorem](/picks-theorem/) gives the same value: the polygon has $B = 6$ lattice points on its boundary and $I = 10$ inside, and $I + B/2 - 1 = 12$. In the reverse order every term changes sign, and the formula returns $-12$.

A self-intersecting example: the bowtie $(0,0), (2,2), (2,0), (0,2)$ has $s = 0$. Its two triangles have area 1 each, but one is traced clockwise and one counterclockwise, so they cancel. The area of the region covered is 2; see [polygon area](/polygon-area/) for that variant.

## Correctness

**Theorem.** Let $P$ be a simple polygon with $n \ge 3$ vertices. SHOELACE$(P)$ returns $\operatorname{area}(P)$ when the vertices are in counterclockwise order and $-\operatorname{area}(P)$ when they are in clockwise order. For every closed polygon, simple or not, it returns $\iint w(q)\, dq$, the integral of the winding number.

The proof is in [proofs/correctness.md](proofs/correctness.md). For a simple polygon it goes by induction on $n$. A triangle is the base case: its shoelace sum is $\mathrm{orient}(a, b, c)$, which is twice its signed area. A simple polygon with four or more vertices has a diagonal (the [two ears theorem](/two-ears-theorem/) gives one), and the diagonal splits it into two smaller simple polygons. The diagonal appears in the two sums with opposite directions, and $p \times q + q \times p = 0$, so the two sums add up to the sum for $P$. The general case uses the identity $v_i \times v_{i+1} = (x_i - x_{i+1})(y_i + y_{i+1}) + x_{i+1} y_{i+1} - x_i y_i$: the last two terms telescope, and what remains is a sum of signed trapezoids under the edges, which integrates the winding number along each vertical line.

## Complexity

- **Time.** The loop of lines L3 to L5 runs $n$ times and does two multiplications, one subtraction and one addition each time. So the time is $\Theta(n)$ on the [real RAM](/real-ram/), in the best and the worst case.
- **Lower bound.** Every correct algorithm reads all $2n$ coordinates in the worst case. Take any polygon where $y_{i-1} \ne y_{i+1}$; moving $x_i$ by $\delta$ changes the area by $\delta (y_{i+1} - y_{i-1})/2 \ne 0$. An algorithm that never reads $x_i$ cannot tell the two inputs apart. So $\Theta(n)$ is optimal.
- **Space.** One accumulator, so $\Theta(1)$ extra space. The algorithm reads the vertices once, in order, so it also works on a stream of vertices if it keeps the first vertex for the closing edge.
- **Size of the numbers.** If all coordinates are integers with $|x|, |y| \le M$, each term has absolute value at most $2M^2$, and $|s| \le 2nM^2$. With the shift $c = v_0$, each term is at most $8M^2$ but is often far smaller, since it depends only on the size of the polygon, not on its distance from the origin.

## Properties

- **Exact.** On integer input $s$ is an integer, and on rational input it is a rational number. No rounding happens.
- **Signed.** The sign of $s$ is the [orientation](/polygon-orientation/) of a simple polygon; $s = 0$ only for a degenerate polygon of zero area.
- **Invariant under translation and rotation of the start.** Shifting all vertices by a vector, or starting the list at another vertex, does not change $s$. Reversing the list negates $s$.
- **Additive.** Gluing two polygons along a common edge, traversed in opposite directions, adds their sums. This is what makes the triangulation proof work, and it is the reason that the sum of the triangle areas of a [triangulation](/polygon-triangulation/) equals the polygon area.

## Variants and improvements

- **Trapezoid form.** $2A = \sum_i (x_i - x_{i+1})(y_i + y_{i+1})$. Each term is twice the signed area of the trapezoid between an edge and the $x$-axis. This is the form surveyors used, and the base of the general proof.
- **Shifted fan.** $2A = \sum_{i=1}^{n-2} \mathrm{orient}(v_0, v_i, v_{i+1})$, with the differences taken relative to $v_0$. It needs fewer large intermediate values, which matters for floats and for fixed-width integers.
- **Polygons with holes.** Sum the formula over the outer boundary in counterclockwise order and over each hole in clockwise order. See [polygon with holes](/polygon-with-holes/).

## When to use it

Use the shoelace formula whenever you need the area or the orientation of a polygon given by its vertices. Nothing is faster, since every vertex must be read. Use integers or `fractions.Fraction` when the sign matters, for example to decide the orientation before [ear clipping](/ear-clipping/) or [Sutherland-Hodgman clipping](/sutherland-hodgman/). For the area of the region covered by a self-intersecting polygon, or of a union, the formula alone is not enough: first [clip](/polygon-clipping/) or [union](/polygon-union/) the polygons into simple pieces.

## Pitfalls

- **Forgetting the closing edge.** A loop `for i in range(n - 1)` drops the term of the edge $v_{n-1} v_0$. Line L4 takes $j = (i+1) \bmod n$.
- **Repeating the first vertex.** Some file formats repeat $v_0$ at the end. The extra edge $v_0 v_0$ adds $v_0 \times v_0 = 0$, so the area is still right, but a code that also counts vertices or edges gets $n + 1$.
- **Absolute value too early.** Taking $|v_i \times v_{i+1}|$ in line L5 sums the areas of all fan triangles, which is wrong for any polygon that does not contain the origin. Take the absolute value of $s$ once, at the end, and only for a simple polygon.
- **Self-intersecting input.** The bowtie of the example gives 0. The formula integrates the winding number, so a region covered with winding number $-1$ subtracts. Check that the polygon is simple with a [simplicity test](/polygon-simplicity-test/) when that matters.
- **Cancellation in floating point.** Take the unit square with lower left corner $(10^8, 10^8)$. In IEEE double precision the products $x_i y_{i+1}$ are near $10^{16}$, larger than $2^{53}$, and the naive sum returns 0, not 1. The shifted fan returns 1, and exact integers or fractions return 1 for any shift. See [floating-point arithmetic](/floating-point-arithmetic/).
- **Fixed-width overflow.** With 32-bit integer coordinates, each product needs 64 bits and the sum can need more. Use 128-bit integers or the shifted fan, or Python integers. See [integer overflow](/integer-overflow/).

## Implementations

The Python version computes twice the signed area as an exact `int` or `Fraction`, the signed area as a `Fraction`, and the shifted fan. The tests check the worked example, polygons with fewer than three vertices, collinear vertices, the bowtie and a doubly traced square, invariance under translation (also by $10^{15}$), start shift and reversal, the triangle fan on random convex polygons, and the area on 500 random simple lattice polygons against Pick's theorem with brute-force lattice point counts.

## History

Braden's survey attributes the formula to A. L. F. Meister, who gave it in 1769, and to C. F. Gauss, who used it in 1795. It is also called the surveyor's formula, because it computes the area of a field from the coordinates of its corners. In computational geometry it is the standard area routine, and its triangle form is the [orientation test](/orientation-test/).

## References
