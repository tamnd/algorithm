---
tag: KV7YMA
kind: theorem
slug: sorted-search-lower-bound
name: Sorted search lower bound
aliases:
- search lower bound in sorted array
- binary search optimality
area: foundations/lower-bounds
level: intro
summary: Searching a sorted array of n items by comparisons needs ceil(log2(n+1)) probes; binary search is optimal.
prereqs: [decision-tree-model, comparison-model, binary-search]
see_also: [binary-search, search-in-sorted-array, search-lower-bound, decision-tree-method, information-theoretic-bound, interpolation-search, exponential-search, adversary-argument]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table (comparison trees for search, binary search and its optimality, and the history of binary search)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1, Lower bounds for sorting (the decision-tree model and the bound from the number of leaves)
---

The sorted search lower bound says that every algorithm that searches a sorted array of $n$ distinct keys by comparing the search key with array entries makes at least $\lceil \lg(n+1) \rceil$ comparisons in the worst case. [Binary search](/binary-search/) makes at most $\lfloor \lg n \rfloor + 1$ comparisons, which is the same number, so binary search is exactly optimal for every $n$. The proof is a [decision tree](/decision-tree-model/) argument: the $n + 1$ gaps between the keys must reach different leaves along answers "less" and "greater" only. The bound holds only for comparisons; [interpolation search](/interpolation-search/) uses arithmetic on keys and can do better on some inputs.

## Statement

The input is a sorted array $A[1] < A[2] < \dots < A[n]$ and a key $x$. The algorithm may compare $x$ with any entry $A[i]$, and each comparison has three answers: $x < A[i]$, $x = A[i]$, $x > A[i]$. It must output an index $i$ with $A[i] = x$, or report that $x$ is absent.

**Theorem.** Let $n \ge 1$. Every deterministic algorithm of this kind makes at least $\lceil \lg(n+1) \rceil$ comparisons on some input. Binary search makes at most $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$ comparisons on every input. So the least worst-case number of comparisons is $\lceil \lg(n+1) \rceil$.

**Two-way variant.** If each comparison has only two answers, $x < A[i]$ or not, or $x \le A[i]$ or not, the least worst-case number is $\lceil \lg(2n+1) \rceil = \lfloor \lg n \rfloor + 2$.

## In plain words

Think of a dictionary with its words in order, and a word that you want to look up. Each time you open the book at a word and compare, you learn whether your word comes before it, after it, or is it. If your word is not in the book, the only useful replies are "before" and "after", so each look splits the open places into two parts at best.

To be sure that a word is missing, you must find the exact place where it would go, between two neighbours, and check both of them. There is one such place more than there are words. Halving that many places until one is left takes a fixed number of looks, and opening the book in the middle each time takes exactly that many.

## Proof

**Lower bound.** Fix a correct algorithm and $n$. Its runs form a comparison tree with three answers at each node. Use the array $A[i] = 2i$. A key in **gap** $g$, for $g = 0, 1, \dots, n$, is the key $x_g = 2g + 1$, so $A[g] < x_g < A[g+1]$, with $A[0] = -\infty$ and $A[n+1] = +\infty$. Each $x_g$ is absent.

*Claim 1. The run on $x_g$ compares $x_g$ with $A[g+1]$ if $g < n$, and with $A[g]$ if $g > 0$.* Suppose $g < n$ and the run never compares $x_g$ with $A[g+1]$. Let $x' = A[g+1] = 2g + 2$. For each $j \ne g + 1$, $x_g$ and $x'$ give the same answer against $A[j]$: both are greater than $A[j]$ for $j \le g$, and both are less for $j \ge g + 2$. So the run on $x'$ follows the same path and reports "absent", but $x'$ is in the array. This is wrong. The case of $A[g]$ with $g > 0$ is the same, with $x' = A[g]$.

