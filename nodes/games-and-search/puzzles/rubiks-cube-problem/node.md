---
tag: CVDGSV
kind: problem
slug: rubiks-cube-problem
name: Rubik's Cube problem
aliases:
- Rubik's Cube solving
- Rubik's cube
area: games-and-search/puzzles
level: intro
summary: "Find face turns that return a scrambled Rubik's Cube to its solved state; there are about 4.3 x 10^19 positions, and 20 turns always suffice."
prereqs: [symmetric-group, state-space]
see_also: [gods-number, kociemba-algorithm, sliding-tile-puzzle, macro-operators, permutation-parity, pattern-database, iterative-deepening-a-star, bidirectional-search]
sources:
  - paper: "Richard E. Korf, Finding optimal solutions to Rubik's Cube using pattern databases, Proceedings of the 14th National Conference on Artificial Intelligence (AAAI-97), 1997"
    locator: "pp. 700-705; IDA* with pattern databases finds shortest solutions of random positions, with median length 18"
  - paper: doi:10.1137/140973499
    title: "Tomas Rokicki, Herbert Kociemba, Morley Davidson and John Dethridge, The diameter of the Rubik's Cube group is twenty, SIAM Review 56(4), 2014"
    locator: "pp. 645-670; every position can be solved in at most 20 face turns"
  - paper: doi:10.1007/978-3-642-23719-5_58
    title: "Erik D. Demaine, Martin L. Demaine, Sarah Eisenstat, Anna Lubiw and Andrew Winslow, Algorithms for solving Rubik's Cubes, ESA 2011, LNCS 6942"
    locator: "pp. 689-700; the n by n by n cube has diameter Θ(n^2 / log n), with an algorithm that reaches it"
  - paper: doi:10.4230/LIPIcs.STACS.2018.24
    title: "Erik D. Demaine, Sarah Eisenstat and Mikhail Rudoy, Solving the Rubik's Cube optimally is NP-complete, STACS 2018, LIPIcs 96"
    locator: "24:1-24:13; a shortest solution of the n by n by n cube is NP-complete to find, by a reduction from Hamiltonian cycle in grid graphs"
  - url: "https://www.cube20.org/"
    locator: "the table of bounds on the number of moves since 1981, including Thistlethwaite's 52"
---

The Rubik's Cube problem asks for a sequence of face turns that takes a scrambled Rubik's Cube back to the solved state, and in its hard form for a shortest such sequence. The positions form a group of 43,252,003,274,489,856,000 elements, far too many to search one by one, but group structure and heuristic search make the problem easy in practice. Every position can be solved in 20 face turns, which is [God's number](/gods-number/), and [Kociemba's two-phase algorithm](/kociemba-algorithm/) finds solutions of about that length in seconds.

## In plain words

The cube has six faces of nine stickers, and each face can turn. A scramble is any mix of turns. To solve the cube you must find turns that bring every face back to one colour. The cube is made of small pieces: corners with three stickers and edges with two. A turn moves four corners and four edges around a face. Some changes can never happen, such as turning one corner in its place, so only one in twelve ways to put the pieces in the frame can be reached. People solve the cube with fixed recipes that fix a few pieces at a time and leave the rest unchanged. Computers use search: they guess a lower bound on the moves still needed and cut off any path that is too long.

## Definition

The cube has 8 corner pieces, 12 edge pieces and 6 centres. The centres never move relative to each other, so a position is given by:

| Part | Values | Meaning |
|---|---|---|
| corner permutation $c_p$ | a permutation of the 8 corner places | which corner is in each place |
| corner twists $c_o$ | $\{0, 1, 2\}^8$ | how each corner is rotated in its place |
| edge permutation $e_p$ | a permutation of the 12 edge places | which edge is in each place |
| edge flips $e_o$ | $\{0, 1\}^{12}$ | whether each edge is flipped in its place |

