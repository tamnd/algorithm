---
tag: 62BBM5
kind: model
slug: external-memory-model
name: External memory model
aliases:
- Aggarwal-Vitter model
- I/O model
- disk access model
area: foundations/models-of-computation
level: core
summary: Two-level memory model counting block transfers between a cache of size M and disk with block size B.
prereqs: [random-access-machine, memory-hierarchy, asymptotic-notation]
see_also: [cache-oblivious-model, b-tree, external-merge-sort, external-sorting-io-lower-bound, external-permuting, buffer-tree, red-blue-pebble-game, external-searching]
sources:
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988)
    locator: pp. 1116 to 1127 (the model, and the bounds for sorting, FFT, permutation networks, permuting and matrix transposition)
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 2 (the parallel disk model), Chapter 3 (Table 3.1), Theorems 5.1, 5.3, 5.4, 6.1, 7.1 and 7.2, Table 9.1, Sections 11.1 and 11.4
  - paper: "Jeffrey Scott Vitter and Elizabeth A. M. Shriver, Algorithms for parallel memory I: two-level memories, Algorithmica 12(2/3) (1994)"
    locator: pp. 110 to 147 (the parallel disk model)
  - paper: "Robert W. Floyd, Permuting information in idealized two-level storage, in Raymond E. Miller and James W. Thatcher (editors), Complexity of Computer Computations, Plenum Press (1972)"
    locator: pp. 105 to 109
  - paper: "Jia-Wei Hong and H. T. Kung, I/O complexity: the red-blue pebble game, Proceedings of the 13th ACM Symposium on Theory of Computing (1981)"
    locator: pp. 326 to 333
  - paper: "David A. Hutchinson, Peter Sanders and Jeffrey Scott Vitter, Duality between prefetching and queued writing with parallel disks, SIAM Journal on Computing 34(6) (2005)"
    locator: pp. 1443 to 1463 (the lower bound with constant 2, Theorem 6.1 in Vitter's survey)
  - paper: "Lars Arge, The buffer tree: a technique for designing batched external data structures, Algorithmica 37(1) (2003)"
    locator: pp. 1 to 24
  - paper: "Yi-Jen Chiang, Michael T. Goodrich, Edward F. Grove, Roberto Tamassia, Darren E. Vengroff and Jeffrey Scott Vitter, External-memory graph algorithms, Proceedings of the 6th ACM-SIAM Symposium on Discrete Algorithms (1995)"
    locator: pp. 139 to 149 (list ranking and time-forward processing)
  - paper: "Lars Arge, Mikael Knudsen and Kirsten Larsen, A general lower bound on the I/O-complexity of comparison-based algorithms, Workshop on Algorithms and Data Structures (WADS 1993)"
    locator: pp. 83 to 94
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 18 (B-trees), Section 18.1 (the height bound)
---

The external memory model (also called the I/O model or the disk access model) is a model of computation with a fast internal memory of $M$ items and an unbounded external memory, such as a disk, that the two exchange in blocks of $B$ items. The cost of an algorithm is the number of block transfers (I/Os), and computation in the internal memory is free. Aggarwal and Vitter defined it in 1988 and proved tight bounds in it for sorting and related problems. It is the standard two-level form of the [memory hierarchy](/memory-hierarchy/), and the [cache-oblivious model](/cache-oblivious-model/) is its variant in which the algorithm does not know $M$ and $B$.

## The machine

The machine has a processor, an internal memory and an external memory.

- The internal memory holds $M$ items. The processor works only on items in the internal memory, as a [random access machine](/random-access-machine/) does.
- The external memory is unbounded and is divided into blocks. Block $i \ge 0$ holds the items at positions $iB$ to $(i+1)B - 1$.
- One *I/O* copies one whole block from the external memory into $B$ cells of the internal memory, or copies $B$ items from the internal memory into one whole block of the external memory.
- Items have a fixed size and are *indivisible*: the algorithm copies, moves and compares them, but the lower bounds do not allow it to split an item into bits or to combine items.
- The $N$ input items fill $\lceil N/B \rceil$ consecutive blocks at the start, and the output must fill consecutive blocks in the same way.

The parameters satisfy $M < N$ and $1 \le B \le M/2$, so that the internal memory holds at least two blocks (Vitter, Section 2.1). It is usual to write $n = N/B$ and $m = M/B$ for the sizes in blocks.

The algorithm decides which blocks to read and write, and which items to keep. There is no cache that evicts items by itself: the algorithm controls the internal memory explicitly. This is the main difference from the [cache-oblivious model](/cache-oblivious-model/).

Aggarwal and Vitter allowed one I/O to move up to $P$ blocks at once, at any positions. The *parallel disk model* of Vitter and Shriver (1994) is closer to real disks: it has $D$ independent disks, and one I/O moves at most one block on each disk. This page treats $P = D = 1$. The lower bounds of Aggarwal and Vitter also hold in the parallel disk model, because that model is a restriction of theirs (Vitter, Section 2.3).

## What it counts

The cost of an algorithm on an input is the number of I/Os that it makes. The bounds are worst-case bounds, as functions of $N$, $M$ and $B$, unless the text says otherwise. A second measure is the space in the external memory, in blocks. An analysis can also state the internal computation time, but the model does not charge for it.

The unit is the item, not the byte. $B$ and $M$ are counted in items of the problem.

Four bounds appear in most results (Vitter, Table 3.1):

$$\mathrm{Scan}(N) = \Theta\!\left(\frac{N}{B}\right), \qquad \mathrm{Sort}(N) = \Theta\!\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right),$$

