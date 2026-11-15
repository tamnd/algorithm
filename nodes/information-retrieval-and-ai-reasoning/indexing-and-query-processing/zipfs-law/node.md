---
tag: 961PYC
kind: model
slug: zipfs-law
name: Zipf's law
aliases:
- Zipf distribution of term frequencies
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: The frequency of the i-th most common term in a collection is roughly proportional to 1/i.
prereqs: [term-document-incidence-matrix, discrete-probability-distribution]
see_also: [heaps-law, stop-word-removal, two-poisson-model, postings-gap-encoding, huffman-coding, harmonic-series, linear-regression, tf-idf]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 5, Section 5.1.2 (the law cf_i proportional to 1/i, the power law form, Figure 5.2 with the weighted least-squares fit on Reuters-RCV1 and its intercept 6.95, and the remark that the fit is not particularly good but good enough to serve as a model), Section 5.1 (Table 5.1 and the rule of 30), Exercise 5.13, and Section 5.4 (the references to Zipf 1949 and to Witten and Bell 1990 on the quality of the fit)
  - paper: "George Kingsley Zipf, Human Behavior and the Principle of Least Effort, Addison-Wesley, 1949"
    locator: the rank and frequency relation of words, proposed as an empirical regularity of language, as cited in Section 5.4 of Manning, Raghavan and Schuetze
---

Zipf's law is an empirical law about text: if the terms of a collection are ranked by how often they occur, the collection frequency of the term of rank $i$ is roughly proportional to $1/i$. It is a regularity that people fit to data, not a theorem, and on real collections it holds only roughly, with the largest errors at the top and the bottom ranks. George Kingsley Zipf described it in 1949. In information retrieval it is the standard model of how skewed term frequencies are, and it is used to estimate the effect of [stop word removal](/stop-word-removal/), the length of posting lists and, through [Heaps' law](/heaps-law/), the growth of the vocabulary.

## The machine

**Ranks and frequencies.** A collection is a sequence of $T$ tokens over a vocabulary of $M$ distinct terms. The *collection frequency* $\mathrm{cf}(t)$ of a term $t$ is the number of its tokens, so $\sum_t \mathrm{cf}(t) = T$. Sort the terms by frequency, $\mathrm{cf}_1 \ge \mathrm{cf}_2 \ge \cdots \ge \mathrm{cf}_M$, so that $\mathrm{cf}_i$ is the frequency of the term of rank $i$.

**The law.** In the form of Manning, Raghavan and Schuetze,

$$\mathrm{cf}_i \approx \frac{c}{i},$$

for a constant $c$ of the collection. The general form is a power law $\mathrm{cf}_i \approx c \, i^{-\alpha}$, with $\alpha$ near 1 for word counts. On a plot of $\log \mathrm{cf}_i$ against $\log i$, the law is a straight line, $\log \mathrm{cf}_i = \log c - \alpha \log i$, so $c$ and $\alpha$ are fitted by [linear regression](/linear-regression/) on the log-log points. The fit depends on the method: a plain least-squares line is pulled by the many rare terms at the end of the ranking, so fits often give weights to the points.

**The random text model.** To reason with the law, model the text as $T$ independent draws from a [discrete distribution](/discrete-probability-distribution/) over the ranks, with

$$p_i = \frac{i^{-\alpha}}{Z}, \qquad Z = \sum_{j} j^{-\alpha}.$$

For $\alpha = 1$ the sum must stop at a finite vocabulary size $M$, and $Z = H_M$, the $M$-th [harmonic number](/harmonic-series/). For $\alpha > 1$ the vocabulary can be infinite, and $Z = \zeta(\alpha)$, the Riemann zeta function. The expected frequency of rank $i$ is $T p_i$, which is the law with $c = T/Z$.

