---
tag: T2NA0M
kind: model
slug: bm25
name: Okapi BM25
aliases:
- BM25
- best match 25
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Scores a document by summing idf times a saturating, length-normalized term frequency, with parameters k1 and b.
prereqs: [binary-independence-model, tf-idf, pivoted-length-normalization]
see_also: [two-poisson-model, bm25f, divergence-from-randomness, query-likelihood-model, wand, block-max-wand, relevance-feedback, splade]
sources:
  - paper: doi:10.1007/978-1-4471-2099-5_24
    title: Stephen E. Robertson and Steve Walker, Some simple effective approximations to the 2-Poisson model for probabilistic weighted retrieval, Proceedings of SIGIR 1994, 232 to 241
    locator: the saturation function tf/(k1 + tf) as an approximation of the two-Poisson weight, the verbosity and scope hypotheses, and the length correction
  - paper: "Stephen E. Robertson, Steve Walker, Susan Jones, Micheline M. Hancock-Beaulieu and Mike Gatford, Okapi at TREC-3, in D. K. Harman (ed.), Overview of the Third Text REtrieval Conference (TREC-3), NIST Special Publication 500-225, 1995"
    locator: the weighting function BM25 with the parameters k1, b and k3, as used by the Okapi system in TREC-3
  - paper: doi:10.1561/1500000019
    title: Stephen Robertson and Hugo Zaragoza, The probabilistic relevance framework, BM25 and beyond, Foundations and Trends in Information Retrieval 3(4), 333 to 389, 2009
    locator: the derivation of BM25 from the binary independence model and eliteness, the meaning of k1 and b, and the usual values k1 from 1.2 to 2.0 and b equal to 0.75
  - paper: doi:10.1007/978-3-030-45442-5_4
    title: Chris Kamphuis, Arjen P. de Vries, Leonid Boytsov and Jimmy Lin, Which BM25 do you mean? A large-scale reproducibility study of scoring variants, Proceedings of ECIR 2020, Lecture Notes in Computer Science 12036, 28 to 34
    locator: eight variants of BM25 from the literature and from search engines, compared on several test collections, with small differences in effectiveness
  - paper: doi:10.1145/2063576.2063584
    title: Yuanhua Lv and ChengXiang Zhai, Lower-bounding term frequency normalization, Proceedings of CIKM 2011, 7 to 16
    locator: the lower bound delta added to the term frequency part of BM25 for very long documents
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 11, Section 11.4.3 (Okapi BM25, a non-binary model)
---

Okapi BM25 scores a document for a query by adding, over the query terms that the document contains, an [idf](/tf-idf/) weight times a term frequency factor that saturates and is corrected for the length of the document. It came out of the Okapi system of Robertson, Walker and colleagues at City University London, and its standard form was used at TREC-3 in 1994. Two of its parts are derived, the idf from the [binary independence model](/binary-independence-model/) and the shape of the saturation from the [two-Poisson model](/two-poisson-model/), and the rest are approximations with constants $k_1$ and $b$ fitted by experiment. With $k_1 = 1.2$ and $b = 0.75$ it is the usual baseline of ranked retrieval.

## The machine

**The formula.** For a query $q$ and a document $d$ in a collection of $N$ documents with average length $\mathrm{avgdl}$, with natural logs,

$$s(q, d) = \sum_{t \in q} \mathrm{IDF}(t) \cdot \frac{\mathrm{tf}(t, d) \, (k_1 + 1)}{\mathrm{tf}(t, d) + k_1 \left(1 - b + b \, \frac{|d|}{\mathrm{avgdl}}\right)} \cdot \frac{(k_3 + 1) \, \mathrm{qtf}(t, q)}{k_3 + \mathrm{qtf}(t, q)},$$

where the sum is over distinct query terms, and a term with $\mathrm{tf}(t, d) = 0$ adds 0. Two idf forms are common:

$$\mathrm{IDF}_{\mathrm{RSJ}}(t) = \ln \frac{N - \mathrm{df}(t) + 0.5}{\mathrm{df}(t) + 0.5}, \qquad \mathrm{IDF}_{\mathrm{Lucene}}(t) = \ln \left(1 + \frac{N - \mathrm{df}(t) + 0.5}{\mathrm{df}(t) + 0.5}\right).$$

The usual values are $k_1$ from 1.2 to 2.0 and $b = 0.75$ (Robertson and Zaragoza 2009). For $k_3$, Singhal (2001) gives values from 0 to 1000. As $k_3 \to \infty$ the query factor becomes $\mathrm{qtf}$, and $k_3 = 0$ makes it 1. For short queries with no repeated terms it is 1 in any case.

