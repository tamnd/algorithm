---
tag: SBSZSV
kind: algorithm
slug: wolf-lam-locality-algorithm
name: Wolf-Lam locality optimization
aliases:
- data locality optimizing algorithm
- reuse analysis
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Models temporal and spatial reuse as vector spaces and picks unimodular transformations and tiling that keep the reuse in the innermost loops.
model: word-ram
complexity:
  vars: {k: the depth of the loop nest, D: the number of distance vectors, A: the number of array accesses}
  time: {worst: O(4^k k! k D + 2^k k^3 A^2)}
  space: {extra: O(k^2 + A)}
properties: {deterministic: true, recursive: false}
prereqs: [dependence-distance-vector, unimodular-transformations, loop-tiling]
see_also: [loop-interchange, loop-skewing, lamport-hyperplane-method, pluto-algorithm, polyhedral-model, nullspace, lru-cache, cache-oblivious-matrix-multiplication]
sources:
  - paper: doi:10.1145/113445.113449
    title: Michael E. Wolf and Monica S. Lam, A data locality optimizing algorithm, Proceedings of the ACM SIGPLAN 1991 Conference on Programming Language Design and Implementation (PLDI), 1991, 30-44
    locator: Section 4 (self-temporal, self-spatial and group reuse as vector spaces, uniformly generated sets, the localized vector space, memory accesses per iteration) and Section 5 (subsets of the loops tiled innermost, the SRP transformation)
  - paper: doi:10.1109/71.97902
    title: Michael E. Wolf and Monica S. Lam, A loop transformation theory and an algorithm to maximize parallelism, IEEE Transactions on Parallel and Distributed Systems 2(4), 1991, 452-471
    locator: unimodular transformations, fully permutable loop nests, and skewing to make a nest fully permutable
  - paper: doi:10.1016/0743-7315(88)90014-7
    title: Dennis Gannon, William Jalby and Kyle Gallivan, Strategies for cache and local memory management by global program transformation, Journal of Parallel and Distributed Computing 5(5), 1988, 587-616
    locator: uniformly generated references and reference windows
  - paper: doi:10.1145/106972.106981
    title: Monica S. Lam, Edward E. Rothberg and Michael E. Wolf, The cache performance and optimizations of blocked algorithms, ASPLOS-IV, 1991, 63-74
    locator: the choice of tile size and the effect of cache interference on tiled code
  - paper: doi:10.1145/233561.233564
    title: Kathryn S. McKinley, Steve Carr and Chau-Wen Tseng, Improving data locality with loop transformations, ACM Transactions on Programming Languages and Systems 18(4), 1996, 424-453
    locator: a simpler cost model in cache lines per loop and a memory order for permutation, fusion, distribution and reversal
---

The Wolf-Lam algorithm chooses a [unimodular transformation](/unimodular-transformations/) and a [tiling](/loop-tiling/) of a perfect loop nest so that data that the nest uses again is still in the cache when it is used again. It describes reuse with vector spaces: for an access $A[H i + c]$, the iterations that touch the same element differ by a vector in the [nullspace](/nullspace/) of $H$. The loops that run inside one tile span the *localized space* $L$, and reuse along a direction in $L$ becomes a cache hit. For each candidate set of loops, the algorithm checks that a legal transformation can put those loops innermost as a fully permutable band, estimates the memory accesses per iteration from the reuse spaces inside $L$, and keeps the cheapest set. Michael Wolf and Monica Lam published it at PLDI in 1991.

## In plain words

A program that walks over a big table often reads the same numbers many times. If the second read comes soon after the first, the number is still in the fast cache. If it comes late, the program waits for the slow memory. This algorithm looks at each array read in a loop nest and finds the directions in which the loops come back to the same number, or to a neighbour in the same cache line. Then it tries groups of loops. For each group it asks whether the loops can be legally reordered so that this group runs in small blocks at the inside of the nest. For each group that works, it estimates how many slow memory reads one step costs, and it keeps the cheapest group. Last, it cuts that group into blocks.

## The problem

**Input.** A perfect nest of depth $k$ with rectangular bounds. A set $D$ of constant [dependence distance vectors](/dependence-distance-vector/), each nonzero and lexicographically positive. A list of array accesses $A[H i + c]$, where $H$ is an integer matrix with $k$ columns and $c$ a constant vector; all accesses with the same array and the same $H$ form one *uniformly generated set*. The arrays are in [row-major order](/row-major-order/). Two numbers for the cost model: $l$, the number of elements in a cache line, and $s$, an estimate of the trip count of a loop inside a tile.

