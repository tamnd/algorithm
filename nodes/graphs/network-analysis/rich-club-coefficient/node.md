---
tag: 135Q0W
kind: definition
slug: rich-club-coefficient
name: Rich-club coefficient
aliases:
- rich club
area: graphs/network-analysis
level: advanced
summary: Density of edges among the highest-degree nodes compared with a null model.
prereqs: [degree, degree-distribution, configuration-model]
see_also: [assortativity, core-periphery-structure, degree-distribution, scale-free-network, configuration-model, k-core-decomposition, clustering-coefficient, network-motif]
sources:
  - paper: doi:10.1109/LCOMM.2004.823426
    title: Shi Zhou and Raúl J. Mondragón, The rich-club phenomenon in the Internet topology, IEEE Communications Letters 8(3), 180 to 182 (2004)
    locator: the rich-club coefficient as the density of links among the nodes of highest degree, measured on the autonomous systems graph of the Internet
  - paper: doi:10.1038/nphys209
    title: Vittoria Colizza, Alessandro Flammini, M. Ángeles Serrano and Alessandro Vespignani, Detecting rich-club ordering in complex networks, Nature Physics 2, 110 to 115 (2006)
    locator: the coefficient phi(k) over the nodes of degree greater than k, the observation that it increases with k even in random networks, and the normalized ratio against degree-preserving randomized networks
  - paper: doi:10.1103/PhysRevLett.101.168702
    title: Tore Opsahl, Vittoria Colizza, Pietro Panzarasa and José J. Ramasco, Prominence and control, the weighted rich-club effect, Physical Review Letters 101(16), 168702 (2008)
    locator: the weighted rich-club coefficient, comparing the weight on the links among the richest nodes with the largest weights in the network
---

The rich-club coefficient $\phi(k)$ of a network is the density of edges among the vertices of [degree](/degree/) greater than $k$: the fraction of the possible links between these "rich" vertices that are present. A network has *rich-club ordering* when the hubs are more densely tied to each other than they would be by chance, which is tested by dividing $\phi(k)$ by its value in random networks with the same degrees. Zhou and Mondragón (2004) introduced the coefficient for the Internet, and Colizza, Flammini, Serrano and Vespignani (2006) showed that the comparison with a null model is essential, because $\phi(k)$ rises with $k$ even in random networks.

## Definition

Let $G = (V, E)$ be an undirected simple graph without weights. For an integer $k \ge 0$, let $R_{>k} = \{v : d(v) > k\}$ be the vertices of degree greater than $k$, with $N_{>k} = |R_{>k}|$, and let $E_{>k}$ be the number of edges with both ends in $R_{>k}$. The *rich-club coefficient* is

$$\phi(k) = \frac{2 E_{>k}}{N_{>k}(N_{>k} - 1)},$$

the density of the subgraph induced on $R_{>k}$. It is defined when $N_{>k} \ge 2$; for larger $k$ it is undefined, not 0. The threshold is strict, so all vertices of the same degree are in or out together and there are no ties to break. The graph need not be connected: the definition counts edges, not paths.

**The normalized coefficient.** Let $\phi_{\mathrm{ran}}(k)$ be the mean of $\phi(k)$ over random graphs with the same degree sequence, sampled by degree-preserving edge swaps or from the [configuration model](/configuration-model/). Then

$$\rho(k) = \frac{\phi(k)}{\phi_{\mathrm{ran}}(k)},$$

and $G$ has rich-club ordering at degree $k$ when $\rho(k) > 1$ by a significant margin. A value $\rho(k) < 1$ means that the hubs avoid each other.

**Why the normalization is needed.** In a random graph with given degrees, two vertices of degrees $d_u$ and $d_v$ are joined with probability about $d_u d_v / 2m$ when this is small. Vertices of high degree are therefore joined to each other more often, and $\phi_{\mathrm{ran}}(k)$ increases with $k$ for any degree sequence. A rising $\phi(k)$ alone says only that the degrees are uneven.

**Directed and weighted versions.** For a directed graph, $R_{>k}$ is defined by the out-degree, the in-degree, or the total degree (the choice must be stated), and the density divides the arcs by $N_{>k}(N_{>k} - 1)$. For a weighted graph, Opsahl and coauthors rank the vertices by a richness measure such as the strength, take the $E_{>r}$ links among the richest vertices, and divide the weight on these links by the sum of the $E_{>r}$ largest weights in the whole network, again normalized by a null model that reshuffles the weights.

## Examples and non-examples

**Hubs that form a clique.** Take four hubs $0, 1, 2, 3$ joined to each other, give each hub three leaves of its own, and join two pairs of leaves of different hubs. The graph has 16 vertices and 20 edges; the hubs have degree 6, four leaves have degree 2, and eight have degree 1.

| $k$ | $N_{>k}$ | $E_{>k}$ | $\phi(k)$ | $\phi_{\mathrm{ran}}(k)$ | $\rho(k)$ |
|---|---|---|---|---|---|
| 0 | 16 | 20 | 1/6 | 0.167 | 1.00 |
| 1 | 8 | 12 | 3/7 | 0.438 | 0.98 |
| 2 to 5 | 4 | 6 | 1 | 0.881 | 1.13 |

The values of $\phi_{\mathrm{ran}}$ are means over 2000 graphs made by degree-preserving edge swaps. The hubs form a complete graph, so $\phi = 1$ from $k = 2$ on, which looks like a perfect rich club. But the random graphs with the same degrees already have $\phi_{\mathrm{ran}} \approx 0.88$: four vertices of degree 6 in a graph with only 20 edges can hardly avoid each other. The ratio $\rho \approx 1.13$ shows only a mild rich club. At $k = 0$ every graph with the degree sequence has the same $\phi$, so $\rho(0) = 1$ always.

**Hubs that avoid each other.** Four hubs, each with six leaves of its own and no other edges, give $\phi(1) = 0$: the only vertices of degree greater than 1 are the hubs, and no two are joined. The random graphs with the same degrees have $\phi_{\mathrm{ran}}(1) \approx 0.69$, so $\rho(1) = 0$, the opposite of a rich club.

**Real networks.** Colizza and coauthors found $\rho(k) > 1$ for large $k$ in a scientific collaboration network and in the network of air routes, where the large airports are densely joined, and $\rho(k) < 1$ in protein interaction networks and in the Internet at the level of autonomous systems, whose raw $\phi(k)$ had been read as a rich club.

**Non-examples.**

- The density of the whole graph is $\phi(0)$ when no vertex is isolated, not a rich-club measure: it does not single out the hubs.
- [Assortativity](/assortativity/) measures the correlation of degrees at the two ends of all edges. A network can be disassortative overall and still have a rich club among its few largest hubs, because the rich club is about a small set of vertices.
- The [k-core](/k-core-decomposition/) of a graph is also a set of well-connected vertices, but it is defined by degrees inside the subgraph, not in the whole graph, and it says nothing about a null model.

## Related definitions

- [Core-periphery structure](/core-periphery-structure/): a dense core of tightly linked vertices with a sparse periphery tied to it; a rich club is one form of core.
- [Assortativity](/assortativity/): the degree correlation over all edges.
- [Configuration model](/configuration-model/): the standard null model for $\rho(k)$.
- [Degree distribution](/degree-distribution/) and [scale-free networks](/scale-free-network/): the uneven degrees that make the normalization necessary.
- [k-core decomposition](/k-core-decomposition/): nested subgraphs of minimum degree $k$.
- [Network motif](/network-motif/): the same idea of comparing a count with degree-preserving random graphs, applied to small patterns.

## References
