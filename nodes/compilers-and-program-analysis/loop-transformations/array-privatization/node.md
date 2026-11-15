---
tag: SY7S7N
kind: technique
slug: array-privatization
name: Array privatization
aliases:
- privatization
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Gives each iteration or thread its own copy of a scratch array written before read in each iteration, removing false dependences.
prereqs: [data-dependence, loop-carried-dependence, reaching-definitions, live-variable-analysis]
see_also: [loop-distribution, doall-loop, parallel-for, feautrier-array-dataflow, loop-interchange, practical-dependence-tests, loop-fusion, dependence-testing]
sources:
  - paper: doi:10.1007/3-540-57659-2_29
    title: Peng Tu and David Padua, Automatic array privatization, Languages and Compilers for Parallel Computing (LCPC 1993), Lecture Notes in Computer Science 768, Springer, 1994, 500-521
    locator: the privatizability condition (no upward-exposed use of the array in an iteration), the data flow analysis over array sections that computes it, and the last-value copy-out
  - title: Zhiyuan Li, Array privatization for parallel execution of loops, Proceedings of the 6th International Conference on Supercomputing (ICS), Washington, 1992, 313-322
    locator: privatizable arrays in loops, defined by reads that are covered by writes of the same iteration, and their effect on the parallel loops of benchmark programs
  - paper: doi:10.1145/158511.158515
    title: Dror E. Maydan, Saman P. Amarasinghe and Monica S. Lam, Array-data flow analysis and its use in array privatization, Proceedings of the 20th ACM Symposium on Principles of Programming Languages (POPL), 1993
    locator: exact array data flow (the last write that reaches each read) used to decide which arrays can be made private, and the values to copy out
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 6 (Creating Coarse-Grained Parallelism), private variables and scalar expansion as ways to remove carried dependences on temporaries
---

Array privatization gives each thread of a parallel loop its own copy of an array that the loop uses as scratch space. It applies when, in every iteration, each element that the iteration reads has been written earlier in the same iteration. Then no iteration ever reads a value that another iteration produced, and every [dependence](/data-dependence/) on the array that the loop carries is an anti or output dependence caused only by the reuse of the same memory. A private copy per thread removes these dependences, and the loop can become a [DOALL loop](/doall-loop/). If the array is used after the loop, the values of the last iteration in the original order are copied back. For a scalar temporary the same idea is old and common; for arrays the hard part is the analysis, which must prove that the writes of an iteration cover its reads, element by element.

## In plain words

Picture a team of cooks who share one small whiteboard. Each cook, for each dish, first writes the list of steps on the board and then reads it while cooking. Because they share the board, they must take turns, even though no cook ever needs what another cook wrote. Give each cook a private board, and they can all cook at the same time. This is safe because each cook always writes before reading, so nothing on the board ever comes from someone else. It is not safe if a cook sometimes skips the writing and reads what is left on the board, because then the dish depends on who used the board last.

## When it applies

Take a loop `for i = L to U` and an array `T` used in its body. For an iteration $i$, let

- $W(i)$ be the set of elements of `T` that iteration $i$ writes, on every path through the body, before a given point, and
- $E(i)$, the *upward-exposed reads*, be the set of elements that iteration $i$ may read at a point where the element has not yet been written in the same iteration.

The conditions are:

- **(P1) No upward-exposed read.** $E(i) = \emptyset$ for every $i$. Every read of an element of `T` follows a write of that element in the same iteration, on every path.
- **(P2) Values after the loop.** If `T` is [live](/live-variable-analysis/) after the loop, the code must restore the values that the original loop leaves in `T`. When every iteration writes the same set of elements, these are the values of iteration $U$.
- **(P3) No aliases.** `T` is not reachable under another name in the body, and its address does not escape to code that runs in another iteration.

A scalar is the case of an array with one element. Making a scalar private needs only that every use in the body is reached by a definition in the same iteration, which [reaching definitions](/reaching-definitions/) on the body answer directly.

## The template

```pseudo id=main
PRIVATIZE(loop for i = L to U with body BODY, array T)
L1  compute E, the upward-exposed reads of T in BODY        ▷ array region analysis
L2  if E is not empty then
L3      return "not privatizable: an iteration reads a value from another one"
L4  allocate one copy T_p of T for each thread
L5  replace T by T_p in BODY
L6  if T is live after the loop then
L7      after the loop, copy into T the values that the last writing iteration left
L8  drop every dependence on T carried by the loop
```

The holes are the loop, the array, and the precision of the analysis in line L1. Line L1 needs sets of array elements, not just yes or no: Tu and Padua compute them as array sections, and Maydan, Amarasinghe and Lam compute for each read the exact last write that reaches it. A conservative answer, an $E$ that is too large, only loses the chance to make the loop parallel.

**Theorem.** Under (P1) and (P3), each read of `T` in the loop gets the same value when each thread uses its own copy, for any assignment of iterations to threads and any interleaving of the threads, as long as each thread runs its iterations one at a time.

