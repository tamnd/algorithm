---
tag: BFZ8DK
kind: algorithm
slug: watterson-estimator
name: Watterson estimator
aliases:
- Watterson's theta
area: biology/population-genetics
level: core
summary: Estimate theta = 4N mu as the number of segregating sites divided by the harmonic number a_n of the sample size minus one.
model: real-ram
complexity:
  vars: {n: the number of sequences, m: the number of aligned sites}
  time: {worst: Θ(n m), average: Θ(n m), best: Θ(n m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1975
  people: [G. A. Watterson]
  note: Watterson derived the distribution of the number of segregating sites in a sample without recombination in 1975 and gave the estimator S / a_n of theta.
prereqs: [infinite-sites-model, kingman-coalescent]
see_also: [nucleotide-diversity, site-frequency-spectrum, tajimas-d, coalescent-simulation, effective-population-size, psmc]
sources:
  - paper: doi:10.1016/0040-5809(75)90020-9
    title: G. A. Watterson, On the number of segregating sites in genetical models without recombination, Theoretical Population Biology 7(2), 1975
    locator: pp. 256-276 (the mean theta a_n and the variance of the number of segregating sites, and the estimator of theta)
  - paper: doi:10.1093/genetics/123.3.585
    title: Fumio Tajima, Statistical method for testing the neutral mutation hypothesis by DNA polymorphism, Genetics 123(3), 1989
    locator: pp. 585-595 (the estimate of theta squared from S, used in the variance of D)
  - book: isbn:9780974707754
    title: John Wakeley, Coalescent Theory, An Introduction, Roberts and Company, 2009
    locator: Chapter 4 (the number of segregating sites and estimators of theta)
---

Watterson's estimator gives the population mutation rate $\theta = 4N\mu$ of a DNA region from a sample of $n$ aligned sequences. It counts the segregating sites $S$, the sites where the sample is not all the same, and divides by $a_n = \sum_{i=1}^{n-1} 1/i$. Under the neutral [infinite sites model](/infinite-sites-model/) with constant size, $E[S] = \theta a_n$ (Watterson 1975), so $\hat\theta_W = S / a_n$ is unbiased. It needs only one pass over the alignment and does not need to know which allele is ancestral. With [nucleotide diversity](/nucleotide-diversity/) it is one of the two estimators that [Tajima's D](/tajimas-d/) compares.

## In plain words

Line up the sequences and walk along them. At each position, look down the column: if all sequences have the same letter, move on; if not, add one to a counter. The counter is the number of places where mutations have happened in the history of the sample.

The history of a larger sample has more branches, so it has more room for mutations. But most of the extra branches are short, because new sequences mostly join the tree near its tips. The total length grows only like the logarithm of the sample size, and $a_n$ is that growth. Dividing by $a_n$ removes the effect of the sample size and leaves the mutation rate.

## The problem

**Input.** A sample of $n \ge 2$ aligned sequences of $m$ sites each, as strings over an alphabet of alleles. Some characters may mark missing data.

**Output.** The number $S$ of segregating sites (sites whose non-missing characters show at least two alleles) and $\hat\theta_W = S / a_n$. Divided by $m$, it is the estimate of $\theta$ per site.

The output is an estimate of $\theta$ only under a model. The model here is neutral mutations, a constant population of $N$ diploids, random mating, and the infinite sites model, so that each segregating site comes from one mutation.

## The algorithm

```pseudo id=main
WATTERSON(H)
L1  S ← 0
L2  for each site j = 1, ..., m do
L3      if the non-missing characters of column j are not all equal then S ← S + 1
L4  a ← 1 + 1/2 + ... + 1/(n − 1)
L5  return S / a
```

Lines L1 to L3 count the segregating sites. Line L4 computes the harmonic number $a_n$, and line L5 returns the estimate. The implementation also returns an estimate of the variance of $\hat\theta_W$:

$$\widehat{\operatorname{Var}}[\hat\theta_W] = \frac{\hat\theta_W}{a_n} + \frac{b_n}{a_n^2} \cdot \frac{S(S - 1)}{a_n^2 + b_n}, \qquad b_n = \sum_{i=1}^{n-1} \frac{1}{i^2}.$$

## Example

The sample of the [infinite sites model](/infinite-sites-model/) page has $n = 5$ sequences and six sites:

| copy | s1 | s2 | s3 | s4 | s5 | s6 |
|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| 4 | 0 | 0 | 1 | 1 | 0 | 0 |
| 5 | 0 | 0 | 1 | 1 | 1 | 0 |

Every column has both a 0 and a 1, so lines L1 to L3 give $S = 6$. Line L4 gives $a_5 = 1 + 1/2 + 1/3 + 1/4 = 25/12$, and line L5 returns $\hat\theta_W = 6 \cdot 12 / 25 = 2.88$. If the six sites lie in a region of $m = 1000$ bases, the estimate per site is $0.00288$.

For the variance, $b_5 = 1 + 1/4 + 1/9 + 1/16 = 1.423611$. The estimate of $\theta^2$ is $S(S - 1)/(a_5^2 + b_5) = 30 / 5.763889 = 5.204819$, and the formula above gives $\widehat{\operatorname{Var}} = 2.88/2.083333 + 1.423611 \cdot 5.204819 / 4.340278 = 3.0896$. So the standard error is about $1.76$: six segregating sites say little about $\theta$.

The [nucleotide diversity](/nucleotide-diversity/) of the same sample is $3$.

## Correctness

The loop of lines L2 and L3 adds one for each segregating site and nothing for the other sites, so after it $S$ is the number of segregating sites. Line L5 returns $S / a_n$.

The estimator is unbiased under the model. Given the coalescent tree with total branch length $L$ (in units of $2N$ generations), each mutation on the tree makes one new segregating site, and the mutations form a Poisson process of rate $\theta/2$ on the branches. So $E[S \mid L] = \theta L / 2$. While $k$ lineages exist, $k$ branches grow for a time $T_k$ with mean $2/(k(k-1))$, so $E[L] = \sum_{k=2}^{n} k \cdot 2/(k(k-1)) = 2 a_n$. So $E[S] = \theta a_n$ and $E[\hat\theta_W] = \theta$. The same computation with the variance of the $T_k$ gives $\operatorname{Var}[S] = \theta a_n + \theta^2 b_n$, so

$$\operatorname{Var}[\hat\theta_W] = \frac{\theta}{a_n} + \frac{\theta^2 b_n}{a_n^2},$$

and $E[S(S - 1)] = \theta^2 (a_n^2 + b_n)$, which makes the estimate of the variance above unbiased too. The proofs are below.

## Complexity

- **Time.** Line L3 reads the $n$ characters of each of the $m$ columns, so the count takes $\Theta(n m)$ time in every case. Line L4 takes $O(n)$ time, or $O(1)$ with the approximation $a_n \approx \ln(n - 1) + 0.5772 + 1/(2(n - 1))$.
- **Space.** Besides the input, a counter and the set of alleles of one column, which has at most the size of the alphabet: $\Theta(1)$.
- **From a VCF file.** When the input is a list of variant sites with genotypes, $S$ is the number of sites with at least two alleles in the sample, and the work is linear in the size of the file.

## Properties

- **Unbiased under the neutral model,** with or without recombination, because $E[S]$ is a sum over sites and each site has the same expected tree length. Recombination changes only the variance, which then is smaller.
- **Consistent in $n$, but slowly.** $\operatorname{Var}[\hat\theta_W] \to 0$ as $n \to \infty$, at the rate $1/\ln n$. Going from $n = 10$ to $n = 100$ raises $a_n$ only from $2.83$ to $5.18$. For $\theta = 5$, the variance is $6.577$ at $n = 10$ and $3.141$ at $n = 50$. More sequence length (with recombination) helps more than more sequences.
- **Smaller variance than $\hat\pi$.** The [nucleotide diversity](/nucleotide-diversity/) $\hat\pi$ is also unbiased, but its variance tends to $\theta/3 + 2\theta^2/9$, not to 0. For $\theta = 5$ and $n = 10$ it is $9.012$, against $6.577$ for $\hat\theta_W$.
- **No outgroup needed.** A site is segregating whatever allele is ancestral.
- **Linear in the spectrum.** $\hat\theta_W = \sum_i \xi_i / a_n$, with equal weight on every class of the [site frequency spectrum](/site-frequency-spectrum/). Because rare variants are the most common class, $\hat\theta_W$ reacts strongly to an excess of rare variants.
- **Streaming.** The sites can arrive one at a time, in any order.

## Variants and improvements

- **Per site.** Divide by the number of sites $m$ that were sequenced, including the invariant ones. The count of invariant sites is often the hard part with real data.
- **Missing data.** If site $j$ has data for $n_j$ sequences, $\sum_j [\text{site } j \text{ segregates}] / a_{n_j}$ is still unbiased for $\theta$ of the region, because each site has its own expectation $\theta_j a_{n_j}$ to first order in the per-site rate.
- **Number of mutations instead of sites.** At a site with $k$ alleles, count $k - 1$ mutations. Under the infinite sites model the two counts agree; under a finite sites model the mutation count is closer to the model, and both are too small when repeat hits are common.
- **Estimators with other weights.** Every $\sum_i w_i \xi_i$ with $\sum_i w_i / i = 1$ is unbiased. With the covariances of the $\xi_i$ (Fu 1995), one can choose the weights of the best linear unbiased estimator under the neutral model, which has a smaller variance than both $\hat\theta_W$ and $\hat\pi$.
- **Maximum likelihood.** Given the whole data and not only $S$, the likelihood of $\theta$ can be computed by importance sampling or MCMC over genealogies, at a far higher cost. For data with recombination, [PSMC](/psmc/) and related methods estimate $\theta$ and a history of $N$ from one genome.

## When to use it

Use it as the first summary of the amount of variation in a region, to compare regions or populations, and as an input to [Tajima's D](/tajimas-d/) and related tests. To turn $\theta$ into an [effective population size](/effective-population-size/), divide by $4\mu$ with an independent estimate of the mutation rate per generation. If the population was not of constant size, $\hat\theta_W$ estimates a weighted average of past sizes, with more weight on recent times than $\hat\pi$ has.

## Pitfalls

- **Sequencing errors.** An error in one read makes a false singleton. Since $\hat\theta_W$ weights singletons as much as any other site, errors inflate it more than they inflate $\hat\pi$.
- **Sample size.** $a_n$ uses the number of sequences, which for diploids is twice the number of individuals. Using the number of individuals gives the wrong $a_n$.
- **Missing data.** With a fixed $n$ in $a_n$, sites with many missing calls segregate less often, and the estimate is too small. Use the per-site version above.
- **The model.** Growth, bottlenecks, structure and selection all change $E[S]$. The number is an estimate of $\theta$ only under the neutral constant-size model; otherwise it is a summary of the data.
- **Repeat hits.** When $\theta$ per site is large (some viruses, distant samples), a site may have mutated more than once, and $S$ undercounts the mutations.

## Implementations

## History

Watterson's 1975 paper in Theoretical Population Biology derived the distribution of the number of segregating sites in a sample from a neutral population without recombination, under Kimura's infinite sites model of 1969. It gave the mean $\theta a_n$, the variance $\theta a_n + \theta^2 b_n$, and the estimator $S / a_n$, before Kingman formalized the coalescent in 1982. Tajima's 1989 test used it together with the mean pairwise difference, and it is now one of the standard outputs of population genetics software.

## References
