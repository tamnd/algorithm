---
tag: EWRA39
kind: definition
slug: doall-loop
name: DOALL loop
area: compilers-and-program-analysis/loop-transformations
level: core
summary: A loop that carries no data dependence at its own level, so its iterations may run in any order or in parallel with the same result.
prereqs: [loop-carried-dependence, loop-transformation-legality]
see_also: [parallel-for, doacross-parallelization, vectorization, allen-kennedy-algorithm, array-privatization, parallel-reduction, loop-distribution, lamport-hyperplane-method]
sources:
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (the section on parallelization and vectorization, where a loop that carries no dependence can run in parallel) and Chapter 6 (creating coarse-grained parallel loops by privatization, distribution, alignment and interchange)
  - paper: doi:10.1145/7902.7904
    title: David A. Padua and Michael J. Wolfe, Advanced compiler optimizations for supercomputers, Communications of the ACM 29(12), 1986, 1184-1201
    locator: the sections on DOALL loops, DOACROSS loops and the dependence conditions for each
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 11 (Section 11.7 on synchronization-free parallelism and Section 11.8 on synchronization between parallel loops)
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapters on data dependence and on parallel loops (DOALL and DOACROSS execution)
---

A DOALL loop is a loop that carries no [data dependence](/data-dependence/) at its own level: no dependence goes from one of its iterations to another iteration of the same loop instance. So its iterations may run in any order, or at the same time, and every statement instance still reads the same values as in the sequential run. A compiler marks such a loop as a [parallel for](/parallel-for/) loop. The test is the absence of a [loop-carried dependence](/loop-carried-dependence/) at the level of the loop, which comes from [dependence testing](/dependence-testing/).

## Definition

Take a loop nest in the notation of the loop pages. A statement instance is $S(\vec{i})$, the iteration vector $\vec{i} = (i_1, \dots, i_k)$ runs in lexicographic order $\prec$, and a dependence from $S(\vec{i})$ to $T(\vec{j})$ exists when both touch the same memory cell, at least one writes it, and $S(\vec{i})$ runs first. For a dependence between two statements with $c$ common loops, the distance is $\vec{d} = (j_1 - i_1, \dots, j_c - i_c)$. The dependence is *carried at level* $l$ if $d_1 = \dots = d_{l-1} = 0$ and $d_l > 0$. It is loop independent if $\vec{d} = \vec{0}$.

**Definition.** The loop at level $l$ of a nest is a *DOALL loop* if no dependence of the nest is carried at level $l$.

**Parallel execution.** Run the loop at level $l$ as a DOALL loop means this. The outer loops at levels $1$ to $l - 1$ stay sequential. For each fixed outer iteration $(i_1, \dots, i_{l-1})$, every iteration $i_l$ of the loop runs its body, with the inner loops, in the original order. Across different values of $i_l$, the statement instances may interleave in any way. Each statement instance runs as one atomic step. The loop ends when all its iterations end, which is a barrier.

A reordering of the instances is called *legal* if it keeps the order of every dependent pair (the condition of Theorem 1 on the [legality page](/loop-transformation-legality/)). Then every instance reads the same values and the final memory is the same, for every initial memory.

**Theorem.** Running the loop at level $l$ as a DOALL loop is legal for every interleaving if and only if no dependence is carried at level $l$.

*Proof.* Take a dependent pair, from $S(\vec{i})$ to $T(\vec{j})$, with distance $\vec{d}$ and level of carry $m$ (or loop independent).

- If $m < l$, the two instances have different values of $i_1, \dots, i_m$, with $i_m < j_m$. The loop at level $m$ is still sequential, so all instances with the smaller value of $i_m$ end before any instance with the larger value starts. The order is kept.
- If $m > l$ or the dependence is loop independent, then $i_1 = j_1, \dots, i_l = j_l$. So both instances are in the same iteration of the loop at level $l$, which runs its body in the original order. The order is kept.
- If $m = l$, the two instances are in different iterations $i_l < j_l$ of the same instance of the loop. The interleaving that runs all of iteration $j_l$ before iteration $i_l$ reverses the pair.

So all pairs keep their order for every interleaving exactly when no pair has $m = l$. With the reordering theorem of the legality page, this gives the claim. $\square$

The converse is about dependences, not about values. A reversed flow or anti dependence changes a value that some instance reads, when each statement stores a value that is a one to one function of its inputs and of its own identity. A reversed output dependence alone may leave the result the same, for example if a later statement overwrites the cell. Compilers do not use that freedom: they treat every carried dependence as a reason to keep the loop sequential.

