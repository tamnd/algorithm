---
tag: M4SDHR
kind: algorithm
slug: hardy-weinberg-exact-test
name: Hardy-Weinberg exact test
aliases:
- HWE exact test
area: biology/population-genetics
level: core
summary: "Test departure from Hardy-Weinberg proportions by the exact probability of heterozygote counts given allele counts, computed by a recurrence."
model: real-ram
complexity:
  vars: {n: the number of individuals, m: the number of copies of the minor allele (m <= n)}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2005
  people: [Janis E. Wigginton, David J. Cutler, Gonçalo R. Abecasis]
  note: "Wigginton, Cutler and Abecasis gave the linear-time recurrence for the exact test in 2005. The exact null law of the heterozygote count goes back to Levene in 1949."
prereqs: [hardy-weinberg-principle, p-value]
see_also: [fisher-exact-test, chi-squared-goodness-of-fit-test, permutation-test, sufficient-statistic, genome-wide-association-study, multiple-comparisons-problem, allele-frequency, binomial-coefficient]
sources:
  - paper: doi:10.1086/429864
    title: Janis E. Wigginton, David J. Cutler and Gonçalo R. Abecasis, A note on exact tests of Hardy-Weinberg equilibrium, American Journal of Human Genetics 76(5), 2005
    locator: pp. 887-893 (the recurrence for the heterozygote probabilities, the start near the mode, the two-sided p-value and the comparison with the chi-square test)
  - paper: "Howard Levene, On a matching problem arising in genetics, Annals of Mathematical Statistics 20(1), 1949"
    title: Levene 1949
    locator: the exact distribution of the number of heterozygotes given the allele counts under random union
  - paper: "Sun-Wei Guo and Elizabeth A. Thompson, Performing the exact test of Hardy-Weinberg proportion for multiple alleles, Biometrics 48(2), 1992"
    title: Guo and Thompson 1992
    locator: the exact test for many alleles by a Markov chain over tables with fixed allele counts
  - book: isbn:9780878939022
    title: Bruce S. Weir, Genetic Data Analysis II, Methods for Discrete Population Genetic Data, Sinauer, 1996
    locator: Chapter 3 (disequilibrium, and the tests for Hardy-Weinberg proportions)
---

The Hardy-Weinberg exact test asks whether the genotype counts at one biallelic site fit the proportions $p^2$, $2pq$ and $q^2$ of the [Hardy-Weinberg principle](/hardy-weinberg-principle/). It conditions on the allele counts, so the unknown allele frequency drops out, and it computes the exact null probability of every possible number of heterozygotes. The algorithm of Wigginton, Cutler and Abecasis gets all these probabilities from one start value by a ratio of neighbouring terms, in time linear in the minor allele count. Unlike the chi-square test, it stays valid for rare alleles and small samples.

## In plain words

Take the gene copies of all sampled people, put them in one heap, and deal them out again in pairs at random. Under Hardy-Weinberg proportions, the real sample looks like one such random deal. So count, over all ways to deal the heap, how often each number of mixed pairs (heterozygotes) comes up. If the observed number of heterozygotes is one of the rare outcomes, the sample does not fit. The exact test adds up the chances of all outcomes that are as rare as the observed one or rarer. The trick of the algorithm is that the chance of one count follows from the chance of the next count by a short formula, so there is no need to count deals one by one.

## The problem

**Input.** Genotype counts $n_{AA}$, $n_{Aa}$ and $n_{aa}$ of $n = n_{AA} + n_{Aa} + n_{aa} \ge 1$ diploid individuals at a biallelic site.

**Null hypothesis.** The genotypes are independent draws with probabilities $p^2$, $2pq$ and $q^2$ for some unknown $p$.

**Output.** The p-value of the observed heterozygote count $h_{\text{obs}} = n_{Aa}$ against its exact null law given the allele counts $n_A = 2n_{AA} + n_{Aa}$ and $n_a = 2n - n_A$.

Let $m = \min(n_A, n_a)$ be the minor allele count. For a possible heterozygote count $h$ (with $0 \le h \le m$ and $h \equiv m \pmod 2$) the minor homozygotes number $r = (m - h)/2$ and the common homozygotes $c = n - h - r$. Under the null, given $n_A$ (Levene 1949),

$$P(h) = \frac{n!\; n_A!\; n_a!\; 2^h}{r!\; h!\; c!\; (2n)!}.$$

The factor $p^{n_A} q^{n_a}$ of the multinomial law cancels against the binomial law of $n_A$, so $P$ does not depend on $p$: the allele count is a [sufficient statistic](/sufficient-statistic/) for $p$, and conditioning on it gives a similar test, as in the [Fisher exact test](/fisher-exact-test/). Equivalently, $P$ is the law of the number of mixed pairs when the $2n$ copies are paired at random. The two-sided [p-value](/p-value/) is

$$\pi(h_{\text{obs}}) = \sum_{h :\, P(h) \le P(h_{\text{obs}})} P(h).$$

## The algorithm

