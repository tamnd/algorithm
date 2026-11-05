---
tag: X4TXHT
kind: model
slug: watts-strogatz-model
name: Watts-Strogatz model
aliases:
- WS model
- rewired ring lattice
area: graphs/network-analysis
level: core
summary: Ring lattice with random rewiring that interpolates between order and randomness.
prereqs: [clustering-coefficient, shortest-path, erdos-renyi-model]
see_also: [small-world-network, six-degrees-of-separation, kleinberg-small-world-model, clustering-coefficient, erdos-renyi-model, barabasi-albert-model, random-geometric-graph, percolation]
sources:
  - paper: doi:10.1038/30918
    title: Duncan J. Watts and Steven H. Strogatz, Collective dynamics of small-world networks, Nature 393, 440 to 442 (1998)
    locator: the whole paper (the rewiring procedure, Figure 2 with C(p)/C(0) and L(p)/L(0) for n = 1000 and k = 10, and the three real networks)
  - paper: doi:10.1007/s100510050067
    title: Alain Barrat and Martin Weigt, On the properties of small-world network models, European Physical Journal B 13(3), 547 to 560 (2000)
    locator: the clustering coefficient of the ring lattice, the approximation C(p) ≈ C(0)(1 − p)^3, and the degree distribution of the rewired graph
  - paper: doi:10.1103/PhysRevE.60.7332
    title: M. E. J. Newman and D. J. Watts, Scaling and percolation in the small-world network model, Physical Review E 60(6), 7332 to 7342 (1999)
    locator: the variant that adds shortcuts without removing edges, and the scaling form of the mean distance in the number of shortcuts
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 15, Other network models (the section on the small-world model)
---

The Watts-Strogatz model is a random [graph](/graph/) model that starts from a ring lattice, where each vertex is joined to its $k$ nearest neighbours, and moves each edge to a random endpoint with probability $\beta$. At $\beta = 0$ the graph is regular, with a high [clustering coefficient](/clustering-coefficient/) and long paths; at $\beta = 1$ it is close to a random graph, with short paths and low clustering. Watts and Strogatz (1998) showed that a small $\beta$ already makes the paths short while the clustering stays high, and called such graphs [small-world networks](/small-world-network/).

## The machine

**Parameters.** The number of vertices $n$, an even mean degree $k$, and the rewiring probability $\beta \in [0, 1]$. The usual regime is $n \gg k \gg \ln n \gg 1$, where $k \gg \ln n$ keeps the graph connected with high probability even at $\beta = 1$.

**The ring lattice.** Place the vertices $0, 1, \ldots, n-1$ on a circle. Join each vertex $i$ to $i \pm 1, \ldots, i \pm k/2$, with indices mod $n$. This graph $R(n, k)$ is $k$-regular, undirected and without weights, and has $nk/2$ edges.

**Rewiring.** For $j = 1, \ldots, k/2$ in turn, and for each vertex $i$ in clockwise order: take the edge $\{i, i + j\}$ of the lattice. With probability $\beta$, independently of all other choices, replace it by $\{i, w\}$, where $w$ is chosen uniformly from the vertices that are not $i$ and not already adjacent to $i$. Otherwise keep it. This forbids self-loops and repeated edges, so the result is a simple graph with exactly $nk/2$ edges, and each vertex keeps at least the $k/2$ edges it did not rewire from its own side.

**Randomness and ties.** The model defines a probability distribution on graphs; one run is one sample. Measures on the model are expectations over samples, or the values on one large sample, which are close to the expectations when $n$ is large. Vertices are not ranked, so there are no ties to break.

## What it counts

The model is used to study two statistics as functions of $\beta$, each divided by its value at $\beta = 0$.

- **Clustering.** $C(\beta)$ is the average local clustering coefficient $\bar C$ over the vertices of degree at least 2.
- **Path length.** $L(\beta)$ is the mean [shortest-path](/shortest-path/) distance over pairs of vertices. When the rewiring disconnects the graph (possible when $k$ is small and $\beta$ is large), $L$ is taken over the pairs that are connected, and the fraction of disconnected pairs is reported with it.

The point of the model is that the two curves fall at very different rates: $L(\beta)/L(0)$ drops to a small value at a $\beta$ where $C(\beta)/C(0)$ is still close to 1.

## Relation to other models

