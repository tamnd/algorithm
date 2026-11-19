---
tag: HJM1EQ
kind: definition
slug: word-context-matrix
name: Word-context matrix
aliases:
- co-occurrence matrix
- term-context matrix
area: natural-language-and-speech/word-and-sentence-embeddings
level: intro
summary: The matrix whose entry (w, c) counts how often word w occurs near context c in a corpus, the raw material of count-based word vectors.
prereqs: [distributional-hypothesis]
see_also: [pointwise-mutual-information, positive-pointwise-mutual-information, cosine-similarity, sparse-matrix, latent-semantic-analysis, vector-space-model, glove, zipfs-law]
sources:
  - paper: "Peter D. Turney and Patrick Pantel, From frequency to meaning, vector space models of semantics, Journal of Artificial Intelligence Research 37, 2010, pages 141 to 188"
    title: Turney and Pantel 2010
    locator: the term-document, word-context and pair-pattern matrices, and the steps of building, weighting and comparing them
  - paper: "Omer Levy, Yoav Goldberg and Ido Dagan, Improving distributional similarity with lessons learned from word embeddings, Transactions of the ACL 3, 2015, pages 211 to 225"
    title: Levy, Goldberg and Dagan 2015
    locator: the window size and the dynamic context windows that weight a context at distance d by 1/d or by (L - d + 1)/L
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: the chapter on vector semantics and embeddings, the sections on term-document and term-context matrices
---

A word-context matrix has one row per word of a vocabulary and one column per context, and its entry $(w, c)$ counts how often $w$ occurs with $c$ in a corpus. A context is usually a word within a window of $k$ tokens, but it can also be a document or a syntactic relation to another word. The rows are the simplest word vectors of the [distributional hypothesis](/distributional-hypothesis/): two words with similar rows occur in similar contexts. The counts are almost never used as they are. A weighting such as [PPMI](/positive-pointwise-mutual-information/) comes first, and often a low-rank reduction such as [latent semantic analysis](/latent-semantic-analysis/). A page or paper that uses such a matrix should say what a context is, the window size, whether the window is weighted, and whether it crosses sentence boundaries, because each of these changes the similarities.

## Definition

Let a corpus be a list of sentences, each a list of tokens $t_1, \ldots, t_n$, and let $W$ be the vocabulary of target words and $C$ the set of contexts. For **window contexts** with $C = W$ and a window size $k \ge 1$, the entry is

$$ M[w, c] = \sum_{\text{sentences}} \#\{ (i, j) : t_i = w,\ t_j = c,\ 1 \le |i - j| \le k \}. $$

A **weighted window** adds $g(|i - j|)$ for each pair instead of 1, with a weight $g$ that falls with the distance $d$, for example $g(d) = 1/d$, or $g(d) = (k - d + 1)/k$, which is the average weight of the dynamic window of word2vec (Levy, Goldberg and Dagan 2015). An **asymmetric window** counts only $j > i$ or only $j < i$, and a **positional context** keeps the offset, so that "the" at offset $-1$ and "the" at offset $+1$ are different columns. For **document contexts**, $C$ is the set of documents and $M[w, d]$ is the number of occurrences of $w$ in $d$, which gives the term-document matrix of information retrieval. For **syntactic contexts**, a column is a pair (relation, word) from a dependency parse, such as (object of, drink) for "milk".

The total is $N = \sum_{w, c} M[w, c]$, the number of word and context pairs, and the row and column sums are $M[w, *]$ and $M[*, c]$. For an unweighted symmetric window, $M$ is symmetric, and a sentence of $n$ tokens adds $2 \sum_{d=1}^{k} \max(n - d, 0)$ to $N$. The empirical probabilities $P(w, c) = M[w, c] / N$, $P(w) = M[w, *] / N$ and $P(c) = M[*, c] / N$ are the input of [pointwise mutual information](/pointwise-mutual-information/).

## Examples and non-examples

**A window of 1.** Take the five sentences "the cat drinks milk", "the dog drinks water", "a cat eats fish", "a dog eats meat" and "the child drinks milk", with $k = 1$ and no context across sentences. Each sentence of 4 tokens gives 6 pairs, so $N = 30$. Some rows of the $11 \times 11$ matrix, with the columns that are not zero in any of them:

| word | the | a | drinks | eats | cat | dog | child | milk | water | fish | meat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cat | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dog | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| child | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| drinks | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 2 | 1 | 0 | 0 |
| milk | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The rows of "cat" and "dog" are equal, so their cosine is 1. The column of "cat" is the row of "cat", since the window is symmetric. The column sums are the counts of each word as a context: "drinks" has 6, because it occurs three times with a neighbor on each side.

**A window of 2.** With $k = 2$ the same corpus has $2 \cdot (3 + 2) = 10$ pairs per sentence and $N = 50$, and "cat" now also counts "milk" and "fish". A larger window adds pairs that are further apart and more about the topic than about the grammar.

**A term-document matrix.** With the five sentences as documents, the row of "cat" is $(1, 0, 1, 0, 0)$ and the row of "dog" is $(0, 1, 0, 1, 0)$. Their cosine is 0: as documents, the two words never meet, although they have the same neighbors. The choice of context changes which words are similar.

**Not the same matrix: a window across sentences.** If the window runs across sentence boundaries, "milk" at the end of one sentence counts "the" at the start of the next. The result is the word-context matrix of the corpus read as one long sentence, which is a different matrix from the one above, so the definition of a matrix must say which one it is.

**Not: a similarity matrix.** The $V \times V$ matrix of cosines between the rows is computed from a word-context matrix, but its entries are not counts, and it is not one.

**Not: an embedding matrix.** The dense vectors of the [skip-gram model](/skip-gram-model/) or [GloVe](/glove/) are learned from the same counts, but the matrix of these vectors has a few hundred learned columns that are not contexts.

## Related definitions

- **Weightings.** [Pointwise mutual information](/pointwise-mutual-information/) replaces each count by $\log \frac{P(w, c)}{P(w) P(c)}$, and [PPMI](/positive-pointwise-mutual-information/) keeps its positive part. [tf-idf](/tf-idf/) is the usual weighting of a term-document matrix.
- **Sparsity.** By [Zipf's law](/zipfs-law/), most words are rare, and most entries of the matrix are 0. It is stored as a [sparse matrix](/sparse-matrix/) or a hash map of the pairs that occur, and its size is the number of distinct pairs, not $|W| \cdot |C|$.
- **Reduction.** A truncated [singular value decomposition](/singular-value-decomposition/) of the weighted matrix gives dense vectors of a few hundred dimensions. Applied to a term-document matrix this is [latent semantic analysis](/latent-semantic-analysis/).
- **Similarity.** Rows are compared with [cosine similarity](/cosine-similarity/), which does not depend on the length of a row and so not directly on the frequency of the word.
- **Class bigram counts.** [Brown clustering](/brown-clustering/) uses the matrix of an ordered window of size 1, the bigram counts $n(u, w)$, and sums its rows and columns over classes.

## References
