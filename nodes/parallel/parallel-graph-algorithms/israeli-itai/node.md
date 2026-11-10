---
tag: NSTYXT
kind: algorithm
slug: israeli-itai
name: Israeli-Itai matching
aliases:
- Israeli-Itai parallel maximal matching
area: parallel/parallel-graph-algorithms
level: advanced
summary: Randomized parallel algorithm computing a maximal matching in O(log n) expected rounds.
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {expected: O(n + m)}
  depth: {expected: O(log^2 n)}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [maximal-matching, linearity-of-expectation, markov-inequality, work-span-model]
see_also: [luby-mis, maximal-independent-set, distributed-maximal-matching, locally-dominant-matching, maximum-matching, line-graph, vertex-cover-2-approximation, random-mate-contraction]
sources:
  - paper: doi:10.1016/0020-0190(86)90144-4
    title: Amos Israeli and Alon Itai, A fast and simple randomized parallel algorithm for maximal matching, Information Processing Letters 22(2), 1986
    locator: pp. 77 to 80 (the round of proposals, the graph of largest degree 2, and the O(log n) expected rounds); DOI and pages to be checked
  - paper: doi:10.1137/0215074
    title: Michael Luby, A simple parallel algorithm for the maximal independent set problem, SIAM Journal on Computing 15(4), 1986
    locator: pp. 1036 to 1053 (maximal matching as a maximal independent set of the line graph)
  - paper: doi:10.1145/2312005.2312058
    title: Guy E. Blelloch, Jeremy T. Fineman and Julian Shun, Greedy sequential maximal independent set and matching are parallel on average, SPAA 2012
    locator: the random-order greedy maximal matching and its round bound; DOI to be checked
---

The Israeli-Itai algorithm finds a [maximal matching](/maximal-matching/) of a graph in parallel rounds. In each round every vertex proposes to a random neighbour, every vertex keeps one of the proposals it gets, and the kept edges form paths and cycles; each vertex then picks one of its kept edges at random, and an edge picked by both its ends joins the matching. A round removes a constant fraction of the remaining edges in expectation, so the algorithm takes $O(\log n)$ rounds with high probability and $O(n + m)$ expected work.

Notation on this page: $G = (V, E)$ is an undirected graph with $n$ vertices and $m$ edges. In round $t$, $G_t$ is the remaining graph, $m_t$ its number of edges, and $d(v)$ and $N(v)$ the degree and the neighbours of $v$ in $G_t$. $W$ is the work, $S$ the span and $T_p$ the time on $p$ processors. The model is the [work-span model](/work-span-model/) with arbitrary concurrent writes (line L4 needs one); this is the arbitrary CRCW PRAM in work-span terms. The work bound is in expectation; the round bound holds with high probability (w.h.p.), that is, with probability at least $1 - n^{-c}$ for any fixed $c > 0$.

## In plain words

People in a room want to form pairs, and only friends can pair up. No pair may share a person, and at the end no two unpaired friends may be left.

In each round, every person who still has an unpaired friend asks one of those friends, chosen at random. A person who gets asked accepts one of the askers. Now each person holds at most two links: the one they asked, if accepted, and the one they accepted.

Each person then points at one of their links at random. When two people point at each other, they become a pair and leave the room.

A person whose friends are mostly less popular gets asked often, so such a person pairs up with a fair chance. Many friendships end in each round, and the room soon has no unpaired friends left.

## The problem

The input is an undirected graph $G$. The output is a matching $M \subseteq E$, a set of edges with no shared end, that is maximal: every edge of $G$ has an end matched by $M$. A maximal matching has at least half the size of a [maximum matching](/maximum-matching/), and its matched vertices form a [vertex cover of at most twice the minimum size](/vertex-cover-2-approximation/).

## The algorithm

Only vertices with at least one remaining edge take part in a round. $H$ is the set of edges $\{v, u\}$ for which $v$ proposed to $u$ and $u$ kept the proposal of $v$.

```pseudo id=main
ISRAELI-ITAI(V, E)
L1  M ← ∅
L2  while some edge remains do
L3      for all v with an edge in parallel do v proposes to a uniformly random neighbour
L4      for all v that got a proposal in parallel do v keeps any one of them
L5      H ← the edges {v, u} where u kept the proposal of v      ▷ every vertex has at most 2 edges in H
L6      for all v with an edge in H in parallel do v picks one of its edges in H uniformly at random
L7      for all edges {u, v} in H picked by both u and v in parallel do add {u, v} to M
L8      remove the matched vertices and all their edges; pack the rest
L9  return M
```

A vertex has at most one edge in $H$ from its own proposal and at most one from the proposal it kept, so $H$ is a set of paths and cycles. Line L4 does not need random choices: the analysis holds for any rule, such as the arbitrary winner of a concurrent write.

This is the form of the round used on this page and in its proof. The paper of Israeli and Itai uses the same three steps: random proposals, one kept proposal, and a matching found inside the paths and cycles of largest degree 2.

## Example

