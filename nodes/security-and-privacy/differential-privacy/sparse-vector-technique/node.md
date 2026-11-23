---
tag: QVW2C4
kind: algorithm
slug: sparse-vector-technique
name: Sparse vector technique
aliases:
- AboveThreshold
- SVT
area: security-and-privacy/differential-privacy
level: core
summary: Compares a stream of low-sensitivity queries with a noisy threshold and reports only which one is first above it. The privacy cost is paid only for the queries above the threshold.
model: real-ram
complexity:
  vars: {k: the number of queries asked, c: the cutoff (the number of tops allowed)}
  time: {worst: O(k)}
  space: {extra: O(1)}
history:
  year: 2009
  people: [Cynthia Dwork, Moni Naor, Omer Reingold, Guy N. Rothblum, Salil Vadhan]
  note: Dwork, Naor, Reingold, Rothblum and Vadhan introduced the technique at STOC 2009. Roth and Roughgarden and then Hardt and Rothblum refined it in 2010. Dwork and Roth gave the AboveThreshold form in 2014.
prereqs: [differential-privacy-definition, global-sensitivity, laplace-mechanism]
see_also: [report-noisy-max, exponential-mechanism, private-query-release, mwem, sequential-composition-theorem, advanced-composition-theorem, propose-test-release, dinur-nissim-reconstruction-attack]
sources:
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: Section 3.6, Algorithm 1 (AboveThreshold), Theorem 3.23 (privacy), Theorem 3.24 (accuracy), Algorithm 2 (Sparse) and Theorems 3.25 and 3.26, Algorithm 3 (NumericSparse) and Theorems 3.27 and 3.28
  - paper: arxiv:1603.01699
    title: "Min Lyu, Dong Su and Ninghui Li, Understanding the sparse vector technique for differential privacy, Proceedings of the VLDB Endowment 10(6), 2017, pages 637 to 648"
    locator: "Section 3 and Figures 1 and 2 (six variants; Algorithms 3 to 6 are not epsilon-DP, and Algorithms 3, 5 and 6 are not private for any finite epsilon); equation (12) (the budget split epsilon1 to epsilon2 as 1 to (2c)^(2/3))"
  - paper: "Cynthia Dwork, Moni Naor, Omer Reingold, Guy N. Rothblum and Salil Vadhan, On the complexity of differentially private data release, efficient algorithms and hardness results, STOC 2009, pages 381 to 390"
    locator: the first form of the sparse vector technique
  - paper: "Moritz Hardt and Guy N. Rothblum, A multiplicative weights mechanism for privacy-preserving data analysis, FOCS 2010, pages 61 to 70"
    locator: the use of the sparse vector technique to decide when to update the synthetic distribution
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012"
    locator: the attack on floating-point Laplace noise and the snapping defense
---

The sparse vector technique answers a long stream of threshold questions about a private dataset: "is the answer to this query above $T$?". It adds Laplace noise to the threshold once and to each query, and it stops at the first query whose noisy answer is above the noisy threshold. The surprise is that the queries below the threshold cost no privacy. The whole run is $\varepsilon$-differentially private, however many queries come before the first "yes". It is the base of the online query release algorithms, such as private multiplicative weights, and it is easy to get wrong: Lyu, Su and Li (2017) found that four of six published variants are not private.

## In plain words

You want to know which of many questions has a large answer, for example which of thousands of product counts is above a level. To answer each one with noise would cost privacy for each question. Most of the answers are "no", and each "no" says little.

The technique moves the level a little at random, one time. It also moves each answer a little at random. Then it goes down the list and reports "no" until one noisy answer clears the noisy level. It reports "yes" for that one and stops. If you need more than one "yes", you start again with a new random level and pay again. You pay for each "yes", and the "no" answers are free.

## The problem

