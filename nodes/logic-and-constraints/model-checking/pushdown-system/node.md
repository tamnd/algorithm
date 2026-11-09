---
tag: 3A6R2T
kind: model
slug: pushdown-system
name: Pushdown system
aliases:
- Pushdown automaton model of programs
- PDS
area: logic-and-constraints/model-checking
level: research
summary: A finite control with an unbounded stack and no input. It models programs with recursion; its infinite configuration graph still has regular reachability sets.
prereqs: [pushdown-automaton, labelled-transition-system]
see_also: [pushdown-reachability, pushdown-saturation, cfl-reachability, context-free-grammar, regular-language, ltl-model-checking, mu-calculus-model-checking, petri-net]
sources:
  - paper: "J. Richard Büchi, Regular canonical systems, Archiv für mathematische Logik und Grundlagenforschung 6, 1964, pages 91 to 111"
    title: Regular canonical systems
    locator: the theorem that the set of words derivable in a prefix rewriting system from a regular set is regular
  - paper: "Ahmed Bouajjani, Javier Esparza and Oded Maler, Reachability analysis of pushdown automata: application to model-checking, CONCUR 1997, Lecture Notes in Computer Science 1243, Springer, pages 135 to 150"
    title: "Reachability analysis of pushdown automata: application to model-checking"
    locator: P-automata, the saturation procedures for pre* and post*, and LTL and CTL model checking of pushdown systems
  - paper: "Javier Esparza, David Hansel, Peter Rossmanith and Stefan Schwoon, Efficient algorithms for model checking pushdown systems, CAV 2000, Lecture Notes in Computer Science 1855, Springer, pages 232 to 247"
    title: Efficient algorithms for model checking pushdown systems
    locator: the normal form of rules, the efficient pre* and post* algorithms and their bounds, and the model of Boolean programs
  - paper: "Stefan Schwoon, Model-checking pushdown systems, PhD thesis, Technische Universität München, 2002"
    title: Model-checking pushdown systems
    locator: the encoding of programs as pushdown systems, weighted extensions, and the Moped tool
  - paper: "Igor Walukiewicz, Pushdown processes: games and model checking, CAV 1996, Lecture Notes in Computer Science 1102, Springer"
    title: "Pushdown processes: games and model checking"
    locator: the EXPTIME algorithm for parity games on pushdown graphs and for modal mu-calculus model checking
  - paper: "Shaz Qadeer and Jakob Rehof, Context-bounded model checking of concurrent software, TACAS 2005, Lecture Notes in Computer Science 3440, Springer"
    title: Context-bounded model checking of concurrent software
    locator: the decidability of reachability for several stacks when the number of context switches is bounded
  - paper: "Rajeev Alur, Michael Benedikt, Kousha Etessami, Patrice Godefroid, Thomas Reps and Mihalis Yannakakis, Analysis of recursive state machines, ACM Transactions on Programming Languages and Systems 27(4), 2005"
    title: Analysis of recursive state machines
    locator: recursive state machines, their relation to pushdown systems, and cubic reachability
---

A *pushdown system* is a finite control together with an unbounded stack, with rules that look at the control state and the top of the stack and replace the top by a short word. It is a [pushdown automaton](/pushdown-automaton/) with the input removed: what matters is its graph of configurations, not the language it accepts. Pushdown systems are the standard model of sequential programs with recursion: the control holds the values of global variables, and the stack holds the return addresses and the local variables of the active procedure calls. The configuration graph is infinite, but Büchi (1964) proved that the set of configurations reachable from a regular set is regular, and it can be computed in polynomial time by [saturation](/pushdown-saturation/). This makes [pushdown reachability](/pushdown-reachability/) and many model checking problems decidable.

## The machine

**Definition.** A pushdown system is a triple $\mathcal{P} = (P, \Gamma, \Delta)$, where

