---
tag: WNQFZC
kind: algorithm
slug: rappor
name: RAPPOR
aliases:
- randomized aggregatable privacy-preserving ordinal response
area: security-and-privacy/differential-privacy
level: advanced
summary: "Encodes each value into a Bloom filter and applies two stages of randomized response, so a server can estimate value frequencies over time."
model: word-ram
complexity:
  vars: {N: the number of reports, k: the bits of the Bloom filter, h: the hash functions, m: the cohorts, M: the candidate values}
  time: {worst: O(N k + k m M^2 + M^3)}
  space: {extra: O(k m M)}
properties: {deterministic: false, randomized: true}
history:
  year: 2014
  people: [Úlfar Erlingsson, Vasyl Pihur, Aleksandra Korolova]
  note: "Erlingsson, Pihur and Korolova described RAPPOR at ACM CCS 2014, with its use in the Chrome web browser to collect statistics on client settings."
prereqs: [local-differential-privacy, bloom-filter, randomized-response]
see_also: [optimized-local-hashing, post-processing-theorem, sequential-composition-theorem, privacy-amplification-by-shuffling, ordinary-least-squares, frequency-estimation, hash-function, geometric-mechanism]
sources:
  - url: "https://arxiv.org/abs/1407.6981"
    title: "Úlfar Erlingsson, Vasyl Pihur and Aleksandra Korolova, RAPPOR: randomized aggregatable privacy-preserving ordinal response, ACM CCS 2014, pages 1054 to 1067"
    locator: "the algorithm (Bloom filter, permanent and instantaneous randomized response), Theorem 1 (the bound epsilon_infinity), Theorem 2 (the bound for one report), and Section 4 (decoding with cohorts, Lasso and least squares)"
  - paper: "Tianhao Wang, Jeremiah Blocki, Ninghui Li and Somesh Jha, Locally differentially private protocols for frequency estimation, USENIX Security 2017, pages 729 to 745"
    locator: the comparison of basic RAPPOR with the other frequency oracles in the pure LDP framework
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: why the samplers of a deployment must be exact
---

RAPPOR is a local differential privacy method to collect strings, such as a browser setting, from many clients. Each client hashes its value into a [Bloom filter](/bloom-filter/) of $k$ bits. It then applies [randomized response](/randomized-response/) to each bit two times. The first time, the result is stored and reused for this value forever (the permanent step). The second time, fresh noise is added for each report (the instantaneous step). The permanent step limits what any number of reports of one value can leak to $\varepsilon_\infty$. The instantaneous step makes a single report leak much less, and makes two reports hard to link. The collector counts the ones per bit, removes the known bias, and fits the counts of a list of candidate strings by least squares. Erlingsson, Pihur and Korolova (2014) designed it for the Chrome web browser.

## In plain words

Each client turns its answer into a short row of bits. A few bits are on, chosen by hashing the answer. The client then lies about some of the bits, at random. It writes this lie down and keeps it. Each time the server asks, the client lies again about the written row, with new coins, and sends that.

Because the written row never changes for one answer, the server cannot remove the noise by asking many times. Because each report adds new noise, one report shows very little.

The server knows how often the coins lie. It adds up the reports from many clients, removes the expected share of lies, and finds which answers best explain the counts. This works for answers that many clients share. Rare answers stay hidden in the noise.

## The problem

There are $N$ clients. Client $u$ holds a value $v_u$ from a large set of strings that the collector does not know in advance. The collector wants the number of clients that hold each popular value. The data of each client must stay private from the collector, under the local model: the randomizer of one client, as a function of that client's value, must be $\varepsilon$-[LDP](/local-differential-privacy/). The neighbor relation is replace: two inputs of one client are two different values.

A client may report many times, for example once a day, about the same value. The privacy claim must hold for all these reports together, not only for one.

## The algorithm

The parameters are the filter size $k$, the number $h$ of hash functions, the number $m$ of cohorts, and three rational probabilities: $f \in (0, 1)$ for the permanent step and $0 \le p < q \le 1$ for the instantaneous step. Each client is in one fixed cohort $j$, and each cohort has its own $h$ hash functions $H_{j,1}, \ldots, H_{j,h}$ into $\{0, \ldots, k - 1\}$.

```pseudo id=main
REPORT(client, v)                         ▷ run by the client; memo is kept on the device
L1  if memo has no entry for v then
L2      B <- the k-bit Bloom filter of v: bit H_{j,t}(v) is 1 for t = 1, ..., h
L3      for each bit i: B'_i <- 1 w.p. f/2, 0 w.p. f/2, else B_i
L4      memo[v] <- B'
L5  B' <- memo[v]
L6  for each bit i: S_i <- 1 w.p. q if B'_i = 1, w.p. p if B'_i = 0
L7  return S

ESTIMATE(reports, candidates)             ▷ run by the collector
L8  c_{ji} <- the number of reports of cohort j with bit i set; N_j <- the reports of cohort j
L9  t_{ji} <- (c_{ji} - p* N_j) / ((1 - f)(q - p))
L10 X <- the km x M matrix: column v has a 1 at row (j, i) when bit i of v's filter in cohort j is 1
L11 a <- the least squares solution of X a = t
L12 return m a                            ▷ the cohorts are balanced
```

