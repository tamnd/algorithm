---
tag: A6Y79E
kind: algorithm
slug: parallel-matrix-transpose
name: Parallel matrix transpose
area: parallel/parallel-primitives
level: intro
summary: Transpose a square matrix in place by divide and conquer. Transpose the two diagonal blocks and swap the other two in parallel, with Θ(n^2) work, Θ(log n) span and n^2/B cache misses.
model: work-span-model
complexity:
  vars: {n: the order of the matrix, M: the cache size in words (at least 2B^2), B: the line size in words}
  time: {worst: Θ(n^2)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(log n)}
  io:
    worst: "Θ(n^2/B)"
properties: {deterministic: true, recursive: true, in_place: true}
prereqs: [fork-join-model, work-span-model, divide-and-conquer-paradigm, cache-oblivious-model]
see_also: [parallel-matrix-multiplication, cache-oblivious-matrix-multiplication, bit-matrix-transpose, fork-join-parallelism, external-memory-model, memory-coalescing, shared-memory-tiling, shared-memory-bank-conflicts]
sources:
  - paper: doi:10.1109/SFFCS.1999.814600
    title: Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, 40th Annual Symposium on Foundations of Computer Science (FOCS), 1999
    locator: Section 3, matrix transposition (the recursive transpose with O(1 + mn/B) cache misses)
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Chapter 27, Section 27.1 (the work-span model and parallel loops) and the exercises of Section 27.2 on transposing in parallel
---

Parallel matrix transpose turns the rows of a square matrix into its columns in place, with a [fork-join](/fork-join-parallelism/) divide and conquer. Split the matrix into four blocks. The transpose of the whole matrix has the transposes of the two diagonal blocks on the diagonal, and it exchanges the two other blocks, each transposed. So the algorithm transposes the two diagonal blocks and swaps the top right block with the transpose of the bottom left block, all three in parallel. The swap is a divide and conquer too, with four parallel parts. The work is $n^2 + n - 1$ in the cost model of this page, the span is $2\lg n + 1$, and on one processor the run makes only the $n^2/B$ cache misses that it must make, without knowing the cache size.

Notation on this page: $n$ is the order of the matrix, a power of 2 in the main form, and $n = 2^L$. $A_{ab}$ is the block in block row $a$ and block column $b$, and $X^{\mathsf T}$ is the transpose of $X$. $W$ is the work and $S$ the span in the [work-span model](/work-span-model/). $M$ is the cache size and $B$ the line size, both in words, as in the [cache-oblivious model](/cache-oblivious-model/). $\lg$ is $\log_2$.

## In plain words

To transpose a square table, mirror it in its main diagonal: the number in row 3, column 5 goes to row 5, column 3.

Cut the table into four squares. The two squares on the diagonal stay where they are, but each must be mirrored in its own diagonal. The two other squares change places, and each is mirrored on the way. These three jobs share no cell, so three workers can do them at the same time.

Changing the places of two squares also splits into four smaller jobs that share no cell. In the end, each job is one exchange of two numbers.

Small squares fit in the cache, so each piece of memory is loaded only once.

## The problem

The input is an $n \times n$ matrix $A$, stored by rows. The output is $A^{\mathsf T}$, with $a^{\mathsf T}_{rs} = a_{sr}$, in the same memory. Each pair of cells $(r, s)$ and $(s, r)$ with $r \ne s$ must exchange their values, and the diagonal stays. The sequential loop is two lines; the parallel question is how to keep the span small and the cache misses few at the same time.

## The algorithm

```pseudo id=main
P-TRANSPOSE(A, r, n)                       ▷ transpose the n × n block of A at (r, r) in place
L1  if n = 1 then return
L2  h ← n / 2
L3  spawn P-TRANSPOSE(A, r, h)              ▷ A₁₁
L4  spawn P-TRANSPOSE(A, r + h, h)          ▷ A₂₂
L5  P-SWAP-T(A, r, r + h, r + h, r, h)      ▷ swap A₁₂ with the transpose of A₂₁
L6  sync

P-SWAP-T(A, i, j, k, l, n)                 ▷ swap the n × n block X at (i, j) with the transpose of the block Y at (k, l)
L7  if n = 1 then exchange A[i][j] with A[k][l]; return
L8  h ← n / 2
L9  spawn P-SWAP-T(A, i, j, k, l, h); spawn P-SWAP-T(A, i, j + h, k + h, l, h)            ▷ X₁₁ with Y₁₁, X₁₂ with Y₂₁
L10 spawn P-SWAP-T(A, i + h, j, k, l + h, h); P-SWAP-T(A, i + h, j + h, k + h, l + h, h)  ▷ X₂₁ with Y₁₂, X₂₂ with Y₂₂
L11 sync
```

