---
tag: PVZ278
kind: concept
slug: triadic-closure
name: Triadic closure
aliases:
- triangle closure principle
area: graphs/network-analysis
level: intro
summary: Tendency for two neighbours of a node to become connected.
prereqs: [graph, neighborhood, degree]
see_also: [clustering-coefficient, weak-ties, structural-holes, common-neighbors, link-prediction, triangle-counting, small-world-network, homophily]
sources:
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 3, Strong and weak ties (triadic closure, the clustering coefficient, and the strong triadic closure property)
  - paper: doi:10.1126/science.1116869
    title: Gueorgi Kossinets and Duncan J. Watts, Empirical analysis of an evolving social network, Science 311(5757), 88 to 90 (2006)
    locator: the whole paper (the probability of a new tie as a function of the number of shared acquaintances, in e-mail data of a university)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on transitivity)
  - paper: doi:10.1086/225469
    title: Mark S. Granovetter, The strength of weak ties, American Journal of Sociology 78(6), 1360 to 1380 (1973)
    locator: the argument that two strong ties of one person make a tie between the other two likely (the forbidden triad)
---

Triadic closure is the tendency of a social network to close triangles: if $v$ is linked to both $u$ and $w$, then $u$ and $w$ are more likely than two random people to become linked. It explains why social networks have a high [clustering coefficient](/clustering-coefficient/), and it is the reason that counting [common neighbours](/common-neighbors/) is a good way to predict new links. The concept is a statement about how a network changes over time, and its static trace is the large number of triangles.

## In plain words

Two of your friends are more likely to meet each other than two strangers are. They come to the same parties, they hear about each other from you, and they may trust each other because they both trust you. Over time, many of them become friends too.

So a social network fills up with small groups of three people who all know each other. A pair of people with many friends in common is very likely to be linked already, or to become linked soon. This is why a social site suggests "people you may know" by counting the friends you share.

The rule is a tendency, not a law. Some pairs of your friends never meet.

## The idea

**Open and closed triads.** Let $G = (V, E)$ be an undirected graph without weights. A *connected triple* centred at $v$ is a path $u - v - w$ with $u \ne w$. It is *closed* when $\{u, w\} \in E$, so that $u, v, w$ form a triangle, and *open* otherwise. Triadic closure says that an open triple tends to become closed: in a graph that evolves in time, the probability that the edge $\{u, w\}$ appears in the next time step is higher when $u$ and $w$ have a common neighbour, and it grows with the number of common neighbours $|N(u) \cap N(w)|$.

**The static trace.** A network in which this process has run for some time has many closed triples. The global [clustering coefficient](/clustering-coefficient/) $C_\Delta = 3 \times \text{(triangles)} / \text{(connected triples)}$ is the fraction of closed triples. In the [Erdős-Rényi model](/erdos-renyi-model/) $G(n, p)$, each triple is closed with probability $p$ on its own, so $C_\Delta \approx p$, which goes to 0 for a sparse graph. Social networks have much larger values at a mean degree that makes $p$ tiny, and triadic closure is the usual explanation.

**Strong triadic closure.** Easley and Kleinberg state a sharper version for graphs whose edges are labelled *strong* or *weak*. A vertex $v$ violates the *strong triadic closure property* when it has strong edges to two vertices $u$ and $w$ that are not adjacent at all. A labelling satisfies the property when no vertex violates it. Granovetter (1973) argued that the open triad with two strong ties is rare, and called it the forbidden triad. From this property follows the result that every local bridge is a weak tie; the proof is on the page on [weak ties](/weak-ties/).

**Directed graphs.** In a directed graph, a triple has several orientations, and the closure of $u \to v \to w$ by $u \to w$ is called transitivity. The triad census counts the 16 kinds of directed triads, up to isomorphism. This page treats the undirected case.

**Ties and disconnected graphs.** Counting common neighbours to predict closures often produces ties, for example many pairs with exactly one common neighbour. A prediction method must state its tie rule, such as a second score like the [Adamic-Adar index](/adamic-adar-index/), or a random choice. Triadic closure acts only inside a component: two vertices in different components have no common neighbour, so the process never joins two components. Other mechanisms, such as random meetings or [homophily](/homophily/), are needed for that.

## Examples

**Counting open triads.** Take the vertices 0 to 5 and the 7 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$. The degrees are $2, 3, 3, 3, 2, 1$, so there are $1 + 3 + 3 + 3 + 1 + 0 = 11$ connected triples. The two triangles $\{0,1,2\}$ and $\{1,2,3\}$ close 6 of them, so $C_\Delta = 6/11 \approx 0.545$. The 5 open triples and the common neighbours of their end vertices are:

| missing edge | common neighbours | open triples it would close |
|---|---|---|
| $\{0, 3\}$ | 1, 2 | $0 - 1 - 3$ and $0 - 2 - 3$ |
| $\{1, 4\}$ | 3 | $1 - 3 - 4$ |
| $\{2, 4\}$ | 3 | $2 - 3 - 4$ |
| $\{3, 5\}$ | 4 | $3 - 4 - 5$ |

The pair $\{0, 3\}$ has the most common neighbours, so triadic closure predicts it first. After the edge $\{0, 3\}$ is added, there are 4 triangles and 16 connected triples, and $C_\Delta$ rises to $12/16 = 0.75$. The other three candidates tie with one common neighbour each.

**Evidence from data.** Kossinets and Watts (2006) followed the e-mail traffic of a university community over one academic year. They measured the probability that two people who had not been in contact started to exchange e-mail, as a function of the number of contacts they shared. The probability grew with the number of shared contacts, and it was much higher for pairs with at least one shared contact than for pairs at distance more than 2. This is the time-resolved form of the triangle count above.

**A non-example.** A [bipartite graph](/bipartite-graph/), such as a graph of people and the clubs they join, has no triangles at all, because each cycle has even length. Triadic closure does not apply to it directly. It applies to the one-mode projection, where two people are joined when they share a club, and that projection is full of triangles by construction.

## Where it is used

- [Clustering coefficient](/clustering-coefficient/) and [triangle counting](/triangle-counting/): the measures of how much closure has happened.
- [Link prediction](/link-prediction/), [common neighbors](/common-neighbors/) and the [Adamic-Adar index](/adamic-adar-index/): scores that rank the open triads by how likely they are to close.
- [Weak ties](/weak-ties/) and [structural holes](/structural-holes/): what the open triads that stay open mean for the flow of information.
- [Small-world network](/small-world-network/) and [Watts-Strogatz model](/watts-strogatz-model/): models that keep the high clustering that closure creates.
- [Network motif](/network-motif/): the triangle is the simplest motif, and its excess over a null model is the usual test.

## References
