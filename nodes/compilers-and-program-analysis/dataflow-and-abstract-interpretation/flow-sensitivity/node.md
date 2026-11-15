---
tag: KGCKK9
kind: concept
slug: flow-sensitivity
name: Flow sensitivity
aliases:
- flow-sensitive analysis
- flow-insensitive analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Whether an analysis takes the order of statements into account and computes a fact per program point, or one fact for the whole program.
prereqs: [dataflow-analysis, monotone-dataflow-framework]
see_also: [points-to-analysis, andersen-analysis, steensgaard-analysis, sparse-flow-sensitive-pointer-analysis, context-sensitivity, field-sensitivity, flow-insensitive-alias-np-hardness, sparse-conditional-constant-propagation]
sources:
  - paper: doi:10.1145/379605.379665
    title: "Michael Hind, Pointer analysis: haven't we solved this problem yet?, Proceedings of the ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering (PASTE '01), 54 to 61, 2001"
    locator: flow sensitivity as one of the dimensions of precision of a pointer analysis
  - paper: doi:10.1145/239912.239913
    title: "Susan Horwitz, Precise flow-insensitive may-alias analysis is NP-hard, ACM Transactions on Programming Languages and Systems 19(1), 1 to 6, 1997"
    locator: the definition of the flow-insensitive problem (statements in any order, any number of times) and the hardness result
  - paper: doi:10.1145/158511.158639
    title: "Jong-Deok Choi, Michael Burke and Paul Carini, Efficient flow-sensitive interprocedural computation of pointer-induced aliases and side effects, Proceedings of the 20th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '93), 232 to 245, 1993"
    locator: the flow-sensitive formulation of pointer aliasing at each program point
  - paper: doi:10.1109/cgo.2011.5764696
    title: "Ben Hardekopf and Calvin Lin, Flow-sensitive pointer analysis for millions of lines of code, Proceedings of the 9th Annual IEEE/ACM International Symposium on Code Generation and Optimization (CGO 2011), 289 to 298, 2011"
    locator: the staged analysis, which uses a flow-insensitive pointer analysis to build the def-use graph of a sparse flow-sensitive one
  - paper: doi:10.1145/103135.103136
    title: "Mark N. Wegman and F. Kenneth Zadeck, Constant propagation with conditional branches, ACM Transactions on Programming Languages and Systems 13(2), 1991, 181-210"
    locator: Section 3, the sparse simple constant algorithm over SSA names
---

An analysis is *flow-sensitive* when it respects the order of the statements and computes one fact for each program point. An analysis is *flow-insensitive* when it computes one fact for the whole program, or for a whole procedure, that holds at every point. It treats the program as a set of statements that may run in any order, any number of times. A flow-insensitive analysis is cheaper and less precise, but it is still an analysis of the program: every statement contributes, and the result is sound at every point. Flow sensitivity is one of the main dimensions of precision of an analysis, next to [context sensitivity](/context-sensitivity/) and, for pointers, [field sensitivity](/field-sensitivity/).

## In plain words

Suppose you want to know what a variable can hold. One way is to walk through the program in order and write down what is true after each line. This is precise. You see that a variable was set to one thing and later set to another, so the old value no longer matters. It also costs one note per line. Another way is to read every line once, ignore the order, and write one note that covers the whole program. If a variable gets two different values anywhere, the note says it can hold either. This note is right at every line, but it is vague. It is still useful: if no line ever stores the address of some variable, the note proves that nothing points to it. Single assignment form gives each value its own name, and then the cheap way loses almost nothing.

## The idea

**Setting.** Take a [monotone dataflow framework](/monotone-dataflow-framework/) in the meet convention of Kildall: a lattice $L$ with meet $\sqcap$, top $\top$ as the start value, a boundary value $\iota$ at the entry, and a monotone transfer function $f_s$ for each statement $s$. Lower values are less precise, and the analysis computes the greatest fixed point. Flipping the order gives the join convention of Cousot, where the analysis computes the least fixed point and every statement below holds with the order reversed.

**Flow-sensitive.** The program is a control flow graph whose edges carry statements. The analysis keeps one value $x(n)$ at each point $n$. Its result MFP is the greatest solution of

$$x(\mathit{entry}) \sqsubseteq \iota, \qquad x(n) \sqsubseteq f_s(x(m)) \text{ for each edge } m \xrightarrow{s} n.$$

**Flow-insensitive.** The analysis keeps one value $I$ for the whole program. A value $I$ is a solution when

$$I \sqsubseteq \iota \qquad\text{and}\qquad I \sqsubseteq f_s(I) \text{ for every statement } s.$$

The best one is the greatest solution $I^*$, the greatest fixed point of $g(I) = \iota \sqcap \bigsqcap_s f_s(I)$. It exists by the [Knaster-Tarski theorem](/knaster-tarski-theorem/), and in a lattice of finite height $h$ the [Kleene iteration](/kleene-fixed-point-theorem/) from $\top$ reaches it in at most $h + 1$ rounds over the statements.

