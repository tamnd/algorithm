---
tag: FAARYD
kind: concept
slug: small-world-network
name: Small-world network
aliases:
- small world
area: graphs/network-analysis
level: core
summary: Network with high clustering and logarithmic average path length.
prereqs: [clustering-coefficient, shortest-path, erdos-renyi-model]
see_also: [watts-strogatz-model, six-degrees-of-separation, kleinberg-small-world-model, clustering-coefficient, scale-free-network, triadic-closure, effective-diameter, navigable-small-world]
sources:
  - paper: doi:10.1038/30918
    title: Duncan J. Watts and Steven H. Strogatz, Collective dynamics of small-world networks, Nature 393, 440 to 442 (1998)
    locator: the whole paper (the definition by comparison with a random graph, and Table 1 with L and C for the film actors, the power grid and C. elegans)
  - paper: doi:10.1371/journal.pone.0002051
    title: Mark D. Humphries and Kevin Gurney, Network small-world-ness, a quantitative method for determining canonical network equivalence, PLoS ONE 3(4), e0002051 (2008)
    locator: the definition of the index sigma as the ratio of the normalized clustering to the normalized path length
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 8, The large-scale structure of networks (the section on the small-world effect), and Chapter 15 (the small-world model)
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 20, The small-world phenomenon
---

A small-world network is a [graph](/graph/) whose typical [shortest-path](/shortest-path/) distance is as small as that of a random graph with the same number of vertices and edges, about the logarithm of the number of vertices, while its [clustering coefficient](/clustering-coefficient/) is much higher than that of the random graph. The term and the test come from Watts and Strogatz (1998), who found this combination in a film actor network, a power grid and the neural network of a worm, and built the [Watts-Strogatz model](/watts-strogatz-model/) to explain it. It is the graph form of [six degrees of separation](/six-degrees-of-separation/).

## In plain words

Two things are true of many real networks at the same time. First, your friends tend to know each other: the network is full of tight local groups. Second, you can still reach almost anyone in a few steps.

These two facts seem to pull in opposite directions. A network made only of tight local groups, like people who know only their neighbours on a street, has very long chains. A network of random links has short chains but no groups.

A small-world network has both. A few links that jump far away are enough to make the chains short, and they are too few to break up the local groups. Social networks, the links between brain cells and power grids all look like this.

## The idea

**The comparison.** Let $G$ be an undirected graph without weights, with $n$ vertices and $m$ edges, and mean degree $k = 2m/n$. Let $L$ be its mean shortest-path distance and $C$ its clustering coefficient (the average local coefficient, or the transitivity; the choice must be stated). Let $L_r$ and $C_r$ be the same quantities for a random graph with the same $n$ and $m$, such as the [Erdős-Rényi graph](/erdos-renyi-model/) $G(n, m)$, for which $L_r \approx \ln n / \ln k$ and $C_r \approx k/n$. Watts and Strogatz call $G$ a small world when

$$L \gtrsim L_r \quad \text{and} \quad C \gg C_r.$$

**An index.** Humphries and Gurney turn this into one number,

$$\sigma = \frac{C / C_r}{L / L_r},$$

and call a network a small world when $\sigma > 1$, in practice when $\sigma$ is well above 1. The index depends on $n$: $C_r$ shrinks like $1/n$, so for a large sparse graph with any fixed clustering $\sigma$ is large. It should be compared only between networks of similar size, or with a stated null model. A [configuration model](/configuration-model/) with the same degrees is a better null model than $G(n, m)$ when the degrees are very uneven.

**An asymptotic form.** For a family of graphs with $n \to \infty$ and a fixed mean degree, a common formal version is: $L = O(\log n)$, and $C$ stays above a positive constant. The Erdős-Rényi graph fails the second condition ($C \to 0$), the ring lattice fails the first ($L \sim n/(2k)$), and the Watts-Strogatz graph with a fixed small rewiring probability satisfies both.

**Directed graphs, weights and disconnected graphs.** The test is defined for undirected graphs without weights. A directed graph is usually made undirected first. When the graph is not connected, $L$ is the mean over the pairs that are connected, which in practice means over the [giant component](/giant-component/), and the random graph used for $L_r$ should be restricted the same way. An alternative that needs no special case is the harmonic mean of the distances, in which a pair at distance $\infty$ adds 0.

## Examples

**The three networks of Watts and Strogatz.** Their Table 1 gives the following values, with $L_r$ and $C_r$ from a random graph with the same $n$ and $k$. The last column is computed from these values.

| network | $L$ | $L_r$ | $C$ | $C_r$ | $\sigma$ |
|---|---|---|---|---|---|
| film actors | 3.65 | 2.99 | 0.79 | 0.00027 | 2397 |
| power grid of the western USA | 18.7 | 12.4 | 0.080 | 0.005 | 10.6 |
| neural network of *C. elegans* | 2.65 | 2.25 | 0.28 | 0.05 | 4.8 |

In each case $L$ is within a factor of about 1.5 of $L_r$, while $C$ is 5 to 3000 times $C_r$. The very large $\sigma$ of the actor network comes mostly from its size: $C_r$ is tiny because the graph is large and sparse.

**The Watts-Strogatz model.** With $n = 1000$, $k = 10$ and rewiring probability $0.01$, samples of the model have $C \approx 0.645$ and $L \approx 8.6$. Against $C_r = k/n = 0.01$ and $L_r \approx \ln 1000 / \ln 10 = 3$, this gives $\sigma \approx 64.5 / 2.9 \approx 22$. The ring lattice without rewiring has $L \approx 50.5$ and $C = 2/3$, so $\sigma \approx 66.7 / 16.8 \approx 4$: it has the clustering but not the short paths.

**Non-examples.**

- A long cycle has $L \approx n/4$ and $C = 0$. It fails both conditions.
- A sparse Erdős-Rényi graph has short paths but $C \approx k/n \to 0$, so $\sigma \approx 1$.
- A two-dimensional grid has $L$ of order $\sqrt n$ and $C = 0$.
- A [scale-free network](/scale-free-network/) of the [Barabási-Albert](/barabasi-albert-model/) type has very short paths, but its clustering also goes to 0 as $n$ grows, so it is not a small world in the asymptotic sense, although it can pass the test of $\sigma$ at a fixed size.

## Where it is used

- [Watts-Strogatz model](/watts-strogatz-model/): the model that produces small worlds from a lattice.
- [Kleinberg small-world model](/kleinberg-small-world-model/): when short paths in a small world can be found by greedy routing.
- [Navigable small world](/navigable-small-world/) graphs and HNSW: nearest-neighbour search indexes that use long links for fast greedy search.
- [Six degrees of separation](/six-degrees-of-separation/): the social observation behind the concept.
- [Triadic closure](/triadic-closure/): the mechanism behind the high clustering.
- Epidemics and [percolation](/percolation/): a few shortcuts change how fast a disease spreads on a lattice, which was one of the questions of the original paper.

## References
