---
tag: 0QXN82
kind: technique
slug: disk-striping
name: Disk striping
aliases:
- striping
- RAID striping
area: sorting/external-sorting
level: core
summary: Spread consecutive blocks across several disks so that they can be read or written in parallel.
prereqs: [external-memory-model]
see_also: [external-merge-sort, external-sorting-io-lower-bound, balance-sort, external-samplesort, double-buffering, hard-disk-model, b-tree]
sources:
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 4.2, Disk Striping and Parallelism with Multiple Disks (equations 4.1 to 4.4)
  - paper: "Kenneth Salem and Hector Garcia-Molina, Disk striping, Proceedings of the 2nd IEEE International Conference on Data Engineering (ICDE 1986)"
    locator: the whole paper, the striped layout and its performance
  - paper: doi:10.1145/50202.50214
    title: David A. Patterson, Garth Gibson and Randy H. Katz, A case for redundant arrays of inexpensive disks (RAID), Proceedings of the 1988 ACM SIGMOD International Conference on Management of Data
    locator: the RAID levels, with striping of data across the disks of an array
  - paper: doi:10.1007/BF01185207
    title: Jeffrey Scott Vitter and Elizabeth A. M. Shriver, Algorithms for parallel memory I, Two-level memories, Algorithmica 12(2-3), 1994, pages 110 to 147
    locator: the parallel disk model and the optimal sorting bound for D disks
---

Disk striping places logical block $j$ of a file on disk $j \bmod D$ of an array of $D$ disks, so that $D$ consecutive blocks, one *stripe*, can be transferred in one parallel I/O. It makes $D$ disks behave as one disk with blocks of $DB$ items. Each algorithm for one disk then runs on $D$ disks with no change, and scans become $D$ times faster. For sorting it is not optimal when $D$ is large, because the larger block lowers the fan-in of each merge from about $M/B$ to about $M/(DB)$.

## In plain words

A shop has several shelves, with one helper at each shelf. If all books of a series stand on one shelf, one helper must fetch them one after the other. If book 1 is on shelf 1, book 2 on shelf 2, and so on, all helpers can fetch a book at the same time.

Disk striping puts consecutive blocks of a file on different disks, in turn. A program then asks for a row of blocks, one from each disk, and all disks work at the same time. To the program, the disks look like one disk that reads very large blocks.

This is simple, and good for a read from start to end. But large blocks have a cost. A merge holds one block of each input in memory, so with larger blocks it merges fewer inputs at a time, and a sort can need more passes.

## When it applies

- There are $D$ disks that can transfer one block each in the same step, as in the parallel disk model of Vitter and Shriver.
- The algorithm accesses data in large sequential pieces, such as a scan, a copy, a merge, or a [B-tree](/b-tree/) search with large nodes.
- Memory holds at least a few stripes: $M \ge 3DB$ for a merge, so that the fan-in $M/(DB) - 1$ is at least 2.
- Simplicity is more important than the last factor of the I/O count, or $D$ is small compared with $M/B$.

## The template

The hole is an algorithm $\mathcal{A}$ for one disk with blocks of $B' = DB$ items. A logical block is a stripe.

```pseudo id=main
STRIPED(𝒜, D)                           ▷ 𝒜 is an algorithm for one disk with blocks of DB items
L1  run 𝒜, and at each I/O of 𝒜 on its logical block j do
L2      for d ← 0 to D − 1, all in the same parallel I/O do
L3          transfer the items jDB + dB to jDB + dB + B − 1 of the file
L4              to or from block j of disk d
```

Item $i$ of the file is in logical block $j = \lfloor i/(DB) \rfloor$, on disk $d = \lfloor i/B \rfloor \bmod D$, in block $j$ of that disk. This is the same as: physical block $\lfloor i/B \rfloor$ of the file goes to disk $\lfloor i/B \rfloor \bmod D$.

**Why it is correct.** The map from item $i$ to the triple (disk $d$, block $j$, offset $i \bmod B$) is a bijection between the positions of the file and the positions on the disks: $i = jDB + dB + (i \bmod B)$ with $0 \le d < D$ and $0 \le i \bmod B < B$. So each I/O of $\mathcal{A}$ on its logical block $j$ moves exactly the $DB$ items that $\mathcal{A}$ expects, and the striped run computes the same result as $\mathcal{A}$.