**Output.** A set $I$ of loops to localize, and a unimodular matrix $T$ that keeps every dependence and makes the loops of $I$ the innermost loops, as a fully permutable band. A band is *fully permutable* when every dependence that the outer loops do not carry has a nonnegative entry at every loop of the band; then every order of the band is legal, and so is tiling it.

**Goal.** The smallest estimated number of memory accesses per iteration. There are three kinds of reuse. An access has *self-temporal* reuse when it touches the same element in two iterations, and *self-spatial* reuse when it touches the same cache line. Two accesses of one uniformly generated set have *group* reuse when they touch the same data.

## The algorithm

```pseudo id=main
WOLF-LAM(accesses A[H i + c], distances D, depth k, line l, trip s)
L1  for each uniformly generated set (A, H) do R_ST <- ker H; R_SS <- ker H_S
L2  best <- none
L3  for each subset I of the loops, smallest first do
L4      T <- signed permutation with I innermost, then skew of I, with I fully permutable
L5      if no such T is legal then continue
L6      L <- span{e_j : j in I}
L7      cost <- sum over the sets of (g_S + (g_T - g_S) / l) / (l^e s^dim(R_ST ∩ L))
L8      if best = none or cost < best.cost then best <- (I, T, cost)
L9  apply best.T and tile the |I| innermost loops by B when |I| >= 2
```

Line L1 computes the reuse spaces. $R_{ST} = \ker H$ holds the directions in which one access touches the same element again. $H_S$ is $H$ with its last row set to $0$, so $R_{SS} = \ker H_S$ holds the directions in which the access stays in one row of the array, where the elements share cache lines. The spaces depend only on $H$, so one computation serves the whole set.

Lines L3 to L5 test whether the loops of $I$ can run innermost. Line L4 tries every order and every sign (loop reversal) of the loops outside $I$, then every order and sign of the loops of $I$, and accepts the first choice that makes every distance lexicographically positive. Then it [skews](/loop-skewing/) the band, loop by loop, by the smallest factor that makes the band entries of every distance not carried by an outer loop nonnegative. After the skew, the band is fully permutable.

Line L6 is the localized space. The outer loops are a signed copy of the loops outside $I$, so two iterations of one tile differ only on the loops of $I$, whatever the skew is.

Line L7 is the cost model of the paper. $g_T$ is the number of classes of offsets in a set, where $c_1$ and $c_2$ are in one class when $H r = c_1 - c_2$ for some $r \in L$: the accesses of a class touch the same data within a tile, so the class fetches it once. $g_S$ is the same count for $H_S$ and the offsets with their last entry set to $0$. The classes of $g_S$ fetch a cache line; the extra temporal classes inside them cost $1/l$ each. The term $s^{\dim(R_{ST} \cap L)}$ divides by $s$ for each localized direction of self-temporal reuse. $e = 1$ when $R_{SS} \cap L$ is larger than $R_{ST} \cap L$, which means the access also walks along a cache line inside the tile; then the cost divides by $l$. Otherwise $e = 0$. Line L8 keeps the cheapest set, and the smaller one on a tie. Line L9 tiles the band; a band of one loop needs no tile loop.

## Example

The [successive over-relaxation](/successive-over-relaxation/) sweep

```
for i1 = 1 to t:
  for i2 = 1 to n - 2:
    for i3 = 1 to n - 2:
      A[i2][i3] = (A[i2][i3] + A[i2+1][i3] + A[i2-1][i3] + A[i2][i3+1] + A[i2][i3-1]) / 5
```

has one uniformly generated set: $H = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$ with the offsets $(0,0)$, $(1,0)$, $(-1,0)$, $(0,1)$, $(0,-1)$. Line L1 gives $R_{ST} = \operatorname{span}\{e_1\}$: every sweep reads the same array. $H_S = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 0 \end{pmatrix}$ gives $R_{SS} = \operatorname{span}\{e_1, e_3\}$. The distances are $(0,1,0)$, $(0,0,1)$, $(1,0,0)$, $(1,-1,0)$ and $(1,0,-1)$. The candidates of lines L3 to L8, with $l = 8$ and $s = 100$:

