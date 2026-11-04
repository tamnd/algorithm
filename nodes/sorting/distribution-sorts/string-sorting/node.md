---
tag: K3X2A2
kind: problem
slug: string-sorting
name: String sorting
aliases:
- Lexicographic sorting of strings
area: sorting/distribution-sorts
level: core
summary: Sort a collection of strings lexicographically, with running time depending on total string length.
model: word-ram
complexity:
  vars: {n: the number of strings, N: the total length of the strings, D: the sum of the distinguishing prefix lengths}
  time: {worst: Ω(D + n log n)}
prereqs: [sorting-problem, lexicographic-order]
see_also: [msd-radix-sort, radix-sort, multikey-quicksort, three-way-radix-quicksort, american-flag-sort, burstsort, trie, sorting-variable-length-items]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.1, String Sorts (LSD string sort, MSD string sort and three-way string quicksort, with the table of the costs of the string-sorting algorithms)
  - paper: Jon L. Bentley and Robert Sedgewick, Fast algorithms for sorting and searching strings, Proceedings of the Eighth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1997, pages 360 to 369
    locator: the description of multikey quicksort and its analysis in terms of n log n plus the total length of the distinguishing prefixes
  - paper: Peter M. McIlroy, Keith Bostic and M. Douglas McIlroy, Engineering radix sort, Computing Systems 6(1), 1993, pages 5 to 27
    locator: the introduction (the cost of comparison sorts on strings with long common prefixes) and the MSD radix sorts for strings
---

String sorting is the problem of putting $n$ strings over an ordered [alphabet](/alphabet/) in [lexicographic order](/lexicographic-order/). Its cost is measured in character operations, not only in comparisons of whole strings, because one comparison of two strings can read many characters. The natural measure of the input is $D$, the total length of the distinguishing prefixes, and in a model that compares characters each algorithm needs $\Omega(D + n \log n)$ time; [multikey quicksort](/multikey-quicksort/) reaches this bound in expectation and [MSD radix sort](/msd-radix-sort/) reaches $O(D)$ plus a cost for the buckets.

## In plain words

You must put a list of words or other texts in dictionary order. Two words are compared letter by letter from the left, and the first letter where they differ decides the order. If one word is the start of the other, the shorter word comes first.

A normal sort treats each comparison of two words as one step. But a comparison of two long words with the same start, such as two web addresses from the same site, reads many letters before it finds the difference. So the true cost depends on how many letters a sort must read.

Good string sorts read each letter only a small number of times. They look at the first letter of all words, group the words by that letter, and go on with the next letter only inside each group.

## Definition

**Input.** A sequence $s_1, \ldots, s_n$ of strings over an alphabet $\Sigma$ with a total order. The alphabet has size $\sigma$. The total length is $N = \sum_i |s_i|$.

**Output.** The strings in non-decreasing lexicographic order: $s \le t$ if $s$ is a prefix of $t$, or if $s[j] < t[j]$ at the first position $j$ where they differ.

**Distinguishing prefixes.** The distinguishing prefix of $s_i$ is the shortest prefix of $s_i$ that is not a prefix of any other string of the input. If no such prefix exists (because $s_i$ is a prefix of another string, or occurs twice), it is $s_i$ itself. Let $D$ be the sum of the lengths of the distinguishing prefixes. Then $D \le N$, and a correct sort must read at least the characters that $D$ counts, because a character of a distinguishing prefix that is not read could be changed and change the order.

**Cost model.** Time counts character reads and character comparisons, plus word operations on indices. Two settings are usual: a *comparison alphabet*, where characters can only be compared, and an *integer alphabet* $\{0, \ldots, \sigma - 1\}$, where a character can be an array index.

## Variants

- **Fixed-length strings.** All strings have length $L$. [LSD radix sort](/radix-sort/) sorts them in $O(L(n + \sigma))$ time with $L$ stable passes.
- **Variable-length strings.** The lengths differ. Either pad with an end marker smaller than all characters or treat the end of a string as a key smaller than each character. See [sorting variable-length items](/sorting-variable-length-items/).
- **Small and large alphabets.** For bytes $\sigma = 256$, and an array of $\sigma$ counters per bucket is cheap. For Unicode code points or words as characters, an array per bucket is expensive, and methods that compare characters do better.
- **Suffix sorting.** The input is all suffixes of one text. Here $N$ is quadratic in the text length, and special methods build the [suffix array](/suffix-array/) instead.
- **Sorting with the LCP output.** Some applications also want the longest common prefix of each pair of adjacent strings in the output, the [LCP array](/lcp-array/) of the set.

