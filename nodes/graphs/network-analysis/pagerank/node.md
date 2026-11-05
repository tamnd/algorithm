---
tag: YEWMFK
kind: algorithm
slug: pagerank
name: PageRank
aliases:
- Google PageRank
- random surfer model
area: graphs/network-analysis
level: core
summary: Stationary distribution of a random walk with teleportation, computed by power iteration.
solves: [link-analysis-ranking]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, k: the number of iterations}
  time: {worst: Θ(k(n + m))}
  space: {extra: Θ(n)}
properties: {directed: true, weighted: false, deterministic: true, recursive: false}
history:
  year: 1998
  people: [Sergey Brin, Lawrence Page]
  note: Brin and Page described PageRank as the ranking of the Google search engine in 1998.
prereqs: [directed-graph, markov-chain, stationary-distribution, power-iteration]
see_also: [personalized-pagerank, eigenvector-centrality, katz-centrality, hits-algorithm, link-analysis-ranking, centrality, perron-frobenius-theorem, transition-matrix]
sources:
  - paper: doi:10.1016/S0169-7552(98)00110-X
    title: Sergey Brin and Lawrence Page, The anatomy of a large-scale hypertextual Web search engine, Computer Networks and ISDN Systems 30(1 to 7), 107 to 117 (1998)
    locator: Section 2.1, PageRank (the formula with the damping factor d and the random surfer)
  - book: isbn:9780691122021
    title: Amy N. Langville and Carl D. Meyer, Google's PageRank and Beyond, The Science of Search Engine Rankings, Princeton University Press, 2006
    locator: Chapter 4, The mathematics of Google's PageRank (the stochastic and the primitive adjustments, and the power method), and Chapter 6, The sensitivity of PageRank (the role of the damping factor)
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 14, Link analysis and web search (the basic and the scaled PageRank update rules and the random walk view)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on PageRank, as a variant of Katz centrality)
---

PageRank scores the vertices of a [directed graph](/directed-graph/) by the long-run fraction of time that a random surfer spends at each one. The surfer follows a random out-arc with probability $\alpha$ (usually $0.85$) and jumps to a uniformly random vertex otherwise. The scores form the [stationary distribution](/stationary-distribution/) of this [Markov chain](/markov-chain/), and the algorithm computes them by [power iteration](/power-iteration/): each round passes the current scores along the arcs, in $\Theta(n + m)$ time, and the error shrinks by a factor of $\alpha$ each round. It was the first ranking of the Google search engine and is a standard [centrality](/centrality/) measure.

## In plain words

Imagine a person who browses the web without a goal. On each page, they usually click one of its links at random. Now and then they get bored and type the address of a random page instead. Over a long time, they visit some pages much more often than others. The share of time spent on a page is its PageRank.

A page gets a high score when many pages link to it, and more so when those pages have high scores themselves and few other links. The random jumps make sure the walk never gets stuck in a corner of the web.

To compute the scores, start with equal shares. In each round, every page hands its share to the pages it links to, a small part goes to everyone, and the result is the new share. After a few dozen rounds the shares stop changing.

## The problem

The input is a directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, $n \ge 1$, given as a list of $m$ arcs, a damping factor $\alpha$ with $0 \le \alpha < 1$, and a tolerance $\varepsilon > 0$. Arcs have no weights. A repeated arc counts as many times as it appears, and a self-loop $(u, u)$ is an ordinary arc. The graph need not be connected. Let $d^+(u)$ be the out-degree of $u$. A vertex with $d^+(u) = 0$ is *dangling*.

The surfer at $u$ moves as follows. With probability $1 - \alpha$, or if $u$ is dangling, it jumps to a uniformly random vertex. Otherwise it takes one of the $d^+(u)$ out-arcs of $u$, each with the same probability. So the transition probability from $u$ to $v$ is

$$P_{uv} = \begin{cases} \alpha \dfrac{c_{uv}}{d^+(u)} + \dfrac{1 - \alpha}{n} & \text{if } d^+(u) > 0, \\[2mm] \dfrac{1}{n} & \text{if } d^+(u) = 0, \end{cases}$$

where $c_{uv}$ is the number of arcs from $u$ to $v$. The matrix $P$ is the *Google matrix*. The PageRank vector $\pi$ is the unique probability vector with $\pi = \pi P$; written out,

$$\pi_v = \frac{1 - \alpha}{n} + \alpha \sum_{(u, v) \in E} \frac{\pi_u}{d^+(u)} + \frac{\alpha}{n} \sum_{u \text{ dangling}} \pi_u.$$

The output is a vector $x$ with $\|x - \pi\|_1 \le \alpha \varepsilon / (1 - \alpha)$. Ranking the vertices by $x$ is the [link analysis ranking](/link-analysis-ranking/) problem. Two vertices can have exactly the same PageRank (an automorphism of the graph forces it); a ranking must then break the tie by a fixed rule, such as the smaller vertex number, and a computed $x$ can split a true tie by rounding, so scores that differ by less than the error bound should be treated as equal.

