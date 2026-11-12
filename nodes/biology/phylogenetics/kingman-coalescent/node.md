---
tag: 6QE1Y8
kind: model
slug: kingman-coalescent
name: Kingman coalescent
aliases:
- standard coalescent
- n-coalescent
area: biology/phylogenetics
level: advanced
summary: "The neutral coalescent of one panmictic population: with k lineages, wait an exponential time of rate k(k-1)/2, then merge a uniform pair."
history:
  year: 1982
  people: [J. F. C. Kingman]
  note: Kingman defined the coalescent and proved that it is the limit of the genealogy of a sample in a large population in 1982.
prereqs: [coalescent-theory, markov-chain, harmonic-series]
see_also: [coalescent-theory, multispecies-coalescent, yule-model, ancestral-recombination-graph, incomplete-lineage-sorting, poisson-distribution, variance]
sources:
  - paper: doi:10.1016/0304-4149(82)90011-4
    title: J. F. C. Kingman, The coalescent, Stochastic Processes and their Applications 13(3), 1982
    locator: pp. 235-248 (the n-coalescent as a Markov chain on partitions, and its rates)
  - paper: doi:10.1016/0040-5809(75)90020-9
    title: G. A. Watterson, On the number of segregating sites in genetical models without recombination, Theoretical Population Biology 7(2), 1975
    locator: pp. 256-276 (E[S] = theta a_n, Var[S] = theta a_n + theta^2 b_n, and the estimator S / a_n)
  - book: isbn:9780974707754
    title: John Wakeley, Coalescent Theory, An Introduction, Roberts and Company, 2009
    locator: Chapter 3 (the coalescent, times to common ancestry and total branch length)
  - paper: doi:10.1006/tpbi.1995.1025
    title: Yun-Xin Fu, Statistical properties of segregating sites, Theoretical Population Biology 48(2), 1995
    locator: pp. 172-197 (the expected number of sites with i derived copies, theta / i)
---

The Kingman coalescent is the random genealogy of a sample of $n$ gene copies from a large neutral population with constant size and random mating. Going back in time, while $k$ lineages remain, the process waits an exponential time with rate $\binom{k}{2} = k(k-1)/2$ and then merges one pair of lineages chosen uniformly. Kingman defined it in 1982 and proved that it is the limit of the genealogy in the Wright-Fisher model and in a wider class of models. It is the base model of [coalescent theory](/coalescent-theory/), and it runs inside each branch of the [multispecies coalescent](/multispecies-coalescent/).

## The machine

**The state.** The state is a partition of the sample $\{1, \ldots, n\}$ into blocks. Each block is one ancestral lineage, and it holds the sampled copies that descend from it. The process starts with $n$ singleton blocks and stops with one block.

**The moves.** Each pair of blocks merges at rate 1, independently of the other pairs. So from a state with $k$ blocks the next event comes after a time $T_k \sim \text{Exp}\big(\binom{k}{2}\big)$, and the pair that merges is uniform among the $\binom{k}{2}$ pairs. The times $T_n, T_{n-1}, \ldots, T_2$ are independent, and they are independent of the order of the merges. It is a continuous-time [Markov chain](/markov-chain/) on partitions.

**The time unit.** Time is in coalescent units: $2N$ generations for a diploid population of $N$ individuals ($2N$ gene copies), or $N$ generations for a haploid population of $N$ copies. All numbers on this page use this unit. For other population models with offspring variance $\sigma^2$ per copy, the unit is $2N/\sigma^2$ generations (diploid) instead of $2N$.

**Why these rates.** In a haploid Wright-Fisher population of $N$ copies, two copies pick the same parent with probability $1/N$. With $k$ copies, the probability that some pair shares a parent in one generation is $\binom{k}{2}/N + O(k^4/N^2)$. So the number of generations to the first merge, divided by $N$, tends to $\text{Exp}\big(\binom{k}{2}\big)$, and the chance of a triple merge or of two merges in one generation vanishes in the limit. Kingman proved the convergence of the whole genealogy, not only of one wait.

