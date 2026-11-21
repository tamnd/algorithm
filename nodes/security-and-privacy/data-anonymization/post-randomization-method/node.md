---
tag: 4VVPMW
kind: algorithm
slug: post-randomization-method
name: Post-randomization method
aliases:
- PRAM masking
area: security-and-privacy/data-anonymization
level: core
summary: Replaces each categorical value by a random value drawn from a published Markov matrix, so that analysts can correct for it.
model: word-ram
complexity:
  vars: {n: the number of records, K: the number of categories}
  time: {worst: O(n K + K^3)}
  space: {extra: O(K^2)}
history:
  year: 1997
  people: [Peter Kooiman, Leon Willenborg, Jose Gouweleeuw]
  note: "Kooiman, Willenborg and Gouweleeuw proposed PRAM at Statistics Netherlands in 1997. Gouweleeuw, Kooiman, Willenborg and de Wolf gave its theory and invariant PRAM in 1998."
prereqs: [randomized-response, markov-chain, gaussian-elimination]
see_also: [data-swapping, local-differential-privacy, microaggregation, k-anonymity, matrix-inversion, expectation-maximization, method-of-moments, linkage-attack]
sources:
  - url: "https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/post-randomisation-for-statistical-disclosure-control-theory-and-implementation.pdf"
    title: "Jose M. Gouweleeuw, Peter Kooiman, Leon C. R. J. Willenborg and Peter-Paul de Wolf, Post randomisation for statistical disclosure control, theory and implementation, Journal of Official Statistics 14(4), 1998"
    locator: "pp. 463 to 478, the PRAM matrix, the unbiased moment estimate with the inverse of the matrix, and invariant PRAM in Section 5"
  - paper: "Peter Kooiman, Leon Willenborg and Jose Gouweleeuw, PRAM, a method for disclosure limitation of microdata, Research paper 9705, Statistics Netherlands, 1997"
    locator: the first description of the method
  - book: isbn:9781119978152
    title: "Anco Hundepool, Josep Domingo-Ferrer, Luisa Franconi, Sarah Giessing, Eric Schulte Nordholt, Keith Spicer and Peter-Paul de Wolf, Statistical Disclosure Control, Wiley, 2012"
    locator: "Chapter 3, Microdata, the section on PRAM among the perturbative masking methods for categorical data"
  - book: isbn:9780387951218
    title: "Leon Willenborg and Ton de Waal, Elements of Statistical Disclosure Control, Lecture Notes in Statistics 155, Springer, 2001"
    locator: the chapters on perturbative methods for microdata
  - paper: "Stanley L. Warner, Randomized response, a survey technique for eliminating evasive answer bias, Journal of the American Statistical Association 60(309), 1965"
    locator: "pp. 63 to 69, the randomized response design and its unbiased estimate"
---

The post-randomization method (PRAM) masks a categorical attribute of a microdata file. The agency replaces each value $k$ by a random value $l$, drawn with probability $p_{kl}$ from row $k$ of a transition matrix $P$, independently for each record, and it publishes $P$ together with the data. A person who links a released record to a known person cannot trust its value, because it may be a random replacement. An analyst can still estimate the true counts without bias by solving $P^{\mathsf T} \hat T = T^*$, where $T^*$ are the released counts. It is the agency side of [randomized response](/randomized-response/), where the respondent does the random step. A variant called invariant PRAM chooses the matrix so that the expected released counts equal the true counts. PRAM with a matrix that has no zero entries is also [locally differentially private](/local-differential-privacy/), with $\varepsilon$ set by the largest ratio in a column.

## In plain words

An office releases a file where each person has a region. Before it publishes, it rolls a die for each person. Most of the time the region stays the same. Sometimes it changes to another region, with chances that the office fixes in a table. The office publishes the table of chances with the data.

A reader who finds a line that looks like a neighbor cannot be sure of the region on that line. But a researcher who counts the people in each region can undo the effect on average. She knows how many people the die moves out of each region and into it, so she can solve for the counts before the die.

The more the die changes, the more privacy, and the noisier the corrected counts.

## The problem

The input is a list of $n$ values $x_1, \ldots, x_n$ of a categorical attribute with $K$ categories $1, \ldots, K$, and a $K \times K$ matrix $P$ with $p_{kl} \ge 0$ and $\sum_l p_{kl} = 1$ for each $k$. Such a matrix is the transition matrix of a [Markov chain](/markov-chain/). The output is a released list $y_1, \ldots, y_n$ with $\Pr[y_i = l \mid x_i = k] = p_{kl}$, independently for each $i$. An analyst who has $y$ and $P$ wants the true counts $T_k = |\{i : x_i = k\}|$. The choice of $P$ is a policy choice of the agency: large diagonal entries keep the data close to the truth, small ones protect more.

