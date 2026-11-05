---
tag: GHWWJ6
kind: algorithm
slug: parallel-radix-sort
name: Parallel radix sort
aliases:
- parallel LSD radix sort
area: sorting/parallel-sorting
level: core
summary: Radix sort whose per-digit counting and scatter steps use parallel prefix sums.
solves: [parallel-sorting-problem]
model: erew-pram
complexity:
  vars: {n: the number of keys, w: the number of bits in a key, b: the number of bits in a digit, p: the number of processors}
  time: {worst: Θ(⌈w/b⌉ (n + 2^b p))}
  space: {extra: Θ(n + 2^b p)}
  depth: {worst: O(⌈w/b⌉ (n/p + 2^b + log p))}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
prereqs: [radix-sort, counting-sort, all-prefix-sums, erew-pram]
see_also: [radix-sort, counting-sort, msd-radix-sort, integer-sorting, sample-sort, parallel-pack, blelloch-scan, scatter-and-gather]
sources:
  - book: isbn:9780262023139
    title: Guy E. Blelloch, Vector Models for Data-Parallel Computing, MIT Press, 1990
    locator: the split operation and the split radix sort built from scans
  - paper: "Guy E. Blelloch, Charles E. Leiserson, Bruce M. Maggs, C. Greg Plaxton, Stephen J. Smith and Marco Zagha, A comparison of sorting algorithms for the Connection Machine CM-2, Proceedings of the 3rd ACM Symposium on Parallel Algorithms and Architectures (SPAA), 1991"
    locator: the radix sort with per-processor digit counts and one scan per pass, compared with bitonic sort and sample sort
  - paper: "Marco Zagha and Guy E. Blelloch, Radix sort for vector multiprocessors, Proceedings of Supercomputing 1991"
    locator: the parallel radix sort with one histogram for each processor and a scan in digit-major order
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition, Addison-Wesley, 2003
    locator: Chapter 9, Sorting, the section on other sorting algorithms (parallel radix sort with prefix sums)
---

Parallel radix sort is [LSD radix sort](/radix-sort/) in which each pass, a stable [counting sort](/counting-sort/) on one digit, runs on $p$ processors. Each processor counts the digits of its own block of keys, one [prefix sum](/all-prefix-sums/) over all the counts gives every processor the output slots for each digit, and then each processor writes its keys to their slots. On the [EREW PRAM](/erew-pram/) with $p$ processors, a pass on $n$ keys with $b$-bit digits takes time $O(n/p + 2^b + \log p)$. It is the fastest way to sort short integer keys on GPUs and other wide machines.

## In plain words

Sort a pile of mail by postcode, one digit at a time, starting with the last digit. A single person deals the letters into ten trays by the current digit, keeping the order within each tray, and then stacks the trays.

With many people, each takes a part of the pile and counts how many of their letters go to each tray. These counts are written in a table, tray by tray and person by person. A running total of the table tells each person exactly where in the final row their letters for each tray start. Then all of them place their letters at once, and nobody gets in anybody's way. Because the order within each tray is kept, the earlier digits stay in order when the next digit is used.

## The problem

The input is an array $A[0 \ldots n-1]$ of non-negative integers of $w$ bits each. The output is the same keys in non-decreasing order. This is the [integer sorting](/integer-sorting/) case of the [parallel sorting problem](/parallel-sorting-problem/). The model is the [EREW PRAM](/erew-pram/) with $p \le n$ processors, and the keys are cut into $\lceil w/b \rceil$ digits of $b$ bits, so each digit is in $[0, R)$ with $R = 2^b$. Processor $j$ owns the block $A[\lfloor jn/p \rfloor \ldots \lfloor (j+1)n/p \rfloor - 1]$.

## The algorithm

Here $\operatorname{digit}_t(x) = \lfloor x / R^t \rfloor \bmod R$ is digit $t$ of $x$, with digit $0$ the least significant.

```pseudo id=main
PAR-RADIX-SORT(A[0 .. n − 1], w, b, p)
L1  for t ← 0 to ⌈w/b⌉ − 1 do
L2      parallel for j ← 0 to p − 1 do           ▷ processor j, on block j
L3          for each d ∈ [0, R): C[d][j] ← number of keys x in block j with digit_t(x) = d
L4      O ← exclusive prefix sums of C in the order C[0][0], …, C[0][p − 1], C[1][0], …, C[R − 1][p − 1]
L5      parallel for j ← 0 to p − 1 do
L6          for each key x of block j, from left to right do
L7              d ← digit_t(x);  B[O[d][j]] ← x;  O[d][j] ← O[d][j] + 1
L8      A ← B
```

The order of the prefix sum on line L4 is the key point. It lists all counts for digit $0$ first, block by block, then all counts for digit $1$, and so on. So $O[d][j]$ is the number of keys with a smaller digit, plus the number of keys with digit $d$ in the blocks before $j$.

## Example

Sort $A = [170, 45, 75, 90, 802, 24, 2, 66]$ in base $R = 10$ with $p = 2$ processors, so block 0 is $[170, 45, 75, 90]$ and block 1 is $[802, 24, 2, 66]$. In pass $t = 0$, the last digits are $0, 5, 5, 0$ in block 0 and $2, 4, 2, 6$ in block 1. The nonzero counts and their offsets, in the order of line L4, are:

| digit $d$, block $j$ | 0, 0 | 2, 1 | 4, 1 | 5, 0 | 6, 1 |
| --- | --- | --- | --- | --- | --- |
| count $C[d][j]$ | 2 | 2 | 1 | 2 | 1 |
| offset $O[d][j]$ | 0 | 2 | 4 | 5 | 7 |

