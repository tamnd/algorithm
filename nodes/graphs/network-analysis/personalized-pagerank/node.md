---
tag: ZFSMYK
kind: definition
slug: personalized-pagerank
name: Personalized PageRank
aliases:
- topic-sensitive PageRank
- random walk with restart
area: graphs/network-analysis
level: advanced
summary: PageRank whose random jumps return to a chosen set of seed nodes.
prereqs: [pagerank, markov-chain, stationary-distribution]
see_also: [pagerank, node-similarity, simrank, katz-centrality, conductance, node2vec, link-prediction, markov-chain]
sources:
  - paper: doi:10.1145/511446.511513
    title: Taher H. Haveliwala, Topic-sensitive PageRank, Proceedings of the 11th International World Wide Web Conference, 517 to 526 (2002)
    locator: the PageRank vectors biased toward the pages of a topic, computed in advance for a set of topics and combined at query time
  - paper: doi:10.1145/775152.775191
    title: Glen Jeh and Jennifer Widom, Scaling personalized web search, Proceedings of the 12th International World Wide Web Conference, 271 to 279 (2003)
    locator: the linearity theorem and the decomposition theorem that writes the vector of a vertex through the vectors of its out-neighbours
  - paper: doi:10.1109/FOCS.2006.44
    title: Reid Andersen, Fan Chung and Kevin Lang, Local graph partitioning using PageRank vectors, Proceedings of the 47th IEEE Symposium on Foundations of Computer Science, 475 to 486 (2006)
    locator: the push algorithm for an approximate vector, its running time independent of the graph size, and the sweep cut with a conductance guarantee
  - book: isbn:9780691122021
    title: Amy N. Langville and Carl D. Meyer, Google's PageRank and Beyond, Princeton University Press, 2006
    locator: Chapter 4, The mathematics of Google's PageRank (the personalization vector in the teleportation term)
---

Personalized PageRank is [PageRank](/pagerank/) in which the random surfer, instead of jumping to a uniformly random vertex, jumps back to a chosen seed vertex, or to a vertex drawn from a chosen seed distribution. The score of a vertex then measures how easy it is to reach from the seeds by short random walks, so the vector ranks the graph from the point of view of the seeds. It is used for recommendation ("who to follow"), for [node similarity](/node-similarity/) and [link prediction](/link-prediction/), and for finding a good cluster around a seed vertex in time that does not depend on the size of the graph.

## Definition

Let $G = (V, E)$ be a directed graph with $V = \{0, \ldots, n-1\}$, and let $P$ be its random walk [transition matrix](/transition-matrix/): $P_{uv} = 1/d^+(u)$ for each arc $(u, v)$, counted with multiplicity. For a weighted graph, $P_{uv} = w_{uv} / \sum_x w_{ux}$ instead. An undirected graph is read as a directed graph with both arcs of each edge. Let $\alpha \in [0, 1)$ be the probability of continuing the walk, and let $s$ be a probability vector on $V$, the *personalization* or *seed* vector.

**No dangling vertices.** When every vertex has an out-arc, the personalized PageRank vector $\pi_s$ is the unique probability vector with

$$\pi_s = (1 - \alpha)\, s + \alpha\, \pi_s P,$$

that is, the [stationary distribution](/stationary-distribution/) of the chain that, at each step, follows a random out-arc with probability $\alpha$ and jumps to a vertex drawn from $s$ with probability $1 - \alpha$. Solving the equation gives

$$\pi_s = (1 - \alpha)\, s \sum_{\ell \ge 0} \alpha^\ell P^\ell = (1 - \alpha)\, s\, (I - \alpha P)^{-1},$$

so $\pi_s(v)$ is the probability that a walk started from a vertex drawn from $s$, which stops after each step with probability $1 - \alpha$, is at $v$ when it stops. With $s$ uniform this is ordinary PageRank. With $s = e_u$, the vector of one vertex $u$, it is the *random walk with restart* from $u$, written $\pi_u$.

**Dangling vertices.** A vertex with no out-arc needs a rule. The usual rules send its mass to the seed distribution $s$, or to a fixed distribution such as the uniform one; the rule must be stated, because the vectors differ. With the second rule, the equation stays linear in $s$.

**Ties and disconnected graphs.** $\pi_s(v) > 0$ exactly when $v$ can be reached from the support of $s$ (under the rule that returns dangling mass to $s$); every other vertex has score 0, which is the main difference from PageRank. A ranking by $\pi_s$ breaks ties by the vertex number.

**Basic facts.**