| item | flow-sensitive | flow-insensitive |
|---|---|---|
| values kept | one per program point | one for the program or procedure |
| equations | one per edge of the control flow graph | one per statement, edges ignored |
| result | greatest solution MFP | greatest solution $I^*$ |
| kills | a later assignment replaces the old fact (strong update) | no kills: every assignment adds to the old fact (weak update) |
| sound at a point | yes, by the [coincidence theorem](/mop-mfp-coincidence-theorem/): MFP is below MOP | yes, since $I^* \sqsubseteq \mathrm{MFP}$ at every point (Proposition 1) |
| space | (points) times (size of a value) | size of one value |

**Proposition 1 (sound, and coarser).** For every point $n$, $I^* \sqsubseteq \mathrm{MFP}(n)$.

*Proof.* Put $x(n) = I^*$ at every point. Then $x(\mathit{entry}) = I^* \sqsubseteq \iota$, and for each edge $m \xrightarrow{s} n$ we have $x(n) = I^* \sqsubseteq f_s(I^*) = f_s(x(m))$. So the constant map is a solution of the flow-sensitive inequations, and MFP is the greatest solution. $\square$

So a flow-insensitive fact is true wherever the flow-sensitive fact is true. Because MFP is below the [MOP solution](/meet-over-all-paths-solution/), $I^*$ is below the value of every path.

**Proposition 2 (any order, any number of times).** $I^*$ is the MFP solution of a graph with one point and one self loop for each statement. If every $f_s$ is distributive, $I^*$ is the meet of $f_{s_k} \circ \cdots \circ f_{s_1}(\iota)$ over all finite sequences $s_1, \ldots, s_k$ of statements of the program, with repeats allowed.

*Proof.* The inequations of the one-point graph are the flow-insensitive inequations. Its paths are all finite sequences of statements, so the [coincidence theorem](/mop-mfp-coincidence-theorem/) for distributive frameworks gives the second part. $\square$

This is the precise meaning of "the statements may run in any order, any number of times". It also shows what flow insensitivity loses: the facts of sequences that no path of the program follows.

**Gen-kill problems.** For a may problem with $f_s(X) = (X \setminus \mathit{kill}_s) \cup \mathit{gen}_s$, such as [reaching definitions](/reaching-definitions/), write the result in the subset order. The least set $X$ with $\iota \subseteq X$ and $f_s(X) \subseteq X$ for all $s$ is $\iota \cup \bigcup_s \mathit{gen}_s$, since $f_s(X) \subseteq X \cup \mathit{gen}_s$. The kill sets drop out: every fact that any statement generates holds everywhere. For a must problem with an empty boundary, such as [available expressions](/available-expressions/), the greatest $X \subseteq \iota = \emptyset$ is empty. Flow-insensitive analysis suits may facts, which say what can never happen. It does not suit must facts that statements kill.

**Single assignment form.** In [SSA form](/static-single-assignment-form/), each name has one definition, so there is nothing to kill. For problems that keep one value per name, such as [constant propagation](/constant-propagation-problem/), the flow-insensitive analysis over SSA names loses nothing.

**Proposition 3.** Take a program in strict SSA form in which every block is reachable from the entry, and a framework that keeps one value per name, where the statement that defines $v$ sets $v$ from the values of its operands and keeps all other names. A phi takes the meet of its operands, each read at the end of its predecessor block. Then at every point $n$ that the definition of $v$ dominates, $\mathrm{MFP}(n)(v) = I^*(v)$. In strict SSA form, this covers every use of $v$.

*Proof.* Let $d$ be the point just after the definition of $v$, and $R$ the points that $d$ dominates. A path from the entry to a point of $R$ passes $d$, and after its last visit to $d$ it stays in $R$, where no statement writes $v$. So $\mathrm{MFP}(n)(v) \sqsubseteq \mathrm{MFP}(d)(v)$ for $n \in R$. Raising $v$ to $\mathrm{MFP}(d)(v)$ at all points of $R$ gives another solution, since the only predecessors of points in $R$ are $d$ and points of $R$, and all transfer functions are monotone. As MFP is the greatest solution, $\mathrm{MFP}(n)(v) = \mathrm{MFP}(d)(v) =: M(v)$ for all $n \in R$. The definitions of the operands of $v$ dominate the definition of $v$, and the definition of a phi operand dominates the end of its predecessor. So $M(v)$ is the transfer function of $v$ applied to $M$, and $M$ is a fixed point of $g$. Then $M \sqsubseteq I^*$, and Proposition 1 gives $I^* \sqsubseteq M$. $\square$

The global map of [SSA](/static-single-assignment-form/) names to lattice values is the simple constant algorithm of Wegman and Zadeck (1991), and [sparse conditional constant propagation](/sparse-conditional-constant-propagation/) adds reachability of edges to it. The same idea is behind the sparse flow-sensitive pointer analyses: they move facts along def-use chains, so they keep the precision of the flow-sensitive analysis and pay for far fewer points ([sparse flow-sensitive pointer analysis](/sparse-flow-sensitive-pointer-analysis/)).