The input is a dataset $x$, a threshold $T$, a privacy parameter $\varepsilon > 0$ and a stream of queries $f_1, f_2, \ldots$, each a function from datasets to $\mathbb{R}$. Each query has sensitivity at most $\Delta$: $|f_i(x) - f_i(x')| \le \Delta$ for all neighbors $x \sim x'$. Two datasets are neighbors if one is the other with one record added or removed (add/remove), as in Dwork and Roth, who use histograms with $\|x - x'\|_1 \le 1$. The proof uses only the sensitivity bound, so it holds for any neighbor relation under which each $f_i$ has sensitivity $\Delta$. The analyst may choose $f_i$ after it sees the earlier outputs.

The output is a sequence $a_1, a_2, \ldots, a_j$ with $a_i \in \{\bot, \top\}$: $\bot$ for "below", and $\top$ for "above". The goal is $\varepsilon$-DP for the whole sequence, and accuracy: each $\top$ is for a query with $f_i(x) \ge T - \alpha$, and each $\bot$ for a query with $f_i(x) \le T + \alpha$.

$\mathrm{Lap}(b)$ is the Laplace distribution with density $\frac{1}{2b} e^{-|z|/b}$. It has variance $2b^2$, and $P(|Z| > t) = e^{-t/b}$.

## The algorithm

This is AboveThreshold, Algorithm 1 of Dwork and Roth, with a general sensitivity $\Delta$ (they use $\Delta = 1$).

```pseudo id=main
ABOVE-THRESHOLD(x, f₁, f₂, ..., T, Δ, ε)
L1  T̂ ← T + Lap(2Δ/ε)                 ▷ one noisy threshold for the whole run
L2  for i ← 1, 2, ... do
L3      νᵢ ← Lap(4Δ/ε)                 ▷ fresh noise for each query
L4      if fᵢ(x) + νᵢ ≥ T̂ then
L5          output ⊤ and halt
L6      else output ⊥
```

Line L1 draws the threshold noise one time. Lines L3 and L4 compare a noisy answer with the noisy threshold. Line L5 halts at the first $\top$, and this is what keeps the cost at $\varepsilon$. The noisy values themselves are never output, only the comparison.

To allow $c$ tops, run AboveThreshold again after each $\top$, with a fresh noisy threshold. With $\varepsilon/c$ per run, basic composition gives $\varepsilon$-DP in total. This is Sparse, Algorithm 2 of Dwork and Roth, with noise $\mathrm{Lap}(\sigma)$ on the threshold and $\mathrm{Lap}(2\sigma)$ on each query, $\sigma = 2c\Delta/\varepsilon$. With advanced composition, $\sigma = \sqrt{32 c \ln(1/\delta)}\,\Delta/\varepsilon$ gives $(\varepsilon, \delta)$-DP.

## Example

Take $\varepsilon = 1$, $\Delta = 1$ and $T = 10$, so the threshold noise is $\mathrm{Lap}(2)$ and the query noise is $\mathrm{Lap}(4)$. The query answers are $f(x) = (3, 8, 6, 11, 14, 5)$. The run of the code with `random.Random(16)` draws $\hat T = 9.35$ in line L1, and the noise values below.

| step | $f_i(x)$ | $\nu_i$ | $f_i(x) + \nu_i$ | compare with $\hat T = 9.35$ | output |
|---|---|---|---|---|---|
| L1 | | | | $\hat T = 9.35$ | |
| $i = 1$ | 3 | $-0.16$ | 2.84 | below | $\bot$ |
| $i = 2$ | 8 | $-0.73$ | 7.27 | below | $\bot$ |
| $i = 3$ | 6 | $-0.45$ | 5.55 | below | $\bot$ |
| $i = 4$ | 11 | $-0.80$ | 10.20 | above | $\top$, halt |
| $i = 5$ | 14 | | | not asked | |
| $i = 6$ | 5 | | | not asked | |

The output is $(\bot, \bot, \bot, \top)$. Query 4 is above $T$ and it is reported. Query 5 is also above $T$, but the run halted. To find it too, use Sparse with $c = 2$. Theorem 3.24 with $k = 6$ and $\beta = 0.1$ gives $\alpha = 8(\ln 6 + \ln 20)/1 = 38.3$. So the guarantee at this $\varepsilon$ is weak for answers of size 10: the method needs large counts or a larger $\varepsilon$.

## Correctness

**Privacy (Dwork-Roth Theorem 3.23, a theorem).** For adaptively chosen queries of sensitivity $\Delta$, AboveThreshold is $(\varepsilon, 0)$-DP.

The key step: fix $x \sim x'$ and an output that halts at query $k$. Fix the noise $\nu_1, \ldots, \nu_{k-1}$, which the two runs share. Let $g(x) = \max_{i<k} (f_i(x) + \nu_i)$. The output is $(\bot^{k-1}, \top)$ exactly when $\hat T > g(x)$ and $f_k(x) + \nu_k \ge \hat T$. Shift the threshold noise by at most $\Delta$ and the query noise $\nu_k$ by at most $2\Delta$: this maps the good event on $x$ into the good event on $x'$. The densities change by at most $e^{\varepsilon/2}$ each, because the scales are $2\Delta/\varepsilon$ and $4\Delta/\varepsilon$. The full proof is in proofs/correctness.md.

**Accuracy (Dwork-Roth Theorem 3.24, a theorem).** Let $\alpha = 8\Delta(\ln k + \ln(2/\beta))/\varepsilon$. With probability at least $1 - \beta$, $|\hat T - T| \le \alpha/2$ and $|\nu_i| \le \alpha/2$ for all $i \le k$. On this event each $\top$ has $f_i(x) \ge T - \alpha$ and each $\bot$ has $f_i(x) < T + \alpha$. The theorem adds the condition that no query before the $k$-th has $f_i(x) \ge T - \alpha$, so that the run reaches query $k$.

## Complexity

In the [real-RAM model](/real-ram/) with one Laplace draw at unit cost:

- Each query costs one evaluation $f_i(x)$, one draw and one comparison. For $k$ queries the time is $O(k)$ plus the cost of the evaluations.
- The extra space is $O(1)$: the run keeps only $\hat T$.
- Sparse with cutoff $c$ draws at most $c$ thresholds, so it is still $O(k)$.

The privacy cost does not grow with $k$. This is the point of the technique. With the [Laplace mechanism](/laplace-mechanism/) on each query and [sequential composition](/sequential-composition-theorem/), the cost grows as $k\varepsilon$.

## Properties

- **Online and adaptive.** The queries may come one at a time, and each may depend on the earlier outputs.
- **Output only the comparison.** The noisy answers $f_i(x) + \nu_i$ stay inside. To publish a value for each $\top$, NumericSparse (Algorithm 3 of Dwork and Roth) spends a separate budget on a fresh Laplace answer.
- **Pure DP.** AboveThreshold and Sparse with $\delta = 0$ are $\varepsilon$-DP. Sparse with advanced composition is $(\varepsilon, \delta)$-DP.
- **Randomized.** The output for one dataset is a random variable. Repeated runs on the same data each cost $\varepsilon$.

## Variants and improvements

- **Sparse with cutoff $c$.** Halt after $c$ tops, with a fresh threshold after each $\top$ (Dwork-Roth Theorems 3.25 and 3.26). For $\delta = 0$ the accuracy is $\alpha = 8c\Delta(\ln k + \ln(2c/\beta))/\varepsilon$.
- **One threshold for $c$ tops.** Lyu, Su and Li prove that the threshold need not be refreshed: noise $\mathrm{Lap}(\Delta/\varepsilon_1)$ on the threshold and $\mathrm{Lap}(2c\Delta/\varepsilon_2)$ on each query, with $\varepsilon_1 + \varepsilon_2 = \varepsilon$, is $\varepsilon$-DP. The noise on the threshold then scales with $\Delta/\varepsilon_1$, not $c\Delta/\varepsilon$. Their analysis gives the split $\varepsilon_1 : \varepsilon_2 = 1 : (2c)^{2/3}$.
- **Monotone queries.** If all answers move in the same direction between neighbors, the query noise can be $\mathrm{Lap}(c\Delta/\varepsilon_2)$ (Lyu, Su and Li).
- **NumericSparse.** Also release a noisy value of each query above the threshold.
- **Private multiplicative weights.** Hardt and Rothblum use the technique to find the queries on which a synthetic dataset is wrong, and update only there. See [MWEM](/mwem/) for the offline relative.

## When to use it

Use the sparse vector technique when you expect few of many queries to be above a threshold, and the queries arrive online. Examples are finding the first large count, checking whether a public synthetic answer is still close to the true one, and the update test of online query release. If all queries are known in advance and you need the largest, use [report noisy max](/report-noisy-max/) or the [exponential mechanism](/exponential-mechanism/): Lyu, Su and Li show that in the non-interactive setting the exponential mechanism is more accurate. If most answers are above the threshold, the technique saves nothing.

## Pitfalls

- **No noise on the queries.** Dropping line L3 ($\nu_i = 0$) and not halting gives a mechanism that is not $\varepsilon$-DP for any $\varepsilon$. For counts $f_1$ of value 0 and $f_2$ of value 1, the data $(0)$ gives $(1, 0)$ and the neighbor $(0, 1)$ gives $(1, 1)$. The output $(\top, \bot)$ needs $f_1 \ge \hat T > f_2$, which has probability 0 on the neighbor. The test file checks this. The variant of Stoddard, Chen and Machanavajjhala has this error (Lyu, Su and Li, Algorithm 5).
- **Query noise that does not scale with $c$.** When one run allows $c$ tops, the query noise in line L3 must grow with $c$: $\mathrm{Lap}(2\sigma)$ with $\sigma = 2c\Delta/\varepsilon$ in Sparse. Lyu, Su and Li show that the variant of Lee and Clifton, with query noise that does not scale with $c$, is only $\frac{1 + 6c}{4}\varepsilon$-DP.
- **No cutoff.** Line L5 must halt, or Sparse must stop after $c$ tops. Without the cutoff, the variants of Stoddard et al. and of Chen et al. are not private for any finite $\varepsilon$ (Lyu, Su and Li, Figure 2).
- **Publishing the noisy answer.** Outputting $f_i(x) + \nu_i$ in line L5, in place of $\top$, is not private for any finite $\varepsilon$. The variant in Roth's 2011 lecture notes does this (Lyu, Su and Li, Algorithm 3). Use a fresh Laplace answer, as NumericSparse does.
- **Float noise.** The code uses float Laplace noise from `random.Random`, for tests only. A deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020); see the [discrete Gaussian mechanism](/discrete-gaussian-mechanism/).

## Implementations

## History

Dwork, Naor, Reingold, Rothblum and Vadhan introduced the technique at STOC 2009, in their work on efficient [private query release](/private-query-release/). Roth and Roughgarden (STOC 2010, the median mechanism) and Hardt and Rothblum (FOCS 2010, private multiplicative weights) refined it and used it to answer many queries online. The book of Dwork and Roth (2014) gave the AboveThreshold form used here. Lyu, Su and Li (PVLDB 2017) surveyed the published variants, showed that most of them are not private, and gave a corrected version with a better budget split.

## References
