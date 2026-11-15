---
tag: N6VXTA
kind: problem
slug: global-value-numbering
name: Global value numbering
aliases:
- GVN
area: compilers-and-program-analysis/optimizations
level: core
summary: Partition the values of a procedure into classes that surely hold equal values, so that a computation whose class is already computed can be removed.
prereqs: [static-single-assignment-form, local-value-numbering, dominator-tree, phi-function]
see_also: [alpern-wegman-zadeck-value-numbering, partial-redundancy-elimination, common-subexpression-elimination, congruence-closure, herbrand-universe, robinson-unification, sparse-conditional-constant-propagation, full-employment-theorem]
sources:
  - paper: doi:10.1145/73560.73561
    title: "Bowen Alpern, Mark N. Wegman and F. Kenneth Zadeck, Detecting equality of variables in programs, Proceedings of the 15th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 1988), 1-11"
    locator: the whole paper (the value graph, congruence as the coarsest partition, optimistic partitioning in O(E log E) time, and the use of SSA form)
  - paper: doi:10.1145/73560.73562
    title: "Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Global value numbers and redundant computations, Proceedings of the 15th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 1988), 12-27"
    locator: the whole paper (global value numbers on SSA form and the removal of redundant computations)
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the common subexpression analysis on partitions of expressions, which finds all equalities when operators are uninterpreted
  - paper: doi:10.1007/3-540-48294-6_15
    title: "Oliver Rüthing, Jens Knoop and Bernhard Steffen, Detecting equalities of variables, combining efficiency with precision, Static Analysis Symposium (SAS 1999), LNCS 1694, 232-247"
    locator: the whole paper (normalization rules on the value graph that extend the method of Alpern, Wegman and Zadeck)
  - paper: doi:10.1007/978-3-540-27864-1_17
    title: "Sumit Gulwani and George C. Necula, A polynomial-time algorithm for global value numbering, Static Analysis Symposium (SAS 2004), LNCS 3148, 212-227"
    locator: Sections 1, 3 and 4 (all Herbrand equivalences among terms up to a size bound in polynomial time, the lattice of finite height, and the programs whose equivalences need an exponential value graph)
  - paper: doi:10.1145/964001.964030
    title: "Sumit Gulwani and George C. Necula, Global value numbering using random interpretation, Proceedings of the 31st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL 2004), 342-352"
    locator: the whole paper (a randomized algorithm for Herbrand equivalences)
  - paper: doi:10.1007/978-3-540-30579-8_6
    title: "Markus Müller-Olm, Oliver Rüthing and Helmut Seidl, Checking Herbrand equalities and beyond, Verification, Model Checking, and Abstract Interpretation (VMCAI 2005), LNCS 3385, 79-96"
    locator: the whole paper (checking whether a given Herbrand equality holds, also with disequality guards)
  - paper: doi:10.1145/207110.207154
    title: "Cliff Click, Global code motion, global value numbering, Proceedings of the ACM SIGPLAN 1995 Conference on Programming Language Design and Implementation (PLDI 1995), 246-257"
    locator: the section on global value numbering (a hash table lookup over the SSA graph, ignoring block boundaries, with constant folding and algebraic identities)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Section 10.5.2 (Dominator-Based Value Numbering)
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 12.4.2 (Global Value Numbering)
---

Global value numbering (GVN) asks which values of a procedure are surely equal. The answer is a partition of the values into classes, such that two values in one class are equal whenever both are available. A compiler then removes a computation whose class was already computed at a point that [dominates](/dominator-tree/) it. GVN is the global form of [local value numbering](/local-value-numbering/). It works across blocks and through [phi-functions](/phi-function/), and it sees through renaming. It finds equal values, while [common subexpression elimination](/common-subexpression-elimination/) finds equal text. Exact equality of values is undecidable, so every algorithm finds a safe part of it. The standard parts are congruence, found by the algorithm of [Alpern, Wegman and Zadeck](/alpern-wegman-zadeck-value-numbering/), and Herbrand equivalence, which is decidable.

## In plain words

Give every value in a procedure a ticket, and give two values the same ticket only when you are sure they are equal on every run. Two sums get the same ticket if they add values with the same tickets. Where two paths join, a merged value gets the ticket of another merge at the same join if the values that come in on each path have equal tickets.

Loops make this hard, because a value in a loop depends on itself. You can start cautious and assume that nothing is equal until it is proved, or start hopeful and assume that values of the same kind are equal until something proves them different. The hopeful start finds more, for example two counters that step together.

