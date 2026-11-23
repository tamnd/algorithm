---
tag: N6CR1F
kind: problem
slug: private-query-release
name: Private query release
aliases:
- private data release
- differentially private synthetic data
area: security-and-privacy/differential-privacy
level: core
summary: Answer every query of a large class, such as all counting queries, accurately under differential privacy.
history:
  year: 2008
  people: [Avrim Blum, Katrina Ligett, Aaron Roth]
  note: Blum, Ligett and Roth showed at STOC 2008 that an epsilon-DP mechanism can answer exponentially many counting queries with a synthetic dataset. Earlier methods paid for each query.
prereqs: [differential-privacy-definition, laplace-mechanism]
see_also: [smalldb-mechanism, mwem, matrix-mechanism, binary-tree-mechanism, sparse-vector-technique, dinur-nissim-reconstruction-attack, packing-lower-bound, fingerprinting-codes-lower-bound]
sources:
  - paper: doi:10.1007/978-3-319-57048-8_7
    title: "Salil Vadhan, The complexity of differential privacy, in Tutorials on the Foundations of Cryptography, Springer, 2017, pages 347 to 450"
    locator: "Section 2 (Theorems 2.6 and 2.7, arbitrary counting queries), Section 4 (Theorem 4.1, SmallDB, and Theorem 4.3, private multiplicative weights), Section 5 (information-theoretic lower bounds) and Section 6 (computational lower bounds)"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014"
    locator: "Chapter 4 (releasing linear queries with correlated error: SmallDB and online multiplicative weights) and Chapter 8 (lower bounds)"
  - paper: doi:10.1145/2450142.2450148
    title: "Avrim Blum, Katrina Ligett and Aaron Roth, A learning theory approach to noninteractive database privacy, Journal of the ACM 60(2), Article 12, 2013"
    locator: the release of a small synthetic database for a class of finite VC dimension
  - paper: doi:10.1109/FOCS.2010.85
    title: "Moritz Hardt and Guy N. Rothblum, A multiplicative weights mechanism for privacy-preserving data analysis, FOCS 2010, pages 61 to 70"
    locator: private multiplicative weights, an online mechanism with error of order n to the minus 1/2
  - paper: "Jonathan Ullman, Answering n^(2+o(1)) counting queries with differential privacy is hard, STOC 2013, pages 361 to 370"
    locator: the hardness of efficient release for more than about n^2 arbitrary counting queries
---

Private query release asks for answers to every query in a large class $Q$, such as all counting queries over a universe or all marginals of a table, under [differential privacy](/differential-privacy-definition/). The answers must all be accurate at the same time, and the release must hide each row. If each query gets its own noise, the error grows with the number of queries, so a few thousand queries on a few thousand rows give nothing useful. Blum, Ligett and Roth (2008) showed that the error can grow only with the logarithm of $|Q|$ and of the universe size: release a small synthetic dataset, chosen privately, and answer every query from it. Lower bounds show the limits: no mechanism answers too many queries too well ([reconstruction](/dinur-nissim-reconstruction-attack/)), pure DP pays $\log|X|$ ([packing](/packing-lower-bound/)), and approximate DP pays about $\sqrt{|Q|}$ for $|Q|$ attribute means ([fingerprinting codes](/fingerprinting-codes-lower-bound/)). Efficient algorithms for every class do not exist under standard cryptographic assumptions.

**Notation.** $X$ is the data universe, $n$ the number of rows, $Q$ the query class, $\alpha$ the error and $\beta$ the failure probability. For $X = \{0,1\}^d$, $d$ is the number of binary attributes. $\mathrm{Lap}(b)$ has the density $(1/(2b))e^{-|z|/b}$, the variance $2b^2$ and $P(|Z| > t) = e^{-t/b}$.

## In plain words

A hospital wants to publish many statistics about its patients: how many are over 60, how many smoke, how many are over 60 and smoke, and so on, for every combination someone might ask. Each number must be close to the truth, and no number may give away a single patient.

If you add separate noise to each number, the noise must grow with the count of numbers, because together they say a lot. A better way is to build a small fake table of patients that gives nearly the right answer to every question, choose it with a private random process, and publish only the fake table. Then anyone can ask any question of the fake table. This works when the table has enough real rows. Some limits cannot be beaten: with too few rows, any table that answers all questions well also gives away the patients.

## Definition

