---
tag: AQQH48
kind: algorithm
slug: lazy-code-motion
name: Lazy code motion
aliases:
- Knoop-Ruthing-Steffen algorithm
area: compilers-and-program-analysis/optimizations
level: core
summary: Solves PRE with unidirectional bit-vector analyses, placing each computation as late as possible to keep register pressure low.
solves: [partial-redundancy-elimination]
model: word-ram
complexity:
  vars: {n: the number of nodes of the flow graph (one per instruction and terminator), m: the number of distinct expressions}
  time: {worst: O(n^2 m)}
  space: {extra: Θ(n m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [available-expressions, very-busy-expressions, critical-edge-splitting, dataflow-analysis]
see_also: [ssapre, common-subexpression-elimination, loop-invariant-code-motion, global-value-numbering, register-allocation-problem, mop-mfp-coincidence-theorem, kam-ullman-iteration-bound, live-variable-analysis]
sources:
  - paper: doi:10.1145/143095.143136
    title: "Jens Knoop, Oliver Rüthing and Bernhard Steffen, Lazy code motion, Proceedings of the ACM SIGPLAN 1992 Conference on Programming Language Design and Implementation (PLDI 1992)"
    locator: the whole paper (down-safety and earliestness, the delay and isolation analyses, and the claims of computational and lifetime optimality)
  - paper: doi:10.1145/183432.183443
    title: "Jens Knoop, Oliver Rüthing and Bernhard Steffen, Optimal code motion: theory and practice, ACM Transactions on Programming Languages and Systems 16(4), 1994, 1117-1155"
    locator: the whole paper (the full proofs of safety, computational optimality and lifetime optimality, and busy code motion as the first step)
  - paper: doi:10.1145/359060.359069
    title: "Etienne Morel and Claude Renvoise, Global optimization by suppression of partial redundancies, Communications of the ACM 22(2), 1979, 96-103"
    locator: the whole paper (the first formulation of partial redundancy elimination, with a bidirectional system of equations)
  - book: isbn:9780321486813
    title: "Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers: Principles, Techniques, and Tools, 2nd edition, Addison-Wesley, 2006"
    locator: Section 9.5 (Partial-Redundancy Elimination, the lazy code motion algorithm with anticipated, available, postponable and used expressions)
  - book: isbn:9780128154120
    title: "Keith D. Cooper and Linda Torczon, Engineering a Compiler, 3rd edition, Morgan Kaufmann, 2022"
    locator: Section 10.3.1 (Lazy Code Motion)
---

Lazy code motion (LCM) is an algorithm for [partial redundancy elimination](/partial-redundancy-elimination/) by Knoop, Rüthing and Steffen. It finds the places where an expression can be computed so that no path computes it more often than before, and it picks the latest of these places, so the temporary that holds the value lives as short a time as possible. It uses four simple bit-vector [dataflow analyses](/dataflow-analysis/), each in one direction, where the first PRE method of Morel and Renvoise needed one bidirectional system. It needs the [critical edges](/critical-edge-splitting/) of the flow graph split.

## In plain words

Look at one expression, such as `a * b`. One branch computes it and the code after the join computes it again, while the other branch does not compute it.

First find the places where the value will surely be needed later on every path, before `a` or `b` changes. Putting the computation there cannot add work to any path. Among these places, take the first ones that are not already covered by a computation above. Putting the computation there removes as many computations as can be removed.

Then push each computation down, as long as it still covers the same uses and no path gets an extra copy. Stop at the last place where it can go. At that place, store the value in a new temporary, and let every old computation read the temporary. A late computation keeps the temporary alive briefly, so it needs fewer registers.

## The problem

The input is a procedure of the toy IR with const, copy and op instructions and any control flow. An expression is the text `a op b` of an op instruction, so `a + b` and `b + a` are different expressions. The output is a program that gives the same result or trap on every input that ends, and in which every path from the entry to a `ret` evaluates each expression at most as often as before. Among all such programs that only compute at safe places, LCM wants one with the fewest evaluations on every path at once, and among those, one with the shortest life for each temporary.

## The algorithm

The algorithm works on a graph with one node for each instruction and one for each terminator. A node computes an expression if it is `x = e`, and it kills every expression with an operand that it defines. All sets are bit vectors with one bit per expression.

```pseudo id=main
LCM(P)
L1  remove unreachable blocks, give the entry no predecessor, and split every critical edge
L2  for each node n: USE[n] <- the expression n computes; KILL[n] <- the expressions with an operand defined at n
L3  ANT.out[n] = ∩ ANT.in[s] over successors s (∅ at a ret); ANT.in[n] = USE[n] ∪ (ANT.out[n] \ KILL[n])
L4  AV.in[n] = ∩ AV.out[p] over predecessors p (∅ at the entry); AV.out[n] = (ANT.in[n] ∪ AV.in[n]) \ KILL[n]
L5  EARLIEST[n] <- ANT.in[n] \ AV.in[n]
L6  POST.in[n] = ∩ POST.out[p] (∅ at the entry); POST.out[n] = (EARLIEST[n] ∪ POST.in[n]) \ USE[n]
L7  LATEST[n] <- (EARLIEST[n] ∪ POST.in[n]) ∩ (USE[n] ∪ not ∩ (EARLIEST[s] ∪ POST.in[s]) over successors s)
L8  USED.out[n] = ∪ USED.in[s]; USED.in[n] = (USE[n] ∪ USED.out[n]) \ LATEST[n]
L9  for each node n and each e in LATEST[n] ∩ USED.out[n]: insert t_e = e before n
L10 for each node n that is x = e
L11     if e is not in LATEST[n], or e is in USED.out[n], then replace it by x = t_e
L12 return P
```

Each equation of lines L3, L4, L6 and L8 is solved by iteration to a fixed point. The intersections start from the full set and the union starts from the empty set.

- ANT (line L3) is the anticipated or [very busy](/very-busy-expressions/) analysis. $e \in \mathrm{ANT.in}[n]$ says that every path from $n$ computes $e$ before an operand changes. Such a node is *down-safe*, and a computation there adds no work to any path.
- AV (line L4) is [availability](/available-expressions/) under the guess that $e$ is computed at every down-safe point. EARLIEST (line L5) keeps the down-safe points where $e$ is not yet available. Inserting there and replacing every old computation is *busy code motion*, which is already computationally optimal.
- POST (line L6) moves the computation down. $e \in \mathrm{POST.in}[n]$ says that on every path to $n$ an earliest point came before, with no use of $e$ since then. LATEST (line L7) is the last such node: it uses $e$, or one of its successors cannot take the computation.
- USED (line L8) is a [liveness](/live-variable-analysis/) analysis for the temporary. If a latest point computes $e$ and no later node reads the temporary, line L11 keeps `x = e` and no temporary is made.

## Example

The parameters are `a`, `b` and `n`.

```
B0:
  i = 0
  br n B1 B2
B1:
  x = a * b
  jump B3
B2:
  a = a + 1
  jump B3
B3:
  i = i + 1
  y = a * b
  c = i < n
  br c B3 B4
B4:
  z = a * b
  ret z
```

The edge from `B3` to itself is critical, so line L1 adds a block `B3_B3` that only jumps to `B3`. The analyses give these points.

| expression | EARLIEST | LATEST | inserted at |
|---|---|---|---|
| `a * b` | start of `B1`; end of `B2`, after `a = a + 1` | the same | the same |
| `i + 1` | end of `B0`, after `i = 0`; `B3_B3` | `i = i + 1` in `B3` | nowhere |
| `i < n` | `y = a * b` in `B3` | `c = i < n` in `B3` | nowhere |
| `a + 1` | `a = a + 1` in `B2` | the same | nowhere |

The expression `a * b` is not anticipated in `B0`, because `B2` changes `a` before any use. So the two earliest points are in the branches. In `B3`, `a * b` is available from both branches and from the back edge, so the computation leaves the loop. The result is:

```
B1:
  pre.0 = a * b
  x = pre.0
  jump B3
B2:
  a = a + 1
  pre.0 = a * b
  jump B3
B3:
  i = i + 1
  y = pre.0
  c = i < n
  br c B3_B3 B4
B3_B3:
  jump B3
B4:
  z = pre.0
  ret z
```

On the input $a = 2$, $b = 3$, $n = 3$ the loop runs three times, and the operations run drop from 11 to 7, all from `a * b`.

Busy code motion evaluates every expression as often as LCM on every path, but it makes three more temporaries. It computes `i + 1` at the end of `B0` and on the back edge, so `pre.2` lives from `B0` through `B1` or `B2` into `B3`. It also sends `a + 1` through a temporary and computes `i < n` one instruction early. LCM leaves these three computations at their old places, where no temporary is needed.

## Correctness

The proof file has the full proof. It fixes one expression and reads each analysis as a statement about all paths, which is exact for these bit-vector problems by the [MOP and MFP coincidence theorem](/mop-mfp-coincidence-theorem/).

- **Safety.** Every insertion is at a down-safe node. If it traps, the old program, which goes on from the same state, either traps on the way or reaches a computation of the same expression with the same operands, which traps too. A replaced `x = e` reads a temporary that was computed from the same operand values without a trap. So on every input on which the old program ends, the new program returns the same value or also traps.
- **Computational optimality.** On a path from the entry to a `ret`, each earliest point starts a *segment* that ends at the next computation of $e$. Every safe and correct placement must compute $e$ inside each segment, because the earliest point has a path from the entry on which $e$ is not available. The segments are disjoint, so no placement does better than one computation per segment. LCM has exactly one computation in each segment.
- **Lifetime optimality.** A placement with the same counts as LCM has exactly one computation in each segment, and it is never after the LCM point. So wherever the LCM temporary is live, the other temporary is live too.

The proof uses the split edges in three lemmas. After the split, a node with two predecessors has predecessors with one successor each. So the end of a branching block never needs a computation that only one of its successors wants.

## Complexity

Let $n$ be the number of nodes and $m$ the number of expressions. Each node has at most two successors, so a pass of any of the four iterative analyses costs $O(n m)$ bit operations, which is $O(n \lceil m / w \rceil)$ word operations on a machine with $w$-bit words. A round-robin pass in a good order reaches the fixed point after a number of passes bounded by the loop depth plus two, by the [Kam and Ullman bound](/kam-ullman-iteration-bound/), which is at most $n + 1$. So the worst case is $O(n^2 m)$ and the usual case is close to $O(n m)$. The sets take $\Theta(n m)$ bits. Working on basic blocks instead of single instructions, with local summary sets for each block, divides $n$ by the block length.

## Properties

- **Safe.** It never inserts a computation on a path that would not compute the expression later with the same operands.
- **Computationally optimal.** No safe placement evaluates any expression fewer times on any path.
- **Lifetime optimal.** Among the computationally optimal placements, its temporaries are live at the fewest points, for each expression on its own.
- **Unidirectional.** Each analysis goes only forward or only backward, so standard bit-vector solvers work.
- **Lexical.** It moves the text `a op b`. It does not see that two names hold the same value, so copies or SSA renaming can hide redundancy.
- **Never more evaluations.** The old program is one of the placements, so no path evaluates an expression more often than before.

## Variants and improvements

- **Block level.** The textbook form computes the sets for whole basic blocks, with local summaries for the upward-exposed and downward-exposed uses, and inserts at the start or end of a block.
- **SSA form.** [SSAPRE](/ssapre/) gets the same placement on SSA form, one expression at a time, with sparse graphs instead of bit vectors.
- **Value-based PRE.** Running PRE on the classes of [global value numbering](/global-value-numbering/) instead of on lexical expressions finds redundancy that renaming hides.
- **Speculation.** With profile data, a compiler can give up safety on cold paths and insert computations that cannot trap where they pay off on hot paths.
- **Partial dead code.** Knoop, Rüthing and Steffen used the same delay idea in the other direction, to sink assignments that are dead on some paths.

## When to use it

Use LCM as the global redundancy pass of a compiler that works on a flow graph without SSA, or with SSA names mapped back to lexical expressions. It removes common subexpressions and moves loop-invariant code in one pass, and it does not lengthen live ranges the way busy hoisting does. On SSA form, SSAPRE is often the simpler fit. If most redundancy is between different names with equal values, run [global value numbering](/global-value-numbering/) first.

## Pitfalls

- **Critical edges.** In this program `a / b` is partially redundant at `B3`, but `B2 -> B3` is a critical edge.

  ```
  B0:
    br c B1 B2
  B1:
    x = a / b
    jump B3
  B2:
    br d B3 B4
  B3:
    y = a / b
    ret y
  B4:
    ret 0
  ```

  The computation cannot go into `B2`, because the path to `B4` does not divide, and `b` can be 0 there. The start of `B3` is too late. Only a new block on the edge can take it, and LCM puts `pre.0 = a / b` there.
- **Loops that may not run.** In a `while` loop whose test comes first, `a / b` in the body is not down-safe at the loop entry, because the loop can exit at once. LCM leaves it in the loop. Turning the loop into a test followed by a `do-while` loop makes the computation down-safe in the guarded block.
- **Runs that never end.** Safety looks at paths that reach a `ret`. If a run passes an insertion and then loops forever, the new program can trap where the old one only ran forever.
- **An operand defined by the same node.** `a = a + b` uses $e$ and kills it. The insertion goes before the node, and the expression is not available after it.
- **Optimal per expression only.** Lifetime optimality holds for each temporary alone. Many temporaries can still raise the register pressure, and the copies `x = t` need [copy propagation](/copy-propagation/) or coalescing afterwards.

## Implementations

## History

Morel and Renvoise introduced partial redundancy elimination in 1979, with a bidirectional system of equations that was hard to solve and could move computations higher than needed. Knoop, Rüthing and Steffen presented lazy code motion at PLDI 1992. They split the problem into busy code motion, which is computationally optimal, and a delay step, which makes it lifetime optimal, and they showed that unidirectional analyses suffice. The full proofs appeared in TOPLAS in 1994. The second edition of the Dragon book presents the block-level form with anticipated, available, postponable and used expressions, and Chow and colleagues carried the same results to SSA form with SSAPRE in 1997.

## References
