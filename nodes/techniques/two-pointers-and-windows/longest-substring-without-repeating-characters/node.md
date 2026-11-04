---
tag: 8WN845
kind: problem
slug: longest-substring-without-repeating-characters
name: Longest substring without repeating characters
aliases:
- longest distinct substring
area: techniques/two-pointers-and-windows
level: intro
summary: Find the longest contiguous substring with all characters distinct.
prereqs: [sliding-window, hash-table]
see_also: [sliding-window-longest-substring, longest-substring-with-k-distinct, element-distinctness, element-distinctness-lower-bound, distinct-count-two-pointers, monotone-window-property, subsequence, sliding-window]
sources:
  - url: https://leetcode.com/problems/longest-substring-without-repeating-characters/
    title: LeetCode, problem 3, Longest Substring Without Repeating Characters
    locator: problem statement
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Data structures (hashing) and Chapter 4, Sorting (uniqueness testing)
---

The problem asks for the longest substring of a string in which no character appears twice. A substring is contiguous, so the answer is a window $s[i \ldots j]$, and the property "no repeated character" is kept when the window is cut shorter. This makes the problem a standard [sliding window](/sliding-window/) problem. The [sliding window for the longest distinct substring](/sliding-window-longest-substring/) solves it in one pass with the last position of each character, in $\Theta(n + \sigma)$ time for an alphabet of size $\sigma$. Over an alphabet with only comparisons, the problem contains [element distinctness](/element-distinctness/) and needs $\Omega(n \log n)$ comparisons.

## In plain words

You have a string of letters and you want the longest piece of it, without gaps, in which every letter is different. For $\texttt{abcabcbb}$ the answer is $\texttt{abc}$, of length 3.

The piece has no gaps, so it is a window over the string. If a window has a repeated letter, every bigger window around it also has that repeat. So you can slide a window from left to right, grow it on the right, and cut it on the left only when a repeat appears. The answer is the longest window you see.

## Definition

**Input.** A string $s = s_0 \cdots s_{n-1}$ over an alphabet $\Sigma$, with $\sigma = |\Sigma|$.

**Output.** The largest $L$ such that some substring $s[i \ldots i + L - 1]$ has $L$ distinct characters. In the search version, also a start $i$; the usual convention is the smallest one.

The answer is at most $\min(n, \sigma)$, and at least 1 when $n \ge 1$.

## Variants

- **Subsequence instead of substring.** If the characters need not be contiguous, the answer is just the number of distinct characters of $s$; see [subsequence](/subsequence/).
- **At most $k$ copies of each character.** The window shrinks while the count of the new character exceeds $k$.
- **At most $k$ distinct characters.** A different limit: [longest substring with at most $k$ distinct characters](/longest-substring-with-k-distinct/).
- **Arrays of numbers.** The longest subarray with distinct values. The same algorithm works with a hash table of last positions.
- **Count the repeat-free substrings.** With $L(r)$ the smallest start of a repeat-free window that ends at $r$, the number of repeat-free nonempty substrings is $\sum_r (r - L(r) + 1)$.
- **Circular strings.** Run the scan on $s s$ and cap the length at $n$.

## Examples

| $s$ | answer | a longest substring |
| --- | --- | --- |
| $\texttt{abcabcbb}$ | 3 | $\texttt{abc}$, at 0 |
| $\texttt{bbbbb}$ | 1 | $\texttt{b}$, at 0 |
| $\texttt{pwwkew}$ | 3 | $\texttt{wke}$, at 2 |
| $\texttt{abba}$ | 2 | $\texttt{ab}$, at 0 |
| $\texttt{dvdf}$ | 3 | $\texttt{vdf}$, at 1 |
| $\texttt{tmmzuxt}$ | 5 | $\texttt{mzuxt}$, at 2 |
| empty string | 0 | |

In $\texttt{pwwkew}$, the string $\texttt{pwke}$ has distinct characters, but it is a subsequence, not a substring. The input $\texttt{abba}$ is the standard test for a left end that moves back by mistake; the [algorithm page](/sliding-window-longest-substring/) explains it.

## Known algorithms

| algorithm | time | extra space |
| --- | --- | --- |
| check every substring with a set | $O(n^3)$, or $O(n^2)$ by growing each start | $O(\sigma)$ |
| sliding window with a set, shrink step by step | $O(n)$ expected | $O(\min(n, \sigma))$ |
| [sliding window with last positions](/sliding-window-longest-substring/) | $\Theta(n + \sigma)$ with an array | $\Theta(\sigma)$ |
| sort-based, comparison model | $O(n \log n)$ | $O(n)$ |

**The window method.** For each end $r$, let $L(r)$ be the smallest start such that $s[L(r) \ldots r]$ is repeat-free, and $p(r)$ the last position before $r$ of the character $s_r$, or $-1$. Then $L(r) = \max(L(r - 1), p(r) + 1)$. The answer is $\max_r (r - L(r) + 1)$. The left end only moves right, and the invariant "$l = L(r)$" after step $r$ shows that every end $r$ is paired with its best start. A start that the left end passes gives a window with a repeat, and every longer window with this start keeps the repeat, so no candidate is lost.

**Comparison model.** If characters can only be compared, compute $p(r)$ for all $r$ by sorting the pairs $(s_r, r)$; then run the same recurrence. This takes $O(n \log n)$ time. A balanced search tree of the characters in the window gives the same bound online.

## Bounds

**Upper bound.** $\Theta(n + \sigma)$ time with an array indexed by character, or $O(n)$ expected time with hashing.

**Lower bound, reads.** Every algorithm reads all $n$ characters on some input: for a string of $n$ distinct characters the answer is $n$, and changing any unread character to a copy of another one makes the answer smaller.

**Lower bound, comparisons.** The answer is $n$ if and only if all characters are distinct. So the problem contains [element distinctness](/element-distinctness/), and needs $\Omega(n \log n)$ comparisons in the algebraic decision tree model, by the [element distinctness lower bound](/element-distinctness-lower-bound/). The linear-time algorithms use the characters as indices or hash keys, which this model does not allow.

## Reductions

- **From element distinctness.** As above: decide distinctness by comparing the answer with $n$.
- **To the sliding window template.** The predicate "repeat-free" is closed under sub-intervals, the [monotone window property](/monotone-window-property/), so the longest valid window for each end is found by a left end that never moves back.
- **To the previous-occurrence array.** The answer depends only on the array $p(0), \ldots, p(n-1)$. Any method that computes it, such as sorting, gives an algorithm.

## Applications

- **Teaching sliding windows.** It is the most common first example of a variable-size window.
- **Data streams.** The longest run of distinct items, such as distinct user ids in a log, measures how long a stream goes without a repeat.
- **Testing random generators.** The position of the first repeat in a sequence of outputs is the quantity behind birthday-type tests; this scan finds the longest repeat-free run in a long output.

## References
