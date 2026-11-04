---
tag: 921J83
kind: algorithm
slug: bidirectional-search
name: Bidirectional search
aliases:
- bidirectional breadth-first search
- meet-in-the-middle search
area: techniques/search-strategies
level: core
summary: Runs two searches, one forward from the start and one backward from the goal, until their frontiers meet.
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {b: the branching factor in each direction, d: the distance from the start to the goal, V: the number of vertices, E: the number of edges}
  time: {worst: O(b^(d/2)), best: O(1)}
  space: {extra: O(b^(d/2))}
properties: {deterministic: true, recursive: false}
prereqs: [breadth-first-search, search-frontier, hash-table]
see_also: [breadth-first-search, bidirectional-dijkstra, bidirectional-heuristic-search, iterative-deepening-search, search-strategy, single-pair-shortest-path, meet-in-the-middle-attack, rubiks-cube-problem]
sources:
  - paper: "Ira Pohl, Bi-directional search, Machine Intelligence 6, Edinburgh University Press (1971)"
    title: Bi-directional search
    locator: pp. 127 to 140 (bidirectional search for shortest paths, the rule that picks the side with the smaller frontier, and the heuristic version)
  - paper: doi:10.2172/4785039
    title: Ira Pohl, Bi-directional and heuristic search in path problems, Stanford Linear Accelerator Center report (1969)
    locator: the chapters on bidirectional search without heuristics and the stopping condition for shortest paths
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.4.5 (bidirectional search, the cost O(b^(d/2)), the need for predecessors, and the comparison table of Section 3.4)
---

Bidirectional search finds a path from a start state to a goal state by running two searches at once, a forward search from the start and a backward search from the goal, and it stops when the two meet. With breadth-first search on both sides and unit action costs, each side only has to reach about half of the distance $d$. So the search generates $O(b^{d/2})$ nodes instead of the $O(b^d)$ of one [breadth-first search](/breadth-first-search/), a saving that grows exponentially with $d$. It needs a single known goal state and a way to list the predecessors of a state, and it must store one of the two searches in full.

## In plain words

Two friends want to meet, and each stands in a city on a large road map. If one friend searches for the other alone, she must look at all roads up to the full distance between them. If both search at the same time, each one looks only half way, and they meet in the middle.

Each friend checks the towns that are one road further, then two roads, and so on. When a new town of one friend is a town that the other friend has already seen, they have a route: the way from the first friend to that town, then the way from that town to the second friend. To be sure that this route is the shortest, each friend must finish a full round of towns at the same distance before the next round starts.

## The problem

The input is a graph, given implicitly by two functions: SUCCESSORS$(u)$ lists the states one action after $u$, and PREDECESSORS$(v)$ lists the states $u$ with $v$ in SUCCESSORS$(u)$. There is a start state $s$ and a goal state $t$, and each action costs 1. The output is a path from $s$ to $t$ with the fewest actions, or failure when $t$ cannot be reached from $s$. This is the [single-pair shortest path](/single-pair-shortest-path/) problem for unit costs.

## The algorithm

Each side keeps a table of parents (its reached set, with the parent of each state) and a frontier that is one full layer of its breadth-first search. At each step, the side with the smaller frontier expands its whole layer. When a newly reached state is already in the other side's table, the two half-paths are joined.

```pseudo id=main
BIDIRECTIONAL-SEARCH(s, t, SUCCESSORS, PREDECESSORS)
L1  if s = t then return [s]
L2  parent_f ← { s ↦ nil };  parent_b ← { t ↦ nil }
L3  front_f ← [s];  front_b ← [t]
L4  while front_f and front_b are both non-empty do
L5      pick the side x ∈ {f, b} with the smaller frontier (f on a tie)
L6      next ← []
L7      for each u in front_x do
L8          for each v in NEIGHBOURS_x(u) do            ▷ SUCCESSORS for f, PREDECESSORS for b
L9              if v is in parent_x then continue
L10             parent_x[v] ← u
L11             if v is in the other side's table then return JOIN(v)
L12             append v to next
L13     front_x ← next
L14 return failure
```

JOIN$(v)$ follows *parent_f* from $v$ back to $s$, reverses that part, and then follows *parent_b* from $v$ to $t$. Each frontier is a complete layer when line L5 picks a side, and this is what makes the first meeting a shortest path, see Correctness.

## Example

The graph has the directed edges S→A, S→C, A→B, B→D, C→D, D→G, with start S and goal G. The shortest path is S-C-D-G with 3 actions, and S-A-B-D-G has 4.

| step | side | layer expanded | states reached | meeting |
| --- | --- | --- | --- | --- |
| 1 | forward (1 ≤ 1) | S | A, C | none |
| 2 | backward (2 > 1) | G | D | none |
| 3 | backward (2 > 1) | D | B, then C | C is in the forward table |

The search returns S-C-D-G. The rule of complete layers matters here. A version that alternates single nodes and stops at the first meeting goes wrong on this graph: the forward side expands S, the backward side expands G, the forward side expands A and reaches B, and then the backward side expands D and meets B first. It returns S-A-B-D-G, with 4 actions.

For a uniform tree with $b = 10$ in both directions and $d = 6$, one breadth-first search with the goal test at generation generates up to $10 + 100 + \cdots + 10^6 = 1{,}111{,}110$ nodes. Bidirectional search expands three layers on each side, and it generates at most $2 \times (10 + 100 + 1000) = 2{,}220$ nodes.

## Correctness

Write $d_s(v)$ for the least number of actions from $s$ to $v$, $d_t(v)$ for the least number from $v$ to $t$, and $d = d_s(t)$. The proof below shows these facts.

