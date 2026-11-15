---
tag: VBG0ZZ
kind: definition
slug: path-condition
name: Path condition
aliases:
- path constraint
area: compilers-and-program-analysis/verification-and-synthesis
level: intro
summary: The conjunction of branch conditions over symbolic inputs that an execution path takes, satisfiable exactly by inputs that follow it.
prereqs: [symbolic-execution, control-flow-graph]
see_also: [symbolic-execution-tree, path-explosion-problem, concolic-testing, generational-search, weakest-precondition, strongest-postcondition, smt-problem, bounded-model-checking]
sources:
  - paper: doi:10.1145/360248.360252
    title: James C. King, Symbolic execution and program testing, Communications of the ACM 19(7), 1976
    locator: pp. 385 to 394, the definition of the path condition pc and the rule for IF statements
  - paper: doi:10.1145/2408776.2408795
    title: Cristian Cadar and Koushik Sen, Symbolic execution for software testing, three decades later, Communications of the ACM 56(2), 2013
    locator: pp. 82 to 90, the section on classical symbolic execution (symbolic state and path constraint)
  - paper: doi:10.1145/3182657
    title: Roberto Baldoni, Emilio Coppa, Daniele Cono D'Elia, Camil Demetrescu and Irene Finocchi, A survey of symbolic execution techniques, ACM Computing Surveys 51(3), 2018
    locator: Article 50, Section 1 (the symbolic state and the path constraint) and the section on constraint solving
  - url: "https://www.usenix.org/legacy/event/osdi08/tech/full_papers/cadar/cadar.pdf"
    title: Cristian Cadar, Daniel Dunbar and Dawson Engler, KLEE, unassisted and automatic generation of high-coverage tests for complex systems programs, Proceedings of OSDI 2008, USENIX
    locator: pp. 209 to 224, the section on the architecture (checks of dangerous operations such as division by zero)
---

A path condition is a formula over the input symbols of a program that holds for exactly the inputs whose run follows a given path of the [control flow graph](/control-flow-graph/). It is the conjunction of the branch conditions along the path, each one written in terms of the inputs, with the sign that the path takes. A path is *feasible* when its path condition is satisfiable. This page gives the exact definition for the toy IR of the compilers pages; the method that builds path conditions and uses them is [symbolic execution](/symbolic-execution/).

## Definition

Take a program $P$ in the [three-address code](/three-address-code/) of the toy IR, with parameters $x_1, \dots, x_k$ over the integers. Give each parameter a fresh *input symbol* $\alpha_1, \dots, \alpha_k$. A *symbolic expression* is a term built from the input symbols and integer constants with the operators of the IR. A *path* $p = (B_0, B_1, \dots, B_m)$ is a sequence of block labels with $B_0$ the entry block and each $B_{i+1}$ a successor of $B_i$.

Walk along $p$ and keep a *symbolic store* $\sigma$ that maps each defined name to a symbolic expression. At the start, $\sigma(x_j) = \alpha_j$. An instruction $x = a \mathbin{op} b$ sets $\sigma(x) = \sigma(a) \mathbin{op} \sigma(b)$, where $\sigma(k) = k$ for a constant $k$. Copies and constants work in the same way. Each step adds conditions to a list:

- At a terminator `br a L1 L2` of block $B_i$, add $\sigma(a) \ne 0$ if $B_{i+1} = L_1$, and add $\sigma(a) = 0$ if $B_{i+1} = L_2$. (If $L_1 = L_2$, add nothing.)
- At an instruction $x = a \mathbin{/} b$ or $x = a \mathbin{\%} b$, add $\sigma(b) \ne 0$. At a shift, add $0 \le \sigma(b) \le 63$. These are the *implicit conditions* of the operations that can trap.

The **path condition** of $p$ is the conjunction of the list:

$$\mathrm{PC}(p) \;=\; c_1 \wedge c_2 \wedge \dots \wedge c_r .$$

A run that traps at an instruction of $B_m$ has the path condition of the prefix up to that instruction, with the implicit condition of that instruction negated. An input $v \in \mathbb{Z}^k$ *follows* $p$ if the run of $P$ on $v$ visits the blocks $B_0, \dots, B_m$ in this order, with no trap before the end of $B_m$.

**Property.** For every path $p$ and every input $v$, the input $v$ follows $p$ if and only if $\mathrm{PC}(p)[\alpha := v]$ is true. The proof is an induction on the length of $p$: the store gives the value of each name as a function of the input, so each recorded condition is true exactly when the run makes the same choice. The page [symbolic execution](/symbolic-execution/) gives this induction. Two consequences follow:

- The path $p$ is **feasible** if and only if $\mathrm{PC}(p)$ is satisfiable. A model of $\mathrm{PC}(p)$ is a test input for $p$.
- Two complete paths that differ at some branch have path conditions that no input satisfies together. On a loop-free program, the path conditions of the complete paths, with the conditions of the trap outcomes, split the input space into disjoint parts.

**Decidability.** Whether a given path is feasible is a satisfiability question in the theory of the operations on the path, so it is as hard as that theory:

