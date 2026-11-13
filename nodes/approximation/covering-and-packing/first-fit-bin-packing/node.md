---
tag: 2VPCK0
kind: algorithm
slug: first-fit-bin-packing
name: First-fit bin packing
aliases:
- first fit
area: approximation/covering-and-packing
level: intro
summary: Place each item in the lowest-index bin where it fits; at most 1.7 OPT bins, rounded down.
solves: [bin-packing]
model: real-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1974
  people: [Jeffrey D. Ullman, Michael R. Garey, Ronald L. Graham, David S. Johnson, Andrew C. Yao, György Dósa, Jiří Sgall]
  note: Ullman (1971) proved 1.7 OPT + 3, Garey, Graham, Johnson and Yao (1976) proved the ceiling of 1.7 OPT, and Dósa and Sgall (2013) proved the floor of 1.7 OPT.
prereqs: [bin-packing, bin-packing-lower-bound, next-fit-bin-packing, approximation-ratio]
see_also: [best-fit-bin-packing, first-fit-decreasing, next-fit-bin-packing, online-algorithm, first-fit-allocation, bin-packing-aptas]
sources:
  - paper: doi:10.4230/LIPIcs.STACS.2013.538
    title: "György Dósa and Jiří Sgall, First Fit bin packing: a tight analysis, STACS 2013, LIPIcs 20"
    locator: pp. 538-549, the main theorem (FF is at most the floor of 1.7 OPT) and the lower bound constructions
  - paper: "M. R. Garey, R. L. Graham, D. S. Johnson and A. C.-C. Yao, Resource constrained scheduling as generalized bin packing, Journal of Combinatorial Theory, Series A 21, 1976, pp. 257-298"
    title: Garey, Graham, Johnson and Yao 1976
    locator: the bound FF at most the ceiling of 1.7 OPT
  - paper: "D. S. Johnson, A. Demers, J. D. Ullman, M. R. Garey and R. L. Graham, Worst-case performance bounds for simple one-dimensional packing algorithms, SIAM Journal on Computing 3, 1974"
    title: Johnson, Demers, Ullman, Garey and Graham 1974
    locator: the weight function proof of 1.7 and the lower bound lists for first fit
  - paper: "D. S. Johnson, Fast algorithms for bin packing, Journal of Computer and System Sciences 8, 1974, pp. 272-314"
    title: Johnson 1974
    locator: the O(n log n) implementation of first fit with a tree
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 2, E. G. Coffman, M. R. Garey and D. S. Johnson, Approximation algorithms for bin packing, a survey (first fit)
---

First fit is the classic online algorithm for [bin packing](/bin-packing/): it keeps all bins open in the order in which they were opened, and it puts each item into the first bin with enough room, opening a new bin only if no bin has room. It uses at most $\lfloor 1.7\,\mathrm{OPT} \rfloor$ bins on every list (Dósa and Sgall 2013), and the factor 1.7 is the best possible for first fit. With a tree over the free space of the bins it runs in $O(n \log n)$ time. This page proves the bound $\mathrm{FF} < 1.7\,\mathrm{OPT} + 2.9$ in full with the classic weight function and states the absolute bound.

## In plain words

You keep a row of boxes. When an object comes, you walk along the row from the start and put the object into the first box where it fits. If no box in the row has room, you put a new box at the end of the row.

Unlike next fit, an old box can still receive a small object later, so less space is wasted. Big objects, more than half a box, always need their own boxes, and a careful count shows that first fit never uses much more than 1.7 times the best number of boxes. There are inputs where it uses that many.

## The problem

The input is a list of sizes $s_1, \ldots, s_n$ with $0 < s_i \le 1$, in the order of arrival. The output is a partition into bins with load at most 1, and the goal is few bins. This is the [bin packing problem](/bin-packing/). We write $S = \sum_i s_i$, $\mathrm{OPT}$ for the least number of bins, and $\mathrm{FF}$ for the number of bins of first fit.

*Ratio convention.* The bound $\mathrm{FF} \le \lfloor 1.7\,\mathrm{OPT} \rfloor$ is an absolute bound: it holds for every list, with no additive term. The asymptotic ratio of first fit is also exactly 1.7. Each analysis compares with a [lower bound on OPT](/bin-packing-lower-bound/): the simple proof uses the size bound $\lceil S \rceil$, and the 1.7 proof uses a weighted size, at most $1.7$ per bin of an optimal packing.

## The algorithm

