---
tag: NB3A2H
kind: definition
slug: allele-frequency
name: Allele frequency
aliases:
- gene frequency
area: biology/population-genetics
level: intro
summary: The fraction of copies of a gene in a population that carry a given allele, the basic state variable of population genetics.
prereqs: [binomial-distribution]
see_also: [hardy-weinberg-principle, genetic-drift, wright-fisher-model, site-frequency-spectrum, linkage-disequilibrium, fixation-index, genotype-likelihood, variance]
sources:
  - book: isbn:9780801880094
    title: John H. Gillespie, Population Genetics, A Concise Guide, 2nd edition, Johns Hopkins University Press, 2004
    locator: Section 1.3 (genotype and allele frequencies)
  - book: isbn:9781605351537
    title: Rasmus Nielsen and Montgomery Slatkin, An Introduction to Population Genetics, Theory and Applications, Sinauer, 2013
    locator: Chapter 1 (allele frequencies, genotype frequencies and Hardy-Weinberg equilibrium)
  - book: isbn:9780878939022
    title: Bruce S. Weir, Genetic Data Analysis II, Methods for Discrete Population Genetic Data, Sinauer, 1996
    locator: Chapter 2 (estimating frequencies, and the variance of an allele frequency estimate with and without Hardy-Weinberg proportions)
---

The allele frequency of an allele is the share of all gene copies at one locus that are copies of that allele. It is a number between 0 and 1, and the frequencies of all alleles at the locus sum to 1. Population genetics describes evolution at a locus mostly as the change of these numbers over time, by [drift](/genetic-drift/), selection, mutation and migration.

## Definition

Take one locus in a population of $N$ diploid individuals. Each individual carries two copies of the locus, so the population holds $2N$ gene copies. Let the alleles at the locus be $A_1, \ldots, A_k$.

**Allele frequency.** The frequency of $A_i$ is

$$p_i = \frac{\text{number of copies of } A_i}{2N}.$$

So $0 \le p_i \le 1$ and $p_1 + \cdots + p_k = 1$. For a biallelic locus with alleles $A$ and $a$, this page writes $p$ for the frequency of $A$ and $q = 1 - p$ for the frequency of $a$.

**From genotype frequencies.** Let $P_{ij}$ be the fraction of individuals with genotype $A_iA_j$ (with $P_{ij} = P_{ji}$ counted once). A homozygote $A_iA_i$ carries two copies of $A_i$ and a heterozygote $A_iA_j$ carries one, so

$$p_i = P_{ii} + \tfrac{1}{2} \sum_{j \ne i} P_{ij}.$$

For two alleles this is $p = P_{AA} + \tfrac12 P_{Aa}$. The map from genotype frequencies to allele frequencies loses information: many genotype vectors give the same $p$. The [Hardy-Weinberg principle](/hardy-weinberg-principle/) says which genotype vector random mating gives for a given $p$.

**In a sample.** A sample of $n$ diploid individuals has $2n$ copies. If $x$ of them are copies of $A$, the sample allele frequency is $\hat p = x / (2n)$. With genotype counts $n_{AA}$, $n_{Aa}$ and $n_{aa}$, $x = 2 n_{AA} + n_{Aa}$.

**Sampling error.** Let $g \in \{0, 1, 2\}$ be the number of $A$ copies of one individual drawn at random from a large population. Then $\mathbb E[g] = 2p$ and $\operatorname{Var}(g) = 4P_{AA} + P_{Aa} - 4p^2$. With $P_{Aa} = 2(p - P_{AA})$ and $D_A = P_{AA} - p^2$, this is $\operatorname{Var}(g) = 2pq + 2D_A$. For $n$ independent individuals, $\hat p = (g_1 + \cdots + g_n)/(2n)$, so

$$\mathbb E[\hat p] = p, \qquad \operatorname{Var}(\hat p) = \frac{pq + D_A}{2n}.$$

Under Hardy-Weinberg proportions $D_A = 0$, the $2n$ copies are independent, $x$ has the [binomial distribution](/binomial-distribution/) $\text{Binomial}(2n, p)$, and the [variance](/variance/) is $pq/(2n)$. With an inbreeding coefficient $F$, $D_A = Fpq$ and the variance is $pq(1 + F)/(2n)$: copies inside one individual are correlated, so a sample of $n$ inbred individuals carries less information than $2n$ independent copies (Weir 1996, chapter 2).

