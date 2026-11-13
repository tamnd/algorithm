---
tag: C7VG9R
kind: algorithm
slug: bidirectional-heuristic-search
name: Bidirectional heuristic search
aliases:
- bidirectional A*
- BHPA*
area: games-and-search/heuristic-search
level: advanced
summary: Runs a heuristic search forward from the start and one backward from the goal, and stops when no path cheaper than the best meeting can remain. MM orders both by max(f, 2g) so they meet in the middle.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {n: the number of states that the two searches see, b: the largest number of successors or predecessors of a state}
  time: {per-expansion: O(b log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1971
  people: [Ira Pohl, Dennis de Champeaux, Lenie Sint, Hermann Kaindl, Gerhard Kainz, Robert C. Holte, Ariel Felner, Guni Sharon, Nathan R. Sturtevant]
  note: Pohl gave the first bidirectional heuristic search in 1971. In 2016 Holte, Felner, Sharon and Sturtevant gave MM, the first one that is sure to meet in the middle.
prereqs: [a-star-search, bidirectional-search, admissible-heuristic]
see_also: [bidirectional-dijkstra, consistent-heuristic, pattern-database, sliding-tile-puzzle, rubiks-cube-problem, duplicate-detection, open-list]
sources:
  - paper: Ira Pohl, Bi-directional search, Machine Intelligence 6 (1971)
    locator: pp. 127 to 140 (the bidirectional heuristic path algorithm, its stopping rule and the cardinality rule for the choice of direction)
  - paper: doi:10.1145/322003.322004
    title: Dennis de Champeaux and Lenie Sint, An improved bidirectional heuristic search algorithm, Journal of the ACM 24(2) (1977)
    locator: pp. 177 to 191 (front-to-front heuristics, which estimate the cost between a node and the nodes of the other frontier)
  - paper: doi:10.1613/jair.460
    title: Hermann Kaindl and Gerhard Kainz, Bidirectional heuristic search reconsidered, Journal of Artificial Intelligence Research 7 (1997)
    locator: pp. 283 to 317 (why bidirectional heuristic search often did not pay, and the work after the frontiers meet)
  - paper: doi:10.1609/aaai.v30i1.10436
    title: Robert C. Holte, Ariel Felner, Guni Sharon and Nathan R. Sturtevant, Bidirectional search that is guaranteed to meet in the middle, Proceedings of the 30th AAAI Conference on Artificial Intelligence (AAAI-16)
    locator: pp. 3411 to 3417 (MM, the priority max(f, 2g), the stopping rule, and the proofs that MM is optimal and meets in the middle)
  - paper: doi:10.1609/icaps.v27i1.13825
    title: Jürgen Eckerle, Jingwei Chen, Nathan R. Sturtevant, Sandra Zilles and Robert C. Holte, Sufficient conditions for node expansion in bidirectional heuristic search, Proceedings of the 27th International Conference on Automated Planning and Scheduling (ICAPS 2017)
    locator: pp. 79 to 87 (the pairs of forward and backward nodes that every admissible front-to-end bidirectional search must expand)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition
    locator: Section 3.5.6 (bidirectional heuristic search, front-to-end and front-to-front heuristics, and the priority of MM)
---

Bidirectional heuristic search finds a cheapest path from a start $s$ to a goal $t$ with two [A*](/a-star-search/)-like searches at the same time: a forward search from $s$ with a heuristic $h_F$ that estimates the cost to $t$, and a backward search from $t$ over the predecessors with a heuristic $h_B$ that estimates the cost from $s$. Each time one search generates a state that the other one has seen, the two half paths give a path from $s$ to $t$, and the best of these, $U$, is an upper bound. The search stops when it can show that no path cheaper than $U$ remains. Plain [bidirectional search](/bidirectional-search/) does this without heuristics and can save a lot. With a good heuristic, early versions often did more work than A*, because each search went far past the middle before the stopping rule held. MM, by Holte, Felner, Sharon and Sturtevant (2016), orders each search by $\max(f, 2g)$, so that neither one expands a state with $g$ above $C^*/2$. This page gives MM.

## In plain words

Two friends look for the shortest road between their towns. One starts from each town, and each one has a rough idea of how far the other town is.

Each friend always walks to the next place that looks most promising. Each one also avoids getting more than halfway from home on the best possible road. When one of them reaches a place the other has already visited, they have a full road between the towns.

They do not stop at once, since a shorter road could still exist. They stop when every place still left to try is too far to give a shorter road than the one they have.

## The problem

The input is a start state $s$, a goal state $t$, the functions SUCCESSORS and PREDECESSORS that give the actions out of and into a state with their positive costs, a forward heuristic $h_F$ with $h_F(u)$ at most the cost of a cheapest path from $u$ to $t$, a backward heuristic $h_B$ with $h_B(u)$ at most the cost of a cheapest path from $s$ to $u$, and a number $\epsilon \ge 0$ that is at most the cost of each action. The output is a cheapest path from $s$ to $t$, or *failure* when there is none. The goal is one state, not a goal test, because the backward search must start somewhere.

## The algorithm

In each direction $D$, a state $n$ has the value $g_D(n)$, the cost $f_D(n) = g_D(n) + h_D(n)$ and the priority $pr_D(n) = \max(f_D(n), 2\,g_D(n))$. Let $\mathit{prmin}_D$, $\mathit{fmin}_D$ and $\mathit{gmin}_D$ be the least values of $pr_D$, $f_D$ and $g_D$ over $\mathrm{OPEN}_D$.

```pseudo id=main
MM(s, t, SUCCESSORS, PREDECESSORS, hF, hB, ε)
L1  gF[s] ← 0, OPEN_F ← {s}; gB[t] ← 0, OPEN_B ← {t}
L2  U ← 0 if s = t, else ∞
L3  while OPEN_F and OPEN_B are not empty do
L4      C ← min(prmin_F, prmin_B)
L5      if U ≤ max(C, fmin_F, fmin_B, gmin_F + gmin_B + ε) then leave the loop
L6      D ← the direction with prmin_D = C, forward on a tie; n ← a state of OPEN_D with pr_D(n) = C, ties to the smaller g
L7      move n from OPEN_D to CLOSED_D
L8      for each action (m, c) of n in direction D do               ▷ successors forward, predecessors backward
L9          if m has a value gD[m] ≤ gD[n] + c then skip m
L10         take m out of OPEN_D and CLOSED_D
L11         gD[m] ← gD[n] + c; parentD[m] ← n; put m in OPEN_D
L12         if m has a value g in the other direction and gD[m] + g_other[m] < U then U ← that sum; MEET ← m
L13 if U = ∞ then return failure
L14 return the forward path from s to MEET, then the backward path from MEET to t
```

**The priority.** A* in one direction expands every state with $f < C^*$. In a bidirectional search, a state far from its own start, with $g > C^*/2$, is not needed: a cheapest path of cost $C^*$ has a point where the cost from $s$ and the cost to $t$ are both at most $C^*/2$. The term $2g$ in the priority keeps such states back until the end, so the two searches meet near the middle of the cheapest path.

**The stopping rule.** Each of the four terms at line L5 is a lower bound on the cost of any path that the search has not found yet: $C$ by the meeting argument above, $\mathit{fmin}_F$ and $\mathit{fmin}_B$ by admissibility, and $\mathit{gmin}_F + \mathit{gmin}_B + \epsilon$ because such a path must leave both open lists and use at least one more action. The paper states the rule with all four terms. Line L12 updates $U$ when $m$ has a value in the other direction, open or closed. The paper tests only the other open list. The test here can only find a path sooner, and the proof on this site uses it.

## Example

The graph is the one of the page [A* search](/a-star-search/): the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, the start S and the goal G, with $C^* = 7$. The states have the grid positions S (0, 0), A (2, 0), B (0, 2), C (2, 2), D (4, 0), E (0, 4), F (−1, 0) and G (4, 2). The heuristic $h_F$ is the Manhattan distance to G and $h_B$ the Manhattan distance to S. The neighbors are taken in alphabetical order, and $\epsilon = 0$.

| step | $C$ | stopping bound | expands | new values | $U$ |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 6 | forward S, $g = 0$ | $g_F$: A 2, B 3, F 1 | ∞ |
| 2 | 6 | 6 | forward A, $g = 2$ | $g_F$: C 6, D 5 | ∞ |
| 3 | 6 | 7 | backward G, $g = 0$ | $g_B$: C 2, D 3 | 8, at C |
| 4 | 6 | 7 | backward C, $g = 2$ | $g_B$: A 6, B 4 | 7, at B |
| 5 | 7 | 7 | stop, since $U = 7 \le 7$ | | 7 |

In step 3, G gives C the value $g_B = 2$, and C has $g_F = 6$, so $U = 8$. In step 4, C gives B the value $g_B = 4$, and B has $g_F = 3$, so $U = 7$. Then the forward state B has $f_F = 3 + 4 = 7$ and $pr_F = \max(7, 6) = 7$, every other open state has $pr$ at least 7, and the bound of line L5 is 7, so MM stops with the path S-B-C-G of cost 7. MM expanded 4 states, A* 5. No expanded state has $g > 7/2$.

**The 8-puzzle.** The script draws 20 instances with `random.Random(2024)`: each one is the goal after 60 random moves, kept if a breadth-first search gives an optimal cost $d \ge 14$, from 14 to 24 here. Both heuristics are the Manhattan distance, to the goal and to the start. Over the 20 instances, MM expanded 5,013 states with $\epsilon = 0$ and also with $\epsilon = 1$, against 3,411 for A*. With a good heuristic, MM did not pay on these instances, which is the effect that Kaindl and Kainz describe. These numbers are measured on these instances only.

## Correctness

The [proof](proofs/correctness.md) shows, for positive costs and admissible $h_F$ and $h_B$:

- **The bound $U$.** $U$ is the cost of a real path from $s$ to $t$, and at each moment it is at most $g_F(x) + g_B(x)$ for every state $x$ with a value in both directions.
- **A good pair.** Until $U = C^*$, there are states $p_i$ in $\mathrm{OPEN}_F$ and $p_j$ in $\mathrm{OPEN}_B$ on a cheapest path, with their least $g$ and with $p_i$ before $p_j$ on the path. Then $C$, $\mathit{fmin}_F$, $\mathit{fmin}_B$ and $\mathit{gmin}_F + \mathit{gmin}_B + \epsilon$ are all at most $C^*$.
- **Optimality.** So the stopping rule cannot hold while $U > C^*$, and MM returns a path of cost $C^*$.
- **Meeting in the middle.** Each state that MM expands has $pr \le C^*$, so $g \le C^*/2$ and $f \le C^*$ in its direction.
- **Termination.** On a finite graph, MM ends, and it returns failure only when no path exists.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, PREDECESSORS, $h_F$ and $h_B$ and each operation of the hash table counted as $O(1)$.

**Time per expansion.** An expansion looks at $b$ neighbors. With a priority queue in each direction keyed by $pr$, and two more keyed by $f$ and by $g$ for the minima of line L5, each update costs $O(\log n)$, so an expansion costs $O(b \log n)$. The implementation scans the open lists at each step, which is simpler and costs $O(n)$ per step.

**Number of expansions.** MM expands only states with $g \le C^*/2$ in their direction. Without a heuristic, this is about the square root of the work of a one-way search on a graph that grows exponentially, as for [bidirectional Dijkstra](/bidirectional-dijkstra/). With a strong heuristic, A* may expand few states with $g > C^*/2$ anyway, and MM can do more work than A*, as on the 8-puzzle above. Eckerle and others showed which pairs of states every admissible front-to-end bidirectional search must expand. Neither MM nor A* is the better one on all problems.

**Space.** Both searches keep their states, $O(n)$ in all, like A*.

## Properties

- **Optimal** with admissible heuristics in both directions, and **complete** on finite graphs.
- **Meets in the middle**: no state with $g > C^*/2$ in its direction is expanded.
- **Front-to-end**: each heuristic estimates the cost to the far end, not to the other frontier.
- **Needs** one explicit goal state and a predecessor function.
- **Space** like A*, for both directions.
- **Deterministic and not recursive.**

## Variants and improvements

- **BHPA (Pohl 1971).** The first bidirectional heuristic search: two A* searches with front-to-end heuristics, a choice of direction by the size of the open lists, and a stop when $U$ is at most the larger of $\mathit{fmin}_F$ and $\mathit{fmin}_B$. Its frontiers often went past each other before the rule held.
- **Front-to-front search.** De Champeaux and Sint (1977) estimate the cost from a node to each node of the other frontier. This gives better bounds, but each estimate costs time that grows with the size of the frontier.
- **MM0.** MM with $h_F = h_B = 0$ is a bidirectional uniform-cost search that also meets in the middle.
- **NBS.** Chen, Holte, Zilles and Sturtevant (2017) expand pairs of forward and backward states, and showed that NBS expands at most twice as many states as the best admissible front-to-end search on the same problem.

## When to use it

Use bidirectional heuristic search when the goal is a single known state, predecessors are easy to compute, and the heuristic is weak compared to the size of the search, so that one-way A* would go deep past the middle. Large puzzles with a modest heuristic and road networks are typical cases. With a strong heuristic, plain A* is often as good or better, as Kaindl and Kainz showed and the 8-puzzle example above repeats. If memory is the limit, both directions store their states, so a [memory-bounded search](/memory-bounded-heuristic-search/) may fit better.

## Pitfalls

- **Stopping at the first meeting.** The first path found where the searches touch need not be the cheapest, as $U = 8$ in step 3 of the example shows. Stop only when the rule of line L5 holds.
- **The wrong backward heuristic.** $h_B$ must estimate the cost from $s$, not to $t$. Using $h_F$ in both directions makes the backward search inadmissible.
- **A goal test instead of a goal state.** The backward search needs a state to start from. With many goal states, add a virtual goal with an action of cost 0 from each of them, and keep $\epsilon$ at most the least cost.
- **Checking only the other open list at line L12.** Then a meeting at a closed state of the other direction is missed until later. The paper's rule is still correct, but the proof on this site needs the test against all states with a value.
- **$\epsilon$ above the least action cost.** The term $\mathit{gmin}_F + \mathit{gmin}_B + \epsilon$ is a lower bound only if $\epsilon$ is at most the cost of every action. With a larger $\epsilon$ the search can stop too soon.

## Implementations

## History

Pohl proposed bidirectional heuristic search in 1971, with the bidirectional heuristic path algorithm and its front-to-end heuristics. He found that the two searches tended to pass each other. In 1977 de Champeaux and Sint gave a front-to-front algorithm that aims each search at the other frontier, at a high cost per node. For many years bidirectional heuristic search was thought not to pay. In 1997 Kaindl and Kainz showed that the frontiers usually meet early, and that most of the work goes into the proof that no cheaper path exists. In 2016 Holte, Felner, Sharon and Sturtevant gave MM at AAAI, the first bidirectional heuristic search that is sure to meet in the middle, with a journal version in Artificial Intelligence in 2017. The same group and Eckerle then studied which nodes any such search must expand, which led to NBS.

## References
