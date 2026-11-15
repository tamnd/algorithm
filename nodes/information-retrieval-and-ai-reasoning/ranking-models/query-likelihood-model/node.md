---
tag: 5D98HN
kind: model
slug: query-likelihood-model
name: Query likelihood model
aliases:
- language modeling approach to retrieval
- Ponte-Croft model
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Ranks each document by the probability that a unigram language model estimated from it generates the query.
prereqs: [maximum-likelihood-estimation, bayes-theorem, ranked-retrieval]
see_also: [jelinek-mercer-smoothing, dirichlet-prior-smoothing, relevance-model-rm3, bm25, tf-idf, probability-ranking-principle, kullback-leibler-divergence, divergence-from-randomness]
sources:
  - paper: doi:10.1145/290941.291008
    title: Jay M. Ponte and W. Bruce Croft, A language modeling approach to information retrieval, Proceedings of the 21st Annual International ACM SIGIR Conference (SIGIR 1998), 275-281
    locator: the language model of each document, the ranking by the probability of the query under it, and the multiple-Bernoulli form of that probability
  - paper: doi:10.1145/984321.984322
    title: Chengxiang Zhai and John Lafferty, A study of smoothing methods for language models applied to information retrieval, ACM Transactions on Information Systems 22(2) (2004), 179-214
    locator: the general form of a smoothed document model with the coefficient alpha_d, the rank-equivalent score, and the comparison of Jelinek-Mercer, Dirichlet prior and absolute discounting smoothing on TREC collections
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 12, Section 12.2 (the query likelihood model, the conjunctive behaviour of the maximum likelihood estimate, and the linear interpolation with the collection model)
---

The query likelihood model ranks the documents of a collection for a query $q$ by $P(q \mid M_d)$, the probability that a language model $M_d$ estimated from document $d$ generates the words of $q$. The model of each document is a unigram model: a probability for each word of the vocabulary, with no word order. Jay Ponte and Bruce Croft introduced this language modeling approach in 1998. The standard form today uses a multinomial model and a smoothing method, most often [Jelinek-Mercer](/jelinek-mercer-smoothing/) or [Dirichlet prior smoothing](/dirichlet-prior-smoothing/), because the [maximum likelihood](/maximum-likelihood-estimation/) estimate gives probability 0 to every query with a word that the document lacks. With smoothing the model reaches the effectiveness of [BM25](/bm25/) and is the base of feedback models such as the [relevance model](/relevance-model-rm3/).

## The machine

