---
tag: 935KM5
kind: algorithm
slug: randomized-response
name: Randomized response
aliases:
- Warner randomized response
area: security-and-privacy/differential-privacy
level: intro
summary: Each person answers a yes or no question truthfully with probability p and flips it otherwise, so the population rate can still be estimated.
model: word-ram
complexity:
  vars: {n: the number of people (one report each)}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {deterministic: false, randomized: true}
history:
  year: 1965
  people: [Stanley L. Warner]
  note: Warner proposed randomized response in 1965 as a survey method to reduce evasive answers to sensitive questions.
prereqs: [differential-privacy-definition, binomial-distribution, expected-value]
see_also: [local-differential-privacy, rappor, optimized-local-hashing, laplace-mechanism, post-processing-theorem, hoeffding-inequality, linearity-of-expectation, privacy-amplification-by-shuffling]
sources:
  - paper: doi:10.1080/01621459.1965.10480775
    title: "Stanley L. Warner, Randomized response, a survey technique for eliminating evasive answer bias, Journal of the American Statistical Association 60(309), 1965, pages 63 to 69"
    locator: the randomizing device, the maximum likelihood estimate of the population proportion and its variance
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 3.2, the coin-flip version and Claim 3.5 (it is (ln 3, 0)-differentially private)"
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: why the samplers of a deployment must be exact
  - paper: "Clement L. Canonne, Gautam Kamath and Thomas Steinke, The discrete Gaussian for differential privacy, NeurIPS 2020"
    locator: exact sampling of Bernoulli variables with rational and irrational parameters
---

Randomized response lets each person answer a yes or no question with a random flip, so that no single answer can be trusted, but the fraction of "yes" in the population can still be estimated. Each person tells the truth with probability $p = e^{\varepsilon} / (1 + e^{\varepsilon})$ and gives the other answer otherwise. Then each report is $\varepsilon$-[locally differentially private](/local-differential-privacy/): no one, not even the collector, needs to be trusted with the true answers. Warner (1965) proposed it as a survey method, and it is the base of the local mechanisms such as [RAPPOR](/rappor/).

## In plain words

A survey asks a question that people do not like to answer, such as "did you cheat on a test?". Each person secretly flips a biased coin. If the coin says "truth", the person gives the true answer. If not, the person gives the opposite answer. The person who reads the answer does not see the coin.

So a "yes" can be a true "yes" or a flipped "no", and each person can deny the answer. But the coin has a known bias. Over many people, the share of flipped answers is predictable, and you can correct for it. The estimate of the true share is good when many people answer, and poor for a small group.

## The problem

Each of $n$ people $j = 1, \ldots, n$ holds a private bit $v_j \in \{0, 1\}$. The goal is an estimate of the true fraction $\pi = \frac1n \sum_j v_j$, such that the report of each person is $\varepsilon$-differentially private with respect to that person's own bit.

