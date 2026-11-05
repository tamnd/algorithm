---
tag: N95D2A
kind: model
slug: barabasi-albert-model
name: Barabási-Albert model
aliases:
- BA model
- preferential attachment model
area: graphs/network-analysis
level: core
summary: A growing random graph in which each new vertex joins m old vertices chosen with probability proportional to their degree, which gives a power-law degree distribution.
prereqs: [degree-distribution, erdos-renyi-model]
see_also: [scale-free-network, preferential-attachment, degree-distribution, configuration-model, chung-lu-model, kronecker-graph-model, watts-strogatz-model]
sources:
  - paper: doi:10.1126/science.286.5439.509
    title: Albert-László Barabási and Réka Albert, Emergence of scaling in random networks, Science 286(5439), 509 to 512 (1999)
    locator: the whole paper (growth with preferential attachment, and the mean-field exponent 3)
  - paper: doi:10.1002/rsa.1009
    title: Béla Bollobás, Oliver Riordan, Joel Spencer and Gábor Tusnády, The degree sequence of a scale-free random graph process, Random Structures and Algorithms 18(3), 279 to 290 (2001)
    locator: the main theorem (the exact form of the limit degree distribution, for degrees up to a power of n)
  - paper: doi:10.1007/s00493-004-0002-2
    title: Béla Bollobás and Oliver Riordan, The diameter of a scale-free random graph, Combinatorica 24(1), 5 to 34 (2004)
    locator: the main theorem (diameter asymptotic to log n / log log n for m at least 2)
  - book: isbn:9781107076266
    title: Albert-László Barabási, Network Science, Cambridge University Press, 2016
    locator: Chapter 5, The Barabási-Albert model (the model, the continuum theory of degree growth, the degree distribution, and the absence of growth or of preferential attachment)
  - book: isbn:9781107172876
    title: Remco van der Hofstad, Random Graphs and Complex Networks, Volume 1, Cambridge University Press, 2017
    locator: Chapter 8, Preferential attachment models (definitions, the degree sequence and the maximal degree)
  - paper: doi:10.1002/asi.4630270505
    title: Derek de Solla Price, A general theory of bibliometric and other cumulative advantage processes, Journal of the American Society for Information Science 27(5), 292 to 306 (1976)
    locator: the whole paper (the cumulative advantage model of citations)
  - paper: doi:10.1103/PhysRevE.71.036113
    title: Vladimir Batagelj and Ulrik Brandes, Efficient generation of large random networks, Physical Review E 71, 036113 (2005)
    locator: the linear-time algorithm for preferential attachment graphs with an array of edge ends
---

The Barabási-Albert model is a random graph that grows one [vertex](/vertex/) at a time: each new vertex brings $m$ edges and joins them to old vertices chosen with probability proportional to their [degree](/degree/). This rule, [preferential attachment](/preferential-attachment/), lets early and well-linked vertices gain links faster, and the [degree distribution](/degree-distribution/) tends to a power law $p_k \sim 2m^2 k^{-3}$. Barabási and Albert proposed it in 1999 to explain the heavy tails of the web and other [scale-free networks](/scale-free-network/); Bollobás, Riordan, Spencer and Tusnády made it exact and proved the degree law.

## The machine

**Parameters.** An integer $m \ge 1$, a final size $n$, and a small seed graph $G_{t_0}$, for example the [complete graph](/complete-graph/) on $m + 1$ vertices, so that each seed vertex has degree $m$.

**One step.** At time $t > t_0$, add a new vertex $t$. Choose $m$ old vertices $u$, each with probability

$$\Pr[t \to u] = \frac{d_{t-1}(u)}{\sum_{w} d_{t-1}(w)} = \frac{d_{t-1}(u)}{2 e_{t-1}},$$

where $d_{t-1}(u)$ is the degree of $u$ and $e_{t-1}$ the number of edges before the step, and add the $m$ edges from $t$ to them. The original paper does not say how the $m$ choices depend on each other. Two exact versions are common.

- *Distinct targets.* Draw targets by the rule above and redraw a vertex that is already chosen. The graph stays simple.
- *The linearized chord diagram* of Bollobás and Riordan. Add the $m$ edges one at a time, and let the new vertex itself be a possible target, with its current degree plus 1. This allows loops and parallel edges, but it makes the model exact and easy to analyse. For $m \ge 2$ it is defined from $G^{(1)}_{mn}$ by merging each run of $m$ vertices into one.

**The kind of graph.** The result is an undirected graph without weights. Its edges are naturally oriented from the newer to the older vertex, and many studies keep this order, for example when they count citations. The graph is connected, because each new vertex attaches to the graph that already exists. For $m = 1$ it is a [tree](/tree/).

**Generating a sample.** Keep an array with both ends of each edge. A vertex of degree $d$ appears $d$ times in it, so a uniform random entry is a degree-proportional choice. Each step draws $m$ entries and appends $2m$ entries, so the whole graph takes $O(nm)$ time, which is linear in the number of edges. Batagelj and Brandes give this method.

## What it counts

The model is a sequence of random graphs $G_t$, and one studies their statistics as $t \to \infty$, with $m$ fixed.

**Degree growth, a mean-field argument.** Treat $d_t(i)$ as a smooth function of $t$. A vertex gains on average $m \cdot d_t(i)/(2mt)$ edges per step, since $e_t \approx mt$. So

