---
tag: 9JN0A4
kind: problem
slug: jigsaw-puzzle-problem
name: Jigsaw puzzle problem
aliases:
- Jigsaw puzzle assembly
area: games-and-search/puzzles
level: advanced
summary: Place square pieces with tabs and blanks in a rectangle so that all touching edges fit. Easy when each tab fits one blank; NP-complete when matches are ambiguous, even for 1 by n.
prereqs: [np-complete, generic-backtracking-algorithm]
see_also: [polyomino-tiling-problem, exact-cover, gadget-reduction, hash-table, hamiltonian-path-problem, traveling-salesman-problem, minimum-spanning-tree]
sources:
  - paper: doi:10.1007/s00373-007-0713-4
    title: Erik D. Demaine and Martin L. Demaine, Jigsaw puzzles, edge matching, and polyomino packing, connections and complexity, Graphs and Combinatorics 23(Suppl. 1), 2007, 195 to 208
    locator: the whole paper (the three problems, the reductions between them, and their NP-completeness)
  - paper: doi:10.2197/ipsjjip.25.682
    title: Jeffrey Bosboom, Erik D. Demaine, Martin L. Demaine, Adam Hesterberg, Pasin Manurangsi and Anak Yodpinyanee, Even 1 x n edge matching and jigsaw puzzles are really hard, Journal of Information Processing 25, 2017, 682 to 694
    locator: the whole paper (NP-hardness for 1 by n puzzles with rotation, hardness of approximation for the most pieces placed, and a 1/2-approximation)
  - paper: "Herbert Freeman and L. Garder, Apictorial jigsaw puzzles, the computer solution of a problem in pattern recognition, IEEE Transactions on Electronic Computers EC-13(2), 1964, 118 to 127"
    locator: the whole paper (assembly of pieces from their outlines alone)
---

The jigsaw puzzle problem gives $N$ pieces, each a unit square whose four sides are flat, a tab or a blank, with a shape for each tab and blank. Decide whether the pieces fill an $m \times n$ rectangle with flat sides on the border, so that every pair of touching sides is a tab and a blank of the same shape. If every tab shape fits exactly one blank, the pieces can be assembled in linear time, one neighbor at a time. When shapes repeat, so that matches are ambiguous, the problem is [NP-complete](/np-complete/) (Demaine and Demaine 2007), even for a $1 \times n$ strip of pieces that may be rotated (Bosboom et al. 2017). The same holds for edge-matching puzzles, where sides carry colors that must be equal, and the two are tied by reductions to [polyomino packing](/polyomino-tiling-problem/).

## In plain words

A jigsaw puzzle is a box of pieces that fit together into a picture. Here we ignore the picture and only look at the shapes of the edges. Each edge is flat, or sticks out, or goes in, and an edge that sticks out must meet one that goes in with the same shape.

If every edge shape is different, the puzzle is easy: start in a corner, and for each place there is only one piece that fits next to the pieces already placed.

If many edges have the same shape, a piece may seem to fit in many places, and a choice that looks right can block the puzzle much later. Then no fast method is known.

## Definition

A *piece* is a 4-tuple $(t, r, b, l)$ of side labels in $\mathbb{Z}$: top, right, bottom and left. Label 0 is a flat side; a label $x \ne 0$ is a tab of shape $|x|$ if $x > 0$ and a blank of shape $|x|$ if $x < 0$. Two sides *fit* when their labels are $x$ and $-x$ with $x \ne 0$.

A *solution* is a bijection from the pieces to the cells of an $m \times n$ grid, such that:

- a side on the border of the rectangle has label 0, and every inner side does not;
- each horizontal neighbor pair has fitting right and left sides, and each vertical pair has fitting bottom and top sides.

In the version with *rotation*, each piece may also be turned by a multiple of 90 degrees. The *decision problem* asks whether a solution exists.

An *edge-matching puzzle* is the same, except that two sides fit when their labels are equal. This is the *unsigned* version; the jigsaw rule is the *signed* version.

## Variants

