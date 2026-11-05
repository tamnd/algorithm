---
tag: AJD47V
kind: algorithm
slug: hits-algorithm
name: HITS algorithm
aliases:
- hubs and authorities
- Kleinberg's HITS
area: graphs/network-analysis
level: core
summary: Computes mutually reinforcing hub and authority scores via alternating updates.
solves: [link-analysis-ranking]
model: real-ram
complexity:
  vars: {n: the number of nodes, m: the number of arcs, k: the number of iterations}
  time: {worst: Θ(k(n + m)), best: Θ(k(n + m))}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1998
  people: [Jon Kleinberg]
  note: Presented at SODA 1998 and published in the Journal of the ACM in 1999, while Kleinberg was visiting IBM Almaden.
prereqs: [link-analysis-ranking, directed-graph, power-iteration, eigenvector-centrality]
see_also: [pagerank, eigenvector-centrality, personalized-pagerank, katz-centrality, simrank, singular-value-decomposition]
sources:
  - paper: doi:10.1145/324133.324140
    title: Jon M. Kleinberg, Authoritative sources in a hyperlinked environment, Journal of the ACM 46(5), 604 to 632 (1999)
    locator: the construction of the focused subgraph, the operations I and O, the iterative algorithm, and the theorem that the iterates converge to the principal eigenvectors of A^T A and A A^T
  - paper: doi:10.1145/1052934.1052942
    title: Allan Borodin, Gareth O. Roberts, Jeffrey S. Rosenthal and Panayiotis Tsaparas, Link analysis ranking, algorithms, theory, and experiments, ACM Transactions on Internet Technology 5(1), 231 to 297 (2005)
    locator: the sections on HITS, its variants, and its stability
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Reasoning about a Highly Connected World, Cambridge University Press, 2010
    locator: Chapter 14, Link analysis and web search (hubs and authorities, and the spectral analysis of the updates)
  - book: isbn:9780691122021
    title: Amy N. Langville and Carl D. Meyer, Google's PageRank and Beyond, The Science of Search Engine Rankings, Princeton University Press, 2006
    locator: Chapter 11, The HITS method for ranking webpages
---

The HITS algorithm (hyperlink-induced topic search) gives each node of a [directed graph](/directed-graph/) two scores: an **authority** score, high when many good hubs point to the node, and a **hub** score, high when the node points to many good authorities. It starts from all ones and alternates two updates, each a sum over the arcs, with a normalization after each round. This is [power iteration](/power-iteration/) on $A^{\mathsf T} A$, so the scores converge to its principal eigenvector, at a rate set by the gap between its two largest eigenvalues. Each round takes $\Theta(n + m)$ time. It is one of the two classic solutions of [link-analysis ranking](/link-analysis-ranking/), with [PageRank](/pagerank/).

## In plain words

On the web, some pages are good sources on a topic, and some pages are good lists of links to such sources. Call the first kind authorities and the second kind hubs. A good hub points to many good authorities, and a good authority is pointed to by many good hubs.

The algorithm turns this circle into a loop. Give every page a hub score of one. Set each page's authority score to the sum of the hub scores of the pages that link to it. Then set each page's hub score to the sum of the authority scores of the pages it links to. Scale both lists so they stay small, and repeat. After some rounds, the scores stop changing.

## The problem

The input is a directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, $m$ arcs, and adjacency matrix $A$, with $A_{uv} = 1$ when $(u, v) \in E$. Self-loops are allowed and count as one arc. With arc weights $w_{uv} \ge 0$, $A_{uv} = w_{uv}$ and nothing else changes. The graph need not be connected. The output is a pair of vectors $a, h \in \mathbb{R}^n_{\ge 0}$ with Euclidean norm 1 that satisfy, up to the tolerance,

$$\lambda_1\, a = A^{\mathsf T} A\, a, \qquad h = \frac{A a}{\lVert A a \rVert},$$

where $\lambda_1$ is the largest eigenvalue of $A^{\mathsf T} A$. When $\lambda_1$ is a simple eigenvalue this pins $a$ down. When it is repeated, the output is the specific eigenvector that the start of all ones leads to. If $G$ has no arcs, there is nothing to rank and the algorithm returns zero vectors.

## The algorithm

