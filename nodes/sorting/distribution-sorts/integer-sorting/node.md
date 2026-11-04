---
tag: 1HN3MR
kind: problem
slug: integer-sorting
name: Integer sorting
aliases:
- Sorting integers
- Sorting keys from a bounded universe
area: sorting/distribution-sorts
level: core
summary: Sort n keys drawn from a bounded integer range, where the range enables faster-than-comparison sorting.
model: word-ram
complexity:
  vars: {n: the number of keys, w: the word length in bits, U: the size of the key universe}
  time: {worst: O(n log log n)}
prereqs: [sorting-problem, word-ram]
see_also: [counting-sort, radix-sort, comparison-sort-lower-bound, fusion-tree, han-integer-sort, han-thorup-integer-sort, priority-queue, string-sorting]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Sorting in Linear Time (Section 8.2, Counting sort, and Section 8.3, Radix sort, with Lemma 8.4 on the choice of the digit size)
  - paper: doi:10.1006/jcss.1998.1580
    title: Arne Andersson, Torben Hagerup, Stefan Nilsson and Rajeev Raman, Sorting in linear time?, Journal of Computer and System Sciences 57(1), 1998, pages 74 to 93
    locator: the introduction (the survey of earlier bounds) and the sections on signature sort and on packed sorting
  - paper: doi:10.1016/j.jalgor.2003.09.001
    title: Yijie Han, Deterministic sorting in O(n log log n) time and linear space, Journal of Algorithms 50(1), 2004, pages 96 to 105
    locator: the main theorem (deterministic O(n log log n) time and linear space on the word RAM) and the introduction (the history of the problem)
---

Integer sorting is the problem of sorting $n$ keys that are integers in a bounded universe $\{0, 1, \ldots, U - 1\}$, on a machine that can compute with the keys and not only compare them. The usual model is the [word RAM](/word-ram/) with words of $w \ge \lg n$ bits and $U \le 2^w$. Because an algorithm can use a key as an array index or split it into digits, the $\Omega(n \log n)$ [comparison lower bound](/comparison-sort-lower-bound/) does not apply, and the best known deterministic bound is $O(n \log \log n)$. Whether $O(n)$ time is possible for every word length is an open problem.

## In plain words

You must put a list of whole numbers in order, and you know that each number fits in one machine word. A sort that only compares two numbers at a time needs a number of steps that grows a bit faster than the length of the list. But whole numbers give more help: you can use a number as the address of a box, or look at its digits one by one.

If the numbers are small, you count how often each value occurs and write the values out in order. If the numbers are large, you sort them by one group of digits at a time. These methods are faster than comparison sorts on large lists of small or medium numbers. For very large numbers, researchers have found cleverer methods, but nobody knows yet if a sort can always be as fast as reading the list.

## Definition

**Input.** A sequence $a_1, \ldots, a_n$ of keys with $a_i \in \{0, \ldots, U - 1\}$, each key possibly with satellite data. Each key fits in one word: $U \le 2^w$. The word length satisfies $w \ge \lg n$, so that an index into the input also fits in one word.

**Output.** The keys in non-decreasing order, as in the [sorting problem](/sorting-problem/). A *stable* integer sort keeps equal keys in their input order.

**Model.** The [word RAM](/word-ram/) has constant-time addition, subtraction, comparison, bitwise operations, shifts and indirect addressing on $w$-bit words. Some results also use multiplication, and some use only the operations of the circuit class $\mathrm{AC}^0$. Time is the number of word operations, and space is the number of words.

Signed integers, fixed-point numbers and IEEE floating-point numbers reduce to this problem: a fixed map of the bit pattern sends them to unsigned integers in the same order (for [IEEE 754](/ieee-754/) numbers, flip the sign bit of a positive number and all bits of a negative number).

## Variants

- **Small universe, $U = O(n)$.** [Counting sort](/counting-sort/) solves it in $\Theta(n + U)$ time, which is linear.
- **Polynomial universe, $U = n^{O(1)}$.** [Radix sort](/radix-sort/) with base $n$ makes $O(1)$ passes, each in $O(n)$ time, so the total is linear.
- **General universe, $U = 2^w$.** The hard case. The cost depends on $w$, and the bounds below are stated for each $w$.
- **Deterministic or randomized.** Randomized algorithms use hashing and give bounds on the expected time.
- **Linear space.** Some fast methods use space that grows with $U$ or with $2^{w^\varepsilon}$. A linear-space bound uses $O(n)$ words.
- **Strings and multi-word keys.** Keys longer than a word lead to [string sorting](/string-sorting/).

## Examples

**Small universe.** For the keys $3, 1, 4, 1, 5, 9, 2, 6$ with $U = 10$, the counts of the values $0, \ldots, 9$ are $0, 2, 1, 1, 1, 1, 1, 0, 0, 1$. Reading the values out by their counts gives $1, 1, 2, 3, 4, 5, 6, 9$. No two keys were compared.

