---
tag: FCW45A
kind: algorithm
slug: textrank
name: TextRank
aliases:
- TextRank keyword extraction
area: natural-language-and-speech/text-generation-and-decoding
level: core
summary: Rank sentences or words by weighted PageRank with d = 0.85 on a graph whose edges weigh word overlap or co-occurrence, then extract the top ones. A heuristic with no training.
model: word-ram
complexity:
  vars: {n: the number of sentences, N: the number of tokens, I: the number of iterations}
  time: {expected: "O(n N + I n²)"}
  space: {extra: "O(n²)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2004
  people: [Rada Mihalcea, Paul Tarau]
  note: Mihalcea and Tarau presented TextRank at EMNLP 2004, applying the PageRank idea of ranking web pages to the words and sentences of one text, for keyword extraction and single-document summarization.
prereqs: [pagerank, automatic-summarization]
see_also: [lexrank, luhn-summarization, power-iteration, stationary-distribution, personalized-pagerank, eigenvector-centrality, rouge, maximal-marginal-relevance]
sources:
  - paper: "Rada Mihalcea and Paul Tarau, TextRank: Bringing Order into Texts, EMNLP 2004, pages 404 to 411, ACL Anthology W04-3252"
    title: Mihalcea and Tarau 2004
    locator: "Section 2.2 (the weighted score with d = 0.85), Section 3.1 (keyword extraction, the window, the filter, a third of the vertices, Table 1), Section 4.1 (the sentence similarity), Section 4.2 (DUC 2002, Table 2)"
  - paper: doi:10.1613/jair.1523
    title: Gunes Erkan and Dragomir R. Radev, LexRank, Graph-based Lexical Centrality as Salience in Text Summarization, Journal of Artificial Intelligence Research 22, 2004, pages 457 to 479
    locator: Section 3 (the related method on a cosine similarity graph)
---

TextRank builds a graph from one text and ranks its vertices with a weighted form of [PageRank](/pagerank/). For summarization the vertices are the sentences, and the weight of an edge is the number of words two sentences share, divided by the sum of the logarithms of their lengths. For keyword extraction the vertices are words, joined when they occur close together. The best sentences form an extractive summary, and the best words form the keywords. Rada Mihalcea and Paul Tarau published the method in 2004. The ranking is a fixed point that the iteration finds to any precision; its use as a summarizer is a heuristic whose value is measured.

## In plain words

Think of the sentences of an article as people at a meeting. Two sentences that use the same words "agree" with each other, and the more words they share, the stronger the link. A sentence that many others agree with is probably about the main topic.

TextRank turns this into numbers. Each sentence starts with the score 1. In each round, a sentence collects a share of the scores of the sentences linked to it, in proportion to the link weights, and a fixed amount of 0.15. After some rounds the scores stop changing. The sentences with the highest scores make the summary.

For keywords, the same scoring runs on words. Two nouns or adjectives that stand next to each other are linked, and the words with the highest scores become the keywords.

## The problem

The input is a text split into sentences $S_1, \ldots, S_n$, each a list of tokens, and a number $k$. The similarity of two sentences is

$$w_{ij} = \frac{|\{ v : v \in S_i \text{ and } v \in S_j \}|}{\log |S_i| + \log |S_j|}, \qquad i \ne j,$$

where the numerator counts distinct shared words and $|S_i|$ is the number of tokens. Set $w_{ij} = 0$ where the numerator is 0 or the denominator is not positive, and $w_{ii} = 0$. The graph is undirected, so $w_{ij} = w_{ji}$. Let $\mathrm{out}_j = \sum_k w_{jk}$. The TextRank scores are the solution of

$$WS(i) = (1 - d) + d \sum_{j : w_{ji} > 0} \frac{w_{ji}}{\mathrm{out}_j} WS(j), \qquad i = 1, \ldots, n,$$

with the damping factor $d = 0.85$. The output is the $k$ sentences with the highest scores, in document order. In matrix form, with $M_{ij} = w_{ji} / \mathrm{out}_j$ (and 0 for $\mathrm{out}_j = 0$), the scores solve $(I - dM)\,WS = (1 - d)\mathbf{1}$.

## The algorithm

```pseudo id=main
TEXTRANK(S, d, ε, k)          ▷ S: n sentences; d = 0.85, ε = 0.0001 in the paper
L1  for each pair i ≠ j do w_ij ← shared words / (log |S_i| + log |S_j|), or 0
L2  for each j do out_j ← Σ_k w_jk
L3  for each i do WS(i) ← 1
L4  repeat
L5      for each i do new(i) ← (1 - d) + d · Σ_(j : w_ji > 0) (w_ji / out_j) · WS(j)
L6      δ ← Σ_i |new(i) - WS(i)|
L7      WS ← new
L8  until δ < ε
L9  return the k sentences with the largest WS, in document order
```

Line L1 builds the graph and line L2 the total weight at each vertex. Lines L4 to L8 are the iteration of the weighted PageRank formula of Section 2.2 of the paper, started at 1 as in the paper. Line L6 measures the change in the 1-norm. The paper stops at a threshold of 0.0001 and reports that this takes 20 to 30 rounds. Line L9 sorts by score and breaks ties by the earlier sentence.

**Keywords.** Section 3.1 of the paper runs the same ranking on words. A syntactic filter keeps the candidate words (nouns and adjectives worked best). Two candidates are joined by an unweighted, undirected edge when they occur within a window of $N$ words, with $N$ from 2 to 10 (2 worked best). After the ranking, the top third of the vertices are marked in the text, and runs of adjacent marked words are joined into one keyword, as "Matlab code" in the paper. The paper does not say whether the window counts the words that the filter removed; the code counts positions in the filtered sequence, so window 2 joins two candidates with only non-candidates between them.

## Example

Take four sentences: (1) "the cat sat on the mat", (2) "the dog sat on the log", (3) "a cat and a dog met", (4) "birds fly south". Sentences 1 and 2 share the, sat and on, so $w_{12} = 3 / (2 \ln 6) = 0.837166$. Sentences 1 and 3 share cat, and 2 and 3 share dog, so $w_{13} = w_{23} = 1/(2 \ln 6) = 0.279055$. Sentence 4 shares no word with any other. So $\mathrm{out}_1 = \mathrm{out}_2 = 1.116221$, $\mathrm{out}_3 = 0.558111$, and $\mathrm{out}_4 = 0$.

| round | WS(1) | WS(2) | WS(3) | WS(4) |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1.212500 | 1.212500 | 0.575000 | 0.15 |
| 2 | 1.167344 | 1.167344 | 0.665312 | 0.15 |
| 3 | 1.176939 | 1.176939 | 0.646121 | 0.15 |
| 7 | 1.175261 | 1.175261 | 0.649478 | 0.15 |
| fixed point | 1.175258 | 1.175258 | 0.649485 | 0.15 |

In round 1, sentence 1 gets $0.15 + 0.85 \,(0.75 \cdot 1 + 0.5 \cdot 1) = 1.2125$, since sentence 2 gives three quarters of its weight to sentence 1 and sentence 3 gives half. The fixed point solves $x = 0.15 + 0.85\,(0.75 x + 0.5 y)$ and $y = 0.15 + 0.85 \cdot 0.5 x$, so $x = 0.21375 / 0.181875 = 1.175258$. With $\varepsilon = 0.0001$ the loop stops after 7 rounds. For $k = 2$ the summary is sentences 1 and 2. The isolated sentence 4 keeps $1 - d = 0.15$.

## Correctness

Three facts make the method well defined. These are theorems; the full proofs are in the proofs file.

- **Unique fixed point.** Every column of $M$ sums to 1 (for a vertex with edges) or 0 (for an isolated vertex), so $\|M\|_1 \le 1$, and the map $x \mapsto (1 - d)\mathbf{1} + d M x$ is a contraction with factor $d < 1$ in the 1-norm. By the Banach fixed point theorem it has exactly one fixed point $WS^*$, and the iteration converges to it from any start.
- **Rate and stopping rule.** The error shrinks by the factor $d$ each round, and when line L8 stops with change $\delta$, the error is at most $d\delta / (1 - d)$ in the 1-norm, which is $5.67\,\delta$ for $d = 0.85$.
- **Mass.** If no vertex is isolated, $\sum_i WS^*(i) = n$. An isolated vertex has score $1 - d$.

Whether the high-scoring sentences make a good summary is not a theorem. TextRank does not optimize coverage or redundancy; it is a centrality heuristic, and its quality is measured with [ROUGE](/rouge/).

## Complexity

Line L1 compares all $\binom{n}{2}$ pairs. With a hash set of the words of each sentence, one pair costs $O(|S_i| + |S_j|)$ expected time, so the graph takes $O(n N)$ expected time for $N$ tokens and $O(n^2)$ space. Each round of lines L5 to L7 takes $O(n^2)$ time on the dense matrix, or $O(n + E)$ on a list of the $E$ nonzero edges. To get the error below $\eta$ from a start with error $e_0$ takes $I \le \log(e_0 / \eta) / \log(1/d)$ rounds, about 14.2 rounds per factor of 10 for $d = 0.85$. This is a worst case bound; the example above needed 7 rounds. In total: $O(nN + I n^2)$ time.

## Properties

- **Unsupervised.** It needs no training data and no corpus, only the text.
- **Scale invariance.** The scores depend on the weights only through $w_{ji} / \mathrm{out}_j$, so multiplying every weight by the same constant changes nothing. In particular the base of the logarithm does not matter.
- **Not normalized.** With this form, the scores average 1 over the vertices that have edges; they are not probabilities. The variant with $(1 - d)/n$ in place of $1 - d$ divides every score by $n$, so it gives the same ranking, and scores that sum to 1 when no vertex is isolated.
- **Length.** The logarithms in the denominator damp the advantage of long sentences, but long sentences still share more words and tend to score higher.
- **Redundancy.** Two near copies of the same central sentence both score high, and both can be picked.
- **Undirected graphs worked best.** In the keyword experiments, forward and backward directed graphs gave lower scores than the undirected graph (a measurement).

## Variants and improvements

- **[LexRank](/lexrank/).** Erkan and Radev (2004) published a close method at the same time, with an idf-weighted [cosine similarity](/cosine-similarity/), a threshold on the edges and the stationary distribution of a random walk.
- **Keyword extraction.** The word graph of Section 3.1, with a part of speech filter and the joining of adjacent keywords. On 500 Inspec abstracts with window 2, TextRank had precision 31.2, recall 43.1 and F-measure 36.2, against 25.2, 51.7 and 33.9 for the best supervised system of Hulth (2003) (measurements, in percent).
- **Other similarities.** Later systems replace the word overlap with BM25, with [tf-idf](/tf-idf/) cosine, or with the cosine of [sentence embeddings](/sentence-embedding/).
- **Biased ranking.** With a nonuniform restart vector the ranking becomes [personalized PageRank](/personalized-pagerank/), which can favor sentences near a query or at the start of the text.
- **Redundancy control.** Selecting the sentences one at a time with [maximal marginal relevance](/maximal-marginal-relevance/) avoids near duplicates.

## When to use it

Use TextRank as an unsupervised baseline for extractive summaries or keywords of a single document, when you have no training data. On 567 DUC 2002 news articles with 100-word summaries, it scored 0.4708 in ROUGE unigram recall with no stemming, against 0.4814 for the best of 15 systems and 0.4599 for the baseline of the first sentences (measurements, Table 2). It would rank third in that column. For news with a strong lead structure, compare it with the first sentences of the article before you use it.

## Pitfalls

- **Zero denominator.** Two one-word sentences give $\log 1 + \log 1 = 0$ in line L1. Treat the weight as 0, or drop one-word sentences before you build the graph.
- **Dangling vertex.** A sentence with no shared words has $\mathrm{out}_j = 0$. Line L5 must skip it as a source; dividing by $\mathrm{out}_j$ there fails.
- **Stop words.** If the stop words are kept, "the" and "of" link almost every pair of sentences, and the ranking mostly measures sentence length. Remove them or weight the words.
- **Max-norm and 1-norm.** A stopping test with the largest change per vertex instead of the sum in line L6 stops earlier for large $n$. The error bound above holds for the 1-norm.
- **The meaning of d.** In this formula $d = 0.85$ is the weight of the links, and $1 - d$ is the restart. Some papers on LexRank use $d$ for the restart weight. Check the formula, not only the number.
- **Ties.** Line L9 needs a fixed tie rule; with symmetric sentences, as in the example, two scores can be equal.

## Implementations

## History

PageRank (Brin and Page, 1998) ranked web pages by the stationary distribution of a random surfer. In 2004 two groups applied the same idea to text: Rada Mihalcea and Paul Tarau at EMNLP with TextRank, for keywords and sentences, and Güneş Erkan and Dragomir Radev in JAIR with LexRank, for multi-document summaries. TextRank's keyword method became a standard baseline for unsupervised keyphrase extraction, and graph ranking of sentences remained a common unsupervised baseline in summarization research before neural methods took over.

## References
