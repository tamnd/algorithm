---
tag: 887HFH
kind: algorithm
slug: weighted-a-star
name: Weighted A*
aliases:
- WA*
area: games-and-search/heuristic-search
level: core
summary: A* with the evaluation f = g + w h for a weight w >= 1. With an admissible h it returns a path of cost at most w times the optimum, often after far fewer expansions.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {n: the number of states reachable from the start, m: the number of actions among them}
  time: {consistent: O(m log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1970
  people: [Ira Pohl]
  note: Pohl studied the evaluation (1 - w) g + w h and the effect of the weight on the search.
prereqs: [a-star-search, admissible-heuristic]
see_also: [greedy-best-first-search, anytime-repairing-a-star, consistent-heuristic, a-star-optimality, beam-search, effective-branching-factor]
sources:
  - paper: doi:10.1016/0004-3702(70)90007-X
    title: Ira Pohl, Heuristic search viewed as path finding in a graph, Artificial Intelligence 1(3-4) (1970)
    locator: pp. 193 to 204 (the weighted evaluation function and the trade between the cost of the solution and the effort of the search)
  - paper: Maxim Likhachev, Geoff Gordon and Sebastian Thrun, ARA*, Anytime A* with provable bounds on sub-optimality, Advances in Neural Information Processing Systems 16 (NIPS 2003)
    locator: pp. 767 to 774 (weighted A* that expands each state at most once and keeps the bound w C* when h is consistent)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.5.4 (satisficing search, inadmissible heuristics and weighted A*, with its bound W C*)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 3 (formal properties of heuristic search, including weighted evaluation functions and searches that are admissible within a factor)
---

Weighted A* is [A* search](/a-star-search/) with the evaluation $f(n) = g(n) + w\,h(n)$ for a weight $w \ge 1$. A larger weight makes the search trust the [heuristic](/heuristic-function/) more and the cost so far less, so it usually goes more straight to a goal and expands fewer states. The price is the cost of the path: with an [admissible](/admissible-heuristic/) $h$ the path costs at most $w C^*$, where $C^*$ is the least cost. With a [consistent](/consistent-heuristic/) $h$ the bound holds even if the search never reopens a state. With $w = 1$ it is A*, and as $w$ grows it comes close to [greedy best-first search](/greedy-best-first-search/). Pohl studied the weighted evaluation in 1970.

## In plain words

You plan a trip and you compare roads by two numbers: the distance you have already driven, and a guess of the distance that is left. A* adds the two. Weighted A* counts the guess two or three times. The search then rushes toward roads that look close to the goal and spends less time on roads that only look cheap so far.

If the guess is never too high, you can say how much you lose: with the guess counted twice, the trip you find is at most twice as long as the best one. Often it is much closer to the best one. Counting the guess more does not always make the search faster, though. A strong push toward the goal can lead into a dead end, and then the search must come back.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives the finite list of pairs $(n', c)$ of a next state and the nonnegative cost of the action to it, a goal test IS-GOAL, a heuristic $h(n) \ge 0$, and a weight $w \ge 1$. The output is a path from $s_0$ to a goal of cost at most $w C^*$, or *failure* when no goal can be reached. A solution of this kind is called $w$-admissible, or bounded suboptimal.

## The algorithm

```pseudo id=main
WEIGHTED-A-STAR(s0, SUCCESSORS, IS-GOAL, h, w)
L1  g[s0] ← 0, parent[s0] ← nil
L2  OPEN ← { s0 } with key f(s0) = w·h(s0), CLOSED ← ∅
L3  while OPEN ≠ ∅ do
L4      n ← the state of OPEN with least f, ties toward larger g; remove it
L5      if IS-GOAL(n) then return PATH(parent, n), g[n]
L6      add n to CLOSED
L7      for each (n′, c) in SUCCESSORS(n) do
L8          if n′ has no g or g[n] + c < g[n′] then
L9              g[n′] ← g[n] + c, parent[n′] ← n
L10             if n′ ∈ CLOSED then remove n′ from CLOSED      ▷ reopen
L11             put n′ in OPEN with key f(n′) = g[n′] + w·h(n′), or lower its key
L12 return failure
```

The lines are those of A*, with $w\,h$ in place of $h$ at lines L2 and L11. Line L10 reopens a state in CLOSED when a cheaper path to it is found. The *no reopening* form skips such a path instead, and leaves the state in CLOSED. The code has a flag `reopen` for the two forms. With a consistent $h$ both forms keep the bound $w C^*$, and the form without reopening expands each state at most once, which is why most programs use it.

Use an integer or a rational weight in a program, so that keys compare exactly. With a weight of type float, rounding can break ties in a different way on different machines.

## Example

The graph is the one of the page [A* search](/a-star-search/): the undirected edges S-A 2, S-B 3, S-F 1, A-C 4, A-D 3, B-C 2, B-E 2, C-G 2 and D-G 3, the goal G, and $h$ the Manhattan distance to G, with the values 6, 4, 4, 2, 2, 6, 7, 0 on S, A, B, C, D, E, F, G. This $h$ is consistent and $C^* = 7$. The trace for $w = 3/2$, with each entry written as $g/f$:

| step | removed $g/f$ | what lines L7 to L11 do | OPEN after the step |
| --- | --- | --- | --- |
| 1 | S 0/9 | A, B, F get $g$ = 2, 3, 1 | A 2/8, B 3/9, F 1/23/2 |
| 2 | A 2/8 | C gets 6, D gets 5 | D 5/8, C 6/9, B 3/9, F 1/23/2 |
| 3 | D 5/8 | G gets 8 | G 8/8, C 6/9, B 3/9, F 1/23/2 |
| 4 | G 8/8 | goal: return S-A-D-G, cost 8 | |

With $w = 1$ the search is A*: it expands S, A, D, B and C and returns S-B-C-G of cost 7. With each of $w = 5/4, 3/2, 2, 3, 5$ it expands only S, A and D and returns S-A-D-G of cost 8. The bound allows $8.75$ for $w = 5/4$, so the path is well inside it.

**Measured on the 8-puzzle.** The script draws 20 instances from `random.Random(2024)`. Each one is a random walk of 60 moves from the goal, kept when breadth-first search gives an optimal depth $d \ge 14$; the depths are 14 to 24. The heuristic is the Manhattan distance of the tiles, which is consistent, and the search reopens states.

| weight | expansions in all | mean of cost / $d$ | largest cost / $d$ |
| --- | --- | --- | --- |
| 1 (A*) | 3,411 | 1 | 1 |
| 3/2 | 2,434 | 1 | 1 |
| 2 | 2,390 | 1.020 | 5/4 |
| 3 | 3,870 | 1.154 | 13/8 |
| 5 | 4,637 | 1.342 | 15/8 |

Each cost is well under its bound $w d$. The number of expansions does not fall steadily with $w$. Here, weights of 3 and 5 expanded more states than A*. Greedy best-first search on the same instances made 3,949 expansions. These are measured numbers for these 20 small instances only, and they say nothing about larger puzzles.

## Correctness

The [proof](proofs/correctness.md) shows two bounds. Both use $h(t) = 0$ at goals, which follows from admissibility.

- **With reopening.** If $h$ is admissible, the returned path costs at most $w C^*$. Until a goal is removed, OPEN holds a state $p$ on a cheapest path with $g[p] = g^*(p)$, and then $f(p) = g^*(p) + w\,h(p) \le w\,(g^*(p) + h^*(p)) = w C^*$. This fact is Lemma 2 of the [A* proof](/a-star-search/), and its proof does not depend on the key.
- **Without reopening.** If $h$ is consistent, each state $s$ that is removed from OPEN has $g[s] \le w\,g^*(s)$, so the goal has $g \le w C^*$. This is the result of Likhachev, Gordon and Thrun (2003).

Termination on a finite graph, and completeness, follow as for A*.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS, IS-GOAL and $h$ counted as $O(1)$, $n$ the number of states reachable from $s_0$ and $m$ the number of actions among them.

**Without reopening.** Each state is expanded at most once, so the time is $O(m \log n)$ with a [binary heap](/binary-heap/) and the space is $O(n + m)$ with lazy deletion. This is the same worst case as A* with a consistent $h$.

**With reopening.** Even with a consistent $h$, weighted A* can reopen states, because $g + w\,h$ is not a consistent evaluation when $w > 1$. The worst case is then the exponential bound of A* with an inconsistent heuristic. If the bound is all you need and $h$ is consistent, use the form without reopening.

There is no general theorem that a larger weight gives fewer expansions. The table above shows a case where it does not. The effect of the weight is best described as a lower [effective branching factor](/effective-branching-factor/) when $h$ is good.

## Properties

- **Bounded suboptimal.** The cost is at most $w C^*$, with an admissible $h$ and reopening, or with a consistent $h$.
- **Complete** on finite graphs, and on infinite graphs with finite branching and costs bounded below by some $\delta > 0$.
- **Not in place.** It stores all generated states.
- **Deterministic**, with the tie rule of line L4.
- **Bound only at the end.** Weighted A* has no anytime behavior: it returns one path. [ARA*](/anytime-repairing-a-star/) runs it with falling weights and reuses the work.

## Variants and improvements

- **[Anytime repairing A*](/anytime-repairing-a-star/).** Start with a large weight, report the path, then lower the weight and continue from the state of the last search.
- **The form of Pohl.** Pohl wrote the evaluation as $(1 - \lambda)\,g + \lambda\,h$ for $0 \le \lambda \le 1$. This orders states as $g + w\,h$ with $w = \lambda / (1 - \lambda)$, for $\lambda < 1$, so the two forms are the same method.
- **Dynamic weighting.** Let the weight depend on the depth of the node, large near the start and close to 1 near the goal. Pohl proposed this in later work.
- **Focal search, or A*$_\varepsilon$.** Pearl and Kim (1982) keep a FOCAL list of the states of OPEN with $f \le (1 + \varepsilon) f_{\min}$, and choose among them by a second heuristic, for example an estimate of the number of actions left. The bound $(1 + \varepsilon) C^*$ holds with an admissible $h$.
- **[Greedy best-first search](/greedy-best-first-search/).** The limit $w \to \infty$, with no bound on the cost.

## When to use it

Use weighted A* when an optimal path costs too much time or memory, and a path within a known factor of the optimum is good enough. Typical uses are planning, path finding on large maps and puzzles such as the fifteen puzzle. Choose a small weight first, such as $3/2$ or $2$, and measure: a large weight often does not help, as the 8-puzzle table shows. When you need a solution soon but want a better one if time allows, use ARA*. When you need the optimum, use A* or [IDA*](/iterative-deepening-a-star/).

## Pitfalls

- **Reading the bound as the typical loss.** The bound $w C^*$ is a worst case. The paths are often much better, so a small measured loss does not mean a smaller weight is safe to replace.
- **Dropping reopening with an inconsistent heuristic.** Without line L10, the bound needs a consistent $h$. With an admissible $h$ that is not consistent, keep the reopening.
- **A float weight.** Keys such as $3 + 1.1 \cdot 4$ are rounded, and ties then depend on rounding. Use a fraction.
- **Goal test at generation.** It breaks the proof, since a goal that is generated can have a $g$ far above the bound. Test at line L5.
- **Weights below 1.** They give a search between A* and [uniform-cost search](/uniform-cost-search/) that is still optimal with an admissible $h$, since $w\,h$ is then admissible too, but it gains nothing over A*. The code rejects them, since they are almost always a mistake.

## Implementations

## History

Pohl (1970) studied best-first search with the evaluation $(1 - \lambda)\,g + \lambda\,h$ and the trade between the cost of the solution and the work of the search. The bound $w C^*$ for an admissible $h$ is a simple consequence of the A* argument and is in Pearl's book (1984). Pearl and Kim (1982) gave focal search with a bound of the same kind. Likhachev, Gordon and Thrun (2003) showed that with a consistent heuristic the bound holds even when no state is reopened, and used this in ARA*. The name weighted A* is now standard in the literature on suboptimal search.

## References
