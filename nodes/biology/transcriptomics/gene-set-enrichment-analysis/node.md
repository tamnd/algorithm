---
tag: W39J2F
kind: algorithm
slug: gene-set-enrichment-analysis
name: Gene set enrichment analysis
aliases:
- GSEA
area: biology/transcriptomics
level: core
summary: Walk down the genes ranked by association and test whether a set's members gather at the top with a weighted Kolmogorov-Smirnov statistic.
model: real-ram
complexity:
  vars: {n: the number of genes, m: the number of samples, b: the number of permutations, s: the number of gene sets}
  time: {worst: Θ(b (n m + s n log n)), best: Θ(b (n m + s n log n))}
  space: {extra: Θ(n + s b)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Vamsi K. Mootha, Aravind Subramanian, Pablo Tamayo, Jill P. Mesirov]
  note: Mootha et al. introduced the method in Nature Genetics in 2003, with an unweighted Kolmogorov-Smirnov statistic, and found that genes of oxidative phosphorylation are lower in muscle of people with diabetes. Subramanian et al. gave the weighted score, the normalized score and the software in PNAS in 2005.
prereqs: [kolmogorov-smirnov-test, permutation-test, differential-expression-analysis]
see_also: [over-representation-analysis, kolmogorov-smirnov-test, permutation-test, differential-expression-analysis, false-discovery-rate, moderated-t-statistic, multiple-comparisons-problem, weighted-gene-coexpression-network-analysis]
sources:
  - paper: doi:10.1073/pnas.0506580102
    title: Aravind Subramanian, Pablo Tamayo, Vamsi K. Mootha and others, Gene set enrichment analysis, a knowledge-based approach for interpreting genome-wide expression profiles, PNAS 102(43) (2005), pages 15545 to 15550
    locator: the weighted running sum, the enrichment score, the phenotype permutations, the nominal p-value from the part of the null distribution with the sign of the score, the normalized score, and the leading edge
  - paper: doi:10.1038/ng1180
    title: Vamsi K. Mootha, Cecilia M. Lindgren, Karl-Fredrik Eriksson and others, PGC-1 alpha-responsive genes involved in oxidative phosphorylation are coordinately downregulated in human diabetes, Nature Genetics 34(3) (2003), pages 267 to 273
    locator: the first form of the method, with a Kolmogorov-Smirnov statistic over the ranked genes and permutations of the sample labels
  - paper: doi:10.1093/bioinformatics/btm051
    title: Jelle J. Goeman and Peter Bühlmann, Analyzing gene expression data in terms of gene sets, methodological issues, Bioinformatics 23(8) (2007), pages 980 to 987
    locator: competitive and self-contained null hypotheses, and why permuting genes rather than samples ignores the correlation between genes
  - paper: doi:10.1214/07-AOAS101
    title: Bradley Efron and Robert Tibshirani, On testing the significance of sets of genes, Annals of Applied Statistics 1(1) (2007), pages 107 to 129
    locator: the maxmean statistic and restandardization, which combine the sample permutations with the gene randomization
  - paper: doi:10.1093/nar/gks461
    title: Di Wu and Gordon K. Smyth, Camera, a competitive gene set test accounting for inter-gene correlation, Nucleic Acids Research 40(17) (2012), article e133
    locator: the variance inflation of competitive tests from the correlation between genes, and a test that estimates it
---

Gene set enrichment analysis tests whether the members of a gene set tend to lie near the top or near the bottom of a ranking of all genes by their association with a phenotype. It does not need a cutoff. It walks down the ranked list, going up at each member of the set by an amount that depends on the member's score, and down at each other gene by a fixed step. The enrichment score is the point of the walk farthest from zero. With all members weighted equally, it is the signed two-sample [Kolmogorov-Smirnov statistic](/kolmogorov-smirnov-test/) of the positions of the members against the positions of the other genes. Its significance is assessed by a [permutation test](/permutation-test/) that shuffles the sample labels and recomputes the ranking, which keeps the correlation between genes. Mootha et al. (2003) introduced it, and Subramanian et al. (2005) gave its standard form. Unlike [over-representation analysis](/over-representation-analysis/), which counts members in a list cut at a threshold, it uses the full ranking, so a set of many genes that each change a little can be found.

## In plain words