This is the local model: a randomizer $R$ is $\varepsilon$-LDP if $\Pr[R(v) = r] \le e^{\varepsilon} \Pr[R(v') = r]$ for all inputs $v, v'$ and all outputs $r$. For the whole vector of reports $(R(v_1), \ldots, R(v_n))$, this is $\varepsilon$-[differential privacy](/differential-privacy-definition/) under replace neighbors: two datasets are neighbors when $n$ is the same and one bit differs.

## The algorithm

The parameter is the exact number $e^{\varepsilon}$, a rational number at least 1, so that the truth probability $p$ is an exact fraction $a/q$. For example, $\varepsilon = \ln 3$ gives $e^{\varepsilon} = 3$ and $p = 3/4$.

```pseudo id=main
RANDOMIZED-RESPONSE(v, e^epsilon)            ▷ run by each person on the bit v
L1  p <- e^epsilon / (1 + e^epsilon)         ▷ p = a / q in lowest terms
L2  c <- 1 if a uniform integer in {0, ..., q - 1} is below a, else 0
L3  if c = 1 then return v                   ▷ tell the truth
L4  return 1 - v                             ▷ give the other answer

ESTIMATE(r_1, ..., r_n, e^epsilon)           ▷ run by the collector on the reports
L5  lambda <- (r_1 + ... + r_n) / n          ▷ the observed fraction of ones
L6  return (lambda - (1 - p)) / (2p - 1)
```

Line L2 draws a coin with $\Pr[c = 1] = p$ exactly, with one uniform integer. Lines L3 and L4 report the bit or its complement. The collector sees only the reports. Line L5 computes the fraction $\lambda$ of ones among them. Each report is 1 with probability $p v + (1 - p)(1 - v)$, so $\mathbb E[\lambda] = p\pi + (1 - p)(1 - \pi) = (2p - 1)\pi + (1 - p)$. Line L6 solves this for $\pi$. It needs $p > 1/2$, which means $\varepsilon > 0$.

The code uses a seeded generator so that the tests can repeat each run. A deployment needs a cryptographic source of randomness and an exact coin (Mironov 2012; Canonne, Kamath and Steinke 2020). Line L2 is exact when $e^{\varepsilon}$ is rational.

## Example

Take $\varepsilon = \ln 3$, so $p = 3/4$, $a = 3$ and $q = 4$. Eight people hold the bits $v = (1, 0, 1, 1, 0, 0, 1, 0)$, so the true fraction is $\pi = 1/2$. Line L2 draws the integers $0, 3, 2, 1, 0, 2, 1, 1$ from $\{0, 1, 2, 3\}$.

| person $j$ | $v_j$ | draw | $c$ (line L2) | report $r_j$ |
|---|---|---|---|---|
| 1 | 1 | 0 | 1 | 1 (line L3) |
| 2 | 0 | 3 | 0 | 1 (line L4) |
| 3 | 1 | 2 | 1 | 1 |
| 4 | 1 | 1 | 1 | 1 |
| 5 | 0 | 0 | 1 | 0 |
| 6 | 0 | 2 | 1 | 0 |
| 7 | 1 | 1 | 1 | 1 |
| 8 | 0 | 1 | 1 | 0 |

Line L5 gives $\lambda = 5/8$. Line L6 gives $(5/8 - 1/4) / (1/2) = 3/4$. The standard deviation of the estimate is $\sqrt{p(1-p) / (n (2p-1)^2)} = \sqrt{3/32} = 0.306$, so the error of $1/4$ is within one standard deviation. With $\varepsilon = 1$ the truth probability is $p = e/(1+e) = 0.731059$.

## Correctness

**Theorem (privacy; Dwork-Roth Claim 3.5 for $\varepsilon = \ln 3$).** RANDOMIZED-RESPONSE is $\varepsilon$-LDP, and the vector of the $n$ reports is $\varepsilon$-DP under replace neighbors.

For each output $r$, $\Pr[R(v) = r]$ is $p$ if $r = v$ and $1 - p$ otherwise. So the largest ratio is $p / (1-p) = e^{\varepsilon}$. For the vector, the reports are independent, and two neighbors differ in one bit, so all factors but one cancel.

**Theorem (unbiased estimate).** For every fixed dataset, $\mathbb E[\text{ESTIMATE}] = \pi$ and $\mathrm{Var}[\text{ESTIMATE}] = p(1-p) / (n (2p - 1)^2)$.

The key fact is that each report is an independent [indicator random variable](/indicator-random-variable/), and that its variance is $p(1-p)$ whatever the bit is. The full proofs are in the correctness proof of this page.

## Complexity

The model is the [word RAM](/word-ram/) with words of $O(\log q + \log n)$ bits.

- **Per report.** Line L1 is $O(1)$ arithmetic on the fraction, line L2 is one uniform integer and one comparison, and lines L3 and L4 are $O(1)$. So each report takes $O(1)$ time and one random draw.
- **Estimate.** Line L5 sums $n$ bits in $O(n)$ time, and line L6 is $O(1)$. The extra space is $O(1)$ besides the reports.
- **Total.** The $n$ reports and the estimate take $O(n)$ time in the worst case.

## Properties

- **Local.** Each person randomizes before the data leaves the device. The collector learns the same thing as anyone who reads the reports.
- **Exact.** With a rational $e^{\varepsilon}$, every probability is a fraction, and the privacy loss is exactly $\varepsilon$ (a theorem). The tests check it with exact arithmetic, and they check that the claim fails for $\varepsilon - 0.01$.
- **Unbiased, with a large variance.** The variance $p(1-p)/(n(2p-1)^2)$ is about $1/(n\varepsilon^2)$ for small $\varepsilon$. A central mechanism such as the [Laplace mechanism](/laplace-mechanism/) on the count has error about $1/(n\varepsilon)$ on the fraction. So the local model costs a factor of about $\sqrt n$ in the error.
- **Not always in range.** Line L6 can give a value below 0 or above 1, for example $-1/2$ or $3/2$ when all reports are 0 or 1 with $p = 3/4$. Clamping to $[0, 1]$ is [post-processing](/post-processing-theorem/), so it keeps the privacy, but it adds a bias.

## Variants and improvements

- **Two coins.** Dwork and Roth flip a fair coin: on heads, tell the truth; on tails, flip a second fair coin and report it. Then $p = 3/4$ and $\varepsilon = \ln 3$. This is the case $e^{\varepsilon} = 3$ of the algorithm above.
- **Warner's original design.** Warner (1965) gave each person a spinner that picks the statement "I am in group A" with probability $p$ and "I am not in group A" otherwise. The person answers the chosen statement truly. The reports have the same distribution as above.
- **More than two values.** Generalized randomized response reports the true value of $d$ values with probability $e^{\varepsilon}/(e^{\varepsilon} + d - 1)$ and each other value otherwise. For large $d$, [optimized local hashing](/optimized-local-hashing/) and [RAPPOR](/rappor/) have a smaller variance.
- **Repeated reports.** A person who answers the same question again with a fresh coin spends $\varepsilon$ again. RAPPOR stores one randomized answer and randomizes it again for each report, so that repeated reports do not add up the loss.
- **Shuffling.** If a trusted shuffler removes the link between reports and people, the reports satisfy central DP with a much smaller $\varepsilon$ ([privacy amplification by shuffling](/privacy-amplification-by-shuffling/)).

## When to use it

Use randomized response when no party can be trusted with the true bits, and when the population is large: the error is about $1/(\varepsilon\sqrt n)$ on the fraction. When a trusted curator exists, the Laplace or the [geometric mechanism](/geometric-mechanism/) on the count gives an error that is smaller by a factor of about $\sqrt n$. For values from a large domain, use a frequency oracle such as optimized local hashing.

## Pitfalls

- **A float coin.** Line L2 written as "random float < p" with $p = e^{\varepsilon}/(1+e^{\varepsilon})$ in floats gives a probability that differs a little from $p$, and the claimed $\varepsilon$ is then not exact. Line L2 must compare a uniform integer in $\{0, \ldots, q-1\}$ with the numerator $a$ of the exact fraction, or use an exact Bernoulli sampler.
- **A second fresh answer to the same question.** Running lines L2 to L4 again for the same person and the same bit leaks more: two independent reports are only $2\varepsilon$-LDP. Store the first report and send it again, or count the loss with the [sequential composition theorem](/sequential-composition-theorem/).
- **No correction in the estimate.** Line L6 replaced by $\lambda$ itself gives a biased estimate, because $\mathbb E[\lambda] = (2p-1)\pi + (1-p)$. For $p = 3/4$ and $\pi = 0$, $\lambda$ is about $1/4$. Line L6 must subtract $1 - p$ and divide by $2p - 1$.
- **The wrong truth probability.** Line L1 with $p = e^{\varepsilon}$ over 2, or with $p = 1 - e^{-\varepsilon}$, does not give the ratio $p/(1-p) = e^{\varepsilon}$. Line L1 must use $p = e^{\varepsilon}/(1 + e^{\varepsilon})$.

## Implementations

## History

Warner (1965) introduced randomized response in the Journal of the American Statistical Association, as a way to get honest answers to questions about stigmatized behavior. He gave the maximum likelihood estimate of the proportion and its variance under random sampling. The method was used in many surveys after that. Dwork and Roth (2014) showed that the coin version is $(\ln 3)$-differentially private, which links the survey method to differential privacy. It is now the standard first example of local differential privacy.

## References
