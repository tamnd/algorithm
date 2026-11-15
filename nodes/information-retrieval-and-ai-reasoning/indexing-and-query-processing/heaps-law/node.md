---
tag: Q84HKV
kind: model
slug: heaps-law
name: Heaps' law
aliases:
- Herdan's law
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: The number of distinct terms in a collection of T tokens grows as k T^b with b near one half.
prereqs: [zipfs-law, expected-value]
see_also: [coupon-collector-problem, balls-into-bins, front-coding, dynamic-index-maintenance, stemming, inverted-index, linear-regression]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 5, Section 5.1.1 (the law M = kT^b, the typical ranges 30 to 100 for k and about 0.5 for b, the least-squares fit log10 M = 0.49 log10 T + 1.64 on Reuters-RCV1, and the prediction of 38,323 terms for the first 1,000,020 tokens against 38,365 observed), Exercise 5.13, and Section 5.4 (Heaps 1978 and the study of vocabulary growth by Williams and Zobel 2005)
  - paper: "H. S. Heaps, Information Retrieval, Computational and Theoretical Aspects, Academic Press, 1978"
    locator: the growth of the vocabulary as a power of the size of the text, as cited in Section 5.4 of Manning, Raghavan and Schuetze
  - paper: doi:10.1371/journal.pone.0014139
    title: Linyuan Lü, Zi-Ke Zhang and Tao Zhou, Zipf's law leads to Heaps' law, Analyzing their relation in finite-size systems, PLoS ONE 5(12), e14139, 2010
    locator: Heaps' law as a derivative phenomenon of Zipf's law, the approximate exponent of Heaps' law as an asymptotic result for infinite systems, and its dependence on the size of a finite system
---

Heaps' law is an empirical law about text: a collection of $T$ tokens has about $M = kT^b$ distinct terms, with constants $k$ and $0 < b < 1$ that are fitted to the collection, and $b$ is usually near one half. It is a fit to measured data, not a theorem, but under a random model of text it can be derived from [Zipf's law](/zipfs-law/). H. S. Heaps stated it in 1978, and in information retrieval it is used to estimate the size of the dictionary of an [inverted index](/inverted-index/) as the collection grows. The law says that the vocabulary never stops growing: new documents keep bringing new names, numbers and spelling errors.

## The machine

**Vocabulary growth.** Read the tokens of a collection in order. After $T$ tokens, let $M(T)$ be the number of distinct terms seen so far. The law is

$$M(T) \approx k \, T^b, \qquad \log M = \log k + b \log T,$$

so on a log-log plot the growth curve is a straight line with slope $b$, and $k$ and $b$ are fitted by [linear regression](/linear-regression/) on the log-log points. Manning, Raghavan and Schuetze give the typical ranges $30 \le k \le 100$ and $b \approx 0.5$ for English text. The order of the documents matters for a short prefix of the collection, and little for a long one.

**The random text model.** For the derived results, model the text as $T$ independent draws from a distribution $p_1 \ge p_2 \ge \cdots$ over the ranks of the terms. Rank $i$ is in the vocabulary after $T$ draws unless all $T$ draws miss it, so by linearity of [expectation](/expected-value/)

$$\mathbb{E}[M(T)] = \sum_i \left(1 - (1 - p_i)^T\right).$$

With equal probabilities $p_i = 1/n$ this is the count of filled bins in [balls into bins](/balls-into-bins/), and the time until all $n$ terms are seen is the [coupon collector problem](/coupon-collector-problem/). Heaps' law comes from the case of a Zipf distribution $p_i \propto i^{-\alpha}$.

**On the toy collection.** The toy collection of the information retrieval pages, read document by document, gives these pairs of tokens and terms: (9, 8), (19, 15), (29, 24), (39, 28), (49, 34), (59, 39), (69, 46), (79, 50). A least-squares line through the log-log points has slope $b \approx 0.84$ and $k \approx 1.28$. So short texts have $b$ near 1, because most of their words are new; the exponent near one half shows only after millions of tokens.

## What it counts

