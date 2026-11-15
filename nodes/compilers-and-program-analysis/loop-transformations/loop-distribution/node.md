---
tag: JEA9PQ
kind: technique
slug: loop-distribution
name: Loop distribution
aliases:
- loop fission
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Splits a loop into several loops over the same range, each with part of the body, by the strongly connected components of dependences.
prereqs: [data-dependence, loop-carried-dependence, strongly-connected-components, topological-sort]
see_also: [loop-fusion, allen-kennedy-algorithm, tarjan-scc, doall-loop, vectorization, loop-interchange, array-privatization, loop-transformation-legality]
sources:
  - paper: doi:10.1145/567532.567555
    title: David J. Kuck, Robert H. Kuhn, David A. Padua, Bruce Leasure and Michael Wolfe, Dependence graphs and compiler optimizations, Proceedings of the 8th ACM Symposium on Principles of Programming Languages (POPL), 1981, 207-218
    locator: the dependence graph of a loop body, its strongly connected components (pi-blocks), and loop distribution over them
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (Dependence, Theory and Practice), loop distribution by strongly connected components in the vectorization algorithm; Chapter 6 (Creating Coarse-Grained Parallelism), distribution and scalar expansion for parallel loops
  - paper: doi:10.1007/3-540-57659-2_18
    title: Ken Kennedy and Kathryn S. McKinley, Maximizing loop parallelism and improving data locality via loop fusion and distribution, Languages and Compilers for Parallel Computing (LCPC 1993), Lecture Notes in Computer Science 768, Springer, 1994, 301-320
    locator: distribution into the finest legal partition and fusion of the parallel pieces back together
---

Loop distribution splits one loop into several loops over the same range, each running a part of the original body. The statements are grouped by the *strongly connected components* of the [dependence](/data-dependence/) graph of the body: statements on a common dependence cycle stay in one loop, and the loops follow a topological order of the components. With this rule the distribution is always legal. The point is that the cycles are now separate. A statement that is not on any cycle carried by the loop lands in a loop of its own with no [carried dependence](/loop-carried-dependence/), and that loop can run in parallel or as [vector code](/vectorization/), while the recurrences stay in small sequential loops. Distribution is the inverse of [loop fusion](/loop-fusion/), and it is the core step of the [Allen-Kennedy algorithm](/allen-kennedy-algorithm/).

## In plain words

A loop body often does several jobs at once. Some jobs depend on what they did in the last turn of the loop, and others do not. Distribution pulls the jobs apart into separate loops, so that each loop does one group of jobs over the whole range. Jobs that feed each other in a circle must stay together, because neither can finish first. All other jobs can go in their own loops, placed so that each loop comes after the loops whose results it needs. A loop whose job never needs its own earlier turns can then run all its turns at the same time.

## When it applies

Take a loop `for i = L to U` whose body is the statements $S_1, \dots, S_m$ in this textual order, and build the dependence graph $G$: a node per statement, and an edge $S_a \to S_b$ for every dependence from an instance of $S_a$ to an instance of $S_b$, either carried by this loop or loop-independent. The loop must satisfy:

- **(D1) A straight-line body.** The statements form a sequence. A conditional is first turned into a guarded statement, with the condition kept in a temporary if the statements split.
- **(D2) Known dependences.** Every dependence of the body is an edge of $G$, flow, anti and output alike. A test that cannot decide gives an edge.

In a nest, distributing the loop at depth $l$ uses only the dependences carried at depth $l$ or deeper, and the loop-independent ones. The dependences carried by an outer loop stay satisfied, because the outer loop still runs its iterations in order around the new loops.

## The template

```pseudo id=main
DISTRIBUTE(for i = L to U: S_1; ...; S_m)
L1  build the dependence graph G on S_1, ..., S_m
L2  find the strongly connected components C_1, ..., C_r of G
L3  order the components in a topological order of the component graph
L4  for each component C in that order do
L5      emit for i = L to U: the statements of C in their original textual order
L6      if no edge inside C is carried by the loop then
L7          mark this loop as parallel
```

