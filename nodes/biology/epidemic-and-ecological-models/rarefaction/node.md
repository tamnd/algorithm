---
tag: 5Z889P
kind: technique
slug: rarefaction
name: Rarefaction
aliases:
- rarefaction curve
area: biology/epidemic-and-ecological-models
level: core
summary: Compare species richness across samples of unequal size by the expected number of species in a random subsample of m individuals.
history:
  year: 1968
  people: [Howard L. Sanders, Stuart H. Hurlbert, Kenneth L. Heck Jr., Gerald van Belle, Daniel Simberloff]
  note: Sanders proposed rarefaction for benthic samples in 1968, Hurlbert gave the exact hypergeometric formula in 1971, and Heck, van Belle and Simberloff gave its variance in 1975.
prereqs: [linearity-of-expectation, simpson-diversity-index]
see_also: [chao1-estimator, shannon-diversity-index, simpson-diversity-index, phylogenetic-diversity, coupon-collector-problem, sequencing-coverage, linearity-of-expectation, lincoln-petersen-estimator]
sources:
  - paper: doi:10.1086/282541
    title: Howard L. Sanders, Marine benthic diversity, a comparative study, The American Naturalist 102(925), 1968
    locator: pages 243 to 282 (the rarefaction method for comparing samples of different sizes)
  - paper: doi:10.2307/1934145
    title: Stuart H. Hurlbert, The nonconcept of species diversity, a critique and alternative parameters, Ecology 52(4), 1971
    locator: pages 577 to 586 (the exact expected number of species in a subsample, and the overestimate in Sanders' method)
  - paper: doi:10.2307/1934716
    title: Kenneth L. Heck Jr., Gerald van Belle and Daniel Simberloff, Explicit calculation of the rarefaction diversity measurement and the determination of sufficient sample size, Ecology 56(6), 1975
    locator: pages 1459 to 1461 (the variance of the rarefied number of species)
  - paper: doi:10.1046/j.1461-0248.2001.00230.x
    title: Nicholas J. Gotelli and Robert K. Colwell, Quantifying biodiversity, procedures and pitfalls in the measurement and comparison of species richness, Ecology Letters 4(4), 2001
    locator: pages 379 to 391 (individual-based and sample-based rarefaction, and accumulation curves)
---

Rarefaction compares the number of species in samples of different sizes. A larger sample finds more species, so raw counts of species are not comparable. Rarefaction asks a fair question of each sample: if only $m$ individuals had been taken, how many species would we expect to see? For a sample of $n$ individuals with $n_i$ of species $i$, a random subsample of $m$ individuals misses species $i$ with probability $\binom{n - n_i}{m} / \binom{n}{m}$. By linearity of expectation, the expected number of species is the sum over species of one minus this probability, with no simulation needed. The rarefaction curve plots this value against $m$ from 1 to $n$. Two samples are compared at the size $m$ of the smaller one. The same template works for any feature that a set of individuals covers, for example the branches of a phylogenetic tree.

## In plain words

You count beetles in two forests. In the first forest you caught 500 beetles of 40 kinds. In the second you caught 100 beetles of 25 kinds. The first forest looks richer, but you also caught five times as many beetles there, and more beetles always means more kinds.

To compare fairly, ask how many kinds you would have seen in the first forest if you had caught only 100 beetles. Imagine picking 100 of your 500 beetles at random, many times over, and counting the kinds each time. Rarefaction works out the average of this count exactly, by adding up, kind by kind, the chance that the kind is among the picked beetles.

If the first forest still shows more kinds at 100 beetles, it is richer at that sample size.

## When it applies

- Samples differ in size, and the question is about the number of species or another count of distinct things found by sampling.
- The individuals of each sample are a random sample of one community, so that a random subsample is a smaller random sample of the same community.
- The quantity is a sum over features of a weight times "the feature is seen", so that linearity of expectation reduces the subsample average to one probability per feature. This covers species richness, phylogenetic diversity, the number of genes or k-mers found by a set of reads, and the number of distinct values in a data set.
- A signal that the technique is needed: a plot of the number of species against the sample size that still rises steeply at the largest sample.

## The template

```pseudo id=main
RAREFY(units, FEATURES, WEIGHT, CARRIES, m)
L1  n ← the number of units in the full sample
L2  for each feature f in FEATURES: k_f ← the number of units u with CARRIES(u, f)
L3      q_f ← C(n - k_f, m) / C(n, m)        the probability that no unit of the subsample carries f
L4  E ← the sum over f of WEIGHT(f) (1 - q_f)
L5  V ← the sum over f, g of WEIGHT(f) WEIGHT(g) (q_fg - q_f q_g), with q_fg ← C(n - k_f - k_g + k_fg, m) / C(n, m)
L6  return (E, V)
```

The holes are the units, the features, the weights and the relation CARRIES. For species richness, the units are individuals, each feature is a species with weight 1, and an individual carries its own species, so $k_f = n_i$ and $k_{fg} = 0$ for two different species. Then line L4 is Hurlbert's formula

$$\mathbb{E}[S_m] = \sum_{i} \left(1 - \frac{\binom{n - n_i}{m}}{\binom{n}{m}}\right),$$

and line L5 is the variance of Heck, van Belle and Simberloff, $\sum_i q_i (1 - q_i) + 2 \sum_{i < j} (q_{ij} - q_i q_j)$ with $q_{ij} = \binom{n - n_i - n_j}{m} / \binom{n}{m}$. Line L3 is the probability that a uniform random set of $m$ of the $n$ units avoids the $k_f$ units that carry $f$. Line L4 follows from [linearity of expectation](/linearity-of-expectation/), and line L5 from the variance of a sum of indicators. Compute the binomial ratios as products, $q = \prod_{j=0}^{m-1} (n - k - j) / (n - j)$, or in log space. $\binom{n}{m}$ overflows a float for a few thousand individuals.

**A theorem behind the use.** If the $n$ individuals are an independent sample from a community with abundances $p_i$, then a uniform random subsample of $m$ of them is an independent sample of size $m$. So the rarefied value of line L4 is an unbiased estimate of $\sum_i (1 - (1 - p_i)^m)$, the expected number of species in a new sample of $m$ individuals from the community.

**The example sample $(5, 3, 2)$.** With $n = 10$:

| $m$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\mathbb{E}[S_m]$ | 1 | 1.688889 | 2.158333 | 2.476190 | 2.690476 | 2.833333 | 2.925 | 2.977778 | 3 | 3 |

At $m = 5$, $q = (\binom{5}{5}, \binom{7}{5}, \binom{8}{5}) / \binom{10}{5} = (1, 21, 56)/252$, so $\mathbb{E}[S_5] = 3 - 78/252 = 113/42 = 2.690476$, and line L5 gives $\mathrm{Var}(S_5) = 391/1764 = 0.221655$. At $m = 2$, $\mathbb{E}[S_2] - 1 = 0.688889$, which is the Gini-Simpson index without replacement of the [Simpson diversity index](/simpson-diversity-index/) page.

## Classic examples

- **Species richness of a sample.** The template with species as features, as above. It is the standard way to compare $S_{obs}$ across samples of different sizes, and to show how close a sample is to its asymptote.
- **The Simpson index as a point on the curve.** For $m = 2$, the expected number of species minus 1 is the probability that two different individuals belong to different species, Hurlbert's probability of an interspecific encounter. See the [Simpson diversity index](/simpson-diversity-index/).
- **Phylogenetic diversity.** Take the branches of a phylogenetic tree as features, each with its length as the weight, and let an individual carry every branch on the path from the root to its species. Then line L4 is the expected [phylogenetic diversity](/phylogenetic-diversity/) of a subsample. For the tree $((A{:}1, B{:}1){:}2, C{:}3)$ and the counts $A = 5$, $B = 3$, $C = 2$, the full sample has a diversity of 7, and a subsample of 5 individuals has expected diversity $787/126 = 6.246$.
- **Sampling with replacement.** If the subsample is drawn with replacement, $q_f = (1 - k_f / n)^m$. With equal abundances this is the [coupon collector problem](/coupon-collector-problem/): the expected number of distinct coupons after $m$ draws.
- **Sequencing depth.** With reads as units and genes, k-mers or positions as features, the curve shows how many features a smaller run would find. This is the logic of saturation curves for [sequencing coverage](/sequencing-coverage/) and library complexity.

## Variations

- **Sample-based rarefaction.** When the data are the presence or absence of species in sampling units (plots, traps, nights), use the units in the template and let a unit carry every species found in it. Gotelli and Colwell (2001) recommend this form when individuals are not independent, for example when they occur in clumps.
- **Extrapolation.** Beyond $m = n$ the curve cannot be computed by subsampling. Estimators of the unseen species such as the [Chao1 estimator](/chao1-estimator/) extend the curve to larger $m$ and give its asymptote.
- **Coverage-based rarefaction.** Compare samples at the same estimated coverage, the fraction of the community abundance that belongs to observed species, in place of the same $m$. The Good-Turing estimate $1 - f_1 / n$ is the usual coverage estimate.
- **Rarefaction of other indices.** Any index that is a sum of feature indicators works with the template. The Shannon index is not of this form, so its rarefied mean needs simulation or a separate formula.
- **Random subsampling.** Drawing one random subsample per sample, often called rarefying, gives a single random value in place of the mean of line L4. It adds noise and discards data.

## Pitfalls

- **Overflow in line L3.** $\binom{n}{m}$ for $n = 5000$ does not fit in a float. Compute $q$ as the product of ratios, or with the log-gamma function, not as a ratio of two large binomials.
- **The method of Sanders.** Sanders' original method scaled the species counts in proportion and overestimates the expected number of species. Use Hurlbert's exact formula of line L4.
- **Comparing at different sizes.** Compare curves at a common $m$, not the endpoint of one curve with a point on another. Curves can cross: a sample can be richer at small $m$ and poorer at large $m$, if it has a few common species and many rare ones.
- **The variance is about subsampling.** Line L5 is the variance over subsamples of the one observed sample. It is zero at $m = n$. It does not include the variation between new samples from the community, so it is too small for a test between communities.
- **Rarefying count tables for testing.** Throwing away reads to reach a common depth before a statistical test of differences between groups loses power. Rarefaction curves are for the description of richness; for testing, a model of the counts is the better tool.

## Exercises

1. Show that $\mathbb{E}[S_2] - 1 = 1 - \sum_i n_i (n_i - 1) / (n (n - 1))$ for every sample.
2. Show that the curve is concave: with $q_i(m) = \binom{n - n_i}{m} / \binom{n}{m}$, prove that $q_i(m) - q_i(m + 1) = q_i(m)\, n_i / (n - m)$, and that this difference does not increase with $m$ when $n_i \ge 1$.
3. Compute $\mathbb{E}[S_3]$ for the sample $(5, 3, 2)$ and check that it is $259/120$.
4. For a community with abundances $(0.5, 0.3, 0.2)$, compute the expected number of species in a sample of $m$ individuals drawn with replacement for $m = 2$ and $m = 5$ (the answers are $1.62$ and $2.473$), and compare them with the rarefied values of the sample $(5, 3, 2)$.
5. Prove the theorem above: a uniform random $m$-subset of an independent sample of $n$ individuals is an independent sample of $m$ individuals, so the rarefied value is unbiased for $\sum_i (1 - (1 - p_i)^m)$.

## References
