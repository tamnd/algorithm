---
tag: XQFSNB
kind: model
slug: two-poisson-model
name: Two-Poisson model
aliases:
- 2-Poisson model
- Harter's model
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Models within-document term frequency as a mixture of two Poisson distributions, for documents elite and not elite for the term.
prereqs: [poisson-distribution, binary-independence-model]
see_also: [bm25, divergence-from-randomness, expectation-maximization, gaussian-mixture-model, zipfs-law, tf-idf]
sources:
  - paper: "Abraham Bookstein and Don R. Swanson, Probabilistic models for automatic indexing, Journal of the American Society for Information Science 25(5), 1974, from page 312"
    locator: the proposal of a mixture of Poisson distributions for the occurrences of a word, with one class of documents about the concept of the word
  - paper: doi:10.1002/asi.4630260402
    title: Stephen P. Harter, A probabilistic approach to automatic keyword indexing, Part I, On the distribution of specialty words in a technical literature, Journal of the American Society for Information Science 26(4), 197 to 206, 1975
    locator: the mixture of two Poisson distributions for specialty words, and its fit to word counts in a technical collection
  - paper: "Stephen E. Robertson, C. J. van Rijsbergen and Martin F. Porter, Probabilistic models of indexing and searching, in R. N. Oddy, S. E. Robertson, C. J. van Rijsbergen and P. W. Williams (eds.), Information Retrieval Research, Butterworths, 1981, pages 35 to 56"
    locator: the combination of the two-Poisson model of eliteness with the relevance weighting model, which gives a weight as a function of term frequency
  - paper: doi:10.1007/978-1-4471-2099-5_24
    title: Stephen E. Robertson and Steve Walker, Some simple effective approximations to the 2-Poisson model for probabilistic weighted retrieval, Proceedings of SIGIR 1994, 232 to 241
    locator: the properties of the two-Poisson weight as a function of tf (zero at zero, increasing, with an asymptote), its approximation by tf/(k1 + tf), and the correction for document length
  - paper: doi:10.1561/1500000019
    title: Stephen Robertson and Hugo Zaragoza, The probabilistic relevance framework, BM25 and beyond, Foundations and Trends in Information Retrieval 3(4), 333 to 389, 2009
    locator: eliteness, the two-Poisson model and the saturation function of BM25
---

The two-Poisson model says that the number of times a term occurs in a document follows a mixture of two [Poisson distributions](/poisson-distribution/). Documents that are *elite* for the term, that is, about the concept the term names, have a high mean count, and the other documents have a low one. Bookstein and Swanson (1974) and Harter (1975) proposed it to choose index terms. Robertson, van Rijsbergen and Porter (1981) joined it to the [binary independence model](/binary-independence-model/), and the shape of the term weight that results is the source of the saturating term frequency of [BM25](/bm25/).

## The machine

**Eliteness.** Fix a term $t$ and documents of equal length. Each document has a hidden 0-1 variable $E$, which is 1 when the document is elite for $t$. Let $\pi = P(E = 1)$. Given $E$, the term frequency $\mathrm{tf}$ is Poisson:

$$P(\mathrm{tf} = k) = \pi \, \frac{e^{-\lambda} \lambda^k}{k!} + (1 - \pi) \, \frac{e^{-\mu} \mu^k}{k!}, \qquad k = 0, 1, 2, \ldots,$$

with $\lambda > \mu$. A non-elite document can still contain the term, by chance, at the low rate $\mu$.

**Relevance.** Relevance acts on $\mathrm{tf}$ only through eliteness: given $E$, the count does not depend on $R$. Let $p' = P(E = 1 \mid R = 1)$ and $q' = P(E = 1 \mid R = 0)$, with $p' > q'$. Write $P_\lambda(k) = e^{-\lambda}\lambda^k/k!$. Then

$$P(\mathrm{tf} = k \mid R = 1) = p' P_\lambda(k) + (1 - p') P_\mu(k), \qquad P(\mathrm{tf} = k \mid R = 0) = q' P_\lambda(k) + (1 - q') P_\mu(k).$$

**The weight.** As in the binary independence model, the term adds to the log odds of relevance the weight of $\mathrm{tf} = k$ relative to $\mathrm{tf} = 0$, with the natural log:

$$w(k) = \ln \frac{P(\mathrm{tf} = k \mid R = 1) \, P(\mathrm{tf} = 0 \mid R = 0)}{P(\mathrm{tf} = k \mid R = 0) \, P(\mathrm{tf} = 0 \mid R = 1)}.$$

It has three properties (Robertson and Walker 1994):

- $w(0) = 0$;
- $w(k)$ increases with $k$;
- $w(k)$ has a limit. For large $k$ the $P_\lambda$ part dominates both counts, so $w(k) \to \ln(p'/q') + \ln(P(0 \mid R = 0)/P(0 \mid R = 1))$. When $e^{-\lambda}$ is close to 0 the limit is close to $\ln[p'(1 - q')/(q'(1 - p'))]$, the binary independence weight of eliteness itself.

