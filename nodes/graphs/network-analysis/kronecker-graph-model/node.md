---
tag: V5P81A
kind: model
slug: kronecker-graph-model
name: Kronecker graph model
aliases:
- R-MAT
- stochastic Kronecker graph
area: graphs/network-analysis
level: advanced
summary: Recursive Kronecker product of a small seed matrix that produces realistic graphs.
prereqs: [kronecker-product, adjacency-matrix, degree-distribution, erdos-renyi-model]
see_also: [erdos-renyi-model, stochastic-block-model, chung-lu-model, barabasi-albert-model, scale-free-network, effective-diameter, network-diameter-estimation, maximum-likelihood-estimation]
sources:
  - url: "https://jmlr.org/papers/v11/leskovec10a.html"
    locator: Jure Leskovec, Deepayan Chakrabarti, Jon Kleinberg, Christos Faloutsos and Zoubin Ghahramani, Kronecker graphs, an approach to modeling networks, Journal of Machine Learning Research 11, 985 to 1042 (2010) (the deterministic and stochastic models, the theorems on degrees, eigenvalues, densification and constant diameter, the fast generation by edge dropping, and the KronFit estimator)
  - paper: doi:10.1007/11564126_17
    title: Jure Leskovec, Deepayan Chakrabarti, Jon Kleinberg and Christos Faloutsos, Realistic, mathematically tractable graph generation and evolution, using Kronecker multiplication, Knowledge Discovery in Databases, PKDD 2005, Lecture Notes in Computer Science 3721, 133 to 145 (2005)
    locator: the first version of the model and of its densification and diameter results
  - paper: doi:10.1145/1273496.1273559
    title: Jure Leskovec and Christos Faloutsos, Scalable modeling of real graphs using Kronecker multiplication, Proceedings of the 24th International Conference on Machine Learning (ICML 2007), 497 to 504
    locator: the maximum likelihood fit of the initiator with Metropolis sampling of the vertex permutation, in time linear in the number of edges per step
  - paper: doi:10.1137/1.9781611972740.43
    title: Deepayan Chakrabarti, Yiping Zhan and Christos Faloutsos, R-MAT, a recursive model for graph mining, Proceedings of the 2004 SIAM International Conference on Data Mining, 442 to 446
    locator: the recursive placement of each edge in one of four quadrants with probabilities a, b, c, d
  - paper: doi:10.1002/rsa.20335
    title: Mohammad Mahdian and Ying Xu, Stochastic Kronecker graphs, Random Structures and Algorithms 38(4), 453 to 466 (2011)
    locator: the thresholds for connectivity, for a giant component and for a constant diameter of the stochastic Kronecker graph with a 2 by 2 initiator
  - paper: doi:10.1145/2450142.2450149
    title: C. Seshadhri, Ali Pinar and Tamara G. Kolda, An in-depth analysis of stochastic Kronecker graphs, Journal of the ACM 60(2), article 13 (2013)
    locator: the large fraction of isolated vertices, the oscillating degree distribution, and the noisy variant that smooths it
  - paper: doi:10.1090/S0002-9939-1962-0133816-6
    title: Paul M. Weichsel, The Kronecker product of graphs, Proceedings of the American Mathematical Society 13(1), 47 to 52 (1962)
    locator: the connectivity of the Kronecker product of two connected graphs
  - url: "https://graph500.org/"
    locator: the Graph 500 benchmark specification, which generates its graphs with the Kronecker edge-dropping method, the initiator 0.57, 0.19, 0.19, 0.05 and 16 edges per vertex
---

The Kronecker graph model builds a large graph from a small one by taking the [Kronecker product](/kronecker-product/) of its [adjacency matrix](/adjacency-matrix/) with itself again and again. In the stochastic version, the small matrix holds probabilities, the product gives a probability for every pair of vertices, and each edge appears independently with its probability. The result is self-similar, with communities inside communities, and it has heavy-tailed degrees, a number of edges that grows faster than the number of vertices, and a small diameter, while each of these can be computed from the small matrix. Leskovec, Chakrabarti, Kleinberg, Faloutsos and Ghahramani introduced it in 2005 and fitted it to real networks; its 2 by 2 case with edge dropping is the R-MAT generator of Chakrabarti, Zhan and Faloutsos, and it is the generator of the Graph 500 benchmark.

## The machine

**The deterministic model.** Take a small graph $K_1$ on $N_1$ vertices, given by its $N_1 \times N_1$ adjacency matrix, usually with self-loops. The *$k$-th Kronecker power* is

$$K_k = K_1 \otimes K_1 \otimes \cdots \otimes K_1 \quad (k \text{ factors}),$$

a graph on $N_1^k$ vertices. Number the vertices of $K_k$ by words $u = u_1 u_2 \cdots u_k$ over $\{0, \dots, N_1 - 1\}$. Then $u$ and $v$ are joined in $K_k$ exactly when $u_i$ and $v_i$ are joined in $K_1$ for every position $i$. If $K_1$ has $E_1$ nonzero entries, $K_k$ has $E_1^k$.

