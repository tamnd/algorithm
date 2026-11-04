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
see_also: [common-growth-rates, linear-time, quadratic-time, merge-sort, master-theorem, comparison-sort-lower-bound, fast-fourier-transform, doubling-hypothesis]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2 (merge sort), Chapter 4 (divide and conquer) and Section 8.1 (lower bounds for sorting)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (minimum-comparison sorting)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2 (mergesort) and Section 1.4
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, STOC 1983"
    locator: the lower bound for element distinctness
---

An algorithm runs in linearithmic time when its running time is $T(n) = \Theta(n \log n)$ for an input of size $n$, or $O(n \log n)$ when only an upper bound is known. It sits between [linear time](/linear-time/) and [quadratic time](/quadratic-time/): $n \log n$ grows faster than $n$, but more slowly than $n^{1+\varepsilon}$ for each constant $\varepsilon > 0$. It is the typical cost of sorting by comparisons and of divide and conquer algorithms that do linear work to split and combine.

## In plain words

Sort a deck of cards by splitting it into two halves, sorting each half, and then merging the two sorted halves. The merging touches every card once. You do this at every level of the splitting. The deck can be halved about as many times as the logarithm of its size. So you touch every card once for each level, and the total work is the number of cards times the number of levels.

This is more than a single pass, but not by much. For a million items the number of levels is about 20. A method that compares every pair of items would need on the order of half a million times a million steps, and the halving method needs about twenty million.

The same shape appears when each item needs a logarithmic amount of work.

## The idea

### Definition

Fix a model and a case, and let $T(n)$ be the cost. The algorithm runs in linearithmic time when $T(n) = \Theta(n \log n)$. The phrase "runs in $O(n \log n)$ time" is the common upper-bound form, and it also holds for a linear-time algorithm. The base of the logarithm does not matter, see [logarithms](/logarithms/). The bound makes sense for $n \ge 2$.

Most authors use the name "quasilinear" for the wider class $O(n \log^k n)$ for a constant $k$, which also contains $n \log^2 n$. A few use it for $n \log n$ alone. A page or a paper that uses the word should say which meaning it has.

### Shapes of linearithmic-time algorithms

**Divide and conquer with linear combining.** Split the input into two parts of about half size, solve each part, and combine in linear time. The cost satisfies $T(n) = 2T(n/2) + \Theta(n)$. By case 2 of the [master theorem](/master-theorem/), $T(n) = \Theta(n \log n)$. A direct count for [merge sort](/merge-sort/) with $n = 2^k$ gives an upper bound. The bound is tight: on an input where each merge interleaves its two halves completely, each merge of $2m$ items makes exactly $2m - 1$ comparisons, so equality holds at each level. Let $C(n)$ be the largest number of comparisons. Merging two sorted lists of $m$ items each takes at most $2m - 1$ comparisons, so $C(1) = 0$ and $C(2m) \le 2C(m) + 2m - 1$. We claim $C(n) \le n \lg n - n + 1$ for each $n = 2^k$. For $n = 1$ both sides are $0$. For $2m$, with the claim true for $m$:

$$C(2m) \le 2(m \lg m - m + 1) + 2m - 1 = 2m \lg m + 1 = 2m(\lg(2m) - 1) + 1 = 2m \lg(2m) - 2m + 1.$$

So the claim is true for $2m$. For $n = 8$ the bound is $8 \cdot 3 - 8 + 1 = 17$ comparisons. [Heapsort](/heapsort/) also runs in $\Theta(n \log n)$ in the worst case. [Quicksort](/quicksort/) runs in $\Theta(n \log n)$ in expectation with a random pivot, but its worst case is $\Theta(n^2)$.

**Linear work on each of a logarithmic number of levels.** A recursion tree with $\lg n$ levels, where the nodes of each level share a total cost of $\Theta(n)$, gives $\Theta(n \log n)$. The [fast Fourier transform](/fast-fourier-transform/) on $n$ points uses $\Theta(n \log n)$ arithmetic operations in this way.

