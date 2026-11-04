---
tag: FC1SBR
kind: model
slug: cache-oblivious-model
name: Cache-oblivious model
aliases:
- cache-oblivious analysis
- cache-oblivious model
- ideal cache model
area: foundations/models-of-computation
level: advanced
summary: External memory analysis without knowing cache or block parameters, via recursive divide-and-conquer layouts.
prereqs: [external-memory-model, memory-hierarchy, random-access-machine, asymptotic-notation]
see_also: [funnelsort, van-emde-boas-layout, cache-oblivious-b-tree, cache-oblivious-matrix-multiplication, cache-replacement-policy, locality-of-reference, red-blue-pebble-game, external-sorting-io-lower-bound]
sources:
  - paper: "Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, 40th Annual Symposium on Foundations of Computer Science (FOCS 1999)"
    locator: the ideal-cache model, the LRU simulation lemma, and the algorithms for matrix transposition, matrix multiplication and funnelsort
  - paper: "Harald Prokop, Cache-oblivious algorithms, Master's thesis, Massachusetts Institute of Technology (1999)"
    locator: the chapters on the model, on the tall-cache assumption and on funnelsort
  - paper: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985)"
    locator: the analysis of paging with a cache of size k against an optimal algorithm with a cache of size h
  - paper: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988), 1116 to 1127"
    locator: the sorting bound and the model with two levels
  - paper: "Gerth Stolting Brodal and Rolf Fagerberg, On the limits of cache-obliviousness, Proceedings of the 35th ACM Symposium on Theory of Computing (STOC 2003)"
    locator: abstract (the need for a tall cache)
  - paper: "Michael A. Bender, Erik D. Demaine and Martin Farach-Colton, Cache-oblivious B-trees, 41st Annual Symposium on Foundations of Computer Science (FOCS 2000)"
    locator: abstract (the dynamic search tree with O(log_B N) cost)
  - paper: "Jia-Wei Hong and H. T. Kung, I/O complexity: the red-blue pebble game, Proceedings of the 13th Annual ACM Symposium on Theory of Computing (STOC 1981)"
    locator: the red-blue pebble game and the I/O lower bound for matrix multiplication
  - paper: "Michael A. Bender, Gerth Stolting Brodal, Rolf Fagerberg, Dongdong Ge, Simai He, Haodong Hu, John Iacono and Alejandro Lopez-Ortiz, The cost of cache-oblivious searching, 44th Annual Symposium on Foundations of Computer Science (FOCS 2003)"
    locator: abstract (the lower bound of lg e times log_B N for cache-oblivious search)
---

The cache-oblivious model is the [external memory model](/external-memory-model/) with one change: the algorithm does not know the cache size $M$ or the block size $B$. The cache is ideal: it is fully associative and it replaces blocks by the optimal offline rule. Frigo, Leiserson, Prokop and Ramachandran defined it in 1999. An algorithm that is optimal in this model for all $M$ and $B$ is, under a mild regularity condition, within a constant factor of optimal on every level of an LRU [memory hierarchy](/memory-hierarchy/) at once, with no tuning.

## The machine

The machine has a processor and two levels of memory, as in the [external memory model](/external-memory-model/).

- The cache holds $M$ words, divided into $M/B$ lines of $B$ words each. The main memory is unbounded and is divided into blocks of $B$ words. A line holds one block.
- The processor works on words in the cache. A word that is not in the cache is a *cache miss*. A miss loads the block that holds the word into the cache. If the cache is full, the block of one line is written back to the main memory.
- The cache is *ideal*. It is fully associative: any block can go in any line. The replacement rule is optimal and offline: when a line must be freed, the cache evicts the block whose next use is farthest in the future.
- The program is an ordinary [random access machine](/random-access-machine/) program. It has no variable and no instruction that refers to $M$ or $B$. It cannot choose block sizes, and it cannot move blocks.

The analysis does depend on $M$ and $B$. A bound is a function of the input size $n$, $M$ and $B$, and it must hold for all $M$ and $B$, perhaps under the assumption below.

**The tall-cache assumption.** Many bounds need $M = \Omega(B^2)$. The cache then holds at least about $B$ lines, so it can hold a $B \times B$ square of items, each row in its own line. Some results use the weaker form $M = \Omega(B^{1+\varepsilon})$ for a constant $\varepsilon > 0$.

## What it counts

