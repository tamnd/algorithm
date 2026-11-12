---
tag: YVD13Y
kind: algorithm
slug: marching-squares
name: Marching squares
aliases:
- 2D marching cubes
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: Extracts contour lines of a 2D scalar field from the sign pattern on each grid cell.
solves: [isosurface-extraction]
model: real-ram
complexity:
  vars: {w: the number of samples in a row, h: the number of rows}
  time: {worst: Θ(w h), average: Θ(w h), best: Θ(w h)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1987
  people: [William E. Lorensen, Harvey E. Cline]
  note: Marching squares is the 2D form of the marching cubes method of Lorensen and Cline; Nielson and Hamann (1991) resolved its two saddle cases with the asymptotic decider.
prereqs: [isosurface-extraction, bilinear-interpolation]
see_also: [marching-cubes, marching-tetrahedra, dual-contouring, implicit-surface, level-set-method, curve-simplification, flood-fill]
sources:
  - paper: doi:10.1145/37401.37422
    title: William E. Lorensen and Harvey E. Cline, Marching cubes, a high resolution 3D surface construction algorithm, Computer Graphics (SIGGRAPH 87 Proceedings) 21(4), 163 to 169, 1987
    locator: the whole paper (the cell by cell case table, which marching squares reduces to two dimensions)
  - paper: doi:10.1109/VISUAL.1991.175782
    title: Gregory M. Nielson and Bernd Hamann, The asymptotic decider, resolving the ambiguity in marching cubes, Proceedings of Visualization 91, IEEE, 83 to 91, 1991
    locator: the whole paper (the bilinear interpolant on a face, its saddle value and the decision rule for the two ambiguous cases)
  - book: isbn:9781930934191
    title: Will Schroeder, Ken Martin and Bill Lorensen, The Visualization Toolkit, An Object-Oriented Approach to 3D Graphics, fourth edition, Kitware, 2006
    locator: Chapter 6, Fundamental Algorithms, Section 6.2, Scalar Algorithms (contouring, the 16 marching squares cases and the ambiguous cases 5 and 10)
---

Marching squares draws the contour lines $f = c$ of a function $f$ that is known only at the points of a rectangular grid. It looks at one grid cell at a time. The four corners of the cell are each inside ($f < c$) or outside, which gives one of 16 cases, and a table gives the one or two line segments that cross the cell in that case. The segment endpoints are on the cell edges, at the points where linear interpolation of the two corner values gives $c$. Two cases are saddles, where the table has two possible answers; the asymptotic decider of Nielson and Hamann picks the answer that matches the bilinear interpolant of the cell. The cost is $\Theta(wh)$ for a $w \times h$ grid.

## In plain words

You have a map of heights measured at the points of a grid, and you want the line that marks one height, as on a contour map. Look at one small square of the grid at a time. Each corner is below the height or not, so there are 16 patterns. For most patterns the line enters the square through one side and leaves through another, and you can read the two sides from a small table. On each side, the line crosses at the point where the height changes from below to above, found by a straight-line guess between the two corners.

Two patterns have the two low corners on opposite corners of the square. Then the line can go either way. A test on the four corner heights picks the way that matches a smooth surface through the corners.

## The problem

The input is a grid of samples $g[j][i]$ for $0 \le i < w$ and $0 \le j < h$, with $w, h \ge 2$, where $g[j][i]$ is the value of $f$ at the point $(i, j)$, and an iso value $c$. This is the 2D case of [isosurface extraction](/isosurface-extraction/). A sample is inside when $g[j][i] < c$ and outside when $g[j][i] \ge c$, so a sample equal to $c$ counts as outside. Cell $(i, j)$, for $0 \le i < w - 1$ and $0 \le j < h - 1$, is the unit square with corners

$$p_0 = (i, j),\quad p_1 = (i+1, j),\quad p_2 = (i+1, j+1),\quad p_3 = (i, j+1),$$

counted counterclockwise, with values $f_0, \ldots, f_3$. Edge $e$ of the cell joins corners $e$ and $e + 1 \bmod 4$: edge 0 is the bottom, 1 the right, 2 the top and 3 the left. The output is a set of line segments. Inside the cell, the target curve is the level set of the [bilinear interpolant](/bilinear-interpolation/)

$$b(x, y) = f_0 (1 - x)(1 - y) + f_1 x (1 - y) + f_2 x y + f_3 (1 - x) y$$

in local coordinates $x, y \in [0, 1]$. The output is a piecewise linear curve with the same crossings on the grid edges and, in each cell, the same separation of the corners as the curve $b = c$.

## The algorithm

The case number of a cell is $\sum_k 2^k [f_k < c]$. For each case, the table lists the segments as pairs of edges, oriented so that the inside is on the left. Cases 0 and 15 have no segment. Cases 5 (corners 0 and 2 inside) and 10 (corners 1 and 3 inside) are the saddles and have two entries.

| case | inside corners | segments (edge to edge) |
| --- | --- | --- |
| 1, 2, 4, 8 | one corner $k$ | from edge $k$ to edge $k - 1$: $(0,3)$, $(1,0)$, $(2,1)$, $(3,2)$ |
| 14, 13, 11, 7 | all but corner $k$ | from edge $k - 1$ to edge $k$: $(3,0)$, $(0,1)$, $(1,2)$, $(2,3)$ |
| 3, 6, 12, 9 | two corners on one edge | $(1,3)$, $(2,0)$, $(3,1)$, $(0,2)$ |
| 5 separated | 0 and 2 | $(0,3)$ and $(2,1)$ |
| 5 joined | 0 and 2 | $(0,1)$ and $(2,3)$ |
| 10 separated | 1 and 3 | $(1,0)$ and $(3,2)$ |
| 10 joined | 1 and 3 | $(1,2)$ and $(3,0)$ |

```pseudo id=main
MARCHING-SQUARES(g, c)                         ▷ g[j][i] = f(i, j), w by h samples
L1  S ← empty list
L2  for j ← 0 to h − 2 do
L3      for i ← 0 to w − 2 do
L4          f_k ← g at corner p_k of cell (i, j), for k = 0..3
L5          case ← Σ_k 2^k · [f_k < c]
L6          if case = 5 or case = 10 then
L7              s ← (f_0 f_2 − f_1 f_3) / (f_0 + f_2 − f_1 − f_3)    ▷ the saddle value
L8              pairs ← TABLE[case, joined] if s < c else TABLE[case, separated]
L9          else pairs ← TABLE[case]
L10         for each (a, b) in pairs do
L11             append (CROSS(a), CROSS(b)) to S
L12 return S

CROSS(e)                                         ▷ edge e of the current cell, from p_u to p_v
L13 t ← (c − f_u) / (f_v − f_u)
L14 return p_u + t (p_v − p_u)
```

Line L5 reads the sign pattern. Lines L6 to L8 are the asymptotic decider. The bilinear interpolant $b$ has one critical point, a saddle, and $s$ is its value there. In a saddle case the saddle point is inside the cell, and the two inside corners are joined in $\{b < c\}$ exactly when $s < c$. Line L13 is only reached on an edge with one corner inside and one outside, so $f_v \ne f_u$ and $0 < t \le 1$. The implementation computes the test $s < c$ of line L8 as $f_0 f_2 - f_1 f_3 < c\,d$ for $d = f_0 + f_2 - f_1 - f_3 > 0$, with the inequality reversed for $d < 0$, so it needs no division. With integer or rational samples and a rational $c$, all endpoints are exact rationals.

The output is a list of oriented segments, each once. A crossing point on an edge inside the grid is the end of one segment of one cell and the start of one segment of the other cell. To get polylines, join each segment to the one that starts at its end point, with a [hash table](/hash-table/) keyed by the point, in $O(|S|)$ expected time.

## Example

Take $c = 2$ and the $4 \times 4$ grid below, with rows $j = 0$ to $3$ from top to bottom as written in the code. The inside samples are $g[1][1] = 0$ and $g[2][2] = 1$.

$$g = \begin{pmatrix} 3 & 3 & 3 & 3 \\ 3 & 0 & 4 & 3 \\ 3 & 4 & 1 & 3 \\ 3 & 3 & 3 & 3 \end{pmatrix}$$

The nine cells give:

| cell $(i, j)$ | $(f_0, f_1, f_2, f_3)$ | case | segments |
| --- | --- | --- | --- |
| (0, 0) | (3, 3, 0, 3) | 4 | $(\tfrac13, 1) \to (1, \tfrac13)$ |
| (1, 0) | (3, 3, 4, 0) | 8 | $(1, \tfrac13) \to (\tfrac32, 1)$ |
| (2, 0) | (3, 3, 3, 4) | 0 | none |
| (0, 1) | (3, 0, 4, 3) | 2 | $(1, \tfrac32) \to (\tfrac13, 1)$ |
| (1, 1) | (0, 4, 1, 4) | 5, $s = \tfrac{16}{7}$ | $(\tfrac32, 1) \to (1, \tfrac32)$ and $(\tfrac53, 2) \to (2, \tfrac53)$ |
| (2, 1) | (4, 3, 3, 1) | 8 | $(2, \tfrac53) \to (\tfrac52, 2)$ |
| (0, 2) | (3, 4, 3, 3) | 0 | none |
| (1, 2) | (4, 1, 3, 3) | 2 | $(2, \tfrac52) \to (\tfrac53, 2)$ |
| (2, 2) | (1, 3, 3, 3) | 1 | $(\tfrac52, 2) \to (2, \tfrac52)$ |

In cell (0, 0), the top edge runs from $p_2 = (1, 1)$ with value 0 to $p_3 = (0, 1)$ with value 3, so $t = 2/3$ and the crossing is $(\tfrac13, 1)$. The center cell (1, 1) is a saddle with $d = 0 + 1 - 4 - 4 = -7$ and $s = (0 \cdot 1 - 4 \cdot 4)/(-7) = 16/7$. Since $16/7 > 2$, the saddle point is outside, and the two inside corners are separated. The 8 segments form two closed diamonds, one around $(1, 1)$ with area $49/72$ and one around $(2, 2)$ with area $25/72$.

With $c = 5/2$, the cell cases are the same, but now $16/7 < 5/2$, so the center cell takes the joined entry $(0, 1)$ and $(2, 3)$. It gives $(\tfrac{13}{8}, 1) \to (2, \tfrac32)$ and $(\tfrac32, 2) \to (1, \tfrac{13}{8})$, which cut off the outside corners 1 and 3. The 8 segments now form one closed curve around both inside samples, with area $673/288$. A table without the decider would give the same picture for both values of $c$.

## Correctness

**Claim.** Assume no sample equals $c$. Then (1) the endpoints of the output segments are exactly the points on the grid edges where the linear interpolant of the two end values equals $c$; (2) each segment has the inside on its left; (3) each crossing on an edge inside the grid is the end of exactly one segment and the start of exactly one segment; (4) in each cell, two corners are on the same side of the segments if and only if they are in the same component of $\{b < c\}$ or of $\{b \ge c\}$ in the cell. If every sample on the border of the grid is outside, the segments form disjoint closed polygons.

Statement (1) and (2) are a check of the 16 table entries. Statement (3) follows from (2): the two segments at a crossing lie in the two cells on the two sides of the edge, so one of them must leave the point and the other must arrive at it. Statement (4) needs the saddle value: $b(x, y) = d (x - x_0)(y - y_0) + s$, and $b = s$ on the two lines $x = x_0$ and $y = y_0$ through the saddle point. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/), or exact rational arithmetic on numbers of bounded size, with unit cost for each comparison and each arithmetic operation on the samples.

