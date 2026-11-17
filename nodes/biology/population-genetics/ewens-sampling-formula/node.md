---
tag: 98RRBF
kind: theorem
slug: ewens-sampling-formula
name: Ewens sampling formula
aliases:
- Ewens distribution
area: biology/population-genetics
level: advanced
summary: "Under the neutral infinite alleles model, the probability of an allelic partition of a sample of n genes, with theta as the only parameter."
prereqs: [infinite-alleles-model]
see_also: [infinite-alleles-model, kingman-coalescent, stirling-numbers, random-permutation, dirichlet-process, sufficient-statistic, maximum-likelihood-estimation, integer-partitions]
sources:
  - paper: "Warren J. Ewens, The sampling theory of selectively neutral alleles, Theoretical Population Biology 3(1), 1972"
    title: Ewens 1972
    locator: the formula for the allele counts of a sample, the sufficiency of the number of alleles and the estimate of theta
  - paper: "Fred M. Hoppe, Polya-like urns and the Ewens sampling formula, Journal of Mathematical Biology 20, 1984"
    title: Hoppe 1984
    locator: the urn that draws a sample with the law of the formula
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 3.6 (infinitely many alleles models, p. 111), Section 9.5 (sample properties of the infinitely many alleles model, p. 301) and Section 11.2.2 (the Ewens and Watterson tests, p. 349)
---

The Ewens sampling formula gives the probability of each way that a sample of $n$ genes can split into allele classes, when the population follows the neutral [infinite alleles model](/infinite-alleles-model/) at equilibrium. It has one parameter, the scaled mutation rate $\theta = 4Nu$. A strong consequence is that the number of distinct alleles in the sample carries all the information about $\theta$. The same law appears outside genetics, as the law of the cycle type of a random permutation and of the clusters of a Dirichlet process.

## Statement

**The setting.** A sample of $n$ genes from a large population under the neutral infinite alleles model at stationarity, in the limit $N \to \infty$ with $\theta = 4Nu$ fixed. Equivalently, the genealogy of the sample is the [Kingman coalescent](/kingman-coalescent/) (time in units of $2N$ generations), and mutations fall on each lineage at rate $\theta/2$; each mutation makes a new allele. Let $a_j$ be the number of alleles that have exactly $j$ copies in the sample, so $\sum_j j a_j = n$, and let $K = \sum_j a_j$ be the number of distinct alleles. Write $\theta^{(n)} = \theta(\theta + 1)\cdots(\theta + n - 1)$.

**Theorem (Ewens 1972).**

(a) The allele counts have the law

$$\Pr(a_1, \ldots, a_n) = \frac{n!}{\theta^{(n)}} \prod_{j=1}^{n} \frac{(\theta/j)^{a_j}}{a_j!}.$$

(b) The number of alleles has the law $\Pr(K = k) = |s(n, k)|\,\theta^k/\theta^{(n)}$, where $|s(n, k)|$ is the unsigned [Stirling number](/stirling-numbers/) of the first kind.

(c) Given $K = k$, the law of $(a_1, \ldots, a_n)$ does not depend on $\theta$. So $K$ is a [sufficient statistic](/sufficient-statistic/) for $\theta$.

(d) $K$ is a sum of independent Bernoulli variables with means $\theta/(\theta + i)$, $i = 0, \ldots, n - 1$, so

$$\mathbb E[K] = \sum_{i=0}^{n-1} \frac{\theta}{\theta + i}, \qquad \operatorname{Var}(K) = \sum_{i=0}^{n-1} \frac{\theta\,i}{(\theta + i)^2}.$$

**Check values.** For $n = 3$ and $\theta = 2$, the profiles $(3, 0, 0)$ (three different alleles), $(1, 1, 0)$ and $(0, 0, 1)$ (one allele) have probabilities $1/3$, $1/2$ and $1/6$. For $n = 3$ and $\theta = 1$ they are $1/6$, $1/2$ and $1/3$. For $n = 10$ and $\theta = 2$, $\mathbb E[K] = 4.03975$ and $\operatorname{Var}(K) = 1.80763$.

## In plain words

Take a few genes from a population in which every mutation makes a new variant and no variant is better than another. Some variants appear once in the sample, some twice, and so on. The formula gives the chance of each such pattern. It depends on a single number, which says how often mutations happen compared with how fast chance removes variants. When that number is large, the sample has many variants, most of them seen once; when it is small, most genes carry the same variant. The surprising part is that only the number of different variants tells you about that single number. How the genes are spread among the variants adds nothing, so it can be used to check whether the variants really are neutral.

## Proof

**Step 1: the coalescent gives an urn.** Follow the genealogy of the sample back in time and stop each lineage at its most recent mutation; the sample genes below that mutation, with no other mutation between, form one allele class. With $k$ lineages, coalescences happen at rate $\binom{k}{2}$ and mutations at rate $k\theta/2$. So the next event is a mutation with probability $\theta/(\theta + k - 1)$ and a coalescence with probability $(k - 1)/(\theta + k - 1)$, and by exchangeability the lineages involved are uniform. Read forward, from one lineage up to $n$, this is the Hoppe urn (Hoppe 1984): gene $k + 1$ is a new allele with probability $\theta/(\theta + k)$, and otherwise it copies the allele of one of the first $k$ genes, chosen uniformly.

**Step 2: the urn gives the formula.** Fix a partition of the genes $1, \ldots, n$ into $k$ classes of sizes $n_1, \ldots, n_k$. The urn makes exactly this partition with probability