| localized loops $I$ | $g_T$, $g_S$, $e$, $\dim(R_{ST} \cap L)$ | cost | value |
|---|---|---|---|
| none | 5, 3, 0, 0 | $3 + 2/l$ | 3.25 |
| $\{i_3\}$ | 3, 3, 1, 0 | $3/l$ | 0.375 |
| $\{i_2\}$ | 3, 1, 0, 0 | $1 + 2/l$ | 1.25 |
| $\{i_2, i_3\}$ | 1, 1, 1, 0 | $1/l$ | 0.125 |
| $\{i_1, i_2, i_3\}$ | 1, 1, 1, 1 | $1/(l s)$ | 0.00125 |
| $\{i_1\}$, $\{i_1, i_2\}$, $\{i_1, i_3\}$ | | not legal | |

Every set with $i_1$ inside and some other loop outside fails line L5. The outermost loop is then $i_2$ or $i_3$. The distances $(0, 1, 0)$ and $(1, -1, 0)$ have opposite signs at $i_2$, and $(0, 0, 1)$ and $(1, 0, -1)$ have opposite signs at $i_3$, so with either sign, one distance starts with a negative entry. The set of all three loops is legal only with the skew. Line L4 keeps the order $(i_1, i_2, i_3)$ and skews by $T = \begin{pmatrix} 1 & 0 & 0 \\ 1 & 1 & 0 \\ 2 & 1 & 1 \end{pmatrix}$. The distances become $(0,1,1)$, $(0,0,1)$, $(1,1,2)$, $(1,0,1)$ and $(1,1,1)$, all nonnegative, so the three new loops can be tiled.

An [LRU](/lru-cache/) simulation shows the effect and the limit of the model. The setup is 8 sweeps over the $30 \times 30$ interior of a $32 \times 32$ array, 8 elements per line, a cache of 32 lines, and the five reads of each iteration:

| order | misses |
|---|---|
| original | 1024 |
| tiles of 8 on $i_2, i_3$ only | 1120 |
| skewed, tiles of 4 | 502 |
| skewed, tiles of 8 | 512 |
| skewed, tiles of 16 | 1027 |

The skewed and tiled nest halves the misses. With tiles of 16, the data of one tile does not fit in the cache any more, and the result is worse than the original. The cost model does not see the tile size.

A smaller case: `for i: for j: sum += A[j][i]` walks down the columns. Here $R_{ST} = 0$ and $R_{SS} = \operatorname{span}\{e_1\}$. Localizing $\{i\}$ costs $1/l$ and localizing $\{j\}$ costs $1$, so the algorithm picks $\{i\}$ and [interchanges](/loop-interchange/) the loops. For $64 \times 64$ elements, lines of 8 and a 16-line cache, the misses fall from 4096 to 512.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts.

**The reuse spaces are exact.** One access touches the same element at $i$ and $i + r$ exactly when $H r = 0$, and the same row exactly when $H_S r = 0$. Two accesses of one set touch the same element at $i$ and $i'$ exactly when $H(i' - i) = c_1 - c_2$; with $i' - i \in L$ this is an equivalence relation on the offsets, because $H L$ is a subspace.

**The chosen nest keeps every dependence.** $T$ is a signed permutation followed by a unitriangular skew, so $\det T = \pm 1$. For each distance, the outer part of $T d$ is lexicographically positive, or it is $0$ and the band part is nonnegative and nonzero; an induction over the band loops shows that the skew factor of line L4 gives this. Then the tile entries $\lfloor b / B \rfloor$ cannot decrease along a dependence, and the order of tiles, then points, puts every sink after its source. By Theorem 1 of the [legality page](/loop-transformation-legality/), the result equals that of the original nest.

**The search finds the cheapest legal set.** Line L4 finds a transformation for $I$ exactly when some signed permutation with the loops of $I$ innermost is legal, since it tries all of them. The empty set is always legal. Line L3 tries every set, so line L8 ends with a set of minimum cost.

## Complexity

There are $2^k$ subsets. For one subset, line L4 tries at most $k!\,2^k$ signed permutations and checks each against $D$ distances in $O(k D)$; the skew costs $O(k^2 D)$. Line L7 compares the offsets of each set in pairs, and each comparison is a rank computation of $O(k^3)$ on vectors of length at most $k$, for a total of $O(k^3 A^2)$. In all, $O(4^k k!\, k D + 2^k k^3 A^2)$. Loop nests are shallow; for $k = 3$ there are 8 subsets and at most 48 signed permutations each. Line L1 is done once per set. The extra space is $O(k^2)$ for the matrices and $O(A)$ for the classes. The implementation produces the tiled order by sorting the $N$ iterations on their keys, $O(N \log N)$; a compiler emits loops instead.

