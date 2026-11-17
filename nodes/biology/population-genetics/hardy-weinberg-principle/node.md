---
tag: 50C79H
kind: theorem
slug: hardy-weinberg-principle
name: Hardy-Weinberg principle
aliases:
- Hardy-Weinberg equilibrium
- Hardy-Weinberg law
area: biology/population-genetics
level: intro
summary: "With random mating, an autosomal locus with equal allele frequencies in both sexes and no selection, mutation, migration or drift (a large population) reaches p^2, 2pq, q^2 in one generation."
prereqs: [allele-frequency]
see_also: [hardy-weinberg-exact-test, chi-squared-goodness-of-fit-test, linkage-disequilibrium, fixation-index, genetic-drift, wright-fisher-model, kinship-coefficient, law-of-large-numbers]
sources:
  - paper: doi:10.1126/science.28.706.49
    title: G. H. Hardy, Mendelian proportions in a mixed population, Science 28(706), 1908
    locator: pp. 49-50 (the proportions p^2, 2pq, q^2 after one generation of random mating, and their stability)
  - paper: "Wilhelm Weinberg, Über den Nachweis der Vererbung beim Menschen, Jahreshefte des Vereins für vaterländische Naturkunde in Württemberg 64, 1908"
    title: Weinberg 1908
    locator: the same equilibrium, found independently of Hardy
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 1.2 (the Hardy-Weinberg law, p. 3), Section 2.3 (dioecious populations, p. 44) and Section 2.4 (multiple alleles, p. 49)
  - book: isbn:9780801880094
    title: John H. Gillespie, Population Genetics, A Concise Guide, 2nd edition, Johns Hopkins University Press, 2004
    locator: Section 1.4 (the Hardy-Weinberg law)
  - book: isbn:9781605351537
    title: Rasmus Nielsen and Montgomery Slatkin, An Introduction to Population Genetics, Theory and Applications, Sinauer, 2013
    locator: Chapter 1 (Hardy-Weinberg equilibrium and the departures from it)
---

The Hardy-Weinberg principle says that random mating turns any set of genotype frequencies at one locus into the proportions $p^2$, $2pq$ and $q^2$ in one generation, and that these proportions then stay fixed. It holds under a strict list of assumptions: an autosomal locus, equal allele frequencies in the two sexes, no selection, mutation or migration, discrete generations and a population so large that chance plays no part. The "no drift" in the summary stands for this last assumption. The principle is the null model of population genetics: each force of evolution shows itself as a departure from it.

## Statement

**The setting.** One autosomal locus with alleles $A_1, \ldots, A_k$ in a diploid population. Let $P_{ij}$ be the frequency of genotype $A_iA_j$ among the parents, counted once for each unordered pair, and let

$$p_i = P_{ii} + \tfrac12 \sum_{j \ne i} P_{ij}$$

be the [allele frequency](/allele-frequency/) of $A_i$. For two alleles $A$ and $a$, write $p$ and $q = 1 - p$.

**The hypotheses.**

1. *Random mating.* Each offspring has two parents drawn independently from the parent generation, with no regard to genotype. (Random union of gametes from a common pool gives the same result.)
2. *Mendelian transmission.* A parent passes each of its two copies to an offspring with probability $1/2$.
3. *Equal frequencies in the sexes.* If the sexes are separate, the genotype frequencies, or at least the allele frequencies, are the same in males and in females.
4. *No selection.* All genotypes have the same survival and the same fertility.
5. *No mutation and no migration.*
6. *Discrete generations.* Parents breed once and do not mate with their offspring.
7. *An infinite population.* The frequencies in the offspring generation equal their probabilities. For a finite population, the statements below hold for the expected genotype frequencies of one offspring, and [genetic drift](/genetic-drift/) adds random error.

**The claims.**

- **(A) Allele frequencies are constant.** The offspring generation has the allele frequencies $p_1, \ldots, p_k$ of the parents.
- **(B) One generation suffices.** The offspring genotype frequencies are
$$P'_{ii} = p_i^2, \qquad P'_{ij} = 2 p_i p_j \quad (i < j),$$
whatever the parental genotype frequencies were. For two alleles they are $p^2$, $2pq$ and $q^2$.
- **(C) Equilibrium.** Every later generation has the same frequencies. A population in these proportions is in *Hardy-Weinberg equilibrium*.

