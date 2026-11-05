---
tag: DEFDTW
kind: concept
slug: maximal-matching
name: Maximal matching
aliases:
- inclusion-maximal matching
area: graphs/matching
level: intro
summary: A matching to which no edge can be added; found greedily and a 2-approximation for minimum vertex cover.
prereqs: [undirected-graph, greedy-algorithm]
see_also: [maximum-matching, vertex-cover-2-approximation, maximal-independent-set, line-graph, augmenting-path, distributed-maximal-matching, streaming-maximal-matching-problem, maximum-weight-matching]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 35.1, The vertex-cover problem (APPROX-VERTEX-COVER picks the edges of a maximal matching, Theorem 35.1)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer
    locator: Chapter 1, Introduction (cardinality vertex cover, maximal matchings as a lower bound on OPT, and the tight example)
  - paper: doi:10.1137/0138030
    title: Mihalis Yannakakis and Fanica Gavril, Edge dominating sets in graphs, SIAM Journal on Applied Mathematics 38(3), 364 to 372 (1980)
    locator: the whole paper (minimum maximal matching equals minimum edge dominating set, and NP-completeness)
  - paper: "Amos Israeli and Alon Itai, A fast and simple randomized parallel algorithm for maximal matching, Information Processing Letters 22(2), 77 to 80 (1986)"
    locator: the whole paper (the randomized algorithm with O(log n) expected rounds)
---

A maximal matching of a graph is a [matching](/maximum-matching/) that is not a proper subset of another matching: every edge outside it shares an end with an edge inside it. It is a local notion, unlike a maximum matching, which has the largest size of all matchings. A greedy scan over the edges finds a maximal matching in linear time, and each maximal matching has at least half the size of a maximum one. Its end vertices form a [vertex cover](/vertex-cover/) at most twice the minimum, which is the classic [2-approximation for vertex cover](/vertex-cover-2-approximation/).

## In plain words

A group of people want to form pairs, and two people can pair only if they know each other. You go through the list of friendships one by one. If both friends are still alone, you pair them. Otherwise you skip the friendship. At the end no friendship is left with two people who are both alone. That set of pairs is a maximal matching.

It can be smaller than the best possible set of pairs. An early pair can block two later pairs, so you can end with about half of the best number of pairs. It can never be worse than half: each pair that you made touches at most two pairs of the best solution.

## The idea

Let $G = (V, E)$ be an [undirected graph](/undirected-graph/), without weights, bipartite or general. Self-loops are ignored. A *matching* is a set $M \subseteq E$ of edges such that no two edges of $M$ share an end. A vertex is *covered* by $M$ if it is an end of an edge of $M$, and *exposed* otherwise; $V(M)$ is the set of covered vertices, so $|V(M)| = 2|M|$.

**Definition.** A matching $M$ is *maximal* if no edge $e \in E \setminus M$ makes $M \cup \{e\}$ a matching. Equivalently, every edge of $G$ has at least one end in $V(M)$, that is, $V(M)$ is a vertex cover, and the exposed vertices form an [independent set](/independent-set/).

A matching is *maximum* if no matching of $G$ has more edges. Its size is the matching number $\nu(G)$. Each maximum matching is maximal, but not the other way round.

**Greedy construction.** Start with $M = \emptyset$. Scan the edges in any order and add the edge $\{u, v\}$ to $M$ when both $u$ and $v$ are exposed. With a Boolean array for "covered", this takes $O(|V| + |E|)$ time. The result is maximal: when an edge $\{u, v\}$ was skipped, $u$ or $v$ was already covered, and covered vertices stay covered. Each maximal matching is the output of the scan for some order: put its own edges first.

**Fact 1 (half of the maximum).** For each maximal matching $M$ and each matching $M^*$, $|M^*| \le 2|M|$. So $|M| \ge \nu(G)/2$.

*Proof.* Each edge of $M^*$ has an end in $V(M)$, because $V(M)$ is a vertex cover. The edges of $M^*$ are disjoint, so different edges of $M^*$ use different vertices of $V(M)$ for this. So $|M^*| \le |V(M)| = 2|M|$. $\square$

**Fact 2 (vertex cover).** For each maximal matching $M$, the set $V(M)$ is a vertex cover with $|V(M)| = 2|M| \le 2\tau(G)$, where $\tau(G)$ is the least size of a vertex cover.

*Proof.* $V(M)$ is a vertex cover by maximality. Each vertex cover $C$ contains an end of each edge of $M$, and these ends are distinct because the edges of $M$ are disjoint. So $|C| \ge |M|$, and $|V(M)| = 2|M| \le 2|C|$. $\square$

