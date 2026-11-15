---
tag: 7PSWMK
kind: technique
slug: dirichlet-prior-smoothing
name: Dirichlet prior smoothing
aliases:
- Bayesian smoothing with Dirichlet priors
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Smooths a document language model by adding mu pseudo-counts in proportion to the collection model, so short documents are smoothed more.
prereqs: [query-likelihood-model, jelinek-mercer-smoothing]
see_also: [conjugate-prior, bayesian-inference, relevance-model-rm3, bm25, pivoted-length-normalization, naive-bayes-classifier, latent-dirichlet-allocation]
sources:
  - paper: doi:10.1145/984321.984322
    title: Chengxiang Zhai and John Lafferty, A study of smoothing methods for language models applied to information retrieval, ACM Transactions on Information Systems 22(2) (2004), 179-214
    locator: the Dirichlet prior smoothing of document models with the coefficient alpha_d equal to mu over the document length plus mu, the comparison with Jelinek-Mercer and absolute discounting, and the measured good values of mu, about 2000
  - paper: "David J. C. MacKay and Linda C. Bauman Peto, A hierarchical Dirichlet language model, Natural Language Engineering (1995)"
    locator: the Dirichlet prior on the word distributions of a language model and the resulting predictive probabilities with pseudo-counts
  - paper: "Nasreen Abdul-Jaleel, James Allan, W. Bruce Croft, Fernando Diaz, Leah Larkey, Xiaoyan Li, Mark D. Smucker and Courtney Wade, UMass at TREC 2004, novelty and HARD, Proceedings of the Thirteenth Text REtrieval Conference (TREC 2004)"
    locator: Section 3.1.4, the retrieval runs with Dirichlet smoothing at mu equal to 1000 and the RM3 feedback model
---

Dirichlet prior smoothing estimates the language model of a document $d$ as $p(t \mid d) = (\mathrm{tf}(t, d) + \mu \, p(t \mid C))/(|d| + \mu)$: the counts of the document plus $\mu$ pseudo-counts spread over the vocabulary in proportion to the collection model $p(t \mid C)$. It is the posterior mean of the word distribution under a Dirichlet prior whose mean is the collection model, so it is a [Bayesian](/bayesian-inference/) estimate with a [conjugate prior](/conjugate-prior/). Compared with [Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/), the weight of the collection model is $\mu/(|d| + \mu)$, which is large for short documents and small for long ones. Zhai and Lafferty studied it in the [query likelihood model](/query-likelihood-model/) and measured that a $\mu$ of about 2000 works well on TREC collections, and it is a common default document model in language modeling systems.

## In plain words

A document gives us counts of its words. Before we read it, we already have a guess about word chances: the chances in the whole collection. Dirichlet smoothing treats that guess as if we had already seen some extra words, say a few thousand, spread over the vocabulary in collection proportions. We add these imagined words to the real counts and divide by the new total. A short document has few real words, so the imagined words decide most of its chances. A long document has many real words, so its own counts decide. This is what we want: a long document is a big sample, and we can trust it more. One number, the count of imagined words, controls how strong the guess is.

## When it applies

Use it when many small samples share one background distribution and the samples differ in size, so that a fixed mixing weight would smooth the large samples too much or the small ones too little. In retrieval the samples are documents of different lengths and the background is the collection. It needs a background model that is nonzero for every word that can occur in a query. If all documents have about the same length, it behaves almost like Jelinek-Mercer smoothing with $\lambda = \mu/(\bar{n} + \mu)$, where $\bar{n}$ is the common length.

## The template

```pseudo id=main
DIRICHLET-SCORE(q, d, μ)
L1  s ← 0
L2  for each word t of q, with count c(t, q):
L3      p_C ← cf(t) / |C|                          ▷ hole: the prior mean, nonzero for every t
L4      p ← (tf(t, d) + μ · p_C) / (|d| + μ)       ▷ hole: the prior mass μ
L5      s ← s + c(t, q) · log p
L6  return s
```

