---
tag: FMPTMB
kind: technique
slug: loop-tiling
name: Loop tiling
aliases:
- loop blocking
- cache blocking
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Splits the iteration space of a nest into blocks that fit in cache and runs each block fully, for data reuse and parallelism.
prereqs: [strip-mining, loop-interchange, loop-transformation-legality]
see_also: [loop-skewing, blocked-matrix-multiplication, cache-oblivious-matrix-multiplication, shared-memory-tiling, wolf-lam-locality-algorithm, pluto-algorithm, memory-hierarchy, wavefront-parallelism]
sources:
  - paper: doi:10.1145/73560.73588
    title: François Irigoin and Rémi Triolet, Supernode partitioning, Proceedings of the 15th ACM Symposium on Principles of Programming Languages (POPL), 1988, 319-329
    locator: the partition of the iteration space into tiles (supernodes) by hyperplanes, and the condition that no dependence goes from a later tile back to an earlier one
  - paper: doi:10.1145/76263.76337
    title: Michael Wolfe, More iteration space tiling, Proceedings of Supercomputing '89, ACM, 1989, 655-664
    locator: tiling as strip mining plus interchange, its legality, and skewing before tiling
  - paper: doi:10.1145/106972.106981
    title: Monica S. Lam, Edward E. Rothberg and Michael E. Wolf, The cache performance and optimizations of blocked algorithms, Proceedings of ASPLOS IV, 1991, 63-74
    locator: the measured cache behavior of blocked matrix multiplication, self-interference misses in caches of low associativity, and the choice of the block size
  - paper: doi:10.1145/113445.113449
    title: Michael E. Wolf and Monica S. Lam, A data locality optimizing algorithm, Proceedings of the ACM SIGPLAN '91 Conference on Programming Language Design and Implementation (PLDI), 1991, 30-44
    locator: fully permutable loop nests as the loops that can be tiled, and the choice of the loops to tile
---

Loop tiling replaces a nest of loops by a nest that runs the iteration space block by block. Each block, a *tile*, is a small rectangle of iterations, and the program finishes one tile before it starts the next. The construction is [strip mining](/strip-mining/) of each loop of a band, followed by [interchange](/loop-interchange/) that moves the strip loops outward. Tiling is legal on a *fully permutable band*: a set of adjacent loops in which every dependence that the outer loops do not carry has a nonnegative distance on every loop of the band. The gain is reuse. In a tile, the data touched is small enough to stay in cache while every iteration of the tile uses it, so a program like [matrix multiplication](/blocked-matrix-multiplication/) loads each element a few times instead of once per use. Tiles are also units of parallel work, on CPUs and as the [shared-memory tiles](/shared-memory-tiling/) of GPUs.

## In plain words

Picture a big field that you water row after row. When you reach the end of a row, the hose you used at its start has to be pulled all the way back. Tiling means you water the field in small squares instead: finish one square, then move to the next. Everything you need for one square stays within reach. A program does the same with its data. In a small square of work, the values it uses are still in the fast memory when they are needed again. The order of the work changes, so it is safe only when no square needs a result from a square that now runs later. Choosing the square size is the second part: too large, and the data no longer fits.

## When it applies

The nest has a band of adjacent loops $p, \dots, q$ with step 1. The band is **fully permutable**: every dependence distance vector $d$ with $d_1 = \dots = d_{p-1} = 0$ has $d_l \ge 0$ for $p \le l \le q$. Dependences carried by the loops outside the band, which have a positive entry before $p$, are free. A band of one loop is always fully permutable. For direction vectors, the condition is that no such vector has $>$ or $*$ on the band.

If the band has a dependence with a negative entry, such as $(1, -1)$, the band is not fully permutable. [Loop skewing](/loop-skewing/) by a large enough factor makes it so, and then the skewed band can be tiled. The tile sizes $B_p, \dots, B_q$ are positive and do not change while the nest runs.

## The template

For a band of two loops with rectangular bounds:

