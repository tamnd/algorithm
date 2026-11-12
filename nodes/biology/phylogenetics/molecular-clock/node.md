---
tag: XVPBMY
kind: concept
slug: molecular-clock
name: Molecular clock
aliases:
- clock hypothesis
area: biology/phylogenetics
level: core
summary: The hypothesis that all lineages change at one constant rate. Branch lengths are then rate times time, the tree is ultrametric, and a test compares it with a tree of free branch lengths.
prereqs: [phylogenetic-tree]
see_also: [relaxed-molecular-clock, divergence-time-estimation, ultrametric, upgma, ultrametric-tree-reconstruction, midpoint-rooting, tree-rooting, kingman-coalescent]
sources:
  - paper: doi:10.1038/217624a0
    title: Motoo Kimura, Evolutionary rate at the molecular level, Nature 217, 1968, 624-626
    locator: the neutral theory, under which the substitution rate of neutral mutations equals the mutation rate
  - paper: doi:10.1126/science.179.4078.1144
    title: Vincent M. Sarich and Allan C. Wilson, Generation time and genomic evolution in primates, Science 179(4078), 1973, 1144-1147
    locator: the relative rate test, which compares the distances of two taxa to an outgroup
  - paper: doi:10.1007/BF01797451
    title: Charles H. Langley and Walter M. Fitch, An examination of the constancy of the rate of molecular evolution, Journal of Molecular Evolution 3(3), 1974, 161-177
    locator: the maximum likelihood fit of a clock tree to Poisson counts of substitutions on branches, and the test of the constant rate
  - paper: doi:10.1007/BF01734359
    title: Joseph Felsenstein, Evolutionary trees from DNA sequences, a maximum likelihood approach, Journal of Molecular Evolution 17(6), 1981, 368-376
    locator: the likelihood ratio test of the clock, comparing the tree with a clock to the tree with free branch lengths
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 19, Testing models, trees, and clocks
  - book: isbn:9780199602605
    title: Ziheng Yang, Molecular Evolution, a Statistical Approach, Oxford University Press, 2014
    locator: Chapter 10, Molecular clock and estimation of species divergence times, Section 10.2, tests of the molecular clock
---

The molecular clock is the hypothesis that the sequences of all lineages change at the same constant rate. Zuckerkandl and Pauling put it forward in 1962 and 1965 from the amino acid differences of hemoglobins and other proteins, and Kimura's neutral theory (1968) gave a reason for it: if most substitutions are neutral, the substitution rate equals the mutation rate, which may be steady. Under a strict clock with rate $r$, the length of a branch is $r$ times its duration. Then every leaf is at the same distance from the root, and the distances between leaves form an [ultrametric](/ultrametric/). A clock turns genetic distance into time, gives the root of the tree, and is the assumption behind [UPGMA](/upgma/). Real data often reject it, which is why [relaxed clocks](/relaxed-molecular-clock/) exist.

## In plain words

If a gene changes at the same speed in every species, it works like a clock. Two species that split long ago have had a long time to change, so their genes differ a lot. Two species that split recently differ little. Count the differences and you can read the time since the split.

This only works if the speed is the same everywhere. A test asks whether the data fit this. Take two species and a third, more distant species. If both of the first two are equally far from the third, the clock may hold. If one of them is much farther, its line has changed faster, and the clock fails for these data.

## The idea

**The model.** Take $n$ taxa with $m$ aligned sites, such as DNA, and a rooted binary tree in which each vertex $v$ has an age $t_v$, with the leaves at age 0 for living taxa. A strict clock has one rate $r$, in substitutions per site per unit time, for every branch. The branch from $u$ to its child $v$ then has length
$$b_{uv} = r\,(t_u - t_v).$$
The tree has $n - 1$ internal ages and one rate. The likelihood depends only on the products $r\,t_v$, so only $n - 1$ numbers can be estimated from the sequences: rate and time are not separately identified without a calibration, as on the [divergence time page](/divergence-time-estimation/). A tree without a clock has $2n - 3$ free branch lengths on an unrooted tree. In both cases the topology is found by a heuristic search over the $(2n-5)!!$ unrooted or $(2n-3)!!$ rooted trees.

