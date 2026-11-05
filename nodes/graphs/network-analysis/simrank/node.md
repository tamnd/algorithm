---
tag: G0C81F
kind: algorithm
slug: simrank
name: SimRank
aliases:
- SimRank similarity
area: graphs/network-analysis
level: advanced
summary: Node similarity defined recursively by similarity of in-neighbours.
solves: [node-similarity]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, K: the number of rounds}
  time: {worst: Θ(K(n^2 + m^2))}
  space: {extra: Θ(n^2)}
properties: {directed: true, weighted: false, deterministic: true, recursive: false}
history:
  year: 2002
  people: [Glen Jeh, Jennifer Widom]
  note: Jeh and Widom defined SimRank at KDD 2002 by the rule that two objects are similar if they are referenced by similar objects.
prereqs: [node-similarity, directed-graph, in-degree-and-out-degree]
see_also: [node-similarity, personalized-pagerank, structural-equivalence, pagerank, link-prediction, katz-centrality, cosine-similarity, weisfeiler-leman]
sources:
  - paper: doi:10.1145/775047.775126
    title: Glen Jeh and Jennifer Widom, SimRank, a measure of structural-context similarity, Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 538 to 543 (2002)
    locator: Section 3 (the recursive definition and the iterative computation), the university example with C = 0.8, and the random surfer-pairs model with expected meeting distance
  - paper: doi:10.14778/1453856.1453904
    title: Dmitry Lizorkin, Pavel Velikhov, Maxim Grinev and Denis Turdakov, Accuracy estimate and optimization techniques for SimRank computation, Proceedings of the VLDB Endowment 1(1), 422 to 433 (2008)
    locator: the bound C^(k+1) on the error after k iterations, and the partial sums technique that reduces the cost of a round
  - paper: doi:10.1145/1060745.1060828
    title: Dániel Fogaras and Balázs Rácz, Scaling link-based similarity search, Proceedings of the 14th International World Wide Web Conference, 641 to 650 (2005)
    locator: the Monte Carlo estimation of SimRank from coupled backward random walks and their first meeting time
---

SimRank is a [node similarity](/node-similarity/) measure for directed graphs built on the rule "two vertices are similar if they are pointed to by similar vertices", with every vertex maximally similar to itself. Jeh and Widom (2002) defined it as the fixed point of a recursive equation and computed it by iterating the equation from the identity matrix, each round averaging the scores of all pairs of in-neighbours and scaling by a decay factor $C < 1$. After $K$ rounds every score is within $C^{K+1}$ of the exact value. SimRank can make two vertices similar even when they have no in-neighbour in common, which the local scores cannot.

## In plain words

Two web pages are probably about the same topic if the pages that link to them are about the same topic. Two papers are probably related if they are cited by related papers. SimRank turns this circular idea into numbers.

Start by saying that every page is similar only to itself. Then, again and again, update the score of each pair of pages: look at all the pages that link to the first one and all the pages that link to the second one, and take the average of their current scores, made a little smaller. The scores grow at each round and settle down quickly. A pair gets a high score when the pages pointing to them are similar, and those are similar when the pages pointing to them are, and so on.

## The problem

The input is a directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given as a list of $m$ arcs, a decay factor $C$ with $0 < C < 1$ (Jeh and Widom used $0.8$), and a number of rounds $K \ge 0$. Let $I(v)$ be the list of in-neighbours of $v$; a repeated arc appears in it as many times as it is repeated, and a self-loop makes $v$ its own in-neighbour. Arcs have no weights. The SimRank matrix $S$ is the solution of

$$S(a, a) = 1, \qquad S(a, b) = \frac{C}{|I(a)|\,|I(b)|} \sum_{i \in I(a)} \sum_{j \in I(b)} S(i, j) \quad (a \ne b),$$

with $S(a, b) = 0$ when $a \ne b$ and $I(a)$ or $I(b)$ is empty. The equations have exactly one solution. The output is an approximation $R$ of $S$ with $S - C^{K+1} \le R \le S$ entrywise.

For an undirected graph, $I(v)$ is the neighbourhood of $v$. The graph need not be connected; a pair has a positive score exactly when there is a length $\ell \ge 1$ and a vertex $w$ with walks of length $\ell$ from $w$ to both $a$ and $b$, so vertices in different weakly connected components score 0. Scores can tie; a ranking by score breaks ties by the vertex number.

