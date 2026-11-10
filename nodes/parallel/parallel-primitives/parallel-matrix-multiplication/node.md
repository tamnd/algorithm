---
tag: QZM9BG
kind: algorithm
slug: parallel-matrix-multiplication
name: Parallel matrix multiplication
area: parallel/parallel-primitives
level: core
summary: Three fork-join ways to multiply n by n matrices with Θ(n^3) work. Parallel loops give span Θ(n), and divide and conquer gives span Θ(log^2 n) with a temporary matrix or Θ(n) with none.
model: work-span-model
complexity:
  vars: {n: "the order of the matrices, a power of 2 for the recursive forms"}
  time: {worst: Θ(n^3)}
  depth: {worst: Θ(log^2 n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [naive-matrix-multiplication, divide-and-conquer-matrix-multiplication, parallel-for, fork-join-model, work-span-model]
see_also: [parallel-strassen, strassen-algorithm, cache-oblivious-matrix-multiplication, blocked-matrix-multiplication, parallel-matrix-transpose, fork-join-parallelism, determinacy-race, parallelism]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Chapter 27, Section 27.2, Multithreaded matrix multiplication (P-SQUARE-MATRIX-MULTIPLY and P-MATRIX-MULTIPLY-RECURSIVE with the temporary matrix T)
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 4th edition, MIT Press, 2022
    locator: Chapter 26, Section 26.2, Parallel matrix multiplication
  - paper: doi:10.1109/SFFCS.1999.814600
    title: Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, 40th Annual Symposium on Foundations of Computer Science (FOCS), 1999
    locator: Section 2, matrix multiplication (the recursive product and its cache misses)
---

Parallel matrix multiplication computes $C = AB$ for $n \times n$ matrices with a [fork-join](/fork-join-parallelism/) program. All three forms on this page do the $n^3$ products of the [triple loop](/naive-matrix-multiplication/), so the work is $\Theta(n^3)$; they differ in the span. Two [parallel loops](/parallel-for/) over the rows and the columns of $C$, with a sequential dot product inside, give span $\Theta(n)$. The [divide and conquer product](/divide-and-conquer-matrix-multiplication/) runs its eight block products at the same time, four into $C$ and four into a temporary matrix $T$, and then adds $T$ into $C$; this gives span $\Theta(\log^2 n)$. With no temporary matrix, the two products that go into one block of $C$ must run one after the other, and the span is $\Theta(n)$ again.

Notation on this page: $n$ is the order of the matrices, a power of 2 for the recursive forms, and $n = 2^L$. $W$ is the work and $S$ the span in the [work-span model](/work-span-model/) with the counting rules of the [complexity proof](proofs/complexity.md): a multiply-add or an add costs 1, and a group of $k$ parallel tasks adds $k - 1$ to the work and $\lceil \lg k \rceil$ to the span. $\lg$ is $\log_2$.

## In plain words

Each number in the answer is a row of the first table times a column of the second. These numbers do not depend on each other, so many workers can compute them at the same time. But each one is a long sum that one worker adds term by term, so the time is at least the length of one sum.

The faster way cuts each table into four quarters. The answer is built from eight products of quarters. All eight can run at the same time if half of them write into a spare table. At the end, the spare table is added into the answer. Each quarter product does the same again, so the long sums are added in a tree.

Without the spare table, two products write into the same quarter of the answer, so they must take turns, and the time is long again.

## The problem

The input is two $n \times n$ matrices $A$ and $B$ over a ring, for example the integers. The output is $C = AB$ with $c_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}$. The sequential forms and their history are on the pages [naive matrix multiplication](/naive-matrix-multiplication/) and [divide and conquer matrix multiplication](/divide-and-conquer-matrix-multiplication/). This page is about the parallel forms and their span.

## The algorithm

The main form is P-MATRIX-MULTIPLY-RECURSIVE of CLRS, 3rd edition, Section 27.2. The blocks $A_{ik}$, $B_{kj}$, $C_{ij}$ and $T_{ij}$ are the $n/2 \times n/2$ quarters, found by index arithmetic in $O(1)$ time.

```pseudo id=main
P-MATRIX-MULTIPLY-RECURSIVE(C, A, B)        ▷ set C to A·B, with n a power of 2
L1  n ← the number of rows of A
L2  if n = 1 then c₁₁ ← a₁₁ · b₁₁; return
L3  let T be a new n × n matrix
L4  partition A, B, C and T into four n/2 × n/2 blocks
L5  spawn P-MMR(C₁₁, A₁₁, B₁₁); spawn P-MMR(C₁₂, A₁₁, B₁₂); spawn P-MMR(C₂₁, A₂₁, B₁₁); spawn P-MMR(C₂₂, A₂₁, B₁₂)
L6  spawn P-MMR(T₁₁, A₁₂, B₂₁); spawn P-MMR(T₁₂, A₁₂, B₂₂); spawn P-MMR(T₂₁, A₂₂, B₂₁); P-MMR(T₂₂, A₂₂, B₂₂)
L7  sync
L8  parallel for i ← 1 to n
L9      parallel for j ← 1 to n
L10         c_ij ← c_ij + t_ij
```

P-MMR is short for P-MATRIX-MULTIPLY-RECURSIVE. Lines L5 and L6 compute $C_{ij} = A_{i1} B_{1j}$ and $T_{ij} = A_{i2} B_{2j}$ in parallel, and lines L8 to L10 add the two halves, since $(AB)_{ij} = A_{i1} B_{1j} + A_{i2} B_{2j}$.

The two other forms are short. The loop form is P-SQUARE-MATRIX-MULTIPLY of the same section:

```pseudo
P-SQUARE-MATRIX-MULTIPLY(A, B)
1  parallel for i ← 1 to n
2      parallel for j ← 1 to n
3          s ← 0; for k ← 1 to n do s ← s + a_ik · b_kj
4          c_ij ← s
```

The form with no temporary matrix adds $AB$ into $C$, and runs the two products of each block in two phases:

```pseudo
P-MATRIX-MULTIPLY-ADD(C, A, B)               ▷ C ← C + A·B
1  if n = 1 then c₁₁ ← c₁₁ + a₁₁ · b₁₁; return
2  partition A, B and C into four n/2 × n/2 blocks
3  spawn C₁₁ += A₁₁B₁₁; spawn C₁₂ += A₁₁B₁₂; spawn C₂₁ += A₂₁B₁₁; C₂₂ += A₂₁B₁₂   ▷ each by a call of P-MATRIX-MULTIPLY-ADD
4  sync
5  spawn C₁₁ += A₁₂B₂₁; spawn C₁₂ += A₁₂B₂₂; spawn C₂₁ += A₂₂B₂₁; C₂₂ += A₂₂B₂₂
6  sync
```

## Example

Take $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}$. The blocks are single entries. Lines L5 and L6 compute eight products at the same time:

