---
tag: YQKT8T
kind: algorithm
slug: java-system-sort
name: Java system sort
aliases:
- Arrays.sort
- Collections.sort
area: sorting/comparison-sorts
level: core
summary: The sorting routine in the Java standard library, using a tuned quicksort for primitives and a stable mergesort variant for objects.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n)}
  space: {extra: O(n)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 2009
  people: [Vladimir Yaroslavskiy, Jon Bentley, Joshua Bloch, Tim Peters]
  note: Java 7 (2011) replaced the tuned quicksort of Bentley and McIlroy for primitive arrays by the dual-pivot quicksort that Yaroslavskiy proposed in 2009, and replaced the merge sort for objects by Timsort, the sort that Tim Peters wrote for Python in 2002.
prereqs: [dual-pivot-quicksort, timsort, insertion-sort, stable-sort]
see_also: [introsort, heapsort, bentley-mcilroy-partitioning, merge-sort, natural-merge-sort, quicksort]
sources:
  - paper: "Oracle, Java Platform, Standard Edition API Specification, class java.util.Arrays"
    locator: the notes on the methods sort(int[]) (a dual-pivot quicksort by Yaroslavskiy, Bentley and Bloch) and sort(Object[]) (a stable, adaptive, iterative merge sort adapted from Tim Peters's list sort for Python)
  - paper: doi:10.1002/spe.4380231105
    title: Jon L. Bentley and M. Douglas McIlroy, Engineering a sort function, Software Practice and Experience 23(11) (1993)
    locator: pp. 1249 to 1265 (the tuned quicksort that Java used for primitive arrays up to Java 6)
  - paper: "Sebastian Wild and Markus E. Nebel, Average case analysis of Java 7's dual pivot quicksort, European Symposium on Algorithms (ESA 2012), Lecture Notes in Computer Science 7501"
    locator: pp. 825 to 836 (about 1.9 n ln n comparisons and 0.6 n ln n swaps on average)
  - paper: "Stijn de Gouw, Jurriaan Rot, Frank S. de Boer, Richard Bubel and Reiner Hähnle, OpenJDK's java.utils.Collection.sort() is broken: the good, the bad and the worst case, Computer Aided Verification (CAV 2015), Lecture Notes in Computer Science 9206"
    locator: pp. 273 to 289 (the error in the merge rule of Timsort and the fixed rule)
---

The Java system sort is the pair of sorts behind `java.util.Arrays.sort` and `Collections.sort`. Arrays of a primitive type, such as `int[]` or `double[]`, are sorted by a tuned [dual-pivot quicksort](/dual-pivot-quicksort/) that is not stable, with [insertion sort](/insertion-sort/) for short ranges. Arrays and lists of objects are sorted by [Timsort](/timsort/), a stable merge of natural runs, because the order of equal objects can be seen. The split comes from the two needs: speed and no extra memory for primitive values, where equal values cannot be told apart, and stability for objects. This page describes a model of the two paths that keeps their main steps.

## In plain words

Java has two sorts and picks one by the type of the array. Numbers are just values: two equal numbers look the same, so it does not matter which one comes first. For them, Java uses a fast quicksort that splits the array around two pivots at once into three parts, and switches to insertion sort when a part is short.

Objects can be equal in the sort key but different in other fields, like two people with the same last name. A user who sorts by last name after a sort by first name expects the first sort to show among equal last names. So Java sorts objects with a stable method: it finds the parts of the array that are already in order, makes short ones longer, and merges neighbouring parts in a careful order. On data that is already partly sorted, this is very fast.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). For arrays of objects, the output must also be [stable](/stable-sort/): items with equal keys keep their input order.

## The algorithm

The model has a dual-pivot quicksort for primitive values, in the form of Java 7 and 8, with a fall-back to [heapsort](/heapsort/) when the recursion is too deep, as in [introsort](/introsort/), and the run-merging sort of Timsort for objects, without the galloping mode.

```pseudo id=main
JAVA-SORT(A)
L1  if the items have a primitive type then SORT-PRIMITIVE(A, 0, n − 1, 2⌊lg n⌋ + 4)
L2  else SORT-OBJECTS(A)

SORT-PRIMITIVE(A, lo, hi, depth)                  ▷ dual-pivot quicksort, not stable
L3  if hi − lo < 47 then INSERTION-SORT(A, lo, hi), return
L4  if depth = 0 then HEAPSORT(A, lo, hi), return
L5  sort five sample items, move the 2nd to A[lo] and the 4th to A[hi], p ← A[lo], q ← A[hi]
L6  partition A[lo+1 .. hi−1] into the parts < p, from p to q, and > q
L7  exchange p and q into their places lt and gt between the parts
L8  SORT-PRIMITIVE(A, lo, lt − 1, depth − 1), SORT-PRIMITIVE(A, gt + 1, hi, depth − 1)
L9  if p < q then SORT-PRIMITIVE(A, lt + 1, gt − 1, depth − 1)

SORT-OBJECTS(A)                                   ▷ Timsort without galloping, stable
L10 from left to right, take the next natural run, reverse it if it strictly descends, and extend it to minrun items by binary insertion sort
L11 push the run on a stack of runs, and merge neighbouring runs on the top until the run lengths satisfy the invariants
L12 merge the runs left on the stack, from the top
```

**The primitive path.** Line L5 takes five items spaced about $n/7$ apart around the middle, sorts them, and uses the second and the fourth as the pivots $p \le q$. Line L6 is Yaroslavskiy's partition: an index $k$ runs from the left, items less than $p$ go to the left part, and items greater than $q$ are exchanged with items from the right end. Line L9 skips the middle part when $p = q$, because then it holds only keys equal to $p$. Java 7 and 8 also check for long runs in arrays of at least 286 items and merge them, and use [counting sort](/counting-sort/) for large arrays of bytes, shorts and chars. The model leaves these steps out.

**The object path.** A natural run is a maximal ascending part $A[i] \le A[i+1] \le \cdots$, or a strictly descending part, which line L10 reverses. Strictly descending, because a reversal of equal items would break stability. The minimum run length $minrun$ is between 16 and 32, chosen so that $n / minrun$ is close to a power of 2 from below. For $n < 32$, $minrun = n$, so the whole sort is one binary insertion sort. Line L11 keeps the run lengths $\ldots, X, Y, Z$ on the top of the stack with $X > Y + Z$ and $Y > Z$, the rule of Timsort with the fix of de Gouw et al., which checks the invariant one level deeper. So the lengths grow at least as fast as the Fibonacci numbers from the top down, and the stack has $O(\log n)$ runs.

## Example

Sort an array of the 10 objects $3, 4, 5, 6, 0, 1, 9, 8, 7, 2$, for example `Integer` objects. Since $n < 32$, the object path finds the first run and sorts the rest by binary insertion.

| step | item inserted | its new index | comparisons | items moved | the array |
|---|---|---|---|---|---|
| the first run | | | 4 | | 3 4 5 6 \| 0 1 9 8 7 2 |
| 1 | 0 | 0 | 3 | 4 | 0 3 4 5 6 \| 1 9 8 7 2 |
| 2 | 1 | 1 | 3 | 4 | 0 1 3 4 5 6 \| 9 8 7 2 |
| 3 | 9 | 6 | 2 | 0 | 0 1 3 4 5 6 9 \| 8 7 2 |
| 4 | 8 | 6 | 3 | 1 | 0 1 3 4 5 6 8 9 \| 7 2 |
| 5 | 7 | 6 | 3 | 2 | 0 1 3 4 5 6 7 8 9 \| 2 |
| 6 | 2 | 2 | 3 | 7 | 0 1 2 3 4 5 6 7 8 9 |

The run detection compares neighbours until $0 < 6$ ends the ascending run $3, 4, 5, 6$, with 4 comparisons. Each binary search costs at most $\lceil \lg(m+1) \rceil$ comparisons in a sorted prefix of $m$ items. The run makes 21 comparisons and 18 moves. An `int[]` with the same values takes the primitive path, and since $n < 47$ it is sorted by straight insertion sort.

## Correctness

**The primitive path.** Each step changes $A$ only by exchanges inside $A[lo \ldots hi]$. Line L6 keeps the invariant that $A[lo+1 \ldots lt-1] < p$, $p \le A[lt \ldots k-1] \le q$ and $A[gt+1 \ldots hi-1] > q$. When $k$ passes $gt$, every item is in one of the three parts, and line L7 puts $p$ at index $lt$ and $q$ at index $gt$. So each item left of $lt$ is less than $p$, each item between is from $p$ to $q$, and each item right of $gt$ is greater than $q$. By induction on the length of the range, the three recursive calls sort their parts, and the whole range is sorted. If $p = q$, the middle part has only keys equal to $p$ and is already sorted. Each call is on a shorter range, so the recursion stops, and the depth limit of line L4 stops it after $O(\log n)$ levels in any case.

**The object path.** The stack holds runs that are adjacent, sorted, and cover $A[0 \ldots i-1]$ from left to right. Line L10 adds a sorted run, and each merge replaces two neighbouring sorted runs by one sorted run of the same items. At the end, line L12 leaves one run, which is the whole array. The sort is stable: line L10 reverses only strictly descending runs, binary insertion puts an item after the items equal to it, and the merge takes the item of the left run when two items are equal. Since only neighbouring runs are merged, an item of a run to the left always stays to the left of an equal item of a run to the right.

The full proof is below.

## Complexity

**Primitive path.** Wild and Nebel (2012) show that Java 7's dual-pivot quicksort makes about $1.9\, n \ln n$ comparisons and $0.6\, n \ln n$ swaps on average, against $2 n \ln n$ comparisons and $0.33\, n \ln n$ swaps for classic quicksort. Its speed comes from fewer scans of memory, not from fewer comparisons. Java 7 and 8 have no depth limit, so an input built against them takes $\Theta(n^2)$ time. With the depth limit of the model, the worst case is $O(n \log n)$: each level of recursion costs $O(n)$, there are $O(\log n)$ levels, and the heapsort calls cost $O(n \log n)$ in total. The extra space is the recursion stack, $O(\log n)$.

**Object path.** Each item takes part in $O(\log n)$ merges, because of the stack invariant, so the worst case is $O(n \log n)$ comparisons. If the input has $r$ natural runs, the cost is $O(n + n \log r)$. A sorted or reverse sorted array is one run, found with $n - 1$ comparisons, so the best case is $\Theta(n)$. The model copies the left run of each merge into a buffer, so it uses up to $n$ items of extra space. Java copies the shorter of the two runs, which needs at most $n/2$ items.

## Properties

- **Stable on objects.** The Java specification guarantees it for `Arrays.sort(Object[])` and `Collections.sort`. For primitive values, two equal values are the same value, so the sort cannot show whether it is stable. Floating-point values are the exception in Java: `-0.0` and `0.0` are equal under `<`, and Java orders `-0.0` first.
- **Not in place.** The object path needs a buffer of up to $n/2$ items. The primitive path is in place up to its stack.
- **Adaptive.** The object path is linear on sorted input and fast on inputs with few runs. The primitive path in Java 7 and 8 checks for runs in large arrays.
- **Deterministic.** The pivots are fixed sample positions, not random ones.

## Variants and improvements

- **Java 6 and before.** Primitive arrays used the tuned quicksort of [Bentley and McIlroy](/bentley-mcilroy-partitioning/), with a three-way partition and a pseudomedian of nine as the pivot. Objects used a merge sort with insertion sort below 7 items and a skip of the merge when the two halves were already in order. The system property `java.util.Arrays.useLegacyMergeSort` brought back the old merge sort in Java 7.
- **Later versions.** The dual-pivot quicksort was rewritten in later versions of the JDK, with more steps for small and nearly sorted arrays and a fall-back to heapsort.
- **Parallel sort.** `Arrays.parallelSort`, since Java 8, splits the array into parts, sorts them in parallel, and merges them.
- **Other libraries.** C++ `std::sort` is [introsort](/introsort/), which is quicksort with a fall-back to heapsort, and `std::stable_sort` is a merge sort. Python's `sorted` is Timsort for all items, since Python has no primitive types.

## When to use it

In Java, call `Arrays.sort` or `List.sort`. Write a custom sort only for a special case, such as integer keys with a small range, where [counting sort](/counting-sort/) or [radix sort](/radix-sort/) is faster, or when a fixed worst case is needed on primitive arrays in an old JDK.

## Pitfalls

- **A comparator that is not an order.** Timsort checks some consequences of the contract of `compare`. A comparator that is not transitive, or that returns `a - b` and overflows, can make it throw `IllegalArgumentException: Comparison method violates its general contract`.
- **Expecting stability for a primitive array of keys.** Sorting an `int[]` of keys and then looking up the records loses the link between equal keys and their records. Sort the records, or an index array with the [index sort](/index-sort/) technique.
- **Quadratic inputs.** Inputs built against a fixed pivot rule exist for the dual-pivot quicksort of Java 7 and 8. A service that sorts arrays from untrusted users should not depend on it for its worst case.
- **The old merge rule of Timsort.** The rule of Tim Peters checked the stack invariant only for the top three runs. De Gouw et al. (2015) found inputs where the invariant fails deeper in the stack, and the fixed stack size of the Java code overflowed. The rule in line L11 checks one more level.

## Implementations

## History

Java 1.2 to 6 sorted primitive arrays with the quicksort of Bentley and McIlroy (1993), and objects with a merge sort. Vladimir Yaroslavskiy proposed the dual-pivot quicksort in 2009, and with the help of Jon Bentley and Joshua Bloch it became the sort for primitive arrays in Java 7, released in 2011. Java 7 also replaced the merge sort for objects by Timsort, ported from the list sort that Tim Peters wrote for Python in 2002. In 2015, de Gouw and others found an error in the merge rule of Timsort while they tried to verify the Java code, and the code was fixed.

## References
