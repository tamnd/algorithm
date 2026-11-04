---
tag: MQ3R69
kind: algorithm
slug: best-first-search
name: Best-first search
aliases:
- best-first graph search
area: techniques/search-strategies
level: core
summary: Expands the frontier state with the smallest value of an evaluation function, a generalisation of uniform-cost search.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {N: the number of nodes generated, V: the number of reachable states}
  time: {worst: O(N log N), best: O(1)}
  space: {extra: O(N + V)}
properties: {deterministic: true, recursive: false}
prereqs: [search-strategy, search-frontier, priority-queue, graph-search-vs-tree-search]
see_also: [uniform-cost-search, greedy-best-first-search, a-star-search, breadth-first-search, heuristic-function, admissible-heuristic, recursive-best-first-search, best-first-branch-and-bound]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.3.1 (the BEST-FIRST-SEARCH function with the reached table) and Section 3.5 (greedy best-first search and A* as instances)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (the best-first strategy BF and its special cases) and Chapter 3 (the properties of A*)
  - paper: doi:10.1145/3828.3830
    title: Rina Dechter and Judea Pearl, Generalized best-first search strategies and the optimality of A*, Journal of the ACM 32(3) (1985)
    locator: pp. 505 to 536 (best-first search with a general evaluation function, and the conditions for admissibility)
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (the algorithm A* and the proof that it is admissible)
---

Best-first search is the general [search strategy](/search-strategy/) that keeps the [frontier](/search-frontier/) in a [priority queue](/priority-queue/) and always expands the node with the least value of an evaluation function $f$. The function $f$ is a parameter: $f = g$, the path cost, gives [uniform-cost search](/uniform-cost-search/), $f = h$, an estimate of the cost to a goal, gives [greedy best-first search](/greedy-best-first-search/), and $f = g + h$ gives [A* search](/a-star-search/). Each choice keeps the same loop and changes the order. As graph search, it stops on each finite space for every $f$. It returns a cheapest path when $f = g + h$ with an [admissible heuristic](/admissible-heuristic/) $h$.

## In plain words

You keep a list of places you can still explore, and you give each place a score. At each step you take the place with the best score. If it is a goal, you stop. If not, you look at its neighbours, give each a score, and put them on the list.

