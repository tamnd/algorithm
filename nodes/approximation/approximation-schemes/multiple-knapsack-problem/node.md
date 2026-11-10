---
tag: E57TZQ
kind: problem
slug: multiple-knapsack-problem
name: Multiple knapsack problem
aliases:
- multiple knapsack
- MKP
- 0-1 multiple knapsack problem
- multiple knapsack with identical capacities
area: approximation/approximation-schemes
level: advanced
summary: Pack items into several knapsacks with individual capacities to maximize total profit.
prereqs: [knapsack-problem, bin-packing, strong-np-hardness]
see_also: [chekuri-khanna-ptas, generalized-assignment-problem, shmoys-tardos-gap, knapsack-fptas, no-fptas-for-strongly-np-hard-problems, eptas, bin-packing-aptas, partition-problem]
sources:
  - paper: doi:10.1137/S0097539700382820
    title: Chandra Chekuri and Sanjeev Khanna, A polynomial time approximation scheme for the multiple knapsack problem, SIAM Journal on Computing 35(3), 2005
    locator: pages 713 to 728; Proposition 2.1 (no FPTAS for two bins), Section 2.1 (identical capacities), Theorem 2.12 (the PTAS), Theorems 3.2 and 3.3 (APX-hard cases of GAP), Proposition 3.6 (the 2-approximation), Claims 4.1 and 4.2 (greedy)
  - paper: doi:10.1137/080731207
    title: Klaus Jansen, Parameterized approximation scheme for the multiple knapsack problem, SIAM Journal on Computing 39(4), 2010
    locator: pages 1392 to 1412 (the EPTAS)
  - book: isbn:9780471924203
    title: Silvano Martello and Paolo Toth, Knapsack Problems, Algorithms and Computer Implementations, Wiley, 1990
    locator: Chapter 6 (the 0-1 multiple knapsack problem)
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the chapter on the multiple knapsack problem
  - title: Hans Kellerer, A polynomial time approximation scheme for the multiple knapsack problem, Proceedings of RANDOM-APPROX 1999, Lecture Notes in Computer Science 1671
    locator: the PTAS for identical capacities
---

The multiple knapsack problem (MKP) gives $n$ items, each with a size and a profit, and $m$ knapsacks (bins), each with its own capacity. It asks for a set of items of largest total profit that can be packed into the knapsacks with no knapsack over its capacity. With one knapsack it is the [0/1 knapsack problem](/knapsack-problem/), and its decision form contains [bin packing](/bin-packing/), so it is [strongly NP-hard](/strong-np-hardness/). It is the special case of the [generalized assignment problem](/generalized-assignment-problem/) in which the size and the profit of an item do not depend on the knapsack. For approximation it sits at an exact boundary: it has no FPTAS, even with two knapsacks, but it has a PTAS, the [Chekuri and Khanna PTAS](/chekuri-khanna-ptas/), and even an EPTAS (Jansen 2010), while small generalizations toward GAP are APX-hard.

## In plain words

You have several bags, and each bag can hold a different weight. In front of you are items, each with a weight and a value. You put each item into one bag or leave it out. No bag may be over its limit. You want the largest total value.

With one bag this is the usual knapsack problem, which is easy when the weights are small numbers. With many bags it is also a packing puzzle like bin packing, and it stays hard even with small numbers. Even with two bags of the same size, no method can get as close to the best as you like at a cost that grows only polynomially with the accuracy, unless P = NP. But for each fixed accuracy there is a polynomial method.

## Definition

**Input.** A set of $n$ items. Item $i$ has a size $s_i \in \mathbb{Z}_{>0}$ and a profit $p_i \in \mathbb{Z}_{>0}$. A set of $m$ knapsacks. Knapsack $j$ has a capacity $c_j \in \mathbb{Z}_{>0}$.

**Output.** Disjoint sets $S_1, \ldots, S_m$ of items with $\sum_{i \in S_j} s_i \le c_j$ for each $j$, that maximize $\sum_{j} \sum_{i \in S_j} p_i$. As an integer program:

$$
\max \sum_{i=1}^{n} \sum_{j=1}^{m} p_i x_{ij} \quad \text{subject to} \quad \sum_{i} s_i x_{ij} \le c_j \ (\text{each } j), \qquad \sum_{j} x_{ij} \le 1 \ (\text{each } i), \qquad x \in \{0, 1\}^{n \times m}.
$$

The empty packing is feasible, so an optimum always exists. Write $\mathrm{OPT}$ for its value and $p_{\max} = \max_i p_i$. Items that fit in no knapsack can be removed first, and then $p_{\max} \le \mathrm{OPT} \le n \, p_{\max}$.

**Decision version.** Given also a target $K$, is there a packing of profit at least $K$? It is NP-complete in the strong sense when $m$ is part of the input.

## Variants

