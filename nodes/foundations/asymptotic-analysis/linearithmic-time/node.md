---
tag: EWMRWP
kind: concept
slug: linearithmic-time
name: Linearithmic time
aliases:
- n log n time
- quasilinear time
area: foundations/asymptotic-analysis
level: intro
summary: Running time of order n log n, the typical cost of efficient comparison sorting.
prereqs: [asymptotic-notation, logarithms, time-complexity]
see_also: [common-growth-rates, linear-time, quadratic-time, merge-sort, master-theorem, comparison-sort-lower-bound, fast-fourier-transform, element-distinctness]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3 (merge sort), Chapter 4 (the master method), Chapter 6 (heapsort), Section 7.2 (unbalanced splits of quicksort) and Section 8.1 (lower bounds for sorting)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4 (sorting by merging) and Section 5.3.1 (minimum-comparison sorting)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Mergesort (the lower bound for compare-based sorting) and Section 1.4
  - paper: doi:10.1145/800061.808735
    title: Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983), 80 to 86
    locator: the lower bound for element distinctness
  - paper: doi:10.1016/j.jalgor.2003.09.001
    title: Yijie Han, Deterministic sorting in O(n log log n) time and linear space, Journal of Algorithms 50(1), 96 to 105 (2004)
    locator: the main theorem
---

An algorithm runs in linearithmic time when its cost is $T(n) = \Theta(n \log n)$ for an [input size](/input-size/) $n$, or $O(n \log n)$ when only an upper bound is known. It lies between [linear time](/linear-time/) and [quadratic time](/quadratic-time/): $n \log n$ grows faster than $n$, but more slowly than $n^{1+\varepsilon}$ for each constant $\varepsilon > 0$. It is the cost of [merge sort](/merge-sort/) and of every optimal sort in the [comparison model](/comparison-model/), and of divide and conquer algorithms that do linear work to split and combine.

## In plain words

Sort a deck of cards by splitting it into two halves, sorting each half the same way, and then merging the two sorted halves. A merge touches each card once. The deck can be halved about as many times as the logarithm of its size, and at each level of halving the merges together touch each card once. So the total work is the number of cards times the number of levels.

This is more than a single pass, but not by much. For a million items there are about 20 levels, so about twenty million steps. A method that compares every pair of items needs about half a million million steps.

The same total appears when each of the items needs a logarithmic amount of work, for example one insertion into a balanced tree.

## The idea

### Definition

Fix a model and a case, and let $T(n)$ be the cost. The algorithm runs in linearithmic time when $T(n) = \Theta(n \log n)$. The phrase "runs in $O(n \log n)$ time" is the common upper-bound form, and it is also true of a linear-time algorithm. The base of the logarithm does not matter, see [logarithms](/logarithms/). The bound is stated for $n \ge 2$.

The word "quasilinear" is used in two ways. Many authors use it for the wider class $O(n \log^k n)$ for a constant $k$, which also contains $n \lg^2 n$. Others use it for $n \log n$ alone. State which meaning you use.

### The main example: merge sort, counted exactly

Let $C(n)$ be the largest number of comparisons that [merge sort](/merge-sort/) makes on $n$ items, for $n = 2^k$. Merging two sorted lists of $m$ items makes at most $2m - 1$ comparisons, so $C(1) = 0$ and $C(2m) \le 2C(m) + 2m - 1$.

*Claim.* $C(n) \le n \lg n - n + 1$ for each $n = 2^k$, with equality.

*Proof of the bound.* For $n = 1$ both sides are 0. If the claim holds for $m$, then

$$C(2m) \le 2(m \lg m - m + 1) + 2m - 1 = 2m \lg m + 1 = 2m \lg(2m) - 2m + 1.$$

*Proof of equality.* Define the input $W_n$ by $W_1 = (0)$ and $W_{2m} = (2W_m, \ 2W_m + 1)$, where $2W_m$ means each entry doubled. The left half of $W_{2m}$ holds the even values and the right half the odd values. After each half is sorted, they are $0, 2, 4, \ldots$ and $1, 3, 5, \ldots$, which interleave completely, so the merge takes the items alternately and makes all $2m - 1$ comparisons. Each half is $W_m$ with every entry doubled, or doubled plus 1, and these maps keep the order, so each half is again a worst case. So equality holds at each level. $\square$

For general $n$ the exact worst case is $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ (Knuth, Section 5.2.4). The table compares $C(n)$ with the lower bound $\lceil \lg(n!) \rceil$ below.

| $n$ | merge sort, worst case | $\lceil \lg(n!) \rceil$ | $n \lg n$ |
| --- | --- | --- | --- |
| 8 | 17 | 16 | 24 |
| 16 | 49 | 45 | 64 |
| 64 | 321 | 296 | 384 |
| 1024 | 9217 | 8770 | 10240 |

### The lower bound for comparison sorting

Every algorithm that sorts $n$ distinct keys and learns about them only by comparisons of two keys makes at least $\lceil \lg(n!) \rceil$ comparisons on some input. *Proof.* Its [decision tree](/decision-tree-model/) is a binary tree. Two different orders of the input need different permutations to sort them, so they reach different leaves, and the tree has at least $n!$ leaves. A binary tree of height $h$ has at most $2^h$ leaves, so $h \ge \lg(n!)$. $\square$ Since $\lg(n!) \ge \lg((n/2)^{n/2}) = (n/2)\lg(n/2)$, the bound is $\Omega(n \log n)$. For $n = 10$ it is 22, and for $n = 1000$ it is 8530, against $n \lg n \approx 9966$. See [comparison sort lower bound](/comparison-sort-lower-bound/) and CLRS, Section 8.1. So merge sort and [heapsort](/heapsort/) are worst-case optimal in the comparison model, up to a constant factor, and merge sort is optimal up to a lower-order term.