```pseudo id=main
FIRST-FIT(s[1 .. n])
L1  k ← 0                                   ▷ no bin is open yet
L2  for i ← 1 to n do
L3      j ← the least index in 1 .. k with load[j] + s[i] ≤ 1, or k + 1 if there is none
L4      if j = k + 1 then k ← k + 1, B[k] ← ∅, load[k] ← 0
L5      B[j] ← B[j] ∪ {i}, load[j] ← load[j] + s[i]
L6  return B[1 .. k]
```

A direct scan in line L3 costs $O(k)$ per item. A faster way keeps a complete binary tree with one leaf per possible bin, where each node stores the largest free space among the leaves below it, and bins that are not open have free space 1. Line L3 walks down from the root and goes left whenever the left child has free space at least $s_i$. Line L5 updates the leaf and its ancestors. Both steps take $O(\log n)$ time.

## Example

Run first fit on $L = (0.2, 0.5, 0.4, 0.7, 0.1, 0.3, 0.8)$, where $S = 3$ and $\mathrm{OPT} = 3$.

| item | size | loads before | choice | loads after |
|---|---|---|---|---|
| 1 | 0.2 | none | new $B_1$ | 0.2 |
| 2 | 0.5 | 0.2 | $B_1$ | 0.7 |
| 3 | 0.4 | 0.7 | new $B_2$ | 0.7, 0.4 |
| 4 | 0.7 | 0.7, 0.4 | new $B_3$ | 0.7, 0.4, 0.7 |
| 5 | 0.1 | 0.7, 0.4, 0.7 | $B_1$ | 0.8, 0.4, 0.7 |
| 6 | 0.3 | 0.8, 0.4, 0.7 | $B_2$ | 0.8, 0.7, 0.7 |
| 7 | 0.8 | 0.8, 0.7, 0.7 | new $B_4$ | 0.8, 0.7, 0.7, 0.8 |

First fit uses 4 bins: $[0.2\ 0.5\ 0.1]$, $[0.4\ 0.3]$, $[0.7]$, $[0.8]$. [Next fit](/next-fit-bin-packing/) uses 5 bins on the same list, and [first fit decreasing](/first-fit-decreasing/) uses 3. Item 5 goes back to $B_1$ and item 6 goes back to $B_2$, which next fit cannot do.

## Correctness

Line L3 always finds a bin with room, since a new bin has room for any item of size at most 1, so each bin has load at most 1. The analysis rests on one property: if item $i$ is in bin $B_j$ and $e < j$, then $s_i > 1 - \ell(B_e)$, where $\ell(B_e)$ is the final load of $B_e$. The reason is that $B_e$ was open when $i$ came, and first fit passed it.

*The factor 2.* From this property, at most one bin has load at most $\frac12$, and that bin together with any other bin holds more than 1. So $S > \mathrm{FF}/2$ when $\mathrm{FF} \ge 2$, and $\mathrm{FF} \le 2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$.

*The factor 1.7.* Give each item of size $a$ the weight $w(a) = \frac65 a + v(a)$, where the bonus $v(a)$ is 0 up to $\frac16$, grows linearly as $\frac35(a - \frac16)$ up to $\frac13$, is $\frac1{10}$ on $(\frac13, \frac12]$, and is $\frac25$ above $\frac12$. Two facts give the bound.

1. A set of items that fits into one bin has weight at most $\frac{17}{10}$. So the total weight $W$ is at most $1.7\,\mathrm{OPT}$.
2. Almost every bin of first fit has weight at least 1. The bins of weight less than 1 have loads less than $\frac56$, and their free space, read in the order of the bins, can only grow; a telescoping sum bounds their total deficit by $2.9$. So $W > \mathrm{FF} - 2.9$.

Together, $\mathrm{FF} < 1.7\,\mathrm{OPT} + 2.9$. The full proof is below.

*The absolute bound (sketch).* Dósa and Sgall (2013) refine the same weight function. They show that the total bonus of the bins of first fit is large enough to remove the additive term, and they get $\mathrm{FF} \le \lfloor 1.7\,\mathrm{OPT} \rfloor$ for every list. The proof is long, and this page does not repeat it.

## Complexity

- **Time.** With the tree of the algorithm section, each item costs $\Theta(\log n)$, so the time is $\Theta(n \log n)$, in the [real RAM](/real-ram/) model. The direct scan costs $\Theta(nk)$, which is $\Theta(n^2)$ when most items are larger than $\frac12$. Johnson (1974) gave the $O(n \log n)$ implementation.
- **Space.** $\Theta(n)$ for the loads and the tree, plus the output. First fit is not bounded space: all bins stay open.

## Properties