## Properties

- **Model, not measurement.** The cost counts memory accesses per iteration under the assumption that the reuse inside a tile stays in the cache.
- **Exact legality.** Every transformation it returns keeps every dependence, for any tile size.
- **Loop axes only.** The localized spaces are spans of loop axes, as in the paper.
- **Tile size left open.** The choice of $I$ and $T$ does not depend on $B$; the tile size is a separate decision.

## Variants and improvements

- **The SRP heuristic.** Wolf and Lam do not try every signed permutation. Their SRP transformation (skew, reversal, permutation) places loops one at a time and runs in $O(n^2 d)$ for depth $n$ and $d$ dependences. They also prune the loops first: loops that carry no reuse and can go outermost are set aside, and so are loops that carry reuse but must stay outermost. Only the remaining loops enter the power set. The exhaustive search here is simpler and fast enough for $k \le 4$.
- **Simpler cost model.** McKinley, Carr and Tseng count, for each loop, the cache lines that the nest touches when that loop is innermost, and sort the loops into a *memory order*. They combine it with permutation, [fusion](/loop-fusion/), [distribution](/loop-distribution/) and reversal.
- **Tile size.** Lam, Rothberg and Wolf choose the tile size from the cache size and from cache interference; a tile that maps two rows onto the same cache lines loses its reuse.
- **Polyhedral scheduling.** The [Pluto algorithm](/pluto-algorithm/) finds tiling hyperplanes for imperfect nests and affine dependences in the [polyhedral model](/polyhedral-model/), with a cost on the dependence distances instead of a reuse model.
- **Recursion instead of tiles.** [Cache-oblivious matrix multiplication](/cache-oblivious-matrix-multiplication/) gets the same kind of locality for every cache size at once, without a tile size.

## When to use it

Use it for perfect nests of dense array code with affine subscripts and constant distances, such as stencils, relaxation sweeps and matrix kernels, when the compiler must choose between interchange, reversal, skewing and tiling. If the subscripts or the distances are not known at compile time, the reuse spaces cannot be computed. For imperfect nests, use a polyhedral scheduler. For a single loop order question in a two-deep nest, the [loop interchange](/loop-interchange/) page is enough.

## Pitfalls

- **The wrong row in line L1.** $H_S$ zeroes the last row only for row-major arrays. For column-major arrays, as in Fortran, zero the first row; otherwise the model finds spatial reuse in the wrong direction and makes the strided loop innermost.
- **No skew in line L4.** Without the skew, the band of all three SOR loops is not fully permutable: $(1, -1, 0)$ has a negative entry. Tiling it without the skew changes the result.
- **A zero distance in line L4.** A dependence inside one iteration has $d = 0$. It is never lexicographically positive, so it makes every set fail. Keep only the distances between different iterations.
- **Ties in line L8.** In the column example, $\{i\}$ and $\{i, j\}$ both cost $1/l$. With $\le$ instead of $<$ the larger set wins and adds tile loops for no gain.
- **Trusting line L7 for the tile size.** The cost does not depend on $B$. In the example, tiles of 16 give more misses than the original order; choose $B$ from the cache size in line L9.
- **Tiling a band of one loop in line L9.** That is [strip-mining](/strip-mining/) and changes no order, so it adds loop overhead and no locality.

## Implementations

## History

Dennis Gannon, William Jalby and Kyle Gallivan described in 1988 how to estimate the data a loop nest needs in a cache with reference windows of uniformly generated references. Michael Wolf and Monica Lam, at Stanford, gave in 1991 a loop transformation theory in which interchange, reversal and skewing are unimodular matrices, and a nest is tiled after it is made fully permutable. Their PLDI paper of the same year added the reuse vector spaces, the localized space and the cost per iteration, and searched the subsets of the loops for the cheapest one that can be tiled innermost. Lam, Rothberg and Wolf studied in the same year how the tile size and cache conflicts change the result. McKinley, Carr and Tseng in 1996 gave a simpler cost model, and the polyhedral schedulers of the 2000s, such as Pluto, extended tiling to imperfect nests.

## References
