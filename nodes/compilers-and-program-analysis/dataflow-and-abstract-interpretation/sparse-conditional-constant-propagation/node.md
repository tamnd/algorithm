---
tag: WNK50T
kind: algorithm
slug: sparse-conditional-constant-propagation
name: Sparse conditional constant propagation
aliases:
- SCCP
- Wegman-Zadeck algorithm
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Propagates constants over SSA edges and executable flow edges together, so it ignores branches that constants prove dead.
solves: [constant-propagation-problem]
model: word-ram
complexity:
  vars: {n: the number of instructions in SSA form, m: the number of CFG edges, s: the number of SSA edges, d: the largest number of predecessors of a block}
  time: {worst: O(n + m + s d), average: O(n + m + s d), best: Θ(n + s)}
  space: {extra: Θ(n + m + s)}
properties: {deterministic: true, recursive: false}
prereqs: [constant-propagation-problem, static-single-assignment-form, worklist-dataflow-algorithm]
see_also: [cytron-ssa-construction, def-use-chains, dead-code-elimination, constant-folding, global-value-numbering, interprocedural-constant-propagation, ide-framework, knaster-tarski-theorem]
sources:
  - paper: doi:10.1145/103135.103136
    title: "Mark N. Wegman and F. Kenneth Zadeck, Constant propagation with conditional branches, ACM Transactions on Programming Languages and Systems 13(2), 1991, 181-210"
    locator: Section 3 (the four algorithms SC, SSC, CC and SCC), Section 3.4 and 3.4.1 (the algorithm and its cost, each SSA edge examined at most twice), Section 4 (conservative and at least as strong as CC), Section 5.1 (optimistic and pessimistic algorithms)
  - paper: doi:10.1145/318593.318659
    title: "Mark N. Wegman and F. Kenneth Zadeck, Constant propagation with conditional branches, Proceedings of the 12th ACM Symposium on Principles of Programming Languages (POPL 1985), 291-299"
    locator: the whole paper (the first version)
  - paper: doi:10.1109/tse.1975.6312852
    title: "Ben Wegbreit, Property extraction in well-founded property sets, IEEE Transactions on Software Engineering SE-1(3), 1975, 270-285"
    locator: Algorithm 3.1, the dense conditional algorithm that Wegman and Zadeck call CC
  - paper: doi:10.1145/115372.115320
    title: "Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, 451-490"
    locator: the whole paper (the SSA construction that the implementation uses)
  - paper: doi:10.1145/201059.201061
    title: "Cliff Click and Keith D. Cooper, Combining analyses, combining optimizations, ACM Transactions on Programming Languages and Systems 17(2), 1995, 181-196"
    locator: the whole paper (combining two analyses into one optimistic analysis, with constant propagation and unreachable code as the main case)
---

Sparse conditional constant propagation (SCCP) solves the [constant propagation problem](/constant-propagation-problem/) on a program in [static single assignment form](/static-single-assignment-form/). It keeps two worklists. One holds edges of the [control flow graph](/control-flow-graph/) that may run. The other holds SSA edges, from the one definition of a name to a use of it. The algorithm starts with every name at $\top$, "no value seen yet", and only the entry reachable. It looks at an instruction only after some executable edge reaches its block. A branch whose condition is a known constant makes only one of its edges executable. So a constant can prove a branch dead, and the dead branch then cannot spoil other constants. The result is the greatest fixed point of one combined system for values and reachability. It is at least as strong as simple constant propagation and dead branch elimination run one after the other in any order and as often as you like, and it can be strictly stronger when the program has a loop. Each SSA edge goes through the worklist at most twice, so the work is close to linear in the size of the SSA form.

## In plain words

Assume at first that every variable is a constant whose value is not known yet, and that no code runs except the first block. Then follow the program forward. When a block becomes reachable, work out its instructions. When a value becomes known, tell every instruction that reads it. When a branch tests a known value, mark only the side it will take as reachable. A variable only gets less hopeful over time: unknown, then one constant, then "not a constant". So the work ends soon. Code that never becomes reachable is never looked at, and its assignments cannot spoil the constants in the code that does run.

