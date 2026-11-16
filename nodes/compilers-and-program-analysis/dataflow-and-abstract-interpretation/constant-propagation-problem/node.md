---
tag: CY112C
kind: problem
slug: constant-propagation-problem
name: Constant propagation
aliases:
- constant propagation analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: For each program point, find the variables that hold the same known value on every path, using a flat lattice that is monotone but not distributive.
prereqs: [monotone-dataflow-framework, dataflow-analysis]
see_also: [sparse-conditional-constant-propagation, constant-folding, mop-mfp-coincidence-theorem, distributive-dataflow-framework, interprocedural-constant-propagation, ide-framework, dead-code-elimination, worklist-dataflow-algorithm]
sources:
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (constant propagation as an instance of the lattice framework, solved by the iterative algorithm)
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (constant propagation as a monotone framework that is not distributive, and no algorithm for the meet over all paths in general)
  - paper: doi:10.1145/103135.103136
    title: "Mark N. Wegman and F. Kenneth Zadeck, Constant propagation with conditional branches, ACM Transactions on Programming Languages and Systems 13(2), 1991, 181-210"
    locator: the whole paper (simple, sparse simple, conditional and sparse conditional constant propagation, compared on the same lattice)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.4 (Constant Propagation, the semilattice of values, the transfer functions, 9.4.4 monotonicity and 9.4.5 nondistributivity)
---

Constant propagation asks, for each point of a program, which variables hold one fixed value on every path that reaches the point. A compiler uses the answer to replace reads by constants and to fold the arithmetic that follows, as in [constant folding](/constant-folding/), and to remove branches whose direction is known. It is the standard example of a [monotone dataflow framework](/monotone-dataflow-framework/) that is not distributive. Its iterative solution is safe but can be strictly weaker than the meet over all paths, and that ideal answer cannot be computed at all. The strongest practical method is [sparse conditional constant propagation](/sparse-conditional-constant-propagation/).

## In plain words

Walk through the program and keep a note for each variable: "not seen yet", "always this number", or "could be many things". An assignment of a number sets the note to that number. An addition of two known numbers gives a known number. Anything read from outside, such as a parameter, is "many things".

Where two paths meet, compare the notes. If both say the same number, keep it. If they differ, the variable is "many things". A loop sends notes back to its top, so you repeat the walk until no note changes.

The notes only move from "not seen yet" to a number and then to "many things", so the walk ends soon. The answer is never wrong, but it can miss a constant when the paths agree on a result while they disagree on the inputs.

## Definition

**Input.** A [control flow graph](/control-flow-graph/) of [three-address code](/three-address-code/) with $n$ blocks, $m$ edges, $s$ instructions and $v$ variables, and one entry block. The parameters come from outside.

**Output.** For every block $B$ and variable $x$, a value $\mathrm{IN}[B](x)$ in the flat lattice below, and the same at the end of the block. A variable is *a constant* at a point if its value there is an integer $c$.

**The value lattice.** For one variable, the flat lattice has $\top$ ("no value yet", or not defined), every integer, and $\bot$ ("not a constant"), with $\top$ above every integer and every integer above $\bot$. The meet is $\top \sqcap a = a$, $c \sqcap c = c$, and $c \sqcap d = \bot$ for $c \ne d$. Two different integers are not comparable.

**The framework.**

| property | value |
|---|---|
| direction | forward |
| may or must | must: a constant must hold the same value on every path |
| domain $L$ | the maps from the $v$ variables to the flat lattice |
| order $\sqsubseteq$ | pointwise; a lower value is a weaker claim |
| meet $\sqcap$ | pointwise meet of the flat lattice |
| $\top$ and $\bot$ | every variable $\top$; every variable $\bot$ |
| boundary value $\iota$ | at the start of the entry, the parameters are $\bot$ and the other variables are $\top$ (not yet defined) |
| start value elsewhere | $\top$ |
| transfer functions | the rules below, monotone and not distributive |
| height $h$ | $2v$ per point, since each variable can fall at most twice |

