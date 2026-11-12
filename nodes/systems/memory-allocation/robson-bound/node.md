---
tag: 71MSB3
kind: theorem
slug: robson-bound
name: Robson's bound
aliases:
- Robson's lower bound
area: systems/memory-allocation
level: research
summary: "An allocator that never moves blocks can be forced to use about (1/2) M log2 n words, for live size M and block sizes up to n. Simple schemes need only O(M log n)."
prereqs: [online-memory-allocation, external-fragmentation]
see_also: [first-fit-allocation, best-fit-allocation, size-classes, segregated-free-lists, buddy-system, memory-compaction, offline-dynamic-storage-allocation, competitive-ratio]
sources:
  - paper: doi:10.1145/321650.321658
    title: "J. M. Robson, An estimate of the store size necessary for dynamic storage allocation, Journal of the ACM 18(3) (1971), 416-423"
    locator: the main result, a lower bound for every strategy that grows with the logarithm of the largest block size
  - paper: doi:10.1145/321832.321846
    title: "J. M. Robson, Bounds for some functions concerning dynamic storage allocation, Journal of the ACM 21(3) (1974), 491-499"
    locator: the lower bound, which is the exact solution for block sizes that are powers of 2, and the improved upper bound for general sizes
  - paper: doi:10.1093/comjnl/20.3.242
    title: "J. M. Robson, Worst case fragmentation of first fit and best fit storage allocation strategies, The Computer Journal 20(3) (1977), 242-244"
    locator: the worst case of address-ordered first fit (about M log2 n) and of best fit (about M n)
  - paper: doi:10.1007/3-540-60368-9_19
    title: "Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation: a survey and critical review, IWMM 1995, LNCS 986, 1-116"
    locator: Section 4.1, the paragraphs on Robson 1971, 1974 and 1977 (the 0.5 M log2 n and 0.84 M log2 n bounds, first fit and best fit)
  - url: https://www.sqlite.org/malloc.html
    title: "SQLite, Dynamic Memory Allocation In SQLite"
    locator: Section 4, the Robson proof, the formula N = M(1 + (log2 n)/2) - n + 1 and the power-of-two first-fit allocator memsys5
---

Robson's bound tells how much address space an allocator must reserve so that fragmentation can never make a request fail. Let at most $M$ words be live at any time, and let every block have between $1$ and $n$ words. Every allocator that places blocks online and never moves them can be forced to use about $\tfrac12 M \log_2 n$ words, and a simple allocator gets by with $M(\log_2 n + 1)$. For block sizes that are powers of two, Robson (1974) found the exact value $M(1 + \tfrac12 \log_2 n) - n + 1$.

## Statement

**Model.** This is the model of [online memory allocation](/online-memory-allocation/). The heap is the set of addresses $0, 1, 2, \dots$. A program sends a sequence of requests. Each request asks for a block of $s$ words, with $1 \le s \le n$, or frees a live block. At every moment the live blocks total at most $M$ words. The [allocator](/allocator/) answers each request for a block at once with an interval $[p, p + s)$ that meets no live block, and it never moves a live block. The heap size of a run is the largest address used, plus one. Let $N(M, n)$ be the least $H$ such that some allocator serves every such sequence inside $[0, H)$. Let $N_2(M, n)$ be the same quantity when every requested size is a power of two.

**Theorem.**

