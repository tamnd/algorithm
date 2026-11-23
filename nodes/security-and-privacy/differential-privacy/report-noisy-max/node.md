---
tag: GKS5RH
kind: algorithm
slug: report-noisy-max
name: Report noisy max
aliases:
- noisy argmax
area: security-and-privacy/differential-privacy
level: core
summary: Adds independent Laplace or exponential noise to each candidate's count and reports only the index of the largest.
model: real-ram
complexity:
  vars: {m: the number of scores}
  time: {worst: O(m)}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true}
history:
  year: 2014
  people: [Cynthia Dwork, Aaron Roth]
  note: Dwork and Roth present report noisy max with Laplace noise and its privacy proof in their 2014 monograph, next to the exponential mechanism.
prereqs: [laplace-mechanism, global-sensitivity]
see_also: [exponential-mechanism, gumbel-max-trick, sparse-vector-technique, pate, mwem, union-bound, post-processing-theorem, geometric-mechanism]
sources:
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 3.3, the Report Noisy Max algorithm and Claim 3.9 (privacy); Section 3.4, the definition of a monotonic function, Theorem 3.13 (report one-sided noisy arg-max) and Remark 3.1 (Gumbel noise)"
  - paper: doi:10.1109/FOCS.2007.66
    title: "Frank McSherry and Kunal Talwar, Mechanism design via differential privacy, FOCS 2007, pages 94 to 103"
    locator: the exponential mechanism, the other standard tool for private selection
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: why float Laplace noise is not enough for a release
---

Report noisy max selects the best of $m$ candidates privately. It adds independent [Laplace](/laplace-mechanism/) noise to the score of each candidate, such as a count, and releases only the index of the largest noisy score. For counts under add/remove neighbors, noise of scale $1/\varepsilon$ makes the index $\varepsilon$-[differentially private](/differential-privacy-definition/), although $m$ noisy counts released in full would cost $m\varepsilon$. Dwork and Roth (2014) give it with this proof. It is one of the two standard tools for private selection, next to the [exponential mechanism](/exponential-mechanism/).

## In plain words

You count the votes for each of several options and want to name the winner without revealing any one vote. You add a little random noise to each count, compare the noisy counts, and say only which option won. You do not show the noisy counts.

Showing all the noisy counts would need much more noise, because every count can leak something. But the winner is only one piece of information. One vote can help only one option, and it can help it by at most one. So the chance that a given option wins changes by at most a small factor when one voter leaves.

## The problem