## The problem

The input is a program in strict SSA form: every name has one definition, which dominates its uses. The output gives every name a value in the flat constant lattice, and marks the CFG edges and blocks that may run. The analysis uses the meet convention of Kildall: $\top$ is the start value and the result is a greatest fixed point. Flipping the order gives the join convention of Cousot, with $\bot$ as the start value and a least fixed point; the result is the same.

| item | choice |
|---|---|
| direction | forward, along SSA edges and CFG edges |
| may or must | must: a constant holds on every run that reaches the definition |
| domain | for each SSA name, a value in $\{\top\} \cup \mathbb{Z} \cup \{\bot\}$; for each CFG edge, executable or not |
| order | $\bot \sqsubseteq c \sqsubseteq \top$, constants pairwise incomparable; for edges, fewer executable edges is higher |
| meet | $c \sqcap c = c$, $c \sqcap c' = \bot$ for $c \ne c'$, $\top$ is the identity |
| $\top$ and $\bot$ | $\top$: no value seen yet; $\bot$: not a constant |
| boundary | parameters are $\bot$; the pseudo edge into the entry is executable |
| initial value | every other name is $\top$; every other edge is not executable |
| transfer functions | monotone; not distributive, as for [constant propagation](/constant-propagation-problem/) |
| height | 2 per name, 1 per edge |

**Lattice and transfer functions.** A state is a pair $(V, E)$ of values and executable edges, ordered by "higher values and fewer edges". An instruction $x = a \mathbin{op} c$ gets $fold(op, V[a], V[c])$: any $\top$ operand gives $\top$, else any $\bot$ operand gives $\bot$, else the operation runs, and an operation that would trap, such as division by zero, gives $\bot$. A [phi-function](/phi-function/) $x = \phi[p_1: a_1, \ldots]$ in block $b$ gets the meet of $V[a_i]$ over the operands whose edge $(p_i, b)$ is in $E$. A call gives $\bot$. A branch `br a L1 L2` allows both edges if $V[a] = \bot$, only the edge picked by $c$ if $V[a] = c$ (nonzero picks `L1`), and none if $V[a] = \top$.

**Equations.** The combined map $\Phi(V, E)$ recomputes every value from $V$ and $E$, gives $\top$ to the names of blocks that no edge in $E$ reaches, and makes $E$ the pseudo edge plus the edges that the terminators of reached blocks allow. $\Phi$ is monotone, so by the [Knaster-Tarski theorem](/knaster-tarski-theorem/) it has a greatest fixed point. SCCP computes it.

**MOP and soundness.** The [meet-over-all-paths solution](/meet-over-all-paths-solution/) is the ideal answer, and as for every constant propagation it is not computable in general. The fixed point found here is sound for real runs: every block a run enters is reachable in the result, every edge it takes is executable, and every value it assigns to a name with a constant result is that constant. The proof file has the details.

**Precision.** Simple constant propagation is the same analysis with every edge executable, which is the [maximal fixed point](/maximal-fixed-point-solution/) of the usual framework. SCCP is never below it, and the example below shows a case where it is strictly above it and also above any mix of it with dead branch elimination.

**Cost.** The cost is $O(n + m + s d)$ for $n$ SSA instructions, $m$ CFG edges, $s$ SSA edges and at most $d$ predecessors per block. See the section on complexity.

## The algorithm

The analysis needs the SSA form, a list of the uses of each name, and a flag per CFG edge. Both worklists are queues. A CFG edge is put on FlowWL at most once; a set of edges seen before checks that.

