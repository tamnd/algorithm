---
tag: K6B73V
kind: algorithm
slug: chekuri-khanna-ptas
name: Chekuri-Khanna PTAS for multiple knapsack
aliases:
- Chekuri-Khanna multiple knapsack PTAS
- Chekuri and Khanna approximation scheme
- PTAS for the multiple knapsack problem
area: approximation/approximation-schemes
level: advanced
summary: Polynomial-time approximation scheme for multiple knapsack, combining rounding with a structured assignment of large items.
solves: [multiple-knapsack-problem]
model: word-ram
complexity:
  vars: {n: the number of items, m: the number of knapsacks, ε: "the accuracy parameter, 0 < ε ≤ 1"}
  time: {worst: "n^O(log(1/ε)/ε^8)"}
  space: {extra: "n^O(log(1/ε)/ε^8)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2000
  people: [Chandra Chekuri, Sanjeev Khanna]
  note: Chekuri and Khanna gave the first PTAS for the multiple knapsack problem with arbitrary capacities at SODA 2000; the journal version appeared in the SIAM Journal on Computing.
prereqs: [multiple-knapsack-problem, ptas, rounding-and-scaling, lp-relaxation]
see_also: [multiple-knapsack-problem, generalized-assignment-problem, shmoys-tardos-gap, eptas, bin-packing-aptas, knapsack-fptas, no-fptas-for-strongly-np-hard-problems, ptas]
sources:
  - paper: doi:10.1137/S0097539700382820
    title: Chandra Chekuri and Sanjeev Khanna, A polynomial time approximation scheme for the multiple knapsack problem, SIAM Journal on Computing 35(3), 2005
    locator: pages 713 to 728; Section 2.2 (guessing items, Lemmas 2.2 to 2.6), Section 2.3 (packing items, Lemmas 2.8 to 2.11), Theorem 2.12
  - title: Chandra Chekuri and Sanjeev Khanna, A PTAS for the multiple knapsack problem, Proceedings of the 11th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 2000
    locator: pages 213 to 222 (the conference version)
  - paper: doi:10.1137/080731207
    title: Klaus Jansen, Parameterized approximation scheme for the multiple knapsack problem, SIAM Journal on Computing 39(4), 2010
    locator: pages 1392 to 1412 (the EPTAS, and the running time of the Chekuri and Khanna scheme as stated there)
  - title: David B. Shmoys and Éva Tardos, An approximation algorithm for the generalized assignment problem, Mathematical Programming 62, 1993
    locator: pages 461 to 474 (the rounding of the GAP linear program used in the packing step)
---

The Chekuri and Khanna PTAS is the first [polynomial-time approximation scheme](/ptas/) for the [multiple knapsack problem](/multiple-knapsack-problem/) with arbitrary capacities. For each fixed $\varepsilon > 0$ it finds, in polynomial time, a packing of profit at least $(1 - \varepsilon) \cdot \mathrm{OPT}$. It works in two steps. The guessing step lists a polynomial number of candidate item sets, and one of them fits in the knapsacks and has almost the optimal profit. The trick is to round the profits to $O(\varepsilon^{-1} \log n)$ classes and to describe a candidate by a short tuple of numbers with a bounded sum. The packing step then packs most of a candidate by guessing the large items and rounding a linear program of the [generalized assignment problem](/generalized-assignment-problem/). The time is $n^{O(\log(1/\varepsilon)/\varepsilon^8)}$, as Jansen states it, so the scheme is not efficient; Jansen (2010) later gave an [EPTAS](/eptas/). The problem has no FPTAS unless P = NP, so a PTAS is the right kind of result.

## In plain words

You have several bags of different sizes and many items, each with a weight and a value. You want the most value that fits. Trying every set of items is too slow. This method makes a short list of sets to try, and shows that one set on the list fits and is almost as good as the best.

To make the list short, it first guesses the best total value roughly, drops the items that are worth very little, and rounds each value down to one of a few levels. Items on the same level are worth the same, so for each level only the count matters, and it is best to take the lightest items of that level. A list of counts with a small total then describes a whole set. In the paper, a second step packs the chosen set into the bags almost completely.

## The problem

The input is $n$ items with positive integer sizes $s_i$ and profits $p_i$, $m$ knapsacks with positive integer capacities $c_1, \ldots, c_m$, and an accuracy parameter $0 < \varepsilon \le 1$. A packing puts disjoint sets of items into the knapsacks with no knapsack over its capacity. The task is a packing with

$$
p(\text{packing}) \ge (1 - \varepsilon) \cdot \mathrm{OPT},
$$

where $\mathrm{OPT}$ is the largest profit of a packing. This is a maximization problem, so the ratio is written as $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha = 1 - \varepsilon$. The guarantee holds on each instance. With $p_{\max}$ the largest profit of an item that fits in some knapsack, $p_{\max} \le \mathrm{OPT} \le n \, p_{\max}$.

## The algorithm

```pseudo id=main
CHEKURI-KHANNA(s[1 .. n], p[1 .. n], c[1 .. m], ε)        ▷ 0 < ε ≤ 1
L1  remove the items that fit in no knapsack; n ← the number left; best ← the empty packing
L2  δ ← ε/3; J ← the least integer with (1 + δ)^J ≥ n
L3  for j ← 0 to J do O ← p_max·(1 + δ)^j                  ▷ guess the optimum
L4      T ← the items with p_i ≥ δO/n
L5      for i ∈ T do e_i ← ⌊log_{1+δ}(p_i·n/(δO))⌋; a_i ← (δO/n)·(1 + δ)^{e_i}
L6      split T into classes S_1, ..., S_h by e_i; sort each class by size, smallest first
L7      g ← δ²O/h; D ← ⌊(1 + δ)·h/δ²⌋
L8      for each tuple (k_1, ..., k_h) of integers k_r ≥ 0 with k_1 + ... + k_h ≤ D do
L9          U ← the union over r of the ⌈k_r·g/a_r⌉ smallest items of S_r      ▷ skip if S_r is too small
L10         if p(U) > p(best) then P ← PACK(U); if P ≠ fail then best ← P
L11 return best
```

Lines L1 to L3 guess the optimum on a geometric grid. One guess $O$ has $O \le \mathrm{OPT} < (1 + \delta) O$, and there are $J + 1 = O(\delta^{-1} \log n)$ guesses. Lines L4 and L5 are the rounding of Lemma 2.2 of the paper: items of profit below $\delta O / n$ are dropped, which loses less than $\delta O$ in total, and each other profit is rounded down to a power of $1 + \delta$ times $\delta O / n$, which loses a factor below $1 + \delta$. After this there are only $h = O(\delta^{-1} \log(n / \delta))$ distinct profits.

Line L6 groups the items by rounded profit. Within a class all items are worth the same, so a good set should use the smallest items of the class. Lines L7 to L9 are the guessing of Lemma 2.3: the number $k_r$ is the profit taken from class $r$ in units of $g = \delta^2 O / h$, and the tuple fixes the whole set. The bound $k_1 + \cdots + k_h \le D$ holds for the tuple of an optimal set, because the profits of the classes add up to less than $(1 + \delta) O$. This bound is what makes the list short: there are at most $\binom{D + h}{h} = (n/\delta)^{O(\log(1/\delta)/\delta)}$ tuples, while the $h$ numbers $k_r$ taken independently would give a count that is not polynomial in $n$.

Line L10 calls the packing step PACK on a candidate set $U$.

- **In the paper,** PACK runs in polynomial time for a fixed $\varepsilon$ and, when $U$ fits, returns a packing of a subset of $U$ of profit at least $(1 - O(\varepsilon))\,p(U)$. It first rounds the sizes in each class to $O(\varepsilon^{-2} \log n)$ values, groups the knapsacks into blocks of similar capacity, and keeps a bounded number of the blocks that have few knapsacks. Then it guesses the most profitable items of each knapsack in those blocks, and the number of large items of each size in each block with many knapsacks. It packs the large items with a few extra knapsacks, assigns the other items by the LP of the generalized assignment problem rounded by the method of [Shmoys and Tardos](/shmoys-tardos-gap/), and repairs the result by dropping one item per knapsack or the least profitable knapsacks of a block. The [proof](#correctness) sketches it.
- **In the code on this page,** PACK is an exact search that packs all of $U$ or reports that $U$ does not fit. This keeps the guessing step exact and testable, but the search is exponential in $|U|$, so the code is for small instances.

The code lists each distinct vector of counts $c_r = \lceil k_r g / a_r \rceil$ once, by taking the least $k_r$ for each count. This gives the same sets as line L8 with fewer repeats. The rule "take the smallest $c_r$ items" is a slight simplification of the paper, which uses two rules, one for classes of small profit and one for classes of large profit. The bound $(1 - 2\delta - \delta^2)\,\mathrm{OPT}$ is proved for this rule.

## Example

Two knapsacks with capacities 10 and 6, and five items (the instance of the [multiple knapsack problem](/multiple-knapsack-problem/) page):

| item | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| size | 6 | 5 | 5 | 4 | 3 |
| profit | 9 | 7 | 7 | 6 | 3 |

The optimum is 23, with items 2 and 3 in the first knapsack and item 1 in the second. Take $\varepsilon = 1$, so $\delta = 1/3$. Then $p_{\max} = 9$ and $J = 6$, because $(4/3)^5 \approx 4.21 < 5 \le (4/3)^6 \approx 5.62$. So there are 7 guesses. The guess with $O \le 23 < \frac{4}{3} O$ is $j = 3$, $O = 9 \cdot (4/3)^3 = 64/3 \approx 21.33$.

- **Rounding (lines L4 and L5).** The unit is $\delta O / n = 64/45 \approx 1.42$, and no item is below it. The rounded profits are $a = (64/45)(4/3)^e$: item 5 gets $e = 2$ and $a \approx 2.53$, items 2, 3 and 4 get $e = 5$ and $a \approx 5.99$, and item 1 gets $e = 6$ and $a \approx 7.99$.
- **Classes (line L6).** $S_1 = (5)$, $S_2 = (4, 2, 3)$ by size $4, 5, 5$, and $S_3 = (1)$. So $h = 3$.
- **Tuples (lines L7 to L9).** $g = \delta^2 O / h = 64/81 \approx 0.79$ and $D = \lfloor (4/3) \cdot 3 \cdot 9 \rfloor = 36$. There are $\binom{39}{3} = 9139$ tuples, but they give only $2 \cdot 4 \cdot 2 = 16$ distinct sets, since $S_2$ can give 0 to 3 items and the other classes 0 or 1.
- **Packing (line L10).** Of the 16 sets, the 4 sets $\{1,2,3,4\}$, $\{1,2,3,4,5\}$, $\{1,2,4,5\}$ and $\{2,3,4,5\}$ do not fit. The best set that fits is $\{1, 2, 4\}$ with profit 22: items 1 and 4 in the first knapsack ($6 + 4 = 10$) and item 2 in the second.

The run returns 22. The optimal set $\{1, 2, 3\}$ is not a candidate: it takes two items of $S_2$ but not item 4, the smallest one. The loss is within the bound: $22 \ge (1 - 2\delta - \delta^2) \cdot 23 = \frac{2}{9} \cdot 23$. With $\varepsilon = 1/2$, so $\delta = 1/6$, the right guess is $O = 9 \cdot (7/6)^6 \approx 22.69$. Then item 4 gets a lower class than items 2 and 3, the set $\{1, 2, 3\}$ becomes one of 24 candidates, and the run returns 23.

## Correctness

The full argument is in the [proof](proofs/correctness.md); the part on the packing step of the paper is a sketch. The main steps for the guessing step are these. Fix the guess $O$ with $O \le \mathrm{OPT} < (1 + \delta) O$ and an optimal set $U^*$. Let $U'$ be $U^*$ without the dropped items; then $p(U') \ge (1 - \delta)\,\mathrm{OPT}$, and its rounded profit is $a(U') > p(U')/(1 + \delta)$. Let $u_r$ be the number of items of $U'$ in class $r$, and $k_r = \lfloor u_r a_r / g \rfloor$. Then $\sum_r k_r \le D$, so line L8 meets this tuple, and the count $c_r = \lceil k_r g / a_r \rceil$ is at most $u_r$.

The set $U$ of the $c_r$ smallest items of each class fits: in the packing of $U'$, each item of class $r$ that $U$ needs can take the place of an item of $U'$ of the same class that is at least as large. Its rounded profit is $\sum_r c_r a_r \ge \sum_r k_r g > a(U') - h g = a(U') - \delta^2 O$. Together,

$$
\mathrm{ALG} \ge p(U) \ge \frac{1 - \delta}{1 + \delta}\,\mathrm{OPT} - \delta^2\,\mathrm{OPT} \ge (1 - 2\delta - \delta^2)\,\mathrm{OPT} \ge (1 - \varepsilon)\,\mathrm{OPT}
$$

with $\delta = \varepsilon / 3$. The tests check this bound against brute force on random instances for $\varepsilon = 1, 1/2, 1/3$, and they check for the right guess that some candidate fits and reaches the bound.

## Complexity

- **Guesses.** $J + 1 \le 2 + 2 \ln n / \delta$ values of $O$.
- **Candidates per guess.** At most $\binom{D + h}{h} \le (2e/\delta^2)^h$ with $h \le 1 + 2\ln(n/\delta)/\delta$, which is $(n/\delta)^{O(\log(1/\delta)/\delta)}$. The paper uses a cruder count and states $n^{O(1/\varepsilon^3)}$ candidate instances (Lemma 2.6). The tests check the bound $\binom{D + h}{h}$ for each guess.
- **The packing step of the paper.** Polynomial for a fixed $\varepsilon$; the guesses for the small blocks and for the large items dominate. Jansen gives the total time of the scheme as $n^{O(\log(1/\varepsilon)/\varepsilon^8)}$.
- **The code on this page.** Lines L1 to L9 are polynomial for a fixed $\varepsilon$, but the exact PACK is exponential in $|U|$ in the worst case.

So the scheme is a PTAS, with $\varepsilon$ in the exponent of $n$. It is not an EPTAS, and it cannot be an FPTAS unless P = NP, because the problem has [no FPTAS even for two knapsacks](/no-fptas-for-strongly-np-hard-problems/).

## Properties

- **Deterministic.** All guesses are made by trying every value.
- **Not exact.** It returns a packing of profit at least $(1 - \varepsilon)\,\mathrm{OPT}$, and the example shows that the bound can be met with a strict loss.
- **Arbitrary capacities.** The capacities may differ by any factor. For identical capacities a simpler scheme works (see below).
- **A reduction to few profits and sizes.** The guessing step turns an arbitrary instance into a polynomial number of instances with $O(\varepsilon^{-1} \log n)$ profits and $O(\varepsilon^{-2} \log n)$ sizes, one of which keeps almost all of the optimum. The paper calls this a PTAS-preserving reduction, and it is useful on its own.

## Variants and improvements

- **Identical capacities.** If all knapsacks have the same capacity and $m > 1/\varepsilon$, pack a guessed set with the [bin packing APTAS](/bin-packing-aptas/) into at most $(1 + \varepsilon) m + 1$ bins and keep the $m$ most profitable bins (Section 2.1 of the paper). If $m \le 1/\varepsilon$, the number of knapsacks is a constant, and a PTAS is known even for GAP. Kellerer (1999) gave a PTAS for identical capacities by another route.
- **Greedy.** Filling the knapsacks one after the other with the [knapsack FPTAS](/knapsack-fptas/) gives ratio $2 + \varepsilon$, and $(e - 1)/e - O(\varepsilon)$ for identical capacities (Claims 4.1 and 4.2 of the paper). It is much faster.
- **LP rounding.** The rounding of [Shmoys and Tardos](/shmoys-tardos-gap/) gives a 2-approximation for GAP, so also for MKP.
- **Efficient scheme.** Chekuri and Khanna asked whether an EPTAS exists. Jansen (2010) gave one, with time $2^{O(\log(1/\varepsilon)/\varepsilon^5)} \cdot \mathrm{poly}(n) + O(m)$.
- **Generalizations.** If the sizes or the profits may depend on the knapsack, the problem is GAP, which is APX-hard even in very restricted cases (Theorems 3.2 and 3.3 of the paper), so no PTAS of this kind exists for it unless P = NP.

## When to use it

Use it as the proof that MKP has a PTAS, and as a model of the guessing technique: round to few classes, describe a candidate by a tuple with a bounded sum, and count the tuples. The time bound is far too large for practice. For real instances use exact branch and bound, the greedy method, or LP rounding, and use Jansen's EPTAS when an approximation scheme with a better time bound is needed.

## Pitfalls

- **Guessing each count independently.** With $h = \Theta(\varepsilon^{-1} \log n)$ classes and up to $h/\varepsilon^2$ values for each $k_r$, the product of the ranges is about $(h/\varepsilon^2)^h$. Its exponent of $n$ grows with $\log \log n$, so it is not polynomial; the paper calls this count quasi-polynomial. The bound on the sum is what makes the count polynomial.
- **Taking any items of a class.** The exchange argument needs the smallest items of each class. A set with the right counts but larger items may not fit.
- **The guess grid.** The grid must start at $p_{\max}$ of the items that fit, not of all items. An item that fits nowhere can make $p_{\max} > \mathrm{OPT}$, and then no guess satisfies $O \le \mathrm{OPT}$.
- **Rounding up.** Rounding the profits up breaks the bound $p(U) \ge a(U)$ in the proof. Round down.
- **Expecting PACK to pack all of $U$.** Deciding whether a set fits is as hard as bin packing. The paper packs only a subset of $U$ of profit $(1 - O(\varepsilon))\,p(U)$, and the analysis must take this loss.
- **Floating point.** The class boundaries are powers of $1 + \delta$ times $\delta O / n$, and a rounding error can move an item to the wrong class. The code uses exact fractions.

## Implementations

## History

Chekuri and Khanna presented the scheme at SODA 2000, and the journal version appeared in the SIAM Journal on Computing. Before it, the best ratio known for MKP with arbitrary capacities was 2, from the 2-approximation for GAP that follows from the work of Shmoys and Tardos (1993). Kellerer had given a PTAS for identical capacities in 1999. The paper also showed that small generalizations of MKP toward GAP are APX-hard, so MKP is close to the boundary of the problems with a PTAS, and it asked for an efficient scheme. Jansen answered with an EPTAS in 2010.

## References
