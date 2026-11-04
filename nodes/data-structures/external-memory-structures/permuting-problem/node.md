---
tag: 402D9F
kind: problem
slug: permuting-problem
name: Permuting problem
aliases:
- external permutation
area: data-structures/external-memory-structures
level: advanced
summary: Rearrange N records stored on disk into a given permutation order.
model: external-memory-model
prereqs: [external-memory-model, external-merge-sort]
see_also: [permuting-lower-bound, external-permuting, external-sorting-lower-bound, external-merge-sort, distribution-sort, list-ranking, disk-striping]
sources:
  - paper: doi:10.1145/48529.48535
    title: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988), 1116-1127"
    locator: Theorem 3.2 (permuting) and the bounds for matrix transposition and the FFT in Section 3
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 3 (the bound Perm(N) and the table of fundamental bounds), Chapter 6 (lower bounds, Section 6.1 on permuting)
  - paper: "Yi-Jen Chiang, Michael T. Goodrich, Edward F. Grove, Roberto Tamassia, Darren E. Vengroff and Jeffrey Scott Vitter, External-memory graph algorithms, Proceedings of the 6th ACM-SIAM Symposium on Discrete Algorithms (1995)"
    locator: pp. 139 to 149 (lower bounds for graph problems by reduction from permuting)
---

The permuting problem asks to rearrange $N$ records on disk so that the record with target $\pi(i)$ ends in position $\pi(i)$, for a permutation $\pi$ that is known in advance. In internal memory this is trivial: one pass, $N$ moves. In the [external memory model](/external-memory-model/) it is as hard as sorting: it costs $\Theta\big(\min\big\{N, \frac{N}{B}\log_{M/B}\frac{N}{B}\big\}\big)$ block transfers, which Vitter writes as $\mathrm{Perm}(N)$. The two terms are the two methods: move one record per I/O, or sort the records by their targets. The lower bound is the [permuting lower bound](/permuting-lower-bound/) of Aggarwal and Vitter. The same problem, seen from external sorting, is on the [external permuting](/external-permuting/) page.

## In plain words

You have a huge file of records, and for each record you know the place where it must go. You do not need to compare anything. You only have to move the records.

On a disk this is hard. Records come in blocks, and the records of one block must usually go to many different blocks. If you fetch each record on its own, you pay one disk transfer per record. The better way, for large blocks, is to sort the records by their target places, which reads the whole file only a few times. No method does much better than the better of these two.

## Definition

**Model.** The [external memory model](/external-memory-model/) with an internal memory of $M$ items, blocks of $B$ items, $1 \le B \le M/2$, and $n = N/B$ blocks of input. Records are indivisible.

**Input.** $N$ records in the blocks $0, \ldots, n - 1$. Each record carries its *target*, an integer $\pi(i)$, and the targets form a permutation of $\{1, \ldots, N\}$. (When $\pi$ is given as a separate array, or as a formula, the algorithm can attach the targets with a scan and a sort of the array, or for free, so the forms are equivalent up to $O(\mathrm{Sort}(N))$.)

**Output.** The same records, in the blocks $0, \ldots, n - 1$, with the record of target $p$ in the cell $p$.

**Cost.** The number of block reads and writes in the worst case over $\pi$.

## Variants

- **Known structure.** For special permutations the cost can be lower. A cyclic shift by a multiple of $B$ costs $O(N/B)$, and so does any permutation that moves whole blocks. Matrix transposition and the bit-reversal permutation of the FFT have their own tight bounds, found by Aggarwal and Vitter, which for some shapes are below $\mathrm{Perm}(N)$.
- **In-place permuting.** Use only $O(1)$ blocks of extra disk space. Following the cycles of $\pi$ is in place but costs one I/O per record.
- **Parallel disks.** With $D$ disks, the bound becomes $\Theta\big(\min\big\{\frac{N}{D}, \frac{N}{DB}\log_{M/B}\frac{N}{B}\big\}\big)$.
- **Cache-oblivious permuting.** An algorithm that does not know $M$ and $B$ cannot always choose the better of the two terms. Brodal and Fagerberg proved that a cache-oblivious algorithm cannot meet the bound for all $M$ and $B$, but cache-oblivious sorting, such as [funnelsort](/funnelsort/), gives the sort term under the tall-cache assumption.
- **Scattering and gathering.** Writing records to target positions that are not a permutation (some positions empty), or reading records from given positions (a gather), have the same bound by the same methods.

## Examples

