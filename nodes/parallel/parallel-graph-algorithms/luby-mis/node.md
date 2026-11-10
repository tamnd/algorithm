---
tag: HV73GG
kind: algorithm
slug: luby-mis
name: Luby's algorithm
aliases:
- Luby algorithm for MIS
- Luby's distributed MIS algorithm
- Luby-Alon-Israeli-Itai algorithm
- Metivier et al. MIS
- parallel MIS
area: parallel/parallel-graph-algorithms
level: advanced
summary: 'Randomized parallel MIS: vertices with locally minimal random priorities join the set and their neighbours are removed each round.'
solves: [maximal-independent-set]
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {expected: O(n + m)}
  depth: {expected: O(log^2 n)}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [maximal-independent-set, linearity-of-expectation, markov-inequality, work-span-model]
see_also: [distributed-mis, jones-plassmann, israeli-itai, random-mate-contraction, ruling-set, kmw-lower-bound, greedy-coloring, maximal-matching]
sources:
  - paper: doi:10.1137/0215074
    title: Michael Luby, A simple parallel algorithm for the maximal independent set problem, SIAM Journal on Computing 15(4), 1986
    locator: pp. 1036 to 1053 (the randomized algorithm with O(log n) expected rounds, and its derandomization with pairwise independent values); section numbers to be checked
  - paper: doi:10.1016/0196-6774(86)90019-2
    title: Noga Alon, László Babai and Alon Itai, A fast and simple randomized parallel algorithm for the maximal independent set problem, Journal of Algorithms 7(4), 1986
    locator: pp. 567 to 583 (an independent randomized algorithm of the same kind, and small sample spaces for its derandomization)
  - paper: doi:10.1007/s00446-010-0121-5
    title: Yves Métivier, John Michael Robson, Nasser Saheb-Djahromi and Akka Zemmari, An optimal bit complexity randomized distributed MIS algorithm, Distributed Computing 23(5-6), 2011
    locator: the analysis by which a round removes half of the edges in expectation; volume, issue and DOI to be checked
---

Luby's algorithm finds a [maximal independent set](/maximal-independent-set/) in rounds. In each round every remaining vertex draws a random priority, the vertices whose priority is smaller than that of all their remaining neighbours join the set, and they leave the graph together with their neighbours. Each round removes at least half of the remaining edges in expectation, so the algorithm takes $O(\log n)$ rounds with high probability and $O(n + m)$ expected work in the [work-span model](/work-span-model/). Luby (1986) and Alon, Babai and Itai (1986) found it at the same time; the half-the-edges argument on this page is the one of Métivier, Robson, Saheb-Djahromi and Zemmari (2011).

Notation on this page: $G = (V, E)$ is an undirected graph with $n$ vertices and $m$ edges, $d(v)$ is the degree of $v$ in the graph that remains at the start of a round, and $N(v)$ is the set of neighbours of $v$ in that graph. $W$ is the work, $S$ the span and $T_p$ the time on $p$ processors. "With high probability" (w.h.p.) means with probability at least $1 - n^{-c}$ for any fixed $c > 0$, with the constant of the bound depending on $c$. The work bound is in expectation and the round bound holds w.h.p.

## In plain words

Every person in the room draws a random ticket number. A person whose number is smaller than the numbers of all their rivals still in the room joins the team. Two rivals cannot both have the smallest number between them, so the team has no rivals in it.

Each new team member then leaves the room, and so do all their rivals: those rivals can never join any more, because they now have a rival in the team. The people left draw new tickets, and the process repeats until the room is empty.

Each round removes about half of the rival pairs or more, so the room empties after a number of rounds that grows with the logarithm of its size. A person with no rivals left joins at once.

## The problem

The input is an undirected graph $G$ as adjacency lists. The output is a set $I \subseteq V$ that is independent (no edge inside $I$) and maximal (every vertex outside $I$ has a neighbour in $I$).

## The algorithm

