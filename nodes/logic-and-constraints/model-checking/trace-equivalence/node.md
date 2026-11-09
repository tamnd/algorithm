---
tag: MG7C8J
kind: definition
slug: trace-equivalence
name: Trace equivalence
aliases:
- Language equivalence of transition systems
- Trace inclusion
- Trace preorder
area: logic-and-constraints/model-checking
level: advanced
summary: Two states are trace equivalent if they can perform the same sequences of actions; it preserves linear-time properties but not branching or deadlock, and is PSPACE-complete to decide.
prereqs: [labelled-transition-system, kripke-structure, nfa-equivalence]
see_also: [bisimulation, simulation-relation, stuttering-equivalence, equivalence-checking, language-containment, nfa-equivalence, subset-construction, linear-temporal-logic]
sources:
  - paper: doi:10.1016/0890-5401(90)90025-D
    title: Paris C. Kanellakis and Scott A. Smolka, CCS expressions, finite state processes, and three problems of equivalence, Information and Computation 86(1), 1990
    locator: pages 43 to 68 (the PSPACE-completeness of trace and failure equivalence of finite state processes, and the polynomial algorithm for bisimilarity)
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, the sections on traces, linear-time properties and trace equivalence (trace inclusion preserves linear-time properties, and finite versus infinite traces)
  - book: isbn:9780131532717
    title: C. A. R. Hoare, Communicating Sequential Processes, Prentice Hall, 1985
    locator: the trace model of CSP, and parallel composition defined on traces
  - paper: "Rob J. van Glabbeek, The linear time - branching time spectrum, CONCUR 1990, LNCS 458"
    title: The linear time - branching time spectrum
    locator: trace equivalence as the coarsest of the classical equivalences, and the examples that separate it from the finer ones
---

Two states of a [labelled transition system](/labelled-transition-system/) are trace equivalent if they can perform exactly the same finite sequences of actions, their *traces*. Trace equivalence is the linear-time view of behaviour: it records what can happen, but not when choices are made. For [Kripke structures](/kripke-structure/), the traces are the label sequences of the paths, and trace inclusion is what a linear-time property needs: if every trace of $M$ is a trace of $M'$, then every [LTL](/linear-temporal-logic/) property of $M'$ holds in $M$. This makes trace inclusion the notion behind [language containment](/language-containment/) checking and the CSP refinement order. Trace equivalence is coarser than [bisimulation](/bisimulation/) and [simulation equivalence](/simulation-relation/); the two vending machines below are trace equivalent but not bisimilar. It is also harder to decide: for finite systems it is PSPACE-complete (Kanellakis and Smolka, 1990), because it is the equivalence of nondeterministic automata in which every state accepts, while bisimilarity is decidable in polynomial time and is P-complete (Balcázar, Gabarró and Sántha, 1992). See [equivalence checking](/equivalence-checking/) for the algorithms.

## Definition

**Labelled transition systems.** Let $(S, \mathit{Act}, \to)$ be a labelled transition system. For a word $w = a_1 \cdots a_k \in \mathit{Act}^*$, write $s \xrightarrow{w} s'$ if there are states $s = s_0 \xrightarrow{a_1} s_1 \cdots \xrightarrow{a_k} s_k = s'$. The set of *traces* of $s$ is
$$\mathrm{Tr}(s) = \{w \in \mathit{Act}^* : s \xrightarrow{w} s' \text{ for some } s'\}.$$
It is nonempty, since it contains the empty word, and prefix closed. The *trace preorder* is $s \sqsubseteq_{\mathrm{tr}} t$ if $\mathrm{Tr}(s) \subseteq \mathrm{Tr}(t)$, and $s$ and $t$ are *trace equivalent*, $s \equiv_{\mathrm{tr}} t$, if $\mathrm{Tr}(s) = \mathrm{Tr}(t)$. Two systems are compared by their initial states, or, with several initial states, by the unions of their trace sets.

**Kripke structures.** For a Kripke structure $(S, I, R_T, L)$ with a total transition relation, the traces are the infinite words $L(s_0) L(s_1) \cdots \in (2^{\mathit{AP}})^\omega$ of the paths from initial states. Trace inclusion and trace equivalence are defined in the same way. For finite structures, inclusion of the infinite traces is the same as inclusion of their finite prefixes, by König's lemma: a finite structure has an infinite path along every infinite word all of whose prefixes it can produce.

