---
tag: 4AHTW8
kind: algorithm
slug: over-representation-analysis
name: Over-representation analysis
aliases:
- hypergeometric enrichment test
- gene ontology enrichment
area: biology/transcriptomics
level: intro
summary: Test whether a gene set has more members in a list of selected genes than chance predicts, with a hypergeometric test per set.
model: real-ram
complexity:
  vars: {u: the number of genes in the universe, s: the number of gene sets}
  time: {worst: Θ(s u + s log s), best: Θ(u + s log s)}
  space: {extra: Θ(u + s)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1935
  people: [Ronald A. Fisher]
  note: Fisher described the exact test for a 2 by 2 table, whose null law is hypergeometric, with the experiment of the lady tasting tea in The Design of Experiments in 1935. Its use for lists of genes and categories such as Gene Ontology terms became common with microarrays in the early 2000s.
prereqs: [fisher-exact-test, benjamini-hochberg-procedure]
see_also: [gene-set-enrichment-analysis, fisher-exact-test, differential-expression-analysis, benjamini-hochberg-procedure, false-discovery-rate, multiple-comparisons-problem, permutation-test, weighted-gene-coexpression-network-analysis]
sources:
  - paper: doi:10.1186/gb-2010-11-2-r14
    title: Matthew D. Young, Matthew J. Wakefield, Gordon K. Smyth and Alicia Oshlack, Gene ontology analysis for RNA-seq, accounting for selection bias, Genome Biology 11(2) (2010), article R14
    locator: the bias of RNA-seq toward calling long and highly expressed genes, the probability weighting function fitted against gene length, and the weighted null distribution that corrects the bias
  - paper: doi:10.1093/bioinformatics/btm051
    title: Jelle J. Goeman and Peter Bühlmann, Analyzing gene expression data in terms of gene sets, methodological issues, Bioinformatics 23(8) (2007), pages 980 to 987
    locator: competitive and self-contained null hypotheses, and the assumption of independent genes behind tests that sample genes, such as the hypergeometric test
  - paper: doi:10.1073/pnas.0506580102
    title: Aravind Subramanian, Pablo Tamayo, Vamsi K. Mootha and others, Gene set enrichment analysis, a knowledge-based approach for interpreting genome-wide expression profiles, PNAS 102(43) (2005), pages 15545 to 15550
    locator: the critique of methods that depend on an arbitrary cutoff for the list of selected genes
---

Over-representation analysis asks, for each gene set in a collection, whether a list of selected genes, usually the genes found by [differential expression analysis](/differential-expression-analysis/), contains more members of the set than a random list of the same size would. The gene sets come from databases of pathways, of Gene Ontology terms, or of targets of a regulator. For each set, the number of members in the list is compared with the hypergeometric distribution, which is the law of that number when the list is a uniformly random subset of the universe of genes. The p-value is the one-sided [Fisher exact test](/fisher-exact-test/) on a 2 by 2 table, and the p-values of all sets are then adjusted for multiple testing. Gene Ontology is one source of gene sets, so "gene ontology enrichment" names the most common use, not a different method. Unlike [gene set enrichment analysis](/gene-set-enrichment-analysis/), which uses the ranking of all genes, over-representation analysis needs a cutoff that splits the genes into selected and not selected.

## In plain words

You have found 200 genes that changed in an experiment, out of 10,000 that you measured. A pathway has 50 genes, and 8 of them are in your list. Is that a lot? If you had picked 200 genes at random, you would expect 1 of them in the pathway. So 8 looks like a lot, and the test tells you exactly how unlikely 8 or more would be by chance. You do this for every pathway in your database, and then correct for doing thousands of tests. The answer depends on what "all genes" means: it must be the genes you could have found, not every gene in the genome.

## The problem

**Input.** A universe $U$ of $N$ genes, the genes that were measured and could have been selected; a list $D$ of selected genes; and a collection of gene sets $S_1, \dots, S_s$.

**Output.** For each gene set $S$: the number $K = |S \cap U|$ of its members in the universe, the number $k = |S \cap D|$ of selected members, the expected number $nK/N$ with $n = |D \cap U|$, a p-value, and an adjusted p-value.

**Null hypothesis.** The selected list is a uniformly random subset of $U$ of size $n$, independent of membership in $S$. This is a competitive hypothesis in the sense of Goeman and Bühlmann (2007): it compares the set with the other genes, and it treats the genes, not the samples, as the units.

## The algorithm

```pseudo id=main
ORA(D, U, sets)
L1  D ← D ∩ U;  N ← |U|;  n ← |D|                     ▷ drop genes outside the universe
L2  for each gene set S in sets do
L3      S ← S ∩ U;  K ← |S|;  k ← |S ∩ D|
L4      p_S ← Σ_{i=k}^{min(K, n)} C(K, i) C(N - K, n - i) / C(N, n)   ▷ hypergeometric upper tail
L5  q ← BENJAMINI-HOCHBERG(p)
L6  return (k, K, nK/N, p_S, q_S) for each set
```

Line L1 cuts the list to the universe, because a gene that could not have been measured cannot count. Line L3 does the same for each set, so that $K$ counts only the members that could have been selected. Line L4 sums the hypergeometric probabilities of $k$ or more selected members. The code computes the sum with exact integers and divides once, so no rounding happens before the final conversion. Line L5 adjusts the p-values of all tested sets with the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/). The code also skips sets with fewer than a given number of members in the universe, a common filter.

## Example

The universe is $U = \{g_1, \dots, g_{20}\}$, so $N = 20$. The list is $g_1, \dots, g_5$ and a gene $x_1$ that is not in $U$, so line L1 drops $x_1$ and $n = 5$.

