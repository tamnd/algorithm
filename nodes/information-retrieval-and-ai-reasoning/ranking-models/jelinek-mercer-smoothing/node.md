---
tag: ZBH2C6
kind: technique
slug: jelinek-mercer-smoothing
name: Jelinek-Mercer smoothing
aliases:
- linear interpolation smoothing
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Smooths a document language model by mixing it with the collection model at a fixed weight lambda.
prereqs: [query-likelihood-model]
see_also: [dirichlet-prior-smoothing, relevance-model-rm3, expectation-maximization, maximum-likelihood-estimation, tf-idf, pagerank]
sources:
  - paper: "Frederick Jelinek and Robert L. Mercer, Interpolated estimation of Markov source parameters from sparse data, in E. S. Gelsema and L. N. Kanal (editors), Pattern Recognition in Practice, North-Holland (1980)"
    locator: the interpolation of a sparse estimate with a more general one, with weights estimated on held-out data
  - paper: doi:10.1145/984321.984322
    title: Chengxiang Zhai and John Lafferty, A study of smoothing methods for language models applied to information retrieval, ACM Transactions on Information Systems 22(2) (2004), 179-214
    locator: Jelinek-Mercer smoothing of document models for retrieval, its term weight, and the measured best values of lambda, near 0.1 for title queries and near 0.7 for long queries
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 12, Section 12.2.2 (the linear interpolation of the document model with the collection model, where lambda weights the document side)
---

Jelinek-Mercer smoothing estimates the language model of a document as a fixed mixture of two models: the maximum likelihood model of the document, with weight $1 - \lambda$, and the model of the whole collection, with weight $\lambda$. Every word of the collection then gets a nonzero probability in every document, so the [query likelihood model](/query-likelihood-model/) no longer gives $-\infty$ to a document that lacks one query word. Frederick Jelinek and Robert Mercer introduced the interpolation in 1980 for speech recognition, with weights learned on held-out data. In retrieval, Zhai and Lafferty showed that it gives the query likelihood score an idf-like weight per word, and measured that the best $\lambda$ depends on the length of the queries.

## In plain words

A short document is a small sample of words. If we estimate word chances from it alone, every word that it does not contain gets chance zero, and a query with one such word gets chance zero too. That is too harsh: the document may still be about the topic. So we mix two guesses. One guess is the word chances in the document. The other is the word chances in the whole collection, which are never zero for a word that occurs somewhere. We take a fixed share of each, for example half and half, and add them. Words that the document uses often keep high chances. Missing words get a small chance, the same share of their collection chance in every document. A common word then helps a document less than a rare word, because every document gets much of its chance anyway.

## When it applies

Use it when an estimate from little data must be combined with a broad estimate from much data, and one fixed weight for all cases is good enough. In retrieval this is the document model of the query likelihood model, the mixture of a feedback model with the query model, and the teleport of a random walk. It needs a background model that gives nonzero probability to every event that can occur, here every query word. It is a weaker choice when the right amount of smoothing depends on how much data each case has, such as documents of very different lengths; then [Dirichlet prior smoothing](/dirichlet-prior-smoothing/) adapts the weight to the length.

## The template

```pseudo id=main
JM-SCORE(q, d, λ)
L1  s ← 0
L2  for each word t of q, with count c(t, q):
L3      p_d ← tf(t, d) / |d|                ▷ hole: the sparse estimate
L4      p_C ← cf(t) / |C|                   ▷ hole: the background model, nonzero for every t
L5      s ← s + c(t, q) · log((1 - λ) · p_d + λ · p_C)    ▷ hole: λ, fixed in (0, 1)
L6  return s
```

**The term weight.** For a word $t$ that $d$ lacks, line L5 adds $c(t, q) \log(\lambda \, p(t \mid C))$, which is the same for every document. Subtract this from every term of every document. What is left is a sum over the query words that $d$ contains:

$$\log P(q \mid d) = \sum_{t \in q,\ \mathrm{tf}(t, d) > 0} c(t, q) \log\Bigl(1 + \frac{1 - \lambda}{\lambda} \cdot \frac{\mathrm{tf}(t, d)}{|d| \, p(t \mid C)}\Bigr) + \sum_{t \in q} c(t, q) \log(\lambda \, p(t \mid C)).$$

The second sum is a constant for the query. The weight of a matched word grows with its relative frequency $\mathrm{tf}/|d|$ in the document and falls with its collection probability, as a tf-idf weight does. The coefficient $\alpha_d$ of the [query likelihood](/query-likelihood-model/) form is $\lambda$ for every document, so the length term $|q| \log \alpha_d$ is the same for all documents and has no effect.

**Walk-through on the toy collection.** For q1 = "sorted array search", $p(t \mid C)$ is $5/79$, $3/79$ and $2/79$. Document 1 has 9 tokens and each query word once; document 2 has "sorted" twice and "array" once in 10 tokens. With $\lambda = 0.5$ the factor $(1 - \lambda)/\lambda$ is 1:

| document | sorted | array | search | sum of weights | score |
|---|---|---|---|---|---|
| 1 | 1.0136 | 1.3676 | 1.6843 | 4.0656 | -7.7210 |
| 2 | 1.4255 | 1.2902 | none | 2.7157 | -9.0709 |

The constant is $-11.7866$, the score of documents 3, 5 and 6, which hold no query word. The full scores for three values of $\lambda$:

| document | 1 | 2 | 8 | 7 | 4 | 3, 5, 6 |
|---|---|---|---|---|---|---|
| $\lambda = 0.1$ | -6.7841 | -10.0257 | -10.6855 | -13.0162 | -13.8923 | -16.6149 |
| $\lambda = 0.5$ | -7.7210 | -9.0709 | -9.5486 | -10.1872 | -10.8388 | -11.7866 |
| $\lambda = 0.7$ | -8.3454 | -9.1655 | -9.5046 | -9.7866 | -10.2601 | -10.7772 |

The order $1, 2, 8, 7, 4$ is the same for all three. What changes is the gap. At $\lambda = 0.1$, document 1, the only one with all three words, leads document 2 by 3.24; at $\lambda = 0.7$ the lead is 0.82. A small $\lambda$ rewards documents that hold all the query words, and a large $\lambda$ lets one frequent word count about as much as several words once each.

## Classic examples

- **[Query likelihood model](/query-likelihood-model/).** The document model is mixed with the collection model, as in the template. Zhai and Lafferty measured on TREC collections that short title queries do best with $\lambda$ near 0.1 and long queries with $\lambda$ near 0.7. Their explanation is that long queries hold many common words, and a large $\lambda$ lowers the weight of those words more.
- **[Relevance model](/relevance-model-rm3/).** RM3 mixes the term distribution estimated from feedback documents with the original query model at a fixed weight, and Lavrenko and Croft smoothed the document models inside the relevance model with this interpolation.
- **[PageRank](/pagerank/) and [Markov chain rank aggregation](/markov-chain-rank-aggregation/).** The teleport step mixes the transition distribution of each state with the uniform distribution at a fixed weight. The mixture makes every transition possible, which gives a unique stationary distribution, just as mixing with the collection model makes every word possible.
- **[Rocchio algorithm](/rocchio-algorithm/).** The new query is a fixed linear combination of the old query and the centroids of the judged documents, an interpolation of vectors instead of distributions.

## Variations

- **Deleted interpolation.** Jelinek and Mercer estimated the weights on held-out data, which is an [expectation-maximization](/expectation-maximization/) problem: each held-out word is explained by one of the two models, and the weight is the expected share of words explained by the document model.
- **A weight that depends on the length.** Making $\lambda$ larger for short documents and smaller for long ones gives Dirichlet prior smoothing, where $\lambda_d = \mu/(|d| + \mu)$.
- **Several levels.** Interpolate the document model with a model of its cluster or its topic and then with the collection model, with one weight per level.
- **Two-stage smoothing.** Zhai and Lafferty first smooth the document with a Dirichlet prior and then interpolate the result with a model of the query background, with weights estimated from the data.
- **N-gram models.** In speech and text models, a trigram estimate is mixed with bigram and unigram estimates in the same way, which is the original use.

## Pitfalls

- **The meaning of $\lambda$.** Zhai and Lafferty put $\lambda$ on the collection model, as here; Manning, Raghavan and Schütze put it on the document model. A value of 0.1 means little smoothing in one book and much in the other. State the convention.
- **The ends of the range.** With $\lambda = 0$ there is no smoothing and every document without a query word scores $-\infty$. With $\lambda = 1$ every document has the same model and the same score. Keep $\lambda$ strictly between 0 and 1.
- **Words that the collection lacks.** If $\mathrm{cf}(t) = 0$, line L5 takes the log of 0 for every document. Drop such words from the query, or give the background model a floor.
- **No length correction.** With a fixed $\lambda$, a long document and a short one with the same relative frequency of a word get the same weight, though the estimate from the long document is more reliable. If your collection mixes short and long documents, compare with Dirichlet smoothing.
- **Tuning on the test queries.** The best $\lambda$ depends on the collection and on the kind of query. A value tuned on the test queries makes the results look better than they will be on new queries.

## Exercises

1. Show that the scores of the template and the sum of the matched term weights give the same ranking for every query. *Hint:* the difference is the constant $\sum_{t \in q} c(t, q) \log(\lambda \, p(t \mid C))$.
2. Show that as $\lambda \to 1$, if there are no ties, the ranking tends to the order by $\sum_{t \in q} c(t, q) \, \mathrm{tf}(t, d)/(|d| \, p(t \mid C))$. *Hint:* $\log(1 + x) = x + O(x^2)$, and the factor $(1 - \lambda)/\lambda$ is the same for all documents.
3. On the toy collection with $\lambda = 0.5$, document 1 gets the weight 1.6843 for "search" and document 7 gets 1.5994 for the same word with $\mathrm{tf} = 1$. Why? *Answer:* document 1 has 9 tokens and document 7 has 10, so the relative frequency is $1/9$ against $1/10$.

## References