```pseudo id=main
TILE(for i = L1 to U1: for j = L2 to U2: BODY(i, j), sizes B1, B2)
L1  if some dependence d has d_1 < 0 or d_2 < 0 then
L2      return "not fully permutable: skew first"
L3  for it = L1 to U1 step B1 do                          ▷ tile loops
L4      for jt = L2 to U2 step B2 do
L5          for i = it to min(it + B1 - 1, U1) do          ▷ element loops
L6              for j = jt to min(jt + B2 - 1, U2) do
L7                  BODY(i, j)
```

The holes are the band, the tile sizes, and the order of the element loops inside a tile, which is free on a fully permutable band. For a band of $m$ loops there are $m$ tile loops followed by $m$ element loops. When the bounds are not rectangular, for example after skewing, the bounds of the tile loops and element loops come from [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) of the original bounds together with $it \le i \le it + B_1 - 1$.

**Legality.** Let $t_l(i) = \lfloor (i_l - L_l) / B_l \rfloor$ be the tile number of the iteration $i$ on loop $l$. The tiled nest runs the iterations in the lexicographic order of the key
$$K(i) = (i_1, \dots, i_{p-1},\; t_p(i), \dots, t_q(i),\; i_p, \dots, i_q,\; i_{q+1}, \dots, i_k).$$
**Claim.** If the band is fully permutable, then every dependence from $i$ to $j = i + d$ has $K(i) \prec K(j)$.

*Proof.* If the first nonzero entry of $d$ is before $p$, then $K(i)$ and $K(j)$ differ first in that entry, and $K(i) \prec K(j)$. Otherwise $d_1 = \dots = d_{p-1} = 0$, and full permutability gives $d_l \ge 0$, so $j_l \ge i_l$ for every band loop. The floor function does not decrease, so $t_l(j) \ge t_l(i)$ for each $l$. If some tile number differs, the first one that differs is larger in $j$, and $K(i) \prec K(j)$. If all tile numbers are equal, the rest of the two keys is $i$ and $j$ without their common prefix, and $j - i = d$ is lexicographically positive with zeros before $p$, so again $K(i) \prec K(j)$. $\square$

With Theorem 1 of the [legality page](/loop-transformation-legality/), the tiled nest computes the same result. The condition is also needed in general: if $d = (1, -1)$ and $B_1 \ge 2$, the source $(i, j)$ at the first column of a tile and the sink $(i + 1, j - 1)$ in the previous column of tiles get $t_2(j) < t_2(i)$, and when both rows are in one row of tiles, the sink runs first.

**Profit.** The cost model is the number of cache misses. If the data that one tile touches fits in the cache, each element is loaded once per tile that uses it, instead of once per row or column of the whole space. For $n \times n$ matrix multiplication with $B \times B$ tiles in a cache too small for a whole matrix, this brings the misses from about $n^3$ for the order $i, j, k$, which reads `B` down a column, and about $n^3 / L$ for the order $i, k, j$, down to a small constant times $n^3 / (B L)$, where $L$ is the number of elements in a cache line. A rule of thumb for three operands is $3 B^2 \le$ the cache size in elements.

## Classic examples

**Matrix multiplication.** The nest `for i: for k: for j: C[i][j] = C[i][j] + A[i][k] * B[k][j]` has the dependence distance $(0, 1, 0)$ on `C[i][j]` in the order $i, k, j$. All entries are nonnegative, so the three loops form a fully permutable band, and tiling all three is legal. With $n = 32$, lines of 8 elements, the three arrays in separate memory and a fully associative LRU cache, the counted misses are:

| loop order | 32 lines (256 elements) | 64 lines (512 elements) |
|---|---|---|
| $i, j, k$, no tiling | 33025 | 4353 |
| $i, k, j$, no tiling | 4353 | 4353 |
| $i, k, j$, tiles $8 \times 8 \times 8$ | 1853 | 1161 |
| $i, k, j$, tiles $16 \times 16 \times 16$ | 4735 | 895 |

