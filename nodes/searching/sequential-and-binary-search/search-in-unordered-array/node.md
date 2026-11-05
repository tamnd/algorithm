---
tag: RFE22A
kind: problem
slug: search-in-unordered-array
name: Search in an unordered array
aliases:
- unsorted membership search
area: searching/sequential-and-binary-search
level: intro
summary: Given an unsorted array and a key, decide whether the key occurs and where; Theta(n) comparisons are needed in the worst case.
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n)}
prereqs: [array, comparison-model]
see_also: [linear-search, sentinel-search, search-in-sorted-array, self-organizing-list-search, hash-table, unstructured-search, grover-search, adversary-argument]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1, Sequential searching (Algorithms S and Q, and the average number of comparisons)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1, exercises (the searching problem and linear search)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1, Symbol tables (sequential search in an unordered linked list)
---

Search in an unordered array asks, for an [array](/array/) $A[0 \ldots n-1]$ in no particular order and a key $x$, for an index $i$ with $A[i] = x$, or for the answer that no such index exists. Because the order of the items tells nothing about where $x$ is, each correct algorithm in the [comparison model](/comparison-model/) must, in the worst case, make $n$ comparisons, and [linear search](/linear-search/) makes exactly $n$. The problem is the base case of all search: each faster method, such as [binary search](/binary-search/) on a [sorted array](/search-in-sorted-array/) or a [hash table](/hash-table/), pays for its speed with some work done before the search.

## In plain words

You have a box of papers in no order, and you want the one with a given name on it. Nothing about the papers you have seen tells you where the one you want is. So you look at them one by one. If the paper is in the box, you may find it early, or late. If it is not in the box, you must look at every paper before you can say so, because any paper you skip could be the one.

The same holds for a program. Without order, without a hash, and without extra memory, the only way to be sure a value is absent is to look at each item.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of $n \ge 0$ items from a set $U$, and a key $x \in U$. The items need not be distinct and need not be in any order.

**Output.** An index $i \in \{0, \ldots, n-1\}$ with $A[i] = x$, or NIL when $A[i] \ne x$ for each $i$.

When $x$ occurs more than once, each of its indices is a correct output. The common convention, and the one that [linear search](/linear-search/) meets, is to return the smallest such index:

$$ \text{answer}(A, x) = \min\{\, i : A[i] = x \,\} \quad\text{or NIL when the set is empty.} $$

The cost is the number of comparisons that involve items. In the basic model the only test is the equality test "$A[i] = x$?". A stronger model also allows the three-way test of a [total order](/total-order/) between any two of $x, A[0], \ldots, A[n-1]$. The lower bound below holds in both models.

## Variants

- **Decision.** Return only yes or no: is $x$ in $A$?
- **First, last or all occurrences.** Return the smallest index, the largest index, or the full set $\{i : A[i] = x\}$. The last one always needs $n$ tests.
- **Search by a predicate.** Return the first $i$ with $P(A[i])$ true, for any test $P$. Linear search solves this without change.
- **Search in a linked list.** The items are reachable only one after the other. Random access does not help in the unordered case, so the bounds are the same.
- **Repeated searches.** Many keys are searched in the same array. Then it pays to build a structure first: sort the array once, or build a hash table, or move the items that are often asked for to the front of a [self-organizing list](/self-organizing-list-search/).
- **Probabilistic input.** The key is present with probability $q$, at a position chosen from a known distribution. The question is the expected number of comparisons.

## Examples

| $A$ | $x$ | output (smallest index) | equality tests by linear search |
|---|---|---|---|
| 7 3 9 3 1 | 3 | 1 | 2 |
| 7 3 9 3 1 | 1 | 4 | 5 |
| 7 3 9 3 1 | 8 | NIL | 5 |
| (empty) | 8 | NIL | 0 |
| 4 4 4 | 4 | 0 | 1 |

In the first row, both 1 and 3 are indices of the key. A problem that asks for "an index" accepts both. A problem that asks for the first index accepts only 1.