**Cost.** Each I/O of $\mathcal{A}$ becomes one parallel I/O. So if $\mathcal{A}$ does $t(N, M, DB)$ I/Os with blocks of $DB$ items, the striped run does $t(N, M, DB)$ parallel I/Os on $D$ disks with blocks of $B$ items. With $n = N/B$ and $m = M/B$:

| task | striped cost | optimal cost on D disks |
|---|---|---|
| scan of N items | $\lceil n/D \rceil$ | $\Theta(n/D)$ |
| search in a B-tree | $\Theta(\log_{DB} N)$ | $\Theta(\log_{DB} N)$ |
| sort of N items | $\Theta\big(\frac nD \log_{m/D} \frac nD\big)$ | $\Theta\big(\frac nD \log_m n\big)$ |

Striping is optimal for the first two rows. For sorting, the ratio of the two bounds is about $\log m / \log(m/D)$. When $D \le \sqrt m$, this ratio is at most 2. When $D$ is close to $m$, it grows like $\log m$. The proof that no striped sort can do better, and that striped merge sort is optimal for $D \le \sqrt m$, is on the page [external sorting I/O lower bound](/external-sorting-io-lower-bound/).

## Classic examples

**Striped merge sort.** An [external merge sort](/external-merge-sort/) with stripes as blocks has the fan-in $k = m/D - 1$. Take $n = 10^6$ blocks, $m = 1000$ and $r = 1000$ runs after run formation. Each pass costs $2n/D$ parallel I/Os.

| disks D | fan-in | merge passes | parallel I/Os |
|---|---|---|---|
| 1 | 999 | 2 | 6000000 |
| 10 | 99 | 2 | 600000 |
| 100 | 9 | 4 | 100000 |

With 10 disks, striping gives the full factor of 10. With 100 disks, the fan-in drops to 9 and the sort needs 4 merge passes instead of 2, so it gains a factor of 60, not 100. Here $\log m / \log(m/D) = 3$.

**RAID arrays.** RAID level 0 is striping with no redundancy. RAID levels 4 and 5 add a parity block to each stripe. A write of a full stripe computes the parity from the new data, but a write of one block must also read the old block and the old parity. Vitter's Section 4.2 explains that optimal sorting needs independent disks only for input or only for output, so a sort can keep striped writes, which makes parity easy.

**Scans and B-trees.** A scan, a copy or a filter is a stream over the file, so it reads one stripe per parallel I/O and is optimal. A [B-tree](/b-tree/) with nodes of $DB$ items reads one node per parallel I/O, and its height is $\log_{DB} N$, which is also optimal for one search.

## Variations

- **Striping unit.** The unit that goes to one disk can be one block, or several blocks, or a few bits or bytes, as in the bit-interleaved RAID level 3. A large unit gives a small request one disk; a small unit spreads every request over all disks.
- **Partial striping.** Group the $D$ disks into $D/c$ clusters of $c$ disks, stripe inside each cluster, and control the clusters independently. The logical block is $cB$ items, so the fan-in falls less.
- **Independent disks.** Optimal sorts on $D$ disks control each disk on its own. [Balance sort](/balance-sort/) and the randomized cycling of [external samplesort](/external-samplesort/) place the blocks of each bucket so that the next $D$ blocks needed are on different disks.
- **Striping only the output.** Read the disks independently and write stripes. Vitter's survey shows that this is sufficient for an optimal sort.

## Pitfalls

- **Counting the memory in stripes.** With stripes as blocks, memory holds only $m/D$ blocks. If the fan-in in line L1 is computed as $m - 1$, memory overflows.
- **Too many disks for the memory.** If $D \ge m/2$, memory holds fewer than 2 stripes plus an output stripe, and a striped merge cannot run. The algorithm must then stop striping or use partial striping.
- **Expecting a factor of D for sorting.** Striping divides the cost of a scan by $D$, but it divides the cost of a sort by less, because of the smaller fan-in.
- **A file that does not start at a stripe.** If logical block $j$ in line L3 does not start on disk 0, a read of one logical block touches two stripes, and the cost doubles.

## Exercises

1. Show that $\log m / \log(m/D) \le 2$ when $1 \le D \le \sqrt m$.
2. For $m = 4096$, find the largest number of disks $D$ for which striped merge sort with $r = 1000$ runs still needs only one merge pass.
3. Write item 1234 of a file in the form (disk, block, offset) for $D = 4$ disks and $B = 100$ items.
4. Compute the striped sort cost of the example for $D = 50$, and compare it with $D = 10$ and $D = 100$.

## References