## The algorithm

```pseudo id=main
SIMRANK(G, C, K)
L1  for each (a, b) ∈ V × V do R[a, b] ← 1 if a = b, else 0
L2  repeat K times
L3      for each (a, b) ∈ V × V do
L4          if a = b then R'[a, b] ← 1
L5          else if I(a) = ∅ or I(b) = ∅ then R'[a, b] ← 0
L6          else R'[a, b] ← C / (|I(a)|·|I(b)|) · Σ_{i ∈ I(a)} Σ_{j ∈ I(b)} R[i, j]
L7      R ← R'
L8  return R
```

Line L1 starts from the identity: before any evidence, a vertex is similar only to itself. Each round of lines L3 to L6 applies the right-hand side of the SimRank equations to the current matrix, and line L7 replaces the matrix. The new matrix is computed entirely from the old one, so the order of the pairs does not matter. To reach a target error $\varepsilon$, take $K = \lceil \log \varepsilon / \log C \rceil - 1$.

## Example

Jeh and Widom's university graph has the vertices Univ, ProfA, ProfB, StudentA and StudentB, and the arcs Univ → ProfA, Univ → ProfB, ProfA → StudentA, StudentA → Univ, ProfB → StudentB and StudentB → ProfB. So $I(\text{ProfA}) = \{\text{Univ}\}$, $I(\text{ProfB}) = \{\text{Univ}, \text{StudentB}\}$, $I(\text{StudentA}) = \{\text{ProfA}\}$ and $I(\text{StudentB}) = \{\text{ProfB}\}$. Take $C = 0.8$.

- Round 1: $R(\text{ProfA}, \text{ProfB}) = \frac{0.8}{1 \cdot 2}\bigl(R(\text{Univ}, \text{Univ}) + R(\text{Univ}, \text{StudentB})\bigr) = 0.4 \cdot (1 + 0) = 0.4$. Every other pair of distinct vertices stays 0.
- Round 2: $R(\text{StudentA}, \text{StudentB}) = 0.8 \cdot R(\text{ProfA}, \text{ProfB}) = 0.32$.
- Round 3: $R(\text{Univ}, \text{ProfB})$ becomes $0.128$, and round 4 gives $R(\text{ProfA}, \text{StudentB}) = 0.1024$.

The scores keep growing slowly, because each new positive score feeds back into others. The exact solution of the equations has

| pair | exact $S$ | value |
|---|---|---|
| ProfA, ProfB | 6250/15113 | 0.414 |
| StudentA, StudentB | 5000/15113 | 0.331 |
| Univ, ProfB | 2000/15113 | 0.132 |
| ProfA, StudentB | 1600/15113 | 0.106 |
| ProfB, StudentA | 640/15113 | 0.042 |
| Univ, StudentB | 512/15113 | 0.034 |

and the pairs (Univ, ProfA), (Univ, StudentA) and (ProfA, StudentA) score 0. After 10 rounds the largest error is about $0.0014$, well within the bound $0.8^{11} \approx 0.086$. The two professors are the most similar pair, because both are pointed to by Univ, and the two students follow, because their professors are similar, although the students have no in-neighbour in common.

## Correctness

Write $F$ for the map that lines L3 to L6 apply to the matrix. For two matrices $X$ and $Y$, each entry of $F(X) - F(Y)$ off the diagonal is $C$ times an average of entries of $X - Y$, and the other entries are 0, so $\max |F(X) - F(Y)| \le C \max |X - Y|$. So $F$ is a contraction in the max norm, and by the Banach fixed-point theorem it has exactly one fixed point $S$, which is the SimRank matrix, and the rounds converge to it. Since $F$ is monotone and $R_0 \le R_1$, the sequence $R_k$ increases toward $S$. The diagonals agree and $0 \le S(a, b) \le C$ off the diagonal, so $\max |S - R_0| \le C$ and $0 \le S - R_k \le C^{k+1}$ entrywise. The full proof is in the proof file below.

## Complexity