**What is derived and what is fitted.** BM25 is a family of formulas shaped by experiments, not the output of one derivation.

- *The sum over terms* is derived. It is the log odds of relevance under the term independence assumption of the binary independence model, ranked by the [probability ranking principle](/probability-ranking-principle/).
- *The idf* is derived. $\mathrm{IDF}_{\mathrm{RSJ}}$ is the Robertson-Sparck Jones weight with no relevance information, with the 0.5 corrections as a smoothing choice. It is 0 for a term in half of the documents and negative above. The Lucene form adds 1 inside the log so that it stays positive. That is an engineering choice, not a derivation.
- *The saturation* is an approximation. The two-Poisson weight is 0 at $\mathrm{tf} = 0$, increases with $\mathrm{tf}$ and has a limit. The function $\mathrm{tf}(k_1 + 1)/(\mathrm{tf} + k_1)$ has the same three properties and one parameter (Robertson and Walker 1994). $k_1$ sets how fast it saturates: $k_1 = 0$ gives a 0-1 weight, and a large $k_1$ gives a weight almost linear in $\mathrm{tf}$.
- *The length factor* $B(d) = 1 - b + b|d|/\mathrm{avgdl}$ is a heuristic. Under the *verbosity* hypothesis, a long document says the same thing with more words, so $\mathrm{tf}$ should be divided by the length. Under the *scope* hypothesis, it covers more topics, so the length should not matter. The slope $b$ mixes the two, exactly as in [pivoted length normalization](/pivoted-length-normalization/) with the pivot at $\mathrm{avgdl}$. BM25 divides $\mathrm{tf}$ by $B(d)$ inside the saturation.
- *The factor $k_1 + 1$* makes the tf part equal 1 when $\mathrm{tf} = 1$ and $B(d) = 1$. It multiplies every score by one constant and does not change the ranking, and some implementations leave it out.
- *The query factor with $k_3$* is a saturation of the query term frequency of the same form, chosen by analogy.

**Example.** The toy collection of the information retrieval pages has $N = 8$, $|d_1| = 9$, every other document 10 tokens long, and $\mathrm{avgdl} = 9.875$. Take q1 = "sorted array search", $k_1 = 1.2$, $b = 0.75$ and the Lucene idf. The document frequencies are 4, 3 and 2, so the idf values are $\ln 2 = 0.6931$ for "sorted", $\ln(1 + 5.5/3.5) = 0.9445$ for "array" and $\ln(1 + 6.5/2.5) = 1.2809$ for "search".

- For $d_1$, $B = 0.25 + 0.75 \cdot 9/9.875 = 0.9335$, so $k_1 B = 1.1203$, and each query term has $\mathrm{tf} = 1$, with tf part $2.2/2.1203 = 1.0376$. The score is $(0.6931 + 0.9445 + 1.2809) \cdot 1.0376 = 3.0283$.
- For a document of 10 tokens, $B = 1.0095$ and $k_1 B = 1.2114$. The tf part is $2.2/2.2114 = 0.9948$ for $\mathrm{tf} = 1$ and $4.4/3.2114 = 1.3701$ for $\mathrm{tf} = 2$. Document $d_2$ holds "sorted" twice and "array" once, so its score is $0.6931 \cdot 1.3701 + 0.9445 \cdot 0.9948 = 1.8893$.

| rank | document | query terms with tf | Lucene idf score | RSJ idf score |
|---|---|---|---|---|
| 1 | $d_1$ | sorted 1, array 1, search 1 | 3.0283 | 1.4604 |
| 2 | $d_2$ | sorted 2, array 1 | 1.8893 | 0.4497 |
| 3 | $d_8$ | sorted 1, array 1 | 1.6292 | 0.4497 |
| 4 | $d_7$ | search 1 | 1.2743 | 0.9506 |
| 5 | $d_4$ | sorted 1 | 0.6896 | 0.0000 |

The rank column is for the Lucene idf. With the RSJ idf, "sorted" is in exactly half of the documents and gets weight 0, so the order becomes $d_1$, $d_7$, $d_2$, $d_8$, $d_4$, and $d_2$ ties with $d_8$ because only "array" counts for both. On q2 = "posting list merge" the Lucene scores are $d_4$ 2.6946, $d_3$ 2.2139, $d_5$ 2.2139 and $d_2$ 1.2743. The scores of $d_3$ and $d_5$ are equal, because "list" and "merge" both have $\mathrm{df} = 2$ and both documents have 10 tokens, so $d_3$ comes first by id. On q3 = "rank documents" only $d_7$ scores, with 3.5651. On q4 = "quantum circuit" no document contains a query term and the answer is empty.

