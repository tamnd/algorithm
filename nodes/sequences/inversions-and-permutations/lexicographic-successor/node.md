---
tag: ERZ6T3
kind: problem
slug: lexicographic-successor
name: Lexicographic successor of a permutation
aliases:
- next permutation problem
area: sequences/inversions-and-permutations
level: core
summary: Given a permutation, find the next one in lexicographic order.
prereqs: [permutation, lexicographic-order]
see_also: [next-permutation, lexicographic-permutation-successor, lehmer-code, factorial-number-system, permutation-rank-unrank, generating-all-permutations, multiset-permutations, steinhaus-johnson-trotter]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (generating all permutations, Algorithm L for lexicographic permutation generation, and its history)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversion tables and the correspondence between permutations and mixed-radix numbers)
---

The lexicographic successor of a [permutation](/permutation/) is the next permutation of the same items in [lexicographic order](/lexicographic-order/), the order of words in a dictionary. It is found by locating the longest decreasing suffix, swapping the item just before it with the smallest larger item in that suffix, and reversing the suffix. This takes $O(n)$ time in the worst case and $O(1)$ amortized time over a run through all $n!$ permutations. Seen through the [Lehmer code](/lehmer-code/), the step is the same as adding 1 to a number in the [factorial number system](/factorial-number-system/), and the decreasing suffix is the block of digits that roll over.

## In plain words

List all the ways to arrange a few letters in dictionary order, and ask which arrangement comes right after a given one.

Look at the end of the word. If its last letters are already in falling order, they are as late as they can be, so the change must happen just before them. Take the letter just before that falling tail and replace it by the next larger letter from the tail. Then put the tail in rising order, the earliest it can be. The result is the very next word.

This is like adding one to a counter: the digits at the end that are already at their maximum go back to the start, and the first digit that can grow goes up by one.

## Definition

**Input.** A sequence $a = (a_1, \ldots, a_n)$ of items from a [total order](/total-order/), usually a permutation of $[n]$.

**Order.** For two arrangements $a \ne b$ of the same items, $a < b$ in lexicographic order when $a_k < b_k$ at the first position $k$ with $a_k \ne b_k$.

**Output.** The least arrangement $b$ of the same items with $b > a$, or a signal that $a$ is the last one, which happens exactly when $a$ is non-increasing.

**The standard solution.** For a permutation it is unique, and it is computed in four steps:

```pseudo
SUCCESSOR(a[1 .. n])
1  i ← n − 1
2  while i ≥ 1 and a[i] ≥ a[i + 1] do i ← i − 1
3  if i = 0 then return LAST                     ▷ a is non-increasing
4  j ← n
5  while a[j] ≤ a[i] do j ← j − 1
6  exchange a[i] and a[j]
7  reverse a[i + 1 .. n]
8  return a
```

*Why it is right.* Let $a_{i+1} \ge \cdots \ge a_n$ be the longest non-increasing suffix, so $a_i < a_{i+1}$. Every arrangement that keeps the prefix $a_1 \cdots a_i$ has its last $n - i$ items in some order, and the non-increasing one is the largest of them, so the successor must change position $i$ or an earlier one. It cannot change an earlier one while staying close: keeping $a_1 \cdots a_{i-1}$ and putting at position $i$ some item of the suffix that is larger than $a_i$ already gives a larger arrangement. The least choice is the smallest such item, $a_j$, which is the rightmost item larger than $a_i$ because the suffix is non-increasing. After the exchange, the suffix is still non-increasing, since $a_i$ took the place of $a_j$ between an item larger than $a_j$ and an item not larger than $a_i$. Reversing it gives the least order of those items. So the result is the least arrangement larger than $a$.

## Variants

