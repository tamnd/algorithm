---
tag: 42DPCA
kind: concept
slug: percolation
name: Percolation
aliases:
- site percolation
- bond percolation
area: graphs/network-analysis
level: advanced
summary: Random removal or retention of nodes or edges and the resulting connectivity transition.
prereqs: [giant-component, configuration-model, erdos-renyi-model, connected-components]
see_also: [giant-component, configuration-model, scale-free-network, sir-epidemic-model, epidemic-threshold, union-find-connectivity, erdos-renyi-model, random-geometric-graph]
sources:
  - paper: doi:10.1017/S0305004100032680
    title: S. R. Broadbent and J. M. Hammersley, Percolation processes I, Crystals and mazes, Mathematical Proceedings of the Cambridge Philosophical Society 53(3), 629 to 641 (1957)
    locator: the whole paper (the definition of percolation on a lattice and the existence of a critical probability)
  - paper: doi:10.1007/BF01197577
    title: Harry Kesten, The critical probability of bond percolation on the square lattice equals 1/2, Communications in Mathematical Physics 74(1), 41 to 59 (1980)
    locator: the whole paper (the proof that the threshold of bond percolation on the square lattice is 1/2)
  - paper: doi:10.1103/PhysRevLett.85.5468
    title: Duncan S. Callaway, M. E. J. Newman, Steven H. Strogatz and Duncan J. Watts, Network robustness and fragility, percolation on random graphs, Physical Review Letters 85(25), 5468 to 5471 (2000)
    locator: the generating function solution of site and bond percolation on random graphs with a given degree distribution, and the removal of the vertices of highest degree
  - paper: doi:10.1103/PhysRevLett.85.4626
    title: Reuven Cohen, Keren Erez, Daniel ben-Avraham and Shlomo Havlin, Resilience of the Internet to random breakdowns, Physical Review Letters 85(21), 4626 to 4628 (2000)
    locator: the threshold for random removal in terms of the first two moments of the degree, and its vanishing for power-law degrees with exponent at most 3
  - paper: doi:10.1103/PhysRevE.64.016706
    title: M. E. J. Newman and R. M. Ziff, Fast Monte Carlo algorithm for site or bond percolation, Physical Review E 64(1), 016706 (2001)
    locator: the algorithm that adds sites or bonds in random order with union-find and obtains the cluster sizes for all occupation probabilities in one pass
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 16, Percolation and network resilience
---

Percolation is the study of what remains connected when each vertex (*site percolation*) or each edge (*bond percolation*) of a graph is kept independently with probability $\phi$ and removed otherwise. On large graphs the answer changes sharply at a *threshold* $\phi_c$: below it, the kept part breaks into small pieces, and above it, a [giant component](/giant-component/) holds a positive fraction of all vertices. Broadbent and Hammersley (1957) introduced it for fluids flowing through porous material; in network science it models random failures, targeted attacks and the spread of epidemics, and it explains why [scale-free networks](/scale-free-network/) survive random failures so well.

## In plain words

Take a network, such as the Internet or a power grid, and break each part at random, say each router fails with some probability. When only a few parts fail, almost everything can still reach almost everything else. When many fail, the network falls apart into small islands that cannot reach each other.

The surprise is that this change is not gradual. As the failure rate grows, the large connected core shrinks slowly, and then, at a particular rate, it vanishes. That tipping point is the threshold. Networks with a few huge hubs keep their core under random failures almost to the end, because random failures rarely hit a hub, but they fall apart quickly when the hubs are attacked on purpose.

## The idea

**Site and bond percolation.** Let $G = (V, E)$ be an undirected graph without weights, and let $0 \le \phi \le 1$. In *site* percolation, each vertex is *occupied* (kept) independently with probability $\phi$, and the result is the subgraph induced by the occupied vertices. In *bond* percolation, each edge is kept independently with probability $\phi$, and all vertices stay. The connected parts of the result are the *clusters*. The questions are the size of the largest cluster, the distribution of cluster sizes, and the value of $\phi$ where they change.

**The threshold.** For a family of graphs with $n \to \infty$, let $S(\phi)$ be the fraction of vertices in the largest cluster. The *percolation threshold* $\phi_c$ is the point where $S$ becomes positive: $S(\phi) \to 0$ for $\phi < \phi_c$ and $S(\phi) > 0$ for $\phi > \phi_c$. On infinite lattices, $\phi_c$ is the point above which an infinite cluster exists with probability 1. Known values include $1/2$ for bond percolation on the square lattice (Kesten 1980), $1/2$ for site percolation on the triangular lattice, about $0.5927$ for site percolation on the square lattice (known only numerically), and $1/(z - 1)$ for both kinds on the infinite tree in which every vertex has degree $z$.

