---
tag: 3RY3K8
kind: technique
slug: phylogenetic-bootstrap
name: Phylogenetic bootstrap
aliases:
- Felsenstein bootstrap
- nonparametric bootstrap
area: biology/phylogenetics
level: core
summary: Resample the alignment columns with replacement, rebuild the tree from each resample, and report for each split the fraction of resamples whose tree contains it.
prereqs: [phylogenetic-tree-reconstruction, splits-of-a-tree]
see_also: [majority-rule-consensus, consensus-tree, bagging, maximum-parsimony, maximum-likelihood-phylogeny, bayesian-phylogenetic-inference, robinson-foulds-distance, monte-carlo-integration]
sources:
  - paper: doi:10.1111/j.1558-5646.1985.tb00420.x
    title: Joseph Felsenstein, Confidence limits on phylogenies, an approach using the bootstrap, Evolution 39(4), 1985, 783-791
    locator: the resampling of characters with replacement, the count of replicates that contain a group, and the majority-rule consensus of the replicate trees
  - paper: doi:10.1214/aos/1176344552
    title: B. Efron, Bootstrap methods, another look at the jackknife, Annals of Statistics 7(1), 1979, 1-26
    locator: the bootstrap as resampling from the empirical distribution
  - paper: doi:10.1093/sysbio/42.2.182
    title: David M. Hillis and James J. Bull, An empirical test of bootstrapping as a method for assessing confidence in phylogenetic analysis, Systematic Biology 42(2), 1993, 182-192
    locator: the simulation study that compares bootstrap proportions with the probability that a clade is correct
  - paper: doi:10.1093/molbev/mst024
    title: Bui Quang Minh, Minh Anh Thi Nguyen and Arndt von Haeseler, Ultrafast approximation for phylogenetic bootstrap, Molecular Biology and Evolution 30(5), 2013, 1188-1195
    locator: UFBoot, which scores the trees met during one likelihood search on each replicate by resampled site log likelihoods
  - paper: doi:10.1093/molbev/msx281
    title: Diep Thi Hoang, Olga Chernomor, Arndt von Haeseler, Bui Quang Minh and Le Sy Vinh, UFBoot2, improving the ultrafast bootstrap approximation, Molecular Biology and Evolution 35(2), 2018, 518-522
    locator: the improved ultrafast bootstrap and its option to guard against severe model violations
  - paper: doi:10.1038/s41586-018-0043-0
    title: F. Lemoine, J.-B. Domelevo Entfellner, E. Wilkinson, D. Correia, M. Davila Felipe, T. De Oliveira and O. Gascuel, Renewing Felsenstein's phylogenetic bootstrap in the era of big data, Nature 556, 2018, 452-456
    locator: the transfer bootstrap expectation, a support measure based on the transfer distance between splits
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 20, Bootstrap, jackknife, and permutation tests
---

The phylogenetic bootstrap measures how strongly an alignment supports each split of an inferred tree. It draws $m$ columns from the $m$ columns of the alignment, uniformly and with replacement, runs the same tree method on this resample, and repeats this $B$ times. The support of a split is the fraction of the $B$ trees that contain it. Felsenstein (1985) brought Efron's bootstrap to phylogenetics, and it is still the most common support value on published trees. The method treats the sites as independent draws from one distribution, so a resample of the columns plays the part of a new data set from the same source.

## In plain words

You have one alignment and one tree built from it. You want to know which branches of the tree you can trust. If you had many alignments from the same genes, you could build a tree from each and see which branches come back each time. You have only one.

So you make fake alignments from the real one. Pick columns of the alignment at random, one at a time, and put each copy back so that it can be picked again, until the fake alignment is as long as the real one. Some columns appear twice and some not at all. Build a tree from it with the same method. Do this a thousand times. A branch that is in 95 percent of these trees has bootstrap support 95.

## When it applies

The model is $n$ taxa with $m$ aligned sites, of any character type (DNA, protein or binary), and any tree method that maps an alignment to an unrooted binary tree: [maximum parsimony](/maximum-parsimony/), [maximum likelihood](/maximum-likelihood-phylogeny/), [neighbor joining](/neighbor-joining/) or another. A split $A \mid B$ of the taxa is an edge of a tree, as on the [splits page](/splits-of-a-tree/), and a binary tree has $n - 3$ nontrivial splits. For most methods the tree search is a heuristic over $(2n-5)!!$ trees, and the bootstrap runs this heuristic $B$ more times.

It needs sites that are independent and identically distributed, or close to it. Columns that are linked, such as the paired sites of an RNA stem, or the codons of a gene, break this assumption, and resampling single columns then gives too high a support. It also needs the tree method to be a fixed function of the data: the same settings and the same search on every replicate.

## The template

The holes are ESTIMATE, the tree method, and $B$, the number of replicates. ESTIMATE may return $t$ tied trees; each one then counts $1/t$.

```pseudo id=main
BOOTSTRAP-SUPPORT(D, ESTIMATE, B, rng)
L1  count ← an empty map from splits to numbers
L2  repeat B times
L3      D* ← m columns of D drawn uniformly with replacement
L4      trees ← ESTIMATE(D*)
L5      for each tree t in trees and each split s of t do count[s] ← count[s] + 1 / |trees|
L6  return count[s] / B for each split s
```

With an estimator that costs $E(n, m)$, a run costs $O(B \,(E(n, m) + nm))$: line L3 takes $O(nm)$ to copy the columns. For the exhaustive parsimony estimator of the code, $E(n, m) = O((2n-5)!!\, nm)$, which limits it to small $n$.

