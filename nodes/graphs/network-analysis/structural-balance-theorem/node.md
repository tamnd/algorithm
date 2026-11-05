---
tag: RGF93E
kind: theorem
slug: structural-balance-theorem
name: Structural balance theorem
aliases:
- Heider balance theorem
- Cartwright-Harary theorem
area: graphs/network-analysis
level: core
summary: A signed graph is balanced exactly when its nodes split into two opposing groups.
prereqs: [graph, bipartite-graph, bipartite-odd-cycle-theorem]
see_also: [bipartite-odd-cycle-theorem, bipartite-testing, triadic-closure, correlation-clustering, union-find-connectivity, breadth-first-search, structural-equivalence, weak-ties]
sources:
  - paper: doi:10.1307/mmj/1028989917
    title: Frank Harary, On the notion of balance of a signed graph, Michigan Mathematical Journal 2(2), 143 to 146 (1953)
    locator: the definition of balance by cycles and the theorem that a signed graph is balanced if and only if its vertices split into two sets with every negative edge between them
  - paper: doi:10.1037/h0046049
    title: Dorwin Cartwright and Frank Harary, Structural balance, a generalization of Heider's theory, Psychological Review 63(5), 277 to 293 (1956)
    locator: the translation of Heider's balance into signed graphs and the structure theorem
  - paper: doi:10.1080/00223980.1946.9917275
    title: Fritz Heider, Attitudes and cognitive organization, Journal of Psychology 21(1), 107 to 112 (1946)
    locator: the whole paper (balanced and unbalanced triads of sentiments)
  - paper: doi:10.1177/001872676702000206
    title: James A. Davis, Clustering and structural balance in graphs, Human Relations 20(2), 181 to 187 (1967)
    locator: the weaker condition (no cycle with exactly one negative edge) and its characterization by splits into any number of groups
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 5, Positive and negative relationships (Sections 5.1 to 5.3, the balance theorem for complete graphs and its proof, and the extension to arbitrary graphs)
---

The structural balance theorem says that a signed graph, in which each edge is marked positive (friends) or negative (enemies), is *balanced*, meaning that every cycle has an even number of negative edges, exactly when its vertices can be split into two groups with all positive edges inside the groups and all negative edges between them. Heider (1946) proposed balance as a principle of attitudes; Harary (1953) proved the theorem, and Cartwright and Harary (1956) brought it to social networks. It is the signed form of the [odd cycle theorem](/bipartite-odd-cycle-theorem/) for [bipartite graphs](/bipartite-graph/), and it gives a linear-time test for balance.

## Statement

A *signed graph* is an undirected [graph](/graph/) $G = (V, E)$ with a sign $\sigma(e) \in \{+1, -1\}$ on each edge. It has no weights other than the signs: the magnitude of a tie is ignored, and a pair with no relation has no edge. The *sign of a cycle* is the product of the signs of its edges, so a cycle is positive exactly when it has an even number of negative edges. $G$ is *balanced* when every cycle is positive.

**Theorem (Harary).** A signed graph $G$ is balanced if and only if $V$ can be split into two disjoint sets $V_1$ and $V_2$, one of which may be empty, such that every positive edge has both ends in the same set and every negative edge has one end in each set.

**Corollary (complete graphs).** If $G$ is complete, then $G$ is balanced if and only if every triangle has an even number of negative edges (that is, three positive edges or exactly one).

When $G$ is not connected, the condition is separate for each connected component, and the split is made in each component and then combined. In a connected balanced graph the split is unique up to swapping $V_1$ and $V_2$; a balanced graph with $c$ components has $2^{c-1}$ splits.

**Example.** Take the vertices $a, \ldots, e$ with positive edges $ab$, $ac$, $bc$, $de$ and negative edges $ad$, $be$, $ce$. The split $\{a, b, c\}$ against $\{d, e\}$ puts every positive edge inside and every negative edge across, so the graph is balanced; the cycle $a, d, e, b, a$ has the two negative edges $ad$ and $be$. The graph is connected, so this is the only split. If $de$ is made negative, the same cycle has three negative edges, no split exists, and removing the single edge $de$ restores balance, so the frustration index is 1.

## In plain words

Think of a group of people where each pair is either friends, enemies, or has no relation. Some patterns feel stable: "the friend of my friend is my friend" and "the enemy of my enemy is my friend". Some feel tense: being friends with two people who hate each other.

The theorem says that if every loop of relations around the group is of the stable kind, then the whole group falls into at most two camps. Everyone inside a camp is on friendly terms, and every hostile relation goes from one camp to the other. And the other way round: if there are two such camps, every loop is stable.

So local stability, checked on loops, forces a global shape: two opposing sides.

## Proof

*Two camps give balance.* Suppose $V_1, V_2$ is such a split. Walk around a cycle $u_1, u_2, \ldots, u_k, u_1$. Each negative edge moves the walk from one set to the other, and each positive edge keeps it in the same set. The walk ends where it started, so it crosses between the sets an even number of times. Hence the cycle has an even number of negative edges.

