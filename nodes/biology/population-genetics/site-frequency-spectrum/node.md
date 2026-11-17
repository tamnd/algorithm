---
tag: D8B6H3
kind: definition
slug: site-frequency-spectrum
name: Site frequency spectrum
aliases:
- allele frequency spectrum
area: biology/population-genetics
level: core
summary: The counts of segregating sites at which the derived allele appears in 1, 2, up to n - 1 of n sampled sequences.
prereqs: [infinite-sites-model, kingman-coalescent]
see_also: [watterson-estimator, nucleotide-diversity, tajimas-d, coalescent-simulation, allele-frequency, mcdonald-kreitman-test]
sources:
  - paper: doi:10.1006/tpbi.1995.1025
    title: Yun-Xin Fu, Statistical properties of segregating sites, Theoretical Population Biology 48(2), 1995
    locator: pp. 172-197 (the expected number of segregating sites of each frequency class, theta / i, and their covariances)
  - book: isbn:9780974707754
    title: John Wakeley, Coalescent Theory, An Introduction, Roberts and Company, 2009
    locator: Chapter 4 (the site frequency spectrum under the infinite-sites model)
  - paper: doi:10.1093/genetics/123.3.585
    title: Fumio Tajima, Statistical method for testing the neutral mutation hypothesis by DNA polymorphism, Genetics 123(3), 1989
    locator: pp. 585-595 (a test that compares two estimators of theta, both linear in the spectrum)
---

The site frequency spectrum (SFS) of a sample of $n$ aligned DNA sequences is the vector $(\xi_1, \ldots, \xi_{n-1})$, where $\xi_i$ is the number of segregating sites at which exactly $i$ of the $n$ sequences carry the derived allele. It is a histogram of the [allele frequencies](/allele-frequency/) in the sample, one entry per site. Under the neutral [infinite sites model](/infinite-sites-model/) with constant size, $E[\xi_i] = \theta / i$ (Fu 1995). Most summary statistics of DNA polymorphism, among them [Watterson's estimator](/watterson-estimator/), [nucleotide diversity](/nucleotide-diversity/) and [Tajima's D](/tajimas-d/), are linear functions of the SFS.

## Definition

Let $H$ be an $n \times S$ matrix over $\{0, 1\}$, one row per sampled sequence and one column per segregating site, with 1 for the derived allele and 0 for the ancestral allele. Let $c_j = \sum_{r=1}^{n} H_{rj}$ be the derived count of site $j$. Because the site segregates, $1 \le c_j \le n - 1$.

The **unfolded site frequency spectrum** is the vector $\xi = (\xi_1, \ldots, \xi_{n-1})$ with

$$\xi_i = \left|\{\, j : c_j = i \,\}\right|, \qquad i = 1, \ldots, n - 1.$$

So $\sum_{i} \xi_i = S$, the number of segregating sites.

When the ancestral allele is not known, only the minor allele count $\min(c_j, n - c_j)$ is defined. The **folded spectrum** is $\eta = (\eta_1, \ldots, \eta_{\lfloor n/2 \rfloor})$ with $\eta_i = \xi_i + \xi_{n-i}$ for $i < n/2$ and $\eta_{n/2} = \xi_{n/2}$ when $n$ is even.

**Expectation (Fu 1995).** Under the neutral infinite sites model with a constant population size and $\theta = 4N\mu$ with time in units of $2N$ generations,

$$E[\xi_i] = \frac{\theta}{i}, \qquad i = 1, \ldots, n - 1.$$

*Proof.* Look at the [Kingman coalescent](/kingman-coalescent/) tree of the sample during the time $T_k$ when $k$ lineages exist. The tree shape is independent of the times. The $n$ leaves split among the $k$ lineages, and by the Pólya urn argument of the root split result on the Kingman coalescent page, run with $k$ colours instead of two, the vector of their sizes is uniform over the $\binom{n-1}{k-1}$ ordered ways to write $n$ as a sum of $k$ positive parts. So a fixed one of the $k$ lineages has exactly $i$ leaves below it with probability $\binom{n-i-1}{k-2} / \binom{n-1}{k-1}$, the number of ways to split the other $n - i$ leaves into $k - 1$ positive parts over the total. A mutation on that lineage during $T_k$ gives a site with derived count $i$. Mutations fall at rate $\theta/2$ per lineage, and $E[T_k] = 2/(k(k-1))$. Summing over the $k$ lineages and over $k$,

$$E[\xi_i] = \sum_{k=2}^{n} k \cdot \frac{\theta}{2} \cdot \frac{2}{k(k-1)} \cdot \frac{\binom{n-i-1}{k-2}}{\binom{n-1}{k-1}} = \theta \sum_{k=2}^{n} \frac{\binom{n-i-1}{k-2}}{(k-1)\binom{n-1}{k-1}}.$$

