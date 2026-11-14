---
tag: VPGMEM
kind: problem
slug: ssa-construction-problem
name: SSA construction
aliases:
- conversion to SSA form
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Given a program in a non-SSA IR, insert phi-functions and rename variables so that each has one definition and the meaning is kept.
prereqs: [static-single-assignment-form, phi-function, dominance-frontier]
see_also: [cytron-ssa-construction, braun-ssa-construction, pruned-ssa-form, dominance-frontier-computation, out-of-ssa-translation, reaching-definitions, live-variable-analysis, ssa-cps-correspondence]
sources:
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the statement of the problem, minimal SSA form defined by convergent paths, the theorem that the iterated join set equals the iterated dominance frontier, and the construction by placement and renaming
  - paper: doi:10.1145/199448.199464
    title: Vugranam C. Sreedhar and Guang R. Gao, A linear time algorithm for placing phi-nodes, Proceedings of the 22nd ACM Symposium on Principles of Programming Languages (POPL), 1995, pages 62-73
    locator: phi placement in linear time per variable with DJ-graphs
  - paper: doi:10.1007/978-3-642-37051-9_6
    title: Matthias Braun, Sebastian Buchwald, Sebastian Hack, Roland Leißa, Christoph Mallon and Andreas Zwinkau, Simple and efficient construction of static single assignment form, Compiler Construction (CC 2013), LNCS 7791, pages 102-122
    locator: Section 2 (construction directly from the abstract syntax tree, with no dominance information) and Section 4 (pruned and minimal SSA form, and the running time)
  - paper: doi:10.1007/3-540-46423-9_8
    title: John Aycock and R. Nigel Horspool, Simple generation of static single-assignment form, Compiler Construction (CC 2000), LNCS 1781, 2000
    locator: the construction that places phi-functions everywhere and removes the trivial ones, minimal on reducible graphs
  - paper: "Preston Briggs, Keith D. Cooper, Timothy J. Harvey and L. Taylor Simpson, Practical improvements to the construction and destruction of static single assignment form, Software: Practice and Experience 28(8), 1998, pages 859-881"
    locator: semi-pruned SSA form and the cost of minimal, semi-pruned and pruned construction
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 3 (Standard Construction and Destruction Algorithms); Chapter 4 (Advanced Construction Algorithms for SSA); Chapter 5 (SSA Reconstruction)
---

SSA construction is the task of turning a program in an ordinary [intermediate representation](/intermediate-representation/) into [static single assignment form](/static-single-assignment-form/). The compiler must add [phi-functions](/phi-function/) at some join points and give every definition a new name, so that each name has one definition, every use refers to the right definition, and the program still computes the same results. Any set of phi-functions large enough gives a correct program, so the real question is where they are needed. Cytron, Ferrante, Rosen, Wegman and Zadeck (1991) answered it: the blocks where two definitions first meet are the iterated [dominance frontier](/dominance-frontier/) of the blocks that assign the variable. Their algorithm, and newer ones that avoid dominance information, are the standard solutions.

## In plain words

A variable that is assigned in several places has to be split into several names, one per assignment. Each read then has to pick the name of the assignment it sees. Inside a straight run of code that is easy: take the latest one above. Where two branches come back together, the latest assignment depends on which branch ran. So the compiler puts a merge instruction there that chooses by the branch. The problem is to put merges in every place that needs one, and in as few other places as possible, and then to give every read its name. Extra merges cost time and memory in every later pass, so the fewer the better.

## Definition

**Input.** A procedure in three-address code over a [control flow graph](/control-flow-graph/) $G = (N, E, r)$, with variables $V$, no phi-functions, and an entry $r$ with no predecessors. Each instruction may assign one variable and read some others.

**Output.** A procedure over the same graph with:

1. a set of phi-functions at the tops of blocks, each for one variable, with one operand per incoming edge;
2. a new name for each definition, including each phi-function, so that each name has exactly one definition;
3. each use renamed to one of the names of its variable.

**Correctness.** On every input, the new procedure follows the same blocks as the old one, and at each use the new name holds the value the variable holds in the old procedure at that point. So both return the same results. A definition at the entry gives each variable its value on entry: the parameter, or an undefined value for a local variable.

