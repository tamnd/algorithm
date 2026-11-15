---
tag: WP2EC3
kind: problem
slug: program-slicing
name: Program slicing
aliases:
- static slicing
- backward slice
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Given a program point and a set of variables, find the statements that may affect their values there.
model: word-ram
complexity:
  vars: {n: the number of statements, e: the number of edges of the program dependence graph}
  time: {dependence-slice: O(n + e)}
prereqs: [control-flow-graph, data-dependence, control-dependence]
see_also: [weiser-slicing, pdg-slicing, system-dependence-graph-slicing, dynamic-slicing, program-dependence-graph, halting-problem, aggressive-dead-code-elimination, cfl-reachability]
sources:
  - paper: "Mark Weiser, Program slicing, Proceedings of the 5th International Conference on Software Engineering, San Diego, March 1981, pages 439-449"
    locator: the slicing criterion, slices obtained by deleting statements, and the dataflow equations for slices
  - paper: doi:10.1109/TSE.1984.5010248
    title: Mark Weiser, Program slicing, IEEE Transactions on Software Engineering SE-10(4), 1984, pages 352-357
    locator: the definitions of criterion and slice, the argument that statement-minimal slices cannot be computed in general, and the iterative algorithm
  - paper: "Frank Tip, A survey of program slicing techniques, Journal of Programming Languages 3(3), 1995, pages 121-189"
    locator: the sections on static slicing (dataflow equations, dependence graphs, procedures, unstructured control flow) and on dynamic slicing
  - paper: doi:10.1145/77606.77608
    title: Susan Horwitz, Thomas Reps and David Binkley, Interprocedural slicing using dependence graphs, ACM Transactions on Programming Languages and Systems 12(1), 1990, pages 26-60
    locator: slices as reachability in dependence graphs, and the problem of calling context for slices across procedures
  - paper: doi:10.1016/S0950-5849(98)00093-7
    title: Thomas Reps, Program analysis via graph reachability, Information and Software Technology 40(11-12), 1998, pages 701-726
    locator: interprocedural slicing as a CFL-reachability problem
---