```pseudo id=main
SCCP(P)    P is in strict SSA form
L1  for each parameter p do V[p] ← ⊥; for each other name x do V[x] ← ⊤
L2  Exec ← ∅; Visited ← ∅
L3  FlowWL ← [(start, entry)]; SSAWL ← []
L4  while FlowWL or SSAWL is not empty do
L5      if FlowWL is not empty then
L6          (p, b) ← remove the first edge of FlowWL
L7          add (p, b) to Exec; VISIT every phi of b
L8          if b ∉ Visited then add b to Visited; VISIT every other instruction of b, then its terminator
L9      else (x, u) ← remove the first SSA edge of SSAWL
L10         if the block of u is in Visited then VISIT(u)

VISIT(u), for an instruction or terminator u of block b
L11     if u is x = phi[p1: a1, ...] then new ← ⊓ of V[ai] over the i with (pi, b) ∈ Exec
L12     if u is x = a op c then new ← fold(op, V[a], V[c])   (x = k gives k, a copy gives V[a], a call gives ⊥)
L13     if new ≠ V[x] then V[x] ← new; append (x, w) to SSAWL for each use w of x
L14     if u is br a L1 L2 then: if V[a] = ⊥ then PUSH (b, L1) and (b, L2); if V[a] = c then PUSH the edge that c picks
L15     if u is jump L then PUSH (b, L)
    return V, Exec, Visited
```

PUSH appends an edge to FlowWL unless it was appended before. A use $w$ at line L13 is a use site: if one instruction reads $x$ twice, as in `y = x + x`, there is one SSA edge, not two.

After the analysis, a rewrite applies the result. Every name with a constant value gets the definition `x = c`, and every use of it reads `c`. A branch whose condition is a constant becomes a jump. Blocks outside $Visited$ go away, and so do the phi operands of edges outside $Exec$. Lemma 6 of the proof shows that no name in a reachable block keeps $\top$, so the rewrite never meets a branch with no allowed edge.

## Example

This loop sets `i = 1`, and the only other store to `i` is in a branch that runs when `i` is not 1. The parameter is `n`.

```
entry:
  i = 1
  k = 0
  jump head
head:
  c = i == 1
  br c same other
same:
  jump latch
other:
  i = 2
  jump latch
latch:
  k = k + 1
  t = k < n
  br t head exit
exit:
  ret i
```

In pruned SSA form, `head` gets `i.2 = phi [entry: i.1, latch: i.4]` and `k.2 = phi [entry: k.1, latch: k.3]`, and `latch` gets `i.4 = phi [same: i.2, other: i.3]`, where `i.3 = 2` is in `other`. The run:

| step | item taken | what changes | edges pushed |
|---|---|---|---|
| 1 | flow (start, entry) | i.1 = 1, k.1 = 0 | (entry, head) |
| 2 | flow (entry, head) | phis over the one executable edge: i.2 = 1, k.2 = 0; then c.1 = 1 | (head, same) only, since c.1 is the constant 1 |
| 3 | flow (head, same) | nothing | (same, latch) |
| 4 | flow (same, latch) | i.4 = 1 (only the edge from `same` is executable), k.3 = 1, t.1 = ⊥ | (latch, head) and (latch, exit) |
| 5 | flow (latch, head) | i.2 stays 1, since 1 ⊓ 1 = 1; k.2 = 0 ⊓ 1 = ⊥ | none |
| 6 | flow (latch, exit) | the `ret` reads i.4 | none |
| 7 to 20 | 14 SSA edges | only k.3 changes, from 1 to ⊥ | none |

The edge `(head, other)` never becomes executable, so `i.3` stays $\top$ and `other` is never visited. The result has `i.2 = i.4 = 1` and `c.1 = 1`. The rewrite drops `other`, turns the branch in `head` into `jump same`, and ends with `ret 1`. The run takes 6 flow items and 14 SSA items, and it does 29 visits.

Simple constant propagation counts every edge. It gets `i.4 = i.2 ⊓ 2 = ⊥` around the loop, so `i.2 = 1 ⊓ ⊥ = ⊥` and `c.1 = ⊥`. Dead branch elimination needs a literal condition, so it does nothing. Running the two passes again changes nothing, in either order. The value 1 holds on every run, but only an analysis that assumes the branch is dead while it studies the loop can prove it. In a program without loops this gap closes: there the two passes, repeated until nothing changes, reach the same result as SCCP.

