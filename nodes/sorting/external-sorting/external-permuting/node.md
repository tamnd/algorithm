---
tag: 0NBC1N
kind: problem
slug: external-permuting
name: External permuting
aliases:
- permuting in external memory
- external permutation
area: sorting/external-sorting
level: advanced
summary: Rearrange N records into a given permutation on disk; its I/O cost is min of N and the sorting bound.
model: external-memory-model
prereqs: [permuting-problem, external-merge-sort]
see_also: [permuting-lower-bound, external-sorting-io-lower-bound, external-sorting-lower-bound, disk-striping, sorted-run, suffix-array]
sources:
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.6, Permuting (Theorem 5.3, the bound for D disks, and the case B log m = o(log n))
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1988, pages 1116 to 1127
    locator: Theorem 3.2 (permuting)
  - paper: doi:10.1007/BF01185207
    title: Jeffrey Scott Vitter and Elizabeth A. M. Shriver, Algorithms for parallel memory I, Two-level memories, Algorithmica 12(2-3), 1994, pages 110 to 147
    locator: the randomized placement that moves items one by one in O(N/D) I/Os on D disks
---

External permuting is the step of an external sort that moves the records to the places that the sort has chosen. The general problem, its lower bound and its basic algorithms are on the page [permuting problem](/permuting-problem/). This page looks at permuting from the side of sorting: when a sort of short keys followed by a permutation of the long records is cheaper than a sort of the records, and what changes with $D$ disks. The answer depends on the number $B$ of records in a block: moving records one by one wins only when $B$ is less than about twice the number of merge passes.

## In plain words

A file holds large records, each with a short key. One way to sort the file is to sort the records themselves. Another way is to copy out only the keys, each with the number of its record, sort these short pairs, and then fetch the records in the sorted order. The second way sorts much less data. But the last step, the fetch, takes one disk access for each record, because the records that are next to each other in the output are in different places on the disk.

So the second way wins only if few records fit in a block. If a block holds many records, a sort of the full records moves a whole block with each access and is much faster than a fetch of one record at a time.

## Definition

**Model.** The [external memory model](/external-memory-model/) with a memory of $M$ records and blocks of $B$ records, or the parallel disk model with $D$ disks and striped input and output, as on the page [I/O lower bound for sorting](/external-sorting-io-lower-bound/). Write $n = N/B$ and $m = M/B$. Records are indivisible.

**Input.** $N$ records in $n$ blocks, and a permutation in one of two forms:

- *target form*: each record carries the index $\pi(i)$ of its output cell;
- *source form*: for each output cell $p$, a list gives the index $\sigma(p)$ of the record that goes there, with $\sigma = \pi^{-1}$.

**Output.** The records in $n$ blocks, with record $\sigma(p)$ in cell $p$ for each $p$.

**Cost.** The number of I/Os, or of parallel I/Os with $D$ disks, in the worst case over the permutation. A sort of $N$ pairs of integers converts one form into the other, so the forms differ by at most the cost of a sort of short pairs.

## Variants

- **Gather.** The source form, filled one output block at a time. A sort of (key, record number) pairs produces exactly this form, so it is the usual form after a key sort.
- **Scatter.** The target form, written one input record at a time. Each record needs a read and a write of its output block, unless that block is still in memory.
- **Records larger than a block.** If a record fills $w \ge 1$ blocks, each record must be read and written at least once, and moving records one by one costs $2wN$ I/Os, which is optimal. A sort of the records cannot be cheaper, because it also reads and writes each record at least once.
- **Parallel disks.** With $D$ disks, a one-by-one method can be slow when many records that it needs at the same time are on the same disk. Vitter and Shriver place the blocks at random so that, with high probability, the requests are spread over the disks, and the one-by-one method takes $O(N/D)$ parallel I/Os.

## Examples

**A gather after a key sort.** Six records with $B = 2$ are in the blocks $[0{:}K\ 1{:}C]\ [2{:}T\ 3{:}A]\ [4{:}P\ 5{:}F]$, written as record number and key. A sort of the pairs (key, number) gives $(A, 3), (C, 1), (F, 5), (K, 0), (P, 4), (T, 2)$, so $\sigma = (3, 1, 5, 0, 4, 2)$. Output block 0 needs records 3 and 1, so it reads input blocks 1 and 0; output block 1 needs records 5 and 0, from input blocks 2 and 0; output block 2 needs records 4 and 2, from input blocks 2 and 1. The gather makes 6 reads and 3 writes, $N + n = 9$ I/Os.

