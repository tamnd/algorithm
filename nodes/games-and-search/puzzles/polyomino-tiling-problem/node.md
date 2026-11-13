---
tag: 6M5XGW
kind: problem
slug: polyomino-tiling-problem
name: Polyomino tiling problem
aliases:
- Polyomino packing
- Pentomino tiling
area: games-and-search/puzzles
level: advanced
summary: Decide whether a finite region of the grid can be covered exactly by copies of given polyominoes. NP-complete even for the right tromino alone; tiling the whole plane is undecidable.
prereqs: [exact-cover, np-complete]
see_also: [algorithm-x, dancing-links, polyomino-enumeration, domino-tiling-problem, wang-tiling-problem, one-in-three-sat, perfect-matching, sat]
sources:
  - paper: doi:10.1007/s00454-001-0047-6
    title: Cristopher Moore and John Michael Robson, Hard tiling problems with simple tiles, Discrete and Computational Geometry 26(4), 2001, 573 to 590
    locator: the abstract and the reduction from monotone 1-in-3 satisfiability on planar cubic graphs (the right tromino with the square tetromino, the right tromino alone, and the results on higher-dimensional lattices)
  - paper: doi:10.1016/S0021-9800(70)80055-2
    title: Solomon W. Golomb, Tiling with sets of polyominoes, Journal of Combinatorial Theory 9(1), 1970, 60 to 71
    locator: the equivalence of tiling the plane with a finite set of polyominoes and Wang's domino problem
  - paper: "Nicolas Ollinger, Tiling the plane with a fixed number of polyominoes, Language and Automata Theory and Applications (LATA 2009), Lecture Notes in Computer Science 5457, 2009, 638 to 647"
    locator: the undecidability of tiling the plane with sets of 5 polyominoes
  - paper: "John H. Conway and Jeffrey C. Lagarias, Tiling with polyominoes and combinatorial group theory, Journal of Combinatorial Theory, Series A 53(2), 1990, 183 to 208"
    locator: the tiling group of a set of tiles as an invariant that proves tilings impossible
  - paper: doi:10.2307/2324578
    title: William P. Thurston, Conway's tiling groups, The American Mathematical Monthly 97(8), 1990, 757 to 773
    locator: the height functions and the polynomial algorithm for domino tilings of simply connected regions
  - paper: "C. B. Haselgrove and Jenifer Haselgrove, A computer program for pentominoes, Eureka 23, 1960, 16 to 18"
    locator: the 2339 tilings of the 6 by 10 rectangle by the 12 pentominoes
  - book: isbn:9780691024448
    title: Solomon W. Golomb, Polyominoes, Puzzles, Patterns, Problems, and Packings, 2nd edition, Princeton University Press, 1994
    locator: the coloring arguments and the pentomino rectangles
---

The polyomino tiling problem gives a finite region of the square grid and a finite set of polyominoes, shapes made of unit squares joined along their sides, and asks whether the region can be covered by copies of the shapes, turned or flipped as allowed, with no gaps and no overlaps. In puzzles such as the pentomino rectangles each shape is used exactly once. The problem is [NP-complete](/np-complete/), and Moore and Robson (2001) showed that it stays NP-complete for the right tromino alone. On the infinite plane the question is undecidable (Golomb 1970), and for dominoes it is solved in polynomial time by matching.

## In plain words

A polyomino is a shape made of squares stuck together edge to edge, like the pieces of Tetris. You get a board, which is a set of squares, and a box of pieces.

Can you lay the pieces on the board so that every square of the board is covered exactly once? Pieces may be turned over and around, but they may not stick out of the board or overlap.

A computer picks the empty square with the fewest ways to be covered, tries each piece position that covers it, and goes back when it is stuck. To prove that no tiling exists, a clever coloring of the board is often much faster than trying.

## Definition

A *polyomino* is a finite set of cells of $\mathbb{Z}^2$ that is connected through shared sides. Let $G$ be the allowed motions: translations combined with the 4 rotations, with the 4 rotations and 4 reflections, or with no turn at all. An *instance* is a finite region $R \subseteq \mathbb{Z}^2$ and a list of polyominoes $P_1, \ldots, P_k$. A *placement* is a set $g(P_i) \subseteq R$ for a motion $g \in G$. A *tiling* is a set of placements that partitions $R$.

- **Copies.** Each $P_i$ may be used any number of times, or, in the puzzle form, exactly once.
- **Decision.** Is there a tiling? **Counting.** How many?
- **Packing.** Place as many copies as possible without overlap, leaving cells empty.

The region has at most $|R| \cdot 8k$ placements, each found in time polynomial in the size of $R$ and the pieces, so a tiling is a certificate of polynomial size and the problem is in [NP](/np/).

## Variants

- **The whole plane.** Given a finite set of polyominoes, can copies tile the infinite plane? Golomb (1970) showed this equivalent to Wang's domino problem, which Berger proved undecidable in 1966, so it is undecidable too; see [Wang tiling](/wang-tiling-problem/). Ollinger (2009) kept it undecidable for sets of 5 polyominoes.
- **Dominoes.** With the single piece of two cells, a tiling is a [perfect matching](/perfect-matching/) of the grid graph of $R$; see [domino tiling](/domino-tiling-problem/).
- **Pentomino puzzles.** The 12 pentominoes, each once, on a region of 60 cells; their shapes are listed by [polyomino enumeration](/polyomino-enumeration/).
- **Higher dimensions.** Polycubes in boxes, such as the Soma cube.

