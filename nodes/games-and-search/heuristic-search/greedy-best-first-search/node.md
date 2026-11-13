---
tag: TT8WY1
kind: algorithm
slug: greedy-best-first-search
name: Greedy best-first search
aliases:
- best-first search by h
- greedy heuristic search
- greedy search
area: games-and-search/heuristic-search
level: intro
summary: Best-first search that always expands the open state of least heuristic value h. It is often fast, but the path it returns can cost much more than the cheapest one.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {n: the number of states reachable from the start, m: the number of actions among them}
  time: {graph: O(m + n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1966
  people: [J. E. Doran, Donald Michie]
  note: The Graph Traverser of Doran and Michie expanded the node of least estimated distance to the goal, which is greedy best-first search.
prereqs: [heuristic-function, best-first-search, open-list]
see_also: [a-star-search, weighted-a-star, beam-search, hill-climbing, uniform-cost-search, graph-search-vs-tree-search, completeness-and-optimality-of-search, limited-discrepancy-search]
sources:
  - paper: doi:10.1098/rspa.1966.0205
    title: J. E. Doran and D. Michie, Experiments with the Graph Traverser program, Proceedings of the Royal Society of London, Series A 294(1437) (1966)
    locator: pp. 235 to 259 (the Graph Traverser, which develops the node of least heuristic value, and experiments on the 8-puzzle)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.5.1 (greedy best-first search, the example on the map of Romania, and its completeness in finite spaces)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (best-first search with an evaluation function, of which ordering by h alone is the special case)
---

Greedy best-first search is [best-first search](/best-first-search/) with the evaluation $f(n) = h(n)$, where $h$ is a [heuristic function](/heuristic-function/) that estimates the cost from $n$ to a goal. It always expands the state that looks closest to a goal and ignores the cost $g(n)$ of the path that led there. With a good $h$ it reaches a goal after few expansions, but the path it returns is not always cheapest, and it can be arbitrarily worse. As a graph search on a finite graph it always finds a path when one exists. As a tree search it can loop forever. Doran and Michie used it in the Graph Traverser in 1966.

## In plain words

You walk in a city you do not know, toward a tall tower that you can see. At each corner you take the street that points most directly at the tower. You do not count how far you walked. Often this gets you there fast. But sometimes a street that points at the tower ends at a river, and you must walk back a long way. And sometimes you get to the tower by a long winding route, when a short one started in a direction that looked wrong.

If you mark each corner where you have been, you never walk in a circle, and in a city of finite size you reach the tower if any route goes there. If you do not mark corners, two corners that each look better than the other can keep you walking between them.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(n', c)$ of a next state and the nonnegative cost of the action to it, a goal test IS-GOAL, and a heuristic $h(n) \ge 0$. The output is some path from $s_0$ to a goal state with its cost, or *failure* when no goal can be reached. The method does not promise a cheapest path. We write $C^*$ for the cost of a cheapest one.

## The algorithm

```pseudo id=main
GREEDY-BEST-FIRST-SEARCH(s0, SUCCESSORS, IS-GOAL, h)
L1  make a node for s0 with g = 0 and parent nil
L2  OPEN ← { s0 } with key h(s0), REACHED ← { s0 }
L3  while OPEN ≠ ∅ do
L4      n ← the node of OPEN with least h, ties first in, first out; remove it
L5      if IS-GOAL(n) then return PATH(n), g(n)
L6      for each (n′, c) in SUCCESSORS(n) do
L7          if n′ ∉ REACHED then
L8              add n′ to REACHED
L9              put a node for n′ in OPEN with key h(n′), g = g(n) + c, parent n
L10 return failure
```

OPEN is the [open list](/open-list/), a [priority queue](/priority-queue/) keyed by $h$. REACHED holds each state that was ever put in OPEN, so a state enters OPEN at most once and keeps the first path found to it. This is the *graph search* form. The *tree search* form drops lines L7 and L8 and puts every successor in OPEN. The page [graph search versus tree search](/graph-search-vs-tree-search/) explains the general difference.

The value $g$ plays no part in the order. The code keeps it only to report the cost of the path. Because the order ignores $g$, it makes no sense to update the path of a state in REACHED when a cheaper path to it shows up: the search does not try to be cheap.

## Example

The graph has the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, and the goal is G. The heuristic is the Manhattan distance to G of the points S $(0,0)$, A $(2,0)$, B $(0,2)$, C $(2,2)$, D $(4,0)$, E $(0,4)$, F $(-1,0)$ and G $(4,2)$. It is [consistent](/consistent-heuristic/), and the same graph is the example of the page [A* search](/a-star-search/). Successors are listed in alphabetical order.

| state | S | A | B | C | D | E | F | G |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $h$ | 6 | 4 | 4 | 2 | 2 | 6 | 7 | 0 |

| step | removed ($h$) | put in OPEN | OPEN after the step ($h$) |
| --- | --- | --- | --- |
| 1 | S (6) | A, B, F | A 4, B 4, F 7 |
| 2 | A (4) | C, D (S is in REACHED) | C 2, D 2, B 4, F 7 |
| 3 | C (2) | G (A and B are in REACHED) | G 0, D 2, B 4, F 7 |
| 4 | G (0) | goal: return S-A-C-G, cost 8 | |

At step 2, A and B tie at $h = 4$ and the first in comes first. At step 3, G gets the parent C by way of A, at $g = 2 + 4 + 2 = 8$. The cheapest path S-B-C-G costs 7, and A* finds it after 5 expansions. Greedy best-first search made 3 expansions and returned a path that costs $8/7$ of the optimum.

**Arbitrarily bad paths.** Take the edges S→X 1, S→Y 1, X→G $M$ and Y→G 1, with $h(S) = 1$, $h(X) = 0$, $h(Y) = 1$ and $h(G) = 0$. This $h$ is consistent. The search expands S, then X, which puts G in OPEN with $g = 1 + M$, and then removes G. It returns cost $M + 1$ against $C^* = 2$, for each $M$.

**A loop in tree search.** Take the undirected unit-cost path A-S-B-C-D-G, with $h$ = 1, 2, 3, 2, 1, 0 on A, S, B, C, D, G. This $h$ is consistent. It equals the true distance to G at B, C, D and G, and it is lower at S and A. The tree search expands S, then A (key 1 against 3 for B), then the copy of S that A generates (key 2), then a copy of A, and so on: it alternates between S and A forever and never expands B. The graph search expands S, A, B, C, D and returns S-B-C-D-G.

**Measured on the 8-puzzle.** The script draws 20 instances from `random.Random(2024)`. Each one is a random walk of 60 moves from the goal, kept when breadth-first search gives an optimal depth $d \ge 14$. The depths are 14 to 24. With the Manhattan distance of the tiles as $h$, graph search with the tie rule of line L4 returned paths that cost $1.80 d$ on average and $19/7 \approx 2.71 d$ at most. It made 3,949 expansions in all, against 3,411 for A* with the same $h$. So on these instances the greedy order did not even save expansions.

## Correctness

The [proof](proofs/correctness.md) shows three facts about the graph search with nonnegative costs.

- **Valid answer.** A returned path goes from $s_0$ to a goal along actions of the graph, and $g$ is its cost.
- **Termination.** On a finite graph with $n$ reachable states the loop runs at most $n$ times, since each state enters OPEN at most once.
- **Completeness.** On a finite graph the search returns failure only when no goal can be reached. When the search ends with failure, every state in REACHED was expanded, so REACHED is closed under SUCCESSORS and holds every reachable state.

Nothing is claimed about the cost of the path. The examples above show that it can be any amount above $C^*$, even with a consistent $h$. On an infinite graph the graph search can also run forever, if $h$ leads it down an infinite path of states with small $h$.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ counted as $O(1)$, $n$ the number of states reachable from $s_0$ and $m$ the number of actions among them.

**Graph search.** Each state is put in OPEN at most once and removed at most once, so with a [binary heap](/binary-heap/) the heap work is $O(n \log n)$. Line L7 runs once for each action out of an expanded state, $O(m)$ in all with a [hash table](/hash-table/) for REACHED. The time is $O(m + n \log n)$ and the space is $O(n)$. If $h$ takes few distinct small integer values, a [bucket queue](/bucket-queue/) makes each heap step $O(1)$.

**Tree search.** On a graph with a cycle there is no bound, as the loop example shows. On a tree with branching factor $b$ and maximum depth $m'$ it can generate $O(b^{m'})$ nodes, the bound that Russell and Norvig give. A good $h$ makes the real numbers far smaller, but no worst case bound in terms of the error of $h$ is known for this method, unlike for A*.

These are worst case bounds. The speed of greedy best-first search in practice comes from the heuristic, and it can be poor: when $h$ is low in a region with no exit, as in front of a wall on a grid, the search expands the whole region before it leaves.

## Properties

- **Not optimal**, even with the perfect heuristic $h = h^*$, since the order ignores $g$. With the edges S→A 100, A→G 1, S→B 1 and B→G 50 and $h = h^*$, it expands A before B and returns S-A-G of cost 101, against $C^* = 51$.
- **Complete** as a graph search on finite graphs. Incomplete as a tree search on graphs with cycles, and incomplete on infinite graphs.
- **Not in place.** The graph search stores all reached states.
- **Deterministic**, with the tie rule of line L4.
- **Insensitive to costs.** Changing the action costs does not change the states it expands, only the reported cost.

## Variants and improvements

- **[A* search](/a-star-search/).** Order by $g + h$ instead of $h$. With an admissible $h$ the path is optimal.
- **[Weighted A*](/weighted-a-star/).** Order by $g + w h$. As $w$ grows, the order comes close to that of greedy best-first search, and the cost bound $w C^*$ gets weaker.
- **[Beam search](/beam-search/).** Keep only the $k$ best states of each layer. It saves memory and loses completeness.
- **[Hill climbing](/hill-climbing/).** Keep only one state and move to its best successor. It is greedy best-first search with OPEN of size one, and it stops at a local minimum of $h$.
- **[Limited discrepancy search](/limited-discrepancy-search/).** Follow the heuristic choice in a depth-first way, and allow a growing number of choices against it.
- **Distance instead of cost.** Use as $h$ an estimate of the number of actions to a goal instead of their cost. When costs vary a lot, this can find some path sooner.

## When to use it

Use greedy best-first search when any path will do, when you need it fast, and when the heuristic is good, for example in planning where the plan is checked later, or to get a first path for a method that improves it. Use graph search, not tree search, unless the state space is a tree. When the cost of the path matters, use A* or weighted A*, since a small change of order costs little and gives a bound on the cost.

## Pitfalls

- **Expecting a short path.** The path in the example costs 8, not 7, and the second example shows no bound at all. Do not use the cost of a greedy path as an estimate of $C^*$.
- **Tree search on a graph.** Two states that point at each other can trap the search, as in the loop example. Keep REACHED, or at least check the current path.
- **Updating the parent on a cheaper path.** It does no harm to correctness, but it does not make the method optimal, since the order still ignores $g$.
- **Goal test at generation.** It makes the search a little faster, and it is correct here, since no claim of optimality is lost. Do not copy this habit into A*.
- **A heuristic with large flat regions.** When many states share the least $h$, the tie rule decides the search, and first in, first out turns it into a breadth-first search over the flat region.

## Implementations

## History

Doran and Michie (1966) described the Graph Traverser, a program that develops the node of least heuristic value, and tested it on the 8-puzzle. This is greedy best-first search. Hart, Nilsson and Raphael (1968) added the cost $g$ to the order and got A*. Pohl (1970) studied the weighted sum of the two, which goes from A* to greedy best-first search as the weight on $h$ grows. The method is a standard baseline in planning, where a search guided only by $h$ is often the fastest way to find some plan.

## References