Sort all your genes from the most increased to the most decreased. Now take a pathway and mark its genes on that sorted list. If the pathway does not matter, its genes are spread evenly. If it matters, they bunch up near one end. To measure the bunching, walk down the list with a counter. Each time you pass a pathway gene, the counter goes up, more for genes with large changes. Each time you pass another gene, it goes down a little. The highest point the counter reaches is the score. To see whether that score is large, shuffle which samples are cases and which are controls many times, and see how often a shuffle gives a score as large.

## The problem

**Input.** An expression matrix of $n$ genes in $m$ samples, a label per sample (group A or B), and a collection of $s$ gene sets.

**Output.** For each gene set: the enrichment score ES, the normalized score NES, a p-value, and the leading edge, the members that account for the score.

**The walk.** Let the genes in order of decreasing score be $g_1, \dots, g_n$, with scores $r_1 \ge \dots \ge r_n$. Let $S$ have $N_H$ members, and let $N_R = \sum_{g_j \in S}|r_j|^p$. The running sum is
$$P(i) = \sum_{j \le i,\ g_j \in S}\frac{|r_j|^p}{N_R} - \sum_{j \le i,\ g_j \notin S}\frac{1}{n - N_H},$$
and ES is the value of $P(i)$ with the largest absolute value. The exponent $p$ is 1 by default; $p = 0$ gives the unweighted walk.

## The algorithm

```pseudo id=main
ENRICHMENT-SCORE(genes, r, S, p)
L1  order the genes by decreasing r, keeping the given order for equal scores
L2  w_j ← |r_j|^p for each member j of S;  N_R ← Σ w_j
L3  P ← 0;  ES ← 0
L4  for each gene j in that order do
L5      if j ∈ S then P ← P + w_j / N_R
L6      else P ← P - 1 / (n - N_H)
L7      if |P| > |ES| then ES ← P
L8  return ES
```

Line L1 ranks the genes. In the full method the scores $r$ are the signal-to-noise ratios $(\bar x_A - \bar x_B)/(\sigma_A + \sigma_B)$ of the genes, with the sample standard deviations. Line L2 sets the step of each member: with $p = 1$, members with large scores count more. Lines L4 to L7 walk down the list and keep the running sum farthest from 0. The steps up add to 1 and the steps down add to 1, so the walk ends at 0. If all members have score 0, the code gives them equal weights.

