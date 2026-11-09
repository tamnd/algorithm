---
tag: G1NQQB
kind: problem
slug: lexicographic-permutation-successor
name: Lexicographic successor of a permutation
aliases:
- next permutation problem
area: combinatorics/generating-permutations
level: intro
summary: Given a permutation, return the lexicographically next permutation of the same items.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
prereqs: [lexicographic-order, permutation]
see_also: [next-permutation, lexicographic-successor, generating-all-permutations, multiset-permutations, permutation-ranking, permutation-unranking, lehmer-code, factorial-number-system]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2, Algorithm L (lexicographic permutation generation, for multisets as well as sets)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 2 (the successor algorithm for permutations in lexicographic order)
  - paper: doi:10.1145/356689.356692
    title: Robert Sedgewick, Permutation generation methods, ACM Computing Surveys 9(2) (1977) 137-164
    locator: the section on lexicographic methods
---

The lexicographic successor of a [permutation](/permutation/) is the next arrangement of the same items in [lexicographic order](/lexicographic-order/). It exists for every arrangement except the last one, which is the arrangement in non-increasing order. It has a simple form: keep the longest prefix that can stay, put the next larger item at the first place that must change, and sort the rest in increasing order. The [next permutation](/next-permutation/) algorithm finds it in $\Theta(n)$ time in the worst case and $O(1)$ time on average.

## In plain words

Think of the items as letters and of each order as a word. Sort all the words as in a dictionary. Given one word, you want the word that comes just after it in the dictionary, made from the same letters.

To find it, look at the word from its right end. While the letters go up from right to left, nothing can change there to make a larger word. At the first letter that is smaller than the letter on its right, a change is possible. Put there the smallest larger letter from its right side, and write the other letters on its right in increasing order. If the letters go up all the way, the word is the last one, and it has no next word.

## Definition

**Input.** A sequence $A = (a_1, \ldots, a_n)$ of items from a [totally ordered](/total-order/) set. Items may repeat.

**Output.** The smallest sequence $B$ in lexicographic order such that $B$ is an arrangement of the same items as $A$ (the same multiset) and $B > A$. If no such $B$ exists, report that $A$ is the last arrangement.

Two sequences of the same length compare by the first position where they differ. A common form of the problem changes $A$ in place and returns a flag that says whether a successor exists.

**Theorem.** Let $i$ be the largest index with $a_i < a_{i+1}$.

1. If no such $i$ exists, then $a_1 \ge a_2 \ge \cdots \ge a_n$, and $A$ has no successor.
2. Otherwise let $x$ be the smallest item of the suffix $a_{i+1}, \ldots, a_n$ that is larger than $a_i$. The successor is $a_1, \ldots, a_{i-1}$, then $x$, then the other $n - i$ items of the suffix and $a_i$, without one copy of $x$, in non-decreasing order.

*Proof.* An arrangement $B > A$ first differs from $A$ at some position $p$, where $b_p > a_p$, and $b_p$ is an item of the multiset $\{a_p, \ldots, a_n\}$. If $a_p \ge a_{p+1} \ge \cdots \ge a_n$, then $a_p$ is a largest item of this multiset, and no such $b_p$ exists. So in case 1 there is no $B$, and in case 2 the position $p$ is at most $i$. An arrangement with $p = i$ exists, because $a_i < a_{i+1}$. Each arrangement with $p = i$ is smaller than each arrangement with $p < i$, because at the first position $p' < i$ where the other one differs from $A$, it has the item of $A$ and the other one has a larger item. Among the arrangements with $p = i$, the smallest one takes the smallest allowed item $x$ at position $i$, and then the smallest order of the rest, which is non-decreasing. $\blacksquare$

The suffix $a_{i+1}, \ldots, a_n$ is non-increasing, by the choice of $i$. So $x$ can be found by a scan from the right end, and the rest is sorted by an exchange and a reversal of the suffix. This is the [next permutation](/next-permutation/) algorithm.

## Variants

- **Predecessor.** Find the arrangement just before $A$. Reverse all inequalities: $i$ is the largest index with $a_i > a_{i+1}$, and the rest is sorted in non-increasing order.
- **Wrap-around.** Return the first arrangement, in non-decreasing order, when $A$ is the last one. The C++ library function `std::next_permutation` does this and returns false.
- **Other orders.** The successor in the [minimal-change order](/minimal-change-permutation-order/) of the [Steinhaus-Johnson-Trotter algorithm](/steinhaus-johnson-trotter/) can also be computed from the permutation alone, without the direction array. Kreher and Stinson give this algorithm.
- **Partial permutations.** Find the next sequence of $k$ distinct items from $n$ items in lexicographic order. The same idea works, with the unused items as a reserve.
- **Combinations.** The successor of a $k$-subset in lexicographic order is the problem of [lexicographic combinations](/lexicographic-combinations/).

