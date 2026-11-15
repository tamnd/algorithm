---
tag: 1PQA1J
kind: definition
slug: data-dependence
name: Data dependence
aliases:
- flow dependence
- anti-dependence
- output dependence
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Two accesses to the same location, at least one a write, whose order must be kept; flow, anti and output by which access writes.
prereqs: [control-flow-graph]
see_also: [loop-carried-dependence, dependence-distance-vector, dependence-testing, loop-transformation-legality, control-dependence, program-dependence-graph, feautrier-array-dataflow, alias-analysis]
sources:
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (dependence, the three kinds, reordering transformations, Section 2.2.3 with Theorem 2.2, the fundamental theorem of dependence)
  - paper: doi:10.1145/567532.567555
    title: David J. Kuck, Robert H. Kuhn, David A. Padua, Bruce Leasure and Michael Wolfe, Dependence graphs and compiler optimizations, POPL 1981
    locator: pp. 207 to 218 (the dependence graph of a program, flow, anti and output dependence, and transformations that remove dependence arcs)
  - paper: "A. J. Bernstein, Analysis of programs for parallel processing, IEEE Transactions on Electronic Computers EC-15(5), 1966"
    locator: pp. 757 to 763 (the conditions on the input and output sets of two program parts that let them run in parallel)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 11.6 (array data-dependence analysis)
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapter on data dependence (kinds of dependence, the dependence graph, dependence in loops)
---

A data dependence is an ordering constraint between two runs of statements, called statement instances. Two instances depend on each other when both touch the same memory location, at least one of them writes it, and one runs before the other. A compiler may reorder the instances of a program only if it keeps the order of each dependent pair; this is the [legality theorem](/loop-transformation-legality/). There are three kinds: flow, anti and output, by which of the two accesses writes. Data dependence differs from [control dependence](/control-dependence/), which says whether an instance runs at all; the [program dependence graph](/program-dependence-graph/) holds both.

## Definition

### Statement instances

A program runs a sequence of *statement instances*. In a loop nest of depth $k$, statement $S$ runs once for each iteration vector $\vec{i} = (i_1, \dots, i_k)$ in its domain $D_S = \{\vec{i} \in \mathbb{Z}^k : A\vec{i} + \vec{b} \ge 0\}$, and $S(\vec{i})$ names that run. The iterations run in lexicographic order $\prec$, and the statements of one iteration run in the order of the text. Write $S(\vec{i}) \lessdot T(\vec{j})$ when $S(\vec{i})$ runs before $T(\vec{j})$ in the original program:

$$S(\vec{i}) \lessdot T(\vec{j}) \iff \vec{i}_{c} \prec \vec{j}_{c} \ \text{ or } \ \big(\vec{i}_{c} = \vec{j}_{c} \text{ and } S \text{ comes before } T \text{ in the text}\big),$$

where $\vec{i}_c$ and $\vec{j}_c$ are the parts of the vectors that belong to the loops common to $S$ and $T$.

For an instance $x$, let $R(x)$ be the set of memory locations that $x$ reads and $W(x)$ the set it writes. An array access has an affine access function: $S$ writes $X[F\vec{i} + \vec{f}]$, and that is one element for each $\vec{i}$.

### Dependence

There is a *data dependence* from $x$ to $y$, written $x \to y$, when $x \lessdot y$ and some location $\ell$ satisfies one of these three cases:

| kind | condition | also called |
|---|---|---|
| flow | $\ell \in W(x) \cap R(y)$ | true dependence, read after write |
| anti | $\ell \in R(x) \cap W(y)$ | write after read |
| output | $\ell \in W(x) \cap W(y)$ | write after write |

The case $\ell \in R(x) \cap R(y)$ is an *input dependence* (read after read). It does not constrain the order, because two reads give the same values in either order. Some compilers still record it, because it shows reuse of data in a cache.

$x$ is the *source* and $y$ is the *sink*. Between statements, $S \to T$ holds when $S(\vec{i}) \to T(\vec{j})$ for some pair of instances. In the isl notation, each kind between two statements is a relation, for example `{ S[i] -> T[j] : ... }`.

The definition is *memory-based*: it counts each pair that touches the same location, even when a third write lies between them. The *value-based* (dataflow) dependence keeps only the pair where the read gets its value from the write. The page [Feautrier array dataflow analysis](/feautrier-array-dataflow/) computes it exactly for affine programs.

### Why the order matters

Flow dependences carry values: the sink reads what the source wrote. Anti and output dependences come from the reuse of a location. Renaming removes them: give the later write a new location, for example a private copy of an array per iteration ([array privatization](/array-privatization/)) or a new name per assignment ([static single assignment form](/static-single-assignment-form/) for scalars). For this reason anti and output dependences are also called *false* or *name* dependences.

In real code the compiler often does not know the exact locations. Two pointers may point to the same object; a subscript may depend on input data. A compiler then assumes a dependence unless an [alias analysis](/alias-analysis/) or a [dependence test](/dependence-testing/) proves that none exists. The computed relation is a superset of the true one. A superset is safe: it can block a legal transformation, but it never allows an illegal one.

