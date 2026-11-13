---
tag: C2A3S2
kind: problem
slug: knights-tour-problem
name: Knight's tour problem
aliases:
- Knight's tour
- knight's tour
- knight's tour puzzle
area: games-and-search/puzzles
level: intro
summary: Find a sequence of knight moves that visits every square of an m by n board exactly once, open or closed. Schwenk (1991) says which boards have closed tours; tours are built in linear time.
prereqs: [hamiltonian-path-problem]
see_also: [warnsdorff-rule, hamiltonian-cycle-problem, depth-first-search, generic-backtracking-algorithm, bipartite-graph]
sources:
  - paper: doi:10.2307/2690649
    title: Allen J. Schwenk, Which rectangular chessboards have a knight's tour?, Mathematics Magazine 64(5), 1991, 325 to 332
    locator: the main theorem (the boards with a closed tour) and the coloring proofs for the exceptions
  - paper: doi:10.1016/0166-218X(92)00170-Q
    title: Axel Conrad, Tanja Hindrichs, Hussein Morsy and Ingo Wegener, Solution of the knight's Hamiltonian path problem on chessboards, Discrete Applied Mathematics 50(2), 1994, 125 to 134
    locator: the main theorem (the boards with an open tour, also with given end squares) and the linear-time construction
  - paper: doi:10.1016/S0166-218X(96)00010-8
    title: Ian Parberry, An efficient algorithm for the knight's tour problem, Discrete Applied Mathematics 73(3), 1997, 251 to 260
    locator: the divide and conquer construction of closed tours on n by n and n by (n+2) boards for even n at least 6
  - paper: "Brendan D. McKay, Knight's tours of an 8 x 8 chessboard, Technical Report TR-CS-97-03, Department of Computer Science, Australian National University, 1997"
    locator: the count of closed tours on the 8 by 8 board
  - paper: doi:10.37236/1229
    title: Martin Löbbing and Ingo Wegener, The number of knight's tours equals 33,439,123,484,294 (counting with binary decision diagrams), The Electronic Journal of Combinatorics 3(1), 1996, R5
    locator: the BDD method and the count, later found to be wrong
  - paper: "Leonhard Euler, Solution d'une question curieuse qui ne paroit soumise à aucune analyse, Mémoires de l'académie des sciences de Berlin 15 (1759), published 1766, 310 to 337 (Eneström index E309)"
    locator: the method of joining partial paths into a closed tour, and tours with symmetry
  - book: "John J. Watkins, Across the Board: The Mathematics of Chessboard Problems, Princeton University Press, 2004"
    locator: Chapter 2 (Knight's Tours) and Chapter 3 (The Knight's Tour Problem)
  - url: https://oeis.org/A001230
    title: The On-Line Encyclopedia of Integer Sequences, A001230, number of undirected closed knight's tours on a 2n by 2n chessboard
    locator: the terms 9862 for 6 by 6 and 13267364410532 for 8 by 8
---

The knight's tour problem asks for a sequence of knight moves that visits every square of an $m \times n$ board exactly once. A tour is *closed* when the last square is one knight move from the first, and *open* otherwise. In graph terms it is the [Hamiltonian path problem](/hamiltonian-path-problem/) and the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) on the knight's graph, which are NP-complete on general graphs, but on rectangular boards the answer is known exactly: Schwenk (1991) listed the boards with closed tours, Conrad, Hindrichs, Morsy and Wegener (1994) the boards with open tours, and both kinds of tour are built in time linear in the number of squares.

## In plain words

A knight in chess jumps two squares in one direction and one square to the side. Put a knight on a board and try to visit every square once, never landing on a square twice. If the last jump can bring the knight back to its first square, the tour is closed.

On a normal chessboard there are trillions of tours, and people have made them by hand for centuries. On small or thin boards there may be no tour at all, and a short coloring argument often proves this.

To find a tour, a program can try moves and back up when it gets stuck, but that can take very long on big boards. Two better ways exist: a simple rule that picks the square with the fewest onward moves, and a method that glues together ready-made tours of small blocks.

## Definition

Let $B = \{0, \ldots, m-1\} \times \{0, \ldots, n-1\}$. The *knight's graph* $K_{m,n}$ has vertex set $B$ and an edge between $(r, c)$ and $(r', c')$ when $\{|r - r'|, |c - c'|\} = \{1, 2\}$. An *open tour* is a [Hamiltonian path](/hamiltonian-path/) of $K_{m,n}$: a sequence $s_1, \ldots, s_{mn}$ that lists every square once, with $s_i s_{i+1}$ an edge for $1 \le i < mn$. A *closed tour* is a [Hamiltonian cycle](/hamiltonian-cycle/): an open tour in which $s_{mn} s_1$ is also an edge.

- **Existence.** Given $m$ and $n$, is there an open (closed) tour?
- **Construction.** Output one.
- **Counting.** How many tours are there? A closed tour is counted once as an undirected cycle, regardless of its start and direction.

A knight move changes $r + c$ by an odd number, so it always changes the color of the square. So $K_{m,n}$ is a [bipartite graph](/bipartite-graph/), with the black squares ($r + c$ even) on one side.

## Variants

