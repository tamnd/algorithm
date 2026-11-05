---
tag: Y2580E
kind: definition
slug: degree-distribution
name: Degree distribution
area: graphs/network-analysis
level: intro
summary: The fraction p_k of vertices that have degree k, for each k.
prereqs: [degree, graph]
see_also: [degree-centrality, scale-free-network, erdos-renyi-model, barabasi-albert-model, configuration-model, chung-lu-model, assortativity, poisson-distribution]
sources:
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 8, The large-scale structure of networks (the sections on degree distributions and on power laws and scale-free networks)
  - book: isbn:9781107076266
    title: Albert-László Barabási, Network Science, Cambridge University Press, 2016
    locator: Chapter 2, Graph theory (degree distribution) and Chapter 4, The scale-free property
  - paper: doi:10.1137/070710111
    title: Aaron Clauset, Cosma Rohilla Shalizi and M. E. J. Newman, Power-law distributions in empirical data, SIAM Review 51(4), 661 to 703 (2009)
    locator: Sections 2 and 3 (the maximum likelihood estimator of the exponent, the choice of the lower cut-off, and the warning against least-squares fits on a log-log plot)
  - paper: doi:10.1086/229693
    title: Scott L. Feld, Why your friends have more friends than you do, American Journal of Sociology 96(6), 1464 to 1477 (1991)
    locator: the whole paper (the friendship paradox)
---

The degree distribution of a [graph](/graph/) is the list of the fractions $p_k$ of [vertices](/vertex/) that have [degree](/degree/) $k$, for $k = 0, 1, 2, \ldots$. It is the first statistic computed for a network, and it separates the main random graph models: the [Erdős-Rényi model](/erdos-renyi-model/) gives a Poisson distribution with a thin tail, while many real networks and the [Barabási-Albert model](/barabasi-albert-model/) give a heavy tail with a few hubs. The [configuration model](/configuration-model/) and the [Chung-Lu model](/chung-lu-model/) build random graphs with a given degree distribution.

## Definition

Let $G = (V, E)$ be a graph with $n \ge 1$ vertices, and let $n_k$ be the number of vertices of degree $k$. The **degree distribution** is

$$p_k = \frac{n_k}{n}, \qquad k = 0, 1, 2, \ldots$$

So $p_k \ge 0$ and $\sum_k p_k = 1$: $p_k$ is the probability that a uniform random vertex has degree $k$. The **complementary cumulative distribution** is $P_k = \sum_{j \ge k} p_j$, the fraction of vertices with degree at least $k$.

**Moments.** The mean degree is $\langle k \rangle = \sum_k k\, p_k = 2m/n$, by the [handshake lemma](/handshake-lemma/), where $m = |E|$. The second moment is $\langle k^2 \rangle = \sum_k k^2 p_k$.

**The degree of a neighbour.** Pick a uniform random edge and then one of its two ends at random. The chosen vertex has degree $k$ with probability $q_k = k\, p_k / \langle k \rangle$, because a vertex of degree $k$ is an end of $k$ edges. So the mean degree of a neighbour is

$$\sum_k k\, q_k = \frac{\langle k^2 \rangle}{\langle k \rangle} = \langle k \rangle + \frac{\operatorname{Var}(k)}{\langle k \rangle} \ \ge\ \langle k \rangle,$$

for $m \ge 1$, with equality exactly when all vertices have the same degree. This is the *friendship paradox* of Feld: on average, your friends have more friends than you do. The ratio $\langle k^2 \rangle / \langle k \rangle$ also decides when a [giant component](/giant-component/) appears in the configuration model.

**Power laws.** The distribution has a *power-law tail* with exponent $\alpha > 1$ when $p_k \sim C k^{-\alpha}$ as $k \to \infty$, for a constant $C > 0$. Then $P_k$ behaves like $k^{-(\alpha - 1)}$. For $2 < \alpha \le 3$, which many real networks show, the mean is finite but $\langle k^2 \rangle$ grows without bound with $n$. A graph with such a tail is called [scale-free](/scale-free-network/).