- **Time.** The loops visit the $(w - 1)(h - 1)$ cells once. Each cell costs $O(1)$: four comparisons, at most one decider and at most two segments of two crossings each. The time is $\Theta(wh)$ in all cases, whether or not the curve meets the cell.
- **Output.** There are at most $2(w - 1)(h - 1)$ segments.
- **Space.** Besides the input and the output, the loop keeps $O(1)$ values. Joining the segments into polylines takes $O(|S|)$ extra space.

The time is linear in the number of cells, not in the length of the output. A [flood fill](/flood-fill/) or contour tracing that starts at one known crossing and follows the curve from cell to cell visits only the cells that the curve meets, which is output sensitive for one component.

## Properties

- **Local.** The answer in a cell depends only on its four samples, so cells can be processed in any order or in parallel.
- **Consistent at shared edges.** Two neighboring cells compute the crossing on their shared edge from the same two samples, so their segments meet exactly.
- **Closed contours.** If the field is outside on the whole border, each contour is a closed polygon. Otherwise, contours can end on the border.
- **Topology of the bilinear interpolant.** With the decider, each cell separates its corners as the bilinear interpolant does. Without it, the cell picks one of the two saddle entries by a fixed rule; the output is still a set of closed curves, but it can differ from the bilinear one.
- **Not the true curve.** The segments are a linear approximation of $b = c$ in each cell. A component of $\{f < c\}$ that falls between samples is missed.

