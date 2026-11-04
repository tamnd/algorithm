---
tag: V0XMYJ
kind: technique
slug: presorting
name: Presorting
aliases:
- preprocessing by sorting
area: techniques/reductions-and-transforms
level: intro
summary: Sorting the input first so that a later step can scan it in order and avoid repeated comparisons.
prereqs: [sorting-problem, merge-sort, binary-search]
see_also: [transform-and-conquer, reduction-to-sorting, element-distinctness, element-distinctness-lower-bound, mode-finding, remove-duplicates-from-sorted-array, two-sum-sorted, hash-table]
sources:
  - book: isbn:9780132316811
    title: Anany Levitin, Introduction to the Design and Analysis of Algorithms, third edition, Pearson, 2012
    locator: Section 6.1, Presorting (element uniqueness, computing a mode, searching)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition, Springer, 2020
    locator: Chapter 4, Sorting (the applications of sorting)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3 (merge sort)
---

Presorting is the [transform-and-conquer](/transform-and-conquer/) technique in which an algorithm first sorts its input and then solves the problem by one pass over the sorted order. It is the simplest case of *instance simplification* in Levitin's terms: the instance stays the same set of items, but in an order that puts equal and near items next to each other. With an $O(n \log n)$ sort such as [merge sort](/merge-sort/), it turns several quadratic brute-force algorithms, such as the test for [element distinctness](/element-distinctness/) and [mode finding](/mode-finding/), into $O(n \log n)$ ones.

## In plain words

Many questions about a list are hard to answer when the list is in random order. To see if two items are equal, you compare each item with every other item. That is a lot of work for a long list.

Sort the list first. Now equal items stand next to each other, so one walk from left to right finds them. The same walk counts how often each value occurs. A sorted list also lets you find any value fast, by looking in the middle and throwing away the half that cannot hold it.

Sorting has a cost of its own. It pays off when the walk after it is much cheaper than the work it replaces, or when you ask many questions about the same list.

## When it applies

- The answer depends on the multiset of values, not on their positions in the input. Sorting destroys the positions, so a question about positions needs the original indices kept beside the values.
- The question is about equal values (duplicates, counts, groups) or about neighbours in value order (the smallest gap, the next larger value).
- The brute-force algorithm compares all pairs, which costs $\Theta(n^2)$.
- Many queries are asked about one fixed set, so the cost of the sort is shared among them.
- The keys have a total order. If the keys can only be tested for equality, presorting does not apply, and a [hash table](/hash-table/) is the usual tool.

## The template

The input is an array $A[1 \ldots n]$ of keys with a total order. The holes are SORT, the per-run action VISIT, and the final COMBINE.

```pseudo id=main
PRESORT-SCAN(A, n)
L1  SORT(A)                          ▷ any O(n log n) sort; A[1] ≤ A[2] ≤ … ≤ A[n]
L2  i ← 1
L3  while i ≤ n do
L4      j ← i
L5      while j < n and A[j + 1] = A[i] do
L6          j ← j + 1
L7      VISIT(A[i], j − i + 1)        ▷ the run A[i .. j] holds all copies of A[i]
L8      i ← j + 1
L9  return COMBINE()
```

After line L1, all copies of a value form one contiguous run, because a value $v$ and a larger value $w$ in the wrong order would contradict the sorted order. Lines L3 to L8 visit each run once, from the smallest value to the largest. Each pass of the inner test at L5 either moves $j$ forward or ends the run, so lines L2 to L8 use exactly $n - 1$ key comparisons in total: one for each adjacent pair $(A[k], A[k+1])$. The total cost is the cost of the sort plus $n - 1$ comparisons.

For element distinctness, VISIT returns "not distinct" as soon as a run has length at least 2. For the mode, VISIT keeps the run with the largest length. For a set of queries, the scan is replaced by one [binary search](/binary-search/) for each query.

## Classic examples

### Element uniqueness

The brute-force test compares every pair. When all items are distinct, it makes $\binom{n}{2} = n(n-1)/2$ comparisons. Presorting with merge sort uses at most $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ comparisons for the sort and at most $n - 1$ for the scan.

| $n$ | brute force | merge sort + scan |
|---|---|---|
| $8$ | $28$ | $17 + 7 = 24$ |
| $10^6$ | $499{,}999{,}500{,}000$ | $18{,}951{,}425 + 999{,}999 = 19{,}951{,}424$ |

For small inputs the gain is small. For a million items, presorting makes about $25{,}000$ times fewer comparisons.

*Worked example.* Let $A = (23, 8, 15, 42, 8, 4, 16, 11)$. After the sort, $A = (4, 8, 8, 11, 15, 16, 23, 42)$. The scan compares $4$ with $8$, then $8$ with $8$, and stops: the items are not distinct.

