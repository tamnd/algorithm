---
tag: 3V0287
kind: algorithm
slug: smalldb-mechanism
name: SmallDB mechanism
aliases:
- BLR mechanism
- Blum-Ligett-Roth mechanism
area: security-and-privacy/differential-privacy
level: advanced
summary: Picks a small synthetic database with the exponential mechanism. It answers a huge set of counting queries, with an error that grows only with the log of their number.
model: real-ram
complexity:
  vars: {U: the size of the data universe, m: the size of the small databases, Q: the query set}
  time: {worst: "O(U^(m+1) |Q|)"}
  space: {extra: O(U^m)}
history:
  year: 2008
  people: [Avrim Blum, Katrina Ligett, Aaron Roth]
  note: Blum, Ligett and Roth gave the mechanism at STOC 2008. It was the first to answer exponentially many counting queries with useful error under differential privacy.
prereqs: [differential-privacy-definition, exponential-mechanism, hoeffding-inequality, union-bound]
see_also: [mwem, private-query-release, sparse-vector-technique, vc-dimension, pac-learning, fingerprinting-codes-lower-bound, packing-lower-bound, dinur-nissim-reconstruction-attack]
sources:
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014"
    locator: "Section 4.1: Algorithm 4 (SmallDB), Proposition 4.1 (a small database exists), Theorem 4.2 (privacy), Proposition 4.4 and Theorem 4.5 (accuracy)"
  - paper: doi:10.1007/978-3-319-57048-8_7
    title: "Salil Vadhan, The complexity of differential privacy, in Tutorials on the Foundations of Cryptography, Springer, 2017, pages 347 to 450"
    locator: Section 4.1 (SmallDB) and Theorem 4.1
  - paper: "Avrim Blum, Katrina Ligett and Aaron Roth, A learning theory approach to non-interactive database privacy, STOC 2008; journal version in Journal of the ACM, 2013"
    locator: the original mechanism and its bound in terms of the VC dimension of the query class
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012"
    locator: the attack on floating-point noise and the snapping defense
---

The SmallDB mechanism answers a large set $Q$ of counting queries by releasing a synthetic database of only $m = \lceil \ln|Q|/\alpha^2 \rceil$ records. A random sample of that size already answers every query in $Q$ within $\alpha$. So the mechanism lists all databases of $m$ records and picks one with the [exponential mechanism](/exponential-mechanism/), with a score that rewards small error. The output is $\varepsilon$-differentially private, and its error grows as $(\log|X| \log|Q|/(\varepsilon n))^{1/3}$: only with the log of the number of queries. The listing takes time exponential in $m$, so SmallDB is a proof that such accuracy is possible, not a tool for large data. [MWEM](/mwem/) reaches similar error with a practical algorithm.

## In plain words

You want to publish a fake table of records that gives almost the same answers as the real table, for a very long list of questions of the form "what fraction of the records have this property?".

A few random records from the real table would already give good answers to all the questions, because a random sample is close to the whole for each question, and the list of questions grows the sample size only slowly. But a real sample would leak real records. So SmallDB looks at every possible fake table of that small size and scores each one by its worst answer. It then picks one at random, with a strong preference for good scores. The randomness in the pick hides each person.

## The problem

The universe $X$ is a finite set of $U$ possible records. The data is a histogram $x$ over $X$ with $n$ records, and $n$ is public. A counting query is a vector $f \in \{0,1\}^X$, and its normalized answer is $f(x) = \frac{1}{n}\sum_j f_j x_j$, the fraction of records it counts. Given a set $Q$ of queries, the goal is a synthetic database $y$ with $\max_{f \in Q} |f(x) - f(y)|$ small, under $\varepsilon$-DP. Two datasets are neighbors if one record is replaced by another (replace), so each $f(x)$ moves by at most $1/n$. Dwork and Roth use histograms with $\|x - x'\|_1 \le 1$ and the same sensitivity $1/\|x\|_1$.

## The algorithm

This is Algorithm 4 of Dwork and Roth.

