---
tag: Y3SNG1
kind: algorithm
slug: pairwise-sorting-network
name: Pairwise sorting network
aliases:
- Parberry's pairwise sorting network
- pairwise sort
area: sorting/sorting-networks
level: advanced
summary: Parberry's network that sorts pairs, sorts the first and second items of the pairs, and then sorts the sorted pairs, with exactly the size and depth of odd-even merge sort.
solves: [sorting-problem]
model: sorting-network
complexity:
  vars: {n: "the number of items, a power of 2 in the exact counts"}
  time: {worst: Θ(n log² n), average: Θ(n log² n), best: Θ(n log² n)}
  space: {extra: Θ(log n)}
  depth: {worst: Θ(log² n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1992
  people: [Ian Parberry]
  note: Parberry published the pairwise sorting network in Parallel Processing Letters in 1992.
prereqs: [odd-even-merge-sort]
see_also: [odd-even-merge-sort, bitonic-sort, zero-one-principle, merging-network, network-size, network-depth]
sources:
  - paper: doi:10.1142/S0129626492000337
    title: Ian Parberry, The pairwise sorting network, Parallel Processing Letters 2(2-3) (1992)
    locator: pp. 205 to 211 (Section 2, the construction; Section 3, sorting sorted pairs; Section 4, the size and the depth)
  - paper: doi:10.1145/1468075.1468121
    title: K. E. Batcher, Sorting networks and their applications, AFIPS Spring Joint Computer Conference 32 (1968)
    locator: pp. 307 to 314
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (Theorem Z and Floyd's lower bound for merging networks)
---

The pairwise sorting network is Parberry's [sorting network](/sorting-network/) for $n = 2^k$ items. It sorts the items in pairs, sorts the first items and the second items of the pairs on their own, and then sorts the resulting sequence of sorted pairs with $k - 1$ rounds of [comparators](/comparator/). It has exactly the [size](/network-size/) $\tfrac14 n k (k - 1) + n - 1$ and the [depth](/network-depth/) $\tfrac12 k (k + 1)$ of Batcher's [odd-even merge sort](/odd-even-merge-sort/), but the two networks are different. Its interest is a second, simple design that reaches Batcher's bounds, and a step that sorts sorted pairs which is useful on its own.

## In plain words

Put the items in pairs, and put the smaller item of each pair first. Now sort all first items of the pairs, and all second items of the pairs, each with the same method. After this, the pairs are in a good order: each first item is still at most the second item of its pair, and both rows are sorted.

The list is not yet sorted, but it is close. Compare the second item of each pair with the first item of the pair half the number of pairs further on. Then do the same with a quarter, an eighth, and so on, down to the next pair. Each round halves the size of the part that is out of order.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, where $n = 2^k$. The output is the same array in non-decreasing order. The method must be a fixed sequence of compare-exchange steps that depends on $n$ only. This is the [sorting problem](/sorting-problem/) in the [sorting network](/sorting-network/) model.

## The algorithm

The call PAIRWISE-SORT$(A, 0, n, 1)$ sorts the full array. A call PAIRWISE-SORT$(A, lo, m, r)$ sorts the subsequence $A[lo], A[lo + r], \ldots, A[lo + m - r]$ of $L = m / r$ items. In this subsequence, the pair $i$ is the items at places $2i$ and $2i + 1$. We call them $a_i$ and $b_i$; they are on the wires $lo + 2ir$ and $lo + (2i + 1) r$.

```pseudo id=main
PAIRWISE-SORT(A, lo, m, r)                 ▷ sort A[lo], A[lo + r], .., A[lo + m − r]
L1  if r ≥ m then return                   ▷ at most one item
L2  for i ← lo, lo + 2r, lo + 4r, .. while i < lo + m do COMPARE(A, i, i + r)    ▷ sort each pair
L3  PAIRWISE-SORT(A, lo, m, 2r)            ▷ sort the first items a_0, a_1, ..
L4  PAIRWISE-SORT(A, lo + r, m, 2r)        ▷ sort the second items b_0, b_1, ..
L5  k ← m / (2r)                           ▷ the number of pairs
L6  g ← k / 2
L7  while g ≥ 1 do
L8      for i ← 0 to k − g − 1 do COMPARE(A, lo + (2i + 1) r, lo + 2(i + g) r)    ▷ b_i against a_(i+g)
L9      g ← g / 2

COMPARE(A, i, j)                           ▷ a comparator [i:j], with i < j
L10 if A[i] > A[j] then exchange A[i] and A[j]
```

Lines L2 to L4 are Parberry's steps 1 and 2, and lines L5 to L9 are step 3, the sort of sorted pairs. The comparators of line L2, and of one round of line L8, have disjoint wires, so each of them is one layer. The two calls of lines L3 and L4 use disjoint wires and run at the same time. All comparators are standard, because $(2i + 1) r < 2(i + g) r$ for $g \ge 1$.

## Example

Sort $A = [1, 6, 8, 3, 2, 7, 5, 4]$, so $k = 4$ pairs at the top level.

| step | comparators | the array |
|---|---|---|
| sort the pairs (L2) | [0:1] [2:3] [4:5] [6:7] | 1 6 3 8 2 7 4 5 |
| sort the first items (L3) | on wires 0, 2, 4, 6 | 1 6 2 8 3 7 4 5 |
| sort the second items (L4) | on wires 1, 3, 5, 7 | 1 5 2 6 3 7 4 8 |
| $g = 2$ (L8) | [1:4] [3:6] | 1 3 2 4 5 7 6 8 |
| $g = 1$ (L8) | [1:2] [3:4] [5:6] | 1 2 3 4 5 6 7 8 |

After line L4 the pairs are $(1, 5), (2, 6), (3, 7), (4, 8)$: both rows are sorted and each pair is in order. The round $g = 2$ compares $b_0 = 5$ with $a_2 = 3$ and $b_1 = 6$ with $a_3 = 4$, and the round $g = 1$ fixes the rest. The network for $n = 8$ has 19 comparators in 6 layers, the same numbers as odd-even merge sort.

## Correctness

By the [zero-one principle](/zero-one-principle/) it is enough to consider inputs of zeros and ones. After line L2 each pair has $a_i \le b_i$, so the second items hold at least as many ones as the first items. After lines L3 and L4 both rows are sorted, with $\alpha$ zeros among the first items and $\beta \le \alpha$ zeros among the second items. Then $a_i = 0$ if and only if $i < \alpha$, $b_i = 0$ if and only if $i < \beta$, and the sequence is $0^{2\beta} (0 1)^{\mu} 1^{\ast}$ with the *amplitude* $\mu = \alpha - \beta$. It is sorted if and only if $\mu \le 1$. The key lemma: if $\mu \le 2g$, the round $g$ of line L8 keeps this form and leaves an amplitude of at most $g$. If $\mu \le g$, no comparator of the round exchanges anything; else it exchanges exactly the pairs $b_i, a_{i+g}$ with $\beta \le i < \alpha - g$, and the new amplitude is $2g - \mu < g$. The rounds $g = k/2, k/4, \ldots, 1$ take the amplitude from at most $k$ down to at most 1. The full proof is below.

## Complexity

Let $n = 2^k$. The sort of $p$ sorted pairs in lines L5 to L9 has $\lg p$ rounds, and the round with the value $g$ has $p - g$ comparators, so it has $\sum_{j=1}^{\lg p} (p - p/2^j) = p \lg p - p + 1$ comparators in $\lg p$ layers. Then the size $S$ and the depth $D$ satisfy, with $S(1) = D(1) = 0$,

$$S(n) = 2 S(n/2) + \tfrac{n}{2} + \tfrac{n}{2} \lg \tfrac{n}{2} - \tfrac{n}{2} + 1, \qquad D(n) = D(n/2) + 1 + \lg \tfrac{n}{2},$$

so $S(n) = 2 S(n/2) + \tfrac12 n (\lg n - 1) + 1$ and $D(n) = D(n/2) + \lg n$. These are the recurrences of odd-even merge sort, so

$$S(n) = \tfrac14 n k (k - 1) + n - 1, \qquad D(n) = \tfrac12 k (k + 1).$$

For $n = 2, 4, 8, 16, 32, 64$ this is $1, 5, 19, 63, 191, 543$ comparators and $1, 3, 6, 10, 15, 21$ layers.

- **Sequential time.** $\Theta(n \log^2 n)$ in each case.
- **Parallel time.** $\Theta(\log^2 n)$ with $n/2$ processors.
- **Extra space.** $\Theta(\log n)$ for the recursion.

The step that sorts $p$ sorted pairs has optimal depth $\lg p$, and its size is at most twice the optimum. Parberry shows this by turning it into a [merging network](/merging-network/): compare $x_i$ with $y_i$ for two sorted 0-1 lists $x$ and $y$, and the interleave $(x_0, y_0, x_1, y_1, \ldots)$ is a sequence of sorted pairs. So the lower bounds for merging, Floyd's $\tfrac12 p \lg p - O(p)$ comparators and depth about $\lg p$, apply.

## Properties

- **Same costs as Batcher, different network.** For $n = 16$ the third layer differs from that of odd-even merge sort, and Parberry proves by induction that the two networks are not isomorphic for each larger power of 2.
- **Data oblivious, in place, not stable, not adaptive,** as each sorting network of this kind.
- **Its first $k$ layers are a hypercube.** Lines L2 to L4 start with the layers that compare $i$ with $i \oplus 1$, then $i \oplus 2$, and so on, up to $i \oplus n/2$: the first layer of every level of recursion runs before the later rounds. After these $k$ layers, the wire $w$ holds an item that is at most the item on each wire $w'$ whose binary digits include those of $w$.

## Variants and improvements

- **Any $n$.** Build the network for the next power of 2 and drop each comparator that touches a wire $j \ge n$. The missing wires act as $+\infty$, and in a network of standard comparators a comparator on such a wire changes nothing. The Python code below does this.
- **Sorting sorted pairs elsewhere.** Lines L5 to L9 on their own sort any sequence of sorted pairs whose two rows are sorted. Parberry used this step to reduce the depth of a reduction in his work on the complexity of [verifying sorting networks](/sorting-network-verification/).
- **Smaller networks for fixed $n$.** For $n = 16$ the best known size is 60 and the best known depth is 9, both below the 63 comparators and 10 layers of the pairwise and the odd-even networks. See [Green's network](/green-filter/).

## When to use it

Use the pairwise network where you would use odd-even merge sort: hardware, SIMD code and oblivious algorithms with a size that is a power of 2. The costs are the same, so the choice depends on the wiring. The pairwise network starts with the $k$ hypercube layers, which some layouts prefer. For small fixed $n$, a network from the tables of optimal networks is smaller.

## Pitfalls

- **The wrong pairs in line L8.** The round compares the second item $b_i$ of a pair with the first item $a_{i+g}$ of a later pair. Comparing $a_i$ with $a_{i+g}$, or $b_i$ with $b_{i+g}$, does nothing useful, because both rows are already sorted.
- **The order of the rounds.** The rounds must run with $g = k/2$ first and $g = 1$ last. In the other order the amplitude is not reduced.
- **A false claim of fewer comparators.** The pairwise network does not have fewer comparators than odd-even merge sort; it has exactly as many.

## Implementations

## History

Ian Parberry published the pairwise sorting network in Parallel Processing Letters in 1992. He built it with the zero-one principle as a guide, and he proved that it has the same size and depth as Batcher's odd-even merge sort of 1968 but is not isomorphic to it.

## References
