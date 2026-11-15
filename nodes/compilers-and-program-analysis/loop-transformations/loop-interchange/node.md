---
tag: ZBVENY
kind: technique
slug: loop-interchange
name: Loop interchange
aliases:
- loop permutation
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Swaps two loops of a nest, which can make memory access contiguous or move a parallel loop outward, when dependences allow.
prereqs: [dependence-distance-vector, dependence-direction-vector, loop-transformation-legality]
see_also: [loop-tiling, loop-skewing, unimodular-transformations, strip-mining, locality-of-reference, vectorization, doall-loop, wolf-lam-locality-algorithm]
sources:
  - paper: doi:10.1145/502874.502897
    title: John R. Allen and Ken Kennedy, Automatic loop interchange, Proceedings of the SIGPLAN '84 Symposium on Compiler Construction, ACM, 1984, 233-246
    locator: the direction-vector test for interchange, the (<, >) direction as the case that forbids it, and interchange for vector and parallel code
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Section 5.2 (Loop Interchange), the legality theorem in direction vectors and the interchange of loops for vectorization; Chapter 9 (Managing Cache), interchange for stride
  - book: isbn:9780805327304
    title: Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996
    locator: the chapter on loop restructuring, loop interchange of rectangular and triangular nests and the computation of the new bounds
---

Loop interchange swaps two adjacent loops of a perfect nest, so that `for i: for j: S` becomes `for j: for i: S`. The body and the set of iterations stay the same, and only their order changes. The interchange is legal exactly when no dependence would point backward in the new order, that is, when no [distance vector](/dependence-distance-vector/) has the [direction](/dependence-direction-vector/) $(<, >)$ on the two loops with $=$ before them. A compiler uses it for two goals. It can put the loop that walks memory with stride 1 innermost, which improves [locality](/locality-of-reference/), and it can move a loop with no carried dependence inward for [vector code](/vectorization/) or outward for coarse [parallel](/doall-loop/) work. A legal interchange is not always a good one: the same swap that helps one nest can make another nest several times slower.

## In plain words

Picture a table of numbers that you visit cell by cell, row after row. Interchange means you visit it column after column instead. You still visit every cell once. The question is whether any cell needs a value that another cell computes first. If cell B uses the result of cell A, then A must still come before B in the new order. For a swap of rows and columns, only one shape of need breaks: a cell that uses a cell in the row above and in a column to the right. In the new order that right column is not yet done. When no cell needs such a value, the swap is safe. Then the only question is speed, and the swap can make it better or worse.

## When it applies

The nest is perfect: the loops $p$ and $p+1$ are adjacent and all statements are inside the inner one. The bounds of loop $p+1$ do not depend on values that the body computes. The dependences of the nest are known as distance vectors $d = (d_1, \dots, d_k)$, or, when the distance is not constant, as direction vectors over $<$, $=$ and $>$.

**Theorem.** Interchanging loops $p$ and $p+1$ maps every dependence to a lexicographically positive vector if and only if no dependence vector has $d_1 = \dots = d_{p-1} = 0$, $d_p > 0$ and $d_{p+1} < 0$. In direction vectors: no vector of the form $(=, \dots, =, <, >, \dots)$ with the $<$ at position $p$.

By Theorem 1 of the [legality page](/loop-transformation-legality/), an interchange that keeps every dependence pair in order keeps the meaning of the program. If a vector of the forbidden form exists, the swap runs the sink of a real dependence before its source, and the program reads a value that is not yet written, or writes over one that is not yet read. The example below shows that this changes the result.

## The template

```pseudo id=main
INTERCHANGE(nest, loops p and p + 1)
L1  for each dependence vector d of the nest do
L2      if d_1 = ... = d_(p-1) = 0 and d_p > 0 and d_(p+1) < 0 then
L3          return "illegal"                    ▷ this d becomes negative
L4  swap the headers of loops p and p + 1
L5  recompute the bounds of the two loops       ▷ by Fourier-Motzkin if they depend on each other
L6  return the new nest
```

