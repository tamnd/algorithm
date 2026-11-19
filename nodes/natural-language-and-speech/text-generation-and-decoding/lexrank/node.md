---
tag: EFQYD8
kind: algorithm
slug: lexrank
name: LexRank
aliases:
- lexical PageRank summarization
area: natural-language-and-speech/text-generation-and-decoding
level: core
summary: Score sentences by the stationary distribution of a random walk on a graph of idf-weighted cosine similarities above a threshold (0.1), with random jumps, found by the power method.
model: word-ram
complexity:
  vars: {n: the number of sentences, N: the number of tokens, I: the number of power method steps}
  time: {expected: "O(n N + I n²)"}
  space: {extra: "O(n²)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2004
  people: [Güneş Erkan, Dragomir R. Radev]
  note: Erkan and Radev at the University of Michigan published LexRank in the Journal of Artificial Intelligence Research in 2004. A MEAD system with LexRank placed first in more than one task of DUC 2004.
prereqs: [pagerank, tf-idf, cosine-similarity, power-iteration]
see_also: [textrank, stationary-distribution, markov-chain, perron-frobenius-theorem, eigenvector-centrality, automatic-summarization, rouge, maximal-marginal-relevance]
sources:
  - paper: doi:10.1613/jair.1523
    title: Gunes Erkan and Dragomir R. Radev, LexRank, Graph-based Lexical Centrality as Salience in Text Summarization, Journal of Artificial Intelligence Research 22, 2004, pages 457 to 479
    locator: "equation 2 (the idf-modified cosine), Section 3.1 (degree centrality), Section 3.2 (the stationary distribution, equations 8 and 9, Algorithms 2 and 3), Section 3.3 (continuous LexRank), Section 5.1 (the thresholds 0.1 to 0.4)"
  - paper: "Rada Mihalcea and Paul Tarau, TextRank: Bringing Order into Texts, EMNLP 2004, pages 404 to 411, ACL Anthology W04-3252"
    title: Mihalcea and Tarau 2004
    locator: Section 4 (the related method with a word overlap similarity)
---

LexRank scores the sentences of a document or of a cluster of documents by their centrality in a similarity graph. Two sentences are joined when the cosine of their tf-idf vectors is above a threshold. A random walk on this graph, with a small chance of jumping to a random sentence at each step, has a unique stationary distribution, and the probability of each sentence in it is its LexRank score. The power method computes it. Güneş Erkan and Dragomir Radev published the method in 2004 as the graph form of [eigenvector centrality](/eigenvector-centrality/), the idea behind [PageRank](/pagerank/). The scores are exact up to the stopping tolerance; their use for picking summary sentences is a heuristic.

## In plain words

In a set of news stories about one event, the sentences about the main facts are repeated in many forms. LexRank links two sentences when they use enough of the same informative words. A sentence linked to many other sentences is central, and its score should be high.

Counting links alone gives a vote to every sentence, even to one that only links to unimportant sentences. LexRank instead lets each sentence pass its score to its neighbors, in equal parts, over and over. A sentence is then important when important sentences link to it. A small share of the score is spread over all sentences in each round, so that the result is unique.

The process stops when the scores no longer change. The scores add up to 1. The top sentences form the summary.

## The problem

The input is a set of sentences $S_1, \ldots, S_n$, an idf table, a threshold $t$ and a jump probability $d$. For a word $w$ and a sentence $x$, let $\mathrm{tf}_{w,x}$ be the number of times $w$ occurs in $x$. The idf-modified cosine (equation 2 of the paper) is

$$\cos(x, y) = \frac{\sum_{w} \mathrm{tf}_{w,x}\, \mathrm{tf}_{w,y}\, \mathrm{idf}_w^2}{\sqrt{\sum_{w} (\mathrm{tf}_{w,x}\, \mathrm{idf}_w)^2}\ \sqrt{\sum_{w} (\mathrm{tf}_{w,y}\, \mathrm{idf}_w)^2}},$$

with $\mathrm{idf}_w = \log(N / n_w)$ for a collection of $N$ documents of which $n_w$ contain $w$. The adjacency matrix has $A_{ij} = 1$ if $\cos(S_i, S_j) > t$ and 0 otherwise, and $A_{ii} = 1$. The matrix $B$ divides each row of $A$ by its sum, the degree. LexRank is the probability vector $p$ with

$$p = \Bigl[\frac{d}{n} U + (1 - d) B\Bigr]^{\mathsf T} p, \qquad \sum_i p_i = 1,$$

where $U$ is the $n \times n$ matrix of ones (equation 9 of the paper). In continuous LexRank (Section 3.3), $A_{ij} = \cos(S_i, S_j)$ instead. The output is the $k$ sentences with the highest $p_i$.

## The algorithm

```pseudo id=main
LEXRANK(S, idf, t, d, ε)       ▷ S: n sentences; t = 0.1; d: jump probability
L1  for i ← 1 to n do for j ← 1 to n do
L2      c_ij ← idf-modified cosine of S_i and S_j
L3      A_ij ← 1 if i = j or c_ij > t, else 0      ▷ continuous: A_ij ← c_ij
L4  for each i do deg_i ← Σ_j A_ij; B_ij ← A_ij / deg_i for each j
L5  p ← (1/n, ..., 1/n)
L6  repeat
L7      q_j ← d / n + (1 - d) Σ_i B_ij p_i for each j
L8      δ ← Σ_j |q_j - p_j|; p ← q
L9  until δ < ε
L10 return p
```

Lines L1 to L4 are Algorithm 3 of the paper, and lines L5 to L10 are its power method, Algorithm 2, applied to the matrix with random jumps. Line L3 keeps the self loop: the cosine of a sentence with itself is 1, so every degree is at least 1 and line L4 never divides by 0. Line L7 is one step of the random walk: with probability $1 - d$ it follows an edge of the current sentence, chosen uniformly (or in proportion to the weights in the continuous form), and with probability $d$ it jumps to any sentence. The paper reports experiments with $t$ from 0.1 to 0.4 and finds 0.1 best.

## Example

Four sentences: (1) "the storm hit the coast", (2) "the storm flooded the coast roads", (3) "flooded roads closed schools", (4) "schools reopened after the storm". The idf comes from these four sentences: $\log(4/3) = 0.2877$ for "the" and "storm", $\log 2 = 0.6931$ for "coast", "roads", "flooded" and "schools", and $\log 4 = 1.3863$ for the rest. The cosines are

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 1 | 0.3912 | 0 | 0.0698 |
| 2 | 0.3912 | 1 | 0.3847 | 0.0860 |
| 3 | 0 | 0.3847 | 1 | 0.1236 |
| 4 | 0.0698 | 0.0860 | 0.1236 | 1 |

With $t = 0.1$ the graph is the path 1 - 2 - 3 - 4 with self loops, so the degrees are 2, 3, 3, 2, and the rows of $B$ are $(\frac12, \frac12, 0, 0)$, $(\frac13, \frac13, \frac13, 0)$, $(0, \frac13, \frac13, \frac13)$ and $(0, 0, \frac12, \frac12)$. With $d = 0.15$:

| step | $p_1$ | $p_2$ | $p_3$ | $p_4$ |
|---|---|---|---|---|
| 0 | 0.25 | 0.25 | 0.25 | 0.25 |
| 1 | 0.214583 | 0.285417 | 0.285417 | 0.214583 |
| 2 | 0.209566 | 0.290434 | 0.290434 | 0.209566 |
| 3 | 0.208855 | 0.291145 | 0.291145 | 0.208855 |
| limit | 43/206 = 0.208738 | 30/103 = 0.291262 | 30/103 | 43/206 |

By symmetry the limit is $(x, y, y, x)$ with $2x + 2y = 1$ and $x = 0.0375 + 0.85\,(x/2 + y/3)$, which gives $x = 43/206$. Without jumps ($d = 0$) the limit is the degree vector over its sum, $(0.2, 0.3, 0.3, 0.2)$. Sentences 2 and 3 tie; with $k = 1$ the tie rule picks sentence 2. Continuous LexRank breaks the tie: it gives $(0.2387, 0.2905, 0.2452, 0.2255)$.

## Correctness

The matrix $M = \frac{d}{n} U + (1 - d) B$ is row stochastic, and for $d > 0$ all its entries are positive. So the Markov chain is irreducible and aperiodic, and by the [Perron-Frobenius theorem](/perron-frobenius-theorem/) it has exactly one [stationary distribution](/stationary-distribution/); the paper uses this argument. The convergence of the power method has a short direct proof: each step keeps the sum of $p$ equal to 1, and the difference to the limit is multiplied by $(1 - d)B^{\mathsf T}$, whose 1-norm is at most $1 - d$. So the error falls at least by the factor $1 - d$ per step, and when line L9 stops with change $\delta$, the error is at most $(1 - d)\delta / d$. For a symmetric $A$ and $d = 0$, the degree vector divided by its sum is stationary, which ties LexRank to degree centrality (Section 3.1 of the paper). These are theorems; the full proofs are in the proofs file.

That the most central sentences make a good summary is a heuristic. The paper measures it with ROUGE on DUC data.

## Complexity

Line L2 needs the tf vectors of the sentences, built in $O(N)$ expected time with hash tables. One cosine takes $O(|S_i| + |S_j|)$ expected time, so all pairs take $O(nN)$ time, and the matrices take $O(n^2)$ space. Each power step costs $O(n^2)$ on the dense matrix, or $O(n + E)$ with the $E$ edges of the threshold graph, since the jump term adds the same $d/n$ to every entry. Reaching error $\eta$ takes at most $\log(2/\eta) / \log(1/(1 - d))$ steps, about 14 steps per factor of 10 for $d = 0.15$. In total: $O(nN + I n^2)$ time.

## Properties

- **A probability vector.** The scores are positive and sum to 1 (a theorem), so scores from clusters of different sizes are not comparable without rescaling. The paper prints them divided by the largest score.
- **Depends on the threshold.** A high threshold removes most edges, and the scores tend to $1/n$. The paper measured that 0.1 gave the best ROUGE-1 among 0.1, 0.2, 0.3 and 0.4 on DUC 2004 Task 2.
- **Isolated sentences.** A sentence with no edge except its self loop passes all its mass back to itself, so $p_i = d/n + (1 - d)p_i$ and $p_i = 1/n$ exactly. In a small graph this can be more than a connected sentence gets: add "the council met on friday" as a fifth sentence to a similar set of storm sentences, and it can outscore the end sentences of a path.
- **Symmetric similarity.** The graph is undirected. With $d = 0$ and a connected graph, LexRank equals degree centrality; the jumps make it differ.
- **Idf from a corpus.** The paper takes the idf from a large corpus. Computing it from the input sentences, as in the example, gives 0 to a word that occurs in every sentence.

## Variants and improvements

- **Degree centrality.** The degree of each sentence in the threshold graph, which is the $d = 0$ case on a connected graph. The paper compares it with LexRank.
- **Continuous LexRank.** The weights are the cosines themselves, with no threshold (Section 3.3). The paper reports that thresholded LexRank did better than continuous LexRank in its experiments (a measurement).
- **[TextRank](/textrank/).** The same year, Mihalcea and Tarau used a word overlap similarity and the unnormalized PageRank formula.
- **Within MEAD.** In the paper, LexRank is one feature in the MEAD system, combined with the position and length of the sentence, and followed by a reranker that removes redundant sentences. Without a reranker, two near copies of a central sentence both rank high.
- **Biased LexRank.** A jump vector that favors sentences similar to a query gives query-focused summaries, as in [personalized PageRank](/personalized-pagerank/).

## When to use it

Use LexRank for unsupervised extractive summaries of a cluster of related documents, where a sentence repeated in many forms is likely to be important. Combine it with a redundancy step such as [maximal marginal relevance](/maximal-marginal-relevance/), and with sentence position for news. Compute the idf from a corpus in the same domain. For a single short document, the graph is small and the scores are close to uniform, so the method has little to work with.

## Pitfalls

- **Two meanings of d.** In equation 8 of the paper, $d$ is the jump probability and is "typically chosen in the interval [0.1, 0.2]". Its Table 2 says "setting the damping factor to 0.85", which uses the other convention, where 0.85 is the probability of following a link. Writing $d = 0.85$ into line L7 gives a walk that jumps 85 percent of the time, and scores close to uniform.
- **No self loop.** If line L3 drops the diagonal, a sentence with no edge has degree 0, and line L4 divides by 0.
- **Threshold at or above 1.** A test $c_{ij} > t$ for the diagonal too would remove every self loop when $t \ge 1$. Line L3 keeps $i = j$ separate.
- **Column or row.** $B$ is row stochastic, and line L7 sums over the rows $i$. Using $B$ in place of $B^{\mathsf T}$ computes another vector, which is not a distribution.
- **Plain cosine.** The cosine of the raw counts gives stop words most of the weight. Use the idf weights of equation 2.
- **Stopping too early.** Two scores closer than the error bound can come out in the wrong order. Use a small $\varepsilon$, or check ties.

## Implementations

## History

Erkan and Radev built LexRank on the PageRank work of Brin and Page (1998) and on the centroid method of the MEAD summarizer of Radev and colleagues. They showed that degree and eigenvector centrality on a cosine graph pick better sentences than the centroid method on DUC 2003 and DUC 2004 data. A version called LexPageRank appeared at EMNLP 2004, at the same conference as TextRank, and the full article appeared in JAIR the same year. LexRank became a standard unsupervised baseline for multi-document summarization.

## References
