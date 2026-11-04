---
tag: P385WS
kind: algorithm
slug: oscillating-sort
name: Oscillating sort
aliases:
- oscillating merge sort
area: sorting/external-sorting
level: advanced
summary: A tape merge scheme that alternates the direction of reading runs so that tape rewinds are avoided.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {N: the number of items, S: the number of initial runs, T: the number of tapes}
  time: {worst: O(N log N), average: O(N log N), best: O(N log N)}
  space: {extra: Θ(N)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [balanced-merge-sort, k-way-merge, sorted-run]
see_also: [polyphase-merge-sort, cascade-merge-sort, external-merge-sort, merge-sort, stack]
sources:
  - paper: doi:10.1145/321127.321133
    title: Sheldon Sobel, Oscillating sort, a new sort merging technique, Journal of the ACM 9(3), 1962, pages 372 to 374
    locator: the whole paper, the first description of the method
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.5, The Oscillating Sort (the algorithm for tapes that read backward, and its comparison with the other tape merges)
  - book: isbn:9780201416077
    title: Gaston H. Gonnet and Ricardo Baeza-Yates, Handbook of Algorithms and Data Structures, second edition
    locator: Section 4.4, External sorting (tape merges that read backward)
---

Oscillating sort is a tape sort for tapes that can be read backward. It does not distribute all runs first and merge them later. It alternates: it reads a few initial [sorted runs](/sorted-run/) from the input, merges them, reads more, and merges again, so that the work goes back and forth between distribution and merging. Each work tape is used as a [stack](/stack/) of runs, so no tape is ever rewound. With $T$ tapes it merges $T - 2$ runs at a time and needs $\lceil \log_{T-2} S \rceil$ merge levels for $S$ runs.

## In plain words

Some tape drives can read a tape backward, from the place where they stopped writing. If you write a sorted piece and then read it backward, you get the items in reverse order. A tape then works like a pile of plates: you put a piece on top, and later you take the top piece off.

The oscillating sort uses this. To make one long sorted piece, it first makes a few shorter pieces, each on a different tape, sorted in the opposite direction. Then it reads them backward, which puts them in the right direction, and merges them onto the target tape. Each shorter piece is made in the same way, from even shorter pieces. The sort never stops to rewind a tape.

## The problem

The input is a file $F$ of $N$ items with a total order, on its own tape, and a memory of $M$ items. There are $T - 1 \ge 3$ work tapes, which are written forward and can be read backward. The output is a work tape with the items of $F$ in non-decreasing order. This is the [sorting problem](/sorting-problem/) on sequential devices.

## The algorithm

Let $P = T - 2$, the number of work tapes other than the target of a merge. The direction of a run is ascending or descending.

```pseudo id=main
OSCILLATING-SORT(F, M, T)               ▷ the input tape and work tapes W₁ … W_{T−1}
L1  S ← ⌈N/M⌉; P ← T − 2
L2  BUILD(S, W₁, ascending); return the run on W₁

BUILD(n, x, dir)                        ▷ append to tape x one run of the next n parts of F
L3  if n = 1 then
L4      read the next M items of F, sort them in the direction dir, and write them at the end of x
L5  else split n into P parts n₁ ≥ ⋯ ≥ n_P that differ by at most 1; y₁ … y_P are the work tapes other than x
L6      for each i with n_i > 0 do BUILD(n_i, y_i, opposite of dir)
L7      read the last run of each such y_i backward    ▷ it comes out in the direction dir
L8      merge these runs in the direction dir, and write the result at the end of x
```

BUILD keeps a stack discipline: it adds one run to the end of $x$ and leaves all other work tapes as they were. Line L6 builds the pieces on the tapes other than $x$, and their own calls use $x$ too, but they take back all that they write. Line L7 takes the pieces off again. A merge in the direction "descending" takes the largest key first; it is a [k-way merge](/k-way-merge/) with the order reversed.

## Example

Sort $F = (5, 2, 7, 1, 8, 3, 6, 4)$ with $M = 2$ and $T = 4$, so $P = 2$ and there are 3 work tapes. The runs are $R_1 = (2, 5)$, $R_2 = (1, 7)$, $R_3 = (3, 8)$ and $R_4 = (4, 6)$. The call BUILD(4, $W_1$, ascending) splits 4 into $2 + 2$ and builds two descending runs, on $W_2$ and on $W_3$.

| step | action | $W_1$ | $W_2$ | $W_3$ |
|---|---|---|---|---|
| 1 | write $R_1$ ascending on $W_1$ | (2 5) | | |
| 2 | write $R_2$ ascending on $W_3$ | (2 5) | | (1 7) |
| 3 | read $W_1$ and $W_3$ backward, merge descending onto $W_2$ | | (7 5 2 1) | |
| 4 | write $R_3$ ascending on $W_1$ | (3 8) | (7 5 2 1) | |
| 5 | write $R_4$ ascending on $W_2$ | (3 8) | (7 5 2 1), (4 6) | |
| 6 | read $W_1$ and the last run of $W_2$ backward, merge descending onto $W_3$ | | (7 5 2 1) | (8 6 4 3) |
| 7 | read $W_2$ and $W_3$ backward, merge ascending onto $W_1$ | (1 2 3 4 5 6 7 8) | | |

Step 5 writes $R_4$ on top of the run on $W_2$, and step 6 takes it off again, so $W_2$ holds its old run for step 7. The input is read once, there are $\lceil \log_2 4 \rceil = 2$ merge levels, the merges move 16 items, and no tape is rewound.

## Correctness

By induction on $n$, BUILD($n$, $x$, dir) reads the next $n$ parts of $F$, adds to the end of $x$ one run of their items sorted in the direction dir, and leaves every other work tape as it was. For $n \ge 2$, the sub-calls of line L6 leave each $y_i$ with its old runs plus one run in the opposite direction, line L7 removes these runs and reads them in the direction dir, and line L8 merges them. The top call then leaves one ascending run of all items on $W_1$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Merge levels.** The recursion splits $n$ into parts of at most $\lceil n/P \rceil$, so there are $\lceil \log_P S \rceil$ levels. Each item takes part in one merge per level.
- **Data moved.** The input is read once, and each item is written once at line L4 and once per level, so the sort writes $N(1 + \lceil \log_{T-2} S \rceil)$ items. For $S = 1000$ runs this is 1 + 7 passes with 5 tapes, 1 + 5 with 6 tapes and 1 + 4 with 10 tapes. The [balanced merge sort](/balanced-merge-sort/) merges only $\lfloor T/2 \rfloor$ runs at a time and needs 10, 7 and 5 merge passes on 5, 6 and 10 tapes.
- **No rewinds.** All reads of work tapes are backward reads of the last run, which starts where the head stands. On real tape drives this saves the rewind time of the other tape sorts.
- **Time in memory.** $O(N \log M)$ for line L4 and $O(\log P)$ per item merged, so $O(N \log N)$ in total.
- **Memory.** One buffer for each of the $P$ inputs of a merge, plus the memory of line L4.

## Properties

- **Not stable.** A run read backward reverses the order of its equal keys, so equal keys can leave in a different order.
- **Not in place.** The data moves from tape to tape.
- **Recursive.** BUILD is a recursion of depth $\lceil \log_P S \rceil$. Its stack holds only the counts and the tape names, not the data.

## Variants and improvements

- **Knuth's form.** Knuth's Section 5.4.5 gives the method as an iterative algorithm with a fixed pattern of phases for each number of tapes, which avoids the recursion.
- **Unknown S.** If $S$ is not known in advance, the sort can build complete groups of $P^k$ runs for $k = 1, 2, \ldots$ and merge the groups at the end.
- **Forward reading.** On tapes that read only forward, the stack discipline fails, because a run must be read from its start. The [balanced merge sort](/balanced-merge-sort/), the [polyphase merge sort](/polyphase-merge-sort/) and the [cascade merge sort](/cascade-merge-sort/) are for such tapes.
- **On disks.** The recursion is a top-down [merge sort](/merge-sort/) with fan-in $P$, in which each piece is merged as soon as it is complete. An [external merge sort](/external-merge-sort/) on disk uses the full fan-in $M/B - 1$ instead.

## When to use it

Use an oscillating sort on tape drives that can read backward, when rewind time is a large part of the cost, or when the input arrives as a stream and the sort must start before the input ends. With such drives it needs about as many merge levels as a balanced merge with $T - 2$ inputs, and no rewinds. On disks, use an [external merge sort](/external-merge-sort/).

## Pitfalls

- **Writing the pieces in the wrong direction.** Line L6 must build the pieces in the opposite direction. If they are in the direction dir, line L7 reads them reversed and the merge fails.
- **Building on the target tape.** The tapes $y_i$ of line L5 must differ from $x$. A piece built on $x$ would lie on top of the run that the caller expects at the end of $x$.
- **Reading the wrong run.** Line L7 must take the last run of each $y_i$. The runs below it belong to the callers.
- **Forgetting the input tape.** The input needs its own tape or device. With $T$ tapes in total there are only $T - 1$ work tapes, and the merge order is $T - 2$, not $T - 1$.

## Implementations

## History

Sobel described the oscillating sort in 1962, for tape drives that could read backward. Knuth's Section 5.4.5 gives the method in detail, with its history, and compares it with the balanced, polyphase and cascade merges. This page gives a recursive form of the idea, which makes the stack discipline easy to see.

## References
