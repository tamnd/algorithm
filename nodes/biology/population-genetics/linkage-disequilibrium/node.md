---
tag: MKN0WR
kind: definition
slug: linkage-disequilibrium
name: Linkage disequilibrium
aliases:
- gametic phase disequilibrium
- LD measure
area: biology/population-genetics
level: core
summary: The non-random association of alleles at two loci, measured by D = p_AB - p_A p_B and its scaled forms D' and r^2.
history:
  year: 1964
  people: [Richard C. Lewontin, William G. Hill, Alan Robertson]
  note: "Lewontin proposed the scaled measure D' in 1964. Hill and Robertson used the squared correlation r^2 in their 1968 study of linkage disequilibrium in finite populations."
prereqs: [allele-frequency, hardy-weinberg-principle]
see_also: [em-haplotype-frequency-estimation, haplotype-phasing, chi-squared-test-of-independence, extended-haplotype-homozygosity, ld-score-regression, genotype-imputation, li-stephens-model, four-gamete-condition]
sources:
  - paper: doi:10.1093/genetics/49.1.49
    title: Richard C. Lewontin, The interaction of selection and linkage. I. General considerations; heterotic models, Genetics 49(1), 1964
    locator: pp. 49-67 (the measure D' as D divided by its largest value given the allele frequencies)
  - paper: doi:10.1007/BF01245622
    title: William G. Hill and Alan Robertson, Linkage disequilibrium in finite populations, Theoretical and Applied Genetics 38(6), 1968
    locator: pp. 226-231 (the squared correlation r^2 of the alleles at two loci and its expected value under drift and recombination)
  - book: isbn:9780878939022
    title: Bruce S. Weir, Genetic Data Analysis II, Methods for Discrete Population Genetic Data, Sinauer, 1996
    locator: Chapter 3 (disequilibrium coefficients, their estimates from haplotypes and from genotypes, and their tests)
  - paper: "John A. Sved, Linkage disequilibrium and homozygosity of chromosome segments in finite populations, Theoretical Population Biology 2(2), 1971"
    title: Sved 1971
    locator: the approximation of the expected r^2 as 1/(1 + 4Nc)
  - paper: doi:10.1038/nrg2361
    title: Montgomery Slatkin, Linkage disequilibrium, understanding the evolutionary past and mapping the medical future, Nature Reviews Genetics 9(6), 2008
    locator: pp. 477-485 (the measures D, D' and r^2, the causes of LD and its decay)
---

Linkage disequilibrium (LD) is the statistical association of the alleles at two loci on the haplotypes of a population. Two loci are in linkage equilibrium when the frequency of each two-locus haplotype is the product of the frequencies of its alleles. The basic measure is $D = p_{AB} - p_A p_B$, and two scaled measures are in common use: $D'$ of Lewontin (1964) and the squared correlation $r^2$ of Hill and Robertson (1968). Recombination makes $D$ decay over generations, so LD between close loci lasts longer. This is why LD carries information about the history of a population and about the position of a variant that causes a trait. Despite the name, LD can exist between loci that are not linked.

## Definition

Take two biallelic loci with alleles $A, a$ and $B, b$. On the haplotypes of a population (or of a sample), let $p_{AB}$, $p_{Ab}$, $p_{aB}$ and $p_{ab}$ be the frequencies of the four two-locus haplotypes. They are non-negative and sum to 1. The allele frequencies are $p_A = p_{AB} + p_{Ab}$, $p_B = p_{AB} + p_{aB}$, $p_a = 1 - p_A$ and $p_b = 1 - p_B$.

**The coefficient $D$.** The linkage disequilibrium coefficient is

$$D = p_{AB} - p_A p_B.$$

The loci are in *linkage equilibrium* when $D = 0$. An equivalent form is $D = p_{AB} p_{ab} - p_{Ab} p_{aB}$. To see it, expand $p_A p_B = (p_{AB} + p_{Ab})(p_{AB} + p_{aB})$ and use $p_{AB} = p_{AB}(p_{AB} + p_{Ab} + p_{aB} + p_{ab})$; the terms that remain are $p_{AB} p_{ab} - p_{Ab} p_{aB}$. The same argument gives $p_{Ab} = p_A p_b - D$, $p_{aB} = p_a p_B - D$ and $p_{ab} = p_a p_b + D$. So the four haplotype frequencies are fixed by $p_A$, $p_B$ and $D$. If the labels of the alleles at one locus are swapped, $D$ changes sign.

**The scaled measure $D'$.** Given the allele frequencies, the four haplotype frequencies must be non-negative, and this bounds $D$:

$$D_{\max} = \begin{cases} \min(p_A p_b,\ p_a p_B) & D > 0, \\ \min(p_A p_B,\ p_a p_b) & D < 0, \end{cases} \qquad D' = \frac{D}{D_{\max}}.$$

Then $-1 \le D' \le 1$. Many papers report $|D'|$. $|D'| = 1$ means that at least one of the four haplotypes is missing.

**The squared correlation $r^2$.** Let $X = 1$ if a random haplotype carries $A$ and $X = 0$ otherwise, and let $Y$ be the same indicator for $B$. Then $\mathrm{Cov}(X, Y) = p_{AB} - p_A p_B = D$, $\mathrm{Var}(X) = p_A p_a$ and $\mathrm{Var}(Y) = p_B p_b$. So the squared correlation of $X$ and $Y$ is

$$r^2 = \frac{D^2}{p_A p_a p_B p_b},$$

defined when both loci are polymorphic. It does not depend on the labels of the alleles, and $0 \le r^2 \le 1$. If $p_A \le p_B$ and $D > 0$, its largest value for these allele frequencies is $p_A p_b / (p_a p_B)$, so $r^2 = 1$ needs $p_A = p_B$ (or $p_A = p_b$ when $D < 0$) and only two haplotypes. This page uses $D$, $D'$ and $r^2$ in this sense, on haplotype frequencies.

**Decay under recombination.** In a very large population with random mating and discrete generations, let $c$ be the recombination fraction between the loci. A haplotype of the next generation is a parental haplotype with probability $1 - c$, and with probability $c$ it joins an allele at the first locus from one parental haplotype and an allele at the second from another, which are independent under random mating. So $p'_{AB} = (1 - c) p_{AB} + c\, p_A p_B$, while the allele frequencies do not change. Subtracting $p_A p_B$ gives $D_{t+1} = (1 - c) D_t$, where $D_t$ is the value of $D$ in generation $t$, and so

$$D_t = (1 - c)^t D_0.$$

For unlinked loci $c = 1/2$, and $D$ halves each generation. In a finite population, drift creates new LD while recombination removes it.

## Examples and non-examples

**A symmetric case.** $p_{AB} = 0.4$, $p_{Ab} = 0.1$, $p_{aB} = 0.1$ and $p_{ab} = 0.4$. Then $p_A = p_B = 0.5$ and $D = 0.4 - 0.25 = 0.15$, which equals $0.4 \cdot 0.4 - 0.1 \cdot 0.1$. Here $D_{\max} = 0.25$, so $D' = 0.6$, and $r^2 = 0.0225 / 0.0625 = 0.36$.

**$|D'| = 1$ with a small $r^2$.** $p_{AB} = 0.1$, $p_{Ab} = 0$, $p_{aB} = 0.4$ and $p_{ab} = 0.5$. Then $p_A = 0.1$, $p_B = 0.5$ and $D = 0.1 - 0.05 = 0.05 = D_{\max}$, so $D' = 1$. But $r^2 = 0.0025 / (0.1 \cdot 0.9 \cdot 0.5 \cdot 0.5) = 0.111$, which is also the largest $r^2$ possible for these allele frequencies. One haplotype is missing, as it is for a new mutation that has not yet recombined, but the rare allele $A$ predicts $B$ only weakly. This is why association studies use $r^2$ to say how well one marker stands for another, and $D'$ to say whether recombination has happened.

**A sample.** 100 haplotypes with 30 $AB$, 10 $Ab$, 15 $aB$ and 45 $ab$ give $p_A = 0.4$, $p_B = 0.45$, $D = 0.3 - 0.18 = 0.12$, $D' = 0.12 / 0.22 = 0.545$ and $r^2 = 0.242$. For a $2 \times 2$ table of haplotype counts, the Pearson statistic of the [chi-squared test of independence](/chi-squared-test-of-independence/) equals $n r^2$, here $24.24$ on 1 degree of freedom.

**Decay.** With $c = 0.01$, $D$ falls by a factor $0.99$ per generation, so it halves in $\ln 2 / (-\ln 0.99) = 69.0$ generations. From $D_0 = 0.15$, $D_{10} = 0.1357$ and $D_{100} = 0.0549$.

**Non-example: equilibrium.** $p_{AB} = 0.3$, $p_{Ab} = 0.2$, $p_{aB} = 0.3$ and $p_{ab} = 0.2$ give $p_A = 0.5$, $p_B = 0.6$ and $D = 0.3 - 0.3 = 0$. The loci are in linkage equilibrium, and $D'$ and $r^2$ are 0.

**Non-example: LD is not linkage.** Mix two populations in equal parts, one with $p_A = p_B = 0.9$ and one with $p_A = p_B = 0.1$, each in linkage equilibrium. In the mix, $p_{AB} = 0.5 \cdot 0.81 + 0.5 \cdot 0.01 = 0.41$ and $p_A = p_B = 0.5$, so $D = 0.16$, even for loci on different chromosomes. With random mating after the mix, this $D$ halves each generation for unlinked loci. Admixture, population structure, drift and selection all make LD; linkage only makes it last.

**Non-example: one locus.** A departure from [Hardy-Weinberg](/hardy-weinberg-principle/) proportions is an association between the two alleles of one locus in one individual. LD is an association between alleles at two loci on one haplotype. They are different quantities.

## Related definitions

- **Estimates from genotypes.** When only unphased genotypes are known, the haplotype frequencies are estimated first, for example by [EM haplotype frequency estimation](/em-haplotype-frequency-estimation/), or the phase is inferred by [haplotype phasing](/haplotype-phasing/). Weir (1996, Chapter 3) gives a composite measure that needs no assumption of random mating.
- **Expected $r^2$ under drift.** Under drift and recombination at equilibrium, the expected value of $r^2$ decreases in $\rho = 4 N c$. Hill and Robertson (1968) studied it by simulation. Sved (1971) gave the approximation $E[r^2] \approx 1/(1 + 4 N c)$ from an argument on identity by descent of chromosome segments. It is a rule of thumb, not an exact result: the true value also depends on the sample size, on mutation and on the allele frequency filter of the data.
- **Many alleles and many loci.** For loci with many alleles, a coefficient $D_{ij}$ is defined for each pair of alleles, and summaries combine them. For three or more loci, higher-order coefficients describe the part of the association that pairs do not explain.
- **Haplotype structure.** The [four-gamete condition](/four-gamete-condition/) asks whether all four haplotypes occur, which is the same as $|D'| < 1$ when the loci are polymorphic. [Extended haplotype homozygosity](/extended-haplotype-homozygosity/) measures how far haplotypes stay identical around a site.
- **LD in methods.** [Genotype imputation](/genotype-imputation/) and the [Li-Stephens model](/li-stephens-model/) use LD between close sites, and [LD score regression](/ld-score-regression/) uses the sum of $r^2$ of a variant with its neighbours.

## References
