---
tag: 2B5Z97
kind: definition
slug: simpson-diversity-index
name: Simpson diversity index
aliases:
- Simpson's index
area: biology/epidemic-and-ecological-models
level: intro
summary: The probability that two individuals drawn at random with replacement from a community belong to the same species, or one minus it.
history:
  year: 1949
  people: [Edward H. Simpson]
  note: Simpson defined the index as a measure of concentration in a one-page letter to Nature in 1949, with the form without replacement for a finite sample.
prereqs: [linearity-of-expectation]
see_also: [shannon-diversity-index, rarefaction, gini-impurity, chao1-estimator, shannon-entropy, linearity-of-expectation]
sources:
  - paper: doi:10.1038/163688a0
    title: E. H. Simpson, Measurement of diversity, Nature 163(4148), 1949
    locator: page 688 (the concentration as the probability that two individuals belong to the same group, and its estimate from a sample)
  - paper: doi:10.2307/1934145
    title: Stuart H. Hurlbert, The nonconcept of species diversity, a critique and alternative parameters, Ecology 52(4), 1971
    locator: pages 577 to 586 (the probability of an interspecific encounter, and the expected number of species in a subsample)
  - paper: doi:10.2307/1934352
    title: M. O. Hill, Diversity and evenness, a unifying notation and its consequences, Ecology 54(2), 1973
    locator: pages 427 to 432 (the inverse of the Simpson concentration as the diversity number of order 2)
  - book: isbn:9780632056330
    title: Anne E. Magurran, Measuring Biological Diversity, Blackwell, 2004
    locator: the chapter on diversity indices (Simpson's index, its forms and its sampling properties)
---

The Simpson index of a community is $\lambda = \sum_i p_i^2$, the probability that two individuals drawn at random with replacement belong to the same species. It is a measure of concentration: it is 1 when one species makes up the whole community and small when many species share it evenly. Three forms are in use, and papers often call each of them "Simpson's index": the concentration $\lambda$ itself, the Gini-Simpson index $1 - \lambda$ (the probability that the two individuals differ), and the inverse Simpson index $1 / \lambda$ (the effective number of species of order 2). From a sample, Simpson's form without replacement, $\sum n_i (n_i - 1) / (n (n - 1))$, is an unbiased estimate of $\lambda$. Always say which form you report.

## Definition

Let a community have $S$ species with relative abundances $p_1, \ldots, p_S \ge 0$ and $\sum_i p_i = 1$. The **Simpson concentration** is

$$\lambda = \sum_{i=1}^{S} p_i^2.$$

If two individuals are drawn independently, each of species $i$ with probability $p_i$ (that is, with replacement), then $\lambda$ is the probability that they are of the same species. The **Gini-Simpson index** is $1 - \lambda$, and the **inverse Simpson index** is $D_2 = 1 / \lambda$.

For a sample of $n \ge 2$ individuals with $n_i$ of species $i$, the plug-in value is $\hat\lambda = \sum_i (n_i / n)^2$, and the form **without replacement** is

$$\hat\lambda_u = \sum_i \frac{n_i (n_i - 1)}{n (n - 1)},$$

the probability that two different individuals drawn from the sample are of the same species.

Properties that follow from the definition (theorems):
- $1 / S \le \lambda \le 1$ for $S$ species with $p_i > 0$. $\lambda = 1 / S$ if and only if all $p_i = 1/S$, and $\lambda = 1$ if and only if $S = 1$. So $1 \le D_2 \le S$.
- **Unbiasedness.** Under multinomial sampling of $n$ individuals, $n_i$ is binomial with $\mathbb{E}[n_i (n_i - 1)] = n (n - 1) p_i^2$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[\hat\lambda_u] = \lambda$. The plug-in value has $\mathbb{E}[\hat\lambda] = \lambda + (1 - \lambda)/n$, so it is too high.
- $1 / \hat\lambda_u$ is not an unbiased estimate of $1/\lambda$, because the reciprocal is not linear.
- **Order 2 of Hill's family.** $D_2$ is the Hill number $(\sum p_i^q)^{1/(1 - q)}$ for $q = 2$. It counts common species more than the [Shannon index](/shannon-diversity-index/) does, which is the order 1 member $e^H$. So $D_2 \le e^H \le S$.

## Examples and non-examples

- The abundances $(5, 3, 2)$ give $p = (0.5, 0.3, 0.2)$ and $\lambda = 0.25 + 0.09 + 0.04 = 0.38$, so the Gini-Simpson index is $0.62$ and the inverse Simpson index is $1 / 0.38 = 2.631579$. This is less than $e^H = 2.800094$ for the same community.
- As a sample of $n = 10$, the form without replacement is $\hat\lambda_u = (20 + 6 + 2) / 90 = 28/90 = 0.311111$, so $1 - \hat\lambda_u = 0.688889$ and $1 / \hat\lambda_u = 3.214286$.
- The counts $(10, 6, 4)$ have the same proportions and the same $\lambda = 0.38$, but $\hat\lambda_u = (90 + 30 + 12) / 380 = 0.347368$. The two forms get closer as $n$ grows.
- Four species with equal abundance give $\lambda = 0.25$ and $D_2 = 4$. The counts $(97, 1, 1, 1)$ give $\lambda = 0.9412$ and $D_2 = 1.062473$: one species dominates.
- **Non-example: a sample of singletons.** Five individuals of five species give $\hat\lambda_u = 0$, and $1 / \hat\lambda_u$ has no value. The sample shows only that no two individuals share a species.
- **Non-example: the index of a large and a small sample.** The plug-in $\hat\lambda$ of a small sample is too high by $(1 - \lambda)/n$, so a small sample looks less diverse. Use $\hat\lambda_u$ to compare samples of different sizes.
- **Non-example: "higher is more diverse".** For $\lambda$ a higher value means less diversity, and for $1 - \lambda$ and $1 / \lambda$ it means more. A value without its form is ambiguous.

The pseudocode below computes all forms from a list of counts.

```pseudo id=main
SIMPSON(counts)
L1  n ← the sum of the counts
L2  λ ← the sum of (c / n)^2 over the counts c
L3  λ_u ← the sum of c (c - 1) over the counts, divided by n (n - 1), if n ≥ 2
L4  return (λ, 1 - λ, 1 / λ, λ_u, 1 - λ_u)
```

## Related definitions

- [Gini impurity](/gini-impurity/) of a node of a decision tree is the Gini-Simpson index of its class proportions.
- The [Shannon diversity index](/shannon-diversity-index/) is the order 1 member of Hill's family, and it gives rare species more weight. [Shannon entropy](/shannon-entropy/) and the Rényi entropy of order 2, $-\ln \lambda$, are the information measures behind the two indices.
- Hurlbert's probability of an interspecific encounter, $1 - \hat\lambda_u$, is also the expected number of species in a random subsample of 2 individuals, minus 1. So it is the first nontrivial point of the [rarefaction](/rarefaction/) curve: for the sample $(5, 3, 2)$, $\mathbb{E}[S_2] - 1 = 0.688889$.
- The [Chao1 estimator](/chao1-estimator/) estimates the number of species, the diversity of order 0, which depends most on the rare species.

## References
