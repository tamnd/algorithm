---
tag: M8RQ8V
kind: concept
slug: memory-bounded-heuristic-search
name: Memory-bounded heuristic search
aliases:
- memory-limited search
area: games-and-search/heuristic-search
level: advanced
summary: Heuristic searches that store only a bounded number of nodes, such as IDA*, RBFS, SMA* and fringe search. They pay for the saved memory by regenerating the nodes they forget.
prereqs: [a-star-search, iterative-deepening-search]
see_also: [iterative-deepening-a-star, recursive-best-first-search, simplified-memory-bounded-a-star, fringe-search, depth-first-branch-and-bound, beam-search, beam-stack-search, partial-expansion-a-star]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition
    locator: Section 3.5.5 (memory-bounded search, with beam search, IDA*, RBFS and SMA*)
  - paper: doi:10.1016/0004-3702(93)90045-D
    title: Richard E. Korf, Linear-space best-first search, Artificial Intelligence 62(1) (1993)
    locator: pp. 41 to 78 (the problem of the memory of best-first search, and RBFS against IDA*)
  - paper: Stuart Russell, Efficient memory-bounded search methods, Proceedings of the 10th European Conference on Artificial Intelligence (ECAI-92)
    locator: pp. 1 to 5 (searches that use all the memory that is available, and SMA*)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications, Morgan Kaufmann (2012)
    locator: the chapters on linear-space search and on memory-restricted search (general locator)
---

Memory-bounded heuristic search is the family of searches that find paths with a [heuristic](/heuristic-function/), like [A*](/a-star-search/), but store only a bounded number of nodes. A* keeps every state it generates, so its memory grows as fast as its time, and on hard problems such as the 15-puzzle it runs out of memory long before it runs out of time. A memory-bounded search keeps less and generates some nodes again when it needs them. The methods differ in how much they keep: one path with [IDA*](/iterative-deepening-a-star/) and [RBFS](/recursive-best-first-search/), a fixed number $M$ of nodes with [SMA*](/simplified-memory-bounded-a-star/), a frontier with [fringe search](/fringe-search/), or a beam of fixed width with [beam search](/beam-search/). With an [admissible heuristic](/admissible-heuristic/), most of them still return optimal paths.

## In plain words

A* is like an explorer who writes down every place seen so far. That list is what makes A* fast, because it never looks at a place twice. But on a big map, the list gets too long to carry.

Memory-bounded searches carry a short list. Some keep only the way back to the start. Some keep a fixed number of places and throw away the worst one when the list is full. Some keep only the best few places at each step.

When they throw a place away, they lose the work they did to reach it. If they need it later, they find it again. So they trade time for space. A good method throws away the places it will not need, and remembers how good the places it threw away looked, so that it knows when to come back.

## The idea

**Why memory is the limit.** A* stores each generated state in its [open list](/open-list/) or its closed list. With an [effective branching factor](/effective-branching-factor/) $b$ and a solution at depth $d$, it stores about $b^d$ states in the worst case, the same order as the number it expands. Expanding a state is fast and storing it is not free, so on hard problems A* fills memory long before it would finish.

**What a method forgets.** Each method chooses what to keep:

| method | what it stores | how it gets back what it forgot | optimal with an admissible $h$ |
| --- | --- | --- | --- |
| [IDA*](/iterative-deepening-a-star/) | the current path, $O(b\,d)$ | depth-first iterations with a rising threshold on $f$ | yes |
| [RBFS](/recursive-best-first-search/) | the current path and the values of its siblings, $O(b\,d)$ | returns to a forgotten subtree when the alternatives get worse than its backed-up value | yes |
| [SMA*](/simplified-memory-bounded-a-star/) | at most $M$ nodes | deletes the worst leaf, keeps its value in the parent, and makes it again later | yes, when an optimal path fits in $M$ nodes |
| [fringe search](/fringe-search/) | the frontier and a table of $g$ values | threshold passes over a list, with no restart from the root | yes |
| [depth-first branch and bound](/depth-first-branch-and-bound/) | the current path and the best cost so far | depth-first search that prunes nodes with $f$ at least the best cost | yes, if the tree is finite |
| [beam search](/beam-search/) | $k$ states per layer | never, it drops states for good | no, and not complete |
| [beam-stack search](/beam-stack-search/) | $k$ states per layer and a stack of ranges of $f$ | backtracks to the next range of a layer | yes, for unit costs and a consistent $h$ |

