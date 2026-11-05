---
tag: TE12XE
kind: problem
slug: dynamic-vertex-cover
name: Dynamic vertex cover
aliases:
- fully dynamic vertex cover
area: graphs/dynamic-graphs
level: research
summary: Maintain a (approximate) minimum vertex cover under edge updates.
prereqs: [vertex-cover, maximal-matching, fully-dynamic-graph]
see_also: [dynamic-matching, gupta-peng-dynamic-matching, vertex-cover-2-approximation, konig-theorem, unique-games-conjecture, kernelization, amortized-update-time, oblivious-adversary]
sources:
  - paper: "Krzysztof Onak and Ronitt Rubinfeld, Maintaining a large matching and a small vertex cover, Proceedings of the 42nd ACM Symposium on Theory of Computing (STOC 2010), 457 to 464"
    locator: the main theorem (a constant-factor approximate vertex cover with O(log^2 n) amortized update time, randomized)
  - paper: "Surender Baswana, Manoj Gupta and Sandeep Sen, Fully dynamic maximal matching in O(log n) update time, SIAM Journal on Computing 44(1), 88 to 113 (2015)"
    locator: Section 1 (a maximal matching in O(log n) expected amortized time against an oblivious adversary, and the 2-approximate vertex cover that follows)
  - paper: "Sayan Bhattacharya, Monika Henzinger and Giuseppe F. Italiano, Deterministic fully dynamic data structures for vertex cover and matching, SIAM Journal on Computing 47(3), 859 to 887 (2018)"
    locator: the vertex cover theorem (a deterministic (2 + ε)-approximation with O(log n / ε^2) amortized update time, by a hierarchical partition of the vertices)
  - paper: "Shay Solomon, Fully dynamic maximal matching in constant update time, Proceedings of the 57th IEEE Symposium on Foundations of Computer Science (FOCS 2016), 325 to 334"
    locator: the main theorem (a maximal matching in O(1) expected amortized time per update)
---

Dynamic vertex cover asks to keep a small [vertex cover](/vertex-cover/) of a graph, a set of vertices that touches every edge, while edges are inserted and deleted. A minimum vertex cover is NP-hard to compute even once, so dynamic algorithms keep an approximate cover, and the standard target is a factor close to 2. The two ends of every edge of a [maximal matching](/maximal-matching/) form a 2-approximate cover, so any dynamic maximal matching gives a dynamic 2-approximate cover; the best known algorithms take $O(1)$ amortized expected time per update against an [oblivious adversary](/oblivious-adversary/), and deterministic algorithms reach a factor $2 + \varepsilon$ in $O(1/\varepsilon^2)$ amortized time. The problem is a central test case of dynamic algorithms for approximate optimization.

## In plain words

Put guards on some corners of a street map so that every street has a guard at one of its two ends. Use as few guards as you can. Streets open and close, and after each change the guard plan must still cover every street.

Finding the best plan is too hard even once, so the program accepts a plan that uses at most about twice as many guards as needed. The classic trick: pick a set of streets that share no corner and to which no other street can be added. Put guards at both ends of each picked street. Any plan must put a guard at one end of each picked street, so this plan uses at most twice the best number.

The work is to repair the set of picked streets fast after each change.

## Definition

A **vertex cover** of a graph $G = (V, E)$ is a set $C \subseteq V$ such that every edge has at least one end in $C$. Let $\tau(G)$ be the size of a minimum vertex cover.

**Dynamic vertex cover.** Start from a graph on $n$ vertices with no edges. A sequence of updates inserts or deletes edges, so the graph is [fully dynamic](/fully-dynamic-graph/). After each update the algorithm must hold a vertex cover $C$ of the current graph $G$ with

$$|C| \le \alpha \cdot \tau(G),$$

where $\alpha \ge 1$ is the **approximation factor**. The algorithm either keeps $C$ explicitly, and the measure includes the number of vertices that enter or leave $C$ per update (the **recourse**), or answers queries such as "is $v$ in the cover?" and "what is $|C|$?". The update time is stated as worst case or amortized, and for randomized algorithms the adversary is usually oblivious.

## Variants

