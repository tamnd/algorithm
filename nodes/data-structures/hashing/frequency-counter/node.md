---
tag: TCABJ9
kind: problem
slug: frequency-counter
name: Frequency counter
area: data-structures/hashing
level: intro
summary: Problem of counting how often each distinct word appears in an input, typically solved with a symbol table.
model: comparison-model
complexity:
  vars: {n: the number of words in the input}
  time: {worst: Ω(n log n)}
prereqs: [dictionary, hash-table, element-distinctness]
see_also: [dedup, mode-finding, frequent-items-problem, misra-gries-summary, count-min-sketch, word-count, hash-aggregation, top-k-selection]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1 (Symbol tables), the client FrequencyCounter and its use as a test of symbol-table implementations
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 11 (Hash tables) for the expected O(1) dictionary operations
  - paper: doi:10.1145/800061.808735
    title: Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983)
    locator: pp. 80 to 86 (the Omega(n log n) bound for element distinctness)
---

The frequency counter problem asks, for a sequence of words, how many times each distinct word occurs. The standard solution keeps a [dictionary](/dictionary/) from each word to its count and adds 1 at each occurrence; with a [hash table](/hash-table/) this takes $O(n)$ expected time for $n$ words of constant length. In the [comparison model](/comparison-model/) it needs $\Omega(n \log n)$ comparisons, because the counts answer [element distinctness](/element-distinctness/). Sedgewick and Wayne use the client FrequencyCounter as the test of each symbol table in their book.

## In plain words

You have a long text and you want to know which words it uses and how often. Keep a notebook with one line for each word. Read the text one word at a time. If the word already has a line, add one to its number. If not, write a new line with the word and the number one. At the end, each line gives a word and its count.

The work is in finding the line of a word fast. A sorted notebook needs a search. A hash table goes almost straight to the line, so the whole job is about one step for each word of the text.

## Definition

**Input.** A sequence $w_1, w_2, \ldots, w_n$ of $n \ge 0$ words (or keys) from a universe $U$ with an equality relation.

**Output.** The multiplicity function of the sequence, as a set of pairs
$$F = \{(x, c(x)) : x \in \{w_1, \ldots, w_n\}\}, \qquad c(x) = |\{i : 1 \le i \le n,\ w_i = x\}|.$$

$F$ has one pair for each of the $d$ distinct words, each count is at least 1, and the counts add up to $n$. The order of the pairs is not part of the problem, unless a variant asks for one.

## Variants

- **The most frequent word.** Output a word with the largest count, the [mode](/mode-finding/). The client FrequencyCounter of Sedgewick and Wayne does this, and counts only the words of a given minimum length.
- **The top $k$ words.** Output the $k$ words with the largest counts, by a [selection of the top $k$](/top-k-selection/) of the $d$ pairs.
- **Sorted output.** Output the pairs in order of the word, or in decreasing order of the count.
- **Frequent items in a stream.** With memory much smaller than $d$, find the words whose count is more than $n/k$. The [frequent items problem](/frequent-items-problem/) is solved by the [Misra-Gries summary](/misra-gries-summary/) with $k - 1$ counters, and approximate counts come from a [count-min sketch](/count-min-sketch/).
- **Distributed counting.** The [word count](/word-count/) job of MapReduce counts the words of many files on many machines, and then adds the partial counts of each word.
- **Small integer keys.** When the words are integers in $\{0, \ldots, u - 1\}$, an array of $u$ counters solves the problem in $O(n + u)$ time. This is the first step of [counting sort](/counting-sort/).

## Examples

The input "it was the best of times it was the worst of times" has $n = 12$ words and $d = 7$ distinct words.

| word | count |
|---|---|
| it | 2 |
| was | 2 |
| the | 2 |
| best | 1 |
| of | 2 |
| times | 2 |
| worst | 1 |

The counts add up to 12. Five words tie for the largest count, 2, so the mode is not unique here.

| input | output |
|---|---|
| a b a c a b | (a, 3) (b, 2) (c, 1) |
| x x x x | (x, 4) |
| (empty) | (empty) |

## Known algorithms

- **Hash table of counters.** For each word, search the [hash table](/hash-table/); if the word is there add 1 to its count, else insert it with count 1. This is $n$ operations, so $O(n)$ expected time with [universal hashing](/universal-hashing/) and $O(d)$ space, for words of constant length. For words of total length $L$ it takes $O(L)$ expected time. Python's `collections.Counter` works in this way, and so does a Java `HashMap` from words to counts.
- **Balanced search tree.** The same loop with a [red-black tree](/red-black-tree/) takes $O(n \log d)$ time in the worst case and gives the words in sorted order at the end.
- **Trie.** A [trie](/trie/) with a counter at the node of each word takes $O(L)$ worst-case time for an alphabet of constant size.
- **Sort and count runs.** Sort the words, for example with [merge sort](/merge-sort/), then count each run of equal words. This takes $O(n \log n)$ comparisons.
- **Elementary symbol tables.** Sedgewick and Wayne also run the client with a [sequential search symbol table](/sequential-search-symbol-table/), which takes $O(nd)$ time, and a [binary search symbol table](/binary-search-symbol-table/), which takes $O(n \log d)$ comparisons for the searches and $O(d^2)$ time for the inserts in the worst case, because each new word shifts up to $d$ entries of the sorted arrays.

## Bounds

**Comparison model.** Each algorithm that only compares words by $<$, $=$ and $>$ needs $\Omega(n \log n)$ comparisons in the worst case. The input is distinct exactly when each count is 1, so a frequency counter decides element distinctness with $O(n)$ extra steps and no further comparison, and element distinctness needs $\Omega(n \log n)$ comparisons in this model. The bound also holds in the [algebraic computation tree](/algebraic-computation-tree/) model, by the [element distinctness lower bound](/element-distinctness-lower-bound/). Sorting, and a balanced tree, match it.

**Hashing.** With a random hash function, the hash table of counters takes $O(n)$ expected time on the [word RAM](/word-ram/), and no algorithm takes less than $\Omega(n)$, since each word must be read.

**Streams.** An exact answer needs memory for all $d$ distinct words in the worst case. The Misra-Gries summary uses $k - 1$ counters and gives each count with an error of at most $n/k$.

## Reductions

- **Element distinctness reduces to frequency counting** with $O(n)$ extra work: check that each count is 1.
- **[Deduplication](/dedup/) reduces to frequency counting:** the keys of the output are the distinct items.
- **Frequency counting reduces to sorting** with $O(n)$ extra work: after a sort, equal words form runs, and the length of each run is its count.
- **Mode finding reduces to frequency counting** with $O(d)$ extra work: take a pair with the largest count.

## Applications

- Word statistics of texts, and the term counts of an [inverted index](/inverted-index/) for the search of documents.
- `GROUP BY ... COUNT(*)` in SQL, done by [hash aggregation](/hash-aggregation/).
- Histograms of data, counts of [k-mers](/kmer-counting/) in genome analysis, and counts of the events of a log.
- The benchmark of symbol tables in Sedgewick and Wayne, who run FrequencyCounter on texts such as A Tale of Two Cities.

## References