## The algorithm

```pseudo id=main
PAGERANK(G, α, ε)
L1  for each v ∈ V do x[v] ← 1/n
L2  repeat
L3      for each v ∈ V do y[v] ← 0
L4      d ← the sum of x[u] over the dangling vertices u
L5      for each arc (u, v) ∈ E do y[v] ← y[v] + x[u] / d⁺(u)
L6      for each v ∈ V do y[v] ← α·y[v] + (α·d + 1 − α) / n
L7      δ ← Σ_v |y[v] − x[v]|
L8      x ← y
L9  until δ < ε
L10 return x
```

One round computes $y = xP$ without building the dense matrix $P$. Line L5 moves the share of each vertex along its arcs. Line L4 collects the share of the dangling vertices, and line L6 spreads it evenly, together with the teleport share $1 - \alpha$. Line L7 measures the change in the $L_1$ norm, and the loop stops when the change is below $\varepsilon$.

## Example

Take $n = 6$, $\alpha = 0.85$, and the 8 arcs $0 \to 1$, $0 \to 2$, $1 \to 2$, $2 \to 0$, $3 \to 2$, $3 \to 4$, $4 \to 3$, $4 \to 5$. Vertex 5 is dangling, and no arc enters vertex 3 or 4 from the group $\{0, 1, 2\}$. The table gives $x$ after some rounds, rounded to 4 places, and the change $\delta$.

| round | $x_0$ | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $\delta$ |
|---|---|---|---|---|---|---|---|
| 0 | 0.1667 | 0.1667 | 0.1667 | 0.1667 | 0.1667 | 0.1667 | |
| 1 | 0.1903 | 0.1194 | 0.3319 | 0.1194 | 0.1194 | 0.1194 | 0.3778 |
| 2 | 0.3241 | 0.1228 | 0.2751 | 0.0927 | 0.0927 | 0.0927 | 0.2743 |
| 3 | 0.2719 | 0.1759 | 0.3196 | 0.0775 | 0.0775 | 0.0775 | 0.1952 |
| 10 | 0.3205 | 0.1686 | 0.3367 | 0.0581 | 0.0581 | 0.0581 | 0.0041 |
| 20 | 0.3201 | 0.1692 | 0.3376 | 0.0577 | 0.0577 | 0.0577 | 0.00002 |

With $\varepsilon = 10^{-10}$ the loop stops after 44 rounds. The exact solution of the linear system is $\pi = (\tfrac{29447}{91988}, \tfrac{31133}{183976}, \tfrac{62107}{183976}, \tfrac{3}{52}, \tfrac{3}{52}, \tfrac{3}{52}) \approx (0.3201, 0.1692, 0.3376, 0.0577, 0.0577, 0.0577)$. Vertex 2 ranks first: it has three in-arcs. Vertex 0 has only one in-arc, but it comes from vertex 2, which gives all of its share to 0, so vertex 0 ranks above vertex 1. The vertices 3, 4 and 5 tie exactly. The share that the group $\{3, 4\}$ sends to 2 never comes back except by teleport, so the walk spends most of its time in $\{0, 1, 2\}$.

## Correctness