## Examples

| input $A$ | $i$ | $x$ | successor |
|---|---|---|---|
| 2 6 3 9 7 5 4 1 | 3 | 4 | 2 6 4 1 3 5 7 9 |
| 1 3 2 | 1 | 2 | 2 1 3 |
| 1 2 2 1 | 1 | 2 | 2 1 1 2 |
| a b d c | 2 | c | a c b d |
| 5 3 4 9 7 6 | 3 | 6 | 5 3 6 4 7 9 |
| 3 2 1 | none | | none (last) |
| 2 2 1 1 | none | | none (last) |

In the first row, the suffix 9 7 5 4 1 is decreasing, and $a_3 = 3 < 9$. The smallest suffix item larger than 3 is 4. The other items 9 7 5 3 1 go after it in increasing order. In the row 5 3 4 9 7 6, the answer is the next larger number with the same digits.

The arrangements of the multiset $\{1, 1, 2, 2\}$ in order are 1122, 1212, 1221, 2112, 2121, 2211. The successor of 1221 is 2112, as the third row shows.

## Known algorithms

- **[Next permutation](/next-permutation/)** (Knuth's Algorithm L, also on the page [lexicographic successor](/lexicographic-successor/)). Find $i$ by a scan from the right, find $x$ by a second scan from the right, exchange, and reverse the suffix. It takes $\Theta(n - i + 1)$ time and $O(1)$ extra space, and it works for multisets.
- **Through the rank.** Compute the rank $r$ of $A$, then the permutation of rank $r + 1$, with the [permutation rank and unrank algorithm](/permutation-rank-unrank/). This takes $O(n \log n)$ time, and it works for permutations of distinct items. It is useful when the step is not $+1$ but $+s$ for a large $s$.
- **Through the Lehmer code.** The [Lehmer code](/lehmer-code/) of the successor is the code of $A$ plus 1 in the [factorial number system](/factorial-number-system/). The digits that roll over to 0 match the decreasing suffix.

## Bounds

- **Worst case.** $\Theta(n)$. The successor of $1\,n\,(n-1) \cdots 2$ is $2\,1\,3 \cdots n$, which differs from it in at least $n - 1$ positions, so an algorithm that writes the answer into the array needs $\Omega(n)$ time on this input. Next permutation takes $O(n)$ time on every input.
- **Average case for distinct items.** For a uniformly random permutation of $n$ distinct items, the last $k$ items are in decreasing order with probability $1/k!$. So the expected length of the decreasing suffix is $\sum_{k=1}^{n} 1/k! < e - 1$, and next permutation takes $O(1)$ expected time. Over a run through all $n!$ permutations, the average is about $e - 1$ comparisons to find $i$ and about $3e/2 - 1 \approx 3.08$ comparisons in total per call.
- **Multisets.** The average can be large. For the multiset with $n - 1$ copies of 0 and one 1, a run through all $n$ arrangements makes $n^2 - 1$ comparisons, which is $\Theta(n)$ per arrangement.
- **Space.** $O(1)$ extra words, as the answer replaces the input.

## Reductions

- **To and from ranking.** The successor of $A$ is the permutation of rank $\operatorname{rank}(A) + 1$, so [ranking](/permutation-ranking/) and [unranking](/permutation-unranking/) solve this problem. In the other direction, $r$ successor steps from the first permutation give the permutation of rank $r$, but this takes time $\Omega(r)$.
- **Listing.** Repeated successor steps from the sorted arrangement solve [generating all permutations](/generating-all-permutations/) and [multiset permutations](/multiset-permutations/) in lexicographic order. The state between steps is the current arrangement alone.

## Applications

- **Listing in order.** Library functions such as C++ `std::next_permutation` list the arrangements of a sequence in sorted order, with copies of equal items handled correctly.
- **Resumable search.** A search over all orders can stop and later continue from the last arrangement it saw, because the successor needs no other state.
- **Next larger number with the same digits.** Treat the digits of a number as a sequence. The successor, if it exists, is the next larger number with the same digits.

## References