$$\frac{\theta^k \prod_{i=1}^{k} (n_i - 1)!}{\theta^{(n)}},$$

because the $k$ first genes of the classes contribute $\theta$ each, a gene that joins a class that has $m$ genes contributes $m$, and the denominators are $\theta, \theta + 1, \ldots, \theta + n - 1$. This depends only on the class sizes. The number of partitions of $\{1, \ldots, n\}$ with $a_j$ classes of size $j$ is $n!/\prod_j (j!)^{a_j} a_j!$. Multiplying, and using $(j - 1)!/j! = 1/j$, gives (a).

**Step 3: the number of alleles.** Summing the probability of Step 2 over all partitions into $k$ classes gives $\theta^k/\theta^{(n)}$ times $\sum \prod_i (n_i - 1)!$. This sum counts the permutations of $n$ elements with $k$ cycles (each class of size $m$ can be made into a cycle in $(m - 1)!$ ways), which is $|s(n, k)|$. This proves (b).

**Step 4: sufficiency.** Dividing (a) by (b), the factors $\theta^k$ and $\theta^{(n)}$ cancel:

$$\Pr(a \mid K = k) = \frac{n!}{|s(n, k)|} \prod_j \frac{1}{j^{a_j} a_j!},$$

which does not depend on $\theta$. This proves (c).

**Step 5: moments.** In the urn, gene $i + 1$ starts a new allele with probability $\theta/(\theta + i)$, independently of the earlier steps, and $K$ is the number of genes that do. This proves (d). $\square$

## Consequences

**Random permutations.** With $\theta = 1$, $\theta^{(n)} = n!$, and the formula is $\prod_j 1/(j^{a_j} a_j!)$, Cauchy's formula for the share of permutations with $a_j$ cycles of length $j$. So the allele counts of a sample with $\theta = 1$ have the law of the cycle type of a uniform [random permutation](/random-permutation/). For $n = 4$ the five profiles have probabilities $1/24$, $1/4$, $1/8$, $1/3$ and $1/4$, and $K$ takes the values 1, 2, 3, 4 with probabilities $1/4$, $11/24$, $1/4$ and $1/24$.

**Independent Poisson counts.** Let $Z_1, \ldots, Z_n$ be independent with $Z_j$ Poisson with mean $\theta/j$. Then $\Pr(Z = a)$ is proportional to $\prod_j (\theta/j)^{a_j}/a_j!$, so the formula is the law of $Z$ given $\sum_j jZ_j = n$. As $n \to \infty$, the number of alleles with $j$ copies tends to a Poisson variable with mean $\theta/j$, for each fixed $j$. In particular, a large sample has about $\theta$ singletons; for $n = 10$ and $\theta = 2$ the exact mean number of singletons is $n\theta/(\theta + n - 1) = 20/11$.

**Estimating theta.** By (c), all the information about $\theta$ is in $K$. The log-likelihood is $k \ln \theta - \ln \theta^{(n)}$, and the [maximum likelihood](/maximum-likelihood-estimation/) estimate solves $k = \sum_{i=0}^{n-1} \hat\theta/(\hat\theta + i)$. For $n = 10$ and $k = 4$, $\hat\theta = 1.956$. The Fisher information is $\operatorname{Var}(K)/\theta^2 \approx \ln n/\theta$, so the variance of the estimate falls only like $\theta/\ln n$: a much larger sample gives little more precision. This is a property of the model, not of the estimator.

**Tests of neutrality.** Because the law of the counts given $K$ does not involve $\theta$, one can test neutrality without estimating $\theta$. The Ewens-Watterson test compares the homozygosity $\sum_i (n_i/n)^2$ of the sample with its law given $K$ (Ewens 2004, Section 11.2.2): too even counts point to balancing selection, too uneven ones to purifying selection or a population expansion.

**Clustering.** The Hoppe urn without the special role of mutation is the Chinese restaurant process, and (b) is the law of the number of clusters in a sample from a [Dirichlet process](/dirichlet-process/) with concentration $\theta$ (Antoniak 1974).

## Tightness

**Large N and small u.** The formula is exact for the coalescent limit. For a finite Wright-Fisher population it is an approximation. For a sample of two genes it gives $\Pr(\text{same allele}) = 1/(1 + \theta)$; the exact Wright-Fisher value is the equilibrium homozygosity of the [infinite alleles model](/infinite-alleles-model/). With $2N = 20$ and $u = 0.05$ ($\theta = 2$) that value is $0.316389$, against $1/3$ from the formula: 5 percent off. With $N = 50$ and $u = 0.001$ it is $0.833125$ against $0.833333$.

**Neutrality.** With selection the formula fails. Under heterozygote advantage the allele counts are more even than it predicts, and under purifying selection there are too many rare alleles.

**Equilibrium and constant size.** The population must have been at equilibrium for a time of order $N$ generations. After a recent expansion, the sample has too many alleles seen once; after a bottleneck, too few alleles. Population structure also changes the law.

**New alleles only.** If mutation can make an allele that already exists, as in a stepwise model of microsatellites or in electrophoretic classes of proteins, the formula does not hold. In particular, $K$ is then not sufficient for $\theta$.

## History

Ewens (1972) found the formula and its consequences for estimation and testing; Karlin and McGregor (1972) gave a second proof in the same year. Kingman (1978, 1982) placed it in his theory of partition structures and explained it through the coalescent. Hoppe (1984) gave the urn. Antoniak (1974) found the same law independently in Bayesian statistics, and Watterson (1977) built the test of neutrality on the conditional law given $K$.

## References
