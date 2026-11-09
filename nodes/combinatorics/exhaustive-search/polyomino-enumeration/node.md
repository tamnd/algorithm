---
tag: D8FD5N
kind: problem
slug: polyomino-enumeration
name: Polyomino enumeration
aliases:
- enumeration of polyominoes
- fixed polyominoes
area: combinatorics/exhaustive-search
level: advanced
summary: List all polyominoes of a given size, up to translation, rotation or reflection.
prereqs: [enumeration-problem, burnside-lemma, depth-first-search]
see_also: [redelmeier-algorithm, polyomino-tiling-problem, self-avoiding-walk-enumeration, transfer-matrix-method, burnside-lemma, exact-cover, combinatorial-explosion, enumeration-problem]
sources:
  - paper: doi:10.1016/0012-365X(81)90237-5
    title: D. Hugh Redelmeier, Counting polyominoes, yet another attack, Discrete Mathematics 36(2), 1981, 191 to 203
    locator: the method that lists each fixed polyomino once, and the counts up to 24 cells
  - url: https://oeis.org/A001168
    title: OEIS A001168, number of fixed polyominoes with n cells
    locator: the table of values
  - url: https://oeis.org/A000105
    title: OEIS A000105, number of free polyominoes with n cells
    locator: the table of values
  - url: https://oeis.org/A000988
    title: OEIS A000988, number of one-sided polyominoes with n cells
    locator: the table of values
  - paper: "David A. Klarner, Cell growth problems, Canadian Journal of Mathematics 19, 1967, 851 to 863"
    locator: the inequality a(m) a(n) at most a(m + n) and the existence of the growth constant
  - paper: "Gill Barequet, Günter Rote and Mira Shalah, λ > 4: an improved lower bound on the growth constant of polyominoes, Communications of the ACM 59(7), 2016, 88 to 95"
    locator: the lower bound λ > 4.00253 and the survey of the known bounds and estimates
  - paper: "Iwan Jensen, Enumerations of lattice animals and trees, Journal of Statistical Physics 102, 2001, 865 to 881"
    locator: the transfer-matrix count of fixed polyominoes and the estimate of the growth constant
---

