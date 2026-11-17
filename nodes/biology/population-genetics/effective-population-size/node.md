---
tag: GQRY99
kind: definition
slug: effective-population-size
name: Effective population size
aliases:
- Ne
area: biology/population-genetics
level: core
summary: The size of an ideal Wright-Fisher population with the same rate of drift or coalescence as the real population under study.
prereqs: [wright-fisher-model, genetic-drift]
see_also: [genetic-drift, wright-fisher-model, moran-model, kingman-coalescent, coalescent-theory, nucleotide-diversity, watterson-estimator, fixation-index]
sources:
  - paper: "Sewall Wright, Evolution in Mendelian populations, Genetics 16(2), 1931"
    title: Wright 1931
    locator: pp. 97-159 (the effective number of a population, and its value with unequal numbers of males and females)
  - book: "James F. Crow and Motoo Kimura, An Introduction to Population Genetics Theory, Harper and Row, 1970"
    title: Crow and Kimura 1970
    locator: the inbreeding and variance effective numbers, and the effect of the variance of family size
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 3.7 (effective population size, p. 119)
  - book: isbn:9780801880094
    title: John H. Gillespie, Population Genetics, A Concise Guide, 2nd edition, Johns Hopkins University Press, 2004
    locator: Section 2.7 (the effective population size)
---

The effective population size $N_e$ of a population is the number $N$ of diploid individuals of an ideal [Wright-Fisher](/wright-fisher-model/) population that has the same amount of [genetic drift](/genetic-drift/) as the real one. It is often much smaller than the number of living individuals, because unequal numbers of the sexes, unequal family sizes and changes of size over time all make drift faster. Since "the same amount of drift" can be measured in more than one way, there is more than one effective size; for an ideal population of constant size they are all equal to $N$.

## Definition

**The ideal population.** A Wright-Fisher population of $N$ diploid individuals ($2N$ gene copies) of constant size, in discrete generations, with random union of gametes (selfing allowed), no selection, no mutation and no migration. Each gene copy of the next generation is a copy of a parent copy chosen uniformly. In this population, with $p$ the frequency of an allele and $q = 1 - p$:

- the change of frequency in one generation has $\operatorname{Var}(\Delta p \mid p) = pq/(2N)$;
- two distinct copies of one generation are copies of the same parent copy with probability $1/(2N)$, so the heterozygosity drops by the factor $1 - 1/(2N)$ per generation;
- the genealogy of a sample tends, as $N \to \infty$, to the [Kingman coalescent](/kingman-coalescent/) with time in units of $2N$ generations.

**Effective sizes.** For a real population (a model with a different structure), each of these quantities defines an effective size, as the $N$ of the ideal population that gives the same value:

- **Variance effective size** $N_e^{(v)}$: $\operatorname{Var}(\Delta p \mid p) = pq/(2N_e^{(v)})$.
- **Inbreeding effective size** $N_e^{(i)}$: the probability that two distinct copies come from the same parent copy is $1/(2N_e^{(i)})$. This sets the rise of the inbreeding coefficient and the loss of heterozygosity.
- **Eigenvalue effective size** $N_e^{(e)}$: the largest eigenvalue below 1 of the transition matrix of the allele count is $1 - 1/(2N_e^{(e)})$, so this size sets the long-term rate of loss of variation.
- **Coalescent effective size** $N_e^{(c)}$: the genealogy of a sample, with time in units of $2N_e^{(c)}$ generations, tends to the Kingman coalescent. This size exists only when such a limit exists.

The page writes $N_e$ when the kinds agree. They differ when the size changes over time: the variance size depends more on the number of offspring and the inbreeding size more on the number of parents. For a haploid population, replace $2N$ by $N$ in all these definitions.

**Three standard formulas.** Each is the result of the definition in a stated model, to first order in $1/N$.

- **Separate sexes (Wright 1931).** With $N_m$ males and $N_f$ females mating at random, $N_e = 4 N_m N_f/(N_m + N_f)$. Two copies have parents of the same sex and the same individual with probability $\tfrac14(1/N_m + 1/N_f)$, and then the same parent copy with probability $\tfrac12$. Setting $\tfrac18(1/N_m + 1/N_f) = 1/(2N_e)$ gives the formula.
- **Size that changes over time.** With sizes $N_1, \ldots, N_t$ over $t$ generations, the heterozygosity keeps the share $\prod_i (1 - 1/(2N_i))$. Setting this equal to $(1 - 1/(2N_e))^t$ and using $1 - x \approx e^{-x}$ gives $1/N_e \approx \tfrac1t \sum_i 1/N_i$: the harmonic mean of the sizes.
- **Variance of family size.** In a population of constant size $N$ in which the number of gametes $k$ that an individual passes on has variance $V_k$ (and mean 2), the inbreeding effective size is $N_e = (4N - 2)/(V_k + 2)$ (Crow and Kimura 1970). Poisson family sizes, $V_k = 2$, give $N_e = N - 1/2$, close to the ideal value. Equal family sizes, $V_k = 0$, give $N_e = 2N - 1$.

## Examples and non-examples

- **Few males.** A herd of 10 males and 90 females has census size 100 but $N_e = 4 \cdot 10 \cdot 90/100 = 36$. The 10 males together supply half the genes of the next generation, so each male passes on 5 percent of all genes, and two copies of the next generation often come from the same father.
- **A bottleneck.** Three generations of sizes 1000, 10 and 1000 have the harmonic mean $3/(1/1000 + 1/10 + 1/1000) \approx 29.4$, and the arithmetic mean 670. The exact share of heterozygosity kept is $0.949050$; a constant size $29.4$ predicts $0.949862$, and a constant size 670 predicts $0.9978$. One small generation controls the result.
- **The Moran model.** A [Moran](/moran-model/) population of $N$ haploid individuals loses heterozygosity at about $2/N$ per generation, so its effective size is $N/2$ copies on the haploid Wright-Fisher scale. The factor comes from the offspring variance, which is 2 per generation instead of 1.
- **Controlled breeding.** A captive population in which every pair has exactly two offspring has $V_k = 0$, so $N_e \approx 2N$, larger than the census size. This is a reason for breeding plans that equalize family sizes.
- **Non-example: the census size.** $N$ is the number of living individuals. It is $N_e$ only in the ideal population. Old individuals that no longer breed and young ones that have not yet bred count in $N$ but not in $N_e$.
- **Non-example: a single number for a structured population.** For a subdivided population with little migration, the variance size of one subpopulation and the coalescent size of the whole population are very different, and the latter can be larger than the total census size, because lineages in different demes take long to meet. The kind of effective size must be stated.

## Related definitions

- **Population mutation rate.** $\theta = 4 N_e \mu$ for diploids, with $\mu$ the mutation rate per copy per generation. Estimates of $\theta$ from DNA data, such as the [Watterson estimator](/watterson-estimator/) and [nucleotide diversity](/nucleotide-diversity/), give $N_e$ when $\mu$ is known. This $N_e$ is a long-term value, close to the harmonic mean of the sizes over the time scale of the genealogy.
- **Coalescent time unit.** In [coalescent theory](/coalescent-theory/), the time unit is $2N_e$ generations, with $N_e$ the coalescent effective size.
- **Fixation index.** Drift in subpopulations of effective size $N_e$ increases the [fixation index](/fixation-index/) by about $1/(2N_e)$ per generation, until migration balances it.
- **Census size and breeding size.** The census size counts all individuals; the breeding size counts those that reproduce. Both are upper estimates of $N_e$ in most natural populations.

## References
