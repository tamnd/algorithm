---
tag: ZQCPTZ
kind: algorithm
slug: greedy-streaming-matching
name: Greedy streaming matching
aliases:
- semi-streaming greedy matching
area: online-and-streaming/streaming-sketches
level: advanced
summary: Adds an edge of the stream whenever both of its endpoints are free. One pass and O(n log n) bits give a maximal matching, which has at least half the edges of a maximum matching.
solves: [streaming-maximal-matching-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges in the stream}
  time: {worst: O(m)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, one_pass: true, approximation_ratio: 1/2}
history:
  year: 2005
  people: [Joan Feigenbaum, Sampath Kannan, Andrew McGregor, Siddharth Suri, Jian Zhang]
  note: Greedy maximal matching is folklore. Feigenbaum, Kannan, McGregor, Suri and Zhang defined the semi-streaming model in 2005 and used the one-pass greedy algorithm as its basic matching result. No one-pass semi-streaming algorithm with a better ratio for general streams is known.
prereqs: [maximal-matching, maximum-matching, streaming-model, approximation-ratio]
see_also: [streaming-maximal-matching-problem, greedy-online-matching, maximum-weight-matching, hopcroft-karp, edmonds-blossom, agm-graph-sketch, greedy-algorithm, b-matching]
sources:
  - paper: doi:10.1016/j.tcs.2005.09.013
    title: Joan Feigenbaum, Sampath Kannan, Andrew McGregor, Siddharth Suri and Jian Zhang, On graph problems in a semi-streaming model, Theoretical Computer Science 348(2-3), 2005
    locator: pp. 207 to 216; the definition of the semi-streaming model and the section on matching (the greedy maximal matching and the weighted 1/6 algorithm)
  - paper: doi:10.1145/2627692.2627694
    title: Andrew McGregor, Graph stream algorithms, a survey, SIGMOD Record 43(1), 2014
    locator: the section on matchings (greedy, weighted matching, and lower bounds)
  - url: https://arxiv.org/abs/2607.14644
    title: Sepehr Assadi, Max Jiang and Mars Xiang, Semi-streaming matching in a single pass I, a new framework for lower bounds via blueprints, 2026
    locator: the abstract and introduction (the prior bound 1/(1 + ln 2) and the new bound (8 − 2√10)/3 ≈ 0.558 for one pass)
---

Greedy streaming matching reads the edges of a graph once, in the order of the stream, and keeps an edge exactly when neither of its endpoints is already matched. The result is a maximal matching: no edge of the graph can be added to it. A maximal matching has at least half as many edges as a [maximum matching](/maximum-matching/), so the algorithm is a $1/2$-approximation in one pass, with memory for at most $n/2$ edges and one bit per vertex. Despite its simplicity, no one-pass algorithm in the semi-streaming model is known to do better on adversarial streams. On this page $n$ is the number of vertices and $m$ the number of edges in the stream.

## In plain words

At a dance, people arrive in pairs who would like to dance together, one pair at a time. If both people of a pair are still free, they become partners. If one of them already has a partner, the pair is skipped. You only remember who is taken and who dances with whom. At the end, every skipped pair has at least one person who dances with someone. A perfect host could perhaps make more couples, but at most twice as many, because every couple of the host's plan needs one of the people that you already used.

## The problem

The input is a stream of the edges of a graph $G = (V, E)$ with $|V| = n$, in any order, each edge once (repeats are harmless). The output is a matching $M \subseteq E$, a set of edges with no shared endpoint. The goal of the [maximal matching in streams problem](/streaming-maximal-matching-problem/) is a matching whose size is close to the size $\nu(G)$ of a maximum matching, in one pass and $O(n\,\mathrm{polylog}\,n)$ bits. The greedy algorithm guarantees $|M| \ge \nu(G)/2$.

## The algorithm

```pseudo id=main
GREEDY-MATCHING(stream)
L1  M ← ∅; every vertex is free
L2  for each edge {u, v} of the stream, in order, do
L3      if u is free and v is free then
L4          add {u, v} to M; mark u and v as matched
L5  return M
```

The state is the list $M$ and one bit per vertex. With an array of bits the test of line L3 and the update of line L4 take constant time; the code of this page uses a hash set instead.

## Example

Take the 6-cycle $1, 2, 3, 4, 5, 6$ with the edges in the stream order $\{2,3\}$, $\{1,2\}$, $\{3,4\}$, $\{5,6\}$, $\{4,5\}$, $\{1,6\}$.

| edge | free ends | action | matched vertices |
|---|---|---|---|
| $\{2,3\}$ | both | add | 2, 3 |
| $\{1,2\}$ | 1 only | skip | 2, 3 |
| $\{3,4\}$ | 4 only | skip | 2, 3 |
| $\{5,6\}$ | both | add | 2, 3, 5, 6 |
| $\{4,5\}$ | 4 only | skip | 2, 3, 5, 6 |
| $\{1,6\}$ | 1 only | skip | 2, 3, 5, 6 |

The output is $M = \{\{2,3\}, \{5,6\}\}$. The free vertices 1 and 4 are not adjacent, so $M$ is maximal. The cycle has the perfect matching $\{1,2\}, \{3,4\}, \{5,6\}$, so $\nu = 3$, and here greedy has $2/3$ of the optimum. Over all $720$ orders of these six edges, greedy finds 2 or 3 edges.

