---
tag: XEEEED
kind: technique
slug: patterson-f-statistics
name: Patterson f-statistics
aliases:
- f3 statistic
- f4 statistic
area: biology/population-genetics
level: advanced
summary: Moments of allele frequency differences among three or four populations that test for admixture and fit admixture graphs.
history:
  year: 2009
  people: [David Reich, Kumarasamy Thangaraj, Nick Patterson, Alkes L. Price, Lalji Singh]
  note: "Reich and coauthors used the three-population and four-population statistics in 2009 to show that most Indian groups are mixtures of two ancestral populations. Patterson and coauthors gave the full theory, the unbiased estimators and the fit of admixture graphs in 2012."
prereqs: [allele-frequency, fixation-index]
see_also: [abba-baba-test, jackknife-resampling, multispecies-coalescent, phylogenetic-network, population-structure-inference, genetic-drift, z-test, incomplete-lineage-sorting]
sources:
  - paper: doi:10.1534/genetics.112.145037
    title: Nick Patterson, Priya Moorjani, Yontao Luo, Swapan Mallick, Nadin Rohland, Yiping Zhan, Teri Genschoreck, Teresa Webster and David Reich, Ancient admixture in human history, Genetics 192(3), 2012
    locator: pp. 1065-1093 (the definitions of f2, f3 and f4, their unbiased estimators, the f4 ratio, the block jackknife, and the fit of admixture graphs)
  - paper: doi:10.1038/nature08365
    title: David Reich, Kumarasamy Thangaraj, Nick Patterson, Alkes L. Price and Lalji Singh, Reconstructing Indian population history, Nature 461(7263), 2009
    locator: pp. 489-494 (the three-population test of admixture and the four-population test of a tree, applied to Indian groups)
  - paper: doi:10.1126/science.1188021
    title: Richard E. Green and coauthors, A draft sequence of the Neandertal genome, Science 328(5979), 2010
    locator: pp. 710-722 (the D statistic and the estimate of the Neandertal fraction in non-Africans)
---

Patterson f-statistics are averages, over many biallelic sites, of products of allele frequency differences between populations. For populations with frequencies $a$, $b$, $c$, $d$ of one allele at a site, $f_2(A, B) = E[(a - b)^2]$, $f_3(C; A, B) = E[(c - a)(c - b)]$ and $f_4(A, B; C, D) = E[(a - b)(c - d)]$. When the populations are related by a tree with drift on its branches, $f_2$ is a sum of branch lengths along a path, $f_3$ is the length of one branch and is never negative, and $f_4$ is the shared length of two paths, so it is zero for a tree that splits $\{A, B\}$ from $\{C, D\}$. A significantly negative $f_3$ or a nonzero $f_4$ where a tree predicts zero is evidence of admixture. Reich and coauthors (2009) introduced the tests, and Patterson and coauthors (2012) gave the theory and the fit of admixture graphs.

## In plain words

Every population drifts, so the frequency of a gene variant moves up and down by chance over the generations. Two populations that split long ago have frequencies that differ more than two that split recently. The f-statistics measure how much of this random change two or more populations share.

If the populations sit on a simple family tree, the shared change follows fixed rules: some measures are never below zero, and some are always about zero. If a population is a mix of two others, its variant frequencies sit between theirs, and one of the measures turns negative. If gene flow joins two branches of the tree, a measure that should be zero is not. You compute the measures over many sites across the genome, estimate their error from large blocks of the genome, and check which tree, or which tree with mixing, fits.

## When it applies

- **Data.** Allele frequencies at many biallelic SNPs in each population, from sequences or arrays. The target population of an $f_3$ test needs at least two sampled gene copies for the bias correction.
- **Model.** The theory treats frequencies as changed by drift only along the branches. It holds when the sites were polymorphic before the populations split and new mutations on the branches are rare, as for SNPs that are old relative to the splits, or for SNPs found in an outgroup.
- **Question.** Is a population a mixture of two others? Do four populations fit a tree? What fraction of a population comes from a source? Which graph of splits and admixtures fits all the statistics?
- **Not for.** Dates of admixture, which need linkage information, or populations with very few sites, where the standard errors are large.

