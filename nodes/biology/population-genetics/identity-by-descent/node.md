---
tag: TC62NH
kind: definition
slug: identity-by-descent
name: Identity by descent
aliases:
- IBD
- identical by descent
area: biology/population-genetics
level: core
summary: "Two gene copies are identical by descent when both are copies of one ancestral gene copy, relative to a set of founders of a pedigree or to a reference time in the past."
prereqs: [allele-frequency, conditional-probability]
see_also: [kinship-coefficient, lander-green-algorithm, elston-stewart-algorithm, coalescent-theory, linkage-disequilibrium, fixation-index, positional-burrows-wheeler-transform, snp-heritability-estimation]
sources:
  - paper: doi:10.1534/genetics.112.148825
    title: Elizabeth A. Thompson, Identity by descent, variation in meiosis, across genomes, and in populations, Genetics 194(2), 2013
    locator: pp. 301-326 (IBD relative to founders and to a reference time, the coefficients of pairs of individuals, and IBD segments along the genome)
  - book: isbn:9780387953892
    title: Kenneth Lange, Mathematical and Statistical Methods for Genetic Analysis, 2nd edition, Springer, 2002
    locator: Chapter 5, Genetic Identity Coefficients, pp. 81-96
---

Two gene copies at the same locus are identical by descent (IBD) when both are copies of one gene copy in a common ancestor. The definition always needs a reference point: in a pedigree, the founders, whose copies are taken as unrelated, and in a population, a time in the past, before which all common ancestry is ignored. IBD is the quantity that relatedness, linkage analysis and heritability estimation are about. Markers do not show it directly. They show identity by state, which IBD makes more likely.

## Definition

**IBD of two gene copies.** Fix a pedigree with a set of founders. Each gene copy in a non-founder is a copy of one of the two copies of a parent, chosen at meiosis. Follow two gene copies at a locus back through these choices. They are IBD relative to the founders if both paths end at the same founder copy. They are not IBD if the paths end at different founder copies, even if those copies carry the same allele.

**IBD relative to a time.** In a population without a fixed pedigree, two copies are IBD relative to time $T$ in the past if their most recent common ancestor at this locus lived less than $T$ generations ago. In terms of [coalescent theory](/coalescent-theory/), the coalescence time of the two lineages is below $T$. Every two copies are IBD relative to a time far enough in the past, so the choice of $T$ or of the founders is part of the statement.

**IBD state of two individuals.** Two non-inbred individuals $i$ and $j$ carry four copies at a locus. They share $0$, $1$ or $2$ copies IBD. The probabilities $k_0, k_1, k_2$ of these three cases, with $k_0 + k_1 + k_2 = 1$, are the Cotterman coefficients of the pair. If inbreeding is allowed, the two copies within one person can also be IBD, and the four copies fall into one of 15 IBD patterns, or 9 condensed states when the order of the two copies within each person is ignored (Jacquard's identity states).

**IBD segments.** Along a chromosome, the IBD status of two copies changes only where a crossover happened in one of the meioses on the paths between them. A segment is a maximal interval over which two chromosome copies are IBD. If $m$ meioses separate the two copies and crossovers occur as a Poisson process of rate 1 per Morgan in each meiosis (no interference), the length of a segment in Morgans has the exponential law with rate $m$, so its mean is $100/m$ cM.

## Examples and non-examples

- **Parent and child.** If the parents are unrelated and not inbred, the child carries exactly one copy of each parent at every locus, so $(k_0, k_1, k_2) = (0, 1, 0)$.
- **Full sibs.** The two sibs get the same paternal copy with probability $1/2$ and the same maternal copy with probability $1/2$, independently. So $k_2 = 1/4$, $k_1 = 2 \cdot 1/2 \cdot 1/2 = 1/2$ and $k_0 = 1/4$.
- **Half sibs.** Only the shared parent can give them an IBD copy, with probability $1/2$, so $(k_0, k_1, k_2) = (1/2, 1/2, 0)$.
- **First cousins.** Cousin $A$ gets one copy chosen at random from parent $P_A$, and cousin $B$ one from parent $P_B$, where $P_A$ and $P_B$ are full sibs. These two copies are IBD with the probability that random copies of two full sibs are IBD, which is $k_1/4 + k_2/2 = 1/8 + 1/8 = 1/4$ for full sibs. So $(k_0, k_1, k_2) = (3/4, 1/4, 0)$.
- **Segment lengths.** First cousins are separated by 4 meioses on the path through a shared grandparent, so their IBD segments have a mean length of $100/4 = 25$ cM. A parent and child share one copy IBD at every point of the genome. At each crossover of the meiosis, the shared copy switches from one copy of the parent to the other.
- **Non-example: identical in state but not IBD.** At a SNP with allele frequency $p = 0.3$, two unrelated people ($k_0 = 1$) carry copies of the same allele, in one random copy each, with probability $p^2 + (1 - p)^2 = 0.09 + 0.49 = 0.58$. These copies are identical by state but not IBD relative to the founders of their pedigrees.
- **Non-example: IBD but different in state.** An IBD pair of copies carries different alleles if a mutation happened on one of the paths since the common ancestor. For recent common ancestors this is rare, which is why markers can reveal IBD.

## Related definitions

- **Kinship coefficient.** The [kinship coefficient](/kinship-coefficient/) of $i$ and $j$ is the probability that one random copy of each is IBD: $\phi_{ij} = k_1/4 + k_2/2$ for non-inbred individuals.
- **Inbreeding coefficient.** The probability that the two copies within one person are IBD. It equals the kinship coefficient of the parents.
- **Identity by state.** Two copies are identical by state if they carry the same allele, IBD or not. Markers measure identity by state, and methods such as the [Lander-Green algorithm](/lander-green-algorithm/) compute the probability of IBD given the marker states in a pedigree.
- **Fixation index.** $F_{ST}$ can be read as an IBD probability of two copies within a subpopulation relative to the whole population, see [fixation index](/fixation-index/).
- **Linkage disequilibrium.** [Linkage disequilibrium](/linkage-disequilibrium/) is the association of alleles at nearby loci in a population. Two people who share a segment IBD carry the same alleles at all markers in it, so IBD segments are found as long runs of matching haplotypes.

## References