Program slicing is the problem of finding the statements of a program that may affect the values of some variables at some program point. The point and the variables form the *slicing criterion*, and the answer is a *slice*. Mark Weiser defined slices and the problem (ICSE 1981, IEEE TSE 1984) as a way to cut a program down for debugging. This page states the problem. [Weiser's algorithm](/weiser-slicing/), [slicing by dependence graph reachability](/pdg-slicing/), [system dependence graph slicing](/system-dependence-graph-slicing/) and [dynamic slicing](/dynamic-slicing/) solve versions of it.

## In plain words

When a variable has a wrong value at some line, a programmer reads the code backward. Which lines wrote the variable? Which lines computed the values that those lines used? Which tests decided whether those lines ran at all? The lines found this way form a slice. The other lines can be hidden, because they cannot change the value being studied. A slice is often much smaller than the program. The smallest possible slice depends on what the program really computes, and no tool can find it for every program. So tools find a slice that can be too large. They follow every write and every test that could matter on some path, even when that path never runs.

## Definition

Programs are in the toy IR of the [control flow graph](/control-flow-graph/) pages. A *statement* is an instruction or a terminator. Write $(\ell, i)$ for statement $i$ of block $\ell$, where $i$ equals the number of instructions of $\ell$ for its terminator. A *program point* is the point just before a statement. Every block is assumed to reach a `ret`.

**Criterion and observations.** A slicing criterion is a pair $C = \langle p, V \rangle$ of a point $p$ and a set $V$ of variables. For an input $I$, let $\mathrm{obs}_P(I, C)$ be the sequence of tuples of values that the variables of $V$ have each time the run of $P$ on $I$ reaches $p$. The sequence is finite or infinite, and it ends early if the run traps.

**Executable slices.** Fix a set $K$ of instructions and branches of $P$. The *projection* of $P$ on $K$ deletes every instruction outside $K$. It replaces every branch `br a L1 L2` outside $K$, at the end of block $\ell$, by `jump d`, where $d$ is the immediate [post-dominator](/post-dominance/) of $\ell$, or by `ret 0` when that post-dominator is the exit. It keeps every `jump`. A `ret a` keeps its operand only when $p$ is that return and $a \in V$; otherwise it becomes `ret 0`, which changes no observation. The projection $Q$ is a *slice* of $P$ for $C$ when, for every input $I$ on which the run of $P$ reaches a `ret`, the run of $Q$ on $I$ also reaches a `ret` and

$$\mathrm{obs}_Q(I, C_Q) = \mathrm{obs}_P(I, C),$$

where $C_Q = \langle p_Q, V \rangle$ and, for $p = (\ell, i)$, $p_Q$ is the point of $Q$ before the first kept statement at or after position $i$ in block $\ell$. The size of a slice is $|K|$. $K$ = all instructions and branches always gives a slice, so slices exist. A *statement-minimal* slice is one of least size. This is Weiser's definition in the toy IR. Weiser's own programs had structured statements, and deleting a structured statement plays the role of the jump to the post-dominator.

**Dependence slices.** A statement $t$ is *data dependent* on a statement $s$ if $s$ defines a variable $x$, $t$ reads $x$, and some path in the control flow graph goes from just after $s$ to $t$ with no definition of $x$ before $t$ ([data dependence](/data-dependence/), flow dependences only). A statement is *control dependent* on a branch as defined on the [control dependence](/control-dependence/) page. The *dependence slice* of $C$ is the least set $K$ of instructions and branches such that:

1. $K$ holds every instruction $s$ that defines some $x \in V$ such that some path goes from just after $s$ to $p$ with no definition of $x$;
2. $K$ holds every branch on which the statement at $p$ is control dependent;
3. if $t \in K$ and $t$ is data or control dependent on an instruction or branch $s$, then $s \in K$.

The dependence slice is what all practical tools compute. It is a set of nodes of the [program dependence graph](/program-dependence-graph/), found by backward reachability. Used as $K$, it gives a slice in the executable sense for every program in which every block reaches a `ret`; the proof is on the [Weiser's algorithm](/weiser-slicing/) page. It is not always statement-minimal.

**Forward slices.** The *forward slice* of a statement is the set of statements that depend on it, directly or through a chain of dependences. It answers "what can this change affect", while the backward slice answers "what can affect this".

## Variants

- **Static or dynamic.** A static slice must work for every input. A [dynamic slice](/dynamic-slicing/) must work for one given input, and it is often much smaller. It may be wrong for every other input.
- **Executable or closure slices.** Weiser asks for a program that runs. A dependence graph slice is a set of nodes, and the jumps and the block structure must be rebuilt before it runs. For programs with unstructured jumps, plain deletion can give a wrong program, and slicers must add jumps back; the survey of Tip covers the fixes for unstructured control flow.
- **Interprocedural.** Across calls, a slice should follow only paths where each return goes back to the call that entered the procedure. [System dependence graph slicing](/system-dependence-graph-slicing/) does this. A slicer that ignores calling context still gives a correct slice, but a larger one.
- **Conditioned slicing.** The criterion also gives a predicate on the inputs, and the slice must work only for the inputs that satisfy it. Static and dynamic slicing are the two ends: no condition, and a condition that fixes one input.
- **Amorphous slicing.** The slice may be any program that gives the same observations, not only a projection. It can be smaller, but it is no longer a subset of the original code.
- **Chopping.** A chop of a source statement and a target statement holds the statements on dependence chains from the source to the target. Within one procedure, it is the intersection of the forward slice of the source and the backward slice of the target.

## Examples

**Two slices of one loop.** The program below returns $s$, the sum of the odd numbers from 1 to $n$, and also computes $p = n!$ (with $p = 1$ for $n \le 0$).

```
B1:
  i = 1
  s = 0
  p = 1
  jump B2
B2:
  t = i <= n
  br t B3 B6
B3:
  p = p * i
  u = i % 2
  br u B4 B5
B4:
  s = s + i
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret s
```

For the criterion $\langle (B6, 0), \{p\} \rangle$ the dependence slice has 6 statements: `i = 1`, `p = 1`, `t = i <= n`, `br t B3 B6`, `p = p * i` and `i = i + 1`. The parity test and both statements on $s$ drop out. In the projection, `br u B4 B5` becomes `jump B5`, because B5 is the immediate post-dominator of B3, and `ret s` becomes `ret 0`. For the criterion $\langle (B6, 0), \{s\} \rangle$ the slice has 8 statements: all but `p = 1` and `p = p * i`. The two slices share the loop control: `i = 1`, `t = i <= n`, the branch on `t` and `i = i + 1`. On the inputs $n = 0, 1, 2, 3, 4, 5$ the pair $(s, p)$ at B6 is $(0, 1), (1, 1), (1, 2), (4, 6), (4, 24), (9, 120)$, and each slice gives the same value of its variable as the full program.

**A non-example.** Take $K$ = `i = 1`, `p = 1`, `p = p * i`, `i = i + 1`, without the loop test. Then `br t B3 B6` becomes `jump B6`, the loop body never runs, and the projection gives $p = 1$ at B6 for every $n$. For $n = 3$ the program gives 6, so this $K$ is not a slice. The control dependence of the loop body on the test is what forces the test into the slice.

**A dependence slice that is not minimal.**

```
B1:
  y = 1
  t = a * a
  c = t < 0
  br c B2 B3
B2:
  y = 2
  jump B3
B3:
  ret y
```

For $\langle (B3, 0), \{y\} \rangle$ the dependence slice holds all 5 instructions and branches, since `y = 2` may reach B3 and depends on the branch. But $a \cdot a \ge 0$ for every integer $a$, so $c = 0$ and B2 never runs. $K = \{$`y = 1`$\}$ is a slice of size 1, and it is statement-minimal, because with $K = \emptyset$ the variable $y$ is undefined at B3. To see this, a slicer must know that a square is never negative, which is a fact about values, not about the graph.

## Known algorithms

| algorithm | slice | method | cost for one criterion |
|---|---|---|---|
| [Weiser](/weiser-slicing/) (1981, 1984) | static, executable | iterated backward dataflow equations for relevant variables, plus branches | $O((c + 1)\, v\, (n + m))$ set operations for $c$ branches and $v$ variables |
| [dependence graph reachability](/pdg-slicing/) (Ottenstein and Ottenstein 1984) | static, set of nodes | backward reachability in the program dependence graph | $O(n + e)$ after the graph is built |
| [system dependence graph](/system-dependence-graph-slicing/) (Horwitz, Reps and Binkley 1990) | static, interprocedural | summary edges, then a two-phase backward traversal | linear in the size of the graph with its summary edges, after they are built |
| [dynamic slicing](/dynamic-slicing/) (Korel and Laski 1988; Agrawal and Horgan 1990) | one input | dependences seen in a trace of the run | linear in the size of the dependence graph of the trace |

Here $n$ is the number of statements, $m$ the number of control flow edges and $e$ the number of edges of the dependence graph.

## Bounds

**Minimal slices are not computable.** Weiser showed that no algorithm finds a statement-minimal slice for every program and criterion. A short proof in the toy IR follows.

*Proof.* The toy IR has unbounded integers and the operators `*`, `/` and `%`, so a toy IR program can simulate any Turing machine $M$ on a fixed input $w$: it keeps the two halves of the tape as two numbers in base $k$ and moves the head with multiplication, division and remainder. Build the program

```
B1:
  x = 0
  jump SIM
SIM:
  # the blocks that simulate M on w; they never read or write x
  ...
DONE:
  x = 1
  ret x
```

where the simulation jumps to DONE when $M$ halts, and every block of the simulation has a path to DONE. Take the criterion $\langle (DONE, 1), \{x\} \rangle$, the point before `ret x`. If $M$ halts on $w$, the program reaches that point once, with $x = 1$, and returns. Every slice must then keep `x = 1`, since without it $x$ is 0 or undefined there. The set $K = \{$`x = 1`$\}$ is a slice. In its projection every block other than DONE ends in a jump to its immediate post-dominator (a block with one successor has that successor as its immediate post-dominator), so every run climbs the post-dominator tree, reaches DONE, sets $x = 1$ and returns. So the minimal size is 1. If $M$ does not halt on $w$, the program never reaches a `ret`, the condition on slices is empty, and $K = \emptyset$ is a slice of size 0. So the minimal size is 1 if and only if $M$ halts on $w$. An algorithm that returns a minimal slice would decide the [halting problem](/halting-problem/), which is impossible. $\square$

The same argument, with "the slice keeps statement $s$" as the property, shows that no algorithm decides whether a given statement belongs to some or to every minimal slice: in the program above, `x = 1` is the only statement of the unique minimal slice when $M$ halts, and the unique minimal slice is empty when $M$ does not halt. The argument has the same shape as the proof of [Rice's theorem](/rice-theorem/).

**Dependence slices are cheap.** Given the program dependence graph, the dependence slice is one backward search, so it costs $O(n + e)$ time. The graph itself can have $\Theta(n^2)$ edges, as the [program dependence graph](/program-dependence-graph/) page shows, so building it dominates when only a few slices are needed.

## Reductions

- **From halting.** The proof above reduces the halting problem to finding a minimal slice.
- **To graph reachability.** A dependence slice is the set of nodes from which the criterion node is reachable in the program dependence graph ([graph reachability](/graph-reachability/)).
- **To CFL reachability.** With procedures, a precise slice is the set of nodes that reach the criterion by a path whose call and return edges match, which is a [CFL reachability](/cfl-reachability/) problem over a Dyck language of call sites (Reps 1998).
- **Dead code.** [Aggressive dead code elimination](/aggressive-dead-code-elimination/) keeps exactly the slice of all output statements and removes the rest.

## Applications

- **Debugging.** Weiser's motivation: the statements outside the slice of a wrong value cannot be the cause. Dynamic slices narrow this to the statements that acted in the failing run.
- **Program understanding and maintenance.** A slice shows which code computes one output, and a forward slice shows what a change can affect.
- **Testing.** After a change, only the tests whose outputs have the changed statement in their slice need to run again.
- **Optimization.** Dead code removal and the extraction of independent computations for parallel execution both use slices of the dependence graph.