**A small run.** Take $N = 8$, $B = 2$, $M = 6$, and the input blocks $[a\ b]\ [c\ d]\ [e\ f]\ [g\ h]$ with the targets $a{:}8, b{:}1, c{:}6, d{:}3, e{:}2, f{:}7, g{:}4, h{:}5$. The output is $[b\ e]\ [d\ g]\ [h\ c]\ [f\ a]$. Each output block takes its two records from two different input blocks, and so does each input block send its records to two different output blocks. The naive method reads, for the output block $[b\ e]$, the blocks of $b$ and $e$, then writes: 8 reads and 4 writes, 12 I/Os. Sorting by target makes two runs, of 6 and 2 records, and merges them, so it reads and writes each block twice: 16 I/Os. At this tiny size the naive method wins.

**A large file.** Take $N = 10^{10}$ records, $B = 10^4$ and $M = 8 \cdot 10^7$, so $n = 10^6$ blocks. The naive method makes about $10^{10}$ reads. External merge sort makes runs of $M$ records, 125 of them, and merges them in one pass, so it reads and writes each block twice: $4 \times 10^6$ I/Os, 2500 times fewer. The [permuting lower bound](/permuting-lower-bound/) gives at least about $1.38 \times 10^6$ I/Os for some $\pi$, so sorting is within a factor of 3.

**Tiny blocks.** With $B = 1$, the naive method costs $2N$ I/Os and sorting costs $\Theta(N \log N / \log M)$, more than $N$. Here permuting is cheaper than sorting.

## Known algorithms

| method | I/Os | memory | notes |
|---|---|---|---|
| naive: fill each output block by reading the blocks of its records | $N + N/B$ | $2B$ | best for tiny $B$ |
| follow the cycles of $\pi$ | about $2N$ | $O(B)$ | in place |
| [external merge sort](/external-merge-sort/) on the targets | $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ | $M$ | best for usual $B$ |
| [distribution sort](/distribution-sort/) on the targets, with exact splitters | $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ | $M$ | the targets are known, so the buckets need no sampling |
| take the better of the first and the third | $O(\min\{N, \mathrm{Sort}(N)\})$ | $M$ | optimal |

With known targets, a distribution pass can split the records into $M/B$ ranges of targets of equal size, and $\log_{M/B}(N/B)$ passes bring each record to its block. This is a radix sort on the targets with radix $M/B$.

## Bounds

- **Lower bound.** Every algorithm with indivisible records, even one designed for the given $\pi$, needs $\Omega\big(\min\big\{N, \frac{N}{B}\log_{M/B}\frac{N}{B}\big\}\big)$ I/Os for some $\pi$, and for most $\pi$. The proof is a count of the ways in which one I/O can change the sets of records in the blocks; see the [permuting lower bound](/permuting-lower-bound/).
- **Upper bound.** The methods above meet the bound, so $\mathrm{Perm}(N) = \Theta(\min\{N, \mathrm{Sort}(N)\})$.
- **Which term is smaller.** $N < \frac{N}{B}\log_{M/B}\frac{N}{B}$ exactly when $B\log\frac{M}{B} < \log\frac{N}{B}$. For any realistic disk, with $B$ in the hundreds or more, the sort term is smaller, so in practice $\mathrm{Perm}(N) = \Theta(\mathrm{Sort}(N))$.

## Reductions

- **Permuting reduces to sorting.** Sort the records by their targets. So $\mathrm{Perm}(N) = O(\mathrm{Sort}(N))$.
- **Sorting indivisible items is at least permuting.** A sort must move each record to the place of its rank, which is a permutation. So the permuting bound is also a lower bound for sorting, for every sorting algorithm that moves whole records, with or without comparisons.
- **Graph and list problems are at least permuting.** [List ranking](/list-ranking/), the Euler tour of a tree, and many problems on graphs can be given inputs on which their output, or a step of their work, is an arbitrary permutation of the input. Chiang and others (1995) used this to prove $\Omega(\mathrm{Perm}(N))$ lower bounds for them, which [time-forward processing](/time-forward-processing/) and sorting then meet.

## Applications

- **Applying a computed order.** Sort small (key, record id) pairs, then permute the large records into that order. The second step is permuting.
- **Changing the layout of data.** Transposing a matrix stored by rows into one stored by columns, or turning a tree into the [van Emde Boas layout](/van-emde-boas-layout/), is a permutation of the cells.
- **Graph algorithms.** Relabeling the vertices of a graph, and moving the data of each vertex to the place of its new label, is permuting. External graph algorithms do this at each step.
- **Joins in databases.** A join through record ids fetches records in an order given by another table, which is a gather with the same cost.

## References
