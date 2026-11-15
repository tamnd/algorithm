---
tag: 0RJ20A
kind: technique
slug: loop-fusion
name: Loop fusion
aliases:
- loop jamming
- loop merging
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Merges adjacent loops with the same bounds into one loop, which improves reuse of data and lowers loop overhead.
prereqs: [data-dependence, loop-carried-dependence, loop-transformation-legality]
see_also: [loop-distribution, loop-interchange, loop-tiling, doall-loop, array-privatization, locality-of-reference, register-allocation-problem, loop-unrolling]
sources:
  - paper: doi:10.1007/3-540-57659-2_18
    title: Ken Kennedy and Kathryn S. McKinley, Maximizing loop parallelism and improving data locality via loop fusion and distribution, Languages and Compilers for Parallel Computing (LCPC 1993), Lecture Notes in Computer Science 768, Springer, 1994, 301-320
    locator: the fusion graph with fusion-preventing edges, fusion of parallel loops without loss of parallelism, and the proof that fusion for the most data reuse with weighted edges is NP-hard
  - url: "https://www.cs.utexas.edu/~mckinley/papers/tfusion-1993.pdf"
    title: Ken Kennedy and Kathryn S. McKinley, Typed fusion with applications to parallel and sequential code generation, Technical Report TR93-208, Rice University, 1993
    locator: Section 2 (fusion is illegal when a loop-independent dependence becomes a backward carried dependence), the O((N + E)T) ordered typed fusion algorithm, and the NP-hardness of typed fusion with more than two types
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 6 (Creating Coarse-Grained Parallelism), loop fusion and fusion-preventing dependences; Section 8.6 (Loop Fusion for Register Reuse)
---

Loop fusion merges two adjacent loops with the same iteration range into one loop whose body is the body of the first loop followed by the body of the second. The work is the same, but the order changes: before, every iteration of the first loop ran before any iteration of the second; after, they alternate. Fusion is legal exactly when no [dependence](/data-dependence/) goes from iteration $i$ of the first loop to an earlier iteration $j < i$ of the second loop. Such a dependence is called *fusion-preventing*: it is a loop-independent dependence between the two loops that would become a backward [carried dependence](/loop-carried-dependence/) in the fused loop. The test is about the dependences between the loops, so two loops that are each fully parallel can still be impossible to fuse. When fusion is legal, a value that the first body writes is often read by the second body in the same iteration, while it is still in a register or in cache. Fusion is the inverse of [loop distribution](/loop-distribution/).

## In plain words

Two loops that walk the same range one after the other can often walk it together: at each step, do the work of the first loop and then the work of the second. Each piece of data is then used twice while it is close at hand, instead of being fetched again on a second pass. The danger is in what the second loop reads. Before the merge, the first loop had finished completely when the second loop began, so the second loop could read any result of the first. After the merge, the second loop at step 5 runs before the first loop reaches step 6. If it needs a value that step 6 of the first loop writes, it reads an old value. The merge is safe when the second loop at each step only needs results of the first loop from the same step or earlier steps.

## When it applies

Take two loops

```
for i = L to U: S1(i)
for i = L to U: S2(i)
```

where S1 and S2 stand for the bodies. The conditions are:

- **(F1) Same range.** Both loops run the same iterations $L, \dots, U$ in the same order. Loops with ranges that differ by a few iterations can be made to match by peeling those iterations off.
- **(F2) Adjacent.** No statement runs between the two loops, or the statements between them have no dependence with the second loop and can be moved before the first.
- **(F3) No fusion-preventing dependence.** No dependence from S1 at iteration $i$ to S2 at iteration $j$ has $j < i$.

Dependences inside S1 or inside S2 do not matter for legality. A dependence from S2 to S1 cannot exist in the original program, because every instance of S1 runs before every instance of S2.

## The template