Lines L1 to L4 run only the first time a client sees the value $v$. Line L2 computes the Bloom filter $B$, which has at most $h$ ones. Line L3 is the permanent randomized response: each bit is forced to 1 or to 0 with probability $f/2$ each, and is kept otherwise. Line L4 stores the result $B'$ on the device. Lines L5 and L6 run for every report: they read $B'$ and send a fresh noisy copy $S$, where a 1 of $B'$ becomes a 1 with probability $q$ and a 0 becomes a 1 with probability $p$.

On the collector side, a reported bit is 1 with probability $q^* = \frac{f}{2}(p + q) + (1 - f)q$ when the true bit is 1, and $p^* = \frac{f}{2}(p + q) + (1 - f)p$ when it is 0. Line L9 inverts this, so that $t_{ji}$ estimates the number of clients of cohort $j$ whose filter has bit $i$ on. Line L10 builds the matrix of the candidate filters, and line L11 finds the candidate counts that best explain $t$. The paper first selects the candidates with the Lasso and then fits them by least squares, and it keeps only the candidates that pass a significance test. The code on this page has only the least squares step on a given list.

The coins of lines L3 and L6 use exact rational probabilities and one uniform integer per bit. The tests use a seeded generator so that each run repeats. A deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012).

## Example

Take $k = 8$, $h = 2$, one cohort, $f = 1/2$, $p = 1/2$ and $q = 3/4$. The code hashes the value "apple" to the bits 2 and 3, so $B = (0, 0, 1, 1, 0, 0, 0, 0)$. Line L3 draws $u$ from $\{0, 1, 2, 3\}$ for each bit: $u = 0$ forces a 1, $u = 1$ forces a 0, and $u \in \{2, 3\}$ keeps the bit. Line L6 draws from $\{0, 1, 2, 3\}$ and sends 1 below 3 when $B'_i = 1$, and draws from $\{0, 1\}$ and sends 1 below 1 when $B'_i = 0$.

| bit $i$ | $B_i$ (line L2) | draw of line L3 | $B'_i$ | draw of line L6 | $S_i$ |
|---|---|---|---|---|---|
| 0 | 0 | 2 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 2 | 1 |
| 2 | 1 | 3 | 1 | 0 | 1 |
| 3 | 1 | 1 | 0 | 0 | 1 |
| 4 | 0 | 2 | 0 | 1 | 0 |
| 5 | 0 | 3 | 0 | 0 | 1 |
| 6 | 0 | 1 | 0 | 1 | 0 |
| 7 | 0 | 2 | 0 | 1 | 0 |

The client stores $B' = (0, 1, 1, 0, 0, 0, 0, 0)$ and sends $S = (0, 1, 1, 1, 0, 1, 0, 0)$. The next report of "apple" skips lines L2 to L4 and draws only line L6 again.

These parameters give $q^* = 11/16 = 0.6875$ and $p^* = 9/16 = 0.5625$. The bound for all reports of one value is $\varepsilon_\infty = 2h\ln((1 - f/2)/(f/2)) = 4 \ln 3 = 4.3944$, and the bound for one report is $\varepsilon_1 = h \ln(q^*(1 - p^*)/(p^*(1 - q^*))) = 1.0743$. With $h = 4$ they grow to $8.7889$ and $2.1486$.

On the collector side, suppose that $N = 1000$ clients report and that 300 of them have bit 2 on. Then $\mathbb E[c] = 300 \cdot 0.6875 + 700 \cdot 0.5625 = 600$, and line L9 gives $t = (c - 562.5)/0.125$, which is 300 when $c = 600$. The standard deviation of $c$ is 15.39, so the standard deviation of $t$ is 123.1. A count of 300 among 1000 is only about 2.4 standard deviations from 0. RAPPOR needs many clients.

## Correctness

**Theorem (longitudinal privacy; Erlingsson, Pihur and Korolova, Theorem 1).** All the reports that a client sends about one value are together $\varepsilon_\infty$-LDP, with $\varepsilon_\infty = 2h \ln((1 - f/2)/(f/2))$, for any number of reports.

Two Bloom filters differ in at most $2h$ bits, and the ratio of the probabilities of $B'$ at each such bit is at most $(1 - f/2)/(f/2)$. Every report is a function of $B'$ and of fresh coins, so the [post-processing theorem](/post-processing-theorem/) carries the bound to all reports.

**Theorem (one report; their Theorem 2).** A single report is $\varepsilon_1$-LDP with $\varepsilon_1 = h \ln(q^*(1 - p^*)/(p^*(1 - q^*)))$.

**Theorem (unbiased counts).** For one report per client, $\mathbb E[t_{ji}]$ is the true number of clients of cohort $j$ whose filter has bit $i$ on. If every client holds a candidate, the cohorts are balanced and $X$ has independent columns, line L12 is an unbiased estimate of the true counts.

