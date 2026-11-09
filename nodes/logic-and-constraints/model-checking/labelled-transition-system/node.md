---
tag: XWJ2SN
kind: definition
slug: labelled-transition-system
name: Labelled transition system
aliases:
- LTS
- Labeled transition system
area: logic-and-constraints/model-checking
level: intro
summary: A set of states with transitions labelled by actions, the standard model of process calculi; it puts the information on the edges where a Kripke structure puts it on the states.
prereqs: [directed-graph]
see_also: [kripke-structure, bisimulation, simulation-relation, trace-equivalence, modal-mu-calculus, petri-net, deadlock-freedom-checking, reachability-problem]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 2, Section 2.1 (transition systems with actions and a state labelling) and Section 2.2 (parallel composition with handshaking)
  - book: "Robin Milner, Communication and Concurrency, Prentice Hall, 1989"
    locator: Chapter 2 (labelled transition systems as the semantics of CCS) and Chapter 4 (strong bisimulation)
  - paper: doi:10.1145/360248.360251
    title: Robert M. Keller, Formal verification of parallel programs, Communications of the ACM 19(7), 1976, pages 371 to 384
    locator: the transition system model of parallel programs with named transitions
  - paper: doi:10.1145/2455.2460
    title: Matthew Hennessy and Robin Milner, Algebraic laws for nondeterminism and concurrency, Journal of the ACM 32(1), 1985, pages 137 to 161
    locator: the modal logic of actions (Hennessy-Milner logic) and its characterization of bisimilarity on image-finite systems
---

A labelled transition system (LTS) is a set of states together with transitions $s \xrightarrow{a} t$ that carry an action name $a$. It is the semantic model of process calculi such as CCS and CSP, and the input of [bisimulation](/bisimulation/) checking and of model checkers for action-based logics. It differs from a [Kripke structure](/kripke-structure/) only in where it keeps its information: on the transitions, not on the states.

## Definition

A **labelled transition system** is a tuple $T = (S, \mathit{Act}, \to, s_0)$ where

- $S$ is a set of *states* (finite for model checking, but the definition allows any set),
- $\mathit{Act}$ is a set of *actions*,
- ${\to} \subseteq S \times \mathit{Act} \times S$ is the *transition relation*; we write $s \xrightarrow{a} t$ for $(s, a, t) \in {\to}$,
- $s_0 \in S$ is the *initial state*. Some authors use a set of initial states, and some have none.

The relation need not be total: a state with no outgoing transition is a *terminal* state, which is a [deadlock](/deadlock-freedom-checking/) when it is not meant as successful termination. The LTS is *finitely branching* when each state has finitely many outgoing transitions, and *deterministic* when $s \xrightarrow{a} t$ and $s \xrightarrow{a} t'$ imply $t = t'$.

An **execution** is a finite or infinite alternating sequence $s_0 a_1 s_1 a_2 s_2 \ldots$ with $s_{i-1} \xrightarrow{a_i} s_i$ for each $i$. Its **trace** is the sequence of actions $a_1 a_2 \ldots$. The set of finite traces from $s_0$ is the *trace language* of $T$.

**Size.** For a finite LTS, $|T| = |S| + |{\to}|$, the size of the graph in [adjacency lists](/adjacency-list/), as for a Kripke structure.

**Baier and Katoen's transition systems.** Baier and Katoen use a tuple $(S, \mathit{Act}, \to, I, AP, L)$ with both action labels and a state labelling $L : S \to 2^{AP}$. Dropping $L$ gives an LTS, and dropping $\mathit{Act}$ gives a Kripke structure (without the totality condition).

## Examples and non-examples

**Two vending machines.** Machine $A$ has states $a_0, a_1, a_2, a_3$ and transitions $a_0 \xrightarrow{\mathit{coin}} a_1$, $a_1 \xrightarrow{\mathit{tea}} a_2$, $a_1 \xrightarrow{\mathit{coffee}} a_3$. Machine $B$ has states $b_0, \ldots, b_4$ and transitions $b_0 \xrightarrow{\mathit{coin}} b_1$, $b_0 \xrightarrow{\mathit{coin}} b_2$, $b_1 \xrightarrow{\mathit{tea}} b_3$, $b_2 \xrightarrow{\mathit{coffee}} b_4$. Both have the same four finite traces: the empty trace, $\mathit{coin}$, $\mathit{coin}\,\mathit{tea}$ and $\mathit{coin}\,\mathit{coffee}$. So they are [trace equivalent](/trace-equivalence/). But after a coin, $A$ still offers both drinks, and $B$ has already chosen one. The Hennessy-Milner formula $\langle \mathit{coin} \rangle (\langle \mathit{tea} \rangle \mathit{true} \wedge \langle \mathit{coffee} \rangle \mathit{true})$ holds at $a_0$ and fails at $b_0$, so $a_0$ and $b_0$ are not [bisimilar](/bisimulation/). This is Milner's standard example of why traces are too coarse for systems that interact.

**A Petri net.** The reachability graph of a [Petri net](/petri-net/) is an LTS: the states are markings, and $M \xrightarrow{t} M'$ when firing transition $t$ in $M$ gives $M'$. It is finite exactly when the net is bounded.

**A program with an infinite state space.** A program with an unbounded integer counter has an LTS with infinitely many states. The definition allows it, but the explicit algorithms on this page need a finite $S$; [pushdown systems](/pushdown-system/), Petri nets and [timed automata](/timed-automata/) are infinite-state models with their own decision procedures.

**Non-example: labels on states.** A graph whose states carry sets of propositions and whose edges carry no names is a Kripke structure. A model checker for CTL reads state labels; an LTS gives them only after a conversion.

## Related definitions

- **From an LTS to a Kripke structure.** Make an initial state $(s_0, \bot)$ with the empty label, and a state $(t, a)$ for each transition $s \xrightarrow{a} t$, with the label $\{a\}$. Add $(t, a) \to (u, b)$ when $t \xrightarrow{b} u$. Add a self-loop and the label $\mathit{dead}$ to each state whose first component is terminal, so that the relation becomes total. The result has at most $1 + |{\to}|$ states, and one edge for each pair of consecutive transitions.
- **From a Kripke structure to an LTS.** Label each edge $s \to t$ with the action $L(t)$, so that the trace of a path is its sequence of labels.
- **Equivalences.** [Bisimulation](/bisimulation/), [simulation](/simulation-relation/), [trace equivalence](/trace-equivalence/) and [stuttering equivalence](/stuttering-equivalence/) compare two LTSs. On image-finite systems, two states are bisimilar if and only if they satisfy the same Hennessy-Milner formulas (Hennessy and Milner 1985).
- **Logics.** Hennessy-Milner logic has the modalities $\langle a \rangle \varphi$ (some $a$-step leads to a state where $\varphi$ holds) and $[a]\varphi$ (each $a$-step does). The [modal mu-calculus](/modal-mu-calculus/) adds least and greatest fixed points to them.
- **Questions on an LTS.** [Reachability](/reachability-problem/) of a state or an action, [deadlock detection](/deadlock-freedom-checking/), equivalence checking, and model checking of action-based temporal logics.

## References