In the [algebraic computation tree](/algebraic-computation-tree/) model, no algorithm does better than $\Omega(n \log n)$ for this problem ([element distinctness lower bound](/element-distinctness-lower-bound/)), so presorting is optimal up to a constant factor in that model. On a [word RAM](/word-ram/) with integer keys, hashing gives $O(n)$ expected time.

### Computing a mode

A *mode* is a value that occurs most often. The brute-force method keeps a list of the distinct values seen so far with their counts, and it searches the list for each new item. When all items are distinct, it makes $0 + 1 + \cdots + (n-1) = n(n-1)/2$ comparisons. With presorting, the template visits the runs and keeps the longest one: $O(n \log n)$ in total.

*Worked example.* Let $A = (5, 1, 5, 7, 6, 5, 7, 1, 7)$. After the sort, $A = (1, 1, 5, 5, 5, 6, 7, 7, 7)$. The runs are $1$ (2 copies), $5$ (3 copies), $6$ (1 copy) and $7$ (3 copies). The largest run length is $3$, and both $5$ and $7$ reach it. If VISIT replaces the best run only when the new run is strictly longer, the answer is $5$, the smallest mode. If it replaces on a tie, the answer is $7$, the largest mode.

### Searching with many queries

To answer $k$ membership queries on $n$ items, sequential search makes up to $kn$ comparisons. Presorting makes one sort and $k$ binary searches, each with at most $\lfloor \lg n \rfloor + 1$ three-way comparisons. For one query, presorting is worse: $\Theta(n \log n)$ instead of $\Theta(n)$. For $n = 10^6$, the worst cases are $kn = 10^6 k$ and $18{,}951{,}425 + 20k$. Presorting wins for $k \ge 19$. For $k = 1000$ queries, the counts are $10^9$ and $18{,}971{,}425$.

### Other examples

- [Remove duplicates](/remove-duplicates-from-sorted-array/): keep the first item of each run.
- [Two sum](/two-sum/): after the sort, two indices move toward each other ([two sum on a sorted array](/two-sum-sorted/)), $O(n \log n)$ in total instead of $\Theta(n^2)$.
- [Intersection of two sets](/sorted-array-intersection/): sort both, then merge them in one pass.

## Variations

- **Sort a copy of the indices.** When the answer must name positions in the input, sort the pairs $(A[i], i)$ instead of the keys. Ties are then broken by the index, and the original positions survive.
- **Sort by a key.** Sort the items by a function of each item, such as a date inside a record. When the key itself is a transformed object, the technique becomes a [reduction to sorting](/reduction-to-sorting/).
- **Integer keys.** For integers in a small range, [counting sort](/counting-sort/) or [radix sort](/radix-sort/) replaces the comparison sort, and the whole method takes linear time.
- **Hashing instead of sorting.** For the questions about equal values, a [hash table](/hash-table/) gives $O(n)$ expected time. It does not give the order of the values, so it cannot answer questions about neighbours in value order.

## Pitfalls

- **Ties in the answer.** A mode, a most frequent pair or a closest pair may not be unique. The scan returns the first or the last one it meets, depending on a strict or non-strict test. Say which one the problem wants, and write the test to match.
- **Lost positions.** After the sort, $A[i]$ is no longer the $i$th item of the input. A problem that asks "the first duplicate in input order" or "the index of each item" needs the indices carried along, and a [stable sort](/stable-sort/) if equal keys must keep their input order.
- **Sorting in place destroys the input.** If the caller needs the original order, sort a copy.
- **One query.** Sorting costs $\Theta(n \log n)$ comparisons in the worst case for a comparison sort ([comparison sort lower bound](/comparison-sort-lower-bound/)). For a single search, sequential search with $n$ comparisons is cheaper.
- **Equality that is not the order's equality.** The scan finds runs of keys equal under the sort's comparison. If two keys compare equal but are different objects (strings compared without case, floating-point $+0$ and $-0$), the runs follow the comparison, not the identity of the objects.

## Exercises

1. Write a presorting algorithm that returns the positions $i < j$ of the first pair of equal items in input order, where "first" means the smallest $j$. Give its cost.
2. Given $n$ real numbers, find the smallest difference between two of them. Show that presorting gives $O(n \log n)$ and explain why only adjacent items in the sorted order need to be compared.
3. For $n = 1000$ items, find the smallest number $k$ of membership queries for which merge sort plus $k$ binary searches makes fewer worst-case comparisons than $k$ sequential searches.
4. Modify the mode algorithm of the template so that it returns all modes. Prove that its cost is still the sort plus $n - 1$ comparisons.
5. Given two sets of size $n$, decide whether they are disjoint in $O(n \log n)$ comparisons.

## References
