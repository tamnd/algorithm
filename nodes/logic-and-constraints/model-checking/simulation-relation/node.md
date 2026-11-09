---
tag: 76PAMV
kind: definition
slug: simulation-relation
name: Simulation relation
aliases:
- Simulation preorder
- Similarity
- Simulation
area: logic-and-constraints/model-checking
level: advanced
summary: A relation in which the second state can match every step of the first, in one direction only; the simulation preorder preserves universal temporal properties such as ACTL*.
prereqs: [kripke-structure, labelled-transition-system, bisimulation]
see_also: [bisimulation, trace-equivalence, stuttering-equivalence, equivalence-checking, cegar, predicate-abstraction, compositional-verification, language-containment]
sources:
  - paper: doi:10.1145/177492.177725
    title: Orna Grumberg and David E. Long, Model checking and modular verification, ACM TOPLAS 16(3), 1994
    locator: pages 843 to 871 (the simulation preorder on Moore machines, the preservation of ACTL* formulas, and composition)
  - paper: doi:10.1109/SFCS.1995.492576
    title: Monika R. Henzinger, Thomas A. Henzinger and Peter W. Kopke, Computing simulations on finite and infinite graphs, FOCS 1995
    locator: pages 453 to 462 (the computation of the similarity relation of a finite graph in O(mn) time)
  - paper: doi:10.1145/186025.186051
    title: Edmund M. Clarke, Orna Grumberg and David E. Long, Model checking and abstraction, ACM TOPLAS 16(5), 1994
    locator: pages 1512 to 1542 (existential abstraction, which simulates the concrete system, and the preservation of ACTL*)
  - paper: "Robin Milner, An algebraic definition of simulation between programs, Second International Joint Conference on Artificial Intelligence (IJCAI), 1971"
    title: An algebraic definition of simulation between programs
    locator: the first definition of simulation between programs
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Sections 7.4 to 7.6 (the simulation order, simulation equivalence, the universal fragments of CTL* and their characterization, and the algorithms)
---

A simulation is a relation $R$ between states such that, whenever $(s, t) \in R$, the state $t$ has the same labels as $s$ and can match every step of $s$ with a step into a state related to the successor of $s$. Then $t$ *simulates* $s$, written $s \preceq t$: whatever $s$ does, $t$ can also do. Unlike [bisimulation](/bisimulation/), the matching goes in one direction only, so $t$ may have extra behaviour. The largest simulation, *similarity*, is a preorder, and it is the greatest fixed point of the matching condition. Its use in model checking comes from preservation: if $M \preceq M'$, then every formula of ACTL\*, the universal fragment of [CTL\*](/ctl-star/), that holds in $M'$ also holds in $M$ (Grumberg and Long 1994). This is why an over-approximating abstraction, which simulates the concrete system, can prove universal properties, as in [CEGAR](/cegar/) and [predicate abstraction](/predicate-abstraction/), and why a component simulates any composition that contains it. Henzinger, Henzinger and Kopke (1995) compute similarity of a finite system in $O(|R| \cdot |S|)$ time, where $|R|$ is the number of transitions; see [equivalence checking](/equivalence-checking/). Milner defined simulation between programs in 1971.

## Definition

**Kripke structures.** Let $M = (S, I, R_T, L)$ and $M' = (S', I', R'_T, L')$ be [Kripke structures](/kripke-structure/) over the same atomic propositions, with total transition relations. A relation $R \subseteq S \times S'$ is a *simulation* if for every $(s, t) \in R$:

1. $L(s) = L'(t)$, and
2. for every $s'$ with $(s, s') \in R_T$ there is $t'$ with $(t, t') \in R'_T$ and $(s', t') \in R$.

$t$ *simulates* $s$, written $s \preceq t$, if some simulation contains $(s, t)$. $M'$ simulates $M$, written $M \preceq M'$, if every initial state of $M$ is simulated by some initial state of $M'$. When the propositions of $M'$ are a subset of those of $M$, condition 1 compares only those, as is usual for abstractions.

**Labelled transition systems.** For a [labelled transition system](/labelled-transition-system/), drop condition 1 and require in condition 2 that the matching step has the same action: if $s \xrightarrow{a} s'$, then $t \xrightarrow{a} t'$ with $(s', t') \in R$.

**Fixed point.** With $G(R)$ the set of pairs that satisfy conditions 1 and 2 with respect to $R$, the function $G$ is monotone, simulations are the relations with $R \subseteq G(R)$, and similarity is the greatest fixed point $\nu G$, as for bisimulation.

**Basic facts.** The identity is a simulation, and the composition of two simulations is one, so similarity is a preorder. *Simulation equivalence* is $s \preceq t$ and $t \preceq s$. A relation is a bisimulation if and only if it and its inverse are simulations. So bisimilarity implies simulation equivalence, but the converse fails, as the example below shows.

