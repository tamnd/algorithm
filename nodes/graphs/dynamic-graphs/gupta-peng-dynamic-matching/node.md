---
tag: PZK1QP
kind: algorithm
slug: gupta-peng-dynamic-matching
name: Gupta-Peng dynamic matching algorithm
aliases:
- Gupta-Peng (1+eps)-approximate dynamic matching
area: graphs/dynamic-graphs
level: research
summary: Maintains a (1+epsilon)-approximate maximum matching under edge updates.
solves: [dynamic-matching]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, ε: the accuracy parameter}
  time: {worst: O(m^(1/2) / ε^2)}
  space: {extra: O(m + n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [maximum-matching, augmenting-path, fully-dynamic-graph, lazy-rebuilding]
see_also: [dynamic-matching, dynamic-vertex-cover, maximal-matching, hopcroft-karp, edmonds-blossom, global-rebuilding, worst-case-update-time, oblivious-adversary]
sources:
  - paper: "Manoj Gupta and Richard Peng, Fully dynamic (1+ε)-approximate matchings, Proceedings of the 54th IEEE Symposium on Foundations of Computer Science (FOCS 2013), 548 to 557"
    locator: the stability lemma (a matching stays approximate for about ε times its size updates), the rebuild by short augmenting paths, the reduction for small matchings, and the main theorem (O(m^(1/2) ε^(-2)) worst-case update time, deterministic)
  - paper: "Mark Overmars, The design of dynamic data structures, Lecture Notes in Computer Science 156, Springer (1983)"
    locator: global rebuilding, the method of spreading a periodic rebuild over the following updates
  - paper: "John E. Hopcroft and Richard M. Karp, An n^(5/2) algorithm for maximum matchings in bipartite graphs, SIAM Journal on Computing 2(4), 225 to 231 (1973)"
    locator: the phases of shortest augmenting paths, and the bound that stopping after O(1/ε) phases gives a (1 + ε)-approximate matching
---

The Gupta-Peng algorithm keeps a $(1 + \varepsilon)$-approximate [maximum matching](/maximum-matching/) of a graph under edge insertions and deletions in $O(m^{1/2} / \varepsilon^2)$ worst-case time per update, deterministically. Its central idea is **stability**: a matching that is close to maximum stays close to maximum for about $\varepsilon$ times its size updates, because one update changes the maximum matching size by at most one. So the algorithm rebuilds a near-maximum matching only every $\Theta(\varepsilon |M|)$ updates, and between rebuilds it only drops deleted edges. With a rebuild in $O(m / \varepsilon)$ time by short [augmenting paths](/augmenting-path/), this costs $O(m / (\varepsilon^2 |M|))$ per update; a reduction for small matchings and the spreading of each rebuild over the next updates give the worst-case bound. Gupta and Peng presented it at FOCS 2013. It is fully dynamic and works in general graphs.

## In plain words

Pair up people who know each other, as many pairs as possible. Friendships begin and end over time.

A good set of pairs does not go bad quickly. When one friendship changes, the best possible number of pairs changes by at most one, and the current set loses at most one pair. So if the set is nearly the best, it stays nearly the best for a while.

So the program does the hard work of finding a nearly best set only now and then. In between, it just throws out pairs whose friendship ended. The bigger the set, the longer it can wait, so the hard work spreads thin over many changes.

## The problem

The input is a number $n$ of vertices, an accuracy $\varepsilon > 0$, and a sequence of edge insertions and deletions of an undirected graph $G$ with $m$ edges. After each update, the algorithm must hold a [matching](/maximum-matching/) $M$ of the current graph with

$$(1 + \varepsilon) \cdot |M| \ge \nu(G),$$

where $\nu(G)$ is the size of a maximum matching. This is the approximate form of [dynamic matching](/dynamic-matching/). The update time is measured per update, in the worst case.

## The algorithm

The core is lazy rebuilding. Let $M$ be the matching after the last rebuild and $b = \lfloor \varepsilon |M| / (2 + \varepsilon) \rfloor$ the number of updates it can absorb.

```pseudo id=main
REBUILD
L1  M ← a maximum matching of G (or (1 + ε/2)-approximate); b ← ⌊ε|M| / (2 + ε)⌋; c ← 0

INSERT(u, v)
L2  add the edge; if u and v are both free then add {u, v} to M

DELETE(u, v)
L3  remove the edge; if {u, v} ∈ M then remove it from M

after each update
L4  c ← c + 1
L5  if c > b then REBUILD

QUERY
L6  return M
```

Line L1 computes a good matching from scratch. In the paper this is a $(1 + \varepsilon/2)$-approximate matching found with $O(1/\varepsilon)$ phases of shortest augmenting paths, as in [Hopcroft-Karp](/hopcroft-karp/), extended to general graphs, in $O(m / \varepsilon)$ time; the implementation here uses [Edmonds' blossom algorithm](/edmonds-blossom/) for an exact maximum matching. Lines L2 and L3 keep $M$ a matching of the current graph. Line L5 starts a rebuild once the budget is used up.

The full algorithm adds two steps.

- **Small matchings.** When $\nu(G)$ is small compared to $m^{1/2}$, the budget is small and rebuilds are frequent. Then the paper works on a smaller graph that still holds a near-maximum matching, built around a small vertex cover, so each rebuild is cheap.
- **Worst-case time.** Instead of rebuilding at once, the new matching is computed in pieces during the next $b/2$ updates, while the old one still serves, with a smaller budget so that the guarantee holds throughout; this is [global rebuilding](/global-rebuilding/).

## Example

Take a path on the vertices $0, 1, \ldots, 11$ and $\varepsilon = 1$. After the 11 insertions, the last rebuild left the perfect matching $\{01, 23, 45, 67, 89, (10\ 11)\}$ with $|M| = 6$, so $b = \lfloor 6/3 \rfloor = 2$.

| update | $M$ after it | $\lvert M \rvert$ | $\nu(G)$ | $c$ | rebuild |
|---|---|---|---|---|---|
| delete 01 | 23, 45, 67, 89, (10 11) | 5 | 5 | 1 | |
| delete 23 | 45, 67, 89, (10 11) | 4 | 5 | 2 | |
| delete 45 | 12, 34, 67, 89, (10 11) | 5 | 5 | 0 | yes, $b = 1$ |
| insert 02 | 12, 34, 67, 89, (10 11) | 5 | 5 | 1 | |
| delete 67 | 12, 34, 56, 89, (10 11) | 5 | 5 | 0 | yes, $b = 1$ |

After the second deletion, $M$ has 4 edges and $\nu(G) = 5$, and $(1 + 1) \cdot 4 \ge 5$, so $M$ is still within the factor. The third deletion leaves 3 edges, more than the budget allows, and the rebuild adds the edges 12 and 34, each an augmenting path of one edge between free vertices. The insertion of 02 is absorbed: both of its ends are matched, and nothing is rebuilt.

## Correctness

The **stability lemma**: let $M_0$ be a matching with $(1 + \varepsilon') |M_0| \ge \nu(G_0)$, and let $t$ updates follow, after which $M_t$ is $M_0$ without its deleted edges. Each update changes $\nu$ by at most one and removes at most one edge of $M$, so $\nu(G_t) \le (1 + \varepsilon')|M_0| + t$ and $|M_t| \ge |M_0| - t$. Then $(1 + \varepsilon)|M_t| \ge \nu(G_t)$ holds whenever $t (2 + \varepsilon) \le (\varepsilon - \varepsilon') |M_0|$. With an exact rebuild, $\varepsilon' = 0$, which gives the budget $b$ of line L1. Edges added at line L2 only make $M$ larger. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Amortized cost of rebuilds.** A rebuild by $O(1/\varepsilon)$ phases of augmenting paths costs $O(m / \varepsilon)$ and serves $\Theta(\varepsilon |M|)$ updates, so it costs $O(m / (\varepsilon^2 |M|))$ amortized per update, which is $O(m / (\varepsilon^2 \nu))$.
- **Large matchings.** If $\nu \ge m^{1/2}$, this is at most $O(m^{1/2} / \varepsilon^2)$.
- **Small matchings.** If $\nu < m^{1/2}$, the paper's reduction to a smaller graph keeps the rebuild cost in proportion, and the bound is again $O(m^{1/2} / \varepsilon^2)$.
- **Worst case.** Spreading each rebuild over the next updates turns the amortized bound into a worst-case bound, $O(m^{1/2} / \varepsilon^2)$ per update.
- **This implementation.** The rebuild uses Edmonds' algorithm in $O(n^3)$ time, so it has the stability guarantee but not the time bound.
- **Space.** $O(m + n)$.
- **Deterministic.** The bound holds against an adaptive adversary.

## Properties

- **Fully dynamic.** Insertions and deletions in any order.
- **Worst case.** The final bound is per update, not amortized.
- **Deterministic.**
- **Approximate.** The factor is $1 + \varepsilon$ for any fixed $\varepsilon > 0$; the cost grows as $\varepsilon^{-2}$.
- **Black box.** Any static approximate matching algorithm can be used for the rebuild, and the bound follows from its running time.

## Variants and improvements

- **Weighted graphs.** Gupta and Peng also give a $(1 + \varepsilon)$-approximate maximum weight matching, with a larger dependence on $\varepsilon$ and a logarithmic factor in the ratio of the weights.
- **Factor 2 and below.** A [maximal matching](/maximal-matching/) is 2-approximate and can be kept in $O(1)$ amortized expected time against an [oblivious adversary](/oblivious-adversary/); this also gives a [dynamic vertex cover](/dynamic-vertex-cover/). Many later algorithms target factors between 1.5 and 2 in polylogarithmic or $n^{o(1)}$ time.
- **Size only.** Estimating $\nu$ within $1 + \varepsilon$ without keeping the matching can be done faster in some settings.
- **Lower bounds.** Conditional lower bounds show that keeping an exact maximum matching, or even its exact size, needs polynomial update time; see [dynamic matching](/dynamic-matching/).

## When to use it

Use it when a graph changes by single edges, a near-maximum matching is needed after each change, and the matching is large, so that rebuilds are rare. The lazy rebuild alone is short to write: a static matching routine, a counter and a budget. For a 2-approximation, a dynamic maximal matching is much faster. When exactness is needed, recompute or use augmenting paths after each update.

## Pitfalls

- **A budget that ignores insertions.** Insertions can raise $\nu$ by one each, so they count toward the budget like deletions.
- **Rebuilding from the old matching only.** A rebuild must reach a $(1 + \varepsilon')$-approximate matching of the current graph, for example by augmenting the current $M$ until no short augmenting path is left. Keeping the old matching without augmentation does not restart the budget.
- **Zero budget.** When $\varepsilon |M| < 2 + \varepsilon$, the budget is 0, and the structure rebuilds after every update. This is correct, and it is the case the reduction for small matchings is for.
- **Bipartite-only rebuilds.** In a general graph, augmenting paths need blossoms; Hopcroft-Karp alone is not enough.

## Implementations

## History

Before 2013, dynamic matching algorithms kept maximal matchings with factor 2, such as Baswana, Gupta and Sen (2011), or exact matchings with polynomial update time, such as Sankowski (2007). Gupta and Peng (FOCS 2013) gave the first $(1 + \varepsilon)$-approximation with sublinear worst-case update time, with a simple argument from stability. The same stability idea, with periodic rebuilds, became a standard tool for dynamic approximate matching and related problems.

## References