A round visits $n^2$ pairs, and the pair $(a, b)$ costs $O(1 + |I(a)|\,|I(b)|)$. Since $\sum_{a, b} |I(a)|\,|I(b)| = (\sum_a |I(a)|)^2 = m^2$, a round takes $\Theta(n^2 + m^2)$ time, and $K$ rounds take $\Theta(K(n^2 + m^2))$. The two matrices take $\Theta(n^2)$ space. For a dense graph with $m = \Theta(n^2)$ this is $\Theta(K n^4)$, and the quadratic space alone rules out graphs with more than about $10^5$ vertices. The number of rounds for an error $\varepsilon$ is $\lceil \log \varepsilon / \log C \rceil - 1$, independent of the graph: 41 rounds for $\varepsilon = 10^{-4}$ and $C = 0.8$.

## Properties

- **Directed, unweighted.** It uses in-neighbours. Using out-neighbours gives a second measure; the two can be combined, as in the bipartite version of Jeh and Widom for users and items.
- **Symmetric and bounded.** $S(a, b) = S(b, a)$, $S(a, a) = 1$, and $S(a, b) \le C$ for $a \ne b$.
- **Monotone iteration.** Every round only raises scores, so a partial computation never overestimates.
- **Deterministic.** No random choices. The random-walk reading below is only an interpretation.
- **Random surfers.** $S(a, b) = \mathbb E[C^{\tau}]$, where $\tau$ is the first time at which two independent walks, started at $a$ and $b$ and moving backward along arcs to a uniform in-neighbour, are at the same vertex ($C^\infty = 0$).

## Variants and improvements

- **Partial sums.** Store $P_a(j) = \sum_{i \in I(a)} R[i, j]$ once per $a$ and reuse it for every $b$. This cuts the cost of a round to $O(nm)$ (Lizorkin and coauthors).
- **Monte Carlo.** Simulate pairs of backward walks and average $C^{\tau}$, truncated at a fixed length. Fogaras and Rácz use fingerprint trees to answer single-source queries on large graphs.
- **Single-pair and single-source methods.** Linearized forms of the equations and local push methods compute one row of $S$ without the $n^2$ matrix.
- **Matrix form.** With $W$ the column-normalized adjacency matrix, a round sets $R' = C\, W^T R\, W$ off the diagonal and $R' = 1$ on the diagonal. Several papers replace this by the linear equation $S = C\, W^T S\, W + (1 - C) I$, which is easier to compute but defines a different measure.
- **Relatives.** P-Rank combines in-neighbours and out-neighbours; SimRank++ adds weights and evidence factors for query-ad graphs.

## When to use it

Use SimRank when similarity should follow from the similarity of the referrers, not only from shared referrers: citation graphs, user-item graphs, and graphs of web pages, where two items can be related through different but related neighbours. On a small or medium graph, the plain iteration with partial sums is simple and exact up to $C^{K+1}$. On a large graph, use single-source Monte Carlo or push methods. When shared neighbours are enough, the local scores such as Jaccard or Adamic-Adar are far cheaper.

## Pitfalls

- **Quadratic memory.** The full matrix has $n^2$ entries: 80 GB of doubles for $10^5$ vertices. Plan for single-source queries on large graphs.
- **Reading old and new scores in one round.** Updating $R$ in place mixes rounds. It still converges, but the error bound $C^{K+1}$ and the monotone order of the rounds then need a separate argument. Keep two matrices.
- **Forgetting the empty in-neighbourhood.** A vertex with no in-arcs has score 0 with every other vertex; dividing by $|I(a)| = 0$ must be avoided, as in line L5.
- **Walks must have equal length.** The two backward walks move in step, so they can meet only at a vertex that reaches both $a$ and $b$ by walks of the same length. In the path $0 \to 1 \to 2$, the adjacent vertices 1 and 2 score 0: $S(1, 2) = C\, S(0, 1)$, and $S(0, 1) = 0$ because vertex 0 has no in-neighbour. SimRank is not a closeness measure.
- **Large C.** The error bound $C^{K+1}$ decays slowly for $C$ close to 1, so the number of rounds grows like $1/(1 - C)$.

## Implementations

## History

Glen Jeh and Jennifer Widom introduced SimRank at KDD 2002, with the iterative algorithm and the random surfer-pairs model. Fogaras and Rácz (2005) gave scalable Monte Carlo methods, and Lizorkin and coauthors (2008) proved the error bound and introduced partial sums. Many later papers give faster single-source and single-pair algorithms.

## References
