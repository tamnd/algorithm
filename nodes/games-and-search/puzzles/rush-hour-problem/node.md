---
tag: 72JECE
kind: problem
slug: rush-hour-problem
name: Rush Hour problem
aliases:
- Rush Hour puzzle
area: games-and-search/puzzles
level: advanced
summary: Slide cars along their own rows or columns until the target car can leave the grid. PSPACE-complete on n by n boards (Flake and Baum 2002); the hardest 6 by 6 start needs 93 moves.
prereqs: [state-space-search, pspace]
see_also: [breadth-first-search, iterative-deepening-search, bidirectional-search, duplicate-detection, gadget-reduction, sokoban-problem, sliding-tile-puzzle, motion-planning]
sources:
  - paper: doi:10.1016/S0304-3975(01)00173-6
    title: Gary W. Flake and Eric B. Baum, Rush Hour is PSPACE-complete, or "Why you should generously tip parking lot attendants", Theoretical Computer Science 270(1-2), 2002, 895 to 911
    locator: the whole paper (the gadgets of cars and the proof of PSPACE-completeness on n by n boards)
  - paper: doi:10.1016/j.tcs.2005.05.008
    title: Robert A. Hearn and Erik D. Demaine, PSPACE-completeness of sliding-block puzzles and other problems through the nondeterministic constraint logic model of computation, Theoretical Computer Science 343(1-2), 2005, 72 to 96
    locator: the section on Rush Hour (a shorter proof by nondeterministic constraint logic)
  - paper: "John Tromp and Rudi Cilibrasi, Limits of Rush Hour logic complexity, preprint, 2005"
    locator: the whole paper (hardness with cars of length 2 only, and the limits of smaller gadgets)
  - paper: "Sébastien Collette, Jean-François Raskin and Frédéric Servais, On the symbolic computation of the hardest configurations of the RUSH HOUR game, Computers and Games (CG 2006), Lecture Notes in Computer Science 4630, Springer, 2007, 220 to 233"
    locator: the whole paper (all 6 by 6 configurations by symbolic search, and the hardest start, which needs 93 moves)
---

The Rush Hour problem gives a grid with cars of width one and length two or three. Each car can slide only forward or backward along its own row or column, and cars cannot pass through each other. One target car sits in a row with an exit at the right edge. Decide whether some sequence of slides lets the target car reach the exit, and find one with the fewest moves. On $n \times n$ boards the problem is [PSPACE](/pspace/)-complete (Flake and Baum 2002), and it stays so with cars of length 2 only (Tromp and Cilibrasi 2005). Every slide can be undone, so the states form an undirected graph. For the $6 \times 6$ board of the commercial puzzle, [breadth-first search](/breadth-first-search/) solves any start, and the hardest start needs 93 moves (Collette, Raskin and Servais 2006).

## In plain words

Cars and trucks are packed into a small square parking lot. Each one can only drive forward or backward, never turn. Your red car must get out through the gap in the wall, and other cars are in its way.

To clear the way, you move the blocking cars, but they are blocked by other cars, which you must move first. A good solution plans this chain of moves.

Every move can be undone, so you can never get stuck for good, but the shortest way out can be long. On big boards, no fast method is known, and the puzzle can encode any computation that uses a fixed amount of memory.

## Definition

A *board* is an $h \times w$ grid. A *car* $i$ has an orientation (horizontal or vertical), a fixed line (its row or column), a length $\ell_i \in \{2, 3\}$ and a position $x_i$, the first square it covers along its line. A *state* is the vector $(x_1, \ldots, x_m)$ such that no two cars share a square and all lie inside the grid. The target car $t$ is horizontal, and the state is *solved* when $x_t + \ell_t = w$, so that its right end is at the exit.

A *slide* changes one $x_i$ by $\delta \ne 0$ such that all the squares the car passes over are empty. Two costs are usual:

- **Moves.** Each slide costs 1, however far the car goes.
- **Steps.** A slide by $\delta$ costs $|\delta|$.

The problem asks whether a solved state is reachable from the start, and for the least cost.

## Variants

