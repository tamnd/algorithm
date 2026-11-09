---
tag: FPPN86
kind: algorithm
slug: grasp
name: GRASP
aliases:
- greedy randomized adaptive search procedure
area: optimization/metaheuristics
level: advanced
summary: Repeat randomized greedy construction followed by local search and keep the best.
model: word-ram
complexity:
  vars: {K: the number of iterations, n: the number of sets, m: the number of elements, H: the time of one run of the local search}
  time: {worst: O(K (n^2 m + H))}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [local-search, greedy-algorithm, hill-climbing, local-optimum]
see_also: [random-restart-hill-climbing, path-relinking, iterated-local-search, set-cover, greedy-set-cover, tabu-search, intensification-and-diversification, metaheuristic]
sources:
  - paper: "Thomas A. Feo and Mauricio G. C. Resende, A probabilistic heuristic for a computationally difficult set covering problem, Operations Research Letters 8(2), 1989"
    locator: pp. 67 to 71 (the first randomized greedy construction with local search, on a set covering problem)
  - paper: doi:10.1007/BF01096763
    title: Thomas A. Feo and Mauricio G. C. Resende, Greedy randomized adaptive search procedures, Journal of Global Optimization 6, 1995
    locator: pp. 109 to 133 (the name GRASP, the two phases, the restricted candidate list)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 6, Greedy Randomized Adaptive Search Procedures, Advances and Extensions, by Mauricio G. C. Resende and Celso C. Ribeiro, from p. 169
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.3, Hybrid SLS Methods, from p. 85 (GRASP as construction plus local search)
  - paper: "Vašek Chvátal, A greedy heuristic for the set-covering problem, Mathematics of Operations Research 4(3), 1979"
    locator: pp. 233 to 235 (the greedy cover costs at most H(d) times the optimum)
---

GRASP, the greedy randomized adaptive search procedure, is a [metaheuristic](/metaheuristic/) that repeats two phases and keeps the best result. The first phase builds a solution step by step like a [greedy algorithm](/greedy-algorithm/), but at each step it picks at random among the good choices, not always the best one. The second phase improves that solution by [local search](/local-search/) to a [local optimum](/local-optimum/). Feo and Resende introduced the method in 1989 for a set covering problem and named it in 1995. The random choices give a different start in each iteration, and the greedy bias keeps these starts good. GRASP has no guarantee of reaching an optimum in a fixed number of iterations; if one iteration reaches it with probability $p$, then $K$ iterations all miss with probability $(1 - p)^K$.

## In plain words

You must pack a bag, and you want a good packing. A greedy packer always takes the item that looks best now, so it packs the same bag each time. GRASP makes a short list of the items that look nearly best, and it takes one of them at random. Then it looks at the finished bag and makes small swaps while they help. It does this many times and keeps the best bag.

The short list is controlled by one number. If the list holds only the best choice, the method is plain greedy and repeats itself. If the list holds every choice, the starts are random and often poor. Between these, the starts are good and different, which is what the swaps need.

## The problem

The page shows GRASP on weighted [set cover](/set-cover/). The input is a universe $U$ of $m$ elements, sets $S_1, \ldots, S_n \subseteq U$ whose union is $U$, costs $c_j > 0$, a parameter $\alpha \in [0, 1]$ and a number of iterations $K \ge 1$. A cover is a set $x$ of indices with $\bigcup_{j \in x} S_j = U$, of cost $c(x) = \sum_{j \in x} c_j$. The output is a cover of low cost. The aim is a cover of least cost, which is [NP-hard](/np-hard/) to find, and GRASP cannot prove that it has found one.

The same scheme works for any problem with a greedy construction and a local search: the construction needs a greedy score for each candidate, and the local search needs a [neighborhood](/neighborhood-structure/).

## The algorithm

```pseudo id=main
GRASP(U, S, c, α, K)
L1  b ← none
L2  for i ← 1 to K do
L3      x ← empty set of chosen sets
L4      while x does not cover U do
L5          r_j ← c_j / |S_j \ covered(x)| for every set j with uncovered elements
L6          RCL ← { j : r_j ≤ r_min + α (r_max − r_min) }
L7          add a set chosen uniformly at random from RCL to x
L8      x ← LOCAL-SEARCH(x)       ▷ drop and swap moves
L9      if b = none or c(x) < c(b) then b ← x
L10 return b
```