$$\mathrm{Search}(N) = \Theta(\log_B N), \qquad \mathrm{Output}(Z) = \Theta\!\left(\max\left\{1, \frac{Z}{B}\right\}\right),$$

where $Z$ is the number of items in the answer to a query. In this notation $\mathrm{Sort}(N) = \Theta(n \log_m n)$. Scanning is the linear cost of the model. Sorting is the cost of most batched problems that are easy in internal memory, such as permuting, list ranking and transposing a matrix.

## Relation to other models

- **Random access machine.** The [random access machine](/random-access-machine/) charges one step for any access. Here an access to an item in a block that is not in the internal memory costs one I/O, and the other $B - 1$ items of the block come with it. A RAM algorithm that accesses memory at random can use one I/O per access, which is up to $B$ times more than an algorithm that uses every item of each block it reads.
- **Cache-oblivious model.** The [cache-oblivious model](/cache-oblivious-model/) has the same two levels, but the algorithm does not know $M$ and $B$, and an ideal cache moves the blocks by the optimal offline rule. An optimal cache-oblivious algorithm is also optimal here, up to a constant factor (Vitter, Section 2.3), and a lower bound here is also a lower bound there, because a cache-oblivious algorithm is a special external memory algorithm.
- **Earlier models.** Floyd (1972) studied permuting and transposing in a two-level storage with $B = M/2$ and gave matching upper and lower bounds for those parameters (Vitter, Section 2.3). Hong and Kung (1981) introduced the [red-blue pebble game](/red-blue-pebble-game/), which counts word transfers ($B = 1$) for a computation given as a fixed graph. Aggarwal and Vitter (1988) allowed general $M$ and $B$, and proved bounds that are tight for all parameter values.
- **Several disks.** In the parallel disk model the bounds for scanning, sorting and output are divided by $D$, and searching becomes $\Theta(\log_{DB} N)$ (Vitter, Table 3.1). [Disk striping](/disk-striping/) treats the $D$ disks as one disk with blocks of $DB$ items. It is optimal for scanning and searching, but for sorting it makes $\Theta\big(\frac{n}{D}\log_{m/D}\frac{n}{D}\big)$ I/Os, which is more than the optimum by a factor of about $\frac{\log m}{\log(m/D)}$ (Vitter, Section 4.2).
- **Real disks.** The model gives every I/O the same cost. On a hard disk, a random I/O pays a seek and a rotational delay, and a sequential I/O does not, so two algorithms with the same I/O count can differ in time (Vitter, Section 2.2).

