---
tag: X0W0GT
kind: problem
slug: lattice-points-in-non-lattice-polygon
name: Lattice points inside a non-lattice polygon
aliases:
- lattice points in a rational polygon
- integer points in a polygon with rational vertices
- counting integer points under a polygon
area: geometry/polygons
level: advanced
summary: Problem of counting integer points inside a polygon whose vertices need not be lattice points, solved with a Pick-like formula and gcd computations.
prereqs: [picks-theorem, simple-polygon, euclidean-algorithm]
see_also: [lattice-point-counting, shoelace-formula, scanline-polygon-fill, top-left-fill-rule, extended-euclidean-algorithm, barvinok-algorithm, point-in-polygon, polygon-area]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Chapter 3, Section 3.5 (floor and ceiling sums, the sum of floor((m k + x)/n) over k and its reciprocity law)
  - url: https://cp-algorithms.com/geometry/lattice-points.html
    title: cp-algorithms, Lattice points inside non-lattice polygon
    locator: the whole article (the points under a line y = (k x + b), the Euclid-like reduction, and the sum over the edges of a polygon)
  - url: https://github.com/atcoder/ac-library/blob/master/atcoder/math.hpp
    title: AtCoder Library, math.hpp
    locator: the function floor_sum(n, m, a, b), with its O(log m) loop
  - paper: "Alexander I. Barvinok, A polynomial time algorithm for counting integral points in polyhedra when the dimension is fixed, Mathematics of Operations Research 19(4), 1994, 769 to 779"
    locator: the general fixed dimension result, of which the plane is the case d = 2
---