```pseudo id=main
HITS(G, ε, K)
L1  for each v ∈ V do a[v] ← 0; h[v] ← 1
L2  for t ← 1 to K do
L3      for each v ∈ V do a′[v] ← Σ over arcs (u, v) of h[u]        ▷ the I operation
L4      for each u ∈ V do h′[u] ← Σ over arcs (u, v) of a′[v]       ▷ the O operation
L5      if a′ = 0 then return (a′, h′)                          ▷ G has no arcs
L6      a′ ← a′ / ‖a′‖; h′ ← h′ / ‖h′‖                           ▷ Euclidean norm
L7      δ ← ‖a′ − a‖ + ‖h′ − h / ‖h‖‖
L8      a ← a′; h ← h′
L9      if δ ≤ ε then return (a, h)
L10 return (a, h)
```

Lines L3 and L4 are Kleinberg's two operations. Line L3 scans each arc once and adds the hub score of its tail to the authority score of its head. Line L4 scans each arc once and adds the new authority score of its head to the hub score of its tail. So after round $t$, before the scaling, $a' = A^{\mathsf T} h$ and $h' = A a' = A A^{\mathsf T} h$. If $a' \ne 0$ then $h' \ne 0$, because $\lVert h' \rVert \, \lVert h \rVert \ge h^{\mathsf T} A a' = \lVert a' \rVert^2 > 0$, so line L6 never divides by 0. Line L7 measures the change; the first round compares with the start vectors, scaled to norm 1. The loop stops when the change is at most $\varepsilon$ or after $K$ rounds.

## Example

Take the nodes 0 to 4 and the arcs $0 \to 2$, $0 \to 3$, $1 \to 2$, $1 \to 3$, $1 \to 4$, $4 \to 3$. The table gives the vectors of lines L3 and L4 without the scaling of line L6, which changes no ratio.

| round | $a'$ for nodes 0 to 4 | $h'$ for nodes 0 to 4 |
|---|---|---|
| 1 | 0, 0, 2, 3, 1 | 5, 6, 0, 0, 3 |
| 2 | 0, 0, 11, 14, 6 | 25, 31, 0, 0, 14 |
| 3 | 0, 0, 56, 70, 31 | 126, 157, 0, 0, 70 |
| 4 | 0, 0, 283, 353, 157 | 636, 793, 0, 0, 353 |
| limit, norm 1 | 0, 0, 0.591, 0.737, 0.328 | 0.591, 0.737, 0, 0, 0.328 |

Round 1 gives the in-degrees as the first authority scores. Node 3 is the best authority: three hubs point to it, two of them strong. Node 1 is the best hub, since it points to all three authorities. Node 4 is both a weak authority and a weak hub. The eigenvalues of $A^{\mathsf T} A$ are about $5.0489$, $0.6431$, $0.3080$, $0$ and $0$. Their ratio $0.6431/5.0489 \approx 0.127$ means that each round cuts the error by a factor of about 8, and after round 4 the ratios $283 : 353 : 157$ already agree with the limit to three digits.

## Correctness

Let $M = A^{\mathsf T} A$. It is symmetric and positive semidefinite, so $\mathbb{R}^n$ has an orthonormal basis of eigenvectors $e_1, \ldots, e_n$ with eigenvalues $\lambda_1 \ge \cdots \ge \lambda_n \ge 0$. After round $t$, the vector $a$ is $M^{t-1} x_0$ scaled to norm 1, where $x_0 = A^{\mathsf T} \mathbf{1}$ is the vector of in-degrees. Write $P$ for the orthogonal projection onto the eigenspace of $\lambda_1$. The key facts are:

- $P x_0 \ne 0$ when $G$ has an arc. By the Perron-Frobenius theorem for the non-negative matrix $M$, the eigenspace of $\lambda_1$ holds a non-negative eigenvector $w \ne 0$. Since $w = M w / \lambda_1 = A^{\mathsf T}(A w)/\lambda_1$, $w$ is 0 at each node with in-degree 0. So $x_0^{\mathsf T} w = \sum_v \deg^-(v) w_v > 0$.
- $M^{t-1} x_0 = \lambda_1^{t-1} \big(P x_0 + \sum_{i : \lambda_i < \lambda_1} (\lambda_i/\lambda_1)^{t-1} c_i e_i\big)$, and each ratio $\lambda_i/\lambda_1$ is in $[0, 1)$.