- **Approximation factor.** $\alpha = 2$ (from a maximal matching), $\alpha = 2 + \varepsilon$ (deterministic hierarchical methods), or a constant. Exact covers ($\alpha = 1$) are studied only in special cases.
- **Size only.** Keep only an estimate of $\tau(G)$, not the set itself. This can be easier, as for matchings.
- **Bipartite graphs.** By [König's theorem](/konig-theorem/), $\tau(G)$ equals the size of a [maximum matching](/maximum-matching/) in a bipartite graph, so the exact problem is a [dynamic matching](/dynamic-matching/) problem.
- **Parameterized.** Keep a cover of size at most $k$, or report that none exists, with update time that depends on $k$ only; the methods use [kernelization](/kernelization/).
- **Weighted.** Each vertex has a cost, and the cover must be of near-minimum cost.
- **Hypergraphs and set cover.** Each hyperedge of size at most $f$ must be covered; the dynamic [set cover](/set-cover/) problem with frequency $f$ generalizes vertex cover ($f = 2$).

## Examples

**A 2-approximation by a maximal matching.** Take six vertices and keep a maximal matching $M$ with the rule: after an insertion, match the new edge if both ends are free; after the deletion of a matched edge, try to match each of its ends to a free neighbor. The cover is the set of matched vertices.

| update | maximal matching $M$ | cover $C$ | $\tau(G)$ |
|---|---|---|---|
| insert 01 | 01 | 0, 1 | 1 |
| insert 12 | 01 | 0, 1 | 1 |
| insert 34 | 01, 34 | 0, 1, 3, 4 | 2 |
| insert 45 | 01, 34 | 0, 1, 3, 4 | 2 |
| delete 01 | 12, 34 | 1, 2, 3, 4 | 2 |
| insert 05 | 12, 34, 05 | 0, 1, 2, 3, 4, 5 | 3 |

In the last row the cover has 6 vertices and $\tau(G) = 3$ (for example $\{1, 4, 5\}$), so the factor 2 is reached exactly. When 01 is deleted, vertex 1 finds the free neighbor 2, and vertex 0 has no free neighbor and leaves the cover.

**Why a maximal matching gives a factor 2.** The edges of $M$ share no vertex, so any cover must hold at least one end of each, and $\tau(G) \ge |M|$. The cover of matched vertices has $2|M|$ vertices. It covers every edge, because an edge with two free ends could be added to $M$, which contradicts maximality.

**Why the simple rule is slow.** After a matched edge $\{u, v\}$ is deleted, finding a free neighbor of $u$ scans its neighbors, which takes $\Theta(\deg(u))$ time. An adversary can delete the matched edges of a high-degree vertex again and again, so this rule costs $\Theta(n)$ per update in the worst sequences. The randomized algorithms below match a vertex to a random neighbor, so an oblivious adversary hits the matched edge only rarely.

## Known algorithms

| algorithm | factor | update time | kind |
|---|---|---|---|
| recompute a maximal matching | 2 | $O(m)$ | worst case, deterministic |
| simple local repair | 2 | $O(n)$ | worst case, deterministic |
| Onak and Rubinfeld (2010) | $O(1)$ | $O(\log^2 n)$ | amortized expected, randomized |
| Baswana, Gupta and Sen (2011) | 2 | $O(\log n)$ | amortized expected, oblivious adversary |
| Bhattacharya, Henzinger and Italiano (2015) | $2 + \varepsilon$ | $O(\log n / \varepsilon^2)$ | amortized, deterministic |
| Solomon (2016) | 2 | $O(1)$ | amortized expected, oblivious adversary |
| Bhattacharya and Kulkarni (2019) | $2 + \varepsilon$ | $O(1/\varepsilon^2)$ | amortized, deterministic |

- **Maximal matching methods** (Baswana, Gupta and Sen; Solomon) keep the vertices at levels by degree and match each vertex to a random neighbor at its level. The cover is the set of matched vertices.
- **Hierarchical partitions** (Bhattacharya, Henzinger and Italiano) keep a fractional matching through levels of vertices, where each vertex has a weight that depends on its level, and take the vertices at high levels as the cover. The dual of the fractional matching proves the factor $2 + \varepsilon$. This approach is deterministic and handles an [adaptive adversary](/adaptive-adversary/).
- **Worst-case bounds.** Neiman and Solomon (2013) gave a deterministic maximal matching, and so a 2-approximate cover, with $O(m^{1/2})$ worst-case update time. Later work reached polylogarithmic worst-case time for factors near 2.

## Bounds

- **Static hardness.** Computing $\tau(G)$ is NP-hard, and under the [unique games conjecture](/unique-games-conjecture/) no polynomial-time algorithm achieves a factor $2 - \varepsilon$. So no dynamic algorithm with polynomial update time keeps a cover with a better factor unless the static hardness fails, because a static algorithm can insert the edges one at a time.
- **Upper bounds.** A factor of 2 in $O(1)$ amortized expected time, and $2 + \varepsilon$ deterministically in $O(1/\varepsilon^2)$ amortized time, as in the table.
- **Exact bipartite covers.** Through König's theorem, conditional lower bounds for keeping the size of a maximum matching exactly also apply to exact covers in bipartite graphs; see [dynamic matching](/dynamic-matching/).

## Reductions

- **From maximal matching.** A dynamic maximal matching with update time $T$ gives a dynamic 2-approximate vertex cover with update time $T$ and recourse $O(1)$ per change of the matching.
- **To and from matching size.** In any graph, $\nu(G) \le \tau(G) \le 2\nu(G)$, where $\nu(G)$ is the size of a maximum matching. So a $c$-approximate estimate of $\nu$ gives a $2c$-approximate estimate of $\tau$, and the reverse.
- **Fractional matching duality.** A fractional matching and a fractional vertex cover of equal value certify each other's quality. Deterministic algorithms keep both and round the cover.
- **Static lower bound by insertions.** As above, a dynamic algorithm gives a static algorithm by $m$ insertions, which carries static hardness to the dynamic problem.

## Applications

- **Monitoring of networks.** Vertex covers model sets of monitors that observe every link; links appear and fail over time.
- **A tool inside other dynamic algorithms.** Approximate covers and the matchings that come with them are used in dynamic [matching](/dynamic-matching/) algorithms, such as the [Gupta-Peng algorithm](/gupta-peng-dynamic-matching/), and in dynamic set cover.
- **Benchmarks for techniques.** Hierarchical partitions, primal-dual methods for an adaptive adversary, and methods for worst-case bounds were often developed first for vertex cover and matching.

## References
