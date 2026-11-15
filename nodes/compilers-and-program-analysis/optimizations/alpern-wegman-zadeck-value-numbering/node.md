---
tag: 1FT49Y
kind: algorithm
slug: alpern-wegman-zadeck-value-numbering
name: Alpern-Wegman-Zadeck value numbering
aliases:
- partition-based value numbering
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Finds congruent SSA values by refining a partition of the value graph until operands of congruent values are congruent, as in DFA minimization.
solves: [global-value-numbering]
model: word-ram
complexity:
  vars: {n: the number of nodes of the value graph, e: the number of edges of the value graph}
  time: {worst: O((n + e) log n)}
  space: {extra: Θ(n + e)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [static-single-assignment-form, partition-refinement, dominator-tree, local-value-numbering]
see_also: [hopcroft-minimization, dfa-minimization, partial-redundancy-elimination, congruence-closure, sparse-conditional-constant-propagation, common-subexpression-elimination, hash-consing, full-employment-theorem]
sources:
  - paper: doi:10.1145/73560.73561
    title: "Bowen Alpern, Mark N. Wegman and F. Kenneth Zadeck, Detecting equality of variables in programs, Proceedings of the 15th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 1988), 1-11"
    locator: the whole paper (the value graph of SSA form, congruence, the optimistic partition by the method of Hopcroft in O(E log E) time, and the proof that congruent variables are equal where both are defined)
  - paper: doi:10.1145/73560.73562
    title: "Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Global value numbers and redundant computations, Proceedings of the 15th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 1988), 12-27"
    locator: the whole paper (the companion paper on removing redundant computations with global value numbers)
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 12.4.2 (Global Value Numbering, the value graph and the partitioning algorithm)
  - paper: doi:10.1145/201059.201061
    title: "Cliff Click and Keith D. Cooper, Combining analyses, combining optimizations, ACM Transactions on Programming Languages and Systems 17(2), 1995, 181-196"
    locator: the whole paper (conditional constant propagation and value numbering combined in one optimistic analysis)
  - paper: doi:10.1007/3-540-48294-6_15
    title: "Oliver Rüthing, Jens Knoop and Bernhard Steffen, Detecting equalities of variables, combining efficiency with precision, Static Analysis Symposium (SAS 1999), LNCS 1694, 232-247"
    locator: the whole paper (rewrite rules for phis, alternated with the AWZ partition, to find more equalities)
  - paper: doi:10.1007/978-3-540-27864-1_17
    title: "Sumit Gulwani and George C. Necula, A polynomial-time algorithm for global value numbering, Static Analysis Symposium (SAS 2004), LNCS 3148, 212-227"
    locator: Section 1 (AWZ is incomplete because it treats phi functions as uninterpreted)
---

The Alpern-Wegman-Zadeck algorithm (AWZ) solves [global value numbering](/global-value-numbering/) on [SSA form](/static-single-assignment-form/). It builds the value graph of the procedure, in which each SSA name is a node labeled with its operator and pointing to its operands. Then it finds the coarsest partition of the nodes in which equal labels and congruent operands are the only reason to share a class. It starts from the hopeful guess that all nodes with the same label are equal, and splits classes only when operands prove two nodes different. This is the [partition refinement](/partition-refinement/) of [Hopcroft's DFA minimization](/hopcroft-minimization/), and it runs in $O((n + e) \log n)$ time. Because it starts hopeful, it finds equal values that depend on themselves through loops, which a one-pass hashing method like [local value numbering](/local-value-numbering/) cannot.

## In plain words

Put every value of the program into a group with all the values of the same kind: all additions together, all multiplications together, and all merges at the same join together. Now check each group. Two values in a group must have their first operands in one group and their second operands in one group. If they do not, split the group. Repeat until no group needs a split.

At the end, two values in one group are equal on every run, wherever both are available. A value whose group was already computed higher up in the program is replaced by a copy of the earlier one.

The hopeful start is the point. Two loop counters that both start at 1 and both add 1 are in one group from the start, and nothing ever splits them.

## The problem

The input is a procedure of the toy IR with const, copy and op instructions and any control flow. The output is a program with the same behavior on every input in which some operations are replaced by copies of equal values computed earlier. The algorithm is meant to remove every operation that is congruent to an operation that dominates it. Congruence is defined on the value graph in the [definition of the problem](/global-value-numbering/): a partition that refines the labels and in which nodes of one class have their $j$-th operands in one class, for every $j$.

AWZ does not find all equal values. That problem is undecidable, and even Herbrand equivalence, which treats operators as unknown functions, is more than congruence, because AWZ treats each phi as an unknown function of its block.

## The algorithm

The value graph has a node for each parameter, SSA name and constant. The label of an op is its operator, the label of a phi is its block, a parameter has a label of its own, and a constant is labeled by its value. The children of an op are its operands, and the children of a phi are its operands in the order of the predecessors of the block.

```pseudo id=main
AWZ(P)
L1  S <- SSA form of P, with copies and constants folded into the operands
L2  G <- the value graph of S
L3  B <- the partition of the nodes of G by label and number of children
L4  W <- all classes of B
L5  while W is not empty do
L6      take a class C out of W
L7      for each position j do
L8          for each class D that has nodes whose j-th child is in C and nodes whose j-th child is not
L9              split D into those two parts; the larger part keeps the name D
L10             put the smaller part into W
L11 walk the dominator tree of S from the entry, with a scoped map REP from classes to names
L12     for each definition x of the block, phis first
L13         if REP has the class of x then replace the definition by x = REP[class of x]
L14         else REP[class of x] <- x
L15 return S
```

Line L8 uses the members of $C$ as they were at line L6. The worklist holds classes, and line L10 is Hopcroft's rule: a part that splits off goes into the worklist, and the larger part, which keeps the name, needs no new entry. If $D$ was waiting in $W$, both parts are waiting now. If $D$ was not, the partition is already stable for $D$, and stability for the smaller part implies stability for the larger one.

Lines L11 to L14 are the elimination. A replaced phi becomes a copy placed right after the phis of its block. The representative of a phi is another phi of the same block, since only those share its label. The SSA builder places phis at the [dominance frontiers](/dominance-frontier/) of the definitions, only where the variable is live, as in [SSA construction](/cytron-ssa-construction/).

## Example

The parameter is `n`.

```
entry:
  i = 1
  j = 1
  s = 0
  jump loop
loop:
  a = i * 4
  b = j * 4
  s = s + a
  s = s + b
  i = i + 1
  j = j + 1
  c = i <= n
  br c loop exit
exit:
  ret s
```

In SSA form, with the constants folded, the loop block starts with `i.1 = phi [entry: 1, loop: i.2]`, `s.1 = phi [entry: 0, loop: s.3]` and `j.1 = phi [entry: 1, loop: j.2]`. The value graph has 14 nodes: `n`, the constants 0, 1 and 4, three phis and seven ops.

| step | classes with more than one node |
|---|---|
| L3, by label | phis of `loop`: {i.1, j.1, s.1}; `*`: {a.1, b.1}; `+`: {s.2, s.3, i.2, j.2} |
| first operand of a phi is 0, not 1 | {i.1, j.1}, s.1 alone |
| first operand of a `+` is a phi, not a `+` | {s.2, i.2, j.2}, s.3 alone |
| second operand of a `+` is a `*`, not a constant | {i.2, j.2}, s.2 alone |
| no more splits | {i.1, j.1}, {a.1, b.1}, {i.2, j.2} |

The order of the splits depends on the worklist, but the final partition does not. The elimination meets `i.1` before `j.1`, `a.1` before `b.1` and `i.2` before `j.2`, so it gives:

```
loop:
  i.1 = phi [entry: 1, loop: i.2]
  s.1 = phi [entry: 0, loop: s.3]
  j.1 = i.1
  a.1 = i.1 * 4
  b.1 = a.1
  s.2 = s.1 + a.1
  s.3 = s.2 + b.1
  i.2 = i.1 + 1
  j.2 = i.2
  c.1 = i.2 <= n
  br c.1 loop exit
```

For $n = 3$ both programs return $2 \cdot (4 + 8 + 12) = 48$, and the operations run drop from 21 to 15. A pessimistic hashing method that visits `loop` first meets `i.1` and `j.1` before their back-edge operands have numbers, so it must give them different numbers, and it finds none of these three equalities.

## Correctness

The proof file has the full proof. It has three parts.

- **The partition is the coarsest congruence.** Every congruence refines the current partition, because a split separates two nodes whose $j$-th children lie on different sides of a union of classes, and no congruence relates such nodes. When the worklist is empty, the partition is stable for each of its classes, which is the definition of a congruence. The second part needs an invariant: every class is in the worklist, or the partition is stable for the union of the class with some classes that are in the worklist.
- **Congruent names hold equal values.** In every run, if $x$ and $y$ are congruent and both definitions dominate the current point, they hold equal values. The proof goes by induction on the steps of the run. Its key lemma says that the latest execution of an operand comes before the latest execution of a value that uses it, when the value dominates the point. Strict SSA form gives this.
- **The elimination keeps every outcome.** A replaced op is congruent to a dominating one that was computed from equal operands without a trap, so the copy writes the value that the op would write, and the op could not have trapped. A replaced phi gets the value of a congruent phi of the same block. The two programs run in lockstep with the same environments, so they return the same value, trap at the same step or run out of fuel at the same step.

## Complexity

The value graph has $n$ nodes and $e$ edges, with $n$ and $e$ linear in the size of the SSA form. Taking a class $C$ from the worklist costs $O(|C|)$ plus the edges into $C$, and a split costs time linear in the part that is moved. A class that contains a fixed node enters the worklist at most $1 + \log_2 n$ times, since each later entry is at most half of the class of the node before the split. So the refinement takes $O((n + e) \log n)$ time, which Alpern, Wegman and Zadeck state as $O(E \log E)$. The partition and the lists of users take $\Theta(n + e)$ space. SSA construction and the dominator tree are near linear, and the elimination is one walk of the tree with a hash map, so the whole pass is dominated by the refinement.

## Properties

- **Optimistic.** It assumes equality and refutes it, so it finds the greatest fixed point: the coarsest congruence. A pessimistic method finds a congruence too, but it can be finer.
- **The result does not depend on the order.** The coarsest congruence is unique, so any worklist order gives the same partition as naive round-by-round refinement.
- **Never more operations.** Each operation is kept or replaced by a copy, so no run executes more operations than before.
- **No algebra.** Operators are uninterpreted: $x + y$ and $y + x$ are different unless the operands are sorted first, and $a \cdot 2$ and $a + a$ are never merged.
- **Phis are local to their block.** Two phis are congruent only if they are in the same block, so equalities that move an operation through a phi are missed.

## Variants and improvements

- **Commutative operators.** Sort the two operands of a commutative operator by a fixed key before the refinement, or give such a node an unordered pair of children. The first is cheap and finds the common cases.
- **Constants and conditions.** Click and Cooper combine optimistic value numbering with conditional constant propagation, in the style of [sparse conditional constant propagation](/sparse-conditional-constant-propagation/), so that a known constant can merge classes and an unreachable edge drops a phi operand.
- **Rewrite rules for phis.** Rüthing, Knoop and Steffen alternate the AWZ partition with rules that move an operation through a phi, which finds more Herbrand equalities while staying polynomial.
- **Redundancy beyond dominance.** Congruent values that do not dominate each other can be removed by [partial redundancy elimination](/partial-redundancy-elimination/) on value classes, which inserts computations where needed.

## When to use it

Use AWZ when the program is in SSA form and loops carry values that step together, such as induction variables after unrolling or inlining. It finds what pessimistic hashing misses, in $O((n + e) \log n)$ time. When most redundancy is in straight-line code, or when algebraic rules matter more than loops, dominator-based hashing with folding is simpler and almost as good. When a redundant value is computed on only some paths, use [partial redundancy elimination](/partial-redundancy-elimination/).

## Pitfalls

- **Congruent but not available.** Congruent values in two branches of an `if` are equal where both are defined, but neither dominates the other. Replacing one by the other reads an undefined name on the other path.
- **Merging phis of different blocks.** A phi label must name its block. Two phis `phi [L: a, R: b]` at two different joins can choose by different conditions, so they can differ on the same run.
- **Ignoring the operand order of a phi.** The children of a phi follow the order of the predecessors of its block. Comparing them as a set merges `phi [L: a, R: b]` with `phi [L: b, R: a]`.
- **Algebra that removes traps.** AWZ itself never removes a trap, because it only replaces an op by a dominating congruent op that ran without a trap on equal operands. An added rule such as $a / a = 1$ breaks this for $a = 0$.
- **Non-strict SSA.** The proof needs every use to be dominated by its definition. If a variable is read before it is defined on some path, the builder must give that path an explicit value, as the implementation does with 0.
- **Longer live ranges.** A copy of a value defined far above keeps that value live, which can cost a register in a loop.

## Implementations

## History

Alpern, Wegman and Zadeck presented the algorithm at POPL 1988, together with the companion paper of Rosen, Wegman and Zadeck on global value numbers and redundant computations, which also uses SSA form. AWZ took the partition refinement of Hopcroft's 1971 DFA minimization and applied it to the value graph, which made the optimistic assumption cheap. Muchnick presents it as the global value numbering of his textbook. Later work measured what it misses: Rüthing, Knoop and Steffen added rules for phis in 1999, and Gulwani and Necula gave a polynomial algorithm for Herbrand equivalence in 2004 and noted that AWZ is incomplete because it treats phis as uninterpreted.

## References