The support $\hat p_B(s)$ on line L6 is a Monte Carlo estimate of the ideal bootstrap support $p(s)$, the mean count of $s$ over all $m^m$ resamples, each with weight $m^{-m}$. The estimate is unbiased, and its standard error is $\sqrt{p(s)(1-p(s))/B} \le 1/(2\sqrt B)$. With $B = 100$ the error can be 5 points, and with $B = 1000$ it is at most about 1.6 points. The ideal support depends only on how many times each column is drawn, so it is a sum over the $\binom{2m-1}{m}$ count vectors with multinomial weights, which the test computes exactly for small $m$.

The support values are usually shown on the input tree, or on the [majority-rule consensus](/majority-rule-consensus/) of the replicate trees, which holds every split with support above one half.

## Classic examples

**Five taxa and five sites.** Take A = AAAAC, B = AAACC, C = CCAAA, D = CCCCA and E = CACCA, with exhaustive [Fitch](/fitch-algorithm/) parsimony as ESTIMATE. Each site is a two-state column with one change at best. Sites 1 and 5 split AB from CDE, site 2 splits CD from ABE, site 3 splits DE from ABC, and site 4 splits AC from BDE. Two trees tie at length 7: $((A,B),C,(D,E))$ and $((A,B),E,(C,D))$. Over all $5^5 = 3125$ resamples, the exact supports and the estimates from `random.Random(4)` are these.

| split | exact support | exact value | $B = 100$ | $B = 1500$ |
|---|---|---|---|---|
| AB \| CDE | 7363/9375 | 0.785 | 0.748 | 0.785 |
| DE \| ABC | 4966/9375 | 0.530 | 0.572 | 0.546 |
| CD \| ABE | 267/625 | 0.427 | 0.378 | 0.409 |
| AC \| BDE | 1894/9375 | 0.202 | 0.232 | 0.206 |
| CE \| ABD | 64/3125 | 0.020 | 0.023 | 0.020 |
| BE \| ACD | 157/9375 | 0.017 | 0.020 | 0.016 |
| BD \| ACE | 106/9375 | 0.011 | 0.013 | 0.013 |
| AE \| BCD | 17/3125 | 0.005 | 0.007 | 0.004 |
| BC \| ADE | 16/9375 | 0.002 | 0.007 | 0.002 |

The split AB is in both shortest trees, and two of the five sites support it, so it gets the highest support. DE and CD each rest on one site and compete for the second edge. Every replicate gives $n - 3 = 2$ splits in total, so the column sums to 2. With $B = 100$ the estimate of DE is 4 points off the exact value, close to the standard error of 5 points.

**Felsenstein (1985).** The paper resampled the characters, built a tree from each replicate, and summarized the replicate trees by their majority-rule consensus. It read the fraction of replicates that contain a group as a measure of confidence in that group.

**Ultrafast bootstrap.** Minh, Nguyen and von Haeseler (2013) avoid one full tree search per replicate. During one likelihood search on the real data, they keep the trees met on the way and score each against every replicate by resampled site log likelihoods. UFBoot2 (Hoang et al. 2018) improves this. These supports are not on the same scale as the standard bootstrap, and the authors give a different threshold to read them.

## Variations

- **Parametric bootstrap.** Fit a model to the data, simulate $B$ alignments of length $m$ under the fitted tree and model, and rebuild the tree from each. It tests the model as much as the data.
- **Jackknife.** Delete a fraction of the columns, often half, without replacement, instead of drawing with replacement.
- **Transfer bootstrap expectation.** Lemoine et al. (2018) count a replicate split as partly present when few taxa must move to turn it into the input split. On large trees with a few unstable taxa, the classic support of deep splits falls to near 0, and the transfer support does not.
- **Block bootstrap.** Resample blocks of adjacent columns, or whole codons or genes, when single sites are not independent.

## Pitfalls

- **Support is not the probability that the clade is true.** Hillis and Bull (1993) found by simulation that bootstrap proportions and the probability that a clade is correct are different numbers, related in a way that depends on the conditions. In their simulations, a support of 70 percent often went with a much higher chance that the clade was correct, and they also found that the bootstrap can be biased.
- **Support is not a posterior probability.** A [Bayesian](/bayesian-phylogenetic-inference/) posterior split probability answers a different question, and the two values often differ on the same edge.
- **Systematic error.** If the method is inconsistent on the data, for example by [long branch attraction](/long-branch-attraction/), the bootstrap repeats the same error on every replicate and gives the wrong split high support.
- **Too few replicates.** With $B = 100$, values near 50, 70 or 95 percent are uncertain by several points.
- **Ties and search.** A heuristic search that stops early, or a tie rule that always picks the same tree, changes the support. Split ties evenly, as line L5 does, or report the rule.
- **Same settings.** Every replicate must use the same method and settings as the input tree. A fast search on the replicates and a careful search on the data give support for a different method.

## Exercises

1. Show that $\sum_s \hat p_B(s) = n - 3$ for any binary estimator, and that the support of each split lies in $[0, 1]$.
2. Show that the chance that a given column is absent from a resample is $(1 - 1/m)^m$, which tends to $e^{-1} \approx 0.368$.
3. Prove that the ideal support depends only on the count vector of draws, and that there are $\binom{2m-1}{m}$ count vectors.
4. In the five-taxon example, find the probability that a resample has no copy of site 1 and no copy of site 5, and explain what the parsimony trees of such a resample look like.
5. For an alignment in which all $m$ columns are equal and split $A \mid B$, show that the support of $A \mid B$ is exactly 1 for every $B$.

## References
