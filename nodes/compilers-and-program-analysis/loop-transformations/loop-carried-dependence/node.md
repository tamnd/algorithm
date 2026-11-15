---
tag: AR27GT
kind: definition
slug: loop-carried-dependence
name: Loop-carried dependence
aliases:
- cross-iteration dependence
area: compilers-and-program-analysis/loop-transformations
level: core
summary: A dependence between different iterations of a loop, carried by the outermost loop whose distance component is not zero.
prereqs: [data-dependence, dependence-distance-vector]
see_also: [dependence-direction-vector, loop-transformation-legality, doall-loop, parallel-for, loop-interchange, vectorization, array-privatization, dependence-testing]
sources:
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (loop-carried and loop-independent dependences, Definition 2.11, the level of a dependence, and Theorem 2.4 on transformations that keep all level-k dependences)
  - paper: "Randy Allen and Ken Kennedy, Automatic translation of FORTRAN programs to vector form, ACM Transactions on Programming Languages and Systems 9(4), 1987"
    locator: the sections on loop-carried and loop-independent dependence and on the level of a dependence, used by the vector code generation algorithm
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 11.6 (array data-dependence analysis) and Section 11.7 (synchronization-free parallelism)
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapter on data dependence (dependence in loops, carried dependences and the level of a dependence)
---

A loop-carried dependence is a [data dependence](/data-dependence/) whose source and sink run in different iterations of a loop. In a loop nest it is *carried* by one loop, the outermost loop in which the two iterations differ. A dependence whose source and sink run in the same iteration of every common loop is *loop independent*. The level that carries a dependence decides which loops can run their iterations in parallel: a loop can be a [DOALL loop](/doall-loop/) exactly when it carries no dependence.

## Definition

Take a dependence from $S(\vec{i})$ to $T(\vec{j})$, where $\vec{i}$ and $\vec{j}$ are the iteration vectors of the $k$ loops common to $S$ and $T$. Its [distance vector](/dependence-distance-vector/) is $\vec{d} = \vec{j} - \vec{i}$. Because the source runs first, $\vec{i} \preceq \vec{j}$, so $\vec{d}$ is lexicographically positive or zero.

- The dependence is **carried at level $l$**, or carried by the loop of index $i_l$, when $d_1 = \dots = d_{l-1} = 0$ and $d_l \ne 0$. Then $d_l > 0$, because $\vec{d} \succ \vec{0}$.
- The dependence is **loop independent** when $\vec{d} = \vec{0}$. Then $S(\vec{i})$ and $T(\vec{i})$ run in the same iteration, and $S$ comes before $T$ in the loop body. A dependence between statements that share no loop ($k = 0$) is also loop independent.