**Other ploidies.** For a haploid population of $N$ individuals there are $N$ copies, and $p_i$ is the count over $N$. For an X-linked locus a female carries two copies and a male carries one, so with $n_f$ females and $n_m$ males the frequency of $A$ is $(2 n_{f,AA} + n_{f,Aa} + n_{m,A}) / (2 n_f + n_m)$.

## Examples and non-examples

- **A sample of 100.** Genotype counts 50 $AA$, 30 $Aa$ and 20 $aa$ give $x = 2 \cdot 50 + 30 = 130$ copies of $A$ out of 200, so $\hat p = 0.65$ and $\hat q = 0.35$. Here $\hat D_A = 0.50 - 0.65^2 = 0.0775$, so the standard error of $\hat p$ is $\sqrt{(0.2275 + 0.0775)/200} \approx 0.0391$, against $\sqrt{0.2275/200} \approx 0.0337$ under Hardy-Weinberg proportions.
- **Same allele frequency, different genotypes.** Population 1 has 25 percent $AA$, 50 percent $Aa$ and 25 percent $aa$. Population 2 has 50 percent $AA$, no $Aa$ and 50 percent $aa$. Both have $p = 0.5$. Only population 1 is in Hardy-Weinberg proportions; population 2 could be a mix of two inbred lines.
- **The check value of the area.** The sample with 30 $AA$, 40 $Aa$ and 30 $aa$ has $\hat p = (60 + 40)/200 = 0.5$. The [Hardy-Weinberg exact test](/hardy-weinberg-exact-test/) uses this sample as its worked example.
- **Three alleles.** The ABO blood group locus has the alleles $A$, $B$ and $O$. If 40 people of 100 are $AO$, 10 are $AB$, 20 are $BO$ and 30 are $OO$, then $p_A = (40 + 10)/200 = 0.25$, $p_B = (10 + 20)/200 = 0.15$ and $p_O = (40 + 20 + 60)/200 = 0.60$. In practice the genotypes $AA$ and $AO$ show the same blood type, so allele frequencies of ABO are estimated from phenotypes, for example by [expectation maximization](/expectation-maximization/).
- **Not an allele frequency: the carrier frequency.** The fraction of individuals that carry at least one copy of $a$ is $P_{Aa} + P_{aa}$. Under Hardy-Weinberg proportions with $q = 0.01$ it is $1 - p^2 = 0.0199$, about twice $q$, because almost every carrier is a heterozygote.
- **Not an allele frequency: the allele fraction in reads.** In sequencing data, the share of reads at a site that show the alternate base in one person is near 0.5 for a heterozygote and near 1 for a homozygote. It is a property of one genotype and of the read sampling, not of a population. The [genotype likelihood](/genotype-likelihood/) turns it into evidence about the genotype.
- **Not an allele frequency: a genotype frequency.** $P_{AA}$ is the share of individuals, and $p$ is the share of copies. They agree only when every individual is homozygous.
- **Minor and derived allele frequency.** The minor allele frequency is $\min(p, q)$, so it is at most 0.5. The derived allele frequency is the frequency of the allele that arose by mutation; it needs an outgroup to tell the ancestral allele, and its sample counts give the unfolded [site frequency spectrum](/site-frequency-spectrum/).

## Related definitions

- **Fixation and loss.** An allele is fixed when $p = 1$ and lost when $p = 0$. Without mutation both states are absorbing in the [Wright-Fisher model](/wright-fisher-model/) and the [Moran model](/moran-model/).
- **Heterozygosity.** The expected heterozygosity is $H = 1 - \sum_i p_i^2$, the chance that two copies drawn with replacement differ. For two alleles it is $2pq$. [Genetic drift](/genetic-drift/) makes it decay at rate $1/(2N)$ per generation.
- **Hardy-Weinberg proportions.** The genotype frequencies $p^2$, $2pq$ and $q^2$ that random mating gives in one generation; see [Hardy-Weinberg principle](/hardy-weinberg-principle/).
- **Haplotype frequency.** The frequency of a combination of alleles at two or more loci on one chromosome. Its departure from the product of the allele frequencies is [linkage disequilibrium](/linkage-disequilibrium/).
- **Fixation index.** The [fixation index](/fixation-index/) compares the allele frequencies of subpopulations: it is the share of the total heterozygosity lost by the differences of $p$ between them.
- **Allele frequency spectrum.** Over many sites, the counts of the number of copies of the derived allele give the [site frequency spectrum](/site-frequency-spectrum/), which the [infinite sites model](/infinite-sites-model/) predicts.

## References
