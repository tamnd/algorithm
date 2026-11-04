---
tag: RNSRZD
kind: problem
slug: dedup
name: Deduplication
aliases:
- Dedup
area: data-structures/hashing
level: intro
summary: Problem of removing repeated items from a collection, usually done with a set that remembers what was seen.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Ω(n log n)}
prereqs: [hash-table, element-distinctness, dictionary-problem]
see_also: [element-distinctness, remove-duplicates-from-sorted-array, distinct-elements-problem, frequency-counter, bloom-filter, minhash, hash-aggregation, sorting-problem]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.5 (Applications), the set client DeDup that removes duplicates from a stream of keys
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 11 (Hash tables) for the expected O(1) set operations, and Section 8.1 (Lower bounds for sorting) for the decision-tree model
  - paper: doi:10.1145/800061.808735
    title: Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983)
    locator: pp. 80 to 86 (the Omega(n log n) bound for element distinctness)
---

Deduplication asks to remove the repeated items of a sequence, so that each distinct item is kept once. The usual solution scans the items and keeps a [hash table](/hash-table/) of the items seen so far, which takes $O(n)$ expected time for $n$ items. In the [comparison model](/comparison-model/) the problem needs $\Omega(n \log n)$ comparisons, because it answers [element distinctness](/element-distinctness/), and sorting the items reaches this bound. Deduplication is a step of many programs, from the `uniq` filter of Unix to the removal of copies of files in backup systems.

## In plain words

You have a list in which some things appear more than once, such as the e-mail addresses on a mailing list. You want each address only once. Go through the list from the start. Keep a set of the addresses that you have already seen. For each address, look in the set. If it is there, skip the address. If it is not there, keep the address and add it to the set.

This keeps the first copy of each address, in the order of the list. With a set that answers each question in constant time on average, the whole work is one pass over the list.

## Definition

**Input.** A sequence $a_1, a_2, \ldots, a_n$ of $n \ge 0$ items from a universe $U$ with an equality relation $=$ (an equivalence relation).

**Output.** The subsequence of first occurrences, that is, the sequence of the items $a_i$, in increasing order of $i$, for which $a_i \ne a_j$ for each $j < i$.

The output has one item from each class of equal input items, and its length is the number $d$ of distinct items. This is the **stable** form: it keeps the first copy and the input order. The **unordered** form asks only for the set $\{a_1, \ldots, a_n\}$, in any order.

## Variants

- **Unordered output.** Return the distinct items in any order. Sorting and then removing adjacent equal items solves this form.
- **Keep the last copy.** Keep $a_i$ when $a_i \ne a_j$ for each $j > i$.
- **Sorted input.** When equal items are adjacent, one pass with two indices solves the problem in place, with $O(1)$ extra space. This is [remove duplicates from a sorted array](/remove-duplicates-from-sorted-array/).
- **Deduplication by key.** Two records count as equal when a key field is equal, for example two users with the same e-mail address. The rest of the record is taken from the kept copy.
- **Counting only.** Return only the number $d$ of distinct items. This is the [distinct elements problem](/distinct-elements-problem/); in a stream with little memory it is solved approximately, for example by [HyperLogLog](/hyperloglog/).
- **Approximate membership.** A [Bloom filter](/bloom-filter/) replaces the exact set with fewer bits. It can drop a new item as a false duplicate, but it never keeps a second copy.
- **Near-duplicates.** Items count as duplicates when they are similar, not equal, for example web pages that differ only in a date. [MinHash](/minhash/) and [SimHash](/simhash/) find such pairs.
- **Storage deduplication.** A file system or a backup tool cuts the data into chunks, computes a fingerprint of each chunk, for example with a [Rabin fingerprint](/rabin-fingerprint/) to find the chunk borders, and stores each distinct chunk once.

## Examples

| input | output (stable form) |
|---|---|
| 3 1 3 2 1 3 | 3 1 2 |
| m i s s i s s i p p i | m i s p |
| 5 5 5 5 | 5 |
| 4 2 7 | 4 2 7 |
| (empty) | (empty) |
| "Ann" "ann" "Bob", equality ignoring case | "Ann" "Bob" |

## Known algorithms

- **Hash set.** Scan the items, and keep $a_i$ when it is not in a [hash table](/hash-table/) of the items seen, then insert it. This takes $n$ searches and at most $n$ inserts, so $O(n)$ expected time with [universal hashing](/universal-hashing/), and $O(d)$ extra space. It needs a [hash function](/hash-function/) that agrees with the equality.
- **Sort and scan.** Sort the pairs $(a_i, i)$ by item and then by index, for example with [merge sort](/merge-sort/), keep the first pair of each run of equal items, and sort the kept pairs by index. This takes $O(n \log n)$ time in the worst case and needs only comparisons. Without the second sort it solves the unordered form.
- **Balanced search tree.** The hash set can be replaced by a [red-black tree](/red-black-tree/), for $O(n \log d)$ time in the worst case.
- **Pairwise comparison.** Compare each item with each kept item. This takes $O(nd)$ time, which is $O(n^2)$ in the worst case, and it needs only the equality test.

## Bounds

**Comparison model.** If an algorithm can compare two items by $<$, $=$ and $>$, it needs $\Omega(n \log n)$ comparisons in the worst case. The output has $n$ items exactly when the input is distinct, so a deduplication algorithm decides element distinctness with no further comparison, and element distinctness needs $\Omega(n \log n)$ comparisons in this model. The same bound holds in the stronger [algebraic computation tree](/algebraic-computation-tree/) model for real inputs, by the [Ben-Or theorem](/ben-or-theorem/); see the [element distinctness lower bound](/element-distinctness-lower-bound/). Sort and scan matches it.

**Equality only.** If an algorithm can only test two items for equality, it needs $\binom{n}{2} = n(n-1)/2$ tests in the worst case, so pairwise comparison is optimal in this model. The [adversary argument](/adversary-argument/): answer "not equal" to each test. If some pair $(i, j)$ is never tested when the algorithm stops, then both the input with all items distinct and the input where only $a_i$ and $a_j$ are equal agree with all the answers, but they need different outputs. For $n = 6$ items this is 15 tests.

**Hashing.** With a random hash function, the hash set takes $O(n)$ expected time on the [word RAM](/word-ram/). The lower bounds above do not apply, because a hash value is not a comparison. No algorithm can beat $\Omega(n)$ time, since it must read each item.

## Reductions

- **Element distinctness reduces to deduplication** with $O(1)$ extra work: the input is distinct exactly when the output has $n$ items.
- **Deduplication reduces to sorting** with $O(n)$ extra work, by the sort and scan method above (two sorts for the stable form).
- **Deduplication reduces to frequency counting.** A [frequency counter](/frequency-counter/) that keeps the keys in the order of first insertion gives the stable output as its list of keys.

## Applications

- The Unix filter `sort | uniq` removes duplicate lines. `uniq` alone removes only adjacent duplicates, which is the sorted-input variant.
- `SELECT DISTINCT` in SQL, done by [hash aggregation](/hash-aggregation/) or by sorting.
- The visited set of a graph search, which keeps each vertex from being processed twice.
- Removal of copies of web pages in a search engine, and of blocks in backup and storage systems.
- Cleaning of data before analysis, for example the merge of customer records.

## References