**A choice of digit size.** For $n = 10^6$ keys of 32 bits, radix sort with 16-bit digits makes 2 passes, each with about $n + 2^{16}$ steps, about $2.13 \cdot 10^6$ in total. With 8-bit digits it makes 4 passes of about $n + 2^8$ steps, about $4.00 \cdot 10^6$ in total. A comparison sort needs about $n \lg n \approx 1.99 \cdot 10^7$ comparisons for the same input.

**Where radix sort loses.** For $n = 1000$ keys of 64 bits, the best digit size gives about $10^4$ steps, the same order as $n \lg n \approx 9966$. When $w$ is large compared with $\lg n$, radix sort with digits of $\lg n$ bits costs $\Theta(n w / \log n)$ and is no longer linear.

## Known algorithms

| Algorithm | Time | Notes |
|---|---|---|
| [Counting sort](/counting-sort/) | $O(n + U)$ | linear for $U = O(n)$, stable |
| [Radix sort](/radix-sort/) | $O(n \cdot w / \log n)$ | linear for $w = O(\log n)$, stable |
| Kirkpatrick and Reisch (1984) | $O(n \log (w / \log n))$ | reduces the key length by recursion |
| Fredman and Willard (1993), [fusion trees](/fusion-tree/) | $O(n \log n / \log \log n)$ | deterministic, linear space |
| Andersson, Hagerup, Nilsson and Raman (1998) | $O(n)$ expected for $w \ge (\log n)^{2+\varepsilon}$; $O(n \log \log n)$ in general | signature sort and packed sorting |
| [Han (2004)](/han-integer-sort/) | $O(n \log \log n)$ | deterministic, linear space |
| [Han and Thorup (2002)](/han-thorup-integer-sort/) | $O(n \sqrt{\log \log n})$ expected | randomized, linear space |

For keys of a few words in practice, LSD radix sort with 8-bit to 16-bit digits, [MSD radix sort](/msd-radix-sort/) and [spreadsort](/spreadsort/) are the usual choices.

## Bounds

- **Lower bound.** Each algorithm must read all keys, so $\Omega(n)$ time is needed. No better general lower bound is known on the word RAM with multiplication.
- **Upper bounds.** For $w = O(\log n)$ and for $w \ge (\log n)^{2+\varepsilon}$ the problem takes $O(n)$ time, the second bound in expectation. For the other word lengths, the best bounds are $O(n \log \log n)$ deterministic and $O(n \sqrt{\log \log n})$ expected.
- **Comparison sorts.** In the [decision tree model](/decision-tree-model/) sorting needs $\lceil \lg n! \rceil$ comparisons. Integer sorts escape this bound because one operation on a word can do more than a two-way branch.
- **The role of the word length.** All the bounds above are for $w \ge \lg n$. The cost of a method can depend on $w$, and a bound that holds for every $w$ is the strongest form of a result.

## Reductions

- **Priority queues.** Thorup (2007) proved that sorting and priority queues are equivalent on the word RAM: if $n$ keys can be sorted in $n \cdot S(n)$ time, then a [priority queue](/priority-queue/) supports insert and delete-min in $O(S(n))$ time per operation, and the converse is direct. So Han's bound gives a priority queue with $O(\log \log n)$ time per operation.
- **Predecessor search.** A predecessor structure with $O(t)$ time per operation sorts in $O(n t)$ time: insert all keys, then walk the order. Fusion trees and van Emde Boas style structures give sorting bounds this way; the [predecessor lower bound](/predecessor-lower-bound/) limits what this route can give.
- **Strings.** A set of strings sorts by repeated integer sorts on characters, as in [MSD radix sort](/msd-radix-sort/), so string sorting reduces to integer sorting plus the cost of reading the characters.
- **Element distinctness.** After an integer sort, equal keys are adjacent, so [element distinctness](/element-distinctness/) on integers takes the time of an integer sort plus $O(n)$.

## Applications

- **Suffix arrays.** [Prefix doubling](/prefix-doubling/) and linear-time [suffix array](/suffix-array/) construction sort pairs of integer ranks with radix sort in each round.
- **Graph algorithms.** [Kruskal's algorithm](/kruskal/) with integer weights can sort the edges with radix sort. [Dijkstra's algorithm](/dijkstra/) with integer weights uses integer priority queues such as the [bucket queue](/bucket-queue/) and the [radix heap](/radix-heap/).
- **Databases and joins.** Sort-based joins and group-by steps sort integer keys or hash values, often with radix sort.
- **Computer graphics and simulation.** Depth sorting and spatial sorting of points by integer codes use radix sorts, also on parallel hardware, see [parallel radix sort](/parallel-radix-sort/).

## References
