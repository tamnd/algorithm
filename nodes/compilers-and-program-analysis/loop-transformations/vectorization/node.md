---
tag: K80AKR
kind: technique
slug: vectorization
name: Vectorization
aliases:
- auto-vectorization
- loop vectorization
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Turns loops or statement groups into SIMD instructions that process several data elements at once, when dependences allow.
prereqs: [data-dependence, loop-carried-dependence, dependence-distance-vector, strip-mining, doall-loop]
see_also: [allen-kennedy-algorithm, slp-vectorization, simd-within-a-register, loop-distribution, loop-interchange, parallel-reduction, dependence-testing, roofline-model]
sources:
  - paper: doi:10.1145/29873.29875
    title: Randy Allen and Ken Kennedy, Automatic translation of FORTRAN programs to vector form, ACM Transactions on Programming Languages and Systems 9(4), 1987, 491-542
    locator: the conditions for a statement to become a vector statement (no dependence cycle at the level of the loop) and the vector code generation procedure
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (parallelization and vectorization), Chapter 5 (enhancing fine-grained parallelism) and the chapter on short vector (SIMD) code
  - paper: doi:10.1145/7902.7904
    title: David A. Padua and Michael J. Wolfe, Advanced compiler optimizations for supercomputers, Communications of the ACM 29(12), 1986, 1184-1201
    locator: the sections on vectorization, strip mining and the dependence conditions for vector code
  - paper: doi:10.1145/349299.349320
    title: Samuel Larsen and Saman Amarasinghe, Exploiting superword level parallelism with multimedia instruction sets, PLDI 2000, 145-156
    locator: Section 1 and Section 2 (vector parallelism in loops against superword parallelism in basic blocks)
  - paper: doi:10.1145/1133981.1133997
    title: Dorit Nuzman, Ira Rosen and Ayal Zaks, Auto-vectorization of interleaved data for SIMD, PLDI 2006, 132-143
    locator: the loop vectorizer of GCC, accesses with constant strides that are powers of 2
---

Vectorization turns scalar code into vector code: one instruction works on several data elements, called *lanes*, at the same time. A vector machine of the 1970s and 1980s had long vector registers and pipelines; a modern processor has SIMD units with a fixed number of lanes, such as 4, 8 or 16. The compiler finds the work for these lanes in two places. *Loop vectorization* runs consecutive iterations of a loop in the lanes. [SLP vectorization](/slp-vectorization/) packs similar statements of one basic block into lanes. This page is about loops. The [Allen-Kennedy algorithm](/allen-kennedy-algorithm/) is the classic method for whole loop nests; the result below says when a single loop can run with a given number of lanes.

## In plain words

Picture a row of workers who each handle one item, all doing the same step at the same moment. A loop that does the same work for item 1, item 2, item 3 and so on fits this well, if no item needs the result of an item that is in the same group. The compiler groups the items in batches of the size of the row, and runs each step of the loop body on the whole batch. It can do this if every value that one item hands to a later item reaches it in a later batch, or at a later step of the same batch. A value that goes back to an earlier step and to an item of the same batch arrives too late, and the result is wrong.

## When it applies

- The loop body is a sequence of statements that does the same operations in every iteration. Branches must first become masks or selects (if-conversion).
- The subscripts are affine in the loop index, or the compiler can test the addresses at run time. Constant stride 1 is the best case; other strides need shuffles, gathers or scatters.
- The dependences carried by the loop allow it. With the statements in a fixed order, the rule below says exactly when strips of $VL$ iterations can run as vector steps.
- The data types fit the lanes, and the trip count is large enough that the vector loop, plus a scalar loop for the rest, is faster than the scalar loop alone.

## The template

Take a loop `for i = 1 to N` whose body is a straight sequence of statements $S_1, \dots, S_r$. Let $VL$ be the number of lanes.