## Known results in the model

All bounds count I/Os in the worst case with one disk, $1 \le B \le M/2$ and $M < N$, unless the text says otherwise.

**Scanning.** Reading $N$ consecutive items takes $\lceil N/B \rceil$ I/Os. The bound is tight for every problem whose answer depends on every item, such as the sum of the items. The input fills $\lceil N/B \rceil$ blocks, and an algorithm that reads fewer blocks never sees some item. Changing that item changes the sum but not the run of the algorithm, so the algorithm gives a wrong answer on one of the two inputs.

**Searching.** Let $N$ keys be stored in blocks in any fixed layout, and let a query ask for the rank of a key $q$ among them, with only comparisons on keys. Then every algorithm makes at least $\log_{B+1}(N+1)$ reads in the worst case. Proof: the order of the stored keys is fixed and known in advance, so only comparisons with $q$ give information. A key is compared with $q$ only after the block that holds it is read. When a block of at most $B$ keys is read, the comparisons of $q$ with these keys have at most $B + 1$ different outcomes (the position of $q$ among them), and later comparisons with the same keys add nothing new. A write gives no information. So the algorithm is a tree in which each read has at most $B + 1$ children. There are $N + 1$ possible ranks, so the tree has at least $N + 1$ leaves, and its depth in reads is at least $\log_{B+1}(N+1)$. $\square$

The [B-tree](/b-tree/) meets this bound. A B-tree of minimum degree $t \ge 2$ with $N \ge 1$ keys has height $h \le \log_t \frac{N+1}{2}$ (CLRS, Section 18.1). Store one node in one block, with $t = \lfloor B/4 \rfloor$, so that the at most $2t - 1$ keys and $2t$ child pointers of a node fit in $B$ items. For $B \ge 8$ this gives $t \ge 2$ and $t = \Theta(B)$. A search reads one node on each of the $h + 1$ levels, so it takes $O(\log_B N)$ I/Os. Insertion and deletion take $O(\log_B N)$ I/Os, and a range query that reports $Z$ keys takes $O(\log_B N + Z/B)$ I/Os (Vitter, Section 11.1). [Binary search](/binary-search/) on a sorted array takes $\Theta(\log_2(N/B))$ I/Os, a factor of about $\log_2 B$ more. Hashing finds a key in $O(1)$ I/Os on average, because it does not compare keys. See [external searching](/external-searching/) and [extendible hashing](/extendible-hashing/).

**Sorting.** For $N > M$, sorting $N$ items takes $\Theta\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os (Aggarwal and Vitter 1988; Vitter, Theorem 5.1). The lower bound is proved on the page [external sorting I/O lower bound](/external-sorting-io-lower-bound/). For indivisible items and $B \log m = \omega(\log N)$, every algorithm needs at least $(2 - o(1))\, n \log_m n$ I/Os, so the constant in front is at least 2 (Hutchinson, Sanders and Vitter 2005; Vitter, Theorem 6.1). Arge, Knudsen and Larsen (1993) showed more generally that in the comparison model every problem with an $\Omega(N \log N)$ lower bound on comparisons needs $\Omega(n \log_m n)$ I/Os.

The upper bound comes from [external merge sort](/external-merge-sort/). Here is the argument when $M \ge 3B$ and $B$ divides $M$. If $B$ does not divide $M$, use $B \lfloor M/B \rfloor$ in place of $M$, which changes $M/B$ by less than a factor of 2 and the bound by a constant factor. Aggarwal and Vitter cover the case $2B \le M < 3B$, which is not derived here.