*Claim 2. The runs on $x_0, \dots, x_n$ end at $n + 1$ different leaves.* Let $g < g'$. The run on $x_g$ compares $x_g$ with $A[g+1]$ and gets "less". Since $g' \ge g + 1$, $x_{g'} > A[g+1]$. If both runs reached the same leaf, they would follow the same path, and the comparison with $A[g+1]$ would give the same answer to both. It does not, so the leaves differ.

*Count.* Each answer on these $n + 1$ paths is "less" or "greater", because $x_g$ equals no entry. Following only these two answers from the root, at most $2^d$ nodes are reached at depth $d$, so at most $2^h$ leaves are reached in a tree of height $h$. Hence $n + 1 \le 2^h$, and $h \ge \lceil \lg(n+1) \rceil$. ∎

**Upper bound.** Binary search on $A[lo..hi]$ compares $x$ with the middle entry $A[mid]$, $mid = \lfloor (lo + hi)/2 \rfloor$, stops on "equal", and goes on with the part to the left or to the right. With $k = hi - lo + 1$ entries, the left part has $\lfloor (k-1)/2 \rfloor$ entries and the right part $\lfloor k/2 \rfloor$. So the worst number of comparisons satisfies $B(0) = 0$ and $B(k) = 1 + B(\lfloor k/2 \rfloor)$, which gives $B(n) = \lfloor \lg n \rfloor + 1$ for $n \ge 1$: the number of times $n$ can be halved, rounding down, before it reaches 0 is the number of binary digits of $n$.

Finally $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$. Let $k = \lfloor \lg n \rfloor$, so $2^k \le n < 2^{k+1}$. Then $2^k < n + 1 \le 2^{k+1}$, so $\lceil \lg(n+1) \rceil = k + 1$. ∎

**Two-way variant.** With two answers, an input with $x = A[i]$ and an input with $x$ in a gap must also reach different leaves. Consider the $2n + 1$ **cells**: the $n + 1$ gaps and the $n$ entries. Take one key in each cell. A comparison with $A[j]$ cannot tell apart $x$ in gap $j - 1$ and $x = A[j]$ unless it is the test "$x < A[j]$", and cannot tell apart $x = A[j]$ and $x$ in gap $j$ unless it is the test "$x \le A[j]$". The argument of Claim 1 shows that each path must contain the test that separates its cell from each neighbouring cell with a different correct output, and the argument of Claim 2 then shows that the $2n + 1$ cells reach different leaves. So the height is at least $\lceil \lg(2n+1) \rceil$. A search that finds the least $j$ with $x \le A[j]$ by $\lceil \lg(n+1) \rceil$ tests "$x \le A[mid]$", and then makes one test "$x < A[j]$" to decide whether $x = A[j]$, meets this, because $\lceil \lg(n+1) \rceil + 1 = \lfloor \lg n \rfloor + 2 = \lceil \lg(2n+1) \rceil$.

## Consequences

- **Binary search is exactly optimal.** No comparison algorithm, however clever, saves even one comparison in the worst case, for any $n$.
- **The average case.** In a tree for search, the unsuccessful searches end at $n + 1$ leaves reached by two answers. Their average depth is smallest when all their depths are $\lfloor \lg(n+1) \rfloor$ or $\lceil \lg(n+1) \rceil$, and binary search has this shape (Knuth, Section 6.2.1). So binary search also has the least average cost for unsuccessful searches.
- **Searching with insertion.** Finding the position at which to insert a key into a sorted list of $n$ keys is the same problem without the answer "equal", and needs $\lceil \lg(n+1) \rceil$ comparisons. Binary insertion of the $k$th item costs $\lceil \lg k \rceil$, which is part of the analysis of [merge sort optimality](/merge-sort-optimality/) and of the [Ford and Johnson algorithm](/ford-johnson-algorithm/).

| $n$ | three-way $\lceil \lg(n+1) \rceil$ | two-way $\lceil \lg(2n+1) \rceil$ | linear search $n$ |
|---|---|---|---|
| 1 | 1 | 2 | 1 |
| 2 | 2 | 3 | 2 |
| 3 | 2 | 3 | 3 |
| 4 | 3 | 4 | 4 |
| 7 | 3 | 4 | 7 |
| 8 | 4 | 5 | 8 |
| 15 | 4 | 5 | 15 |
| 16 | 5 | 6 | 16 |
| 100 | 7 | 8 | 100 |
| 1000 | 10 | 11 | 1000 |
| $10^6$ | 20 | 21 | $10^6$ |
| $10^9$ | 30 | 31 | $10^9$ |

## Tightness

The bound is exact for every $n \ge 1$, in both variants. The worst case of binary search jumps by one exactly when $n + 1$ passes a power of 2: from $n = 7$ to $n = 8$ it goes from 3 to 4.

The theorem is for the comparison model. Other models give other values.

- **Interpolation search** computes the next probe from the values of the keys. On keys drawn uniformly at random it makes $O(\lg \lg n)$ probes on average, but $\Theta(n)$ in the worst case.
- **Hashing** answers membership in $O(1)$ expected time, but it does not keep the order.
- **External memory.** When each probe reads a block of $B$ keys, a B-tree search reads $O(\log_B n)$ blocks, which is optimal in that model.
- **Unbounded search.** If $n$ is not known, [exponential search](/exponential-search/) finds a key at position $i$ with about $2 \lg i$ comparisons.

### Pitfalls

- **The gaps, not the entries, count.** A leaf count that uses only the $n$ outputs "found at $i$" plus one output "absent" gives $\lceil \log_3(n+1) \rceil$, which is too weak. The proof must show that the $n + 1$ gaps need different leaves, even though they all give the answer "absent".
- **Three-way comparisons need care.** The answer "equal" occurs only when $x$ is an entry, so it adds no branching on absent keys. That is why the base is 2, not 3.
- **The changed key must be legal.** In Claim 1 the new key $x'$ is an entry of the same sorted array. A proof that changes the array must keep it sorted.
- **Off by one.** $\lfloor \lg n \rfloor + 1$ and $\lceil \lg(n+1) \rceil$ are equal, but $\lceil \lg n \rceil$ is one less when $n$ is a power of 2: for $n = 8$ it is 3, while 4 comparisons are needed.
- **Duplicates.** With equal keys in the array, "find some $i$ with $A[i] = x$" is still solved by binary search, but "find the first $i$" needs the two-way search for the left end of the run of equal keys.

## History

Knuth, Volume 3, Section 6.2.1, proves that binary search is optimal by comparison trees and reports its history: binary search was described by John Mauchly in 1946, and the first version that works for every $n$, not only for $n$ one less than a power of 2, was published by D. H. Lehmer in 1960. The method of the proof, a bound on the number of leaves of a decision tree, is the one used for the lower bound for sorting in CLRS, Section 8.1.

## References