**Quality.** Let $S_v$ be the blocks that assign $v$, plus $r$. Two definitions of $v$ *converge* at $y$ if there are non-empty paths from two different definition blocks to $y$ that share only $y$. A placement $\Phi_v$ is *valid* if every block where two definitions in $S_v \cup \Phi_v$ converge is in $\Phi_v$. Otherwise a use at the top of that block would have two reaching definitions. The output is in:

- **minimal SSA form** if each $\Phi_v$ is the least valid placement, the iterated join set $J^+(S_v)$;
- **[pruned SSA form](/pruned-ssa-form/)** if, in addition, it has no phi-function for $v$ at a block where $v$ is dead on entry;
- **strict SSA form** if every definition dominates all its uses.

The main theorem (Cytron et al., 1991) is

$$J^+(S_v) = DF^+(S_v),$$

so minimal SSA places a phi-function for $v$ at each block of the iterated dominance frontier of $S_v$. The [Cytron SSA construction](/cytron-ssa-construction/) page proves it in full.

## Variants

- **Minimal, semi-pruned and pruned.** These differ only in which phi-functions are dropped. Semi-pruned SSA, from Briggs, Cooper, Harvey and Simpson (1998), skips the variables that are never live across a block boundary. Pruned SSA uses full [liveness](/live-variable-analysis/).
- **Construction from the syntax tree.** The CFG is not built yet. [Braun et al.](/braun-ssa-construction/) build SSA form while they translate the syntax tree, and look up definitions on demand.
- **SSA reconstruction.** The program is already in SSA form, but a transformation such as loop unrolling, jump threading or spilling adds new definitions of an existing value. Only the uses of that value need repair. Chapter 5 of the SSA book covers this case.
- **Irreducible graphs.** Cytron's algorithm works on any CFG. Braun's algorithm gives minimal SSA form directly only on reducible graphs and needs an extra pass otherwise.
- **Memory and arrays.** Memory SSA gives versions to the whole memory, or to groups of memory locations, and places phi-functions for them with the same rules.

## Examples

### A diamond

```
B1: br a B2 B3
B2: x = b + 1; jump B4
B3: x = b * 2; jump B4
B4: y = x + a; ret y
```

$S_x = \{B1, B2, B3\}$, and $DF(B2) = DF(B3) = \{B4\}$. The two definitions converge at B4, so B4 gets `x.3 = phi [B2: x.1, B3: x.2]`, and the use in B4 becomes `x.3`. The variable `y` is assigned only in B4, and $DF(B4) = \emptyset$, so it gets no phi-function.

### Minimal and pruned on one loop

The program from the [control flow graph](/control-flow-graph/) page that adds the odd numbers below $n$ has the frontiers $DF(B2) = DF(B3) = DF(B5) = \{B2\}$ and $DF(B4) = \{B5\}$. With $S$ including the entry B1:

| variable | $S_v$ | $DF^+(S_v)$ | live on entry to those blocks |
|---|---|---|---|
| `i` | B1, B5 | B2 | yes |
| `s` | B1, B4 | B2, B5 | yes at both |
| `t1` | B1, B2 | B2 | no |
| `t2` | B1, B3 | B2 | no |

Minimal SSA form has five phi-functions: `i`, `s`, `t1` and `t2` at B2, and `s` at B5. The Cytron construction gives:

```
# params: n
B1:
  t1.0 = 0
  t2.0 = 0
  i.1 = 0
  s.1 = 0
  jump B2
B2:
  i.2 = phi [B1: i.1, B5: i.3]
  s.2 = phi [B1: s.1, B5: s.4]
  t1.1 = phi [B1: t1.0, B5: t1.2]
  t2.1 = phi [B1: t2.0, B5: t2.2]
  t1.2 = i.2 < n
  br t1.2 B3 B6
B3:
  t2.2 = i.2 % 2
  br t2.2 B4 B5
B4:
  s.3 = s.2 + i.2
  jump B5
B5:
  s.4 = phi [B3: s.2, B4: s.3]
  i.3 = i.2 + 1
  jump B2
B6:
  ret s.2
```