## The algorithm

```pseudo id=main
PRAM(x, P)
L1  for i ← 1 to n do
L2      k ← x_i
L3      u ← a uniform random number in [0, 1)
L4      l ← the least l with p_k1 + p_k2 + ... + p_kl > u
L5      y_i ← l
L6  return y

ESTIMATE(y, P)
L7  T* ← the count of each category in y
L8  solve P^T T̂ = T* for T̂              ▷ by Gaussian elimination; P must be invertible
L9  return T̂
```

Lines L1 to L6 run at the agency, and lines L7 to L9 at the analyst. Line L4 is the inverse of the cumulative distribution of row $k$. The test is strict, so a category with $p_{kl} = 0$ is never chosen. With the cumulative sums stored, a binary search makes line L4 take $O(\log K)$ time.

**Invariant PRAM.** Let $T$ be the true counts and $\lambda_l = \sum_j p_{jl} T_j$ the expected released count of $l$. Gouweleeuw et al. (1998, Section 5) define $q_{lk} = p_{kl} T_k / \lambda_l$ and the matrix $R = P Q$. Then $T^{\mathsf T} R = T^{\mathsf T}$: PRAM with $R$ releases counts whose expectation is the truth, so the analyst can use the released counts directly. The matrix $R$ depends on the data. The agency computes it from the true counts and applies PRAM with $R$ in place of $P$.

## Example

Three regions, with the matrix

| true \ released | 1 | 2 | 3 |
|---|---|---|---|
| 1 | 4/5 | 1/10 | 1/10 |
| 2 | 1/10 | 4/5 | 1/10 |
| 3 | 0 | 1/5 | 4/5 |

and the true counts $T = (50, 30, 20)$. By the [linearity of expectation](/linearity-of-expectation/), the expected released counts are $P^{\mathsf T} T = (40 + 3 + 0,\ 5 + 24 + 4,\ 5 + 3 + 16) = (43, 33, 24)$. The raw released counts are biased: region 1 seems smaller than it is.

Say one run releases $T^* = (45, 31, 24)$. Line L8 solves

$$\tfrac{4}{5} \hat T_1 + \tfrac{1}{10} \hat T_2 = 45, \quad \tfrac{1}{10} \hat T_1 + \tfrac{4}{5} \hat T_2 + \tfrac{1}{5} \hat T_3 = 31, \quad \tfrac{1}{10} \hat T_1 + \tfrac{1}{10} \hat T_2 + \tfrac{4}{5} \hat T_3 = 24,$$

which gives $\hat T = (370/7, 190/7, 20) \approx (52.9, 27.1, 20)$. Each released count can differ from its mean by a few units, and the inverse spreads the error over the estimate. On the mean $T^* = (43, 33, 24)$, the solve gives back $(50, 30, 20)$ exactly.

For invariant PRAM, take two categories, the matrix of randomized response with $p = 3/4$, and $T = (60, 20)$:

| | $P$ | $\lambda$ | $Q$ | $R = P Q$ |
|---|---|---|---|---|
| row 1 | (3/4, 1/4) | 50 | (9/10, 1/10) | (4/5, 1/5) |
| row 2 | (1/4, 3/4) | 30 | (1/2, 1/2) | (3/5, 2/5) |

The check is $60 \cdot (4/5, 1/5) + 20 \cdot (3/5, 2/5) = (60, 20)$. The ratios in the columns are 3 for $P$ and 2 for $R$, so as a local mechanism $P$ is $\ln 3$-private and $R$ is $\ln 2$-private. The matrix of the example with three regions has a 0 in a column with positive entries, so it is not locally private for any $\varepsilon$: a released 1 proves that the true region was not 3.

## Correctness

By the inverse of the distribution function, lines L3 to L5 give $y_i = l$ exactly when $u$ falls in an interval of length $p_{kl}$, so $\Pr[y_i = l] = p_{kl}$. By linearity, $\mathbb{E}[T^*] = P^{\mathsf T} T$. The solve of line L8 is a linear map, so $\mathbb{E}[\hat T] = (P^{\mathsf T})^{-1} P^{\mathsf T} T = T$, and $\hat T$ is unbiased. For invariant PRAM, $(T^{\mathsf T} P)_l = \lambda_l$ and $\sum_l \lambda_l q_{lk} = T_k$. The full proofs, with the covariance of $\hat T$ and the local privacy bound, are in proofs/correctness.md.

## Complexity

The model is the [word RAM](/word-ram/), with one step for each operation on a probability.