Some equalities need algebra, like `a * 2` and `a + a`. Most GVN methods treat operators as black boxes and miss these.

## Definition

**Input.** A procedure in [static single assignment form](/static-single-assignment-form/), as a [control flow graph](/control-flow-graph/) of the toy IR with $N$ SSA names. Each name has one definition: a parameter, an operation `x = a op b`, or a phi `x = phi [P1: a1, ..., Pk: ak]`. Copies and constants are folded into the operands.

**Output.** A partition of the names into *value classes*. The partition is *sound* if, in every run, two names $x$ and $y$ in one class hold equal values at every point that both definitions dominate. The goal is a sound partition with as few classes as possible.

**The transformation.** A sound partition lets the compiler replace the definition of $y$ by the copy `y = x` when $x$ is in the class of $y$ and its definition dominates the definition of $y$. On a run that reaches $y$, $x$ was computed from equal operands, so the copy writes the same value, and $y$ cannot trap if $x$ did not.

**Three notions of equality.** The ideal partition uses *semantic equality*: $x$ and $y$ are equal at a point if every run that reaches the point has the same values in them. Two weaker notions are decidable.

- *Herbrand equivalence.* Read every operator as an uninterpreted function symbol, so that the value of a name is a term, such as $+(a, \times(b, 4))$, over the parameters and constants. Read every branch as a free choice. Two names are Herbrand equivalent at point $p$ if they have the same term after every path from the entry to $p$. Herbrand equivalence implies semantic equality, since it holds for every meaning of the operators and every outcome of the branches.
- *Congruence.* Build the *value graph*: a node for each name and constant, labeled with its operator (a phi is labeled with its block), with edges to its operands in order. A *congruence* is a partition that refines the labels and in which nodes of one class have their $i$-th operands in one class, for every $i$. The coarsest congruence is what Alpern, Wegman and Zadeck compute. Congruent names are equal at every point that both definitions dominate, and the [AWZ correctness proof](/alpern-wegman-zadeck-value-numbering/) shows this. Congruence is weaker than Herbrand equivalence, because two phis of different blocks are never congruent.

So congruence implies Herbrand equivalence at the points that both definitions dominate, which implies semantic equality, and both implications can be strict.

## Variants