- $P$ is a finite set of *control locations*;
- $\Gamma$ is a finite *stack alphabet*;
- $\Delta \subseteq (P \times \Gamma) \times (P \times \Gamma^*)$ is a finite set of *rules*. A rule $((p, \gamma), (p', w))$ is written $\langle p, \gamma \rangle \hookrightarrow \langle p', w \rangle$.

A *configuration* is a pair $\langle p, w \rangle \in P \times \Gamma^*$; the first letter of $w$ is the top of the stack. The *step relation* $\Rightarrow$ on configurations is

$$\langle p, \gamma u \rangle \Rightarrow \langle p', w u \rangle \quad \text{for each rule } \langle p, \gamma \rangle \hookrightarrow \langle p', w \rangle \text{ and each } u \in \Gamma^*.$$

So a rule applies to any stack with $\gamma$ on top, and it only touches the top. A configuration with an empty stack has no successor. We write $\Rightarrow^*$ for the reflexive and transitive closure, and for a set $C$ of configurations,

$$\mathrm{post}^*(C) = \{ c' : c \Rightarrow^* c' \text{ for some } c \in C \}, \qquad \mathrm{pre}^*(C) = \{ c : c \Rightarrow^* c' \text{ for some } c' \in C \}.$$

**Normal form.** Every pushdown system can be changed, with a linear increase in size, into one where each rule has $|w| \le 2$, with the same reachability between the original configurations: a rule that pushes a long word is split into a chain of rules through new control locations. Rules with $|w| = 0$ are *pop* rules, with $|w| = 1$ *internal* rules, and with $|w| = 2$ *push* rules.

**Regular sets of configurations.** Infinite sets of configurations are given by finite automata. A *$\mathcal{P}$-automaton* is a nondeterministic finite automaton over $\Gamma$ whose initial states include the control locations $P$. It accepts $\langle p, w \rangle$ when it has a path labelled $w$ from the state $p$ to a final state. A set of configurations is *regular* when some $\mathcal{P}$-automaton accepts exactly it.

**Programs as pushdown systems.** Take a program whose variables have finite types, such as a Boolean program. Let $G$ be the set of valuations of global variables and $L$ the set of pairs of a program point and a valuation of local variables. Use $P = G$ and $\Gamma = L$. Then

- an assignment at point $n$ that leads to $n'$ is an internal rule $\langle g, (n, l) \rangle \hookrightarrow \langle g', (n', l') \rangle$;
- a call at point $n$ to a procedure with entry $e$, returning to $n'$, is a push rule $\langle g, (n, l) \rangle \hookrightarrow \langle g', (e, l_0)\, (n', l) \rangle$, which stores the caller's locals below the callee's frame;
- a return is a pop rule $\langle g, (n, l) \rangle \hookrightarrow \langle g', \varepsilon \rangle$.

The stack of the pushdown system is the call stack of the program.

**Example.** One control location $g$ and the stack alphabet $\{m_0, m_1, p_0, p_1, p_2\}$. The procedure $\mathit{main}$ is at $m_0$ and calls $\mathit{p}$, which returns to $m_1$, where $\mathit{main}$ loops. The procedure $\mathit{p}$ starts at $p_0$ and either goes to $p_1$, where it calls itself and returns to $p_2$, or goes to $p_2$ at once; at $p_2$ it returns. The rules are

$$\langle g, m_0 \rangle \hookrightarrow \langle g, p_0 m_1 \rangle, \quad \langle g, p_0 \rangle \hookrightarrow \langle g, p_1 \rangle, \quad \langle g, p_0 \rangle \hookrightarrow \langle g, p_2 \rangle, \quad \langle g, p_1 \rangle \hookrightarrow \langle g, p_0 p_2 \rangle, \quad \langle g, p_2 \rangle \hookrightarrow \langle g, \varepsilon \rangle, \quad \langle g, m_1 \rangle \hookrightarrow \langle g, m_1 \rangle.$$

From $\langle g, m_0 \rangle$, a run is $\langle g, m_0 \rangle \Rightarrow \langle g, p_0 m_1 \rangle \Rightarrow \langle g, p_1 m_1 \rangle \Rightarrow \langle g, p_0 p_2 m_1 \rangle \Rightarrow \langle g, p_2 p_2 m_1 \rangle \Rightarrow \langle g, p_2 m_1 \rangle \Rightarrow \langle g, m_1 \rangle$. The stack can grow without bound, so infinitely many configurations are reachable, but they form a regular set:

$$\mathrm{post}^*(\{\langle g, m_0 \rangle\}) = \{ \langle g, m_0 \rangle, \langle g, m_1 \rangle \} \cup \{ \langle g, x\, p_2^k\, m_1 \rangle : x \in \{p_0, p_1, p_2\},\ k \ge 0 \}.$$

## What it counts

The cost of an algorithm on a pushdown system is measured in $|P|$, $|\Gamma|$ and $|\Delta|$, and in the number of states and transitions of the $\mathcal{P}$-automata that describe the input sets. The configuration graph is infinite, so algorithms never explore it directly. They work on $\mathcal{P}$-automata, and their running time is polynomial in these sizes: the [saturation algorithms](/pushdown-saturation/) for $\mathrm{pre}^*$ and $\mathrm{post}^*$ run in time cubic in the size of the input.

For programs, the number of control locations is exponential in the number of global Boolean variables, and the stack alphabet is exponential in the number of local Boolean variables of a procedure. This is the [state explosion problem](/state-explosion-problem/) of the finite part, while the unbounded recursion costs nothing extra. Symbolic implementations, such as the Moped tool, store the rules with binary decision diagrams.

## Relation to other models

- **Pushdown automata and context-free languages.** Adding input letters to the rules gives a [pushdown automaton](/pushdown-automaton/). The language view asks which words are read; the system view asks which configurations are reached. The two are linked: the stack contents of the reachable configurations always form a regular language, while the accepted words form a [context-free language](/context-free-language/).
- **Context-free grammars and CFL-reachability.** A pushdown system with one control location is a prefix rewriting system, and its pre* and post* computations are closely related to the closure computations of [context-free grammars](/context-free-grammar/). Interprocedural program analysis by [CFL-reachability](/cfl-reachability/) (Reps, Horwitz and Sagiv 1995) asks for paths whose call and return edges match like brackets, which is reachability in a pushdown system.
- **Recursive state machines.** A recursive state machine is a set of finite-state machines that can call each other (Alur et al. 2005). It is equivalent to a pushdown system, with translations in linear time, and it keeps the structure of procedures visible.
- **Finite-state systems.** A pushdown system whose stack height is bounded is a finite [Kripke structure](/kripke-structure/), and the usual algorithms apply. Unbounded recursion is what makes the model infinite.
- **Two stacks and Petri nets.** Two stacks can simulate a Turing machine tape, so reachability with two stacks is undecidable; this is why concurrent programs with recursion are hard. Bounding the number of context switches between threads makes reachability decidable again (Qadeer and Rehof 2005). A [Petri net](/petri-net/) counts without order, while a stack keeps order but cannot count independent things; neither model simulates the other.

## Known results in the model

| Problem | Result | Source |
|---|---|---|
| Regularity of $\mathrm{post}^*(C)$ and $\mathrm{pre}^*(C)$ for regular $C$ | Always regular | Büchi 1964 |
| Computing $\mathrm{pre}^*$ and $\mathrm{post}^*$ as $\mathcal{P}$-automata | Polynomial time by saturation | Bouajjani, Esparza and Maler 1997; Finkel, Willems and Wolper 1997 |
| [Pushdown reachability](/pushdown-reachability/) of a configuration | Cubic time, P-complete | Esparza et al. 2000 |
| [LTL model checking](/ltl-model-checking/) | Polynomial in the system, exponential in the formula; EXPTIME-complete | Bouajjani, Esparza and Maler 1997 |
| [Modal mu-calculus](/mu-calculus-model-checking/) model checking, parity games on pushdown graphs | EXPTIME-complete | Walukiewicz 1996 |
| CTL model checking | EXPTIME-complete | Walukiewicz; Bouajjani, Esparza and Maler 1997 |
| Reachability with two stacks | Undecidable | simulation of a Turing machine |
| Reachability with several stacks and at most $k$ context switches | Decidable | Qadeer and Rehof 2005 |

The regularity of reachable sets is the central fact of the model: it gives finite representations of infinite sets that are closed under the operations a model checker needs, such as union, intersection and the pre* and post* images.

## References

- J. Richard Büchi, Regular canonical systems, Archiv für mathematische Logik und Grundlagenforschung 6, 1964, pages 91 to 111.
- Ahmed Bouajjani, Javier Esparza and Oded Maler, Reachability analysis of pushdown automata: application to model-checking, CONCUR 1997, LNCS 1243, pages 135 to 150.
- Javier Esparza, David Hansel, Peter Rossmanith and Stefan Schwoon, Efficient algorithms for model checking pushdown systems, CAV 2000, LNCS 1855, pages 232 to 247.
- Stefan Schwoon, Model-checking pushdown systems, PhD thesis, TU München, 2002.
- Igor Walukiewicz, Pushdown processes: games and model checking, CAV 1996, LNCS 1102.
- Shaz Qadeer and Jakob Rehof, Context-bounded model checking of concurrent software, TACAS 2005, LNCS 3440.
- Rajeev Alur et al., Analysis of recursive state machines, ACM TOPLAS 27(4), 2005.
