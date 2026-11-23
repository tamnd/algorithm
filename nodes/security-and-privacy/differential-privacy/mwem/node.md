---
tag: R361Z0
kind: algorithm
slug: mwem
name: Multiplicative weights exponential mechanism
aliases:
- MWEM
area: security-and-privacy/differential-privacy
level: advanced
summary: Keeps a synthetic histogram, picks a badly answered query with the exponential mechanism, measures it with Laplace noise and corrects the histogram by multiplicative weights.
model: real-ram
complexity:
  vars: {T: the number of rounds, Q: the query set, N: the size of the data domain}
  time: {worst: "O(T |Q| N)"}
  space: {extra: "O(N + |Q|)"}
history:
  year: 2012
  people: [Moritz Hardt, Katrina Ligett, Frank McSherry]
  note: Hardt, Ligett and McSherry gave MWEM at NIPS 2012, as a simple and practical form of the private multiplicative weights of Hardt and Rothblum (2010).
prereqs: [differential-privacy-definition, laplace-mechanism, exponential-mechanism, sequential-composition-theorem, multiplicative-weights-update, kullback-leibler-divergence]
see_also: [private-query-release, smalldb-mechanism, sparse-vector-technique, matrix-mechanism, report-noisy-max, histogram, fingerprinting-codes-lower-bound, binary-tree-mechanism]
sources:
  - paper: arxiv:1012.4763
    title: "Moritz Hardt, Katrina Ligett and Frank McSherry, A simple and practical algorithm for differentially private data release, NIPS 2012"
    locator: "Figure 1 (the algorithm), Theorem 2.1 (privacy), Theorem 2.2 (error), Corollary 2.1, Section 2.3.3 (improvements: output A_T and reuse past measurements)"
  - paper: "Moritz Hardt and Guy N. Rothblum, A multiplicative weights mechanism for privacy-preserving data analysis, FOCS 2010, pages 61 to 70"
    locator: the private multiplicative weights mechanism and the relative entropy argument
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014"
    locator: Section 4.2 (the online multiplicative weights mechanism)
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012"
    locator: the attack on floating-point Laplace noise and the snapping defense
---

MWEM builds a private synthetic histogram that answers a set of counting queries. It starts from the uniform histogram and runs $T$ rounds. In each round it uses the [exponential mechanism](/exponential-mechanism/) to pick a query on which the synthetic data is far from the real data, measures that one query with the [Laplace mechanism](/laplace-mechanism/), and moves the synthetic histogram toward the measurement by a [multiplicative weights](/multiplicative-weights-update/) step. The result is $\varepsilon$-differentially private, and its error grows with $\log |Q|$ and $\log |D|$, not with the number of queries. It is the practical form of the multiplicative weights approach to [private query release](/private-query-release/).

## In plain words

You want a fake table of counts that gives nearly the same answers as the real table, for many questions at once. You start with a flat fake table. Then you repeat a few times: find a question where the fake table is badly wrong, ask the real table that one question with noise, and fix the fake table so that it agrees better with the noisy answer. The fix raises the counts that the question covers if the fake answer is too low, and lowers them if it is too high.

The search for a bad question and the noisy answer each use a small part of the privacy budget. Only a few questions are asked, so each can have little noise. All other questions are answered by the fake table for free.

## The problem

The data is a histogram $B$ over a finite domain $D$ of size $N$, with $n$ records. The number $n$ is public. A counting query is a vector $q \in \{0, 1\}^D$, and its answer on a histogram $H$ is $q(H) = \sum_x q(x) H(x)$. Given a set $Q$ of queries, the goal is a synthetic histogram $\bar A$ with total $n$ that makes $\max_{q \in Q} |q(\bar A) - q(B)|$ small, under $\varepsilon$-DP. Two datasets are neighbors if one record is replaced by another (replace, so $n$ stays the same); then each $q(B)$ moves by at most 1. Hardt, Ligett and McSherry use add/remove neighbors and treat $n$ as known.

$\mathrm{Lap}(b)$ is the Laplace distribution with density $\frac{1}{2b} e^{-|z|/b}$. It has variance $2b^2$, and $P(|Z| > t) = e^{-t/b}$.

## The algorithm

