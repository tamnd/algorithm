---
tag: 42Y3XQ
kind: algorithm
slug: kociemba-algorithm
name: Kociemba's two-phase algorithm
aliases:
- Two-phase algorithm
area: games-and-search/puzzles
level: advanced
summary: "Solve the Rubik's Cube in two searches: reach the subgroup <U, D, R2, L2, F2, B2>, then solve inside it. First solutions have at most 30 moves; run to the end it finds a shortest one."
solves: [rubiks-cube-problem]
model: word-ram
complexity:
  vars: {a: the number of phase-1 moves, b: the number of phase-2 moves, t: the number of table entries}
  time: {worst: O(t + 18^a + 10^b)}
  space: {extra: O(t + a + b)}
properties: {deterministic: true, recursive: true, anytime: true}
history:
  year: 1992
  people: [Herbert Kociemba]
  note: Kociemba published the algorithm in Cubism For Fun in 1992, joining the four phases of Thistlethwaite's 1981 method into two; Reid showed in 1995 that every position can be solved in at most 29 moves.
prereqs: [rubiks-cube-problem, iterative-deepening-a-star, subgroup]
see_also: [gods-number, pattern-database, admissible-heuristic, iterative-deepening-a-star, breadth-first-search, permutation-rank-unrank, macro-operators, bidirectional-search]
sources:
  - paper: "Herbert Kociemba, Close to God's algorithm, Cubism For Fun 28, April 1992"
    locator: "pp. 10-13; cited as reference 1 of Rokicki 2008 and by Rokicki et al. 2014, the article itself was not checked"
  - paper: "Tomas Rokicki, Twenty-five moves suffice for Rubik's Cube, arXiv:0803.3435, 2008"
    locator: "pp. 3-5: the subgroup H, Reid's bounds of 12 moves into H and 18 moves inside it, Table 1 with the distances inside H, and Algorithm 1, the search run to the end"
  - paper: "Michael Reid, New upper bounds, cube-lovers e-mail, January 7, 1995"
    locator: "cited as reference 6 of Rokicki 2008 for the bound of 29 moves; the message itself was not checked"
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: "Richard E. Korf, Depth-first iterative-deepening: an optimal admissible tree search, Artificial Intelligence 27(1), 1985"
    locator: "pp. 97-109, IDA*, the search used in both phases"
  - paper: doi:10.1137/140973499
    title: "Tomas Rokicki, Herbert Kociemba, Morley Davidson and John Dethridge, The diameter of the Rubik's Cube group is twenty, SIAM Review 56(4), 2014"
    locator: "pp. 645-670; the set solver built on the two phases, which proved that 20 moves suffice"
---

Kociemba's two-phase algorithm solves the [Rubik's Cube](/rubiks-cube-problem/) by splitting the problem at the subgroup $G_1 = \langle U, D, R2, L2, F2, B2 \rangle$. Phase 1 brings the cube into $G_1$ with any moves, and phase 2 solves it with only the ten moves of $G_1$; each phase is an [IDA\*](/iterative-deepening-a-star/) search guided by small exact tables. The first solution comes in well under a second in a compiled program and has at most 30 moves, and if the search goes on through longer phase-1 sequences it finds a shortest solution.

## In plain words

Solving the cube in one search is too slow, because the number of positions is huge. The trick is to stop halfway. There is a large family of positions in which every corner and edge sits the right way round and the four middle edges sit in the middle layer. From there, the cube can be finished with only half turns of four faces and any turns of the top and bottom. Reaching that family takes at most 12 moves, and finishing takes at most 18. Each half is small enough to have tables that tell, for any position, a lower bound on the moves left, so the search cuts off every branch that is too long. After the first answer, the algorithm tries longer first halves, because a longer first half can make the second half much shorter.

## The problem