A dependence test is conservative: it may report a dependence that does not exist, and it never misses one that exists. A loop that the compiler proves DOALL is a DOALL loop. A loop that the compiler does not prove DOALL may still be one.

## Examples and non-examples

**A plain DOALL loop.**

```
for i = 1 to n:
  A[i] = B[i] + C[i]
```

Each iteration writes its own cell of $A$ and reads only $B$ and $C$. No dependence exists, so the loop is DOALL.

**A recurrence is not DOALL.**

```
for i = 1 to 6:
  A[i] = A[i-1] + B[i]
```

The write $A[i]$ and the read $A[i-1]$ in iteration $i + 1$ touch the same cell, so there is a flow dependence with distance $1$, carried at level 1. With $A[0] = 1$, the other cells of $A$ zero and $B[i] = i$, the sequential run gives $A = [1, 2, 4, 7, 11, 16, 22]$, the prefix sums. The interleaving that runs the iterations from $i = 6$ down to $1$ gives $A = [1, 2, 2, 3, 4, 5, 6]$, because each iteration reads $A[i-1]$ before it is written. The recurrence has a parallel algorithm (a parallel prefix sum), but that changes the order of the additions, so it is not a DOALL run of this loop.

**One loop of a nest.**

```
for i = 1 to n:
  for j = 1 to m:
    A[i][j] = A[i-1][j] + 1
```

The only dependence has distance $(1, 0)$, carried at level 1. The $j$ loop is DOALL and the $i$ loop is not. Each column is a chain, so after [loop interchange](/loop-interchange/), which is legal here because $(0, 1)$ stays lexicographically positive, the outer loop over $j$ is DOALL and runs $m$ independent chains.

**An exact test helps.**

```
for i = 0 to n:
  A[2*i] = A[2*i+1] + 1
```

A dependence needs $2 i = 2 i' + 1$, which has no integer solution because $\gcd(2, 2) = 2$ does not divide $1$. The [GCD test](/gcd-test/) proves this, so the loop is DOALL. A test that ignored integrality would report a possible dependence and lose the parallel loop.

**A scalar temporary.**

```
for i = 1 to n:
  t = A[i]
  B[i] = t * t
```

All iterations write the same cell $t$. This gives an output dependence and an anti dependence, from the read of $t$ in iteration $i$ to the write of $t$ in iteration $i + 1$, both carried at level 1. So the loop is not DOALL as written. Each read of $t$ follows a write of $t$ in the same iteration, so $t$ can be made private to each iteration ([array privatization](/array-privatization/), which also covers scalars). After privatization no dependence is carried, and the loop is DOALL.

**A reduction is not DOALL.**

```
for i = 1 to n:
  s = s + A[i]
```

The flow dependence on $s$ has distance 1. Because $+$ is associative and commutative on integers, a compiler can run the loop as a [parallel reduction](/parallel-reduction/): each thread sums a part, and the parts are added at the end. That is a different program, not a DOALL run of this one. For floating point numbers it can change the result.

**Indirect subscripts.** In `A[idx[i]] = B[i]`, the loop is DOALL exactly when `idx` has no repeated value among the iterations. The compiler cannot know this from the text. A run-time check (an inspector that tests the index array before the loop) can decide it.

## Related definitions

- [Loop-carried dependence](/loop-carried-dependence/) and [dependence distance vectors](/dependence-distance-vector/) give the level of a dependence, which is the only fact the definition uses.
- A [DOACROSS loop](/doacross-parallelization/) runs the iterations of a loop with carried dependences in parallel, with post and wait synchronization that keeps each carried pair in order.
- [Vectorization](/vectorization/) needs less than DOALL for one statement: the statement must not be on a dependence cycle at its level. The [Allen-Kennedy algorithm](/allen-kennedy-algorithm/) splits a loop into DOALL pieces and sequential pieces by the strongly connected components of the dependence graph, the same way as [loop distribution](/loop-distribution/).
- The [hyperplane method](/lamport-hyperplane-method/) and [wavefront parallelism](/wavefront-parallelism/) build new loops, of which all but the outer one are DOALL, when no original loop is.
- In a parallel language, the [parallel for](/parallel-for/) loop is the construct. A DOALL loop is the property that makes a loop safe to write as a parallel for loop.

## References
