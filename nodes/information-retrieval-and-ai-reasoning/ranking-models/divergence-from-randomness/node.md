---
tag: 84Z020
kind: model
slug: divergence-from-randomness
name: Divergence from randomness
aliases:
- DFR framework
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Weights a term by how far its frequency in a document diverges from a random model, normalized for information gain and document length.
prereqs: [two-poisson-model, binomial-distribution]
see_also: [bm25, tf-idf, poisson-distribution, geometric-distribution, stirling-approximation, shannon-entropy, kullback-leibler-divergence, pivoted-length-normalization]
sources:
  - paper: doi:10.1145/582415.582416
    title: Gianni Amati and Cornelis Joost van Rijsbergen, Probabilistic models of information retrieval based on measuring the divergence from randomness, ACM Transactions on Information Systems 20(4), 357 to 389, 2002
    locator: the weight (1 - Prob2) times (-log2 Prob1) in equations 1 and 3; the basic models P, D, G, BE, I(n), I(ne) and I(F) in equations 6 to 21; the first normalizations L and B in equations 24 and 27; the second normalizations H1 and H2 in equations 41 and 42 and the parameter c in equation 46; the score of equation 43; the names of Table I; and the comparison with BM25 in Section 6, equation 45
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 9 (language modeling and related methods, with divergence from randomness)
---

Divergence from randomness is a framework of term weights in which a term gets a high weight in a document when its frequency there would be very improbable if the occurrences of the term were spread over the documents at random. Amati and van Rijsbergen (2002) build each weight from three choices: a *basic model* of randomness, such as the [Poisson distribution](/poisson-distribution/), whose improbability is measured in bits; a *first normalization*, the after effect, which discounts the gain once the term is known to occur; and a *second normalization* of the term frequency for document length. The choices give names such as PL2 and InL2, and InL2 is close to [BM25](/bm25/) with $k_1 \approx 1$ and $b \approx 0.72$. The framework keeps the eliteness idea of the [two-Poisson model](/two-poisson-model/) with no parameter to fit for the basic models.

## The machine

**Statistics.** For a term $t$ and a document $d$: $N$ documents, $F = \mathrm{cf}(t)$ occurrences of $t$ in the collection, $n = \mathrm{df}(t)$ documents that contain it, $l = |d|$ and the average length $\mathrm{avg\_l}$. All logs on this page are $\log_2$, so the weights are in bits.

**The weight.** Equations 1 and 3 of Amati and van Rijsbergen define

$$w(t, d) = \mathrm{Inf}_1 \cdot \mathrm{Inf}_2 = \left(-\log_2 \mathrm{Prob}_1(\mathrm{tfn})\right) \cdot \left(1 - \mathrm{Prob}_2(\mathrm{tfn})\right),$$

and the score is $R(q, d) = \sum_{t \in q} \mathrm{qtf}(t, q) \cdot w(t, d)$ (equation 43). Three choices fill it in.

**1. Second normalization: length.** The raw $\mathrm{tf}$ is first mapped to a normalized frequency $\mathrm{tfn}$:

- H1 (equation 41): $\mathrm{tfn} = \mathrm{tf} \cdot \mathrm{avg\_l}/l$, a uniform density of the term over the document;
- H2 (equation 42): $\mathrm{tfn} = \mathrm{tf} \cdot \log_2(1 + \mathrm{avg\_l}/l)$, a density that falls more slowly with length.

The paper introduces a free parameter later (equation 46), $\mathrm{tfn} = \mathrm{tf} \cdot \log_2(1 + c \cdot \mathrm{avg\_l}/l)$, and uses $c = 7$ for TREC-10. The base form H2 is the case $c = 1$.

**2. Basic model: $\mathrm{Inf}_1 = -\log_2 \mathrm{Prob}_1$.** $\mathrm{Prob}_1(\mathrm{tfn})$ is the probability that a document gets $\mathrm{tfn}$ occurrences of $t$ when the $F$ occurrences fall into the $N$ documents at random. With $\lambda = F/N$:

- P, Poisson (equation 6), with [Stirling's formula](/stirling-approximation/) for the factorial: $\mathrm{Inf}_1 = \mathrm{tfn} \log_2 \frac{\mathrm{tfn}}{\lambda} + \left(\lambda + \frac{1}{12\,\mathrm{tfn}} - \mathrm{tfn}\right) \log_2 e + \frac{1}{2} \log_2(2\pi\,\mathrm{tfn})$;
- G, the [geometric](/geometric-distribution/) limit of the Bose-Einstein model (equation 17): $\mathrm{Inf}_1 = -\log_2 \frac{1}{1 + \lambda} - \mathrm{tfn} \log_2 \frac{\lambda}{1 + \lambda}$;
- I(n), the tf-idf model (equation 19): $\mathrm{Inf}_1 = \mathrm{tfn} \log_2 \frac{N + 1}{n + 0.5}$;
- I(ne) (equation 20): the same with $n$ replaced by the expected number of documents that contain $t$, $n_e = N(1 - ((N - 1)/N)^F)$, and I(F) (equation 21) with $F$ in place of $n$;
- D, the divergence approximation of the [binomial](/binomial-distribution/) (equation 8), and BE, the Bose-Einstein model (equation 18).

**3. First normalization: the after effect, $\mathrm{Inf}_2 = 1 - \mathrm{Prob}_2$.** Once a term occurs in a document, more occurrences are less surprising. $\mathrm{Prob}_2$ is the probability of one more occurrence, given $\mathrm{tfn}$ of them, in the elite set of the term:

- L, Laplace's law of succession (equation 24): $\mathrm{Inf}_2 = 1/(\mathrm{tfn} + 1)$;
- B, a ratio of two binomials (equation 27): $\mathrm{Inf}_2 = (F + 1)/(n\,(\mathrm{tfn} + 1))$.

**Names.** A model is named by its three letters: basic model, after effect, length normalization. PL2 is Poisson with Laplace and H2, InL2 is I(n) with Laplace and H2, and BB2 is Bose-Einstein with B and H2 (Table I of the paper).

**A check on the paper's example.** For the term "progress" Amati and van Rijsbergen take $F = 22789$, $N = 567529$ and $\mathrm{tf} = 11$, so $\lambda = 0.040155$. Model P gives $11 \log_2(11/0.040155) = 89.0749$, then $(0.040155 + 1/132 - 11) \log_2 e = -15.8008$, then $\frac{1}{2}\log_2(22\pi) = 3.0555$, which sum to 76.3296. The paper prints 76.3295.

**Example on the toy collection.** In the toy collection of the information retrieval pages, $N = 8$, $\mathrm{avg\_l} = 9.875$, $|d_1| = 9$ and every other document has 10 tokens. With H2 and $c = 1$, $\mathrm{tfn} = \log_2(1 + 9.875/9) = 1.0685$ for one occurrence in $d_1$, $0.9910$ for one occurrence in a document of 10 tokens and $1.9819$ for two. For q1 = "sorted array search" the values of $\lambda = F/N$ are $5/8 = 0.625$, $3/8 = 0.375$ and $2/8 = 0.25$. In $d_1$, for "search":

$$\mathrm{Inf}_1 = 1.0685 \log_2 \frac{1.0685}{0.25} + \left(0.25 + \frac{1}{12.822} - 1.0685\right) \log_2 e + \frac{1}{2} \log_2(2\pi \cdot 1.0685) = 2.2391 - 1.0683 + 1.3735 = 2.5443,$$

and $\mathrm{Inf}_2 = 1/2.0685 = 0.4834$, so the PL2 weight is 1.2300. The same steps give 0.8087 for "sorted" and 1.0150 for "array" in $d_1$.

| rank | document | PL2 | InL2 |
|---|---|---|---|
| 1 | $d_1$ | 3.0538 | 2.1750 |
| 2 | $d_2$ | 2.0555 | 1.3428 |
| 3 | $d_8$ | 1.7643 | 1.1759 |
| 4 | $d_7$ | 1.1755 | 0.9198 |
| 5 | $d_4$ | 0.7893 | 0.4977 |

For InL2 the I(n) factors $\log_2(9/(n + 0.5))$ are 1.0 for "sorted", 1.3626 for "array" and 1.8480 for "search", so in $d_1$ the weight is $(1.0 + 1.3626 + 1.8480) \cdot 1.0685 \cdot 0.4834 = 2.1750$. On q2 = "posting list merge" InL2 ties $d_3$ and $d_5$ at 1.5980, like BM25, because it uses $n$, and "list" and "merge" both have $n = 2$. PL2 separates them, $d_5$ 2.1505 above $d_3$ 1.9499, because it uses $F$: "list" occurs 3 times in the collection ($d_4$ holds it twice) and "merge" only 2 times, so one occurrence of "merge" is less likely by chance.

## What it counts

- **Information in bits.** $\mathrm{Inf}_1$ is the information content, in the sense of [Shannon](/shannon-entropy/), of seeing $\mathrm{tfn}$ occurrences under the random model. $\mathrm{Inf}_2$ is the fraction of that information that counts as gain.
- **Parameters.** None for the basic models and the after effects, which use only $N$, $F$ and $n$. The length normalization H2 has $c$ in its later form, tuned for each collection.
- **Statistics and cost.** Each posting needs $\mathrm{tf}$, each document its length, and each term $n$ and $F$. Scoring reads the posting lists of the query terms, $O(\sum_{t \in q} \mathrm{df}(t))$ postings, as for BM25.

## Relation to other models

- **Two-Poisson model.** The [two-Poisson model](/two-poisson-model/) fits two Poisson parts for each term, elite and non-elite. Divergence from randomness keeps one random part, fitted to the whole collection, and measures how far a document is from it. The after effect plays the role of the elite set: it is computed as if the document were already elite for the term.
- **BM25.** For InL2 the length and tf part is $\mathrm{tfn}/(\mathrm{tfn} + 1)$ with $\mathrm{tfn} = \mathrm{tf} \log_2(1 + \mathrm{avg\_l}/l)$. Amati and van Rijsbergen expand it (Section 6, equation 45) as about $\mathrm{tf}/(\mathrm{tf} + 0.2786 + 0.7213\, l/\mathrm{avg\_l})$. That is the tf part of [BM25](/bm25/) with $k_1 (1 - b) = 0.2786$ and $k_1 b = 0.7213$, so $k_1 \approx 1$ and $b \approx 0.72$. At $l/\mathrm{avg\_l} = 0.8$ and $\mathrm{tf} = 1$ the exact value is 0.5392 and the approximation 0.5389. The paper also notes that the tf formula of the INQUERY system matches $k_1 = 2$ (equation 34).
- **Tf-idf.** The I(n) basic model is $\mathrm{tfn}$ times an idf in bits, so InL2 is a [tf-idf](/tf-idf/) weight with a saturating tf part.
- **Pivoted normalization.** H2 is another length correction. It divides by a logarithm of the relative length, not by the straight line of [pivoted normalization](/pivoted-length-normalization/).
- **Divergence measures.** Model D approximates the binomial probability through the [Kullback-Leibler divergence](/kullback-leibler-divergence/) of the term's share of the document from its share of the collection.

## Known results in the model

- **InL2 approximates BM25.** The expansion above (Amati and van Rijsbergen 2002, equation 45) shows that a weight derived from three independent choices with no tuned constant lands close to BM25 with $k_1 = 1$ and $b = 0.72$.
- **The after effect is needed.** Without it, the basic models grow at least linearly in $\mathrm{tfn}$. With L, the PL2 weight grows only like $\log_2(\mathrm{tfn}/\lambda)$: for $\lambda = 0.625$ and no length normalization it is 0.7915 at $\mathrm{tf} = 1$, 2.6794 at $\mathrm{tf} = 10$ and 5.8760 at $\mathrm{tf} = 100$. With I(n) and L the weight is bounded by the idf, as in BM25.
- **A family of models.** The paper evaluates many combinations of basic model, after effect and normalization on TREC collections, and its Table I names them. The Terrier search engine implements the framework, and PL2, InL2 and I(ne)B2 are among its standard models.
- **Length parameter.** The base form of H2 has no free parameter. The constant $c$ of equation 46 was added afterwards and is tuned for each collection.

## References