| set | members | $K$ | $k$ | expected | p | q |
|---|---|---|---|---|---|---|
| A | $g_1, g_2, g_3, g_6$ | 4 | 3 | 1 | 0.0320 | 0.0960 |
| B | $g_4, g_7, \dots, g_{11}$ | 6 | 1 | 1.5 | 0.871 | 1 |
| C | $g_{12}, g_{13}, y_1$ | 2 | 0 | 0.5 | 1 | 1 |

For set A, $P(X \ge 3) = (\binom43\binom{16}{2} + \binom44\binom{16}{1})/\binom{20}{5} = (480 + 16)/15504 = 31/969 = 0.0320$. For set B, $P(X \ge 1) = 1 - \binom{14}{5}/\binom{20}{5} = 1 - 2002/15504 = 0.871$. Set C loses $y_1$ at line L3, so $K = 2$. The adjusted value of A is $3 \cdot 0.0320/1 = 0.0960$. So at a target of 0.05, no set is called, although A has three times the expected number of selected genes. With only 20 genes, the test has little power.

## Correctness

The [proof](proofs/correctness.md) shows that the value of line L4 is the exact probability that a uniformly random subset of $U$ of size $n$ has at least $k$ members in $S$, so it is a valid p-value for the null hypothesis above: $P(p_S \le a) \le a$ for every $a$, with equality only at the attainable values, since the law is discrete. It shows that this is also the p-value of the one-sided Fisher exact test, by writing the table as two independent binomial counts with the same success probability and conditioning on their sum. The Benjamini-Hochberg step controls the false discovery rate when the p-values are independent or positively dependent. Gene sets overlap and genes are correlated, so for real collections this control is a heuristic, not a theorem.

## Complexity

On a [real RAM](/real-ram/), with hash sets, line L1 takes $O(u)$ time, where $u = N$ is the size of the universe. For a set of $K$ members, line L3 takes $O(K)$ time, and line L4 takes $O(\min(K, n))$ arithmetic operations if each term is computed from the previous one by the ratio of binomial coefficients. Since $K \le u$, the loop takes $O(su)$ time in the worst case and less when the sets are small. The adjustment at line L5 sorts the $s$ p-values, in $\Theta(s\log s)$ time. The code uses exact integers, whose cost grows with their length; this does not change the result, only the time on large inputs. The extra space is $\Theta(u + s)$.

## Properties

- **Exact.** The p-value is exact under the null hypothesis of a random list, with no approximation.
- **One-sided.** It tests for more selected members than expected. Depletion needs the lower tail.
- **Conservative for discrete data.** Since the law is discrete, $P(p_S \le a)$ is often less than $a$, so the test is valid but loses some power.
- **Depends on the cutoff.** The list $D$ comes from a threshold on the results of another analysis. Different thresholds give different lists and different answers.
- **Depends on the universe.** The p-value changes with $N$ even when $D$ and $S$ stay the same.

## Variants and improvements

- **Chi-squared or z approximation.** For large counts, the 2 by 2 table can be tested with a chi-squared test. The exact sum is cheap, so there is little reason to approximate.
- **Up and down lists.** Test the genes that went up and the genes that went down separately, since a pathway can be activated or repressed.
- **Length bias correction.** In RNA-seq, long and highly expressed genes have more reads, so they are more likely to be called. Young et al. (2010) estimate the probability of selection as a function of gene length and use a weighted null distribution, so that a set of long genes is not enriched only because of length.
- **Using the structure of the ontology.** Gene Ontology terms are nested, so a specific term and all terms above it are often called together. Some methods remove genes already explained by a more specific term before testing a more general one.
- **Ranked methods.** [Gene set enrichment analysis](/gene-set-enrichment-analysis/) uses the whole ranking and needs no cutoff. Methods such as CAMERA test sets with the sample correlation between genes taken into account.

## When to use it

Use it when the result of an analysis is a list of genes, not a ranking: the genes of a cluster or a module of [WGCNA](/weighted-gene-coexpression-network-analysis/), the targets of a factor from a binding experiment, or the genes near variants found in a genetic study. It is fast and easy to explain. When you have a statistic for every gene, a ranked method usually uses the data better, because it does not throw away the information below the cutoff.

## Pitfalls

- **The wrong universe.** Using all genes in the genome as the universe, when only the expressed genes could be selected, makes almost every set of expressed genes look enriched. The universe must be the genes that were measured and passed the filters.
- **Genes outside the universe.** Genes of the list or of a set that are not in the universe must be removed before counting, as lines L1 and L3 do.
- **Correlated genes.** The test treats the genes as independent units. Genes in a pathway are often correlated across samples, so they tend to be selected together, and the test gives p-values that are too small for the claim that the condition affects the pathway.
- **Many overlapping sets.** Thousands of nested terms are tested, so many significant terms say the same thing. Report the overlap, or reduce the collection first.
- **Small and large sets.** Very small sets give few attainable p-values, and very large sets, such as "cellular process", are rarely informative. Filter by size before testing, and report the filter.
- **Length bias.** For RNA-seq lists, ignoring the length bias favours long genes.

## Implementations

## History

Fisher described the exact test for a 2 by 2 table, whose null law is hypergeometric, in 1935. After the Gene Ontology was published in 2000 and microarrays gave long lists of changed genes, many tools tested the terms and pathways of a database for enrichment in a list, mostly with this test or the chi-squared test. Goeman and Bühlmann (2007) showed that such tests sample genes rather than subjects, and so assume that genes are independent. Young et al. (2010) corrected the length bias of RNA-seq. Subramanian et al. (2005) proposed gene set enrichment analysis, partly to remove the need for a cutoff.

## References
