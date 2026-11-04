---
tag: 76CY83
kind: algorithm
slug: iterative-deepening-search
name: Iterative deepening search
aliases:
- iterative deepening depth-first search
- IDDFS
- IDS
area: techniques/search-strategies
level: core
summary: Runs depth-limited search with limits 0, 1, 2, ... to combine DFS memory use with BFS-like optimality for unit costs.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth of a shallowest goal}
  time: {worst: O(b^d), best: O(1)}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
prereqs: [depth-limited-search, breadth-first-search, depth-first-search, search-tree]
see_also: [depth-limited-search, iterative-deepening-a-star, breadth-first-search, depth-first-search, completeness-and-optimality-of-search, iterative-broadening, alpha-beta-pruning, bidirectional-search]
sources:
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: Richard E. Korf, Depth-first iterative-deepening, an optimal admissible tree search, Artificial Intelligence 27(1) (1985)
    locator: pp. 97 to 109 (the algorithm, the count of nodes against breadth-first search, the bound b/(b-1), and the proof that it is asymptotically optimal among brute-force tree searches)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.4.4 (the ITERATIVE-DEEPENING-SEARCH function, the counts 123,450 and 111,110 for b = 10 and d = 5, and the comparison table of Section 3.4)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (depth-first search with a depth bound, and searches that repeat with a larger bound)
---

Iterative deepening search runs [depth-limited search](/depth-limited-search/) with the limits $0, 1, 2, \ldots$ until a run does not report *cutoff*. It finds a goal with the fewest actions, as [breadth-first search](/breadth-first-search/) does, but it uses memory linear in the depth, as [depth-first search](/depth-first-search/) does. It repeats the work of the upper levels in each run, but in a tree with branching factor $b \ge 2$ this costs at most a factor $b/(b-1)$ over the nodes that breadth-first search generates. Korf (1985) showed that it is asymptotically optimal among brute-force tree searches in time, space and solution length.

## In plain words

You look for your keys in a house with many rooms, and you have a bad memory. First you look only in the room where you stand. Then you start again and look in that room and the rooms one door away. Then two doors away, and so on. Each round goes one door further than the last.

You look at the near rooms again and again, which seems wasteful. But in a house where each room has many doors, most rooms are far away, in the last round. So the repeats add only a little. You find the keys in the round where they are closest to you, and you never have to remember more than the way back to where you started.

## The problem

The input is a [state-space search](/state-space-search/) problem: a start state $s_0$, a function SUCCESSORS that gives a finite list of next states, and a goal test IS-GOAL. The output is a path from $s_0$ to a goal state with the fewest actions, or *failure* when no goal can be reached. Action costs play no part, so the path is the cheapest one only when all actions cost the same.

## The algorithm

```pseudo id=main
ITERATIVE-DEEPENING-SEARCH(s0, SUCCESSORS, IS-GOAL)
L1  for ℓ ← 0, 1, 2, ... do
L2      r ← DEPTH-LIMITED-SEARCH(s0, SUCCESSORS, IS-GOAL, ℓ)
L3      if r ≠ cutoff then return r
```

The answer of line L2 is a path, *cutoff* or *failure*, as defined on the page [depth-limited search](/depth-limited-search/). A path ends the loop with a solution. Failure ends it because no goal can be reached at all. Only cutoff makes the loop go on. The depth-limited search here checks for cycles on the current path, so on a finite space some limit shows the whole space and the loop ends with failure when no goal exists.

## Example

The graph has the directed edges S→A, S→G, A→B, A→C, B→D, C→D, C→G, D→G, and children are tried in this order. The goal is D.

| limit $\ell$ | states goal-tested, in order | answer |
| --- | --- | --- |
| 0 | S | cutoff |
| 1 | S, A, G | cutoff |
| 2 | S, A, B, C, G | cutoff |
| 3 | S, A, B, D | S-A-B-D |