```pseudo id=main
MWEM(B, Q, T, ε)
L1  A₀ ← the uniform histogram over D with total n
L2  for i ← 1 to T do
L3      pick qᵢ ∈ Q with probability ∝ exp(ε |q(Aᵢ₋₁) − q(B)| / (4T))   ▷ exponential mechanism, ε/(2T)
L4      mᵢ ← qᵢ(B) + Lap(2T/ε)                                          ▷ Laplace mechanism, ε/(2T)
L5      Aᵢ(x) ∝ Aᵢ₋₁(x) · exp(qᵢ(x) (mᵢ − qᵢ(Aᵢ₋₁)) / (2n)), scaled to total n
L6  output Ā ← (1/T) Σ_{i=0}^{T−1} Aᵢ
```

Line L3 is the exponential mechanism with budget $\varepsilon/(2T)$ and score $|q(A_{i-1}) - q(B)|$, which has sensitivity 1. Line L4 spends the other $\varepsilon/(2T)$ of the round on one noisy count. Line L5 raises the weight of each cell in $q_i$ if the measurement is above the synthetic answer, and lowers it if it is below. Line L6 averages the histograms that the rounds start from, as in Figure 1 of the paper. In their experiments the authors output the last histogram $A_T$ in place of the average; both are post-processing of the same run.

## Example

Take the domain of 8 cells, the data $B = (500, 1200, 3000, 2600, 1500, 800, 300, 100)$ with $n = 10000$, the 36 range queries over the cells, $\varepsilon = 1$ and $T = 5$. Each round spends $0.1$ on the selection and $0.1$ on the measurement, so the measurement noise is $\mathrm{Lap}(10)$. The uniform start puts 1250 in each cell, and its worst range error is 3350. The run of the code with `random.Random(1)`, rounded:

| round $i$ | worst error of $A_{i-1}$ | chosen range | $q_i(A_{i-1})$ | $q_i(B)$ | $m_i$ | $A_i$ |
|---|---|---|---|---|---|---|
| 1 | 3350 | cells 3 to 5 | 3750 | 7100 | 7111.9 | (1170, 1170, 1384, 1384, 1384, 1170, 1170, 1170) |
| 2 | 2979 | cells 2 to 5 | 5321 | 8300 | 8293.3 | (1078, 1251, 1479, 1479, 1479, 1078, 1078, 1078) |
| 3 | 2662 | cells 3 to 5 | 4438 | 7100 | 7098.9 | (1014, 1176, 1590, 1590, 1590, 1014, 1014, 1014) |
| 4 | 2445 | cells 2 to 4 | 4355 | 6800 | 6808.6 | (959, 1258, 1700, 1700, 1504, 959, 959, 959) |
| 5 | 2199 | cells 3 to 4 | 3401 | 5600 | 5571.3 | (923, 1211, 1824, 1824, 1448, 923, 923, 923) |

In each round the chosen range is the worst one: here the exponential mechanism put between 0.52 and 0.92 of its mass on it. The step in line L5 is small, because $\eta = (m_i - q_i(A_{i-1}))/(2n)$ is at most about $0.17$ here. The worst error of the average $\bar A$ is 2697 and that of the last histogram $A_5$ is 2004. More rounds help on this data (a measurement from the same code): with $T = 10, 20, 40$ the worst error of $A_T$ is 1332, 741 and 455, and that of the average is 2189, 1579 and 1085. Theorem 2.2 gives the bound 13077 for $T = 5$, which is larger than $n$. The bound is for the worst case, and MWEM does much better on this data.

## Correctness

**Privacy (Hardt-Ligett-McSherry Theorem 2.1, a theorem).** Each round makes two releases, each $\varepsilon/(2T)$-DP given the earlier ones: the selection in line L3, whose score has sensitivity 1 because $A_{i-1}$ depends only on earlier releases, and the noisy count in line L4. By adaptive [sequential composition](/sequential-composition-theorem/) the $2T$ releases are $\varepsilon$-DP, and line L6 is post-processing.

**Accuracy (Hardt-Ligett-McSherry Theorem 2.2, a theorem).** With probability at least $1 - 2T/|Q|$,

$$\max_{q \in Q} |q(\bar A) - q(B)| \le 2n\sqrt{\frac{\ln N}{T}} + \frac{10\, T \ln |Q|}{\varepsilon}.$$

The invariant is a potential: the [relative entropy](/kullback-leibler-divergence/) $\Psi_i$ from $B/n$ to $A_i/n$. It starts at most $\ln N$ and stays at least 0. Each update lowers it by at least $((q_i(A_{i-1}) - q_i(B))^2 - \nu_i^2)/(4n^2)$, where $\nu_i$ is the noise of line L4. So the errors of the chosen queries are small on average, and the exponential mechanism makes the chosen errors close to the worst errors. The full proofs are in proofs/correctness.md. Choosing $T$ to balance the two terms gives the error $O(n^{2/3} (\log N \log |Q| / \varepsilon)^{1/3})$ (Corollary 2.1).