Both privacy bounds are tight for two values whose filters have $h$ ones each and no common one. The full proofs are in the correctness proof of this page. The tests check both bounds with exact fractions on all filters of 4 bits, and the two-report law against $\varepsilon_\infty$.

## Complexity

The model is the [word RAM](/word-ram/). A hash is counted as $O(1)$ word operations.

- **One report.** Line L2 costs $O(h + k)$, line L3 costs $O(k)$ and $k$ draws, and line L6 costs $O(k)$ and $k$ draws. So a report costs $O(h + k)$ time and at most $2k$ draws. The memo holds $k$ bits for each value that the client has reported.
- **Counting.** Line L8 reads $N$ reports of $k$ bits in $O(N k)$ time. Line L9 is $O(k m)$.
- **Fit.** Line L10 builds a $km \times M$ matrix with $O(m M (h + k))$ work. The normal equations cost $O(k m M^2)$ to form and $O(M^3)$ to solve. So the collector runs in $O(N k + k m M^2 + M^3)$ time and $O(k m M)$ extra space.

## Properties

- **Two levels of privacy.** The permanent bits protect against an observer who collects every report for a long time. The instantaneous bits protect a single report much more: $\varepsilon_1 = 1.0743$ against $\varepsilon_\infty = 4.3944$ in the example.
- **Per value, not per client.** The bound $\varepsilon_\infty$ holds for one value. A client whose value changes gets a new $B'$ for each new value, and the losses add up by [sequential composition](/sequential-composition-theorem/). Values that change in a correlated way can leak more than one value's worth.
- **Unbiased, with a large variance.** The variance of $t_{ji}$ is about $N p^*(1 - p^*)/((1 - f)^2(q - p)^2)$. Only values held by a large share of the clients can be found.
- **Unknown domain.** The collector needs only a list of candidate strings at decoding time, not before collection. Strings that are not on the list are not found, and they bias the fit.
- **Cohorts.** Different hash functions per cohort reduce the chance that two candidates collide in every cohort, so that $X$ has independent columns.

## Variants and improvements

- **One-time RAPPOR.** If each client reports only once, the instantaneous step can be left out, and the report is $B'$ itself, with the loss $\varepsilon_\infty$ (Erlingsson, Pihur and Korolova).
- **Basic RAPPOR.** For a small known domain, $h = 1$ and one bit per value (a one-hot code) remove the hash collisions. Wang, Blocki, Li and Jha (2017) analyze this case as a frequency oracle.
- **Optimized local hashing.** For one report per client, [optimized local hashing](/optimized-local-hashing/) has a smaller variance than basic RAPPOR in most settings, and its report is $O(\log n)$ bits, not $k$.
- **Shuffling.** Mixing the reports of many clients before the collector reads them gives central DP with a smaller $\varepsilon$ ([privacy amplification by shuffling](/privacy-amplification-by-shuffling/)).
- **Unknown strings.** Fanti, Pihur and Erlingsson (2016) extended RAPPOR to learn the strings themselves, without a candidate list, by reporting several parts of each string and learning which parts occur together.

## When to use it

Use RAPPOR when the collector is not trusted, the clients are many (at least tens of thousands), and each client reports the same slowly changing value many times. The permanent step is the reason to choose it over a plain local frequency oracle. For one report per client over a known domain, optimized local hashing gives a smaller error. If a trusted curator is available, the [geometric mechanism](/geometric-mechanism/) on each count gives an error that is smaller by a factor of about $\sqrt N$.

## Pitfalls

- **No memo.** Lines L1 to L5 replaced by a fresh line L3 for each report give a new $B'$ each time. The collector can average the reports and recover $B$, and the loss grows with the number of reports. Line L3 must run once per value, and line L4 must store the result on the device.
- **A new cohort for each report.** If line L2 uses a new random cohort for each report, the filter changes, and so does $B'$. Each report then spends $\varepsilon_\infty$ again. The cohort of a client must stay fixed.
- **The wrong correction.** Line L9 with $p N_j$ in place of $p^* N_j$, or a division by $q - p$ in place of $(1 - f)(q - p)$, gives biased counts. Line L9 must use the two-stage values.
- **Float coins.** Lines L3 and L6 written as "random float below $f/2$" give probabilities that differ a little from the analysis. The coins must compare a uniform integer with the numerator of an exact fraction.
- **A short candidate list.** Line L11 on a list that misses a popular value spreads its counts over the other candidates. The paper first selects candidates with the Lasso and tests the fitted counts for significance; skip that step only when the list is known to be complete.

## Implementations

## History

Erlingsson, Pihur and Korolova presented RAPPOR at ACM CCS 2014. Google used it in the Chrome web browser to collect statistics on settings such as the home page, and published an open source version. It was one of the first large deployments of local differential privacy. Fanti, Pihur and Erlingsson (2016) extended it to strings that are not known in advance. Wang, Blocki, Li and Jha (2017) placed its basic form in a common framework of frequency oracles and showed that optimized local hashing has a smaller variance for one report.

## References