The priorities of a round are a uniformly random permutation of the live vertices, drawn fresh in each round. Any distinct random values do the same, such as independent uniform reals.

```pseudo id=main
LUBY-MIS(V, E)
L1  I ← ∅; live ← V
L2  while live is not empty do
L3      for all v in live in parallel do r(v) ← a random priority, all distinct, fresh in each round
L4      for all v in live in parallel do join(v) ← (r(v) < r(u) for every live neighbour u)
L5      for all v in live with join(v) in parallel do add v to I
L6      for all v in live in parallel do if join(v) or join(u) for some live neighbour u then mark v removed
L7      live ← the live vertices not marked, and keep only the edges between them      ▷ pack
L8  return I
```

A live vertex with no live neighbours has $join(v)$ true at once, because the condition of line L4 is empty.

## Example

The path $0 - 1 - 2 - 3 - 4 - 5 - 6$, with the priorities of round 1 as in the table.

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $r(v)$ in round 1 | 6 | 0 | 2 | 3 | 4 | 1 | 5 |
| local minimum (L4) | no | yes | no | no | no | yes | no |
| removed in round 1 (L6) | yes | yes | yes | no | yes | yes | yes |

Vertex 1 beats 0 and 2, and vertex 5 beats 4 and 6. Vertex 3 is not a local minimum ($r(3) = 3 > r(2) = 2$), and neither of its neighbours joins, so it survives. In round 2, vertex 3 is live and has no live neighbours, so it joins. The result is $I = \{1, 3, 5\}$ after 2 rounds; the 6 edges fall to 0 in one round.

## Correctness

Independence: two adjacent live vertices cannot both have the smaller priority, so the vertices added in one round are independent; and every vertex that stays live is not adjacent to any member of $I$, because the neighbours of members are removed. Maximality: a vertex leaves only in line L6, either into $I$ or as a neighbour of a vertex that joins. Termination: in each round the live vertex with the least priority joins, so at least one vertex leaves. The proof file proves these facts and the bounds below in full.

## Complexity

**Theorem (proved in the proof file).** Let $m_t$ be the number of live edges at the start of round $t$, counting from $t = 0$. Then $E[m_{t+1} \mid \text{round } t \text{ state}] \le m_t / 2$. So $E[m_t] \le m / 2^t$, the number of rounds $R$ satisfies $E[R] \le \log_2 m + 4$ for $m \ge 1$, and $\Pr[R > (c + 2) \log_2 n + 2] \le n^{-c}$.

*Sketch of the key step.* For an edge $\{u, v\}$, let $A(u \to v)$ be the event that $u$ has the least priority in $N(u) \cup N(v)$. Then $u$ joins and $v$ leaves with all its $d(v)$ edges. The events $A(u \to v)$ for a fixed $v$ are disjoint, and each has probability at least $1/(d(u) + d(v))$. Summing $d(v) / (d(u) + d(v))$ over both directions of each edge gives at least $m$, and each removed edge is counted at most twice, which gives $m / 2$.

**Cost of a round.** In the work-span model, line L4 is a minimum over the live neighbours of each vertex, line L6 an OR, and line L7 a [pack](/parallel-pack/); a random permutation costs $O(n_t)$ expected work and $O(\log n)$ span. So a round with $n_t$ live vertices and $m_t$ live edges costs $O(n_t + m_t)$ work and $O(\log n)$ span.

**Totals.** A live vertex with a live neighbour is an end of a live edge, so there are at most $2 m_t$ of them, and a live vertex without one joins in that round. So $\sum_t n_t \le n + 2 \sum_t m_t$, and $E[\sum_t m_t] \le 2m$. Hence

$$E[W] = O(n + m), \qquad S = O(\log^2 n) \text{ w.h.p.}$$