**Where the formula comes from.** Model the words of $d$ as draws from a multinomial with parameters $\theta$. Put on $\theta$ a Dirichlet prior with parameters $\mu \, p(t \mid C)$ for each word $t$. The Dirichlet is conjugate to the multinomial, so after the counts $\mathrm{tf}(t, d)$ the posterior is a Dirichlet with parameters $\mathrm{tf}(t, d) + \mu \, p(t \mid C)$, and the posterior mean of $\theta_t$, which is also the probability that the next word is $t$, is the formula of line L4. With $\mu = 0$ it is the [maximum likelihood](/maximum-likelihood-estimation/) estimate.

**The rank-equivalent form.** A word that $d$ lacks gets $\alpha_d \, p(t \mid C)$ with $\alpha_d = \mu/(|d| + \mu)$. Dividing each term of line L5 by $\alpha_d \, p(t \mid C)$ and dropping the part that is the same for all documents gives

$$\log P(q \mid d) \stackrel{\text{rank}}{=} \sum_{t \in q,\ \mathrm{tf}(t, d) > 0} c(t, q) \log\Bigl(1 + \frac{\mathrm{tf}(t, d)}{\mu \, p(t \mid C)}\Bigr) + |q| \log \frac{\mu}{|d| + \mu}.$$

The first sum holds the matched words. Their weight depends on the raw count $\mathrm{tf}$, not on $\mathrm{tf}/|d|$. The second term is a length penalty: it is closer to 0 for a short document. For Jelinek-Mercer the same term is $|q| \log \lambda$, the same for all documents, so the length effect is the difference between the two methods.

**Walk-through on the toy collection.** Take $\mu = 10$. Every document has 10 tokens, except document 1 with 9, so for most documents $\alpha_d = 10/20 = 0.5$, and their model is exactly Jelinek-Mercer with $\lambda = 0.5$. For document 1, $\alpha_d = 10/19 = 0.5263$. On q1 = "sorted array search":

| document | 1 | 2 | 8 | 7 | 4 | 3, 5, 6 |
|---|---|---|---|---|---|---|
| Jelinek-Mercer, $\lambda = 0.5$ | -7.7210 | -9.0709 | -9.5486 | -10.1872 | -10.8388 | -11.7866 |
| Dirichlet, $\mu = 10$ | -7.7954 | -9.0709 | -9.5486 | -10.1872 | -10.8388 | -11.7866 |

Only document 1 changes. Its matched weights are $\log(1 + 1/(10 \, p))$: 0.9478 for "sorted", 1.2902 for "array" and 1.5994 for "search", sum 3.8373, the same as a document of 10 tokens with these counts. Its length term is $3 \log(10/19) = -1.9256$, against $3 \log 0.5 = -2.0794$ for the others. The two parts give $3.8373 - 1.9256 - 9.7071 = -7.7954$, where $-9.7071 = \sum_t \log p(t \mid C)$.

The length term can reorder documents that match nothing. On q2 = "posting list merge", document 1 holds no query word but scores -12.1435, above documents 6, 7 and 8, which also hold none and score -12.2974, because it is one token shorter. On q3, document 7 leads with -5.7531, then document 1 with -10.0226, then the others with -10.1252.

With $\mu = 2000$, all q1 scores are near $-9.7$, within 0.04 of each other, in the same order. The pseudo-counts dwarf documents of 10 tokens, but only the order matters, and it is kept.

**Two documents of different length.** Let $p(t \mid C) = 0.01$ and $\mu = 100$. Document A has 5 tokens with $t$ once, and document B has 50 tokens with $t$ 10 times, so both have the relative frequency 0.2. Dirichlet gives A $(1 + 1)/105 = 0.0190$ and B $(10 + 1)/150 = 0.0733$. Jelinek-Mercer with $\lambda = 0.5$ gives both $0.5 \cdot 0.2 + 0.5 \cdot 0.01 = 0.105$. Dirichlet trusts the 10 occurrences in B more than the single one in A.