- **[Erdős-Rényi model](/erdos-renyi-model/).** At $\beta = 1$ every lattice edge is rewired, but each vertex $i$ keeps its end of each of its $k/2$ clockwise edges, so the graph is not exactly $G(n, p)$: its degrees are at least $k/2$, while its mean distance and clustering are close to those of $G(n, k/n)$: $L \approx \ln n / \ln k$ and $C \approx k/n$.
- **Newman-Watts model.** Instead of moving each edge, add a shortcut between a uniform random pair for each lattice edge with probability $\beta$, and keep the lattice. The graph is always connected, which makes the analysis easier, and it has the same small-world behaviour.
- **[Kleinberg small-world model](/kleinberg-small-world-model/).** A grid with long links chosen with probability depending on the distance. It shows when short paths can be found by a local search, which the Watts-Strogatz model does not address.
- **[Barabási-Albert model](/barabasi-albert-model/).** Its degrees follow a power law, while the Watts-Strogatz degrees stay close to $k$, with an exponentially decaying tail.
- **[Random geometric graph](/random-geometric-graph/).** Another model with high clustering from geometry, but without long links, so its paths are long.

## Known results in the model

**Clustering of the lattice.** For $n > 3k/2$,

$$C(0) = \frac{3(k - 2)}{4(k - 1)},$$

which tends to $3/4$ as $k$ grows. *Proof.* Let $h = k/2$. The neighbours of vertex 0 are at the offsets $\pm 1, \ldots, \pm h$. Two neighbours at offsets $a$ and $b$ are adjacent exactly when $|a - b| \le h$; the condition $n > 3h$ makes sure that the circle does not create other adjacencies, since $|a - b| \le 2h < n - h$. Two neighbours on the same side differ by at most $h - 1$, so all $2\binom{h}{2}$ such pairs are adjacent. A pair $a > 0 > b$ is adjacent when $a + |b| \le h$, and there are $\binom{h}{2}$ pairs of positive integers with sum at most $h$. So vertex 0 has $3\binom{h}{2}$ closed pairs out of $\binom{2h}{2}$, and

$$C(0) = \frac{3h(h-1)/2}{h(2h-1)} = \frac{3(h-1)}{2(2h-1)} = \frac{3(k-2)}{4(k-1)}.$$

Every vertex is the same, so this is also $\bar C$ and the transitivity. $\square$

**Path length of the lattice.** In $R(n, k)$, the distance between two vertices at ring distance $j \le n/2$ is $\lceil j/h \rceil$, since each step covers at most $h$ positions. So $L(0) \approx n/(2k)$ for large $n$: it grows linearly in $n$.

**Clustering under rewiring.** Barrat and Weigt showed that a triangle of the lattice survives when none of its three edges is rewired, which gives the approximation

$$C(\beta) \approx C(0)(1 - \beta)^3,$$

where $C(\beta)$ is defined as the ratio of the mean number of closed pairs to the mean number of pairs. It ignores the few triangles made by new edges, which is accurate when $k \ll n$.

**Path length under rewiring.** The mean distance falls as soon as the expected number of shortcuts, about $nk\beta/2$, is large compared with 1. Newman and Watts showed that in the variant with added shortcuts the mean distance has the scaling form $L = (n/k) f(nk\beta)$ for a function $f$ with $f(x) \to $ const as $x \to 0$ and $f(x) \sim (\ln x)/x$ as $x \to \infty$, so $L$ grows like $\ln n$ once $nk\beta \gg 1$.

**The standard example.** Watts and Strogatz used $n = 1000$ and $k = 10$. Then $C(0) = 24/36 = 2/3$, and the exact mean distance of the lattice is $L(0) = 5600/111 \approx 50.45$. The table gives the two ratios, each the mean of 3 samples of the procedure above, and the Barrat-Weigt approximation.

| $\beta$ | $C(\beta)/C(0)$ | $(1 - \beta)^3$ | $L(\beta)/L(0)$ |
|---|---|---|---|
| 0.001 | 0.997 | 0.997 | 0.51 |
| 0.01 | 0.968 | 0.970 | 0.17 |
| 0.1 | 0.730 | 0.729 | 0.087 |
| 1 | 0.014 | 0 | 0.065 |

At $\beta = 0.01$ the paths are about 6 times shorter than in the lattice, while the clustering has lost only 3 percent. At $\beta = 1$ the clustering is near $k/n = 0.01$ divided by $C(0)$, and the mean distance is about 3.3, close to $\ln 1000/\ln 10 = 3$.

**Degrees.** Each vertex has degree at least $k/2$. Barrat and Weigt give the exact degree distribution; for $\beta = 1$ it is $k/2$ plus a Poisson-like variable with mean $k/2$. So there are no hubs, unlike in the [scale-free networks](/scale-free-network/) that many real networks are.

## References
