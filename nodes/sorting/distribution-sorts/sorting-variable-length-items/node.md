---
tag: NH6AN3
kind: problem
slug: sorting-variable-length-items
name: Sorting variable-length items
area: sorting/distribution-sorts
level: core
summary: Sorting strings or items of differing lengths in time linear in the total number of characters.
model: word-ram
complexity:
  vars: {n: the number of items, N: the total number of digits or characters, σ: the alphabet size}
  time: {worst: Θ(N + σ)}
prereqs: [radix-sort, counting-sort, string-sorting]
see_also: [msd-radix-sort, integer-sorting, lexicographic-order, multikey-quicksort, trie, positional-number-system]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Problem 8-3, Sorting variable-length items (part a for integers with different numbers of digits, part b for strings)
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Section 3.2, Radix sorting (the lexicographic sort of strings of varying length in time linear in the total length plus the alphabet size)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.1, String Sorts (MSD string sort, with the convention that the end of a string is smaller than every character)
---

Sorting variable-length items is the problem of sorting $n$ items of different lengths, such as integers with different numbers of digits or strings with different numbers of characters, in time linear in the total length $N$. A plain [radix sort](/radix-sort/) pads every item to the length of the longest one and can cost $\Theta(n \cdot L_{\max})$, which is much more than $N$ when a few items are long. Two ideas give $O(N + \sigma)$: group the items by length first, and let each pass of the sort touch only the items that are long enough.

## In plain words

You must sort items that are not all the same size. Some numbers have two digits and some have twenty. Some words are short and some are long. A simple digit-by-digit sort makes every item as long as the longest one, by adding blanks. Then one very long item makes the whole sort slow.

A better sort does work in proportion to the total size of all items. For whole numbers this is easy: a number with more digits is larger, so first put the numbers in groups by their digit count, then sort each group on its own. For words, the sort goes from the last position to the first and, at each position, it handles only the words that are long enough to have a letter there.

## Definition

**Integers.** The input is $n$ non-negative integers written in base $b$ without leading zeros. Let $\ell_i$ be the number of digits of the $i$-th integer and $N = \sum_i \ell_i$. The task is to sort them in $O(N)$ time for a fixed base $b$.

**Strings.** The input is $n$ strings over the alphabet $\{0, \ldots, \sigma - 1\}$ with lengths $\ell_1, \ldots, \ell_n$ and total length $N = \sum_i \ell_i$. The task is to sort them in [lexicographic order](/lexicographic-order/), with a proper prefix before the longer string, in $O(N + \sigma)$ time.

The difference between the two cases is important. For integers without leading zeros, the length decides the order between two items of different lengths. For strings it does not: ab comes before b although it is longer.

## Variants

- **With padding.** Pad each item to length $L_{\max}$ with a symbol smaller than all others and run LSD radix sort. The cost is $\Theta(L_{\max}(n + \sigma))$, which is linear in $N$ only if most items have length close to $L_{\max}$.
- **Top-down.** [MSD radix sort](/msd-radix-sort/) reads only the distinguishing prefixes, so it costs $O(D)$ plus the bucket overhead, where $D \le N$. The problem in this page asks for a bound in $N$, which is weaker but holds for a bottom-up method.
- **Satellite data.** The items can carry records; each method below moves references and is stable.
- **Signed integers and floating-point numbers.** Map them first to unsigned keys in the same order, as in [integer sorting](/integer-sorting/).

## Examples

**Integers.** Sort $5, 123, 47, 9, 1000, 62, 300$ in base 10. Here $N = 1 + 3 + 2 + 1 + 4 + 2 + 3 = 16$. A [counting sort](/counting-sort/) on the length gives the groups $\{5, 9\}$, $\{47, 62\}$, $\{123, 300\}$ and $\{1000\}$, in this order. Radix sort inside each group gives $5, 9$, then $47, 62$, then $123, 300$, then $1000$. Padding all seven numbers to four digits would read $28$ digits instead of $16$.