| block | line L5 into $C$ | line L6 into $T$ | line L10: $c + t$ |
|---|---|---|---|
| $(1,1)$ | $a_{11} b_{11} = 1 \cdot 5 = 5$ | $a_{12} b_{21} = 2 \cdot 7 = 14$ | 19 |
| $(1,2)$ | $a_{11} b_{12} = 1 \cdot 6 = 6$ | $a_{12} b_{22} = 2 \cdot 8 = 16$ | 22 |
| $(2,1)$ | $a_{21} b_{11} = 3 \cdot 5 = 15$ | $a_{22} b_{21} = 4 \cdot 7 = 28$ | 43 |
| $(2,2)$ | $a_{21} b_{12} = 3 \cdot 6 = 18$ | $a_{22} b_{22} = 4 \cdot 8 = 32$ | 50 |

So $C = \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}$. The costs that the implementation counts for larger $n$ follow the closed forms of the next section exactly:

| $n$ | loops: $W$ | loops: $S$ | temporary: $W$ | temporary: $S$ | no temporary: $W$ | no temporary: $S$ |
|---|---|---|---|---|---|---|
| 2 | 11 | 4 | 22 | 7 | 14 | 6 |
| 8 | 575 | 14 | 1846 | 25 | 950 | 36 |
| 32 | 33791 | 42 | 124342 | 51 | 60854 | 156 |
| 64 | 266239 | 76 | 1002934 | 67 | 486838 | 316 |