The lowest possible count is $3 \cdot 32^2 / 8 = 384$, one miss per line of each matrix. Tiles of 8 cut the misses by a factor of about 2.3 and 3.7 against the best untiled order. Tiles of 16 are better when the cache has 512 elements and worse than no tiling at all when it has 256: one $16 \times 16$ tile of `B` fills the whole small cache. The tiled code gives the same matrix as the original, with the same order of the additions into each `C[i][j]`, because the $k$ loop still runs in increasing order inside and across tiles. [Blocked matrix multiplication](/blocked-matrix-multiplication/) and [cache-oblivious matrix multiplication](/cache-oblivious-matrix-multiplication/) treat this problem in depth.

**A stencil after skewing.** A Gauss-Seidel style sweep `A[i][j] = (A[i-1][j] + A[i][j-1] + A[i-1][j+1]) / 3`, with $i$ the time step and $j$ the position, has the distances $(1, 0)$, $(0, 1)$ and $(1, -1)$. The last one has a negative entry, so the band is not fully permutable, and tiles in $(i, j)$ are illegal. Skewing $j' = j + i$ maps the distances to $(1, 1)$, $(0, 1)$ and $(1, 0)$, and the skewed nest can be tiled. In the original space, each tile is a parallelogram. The [loop skewing](/loop-skewing/) page gives the factor.

**Parallel tiles.** On a fully permutable band of depth 2, the tiles on one anti-diagonal $t_1 + t_2 = c$ do not depend on each other, because every dependence goes to a tile with an equal or larger number in each coordinate, and so to a larger sum, or to the same tile. The tiles of one anti-diagonal can run at the same time, as a [wavefront](/wavefront-parallelism/).

## Variations

- **Tiling for registers.** Tiles of $2 \times 2$ or $4 \times 4$ with the element loops fully unrolled keep a small block of `C` in registers. This is [unroll and jam](/loop-unrolling/) seen as tiling.
- **Multilevel tiling.** Tile the tile loops again, with one size per level of the [memory hierarchy](/memory-hierarchy/): registers, L1, L2.
- **Non-rectangular tiles.** Skewing then tiling gives parallelogram tiles in the original space. The [Pluto algorithm](/pluto-algorithm/) chooses the hyperplanes of the tiles by an integer program.
- **Cache-oblivious recursion.** Splitting the space recursively in halves gives tiles of every size at once and needs no tile size. See the [cache-oblivious model](/cache-oblivious-model/).
- **Copying.** Copy a tile of an operand into a contiguous buffer before use. This removes the conflict misses described below, at the cost of the copy.

## Pitfalls

- **Tiling a band that is not fully permutable.** One distance $(1, -1)$ is enough to make tiling wrong. Check the band, and skew first.
- **Tiles too large.** A tile whose data does not fit runs slower than the untiled loop, as the 256-element column of the table shows.
- **Conflict misses.** In a direct-mapped or low-associativity cache, the rows of a tile can map to the same sets, for example when the row length is a power of two. Lam, Rothberg and Wolf measured that the misses then depend strongly on the tile size and the matrix size. Choose a tile size from the cache geometry, or copy the tile.
- **Partial tiles.** Missing `min` bounds run iterations outside the space when $B$ does not divide the trip count.
- **Reductions.** If the band is fully permutable only after a reduction loop is treated as free of dependences, the floating-point result can change.

## Exercises

1. A nest has the distances $(1, 0)$, $(0, 1)$ and $(1, 1)$. Can both loops be tiled? *Answer.* Yes, all entries are nonnegative, so the band is fully permutable.
2. A nest has the distances $(1, 0)$ and $(1, -2)$. Which skewing factor $f$ in $j' = j + f i$ makes the band fully permutable? *Answer.* The new distances are $(1, f)$ and $(1, f - 2)$, so $f = 2$ is the smallest one.
3. For `for i = 1 to 10: for j = 1 to 10` and tiles of $4 \times 4$, how many tiles are there and how many iterations does the last tile have? *Answer.* $3 \times 3 = 9$ tiles. The tile with $it = jt = 9$ has $2 \times 2 = 4$ iterations.
4. A cache holds 4096 elements. What is the largest square tile for matrix multiplication by the rule $3 B^2 \le$ cache size? *Answer.* $B = 36$, since $3 \cdot 36^2 = 3888$ and $3 \cdot 37^2 = 4107$.

## References