So $a \to P x_0 / \lVert P x_0 \rVert$, which is an eigenvector of $\lambda_1$, the error after $t$ rounds is $O((\lambda_2'/\lambda_1)^{t})$ where $\lambda_2'$ is the largest eigenvalue below $\lambda_1$, and $h = A a / \lVert A a \rVert$ at each round. The full proof, with the termination of the loop and the case of no arcs, is in [the proof page](proofs/correctness.md).

## Complexity

- **Time.** Lines L3 and L4 each scan the $m$ arcs once and touch each node once, so each takes $\Theta(n + m)$. Lines L5 to L8 take $\Theta(n)$. One round is $\Theta(n + m)$, and $k$ rounds take $\Theta(k(n + m))$ in the best and in the worst case, where $k \le K$ is the number of rounds run.
- **Rounds.** To get the error below $\varepsilon$ needs about $\log(1/\varepsilon)/\log(\lambda_1/\lambda_2')$ rounds, which grows without bound as the gap closes. Kleinberg reports that about 20 rounds were enough on his focused subgraphs of the web.
- **Space.** The four vectors $a$, $h$, $a'$, $h'$ take $\Theta(n)$ words besides the graph. Line L4 needs the out-arcs of each node and line L3 only needs to scan all arcs, so one arc list serves both.
- **Model.** The cost counts arithmetic on reals, in the [real RAM](/real-ram/). With floating point numbers, the scaling of line L6 keeps the values in range.

## Properties

- **Two scores per node.** Unlike PageRank, a node gets separate scores for pointing and for being pointed to.
- **Query-dependent in its original form.** Kleinberg runs it on a small focused subgraph built for each query, not on the whole web.
- **Deterministic.** The start of all ones makes the output a function of the graph and its numbering; with a repeated $\lambda_1$, it is still determined, but a different start vector could give a different limit.
- **No damping.** Nodes with no in-arcs get authority 0, and nodes with no out-arcs get hub 0, from round 1 on.
- **Linked to the SVD.** The limits $a$ and $h$ are the right and left singular vectors of $A$ for its largest [singular value](/singular-value-decomposition/) $\sqrt{\lambda_1}$, when it is simple.

## Variants and improvements

- **The focused subgraph.** Take the top pages of a text search as the root set, add the pages they link to and some pages that link to them, and drop links inside one host. This is how Kleinberg builds the input graph.
- **Further eigenvectors.** The other eigenvectors of $A^{\mathsf T} A$, with positive and negative parts, split the pages into communities on different meanings of the query.
- **SALSA.** Lempel and Moran divide each vote by the degrees, which makes the scores stationary distributions of random walks and removes the dependence on a single dense block.
- **Weights and normalizations.** Weighted arcs, and normalization by the sum or by the maximum instead of the Euclidean norm. The normalization changes the scale of the scores but not their ratios.

## When to use it

Use HITS when two roles are natural, such as lists of resources and the resources, or reviewers and the items they review, and the graph is small enough to build per query. Use [PageRank](/pagerank/) when a single global score is needed, when the graph has many disconnected parts, or when robustness to small changes matters: its damping makes the answer unique and stable, while the HITS answer can jump when $\lambda_1$ and $\lambda_2$ are close. For undirected graphs, use [eigenvector centrality](/eigenvector-centrality/), which is the one-score analogue.

## Pitfalls

- **Reading the arcs the wrong way.** Line L3 sums over the arcs that *enter* $v$, and line L4 over the arcs that *leave* $u$. Swapping the two directions swaps the roles: the program then returns the hubs as authorities.
- **No normalization.** Without line L6 the values grow like $\lambda_1^{t}$ and overflow after a few hundred rounds on large graphs.
- **Starting from zero hubs or from a bad vector.** A start vector orthogonal to the top eigenspace never reaches it. The start of all ones in line L1 avoids this, as the proof shows.
- **Assuming a unique answer.** When the graph has two separate dense blocks with the same $\lambda_1$, the limit mixes them in proportions set by the start vector. Check the gap, or use a damped variant.
- **Tightly knit communities.** A dense group of pages that all link to each other, such as one site's navigation links, can take all the authority mass, even when it is off the topic. This is why links inside one host are dropped.

## Implementations

## History

Jon Kleinberg introduced hubs and authorities in a paper at the ACM-SIAM Symposium on Discrete Algorithms in 1998, published in full in the Journal of the ACM in 1999. The work was done at the same time as PageRank, and the two papers set out the two main ideas of link analysis for web search. The algorithm was the basis of the Clever project at IBM Almaden. Lempel and Moran proposed SALSA in 2000 and 2001, and Borodin, Roberts, Rosenthal and Tsaparas compared the methods and their stability in 2005.

## References