```pseudo id=main
FUSE(for i = L to U: S1(i), for i = L to U: S2(i))
L1  if the two loops do not have the same range then
L2      return "not conformable: peel or align first"
L3  for each dependence from S1(i) to S2(j) do
L4      if j < i then
L5          return "illegal: fusion-preventing dependence"
L6  return for i = L to U: S1(i); S2(i)
```

The holes are the two bodies and their common range. For dependences with a constant distance, the test of line L4 reads: S1 writes an element at iteration $i$ that S2 reads or writes at $i - c$ with $c > 0$, or the other way round. With the array subscripts `A[i + a]` in S1 and `A[i + b]` in S2, iteration $i$ of S1 and iteration $j$ of S2 touch the same element when $j = i + a - b$, so the pair is fusion-preventing exactly when $a > b$.

**Theorem.** Under (F1) and (F2), fusion keeps every dependence pair in order if and only if (F3) holds.

*Proof.* Write an instance as $S1(i)$ or $S2(i)$. The fused loop runs them in the order: $S1(i)$ before $S2(i)$, and every instance of iteration $i$ before every instance of iteration $i' > i$. Take a dependence pair.

- Both ends in S1. The fused order restricted to the instances of S1 is $S1(L), S1(L+1), \dots$, the same as in the first loop. The pair keeps its order. The same holds for S2.
- Source $S1(i)$, sink $S2(j)$. In the fused order, $S1(i)$ runs first if $j \ge i$: in the same iteration S1 comes first, and in a later iteration everything comes later. If $j < i$, iteration $j$ ends before iteration $i$ starts, so $S2(j)$ runs first.
- Source in S2, sink in S1. This is not possible, as said above.

So all pairs keep their order exactly when no pair has source $S1(i)$ and sink $S2(j)$ with $j < i$. By Theorem 1 of the [legality page](/loop-transformation-legality/), the fused loop then gives the same result. $\square$

**Profit.** The cost model is the memory traffic, or the number of loads. A value written in S1 and read in S2 at the same iteration needs no second load, and if the array is a temporary that nothing else reads, it can become a scalar (*array contraction*), which removes the array from memory. The loop control runs once instead of twice. The costs are more registers for the larger body, and possibly lost parallelism: if the fused loop carries a dependence between S1 and S2, it is sequential even when both loops were parallel.

## Classic examples

**Two parallel loops that cannot be fused.**

```
for i = 1 to n: A[i] = B[i] + 1
for i = 1 to n: C[i] = A[i+1] * 2
```

Each loop is a [DOALL loop](/doall-loop/): no iteration of either loop depends on another iteration of the same loop. Between the loops, S2 at iteration $i$ reads `A[i+1]`, which S1 writes at iteration $i + 1$: a dependence from $S1(i+1)$ to $S2(i)$, with $j < i$. In the fused loop, $S2(i)$ reads `A[i+1]` one iteration before $S1(i+1)$ writes it. With $n = 4$, `B = [1, 2, 3, 4]` and `A` all zero at the start, the original code gives `C = [6, 8, 10, 0]` and the fused loop gives `C = [0, 0, 0, 0]`. The fix is *alignment*: shift S2 by one iteration, so that $S2(i - 1)$ runs with $S1(i)$, and peel the ends:

```
A[1] = B[1] + 1
for i = 2 to n:
  A[i] = B[i] + 1
  C[i-1] = A[i] * 2
C[n] = A[n+1] * 2
```

Now the read of `A[i]` follows its write in the same iteration, and the fused loop is still parallel.

**Fusion that is legal but costs parallelism.** If S2 is `C[i] = A[i-1] * 2`, the dependence goes from $S1(i - 1)$ to $S2(i)$, forward, and fusion is legal. The fused loop carries this dependence with distance 1, so it is no longer a DOALL loop. A compiler that wants parallel loops treats such a dependence as fusion-preventing too, as Kennedy and McKinley do when they fuse only loops of the same type.

