---
tag: CX734T
kind: problem
slug: partial-redundancy-elimination
name: Partial redundancy elimination
aliases:
- PRE
area: compilers-and-program-analysis/optimizations
level: core
summary: Insert and remove computations so that no expression is computed twice on any path, which subsumes CSE and loop-invariant code motion.
prereqs: [common-subexpression-elimination, loop-invariant-code-motion, available-expressions, control-flow-graph]
see_also: [lazy-code-motion, ssapre, global-value-numbering, very-busy-expressions, critical-edge-splitting, strength-reduction, register-allocation-problem, profile-guided-optimization]
sources:
  - paper: doi:10.1145/359060.359069
    title: "Etienne Morel and Claude Renvoise, Global optimization by suppression of partial redundancies, Communications of the ACM 22(2), 1979, 96-103"
    locator: the whole paper (the problem of partial redundancy, the safety condition, and the first algorithm, a bidirectional system of bit-vector equations)
  - paper: doi:10.1145/143095.143136
    title: "Jens Knoop, Oliver Rüthing and Bernhard Steffen, Lazy code motion, Proceedings of the ACM SIGPLAN 1992 Conference on Programming Language Design and Implementation (PLDI 1992)"
    locator: the whole paper (computational and lifetime optimality as the goals of code motion, and an algorithm that reaches both)
  - paper: doi:10.1145/183432.183443
    title: "Jens Knoop, Oliver Rüthing and Bernhard Steffen, Optimal code motion: theory and practice, ACM Transactions on Programming Languages and Systems 16(4), 1994, 1117-1155"
    locator: the definitions of safe, correct, computationally optimal and lifetime optimal placements, and the proofs
  - paper: doi:10.1145/258915.258940
    title: "Fred Chow, Sun Chan, Robert Kennedy, Shin-Ming Liu, Raymond Lo and Peng Tu, A new algorithm for partial redundancy elimination based on SSA form, Proceedings of the ACM SIGPLAN 1997 Conference on Programming Language Design and Implementation (PLDI 1997), 273-286"
    locator: the whole paper (PRE on SSA form, one expression at a time)
  - paper: doi:10.1145/319301.319348
    title: "Robert Kennedy, Sun Chan, Shin-Ming Liu, Raymond Lo, Peng Tu and Fred Chow, Partial redundancy elimination in SSA form, ACM Transactions on Programming Languages and Systems 21(3), 1999, 627-676"
    locator: the whole paper (the full SSAPRE algorithm with proofs, and its use for loads, stores and strength reduction)
  - book: isbn:9780321486813
    title: "Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers: Principles, Techniques, and Tools, 2nd edition, Addison-Wesley, 2006"
    locator: Section 9.5 (Partial-Redundancy Elimination, with the sources of redundancy, whether all redundancy can be removed, critical edges, and lazy code motion)
  - url: "https://llvm.org/docs/Passes.html"
    title: LLVM Project, LLVM's Analysis and Transform Passes, LLVM documentation
    locator: the entry for -gvn (global value numbering that removes fully and partially redundant instructions and redundant loads)
---

Partial redundancy elimination (PRE) asks where to compute each expression so that it is computed as few times as possible on every path through a procedure. A computation is *partially redundant* if the same value was already computed on some, but not all, paths that reach it. PRE removes it by inserting the computation on the other paths, at places where it does no extra work, and by reading the result from a temporary.

## In plain words

Say a program computes `a + b` in one branch of an `if`, and again after the two branches join. On the path through the other branch it is computed once, which is fine. On the path through the first branch it is computed twice, which is a waste.

The fix is to compute `a + b` on the second branch as well, store the value in a temporary on both branches, and read the temporary after the join. Now every path computes it once.

The hard part is where to put the new computations. A new computation must not go on a path that did not compute the expression before, because it can add work or even make the program crash, for example by dividing by zero. And among the good places, a late one is better, because the temporary then holds a register for a shorter time.

## Definition