The *level* of the dependence is $l$ in the first case and $\infty$ in the second. In the notation of [direction vectors](/dependence-direction-vector/) (Wolfe's $<, =, >$, where $<$ at position $l$ means $i_l < j_l$, that is, $d_l > 0$), a dependence is carried at level $l$ when its direction vector has $=$ in positions $1$ to $l-1$ and $<$ at position $l$, and it is loop independent when all entries are $=$.

Between two statements, the set of instance pairs can have many distance vectors, so the dependence $S \to T$ can be carried at several levels and also be loop independent. Each level that occurs is recorded on its own edge of the dependence graph.

A dependence of an instance on itself does not exist: a statement such as `x = x + 1` reads and then writes $x$ inside one instance, and that order is fixed. So a dependence of $S$ on itself always has $\vec{d} \ne \vec{0}$ and is loop-carried.

### Which loops can run in parallel

Run the nest with the loops of levels $1$ to $l - 1$ in order, run the iterations of the level-$l$ loop for each fixed outer iteration in any order or at the same time, and run each such iteration in order inside. This keeps the order of each dependence that is not carried at level $l$:

- carried at a level $m < l$: source and sink lie in different iterations of the outer loop $m$, which still runs in order;
- carried at a level $m > l$ or loop independent: source and sink lie in the same iteration of the level-$l$ loop, which still runs in order.

So by the [legality theorem](/loop-transformation-legality/), the level-$l$ loop can run in parallel if no dependence is carried at level $l$. If one is, the parallel run does not fix the order of its source and sink, and the result can change. Allen and Kennedy state the general form as their Theorem 2.4: a reordering that keeps the order of the loops and the iteration order of the level-$k$ loop keeps all level-$k$ dependences.

## Examples and non-examples

### One loop

```
for i = 1 to n:
  S1: A[i] = A[i-1] + 1
```

$S1(i)$ writes $A[i]$ and $S1(i+1)$ reads it. The flow dependence has distance $1$ and is carried by the $i$ loop. The loop is a recurrence, and its iterations cannot run in parallel as written.

```
for i = 1 to n:
  S1: A[i] = B[i] + 1
  S2: C[i] = A[i] * 2
```

$S1(i)$ writes $A[i]$ and $S2(i)$ reads it in the same iteration: distance $0$, loop independent. The loop carries no dependence, so its iterations can run in parallel, as long as each iteration runs $S1$ before $S2$.

### Two loops

```
for i = 1 to n:
  for j = 1 to n:
    S: A[i][j] = A[i-1][j+1] + 1
```

$S(i, j)$ writes $A[i][j]$, and $S(i+1, j-1)$ reads it. The distance is $(1, -1)$ and the direction vector is $(<, >)$. The $i$ loop carries the dependence. The $j$ loop carries nothing, so for a fixed $i$ all iterations of $j$ can run in parallel, even though the second entry of the distance is negative.

```
for i = 1 to n:
  for j = 1 to n:
    S: B[i][j] = B[i][j-1] + 1
```

The distance is $(0, 1)$: carried at level 2. The $i$ loop carries nothing, so the outer loop is parallel and each row runs its recurrence in order.

### One dependence carried at two levels

```
for i = 1 to 3:
  for j = 1 to 3:
    S: X[i+j] = X[i+j-1] + 1
```

All instance pairs, enumerated: the flow dependences have the distances $(0, 1)$, $(1, 0)$ and $(2, -1)$; the output dependences have $(1, -1)$ and $(2, -2)$; the anti dependence has $(1, -2)$. The flow dependence $S \to S$ is carried at level 2 by $(0,1)$ and at level 1 by the others. Neither loop is parallel.

### Non-examples

- A dependence with distance $(0, 0)$ is not carried by any loop. It is loop independent, even inside two loops. A transformation that changes only the order of iterations keeps it, if it keeps the order of the statements in the body.
- A dependence whose only cause is a temporary scalar, such as `t = A[i]; B[i] = t * t` inside a loop, is carried by the loop through the output and anti dependences on `t`. Giving each iteration its own copy of `t` removes them. A loop that carries only such dependences becomes parallel after [privatization](/array-privatization/).

## Related definitions

- **Distance and direction vectors.** The [distance vector](/dependence-distance-vector/) gives the level directly; when the distance is not known, the [direction vector](/dependence-direction-vector/) still gives it.
- **DOALL and DOACROSS.** A loop that carries no dependence is a [DOALL loop](/doall-loop/) and can run as a [parallel for](/parallel-for/). A loop that carries dependences can still overlap its iterations with synchronization ([DOACROSS](/doacross-parallelization/)).
- **Vectorization.** A statement can be turned into vector operations at a level if it is not on a cycle of dependences carried at that level or deeper; see [vectorization](/vectorization/) and the [Allen-Kennedy algorithm](/allen-kennedy-algorithm/).
- **Interchange.** [Loop interchange](/loop-interchange/) moves a carried dependence to another level. The dependence $(1, -1)$ above becomes $(-1, 1)$, which is not lexicographically positive, so that interchange is illegal.

## References
