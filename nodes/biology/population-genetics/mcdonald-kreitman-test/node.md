---
tag: 4QSXZX
kind: algorithm
slug: mcdonald-kreitman-test
name: McDonald-Kreitman test
aliases:
- MK test
area: biology/population-genetics
level: core
summary: Compare the ratio of nonsynonymous to synonymous changes within species and between species in a 2 x 2 table to detect adaptive evolution.
model: real-ram
complexity:
  vars: {n: the number of sequences, c: the number of codons, m: the number of counted changes}
  time: {worst: Θ(n c + m), average: Θ(n c + m), best: Θ(n c + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1991
  people: [John H. McDonald, Martin Kreitman]
  note: McDonald and Kreitman proposed the test in 1991 and applied it to the Adh gene of three Drosophila species, where they found an excess of fixed amino acid differences.
prereqs: [dn-ds-ratio, fisher-exact-test, infinite-sites-model]
see_also: [nei-gojobori-method, tajimas-d, codon-substitution-model, extended-haplotype-homozygosity, kimura-fixation-probability, coalescent-simulation, nucleotide-diversity]
sources:
  - paper: doi:10.1038/351652a0
    title: John H. McDonald and Martin Kreitman, Adaptive protein evolution at the Adh locus in Drosophila, Nature 351(6328), 1991
    locator: pp. 652-654 (the 2 x 2 table of fixed and polymorphic, replacement and synonymous changes, and the Adh data)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 11 (neutral and adaptive protein evolution)
---

The McDonald-Kreitman test asks whether the amino acid changes in a gene fixed between two species more often than neutral theory allows. It counts four kinds of changes in an alignment of coding sequences from two species: nonsynonymous and synonymous fixed differences between the species, $D_n$ and $D_s$, and nonsynonymous and synonymous polymorphisms within the species, $P_n$ and $P_s$. Under neutrality, a change is nonsynonymous with the same probability whether it ends up fixed or polymorphic, so $D_n / D_s$ and $P_n / P_s$ have the same expected value. A 2 x 2 test of independence, usually [Fisher's exact test](/fisher-exact-test/), tests this. An excess of nonsynonymous fixed differences points to adaptive evolution. McDonald and Kreitman introduced the test in 1991.

## In plain words

Take a gene from a few individuals of two related species. Some differences are inside a species: some individuals have one base, some another. Others are between the species: all individuals of one species have one base, all of the other species have another. Each difference is also either silent (the protein stays the same) or a change of amino acid.

If all these changes were neutral, the share of amino acid changes would be the same in both groups, because a mutation does not know if it will become fixed. If selection favoured new amino acids, those changes would spread fast to fixation and would be rare as polymorphisms, so the share of amino acid changes would be higher among the fixed differences. The test checks whether the two shares differ by more than chance.

## The problem

**Input.** Aligned, in-frame coding sequences of $n_A \ge 1$ individuals of species A and $n_B \ge 1$ of species B, with $c$ codons each and no stop codons. For a test with power, at least one species needs several sequences.

**Output.** The table

| | nonsynonymous | synonymous |
|---|---|---|
| fixed | $D_n$ | $D_s$ |
| polymorphic | $P_n$ | $P_s$ |

the p-value of a test of independence of rows and columns, the neutrality index $\mathrm{NI} = (P_n / P_s)/(D_n / D_s)$, and $\alpha = 1 - \mathrm{NI} = 1 - \frac{D_s P_n}{D_n P_s}$, an estimate of the fraction of amino acid substitutions that were adaptive.

**The counting rule of the implementation.** A codon is used when all sequences have a codon there and exactly one of its positions varies over all sequences. The change is synonymous if all the codons seen at that place code the same amino acid. It is polymorphic if the site varies inside A or inside B, and fixed if each species has one base and the two differ. Codons with two or more varying positions are skipped and reported, because the order of the changes is unknown. Programs differ in how they handle such codons, for example by the pathways of the [Nei-Gojobori method](/nei-gojobori-method/).

## The algorithm

```pseudo id=main
MK-TEST(A, B)
L1  D_n ← D_s ← P_n ← P_s ← 0
L2  for each codon where exactly one position varies over all sequences do
L3      syn ← all the codons at this place code the same amino acid
L4      if the site varies within A or within B then add 1 to P_n (not syn) or P_s (syn)
L5      else add 1 to D_n (not syn) or D_s (syn)
L6  p ← the two-sided Fisher exact p-value of [[D_n, D_s], [P_n, P_s]]
L7  NI ← (P_n / P_s) / (D_n / D_s); α ← 1 − NI
L8  return the table, p, NI and α
```

Line L6 enumerates the tables with the same margins. With $r_1 = D_n + D_s$, $r_2 = P_n + P_s$ and $c_1 = D_n + P_n$, a table with $k$ in the top left cell has weight $\binom{r_1}{k}\binom{r_2}{c_1 - k}$, and the p-value is the total weight of the tables with weight at most that of the observed one, over $\binom{r_1 + r_2}{c_1}$. The implementation does this in exact integers, so ties are exact. Line L7 is undefined when $D_n$, $D_s$ or $P_s$ is 0.

## Example

**A small alignment.** Species A has three sequences and species B has two, of six codons:

| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| A1 | ATG | GCT | TTA | CCT | GAA | AAA |
| A2 | ATG | GCC | TTA | CCT | GAA | AAA |
| A3 | ATG | GCT | TTA | CCT | GAA | AGA |
| B1 | ATG | GCT | CTA | CCT | GAT | AAA |
| B2 | ATG | GCT | CTA | CCT | GAT | AAA |

Codon 2 varies inside A, GCT and GCC both code Ala: a synonymous polymorphism. Codon 6 varies inside A, AAA (Lys) and AGA (Arg): a nonsynonymous polymorphism. Codon 3 is TTA in all of A and CTA in all of B, both Leu: a synonymous fixed difference. Codon 5 is GAA (Glu) in A and GAT (Asp) in B: a nonsynonymous fixed difference. So $D_n = D_s = P_n = P_s = 1$, $\mathrm{NI} = 1$, $\alpha = 0$ and $p = 1$.

**The Adh data.** McDonald and Kreitman counted, for the alcohol dehydrogenase gene of *Drosophila melanogaster*, *D. simulans* and *D. yakuba*, $D_n = 7$, $D_s = 17$, $P_n = 2$ and $P_s = 42$. Among fixed differences, $7/24 = 29\%$ change the amino acid; among polymorphisms only $2/44 = 4.5\%$ do. The margins are $r_1 = 24$, $r_2 = 44$ and $c_1 = 9$, and the two-sided Fisher p-value is $8206423/1120001480 = 0.0073$. The neutrality index is $\frac{2/42}{7/17} = 0.116$, and $\alpha = 0.884$: by this estimate, most of the amino acid substitutions between the species were adaptive.

## Correctness

Lines L2 to L5 put every counted change in exactly one of the four cells, by the counting rule. Line L6 is Fisher's exact test, so the p-value is exact for the null hypothesis that, given the margins, the table has the hypergeometric law.

The test is valid under its null model because of one fact. Suppose the region does not recombine, every mutation is at a new site, and every nonsynonymous mutation is either neutral or so harmful that it never appears in the sample. Then mutations fall on the genealogy of the sample as a Poisson process, and the kind of a mutation (nonsynonymous with probability $f$, the same everywhere) is independent of where on the genealogy it falls. Where it falls decides whether it is fixed or polymorphic. So, given the numbers of fixed and polymorphic changes, $D_n$ and $P_n$ are independent binomials with the same $f$, and given also $D_n + P_n$, $D_n$ is hypergeometric: exactly the null law of Fisher's test. The full proof is below.

## Complexity

- **Counting.** Lines L2 to L5 read every base once and use sets of at most four bases and 21 amino acid codes per codon: $\Theta(n c)$ for $n = n_A + n_B$ sequences.
- **The test.** Line L6 has at most $m + 1$ tables, where $m = D_n + D_s + P_n + P_s$, each with a product of two binomial coefficients. With the weights updated from one table to the next by a ratio, it costs $\Theta(m)$ arithmetic operations on integers of $O(m)$ bits. The implementation calls `comb` for each table, which is simpler and a little slower.
- **Space.** The counters and the codons of one column: $\Theta(n)$; the enumeration needs $O(m)$ for its integers.

## Properties

- **Robust to the genealogy.** The test does not need the tree, the population size or the demographic history, because these act on both kinds of mutations in the same way. This makes it more robust to demography than tests on the frequency spectrum, such as [Tajima's D](/tajimas-d/).
- **A direction.** $\mathrm{NI} < 1$ (an excess of nonsynonymous fixed differences) points to adaptive evolution. $\mathrm{NI} > 1$ (an excess of nonsynonymous polymorphism) points to slightly deleterious variants that segregate but rarely fix.
- **Conservative.** Fisher's test conditions on both margins and is conservative for two independent binomials; the tests show a rejection rate below the nominal level under the null.
- **Little power for one gene.** Counts are often small; power comes from genes with many changes or from pooling over genes.
- **Biased alpha.** The ratio estimate $\alpha$ is biased when counts are small, because it is a ratio of random counts.

## Variants and improvements

- **G test and chi-squared test.** The same table can be tested with a G test or a chi-squared test of independence. With large counts they agree with Fisher's test.
- **Removing rare polymorphisms.** Slightly deleterious nonsynonymous variants are mostly at low frequency. Leaving out polymorphisms below a frequency cutoff, such as 5%, reduces the downward bias of $\alpha$.
- **Asymptotic MK.** Messer and Petrov (2013) compute $\alpha$ as a function of the frequency cutoff and extrapolate to frequency 1.
- **Pooling over genes.** Estimators of $\alpha$ over many genes, such as that of Smith and Eyre-Walker (2002), combine the counts with weights to reduce the small-count bias.
- **Distribution of fitness effects.** Methods such as DFE-alpha (Eyre-Walker and Keightley) fit a model of the effects of new mutations to the polymorphism frequencies and use it to predict the neutral expectation of $D_n$.

## When to use it

Use it to test a gene, or a set of genes, for adaptive amino acid evolution between two closely related species, when there are polymorphism data for at least one of them. It is the standard first test of positive selection that combines polymorphism and divergence. For divergence only, use [dN/dS](/dn-ds-ratio/) with a [codon substitution model](/codon-substitution-model/); for recent selection within a population, use haplotype statistics such as [extended haplotype homozygosity](/extended-haplotype-homozygosity/).

## Pitfalls

- **Slightly deleterious mutations.** They raise $P_n$ more than $D_n$ and push $\alpha$ down, even to negative values; with a recent increase in population size, they can also fix more in the past than now and give a false signal of adaptation.
- **Demography is not fully harmless.** Changes of population size between the time of divergence and today change how many weakly selected mutations fix and how many segregate. The test is robust only when all nonsynonymous mutations are neutral or strongly deleterious.
- **Distant species.** Multiple hits at the same site, especially at synonymous sites, make the fixed counts too low. Use closely related species.
- **Recombination.** With recombination, sites in different parts of the gene have different genealogies. The null law then also needs synonymous and nonsynonymous sites to be mixed evenly along the gene, which is usually close to true inside one gene.
- **Codon usage selection.** Selection on synonymous codons breaks the assumption that synonymous changes are neutral.
- **Pooling across genes.** A simple sum of tables over genes with different ratios of polymorphism to divergence can give a false result (a Simpson's paradox); use stratified methods.

## Implementations

## History

McDonald and Kreitman published the test in Nature in 1991, with the Adh data from three Drosophila species, and it became one of the main tests of adaptive protein evolution. Later work moved from single genes to genome-wide estimates of $\alpha$, with methods that correct for slightly deleterious mutations.

## References