## Variants and improvements

- **Fixed saddle rule.** Many programs drop lines L6 to L8 and always take one saddle entry, or decide from the average of the four corners. Both give closed curves, because the choice reads only one cell, but the topology can differ from the bilinear one.
- **Isobands.** A variant marks each sample as below, between or above two values $c_1 < c_2$ and fills the band between them, with $3^4 = 81$ cases.
- **Triangles.** Split each cell into two triangles and contour each with linear interpolation. Each triangle has one segment at most and no ambiguity, as in [marching tetrahedra](/marching-tetrahedra/). The result depends on which diagonal is used.
- **3D.** [Marching cubes](/marching-cubes/) uses the same idea on cubes with 256 cases. Each face of a cube is a marching squares cell, and the decider is used on faces.
- **Sharp corners.** With gradients at the crossings, [dual contouring](/dual-contouring/) puts one vertex in each cell at the point that best fits the tangent lines, which keeps corners.
- **Output sensitive.** Store cells by their minimum and maximum value, as in the span space of [isosurface extraction](/isosurface-extraction/), to visit only cells that the contour meets.
- **Simplification.** The output has many short segments. [Curve simplification](/curve-simplification/) reduces them after the extraction.

## When to use it

Use marching squares to draw contour lines of gridded data, such as heights, temperature or a 2D [implicit curve](/implicit-surface/) sampled on a grid, and for the boundary of a thresholded image. It is short, exact on rational input, and local. When the field is a [level set](/level-set-method/) of a moving front, use it to draw the zero contour of each step. When only one contour component through a known point is needed, follow it from cell to cell instead of scanning the whole grid.

