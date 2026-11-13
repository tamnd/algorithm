---
tag: KA46D3
kind: concept
slug: pattern-database
name: Pattern database
aliases:
- PDB
- abstraction heuristic
area: games-and-search/heuristic-search
level: advanced
summary: A table of exact costs in an abstract space that keeps part of each state, built by one backward search and read as an admissible heuristic. Disjoint tables that count only their own moves add up.
prereqs: [relaxation-heuristic, consistent-heuristic, breadth-first-search]
see_also: [heuristic-dominance, sliding-tile-puzzle, rubiks-cube-problem, iterative-deepening-a-star, permutation-rank-unrank, a-star-search, hsp-planner, landmark-heuristic]
sources:
  - paper: doi:10.1111/0824-7935.00065
    title: Joseph C. Culberson and Jonathan Schaeffer, Pattern databases, Computational Intelligence 14(3) (1998)
    locator: pp. 318 to 334 (pattern databases for the 15 puzzle, built by backward breadth-first search, with IDA*, and the reduction of the nodes searched on 100 standard instances by more than a factor of 1000)
  - paper: doi:10.1016/S0004-3702(01)00092-3
    title: Richard E. Korf and Ariel Felner, Disjoint pattern database heuristics, Artificial Intelligence 134(1-2) (2002)
    locator: pp. 9 to 22 (disjoint additive databases that count only the moves of the pattern tiles, the 15 puzzle about 2000 times faster than with the Manhattan distance, and optimal solutions of 50 random 24 puzzles)
  - paper: doi:10.1613/jair.1480
    title: Ariel Felner, Richard E. Korf and Sarit Hanan, Additive pattern database heuristics, Journal of Artificial Intelligence Research 22 (2004)
    locator: pp. 279 to 318 (statically and dynamically partitioned additive databases, the 7-8 partition of the 15 puzzle and the 6-6-6-6 partition of the 24 puzzle with its reflection)
  - paper: Richard E. Korf, Finding optimal solutions to Rubik's Cube using pattern databases, Proceedings of AAAI-97 (1997)
    title: Finding optimal solutions to Rubik's Cube using pattern databases
    locator: pp. 700 to 705 (IDA* with the maximum of a corner table and two tables of six edge cubies, the first optimal solutions of random cubes)
  - paper: Stefan Edelkamp, Planning with pattern databases, Proceedings of the 6th European Conference on Planning, ECP 2001 (2001)
    title: Planning with pattern databases
    locator: pp. 13 to 24 (pattern databases for domain-independent planning)
  - paper: doi:10.1016/j.artint.2011.02.001
    title: Ariel Felner, Uzi Zahavi, Robert Holte, Jonathan Schaeffer, Nathan Sturtevant and Zhifu Zhang, Inconsistent heuristics in theory and practice, Artificial Intelligence 175(9-10) (2011)
    locator: Section 6 (pattern databases that are admissible but not consistent, among them compressed tables that store one value for several entries)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 4 (abstraction transformations, pattern databases, disjoint and additive pattern databases)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.6 (heuristics from subproblems, pattern databases and disjoint pattern databases)
---

A pattern database is a table that stores, for each state of an abstract version of a search problem, the exact cost from that state to the abstract goal. The abstract state keeps only part of the real state, the *pattern*: for a [sliding tile puzzle](/sliding-tile-puzzle/), the squares of a few chosen tiles and of the blank. One [breadth-first search](/breadth-first-search/) backward from the goal fills the table, and during the real search the [heuristic](/heuristic-function/) of a state is one table lookup. The abstraction is a [relaxation](/relaxation-heuristic/) that merges states, so the value is [admissible](/admissible-heuristic/) and [consistent](/consistent-heuristic/). Culberson and Schaeffer (1998) introduced the idea for the 15 puzzle, and Korf and Felner (2002) showed that tables for disjoint sets of tiles can be added when each one counts only the moves of its own tiles.

## In plain words

Solving the whole puzzle is hard, so solve a smaller puzzle instead: watch only four of the tiles, and treat the other tiles as blank-looking pieces with no numbers. This smaller puzzle has few enough positions that a program can solve all of them once, ahead of time, and write the answers in a table.

During the real search, look at where the four watched tiles are, and read the table. The answer is never more than the true number of moves, because every real solution also solves the small puzzle.

You can build several tables for different groups of tiles. Taking the largest answer is always safe. Adding the answers is also safe, but only when the groups do not share tiles and each table counts only the moves of its own tiles. Bigger tables give better guesses but use more memory.

## The idea

### Definition

