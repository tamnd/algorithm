---
tag: E7EQCD
kind: model
slug: bm25f
name: BM25F
aliases:
- field-weighted BM25
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Extends BM25 to documents with fields by combining weighted, field-normalized term frequencies before the saturation step.
prereqs: [bm25]
see_also: [two-poisson-model, pivoted-length-normalization, anchor-text-indexing, learning-to-rank, inverted-index, wand]
sources:
  - paper: doi:10.1145/1031171.1031181
    title: Stephen Robertson, Hugo Zaragoza and Michael Taylor, Simple BM25 extension to multiple weighted fields, Proceedings of CIKM 2004, 42 to 49
    locator: why a linear combination of the BM25 scores of the fields breaks the saturation of term frequency, and the combination of weighted field frequencies before the saturation
  - paper: doi:10.1561/1500000019
    title: Stephen Robertson and Hugo Zaragoza, The probabilistic relevance framework, BM25 and beyond, Foundations and Trends in Information Retrieval 3(4), 333 to 389, 2009
    locator: the BM25F formula with per-field weights and per-field length normalization, and eliteness as a property of the whole document
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 8 (probabilistic retrieval, BM25 and its extension to fields)
---

BM25F is the form of [BM25](/bm25/) for documents with fields, such as a title, a body and the [anchor text](/anchor-text-indexing/) of links to the page. For each query term it adds the term frequencies of the fields, each one multiplied by a field weight and divided by a length factor of its own field, and it applies the saturation of BM25 once to that sum. Robertson, Zaragoza and Taylor (2004) proposed it because adding the BM25 scores of the separate fields lets one term count several times at nearly full strength, which undoes the saturation. With one field of weight 1, BM25F is exactly BM25.

## The machine

**Fields.** A document $d$ has fields $f = 1, \ldots, F$, each a list of tokens. For field $f$ let $l_f(d)$ be its length, $\mathrm{avgl}_f$ the average of $l_f$ over the collection and $\mathrm{tf}_f(t, d)$ the number of occurrences of $t$ in that field. Each field has a weight $w_f \ge 0$ and a slope $b_f \in [0, 1]$.

**Score.** The length factor of a field and the weighted pseudo-frequency of a term are

$$B_f(d) = 1 - b_f + b_f \, \frac{l_f(d)}{\mathrm{avgl}_f}, \qquad \widetilde{\mathrm{tf}}(t, d) = \sum_{f=1}^{F} w_f \, \frac{\mathrm{tf}_f(t, d)}{B_f(d)},$$

and the score, with natural logs, is

$$s(q, d) = \sum_{t \in q} \mathrm{IDF}(t) \cdot \frac{\widetilde{\mathrm{tf}}(t, d) \, (k_1 + 1)}{\widetilde{\mathrm{tf}}(t, d) + k_1}.$$

The idf is computed on whole documents: $\mathrm{df}(t)$ counts the documents that contain $t$ in any field. Robertson and Zaragoza (2009) write the formula without the factor $k_1 + 1$. This page keeps it, as on the BM25 page. It multiplies every score by one constant and does not change the ranking.

**One field.** With $F = 1$ and $w_1 = 1$, $\widetilde{\mathrm{tf}} = \mathrm{tf}/B$ and

$$\frac{(\mathrm{tf}/B)(k_1 + 1)}{\mathrm{tf}/B + k_1} = \frac{\mathrm{tf} \, (k_1 + 1)}{\mathrm{tf} + k_1 B},$$

which is the tf part of BM25. So BM25F moves the length normalization of BM25 inside each field and keeps one saturation.

**Why combine before the saturation.** In the [two-Poisson](/two-poisson-model/) view, a document is elite for a term or not, and every field is evidence about that one hidden event. A word in the title and the same word in the body are two observations of the same eliteness, so their counts should add before they pass through the saturating curve. With $b_f = 0$ for every field and integer weights, $\widetilde{\mathrm{tf}}$ is the term frequency of the document in which field $f$ is written out $w_f$ times, so a title weight of 2 means "read the title twice".

**Example.** Split each document of the toy collection of the information retrieval pages into a title, its first three tokens, and a body, the rest. Every title has 3 tokens, so $\mathrm{avgl}_{\mathrm{title}} = 3$ and $B_{\mathrm{title}} = 1$. The body of $d_1$ has 6 tokens and every other body has 7, so $\mathrm{avgl}_{\mathrm{body}} = 6.875$. Take $w_{\mathrm{title}} = 2$, $w_{\mathrm{body}} = 1$, $b_f = 0.75$ for both fields, $k_1 = 1.2$, and the Lucene idf of the whole documents: 0.6931 for "sorted", 0.9445 for "array" and 1.2809 for "search".