The input is a position $c$ of the cube group $G$, given by corner and edge permutations, twists and flips as on the [problem page](/rubiks-cube-problem/), and a length bound $M$. The 18 moves $S$ are the quarter and half turns of the six faces (the half turn metric). The output is a sequence of moves of $S$ that takes $c$ to the solved cube $e$, of at most $M$ moves. In the first mode the output is any such sequence; in the second it must be as short as possible.

## The algorithm

Let $A = \{U, U2, U', D, D2, D', R2, L2, F2, B2\}$. The group $G_1 = \langle A \rangle$ is the set of positions with every twist 0, every flip 0, and the four middle-slice edges FR, FL, BL, BR in the middle slice. It has

$$|G_1| = \frac{8!\; 8!\; 4!}{2} = 19{,}508{,}428{,}800$$

elements, and $G$ splits into $|G| / |G_1| = 3^7 \cdot 2^{11} \cdot \binom{12}{4} = 2{,}217{,}093{,}120$ cosets of it.

**Coordinates.** Each phase sees the cube through three small numbers that a move changes independently of the rest of the cube:

| Phase | Coordinate | Values | Solved value |
|---|---|---|---|
| 1 | twist: the twists of 7 corners in base 3 | 2,187 | 0 |
| 1 | flip: the flips of 11 edges in base 2 | 2,048 | 0 |
| 1 | slice: which 4 of the 12 edge places hold the slice edges | 495 | one value |
| 2 | corner permutation, by [rank](/permutation-rank-unrank/) | 40,320 | 0 |
| 2 | permutation of the 8 edges of the U and D layers | 40,320 | 0 |
| 2 | permutation of the 4 slice edges | 24 | 0 |

A cube is in $G_1$ exactly when the phase-1 coordinates have their solved values. A *move table* gives the next value of a coordinate for each value and move. A *pruning table* gives, for each pair of coordinates, the exact distance of the pair to the solved pair, found by [breadth-first search](/breadth-first-search/) over the pairs. The algorithm uses the pairs (slice, twist) and (slice, flip) in phase 1 and (corners, slice edges) and (layer edges, slice edges) in phase 2:

$$h_1(x) = \max(P_{\text{st}}(x), P_{\text{sf}}(x)), \qquad h_2(x) = \max(P_{\text{cs}}(x), P_{\text{es}}(x)).$$

Both are lower bounds on the moves still needed, so both are [admissible heuristics](/admissible-heuristic/).

A sequence is *canonical* if no two neighbouring moves turn the same face, and two neighbouring moves on opposite faces are in the fixed order U before D, R before L, F before B. Both searches list only canonical sequences.

```pseudo id=main
KOCIEMBA(c, M, first)      ▷ c: a position; M: the length bound; first: stop at the first solution
L1  build the move tables and the pruning tables for h1 and h2
L2  best ← none
L3  for d ← 0 to M do
L4      if best ≠ none and d ≥ |best| then return best
L5      for each canonical p with |p| = d, c·p ∈ G1, and p empty or its last move not in A, by depth-first search cut where h1 > moves left do
L6          c′ ← c·p
L7          ℓ ← (|best| − 1 if best ≠ none else M) − d
L8          q ← a shortest canonical sequence of moves of A with |q| ≤ ℓ and c′·q = e, by IDA* with h2, or none
L9          if q ≠ none then best ← p q; if first then return best
L10 return best
```

L5 is one iteration of IDA* for phase 1 with bound $d$; it lists every phase-1 sequence of exactly $d$ moves. It skips sequences whose last move is in $A$, because the same sequence without that move also ends in $G_1$ and has already been listed at a smaller $d$. L7 asks phase 2 only for solutions that beat the best one found.

## Example

Take the position $c$ reached from $e$ by R U R′ U′ F2 D L′ B, and $M = 30$. Its phase-1 coordinates are twist 321, flip 137 and slice 95, and $h_1(c) = 5$, so L5 lists nothing for $d \le 4$ (each search is cut at the root) and nothing for $d = 5, 6$ either.