There are $8!\, 3^8\, 12!\, 2^{12}$ such assemblies. A move turns one face. In the half turn metric (HTM) there are 18 moves: each face U, D, R, L, F, B by a quarter turn clockwise (U), counterclockwise (U′) or a half turn (U2). In the quarter turn metric (QTM) there are the 12 quarter turns. A move is a fixed assembly, and doing move $m$ after position $x$ gives the product $x \cdot m$:

$$(x \cdot m)_p(i) = x_p(m_p(i)), \qquad (x \cdot m)_o(i) = x_o(m_p(i)) + m_o(i)$$

for corners and edges, with the twists modulo 3 and the flips modulo 2.

**Problem.** Given a position $x$ reached from the solved position $e$, find moves $m_1, \dots, m_k$ with $x \cdot m_1 \cdots m_k = e$. In the optimization version $k$ must be as small as possible.

**Reachable positions.** A quarter turn moves 4 corners and 4 edges in 4-cycles, which are odd permutations, and its twists add to 0 modulo 3 and its flips to 0 modulo 2. So every reachable position has:

1. total twist $\sum c_o \equiv 0 \pmod 3$,
2. total flip $\sum e_o \equiv 0 \pmod 2$,
3. the [parity](/permutation-parity/) of $c_p$ equal to the parity of $e_p$.

These are the only obstructions. Short sequences such as commutators $a\,b\,a^{-1} b^{-1}$ give a 3-cycle of corners, a 3-cycle of edges, a twist of two corners in opposite directions and a flip of two edges. With a quarter turn to fix the parity, these place and orient every piece but the last corner and the last edge, and the three conditions force those two to be right. The conditions cut the assemblies by $3 \cdot 2 \cdot 2 = 12$, so the cube group has

$$|G| = \frac{8!\, 3^8\, 12!\, 2^{12}}{12} = 43{,}252{,}003{,}274{,}489{,}856{,}000$$

elements, a [subgroup](/subgroup/) of the [symmetric group](/symmetric-group/) on the 48 moving stickers.

## Variants

- **Metric.** The answer depends on what counts as one move. In HTM God's number is 20, and in QTM it is 26.
- **Shortest or any solution.** Finding some solution is easy; finding a shortest one is the hard version and the subject of most of the algorithms below.
- **Other sizes.** The $2 \times 2 \times 2$ cube has only corners and 3,674,160 positions, few enough for a full [breadth-first search](/breadth-first-search/); its diameter is 11 in HTM and 14 in QTM. For the $n \times n \times n$ cube the diameter is $\Theta(n^2 / \log n)$.
- **Supercube.** If the centres carry pictures, their rotation matters too, and the number of positions grows.
- **Fewest moves of a fixed kind.** Human methods and some programs restrict the moves, for example to $\langle U, D, R2, L2, F2, B2 \rangle$ in the second phase of Kociemba's algorithm.

## Examples

**Distances near the solved cube.** A breadth-first search gives the number of positions at each distance:

| Distance | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| HTM | 1 | 18 | 243 | 3,240 | 43,239 |
| QTM | 1 | 12 | 114 | 1,068 | 10,011 |

At distance 2 in HTM, $18 \cdot 15 = 270$ sequences avoid two turns of the same face, but U D and D U give the same position for each of the $3 \cdot 9 = 27$ pairs of opposite faces, which leaves 243.

**Orders of moves.** Repeating R U returns to the solved cube after 105 times, and repeating R U R′ U′ after 6 times.

**Superflip.** The position with every piece in its place and every edge flipped commutes with every move. It needs 20 face turns, so it is among the hardest positions.

**Solving short scrambles.** For a scramble of at most 8 moves, two breadth-first searches of radius 4, one from the solved cube and one from the scramble, give its exact distance where they meet, a [bidirectional search](/bidirectional-search/). For R U R′ U′ F2 D L′ B the meeting gives distance 8. Kociemba's algorithm finds a 20-move solution of the same position at once, and finds the 8-move solution B′ L D′ F2 U R U′ R′ when it runs to the end.

**Unreachable assembly.** Take the cube apart and put one corner back twisted. The total twist is then 1 modulo 3, so no sequence of moves can solve it.

## Known algorithms

