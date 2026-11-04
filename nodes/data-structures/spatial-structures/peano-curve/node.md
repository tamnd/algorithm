---
tag: KTFCA8
kind: concept
slug: peano-curve
name: Peano curve
aliases:
- Peano space-filling curve
area: data-structures/spatial-structures
level: advanced
summary: Original space-filling curve, which fills the unit square by recursive ternary subdivision.
prereqs: [space-filling-curve]
see_also: [hilbert-curve, z-order-curve, morton-encoding, linear-quadtree, locality-of-reference, cache-oblivious-model]
sources:
  - paper: doi:10.1007/BF01199438
    title: Giuseppe Peano, Sur une courbe, qui remplit toute une aire plane, Mathematische Annalen 36, 1890
    locator: pages 157 to 160 (the map from the ternary digits of t to the ternary digits of x and y, with the digit complement k)
  - book: isbn:9780387942650
    title: Hans Sagan, Space-Filling Curves, Springer, 1994
    locator: Chapter 3, Peano's space-filling curve (Peano's definition by ternary digits, the geometric generation by nine subsquares, continuity and nowhere differentiability)
  - book: isbn:9783642310454
    title: Michael Bader, Space-Filling Curves, An Introduction with Applications in Scientific Computing, Springer, 2013
    locator: the chapters on the Peano curve, its grammar and its use for cache-efficient matrix operations
---

The Peano curve is the first space-filling curve, published by Giuseppe Peano in 1890: a continuous map from the interval $[0, 1]$ onto the unit square. Peano defined it by a rule on ternary digits. Seen as a picture, it cuts the square into $3 \times 3$ subsquares, walks them in a snake order, up the first column, down the second and up the third, and does the same inside each subsquare with copies that are reflected so that the pieces join. Like the [Hilbert curve](/hilbert-curve/), each step of its discrete form goes to a neighboring cell, so it orders the cells of a $3^m \times 3^m$ grid with good locality.

## In plain words

Cut a square into nine small squares, three by three. Walk through them in a snake: up the left column, down the middle one, up the right one. Each step goes to a square next to the last one.

Now cut each small square into nine again, and walk each one in a snake too. Flip the small walks where needed, so that each one ends next to where the next one starts.

Do this again and again. The walk gets finer each time, and in the limit it passes through every point of the square, without lifting the pen.

## The idea

**Peano's rule.** Write $t \in [0, 1]$ in base 3 as $t = 0.t_1 t_2 t_3 t_4 \ldots$, and let $k(d) = 2 - d$ be the digit complement, with $k^j$ meaning $k$ applied $j$ times, which is $k$ when $j$ is odd and the identity when $j$ is even. Then
$$x = 0.\,a_1 a_2 a_3 \ldots, \quad a_i = k^{\,t_2 + t_4 + \cdots + t_{2i-2}}(t_{2i-1}),$$
$$y = 0.\,b_1 b_2 b_3 \ldots, \quad b_i = k^{\,t_1 + t_3 + \cdots + t_{2i-1}}(t_{2i}).$$
So the odd digits of $t$ give the digits of $x$ and the even digits give those of $y$, each one complemented when the sum of the earlier digits of the other kind is odd. A number with two ternary expansions, one ending in 0s and one in 2s, gives the same point either way, which is why the map is well defined.

**The discrete curve.** Take $2m$ digits. The index $d = (t_1 t_2 \ldots t_{2m})_3$, from 0 to $9^m - 1$, maps to the cell $(x, y) = ((a_1 \ldots a_m)_3, (b_1 \ldots b_m)_3)$ of the $3^m \times 3^m$ grid. The digits $t_1$ and $t_2$ choose the column and the row of the $3 \times 3$ block, and the complements make the path go down in the middle column and turn the copies at each level. The path starts at $(0, 0)$, ends at $(3^m - 1, 3^m - 1)$, and each step goes to a cell that shares an edge with the last one. Unlike the Hilbert curve, the copies are only reflected, never turned by 90 degrees, and the curve starts and ends at opposite corners.