- **Predecessor.** Reverse every comparison: find the longest non-decreasing suffix, exchange the item before it with the largest smaller item of the suffix, and reverse the suffix.
- **Multisets.** With repeated items, the same algorithm with the non-strict tests of lines 2 and 5 steps through the distinct arrangements, each once. Starting from $1\,1\,2\,2$ it lists the $\binom42 = 6$ arrangements $1122, 1212, 1221, 2112, 2121, 2211$. See [multiset permutations](/multiset-permutations/).
- **The $k$-th successor.** To jump $k$ places, [rank](/permutation-rank-unrank/) the permutation, add $k$ and unrank, in $O(n \log n)$ time with a [Fenwick tree](/fenwick-tree/), instead of $k$ steps.
- **Other orders.** In the [Steinhaus-Johnson-Trotter order](/steinhaus-johnson-trotter/) or the order of [Heap's algorithm](/heaps-algorithm/), consecutive permutations differ by a single exchange, and the successor takes $O(1)$ time in the worst case with extra state. Lexicographic order needs up to $\lfloor (n-1)/2 \rfloor + 1$ exchanges per step.
- **Successor among $k$-permutations or combinations.** The same suffix idea gives the next $k$-subset in lexicographic order.

## Examples

**One step.** For $a = 1\,3\,6\,5\,4\,2$, the longest decreasing suffix is $6\,5\,4\,2$, so $i = 2$ with $a_2 = 3$. The rightmost item larger than 3 is $4$, at $j = 5$. Exchanging gives $1\,4\,6\,5\,3\,2$, and reversing the suffix gives
$$\operatorname{succ}(1\,3\,6\,5\,4\,2) = 1\,4\,2\,3\,5\,6.$$
In Lehmer code, $(0, 1, 3, 2, 1, 0)$ becomes $(0, 2, 0, 0, 0, 0)$. The last four digits were at their maxima $3, 2, 1, 0$, one for each item of the decreasing suffix. They roll over to 0 and the digit before them goes up by 1. The [rank](/permutation-rank-unrank/) goes from 47 to 48.

**A short step.** $\operatorname{succ}(3\,1\,4\,5\,2) = 3\,1\,5\,2\,4$: the suffix is $5\,2$, the item $4$ is exchanged with $5$, and the suffix $4\,2$ is reversed. The Lehmer code goes from $(2, 0, 1, 1, 0)$ to $(2, 0, 2, 0, 0)$.

**The whole list for $n = 3$.** $123 \to 132 \to 213 \to 231 \to 312 \to 321$, and $321$ is the last.

**A step that changes every position.** $\operatorname{succ}(1\,4\,3\,2) = 2\,1\,3\,4$. In general $1\,n\,(n-1) \cdots 2$ is followed by $2\,1\,3 \cdots n$, and no position keeps its item.

## Known algorithms

- **Suffix scan, exchange and reversal.** The method above. Knuth gives it as Algorithm L in Section 7.2.1.2 and traces it to Nārāyaṇa Paṇḍita in fourteenth-century India. The C++ library function `std::next_permutation` implements it. The algorithm page is [next permutation](/next-permutation/), and the same problem in the combinatorics area is [lexicographic permutation successor](/lexicographic-permutation-successor/).
- **Through the Lehmer code.** Keep the Lehmer code $c$ along with $a$. Add 1 to $c$ in the factorial base, and redo the suffix of $a$ that corresponds to the digits that changed. This is the same work as the direct method, organized as a counter.
- **Generating all permutations.** Starting from the sorted order and applying the successor until LAST lists all $n!$ permutations in lexicographic order. See [generating all permutations](/generating-all-permutations/).

## Bounds

- **Worst case.** $\Theta(n)$ time. A step can change all $n$ positions, as in the last example, so $\Omega(n)$ writes are needed for some inputs.
- **Amortized.** Let $L$ be the length of the longest decreasing suffix. Lines 2 and 5 make at most $L + 1$ comparisons each, and lines 6 and 7 move at most $L + 1$ items. For a uniform random permutation, $\Pr[L \ge k] = 1/k!$ for $1 \le k \le n$, because the last $k$ items are in decreasing order with that probability. So $\mathbb{E}[L] = \sum_{k=1}^{n} 1/k! < e - 1 \approx 1.718$, and a run through all $n!$ permutations costs $O(n!)$ in total, $O(1)$ amortized per step.
- **Lower bound per step.** Any method that keeps only the array must read the whole decreasing suffix and the item before it to know where the change happens, so $L + 1$ reads are necessary on each input.

## Reductions

- **To the factorial number system.** Lexicographic order on $S_n$ is the order of the [Lehmer codes](/lehmer-code/) read as numbers in the [factorial base](/factorial-number-system/), so the successor of $a$ is the permutation whose code is the code of $a$ plus 1. A decreasing suffix of length $L$ is exactly a block of $L$ maximal digits $c_i = n - i$ at the end of the code.
- **To ranking.** $\operatorname{succ}(a) = \operatorname{unrank}(\operatorname{rank}(a) + 1)$, which turns any [rank and unrank](/permutation-rank-unrank/) algorithm into a successor algorithm, more slowly.
- **From combinations.** The successor of a $k$-subset of $[n]$ in lexicographic order is the lexicographic predecessor of its 0-1 word, a multiset permutation of 0s and 1s: the subsets $12, 13, 14, 23, 24, 34$ of $[4]$ have the words $1100, 1010, 1001, 0110, 0101, 0011$, in decreasing order.

## Applications

- **Exhaustive search.** Trying every order of a few items, as in brute-force solutions of the traveling salesman problem or of scheduling puzzles, with the next permutation function as the loop step.
- **Contest and library use.** `std::next_permutation` and `std::prev_permutation` in C++ are this algorithm, and many problems ask for the $k$-th next arrangement or for the next larger number with the same digits.
- **Next larger number with the same digits.** The digits of a number form a multiset, and the successor of its digit sequence is the least larger number made of the same digits, as $1\,3\,6\,5\,4\,2 \to 1\,4\,2\,3\,5\,6$.
- **Testing and enumeration.** Listing the permutations of small $n$ in a fixed order gives reproducible test cases for sorting and permutation code.

## References