**As automata.** Make every state accepting, and $\mathrm{Tr}(s)$ is the language of the nondeterministic automaton with start state $s$. So trace equivalence of finite systems is a case of [NFA equivalence](/nfa-equivalence/), and it can be decided by the [subset construction](/subset-construction/): explore the pairs $(X, Y)$ of state sets reached from $(\{s\}, \{t\})$ by the same word, and look for a pair where one set is empty and the other is not. The word that leads to it is a shortest distinguishing trace.

**Facts.**

- *Coarseness.* If $s \sim t$ (bisimilar) or $s \preceq t$ (simulation), then $\mathrm{Tr}(s) \subseteq \mathrm{Tr}(t)$, by induction on the length of the trace. For deterministic systems, where each state has at most one $a$-successor for each $a$, trace equivalence and bisimilarity coincide.
- *Preservation.* If $M \sqsubseteq_{\mathrm{tr}} M'$ for Kripke structures and $\varphi$ is a linear-time property, a set of infinite words, with $\mathrm{Tr}(M') \subseteq \varphi$, then $\mathrm{Tr}(M) \subseteq \varphi$. So trace equivalent structures satisfy the same LTL formulas. They need not satisfy the same CTL formulas.
- *Compositionality.* In CSP, the traces of a parallel composition with synchronization on shared actions are determined by the traces of the components, so trace equivalence is a congruence for that composition.
- *Complexity (Kanellakis and Smolka, 1990).* For finite labelled transition systems, deciding trace equivalence is PSPACE-complete. Membership in PSPACE follows from the pair search, done in nondeterministic polynomial space and Savitch's theorem. For hardness, one can reduce the equivalence of nondeterministic automata, which is PSPACE-complete by Stockmeyer and Meyer: trim the automata so that every state can reach an accepting state, and add a fresh action $\mathit{end}$ from each accepting state to a dead state. Then the traces are the prefixes of the language together with the words $w\,\mathit{end}$ for $w$ in the language, so the traces are equal if and only if the languages are.

## Examples and non-examples

**The vending machines.** Let $p_0 \xrightarrow{a} p_1$, $p_1 \xrightarrow{b} p_2$, $p_1 \xrightarrow{c} p_3$, and $q_0 \xrightarrow{a} q_1 \xrightarrow{b} q_2$, $q_0 \xrightarrow{a} q_4 \xrightarrow{c} q_5$. Both have the traces $\{\varepsilon, a, ab, ac\}$, so $p_0 \equiv_{\mathrm{tr}} q_0$. They are not bisimilar, since after $a$ the second machine has already chosen the drink. A user who wants $b$ after paying is always served by the first machine, and may be stuck with the second.

**Deadlock is not preserved.** The systems $a.b.\mathbf{0} + a.\mathbf{0}$ and $a.b.\mathbf{0}$ both have the traces $\{\varepsilon, a, ab\}$. The first can stop after $a$, the second cannot. Completed trace equivalence and failures equivalence, which are finer, tell them apart.

**Different traces.** The systems $a.(b.\mathbf{0} + c.\mathbf{0})$ and $a.b.\mathbf{0}$ are not trace equivalent: the trace $ac$ belongs only to the first, and it is a shortest distinguishing trace. The first trace-includes the second.

**A loop and its unfolding.** $s \xrightarrow{a} s$ and $t_0 \xrightarrow{a} t_1 \xrightarrow{a} t_0$ both have the traces $a^*$. They are also bisimilar, which implies trace equivalence.

## Related definitions

- [Bisimulation](/bisimulation/): the finest of the classical equivalences. It implies trace equivalence, and the converse holds for deterministic systems.
- [Simulation relation](/simulation-relation/): similarity implies trace inclusion and can be computed in polynomial time, so it is used as a sufficient test for trace inclusion.
- [Stuttering equivalence](/stuttering-equivalence/): its linear-time counterpart, stutter trace equivalence, compares traces up to repeated labels and preserves LTL without the next operator.
- Completed traces, failures, readiness and the other equivalences of van Glabbeek's linear time and branching time spectrum lie between trace equivalence and bisimilarity.
- [Language containment](/language-containment/): automata-theoretic model checking of linear-time properties is trace inclusion between a system and a property automaton.
- [Equivalence checking](/equivalence-checking/): the decision problem, its algorithms, and its complexity for each notion.

## References
