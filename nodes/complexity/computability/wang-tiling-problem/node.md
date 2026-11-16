---
tag: K2W6QP
kind: problem
slug: wang-tiling-problem
name: Wang tiling problem
aliases:
- domino problem
- tiling problem
area: complexity/computability
level: advanced
summary: Given a finite set of square tiles with colored edges, decide whether copies of them can cover the whole plane with matching edges. Berger proved in 1966 that this is undecidable.
prereqs: [halting-problem, turing-machine, many-one-reducibility]
see_also: [halting-problem, undecidability, turing-completeness, entscheidungsproblem, church-theorem, cellular-automaton, domino-tiling-problem, polyomino-tiling-problem]
sources:
  - title: Hao Wang, Proving theorems by pattern recognition II, Bell System Technical Journal 40(1) (1961)
    locator: pp. 1 to 41 (the dominoes and the conjecture that every set that tiles the plane tiles it periodically)
  - paper: doi:10.1073/pnas.48.3.365
    title: A. S. Kahr, Edward F. Moore and Hao Wang, Entscheidungsproblem reduced to the AEA case, Proceedings of the National Academy of Sciences 48(3) (1962)
    locator: pp. 365 to 377 (the origin-constrained domino problem is undecidable)
  - paper: doi:10.1090/memo/0066
    title: Robert Berger, The undecidability of the domino problem, Memoirs of the American Mathematical Society 66 (1966)
  - paper: doi:10.1007/BF01418780
    title: Raphael M. Robinson, Undecidability and nonperiodicity for tilings of the plane, Inventiones Mathematicae 12 (1971)
    locator: pp. 177 to 209
  - paper: doi:10.19086/aic.18614
    title: Emmanuel Jeandel and Michaël Rao, An aperiodic set of 11 Wang tiles, Advances in Combinatorics 2021:1
    locator: 37 pp.
  - title: Peter van Emde Boas, The convenience of tilings, in A. Sorbi (ed.), Complexity, Logic, and Recursion Theory, Lecture Notes in Pure and Applied Mathematics 187, Marcel Dekker, 1997
    locator: pp. 331 to 363 (bounded tiling problems and their complexity)
---

The Wang tiling problem asks whether a finite set of square tiles with colored edges can tile the whole plane. Copies of each tile may be used without limit, tiles may not be turned or flipped, and two tiles that touch must have the same color on the shared edge. Hao Wang posed the problem in 1961. He noted that if every set that tiles the plane could also tile it periodically, the problem would be decidable. Robert Berger proved in 1966 that the problem is [undecidable](/undecidability/), and in doing so found the first *aperiodic* set: a set that tiles the plane, but only in ways that never repeat. The problem is not the [domino tiling problem](/domino-tiling-problem/) of covering a region with $1 \times 2$ dominoes, which is a different, solvable puzzle; Wang called his tiles "dominoes", which is where the alias comes from.

## In plain words

You have a few kinds of square tiles. Each edge of a tile has a color. You must cover an endless floor with copies of these tiles, without turning them, so that every pair of touching edges has the same color. Can it be done?

If the tiles can fill a pattern that repeats, the answer is yes. If they get stuck on every square of some size, the answer is no. Wang hoped that one of these two things always happens.

It does not. Berger found tile sets that fill the floor only in patterns that never repeat. He also showed how to build tiles whose rows copy the steps of a computer program, so that the floor can be filled exactly when the program runs forever. So no method can answer the question for every tile set.

## Definition

A *Wang tile* is a unit square with a color on each of its four edges, written $(n, e, s, w)$ for north, east, south and west. A *tiling* of the plane by a set $T$ is a map $\tau : \mathbb{Z}^2 \to T$ such that for every cell $(x, y)$ the east color of $\tau(x, y)$ equals the west color of $\tau(x+1, y)$, and the north color of $\tau(x, y)$ equals the south color of $\tau(x, y+1)$.

**Instance.** A finite set $T$ of Wang tiles.

**Question.** Is there a tiling of the plane by $T$?

**Theorem (Berger 1966).** The set of tile sets that tile the plane is not decidable. Its complement, the set of tile sets that do not tile the plane, is c.e. and complete for the c.e. sets under many-one reductions.

**Why the complement is c.e.** A tile set tiles the plane if and only if it tiles every $n \times n$ square. One direction is clear. For the other, the tilings of the squares of sizes $1, 3, 5, \ldots$ around the origin form an infinite, finitely branching tree under restriction, so by König's lemma the tree has an infinite branch, and the branch is a tiling of the plane. So a set does not tile the plane exactly when some square cannot be tiled, and a program that tries $n = 1, 2, 3, \ldots$ by backtracking finds such a square when one exists.