**On the toy collection.** The toy collection of the information retrieval pages has 79 tokens and 50 terms. The most frequent are "a" with 8 tokens, "sorted" with 5, and "array", "posting", "list", "of" and "the" with 3 each. With $c = 8$ the law predicts 4 for rank 2 and about 2.7 for rank 3. The data is far too small for a fit, but the shape is there: one term is much more common than the rest, and most terms are rare.

## What it counts

- **Parameters.** The exponent $\alpha$ and the constant $c$, or, in the random text model, $\alpha$ and the vocabulary size $M$.
- **Data.** The frequencies of the terms of one collection, after a fixed tokenization. Case folding, numbers and [stemming](/stemming/) change the counts and so the fitted constants.
- **What it predicts.** The share of the tokens that the top $r$ ranks cover, which is $H_r / H_M$ for $\alpha = 1$; the number of terms with a given frequency; and the length of the posting list of a term of rank $i$, which is at most $\mathrm{cf}_i$.
- **What it leaves out.** Which terms are frequent, how the tokens of a term spread over documents, and any order of the tokens. Two collections with the same rank and frequency curve can have very different posting lists.

## Relation to other models

- **[Heaps' law](/heaps-law/)** describes the number of distinct terms as a function of the number of tokens. The two laws are fitted to different measurements of the same text: the frequencies at one size, and the vocabulary as the size grows.
- **[Two-Poisson model](/two-poisson-model/).** Zipf's law is about totals over the whole collection. The two-Poisson model is about the counts of one term across documents, and it models how the tokens of a content word gather in few documents.
- **Codes for skewed data.** A [Huffman code](/huffman-coding/) of the terms, or a variable length code of the gaps of [posting lists](/postings-gap-encoding/), gets its gain from this skew: a few terms and many small gaps are very common.
- **Other power laws.** The same form fits many rank and size data outside text. The model here is only the one for term counts.

## Known results in the model

- **The fit on Reuters-RCV1 (measured).** Manning, Raghavan and Schuetze fit a line of slope $-1$ to the log-log plot of RCV1 by weighted least squares and get the intercept 6.95 in base 10, which is $\mathrm{cf}_1 \approx 10^{6.95} \approx 8.9$ million. They describe the fit as not particularly good, but good enough to serve as a model for their calculations of index size.
- **The share of the top ranks (derived, then measured).** With $\alpha = 1$ and the RCV1 vocabulary of $M = 391{,}523$ terms after case folding, the 30 most frequent terms cover $H_{30}/H_M = 3.995/13.455 \approx 0.297$ of the tokens, and the top 150 cover about 0.416. The token counts of Table 5.1 of the same book drop from 179,158,204 to 121,857,825 when the 30 most common words are removed, and to 94,516,599 for 150 words: 32 and 47 percent. So the law gets the size right, and it predicts too little for the very top ranks. The book states the same fact as the rule of 30: the 30 most common words account for about 30 percent of the tokens of written text.
- **The number of rare terms (derived).** If $\mathrm{cf}_i = c/i$ exactly, the terms with frequency at least $f$ are the ranks up to $c/f$, so about $c/f - c/(f+1) = c/(f(f+1))$ terms have frequency exactly $f$, out of about $c$ terms in all. So half of the terms occur once and one sixth occur twice. On the toy collection, 35 of 50 occur once and 8 occur twice.
- **Finite against infinite vocabulary (derived).** With $\alpha = 1$ the sum $\sum_i 1/i$ diverges, so the law can only hold up to a finite vocabulary size; this is part (i) of Exercise 5.13 of Manning, Raghavan and Schuetze. With $\alpha > 1$ the sum converges, and the model allows an unbounded vocabulary that grows with $T$ as Heaps' law says.
- **Vocabulary growth (derived).** In the random text model with $\alpha > 1$, the expected number of distinct terms in $T$ tokens grows as a constant times $T^{1/\alpha}$. The derivation, and the published results on finite collections, are on the page of [Heaps' law](/heaps-law/).

## References