Let the real problem have states $S$, unit-cost or weighted actions, and a goal state $t$. An *abstraction* is a map $\varphi$ from $S$ onto a smaller set of abstract states, with an abstract action $\varphi(u) \to \varphi(v)$ for each real action $u \to v$, of the same cost. The *pattern database* of $\varphi$ is the table

$$\mathrm{PDB}[a] = \text{the cost of a cheapest abstract path from } a \text{ to } \varphi(t),$$

for each abstract state $a$, and its heuristic is $h(s) = \mathrm{PDB}[\varphi(s)]$. For a sliding tile puzzle with $n$ squares and a pattern of $k$ tiles, $\varphi(s)$ is the tuple of the squares of the $k$ tiles and of the blank. The other tiles become indistinguishable, so many real boards share one entry.

### Building the table

The real moves of the puzzles are reversible with equal cost, so a breadth-first search in the abstract space that starts at $\varphi(t)$ reaches each abstract state $a$ at depth $\mathrm{PDB}[a]$. The search never touches the real space. The table has one entry per abstract state:

$$\frac{n!}{(n - k - 1)!} \text{ entries with the blank in the key}, \qquad \frac{n!}{(n - k)!} \text{ without it}.$$

Programs store it as an array indexed by a [rank of the partial permutation](/permutation-rank-unrank/), with one byte or less per entry, so a lookup costs $O(k)$ word operations to compute the rank and one memory access. When actions have different costs, a [Dijkstra](/dijkstra/) search replaces the breadth-first search.

### Admissible and consistent

The abstraction satisfies the definition of a relaxation on the page [relaxation heuristic](/relaxation-heuristic/): each real action maps to an abstract action of the same cost, and the goal maps to the abstract goal. The fact proved there gives $h(u) \le c(u, v) + h(v)$ for each action and $h(t) = 0$, so the table is consistent and admissible. A finer abstraction, one that maps two real states together only when a coarser one also does, gives a table that [dominates](/heuristic-dominance/) the coarser one.

### Combining several tables

**Maximum.** For any tables $h_1, \ldots, h_r$, $\max_i h_i$ is admissible and consistent, since each $h_i$ is. A move of the 15 puzzle or of Rubik's Cube changes the positions of tiles in several patterns, so the sum of such tables can overestimate.

**Disjoint additive tables.** Korf and Felner (2002) split the tiles into disjoint patterns $P_1, \ldots, P_r$ and gave the abstract space of $P_i$ a different cost: a move of a tile of $P_i$ costs 1, and a move of any other tile costs 0. The table is then a 0-1 breadth-first search, with 0-cost moves at the front of the queue.

**Fact.** If each table counts only the moves of its own pattern, and the patterns are disjoint, then $h(s) = \sum_i \mathrm{PDB}_i[\varphi_i(s)]$ is admissible, and it is consistent when the key of each table holds the blank.

*Proof.* Take a cheapest real path from $s$ of length $h^*(s)$. Each move on it moves one tile, which lies in at most one pattern. Map the path into the abstract space of $P_i$: it becomes an abstract path from $\varphi_i(s)$ to the abstract goal whose cost is the number of moves of tiles of $P_i$. That cost is at least $\mathrm{PDB}_i[\varphi_i(s)]$. Summing over $i$, the right sides add up to at most the number of moves on the path, so $h(s) \le h^*(s)$. For consistency, let a real move take $s$ to $s'$ and move a tile of $P_j$, or of no pattern. In the space of $P_j$ it is an abstract move of cost 1, so that term drops by at most 1. In each other space it is an abstract move of cost 0, and its reverse is one too, so by the triangle inequality those terms do not change. So $h(s) \le 1 + h(s')$. $\square$

Each additive table is at least the Manhattan distance of its own tiles, since the Manhattan distance of a tile is the cost of the further relaxation in which the tile ignores all others. So the sum dominates the Manhattan distance.

**Tables without the blank.** To save memory, Korf and Felner drop the blank from the key of an additive table and store the least value over the blank squares. This is still admissible, as the proof shows. It is not always consistent: the table stores one value for several entries, which Felner et al. (2011, Section 6) list as a source of inconsistent heuristics. The example below counts the violations. With such a table, [A*](/a-star-search/) must reopen states or it can return a path that is too long, while [IDA*](/iterative-deepening-a-star/), the usual partner of pattern databases, is not affected.

### Limits

A table is a trade of memory for search. A larger pattern gives larger values, and the table grows by a factor of about $n - k$ for each tile added. The gain does not come for free elsewhere either: the values are exact only for the abstract space, so on states where the ignored tiles are badly placed the estimate stays weak. The table pays off when many searches share one goal, since it is built once per goal and pattern.