The model has two costs. The *work* $W(n)$ is the number of RAM operations, as in the [word RAM](/word-ram/). The *cache complexity* $Q(n; M, B)$ is the number of cache misses on an input of size $n$ in an ideal cache of $M$ words with lines of $B$ words. Both are worst-case bounds unless stated. The cost of a miss is 1, and the cost of a hit is 0 in $Q$.

**Why the ideal cache is a fair choice.** A real cache is not ideal. It is not fully associative, and it does not know the future. Two facts reduce the ideal cache to a real one.

First, least-recently-used (LRU) replacement is nearly as good as the optimal rule when it has a larger cache. Sleator and Tarjan (1985) proved the following for a cache of $k$ lines under LRU against an optimal algorithm with $h \le k$ lines. On every sequence of block requests, LRU makes at most $\frac{k}{k-h+1}$ times as many misses as the optimal algorithm, plus an additive term of at most $h$. The additive term comes from different initial contents of the two caches. When both caches start empty, the additive term is not needed. Take $k = 2h$. Then the factor is $\frac{2h}{h+1} < 2$, and with both caches empty at the start
$$Q_{\mathrm{LRU}}(n; M, B) \le 2\,Q_{\mathrm{OPT}}(n; M/2, B).$$
Frigo et al. state this lemma and use it to move the analysis from the optimal rule to LRU. They add the *regularity condition* $Q(n; M, B) = O(Q(n; 2M, B))$. Under it, halving the cache changes the number of misses by a constant factor only, and so LRU with cache $M$ is within a constant factor of the optimal rule with cache $M$. The bounds below satisfy this condition.

Second, the same argument applies to each level of a hierarchy. If an algorithm satisfies the regularity condition and is optimal in the two-level ideal-cache model for all $M$ and $B$, then it is optimal, up to a constant factor, on every level $(M_i, B_i)$ of a multilevel hierarchy of LRU caches with the inclusion property (Frigo et al.). This is the reason for the model: one analysis serves all levels, and the program needs no machine parameters.

**Full associativity.** The ideal cache hides the conflict misses of a direct-mapped or set-associative cache. The model is silent about them.

## Relation to other models

- **External memory model.** The [external memory model](/external-memory-model/) has the same two levels, but the algorithm knows $M$ and $B$ and it decides which blocks to move. A cache-oblivious algorithm is an external memory algorithm that works for all $M$ and $B$ at once. So a cache-oblivious bound is at least as large as the best external memory bound, and one asks when it is equal to it. For scanning, searching, transposing and sorting (below) it is equal, up to constant factors.
- **RAM and word RAM.** With $B = 1$ and $M = \infty$ the cache complexity is the number of distinct words that the program touches, and the work is the running time of the [random access machine](/random-access-machine/). The model refines the RAM cost with a locality cost.
- **Red-blue pebble game.** The [red-blue pebble game](/red-blue-pebble-game/) of Hong and Kung (1981) is the model with $B = 1$ and an offline schedule that the algorithm chooses. It gives lower bounds on the number of transfers that hold for every schedule.
- **Online paging.** The cache replacement is a [paging problem](/paging-problem/). The cache-oblivious model gives the optimal offline rule to the cache. The LRU lemma is its link to the online setting.

## Known results in the model

Here $N$ and $n$ are the sizes of the input in words, and all results are worst-case bounds on cache misses. Each result states what it needs from the cache.

**Scanning.** A contiguous array of $n$ words occupies at most $\lceil n/B \rceil + 1$ blocks. A scan that reads it from left to right incurs at most $\lceil n/B \rceil + 1$ misses, whatever $M$ and $B$ are. Proof: the array starts at some word $s$ and ends at word $s + n - 1$. It meets the blocks with numbers $\lfloor s/B \rfloor$ to $\lfloor (s+n-1)/B \rfloor$. The number of these blocks is $c = \lfloor (s+n-1)/B \rfloor - \lfloor s/B \rfloor + 1$. Because $\lfloor s/B \rfloor > (s - B)/B$ and $\lfloor (s+n-1)/B \rfloor \le (s+n-1)/B$, we get $c < (n-1)/B + 2 \le n/B + 2$. An integer $c$ with $c < n/B + 2$ satisfies $c \le \lceil n/B \rceil + 1$. A scan loads each block once and keeps the current block until it is done, which needs one line.