*Balance gives two camps.* Suppose every cycle is positive. It suffices to split each connected component, since the union of the splits of the components is a split of $G$ (an edge never joins two components). So let $G$ be connected, pick a root $r$ and a spanning tree $T$, for example by [breadth-first search](/breadth-first-search/). For each vertex $v$ let $\pi(v)$ be the product of the signs on the tree path from $r$ to $v$, and set $V_1 = \{v : \pi(v) = +1\}$ and $V_2 = \{v : \pi(v) = -1\}$.

For a tree edge $\{u, v\}$, with $u$ the parent, $\pi(v) = \pi(u)\, \sigma(uv)$, so $\sigma(uv) = \pi(u)\pi(v)$. For an edge $\{u, v\}$ not in $T$, the tree paths from $u$ and from $v$ meet at a last common vertex $w$; the path from $w$ to $u$ in $T$, the edge $\{u, v\}$, and the path from $v$ back to $w$ form a cycle $C$. The sign of $C$ is $\sigma(uv)$ times the product of the signs on the two tree paths from $w$, which is $\sigma(uv)\, \pi(u)\pi(w) \cdot \pi(v)\pi(w) = \sigma(uv)\, \pi(u)\pi(v)$, since $\pi(w)^2 = 1$. By balance, this is $+1$, so again $\sigma(uv) = \pi(u)\pi(v)$.

So every edge has $\sigma(uv) = \pi(u)\pi(v)$: a positive edge joins two vertices with the same $\pi$, which lie in the same set, and a negative edge joins two vertices with different $\pi$, which lie in different sets. This is the required split.

*Uniqueness.* In a connected graph, fixing the set of $r$ fixes the set of every vertex along the tree, because each edge forces "same set" or "other set". So there are exactly two ordered splits, which are the same unordered split.

*The corollary.* In a complete graph, if every cycle is positive, then every triangle is. Conversely, suppose every triangle is positive, fix a vertex $r$, and put $V_1 = \{r\} \cup \{v : \sigma(rv) = +1\}$ and $V_2 = \{v : \sigma(rv) = -1\}$. For two vertices $u, v \ne r$, the triangle $r, u, v$ is positive, so $\sigma(uv) = \sigma(ru)\sigma(rv)$, which is $+1$ when $u$ and $v$ are in the same set and $-1$ otherwise. Edges at $r$ fit by the definition of the sets. So the split exists, and the theorem gives balance. $\blacksquare$

## Consequences

- **A linear-time test.** Balance can be tested in $O(n + m)$ time: run the proof, by assigning $\pi$ along a breadth-first search tree and checking $\sigma(uv) = \pi(u)\pi(v)$ on every edge. A failing edge closes a negative cycle, which is the certificate. Another way is to merge the ends of each positive edge with [union-find](/union-find-connectivity/), reject if a negative edge has both ends in one class, and then [test](/bipartite-testing/) whether the negative edges form a bipartite graph on the classes.
- **Bipartite graphs.** When every edge is negative, balance means that every cycle has even length, and the split is a 2-colouring. So the [odd cycle theorem](/bipartite-odd-cycle-theorem/) is the special case with all signs negative.
- **Frustration.** The least number of edges whose removal (or sign change) makes a signed graph balanced is its *frustration index*. Computing it is NP-hard, since for an all-negative graph it equals $m$ minus the size of a maximum cut. It is a special case of [correlation clustering](/correlation-clustering/) with two clusters.
- **Social dynamics.** Balance theory predicts that unbalanced triangles are unstable and that networks of alliances drift toward two blocs. Easley and Kleinberg use it to read the shift of European alliances before the First World War into two camps.

## Tightness

- **Triangles are not enough in general graphs.** The 4-cycle with signs $+, +, +, -$ has no triangle, so every triangle condition holds vacuously, but the cycle itself has one negative edge, and no split exists: following the three positive edges puts all four vertices in one set, and then the negative edge lies inside a set. The corollary needs completeness, or at least a chordal graph, where every cycle is a product of triangles.
- **Two groups, not more.** With three mutually hostile groups, the triangle with one vertex in each group has three negative edges and is negative. Davis (1967) weakened balance to *clusterability*: a signed graph splits into any number of groups, with positive edges inside and negative edges between, if and only if no cycle has exactly one negative edge. For complete graphs, it suffices that no triangle has exactly one negative edge.
- **The split cannot be required to be into two non-empty sets.** A graph with only positive edges is balanced with $V_2 = \emptyset$, and no split with both sets non-empty puts all edges inside.

## History

Heider (1946) studied triads of a person, another person and an object, and called a triad balanced when the product of the three sentiments is positive. Harary (1953) defined signed graphs and balance by cycles and proved the theorem. Cartwright and Harary (1956) applied it to groups of people, and Davis (1967) introduced clusterability. Later work studied how unbalanced networks evolve, and Leskovec, Huttenlocher and Kleinberg (2010) tested balance on online networks with positive and negative links, finding partial support.

## References