- **Unique matches.** Every nonzero label $x$ occurs on exactly one side, and so does $-x$. Then the solution, if it exists, is unique, and it is found greedily.
- **Ambiguous matches.** Labels repeat. This is the NP-complete case.
- **Edge matching.** Colors instead of tabs and blanks. Commercial puzzles such as Eternity II, with 256 pieces on a $16 \times 16$ board, are of this kind.
- **Strips.** The $1 \times n$ case with rotation is still NP-complete, and it is NP-hard to approximate the most pieces that can be placed within some constant factor less than 1. A simple method places half the pieces (Bosboom et al. 2017).
- **Pictorial puzzles.** The pieces carry parts of an image, and the fit of two sides is scored by how well the colors along them agree. The task is then an optimization problem, studied in computer vision.
- **Apictorial puzzles.** Real pieces with curved outlines, matched by their shapes alone (Freeman and Garder 1964).

## Examples

**Unique matches.** Take the $2 \times 2$ puzzle with pieces

| piece | top | right | bottom | left |
|---|---|---|---|---|
| A | 0 | 1 | 2 | 0 |
| B | 0 | 0 | -3 | -1 |
| C | -2 | 4 | 0 | 0 |
| D | 3 | 0 | 0 | -4 |

Only A has flat top and left sides, so A goes in the top-left corner. Its right side 1 fits the left side $-1$ of B only, and its bottom side 2 fits the top side $-2$ of C only. Then D must take the last cell, and its sides $3$ and $-4$ fit B and C. The assembly is unique, and each step is one table lookup.

**Ambiguous matches.** If the same tab shape is used on every inner side, the border still fixes where the corner and side pieces go up to their order along each side. But inside, many pieces fit the same pair of neighbors. A search must try them and back up when it reaches a cell where no piece fits, and the number of complete assemblies can be large.

## Known algorithms

- **Greedy assembly with a table.** For unique matches, put all pieces in a [hash table](/hash-table/) keyed by their left side and by their top side. Place the corner, then fill the grid in row order by looking up the only piece that fits the neighbor to the left, or above for the first column. This takes $O(N)$ expected time.
- **Backtracking.** Fill the cells in row order and try each unused piece that fits the neighbors already placed, undoing a choice when no piece fits a cell. This is [backtracking](/generic-backtracking-algorithm/) with exponential worst case, and it can count all solutions.
- **Exact cover.** Fixed orientations or rotations give a set of candidate placements. Cells and pieces are the items to be covered, with extra constraints for the sides, so solvers for [exact cover](/exact-cover/) and SAT apply.
- **Pictorial assembly.** For image pieces, score each pair of sides, then grow the assembly greedily from the most confident pairs, or join pieces along a [minimum spanning tree](/minimum-spanning-tree/) of the pair costs. This is a heuristic; finding the best scoring assembly is NP-hard, as it contains the decision problem above.

## Bounds

- **Unique matches.** $O(N)$ expected time by the greedy method.
- **NP-complete.** Jigsaw puzzles and edge-matching puzzles with ambiguous matches, in the $m \times n$ case (Demaine and Demaine 2007). Membership in NP holds since a placement can be checked in $O(N)$ time.
- **$1 \times n$ with rotation.** NP-complete, and NP-hard to approximate the most pieces placed within a constant factor just below 1, while an easy method places at least half the best number (Bosboom et al. 2017).

## Reductions

- **Between the puzzles.** Demaine and Demaine (2007) reduce signed jigsaw puzzles, unsigned edge matching and polyomino packing to each other. A side label becomes a pattern of bumps and notches on a larger polyomino, and a polyomino is cut into unit pieces with labels that force its cells to stay together. These are [gadget reductions](/gadget-reduction/), so the hardness of one puzzle carries over to the others.
- **To path problems.** A $1 \times n$ strip with fixed orientation is a path through all pieces, with an edge from piece $p$ to piece $q$ when the right side of $p$ fits the left side of $q$. This is a [Hamiltonian path](/hamiltonian-path-problem/) problem on a special graph. With fit scores instead of fit or no fit, ordering strips of a shredded page is a [traveling salesman problem](/traveling-salesman-problem/).

## Applications

- **Reconstruction of broken objects.** Joining fragments of pottery, frescoes or bone by the shapes of their breaks is an apictorial puzzle.
- **Document reconstruction.** Shredded paper strips are a $1 \times n$ puzzle with fit scores from the text and the ink along the cuts.
- **Image processing.** Rebuilding an image from shuffled square tiles is a test problem for methods that measure how well two edges of an image continue each other.
- **Hard instances.** Edge-matching puzzles give compact, hard test cases for SAT and constraint solvers.

## References