The problem asks for the number of points with integer coordinates inside a [simple polygon](/simple-polygon/) whose vertices are rational points, not necessarily lattice points. For a lattice polygon, [Pick's theorem](/picks-theorem/) gives the answer from the area and a gcd per edge. For other vertices Pick's formula is false, but a Pick-like computation still works. Split the count into one signed term per edge: the number of lattice points under that edge, above some fixed level. Each term is a *floor sum* $\sum_x \lfloor (a x + b)/c \rfloor$. A Euclid-like recursion evaluates it in $O(\log c)$ arithmetic operations, so the whole count takes $O(n \log M)$ operations, where $M$ bounds the numerators and denominators of the coordinates. The running time does not depend on the area of the polygon.

## In plain words

Draw a polygon on graph paper whose corners do not sit on grid crossings. How many crossings lie inside it? You could test every crossing in a box around the polygon, but the box can be huge.

Instead, look at one edge of the outline at a time. Count the crossings that lie below the edge, down to a fixed floor line. Edges along the top of the shape add their count. Edges along the bottom subtract theirs. What remains is the set of crossings between the bottom and the top, which is the inside.

Counting the crossings under one straight edge has a shortcut. You swap the roles of rows and columns and shrink the numbers, the same way the Euclidean algorithm shrinks a pair of numbers. Points that lie exactly on the outline need a little extra bookkeeping.

## Definition

**Input.** A simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order, with rational coordinates given exactly as pairs of integers. Collinear consecutive vertices are allowed.

**Output.** The number $C$ of lattice points $(x, y) \in \mathbb{Z}^2$ in the closed polygon. Usually one also wants the number $B$ of lattice points on the boundary and the number $I = C - B$ of lattice points in the interior.

**Edge lines.** An edge $v_i v_{i+1}$ that is not vertical lies on a line $y = (A x + B)/D$ with integers $A, B$ and $D > 0$, found by clearing the denominators of the slope and the intercept. For integers $L \le R$, let
$$S(A, B, D; L, R) = \sum_{x = L}^{R - 1} \left\lfloor \frac{A x + B}{D} \right\rfloor .$$

**Why Pick fails.** Pick's formula $I + B/2 - 1$ for the area needs lattice vertices. The triangle $(1/2, 1/2), (9/2, 1), (2, 4)$ has area $53/8$, which is not even a multiple of $1/2$, while $I$ and $B$ are integers.

## Variants

- **Closed, open or half-open counts.** The closed count $C$, the interior count $I$, and a half-open count that takes each boundary point only when the polygon lies just below it. The half-open count is what the signed floor sums give directly. It is additive: if a polygon is cut into pieces, the half-open counts of the pieces add up to that of the whole.
- **Lattice vertices.** If all vertices are integer points, Pick's theorem gives $I = \text{area} - B/2 + 1$ with $B = \sum_i \gcd(|\Delta x_i|, |\Delta y_i|)$, and no floor sums are needed.
- **Polygons with holes.** Run the same sum over every boundary cycle, the outer one counterclockwise and the holes clockwise. The signed sums add up, and the boundary corrections are made per cycle.
- **Points under a line.** The core subproblem: count the lattice points $(x, y)$ with $L \le x < R$ and $0 < y \le (A x + B)/D$. This is the floor sum itself, also written $\sum_{i=0}^{n-1} \lfloor (a i + b)/m \rfloor$.
- **Other lattices and pixel grids.** Pixel centers at half-integer coordinates become integer points after the shift $(x, y) \mapsto (x - 1/2, y - 1/2)$. A general lattice $\{u a + w b\}$ becomes $\mathbb{Z}^2$ after an exact linear change of coordinates.
- **Higher dimensions.** Counting integer points in a rational polytope of fixed dimension is [lattice point counting](/lattice-point-counting/), solved in polynomial time by [Barvinok's algorithm](/barvinok-algorithm/).

## Examples

**A triangle with half-integer corners.** Take $T = (1/2, 1/2), (9/2, 1), (2, 4)$, counterclockwise. The columns with integer $x$ that meet $T$ are $x = 1, 2, 3, 4$. The bottom edge from $(1/2, 1/2)$ to $(9/2, 1)$ lies on $y = (x + 7/2)/8$, which is below $1$ on all four columns, so its floor sum is $0 + 0 + 0 + 0 = 0$ and it is subtracted. The top right edge from $(9/2, 1)$ to $(2, 4)$ lies on $y = (32 - 6x)/5$. On the columns $x = 2, 3, 4$ the floors are $4, 2, 1$, which add to $7$. The top left edge from $(2, 4)$ to $(1/2, 1/2)$ lies on $y = (7x - 2)/3$. On the column $x = 1$ the floor is $1$. A column belongs to an edge when $x_{\text{left}} \le x < x_{\text{right}}$, so the column $x = 2$ goes to the right edge only. The half-open count is $7 + 1 - 0 = 8$, one column at a time $1 + 4 + 2 + 1$.

There are no lattice points in the open edges. The only lattice vertex is $(2, 4)$, and $T$ lies below it, so the half-open count already contains it. Hence $C = 8$, $B = 1$ and $I = 7$. The eight points are $(1,1)$, $(2,1)$, $(2,2)$, $(2,3)$, $(2,4)$, $(3,1)$, $(3,2)$ and $(4,1)$. Pick's formula would give $7 + 1/2 - 1 = 13/2$, but the area is $53/8$.

**A rectangle with a collinear vertex.** Take $(0,0), (3/2, 0), (3,0), (3,2), (0,2)$, the box $[0,3] \times [0,2]$ with an extra vertex in the middle of the bottom edge. The two bottom edges have floor sums $0$. The top edge, going left, contributes $2 + 2 + 2 = 6$ over the columns $x = 0, 1, 2$. The half-open count $6$ misses the boundary points that have the outside just below them:

- the bottom points $(1, 0)$ and $(2, 0)$;
- the point $(3, 1)$ on the right edge, which goes up;
- the corners $(0,0)$, $(3,0)$ and $(3,2)$.

That adds $6$, so $C = 12 = 4 \cdot 3$, $B = 10$ and $I = 2$. The extra vertex $(3/2, 0)$ is not a lattice point and changes none of the terms. Since all corners here are lattice points, Pick's theorem applies as a check: $2 + 10/2 - 1 = 6$, the area.

**A huge thin polygon.** The triangle $(0, 0), (10^{9}, 1), (0, 1/3)$ has a bounding box with about $10^{9}$ columns. A scan over the columns takes $10^9$ steps. The floor sums take a few dozen and find $C = 2$: the triangle is so thin that it contains only its two lattice corners $(0,0)$ and $(10^9, 1)$.

## Known algorithms

| method | time | notes |
|---|---|---|
| test every lattice point of the bounding box | $O(W H n)$ | $W \times H$ is the box size; a [point in polygon](/point-in-polygon/) test per point |
| scan the integer columns | $O(W n)$ | per column, sort the edge crossings and count the integers between them; the method of [scanline fill](/scanline-polygon-fill/) |
| signed floor sums per edge | $O(n \log M)$ | exact; independent of the area |
| Pick's theorem | $O(n \log M)$ | lattice vertices only; one gcd per edge |

**Signed floor sums.** For a vertical line $x = k$ with $k$ an integer, the edges that cross it, counting an edge when $x_{\text{left}} \le k < x_{\text{right}}$, alternate between *lower* edges, which go right and have the interior above them, and *upper* edges, which go left and have the interior below them. The lattice points of the polygon on this line, in the half-open sense, are the integers $y$ in $(\ell, u]$ for each lower crossing $\ell$ and the upper crossing $u$ above it. Their number is $\lfloor u \rfloor - \lfloor \ell \rfloor$. Summed over all columns and regrouped by edge, the half-open count is
$$N = \sum_{\text{upper edges}} S(A, B, D; L, R) - \sum_{\text{lower edges}} S(A, B, D; L, R),$$
with $L = \lceil x_{\text{left}} \rceil$ and $R = \lceil x_{\text{right}} \rceil$. Vertical edges contribute nothing. Regrouping by edge is valid because both sides count the same pairs (column, crossing).

**The floor sum in logarithmic time.** Write $f(n, m, a, b) = \sum_{i=0}^{n-1} \lfloor (a i + b)/m \rfloor$, so that $S(A, B, D; L, R) = f(R - L, D, A, A L + B)$. If $a \ge m$ or $b \ge m$, or either is negative, pull out the integer parts: $f(n, m, a, b) = \lfloor a/m \rfloor \binom{n}{2} + \lfloor b/m \rfloor n + f(n, m, a \bmod m, b \bmod m)$. Once $0 \le a, b < m$, the sum counts the lattice points under a segment of slope $a/m < 1$. Counting the same points by rows instead of columns gives a sum of the same form with the roles of $a$ and $m$ swapped. The AtCoder Library writes this as: with $y = a n + b$, $f(n, m, a, b) = f(\lfloor y/m \rfloor, a, m, y \bmod m)$. The pair $(m, a)$ shrinks like the pair in the [Euclidean algorithm](/euclidean-algorithm/), so there are $O(\log m)$ rounds. This exchange of rows and columns is the reciprocity law for floor sums in Concrete Mathematics.

**Boundary corrections.** The half-open count takes a boundary point $p$ exactly when the point $p + (\varepsilon, -\delta)$, a tiny step down and an even tinier step right, lies inside $P$. So
$$C = N + \sum_{\text{edges going right or straight up}} (\text{lattice points inside the edge}) + \#\{\text{lattice vertices whose downward direction leaves } P\}.$$
The lattice points inside an edge come from the [extended Euclidean algorithm](/extended-euclidean-algorithm/). Write the line as $a x + b y = c$ with coprime integers $a, b$. If $\gcd(a, b)$ does not divide $c$, there are none. Otherwise one solution and the step $(b, -a)$ list them all, and a division counts those strictly between the endpoints. At a lattice vertex $v$, the downward test asks whether the direction $(\varepsilon, -1)$ lies in the interior angle between the outgoing edge and the reversed incoming edge. This takes two exact cross products, with a second, tie-breaking cross product when an edge is vertical. Finally, $B$ is the sum of the edge-interior counts plus the number of lattice vertices, and $I = C - B$.

## Bounds

- **Upper bound.** $O(n \log M)$ arithmetic operations, with $M$ a bound on the absolute values of the numerators and denominators. The integers $A, B, D$ of an edge have $O(\log M)$ bits, and the floor sum loop runs $O(\log M)$ rounds on numbers of that size.
- **Lower bound.** $\Omega(n)$, to read the polygon. Every vertex can change the answer.
- **Enumeration.** The answer can be as large as $\Theta(M^2)$, exponential in the input size, so no method that visits the points one by one is polynomial. The column scan is only pseudo-polynomial.

## Reductions

- **To floor sums.** The polygon count reduces to $n$ floor sums plus $O(n)$ boundary corrections, as above.
- **Floor sums to themselves.** The reciprocity step maps $f(n, m, a, b)$ to $f(n', a, m, b')$ with smaller parameters, the same way $\gcd(m, a)$ reduces to $\gcd(a, m \bmod a)$.
- **Pick's theorem as a special case.** With lattice vertices, the floor sums add up to the [shoelace](/shoelace-formula/) area plus a correction that depends only on the gcds of the edge vectors, and the result is Pick's formula.
- **From two-variable linear inequalities.** Counting the integer solutions of a system of linear inequalities in two unknowns is this problem for a convex polygon, after clipping it to a bounded box when it is unbounded.

## Applications

- **Pixel coverage.** The number of pixel centers that a polygon with subpixel vertices covers, under a fixed tie rule such as the [top-left rule](/top-left-fill-rule/), can be found without rasterizing. The half-open count is one such rule: a point counts when the interior lies just below it.
- **Number theory.** Sums like $\sum_{k} \lfloor (p k)/q \rfloor$ appear in the proof of quadratic reciprocity and in Dedekind sums. They are lattice-point counts in triangles.
- **Competitive programming.** Counting integer points in a region bounded by lines with large coefficients, and sums of the form $\sum_i \lfloor (a i + b)/m \rfloor$ for $n$ up to $10^{18}$.
- **Integer programming in the plane.** Counting the feasible integer points of a two-variable problem, for example to sample one uniformly.

## References