**Directed and weighted graphs.** A directed graph has an in-degree distribution, an out-degree distribution and a joint distribution $p_{jk}$ of the pair (in-degree $j$, out-degree $k$). Both marginal means equal $m/n$. In a weighted graph, the *strength distribution* uses the sum of the weights at each vertex in place of the degree.

**Disconnected graphs and isolated vertices.** The definition is per vertex, so it needs no change for a disconnected graph. Isolated vertices count in $p_0$. Data sets often drop them, which changes all other $p_k$, so a report must say whether $p_0$ is included.

**Cost.** All degrees, and so all $n_k$, take $\Theta(n + m)$ time from an [edge list](/edge-list/) or an [adjacency list](/adjacency-list/), with an array of counters of size $\max_v d(v) + 1 \le n$.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. The degrees are $2, 3, 3, 3, 3, 2, 2$.

| $k$ | $n_k$ | $p_k$ | $P_k$ | $q_k = k p_k / \langle k \rangle$ |
|---|---|---|---|---|
| 2 | 3 | 3/7 | 1 | 1/3 |
| 3 | 4 | 4/7 | 4/7 | 2/3 |

Here $\langle k \rangle = 18/7 \approx 2.571 = 2 \cdot 9 / 7$ and $\langle k^2 \rangle = 48/7$. The mean degree of a neighbour is $48/18 = 8/3 \approx 2.667$, which is larger than $\langle k \rangle$.

**Standard models.**

- [Erdős-Rényi](/erdos-renyi-model/) $G(n, p)$: the degree of a fixed vertex is $\mathrm{Bin}(n-1, p)$. With $p = c/(n-1)$ for a fixed $c$, this tends to the [Poisson distribution](/poisson-distribution/) $p_k = e^{-c} c^k / k!$. Its tail falls faster than any power of $k$.
- A $d$-[regular graph](/regular-graph/): $p_d = 1$.
- [Barabási-Albert](/barabasi-albert-model/) with $m_0$ edges per new vertex: $p_k \to \dfrac{2 m_0 (m_0 + 1)}{k(k+1)(k+2)}$ for $k \ge m_0$, a power law with $\alpha = 3$.
- A star $K_{1, n-1}$: $p_1 = (n-1)/n$ and $p_{n-1} = 1/n$. Here $\langle k \rangle = 2(n-1)/n < 2$, while a random neighbour has mean degree $\langle k^2 \rangle / \langle k \rangle = n/2$.

**Non-examples.**

- The *degree sequence* is not the degree distribution. The sequence lists the degree of each vertex and keeps $n$; the distribution forgets which vertex has which degree and how many vertices there are. Two graphs of different sizes can have the same distribution.
- The degree distribution does not fix the graph, not even up to isomorphism. The 6-cycle and two disjoint triangles both have $p_2 = 1$, but one is connected and the other is not.
- A straight line on a log-log plot of the histogram is not evidence of a power law. Clauset, Shalizi and Newman show that a least-squares fit of such a line gives biased exponents, and that other heavy-tailed laws, such as the log-normal, often fit as well. Their method uses the maximum likelihood estimate of $\alpha$ above a cut-off chosen from the data, followed by a goodness-of-fit test.

## Related definitions

- [Degree](/degree/) and [degree centrality](/degree-centrality/): the per-vertex quantity.
- [Scale-free network](/scale-free-network/) and [preferential attachment](/preferential-attachment/): heavy tails and a process that makes them.
- [Configuration model](/configuration-model/) and [Chung-Lu model](/chung-lu-model/): random graphs with a given degree sequence or expected degrees.
- [Assortativity](/assortativity/): the correlation between the degrees at the two ends of an edge, which the distribution does not capture.

## References