```pseudo id=main
SMALLDB(x, Q, ε, α)
L1  m ← ⌈ln|Q| / α²⌉                                  ▷ the size of the small databases
L2  R ← all histograms y of m records over X
L3  for each y ∈ R: u(y) ← −max_{f ∈ Q} |f(x) − f(y)|   ▷ the score, sensitivity 1/n
L4  output y ∈ R with probability ∝ exp(ε n u(y) / 2)   ▷ the exponential mechanism
```

Line L1 sets the size from Proposition 4.1: a sample of $m$ records has error at most $\alpha$ on all of $Q$. Line L2 lists the candidates, which do not depend on the data. Line L3 scores each by its worst error. Line L4 is the exponential mechanism $\exp(\varepsilon u/(2\Delta u))$ with $\Delta u = 1/n$. The output is a set of $m$ records, and it answers any counting query, not only those in $Q$.

## Example

Take the universe $X = \{1, 2, 3, 4\}$, the data $x = (40, 30, 20, 10)$ with $n = 100$, all 15 non-empty subset queries, $\varepsilon = 1$ and $\alpha = 0.5$. Line L1 gives $m = \lceil \ln 15 / 0.25 \rceil = 11$, and line L2 lists $\binom{14}{3} = 364$ databases. The exact output distribution, from the code, puts most of its mass on a few of them:

| small database $y$ | worst error | probability |
|---|---|---|
| (5, 3, 2, 1) | 0.055 | 0.383 |
| (4, 4, 2, 1) | 0.064 | 0.243 |
| (4, 3, 3, 1) | 0.073 | 0.154 |
| (4, 3, 2, 2) | 0.082 | 0.098 |
| (5, 4, 2, 0) | 0.118 | 0.016 |

The best database $(5, 3, 2, 1)$ is the closest shape to $(40, 30, 20, 10)$ with 11 records. With probability 0.878 the output has worst error at most 0.1, and the mean worst error is 0.072. The run with `random.Random(1)` outputs $(5, 3, 2, 1)$. The guarantee of Claim 3 with $\beta = 0.1$ is $0.5 + 2(\ln 364 + \ln 10)/100 = 0.66$, much weaker than the real error: the term $\alpha$ is a worst case over all data, and here a much better small database exists.

## Correctness

**Privacy (Dwork-Roth Theorem 4.2, a theorem).** The score $u$ changes by at most $1/n$ between neighbors, and $R$ does not depend on the data. So line L4 is the exponential mechanism with the right sensitivity, and it is $\varepsilon$-DP.

**A small database exists (Dwork-Roth Proposition 4.1, a theorem).** For $|Q| \ge 3$, draw $m \ge \ln|Q|/\alpha^2$ records at random from $x$. By the [Hoeffding inequality](/hoeffding-inequality/), each query has error above $\alpha$ with probability at most $2e^{-2m\alpha^2} \le 2/|Q|^2$. By the [union bound](/union-bound/), all queries are within $\alpha$ with positive probability, so such a database exists in $R$.

**Accuracy (Dwork-Roth Theorem 4.5, a theorem).** By the accuracy of the exponential mechanism, with probability at least $1 - \beta$ the output has worst error at most $\alpha + 2(\ln|R| + \ln(1/\beta))/(\varepsilon n)$, and $\ln|R| \le m \ln U$. Choosing $\alpha$ to balance the two terms gives the error

$$\left(\frac{16 \log|X| \log|Q| + 4\log(1/\beta)}{\varepsilon n}\right)^{1/3}.$$

The full proofs are in proofs/correctness.md.

## Complexity

In the [real-RAM model](/real-ram/):

- Line L2 lists $|R| = \binom{m + U - 1}{U - 1} \le U^m$ histograms.
- Line L3 scores each in $O(|Q| U)$ time.
- Line L4 samples in $O(|R|)$ time.