Everything depends on the score. If the score is the price of the trip so far, you get the cheapest trip. If the score is a guess of how far the goal still is, you rush to the goal, and you may pay too much. If the score is the price so far plus a guess that never overestimates the rest, you still get the cheapest trip, and a good guess makes you look at far fewer places.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(s', c)$ of a next state and an action cost $c \ge 0$, a goal test IS-GOAL, and an evaluation function $f$ on nodes. A node $n$ holds a state, a parent, the path cost $g(n)$ and the depth. The output is a path from $s_0$ to a goal state, or failure. The quality of the path depends on $f$, see Correctness.

## The algorithm

This is the graph-search version of Russell and Norvig. The table *reached* maps each state to the cheapest node known for it. A child is added when its state is new or when its path cost $g$ is strictly lower than the stored one. The older node of the state then stays in the queue, and line L6 skips it.

```pseudo id=main
BEST-FIRST-SEARCH(s0, SUCCESSORS, IS-GOAL, f)
L1  node ← NODE(state = s0, parent = nil, g = 0, depth = 0)
L2  frontier ← a min-priority queue on f, holding node
L3  reached ← { s0 ↦ node }
L4  while frontier is not empty do
L5      n ← POP-MIN(frontier)
L6      if n ≠ reached[n.state] then continue            ▷ a cheaper node replaced n
L7      if IS-GOAL(n.state) then return PATH(n), n.g
L8      for each (s', c) in SUCCESSORS(n.state) do
L9          child ← NODE(state = s', parent = n, g = n.g + c, depth = n.depth + 1)
L10         if s' is not in reached or child.g < reached[s'].g then
L11             reached[s'] ← child
L12             PUSH(frontier, child) with key f(child)
L13 return failure
```

The goal test is at line L7, when a node leaves the frontier. The test at line L10 compares path costs, not values of $f$. So a state that was already expanded is expanded again when a cheaper path to it appears. This reopening is what keeps A* optimal with a heuristic that is admissible but not consistent, see [graph search versus tree search](/graph-search-vs-tree-search/). Ties in $f$ are broken in the order of insertion.

## Example

The graph has the directed edges S→A 1, S→G 12, A→B 4, A→C 1, B→D 3, C→D 1, C→G 2, D→G 3, with start S and goal G. Its solutions cost 12 (S-G), 4 (S-A-C-G), 6 and 11, so $C^* = 4$. Two heuristics are used. The function $h^*$ is the true cost to G: S 4, A 3, B 6, C 2, D 3, G 0. The function $h_1$ is S 4, A 3, B 1, C 2, D 1, G 0, which is admissible but not exact.

| $f$ | strategy | states expanded, in order | path returned | cost |
| --- | --- | --- | --- | --- |
| $g$ | uniform-cost | S, A, C, D | S-A-C-G | 4 |
| depth | breadth-first, late goal test | S, A | S-G | 12 |
| $g + h^*$ | A* with a perfect heuristic | S, A, C | S-A-C-G | 4 |
| $h_1$ | greedy best-first | S | S-G | 12 |

The run with $f = g + h^*$ in detail, with the frontier as path:$g$:$f$:

| step | frontier before POP-MIN | popped | children pushed |
| --- | --- | --- | --- |
| 1 | S:0:4 | S | S-A:1:4, S-G:12:12 |
| 2 | S-A:1:4, S-G:12:12 | S-A | S-A-C:2:4, S-A-B:5:11 |
| 3 | S-A-C:2:4, S-A-B:5:11, S-G:12:12 | S-A-C | S-A-C-G:4:4, S-A-C-D:3:6 |
| 4 | S-A-C-G:4:4, S-A-C-D:3:6, S-A-B:5:11, S-G:12:12 | S-A-C-G, a goal | |

With the perfect heuristic, A* expands only the states of the cheapest path. Uniform-cost search also expands D, whose $g = 3$ is below $C^* = 4$. Greedy search goes to G at once because $h_1(G) = 0$, and it does not look at the cost 12 of that edge. Breadth-first order, as $f$ = depth with the late goal test, selects S-G at depth 1 before the nodes of depth 2.

## Correctness

The results below hold for the pseudocode above and non-negative action costs.

- **Soundness.** A returned path is a path from $s_0$ to a goal, and its cost is $n.g$.
- **Finite spaces, every $f$.** The search stops, and it returns failure only when no goal can be reached. Each pushed node is a path without a repeated state, because a state is pushed again only on a strictly cheaper path, so there are finitely many pushes.
- **Optimality for $f = g + h$.** Let $h \ge 0$ be admissible, that is, $h(s)$ is at most the least cost from $s$ to a goal, with $h = 0$ on goals. Then the path returned has cost $C^*$. The proof keeps a node of an optimal path in the frontier with $g$ equal to the cost of the optimal prefix, so its $f$ is at most $C^*$, while a goal node with a larger cost has $f > C^*$. Uniform-cost search is the case $h = 0$.
- **Infinite spaces.** For $f = g + h$ with $h$ admissible, a finite branching factor and costs at least $\epsilon > 0$, the search returns a path of cost $C^*$ when a goal is reachable. For other $f$, such as $f = h$, the search can run for ever on an infinite space that has a goal.

The full proofs are below.

## Complexity

The costs are in the [word RAM](/word-ram/), with a call of SUCCESSORS per generated child, IS-GOAL and an operation on *reached* each counted as $O(1)$ ($O(1)$ expected for a hash table). Let $N$ be the number of nodes generated. Each node is pushed once and popped at most once, and a binary heap does each operation in $O(\log N)$ time. So the time is $O(N \log N)$ and the space is $O(N + V)$ for the heap and the table, where $V$ is the number of states reached.

$N$ depends on $f$ and on the problem, and the special cases have their own bounds. For uniform-cost search, $N = O(b^{1 + \lfloor C^*/\epsilon \rfloor})$ in a tree of branching factor $b$. With $f$ = depth, it is $O(b^{d+1})$. On an explicit graph with $E$ edges, if no state is expanded twice, $N \le E + 1$. This holds for $f = g$ and for $f = g + h$ with a [consistent heuristic](/consistent-heuristic/). With a heuristic that is admissible but not consistent, a state can be expanded many times, and on some graphs A* with reopening expands exponentially many nodes in the number of states. In the best case the start state is a goal, and the search does $O(1)$ work.

## Properties

- **One loop, many strategies.** Uniform-cost search, greedy best-first search, A*, weighted A* and breadth-first search with a late goal test differ only in $f$.
- **Graph search.** The table *reached* gives one live node per state. Memory grows with the number of states reached, and this is the main practical limit of best-first search.
- **Informed or uninformed.** The search is informed when $f$ uses a heuristic, and uninformed when $f$ uses only $g$ and the depth.
- **Order-preserving.** States leave the frontier in non-decreasing order of $f$ when $f$ does not decrease along each path, as for $f = g$ and for $f = g + h$ with a consistent $h$.

## Variants and improvements

- **[Greedy best-first search](/greedy-best-first-search/), $f = h$.** Fast when $h$ is good, but not cost-optimal.
- **[A* search](/a-star-search/), $f = g + h$.** Cost-optimal with an admissible $h$, and it expands no state twice with a consistent $h$.
- **[Weighted A*](/weighted-a-star/), $f = g + w h$ with $w > 1$.** The cost of the path is at most $w C^*$ when $h$ is admissible, and the search often expands far fewer nodes.
- **[Recursive best-first search](/recursive-best-first-search/) and [SMA*](/simplified-memory-bounded-a-star/).** Keep the best-first order with memory linear in the depth, or with a fixed memory, at the price of repeated work.
- **[Beam search](/beam-search/).** Keep only the best $k$ nodes of the frontier. The memory is bounded, but the search is no longer complete.
- **Tree-like best-first search.** Drop *reached*. It needs no table, but it repeats states and may not stop on a finite space with cycles.
- **[Best-first branch and bound](/best-first-branch-and-bound/).** The same rule in optimization: the frontier holds subproblems, and $f$ is a bound on their best value.

## When to use it

Use best-first search when you can say which nodes are more promising, and you can afford a table of all reached states. Pick $f$ by what you need. For a cheapest path without a heuristic, use $f = g$. For a cheapest path with an admissible heuristic, use $f = g + h$. For any path found fast, use $f = h$ or a weighted A*. When the reached states do not fit in memory, use a depth-first method such as [iterative deepening](/iterative-deepening-search/) or [IDA*](/iterative-deepening-a-star/).

## Pitfalls

- **Goal test at generation.** Testing $s'$ for the goal in the loop of line L8 can return a costly goal that was generated early. Test at line L7.
- **Comparing $f$ instead of $g$ at line L10.** For $f = g + h$ the two tests agree, because both nodes have the same state. For an $f$ that is not of this form, such as the depth or a weighted sum, comparing $f$ can refuse a cheaper path. Keep the test on $g$.
- **A closed set without reopening.** If line L10 refuses every state that was already expanded, A* with an admissible but inconsistent heuristic can return a costly path. The example on the page [graph search versus tree search](/graph-search-vs-tree-search/) returns cost 7 instead of 6.
- **Changing the key of a node in the heap.** Writing a new $g$ into a node that is in a binary heap breaks the heap order. Push a new node and skip the old one at line L6.
- **Negative costs.** The optimality proof needs $c \ge 0$.

## Implementations

## History

Hart, Nilsson and Raphael defined A* in 1968 and proved that it finds a cheapest path with an admissible heuristic. Pearl's book of 1984 treats best-first search with a general evaluation function as the common frame of these methods, and Dechter and Pearl (1985) studied generalized best-first strategies and the conditions under which A* is optimal among them. Russell and Norvig, in their fourth edition, use one BEST-FIRST-SEARCH function with a *reached* table for uniform-cost search, greedy search and A*.

## References
