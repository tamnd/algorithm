---
tag: QSTAC1
kind: algorithm
slug: larsson-sadakane-algorithm
name: Larsson-Sadakane algorithm
aliases:
- Larsson-Sadakane suffix sort
- qsufsort
area: strings/suffix-structures
level: advanced
summary: A faster prefix-doubling suffix sort that skips already sorted groups.
solves: [suffix-array-construction]
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: true, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 1999
  people: [N. Jesper Larsson, Kunihiko Sadakane]
  note: First a Lund University technical report in 1999, with the journal version in Theoretical Computer Science in 2007; the program was distributed as qsufsort.
prereqs: [prefix-doubling, suffix-array, three-way-radix-quicksort]
see_also: [karp-miller-rosenberg-algorithm, manber-myers-algorithm, prefix-doubling, multikey-quicksort, sa-is, dc3-skew-algorithm, suffix-array-construction, burrows-wheeler-transform]
sources:
  - paper: doi:10.1016/j.tcs.2007.07.017
    title: N. Jesper Larsson and Kunihiko Sadakane, Faster suffix sorting, Theoretical Computer Science 387(3), 2007
    locator: the doubling with group numbers, the ternary-split quicksort, the combined sorted groups, and the O(n log n) worst-case bound
  - paper: doi:10.1145/1242471.1242472
    title: Simon J. Puglisi, William F. Smyth and Andrew H. Turpin, A taxonomy of suffix array construction algorithms, ACM Computing Surveys 39(2), 2007
    locator: the section on prefix-doubling algorithms, with Larsson-Sadakane among them
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948, the prefix-doubling sort on which the method improves
---

The Larsson-Sadakane algorithm builds the [suffix array](/suffix-array/) of a text by [prefix doubling](/prefix-doubling/): after the pass with the value $h$, the suffixes are sorted by their first $2h$ symbols. Unlike the [Manber-Myers algorithm](/manber-myers-algorithm/), it sorts only the groups of suffixes that are still tied, with a ternary-split quicksort on one integer key, and it skips the runs of suffixes whose rank is already final. It runs in $O(n \log n)$ worst-case time with $\Theta(n)$ extra words, and on real data it was for years among the fastest suffix sorts, distributed as the program qsufsort.

## In plain words

Sort all endings of a text by their first letter. Endings with different first letters are now in the right order for good; only endings with the same first letter are still tied. Each tied block is called a group.

Now look at a group whose members all start with the same $h$ letters. To break the tie, look $h$ letters further: the ending that starts there is already placed in some group, and the number of that group tells its order. Sort the group by these numbers. Members with equal numbers stay tied, but now they share $2h$ letters. Repeat with $2h$.

The trick that makes it fast: an ending alone in its group is finished, and a later pass jumps over whole stretches of finished endings without looking at them. Most of the work is done in the first passes.

## The problem

Given a text $T = T[0 \ldots n-1]$ over a general ordered alphabet, compute its suffix array $SA$, the start positions of the suffixes $T_i = T[i \ldots n-1]$ in increasing lexicographic order, and its inverse. Symbols are compared only in the first pass. Positions and ranks are 0-based. No sentinel is appended: a suffix that is a proper prefix of another sorts first. This is [suffix array construction](/suffix-array-construction/).

## The algorithm

The algorithm keeps three arrays of $n$ integers.

- $I$, the current order of the positions, which becomes $SA$.
- $V$, the group number of each position: the last rank of its group in $I$. Group numbers respect the order: if $V[x] < V[y]$, then $T_x < T_y$.
- $L$, the block lengths: at the first rank $s$ of an unsorted group of size $g$, $L[s] = g$; at the first rank of a run of $c$ consecutive sorted entries, $L[s] = -c$.

```pseudo id=main
LS-SORT(T)                               ▷ n = |T|; returns I = SA and V = SA⁻¹
L1  if n = 0 then return the empty arrays
L2  I ← positions sorted by T[i]; V[x] ← last rank of the group of x; L marks groups and sorted runs
L3  h ← 1
L4  loop
L5      for each block of ranks [s, e), from left to right, using L to jump do
L6          if L[s] < 0 then skip the sorted run, joining it with a sorted run just before it
L7          else sort I[s .. e − 1] by key(x) = V[x + h] (−1 if x + h = n) with ternary-split quicksort
L8              each block of equal keys becomes a group numbered by its last rank; a block of size 1 is sorted
L9      if the pass found no unsorted group then return I and V
L10     h ← 2h
```

