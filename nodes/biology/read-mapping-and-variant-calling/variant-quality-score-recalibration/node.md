---
tag: DTZA1Z
kind: algorithm
slug: variant-quality-score-recalibration
name: Variant quality score recalibration
aliases:
- VQSR
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Fit a Gaussian mixture to the annotations of calls at trusted sites, and score each call by its log likelihood ratio under good and bad models.
model: real-ram
complexity:
  vars: {N: the number of calls, d: the number of annotations, K: the number of mixture components, I: the number of EM iterations}
  time: {worst: O(I N K d + N log N), average: O(I N K d + N log N), best: O(N K d + N log N)}
  space: {extra: O(N K + K d)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2011
  people: [Mark A. DePristo, Eric Banks, Ryan Poplin]
  note: Introduced in the GATK framework as a filter that learns from the annotations of calls at known sites, in place of hand-set thresholds on each annotation.
prereqs: [gaussian-mixture-model, expectation-maximization, variant-call-format]
see_also: [variant-calling-problem, bayesian-genotype-calling, base-quality-score-recalibration, precision-and-recall, likelihood-ratio-test, one-class-svm, false-discovery-rate, quantile]
sources:
  - paper: doi:10.1038/ng.806
    title: Mark A. DePristo, Eric Banks, Ryan Poplin and others, A framework for variation discovery and genotyping using next-generation DNA sequencing data, Nature Genetics 43(5), 2011
    locator: pp. 491 to 498, the section on variant quality score recalibration and its supplementary methods (the Gaussian mixture on the annotations, the training sites, the score and the tranches by truth sensitivity)
  - book: isbn:978-0-387-31073-2
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Chapter 9, Section 9.2 (mixtures of Gaussians and their fit by EM) and Section 10.2 (the variational mixture of Gaussians)
  - paper: doi:10.1111/j.2517-6161.1977.tb01600.x
    title: Arthur P. Dempster, Nan M. Laird and Donald B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society Series B 39(1), 1977
    locator: pp. 1 to 38 (the EM algorithm and the proof that each iteration does not lower the likelihood)
---

Variant quality score recalibration (VQSR) filters a set of raw variant calls by learning what good calls look like. Each call comes with annotations, numbers such as the quality by depth (QD) and the strand bias (FS) that the caller computes from the reads. VQSR fits a [Gaussian mixture model](/gaussian-mixture-model/) to the annotations of the calls at trusted sites, fits a second mixture to the calls that look least like them, and scores every call by the log ratio of the two densities. It then picks the score threshold that keeps a chosen share, such as 99%, of the calls at a set of truth sites. The method is the one of the GATK pipeline of DePristo et al. (2011); the code on this page is a reduced version, and the parts it leaves out are listed below.

## In plain words

A variant caller finds many possible variants, and some are mistakes. Each one has a few measurements, such as how strong the evidence is per read and whether the reads all come from one strand.

Take the calls that sit at places where a variant is already known to exist. Their measurements show what real variants look like. Then take the calls that look least like those; they show what mistakes look like. Give every call a score: high if it looks like the real ones and not like the mistakes. Last, choose the lowest score you accept so that you keep, for example, 99 of every 100 known real variants. Calls below that score are marked as filtered.

## The problem

**Input.** $N$ raw calls, each with an annotation vector $x_i \in \mathbb{R}^d$; a *training* subset of calls at trusted sites; a *truth* subset, often the same or a smaller one; and a target sensitivity $\sigma \in (0, 1]$.

**Output.** A score $s_i$ for every call, a threshold $\tau$, and a filter decision $s_i \ge \tau$, such that at least the share $\sigma$ of the truth calls pass, and calls that look like artifacts score low.

For SNPs, GATK's documentation uses annotations such as QD, MQ, MQRankSum, ReadPosRankSum, FS and SOR, and training resources for humans such as HapMap, Omni and high-confidence 1000 Genomes sites. These are choices of the GATK workflow, not parts of the method.

## The algorithm

```pseudo id=main
VQSR(x_1, ..., x_N, training set T, truth set U, sensitivity σ)
L1  p+ ← a K+ component Gaussian mixture fitted by EM to {x_i : i ∈ T}
L2  λ_i ← ln p+(x_i) for every call i
L3  B ← the max(K-, ⌊βN⌋) calls of smallest λ_i
L4  p- ← a K- component Gaussian mixture fitted by EM to {x_i : i ∈ B}
L5  s_i ← λ_i - ln p-(x_i) for every call i
L6  τ ← the largest t such that at least the share σ of {s_i : i ∈ U} is at least t
L7  pass_i ← (s_i ≥ τ) for every call i
L8  return s, τ, pass
```

The mixtures have diagonal covariances, with a floor on each variance so that a component cannot shrink onto one point. EM starts from $K$ random calls as the means and the overall variance; the code fixes the seed. The share $\beta$ of calls that train the bad model is 10% by default in the code. The score $s_i$ is what GATK writes as VQSLOD, a log odds that the call is real against that it is an artifact, up to the ratio of the priors.

Line L6 sorts the truth scores in decreasing order and takes the entry at rank $\lceil \sigma |U| \rceil$.

## Example

The test of the code simulates 900 calls with two annotations, QD and FS. The 700 real calls are in two clusters, at QD about 12 and 25, with FS near 0 to 3. The 200 artifacts have QD about 4 and FS about 18. Half of the real calls, 356 of them, form both the training set and the truth set. With $K_+ = 3$, $K_- = 2$ and $\beta = 0.1$:

| target sensitivity | threshold | truth calls kept | real calls kept | artifacts kept |
|---|---|---|---|---|
| 90% | 37.56 | 321 of 356 | 625 of 700 | 0 of 200 |
| 99% | 31.77 | 353 of 356 | 693 of 700 | 0 of 200 |
| 100% | 27.16 | 356 of 356 | 700 of 700 | 0 of 200 |

The share of the real calls that pass tracks the share of the truth calls, because the truth calls are a random half of the real ones. In this simple case the two groups are well apart, and even the 100% tranche keeps no artifact. In real data the classes overlap, and the higher tranches let in more false calls.

A small case of line L6: truth scores 5, 1, 3, 2 and $\sigma = 0.75$. Sorted in decreasing order they are 5, 3, 2, 1, and the entry at rank $\lceil 0.75 \cdot 4 \rceil = 3$ is 2, so $\tau = 2$ keeps three of the four.

## Correctness

The method is a heuristic classifier, so its correctness has two parts that can be proved. First, each EM iteration of lines L1 and L4 does not lower the likelihood of its data: the E step makes a lower bound tight by [Jensen's inequality](/jensens-inequality/), and the M step maximizes the bound, also with the floor on the variances. So the fit converges to a stationary value of the likelihood, which may be a local maximum. With one component, the fit is the sample mean and variance. Second, the threshold of line L6 keeps at least the share $\sigma$ of the truth calls, and no larger threshold does. The full proof is in proofs/correctness.md. That the filter removes artifacts is not a theorem; it depends on the annotations and the training sites.

## Complexity

- **Time.** One EM iteration costs $O(n K d)$ for $n$ points, so each fit costs $O(I N K d)$ for $I$ iterations. Line L3 and line L6 sort, $O(N \log N)$. The fits dominate.
- **Space.** $O(N K)$ for the responsibilities of EM and $O(K d)$ for the mixture.

## Properties

- **Not deterministic in general.** EM starts from random points and can reach different local maxima; fixing the seed makes a run repeatable.
- **Calibrated to sensitivity, not to precision.** The tranche fixes the share of truth calls kept. The share of false calls among those kept is not controlled, and it depends on how the artifacts fall in the annotation space.
- **Needs many calls.** The mixtures need enough training calls to fit, which is why GATK's documentation suggests hard filters for small call sets, such as a single exome.
- **Ranking.** The score orders the calls, so one fit gives every tranche.

## Variants and improvements

The GATK tool differs from this page in several ways, which the code leaves out.

- **Variational Bayes.** GATK fits a Bayesian Gaussian mixture by variational inference, with priors on the means and covariances, which can switch off components it does not need (Bishop 2006, Section 10.2).
- **Full covariances.** GATK uses full covariance matrices; the code uses diagonal ones.
- **Separate models.** SNPs and indels get separate models with their own annotations and training sets.
- **Annotation scaling.** GATK centers and scales each annotation before the fit.
- **Several tranches.** GATK writes the filter names of several tranches, such as 90, 99, 99.9 and 100, so that the user can pick one later.
- **Hard filters.** The simple alternative is fixed thresholds on each annotation. GATK's documentation suggests, for SNPs, filtering QD < 2.0, QUAL < 30, SOR > 3.0, FS > 60.0, MQ < 40.0, MQRankSum < -12.5 and ReadPosRankSum < -8.0. These are its rules of thumb, not results of a model.
- **Other classifiers.** Any classifier trained on known sites can play the same role, for example a [random forest](/random-forest/) or a [one-class SVM](/one-class-svm/) on the good calls alone. Later GATK tools also score variants with neural networks.

## When to use it

Use it on large germline call sets, a whole genome or many exomes, when a good set of known variant sites exists for the species. For small call sets or species without such resources, use hard filters. The choice of the tranche is a trade between sensitivity and precision; measure both on a benchmark with [precision and recall](/precision-and-recall/) if one is available.

## Pitfalls

- **Training bias.** The good model learns what known variants look like. Real variants of a kind that the training sites lack, such as variants in hard regions, can score low.
- **Annotations with a fixed value.** An annotation that is the same for most calls, such as a mapping quality of 60, makes a component collapse onto it. The variance floor guards against this; dropping the annotation from the model is the other fix.
- **Depth in exomes.** Depth-based annotations behave differently in targeted data, where depth varies by target, so they are often left out for exomes.
- **Truth sensitivity is not true sensitivity.** The tranche is measured on the truth sites, which are easier than the average real variant, so the real sensitivity is lower.
- **Reading VQSLOD as a probability.** The score is a log density ratio, without calibrated priors, so it ranks calls but does not give the probability that a call is real.

## Implementations

## History

DePristo et al. (2011) described VQSR as the last step of their framework for variant discovery, after mapping, local realignment, base quality score recalibration and genotyping. It replaced hard thresholds on each annotation with a model fitted to the calls at known sites, and it introduced the tranches by truth sensitivity. It was a standard step of the GATK best practices for germline short variants for many years.

## References
