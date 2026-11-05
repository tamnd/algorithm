---
tag: JK577Z
kind: model
slug: configuration-model
name: Configuration model
aliases:
- random graph with given degree sequence
area: graphs/network-analysis
level: advanced
summary: Random graph with a prescribed degree sequence, built by random stub matching.
prereqs: [degree-distribution, multigraph, perfect-matching, erdos-renyi-model]
see_also: [chung-lu-model, erdos-renyi-model, degree-distribution, giant-component, modularity, assortativity, regular-graph, fisher-yates-shuffle]
sources:
  - paper: doi:10.1016/0097-3165(78)90059-6
    title: Edward A. Bender and E. Rodney Canfield, The asymptotic number of labeled graphs with given degree sequences, Journal of Combinatorial Theory, Series A 24(3), 296 to 307 (1978)
    locator: the whole paper (the asymptotic number of simple graphs with bounded degrees, and the factor exp(−λ − λ²))
  - paper: doi:10.1016/S0195-6698(80)80030-8
    title: Béla Bollobás, A probabilistic proof of an asymptotic formula for the number of labelled regular graphs, European Journal of Combinatorics 1(4), 311 to 316 (1980)
    locator: the whole paper (the pairing model of half-edges and the Poisson limits of the numbers of loops and double edges)
  - paper: doi:10.1002/rsa.3240060204
    title: Michael Molloy and Bruce Reed, A critical point for random graphs with a given degree sequence, Random Structures and Algorithms 6(2-3), 161 to 180 (1995)
    locator: Theorem 1 (the giant component exists when the sum of d(d−2) times the fraction of vertices of degree d is positive)
  - paper: doi:10.1103/PhysRevE.64.026118
    title: M. E. J. Newman, Steven H. Strogatz and Duncan J. Watts, Random graphs with arbitrary degree distributions and their applications, Physical Review E 64(2), 026118 (2001)
    locator: Sections II and III (generating functions for the degree and the excess degree, component sizes and the giant component)
  - book: isbn:9781107172876
    title: Remco van der Hofstad, Random Graphs and Complex Networks, Volume 1, Cambridge University Press, 2017
    locator: Chapter 7, Configuration model (the definition, the number of loops and multiple edges, the probability of being simple, and uniformity given simplicity)
---

The configuration model is a random [graph](/graph/) with a given degree sequence $d_1, \ldots, d_n$. Each vertex $i$ gets $d_i$ half-edges, called stubs, and the stubs are joined in pairs uniformly at random. The result has exactly the prescribed degrees, but may contain self-loops and multiple edges; conditioned on having none, it is a uniform random simple graph with these degrees. It is the standard null model for networks with a given [degree distribution](/degree-distribution/), for example with heavy tails that the [Erdős-Rényi model](/erdos-renyi-model/) cannot produce, and the basis of the null model in [modularity](/modularity/). Bender and Canfield in 1978 and Bollobás in 1980 introduced it to count graphs with given degrees.

## The machine

**Input.** A sequence of non-negative integers $d_1, \ldots, d_n$ with an even sum $2m$.

