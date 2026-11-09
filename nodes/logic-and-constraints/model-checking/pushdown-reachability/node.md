---
tag: DW4ZV8
kind: problem
slug: pushdown-reachability
name: Pushdown reachability
aliases:
- Reachability in pushdown systems
- Interprocedural reachability
area: logic-and-constraints/model-checking
level: research
summary: Decide whether a pushdown system can go from one configuration, or regular set of configurations, to another. Solvable in cubic time by saturation; P-complete.
prereqs: [pushdown-system]
see_also: [pushdown-saturation, cfl-reachability, reachability-problem, context-free-grammar, dyck-language, ltl-model-checking, safety-property]
sources:
  - paper: "J. Richard Büchi, Regular canonical systems, Archiv für mathematische Logik und Grundlagenforschung 6, 1964, pages 91 to 111"
    title: Regular canonical systems
    locator: the regularity of the sets of words reachable in prefix rewriting systems
  - paper: "Ahmed Bouajjani, Javier Esparza and Oded Maler, Reachability analysis of pushdown automata: application to model-checking, CONCUR 1997, Lecture Notes in Computer Science 1243, Springer, pages 135 to 150"
    title: "Reachability analysis of pushdown automata: application to model-checking"
    locator: the computation of pre* and post* of regular sets by saturation
  - paper: "Javier Esparza, David Hansel, Peter Rossmanith and Stefan Schwoon, Efficient algorithms for model checking pushdown systems, CAV 2000, Lecture Notes in Computer Science 1855, Springer, pages 232 to 247"
    title: Efficient algorithms for model checking pushdown systems
    locator: the cubic algorithms for pre* and post* and their bounds
  - paper: "Thomas Reps, Susan Horwitz and Mooly Sagiv, Precise interprocedural dataflow analysis via graph reachability, 22nd ACM Symposium on Principles of Programming Languages (POPL 1995), pages 49 to 61"
    title: Precise interprocedural dataflow analysis via graph reachability
    locator: the reduction of interprocedural dataflow problems to realizable-path reachability and the summary-edge algorithm
  - paper: "Micha Sharir and Amir Pnueli, Two approaches to interprocedural data flow analysis, in Program Flow Analysis: Theory and Applications, Prentice-Hall, 1981, pages 189 to 233"
    title: Two approaches to interprocedural data flow analysis
    locator: the functional approach, which computes procedure summaries
  - paper: "Swarat Chaudhuri, Subcubic algorithms for recursive state machines, 35th ACM Symposium on Principles of Programming Languages (POPL 2008)"
    title: Subcubic algorithms for recursive state machines
    locator: the reachability algorithm in time O(n^3 / log n)
  - paper: "Thomas Ball and Sriram K. Rajamani, Bebop: a symbolic model checker for Boolean programs, SPIN 2000, Lecture Notes in Computer Science 1885, Springer"
    title: "Bebop: a symbolic model checker for Boolean programs"
    locator: reachability for Boolean programs with procedures, as used in the SLAM project
  - paper: "G. Ramalingam, Context-sensitive synchronization-sensitive analysis is undecidable, ACM Transactions on Programming Languages and Systems 22(2), 2000, pages 416 to 430"
    title: Context-sensitive synchronization-sensitive analysis is undecidable
    locator: the undecidability of reachability for two pushdown systems that synchronize
---

*Pushdown reachability* asks whether a [pushdown system](/pushdown-system/) can move from a given configuration, or from any configuration in a regular set, to a given configuration or into a regular set. It is the basic verification question for sequential programs with recursion: can the program reach this statement, with this call stack, from its start? The configuration graph is infinite, so graph search does not apply directly. But the sets of predecessors and successors of a regular set are regular (Büchi 1964), and [saturation](/pushdown-saturation/) computes them in polynomial time, which solves the problem in time cubic in the size of the input. The problem is P-complete, and it is closely related to [CFL-reachability](/cfl-reachability/) on graphs and to the emptiness problem for context-free grammars.

## In plain words

A program with procedures keeps a call stack. When a procedure calls another, a return address goes on the stack; when it returns, the address comes off. The stack has no fixed size, because procedures can call themselves. The question is whether the program can get from its start to some bad point, and maybe with a certain stack. Trying all runs one by one never ends, since the stack can grow forever. The way out is to work with descriptions of whole sets of stacks, written as small finite automata, and to grow these descriptions until they stop changing. A different way, used in program analysis, computes for each procedure a summary of what it can do from entry to exit, and then reuses that summary at every call.

## Definition

A pushdown system $\mathcal{P} = (P, \Gamma, \Delta)$ has control locations $P$, a stack alphabet $\Gamma$ and rules $\langle p, \gamma \rangle \hookrightarrow \langle p', w \rangle$; it moves by $\langle p, \gamma u \rangle \Rightarrow \langle p', w u \rangle$.

**Configuration reachability.** Input: $\mathcal{P}$ and two configurations $c = \langle p, w \rangle$ and $c' = \langle p', w' \rangle$. Question: does $c \Rightarrow^* c'$?