## Correctness

The full proof is in the proof file. Its steps:

1. **Φ is monotone.** A phi meets fewer operands when fewer edges are executable, $fold$ is monotone, and a higher condition allows fewer edges. So the greatest fixed point $G$ exists.
2. **Values only go down.** Each visit recomputes a value from inputs that only went down, with more executable edges. So every change at line L13 is a strict step down.
3. **Termination and the bound.** The flat lattice has height 2, so a name changes at most twice and each SSA edge enters SSAWL at most twice. Each CFG edge enters FlowWL at most once.
4. **Nothing above G is lost.** The values stay above $G$ and $Exec$ stays inside $G$'s edges, because each step is one application of a monotone map to a state above $G$.
5. **The end is a fixed point.** Each input change of an instruction leads to a new visit of it: a new reachable block visits all its instructions, a new edge visits the phis, and a changed operand queues the SSA edge. So at the end every value and every edge agrees with $\Phi$. Steps 4 and 5 give the result $= G$.
6. **Soundness.** By induction along a run: the run stays in executable edges, and each value it assigns is described by the value of its name.
7. **At least as strong as CP and DBE in any order.** Every program that a sequence of these passes produces describes a state $S$ with $S \sqsubseteq \Phi(S)$, and $G$ is the join of all such states.

## Complexity

- **Worklist items.** At most $m + 1$ flow items and $2s$ SSA items.
- **Visits.** Each instruction is visited once when its block first becomes reachable. A phi is visited again for each new executable edge into its block and for each SSA item that reaches it. A visit of an ordinary instruction costs $O(1)$; a visit of a phi costs $O(d)$, because it meets its operands again. So all visits cost $O(n + m + s d)$. Wegman and Zadeck (Section 5.4) show how to do all the recomputations of one expression in time proportional to its size, which gives $O(n + m + s)$.
- **Space.** The values, the use lists, the edge flags and the two lists: $\Theta(n + m + s)$.
- **Best case.** Building the use lists reads the whole program, $\Theta(n + s)$, even when a constant branch at the entry makes most of the program unreachable.
- **SSA form.** The SSA form can be larger than the program. The number of phi-functions can grow quadratically in the worst case, so $n$ and $s$ are sizes of the SSA form, not of the source program.

The table below is *measured*, not proved. For each number of blocks $B$, it averages 50 random looping programs of the toy IR with 6 variables, made with the seed $B$ and put in pruned SSA form.

| blocks | SSA instructions | SSA edges $s$ | CFG edges $m$ | SSA items taken | flow items taken | visits | most pushes of one SSA edge |
|---|---|---|---|---|---|---|---|
| 8 | 34.6 | 46.1 | 10.2 | 50.4 | 9.3 | 93.0 | 2 |
| 16 | 74.0 | 111.4 | 22.2 | 113.9 | 16.2 | 192.8 | 2 |
| 32 | 153.1 | 253.0 | 46.0 | 268.9 | 29.5 | 429.4 | 2 |
| 64 | 376.9 | 694.5 | 96.1 | 775.1 | 57.3 | 1197.4 | 2 |

The SSA items stay close to $s$, well below the bound $2s$, and the flow items stay below $m + 1$ because some edges never become executable.

## Properties

- **Optimistic.** It starts from $\top$ and assumes the best until the program proves otherwise. This is why it can find constants that flow around a loop. A pessimistic method starts from $\bot$ and must stop at a lower fixed point.
- **Order-free result.** The result is the greatest fixed point of $\Phi$, so any order of the two lists gives the same values and edges. Only the amount of work changes.
- **Sparse.** Values travel along SSA edges, from definition to use, and not through every block in between. The dense versions keep one value per variable per block, which costs a factor of the number of variables more.
- **Deterministic and iterative.** For a fixed input and fixed queues the run is fixed. It uses no recursion.
- **Strictly stronger than the parts.** On the example, no sequence of constant propagation and dead branch elimination finds `i = 1`, but SCCP does.