**Strings.** Sort ab, b, abc, a, ba. The longest length is 3. Each pass $j$, from 3 down to 1, starts from the list of the last pass, puts the strings of length exactly $j$ in front, and then sorts this list by character $j$ with a stable [counting sort](/counting-sort/).

| Pass $j$ | List before the sort | After the stable sort by character $j$ |
|---|---|---|
| 3 | abc | abc |
| 2 | ab, ba, abc | ba, ab, abc |
| 1 | b, a, ba, ab, abc | a, ab, abc, b, ba |

The output a, ab, abc, b, ba is in lexicographic order. The strings of length exactly $j$ go in front because, at pass $j$, their remaining suffix after position $j$ is empty, and the empty suffix is the smallest.

## Known algorithms

**Integers: group, then sort.** Sort the items by length with counting sort, in $O(n + L_{\max}) = O(N)$ time, since $L_{\max} \le N$. A longer integer is larger, so the groups are already in order. Sort the group of length $\ell$ with $n_\ell$ items by LSD radix sort in $O(\ell(n_\ell + b))$ time. The sum over all lengths that occur is $O(\sum_\ell \ell n_\ell + b \sum_\ell \ell) = O(N + bN)$, because each length that occurs is the length of at least one item, so $\sum_\ell \ell \le N$. For a fixed base this is $O(N)$.

**Strings: bottom-up with growing lists.** First, group the strings by length with a counting sort. Then run the passes $j = L_{\max}, \ldots, 1$ as in the example. Pass $j$ sorts only the strings of length at least $j$, and each string takes part in exactly $\ell_i$ passes, so the work on strings is $O(N)$ in total. A plain counting sort also scans $\sigma$ buckets in each pass, which adds $O(\sigma L_{\max})$. The method of Aho, Hopcroft and Ullman removes this term: it first sorts all pairs (position $j$, character at position $j$) by radix sort in $O(N + \sigma)$ time, which gives for each $j$ the sorted list of the characters that occur at position $j$, and then each pass visits only these non-empty buckets. The total is $O(N + \sigma)$.

**Strings: top-down.** [MSD radix sort](/msd-radix-sort/), [multikey quicksort](/multikey-quicksort/) and insertion into a [trie](/trie/) all treat the end of a string as a symbol smaller than each character. They cost $O(N)$ or less in character reads, plus bucket or comparison overhead.

## Bounds

- **Lower bound.** Each algorithm must read the input, so $\Omega(N)$ time is needed when all characters can matter; for strings the tighter reading bound is $\Omega(D)$, see [string sorting](/string-sorting/).
- **Upper bound.** $O(N)$ for integers in a fixed base and $O(N + \sigma)$ for strings, by the methods above. Both are optimal up to a constant factor when $\sigma = O(N)$.
- **Comparison sorts.** A comparison sort makes $\Theta(n \log n)$ comparisons, and a comparison of two items can read up to $\min(\ell_i, \ell_k)$ characters. On inputs with long common prefixes the total can be $\Theta(N \log n)$.

## Reductions

- **Strings to fixed length.** Padding to $L_{\max}$ reduces the problem to fixed-length [radix sort](/radix-sort/), at the cost of a factor of up to $n L_{\max} / N$.
- **Integers to strings.** An integer without leading zeros, written as one symbol for its length followed by its digits, compares in lexicographic order the same as in numeric order. So the integer case reduces to the string case.
- **Multi-key records.** Records with a variable number of fields, compared field by field, are strings over the alphabet of field values, see [multi-key sorting](/multi-key-sorting/).

## Applications

- **Sorting words and lines of text**, where the lengths vary a lot.
- **Big integers**, such as the keys of a database of numbers with arbitrary precision.
- **Tree isomorphism.** The linear-time algorithm of Aho, Hopcroft and Ullman for rooted trees sorts, level by level, the lists of the labels of the children of each node, and these lists have different lengths.
- **Suffix and rank sorting**, where names of variable-length blocks are sorted to give integer ranks, as in [prefix doubling](/prefix-doubling/).

## References