- **Given end squares.** Conrad et al. (1994) also decide, for given squares $s$ and $t$, whether an open tour from $s$ to $t$ exists.
- **Symmetric and magic tours.** Tours that map to themselves under a rotation of the board (Euler 1759 built some), or tours whose step numbers form a magic square.
- **Other boards and pieces.** Cylinders, tori, three-dimensional boards, and leapers that move $(a, b)$ instead of $(1, 2)$.
- **Heuristic search.** [Warnsdorff's rule](/warnsdorff-rule/) builds an open tour one move at a time without backtracking. It is fast and works on most boards tried, but it can fail.

## Examples

**Which boards have tours.** Let $m \le n$.

- *Closed tours* (Schwenk 1991). The board has a closed tour unless (a) $m$ and $n$ are both odd, (b) $m \in \{1, 2, 4\}$, or (c) $m = 3$ and $n \in \{4, 6, 8\}$.
- *Open tours* (Conrad et al. 1994). The board has an open tour unless (a) $m = 1$ and $n > 1$, (b) $m = 2$, (c) $m = 3$ and $n \in \{3, 5, 6\}$, or (d) $m = 4$ and $n = 4$.

So $5 \times 5$ has open tours, 1728 of them as directed paths, but no closed tour; $3 \times 4$ has an open tour but no closed tour; $6 \times 6$ has 9862 closed tours, and $8 \times 8$ has $13\,267\,364\,410\,532$ (McKay 1997, OEIS A001230). Löbbing and Wegener (1996) had published $33\,439\,123\,484\,294$ for $8 \times 8$, which was wrong.

**Odd boards have no closed tour.** The colors alternate along a closed tour, so a closed tour has as many black squares as white squares and an even length. A board with $m$ and $n$ both odd has an odd number of squares. $\square$

**The $4 \times n$ board has no closed tour.** Call the squares of rows 0 and 3 *outer* and those of rows 1 and 2 *inner*. Each knight move from an outer square goes to an inner square, and both sets have $2n$ squares. In a closed tour, each of the $2n$ outer squares is followed by an inner square, which uses all $2n$ inner squares, so outer and inner squares alternate along the cycle. The colors also alternate, so all outer squares have the same color. But row 0 holds squares of both colors when $n \ge 2$. $\square$

**One open tour of $5 \times 5$.** The step number of each square, starting from the top left corner:

```
 1 12 25 18  3
22 17  2 13 24
11  8 23  4 19
16 21  6  9 14
 7 10 15 20  5
```

The last square (25, in row 0, column 2) is not a knight move from the first, as the odd board requires.

## Known algorithms

- **Backtracking.** [Depth-first search](/depth-first-search/) over partial paths, as in the [generic backtracking algorithm](/generic-backtracking-algorithm/). Two cuts make it fast on small boards: try the free square with fewest free neighbors first, and give up when two free squares next to the current square have no other free neighbor, since a path can end in only one of them. In Python it proves non-existence on boards of about 30 squares in a few seconds, but its worst case is exponential.
- **Warnsdorff's rule.** Always move to the square with the fewest onward moves. One tour costs $O(mn)$ time; see [Warnsdorff's rule](/warnsdorff-rule/) for when it fails and how ties are broken.
- **Divide and conquer.** Split the board into blocks whose sizes are in a small table, take a closed tour of each block that uses certain fixed moves near the corners, and delete one such move in each pair of neighboring blocks and add two new moves to join their cycles. Parberry (1997) did this for $n \times n$ and $n \times (n+2)$ boards with $n$ even and $n \ge 6$; Conrad et al. (1994) gave a construction of the same kind for open tours. Both run in $O(mn)$ time, which is optimal since the output has $mn$ squares, and the joins are local, so the blocks can be built in parallel.
- **Counting.** By backtracking for small boards. For $8 \times 8$ the count needs much more care: Löbbing and Wegener (1996) used [binary decision diagrams](/binary-decision-diagram/), and McKay (1997) gave the accepted count with a different computer method.

## Bounds

- **Time.** $\Theta(mn)$ to construct a tour when one exists, since the output has $mn$ squares and the block constructions match this.
- **Existence.** In $O(1)$ time from $m$ and $n$ by the two theorems above.
- **General graphs.** The Hamiltonian path and cycle problems are NP-complete, so no fast general method is known; the knight's graph is easy because of its regular structure.
- **Counts.** The number of closed tours on the $8 \times 8$ board is $13\,267\,364\,410\,532$, so listing all tours is out of reach beyond small boards.

## Reductions

- **To Hamiltonian path and cycle.** A tour is a Hamiltonian path or cycle of $K_{m,n}$, so any Hamiltonian search, such as backtracking with pruning or a [SAT](/sat/) encoding, solves it.
- **Obstructions from colorings.** The proofs of the exceptions in Schwenk's theorem are colorings of the board, like the outer and inner coloring of the $4 \times n$ board, that every cycle must respect.

## Applications

- **Teaching.** The problem is a standard first example of [backtracking](/generic-backtracking-algorithm/) and of a greedy heuristic that is not always right.
- **Puzzles.** Tours appear in chess books and in magic squares, where the step numbers of a tour are the entries of the square.
- **Test cases.** The knight's graph is a sparse graph with a known answer for every size, so it is a convenient test for Hamiltonian path solvers.

## References