- **Generalized Rush Hour.** The $n \times n$ board with any number of cars of length 2 and 3. This is the version that is PSPACE-complete.
- **Cars of length 2 only.** Still PSPACE-complete (Tromp and Cilibrasi 2005).
- **Fixed board.** For $6 \times 6$, the number of states is finite, so every question has a fixed-size answer. Collette, Raskin and Servais (2006) solved all starts with symbolic search over binary decision diagrams, and found the hardest one, with 93 moves.
- **Related puzzles.** [Sokoban](/sokoban-problem/), where pushes cannot be undone, and the [sliding tile puzzle](/sliding-tile-puzzle/), where tiles move in all four directions. Sliding-block puzzles in general are PSPACE-complete too (Hearn and Demaine 2005).

## Examples

**One truck.** The target car A is in row 3 and a vertical truck B of length 3 blocks it.

```text
..B...
..B...
AAB...
......
......
......
```

Moving B down by 1 or 2 squares still blocks row 3, so B goes down by 3 squares. Then A slides right by 4 squares to the exit. The fewest moves is 2, and the fewest steps is $3 + 4 = 7$. If a second truck stood below B, filling the bottom three squares of that column, B could not leave row 3 and there would be no solution.

**A harder start.**

```text
MMKD.C
IIKD.C
J..AAC
J.HHB.
LEEEB.
LGGGFF
```

Here A is blocked by C, C by F, and so on. Breadth-first search finds the fewest moves, 12, and the fewest steps, 17. The start lies in a connected part of the state graph with 1935 states. Iterative deepening search to depth 12 finds the same least number of moves.

## Known algorithms

- **Breadth-first search.** Search the graph of states with slides as edges, with a hash set of visited states ([duplicate detection](/duplicate-detection/)). The first solved state found gives the fewest moves. For the steps cost, use only slides by one square. The state graph is undirected, so the search from the start explores exactly its connected part.
- **Iterative deepening.** [Iterative deepening search](/iterative-deepening-search/) uses memory linear in the depth, at the cost of repeated work. With a table of the depth left at each state seen, it skips most repeats.
- **Bidirectional search.** The target is not a single state but a set, so a backward search starts from all solved states of the part. [Bidirectional search](/bidirectional-search/) then meets in the middle.
- **Symbolic search.** Represent sets of states as binary decision diagrams and compute the layers of the search all at once (Collette, Raskin and Servais 2006). This is how all $6 \times 6$ starts were solved.
- **Heuristics.** A lower bound is the number of cars that block the target car, plus 1. It is weak, since the blocking cars may need many moves of other cars before they can leave.

## Bounds

- **PSPACE-complete** on $n \times n$ boards (Flake and Baum 2002). Membership holds since a state has polynomial size and the problem is reachability in a graph given implicitly, so [Savitch's theorem](/savitch-theorem/) applies.
- **Cars of length 2.** PSPACE-complete (Tromp and Cilibrasi 2005).
- **Search cost.** Breadth-first search takes time and space linear in the size of the connected part, which can be exponential in the number of cars. Each state has $O(m n)$ slides.
- **$6 \times 6$.** The hardest start needs 93 moves (Collette, Raskin and Servais 2006).

## Reductions

- **From reversible circuits.** Flake and Baum build gadgets of cars that act as logic gates whose signals can move both ways. Wired together on a large board, they simulate a computation with polynomial memory. The target car can leave only if the computation accepts.
- **From nondeterministic constraint logic.** Hearn and Demaine (2005) give AND and OR gadgets for NCL made of cars, a shorter proof that also covers other sliding-block puzzles. See [gadget reduction](/gadget-reduction/).
- **To graph search.** The puzzle is reachability in the state graph, so all [state-space search](/state-space-search/) methods apply.

## Applications

- **A model of motion planning.** Moving many objects in a tight space, each with limited freedom, is a [motion planning](/motion-planning/) problem. Rush Hour shows that it is hard even with straight-line moves on a grid.
- **Puzzle design.** Breadth-first search over all starts with a given set of cars rates puzzles by their least number of moves, and finds the hardest ones.
- **Teaching search.** A small, familiar puzzle with an undirected state graph and a hard general case.

## References