Work on the flow graph with one node for each instruction and one for each terminator, from an entry node $s$. Fix an expression $e = a \mathbin{op} b$, as text. $\mathrm{Comp}(n)$ says that node $n$ is `x = e`, and $\mathrm{Transp}(n)$ says that $n$ does not assign $a$ or $b$. A *complete path* goes from $s$ to a `ret` node.

- A node $n$ is *down-safe* if every path from $n$ to a `ret` reaches a $\mathrm{Comp}$ node through transparent nodes, and *up-safe* if every path from $s$ to $n$ passes a $\mathrm{Comp}$ node and then only transparent nodes. It is *safe* if it is one of the two.
- A *placement* is a set $I$ of nodes. Its program computes `t = e` just before each node of $I$, into a new name $t$, and replaces each `x = e` by `x = t`.
- The placement is *admissible* if every node of $I$ is safe and, on every path from $s$ to a $\mathrm{Comp}$ node $m$, some node of $I$ comes before $m$ with only transparent nodes between them.

**Input:** a procedure and an expression $e$ (or all of its expressions, one at a time).

**Output:** an admissible placement $I$ that is *computationally optimal*: for every admissible placement $J$ and every complete path $p$, the number of positions of $I$ on $p$ is at most that of $J$. The usual second goal is *lifetime optimality*: among the computationally optimal placements, the set of nodes after which $t$ is live is the smallest.

It is not clear at first that one placement can be best on all paths at once, since doing better on one path might cost on another. Knoop, Rüthing and Steffen proved that it can be, provided the critical edges are split, and that among the best placements one has the shortest lifetimes. The proof is on the page of [lazy code motion](/lazy-code-motion/).

Safety is part of the problem, not a detail. An insertion at a node that is not safe can put a computation on a path that never computed $e$. That path then does more work, and if $e$ can trap, as `a / b` can in the toy IR, the program can trap on an input on which it used to return.

PRE subsumes [common subexpression elimination](/common-subexpression-elimination/) and [loop-invariant code motion](/loop-invariant-code-motion/). A fully redundant computation, which CSE removes, is the case in which every path already computes $e$, so PRE needs no insertion. A loop-invariant computation is redundant on the back edge and not on the edge into the loop, so it is partially redundant at the loop header, and PRE inserts it on the edge into the loop.

## Variants

- **Lexical or value-based.** The classic problem treats $e$ as text. Value-based PRE works on the classes of [global value numbering](/global-value-numbering/), so `x + y` and `u + v` count as one expression when $x = u$ and $y = v$ on all runs.
- **Safe or speculative.** Speculative PRE allows insertions that are not safe, for expressions that cannot trap, and minimizes the expected count under a [profile](/profile-guided-optimization/) instead of the count on every path.
- **Node or edge placement.** Inserting on edges instead of nodes needs no split blocks. It is the same problem on the graph with the critical edges split.
- **Complete PRE.** Some redundancy cannot be removed by any safe placement. Duplicating code, for example to peel the first iteration of a loop, can make it removable.
- **Memory operations.** Loads can be treated like expressions, with stores and calls as kills, if alias analysis says which stores can change the loaded cell. Stores can be sunk with the dual problem.
- **Strength reduction.** With $i \cdot c$ as the expression and $i = i + 1$ as an update instead of a kill, PRE also does [strength reduction](/strength-reduction/).

## Examples

**A diamond.** The parameters are `a`, `b` and `c`.

```
B0:
  br c B1 B2
B1:
  x = a + b
  jump B3
B2:
  x = 0
  jump B3
B3:
  y = a + b
  r = x + y
  ret r
```

`a + b` in `B3` is redundant on the path through `B1` and not on the path through `B2`. The optimal placement inserts it at the end of `B2` and reads the temporary in `B3`:

```
B1:
  pre.0 = a + b
  x = pre.0
  jump B3
B2:
  x = 0
  pre.0 = a + b
  jump B3
B3:
  y = pre.0
  r = x + y
  ret r
```

The path through `B1` now computes `a + b` once instead of twice, and the path through `B2` still computes it once.

**A loop whose body runs at least once.** The parameters are `a`, `b` and `n`.

```
B0:
  i = 0
  jump B1
B1:
  x = a / b
  i = i + 1
  c = i < n
  br c B1 B2
B2:
  ret x
```

