---
tag: 6K9J0E
kind: algorithm
slug: a-star-search
name: A* search
aliases:
- A*
- algorithm A*
area: games-and-search/heuristic-search
level: intro
summary: Best-first search that expands the state of least f = g + h. With an admissible h it returns a cheapest path, and with a consistent h it expands each state at most once.
solves: [state-space-search, single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of states reachable from the start, m: the number of actions among them}
  time: {consistent: O(m log n), inconsistent: O(2^n n log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [best-first-search, uniform-cost-search, admissible-heuristic, open-list]
see_also: [a-star-optimality, optimal-efficiency-of-a-star, consistent-heuristic, dijkstra, potential-function-reduced-costs, iterative-deepening-a-star, weighted-a-star, alt-algorithm]
sources:
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (the algorithm A*, the proof that it is admissible when h is a lower bound, the consistency assumption, and the comparison of more informed algorithms)
  - paper: doi:10.1145/1056777.1056779
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, Correction to "A formal basis for the heuristic determination of minimum cost paths", SIGART Newsletter 37 (1972)
    locator: pp. 28 to 29 (the claim that the optimality result of the 1968 paper holds without the consistency assumption)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.5.2 (A* search, admissibility and consistency) and Section 3.5.3 (search contours)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (best-first search and A*), Chapter 3 (formal properties of A*) and Chapter 6 (the complexity of A* as a function of the error of h)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 2 (A*, its relation to Dijkstra's algorithm, and the reopening of states for heuristics that are not consistent)
  - paper: doi:10.1016/0004-3702(77)90002-9
    title: Alberto Martelli, On the complexity of admissible search algorithms, Artificial Intelligence 8(1) (1977)
    locator: pp. 1 to 13 (graphs on which A* with an admissible h makes exponentially many expansions, and algorithm B)
  - paper: doi:10.1016/j.artint.2011.02.001
    title: Ariel Felner, Uzi Zahavi, Robert Holte, Jonathan Schaeffer, Nathan Sturtevant and Zhifu Zhang, Inconsistent heuristics in theory and practice, Artificial Intelligence 175(9-10) (2011)
    locator: Section 4 (the worst case of A* with inconsistent heuristics, Martelli's family of graphs, and the size of edge costs that it needs)
---

A* search finds a cheapest path from a start state to a goal state. It is [best-first search](/best-first-search/) with the evaluation $f(n) = g(n) + h(n)$, where $g(n)$ is the cost of the best path to $n$ found so far and $h(n)$ is a [heuristic function](/heuristic-function/) that estimates the cost from $n$ to a goal. If $h$ never overestimates, that is if it is [admissible](/admissible-heuristic/), the first goal that A* removes from OPEN has the least cost. If $h$ is also [consistent](/consistent-heuristic/), A* expands each state at most once and is [Dijkstra's algorithm](/dijkstra/) on modified costs. A good $h$ makes A* expand far fewer states than [uniform-cost search](/uniform-cost-search/), which is A* with $h = 0$. Hart, Nilsson and Raphael introduced it in 1968.

## In plain words

You drive to a town you cannot see, and you have a map of the roads. For each road junction you know two things: how far you drove to get there, and roughly how far it is from there to the town in a straight line. You always go on from the junction where these two together are smallest. You do not care only about the road behind you, and you do not care only about the guess ahead of you. You care about the whole trip.

If your guess is never too large, you cannot miss a shorter route: a junction on the best route always looks at least as good as the town does at the end. The better your guesses, the fewer junctions you look at. With no guess at all, you look at every junction closer than the town.

## The problem

The input is a [state-space search](/state-space-search/) problem with costs: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(n', c)$ of a next state and the nonnegative cost of the action to it, and a goal test IS-GOAL. A heuristic function $h$ gives a number $h(n) \ge 0$ for each state. The output is a path from $s_0$ to a goal state of least total cost $C^*$, or *failure* when no goal can be reached. On an explicit graph with one goal this is the [single-pair shortest path](/single-pair-shortest-path/) problem.

We write $g^*(n)$ for the cost of a cheapest path from $s_0$ to $n$ and $h^*(n)$ for the cost of a cheapest path from $n$ to a goal. The heuristic is admissible if $h(n) \le h^*(n)$ for all $n$, and consistent if $h(n) \le c(n, n') + h(n')$ for each action and $h = 0$ at goals.

## The algorithm

```pseudo id=main
A-STAR(s0, SUCCESSORS, IS-GOAL, h)
L1  g[s0] ← 0, parent[s0] ← nil
L2  OPEN ← { s0 } with key f(s0) = h(s0), CLOSED ← ∅
L3  while OPEN ≠ ∅ do
L4      n ← the state of OPEN with least f, ties toward larger g; remove it
L5      if IS-GOAL(n) then return PATH(parent, n), g[n]
L6      add n to CLOSED
L7      for each (n′, c) in SUCCESSORS(n) do
L8          if n′ has no g or g[n] + c < g[n′] then
L9              g[n′] ← g[n] + c, parent[n′] ← n
L10             if n′ ∈ CLOSED then remove n′ from CLOSED      ▷ reopen
L11             put n′ in OPEN with key f(n′) = g[n′] + h(n′), or lower its key
L12 return failure
```

OPEN is the [open list](/open-list/), a [priority queue](/priority-queue/) keyed by $f$. CLOSED holds the expanded states, and together with the table $g$ it is the [duplicate detection](/duplicate-detection/) of the search: a state reached again by a path that is not cheaper is dropped at line L8. PATH follows the parent pointers from $n$ back to $s_0$.

Three details make this A* and not a near relative. The goal test is at line L5, when a state leaves OPEN, and not when it is generated. A state in CLOSED that gets a cheaper $g$ goes back to OPEN at line L10; with a consistent $h$ this never happens, and many programs then drop line L10. The tie rule of line L4 is free, because any rule keeps the result optimal, but toward larger $g$ is the usual choice, since among states of equal $f$ it prefers the one that is closer to a goal by the estimate.

## Example

The graph has the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, and the goal is G. Each state lies on a point of the plane, S at $(0,0)$, A at $(2,0)$, B at $(0,2)$, C at $(2,2)$, D at $(4,0)$, E at $(0,4)$, F at $(-1,0)$ and G at $(4,2)$, and each edge costs at least the Manhattan distance between its ends. So $h$ = the Manhattan distance to G is consistent. Its values are

| state | S | A | B | C | D | E | F | G |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $h$ | 6 | 4 | 4 | 2 | 2 | 6 | 7 | 0 |
| $h^*$ | 7 | 6 | 4 | 2 | 3 | 6 | 8 | 0 |

Successors are listed in alphabetical order. A cell $X\ g/f$ means that $X$ is in OPEN with these values.

| step | removed $g/f$ | what lines L7 to L11 do | OPEN after the step |
| --- | --- | --- | --- |
| 1 | S 0/6 | A, B, F get $g$ = 2, 3, 1 | A 2/6, B 3/7, F 1/8 |
| 2 | A 2/6 | C gets 6, D gets 5; S is not cheaper | B 3/7, D 5/7, C 6/8, F 1/8 |
| 3 | D 5/7 | G gets 8; A is not cheaper | B 3/7, C 6/8, F 1/8, G 8/8 |
| 4 | B 3/7 | C drops from 6 to 5, E gets 5 | C 5/7, G 8/8, F 1/8, E 5/11 |
| 5 | C 5/7 | G drops from 8 to 7 | G 7/7, F 1/8, E 5/11 |
| 6 | G 7/7 | goal: return S-B-C-G, cost 7 | |

At step 3, D and B tie at $f = 7$, and the tie rule takes D because its $g$ is larger. D is not on the best path, and G is now in OPEN with the wrong cost 8. A search that stopped when it generated a goal would return S-A-D-G of cost 8 here. A* waits until G leaves OPEN, and by then B and C have lowered its cost to 7. F and E have $f > 7 = C^*$, so A* never expands them.

The same graph with three heuristics gives these counts. "Expanded" counts line L6, "generated" counts the pairs of line L7, and "pushed" counts the entries put in OPEN, the start included.

| heuristic | expanded, in order | expanded | generated | pushed |
| --- | --- | --- | --- | --- |
| $h = 0$ (uniform-cost search) | S, F, A, B, D, C, E | 7 | 16 | 10 |
| Manhattan distance | S, A, D, B, C | 5 | 14 | 10 |
| $h = h^*$ | S, B, C | 3 | 9 | 7 |

All three return the same path. With $h = 0$, A* expands every state with $g^* < 7$, which is the behavior of Dijkstra's algorithm. With the perfect $h^*$, it expands only the best path. The heuristics [dominate](/heuristic-dominance/) one another in this order, and the sets of expanded states shrink.

## Correctness

The [proof](proofs/correctness.md) gives these facts for a graph with finite branching and nonnegative costs.

- **Optimal answer.** If $h$ is admissible and the search returns, the path goes from $s_0$ to a goal and costs $C^*$. The key lemma is that, until a goal is removed, OPEN holds a state $p$ on a cheapest path with $g[p] = g^*(p)$, so $f(p) \le C^*$, and a goal removed before it cannot have $g > C^*$.
- **Termination and completeness.** On a finite graph A* stops for each $h$, because each value of $g[n]$ is the cost of a path that repeats no state, and $g[n]$ only goes down. If a goal can be reached and $h$ is admissible, it returns a cheapest path, also on an infinite graph when each action costs at least some $\delta > 0$.
- **No reopening with a consistent $h$.** Each state leaves OPEN with $g = g^*$, so line L10 never runs, and the values $f$ of the removed states never go down.

The page [A* optimality](/a-star-optimality/) states the result as a theorem, with the sets of states that A* must and cannot expand. The page [optimal efficiency of A*](/optimal-efficiency-of-a-star/) shows that no admissible algorithm with the same information can expand fewer states, when $h$ is consistent.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ counted as $O(1)$, $n$ the number of states reachable from $s_0$ and $m$ the number of actions among them.

**Consistent $h$.** Each state is expanded at most once, so lines L7 to L11 run at most $m$ times in all. With a [binary heap](/binary-heap/) the time is $O(m \log n)$, with an [indexed priority queue](/indexed-priority-queue/) and [decrease-key](/decrease-key/), or with lazy deletion as in the code, where the heap holds at most $m + 1$ entries. With a [Fibonacci heap](/fibonacci-heap/) it is $O(m + n \log n)$. This is the cost of Dijkstra's algorithm, and for a good reason: with a consistent $h$, A* is Dijkstra's algorithm on the costs $c(u, v) - h(u) + h(v)$, which are nonnegative, as the page [potential functions and reduced costs](/potential-function-reduced-costs/) shows. The heuristic does not change the worst case. It changes which states come before the goal.

**Admissible $h$ that is not consistent.** States can be reopened, and Martelli (1977) built graphs with $i + 1$ states on which A* needs $O(2^i)$ expansions; this is the worst case, so the time bound is $O(2^n n \log n)$. Felner et al. (2011, Section 4) showed that such graphs need edge costs and values of $h$ that grow exponentially in the number of states, so with small integer costs the number of reopenings stays polynomial.

**Space.** A* keeps every generated state in OPEN or CLOSED, which is $O(n + m)$ words with lazy deletion and $O(n)$ with decrease-key. In practice memory runs out long before time does. On a tree with branching factor $b$, unit costs and a goal at depth $d$, A* with $h = 0$ generates $O(b^d)$ nodes. A better $h$ lowers the base of this growth, which the [effective branching factor](/effective-branching-factor/) measures. Pearl (1984, Chapter 6) showed, for a model of a uniform tree with one goal, that the number of expansions stays polynomial in $d$ only when the error $h^* - h$ grows at most like the logarithm of $h^*$. Errors proportional to $h^*$ leave it exponential.

## Properties

- **Admissible**, in the old sense: with an admissible $h$ it returns a cheapest path.
- **Complete** on finite graphs, and on infinite graphs with finite branching and costs bounded below by some $\delta > 0$.
- **Not in place.** It stores all generated states.
- **Deterministic.** The result depends on the tie rule only through which of several cheapest paths is returned.
- **Contours.** With a consistent $h$, A* expands all states with $g^* + h < C^*$, some with $g^* + h = C^*$, and none with $g^* + h > C^*$.

## Variants and improvements

- **Without reopening.** Drop line L10 and ignore a cheaper path to a CLOSED state. This is correct for a consistent $h$. For an admissible $h$ that is not consistent it can return a path that is too expensive; the page [graph search versus tree search](/graph-search-vs-tree-search/) gives an example.
- **[Pathmax](/pathmax/).** Raise $h$ of a child to $h(\text{parent}) - c$ when that is larger. The values $f$ along each path then never go down, but states can still need reopening.
- **[Weighted A*](/weighted-a-star/).** Use $f = g + w h$ with $w > 1$. It is faster and returns a path that costs at most $w C^*$.
- **[IDA*](/iterative-deepening-a-star/).** Depth-first search with a bound on $f$, raised in rounds. It uses memory linear in the depth. Other [memory-bounded searches](/memory-bounded-heuristic-search/) keep as many states as fit.
- **[Bidirectional heuristic search](/bidirectional-heuristic-search/).** Search from both ends with a heuristic in each direction.
- **[ALT](/alt-algorithm/).** A* on road maps with a heuristic built from distances to a few landmarks and the [triangle inequality](/triangle-inequality/).
- **Martelli's algorithm B.** When the least $f$ in OPEN is below the largest $f$ expanded so far, expand the state of least $g$ among those. It brings the worst case for inconsistent heuristics down to $O(n^2)$ expansions.
- **Better heuristics.** [Relaxation](/relaxation-heuristic/) and [pattern databases](/pattern-database/) give admissible heuristics for puzzles and planning.

## When to use it

Use A* when you need a cheapest path, you have an admissible heuristic that is not trivial, and the states that A* generates fit in memory. It is the standard method for path finding on game maps and grids, for planning with a cost model, and for puzzles of moderate size such as the 8-puzzle. For one source and many targets, or when no heuristic is known, use Dijkstra's algorithm. When memory is the limit, use IDA* or a memory-bounded search. When a good path is enough and time is short, use weighted A* or [greedy best-first search](/greedy-best-first-search/).

## Pitfalls

- **Goal test when a state is generated.** In the example it returns a path of cost 8 instead of 7. The goal test must be at line L5.
- **A heuristic that overestimates.** Then A* can return a path that is too expensive. Check $h \le h^*$, for example by solving small instances exactly.
- **Closing states with an inconsistent heuristic.** Without line L10, an admissible but inconsistent $h$ can give a wrong cost. Either keep the reopening or make sure that $h$ is consistent.
- **Comparing $f$ alone in the heap.** Then the entries of equal $f$ come out in any order, which is correct but can expand many more states in grids with many ties. Break ties toward larger $g$.
- **Stale heap entries.** A state whose $g$ dropped has an old entry in a lazy heap. Skip an entry whose $g$ is not the current one, or the state is expanded twice with the wrong cost.
- **Floating point costs.** With real coordinates, Euclidean distances and sums of costs are rounded, so $h$ can exceed $h^*$ by a tiny amount and ties become random. Use integers, or compare with a tolerance and accept a tiny loss of optimality.
- **Recomputing $h$.** An expensive $h$, such as a large pattern database lookup, should be computed once per state and stored.

## Implementations

## History

Hart, Nilsson and Raphael introduced A* in 1968 at the Stanford Research Institute, in work on the route planning of the Shakey robot. They defined admissibility, proved that A* is admissible when $h$ is a lower bound on $h^*$, and proved under a consistency assumption that A* expands no more states than any admissible algorithm that is no better informed. In a correction of 1972 in the SIGART Newsletter they claimed that the consistency assumption was not needed. Dechter and Pearl (1985) showed that this claim was false. Martelli (1977) showed that without consistency A* can make exponentially many expansions and gave algorithm B. Pearl's book (1984) gave the standard treatment of the formal properties of A* and of its complexity in terms of the error of $h$. Felner et al. (2011) showed that inconsistent heuristics, long avoided, are useful in practice.

## References