| claim | statement | status |
|---|---|---|
| simple bound | $\mathrm{FF} \le 2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$ | proved below |
| asymptotic bound | $\mathrm{FF} < 1.7\,\mathrm{OPT} + 2.9$ | proved below |
| absolute bound | $\mathrm{FF} \le \lfloor 1.7\,\mathrm{OPT} \rfloor$ | Dósa and Sgall 2013, cited |
| lower bound 5/3 | $\mathrm{FF} = \frac53\,\mathrm{OPT}$ on a simple family | proved below |
| lower bound 1.7 | lists with $\mathrm{FF} = \lfloor 1.7\,\mathrm{OPT} \rfloor$ for most values of $\mathrm{OPT}$, and $\mathrm{FF} \ge 1.7\,\mathrm{OPT} - c$ for all large $\mathrm{OPT}$ | Johnson et al. 1974, Dósa and Sgall 2013, cited |
| online | yes; each item is placed before the next item is seen | by definition |

*A family with ratio 5/3.* Take $6m$ items of size $\frac17 + \varepsilon$, then $6m$ items of size $\frac13 + \varepsilon$, then $6m$ items of size $\frac12 + \varepsilon$, with a small $\varepsilon > 0$. First fit packs the first kind six to a bin ($m$ bins), the second kind two to a bin ($3m$ bins), and the third kind one to a bin ($6m$ bins): $10m$ bins. One item of each kind fits into one bin, so $\mathrm{OPT} = 6m$. The lists that reach 1.7 use the same idea with items near $\frac16$, $\frac13$ and $\frac12$ whose sizes are perturbed so that the small items fill bins badly; they are in the cited papers.

## Variants and improvements

- **Best fit.** Put the item into the fullest bin where it fits. It has the same bounds, $\lfloor 1.7\,\mathrm{OPT} \rfloor$ and asymptotic ratio 1.7; see [best fit](/best-fit-bin-packing/).
- **Worst fit and almost worst fit.** Worst fit puts the item into the emptiest open bin; its asymptotic ratio is 2. Almost worst fit uses the second emptiest bin and has ratio 1.7.
- **First fit decreasing.** If the whole list is known, sort it by decreasing size first. The bound drops to $\frac{11}{9}\mathrm{OPT} + \frac69$; see [first fit decreasing](/first-fit-decreasing/).
- **Harmonic type algorithms.** Online algorithms that classify items by size reach asymptotic ratios below 1.6. No online algorithm has asymptotic ratio below about 1.54 (see the survey of Coffman, Garey and Johnson).
- **Memory allocation.** The same rule allocates blocks in memory; see [first-fit allocation](/first-fit-allocation/).

## When to use it

Use first fit for online packing when all bins may stay open and a simple rule is wanted. It is a good default for one-dimensional packing in practice: on random lists its waste is small. If the list is known in advance, sort it first and use [first fit decreasing](/first-fit-decreasing/). If only a few bins may be open at a time, use [next fit](/next-fit-bin-packing/) or a bounded-space rule.

## Pitfalls

- **Quadratic time.** The direct scan in line L3 is fine for small lists but costs $\Theta(n^2)$ on lists of large items. Use the tree.
- **Floating-point sizes.** The test $\mathrm{load} + s_i \le 1$ must be exact. Use integer sizes and an integer capacity, or exact fractions.
- **The constant in the bound.** The bound $1.7\,\mathrm{OPT} + 2.9$ proved here is asymptotic. Do not quote it as the absolute bound; the absolute bound is $\lfloor 1.7\,\mathrm{OPT} \rfloor$, with a much longer proof.
- **Order matters.** On the same multiset of sizes, first fit can use between $\mathrm{OPT}$ and $1.7\,\mathrm{OPT}$ bins, depending on the order. Sorting by decreasing size is the usual fix.

## Implementations

## History

Ullman (1971, Princeton technical report) proved $\mathrm{FF} \le 1.7\,\mathrm{OPT} + 3$. Garey, Graham and Ullman (1972) lowered the term to 2, and Johnson, Demers, Ullman, Garey and Graham (1974) gave the weight function proof and the lower bound lists. Garey, Graham, Johnson and Yao (1976) proved $\mathrm{FF} \le \lceil 1.7\,\mathrm{OPT} \rceil$. Later work lowered the absolute ratio: Simchi-Levi (1994) proved 1.75, and Xia and Tan (2010) and Boyar, Dósa and Epstein (2012) proved $\frac{12}{7}$. Dósa and Sgall (2013) closed the question with $\lfloor 1.7\,\mathrm{OPT} \rfloor$.

## References
