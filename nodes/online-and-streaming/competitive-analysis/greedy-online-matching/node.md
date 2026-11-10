---
tag: 39VNTT
kind: algorithm
slug: greedy-online-matching
name: Greedy online matching
aliases:
- greedy matching
- online greedy matching
area: online-and-streaming/competitive-analysis
level: intro
summary: Matches each arriving vertex to any free neighbour; it returns a maximal matching, so it is 1/2-competitive, and no deterministic rule does better.
solves: [online-bipartite-matching]
model: word-ram
complexity:
  vars: {n: the number of online vertices, m: the number of edges, k: the number of offline vertices}
  time: {worst: O(m + k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1990
  people: [Richard M. Karp, Umesh V. Vazirani, Vijay V. Vazirani]
  note: Karp, Vazirani and Vazirani stated the online bipartite matching problem, noted that each greedy rule gets half of the optimum and that no deterministic rule gets more, and showed that a random choice of neighbour does not help.
prereqs: [online-bipartite-matching, maximal-matching, competitive-ratio]
see_also: [ranking-algorithm, balance-algorithm, maximum-matching, hopcroft-karp, adaptive-adversary, online-adwords-problem]
sources:
  - paper: doi:10.1145/100216.100262
    title: "Richard M. Karp, Umesh V. Vazirani and Vijay V. Vazirani, An optimal algorithm for on-line bipartite matching, Proceedings of the 22nd Annual ACM Symposium on Theory of Computing (STOC 1990), 352-358"
    locator: the introduction (greedy gets 1/2, and no deterministic algorithm does better) and the section on the algorithm RANDOM
  - paper: doi:10.1561/0400000057
    title: "Aranyak Mehta, Online matching and ad allocation, Foundations and Trends in Theoretical Computer Science 8(4) (2013), 265-368"
    locator: Chapter 3, the greedy algorithm and the bound 1/2, and the deterministic upper bound
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1 (competitive ratio) and Chapter 6 (randomized algorithms and adaptive adversaries)
---

Greedy online matching is the simplest rule for [online bipartite matching](/online-bipartite-matching/): when an online vertex arrives, match it to any neighbour that is still free, and leave it unmatched only if it has no free neighbour. The output is always a [maximal matching](/maximal-matching/), so it has at least half as many edges as a [maximum matching](/maximum-matching/). The ratio $1/2$ is tight, and no deterministic online rule does better. The rule runs in time linear in the number of edges.

## In plain words

Jobs arrive one at a time, and each job names the workers who can do it. Give the job to any free worker on its list. Turn it away only when every worker on its list is busy.

Why is this at least half as good as the best plan? Take any job that the best plan gives to some worker. Either the greedy rule served that job, or it turned it away, and then that worker was already busy. So each pair of the best plan has a busy member in the greedy plan, and each greedy pair can account for only two such members. A sly order of jobs makes the greedy rule lose exactly half, whatever free worker it picks.

## The problem

The input is a bipartite graph $G = (U \cup V, E)$. The offline side $U$ is known at the start, and the online vertices $v_1, \ldots, v_n$ arrive one at a time, each with its neighbour set $N(v_t) \subseteq U$. Each $v_t$ must be matched to a free neighbour or left unmatched before the next arrival, for good. The goal is a large matching. $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the sizes of the online matching and of a maximum matching on the sequence $\sigma$. The ratio convention is $\mathrm{ALG}(\sigma) \ge c \cdot \mathrm{OPT}(\sigma)$ with $c \le 1$ and no additive term.

## The algorithm

$F$ is the set of free offline vertices and $M$ is the matching. The parameter CHOOSE is any rule that returns one element of a non-empty set; it may depend on the past.

```pseudo id=main
GREEDY-ONLINE-MATCHING(U, σ, CHOOSE)              ▷ σ = v_1 .. v_n, revealed one at a time
L1  M ← ∅, F ← U
L2  for t ← 1 to n do
L3      receive v_t and N(v_t)
L4      C ← N(v_t) ∩ F                              ▷ free neighbours
L5      if C ≠ ∅ then
L6          u ← CHOOSE(C)
L7          M ← M ∪ {(u, v_t)}
L8          F ← F \ {u}
L9  return M
```

Common choices for CHOOSE are the first neighbour in a fixed order of $U$, the first in the order of the neighbour list, and a uniform random free neighbour (the rule RANDOM). The [Ranking algorithm](/ranking-algorithm/) is greedy too: its CHOOSE is "the first free neighbour in one random order of $U$ drawn at the start".

## Example

Take $U = \{a, b, c, d\}$, CHOOSE = the first free neighbour in the list, and the arrivals below.

| $t$ | $N(v_t)$ | $F$ before | $C$ | match | $M$ after |
|---|---|---|---|---|---|
| 1 | $a, b$ | $a, b, c, d$ | $a, b$ | $a$ | $v_1 a$ |
| 2 | $a$ | $b, c, d$ | none | unmatched | $v_1 a$ |
| 3 | $b, c$ | $b, c, d$ | $b, c$ | $b$ | $v_1 a, v_3 b$ |
| 4 | $c, d$ | $c, d$ | $c, d$ | $c$ | $v_1 a, v_3 b, v_4 c$ |

Greedy matches 3 vertices. The maximum matching $v_1 b, v_2 a, v_3 c, v_4 d$ has 4, so the ratio on this input is $3/4 \ge 1/2$. The loss comes from step 1: greedy took $a$, the only neighbour of $v_2$.

**The tight case.** Let $U = \{u_1, u_2\}$. The vertex $v_1$ is adjacent to both. Whatever greedy takes, the adversary makes $v_2$ adjacent only to that vertex. Greedy gets 1 and the optimum is 2. Each deterministic CHOOSE has such an input, and $k$ disjoint copies give $k$ against $2k$.

## Correctness

The [proof](proofs/correctness.md) shows four facts. The set $F$ stays equal to the uncovered offline vertices, so line L7 always adds an edge between two uncovered vertices and $M$ is a matching. Each decision uses only the past and is never undone. Each edge has a covered endpoint, because an online vertex is left unmatched only when all its neighbours are covered, so $M$ is maximal. A maximal matching has at least half the edges of a maximum one, because the disjoint edges of $M^*$ need $\lvert M^* \rvert$ distinct covered vertices and $M$ covers $2\lvert M \rvert$. The gadget above shows that no deterministic algorithm beats $1/2$.

## Complexity

- **Time.** Keep $F$ as a hash set or a Boolean array over $U$. Line L4 costs $O(\lvert N(v_t) \rvert)$, so the whole run costs $O(m + k)$ with $m = \sum_t \lvert N(v_t) \rvert$ and $k = \lvert U \rvert$, plus the cost of CHOOSE. The first-element rule and the uniform random rule are $O(\lvert C \rvert)$.
- **Space.** $O(k)$ for $F$, plus $O(n)$ for the output.
- **Per arrival.** The rule needs no lookahead and no recomputation: $O(\deg v_t)$ time per arrival.

## Properties

- **Competitive ratio $1/2$, tight.** $\mathrm{ALG}(\sigma) \ge \mathrm{OPT}(\sigma)/2$ for each $\sigma$ and each CHOOSE, and some $\sigma$ gives equality for each deterministic CHOOSE.
- **Optimal among deterministic algorithms.** No deterministic online algorithm, greedy or not, has a ratio above $1/2$. A non-greedy rule can be worse: one that leaves $v_t$ unmatched with a free neighbour can lose the only edge of the input.
- **Random choice alone does not help.** RANDOM is still $1/2 + o(1)$ in the worst case (Karp, Vazirani and Vazirani 1990). Against an [adaptive adversary](/adaptive-adversary/), every greedy rule, random or not, is held to $1/2$.
- **Maximal output.** The output is a maximal matching of the final graph, which is the only property the ratio proof uses.
- **Online and irrevocable.** No edge is ever removed, and no offline vertex is ever freed again.

## Variants and improvements

- **Ranking.** Draw one random order of $U$ at the start and always take the first free neighbour in it. The ratio rises to $1 - 1/e$ against an oblivious adversary, which is optimal ([Ranking algorithm](/ranking-algorithm/)).
- **Balance.** If each offline vertex can take $b$ online vertices, assign to the free neighbour with the smallest load. The ratio is $1 - (1 + 1/b)^{-b}$ ([Balance algorithm](/balance-algorithm/)). Any greedy $b$-matching rule is still $1/2$.
- **Vertex weights.** Taking the free neighbour of largest weight is $1/2$-competitive for the weight of the matched offline vertices.
- **Budgets.** In the [online adwords problem](/online-adwords-problem/), the greedy rule "highest bid that fits" is $1/2$-competitive.
- **General graphs and edge arrival.** The same proof works when edges of a general graph arrive one at a time and greedy adds each edge whose two ends are free: the result is a maximal matching, so it is $1/2$-competitive.

## When to use it

Use greedy when decisions must be fast and simple, when the input is not adversarial, or as the baseline that any online matching rule must beat. When the worst case matters and the adversary does not see the coins, use Ranking: it costs one random permutation more and gains about $0.13$ in the ratio. When offline vertices have capacities larger than one, use Balance.

## Pitfalls

- **Leaving a vertex unmatched with a free neighbour.** The bound $1/2$ needs the rule to be greedy. A rule that skips a free neighbour to "save" it can get ratio 0 on an input that stops early.
- **Expecting a random tie break to beat 1/2.** A fresh random choice for each arrival is not Ranking. RANDOM is still $1/2 + o(1)$; the gain of Ranking comes from one correlated order used for all arrivals.
- **Comparing with a maximal matching instead of a maximum one.** $\mathrm{OPT}$ is a maximum matching. Two maximal matchings can differ by a factor 2.
- **Ignoring the adversary model.** The tight example is built after the adversary sees the choice. It applies to every deterministic rule and, with an adaptive adversary, to randomized ones; it does not apply to Ranking against an oblivious adversary.

## Implementations

## History

Karp, Vazirani and Vazirani (1990) defined online bipartite matching and opened their paper with the two facts on this page: each greedy rule matches at least half of the optimum, and no deterministic rule does better. They then showed that RANDOM, the greedy rule with a fresh uniform choice, is still only $1/2 + o(1)$, and that the Ranking rule, with one random order of the offline side, gets $1 - 1/e$. The bound $1/2$ for a maximal matching was known earlier in the offline setting, as the approximation ratio of the greedy matching algorithm.

## References