Moving from $h$ to $h - 2$ turns two heterozygotes into one homozygote of each kind, so most factors of $P$ cancel in the ratio:

$$\frac{P(h-2)}{P(h)} = \frac{h(h-1)}{4\,(r+1)(c+1)}, \qquad \frac{P(h+2)}{P(h)} = \frac{4\,r\,c}{(h+1)(h+2)},$$

with $r$ and $c$ taken at $h$. The algorithm sets an unnormalized weight 1 at a value near the mode and walks down and up with these ratios.

```pseudo id=main
HWE-EXACT(n_AA, n_Aa, n_aa)
L1  n ← n_AA + n_Aa + n_aa;  m ← min(2·n_AA + n_Aa, 2·n_aa + n_Aa)
L2  h0 ← floor(m(2n - m) / (2n));  if h0 and m differ in parity then h0 ← h0 + 1
L3  w[h0] ← 1
L4  for h ← h0, h0 - 2, ... while h ≥ 2 do  w[h - 2] ← w[h] · h(h - 1) / (4 (r + 1)(c + 1))
L5  for h ← h0, h0 + 2, ... while h ≤ m - 2 do  w[h + 2] ← w[h] · 4 r c / ((h + 1)(h + 2))
L6  S ← sum of all w[h];  P[h] ← w[h] / S for each h
L7  return the sum of P[h] over all h with P[h] ≤ P[n_Aa]
```

In lines L4 and L5, $r = (m - h)/2$ and $c = n - h - r$ are the homozygote counts at the current $h$. Line L2 starts at $2n \hat p \hat q$, the value where the ratio crosses 1. The start does not matter for the result, but there the weights are at most about 1, so floats do not overflow.

## Example

**Ten individuals.** Counts $n_{AA} = 2$, $n_{Aa} = 2$ and $n_{aa} = 6$ give $n = 10$, $n_A = 6$, $n_a = 14$ and $m = 6$ (a check value of the area). Line L2 gives $\lfloor 6 \cdot 14 / 20 \rfloor = 4$, which has the parity of $m$, so $h_0 = 4$ with $r = 1$ and $c = 5$.

| step | $h$ | $r$ | $c$ | ratio | $w$ |
|---|---|---|---|---|---|
| L3 | 4 | 1 | 5 | | $1$ |
| L4 | 4 to 2 | | | $4 \cdot 3 / (4 \cdot 2 \cdot 6) = 1/4$ | $w[2] = 1/4$ |
| L4 | 2 to 0 | 2 | 6 | $2 \cdot 1 / (4 \cdot 3 \cdot 7) = 1/42$ | $w[0] = 1/168$ |
| L5 | 4 to 6 | 1 | 5 | $4 \cdot 1 \cdot 5 / (5 \cdot 6) = 2/3$ | $w[6] = 2/3$ |

The sum is $1/168 + 1/4 + 1 + 2/3 = 323/168$, so line L6 gives $P(0) = 1/323$, $P(2) = 42/323$, $P(4) = 168/323$ and $P(6) = 112/323$. The observed $h = 2$ has probability $42/323$. Only $h = 0$ and $h = 2$ have probability at most $42/323$, so the p-value is $43/323 \approx 0.13313$. The closed form agrees: $P(2) = 10!\, 6!\, 14!\, 2^2 / (2!\, 2!\, 6!\, 20!) = 42/323$.

**One hundred individuals.** Counts 30, 40 and 30 give $n_A = n_a = 100$, $m = 100$ and $h_0 = 50$, the mode, with $P(50) \approx 0.15858$. The observed $P(40) \approx 0.019740$. The values $h \le 40$ have probabilities at most this, and so do the values $h \ge 62$ ($P(62) \approx 0.010207$), but $h = 60$ does not ($P(60) \approx 0.024127$). The p-value is $\Pr(H \le 40) + \Pr(H \ge 62) \approx 0.031537 + 0.015319 = 0.046855$, which rounds to the check value 0.04686. The [chi-squared goodness-of-fit test](/chi-squared-goodness-of-fit-test/) on the same data has expected counts 25, 50 and 25, statistic $4.0$ on 1 degree of freedom and p-value $0.0455$. Here the two tests agree; they part ways for rare alleles (see Pitfalls).

## Correctness

The algorithm computes $P(h)/P(h_0)$ for each possible $h$ by induction along the walk, because each step multiplies by the exact ratio $P(h \mp 2)/P(h)$, and the walks from $h_0$ in steps of 2 reach exactly the values from the least possible one (0 or 1) up to $m$. Every ratio is positive and finite there: $h(h-1) > 0$ for $h \ge 2$, and $r, c \ge 1$ for $h \le m - 2$ because $m \le n$. Dividing by the sum gives $P$. The p-value is valid: for every $\alpha$, $\Pr(\pi(H) \le \alpha) \le \alpha$ under the null, because the set of outcomes with $\pi \le \alpha$ is contained in a set $\{h : P(h) \le P(h^*)\}$ whose total probability is $\pi(h^*) \le \alpha$. The full proofs, with the derivation of Levene's law and the unimodality of $P$, are below.

