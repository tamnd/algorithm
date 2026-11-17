---
tag: 5PQV9Z
kind: algorithm
slug: em-haplotype-frequency-estimation
name: EM haplotype frequency estimation
aliases:
- Excoffier-Slatkin algorithm
area: biology/population-genetics
level: core
summary: "Estimate haplotype frequencies from unphased genotypes with EM. Split each genotype over its compatible haplotype pairs, then count again."
model: real-ram
complexity:
  vars: {n: the number of individuals, m: the number of sites, h: the largest number of heterozygous sites in one genotype, T: the number of iterations}
  time: {worst: O(T n m 2^h), average: O(T n m 2^h), best: O(n m)}
  space: {extra: O(n m 2^h)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [Laurent Excoffier, Montgomery Slatkin]
  note: "Excoffier and Slatkin gave the EM algorithm for many sites in 1995. Hawley and Kidd, and Long, Williams and Urbanek, published the same method in the same year. Hill had used EM-like gene counting for two sites in 1974."
prereqs: [expectation-maximization, hardy-weinberg-principle, linkage-disequilibrium]
see_also: [haplotype-phasing, li-stephens-model, maximum-likelihood-estimation, allele-frequency, genotype-imputation, gaussian-mixture-model, positional-burrows-wheeler-transform]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a040269
    title: Laurent Excoffier and Montgomery Slatkin, Maximum-likelihood estimation of molecular haplotype frequencies in a diploid population, Molecular Biology and Evolution 12(5), 1995
    locator: pp. 921-927 (the likelihood of the genotypes, the E-step over the compatible haplotype pairs, the M-step by gene counting, and the tests on simulated data)
  - paper: doi:10.1111/j.2517-6161.1977.tb01600.x
    title: Arthur P. Dempster, Nan M. Laird and Donald B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society Series B 39(1), 1977
    locator: pp. 1-38 (the EM algorithm and the proof that each step does not lower the likelihood)
  - paper: "Jeff C. Long, Robert C. Williams and Margrit Urbanek, An E-M algorithm and testing strategy for multiple-locus haplotypes, American Journal of Human Genetics 56(3), 1995"
    title: Long, Williams and Urbanek 1995
    locator: pp. 799-810 (the same EM method, with a likelihood ratio test of linkage disequilibrium)
  - paper: "Michael E. Hawley and Kenneth K. Kidd, HAPLO, a program using the EM algorithm to estimate the frequencies of multi-site haplotypes, Journal of Heredity 86(5), 1995"
    title: Hawley and Kidd 1995
    locator: pp. 409-411 (the program HAPLO)
  - paper: "William G. Hill, Estimation of linkage disequilibrium in randomly mating populations, Heredity 33(2), 1974"
    title: Hill 1974
    locator: pp. 229-239 (two sites, where only the double heterozygotes are ambiguous; the maximum likelihood estimate of the haplotype frequency is a root of a cubic)
---

EM haplotype frequency estimation finds the [maximum likelihood](/maximum-likelihood-estimation/) frequencies of multi-site haplotypes from genotypes whose phase is not known. A genotype tells how many copies of each allele an individual has at each site, but not which alleles sit together on one chromosome. The algorithm is the [expectation-maximization](/expectation-maximization/) method for this missing phase: it splits each individual over the haplotype pairs that fit its genotype, in proportion to their current probability, and then counts the haplotypes again. Excoffier and Slatkin published it in 1995, at the same time as two other groups. It estimates frequencies in the population. It does not by itself give the best phase of each individual; that is the [haplotype phasing](/haplotype-phasing/) problem.

## In plain words

Each person has two copies of a chromosome. A genotype test tells you, at each site, whether the person has zero, one or two copies of a variant, but it does not tell you which copy carries which variant. If a person differs between the two copies at only one site, there is only one way to split the genotype. If the person differs at two or more sites, there are several ways.

The method keeps a guess of how common each full haplotype is. For each person, it shares the person out over the possible splits, with more weight on splits made of common haplotypes. Then it counts all the haplotypes again, with these shares, to make a new guess. It repeats these two steps. Each round makes the data at least as likely as before.

## The problem

**Input.** Genotypes $g_1, \ldots, g_n$ of $n$ diploid individuals at $m$ biallelic sites. Here $g_{ij} \in \{0, 1, 2\}$ is the number of copies of allele 1 that individual $i$ has at site $j$. A haplotype is a vector $h \in \{0, 1\}^m$.

**Model.** The two haplotypes of each individual are drawn independently from one frequency vector $p = (p_h)$, and the individuals are independent. This is [Hardy-Weinberg](/hardy-weinberg-principle/) proportions for haplotypes. A pair $\{h, h'\}$ is compatible with $g$ when $h + h' = g$ site by site. Let $S(g)$ be the set of unordered compatible pairs. Then

$$P(g \mid p) = \sum_{\{h, h'\} \in S(g)} w(h, h')\, p_h p_{h'}, \qquad w(h, h') = \begin{cases} 1 & h = h' \\ 2 & h \ne h', \end{cases}$$

because an ordered pair with two different haplotypes can occur in two orders.

**Output.** A frequency vector $\hat p$ on the simplex that is a stationary point of the log-likelihood $\ell(p) = \sum_i \ln P(g_i \mid p)$, and the value $\ell(\hat p)$.

If $g$ has $k$ heterozygous sites, then $|S(g)| = 2^{k - 1}$ for $k \ge 1$ and $|S(g)| = 1$ for $k = 0$: each heterozygous site can put allele 1 on either haplotype, and swapping the two haplotypes gives the same unordered pair.

## The algorithm

```pseudo id=main
EM-HAPLOTYPES(g_1, ..., g_n, T, ε)
L1  for each individual i, list the compatible pairs S_i ← S(g_i)
L2  H ← the haplotypes that occur in some pair; p_h ← 1/|H| for each h in H
L3  repeat at most T times
L4      c_h ← 0 for each h in H                         ▷ expected copies of h
L5      for each individual i do
L6          P_i ← Σ over {h, h'} in S_i of w(h, h') p_h p_h'
L7          for each {h, h'} in S_i: e ← w(h, h') p_h p_h' / P_i; c_h ← c_h + e; c_h' ← c_h' + e
L8      p_h ← c_h / (2n) for each h in H               ▷ M-step: gene counting
L9      if ℓ(p) gained less than ε in this round then stop
L10 return p
```

Line L7 is the E-step: $e$ is the posterior probability that the individual carries the pair $\{h, h'\}$. When $h = h'$, both updates of line L7 go to the same haplotype, which then gets two copies. Line L8 is the M-step: the expected number of copies of each haplotype over the total $2n$. A haplotype that is in no compatible pair has zero likelihood weight and never enters $H$.

## Example

Ten individuals at two sites. The sum of allele 1 counts over the two sites gives these genotype classes, written as $(g_{i1}, g_{i2})$:

| genotype | (0, 0) | (0, 1) | (1, 0) | (1, 1) | (1, 2) | (2, 2) |
|---|---|---|---|---|---|---|
| individuals | 2 | 1 | 1 | 3 | 1 | 2 |

Only the three double heterozygotes $(1, 1)$ are ambiguous: each is $\{00, 11\}$ (the cis pair) or $\{01, 10\}$ (the trans pair). The other seven individuals give 14 haplotype copies directly: 6 of 00, 2 of 01, 1 of 10 and 5 of 11.

**Round 1.** From the uniform start, each double heterozygote splits $1/2$ and $1/2$. The counts are $6 + 1.5$, $2 + 1.5$, $1 + 1.5$ and $5 + 1.5$ out of 20, so $p = (0.375, 0.175, 0.125, 0.325)$ for 00, 01, 10 and 11. The log-likelihood rises from $-21.4876$ to $-18.7302$.

**Round 2.** The cis weight is $2 \cdot 0.375 \cdot 0.325 = 0.24375$ and the trans weight is $2 \cdot 0.175 \cdot 0.125 = 0.04375$, so each double heterozygote is cis with probability $0.847826$. The new frequency of 00 is $(6 + 3 \cdot 0.847826)/20 = 0.427174$.

**Limit.** After 13 rounds the gain is below $10^{-15}$, and $\hat p = (0.445269, 0.104731, 0.054731, 0.395269)$ with $\ell(\hat p) = -17.870215$. Each double heterozygote is now cis with probability $0.968$. The allele frequencies are $0.45$ and $0.5$, the sample values. The [linkage disequilibrium](/linkage-disequilibrium/) of the estimate is $D = 0.395269 - 0.45 \cdot 0.5 = 0.170269$, $D' = 0.757$ and $r^2 = 0.469$.

## Correctness

The proof has three parts. First, line L7 computes the exact posterior probability of each compatible pair under the current $p$, by Bayes' rule on the model. Second, line L8 maximizes the expected complete-data log-likelihood, because the complete data are $2n$ independent draws from $p$, and the maximum likelihood estimate of a multinomial is the vector of observed shares. Third, the general EM inequality gives $\ell(p^{(t+1)}) \ge \ell(p^{(t)})$. The log-likelihood is bounded above by 0, so the values converge. At a fixed point with all $p_h > 0$, the gradient of $\ell$ is the same for all $h$ in $H$, which is the stationarity condition on the simplex. A further fact helps in practice: after the first round, the allele frequency at each site equals its sample value, since every compatible pair of an individual holds the same alleles. The full proof is below.

## Complexity

Let $k_i$ be the number of heterozygous sites of individual $i$ and $h = \max_i k_i$.

- **Setup.** Line L1 builds $\sum_i 2^{\max(k_i - 1, 0)}$ pairs, each of length $m$: $O(n m 2^h)$ time and space.
- **One round.** Lines L4 to L8 do $O(1)$ arithmetic per pair, plus the cost of a dictionary lookup on a haplotype of length $m$: $O(n m 2^h)$. With haplotypes stored as integer codes, a round costs $O(n 2^h + |H|)$.
- **Rounds.** The number of rounds $T$ depends on the data, and EM converges only linearly near the limit, at a rate set by the fraction of missing information (Dempster, Laird and Rubin). A measured round count is not a bound.
- **Exponential growth.** With many sites, $h$ grows, and $2^{h-1}$ pairs per individual become too many. Excoffier and Slatkin used the method for a moderate number of sites. Longer regions need the methods under Variants.

## Properties

- **A local optimum.** The likelihood can have several local maxima, so EM can end at a point that is not the global maximum. Runs from several starting points are the usual guard.
- **Allele frequencies.** After one round, the frequency of allele 1 at each site is its sample count over $2n$, whatever the start.
- **Phase-known data.** If no individual is heterozygous at two or more sites, each genotype has one compatible pair, and one round gives the direct haplotype count, which is the maximum likelihood estimate.
- **Two sites.** Only the double heterozygotes are ambiguous, and the estimate of the frequency of haplotype 11 is the root of a cubic (Hill 1974). EM finds a root by iteration.
- **Zeros.** A frequency that is 0 at some round stays 0. A uniform start, with every compatible haplotype positive, avoids this.

## Variants and improvements

- **Partition ligation.** Estimate frequencies in short blocks of sites, keep the common haplotypes, and join neighbouring blocks (Niu and coauthors 2002, and Qin and coauthors 2002). This avoids the $2^{h-1}$ pairs of a long region.
- **Bayesian and coalescent priors.** PHASE puts a prior from coalescent theory on the haplotypes and samples the phase of each individual (Stephens, Smith and Donnelly 2001). See [haplotype phasing](/haplotype-phasing/).
- **Copying models.** Modern phasing uses the [Li-Stephens model](/li-stephens-model/), whose cost is linear in the number of sites.
- **Missing genotypes.** A missing site adds both alleles as options, so the set of compatible pairs grows. The E-step stays the same.
- **Likelihood ratio test of LD.** Fit the model with and without independence between sites and compare the maximized likelihoods (Long, Williams and Urbanek 1995; [likelihood ratio test](/likelihood-ratio-test/)).

## When to use it

Use it to estimate the frequencies of haplotypes over a few to about ten sites from unrelated individuals, for example for association tests on haplotypes or for a measure of [linkage disequilibrium](/linkage-disequilibrium/) between two sites from unphased data. For whole chromosomes, or when you need the phase of each individual, use a phasing method.

## Pitfalls

- **Hardy-Weinberg assumption.** The model draws the two haplotypes of an individual independently. Inbreeding or population structure breaks this, and the estimates are then biased.
- **Frequencies are not phases.** The posterior of the pairs of one individual is a by-product. Taking the most likely pair for each individual is a crude phasing method; its error rate is not controlled.
- **The double weight.** A pair of two different haplotypes has weight $2 p_h p_{h'}$, and a pair of one haplotype twice has weight $p_h^2$. A genotype with a heterozygous site has only pairs of two different haplotypes, so the factor 2 cancels in the E-step. It does not cancel in the log-likelihood, and a program that drops it reports wrong likelihoods and wrong likelihood ratio tests.
- **Stopping rule.** A small change of the parameters per round can hide slow convergence. Stop on the gain in log-likelihood and run from several starts.
- **Too many sites.** The number of compatible pairs doubles with each heterozygous site.

## Implementations

## History

Hill in 1974 estimated two-site haplotype frequencies from unphased genotypes by maximum likelihood, where the double heterozygotes are the only missing data. In 1995 three groups published the general EM algorithm for many sites: Excoffier and Slatkin, Hawley and Kidd (the program HAPLO), and Long, Williams and Urbanek. The method follows the EM framework of Dempster, Laird and Rubin (1977). Later Bayesian methods such as PHASE, and HMM methods based on the Li-Stephens model, replaced it for long regions.

## References