```pseudo id=main
VECTORIZE(loop i = 1 to N, body S_1 ... S_r, VL)
L1  find the dependences of the loop and their distances
L2  order the statements so that each loop-independent dependence goes forward
L3  check that each carried dependence from S_p to S_q with p >= q has distance >= VL
L4  for s <- 1 to N step VL do                   ▷ strip mining
L5      t <- min(s + VL - 1, N)                  ▷ the last strip may be short
L6      for q <- 1 to r do
L7          run S_q for i = s to t as one vector step
```

A *vector step* reads all its operands, then writes all its results. On a real machine the short last strip in line L5 is a scalar remainder loop or a masked step. Line L2 is the topological order of the [Allen-Kennedy algorithm](/allen-kennedy-algorithm/) restricted to one loop. If line L3 fails, the loop is not vectorized as written; the Variations section lists the ways out.

**Theorem.** Assume that the statements are in an order where each loop-independent dependence goes from an earlier statement to a later one. If every carried dependence from $S_p(i)$ to $S_q(i + d)$, $d \ge 1$, with $p \ge q$ has $d \ge VL$, then the strip-mined vector code computes the same memory as the scalar loop.

*Proof.* The vector code puts the instance $S_q(i)$ in the step with key $(\lfloor (i - 1) / VL \rfloor, q)$, and runs the steps in lexicographic order of the keys. By the reordering theorem on the [legality page](/loop-transformation-legality/), it is enough that each dependence pair has its source in an earlier step than its sink, so that no pair is inside one step and every pair keeps its order. Take a pair from $S_p(i)$ to $S_q(i + d)$.

- If $d = 0$, the pair is loop independent, so $p < q$ by the order of line L2. The two instances are in the same strip, and step $p$ comes before step $q$.
- If $d \ge 1$ and $p < q$, the strip of $i + d$ is the same as the strip of $i$ or later. In the same strip, step $p$ comes before step $q$. In a later strip, all steps come later.
- If $d \ge 1$ and $p \ge q$, then $d \ge VL$ by assumption. The two indices differ by at least $VL$, so they are in different strips, and the strip of $i$ comes first.

So every pair keeps its order and no pair shares a step. $\square$

So a dependence distance of at least $VL$ is harmless, even on a dependence cycle: the source and the sink are never in the same strip. The rule is tight in most cases. If a carried dependence with $1 \le d < VL$ goes from $S_p$ to $S_q$ with $p > q$, then for the first iteration $i$ of a full strip both $i$ and $i + d$ are in that strip, and step $q$ runs the sink before step $p$ runs the source. If it is a flow or output dependence of a statement on itself ($p = q$, $d < VL$), the source and the sink are in one step, so the sink reads the old value or the two writes are not ordered. The one case the rule does not need is an anti-dependence of a statement on itself, as in `A[i] = A[i+1] + 1`: a vector step reads all of $A[i+1 \ldots i+VL]$ before it writes, so the old values are read, as in the scalar loop.

## Classic examples

**A plain loop.** `A[i] = B[i] * C[i] + D[i]` has no dependence. With $VL = 8$ it runs as one multiply-add over each 8 lanes, with a remainder loop of at most 7 iterations.

**A distance of 2.** Take

```
for i = 0 to 7:
  A[i+2] = A[i] + 1
```

with $A$ zero at the start. The flow dependence from iteration $i$ to iteration $i + 2$ has distance 2. The scalar loop gives $A = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]$. With $VL = 2$, each strip reads cells that the strip before wrote, and the result is the same. With $VL = 4$, the first strip reads $A[0 \ldots 3]$, which are all zero, and the second strip reads $A[4], A[5]$ written by the first strip but $A[6], A[7]$ not yet written. The result is $[0, 0, 1, 1, 1, 1, 2, 2, 1, 1]$, which is wrong. The loop vectorizes for 2 lanes and not for 4.

**The order of the statements.**

```
for i = 1 to N:
  S1: C[i] = A[i-1] * 2
  S2: A[i] = B[i] + 1
```