**Significance.** The full method repeats the computation for $b$ shuffles of the sample labels: each shuffle gives new signal-to-noise ratios, a new ranking and a null score $\mathrm{ES}^*$ per set. The code reports two p-values. The GSEA convention compares ES only with the null scores of the same sign: $p_{\text{sign}} = (1 + \#\{\mathrm{ES}^* \ge \mathrm{ES}\})/(1 + \#\{\mathrm{ES}^* \ge 0\})$ when $\mathrm{ES} \ge 0$, and the mirror image when it is negative. The second is the plain permutation p-value of the absolute score, $p_{\text{abs}} = (1 + \#\{|\mathrm{ES}^*| \ge |\mathrm{ES}|\})/(1 + b)$. The normalized score NES divides ES by the mean absolute value of the null scores of the same sign, so that sets of different sizes can be compared. The leading edge is the set of members at or before the peak of the walk, for a positive ES.

## Example

Eight genes, already ranked, with scores 2, 1.5, 1, 0.5, -0.2, -0.6, -1.2 and -2.5, and the set $S = \{g_1, g_3, g_6\}$. So $N_H = 3$, each other gene moves the walk down by $1/5 = 0.2$, and with $p = 1$, $N_R = 2 + 1 + 0.6 = 3.6$.

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| member | yes | no | yes | no | no | yes | no | no |
| step | 0.556 | -0.2 | 0.278 | -0.2 | -0.2 | 0.167 | -0.2 | -0.2 |
| $P(i)$ | 0.556 | 0.356 | 0.633 | 0.433 | 0.233 | 0.400 | 0.200 | 0 |

The peak is at $i = 3$, so $\mathrm{ES} = 0.633$ and the leading edge is $\{g_1, g_3\}$. With $p = 0$, each member adds $1/3$, and the peak is again at $i = 3$, with $\mathrm{ES} = 2/3 - 0.2 = 0.467$. This is the Kolmogorov-Smirnov statistic: at position 3, two of the three members and one of the five other genes have been passed, and $2/3 - 1/5 = 0.467$.

## Correctness

The [proof](proofs/correctness.md) shows that the walk starts and ends at 0 and stays in $[-1, 1]$, so ES lies in $[-1, 1]$. It shows that, with $p = 0$, ES is the signed two-sample Kolmogorov-Smirnov statistic of the positions of the members, which is the sense in which the method is a weighted Kolmogorov-Smirnov test. The order of equal scores can change ES, so the code fixes it. For significance, the proof shows that $p_{\text{abs}}$ is a valid p-value, $P(p_{\text{abs}} \le a) \le a$, when the sample labels are exchangeable under the null hypothesis: by a rank argument with exact enumeration of the labellings, and by exchangeability with random shuffles, where the added 1 in the numerator and the denominator is needed. The p-value $p_{\text{sign}}$ of the GSEA convention conditions on the sign of the null scores, and has no such guarantee. NES and the false discovery rates that GSEA computes from it are heuristics.

## Complexity

On a [real RAM](/real-ram/), one enrichment score takes $\Theta(n\log n)$ time for the sort at line L1 and $\Theta(n)$ for the walk. Each permutation computes the $n$ signal-to-noise ratios in $\Theta(nm)$ time and then the scores of the $s$ sets. The code sorts again for each set, so the total is $\Theta(b(nm + sn\log n))$. Sorting once per permutation and sharing the order between the sets lowers it to $\Theta(b(nm + n\log n + sn))$. The extra space is $\Theta(n)$ for the ranking and $\Theta(sb)$ for the null scores.

## Properties

- **No cutoff.** All genes count, and the result does not depend on a threshold for significance.
- **Sign.** A positive ES means that the members gather at the top, a negative ES at the bottom.
- **Weighted.** With $p = 1$, a few members with very large scores can produce a large ES alone. With $p = 0$ the statistic depends only on the ranks.
- **Sample permutation keeps the correlation.** Shuffling sample labels moves the values of all genes of a sample together, so the null distribution reflects the correlation between genes.
- **Few samples, few permutations.** With 3 samples per group, there are only 20 labellings, so $p_{\text{abs}}$ cannot be smaller than 0.05.

## Variants and improvements

- **Gene permutation.** Shuffle the membership of the genes instead of the sample labels, as preranked GSEA does when only a ranked list is available. This tests a competitive null hypothesis and needs no samples, but it treats genes as independent, so correlated sets get p-values that are too small (Goeman and Bühlmann 2007).
- **Other gene scores.** The signal-to-noise ratio can be replaced by a [moderated t-statistic](/moderated-t-statistic/) or a signed statistic from a count model, which handle few samples better.
- **Maxmean and restandardization.** Efron and Tibshirani (2007) proposed a simpler statistic, the larger of the mean positive part and the mean negative part of the scores in the set, and combined the sample permutations with a gene randomization.
- **CAMERA.** Wu and Smyth (2012) estimate the correlation between the genes of a set and correct the variance of a competitive test for it, without permutations.
- **Single-sample scores.** Methods such as ssGSEA compute a walk per sample, giving a score for each set in each sample, which can then be used as a new variable.

## When to use it

Use it when you have a statistic for every gene and want to know which pathways or programs move as a whole, especially when single genes change too little to pass a threshold. Use sample permutation when there are enough samples per group that the permutation p-values can be small. With fewer samples, use a ranked method that accounts for correlation, such as CAMERA, or interpret preranked results with care. When all you have is a list of genes, use [over-representation analysis](/over-representation-analysis/).

## Pitfalls

- **Which p-value.** $p_{\text{sign}}$ compares ES with only part of the null distribution, and it is not a valid p-value in general. State which p-value is reported.
- **Ties.** Many genes with the same score, such as genes with zero counts, make ES depend on their order. Break ties at random or remove such genes.
- **Few samples.** With few samples, the number of distinct labellings is small. GSEA then often falls back to gene permutation, with the problem above.
- **Large sets.** Very large sets almost always reach a moderate ES, and very small ones are noisy. Filter the sets by size before testing, and report the bounds.
- **Overlapping sets.** Many sets share their leading edge genes and so report the same signal. Look at the leading edges before reporting many sets.
- **Standard deviations near zero.** The signal-to-noise ratio is unstable when a gene barely varies. Filter such genes first.

## Implementations

## History

Mootha et al. (2003) introduced the method to find that genes of oxidative phosphorylation, each only slightly lower, were together lower in muscle from people with type 2 diabetes. That first form used an unweighted Kolmogorov-Smirnov statistic. Subramanian et al. (2005) added the weights, the normalized score, the leading edge and the MSigDB collection of gene sets, and released the software. Goeman and Bühlmann (2007), Efron and Tibshirani (2007) and Wu and Smyth (2012) analysed its null hypotheses and proposed alternatives.

## References
