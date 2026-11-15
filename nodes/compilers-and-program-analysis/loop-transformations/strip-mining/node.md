---
tag: QXEEEZ
kind: technique
slug: strip-mining
name: Strip mining
aliases:
- loop sectioning
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Splits one loop into an outer loop over strips and an inner loop over a fixed number of iterations, as for vector registers.
prereqs: [data-dependence, dependence-distance-vector]
see_also: [loop-unrolling, loop-tiling, loop-interchange, vectorization, parallel-for, doall-loop, loop-transformation-legality]
sources:
  - paper: doi:10.1145/76263.76337
    title: Michael Wolfe, More iteration space tiling, Proceedings of Supercomputing '89, ACM, 1989, 655-664
    locator: strip mining as the one-loop case, and tiling as strip mining followed by loop interchange
  - book: isbn:9780805327304
    title: Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996
    locator: the chapter on loop restructuring, strip mining and its use for vector registers and for tiling
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 9 (Managing Cache), strip-mine-and-interchange as the basic step of blocking
---

Strip mining splits one loop into two: an outer loop that steps over *strips* of $B$ consecutive iterations, and an inner loop that runs the iterations of one strip. The last strip is shorter when $B$ does not divide the trip count. The iterations run in the same order as before, so strip mining is always legal and changes no [data dependence](/data-dependence/). It gives no speedup by itself. Its value is the new loop level it creates: the inner strip loop can become one vector instruction of length $B$ ([vectorization](/vectorization/)), a chunk of work for one thread, or, after [loop interchange](/loop-interchange/) moves the strip loop outward, a tile of a [tiled](/loop-tiling/) nest.

## In plain words

Think of reading a long list of numbers to a person who can only keep four of them in mind at a time. You read them four by four, in the same order as before, and the last group may be smaller. Nothing about the list or the order changes, so the result is the same. What changes is that the work now comes in groups of a fixed size, and other tools can use that. A processor with registers that hold four numbers can do one group in one step, and a cache can keep one group while it is in use. Splitting into groups is safe. Doing a group all at once is a separate question.

## When it applies

Take a counted loop `for i = L to U: BODY(i)` with step 1, and a strip size $B \ge 1$. The conditions are the same as for [loop unrolling](/loop-unrolling/): $L$ and $U$ are evaluated once, BODY does not assign $i$, and the bound $is + B - 1$ is computed without overflow. $B$ must be a positive constant or a value that does not change during the loop. No dependence test is needed for the split itself.

A loop with step $s > 1$ is first normalized to step 1, so that the strips count iterations and not index values.

## The template

```pseudo id=main
STRIP-MINE(for i = L to U: BODY(i), strip size B)
L1  for is = L to U step B do               ▷ strip loop: is = L, L + B, L + 2B, ...
L2      for i = is to min(is + B - 1, U) do  ▷ element loop: at most B iterations
L3          BODY(i)
```

The holes are the body, the bounds $L$ and $U$, and the strip size $B$. When $B$ divides the trip count $U - L + 1$, the `min` is not needed and every strip has exactly $B$ iterations. Otherwise a compiler often runs the full strips with the simple bound $is + B - 1$ and handles the last, short strip in a separate copy of the loop, the same way as the remainder loop of unrolling.

**Legality.** The strips are the sets $\{is, \dots, \min(is + B - 1, U)\}$ for $is = L, L + B, L + 2B, \dots \le U$. Every $i$ with $L \le i \le U$ is in exactly one strip, the one with $is = L + B \lfloor (i - L)/B \rfloor$, because $is \le i \le is + B - 1$ holds for this value and for no other multiple. The strips run in increasing order of $is$, and inside a strip $i$ increases. So $i < i'$ implies that $i$ runs first: either both are in one strip and the inner loop runs $i$ first, or the strip of $i$ has a smaller $is$ and the outer loop runs it first. The new code therefore runs $\mathrm{BODY}(L), \dots, \mathrm{BODY}(U)$ in the original order, and from the same state it reaches the same final state. Every dependence keeps its source before its sink.