The page uses the meet convention of Kildall. Turning the order upside down gives the join convention of [abstract interpretation](/abstract-interpretation/), where $\bot$ is "no value yet".

**Transfer functions.** Let $\sigma$ be the map before an instruction.

- `x = k` sets $x$ to $k$.
- `x = y` sets $x$ to $\sigma(y)$.
- `x = a op b` sets $x$ to the value of the operation on $\sigma(a)$ and $\sigma(b)$, where an integer operand stands for itself. If either operand is $\top$, the result is $\top$. Otherwise, if either operand is $\bot$, the result is $\bot$. Otherwise both are integers, and the result is the folded value, except that an operation that would trap, a division or remainder by 0 or a shift by a count outside 0 to 63, gives $\bot$. A trapping operation is never folded.

A block applies its instructions in order. Each rule is monotone: if the operands go down, the result goes down. A $\top$ operand gives $\top$, which is above everything; an operand that is not $\top$ stays not $\top$ when it goes down, and the result then moves only from the folded value to $\bot$.

**Equations.**

$$\mathrm{IN}[\mathrm{entry}] = \iota \sqcap \bigsqcap_{P \in \mathrm{pred}(\mathrm{entry})} \mathrm{OUT}[P], \qquad \mathrm{IN}[B] = \bigsqcap_{P \in \mathrm{pred}(B)} \mathrm{OUT}[P], \qquad \mathrm{OUT}[B] = f_B(\mathrm{IN}[B]).$$

**Meet over all paths.** For a path $\pi$ from the entry to the start of $B$, $f_\pi(\iota)$ gives each variable the value it has after the instructions along $\pi$, $\bot$ if it depends on a parameter or on a trap, and $\top$ if $\pi$ does not define it. The [meet-over-all-paths solution](/meet-over-all-paths-solution/) makes $x$ a constant $c$ at $B$ when every path that defines $x$ gives it $c$. This is the ideal answer for the CFG, with every branch taken as possible.

**The fixed point computed.** The [worklist dataflow algorithm](/worklist-dataflow-algorithm/) starts every map at $\top$, puts $\iota$ at the entry, and lowers the maps until the equations hold. The result is the [maximal fixed-point solution](/maximal-fixed-point-solution/).

**Soundness.** Say that a map $\sigma$ *describes* a state of a run if every variable $x$ that the run has defined has $\sigma(x) = \bot$ or $\sigma(x)$ equal to its value, and every variable with $\sigma(x) = \top$ is undefined. The boundary value describes every start state. Each rule keeps the relation: an operand that is $\top$ is undefined, so a run that reads it stops, and otherwise the folded value is the value that the run computes. By induction along the path of a run, $f_\pi(\iota)$ describes the state at the end of $\pi$. The MOP value is below every path value, and the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) gives $\mathrm{MFP} \sqsubseteq \mathrm{MOP}$ for every monotone framework. A map below a map that describes a state also describes it, so MOP and MFP describe every run: if MFP says $x = c$ at a point, every run that reaches the point with $x$ defined has $x = c$ there.

**Constant propagation is not distributive.** *Proposition.* The function of `z = x + y` is not distributive. *Proof.* Let $\sigma$ have $x = 2, y = 3$ and $\tau$ have $x = 3, y = 2$. Then $f(\sigma)$ and $f(\tau)$ both have $z = 5$, so $f(\sigma) \sqcap f(\tau)$ has $z = 5$. But $\sigma \sqcap \tau$ has $x = y = \bot$, so $f(\sigma \sqcap \tau)$ has $z = \bot$. As $\bot \ne 5$, $f(\sigma \sqcap \tau) \ne f(\sigma) \sqcap f(\tau)$. $\square$ The same branches before `z = x + y` make MFP give $z = \bot$ while MOP gives $z = 5$; the [distributive dataflow framework](/distributive-dataflow-framework/) page shows this case in a table. The gap is not only for two variable operands. For `x = y * 0`, the maps with $y = 2$ and $y = 3$ give $x = 0$ each, but their meet has $y = \bot$, and the rule gives $x = \bot$. On the other hand, the rules for `x = k`, `x = y` and `x = y + k` are distributive, because the map $c \mapsto c + k$ is one to one.

