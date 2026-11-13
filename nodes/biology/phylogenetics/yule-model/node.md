---
tag: CV9KCF
kind: model
slug: yule-model
name: Yule model
aliases:
- pure-birth process
- Yule process
- Yule-Harding model
area: biology/phylogenetics
level: advanced
summary: A pure-birth model of speciation. Each lineage splits at rate lambda and none dies; all ranked labeled histories of n tips are equally likely.
history:
  year: 1925
  people: [G. Udny Yule]
  note: Yule used a pure-birth process in 1925 to model the numbers of species in genera.
prereqs: [rooted-and-unrooted-trees, markov-chain]
see_also: [birth-death-process, kingman-coalescent, coalescent-theory, phylogenetic-tree, rooted-and-unrooted-trees, catalan-numbers]
sources:
  - paper: doi:10.1098/rstb.1925.0002
    title: G. Udny Yule, A mathematical theory of evolution, based on the conclusions of Dr. J. C. Willis, F.R.S., Philosophical Transactions of the Royal Society of London B 213, 1925
    locator: pp. 21-87 (the pure-birth process of species within a genus)
  - book: isbn:9781611974478
    title: Mike Steel, Phylogeny, Discrete and Random Processes in Evolution, SIAM, 2016
    locator: Chapter 3 (tree shape and random discrete phylogenies, the Yule-Harding distribution)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 33 (tests based on tree shape)
  - paper: doi:10.1016/S0025-5564(99)00060-7
    title: Andy McKenzie and Mike Steel, Distributions of cherries for two models of trees, Mathematical Biosciences 164(1), 2000
    locator: pp. 81-92 (the mean n/3 of the number of cherries under the Yule model)
---

The Yule model is a random model of a growing tree of species in which each lineage splits into two at a constant rate $\lambda$, independently of the others, and no lineage goes extinct. It is the pure-birth case $\mu = 0$ of the [birth-death process](/birth-death-process/). Run from one lineage until $n$ lineages exist, it gives a random rooted binary tree with branch lengths, and labels the $n$ tips in a uniform random order. Its distribution on labeled tree shapes, often called the Yule-Harding distribution, is the standard null model for the shape of a [phylogenetic tree](/phylogenetic-tree/).

## The machine

**The state.** The state is the number $k$ of living lineages, together with the tree drawn so far. It is a continuous-time [Markov chain](/markov-chain/).

**The moves.** Each lineage splits at rate $\lambda$. With $k$ lineages the next split comes after an exponential time with rate $k\lambda$, and the lineage that splits is uniform among the $k$. The waits are independent of the choices of lineages.

**The stop rule.** Two stop rules are common. Stop at a fixed time $t$: then the number of tips $N(t)$ is random. Or stop when $n$ lineages exist, and then the tips get the labels $1, \ldots, n$ in a uniform random order. The tree shape results below use the second rule.

```pseudo id=main
SIMULATE-YULE(n, λ)
L1  lineages ← [root]
L2  for k ← 1 to n − 1 do
L3      draw a wait from Exp(kλ)          ▷ add it to each living branch
L4      choose a lineage x uniformly from the k lineages
L5      replace x by two new child lineages of x
L6  give the labels 1, ..., n to the n lineages in a uniform random order
L7  return the tree
```

The run takes $n - 1$ steps of $O(1)$ time each, apart from the labeling, so $O(n)$ time.

**Ranked trees.** The *rank* of a split is its place in time: the first split has rank 1, and the last has rank $n - 1$. A *ranked labeled history* is a labeled rooted binary tree together with the order of its splits. A *ranked tree shape* is the same without the labels.

## What it counts

- The number of lineages $N(t)$ at time $t$, and the waits between splits.
- The labeled topology, its ranking, and the unlabeled shape.
- Statistics of tree balance, such as the number of *cherries* (internal nodes whose two children are tips) and the sizes of the two clades at the root.

## Relation to other models

- **[Birth-death process](/birth-death-process/).** The Yule model is the case with extinction rate $\mu = 0$. The reconstructed tree of a constant-rate birth-death process, the tree of the lineages that survive, has the same distribution of labeled topologies as the Yule model, but other branch lengths.
- **[Kingman coalescent](/kingman-coalescent/).** The coalescent builds a gene tree backward in time. It gives each ranked labeled history the same probability as the Yule model, so the two give the same distribution of topologies. The waits differ: rate $k\lambda$ forward here, rate $k(k-1)/2$ backward there.
- **The uniform model.** The uniform (proportional to distinguishable arrangements) model gives each of the $(2n - 3)!!$ labeled rooted binary trees the same probability. It gives more weight to unbalanced trees than the Yule model does. For $n = 4$, the uniform model gives the balanced shape probability $3/15 = 0.2$, and the Yule model gives $1/3$.

## Known results in the model

Write $n_v$ for the number of tips below an internal node $v$, and $c(T)$ for the number of cherries of $T$.

**The number of lineages.** Started from one lineage, $P(N(t) = m) = e^{-\lambda t}(1 - e^{-\lambda t})^{m-1}$ for $m \ge 1$: a geometric law with mean $E[N(t)] = e^{\lambda t}$.

