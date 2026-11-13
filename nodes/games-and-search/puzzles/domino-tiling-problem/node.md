---
tag: YTYE25
kind: problem
slug: domino-tiling-problem
name: Domino tiling problem
aliases:
- Domino tiling counting
- Perfect matchings of grid graphs
area: games-and-search/puzzles
level: advanced
summary: Decide whether a region of the grid can be covered by dominoes, and count the ways. Deciding is bipartite matching; counting on planar regions is a determinant (Kasteleyn 1961).
prereqs: [perfect-matching, bipartite-matching]
see_also: [kasteleyn-method, counting-perfect-matchings, transfer-matrix-method, broken-profile-dp, hopcroft-karp, polyomino-tiling-problem, wang-tiling-problem, determinant]
sources:
  - paper: doi:10.1016/0031-8914(61)90063-5
    title: P. W. Kasteleyn, The statistics of dimers on a lattice I. The number of dimer arrangements on a quadratic lattice, Physica 27(12), 1961, 1209 to 1225
    locator: the product formula for the m by n rectangle and the limit of the count per cell
  - paper: doi:10.1080/14786436108243366
    title: H. N. V. Temperley and Michael E. Fisher, Dimer problem in statistical mechanics, an exact result, Philosophical Magazine 6(68), 1961, 1061 to 1063
    locator: the whole note (the same product formula, found independently)
  - paper: doi:10.2307/2324578
    title: William P. Thurston, Conway's tiling groups, The American Mathematical Monthly 97(8), 1990, 757 to 773
    locator: the height function of a domino tiling and the algorithm for simply connected regions
  - paper: doi:10.1007/s00454-016-9807-1
    title: Igor Pak, Adam Sheffer and Martin Tassy, Fast domino tileability, Discrete and Computational Geometry 56(2), 2016, 377 to 394
    locator: the introduction (Thurston's algorithm in O(a log a) for area a) and the main theorem (an algorithm in O(p log p) for perimeter p)
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 1979, 189 to 201
    locator: the #P-completeness of counting perfect matchings in bipartite graphs
  - paper: doi:10.37236/2554
    title: Igor Pak and Jed Yang, The complexity of generalized domino tilings, The Electronic Journal of Combinatorics 20(4), 2013, P12
    locator: the abstract and Section 1 (NP-completeness and #P-completeness for generalized dominoes in three and more dimensions)
  - paper: "Noam Elkies, Greg Kuperberg, Michael Larsen and James Propp, Alternating-sign matrices and domino tilings, Journal of Algebraic Combinatorics 1, 1992, 111 to 132 and 219 to 234"
    locator: the main theorem (the Aztec diamond of order n has 2^(n(n+1)/2) tilings)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing, 2009
    locator: Chapter 8 (determinants, Pfaffians and the dimer problem)
---

The domino tiling problem gives a finite region of the square grid and asks whether it can be covered by dominoes, rectangles of two cells, with no gaps and no overlaps, and in the counting form, how many such coverings exist. A tiling is the same thing as a [perfect matching](/perfect-matching/) of the grid graph of the region, so the decision form is [bipartite matching](/bipartite-matching/) and takes polynomial time. The counting form is #P-complete for general bipartite graphs, but for planar regions it is a determinant by the [Kasteleyn method](/kasteleyn-method/), and the $8 \times 8$ board has $12\,988\,816$ tilings. Wang's "domino problem" is a different problem, about tiling the plane with colored squares; see [Wang tiling](/wang-tiling-problem/).

## In plain words

You have a board made of squares, maybe with some squares cut out, and a large box of dominoes. Each domino covers two squares next to each other. Can you cover the whole board, every square exactly once?

Color the board like a chessboard. Every domino covers one dark and one light square. So if the counts of dark and light squares differ, the answer is no at once. When the counts are equal the answer can still be no, and a matching program finds the true answer fast.

Counting the coverings is harder. The number grows very fast, and you cannot list the coverings one by one on a large board. For flat boards a formula from physics turns the count into the value of one determinant of a table of numbers, and computers find that value fast.

## Definition

A *region* is a finite set $R \subset \mathbb{Z}^2$ of cells. Its *grid graph* $G(R)$ has a vertex for each cell and an edge between two cells at distance 1. A *domino* is a set of two adjacent cells, and a *domino tiling* of $R$ is a set of dominoes that partitions $R$. So the tilings of $R$ are exactly the perfect matchings of $G(R)$.

- **Decision.** Given $R$, does $R$ have a tiling?
- **Search.** Given $R$, output a tiling or report that none exists.
- **Counting.** Given $R$, compute the number $T(R)$ of tilings.

Color the cell $(r, c)$ black when $r + c$ is even and white otherwise. Every edge of $G(R)$ joins a black cell to a white cell, so $G(R)$ is a [bipartite graph](/bipartite-graph/), and a tiling needs as many black cells as white cells. Write $T(m, n)$ for the number of tilings of the $m \times n$ rectangle and $a = |R|$ for the area.

## Variants

- **Rectangles.** $T(m, n)$ has the closed form in Examples, found in 1961 by Kasteleyn and, independently, by Temperley and Fisher.
- **Simply connected regions.** A region with no holes. Thurston (1990) assigned to each tiling a *height function* on the vertices of the cells and showed that the region is tilable exactly when a lowest height function exists; it is built in nearly linear time.
- **Regions with holes.** Matching still decides tilability. Counting still works, since every planar graph has a Pfaffian orientation (Kasteleyn 1963, see the [Kasteleyn method](/kasteleyn-method/)), but the simple sign rule for rectangles must be adjusted around each hole.
- **The torus.** With the left side glued to the right and the top to the bottom, the grid graph is no longer planar, and Kasteleyn (1961) wrote the count as a signed sum of four Pfaffians.
- **Three and more dimensions.** Bricks of $2 \times 1 \times 1$ cells in a region of $\mathbb{Z}^3$. The cubic grid graph is still bipartite, so the decision is still matching. Pak and Yang (2013) proved NP-completeness and #P-completeness for several generalized dominoes in three and more dimensions; for example, counting tilings by $2 \times 2 \times 1$ slabs is #P-complete.
- **Other tiles.** Trominoes and larger polyominoes give the NP-complete [polyomino tiling problem](/polyomino-tiling-problem/), which is a different problem.

## Examples

**Small rectangles.** The values of $T(m, n)$ for $m, n \le 8$. A board with an odd number of cells has no tiling.

| $m \backslash n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
| 2 | 1 | 2 | 3 | 5 | 8 | 13 | 21 | 34 |
| 3 | 0 | 3 | 0 | 11 | 0 | 41 | 0 | 153 |
| 4 | 1 | 5 | 11 | 36 | 95 | 281 | 781 | 2245 |
| 5 | 0 | 8 | 0 | 95 | 0 | 1183 | 0 | 14824 |
| 6 | 1 | 13 | 41 | 281 | 1183 | 6728 | 31529 | 167089 |
| 7 | 0 | 21 | 0 | 781 | 0 | 31529 | 0 | 1292697 |
| 8 | 1 | 34 | 153 | 2245 | 14824 | 167089 | 1292697 | 12988816 |

**The $2 \times n$ strip.** $T(2, n) = F_{n+1}$, the [Fibonacci numbers](/fibonacci-numbers/) with $F_1 = F_2 = 1$. *Proof.* The cell in the top left corner is covered either by a vertical domino, which leaves a $2 \times (n - 1)$ strip, or by a horizontal domino. In the second case the cell below it can only be covered by a second horizontal domino, which leaves a $2 \times (n - 2)$ strip. So $T(2, n) = T(2, n - 1) + T(2, n - 2)$ with $T(2, 0) = T(2, 1) = 1$. $\square$

**The product formula.** For all $m, n \ge 1$,

$$T(m, n) = \prod_{j=1}^{\lceil m/2 \rceil} \prod_{k=1}^{\lceil n/2 \rceil} \left( 4 \cos^2 \frac{\pi j}{m + 1} + 4 \cos^2 \frac{\pi k}{n + 1} \right).$$

When $m$ and $n$ are both odd, the factor with $j = (m+1)/2$ and $k = (n+1)/2$ is 0. For the $8 \times 8$ board the 16 factors multiply to $12\,988\,816 = 3604^2$. The number per cell tends to a limit: $\frac{1}{mn} \ln T(m, n) \to G / \pi \approx 0.29156$ as $m, n \to \infty$, where $G = 0.91597\ldots$ is Catalan's constant (Kasteleyn 1961). The convergence is slow: the value is $0.2559$ for $8 \times 8$ and $0.2628$ for $10 \times 10$.

**The mutilated chessboard.** Remove two opposite corners from the $8 \times 8$ board. Both corners have the same color, so 30 cells of that color and 32 of the other remain. Each domino covers one cell of each color, so 31 dominoes would cover 31 of each, and the region has no tiling. A matching program reaches the same answer, but it cannot give this short reason.

**Remove one cell of each color.** The $8 \times 8$ board minus any black cell and any white cell always has a tiling. *Proof.* Walk the board in a closed path that visits every cell once and moves between adjacent cells: go along row 0 from left to right, then snake back through columns 1 to 7 of rows 1 to 7, and return to the start along column 0. The colors alternate along this cycle of 64 cells, so a black cell and a white cell are an odd number of steps apart in both directions. Removing them cuts the cycle into two paths, possibly one empty, and each path has an even number of cells. Pair consecutive cells along each path. $\square$

**The Aztec diamond.** The region of cells $(r, c)$ with $|2r + 1| + |2c + 1| \le 2n$ has $2^{n(n+1)/2}$ tilings (Elkies, Kuperberg, Larsen and Propp 1992): 2, 8, 64, 1024 and 32768 for $n = 1$ to 5.

## Known algorithms

- **Decision and search.** Find a maximum matching of the bipartite graph $G(R)$ with [Hopcroft and Karp](/hopcroft-karp/). The graph has $a$ vertices and fewer than $2a$ edges, so this takes $O(a^{3/2})$ time. [Hall's theorem](/hall-theorem/) gives the certificate when there is no tiling: a set of black cells with fewer white neighbors than its size, which is the general form of the coloring argument.
- **Simply connected regions.** Thurston's height function algorithm builds the lowest height function from the boundary and reads off a tiling, or finds that none exists. Pak, Sheffer and Tassy (2016) state its time as $O(a \log a)$ and give an algorithm in $O(p \log p)$, where $p$ is the perimeter of the region.
- **Counting on planar regions.** The [Kasteleyn method](/kasteleyn-method/) signs the edges so that every inner face of length 4 has an odd number of minus signs. Then $T(R)$ is the absolute value of the [determinant](/determinant/) of the signed biadjacency matrix, of order $a/2$, which [Gaussian elimination](/gaussian-elimination/) computes in $O(a^3)$ arithmetic operations. On a rectangle the signs are $+1$ on horizontal edges and $(-1)^c$ on the vertical edge in column $c$.
- **Counting on thin regions.** The [transfer-matrix method](/transfer-matrix-method/) sweeps the region one column at a time; the state is the set of cells of the next column already covered. With the cell-by-cell [broken profile](/broken-profile-dp/), an $m \times n$ region needs $O(mn\,2^m)$ steps. This works for any region and any weights, planar or not, when one side is small.
- **Exhaustive search.** Cover the first free cell in each possible way and recurse. This lists every tiling, so the time is at least $T(R)$, and it is useful only on small regions.

## Bounds

- **Decision.** In polynomial time for every region, in every dimension, by matching.
- **Counting.** For planar regions in polynomial time, by the determinant. For general bipartite graphs counting perfect matchings is #P-complete (Valiant 1979), see [counting perfect matchings](/counting-perfect-matchings/); in three dimensions several generalized domino tilings are #P-complete to count (Pak and Yang 2013).
- **Growth.** $\ln T(n, n) = (G/\pi) n^2 + O(n)$, so a listing algorithm needs $e^{\Theta(n^2)}$ time on the $n \times n$ board.

## Reductions

- **To perfect matching.** A tiling of $R$ is a perfect matching of $G(R)$, so the decision reduces to [bipartite matching](/bipartite-matching/) and the counting to [counting perfect matchings](/counting-perfect-matchings/).
- **To a determinant.** For planar $G(R)$ the Kasteleyn signs make every term of the determinant count with the same sign, so the count becomes a determinant.
- **Not from Wang tiles.** Wang's domino problem asks whether square tiles with colored edges can tile the whole plane. It is undecidable and has no link to this problem beyond the name.

## Applications

- **Statistical physics.** The *dimer model* puts dimers, molecules that cover two adjacent sites, on a lattice. Its partition function is the weighted count of tilings, and the 1961 papers of Kasteleyn and of Temperley and Fisher solved it for the square lattice.
- **Puzzles.** The mutilated chessboard is a classic test of proofs by invariants, and domino rules appear in many grid puzzles.
- **Random tilings.** Uniform random tilings of large regions, sampled through the determinant or by Markov chains on height functions, show frozen regions near the boundary, for example in the Aztec diamond.

## References