The holes are the nest, the pair of loops, and the list of dependence vectors. When a vector has a direction and not a distance, the test of line L2 must treat $*$ as "could be $<$, $=$ or $>$": a vector $(<, *)$ blocks the swap, because one of its instances is $(<, >)$.

**Proof of the theorem.** The swap maps the vector $d$ to $d'$, which is $d$ with the entries $p$ and $p+1$ exchanged. A dependence vector is lexicographically positive, so it has a first nonzero entry, at level $l$, and $d_l > 0$. Four cases:

- $l < p$. The entries before $p$ do not move, so $d'$ has the same first nonzero entry $d_l > 0$.
- $l > p + 1$. The entries $p$ and $p+1$ are both $0$, so $d' = d$.
- $l = p + 1$. Then $d_p = 0$ and $d_{p+1} > 0$, so $d'_p = d_{p+1} > 0$ is the first nonzero entry of $d'$.
- $l = p$. Then $d'_p = d_{p+1}$. If $d_{p+1} > 0$, then $d'$ is positive at $p$. If $d_{p+1} = 0$, then $d'_{p+1} = d_p > 0$ is the first nonzero entry. If $d_{p+1} < 0$, then $d'$ has its first nonzero entry negative, and $d' \prec 0$.

So $d'$ is negative in exactly one case: $l = p$ and $d_{p+1} < 0$, which is the condition of the theorem.

**Bounds.** For a rectangular nest, the bounds move with the headers. When the inner bounds depend on the outer index, write the bounds as inequalities and eliminate in the new order with [Fourier-Motzkin elimination](/fourier-motzkin-elimination/). For `for i = 1 to n: for j = i to n`, the inequalities are $1 \le i$, $i \le j$, $j \le n$. With $j$ outer, eliminating $i$ gives $1 \le j \le n$, and then $1 \le i \le j$:

```
for j = 1 to n:
  for i = 1 to j:
    S(i, j)
```

**Profit.** The cost model is the number of cache misses, or the number of loop levels that carry no dependence at the place where they are useful. For an array stored row by row, `A[i][j]` with $j$ innermost walks memory with stride 1, and a cache line of $L$ elements serves $L$ accesses. With $i$ innermost, the stride is the row length $n$, and each access touches a new line unless the cache holds a full column of lines.

## Classic examples

**An illegal swap.** The nest

```
for i = 1 to n:
  for j = 1 to n:
    A[i][j] = A[i-1][j+1] + 1
```

has a flow dependence from $(i-1, j+1)$ to $(i, j)$, with distance $(1, -1)$ and direction $(<, >)$. After the swap, the instance $(2, 1)$ runs in the first column, before $(1, 2)$ has written $A[1][2]$. With $n = 4$ and the start values $A[i][j] = 10i + j$, the original order gives $A[2][1] = 5$: it reads $A[1][2] = A[0][3] + 1 = 4$. The swapped order reads the old $A[1][2] = 12$ and gives $13$. Nine of the 16 elements of the result differ. The [loop skewing](/loop-skewing/) page shows how to make this nest interchangeable.

**A legal swap with a parallel loop.** `for i: for j: A[i][j] = A[i-1][j] + A[i][j-1]` has distances $(1, 0)$ and $(0, 1)$. The swap maps them to $(0, 1)$ and $(1, 0)$, both positive, and the swapped nest gives the same array. For `A[i][j] = A[i-1][j] + 1` alone, the only distance is $(1, 0)$: the $j$ loop carries nothing. Kept inside, it is a vector loop. Moved outside, the distance becomes $(0, 1)$, the outer $j$ loop is a [DOALL loop](/doall-loop/), and each thread runs one column.

**Matrix multiplication orders.** In `C[i][j] = C[i][j] + A[i][k] * B[k][j]` the only dependences are on `C[i][j]`, with distance $(0, 0, 1)$ in the order $i, j, k$. A vector with one nonzero entry stays positive under every permutation, so all six orders of the three loops are legal, and each order keeps the additions into one `C[i][j]` in increasing $k$, so even the floating-point result is the same. They differ in speed: with the order $i, k, j$, the inner loop walks `B[k][j]` and `C[i][j]` with stride 1, while the order $i, j, k$ walks `B[k][j]` with stride $n$. [Blocked matrix multiplication](/blocked-matrix-multiplication/) goes further with [tiling](/loop-tiling/).