**Cost.** Each map can fall at most $2v$ times, so the worklist algorithm evaluates each block at most $2v + 1$ times. One evaluation of $B$ costs $O(v)$ per predecessor for the meets, plus $O(v)$ to copy the map, plus one step per instruction. The total is $O((n + m) v^2 + s v)$ time and $O(n v)$ space.

## Variants

- **Simple constant propagation.** The problem above, solved by the iterative algorithm of Kildall. Every branch is taken as possible.
- **Conditional constant propagation.** A branch whose condition is a known constant takes only one edge, and the blocks that no executable edge reaches are skipped. This finds more constants, because values from dead code no longer reach the meets. [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/) is the standard algorithm.
- **Sparse constant propagation.** On [SSA form](/static-single-assignment-form/), each name has one definition, so one value per name is enough. Values flow along the def-use edges of the SSA graph instead of through every block.
- **Copy-constant propagation.** Only `x = k` and `x = y` are evaluated, and every other assignment gives $\bot$. This framework is distributive, so its MFP equals its MOP.
- **Linear constant propagation.** Assignments of the form `x = a * y + b` with constants $a$ and $b$ are also tracked. It is distributive in the form of the [IDE framework](/ide-framework/), which solves it across procedures with summaries.
- **Interprocedural constant propagation.** Constants are passed into calls and back. See [interprocedural constant propagation](/interprocedural-constant-propagation/) and the [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/) page.
- **Richer domains.** Ranges of values, as in the [interval domain](/interval-domain/), or relations between variables, carry more than one value per variable. They need a [widening operator](/widening-operator/), since their lattices have infinite height.

## Examples

**A loop.** `n` is a parameter.

```
entry:
  k = 5
  i = 0
  jump head
head:
  t = i < n
  br t body exit
body:
  j = k * 2
  i = i + 1
  jump head
exit:
  r = k + i
  ret r
```

Round robin in the order entry, head, body, exit gives, at the start of `head`:

| pass | k | i | j | n |
|---|---|---|---|---|
| 1 | 5 | 0 | $\top$ | $\bot$ |
| 2 | 5 | $\bot$ | 10 | $\bot$ |
| 3 | 5 | $\bot$ | 10 | $\bot$ |

In pass 2 the back edge brings $i = 1$, and $0 \sqcap 1 = \bot$. So `k` is the constant 5 everywhere, `j` is 10, and `r = k + i` is not a constant. The value $j = 10$ at `head` and at `exit` uses $\top \sqcap 10 = 10$: on the path that skips the loop, `j` is never defined, so no run reads another value of it there.

**A known branch.** No parameters.

```
entry:
  x = 1
  c = x == 1
  br c then else
then:
  y = 2
  jump join
else:
  y = 3
  jump join
join:
  z = y + 1
  ret z
```

Simple constant propagation finds $c = 1$ but takes both edges, so $y = 2 \sqcap 3 = \bot$ and $z = \bot$ at `join`. Conditional constant propagation sees that `c` is 1, marks only the edge to `then` as executable, and finds $y = 2$ and $z = 3$.

**Opposite branches.** Branches that set $(x, y)$ to $(2, 3)$ and to $(3, 2)$ before `z = x + y` give $z = \bot$ in MFP, while every path gives $z = 5$. Neither simple nor conditional constant propagation finds this constant, since both meet the values of `x` and `y` before the addition.

## Known algorithms

