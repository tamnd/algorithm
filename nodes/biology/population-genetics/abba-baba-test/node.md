---
tag: 7E0M5A
kind: algorithm
slug: abba-baba-test
name: ABBA-BABA test
aliases:
- Patterson's D statistic
- D-statistic for introgression
area: biology/population-genetics
level: advanced
summary: Count ABBA and BABA site patterns across four taxa. An excess of one over the other signals gene flow, since incomplete sorting is symmetric.
model: word-ram
complexity:
  vars: {n: the number of sites, g: the number of jackknife blocks}
  time: {worst: O(n + g), average: O(n + g), best: O(n + g)}
  space: {extra: O(g)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2010
  people: [Richard E. Green, David Reich, Nick Patterson, Eric Y. Durand, Montgomery Slatkin]
  note: "Green and coauthors used the excess of ABBA over BABA patterns in 2010 to show gene flow from Neanderthals into modern humans. Durand, Patterson, Reich and Slatkin derived the statistic and its null model in 2011, and Patterson and coauthors placed it among the f-statistics in 2012."
prereqs: [patterson-f-statistics, incomplete-lineage-sorting, jackknife-resampling]
see_also: [multispecies-coalescent, coalescent-theory, phylogenetic-tree, standard-error, z-test, local-ancestry-inference, population-structure-inference, maximum-likelihood-admixture-estimation]
sources:
  - paper: doi:10.1126/science.1188021
    title: Richard E. Green and coauthors, A draft sequence of the Neandertal genome, Science 328(5979), 2010
    locator: pp. 710-722 (the D statistic from ABBA and BABA counts of a Neandertal, two modern humans and a chimpanzee, with a block jackknife)
  - paper: doi:10.1093/molbev/msr048
    title: Eric Y. Durand, Nick Patterson, David Reich and Montgomery Slatkin, Testing for ancient admixture between closely related populations, Molecular Biology and Evolution 28(8), 2011
    locator: pp. 2239-2252 (the null model, the expectation of D under incomplete lineage sorting and under gene flow, and the form with sample allele frequencies)
  - paper: doi:10.1534/genetics.112.145037
    title: Nick Patterson and coauthors, Ancient admixture in human history, Genetics 192(3), 2012
    locator: pp. 1065-1093 (the D statistic as a normalized f4 statistic, and the block jackknife standard error)
  - paper: doi:10.1093/molbev/msu269
    title: Simon H. Martin, John W. Davey and Chris D. Jiggins, Evaluating the use of ABBA-BABA statistics to locate introgressed loci, Molecular Biology and Evolution 32(1), 2015
    locator: pp. 244-257 (D in small windows and the f_d estimator of the admixed fraction)
  - paper: doi:10.1073/pnas.1200567109
    title: Anders Eriksson and Andrea Manica, Effect of ancient population structure on the degree of polymorphism shared between modern human populations and ancient hominins, PNAS 109(35), 2012
    locator: pp. 13956-13960 (ancestral structure without later gene flow can give D different from 0)
---

The ABBA-BABA test, also called Patterson's D statistic, tests for gene flow between groups that are not sister groups on a tree. It takes three groups $P_1$, $P_2$, $P_3$ with the tree $((P_1, P_2), P_3)$ and an outgroup $O$. Call the allele of the outgroup A and the other allele B. At an ABBA site, $P_2$ and $P_3$ share B; at a BABA site, $P_1$ and $P_3$ share B. Both patterns come from gene trees that do not match the species tree, and under the null model of the test, which includes [incomplete lineage sorting](/incomplete-lineage-sorting/) but no gene flow, the two are equally likely. An excess of ABBA points to gene flow between $P_2$ and $P_3$. The statistic is $D = (\text{ABBA} - \text{BABA}) / (\text{ABBA} + \text{BABA})$, and its standard error comes from a block jackknife over the genome. The test is valid only under its null model: other demographic histories can also make $D$ differ from 0.

## In plain words

Take two closely related groups, a third group, and a distant group that shows the old form of each variant. Along the genome, the first or the second group sometimes shares a new variant with the third group by chance, because the old variation was not sorted when the groups split. Chance favors neither of the first two groups. So the number of variants that the first group shares with the third should be about the same as the number that the second group shares with the third.

If one of the two shares clearly more, some of its genome probably came from the third group, or went into it. The test counts the two kinds of sites, takes their difference, and asks if it is larger than chance along the genome allows.

## The problem

**Input.** For $n$ biallelic sites, the frequency $p_{1s}, p_{2s}, p_{3s}, p_{4s}$ of allele B (the allele that the outgroup does not usually carry) in samples of $P_1$, $P_2$, $P_3$ and $O$ at site $s$. For one sequence per group, each frequency is 0 or 1. A partition of the sites into $g$ blocks of adjacent sites.

**The counts.** Site $s$ adds

$$\text{ABBA}_s = (1 - p_{1s})\, p_{2s}\, p_{3s} (1 - p_{4s}), \qquad \text{BABA}_s = p_{1s} (1 - p_{2s})\, p_{3s} (1 - p_{4s})$$

to the two counts; these are the probabilities that one sequence drawn from each group shows the pattern. Then

$$D = \frac{\sum_s (\text{ABBA}_s - \text{BABA}_s)}{\sum_s (\text{ABBA}_s + \text{BABA}_s)}.$$

The numerator is $\sum_s (p_{2s} - p_{1s})\, p_{3s} (1 - p_{4s})$. When the outgroup carries only A, this is the [f-statistic](/patterson-f-statistics/) $f_4(P_2, P_1; P_3, O) = \sum_s (p_{2s} - p_{1s})(p_{3s} - p_{4s})$, so $D$ is a normalized $f_4$.

**Output.** $D$, its standard error $\widehat{\mathrm{SE}}$ and $Z = D / \widehat{\mathrm{SE}}$. A common rule calls $|Z| > 3$ significant.

## The algorithm

```pseudo id=main
ABBA-BABA(p_1, p_2, p_3, p_4, blocks)
L1  for each block j = 1..g do
L2      for each site s in block j: compute ABBA_s and BABA_s
L3      a_j ← Σ of ABBA_s over block j
L4      b_j ← Σ of BABA_s over block j
L5  A ← Σ_j a_j; B ← Σ_j b_j; D ← (A - B) / (A + B)
L6  for each block j: D_j ← ((A - a_j) - (B - b_j)) / ((A - a_j) + (B - b_j))
L7  SE ← sqrt((g - 1)/g · Σ_j (D_j - mean of D_j)²)
L8  Z ← D / SE
L9  return D, SE, Z
```

Lines L1 to L4 make one pass over the sites. Line L6 is the delete-one [jackknife](/jackknife-resampling/): the value of $D$ with block $j$ left out comes from the totals in $O(1)$ time. Line L7 is the jackknife variance. Sites in one block are linked and their patterns are correlated, so a standard error from independent sites would be too small. Blocks of several megabases, much longer than the range of linkage disequilibrium, are roughly independent. The code on this page recomputes $D$ for each left-out block with a generic jackknife, which costs $O(g^2)$ instead of $O(g)$ and gives the same values.

## Example

**Counting.** With single sequences

```
P1  A A C G T A
P2  G A C G T T
P3  G T C A T T
O   A A G A T A
```

site 1 is ABBA (P1 has the allele of O, P2 and P3 the other one), site 6 is ABBA too, site 3 is BBBA, site 4 is BBAA, and sites 2 and 5 are not informative. So ABBA = 2 and BABA = 0. Swapping $P_1$ and $P_2$ swaps the two counts and changes the sign of $D$.

**The jackknife.** Four blocks with $(a_j, b_j) = (3, 1), (2, 2), (4, 0), (1, 1)$ give $A = 10$, $B = 4$ and $D = 6/14 = 0.4286$. Leaving out each block gives $D_j = 0.4, 0.6, 0.2, 0.5$, with mean $0.425$. The squared deviations sum to $0.0875$, so $\widehat{\mathrm{SE}} = \sqrt{0.75 \cdot 0.0875} = 0.256$ and $Z = 1.67$. Even a large $D$ is not significant when it rests on a few blocks that disagree.

**A simulation.** In 20000 sites from a model with incomplete lineage sorting and no gene flow, the counts were 1470 ABBA and 1536 BABA, with $D = -0.022$ and $Z = -1.37$. When 10 percent of the sites of $P_2$ came from $P_3$, the counts were 1749 and 1413, with $D = 0.106$ and $Z = 6.5$.

## Correctness

The arithmetic is direct: lines L1 to L5 compute the sums in the definition, line L6 computes $D$ on the data without block $j$ because the totals are additive over blocks, and line L7 is the delete-one jackknife formula. The statistical claim is the expectation under the null model. If there is no gene flow, if the ancestral populations mated at random, and if each site has had at most one mutation, then the genealogy of one sequence from each of $P_1$, $P_2$, $P_3$ follows the [multispecies coalescent](/multispecies-coalescent/). The lineages of $P_1$ and $P_2$ either join in the ancestor of $P_1$ and $P_2$, and then no branch of the gene tree separates $\{2, 3\}$ or $\{1, 3\}$ from the rest, so the site can be neither ABBA nor BABA. Or they do not join there, and from then on the two lineages are in the same population and the rest of the process treats them the same way. Swapping their labels maps each ABBA history to a BABA history of the same probability, so $E[\text{ABBA}] = E[\text{BABA}]$. Because $D$ is a ratio, its mean is only close to 0, and the normal law of $Z$ is an approximation from many blocks. The full proof is below.

## Complexity

- **Counts.** One pass over the sites: $O(n)$ time.
- **Jackknife.** $O(g)$ with the totals of line L5. The block sums take $O(g)$ space.
- **Many tests.** For all choices of $(P_1, P_2, P_3)$ among $r$ groups, compute the allele frequencies once and each $D$ in $O(n)$: $O(r^3 n)$ in total.

## Properties

- **Sign.** $D > 0$ means $P_2$ and $P_3$ share more derived alleles than $P_1$ and $P_3$. The test does not say which way the gene flow went.
- **Range.** $-1 \le D \le 1$. Its size depends on the time since the split and on the amount of incomplete lineage sorting, so $D$ is not an estimate of the admixed fraction.
- **Antisymmetry.** Swapping $P_1$ and $P_2$ changes the sign of $D$ and of $Z$.
- **Robust to rate along the genome.** Both patterns need a mutation on an internal branch, so a region with a high mutation rate adds to both counts in the same proportion under the null.
- **Only informative sites count.** BBAA sites, which match the species tree, and singletons do not enter $D$.

## Variants and improvements

- **Frequencies.** The form with $p_{is}$ uses all sampled sequences and reduces the variance (Durand and coauthors 2011).
- **The admixed fraction.** Martin, Davey and Jiggins (2015) define $f_d$, which compares the observed numerator with the value under complete gene flow, as an estimate of the admixed fraction in a window. $f_4$ ratios give it on a genome scale.
- **Weighted jackknife.** With blocks of different sizes, a weighted delete-one jackknife gives each block a weight in proportion to its number of sites.
- **Five or more taxa.** Extensions test gene flow among more groups at once, for example the $D_{\text{FOIL}}$ statistics for five taxa.
- **Admixture graphs.** Several $f_4$ and $D$ values at once fit an admixture graph; see the [f-statistics](/patterson-f-statistics/).

## When to use it

Use it to test for gene flow between a group and one of two sister groups, when an outgroup is available and the sister groups split recently enough that incomplete lineage sorting is common. It works with one genome per group. To find which regions came from the other group, use [local ancestry inference](/local-ancestry-inference/) or window statistics such as $f_d$.

## Pitfalls

- **The null model is narrow.** Structure in the common ancestor of $P_1$ and $P_2$, for example a subdivided ancestral population in which $P_2$ split from a deme closer to $P_3$, can give $D \ne 0$ with no gene flow after the split (Eriksson and Manica 2012). A significant $Z$ rejects the null model, not every model without gene flow.
- **Unequal error rates.** Sequencing errors, ancient DNA damage, or mapping that favors the reference genome add false derived alleles to one group more than the other, and that biases $D$.
- **Recurrent mutation.** The null assumes each site mutated at most once. Many changes at one site, as at CpG sites or in distant groups, break the symmetry.
- **Blocks too short.** Blocks shorter than the range of linkage disequilibrium make $\widehat{\mathrm{SE}}$ too small and $Z$ too large.
- **Windows.** In small windows $D$ has a high variance and is largest where few sites are informative, so it is a poor statistic for scanning the genome.
- **The wrong tree.** If $P_1$ and $P_2$ are not sister groups, $D$ measures the tree, not gene flow.

## Implementations

## History

Green and coauthors (2010) compared a Neandertal genome with two modern humans and a chimpanzee. They found that non-African genomes share more derived alleles with the Neandertal than African genomes do, and gave the D statistic with a block jackknife standard error. Durand, Patterson, Reich and Slatkin (2011) derived the expectation of $D$ under the null model and under gene flow, and the form with allele frequencies. Patterson and coauthors (2012) wrote $D$ as a normalized $f_4$ statistic in ADMIXTOOLS. Later work studied its use in windows (Martin, Davey and Jiggins 2015) and the demographic models other than gene flow that give the same signal.

## References