**Why the problem is hard.** First take the *origin-constrained* problem, where a given tile must sit at the origin. For a [Turing machine](/turing-machine/) $M$, build tiles whose rows are the configurations of $M$ on the blank tape. The south and north colors of a tile carry the content of one cell and, at the head, the state. The east and west colors pass the head from one cell to the next when it moves. The seed tile starts the first row with the start state. The tiles above can only extend a row by the next configuration, and no tile follows a halting configuration. So the upper half plane can be tiled if and only if $M$ runs forever, and the origin-constrained problem is undecidable (Kahr, Moore and Wang 1962). Without a seed, a tile set can avoid the computation by tiling with no seed at all. Berger's proof forces seeds to appear: his tiles build a hierarchy of squares of sizes growing without limit, and each square holds a run of $M$ of matching length. This structure can exist only without a period, which is why the proof produces an aperiodic set.

## Variants

- **Origin-constrained, or seeded.** A given tile must appear at the origin. Undecidable (Kahr, Moore and Wang 1962), with an easier proof than Berger's.
- **Periodic tiling.** Does $T$ admit a periodic tiling? This is c.e., since one can search over tilings of a torus.
- **Finite region.** Can $T$ tile an $n \times n$ square, with some colors fixed on the border? With $n$ written in unary this is NP-complete, and with $n$ written in binary it is NEXP-complete (van Emde Boas 1997).
- **Other shapes.** With rotation allowed, Robinson (1971) found an aperiodic set of $6$ shapes with notches. Such shapes are not Wang tiles, but they can be coded as Wang tiles. Tiling problems for polyominoes are treated under [polyomino tiling](/polyomino-tiling-problem/).

## Examples

**One tile.** The tile $(0, 1, 0, 1)$ has the same color on its north and south edges, and the same on its east and west edges. It tiles the plane by itself, with period $1$ in both directions.

**A checkerboard.** The tiles $(0, 1, 1, 0)$ and $(1, 0, 0, 1)$ each match only the other one on every side. They tile the plane in a checkerboard pattern with period $2$, and neither tile can do it alone.

**A set that gets stuck.** The tiles $(0, 0, 1, 0)$ and $(1, 0, 2, 0)$ fit side by side, since all east and west colors are $0$. But a column can hold only the first tile above the second, since no tile has south color $0$ or north color $2$. So the set tiles the $2 \times 2$ square and no $3 \times 3$ square, and it does not tile the plane. A backtracking search finds this at once.

**An aperiodic set.** Jeandel and Rao (2015) found a set of $11$ Wang tiles with $4$ colors that tiles the plane, but never periodically. They also proved that this is the smallest possible: every set of at most $10$ tiles, and every set with at most $3$ colors, either tiles the plane periodically or does not tile it at all. The previous record was a set of $13$ tiles (Čulík 1996).

## Known algorithms

- **Two semi-decision procedures.** For $n = 1, 2, 3, \ldots$, check by backtracking whether $T$ tiles the $n \times n$ square, and stop with "no" if it does not. At the same time, for each $p$, check whether $T$ tiles a $p \times p$ torus, and stop with "yes" if it does, since a torus tiling repeats to a periodic tiling of the plane. Together they halt on every tile set that is not aperiodic. They run forever exactly on the aperiodic sets.
- **Transducer methods.** Jeandel and Rao treated each row of tiles as a finite transducer between the colors below and above, and searched through compositions of these transducers. This is how they checked all small sets.
- **SAT solvers.** For a fixed square, the bounded problem is a satisfiability instance, with one variable per cell and tile.

## Bounds

- **Undecidable** in general (Berger 1966). The complement is complete for the c.e. sets, so the problem is co-c.e. and its [Turing degree](/turing-degrees/) is that of the [halting problem](/halting-problem/).
- **Aperiodic sets exist**, and the smallest has $11$ tiles. Without them, the two procedures above would decide the problem.
- **Bounded squares.** NP-complete with $n$ in unary, NEXP-complete with $n$ in binary.

## Reductions

All reductions here are many-one reductions by total computable maps.

- **From blank-tape halting.** Berger's construction maps a machine $M$ to a tile set that tiles the plane if and only if $M$ does not halt on the blank tape. So the complement of the blank-tape halting problem reduces to tiling.
- **To halting.** Map $T$ to the machine that searches for an $n \times n$ square that $T$ cannot tile. It halts if and only if $T$ does not tile the plane.
- **To logic.** Kahr, Moore and Wang coded the origin-constrained problem as satisfiability of first-order sentences of the form $\forall x\, \exists y\, \forall z\, \varphi$. So this small class of the [Entscheidungsproblem](/entscheidungsproblem/) is undecidable.

## Applications

- **Logic.** Tilings are a standard tool for proving that fragments of first-order logic, modal logics and description logics are undecidable: the models of a sentence are made to look like tilings of a grid.
- **Two-dimensional systems.** Tiles act like the space-time diagrams of a [cellular automaton](/cellular-automaton/). Tiling arguments are used to show that questions about two-dimensional automata are undecidable.
- **Aperiodic order.** Aperiodic tile sets are models of quasicrystals, solids that are ordered but not periodic.
- **Complexity.** The bounded problem is a convenient NP-complete and NEXP-complete problem for reductions, because tiles copy machine steps so directly.

## References