**The bound 1/2 is tight.** On the path $1, 2, 3, 4$ with the middle edge $\{2,3\}$ first, greedy takes it and must skip $\{1,2\}$ and $\{3,4\}$, so it has 1 edge against $\nu = 2$. Disjoint copies of this path give the ratio exactly $1/2$ for every size.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **M is a matching.** Line L4 adds an edge only when both ends are free and then marks them, so no vertex is in two edges of $M$.
2. **M is maximal.** A matched vertex never becomes free again. When an edge $\{u, v\}$ is read, either both ends are free and it is added, or one end is already matched. In both cases one end of the edge is matched at the end of the stream.
3. **Half of the optimum.** Let $M^*$ be a maximum matching. By step 2, each edge of $M^*$ has an endpoint in $V(M)$, the set of matched vertices. The edges of $M^*$ are disjoint, so they use different such endpoints. Hence $\nu(G) = |M^*| \le |V(M)| = 2|M|$.

## Complexity

**Time.** One test and at most one insertion per edge, so $O(1)$ per edge with a bit array and $O(m)$ in all.

**Space.** At most $\lfloor n/2 \rfloor$ edges of $M$, each in $O(\log n)$ bits, and $n$ bits for the free or matched marks, so $O(n \log n)$ bits, or $O(n)$ words. This fits the semi-streaming model, which allows $O(n\,\mathrm{polylog}\,n)$ bits. The number of edges $m$ can be $\Theta(n^2)$, so the algorithm stores far less than the graph.

**Lower bounds for one pass.** In the semi-streaming model, no one-pass algorithm can reach every ratio below 1 on adversarial streams. Goel, Kapralov and Khanna (SODA 2012) ruled out ratios above $2/3$. Kapralov (SODA 2013) ruled out ratios above $1 - 1/e \approx 0.632$, and Kapralov (SODA 2021) ruled out ratios above $1/(1 + \ln 2) \approx 0.590$. Assadi, Jiang and Xiang (2026) ruled out ratios above $(8 - 2\sqrt{10})/3 \approx 0.558$. Whether some one-pass semi-streaming algorithm beats $1/2$ is open.

## Properties

- **Deterministic and order-dependent.** The output depends on the order of the stream, but the bound $|M| \ge \nu/2$ holds for every order.
- **Online.** Each decision is final when the edge is read, so the algorithm is also an online algorithm for matching with edge arrivals.
- **Vertex cover.** $V(M)$ touches every edge, so it is a vertex cover of size $2|M| \le 2\tau(G)$, where $\tau$ is the minimum vertex cover. So the same pass gives a 2-approximate vertex cover.
- **No deletions.** An edge of $M$ that is deleted later cannot be replaced, since the skipped edges were not stored.

## Variants and improvements

- **Weighted greedy with replacement.** Feigenbaum et al. keep a new edge if its weight is more than twice the total weight of the edges of $M$ that it touches, and then remove those edges. This gives a $1/6$-approximation for maximum weight matching. McGregor (2005) improved the factor to about $1/5.83$ with a better threshold, and Paz and Schwartzman (SODA 2017) reached $1/(2 + \varepsilon)$ with the local ratio technique.
- **More passes.** Augmenting along short paths in further passes reaches $1 - \varepsilon$ with a number of passes that depends only on $\varepsilon$ (McGregor 2005, with later improvements for general and bipartite graphs).
- **Random order.** If the edges arrive in a random order, one pass can beat $1/2$; Konrad, Magniez and Mathieu (2012) gave the first such result.
- **b-matching.** Let each vertex take up to $b$ edges. The same argument gives a $1/2$ approximation for [b-matching](/b-matching/).
- **Dynamic streams.** With deletions, a maximal matching cannot be kept in semi-streaming space in one pass; one uses sketches and accepts an approximation factor that grows with $n$.

## When to use it

Use the greedy algorithm when edges arrive in a stream that you can read once, the graph is too large to store, and a factor 2 is acceptable. It is also the standard first step of multi-pass algorithms, which start from a maximal matching and improve it with augmenting paths. If the graph fits in memory, use [Hopcroft-Karp](/hopcroft-karp/) for bipartite graphs or [Edmonds' blossom algorithm](/edmonds-blossom/) for general graphs to get an exact maximum matching. If edges have weights, plain greedy can be arbitrarily bad; use the weighted variants.

## Pitfalls

- **Weights.** On a path $a, b, c, d$ where $\{a,b\}$ and $\{c,d\}$ have weight 1 and $\{b,c\}$ has weight $W$, with the stream order $\{a,b\}$, $\{c,d\}$, $\{b,c\}$, the greedy algorithm keeps the two edges of weight 1 and misses $W$. Greedy by arrival has no constant ratio for weighted matching.
- **Repeated edges.** A repeated edge is skipped because its ends are already matched, so repeats are harmless. Self-loops are not edges and must be rejected.
- **Expecting better than 1/2.** On some orders greedy finds a maximum matching, but on adversarial orders the factor 1/2 is the truth, as the path example shows.
- **Deletions.** The algorithm does not support edge deletions.

## Implementations

## History

The greedy maximal matching and its factor 2 are folklore from the study of matchings and vertex covers. Feigenbaum, Kannan, McGregor, Suri and Zhang (ICALP 2004, Theoretical Computer Science 2005) defined the semi-streaming model, which allows $O(n\,\mathrm{polylog}\,n)$ space, and gave the greedy matching and a $1/6$ weighted algorithm in one pass. McGregor (APPROX 2005) gave multi-pass $(1 - \varepsilon)$ algorithms. The lower bounds of Goel, Kapralov and Khanna (2012), Kapralov (2013, 2021) and Assadi, Jiang and Xiang (2026) narrowed the gap for one pass, which is now between $1/2$ and about $0.558$.

## References