**Regular reachability.** Input: $\mathcal{P}$ and two $\mathcal{P}$-automata that accept sets of configurations $C$ and $C'$. Question: is there $c \in C$ and $c' \in C'$ with $c \Rightarrow^* c'$? Equivalently, is $\mathrm{post}^*(C) \cap C' \ne \emptyset$, or $C \cap \mathrm{pre}^*(C') \ne \emptyset$?

The size of the input is $|P| + |\Gamma| + |\Delta|$, with each rule counted with the length of its right side, plus the sizes of the configurations or automata.

## Variants

- **Control-state reachability.** Can the system reach control location $p'$ with any stack? Take $C' = \{p'\} \times \Gamma^*$, which an automaton with two states accepts. For programs this asks whether a statement is reachable in any calling context.
- **Head reachability.** Can it reach a configuration with the head $\langle p', \gamma \rangle$, the control location and top letter? This is the form used for program points.
- **Computing the sets.** Output an automaton for $\mathrm{pre}^*(C')$ or $\mathrm{post}^*(C)$, for later use, for example to compute all stacks with which a statement can be reached. This is what [saturation](/pushdown-saturation/) returns.
- **Repeated reachability.** Is there an infinite run that visits a set of heads infinitely often? This is the core of [LTL model checking](/ltl-model-checking/) on pushdown systems, and it reduces to reachability problems.
- **Weighted reachability.** With weights from a semiring on the rules, compute the combined weight of all runs between two sets. This gives interprocedural dataflow analysis.
- **Several stacks.** With two stacks, or two pushdown systems that synchronize, reachability is undecidable (Ramalingam 2000). Bounding the number of context switches gives a decidable version.

## Examples

Take the system of the recursive program on the [pushdown system](/pushdown-system/) page, with one control location $g$ and the rules $\langle g, m_0 \rangle \hookrightarrow \langle g, p_0 m_1 \rangle$, $\langle g, p_0 \rangle \hookrightarrow \langle g, p_1 \rangle$, $\langle g, p_0 \rangle \hookrightarrow \langle g, p_2 \rangle$, $\langle g, p_1 \rangle \hookrightarrow \langle g, p_0 p_2 \rangle$, $\langle g, p_2 \rangle \hookrightarrow \langle g, \varepsilon \rangle$ and $\langle g, m_1 \rangle \hookrightarrow \langle g, m_1 \rangle$.

- **Yes:** $\langle g, m_0 \rangle \Rightarrow^* \langle g, p_2 p_2 p_2 m_1 \rangle$. Call $p$, go to $p_1$ and call $p$ again twice, then go to $p_2$ in the innermost call.
- **No:** $\langle g, m_0 \rangle \not\Rightarrow^* \langle g, p_1 p_1 m_1 \rangle$. Below the top of the stack, only the return point $p_2$ of a recursive call or $m_1$ can occur, because those are the only letters pushed below a new top. The [post* automaton](/pushdown-saturation/) for $\langle g, m_0 \rangle$ accepts $x\, p_2^k\, m_1$ with $x \in \{p_0, p_1, p_2\}$, and $p_1 p_1 m_1$ is not of this form.
- **Pre\*:** the configurations that can reach the return to $\mathit{main}$, $\langle g, m_1 \rangle$, are $\langle g, u\, m \rangle$ with $u \in \{p_0, p_1, p_2\}^*$ and $m \in \{m_0, m_1\}$; the trace is on the [saturation](/pushdown-saturation/) page.

A depth-first search over configurations with a bound on the stack height finds the first answer, but no bound proves the second: the set of reachable configurations is infinite, and only a finite description of it gives a "no".

## Known algorithms

| Method | Idea | Time |
|---|---|---|
| [Pre* saturation](/pushdown-saturation/) (Bouajjani, Esparza and Maler 1997; Esparza et al. 2000) | Add transitions to an automaton for the target set | $O(q^2 r)$ for an automaton with $q$ states and $r$ rules |
| [Post* saturation](/pushdown-saturation/) | The same, forwards from the initial set, with one new state per push target | Polynomial; also cubic |
| Procedure summaries (Sharir and Pnueli 1981; Reps, Horwitz and Sagiv 1995) | Compute entry-to-exit summaries per procedure, then search with summary edges | $O(E D^3)$ for the dataflow version with $E$ edges and $D$ facts |
| CFL-reachability by dynamic programming | Close a graph under the productions of a grammar for matched calls and returns | $O(n^3)$ for $n$ nodes; $O(n^3 / \log n)$ by Chaudhuri (2008) |

For configuration reachability from $c$ to $c' = \langle p', w' \rangle$, build an automaton for $\{c'\}$ with $|P| + |w'|$ states, run pre*, and test whether the result accepts $c$. This takes time $O((|P| + |w'|)^2 |\Delta|)$, plus $O(|w|)$ for the test.