The span with the temporary matrix grows as $\lg^2 n$, and it passes below the span of the loops at $n = 64$.

## Correctness

All three forms rest on the block identity $C_{ij} = A_{i1} B_{1j} + A_{i2} B_{2j}$, which follows by splitting the sum $\sum_k a_{ik} b_{kj}$ at $k = n/2$. The parallel parts have no [determinacy race](/determinacy-race/): in the loop form each iteration writes its own cell; in P-MATRIX-MULTIPLY-RECURSIVE the eight calls of lines L5 and L6 write eight different blocks, four of $C$ and four of $T$; in P-MATRIX-MULTIPLY-ADD the two calls that write the same block of $C$ are in different phases, with a sync between them. Induction on $n$ then gives $C = AB$. The [full proof](proofs/correctness.md) gives each step.

## Complexity

The [complexity proof](proofs/complexity.md) derives each count below with equality, and the tests check them.

| form | recurrences | work $W$ | span $S$ |
|---|---|---|---|
| parallel loops | none | $n^3 + n^2 - 1$ | $2\lceil \lg n \rceil + n$ |
| with temporary $T$ | $W = 8W(n/2) + 2n^2 + 6$, $S = S(n/2) + 2L + 4$ | $n^3 + 2n^2(n - 1) + \tfrac{6}{7}(n^3 - 1)$ | $L^2 + 5L + 1$ |
| no temporary | $W = 8W(n/2) + 6$, $S = 2S(n/2) + 4$ | $n^3 + \tfrac{6}{7}(n^3 - 1)$ | $5n - 4$ |

- **Loops.** The two loops add $2\lceil \lg n \rceil$ to the span, and the sequential dot product adds $n$. So $W = \Theta(n^3)$, $S = \Theta(n)$, and the [parallelism](/parallelism/) is $\Theta(n^2)$.
- **With a temporary matrix.** The eight calls run as one group, so the span recurrence has one call of half size, plus $\Theta(\log n)$ for the add of lines L8 to L10. So $S = \Theta(\log^2 n)$ and the parallelism is $\Theta(n^3 / \log^2 n)$. The work is $\Theta(n^3)$; with these counting rules its constant is about $3.86$, against 1 for the loops, because the adds and the forks of the add loops are counted.
- **No temporary matrix.** The two phases are in sequence, so the span doubles at each level: $S(n) = 2S(n/2) + \Theta(1) = \Theta(n)$. The parallelism is $\Theta(n^2)$, the same as the loops.
- **Space.** A run of P-MATRIX-MULTIPLY-RECURSIVE on one processor holds at most $n^2 + (n/2)^2 + \cdots < \tfrac43 n^2$ entries of temporary matrices at a time, but the matrices it allocates add up to $\Theta(n^3)$ over the run, and a parallel run can hold many of them at once. P-MATRIX-MULTIPLY-ADD needs no extra space apart from the recursion stack.
- **Cache.** The recursive forms touch blocks that fit in the cache once they are small enough. On one processor the recursive product makes $\Theta(n^3 / (B\sqrt{M}))$ cache misses for a cache of $M$ words with lines of $B$ words (Frigo, Leiserson, Prokop and Ramachandran 1999), see [cache-oblivious matrix multiplication](/cache-oblivious-matrix-multiplication/). The loop form reads a column of $B$ for each entry, which costs up to one miss per term.