Processor 0 writes $170 \to 0$, $45 \to 5$, $75 \to 6$, $90 \to 1$, and processor 1 writes $802 \to 2$, $24 \to 4$, $2 \to 3$, $66 \to 7$, at the same time. The array becomes $[170, 90, 802, 2, 24, 45, 75, 66]$.

| after pass | array |
| --- | --- |
| $t = 0$, last digit | $[170, 90, 802, 2, 24, 45, 75, 66]$ |
| $t = 1$, tens digit | $[802, 2, 24, 45, 66, 170, 75, 90]$ |
| $t = 2$, hundreds digit | $[2, 24, 45, 66, 75, 90, 170, 802]$ |

## Correctness

One pass puts each key at the position it has in the stable sort by digit $t$: the keys before it are the keys with a smaller digit, the keys with the same digit in earlier blocks, and the keys with the same digit earlier in its own block. So a pass is a stable counting sort, and the passes together sort by the same induction as sequential [radix sort](/radix-sort/). No two processors read or write the same cell, so the exclusive-access rules of the EREW PRAM hold. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are for the [EREW PRAM](/erew-pram/) with $p$ processors, $n \ge p$ keys of $w$ bits and digits of $b$ bits, $R = 2^b$.

**One pass.** Line L3 takes time $O(n/p + R)$: each processor clears its $R$ counters and reads its $\lceil n/p \rceil$ keys. Line L4 is a prefix sum of $Rp$ numbers on $p$ processors, which takes time $O(R + \log p)$: each processor first sums its own $R$ counts, a [parallel prefix](/parallel-prefix/) over the $p$ sums takes time $O(\log p)$, and each processor then fills in its own counts. Lines L5 to L7 take time $O(n/p)$. So a pass takes time $O(n/p + R + \log p)$ and work $O(n + Rp)$.

**The whole sort.** There are $\lceil w/b \rceil$ passes, so the time is $O(\lceil w/b \rceil (n/p + 2^b + \log p))$ and the work is $O(\lceil w/b \rceil (n + 2^b p))$.

**Choice of $b$.** With $b = \lfloor \lg(n/p) \rfloor$, we have $2^b \le n/p$, and the time is $O((w / \log(n/p)) (n/p + \log p))$. For $p \le n / \log n$, this is $O(w n / (p \log(n/p)))$, which is linear speedup over sequential radix sort with the same digits.

**Work-span form.** With $p = n$ keys in their own blocks and $b = 1$, each pass is a split by one bit: one prefix sum over the flags, with work $O(n)$ and span $O(\log n)$. In the [work-span model](/work-span-model/), this split radix sort has work $O(wn)$ and span $O(w \log n)$.

**Space.** The output array $B$ has $n$ cells and the table $C$ has $2^b p$ cells.

## Properties

- **Stable.** Each pass is stable, and the final order of equal keys is their input order.
- **Not comparison-based.** It reads the digits of keys, so the $\Omega(n \log n)$ [comparison lower bound](/comparison-sort-lower-bound/) does not apply.
- **Deterministic and oblivious in control.** The steps depend on the keys only through the counts, so all processors do the same amount of work in each pass.
- **Exclusive access.** Each processor reads and writes its own counts, and the slots it writes are disjoint from those of all other processors.
- **Not in place.** Each pass writes to a second array.

## Variants and improvements

- **Split radix sort.** With one bit per pass, the counting step becomes one [parallel pack](/parallel-pack/) of the keys with bit 0 followed by those with bit 1. This is Blelloch's split radix sort, built from the scan primitive.
- **MSD radix sort.** [MSD radix sort](/msd-radix-sort/) sorts by the first digit and then sorts each bucket in parallel. It reads only the digits it needs, which helps for long keys such as strings, but the buckets can be very unequal.
- **Local sorting first.** On GPUs, each thread block first sorts its tile by the current digit in fast local memory. The scatter then writes runs of consecutive keys, which makes the memory accesses much faster.
- **One sweep.** Recent GPU sorts compute the histograms of all digits in one read of the keys, and chain the prefix sums of consecutive tiles with a decoupled look-back, so each pass reads and writes the keys only once.
- **Distributed memory.** On a [BSP](/bsp-model/) machine, each pass is a total exchange of keys, an [h-relation](/h-relation/) with $h$ about $n/p$. With few passes of large digits, this is a common way to sort integers on clusters.

## When to use it

Use parallel radix sort for many keys that are integers, or that map to integers in an order-preserving way, such as floating-point numbers after a bit flip. It is the standard sort on GPUs. It is a poor choice when the keys are long and only a short prefix decides the order, and when the comparison function is not a plain key order. For general keys, use [sample sort](/sample-sort/) or [parallel merge sort](/parallel-merge-sort/).

## Pitfalls

- **Wrong scan order.** If the prefix sum runs block by block and then digit by digit, the keys of one block are grouped together and the pass does not sort.
- **Too many buckets.** The table has $2^b p$ entries. With large $b$ and many processors, clearing and scanning the table costs more than moving the keys.
- **Unstable scatter.** If a processor writes its keys in any order other than left to right, equal digits change order, and the later passes destroy the work of the earlier ones.
- **Signed and floating keys.** Two's complement integers and floating-point numbers do not sort correctly as unsigned bit strings. Flip the sign bit, and for negative floats all bits, before sorting.

## Implementations

## History

Radix sort on punched-card machines dates from the early 20th century. Its data-parallel form, with one scan per bit, appears in Blelloch's work on scan primitives. Zagha and Blelloch gave the form with one histogram for each processor and a scan in digit-major order for vector multiprocessors in 1991, and the same year Blelloch and others compared it with bitonic sort and sample sort on the Connection Machine CM-2. GPU radix sorts since the late 2000s use the same counting scheme within thread blocks.

## References