**Search: the van Emde Boas layout.** Let $T$ be a complete binary search tree with $N = 2^h - 1$ keys and $h$ levels. A node takes one word. (A constant number of words per node changes only the constants.) The layout $\mathrm{vEB}(T)$ is recursive. If $h = 1$, the layout is the one node. Otherwise cut $T$ between level $\lfloor h/2 \rfloor$ and level $\lfloor h/2 \rfloor + 1$. This gives a top tree with $\lfloor h/2 \rfloor$ levels and $2^{\lfloor h/2 \rfloor}$ bottom trees with $\lceil h/2 \rceil$ levels. Store the layout of the top tree, then the layouts of the bottom trees from left to right. Each recursive subtree is then stored in a contiguous range of words. The layout is built without $B$. See [van Emde Boas layout](/van-emde-boas-layout/).

A search follows one root-to-leaf path. It makes $O(\log_B N)$ misses with this layout, whatever $B$ is, if the cache holds at least two lines. Here is the proof. Let $k = \lfloor \lg(B+1) \rfloor$, so that $2^k - 1 \le B$. Cut the recursion into *pieces*: split a subtree only if it has more than $k$ levels. The pieces are the subtrees of at most $k$ levels that are not split. If $h \le k$, the whole tree is one piece. Else each piece comes from the split of a subtree with $h_0 \ge k+1$ levels, so it has at least $\lfloor h_0/2 \rfloor \ge \lfloor (k+1)/2 \rfloor$ levels. A piece has at most $2^k - 1 \le B$ words and is contiguous, so it meets at most 2 blocks. A root-to-leaf path enters a piece at its root and leaves it at its bottom level, so the numbers of levels of the pieces on the path add up to $h$. The path meets at most $h / \lfloor (k+1)/2 \rfloor$ pieces. Each piece causes at most 2 misses, if the cache keeps the blocks of the current piece (two lines are enough). Now $k > \lg(B+1) - 1$ and $k \ge 1$, so $k \ge \lg(B+1)/2$ (if $\lg(B+1) \le 2$ then $k \ge 1 \ge \lg(B+1)/2$, else $k > \lg(B+1) - 1 \ge \lg(B+1)/2$). Also $\lfloor (k+1)/2 \rfloor \ge k/2$. So $\lfloor (k+1)/2 \rfloor \ge \lg(B+1)/4$, and with $h = \lg(N+1)$ the number of misses is at most $\max\{2,\ 8 \lg(N+1)/\lg(B+1)\} = O(\log_B N)$.

This matches the bound of the [B-tree](/b-tree/), $\Theta(\log_B N)$, which needs $B$. It is a factor of about $\lg B$ better than [binary search](/binary-search/) on a sorted array, which costs $\Theta(\log_2 (N/B))$ misses. Example: $N = 2^{16} - 1$ keys, $B = 16$ words, and the tree starts at a block boundary. The worst root-to-leaf path meets 7 blocks in the van Emde Boas layout, and 13 blocks in the sorted (in-order) layout and in the breadth-first layout. For other alignments of the start, the van Emde Boas layout meets at most 8 blocks. Bender, Demaine and Farach-Colton (2000) built a dynamic search tree on this idea, with $O(\log_B N)$ misses per search in the worst case. An update costs $O(\log_B N + (\log^2 N)/B)$ amortized misses in the basic structure, and $O(\log_B N)$ amortized misses with one more level of indirection (see [cache-oblivious B-tree](/cache-oblivious-b-tree/)).

**Recursive matrix transposition.** Let $A$ be an $n \times n$ matrix in row-major order, and let $A^T$ be written to a second array in row-major order. The row-by-row method reads $A$ in rows and writes $A^T$ in columns. The words of one column of $A^T$ are $n$ words apart. If $n \ge B$ and $n > M/B$, an LRU cache misses on every write, because the $n$ blocks of one column leave the cache before the next column needs them, so the method makes at least $n^2$ misses. The recursive method transposes a submatrix by halving its larger dimension and transposing the two halves. A submatrix with one word is copied.

Claim: if $n$ is a power of 2 and $M \ge 4B^2$, the recursive method makes $O(1 + n^2/B)$ misses in an LRU cache of $M$ words, and so in an ideal cache. Proof. Let $t$ be the largest power of 2 with $t \le B$. Then $t > B/2$. Suppose first that $n < t$. Both matrices have fewer than $B^2$ words, so both fit in the cache. The scanning bound gives at most $2(\lceil n^2/B \rceil + 1)$ misses. Suppose now that $n \ge t$. Stop the recursion at the first submatrix whose larger dimension is at most $t$. Halving the larger dimension of a square $2t \times 2t$ submatrix gives a $t \times 2t$ or $2t \times t$ rectangle, and halving its larger dimension gives a $t \times t$ square. The shapes alternate between squares and rectangles of ratio 2, so each such *base piece* has size $t \times t$. Let a base piece have $a$ rows and $b$ columns. It reads $a$ rows of $b$ contiguous words of $A$, and writes $b$ rows of $a$ contiguous words of $A^T$. Each row of at most $t \le B$ words meets at most 2 blocks, so the piece meets at most $2a + 2b \le 4t \le 4B$ blocks. The cache has $M/B \ge 4B$ lines. So all blocks of the piece stay in the LRU cache while the piece is processed, and each block is loaded at most once. The cost of a piece is at most $2a+2b = 4t$. There are $n^2/t^2$ pieces, so the total is at most $4n^2/t < 8 n^2/B$. $\square$