Both bounds are tight. On the path $a - b - c - d$, the matching $\{bc\}$ is maximal with size 1, while $\{ab, cd\}$ has size 2. On a [complete graph](/complete-graph/) $K_{2k}$, each maximal matching is perfect, so $V(M)$ has all $2k$ vertices, while the least vertex cover has $2k - 1$; on $k$ disjoint edges the factor 2 is exact.

**Smallest maximal matching.** The least size of a maximal matching equals the least size of an *edge dominating set*, a set $F$ of edges such that each edge shares an end with an edge of $F$. Finding it is NP-hard, even for planar bipartite graphs of maximum degree 3, by Yannakakis and Gavril. Fact 1 shows that any maximal matching is a 2-approximation for this problem as well.

**Line graph view.** The matchings of $G$ are the [independent sets](/independent-set/) of the [line graph](/line-graph/) $L(G)$, so the maximal matchings of $G$ are the [maximal independent sets](/maximal-independent-set/) of $L(G)$.

## Examples

**A graph with six vertices.** Take the path $a - b - c - d - e - f$ and add the chord $b - e$, so $E = \{ab, bc, cd, de, ef, be\}$. Scan the edges in the order $be, ab, bc, cd, de, ef$.

| edge | ends exposed? | action | $M$ |
|---|---|---|---|
| $be$ | yes | add | $\{be\}$ |
| $ab$ | $b$ covered | skip | $\{be\}$ |
| $bc$ | $b$ covered | skip | $\{be\}$ |
| $cd$ | yes | add | $\{be, cd\}$ |
| $de$ | both covered | skip | $\{be, cd\}$ |
| $ef$ | $e$ covered | skip | $\{be, cd\}$ |

The result $\{be, cd\}$ is maximal, of size 2. The exposed vertices $a$ and $f$ are not adjacent. A maximum matching is $\{ab, cd, ef\}$, of size 3, and it is also perfect. The vertex cover $V(M) = \{b, c, d, e\}$ has 4 vertices, while $\{b, d, e\}$ is a least vertex cover, with 3. The smallest maximal matchings of this graph have 2 edges; there are four of them: $\{be, cd\}$, $\{bc, ef\}$, $\{bc, de\}$ and $\{ab, de\}$.

**Small cases.**

- The graph with no edges: the empty matching is maximal and maximum.
- A triangle: each single edge is a maximal matching and a maximum one. The third vertex stays exposed, because the triangle has an odd number of vertices. A maximal matching does not need to be perfect.
- A star $K_{1,r}$: each single edge is maximal and maximum, since all edges share the center.

**Non-example.** In the path $a - b - c - d - e$, the matching $\{bc\}$ is not maximal: the edge $de$ has two exposed ends. Adding it gives $\{bc, de\}$, which is maximal and of size 2, equal to $\nu$.

**Maximal is not maximum.** The matching $\{bc\}$ of the path $a - b - c - d$ is maximal, but it has an [augmenting path](/augmenting-path/) $a\,b\,c\,d$. By [Berge's lemma](/berge-lemma/), a matching is maximum exactly when it has no augmenting path. A maximal matching only excludes augmenting paths of one edge.

## Where it is used

- **Approximate vertex cover.** Fact 2 is the algorithm APPROX-VERTEX-COVER of CLRS and the [2-approximation for vertex cover](/vertex-cover-2-approximation/). No algorithm with a ratio of $2 - \varepsilon$ is known, and the [inapproximability of vertex cover](/vertex-cover-inapproximability/) explains why.
- **Start of exact algorithms.** [Hopcroft-Karp](/hopcroft-karp/), [Kuhn's algorithm](/kuhn-algorithm/) and [Edmonds' blossom algorithm](/edmonds-blossom/) are often started from a greedy maximal matching. It already has at least half of the final size, which saves many augmentations in practice.
- **Weighted greedy.** Scan the edges in order of decreasing weight. The result is a maximal matching of weight at least half the [maximum weight](/maximum-weight-matching/), for nonnegative weights: each edge $e$ of an optimal matching was skipped because of a greedy edge of weight at least $w(e)$ that shares an end with it, or it is itself a greedy edge, and each greedy edge is charged by at most two optimal edges.
- **Parallel, distributed and streaming models.** A maximal matching needs only local decisions, so it is the basic matching problem of these models: see [distributed maximal matching](/distributed-maximal-matching/), the [streaming maximal matching problem](/streaming-maximal-matching-problem/) and [greedy streaming matching](/greedy-streaming-matching/). Israeli and Itai gave a randomized parallel algorithm that uses $O(\log n)$ rounds in expectation.
- **Online matching.** In [online bipartite matching](/online-bipartite-matching/) the greedy rule keeps a maximal matching and is $1/2$-competitive by Fact 1.

## References
