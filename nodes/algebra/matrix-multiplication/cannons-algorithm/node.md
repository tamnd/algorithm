---
tag: E9RHBT
kind: algorithm
slug: cannons-algorithm
name: Cannon's algorithm
aliases:
- Cannon's matrix multiplication
- Cannon's method
area: algebra/matrix-multiplication
level: advanced
summary: Multiplies n×n matrices on a q×q processor grid; after an initial skew it shifts A left and B up q times, so each processor sends 2n^2/q words and does n^3/q^2 multiplications.
model: bsp-model
complexity:
  vars: {n: the order of the matrices, P: the number of processors (a square q^2), g: the BSP cost per word of an h-relation (extra space is counted per processor), L: the BSP cost of a barrier}
  time: {worst: "O(n^3/P + g n^2/sqrt(P) + L sqrt(P))"}
  space: {extra: Θ(n^2/P)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1969
  people: [Lynn E. Cannon]
  note: Cannon described the method in his PhD thesis at Montana State University, for a two-dimensional array of cells with wraparound connections.
prereqs: [blocked-matrix-multiplication, bsp-model]
see_also: [parallel-matrix-multiplication, h-relation, superstep, red-blue-pebble-game, pebbling-lower-bound, cache-oblivious-matrix-multiplication, parallel-strassen]
sources:
  - paper: "Lynn Elliot Cannon, A cellular computer to implement the Kalman filter algorithm, PhD thesis, Montana State University, 1969"
    locator: the cellular array and the shifting schedule for the matrix product
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition
    locator: Section 8.2, Matrix-matrix multiplication (Cannon's algorithm, the DNS algorithm, and their cost on a mesh and a hypercube)
  - paper: doi:10.1145/79173.79181
    title: Leslie G. Valiant, A bridging model for parallel computation, Communications of the ACM 33(8), 1990
    locator: pp. 103 to 111 (the BSP model, supersteps, h-relations and the costs g and L)
  - paper: "Dror Irony, Sivan Toledo and Alexander Tiskin, Communication lower bounds for distributed-memory matrix multiplication, Journal of Parallel and Distributed Computing 64(9), 2004"
    locator: pp. 1017 to 1026 (Ω(n^3/(P sqrt(M))) words for some processor with M words of memory, so Ω(n^2/sqrt(P)) with M = Θ(n^2/P))
  - paper: "Robert A. van de Geijn and Jerrell Watts, SUMMA, scalable universal matrix multiplication algorithm, Concurrency: Practice and Experience 9(4), 1997"
    locator: pp. 255 to 274 (broadcasts along rows and columns instead of shifts, for any grid shape)
  - paper: "Edgar Solomonik and James Demmel, Communication-optimal parallel 2.5D matrix multiplication and LU factorization algorithms, Euro-Par 2011, Lecture Notes in Computer Science 6853"
    locator: the 2.5D version of Cannon's algorithm with c copies and n^2/sqrt(cP) words per processor
---

Cannon's algorithm multiplies two $n \times n$ matrices on $P = q^2$ processors arranged in a $q \times q$ grid with wraparound. Processor $(i, j)$ owns the blocks $A_{ij}$, $B_{ij}$ and $C_{ij}$ of side $n/q$. First the rows of $A$ are rotated left and the columns of $B$ rotated up by different amounts, the skew, so that each processor holds a matching pair $A_{ik}$ and $B_{kj}$. Then, $q$ times, every processor multiplies its pair into $C_{ij}$ and passes its $A$ block one step left and its $B$ block one step up. Each processor does $n^3/q^2$ multiplications and sends $2n^2/q$ words, and it needs only three blocks of memory. In the [BSP model](/bsp-model/) this costs $O(n^3/P + g\, n^2/\sqrt P + L \sqrt P)$, and the communication is optimal for algorithms that keep one copy of the data.

## In plain words

Many computers sit in a square grid, and each one holds one tile of each of the two input tables and one tile of the answer. To build its answer tile, a computer needs a whole row of tiles of the first table and a whole column of tiles of the second. Copying all of them everywhere costs too much memory and traffic.

Cannon's trick moves the tiles around in rings instead. The tiles of the first table move to the left along the rows, and the tiles of the second table move up along the columns. A first shuffle lines them up so that, at each step, every computer holds two tiles that belong together. Each computer multiplies its two tiles, adds the result to its answer tile, and passes the tiles on to its neighbours. After one full turn of the rings, every answer tile is complete.

## The problem

The input is an $n \times n$ matrix $A$ and an $n \times n$ matrix $B$ over a ring $R$, distributed in blocks over a $q \times q$ grid of processors; the output is $C = AB$, distributed the same way. Commutativity is not used and no subtraction is needed, so semirings also work. Rectangular shapes $n \times m$ and $m \times p$ work the same way with rectangular blocks; when $q$ does not divide a side, the matrices are padded with zeros.

The cost model is the [bulk synchronous parallel model](/bsp-model/) of Valiant (1990). A computation is a sequence of [supersteps](/superstep/). In each superstep every processor computes on its local data, then sends and receives messages, then all processors wait at a barrier. If the largest local work is $w$ and every processor sends and receives at most $h$ words (an [h-relation](/h-relation/)), the superstep costs $w + g h + L$. The total cost is $W + gH + LS$ with $W$ and $H$ the sums of $w$ and $h$ over the supersteps and $S$ their number. Index the grid and the blocks from $0$ to $q - 1$, and let $s = n/q$.

## The algorithm

```pseudo id=main
CANNON(A, B, q)                        ▷ processor (i, j) holds A_ij, B_ij; all indices mod q
L1  each processor (i, j) sets C_ij ← 0
L2  skew: (i, j) sends its A block to (i, j − i) and its B block to (i − j, j)
L3  for t ← 0 to q − 1 do
L4      each (i, j) sets C_ij ← C_ij + A_local · B_local, by a sequential product
L5      if t < q − 1 then (i, j) sends A_local to (i, j − 1) and B_local to (i − 1, j)
L6  return C, with C_ij on processor (i, j)
```

Line L2 rotates row $i$ of the $A$ blocks left by $i$ places and column $j$ of the $B$ blocks up by $j$ places. After it, processor $(i, j)$ holds $A_{i, i+j}$ and $B_{i+j, j}$. Line L4 is local work: any sequential product, such as a [blocked product](/blocked-matrix-multiplication/), can be used. Line L5 rotates every row of $A$ blocks left by one and every column of $B$ blocks up by one; on a torus each processor talks only to its neighbours. In BSP terms, line L2 is one superstep with communication only, and each pass of the loop is one superstep: the work of L4 followed by the communication of L5.

## Example

Take $q = 3$ and blocks of size $1 \times 1$, so each processor holds one entry, with
$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 10 \end{pmatrix}, \qquad B = \begin{pmatrix} 1 & 0 & 2 \\ 0 & 1 & 1 \\ 1 & 1 & 0 \end{pmatrix}.$$

At step $t$ processor $(i, j)$ holds $a_{ik}$ and $b_{kj}$ with $k = (i + j + t) \bmod 3$. The values of $k$ form a Latin square at each step:

| step | row 0 | row 1 | row 2 |
|---|---|---|---|
| $t = 0$ | $0, 1, 2$ | $1, 2, 0$ | $2, 0, 1$ |
| $t = 1$ | $1, 2, 0$ | $2, 0, 1$ | $0, 1, 2$ |
| $t = 2$ | $2, 0, 1$ | $0, 1, 2$ | $1, 2, 0$ |

So each processor sees each $k$ exactly once. For processor $(1, 1)$: at $t = 0$, $k = 2$ and it adds $a_{12} b_{21} = 6 \cdot 1 = 6$; at $t = 1$, $k = 0$ and it adds $a_{10} b_{01} = 4 \cdot 0 = 0$; at $t = 2$, $k = 1$ and it adds $a_{11} b_{11} = 5 \cdot 1 = 5$. So $c_{11} = 11$. For processor $(0, 0)$ the terms are $1 \cdot 1$, $2 \cdot 0$ and $3 \cdot 1$, so $c_{00} = 4$. The full result is
$$AB = \begin{pmatrix} 4 & 5 & 4 \\ 10 & 11 & 13 \\ 17 & 18 & 22 \end{pmatrix}.$$
The run has $S = 4$ supersteps (the skew and three compute steps), each processor does $3$ multiplications, and the h-relations are $2$ words each in the skew and the two shifts, so $H = 6 = 2n^2/q$. The implementation reproduces these counts.

At a larger size: $n = 4096$ on $P = 64$ processors ($q = 8$, blocks of $512 \times 512$). Each processor does $n^3/P = 2^{30} \approx 1.07 \times 10^9$ multiplications and as many additions, sends $H = 2n^2/q = 4\,194\,304$ words, holds $3 \cdot 512^2 = 786\,432$ words, and the run has $S = 9$ supersteps.

## Correctness

**Invariant.** At the start of step $t$ of line L3, processor $(i, j)$ holds $A_{i, k}$ and $B_{k, j}$ with $k = (i + j + t) \bmod q$, and $C_{ij} = \sum_{u < t} A_{i, (i+j+u) \bmod q} B_{(i+j+u) \bmod q, j}$.

After the skew, processor $(i, j')$ has received the $A$ block from $(i, j' + i)$, which is $A_{i, i + j'}$, and the $B$ block from $(i' + j, j)$ for $(i', j)$, which is $B_{i'+j, j}$. So the invariant holds for $t = 0$. Line L4 adds $A_{ik} B_{kj}$ for the current $k$. Line L5 gives processor $(i, j)$ the $A$ block of $(i, j + 1)$, whose index is $i + j + 1 + t$, and the $B$ block of $(i + 1, j)$, whose index is also $i + j + 1 + t$. So the invariant holds for $t + 1$. As $t$ runs from $0$ to $q - 1$, $(i + j + t) \bmod q$ takes every value in $\{0, \ldots, q-1\}$ once, so at the end $C_{ij} = \sum_k A_{ik} B_{kj}$, which is the block $(i, j)$ of $AB$ by block multiplication. The full proof is in the proofs section.

## Complexity

With $s = n/q$:

- **Work.** Each processor does $q$ block products of $s \times s$ blocks, $q s^3 = n^3/q^2 = n^3/P$ multiplications and as many additions. So $W = \Theta(n^3/P)$, which is perfect speedup over the triple loop.
- **Communication.** The skew and each of the $q - 1$ shifts are h-relations with $h = 2s^2$: each processor sends and receives at most one $A$ block and one $B$ block. So $H = q \cdot 2s^2 = 2n^2/q = 2n^2/\sqrt P$ for $q \ge 2$.
- **Supersteps.** $S = q + 1 = \sqrt P + 1$.
- **BSP cost.** $W + gH + LS = 2n^3/P + 2g\, n^2/\sqrt P + L(\sqrt P + 1)$.
- **Memory.** Three blocks, $3n^2/P$ words per processor, plus a buffer for incoming blocks. No processor ever holds more than its share of the data.
- **Lower bound.** Irony, Toledo and Tiskin (2004) proved that for the classical product on $P$ processors with $M$ words of memory each, some processor sends or receives $\Omega(n^3/(P\sqrt M))$ words. With $M = \Theta(n^2/P)$, the least memory that holds the data, this is $\Omega(n^2/\sqrt P)$. So Cannon's algorithm is optimal in words moved, up to a constant, among algorithms with this memory.

The BSP costs are exact counts for the schedule. Real running times depend on the network: on a torus each shift is between neighbours, while other networks route the skew over longer paths, and overlapping the shifts with the local products hides some of the communication (observed in practice).

## Properties

- **Memory-efficient.** Each processor holds only its own blocks: $3n^2/P$ words.
- **Neighbour communication.** On a 2D torus, every shift of line L5 is between neighbours, which is why it suits mesh and systolic machines.
- **Same arithmetic as the classical product.** It computes the same $n^3$ products, but the summation order for each $c_{ij}$ depends on $(i + j)$, so in floating point the result can differ from the sequential loop in rounding.
- **Square grid only.** The schedule needs $P = q^2$ and, in its simple form, square block counts in each direction.

## Variants and improvements

- **Fox's algorithm.** Fox, Otto and Hey (1987) broadcast a block of $A$ along each row and shift $B$ up, with no initial skew. It has the same costs up to constants.
- **SUMMA.** Van de Geijn and Watts (1997) broadcast a block column of $A$ along the rows and a block row of $B$ along the columns at each step. It works on any rectangular grid and any shapes, and variants of it are used in ScaLAPACK and later libraries.
- **3D algorithms.** With $P$ processors in a $P^{1/3} \times P^{1/3} \times P^{1/3}$ cube and $P^{1/3}$ copies of the data, each processor sends $O(n^2/P^{2/3})$ words, at the cost of $n^2/P^{2/3}$ words of memory per processor (Aggarwal, Chandra and Snir, 1990; Agarwal and others, 1995).
- **2.5D algorithms.** Solomonik and Demmel (2011) keep $c$ copies, for $1 \le c \le P^{1/3}$, and run a shortened Cannon schedule on each layer. Each processor then sends $O(n^2/\sqrt{cP})$ words and holds $O(c n^2/P)$, which matches the lower bound for that memory.
- **BSP versions.** McColl and Tiskin (1999) gave memory-efficient BSP algorithms for matrix multiplication with matching bounds.
- **Fast local products.** Line L4 can use [Strassen's algorithm](/strassen-algorithm/) locally; parallelizing Strassen itself across processors is a different problem, see [parallel Strassen](/parallel-strassen/).

## When to use it

Use it for dense products on distributed memory when the processor count is a perfect square and memory is tight, or on hardware with a 2D torus or mesh. Most libraries use SUMMA instead, because it handles any grid shape and any matrix shapes with the same performance. When memory is plentiful and $P$ is large, the 2.5D and 3D algorithms move fewer words. On a single shared-memory machine, use a [blocked](/blocked-matrix-multiplication/) or [recursive](/cache-oblivious-matrix-multiplication/) product with threads instead.

## Pitfalls

- **Wrong skew direction.** Row $i$ of $A$ moves left by $i$ and column $j$ of $B$ moves up by $j$. Moving both in the same direction, or by $j$ and $i$, gives unmatched pairs and a wrong result.
- **Shifting after the last product.** The $q$-th shift is not needed; doing it costs one more h-relation. Undoing the skew at the end, to restore the input layout, costs one more.
- **Non-square grids.** With $P$ not a perfect square, the simple schedule does not apply. Use SUMMA or a generalized Cannon.
- **Deadlock with blocking sends.** If every processor first sends and then receives with blocking calls, a ring can deadlock. Use combined send and receive operations or double buffering.
- **Uneven padding.** Padding a side to a multiple of $q$ makes the last row and column of processors do work on zeros; for small $n/q$ this load imbalance is noticeable.

## Implementations

## History

Lynn Cannon described the method in his 1969 PhD thesis at Montana State University, for a cellular array of processors, in the context of a Kalman filter. The systolic arrays of Kung and Leiserson (1978) use a similar flow of data. Fox, Otto and Hey (1987) gave the broadcast variant for hypercubes. Valiant's BSP model (1990) gave a machine-independent way to state its cost. Van de Geijn and Watts introduced SUMMA in 1997. Irony, Toledo and Tiskin proved in 2004 that the communication of Cannon's algorithm is optimal for its memory, and Solomonik and Demmel's 2.5D algorithm (2011) extended it to trade memory for communication.

## References