**The stochastic model.** Take an *initiator* matrix $P_1$ of size $N_1 \times N_1$ with entries in $[0, 1]$, and let $P_k = P_1^{\otimes k}$. For every ordered pair of vertices, put an arc $u \to v$ independently with probability

$$P_k[u, v] = \prod_{i=1}^{k} P_1[u_i, v_i].$$

For an undirected graph, use a symmetric $P_1$ and draw each unordered pair once. A constant matrix $P_1$ with all entries $p^{1/k}$ gives the directed [Erdős-Rényi graph](/erdos-renyi-model/) $G(n, p)$, loops allowed, with $n = N_1^k$.

**Generating a sample.** Testing all $N_1^{2k}$ pairs takes quadratic time. The usual method drops edges instead. Let $S = \sum_{i,j} P_1[i, j]$, the expected number of arcs being $S^k$. To place one arc, descend $k$ levels: at each level pick a cell $(i, j)$ of $P_1$ with probability $P_1[i, j]/S$, and append $i$ to the word of $u$ and $j$ to that of $v$. The arc lands on $(u, v)$ with probability $P_k[u, v]/S^k$, so dropping $S^k$ arcs puts $P_k[u, v]$ arcs on $(u, v)$ in expectation. Arcs that land on the same pair are merged, which makes the sample differ slightly from the exact model. The time is $O(k)$ per arc, $O(k S^k)$ in all.

**R-MAT.** The R-MAT generator of Chakrabarti, Zhan and Faloutsos is this edge-dropping process with a $2 \times 2$ matrix of probabilities $a, b, c, d$ that sum to 1, often with small random changes of $a, b, c, d$ at each level to break the regularity. The Graph 500 benchmark uses $a = 0.57$, $b = c = 0.19$, $d = 0.05$ and drops 16 arcs per vertex.

**The kind of graph.** The sample is a directed graph, possibly with self-loops, on $N_1^k$ vertices; with a symmetric initiator it is read as undirected. It need not be connected, and for common initiators many vertices are isolated.

## What it counts

**Degrees.** In the stochastic model, the expected out-degree of $u$ factors over the letters of its word. With the row sums $r_j = \sum_l P_1[j, l]$,

$$\mathbb{E}[\deg^{+}(u)] = \sum_{v} \prod_{i=1}^k P_1[u_i, v_i] = \prod_{i=1}^k r_{u_i}.$$

So the expected degree depends only on how many times each letter occurs in $u$. For a $2 \times 2$ initiator with rows summing to $r_0 \ge r_1$, the $\binom{k}{w}$ vertices with $w$ ones have expected degree $r_0^{k - w} r_1^{w}$. The expected degrees form a geometric staircase of $k + 1$ values with binomial multiplicities, which looks like a heavy-tailed law on a log-log plot. The same argument for $K_k$ gives the multinomial degree law of the deterministic model.

**Edges and densification.** The deterministic $K_k$ has $N_k = N_1^k$ vertices and $E_k = E_1^k$ nonzero entries, so

$$E_k = N_k^{a}, \qquad a = \frac{\log E_1}{\log N_1}.$$

The stochastic model has $S^k$ expected arcs, so $a = \log S / \log N_1$. For $1 < a < 2$, the mean degree grows as a power of the size, which is the densification law that Leskovec, Kleinberg and Faloutsos observed in growing real networks.

**Distances.** If $K_1$ has a self-loop at every vertex, then in $K_1 \otimes H$ the vertices $(x, y)$ and $(x', y')$ are adjacent exactly when $x = x'$ or $x \sim x'$ in $K_1$, and $y = y'$ or $y \sim y'$ in $H$. A path in the product projects to a walk in each factor, and two shortest paths of lengths $s \le t$ in the factors combine into a path of length $t$ by waiting on self-loops in the shorter one. So distances in the product are the maximum of the distances in the factors, and $K_k$ has the same diameter as $K_1$ for every $k$.

**Eigenvalues.** The eigenvalues of $A \otimes B$ are the products $\lambda_i \mu_j$ of the eigenvalues of $A$ and $B$. So the spectrum of $K_k$ is the set of products of $k$ eigenvalues of $K_1$, with multinomial multiplicities, and the same holds for the expected matrix $P_k$.

**Fitting.** Given a real graph with $N_1^k$ vertices, KronFit of Leskovec and Faloutsos chooses $P_1$ to maximize the likelihood of the graph. The likelihood depends on a matching of the real vertices to the words, which is sampled by a Metropolis chain over permutations, and the term for the absent edges is approximated by a Taylor expansion, so that one gradient step costs time linear in the number of edges.

## Relation to other models