- **One knapsack** ($m = 1$). The [0/1 knapsack problem](/knapsack-problem/), which is weakly NP-hard and has an [FPTAS](/knapsack-fptas/).
- **A fixed number of knapsacks.** With $m$ a constant, a dynamic program over the vector of loads runs in $O(n \prod_j c_j)$ time, which is pseudo-polynomial, so the problem is weakly NP-hard. It still has no FPTAS for $m = 2$ (see Bounds).
- **Identical capacities.** All $c_j$ are equal. Kellerer (1999) gave a PTAS for this case, and Chekuri and Khanna note that their guessing step together with the [bin packing APTAS](/bin-packing-aptas/) also gives one.
- **Multiple subset sum.** $p_i = s_i$ for each item, so the goal is to fill the knapsacks as much as possible.
- **Unit profits.** $p_i = 1$, so the goal is to pack as many items as possible. Then $\mathrm{OPT} \le n$, and an optimal set can be taken to be the $k$ smallest items for some $k$, so only the packing question is hard.
- **Generalized assignment.** In the [generalized assignment problem](/generalized-assignment-problem/) (GAP), item $i$ has a size $s_{ij}$ and a profit $p_{ij}$ that depend on the knapsack $j$. MKP is the case where neither depends on $j$.
- **Not to be confused with the multidimensional knapsack problem**, which has one knapsack and several resource constraints, $\sum_i a_{ki} x_i \le b_k$ for each $k$.

## Examples

**A small instance.** Two knapsacks with capacities $c_1 = 10$ and $c_2 = 6$, and five items:

| item | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| size $s_i$ | 6 | 5 | 5 | 4 | 3 |
| profit $p_i$ | 9 | 7 | 7 | 6 | 3 |

The optimum is 23: items 2 and 3 fill knapsack 1 (size 10, profit 14), and item 1 fills knapsack 2 (size 6, profit 9). A brute-force search over all $3^5$ assignments confirms it. The linear relaxation, which may split items, has value $117/5 = 23.4$.

**Greedy, one knapsack at a time.** Fill the knapsacks one after the other, each time with an optimal single-knapsack solution on the items that are left. If knapsack 1 goes first, it takes items 1 and 4 (size 10, profit 15, the best single-knapsack value). Then knapsack 2 can take only one of items 2 and 3, and the total is $15 + 7 = 22 < 23$. If knapsack 2 goes first, the greedy method finds 23. So the greedy method depends on the order of the knapsacks, and a choice that is best for one knapsack can be wrong for the whole packing.

**The worst case of greedy.** Two items of profit 1 with sizes 1 and $\alpha < 1$, and two knapsacks with capacities 1 and $\alpha$. If the greedy method fills the large knapsack first and picks the small item, the total is 1, and the optimum is 2. This is the example of Chekuri and Khanna that shows that their bound of $2 + \varepsilon$ for greedy is tight.

**Two knapsacks and partition.** For the numbers $3, 1, 1, 2, 2, 1$ with sum 10, make two knapsacks of capacity 5 and six items of profit 1 with these sizes. All six items fit ($3 + 2 = 5$ and $1 + 1 + 2 + 1 = 5$), so $\mathrm{OPT} = 6$. For the numbers $3, 3, 3, 1$, no subset sums to 5, so at most 3 of the 4 items fit and $\mathrm{OPT} = 3$. This is the reduction of the bound below.

## Known algorithms

| algorithm | guarantee | time | source |
|---|---|---|---|
| dynamic program over the loads | exact | $O(n \prod_j c_j)$ | standard |
| branch and bound with relaxations | exact, for practice | exponential in the worst case | Martello and Toth, Chapter 6 |
| greedy with the [knapsack FPTAS](/knapsack-fptas/) on each knapsack | $\mathrm{ALG} \ge \mathrm{OPT} / (2 + \varepsilon)$ | polynomial in $n$, $m$ and $1/\varepsilon$ | Chekuri and Khanna, Claim 4.2 |
| the same greedy, identical capacities | $\mathrm{ALG} \ge ((e - 1)/e - O(\varepsilon))\,\mathrm{OPT}$ | the same | Chekuri and Khanna, Claim 4.1 |
| LP rounding of [Shmoys and Tardos](/shmoys-tardos-gap/) | $\mathrm{ALG} \ge \mathrm{OPT}/2$, also for GAP | polynomial | Chekuri and Khanna, Proposition 3.6 |
| PTAS for identical capacities | $(1 - \varepsilon)\,\mathrm{OPT}$ | polynomial for each fixed $\varepsilon$ | Kellerer 1999 |
| the [Chekuri and Khanna PTAS](/chekuri-khanna-ptas/) | $(1 - \varepsilon)\,\mathrm{OPT}$ | $n^{O(\log(1/\varepsilon)/\varepsilon^8)}$, as stated by Jansen | Chekuri and Khanna 2000 |
| the Jansen EPTAS | $(1 - \varepsilon)\,\mathrm{OPT}$ | $2^{O(\log(1/\varepsilon)/\varepsilon^5)} \cdot \mathrm{poly}(n) + O(m)$ | Jansen 2010 |