## Examples and non-examples

### A loop with all three kinds

```
for i = 1 to 3:
  S1: A[i+1] = A[i] + B[i]
  S2: B[i] = A[i+1] + 1
  S3: t = B[i+1]
```

The program runs nine instances, in the order $S1(1), S2(1), S3(1), S1(2), \dots, S3(3)$. All 13 dependent pairs, grouped:

| from | to | kind | location | pairs | relation |
|---|---|---|---|---|---|
| $S1(i)$ | $S2(i)$ | flow | $A[i+1]$ | 3 | `{ S1[i] -> S2[i] : 1 <= i <= 3 }` |
| $S1(i)$ | $S2(i)$ | anti | $B[i]$ | 3 | `{ S1[i] -> S2[i] : 1 <= i <= 3 }` |
| $S1(i)$ | $S1(i+1)$ | flow | $A[i+1]$ | 2 | `{ S1[i] -> S1[i + 1] : 1 <= i <= 2 }` |
| $S3(i)$ | $S2(i+1)$ | anti | $B[i+1]$ | 2 | `{ S3[i] -> S2[i + 1] : 1 <= i <= 2 }` |
| $S3(i)$ | $S3(i')$ | output | $t$ | 3 | `{ S3[i] -> S3[i'] : 1 <= i < i' <= 3 }` |

- $S1(i)$ writes $A[i+1]$, and $S2(i)$ reads it in the same iteration: a flow dependence inside one iteration. $S1(i+1)$ reads $A[i+1]$ in the next iteration: a flow dependence from one iteration to the next. The page [loop-carried dependence](/loop-carried-dependence/) names these two cases.
- $S1(i)$ reads $B[i]$ before $S2(i)$ writes it: an anti dependence. If a transformation moved $S2(i)$ before $S1(i)$, then $S1(i)$ would read the new value of $B[i]$.
- $S3(i)$ reads $B[i+1]$, and $S2(i+1)$ writes it later: an anti dependence.
- All three instances of $S3$ write the scalar $t$, so each pair is an output dependence, also the pair $S3(1) \to S3(3)$. The memory-based definition counts it. The value-based one does not, because $S3(2)$ writes $t$ between them. A private copy of $t$ per iteration removes all three.
- $S2(i)$ and $S1(i+1)$ both read $A[i+1]$. That is an input dependence, so it is not in the table.

### Non-examples

- `X[2*i] = ...` and `... = X[2*i+1]` in one loop never touch the same element, since an even number is never odd. There is no dependence. The [GCD test](/gcd-test/) proves this.
- Two reads of the same element, as above: no dependence.
- `A[i] = ...` and `... = B[i]` with distinct arrays $A$ and $B$: no dependence, if the compiler knows that $A$ and $B$ do not overlap. In C, two pointer parameters can overlap, and then the compiler must assume a dependence.
- `if c then x = 1` and `y = 2`: here there is no data dependence. The first assignment is control dependent on the test of `c`, which is a different relation.

### Straight-line code

Without loops, each statement runs once. In `a = b + c; b = a * 2; a = 7` the pairs are: flow from the first to the second statement on `a`, anti from the first to the second on `b`, anti from the second to the third on `a`, and output from the first to the third on `a`. Give the third `a` a new name: this removes the anti and the output dependence on `a`, and then the second and the third statements can run in either order.

## Related definitions

- **Bernstein's conditions.** Bernstein (1966) stated when two program parts $P_1$ and $P_2$ can run in parallel: $W_1 \cap R_2 = \emptyset$, $R_1 \cap W_2 = \emptyset$ and $W_1 \cap W_2 = \emptyset$. These are the three kinds of dependence above, for two parts whose order is free.
- **Dependence graph.** The statements are the nodes, and there is an edge $S \to T$ when $S(\vec{i}) \to T(\vec{j})$ for some pair of instances, labeled with the kind and with the [distance](/dependence-distance-vector/) or [direction](/dependence-direction-vector/) vectors. Kuck, Kuhn, Padua, Leasure and Wolfe (1981) made this graph the base of a compiler. Its strongly connected components decide [loop distribution](/loop-distribution/) and [vectorization](/vectorization/).
- **Loop-carried and loop-independent dependence.** A dependence between two different iterations of a loop, or within one iteration. See [loop-carried dependence](/loop-carried-dependence/).
- **Dependence testing.** The problem of deciding, for two array accesses in a loop nest, whether a dependence exists. See [dependence testing](/dependence-testing/).
- **Reordering transformation and legality.** A transformation that runs the same instances in another order. It keeps the meaning of the program if it keeps the order of each dependence. See [legality of loop reordering](/loop-transformation-legality/).
- **Def-use chains.** For scalars, the flow dependences inside a procedure are what [def-use chains](/def-use-chains/) and [reaching definitions](/reaching-definitions/) record.

## References