**Mutations.** Under the neutral infinite-sites model, mutations fall on each branch as a Poisson process with rate $\theta/2$ per unit of time, with $\theta = 4N\mu$ (diploid) or $\theta = 2N\mu$ (haploid), where $\mu$ is the mutation rate of the region per copy per generation. Each mutation hits a new site.

**A simulation.**

```pseudo id=main
SIMULATE-COALESCENT(n)
L1  lineages ← [{1}, {2}, ..., {n}]
L2  for k ← n down to 2 do
L3      draw T_k from Exp(k(k − 1)/2)
L4      choose two distinct lineages A, B uniformly
L5      replace A and B by one lineage A ∪ B
L6  return the tree of the merges and the waits T_n, ..., T_2
```

It uses $n - 1$ steps. With a list and a swap-to-the-end deletion, each step takes $O(1)$ time, so a sample takes $O(n)$ time.

**A trace.** A run of the implementation with seed 7, for $n = 4$ copies labeled 0 to 3, draws $T_4 \approx 0.065$, $T_3 \approx 0.351$ and $T_2 \approx 0.455$. The first two merges join copy 0 with copy 2 and copy 1 with copy 3, and the last merge joins the two pairs, so the tree is $((0,2),(1,3))$. The time to the MRCA is $0.065 + 0.351 + 0.455 \approx 0.871$, and the total branch length is $4 \cdot 0.065 + 3 \cdot 0.351 + 2 \cdot 0.455 \approx 2.224$. The expected values for $n = 4$ are $1.5$ and $11/3 \approx 3.667$.

## What it counts

- $T_k$, the time while $k$ lineages remain, for $k = n, \ldots, 2$.
- $T_{\text{MRCA}} = \sum_{k=2}^n T_k$, the age of the most recent common ancestor of the sample.
- $L = \sum_{k=2}^n k T_k$, the total branch length, because $k$ branches exist during $T_k$.
- The labeled tree shape and the order of the merges (the ranked labeled history).
- With mutations: the number $S$ of segregating sites, and the site frequency spectrum $\xi_1, \ldots, \xi_{n-1}$, where $\xi_i$ counts the sites at which $i$ of the $n$ copies carry the derived allele.

## Relation to other models

- **Wright-Fisher and Moran models.** These are forward-time population models. The Kingman coalescent is the limit of their sample genealogies as the population size grows. The Moran model has a different time scale per generation, but it has the same limit after rescaling.
- **[Yule model](/yule-model/).** Both models give each ranked labeled history the same probability $2^{n-1}/(n!\,(n-1)!)$, so they give the same distribution on labeled tree shapes. The waiting times differ: rate $\binom{k}{2}$ in the coalescent and $k\lambda$ in the Yule model.
- **[Multispecies coalescent](/multispecies-coalescent/).** It runs one Kingman coalescent in each branch of a species tree, with its own population size, and lets lineages that do not merge pass into the ancestral branch.
- **[Ancestral recombination graph](/ancestral-recombination-graph/).** With recombination, a lineage can also split into two going back in time. The genealogy is then a graph, and each site has its own Kingman-like tree.
- **Coalescents with multiple mergers.** In populations where one parent can have a large fraction of the next generation, more than two lineages can merge at once. The Kingman coalescent is the case with only pairwise merges.

## Known results in the model

Write $a_n = \sum_{i=1}^{n-1} 1/i$ and $b_n = \sum_{i=1}^{n-1} 1/i^2$. Each result holds for each $n \ge 2$, in coalescent units.

**Time to the MRCA.** $E[T_{\text{MRCA}}] = 2(1 - 1/n)$.

*Proof.* $E[T_k] = 1/\binom{k}{2} = \frac{2}{k(k-1)} = 2\left(\frac{1}{k-1} - \frac{1}{k}\right)$. The sum over $k = 2, \ldots, n$ telescopes to $2(1 - 1/n)$. $\square$

