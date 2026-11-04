---
tag: 81NJ23
kind: algorithm
slug: uniform-cost-search
name: Uniform-cost search
aliases:
- lowest-cost-first search
- Dijkstra as search
area: techniques/search-strategies
level: core
summary: Expands the frontier state with the smallest path cost so far; optimal for non-negative step costs.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {b: the branching factor, C: the cost C* of a cheapest solution, e: the least action cost ε > 0, V: the number of reachable states, E: the number of transitions from them}
  time: {worst: O(b^(1 + ⌊C/e⌋) (1 + C/e) log b), best: O(1)}
  space: {extra: O(b^(1 + ⌊C/e⌋))}
properties: {deterministic: true, recursive: false}
prereqs: [best-first-search, priority-queue, search-frontier, graph-search-vs-tree-search]
see_also: [dijkstra, breadth-first-search, a-star-search, best-first-search, iterative-deepening-search, completeness-and-optimality-of-search, bidirectional-search, binary-heap]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.4.2 (Dijkstra's algorithm or uniform-cost search, with the bound O(b^(1+⌊C*/ε⌋))) and Section 3.3.1 (the best-first search skeleton)
  - paper: doi:10.1609/socs.v2i1.18191
    title: Ariel Felner, Position paper, Dijkstra's algorithm versus uniform cost search or a case against Dijkstra's algorithm, Proceedings of SoCS 2011
    locator: pp. 47 to 51 (the two formulations and why the search form needs no initialization of all vertices)
  - paper: doi:10.1007/BF01386390
    title: E. W. Dijkstra, A note on two problems in connexion with graphs, Numerische Mathematik 1 (1959)
    locator: pp. 269 to 271 (the second problem, a shortest path between two given nodes)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.3 (Dijkstra's algorithm, its correctness proof and its cost with a binary heap)
---

Uniform-cost search finds a cheapest path from a start state to a goal state by always expanding the [frontier](/search-frontier/) node of least path cost $g$. It is [best-first search](/best-first-search/) with the evaluation function $f = g$, and it is [Dijkstra's algorithm](/dijkstra/) written as a search: it starts with only the start state, generates the other states on demand, and stops when it selects a goal. With non-negative action costs it is cost-optimal. With a finite branching factor and action costs of at least some $\epsilon > 0$ it is also complete, and it generates $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$ nodes.

## In plain words

You look for the cheapest trip from home to any shop. You keep a list of places you can reach, each with the cheapest price you know to get there. At each step you take the place with the lowest price from the list. If it is a shop, you stop. If not, you look at each road out of it, and you add the place at the other end with the new price, when this price is better than the one you know.

Because you always take the cheapest place first, you take the places in order of price. So the first shop that you take is a cheapest shop. A shop that you see early on an expensive road is not taken until all cheaper places are done.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives, for a state $s$, the finite list of pairs $(s', c)$ of a next state and the cost $c \ge 0$ of the action, and a goal test IS-GOAL. The states must be hashable. Let $\delta(s)$ be the least cost of a path from $s_0$ to $s$. The output is a path from $s_0$ to a goal $t$ with cost $C^* = \min_{t \text{ goal}} \delta(t)$, or failure when no goal can be reached. The state space may be infinite and given only by SUCCESSORS.

## The algorithm

A node holds a state, a parent node and the path cost $g$. The frontier is a min-[priority queue](/priority-queue/) on $g$. The table *reached* maps each state seen so far to its cheapest known node. A cheaper path to a state adds a second node for it, and the old node becomes *stale*: it stays in the queue and is skipped when it comes out (lazy insertion, no decrease-key).

```pseudo id=main
UNIFORM-COST-SEARCH(s0, SUCCESSORS, IS-GOAL)
L1  node ← NODE(state = s0, parent = nil, g = 0)
L2  frontier ← a min-priority queue on g, holding node
L3  reached ← { s0 ↦ node }
L4  while frontier is not empty do
L5      n ← POP-MIN(frontier)
L6      if n.g > reached[n.state].g then continue        ▷ stale node
L7      if IS-GOAL(n.state) then return PATH(n), n.g    ▷ late goal test
L8      for each (s', c) in SUCCESSORS(n.state) do
L9          g' ← n.g + c
L10         if s' is not in reached or g' < reached[s'].g then
L11             reached[s'] ← NODE(state = s', parent = n, g = g')
L12             PUSH(frontier, reached[s'])
L13 return failure
```

PATH$(n)$ follows the parent pointers from $n$ to the root and returns the states in order from $s_0$. Line L7 tests for the goal when a node leaves the frontier, not when it enters it. This is the condition for optimality. Line L10 is the graph-search rule of [graph search versus tree search](/graph-search-vs-tree-search/): a state is added again only on a strictly cheaper path. Line L6 skips the nodes made stale by a later, cheaper node. Without it the search is still correct, but it expands some states more than once.

## Example

The graph has the directed edges S→A 1, S→G 12, A→B 4, A→C 1, B→D 3, C→D 1, C→G 2, D→G 3. The start is S and G is the only goal. The frontier is written as path:$g$, with the least $g$ first.

| step | frontier before POP-MIN | popped | what happens | reached after the step |
| --- | --- | --- | --- | --- |
| 1 | S:0 | S:0 | push A:1 and G:12 | S 0, A 1, G 12 |
| 2 | S-A:1, S-G:12 | S-A:1 | push B:5 and C:2 | S 0, A 1, G 12, B 5, C 2 |
| 3 | S-A-C:2, S-A-B:5, S-G:12 | S-A-C:2 | D:3 is new; G:4 is less than 12, so push it | S 0, A 1, G 4, B 5, C 2, D 3 |
| 4 | S-A-C-D:3, S-A-C-G:4, S-A-B:5, S-G:12 | S-A-C-D:3 | G:6 is not less than 4, so no push | unchanged |
| 5 | S-A-C-G:4, S-A-B:5, S-G:12 | S-A-C-G:4 | goal, return S-A-C-G with cost 4 | |

The search returns the path S-A-C-G with cost 4. The goal was reached with cost 12 already at step 1, but the node S-G:12 stays in the queue behind cheaper nodes. At step 3 it becomes stale. A search that tested for the goal at step 1, when G was generated, would return the path S-G with cost 12.

## Correctness

Let the action costs be non-negative. The key fact is a statement about each node that is popped and not stale:

> When a node $n$ is popped at line L5 and passes line L6, $n.g \le \delta(t)$ for each state $t$ that was not expanded before.

Applied to $t = n.state$, it gives $n.g = \delta(n.state)$, because $n.g$ is the cost of a real path. Applied to all goals, it shows that the first goal popped has cost $C^*$. The proof takes a cheapest path to $t$ and finds a node on it in the frontier with cost at most $\delta(t)$. For completeness, with costs at least $\epsilon > 0$ and a finite branching factor, each node popped before the goal has $g \le C^*$, and there are only finitely many paths of cost at most $C^*$. The full proof is below.

## Complexity

The costs are in the [word RAM](/word-ram/). A call of IS-GOAL, the generation of one successor, and a lookup or update of *reached* each count as $O(1)$; for a hash table the last is $O(1)$ expected time.

**Implicit space, tree measure.** Let $b$ be the branching factor, $\epsilon > 0$ the least action cost and $C^*$ the cost of a cheapest solution. Each node popped before the goal has $g \le C^*$, so it is a path of at most $\lfloor C^*/\epsilon \rfloor$ actions. The nodes generated are these nodes and their children, so they are paths of at most $1 + \lfloor C^*/\epsilon \rfloor$ actions, and there are at most

$$ \sum_{i=0}^{1 + \lfloor C^*/\epsilon \rfloor} b^i = O\left(b^{1 + \lfloor C^*/\epsilon \rfloor}\right) $$

of them for $b \ge 2$. Each push and pop on a [binary heap](/binary-heap/) costs $O(\log N)$, where $N$ is the number of nodes generated. The time is $O(N \log N)$ and the space is $O(N)$, with $N = O(b^{1 + \lfloor C^*/\epsilon \rfloor})$, so $\log N = O((1 + C^*/\epsilon) \log b)$. When all actions cost the same, $\lfloor C^*/\epsilon \rfloor = d$, and the bound is $O(b^{d+1})$, one level more than [breadth-first search](/breadth-first-search/) needs, because of the late goal test. The bound is in the worst case. When many actions are much cheaper than $C^*$ and $\epsilon$ is small, $C^*/\epsilon$ is much larger than $d$, and uniform-cost search can explore many cheap, useless paths before it reaches a deep goal.

**Explicit graph.** On a graph with $V$ reachable states and $E$ transitions, each state is expanded at most once (line L6 skips the stale nodes, and the first non-stale pop of a state has its final cost). Each transition causes at most one push. So the heap holds at most $E + 1$ nodes, and the time is $O((V + E) \log V)$, as for Dijkstra's algorithm with a binary heap. The space is $O(V + E)$.

**Best case.** If the start state is a goal, the search does one pop, no expansion and $O(1)$ work.

## Properties

- **Cost-optimal** for non-negative action costs, with the late goal test of line L7.
- **Complete** when the branching factor is finite and each action cost is at least some $\epsilon > 0$. On a finite space it is complete with failure detection for non-negative costs.
- **Systematic.** It expands states in non-decreasing order of $\delta$, in contours of equal cost.
- **Uninformed.** It uses only $g$, no estimate of the distance to the goal.
- **Same as breadth-first search for unit costs**, in the order of the expanded states, except for the time of the goal test and the order of ties.

## Variants and improvements

- **Decrease-key.** Keep one node for each state, and lower its key in the queue when a cheaper path is found. With a Fibonacci heap this gives Dijkstra's bound $O(E + V \log V)$ on explicit graphs. In practice lazy insertion with a binary heap is simpler.
- **Buckets.** With small integer costs, a bucket queue (Dial's method) gives $O(1)$ amortized queue operations.
- **[A* search](/a-star-search/).** Order the frontier by $g + h$, with an admissible heuristic $h$. Uniform-cost search is A* with $h = 0$.
- **[Bidirectional search](/bidirectional-search/).** Run one uniform-cost search from the start and one backward from the goal. The stopping rule must compare the best meeting cost with the two queue minima.
- **Uniform-cost tree search.** Drop the table *reached*. The memory then holds only the frontier, but states are repeated, and the search may not stop when no goal exists.
- **Iterative lengthening.** Repeat a depth-first search with an increasing bound on $g$ instead of on the depth. It uses little memory but can repeat much work when the costs are all different.

## When to use it

Use uniform-cost search when actions have different non-negative costs, you need a cheapest path, and no useful heuristic is known. With a good admissible heuristic, A* finds the same cost with fewer expansions. With equal costs, [breadth-first search](/breadth-first-search/) is simpler and can test the goal at generation. When memory is the limit, [iterative deepening search](/iterative-deepening-search/) (for equal costs) or a memory-bounded best-first search uses far less memory. On an explicit graph where all distances from the source are needed, the textbook [Dijkstra's algorithm](/dijkstra/) is the same method run to the end.

## Pitfalls

- **Goal test at generation.** Testing IS-GOAL on $s'$ inside the loop of line L8 returns the first goal generated, which in the example costs 12 instead of 4. Test at line L7.
- **Negative costs.** With a negative action cost, a state popped at line L5 can later be reached by a cheaper path, and the first goal popped need not be cheapest. Use Bellman-Ford for negative costs without negative cycles.
- **Zero-cost cycles and costs without a lower bound.** Optimality only needs $c \ge 0$, but completeness on an infinite space needs $c \ge \epsilon > 0$. With costs $2^{-i}$ along an infinite chain, the costs of the chain stay below 1, and a goal of cost 1 is never popped.
- **A non-strict test at line L10.** With $g' \le$ instead of $g' <$, a zero-cost cycle pushes the same state again and again, and the loop may not stop.
- **Updating the old node in place.** Changing $g$ of a node that is already in a binary heap, without a decrease-key operation, breaks the heap order. Push a new node instead, and skip the old one at line L6.

## Implementations

## History

Dijkstra published the algorithm in 1959, for a shortest path between two given nodes of a graph, and it grows a set of nodes whose distance is final in order of distance. The AI literature calls the form that starts from one state, generates the graph on demand and stops at a goal uniform-cost search, as in Russell and Norvig. Felner (2011) compared the two forms and argued that the search form, which never initializes all vertices, is the better one to teach and to use on large or implicit graphs.

## References