*Proof.* Go through the statements of iteration $i$ in program order, and assume that every value computed so far is the same in both versions. Take a read of element $e$. By (P1), iteration $i$ has already written $e$; let $w$ be its last write of $e$ before the read. In the original loop, the other iterations run entirely before or entirely after iteration $i$, so no write of $e$ falls between $w$ and the read, and the read gets the value of $w$. In the private version, iteration $i$ runs on one thread, and while it runs, only this iteration touches the thread's copy; by (P3) nothing else reaches it. So again no write of $e$ falls between $w$ and the read, and the read gets the value of $w$. By the assumption, $w$ wrote the same value in both versions. So the read gets the same value, and the induction continues. $\square$

So the carried anti and output dependences on `T` disappear, and no carried flow dependence on `T` existed in the first place, because every read gets its value from its own iteration. If no other dependence is carried, the loop is parallel.

**Profit.** The gain is the parallel loop. The cost is $p$ copies of `T` for $p$ threads, and the copy-out. One copy per thread is enough: one copy per iteration, as in *scalar expansion*, would also work but needs $n$ copies.

## Classic examples

**A scratch row.**

```
for i = 1 to n:
  for j = 1 to m:
    T[j] = A[i][j] * 2
  for j = 1 to m:
    B[i][j] = T[j] + T[m+1-j]
```

Each iteration of the $i$ loop writes `T[1..m]` and then reads `T[j]` and `T[m+1-j]`, both in `1..m`. Every read is covered, so $E(i) = \emptyset$. Without the private copy, the $i$ loop carries an output dependence on `T` (every iteration writes the same elements) and an anti-dependence (iteration $i$ reads `T[j]` before iteration $i + 1$ overwrites it), so it is sequential. With one copy of `T` per thread, the $i$ loop is a [parallel for](/parallel-for/) over the rows. A dependence test that looks only at the subscripts, like the [GCD test](/gcd-test/), sees the same subscripts `T[j]` in every iteration and reports the dependences; it cannot tell that the reads are covered. That needs the flow analysis.

**A conditional write.**

```
for i = 1 to n:
  if c[i] > 0:
    T[1] = x[i]
  y[i] = T[1]
```

When `c[i] <= 0`, iteration $i$ reads `T[1]` without writing it, and gets the value of the last iteration that wrote it. This is a real carried flow dependence: $E(i) = \{T[1]\}$ on that path, and `T` is not privatizable. Making it private would give each thread the last value of its own iterations, which differs from the original. If the read is under the same condition, with both `T[1] = x[i]` and `y[i] = T[1]` inside the `if`, the read is covered on its path and `T` is privatizable.

**Partial coverage.** If the first inner loop writes `T[1..m-1]` but the second reads `T[m]`, element `T[m]` is upward exposed in every iteration. Its value comes from before the loop, and no iteration writes it, so the loop can still run in parallel with `T[m]` shared and read-only, or with a private copy initialized from the original `T[m]`.

## Variations

- **Copy-in.** When some reads are upward exposed but read only values from before the loop, each private copy starts as a copy of the original array.
- **Last value.** When different iterations write different elements, the copy-out needs, for each element, the last iteration that wrote it. A simple version: run the last iteration again on the shared array after the loop, which is correct when every iteration writes the same set of elements.
- **Expansion instead.** For [loop distribution](/loop-distribution/), the scratch array must survive between the new loops, so each iteration gets its own row of a larger array: `T[j]` becomes `T2[i][j]`.
- **Exact data flow.** [Array data flow analysis](/feautrier-array-dataflow/) gives, for each read, the exact write that produced its value. If that write is always in the same iteration, the array is privatizable; this is the approach of Maydan, Amarasinghe and Lam.

## Pitfalls

- **Conditional writes.** A write under a condition does not cover a read outside it, as in the second example. Treat a write as covering only on the paths where it surely happens.
- **Forgetting the copy-out.** If the array is read after the loop, the shared copy must get the final values. The values of an arbitrary thread are wrong.
- **Aliased arrays.** If `T` and another name refer to the same memory, writes through the other name are not seen by the analysis.
- **Coverage across the inner loop bounds.** Proving that `T[m+1-j]` with $1 \le j \le m$ stays inside `1..m` needs the inner loop bounds and symbolic reasoning; a test that gives up there loses the parallel loop, not correctness.
- **Assuming any temporary is private.** An accumulator like `s = s + A[i]` reads the value of the previous iteration. That is a reduction, not a scratch value, and it needs a different transformation.

## Exercises

1. Is `T` privatizable in `for i: T[1] = A[i]; T[2] = B[i]; C[i] = T[1] * T[2]`? *Answer.* Yes. Both reads follow writes of the same elements in the same iteration.
2. Is `T` privatizable in `for i: C[i] = T[1]; T[1] = A[i]`? *Answer.* No. The read of `T[1]` comes first and gets the value of the previous iteration: a carried flow dependence.
3. In the scratch row example, $n = 1000$ and the loop runs on 8 threads. How many copies of `T` does array privatization need, and how many does scalar expansion need? *Answer.* 8 and 1000.
4. The loop of the first example also needs `T` after the loop. What does the copy-out contain? *Answer.* The values of iteration $n$: `T[j] = A[n][j] * 2` for every $j$.

## References
