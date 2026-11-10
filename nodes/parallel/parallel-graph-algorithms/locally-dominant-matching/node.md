---
tag: EHBHSK
kind: algorithm
slug: locally-dominant-matching
name: Locally dominant edge matching
aliases:
- Preis algorithm
- Manne-Bisseling algorithm
area: parallel/parallel-graph-algorithms
level: advanced
summary: 'Parallel 1/2-approximation for weighted matching: add edges that are heaviest at both endpoints, repeat.'
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of edges, r: the number of rounds}
  time: {worst: O(n + m log m)}
  depth: {worst: O(r log n + log^2 n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [maximum-weight-matching, maximal-matching, work-span-model]
see_also: [israeli-itai, distributed-weighted-matching, maximum-weight-matching, jones-plassmann, luby-mis, parallel-merge-sort, union-bound, vertex-cover-2-approximation]
sources:
  - paper: doi:10.1007/3-540-49116-3_24
    title: Robert Preis, Linear time 1/2-approximation algorithm for maximum weighted matching in general graphs, STACS 1999, LNCS 1563
    locator: pp. 259 to 269 (locally dominant edges, the 1/2 bound, and a sequential algorithm in linear time); DOI and pages to be checked
  - url: https://arxiv.org/abs/cs/0410047
    title: Jaap-Henk Hoepman, Simple distributed weighted matchings, 2004
    locator: the distributed algorithm in which each vertex requests its heaviest remaining edge
  - paper: doi:10.1007/978-3-540-68111-3_74
    title: Fredrik Manne and Rob H. Bisseling, A parallel approximation algorithm for the weighted maximum matching problem, PPAM 2007, LNCS 4967
    locator: pp. 708 to 717 (the parallel algorithm with candidate pointers and its implementation); DOI and pages to be checked
---

A locally dominant matching is built from edges that are the heaviest edge at both of their ends. In each round every unmatched vertex points to its heaviest edge to an unmatched neighbour, every edge that gets both pointers joins the matching, and the matched vertices leave. With ties broken by a fixed rule, the result is exactly the greedy matching that takes edges in decreasing weight, so it is a maximal matching with at least half the weight of a [maximum weight matching](/maximum-weight-matching/). After the adjacency lists are sorted, the rounds cost $O(n + m)$ work in total.

Notation on this page: $G = (V, E, w)$ is an undirected graph with $n$ vertices, $m$ edges and weights $w(e)$; $\Delta$ is the largest degree. The key of edge number $i$ is the pair $(w(e_i), i)$, so all keys are distinct and "heavier" means "larger key". $r$ is the number of rounds. $W$ is the work, $S$ the span and $T_p$ the time on $p$ processors, in the [work-span model](/work-span-model/). All bounds are worst case, except the round bound for random weights, which holds with high probability (w.h.p.), that is, with probability at least $1 - n^{-c}$ for any fixed $c > 0$.

## In plain words

Each person in a room has a list of possible partners, and each possible pair has a score. The goal is to form pairs, with nobody in two pairs, and a large total score.

Every person without a partner points at the free person with whom they have the best score. When two people point at each other, they form a pair and leave. People who pointed at someone who just left point again at the best free person still in the room. This repeats until nobody can point at anyone.

The pairs come out the same as if one person had taken the pairs one by one from the best score down, skipping any pair with someone already taken. That simple rule always gets at least half of the best total score.

## The problem

The input is a weighted undirected graph. The output is a matching $M$, a set of edges with no shared end. The goal is a large total weight $w(M)$. Finding a maximum weight matching exactly takes [Edmonds' blossom algorithm](/maximum-weight-matching/) or similar, which is hard to run in parallel; this algorithm gives a matching of weight at least $w(M^*)/2$, where $M^*$ is a maximum weight matching, and the result is also maximal.

An edge is *locally dominant* in a graph if its key is larger than the key of every other edge that shares an end with it.

## The algorithm

The candidate $cand(v)$ of an unmatched vertex $v$ is its heaviest edge to an unmatched neighbour. A vertex only needs a new candidate when the other end of its candidate is matched, so only those vertices do work in a round.

```pseudo id=main
LOCALLY-DOMINANT-MATCHING(V, E, w)
L1  for all v in parallel do sort the edges at v by decreasing key; ptr(v) ← the first one
L2  check ← the vertices with at least one edge
L3  while check is not empty do
L4      for all v in check in parallel do move ptr(v) forward past the edges to matched vertices
L5          cand(v) ← the edge at ptr(v), or none if the list is finished
L6      D ← the edges e = cand(v) with v in check and cand(u) = e at the other end u      ▷ locally dominant
L7      for all {u, v} in D in parallel do match u and v, and add the edge to M
L8      for all matched u in parallel do mark each unmatched neighbour x with cand(x) at u
L9      check ← the marked vertices
L10 return M
```

A vertex that is not in $check$ keeps a candidate whose other end is still unmatched, and that candidate is still its heaviest edge to an unmatched vertex. So in every round, all unmatched vertices point to their heaviest live edge, and the set $D$ of line L6 is the set of locally dominant edges of the remaining graph. A last pass can find that the marked vertices have no edges left; it adds nothing and is not counted as a round.

## Example

The graph has the vertices 0 to 4 and the weighted edges $\{0,1\}$: 5, $\{1,2\}$: 7, $\{2,3\}$: 6, $\{3,4\}$: 3, $\{0,4\}$: 4, $\{1,3\}$: 2.

| round | candidates (L5) | locally dominant (L6) | marked (L8) |
|---|---|---|---|
| 1 | 0: $\{0,1\}$, 1: $\{1,2\}$, 2: $\{1,2\}$, 3: $\{2,3\}$, 4: $\{0,4\}$ | $\{1,2\}$ | 0, 3 |
| 2 | 0: $\{0,4\}$, 3: $\{3,4\}$, and 4 keeps $\{0,4\}$ | $\{0,4\}$ | 3 |
| last pass | 3: none | none | none |

The result is $M = \{\{1,2\}, \{0,4\}\}$ with weight 11, after 2 rounds. It is the greedy matching: in decreasing weight, take $\{1,2\}$, skip $\{2,3\}$ and $\{0,1\}$, take $\{0,4\}$, skip the rest. Here it is also a maximum weight matching; $\{\{0,1\}, \{2,3\}\}$ has the same weight 11.

## Correctness

The proof file proves, in full, that the algorithm returns the greedy matching $G^*$ of the key order. The greedy matching has a local description: an edge is in $G^*$ exactly when no heavier edge that shares an end with it is in $G^*$. The invariant is that every edge added so far is in $G^*$, and every edge removed without being added is not. A locally dominant edge of the remaining graph has no heavier neighbour edge left, and every heavier neighbour edge that was removed is not in $G^*$, so the edge is in $G^*$. The heaviest remaining edge is always locally dominant, so each round adds an edge, and at the end no edge remains, so the matching is maximal and equal to $G^*$.

The weight bound: every edge $f$ of a maximum weight matching $M^*$ is in $G^*$ or shares an end with a heavier edge of $G^*$. Charge $w(f)$ to that edge at the shared end. An edge of $G^*$ gets at most one charge at each of its two ends, each at most its own weight, so $w(M^*) \le 2\, w(G^*)$.

## Complexity

**Work.** Line L1 sorts the adjacency lists, $O(m \log m)$ work in total, or $O(m)$ if the lists come sorted. After that, each pointer only moves forward, so line L4 does $O(m)$ work over the whole run. Each vertex is matched once and marks its neighbours once in line L8, which is $O(m)$ in total. A vertex is in $check$ only after a neighbour of it is matched, so the sizes of the $check$ sets add up to $O(n + m)$. So

$$W = O(n + m \log m), \text{ and } O(n + m) \text{ after the sort.}$$

**Span.** A round has $O(\log n)$ span, for the pack in line L9. The sort has $O(\log^2 n)$ span with a [parallel merge sort](/parallel-merge-sort/). So $S = O(r \log n + \log^2 n)$, and by [Brent's theorem](/brent-theorem/), $T_p = O((n + m \log m)/p + r \log n + \log^2 n)$.

**Rounds.** The number of rounds depends on the weights. The proof file shows that $r$ is at most the number of edges on the longest path of the line graph along which the key decreases. On the path $0, 1, \ldots, n - 1$ with $w(\{i, i+1\}) = i$, only the last remaining edge is ever locally dominant, so $r = \lfloor n/2 \rfloor$: the algorithm is then sequential. If the key order is a uniformly random order of the edges, for example random weights, the proof file proves with the [union bound](/union-bound/) that $r \le \max(2e^2 \Delta, (c + 2) \ln n)$ with probability at least $1 - n^{-c}$. In the tests, on random graphs with $2n$ edges and random weights, the mean number of rounds is 3.2 for $n = 64$, 4.0 for $n = 256$ and 4.3 for $n = 1{,}024$.

## Properties

- **Deterministic.** For fixed keys, the output does not depend on the schedule; it is the greedy matching.
- **1/2-approximation, tight.** On the path with weights $1, 1 + \varepsilon, 1$, the algorithm takes the middle edge, of weight $1 + \varepsilon$, while the two outer edges weigh 2.
- **Maximal.** Every edge has a matched end at the end. With all weights equal and keys broken by index, it is the greedy maximal matching of the index order.
- **Work-efficient after sorting.** The rounds do linear work in total, the same as the sequential pointer algorithm.

## Variants and improvements

- **Sequential linear time.** Preis (1999) finds a locally dominant matching in $O(m)$ time without sorting, by following chains of heavier edges.
- **Distributed form.** Hoepman (2004) gives the same rule as a distributed algorithm in which each vertex sends a request along its heaviest remaining edge; see [distributed weighted matching](/distributed-weighted-matching/).
- **Parallel implementations.** Manne and Bisseling (2007) give the parallel algorithm with candidate pointers for distributed memory. Later shared-memory codes, such as the suitor algorithm of Manne and Halappanavar, compute the same matching with fewer synchronizations.
- **Random weights.** On an unweighted graph, random keys turn the algorithm into the random-order greedy maximal matching, with few rounds w.h.p. Compare [Israeli-Itai](/israeli-itai/), which draws fresh random choices in each round instead.
- **Better ratios.** Algorithms with ratio $2/3 - \varepsilon$ or $1 - \varepsilon$ use augmentations along short paths; they cost more work and more rounds.

## When to use it

Use it to coarsen weighted graphs in multilevel partitioning and clustering, to find a large-weight matching quickly before an exact method, and as the matching step in sparse matrix ordering and scaling. It suits sparse graphs on shared or distributed memory, where most vertices find their partner in the first few rounds.

## Pitfalls

- **Ties in the weights.** Without a fixed tie-breaking rule, the vertices can point past each other: on a triangle with equal weights, vertex 0 can point to $\{0,1\}$, vertex 1 to $\{1,2\}$ and vertex 2 to $\{2,0\}$, so no edge gets two pointers and no progress is made. Break ties by an edge index, the same at both ends.
- **Recomputing every candidate in every round.** Rescanning all edges in each round costs $O(m)$ work per round, $O(m r)$ in total, which is quadratic on the increasing path. Keep sorted lists and pointers that only move forward.
- **Expecting few rounds for every input.** Sorted weights along a path make the algorithm sequential. If the weights can be adversarial, add a random tie-breaking perturbation, or accept the round count.
- **Edges of weight 0 or less.** The algorithm matches them if nothing better is left. For a maximum weight matching, drop them first.

## Implementations

## History

Preis (1999) introduced locally dominant edges and showed that a matching built from them has at least half the maximum weight, the same ratio as the greedy algorithm studied earlier, while taking linear time. Hoepman (2004) turned the rule into a distributed algorithm. Manne and Bisseling (2007) gave the parallel version with candidate pointers and showed that it scales on distributed-memory machines.

## References