**Data and privacy.** A dataset is $x \in X^n$. Two datasets are neighbors if they differ in one row (replace). A mechanism $M$ is $(\varepsilon, \delta)$-DP if $P[M(x) \in S] \le e^{\varepsilon} P[M(x') \in S] + \delta$ for all neighbors $x, x'$ and all sets $S$ of outputs.

**Queries.** A counting query is $q : X \to \{0,1\}$, with the answer $q(x) = \frac{1}{n}\sum_{i=1}^n q(x_i)$. A linear query has $q : X \to [0,1]$ in the same formula. The class $Q$ is public.

**Accuracy.** $M$ outputs a vector $(a_q)_{q \in Q}$, or a data structure that answers every $q \in Q$. It is $(\alpha, \beta)$-accurate for $Q$ if for every dataset $x$,

$$P\Big[\max_{q \in Q} |a_q - q(x)| \le \alpha\Big] \ge 1 - \beta.$$

**The problem.** Given $Q$, $X$, $n$, $\varepsilon$ and $\delta$, find an $(\varepsilon, \delta)$-DP mechanism with the least $\alpha$. The dual question is the sample complexity: the least $n$ for which error $\alpha$ is possible. A mechanism is efficient if it runs in time polynomial in $n$, $|Q|$ and $d = \log|X|$, not in $|X|$.

## Variants

- **Synthetic data.** The output is a dataset $\hat x \in X^m$, and $a_q = q(\hat x)$. This is the form of [SmallDB](/smalldb-mechanism/) and [MWEM](/mwem/), and the one users can load into normal tools.
- **Offline and online.** In the offline (non-interactive) form, $Q$ is fixed and all answers come at once. In the online form, an analyst picks each query after seeing the earlier answers, as in private multiplicative weights and the [sparse vector technique](/sparse-vector-technique/).
- **Linear workloads and other error measures.** For a workload matrix of linear queries, one may ask for small mean squared error and not the worst error, as in the [matrix mechanism](/matrix-mechanism/).
- **Special classes.** Point functions (a histogram), thresholds and ranges on an ordered universe, $t$-way marginals (conjunctions of $t$ attributes), and the attribute means $q_j(w) = w_j$.
- **Continual release.** Data arrive in a stream and the counts must be released at every step, as in the [binary tree mechanism](/binary-tree-mechanism/).
- **Neighbor relation.** With add or remove neighbors, $n$ is private and the answers are counts, not fractions. The bounds change by constant factors.

## Examples

**All 256 counting queries on 3 binary attributes.** Take $X = \{0,1\}^3$, so $|X| = 8$ cells, with $n = 1000$ rows, $\varepsilon = 1$ and $\delta = 0$. Every counting query is a set of cells, so $Q$ has $2^8 = 256$ queries. The numbers below come from the formula for the maximum of independent Laplace variables (theorems, not measurements).

| method | sensitivity in $\ell_1$ | noise | error bound with probability 0.95 |
|---|---|---|---|
| Laplace on all 256 answers | $128/n$ | $\mathrm{Lap}(0.128)$ each | 1.09 on the worst query |
| Laplace on the 8 cells, then add cells | $2/n$ | $\mathrm{Lap}(0.002)$ each | 0.0101 on each cell, so at most 0.081 on any query |

Replacing one row moves one unit of count from one cell to another. That changes the 128 queries that hold exactly one of the two cells, so the vector of 256 answers has $\ell_1$ sensitivity $128/n$, and the [Laplace mechanism](/laplace-mechanism/) on it is useless. The histogram has sensitivity $2/n$, and every query is a sum of at most 8 noisy cells. A query of 8 cells has the noise standard deviation $\sqrt{8 \cdot 2 \cdot 0.002^2} = 0.008$. The noisy histogram is itself synthetic data. This works because $|X|$ is small; for $X = \{0,1\}^d$ with large $d$ the histogram has $2^d$ cells and the methods below are needed.

**Reconstruction as a limit.** With $X = \{0,1\}$ and $Q$ all $2^n$ subsets of rows given by row identifiers, error below $1/40$ on every query lets anyone rebuild 90 percent of the bits (Vadhan Corollary 5.3). So query classes that refer to single rows cannot be released accurately. Classes that treat rows as a multiset, like counting queries on $X$, can.

## Known algorithms

The bounds are on the worst error $\alpha$ with high probability, from the sources (theorems).

| algorithm | privacy | error $\alpha$ | time |
|---|---|---|---|
| Laplace on each query (Vadhan Theorem 2.6) | $\varepsilon$ | $O(\lvert Q\rvert/(\varepsilon n))$ | $\mathrm{poly}(n, \lvert Q\rvert)$ |
| Gaussian on each query (Vadhan Theorem 2.7) | $(\varepsilon, \delta)$ | $O(\sqrt{\lvert Q\rvert \log(1/\delta) \log\log\lvert Q\rvert}/(\varepsilon n))$ | $\mathrm{poly}(n, \lvert Q\rvert)$ |
| Laplace histogram | $\varepsilon$ | $O(\lvert X\rvert \log\lvert X\rvert/(\varepsilon n))$ for any counting query | $\mathrm{poly}(n, \lvert X\rvert)$ |
| [SmallDB](/smalldb-mechanism/) (Blum, Ligett and Roth; Vadhan Theorem 4.1) | $\varepsilon$ | $O((\log\lvert Q\rvert \log\lvert X\rvert/(\varepsilon n))^{1/3})$ | $\lvert X\rvert^{O(\log\lvert Q\rvert/\alpha^2)}$ |
| Private multiplicative weights (Hardt and Rothblum; Vadhan Theorem 4.3) | $(\varepsilon, \delta)$ | $O((\sqrt{\log\lvert X\rvert \log(1/\delta)}\,\log\lvert Q\rvert/(\varepsilon n))^{1/2})$ | $\mathrm{poly}(n, \lvert X\rvert)$ per query |
| [MWEM](/mwem/) (Hardt, Ligett and McSherry) | $\varepsilon$ | of order $n^{-1/3}$, like SmallDB | $O(\lvert X\rvert)$ per round |
| [Matrix mechanism](/matrix-mechanism/) (Li et al.) | $\varepsilon$ or $(\varepsilon, \delta)$ | mean squared error set by a strategy matrix | a convex search over strategies |
| [Binary tree mechanism](/binary-tree-mechanism/) | $\varepsilon$ | $O(\log^{1.5} T/\varepsilon)$ in counts for prefix sums | $O(\log T)$ per step |

The first two rows pay a power of $|Q|$, and the SmallDB and multiplicative weights rows pay only $\log|Q|$, at the price of a lower power of $n$ and time polynomial in $|X|$. For a small universe the histogram is best. The Laplace histogram row uses the union bound over $|X|$ cells; for a query of $c$ cells the error is a sum of $c$ noise terms. Each method needs a cryptographic source of randomness and exact sampling in a deployment (Mironov 2012; Canonne, Kamath and Steinke 2020).

## Bounds

- **Reconstruction (Dinur and Nissim; Vadhan Theorems 5.2 and 5.6).** A class that refers to single rows cannot be released with error $o(1)$ on all $2^n$ queries, or error $o(1/\sqrt n)$ on $n$ random queries. See the [reconstruction theorems](/dinur-nissim-reconstruction-attack/).
- **Packing (Vadhan Theorems 5.13 to 5.15).** For pure DP and a class that tells all of $X$ apart, $\alpha \ge \Omega(\log|X|/(\varepsilon n))$, and the sample complexity for constant error is set by a packing number. See the [packing lower bound](/packing-lower-bound/).
- **Fingerprinting codes (Vadhan Theorems 5.21 and 5.22).** For $(\varepsilon, \delta)$-DP, $d$ attribute means need error $\Omega(\sqrt{d \log(1/\delta)}/(\varepsilon n))$, and some classes of $k$ queries with $n^{2.1} \le k$ need error $\tilde\Omega((\sqrt{\log|X|}\,\log|Q|/(\varepsilon n))^{1/2})$, close to private multiplicative weights. See the [fingerprinting code lower bound](/fingerprinting-codes-lower-bound/).
- **Running time.** Under cryptographic assumptions, some classes of counting queries on $X = \{0,1\}^d$ have no accurate private release in time polynomial in $n$ and $d$ (Dwork, Naor, Reingold, Rothblum and Vadhan, STOC 2009). Ullman (STOC 2013) shows that answering more than about $n^2$ arbitrary counting queries efficiently is hard, while the Gaussian mechanism answers about $n^2$ of them efficiently with constant error. Vadhan Section 6 (traitor-tracing lower bounds and lower bounds for synthetic data) surveys these results.

## Reductions

- **Synthetic data gives query release.** A synthetic dataset $\hat x$ answers every $q$ by $q(\hat x)$, by post-processing. For a small universe the converse holds with twice the error: a linear program finds the fractional histogram whose answers are nearest to the noisy answers in the worst query, and the true histogram is a candidate, so the result is within $2\alpha$ of the truth.
- **Small datasets suffice.** For every $x$ and every $Q$ of counting queries, a random sample of $m = O(\log|Q|/\alpha^2)$ rows of $x$ answers all of $Q$ within $\alpha$ (a Chernoff and union bound). So the search can be over datasets of $m$ rows, which is the base of SmallDB; for a class of finite [VC dimension](/vc-dimension/), $\log|Q|$ can be replaced by the VC dimension (Blum, Ligett and Roth).
- **Online from offline.** Private multiplicative weights uses the sparse vector technique to answer an online query only when the current synthetic data errs on it, and pays only for those updates.
- **Lower bounds from codes and attacks.** The lower bounds above reduce from reconstruction and from fingerprinting codes; the hardness results reduce from traitor-tracing schemes.

## Applications

- **Official statistics.** Agencies publish large sets of counts and marginal tables; query release is the model for formal privacy of such tables, and the reconstruction theorems explain why tables with exact counts are a risk.
- **Synthetic data for analysts.** A private synthetic dataset can be loaded into normal tools, and every later analysis is free by post-processing.
- **Range and prefix counts.** Dashboards of counts over time or over ranges use tree-based and matrix methods.
- **Learning.** Answers to all statistical queries of a class let a learner train in the [statistical query model](/statistical-query-model/) with no extra privacy cost.

## References