*Proof.* Let $p_m(t) = P(N(t) = m)$. The forward equations of the chain are $p_m' = \lambda (m-1) p_{m-1} - \lambda m p_m$, with $p_1(0) = 1$. Put $q = e^{-\lambda t}$ and $p_m = q(1-q)^{m-1}$. Since $q' = -\lambda q$, we get $p_m' = -\lambda q (1-q)^{m-1} + \lambda (m-1) q^2 (1-q)^{m-2}$. The right side of the equation is $\lambda (m-1) q (1-q)^{m-2} - \lambda m q (1-q)^{m-1} = \lambda (m-1) q (1-q)^{m-2} \big(1 - (1-q)\big) - \lambda q (1-q)^{m-1}$, which is the same. The initial value is right, and the solution of this linear system is unique. The mean of a geometric law with success probability $q$ is $1/q = e^{\lambda t}$. $\square$

**The waits.** When the run stops at $n$ tips, the time with $k$ lineages is $\text{Exp}(k\lambda)$, so the expected time back to the start of the run, the origin of the stem lineage, is $\frac{1}{\lambda} \sum_{k=1}^{n-1} \frac{1}{k}$. The root split, the first split, comes after the wait with one lineage, so its expected age is $\frac{1}{\lambda} \sum_{k=2}^{n-1} \frac{1}{k}$.

**Every ranked labeled history has the same probability.** It is $\dfrac{2^{n-1}}{n!\,(n-1)!}$, and there are $\dfrac{n!\,(n-1)!}{2^{n-1}}$ ranked labeled histories.

*Proof.* A run is fixed by its choices of lineages and by its labeling. Record the lineages in a list; when $x$ splits, one child takes the place of $x$ and the other goes to the end. A choice sequence then names a position in $\{1, \ldots, k\}$ at step $k$, so there are $(n-1)!$ sequences, each with probability $\prod_{k=1}^{n-1} \frac{1}{k} = \frac{1}{(n-1)!}$, and $n!$ labelings, each with probability $\frac{1}{n!}$. A ranked labeled history together with a choice, at each of its $n - 1$ splits, of which child keeps the place of the parent, fixes the choice sequence and the labeling, and each pair arises from exactly one such history and choice. So each history has $2^{n-1}$ preimages, each of probability $\frac{1}{n!\,(n-1)!}$. The count follows because the probabilities sum to 1. $\square$

**The probability of a labeled topology.** For a labeled rooted binary tree $T$ with $n$ tips,

$$P(T) = \frac{2^{n-1}}{n!} \prod_{v \text{ internal}} \frac{1}{n_v - 1}.$$

*Proof.* By the result above, $P(T)$ is the number of rankings of $T$ times $\frac{2^{n-1}}{n!\,(n-1)!}$. A ranking is an order of the $n - 1$ internal nodes in which each node comes after its ancestors. The subtree of $v$ has $n_v - 1$ internal nodes. We show by induction on the size that the number of rankings is $\frac{(n-1)!}{\prod_v (n_v - 1)}$. For a cherry, both sides are 1. At the root, the two subtrees have $i$ and $j$ internal nodes with $i + j = n - 2$. The root comes first, and the two rankings of the subtrees interleave in $\binom{n-2}{i}$ ways. By induction this gives $\frac{(n-2)!}{i!\,j!} \cdot \frac{i!}{\prod_{\text{left}}} \cdot \frac{j!}{\prod_{\text{right}}} = \frac{(n-2)!}{\prod_{v \ne \text{root}} (n_v - 1)}$, and the root factor is $n_{\text{root}} - 1 = n - 1$. $\square$

**The probability of a ranked tree shape.** For a ranked tree shape $R$ with $n$ tips,

$$P(R) = \frac{2^{\,n-1-c(R)}}{(n-1)!}.$$

*Proof.* Without the labeling, a run is its choice sequence, with probability $\frac{1}{(n-1)!}$. A ranked shape together with a choice, at each split, of the child that keeps the place of the parent fixes the sequence. At a cherry both children are tips that never split, so the two choices give the same sequence. At any other split the two children differ, because one of them holds a split of a rank that the other does not hold, so the two choices give different sequences. So $R$ has $2^{n-1-c(R)}$ sequences. $\square$

**Cherries.** The expected number of cherries is $n/3$ for $n \ge 3$ (McKenzie and Steel 2000).

**The root split.** The number of tips on a randomly chosen side of the root is uniform on $\{1, \ldots, n-1\}$, by the same Pólya urn argument as on the [Kingman coalescent](/kingman-coalescent/) page.

**Small cases.** For $n = 4$ there are 15 labeled topologies:

| shape | sizes $n_v$ | labeled trees | each | total |
|---|---|---|---|---|
| caterpillar $(((a,b),c),d)$ | 2, 3, 4 | 12 | $1/18$ | $2/3$ |
| balanced $((a,b),(c,d))$ | 2, 2, 4 | 3 | $1/9$ | $1/3$ |

The balanced tree has two rankings, and the caterpillar has one, so each balanced labeled tree is twice as likely. For $n = 5$ there are 105 labeled topologies:

| shape | labeled trees | each | total |
|---|---|---|---|
| $((((a,b),c),d),e)$ | 60 | $1/180$ | $1/3$ |
| $(((a,b),c),(d,e))$ | 30 | $1/60$ | $1/2$ |
| $(((a,b),(c,d)),e)$ | 15 | $1/90$ | $1/6$ |

The five ranked shapes of $n = 5$ are the ranked caterpillar, with one cherry and probability $2^3/4! = 1/3$, and four ranked shapes with two cherries, each with probability $2^2/4! = 1/6$.

**At a fixed time.** With $\lambda = 1$ and $t = 2$, a run from one lineage still has one lineage with probability $e^{-2} \approx 0.135$, and the mean number of lineages is $e^2 \approx 7.39$.

## References
