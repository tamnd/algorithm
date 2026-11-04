---
tag: 9P1Q2T
kind: model
slug: comparison-cost-model
name: Comparison and exchange cost model for sorting
aliases:
- Sorting cost model
area: sorting/comparison-sorts
level: intro
summary: Analyzes sorting algorithms by counting key comparisons and exchanges, as the main operations that determine running time.
prereqs: [comparison-model, comparison-sort, asymptotic-notation]
see_also: [comparison-sort-lower-bound, inversion, permutation-cycles, unit-cost-model, external-memory-model, cycle-sort, selection-sort]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.1, Elementary Sorts (the sorting cost model, compares and exchanges, and the propositions for selection sort and insertion sort); Sections 2.2 to 2.4 for mergesort, quicksort and heapsort
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Chapter 5 introduction and Section 5.2 (the analysis of each method by its number of comparisons and of record moves), Section 5.1.1 (inversions) and Section 5.2.8 (comparison of the methods)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2 (analyzing algorithms in the RAM model) and Section 8.1 (comparisons as the cost of a comparison sort)
---

The comparison and exchange cost model measures a sorting algorithm by two numbers: the number of key comparisons and the number of exchanges (or of item moves) that it makes. It is the usual model to compare [comparison sorts](/comparison-sort/) with each other. It refines the [comparison model](/comparison-model/), which counts comparisons only, and it is coarser than the [unit-cost model](/unit-cost-model/), which counts each step of the program.

## The machine

The input is an array $A[0 \ldots n-1]$ of $n$ items, each with a key from a set with a total order. The algorithm works on the array through these operations:

- **compare$(i, j)$:** return the result of $A[i] < A[j]$, or of a three-way comparison of the two keys. The algorithm can also compare a key in a temporary variable with $A[i]$.
- **exchange$(i, j)$:** swap $A[i]$ and $A[j]$.
- **move:** copy one item from the array to a temporary variable, from a temporary variable to the array, or from one place of the array to another. An exchange is three moves.

Each comparison costs one unit in the first count, and each exchange (or each move) costs one unit in the second count. Work on indices, counters, loop control and the call stack is not counted. The keys are opaque: the only operation that looks at a key is a comparison.

An algorithm has a cost pair $(C(I), X(I))$ for each input $I$, where $C$ is the number of comparisons and $X$ is the number of exchanges. For an algorithm that moves items without exchanges, such as [merge sort](/merge-sort/) or [insertion sort](/insertion-sort/) with shifts, $X$ is replaced by the number of moves $M$, or by the number of array accesses.

## What it counts

The model counts $C$ and $X$ (or $M$) in the worst case, in the best case and on average. For the average, the input is a uniformly [random permutation](/random-permutation/) of $n$ distinct keys unless the statement says otherwise.

The model is useful because, for most sorts, the running time on a real machine is close to $a \cdot C + b \cdot X + (\text{lower-order terms})$ for constants $a$ and $b$ that depend on the machine and on the items. The ratio of $a$ to $b$ changes with the items:

- When the keys are machine integers in an array, a comparison and an exchange each cost a few instructions, and the cost of the loop around them matters as much.
- When a comparison calls a user function, for example to compare two strings, $a$ is much larger than $b$. Then $C$ is the right measure. This is why the library sorts of Python and of Java for objects, which use [Timsort](/timsort/), try to make few comparisons.
- When the items are large records and are moved in place, $b$ is much larger than $a$. Then $X$ or $M$ is the right measure, and an [index sort](/index-sort/) that moves pointers instead of records can help.
- When writes are expensive, as on flash memory, the number of writes to the array matters on its own. [Cycle sort](/cycle-sort/) makes the fewest writes.

The model does not count the cost of memory access. Two sorts with the same $C$ and $X$ can differ much in time because one reads the array in order and the other jumps around it.

## Relation to other models

- **[Comparison model](/comparison-model/).** It keeps only $C$. All its lower bounds hold here for $C$. The comparison model allows any amount of free data movement, so it says nothing about $X$.
- **[Unit-cost model](/unit-cost-model/) of the [random access machine](/random-access-machine/).** It counts each instruction. For a comparison sort on a RAM, the running time is at least $C + X$ and is $O(C + X + \text{loop overhead})$. For most sorts the loop overhead is $O(C + X + n)$, so the two models give the same $\Theta$ bound.
- **[External memory model](/external-memory-model/).** It counts transfers of blocks between a fast memory and a slow memory, not comparisons. Merge sort and heapsort have about the same $C$, but merge sort makes far fewer block transfers.
- **[Word RAM](/word-ram/).** It allows arithmetic on the keys, so it is not bound by the comparison lower bound. The comparison and exchange model does not apply to [radix sort](/radix-sort/) or to [counting sort](/counting-sort/).

## Known results in the model

### Lower bounds

**Comparisons.** Each comparison sort makes at least $\lceil \lg(n!) \rceil$ comparisons on some input of $n$ distinct keys, and at least $\lg(n!)$ on average. See the [comparison sort lower bound](/comparison-sort-lower-bound/).