## Complexity

- **Time.** There are $\lfloor m/2 \rfloor + 1$ possible values of $h$, and each costs $O(1)$ arithmetic operations, so the time is $\Theta(m)$ on a real RAM, and $\Theta(1)$ when $m$ is bounded. Since $m \le n$, it is at most linear in the sample size. Evaluating the closed form for every $h$ would cost a factorial or a log-gamma per term; the recurrence avoids both.
- **Space.** The array $w$ uses $\Theta(m)$ words. Two passes (one to get $S$ and $P(h_{\text{obs}})/P(h_0)$, one to sum the p-value) bring it to $O(1)$ extra words.
- **Exact arithmetic.** With fractions the numbers grow to $O(n \log n)$ bits, so the cost per step is no longer constant. The implementation offers this mode for checking.
- **Many sites.** A genome-wide scan of $M$ sites costs $\Theta(\sum m_i)$, which is cheap; studies also tabulate the law once per pair $(n, m)$.

## Properties

- **Exact and conditional.** The p-value uses the exact law, not a large-sample approximation, and it conditions on the allele counts, so it is valid for every $p$.
- **Conservative.** The law is discrete, so $\Pr(\pi(H) \le \alpha)$ is usually below $\alpha$. In 2000 simulated null samples with $n = 50$ and $n_A = 40$, the implementation rejected at $\alpha = 0.05$ in 3.35 percent of them.
- **Two-sided by probability.** Outcomes are ordered by their own probability, as in the Fisher exact test. Both a deficit and an excess of heterozygotes can give a small p-value.
- **One-sided versions.** $\Pr(H \le h_{\text{obs}})$ tests for a deficit (inbreeding, population structure, null alleles) and $\Pr(H \ge h_{\text{obs}})$ for an excess. In the ten-person example they are $43/323$ and $322/323$. The two one-sided values always sum to $1 + P(h_{\text{obs}})$.
- **Symmetric.** Swapping the names of the alleles does not change the result.
- **Deterministic.** No sampling, unlike a [permutation test](/permutation-test/) of the same null.

## Variants and improvements

- **Many alleles.** For $k$ alleles the conditional law is over tables of genotype counts with fixed allele counts, and there are too many tables to list. Guo and Thompson (1992) estimate the p-value by a Markov chain on these tables, or by Monte Carlo over random pairings.
- **Mid p-value.** Subtracting half of $P(h_{\text{obs}})$ gives a less conservative test whose size is closer to $\alpha$ on average, at the cost of the guarantee.
- **Chi-square and likelihood ratio tests.** Fast, but they rely on large expected counts.
- **Exact test with a different ordering.** Ordering outcomes by $|h - \mathbb E[h]|$ instead of by probability gives another valid exact test; the probability ordering is the one of the paper.
- **X-linked sites.** Males are hemizygous and carry no heterozygote information, so the test is run on females, or with a joint law that uses both sexes.

## When to use it

- Quality control of genotype calls in a [genome-wide association study](/genome-wide-association-study/), where most sites have rare alleles and a chi-square test would be wrong. A strong departure in controls often points to a genotyping error. With many sites, set the threshold with the [multiple comparisons problem](/multiple-comparisons-problem/) in mind.
- Small samples of any kind, where the expected counts are small.
- As a check of the random mating hypothesis before a method that assumes it, such as an estimate of [allele frequency](/allele-frequency/) variance under binomial sampling.

## Pitfalls

- **Rare alleles and the chi-square test.** With $n = 100$, one $aa$ and no $Aa$ ($n_a = 2$), the expected counts are $98.01$, $1.98$ and $0.01$. The chi-square statistic is about $100$, a p-value near $10^{-23}$. The exact law has only $h = 0$ and $h = 2$, with $P(0) = 1/199$, so the exact p-value is about $0.005$. The chi-square test is far too liberal here.
- **What a small p-value means.** A departure can come from inbreeding, population structure (the Wahlund effect), selection, assortative mating, copy number changes or genotyping errors. The test does not say which.
- **Power.** With a rare allele, few outcomes are possible, and the test has little power to see a deficit of heterozygotes.
- **Ties in floating point.** Two values of $h$ can have equal probability. Compare with a small relative tolerance, or work in exact arithmetic, or the p-value can drop a tied term.
- **The start value.** Starting the walk at $h = 0$ or $h = m$ gives weights that can overflow a double for large $n$; start near the mode.

## Implementations

## History

Levene (1949) found the exact law of the number of heterozygotes given the allele counts, as a matching problem: the copies are paired at random. Exact tests based on this law were used for small samples for a long time, often with the full formula for each table. Guo and Thompson (1992) made the test practical for many alleles with Markov chain Monte Carlo. Wigginton, Cutler and Abecasis (2005) gave the linear-time recurrence for two alleles and showed by simulation that the chi-square test has an inflated error rate for rare alleles. Their test became the standard quality filter for genotyping arrays.

## References