**Why one key is enough.** All members of a group share a prefix of length $h$. So two members $x$ and $y$ compare as $T_{x+h}$ and $T_{y+h}$, and the group number $V[x + h]$ orders those: a smaller number means a smaller suffix, and equal numbers mean a common prefix of length $h$. Members with equal keys share $2h$ symbols. A member with $x + h = n$ is the shortest one, a prefix of all others, and its key $-1$ puts it first.

**Ternary split.** Each step of the quicksort picks a pivot key and splits the segment into keys less than, equal to and greater than the pivot. The equal part is a finished subgroup for this pass: it gets its number at once. The other two parts are sorted further. The implementation uses an explicit stack, not recursion. Larsson and Sadakane choose the pivot by a pseudo-median and switch to a simple sort for small segments, as in the sort of Bentley and McIlroy.

**Updates in place.** A group can be split while other groups of the same pass are still waiting, and the waiting groups then read some new, finer group numbers as keys. This is safe: the new numbers still respect the order of the suffixes, and equal numbers still mean a common prefix of length $h$. Finer keys only refine the groups more, which is why the algorithm often finishes in fewer passes than plain doubling. The implementation here reads the keys of one group before it splits that group; the original code achieves the same by the order in which it writes the new numbers.

**Skipping.** The entry $L[s] < 0$ lets a pass jump over a run of sorted entries in one step, and adjacent runs are joined, so a pass costs time in proportion to the unsorted part plus the number of runs.

## Example

The text is $T = \texttt{banana}$, $n = 6$.

| step | $I$ | groups (ranks) | $V$ by position $0..5$ |
|---|---|---|---|
| after L2 | 1 3 5 0 2 4 | {1 3 5} {0} {2 4} | 3, 2, 5, 2, 5, 2 |
| $h = 1$, split ranks 0..2 | 5 1 3 0 2 4 | {5} {1 3} {0} {2 4} | 3, 2, 5, 2, 5, 0 |
| $h = 1$, split ranks 4..5 | 5 1 3 0 4 2 | {5} {1 3} {0} {4} {2} | 3, 2, 5, 2, 4, 0 |
| $h = 2$, split ranks 1..2 | 5 3 1 0 4 2 | all of size 1 | 3, 2, 5, 1, 4, 0 |

In the first pass, the group of `a` at ranks 0 to 2 has the members 1, 3 and 5. Their keys are $V[2] = 5$, $V[4] = 5$ and $-1$ for position 5, since $5 + 1 = n$. So suffix 5 (`a`) comes first, and 1 and 3 stay tied with the number 2: both start with `an`. The group of `n` at ranks 4 and 5 has the members 2 and 4, with the keys $V[3] = 2$ and $V[5] = 0$; this reads the number 0 that the split just before gave to position 5, an update in place. In the second pass only the group {1, 3} is left. Its keys are $V[3] = 2$ and $V[5] = 0$, so 3 (`ana`) comes before 1 (`anana`). The pass with $h = 4$ finds no unsorted group. The result is $SA = [5, 3, 1, 0, 4, 2]$ and $V = [3, 2, 5, 1, 4, 0]$, the inverse.

For `mississippi`, the first pass splits the groups of `i`, `p` and `s`, the second pass splits only the two pairs {1, 4} and {2, 5} that are left, and the third pass finds nothing to do.

## Correctness

The invariant at the start of the pass with the value $h$ has three parts: positions in different groups are in the order of their suffixes; the members of one group share a prefix of length $h$; and $V$ holds the last rank of each group. A split reads the keys $V[x + h]$. Because the members share $h$ symbols, the keys compare as the suffixes do, and equal keys mean $2h$ shared symbols. So after the pass the invariant holds for $2h$. Two different suffixes cannot share $n$ symbols, so after at most $\lceil \log_2 n \rceil$ passes with splits, all groups have size 1, and then $I$ is the suffix array and $V$ its inverse. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| case | time |
|---|---|
| worst case | $O(n \log n)$ |
| text with all symbols different | $\Theta(n)$ after the first sort: no unsorted group is left |
| random text over $\sigma \ge 2$ symbols | few passes, since most groups are split after $O(\log_\sigma n)$ symbols |
| periodic text such as $\texttt{a}^n$ | $\Theta(\log n)$ passes |
| extra space | $\Theta(n)$ words: $I$, $V$ and $L$ |