**Evaluation.** An index stores $\mathrm{tf}(t, d)$ in each posting, $|d|$ for each document, and $N$ and $\mathrm{avgdl}$ for the collection. The implementation in `impl/python/bm25.py` scores term at a time: line L1 computes $B(d)$, line L2 the tf part, line L4 adds each posting's contribution to an accumulator, and line L5 sorts by score descending and then by id ascending.

## What it counts

- **The score.** A real number for each document that contains at least one query term. Only the order matters for the ranking. Scores of different queries are not on a common scale.
- **Parameters.** $k_1$, $b$ and, for long queries, $k_3$, tuned on judged queries. The collection statistics are $N$, $\mathrm{df}(t)$ for each term and $\mathrm{avgdl}$.
- **Time.** $O(\sum_{t \in q} \mathrm{df}(t))$ postings for exhaustive scoring, plus the selection of the top $k$. Each term adds at most $\mathrm{IDF}(t)(k_1 + 1)$ times its query factor, because the tf part is below $k_1 + 1$. This bound lets [WAND](/wand/), [MaxScore](/maxscore/) and [block-max WAND](/block-max-wand/) skip documents that cannot enter the top $k$.
- **Space.** One integer $\mathrm{tf}$ for each posting and one length for each document. Some engines store the lengths in a lossy form of one byte.

## Relation to other models

- **Binary independence model.** With $k_1 = 0$ the tf part is 1 for every present term, and BM25 is the binary independence model with no relevance information. With judged documents, the idf can be replaced by the full Robertson-Sparck Jones weight with $R$ and $r_t$, which is [relevance feedback](/relevance-feedback/) in this model.
- **Two-Poisson model.** The saturation stands in for the weight of the [two-Poisson model](/two-poisson-model/), whose eliteness parameters are not known without judgments.
- **Pivoted length normalization.** The factor $B(d)$ is a [pivoted normalization](/pivoted-length-normalization/) with slope $b$ and pivot $\mathrm{avgdl}$. The limits $b = 0$ and $b = 1$ were the Okapi weights BM15 and BM11.
- **Vector space model.** BM25 is an inner product of a sparse query vector and a sparse document vector, as in the [vector space model](/vector-space-model/), but with saturated and length-corrected document weights and no cosine.
- **BM25F.** For documents with fields such as title and body, [BM25F](/bm25f/) combines the weighted and normalized frequencies of the fields before the saturation.
- **Divergence from randomness.** Amati and van Rijsbergen (2002) show that their model I(n)L2 is close to BM25 with $k_1$ about 1 and $b$ about 0.72; see [divergence from randomness](/divergence-from-randomness/).
- **Language models.** The [query likelihood model](/query-likelihood-model/) with [Dirichlet smoothing](/dirichlet-prior-smoothing/) reaches similar effectiveness from a different model, with the prior mass $\mu$ in the role of the length correction.
- **Learned sparse retrieval.** [SPLADE](/splade/) learns the term weights of documents and queries and keeps the same sum over terms, so it runs on the same inverted index.

## Known results in the model

- **Variants differ little.** Kamphuis, de Vries, Boytsov and Lin (2020) compare eight variants of BM25 from papers and from search engines on several test collections and find that the choice among them changes effectiveness very little.
- **Limits of the parameters.** At $k_1 = 0$ the score is a sum of idf values over the query terms present. As $k_1 \to \infty$ the tf part tends to $\mathrm{tf}/B(d)$, a raw term frequency divided by the length factor. At $b = 0$ the length of the document has no effect.
- **Long documents.** For a very long document $B(d)$ is large, and the tf part of a present term can come close to 0, about as low as the score of a document without the term. Lv and Zhai (2011) add a lower bound $\delta$ to the tf part, which gives BM25+.
- **Negative weights.** With $\mathrm{IDF}_{\mathrm{RSJ}}$, a query term in more than half of the documents gets a negative weight, so a document can score lower because it contains a query term. This is why engines use the Lucene form or clamp the idf at 0.
- **Use.** BM25 is the default similarity of Lucene and of search engines built on it, the first stage of many neural ranking pipelines, and a standard baseline in test collection experiments.

## References