**Fusion for reuse.** For `A[i] = B[i] + 1` followed by `C[i] = A[i] * 2`, the dependence has distance 0, fusion is legal, and the fused loop is parallel. Before fusion, the two loops move $4n$ elements through memory: read `B`, write `A`, read `A` again, write `C`. After fusion, `A[i]` is still in a register when S2 reads it: $3n$. If `A` is dead after the loop, it becomes a scalar, and the traffic is $2n$. Compilers for array languages fuse the loops of consecutive array statements for this reason, and GPU compilers fuse kernels so that the second kernel does not read the temporary back from global memory.

## Variations

- **Fusion of many loops.** A program has a sequence of loops and a choice of which ones to fuse. Kennedy and McKinley build a *fusion graph* with one node per loop, dependence edges and fusion-preventing edges, and they show that the choice that maximizes reuse, with weights on the edges, is NP-hard. Their typed fusion report gives an $O((N + E)T)$ algorithm for $N$ loops, $E$ edges and $T$ types of loops ranked by priority, and shows that the problem is NP-hard when $T > 2$ types have no priority order.
- **Fusion with alignment and peeling.** Shift one loop by a constant, as in the example, to turn a fusion-preventing dependence into a loop-independent one. The [polyhedral model](/polyhedral-model/) chooses such shifts as part of a schedule.
- **Fusion of nests.** Two nests with the same bounds on several levels fuse level by level. The test uses the full distance vector between the two bodies: it must be lexicographically nonnegative.
- **Unroll and jam.** Unrolling an outer loop and fusing the copies of the inner loop, on the [loop unrolling](/loop-unrolling/) page, is fusion inside one nest.

## Pitfalls

- **Testing each loop alone.** That both loops are parallel says nothing about fusion, as the first example shows. Only the dependences between the two bodies decide it.
- **Forgetting the anti-dependences.** A read in S1 followed by a write in S2 is a dependence too. If S1 reads `A[i-1]` and S2 writes `A[i]`, the read in $S1(i)$ and the write in $S2(i - 1)$ form a pair with $j = i - 1 < i$. After fusion the write runs first and S1 reads the new value: fusion-preventing. If S1 reads `A[i+1]` instead, the pair is $S1(i)$ and $S2(i + 1)$, and fusion is legal.
- **Losing parallelism by accident.** A forward carried dependence keeps fusion legal but makes the fused loop sequential. Check what the fused loop is for.
- **Different trip counts.** Fusing loops whose ranges differ without peeling runs extra iterations or skips some.
- **Register pressure.** A large fused body can need more registers than the machine has, and the spills cost more than the saved loads.

## Exercises

1. Can `for i: A[i] = B[i] * 2` and `for i: B[i] = C[i] + 1` be fused? *Answer.* Yes. The pair is the read of `B[i]` in $S1(i)$ and the write of `B[i]` in $S2(i)$, an anti-dependence with $j = i$. In the fused body the read still comes first.
2. Can `for i: A[i] = B[i] * 2` and `for i: B[i] = C[i] + A[i-1]` be fused, and is the fused loop parallel? *Answer.* The flow dependence goes from $S1(i-1)$ to $S2(i)$, forward, and the anti-dependence on `B[i]` has $j = i$, so fusion is legal. The fused loop carries the flow dependence with distance 1 and is not parallel.
3. S1 writes `A[2i]` and S2 reads `A[i]`. Is fusion legal? *Answer.* $S2(j)$ reads the element that $S1(i)$ wrote when $j = 2i$. For $i \ge 1$, $j = 2i > i$, so every dependence is forward and fusion is legal on the range $1, \dots, n$.
4. Give the alignment for `A[i] = B[i] + 1` followed by `C[i] = A[i+2] - 1`. *Answer.* Shift S2 by 2: in iteration $i$ run S1 for $i$ and S2 for $i - 2$. Peel two iterations of S1 at the start and two of S2 at the end.

## References
