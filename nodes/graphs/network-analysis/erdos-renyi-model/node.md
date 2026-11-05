---
tag: 8YZQWG
kind: model
slug: erdos-renyi-model
name: Erdős-Rényi random graph model
aliases:
- G(n,m)
- G(n,p)
- G(n,p) model
- random graph
area: graphs/network-analysis
level: core
summary: Each possible edge is present independently with probability p.
prereqs: [graph, binomial-distribution, linearity-of-expectation]
see_also: [erdos-renyi-giant-component-theorem, erdos-renyi-connectivity-threshold, giant-component, configuration-model, chung-lu-model, stochastic-block-model, watts-strogatz-model, barabasi-albert-model]
sources:
  - paper: "Paul Erdős and Alfréd Rényi, On random graphs I, Publicationes Mathematicae Debrecen 6, 290 to 297 (1959)"
    locator: the whole paper (the model with a fixed number of edges, and the threshold for connectivity)
  - paper: doi:10.1214/aoms/1177706098
    title: Edgar N. Gilbert, Random graphs, Annals of Mathematical Statistics 30(4), 1141 to 1144 (1959)
    locator: the whole paper (each edge present with probability p, and the probability of connectivity)
  - book: isbn:9781107118508
    title: Alan Frieze and Michał Karoński, Introduction to Random Graphs, Cambridge University Press, 2016
    locator: Chapter 1, Random graphs (the models G(n,m) and G(n,p), their asymptotic equivalence, and thresholds), Chapter 2, Evolution, and Chapter 4, Connectivity
  - book: isbn:9780521797221
    title: Béla Bollobás, Random Graphs, second edition, Cambridge University Press, 2001
    locator: Chapter 2, Models of random graphs, and Chapter 3, The degree sequence
  - paper: "Paul Erdős and Alfréd Rényi, On the evolution of random graphs, Publications of the Mathematical Institute of the Hungarian Academy of Sciences 5, 17 to 61 (1960)"
    locator: the whole paper (the phase transition at M = n/2 and the giant component)
  - paper: doi:10.1007/BF02579198
    title: Béla Bollobás and Andrew Thomason, Threshold functions, Combinatorica 7(1), 35 to 38 (1987)
    locator: the theorem that every monotone property has a threshold
  - paper: doi:10.1103/PhysRevE.71.036113
    title: Vladimir Batagelj and Ulrik Brandes, Efficient generation of large random networks, Physical Review E 71, 036113 (2005)
    locator: the algorithm for G(n,p) with geometric skips, in expected time linear in n + m
---

The Erdős-Rényi model is the basic model of a random [graph](/graph/). In the version $G(n, p)$, each of the $\binom{n}{2}$ possible edges on $n$ labelled vertices is present with probability $p$, independently of the others. In the version $G(n, M)$, the graph is chosen uniformly from all graphs with exactly $M$ edges. The model is the null model of network science: its [degree distribution](/degree-distribution/) is binomial, its [clustering](/clustering-coefficient/) is low, and it shows sharp thresholds, such as the sudden birth of a [giant component](/giant-component/) at $p = 1/n$.

## The machine

**$G(n, p)$.** Fix $n \ge 1$ and $p \in [0, 1]$. The vertex set is $V = \{1, \ldots, n\}$. For each of the $N = \binom{n}{2}$ unordered pairs $\{u, v\}$, toss an independent coin that shows heads with probability $p$, and put the edge in $E$ when it shows heads. So a fixed simple graph $H$ on $V$ with $m$ edges appears with probability

$$\Pr[G(n, p) = H] = p^{m} (1 - p)^{N - m}.$$

For $p = 1/2$, all $2^N$ graphs on $V$ are equally likely.

**$G(n, M)$.** Fix $0 \le M \le N$. Choose $E$ uniformly from the $\binom{N}{M}$ sets of $M$ pairs. Each graph with $M$ edges then has probability $1/\binom{N}{M}$.

**The kind of graph.** Both models give simple, undirected graphs without weights and without self-loops. The directed version $D(n, p)$ keeps each of the $n(n-1)$ ordered pairs with probability $p$. Weights, when needed, are drawn on top of the graph and are not part of the model.

**Generating a sample.** The direct method tosses $N$ coins and takes $\Theta(n^2)$ time. Batagelj and Brandes list the pairs in a fixed order and jump from one edge to the next by a geometric number of pairs, $\lfloor \ln(1 - r)/\ln(1 - p) \rfloor$ for a uniform $r \in [0, 1)$. This gives a sample of $G(n, p)$ in $O(n + m)$ expected time. For $G(n, M)$ with $M$ much less than $N$, draw random pairs and reject repeats, with a [hash table](/hash-table/) of the pairs already drawn.

## What it counts

The model is a probability space, and one studies the probability of graph properties as $n \to \infty$, with $p = p(n)$ or $M = M(n)$. A property holds *asymptotically almost surely* (a.a.s.) when its probability tends to 1.

**Basic quantities.** Let $X$ be the number of edges, $d(v)$ the [degree](/degree/) of a fixed vertex $v$, and $T$ the number of triangles. By [linearity of expectation](/linearity-of-expectation/) over the indicator of each pair or triple,

$$\mathbb{E}[X] = p \binom{n}{2}, \qquad d(v) \sim \mathrm{Bin}(n - 1, p), \qquad \mathbb{E}[T] = p^3 \binom{n}{3}.$$