1. **Exact value for powers of two** (Robson 1974). If $n$ is a power of two and $n$ divides $M$, then
$$N_2(M, n) = M\left(1 + \tfrac12 \log_2 n\right) - n + 1.$$
2. **General sizes** (Robson 1971 and 1974). $N(M, n) \ge N_2(M, n')$, where $n'$ is the largest power of two with $n' \le n$, so $N(M, n)$ is at least about $\tfrac12 M \log_2 n$. Robson 1974 also proves an upper bound. In the summary of Wilson et al., the worst case of a best possible strategy lies between about $0.5\, M \log_2 n$ and about $0.84\, M \log_2 n$.
3. **A simple upper bound.** If $n$ is a power of two and $n$ divides $M$, then $N_2(M, n) \le M(\log_2 n + 1)$ and $N(M, n) \le 2M(\log_2 n + 1)$.
4. **First fit and best fit** (Robson 1977). The worst case of address-ordered [first fit](/first-fit-allocation/) is about $M \log_2 n$, so it is $\Theta(M \log n)$. The worst case of [best fit](/best-fit-allocation/) is far worse, at about $M n$.

Part 1 is the exact answer; the lower bound in part 2 follows from it because a program may restrict itself to powers of two.

## In plain words

A program asks for blocks and gives them back in any order it likes. The allocator must put each new block somewhere free, and it may never slide a block that is in use. The question is how big the memory must be so that a request never fails, if the program never holds more than a fixed amount at once.

A spiteful program asks for many small blocks, gives back the ones that leave small gaps, then asks for bigger blocks that do not fit into those gaps. Each round, with a block size twice the last one, pushes the used memory up by about half the live amount. So the waste grows with the number of doublings. Robson proved that no allocator can avoid this, and that a careful allocator loses no more than a small multiple of it.

## Proof

We prove part 3 fully, and the lower bound for the case $n = 2$ fully. The general lower bound is a long argument; we give a proof sketch of its idea and point to the source.

**Part 3, the upper bound.** Let $n = 2^k$ and $n \mid M$. Give each size $2^j$, for $0 \le j \le k$, its own region $R_j = [jM, (j + 1)M)$, cut into $M / 2^j$ aligned slots of $2^j$ words. A request of size $2^j$ takes the first free slot of $R_j$. Suppose that the request arrives when $c_j$ blocks of size $2^j$ are live. The rules of the model give $(c_j + 1) 2^j \le M$, so $c_j < M / 2^j$, and at least one slot of $R_j$ is free. The heap never passes $(k + 1)M = M(\log_2 n + 1)$.

For general sizes $1 \le s \le n$, round each request up to the next power of two $2^j$, and give each region $2M$ words. For $j \ge 1$ a block of class $j$ has more than $2^{j-1}$ words, so when a request of class $j$ arrives, $(c_j + 1)(2^{j-1} + 1) \le M$, and $c_j + 1 < 2M / 2^j$, the number of slots in the region. For $j = 0$ the region has $2M \ge c_j + 1$ slots. So the heap never passes $2M(\log_2 n + 1)$.

**Lower bound for $n = 2$, when $4 \mid M$.** Then $N_2(M, 2) \ge \tfrac32 M - 1$, which is the value of part 1. The adversary works in two rounds.

1. It asks for $M$ blocks of one word. Let $E$ and $O$ be the number placed at even and at odd addresses. Let $c$ be the parity of the larger group, with $k_0 = \max(E, O) \ge M / 2$ blocks.
2. It frees all blocks at addresses of the other parity. If $k_0$ is odd, it frees one more block of parity $c$. Since $M/2$ is even, an odd $k_0 \ge M/2$ is at least $M/2 + 1$, so in every case $k$ blocks remain, with $k$ even and $k \ge M/2$.
3. It asks for $(M - k)/2$ blocks of two words. This is a whole number because $M$ and $k$ are both even, and it keeps the live total at $M$.

Every interval $[p, p + 2)$ holds exactly one address of parity $c$, and that address is not covered by a kept block or by another block of two words. So the heap holds at least $j = k + (M - k)/2 = (M + k)/2$ distinct addresses of parity $c$. The $j$-th address of parity $c$ is at least $2j - 2$, so the heap size is at least $2j - 1 = M + k - 1 \ge \tfrac32 M - 1$. This holds for every allocator, so $N_2(M, 2) \ge \tfrac32 M - 1$.

**General lower bound (proof sketch, not the full proof).** The argument above uses one doubling of the size. The adversary of Robson repeats the idea over the sizes $1, 2, 4, \dots, n$. Before it asks for blocks of size $2^i$, it picks a residue class of addresses modulo $2^i$ that the live blocks cover heavily, and it frees the blocks that miss that class. Every new block of size $2^i$ covers exactly one address of the class, and that address must be free. So the new blocks and the kept blocks need distinct members of one class, and these are $2^i$ apart. An averaging step shows that the kept blocks can be chosen so that each of the $\log_2 n$ rounds adds about $M/2$ words to the heap, which gives about $\tfrac12 M \log_2 n$. The exact accounting, which gives the term $-n + 1$, is in Robson 1974; this sketch does not reproduce it. Wilson et al., Section 4.1, summarize the results. $\blacksquare$

## Consequences

- [Online memory allocation](/online-memory-allocation/): no allocator that never moves blocks can promise a heap of $O(M)$ for all programs. The factor $\Theta(\log n)$ is the price of placing blocks without knowing the future.
- [Size classes](/size-classes/), [segregated free lists](/segregated-free-lists/) and the [buddy system](/buddy-system/) are within a constant factor of the best possible worst case, because they keep each size in its own space as in part 3.
- [First fit](/first-fit-allocation/) is also within a constant factor of the optimum in the worst case, by part 4. [Best fit](/best-fit-allocation/), which often does best on real programs, has a much worse worst case. This is a reason why worst-case results alone do not choose an allocator.
- To beat the bound, an allocator must move blocks. This is [memory compaction](/memory-compaction/), or the copying of a [garbage collector](/copying-collection/).
- In the offline setting, where all requests are known in advance, the ratio to the lower bound $M$ is a constant; see [offline dynamic storage allocation](/offline-dynamic-storage-allocation/).

## Tightness

Part 1 is exact. The table gives $N_2(M, n)$ from the formula, and the worst heap size that address-ordered first fit reaches on the same $M$ and $n$, over all request sequences. An exhaustive search of the safety game for $M \le 8$ gives the same values of $N_2$; the implementation contains that search.

| $M$ | $n$ | $N_2(M, n)$ | worst case of first fit |
|---|---|---|---|
| 4 | 2 | 5 | 6 |
| 6 | 2 | 8 | 9 |
| 8 | 2 | 11 | 12 |
| 4 | 4 | 5 | 6 |
| 8 | 4 | 13 | 16 |
| 8 | 8 | 13 | 16 |

**First fit forced above the optimum.** Take $M = 4$ and sizes $\{1, 2\}$. The table says that some allocator never needs more than 5 words. First fit can be forced to 6:

| Step | Request | First fit places at | Live blocks | Heap size |
|---|---|---|---|---|
| 1 | allocate 1 | 0 | [0,1) | 1 |
| 2 | allocate 1 | 1 | [0,1) [1,2) | 2 |
| 3 | allocate 1 | 2 | [0,1) [1,2) [2,3) | 3 |
| 4 | allocate 1 | 3 | [0,1) [1,2) [2,3) [3,4) | 4 |
| 5 | free [0,1) | | [1,2) [2,3) [3,4) | 4 |
| 6 | free [2,3) | | [1,2) [3,4) | 4 |
| 7 | allocate 2 | 4 | [1,2) [3,4) [4,6) | 6 |

At step 7 the two free words below address 4 are not adjacent, so the block of two words goes above them, and the live total is still 4. The upper bound of part 3 and the lower bound of part 1 differ by a factor of at most 2, so the order $\Theta(M \log n)$ is tight.

## History

Robson (1971) proved the first lower bound that grows with $\log n$ for every allocation strategy, in the Journal of the ACM. In 1974 he sharpened both bounds and solved the case of power-of-two sizes exactly. In 1977 he found the worst cases of first fit and best fit. Wilson, Johnstone, Neely and Boles (1995) review these results and stress that they are worst cases, which real programs seldom reach. SQLite uses the power-of-two formula to size its memsys5 allocator so that it cannot fail from fragmentation.

## References