The general case of an $m \times n$ matrix has the same bound, $O(1 + mn/B)$, under the tall-cache assumption (Frigo et al.). A proof for it is not given here.

**Sorting: funnelsort.** For $n$ items, with $M = \Omega(B^2)$,
$$Q(n; M, B) = O\!\left(1 + \frac{n}{B}\left(1 + \log_M n\right)\right),$$
and the work is $O(n \log n)$. The algorithm is [funnelsort](/funnelsort/). It splits the input into $n^{1/3}$ contiguous parts of size $n^{2/3}$, sorts each part recursively, and merges the sorted parts with an $n^{1/3}$-*funnel*. A $k$-funnel is a recursive structure that merges $k$ sorted sequences of total length $k^3$. It uses $O(k^2)$ space, laid out in the van Emde Boas style, with buffers between its parts. With a tall cache it makes $O\big(1 + k + \frac{k^3}{B}(1 + \log_M k)\big)$ misses to merge $k^3$ items (Frigo et al.). Then the cache complexity satisfies
$$Q(n) \le n^{1/3}\, Q(n^{2/3}) + O\!\left(1 + n^{1/3} + \frac{n}{B} + \frac{n}{B}\log_M n\right),$$
with $Q(n) = O(1 + n/B)$ when $n \le \alpha M$ for a small constant $\alpha$, because the problem then fits in the cache. The merge term $n^{1/3}$ is at most $n/B$ for $n \ge B^{3/2}$, and the recursion stops at size about $\alpha M$, which is at least $B^{3/2}$ when $M = \Omega(B^2)$ and $B$ is large enough. At every recursive level the subproblem size $n_i$ is larger than $\alpha M$, so $\log_M n_i = \Omega(1)$, and the per-level term $O(n/B)$ is $O(\frac{n}{B}\log_M n_i)$. The sizes at the successive levels are $n^{(2/3)^i}$, so their logarithms form a geometric series with ratio $2/3$. The sum of the terms $\frac{n}{B}\log_M n_i$ over all levels is $O(\frac{n}{B}\log_M n)$, and the base case adds $O(n/B)$. This gives the bound above. With a tall cache, $\log_{M/B}(n/B) = \Theta(\log_M n)$ when $n \ge M$, so the bound equals the optimum $\Theta\big(\frac{n}{B}\log_{M/B}\frac{n}{B}\big)$ of the external memory model (see [external sorting I/O lower bound](/external-sorting-io-lower-bound/) and [external merge sort](/external-merge-sort/)). Brodal and Fagerberg (2003) showed that an assumption of this kind is needed: no cache-oblivious comparison-based sorting algorithm reaches the optimal I/O bound for all $M$ and $B$ without a tall-cache assumption. They show the same for permuting.

**Matrix multiplication.** The recursive algorithm that splits each matrix into four quadrants and does 8 recursive products multiplies two $n \times n$ matrices with $O(1 + n^2/B + n^3/(B\sqrt{M}))$ misses when $M = \Omega(B^2)$ (Frigo et al.), which matches the lower bound of the [red-blue pebble game](/red-blue-pebble-game/) for this method. See [cache-oblivious matrix multiplication](/cache-oblivious-matrix-multiplication/).

**Limits of the model.** Cache-obliviousness costs a constant factor in some problems and needs an assumption in others. Bender, Brodal, Fagerberg, Ge, He, Hu, Iacono and Lopez-Ortiz (2003) proved that no cache-oblivious search structure can guarantee fewer than $\lg e \cdot \log_B N \approx 1.443 \log_B N$ block transfers between some two levels of the hierarchy, while a [B-tree](/b-tree/) tuned to $B$ needs about $\log_B N$. For comparison-based sorting and for permuting, the result of Brodal and Fagerberg above shows that the tall-cache assumption cannot be dropped.

## References
