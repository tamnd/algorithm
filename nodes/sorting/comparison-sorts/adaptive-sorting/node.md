---
tag: W64ANZ
kind: concept
slug: adaptive-sorting
name: Adaptive sorting
aliases:
- presortedness
area: sorting/comparison-sorts
level: advanced
summary: A sort whose running time improves when the input is already partly ordered, measured by measures of presortedness.
prereqs: [comparison-sort, comparison-sort-lower-bound, inversion]
see_also: [presortedness, insertion-sort, natural-merge-sort, timsort, smoothsort, average-sorting, splay-tree, finger-search-tree]
sources:
  - paper: doi:10.1145/146370.146381
    title: Vladimir Estivill-Castro and Derick Wood, A survey of adaptive sorting algorithms, ACM Computing Surveys 24(4), 1992
    locator: pp. 441 to 476 (the measures of presortedness, the definition of optimality with respect to a measure, and the optimal algorithms for each measure)
  - paper: doi:10.1109/TC.1985.5009382
    title: Heikki Mannila, Measures of presortedness and optimal sorting algorithms, IEEE Transactions on Computers C-34(4), 1985
    locator: pp. 318 to 325 (the axioms for a measure of presortedness, the lower bound from the number of permutations with small disorder, and local insertion sort)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversions and their distribution) and Section 5.2.4 (natural merge sort and runs)
  - paper: "Alistair Moffat, Gary Eddy and Ola Petersson, Splaysort: fast, versatile, practical, Software: Practice and Experience 26(7), 1996"
    locator: the experiments on nearly sorted inputs
---

A sort is adaptive when it uses fewer comparisons, or less time, on inputs that are already partly in order. To make this precise, one fixes a **measure of presortedness** $M$, such as the number of [inversions](/inversion/) or the number of [sorted runs](/sorted-run/), and asks for a running time that is a function of both $n$ and $M(X)$. A sort is **optimal with respect to $M$** when its number of comparisons matches, up to a constant factor, the information-theoretic lower bound for the inputs whose disorder is at most $M(X)$. [Insertion sort](/insertion-sort/) and [natural merge sort](/natural-merge-sort/) are the simplest adaptive sorts, and [Timsort](/timsort/) is the adaptive sort that most libraries use. The measures themselves are the topic of [presortedness](/presortedness/); this page is about what it means for a sort to adapt to them.

## In plain words

Most real lists are not in a random order. A list of records may be sorted already, apart from a few new records at the end. A list may be two sorted lists, one after the other.

A sort that ignores this does the same work on a sorted list as on a shuffled one. An adaptive sort notices the order that is already there and does less work.

To say how much less, choose a way to count the disorder: for example, the number of pairs that are in the wrong order, or the number of sorted stretches. A good adaptive sort does little work when the count is small, and never much more work than an ordinary fast sort when the count is large. The best ones do only as much work as the count forces any sort to do.

## The idea

**Measures of presortedness.** A measure $M$ maps each sequence $X = x_1, \ldots, x_n$ of distinct keys to a non-negative integer, with $M(X) = 0$ when $X$ is sorted, and depends only on the relative order of the keys. Mannila (1985) gave a short list of axioms for such a measure. The common ones are:

- $\mathrm{Inv}(X)$, the number of [inversions](/inversion/): pairs $i < j$ with $x_i > x_j$. It is between $0$ and $\binom{n}{2}$.
- $\mathrm{Runs}(X)$, the number of step-downs: positions $i$ with $x_{i+1} < x_i$. The input then has $\mathrm{Runs}(X) + 1$ maximal ascending runs.
- $\mathrm{Rem}(X)$, the least number of items to remove to leave a sorted sequence: $n$ minus the length of a longest increasing subsequence.
- $\mathrm{Exc}(X)$, the least number of exchanges that sort $X$: $n$ minus the number of cycles of the permutation that sorts it.
- $\mathrm{Dis}(X)$, the largest distance $j - i$ of an inverted pair, and $\mathrm{Max}(X)$, the largest distance $|i - \mathrm{rank}(x_i)|$ of an item from its final place. An input with $\mathrm{Max}(X) \le k$ is a $k$-sorted array, the topic of [average sorting](/average-sorting/).

These measures disagree. One sequence can be close to sorted for one measure and far from it for another, so a sort can adapt to one measure and not to another.

**The lower bound for a measure.** Fix $M$, $n$ and a value $k$, and let $\mathrm{below}_M(n, k)$ be the set of permutations of $n$ keys with $M \le k$. A comparison sort that must sort each of these inputs is a [decision tree](/decision-tree-model/) with at least $|\mathrm{below}_M(n, k)|$ leaves. So by the argument of the [comparison sort lower bound](/comparison-sort-lower-bound/), its worst case on this set is at least $\lg |\mathrm{below}_M(n, k)|$ comparisons. It must also read each key, which costs $\Omega(n)$ for any $k$, because a test of sortedness needs $n - 1$ comparisons. A sort is **$M$-optimal** when on each input $X$ it makes

$$O\big(n + \lg |\mathrm{below}_M(n, M(X))|\big)$$

comparisons. This is the definition of Mannila (1985) and of Estivill-Castro and Wood (1992). For a random input, $M(X)$ is near its largest value, the set is close to all $n!$ permutations, and the bound is $\Theta(n \log n)$, so an $M$-optimal sort is also optimal in the usual worst-case sense.

**The bounds for the common measures.** Counting the permutations in each set gives these lower bounds, and for each of them there is a sort that meets it (Estivill-Castro and Wood, 1992):

