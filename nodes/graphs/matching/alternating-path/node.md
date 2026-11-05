---
tag: 0MR93H
kind: concept
slug: alternating-path
name: Alternating path
aliases:
- M-alternating path
area: graphs/matching
level: core
summary: A path whose edges alternate between matched and unmatched edges.
prereqs: [graph, simple-path]
see_also: [augmenting-path, berge-lemma, blossom, kuhn-algorithm, hopcroft-karp, dulmage-mendelsohn-decomposition, gallai-edmonds-decomposition, kempe-chain]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (alternating paths, symmetric differences of matchings, and Berge's theorem)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 2.1, Matching in bipartite graphs (alternating and augmenting paths)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 16.1, M-augmenting paths
---

An alternating path, for a [matching](/maximum-matching/) $M$ of a [graph](/graph/), is a [simple path](/simple-path/) whose edges are in $M$ and not in $M$ by turns. Alternating paths are the moves of matching theory: exchanging the matched and unmatched edges along one gives a new matching, and the size goes up by one exactly when the path is an [augmenting path](/augmenting-path/). The definition is the same for bipartite and general graphs; in a [bipartite graph](/bipartite-graph/) the search for alternating paths is a plain graph search, while in a general graph odd cycles, called [blossoms](/blossom/), make it harder. Weights play no role in the definition.

## In plain words

Some pairs of people are already teamed up, and each person is in at most one team. Walk from person to person along the "could work together" links, and use a team link and a non-team link by turns. That walk is an alternating path.

Such a path tells you how to rearrange the teams. Break each team link on the path and form a team on each non-team link instead. Everyone in the middle of the path still has exactly one partner. Only the two people at the ends can change: one may lose a partner and one may gain one. If both ends had no partner at the start, the rearrangement makes one more team.

## The idea

Let $G = (V, E)$ be a finite undirected graph and $M \subseteq E$ a matching: no two edges of $M$ share an end. A vertex is *matched* (or *covered*) if an edge of $M$ has it as an end, and *free* (or *exposed*) otherwise. Edges in $M$ are *matched edges*.

**Definition.** A path $P = v_0 v_1 \cdots v_k$ with distinct vertices is **$M$-alternating** if, for each $1 \le i < k$, exactly one of the edges $v_{i-1}v_i$ and $v_i v_{i+1}$ is in $M$. A cycle is $M$-alternating in the same way, with the indices taken around the cycle. A path with zero or one edge is alternating.

Three facts carry all the uses of the idea.

**1. Two matchings differ by alternating paths and cycles.** Let $M$ and $N$ be matchings, and let $H$ be the graph $(V, M \triangle N)$, where $M \triangle N = (M \setminus N) \cup (N \setminus M)$. *Claim:* each component of $H$ is a path or a cycle, its edges alternate between $M \setminus N$ and $N \setminus M$, and each cycle has even length. *Proof.* A vertex has at most one edge of $M$ and at most one edge of $N$, so its degree in $H$ is at most 2. A finite graph with maximum degree 2 has paths and cycles as components. Two edges of $H$ at a common vertex cannot both be in $M$, or both in $N$, so along each component the edges alternate. A cycle that alternates between two classes has as many edges of one class as of the other, so its length is even. $\square$

**2. Flipping a path.** Let $P$ be an $M$-alternating path and $M' = M \triangle E(P)$. *Claim:* $M'$ is a matching if and only if each end $v$ of $P$ is free or its edge on $P$ is in $M$. *Proof.* An inner vertex $v$ of $P$ has two edges on $P$, one in $M$; as $v$ has at most one edge of $M$, that is its only one. After the flip, $v$ has exactly one edge of $M'$: the other edge of $P$. Let $v$ be an end, with edge $e$ on $P$. If $e \in M$, then $e$ is the only edge of $M$ at $v$, and $v$ has no edge of $M'$. If $e \notin M$, then $e \in M'$, and each edge of $M$ at $v$ is not on $P$ (a path has one edge at an end), so it stays in $M'$. Then $v$ has one edge of $M'$ if $v$ is free in $M$, and two if not. $\square$

The size changes by the number of unmatched edges of $P$ minus the number of matched edges, which is $+1$, $0$ or $-1$. When both ends are free, the path has odd length, starts and ends with an unmatched edge, and $|M'| = |M| + 1$. This is an [augmenting path](/augmenting-path/). When one end is free and the path has even length, $|M'| = |M|$, and the free vertex moves from one end of the path to the other. Flipping an even alternating cycle also gives a matching of the same size.

**3. Parity in bipartite graphs.** Let $G$ be bipartite with sides $X$ and $Y$, and let $P = v_0 v_1 \cdots v_k$ be any path with $v_0 \in X$. The edges join $X$ to $Y$, so $v_i \in X$ if and only if $i$ is even. If $v_0$ is free and $P$ is alternating, then $v_0 v_1 \notin M$, so the edge into $v_i$ is unmatched for $i$ odd and matched for $i$ even. Thus each vertex has one fixed parity for all alternating paths from free vertices of $X$, given by its side. A search may mark a vertex once and never revisit it. In a general graph this fails: one vertex can be the end of an even and of an odd alternating path from the same free vertex, as the second example shows. Odd cycles are the cause, because a graph is bipartite if and only if it has no odd cycle.

**Alternating trees.** A search from a free vertex $r$ that follows unmatched edges out of even vertices and matched edges out of odd vertices grows an *alternating tree*: every path from $r$ in the tree is $M$-alternating. In a bipartite graph, such a tree reaches exactly the vertices that are ends of $M$-alternating paths from $r$. In a general graph it may not, and [Edmonds' blossom algorithm](/edmonds-blossom/) repairs the search by contracting odd cycles.

## Examples

**A bipartite graph.** Take $X = \{x_1, x_2, x_3\}$, $Y = \{y_1, y_2, y_3\}$ and the edges $x_1y_1$, $x_1y_2$, $x_2y_1$, $x_2y_3$, $x_3y_2$, with $M = \{x_1y_1, x_3y_2\}$. The free vertices are $x_2$ and $y_3$. The paths from $x_2$ are:

| path | alternating? | ends | flip gives |
|---|---|---|---|
| $x_2 y_1 x_1 y_2 x_3$ | yes, unmatched, matched, unmatched, matched | free, matched by its path edge | $\{x_2y_1, x_1y_2\}$, size 2, free vertex moves to $x_3$ |
| $x_2 y_3$ | yes | both free | $\{x_1y_1, x_3y_2, x_2y_3\}$, size 3 |
| $x_2 y_1 x_1$ | yes, even length | free, matched | $\{x_2y_1, x_3y_2\}$, size 2, free vertex moves to $x_1$ |

Every vertex reached from $x_2$ by an alternating path has the parity of its side: $y_1$, $y_2$ and $y_3$ at odd positions, $x_1$ and $x_3$ at even ones.

**An odd cycle breaks the parity.** Take the vertices $r, a, b, c, d, x$, the edges $ra$, $ab$, $bc$, $cd$, $dr$, $cx$, and $M = \{ab, cd\}$. The free vertices are $r$ and $x$. The vertex $c$ is the end of the alternating path $r\,a\,b\,c$ of odd length, which reaches $c$ by an unmatched edge, and of $r\,d\,c$ of even length, which reaches $c$ by the matched edge $dc$. Only the second can go on along the unmatched edge $cx$: the path $r\,d\,c\,x$ is augmenting, and flipping it gives the perfect matching $\{ab, rd, cx\}$ of size 3. A search that first reaches $c$ by $r\,a\,b\,c$, marks it as odd and never comes back, follows only the matched edge $cd$ out of $c$, and then finds no augmenting path. The odd cycle $r\,a\,b\,c\,d$ is a [blossom](/blossom/).

**The difference of two matchings.** In the cycle $C_6 = v_1 v_2 \cdots v_6$, let $M = \{v_1v_2, v_3v_4, v_5v_6\}$ and $N = \{v_2v_3, v_4v_5, v_6v_1\}$. Then $M \triangle N$ is the whole cycle, an alternating cycle of length 6. With $N = \{v_2v_3\}$ instead, $M \triangle N$ is the alternating path $v_1 v_2 v_3 v_4$ plus the edge $v_5v_6$, a path of length 1.

**Not alternating.** In the path $v_1 v_2 v_3 v_4$ with $M = \{v_1v_2, v_3v_4\}$, the walk $v_1 v_2 v_3 v_4$ is alternating, but with $M = \{v_1v_2\}$ the walk $v_1v_2v_3v_4$ is not: the edges $v_2v_3$ and $v_3v_4$ are both unmatched.

## Where it is used

- **Augmenting paths and Berge's lemma.** An alternating path between two free vertices is an [augmenting path](/augmenting-path/), and by [Berge's lemma](/berge-lemma/) a matching is maximum exactly when none exists. The proof uses fact 1.
- **Bipartite matching algorithms.** [Kuhn's algorithm](/kuhn-algorithm/) grows one alternating tree at a time, and [Hopcroft-Karp](/hopcroft-karp/) builds alternating layers by [breadth-first search](/breadth-first-search/). Both rely on the parity of fact 3.
- **Weighted matching.** The [Hungarian algorithm](/hungarian-algorithm/) grows alternating trees in the subgraph of tight edges. In weighted problems, alternating cycles with positive gain show that a perfect matching is not optimal.
- **General graphs.** [Edmonds' blossom algorithm](/edmonds-blossom/) and the [Micali-Vazirani algorithm](/micali-vazirani-algorithm/) search for alternating paths in the presence of odd cycles.
- **Structure theorems.** The [Dulmage-Mendelsohn decomposition](/dulmage-mendelsohn-decomposition/) and the [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/) sort vertices by the even alternating paths from free vertices, using the "free vertex moves" flip of fact 2.
- **Flows.** In the flow model of [bipartite matching](/bipartite-matching/), an alternating path is a path in the [residual graph](/residual-graph/): unmatched edges are forward arcs and matched edges are backward arcs.
- **Edge colouring.** In a proper edge colouring, each colour class is a matching. A [Kempe chain](/kempe-chain/) of two colours is then a path or cycle that alternates between two matchings. Swapping its colours is the flip of fact 2.

## References
