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
see_also: [cache-oblivious-model, b-tree, external-merge-sort, external-sorting-io-lower-bound, external-permuting, red-blue-pebble-game, external-searching]
sources:
  - paper: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988), 1116 to 1127"
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory
    locator: Chapters 1 to 3
  - paper: "Jeffrey Scott Vitter and Elizabeth A. M. Shriver, Algorithms for parallel memory I: two-level memories, Algorithmica 12 (1994)"
  - paper: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985)"
  - paper: "Lars Arge, The buffer tree: a new technique for optimal I/O-algorithms, Workshop on Algorithms and Data Structures (1995)"
  - paper: "Jia-Wei Hong and H. T. Kung, I/O complexity: the red-blue pebble game, Proceedings of the 13th ACM Symposium on Theory of Computing (1981)"
  - paper: "Robert W. Floyd, Permuting information in idealized two-level storage, in Complexity of Computer Computations, Plenum Press (1972)"
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 18 (B-trees)
---

The external memory model (also called the I/O model or the disk access model) is a model of computation with a small fast internal memory of $M$ items and a large external memory, such as a disk. The two memories exchange data in blocks of $B$ items, and the cost of an algorithm is the number of block transfers (I/Os) that it makes. Aggarwal and Vitter defined it in 1988 to study sorting and related problems on data that does not fit in main memory. In this model, sorting $N$ items takes $\Theta((N/B)\log_{M/B}(N/B))$ I/Os, and searching in a [B-tree](/b-tree/) takes $O(\log_B N)$ I/Os.

## The machine

The machine has two levels of memory. The levels are a simple form of the [memory hierarchy](/memory-hierarchy/).

- The internal memory holds $M$ items. The processor works only on items in the internal memory.
- The external memory is unbounded. It is divided into blocks of $B$ consecutive items.
- One *I/O* copies one block from the external memory to the internal memory, or one block from the internal memory to the external memory.
- The parameters satisfy $M \ge 2B$ and $N > M$. This page assumes both. (Later work such as Vitter 2008 also assumes $M \ge 2B$.)
- The $N$ input items are stored in $\lceil N/B \rceil$ consecutive blocks of the external memory. The output is written in the same way.

The algorithm decides which blocks to read and which items to remove from the internal memory. There is no cache that evicts items by itself. An algorithm is a sequence of I/Os and of computations on the internal memory.

## What it counts

The cost of an algorithm on an input is the number of I/Os. Computation in the internal memory is free. The model does not count the number of instructions, but an analysis can state the number of instructions as well. The bounds below are worst-case bounds in $N$, $M$ and $B$. Items are treated as atoms: the lower bounds hold for algorithms that copy and compare items but do not combine their bits (the comparison model, and the model of indivisible items in the paper).

The unit of the data is the item, not the byte. The block size $B$ and the memory size $M$ are counted in items.

Two terms are used in all bounds. They are

$$\mathrm{Scan}(N) = \lceil N/B \rceil, \qquad \mathrm{Sort}(N) = \frac{N}{B}\log_{M/B}\frac{N}{B}.$$

## Relation to other models

- The [random access machine](/random-access-machine/) charges one step for each access to any cell. The external memory model charges one I/O for each block, and a block is $B$ items. An algorithm for the random access machine that accesses memory at random uses up to one I/O for each access, which is a factor of $B$ more than an algorithm that reads a block and uses all its items.
- The [cache-oblivious model](/cache-oblivious-model/) uses the same two levels, but the algorithm does not know $M$ and $B$, and the cache evicts blocks by the optimal offline rule. This is justified because least-recently-used eviction with a cache of $2M$ items makes at most twice as many I/Os as the optimal rule with a cache of $M$ items, apart from the first load of each block (Sleator and Tarjan 1985). The I/O bound of a cache-oblivious algorithm then holds for every $M$ and $B$, sometimes under the tall-cache assumption $M = \Omega(B^2)$.
- Earlier models: the [red-blue pebble game](/red-blue-pebble-game/), introduced by Hong and Kung (1981), is an earlier formal model of I/O cost. Floyd (1972) studied permuting and transposing in a two-level storage model. Aggarwal and Vitter (1988) gave the model with general $M$ and $B$ and tight bounds for sorting.
- Aggarwal and Vitter also let one I/O move up to $P$ arbitrary blocks at once. The parallel disk model of Vitter and Shriver (1994) is more realistic: it has $D$ independent disks, and one I/O moves at most one block from each disk. This page treats $P = D = 1$.

## Known results in the model

All bounds are worst-case bounds on the number of I/Os, with $M \ge 2B$.

**Scanning.** Reading the $N$ input items takes $\lceil N/B \rceil$ I/Os, because each I/O brings in a block of $B$ items. The bound is tight for a problem whose answer depends on every item, for example the sum of the items. The input fills $\lceil N/B \rceil$ blocks. An algorithm that reads fewer than $\lceil N/B \rceil$ different blocks never sees some input item, and changing this item changes the sum. So the sum costs $\Theta(N/B)$ I/Os.