The holes are the body and its graph. Line L2 is [Tarjan's algorithm](/tarjan-scc/), which also returns the components in reverse topological order, so line L3 costs nothing more. The result is the finest distribution, with one loop per component. Any coarser one, which merges components that are next to each other in the order, is also legal, and the pieces can be fused back with [loop fusion](/loop-fusion/) to recover reuse.

**Theorem.** Split the statements into groups $G_1, \dots, G_r$ and emit one loop per group in this order, each with its statements in textual order. This keeps every dependence pair in order if and only if no edge of $G$ goes from a statement of a later group to a statement of an earlier group.

*Proof.* In the original loop the instance $S_a(i)$ runs before $S_b(j)$ exactly when $i < j$, or $i = j$ and $a < b$. Take a dependence from $S_a(i)$ to $S_b(j)$, so $S_a(i)$ runs first in the original.

- Same group. The loop for this group runs its instances in the same order as the original, restricted to its statements: by $i$ first and textual order second. The pair keeps its order.
- Group of $S_a$ before the group of $S_b$. Every instance of the earlier loop runs before every instance of the later loop. The pair keeps its order.
- Group of $S_a$ after the group of $S_b$. Then $S_b(j)$ runs first, and the pair is reversed. This is the case the condition forbids.

So all pairs keep their order exactly when no edge goes backward between groups, and Theorem 1 of the [legality page](/loop-transformation-legality/) gives the same result. $\square$

**Corollary.** The SCC grouping in topological order is legal. An edge inside one component stays inside one group. An edge between two components goes from an earlier to a later one in any topological order of the component graph. Conversely, two statements on a common cycle cannot be put in different loops: whichever loop comes first, one edge of the cycle goes backward.

**Profit.** A component with no carried edge gives a parallel loop. Distribution can also make each loop touch fewer arrays, which helps when the body uses more arrays than the cache or the [registers](/register-allocation-problem/) can hold, and it isolates a loop for [interchange](/loop-interchange/) when only some statements block the interchange. The cost is that values used by two loops must now go through memory, and that the loop control runs once per new loop.

## Classic examples

**Four statements, three loops.**

```
for i = 1 to n:
  S1: A[i] = B[i-1] + 1
  S2: B[i] = A[i] * 2
  S3: C[i] = C[i-1] + B[i]
  S4: D[i] = A[i] + 5
```

The edges are: $S_1 \to S_2$ on `A[i]`, loop-independent; $S_2 \to S_1$ on `B`, since $S_2(i)$ writes `B[i]` and $S_1(i+1)$ reads it, carried with distance 1; $S_2 \to S_3$ on `B[i]`, loop-independent; $S_3 \to S_3$ on `C`, carried with distance 1; $S_1 \to S_4$ on `A[i]`, loop-independent. The components are $\{S_1, S_2\}$, a cycle; $\{S_3\}$, with a self loop; and $\{S_4\}$. Both $S_3$ and $S_4$ come after $\{S_1, S_2\}$, and either order of the two is a topological order:

```
for i = 1 to n:           ▷ sequential: the recurrence through A and B
  A[i] = B[i-1] + 1
  B[i] = A[i] * 2
for i = 1 to n:           ▷ sequential: the recurrence on C
  C[i] = C[i-1] + B[i]
for i = 1 to n:           ▷ parallel
  D[i] = A[i] + 5
```

The last loop is a [DOALL loop](/doall-loop/). Run on random start values with $n = 8$, the original and this distribution give the same arrays, and so does the order with the `D` loop before the `C` loop. Splitting $S_1$ from $S_2$ is illegal: the loop of $S_1$ would read every `B[i-1]` before the loop of $S_2$ writes it, and the arrays differ.

**Scalar expansion.** In

```
for i = 1 to n:
  S1: t = A[i] + B[i]
  S2: C[i] = t * t
```

the scalar `t` gives the loop-independent flow edge $S_1 \to S_2$, and also the carried anti-dependence $S_2 \to S_1$, because $S_1(i+1)$ overwrites the `t` that $S_2(i)$ read, and a carried output dependence $S_1 \to S_1$. The two statements form one component, and nothing can be split. *Scalar expansion* replaces `t` by an array element `T[i]`, one per iteration. Then only the edge $S_1 \to S_2$ is left, and the loop splits into two parallel loops. If the last value of `t` is used after the loop, the code sets `t = T[n]`. When the loop is to stay one parallel loop, [array privatization](/array-privatization/) gives each thread its own copy of `t`, which removes the same edges with less memory.

**Vectorization.** A vectorizing compiler uses distribution to turn the acyclic part of a loop into vector statements: the third loop above becomes the array statement `D[1:n] = A[1:n] + 5`. The [Allen-Kennedy algorithm](/allen-kennedy-algorithm/) does this recursively over a nest, distributing at each level and moving to the next level inside each cyclic component.

## Variations

- **Partial distribution.** Split only off the statements that block an interchange or a parallel loop, and keep the rest together for reuse.
- **Distribution plus fusion.** Kennedy and McKinley first distribute to the finest legal partition and then fuse the parallel pieces back, as far as the fusion-preventing edges allow, so that the parallel loops are as large as possible.
- **Distribution in a nest.** Distributing the outer loop of a nest gives several nests, which is how imperfect nests are made perfect before [loop interchange](/loop-interchange/) or [tiling](/loop-tiling/).
- **Node splitting.** A cycle that consists of a loop-independent flow edge and a carried anti edge can sometimes be broken by copying the old value into a temporary array before the loop, which turns the anti edge into a read of the copy.

## Pitfalls

- **Ignoring anti and output dependences.** A cycle through an anti-dependence is a real cycle, as the scalar example shows. Leaving those edges out of the graph splits statements that must stay together.
- **Reordering by text.** Placing the loops in textual order instead of a topological order of the components is wrong when a later statement feeds an earlier one through a carried edge, as in Exercise 3. Always use the component order.
- **Scalars that live past the loop.** After scalar expansion, the value of the scalar after the loop must be restored from the last element.
- **Conditionals.** Splitting the statements of one `if` across loops evaluates the condition twice, and the second evaluation can see changed data. Save the condition in an array, one value per iteration.
- **Forgetting the cost.** Finest distribution can turn one pass over the data into many, and a temporary that was a register becomes memory traffic.

## Exercises

1. Distribute `S1: A[i] = A[i-1] + B[i]; S2: C[i] = A[i] * 3`. *Answer.* Edges: $S_1 \to S_1$ carried, $S_1 \to S_2$ loop-independent. Two components; the loop of $S_1$ comes first and is sequential, the loop of $S_2$ is parallel.
2. Distribute `S1: A[i] = C[i-1] + 1; S2: C[i] = A[i] * 2`. *Answer.* $S_1 \to S_2$ loop-independent and $S_2 \to S_1$ carried: one cycle, no distribution.
3. Distribute `S1: B[i] = A[i] + 1; S2: A[i+1] = C[i] * 2`. *Answer.* $S_2(i)$ writes `A[i+1]`, which $S_1(i+1)$ reads: an edge $S_2 \to S_1$, carried. There is no edge from $S_1$ to $S_2$. The topological order puts $S_2$ first: `for i: A[i+1] = C[i] * 2` then `for i: B[i] = A[i] + 1`, both parallel.
4. Why can a component with only loop-independent edges inside it run in parallel? *Answer.* Its loop carries no dependence, so no iteration uses a value from another iteration of the same loop.

## References
