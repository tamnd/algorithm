---
tag: AHYDH3
kind: problem
slug: longest-substring-with-k-distinct
name: Longest substring with at most k distinct characters
aliases:
- k distinct window
area: techniques/two-pointers-and-windows
level: intro
summary: Find the longest substring containing at most k distinct characters, using a sliding window with counts.
prereqs: [sliding-window, hash-table, frequency-vector]
see_also: [longest-subarray-with-at-most-k-distinct, longest-substring-without-repeating-characters, sliding-window-longest-substring, distinct-count-two-pointers, monotone-window-property, sliding-window-distinct-count, element-distinctness-lower-bound, minimum-window-substring]
sources:
  - url: https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/
    title: LeetCode, problem 340, Longest Substring with At Most K Distinct Characters
    locator: problem statement
  - url: https://leetcode.com/problems/subarrays-with-k-different-integers/
    title: LeetCode, problem 992, Subarrays with K Different Integers
    locator: problem statement (counting windows with exactly k distinct values)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Data structures (hashing) and Chapter 4, Sorting (uniqueness and frequency)
---

The problem asks for the longest substring of a string $s$ that contains at most $k$ distinct characters. A [sliding window](/sliding-window/) with a table of character counts solves it in $O(n)$ time: the right end moves one step at a time, and the left end moves right only while the window has more than $k$ distinct characters. The method works because a substring with at most $k$ distinct characters keeps this property when it is cut shorter, which is the [monotone window property](/monotone-window-property/). For $k = 1$ the answer is the longest run of one character. The case where every character may appear at most once is the related [longest substring without repeating characters](/longest-substring-without-repeating-characters/). The same problem on arrays of numbers is the [longest subarray with at most $k$ distinct values](/longest-subarray-with-at-most-k-distinct/).

## In plain words

You read a long string and want the longest stretch of it that uses only a few different letters, at most $k$ of them.

Keep a window and a tally of how many times each letter is in it. Add letters on the right one at a time. If the window now has too many different letters, remove letters from the left until one letter's tally drops to zero, so that the window is allowed again. After each step, compare the window length with the best so far.

The left edge never needs to go back. If a window has too many different letters, every longer window that contains it has too many as well.

## Definition

**Input.** A string $s = s_0 s_1 \cdots s_{n-1}$ over an alphabet $\Sigma$, and an integer $k \ge 0$.

**Output.** The largest length $j - i$ over $0 \le i \le j \le n$ such that the substring $s[i \ldots j-1]$ has at most $k$ distinct characters, and in the search version one such pair $(i, j)$. The empty substring always counts, so the answer is 0 when $k = 0$ or $n = 0$.

**Model.** The algorithms below use a count table indexed by characters: an array of size $|\Sigma|$ for a small alphabet, or a [hash table](/hash-table/) for a large one.

## Variants

- **Exactly $k$ distinct.** If $s$ has at least $k$ distinct characters, the longest substring with exactly $k$ distinct characters has the same length as the longest with at most $k$. A longest window with fewer than $k$ distinct characters that is not all of $s$ could grow by one character and still have at most $k$, which contradicts its length. If $s$ has fewer than $k$ distinct characters, no such substring exists.
- **Count the substrings.** The number of substrings with at most $k$ distinct characters is $\sum_r (r - l(r) + 1)$, where $l(r)$ is the left end of the window after step $r$. The number with exactly $k$ is the count for at most $k$ minus the count for at most $k - 1$.
- **No repeated characters.** "Each character at most once" is a different limit, on counts instead of on distinct characters. See [longest substring without repeating characters](/longest-substring-without-repeating-characters/).
- **Streaming.** On a stream with a fixed window length, keep the number of distinct values in the window: [sliding window distinct count](/sliding-window-distinct-count/).
- **Arrays of numbers.** The same window works for any values that a hash table can hold: [longest subarray with at most $k$ distinct](/longest-subarray-with-at-most-k-distinct/).

## Examples

**Standard instance.** $s = \texttt{eceba}$ and $k = 2$. The answer is 3, from $\texttt{ece}$.

| $r$ | $s_r$ | $l$ after shrinking | window | distinct | best |
| --- | --- | --- | --- | --- | --- |
| 0 | e | 0 | e | 1 | 1 |
| 1 | c | 0 | ec | 2 | 2 |
| 2 | e | 0 | ece | 2 | 3 |
| 3 | b | 2 | eb | 2 | 3 |
| 4 | a | 3 | ba | 2 | 3 |

