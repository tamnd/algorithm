---
tag: J6ZPMC
kind: definition
slug: positive-pointwise-mutual-information
name: Positive pointwise mutual information
aliases:
- PPMI
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: PPMI(w, c) = max(PMI(w, c), 0), which drops unreliable negative values and makes a sparse word-context weighting that works well for similarity.
prereqs: [pointwise-mutual-information, word-context-matrix]
see_also: [cosine-similarity, distributional-hypothesis, sparse-matrix, latent-semantic-analysis, singular-value-decomposition, sgns-implicit-factorization-theorem, skip-gram-model, glove]
sources:
  - paper: "John A. Bullinaria and Joseph P. Levy, Extracting semantic representations from word co-occurrence statistics, a computational study, Behavior Research Methods 39(3), 2007, pages 510 to 526"
    title: Bullinaria and Levy 2007
    locator: the comparison of weightings and distance measures for word-context vectors, in which positive PMI with the cosine did best
  - paper: "Omer Levy, Yoav Goldberg and Ido Dagan, Improving distributional similarity with lessons learned from word embeddings, Transactions of the ACL 3, 2015, pages 211 to 225"
    title: Levy, Goldberg and Dagan 2015
    locator: PPMI, shifted PPMI max(PMI - log k, 0), and context distribution smoothing with the exponent 0.75
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: the chapter on vector semantics and embeddings, the section on PPMI and the reason for dropping negative values
---

Positive pointwise mutual information is [PMI](/pointwise-mutual-information/) with every negative value replaced by 0: $\operatorname{PPMI}(w, c) = \max(\operatorname{PMI}(w, c), 0)$. It is the usual weighting of a [word-context matrix](/word-context-matrix/) before the rows are compared as word vectors. The cut keeps the information that a word and a context occur together more often than chance, and drops the claim that they occur together less often, which needs far more data to estimate. It also removes the $-\infty$ of the pairs never seen, so the matrix stays as sparse as the counts. That PPMI with the [cosine](/cosine-similarity/) works well for word similarity is a measurement: Bullinaria and Levy 2007 found it the best of the weightings they compared, and Levy, Goldberg and Dagan 2015 found it competitive with learned embeddings when its settings are tuned.

## Definition

Let $M$ be a word-context matrix with total $N$, row sums $M[w, *]$ and column sums $M[*, c]$. The **PPMI matrix** has the entries

$$ \operatorname{PPMI}(w, c) = \max\Big( \log_2 \frac{M[w, c] \cdot N}{M[w, *] \cdot M[*, c]},\ 0 \Big), $$

with the value 0 when $M[w, c] = 0$. Any base of the logarithm can be used, and the page or paper states it. The base scales every entry by the same factor, so it does not change cosines.

Since the cut is at 0, these facts hold at once.

- $\operatorname{PPMI}(w, c) \ge 0$, and $\operatorname{PPMI}(w, c) = 0$ whenever $M[w, c] = 0$. So the PPMI matrix has no more nonzero entries than $M$.
- All rows are nonnegative vectors, so the cosine of two rows is in $[0, 1]$, and it is 0 exactly when the two words share no context with positive PMI.
- A pair keeps its PMI value when it is positive, so the upper bound of PMI holds: $\operatorname{PPMI}(w, c) \le \min(-\log P(w), -\log P(c))$.

**Context distribution smoothing.** Levy, Goldberg and Dagan 2015 replace $P(c)$ by

$$ P_\alpha(c) = \frac{M[*, c]^\alpha}{\sum_{c'} M[*, c']^\alpha}, \qquad \alpha = 0.75, $$

and use $\max(\log \frac{P(w, c)}{P(w) P_\alpha(c)}, 0)$. Since $\alpha < 1$, rare contexts get a larger probability and frequent contexts a smaller one, which lowers the PMI of rare contexts and raises that of frequent ones. The exponent comes from the sampling distribution of negative samples in word2vec.

**Shifted PPMI.** $\max(\operatorname{PMI}(w, c) - \log k, 0)$ for an integer $k \ge 1$ keeps only the pairs with a ratio above $k$. The shifted PMI matrix is, under some assumptions, the matrix that skip-gram with $k$ negative samples factorizes (see the [factorization theorem](/sgns-implicit-factorization-theorem/)).

## Examples and non-examples

**A small matrix.** The counts, written for this page, with $N = 40$, are cat (pet 4, fur 3, road 0, the 5), dog (5, 2, 1, 6) and car (0, 0, 6, 8). The PMI values in bits are on the [PMI](/pointwise-mutual-information/) page. PPMI keeps the positive ones:

| word | pet | fur | road | the |
| --- | --- | --- | --- | --- |
| cat | 0.5670 | 1.0000 | 0 | 0 |
| dog | 0.6666 | 0.1926 | 0 | 0 |
| car | 0 | 0 | 1.2922 | 0.2666 |

The cosines of the rows, raw counts against PPMI:

| pair | raw counts | PPMI |
| --- | --- | --- |
| cat, dog | 0.9748 | 0.7154 |
| cat, car | 0.5657 | 0 |
| dog, car | 0.6647 | 0 |

With raw counts, "car" looks fairly close to "cat" and "dog", because all three occur often with "the". PPMI gives "the" no weight in the rows of "cat" and "dog", and the animals and the car no longer share anything.

**With smoothing.** With $\alpha = 0.75$, the context probabilities change from $(0.225, 0.125, 0.175, 0.475)$ to about $(0.2368, 0.1524, 0.1961, 0.4147)$ for pet, fur, road and the. The rows become cat $(0.4933, 0.7143, 0, 0.0068)$, dog $(0.5929, 0, 0, 0.0474)$ and car $(0, 0, 1.1278, 0.4624)$. The rare context "fur" loses weight, and "dog" and "fur" drop to 0, while the frequent context "the" gets a small positive weight in all three rows.

**Why negative values are dropped.** Take two words with probability $10^{-6}$ each. If they are independent, they occur together with probability $10^{-12}$, so a corpus must have far more than $10^{12}$ pairs before a count of 0 shows that they avoid each other. In a corpus of usual size, almost all pairs of rare words have the count 0, and a negative or $-\infty$ PMI for them is an artifact of the sample size. This is the heuristic reason for the cut.

**Not: a fix for rare events.** PPMI keeps the high positive PMI of a pair seen once with two rare words. The bias of PMI toward rare events remains, and smoothing or a minimum count is needed for it.

**Not: the absolute value.** $|\operatorname{PMI}|$ would give pairs that avoid each other a large weight, together with the $-\infty$ of the pairs never seen. PPMI gives them 0.

## Related definitions

- **PMI.** [Pointwise mutual information](/pointwise-mutual-information/) is the value before the cut. Its average under the joint distribution is the mutual information, which is at least 0. PPMI values are nonnegative one by one.
- **Word-context matrix.** PPMI is a weighting of the counts of a [word-context matrix](/word-context-matrix/). The choice of window and context changes the counts, and so the PPMI values.
- **Low-rank vectors.** A truncated [singular value decomposition](/singular-value-decomposition/) of the PPMI matrix gives dense vectors, as [latent semantic analysis](/latent-semantic-analysis/) does for a term-document matrix.
- **Learned embeddings.** The [skip-gram model](/skip-gram-model/) and [GloVe](/glove/) learn dense vectors whose dot products approximate a shifted PMI and a log count, so they are close relatives of a factorized PPMI matrix.
- **Sparse storage.** The PPMI matrix has the same zero pattern as the counts or a smaller one, so it is stored as a [sparse matrix](/sparse-matrix/).

## References