$$\frac{\mathrm{d}\, d_t(i)}{\mathrm{d}t} = \frac{d_t(i)}{2t}, \qquad d_i(i) = m, \qquad \text{which gives} \qquad d_t(i) = m \sqrt{t/i}.$$

The vertices that arrive early gain the most. A vertex has degree less than $k$ exactly when $i > m^2 t/k^2$, which is a fraction $1 - m^2/k^2$ of the vertices. Taking the derivative in $k$ gives the density $p_k \approx 2 m^2 / k^3$. This argument is a heuristic, not a proof.

**The exact degree law.** Let $n_k(t)$ be the number of vertices of degree $k \ge m$ at time $t$. In one step, a vertex of degree $k$ is hit with probability about $k/(2t)$, which moves it to degree $k + 1$, and the new vertex enters at degree $m$. If $n_k(t) \approx p_k t$, then the expected change gives

$$p_k = \frac{k-1}{2} p_{k-1} - \frac{k}{2} p_k \ \ (k > m), \qquad p_m = 1 - \frac{m}{2} p_m.$$

So $p_m = \frac{2}{m+2}$ and $p_k = \frac{k-1}{k+2}\, p_{k-1}$, and the product telescopes:

$$p_k = \frac{2}{m+2} \prod_{j = m+1}^{k} \frac{j-1}{j+2} = \frac{2 m (m+1)}{k (k+1) (k+2)}, \qquad k \ge m.$$

Bollobás, Riordan, Spencer and Tusnády proved for the linearized chord diagram that the fraction of vertices of degree $k$ in $G^{(m)}_n$ is a.a.s. $(1 + o(1))\, p_k$, uniformly for $m \le k \le n^{1/15}$. For large $k$, $p_k \sim 2m(m+1) k^{-3}$, a power law with exponent 3, whatever $m$ is.

**Ties and disconnected graphs.** Ties do not arise in the rule: when two old vertices have the same degree, they have the same probability. The graph is always connected, so the model has no rule for disconnected graphs. A model with vertices that bring no edges, or with edge deletion, would need one.

## Relation to other models

- **[Erdős-Rényi model](/erdos-renyi-model/).** $G(n, p)$ has no growth and no preference, and its degree law has a Poisson tail. Barabási and Albert showed that both ingredients are needed: growth with uniform attachment gives an exponential degree law, and preferential rewiring without growth does not give a stationary power law (Network Science, Chapter 5).
- **[Preferential attachment](/preferential-attachment/).** The general rule has an attachment function $f(k)$. A linear $f(k) = k + a$ with $a > -m$ gives the exponent $3 + a/m$. A sublinear $f$ gives a stretched-exponential tail, and a superlinear $f$ makes one vertex take almost all edges. Network Science, Chapter 5, treats these cases.
- **Price's model.** In 1976, Price gave a directed growth model of citations with a cumulative advantage rule: a new paper cites an old one with probability proportional to its in-degree plus a constant. The BA model is close to the undirected case of this rule.
- **Static models with given degrees.** The [configuration model](/configuration-model/) and the [Chung-Lu model](/chung-lu-model/) can match the same degree law without growth. They differ from BA in their degree correlations and in their order of arrival.
- **Clustering.** Like $G(n, p)$, the BA model has a clustering coefficient that tends to 0 as $n$ grows. The [Watts-Strogatz model](/watts-strogatz-model/) has high clustering but no heavy tail.
- **[Kronecker graphs](/kronecker-graph-model/)** give heavy tails and shrinking diameters with a different, recursive rule.

## Known results in the model

| quantity, $m$ fixed | result |
|---|---|
| degree law | $p_k = \frac{2m(m+1)}{k(k+1)(k+2)}$ for $k \ge m$, so exponent 3 (Bollobás, Riordan, Spencer and Tusnády) |
| degree of vertex $i$ at time $t$ | of order $m\sqrt{t/i}$; the largest degree is of order $n^{1/2}$ |
| diameter, $m \ge 2$ | a.a.s. $(1 + o(1)) \log n / \log \log n$ (Bollobás and Riordan, 2004) |
| diameter, $m = 1$ | the graph is a random recursive tree with preferential attachment, with diameter $\Theta(\log n)$ |
| clustering | tends to 0 as $n \to \infty$ |
| connectivity | always connected |

**A simulation.** One sample of the distinct-targets version with $m = 2$, the seed $K_3$ and $n = 100000$ vertices has these fractions of vertices of each degree.

| $k$ | 2 | 3 | 4 | 5 | 10 |
|---|---|---|---|---|---|
| sample | 0.5021 | 0.1982 | 0.1000 | 0.0573 | 0.0089 |
| $p_k = \frac{12}{k(k+1)(k+2)}$ | 0.5000 | 0.2000 | 0.1000 | 0.0571 | 0.0091 |

The largest degree in this sample is 785, of the order of $m \sqrt{n} \approx 632$. In $G(n, p)$ with the same mean degree 4, the degrees are close to Poisson with mean 4, and the expected number of vertices of degree at least 17 among $10^5$ is about 0.11, so by the Markov inequality the largest degree is 16 or less with probability at least 0.88.

**A first step by hand.** Start from the triangle on $\{0, 1, 2\}$ with $m = 2$: each vertex has degree 2 and the sum is 6. Vertex 3 picks each old vertex with probability $2/6$. Say it joins 0 and 1. Now the degrees are $3, 3, 2, 2$ with sum 10, and vertex 4 picks vertex 0 first with probability $3/10$ and vertex 2 with probability $2/10$.

## References