`a / b` is the same on every trip. It is down-safe at the end of `B0`, because every path from there divides before `a` or `b` changes, so PRE moves it there, and `B1` starts with `x = pre.0`. For $n = 3$ the division runs once instead of three times. With $b = 0$ both programs trap.

**A loop that may not run.** Put the test first:

```
B0:
  i = 0
  jump B1
B1:
  c = i < n
  br c B2 B3
B2:
  x = a / b
  i = i + 1
  jump B1
B3:
  ret i
```

Now the end of `B0` is not down-safe: for $n = 0$ the program returns 0 without a division. A division there would trap for $b = 0$. So no admissible placement takes `a / b` out of the loop, and safe PRE leaves it alone. The section on bounds proves it.

## Known algorithms

| algorithm | year | form | notes |
|---|---|---|---|
| Morel and Renvoise | 1979 | bit vectors | the first method; bidirectional equations, not always computationally optimal |
| busy code motion | 1992 | bit vectors | inserts at the earliest safe points; computationally optimal, long lifetimes |
| [lazy code motion](/lazy-code-motion/) | 1992 | bit vectors | four unidirectional analyses; computationally and lifetime optimal |
| [SSAPRE](/ssapre/) | 1997 | SSA form | sparse, one expression at a time; the same optimality on SSA form |
| PRE on value numbers | 2000s | SSA form | works on classes of global value numbering, so it removes redundancy between different names |

Many compilers do a simple PRE as part of their global value numbering pass. LLVM's `-gvn` pass, for example, removes fully and partially redundant instructions and redundant loads.

## Bounds

Let $n$ be the number of nodes and $m$ the number of expressions.

- **An optimum exists.** With critical edges split, there is an admissible placement that is computationally optimal on all complete paths at once, and among those, one with the least lifetimes. Lazy code motion builds it.
- **Time.** Lazy code motion needs four bit-vector analyses. Each pass costs $O(n m)$ bit operations, and round-robin iteration needs at most $n + 1$ passes, so the time is $O(n^2 m)$, and close to $O(n m)$ on the loop depths of real programs. SSAPRE works on the occurrences of one expression at a time in SSA form, with work close to linear in the size of the SSA graph of that expression.
- **Safe PRE cannot remove all redundancy.** In the loop that may not run, every admissible placement evaluates `a / b` once in each trip of the loop.

  *Proof.* The nodes of `B0` and `B1` are not down-safe, because the path $B0, B1, B3$ never divides. They are not up-safe, because the path from the entry to them has no division before its first trip. Validity at the division on the path $B0, B1, B2$ asks for a node of the placement on that path, at or before the division. The only safe one is the division itself, so it is in the placement. Every trip of the loop passes this node, so each trip evaluates `a / b` once. $\square$

  The redundancy across trips is still there. Turning the loop into a test followed by a loop that runs at least once makes it removable, which is the complete PRE of the variants.

## Reductions

- **CSE and loop-invariant code motion reduce to PRE**, as shown in the definition.
- **PRE splits by expression.** Lexical PRE for $m$ expressions is $m$ independent problems, one for each expression, since the sets of different expressions never interact. Bit vectors solve them side by side, and SSAPRE solves them one by one.
- **Value-based PRE reduces to lexical PRE** after the program is rewritten so that each value class of [global value numbering](/global-value-numbering/) has one name.
- **Placement is a dataflow problem.** Down-safety is the [very busy expressions](/very-busy-expressions/) analysis, and up-safety is an [available expressions](/available-expressions/) analysis. The placement step needs no search.

## Applications

- **Global redundancy elimination in compilers.** One PRE pass replaces separate passes for CSE and for hoisting loop invariants.
- **Loads and stores.** PRE of loads removes repeated memory reads in loops when alias analysis proves that no store in between can change the cell.
- **Strength reduction and address arithmetic.** PRE moves array index computations out of loops, and with the update rule it can replace a multiplication by additions.
- **JIT compilers.** Value-based PRE on SSA form fits compilers that already keep SSA form and value numbers.

## References