**Pairing.** Make the set $S$ of $2m$ stubs, $d_i$ of them labelled with vertex $i$. Choose a perfect matching of $S$ uniformly among all $(2m - 1)!! = (2m-1)(2m-3) \cdots 3 \cdot 1$ matchings. Each matched pair of stubs $(s, s')$, with labels $i$ and $j$, becomes an edge $\{i, j\}$. The result is an undirected multigraph without weights in which vertex $i$ has degree $d_i$, a self-loop counting 2.

**Uniformity on simple graphs.** A simple graph $H$ with the degrees $d_i$ arises from exactly $\prod_i d_i!$ matchings: at each vertex, its $d_i$ edges can be given its $d_i$ stubs in any order. This number is the same for every such $H$, so conditioned on the multigraph being simple, it is uniform among the simple graphs with the degree sequence. If the probability of being simple stays bounded away from 0, resampling until the result is simple is a practical exact sampler.

**Generating a sample.** List the stubs, shuffle them with the [Fisher-Yates shuffle](/fisher-yates-shuffle/), and join positions $2k - 1$ and $2k$ for each $k$. This gives a uniform matching in $O(n + m)$ time. Two common variants keep the simple graph:

- **Erased configuration model.** Delete self-loops and merge multiple edges. The result is simple, but the degrees may drop slightly and it is no longer uniform.
- **Repeated configuration model.** Reject and resample until simple, which is exact but slow when the degrees have a heavy tail, because then the probability of being simple tends to 0.

**Directed version.** Each vertex gets in-stubs and out-stubs, with equal totals, and each out-stub is matched to a uniform in-stub.

**Disconnected outputs.** Nothing forces the result to be connected; vertices of degree 0 are isolated, and small components occur. The model is studied as it is, with component sizes as one of its results.

## What it counts

The model is a probability space over multigraphs with a fixed degree sequence. Results are stated for a sequence of degree sequences with $n \to \infty$, usually with the fraction of vertices of degree $k$ tending to a distribution $p_k$ with finite mean, and they hold *asymptotically almost surely* (a.a.s.) when their probability tends to 1.

**Edge probabilities.** For two stubs, the probability that they are matched is $1/(2m - 1)$. So the expected number of edges between distinct vertices $i$ and $j$ is $d_i d_j/(2m - 1)$, and the expected number of self-loops at $i$ is $\binom{d_i}{2}/(2m - 1)$. In total,

$$\mathbb{E}[\text{self-loops}] = \frac{\sum_i d_i(d_i - 1)}{2(2m - 1)}.$$

**Excess degree.** Follow a uniform random stub to the vertex at its other end. That vertex has degree $k$ with probability $k p_k/\langle k \rangle$, where $\langle k \rangle = \sum_k k p_k$, so the number of its other stubs, the excess degree, has the distribution

$$q_k = \frac{(k + 1)\, p_{k+1}}{\langle k \rangle}.$$

Its mean is $(\langle k^2 \rangle - \langle k \rangle)/\langle k \rangle$. The degree of the vertex reached has mean $\langle k^2 \rangle/\langle k \rangle \ge \langle k \rangle$, with equality only when all degrees are equal: a neighbour has more neighbours than a typical vertex. This distribution drives the local structure: near a vertex the graph looks like a branching process with the excess degree as the number of children.

**Clustering and mixing.** A neighbour pair of a vertex is joined with probability about $(\langle k^2 \rangle - \langle k \rangle)^2/(n \langle k \rangle^3)$, which tends to 0 when $\langle k^2 \rangle$ is bounded, so the [clustering](/clustering-coefficient/) vanishes. The degrees at the two ends of an edge are nearly independent, so the [assortativity](/assortativity/) is close to 0.

## Relation to other models

- **Erdős-Rényi.** With degrees drawn from a Poisson distribution with mean $c$, the configuration model behaves like $G(n, c/n)$ for local and component properties. $G(n, p)$ fixes only the mean degree.
- **Chung-Lu.** The [Chung-Lu model](/chung-lu-model/) fixes only the expected degrees, joining $i$ and $j$ independently with probability $w_i w_j / \sum_k w_k$. It is simple and has independent edges but random degrees; the configuration model has exact degrees but dependent edges.
- **Modularity.** The expected number $k_i k_j/(2m)$ of edges between $i$ and $j$ in the null model of [modularity](/modularity/) is, up to $2m$ against $2m - 1$, the expected number in the configuration model.
- **Random regular graphs.** With $d_i = d$ for all $i$, the model conditioned on simplicity is the uniform random $d$-[regular graph](/regular-graph/), which is how most results on random regular graphs are proved.
- **Edge switching.** Swapping the ends of two edges keeps all degrees. A Markov chain of such swaps, rejecting swaps that create loops or multiple edges, also samples simple graphs with the given degrees, without the rejection of whole samples.

## Known results in the model

**Probability of being simple.** For bounded degrees, let $\nu = \sum_i d_i(d_i - 1)/\sum_i d_i$. The numbers of self-loops and of double edges tend to independent Poisson variables with means $\nu/2$ and $\nu^2/4$, so

$$\Pr[\text{simple}] \to e^{-\nu/2 - \nu^2/4}.$$

For a $d$-regular sequence, $\nu = d - 1$ and the limit is $e^{-(d^2 - 1)/4}$. The result extends to degree sequences with a finite second moment of the limit distribution. With an infinite second moment, $\nu \to \infty$ and the probability tends to 0.

**Small exact examples.** Every number below was checked by listing all matchings.

| degree sequence | matchings | simple graphs | matchings per graph | $\Pr[\text{simple}]$ | limit formula |
|---|---|---|---|---|---|
| $2, 2, 1, 1$ | 15 | 2 | 4 | $8/15$ | none |
| $2, 2, 2, 2$ | 105 | 3 (the 4-cycles) | 16 | $16/35 \approx 0.457$ | $e^{-3/4} \approx 0.472$ |
| $3, 3, 3, 3$ | 10395 | 1 ($K_4$) | 1296 | $48/385 \approx 0.125$ | $e^{-2} \approx 0.135$ |

For $2, 2, 1, 1$, the two simple graphs are the paths $2, 0, 1, 3$ and $3, 0, 1, 2$, and the expected number of self-loops is $(2 + 2)/(2 \cdot 5) = 2/5$.

**Giant component.** Molloy and Reed showed that, under conditions on the degree sequence such as bounded maximum degree, a giant component of linear size exists a.a.s. when

$$\sum_k k(k - 2)\, p_k > 0, \quad \text{that is,} \quad \langle k^2 \rangle > 2 \langle k \rangle,$$

and all components are small when the sum is negative. Equivalently, the mean excess degree exceeds 1. For Poisson degrees with mean $c$, $\langle k^2 \rangle = c^2 + c$ and the condition is $c > 1$, the threshold of the [giant component theorem](/erdos-renyi-giant-component-theorem/). For degree distributions with $p_k \sim k^{-\tau}$ and $2 < \tau < 3$, the second moment diverges, so the sum is positive and a giant component exists; this case is outside the bounded-degree setting and needs later extensions of the theorem, such as the one of Janson and Luczak.

**Size of the giant.** Newman, Strogatz and Watts give it with generating functions: let $G_0(x) = \sum_k p_k x^k$ and $G_1(x) = G_0'(x)/G_0'(1)$. If $u$ is the smallest root in $[0, 1]$ of $u = G_1(u)$, the giant has about $(1 - G_0(u))\, n$ vertices.

**Distances.** When $\langle k^2 \rangle$ is finite and the mean excess degree $\bar q$ is above 1, typical distances in the giant are about $\ln n / \ln \bar q$. For $2 < \tau < 3$ they are of order $\ln \ln n$, much shorter.

## References