## Examples

### The 8-puzzle

The goal is $(1, 2, 3, 4, 5, 6, 7, 8, \text{blank})$ row by row, and the patterns are $A = \{1, 2, 3, 4\}$ and $B = \{5, 6, 7, 8\}$.

| heuristic | entries | largest entry | mean $h$ over the 181,440 boards | A* expansions, mean of 100 boards |
| --- | --- | --- | --- | --- |
| Manhattan distance | none | none | 14.00 | 730.4 |
| table of $A$, all moves count | 15,120 | 28 | 18.43 | 211.9 |
| maximum of the tables of $A$ and $B$, all moves count | 2 × 15,120 | 28 and 26 | 19.41 | 52.9 |
| sum of the additive tables of $A$ and $B$, blank in the key | 2 × 15,120 | 15 and 16 | 19.13 | 63.0 |
| sum of the additive tables of $A$ and $B$, blank dropped | 2 × 3,024 | 15 and 15 | 18.51 | 80.6 |

The mean of $h^*$ is 21.97. The 100 boards are drawn with a fixed seed, A* breaks ties toward larger $g$, and it reopens states. A 4-tile table of the 8-puzzle covers half of the tiles, so on this small board the maximum of two tables that count all moves beats the additive pair. Korf and Felner report the opposite on the 15 and 24 puzzles, where each pattern holds a smaller share of the tiles.

The blank-free additive heuristic is admissible on all 181,440 boards, but 18,852 of the directed moves break consistency. On the 100 boards, A* without reopening returns one path that is 2 moves too long with it. The four other heuristics are consistent on every move.

**One lookup.** For the board 5 1 3 / 4 blank 2 / 7 8 6, the true cost is 12 moves and the Manhattan distance is 6. The table of $A$ sees the abstract board $\ast$ 1 3 / 4 blank 2 / $\ast$ $\ast$ $\ast$, where $\ast$ is any tile outside $A$, and returns 12, the exact cost. The additive sum returns 8.

### The 15 and 24 puzzles

Culberson and Schaeffer (1998) used tables for the fringe tiles and the corner tiles of the 15 puzzle with [IDA*](/iterative-deepening-a-star/), and on 100 standard instances the number of nodes searched fell by a factor of more than 1000. Korf and Felner (2002) split the 15 puzzle into disjoint patterns of 7 and 8 tiles and the 24 puzzle into four patterns of 6 tiles. Without the blank, these tables have

$$\frac{16!}{9!} = 57{,}657{,}600, \qquad \frac{16!}{8!} = 518{,}918{,}400, \qquad \frac{25!}{19!} = 127{,}512{,}000$$

entries. They solved the 15 puzzle about 2000 times faster than with the Manhattan distance, and found optimal solutions of 50 random 24 puzzles. They also took the maximum of the sum and of the sum on the board reflected about its main diagonal, which uses the same tables a second time.

### Rubik's Cube

Korf (1997) found the first optimal solutions of random instances of the [Rubik's Cube](/rubiks-cube-problem/) with IDA* and the maximum of three tables. The corner table has $8! \cdot 3^7 = 88{,}179{,}840$ entries, one for each placement and twist of the 8 corner cubies, and each of two edge tables has $\frac{12!}{6!} \cdot 2^6 = 42{,}577{,}920$ entries for 6 of the 12 edge cubies. A twist moves both corners and edges, so the three values are combined by the maximum, not the sum. The median optimal solution length of his random cubes appeared to be 18 moves.

## Where it is used

- **Puzzles.** The sliding tile puzzles, Rubik's Cube, the Top Spin puzzle and the Towers of Hanoi with four pegs are standard test domains. Optimal solvers pair the tables with IDA*, which needs no memory for OPEN, so all memory goes to the tables.
- **Domain-independent planning.** Edelkamp (2001) built pattern databases for planning problems, where a pattern is a set of state variables. Planners choose the patterns automatically and combine many tables, a line of work kept apart from the [landmark](/landmark-heuristic/) and delete relaxation heuristics of the [HSP planner](/hsp-planner/) family.
- **Path finding with a fixed goal.** A table of exact distances in a coarse version of a map is a pattern database. [Hierarchical pathfinding A*](/hierarchical-pathfinding-a-star/) uses a related abstraction to plan, not to estimate.
- **Hierarchies of abstractions.** Instead of a full table, a program can compute abstract distances on demand by search and cache them, as in Hierarchical A*. The page [relaxation heuristic](/relaxation-heuristic/) gives Valtorta's limit on such schemes.

## References