**Continuity.** Map the interval $[q/9^m, (q+1)/9^m]$ to the cell of index $q$. If $9^{-(m+1)} < |s - t| \le 9^{-m}$, the two points lie in one interval of level $m$ or in two consecutive ones, whose cells share an edge and fit in a box of $2 \times 1$ cells of side $3^{-m}$. Since $3^{-m} < 3|s - t|^{1/2}$, this gives
$$\lVert p(s) - p(t) \rVert \le 3\sqrt 5\, |s - t|^{1/2},$$
a Hölder bound with exponent $1/2$, the best possible for a curve that preserves area. The curve is onto, nowhere differentiable, and not one to one.

**Compared with the Hilbert curve.** Both curves keep each step between neighbors, and both have the same Hölder exponent. The Peano curve uses base 3, so its grids have side $3^m$, and it splits a cell into 9 parts, not 4. This fits less well with binary coordinates and bit operations, which is why the Hilbert curve and the [Z-order curve](/z-order-curve/) are more common in spatial indexes. The base 3 is natural for some multigrid and matrix algorithms, which cut the data into $3 \times 3$ blocks.

## Examples

- **Order 1.** The $3 \times 3$ grid, with $y$ going up:

  | $y \backslash x$ | 0 | 1 | 2 |
  |---|---|---|---|
  | 2 | 2 | 3 | 8 |
  | 1 | 1 | 4 | 7 |
  | 0 | 0 | 5 | 6 |

  Column 0 goes up from 0 to 2, column 1 goes down from 3 to 5, column 2 goes up from 6 to 8.
- **Order 2.** The $9 \times 9$ grid is made of nine blocks of nine cells. The bottom left block holds 0 to 8 as in order 1. The block above it holds 9 to 17, a copy flipped left to right, so that it starts at $(2, 3)$ above the cell 8 at $(2, 2)$ and runs to 17 at $(0, 5)$. The block above that holds 18 to 26, which runs like order 1 again from $(0, 6)$ to $(2, 8)$. The middle column of blocks holds 27 to 53, going down, and the right column holds 54 to 80, going up, ending at $(8, 8)$.
- **One index.** Take $d = 50 = (1212)_3$, so $t_1 = 1$, $t_2 = 2$, $t_3 = 1$, $t_4 = 2$. Then $a_1 = t_1 = 1$; $b_1 = k^{t_1}(t_2) = k(2) = 0$; $a_2 = k^{t_2}(t_3) = t_3 = 1$, since $t_2 = 2$ is even; $b_2 = k^{t_1 + t_3}(t_4) = t_4 = 2$, since $t_1 + t_3 = 2$ is even. So $x = (11)_3 = 4$ and $y = (02)_3 = 2$: index 50 is the cell $(4, 2)$, in the middle column of blocks, bottom block.
- **The point of $t = 1/2$.** In base 3, $1/2 = 0.1111\ldots$. All digits are 1, and $k(1) = 1$, so all digits of $x$ and $y$ are 1, and $x = y = 0.111\ldots_3 = 1/2$. The curve passes through the center of the square at the middle of its time.

## Where it is used

- **Mathematics.** The curve showed in 1890 that a continuous image of an interval can fill a square, which was a surprise after Cantor's proof that the interval and the square have the same number of points. Together with Netto's theorem that no such map is one to one, it shaped the notion of dimension in topology.
- **Scientific computing.** Bader, Zenger and others used the Peano order for cache-efficient matrix multiplication and for traversing adaptive grids in partial differential equation solvers. The order visits the blocks so that consecutive steps share data, and it needs no knowledge of the cache size, as in the [cache-oblivious model](/cache-oblivious-model/).
- **Data layout.** Like other space-filling curves, the Peano order can store a grid in memory so that blocks of the grid are runs of memory, for [locality of reference](/locality-of-reference/).
- **Generalizations.** Wunderlich and others studied other Peano-type curves with a $3 \times 3$ split, which differ in how the nine subsquares are walked. The name "Peano curve" is also used, loosely, for any [space-filling curve](/space-filling-curve/).

## References