The call P-TRANSPOSE(A, 0, n) transposes the whole matrix. Line L5 uses the block identity $(A^{\mathsf T})_{12} = (A_{21})^{\mathsf T}$, and lines L9 and L10 use the same identity inside the swap: block $X_{ab}$ goes with block $Y_{ba}$.

For $n$ not a power of 2, split $n$ into $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$. The two blocks to swap are then $\lfloor n/2 \rfloor \times \lceil n/2 \rceil$ and $\lceil n/2 \rceil \times \lfloor n/2 \rfloor$, and the swap halves the longer side of the blocks in each step, as in the cache-oblivious transpose of Frigo, Leiserson, Prokop and Ramachandran (1999). The implementation has both forms.

## Example

Transpose the $4 \times 4$ matrix with rows $(1, 2, 3, 4)$, $(5, 6, 7, 8)$, $(9, 10, 11, 12)$, $(13, 14, 15, 16)$.

| step | cells | effect |
|---|---|---|
| line L3 on $A_{11}$ | swap $a_{12} = 2$ with $a_{21} = 5$ | $A_{11}$ becomes rows $(1, 5)$, $(2, 6)$ |
| line L4 on $A_{22}$ | swap $a_{34} = 12$ with $a_{43} = 15$ | $A_{22}$ becomes rows $(11, 15)$, $(12, 16)$ |
| line L5, part $X_{11}$, $Y_{11}$ | swap $a_{13} = 3$ with $a_{31} = 9$ | |
| line L5, part $X_{12}$, $Y_{21}$ | swap $a_{14} = 4$ with $a_{41} = 13$ | |
| line L5, part $X_{21}$, $Y_{12}$ | swap $a_{23} = 7$ with $a_{32} = 10$ | |
| line L5, part $X_{22}$, $Y_{22}$ | swap $a_{24} = 8$ with $a_{42} = 14$ | |

All six swaps can run at the same time, since no two touch the same cell. The result has rows $(1, 5, 9, 13)$, $(2, 6, 10, 14)$, $(3, 7, 11, 15)$, $(4, 8, 12, 16)$. There are $n(n-1)/2 = 6$ swaps, the work is $n^2 + n - 1 = 19$, and the span is $2 \lg n + 1 = 5$: the group of three calls (2), then the group of four calls in P-SWAP-T (2), then one swap (1).

## Correctness

The proof rests on the identity $(X^{\mathsf T})_{ab} = (X_{ba})^{\mathsf T}$ for the four blocks of a square block $X$. By induction on $n$, P-SWAP-T sets $X$ to $Y^{\mathsf T}$ and $Y$ to $X^{\mathsf T}$ whenever $X$ and $Y$ share no cell, and then P-TRANSPOSE sets each block to the block that the identity gives. The three calls of lines L3 to L5 touch the disjoint cell sets $A_{11}$, $A_{22}$ and $A_{12} \cup A_{21}$, and the four calls of lines L9 and L10 touch disjoint pairs of blocks, so there is no [determinacy race](/determinacy-race/). Each pair of cells off the diagonal is swapped exactly once. The [full proof](proofs/correctness.md) also covers the form for any $n$.

## Complexity

The [complexity proof](proofs/complexity.md) has the details. A swap costs 1, and a group of $k$ parallel calls adds $k - 1$ to the work and $\lceil \lg k \rceil$ to the span.

- **Work.** P-SWAP-T on two $n \times n$ blocks has $W_s(n) = 4W_s(n/2) + 3 = 2n^2 - 1$. Then $W(n) = 2W(n/2) + W_s(n/2) + 2$ gives $W(n) = n^2 + n - 1 = \Theta(n^2)$, with exactly $n(n - 1)/2$ swaps. The form for any $n$ has the same work, $n^2 + n - 1$.
- **Span.** $S_s(n) = S_s(n/2) + 2 = 2L + 1$, and $S(n) = 2 + \max\{S(n/2), S_s(n/2)\} = 2L + 1$. The form for any $n$ has span at most $2\lceil \lg n \rceil + 1$. So $S = \Theta(\log n)$, and the parallelism is $\Theta(n^2/\log n)$.
- **The span is optimal.** With binary forks, a computation of span $S$ has at most $2^S - 1$ unit steps, so any transpose that does $n(n-1)/2$ swaps has span at least $\lg(n(n - 1)/2 + 1) \ge 2L - 1$. P-TRANSPOSE is within 2 of this.
- **Cache misses.** On one processor, with rows that start at a line boundary, $B \ge 2$, $n \ge B$ and an LRU cache of at least $2B$ lines, the run has exactly $n^2/B$ misses. The calls of size $B$ each touch at most $2B$ whole lines, and different calls touch different lines. This is the least possible, since each line must be loaded once.
- **Space.** The transpose is in place. The recursion has depth $L$, so the extra space is $\Theta(\log n)$ for the stack.

