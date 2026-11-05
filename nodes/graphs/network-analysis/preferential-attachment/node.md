---
tag: 1SDNKT
kind: concept
slug: preferential-attachment
name: Preferential attachment
aliases:
- rich-get-richer
- Matthew effect
area: graphs/network-analysis
level: core
summary: New links attach to nodes in proportion to their current degree.
prereqs: [degree, degree-distribution, graph]
see_also: [barabasi-albert-model, scale-free-network, degree-distribution, kronecker-graph-model, configuration-model, link-prediction, erdos-renyi-model, homophily]
sources:
  - paper: doi:10.1126/science.286.5439.509
    title: Albert-László Barabási and Réka Albert, Emergence of scaling in random networks, Science 286(5439), 509 to 512 (1999)
    locator: the model with growth and linear preferential attachment, and the mean-field result that the degree exponent is 3
  - paper: doi:10.1002/asi.4630270505
    title: Derek de Solla Price, A general theory of bibliometric and other cumulative advantage processes, Journal of the American Society for Information Science 27(5), 292 to 306 (1976)
    locator: the whole paper (cumulative advantage in a citation network, with attachment in proportion to the citations plus one)
  - paper: doi:10.1093/biomet/42.3-4.425
    title: Herbert A. Simon, On a class of skew distribution functions, Biometrika 42(3/4), 425 to 440 (1955)
    locator: the whole paper (the urn process in which new items join a class with probability proportional to its size)
  - paper: doi:10.1103/PhysRevLett.85.4629
    title: P. L. Krapivsky, S. Redner and F. Leyvraz, Connectivity of growing random networks, Physical Review Letters 85(21), 4629 to 4632 (2000)
    locator: the rate equations for attachment kernels proportional to k^α, with the sublinear, linear and superlinear cases
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 14, Models of network formation (Price's model, the master equation and its solution, and the Barabási-Albert model)
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 18, Power laws and rich-get-richer phenomena
---

Preferential attachment is a rule for a growing network: each new edge attaches to an existing vertex with probability proportional to that vertex's current [degree](/degree/), so vertices that already have many links gain new ones faster. With linear attachment and steady growth, the [degree distribution](/degree-distribution/) becomes a power law with exponent 3, which makes the network [scale-free](/scale-free-network/). The idea is old: Simon used it in 1955 for word frequencies and city sizes, Price in 1976 for citations, and Barabási and Albert in 1999 for the web, in the [Barabási-Albert model](/barabasi-albert-model/).

## In plain words

When a new web page links to other pages, it is more likely to link to a page that is already famous, because people find famous pages more easily. When a scientist cites papers, they cite the ones that many others cite. So the rich get richer.

The rule is simple: the chance that a newcomer picks a member is in proportion to how many links that member already has. A member with ten links is ten times as likely to be picked as a member with one.

Over time, this rule turns small early differences into huge ones. The oldest and luckiest members become hubs with thousands of links, while most members keep only a few. The counts of links then follow a power law.

## The idea

**The rule.** Let $G_t$ be an undirected graph without weights at time $t$, with degrees $k_i(t)$. A new vertex arrives with $m$ edges. Each edge goes to the existing vertex $i$ with probability

$$\Pi(i) = \frac{k_i}{\sum_j k_j} = \frac{k_i}{2|E(G_t)|}.$$

This is *linear* preferential attachment. Ties are not an issue, because the choice is random; the rule gives equal probability to equal degrees. The graph built this way is connected if the start graph is, since each new vertex attaches to it. For a directed graph such as a citation network, the attachment uses the in-degree, and a constant is added so that a vertex with in-degree 0 can be cited: $\Pi(i) \propto k^{\mathrm{in}}_i + a$ with $a > 0$ (Price used $a = 1$).

**The degree law, by the master equation.** Take $m$ edges per new vertex, linear attachment, and let $p_k(n)$ be the fraction of vertices of degree $k$ when there are $n$ vertices. When one vertex is added, the expected number of edges that land on vertices of degree $k$ is $m \cdot n p_k \cdot k/(2mn) = k p_k / 2$, for large $n$. Each of those vertices moves to degree $k + 1$. So

$$(n + 1)\, p_k(n + 1) - n\, p_k(n) = \tfrac12 (k - 1) p_{k-1}(n) - \tfrac12 k\, p_k(n) + [k = m].$$

Assume that $p_k(n) \to p_k$. Then for $k > m$, $p_k = \tfrac12 (k-1) p_{k-1} - \tfrac12 k p_k$, so $p_k = \frac{k - 1}{k + 2}\, p_{k-1}$. For $k = m$, $p_m = 1 - \tfrac12 m p_m$, so $p_m = \frac{2}{m + 2}$. The product telescopes:

$$p_k = \frac{2}{m+2} \prod_{j=m+1}^{k} \frac{j - 1}{j + 2} = \frac{2}{m+2} \cdot \frac{m(m+1)(m+2)}{k(k+1)(k+2)} = \frac{2m(m+1)}{k(k+1)(k+2)} \sim 2m(m+1)\, k^{-3}.$$

This derivation treats the expected change as the actual change; Bollobás, Riordan, Spencer and Tusnády proved the same law rigorously for a precise version of the model. The general case $\Pi \propto k + a$ gives the exponent $\gamma = 3 + a/m$, so a shift tunes $\gamma$ anywhere above 2.

**The degree of one vertex.** In the mean-field view, a vertex born at time $t_i$ gains degree at the rate $\frac{dk_i}{dt} = m \frac{k_i}{2mt} = \frac{k_i}{2t}$, so $k_i(t) = m \sqrt{t/t_i}$. Old vertices are the hubs: a vertex that arrived first has degree about $m\sqrt t$ at time $t$. This is the "first-mover advantage" of the model.

**Other kernels.** Krapivsky, Redner and Leyvraz studied $\Pi(i) \propto k_i^\alpha$:

- $\alpha < 1$ (sublinear): the degree law is a stretched exponential, not a power law.
- $\alpha = 1$ (linear): a power law, as above.
- $\alpha > 1$ (superlinear): one vertex gets a positive fraction of all edges ("winner takes all"), and for $\alpha > 2$ a single vertex is joined to almost every other vertex.

So the power law needs the attachment to be linear, not only increasing.

**Sampling in constant time.** To pick a vertex with probability proportional to its degree, keep a list of all edge endpoints, in which vertex $i$ appears $k_i$ times, and pick a uniform entry. Adding a vertex with $m$ edges appends $2m$ entries. A whole graph with $n$ vertices takes $O(nm)$ time.

## Examples

**One step.** Let the current degrees be $3, 2, 2, 1, 1, 1$, so $\sum_j k_j = 10$. A new vertex with $m = 1$ attaches to the first vertex with probability $0.3$, to each vertex of degree 2 with probability $0.2$, and to each leaf with probability $0.1$. After it attaches to the first vertex, the degrees are $4, 2, 2, 1, 1, 1, 1$, and the first vertex has probability $4/12 \approx 0.333$ at the next step.

**The limit law for $m = 1$.** The formula gives $p_k = \frac{4}{k(k+1)(k+2)}$: $p_1 = 2/3$, $p_2 = 1/6$, $p_3 = 1/15$, $p_4 = 1/30$ and $p_{10} = 1/330 \approx 0.00303$. A sample with $2 \times 10^5$ vertices, grown from one edge with the endpoint-list method, had the fractions $0.668$, $0.165$, $0.067$, $0.034$ and $0.0030$, and its largest degree was 548. A uniform attachment with $m = 1$ would give the geometric law $p_k = 2^{-k}$, with $p_{10} \approx 0.001$ and a largest degree of order $\log n$.

**The Matthew effect.** Merton named the social version after the verse "unto every one that hath shall be given": well-known scientists get more credit for the same work than unknown ones. Preferential attachment is a mathematical form of this.

**Non-examples.**

- The [Erdős-Rényi model](/erdos-renyi-model/) adds edges between uniform random pairs, with no preference, and its degrees are close to Poisson.
- A growing tree in which each new vertex attaches to a uniform random old vertex (the random recursive tree) has a geometric degree law, not a power law. Growth alone is not enough.
- Linking to the vertex of largest degree, always, is not preferential attachment: it is deterministic and produces a star.

## Where it is used

- [Barabási-Albert model](/barabasi-albert-model/): the standard network model built on this rule.
- [Scale-free network](/scale-free-network/): the property that the rule explains.
- [Link prediction](/link-prediction/): the score $k_u k_v$, called preferential attachment, predicts a new edge between two vertices of high degree.
- [Kronecker graph model](/kronecker-graph-model/), [configuration model](/configuration-model/) and [Chung-Lu model](/chung-lu-model/): other ways to get heavy-tailed degrees, without growth.
- Bibliometrics, the sizes of cities and firms, and word frequencies: the older settings of the same process, from Yule and Simon.

## References