## The template

**The basic identities.** For any frequencies, expanding the squares gives
$$f_3(C; A, B) = \tfrac{1}{2}\big[f_2(C, A) + f_2(C, B) - f_2(A, B)\big],$$
$$f_4(A, B; C, D) = \tfrac{1}{2}\big[f_2(A, D) + f_2(B, C) - f_2(A, C) - f_2(B, D)\big].$$
So all f-statistics are linear in the $f_2$ values, and a model that predicts the $f_2$ values predicts all of them.

**On a tree.** If the frequencies drift independently along the branches of a tree, the frequency changes on different branches are uncorrelated with mean zero. Then $f_2(A, B)$ is the sum of the drift lengths of the branches on the path from $A$ to $B$, $f_3(C; A, B)$ is the length of the path from $C$ to the point where the paths to $A$ and $B$ split, which is at least zero, and $f_4(A, B; C, D)$ is the signed length of the overlap of the paths $A$ to $B$ and $C$ to $D$.

**Under admixture.** If $C$ is an exact mixture $c = \alpha a + (1 - \alpha) b$, then $c - a = (1 - \alpha)(b - a)$ and $c - b = \alpha (a - b)$, so
$$f_3(C; A, B) = -\alpha (1 - \alpha) f_2(A, B) < 0.$$
Drift in $C$ after the mixture adds a positive term, so a real mixture may still give $f_3 \ge 0$.

**Steps.**

1. Compute sample frequencies $\hat a$, $\hat b$, ... from $n_A$, $n_B$, ... gene copies at each site.
2. Compute the unbiased term per site. For $f_3$ it is $(\hat c - \hat a)(\hat c - \hat b) - \hat c (1 - \hat c) / (n_C - 1)$, since $E[(\hat c - c)^2] = c(1 - c)/n_C$ and $E[\hat c(1 - \hat c)] = c(1 - c)(1 - 1/n_C)$. For $f_2$ subtract the same term for each of the two populations. For $f_4$ of four distinct populations, no correction is needed, because the four samples are independent.
3. Average the terms over all sites. Patterson and coauthors often divide $f_3$ by an estimate of the heterozygosity of $C$, which makes values comparable across targets.
4. Estimate the standard error with a delete-one block [jackknife](/jackknife-resampling/) over blocks of several megabases, so that linked sites stay in one block.
5. Form $Z = \hat f / \widehat{\text{SE}}$ and compare it with the value that the tree predicts. A common rule treats $|Z| > 3$ as significant.

**The f4 ratio.** If $x = \alpha b + (1 - \alpha) c$ exactly, then $f_4(A, O; X, C) = E[(a - o)\,\alpha (b - c)] = \alpha \, f_4(A, O; B, C)$, so
$$\hat\alpha = \frac{f_4(A, O; X, C)}{f_4(A, O; B, C)}.$$
In practice $B$ and $C$ are relatives of the sources, and the estimate is unbiased when $A$ shares drift with the source related to $B$ only.

## Classic examples