## Classic examples

- **[Query likelihood model](/query-likelihood-model/).** The standard document model. Zhai and Lafferty measured on TREC collections that a $\mu$ of about 2000 worked well across collections. That is a measured value, not a derived one.
- **[Relevance model](/relevance-model-rm3/).** The first retrieval of RM3 and the scores that weight its feedback documents usually come from Dirichlet-smoothed query likelihood. The UMass runs at TREC 2004 used $\mu = 1000$.
- **[Naive Bayes classifier](/naive-bayes-classifier/).** Add-one (Laplace) smoothing of the word counts of each class is the same posterior mean with a uniform prior mean and $\mu$ equal to the size of the vocabulary.
- **[Latent Dirichlet allocation](/latent-dirichlet-allocation/).** The word distributions of the topics and the topic mixtures of the documents have Dirichlet priors, and the estimates in collapsed Gibbs sampling have the same form, counts plus pseudo-counts over a total.

## Variations

- **Estimating $\mu$.** Zhai and Lafferty estimate $\mu$ from the collection by leave-one-out likelihood, with no relevance judgments.
- **Two-stage smoothing.** First smooth each document with a Dirichlet prior, then interpolate with a query background model as in Jelinek-Mercer smoothing. Zhai and Lafferty found that with estimated parameters it came close to the best single setting of either method.
- **Hierarchical priors.** MacKay and Peto put a prior on the prior mean itself, so the background distribution is estimated from the data.
- **Other base measures.** The prior mean need not be the collection model. A cluster model, a model of the document's topic or a model of its neighbours in a link graph can take its place.
- **Lower-bounded term weights.** For very long documents, the gain from one more occurrence of a word becomes small; Lv and Zhai proposed adding a lower bound to the matched weight, as in BM25+.

## Pitfalls

- **Posterior mean, not mode.** The formula of line L4 is the mean of the posterior. The [maximum a posteriori estimate](/maximum-a-posteriori-estimation/) subtracts 1 from each parameter and is negative for words with $\mathrm{tf} = 0$ and $\mu \, p(t \mid C) < 1$. Do not call the formula the MAP estimate.
- **$\mu$ and the document length.** A good $\mu$ is about the length of a typical document or larger, so a $\mu$ tuned on news articles of hundreds of words is wrong for passages of 50 words or for tweets. Tune $\mu$ on the collection you use.
- **Dropping the length term.** Code that only sums the matched weights of the rank-equivalent form, without $|q| \log \alpha_d$, gives a different ranking. The term is what makes the method length-aware.
- **Words that the collection lacks.** If $\mathrm{cf}(t) = 0$, the matched weight divides by 0 and the unmatched probability is 0. Remove such words from the query, as for every smoothing method that backs off to the collection.
- **Comparing scores across queries.** The scores are log probabilities of different queries, so they are not on one scale. Use them only to rank documents for one query.

## Exercises

1. Show that for documents that all have length $n$, Dirichlet smoothing with $\mu$ equals Jelinek-Mercer smoothing with $\lambda = \mu/(n + \mu)$. *Hint:* write $(\mathrm{tf} + \mu p)/(n + \mu)$ as $\frac{n}{n + \mu} \cdot \frac{\mathrm{tf}}{n} + \frac{\mu}{n + \mu} \cdot p$.
2. Show that as $\mu \to \infty$ every document has the score $\sum_t c(t, q) \log p(t \mid C)$, and that as $\mu \to 0$ the score of a document that lacks a query word tends to $-\infty$.
3. On the toy collection with $\mu = 10$, why does document 1 get the same matched weight for "search" as document 7 does, when under Jelinek-Mercer with $\lambda = 0.5$ it gets more? *Answer:* the Dirichlet weight $\log(1 + \mathrm{tf}/(\mu p))$ does not depend on the length; the length enters only through $\alpha_d$.

## References
