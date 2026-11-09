---
tag: ZK9YXN
kind: problem
slug: line-line-intersection
name: Line-line intersection
aliases:
- intersection-of-two-lines
- intersection point of two lines
area: geometry/intersections
level: intro
summary: Compute the common point of two lines in the plane, or report that they are parallel or equal; Cramer's rule on the 2 by 2 system solves it exactly in O(1) operations.
prereqs: [line-representation, cross-product]
see_also: [line-equation-from-segment, segment-intersection-point, half-plane-intersection, line-arrangement, orientation-test, floating-point-arithmetic, circle-line-intersection, polygon-clipping]
sources:
  - url: https://cp-algorithms.com/geometry/lines-intersection.html
    title: cp-algorithms, Intersection Point of Lines
    locator: Cramer's rule for two lines a x + b y + c = 0, and the test for parallel and equal lines by the other two determinants
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 7, Section 7.2, Segment-segment intersection (the parametric form, the common denominator and the parallel case)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 8, Section 8.2, Duality (the intersection of two lines as the dual of the line through two points)
---

Line-line intersection asks for the common points of two lines in the plane. Two distinct lines meet in exactly one point unless they are parallel, and a line meets itself in all its points, so the answer is one point, the empty set, or the whole line. In the general form $A_i x + B_i y + C_i = 0$ the problem is a $2 \times 2$ linear system, and Cramer's rule gives the point as two quotients of determinants with the common denominator $A_1 B_2 - A_2 B_1$, which is zero exactly for parallel or equal lines. With integer coefficients the answer is an exact rational point.

## In plain words

Two straight lines on a sheet of paper either cross at one point, or they run side by side and never meet, or they are the same line. To find the crossing point, you need a point that obeys both line rules at once.

Each rule says "A times x plus B times y plus C is zero". Two such rules with two unknowns have a standard solution: you can write x and y as fractions whose bottom is the same number for both. That number is zero exactly when the two lines point in the same direction. Then there is no single crossing, and one more check tells whether the lines are the same or only parallel.

## Definition

**Input.** Two lines $\ell_1 : A_1 x + B_1 y + C_1 = 0$ and $\ell_2 : A_2 x + B_2 y + C_2 = 0$ with $(A_i, B_i) \ne (0, 0)$, or two lines in point-direction form $p + t d$ and $q + s e$ with $d, e \ne 0$ (see [line representation](/line-representation/)).

**Output.** One of three answers: the single point $\ell_1 \cap \ell_2$; "parallel" if the lines are parallel and distinct; "equal" if they are the same line.

**Notation.** $\operatorname{cross}(u, v) = u_x v_y - u_y v_x$, and for the general form

$$ D = A_1 B_2 - A_2 B_1, \qquad D_x = B_1 C_2 - B_2 C_1, \qquad D_y = C_1 A_2 - C_2 A_1 . $$

**Model.** The [real RAM](/real-ram/). With integer or rational input all three quantities are exact, and the point is $(D_x / D, D_y / D)$ as a pair of rationals.

## Variants

- **Point-direction form.** For $p + t d$ and $q + s e$, the lines meet where $t = \operatorname{cross}(q - p, e) / \operatorname{cross}(d, e)$, and they are parallel when $\operatorname{cross}(d, e) = 0$; they are equal when moreover $\operatorname{cross}(q - p, d) = 0$.
- **Segments and rays.** Restrict the parameters to $[0, 1]$ or $[0, \infty)$; this is [segment intersection](/segment-intersection-point/), which also needs the case of overlapping collinear segments.
- **Homogeneous coordinates.** With lines as triples $(A : B : C)$, the intersection is the cross product $(A_1, B_1, C_1) \times (A_2, B_2, C_2) = (D_x, D_y, D)$ in $\mathbb{R}^3$, and parallel lines meet at the point at infinity $(D_x : D_y : 0)$.
- **Three dimensions.** Two lines in space usually do not meet; they are skew, and the useful answer is the pair of closest points, found from a $2 \times 2$ system for the two parameters.
- **Many lines.** All $\binom{n}{2}$ intersections of $n$ lines with their order along each line form the [line arrangement](/line-arrangement/).
- **Line and circle.** The [circle-line intersection](/circle-line-intersection/) is the next case, with up to two points.

## Examples