**Preservation theorem (Grumberg and Long, 1994).** ACTL\* is the fragment of CTL\* in negation normal form, where negation is applied only to atomic propositions, and with the path quantifier $\mathbf{A}$ only. If $M \preceq M'$ and $M' \models \varphi$ for an ACTL\* formula $\varphi$, then $M \models \varphi$. *Idea of the proof.* Every path of $M$ from a state $s$ is matched step by step by a path of $M'$ from a state $t$ with $s \preceq t$, and the matched states have the same labels. A universal formula true for all paths of $M'$ from $t$ is therefore true for the matched path, and by induction on the formula for the path of $M$.

For finite structures the preservation is exact: $s \preceq t$ if and only if every ACTL formula true at $t$ is true at $s$; Baier and Katoen prove this characterization, for finite systems without terminal states, in their chapter on equivalences and abstraction. The dual statement holds for states and the existential fragment ECTL\*: if $s \preceq t$ and $s$ satisfies an ECTL\* formula $\varphi$, then $t$ satisfies $\varphi$.

**Computation (Henzinger, Henzinger and Kopke, 1995).** For a finite system with $n$ states and $m$ transitions, the similarity relation can be computed in $O(mn)$ time. The algorithm keeps, for each state $v$, the set $\mathit{sim}(v)$ of candidate simulators and removes $u$ from $\mathit{sim}(v)$ when some successor of $v$ has no simulator among the successors of $u$, with counters that charge each removal to a transition. Later algorithms reduce the space by working with a partition of the states.

## Examples and non-examples

**The vending machines.** Take the labelled systems $p_0 \xrightarrow{a} p_1$, $p_1 \xrightarrow{b} p_2$, $p_1 \xrightarrow{c} p_3$ (choose after paying) and $q_0 \xrightarrow{a} q_1 \xrightarrow{b} q_2$, $q_0 \xrightarrow{a} q_4 \xrightarrow{c} q_5$ (the choice is made when paying). The relation $\{(q_0, p_0), (q_1, p_1), (q_4, p_1), (q_2, p_2), (q_5, p_3)\}$ is a simulation, so $q_0 \preceq p_0$. But $p_0 \not\preceq q_0$: the step $p_0 \xrightarrow{a} p_1$ must go to $q_1$ or $q_4$, and neither can do both $b$ and $c$.

**Simulation equivalent but not bisimilar.** Let $s \xrightarrow{a} s_1 \xrightarrow{b} s_2$ and $s \xrightarrow{a} s_3$ with $s_3$ dead, and $t \xrightarrow{a} t_1 \xrightarrow{b} t_2$. Then $t \preceq s$, by matching with $s_1$. Also $s \preceq t$: both $a$-steps of $s$ are matched by $t \xrightarrow{a} t_1$, which works for $s_3$ because $s_3$ has no steps to match. But $s \not\sim t$, since the pair $(s_3, t_1)$ fails in the other direction. The formula $\langle a \rangle \neg \langle b \rangle \mathit{true}$ ("after $a$, $b$ may be impossible") holds at $s$ and not at $t$; it is not universal.

**Abstraction.** In the existential abstraction of a system by a map $h$ from concrete to abstract states, there is an abstract step $h(x) \to h(y)$ for each concrete step $x \to y$. The relation $\{(x, h(x))\}$ is a simulation, so the abstraction simulates the system, and ACTL\* properties proved for the abstraction hold for the system (Clarke, Grumberg and Long, 1994).

**Not a simulation.** The relation $\{(p_0, q_0), (p_1, q_1)\}$ is not a simulation, because $p_1 \xrightarrow{c} p_3$ has no match from $q_1$.

## Related definitions

- [Bisimulation](/bisimulation/): a simulation whose inverse is also a simulation. It preserves all of CTL\*, while simulation preserves only ACTL\* and ECTL\* in the two directions.
- [Trace equivalence](/trace-equivalence/) and trace inclusion: if $s \preceq t$ then every trace of $s$ is a trace of $t$. The converse fails, for example for $p_0$ and $q_0$ above. Trace inclusion is PSPACE-complete for finite systems, while similarity is computable in polynomial time, so tools use simulation as a cheap sufficient test for [language containment](/language-containment/).
- [Stuttering equivalence](/stuttering-equivalence/): stuttering versions of simulation exist and preserve ACTL\* without the next operator.
- Ready simulation and other notions of the linear time and branching time spectrum of van Glabbeek lie between simulation and bisimulation.
- [Compositional verification](/compositional-verification/): with the synchronous composition of Grumberg and Long, $M_1 \parallel M_2 \preceq M_1$, which lets ACTL\* properties of a component carry over to the system.

## References
