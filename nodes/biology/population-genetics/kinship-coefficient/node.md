---
tag: Q5NGNW
kind: definition
slug: kinship-coefficient
name: Kinship coefficient
aliases:
- coancestry coefficient
- coefficient of kinship
- coefficient of coancestry
area: biology/population-genetics
level: core
summary: "The probability that two gene copies drawn at random, one from each of two individuals at the same locus, are identical by descent."
prereqs: [identity-by-descent]
see_also: [snp-heritability-estimation, mixed-model-association, elston-stewart-algorithm, lander-green-algorithm, henderson-mixed-model-equations, linear-mixed-model, fixation-index, genetic-principal-components]
sources:
  - book: isbn:9780387953892
    title: Kenneth Lange, Mathematical and Statistical Methods for Genetic Analysis, 2nd edition, Springer, 2002
    locator: Chapter 5, Genetic Identity Coefficients, pp. 81-96 (the kinship coefficient, its recursion over a pedigree and the condensed identity coefficients)
  - paper: doi:10.1534/genetics.112.148825
    title: Elizabeth A. Thompson, Identity by descent, variation in meiosis, across genomes, and in populations, Genetics 194(2), 2013
    locator: pp. 301-326 (kinship and the coefficients of pairs in pedigrees, and the realized sharing along the genome)
---

The kinship coefficient $\phi_{ij}$ of two individuals is the probability that a gene copy drawn at random from $i$ and a gene copy drawn at random from $j$, at the same locus, are [identical by descent](/identity-by-descent/). It is the standard single number for how related two people are. For a parent and child or for full sibs it is $1/4$, for half sibs $1/8$ and for first cousins $1/16$. Twice the kinship coefficient is the covariance of the additive genetic values of the two individuals, in units of the additive genetic variance, which is why it appears in every mixed model of quantitative genetics.

## Definition

Fix a pedigree whose founders are unrelated. For two individuals $i$ and $j$ and one locus, draw one of the two copies of $i$ and one of the two copies of $j$, each with probability $1/2$, independently of each other and of the inheritance. The **kinship coefficient** is

$$\phi_{ij} = P(\text{the two drawn copies are IBD}).$$

For $i = j$, the two draws are made with replacement, so $\phi_{ii} = \tfrac12 + \tfrac12 F_i = (1 + F_i)/2$, where $F_i$ is the inbreeding coefficient of $i$, the probability that its own two copies are IBD.

**From the IBD state.** For non-inbred $i$ and $j$ with the Cotterman coefficients $(k_0, k_1, k_2)$, the four ways to draw the copies give

$$\phi_{ij} = \tfrac14 k_1 + \tfrac12 k_2.$$

**Recursion over a pedigree.** Order the individuals so that parents come before their children. For founders, $\phi_{ii} = 1/2$ and $\phi_{ij} = 0$ for $i \ne j$. If $i$ has the father $f$ and the mother $m$ and $j$ is not a descendant of $i$, then

$$\phi_{ij} = \tfrac12 (\phi_{fj} + \phi_{mj}), \qquad \phi_{ii} = \tfrac12 (1 + \phi_{fm}),$$

because the copy drawn from $i$ is a copy of a random copy of $f$ or of $m$, each with probability $1/2$. The second formula says that $F_i = \phi_{fm}$, the kinship of the parents.

**Path counting.** Equivalently, $\phi_{ij} = \sum (1/2)^{n + 1} (1 + F_A)$, summed over the paths that go up from $i$ to a common ancestor $A$ and down to $j$ without using an individual twice, where $n$ is the number of parent-child links on the path. This is Wright's rule.

**Matrix form.** The matrix $2\Phi$ is the additive relationship matrix $A$ of the pedigree. Under an additive model the genetic values have the covariance $\sigma_a^2 A$, which is the covariance of the random effect in a [linear mixed model](/linear-mixed-model/).

## Examples and non-examples

| Pair | $(k_0, k_1, k_2)$ | $\phi$ |
|---|---|---|
| Parent and child | $(0, 1, 0)$ | $1/4$ |
| Full sibs | $(1/4, 1/2, 1/4)$ | $1/8 + 1/8 = 1/4$ |
| Half sibs | $(1/2, 1/2, 0)$ | $1/8$ |
| First cousins | $(3/4, 1/4, 0)$ | $1/16$ |
| Identical twins | $(0, 0, 1)$ | $1/2$ |
| Unrelated | $(1, 0, 0)$ | $0$ |

- **First cousins by the recursion.** Let the grandparents $G_1, G_2$ have two children $S_1, S_2$, so $\phi_{S_1 S_2} = 1/4$. $S_1$ has the child $C_1$ with an unrelated founder $W_1$, and $S_2$ has $C_2$ with an unrelated $W_2$. Then $\phi_{S_1 C_2} = \frac12(\phi_{S_1 S_2} + \phi_{S_1 W_2}) = \frac12 \cdot \frac14 = \frac18$, and $\phi_{C_1 C_2} = \frac12 (\phi_{S_1 C_2} + \phi_{W_1 C_2}) = \frac12 \cdot \frac18 = \frac1{16}$.
- **First cousins by path counting.** There are two paths, through $G_1$ and through $G_2$, each with 4 links: $C_1, S_1, G, S_2, C_2$. So $\phi = 2 \cdot (1/2)^5 = 1/16$.
- **Child of first cousins.** Its inbreeding coefficient is the kinship of its parents, $F = 1/16$, and its kinship with itself is $(1 + 1/16)/2 = 17/32$.
- **Non-example: the shared fraction of one pair.** $\phi$ is an expectation over meioses. Two full sibs share, along their genomes, a fraction of IBD copies that varies around $1/4$ from one pair to the next, because crossovers are few per chromosome. The realized value is what marker-based estimates measure.
- **Non-example: an entry of the genomic relationship matrix.** The genomic relationship matrix estimates $2\phi$ relative to the allele frequencies of the sample, not relative to pedigree founders. Its entries for unrelated pairs scatter around $0$ and can be negative, while $\phi$ is never negative.

## Related definitions

- **Identity by descent.** The event whose probability $\phi$ is, see [identity by descent](/identity-by-descent/).
- **Inbreeding coefficient.** $F_i = \phi_{fm}$ for the parents $f$ and $m$ of $i$.
- **Relationship matrix.** $A = 2 \Phi$, the covariance structure of [mixed model association](/mixed-model-association/) and of [SNP heritability estimation](/snp-heritability-estimation/) when it is estimated from markers.
- **Coancestry in populations.** The fixation index $F_{ST}$ is a kinship coefficient of two copies in the same subpopulation, relative to the whole population, see [fixation index](/fixation-index/).
- **Pedigree likelihoods.** The [Elston-Stewart algorithm](/elston-stewart-algorithm/) and the [Lander-Green algorithm](/lander-green-algorithm/) compute the full probability of the marker data, not only the kinship summary.

## References
