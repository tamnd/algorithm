---
title: P-TRANSPOSE has work n^2 + n - 1, span 2 lg n + 1, which is optimal up to an additive constant, and n^2/B cache misses
proves: [time.worst, depth.worst, io.worst]
status: full
---

**The cost model.** A swap, or a call that returns at once, costs 1. A group of $k$ tasks run in parallel adds $k - 1$ to the work and $\lceil \lg k \rceil$ to the span: the group is a balanced binary tree of forks. So the group of three calls in P-TRANSPOSE adds 2 to both the work and the span, and the group of four calls in P-SWAP-T adds 3 to the work and 2 to the span. Let $n = 2^L$, and $\lg = \log_2$.

**Lemma 1 (P-SWAP-T).** On two $n \times n$ blocks, P-SWAP-T has work $W_s(n) = 2n^2 - 1$ and span $S_s(n) = 2L + 1$.

*Proof.* $W_s(1) = S_s(1) = 1$, and for $n \ge 2$, $W_s(n) = 4W_s(n/2) + 3$ and $S_s(n) = S_s(n/2) + 2$. Then $4(2n^2/4 - 1) + 3 = 2n^2 - 1$, and $2(L - 1) + 1 + 2 = 2L + 1$. $\blacksquare$

**Theorem 2 (work and span).** P-TRANSPOSE on an $n \times n$ matrix has work $W(n) = n^2 + n - 1$ and span $S(n) = 2L + 1$. It does exactly $n(n-1)/2$ swaps. So $W = \Theta(n^2)$ and $S = \Theta(\log n)$.

*Proof.* $W(1) = S(1) = 1$. For $n \ge 2$, by Lemma 1,

$$W(n) = 2W(n/2) + W_s(n/2) + 2 = 2W(n/2) + n^2/2 + 1, \qquad S(n) = 2 + \max\{S(n/2), S_s(n/2)\}.$$

For the work, $2\big((n/2)^2 + n/2 - 1\big) + n^2/2 + 1 = n^2 + n - 1$. For the span, $S(n/2) = 2(L - 1) + 1$ by induction and $S_s(n/2) = 2(L - 1) + 1$ by Lemma 1, so $S(n) = 2 + 2L - 1 = 2L + 1$. The number of swaps $C(n)$ satisfies $C(1) = 0$ and $C(n) = 2C(n/2) + (n/2)^2$, and $2 \cdot \tfrac{n}{2}(\tfrac{n}{2} - 1)/2 + n^2/4 = n(n - 1)/2$. $\blacksquare$

**Theorem 3 (any n).** The variant for any $n \ge 1$ has work exactly $n^2 + n - 1$ and span at most $2\lceil \lg n \rceil + 1$.

*Proof.* The swap of a $p \times q$ block with a $q \times p$ block halves the longer side, so its calls form a binary tree with $pq$ leaves (one swap each) and $pq - 1$ forks: work $2pq - 1$. Each fork halves one side, rounding up, and $\lceil \lg \lceil m/2 \rceil \rceil = \lceil \lg m \rceil - 1$ for $m \ge 2$, so a chain has at most $\lceil \lg p \rceil + \lceil \lg q \rceil$ forks, and the span is at most $\lceil \lg p \rceil + \lceil \lg q \rceil + 1$. Let $a = \lfloor n/2 \rfloor$ and $b = \lceil n/2 \rceil$. For $n \ge 2$, $W(n) = W(a) + W(b) + (2ab - 1) + 2$, and by induction this is $a^2 + a - 1 + b^2 + b - 1 + 2ab + 1 = n^2 + n - 1$, with $W(1) = 1$. For the span, $\lceil \lg a \rceil \le \lceil \lg b \rceil = \lceil \lg n \rceil - 1$, so the swap has span at most $2\lceil \lg n \rceil - 1$, both recursive calls have span at most $2(\lceil \lg n \rceil - 1) + 1$ by induction, and the group of three adds 2. $\blacksquare$

**Theorem 4 (the span is optimal).** In this cost model, any fork-join computation with binary forks that does $m$ swaps has span at least $\lg(m + 1)$. So every such transpose of an $n \times n$ matrix that swaps each off-diagonal pair has span at least $\lg(n(n-1)/2 + 1) \ge 2L - 1$ for $n = 2^L \ge 2$, and P-TRANSPOSE is within 2 of it.

*Proof.* Model the run as a DAG of unit nodes with one start node, in which each node has at most two successors (a fork has two, a join or a step one). Give each node its depth, the number of nodes on a longest path from the start to it, minus 1. A node of depth $d \ge 1$ has a predecessor of depth $d - 1$ (the one before it on a longest path), and each node is that predecessor for at most two nodes. So there are at most $2^d$ nodes of depth $d$, and a DAG with span $S$ has at most $2^0 + \cdots + 2^{S-1} = 2^S - 1$ nodes. Each swap is one node, so $m \le 2^S - 1$. For $n = 2^L \ge 2$, $n(n - 1)/2 + 1 > n^2/4 = 2^{2L - 2}$, so $S > 2L - 2$. $\blacksquare$

**Theorem 5 (cache misses).** Let $A$ be stored by rows starting at the start of a cache line, with lines of $B$ words, where $B \ge 2$ and $n \ge B$ are powers of 2. Run P-TRANSPOSE on one processor with a fully associative LRU cache of at least $2B$ lines, so of at least $M = 2B^2$ words. Then the run has exactly $n^2/B$ cache misses, which is the least number possible.

*Proof.* Every call of size $B$ is either a P-TRANSPOSE call on a $B \times B$ block on the diagonal or a P-SWAP-T call on two $B \times B$ blocks. All block offsets in the recursion are multiples of the block size, so each of these blocks starts at a multiple of $B$ in its rows, and each of its $B$ rows is a whole cache line. The calls above size $B$ touch no cell themselves, and every cell that is touched is touched inside one call of size $B$. These calls touch disjoint sets of $B \times B$ blocks, and there are $n/B$ diagonal blocks and $\tfrac12 (n/B)(n/B - 1)$ pairs of other blocks.

A call of size $B$ touches at most $2B$ lines. In an LRU cache with at least $2B$ lines, a line is evicted only after at least $2B$ other lines have been used since its last use, so inside the call each line is loaded at most once. The lines of different calls are different, so the total is at most $(n/B) \cdot B + \tfrac12 (n/B)(n/B - 1) \cdot 2B = n + n^2/B - n = n^2/B$. Each line of the matrix holds a cell off the diagonal, since $B \ge 2$, and that cell is swapped, so each of the $n^2/B$ lines must be loaded at least once. $\blacksquare$

**Remark.** The plain loop that swaps $a_{ij}$ with $a_{ji}$ for $j > i$ walks down a column for each $i$. When the cache holds fewer than $n$ lines, a line of that column is evicted before the next row needs it. The tests count 9103 misses for this loop for $n = 128$, $B = 8$ and 16 lines, against $n^2/B = 2048$ for P-TRANSPOSE.