- **Pessimistic, by hashing.** Visit the blocks in reverse postorder and number each value as [local value numbering](/local-value-numbering/) does, with keys (operator, operand numbers). A phi whose operand comes over a back edge, before it has a number, gets a fresh number. Dominator-based value numbering walks the dominator tree and keeps the table of a block for the blocks it dominates. This is fast and finds nothing that depends on a loop.
- **Optimistic, by partitioning.** Start with all nodes of one label in one class and split classes until operands agree. The [Alpern-Wegman-Zadeck algorithm](/alpern-wegman-zadeck-value-numbering/) does this with the method of [Hopcroft's DFA minimization](/hopcroft-minimization/). It finds the coarsest congruence.
- **Hashing on the whole SSA graph.** Click extends local value numbering to the whole procedure by ignoring block boundaries: one hash table lookup finds an instruction with the same operation and equal inputs. Constants are folded and algebraic identities are used in the same pass, and a later global code motion pass decides where each value is placed.
- **Herbrand complete.** Find every Herbrand equivalence, including the ones that move an operation through a phi. Kildall's method does this by abstract interpretation over sets of equivalences. Rüthing, Knoop and Steffen alternate the AWZ partition with rewrite rules for terms with phis; this finds more than AWZ but is still not complete. Gulwani and Necula find all equivalences among terms up to a given size in polynomial time.
- **With algebra.** Add commutativity, constant folding and identities such as $x - x = 0$. The theory with the full rules of integer arithmetic is undecidable, so practical GVN adds a fixed list of rules, as [local value numbering](/local-value-numbering/) does.
- **With memory.** Give a load a number keyed by its address and by a version of memory, so that two loads with no store in between get the same number. This needs [alias analysis](/alias-analysis/).

## Examples

**Two counters.** This is the example of the [AWZ page](/alpern-wegman-zadeck-value-numbering/):

```
# params: n
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

In SSA form, `i` and `j` become the phis `i.1 = phi [entry: 1, loop: i.2]` and `j.1 = phi [entry: 1, loop: j.2]`. Pessimistic hashing reaches `i.1` before `i.2` has a number, so `i.1` and `j.1` get different numbers, and so do `a` and `b`. The optimistic partition starts with `i.1` and `j.1` in one class and never finds a reason to split them, so it finds that `j.1` equals `i.1`, `b` equals `a` and `j.2` equals `i.2`. For $n = 3$ the loop runs three times, and the operations run drop from 21 to 15.

**A phi of sums against a sum of phis.**

```
# params: a, b, c, d, p
entry:
  br p left right
left:
  x = a + b
  u = a
  v = b
  jump join
right:
  x = c + d
  u = c
  v = d
  jump join
join:
  y = u + v
  z = x - y
  ret z
```

In SSA form `x.3` is a phi of `a + b` and `c + d`, and `y.1` is the sum of the phis of `u` and `v`. On each path `x` and `y` have the same term, so they are Herbrand equivalent, and `z` is always 0. They are not congruent: one is a phi, the other a `+`. AWZ leaves the program as it is. This is the case that the normalization rules of Rüthing, Knoop and Steffen and the algorithm of Gulwani and Necula handle.

**Algebra.** `x = a * 2` and `y = a + a` are equal for every integer `a`, but their terms $\times(a, 2)$ and $+(a, a)$ differ. Only a GVN with the rule $a + a = a \times 2$ finds this.

**Equal but not available.** Two branches both compute `x / y`, and the join computes it again. All three are congruent, but no one of them dominates another, so GVN removes none of them. Removing the one at the join needs [partial redundancy elimination](/partial-redundancy-elimination/), which can also insert computations.

## Known algorithms

| algorithm | finds | time |
|---|---|---|
| Dominator-based hashing | values whose operands are numbered first in reverse postorder | expected linear in the size of the SSA form |
| [Alpern-Wegman-Zadeck](/alpern-wegman-zadeck-value-numbering/) | the coarsest congruence | $O(E \log E)$ for $E$ edges of the value graph |
| Hashing on the SSA graph (Click 1995) | equal operations on equal inputs, plus constants and identities | one hash table lookup per instruction |
| Kildall 1973 | all Herbrand equivalences | exponential in the worst case |
| Rüthing, Knoop and Steffen 1999 | more than congruence, by rewrite rules for phis | polynomial |
| Gulwani and Necula, SAS 2004 | all Herbrand equivalences among terms of size at most $s$; with $s$ the program size, all among program terms | polynomial, linear in $s$ |
| Gulwani and Necula, POPL 2004 | Herbrand equivalences, by random interpretation | polynomial and randomized |

## Bounds

**Semantic equality is undecidable.** *Proposition.* No algorithm decides, for every program of the toy IR, two names $x$ and $y$ and a point $p$, whether $x$ and $y$ hold equal values in every run that reaches $p$.

*Proof.* Reduce from the [halting problem](/halting-problem/) of two-counter [register machines](/register-machine/) started with both counters 0, which is undecidable. Given such a machine $M$, build a program with one parameter $t$:

```
entry:
  x = 0
  y = 0
  r1 = 0
  r2 = 0
  br t done m0
done:
  ret x
```

The blocks `m0`, `m1`, ... simulate $M$. An increment of counter $r$ at state $q$ is the block `mq: r = r + 1; jump m(q')`. A test-and-decrement at state $q$ is `mq: z = r == 0; br z m(q0) dq`, with `dq: r = r - 1; jump m(q1)`. The halting state is the block `x = 1; jump done`. Let $p$ be the start of `done`. A run with $t \ne 0$ jumps to `done` with $x = y = 0$. A run with $t = 0$ runs $M$ step by step. If $M$ halts, that run reaches `done` with $x = 1$ and $y = 0$. If $M$ does not halt, it never reaches `done`. So $x$ and $y$ are equal in every run that reaches $p$ if and only if $M$ does not halt. A decider for value equality would decide this. $\square$

The same holds for every nontrivial property of the values by [Rice's theorem](/rice-theorem/), and it is why no GVN is complete, the point of the [full employment theorem](/full-employment-theorem/).

**Herbrand equivalence is decidable.** *Proposition.* Given a program with $k$ variables in which operators are uninterpreted and branches are free choices, two variables $x$, $y$ and a point $p$, it is decidable whether $x$ and $y$ have the same term after every path from the entry to $p$.

*Proof.* Work backward from $p$ with sets of equations between terms over the program variables, as in a [weakest precondition](/weakest-precondition/) calculus. A substitution $\sigma$ from variables to terms *satisfies* a set $E$ if $\sigma(s)$ and $\sigma(t)$ are the same term for every equation $s = t$ in $E$. The state after a path is the substitution that maps each variable to its term, and the state at the entry is the identity $\iota$, where each variable stands for its own initial value. The assignment `x = e` maps $E$ to $E[e/x]$, and $\sigma$ satisfies $E[e/x]$ if and only if the state after the assignment satisfies $E$. So $x$ and $y$ are Herbrand equivalent at $p$ if and only if $\iota$ satisfies $E_\pi = \{x = y\}$ pulled back along $\pi$, for every path $\pi$ from the entry to $p$.

Order the sets by their sets of solutions. A satisfiable $E$ has a [most general unifier](/most-general-unifier/) $\mu$ in solved form, found by [Robinson unification](/robinson-unification/), and its solutions are exactly the substitutions $\tau \circ \mu$. Let $U(\mu)$ be the variables that $\mu$ leaves unbound. *Lemma:* if the solutions of $E'$ are a proper subset of the solutions of $E$, and $E'$ is satisfiable, then $|U(\mu')| < |U(\mu)|$. Indeed $\mu'$ solves $E$, so $\mu' = \rho \circ \mu$ for some $\rho$. For each $w \in U(\mu')$, $\rho(\mu(w)) = w$, so $\mu(w)$ is a variable $u \in U(\mu)$ with $\rho(u) = w$. Distinct $w$ give distinct $u$, so $|U(\mu')| \le |U(\mu)|$. If the two counts were equal, $\rho$ would rename $U(\mu)$ one to one onto $U(\mu')$, so $\mu = \rho^{-1} \circ \mu'$, and every solution $\tau \circ \mu$ of $E$ would be the solution $\tau \circ \rho^{-1} \circ \mu'$ of $E'$, a contradiction. So a strictly falling chain of solution sets has at most $k + 2$ members: the counts $k, \ldots, 0$ and then the empty set.

The backward problem is a [dataflow problem](/dataflow-analysis/) over this lattice of finite height: the meet is the union of the equation sets, and each transfer function is a substitution, which distributes over unions. By the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) for [distributive frameworks](/distributive-dataflow-framework/), the iterative solution at the entry equals the meet over all paths, and the iteration ends because of the finite height. The answer is yes if and only if $\iota$ satisfies the result, which means that every equation in it is the same term on both sides. $\square$

The terms in this proof can grow exponentially when they are written out. Gulwani and Necula show that the set of all Herbrand equivalences at a point can need a value graph of exponential size, even for acyclic programs, which is why Kildall's method is exponential. They also prove that this lattice has height at most the number of variables, the same fact as the lemma above, and they get a polynomial algorithm by keeping only terms up to a size bound.

**Congruence is cheap.** The coarsest congruence is found in $O(E \log E)$ time by partition refinement, as for the coarsest stable partition of an automaton.

## Reductions

- **To DFA minimization.** The value graph is a deterministic automaton in which the $i$-th operand is the move on letter $i$ and the label is the output. The coarsest congruence is the partition of states that [Hopcroft minimization](/hopcroft-minimization/) computes, and AWZ uses the same [partition refinement](/partition-refinement/).
- **To congruence closure.** Given a set of term equations, [congruence closure](/congruence-closure/) finds all equations they imply in the theory of uninterpreted functions, as in [EUF satisfiability](/euf-satisfiability/). Pessimistic GVN on straight-line code is congruence closure of the equations of the assignments, and the merges at the joins are what make the global problem harder.
- **From halting.** The reduction in Bounds shows that semantic equality is undecidable.

## Applications

- **Redundancy removal.** Replace a value by a dominating equal one, then remove the dead code. This subsumes [common subexpression elimination](/common-subexpression-elimination/) for the cases that dominance covers.
- **Partial redundancy elimination.** GVN-based forms of [partial redundancy elimination](/partial-redundancy-elimination/) use value classes instead of lexical expressions, so they see through copies and renaming.
- **Constant propagation.** Together with [sparse conditional constant propagation](/sparse-conditional-constant-propagation/), GVN finds more: a class with a constant member is constant, and a known constant can split or merge classes.
- **Checking and validation.** Herbrand equivalence of two programs is a cheap proof that they compute the same function under every meaning of the operators, used in translation validation.

## References