1. Read $M$ items, sort them in the internal memory, and write them back as one sorted *run*. This gives $\lceil N/M \rceil$ runs for at most $2\lceil N/B \rceil$ I/Os.
2. Let $k = M/B - 1 \ge 2$. Merge $k$ runs at a time ([k-way merge](/k-way-merge/)). The internal memory holds one block of each input run and one output block, $(k+1)B = M$ items. A merge pass reads and writes each block once, so it costs at most $2\lceil N/B \rceil$ I/Os, and it divides the number of runs by $k$, rounded up.
3. After $\lceil \log_k \lceil N/M \rceil \rceil$ passes one run is left. The total is at most $2\lceil N/B \rceil\,(1 + \lceil \log_k \lceil N/M \rceil \rceil) \le 2\lceil N/B \rceil\,(2 + \log_k \lceil N/M \rceil)$.
4. Let $L = \log_{M/B}(N/B)$. Because $M/B \ge 3$, $k = M/B - 1 \ge \sqrt{M/B}$, so $\log_k x \le 2 \log_{M/B} x$ for $x \ge 1$. Because $N > M \ge 2B$, $\lceil N/M \rceil < 2N/M \le N/B$, so $\log_{M/B} \lceil N/M \rceil \le L$. Also $L > 1$, because $N/B > M/B$. So the total is at most $2\lceil N/B \rceil (2 + 2L) < 8 \lceil N/B \rceil L = O\big(\frac{N}{B} \log_{M/B} \frac{N}{B}\big)$. $\square$

If $N \le M$, one read and one write of all blocks sort the items in $2\lceil N/B \rceil$ I/Os. Distribution sort, the dual method, splits the items into buckets by $S - 1$ splitters, writes each bucket in blocks, and sorts each bucket recursively. With $S = \Theta(\min\{m, n/m\})$ splitters from a random sample, or $S = \Theta(\min\{\sqrt{m}, n/m\})$ splitters chosen deterministically, it has the same bound (Vitter, Section 5.1).

**Permuting.** Moving $N$ items into a given order takes $\Theta\big(\min\{N, \mathrm{Sort}(N)\}\big)$ I/Os for indivisible items (Aggarwal and Vitter 1988; Vitter, Theorem 5.3). The term $N$ is the naive method: for each output block, read the block of each of its $B$ items, then write the output block, for $N + \lceil N/B \rceil$ I/Os. The naive method is better only when $B \log m = o(\log n)$, which means a tiny block or a tiny memory (Vitter, Section 5.6). In the usual case, permuting costs as much as sorting, although it is linear time on a RAM. See [external permuting](/external-permuting/) and the [permuting lower bound](/permuting-lower-bound/).

**FFT and permutation networks.** Computing the $N$-input FFT graph, or running an $N$-input permutation network, takes $\Theta(\mathrm{Sort}(N))$ I/Os (Aggarwal and Vitter 1988; Vitter, Theorem 5.4). See the [fast Fourier transform](/fast-fourier-transform/).

**Matrix transposition.** Transposing a $p \times q$ matrix from row-major to column-major order, with $N = pq$, takes

$$\Theta\!\left(\frac{N}{B}\log_{M/B} \min\left\{M, p, q, \frac{N}{B}\right\}\right)$$

I/Os (Aggarwal and Vitter 1988; Vitter, Theorem 7.2). If $B^2 \le M$, this is $O(N/B)$: the matrix splits into $B \times B$ submatrices, each made of $B$ row blocks and $B$ column blocks, and each fits in the internal memory. Floyd (1972) proved the first lower bound of this kind, for a special case.

**Matrix multiplication.** The standard method, with only semiring operations, multiplies two $K \times K$ matrices with $\Theta\big(K^3/(\min\{K, \sqrt{M}\}\, B)\big)$ I/Os (Vitter, Theorem 7.1). The upper bound blocks the matrices into $\sqrt{M/3} \times \sqrt{M/3}$ submatrices. The lower bound comes from the [red-blue pebble game](/red-blue-pebble-game/) of Hong and Kung (1981) and its extension to blocks by Savage and Vitter.

**Graph problems.** List ranking, the Euler tour of a tree and the evaluation of an expression tree with $V$ vertices take $\Theta(\mathrm{Sort}(V))$ I/Os (Chiang, Goodrich, Grove, Tamassia, Vengroff and Vitter 1995; Vitter, Table 9.1). The lower bound holds because these problems are as hard as permuting. The upper bounds use *time-forward processing*, which passes values along the edges of a directed acyclic graph through a priority queue. See [list ranking](/list-ranking/) and [time-forward processing](/time-forward-processing/).