- With $+$, $-$, comparisons, multiplication by constants, and $/$ and $\%$ by nonzero constants, over unbounded integers, the path condition is a formula of [Presburger arithmetic](/presburger-arithmetic/), and feasibility is decidable. A conjunction of linear constraints is [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/), which is NP-complete.
- With the product of two input symbols, over unbounded integers, feasibility is undecidable in general, by the negative answer to [Hilbert's tenth problem](/hilberts-tenth-problem/): a single branch on a polynomial equation already asks whether it has an integer root.
- On machine words of a fixed width $w$, every operation is a [bit-vector](/bit-vector-satisfiability/) operation and feasibility is decidable and NP-complete.

The question "does some path reach this block?" over all paths of a program with loops is a different question. For programs over unbounded integers it is undecidable, by a reduction from the [halting problem](/halting-problem/): put the block after the code that may run forever. [Rice's theorem](/rice-theorem/) gives the same answer for every nontrivial property of the input and output behavior. One path condition is a finite formula, and the number of paths is what makes the whole question hard.

## Examples and non-examples

**A small program.** The parameters are $x$ and $y$, with the symbols $\alpha$ and $\beta$.

```
entry:
  d = x - y
  t = d < 0
  br t lt ge
lt:
  u = x == y
  br u dead r1
ge:
  q = 12 / d
  v = q == 3
  br v r2 r3
dead:
  ret 9
r1:
  ret 1
r2:
  ret 2
r3:
  ret 3
```

After `entry`, the store has $\sigma(d) = \alpha - \beta$ and $\sigma(t) = [\alpha - \beta < 0]$. The CFG has four complete paths. With the trap of the division, there are five outcomes.

| path | path condition | simplified | feasible |
|---|---|---|---|
| entry, lt, dead | $\alpha - \beta < 0 \wedge \alpha = \beta$ | false | no |
| entry, lt, r1 | $\alpha - \beta < 0 \wedge \alpha \ne \beta$ | $\alpha < \beta$ | yes |
| entry, ge, trap | $\alpha - \beta \ge 0 \wedge \alpha - \beta = 0$ | $\alpha = \beta$ | yes |
| entry, ge, r2 | $\alpha - \beta \ge 0 \wedge \alpha - \beta \ne 0 \wedge 12 / (\alpha - \beta) = 3$ | $\alpha - \beta = 4$ | yes |
| entry, ge, r3 | $\alpha - \beta \ge 0 \wedge \alpha - \beta \ne 0 \wedge 12 / (\alpha - \beta) \ne 3$ | $\alpha - \beta > 0 \wedge \alpha - \beta \ne 4$ | yes |

The simplification of the fourth row uses integer division: for $d > 0$, $12 / d$ takes the values 12, 6, 4, 3, 2, 2, 1 for $d = 1, \dots, 7$, and 0 or 1 above that, so $12 / d = 3$ holds only for $d = 4$. A model of each feasible row is a test: $(x, y) = (0, 2)$ for r1, $(3, 3)$ for the trap, $(5, 1)$ for r2 and $(7, 1)$ for r3. Over the 289 inputs with $x$ and $y$ in $-8$ to $8$, the five outcomes are taken by 136, 17, 13 and 123 inputs (r1, trap, r2, r3), and by no input for `dead`. The sum is 289, as the partition property says.

The path to `dead` is a syntactic path of the CFG with no input. A test generator that picks CFG paths and never checks the path condition wastes work on such paths, and a coverage report shows `dead` as not covered for a good reason.

**A loop.** For `i = 0; while i < n: i = i + 1` with the symbol $\nu$ for $n$, the path that runs the body exactly $j \ge 1$ times has the path condition $0 < \nu \wedge 1 < \nu \wedge \dots \wedge j - 1 < \nu \wedge \neg(j < \nu)$, which simplifies to $\nu = j$. Each $j$ gives one path, so the program has infinitely many feasible paths. This is the root of the [path explosion problem](/path-explosion-problem/).

**Non-examples.**

- *The branch conditions in terms of program names.* The list $d < 0$, $q = 3$ is not a path condition. The names change along the path, so a condition must be written over the input symbols, after the store is applied. For the r2 path, the condition on $q$ becomes $12 / (\alpha - \beta) = 3$.
- *A condition with the implicit checks left out.* The formula $\alpha - \beta \ge 0 \wedge 12 / (\alpha - \beta) = 3$ does not exclude the inputs with $\alpha = \beta$. The SMT-LIB theories make division total and leave the value of $12 / 0$ open, so a solver may pick $12 / 0 = 3$ and return the model $(3, 3)$. That input traps and never reaches r2. KLEE checks each division against the path condition for this reason.
- *An over-approximation.* An [abstract interpretation](/abstract-interpretation/) of the program may find that $d \ge 0$ holds in block `ge`. That is a fact about all paths into `ge`, a superset of the inputs. A path condition is exact for one path.
- *A concretized condition.* A [concolic](/concolic-testing/) tool may replace a symbolic value by its value in the current run, for example the result of a hash function. The formula it records then implies the true path condition, but it is not equal to it: some inputs follow the path and do not satisfy the formula.

## Related definitions

- **Symbolic execution tree.** The tree of all paths, with one path condition per node. See [symbolic execution tree](/symbolic-execution-tree/).
- **Path explosion.** The number of path conditions is exponential in the number of branches and unbounded with loops. See [path explosion problem](/path-explosion-problem/).
- **Weakest precondition of a path.** Turn the path into straight-line code in which each branch becomes `assume c`. Then $\mathrm{PC}(p)$, written over the initial values, is the [weakest precondition](/weakest-precondition/) of this code for the postcondition true. The [strongest postcondition](/strongest-postcondition/) of the code from the precondition "each $x_j = \alpha_j$" is $\mathrm{PC}(p)$ together with the equations of the final store.
- **Verification condition.** A path condition together with the negation of an assertion at the end of the path is one verification condition of that path. [Bounded model checking](/bounded-model-checking/) puts all paths up to a depth into one formula instead of one formula per path.
- **Path feasibility as a query.** Each path condition is one query to an [SMT](/smt-problem/) solver. [Concolic testing](/concolic-testing/) and [generational search](/generational-search/) build the next query by negating one condition of a path condition.

## References