The tests check all the exact counts, and count the misses of the plain row loop as well: for $n = 128$, $B = 8$ and a cache of 16 lines, the row loop has 9103 misses and P-TRANSPOSE has 2048.

## Properties

- **In place.** Only swaps change the matrix; there is no second matrix.
- **Deterministic and race free.** Parallel calls touch disjoint cells.
- **Cache oblivious.** The algorithm does not use $M$ or $B$, and it makes the least number of misses for each cache that holds two $B \times B$ blocks.
- **Exactly one swap per pair.** The diagonal is never touched, and each other pair is swapped once.

## Variants and improvements

- **Coarse base case.** Stop at blocks of some tens of rows and swap them with two plain loops. This removes most of the cost of the calls and keeps the cache behaviour, since such blocks fit in the cache.
- **Out of place.** To write $A^{\mathsf T}$ into a new matrix, split the longer side of the source and run the two halves in parallel. The bounds are the same, with no need to pair blocks.
- **Rectangular matrices.** Out of place, the same recursion works for $m \times n$ matrices with $\Theta(mn/B)$ misses (Frigo et al. 1999). In place, a rectangular transpose is a permutation of cycles of the index map and is much harder.
- **On a GPU.** Each thread block loads a tile into shared memory with reads along rows, and writes the transposed tile with writes along rows, so that both the reads and the writes are coalesced; see [memory coalescing](/memory-coalescing/), [shared memory tiling](/shared-memory-tiling/) and [shared memory bank conflicts](/shared-memory-bank-conflicts/), where a padded tile row avoids the conflicts.
- **Bit matrices.** For matrices of bits packed into words, [bit matrix transpose](/bit-matrix-transpose/) uses word operations on blocks with the same block identity.

## When to use it

- Use it when a matrix must change from row order to column order in place, for example before a step that reads columns, as in a fast Fourier transform on a two-dimensional array.
- Use it when the cache size is not known, or when the code runs on machines with different caches. A blocked loop tuned to one cache can be as fast, but only for that cache.
- Use the plain loop for small matrices that fit in the cache. The recursion costs more than it saves there.
- On a GPU, use the tiled transpose with shared memory, not this recursion.

## Pitfalls

- **Swapping the blocks without transposing them.** If line L5 only exchanges $A_{12}$ with $A_{21}$ cell by cell at the same offsets, the two blocks change places but are not transposed. Line L9 must pair $X_{12}$ with $Y_{21}$, not with $Y_{12}$.
- **A loop over all pairs.** A loop that swaps $a_{ij}$ with $a_{ji}$ for all $i$ and $j$ swaps each pair twice and leaves the matrix as it was. Only pairs with $j > i$ may be swapped; the recursion does this by never touching a cell twice.
- **Spawning the swap twice.** If line L5 swaps $A_{12}$ with $A_{21}^{\mathsf T}$ and a second call swaps $A_{21}$ with $A_{12}^{\mathsf T}$, the two calls race on the same cells.
- **Too fine a grain.** Line L7 makes a call and a spawn for each swap. Real code stops at a block that fits in a few cache lines.
- **Bad alignment.** The count of $n^2/B$ misses needs rows that start at a line boundary. With other row lengths each block row can span one more line, and the count rises, by up to a factor of 2.

## Implementations

## History

Transposing a matrix in place with few block transfers was studied for slow memories well before multicore machines. Frigo, Leiserson, Prokop and Ramachandran (1999) gave the recursive transpose that halves the longer side, and proved that it makes $O(1 + mn/B)$ cache misses for an $m \times n$ matrix without knowing the cache parameters. The same recursion, with its parts run in parallel, is a standard example of a fork-join algorithm with logarithmic span.

## References