## Variants and improvements

- **Sparse simple constant propagation.** Treat every edge as executable. This finds the same constants as Kildall's dense method, faster. Wegman and Zadeck call it SSC and credit it to Reif and Lewis.
- **Dense conditional constant propagation.** Keep the executable flags but run on the CFG with one value per variable per block. Wegman and Zadeck call it CC, a variant of an algorithm of Wegbreit. It finds the same constants as SCCP, more slowly.
- **Combined analyses.** Click and Cooper studied this pattern in general: two optimistic analyses solved as one system can beat any sequence of the two separate passes. SCCP is the classic case. The same idea combines constant propagation with [global value numbering](/global-value-numbering/).
- **Richer lattices.** The flat lattice can be replaced by any lattice of finite height, such as known bits or small sets of values. A lattice of infinite height, such as ranges, needs a way to force the values down fast enough.
- **Branch facts.** On the edge where `x == 5` is true, `x` is 5. Wegman and Zadeck describe inserting assignments on such edges so that the analysis can use the fact.
- **Across procedures.** Wegman and Zadeck also give an interprocedural version. See [interprocedural constant propagation](/interprocedural-constant-propagation/), and the [IDE framework](/ide-framework/) for a version that summarizes procedures.

## When to use it

Use SCCP in a compiler that already has SSA form. It is cheap, it folds constants and removes dead branches in one pass, and its result then feeds [dead code elimination](/dead-code-elimination/), because the definitions it turns into constants often have no uses left. Production compilers built on SSA form, such as LLVM and GCC, include a pass of this kind. If the program is not in SSA form and you need only a quick result, [constant folding](/constant-folding/) inside each block, or the dense [worklist algorithm](/worklist-dataflow-algorithm/), may be enough.

## Pitfalls

- **Visiting unreachable code.** Line L10 must skip a use whose block is not in $Visited$. If it does not, the values from dead code spoil the phis, and the algorithm is no stronger than simple constant propagation.
- **Phis must ignore dead edges.** Line L11 meets only the operands of executable edges. Meeting all operands loses the whole benefit.
- **Starting pessimistic.** If every name starts at $\bot$, or if a phi waits until all its operands are known, constants that flow around a loop are lost. Wegman and Zadeck point out that many older sparse methods worked this way.
- **Names read before they are defined.** If a reachable instruction reads a name that has no definition on some path, its value can stay $\top$, and a branch on it then makes no edge executable. Code that does run would then be marked dead. Give such names an explicit definition first; the implementation here adds `v.0 = 0` at the entry.
- **Folding a trap.** `x = 7 / 0` must give $\bot$, not a value, and the instruction must stay in the program, because it traps when it runs.
- **One SSA edge per use site.** If `y = x + x` adds two SSA edges for `x`, each change of `x` queues `y` twice, and the bound of two items per SSA edge no longer holds in that form.
- **Def-use chains without SSA.** Running the same sparse method on [def-use chains](/def-use-chains/) of a program that is not in SSA form loses precision, because one use can then see several definitions that SSA would have merged by a phi in the right place.

## Implementations

## History

Kildall (1973) gave an early general iterative method for constant propagation. Wegbreit (1975) gave a dense algorithm that also tracks which branches may run. Reif and Lewis gave a sparse method for simple constants. Wegman and Zadeck (POPL 1985; TOPLAS 1991) put the four methods side by side: simple, sparse simple, conditional, and their new sparse conditional algorithm. They proved that it is conservative and that it finds at least the constants of the dense conditional method, and they noted that each SSA edge is examined at most twice. The SSA form it runs on was made practical by Cytron, Ferrante, Rosen, Wegman and Zadeck (1991). Click and Cooper (1995) studied why combined analyses such as this one can beat their parts.

## References
