---
tag: KY6CH2
kind: concept
slug: augmenting-path
name: Augmenting path
aliases:
- M-augmenting path
area: graphs/matching
level: core
summary: An alternating path that starts and ends at unmatched vertices; flipping it enlarges the matching by one.
prereqs: [alternating-path]
see_also: [berge-lemma, augmenting-path-flow, kuhn-algorithm, hopcroft-karp, edmonds-blossom, hungarian-algorithm, maximal-matching, blossom]
sources:
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 16.1, M-augmenting paths, and Section 16.4, An O(n^(1/2) m) algorithm
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (augmenting paths and Berge's theorem)
  - paper: doi:10.1137/0202019
    title: John E. Hopcroft and Richard M. Karp, An n^(5/2) algorithm for maximum matchings in bipartite graphs, SIAM Journal on Computing 2(4), 225 to 231 (1973)
    locator: the lemmas on shortest augmenting paths and vertex-disjoint augmenting paths
---

An augmenting path for a matching $M$ is an [alternating path](/alternating-path/) whose two ends are both free, that is, not covered by $M$. Exchanging the matched and unmatched edges along it gives a matching with one more edge. By [Berge's lemma](/berge-lemma/), a matching is maximum exactly when no augmenting path exists, so every exact algorithm for the maximum cardinality matching problem, in [bipartite](/bipartite-matching/) and in general graphs, is a method to find augmenting paths. This page is about unweighted graphs; the path of the same name in flow networks is the [flow augmenting path](/augmenting-path-flow/).

## In plain words

Some people are paired up, and two people are still alone. Look for a chain that starts at one lonely person, goes to someone they could pair with, then to that person's current partner, then to someone the partner could pair with instead, and so on, until it reaches the other lonely person.

Along such a chain, everybody can switch at the same time: each person pairs with the next person on the chain instead of the old partner. Nobody in the middle loses out, and the two lonely people both get a partner. So the number of pairs grows by one. If no such chain exists anywhere, the pairing is already as large as it can be.

## The idea

Let $G = (V, E)$ be a finite undirected graph, bipartite or not, and $M$ a matching of $G$.

**Definition.** An **$M$-augmenting path** is an $M$-alternating path $P = v_0 v_1 \cdots v_k$ with $k \ge 1$ such that $v_0 \ne v_k$ are both free.

Since $v_0$ is free, the edge $v_0v_1$ is not in $M$, and in the same way $v_{k-1}v_k \notin M$. The edges alternate, so $k$ is odd, $P$ has $(k+1)/2$ unmatched and $(k-1)/2$ matched edges, and all inner vertices $v_1, \ldots, v_{k-1}$ are matched by edges of $P$. A single edge between two free vertices is an augmenting path with $k = 1$.

**Augmentation.** $M' = M \triangle E(P)$ is a matching and $|M'| = |M| + 1$. *Proof.* By the flip rule on the [alternating path](/alternating-path/) page, $M'$ is a matching because both ends are free. The flip removes $(k-1)/2$ edges and adds $(k+1)/2$. $\square$ The vertices covered by $M'$ are those covered by $M$ plus $v_0$ and $v_k$: a matched vertex stays matched after an augmentation.

**Many disjoint augmenting paths.** Let $M^*$ be a maximum matching, $\nu = |M^*|$, and $d = \nu - |M|$. *Claim:* the graph $M \triangle M^*$ contains $d$ vertex-disjoint $M$-augmenting paths. *Proof.* Its components are alternating paths and even cycles. An even cycle, and a path of even length, has as many edges of $M$ as of $M^*$. A path of odd length has one more edge of one matching than of the other. Let $a$ be the number of components with one more edge of $M^*$ and $b$ the number with one more edge of $M$. Then $|M^*| - |M| = a - b$, so $a \ge d$. A component with one more edge of $M^*$ is a path that starts and ends with edges of $M^* \setminus M$. Its ends have no other edge in $M \triangle M^*$; an end $v$ with an edge of $M$ would have that edge in $M \cap M^*$, impossible because $v$ already has an edge of $M^*$. So both ends are free in $M$, and the path is $M$-augmenting. $\square$ With $d \ge 1$ this proves the hard direction of [Berge's lemma](/berge-lemma/).

**A short augmenting path exists.** The $d$ disjoint paths share no edge of $M$, so together they use at most $|M|$ matched edges, and one of them has at most $|M|/d$ matched edges. Its length is at most $2|M|/d + 1$. This bound drives the analysis of [Hopcroft-Karp](/hopcroft-karp/): while $d$ is large, a short augmenting path exists.

**Approximation.** If $M$ has no augmenting path with fewer than $2k + 1$ edges, then $|M| \ge \frac{k}{k+1}\nu$. *Proof.* Each of the $d$ disjoint paths has at least $2k+1$ edges, so at least $k$ matched edges, and the paths share no matched edge. So $|M| \ge kd = k(\nu - |M|)$, and $|M|(k+1) \ge k\nu$. $\square$ For $k = 1$: a [maximal matching](/maximal-matching/), which has no augmenting path of length 1, has at least half the edges of a maximum one.

**How to find one.** In a [bipartite graph](/bipartite-graph/) with sides $X$ and $Y$, orient each unmatched edge from $X$ to $Y$ and each matched edge from $Y$ to $X$. The $M$-augmenting paths are exactly the directed paths from a free vertex of $X$ to a free vertex of $Y$, so one [breadth-first](/breadth-first-search/) or [depth-first search](/depth-first-search/) from all free vertices of $X$ finds one, or proves that none exists, in $O(n + m)$ time, where $n = |V|$ and $m = |E|$. In a general graph this reduction fails, because the alternating paths from a free vertex do not have a fixed parity at each vertex. [Edmonds' blossom algorithm](/edmonds-blossom/) solves the search in polynomial time by shrinking odd cycles called [blossoms](/blossom/).

**Weighted graphs.** With edge weights $w$, the *gain* of an augmenting path $P$ is $w(E(P) \setminus M) - w(E(P) \cap M)$, and an augmentation changes $w(M)$ by the gain. The [Hungarian algorithm](/hungarian-algorithm/) augments along paths of greatest gain, found as shortest paths for reduced costs, which keeps each intermediate matching of maximum weight among the matchings of its size.

## Examples

**A long augmenting path.** Take the bipartite graph with $X = \{1, 2, 3, 4\}$, $Y = \{a, b, c, d\}$ and the edges $1a$, $1b$, $2a$, $3b$, $3c$, $4c$, $4d$. A greedy scan of $1, 2, 3, 4$ that takes the first free neighbour builds $M = \{1a, 3b, 4c\}$ and leaves $2$ and $d$ free. The only augmenting path is

$$2 \to a \Rightarrow 1 \to b \Rightarrow 3 \to c \Rightarrow 4 \to d,$$

where $\to$ is an unmatched edge and $\Rightarrow$ a matched one. It has 7 edges. Augmenting gives $\{2a, 1b, 3c, 4d\}$, a perfect matching of size 4. Here $|M| = 3$ and $d = 1$, so the bound $2|M|/d + 1 = 7$ is met with equality.

**A step of growth.** In the path $P_4 = u_1 u_2 u_3 u_4$ with $M = \{u_2u_3\}$, the whole path is augmenting, and the flip gives $\{u_1u_2, u_3u_4\}$.

**No augmenting path, but a free vertex.** In the 5-cycle $C_5 = v_1 \cdots v_5$ with $M = \{v_1v_2, v_3v_4\}$, the only free vertex is $v_5$. An augmenting path needs two free ends, so there is none, and $M$ is maximum: each matching of $C_5$ has at most $\lfloor 5/2 \rfloor = 2$ edges. A graph with an odd number of vertices never has a perfect matching.

**Odd cycles.** In the graph with edges $ra$, $ab$, $bc$, $cd$, $dr$, $cx$ and $M = \{ab, cd\}$, the augmenting path $r\,d\,c\,x$ goes around the odd cycle $r\,a\,b\,c\,d$ the "short" way. A search that enters $c$ from $b$ first misses it. The [alternating path](/alternating-path/) page traces this case.

**Edge cases.** In a graph with no edges, the empty matching is maximum and there is no augmenting path, even when there are many free vertices. In a graph with a perfect matching $M$, no vertex is free, so no augmenting path exists.

## Where it is used

- [Berge's lemma](/berge-lemma/) characterizes maximum matchings by the absence of augmenting paths.
- [Kuhn's algorithm](/kuhn-algorithm/) finds one augmenting path at a time by depth-first search, for $O(nm)$ time on a bipartite graph.
- [Hopcroft-Karp](/hopcroft-karp/) augments along a maximal set of shortest vertex-disjoint augmenting paths in each phase, for $O(m\sqrt n)$ time.
- [Edmonds' blossom algorithm](/edmonds-blossom/) and the [Micali-Vazirani algorithm](/micali-vazirani-algorithm/) find augmenting paths in general graphs.
- The [Hungarian algorithm](/hungarian-algorithm/) and the [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/) augment along shortest paths for reduced costs in the [assignment problem](/assignment-problem/).
- In the flow model of bipartite matching, an augmenting path is a [flow augmenting path](/augmenting-path-flow/) of the unit-capacity network, and [Ford-Fulkerson](/ford-fulkerson/) on that network is Kuhn's algorithm.
- The approximation bound above gives the simple $\frac12$ guarantee of a [maximal matching](/maximal-matching/) and the $(1 - \varepsilon)$ guarantees of algorithms that only search for short augmenting paths, for example in [dynamic matching](/dynamic-matching/).

## References