Lines L3 to L7 are the construction phase. Line L5 computes the greedy score of each useful set: its cost per newly covered element. The score is *adaptive*: it depends on what the earlier steps have covered. Line L6 builds the *restricted candidate list* (RCL) of the sets whose score is within a fraction $\alpha$ of the best. With $\alpha = 0$ the list holds only the sets of the least ratio, which is the [greedy set cover](/greedy-set-cover/) algorithm; with $\alpha = 1$ it holds every useful set. Line L8 is a best-improvement descent with two moves, drop one chosen set or replace one chosen set by one other set, and it accepts only covers of lower cost. Line L9 keeps the best cover.

## Example

Take $U = \{0, \ldots, 7\}$ and seven sets.

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $S_j$ | 0 2 4 5 7 | 4 6 7 | 0 1 5 6 | 0 4 | 2 3 6 | 3 6 | 0 6 7 |
| $c_j$ | 9 | 5 | 9 | 2 | 9 | 9 | 4 |

By enumeration, the least cost of a cover is 23, by $\{1, 2, 4\}$.

**Plain greedy.** With $\alpha = 0$, the first ratios are $9/5$, $5/3$, $9/4$, $2/2$, $9/3$, $9/2$ and $4/3$, so the greedy step picks set 3. Next it picks set 6, at ratio 2. Now sets 0, 2 and 4 tie at ratio $9/2$, and the tie is broken at random. With seed 0 the run picks 0, then 4, then 2, a cover $\{0, 2, 3, 4, 6\}$ of cost 33. The best move of the descent drops set 0 and reaches $\{2, 3, 4, 6\}$ of cost 24. This cover is a local minimum: to reach $\{1, 2, 4\}$ the search must remove two sets and add one, which is not a move.

The drop and swap moves have exactly three local minima on this instance, of cost 23, 24 and 27. Over all tie breaks, the $\alpha = 0$ construction ends at cost 24 with probability $2/3$ and at cost 33 with probability $1/3$, and the descent then ends at 24 or 27. So greedy with ties broken at random, plus local search, never finds the optimum here, however many times it is run.

**GRASP.** With $\alpha = 1/2$, seed 0 (Python `random.Random(0)`) and $K = 3$, the run goes as follows. In the first step the ratios range from 1 to $9/2$, so the threshold is $1 + (1/2)(7/2) = 11/4$, and the RCL is $\{0, 1, 2, 3, 6\}$.

| $i$ | construction steps (RCL, chosen) | built (cost) | after local search (cost) |
|---|---|---|---|
| 1 | ({0,1,2,3,6}, 3), ({0,1,2,4,6}, 4), ({0,2,6}, 0), ({2}, 2) | {0,2,3,4} (29) | {2,3,4,6} (24) |
| 2 | ({0,1,2,3,6}, 6), ({0,1,2,3,4}, 3), ({0,2,4}, 2), ({4}, 4) | {2,3,4,6} (24) | {2,3,4,6} (24) |
| 3 | ({0,1,2,3,6}, 3), ({0,1,2,4,6}, 2), ({0,1,4,6}, 1), ({4}, 4) | {1,2,3,4} (25) | {1,2,4} (23) |

In iteration 3 the construction picks set 1, which plain greedy never picks, and the descent drops set 3 to reach the optimum 23.

**How $\alpha$ changes the chance.** For this instance the exact probability that one iteration ends at the optimum can be found by listing every path of the construction with its probability. It is 0 for $\alpha = 0$, $43/144 \approx 0.30$ for $\alpha = 1/4$, $93/200 = 0.465$ for $\alpha = 1/2$, $43/90 \approx 0.48$ for $\alpha = 3/4$ and $211/504 \approx 0.42$ for $\alpha = 1$. These numbers hold for this one instance only. For $\alpha = 1/2$, five iterations all miss with probability $(107/200)^5 \approx 0.044$.

## Correctness

GRASP has no optimality guarantee, so "correct" means the following. The construction stops with a cover: the set of least ratio is always in the RCL, so the list is never empty, and each step covers at least one new element. The local search stops, since each move lowers the cost of a cover. The result is the least cost cover among the $K$ local minima found, and it is itself a local minimum for drop and swap moves.

