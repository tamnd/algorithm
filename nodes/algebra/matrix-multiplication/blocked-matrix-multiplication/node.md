---
tag: 4VVM7H
kind: algorithm
slug: blocked-matrix-multiplication
name: Blocked matrix multiplication
aliases:
- tiled matrix multiplication
- cache-aware matrix multiplication
- loop tiling for matrix multiplication
area: algebra/matrix-multiplication
level: advanced
summary: Runs the triple loop on square tiles sized so that three tiles fit in fast memory, which cuts the block transfers from about n^3/B to O(n^3/(B sqrt(M)) + n^2/B).
model: external-memory-model
complexity:
  vars: {n: the order of the matrices, M: the fast memory size in words, B: the block (cache line) size in words, b: the tile side (Θ(sqrt(M)) for the I/O bound with M ≥ 9B^2)}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(b^2)}
  io:
    worst: "O(n^3/(B sqrt(M)) + n^2/B)"
    average: "O(n^3/(B sqrt(M)) + n^2/B)"
    best: "O(n^3/(B sqrt(M)) + n^2/B)"
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [naive-matrix-multiplication, external-memory-model]
see_also: [cache-oblivious-matrix-multiplication, red-blue-pebble-game, pebbling-lower-bound, memory-hierarchy, cannons-algorithm, shared-memory-tiling, roofline-model, arithmetic-intensity]
sources:
  - paper: doi:10.1145/800076.802486
    title: Jia-Wei Hong and H. T. Kung, I/O complexity, the red-blue pebble game, Proceedings of the 13th Annual ACM Symposium on Theory of Computing (STOC 1981)
    locator: pp. 326 to 333 (the lower bound Ω(n^3/sqrt(S)) for the conventional product and the blocked schedule that meets it)
  - paper: "Dror Irony, Sivan Toledo and Alexander Tiskin, Communication lower bounds for distributed-memory matrix multiplication, Journal of Parallel and Distributed Computing 64(9), 2004"
    locator: pp. 1017 to 1026 (the Loomis and Whitney argument and explicit constants for the sequential and parallel cases)
  - paper: "Monica S. Lam, Edward E. Rothberg and Michael E. Wolf, The cache performance and optimizations of blocked algorithms, Proceedings of ASPLOS IV, 1991"
    locator: pp. 63 to 74 (self-interference misses and the choice of the tile size in real caches)
  - paper: doi:10.1145/1356052.1356053
    title: Kazushige Goto and Robert A. van de Geijn, Anatomy of high-performance matrix multiplication, ACM Transactions on Mathematical Software 34(3), 2008
    locator: Article 12 (the layered blocking for registers, L1, L2 and the TLB, and the packing of tiles)
  - paper: "A. C. McKellar and E. G. Coffman, Organizing matrices and matrix operations for paged memory systems, Communications of the ACM 12(3), 1969"
    locator: pp. 153 to 165 (storage by submatrices and the page fault counts of the blocked product)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition
    locator: Section 1.3, Block matrices and algorithms, and Section 1.5, Vectorization and locality
---

Blocked matrix multiplication runs the [triple loop](/naive-matrix-multiplication/) on square tiles of side $b$ instead of single entries. For each tile of $C$ it loads the tile, adds into it the products of the matching tiles of $A$ and $B$ one pair at a time, and writes it back. If three tiles fit in the fast memory, each entry brought in is used $b$ times before it leaves. In the [external memory model](/external-memory-model/) with a fast memory of $M$ words and blocks of $B$ words, the choice $b = \Theta(\sqrt M)$ gives $O(n^3/(B\sqrt M) + n^2/B)$ block transfers, against about $n^3/B$ for the plain loop. By the bound of Hong and Kung this is optimal, up to a constant, for every schedule of the $n^3$ products. It does the same $n^3$ multiplications as the triple loop and is the basis of every fast BLAS library.

## In plain words

A computer has a small fast memory and a large slow one. Moving data between them costs much more than arithmetic. The school method for multiplying two large tables walks over a whole table for each row of the answer, so it pulls almost every number from slow memory again and again.