**A logarithmic operation for each item.** $n$ operations on a [balanced search tree](/balanced-binary-search-tree/) or a [binary heap](/binary-heap/), each of cost $O(\log n)$, cost $O(n \log n)$ in total. [Tree sort](/tree-sort/) with a balanced tree is of this kind. For a size that grows from $1$ to $n$ the sum is $\sum_{k=1}^{n} \lg k = \lg(n!)$, and $\lg(n!) = \Theta(n \log n)$, see [asymptotic notation](/asymptotic-notation/) and [Stirling's approximation](/stirling-approximation/).

**Sort first, then scan.** Many tasks are solved by a sort of cost $\Theta(n \log n)$ followed by a linear pass: find duplicates, group equal keys, find the closest pair on a line. The sort dominates, and the whole algorithm is linearithmic.

### The lower bound for comparison sorting

Every sorting algorithm that gets its information only from comparisons of two keys needs $\Omega(n \log n)$ comparisons in the worst case. Its [decision tree](/decision-tree-model/) must have at least $n!$ leaves, one for each order of the input, so its height is at least $\lceil \lg(n!) \rceil$. For $n = 10$ this is $22$, and for $n = 1000$ it is $8530$ against $n \lg n \approx 9966$. Since $\lg(n!) = \Theta(n \log n)$, the bound is $\Omega(n \log n)$. See [comparison sort lower bound](/comparison-sort-lower-bound/). So merge sort and heapsort are worst-case optimal in the comparison model, up to a constant factor. This bound is about the comparison model only: [radix sort](/radix-sort/) and [counting sort](/counting-sort/) use the values or digits of the keys as array indices, and they can run in linear time for integer keys of bounded range.

### When the input doubles

For the exact function $n \lg n$ we have $2n \lg(2n) / (n \lg n) = 2(1 + 1/\lg n)$. For $n = 10^3$ this is about $2.20$, and for $n = 10^6$ it is about $2.10$. So the ratio is a little above 2 and tends to 2 from above when $n$ grows. If $T(n) \sim a n \lg n$, this holds in the limit. An experiment with the [doubling hypothesis](/doubling-hypothesis/) sees a ratio near 2 and cannot tell this class from linear time without a fit that includes the logarithm. For $n = 10^6$ the factor $\lg n \approx 20$, and for $n = 10^9$ it is about 30, so a linearithmic algorithm is only a small factor slower than a linear one with the same constant.

### Pitfalls

- **Name the case.** Quicksort is $\Theta(n \log n)$ in expectation and $\Theta(n^2)$ in the worst case. Merge sort is $\Theta(n \log n)$ in each case. Heapsort is $\Theta(n \log n)$ in the worst case, and in the best case when the keys are distinct. When all keys are equal, each sift-down stops at once, and heapsort runs in $\Theta(n)$ time. See [worst-case analysis](/worst-case-analysis/).
- **The comparison model.** The $\Omega(n \log n)$ bound does not apply to algorithms that use more than comparisons, for example [radix sort](/radix-sort/).
- **Cost of a comparison.** The bound counts comparisons or steps. When a comparison of two keys costs more than $O(1)$ (strings of length $m$), the total is larger, for example $O(m \, n \log n)$ character comparisons for merge sort on strings.
- **Recurrence with the wrong split.** The recurrence $T(n) = T(n-1) + n$, from a split of one item against the rest, gives $\Theta(n^2)$. The split does not need to be exact. If each part has at most a fraction $c < 1$ of the items for a constant $c$, for example $1/10$ against $9/10$, the cost is still $\Theta(n \log n)$.
- **Hidden extra work.** A sort followed by a step of larger cost, for example a quadratic comparison of the results, makes the whole algorithm cost more than $n \log n$.
- **Constants.** A linearithmic algorithm with a large constant can be slower than a quadratic one with a small constant for every input of practical size. Insertion sort is often used for short subarrays inside sorts of this class.

## Examples

- Merge sort of $n = 8$ items: at most $17$ comparisons by the bound above.
- Any comparison sort of $10$ items: at least $22$ comparisons in the worst case.
- Heapsort of $n$ items: $n$ insertions or one build, and then $n$ extractions of the maximum with cost $O(\log n)$ each, for $O(n \log n)$ in total.
- Check for duplicates in an array of $n$ numbers by sorting and a scan of neighbors: $\Theta(n \log n)$ in the comparison model. This [element distinctness](/element-distinctness/) problem needs $\Omega(n \log n)$ steps even in the [algebraic decision tree](/algebraic-decision-tree/) model. Ben-Or (1983) proved the bound for algebraic computation trees, a model that contains algebraic decision trees, so sort-then-scan is optimal there.
- Non-example: building a binary heap from $n$ items by the bottom-up method takes $\Theta(n)$ time, not $\Theta(n \log n)$, although each sift-down is $O(\log n)$. The cost of a sift-down is proportional to the height of its node, and most nodes are near the leaves.
- Non-example: counting sort of $n$ integers in the range $0$ to $k - 1$ takes $\Theta(n + k)$ time.
- Non-example: selection sort takes $\Theta(n^2)$ comparisons in each case.

## Where it is used

Linearithmic time is the standard cost of general-purpose sorting, and a sort is used as a step in many algorithms. It is also the cost of the FFT and of many divide and conquer algorithms in computational geometry. A running time below $n \log n$ is looked for with more structure on the input. See the table of the [common growth rates](/common-growth-rates/) and the class of [polylogarithmic](/polylogarithmic-time/) bounds.

## References