Expand the factorials: $\frac{1}{k-1} \binom{n-i-1}{k-2} \big/ \binom{n-1}{k-1} = \frac{(n-i-1)!\,(n-k)!}{(n-1)!\,(n-i-k+1)!} = \binom{n-k}{i-1} \big/ \left(i \binom{n-1}{i}\right)$. By the hockey stick identity, $\sum_{k=2}^{n} \binom{n-k}{i-1} = \sum_{j=0}^{n-2} \binom{j}{i-1} = \binom{n-1}{i}$. So the sum is $1/i$. $\square$

The proof uses the tree of one site at a time, and the expectation of a sum over sites is the sum of the expectations. So the result also holds with recombination, where each site has its own tree. The variances and covariances of the $\xi_i$ do depend on recombination. The sum over $i$ gives $E[S] = \theta a_n$ with $a_n = \sum_{i=1}^{n-1} 1/i$, which is Watterson's result. For the folded spectrum, $E[\eta_i] = \theta (1/i + 1/(n-i))$ for $i < n/2$, and $E[\eta_{n/2}] = 2\theta/n$.

## Examples and non-examples

**A sample of five.** The matrix

| copy | s1 | s2 | s3 | s4 | s5 | s6 |
|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| 4 | 0 | 0 | 1 | 1 | 0 | 0 |
| 5 | 0 | 0 | 1 | 1 | 1 | 0 |

has the derived counts $(2, 1, 2, 3, 1, 1)$. So $\xi = (3, 2, 1, 0)$: three singletons, two doubletons, one tripleton and no site with four derived copies. The folded spectrum is $\eta = (\xi_1 + \xi_4, \xi_2 + \xi_3) = (3, 3)$.

With $a_5 = 25/12$, Watterson's estimate is $\hat\theta_W = 6 / (25/12) = 2.88$. The neutral expectation with this $\theta$ is $(2.88, 1.44, 0.96, 0.72)$. The observed spectrum is close to it at frequencies 1 and 3, has more sites at frequency 2 (2 against 1.44) and none at frequency 4 (against 0.72). With six sites, such differences are well inside the random variation of one genealogy.

**Linear statistics.** Each estimator of $\theta$ below is $\sum_i w_i \xi_i$ for weights $w_i$ with $\sum_i w_i \cdot \theta / i = \theta$, so each is unbiased under the neutral model:
- [Watterson's estimator](/watterson-estimator/): $w_i = 1 / a_n$. In the example, $2.88$.
- [Nucleotide diversity](/nucleotide-diversity/) (mean pairwise difference): $w_i = i(n - i) / \binom{n}{2}$. In the example, $(1 \cdot 4 \cdot 3 + 2 \cdot 3 \cdot 2 + 3 \cdot 2 \cdot 1)/10 = 3$.
- The singleton count $\xi_1$ alone: $w_1 = 1$, $w_i = 0$ otherwise.

[Tajima's D](/tajimas-d/) is a scaled difference of the first two. A model that does not fit the neutral expectation (growth, a sweep, structure) changes the shape of the spectrum, and such statistics measure the change in different directions.

**Non-examples.**
- A site where all $n$ sequences carry the derived allele is a fixed difference from the outgroup, not a segregating site. It has no entry $\xi_n$. The [McDonald-Kreitman test](/mcdonald-kreitman-test/) counts such sites separately.
- A site with three alleles has no place in $\xi$. It cannot occur under the infinite sites model; real data sets drop such sites or split them.
- A vector of allele frequencies in the whole population is not the SFS of a sample: the SFS depends on $n$, and $\xi_i$ for $n = 10$ and for $n = 20$ are different quantities.
- A spectrum from data with unknown ancestral states must not be read as unfolded. Polarizing by an outgroup that has its own mutations flips some sites from $i$ to $n - i$ and creates false high-frequency derived variants.

## Related definitions

- **Segregating sites** $S = \sum_i \xi_i$; see [infinite sites model](/infinite-sites-model/).
- **Joint SFS.** For samples from two or more populations, the array of counts of sites with $i$ derived copies in the first sample and $j$ in the second. It carries information about divergence times and migration that the SFS of one population does not.
- **Allele frequency.** The population frequency of the derived allele at one site; see [allele frequency](/allele-frequency/). The SFS is the distribution of the sample version over sites.
- **Expected SFS under other models.** Population growth adds singletons ($E[\xi_1]$ grows relative to $\theta$), a bottleneck can remove them, and a selective sweep adds both rare and high-frequency derived variants. Many demographic inference programs fit the expected spectrum of a model to the observed one. [Coalescent simulation](/coalescent-simulation/) gives the expected spectrum of a model when no formula is known.

## References
