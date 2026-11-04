---
tag: 380AMB
kind: algorithm
slug: minimum-window-substring-algorithm
name: Sliding window for minimum window substring
aliases:
- two-pointer minimum window
area: techniques/two-pointers-and-windows
level: core
summary: Expand the right pointer until the window is valid, then shrink the left pointer while it stays valid; O(n + m) time.
solves: [minimum-window-substring]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the size of the alphabet}
  time: {worst: Θ(n + m + σ), average: Θ(n + m + σ), best: Θ(n + m + σ)}
  space: {extra: Θ(σ)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [minimum-window-substring, sliding-window, monotone-window-property, frequency-vector]
see_also: [minimum-window-substring, minimum-size-subarray-sum, minimum-window-subsequence, sliding-window, monotone-window-property, sliding-window-longest-substring, frequency-vector, hash-table]
sources:
  - url: https://leetcode.com/problems/minimum-window-substring/
    title: LeetCode, problem 76, Minimum Window Substring
    locator: problem statement and the O(m + n) follow-up
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Data structures (hashing and arrays indexed by key)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm design techniques (scanning algorithms)
---

The sliding window algorithm for the minimum window substring finds the shortest substring of a text $s$ that contains every character of a pattern $t$, with at least the multiplicity it has in $t$. It keeps a table $need$ of how many copies of each character the window still lacks, and a counter $missing$ of the copies that are still needed in total. The right end grows the window until $missing = 0$; then the left end shrinks it while it stays valid, and each valid window is a candidate. Both ends only move right, so the time is $\Theta(n + m + \sigma)$. It solves the [minimum window substring](/minimum-window-substring/) problem. Its correctness rests on the [monotone window property](/monotone-window-property/): a window that contains the pattern still contains it when it grows.

## In plain words

You have a long text and a short list of letters, with repeats allowed. You want the shortest piece of the text that has all these letters.

Keep a shopping list: how many of each letter you still need. Move the right edge of the window and cross letters off the list. When the list is empty, the window has everything. Now move the left edge to make the window shorter. Each time you drop a letter that the list needs, the list gets that letter back, and the window is no longer complete. Then move the right edge again. Write down the shortest complete window you see.

## The problem

**Input.** A text $s = s_0 \cdots s_{n-1}$ and a pattern $t = t_0 \cdots t_{m-1}$ over an alphabet of size $\sigma$, with $m \ge 1$.

**Output.** A shortest substring $s[i \ldots j]$ such that each character $c$ occurs in it at least $\mathrm{cnt}_t(c)$ times, where $\mathrm{cnt}_t(c)$ is the number of copies of $c$ in $t$. Among the shortest ones, the algorithm returns the one with the smallest start. If no substring qualifies, the output is the empty string.

Call such a substring *valid*.

## The algorithm

```pseudo id=main
MIN-WINDOW(s[0 .. n − 1], t[0 .. m − 1])
L1  need[c] ← cnt_t(c) for every c; missing ← m; l ← 0; bestlen ← ∞; beststart ← 0
L2  for r ← 0 to n − 1 do
L3      if need[s_r] > 0 then missing ← missing − 1
L4      need[s_r] ← need[s_r] − 1
L5      while missing = 0 do
L6          if r − l + 1 < bestlen then bestlen ← r − l + 1; beststart ← l
L7          need[s_l] ← need[s_l] + 1
L8          if need[s_l] > 0 then missing ← missing + 1
L9          l ← l + 1
L10 if bestlen = ∞ then return the empty string else return s[beststart .. beststart + bestlen − 1]
```

For the window $s[l \ldots r]$, $need[c] = \mathrm{cnt}_t(c) - \mathrm{cnt}_{s[l \ldots r]}(c)$ can be negative, which means the window has extra copies of $c$. The counter $missing$ is $\sum_c \max(need[c], 0)$, the number of copies of pattern characters still lacking. So the window is valid exactly when $missing = 0$, and the test costs $O(1)$ instead of a scan of the alphabet.

Line L3 decreases $missing$ only when the new character was still needed. Lines L7 and L8 increase it only when the dropped character becomes needed again.

## Example

$s = \texttt{ADOBECODEBANC}$ and $t = \texttt{ABC}$, so $n = 13$ and $m = 3$. The table lists every window that the loop of line L5 examines.

| $r$ | window $s[l \ldots r]$ | $l$ | length | recorded |
| --- | --- | --- | --- | --- |
| 5 | $\texttt{ADOBEC}$ | 0 | 6 | yes, best 6 |
| 10 | $\texttt{DOBECODEBA}$ | 1 | 10 | no |
| 10 | $\texttt{OBECODEBA}$ | 2 | 9 | no |
| 10 | $\texttt{BECODEBA}$ | 3 | 8 | no |
| 10 | $\texttt{ECODEBA}$ | 4 | 7 | no |
| 10 | $\texttt{CODEBA}$ | 5 | 6 | no, not shorter |
| 12 | $\texttt{ODEBANC}$ | 6 | 7 | no |
| 12 | $\texttt{DEBANC}$ | 7 | 6 | no |
| 12 | $\texttt{EBANC}$ | 8 | 5 | yes, best 5 |
| 12 | $\texttt{BANC}$ | 9 | 4 | yes, best 4 |

At $r = 5$ the window first contains $\texttt{A}$, $\texttt{B}$ and $\texttt{C}$. Dropping $\texttt{A}$ makes it invalid. At $r = 10$ a new $\texttt{A}$ arrives, and the left end moves up to the $\texttt{C}$ at position 5, the last start that keeps the window valid. At $r = 12$ the left end moves to the $\texttt{B}$ at position 9. The output is $\texttt{BANC}$.

## Correctness

For a start $i$, let $e(i)$ be the smallest $j$ such that $s[i \ldots j]$ is valid, or $\infty$. The shortest valid window that starts at $i$ is $s[i \ldots e(i)]$, so the answer is a window $s[i \ldots e(i)]$ that minimizes $e(i) - i + 1$.

**Monotone property.** If $s[i \ldots j]$ is valid and $i' \le i$, $j' \ge j$, then $s[i' \ldots j']$ is valid, because it has at least as many copies of each character. So $e$ is non-decreasing: $e(i) \le e(i + 1)$.

The algorithm keeps this invariant at the start of each step $r$:

> **(W)** $need[c] = \mathrm{cnt}_t(c) - \mathrm{cnt}_{s[l \ldots r-1]}(c)$ for all $c$, $missing = \sum_c \max(need[c], 0)$, and $s[l \ldots r-1]$ is not valid; for each start $i < l$, $e(i) \le r - 1$, and the window $s[i \ldots e(i)]$ was examined at line L6.

*Why no shortest window is skipped.* The loop of line L5 runs at step $r$ only while $s[l \ldots r]$ is valid, and it examines each such window at line L6 before it drops $s_l$. At the first examination at step $r$, the window $s[l \ldots r-1]$ is not valid by (W). For each later examination, $l$ has grown, and $s[l \ldots r-1]$ is a part of the window $s[l_0 \ldots r-1]$ with the old left end $l_0$, so it is not valid either. So each window $s[l \ldots r]$ examined at step $r$ has $e(l) = r$: it is the shortest valid window with start $l$. Each start is passed only after this window is examined. The starts that are never passed have no valid window, since $s[l \ldots n-1]$ is not valid at the end, and neither is any part of it. So every candidate $s[i \ldots e(i)]$ is examined, and line L6 keeps the shortest one, with the smallest start among ties because it replaces only on a strict decrease.

The [proof page](proofs/correctness.md) gives the full argument, including the bookkeeping of $missing$.

## Complexity

- **Time.** Line L1 takes $\Theta(m + \sigma)$. The right end moves $n$ times and the left end at most $n$ times, and each move costs $O(1)$. In total $\Theta(n + m + \sigma)$. With a hash table instead of an array, $O(n + m)$ expected time.
- **Space.** $\Theta(\sigma)$ for the table, or $O(m)$ for a hash table that holds only the characters of $t$ and ignores the others.
- **No inner rescans.** The counter $missing$ makes the validity test $O(1)$. A version that checks all $\sigma$ counts after each move takes $O(n \sigma)$.

## Properties

- **Online in the text.** Step $r$ needs only $s_0, \ldots, s_r$, so the text can be a stream; the pattern must be known first.
- **Not comparison-based.** It indexes a table by character.
- **Leftmost shortest.** Among the shortest valid windows, it returns the one with the smallest start.

## Variants and improvements

- **Filtered text.** Keep only the positions of $s$ whose characters occur in $t$, and run the window over this list. This saves time when few characters of $s$ are in $t$; the window length is computed from the original positions.
- **Order matters.** If the pattern must appear in order as a subsequence of the window, the window property changes; see [minimum window subsequence](/minimum-window-subsequence/).
- **Sets instead of multisets.** If each character of $t$ is needed once, set $need[c] = 1$ for each distinct character, and $missing$ to the number of distinct characters.
- **All shortest windows.** Record every examined window whose length equals the minimum.
- **Numbers with weights.** The same shape solves [minimum size subarray sum](/minimum-size-subarray-sum/), with the sum in place of $missing$.

## When to use it

Use it when the answer is the shortest contiguous window that satisfies a condition that stays true when the window grows, such as "contains these items", and when the condition can be updated in $O(1)$ when one item enters or leaves.

## Pitfalls

- **Testing validity with the wrong counter.** Decreasing $missing$ for every character that enters, instead of only when $need[s_r] > 0$, counts extra copies as progress. On $s = \texttt{AAB}$ and $t = \texttt{AB}$, this makes $\texttt{AA}$ look complete.
- **Updating $need$ before the test of line L3.** Lines L3 and L4 must test, then decrease. In the other order, the test sees the value after the decrease and misses the last needed copy.
- **Shrinking past the last valid start.** If the left end is advanced by a fixed rule, such as "while $s_l$ is not in $t$", it stops too early: in the example at $r = 10$, it would stop at the $\texttt{B}$ at position 3, because $\texttt{B}$ is in $t$, although the window stays valid up to the start 5. The loop must test validity, which $missing$ does.
- **Pattern longer than the text.** Then no window is valid, and the output is empty.
- **Empty pattern.** With $m = 0$, line L1 sets $missing = 0$; the convention of the caller decides if the answer is the empty string. The implementation returns it at once.

## Implementations

## History

The problem is a standard exercise on online judges, where it is LeetCode problem 76, and it is the standard example of a minimum-length window with a multiset condition. The method is the sliding window pattern with a count table; the $missing$ counter is the usual trick to make the validity test take constant time.

## References
