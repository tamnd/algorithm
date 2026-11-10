---
tag: B0S9SD
kind: algorithm
slug: parallel-strassen
name: Parallel Strassen algorithm
area: parallel/parallel-primitives
level: advanced
summary: Strassen's algorithm in the fork-join style. The ten block sums run in parallel, then the seven products, then the four output blocks, which gives work Θ(n^(lg 7)) and span Θ(log^2 n).
model: work-span-model
complexity:
  vars: {n: "the order of the matrices, a power of 2"}
  time: {worst: Θ(n^(lg 7))}
  depth: {worst: Θ(log^2 n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [strassen-algorithm, parallel-matrix-multiplication, master-theorem, fork-join-model, work-span-model]
see_also: [strassen-algorithm, parallel-matrix-multiplication, divide-and-conquer-matrix-multiplication, matrix-multiplication-exponent, cache-oblivious-matrix-multiplication, fork-join-parallelism, parallelism, work-efficiency]
sources:
  - paper: doi:10.1007/BF02165411
    title: Volker Strassen, Gaussian elimination is not optimal, Numerische Mathematik 13, 1969
    locator: pp. 354 to 356 (the seven products of a 2 by 2 block product)
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Section 4.2 (Strassen's method with the sums S1 to S10 and the products P1 to P7) and Section 27.2 (multithreaded matrix multiplication, with Strassen's method as an exercise)
---

Parallel Strassen runs [Strassen's algorithm](/strassen-algorithm/) as a [fork-join](/fork-join-parallelism/) program. Each level of the recursion has three steps, and the tasks of each step are independent: the ten sums of blocks, the seven recursive products of blocks, and the four blocks of the output, each a sum of some of the products. With parallel loops for the sums, a step of sums has span $\Theta(\log n)$, and the products add one call of half size. So the span is $S(n) = S(n/2) + \Theta(\log n) = \Theta(\log^2 n)$, the same as the [parallel divide and conquer product](/parallel-matrix-multiplication/) with a temporary matrix, while the work drops from $\Theta(n^3)$ to $\Theta(n^{\lg 7}) \approx \Theta(n^{2.807})$.

Notation on this page: $n = 2^L$ is the order of the matrices, $A_{ik}$ and $B_{kj}$ are the $n/2 \times n/2$ blocks, and $W$ and $S$ are the work and span in the [work-span model](/work-span-model/), counted with the rules of the [complexity proof](proofs/complexity.md): an operation on two entries costs 1, and a group of $k$ parallel tasks adds $k - 1$ to the work and $\lceil \lg k \rceil$ to the span. $\lg$ is $\log_2$.

## In plain words

Strassen found a way to multiply two tables cut into four quarters with seven products of quarters instead of eight. The price is some extra adding and subtracting of quarters before and after the products.

This version gives each part to a different worker. First, ten workers each add or subtract two quarters, at the same time. Then seven workers each multiply two quarters, at the same time, and each of them does the same trick again on its smaller tables. Last, four workers each build one quarter of the answer from the products.

The seven products wait for the sums, and the answer waits for the products. So the time is a few rounds of adding for each level of halving.

## The problem

The input is two $n \times n$ matrices $A$ and $B$ over a ring, with $n$ a power of 2; other sizes are padded or split as on the [Strassen's algorithm](/strassen-algorithm/) page. The output is $C = AB$. The sequential algorithm, its identities and its history are on that page; this page is about the parallel structure and its exact work and span.

## The algorithm

```pseudo id=main
P-STRASSEN(A, B)                              ▷ return A·B, with n a power of 2
L1  n ← the number of rows of A
L2  if n = 1 then return (a₁₁ · b₁₁)
L3  partition A and B into four n/2 × n/2 blocks
L4  in parallel compute the ten sums S₁, …, S₁₀ of the table, each by two nested parallel loops
L5  in parallel compute the seven products P₁, …, P₇ of the table, each by a call of P-STRASSEN
L6  sync
L7  in parallel: C₁₁ ← P₅ + P₄ − P₂ + P₆; C₁₂ ← P₁ + P₂; C₂₁ ← P₃ + P₄; C₂₂ ← P₅ + P₁ − P₃ − P₇
L8  return C
```

The sums and products are those of CLRS, 3rd edition, Section 4.2:

| sums | products |
|---|---|
| $S_1 = B_{12} - B_{22}$, $S_2 = A_{11} + A_{12}$ | $P_1 = A_{11} S_1$, $P_2 = S_2 B_{22}$ |
| $S_3 = A_{21} + A_{22}$, $S_4 = B_{21} - B_{11}$ | $P_3 = S_3 B_{11}$, $P_4 = A_{22} S_4$ |
| $S_5 = A_{11} + A_{22}$, $S_6 = B_{11} + B_{22}$ | $P_5 = S_5 S_6$ |
| $S_7 = A_{12} - A_{22}$, $S_8 = B_{21} + B_{22}$ | $P_6 = S_7 S_8$ |
| $S_9 = A_{11} - A_{21}$, $S_{10} = B_{11} + B_{12}$ | $P_7 = S_9 S_{10}$ |

Line L4 has an implicit sync at its end, since line L5 reads the sums. Each step writes only new matrices or its own block of $C$, so the tasks of a step share no cell that one of them writes.

## Example

Take $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}$, so the blocks are entries.

| step | values |
|---|---|
| line L4 | $S_1 = 6 - 8 = -2$, $S_2 = 3$, $S_3 = 7$, $S_4 = 2$, $S_5 = 5$, $S_6 = 13$, $S_7 = -2$, $S_8 = 15$, $S_9 = -2$, $S_{10} = 11$ |
| line L5 | $P_1 = 1 \cdot (-2) = -2$, $P_2 = 3 \cdot 8 = 24$, $P_3 = 7 \cdot 5 = 35$, $P_4 = 4 \cdot 2 = 8$, $P_5 = 65$, $P_6 = -30$, $P_7 = -22$ |
| line L7 | $C_{11} = 65 + 8 - 24 - 30 = 19$, $C_{12} = -2 + 24 = 22$, $C_{21} = 35 + 8 = 43$, $C_{22} = 65 - 2 - 35 + 22 = 50$ |

So $C = \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}$, the same as the triple loop. With the counting rules of this page the work is 43: line L4 costs $10 + 9 = 19$, line L5 costs $7 + 6 = 13$, and line L7 costs $3 + 1 + 1 + 3 + 3 = 11$. The span is 14: $4 + 1$ for line L4, $3 + 1$ for line L5, and $2 + 3$ for line L7. For larger $n$ the counts follow the closed forms below:

| $n$ | $W$ | $S$ |
|---|---|---|
| 2 | 43 | 14 |
| 8 | 3547 | 52 |
| 32 | 196363 | 106 |
| 64 | 1407313 | 139 |

## Correctness

Strassen's identities say that the four sums of line L7 equal $A_{i1}B_{1j} + A_{i2}B_{2j}$, which is the block $(AB)_{ij}$. They follow from expanding the seven products with the factor from $A$ kept on the left, so they hold in any ring, commutative or not. The parallel steps have no [determinacy race](/determinacy-race/): the sums of line L4 and the products of line L5 each write their own new matrix, and the four tasks of line L7 write four different blocks of $C$. Induction on $n$ then gives $C = AB$. The [full proof](proofs/correctness.md) has the expansion and each step.

## Complexity

The [complexity proof](proofs/complexity.md) has the details. With $m = n/2$:

- **Sums.** Each of the ten sums has work $2m^2 - 1$ and span $2\lceil \lg m \rceil + 1$; the group of ten adds 9 to the work and 4 to the span.
- **Products.** The group of seven calls has work $7W(m) + 6$ and span $S(m) + 3$.
- **Output blocks.** The four block sums use 3, 1, 1 and 3 operations per entry, with total work $12m^2 - 1$ and span $2\lceil \lg m \rceil + 5$.
- **Recurrences.** $W(n) = 7W(n/2) + 8n^2 + 4$ and $S(n) = S(n/2) + 4L + 9$, with $W(1) = S(1) = 1$.
- **Closed forms.** $W(n) = (37 \cdot 7^L - 32n^2 - 2)/3 = \Theta(n^{\lg 7})$ and $S(n) = 2L^2 + 11L + 1 = \Theta(\log^2 n)$. The parallelism is $\Theta(n^{\lg 7}/\log^2 n)$.
- **Master theorem.** The work recurrence is case 1 of the [master theorem](/master-theorem/), and the span recurrence is $S(n) = S(n/2) + \Theta(\log n)$, which gives $\Theta(\log^2 n)$.
- **Space.** A call allocates seventeen matrices of $(n/2)^2$ entries. On one processor this is at most $\tfrac{17}{3}n^2$ entries at a time; a parallel run can hold many more.

Counted with the same rules, the recursive product with a temporary matrix has work $n^3 + 2n^2(n-1) + \tfrac67(n^3 - 1)$, and Strassen's count is the smaller one exactly from $n = 512$ on; the tests check this up to $n = 2^{29}$. The span of Strassen is larger by about a factor of 2 ($2L^2$ against $L^2$), since each level has two steps of sums.

## Properties

- **Deterministic and race free.** Each task writes its own matrix or its own block.
- **Not in place.** Each level allocates the seventeen matrices of sums and products.
- **Any ring.** Commutativity is not used, so the algorithm works for blocks that are matrices themselves.
- **Exact over the integers.** Over floating point numbers, the extra sums make the error bound weaker than for the classical product, as on the [Strassen's algorithm](/strassen-algorithm/) page.

## Variants and improvements

- **Crossover.** Below a block size of some hundreds of rows, switch to a tuned classical product. In practice this is necessary: the sums cost more memory traffic than they save at small sizes.
- **Fewer sums.** The Winograd form of Strassen's algorithm uses 15 additions instead of 18, with the same seven products. The span does not change in order.
- **Lower span in other models.** If a parallel loop has span $O(1)$, as on a PRAM, each level costs $O(1)$ and the span is $\Theta(\log n)$.
- **Breadth first or depth first.** At the top levels, run the seven products in parallel (breadth first) while memory allows; below, split each product among the workers (depth first), which needs less memory. Communication-avoiding parallel Strassen schedules mix the two.
- **Other fast products.** Any bilinear scheme with $r$ products of $k \times k$ blocks gives work $\Theta(n^{\log_k r})$ and span $\Theta(\log^2 n)$ in the same way; see the [matrix multiplication exponent](/matrix-multiplication-exponent/).

## When to use it

- Use it for large dense products over exact rings, such as integers modulo a prime, where the error of the extra sums does not matter and $n$ is far above the crossover.
- Use it when the work matters more than the memory: the seventeen temporary matrices per level cost much memory in a parallel run.
- Use the [classical parallel product](/parallel-matrix-multiplication/) for floating point work that needs the usual error bounds, and for moderate $n$, where a tuned classical kernel is faster.

## Pitfalls

- **Starting the products before the sums end.** Line L5 reads the sums of line L4, so there must be a sync between them. Without it, a product can read a sum that is not yet written.
- **Writing the products into C.** If the calls of line L5 write their results into the blocks of $C$ and line L7 then reads them, two block sums of line L7 that both read $P_1$ (for $C_{12}$ and $C_{22}$) see a value that one of them has already changed. Each product needs its own matrix.
- **Running the recursion to 1 × 1.** Line L2 stops at single entries, where seventeen allocations and a group of spawns surround one multiply. Real code stops at a block size where the classical kernel is fast.
- **A wrong sign.** A single wrong sign in the table, for example $S_4 = B_{11} - B_{21}$, gives wrong results only in some blocks. Test against the triple loop on random matrices, as the tests here do.
- **Swapping the factors.** Over a ring that is not commutative, $P_4 = S_4 A_{22}$ in place of $A_{22} S_4$ is wrong. The order of the factors in the table matters for matrix blocks.

## Implementations

## History

Strassen (1969) showed that two $2 \times 2$ matrices can be multiplied with seven multiplications, and by recursion that $n \times n$ matrices can be multiplied with $O(n^{\lg 7})$ operations. Its structure, with independent sums and independent products at each level, made it a natural fit for parallel machines. In the fork-join model, CLRS, 3rd edition (2009), Section 27.2, asks for a multithreaded Strassen and its work, span and parallelism as an exercise, and the analysis on this page answers it with exact counts. Later work on distributed memory, such as communication-avoiding parallel Strassen, studied how to schedule the seven products so as to move the least data.

## References