## Pitfalls

- **Ties at a sample.** If a sample equals $c$ and the code tests $f_k \le c$ in one place and $f_k < c$ in another, neighboring cells disagree and the curve has gaps. Use one rule, such as inside if and only if $f_k < c$ in line L5, everywhere. Even with one rule, a sample equal to $c$ gives $t = 1$ in line L13, so crossings from different edges can meet at that sample and give segments of length zero.
- **Crossing from the wrong corner.** Line L13 must measure $t$ from the corner $p_u$ whose value is $f_u$, as in $t = (c - f_u)/(f_v - f_u)$. Computing $t$ from $p_u$ with $f_v$ in place of $f_u$, or the midpoint $t = 1/2$ in every case, still gives a closed curve but in the wrong place.
- **Saddle decided per cell from local guesses.** A rule that reads values outside the cell, or a random choice, can still give closed curves, but they change when the grid is cut into blocks. Decide from the four samples of the cell only, as in lines L7 and L8.
- **Division in the decider.** Computing $s$ by floating point division and comparing it with $c$ can flip the answer near $s = c$. Compare $f_0 f_2 - f_1 f_3$ with $c\,d$ and flip the test when $d < 0$, as the implementation does.
- **Orientation lost.** A table that does not orient the segments with the inside on one side makes it hard to join segments into polylines and to tell holes from islands. Keep the orientation of the table above.

## Implementations

## History

Marching cubes, published by Lorensen and Cline in 1987, processes a volume cell by cell with a case table, and its 2D form is called marching squares. Dürst (1988) noted that the cube table has ambiguous faces, which are the saddle cases 5 and 10 of marching squares. Nielson and Hamann (1991) gave the asymptotic decider: compare the saddle value of the bilinear interpolant on the face with the iso value.

## References