The greedy bound is short to prove. Fix an optimal packing, and let $X_j$ be the items that it puts in knapsack $j$ and that the greedy method does not pack anywhere. When the greedy method fills knapsack $j$, all of $X_j$ is still available and fits, so the greedy method gets at least $(1 - \varepsilon) p(X_j)$ there. If $\sum_j p(X_j) \ge \mathrm{OPT}/2$, the greedy total is at least $(1 - \varepsilon)\mathrm{OPT}/2$. Otherwise more than half of the optimal profit is in items that the greedy method packs, and again the greedy total is at least $\mathrm{OPT}/2$.

The PTAS of Chekuri and Khanna was the first scheme for arbitrary capacities. It guesses a set of items of profit at least $(1 - O(\varepsilon))\mathrm{OPT}$ among $n^{O(1/\varepsilon^3)}$ candidate sets, with $O(\varepsilon^{-1} \log n)$ distinct profits and $O(\varepsilon^{-2} \log n)$ distinct sizes, and then packs most of the chosen set by guessing the large items and rounding an LP. The details are on its [own page](/chekuri-khanna-ptas/).

## Bounds

**Strong NP-hardness.** Given a bin packing instance with $n$ items and $m$ bins of capacity $B$, make an MKP instance with the same sizes, $m$ knapsacks of capacity $B$ and unit profits. All items fit in $m$ bins exactly when $\mathrm{OPT} = n$. Bin packing is NP-complete in the strong sense, by the reduction from [3-partition](/three-partition/), so MKP with $m$ in the input is NP-hard in the strong sense. By the [Garey and Johnson theorem](/no-fptas-for-strongly-np-hard-problems/), it has no FPTAS unless P = NP.

**No FPTAS even for two identical knapsacks** (Chekuri and Khanna, Proposition 2.1). If MKP with two knapsacks of equal capacity has an FPTAS, then P = NP.

*Proof.* Let $a_1, \ldots, a_k$ be an instance of [partition](/partition-problem/), with an even sum $2A$. Make $k$ items with sizes $a_1, \ldots, a_k$ and profit 1, and two knapsacks of capacity $A$. If the numbers split into two sets of sum $A$, all items fit and $\mathrm{OPT} = k$. Otherwise some item is left out in each packing, and $\mathrm{OPT} \le k - 1$. Run the FPTAS with $\varepsilon = 1/(k + 1)$. Its value satisfies $\mathrm{ALG} \ge (1 - \varepsilon)\mathrm{OPT}$, so if $\mathrm{OPT} = k$ then $\mathrm{ALG} \ge k - k/(k+1) > k - 1$, and $\mathrm{ALG} = k$ because it is an integer. If $\mathrm{OPT} \le k - 1$, then $\mathrm{ALG} \le k - 1$. So the answer to partition is yes exactly when $\mathrm{ALG} = k$. The time is polynomial in the input length and $k + 1$, so partition, which is NP-complete, is solved in polynomial time. $\square$

The proof is the second corollary of the Garey and Johnson theorem: the unit-profit problem has $\mathrm{OPT} \le n$. It also shows that the converse of that theorem fails, because MKP with two knapsacks has the pseudo-polynomial dynamic program above and still no FPTAS.

**Approximation schemes.** MKP has a PTAS (Chekuri and Khanna) and an EPTAS (Jansen 2010). So it is in EPTAS and not in FPTAS unless P = NP, and it separates the two classes. See [EPTAS](/eptas/).

**The LP relaxation.** Chekuri and Khanna observe that the natural LP relaxation has integrality gap 2, even with identical capacities. For example, take $m$ knapsacks of capacity 2 and $2m$ items of size $1 + \delta$ and profit 1, with $0 < \delta < 1$. Each knapsack holds only one item, so $\mathrm{OPT} = m$. But the LP can fill the total capacity $2m$ with fractions of items, and its value is $2m / (1 + \delta)$, which tends to $2m$ as $\delta \to 0$.

## Reductions

- **From partition**, to MKP with two knapsacks and unit profits: no FPTAS (above).
- **From bin packing and 3-partition**, to MKP with unit profits: strong NP-hardness (above).
- **To GAP.** Each MKP instance is a GAP instance with $s_{ij} = s_i$ and $p_{ij} = p_i$. So the [Shmoys and Tardos rounding](/shmoys-tardos-gap/) gives a 2-approximation for MKP.
- **GAP is APX-hard near MKP** (Chekuri and Khanna, Theorems 3.2 and 3.3). By a reduction from maximum [3-dimensional matching](/three-dimensional-matching/) with each element in at most 3 triples, GAP is APX-hard when all profits are 1, all capacities are 3 and each size $s_{ij}$ is 1 or $1 + \delta$; and also when each item has one size in $\{1, 3\}$ for all bins, all capacities are equal and each item has two possible profits. So letting either the sizes or the profits depend on the knapsack loses the PTAS, unless P = NP. If only the profits depend on the knapsack and all sizes are equal, GAP is a matching problem and can be solved in polynomial time (Proposition 3.4).

## Applications

- **Loading.** Loading goods into containers, trucks or ships of different capacities, to carry the most value. Operations research calls MKP the loading problem.
- **Storage.** Placing files or data blocks of known sizes onto disks or servers of different capacities, to keep the most valuable data.
- **Task allocation.** Assigning tasks to processors, each with a memory or time budget, when not all tasks can be run.

## References