**Sorting.** For $N > M$, sorting $N$ items takes $\Theta\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right)$ I/Os. Aggarwal and Vitter proved this bound. The lower bound holds for sorting by comparisons. The page [external sorting I/O lower bound](/external-sorting-io-lower-bound/) has the statement and its proof. The upper bound comes from [external merge sort](/external-merge-sort/). Here is the argument for the upper bound, when $M \ge 3B$ and $B$ divides $M$. If $B$ does not divide $M$, run it with $M$ replaced by $B\lfloor M/B \rfloor$, which changes $M/B$ by less than a factor of 2 and so changes the bound by a constant factor. For $2B \le M < 3B$ the same bound holds (Aggarwal and Vitter), and this page does not derive it.

1. Read $M$ items, sort them in the internal memory, and write them back as one *run*. After $\lceil N/M \rceil$ such steps there are $\lceil N/M \rceil$ sorted runs. This costs at most $2\lceil N/B \rceil$ I/Os.
2. Let $k = \lfloor M/B \rfloor - 1$. Then $k \ge 2$. Merge $k$ runs at a time: keep one block of each input run and one block of the output in the internal memory, which needs $(k+1)B \le M$ items. One merge pass reads and writes each item once, so it costs at most $2\lceil N/B \rceil$ I/Os, and it divides the number of runs by $k$, rounding up.
3. After $\lceil \log_k \lceil N/M \rceil \rceil$ passes there is one run. The total is at most $2\lceil N/B \rceil\,(1 + \lceil \log_k \lceil N/M \rceil \rceil) \le 2\lceil N/B \rceil\,(2 + \log_k \lceil N/M \rceil)$.
4. Because $M/B \ge 3$, we have $k \ge \sqrt{M/B}$, so $\log_k x \le 2\log_{M/B} x$ for $x \ge 1$. Because $N > M$, we have $\lceil N/M \rceil < 2N/M \le N/B$, so $\log_{M/B}\lceil N/M \rceil \le L$, where $L = \log_{M/B}(N/B)$. Also $L > 1$, because $N/B > M/B$. The total is therefore at most $2\lceil N/B \rceil (2 + 2L) < 8\lceil N/B \rceil L = O((N/B) L)$.

If $N \le M$, the items fit in the internal memory, and sorting takes $\Theta(N/B)$ I/Os: one scan to read and one to write.

**Permuting.** Moving $N$ items into a given order takes $\Theta(\min\{N, \mathrm{Sort}(N)\})$ I/Os for indivisible items (Aggarwal and Vitter). The term $N$ is the cost of the naive method, which fills each output block by reading the source block of each of its items: $N + \lceil N/B \rceil$ I/Os. For practical values of $M$ and $B$, $\mathrm{Sort}(N) < N$, so permuting costs as much as sorting. See [external permuting](/external-permuting/).

**Searching.** Finding a key in a sorted set of $N$ keys takes $\Theta(\log_{B+1} N)$ I/Os for algorithms that compare keys, which is $\Theta(\log_B N)$ for $B \ge 2$ (Vitter 2008). The upper bound comes from the [B-tree](/b-tree/). A B-tree of minimum degree $t \ge 2$ has every node other than the root with at least $t-1$ and at most $2t-1$ keys, and its height $h$ satisfies $h \le \log_t \frac{N+1}{2}$ for $N \ge 1$ keys (CLRS 4th edition, Chapter 18). If one node is stored in one block, a search reads one node on each level, so it takes $O(h)$ I/Os. Choose $t = \lfloor B/4 \rfloor$, so that a node with its keys and child pointers fits in one block. This needs $B \ge 8$, so that $t \ge 2$. Then $t = \Theta(B)$ and $h = O(\log_B N)$, and search takes $O(\log_B N)$ I/Os. Insertion and deletion also take $O(\log_B N)$ I/Os. Binary search on a sorted array of $\lceil N/B \rceil$ blocks takes $\Theta(\log_2 (N/B))$ I/Os, which is a factor of about $\log_2 B$ more than a B-tree. See [external searching](/external-searching/).

**Priority queues.** A buffer tree (Arge 1995) supports insert and delete-min in $O\left(\frac{1}{B}\log_{M/B}\frac{N}{B}\right)$ amortized I/Os per operation, so $N$ operations cost $O(\mathrm{Sort}(N))$.

**Example.** Let $N = 2^{30}$ items, $B = 2^{10}$ and $M = 2^{20}$. Then $N/B = 2^{20}$ and $M/B = 2^{10}$. A scan takes $2^{20}$ I/Os. Sorting takes about $2^{20}\log_{2^{10}} 2^{20} = 2^{21}$ I/Os, up to a constant factor. The number of passes, $\log_{M/B}(N/B) = 2$, is a small constant, so sorting costs only a few scans. A B-tree search takes about $\log_{2^{10}} 2^{30} = 3$ I/Os, up to a constant factor.

## References