The graph has the vertices 0 to 5 and the edges $\{0,1\}$, $\{1,2\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{1,4\}$. In round 1 the random choices are as in the table.

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| proposes to (L3) | 1 | 2 | 1 | 4 | 1 | 4 |
| proposals got | none | 0, 2, 4 | 1 | none | 3, 5 | none |
| keeps (L4) | | 0 | 1 | | 5 | |
| edges in $H$ (L5) | $\{0,1\}$ | $\{0,1\}$, $\{1,2\}$ | $\{1,2\}$ | none | $\{4,5\}$ | $\{4,5\}$ |
| picks (L6) | $\{0,1\}$ | $\{0,1\}$ | $\{1,2\}$ | | $\{4,5\}$ | $\{4,5\}$ |
| matched (L7) | yes | yes | no | no | yes | yes |

The edges $\{0,1\}$ and $\{4,5\}$ join $M$. Removing 0, 1, 4 and 5 leaves the single edge $\{2,3\}$. In round 2, vertices 2 and 3 propose to each other, keep each other, and pick the edge $\{2,3\}$. The result $M = \{\{0,1\}, \{2,3\}, \{4,5\}\}$ is a perfect matching, found in 2 rounds; the number of edges went from 6 to 1 to 0.

## Correctness

Each vertex picks one edge in line L6, so the edges added in one round have no shared end, and line L8 removes their ends with all their edges, so later rounds cannot add an edge at a matched vertex. The loop stops only when no edge remains, and an edge is removed only when one of its ends is matched, so $M$ is maximal. The proof file proves this in full, together with the bounds below.

## Complexity

**Good vertices.** Call a vertex $v$ of $G_t$ good if at least $d(v)/3$ of its neighbours have degree at most $d(v)$. The proof file proves, in full:

1. at least half of the edges of $G_t$ have a good end;
2. a good vertex is matched in round $t$ with probability at least $p = (1 - e^{-1/3})/2 > 0.14$: it gets a proposal with probability at least $1 - e^{-1/3}$, and once it has an edge in $H$, both ends of one of its edges pick it with probability at least $1/2$.

So $E[m_{t+1} \mid G_t] \le q \, m_t$ with $q = 1 - p/2 < 0.93$.

**Rounds.** As for [Luby's algorithm](/luby-mis/), [Markov's inequality](/markov-inequality/) gives $\Pr[R > k] = \Pr[m_k \ge 1] \le m q^k$. So $R \le \lceil 9.8 (c + 2) \log_2 n \rceil$ with probability at least $1 - n^{-c}$, and $E[R] \le 9.8 \log_2 m + 16$. These constants come from the simple proof and are far from tight. In the tests, on random graphs with $2n$ edges, the mean number of rounds is 2.5 for $n = 64$, 3.0 for $n = 256$ and 3.5 for $n = 1{,}024$, and the edges fall by about 89 percent per round instead of the proved 7 percent.

**Work and span.** A round over $n_t$ vertices with an edge and $m_t$ edges costs $O(n_t + m_t)$ work: a random neighbour is one random index into an adjacency array, line L4 is one concurrent write per vertex, lines L6 and L7 look at at most 2 edges per vertex, and line L8 is a [pack](/parallel-pack/). The span of a round is $O(\log n)$, for the pack. Every vertex that takes part has an edge, so $n_t \le 2 m_t$, and $E[\sum_t m_t] \le m / (1 - q)$. So

$$E[W] = O(n + m), \qquad S = O(\log^2 n) \text{ w.h.p.}$$

By [Brent's theorem](/brent-theorem/), $T_p = O((n + m)/p + \log^2 n)$ in expectation.

## Properties

- **Randomized, Las Vegas.** The output is always a maximal matching; only the number of rounds is random.
- **Local.** A vertex needs only its neighbours, so the algorithm runs as a distributed algorithm with $O(\log n)$ rounds w.h.p.; see [distributed maximal matching](/distributed-maximal-matching/).
- **Linear expected work.** Unlike an MIS of the line graph, it never builds the line graph.
- **Approximation.** The result has at least half the edges of a maximum matching.

## Variants and improvements

- **MIS of the line graph.** A maximal matching is a [maximal independent set](/maximal-independent-set/) of the [line graph](/line-graph/). Running [Luby's algorithm](/luby-mis/) on it is correct, but the line graph has $\sum_v \binom{d(v)}{2}$ edges, which can be $\Theta(n m)$, so the work is no longer linear.
- **Random-order greedy matching.** Give each edge a random priority once and add an edge when it has the highest priority among the remaining edges that share an end with it. The result is the sequential greedy matching of that order, and Blelloch, Fineman and Shun (2012) bound the number of rounds by a polylogarithm w.h.p.
- **Weighted matching.** With weights, the same local rule with the heaviest edge at both ends instead of a random choice gives the [locally dominant matching](/locally-dominant-matching/), a $1/2$-approximation of the maximum weight.
- **Deterministic and distributed algorithms.** Deterministic algorithms and lower bounds for the LOCAL model are on the page on [distributed maximal matching](/distributed-maximal-matching/).

## When to use it

Use it to coarsen a graph in multilevel partitioning, to pair up vertices for a contraction step, or to get a fast 2-approximation of vertex cover or a $1/2$-approximation of maximum matching on a parallel machine. If the result must be the same on every run, use the random-order greedy variant with a seeded order.

## Pitfalls

- **Matching every kept proposal.** A vertex can keep one proposal and have its own proposal kept by another vertex, so the kept edges share ends. Lines L6 and L7 are needed to select disjoint edges from $H$.
- **Proposing to removed vertices.** The proposals must use only the remaining edges; otherwise a vertex can propose to a matched vertex and make no progress.
- **Reading the bound as a vertex bound.** The proof shows that edges shrink by a constant factor in expectation; the number of vertices with an edge does not need to.
- **Dropping the isolated vertices too late.** A vertex whose neighbours are all matched has no edges and must leave the active set in the pack, or later rounds do work for it.

## Implementations

## History

Israeli and Itai (1986) gave this algorithm, with $O(\log n)$ expected rounds, at the same time as the randomized MIS algorithms of Luby and of Alon, Babai and Itai. Luby's paper also gives maximal matching through the line graph. The idea of proposals and acceptances is used in many later distributed matching algorithms.

## References