- **[Erdős-Rényi model](/erdos-renyi-model/).** It is the special case of a constant initiator. A non-constant initiator adds the heavy tail and the self-similar structure.
- **[Stochastic block model](/stochastic-block-model/).** $P_k$ is an $N_1^k \times N_1^k$ matrix of edge probabilities, like a block model where every vertex is its own block, but with only $N_1^2$ free parameters. Each letter of a word acts as one binary or $N_1$-valued attribute, and the multiplicative attribute graph model of Myunghwan Kim and Jure Leskovec generalizes the model in this direction.
- **[Chung-Lu model](/chung-lu-model/).** Both fix expected degrees. In the Chung-Lu model the probability of an edge is the product of the two weights; in the Kronecker model it is the product over positions, which also builds in correlations between the degrees of the endpoints.
- **[Barabási-Albert model](/barabasi-albert-model/).** Both give heavy tails, but preferential attachment grows one vertex at a time with a constant mean degree and a slowly growing diameter, while a Kronecker graph grows by a factor $N_1$ per level, densifies, and keeps its diameter constant or shrinking.
- **[Scale-free networks](/scale-free-network/).** The expected degrees of a Kronecker graph follow a lognormal-like staircase rather than an exact power law; Seshadhri, Pinar and Kolda show that the degree distribution oscillates, and that adding noise to the initiator at each level smooths it.

## Known results in the model

| quantity | result |
|---|---|
| vertices, arcs | $N_1^k$ vertices; $E_1^k$ arcs (deterministic), $S^k$ expected arcs (stochastic) |
| densification | $E = N^{a}$ with $a = \log E_1/\log N_1$, or $\log S/\log N_1$ |
| expected degree of $u$ | $\prod_i r_{u_i}$, the product of the row sums of the letters of $u$ |
| diameter, deterministic, all self-loops | equal to the diameter of $K_1$ for every $k$ (Leskovec and co-authors) |
| connectivity, $2 \times 2$ initiator $\alpha \ge \beta \ge \gamma$ | connected with high probability exactly when $\beta + \gamma > 1$, apart from a degenerate case (Mahdian and Xu) |
| giant component, same setting | exists with high probability exactly when $(\alpha + \beta)(\beta + \gamma) > 1$ (Mahdian and Xu) |
| diameter, same setting, $\beta + \gamma > 1$ | bounded by a constant with high probability (Mahdian and Xu) |
| isolated vertices | a large fraction for the initiators used in practice, such as that of Graph 500 (Seshadhri, Pinar and Kolda) |
| connectivity of $K_1 \otimes K_1'$ without self-loops | connected exactly when both factors are connected and one of them is not bipartite (Weichsel) |

The thresholds of Mahdian and Xu match the expected degrees above, with $r_0 = \alpha + \beta$ and $r_1 = \beta + \gamma$: the vertex $11\cdots1$ has expected degree $(\beta + \gamma)^k$, which tends to 0 when $\beta + \gamma < 1$, so it is likely isolated, and a typical vertex has about $k/2$ ones and expected degree about $\bigl((\alpha + \beta)(\beta + \gamma)\bigr)^{k/2}$, which tends to infinity exactly when the product exceeds 1.

**A deterministic example.** Let $K_1$ be the path on 3 vertices with a self-loop at each, centre 0:

$$K_1 = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 1 & 0 \\ 1 & 0 & 1 \end{pmatrix}, \qquad N_1 = 3,\ E_1 = 7.$$

| $k$ | vertices | nonzero entries | diameter | row sums (degrees with loop) |
|---|---|---|---|---|
| 1 | 3 | 7 | 2 | 3, 2 |
| 2 | 9 | 49 | 2 | 9, 6, 4 |
| 3 | 27 | 343 | 2 | 27, 18, 12, 8 |

The densification exponent is $\log 7/\log 3 \approx 1.77$. In $K_3$, the $\binom{3}{w} 2^{w}$ words with $w$ letters other than 0 have row sum $3^{3-w} 2^{w}$, so there are 1, 6, 12 and 8 vertices with row sums 27, 18, 12 and 8.

**A stochastic example.** Let $P_1 = \begin{pmatrix} 0.9 & 0.5 \\ 0.5 & 0.1 \end{pmatrix}$, so $S = 2$ and the row sums are $1.4$ and $0.6$. For $k = 2$, with the words $00, 01, 10, 11$,

$$P_2 = \begin{pmatrix} 0.81 & 0.45 & 0.45 & 0.25 \\ 0.45 & 0.09 & 0.25 & 0.05 \\ 0.45 & 0.25 & 0.09 & 0.05 \\ 0.25 & 0.05 & 0.05 & 0.01 \end{pmatrix},$$

with row sums $1.96 = 1.4^2$, $0.84 = 1.4 \cdot 0.6$ twice, and $0.36 = 0.6^2$, and $S^2 = 4$ expected arcs in all. Here $\beta + \gamma = 0.6 < 1$, so as $k$ grows, the vertices with many ones become isolated.

## References