**Two tools.** Most of these methods use one of two ideas. The first is the *threshold*: search only the nodes with $f$ at most a bound, and raise the bound when nothing below it works. IDA* and fringe search do this. The second is the *backed-up value*: when a subtree is forgotten, keep the least $f$ on its frontier in its parent, as a lower bound for the whole subtree. RBFS, SMA* and its predecessor MA* do this. Both ideas keep the search admissible, because the values they use never exceed the cost of the cheapest solution below a node.

**The cost.** A forgotten node costs time to make again. Linear-space methods also lose [duplicate detection](/duplicate-detection/): they see only the states on the current path, so on a graph with many paths to each state, such as a grid, they can expand the same state an exponential number of times. They work best on trees, or on graphs like the sliding-tile puzzles, where most paths to a state are long. A method that uses all the memory it has, like SMA*, regenerates less, but has more work per node.

**Few distinct values.** A threshold method does well when $f$ takes few distinct values, as with unit costs and integer heuristics. Then each new threshold adds many nodes, and the work of the earlier iterations is a small part of the total. With many distinct costs, each iteration can add only one node, and IDA* can expand $O(n^2)$ nodes where A* expands $n$.

## Examples

**The page graph.** On the graph of the page [A* search](/a-star-search/), with 8 states, costs from 1 to 4 and $C^* = 7$, the methods behave as follows:

- A* expands S, A, D, B, C and returns S-B-C-G.
- IDA* runs two iterations, with the thresholds 6 and 7, and expands S, A in the first one and S, A, D, B, C in the second.
- RBFS expands S, A, D, then leaves the subtree of A with the backed-up value 8, and expands B, C. Its 5 expansions are those of A*, in the same order.
- Fringe search uses the same thresholds as IDA*, but in its second pass it goes on from the frontier of the first one, so it expands S, A, D, B, C once each.
- SMA* with $M = 4$ makes 10 children and deletes 7 nodes. With $M = 3$, no solution path fits, since each one has 3 actions, and SMA* returns failure.

**The 8-puzzle.** The scripts of the pages draw 20 instances with `random.Random(2024)`: each one is the goal after 60 random moves, kept if a breadth-first search gives an optimal cost $d \ge 14$. The heuristic is the Manhattan distance. Each method returned an optimal path on each instance, with these totals over the 20 instances:

| method | work, all 20 instances |
| --- | --- |
| A* | 3,411 expansions |
| fringe search | 4,946 expansions |
| RBFS | 7,494 expansions |
| IDA* | 8,229 expansions, over 78 iterations |
| SMA*, $M = 200$ | 7,888 children made |
| SMA*, $M = d + 1$ | 11,605 children made |

The other methods did between about 1.5 and 3.4 times the work of A*. In return, IDA* and RBFS stored only the current path, which has at most 25 states here. These numbers are measured on these instances only.

## Where it is used

- **Puzzles.** IDA* with [pattern databases](/pattern-database/) is the standard way to find optimal solutions of the [sliding-tile puzzles](/sliding-tile-puzzle/) and the [Rubik's cube](/rubiks-cube-problem/), where A* runs out of memory.
- **Game maps.** Fringe search was presented as a faster replacement for A* in path finding on the maps of video games.
- **Planning and scheduling.** Beam search, beam-stack search and depth-first branch and bound are common in planners and schedulers with deep search spaces, where a first good plan matters more than proof of optimality.
- **Sequence alignment.** [Multiple sequence alignment](/multiple-sequence-alignment/) has large search spaces with many duplicates, which led to methods such as [partial-expansion A*](/partial-expansion-a-star/), which keeps fewer nodes in the open list, and to searches that store only the frontier.
- **Speech and language.** Beam search keeps the search of a speech recognizer or a translation model within a fixed time per word.

## References