**Exchanges of any two items.** Let $\pi$ be the permutation that the input is, and let $c(\pi)$ be the number of cycles of $\pi$, with fixed points counted as cycles. Then each algorithm that sorts by exchanges makes at least $n - c(\pi)$ exchanges on $\pi$, and $n - c(\pi)$ exchanges are enough.

*Proof.* Let $\sigma$ be the current arrangement, as a permutation. An exchange of two positions in the same cycle of $\sigma$ splits that cycle into two, and an exchange of two positions in different cycles joins them into one. So each exchange changes the number of cycles by exactly 1. The sorted array is the identity, with $n$ cycles. So at least $n - c(\pi)$ exchanges are necessary. For the upper bound, while some item is not at its place, exchange it with the item at its place. This puts at least one item at its place and splits its cycle, so it adds one cycle each time. $\square$

The worst case is $n - 1$, for a permutation with one cycle. On a random permutation the expected number of cycles is the harmonic number $H_n = \sum_{k=1}^{n} 1/k$, so the expected minimum is $n - H_n$. See [permutation cycles](/permutation-cycles/).

**Exchanges of adjacent items.** Each exchange of two adjacent items changes the number of [inversions](/inversion/) by exactly 1. So a sort that exchanges only adjacent items, such as [bubble sort](/bubble-sort/), [insertion sort](/insertion-sort/) and [gnome sort](/gnome-sort/), makes at least $\operatorname{inv}(\pi)$ exchanges, which is $n(n-1)/2$ in the worst case and $n(n-1)/4$ on average. Each of these three sorts makes exactly $\operatorname{inv}(\pi)$ exchanges.

### Costs of the standard sorts

The table gives the leading terms on a random permutation of $n$ distinct keys, with the worst case after the slash where it differs. Here $\sim$ means that the ratio tends to 1.

| sort | comparisons | exchanges or moves |
|---|---|---|
| [selection sort](/selection-sort/) | $n(n-1)/2$ on each input | $n - 1$ exchanges on each input |
| [insertion sort](/insertion-sort/) | $\sim n^2/4$ / $\sim n^2/2$ | $\sim n^2/4$ / $\sim n^2/2$ |
| [bubble sort](/bubble-sort/) | $\sim n^2/2$ / $n(n-1)/2$ | $\sim n^2/4$ / $n(n-1)/2$ exchanges |
| [merge sort](/merge-sort/) | $\sim n \lg n$ / at most $n \lceil \lg n \rceil$ | $\Theta(n \log n)$ moves on each input |
| [quicksort](/quicksort/), first key as pivot | $\sim 2 n \ln n \approx 1.39\, n \lg n$ / $\sim n^2/2$ | $\sim \tfrac13 n \ln n$ exchanges |
| [heapsort](/heapsort/) | $\sim 2 n \lg n$ / at most $2 n \lg n + O(n)$ | $\sim n \lg n$ exchanges |
| [cycle sort](/cycle-sort/) | $\Theta(n^2)$ on each input | at most $n$ writes, and $n - (\text{fixed points})$ is the least possible |

For $n = 1000$, the mean over 20 random permutations was 499,500 comparisons and 1,000 exchanges for selection sort, 252,304 comparisons and 251,311 exchanges for insertion sort, 497,943 comparisons and 246,787 exchanges for bubble sort with an early stop, 8,709 comparisons for merge sort, 12,162 comparisons and 2,390 exchanges for quicksort with Sedgewick's partition, and 16,850 comparisons and 9,076 exchanges for heapsort. The reference values are $n^2/4 = 250{,}000$, $n \lg n \approx 9{,}966$, $2 n \ln n \approx 13{,}816$, $\tfrac13 n \ln n \approx 2{,}303$ and $2 n \lg n \approx 19{,}932$. The lower-order terms explain the gaps at this size.

The table shows the trade-offs that the model makes visible. Selection sort makes the most comparisons and the fewest exchanges of the quadratic sorts. Insertion sort makes about half the comparisons of selection sort, but $\Theta(n^2)$ moves. Quicksort makes more comparisons than merge sort and heapsort, but few exchanges and cheap ones, which is one reason why it is fast in practice.

### Pitfalls

- **One count is not the time.** Binary insertion sort makes $n \lg n + O(n)$ comparisons, but $\Theta(n^2)$ moves in the worst case. A claim of "$O(n \log n)$" from $C$ alone is wrong for it.
- **Exchanges and moves are different units.** An exchange is three moves. Insertion sort with shifts makes about one move per inversion, and with swaps about three. Say which unit a count uses.
- **The average depends on the input distribution.** The averages in the table are for random permutations of distinct keys. With many equal keys, or with partly sorted inputs, the counts change, and some sorts (for example quicksort with the [Lomuto partition](/lomuto-partition/)) become quadratic on all-equal keys.

## References