- **Indian population history.** Reich and coauthors (2009) found negative $f_3$ for many Indian groups, with one source related to West Eurasians and one not, and modeled them as mixtures of two ancestral populations.
- **The ABBA-BABA test.** With the outgroup carrying only the ancestral allele, $o = 0$, the expected numerator of the D statistic at a site is $(1 - p_1) p_2 p_3 - p_1 (1 - p_2) p_3 = (p_2 - p_1) p_3 = (p_2 - p_1)(p_3 - o)$, which is $f_4(P_2, P_1; P_3, O)$. So the [ABBA-BABA test](/abba-baba-test/) is an $f_4$ test scaled by the count of informative sites. Green and coauthors (2010) used it to show gene flow from Neandertals into non-Africans.
- **A worked mixture.** Take three sites with $a = (0.1, 0.8, 0.5)$, $b = (0.7, 0.2, 0.9)$ and $c = (a + b)/2 = (0.4, 0.5, 0.7)$. The products $(c - a)(c - b)$ are $-0.09$, $-0.09$ and $-0.04$, so $f_3(C; A, B) = -0.22/3 \approx -0.0733$. The squares $(a - b)^2$ are $0.36$, $0.36$ and $0.16$, so $f_2(A, B) = 0.88/3 \approx 0.2933$, and $-\alpha(1 - \alpha) f_2 = -0.25 \cdot 0.2933 \approx -0.0733$, as the identity says.
- **The bias correction.** With $\hat c = 0.4$ from $n_C = 10$ copies, the correction for that site is $0.4 \cdot 0.6 / 9 \approx 0.0267$.

## Variations

- **Outgroup f3.** $f_3(O; A, B)$ with an outgroup $O$ measures the drift shared by $A$ and $B$ since they split from $O$, and is used to rank populations by how close they are to a target.
- **Admixture graphs.** The program qpGraph of Patterson and coauthors fits a graph of splits and admixture events to all $f_2$, $f_3$ and $f_4$ values at once, and reports the statistics that the graph fits worst. TreeMix fits a similar graph to a covariance matrix of frequencies.
- **qpAdm.** A set of $f_4$ statistics with a fixed set of outgroups tests whether a target is a mixture of given sources and estimates the fractions, using the rank of a matrix of $f_4$ values.
- **Relation to $F_{ST}$.** $f_2(A, B)$ is the numerator of a Hudson-type [fixation index](/fixation-index/), which divides it by $E[a(1 - b) + b(1 - a)]$, the probability that one copy from each population differs.
- **Coalescent view.** Under the [multispecies coalescent](/multispecies-coalescent/), the f-statistics are linear in the expected coalescence times of pairs of gene copies, which gives the same tree rules as the drift model above.

## Pitfalls

- **Positive $f_3$ is not evidence against admixture.** Drift in the target after the mixture adds a positive term that can hide the negative one.
- **Zero $f_4$ is not proof of a tree.** Gene flow in two directions can cancel.
- **Ascertainment.** SNPs found in one population bias the frequencies toward that population. The tree rules hold best for SNPs found in an outgroup.
- **Small targets.** With $n_C = 1$, the $f_3$ correction is undefined, and the test cannot be run on that target.
- **Order of the arguments.** $f_4(A, B; C, D) = -f_4(B, A; C, D) = f_4(C, D; A, B)$. Papers use different orders, so check the sign convention before reading a result.
- **Linked sites.** Sites close together are not independent, so a standard error that treats them as independent is too small. Use blocks larger than the scale of linkage disequilibrium.
- **Many tests.** Testing all triples or quadruples of many populations gives many false positives at $|Z| > 3$ unless the threshold is raised.

## Exercises

1. Prove the two identities that write $f_3$ and $f_4$ in terms of $f_2$.
2. Show that $f_4(A, B; C, D) = 0$ in expectation when $A$, $B$, $C$, $D$ drift independently on a tree that splits $\{A, B\}$ from $\{C, D\}$.
3. Show that $E[\hat c (1 - \hat c)] = c (1 - c)(1 - 1/n)$ for the frequency $\hat c$ of $n$ copies sampled with replacement from a population with frequency $c$, and derive the corrected $f_3$ term.
4. Let $C$ be a mixture with fraction $\alpha$ of $A$ and $1 - \alpha$ of $B$, followed by drift of length $t$ in $C$. Show that $f_3(C; A, B) = t - \alpha(1 - \alpha) f_2(A, B)$, and find the $t$ above which the test cannot detect the mixture.
5. Derive the f4 ratio, and show by an example that it is biased when $A$ shares drift with both sources.

## References