**Why the query probability.** [Bayes' theorem](/bayes-theorem/) gives $P(d \mid q) = P(q \mid d) \, P(d) / P(q)$. The factor $P(q)$ is the same for all documents, and with a uniform prior $P(d)$ the ranking by $P(d \mid q)$ is the ranking by $P(q \mid d)$. A prior that depends on the document, for example on its length or its link count, can be added as $\log P(d)$.

**The document model.** Let $\mathrm{tf}(t, d)$ be the count of word $t$ in $d$, $|d|$ the length of $d$ in tokens, $\mathrm{cf}(t)$ the count of $t$ in the whole collection and $|C|$ the number of tokens of the collection. The maximum likelihood estimate is $p_{ml}(t \mid d) = \mathrm{tf}(t, d)/|d|$, and the collection model is $p(t \mid C) = \mathrm{cf}(t)/|C|$. A query $q$ with count $c(t, q)$ for word $t$ has, under the multinomial model with parameters $p(\cdot \mid d)$,

$$\log P(q \mid d) = \sum_{t \in q} c(t, q) \log p(t \mid d),$$

with natural logs. The multinomial coefficient of the query is the same for all documents and is left out.

**Smoothing.** A smoothed model gives a seen word $t$, one with $\mathrm{tf}(t, d) > 0$, the probability $p_s(t \mid d)$, and an unseen word the probability $\alpha_d \, p(t \mid C)$, where $\alpha_d$ makes the probabilities sum to 1. Jelinek-Mercer smoothing uses $p_s(t \mid d) = (1 - \lambda) \, p_{ml}(t \mid d) + \lambda \, p(t \mid C)$ and $\alpha_d = \lambda$. Dirichlet smoothing uses $p_s(t \mid d) = (\mathrm{tf}(t, d) + \mu \, p(t \mid C))/(|d| + \mu)$ and $\alpha_d = \mu/(|d| + \mu)$. Both formulas also hold for unseen words, since they give $\alpha_d p(t \mid C)$ there.

**The rank-equivalent form.** Split the sum into seen and unseen words, and add and subtract $\log(\alpha_d p(t \mid C))$ for the seen ones. Then

$$\log P(q \mid d) = \sum_{t \in q,\ \mathrm{tf}(t, d) > 0} c(t, q) \log \frac{p_s(t \mid d)}{\alpha_d \, p(t \mid C)} + |q| \log \alpha_d + \sum_{t \in q} c(t, q) \log p(t \mid C).$$

The last sum does not depend on $d$, so it can be dropped for ranking. The first sum runs only over the query words in $d$, so it can be computed from the posting lists of the query words, as in any [ranked retrieval](/ranked-retrieval/) system. Zhai and Lafferty used this form to explain what smoothing does.

**The Bernoulli form.** Ponte and Croft's original model is a multiple-Bernoulli model: each word of the vocabulary is present in the query or not, and $P(q \mid d) = \prod_{t \in q} p(t \mid d) \prod_{t \notin q} (1 - p(t \mid d))$. It ignores how often a word occurs in the query. The multinomial form above replaced it in most later work.

**Walk-through on the toy collection.** The toy collection has $N = 8$ documents and $|C| = 79$ tokens. For q1 = "sorted array search", $\mathrm{cf}$ is 5, 3 and 2, so $p(t \mid C)$ is $5/79$, $3/79$ and $2/79$. Document 1, "binary search finds a key in a sorted array", has 9 tokens and holds each query word once. Document 2 holds "sorted" twice and "array" once, document 8 holds "sorted" and "array", document 7 holds "search" and document 4 holds "sorted"; each of these has 10 tokens. Documents 3, 5 and 6 hold no query word.

| document | 1 | 2 | 8 | 7 | 4 | 3, 5, 6 |
|---|---|---|---|---|---|---|
| maximum likelihood | -6.5917 | $-\infty$ | $-\infty$ | $-\infty$ | $-\infty$ | $-\infty$ |
| Jelinek-Mercer, $\lambda = 0.5$ | -7.7210 | -9.0709 | -9.5486 | -10.1872 | -10.8388 | -11.7866 |

Without smoothing only document 1, which has all three words, gets a finite score: $3 \log(1/9) = -6.5917$. With $\lambda = 0.5$ the order is $1, 2, 8, 7, 4$, then the three documents with no query word, which all get the constant $\sum_t \log(0.5 \, p(t \mid C)) = -11.7866$. In the rank-equivalent form, document 1 gets the weights 1.0136 for "sorted", 1.3676 for "array" and 1.6843 for "search", and $-11.7866 + 4.0656 = -7.7210$. The rare word "search" has the largest weight, the common word "sorted" the smallest.

## What it counts

- **The score.** A log probability, at most 0, for each document. Only the order matters. Scores for different queries are not on one scale, because longer queries have lower probabilities.
- **Parameters.** One smoothing parameter, $\lambda$ for Jelinek-Mercer or $\mu$ for Dirichlet, tuned on judged queries. The statistics are $\mathrm{tf}(t, d)$, $|d|$, $\mathrm{cf}(t)$ and $|C|$.
- **Time.** With the rank-equivalent form, $O(\sum_{t \in q} \mathrm{df}(t))$ postings, plus the length of each scored document for $\alpha_d$, plus the selection of the top results. Documents without any query word all get the same score, so they need not be scored.
- **Space.** One $\mathrm{tf}$ for each posting, one length per document and one $\mathrm{cf}$ per word, the same as for BM25.

## Relation to other models

- **Tf-idf.** In the rank-equivalent form, the weight of a seen word grows with $p_{ml}(t \mid d)$, like a tf factor, and falls with $p(t \mid C)$, like an [idf](/tf-idf/) factor; the term $|q| \log \alpha_d$ acts as a length correction. Smoothing with the collection model thus produces the three parts of a classic weighting from a probability model.
- **BM25.** BM25 comes from the [probability ranking principle](/probability-ranking-principle/) and a model of relevance, the query likelihood model from a model of the document. The two reach similar effectiveness on standard test collections, which is a measured result.
- **Binary independence model.** The [binary independence model](/binary-independence-model/) models how documents are generated given relevance and needs relevance information or a guess of it. The query likelihood model needs no relevance information but has no explicit notion of relevance, which feedback models such as the relevance model add back.
- **KL divergence.** Ranking by $-\mathrm{KL}(\theta_q \,\|\, \theta_d)$, the [Kullback-Leibler divergence](/kullback-leibler-divergence/) from a query model $\theta_q$ to the document model, gives $\sum_t p(t \mid \theta_q) \log p(t \mid d)$ plus a constant. With the maximum likelihood query model $p(t \mid \theta_q) = c(t, q)/|q|$, this is $\log P(q \mid d)/|q|$, the same ranking. A better query model, estimated from feedback documents, then plugs into the same formula.
- **Divergence from randomness.** [Divergence from randomness](/divergence-from-randomness/) also compares the frequency of a word in a document with its frequency in the collection, but it scores the surprise of the count under a model of randomness, not a probability of the query.

## Known results in the model

- **Zero probabilities.** Without smoothing, a document that lacks any query word scores $-\infty$, so the model behaves like a Boolean AND, as the toy table shows. A query word with $\mathrm{cf}(t) = 0$ gives $-\infty$ to every document even with smoothing, as in q4 of the toy collection, so systems drop such words from the query or give them a small floor probability.
- **Smoothing does idf and length normalization.** This follows from the rank-equivalent form, as Zhai and Lafferty showed. With Jelinek-Mercer, $\alpha_d = \lambda$ is the same for all documents and the length correction disappears; with Dirichlet, $\alpha_d$ is larger for short documents.
- **Sensitivity to smoothing.** Zhai and Lafferty measured on TREC collections that the results depend strongly on the smoothing parameter. With Jelinek-Mercer, short title queries did best with little smoothing, $\lambda$ near 0.1, and long queries with much more, near 0.7. With Dirichlet smoothing, a $\mu$ of about 2000 worked well across collections. A two-stage method with estimated parameters came close to the best single setting. These are measurements, not theorems.
- **Order on the toy collection.** On q1 the ranking $1, 2, 8, 7, 4$ is the same for $\lambda = 0.1$, 0.5 and 0.7. The documents differ in length by at most one token, so the length effects of Dirichlet smoothing are small there; the [Dirichlet page](/dirichlet-prior-smoothing/) shows one on q2 and uses a made-up pair of documents for a larger one.

## References