With $p = c/n$ for a fixed $c > 0$, the degree of $v$ tends to the [Poisson distribution](/poisson-distribution/) with mean $c$, and $\mathbb{E}[T] \to c^3/6$. Given its degree $k \ge 2$, a vertex has $\mathbb{E}[T(v)] = p \binom{k}{2}$ edges among its neighbours, so its expected local clustering coefficient is $p$.

**Thresholds.** A function $p^*(n)$ is a *threshold* for a property $\mathcal{P}$ when $\Pr[G(n, p) \in \mathcal{P}] \to 0$ if $p/p^* \to 0$, and $\to 1$ if $p/p^* \to \infty$. Bollobás and Thomason proved that every monotone property, one that stays true when edges are added, has a threshold.

**The first moment method.** For a non-negative integer random variable $Y$, $\Pr[Y \ge 1] \le \mathbb{E}[Y]$, by the [Markov inequality](/markov-inequality/). For triangles, if $np \to 0$ then $\mathbb{E}[T] \le (np)^3/6 \to 0$, so a.a.s. there is no triangle. The [Chebyshev inequality](/chebyshev-inequality/) on $T$ gives the other half: if $np \to \infty$, a.a.s. there is a triangle. So $1/n$ is the threshold for a triangle.

## Relation to other models

- **$G(n, p)$ and $G(n, M)$.** Conditioned on having exactly $M$ edges, $G(n, p)$ is distributed as $G(n, M)$, because every graph with $M$ edges has the same probability $p^M (1 - p)^{N - M}$. For a monotone property, the two models agree in the limit when $M \approx pN$ and $pN(1-p) \to \infty$; Frieze and Karoński prove this in Chapter 1.
- **Inhomogeneous models.** The [Chung-Lu model](/chung-lu-model/) uses the probability $w_u w_v / \sum_k w_k$ for the pair $\{u, v\}$. With equal weights $w_u = (n-1)p$ it is close to $G(n, p)$. The [stochastic block model](/stochastic-block-model/) with one block is $G(n, p)$.
- **Given degrees.** The [configuration model](/configuration-model/) fixes the degree sequence. $G(n, p)$ fixes only the mean degree, and its degrees are concentrated, so it cannot give the heavy tails of the [Barabási-Albert model](/barabasi-albert-model/).
- **Clustering.** In $G(n, c/n)$ the clustering coefficient tends to 0, while real social networks have a large one. The [Watts-Strogatz model](/watts-strogatz-model/) keeps high clustering and still has short paths.
- **Geometry.** In a [random geometric graph](/random-geometric-graph/), edges depend on distances in space, so they are not independent.

## Known results in the model

The table lists the classic thresholds of $G(n, p)$ with $c$ a constant.

| property | threshold or result |
|---|---|
| some edge exists | $p^* = n^{-2}$ |
| a tree with $k$ vertices as a subgraph | $p^* = n^{-k/(k-1)}$ |
| a triangle, a cycle | $p^* = 1/n$ |
| a component of size $\Theta(n)$ | $p = c/n$ with $c > 1$; all components $O(\log n)$ for $c < 1$, see the [giant component theorem](/erdos-renyi-giant-component-theorem/) |
| no isolated vertex, and connected | $p = (\ln n + c)/n$ gives the limit $e^{-e^{-c}}$, see the [connectivity threshold](/erdos-renyi-connectivity-threshold/) |
| Hamiltonian cycle | $p = (\ln n + \ln \ln n + c)/n$, the same sharp threshold as minimum degree 2 |
| clique number, $p$ fixed | a.a.s. $(2 + o(1)) \log_{1/p} n$ |

**The giant component.** For $p = c/n$ with $c > 1$, the largest [component](/connected-components/) has about $\beta n$ vertices, where $\beta$ is the positive root of $\beta = 1 - e^{-c\beta}$, and the second largest has $O(\log n)$ vertices. For $c < 1$ all components have $O(\log n)$ vertices. Erdős and Rényi found this phase transition in 1960.

**A small exact example.** Take $n = 4$ and $p = 1/2$. All $2^6 = 64$ graphs are equally likely. The expected number of edges is 3, and the expected number of triangles is $4 \cdot (1/2)^3 = 1/2$. Exactly 38 of the 64 graphs are connected, so $\Pr[\text{connected}] = 19/32$. Exactly 41 graphs have no isolated vertex. The 3 graphs that have no isolated vertex but are not connected are the 3 perfect matchings, two disjoint edges each. For large $n$ near the connectivity threshold, such graphs become rare, and "no isolated vertex" and "connected" have the same limit probability.

**A large example.** Take $n = 1000$ and $p = 0.005$. The expected number of edges is $0.005 \cdot 499500 = 2497.5$, the mean degree is $0.005 \cdot 999 = 4.995$, a vertex is isolated with probability $0.995^{999} \approx 0.00669$, so the expected number of isolated vertices is about 6.69, and the expected number of triangles is $\binom{1000}{3} \cdot 0.005^3 \approx 20.8$. Here $p$ is below $\ln 1000 / 1000 \approx 0.0069$, so isolated vertices are expected and the graph is very likely not connected, but $c \approx 5 > 1$, so it has a giant component.

## References
