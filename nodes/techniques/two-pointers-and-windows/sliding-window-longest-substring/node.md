---
tag: H69540
kind: algorithm
slug: sliding-window-longest-substring
name: Sliding window for longest distinct substring
aliases:
- two-pointer distinct window
area: techniques/two-pointers-and-windows
level: intro
summary: Extend the right end, shrink the left end past duplicates, and track the maximum window length; O(n) time.
solves: [longest-substring-without-repeating-characters]
model: word-ram
complexity:
  vars: {n: the length of the string, σ: the size of the alphabet}
  time: {worst: Θ(n + σ), average: Θ(n + σ), best: Θ(n + σ)}
  space: {extra: Θ(σ)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [sliding-window, longest-substring-without-repeating-characters, hash-table, loop-invariant]
see_also: [longest-substring-without-repeating-characters, longest-substring-with-k-distinct, sliding-window, monotone-window-property, distinct-count-two-pointers, element-distinctness, minimum-window-substring-algorithm]
sources:
  - url: https://leetcode.com/problems/longest-substring-without-repeating-characters/
    title: LeetCode, problem 3, Longest Substring Without Repeating Characters
    locator: problem statement
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Data structures (hashing, and arrays indexed by key)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm design techniques (scanning algorithms that keep the answer for the prefix and for the part that ends at the current position)
---

The sliding window algorithm for the longest substring without repeating characters scans the string once and keeps, for each position $r$, the longest window that ends at $r$ and has no repeated character. It stores the last position of each character. When the character at $r$ already occurs in the window, the left end jumps to one past that occurrence, and it never moves back. It solves the [longest substring without repeating characters](/longest-substring-without-repeating-characters/) in $\Theta(n + \sigma)$ time with an array over an alphabet of size $\sigma$, or in $O(n)$ expected time with a [hash table](/hash-table/).

## In plain words

Read the string from left to right and keep a window of letters that are all different. Also remember, for each letter, where you saw it last.

When the next letter is new for the window, the window grows by one. When the letter is already in the window, the window must lose everything up to and including that earlier copy, so the left edge jumps to just after it. After each letter, compare the window length with the best so far.

One detail matters: the earlier copy may lie to the left of the window already. Then it is not in the window, and the left edge must not move back to it.

## The problem

**Input.** A string $s = s_0 \cdots s_{n-1}$ over an alphabet of size $\sigma$.

**Output.** The largest $L$ such that some substring $s[i \ldots i+L-1]$ has $L$ distinct characters, and the smallest such start $i$. For $n = 0$ the output is $(0, 0)$.

## The algorithm

```pseudo id=main
LONGEST-DISTINCT-SUBSTRING(s[0 .. n − 1])
L1  last[c] ← −1 for every character c; l ← 0; best ← 0; start ← 0
L2  for r ← 0 to n − 1 do
L3      l ← max(l, last[s_r] + 1)
L4      last[s_r] ← r
L5      if r − l + 1 > best then best ← r − l + 1; start ← l
L6  return (best, start)
```

Line L3 moves the left end past the previous copy of $s_r$, but only if that copy is inside the window. Line L4 records the new last position. Line L5 keeps the leftmost longest window, because it replaces the best only on a strict increase.

## Example

$s = \texttt{abcabcbb}$, with $n = 8$. The column "prev" is $last[s_r]$ before line L4.

| $r$ | $s_r$ | prev | $l$ | window | best | start |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | a | $-1$ | 0 | a | 1 | 0 |
| 1 | b | $-1$ | 0 | ab | 2 | 0 |
| 2 | c | $-1$ | 0 | abc | 3 | 0 |
| 3 | a | 0 | 1 | bca | 3 | 0 |
| 4 | b | 1 | 2 | cab | 3 | 0 |
| 5 | c | 2 | 3 | abc | 3 | 0 |
| 6 | b | 4 | 5 | cb | 3 | 0 |
| 7 | b | 6 | 7 | b | 3 | 0 |

The output is $(3, 0)$, the substring $\texttt{abc}$. Other inputs: $\texttt{bbbbb}$ gives $(1, 0)$, $\texttt{pwwkew}$ gives $(3, 2)$ for $\texttt{wke}$, and $\texttt{abba}$ gives $(2, 0)$.

## Correctness

For an end $r$, let $L(r)$ be the smallest $i$ such that $s[i \ldots r]$ has no repeated character. Let $p(r)$ be the largest $j < r$ with $s_j = s_r$, or $-1$ if there is none. Then
$$ L(0) = 0, \qquad L(r) = \max\bigl(L(r-1),\, p(r) + 1\bigr) \text{ for } r \ge 1. $$
A window $s[i \ldots r]$ has no repeat if and only if $s[i \ldots r-1]$ has no repeat and $s_r$ does not occur in $s[i \ldots r-1]$. The first condition is $i \ge L(r-1)$, and the second is $i > p(r)$.

The loop keeps this invariant, after line L5 of step $r$:

> **(U)** $l = L(r)$; for each character $c$, $last[c]$ is the largest $j \le r$ with $s_j = c$, or $-1$; and $(best, start)$ is the length and the smallest start of a longest repeat-free window that ends at some $r' \le r$.

*Why no longest window is skipped.* Line L3 computes $\max(L(r-1), p(r) + 1)$, because $last[s_r] = p(r)$ before line L4. So $l = L(r)$, and $s[l \ldots r]$ is the longest repeat-free window that ends at $r$. Every repeat-free substring ends at some $r$ and starts at or after $L(r)$, so it is no longer than the window that the loop examines at $r$. The left end only skips starts $i < L(r)$, and each of these windows $s[i \ldots r]$ has a repeat, so every longer window $s[i \ldots r']$ with $r' > r$ has the same repeat. This is the [monotone window property](/monotone-window-property/). The [proof page](proofs/correctness.md) gives the full induction, including the leftmost start.

## Complexity

- **Time.** Line L1 takes $\Theta(\sigma)$ with an array of size $\sigma$. The loop runs $n$ times, with $O(1)$ work each time. In total $\Theta(n + \sigma)$. With a hash table instead of an array, $O(n)$ expected time.
- **Space.** $\Theta(\sigma)$ for the array, or $O(\min(n, \sigma))$ for a hash table with only the characters that occur.
- **Left-end moves.** The left end jumps, so there is no inner loop at all. The version that moves $l$ one step at a time and removes characters from a set also takes $O(n)$ time, with at most $2n$ set operations.

## Properties

- **Online.** Step $r$ needs only $s_0, \ldots, s_r$, and after it the answer for the prefix is known.
- **Not comparison-based.** It indexes a table by character. Over an alphabet with only comparisons, the problem needs $\Omega(n \log n)$ comparisons, since it decides [element distinctness](/element-distinctness/) when the answer is $n$.
- **One pass, no inner loop.** The left end moves by jumps.

## Variants and improvements

- **Set and shrink.** Keep a set of the characters in the window. For each $r$, while $s_r$ is in the set, remove $s_l$ and increase $l$; then add $s_r$. This uses no positions, and each character enters and leaves the set once.
- **All maximal windows.** Report every $r$ with $r - L(r) + 1 = best$ to list all longest windows.
- **At most $k$ copies of each character.** Keep counts and shrink while the count of $s_r$ exceeds $k$.
- **At most $k$ distinct characters.** A different limit; see [longest substring with at most $k$ distinct characters](/longest-substring-with-k-distinct/).
- **Small alphabet speed-up.** The answer is at most $\sigma$, so the scan can stop early once $best = \sigma$.

## When to use it

Use it for the longest repeat-free substring or subarray, and as a pattern for any window whose bad event is "the new item repeats an item in the window". For values in a large domain, use a hash table for $last$.

## Pitfalls

- **No max in line L3.** Setting $l \leftarrow last[s_r] + 1$ can move the left end back. On $\texttt{abba}$, at $r = 3$ the last $\texttt{a}$ is at 0, so $l$ goes from 2 back to 1, and the window $\texttt{bba}$ with a repeated $\texttt{b}$ gives the wrong answer 3 instead of 2.
- **Updating $last$ before line L3.** Then $last[s_r] = r$ and $l$ becomes $r + 1$, an empty window.
- **Signed characters.** In C, a `char` above 127 can be negative and index outside the array. Use an unsigned type.
- **Unicode.** A string type may store code units, not characters. Decide which unit counts as a character before the scan.

## Implementations

## History

The problem is a standard exercise in programming interviews and online judges, where it is LeetCode problem 3. The scanning pattern, which keeps the best answer for the prefix and the best answer that ends at the current position, is the pattern of Kadane's scan for the maximum subarray that Bentley describes in Column 8 of *Programming Pearls*.

## References