Two facts are proved. With $\alpha = 0$, the construction is greedy set cover, so each built cover costs at most $H(d)$ times the optimum, where $d$ is the size of the largest set and $H(d) = 1 + 1/2 + \cdots + 1/d$ (Chvátal 1979); the local search only lowers this. And the iterations are independent, so if one iteration finds an optimum with probability $p$, all $K$ miss with probability $(1 - p)^K$. The value of $p$ is not known, and the example shows that it can be 0. The [full proof](proofs/correctness.md) gives all steps.

## Complexity

A construction makes at most $\min(n, m)$ steps, since each step covers a new element and chooses a new set. Each step computes $n$ ratios, each from an intersection of size at most $m$, so one construction takes $O(n m \min(n, m)) \subseteq O(n^2 m)$ time. With $H$ the time of one run of the local search, $K$ iterations take $O(K (n^2 m + H))$ time. For the drop and swap descent, one pass looks at $O(n^2)$ moves, but the number of passes has no polynomial bound in general; it is at most the number of distinct cover costs. The extra space is $O(n + m)$: the ratios, the uncovered elements and the best cover.

## Properties

- **Randomized.** The result depends on the random choices. The run is reproducible with a fixed seed.
- **Memoryless iterations.** Plain GRASP keeps only the best solution. No iteration uses what an earlier one found, which is why the $(1 - p)^K$ bound holds and also why plain GRASP does not learn.
- **One main parameter.** The value of $\alpha$ moves the construction between greedy ($\alpha = 0$) and random ($\alpha = 1$).
- **Easy to run in parallel.** The iterations are independent, so they can run on separate processors with separate random streams.
- **A multi-start method.** GRASP is [random-restart hill climbing](/random-restart-hill-climbing/) with a greedy biased start in place of a uniform random start.

## Variants and improvements

- **RCL by cardinality.** Put the $k$ best candidates in the list, in place of a threshold on the score.
- **Reactive GRASP.** Choose $\alpha$ in each iteration from a set of values, with probabilities that grow for values that gave good results. The handbook chapter by Resende and Ribeiro describes this and other ways to set $\alpha$.
- **Biased choice.** Pick from the RCL with probabilities that favor better scores, in place of a uniform pick.
- **GRASP with path relinking.** Keep a pool of elite solutions and connect each new local minimum to an elite one by [path relinking](/path-relinking/). This adds memory between iterations, and it is a common extension in the GRASP literature.
- **Other local searches.** Line L8 can be any local search, such as [tabu search](/tabu-search/) or [variable neighborhood search](/variable-neighborhood-search/).

## When to use it

Use GRASP when a good greedy rule already exists for the problem, as for set cover, graph partitioning, scheduling or the [quadratic assignment problem](/quadratic-assignment-problem/), and when greedy plus local search alone gets stuck in the same local optimum. It is simple to add to such code: randomize the greedy choice and loop. When good solutions share structure, a method with memory, such as GRASP with path relinking or [iterated local search](/iterated-local-search/), often uses the time better than independent restarts.

## Pitfalls

- **$\alpha = 0$ with no ties.** Then every iteration builds the same solution, and $K$ iterations cost $K$ times as much as one.
- **Comparing ratios with floats.** Ties at the RCL threshold decide what is in the list. With floating point scores, a set at the threshold can drop out by rounding. Exact fractions, as in the test code, or a small tolerance avoid this.
- **A weak local search.** The construction gives the starts, but the local search does most of the work. If it is too slow, there are few iterations; if it is too weak, the good starts are wasted.
- **Reading $(1 - p)^K$ as a guarantee.** The bound needs $p$, which is unknown, and it can be 0 for a given $\alpha$.

## Implementations

## History

Feo and Resende described a randomized greedy construction followed by local search in 1989, for a hard set covering problem, and gave the name GRASP and a general description in their 1995 paper in the Journal of Global Optimization. Resende and Ribeiro survey later work, such as reactive GRASP and GRASP with path relinking, in the Handbook of Metaheuristics. Hoos and Stützle classify GRASP as a hybrid stochastic local search method, a construction method combined with a local search.

## References
