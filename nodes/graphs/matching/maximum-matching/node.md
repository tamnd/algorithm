---
tag: 317S62
kind: problem
slug: maximum-matching
name: Maximum matching
aliases:
- maximum cardinality matching
- general matching
area: graphs/matching
level: core
summary: Find a matching with the largest number of edges in a general graph.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m n^(1/2))}
prereqs: [undirected-graph, maximal-matching]
see_also: [bipartite-matching, perfect-matching, maximum-weight-matching, edmonds-blossom, micali-vazirani-algorithm, tutte-berge-formula, berge-lemma, minimum-edge-cover]
sources:
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer
    locator: Chapter 24, Cardinality nonbipartite matching (the Tutte-Berge formula, Edmonds' algorithm, and the history of faster algorithms)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer
    locator: Chapter 10, Maximum Matchings
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17, 449 to 467 (1965)
    locator: the whole paper (the first polynomial algorithm for general graphs)
  - paper: "Harold N. Gabow, An efficient implementation of Edmonds' algorithm for maximum matching on graphs, Journal of the ACM 23(2), 221 to 234 (1976)"
    locator: the whole paper (an O(n^3) implementation)
  - paper: "Silvio Micali and Vijay V. Vazirani, An O(sqrt(|V|) |E|) algorithm for finding maximum matching in general graphs, 21st Annual Symposium on Foundations of Computer Science, 17 to 27 (1980)"
    locator: the whole paper
  - paper: "Marcin Mucha and Piotr Sankowski, Maximum matchings via Gaussian elimination, 45th Annual IEEE Symposium on Foundations of Computer Science, 248 to 255 (2004)"
    locator: the whole paper (a randomized O(n^ω) algorithm)
---

The maximum matching problem asks for a matching with the largest number of edges in an [undirected graph](/undirected-graph/) without weights. The graph is general: it can have odd cycles, unlike in [bipartite matching](/bipartite-matching/). [Edmonds' blossom algorithm](/edmonds-blossom/) solved it in polynomial time in 1965, and the [Micali-Vazirani algorithm](/micali-vazirani-algorithm/) solves it in $O(m \sqrt n)$ time. Its min-max theorem is the [Tutte-Berge formula](/tutte-berge-formula/).

## In plain words

A group of people want to work in pairs, and some pairs of people can work together. Each person can be in at most one pair. The task is to form as many pairs as possible. The pairs are not restricted to two teams: anyone may pair with anyone they are linked to.

Taking pairs greedily can get stuck early: one bad pair can block two good ones. The fix is to look for a chain that starts and ends at two unpaired people and alternates between unused links and current pairs. Swapping along the chain makes one more pair. When no such chain exists, the number of pairs is the largest possible. Finding such chains is harder when the links form cycles of odd length, and that is what the blossom idea solves.

## Definition

Let $G = (V, E)$ be a finite undirected graph with $n = |V|$ and $m = |E|$, without weights. Self-loops can never be in a matching, and parallel edges do not change the answer. A *matching* is a set $M \subseteq E$ such that no two edges of $M$ share an end.

- **Input:** $G$.
- **Output:** a matching $M$ of $G$ with $|M| \ge |M'|$ for each matching $M'$ of $G$.

The size of a maximum matching is the *matching number* $\nu(G)$. A matching is *perfect* if it covers all vertices, which needs $n$ even and $\nu(G) = n/2$. The empty graph has $\nu = 0$, with the empty matching.

**Optimality.** By [Berge's lemma](/berge-lemma/), a matching $M$ is maximum exactly when there is no [augmenting path](/augmenting-path/): no path between two vertices that $M$ leaves exposed whose edges are alternately outside and inside $M$. By the [Tutte-Berge formula](/tutte-berge-formula/),

$$\nu(G) = \min_{U \subseteq V} \frac{|V| + |U| - \operatorname{odd}(G - U)}{2},$$

where $\operatorname{odd}(G - U)$ is the number of connected components of $G - U$ with an odd number of vertices. A set $U$ that reaches the minimum is a short proof that a given matching is maximum.

## Variants

- **Decision:** given $k$, is $\nu(G) \ge k$? The case $k = n/2$ is the [perfect matching](/perfect-matching/) problem.
- **Bipartite:** $G$ has no odd cycle. This is [bipartite matching](/bipartite-matching/), with simpler algorithms and the min-max theorem of [Kőnig](/konig-theorem/).
- **Weighted:** maximize the total weight, in [maximum-weight matching](/maximum-weight-matching/), or find a [minimum-weight perfect matching](/minimum-weight-perfect-matching/).
- **Maximal:** only ask that no edge can be added. A [maximal matching](/maximal-matching/) is found in linear time and has at least half the maximum size.
- **Approximate:** a matching of size at least $(1 - \varepsilon)\nu(G)$.
- **Degree bounds:** each vertex $v$ may be in up to $b(v)$ edges, the [b-matching](/b-matching/) problem, or in exactly $f(v)$ edges, the [f-factor problem](/f-factor-problem/).
- **Counting:** count the perfect matchings. This is [#P-complete](/counting-perfect-matchings/), even for bipartite graphs, while the search problem is in polynomial time.
- **Other models:** [online bipartite matching](/online-bipartite-matching/), [dynamic matching](/dynamic-matching/), the [streaming maximal matching problem](/streaming-maximal-matching-problem/), and parallel algorithms such as the [randomized parallel perfect matching](/rnc-perfect-matching/).
- **With preferences:** pairs must be stable instead of many, as in the [stable roommates problem](/stable-roommates-problem/).

## Examples

| graph | $n$ | $\nu$ | a maximum matching | a Tutte-Berge set $U$ |
|---|---|---|---|---|
| no edges | $n$ | 0 | $\emptyset$ | $\emptyset$, with $n$ odd components of one vertex |
| triangle $abc$ | 3 | 1 | $\{ab\}$ | $\emptyset$: one odd component, $(3 + 0 - 1)/2 = 1$ |
| 5-cycle | 5 | 2 | two edges | $\emptyset$: $(5 + 0 - 1)/2 = 2$ |
| triangle $abc$ with pendant edges $ce$ and $ad$ | 5 | 2 | $\{bc, ad\}$ | $\{a\}$: $G - a$ has the odd components $\{b, c, e\}$ and $\{d\}$, $(5 + 1 - 2)/2 = 2$ |
| star $K_{1,r}$, $r \ge 1$ | $r + 1$ | 1 | one edge | the center: $r$ odd components, $(r + 2 - r)/2 = 1$ |
| Petersen graph | 10 | 5 | a perfect matching (it has 6) | $\emptyset$ |

**Greedy is not enough.** On the path $a - b - c - d$, a greedy scan that takes $bc$ first stops with one edge. The path $a\,b\,c\,d$ is augmenting for $\{bc\}$, and swapping along it gives $\{ab, cd\}$.

**Odd cycles make the search hard.** Take the path $r - s - x_1$, the 5-cycle $x_1 x_2 x_3 x_4 x_5$, and a pendant vertex $t$ joined to $x_4$, with $M = \{s x_1, x_2 x_3, x_4 x_5\}$. The vertices $r$ and $t$ are exposed, and $r\,s\,x_1\,x_5\,x_4\,t$ is an augmenting path, which gives the perfect matching $\{rs, x_1 x_5, x_2 x_3, x_4 t\}$. A search that labels each vertex once, as in the bipartite case, can go $r\,s\,x_1\,x_2\,x_3\,x_4\,x_5$ first. It then reaches $x_4$ by an edge outside $M$ and can only leave it by the matching edge $x_4 x_5$, so it never tries the edge $x_4 t$, and it misses the augmenting path. [Edmonds' algorithm](/edmonds-blossom/) contracts the odd cycle, the [blossom](/blossom/), to fix this.

## Known algorithms

| algorithm | graphs | time | notes |
|---|---|---|---|
| [Edmonds' blossom algorithm](/edmonds-blossom/) | general | $O(n^2 m)$; $O(n^3)$ with Gabow's implementation | augmenting paths with blossom contraction |
| [Micali-Vazirani](/micali-vazirani-algorithm/) | general | $O(m \sqrt n)$ | shortest augmenting paths in phases |
| [Randomized parallel perfect matching](/rnc-perfect-matching/) | general | polylogarithmic depth, polynomial work | the [Tutte matrix](/tutte-matrix/) and the isolation lemma |
| [Kuhn's algorithm](/kuhn-algorithm/) | bipartite only | $O(nm)$ | one search per vertex |
| [Hopcroft-Karp](/hopcroft-karp/) | bipartite only | $O(m \sqrt n)$ | the bipartite case of the phase method |
| greedy [maximal matching](/maximal-matching/) | general | $O(n + m)$ | at least half of $\nu$ |

A randomized algebraic algorithm of Mucha and Sankowski finds a maximum matching of a general graph in $O(n^{\omega})$ time, where $\omega < 2.38$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/). This is faster than $O(m \sqrt n)$ for dense graphs.

## Bounds

- **Upper bound.** $O(m \sqrt n)$ time in the worst case on the [word RAM](/word-ram/), deterministic, by Micali and Vazirani; $O(n^{\omega})$ with high probability by Mucha and Sankowski.
- **Lower bound.** $\Omega(n + m)$ in the worst case, the size of the input. No better general lower bound is known for the word RAM.
- **Approximation in phases.** If the shortest augmenting path of $M$ has at least $2k + 1$ edges, then $|M| \ge \frac{k}{k+1}\nu(G)$. Proof: let $M^*$ be a maximum matching. The symmetric difference $M \oplus M^*$ is a union of paths and even cycles whose edges alternate, and at least $|M^*| - |M|$ of its components are $M$-augmenting paths, vertex-disjoint. Each has at least $2k + 1$ edges, so at least $k$ edges of $M$, and these edges are distinct. So $k(|M^*| - |M|) \le |M|$, which gives the bound. So $k$ phases of shortest augmenting paths, as in Hopcroft-Karp or Micali-Vazirani, give a $(1 - \frac{1}{k+1})$-approximation in $O(km)$ time.

## Reductions

- **To and from perfect matching.** For $0 \le k \le n/2$, add $n - 2k$ new vertices, each joined to every old vertex and to no new vertex. Then $\nu(G) \ge k$ if and only if the new graph has a perfect matching: a matching of size $k$ leaves $n - 2k$ old vertices exposed, which take the new vertices; and in a perfect matching the new vertices take $n - 2k$ old vertices, so the other $2k$ old vertices are matched among themselves. This is the step that derives the Tutte-Berge formula from [Tutte's theorem](/tutte-theorem/).
- **Bipartite case to max flow.** A bipartite instance is a unit-capacity [max-flow problem](/max-flow-problem/) on the network $s \to L \to R \to t$.
- **Algebraic.** $\nu(G)$ equals half the rank of the [Tutte matrix](/tutte-matrix/) of $G$, a theorem of Lovász. With random values for the variables, the rank of a numeric matrix gives $\nu(G)$ with high probability, by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/).
- **Edge cover.** For a graph without isolated vertices, a [minimum edge cover](/minimum-edge-cover/) has $n - \nu(G)$ edges, and one is built from a maximum matching in linear time.
- **Vertex cover.** The ends of a maximum matching, or of any maximal matching, give a [2-approximation for vertex cover](/vertex-cover-2-approximation/).

## Applications

- **Pairing.** Forming the most pairs from a compatibility graph: partners in a class, players in a round, crews of two, or pairwise exchanges in kidney donation.
- **Scheduling on two machines.** Unit-time jobs with a "may run together" graph: a maximum matching gives the most pairs that run in parallel, so the shortest schedule.
- **Edge covers and independent sets.** The size of a minimum edge cover follows from $\nu$, and in bipartite graphs so does the size of a maximum independent set.
- **Subroutine.** Algorithms for [minimum-weight perfect matching](/minimum-weight-perfect-matching/), for the [Chinese postman problem](/chinese-postman-problem/), and for [Christofides' algorithm](/christofides-algorithm/) build on the same augmenting path and blossom machinery.

## References