### Other shapes of linearithmic-time algorithms

**Divide and conquer with linear combining.** If $T(n) = 2T(n/2) + \Theta(n)$, then $T(n) = \Theta(n \log n)$ by case 2 of the [master theorem](/master-theorem/). The split does not need to be even. If each part has at most a fraction $c < 1$ of the items, for a constant $c$, the recursion has $O(\log n)$ levels with total cost $O(n)$ on each, so the cost is still $O(n \log n)$. CLRS, Section 7.2, works out the split of $1/10$ against $9/10$ for quicksort. The [fast Fourier transform](/fast-fourier-transform/) on $n$ points has this shape and uses $\Theta(n \log n)$ arithmetic operations.

**A logarithmic operation for each item.** $n$ operations on a [balanced binary search tree](/balanced-binary-search-tree/) or a [binary heap](/binary-heap/), each of cost $O(\log n)$, cost $O(n \log n)$. When the size grows from 1 to $n$, the sum is $\sum_{k=1}^{n} \lg k = \lg(n!)$, which is still $\Theta(n \log n)$ by the bound above and $\lg(n!) \le n \lg n$.

**Sort, then scan.** Many tasks are a sort followed by a linear pass: find duplicates, group equal keys, find the closest pair of numbers on a line. The sort dominates.

### When the input doubles

For the exact function $n \lg n$, $\frac{2n \lg(2n)}{n \lg n} = 2\left(1 + \frac{1}{\lg n}\right)$. This is about $2.20$ for $n = 10^3$ and about $2.10$ for $n = 10^6$, and it tends to 2 from above. An experiment with the [doubling hypothesis](/doubling-hypothesis/) sees a ratio near 2 and cannot tell this class from linear time without a fit that includes the logarithm. For $n = 10^6$ the factor $\lg n$ is about 20, and for $n = 10^9$ about 30.

### Pitfalls

- **Name the case.** [Quicksort](/quicksort/) is $\Theta(n \log n)$ in expectation with a random pivot and $\Theta(n^2)$ in the worst case. Merge sort is $\Theta(n \log n)$ in each case. Heapsort is $O(n \log n)$ in the worst case. With all keys equal, each sift-down stops at once, and heapsort takes $\Theta(n)$ time. See [worst-case analysis](/worst-case-analysis/).
- **The lower bound belongs to the model.** The $\Omega(n \log n)$ bound counts comparisons. [Counting sort](/counting-sort/) and [radix sort](/radix-sort/) use the keys as indices and sort $n$ integers from a range of size $n^{O(1)}$ in $O(n)$ time. On the [word RAM](/word-ram/), $n$ integers of one word each can be sorted deterministically in $O(n \log \log n)$ time (Han, 2004). A claim that "sorting needs $n \log n$" must say "by comparisons".
- **The cost of a comparison.** When a comparison of two keys is not $O(1)$, the time is larger than the count of comparisons. Merge sort on $n$ strings of length up to $m$ makes $O(n \log n)$ string comparisons and $O(m\,n \log n)$ character comparisons.
- **The measure of input size.** For $n$ strings of total length $N$, the input size is $N$, not $n$. A sort with $O(n \log n)$ comparisons of strings is not "$O(N \log N)$" without an argument about the cost of each comparison.
- **The wrong split.** The recurrence $T(n) = T(n-1) + \Theta(n)$, from a split of one item against the rest, gives $\Theta(n^2)$, not $\Theta(n \log n)$. A constant fraction is required, not a constant number of items.
- **Hidden extra work.** A sort followed by a quadratic step is quadratic. Copying the input into a new array at each level of a recursion adds $\Theta(n)$ per level, which keeps the class, but allocating a new array in each call of the merge can dominate the constant factor in practice.
- **Constants.** For short inputs a quadratic sort with a small constant can be faster. Library sorts switch to [insertion sort](/insertion-sort/) for short subarrays for this reason.

## Examples

- Merge sort of $n = 8$ items: at most 17 comparisons, reached by the input $0, 4, 2, 6, 1, 5, 3, 7$, which is $W_8$ above.
- Any comparison sort of 10 items: at least 22 comparisons on some input.
- Heapsort of $n$ items: a bottom-up heap build in $O(n)$ time, then $n - 1$ extractions of the maximum with $O(\log n)$ each, for $O(n \log n)$.
- Duplicate check in an array of $n$ numbers by sorting and a scan of neighbors: $O(n \log n)$. This [element distinctness](/element-distinctness/) problem needs $\Omega(n \log n)$ steps also in the [algebraic decision tree](/algebraic-decision-tree/) model, by Ben-Or (1983), whose bound holds for algebraic computation trees. So sort-then-scan is optimal there. With hashing, the expected time is $O(n)$, outside that model.
- Non-example: building a binary heap bottom up takes $\Theta(n)$ time, although each sift-down is $O(\log n)$. The cost of a sift-down is proportional to the height of its node, and most nodes are near the leaves.
- Non-example: counting sort of $n$ integers in the range $0$ to $k - 1$ takes $\Theta(n + k)$ time.
- Non-example: selection sort makes $n(n-1)/2$ comparisons on each input.

## Where it is used

Linearithmic time is the standard cost of general-purpose sorting, and many algorithms use a sort as a step. It is also the cost of the FFT, of many divide and conquer algorithms in computational geometry such as [Graham scan](/graham-scan/) for the [convex hull](/convex-hull/), and of $n$ operations on a balanced tree or a heap. A running time below $n \log n$ needs more than comparisons, or more structure in the input. See the table of the [common growth rates](/common-growth-rates/).

## References