## Properties

- **Deterministic.** The same work is done for each input; the counts depend only on $n$.
- **Not in place.** The output is separate from the inputs, and the main form needs temporary matrices.
- **Race free.** The writes of parallel tasks go to disjoint cells, as the correctness proof shows.
- **Any ring.** Only addition and multiplication are used, and the order of the products in each sum is fixed, so the result is exact over the integers. Over floating point numbers, the recursive forms add the terms in a different order from the loops, so the last bits of the result can differ.

## Variants and improvements

- **Coarse base case.** Stop the recursion at a block of some tens of rows and call a tuned sequential kernel, as in [blocked matrix multiplication](/blocked-matrix-multiplication/). The bounds stay the same, and the overhead of the forks becomes small.
- **Any size.** For $n$ not a power of 2, pad with zeros, or split each dimension into $\lceil n/2 \rceil$ and $\lfloor n/2 \rfloor$. For rectangular matrices, split the largest of the three dimensions, as the cache-oblivious product does. A split of the inner dimension needs a temporary matrix or two phases, as on this page.
- **A sum by reduction.** In the loop form, compute each dot product with a [parallel reduction](/parallel-reduce/). The span drops to $\Theta(\log n)$ and the work stays $\Theta(n^3)$, but each entry needs a reduction tree.
- **Fewer products.** [Parallel Strassen](/parallel-strassen/) uses seven block products instead of eight, which gives work $\Theta(n^{\lg 7})$ with span $\Theta(\log^2 n)$.
- **Distributed memory.** Cannon's algorithm and the 2.5D and 3D algorithms trade extra copies of the matrices for less communication between nodes.

## When to use it

- Use the loop form for a quick parallel product on a multicore machine. Its parallelism $\Theta(n^2)$ is already far more than the number of cores for any $n$ of interest.
- Use the recursive form with a coarse base case when the cache behaviour matters, and the form with the temporary matrix when the span matters, for example with very many processors.
- Use the form with no temporary matrix when memory is short. It has the same parallelism as the loops, with the cache behaviour of the recursive form.
- For production code, call a tuned library such as a BLAS. The parallel forms on this page show the structure; a tuned kernel is many times faster.

## Pitfalls

- **Writing all eight products into C.** If line L6 also writes into $C$, then two parallel calls write the same block, which is a [determinacy race](/determinacy-race/), and the result depends on the schedule. Half of the products must go into $T$.
- **Leaving out the sync.** Without line L7, lines L8 to L10 can read $T$ before the products of line L6 have written it.
- **A parallel loop over k.** Making the inner loop of line 3 of the loop form a parallel loop that adds into $c_{ij}$ races on $c_{ij}$. A parallel sum needs a reduction, not a shared accumulator.
- **Too fine a grain.** Line L2 stops at $1 \times 1$ blocks, where one multiply sits inside a whole function call and a spawn. Real code stops at a block that fills a part of the cache.
- **Allocation cost.** Line L3 allocates a new matrix at each call. With a coarse base case this is small, but a fine grain makes the memory allocator a bottleneck.

## Implementations

## History

Parallel matrix products were studied for the PRAM and for networks of processors long before multicore machines; Cannon's algorithm of 1969 is an early algorithm for a mesh. In the fork-join model, CLRS, 3rd edition (2009), Section 27.2, gives the loop form P-SQUARE-MATRIX-MULTIPLY with span $\Theta(n)$ and the recursive P-MATRIX-MULTIPLY-RECURSIVE with the temporary matrix and span $\Theta(\log^2 n)$. The form with no temporary matrix is the plain way to run the sequential recursion in parallel, and it trades the span for memory. Frigo, Leiserson, Prokop and Ramachandran (1999) showed that the recursive order is also optimal in its use of the cache, without knowing the cache size.

## References