**Large and small records.** Take $N = 10^8$ records, blocks of $10^4$ bytes and a memory of $10^9$ bytes, so $m = 10^5$ blocks. A [k-way merge](/k-way-merge/) of up to $m - 1$ runs is one pass. The tags are pairs of 16 bytes.

| record size | B | sort the records | key sort, then gather |
|---|---|---|---|
| $10^4$ bytes | 1 | $4 \cdot 10^8$ | about $3.01 \cdot 10^8$ |
| 100 bytes | 100 | $4 \cdot 10^6$ | about $1.03 \cdot 10^8$ |

With records of $10^4$ bytes, $n = 10^8$, run formation makes 1000 [sorted runs](/sorted-run/), and one merge pass completes the sort: $2n + 2n$ I/Os. The key sort reads the records once ($10^8$), writes $1.6 \cdot 10^5$ blocks of tags, sorts them in 2 runs and one merge ($6.4 \cdot 10^5$), reads them back ($1.6 \cdot 10^5$), and gathers ($N + n = 2 \cdot 10^8$). With records of 100 bytes, $n = 10^6$ and the sort of the records costs $4n$, while the gather alone costs $N + n = 1.01 \cdot 10^8$, 25 times more.

## Known algorithms

| method | I/Os on one disk | form |
|---|---|---|
| gather, one output block at a time | at most $N + n$ | source |
| scatter, one input record at a time | at most $2N + n$ | target |
| [external merge sort](/external-merge-sort/) on the targets, with $p$ merge passes | $2n(p + 1)$ | target |
| the better of the gather and the sort | $O(\min\{N, n \log_m n\})$ | either |

The sort is [external merge sort](/external-merge-sort/) with fan-in $m - 1$, so $p = \lceil \log_{m-1} \lceil n/m \rceil \rceil$. On $D$ disks, an optimal sort for $D$ disks, such as [balance sort](/balance-sort/), gives the sort term divided by $D$, and the randomized placement of Vitter and Shriver gives the one-by-one term $O(N/D)$.

## Bounds

- **One disk.** $\Theta(\min\{N, n \log_m n\})$ I/Os, by Aggarwal and Vitter. The proof is on the page [permuting lower bound](/permuting-lower-bound/).
- **D disks.** $\Theta\big(\min\big\{\frac ND, \frac nD \log_m n\big\}\big)$ parallel I/Os, Vitter's Theorem 5.3. The lower bound follows from the one-disk bound by the simulation in part (a) of the proof on the page [I/O lower bound for sorting](/external-sorting-io-lower-bound/): a parallel I/O becomes at most $D$ single I/Os, and the simulation moves whole records, so it is also a permuting algorithm.
- **The crossover for merge sort.** The gather costs $n(B + 1)$ and the merge sort costs $2n(p + 1)$, so the gather is cheaper exactly when $B < 2p + 1$. With one merge pass, this means $B \le 2$. Asymptotically, the one-by-one term is the smaller one only when $B \log m = o(\log n)$, which Vitter calls the extreme case.

## Reductions

- **Sorting large records reduces to a key sort and a gather.** Sort the (key, record number) pairs, which gives the source form, then gather. The cost is a sort of $N$ short pairs plus at most $N + n$ I/Os.
- **Permuting reduces to sorting.** Sort the records by their targets. So the permuting cost is at most the sorting cost, and a key sort followed by a gather is never asymptotically better than a direct sort, except in the extreme case of small $B$.
- **Sorting indivisible records is at least as hard as permuting.** A sort must realize the permutation that takes each record to its rank, so the permuting lower bound holds for every sort that moves whole records.

## Applications

- **Database sorts of wide rows.** A sort that carries only the key and a row identifier, and fetches the rows at the end, saves I/O only when the rows are about the size of a page or larger. For short rows, database systems sort the rows themselves.
- **Rank updates in suffix sorting.** External [prefix doubling](/prefix-doubling/) for a [suffix array](/suffix-array/) must send the new rank of each suffix to the position of another suffix in each round. Each such step is a permutation, done by a sort.
- **Changing the layout of a file.** A change from one layout to another, such as from a layout for one disk to a layout for [striped disks](/disk-striping/), is a fixed permutation of the blocks or records.

## References