At $r = 3$ the window $\texttt{eceb}$ has 3 distinct characters. The left end removes $\texttt{e}$ (the count of $\texttt{e}$ drops to 1) and then $\texttt{c}$ (its count drops to 0), and the window $\texttt{eb}$ is allowed again.

**Longer instance.** $s = \texttt{aabacbebebe}$ and $k = 3$ give 7, from $\texttt{cbebebe}$ at positions 4 to 10.

**Edge cases.** $s = \texttt{aa}$ and $k = 1$ give 2. Any $s$ with $k \ge$ the number of distinct characters of $s$ gives $n$.

## Known algorithms

**Sliding window with counts.** Keep $l = 0$, a count table $c$ that starts at zero, the number $d$ of characters with $c > 0$, and $best = 0$. For $r = 0, \ldots, n - 1$: increase $c[s_r]$, and increase $d$ if it became 1. While $d > k$: decrease $c[s_l]$, decrease $d$ if it became 0, and increase $l$. Then set $best \leftarrow \max(best, r - l + 1)$.

For an end $r$, let $L(r)$ be the smallest $i$ such that $s[i \ldots r]$ has at most $k$ distinct characters. The answer is $\max_r (r - L(r) + 1)$. If $s[i \ldots r]$ has at most $k$ distinct characters, so does $s[i' \ldots r']$ for $i \le i' \le r' \le r$. So $L$ is non-decreasing: $L(r+1) \ge L(r)$. The loop keeps, after the inner loop of step $r$:

> **(K)** $l = L(r)$; $c$ holds the counts of the characters of $s[l \ldots r]$ and $d$ their number of distinct characters; and $best = \max_{r' \le r} (r' - L(r') + 1)$.

*Why no longest window is skipped.* Before step $r$, $l = L(r - 1) \le L(r)$, so the left end is not past the best start for $r$. The inner loop advances $l$ only while $s[l \ldots r]$ has more than $k$ distinct characters, so only while $l < L(r)$; it stops at the first $l$ where the window is allowed, which is $L(r)$. Each start that the loop drops is not allowed with end $r$, and by the monotone property it is not allowed with any later end either. So each $r$ sees its longest allowed window, and $best$ is the maximum over all ends.

*Cost.* $r$ and $l$ each move at most $n$ times, and each move updates one count. With an array of counts the time is $O(n + |\Sigma|)$; with a hash table it is $O(n)$ expected time and the table holds at most $k + 1$ keys.

**Variant with a map of last positions.** Keep, for each character in the window, the position of its last occurrence, in a structure ordered by position. When $d > k$, move $l$ to one past the smallest last position, and remove that character. With a balanced search tree this costs $O(n \log k)$ time, but it moves $l$ in one jump.

**Brute force.** For each start $i$, extend $j$ while the window is allowed: $\Theta(n^2)$ time.

## Bounds

**Linear time.** Each character must be read. Take $s = \texttt{aa} \cdots \texttt{a}$ and $k = 1$, with answer $n$. If the character at some position is not read, change it to $\texttt{b}$; the answer drops below $n$, and the algorithm cannot tell the two inputs apart. With counts in an array the sliding window is $O(n + |\Sigma|)$ in the worst case.

**Comparison model.** Over an alphabet with only equality and order comparisons, the problem is at least as hard as [element distinctness](/element-distinctness-lower-bound/): with $k = n - 1$, the answer is $n$ if and only if two characters of $s$ are equal. So $\Omega(n \log n)$ comparisons are needed in the algebraic decision tree model, and the $O(n)$ bound needs hashing or a small alphabet.

## Reductions

- **To the monotone window template.** The predicate "at most $k$ distinct characters" is closed under taking sub-intervals, so the longest allowed window for each end is found by a left end that only moves right.
- **Exactly $k$ by subtraction.** Count of windows with exactly $k$ distinct characters $=$ count with at most $k$ $-$ count with at most $k - 1$. Each count is one window pass.
- **From longest substring without repeats.** No reduction in general, but the window code is the same, with the test "$d > k$" replaced by "some count exceeds 1".

## Applications

- **Caches and working sets.** The longest stretch of a request log that touches at most $k$ distinct items is the longest run that a cache of size $k$ can serve with no miss after each of these items is loaded once.
- **Genomics and text.** Low-complexity regions: the longest region of a sequence with a small number of distinct symbols.
- **Teaching sliding windows.** It is the standard example of a window whose state is a count table with a distinct counter.

## References