- **Layer by layer.** Human methods fix the pieces of the top layer, then the middle and then the bottom, with memorized sequences that move a few pieces and keep all others in place. Such sequences are [macro-operators](/macro-operators/): each one is found once, by search or by hand, and reused. The solutions are easy to find and much longer than the shortest ones.
- **Group membership.** Viewing $G$ as a permutation group on the stickers, the Schreier-Sims algorithm computes a chain of stabilizer subgroups and writes any position as a product of the generators. It runs in time polynomial in the number of stickers, but the words it produces are long.
- **Thistlethwaite's algorithm (1981).** Four phases through the chain $G \supset \langle U, D, R, L, F2, B2 \rangle \supset \langle U, D, R2, L2, F2, B2 \rangle \supset \langle U2, D2, R2, L2, F2, B2 \rangle \supset \{e\}$, each solved by table lookup. At most 52 moves.
- **[Kociemba's two-phase algorithm](/kociemba-algorithm/) (1992).** Two phases through $\langle U, D, R2, L2, F2, B2 \rangle$, each by [IDA\*](/iterative-deepening-a-star/) with exact tables for parts of the position. The first solution has at most 30 moves; Reid showed in 1995 that 29 suffice. Run to the end it gives a shortest solution.
- **Korf's optimal solver (1997).** IDA* with [pattern databases](/pattern-database/): exact distances for the corners alone and for two halves of the edges, combined by taking the maximum. It found shortest solutions of random positions, with median length 18.
- **Exhaustive search over cosets.** To find the largest distance, Rokicki, Kociemba, Davidson and Dethridge solved all cosets of $\langle U, D, R2, L2, F2, B2 \rangle$ at once; see [God's number](/gods-number/).
- **Large cubes.** Demaine et al. (2011) solve the $n \times n \times n$ cube in $O(n^2 / \log n)$ moves by moving many pieces at the same time with one sequence, which matches the lower bound.

## Bounds

- **Exact diameter.** 20 in HTM (2010) and 26 in QTM (2014).
- **Lower bound by counting.** There are fewer than $|G|$ sequences of at most 17 moves that avoid useless pairs, so some position needs 18 moves in HTM, without any search.
- **First solutions.** Kociemba's algorithm gives at most 29 moves in the worst case. In the Python implementation of its page, the first solutions of random positions had 21 to 25 moves.
- **Complexity.** For the $n \times n \times n$ cube, deciding whether a position can be solved in $k$ moves is [NP-complete](/np-complete/) (Demaine, Eisenstat and Rudoy 2018), while a solution of $O(n^2 / \log n)$ moves, within a constant factor of the worst case, can be found in polynomial time (Demaine et al. 2011).

## Reductions

- **To a shortest path in a Cayley graph.** The positions are the vertices, and each move is an edge. Optimal solving is a single-pair shortest path in this [implicit graph](/implicit-graph/), so [breadth-first search](/breadth-first-search/), bidirectional search and IDA* apply. The same holds for the [sliding tile puzzle](/sliding-tile-puzzle/) and the [burnt pancake problem](/burnt-pancake-problem/).
- **To coordinates.** Parts of the position, such as the twists alone or the permutation of the corners alone, change under each move independently of the rest. A [rank](/permutation-rank-unrank/) of each part, for example the [Lehmer code](/lehmer-code/) of the corner permutation, gives an array index, and move tables and distance tables are arrays indexed by ranks.
- **From Hamiltonian cycle.** The NP-completeness proof for the $n \times n \times n$ cube reduces from [Hamiltonian cycle](/hamiltonian-cycle-problem/) in grid graphs.

## Applications

- **Benchmark for heuristic search.** The cube was a main test case for pattern databases and for disk-based and parallel breadth-first search.
- **Teaching group theory.** Commutators, conjugates, [permutation cycles](/permutation-cycles/), parity and cosets all have visible meanings on the cube.
- **Computation at scale.** The proof of God's number split $G$ into cosets, used symmetry to skip most of them, and ran on many machines; the same plan fits other exhaustive searches over large groups.

## References