- **Parameters.** The two constants $k$ and $b$ of one collection and one tokenization. They are fits: other text, other tokenization, or another range of $T$ gives other values.
- **Data.** The pairs $(T, M(T))$ for prefixes of the collection.
- **What it predicts.** The number of distinct terms, and so the size of the dictionary and the number of posting lists, for a collection larger than the one measured. With $b < 1$, the vocabulary grows more slowly than the text, but without a bound.
- **What it leaves out.** Which terms are new, and how often each term occurs; that is the job of Zipf's law.

## Relation to other models

- **[Zipf's law](/zipfs-law/)** is a law about frequencies at one size of the collection. Heaps' law is about the vocabulary as the size grows. In the random text model the first implies the second, with $b = 1/\alpha$; see below.
- **The two are fitted separately.** For English, fits give a Zipf exponent near 1 and a Heaps exponent near 0.5, which the relation $b = 1/\alpha$ of independent draws cannot both match. Real text is not a sequence of independent draws from one fixed distribution: topics change, and names come in bursts.
- **[Balls into bins](/balls-into-bins/) and the [coupon collector problem](/coupon-collector-problem/)** are the case of equal probabilities, where the vocabulary fills up and stops at $n$ terms. Zipf probabilities with $\alpha > 1$ and an infinite vocabulary give growth without a bound.

## Known results in the model

- **The fit on Reuters-RCV1 (measured).** Manning, Raghavan and Schuetze fit $\log_{10} M = 0.49 \log_{10} T + 1.64$ to RCV1 for $T > 10^5$ by least squares, which is $b = 0.49$ and $k = 10^{1.64} \approx 44$. For the first 1,000,020 tokens it predicts $44 \times 1{,}000{,}020^{0.49} \approx 38{,}323$ terms, and the collection has 38,365. With the unrounded $k = 43.65$ the prediction is about 38,019. They note that case folding and stemming lower the growth, and numbers and spelling errors raise it.
- **Heaps from Zipf (derived).** Let $p_i = i^{-\alpha}/\zeta(\alpha)$ with $\alpha > 1$ over an infinite vocabulary. For small $p_i$, $(1 - p_i)^T \approx e^{-T p_i}$, and replacing the sum by an integral over the rank $x$ gives
  $$\mathbb{E}[M(T)] \approx \int_0^\infty \left(1 - e^{-T x^{-\alpha}/\zeta(\alpha)}\right) dx = \left(\frac{T}{\zeta(\alpha)}\right)^{1/\alpha} \int_0^\infty \left(1 - e^{-u^{-\alpha}}\right) du = \Gamma\!\left(1 - \frac{1}{\alpha}\right) \left(\frac{T}{\zeta(\alpha)}\right)^{1/\alpha},$$
  by the substitution $x = (T/\zeta(\alpha))^{1/\alpha} u$ and an integration by parts. This is Heaps' law with $b = 1/\alpha$ and $k = \Gamma(1 - 1/\alpha)\, \zeta(\alpha)^{-1/\alpha}$. For $\alpha = 2$, $k = \sqrt{6/\pi} \approx 1.382$. Against the exact sum, the approximation is off by about 1.1 percent at $T = 10^3$ and by 0.04 percent at $T = 10^6$ for $\alpha = 2$, and by at most 0.4 percent for $\alpha = 1.5$ at these sizes.
- **The case $\alpha = 1$ (derived).** With $\alpha = 1$ the vocabulary must be finite, of some size $n$, and $\mathbb{E}[M(T)] \le n$ for every $T$. So the model gives growth that slows down and stops, not a power law forever. This is the point of Exercise 5.13 of Manning, Raghavan and Schuetze, which asks to show that the vocabulary is finite under Zipf's law and infinite under Heaps' law, and whether one law can be derived from the other.
- **Finite collections (published).** Lü, Zhang and Zhou (2010) show that Heaps' law is a derivative phenomenon of Zipf's law, that the approximate exponent relation holds asymptotically for infinite systems, and that for finite systems the Heaps exponent depends on the size of the system.

## References