- *Linearity* (Jeh and Widom). With no dangling vertices, or with dangling mass sent to a fixed distribution, $\pi_{\lambda s + (1-\lambda) t} = \lambda \pi_s + (1 - \lambda) \pi_t$. So $\pi_s = \sum_u s(u)\, \pi_u$, and the vectors of single vertices determine all others.
- *Decomposition.* For a vertex $u$ with out-arcs, $\pi_u = (1 - \alpha)\, e_u + \frac{\alpha}{d^+(u)} \sum_{(u, w) \in E} \pi_w$: one step of the walk from $u$, then a fresh walk.
- *Symmetry on undirected graphs.* If $G$ is undirected with no isolated vertex, then $\pi_u(v)/d(v) = \pi_v(u)/d(u)$ for all $u, v$, because the walk is reversible with respect to the degrees.
- *Local computation* (Andersen, Chung and Lang). Keep an estimate $p$ and a residual $r$, starting from $p = 0$ and $r = e_u$, and *push* at any vertex $x$ with $r(x) \ge \varepsilon\, d(x)$: move $(1 - \alpha) r(x)$ into $p(x)$ and spread $\alpha r(x)$ over the out-neighbours of $x$. The invariant $\pi_u = p + \sum_x r(x)\, \pi_x$ holds throughout, and the total work is $O(1/(\varepsilon(1 - \alpha)))$, independent of $n$.

## Examples and non-examples

**One seed.** Take the graph of the [PageRank](/pagerank/) page: vertices $0, \ldots, 5$ and the arcs $(0,1)$, $(0,2)$, $(1,2)$, $(2,0)$, $(3,2)$, $(3,4)$, $(4,3)$, $(4,5)$, with $\alpha = 0.85$; vertex 5 is dangling. From the seed $0$, only $\{0, 1, 2\}$ can be reached, and the equations $\pi(0) = 0.15 + 0.85\, \pi(2)$, $\pi(1) = 0.85\, \pi(0)/2$ and $\pi(2) = 0.85\, (\pi(0)/2 + \pi(1))$ give

$$\pi_0 = \tfrac{1}{1769}\, (800, 340, 629, 0, 0, 0) \approx (0.452, 0.192, 0.356, 0, 0, 0).$$

The seed itself has the largest score, and vertices 3, 4 and 5 have score 0, while their ordinary PageRank is $3/52$ each.

**A seed with a dangling vertex in reach.** From the seed 3, with dangling mass returned to the seed, the vector is about $(0.245, 0.104, 0.289, 0.225, 0.096, 0.041)$. Vertex 2 beats the seed because both 3 and the cycle $0 \to 1 \to 2$, $0 \to 2$ feed it.

**Linearity needs the right dangling rule.** For the seed vector $s = (e_0 + e_3)/2$ with dangling mass returned to $s$, the score of vertex 0 is about $0.360$, not the average $0.349$ of the two vectors above: returning the dangling mass to $s$ makes the map from $s$ to $\pi_s$ non-linear. With dangling mass sent to the uniform distribution instead, the vector for $s$ is exactly the average of the two single-seed vectors.

**Non-examples.**

- Ordinary PageRank is the special case with uniform $s$, not a different measure, but it is not "personalized": it does not depend on a viewpoint.
- The [Katz score](/katz-centrality/) $\sum_\ell \beta^\ell A^\ell$ counts walks without dividing by the degrees, so a hub that a walk passes through keeps all its weight; personalized PageRank splits the weight among the out-arcs.
- A breadth-first search distance from the seed is not a random-walk score: it ignores how many paths join the two vertices.

## Related definitions

- [PageRank](/pagerank/): the case of a uniform seed distribution, and the power iteration that computes either.
- [Markov chain](/markov-chain/) and [stationary distribution](/stationary-distribution/): personalized PageRank is the stationary distribution of the walk with restarts.
- [SimRank](/simrank/): a similarity built from pairs of walks; it can be written through first meetings of two random walks.
- [Node similarity](/node-similarity/): $\pi_u(v)$, or its symmetrized form, is one of the global scores, called rooted PageRank by Liben-Nowell and Kleinberg.
- [Conductance](/conductance/): a sweep over the vertices in decreasing order of $p(x)/d(x)$, with $p$ from the push method, finds a set of small conductance near the seed.
- [Node2vec](/node2vec/) and other walk-based embeddings: they learn from the same short random walks from each vertex.
- Heat kernel PageRank: the walk length is Poisson instead of geometric, $\pi = e^{-t} \sum_\ell \frac{t^\ell}{\ell!}\, s P^\ell$.

## References