The total is $O(U^{m+1} |Q|)$ time and $O(U^m)$ space. With $m$ of order $\log|Q|/\alpha^2$ this is exponential in $\log U \cdot \log|Q|/\alpha^2$, and super-polynomial in the universe size. Dwork, Naor, Reingold, Rothblum and Vadhan, and later Ullman and Vadhan, show that under cryptographic assumptions no efficient mechanism can produce such synthetic data for all query classes, so some cost of this kind cannot be avoided in general.

## Properties

- **Synthetic data.** The output is a database, so it answers every counting query, and the answers are consistent.
- **Pure DP.** The mechanism is $(\varepsilon, 0)$-DP.
- **Log dependence on $|Q|$.** The error grows with $\log|Q|$, so $Q$ can be exponential in the number of attributes, such as all conjunctions.
- **Error of order $n^{-1/3}$.** For a fixed $Q$ and universe, the error falls as $n^{-1/3}$. For a small number of queries, the [Laplace mechanism](/laplace-mechanism/) on each query is better.

## Variants and improvements

- **VC dimension.** Blum, Ligett and Roth state their bound with the [VC dimension](/vc-dimension/) of the query class in place of $\log|Q|$, through a sample size from [PAC learning](/pac-learning/) theory.
- **$(\varepsilon, \delta)$ and better rates.** Private multiplicative weights (Hardt and Rothblum 2010) is $(\varepsilon, \delta)$-DP, runs in time linear in $|X|$ for each query, and has error of order $n^{-1/2}$ up to factors in $\log|X|$, $\log|Q|$ and $\log(1/\delta)$. For a large $n$ this beats the $n^{-1/3}$ rate.
- **MWEM.** The offline, practical form of the multiplicative weights approach. See [MWEM](/mwem/).
- **Lower bounds.** The [fingerprinting code lower bound](/fingerprinting-codes-lower-bound/) shows that the dependence of private multiplicative weights on $n$ is close to the best possible for $(\varepsilon, \delta)$-DP. The [packing lower bound](/packing-lower-bound/) shows that pure DP needs error of order $\log|X|/(\varepsilon n)$ for some query sets.

## When to use it

Use SmallDB to understand what is possible: it is the simplest proof that a private synthetic database can answer exponentially many counting queries. It runs only on toy universes, as in the test file. For real data, use [MWEM](/mwem/) or other methods with time polynomial in the universe size. For a few queries, answer them directly with the Laplace mechanism.

## Pitfalls

- **Sensitivity of the unnormalized score.** Line L4 uses $\exp(\varepsilon n u/2)$ because the normalized score has sensitivity $1/n$. If the queries are counts and not fractions, the score has sensitivity 1 and the exponent must be $\varepsilon u/2$. Mixing the two scales gives either no privacy or no accuracy.
- **Private $n$.** The sensitivity $1/n$ in line L4 uses $n$. Under add/remove neighbors $n$ is private. Treat $n$ as public, or spend part of the budget on a noisy $n$ and use a lower bound for it.
- **A data dependent candidate set.** Line L2 must list all databases of size $m$ from the universe $X$. Building $R$ from the records of $x$, for example from sub-samples of the real data, makes the support depend on the data and breaks the proof.
- **Too few candidates.** If $m$ in line L1 is too small, no candidate is within $\alpha$, and the error is large even with no noise. If $m$ is too large, $|R|$ explodes and the term $\ln|R|/(\varepsilon n)$ grows.
- **Float sampling.** The code samples with `random.Random` and float weights, for tests only. A deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).

## Implementations

## History

Dinur and Nissim (2003) showed that answering too many queries too accurately reveals the data, and in the early private mechanisms the noise grew with the number of queries. Blum, Ligett and Roth (STOC 2008) showed that with a synthetic database the number of queries can be exponential in $n$, with error depending on the VC dimension of the query class. Dwork and Roth (2014) gave the form used here, with a finite query set and the exponential mechanism over small databases. Hardt and Rothblum (2010) and Hardt, Ligett and McSherry (2012) then gave faster methods with multiplicative weights.

## References
