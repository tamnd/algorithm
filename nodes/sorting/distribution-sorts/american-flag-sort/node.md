---
tag: GW15GA
kind: algorithm
slug: american-flag-sort
name: American flag sort
aliases:
- In-place MSD radix sort
- In-place radix sort
area: sorting/distribution-sorts
level: advanced
summary: In-place MSD radix sort that permutes keys into digit bins by cycle-following, named for the Dutch flag problem.
solves: [string-sorting, integer-sorting]
model: word-ram
complexity:
  vars: {n: the number of strings, D: the total length of the distinguishing prefixes, R: the alphabet size, L: the largest distinguishing prefix length}
  time: {worst: O(R (n + D)), best: Θ(n + R)}
  space: {extra: O(R L)}
properties: {stable: false, in_place: true, adaptive: true, online: false, deterministic: true, comparison: false, recursive: true}
history: {year: 1993, people: [Peter M. McIlroy, Keith Bostic, M. Douglas McIlroy], note: in-place MSD radix sort for strings in the BSD library}
prereqs: [msd-radix-sort]
see_also: [msd-radix-sort, counting-sort, in-place-permutation, cycle-leader-permutation, dutch-national-flag, three-way-radix-quicksort, multikey-quicksort, string-sorting]
sources:
  - paper: Peter M. McIlroy, Keith Bostic and M. Douglas McIlroy, Engineering radix sort, Computing Systems 6(1), 1993, pages 5 to 27
    locator: the section on American flag sort (the two passes of each step, counting and permuting along cycles, and the explicit stack of piles)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.1, String Sorts (MSD string sort, Algorithm 5.2, and the exercises on in-place key-indexed counting)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.5, Sorting by Distribution (the most significant digit first method)
---

American flag sort is an in-place [MSD radix sort](/msd-radix-sort/): at each step it counts the keys of a range by their character at index $d$, computes where each bucket starts, and then moves the keys into their buckets by swaps along cycles, without a second array. McIlroy, Bostic and McIlroy (1993) introduced it for the BSD string sort, and the name plays on Dijkstra's [Dutch national flag](/dutch-national-flag/) problem, which splits into three colours, while this method splits into many stripes at once. It reads the same characters as MSD radix sort, $O(n + D)$ for a constant alphabet, but needs only $O(R)$ counters per open level instead of a buffer of $n$ items. The price is that it is not stable.

## In plain words

Picture a shelf of folders that must go into labelled sections, A, B, C and so on, on the same shelf. First count how many folders go into each section. Now you know where each section starts and ends. Then walk along the shelf. If the folder in front of you belongs to the current section, leave it and go on. If not, swap it with the first folder that is not yet in place in the section where it belongs. Each swap puts one folder in its final section, so the walk ends after at most one swap per folder.

After that, every section holds the right folders. Sort each section the same way by the next letter. No second shelf is ever needed.

## The problem

The input is an array $A[0 \ldots n-1]$ of strings over $\{0, \ldots, R-1\}$, or of integers split into $R$-ary digits from the top. The output is the strings in [lexicographic order](/lexicographic-order/). As in MSD radix sort, $c(s, d) = s[d] + 1$ if $d < |s|$ and $c(s, d) = 0$ if $s$ has ended, so the bucket 0 of strings that ended comes first.

## The algorithm

A task $(lo, hi, d)$ means that the strings of $A[lo \ldots hi-1]$ agree on their first $d$ characters.

```pseudo id=main
AMERICAN-FLAG-SORT(A, n, R)
L1  S ← a stack that holds the task (0, n, 0)
L2  while S is not empty do
L3      (lo, hi, d) ← pop S
L4      if hi − lo ≤ 1 then continue
L5      C[r] ← the number of i in [lo, hi) with c(A[i], d) = r, for r = 0 .. R
L6      start[r] ← lo + C[0] + ... + C[r − 1]; next[r] ← start[r]; end[r] ← start[r] + C[r]
L7      for r ← 0 to R do
L8          while next[r] < end[r] do
L9              b ← c(A[next[r]], d)
L10             if b = r then next[r] ← next[r] + 1
L11             else swap A[next[r]] and A[next[b]]; next[b] ← next[b] + 1
L12     for r ← R down to 1 do if C[r] ≥ 2 then push (start[r], end[r], d + 1) onto S
L13 return A
```

Lines L5 and L6 are the counting pass of a [counting sort](/counting-sort/). Lines L7 to L11 are the permutation pass. For each bucket $b$, the positions $A[start[b] \ldots next[b] - 1]$ already hold strings of bucket $b$. Line L11 sends the string at $next[r]$ to the first free place of its own bucket $b$ and brings back a string that has not been placed. Each swap places one string for good, so the pass makes at most $hi - lo$ swaps. Line L12 skips bucket 0, whose strings ended and are equal, and buckets with one string.

## Example

Sort $A = [\text{she}, \text{sells}, \text{sea}, \text{shells}, \text{by}, \text{the}, \text{sea}, \text{shore}]$. At $d = 0$ the counts are b: 1, s: 6, t: 1, so bucket b is $[0, 1)$, bucket s is $[1, 7)$ and bucket t is $[7, 8)$. The permutation pass at $d = 0$ makes these swaps.