**In the distance notation.** The new nest has iteration vectors $(is, i)$. A dependence of the original loop with distance $d > 0$ from $i$ to $i + d$ has, in the new nest, the distance $(is' - is, d)$, where $is'$ is the strip of $i + d$. The first entry is $0$ or positive, so the new [distance vector](/dependence-distance-vector/) is lexicographically positive, as the proof says. The first entry depends on where $i$ is in its strip, so one old distance gives several new ones. For $d = 1$ and $B = 4$ the new distances are $(0, 1)$ inside a strip and $(4, 1)$ across the boundary of two strips.

**Profit.** None by itself: the loop runs the same work with a little more control code. The profit comes from the step that follows.

## Classic examples

**Strips of 4 over 10 iterations.** For `for i = 1 to 10`, with $B = 4$:

| strip | $is$ | inner bound $\min(is + 3, 10)$ | iterations |
|---|---|---|---|
| 1 | 1 | 4 | 1, 2, 3, 4 |
| 2 | 5 | 8 | 5, 6, 7, 8 |
| 3 | 9 | 10 | 9, 10 |

The order of the iterations is $1, 2, \dots, 10$, as before.

**Vector code.** On a machine with vector registers of length 4, the loop `for i = 1 to n: A[i] = B[i] + C[i]` is strip-mined with $B = 4$, and the inner loop becomes one vector load of each operand, one vector add and one vector store. Here a second condition enters, because the vector statement does not run the four iterations one by one: it reads all four operands before it writes any result. That is legal for this loop, which has no loop-carried dependence. For `A[i] = A[i-3] + 1` it is not legal with $B = 4$: in the strip $1, \dots, 4$, iteration 4 reads $A[1]$, which iteration 1 of the same strip writes, and the vector load reads the old value. With $B = 3$ every read of a strip refers to an element that an earlier strip wrote, and the vector code is correct. The strip mining is legal in both cases. The vector execution of a strip is a separate step, with its own condition, given on the [vectorization](/vectorization/) page.

**Chunks for threads.** A [DOALL loop](/doall-loop/) of $n$ iterations is strip-mined with $B = \lceil n/p \rceil$ for $p$ threads, and the strip loop becomes a [parallel for](/parallel-for/): thread $t$ runs strip $t$. Each thread then works on a contiguous range of the arrays, which keeps cache lines from being shared between threads.

**The first half of tiling.** In [blocked matrix multiplication](/blocked-matrix-multiplication/), each of the loops $i$, $j$ and $k$ is strip-mined, and the three strip loops are moved outward with interchange. The interchange is the step that needs a dependence test, given on the [loop tiling](/loop-tiling/) page.

## Variations

- **Strip size equal to the vector length.** For vector machines and SIMD units, $B$ is the number of elements a vector register holds, and the short last strip is done with a mask or with scalar code.
- **Strip mining with alignment.** The first strip is made shorter, so that the following strips start at an address that is a multiple of the vector size. This is strip mining with a shifted origin.
- **Strip mining a nest.** Strip-mine each loop of a nest and then move the strip loops outward. That is [loop tiling](/loop-tiling/).
- **Unknown strip size.** On vector machines with a vector length register, $B$ is read at run time, and the bound $\min(is + B - 1, U)$ is computed once per strip.

## Pitfalls

- **Missing `min` in the inner bound.** With `for i = is to is + B - 1`, the last strip runs past $U$ when $B$ does not divide the trip count.
- **Running the strip as a vector without a check.** The split keeps the order, but a vector instruction does not. A flow dependence with a distance less than $B$ makes the vector form wrong, as in the example `A[i] = A[i-3] + 1` with $B = 4$.
- **Expecting a cache gain from the split alone.** The order of the memory accesses does not change, so the cache misses do not change. Locality improves only when another loop is moved inside the strip loop, as in tiling.
- **Running the strip loop in parallel.** Strip mining does not remove a loop-carried dependence. The strips of a loop with a carried dependence must still run one after the other.

## Exercises

1. Strip-mine `for i = 3 to 17` with $B = 5$. List the strips. *Answer.* $is = 3, 8, 13$; the strips are $3..7$, $8..12$ and $13..17$, all full, because the trip count is $15$.
2. In which strip is $i = 22$ for $L = 1$ and $B = 8$? *Answer.* $is = 1 + 8 \lfloor 21/8 \rfloor = 17$, so the strip $17..24$, the third one.
3. A loop has a flow dependence with distance 5. What is the largest strip size for which each strip can run as one vector statement? *Answer.* $5$. Every read in a strip of length at most 5 refers to an element written at least 5 iterations earlier, so in an earlier strip.
4. Strip-mine a loop with full strips and then interchange the two new loops. When is the result legal? *Answer.* The new outer loop runs over the position $c = i - is$ from $0$ to $B - 1$, and the inner loop over the strips, so the order is $L, L + B, L + 2B, \dots, L + 1, L + 1 + B, \dots$. A dependence with distance $d$ that is a multiple of $B$ keeps $c$ and goes to a later strip, so it keeps its order. If $d$ is not a multiple of $B$, a source with $c \ge B - (d \bmod B)$ has its sink at a smaller position, and the sink runs first. So, for a loop with enough strips, the result is legal exactly when every loop-carried distance is a multiple of $B$.

## References
