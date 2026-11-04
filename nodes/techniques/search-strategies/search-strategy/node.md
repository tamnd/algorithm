---
tag: V8EJDX
kind: concept
slug: search-strategy
name: Search strategy
aliases:
- search algorithm
- state-space search strategy
area: techniques/search-strategies
level: intro
summary: A rule that fixes the order in which a search explores the states of a space.
prereqs: [state-space, state-space-search]
see_also: [search-frontier, search-tree, graph-search-vs-tree-search, completeness-and-optimality-of-search, breadth-first-search, depth-first-search, uniform-cost-search, best-first-search]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Sections 3.3 (search algorithms, best-first search and the measures of performance) and 3.4 (uninformed search strategies, with the comparison table at the end of the section)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (basic heuristic-search procedures)
  - paper: doi:10.1145/3828.3830
    title: Rina Dechter and Judea Pearl, Generalized best-first search strategies and the optimality of A*, Journal of the ACM 32(3) (1985)
    locator: pp. 505 to 536 (best-first search with a general evaluation function)
---

A search strategy is the rule that decides which state a [state-space search](/state-space-search/) explores next. Each systematic search keeps a [frontier](/search-frontier/) of states that it has reached but not yet expanded, and the strategy is the rule that picks the next one from it. The choice of rule fixes the main properties of the search: whether it finds a solution when one exists, whether the solution is a cheapest one, and how much time and memory it uses. [Breadth-first search](/breadth-first-search/), [depth-first search](/depth-first-search/), [uniform-cost search](/uniform-cost-search/) and A* are four strategies on the same skeleton.

## In plain words

You are lost in a building and you look for the exit. You keep a list of doors that you know about but have not yet opened. At each step you choose one door from the list, open it, and add the new doors that you see behind it. You stop when you find the exit.

The program is the same for every search. Only the choice of the next door changes. If you always open the oldest door on the list, you check all rooms near the start before rooms far away. If you always open the newest door, you go deep into one corridor before you try another. If you always open the door that is cheapest to reach, you find the cheapest way out. This rule for the choice is the search strategy.

## The idea

### The problem

