---
tag: CQ8RHA
kind: definition
slug: dependence-direction-vector
name: Dependence direction vector
aliases:
- direction vector
area: compilers-and-program-analysis/loop-transformations
level: core
summary: The signs of the components of the distance vectors of a dependence, written with less, equal and greater, when exact distances are unknown.
prereqs: [dependence-distance-vector]
see_also: [loop-carried-dependence, loop-transformation-legality, loop-interchange, banerjee-test, practical-dependence-tests, dependence-testing, loop-skewing, unimodular-transformations]
sources:
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapter on data dependence (direction vectors with the symbols less, equal and greater, and their use for interchange)
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (direction vectors and the rule that the leftmost non-equal entry of the direction vector of a dependence is less) and Chapter 3 (direction vectors computed by the dependence tests)
  - paper: doi:10.1145/567532.567555
    title: David J. Kuck, Robert H. Kuhn, David A. Padua, Bruce Leasure and Michael Wolfe, Dependence graphs and compiler optimizations, POPL 1981
    locator: pp. 207 to 218 (dependence graphs with direction information on the arcs, and the transformations they allow)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 11 (Section 11.6 on array data-dependence analysis, where signs of distances are written with plus, zero and minus)
---

The direction vector of a [data dependence](/data-dependence/) in a loop nest gives, for each common loop, the sign of the [distance](/dependence-distance-vector/) between the sink and the source iterations. It is the summary that compilers keep when the distance is not one fixed vector, which is common: a dependence can hold between many pairs of iterations at many distances. The direction vector still tells which loop [carries](/loop-carried-dependence/) the dependence and which loop permutations are legal. It cannot decide transformations that need the size of a distance, such as [skewing](/loop-skewing/).

## Definition

### Notation

This page uses Wolfe's notation with the symbols $<$, $=$ and $>$. Each symbol compares the source index with the sink index:

| symbol on this page | meaning | sign of $d_l = j_l - i_l$ | Aho, Lam, Sethi and Ullman |
|---|---|---|---|
| $<$ | $i_l < j_l$ | $d_l > 0$ | $+$ |
| $=$ | $i_l = j_l$ | $d_l = 0$ | $0$ |
| $>$ | $i_l > j_l$ | $d_l < 0$ | $-$ |

So "$<$" means that the sink runs in a *later* iteration of loop $l$. The two notations run in opposite visual directions: $<$ goes with $+$. Unions of symbols are also used: $\le$ for $\{<, =\}$, $\ge$ for $\{>, =\}$, $\ne$ for $\{<, >\}$, and $*$ for all three.

### Direction vector of a pair and of a dependence

Let $S(\vec{i}) \to T(\vec{j})$ be a dependence with $k$ common loops, and $\vec{d} = \vec{j} - \vec{i}$. Its **direction vector** is $\vec{\psi} = (\psi_1, \dots, \psi_k)$ with $\psi_l = {<}$, ${=}$ or ${>}$ as $d_l > 0$, $d_l = 0$ or $d_l < 0$.

The **direction vectors of the dependence** $S \to T$ form the set $\Psi(S, T) = \{\vec{\psi}(\vec{d}) : \vec{d} \in \Delta(S, T)\}$, which has at most $3^k$ elements. A vector with union symbols, such as $(<, *)$, stands for the set of all plain vectors it contains, here $(<, <)$, $(<, =)$ and $(<, >)$.

### The legal shape

Every distance vector satisfies $\vec{d} \succeq \vec{0}$ (see [distance vector](/dependence-distance-vector/)). So every direction vector of a dependence has one of two shapes:

- the leftmost entry that is not $=$ is $<$: the dependence is carried at the level of that entry;
- all entries are $=$: the dependence is loop independent, and the source statement comes before the sink statement in the body.

A vector whose leftmost non-$=$ entry is $>$ cannot belong to a dependence from $S$ to $T$. When a test finds solutions with such a vector, they belong to the dependence from $T$ to $S$, whose direction vector has each entry reversed.

### Direction vectors as constraints

A [dependence test](/dependence-testing/) can take a direction vector as an extra constraint: it adds $i_l < j_l$, $i_l = j_l$ or $i_l > j_l$ for each level and asks if a solution remains. Testing $(*, \dots, *)$ first, and refining one $*$ into $<$, $=$ and $>$ only when the test does not rule out the coarser vector, finds the set $\Psi$ with far fewer tests than all $3^k$ vectors in the usual case. The [Banerjee test](/banerjee-test/) and the [practical tests](/practical-dependence-tests/) work this way.

## Examples and non-examples

### A recurrence read in reverse

```
for i = 1 to n:
  S: A[i] = A[i+1] + 1
```

The write of $S(i)$ and the read of $S(i')$ touch the same element when $i = i' + 1$. In the pair (write, read), the read iteration $i'$ is smaller, so the sign is $>$: this is not a flow dependence from the write to the read. Reversed, it is an anti dependence from the read $S(i')$ to the write $S(i' + 1)$, with direction $(<)$ and distance $1$. The value read is the old value of $A[i'+1]$.

### Directions of a dependence with many distances

```
for i = 1 to 3:
  for j = 1 to 3:
    S: X[i+j] = X[i+j-1] + 1
```

The flow distances are $(0, 1)$, $(1, 0)$ and $(2, -1)$, so the flow direction vectors are $(=, <)$, $(<, =)$ and $(<, >)$. The output distances $(1, -1)$ and $(2, -2)$ give $(<, >)$, and the anti distance $(1, -2)$ gives $(<, >)$.

### Interchange

[Loop interchange](/loop-interchange/) of two loops swaps the two entries of each direction vector. It is legal if each swapped vector still has the legal shape. In the example above, $(<, >)$ becomes $(>, <)$, which is not legal, so the interchange is illegal. The vectors $(<, <)$, $(<, =)$ and $(=, <)$ swap to $(<, <)$, $(=, <)$ and $(<, =)$, all legal. So in a two-deep nest, interchange is legal exactly when no dependence has the direction vector $(<, >)$.

### What a direction vector cannot tell

The dependence $\vec{d} = (1, -1)$ has the direction vector $(<, >)$, and so does $\vec{d}' = (1, -2)$. Skewing the inner loop by the outer one, $(i, j) \mapsto (i, i + j)$, maps them to $(1, 0)$ and $(1, -1)$. The first becomes $(<, =)$, the second stays $(<, >)$. So the same direction vector can need a different skew factor, and only the distances say which one. Skewing by $2i$ maps both to vectors with a nonnegative second entry: $(1, 1)$ and $(1, 0)$.

### Non-examples

- $(>, <)$ is not the direction vector of any dependence. It is the reverse of $(<, >)$.
- $(=, =)$ is not the direction vector of a dependence of a statement on itself, because an instance does not depend on itself. It is the direction vector of a loop-independent dependence between two different statements.

## Related definitions

- **Distance vector.** The exact difference $\vec{j} - \vec{i}$; the direction vector is its sign. See [dependence distance vector](/dependence-distance-vector/).
- **Level.** The position of the leftmost $<$ when all earlier entries are $=$. See [loop-carried dependence](/loop-carried-dependence/).
- **Legality.** A loop permutation is legal if it maps each direction vector of each dependence to a vector of the legal shape; this is a special case of the [legality theorem](/loop-transformation-legality/). For general [unimodular transformations](/unimodular-transformations/) the test needs distances, or a direction vector with enough information to bound the signs of $T\vec{d}$.
- **Loop reversal.** Running loop $l$ backward swaps $<$ and $>$ at position $l$ in every vector.

## References