| algorithm | time | result |
|---|---|---|
| [Worklist dataflow algorithm](/worklist-dataflow-algorithm/) on the CFG | $O((n + m) v^2 + s v)$ | MFP of simple constant propagation; Kildall 1973 |
| Sparse propagation on [SSA form](/static-single-assignment-form/) | linear in the size of the SSA graph | one value per SSA name; each value falls at most twice |
| [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/) | linear in the size of the SSA graph | also tracks executable edges; at least as strong as any order of simple propagation and branch removal |
| Path enumeration on an acyclic CFG | exponential in $n$ | MOP; only for small acyclic graphs |

[Elimination dataflow methods](/elimination-dataflow-methods/) do not apply in their usual form, because they need distributive functions with small representations.

## Bounds

**MOP cannot be computed.** *Proposition.* No algorithm decides, for every program, whether a variable is the constant 0 at a point in the meet-over-all-paths solution. *Proof.* Reduce from [Hilbert's tenth problem](/hilberts-tenth-problem/): no algorithm decides whether a polynomial $p(x_1, \ldots, x_k)$ with integer coefficients has a root in the natural numbers. Build a program that sets each $x_i$ to 0, then runs one loop per variable whose body is `xi = xi + 1` and whose test is a parameter. After the loops it computes $q = p(x_1, \ldots, x_k)$ with `+`, `-` and `*`, then `z = q == 0`. The CFG paths through the loops realize every tuple of natural numbers, and on the path for $(a_1, \ldots, a_k)$ the value of `z` is 1 if $p(a_1, \ldots, a_k) = 0$ and 0 otherwise. So the MOP value of `z` at the end is the constant 0 exactly when $p$ has no root in the natural numbers. $\square$ This agrees with the general result of Kam and Ullman that no algorithm computes the MOP solution of every monotone framework. If branch conditions are taken into account, deciding whether a variable is constant on all real runs is undecidable for an even simpler reason, by [Rice's theorem](/rice-theorem/).

**MFP is cheap.** The bound $O((n + m) v^2 + s v)$ above is polynomial, and the sparse algorithms are linear in the size of the SSA form.

**MFP can be strictly weaker than MOP.** The opposite branches example has $\mathrm{MFP}(z) = \bot$ and $\mathrm{MOP}(z) = 5$. The tightness part of the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) builds such an instance from any failure of distributivity whose two arguments the transfer functions can produce from one boundary value.

**Iteration speed.** Constant propagation is not rapid. Round robin can need more passes than the $d + 2$ of the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/), which gives a loop with $d = 1$ that needs 6 passes. The worklist bound $2v + 1$ evaluations per block always holds.

## Reductions

- **To a monotone framework.** Constant propagation is an instance of a [monotone dataflow framework](/monotone-dataflow-framework/) of height $2v$ per point, so every general solver applies.
- **To sparse propagation on SSA.** After [SSA construction](/ssa-construction-problem/), the map at each point is replaced by one value per SSA name. A phi-function takes the meet of its operands. The values flow along [def-use chains](/def-use-chains/), so a change is sent only to the instructions that read the changed name.
- **Linear constants to IDE.** Linear constant propagation is an instance of the [IDE framework](/ide-framework/), where the values are environments and the transfer functions are compositions of $\lambda l.\, a l + b$.
- **From Hilbert's tenth problem.** The reduction in Bounds shows that the MOP version is undecidable.

## Applications

- **Folding and simplification.** Replace each read of a constant by its value and fold the instruction, as in [constant folding](/constant-folding/). This often makes [copy propagation](/copy-propagation/) and [strength reduction](/strength-reduction/) possible.
- **Branch folding and dead code.** A branch on a known condition becomes a jump, and the blocks that are no longer reachable are removed by [dead code elimination](/dead-code-elimination/).
- **Specialization.** [Interprocedural constant propagation](/interprocedural-constant-propagation/) finds parameters that are constant at every call, which [function inlining](/function-inlining/) and [partial evaluation](/partial-evaluation/) exploit.
- **Value numbering.** [Global value numbering](/global-value-numbering/) finds expressions with equal values, and it gains from the constants found first.

## References