Let $S$ be the stochastic matrix of the walk that takes a random out-arc and leaves a dangling vertex to a uniformly random vertex. Then $P = \alpha S + (1 - \alpha) \tfrac{1}{n} \mathbf{1}\mathbf{1}^T$, and the update of lines L3 to L6 maps a probability vector $x$ to $xP = \alpha xS + \tfrac{1 - \alpha}{n} \mathbf{1}^T$, which is again a probability vector. For two probability vectors $x$ and $x'$, the teleport terms cancel, so $\|xP - x'P\|_1 = \alpha \|(x - x')S\|_1 \le \alpha \|x - x'\|_1$. So the map is a contraction of the simplex with factor $\alpha$. By the Banach fixed-point theorem it has exactly one fixed point $\pi$, and $\|x^{(k)} - \pi\|_1 \le 2\alpha^k$. When the loop stops with $\delta < \varepsilon$, the returned vector satisfies $\|x - \pi\|_1 \le \alpha\varepsilon / (1 - \alpha)$. The full proof is in the proof file below. The same fact also follows from the [Perron-Frobenius theorem](/perron-frobenius-theorem/), because $P$ has all entries positive when $\alpha < 1$.

## Complexity

Each round reads each arc once (line L5) and each vertex a constant number of times (lines L3, L4, L6, L7, L8), so it takes $\Theta(n + m)$ time, and $k$ rounds take $\Theta(k(n + m))$. The out-degrees are computed once in $\Theta(n + m)$ time. The extra space is $\Theta(n)$ for the two vectors and the out-degrees.

The number of rounds follows from the contraction. The change satisfies $\delta^{(k)} = \|x^{(k)} - x^{(k-1)}\|_1 \le \alpha^{k-1} \|x^{(1)} - x^{(0)}\|_1 \le 2\alpha^{k-1}$, so for $0 < \alpha < 1$ the loop stops after at most $k = \lceil \log(\varepsilon/2) / \log \alpha \rceil + 1$ rounds. This depends on $\alpha$ and $\varepsilon$ and not on the size of the graph. For $\alpha = 0.85$ and $\varepsilon = 10^{-8}$ the bound is 119 rounds. For $\alpha = 0$ it stops after one round. The second eigenvalue of $P$ is at most $\alpha$ in absolute value for every graph, and on real graphs the observed number of rounds is often lower than the bound, as in the example (44 rounds for $\varepsilon = 10^{-10}$, against a bound of 147).

## Properties

- **Directed and unweighted.** The input is a directed graph. An undirected graph is used as a directed graph with both arcs of each edge; then, for $\alpha$ near 1 and a connected graph without dangling vertices, $\pi_v$ is close to $d(v)/2m$. Weighted PageRank replaces $c_{uv}/d^+(u)$ with $w_{uv} / \sum_x w_{ux}$.
- **A probability vector.** The scores are positive and sum to 1. Each score is at least $(1 - \alpha)/n$.
- **Disconnected graphs are fine.** The teleport makes the chain irreducible and aperiodic for each graph, so no special case is needed.
- **Deterministic.** The algorithm has no random choices. The random surfer is only the interpretation.

## Variants and improvements

- **Personalized PageRank.** Teleport to a fixed distribution $s$ instead of the uniform one. This ranks the vertices by their relevance to the vertices of $s$. See [personalized PageRank](/personalized-pagerank/).
- **Gauss-Seidel and other solvers.** $\pi$ is the solution of the sparse linear system $\pi(I - \alpha S) = \tfrac{1 - \alpha}{n} \mathbf{1}^T$, where $S$ is $P$ for $\alpha = 1$. Gauss-Seidel, Jacobi and Krylov methods solve it, often in fewer rounds than the power method.
- **Monte Carlo.** Start $R$ short random walks at each vertex, each stopping with probability $1 - \alpha$ at each step, and count the visits. This gives an estimate in $O(nR/(1 - \alpha))$ expected time and suits distributed and streaming settings.
- **Adaptive and block methods.** Stop updating the entries that have converged, or exploit the block structure of the web by host.
- **Related rankings.** [HITS](/hits-algorithm/) gives each vertex a hub score and an authority score. [Katz centrality](/katz-centrality/) and [eigenvector centrality](/eigenvector-centrality/) count walks in a similar way, without the division by the out-degree.

## When to use it

Use PageRank to rank the vertices of a large directed graph by global importance when the links are endorsements: web pages, citations, follower graphs. It needs only the arcs, scales linearly per round, and its number of rounds does not grow with the graph. For an undirected graph, it adds little over the degree. For relevance to a query or to a seed set, use personalized PageRank. For a graph where hub pages and authority pages play different roles, HITS fits better.

## Pitfalls

- **Losing the dangling share.** If line L4 is left out, the share of the dangling vertices leaves the system, the vector sums to less than 1, and the scores are wrong, not only scaled: the loss depends on where the dangling vertices are. Keep line L4 and add $\alpha d / n$ in line L6.
- **Teleporting with probability $\alpha$.** In the formula of Brin and Page, $d = 0.85$ is the probability of following a link. Writing $\alpha \cdot (\text{teleport})$ and $(1 - \alpha) \cdot (\text{arcs})$ in line L6 gives a different vector that is almost uniform.
- **Stopping on a small $\delta$ only.** A small $\delta$ bounds the error by $\alpha\delta/(1 - \alpha)$, which is about $5.7\delta$ for $\alpha = 0.85$ and $99\delta$ for $\alpha = 0.99$. Choose $\varepsilon$ with this factor in mind.
- **$\alpha$ close to 1.** The convergence slows down as $1/\log(1/\alpha)$, and the vector becomes sensitive to small changes in the graph: its condition number grows like $1/(1 - \alpha)$.
- **Treating rank order as exact.** Scores closer than the error bound can swap order between runs with different tolerances. Compare them with a tolerance and break ties by a fixed rule.

## Implementations

## History

Sergey Brin and Lawrence Page introduced PageRank in 1998, in their description of the prototype of the Google search engine at Stanford, together with a technical report by Page, Brin, Motwani and Winograd. The idea of ranking by the scores of the vertices that point to a vertex is older: it is in the eigenvector measures of status and of citation influence in sociology and bibliometrics. Langville and Meyer give a full mathematical treatment of the method and of its variants.

## References