**Random graphs with given degrees.** For the [configuration model](/configuration-model/) with degree distribution $p_k$, generating functions give the exact answer as $n \to \infty$. Let $g_0(z) = \sum_k p_k z^k$ and $g_1(z) = g_0'(z)/g_0'(1)$. For site percolation, $S = \phi\,(1 - g_0(u))$, where $u$ is the smallest root in $[0, 1]$ of $u = 1 - \phi + \phi\, g_1(u)$. Both site and bond percolation have the same threshold

$$\phi_c = \frac{\langle k \rangle}{\langle k^2 \rangle - \langle k \rangle},$$

which is the point where a vertex reached along an edge has, on average, one further occupied neighbour. At $\phi = 1$ this is the Molloy-Reed condition for a giant component, $\langle k^2 \rangle > 2\langle k \rangle$.

**The Erdős-Rényi graph.** With mean degree $c$, $p_k$ is Poisson, $\langle k^2 \rangle = c^2 + c$, and $\phi_c = 1/c$. Here $g_0 = g_1 = e^{c(z - 1)}$, and the equations reduce to $S = \phi\,(1 - e^{-cS})$ for site percolation.

**Hubs and robustness.** For a power law $p_k \propto k^{-\gamma}$ with $2 < \gamma \le 3$, $\langle k^2 \rangle$ diverges as $n \to \infty$, so $\phi_c \to 0$: almost all vertices can be removed at random before the giant component disappears (Cohen and coauthors; Callaway and coauthors). If the vertices of highest degree are removed first, the threshold is far higher, and removing a few percent of the hubs is enough to break the network.

**Directed graphs and disconnected graphs.** For a directed graph, percolation asks for a giant strongly connected component, and for the giant in- and out-components, with thresholds that depend on the joint in- and out-degree distribution. The graph need not be connected at the start: the clusters are measured after the removal, and the giant component of the original graph is the case $\phi = 1$.

**Computing it.** The Newman-Ziff algorithm adds the vertices (or edges) in a random order and merges clusters with [union-find](/union-find-connectivity/), recording the largest cluster after each addition. One pass gives $S$ at every value of $\phi$ for one random order, in time close to $O(n + m)$.

## Examples

**Site percolation on an Erdős-Rényi graph.** With mean degree $c = 4$, the threshold is $\phi_c = 1/4$. The table compares the solution of $S = \phi(1 - e^{-4S})$ with the mean fraction in the largest cluster over 5 graphs with $n = 200000$, computed with the Newman-Ziff method.

| $\phi$ | 0.2 | 0.25 | 0.3 | 0.4 | 0.5 | 0.75 | 1 |
|---|---|---|---|---|---|---|---|
| theory | 0 | 0 | 0.094 | 0.257 | 0.398 | 0.705 | 0.980 |
| simulation | 0.0006 | 0.0073 | 0.097 | 0.257 | 0.399 | 0.706 | 0.980 |

At $\phi = 1$, 2 percent of the vertices are outside the giant component, the vertices with no edge and the small trees. Near $\phi_c$ the finite graph shows a smooth step instead of a sharp corner: the largest cluster at the threshold grows like $n^{2/3}$, a vanishing fraction.

**A power law with a cutoff.** Take $p_k \propto k^{-2.5}$ for $1 \le k \le k_{\max}$. Then $\phi_c = \langle k \rangle / (\langle k^2 \rangle - \langle k \rangle)$ is about $0.149$ for $k_{\max} = 100$, $0.043$ for $k_{\max} = 1000$, and $0.013$ for $k_{\max} = 10^4$: the larger the hubs, the smaller the threshold.

**Non-examples.**

- Removing vertices in a chosen order, such as by decreasing degree, is not percolation in the strict sense, because the removals are not independent. It is studied with the same tools as "targeted attack".
- A process in which the kept vertices must have at least $k$ kept neighbours, removed one after another until none is left, is *bootstrap* or $k$-core percolation, which can have a discontinuous transition.

## Where it is used

- **Robustness of networks.** The Internet, power grids and transport networks under random failures and attacks, measured by the giant component after removals.
- **[Epidemics](/sir-epidemic-model/).** The final size of an SIR epidemic in which each infected vertex infects each neighbour with probability $T$ is the size of the bond percolation cluster of the first infected vertex with $\phi = T$, so the [epidemic threshold](/epidemic-threshold/) is a percolation threshold. Vaccinating a fraction of the vertices is site percolation.
- **Physics and materials.** Flow through porous rock, conductivity of composite materials, and gelation of polymers, mostly on lattices.
- **[Random geometric graphs](/random-geometric-graph/).** Continuum percolation: the radius at which disks around random points form a giant cluster, used for wireless networks.
- **Algorithms.** Union-find with random insertions, and the analysis of random graphs in theoretical computer science.

## References