The input is a list of $m$ scores $c_1(x), \ldots, c_m(x)$ that depend on a dataset $x$, a number $\Delta$ and a privacy parameter $\varepsilon > 0$. Each score has sensitivity at most $\Delta$: $|c_i(x) - c_i(x')| \le \Delta$ for all $i$ and all neighbors $x \sim x'$. The page uses add/remove neighbors unless it says otherwise.

The scores are **monotone** under a neighbor relation if, for every pair $x \sim x'$, either $c_i(x) \le c_i(x')$ for all $i$, or $c_i(x) \ge c_i(x')$ for all $i$. Counts are monotone under add/remove, because a new record never lowers a count. Under replace, one count can rise while another falls, so counts are not monotone there.

The output is one index $i \in \{1, \ldots, m\}$. The map from $x$ to the distribution of the index must be $\varepsilon$-DP, and the score of the chosen index must be close to $\max_j c_j(x)$.

## The algorithm

```pseudo id=main
REPORT-NOISY-MAX(c_1, ..., c_m, epsilon, Delta, monotone)   ▷ each c_i has sensitivity <= Delta
L1  b <- Delta / epsilon if monotone else 2 Delta / epsilon
L2  best <- -infinity; best_i <- none
L3  for i <- 1 to m do
L4      y <- c_i + a fresh sample of Lap(b)
L5      if y > best then best <- y; best_i <- i
L6  return best_i                              ▷ the noisy scores are never released
```

Line L1 sets the scale of the noise. Line L4 reads the score of candidate $i$, and the scores are the only input that depends on the data. The Laplace sample of line L4 is drawn by [inverse transform sampling](/inverse-transform-sampling/), as on the Laplace mechanism page. Line L5 keeps the largest noisy score seen so far. Ties have probability 0 in the real RAM; the code gives a tie to the lower index. Line L6 releases only the index. The noisy values $y$ and the noise are not published, and the privacy proof depends on that.

The code on this site uses floats and a seeded pseudorandom generator, so that the tests can repeat each run. A deployment needs a cryptographic source of randomness and an exact sampler (Mironov 2012).

## Example

The candidates are $A$, $B$ and $C$, and their vote counts are $c = (4, 2, 3)$. Counts have sensitivity $\Delta = 1$ and are monotone under add/remove. With $\varepsilon = 1$, line L1 gives $b = 1$. Assume that the Laplace sampler of line L4 draws its uniform value $u$ in $(-1/2, 1/2)$ as $0.3$, $-0.1$ and $0.45$, which gives the noise $-\mathrm{sgn}(u)\ln(1 - 2|u|)$.

| step | $i$ | $c_i$ | noise | $y$ (line L4) | best, best_i (line L5) |
|---|---|---|---|---|---|
| L1, L2 | | | | | $b = 1$; $-\infty$, none |
| L3 to L5 | 1 | 4 | 0.916291 | 4.916291 | 4.916291, 1 |
| L3 to L5 | 2 | 2 | $-0.223144$ | 1.776856 | 4.916291, 1 |
| L3 to L5 | 3 | 3 | 2.302585 | 5.302585 | 5.302585, 3 |
| L6 | | | | | return 3 |

The output is $C$, the second best candidate, because its noise was large. Over all noise, the exact output distribution is $(0.671265, 0.082510, 0.246225)$. A new vote for $A$ gives the add/remove neighbor with counts $(5, 2, 3)$ and the distribution $(0.833750, 0.042318, 0.123932)$. The log ratios of the two distributions are $-0.217$, $0.668$ and $0.687$, all at most $\varepsilon = 1$. For comparison, the exponential mechanism with $c = 1$ on the same counts gives $(0.665241, 0.090031, 0.244728)$, which is close but not equal.

The accuracy theorem below with $\beta = 0.1$ says that, with probability at least 0.9, the chosen count is at least $4 - 2\ln 30 = 4 - 6.802395$. With only three candidates this bound says nothing. With counts in the thousands it says that the chosen count is within about 7 of the largest.

## Correctness

**Theorem (privacy; Dwork-Roth Claim 3.9).** If every score has sensitivity at most $\Delta$ and the scores are monotone, then REPORT-NOISY-MAX with $b = \Delta/\varepsilon$ is $\varepsilon$-DP. Without the monotone condition, $b = 2\Delta/\varepsilon$ is enough.

The key step fixes the noise $r_{-i}$ of all candidates except $i$. For neighbors with $c_j(x') \le c_j(x) \le c_j(x') + \Delta$ for all $j$, let $r^*$ be the smallest noise of $i$ for which $i$ wins on $x'$. Then any noise $r_i \ge r^* + \Delta$ makes $i$ win on $x$:

$$c_i(x) + r_i \ge c_i(x') + r^* + \Delta > c_j(x') + r_j + \Delta \ge c_j(x) + r_j \quad \text{for all } j \ne i.$$

The Laplace density with scale $\Delta/\varepsilon$ changes by at most the factor $e^{\varepsilon}$ under a shift by $\Delta$, so $\Pr[i \text{ wins on } x \mid r_{-i}] \ge e^{-\varepsilon}\Pr[i \text{ wins on } x' \mid r_{-i}]$. The same argument with $x$ and $x'$ swapped gives the other direction, and the average over $r_{-i}$ gives the claim. Without monotone scores, the shift must be $2\Delta$, which is why line L1 doubles the scale. Dwork and Roth prove the case of counts under add/remove. The full proof, for any $\Delta$ and both cases, is in the correctness proof of this page.

**Theorem (accuracy).** For $0 < \beta < 1$, with probability at least $1 - \beta$, the chosen index $i$ has $c_i \ge \max_j c_j - 2b\ln(m/\beta)$. The proof is a [union bound](/union-bound/) over the $m$ tails $\Pr[|Z| > t] = e^{-t/b}$: if every noise is at most $b\ln(m/\beta)$ in absolute value, the winner cannot be more than twice that below the best.

## Complexity

The model is the [real RAM](/real-ram/): a uniform real number, a logarithm and a comparison each cost one step. The cost is counted after the $m$ scores are computed.

- **Time.** The loop of line L3 runs $m$ times, and each pass draws one Laplace sample and does one comparison. So the time is $O(m)$ in the worst case.
- **Space.** The loop keeps the best value and its index, and each noise is used once and dropped. So the extra space is $O(1)$, and the scores can come one at a time from a stream.

## Properties

- **Pure privacy for one index.** The index is $(\varepsilon, 0)$-DP, at the cost of one noisy count and not $m$. The tests compute the exact output distribution by numerical integration on every dataset of at most 3 records over 3 values. For counts under add/remove with $b = 1/\varepsilon$, the largest log ratio is 0.910 for $\varepsilon = 1$ and 0.428 for $\varepsilon = 0.5$ (a measurement on the test data).
- **Utility that grows like $\ln m$.** The chosen score is within $O(b\ln m)$ of the best with high probability, and this does not depend on the size of the dataset.
- **Not the exponential mechanism.** Laplace noise gives a different distribution from the exponential mechanism, although the guarantees are similar (Dwork-Roth Remark 3.1). Gumbel noise in line L4, with the scores scaled as in the exponential mechanism, gives exactly the exponential mechanism.
- **Closed under post-processing.** Any map of the index that does not read $x$ keeps $\varepsilon$-DP, by the [post-processing theorem](/post-processing-theorem/).

## Variants and improvements

- **One-sided exponential noise.** Report one-sided noisy arg-max adds noise from the exponential distribution with parameter $\varepsilon/\Delta$ for monotone scores and $\varepsilon/(2\Delta)$ otherwise (Dwork-Roth Section 3.4 and Theorem 3.13). The noise is never negative, so a bad candidate needs a large draw to win.
- **Gumbel noise.** Gumbel noise gives the [exponential mechanism](/exponential-mechanism/) exactly, by the [Gumbel max trick](/gumbel-max-trick/).
- **Integer counts.** For integer scores, a discrete noise such as that of the [geometric mechanism](/geometric-mechanism/) avoids floats, but then ties have positive probability and need a fixed rule.
- **Inside larger algorithms.** [PATE](/pate/) uses a noisy max of the votes of teacher models to label each query. The [sparse vector technique](/sparse-vector-technique/) uses a similar argument for the first query above a noisy threshold. [MWEM](/mwem/) needs one selection per round, done by the exponential mechanism or by report noisy max.

## When to use it

Use report noisy max to choose the best of a moderate number of candidates whose scores are counts or other low-sensitivity numbers, when only the identity of the best is needed. It is simple, it streams, and the proof is short. If the utility is not a sum of simple counts, or the candidate set is very large and structured, use the exponential mechanism, which also allows any base measure. If you need the value of the best score as well, use a second, separate query.

## Pitfalls

- **Releasing the noisy score.** The privacy proof covers only the index. Publishing the largest noisy value, or all noisy values, is not covered. To publish the score of the winner, answer it with a fresh Laplace query and pay for it by the [sequential composition theorem](/sequential-composition-theorem/).
- **The wrong neighbor relation.** Counts are not monotone under replace. With $b = 1/\varepsilon$, the tests measure a largest log ratio of 1.556 for $\varepsilon = 1$ under replace, so it is not $1$-DP there. With $b = 2/\varepsilon$ the measured value is 0.706.
- **Scores that are not monotone.** A score such as the error of a query, or a count minus another count, can move in both directions between neighbors. Then line L1 must use $2\Delta/\varepsilon$.
- **Candidates that depend on the data.** The list of candidates must be fixed in advance. A list built from the values that occur in $x$ leaks those values.
- **Float noise.** Line L4 on floats with a non-cryptographic generator is fine for study, but not for a release.

## Implementations

## History

Dwork and Roth (2014) present report noisy max with Laplace noise in Section 3.3 of their monograph and prove that it is $\varepsilon$-DP for counts. In Section 3.4 they define monotone utilities, give the one-sided exponential variant, and remark that Gumbel noise gives the exponential mechanism of McSherry and Talwar (2007). Later algorithms, such as PATE for private machine learning, use report noisy max as their selection step.

## References