- Lines L1 to L6 take $O(n K)$ time with a linear scan at line L4, or $O(K^2 + n \log K)$ with stored cumulative sums and a binary search.
- Line L7 takes $O(n + K)$ time, and line L8 takes $O(K^3)$ by [Gaussian elimination](/gaussian-elimination/).
- The extra space is $O(K^2)$ for the matrix and the elimination.

The matrix $R$ of invariant PRAM takes $O(K^3)$ time to compute.

## Properties

- **Unbiased estimate.** $\mathbb{E}[\hat T] = T$ when $P$ is invertible. This is a theorem.
- **The cost of the noise.** $\mathrm{Cov}(\hat T) = (P^{\mathsf T})^{-1} V P^{-1}$ with $V = \sum_k T_k (\mathrm{diag}(p_k) - p_k p_k^{\mathsf T})$. A matrix close to singular makes the variance large. This is also a theorem.
- **Invariant PRAM keeps the expected counts.** Univariate counts need no correction. Cross tables of the masked attribute with other attributes still need one.
- **Local privacy.** With all entries positive, the release of one record is $\varepsilon$-locally differentially private with $\varepsilon = \max_l \ln(\max_k p_{kl} / \min_k p_{kl})$, and this value is tight.
- **Independent of the other records.** Each draw depends only on the value of its own record, unlike [data swapping](/data-swapping/), where a change needs a partner.

## Variants and improvements

- **PRAM on several attributes together.** Apply one matrix to the combinations of two attributes, so that combinations that cannot occur, such as an age of 5 with a status of married, are never released.
- **PRAM in strata.** Use a different matrix for each value of another attribute, for example for each region. The analyst corrects within each stratum.
- **Maximum likelihood.** The moment estimate of line L8 can have negative entries. A maximum likelihood estimate, for example by [expectation-maximization](/expectation-maximization/), stays in the set of valid counts.
- **Randomized response.** [Randomized response](/randomized-response/) uses the same matrix at the collection step, by the respondent. The estimate is the same.
- **Local differential privacy.** Choosing $P$ to minimize the variance of $\hat T$ for a given $\varepsilon$ is the design problem of [local differential privacy](/local-differential-privacy/).

## When to use it

Use PRAM to mask categorical attributes of a public use file when analysts need unbiased frequency tables and accept more variance, and when the agency is willing to publish the matrix. Use invariant PRAM when most users will not correct the counts. If most of the risk comes from a few rare combinations, [generalization and suppression](/generalization-and-suppression/) or [data swapping](/data-swapping/) of those records can lose less. For a formal guarantee over all records and all analyses, use a mechanism designed for [differential privacy](/differential-privacy-definition/) and account for its total privacy loss.

## Pitfalls

- **P instead of P^T at line L8.** The released counts are $P^{\mathsf T} T$, so the system to solve is $P^{\mathsf T} \hat T = T^*$. Solving $P \hat T = T^*$ is wrong whenever $P$ is not symmetric. In the example, on the mean released counts $(43, 33, 24)$, it gives $(2300/49, 1600/49, 1070/49) \approx (46.9, 32.7, 21.8)$ instead of $(50, 30, 20)$.
- **A test with ≥ at line L4.** With the test $p_{k1} + \cdots + p_{kl} \ge u$, a draw of $u = 0$ picks the first category even when its probability is 0. The test must be strict.
- **Negative estimates.** With small counts, line L8 can give $\hat T_k < 0$. Do not round to 0 and keep the rest, because the total then changes. Report the moment estimate with its variance, or use a maximum likelihood estimate.
- **A secret matrix.** If $P$ is not published, the bias cannot be corrected, and PRAM becomes a form of noise with unknown effect. The protection must come from the randomness of the draws, not from the secrecy of $P$.
- **A weak random source.** The tests use a seeded generator so that they repeat. A release needs a cryptographic source, because an attacker who can predict $u$ can undo the masking.
- **Impossible combinations.** PRAM on one attribute ignores the others. A released record can be a combination that cannot occur, which shows that it was changed and harms the analysis of cross tables.

## Implementations

## History

Warner (1965) proposed randomized response, where a respondent answers a sensitive question with a known random change, and gave the unbiased estimate. Kooiman, Willenborg and Gouweleeuw (1997) at Statistics Netherlands moved the random step to the agency, after the data is collected, and named it PRAM. Gouweleeuw, Kooiman, Willenborg and de Wolf (1998) gave the theory, the moment estimate with the inverse matrix, and invariant PRAM. PRAM is one of the methods of the mu-Argus software and of the textbook of Hundepool et al. (2012). Later work on local differential privacy studies the same matrices with a formal privacy bound.

## References