**Passes.** After the pass with the value $2^k$, all groups share $2^{k+1}$ symbols, so there are at most $\lceil \log_2 n \rceil + 1$ passes.

**Cost of the splits.** Larsson and Sadakane bound the total cost of all splits by $O(n \log n)$. The idea is that splitting a group of size $g$ into subgroups of sizes $g_1, \ldots, g_k$ costs $O(g + \sum_i g_i \log(g / g_i))$ comparisons with a good pivot, and the sum of the second terms over the whole run telescopes, since each element's group size only shrinks from at most $n$ to 1. Each pass adds $O(n)$ for the first terms and the walk. The implementation here takes the middle element as the pivot, which is fast on typical data but has no worst-case guarantee.

**Space.** Larsson and Sadakane store $L$ in the same array as $I$, with negative values in the slots of sorted entries, so the method needs only $2n$ integers in addition to the text.

## Properties

- **Adaptive.** Texts with short repeats finish in few passes. The longer the longest repeat, the more passes: the number of passes is about $\log_2$ of the length of the longest repeated substring.
- **Not stable.** Stability has no meaning for suffixes, since all suffixes are different.
- **Not comparison based after the first pass.** Later passes compare integer group numbers.
- **Output.** It returns the inverse suffix array $V$ as well, which is what [Kasai's algorithm](/kasai-algorithm/) and the [Burrows-Wheeler transform](/burrows-wheeler-transform/) need.

## Variants and improvements

- **Manber-Myers.** The [Manber-Myers algorithm](/manber-myers-algorithm/) sorts all suffixes in each pass with bucket moves. Larsson-Sadakane does less work because it touches only unsorted groups.
- **KMR.** The [Karp-Miller-Rosenberg algorithm](/karp-miller-rosenberg-algorithm/) names factors of length $2^j$ with radix sorts; the doubling idea is the same.
- **Initial sort by more symbols.** Larsson and Sadakane pack several symbols into one integer for the first sort when the alphabet is small, which saves the first passes.
- **Linear-time methods.** [SA-IS](/sa-is/) and [DC3](/dc3-skew-algorithm/) run in $O(n)$ time, and on most inputs SA-IS is faster than qsufsort; [multikey quicksort](/multikey-quicksort/) of the suffixes is fast on text with short repeats but slow on repetitive text.

## When to use it

Use it when you need a simple suffix sort with small memory and good speed on ordinary data, and an $O(n \log n)$ worst case is acceptable. It is short to write, needs no recursion on a reduced string, and gives the inverse array for free. For very repetitive data, such as DNA collections of many similar genomes, or when the best speed matters, use a linear algorithm such as [SA-IS](/sa-is/).

## Pitfalls

- **Wrong key for the last member.** For $x + h = n$ the key must be smaller than all group numbers, since $T_x$ is then a prefix of the other members. Using $V[x + h]$ out of range or a large default gives the wrong order without a sentinel.
- **Group number as the first rank.** Any order-preserving numbering works if it is used everywhere, but mixing the first-rank and last-rank conventions breaks the order of the keys. The original uses the last rank.
- **Keys that change during a split.** If a group contains both $x$ and $x + h$, writing the new numbers of some members while the same group is still being sorted can change the keys under the sort. Read the keys first, or follow the original order of updates.
- **Deep recursion.** A recursive quicksort on a group of size $g$ can recurse $g$ times with a bad pivot. Use an explicit stack and recurse on the smaller part.

## Implementations

The Python function returns $SA$ and its inverse. The ternary split uses an explicit stack, and the passes are a loop.

## History

Larsson and Sadakane described the algorithm in a 1999 technical report at Lund University, and the journal version, "Faster suffix sorting", appeared in Theoretical Computer Science in 2007. Their program qsufsort was used to compute the Burrows-Wheeler transform in compressors and indexes until linear algorithms such as SA-IS replaced it in practice.

## References
