---
tag: HX3AB5
kind: technique
slug: pivoted-length-normalization
name: Pivoted document length normalization
aliases:
- pivoted normalization
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Tilts the length normalization of term weights around a pivot so that long documents are not penalized more than their relevance rate suggests.
prereqs: [vector-space-model, tf-idf]
see_also: [bm25, bm25f, divergence-from-randomness, cosine-similarity, query-likelihood-model, dirichlet-prior-smoothing]
sources:
  - paper: doi:10.1145/243199.243206
    title: Amit Singhal, Chris Buckley and Mandar Mitra, Pivoted document length normalization, Proceedings of SIGIR 1996, 21 to 29
    locator: the probability of relevance and of retrieval as functions of document length, the pivoted normalization (1 - slope) times pivot plus slope times old normalization, and pivoted unique normalization
  - paper: "Amit Singhal, Modern information retrieval, a brief overview, IEEE Data Engineering Bulletin 24(4), 35 to 43, 2001"
    locator: the pivoted normalization weighting formula with 1 + ln(1 + ln tf), the factor (1 - s) + s dl / avdl, s usually 0.20, and its comparison with Okapi BM25
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 6, Section 6.4.4 (pivoted normalized document length)
  - paper: doi:10.1145/2063576.2063584
    title: Yuanhua Lv and ChengXiang Zhai, Lower-bounding term frequency normalization, Proceedings of CIKM 2011, 7 to 16
    locator: very long documents get too small a normalized term frequency under length normalization, and a lower bound added to the term frequency part
---

Pivoted document length normalization replaces the length normalizer $u(d)$ of a document, such as its cosine norm, by the tilted line $(1 - s) \cdot p + s \cdot u(d)$, where the pivot $p$ is a typical value of $u$ and the slope $s$ is between 0 and 1. Documents longer than the pivot get a smaller normalizer than before, so a higher score, and shorter ones get a larger normalizer. Singhal, Buckley and Mitra (1996) introduced it after they found that [cosine normalization](/vector-space-model/) ranks long documents lower than their rate of relevance. The length factor of [BM25](/bm25/) is the same line, with the average length as the pivot and the parameter $b$ as the slope.

## In plain words

Long documents hold more words and repeat them more, so their raw scores are high. A normalization divides each score by a measure of length to cancel this. Singhal, Buckley and Mitra measured, on judged queries, how often documents of each length were relevant and how often the system retrieved them. With cosine normalization, short documents were retrieved more often than they were relevant, and long documents less often.

Pivoting keeps the normalization of one typical length, the pivot, and makes the normalization change more slowly with length on both sides of it. A document of the pivot length keeps its score. Shorter documents go down a little and longer documents go up a little. One number, the slope, says how far to tilt, and it is tuned on judged queries.

## When it applies

Use pivoting when:

- the score of a document is a sum of term weights divided by a normalizer that grows with the length of the document;
- the documents vary much in length, as in news, web pages or patents;
- relevance judgments show that the chance of retrieval falls faster with length than the chance of relevance;
- there are training queries to tune one slope.

Notation: $|d|$ is the length of $d$ in tokens, $\mathrm{avgdl}$ the average length, $u(d)$ the old normalizer, $p$ the pivot and $s$ the slope.

## The template

```pseudo id=main
PIVOTED-SCORE(q, d, s, p)
L1  u ← OLD-NORM(d)                     ▷ hole: cosine norm, number of distinct terms, or length in tokens
L2  z ← (1 - s) · p + s · u             ▷ the tilted normalizer
L3  return (sum over t in q of w(t, q) · w(t, d)) / z    ▷ hole: the unnormalized term weights
```

**Where the pivot comes from.** Singhal, Buckley and Mitra sort the documents into bins by length and plot two curves against length: the fraction of relevant documents in each bin, and the fraction of retrieved documents. Under the old normalization the curves cross at one length. Documents shorter than that are retrieved too often, and longer ones too rarely. Turning the normalizer around the crossing point, the pivot, with a slope below 1 moves the retrieval curve toward the relevance curve. In practice the pivot is set to the average of the old normalizer over the collection, and only the slope is tuned.

**The form with the average length.** Dividing every score by the same positive number $p$ does not change the order, so the normalizer of L2 can be written as $(1 - s) + s \cdot u(d)/p$. With $u(d) = |d|$ and $p = \mathrm{avgdl}$ this is

$$z(d) = (1 - s) + s \cdot \frac{|d|}{\mathrm{avgdl}},$$

which is 1 for a document of average length, $1 - s$ for an empty document and grows by $s$ for each extra average length. Singhal (2001) gives the full weighting, with natural logs,

$$s(q, d) = \sum_{t \in q \cap d} \frac{1 + \ln(1 + \ln \mathrm{tf}(t, d))}{(1 - s) + s \cdot |d| / \mathrm{avgdl}} \cdot \mathrm{qtf}(t, q) \cdot \ln \frac{N + 1}{\mathrm{df}(t)},$$