## Complexity

In the [real-RAM model](/real-ram/), with one Laplace draw and one exponential at unit cost:

- Each round evaluates all $|Q|$ queries on $A_{i-1}$ in $O(|Q| N)$ time, samples in $O(|Q|)$, and updates in $O(N)$.
- $T$ rounds cost $O(T |Q| N)$, and the extra space is $O(N + |Q|)$.

The paper states the time as $O(n|Q| + T|D||Q|)$, with $O(n|Q|)$ for the true answers from the records. The cost is linear in the domain size $N = |D|$, which is exponential in the number of attributes. This is the main limit of MWEM. Ullman and Vadhan show that some limit of this kind is needed for efficient private synthetic data, under hardness assumptions.

## Properties

- **Synthetic data.** The output is a histogram, so it answers any query, also queries outside $Q$, and its answers are consistent.
- **Pure DP.** The run is $(\varepsilon, 0)$-DP. With advanced composition it is $(\varepsilon', \delta)$-DP with a different choice of $T$.
- **Data dependent error.** The error depends on the data. The bound of Theorem 2.2 is for the worst case, and on structured data the error is often much smaller.
- **Randomized.** The selection and the measurement are random, so two runs give different outputs, and each run costs $\varepsilon$.

## Variants and improvements

- **Last iterate.** Output $A_T$ in place of the average. The authors use this in all their experiments (Section 2.3.3).
- **Reuse of measurements.** After each new measurement, apply the update of line L5 again for all earlier pairs $(q_j, m_j)$. This uses no new privacy budget, because it only reads the releases, and it speeds up the fit a lot.
- **Better start.** Start from a noisy histogram of the frequent cells in place of the uniform one, at some cost in budget.
- **Online form.** Private multiplicative weights (Hardt and Rothblum 2010) answers queries as they come, and uses the [sparse vector technique](/sparse-vector-technique/) to find the queries on which the synthetic data is wrong.
- **Larger domains.** Later methods replace the explicit histogram over $D$ by a model with fewer parameters, so that the cost is no longer linear in $N$.

## When to use it

Use MWEM when you must release synthetic data or answer a large fixed set of counting queries, such as range queries or low-order marginals, and the domain is small enough to store a weight for each cell. It is easy to implement and it adapts to the data. For a small set of linear queries with a known structure, the [matrix mechanism](/matrix-mechanism/) has a data independent error that you can compute in advance. For a very large domain, MWEM as written is too slow.

## Pitfalls

- **Score with the wrong sensitivity.** Line L3 must use the budget $\varepsilon/(2T)$ in the form $\exp(\varepsilon_0 s/2)$, here $\exp(\varepsilon s/(4T))$, because the score has sensitivity 1. Using $\exp(\varepsilon s/(2T))$ spends twice the budget in each selection. For queries with values in $[-1, 1]$ under replace neighbors, the sensitivity is 2 and the exponent must be halved again.
- **Noise of the wrong scale.** Line L4 must use $\mathrm{Lap}(2T/\varepsilon)$, not $\mathrm{Lap}(1/\varepsilon)$. Each of the $T$ measurements spends $\varepsilon/(2T)$.
- **Private $n$.** Line L5 divides by $n$. If $n$ is private, as under add/remove neighbors, the update reads private data outside the budget. Treat $n$ as public, or spend part of the budget on a noisy $n$.
- **Selection that reads the true answers without noise.** The search for the worst query must go through line L3. Picking the exact worst query, as non-private multiplicative weights does, is not private.
- **Too many rounds.** A large $T$ makes each measurement very noisy. The bound shows the trade-off: the first term falls as $1/\sqrt{T}$ and the second grows as $T$.
- **Float noise.** The code uses float noise from `random.Random`, for tests only. A deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020); see the [discrete Gaussian mechanism](/discrete-gaussian-mechanism/).

## Implementations

## History

Blum, Ligett and Roth (2008) showed that a small synthetic database can answer exponentially many counting queries privately; see the [SmallDB mechanism](/smalldb-mechanism/). Their method takes time exponential in the domain size. Hardt and Rothblum (FOCS 2010) gave private multiplicative weights, an online method with a relative entropy analysis and near optimal error. Hardt, Ligett and McSherry (NIPS 2012) gave MWEM, a simple offline form that combines the exponential mechanism, the Laplace mechanism and multiplicative weights, and showed that it works well on real data.

## References