- **Layers are exact.** When line L5 runs, *parent_f* holds exactly the states with $d_s \le a$, and *front_f* the states with $d_s = a$, for some $a$. The same holds for the backward side with some $\beta$. This is the usual layer argument of breadth-first search.
- **No early meeting.** Until the search returns, the two tables share no state, because a shared state is detected at line L11 when the second side reaches it. If $d \le a + \beta$, a shortest path has a state at distance $\min(a, d)$ from $s$, which lies in both tables. So $d \ge a + \beta + 1$.
- **The meeting is a shortest path.** Say the forward side meets at $v$ while expanding layer $a$. Then $d_s(v) = a + 1$ and $d_t(v) \le \beta$, so JOIN gives a path of at most $a + 1 + \beta \le d$ actions, which is a path of exactly $d$ actions.
- **Failure is correct.** A frontier becomes empty only when its side has reached every state that it can reach without meeting the other side. A path from $s$ to $t$ would pass from the forward table to the backward table, and they would have met.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS and PREDECESSORS and each [hash table](/hash-table/) operation counted as $O(1)$ ($O(1)$ expected).

**Implicit graphs.** Let both directions have branching factor $b$, as in a uniform tree. The frontiers then have $b^a$ and $b^\beta$ states, so line L5 always picks the side with fewer layers, and $a$ and $\beta$ differ by at most 1. The search stops while it expands the layer that makes $a + \beta + 1 = d$, so each side expands at most $\lceil d/2 \rceil$ layers and generates at most $b + b^2 + \cdots + b^{\lceil d/2 \rceil}$ nodes. The time and the space are both $O(b^{d/2})$, against $O(b^d)$ for one breadth-first search. Each state is stored in a table, so the space is as large as the time. This is the main cost of the method.

**Explicit graphs.** Each side reaches each vertex at most once and reads each of its edges at most once, so the time and the space are $O(V + E)$, as for breadth-first search. There is no gain in the worst case: on a path graph with $s$ and $t$ at the two ends, the two sides together visit all vertices.

In the best case $s = t$, and the search does $O(1)$ work.

## Properties

- **Complete and optimal for unit costs**, with the rule of complete layers.
- **Needs PREDECESSORS.** The backward search must invert the actions. When the inverse is easy, as in puzzles with reversible moves or graphs with stored in-edges, this is no problem. When it is hard, the method does not apply.
- **Needs one explicit goal.** With many goal states, or a goal given only by a test, the backward search must start from all of them at once, or it cannot start at all.
- **Memory-bound.** One of the two tables must be complete for the membership test of line L11, so the space is $O(b^{d/2})$.
- **Picks the cheaper side.** Expanding the side with the smaller frontier, Pohl's rule, adapts to graphs in which one direction branches more than the other.

## Variants and improvements

- **[Bidirectional Dijkstra](/bidirectional-dijkstra/).** For non-negative costs. Each side keeps a priority queue, $\mu$ is the cost of the best meeting path seen so far, and the search stops when the least keys of the two queues add up to at least $\mu$. Stopping at the first meeting is wrong with costs.
- **[Bidirectional heuristic search](/bidirectional-heuristic-search/).** Each side uses a heuristic toward the other end. Pohl studied this case and showed that the two searches can pass each other without meeting early. Later methods, such as front-to-front search and searches that are guaranteed to meet in the middle, address this.
- **Memory-light versions.** Run [iterative deepening](/iterative-deepening-search/) on one side and keep only the other side's last layer, or use a [meet-in-the-middle attack](/meet-in-the-middle-attack/) style split, where the two halves are enumerated and matched.
- **Speed-up techniques for road maps.** Methods such as [contraction hierarchies](/contraction-hierarchies/) run a bidirectional search on a preprocessed graph.

## When to use it

Use bidirectional search for a shortest path between two given states in a large graph with equal action costs, when the predecessors are easy to list and the memory for $b^{d/2}$ states is available. Typical cases are puzzles with reversible moves, such as the [Rubik's cube](/rubiks-cube-problem/) and sliding-tile puzzles, and the distance between two people in a social network. With unequal costs, use bidirectional Dijkstra instead.

## Pitfalls

- **Stopping at the first meeting with partial layers.** Alternating single nodes and stopping at the first meeting can return a longer path, as in the example above. Expand complete layers, or keep the best meeting and use a proper stopping rule.
- **Stopping at the first meeting with costs.** With weighted edges, the first meeting is not a cheapest path in general. Use the stopping rule of bidirectional Dijkstra.
- **Wrong predecessors.** The backward search must use the reverse of the actions. Using SUCCESSORS on a directed graph searches the wrong graph.
- **Joining the path wrongly.** The forward half must be reversed, and the meeting state must appear once.
- **Infinite graphs with no path.** When $t$ cannot be reached, the search stops only when one side runs out of states. On an infinite graph, the side with the smaller frontier can grow for ever while the other side, which is finite, is never expanded again.
- **Ignoring the memory.** The space is as large as the time. Do not expect the linear memory of iterative deepening.

## Implementations

## History

Pohl studied bidirectional search in his 1969 Stanford thesis, published as a report, and in his 1971 paper "Bi-directional search". He gave the rule that expands the side with the smaller frontier, analysed the gain for shortest paths, and studied the version with heuristics, in which the two searches may miss each other. Bidirectional versions of Dijkstra's algorithm and of A* became a standard tool for route planning. Russell and Norvig list bidirectional search among the uninformed strategies, with the bound $O(b^{d/2})$.

## References