Polyomino enumeration asks for all polyominoes with $n$ cells, or for their number. A polyomino is a connected set of squares of the grid, joined edge to edge, and three kinds are counted: *fixed* polyominoes, which are equal only up to translation; *one-sided* polyominoes, which may also be rotated; and *free* polyominoes, which may also be reflected. No formula for these numbers is known, and they grow like $\lambda^n$ with $\lambda \approx 4.06$, so every method is an exhaustive search or a clever count. [Redelmeier's algorithm](/redelmeier-algorithm/) lists the fixed polyominoes one at a time with almost no memory, and the [transfer-matrix method](/transfer-matrix-method/) counts them much further.

## In plain words

Take some equal squares and join them edge to edge, like the pieces of the game Tetris. Each such shape is a polyomino. With 4 squares there are 5 different shapes if you may turn and flip them. Tetris has 7 pieces, because it does not let you flip them. With 5 squares there are 12 shapes, the pentominoes.

The question is how many shapes there are for a given number of squares, and how to list them all. Nobody knows a formula. The only known ways are to build the shapes one by one, or to count them by a smart method that builds them column by column. The numbers grow fast: each extra square multiplies them by about four.

## Definition

A *cell* is a unit square of the grid $\mathbb{Z}^2$. Two cells are *adjacent* when they share an edge. A *polyomino with $n$ cells* is a set of $n$ cells that is connected under adjacency.

- A *fixed* polyomino is an equivalence class of such sets under translation. Their number is $a(n)$.
- A *one-sided* polyomino is a class under translations and rotations by multiples of $90°$.
- A *free* polyomino is a class under translations, rotations and reflections, that is, under the 8 symmetries of the square together with translations. Their number is $f(n)$.

The *enumeration problem* is to list one representative of every class for a given $n$, and the *counting problem* is to find $a(n)$ or $f(n)$. The input is the number $n$ alone, so its size is $\Theta(\log n)$; the output is exponential in $n$.

## Variants

- **Kinds of equivalence.** Fixed, one-sided and free, as above. Free counts follow from fixed counts with symmetries by [Burnside's lemma](/burnside-lemma/).
- **Other cells.** Polyiamonds use triangles, and polyhexes use hexagons. Polycubes use cubes in three or more dimensions. In physics, all of these are *lattice animals*.
- **Restricted shapes.** Polyominoes with no holes, convex polyominoes, column-convex polyominoes, and directed animals. Many of these classes have known generating functions, unlike the general class.
- **Counting by perimeter or area.** The count by both the number of cells and the perimeter is a central object in statistical physics.
- **Connected subgraphs.** On a general graph, list the connected sets of $n$ vertices. Polyominoes are the case of the square grid.

## Examples

The counts for small $n$:

| $n$ | fixed $a(n)$ | one-sided | free $f(n)$ |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 1 |
| 3 | 6 | 2 | 2 |
| 4 | 19 | 7 | 5 |
| 5 | 63 | 18 | 12 |
| 6 | 216 | 60 | 35 |
| 7 | 760 | 196 | 108 |
| 8 | 2,725 | 704 | 369 |
| 9 | 9,910 | 2,500 | 1,285 |
| 10 | 36,446 | 9,189 | 4,655 |

**Trominoes.** With 3 cells, there are 2 free polyominoes, the straight I and the bent L. The I has 2 fixed forms, horizontal and vertical. The L has 4 fixed forms, one for each rotation, and a reflection of an L is a rotation of it, so it is one one-sided polyomino. So $a(3) = 6$.

**Tetrominoes and Burnside's lemma.** The 19 fixed tetrominoes give the one-sided count by Burnside's lemma for the 4 rotations. The square O is fixed by all of them. Under the half turn, the fixed forms are O, the two forms of I, the two forms of S and the two forms of Z, 7 in all. Under the quarter turns, only O is fixed. So the number of one-sided tetrominoes is $(19 + 1 + 7 + 1)/4 = 7$.

**Pentominoes.** The 12 free pentominoes are the pieces of the classic tiling puzzles. Tiling a $6 \times 10$ rectangle with them is an [exact cover](/exact-cover/) problem with 2,339 solutions up to symmetry.

**A non-example.** Two squares that touch only at a corner do not form a polyomino, since adjacency is through edges.

## Known algorithms

- **Growth with a table.** Build the polyominoes with $n$ cells from those with $n - 1$ cells by adding one adjacent cell, and remove repeats with a hash table of canonical forms. This is simple but stores all $a(n-1)$ polyominoes, so memory runs out early.
- **Redelmeier's algorithm (1981).** A depth-first search that grows polyominoes cell by cell from a set of untried cells and never makes a fixed polyomino twice, with no table. It takes $O(1)$ amortized time per fixed polyomino in its original form and memory linear in $n$. See [Redelmeier's algorithm](/redelmeier-algorithm/).
- **Transfer matrices.** Count the polyominoes inside a strip of fixed width by a [transfer-matrix method](/transfer-matrix-method/) that moves across the strip one cell at a time, and combine the strips. This counts without listing, in time exponential in $n$ but with a much smaller base than $a(n)$. Jensen used it to count fixed polyominoes far beyond the sizes that any listing method can reach.
- **Free counts.** For each symmetry $g$ of the square, count the fixed polyominoes that $g$ maps to themselves, which is a much smaller search. Then $f(n)$ is the average of these counts over the 8 symmetries, by Burnside's lemma.

## Bounds

**Growth constant.** Klarner (1967) showed that $a(m)\,a(n) \le a(m + n)$: place a polyomino with $m$ cells and one with $n$ cells so that the last cell of the first touches the first cell of the second, in a way that loses no information. By Fekete's lemma the limit

$$\lambda = \lim_{n \to \infty} a(n)^{1/n} = \sup_{n} a(n)^{1/n}$$

exists. It is called *Klarner's constant*. Its value is not known. Barequet, Rote and Shalah (2016) proved $\lambda > 4.00253$, and an upper bound of about $4.65$ is due to Klarner and Rivest. Series analysis gives the estimate $\lambda \approx 4.0626$.

**Asymptotic form.** The counts are believed to satisfy $a(n) \sim C \lambda^n / n$ for a constant $C$, but this is not proven. Since almost all large polyominoes have no symmetry, $f(n) \sim a(n) / 8$.

**Cost of listing.** Any method that lists the fixed polyominoes needs time at least $a(n)$, which grows like $4.06^n$. Redelmeier's method reaches this up to a constant factor.

## Reductions

- **Polyomino tiling to exact cover.** Each placement of a polyomino on a board is an option, and the cells and the pieces are the items. See the [polyomino tiling problem](/polyomino-tiling-problem/).
- **Polyominoes as connected subgraphs.** A fixed polyomino with $n$ cells is a connected set of $n$ vertices of the grid graph whose first vertex in row order is a fixed vertex. So methods for connected induced subgraphs apply.
- **Self-avoiding walks.** A polyomino that is a single path of cells corresponds to a [self-avoiding walk](/self-avoiding-walk-enumeration/), and the two counting problems use the same methods.

## Applications

- **Statistical physics.** Lattice animals model branched polymers and the clusters of percolation, and their counts and growth constants enter estimates of critical exponents.
- **Recreational mathematics.** Pentomino and hexomino puzzles, packing problems, and games such as Tetris use the lists of small polyominoes.
- **Tiling theory.** Lists of polyominoes are the input for questions such as which polyominoes tile the plane, or which tile a rectangle.
- **Test cases for search.** The counts are a standard benchmark for exhaustive search and parallel enumeration.

## References