with $s$ usually 0.20.

**Walk-through on the toy collection.** In the toy collection of the information retrieval pages, $N = 8$, $|d_1| = 9$, every other document has 10 tokens, and $\mathrm{avgdl} = 79/8 = 9.875$. With $s = 0.2$:

- $z(d_1) = 0.8 + 0.2 \cdot 9/9.875 = 0.9823$;
- $z(d) = 0.8 + 0.2 \cdot 10/9.875 = 1.0025$ for a document of 10 tokens.

The idf factors $\ln(9/\mathrm{df})$ are 0.8109 for "sorted", 1.0986 for "array" and 1.5041 for "search", and a term with $\mathrm{tf} = 2$ gets $1 + \ln(1 + \ln 2) = 1.5266$. On q1 = "sorted array search":

| rank | document | sum of the numerators | $s = 0$ | $s = 0.2$ | $s = 1$ |
|---|---|---|---|---|---|
| 1 | $d_1$ | $0.8109 + 1.0986 + 1.5041$ | 3.4136 | 3.4752 | 3.7455 |
| 2 | $d_2$ | $1.5266 \cdot 0.8109 + 1.0986$ | 2.3366 | 2.3307 | 2.3074 |
| 3 | $d_8$ | $0.8109 + 1.0986$ | 1.9095 | 1.9047 | 1.8857 |
| 4 | $d_7$ | $1.5041$ | 1.5041 | 1.5003 | 1.4853 |
| 5 | $d_4$ | $0.8109$ | 0.8109 | 0.8089 | 0.8008 |

The column $s = 0$ has no length normalization. The shorter $d_1$ gains as $s$ grows, and the documents of 10 tokens lose. The lengths in the toy collection differ by one token, so the order does not change. In a collection with a document of 5 tokens and one of 20 tokens, $s = 1$ gives the normalizers 0.506 and 2.025, while $s = 0.2$ gives 0.901 and 1.205: the long document now loses a factor of 1.2 in place of 2.

## Classic examples

- **[Vector space model](/vector-space-model/) with pivoted cosine.** The old normalizer is the cosine norm of the document vector, and the pivot is its average over the collection.
- **[Tf-idf](/tf-idf/) with pivoted unique normalization.** The old normalizer is the number of distinct terms of the document, used with the L tf letter in the SMART scheme Lnu.ltu of Singhal, Buckley and Mitra.
- **[BM25](/bm25/).** Its length factor $1 - b + b \cdot |d| / \mathrm{avgdl}$ is the template with $u = |d|$, $p = \mathrm{avgdl}$ and slope $b$, usually 0.75. It is applied inside the saturation of tf, not to the whole score.
- **[BM25F](/bm25f/).** Each field $f$ has its own factor $1 - b_f + b_f \cdot l_f / \mathrm{avgl}_f$, with its own slope.

## Variations

- **Pivoted byte size.** The old normalizer is the length of the document in bytes. It suits text with many recognition errors, where false words inflate the number of distinct terms.
- **Normalization inside the tf function.** BM25 divides $\mathrm{tf}$ by the factor before the saturation, so the normalization changes the shape of the tf curve and not only its scale.
- **Lower-bounded tf.** Lv and Zhai (2011) show that under such a normalization a very long document that contains a query term can score almost as low as one that does not contain it. They add a constant $\delta$ to the normalized tf part, which gives BM25+ and similar forms.
- **Other length corrections.** [Divergence from randomness](/divergence-from-randomness/) rescales the term frequency as $\mathrm{tf} \cdot \log_2(1 + c \cdot \mathrm{avgdl} / |d|)$, and [Dirichlet smoothing](/dirichlet-prior-smoothing/) of the [query likelihood model](/query-likelihood-model/) corrects for length through its prior.

## Pitfalls

- **Slope out of range.** For $s > 1$ the normalizer of a short document can be 0 or negative. Keep $0 \le s \le 1$.
- **A slope for every collection.** The best slope depends on the collection and on the query set. A slope tuned on one test collection need not be good on another.
- **Stale averages.** When documents are added or removed, $\mathrm{avgdl}$ changes. An index that keeps an old average gives a normalizer that is no longer 1 at the average length.
- **Normalizing the query.** Any factor that depends only on the query multiplies all scores by the same number and does not change the order, so pivoting the query side is wasted work.

## Exercises

1. Show that the normalizers $(1 - s) p + s u(d)$ and $(1 - s) + s u(d)/p$ give the same ranking for every query. *Hint:* the first is $p$ times the second.
2. Compare the pivoted normalizer with $u(d)$ itself. For which documents is it smaller? *Answer:* $(1 - s) p + s u < u$ exactly when $(1 - s) p < (1 - s) u$, that is, for $s < 1$, when $u > p$: the documents above the pivot.
3. On the toy collection with $s = 0.2$, which query term weights of q2 = "posting list merge" are divided by 1.0025? *Answer:* all of them, because "posting", "list" and "merge" occur only in documents of 10 tokens.

## References
