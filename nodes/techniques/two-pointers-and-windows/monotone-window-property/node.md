---
tag: JARTCJ
kind: concept
slug: monotone-window-property
name: Monotone window property
aliases:
- monotonicity of two pointers
area: techniques/two-pointers-and-windows
level: core
summary: Pointers only move forward, so the total number of moves is O(n) and each element enters and leaves the window once.
prereqs: [sliding-window, two-pointers, monotone-predicate]
see_also: [sliding-window, two-pointers, monotone-predicate, binary-search, aggregate-method, knuth-optimization, monge-property, two-pointer-pair-search]
sources:
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm design techniques (scanning algorithms)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting (applications of sorting) and Chapter 5, Divide and conquer (binary search on monotone predicates)
  - url: https://cp-algorithms.com/data_structures/stack_queue_modification.html
    title: cp-algorithms, Minimum stack / Minimum queue
    locator: section Finding the minimum for all subarrays of fixed length
---

The monotone window property is the condition that makes two-pointer and sliding window scans correct and linear. A predicate on contiguous windows has it when goodness is kept under shrinking (every sub-window of a good window is good) or under growing (every super-window of a good window is good). Then the best start for each end, or the best end for each start, is a non-decreasing function. So both pointers can move only forward, each item enters and leaves the window once, the total number of moves is at most $2n$, and no optimal window is skipped. Without the property a forward-only scan can miss the answer.

## In plain words

A window over a list is good or bad by some rule. The rule is "monotone" if making a good window shorter keeps it good, as with "no letter repeats"; or if making a good window longer keeps it good, as with "contains the letters A, B and C".

With such a rule, the best left edge for each right edge never moves back as the right edge moves on. If a left edge was too early for one right edge, it is too early for all later ones too. So you never need to go back and try it again. Both edges walk forward, each at most once over the list, and the work is about two steps per item.

## The idea

Let $P(i, j)$ be a predicate on the windows $A[i \ldots j]$ of an array of length $n$.

**Down-closed.** $P$ is down-closed if $P(i, j)$ implies $P(i', j')$ for all $i \le i' \le j' \le j$. For an end $r$, let $L(r)$ be the smallest $i$ with $P(i, r)$ (with the empty window counted as good). Then:

- The good starts for $r$ form the interval $[L(r), r + 1]$: if $P(i, r)$ then $P(i', r)$ for all $i' \ge i$.
- $L$ is non-decreasing. If $P(L(r), r)$, then its part $A[L(r) \ldots r-1]$ is good, so $L(r - 1) \le L(r)$.

**Up-closed.** $P$ is up-closed if $P(i, j)$ implies $P(i', j')$ for all $i' \le i \le j \le j'$. For a start $i$, let $e(i)$ be the smallest $j$ with $P(i, j)$, or $\infty$. Then the good ends for $i$ form the interval $[e(i), n - 1]$, and $e$ is non-decreasing: if $P(i + 1, e(i + 1))$, then the bigger window $A[i \ldots e(i+1)]$ is good, so $e(i) \le e(i + 1)$.

**What the monotone functions give.**

- *No skipped optimum.* For the longest good window, the answer is $\max_r (r - L(r) + 1)$. A left pointer at $L(r - 1)$ is not past $L(r)$, so it only needs to move forward to reach it. A start $i < L(r)$ that it passes has $\neg P(i, r)$, and then $\neg P(i, r')$ for every $r' \ge r$, because $A[i \ldots r']$ contains $A[i \ldots r]$. So the pointer never passes a start that is good for a later end. The mirror argument works for the shortest good window with $e$.
- *Linear moves.* The right pointer moves $n$ times and the left pointer at most $n$ times (or $n + 1$ with the empty window), so a scan makes at most $2n + 1$ moves, and each item enters and leaves the window once. If each move and each test of $P$ costs $O(1)$, by an incremental summary of the window, the scan takes $O(n)$ time. This is a typical case of the [aggregate method](/aggregate-method/) of amortized analysis: one step can move the left pointer many times, but the total is bounded.
- *Counting.* For a down-closed $P$, the number of good nonempty windows is $\sum_r (r - L(r) + 1)$, and the scan computes it in the same pass.

**Relation to binary search.** For a fixed end $r$, the predicate $i \mapsto P(i, r)$ is a [monotone predicate](/monotone-predicate/), so $L(r)$ could be found by [binary search](/binary-search/) in $O(\log n)$ tests, for $O(n \log n)$ in total. The two-pointer scan uses the second monotonicity, of $L$ in $r$, to replace each search by an amortized $O(1)$ walk.

**Pair version.** The same idea works for pairs $(i, j)$ that are not windows. In the [pair search](/two-pointer-pair-search/) on a sorted array, the sum $A[i] + A[j]$ grows in $i$ and in $j$, so the pairs with sum at most $t$ form a staircase in the table of pairs, and the boundary of the staircase is a non-increasing function. Two pointers walk along this boundary in at most $n - 1$ steps.

## Examples

**Down-closed: no repeated character.** On $\texttt{abcabcbb}$, $L(r)$ for $r = 0, \ldots, 7$ is $0, 0, 0, 1, 2, 3, 5, 7$, which is non-decreasing. The longest good window has length $\max_r (r - L(r) + 1) = 3$, and the number of good nonempty windows is $1 + 2 + 3 + 3 + 3 + 3 + 2 + 1 = 18$.

**Up-closed: sum at least $s$ with non-negative items.** On $A = [2, 3, 1, 2, 4, 3]$ with $s = 7$, $e(i)$ for $i = 0, \ldots, 5$ is $3, 4, 4, 5, 5, \infty$, which is non-decreasing. The shortest good window has length $\min_i (e(i) - i + 1) = 2$, at $i = 4$. See [minimum size subarray sum](/minimum-size-subarray-sum/).

**Not monotone: sum at least $s$ with negative items.** On $A = [1, -3, 4]$ with $s = 4$, the window $[4]$ is good, but the bigger window $[1, -3, 4]$ has sum 2 and is bad. So $P$ is not up-closed, $e(0) = \infty$ while $e(2) = 2$, and a forward-only scan never sees a good window. The problem needs [prefix sums](/prefix-sums/) and a deque instead.

**Fixed length.** "Length exactly $k$" is neither down-closed nor up-closed, but a scan over fixed windows visits all $n - k + 1$ windows anyway, so no monotone property is needed.

| predicate | closed under | scan finds |
| --- | --- | --- |
| no repeated character | sub-windows | longest window, count of windows |
| at most $k$ distinct values | sub-windows | longest window |
| max minus min at most $d$ | sub-windows | longest window |
| sum at most $s$, non-negative items | sub-windows | longest window |
| sum at least $s$, non-negative items | super-windows | shortest window |
| contains every character of $t$ | super-windows | shortest window |
| sum at least $s$, any signs | neither | needs another method |

## Where it is used

- **Sliding window problems.** Every variable-length [sliding window](/sliding-window/) scan relies on it: [longest substring without repeating characters](/longest-substring-without-repeating-characters/), [longest substring with at most $k$ distinct](/longest-substring-with-k-distinct/), [minimum window substring](/minimum-window-substring/).
- **Two-pointer scans on sorted data.** The pair search, [3SUM](/three-sum-two-pointer-scan/) and the [container with most water](/container-with-most-water/) use the pair version.
- **Dynamic programming.** When the best split point $opt(i)$ of a recurrence is non-decreasing in $i$, a pointer can follow it forward instead of searching all splits. This is the idea behind [Knuth's optimization](/knuth-optimization/) and the divide-and-conquer optimization, and the [Monge property](/monge-property/) is a common reason why $opt$ is monotone.
- **Amortized analysis.** The bound "each item enters and leaves once" is the standard first example of aggregate analysis.

## References