| $d$ | Phase-1 sequences | $p$ | $q$ | Length |
|---|---|---|---|---|
| 7 | 2 | B′ L′ U′ R2 L U′ L | U R2 L2 U L2 U R2 U R2 U2 D′ F2 U2 | 20 |
| 7 | | B′ L′ U′ R2 L U′ L′ | U R2 L2 D′ L2 U L2 D′ B2 D F2 B2 | 19 |
| 8 | 22 | B′ L D′ F2 U R U′ R | R2 | 9 |
| 8 | | B′ L D′ F2 U R U′ R′ | (empty) | 8 |
| 9 | | | | stop at L4 |

In the first mode the algorithm returns the 20-move solution of the first row. Run to the end, it improves the solution three times and stops at $d = 9 \ge 8$ with B′ L D′ F2 U R U′ R′, the inverse of the scramble. This is a shortest solution: a [bidirectional search](/bidirectional-search/) with two balls of radius 4 also finds distance 8. The two phase-1 sequences of length 7 differ only in the last quarter turn, L or L′. Such pairs always occur: L′ = L · L2 and L2 is in $A$, so if $c \cdot u\,L$ is in $G_1$, so is $c \cdot u\,L'$.

## Correctness

The full proofs are in the proof file; here is the outline.

- **The tables are exact on coordinates.** Each coordinate of $x \cdot m$ depends only on that coordinate of $x$ and on $m$, so a sequence of $k$ moves on the cube is a path of $k$ steps between coordinate pairs. Hence $h_1$ and $h_2$ never overestimate.
- **Phase 1 is complete.** L5 cuts a branch only when $h_1$ exceeds the moves left, so it lists every canonical sequence of length $d$ into $G_1$ that does not end in $A$.
- **Phase 2 is shortest.** IDA* with an admissible bound returns a shortest solution within the limit, or none.
- **Validity.** Every value of best takes $c$ to $e$ and has at most $M$ moves.
- **First solution.** Every position is at most 12 moves from $G_1$, and every position of $G_1$ is at most 18 moves of $A$ from $e$ (Reid; Rokicki's Table 1 lists the distances inside $G_1$). So with $M \ge 30$, phase 2 succeeds for the first phase-1 sequence found.
- **Optimality when run to the end.** Take a shortest solution, written canonically, and split it after its last move that is not in $A$. The first part $p$ ends in $G_1$ and is listed at $d = |p|$, and the second part is a solution of $c \cdot p$ with moves of $A$, so phase 2 returns one at least as short. The search reaches $d = |p|$, because L4 stops only when $d$ reaches the length of a solution.
- **Termination.** $d$ runs to at most $M$, and both searches are finite.

## Complexity

**Tables.** The move tables have $2187 + 2048 + 495$ rows of 18 entries and $40320 + 40320 + 24$ rows of 10 entries. The pruning tables have

$$495 \cdot 2187 + 495 \cdot 2048 + 2 \cdot 40320 \cdot 24 = 4{,}031{,}685$$

entries of one byte, all reachable. Their largest values are 9 and 9 in phase 1 and 14 and 12 in phase 2, below the true maxima of 12 and 18. Building them is a breadth-first search over each pair, $O(t)$ time with 18 moves per entry; the Python implementation needs about one and a half minutes.

**Search.** In the first mode, phase 1 visits at most $\sum_{d \le a} 18^d = O(18^a)$ prefixes and one call of phase 2 visits at most $O(10^b)$, with $a \le 12$ and $b \le 18$. Canonical sequences grow by a factor of about 13.35 per move in phase 1, not 18, and the tables cut most branches near the root, so the real counts are many orders of magnitude smaller. In the Python implementation, first solutions of random positions take a few seconds and have 21 to 25 moves.

**Run to the end.** The time grows with the length $L$ of a shortest solution, because phase 1 must reach $d$ close to $L$ and phase 2 is called for every phase-1 sequence. For a 13-move scramble (F R U′ L B2 D′ R2 F′ U B L2 D R′) the Python implementation found a 25-move first solution, $10 + 15$, and needed about 8 minutes to reach and prove a 13-move optimum.

**Space.** The tables take $O(t)$ bytes, about 4 MB here, and the two recursion stacks hold $a + b$ moves.

## Properties

- **Anytime.** It reports better and better solutions, and each one is valid, so it can stop at any time or at a target length.
- **Not optimal in the first mode.** The shortest phase-1 sequence can lead to a long phase 2; in the example, a 7-move phase 1 gives 20 moves in total, and an 8-move phase 1 gives 8.
- **Deterministic.** The order of the moves fixes which solution is found first.
- **Small memory.** The tables are a few megabytes, far less than a table of all $|G|$ positions or of all $|G_1|$ positions.

## Variants and improvements

- **Larger tables.** The full phase-1 distance table over the 2,217,093,120 cosets fits in memory with the 16 symmetries of the cube that keep the U-D axis and two bits per entry (Rokicki 2008), which gives exact $h_1$.
- **Three axes and inverse.** The same position can be split at the subgroup for the U-D, R-L or F-B axis, and its inverse can be solved instead. Searching the six variants at the same time finds short solutions faster (Rokicki 2008).
- **Set solver.** For a whole coset of $G_1$ at once, a bitmap of $|G_1|$ bits replaces the per-position phase 2. This solver proved that 20 moves always suffice; see [God's number](/gods-number/).
- **Thistlethwaite's algorithm.** The 1981 method that Kociemba's refines: four phases through a chain of subgroups, with at most 52 moves, each phase short enough for complete tables.
- **Optimal solvers.** Korf's solver (1997) runs a single IDA* over $G$ with [pattern databases](/pattern-database/) for the corners and for two sets of edges. It always returns a shortest solution but is much slower than the first mode here.

## When to use it

Use it to solve the 3 by 3 by 3 cube fast with a short solution: the first mode for near-optimal answers in a fraction of a second in a compiled program, and the run to the end when a shortest solution is wanted and some minutes are acceptable. For a fixed set of hand-learned moves, use [macro-operators](/macro-operators/) instead. The subgroup and the tables are built for the 3 by 3 by 3 cube; another puzzle needs its own subgroup, coordinates and tables.

## Pitfalls

- **Coordinates that are not well defined.** A coordinate must change under a move independently of the rest of the cube; otherwise a move table built from one representative per value is wrong. Twist, flip and slice positions have this property for all moves; the three permutations of phase 2 have it only for the moves of $A$.
- **Phase-1 sequences that end in $A$.** Without the test in L5, every phase-1 sequence of length $d$ comes back at length $d + 1$ with a move of $A$ added, and the search repeats work.
- **Taking the first phase-1 hit.** Stopping at the first $G_1$ position and returning the sum gives up to 30 moves, and 21 to 25 on random positions in the tests; shorter solutions come from trying many phase-1 sequences.
- **A loose limit in L7.** If phase 2 is not bounded by the best length found, it spends most of its time on solutions that cannot improve the result.
- **Mixing metrics.** The bounds 12, 18 and 29 are for the half turn metric; in the quarter turn metric the moves of $A$ and the bounds are different.

## Implementations

## History

Thistlethwaite gave a four-phase method with at most 52 moves in 1981. Herbert Kociemba joined its phases into two and published the result in Cubism For Fun in 1992, with IDA* as the search in each phase. Reid showed that the two phases need at most 12 and 18 moves, and in January 1995 that every position can be solved in at most 29. Kociemba's Windows program Cube Explorer implements the algorithm. Rokicki (2008) turned phase 2 into a solver for whole cosets, and Rokicki, Kociemba, Davidson and Dethridge used it in 2010 to prove that every position can be solved in 20 moves.

## References