| Step | Current bucket | String at next[r] | Its bucket | Action | Array after the step |
|---|---|---|---|---|---|
| 1 | b, position 0 | she | s | swap with position 1 | sells she sea shells by the sea shore |
| 2 | b, position 0 | sells | s | swap with position 2 | sea she sells shells by the sea shore |
| 3 | b, position 0 | sea | s | swap with position 3 | shells she sells sea by the sea shore |
| 4 | b, position 0 | shells | s | swap with position 4 | by she sells sea shells the sea shore |
| 5 | b, position 0 | by | b | keep | by she sells sea shells the sea shore |
| 6 | s, positions 1 to 4 | she, sells, sea, shells | s | keep each | by she sells sea shells the sea shore |
| 7 | s, position 5 | the | t | swap with position 7 | by she sells sea shells shore sea the |
| 8 | s, positions 5 to 6 | shore, sea | s | keep each | by she sells sea shells shore sea the |

Bucket t is then full. The tasks $(1, 7, 1)$, $(1, 4, 2)$, $(1, 3, 3)$, $(4, 7, 2)$ and $(4, 6, 3)$ follow, as in MSD radix sort, and the result is $[\text{by}, \text{sea}, \text{sea}, \text{sells}, \text{she}, \text{shells}, \text{shore}, \text{the}]$ after 9 swaps in total.

## Correctness

The counting pass gives each bucket a block of positions of the right size, in the order of the buckets. In the permutation pass, the invariant is that each position before $next[b]$ in the block of bucket $b$ holds a string of bucket $b$. A swap in line L11 extends one block and never changes a placed string. When the scan of bucket $r$ ends, its whole block holds strings of bucket $r$. So after the pass the range is sorted by $c(\cdot, d)$, which is what one step of MSD radix sort needs, and the rest of the argument is the one for [MSD radix sort](/msd-radix-sort/), except that stability is lost. The full proof is below.

## Complexity

- **Time.** One step on a task with $m$ strings costs $\Theta(m + R)$: one count for each string, $R + 1$ prefix sums, at most $m$ swaps, and $R + 1$ bucket scans. The tasks and the characters read are those of MSD radix sort, so the total is $O(n + D + R\,T)$, where $T \le (n + D)/2$ is the number of tasks with at least two strings. This is $O(R(n + D))$ in the worst case and $O(n + D)$ for a constant $R$.
- **Reads.** Each string has its character at $d$ read twice in a step, once to count and once or more to place it; the number of reads is still $O(n + D)$.
- **Space.** No buffer. Each open task needs $O(R)$ counters, but the counters can be freed before the children start, so only the stack of pending tasks grows: at most $R$ tasks per level, $O(R L)$ in the worst case, where $L$ is the largest distinguishing prefix length.
- **Best case.** If all first characters differ, one step costs $\Theta(n + R)$.

## Properties

- **In place.** Apart from the counters and the stack, it uses $O(1)$ extra space.
- **Not stable.** The swaps move strings past each other. Equal strings are identical, so this matters only with satellite data.
- **Adaptive.** It stops at the distinguishing prefixes.
- **Not a comparison sort.** Characters are array indices.

## Variants and improvements

- **Cut-off to insertion sort.** For small tasks, $R + 1$ counters cost more than the sort. McIlroy, Bostic and McIlroy switch to a simple comparison sort for small piles.
- **Cycle leader form.** In place of swaps, hold one string, find its target, put it there and pick up the string that was there, until the cycle closes. This is a [cycle leader permutation](/cycle-leader-permutation/) and uses fewer writes than swaps.
- **Integers.** With 8-bit digits on 32-bit or 64-bit keys, the same method is an in-place MSD radix sort for integers.
- **Larger digits for integers.** With 16-bit digits there are fewer levels but $2^{16}$ counters per task, so a hybrid that uses 8-bit digits for small tasks is common.

## When to use it

Use American flag sort when MSD radix sort is a good fit but memory is tight: large arrays of byte strings or integer keys where a second array of $n$ pointers is too costly. When stability matters, use [MSD radix sort](/msd-radix-sort/). For large alphabets, [three-way radix quicksort](/three-way-radix-quicksort/) avoids the $R$ counters per task.

## Pitfalls

- **Advancing $next[r]$ after a swap.** After line L11, the string that came to $next[r]$ is new and has not been tested. Only $next[b]$ advances; $next[r]$ advances in line L10.
- **Using the moved $next$ values for the children.** The children need the block bounds $start[r]$ and $end[r]$, not the final $next[r]$; keep a copy of the starts.
- **Bucket 0.** As in MSD radix sort, the strings that ended form bucket 0, and they must not be pushed again.
- **Large alphabets.** Counters for each task make small tasks slow. Without a cut-off, a long common prefix of a few strings costs $R$ per character.

## Implementations

## History

McIlroy, Bostic and McIlroy (1993) developed American flag sort for the radix sorting routines of the BSD Unix library and described it in "Engineering radix sort", together with an MSD radix sort that uses a buffer and a stack of pending piles. They named it after the Dutch national flag problem of Dijkstra, as a flag with many stripes. Knuth (Section 5.2.5) describes the most significant digit first method on which it is based.

## References