The search does 13 goal tests and returns a path of 3 actions, the fewest possible. S is tested 4 times and A 3 times. With the goal G, the run with $\ell = 1$ tests S, A and G and returns S-G, a path of 1 action, though S-A-C-G is cheaper when the edges have costs. With a goal that is not in the graph, the limits 0 to 3 give cutoff, the limit 4 gives failure, and the search makes $1 + 3 + 5 + 8 + 10 = 27$ goal tests.

### How much the repeats cost

In the uniform tree of branching factor $b$ with the only goal at the end of depth $d$, the run with limit $\ell$ generates the nodes of depths 1 to $\ell$, so the nodes of depth $i$ are generated $d + 1 - i$ times. Breadth-first search, with the goal test when a node is generated, generates each node once.

| $b$ | $d$ | iterative deepening | breadth-first | ratio | $b/(b-1)$ |
| --- | --- | --- | --- | --- | --- |
| 2 | 10 | 4,072 | 2,046 | 1.9902 | 2 |
| 3 | 8 | 14,748 | 9,840 | 1.4988 | 1.5 |
| 10 | 5 | 123,450 | 111,110 | 1.1111 | 1.1111 |
| 10 | 10 | 12,345,679,000 | 11,111,111,110 | 1.1111 | 1.1111 |

The row $b = 10$, $d = 5$ is the example of Russell and Norvig. The ratio is close to $b/(b-1)$ and never above it. For $b = 2$ iterative deepening does about twice the work, and for large $b$ the repeats are almost free.

## Correctness

The proofs below give three facts, for finite branching.

- **A returned path has the fewest actions.** Let $d$ be the least number of actions of a path from $s_0$ to a goal. For each $\ell < d$, depth-limited search finds no goal, and it returns cutoff, because the path to the goal is longer than $\ell$. For $\ell = d$ it returns a path of at most $d$ actions, so of exactly $d$ actions.
- **Completeness.** If a goal can be reached, the loop reaches $\ell = d$ after finitely many runs, and each run stops.
- **Failure is correct.** The loop returns failure only when depth-limited search does, which happens only when no goal can be reached. On a finite space with no reachable goal, the run with $\ell$ equal to the length of the longest path without a repeated state returns failure.

On an infinite space with no goal, each run returns cutoff and the loop never stops. By Fact 3 of [completeness and optimality of search](/completeness-and-optimality-of-search/), no search can avoid this on all problems.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of SUCCESSORS and IS-GOAL and each operation on the path set counted as $O(1)$. Count the time, as Korf and Russell and Norvig do, by the nodes generated in a tree with branching factor $b \ge 2$ and a shallowest goal at depth $d$.

**Time.** The run with limit $\ell$ generates at most $S_\ell = b + b^2 + \cdots + b^\ell$ nodes, so the whole search generates at most
$$ N_{\mathrm{IDS}} = \sum_{\ell=1}^{d} S_\ell = \sum_{i=1}^{d} (d + 1 - i)\, b^i . $$
Since $S_\ell = b(b^\ell - 1)/(b - 1)$, we have $S_\ell / S_d = (b^\ell - 1)/(b^d - 1) \le b^{\ell - d}$, and so
$$ N_{\mathrm{IDS}} \le S_d \sum_{\ell=1}^{d} b^{\ell - d} < S_d \cdot \frac{b}{b - 1}. $$
Here $S_d$ is the number of nodes that breadth-first search generates when the goal is the last node of depth $d$, so iterative deepening does less than $b/(b-1)$ times the work of breadth-first search, and $N_{\mathrm{IDS}} = O(b^d)$. Breadth-first search with the goal test at expansion generates, in the same worst case, all nodes of depth up to $d + 1$ except the $b$ children of the goal, that is $S_{d+1} - b = b^2 (b^d - 1)/(b - 1)$ nodes. The bound above is $b^2 (b^d - 1)/(b - 1)^2$, which is not larger, so then iterative deepening generates fewer nodes. In the best case $s_0$ is a goal and the search does $O(1)$ work.