The flow dependence goes from $S_2(i - 1)$ to $S_1(i)$, with distance 1 and $p = 2 > q = 1$. In this order the rule fails, and a vector step of $S_1$ would read old values of $A$. No loop-independent dependence ties the two statements, so line L2 may swap them. In the order $S_2, S_1$ the dependence goes forward, and both statements become vector steps.

**A recurrence.** `A[i] = A[i-1] * x + B[i]` has a flow dependence of distance 1 of the statement on itself. It is not vectorizable for any $VL \ge 2$. Each value needs the one before.

**A reduction.** `s = s + A[i]` has a flow dependence of distance 1 on $s$. The compiler can still vectorize it as a [parallel reduction](/parallel-reduction/): it keeps $VL$ partial sums, one per lane, and adds them at the end. This is a different order of additions. For integers it gives the same result; for floating point numbers it may not, so compilers do it only when the user allows reassociation.

## Variations

- **Breaking the cycle.** Scalar expansion, node splitting, loop distribution and [loop interchange](/loop-interchange/) remove a short dependence cycle from the innermost loop or move a dependence-free loop inward. The Allen-Kennedy algorithm does the distribution step for whole nests.
- **Outer-loop vectorization.** The lanes run iterations of an outer loop, and the inner loop runs in each lane. This helps when the inner loop is short or carries a dependence.
- **Masked and predicated code.** A branch in the body becomes a mask; each lane computes both sides or only the active side. Machines with mask registers also use masks for the short last strip.
- **Vector-length agnostic code.** On machines where the number of lanes is fixed only at run time, such as Arm SVE and the RISC-V vector extension, the loop asks the hardware for the length of each strip. A carried distance $d$ is then safe only if $d$ is at least the largest possible length, or the code limits the strip length to $d$.
- **Run-time checks.** When two pointers may overlap, the compiler emits a test of the address ranges and two versions of the loop, the vector one for the case without overlap.
- **Interleaved data.** Accesses with a constant stride, such as the real and imaginary parts of complex numbers, need loads of several vectors and shuffles; Nuzman, Rosen and Zaks give a scheme for strides that are powers of 2.
- **Statements instead of iterations.** [SLP vectorization](/slp-vectorization/) packs isomorphic statements of one block, which also covers a loop after [loop unrolling](/loop-unrolling/).

## Pitfalls

- **Ignoring the distance.** A cycle of carried dependences does not always stop vectorization, and a carried dependence with a small distance does not always allow it. Both the distance and the direction relative to the statement order count.
- **Aliasing.** In C, two pointer arguments may point into the same array. Without `restrict` or a run-time check, the compiler must assume a dependence of unknown distance.
- **Floating point reductions.** Partial sums change the order of additions, so the result may differ in the last bits or more. Do not vectorize them without permission to reassociate.
- **Speculative loads.** A vector load of a full strip may touch memory past the end of an array, or past a point where the scalar loop would have stopped, for example at a `break`. Masked loads or a remainder loop avoid faults.
- **Assuming faster code.** Gathers, scatters, shuffles and the remainder loop cost time. For short loops or irregular accesses, the vector code can be slower than the scalar code. The [roofline model](/roofline-model/) shows when memory bandwidth, not arithmetic, limits the loop.
- **Alignment.** Some machines need vector loads at aligned addresses, or run them faster there. Peeling a few iterations before the vector loop fixes the alignment of one array, not of all of them.

## Exercises

1. For `A[i+3] = A[i] * 2`, find the largest $VL$ for which the loop vectorizes as written.
2. Show that the loop `S1: A[i] = B[i] + 1; S2: B[i+1] = A[i] * 2` has a cycle of dependences. Can a reordering of the statements make it vectorizable for $VL = 4$?
3. Explain why `A[i] = A[i+1] + 1` vectorizes, while `A[i+1] = A[i] + 1` does not. Which kinds of dependences are they?
4. A loop has one carried dependence from $S_3$ to $S_1$ with distance 8 and one from $S_1$ to $S_3$ with distance 1. For which $VL$ does it vectorize?
5. Show that the theorem stays true if the strips have different lengths, as long as each strip has at most $VL$ iterations.

## References