So $E[T_{\text{MRCA}}] < 2$ for every sample size, while $E[T_2] = 1$: the last wait is on average more than half of the depth.

**Its variance.** $\operatorname{Var}[T_{\text{MRCA}}] = \sum_{k=2}^{n} \frac{4}{k^2 (k-1)^2}$, because the $T_k$ are independent and an exponential of rate $r$ has variance $1/r^2$. The limit as $n \to \infty$ is $\frac{4\pi^2}{3} - 12 \approx 1.159$. For $n = 10$ the variance is $\approx 1.158$, so the depth of the tree has a standard deviation of about $1.08$ units around its mean of $1.8$.

**Total branch length.** $E[L] = 2a_n$ and $\operatorname{Var}[L] = 4 b_n$.

*Proof.* $E[k T_k] = k \cdot \frac{2}{k(k-1)} = \frac{2}{k-1}$; the sum over $k = 2, \ldots, n$ is $2 a_n$. By independence, $\operatorname{Var}[L] = \sum_k k^2 \operatorname{Var}[T_k] = \sum_k \frac{4}{(k-1)^2} = 4 b_n$. $\square$

$E[L]$ grows like $2 \ln n$: a sample of 1000 copies has $E[L] \approx 14.97$, only about 2.6 times the value $5.66$ for 10 copies.

**Segregating sites (Watterson 1975).** $E[S] = \theta a_n$ and $\operatorname{Var}[S] = \theta a_n + \theta^2 b_n$. So $\hat\theta_W = S/a_n$ is an unbiased estimator of $\theta$.

*Proof.* Given the tree, $S$ is Poisson with mean $\theta L / 2$. So $E[S] = \frac{\theta}{2} E[L] = \theta a_n$. By the law of total variance, $\operatorname{Var}[S] = E[\theta L/2] + \operatorname{Var}[\theta L/2] = \theta a_n + \frac{\theta^2}{4} \cdot 4 b_n$. $\square$

The variance has the term $\theta^2 b_n$, and $b_n < \pi^2/6$. So the relative error of $\hat\theta_W$ does not go to zero as $n$ grows: more copies from one region do not remove the randomness of its single genealogy. More independent regions do.

**The ranked history is uniform.** Each sequence of merges has probability $\prod_{k=2}^{n} 1/\binom{k}{2} = \frac{2^{n-1}}{n!\,(n-1)!}$, the same for all sequences. A labeled tree shape $T$ therefore has probability equal to its number of rankings times this value, which is the [Yule](/yule-model/) probability $\frac{2^{n-1}}{n!} \prod_{v} \frac{1}{n_v - 1}$, with $n_v$ the number of leaves below the internal node $v$.

**The root split.** Take one of the two lineages just below the root, at random. The number of sampled copies below it is uniform on $\{1, \ldots, n-1\}$.

*Proof.* Read the ranked history forward in time, from the root: each merge backward is a split forward. The coalescent and the Yule model give every ranked labeled history the same probability (the result above), so the forward reading of the coalescent has the law of the Yule process, in which the lineage that splits is uniform among the lineages present. Colour the two root lineages and their descendants red and blue. Each split of a red lineage adds one red lineage, so the counts follow a Pólya urn that starts with one red and one blue ball and adds $n - 2$ balls. After $m$ draws, the number of red balls is uniform on $\{1, \ldots, m+1\}$, by induction: if it is uniform on $\{1, \ldots, m+1\}$, then $P(\text{red} = j \text{ after } m+1) = \frac{1}{m+1}\left(\frac{j-1}{m+2} + \frac{m+2-j}{m+2}\right) = \frac{1}{m+2}$. With $m = n - 2$ this is uniform on $\{1, \ldots, n-1\}$. $\square$

**Site frequency spectrum.** Fu (1995) showed that $E[\xi_i] = \theta / i$ for $i = 1, \ldots, n-1$. The sum over $i$ is $\theta a_n = E[S]$, as it must be.

## References