The phi-functions for `t1` and `t2` are dead: `t1.1` and `t2.1` are never used. They also need the entry definitions `t1.0 = 0` and `t2.0 = 0`, because on the first entry to B2 these variables have no value yet. Pruned SSA form drops both phi-functions and both entry definitions, which leaves the three phi-functions shown on the [SSA form](/static-single-assignment-form/) page.

## Known algorithms

| algorithm | idea | time | output |
|---|---|---|---|
| [Cytron et al.](/cytron-ssa-construction/) (1991) | phi-functions on $DF^+$, then renaming over the dominator tree | $O(I + V(m + D))$ after the dominator tree | minimal; pruned with liveness |
| Sreedhar and Gao (1995) | $DF^+$ per variable on the DJ-graph, without the frontiers | $O(n + m)$ per variable for placement | minimal |
| Briggs et al. (1998) | Cytron's method, restricted to non-local names | as Cytron | semi-pruned |
| [Braun et al.](/braun-ssa-construction/) (2013) | look up definitions on demand while building the code, remove trivial phi-functions | $\Theta(P + (B + E) V)$ before the removal of trivial phi-functions | pruned; minimal on reducible graphs |

Here $I$ is the number of instructions, $V$ the number of variables, $n$ and $m$ the numbers of blocks and edges, $D$ the total size of the dominance frontiers, and in Braun's bound $P$, $B$ and $E$ are the numbers of instructions, blocks and edges. Aycock and Horspool (2000) start from a phi-function for every variable in every block and delete the trivial ones until none is left. The method is simple, and its result is minimal on reducible graphs.

## Bounds

- **Output size.** For each variable there is at most one phi-function per block, so the output has $O(I + V n)$ instructions and $O(V m)$ phi operands. Any algorithm needs at least that much time to write it.
- **A quadratic lower bound on the output.** Minimal SSA form can need $\Theta(n^2)$ phi-functions for $\Theta(n)$ variables on a graph with $\Theta(n)$ blocks and edges. Take $k$ nested repeat-until loops, with headers $h_1, \ldots, h_k$ and latches $l_1, \ldots, l_k$, and assign a variable $v_i$ in $l_i$. Then $DF^+(\{r, l_i\}) = \{h_1, \ldots, h_i\}$, and the total is $k(k + 1)/2$ phi-functions. The [dominance frontier](/dominance-frontier/) page computes these sets.
- **The dominance frontiers themselves** can have total size $\Theta(n^2)$ on the same family, which is why Cytron's method is quadratic in the worst case even when few phi-functions are needed. Sreedhar and Gao avoid this and place the phi-functions for one variable in $O(n + m)$ time.
- **Measured size.** Cytron et al. found that on real programs the number of phi-functions grows about linearly with the size of the program.

## Reductions

- **Placement is a closure problem.** For one variable, the minimal placement is the least set $\Phi$ with $J(S \cup \Phi) \subseteq \Phi$. By the main theorem this is the least fixed point of $DF$ above $S$, which a worklist computes.
- **Renaming is reaching definitions.** Once the phi-functions are in place, each use is reached by exactly one definition point, the nearest one that dominates it. So renaming is [reaching definitions](/reaching-definitions/) where the answer is always a single definition, and a walk of the dominator tree finds it with one stack per variable.
- **SSA and CPS.** A program in SSA form is a set of mutually recursive local functions, one per block, with the phi-functions as parameters. So SSA construction is closely tied to conversion to [continuation-passing style](/ssa-cps-correspondence/), and minimal SSA form matches the placement of the fewest parameters.
- **Destruction.** The reverse task, [out-of-SSA translation](/out-of-ssa-translation/), is a separate problem. Its difficulty comes from the optimizations run between the two steps.

## Applications

Every SSA-based optimizer starts here. GCC and LLVM build SSA form early and keep it through most of the pipeline. [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/), [global value numbering](/global-value-numbering/), [aggressive dead code elimination](/aggressive-dead-code-elimination/), [operator strength reduction](/operator-strength-reduction/) and SSA-based [partial redundancy elimination](/ssapre/) all need it. [SSA-based register allocation](/ssa-based-register-allocation/) uses the fact that the interference graph of a strict SSA program is chordal. On-demand methods like Braun's suit compilers that build SSA form directly from a syntax tree or from bytecode, because they need no dominance pass.

## References