## In plain words

Think of every parent as a bag that holds two gene copies. A child takes one copy at random from the bag of each parent. Pool all the bags of the population: a copy drawn from a random parent is a given allele with the chance that equals that allele's share of the pool. The two parents are drawn on their own, so the two copies of a child are like two independent draws from the pool. So the share of children with two copies of one kind is the share of that kind times itself, and the share of mixed children is twice the product of the two shares. The pool of the children has the same make-up as the pool of the parents, so the same thing happens again in the next generation. The old mix of genotypes does not matter after one round of random mating.

## Proof

Fix one offspring and look at the copy it gets from its first parent. The parent is a random member of the parent generation, so it has genotype $A_iA_i$ with probability $P_{ii}$ and genotype $A_iA_j$ ($j \ne i$) with probability $P_{ij}$. By hypothesis 2 it passes $A_i$ with probability 1 in the first case and $1/2$ in the second, and never otherwise. By the law of total probability, the transmitted copy is $A_i$ with probability

$$P_{ii} \cdot 1 + \sum_{j \ne i} P_{ij} \cdot \tfrac12 = p_i.$$

By hypothesis 3 the same holds for the second parent, who comes from the other sex. By hypothesis 1 the two parents are drawn independently, and by hypothesis 2 the segregation in one parent does not depend on the other, so the two transmitted copies are independent. Hence the offspring is $A_iA_i$ with probability $p_i \cdot p_i = p_i^2$. It is $A_iA_j$ with $i < j$ when the first copy is $A_i$ and the second is $A_j$, or the other way round, with probability $2 p_i p_j$. By hypotheses 4 and 5 no genotype is removed or changed between conception and breeding, and no copies enter from outside. By hypothesis 7 the offspring frequencies equal these probabilities. This proves (B).

For (A), apply the formula for $p_i$ to the offspring:

$$p'_i = p_i^2 + \tfrac12 \sum_{j \ne i} 2 p_i p_j = p_i \Big(p_i + \sum_{j \ne i} p_j\Big) = p_i,$$

because the frequencies sum to 1.

For (C), the offspring generation satisfies all hypotheses again (hypothesis 6 keeps the generations apart, and hypothesis 3 holds for the offspring because both sexes of the offspring are built by the same draw). So the next generation has genotype frequencies $p_i^2$ and $2p_ip_j$ with the same $p_i$, and by induction so does every later one. $\blacksquare$

**A check by the mating table.** Start with half $AA$ and half $aa$, so $p = 1/2$ and no heterozygotes. Random pairs are $AA \times AA$ with probability $1/4$ (all offspring $AA$), $aa \times aa$ with probability $1/4$ (all $aa$) and $AA \times aa$ in either order with probability $1/2$ (all $Aa$). So the offspring are $1/4$ $AA$, $1/2$ $Aa$ and $1/4$ $aa$, which is $p^2$, $2pq$ and $q^2$ with $p = 1/2$.

## Consequences