A search problem has a set of states, an initial state $s_0$, for each state $s$ a finite set of actions, a transition model that gives the state $\mathrm{RESULT}(s, a)$, an action cost $c(s, a, s') \ge 0$, and a goal test. A solution is a sequence of actions from $s_0$ to a goal state. Its cost is the sum of the action costs. A cheapest solution has cost $C^*$. The set of states with the transitions is the [state space](/state-space/), and the problem is [state-space search](/state-space-search/).

### The skeleton

Each systematic search below works on nodes. A node holds a state, a pointer to its parent node, the action that made it, and the path cost $g(n)$ from $s_0$. To *expand* a node means to generate one child node for each action of its state.

```pseudo id=main
GENERIC-SEARCH(problem, SELECT)
L1  frontier ← { node(s0) }
L2  while frontier is not empty do
L3      n ← SELECT(frontier)                ▷ the strategy
L4      remove n from frontier
L5      if IS-GOAL(n.state) then return the path of n
L6      for each child c of n do
L7          if c is allowed by the duplicate rule then add c to frontier
L8  return failure
```

The strategy is the function SELECT of line L3, together with the duplicate rule of line L7. Most strategies are fixed by the data structure of the frontier:

| frontier | SELECT returns | strategy |
| --- | --- | --- |
| FIFO queue | the oldest node | [breadth-first search](/breadth-first-search/) |
| LIFO stack | the newest node | [depth-first search](/depth-first-search/) |
| [priority queue](/priority-queue/) on $g(n)$ | a node of least path cost | [uniform-cost search](/uniform-cost-search/) |
| priority queue on $h(n)$ | a node that looks closest to a goal | [greedy best-first search](/greedy-best-first-search/) |
| priority queue on $g(n) + h(n)$ | a node of least estimated total cost | [A* search](/a-star-search/) |

Here $h$ is a [heuristic function](/heuristic-function/), an estimate of the cost from a state to a goal. A priority queue on a general evaluation function $f$ gives [best-first search](/best-first-search/), and the last three rows are special cases of it. Breadth-first search is also best-first search with $f$ equal to the depth.

The duplicate rule is the second part. [Tree-like search](/graph-search-vs-tree-search/) has no rule: it may add the same state many times, once for each path. Graph search keeps a table of reached states and adds a child only when its state is new, or when the new path is cheaper. The page [graph search versus tree search](/graph-search-vs-tree-search/) compares them. The nodes that the skeleton can generate form the [search tree](/search-tree/); a strategy is an order in which to visit it.

A strategy can also change the skeleton. [Depth-limited search](/depth-limited-search/) cuts the search tree at a fixed depth. [Iterative deepening search](/iterative-deepening-search/) runs depth-limited search again and again with a larger limit. [Iterative broadening](/iterative-broadening/) limits the number of children instead of the depth. [Bidirectional search](/bidirectional-search/) runs two frontiers, one from the start and one from the goal.

### The measures

Four measures compare strategies. They are defined on the page [completeness and optimality of search](/completeness-and-optimality-of-search/).

- **Completeness.** The search finds a solution whenever one exists, and reports failure when none exists.
- **Cost optimality.** The solution it returns has cost $C^*$.
- **Time.** The number of nodes generated or expanded.
- **Space.** The largest number of nodes kept in memory at the same time.

In an implicit space, the time and the space are given in the branching factor $b$ (the largest number of children of a node), the depth $d$ of a shallowest goal, the largest depth $m$ of the search tree, the cost $C^*$ and the least action cost $\epsilon > 0$. The table gives the standard values for the tree-like versions, as in Russell and Norvig, Section 3.4. Each claim of completeness assumes $b$ finite.

| strategy | complete | cost-optimal | time | space |
| --- | --- | --- | --- | --- |
| breadth-first | yes | if all action costs are equal | $O(b^d)$ | $O(b^d)$ |
| uniform-cost | if each cost is at least $\epsilon > 0$ | yes | $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$ | $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$ |
| depth-first | no | no | $O(b^m)$ | $O(bm)$ |
| depth-limited, limit $\ell$ | no | no | $O(b^\ell)$ | $O(b\ell)$ |
| iterative deepening | yes | if all action costs are equal | $O(b^d)$ | $O(bd)$ |
| bidirectional (breadth-first both ways) | yes | if all action costs are equal | $O(b^{d/2})$ | $O(b^{d/2})$ |

Depth-first search is complete on a finite state space when it uses graph search or a check for cycles on the current path. It is not complete on an infinite space, where it can follow one infinite path for ever.

### Uninformed and informed

A strategy is *uninformed*, or blind, when SELECT uses only the problem definition: the path, its cost and its depth. It is *informed*, or heuristic, when it also uses an estimate $h$ of the distance to a goal. Breadth-first, depth-first, uniform-cost, depth-limited, iterative deepening and bidirectional search are uninformed. Greedy best-first search and A* are informed.

### Systematic and local

The strategies above are *systematic*: they keep enough of the search tree to visit each node, or each state, at most once in an order that is fixed in advance, and so they can prove that no solution exists. A *local* strategy keeps only one state, or a few states, and moves to a neighbour at each step. [Hill climbing](/hill-climbing/), [simulated annealing](/simulated-annealing/) and local [beam search](/beam-search/) are local. They use little memory and work on very large spaces, but they are not complete in general. Their problem is the [local search problem](/local-search-problem/).

## Examples

### One graph, four strategies

The graph has the states S, A, B, C, D and G. The start is S and the goal is G. The directed edges and their costs are

S→A 1, S→G 12, A→B 4, A→C 1, B→D 3, C→D 1, C→G 2, D→G 3.

The paths from S to G are S-G (cost 12, 1 action), S-A-C-G (cost 4, 3 actions), S-A-C-D-G (cost 6) and S-A-B-D-G (cost 11). So the cheapest cost is $C^* = 4$ and the shallowest goal has depth $d = 1$. Children are listed in the order of the edge list.

| strategy | nodes expanded, in order | path returned | its cost |
| --- | --- | --- | --- |
| breadth-first, goal test when a node is generated | S | S-G | 12 |
| depth-first, the first child first | S, A, B, D | S-A-B-D-G | 11 |
| uniform-cost, goal test when a node is selected | S, A, C, D | S-A-C-G | 4 |
| greedy best-first, $h$ = (S 4, A 3, B 1, C 2, D 1, G 0) | S | S-G | 12 |

Breadth-first search returns the path with the fewest actions. It is the cheapest only when all actions cost the same. Depth-first search returns the first path that it meets on its way down. Uniform-cost search returns the cheapest path, after it expands each node with $g$ less than 4. Greedy best-first search goes to the state that looks closest to the goal, here G itself, and does not look at the cost of the edge.

The run of uniform-cost search shows the frontier, with the path cost of each node:

| step | frontier before the step | node selected |
| --- | --- | --- |
| 1 | S:0 | S |
| 2 | S-A:1, S-G:12 | S-A |
| 3 | S-A-C:2, S-A-B:5, S-G:12 | S-A-C |
| 4 | S-A-C-D:3, S-A-C-G:4, S-A-B:5, S-G:12 | S-A-C-D |
| 5 | S-A-C-G:4, S-A-B:5, S-G:12 | S-A-C-G, a goal |

At step 4 the child S-A-C-D-G has cost 6. A graph search does not add it, because G is already reached with cost 4.

### The same strategy with a different duplicate rule

Add the edge D→A with cost 1, and list it before D→G. The graph now has the cycle A, B, D, A. Depth-first tree-like search with the first child first expands S, A, B, D, then the child A of D, then B, D, A again, and so on: it never reaches G. A graph search does not add the second A, because A is already reached. A check that a child is not already on the current path also stops the loop. If the children are taken last first, the same tree-like search expands S and then selects S-G at once. So on a space with cycles, the order of the children and the duplicate rule decide whether depth-first search stops.

## Where it is used

Search strategies are the core of classical AI problem solving, of route finding on road maps and game maps, of planning, of puzzle solvers, and of the exploration of the states of a program in model checking. The same choice of order appears outside AI. The traversals of an explicit graph, [breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/), are the uninformed strategies with graph search. [Dijkstra's algorithm](/dijkstra/) is uniform-cost search on an explicit graph. [Backtracking](/generic-backtracking-algorithm/) is depth-first search on the [state-space tree](/state-space-tree/) of partial solutions, and [branch and bound](/best-first-branch-and-bound/) chooses a node selection rule in the same way. The pages of this area treat the parts in turn: the [frontier](/search-frontier/), the [search tree](/search-tree/), [graph search versus tree search](/graph-search-vs-tree-search/), and the measures of [completeness and optimality](/completeness-and-optimality-of-search/).

## References