**Example of the weight.** Take $\lambda = 3$, $\mu = 0.3$, $p' = 0.7$ and $q' = 0.1$:

| $\mathrm{tf}$ | 0 | 1 | 2 | 3 | 4 | 5 | limit |
|---|---|---|---|---|---|---|---|
| $w(\mathrm{tf})$ | 0 | 0.7329 | 2.1183 | 2.7870 | 2.8936 | 2.9050 | 2.9063 |

The limit is a little below $\ln(0.7 \cdot 0.9/(0.1 \cdot 0.3)) = \ln 21 = 3.0445$, because $e^{-3} = 0.05$ is not 0. With these values the curve is S-shaped: the step from 1 to 2 is larger than the step from 0 to 1, since one occurrence is also likely in a non-elite document.

**Example of the mixture.** With $\pi = 0.2$ and the same $\lambda$ and $\mu$, the mean count is $0.2 \cdot 3 + 0.8 \cdot 0.3 = 0.84$. Compare the mixture with one Poisson of the same mean:

| $k$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| mixture | 0.6026 | 0.2077 | 0.0715 | 0.0475 | 0.0338 |
| one Poisson, mean 0.84 | 0.4317 | 0.3626 | 0.1523 | 0.0426 | 0.0090 |

The mixture has more documents with no occurrence and more with many. A content word occurs in bursts in the documents about its topic, and one Poisson cannot fit that.

**On the toy collection.** In the toy collection of the information retrieval pages, "sorted" has $\mathrm{cf} = 5$ occurrences in $N = 8$ documents. One Poisson with mean $5/8 = 0.625$ predicts $8(1 - e^{-0.625}) = 3.72$ documents that contain it, against the observed $\mathrm{df} = 4$, and $8 \cdot P(2) = 0.84$ documents with two occurrences, against one ($d_2$). Eight documents are far too few to tell one Poisson from two.

## What it counts

- **Parameters.** Three for each term, $\pi$, $\lambda$ and $\mu$, fitted to the counts of the term over the collection, and two more, $p'$ and $q'$, that link eliteness to relevance. Harter fitted the first three to the observed counts of each word; [expectation maximization](/expectation-maximization/) is the usual method now.
- **Data.** The histogram of $\mathrm{tf}$ over the documents for each term. One iteration of EM costs time linear in the number of distinct counts.
- **Length.** The basic model assumes documents of one length. For documents of length $|d|$ the means become $\lambda |d|$ and $\mu |d|$ per unit of length, which is how Robertson and Walker bring length into the weight.

## Relation to other models

- **Binary independence model.** That model observes only whether the term occurs. The two-Poisson model puts a hidden eliteness in its place and observes the count. Its limiting weight is the binary independence weight of eliteness.
- **BM25.** The full weight needs $p'$ and $q'$, which are not known without relevance information. Robertson and Walker (1994) keep its three properties and replace it by $\mathrm{tf}/(k_1 + \mathrm{tf})$ times the Robertson-Sparck Jones weight. The function $\mathrm{tf}/(k_1 + \mathrm{tf})$ is concave, so it keeps the zero, the growth and the bound, but not the S-shape of the example above. This is the derived part of [BM25](/bm25/); $k_1$ and the length factor are fitted by experiment.
- **Divergence from randomness.** [Divergence from randomness](/divergence-from-randomness/) keeps one random model, such as one Poisson for the whole collection, and weights a term by how unlikely its count is under that model. Its after-effect normalization stands in for the elite set.
- **Mixture models.** The model is a two-class mixture with a hidden class, like a [Gaussian mixture model](/gaussian-mixture-model/) with Poisson parts. The EM fit is the same.
- **Word frequencies.** The skewed distribution of words in a collection, as in [Zipf's law](/zipfs-law/), concerns totals over all documents. The two-Poisson model is about the counts of one word across documents.

## Known results in the model

- **Shape of the weight.** Robertson and Walker (1994) show that $w(0) = 0$, that $w$ increases with $\mathrm{tf}$ and that it tends to a limit. The example above shows that it need not be concave for small $\mathrm{tf}$.
- **Simple approximations work.** In the experiments of Robertson and Walker, the approximation $\mathrm{tf}(k_1 + 1)/(k_1 + \mathrm{tf})$ with a length correction did clearly better than weights without tf. Weights of this form were used in the Okapi system as BM15 and BM11, and BM25 interpolates between them with the parameter $b$.
- **Specialty words.** Harter (1975) found that specialty words of a technical literature fit the two-Poisson model better than one Poisson, and he proposed to choose as index terms the words whose two classes separate well.
- **Estimation is hard.** With three parameters for each term and the relevance parameters unknown, the full model was not practical for retrieval. This is why the field moved to approximations of its shape.

## References