**Memory is the hard case.** SSA form renames scalar variables, not memory cells. A store `*p = q` may change one of many cells, so even a flow-sensitive analysis can only replace the old fact (a strong update) when $p$ points to exactly one concrete cell. A flow-insensitive analysis never replaces a fact. The [points-to analysis](/points-to-analysis/) page gives both versions of the transfer functions. Precise flow-insensitive may-alias analysis is NP-hard even without dynamic memory ([Horwitz 1997](/flow-insensitive-alias-np-hardness/)), so the usual flow-insensitive pointer analyses, [Andersen's analysis](/andersen-analysis/) and [Steensgaard's analysis](/steensgaard-analysis/), are themselves approximations of the best flow-insensitive answer.

**Cost.** Let $N$ be the number of statements, $E$ the number of edges of the control flow graph, and $V$ the number of variables. For constant propagation, each variable can drop at most twice ($\top$, a constant, $\bot$).

| analysis | values stored | work |
|---|---|---|
| flow-sensitive, dense | a map of $V$ entries at each of $N$ points | $O(E \cdot V)$ edge visits, each on maps of $V$ entries |
| flow-insensitive over variables | one map of $V$ entries | $O(N + U)$ statement evaluations with a worklist over the uses, where $U$ is the number of operands |
| flow-insensitive over SSA names | one map, one entry per name | the same bound, with SSA names in place of variables |

## Examples

**Constant propagation.** Take the straight-line code below with the boundary of the [constant propagation](/constant-propagation-problem/) page, where variables that are not yet defined are $\top$.

```text
x = 1
y = x + 1
x = 2
z = x + 1
```

| name | flow-sensitive, at the end | flow-insensitive over variables | flow-insensitive over SSA names |
|---|---|---|---|
| x | 2 | $\bot$ | x1 = 1, x2 = 2 |
| y | 2 | $\bot$ | y1 = 2 |
| z | 3 | $\bot$ | z1 = 3 |

Over variables, the flow-insensitive solution needs $I(x) \sqsubseteq 1$ and $I(x) \sqsubseteq 2$, so $I(x) = \bot$, and then $y$ and $z$ are $\bot$ too. The two assignments to `x` are in a fixed order, and the analysis forgets it. After renaming to `x1` and `x2`, the conflict is gone, and the flow-insensitive analysis finds every constant, as Proposition 3 says.

**Points-to.** Take the code below.

```text
p = &a
q = p
p = &b
```

| pointer | flow-sensitive, at the end | flow-insensitive (Andersen) |
|---|---|---|
| p | {b} | {a, b} |
| q | {a} | {a, b} |

The flow-sensitive analysis sees that the last line replaces the target of `p` after `q` copied it. The flow-insensitive analysis lets the copy happen after either assignment.

**Flow-insensitive is not "no analysis".** It is a common mistake to treat a flow-insensitive result as if the analysis had given up. In the points-to example, neither `p` nor `q` can point to a variable `c`, whose address the program never takes. A store `*q = 0` cannot change `c`, so `c` can stay in a register across the store. "No analysis" would have to assume that every pointer may point to every variable. In the same way, a variable whose every assignment stores the constant 5 is the constant 5 at each point where it is defined, with no flow information at all. Flow-insensitive answers lose the facts that depend on order, and they keep the facts that hold for every order, which are often the facts that matter.

## Where it is used

- **Pointer analysis of large programs.** [Andersen's analysis](/andersen-analysis/) and [Steensgaard's analysis](/steensgaard-analysis/) are flow-insensitive, which keeps one points-to set per variable and makes whole programs of millions of lines feasible. Hind (2001) lists flow sensitivity as one of the main choices in the design of a pointer analysis.
- **Staged flow-sensitive analysis.** Hardekopf and Lin (2011) first run a flow-insensitive pointer analysis. They use its result to build def-use chains for memory, and then run a sparse flow-sensitive analysis along those chains ([sparse flow-sensitive pointer analysis](/sparse-flow-sensitive-pointer-analysis/)). The cheap result makes the precise one affordable.
- **Optimizers on SSA form.** Constant propagation, [global value numbering](/global-value-numbering/) and many other scalar analyses run over SSA names with one value per name. By Proposition 3 they get the flow-sensitive answer for scalars at the cost of a flow-insensitive one.
- **Classic dataflow inside a procedure.** [Reaching definitions](/reaching-definitions/), [live variables](/live-variable-analysis/) and [available expressions](/available-expressions/) are flow-sensitive by nature, since their kills carry most of the information.
- **Side effects of procedures.** The set of locations that a procedure may modify or read is usually computed flow-insensitively, since the answer is one set for the whole procedure ([mod-ref analysis](/mod-ref-analysis/)).
- **Types.** A type system that gives each variable one type for its whole scope is flow-insensitive. Type narrowing after a test, as in the checkers of many scripting languages, is flow-sensitive.

## References
