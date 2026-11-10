---
tag: YWN3V4
kind: algorithm
slug: greedy-set-cover
name: Greedy set cover algorithm
aliases:
- Johnson-Lovasz-Stein greedy algorithm
- Chvatal greedy algorithm
- greedy set covering heuristic
area: approximation/covering-and-packing
level: intro
summary: Repeatedly pick the set of least cost per new element; the cover costs at most H_d times the optimum, where d is the largest set size.
solves: [set-cover]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of sets, s: the total size of all sets}
  time: {worst: O(n + s log m)}
  space: {extra: Θ(n + m + s)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1974
  people: [David S. Johnson, Sherman K. Stein, László Lovász, Vašek Chvátal]
  note: Johnson (1974), Stein (1974) and Lovász (1975) analysed the unit-cost greedy; Chvátal (1979) extended the H_d bound to arbitrary costs.
prereqs: [set-cover, greedy-algorithm, harmonic-series, weak-duality]
see_also: [set-cover-primal-dual, dual-fitting, greedy-max-coverage, set-cover-inapproximability, dominating-set, lp-rounding-set-cover]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 35, Section 35.3 (GREEDY-SET-COVER and its ratio H(max |S|))
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Section 1.6 (a greedy algorithm, analysed by dual fitting)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 2, Section 2.1 (the greedy algorithm and its tight example), and Chapter 13 (set cover via dual fitting)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 11, Section 11.3 (set cover, a general greedy heuristic)
  - paper: doi:10.1016/S0022-0000(74)80044-9
    title: David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9(3), 1974
    locator: pages 256 to 278
  - paper: doi:10.1016/0012-365X(75)90058-8
    title: László Lovász, On the ratio of optimal integral and fractional covers, Discrete Mathematics 13(4), 1975
    locator: pages 383 to 390
  - paper: doi:10.1287/moor.4.3.233
    title: Vašek Chvátal, A greedy heuristic for the set-covering problem, Mathematics of Operations Research 4(3), 1979
    locator: pages 233 to 235
  - title: Sherman K. Stein, Two combinatorial covering theorems, Journal of Combinatorial Theory, Series A 16(3), 1974
    locator: pages 391 to 397
  - title: Petr Slavík, A tight analysis of the greedy algorithm for set cover, Journal of Algorithms 25(2), 1997 (STOC 1996)
    locator: the main theorem, ln n − ln ln n + Θ(1) for unit costs
---

The greedy set cover algorithm solves the [set cover problem](/set-cover/) approximately: it repeatedly picks the set with the least cost per element that is not yet covered, until all elements are covered. Its cover costs at most $H_d \cdot$ OPT, where $d$ is the size of the largest set and $H_d = 1 + 1/2 + \cdots + 1/d \le \ln d + 1$ is the [harmonic number](/harmonic-series/). This ratio is tight for the algorithm, and up to lower-order terms it is the best ratio that any polynomial-time algorithm can have unless P = NP. The proof by [dual fitting](/dual-fitting/) given here is a model for many other greedy analyses.

## In plain words

You must cover a list of items with groups, and each group has a price. At each step, look at each group and divide its price by the number of items it would add that are still missing. Buy the group with the smallest value of this "price per new item". Stop when nothing is missing.

Each item pays its share of the group that first covered it. The proof shows that the items of any one group pay, all together, at most a small factor more than the price of that group. The factor is the sum one plus a half plus a third and so on, up to the size of the largest group. The best solution must buy groups that hold all the items, so the greedy total is at most this factor times the best total.

## The problem

The input is a universe $U$ of $n$ elements and $m$ sets $S_1, \ldots, S_m \subseteq U$ with costs $c_j \ge 0$, whose union is $U$. The output is a set $C$ of indices with $\bigcup_{j \in C} S_j = U$. The goal is a small cost $c(C) = \sum_{j \in C} c_j$. With unit costs, the goal is a cover with few sets. OPT is the least cost of a cover, LP* is the optimum of the LP relaxation, and $d = \max_j |S_j|$. The ratio convention is ALG $\le \rho \cdot$ OPT.

## The algorithm

```pseudo id=main
GREEDY-SET-COVER(U, S[1 .. m], c[1 .. m])
L1  R ← U, C ← empty list                    ▷ R holds the elements not yet covered
L2  while R ≠ ∅ do
L3      choose j with S[j] ∩ R ≠ ∅ that minimizes c[j] / |S[j] ∩ R|
L4      for each e in S[j] ∩ R do price(e) ← c[j] / |S[j] ∩ R|
L5      append j to C, R ← R \ S[j]
L6  return C
```

Line L3 picks the set that buys new elements at the lowest rate. With unit costs, this is the set that covers the most new elements. If no set meets $R$, the sets do not cover $U$, and the implementation reports an error. Line L4 is not needed for the output: it records the price of each element, which the analysis uses. Ties in line L3 may be broken in any way; the implementation takes the smallest index.

## Example

The instance has $U = \{1, \ldots, 7\}$ and five sets.

| set | elements | cost |
|---|---|---|
| $S_1$ | 1, 2, 3, 5 | 3 |
| $S_2$ | 3, 4, 6, 7 | 4 |
| $S_3$ | 2, 5, 6 | 4 |
| $S_4$ | 3, 7 | 2 |
| $S_5$ | 1, 2, 4, 7 | 1 |

The table shows the cost per new element $c_j / |S_j \cap R|$ of each set at each round. The word "none" means that the set holds no element of $R$.

| round | $R$ before | $S_1$ | $S_2$ | $S_3$ | $S_4$ | $S_5$ | pick | prices |
|---|---|---|---|---|---|---|---|---|
| 1 | 1, 2, 3, 4, 5, 6, 7 | 3/4 | 1 | 4/3 | 1 | 1/4 | $S_5$ | 1, 2, 4, 7 pay 1/4 |
| 2 | 3, 5, 6 | 3/2 | 2 | 2 | 2 | none | $S_1$ | 3, 5 pay 3/2 |
| 3 | 6 | none | 4 | 4 | none | none | $S_2$ | 6 pays 4 |

Greedy returns $C = (5, 1, 2)$ with cost $1 + 3 + 4 = 8$, which is the sum of the prices: $4 \cdot 1/4 + 2 \cdot 3/2 + 4 = 8$. The optimum is $\{S_1, S_2\}$ with cost 7, and LP* $= 6$. The largest set has $d = 4$, so the theorem promises a cost of at most $H_4 \cdot 6 = (25/12) \cdot 6 = 12.5$. The cheap first pick $S_5$ is the reason greedy loses: after it, element 6 can be covered only by a set of cost 4.

## Correctness

The loop stops after at most $\min(n, m)$ rounds, because each round removes at least one element from $R$, and then $R = \emptyset$, so $C$ is a cover. For the cost, the key fact is a bound on the prices inside one set $S$ with $s$ elements. List the elements of $S$ in the order in which they are covered. When the $i$-th of them is covered, at least $s - i + 1$ elements of $S$ are still uncovered, so $S$ itself offers the rate $c(S)/(s - i + 1)$ or better, and greedy pays at most this rate. So

$$\sum_{e \in S} \text{price}(e) \le c(S) \left( \frac{1}{s} + \frac{1}{s-1} + \cdots + 1 \right) = c(S) H_s.$$

**Theorem.** GREEDY-SET-COVER returns a cover of cost at most $H_d \cdot \text{LP}^* \le H_d \cdot \text{OPT}$, in the worst case.

The proof scales the prices: $y_e = \text{price}(e)/H_d$ is a feasible solution of the [dual LP](/dual-linear-program/), so by [weak duality](/weak-duality/) the cost $\sum_e \text{price}(e) = H_d \sum_e y_e$ is at most $H_d \cdot \text{LP}^*$. This is [dual fitting](/dual-fitting/): the algorithm does not build a dual, but its prices, scaled down, fit one. A second proof needs no LP: charge each element to one set of an optimal cover. With unit costs there is also the bound OPT$\,(\lceil \ln(n/\text{OPT}) \rceil + 1)$ on the number of sets. The full proofs are in the proof file below.

**The lower bound used.** The analysis compares ALG with a feasible dual solution, so with LP*, which is at most OPT. So the bound $H_d$ also bounds the integrality gap of the LP.

**Tight examples.** The ratio $H_d$ is tight for the algorithm.

- *Weighted.* Take $n$ elements, the singletons $\{e_i\}$ with cost $1/i$, and one set $U$ with cost $1 + \varepsilon$. While $i$ elements remain, the singleton $\{e_i\}$ costs $1/i$ per element and $U$ costs $(1 + \varepsilon)/i$. So greedy buys the singletons $\{e_n\}, \{e_{n-1}\}, \ldots, \{e_1\}$ and pays $H_n$, while OPT $= 1 + \varepsilon$. The ratio $H_n/(1 + \varepsilon)$ tends to $H_n$, and here $d = n$.
- *Unit costs.* For $k \ge 2$, put $2(2^k - 1)$ elements in two rows of $2^k - 1$ columns. The two rows are two sets, so OPT $= 2$. Split the columns into blocks of $1, 2, 4, \ldots, 2^{k-1}$ columns, and add one set for each block, with the elements of both rows in it. The largest block has $2^k$ elements, more than the $2^k - 1$ of a row, so greedy takes it first, and the same happens in each round. Greedy takes all $k$ blocks, for a ratio of $k/2$, which is about $0.72 \ln n$.

With unit costs, the exact worst-case ratio of greedy is $\ln n - \ln \ln n + \Theta(1)$ (Slavík 1997).

## Complexity

Let $s = \sum_j |S_j|$ be the total size of the input. The implementation keeps, for each set, the count $|S_j \cap R|$, and for each element the list of sets that contain it. When an element leaves $R$, it decreases the count of each of its sets, so all count updates cost $O(s)$ in total.

- **Time.** A min-heap holds a key $c_j / |S_j \cap R|$ for each set. A key can only grow while $R$ shrinks, so the heap can be lazy: pop the top, and if its key is out of date, push the new key and pop again. Each push follows a decrease of some count, so there are at most $s + m$ pushes and pops, each in $O(\log m)$ time. The total is $O(n + s \log m)$ in the worst case, in the [word RAM](/word-ram/) with costs that fit in a word, where two ratios are compared by cross-multiplication.
- **Simple version.** Recompute all ratios in each round: $O(s)$ per round and at most $\min(n, m)$ rounds, so $O(s \min(n, m))$.
- **Unit costs.** Buckets indexed by the count replace the heap, and the time is $O(n + m + s)$ (CLRS asks for this in the exercises of Section 35.3).
- **Space.** The counts, the element lists and the heap take $\Theta(n + m + s)$ extra space.

## Properties

- **Deterministic.** With a fixed tie rule, the output depends only on the input.
- **Any tie rule.** A different tie rule can change the cover and its cost, but the bound $H_d$ holds for each tie rule, because Lemma 3 of the proof uses only that the chosen ratio is a least one.
- **Output may be redundant.** A set picked early can become unnecessary after later picks. A final pass that drops redundant sets never hurts, but it does not improve the worst-case ratio.
- **Anytime.** After $t$ rounds with unit costs, the chosen sets cover at least a $1 - (1 - 1/\text{OPT})^t$ fraction of the elements. This is the analysis of [greedy maximum coverage](/greedy-max-coverage/).

## Variants and improvements

- **Greedy maximum coverage.** Stop after $k$ picks. The [greedy maximum coverage](/greedy-max-coverage/) algorithm covers at least $1 - 1/e$ of what the best $k$ sets cover.
- **Lazy greedy.** The lazy heap above is the "lazy evaluation" trick of Minoux (1978) for submodular functions. It saves much time in practice.
- **Dominating set.** Run greedy on the closed neighbourhoods of a graph. This gives the $\ln(\Delta + 1) + 1$ ratio of [dominating set](/dominating-set/).
- **Bounded set size.** For sets of size at most $d$, local search and semi-local improvements reach ratios below $H_d$, for example $H_d - 1/2$ (Duh and Fürer 1997).
- **LP-based algorithms.** [LP rounding](/lp-rounding-set-cover/) and the [primal-dual method](/set-cover-primal-dual/) give ratio $f$, the largest [element frequency](/element-frequency/). This is better than $H_d$ when each element is in few sets, as in [vertex cover](/vertex-cover/).

## When to use it

Use greedy when you need a fast and simple method with a guarantee, and the sets are large or elements are in many sets. Its ratio $\ln n + 1$ is the best possible in the worst case, up to lower-order terms, and on many instances it does much better than its worst case. Use the [primal-dual](/set-cover-primal-dual/) or [rounding](/frequency-rounding-set-cover/) $f$-approximation when the [element frequency](/element-frequency/) $f$ is small, for example $f = 2$ for vertex cover, where greedy can be worse by a factor of $\Theta(\log n)$. When the instance is small, or an exact cover is needed, use integer programming; greedy then gives a good first solution and an upper bound.

## Pitfalls

- **Ignoring the costs in line L3.** Picking the set with the most new elements, $\max |S_j \cap R|$, is correct only for unit costs. With costs, it has no bounded ratio: one huge, very expensive set wins. Use $\min c_j / |S_j \cap R|$.
- **Using $|S_j|$ instead of $|S_j \cap R|$.** The ratio must count only the elements not yet covered. With $c_j / |S_j|$, the algorithm is a fixed order and can pick sets that add nothing.
- **Dividing by zero.** A set with $S_j \cap R = \emptyset$ has no defined ratio. Skip it in line L3; it must not be picked.
- **Floating-point ties.** Comparing $c_j / k$ in floating point can break exact ties in an unexpected way. Compare $c_i \cdot k_j$ with $c_j \cdot k_i$ instead.
- **Reading the ratio as $H_m$ or $H_{\text{OPT}}$.** The bound is $H_d$ with $d$ the largest set size, which is at most $H_n$. It does not depend on the number of sets.

## Implementations

## History

Johnson (1974) proved the ratio $H_d$ for the unit-cost greedy algorithm, and Stein (1974) and Lovász (1975) found the same bound in the language of hypergraph covers; Lovász stated it as a bound on the ratio of integral and fractional covers. Chvátal (1979) extended it to arbitrary costs, with the price argument used here. The dual-fitting form of the proof is presented in Vazirani's book and in Williamson and Shmoys. Slavík (1996) found the exact unit-cost ratio. Feige (1998) showed that $(1 - \varepsilon)\ln n$ is not possible unless NP has slightly superpolynomial algorithms, and Dinur and Steurer (2014) proved it under P $\ne$ NP; see [set cover inapproximability](/set-cover-inapproximability/).

## References
