---
tag: PE1XF4
kind: technique
slug: swap-rounding
name: Swap rounding
aliases:
- Chekuri-Vondrák-Zenklusen swap rounding
- randomized swap rounding
area: approximation/lp-rounding
level: research
summary: Round a point of a matroid base polytope by merging the bases of a convex combination with random exchanges; keeps marginals and gives negative correlation.
prereqs: [matroid, dependent-rounding, randomized-rounding, caratheodory-theorem]
see_also: [pipage-rounding, dependent-rounding, matroid, submodular-function, partition-matroid, uniform-matroid, graphic-matroid, matroid-intersection]
sources:
  - paper: "Chandra Chekuri, Jan Vondrák and Rico Zenklusen, Dependent randomized rounding via exchange properties of combinatorial structures, Proceedings of the 51st IEEE Symposium on Foundations of Computer Science (FOCS), 2010"
    locator: pages 575 to 584
  - paper: "Richard A. Brualdi, Comments on bases in dependence structures, Bulletin of the Australian Mathematical Society 1(2), 1969"
    locator: pages 161 to 167 (the symmetric exchange property of bases)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Part IV (matroids and submodular functions)
---

Swap rounding is a randomized rounding for a point $x$ in the base polytope of a [matroid](/matroid/). It writes $x$ as a convex combination of bases, $x = \sum_k \beta_k \mathbf{1}_{B_k}$, and merges the bases two at a time. To merge $B_1$ and $B_2$, it takes an element $i \in B_1 \setminus B_2$ and an element $j \in B_2 \setminus B_1$ that can be exchanged both ways, and with probabilities set by the weights, it makes one base look more like the other. The output $R$ is a base with $\Pr[i \in R] = x_i$ for each element. Chekuri, Vondrák and Zenklusen (2010) showed that its elements are negatively correlated, so Chernoff bounds hold for linear functions, and that a monotone submodular function of $R$ has a lower tail bound. The method is simpler and faster than [pipage rounding](/pipage-rounding/) on a matroid, and it gives the same kind of guarantee.

## In plain words

A fractional answer can be written as a mix of real answers, each with a weight. Swap rounding blends two of them into one, step by step, then blends the result with the next one, and so on.

At each step, it finds one item that is in the first answer only and one that is in the second only, such that trading them keeps both answers valid. Then a weighted coin decides which answer makes the trade. The odds are set so that, on average, each item appears as often as in the mix. In the end one real answer is left, and each item is in it with the chance that the fractional answer gave.

## When it applies