- $d_8$ = "the sorted array" + "of ids is compressed with gap encoding". Both "sorted" and "array" are in the title, so $\widetilde{\mathrm{tf}} = 2 \cdot 1/1 = 2$ for each, with tf part $2 \cdot 2.2/3.2 = 1.375$. The score is $(0.6931 + 0.9445) \cdot 1.375 = 2.2517$.
- $d_1$ = "binary search finds" + "a key in a sorted array". "Search" is in the title, with $\widetilde{\mathrm{tf}} = 2$. "Sorted" and "array" are in the body, where $B_{\mathrm{body}} = 0.25 + 0.75 \cdot 6/6.875 = 0.9045$, so $\widetilde{\mathrm{tf}} = 1.1055$ and the tf part is $1.1055 \cdot 2.2/2.3055 = 1.0549$. The score is $1.2809 \cdot 1.375 + (0.6931 + 0.9445) \cdot 1.0549 = 3.4888$.

On q1 = "sorted array search":

| rank | document | BM25F | BM25 on whole documents | sum of field scores |
|---|---|---|---|---|
| 1 | $d_1$ | 3.4888 | 3.0283 | 4.2894 |
| 2 | $d_8$ | 2.2517 | 1.6292 | 3.2752 |
| 3 | $d_2$ | 1.8857 | 1.8893 | 1.8857 |
| 4 | $d_7$ | 1.7613 | 1.2743 | 2.5619 |
| 5 | $d_4$ | 0.6880 | 0.6896 | 0.6880 |

The rank column is for BM25F. Document $d_8$ moves above $d_2$, because its query terms are in its title, while those of $d_2$ are in its body. The last column adds $w_f$ times a BM25 score computed on each field alone. It ranks $d_7$, whose only query term is "search" in the title, above $d_2$. In the field sum, one title occurrence of "search" adds $2 \cdot 1.2809 \cdot 1 = 2.5619$, twice the full weight of a single occurrence. In BM25F it adds $1.2809 \cdot 1.375 = 1.7613$, still below the bound $1.2809 \cdot 2.2$. On q2 = "posting list merge" BM25F gives $d_4$ 3.3089, $d_3$ and $d_5$ 2.2090 (in id order) and $d_2$ 1.7613, while the field sum puts $d_2$ (2.5619) above $d_3$ and $d_5$ (2.2090) only because "merge" is in its title.

## What it counts

- **Parameters.** $k_1$, and a weight $w_f$ and a slope $b_f$ for each field: $2F + 1$ numbers, tuned on judged queries. Short fields such as titles vary little in length and often get a different $b_f$ from the body.
- **Statistics.** $N$ and $\mathrm{df}(t)$ over whole documents, $l_f(d)$ for each document and field, and $\mathrm{avgl}_f$ for each field.
- **Index.** Either one posting list for each term and field, merged at query time, or one list for each term whose postings hold a frequency for each field. Scoring costs $O(\sum_{t \in q} \mathrm{df}(t))$ postings, as for BM25.
- **Bound.** The contribution of a term is below $\mathrm{IDF}(t)(k_1 + 1)$ whatever the fields hold, the same bound as in BM25, so the pruning methods of BM25 such as [WAND](/wand/) apply.

## Relation to other models

- **BM25.** BM25F with one field of weight 1 is BM25. With several fields and $w_f = 1$, $b_f = b$, it differs from BM25 on the whole document only in that each field is normalized by its own average length.
- **Pivoted length normalization.** Each $B_f$ is a [pivoted normalization](/pivoted-length-normalization/) of one field, with pivot $\mathrm{avgl}_f$ and slope $b_f$.
- **Linear combination of field scores.** Adding $w_f$ times the BM25 score of each field is the obvious alternative. Each field then has its own saturation, so a term in $F$ fields can add up to $\sum_f w_f$ times the bound of one field. Robertson, Zaragoza and Taylor (2004) show that this rewards a term spread over fields too much compared with a term repeated in one field.
- **Anchor text.** The text of links that point to a page is a field of the page in web search, and BM25F is a usual way to weight it against the title and the body; see [anchor text indexing](/anchor-text-indexing/).
- **Learning to rank.** BM25F scores, and the scores of single fields, are standard features of [learning to rank](/learning-to-rank/). The field weights can also be learned directly from judgments.

## Known results in the model

- **Saturation is kept.** For any fields, weights and lengths, the contribution of a term is an increasing function of $\widetilde{\mathrm{tf}}$ with the limit $\mathrm{IDF}(t)(k_1 + 1)$. The field sum has no such single bound.
- **Weights as repetition.** With all $b_f = 0$ and integer weights, BM25F equals BM25 with $b = 0$ on the document with each field repeated $w_f$ times (Robertson, Zaragoza and Taylor 2004).
- **One idf for each term.** The idf is a property of the term in the whole collection, not of a field, because eliteness belongs to the document. A field sum often uses the idf of each field, which is one more way in which it differs from BM25F.
- **Use.** Search engines that index fields, such as Lucene and the engines built on it, offer queries over several fields that combine the field frequencies before the saturation in this way.

## References