**Ultrametric distances.** For leaves $i$ and $j$ with most recent common ancestor of age $t_{ij}$, the path between them has length $d(i, j) = 2 r\, t_{ij}$. For any three leaves $i, j, k$, two of the three common ancestors are the same vertex and it is the oldest of the three, so the two largest of $d(i,j)$, $d(i,k)$ and $d(j,k)$ are equal. This is the three-point condition, and a distance that satisfies it for all triples is an ultrametric. Conversely, an ultrametric matrix is the distance matrix of exactly one rooted tree, not always binary, with all leaves at the same distance from the root, which [ultrametric tree reconstruction](/ultrametric-tree-reconstruction/) builds.

**The root.** Under a clock, the root is the point at the same distance from all leaves. So a clock roots the tree with no outgroup, and [midpoint rooting](/midpoint-rooting/) finds that point on a clock tree.

**The relative rate test.** Sarich and Wilson (1973) used an outgroup $C$ of two taxa $A$ and $B$. Under a clock, $d(A, C) = d(B, C)$, so the difference of the two distances measures how much faster one lineage has changed since $A$ and $B$ split.

**The likelihood ratio test.** Let $\ell_0$ be the maximum log likelihood of the tree under the clock and $\ell_1$ the maximum log likelihood of the same topology with free branch lengths. The clock model is the free model with $(2n - 3) - (n - 1) = n - 2$ equality constraints. Under the clock and for many sites, the statistic $2(\ell_1 - \ell_0)$ has about a chi-squared distribution with $n - 2$ degrees of freedom (Felsenstein 1981). Langley and Fitch (1974) gave an earlier test for counts of substitutions on the branches.

## Examples

**Distances on a clock tree.** Take the tree $((A{:}2, B{:}2){:}3, C{:}5)$, with times in millions of years (My), and $r = 0.01$ substitutions per site per My. The branch lengths are 0.02, 0.02, 0.03 and 0.05, and

| pair | $d$ under the clock | $d$ when B is twice as fast |
|---|---|---|
| A, B | 0.04 | 0.06 |
| A, C | 0.10 | 0.10 |
| B, C | 0.10 | 0.12 |

Under the clock, the two largest distances are equal, 0.10 and 0.10, so the matrix is ultrametric, and the split of A and B is at $0.04 / (2 \times 0.01) = 2$ My. If only the branch to B runs at twice the rate, its length is 0.04, and the two largest distances are 0.10 and 0.12. The relative rate test with C as the outgroup sees the difference $0.12 - 0.10 = 0.02$, which is the extra length of B's branch.

**A relative rate test by likelihood.** Suppose that, since A and B split, 10 substitutions are counted on the lineage of A and 24 on the lineage of B, and that the counts are Poisson. With free rates the means are 10 and 24. Under the clock both means equal $17$. The statistic is
$$2\Bigl(10 \ln \tfrac{10}{17} + 24 \ln \tfrac{24}{17}\Bigr) = 5.94,$$
with $n - 2 = 1$ degree of freedom for the three-taxon tree. The 5 percent critical value is 3.841, and the p-value is 0.015, so the test rejects the clock for this pair. For a clock test on five taxa there are 3 degrees of freedom, and the 5 percent critical value is 7.815.

**Proteins.** Zuckerkandl and Pauling compared hemoglobins and found that the number of amino acid differences grew roughly in proportion to the time since the split, as dated by fossils. This is the observation that gave the clock its name.

## Where it is used

- **Dating.** A clock calibrated by one dated split turns all distances into ages, which is the simplest form of [divergence time estimation](/divergence-time-estimation/).
- **Tree building.** [UPGMA](/upgma/) and [WPGMA](/wpgma/) assume a clock and give an ultrametric tree. On data far from a clock they can give a wrong topology, and [neighbor joining](/neighbor-joining/) does not need the assumption.
- **Rooting.** A clock gives the root without an outgroup, as in [midpoint rooting](/midpoint-rooting/) and [tree rooting](/tree-rooting/) in general.
- **Population genetics.** Coalescent models such as the [Kingman coalescent](/kingman-coalescent/) give genealogies with times, and a clock links these times to the number of differences between sequences.
- **Model testing.** The likelihood ratio test of the clock is a standard check before a strict clock analysis. When it fails, a [relaxed clock](/relaxed-molecular-clock/) lets the rate vary across branches.

## References
