---
tag: T51N2F
kind: algorithm
slug: exponential-mechanism
name: Exponential mechanism
aliases:
- McSherry-Talwar mechanism
area: security-and-privacy/differential-privacy
level: core
summary: "Picks an output with probability proportional to e^(epsilon times its utility over twice the sensitivity); the factor 2 can be dropped when the utility is monotone in the data."
model: real-ram
complexity:
  vars: {m: the number of candidates, q: the cost of one evaluation of the utility}
  time: {worst: O(m q)}
  space: {extra: O(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 2007
  people: [Frank McSherry, Kunal Talwar]
  note: McSherry and Talwar defined the exponential mechanism at FOCS 2007 and used it to build approximately truthful auctions.
prereqs: [differential-privacy-definition, global-sensitivity]
see_also: [report-noisy-max, gumbel-max-trick, laplace-mechanism, mwem, smalldb-mechanism, private-query-release, sparse-vector-technique, vickrey-auction]
sources:
  - paper: doi:10.1109/FOCS.2007.66
    title: "Frank McSherry and Kunal Talwar, Mechanism design via differential privacy, FOCS 2007, pages 94 to 103"
    locator: the definition of the exponential mechanism with a base measure, its privacy theorem and its utility bound
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 3.4, Definition 3.4 (the mechanism), Theorem 3.10 (privacy), Theorem 3.11 and Corollary 3.12 (utility), the definition of a monotonic function, Theorem 3.13 (report one-sided noisy arg-max) and Remark 3.1 (the Gumbel max trick)"
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: why a float sampler is not enough for a release
---

The exponential mechanism selects one item from a set of candidates, such as a price, a threshold or a model, so that good items are likely and the choice is $\varepsilon$-[differentially private](/differential-privacy-definition/). Each candidate $r$ has a utility $u(x, r)$ that depends on the dataset $x$, and the mechanism outputs $r$ with probability proportional to $\exp(\varepsilon u(x, r) / (2\Delta))$, where $\Delta$ is the [sensitivity](/global-sensitivity/) of $u$. When the utility is monotone in the data, the factor 2 can be dropped. It is the general tool for private selection when adding noise to the output makes no sense, and McSherry and Talwar (2007) introduced it to design auctions.

## In plain words

You want to choose the most popular of several options from votes, but you must not let the choice reveal any one vote. So you choose at random, and you give each option a weight that grows exponentially with its number of votes. One vote changes the count of an option by at most one, so it changes each weight by at most a fixed factor. Then the probability of each choice changes very little when one voter leaves.

The best option is the most likely choice. An option that is far behind is exponentially unlikely, so the chosen option is almost always close to the best. The price for privacy is a small loss of utility that grows only with the logarithm of the number of options.

## The problem

The input is a dataset $x$, a finite list $R = (r_1, \ldots, r_m)$ of candidates that does not depend on $x$, a utility function $u(x, r) \in \mathbb R$, a number $\Delta$ and a privacy parameter $\varepsilon > 0$. The **sensitivity** of $u$ is

$$\Delta u = \max_{r \in R}\ \max_{x \sim x'} |u(x, r) - u(x', r)|,$$

and the mechanism needs $\Delta \ge \Delta u$. The page uses add/remove neighbors unless it says otherwise. The utility is **monotone** under a neighbor relation if, for every pair $x \sim x'$, either $u(x, r) \le u(x', r)$ for all $r$ or $u(x, r) \ge u(x', r)$ for all $r$. A count of votes for each option is monotone under add/remove, because a new record never lowers a count. It is not monotone under replace, where one count rises and another count falls.

The output is one candidate $r \in R$. The map from $x$ to the distribution of $r$ must be $\varepsilon$-DP, and $u(x, r)$ must be close to $\mathrm{OPT}(x) = \max_{r} u(x, r)$ with high probability. The output distribution is

$$\Pr[\text{output } r] = \frac{\exp(\varepsilon u(x, r)/(c\Delta))}{\sum_{r' \in R} \exp(\varepsilon u(x, r')/(c\Delta))}, \qquad c = 2 \text{ in general}, \quad c = 1 \text{ for a monotone utility}.$$

## The algorithm

```pseudo id=main
EXPONENTIAL-MECHANISM(x, R, u, Delta, epsilon, monotone)   ▷ R = (r_1, ..., r_m), Delta >= the sensitivity of u
L1  c <- 1 if monotone else 2
L2  s_r <- epsilon u(x, r) / (c Delta) for each r in R
L3  M <- the largest s_r
L4  w_r <- exp(s_r - M) for each r in R
L5  W <- the sum of all w_r
L6  draw U uniform in [0, 1); t <- U W
L7  for r <- r_1 to r_m do
L8      t <- t - w_r
L9      if t < 0 then return r
L10 return r_m                                  ▷ reached only by float rounding
```

Line L1 picks the factor of the exponent. Line L2 computes the scores, and this is the only line that reads the data. Lines L3 and L4 subtract the largest score before the exponential. This divides every weight by the same number $e^M$, so the distribution does not change, but no weight overflows and the largest weight is 1. Lines L5 to L9 sample one candidate with probability $w_r / W$ by [inverse transform sampling](/inverse-transform-sampling/) on the list: the candidate whose interval of length $w_r$ holds the point $U W$ is returned. In exact arithmetic the loop always returns, and line L10 only guards against rounding. Only the output is published; the scores and the weights are never published.

The code on this site uses floats and a seeded pseudorandom generator, so that the tests can repeat each run. A deployment needs a cryptographic source of randomness and an exact sampler, for the same reasons as the [Laplace mechanism](/laplace-mechanism/) (Mironov 2012).

## Example

The candidates are $R = (A, B, C)$ and the dataset is the list of votes $x = (A, A, A, B, B, C)$. The utility $u(x, r)$ is the number of votes for $r$, so the counts are $(3, 2, 1)$ and $\Delta u = 1$ under both neighbor relations. Take $\varepsilon = 1$ and the general version, so $c = 2$. Assume that line L6 draws $U = 0.62$.

| step | value |
|---|---|
| L1 | $c = 2$ |
| L2 | $s = (1.5, 1, 0.5)$ |
| L3 | $M = 1.5$ |
| L4 | $w = (1, e^{-0.5}, e^{-1}) = (1, 0.606531, 0.367879)$ |
| L5 | $W = 1.974410$ |
| L6 | $t = 0.62 \times 1.974410 = 1.224134$ |
| L7 to L9, $r = A$ | $t = 1.224134 - 1 = 0.224134$, not negative |
| L7 to L9, $r = B$ | $t = 0.224134 - 0.606531 = -0.382397$, so return $B$ |

The output distribution is $(0.506480, 0.307196, 0.186324)$. Counts are monotone under add/remove, so the version with $c = 1$ is also $1$-DP there, and it gives $(0.665241, 0.244728, 0.090031)$, which puts more weight on the best option.

A larger example shows the utility bound. With counts $(30, 20, 10)$, $\varepsilon = 1$ and $c = 2$, the distribution is $(0.993262, 0.006693, 0.000045)$. The utility theorem below with $t = 3$ says that the output has utility at most $30 - 2(\ln 3 + 3) = 21.802775$ with probability at most $e^{-3} = 0.049787$. The actual probability of that event, the output $B$ or $C$, is $0.006738$.

## Correctness

**Theorem (privacy; McSherry and Talwar 2007; Dwork-Roth Theorem 3.10).** If $\Delta \ge \Delta u$, then EXPONENTIAL-MECHANISM with $c = 2$ is $\varepsilon$-DP under the neighbor relation that defines $\Delta u$.

The key step splits the ratio of the probabilities into the ratio of the weights and the ratio of the normalizers. For $x \sim x'$ and every $r$,

$$\frac{\Pr[M(x) = r]}{\Pr[M(x') = r]} = \exp\Big(\frac{\varepsilon (u(x, r) - u(x', r))}{2\Delta}\Big) \cdot \frac{\sum_{r'} \exp(\varepsilon u(x', r')/(2\Delta))}{\sum_{r'} \exp(\varepsilon u(x, r')/(2\Delta))} \le e^{\varepsilon/2} \cdot e^{\varepsilon/2}.$$

**Theorem (monotone utility).** If $\Delta \ge \Delta u$ and $u$ is monotone under the neighbor relation, then the version with $c = 1$ is $\varepsilon$-DP. Dwork and Roth define monotone functions and use them for the noisy arg-max in Section 3.4, but they do not state this theorem for the exponential mechanism, so the proof is here. Take $x \sim x'$ with $u(x, r) \le u(x', r) \le u(x, r) + \Delta$ for all $r$. In the ratio for $\Pr[M(x) = r] / \Pr[M(x') = r]$, the first factor is at most 1 and the second at most $e^{\varepsilon}$. In the ratio for the other order, the first factor is at most $e^{\varepsilon}$ and the second at most 1. In both orders the product is at most $e^{\varepsilon}$.

**Theorem (utility; Dwork-Roth Theorem 3.11 and Corollary 3.12).** For every $x$ and $t \ge 0$, the output $r$ satisfies

$$\Pr\Big[u(x, r) \le \mathrm{OPT}(x) - \frac{c\Delta}{\varepsilon}(\ln m + t)\Big] \le e^{-t}.$$

The proof: each bad candidate has weight at most $\exp(\varepsilon(\mathrm{OPT} - (c\Delta/\varepsilon)(\ln m + t))/(c\Delta))$, there are at most $m$ of them, and the normalizer is at least the weight $\exp(\varepsilon\,\mathrm{OPT}/(c\Delta))$ of a best candidate. Dwork and Roth state it for $c = 2$ with $\ln(m / |R_{\mathrm{OPT}}|)$ in place of $\ln m$, where $R_{\mathrm{OPT}}$ is the set of best candidates.

The proofs in full, with the proof that lines L3 to L10 sample the right distribution, are in the correctness proof of this page.

## Complexity

The model is the [real RAM](/real-ram/): an exponential, a uniform real number and an addition each cost one step. One evaluation of $u$ costs $q$ steps.

- **Time.** Line L2 evaluates $u$ once for each of the $m$ candidates, in $O(m q)$ time. Lines L3 to L5 and the loop of lines L7 to L9 each take $O(m)$ time. So the time is $O(m q)$ in the worst case.
- **Space.** The scores and the weights take $O(m)$ numbers. A version that computes each score twice, once for $M$ and $W$ and once in the loop, needs only $O(1)$ extra space and $O(m q)$ time.

When $m$ is very large, as in [SmallDB](/smalldb-mechanism/), where the candidates are all small databases, the running time is the main cost. The privacy and the utility do not depend on how the sampler works.

## Properties

- **Pure privacy.** The output is $(\varepsilon, 0)$-DP. The tests compute the exact output distribution on every dataset of at most 4 votes over 3 options, with $\varepsilon = 1$. The largest log ratio is 0.433 under add/remove and 0.775 under replace for $c = 2$, and 0.977 under add/remove for $c = 1$ (a measurement on the test data). So for counts under add/remove, the factor 2 wastes about half of the budget.
- **Utility that grows like $\ln m$.** The loss is $O((\Delta/\varepsilon)\ln m)$ with high probability, and it does not depend on the size of the dataset. A utility that grows with $n$, such as a count, gives a relative loss that goes to 0.
- **Any output set.** The candidates can be numbers, strings, graphs or models. McSherry and Talwar allow an infinite set with a base measure $\mu$, with a density proportional to $\exp(\varepsilon u(x, r)/(2\Delta))$ with respect to $\mu$.
- **It contains the Laplace mechanism.** On $R = \mathbb R$ with $u(x, r) = -|r - f(x)|$ and $\Delta = \Delta_1 f$, the output density is proportional to $\exp(-\varepsilon |r - f(x)|/(c\Delta))$. This utility is not monotone, so $c = 2$ and the noise is $\mathrm{Lap}(2\Delta/\varepsilon)$, twice the scale of the [Laplace mechanism](/laplace-mechanism/).
- **Closed under post-processing.** Any map of the output that does not read $x$ keeps $\varepsilon$-DP, by the [post-processing theorem](/post-processing-theorem/).

## Variants and improvements

- **Gumbel noise.** Add an independent standard Gumbel sample to each score $s_r$ and output the index of the largest. This samples exactly the distribution of the exponential mechanism, by the [Gumbel max trick](/gumbel-max-trick/) (Dwork-Roth Remark 3.1). It needs no normalizer and works in one pass over a stream of candidates. The tests check it against the exact distribution.
- **Laplace or exponential noise.** [Report noisy max](/report-noisy-max/) adds Laplace noise to each count and reports the index of the largest. Report one-sided noisy arg-max adds one-sided exponential noise with parameter $\varepsilon/\Delta$ for a monotone utility and $\varepsilon/(2\Delta)$ otherwise (Dwork-Roth Theorem 3.13). Both have guarantees similar to the exponential mechanism, but give different distributions.
- **Query release.** [MWEM](/mwem/) uses the exponential mechanism to pick the query with the largest error in each round, and [SmallDB](/smalldb-mechanism/) uses it to pick a small synthetic database. See [private query release](/private-query-release/).
- **Private median and quantiles.** With $u(x, r) = -|\#\{i : x_i \le r\} - n/2|$ over a finite grid of values $r$, the output is an approximate [median](/median/). This utility has sensitivity at most 1 under both neighbor relations, and it is not monotone.

## When to use it

Use the exponential mechanism to choose one item from a discrete set: the best of several options, a price, a split of a decision tree, a parameter from a grid. The output space has no useful metric, or noise on the output would destroy it. When the utility is a count and you only need the index of the best item, report noisy max is a simple alternative with the same kind of guarantee. When the answer is a number and you want to add noise, use the Laplace or the [Gaussian mechanism](/gaussian-mechanism/). The candidate set must be fixed before the data are read.

## Pitfalls

- **The monotone flag under the wrong relation.** Counts are monotone under add/remove but not under replace. The version with $c = 1$ has a largest log ratio of 1.866 under replace in the tests, for $\varepsilon = 1$, so it is only about $2\varepsilon$-DP there. Use $c = 1$ only after you check that every pair of neighbors moves all utilities in the same direction.
- **A candidate set that depends on the data.** If $R$ is built from the values in $x$, such as the set of values that occur, then the presence of a candidate leaks a record. Fix $R$ in advance, for example as a grid.
- **The sensitivity of one candidate.** $\Delta$ must bound the change of $u(x, r)$ for every $r$ at the same time, and over all pairs of neighbors. A bound at the actual $x$ is local sensitivity and is not private.
- **Overflow.** Without lines L3 and L4, $\exp(s_r)$ overflows for scores above about 709 in 64-bit floats. The tests run it with utilities up to $2 \times 10^6$.
- **Float sampling.** Lines L6 to L9 on floats with a non-cryptographic generator are fine for study, but a release needs an exact sampler from a cryptographic source.

## Implementations

## History

McSherry and Talwar (FOCS 2007) defined the exponential mechanism with a base measure on the output set and proved its privacy and utility bounds. They used it to build auctions in which no bidder gains much by lying, because no single bid changes the outcome distribution much, and so tied differential privacy to mechanism design. Dwork and Roth (2014) give the finite form of this page, the utility bound with $\ln(|R| / |R_{\mathrm{OPT}}|)$, and the remark that Gumbel noise samples the same distribution. The mechanism is the selection step of many later algorithms, such as MWEM and SmallDB.

## References