The blocked method cuts the tables into small square tiles. It keeps one tile of the answer and one tile of each input in fast memory, and does all the work these three tiles allow before it moves on. A tile of side $b$ holds $b^2$ numbers but takes part in $b^3$ multiplications, so each number brought in is used $b$ times. Bigger tiles mean less traffic, up to the point where three tiles no longer fit.

## The problem

The input is an $n \times m$ matrix $A$ and an $m \times p$ matrix $B$ over a ring $R$, and the output is $C = AB$. The arithmetic is that of the triple loop, so $R$ need not be commutative, and no subtraction is needed: the method works over semirings too. For the bounds take $n = m = p$.

The cost model is the [external memory model](/external-memory-model/). The matrices are in slow memory in [row-major order](/row-major-order/). Slow memory is split into blocks of $B$ consecutive words. A fast memory holds $M$ words, and arithmetic is done only on words in fast memory. One I/O moves one block between the two. The cost is the number of I/Os. The time, counted in ring operations, is the same $\Theta(n^3)$ as for the triple loop. Cache hardware is close to this model, with the cache size as $M$ and the line size as $B$, except that it decides by itself what to evict.

## The algorithm

```pseudo id=main
BLOCKED-MULTIPLY(A, B, b)               ▷ A is n × m, B is m × p, tile side b
L1  for i0 ← 0 to n − 1 step b do
L2      for j0 ← 0 to p − 1 step b do
L3          load the tile T_C ← C[i0 .. i0+b−1, j0 .. j0+b−1] (zero at the start)
L4          for k0 ← 0 to m − 1 step b do
L5              load the tiles T_A ← A[i0 .. i0+b−1, k0 .. k0+b−1] and T_B ← B[k0 .. k0+b−1, j0 .. j0+b−1]
L6              T_C ← T_C + T_A · T_B by the triple loop inside fast memory
L7          store T_C back to C
```

Index ranges are cut at the edges, so the last tiles in each direction can be smaller. Lines L1, L2 and L4 walk over the tiles. Line L3 brings one tile of $C$ into fast memory, and it stays there for the whole $k_0$ loop. Line L5 brings one tile of $A$ and one of $B$, and line L6 does all $b^3$ products between them. Line L7 writes the finished tile. At any time fast memory holds three tiles, $3b^2$ words.

The tile side is chosen from the machine: the largest $b$ with $3b^2 \le M$ when the tiles are aligned with the blocks, and $b = \lfloor \sqrt{M}/3 \rfloor$ in general (see Complexity). This is why the method is called cache-aware.

## Example

Take $n = 4$, $b = 2$, so each matrix is a $2 \times 2$ grid of tiles $A_{IK}$, $B_{KJ}$, $C_{IJ}$, and blocks of $B = 2$ words, so each tile row is one block and each tile is two blocks. The loops run in this order:

| $C$ tile | tile products at L6 | I/Os |
|---|---|---|
| $C_{11}$ | $A_{11}B_{11}$, then $A_{12}B_{21}$ | $2 + 4 + 4 + 2 = 12$ |
| $C_{12}$ | $A_{11}B_{12}$, then $A_{12}B_{22}$ | $12$ |
| $C_{21}$ | $A_{21}B_{11}$, then $A_{22}B_{21}$ | $12$ |
| $C_{22}$ | $A_{21}B_{12}$, then $A_{22}B_{22}$ | $12$ |

For each $C$ tile: 2 blocks to load it, 4 blocks for each of the two pairs of $A$ and $B$ tiles, and 2 blocks to store it. The total is $48 = 2n^3/(bB) + 2n^2/B = 32 + 16$, and fast memory needs $3b^2 = 12$ words.

At a realistic size the effect is large. Take $n = 4096$, $M = 32768$ words (256 KiB of 8-byte numbers) and $B = 8$ words (a 64-byte line). The tile side $b = 64$ divides $n$, is a multiple of $B$, and has $3b^2 = 12288 \le M$. The blocked schedule makes
$$\frac{2n^3}{bB} + \frac{2n^2}{B} = 268\,435\,456 + 4\,194\,304 = 272\,629\,760$$
I/Os. The plain loop in the order $i, k, j$ under LRU replacement misses on every block of $B$ at each use, since $B$ has $n^2 = 2^{24}$ words and does not fit: that is at least $n \cdot n^2/B = 2^{33} \approx 8.6 \times 10^9$ misses, more than 31 times as many. The lower bound in the [red-blue pebble game](/red-blue-pebble-game/), $n^3/(4\sqrt{2M}) - M$ words, gives at least $8\,384\,512$ I/Os; the gap of about 32 to the blocked count is the weak constant of that bound, not slack in the schedule.

