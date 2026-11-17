---
tag: DC6Q95
kind: algorithm
slug: extended-haplotype-homozygosity
name: Extended haplotype homozygosity
aliases:
- EHH
- integrated haplotype score
- iHS
area: biology/population-genetics
level: advanced
summary: Detect recent positive selection by how far haplotypes carrying an allele stay identical around it, compared with the other allele.
model: real-ram
complexity:
  vars: {n: the number of haplotypes, m: the number of markers}
  time: {worst: Θ(n m), average: O(n m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2002
  people: [Pardis C. Sabeti, David E. Reich, Eric S. Lander, Benjamin F. Voight, Jonathan K. Pritchard]
  note: Sabeti and coauthors defined EHH in 2002 to find recent selection at G6PD and CD40 ligand; Voight and coauthors integrated it over the map and compared the two alleles of each marker in 2006.
prereqs: [allele-frequency, genetic-drift, trapezoidal-rule]
see_also: [linkage-disequilibrium, haplotype-phasing, tajimas-d, mcdonald-kreitman-test, fixation-index, positional-burrows-wheeler-transform, coalescent-simulation]
sources:
  - paper: doi:10.1038/nature01140
    title: Pardis C. Sabeti and coauthors, Detecting recent positive selection in the human genome from haplotype structure, Nature 419(6909), 2002
    locator: pp. 832-837 (the definition of EHH for a core haplotype and its decay with distance)
  - paper: doi:10.1371/journal.pbio.0040072
    title: Benjamin F. Voight, Sridhar Kudaravalli, Xiaoquan Wen and Jonathan K. Pritchard, A map of recent positive selection in the human genome, PLoS Biology 4(3), 2006
    locator: e72, Materials and Methods (the integrated EHH of each allele, the log ratio and its standardization in frequency bins)
---

Extended haplotype homozygosity (EHH) measures how far around a marker the haplotypes that carry one allele stay identical. For the carriers of allele $a$ at a core marker, EHH at a marker $j$ is the fraction of pairs of carriers whose haplotypes are identical at every marker from the core to $j$. It is 1 at the core and decreases with distance, because recombination and mutation break the shared haplotypes. A new allele that a selective sweep has pushed to high frequency in a short time sits on long shared haplotypes, so its EHH decays slowly; a neutral allele at the same frequency is usually old, and its EHH decays fast. Sabeti and coauthors defined EHH in 2002. Voight and coauthors in 2006 took the area under the EHH curve of each allele (the integrated EHH, iHH) and used the log ratio of the two areas, standardized by allele frequency, as a genome-wide scan for recent selection.

## In plain words

Look at many copies of a chromosome from one population, each a string of 0s and 1s at the marker sites. Pick a site and collect the copies that carry the new allele there. Walk outward from the site, one marker at a time, and ask: what fraction of pairs of these copies are still identical over the whole stretch so far? That fraction is EHH.

If the allele is old, recombination over many generations has cut its copies into many short pieces, and EHH falls quickly. If the allele rose fast because it helped its carriers, there was little time for recombination, and the copies still share one long stretch. Comparing the area under the curve for the new allele with that for the old allele at the same site gives one number per site.

## The problem

**Input.** Phased haplotypes $h_1, \ldots, h_n$ of $m$ biallelic markers, with allele 0 (ancestral) or 1 (derived) at each, the map positions $x_1 < \cdots < x_m$ of the markers (genetic distance is best, physical distance is common), a core marker $c$, an allele $a$ with at least two carriers, and a cutoff $\epsilon \ge 0$ (often 0.05).

**Output.** With $C = \{i : h_i[c] = a\}$ and $k = |C| \ge 2$, the curve

$$\mathrm{EHH}_a(j) = \frac{\#\{\{i, i'\} \subseteq C : h_i[t] = h_{i'}[t] \text{ for all } t \text{ between } c \text{ and } j\}}{\binom{k}{2}}, \qquad j = 1, \ldots, m,$$

and the integrated EHH $\mathrm{iHH}_a$: the trapezoid area under $\mathrm{EHH}_a$ over the positions, taken outward from the core on each side and stopped at the first marker where $\mathrm{EHH}_a < \epsilon$. The score of the core is $\ln(\mathrm{iHH}_0 / \mathrm{iHH}_1)$. Voight and coauthors standardize it: from the score of each marker, subtract the mean and divide by the standard deviation of the scores of all markers with a similar derived allele frequency.

## The algorithm

The carriers are split into classes of identical extended haplotypes, and the classes are refined one marker at a time as the walk moves away from the core. A class of one haplotype adds no pair now or later, so it is dropped.

```pseudo id=main
EHH(H, x, c, a, ε)
L1  C ← the haplotypes with allele a at the core c; k ← |C| (at least 2)
L2  E[j] ← 0 for every marker j; E[c] ← 1
L3  for each side d in (+1, −1) do
L4      classes ← [C]; j ← c + d
L5      while 1 ≤ j ≤ m and classes is not empty do
L6          split each class by the allele at j and keep the parts with 2 or more haplotypes
L7          E[j] ← Σ over classes K of C(|K|, 2) / C(k, 2); j ← j + d
L8  iHH ← on each side, add (E[j] + E[j − d]) / 2 · |x[j] − x[j − d]| for j = c + d, c + 2d, ... up to the first j with E[j] < ε
L9  return E and iHH
```

The score of the core is $\ln(\mathrm{iHH}_0 / \mathrm{iHH}_1)$, with two calls of EHH, one for each allele. The implementation also reports, for each side, whether the data ended before EHH fell under $\epsilon$. The area of such a marker is cut short, and scans often leave such markers out.

## Example

Eight haplotypes with five markers at positions 0, 0.1, 0.2, 0.3 and 0.4 (in centimorgans), and the core at the middle marker 3:

| haplotype | 1 | 2 | 3 (core) | 4 | 5 |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 1 | 0 | 1 |
| 2 | 0 | 1 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 | 0 | 0 |
| 4 | 1 | 1 | 1 | 0 | 1 |
| 5 | 0 | 0 | 0 | 1 | 0 |
| 6 | 1 | 0 | 0 | 0 | 1 |
| 7 | 0 | 1 | 0 | 1 | 1 |
| 8 | 1 | 0 | 0 | 0 | 0 |

**Derived allele 1.** The carriers are haplotypes 1 to 4, with $\binom{4}{2} = 6$ pairs. At marker 4 all have 0, so EHH stays 1. At marker 5, haplotype 3 differs, and the class $\{1, 2, 4\}$ keeps 3 pairs: EHH $= 1/2$. On the left, marker 2 keeps all four, and at marker 1 haplotype 4 differs: EHH $= 1/2$. The curve is $(1/2, 1, 1, 1, 1/2)$.

**Ancestral allele 0.** The carriers are haplotypes 5 to 8. At marker 4 the classes are $\{5, 7\}$ and $\{6, 8\}$: EHH $= 2/6 = 1/3$. At marker 5 both classes split: EHH $= 0$. On the left, marker 2 leaves $\{5, 6, 8\}$: EHH $= 3/6 = 1/2$, and marker 1 leaves $\{6, 8\}$: EHH $= 1/6$. The curve is $(1/6, 1/2, 1, 1/3, 0)$.

**Areas with $\epsilon = 0.05$.** For allele 1, each side gives $\frac{1 + 1}{2} \cdot 0.1 + \frac{1 + 0.5}{2} \cdot 0.1 = 0.175$, so $\mathrm{iHH}_1 = 0.35$, and the data end before EHH falls under 0.05. For allele 0, the left side gives $0.075 + \frac{0.5 + 1/6}{2} \cdot 0.1 = 0.1083$, and the right side gives $\frac{1 + 1/3}{2} \cdot 0.1 = 0.0667$ and stops at marker 5, where EHH is 0. So $\mathrm{iHH}_0 = 0.175$ and the score is $\ln(0.175 / 0.35) = \ln 0.5 = -0.693$: the derived allele sits on longer shared haplotypes.

## Correctness

The proof keeps one invariant on each side: after the walk has processed marker $j$, the list of classes holds exactly the classes, of size 2 or more, of the relation "identical at every marker from the core to $j$" on the carriers. Line L6 keeps the invariant, because two carriers are identical up to $j$ exactly when they are identical up to the marker before $j$ and have the same allele at $j$. A pair of carriers that are identical up to $j$ lies in one class, so line L7 counts each such pair once, and the sum over classes of $\binom{|K|}{2}$ is the numerator of the definition. When the list is empty, no pair is identical up to $j$, so no pair is identical further out, and the zeros of line L2 are correct for the markers that the walk does not reach. Line L8 is the trapezoid rule on the points it visits. The full proof is below.

## Complexity

- **Time for one curve.** Line L1 reads one column: $\Theta(n)$. Each marker on the walk reads the allele of every haplotype that is still in a class, at most $k \le n$, so the walk costs $O(n m)$. It is $\Theta(n m)$ when the carriers share haplotypes over the whole region, for example when all are identical. When the classes empty fast, the walk stops after a few markers, and the cost is $\Theta(n + m)$ with the zeros of line L2.
- **Area.** Line L8 visits each marker at most once: $O(m)$.
- **A genome scan.** A score for every marker needs $m$ curves. With the walk of each curve stopped at the cutoff, the cost is the sum of the lengths of the walks, which is usually much less than $n m^2$ in real data.
- **Space.** The classes hold each carrier at most once, and E has $m$ entries: $\Theta(n + m)$.

## Properties

- **Values.** $\mathrm{EHH}_a(c) = 1$, and $\mathrm{EHH}_a$ does not increase as $j$ moves away from the core, because the relation only gets finer.
- **Meaning.** $\mathrm{EHH}_a(j)$ is the probability that two carriers drawn without replacement are identical from the core to $j$. If the haplotypes are independent and the markers are independent fair coins, its mean at $j$ markers from the core is $2^{-j}$.
- **Allele frequency matters.** Under neutrality, the expected length of the shared haplotypes of an allele depends on its frequency. This is why the score is standardized within frequency bins and not across the whole genome.
- **Both alleles in one sample.** The two alleles share the same local recombination rate and the same demographic history, so their comparison removes much of the effect of these factors.
- **Sign.** A large negative score marks a derived allele on unusually long haplotypes; a large positive score marks an ancestral allele on unusually long haplotypes. Scans often rank markers by the absolute value of the standardized score.

## Variants and improvements

- **Core haplotypes.** Sabeti and coauthors used as cores short haplotypes of several close markers, not single markers, and compared the EHH of one core haplotype with the combined EHH of the other core haplotypes (the relative EHH).
- **Between populations.** Sabeti and coauthors in 2007 compared the integrated EHH of the same marker in two populations (XP-EHH); Tang, Thornton and Stoneking defined a similar statistic (Rsb). These find sweeps that are complete or almost complete in one population, where the within-population score has little power because one allele is rare.
- **Haplotype counting statistics.** The number of distinct haplotypes and the haplotype homozygosity in a window (for example the H12 statistic of Garud and coauthors) find soft sweeps, where several haplotypes carry the favoured allele.
- **Unphased data.** Some programs compute versions of these statistics from unphased genotypes.
- **Fast software.** Programs such as rehh and selscan compute EHH and the scores for whole genomes, with different truncation rules and different ways to handle gaps in the marker map.

## When to use it

Use it to scan phased data from one population for recent and incomplete sweeps, where a favoured allele is at intermediate or high frequency and has not yet fixed. It finds only recent selection, because recombination breaks the long haplotypes within a number of generations of the order of one over the recombination rate of the region. This is a much shorter time scale than that of tests on divergence between species, such as the [McDonald-Kreitman test](/mcdonald-kreitman-test/). For complete sweeps, use comparisons between populations or the [site frequency spectrum](/site-frequency-spectrum/).

## Pitfalls

- **Phasing errors.** Switch errors in [haplotype phasing](/haplotype-phasing/) break long haplotypes and lower EHH.
- **Recombination rate.** EHH decays slowly in regions of low recombination even without selection. Use genetic map positions, or compare the two alleles at the same marker.
- **Ancestral allele.** The sign of the score depends on knowing which allele is ancestral, which usually comes from an outgroup and can be wrong.
- **Rare alleles.** With few carriers, EHH has few pairs and is very noisy. Scans leave out markers with a minor allele frequency below a threshold, such as 5%.
- **Edges and gaps.** At the end of a chromosome, or near a large gap between markers, the area is cut short or made too large. Mark such markers and treat them apart.
- **Demography.** Bottlenecks and admixture make long haplotypes too. The standardized score is an outlier measure, not a test with a known null distribution; check outliers with simulations under a fitted demographic model, for example with [coalescent simulation](/coalescent-simulation/).
- **Missing data.** The method needs a full haplotype matrix. Impute or remove missing calls before the scan.

## Implementations

## History

Sabeti and coauthors introduced EHH in 2002 and used it to show recent selection on haplotypes of G6PD and of the CD40 ligand gene, which are linked to resistance to malaria. Voight and coauthors in 2006 integrated EHH over the genetic map, took the log ratio for the ancestral and derived alleles of each marker, standardized it by frequency, and made a genome-wide map of candidate sweeps from the HapMap data. Later work extended the idea to comparisons between populations and to soft sweeps.

## References