**Legal but unprofitable.** `for i = 0 to 63: for j = 0 to 63: A[i][j] = A[i][j] + 1` has no dependence between different iterations, so the swap is legal. Take a row-major array, lines of 8 elements and a fully associative LRU cache:

| cache size in lines | misses, $j$ inner | misses, $i$ inner |
|---|---|---|
| 32 | 512 | 4096 |
| 64 | 512 | 512 |

With $j$ inner, each line is loaded once: $4096 / 8 = 512$ misses. With $i$ inner and 32 lines, the 64 rows of one column do not fit, every line is gone before the next column needs it, and every access misses. With 64 lines the column of lines fits and the cost is the same. A compiler must therefore pair the legality test with a cost model, as the [Wolf-Lam algorithm](/wolf-lam-locality-algorithm/) does. The same swap applied to `s = s + A[j][i]` gives the opposite result: 4096 misses become 512.

## Variations

- **Loop permutation.** Any permutation $\sigma$ of a nest is legal if every permuted vector $(d_{\sigma(1)}, \dots, d_{\sigma(k)})$ is lexicographically positive. Every permutation is a sequence of adjacent swaps, but the intermediate nests need not be legal, so test the final vectors.
- **Interchange with reversal.** Reversing a loop negates its entry. A forbidden $(1, -1)$ becomes legal for interchange after the inner loop is reversed: $(1, 1)$ swaps to $(1, 1)$. This is one of the [unimodular transformations](/unimodular-transformations/).
- **Skew, then interchange.** [Skewing](/loop-skewing/) adds a multiple of the outer entry to the inner one, so that $(1, -1)$ becomes $(1, 0)$, and then the swap is legal.
- **Imperfect nests.** Statements between the two loop headers must first be moved inside, with a guard, or split off with [loop distribution](/loop-distribution/).
- **Tiling.** [Strip mining](/strip-mining/) a loop and interchanging the strip loop outward is the basic step of [loop tiling](/loop-tiling/).

## Pitfalls

- **Treating $*$ as $=$.** A direction vector $(<, *)$ contains $(<, >)$. Ignoring that case allows an illegal swap.
- **Scalar temporaries.** A scalar `t` assigned and used in the body gives dependences in every direction, including $(<, >)$, and blocks the swap. [Array privatization](/array-privatization/) or the expansion of `t` into an array removes them.
- **Copying the bounds.** In a triangular nest, swapping the headers without recomputing the bounds runs a different set of iterations.
- **Checking legality only.** A legal swap can raise the misses by a factor of 8 or more, as in the table above.
- **Reductions in floating point.** The test above keeps the order of the dependences. A compiler that also treats a reduction as free of dependences, to allow more orders, changes the order of the additions and the rounding of the result.

## Exercises

1. A nest has the distances $(1, -1)$ and $(0, 1)$. Is the interchange legal? *Answer.* No. $(1, -1)$ becomes $(-1, 1)$.
2. A nest has the distances $(1, 0)$, $(1, 1)$ and $(0, 1)$. Is the interchange legal, and which loop carries each dependence after it? *Answer.* Yes. The new vectors are $(0, 1)$, $(1, 1)$ and $(1, 0)$; the outer loop carries $(1, 1)$ and $(1, 0)$, the inner loop carries $(0, 1)$.
3. Give the bounds after the interchange of `for i = 1 to n: for j = 1 to i`. *Answer.* `for j = 1 to n: for i = j to n`.
4. A depth-3 nest has the distance $(0, 1, -1)$. Which of the two adjacent swaps are legal? *Answer.* Swapping loops 1 and 2 gives $(1, 0, -1)$, which is legal. Swapping loops 2 and 3 gives $(0, -1, 1)$, which is not.

## References
