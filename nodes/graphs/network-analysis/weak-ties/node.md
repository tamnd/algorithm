---
tag: 3YS6Y4
kind: concept
slug: weak-ties
name: Weak ties
aliases:
- strength of weak ties
area: graphs/network-analysis
level: intro
summary: Sparse links between dense groups that carry novel information.
prereqs: [triadic-closure, bridge, neighborhood]
see_also: [structural-holes, triadic-closure, clustering-coefficient, betweenness-centrality, six-degrees-of-separation, community-detection, girvan-newman-algorithm, percolation]
sources:
  - paper: doi:10.1086/225469
    title: Mark S. Granovetter, The strength of weak ties, American Journal of Sociology 78(6), 1360 to 1380 (1973)
    locator: the whole paper (the forbidden triad, the claim that bridges are weak ties, and the study of how people found jobs)
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 3, Strong and weak ties (local bridges, the strong triadic closure property and the claim that local bridges are weak, and neighbourhood overlap)
  - paper: doi:10.1073/pnas.0610245104
    title: J.-P. Onnela, J. Saramäki, J. Hyvönen, G. Szabó, D. Lazer, K. Kaski, J. Kertész and A.-L. Barabási, Structure and tie strengths in mobile communication networks, PNAS 104(18), 7332 to 7336 (2007)
    locator: the whole paper (the overlap of an edge, its growth with the call volume, and the removal of weak and of strong ties)
---

The strength of weak ties is the thesis, due to Granovetter (1973), that the links that join different groups of a social network are mostly weak ties, and that these links therefore carry most of the new information that reaches a person. A strong tie (a close friend) usually sits inside a dense group, where the information is already shared. A weak tie (an acquaintance) is more often a [local bridge](/bridge/) to another group. In graph terms, edges with a small neighbourhood overlap tend to have low weight, and removing them breaks the network apart faster than removing the strong edges.

## In plain words

Your close friends know each other, and they know what you know. An acquaintance you see once a year moves in other circles. So when you look for a new job, news about an opening is more likely to come from the acquaintance than from a close friend.

The point is about the shape of the network. Close friendships come in tight clusters, where almost everyone knows everyone. The few links that run between clusters are mostly loose acquaintances. Those few links hold the network together and let news travel from one cluster to the next.

Granovetter found this in a study of people who had changed jobs: many had heard of the new job through someone they saw only occasionally.

## The idea

**Ties with a strength.** Let $G = (V, E)$ be a simple undirected graph whose edges carry a strength: either a label *strong* or *weak*, or a weight $w_{uv} > 0$ such as the number of calls between $u$ and $v$. The graph need not be connected. Write $N(v)$ for the [neighborhood](/neighborhood/) of $v$.

**Local bridges.** An edge $\{u, v\}$ is a *local bridge* when $u$ and $v$ have no common neighbour, $N(u) \cap N(v) = \emptyset$. Its *span* is the distance between $u$ and $v$ after the edge is removed; it is at least 3, and it is $\infty$ when the edge is a [bridge](/bridge/) in the usual sense. Each bridge is a local bridge, because a common neighbour would put the edge on a triangle, but a local bridge need not be a bridge.

**The claim and its proof.** Use the strong triadic closure property of [triadic closure](/triadic-closure/): if $v$ has strong ties to $u$ and to $w$, then $u$ and $w$ are adjacent (by a strong or a weak tie).

*Claim (Easley and Kleinberg, Chapter 3).* If a vertex $a$ satisfies the strong triadic closure property and has at least two strong ties, then each local bridge at $a$ is a weak tie.

*Proof.* Let $\{a, b\}$ be a local bridge, and assume that it is strong. Since $a$ has at least two strong ties, it has a strong tie to some $c \ne b$. By the strong triadic closure property at $a$, the vertices $b$ and $c$ are adjacent. Then $c \in N(a) \cap N(b)$, so $\{a, b\}$ is not a local bridge. This contradicts the assumption, so $\{a, b\}$ is weak. $\blacksquare$

The claim turns a local rule (no forbidden triads) into a global statement (the bridges between groups are weak).

**Neighbourhood overlap.** Real data have weights, not labels. Onnela and coauthors measure how close an edge is to a local bridge by its *overlap*

$$O_{uv} = \frac{|N(u) \cap N(v)|}{|N(u) \cup N(v)| - 2},$$

where the $-2$ removes $u$ and $v$ themselves. So $O_{uv} = 0$ exactly for a local bridge, and $O_{uv} = 1$ when $u$ and $v$ have the same other neighbours. It is undefined when $u$ and $v$ have no other neighbours; then the edge is an isolated edge, and it is usually left out. The weak-ties thesis predicts that $O_{uv}$ grows with $w_{uv}$.

**Directed graphs.** The definitions are for undirected graphs. For directed data such as calls, the usual step is to keep an edge when the two people called each other, with the total volume as its weight.

## Examples

**Overlap on a small graph.** Take the 4-clique on the vertices 0, 1, 2, 3, the triangle on 4, 5, 6, and the two edges $\{3, 4\}$ and $\{1, 5\}$ between them.

| edge | common neighbours | $|N(u) \cup N(v)| - 2$ | overlap | distance without the edge |
|---|---|---|---|---|
| $\{0, 2\}$ | 1, 3 | 2 | 1 | 2 |
| $\{1, 3\}$ | 0, 2 | 4 | 0.5 | 2 |
| $\{4, 6\}$ | 5 | 2 | 0.5 | 2 |
| $\{4, 5\}$ | 6 | 3 | 1/3 | 2 |
| $\{3, 4\}$ | none | 5 | 0 | 3 |
| $\{1, 5\}$ | none | 5 | 0 | 3 |

The two edges between the groups are the only local bridges. Each has span 3, so neither is a bridge: removing one leaves a path through the other. If the edges inside the groups are strong and the vertices 1, 3, 4 and 5 satisfy strong triadic closure, the claim forces $\{3, 4\}$ and $\{1, 5\}$ to be weak. Removing the two edges of overlap 0 splits the graph into two components, while removing any two edges inside the 4-clique leaves it connected.

**Job search.** Granovetter interviewed people in a Boston suburb who had recently changed jobs. Of those who found the job through a personal contact, more reported that they saw the contact "occasionally" or "rarely" than "often".

**Mobile phone data.** Onnela and coauthors studied the call graph of millions of mobile phone users, with the call time as the weight. The overlap of an edge rose with its weight, as the thesis predicts. When they removed the edges in order of increasing weight, the giant component broke up at a smaller fraction of removed edges than when they removed them in order of decreasing weight. So the weak ties hold the network together, in the sense of [percolation](/percolation/).

## Where it is used

- [Structural holes](/structural-holes/): Burt's theory of the advantage of a person whose ties bridge groups.
- [Community detection](/community-detection/) and the [Girvan-Newman algorithm](/girvan-newman-algorithm/): the edges between communities are the ones with low overlap and high [betweenness](/betweenness-centrality/).
- [Six degrees of separation](/six-degrees-of-separation/): the bridges between groups keep social distances short.
- [Percolation](/percolation/) and the robustness of networks: the order in which edges fail decides when the network falls apart.
- [Triadic closure](/triadic-closure/): the local rule from which the claim follows.

## References
