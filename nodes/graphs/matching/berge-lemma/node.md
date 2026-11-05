---
tag: 1H9W02
kind: theorem
slug: berge-lemma
name: Berge's lemma
aliases:
- Berge's theorem
area: graphs/matching
level: core
summary: A matching is maximum iff the graph has no augmenting path.
prereqs: [augmenting-path]
see_also: [alternating-path, maximum-matching, kuhn-algorithm, hopcroft-karp, edmonds-blossom, maximal-matching, tutte-berge-formula, max-flow-min-cut-theorem]
sources:
  - paper: doi:10.1073/pnas.43.9.842
    title: Claude Berge, Two theorems in graph theory, Proceedings of the National Academy of Sciences of the USA 43(9), 842 to 844 (1957)
    locator: the first of the two theorems (a matching is maximum if and only if there is no augmenting chain)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (Berge's theorem and its proof by symmetric differences)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 16.1, M-augmenting paths, and Section 24.4j, Historical notes on nonbipartite matching
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 10, Maximum Matchings (Berge's theorem on augmenting paths)
---

Berge's lemma says that a [matching](/maximum-matching/) $M$ of a graph is maximum if and only if the graph has no [augmenting path](/augmenting-path/) for $M$. It holds in every finite undirected graph, [bipartite](/bipartite-graph/) or general, and it is about the number of edges, not about weights. It turns the global question "is there a larger matching?" into the local question "is there one improving path?", and so it is the correctness argument of every augmenting-path algorithm for maximum matching.

## Statement

Let $G = (V, E)$ be a finite undirected graph and $M \subseteq E$ a matching. An $M$-augmenting path is an [$M$-alternating path](/alternating-path/) with at least one edge whose two ends are distinct vertices not covered by $M$.

**Theorem (Berge, 1957).** $M$ has the largest size among all matchings of $G$ if and only if $G$ contains no $M$-augmenting path.

## In plain words

A pairing of people is as large as possible exactly when you cannot find one chain that starts at a person without a partner, goes along possible pairs and current pairs by turns, and ends at another person without a partner.

One direction is the easy one: such a chain lets everyone on it switch partners, and that makes one more pair. The other direction is the surprise. If some larger pairing exists anywhere, even one that looks completely different, then a single chain of this kind must already exist. So a search can improve the pairing one chain at a time, and when it finds no chain it can stop with full confidence.

## Proof

**If $G$ has an augmenting path, $M$ is not maximum.** Let $P = v_0 v_1 \cdots v_k$ be $M$-augmenting. Both ends are free, so $v_0v_1 \notin M$ and $v_{k-1}v_k \notin M$, and as the edges alternate, $k$ is odd with $(k+1)/2$ edges outside $M$ and $(k-1)/2$ in $M$. Let $M' = M \triangle E(P)$. An inner vertex $v_i$ has exactly one edge of $M$, and it lies on $P$; after the exchange it has exactly one edge of $M'$, the other edge of $P$ at $v_i$. An end $v_0$ is free in $M$, so its only edge of $M'$ is $v_0v_1$, and the same holds for $v_k$. A vertex off $P$ keeps its edges. So $M'$ is a matching, and $|M'| = |M| - \frac{k-1}{2} + \frac{k+1}{2} = |M| + 1$.

**If $M$ is not maximum, $G$ has an augmenting path.** Let $N$ be a matching with $|N| > |M|$, and let $H = (V, M \triangle N)$.

1. Each vertex is an end of at most one edge of $M$ and at most one edge of $N$, so it has degree at most 2 in $H$. Each component of $H$ is therefore a path (possibly a single vertex) or a cycle.
2. Two edges of $H$ at one vertex cannot both lie in $M$ or both in $N$. So the edges of each component alternate between $M \setminus N$ and $N \setminus M$.
3. A cycle with alternating edges has as many edges of $M \setminus N$ as of $N \setminus M$. A path with alternating edges has the same number of each, or one more of one kind.
4. $|N \setminus M| - |M \setminus N| = |N| - |M| > 0$. By step 3 this difference is the sum over the components of (edges of $N \setminus M$) minus (edges of $M \setminus N$), and each cycle adds 0. So some component $Q$ is a path with one more edge of $N \setminus M$ than of $M \setminus N$. Then $Q$ has odd length and its first and last edges are in $N \setminus M$.
5. Let $u$ be an end of $Q$ and $e \in N$ its edge on $Q$. Suppose $u$ is covered by an edge $f \in M$. Then $f \ne e$ since $e \notin M$. If $f \notin N$, then $f \in M \triangle N$ is a second edge of $H$ at $u$, and $u$ is not an end of $Q$. If $f \in N$, then $u$ has two edges $e \ne f$ of $N$, which is impossible. So both ends of $Q$ are free in $M$.
6. $Q$ alternates between edges outside $M$ and edges of $M$ by step 2, and its two distinct ends are free by step 5, so $Q$ is an $M$-augmenting path. $\blacksquare$

## Consequences

- **Augmenting-path algorithms are correct.** Start with any matching, augment while an augmenting path exists, and stop. Each augmentation adds one edge, so there are at most $\lfloor n/2 \rfloor$ of them, and by the lemma the final matching is maximum. [Kuhn's algorithm](/kuhn-algorithm/) and [Hopcroft-Karp](/hopcroft-karp/) for bipartite graphs and [Edmonds' blossom algorithm](/edmonds-blossom/) for general graphs follow this plan. They differ in how they find the path.
- **A certificate of non-maximality.** An augmenting path is a short proof that $M$ is not maximum. The other direction needs a different certificate: a vertex cover of size $|M|$ in a bipartite graph ([Kőnig's theorem](/konig-theorem/)), or a set $U$ with $\frac12(|V| + |U| - \mathrm{odd}(G - U)) = |M|$ in general (the [Tutte-Berge formula](/tutte-berge-formula/)).
- **Disjoint augmenting paths.** The proof gives more: $M \triangle N$ contains at least $|N| - |M|$ vertex-disjoint $M$-augmenting paths. This is the counting lemma behind the $O(m\sqrt n)$ bound of [Hopcroft-Karp](/hopcroft-karp/) and the approximation bounds on the [augmenting path](/augmenting-path/) page.
- **Weighted form for perfect matchings.** Let $w$ be edge weights and $M$ a [perfect matching](/perfect-matching/). Then $M$ has the largest weight among perfect matchings if and only if no $M$-alternating cycle $C$ has positive gain $w(C \setminus M) - w(C \cap M)$. *Proof.* A cycle of positive gain gives the heavier perfect matching $M \triangle C$. Conversely, if $N$ is a heavier perfect matching, no vertex is free in either, so $M \triangle N$ has no path components: every vertex of $H$ has degree 0 or 2. It is a union of alternating cycles, the gains of these cycles add up to $w(N) - w(M) > 0$, and one cycle has positive gain. $\square$
- **Flows.** In the unit-capacity network of [bipartite matching](/bipartite-matching/), the lemma is the matching form of the statement that a flow is maximum when its [residual graph](/residual-graph/) has no path from the source to the sink, which is part of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

## Tightness

- **The ends must both be free.** In the path $u_1u_2u_3$ with $M = \{u_2u_3\}$, the alternating path $u_1u_2u_3$ starts at a free vertex, but its other end is matched. Exchanging along it gives $\{u_1u_2\}$, of the same size. $M$ is maximum, and indeed no augmenting path exists.
- **Maximal is not maximum.** In the path $u_1u_2u_3u_4$, the matching $\{u_2u_3\}$ is maximal: no edge can be added. It is not maximum, and $u_1u_2u_3u_4$ is an augmenting path. So "no augmenting path of length 1" is too weak.
- **Short paths are not enough.** For each $k$, the path with $2k + 2$ vertices $u_1 \cdots u_{2k+2}$ and the matching $\{u_2u_3, u_4u_5, \ldots, u_{2k}u_{2k+1}\}$ of size $k$ has exactly one augmenting path, the whole path, with $2k + 1$ edges. A search limited to shorter paths would wrongly stop.
- **Odd cycles matter for the search, not for the lemma.** In the 5-cycle with one free vertex, the matching of size 2 is maximum, and the lemma confirms it: there is only one free vertex. The lemma holds in general graphs, but finding an augmenting path there needs [blossoms](/blossom/).

## History

Claude Berge published the theorem in 1957, in a two-page note in the Proceedings of the National Academy of Sciences, as the first of "two theorems in graph theory". Alternating paths had been used earlier in bipartite matching; Schrijver's historical notes in Sections 16.7h and 24.4j trace that use. Edmonds based his 1965 polynomial-time algorithm for general graphs on Berge's theorem, by showing how to find augmenting paths in the presence of odd cycles.

## References