## Examples

**A small set.** For the strings she, sells, sea, shells, by, the, sea, shore, the sorted output is by, sea, sea, sells, she, shells, shore, the. The distinguishing prefixes are b (1), sea and sea (3 each, because sea occurs twice), sel (3), she (3, because she is a prefix of shells), shel (4), sho (3) and t (1). So $D = 21$, while $N = 30$.

**Long common prefixes.** Take $n$ strings that each start with the same $L$ characters and then differ in one more character. Then $D = n(L + 1)$. A comparison sort makes about $n \lg n$ comparisons, and each one reads $L + 1$ characters, so it reads about $(L + 1) n \lg n$ characters. A string sort that reads each character of the distinguishing prefixes a constant number of times reads $O(nL)$ characters, smaller by a factor of about $\lg n$.

**Random strings.** For $n$ random strings over an alphabet of size $\sigma$, the distinguishing prefixes have length about $\log_\sigma n$, so $D \approx n \log_\sigma n$ even if the strings are very long.

## Known algorithms

| Algorithm | Time | Notes |
|---|---|---|
| Comparison sort, such as [merge sort](/merge-sort/) | $O(n \log n)$ string compares, each up to $O(\text{LCP} + 1)$ characters | simple, but slow on long common prefixes |
| [LSD radix sort](/radix-sort/) | $O(L(n + \sigma))$ | fixed length $L$, stable |
| [MSD radix sort](/msd-radix-sort/) | $O(D + \sigma \cdot T)$, with $T$ the number of buckets | integer alphabet; switch to insertion sort for small buckets |
| [American flag sort](/american-flag-sort/) | as MSD radix sort | in place |
| [Multikey quicksort](/multikey-quicksort/), [three-way radix quicksort](/three-way-radix-quicksort/) | $O(D + n \log n)$ expected | comparison alphabet, in place |
| [Burstsort](/burstsort/) | fast in practice on large sets | builds a [burst trie](/burst-trie/), few cache misses |
| Insertion into a [trie](/trie/) or a [ternary search tree](/ternary-search-tree/), then a traversal | $O(N)$ trie nodes for a trie over an integer alphabet | uses much memory |

## Bounds

- **Reading bound.** Each correct algorithm reads $\Omega(D)$ characters, by the argument in the definition.
- **Comparison bound.** Over a comparison alphabet with $\sigma \ge n$, $n$ distinct strings of length 1 are just $n$ distinct keys, so sorting them needs $\lceil \lg n! \rceil = \Omega(n \log n)$ comparisons by the [comparison lower bound](/comparison-sort-lower-bound/).
- Together these give $\Omega(D + n \log n)$ over a comparison alphabet, and multikey quicksort matches it in expectation.
- **Integer alphabet.** With an integer alphabet, the $n \log n$ term can be replaced by the cost of [integer sorting](/integer-sorting/) the characters that the algorithm reads. MSD radix sort reads $O(D)$ characters and pays $O(\sigma)$ per bucket for the count array.

## Reductions

- **Integer sorting is a special case.** Strings of length 1 over the alphabet $\{0, \ldots, U - 1\}$ are integers, so [integer sorting](/integer-sorting/) reduces to string sorting. Conversely, a $w$-bit integer is a string of $w / 8$ bytes, most significant byte first.
- **From string sorting to integer sorting.** MSD radix sort is a recursion of integer sorts: each step sorts the strings of one bucket by one character.
- **Multi-key records.** Sorting records by several fields in order of priority, as in [multi-key sorting](/multi-key-sorting/), is string sorting with fields as characters.
- **Tries.** Building a [trie](/trie/) of the strings and reading its leaves in order sorts the strings. MSD radix sort can be read as a traversal of the trie that never stores it.

## Applications

- **Text indexing.** Building [inverted indexes](/inverted-index/), dictionaries and [suffix arrays](/suffix-array/) sorts large sets of words or suffixes.
- **Compression.** The [Burrows-Wheeler transform](/burrows-wheeler-transform/) sorts the rotations of a text.
- **Databases.** Sorting on string keys for ORDER BY, joins and the removal of copies; the keys often have long common prefixes, such as URLs or file paths.
- **Command-line tools.** The Unix sort command sorts lines of text, a direct string sorting task.

## References