The summary method and saturation compute the same information. In pre*, a transition $p \xrightarrow{\gamma} p'$ between two control locations says exactly that $\langle p, \gamma \rangle \Rightarrow^* \langle p', \varepsilon \rangle$: the head $\langle p, \gamma \rangle$ can pop its letter and end in $p'$. For a program, this is a summary of the procedure whose frame is $\gamma$: entered with globals $p$, it can return with globals $p'$.

## Bounds

- **Upper bound.** Cubic time, by saturation. Truly subcubic algorithms, in time $O(n^{3-\varepsilon})$, are not known; Chaudhuri (2008) saves a logarithmic factor.
- **Lower bound.** The problem is P-complete under logspace reductions: the emptiness problem for context-free grammars, which is P-complete, reduces to it, and it reduces to grammar emptiness by the classical triple construction below.
- **Regularity.** For regular $C$, the sets $\mathrm{pre}^*(C)$ and $\mathrm{post}^*(C)$ are regular (Büchi 1964), with automata of polynomial size. This is what keeps all the variants above decidable.
- **Beyond one stack.** Reachability for two stacks is undecidable, because two stacks simulate the tape of a Turing machine, one stack on each side of the head. So is reachability for two pushdown systems that synchronize on actions, and for a pushdown system with a counter that can be tested for zero.

## Reductions

- **To grammar emptiness.** For each triple $(p, \gamma, p')$ make a nonterminal $[p \gamma p']$, meaning $\langle p, \gamma \rangle \Rightarrow^* \langle p', \varepsilon \rangle$. A pop rule $\langle p, \gamma \rangle \hookrightarrow \langle p', \varepsilon \rangle$ gives $[p \gamma p'] \to \varepsilon$; an internal rule $\langle p, \gamma \rangle \hookrightarrow \langle p_1, \gamma_1 \rangle$ gives $[p \gamma p'] \to [p_1 \gamma_1 p']$; a push rule $\langle p, \gamma \rangle \hookrightarrow \langle p_1, \gamma_1 \gamma_2 \rangle$ gives $[p \gamma p'] \to [p_1 \gamma_1 p''] [p'' \gamma_2 p']$ for each $p''$. The nonterminal $[p \gamma p']$ derives a word if and only if the pop is possible. This is the classical translation of a [pushdown automaton](/pushdown-automaton/) into a [context-free grammar](/context-free-grammar/), and it has $O(|\Delta| |P|^2)$ productions.
- **From CFL-reachability.** Given a graph with edges labelled by open and close brackets, matched-path reachability ([CFL-reachability](/cfl-reachability/) for the [Dyck language](/dyck-language/)) is pushdown reachability for the system whose control locations are the nodes, which pushes on an open bracket and pops the matching letter on a close bracket.
- **From interprocedural dataflow.** Reps, Horwitz and Sagiv reduce interprocedural, finite, distributive subset (IFDS) dataflow problems to realizable-path reachability in an exploded supergraph, which is pushdown reachability with one stack letter per call site.
- **From safety model checking.** Checking a [safety property](/safety-property/) given by a finite automaton on a pushdown system is reachability in the product of the system with the automaton, which is again a pushdown system.

## Applications

- **Software model checking.** Tools for Boolean programs, such as Bebop in the SLAM project (Ball and Rajamani 2000) and Moped (Schwoon), check reachability of error statements in abstractions of C and Java programs, inside a [CEGAR](/cegar/) loop.
- **Interprocedural dataflow analysis.** Constant propagation, taint analysis and other analyses that respect matching calls and returns are reachability or weighted reachability problems.
- **Stack inspection.** Security checks that depend on which methods are on the call stack ask for reachable configurations with a property of the whole stack, which pre* and post* answer exactly.
- **LTL model checking of recursive programs.** Repeated reachability gives [LTL model checking](/ltl-model-checking/) for pushdown systems.

## References

- J. Richard Büchi, Regular canonical systems, Archiv für mathematische Logik und Grundlagenforschung 6, 1964, pages 91 to 111.
- Ahmed Bouajjani, Javier Esparza and Oded Maler, Reachability analysis of pushdown automata: application to model-checking, CONCUR 1997, LNCS 1243, pages 135 to 150.
- Javier Esparza, David Hansel, Peter Rossmanith and Stefan Schwoon, Efficient algorithms for model checking pushdown systems, CAV 2000, LNCS 1855, pages 232 to 247.
- Thomas Reps, Susan Horwitz and Mooly Sagiv, Precise interprocedural dataflow analysis via graph reachability, POPL 1995, pages 49 to 61.
- Micha Sharir and Amir Pnueli, Two approaches to interprocedural data flow analysis, in Program Flow Analysis: Theory and Applications, Prentice-Hall, 1981.
- Swarat Chaudhuri, Subcubic algorithms for recursive state machines, POPL 2008.
- Thomas Ball and Sriram K. Rajamani, Bebop: a symbolic model checker for Boolean programs, SPIN 2000, LNCS 1885.
- G. Ramalingam, Context-sensitive synchronization-sensitive analysis is undecidable, ACM TOPLAS 22(2), 2000, pages 416 to 430.
