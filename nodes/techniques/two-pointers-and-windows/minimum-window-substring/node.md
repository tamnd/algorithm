---
tag: WSWNKE
kind: problem
slug: minimum-window-substring
name: Minimum window substring
aliases:
- smallest window containing all characters
area: techniques/two-pointers-and-windows
level: core
summary: Find the shortest substring of a text that contains every character of a pattern with required multiplicities.
prereqs: [sliding-window, frequency-vector, hash-table]
see_also: [minimum-window-substring-algorithm, minimum-window-subsequence, minimum-size-subarray-sum, monotone-window-property, longest-substring-with-k-distinct, string-matching, frequency-vector, sliding-window]
sources:
  - url: https://leetcode.com/problems/minimum-window-substring/
    title: LeetCode, problem 76, Minimum Window Substring
    locator: problem statement and the O(m + n) follow-up
  - url: https://leetcode.com/problems/find-all-anagrams-in-a-string/
    title: LeetCode, problem 438, Find All Anagrams in a String
    locator: problem statement (fixed-length window with the same counts)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Data structures (hashing and arrays indexed by key)
---

The minimum window substring problem gives a text $s$ of length $n$ and a pattern $t$ of length $m$, and asks for the shortest substring of $s$ that contains every character of $t$, each at least as many times as in $t$. The order of the characters does not matter. Since a window that contains the pattern still contains it when it grows, the problem has the [monotone window property](/monotone-window-property/), and the [sliding window for minimum window substring](/minimum-window-substring-algorithm/) solves it in $\Theta(n + m + \sigma)$ time for an alphabet of size $\sigma$. It is the standard example of a minimum-length window with a multiset condition.

## In plain words

You have a long text and a short list of letters, where a letter may be listed more than once. You want the shortest stretch of the text, with no gaps, that has all the listed letters, with at least as many copies as the list asks for. The letters may come in any order and other letters may be mixed in.

For the text $\texttt{ADOBECODEBANC}$ and the list $\texttt{ABC}$, the answer is $\texttt{BANC}$.

A stretch that has everything still has everything when you make it longer. So a window can slide over the text: grow on the right until it has everything, then shrink from the left as long as it still has everything.

## Definition

**Input.** A text $s = s_0 \cdots s_{n-1}$ and a pattern $t = t_0 \cdots t_{m-1}$ over an alphabet $\Sigma$, $\sigma = |\Sigma|$, with $m \ge 1$.

**Output.** A substring $s[i \ldots j]$ of least length $j - i + 1$ such that $\mathrm{cnt}_{s[i \ldots j]}(c) \ge \mathrm{cnt}_t(c)$ for every character $c$, where $\mathrm{cnt}_w(c)$ is the number of copies of $c$ in $w$. If several have the least length, the usual convention returns the one with the smallest start. If none exists, the output is the empty string.

A substring with this property is *valid*. A valid substring has length at least $m$.

## Variants

- **Set version.** Each distinct character of $t$ is needed once, whatever its multiplicity in $t$. This is the classic "smallest window that contains all the given characters".
- **In order.** The characters of $t$ must appear in the window in the order of $t$, as a subsequence. Validity is still kept when the window grows, but checking it needs more than counts; see [minimum window subsequence](/minimum-window-subsequence/).
- **Exact counts, fixed length.** Find the windows of length $m$ whose counts equal those of $t$: the anagrams of $t$ in $s$. A window of fixed length $m$ with a counter of mismatched characters does it in $O(n + m + \sigma)$ time.
- **All distinct characters of the text.** Take $t$ to be the set of characters of $s$: the shortest window that contains every character that occurs in $s$.
- **Numbers.** On an array of numbers, the shortest subarray that contains all values of a given set, with a hash table for the counts.
- **Weighted version.** Positive numbers and a target sum: [minimum size subarray sum](/minimum-size-subarray-sum/), the same shape with a sum in place of counts.

## Examples

