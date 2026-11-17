---
tag: 35D89N
kind: algorithm
slug: isorank
name: IsoRank
aliases:
- IsoRank network alignment
area: biology/systems-biology
level: advanced
summary: Score every pair of proteins from two networks by a PageRank-like fixed point that mixes sequence similarity with the scores of neighbor pairs, then match greedily.
solves: [biological-network-alignment]
model: real-ram
complexity:
  vars: {n: the number of nodes of the first network, m: the number of nodes of the second network, e: the number of edges of the first network, f: the number of edges of the second network, T: the number of iterations}
  time: {worst: O(T (e m + n f) + n m log(n m))}
  space: {extra: Θ(n m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [Rohit Singh, Jinbo Xu, Bonnie Berger]
  note: Singh, Xu and Berger presented IsoRank at RECOMB 2007 and published the version for several networks in PNAS in 2008.
prereqs: [biological-network-alignment, pagerank, personalized-pagerank, power-iteration]
see_also: [maximum-weight-matching, bipartite-matching, hungarian-algorithm, greedy-algorithm, perron-frobenius-theorem, quadratic-assignment-problem, graph-isomorphism-problem, markov-chain]
sources:
  - paper: doi:10.1073/pnas.0806627105
    title: Rohit Singh, Jinbo Xu and Bonnie Berger, Global alignment of multiple protein interaction networks with application to functional orthology detection, PNAS 105(35), 12763-12768, 2008
    locator: the eigenvalue equation R = αAR + (1-α)E, the choice α = 0.6, the power method, the extraction of the alignment and the multiple alignment step
  - paper: doi:10.1007/978-3-540-71681-5_2
    title: Rohit Singh, Jinbo Xu and Bonnie Berger, Pairwise global alignment of protein interaction networks by matching neighborhood topology, RECOMB 2007, LNCS 4453, 16-31, 2007
    locator: the first description of IsoRank and the global alignment of the yeast and fly networks
  - paper: doi:10.1093/bioinformatics/btp203
    title: Chung-Shou Liao, Kanghao Lu, Michael Baym, Rohit Singh and Bonnie Berger, IsoRankN, spectral methods for global alignment of multiple protein networks, Bioinformatics 25(12), i253-i258, 2009
    locator: the multiple alignment by spectral clustering of the pairwise scores
  - paper: doi:10.1002/net.3230130404
    title: David Avis, A survey of heuristics for the weighted matching problem, Networks 13(4), 475-493, 1983
    locator: the greedy heuristic for weighted matching and its worst case ratio
  - paper: doi:10.1098/rsif.2010.0063
    title: Oleksii Kuchaiev, Tijana Milenković, Vesna Memišević, Wayne Hayes and Nataša Pržulj, Topological network alignment uncovers biological function and phylogeny, Journal of the Royal Society Interface 7(50), 1341-1354, 2010
    locator: GRAAL, an aligner that uses topology only, and its comparison with IsoRank
---

IsoRank aligns two protein interaction networks. It gives every pair $(i, j)$, with $i$ a protein of the first network and $j$ a protein of the second, a score $R_{ij}$ that is high when $i$ and $j$ have similar sequences and when their neighbors have high scores too. The scores are the solution of one linear fixed point equation, which is a [personalized PageRank](/personalized-pagerank/) on the product of the two networks, and the power method finds it in a few dozen steps. A matching on the scores then gives a one-to-one map from proteins of one network to proteins of the other. IsoRank is a heuristic for [biological network alignment](/biological-network-alignment/), which is NP-hard in its usual forms; the scores have exact properties, but the alignment has no guarantee of optimality for any alignment score.

## In plain words

Two proteins from two species are a good match if their sequences are alike and if the proteins they touch are good matches too. That second part refers back to itself, so the scores are found by repeating one update until they settle.

Start with the sequence scores. In each round, give every pair a share of the scores of all pairs of its neighbors, and mix in a fixed part of its own sequence score. A pair whose neighbors are well matched gains, and a pair with no matched neighbors keeps only its sequence part. After enough rounds the scores stop changing. Then take the best pair, remove its two proteins, take the best pair of what is left, and so on.

## The problem

**Input.** Two undirected graphs $G_1 = (V_1, E_1)$ with $n$ nodes and $e$ edges and $G_2 = (V_2, E_2)$ with $m$ nodes and $f$ edges; a non-negative $n \times m$ matrix $B$ of sequence similarity scores, for example BLAST bit scores; and a weight $\alpha \in [0, 1)$ of the network part.

**Output.** A score matrix $R \in \mathbb{R}^{n \times m}$ and a one-to-one partial map from $V_1$ to $V_2$.

Write $N(u)$ for the set of neighbors of $u$ and $E = B / \sum_{i, j} B_{ij}$, so the entries of $E$ add up to 1. Define the $nm \times nm$ matrix

$$A_{(i, j), (u, v)} = \begin{cases} \dfrac{1}{|N(u)| \, |N(v)|} & \text{if } u \in N(i) \text{ and } v \in N(j), \\ 0 & \text{otherwise.} \end{cases}$$

IsoRank asks for the $R$ with

$$R = \alpha A R + (1 - \alpha) E,$$

where $R$ and $E$ are read as vectors of length $nm$. With $\alpha = 0$ the scores are the sequence scores, and with $\alpha$ near 1 they depend mostly on the topology. Singh, Xu and Berger used $\alpha = 0.6$.

## The algorithm

```pseudo id=main
ISORANK(G1, G2, B, α, ε)
L1  E ← B / (sum of all entries of B)
L2  R ← E
L3  repeat
L4      for each pair (i, j) do R'[i, j] ← α · Σ_{u ∈ N(i)} Σ_{v ∈ N(j)} R[u, v] / (|N(u)| |N(v)|) + (1 - α) · E[i, j]
L5      δ ← Σ |R'[i, j] - R[i, j]|;  R ← R'
L6  until δ ≤ ε
L7  M ← ∅; for each pair (i, j) by decreasing R[i, j] do if neither i nor j is in a pair of M then add (i, j) to M
L8  return M, R
```

Line L4 is one step of the power method. Computed as written, it costs $O(\sum_{i, j} |N(i)| |N(j)|) = O(e f)$. The code computes it in two passes instead: first $S_{uv} = R_{uv} / (|N(u)| |N(v)|)$, then $P_{iv} = \sum_{u \in N(i)} S_{uv}$ for every $i$ and $v$, which costs $O(e m)$, and then $\sum_{v \in N(j)} P_{iv}$ for every $i$ and $j$, which costs $O(n f)$. A pair with an isolated node sends no score to other pairs. Line L7 is the greedy matching of the figure of the paper. In its case study of the yeast and fly networks, the paper uses a maximum weight bipartite matching instead.

## Example

Let $G_1$ be the path a - b - c and $G_2$ the star with center x and leaves y, z and w. Give no sequence information, so $B$ is all ones and every entry of $E$ is $1/12$, and take $\alpha = 0.6$. By the symmetry of the two graphs there are four distinct scores: $R_{bx}$ (center with center), $R_{b\ell}$ (center b with a leaf), $R_{ex}$ (an end a or c with the center x) and $R_{e\ell}$ (an end with a leaf). Write $c = (1 - \alpha)/12 = 1/30$. The neighbors of b are the two ends, of degree 1, and the neighbors of x are the three leaves, of degree 1, so line L4 gives

$$R_{bx} = 6 \alpha R_{e\ell} + c, \quad R_{e\ell} = \frac{\alpha}{2 \cdot 3} R_{bx} + c, \quad R_{b\ell} = \frac{2 \alpha}{3} R_{ex} + c, \quad R_{ex} = \frac{3 \alpha}{2} R_{b\ell} + c.$$

Substituting the second equation in the first gives $R_{bx} (1 - \alpha^2) = c (1 + 6 \alpha)$, so $R_{bx} = \frac{1}{30} \cdot \frac{4.6}{0.64} = \frac{23}{96} \approx 0.2396$ and $R_{e\ell} = \frac{11}{192} \approx 0.0573$. In the same way $R_{b\ell} = c (1 + 2\alpha/3) / (1 - \alpha^2) = \frac{7}{96} \approx 0.0729$ and $R_{ex} = \frac{19}{192} \approx 0.0990$. The 12 scores add up to 1. The power method reaches these values to within $10^{-12}$ in 55 steps. Line L7 takes (b, x) first, with the largest score. All pairs of an end and a leaf then tie at $11/192$, and the tie rule of the code (smallest pair first) gives (a, y) and then (c, z). The topology alone has matched the two centers.

The test file also checks a second pair of graphs by hand: a triangle with a tail against a triangle, with sequence scores and $\alpha = 0.5$. There the exact rational solution of the linear system and the power method agree to $10^{-10}$, and the greedy step maps the triangle to the triangle and leaves the tail unmatched.

## Correctness

The scores have exact properties; the alignment is a heuristic.

**Theorem.** Let $\alpha \in [0, 1)$. (a) Every column of $A$ adds up to at most 1, and to exactly 1 when the column's pair has no isolated node. (b) The map $F(R) = \alpha A R + (1 - \alpha) E$ satisfies $\lVert F(R) - F(R') \rVert_1 \le \alpha \lVert R - R' \rVert_1$, so it has one fixed point $R^\ast = (1 - \alpha) \sum_{k \ge 0} \alpha^k A^k E = (1 - \alpha)(I - \alpha A)^{-1} E$, which is non-negative, and the iteration of lines L3 to L6 satisfies $\lVert R_t - R^\ast \rVert_1 \le \alpha^t \lVert R_0 - R^\ast \rVert_1$. (c) $R^\ast$ is the personalized PageRank, with restart probability $1 - \alpha$ and restart law $E$, of the random walk on the tensor product graph $G_1 \times G_2$, in which $(i, j)$ and $(u, v)$ are adjacent when $i \sim u$ in $G_1$ and $j \sim v$ in $G_2$. If no node is isolated, the entries of $R^\ast$ add up to 1.

Part (a) holds because column $(u, v)$ has the entry $1/(|N(u)| |N(v)|)$ in the $|N(u)| |N(v)|$ rows $(i, j)$ with $i \in N(u)$ and $j \in N(v)$. Part (b) follows from (a), because the 1-norm of a non-negative matrix acting on vectors is its largest column sum, and from the Banach fixed point theorem; the series converges because $\lVert \alpha A \rVert_1 \le \alpha < 1$. Part (c) holds because the pair $(u, v)$ has degree $|N(u)| |N(v)|$ in the product graph, so $A$ is the transition matrix of the walk on it. The proof file gives the details. The greedy step of line L7 returns a matching whose total score is at least half of the largest total score of any matching (a standard result for the greedy matching, see Avis), and the test checks this against an exhaustive search; but a large total score is not the same as a good alignment for any measure of conserved edges.

## Complexity

The model is the real RAM. Lines L1 and L2 cost $O(n m)$. One step of lines L4 and L5 costs $O(e m + n f + n m)$ with the two passes above, and the number of steps $T$ to reach $\lVert R_t - R^\ast \rVert_1 \le \varepsilon$ is at most $\lceil \ln(2 / \varepsilon) / \ln(1 / \alpha) \rceil$, because $\lVert R_0 - R^\ast \rVert_1 \le 2$ when no node is isolated; for $\alpha = 0.6$ and $\varepsilon = 10^{-12}$ this is 56. Line L7 sorts $n m$ scores in $O(n m \log (n m))$ time. The matrix $R$ and its copy take $\Theta(n m)$ space. For two proteomes with $n$ and $m$ near 10000 and 20000, $R$ has $2 \cdot 10^8$ entries, which is the main cost in practice. $B$ is often sparse, with entries only for pairs with a significant BLAST hit, but $R$ is dense after a few steps.

## Properties

- **Deterministic.** No random draws; ties in line L7 are broken by a fixed order.
- **Linear in the sequence scores.** $R^\ast = (1 - \alpha)(I - \alpha A)^{-1} E$ depends linearly on $E$, so the scores for several sources of similarity are the sums of the scores for each.
- **Symmetric in the two networks.** Swapping $G_1$ and $G_2$ transposes $R$.
- **Topology only when $B$ is constant.** With all sequence scores equal, $R$ depends only on the two graphs, as in the example.
- **A walk interpretation.** $R_{ij}$ is the chance that a walk on the product graph, started at a pair drawn from $E$ and stopped at each step with probability $1 - \alpha$, stops at $(i, j)$.

## Variants and improvements

- **Matching step.** A maximum weight bipartite matching, for example by the [Hungarian algorithm](/hungarian-algorithm/), gives the largest total score, at a higher cost than the greedy step.
- **Several networks.** The PNAS version computes $R$ for every pair of networks and then builds clusters of proteins, one or more per network, by a seed and extend step on the graph of all pairwise scores. IsoRankN (Liao et al. 2009) replaces that step by spectral clustering of the pairwise scores.
- **Other topological scores.** GRAAL (Kuchaiev et al. 2010) uses graphlet degree signatures instead of the eigenvector equation, and needs no sequence scores. Many later aligners optimize an explicit count of conserved edges.
- **Low rank forms.** $A$ is the Kronecker product of the random walk matrices $P_1$ and $P_2$ of the two graphs. So if $E = \sum_r u_r v_r^{\top}$ with $s$ terms, then $A^k E = \sum_r (P_1^k u_r)(P_2^k v_r)^{\top}$, and a truncated series for $R^\ast$ needs only products with each graph separately, in $O(s (e + f))$ time per term, without the $n m$ matrix.

## When to use it

Use IsoRank for a global alignment of two whole networks, for example two protein interaction networks of related species, when there are sequence scores for many pairs and you want a fast method with one parameter. It suits the search for functional orthologs, where a pair of proteins with similar sequences and similar partners is more likely to have the same function. For a local alignment that finds small conserved complexes or pathways, use a local aligner instead. For networks without sequence scores, a method made for topology only, such as GRAAL, is a better choice.

## Pitfalls

- **High degree nodes.** A node with many neighbors spreads its score thinly, and a node with few neighbors passes a lot to each. Hubs can still collect large scores from many pairs, so an alignment can match hubs to hubs whatever their sequences.
- **The choice of $\alpha$.** The alignment changes with $\alpha$, and no value is right for all data. The value 0.6 is the choice of the paper, not a rule.
- **Bipartite graphs.** On bipartite graphs, $A$ has a negative eigenvalue of size 1, so the power method for the eigenvector, with no restart, would oscillate. The restart term $(1 - \alpha) E$ removes this, and the contraction bound still holds.
- **Greedy ties.** With few sequence scores, many pairs tie, and the order of the ties decides the alignment, as in the example.
- **Score matrix size.** $R$ is dense even when $B$ is sparse. Keep only the needed pairs or use a low rank form for large networks.

## Implementations

## History

Singh, Xu and Berger presented IsoRank at RECOMB 2007 and used it to compute a global alignment of the yeast and fly protein interaction networks. In PNAS in 2008 they extended it to several networks and aligned the networks of yeast, fly, worm, mouse and human. Liao, Lu, Baym, Singh and Berger gave IsoRankN in 2009. The equation is the [PageRank](/pagerank/) of Brin and Page applied to the product of two graphs, with the sequence scores as the restart law.

## References
