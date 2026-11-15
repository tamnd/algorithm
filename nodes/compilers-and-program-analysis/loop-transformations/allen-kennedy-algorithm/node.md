---
tag: WZS56G
kind: algorithm
slug: allen-kennedy-algorithm
name: Allen-Kennedy vectorization algorithm
aliases:
- Allen-Kennedy codegen
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Distributes a loop nest by the strongly connected components of its dependence graph, level by level, and turns each statement that is on no cycle into a vector statement.
model: word-ram
complexity:
  vars: {n: the depth of the loop nest, r: the number of statements, e: the number of edges of the dependence graph}
  time: {worst: O(n (r + e))}
  space: {extra: O(r + e)}
properties: {deterministic: true, recursive: true}
prereqs: [loop-carried-dependence, loop-distribution, strongly-connected-components, doall-loop]
see_also: [vectorization, tarjan-scc, topological-sort, slp-vectorization, loop-interchange, dependence-testing, loop-transformation-legality, polyhedral-model]
sources:
  - paper: doi:10.1145/29873.29875
    title: Randy Allen and Ken Kennedy, Automatic translation of FORTRAN programs to vector form, ACM Transactions on Programming Languages and Systems 9(4), 1987, 491-542
    locator: the vector code generation procedure (codegen on the strongly connected components of the dependence graph, level by level) and the PFC translator
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (the section on parallelization and vectorization, with the advanced vectorization algorithm codegen and its worked example) and Chapter 5 (transformations that break dependence cycles before vectorization)
  - paper: doi:10.1080/01495739708941417
    title: Alain Darte and Frédéric Vivien, On the optimality of Allen and Kennedy's algorithm for parallelism extraction in nested loops, Parallel Algorithms and Applications 12(1-3), 1997, 83-112
    locator: the main theorem (with dependence levels as the only information, no algorithm finds more parallel loops than Allen and Kennedy's)
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapter on vector code generation (loop distribution by strongly connected components and vector statements)
---

The Allen-Kennedy algorithm, called *codegen* by its authors, turns a loop nest into vector statements and sequential loops. At level $k$ it builds the [dependence graph](/data-dependence/) of the statements with the dependences that are carried at level $k$ or deeper or are loop independent, splits it into [strongly connected components](/strongly-connected-components/), and emits the components in [topological order](/topological-sort/). A component with a cycle keeps a sequential loop at level $k$ and is handled again at level $k + 1$. A statement that is on no cycle becomes a vector statement over all its loops from level $k$ inward. Allen and Kennedy built it for the PFC translator from Fortran to vector Fortran at Rice University, and published it in 1987.

## In plain words

A compiler wants to turn a loop into array operations, such as "add these two whole arrays", that a vector machine runs fast. A statement can become an array operation only if no iteration of it needs a result of another iteration of the same loop. The algorithm draws an arrow between two statements when one must run before the other. Statements that wait for each other in a circle must stay in an ordinary loop, because the order of their iterations matters. Every other statement can run as one array operation, at the right place in the order of the arrows. Inside each circle, the algorithm looks one loop deeper, where some arrows disappear, and tries again.

## The problem

**Input.** A loop nest that forms one chain of loops: loop 1 holds loop 2, which holds loop 3, up to depth $n$. Statement $S$ is inside the loops 1 to $d_S$. The statements and their text order are given. The dependence graph $D$ has an edge $S \to T$ labelled with level $l$ for each [dependence](/data-dependence/) from an instance of $S$ to an instance of $T$ that is carried at level $l$, and with level $n + 1$ for a loop-independent one.

**Output.** An equivalent program built only from the original loops (run sequentially) and vector statements. A vector statement over the loops $k$ to $d_S$ runs, for fixed outer indices $i_1, \dots, i_{k-1}$, all instances of $S$ at once: it reads all its operands, then it writes all its results, as an array assignment in Fortran 90 does. It is legal only if no dependence joins two of its instances.

The dependence graph comes from [dependence testing](/dependence-testing/). The algorithm uses only the level of each edge, not its distance.

## The algorithm

```pseudo id=main
CODEGEN(R, k)                    ▷ R: a set of statements; k: the current loop level
L1  E <- the edges of D between statements of R with level >= k
L2  pi_1, ..., pi_m <- the strongly connected components of (R, E), in topological order
L3  for c <- 1 to m do
L4      if pi_c has two or more statements, or a statement with an edge to itself in E then
L5          emit "for i_k = L_k to U_k:"                       ▷ a sequential loop
L6          CODEGEN(pi_c, k + 1)
L7      else
L8          S <- the only statement of pi_c
L9          emit S as a vector statement over the loops k to d_S   ▷ a scalar statement if d_S = k - 1
```

The call CODEGEN(all statements, 1) produces the program. Line L1 drops the dependences carried at levels $1$ to $k - 1$, because the enclosing sequential loops already keep them, and keeps the loop-independent ones (level $n + 1$) at every level. Line L2 uses [Tarjan's algorithm](/tarjan-scc/) and a topological sort of the component graph; ties go to the text order. A component with a cycle needs the loop at level $k$ to stay sequential, since some of its dependences go from one iteration of that loop to a later one in both directions around the cycle. At level $k + 1$ the edges carried at level $k$ are gone, so the cycle may break.

## Example

This is a small copy of the example in Allen and Kennedy's book, with all loops from 1 to 4 and $N = 2$:

```
for i = 1 to 4:
  S1: X[i] = Y[i] + 10
  for j = 1 to 4:
    S2: B[j] = A[j][N]
    for k = 1 to 4:
      S3: A[j+1][k] = B[j] + C[j][k]
    S4: Y[i+j] = A[j+1][N]
```

The dependence graph has these edges, found by checking all pairs of instances (LI means loop independent, level 4):

| edge | levels | reason |
|---|---|---|
| S2 to S2 | 1 | output on $B[j]$, written in every $i$ |
| S2 to S3 | 1, LI | flow on $B[j]$ |
| S3 to S2 | 1, 2 | flow on $A[j+1][N]$, read as $A[j][N]$ at $j + 1$ or at a later $i$ |
| S3 to S3 | 1 | output on $A[j+1][k]$, written in every $i$ |
| S3 to S4 | 1, LI | flow on $A[j+1][N]$ |
| S4 to S3 | 1 | anti on $A[j+1][N]$ |
| S4 to S4 | 1 | output on $Y[i+j]$ |
| S4 to S1 | 1 | flow on $Y$ |

**Level 1.** All edges count. The components are $\{S2, S3, S4\}$, with the cycle $S3 \to S4 \to S3$, and $\{S1\}$. The edge $S4 \to S1$ puts the big component first. So the $i$ loop stays sequential around the first one, and S1 becomes a vector statement over $i$ after it.

**Level 2, inside the $i$ loop.** The edges of level 2 or more among S2, S3, S4 are $S2 \to S3$ (LI), $S3 \to S2$ (level 2) and $S3 \to S4$ (LI). The components are $\{S2, S3\}$, with a cycle, and then $\{S4\}$. So the $j$ loop stays sequential around S2 and S3, and S4 becomes a vector statement over $j$.

**Level 3, inside the $j$ loop.** Only $S2 \to S3$ (LI) is left. There is no cycle. S2 has depth 2, so it is a scalar statement, and S3 becomes a vector statement over $k$.

```
for i = 1 to 4:
  for j = 1 to 4:
    S2: B[j] = A[j][2]
    S3: A[j+1][1:4] = B[j] + C[j][1:4]
  S4: Y[i+1:i+4] = A[2:5][2]
S1: X[1:4] = Y[1:4] + 10
```

S1 moved to the end, after all of the $i$ loop. This is legal, because no dependence goes from S1 to the other statements, and it is needed, because S1 reads values of $Y$ that S4 writes in earlier iterations.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts.

**Every dependence is kept.** Take a dependence from $S(\vec{i})$ to $T(\vec{j})$ with level $l$. Follow the recursion to the deepest call CODEGEN$(R, k)$ that has both $S$ and $T$ in $R$. If $l < k$, this call sits inside the sequential loop at level $l$, which runs iteration $i_l$ before $j_l$. If $l \ge k$, the edge is in line L1. The two statements cannot be in one component, since that component would be cyclic and line L6 would make a deeper call with both. So the topological order emits all of the component of $S$ before all of that of $T$, for the same outer indices. An acyclic component is one statement with no edge to itself of level $k$ or more, so no dependence joins two instances of one vector statement, and the read-then-write semantics is exact.

**Each statement is vectorized at the first level where it is on no cycle.** Let $G_m$ be the graph of the edges with level $m$ or more. These graphs shrink as $m$ grows. The region $R$ that contains $S$ at level $k$ is the component of $S$ in $G_{k-1}$, and it contains the component of $S$ in $G_k$. So $S$ becomes a vector statement at the smallest $m$ for which $S$ is on no cycle of $G_m$.

**No program of the same kind does better.** Suppose some program built from the original loops, loop distribution, statement order and vector statements runs $S$ as a vector statement over the loops $m$ to $d_S$, and $S$ is on a cycle of $G_m$. All the statements of the cycle are pieces in one sequence for each fixed $i_1, \dots, i_{m-1}$, and the order of the pieces is the same for all outer indices. Every edge of the cycle has its source and sink in the same outer iteration, so it forces its source piece to be no later than its sink piece, and strictly earlier when one of them is the piece of $S$. Around the cycle this gives the piece of $S$ before itself, which is impossible. Darte and Vivien proved more in 1997: with dependence levels as the only information, no transformation at all finds more parallel loops.

## Complexity

Each call runs Tarjan's algorithm and a topological sort on the edges inside its region, in $O(r_R + e_R)$ time. The regions of the calls at one level are disjoint, so one level costs $O(r + e)$ in total, and there are at most $n + 1$ levels. The worst case is $O(n(r + e))$ time and $O(r + e)$ extra space for the graph, the component lists and the recursion. In a real compiler the dependence tests that build the graph cost far more than codegen. The implementation on this page builds the graph by brute force over all pairs of instances on small loop bounds, which is quadratic in the number of instances and is only for testing.

## Properties

- **Distribution only.** The algorithm never interchanges loops and never changes the order of iterations of a loop it keeps. It only distributes loops and reorders statements.
- **Level information only.** It uses the level of each edge and nothing else. The [direction vectors](/dependence-direction-vector/) and distances are not needed.
- **Sequential loops are kept whole.** A loop that stays sequential at level $k$ is a plain loop. Its inner part may still have vector statements and [DOALL loops](/doall-loop/).
- **Parallel loops as well as vectors.** The same recursion, with "run as a parallel loop" instead of "emit as a vector statement", finds DOALL loops; that is the version that Darte and Vivien study.

## Variants and improvements

- **Breaking cycles first.** Scalar expansion, renaming, node splitting and [loop skewing](/loop-skewing/) remove some dependences or change their level before codegen runs. Allen and Kennedy describe them in the chapter on fine-grained parallelism of their book.
- **Loop interchange.** In a cyclic component, a loop that carries no dependence of the component can move inward, so that the vector statement runs along it; see [loop interchange](/loop-interchange/).
- **Self anti-dependences.** A statement such as `A[i] = A[i+1] + 1` has a self edge that is an anti-dependence. The read-then-write semantics of a vector statement keeps it, so a compiler can ignore such edges in line L4. The plain algorithm does not.
- **Fixed-length vectors.** A machine with vectors of $VL$ elements runs a vector statement in strips of $VL$; see [strip mining](/strip-mining/) and [vectorization](/vectorization/).
- **Richer dependence information.** With distance vectors or dependence polyhedra, more parallelism is possible, for example by skewing; the [hyperplane method](/lamport-hyperplane-method/) and [Feautrier's scheduling](/feautrier-scheduling/) use it.

## When to use it

Use it in a vectorizing or parallelizing compiler for loop nests whose dependences are known only up to their level, or whose distances are not uniform. It is simple, fast and optimal for that information. For innermost-loop SIMD code on modern processors it is the core of loop vectorization, together with strip mining and alignment. For short straight-line code, [SLP vectorization](/slp-vectorization/) packs statements of one block instead.

## Pitfalls

- **Text order instead of topological order.** With `S1: C[i] = A[i-1]` and `S2: A[i] = B[i]`, the only edge goes from S2 to S1, carried at level 1. The vector statements must run S2 first. Emitting them in text order reads $A$ before it is written.
- **Dropping loop-independent edges at deep levels.** Line L1 must keep the edges of level $n + 1$ at every level. Without them, two statements of one iteration can come out in the wrong order.
- **Edges of level exactly $k$.** Line L1 takes level $k$ or more, not only level $k$. Edges carried deeper still order the statements.
- **Missing self edges.** A single statement with a carried edge to itself, such as `A[i+1] = A[i] + 1`, is a cycle. Treating every one-statement component as acyclic gives a wrong vector statement.
- **Element-by-element semantics.** The proof uses the rule that a vector statement reads all operands before it writes. That holds for the statements that the algorithm emits, but not for a hand-written loop that a reader takes for a vector statement.
- **A scalar on every iteration.** A scalar temporary written in each iteration makes a cycle at every level. Expand it into an array first.

## Implementations

## History

Randy Allen and Ken Kennedy developed the algorithm for PFC, the Parallel Fortran Converter, at Rice University, and published it in the ACM Transactions on Programming Languages and Systems in 1987. The ideas of dependence graphs and their strongly connected components came from the work of Kuck and his group at Illinois on the Parafrase system. Allen and Kennedy's 2001 book gives the algorithm under the name codegen, with the example above. In 1997 Darte and Vivien proved that it finds the most parallel loops possible when the only information is the level of each dependence.

## References