| $s$ | $t$ | answer |
| --- | --- | --- |
| $\texttt{ADOBECODEBANC}$ | $\texttt{ABC}$ | $\texttt{BANC}$ |
| $\texttt{a}$ | $\texttt{a}$ | $\texttt{a}$ |
| $\texttt{a}$ | $\texttt{aa}$ | empty, $s$ has one $\texttt{a}$ |
| $\texttt{aa}$ | $\texttt{aa}$ | $\texttt{aa}$ |
| $\texttt{AAB}$ | $\texttt{AB}$ | $\texttt{AB}$ |
| $\texttt{abcab}$ | $\texttt{ab}$ | $\texttt{ab}$, at 0; another at 3 |

In the first example, the valid windows of least length for each start are $\texttt{ADOBEC}$ (start 0), $\texttt{CODEBA}$ (start 5), $\texttt{EBANC}$ (start 8) and $\texttt{BANC}$ (start 9), among others; the [algorithm page](/minimum-window-substring-algorithm/) traces all windows that the scan examines.

## Known algorithms

| algorithm | time | extra space |
| --- | --- | --- |
| every start, grow the end with running counts | $O(n^2 + m + \sigma)$ | $\Theta(\sigma)$ |
| binary search on the length, fixed windows | $O((n + \sigma) \log n + m)$ | $\Theta(\sigma)$ |
| [sliding window with a missing counter](/minimum-window-substring-algorithm/) | $\Theta(n + m + \sigma)$ | $\Theta(\sigma)$ |

**Sliding window.** For each start $i$, let $e(i)$ be the first end at which $s[i \ldots e(i)]$ is valid. The answer is the shortest of the windows $s[i \ldots e(i)]$. Because validity is kept when a window grows, $e$ is non-decreasing. So a right end that only moves right and a left end that only moves right visit every pair $(i, e(i))$: the right end stops at the first $r$ where the window is valid, and the left end then moves while the window stays valid, examining each window on the way. A table $need[c]$ of the copies still lacking, and a counter $missing$ of their sum over the characters with $need[c] > 0$, make each step $O(1)$.

*Why the moves skip nothing.* The left end passes a start $i$ only right after the window $s[i \ldots r]$ was valid while $s[i \ldots r-1]$ was not, which means $r = e(i)$ and the best window for $i$ was examined. The right end passes an end $r$ only when $s[l \ldots r]$ is not valid; then no window that ends at $r$ and starts at $l$ or later is valid, and every window that starts before $l$ was already beaten by the examined window of its start. The [algorithm page](/minimum-window-substring-algorithm/) writes this out as the invariant (W) and proves it.

**Binary search on the length.** The predicate "some window of length $L$ is valid" is monotone in $L$. For a fixed $L$, slide a window of length $L$ with counts in $O(n + \sigma)$ time. Binary search over $L$ adds a $\log n$ factor.

## Bounds

**Upper bound.** $\Theta(n + m + \sigma)$ time and $\Theta(\sigma)$ space with arrays; $O(n + m)$ expected time and $O(m)$ space with a hash table that holds only the characters of $t$.

**Lower bound, reads.** Every algorithm reads all of $t$ and all of $s$ on some input. Take $t = \texttt{ab}$ and $s = \texttt{a} \cdots \texttt{a}$ followed by one $\texttt{b}$. The answer is the last two characters. An unread character of $s$ before the last two can be changed to $\texttt{b}$, which creates a valid window elsewhere, and an unread character among the last two can be changed to $\texttt{a}$ or $\texttt{b}$ so that the answer changes. An unread character of $t$ can be changed to a character that $s$ lacks. So $\Omega(n + m)$ time is needed.

## Reductions

- **To the monotone window template.** Validity is closed under super-windows, so the shortest valid window for each start is found by two ends that only move right.
- **Special case: all characters of the text.** The shortest window that contains all distinct characters of $s$ is the case where $t$ lists each character of $s$ once.
- **Relation to string matching.** [String matching](/string-matching/) asks for the windows equal to $t$ in order; this problem asks only for the counts. The order-free condition is what lets counts and a window replace an automaton.

## Applications

- **Search snippets.** The shortest passage of a document that contains all words of a query, with words in place of characters, is a common way to choose the snippet shown with a search result.
- **Bioinformatics and logs.** The shortest region of a sequence, or the shortest period of a log, in which a given set of motifs or events all occur.
- **Teaching sliding windows.** It combines a count table, a validity counter and a minimum-length window, and its proof is the model for the other minimum-window problems.

## References