**Space.** One run at a time is active, with recursion depth at most $d + 1$. The space is $O(d)$ when SUCCESSORS gives children one at a time and $O(bd)$ when it returns them as a list.

**Lower bounds.** Korf (1985) showed that iterative deepening is asymptotically optimal among brute-force tree searches. Each such search must generate $\Omega(b^d)$ nodes in the worst case, because in the uniform tree an adversary can put the only goal at the last node of depth $d$ that the search looks at. It must use $\Omega(d)$ space to hold the path it returns, and no search can return fewer than $d$ actions.

## Properties

- **Complete** for finite branching, also on infinite spaces when a goal exists.
- **Optimal for unit costs.** It returns a path with the fewest actions, so a cheapest path when all actions cost the same. With other costs, use [IDA*](/iterative-deepening-a-star/) with $h = 0$ or a cost limit.
- **Linear memory.** $O(bd)$, against $O(b^d)$ for breadth-first search.
- **Tree-like.** It keeps no table of reached states. On a graph with many paths to the same state, such as a grid, it repeats states within each run, and it can then be much slower than breadth-first graph search.
- **Anytime in games.** Each finished run gives an answer for its depth, which is why game programs use it to fit a time budget.

## Variants and improvements

- **[IDA*](/iterative-deepening-a-star/).** Iterate on a bound of $f = g + h$ instead of the depth. Each new bound is the least $f$ that went over the old one. Korf introduced it in the same paper.
- **Iterative lengthening.** Iterate on a bound of the path cost $g$. It finds a cheapest path, but with many distinct costs it needs one run per distinct cost.
- **Iterative deepening in games.** [Alpha-beta pruning](/alpha-beta-pruning/) to depth 1, 2, 3 and so on, with the best moves of one run tried first in the next, and a [transposition table](/transposition-table/) between runs. The better move order often makes the whole series cheaper than a single deep run.
- **[Bidirectional search](/bidirectional-search/) with iterative deepening.** Deepen from both ends to save time, at the cost of storing one frontier.
- **[Iterative broadening](/iterative-broadening/).** Iterate on the number of children of each node instead of the depth.

## When to use it

Use iterative deepening search when the space is large or infinite, the depth of the solution is not known, the actions have equal costs, and breadth-first search would run out of memory. It is the standard uninformed search for such problems. If the states fit in memory and the space has many paths to each state, breadth-first graph search is faster. If the costs differ, use uniform-cost search or IDA*.

## Pitfalls

- **Stopping on cutoff from an inner run.** Only cutoff makes the loop go on. If depth-limited search reports cutoff for every node at the limit, even one with no child, the loop never stops on a finite space without a goal.
- **No check for cycles.** Without it, the runs on a space with a reachable cycle always end in cutoff, so the search runs for ever when no goal exists, and it repeats much work inside each run.
- **A global visited set inside a run.** It can hide a goal: a state first reached deep, near the limit, is then not expanded when a shorter path reaches it. Check only the current path.
- **Expecting the cheapest path.** With unequal action costs, the path with the fewest actions can be costly, as S-G above.
- **Small branching factors.** For $b$ near 1, as in a long corridor, the bound $b/(b-1)$ is large: on a chain of length $d$ the search does about $d^2/2$ goal tests against $d$.

## Implementations

## History

Searching again with a larger depth was used in chess programs in the 1970s to fit the search into the available time, for example in the CHESS 4.5 program of Slate and Atkin. Korf (1985) named depth-first iterative-deepening as a general search algorithm, counted its nodes against breadth-first search, and proved that it is asymptotically optimal among brute-force tree searches in time, space and the length of the solution. In the same paper he introduced IDA*. Russell and Norvig present it as the preferred uninformed search when the search space is large and the depth of the solution is not known.

## References