A simulation of a fully associative LRU cache, in the implementation, gives observed counts for a smaller case, $n = 64$, $M = 768$, $B = 8$: the tiled order with $b = 16$ makes $6000$ misses (the explicit schedule makes $5120$ I/Os), and the order $i, k, j$ makes $33\,792$.

## Correctness

The tiles split the index ranges $\{0, \ldots, n-1\}$, $\{0, \ldots, m-1\}$ and $\{0, \ldots, p-1\}$ into disjoint intervals. Each triple $(i, j, k)$ lies in exactly one triple of intervals, so line L6 adds the product $a_{ik} b_{kj}$ into $c_{ij}$ exactly once, and nothing else is added to $c_{ij}$. So $C = AB$ at the end. Commutativity is never used: each product keeps $a$ on the left.

More is true. For fixed $(i, j)$ the tiles of $k$ are visited in increasing order at line L4, and the triple loop inside line L6 visits $k$ in increasing order inside a tile. So $c_{ij}$ receives $a_{i0} b_{0j}, a_{i1} b_{1j}, \ldots$ in the same order as in the plain triple loop. In floating point the blocked result is therefore the same, bit for bit, as the plain loop with the same inner order. The proofs section gives the details and the I/O count.

## Complexity

- **Arithmetic.** Exactly $nmp$ multiplications and $nmp$ additions (into a zero tile), the same as the triple loop: $\Theta(n^3)$.
- **I/O, aligned case.** If $b$ divides $n$ and $B$ divides $b$, every tile is $b^2/B$ blocks. There are $(n/b)^2$ tiles of $C$, each loaded and stored once, and $(n/b)^3$ pairs of tiles of $A$ and $B$, each loaded once. So the count is exactly $2n^3/(bB) + 2n^2/B$. With $3b^2 \le M$ and $b$ close to $\sqrt{M/3}$, this is $2\sqrt 3\, n^3/(B \sqrt M) + 2n^2/B$ to leading order.
- **I/O, general case.** A row of a tile is $b$ consecutive words and touches at most $\lceil b/B \rceil + 1$ blocks. If $b \ge B$, a tile touches at most $3b^2/B$ blocks and takes at most $3b^2$ words of fast memory, so $9b^2 \le M$ suffices. With $b = \lfloor \sqrt M / 3 \rfloor$ and $M \ge 9B^2$ (a tall cache), the count is $O(n^3/(B\sqrt M) + n^2/B)$.
- **Lower bound.** Every schedule that computes the $n^3$ products $a_{ik} b_{kj}$ and sums them moves $\Omega(n^3/\sqrt M)$ words between the memories (Hong and Kung, 1981; the proof is on the [red-blue pebble game](/red-blue-pebble-game/) page). One I/O moves at most $B$ words, so it makes $\Omega(n^3/(B\sqrt M))$ I/Os, and reading the input takes $\Omega(n^2/B)$. So the blocked schedule is optimal up to a constant factor. The bound does not apply to [Strassen's algorithm](/strassen-algorithm/), which computes other products.
- **Space.** Three tiles, $3b^2 = O(M)$ words of fast memory.

The I/O counts above are proved in the model. The speedups on real machines are observed and depend on the cache associativity, the TLB, prefetching and vector units, see Pitfalls.

## Properties

- **Same arithmetic as the triple loop.** Same operations, same summation order for each entry, so it inherits the numerical behaviour of the classical product, including its componentwise error bound.
- **Cache-aware.** The tile side depends on $M$ (and on $B$ for alignment). With several levels of cache one needs one level of tiling for each, see Variants.
- **Works over semirings.** No subtraction is used, so Boolean and min-plus products tile the same way.
- **Embarrassingly parallel over $C$ tiles.** The $(i_0, j_0)$ iterations are independent.

## Variants and improvements

- **Loop order inside and outside.** Any of the six orders of the three tile loops is correct. Putting $k_0$ innermost, as here, keeps one $C$ tile resident; other orders keep an $A$ or a $B$ tile resident and write $C$ more often.
- **Rectangular tiles.** Tiles of $b_1 \times b_2$ for $A$ and $b_2 \times b_3$ for $B$, chosen with $b_1 b_2 + b_2 b_3 + b_1 b_3 \le M$, let a library fit tiles to registers and to cache lines.
- **Multiple levels.** Tiling for registers, L1, L2, L3 and the TLB, with the tiles of $A$ and $B$ copied (packed) into contiguous buffers, is the design of GotoBLAS and BLIS (Goto and van de Geijn, 2008). Packing removes conflict misses and TLB misses.
- **Cache-oblivious recursion.** Halving the largest dimension recursively reaches every tile size at once and gives the same bound for every $M$ and $B$ without knowing them, see [cache-oblivious matrix multiplication](/cache-oblivious-matrix-multiplication/).
- **GPUs.** Tiles of $A$ and $B$ are staged in the shared memory of a thread block, see [shared memory tiling](/shared-memory-tiling/). The tile side sets the [arithmetic intensity](/arithmetic-intensity/), about $b/8$ floating point operations per byte for 8-byte words, which decides the position on the [roofline](/roofline-model/).
- **Distributed memory.** Assigning tiles to processors on a grid and moving them gives [Cannon's algorithm](/cannons-algorithm/) and SUMMA.
- **Constants.** Smith, Lowery, Langou and van de Geijn (2017) sharpened the lower bound to about $2n^3/\sqrt M$ words, and a schedule that keeps a $\sqrt M \times \sqrt M$ tile of $C$ and streams rows and columns comes close to it (arXiv 1702.02017; not checked here).

## When to use it

Use it whenever the matrices do not fit in cache and a classical product is wanted, which in practice means always: a library DGEMM or SGEMM is a blocked product with tuned tiles. Write one yourself only when no BLAS is available, for a semiring product that BLAS does not offer, or for learning. When $M$ and $B$ are unknown or the code must run well on many machines, the cache-oblivious version is simpler to tune. For sizes that fit in L1 cache, blocking gives nothing.

## Pitfalls

- **Tiles of exactly the cache size.** Real caches are set-associative. Three tiles that in total fit $M$ can still map to the same sets and evict each other. Lam, Rothberg and Wolf (1991) observed that the best tile is often much smaller than $\sqrt{M/3}$ and depends on $n$; copying tiles into contiguous buffers avoids this.
- **Leading dimensions that are powers of two.** With $n = 4096$, the rows of a tile are $4096$ words apart and fall into the same cache sets. Pad the rows or pack the tiles.
- **Forgetting the edge tiles.** When $b$ does not divide $n$, the last tiles are smaller; indexing past the end reads garbage or crashes.
- **Assuming the lower bound covers every algorithm.** The $\Omega(n^3/\sqrt M)$ bound holds for computing all $n^3$ products. Strassen's algorithm and other fast methods move fewer words for large $n$.
- **Tiny tiles.** A tile side below $B$ wastes most of each block; the count then behaves like $n^3/b$ instead of $n^3/(bB)$.

## Implementations

## History

Blocking is older than its theory: McKellar and Coffman (1969) studied storing and multiplying matrices by square submatrices to reduce page faults in paged virtual memory. Hong and Kung (1981) gave the first proof, in the red-blue pebble game, that the blocked schedule moves an optimal $\Theta(n^3/\sqrt M)$ words. Level 3 BLAS (1990) made blocked matrix products the standard interface for dense linear algebra, and LAPACK built on it. Lam, Rothberg and Wolf (1991) studied the gap between the model and real caches. Irony, Toledo and Tiskin (2004) gave explicit constants and the parallel version of the lower bound. Goto and van de Geijn (2008) described the layered blocking used in today's high performance libraries.

## References