## Known algorithms

- **[Linear search](/linear-search/).** Test $A[0], A[1], \ldots$ in turn. At most $n$ equality tests, so $\Theta(n)$ time in the worst case and $\Theta(1)$ extra space.
- **[Sentinel linear search](/sentinel-search/).** Put $x$ after the last item, so the loop needs no test of the index. It does the same number of key tests, but about half the total tests.
- **Sort, then search.** Sort in $O(n \log n)$ time, then use [binary search](/binary-search/) in $O(\log n)$ for each key. This pays only when there are about $\log n$ or more searches.
- **Hashing.** Build a [hash table](/hash-table/) in $O(n)$ expected time. Each search then takes $O(1)$ expected time. This needs a hash function on the keys, which is outside the comparison model.

## Bounds

**Upper bound.** Linear search answers with at most $n$ equality tests on each input.

**Lower bound.** Each deterministic algorithm that only compares items (with equality tests or with three-way comparisons of any two of $x, A[0], \ldots, A[n-1]$) makes at least $n$ comparisons on some input with $x$ absent. The proof is an [adversary argument](/adversary-argument/) on the *comparison graph*: its vertices are $x$ and the $n$ array cells, and it has an edge for each pair that the algorithm compared.

*Proof.* Take integer keys. Fix an input where $A[i] = 3i$ for each $i$ and $x = -1$, so all values are distinct and $x$ is absent. Run the algorithm on it, and assume it stops with fewer than $n$ comparisons. A graph on $n + 1$ vertices with fewer than $n$ edges is not connected, so some connected component $C$ does not hold $x$. Pick a cell $j$ in $C$ and set $c = x - A[j]$. Build a second input: add $c$ to the value of each cell in $C$, and keep all other values. Each comparison the algorithm made was between two vertices of the same component. Inside $C$ all values moved by the same amount $c$, and outside $C$ nothing moved. So each comparison has the same answer on both inputs, and a deterministic algorithm makes the same comparisons and gives the same output on both. But on the second input $A[j] = x$, so the answer NIL is wrong there, and an index answer is wrong on the first input. This contradicts correctness, so the algorithm makes at least $n$ comparisons. $\blacksquare$

The bound is exact: $n$ comparisons are necessary and sufficient in the worst case. The argument also covers a randomized algorithm that is always correct: for each fixed sequence of random choices, the run on the first input must have a connected comparison graph, so it makes at least $n$ comparisons.

**Average case.** Suppose $x$ is present with probability $q$ and, when present, each of the $n$ positions is equally likely and the items are distinct. Linear search then makes on average

$$ q \cdot \frac{n+1}{2} + (1 - q)\, n $$

equality tests, because a key at index $i$ costs $i + 1$ tests and $\frac1n \sum_{i=0}^{n-1}(i+1) = \frac{n+1}{2}$. For $n = 100$ this is 50.5 tests when $q = 1$ and 75.25 when $q = 1/2$. Knuth derives these values for Algorithm S in Section 6.1.

**Other models.** A quantum algorithm with oracle access to the items needs only $\Theta(\sqrt{n})$ queries, by [Grover search](/grover-search/); this is the [unstructured search](/unstructured-search/) problem. With preprocessing and hashing, a search costs $O(1)$ expected time.

## Reductions

- **This problem reduces to [search in a sorted array](/search-in-sorted-array/)** with an extra $O(n \log n)$ for the sort. Each later search then costs $O(\log n)$.
- **Element distinctness is harder.** Testing whether all $n$ items are distinct needs $\Omega(n \log n)$ comparisons in the comparison model ([element distinctness lower bound](/element-distinctness-lower-bound/)), while one membership test needs only $n$.

## Applications

- A short list, such as the keywords of a small language or the open files of a process, where a scan is faster than any structure.
- The base case inside other structures: the chain of a hash table, a bucket, or the leaf block of a B-tree is searched with a scan.
- Data that is searched only once, or that changes after each search, so that preprocessing does not pay.

## References