- **Genotype frequencies follow from allele frequencies.** Under the hypotheses, a population at one locus is described by $k - 1$ numbers instead of $k(k+1)/2 - 1$. This is why most models of population genetics, from the [Wright-Fisher model](/wright-fisher-model/) to the [Wright-Fisher diffusion](/wright-fisher-diffusion/), follow only the allele frequency $p$.
- **Rare recessive alleles hide in heterozygotes.** With $q = 0.01$, the frequency of affected $aa$ individuals is $q^2 = 0.0001$ and the frequency of carriers $Aa$ is $2pq = 0.0198$. The share of the $a$ copies that sit in heterozygotes is $2pq / (2pq + 2q^2) = p = 0.99$. So selection against $aa$ removes few copies, which is why [mutation-selection balance](/mutation-selection-balance/) gives the large frequency $\sqrt{u/s}$ for a recessive.
- **A null hypothesis for data.** Observed genotype counts are compared with the expected counts $n p^2$, $2npq$ and $nq^2$ by a [chi-squared goodness-of-fit test](/chi-squared-goodness-of-fit-test/) or by the [Hardy-Weinberg exact test](/hardy-weinberg-exact-test/). In association studies a strong departure in controls often points to a genotyping error.
- **What departures mean.** Inbreeding with coefficient $F$ gives $P_{AA} = p^2 + Fpq$, $P_{Aa} = 2pq(1 - F)$ and $P_{aa} = q^2 + Fpq$, a deficit of heterozygotes ([kinship coefficient](/kinship-coefficient/), [identity by descent](/identity-by-descent/)). Pooling subpopulations with different $p$ gives a deficit too (the Wahlund effect): two equal subpopulations with $p = 0.2$ and $p = 0.8$, each in Hardy-Weinberg proportions, have pooled $p = 0.5$ and expected heterozygosity $0.5$, but the observed heterozygosity is $2 \cdot 0.2 \cdot 0.8 = 0.32$. The deficit $0.18$ equals $2 \operatorname{Var}(p) = 2 \cdot 0.09$, and the [fixation index](/fixation-index/) measures it. Viability selection acts after conception, so adults can depart from the proportions even when zygotes satisfy them.
- **Two loci are different.** Each locus reaches Hardy-Weinberg proportions in one generation, but the association between loci does not vanish in one step. The [linkage disequilibrium](/linkage-disequilibrium/) $D$ decays as $D' = (1 - r) D$ per generation, where $r$ is the recombination fraction.

## Tightness

Each hypothesis is needed for the one-generation claim.

- **Unequal allele frequencies in the sexes.** Let the frequency of $A$ be $p_m$ in males and $p_f$ in females. The offspring are $AA$ with probability $p_m p_f$, $Aa$ with $p_m q_f + q_m p_f$ and $aa$ with $q_m q_f$. With $\bar p = (p_m + p_f)/2$, the heterozygote frequency exceeds $2 \bar p \bar q$ by $(p_m - p_f)^2 / 2$. The offspring of both sexes have the frequency $\bar p$, so the next generation is in Hardy-Weinberg proportions: two generations are needed, not one. Example: $p_m = 1$ and $p_f = 0$ give only $Aa$ offspring (heterozygosity 1, not 0.5), and the generation after that has $1/4$, $1/2$ and $1/4$ (Ewens 2004, section 2.3).
- **An X-linked locus.** A male gets his X from his mother, so $p_m' = p_f$, and a female gets one X from each parent, so $p_f' = (p_m + p_f)/2$. The difference $d = p_f - p_m$ obeys $d' = -d/2$: it halves and changes sign each generation, and only the weighted mean $(p_m + 2 p_f)/3$ is constant. From $p_m = 1$ and $p_f = 0$ the pairs $(p_m, p_f)$ are $(1, 0)$, $(0, 0.5)$, $(0.5, 0.25)$, $(0.25, 0.375)$ and so on toward $(1/3, 1/3)$. Females reach Hardy-Weinberg proportions only in the limit.
- **A finite population.** In a population of $N$ diploids, $p$ performs a random walk and the heterozygosity decays by the factor $1 - 1/(2N)$ per generation ([genetic drift](/genetic-drift/)). In a finite sample there is also a small excess of heterozygotes: given $n_A$ copies of $A$ among $2n$, random union gives $\mathbb E[n_{Aa}] = n_A n_a / (2n - 1)$, a bit more than $2n \hat p \hat q = n_A n_a / (2n)$.
- **Overlapping generations.** If parents of different ages mate, the approach is gradual and no single generation step gives the proportions.
- **Non-random mating.** Selfing and assortative mating keep a heterozygote deficit for ever; disassortative mating gives an excess.

## History

G. H. Hardy, a mathematician, wrote a short letter to Science in 1908 to answer the view, then current among biologists, that a dominant allele should spread until the dominant phenotype makes up three quarters of the population. He showed that random mating keeps any allele frequency, with the genotype proportions $p^2$, $2pq$ and $q^2$. The physician Wilhelm Weinberg derived the same law in the same year in a paper on the inheritance of human traits. English-language texts long called it Hardy's law; the name Hardy-Weinberg became standard after Curt Stern pointed to Weinberg's paper in 1943. Earlier special cases appear in the work of Castle and of Pearson (Ewens 2004, section 1.2, gives the background).

## References
