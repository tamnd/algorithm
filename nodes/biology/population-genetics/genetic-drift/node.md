---
tag: V22WMH
kind: concept
slug: genetic-drift
name: Genetic drift
aliases:
- random genetic drift
area: biology/population-genetics
level: intro
summary: The random change of allele frequencies caused by sampling of parents in a finite population, which leads to loss or fixation of alleles.
prereqs: [allele-frequency, wright-fisher-model]
see_also: [wright-fisher-model, moran-model, effective-population-size, kimura-fixation-probability, wright-fisher-diffusion, fixation-index, kingman-coalescent, tajimas-d]
sources:
  - paper: "Sewall Wright, Evolution in Mendelian populations, Genetics 16(2), 1931"
    title: Wright 1931
    locator: pp. 97-159 (the random drift of gene frequencies in a population of size N and the loss of heterozygosity)
  - book: isbn:9780801880094
    title: John H. Gillespie, Population Genetics, A Concise Guide, 2nd edition, Johns Hopkins University Press, 2004
    locator: Section 2.2 (the decay of heterozygosity), Section 2.3 (mutation and drift) and Section 2.7 (the effective population size)
  - book: isbn:9781605351537
    title: Rasmus Nielsen and Montgomery Slatkin, An Introduction to Population Genetics, Theory and Applications, Sinauer, 2013
    locator: Chapter 2 (genetic drift and mutation) and Chapter 8 (selection in a finite population)
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 3.2 (the Wright-Fisher model with two alleles, p. 92)
---

Genetic drift is the random change of allele frequencies from one generation to the next, because only some individuals of a finite population become parents and each parent passes on a random half of its genes. It has no direction: the expected frequency stays the same. But the changes add up, and in the end every allele is lost or fixed unless mutation, migration or selection works against this. Drift is strong in small populations and weak in large ones, and its speed is measured by the [effective population size](/effective-population-size/).

## In plain words

Think of a jar of marbles of two colours. To make the next jar, you take marbles from the old jar at random, note the colour and put the marble back, until the new jar is as full as the old one. The share of each colour in the new jar is close to the old share, but not the same. Repeat this many times and the share wanders up and down like a drunk walker. When a colour is gone, it cannot come back. So after enough rounds the jar holds one colour only. With a big jar the share moves slowly; with a small jar it moves fast. Real populations work in the same way: a gene variant that does not help or harm can become common or vanish by luck alone.

## The idea

**Sampling error.** In the [Wright-Fisher model](/wright-fisher-model/) with $N$ diploid individuals, the $2N$ gene copies of the next generation are a random sample of the copies of this generation. Given the frequency $p$ now, the next frequency has mean $p$ and variance $pq/(2N)$, with $q = 1 - p$. So the frequency is a martingale: drift alone does not push it up or down.

**Loss of variation.** Each generation, the expected heterozygosity $H = \mathbb E[2pq]$ drops by the factor $1 - 1/(2N)$, so $H_t = H_0 (1 - 1/(2N))^t$. Variation is lost in a time of order $2N$ generations. In the neutral Wright-Fisher model an allele at frequency $p$ fixes with probability $p$, and a new mutant, at frequency $1/(2N)$, fixes with probability $1/(2N)$.

**Replicate populations.** Drift acts differently in each population. Many populations that start at the same frequency $p_0$ spread out: the variance among them is $p_0 q_0 (1 - (1 - 1/(2N))^t)$, and in the limit a share $p_0$ of them is fixed for the allele and the rest have lost it. Between isolated populations, drift creates differences in allele frequency that the [fixation index](/fixation-index/) measures.

**Drift and selection.** Selection changes the frequency by about $s p q$ per generation, and drift by about $\sqrt{pq/(2N)}$. Selection controls the fate of an allele when $4Ns$ is large, and drift controls it when $4N|s|$ is small (about 1 or less). Alleles in the second range are called nearly neutral. The [Kimura fixation probability](/kimura-fixation-probability/) shows the change from one range to the other.

**The size that counts.** Real populations are not ideal. Unequal numbers of the sexes, variance of family size and changes of size over time make drift faster than the census size predicts. The effective size $N_e$ is the size of a Wright-Fisher population with the same rate of drift. For a size that changes over time, $N_e$ is close to the harmonic mean of the sizes, so one small generation (a bottleneck) has a large effect.

**Backward in time.** Drift has a mirror image in the genealogy. Two copies have the same parent copy with probability $1/(2N)$, so lineages merge back in time, and the [Kingman coalescent](/kingman-coalescent/) describes this with time in units of $2N$ generations.

## Examples

- **A short run.** In a population of $N = 10$ diploids ($2N = 20$ copies) with 5 copies of a neutral allele, a run of the Wright-Fisher implementation with seed 7 gives the counts $5, 3, 2, 1, 1, 0$. The allele is lost after 5 generations, an outcome with probability $15/20$ from this start.
- **Heterozygosity.** In a population of $N = 50$, after 10 generations the expected heterozygosity is $0.99^{10} \approx 0.904382$ times its start value. After $2N \ln 2 \approx 69$ generations it is about half.
- **Time to fixation or loss.** In a population with $2N = 20$ copies and $p = 1/2$, the exact mean time until one allele is lost is $26.2$ generations.
- **A bottleneck.** Three generations of sizes $1000$, $10$ and $1000$ keep a share $(1 - 1/2000)(1 - 1/20)(1 - 1/2000) \approx 0.9491$ of the heterozygosity. A constant size equal to the harmonic mean, $3/(1/1000 + 1/10 + 1/1000) \approx 29.4$, keeps $0.9499$, close to it. The arithmetic mean, $670$, would predict $0.9978$, which is far off.
- **Weak selection.** In a population of $N = 100$ with genic selection, a new mutant fixes with probability $0.004071$ if $s = -0.001$, $0.005$ if neutral and $0.006060$ if $s = 0.001$. Here $4N|s| = 0.4$, so drift dominates, and a slightly harmful allele has almost the same chance as a neutral one. With $s = -0.01$ the chance drops to $0.000377$.

## Where it is used

- **The neutral theory of molecular evolution.** New neutral mutations arise at rate $2N\mu$ per generation, and each fixes with probability $1/(2N)$, so they replace each other at the rate $\mu$, independent of $N$. This is the basis of the molecular clock.
- **Conservation genetics.** Small populations lose heterozygosity at the rate $1/(2N_e)$ per generation, which is a reason to keep populations large and connected.
- **Null models of tests for selection.** Tests such as [Tajima's D](/tajimas-d/) and the [McDonald-Kreitman test](/mcdonald-kreitman-test/) compare data with the patterns that drift and mutation alone produce.
- **Estimating population size.** The change of allele frequencies between samples taken some generations apart, or the amount of variation at equilibrium, gives estimates of $N_e$.
- **Population structure.** Drift in isolated groups is the source of frequency differences that [linkage disequilibrium](/linkage-disequilibrium/) and the fixation index measure.

## References