On the CRCW PRAM with a priority or a minimum write, each round takes $O(1)$ time apart from the permutation and the pack. By [Brent's theorem](/brent-theorem/), $T_p = O((n + m) / p + \log^2 n)$ in expectation. In the tests, on random graphs with $4n$ edges, the mean number of rounds is 3.2 for $n = 64$, 3.3 for $n = 256$ and 3.9 for $n = 1{,}024$, well below $\log_2 n$; on these graphs the edges fall by far more than half in each round.

## Properties

- **Randomized, Las Vegas.** The output is always a maximal independent set; only the number of rounds is random.
- **Local.** A vertex decides from its own priority and those of its neighbours, so the algorithm runs unchanged as a distributed algorithm in the LOCAL model, with $O(\log n)$ rounds w.h.p.; see [distributed MIS](/distributed-mis/).
- **Fresh randomness per round.** The bound needs new priorities in every round. With priorities fixed once, the output is the greedy MIS for that order, and the number of rounds is its dependence length.
- **Not the greedy MIS.** The output depends on the random choices and is in general not the lexicographically first MIS of any fixed order.

## Variants and improvements

- **Luby's marking form.** In Luby's paper, each vertex marks itself with probability $1/(2 d(v))$, and when two adjacent vertices are both marked, the one of smaller degree unmarks, with ties broken by name. The marked vertices join. The analysis shows that a constant fraction of the edges leaves in each round in expectation.
- **Derandomization.** Luby shows that the analysis needs only pairwise independent random choices, which come from a sample space of polynomial size. Trying all points in parallel gives a deterministic algorithm with $O(\log^2 n)$ time on a polynomial number of processors.
- **Random-order greedy.** If each vertex draws its priority once and keeps it, the algorithm computes the greedy MIS of the random order. Blelloch, Fineman and Shun (2012) show that this takes $O(\log^2 n)$ rounds w.h.p., and Fischer and Noever (2018) improve this to $O(\log n)$. The output is then fixed by the order.
- **Coloring.** [Jones-Plassmann](/jones-plassmann/) uses one fixed random priority per vertex to color the graph greedily, one local-minimum step at a time.
- **Matching.** [Israeli-Itai](/israeli-itai/) adapts the idea to maximal matching, which is an MIS of the line graph.

## When to use it

Use it whenever an MIS, or a symmetry-breaking step built on one, is needed on a parallel or distributed machine: graph coloring, coarsening in multigrid and graph partitioning, and the choice of cluster centers. It is simple, needs only neighbour reads, and does linear expected work. If the output must not depend on the random choices made at run time, use the random-order greedy variant with a seeded order.

## Pitfalls

- **Ties in the priorities.** With priorities from a small range, two adjacent vertices with equal minimal priorities either both join, which breaks independence, or both wait. Use distinct priorities, or break ties by vertex name.
- **Forgetting the neighbours of the new members.** If only the members leave, their neighbours stay live and can join in a later round, next to a member.
- **Comparing against removed vertices.** Line L4 must compare only with live neighbours. A vertex with a smaller-priority neighbour that already left would wait for ever.
- **Reusing the priorities without saying so.** With fixed priorities the algorithm is still correct, but the half-the-edges bound no longer applies to each round; the round count is then the dependence length of the greedy order.
- **Reading the edge bound as a vertex bound.** The number of live vertices does not have to halve; on a star, when a leaf has the least priority, the round removes only that leaf and the center, and the other leaves join together in the next round. The bound is on edges.

## Implementations

## History

Karp and Wigderson (1985) gave the first NC algorithm for MIS, with $O(\log^4 n)$ time. In 1985 and 1986, Luby and, independently, Alon, Babai and Itai gave simple randomized algorithms with $O(\log n)$ expected rounds and showed how to derandomize them with limited independence. Israeli and Itai (1986) applied the same ideas to maximal matching. Métivier, Robson, Saheb-Djahromi and Zemmari (2011) gave the short analysis by edges used here, for the random-priority form, in the setting of distributed algorithms with few bits per message.

## References