**A rational point.** For $\ell_1 : 4x - 3y + 2 = 0$ and $\ell_2 : x + 2y - 4 = 0$,

$$ D = 4 \cdot 2 - 1 \cdot (-3) = 11, \quad D_x = (-3)(-4) - 2 \cdot 2 = 8, \quad D_y = 2 \cdot 1 - (-4) \cdot 4 = 18, $$

so the point is $(8/11, 18/11)$. Check: $32/11 - 54/11 + 22/11 = 0$ and $8/11 + 36/11 - 44/11 = 0$.

**Parallel and equal lines.** $2x + 4y - 6 = 0$ and $x + 2y + 1 = 0$ give $D = 0$ and $D_x = 4 \cdot 1 - 2 \cdot (-6) = 16 \ne 0$, so they are parallel and distinct. $2x + 4y - 6 = 0$ and $x + 2y - 3 = 0$ give $D = D_x = D_y = 0$, so they are equal.

**Point-direction form.** $(0, 0) + t (2, 1)$ and $(3, 0) + s (-1, 1)$: $\operatorname{cross}(d, e) = 2 \cdot 1 - 1 \cdot (-1) = 3$ and $\operatorname{cross}(q - p, e) = 3 \cdot 1 - 0 \cdot (-1) = 3$, so $t = 1$ and the point is $(2, 1)$.

## Known algorithms

**Cramer's rule.** Compute $D$. If $D \ne 0$, return $(D_x / D, D_y / D)$. If $D = 0$, the normals are parallel; the lines are equal if $D_x = D_y = 0$, that is, if the triples are proportional, and parallel otherwise. This is $O(1)$ arithmetic operations: six multiplications and three subtractions for the determinants and two divisions.

**Parametric solution.** In the point-direction form, one cross product gives the denominator and one gives the numerator of $t$; the point is $p + t d$. This form is the natural one when the lines come from segments, and it gives the parameter that segment code needs.

**Exactness.** If the coefficients have absolute value at most $V$, then $|D|, |D_x|, |D_y| \le 2 V^2$, so the coordinates are rationals with numerator and denominator at most $2V^2$. For lines through integer points of absolute value at most $U$, the coefficients from the [line equation](/line-equation-from-segment/) give $V \le 2U^2$ for $C$ and $2U$ for $A, B$, so the denominator is at most $8U^2$ and the numerators at most $8 U^3$ in absolute value.

**Floating point.** With floating-point input, $D$ is computed with rounding error, and for nearly parallel lines it can have the wrong sign or be zero by cancellation. The point is then far away and very inaccurate: the problem itself is ill-conditioned when the angle between the lines is small. A robust program decides the case with an exact sign of $D$, using integers, rationals or [adaptive precision](/shewchuk-expansion-sum/), and computes the point afterwards.

## Bounds

The problem has constant size, so $O(1)$ arithmetic operations suffice and are necessary. The interesting measure is the precision: the decision "parallel or not" is the sign of a polynomial of degree $2$ in the coefficients, and the coordinates of the point are quotients of polynomials of degree $2$. For points as input, the denominator has degree $2$ and the numerators degree $3$ in the coordinates, which fixes the integer width that an exact implementation needs.

## Reductions

- **To a linear system.** The problem is the system $\begin{pmatrix} A_1 & B_1 \\ A_2 & B_2 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} -C_1 \\ -C_2 \end{pmatrix}$, and $D$ is its determinant.
- **Duality.** Under point-line duality, the intersection of two lines is the dual of the line through their two dual points, so the [line equation from a segment](/line-equation-from-segment/) and this problem are the same computation.
- **Inside other problems.** [Segment intersection](/segment-intersection-point/), the vertices of a [half-plane intersection](/half-plane-intersection/), each step of [polygon clipping](/polygon-clipping/), and the vertices of a [line arrangement](/line-arrangement/) are line-line intersections.

## Applications

- **Geometric algorithms.** The crossing points in [Bentley-Ottmann](/bentley-ottmann-algorithm/), the corners of clipped polygons and the vertices of convex regions.
- **Computer graphics.** Clipping a line to a window edge, and ray casting against straight walls in 2D games.
- **Surveying and navigation.** Finding a position from two bearings to known landmarks, which is the intersection of two lines through the landmarks.
- **Computer vision.** Vanishing points of an image are intersections of image lines, computed in homogeneous coordinates.

## References