**Batched data structures.** An external stack or queue takes $O(1/B)$ amortized I/Os per operation, because it keeps the active end of the sequence in one or two blocks in memory. The [buffer tree](/buffer-tree/) of Arge is a tree of degree $\Theta(m)$ in which each node has a buffer of $\Theta(M)$ items. Items move down a level only when a buffer is full, a whole buffer at a time. Inserts, deletes and delete-min then cost $O\big(\frac{1}{B}\log_{M/B}\frac{N}{B}\big)$ amortized I/Os each, so $N$ operations cost $O(\mathrm{Sort}(N))$ (Arge 2003; Vitter, Section 11.4). See the [external memory priority queue](/external-memory-priority-queue/).

**Example.** Let $N = 2^{30}$ items, $M = 2^{20}$ and $B = 2^{10}$, so $n = 2^{20}$ and $m = 2^{10}$.

| Task | Count |
|---|---|
| Scan | $n = 1048576$ I/Os |
| $\log_m n$ | $2$ |
| Merge sort: runs of $M$ items | $N/M = 1024$ runs |
| Merge sort: merge passes with $k = m - 1 = 1023$ | $\lceil \log_{1023} 1024 \rceil = 2$ |
| Merge sort: total, $2n(1 + 2)$ | $6291456$ I/Os, that is 6 scans |
| Naive permuting, $N + n$ | $1074790400$ I/Os, about 171 times the merge sort |
| B-tree with $t = B/4 = 256$: height bound $\log_{256}\frac{N+1}{2}$ | about 3.6, so $h \le 3$ and a search reads at most 4 blocks |
| Binary search on the sorted array | about $\log_2 n = 20$ block reads |
| Transposing a $2^{15} \times 2^{15}$ matrix: $\log_m \min\{M, p, q, n\} = \log_{1024} 2^{15}$ | $1.5$, so $\Theta(1.5\, n)$ I/Os |

The 1024 runs are just one more than $k = 1023$, so one buffer less in memory costs a whole extra pass. Runs of about $2M$ items, which [replacement selection](/replacement-selection/) gives on random input, would halve the number of runs and allow one merge pass.

### Pitfalls

- **Bytes against items.** $M$ and $B$ are counted in items. A disk block of 64 KB with records of 100 bytes gives $B = 655$, not 65536.
- **The base of the logarithm.** The sort bound has $\log_{M/B}$, not $\log_2$ and not $\log_M$. With realistic values, $\log_{M/B}(N/B)$ is a small constant such as 2 or 3, so sorting costs a few scans. Hiding it inside a constant loses this information, and writing $\log_2$ overstates the cost by a factor of about $\log_2(M/B)$.
- **A B-tree for batched work.** Inserting $N$ items into a B-tree costs $\Theta(N \log_B N)$ I/Os, which is about a factor of $B$ more than $\mathrm{Sort}(N)$ (Vitter, Section 11.4). Use sorting, or a [buffer tree](/buffer-tree/), when the answers can wait.
- **Permuting looks free.** Permuting takes linear time on a RAM, but here it costs $\Theta(\min\{N, \mathrm{Sort}(N)\})$, which is usually the sort bound. Do not write $O(N/B)$ for an algorithm that moves items to arbitrary places.
- **The output buffer.** A $k$-way merge needs $k$ input blocks and one output block. Taking $k = M/B$ does not fit, and in the example above $k = M/B - 1$ costs a full extra pass.
- **The model's assumptions in a lower bound.** The sorting and permuting lower bounds need indivisible items, and the searching bound needs comparisons. Hashing searches in $O(1)$ expected I/Os, so the $\Theta(\log_B N)$ bound is not a bound for all algorithms.
- **All I/Os cost the same.** On a hard disk, a sequential I/O is much cheaper than a random one. An algorithm that does more I/Os, all sequential, can be faster than one with fewer random I/Os.
- **$N \le M$.** When the input fits in memory, every problem here costs $O(N/B)$. The bounds above assume $N > M$.

## References
