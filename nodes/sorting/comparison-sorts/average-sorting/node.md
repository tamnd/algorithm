---
tag: 652RN0
kind: problem
slug: average-sorting
name: Average sorting (k-sorted arrays)
aliases:
- Average sorting
area: sorting/comparison-sorts
level: advanced
summary: Sorting an array that is already nearly sorted in the sense that its averages over windows of k items do not decrease, which holds exactly when A[i] ≤ A[i+k] for each i.
prereqs: [sorting-problem, comparison-sort-lower-bound, binary-heap]
see_also: [h-sorting, shell-sort, adaptive-sorting, presortedness, merging-sorted-lists, heapsort, merge-sort, comparison-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Problem 8-5 (Average sorting), and the exercise of Section 6.5 on merging k sorted lists with a min-heap
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Shellsort (h-ordered sequences, and Theorem K that an h-ordered file stays h-ordered after it is k-sorted)
  - paper: "Vladimir Estivill-Castro and Derick Wood, A survey of adaptive sorting algorithms, ACM Computing Surveys 24(4), 1992"
    locator: the measures Dis and Max, and sorting inputs in which each item is near its final place
---

Average sorting is the problem of putting an array into an order that is sorted "on average over windows of $k$ items", and the related problem of finishing the sort of an array that is already in such an order. An array $A[1 \ldots n]$ is **$k$-sorted** when the mean of each $k$ consecutive items is at most the mean of the next $k$ consecutive items. This holds exactly when $A[i] \le A[i+k]$ for each $i$, so a $k$-sorted array is the same thing as a $k$-ordered array in [Shell sort](/shell-sort/). The costs of both problems follow from a counting argument: $\Theta(n \log(n/k))$ comparisons to make an array $k$-sorted, and $\Theta(n \log k)$ comparisons to sort an array that is $k$-sorted already. The problem is CLRS Problem 8-5.

## In plain words

Take a row of numbers and slide a window of $k$ numbers along it. If the average inside the window never goes down as the window moves right, the row is $k$-sorted. For $k = 1$ the window holds one number, and this is the same as sorted.

There is a simpler test. When the window moves one step, one number leaves on the left and one enters on the right. The average does not go down exactly when the number that enters is at least the number that leaves. So the row is $k$-sorted when each number is at most the number $k$ places to its right.

So the row splits into $k$ separate sorted lists, which are mixed together like dealt cards. To make the row $k$-sorted, sort each of the $k$ lists. To sort a $k$-sorted row, merge the $k$ lists.

## Definition

Let $A[1 \ldots n]$ be an array of numbers, and let $1 \le k \le n$. The array is **$k$-sorted** when

$$\frac{1}{k} \sum_{j=i}^{i+k-1} A[j] \;\le\; \frac{1}{k} \sum_{j=i+1}^{i+k} A[j] \qquad \text{for } i = 1, 2, \ldots, n - k.$$

**Equivalent form.** The two sums share the items $A[i+1 \ldots i+k-1]$, and their difference is $A[i+k] - A[i]$. So the array is $k$-sorted if and only if

$$A[i] \le A[i + k] \qquad \text{for } i = 1, 2, \ldots, n - k.$$

This form uses only comparisons, so it makes sense for keys from any total order, not only for numbers. Split the positions into the $k$ residue classes $C_r = \{r, r + k, r + 2k, \ldots\}$ for $r = 1, \ldots, k$. The array is $k$-sorted exactly when the items in each class are sorted. A 1-sorted array is a sorted array, and each array is $n$-sorted.

There are two problems:

- **$k$-sorting.** Input: an array $A$ and $k$. Output: a permutation of $A$ that is $k$-sorted.
- **Sorting a $k$-sorted array.** Input: a $k$-sorted array $A$ and $k$. Output: $A$ in sorted order.

## Variants

- **Each item within $k$ places of its final place.** A different notion of "nearly sorted", with $|i - \mathrm{rank}(A[i])| \le k$ for each $i$. It is the measure $\mathrm{Max}$ of [presortedness](/presortedness/). Such an array is not always $k$-sorted, and a $k$-sorted array can have items far from their final places. It too can be sorted in $O(n \log k)$ time: keep the next $k + 1$ items in a [min-heap](/binary-heap/), and output the minimum each time a new item enters, because the smallest remaining item is always among the next $k + 1$.
- **A sequence of $k$ values.** [Shell sort](/shell-sort/) makes the array $h$-sorted for a decreasing sequence of gaps $h$, ending with $h = 1$. Each step is $h$-sorting in the sense of this page, done by insertion sort on each class; see [h-sorting](/h-sorting/).
- **Other measures of disorder.** [Adaptive sorting](/adaptive-sorting/) studies sorts whose cost depends on the number of inversions, runs or other measures. The $k$-sorted condition is a measure of this kind, with a value of 1 for sorted input.

## Examples

**A 2-sorted array that is not sorted.** $A = [1, 6, 2, 7, 3, 8, 4, 9, 5, 10]$. The odd positions hold $1, 2, 3, 4, 5$ and the even positions hold $6, 7, 8, 9, 10$, both sorted, so $A[i] \le A[i+2]$ for each $i$. The averages of the windows of 2 items are $3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5$, which do not decrease. The item 6 is 4 places from its final place, so the array is 2-sorted although it is not "within 2 places" of sorted.

**3-sorting.** Let $A = [9, 4, 7, 1, 8, 2, 6, 10, 3, 5]$ and $k = 3$. The classes of positions are $\{1, 4, 7, 10\}$, $\{2, 5, 8\}$ and $\{3, 6, 9\}$, which hold $9, 1, 6, 5$ and $4, 8, 10$ and $7, 2, 3$. Sort each class in its own positions:

| position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| input | 9 | 4 | 7 | 1 | 8 | 2 | 6 | 10 | 3 | 5 |
| 3-sorted | 1 | 4 | 2 | 5 | 8 | 3 | 6 | 10 | 7 | 9 |

The sums of the windows of 3 items in the result are $7, 11, 15, 16, 17, 19, 23, 26$, which do not decrease. Merging the three sorted classes $1, 5, 6, 9$ and $4, 8, 10$ and $2, 3, 7$ then gives $1, 2, \ldots, 10$.

**Counts.** For $n = 8$ and $k = 3$, exactly 560 of the $8! = 40{,}320$ permutations are 3-sorted. This is $8! / (3! \, 3! \, 2!)$, the number of ways to choose which keys go into each class. The same holds for each $n$ and $k$ that was checked by brute force: $(6, 2)$ gives 20, $(7, 3)$ gives 210, and $(8, 2)$ gives 70.

## Known algorithms

- **$k$-sorting by sorting each class.** Sort the items of each class $C_r$ with an $O(m \log m)$ sort, such as [merge sort](/merge-sort/) or [heapsort](/heapsort/) on a strided view of the array. The classes have at most $\lceil n/k \rceil$ items, so the time is $O(k \cdot (n/k) \log(n/k)) = O(n \log(n/k))$ for $k < n$, and $O(n)$ when $k$ is close to $n$. Heapsort on a strided view does it in place.
- **Sorting a $k$-sorted array by a $k$-way merge.** The classes are $k$ sorted lists. Put the first item of each list in a min-heap of size $k$, and repeat: extract the minimum, output it, and insert the next item of its list. Each of the $n$ steps costs $O(\log k)$, so the time is $O(n \log k)$, with $\Theta(n)$ extra space for the output. See [merging sorted lists](/merging-sorted-lists/).
- **Insertion sort.** Insertion sort on each class makes an array $k$-sorted in $O(n^2/k)$ time, as in one pass of Shell sort. On a $k$-sorted array, plain insertion sort can still take $\Theta(n^2)$ time: the 2-sorted array with $1, \ldots, n/2$ in the odd positions and $n/2 + 1, \ldots, n$ in the even positions has about $n^2/8$ inversions.

With $n = 100{,}000$ random keys, sorting the $k$ classes with Python's sort and then merging them with a heap gave these comparison counts:

| $k$ | $k$-sorting | lower bound $\lg((n/k)!^k)$ | merging the $k$ classes | lower bound $\lg$ of the multinomial |
|---|---|---|---|---|
| 2 | 1,431,896 | 1,416,713 | 99,999 | 99,991 |
| 16 | 1,131,857 | 1,116,817 | 476,141 | 399,888 |
| 256 | 732,364 | 718,136 | 896,636 | 798,568 |

## Bounds

Let the keys be distinct, and let $k$ divide $n$ to keep the formulas short. The number of $k$-sorted permutations is the multinomial coefficient

$$S(n, k) = \frac{n!}{\big((n/k)!\big)^k},$$

because a $k$-sorted arrangement is fixed by the choice of which keys go into each class.

**Making an array $k$-sorted takes $\Omega(n \log(n/k))$ comparisons.** Take a [decision tree](/decision-tree-model/) for $k$-sorting. At each leaf the algorithm applies a fixed rearrangement to the input. For a fixed rearrangement $\pi$, the inputs that $\pi$ turns into a $k$-sorted array are the inputs $\pi^{-1}(B)$ for the $S(n, k)$ $k$-sorted arrangements $B$. So each leaf serves at most $S(n, k)$ of the $n!$ inputs, and the tree has at least $n! / S(n, k) = ((n/k)!)^k$ leaves. Its height is at least

$$\lg \big((n/k)!\big)^k = k \lg (n/k)! = n \lg (n/k) - O(n).$$

For a constant $k$ this is $\Omega(n \log n)$, so $k$-sorting is as hard as sorting. The bound matches the algorithm that sorts each class.

**Sorting a $k$-sorted array takes $\Omega(n \log k)$ comparisons.** A decision tree that sorts each $k$-sorted input must reach a different leaf for each of the $S(n, k)$ inputs, so its height is at least

$$\lg S(n, k) = \lg n! - k \lg (n/k)! = n \lg k - O(k \log (n/k)),$$

by Stirling's formula. For $k \le n / 2$ this is $\Omega(n \log k)$, and it matches the $k$-way merge.

The two bounds add up to the bound for sorting: $n \lg(n/k) + n \lg k = n \lg n$. Making an array $k$-sorted and then merging the classes is a full sort, and neither step can be done more cheaply than its share of $\lg n!$.

**The variant with displacement at most $k$.** Cut the positions into blocks of $k$ and permute each block in any way. Each item then stays fewer than $k$ places from its final place, so there are at least $(k!)^{\lfloor n/k \rfloor}$ such inputs, and sorting them takes at least $\lfloor n/k \rfloor \lg k! = n \lg k - O(n)$ comparisons. The heap of $k + 1$ items meets this bound.

## Reductions

- **Sorting reduces to $k$-sorting plus merging.** Any sort of an array can be done by first $k$-sorting it and then sorting the $k$-sorted result. The bounds above show that the work splits as $n \lg (n/k)$ and $n \lg k$.
- **$k$-sorting is sorting of $k$ independent arrays.** The $k$ classes do not interact, so $k$-sorting is $k$ instances of the [sorting problem](/sorting-problem/) of size $n/k$, and any sort can be used on each one.
- **Sorting a $k$-sorted array is $k$-way merging.** The $k$ classes are exactly $k$ sorted lists, and each $k$-way merge of sorted lists of length $n/k$ is the sort of a $k$-sorted array, by dealing the lists into the classes.

## Applications

- **Shell sort.** The passes of [Shell sort](/shell-sort/) are $h$-sorting steps, and its analysis uses the fact that an $h$-sorted array stays $h$-sorted after it is $k$-sorted (Knuth, Theorem K in Section 5.2.1).
- **Teaching lower bounds.** The problem shows how to use the [decision tree](/decision-tree-model/) argument for a task whose output is not unique: count how many inputs one leaf can serve, not how many outputs there are.
- **Interleaved sorted streams.** Data that comes from $k$ sources in turn, each source in sorted order, is $k$-sorted, and a $k$-way merge with a heap sorts it in $O(n \log k)$ time.

## References