- **A matroid constraint.** The feasible sets are the bases, or the independent sets, of a matroid with an independence oracle, such as a [partition matroid](/partition-matroid/), a [uniform matroid](/uniform-matroid/) or the [graphic matroid](/graphic-matroid/) of spanning trees.
- **A convex combination of bases.** The fractional point is given as $x = \sum_{k=1}^{K} \beta_k \mathbf{1}_{B_k}$ with $\beta_k > 0$ and $\sum_k \beta_k = 1$. The continuous greedy algorithm for submodular maximization returns $x$ in this form. Otherwise a decomposition with at most $n + 1$ bases exists by [Carathéodory's theorem](/caratheodory-theorem/), and it can be found in polynomial time with the independence oracle.
- **Concentration or nonlinear objectives.** The analysis needs a tail bound for linear functions of the rounded set, or a bound on a submodular function of it.

## The template

```pseudo id=main
SWAP-ROUND((β_1, B_1), ..., (β_K, B_K))
L1  (γ, C) ← (β_1, B_1)
L2  for k ← 2 to K
L3      C ← MERGE(γ, C, β_k, B_k)
L4      γ ← γ + β_k
L5  return C

MERGE(β, A, β', A')
L6  while A ≠ A'
L7      i ← an element of A \ A'                                 ▷ hole: ORDER
L8      j ← an element of A' \ A with A − i + j and A' − j + i both bases
L9      with probability β/(β + β'): A' ← A' − j + i
L10     else: A ← A − i + j
L11 return A
```

**Exchange.** Line L8 always finds a $j$, by the symmetric exchange property of matroid bases (Brualdi, 1969): for bases $A, A'$ and $i \in A \setminus A'$, some $j \in A' \setminus A$ has both $A - i + j$ and $A' - j + i$ bases. After either branch, $|A \setminus A'|$ drops by 1, so MERGE takes at most $r$ steps, where $r$ is the rank. Line L8 tests at most $r$ candidates with two oracle calls each, so SWAP-ROUND uses $O(K r^2)$ oracle calls in the worst case.

**Theorem (Chekuri, Vondrák and Zenklusen).** The output $R$ is a base, and:

1. *Marginals:* $\Pr[i \in R] = x_i$ for each element $i$.
2. *Negative correlation:* for each set $T$ of elements, $\Pr[T \subseteq R] \le \prod_{i \in T} x_i$ and $\Pr[T \cap R = \emptyset] \le \prod_{i \in T} (1 - x_i)$.
3. *Linear tails:* for weights $w_i \in [0, 1]$ and $\mu = \sum_i w_i x_i$, the sum $\sum_{i \in R} w_i$ satisfies the Chernoff upper and lower tail bounds with mean $\mu$.
4. *Submodular lower tail:* for a monotone submodular $f$ with marginal values in $[0, 1]$ and $\mu = F(x)$, where $F$ is the multilinear extension, $\Pr[f(R) \le (1 - \delta) \mu] \le e^{-\mu \delta^2 / 8}$.

*Proof of items 1 and 2.* Track the vector $y = \gamma \mathbf{1}_C + \sum_{k' > k} \beta_{k'} \mathbf{1}_{B_{k'}}$, together with $\beta \mathbf{1}_A + \beta' \mathbf{1}_{A'}$ inside a merge. At the start $y = x$. In a step of MERGE, with probability $\beta/(\beta + \beta')$ the vector changes by $\beta' (\mathbf{1}_i - \mathbf{1}_j)$, and with probability $\beta'/(\beta + \beta')$ by $\beta (\mathbf{1}_j - \mathbf{1}_i)$. So it changes by $\Delta (\mathbf{1}_i - \mathbf{1}_j)$ with $\mathbb{E}[\Delta] = \frac{\beta \beta' - \beta' \beta}{\beta + \beta'} = 0$, and $y$ is a martingale with values in $[0, 1]^n$. At the end, $y = \mathbf{1}_R$, which gives item 1. For a set $T$, the product $\prod_{t \in T} y_t$ is linear in $\Delta$ when one of $i, j$ is in $T$, and changes by a term with expectation $-\mathbb{E}[\Delta^2] \prod_{t \in T \setminus \{i, j\}} y_t \le 0$ when both are. So its expectation does not grow, and at the end it is the indicator of $T \subseteq R$. The same holds for $\prod_{t \in T} (1 - y_t)$. $\square$

Item 3 follows from item 2, because negative correlation is enough for the proof of the Chernoff bound through $\mathbb{E}[e^{\lambda X}]$. Item 4 needs a separate martingale argument, given in the paper.

**The hole.** ORDER picks $i$ in line L7. Any order gives the theorem.

## Classic examples

- **Submodular maximization under a matroid and knapsacks.** Run the continuous greedy algorithm for a monotone [submodular function](/submodular-function/) over the matroid polytope, cut down by $O(1)$ linear packing constraints, then swap round. Item 4 keeps $f(R)$ near $F(x) \ge (1 - 1/e - \varepsilon) \text{OPT}$, and item 3 shows that each packing constraint is violated by little with high probability, after a scaling and a cleanup step. Chekuri, Vondrák and Zenklusen got $1 - 1/e - \varepsilon$ in this way.
- **Partition and uniform matroids.** For a [partition matroid](/partition-matroid/), swap rounding picks exactly one element of each part, with the given marginals and negative correlation. For a [uniform matroid](/uniform-matroid/) it picks exactly $k$ elements, as in Srinivasan's level-set rounding; see [dependent rounding](/dependent-rounding/).
- **Spanning trees.** For the [graphic matroid](/graphic-matroid/), a point in the spanning tree polytope rounds to a [spanning tree](/spanning-tree/) whose edges are negatively correlated. Negative correlation and the marginals are the properties used to find thin trees in the $O(\log n / \log \log n)$ algorithm for [asymmetric TSP](/asymmetric-tsp/) by Asadpour, Goemans, Mądry, Oveis Gharan and Saberi, so swap rounding can take the place of their maximum entropy sampling.

## Variations

- **Independent sets.** To round a point of the independence polytope, add dummy elements that complete it to a point of the base polytope of a larger matroid, round, and drop the dummies.
- **Randomized pipage on a matroid.** [Pipage rounding](/pipage-rounding/) with random directions gives the same marginals and negative correlation, but each step needs a submodular minimization to find a tight set, which makes it slower.
- **Matroid intersection.** For the intersection of two matroids, such as [bipartite matchings](/bipartite-matching/), full negative correlation is not possible: on a 4-cycle with $\frac12$ on each edge, two opposite edges are always chosen together. Only weaker properties hold, such as the correlation at each vertex that [dependent rounding](/dependent-rounding/) gives; see [matroid intersection](/matroid-intersection/).

## Pitfalls

- **No convex combination.** The method needs the decomposition into bases. A point $x$ of the polytope without it must first be decomposed, which costs many oracle calls.
- **Negative correlation for sets, not for all events.** The theorem bounds the events $T \subseteq R$ and $T \cap R = \emptyset$. Other events, such as "exactly one of $i, j$ is in $R$", need not have their independent probability.
- **Wrong exchange.** Line L8 needs both exchanges, $A - i + j$ and $A' - j + i$, to be bases. A one-way exchange can make the other base dependent.
- **Upper tails of submodular functions.** Item 4 is a lower tail bound. Upper tails for submodular functions need other tools.

## Exercises

1. Show that one step of MERGE keeps $\beta \mathbf{1}_A + \beta' \mathbf{1}_{A'}$ unchanged in expectation, and that $|A \setminus A'|$ drops by 1.
2. For the uniform matroid of rank 1 on $\{1, 2, 3\}$ with $x = (\frac12, \frac13, \frac16)$, written as $\frac12 \{1\} + \frac13 \{2\} + \frac16 \{3\}$, run SWAP-ROUND and check that $\Pr[i \in R] = x_i$.
3. Prove the Chernoff upper tail $\Pr[X \ge (1 + \delta) \mu] \le \big( e^{\delta} / (1 + \delta)^{1 + \delta} \big)^{\mu}$ for $X = \sum_{i \in R} w_i$, using only item 2 of the theorem.
4. Give a bipartite graph and a point of its perfect matching polytope for which every distribution over perfect matchings with these marginals has two edges that are positively correlated.

## References