| measure | optimal number of comparisons |
|---|---|
| $\mathrm{Inv}$ | $\Theta\big(n + n \log(1 + \mathrm{Inv}/n)\big)$ |
| $\mathrm{Runs}$ | $\Theta\big(n + n \log(1 + \mathrm{Runs})\big)$ |
| $\mathrm{Rem}$ | $\Theta\big(n + \mathrm{Rem} \log(1 + \mathrm{Rem})\big)$ |
| $\mathrm{Exc}$ | $\Theta\big(n + \mathrm{Exc} \log(1 + \mathrm{Exc})\big)$ |
| $\mathrm{Dis}$ and $\mathrm{Max}$ | $\Theta\big(n + n \log(1 + \mathrm{Dis})\big)$ |

The table shows the shape of the result: a sort that adapts to $\mathrm{Inv}$ makes $O(n)$ comparisons when $\mathrm{Inv} = O(n)$, and still $O(n \log n)$ when $\mathrm{Inv}$ is near $n^2/2$.

**Adaptive is weaker than optimal.** [Insertion sort](/insertion-sort/) makes at most $n - 1 + \mathrm{Inv}(X)$ comparisons, so it adapts to $\mathrm{Inv}$: it is linear when $\mathrm{Inv} = O(n)$. It is not $\mathrm{Inv}$-optimal, because at $\mathrm{Inv} = n^{1.5}$ it makes $\Theta(n^{1.5})$ comparisons, while the bound is $\Theta(n \log n)$. Mannila's local insertion sort inserts each key with a search that starts from the last key inserted, in a [finger search tree](/finger-search-tree/), and so reaches the bound for $\mathrm{Inv}$.

## Examples

**The measures on five inputs.** For $n = 8$:

| $X$ | Inv | Runs | Rem | Exc | Dis | Max |
|---|---|---|---|---|---|---|
| 1 2 3 4 5 6 8 7 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 1 4 3 6 5 8 7 | 4 | 4 | 4 | 4 | 1 | 1 |
| 5 6 7 8 1 2 3 4 | 16 | 1 | 4 | 4 | 7 | 4 |
| 8 1 2 3 4 5 6 7 | 7 | 1 | 1 | 7 | 7 | 7 |
| 2 3 4 5 6 7 8 1 | 7 | 1 | 1 | 7 | 7 | 7 |

The second input has many step-downs, but each key is only one place from home. The third input is two sorted runs, but it has 16 of the 28 possible inversions. The last two inputs need only one key moved, so $\mathrm{Rem} = 1$, but the sorting permutation is one cycle of length 8, so $\mathrm{Exc} = 7$.

**Two sorts on the second and third inputs.** Insertion sort, which adapts to $\mathrm{Inv}$, and natural merge sort, which adapts to $\mathrm{Runs}$, prefer different inputs:

| $X$ | insertion sort comparisons | natural merge sort comparisons |
|---|---|---|
| 2 1 4 3 6 5 8 7 | 10 | 23 |
| 5 6 7 8 1 2 3 4 | 22 | 11 |

Natural merge sort here scans for runs with $n - 1 = 7$ comparisons and then merges pairs of runs from left to right.

**Larger inputs.** With $n = 10{,}000$ random keys, the same two sorts gave these counts of comparisons:

| input | insertion sort | natural merge sort |
|---|---|---|
| sorted | 9,999 | 9,999 |
| 10 random swaps of neighbours | 10,009 | 27,276 |
| 1,000 random swaps of neighbours | 10,911 | 63,347 |
| two sorted runs of 5,000 | 12,362,641 | 19,998 |
| 64 sorted runs | not run | 69,768 |

Each swap of neighbours adds at most one inversion, so insertion sort stays near $n$. The same swaps cut the runs into many short runs, so natural merge sort loses most of its advantage. On two runs the roles change: about $n^2/8$ inversions for insertion sort, and one merge for natural merge sort. With 64 runs, natural merge sort is near $n + n \lg 64 = 70{,}000$.

**The size of the sets.** For $n = 8$ there are $8! = 40{,}320$ permutations, and $\lg 8! \approx 15.3$. Only 285 of them have $\mathrm{Inv} \le 4$, and $\lg 285 \approx 8.2$. So on these inputs an $\mathrm{Inv}$-optimal sort needs about 8 comparisons beyond the cost of reading the input, and no sort can promise fewer in the worst case over this set.

## Where it is used

- **Library sorts.** [Timsort](/timsort/) finds the runs of the input and merges them with a stack discipline. It makes $O(n + n \log(1 + \mathrm{Runs}))$ comparisons and is used by Python and by Java for objects. Powersort, the merge policy of Python since version 3.11, is close to optimal for a finer measure that also counts the lengths of the runs.
- **Small and nearly sorted arrays.** Hybrid sorts call [insertion sort](/insertion-sort/) on short ranges, and on data where each new key is close to its place, because its cost is $n - 1 + \mathrm{Inv}$.
- **Data with local disorder.** Records that arrive with small delays, such as time-stamped events, are $k$-sorted for a small $k$. A heap of $k + 1$ items sorts them in $O(n \log k)$ time; see [average sorting](/average-sorting/).
- **In-place adaptive sorts.** [Smoothsort](/smoothsort/) is an in-place heap sort that takes $O(n)$ time on sorted input and $O(n \log n)$ in the worst case. Splaysort inserts the keys into a [splay tree](/splay-tree/) and reads them back in order. Moffat, Eddy and Petersson (1996) found it fast in practice on several kinds of nearly sorted input.
- **Theory.** The [Cartesian tree](/cartesian-tree/) sort of Levcopoulos and Petersson, and the many sorts in the survey of Estivill-Castro and Wood (1992), show that one sort can be optimal for several measures together. Each measure gives a lower bound by the same counting argument, so adaptive sorting is also a source of instance-sensitive lower bounds.

## References
