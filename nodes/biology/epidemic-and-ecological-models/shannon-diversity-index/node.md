---
tag: 4HC8AE
kind: definition
slug: shannon-diversity-index
name: Shannon diversity index
aliases:
- Shannon-Wiener index
area: biology/epidemic-and-ecological-models
level: intro
summary: The entropy of the relative species abundances in a community, which grows with both the number of species and their evenness.
history:
  year: 1948
  people: [Claude E. Shannon]
  note: Shannon defined the entropy of a probability distribution in 1948 for communication, and ecologists took it as a diversity index in the 1950s and 1960s.
prereqs: [shannon-entropy]
see_also: [shannon-entropy, kullback-leibler-divergence, simpson-diversity-index, rarefaction, chao1-estimator, perplexity, gini-impurity]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: Claude E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: pages 379 to 423 (the entropy H = -K sum p_i log p_i and its properties)
  - paper: doi:10.2307/1934352
    title: M. O. Hill, Diversity and evenness, a unifying notation and its consequences, Ecology 54(2), 1973
    locator: pages 427 to 432 (the diversity numbers of order a, with exp(H) as the number of order 1)
  - paper: doi:10.1111/j.2006.0030-1299.14714.x
    title: Lou Jost, Entropy and diversity, Oikos 113(2), 2006
    locator: pages 363 to 375 (entropies and indices against the effective number of species)
  - book: isbn:9780632056330
    title: Anne E. Magurran, Measuring Biological Diversity, Blackwell, 2004
    locator: the chapter on diversity indices (the Shannon index, its evenness measure and its sampling properties)
---

The Shannon diversity index of a community is the [Shannon entropy](/shannon-entropy/) of its relative species abundances, $H = -\sum_i p_i \ln p_i$. It is 0 when one species makes up the whole community. It grows when species are added, and it grows when the abundances become more even. For $S$ species it is at most $\ln S$, the value of a perfectly even community. Ecologists usually compute it with the natural logarithm, so its unit is the nat. The number $e^H$ is easier to read: it is the number of equally common species that would give the same entropy, the effective number of species. The index is also called the Shannon-Wiener or the Shannon-Weaver index, but Wiener did not define it.

## Definition

Let a community have $S$ species with relative abundances $p_1, \ldots, p_S \ge 0$ and $\sum_{i=1}^{S} p_i = 1$. The **Shannon diversity index** is

$$H = -\sum_{i=1}^{S} p_i \ln p_i, \qquad 0 \ln 0 = 0.$$

The **effective number of species** is $D_1 = e^H$, and **Pielou's evenness** is $J = H / \ln S$ for $S \ge 2$.

In a sample of $n$ individuals with $n_i$ of species $i$, the **plug-in estimate** is

$$\hat H = -\sum_{i : n_i > 0} \frac{n_i}{n} \ln \frac{n_i}{n} = \ln n - \frac{1}{n} \sum_{i : n_i > 0} n_i \ln n_i.$$

It has negative bias: unseen species add nothing, and even for the species that are seen, $\mathbb{E}[\hat H] < H$. The **Miller-Madow correction** adds $(S_{obs} - 1) / (2 n)$, with $S_{obs}$ the number of observed species. This is the first term of the bias for a fixed number of species and large $n$ (an asymptotic result, not an exact correction).

Properties that follow from the definition (theorems):
- $0 \le H \le \ln S$. $H = 0$ if and only if one $p_i = 1$, and $H = \ln S$ if and only if all $p_i = 1/S$.
- $H = \ln S - D_{KL}(p \,\|\, u)$, where $u$ is the uniform distribution on the $S$ species and $D_{KL}$ is the [Kullback-Leibler divergence](/kullback-leibler-divergence/). So $\ln S - H$ measures how far the community is from even.
- Grouping: if the species are split into groups with total abundances $w_g$, then $H$ is the entropy of $(w_g)$ plus $\sum_g w_g H_g$, where $H_g$ is the entropy of the abundances within group $g$.
- A change of the base of the logarithm multiplies $H$ by a constant: $H$ in bits is $H / \ln 2$.

## Examples and non-examples

- The abundances $(5, 3, 2)$ give $p = (0.5, 0.3, 0.2)$ and $H = 1.029653$ nats, or $1.485475$ bits. Then $e^H = 2.800094$, so the community is as diverse as $2.8$ equally common species, and $J = 1.029653 / \ln 3 = 0.937231$. As a sample of $n = 10$, the Miller-Madow form is $1.029653 + 2/20 = 1.129653$.
- The counts $(10, 6, 4)$ have the same proportions, so they give the same $H = 1.029653$. The index depends only on the proportions. The Miller-Madow form is $1.029653 + 2/40 = 1.079653$, closer to the plug-in value because the sample is larger.
- Four species with 25 individuals each give $H = \ln 4 = 1.386294$, $e^H = 4$ and $J = 1$.
- The counts $(97, 1, 1, 1)$ have four species, but one species makes up 97 percent. They give $H = 0.167701$, $e^H = 1.182582$ and $J = 0.120970$.
- **Non-example: a raw count.** $-\sum n_i \ln n_i$ with counts in place of proportions is not the index. It depends on the sample size and can be negative.
- **Non-example: comparing samples of unequal size.** The plug-in $\hat H$ of a sample of 50 individuals and that of a sample of 5000 are not comparable, because the bias depends on $n$. Use [rarefaction](/rarefaction/) to a common size, or a bias-corrected estimate.
- **Non-example: a difference of entropies as a difference of diversity.** $H$ is not linear in the number of species: going from 1 to 2 equally common species adds $0.693$, and going from 100 to 101 adds $0.010$. Compare $e^H$ instead.

The pseudocode below computes the plug-in estimate and the derived quantities from a list of counts.

```pseudo id=main
SHANNON(counts)
L1  n ← the sum of the counts; S ← the number of counts > 0
L2  H ← 0
L3  for each count c > 0: p ← c / n; H ← H - p ln p
L4  return (H, e^H, H / ln S if S ≥ 2, H + (S - 1) / (2 n))
```

## Related definitions

- [Shannon entropy](/shannon-entropy/) is the same quantity for any discrete distribution, with the base 2 logarithm in coding.
- The [Simpson diversity index](/simpson-diversity-index/) uses $\sum p_i^2$ in place of $\sum p_i \ln p_i$. It gives more weight to common species. Hill's diversity numbers $D_q = (\sum p_i^q)^{1/(1 - q)}$ join both: $D_0 = S$, $D_1 = e^H$ (the limit as $q \to 1$) and $D_2 = 1 / \sum p_i^2$.
- [Perplexity](/perplexity/) in language modeling is the same exponential of an entropy, the effective number of choices.
- [Gini impurity](/gini-impurity/) in decision trees is the Gini-Simpson index $1 - \sum p_i^2$, the order 2 counterpart of $H$.
- [Rarefaction](/rarefaction/) and the [Chao1 estimator](/chao1-estimator/) address the same sampling problem for the number of species, the diversity of order 0.

## References