## Examples

**A pentomino rectangle.** The pentominoes L, P, U and Y tile the $4 \times 5$ rectangle in 4 ways, which are the images of one tiling under the 4 symmetries of the rectangle:

```
L L L L Y
L P U U Y
P P U Y Y
P P U U Y
```

All 12 pentominoes tile the $6 \times 10$ rectangle in 2339 ways up to symmetry, as the Haselgroves found by computer in 1960, and the $3 \times 20$ rectangle in only 2 ways. The exact cover form of these puzzles is on the [exact cover](/exact-cover/) page.

**A coloring proof.** The $6 \times 6$ board has no tiling by the straight tetromino of 4 cells in a line. *Proof.* Color cell $(r, c)$ with $(r + c) \bmod 4$. Every placement of the straight tetromino covers 4 consecutive values of $r + c$, so one cell of each color. A tiling by 9 pieces would cover 9 cells of each color, but the board has 9, 10, 9 and 8 cells of the colors 0, 1, 2 and 3. $\square$

**Right trominoes.** The L-shaped tromino tiles the $2 \times 3$ rectangle in 2 ways and the $3 \times 3$ square in none. *Proof.* A tromino that covers a corner of the square lies in the $2 \times 2$ block at that corner, and that block holds no other corner. So the 4 corners need 4 trominoes, but 9 cells hold only 3. $\square$

## Known algorithms

**Exact cover search.** Make one item for each cell of $R$ and, in the puzzle form, one for each piece; each placement is an option that holds its cells and its piece. A tiling is an exact cover, so [Algorithm X](/algorithm-x/) solves it, with [dancing links](/dancing-links/) for speed. The rule that picks the item with the fewest options usually picks a cell in a tight corner, which is where a hand solver also starts.

```pseudo id=main
TILE(R, pieces)
L1  make an item for every cell of R, and for every piece if each is used once; an option for every placement
L2  if no item is left then record the chosen placements as a tiling; return
L3  pick the item c with the fewest options
L4  if c has no options then return
L5  for each option p that holds c do
L6      choose p: remove its items and every option that shares an item with p
L7      TILE on what is left
L8      undo the choice of p
```

*Correctness.* Every tiling contains exactly one placement that holds $c$, so line L5 tries the placement of each tiling once, and the removal at line L6 leaves exactly the placements that can still join it. So every tiling is found exactly once. The time is exponential in $|R|$ in the worst case.

**Proofs of impossibility.** Coloring arguments, as in the example, count the colors that any placement covers. Conway and Lagarias (1990) made a stronger invariant: the *tiling group*, a group whose words trace the boundaries of the tiles, gives conditions on the boundary of $R$ that every tilable region meets, and proves impossibilities that no coloring finds. Thurston (1990) used it for dominoes on simply connected regions, where a *height function* on the boundary decides tilability in polynomial time.

**SAT.** One variable per placement, an exactly-one constraint per cell, and for the puzzle form an exactly-one constraint per piece. This [SAT](/sat/) encoding is the exact cover written in clauses.

## Bounds

- **NP-completeness.** Tiling a finite region with a given set of polyominoes is NP-complete. Moore and Robson (2001) proved it for the right tromino with the square tetromino, and for the right tromino alone, on the square lattice. In 3 dimensions they proved it for the set of two tiles made of the domino and the straight tromino, in general regions of the cubic lattice. Dominoes alone stay polynomial in any dimension, because a domino tiling is a perfect matching of a bipartite graph.
- **Dominoes in the plane.** Polynomial, by bipartite matching on the grid graph of $R$, and by Thurston's height functions for simply connected regions.
- **The infinite plane.** Undecidable for finite sets of polyominoes (Golomb 1970), and for sets of 5 (Ollinger 2009).
- **Brute force.** Every set of pairwise disjoint placements, at most $2^{8k|R|}$ of them.

## Reductions

- **From planar 1-in-3 satisfiability.** Moore and Robson first show that monotone [1-in-3 satisfiability](/one-in-three-sat/) is NP-complete for planar cubic graphs. Their regions then carry *wires*, corridors whose tilings carry a truth value, and clause gadgets that can be tiled exactly when one of their three wires is true. A tiling exists exactly when the formula has an assignment with exactly one true literal per clause.
- **From Wang tiles (Golomb).** Each Wang tile becomes a polyomino with bumps and dents along its sides, one shape per color, so that two polyominoes fit side by side exactly when the colors of the Wang tiles match.
- **To exact cover and SAT.** As in Known algorithms.

## Applications

- **Puzzles.** Pentomino, polycube and other packing puzzles are designed and checked by exact cover search.
- **Layout.** Cutting stock from a sheet without waste and placing modules on a grid are tiling and packing problems of this kind.

## References
