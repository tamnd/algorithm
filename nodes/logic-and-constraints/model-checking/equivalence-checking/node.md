---
tag: N16FPV
kind: problem
slug: equivalence-checking
name: Equivalence checking
aliases:
- Behavioural equivalence checking
- Bisimulation checking
- Process equivalence
area: logic-and-constraints/model-checking
level: advanced
summary: Decide whether two states of finite transition systems are equivalent under a chosen behavioural equivalence; bisimilarity takes O(m log n) time, trace equivalence is PSPACE-complete.
prereqs: [labelled-transition-system, bisimulation, trace-equivalence, partition-refinement]
see_also: [bisimulation, simulation-relation, stuttering-equivalence, trace-equivalence, partition-refinement, hopcroft-minimization, nfa-equivalence, compositional-verification]
sources:
  - paper: doi:10.1137/0216062
    title: Robert Paige and Robert E. Tarjan, Three partition refinement algorithms, SIAM Journal on Computing 16(6), 1987
    locator: pages 973 to 989 (the relational coarsest partition problem in O(m log n) time, by splitting with the smaller half)
  - paper: doi:10.1016/0890-5401(90)90025-D
    title: Paris C. Kanellakis and Scott A. Smolka, CCS expressions, finite state processes, and three problems of equivalence, Information and Computation 86(1), 1990
    locator: pages 43 to 68 (the O(mn) algorithm for bisimilarity, and the PSPACE-completeness of trace and failure equivalence)
  - paper: doi:10.1007/BF03180566
    title: José Balcázar, Joaquim Gabarró and Miklós Sántha, Deciding bisimilarity is P-complete, Formal Aspects of Computing 4, 1992
    locator: the P-completeness of bisimilarity of finite labelled transition systems
  - paper: doi:10.1109/SFCS.1995.492576
    title: Monika R. Henzinger, Thomas A. Henzinger and Peter W. Kopke, Computing simulations on finite and infinite graphs, FOCS 1995
    locator: pages 453 to 462 (similarity in O(mn) time)
  - paper: doi:10.1007/BFb0032063
    title: Jan Friso Groote and Frits Vaandrager, An efficient algorithm for branching bisimulation and stuttering equivalence, ICALP 1990, LNCS 443
    locator: pages 626 to 638 (branching bisimulation and stuttering equivalence in O(mn) time)
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 7 (the quotient algorithms for bisimulation, simulation and stutter bisimulation)
---

Equivalence checking asks whether two systems, or two states of one system, behave in the same way under a chosen notion of equivalence. For finite labelled transition systems the usual notions are [bisimilarity](/bisimulation/), [simulation](/simulation-relation/) equivalence or the simulation preorder, [trace equivalence](/trace-equivalence/) or trace inclusion, and the versions that ignore internal or stuttering steps, such as weak, branching and [stuttering](/stuttering-equivalence/) bisimilarity. The answer, and its cost, depend strongly on the notion. Bisimilarity is the greatest fixed point of a local matching condition, and [partition refinement](/partition-refinement/) computes it: Kanellakis and Smolka (1990) in $O(mn)$ time and Paige and Tarjan (1987) in $O(m \log n)$ time, for $n$ states and $m$ transitions. Similarity takes $O(mn)$ time (Henzinger, Henzinger and Kopke, 1995). Trace equivalence is PSPACE-complete (Kanellakis and Smolka, 1990), because it contains the equivalence of nondeterministic automata. Bisimilarity is P-complete (Balcázar, Gabarró and Sántha, 1992). The same algorithms compute the quotient of a system, the smallest equivalent system, which model checkers use as a reduction that preserves a logic.

## In plain words

We have two machines described by their states and steps, for example a specification and an implementation, and we want to know whether an observer can tell them apart. What "tell apart" means is a choice. The observer may only see sequences of actions (trace equivalence), or may also see which choices remain open at each moment (bisimilarity), or may ignore internal steps.

For bisimilarity the check is fast: group the states into classes and split a class whenever its members can reach different classes. For traces it can be very slow in the worst case, because the check must follow sets of states, and there can be exponentially many.

## Definition

**Input.** A finite labelled transition system $(S, \mathit{Act}, \to)$ with $n = |S|$ states and $m = |{\to}|$ transitions, optionally a labelling of states, two states $s, t \in S$, and an equivalence or preorder $\equiv$. Two systems are given as one system, their disjoint union.

**Output.** Whether $s \equiv t$. A useful algorithm also gives evidence: for a negative answer a distinguishing formula of Hennessy-Milner logic, a distinguishing trace, or a counterexample game; for a positive answer the relation or the partition.

**The quotient problem.** Compute the partition of $S$ into classes of $\equiv$, or the relation $\preceq$ for a preorder. For bisimilarity this is the *relational coarsest partition problem*: find the coarsest partition, finer than the initial one, in which for each action $a$ and blocks $B$ and $C$ either every state of $B$ or no state of $B$ has an $a$-successor in $C$.

## Variants

- **Preorder checking.** Decide $s \preceq t$ for simulation or $\mathrm{Tr}(s) \subseteq \mathrm{Tr}(t)$ for traces. Refinement checkers such as FDR for CSP check trace and failures refinement this way.
- **Weak and branching equivalences.** With an internal action $\tau$, weak bisimilarity matches a step by $\tau^* a \tau^*$, and branching bisimilarity also requires the intermediate states to stay related. Stuttering equivalence is the version for Kripke structures.
- **Symbolic equivalence checking.** The system is given by BDDs, and the partition is computed symbolically; this helps when $n$ is too large to list.
- **Infinite-state systems.** For pushdown and process-rewrite systems, some equivalences remain decidable; Jančar (1995) proved bisimilarity undecidable for Petri nets.
- **Circuit equivalence.** In hardware design, equivalence checking usually means checking that two circuits compute the same outputs, combinationally with SAT or BDDs, or sequentially for deterministic machines with the same inputs. For deterministic systems all the equivalences on this page coincide with language equivalence.

## Examples

**The vending machines.** The implementation on this site uses the states 0 to 8 with $0 \xrightarrow{\mathit{coin}} 1$, $1 \xrightarrow{\mathit{tea}} 2$, $1 \xrightarrow{\mathit{coffee}} 3$ for machine $P$, and $4 \xrightarrow{\mathit{coin}} 5 \xrightarrow{\mathit{tea}} 7$, $4 \xrightarrow{\mathit{coin}} 6 \xrightarrow{\mathit{coffee}} 8$ for machine $Q$. The results are:

| notion | $P$ (state 0) versus $Q$ (state 4) |
| --- | --- |
| trace equivalence | equivalent, both have $\{\varepsilon, \mathit{coin}, \mathit{coin}\,\mathit{tea}, \mathit{coin}\,\mathit{coffee}\}$ |
| simulation | $P$ simulates $Q$, $Q$ does not simulate $P$ |
| bisimilarity | not bisimilar; states 0 and 4 end in different blocks |

Partition refinement shows the last line. Initially all states are in one block. The first round separates the states by the actions that they can do: $\{1\}$ (tea and coffee), $\{5\}$ (tea), $\{6\}$ (coffee), $\{0, 4\}$ (coin), and the dead states $\{2, 3, 7, 8\}$. The second round splits $\{0, 4\}$, because state 0 has a coin-successor in $\{1\}$ and state 4 does not. A distinguishing formula is $\langle \mathit{coin} \rangle (\langle \mathit{tea} \rangle \mathit{true} \wedge \langle \mathit{coffee} \rangle \mathit{true})$.

**A distinguishing trace.** For $0 \xrightarrow{a} 1 \xrightarrow{b} 2$ and $3 \xrightarrow{a} 4$, the pair search of the subset construction starts at $(\{0\}, \{3\})$, reaches $(\{1\}, \{4\})$ with $a$, and then $(\{2\}, \emptyset)$ with $b$. So $ab$ is a shortest trace of state 0 that state 3 lacks.

## Known algorithms

| notion | algorithm | time |
| --- | --- | --- |
| bisimilarity | naive fixed point on pairs | polynomial, $O(n^2 m)$ or more |
| bisimilarity | Kanellakis and Smolka (1990), split blocks until stable | $O(mn)$ |
| bisimilarity | Paige and Tarjan (1987), split with the smaller half | $O(m \log n)$ |
| bisimilarity, deterministic | Hopcroft (1971) DFA minimization | $O(n k \log n)$ for $k$ actions |
| similarity | Henzinger, Henzinger and Kopke (1995) | $O(mn)$ |
| branching bisimilarity, stuttering equivalence | Groote and Vaandrager (1990) | $O(mn)$ |
| weak bisimilarity | $\tau$-closure, then strong bisimilarity | dominated by the transitive closure |
| trace equivalence | subset construction on pairs of state sets | $O(2^{2n} \cdot k)$ pairs in the worst case |

**Partition refinement.** All the bisimulation algorithms keep a partition that is coarser than bisimilarity and split a block $B$ when its states disagree on whether they can reach a block $C$ with an action $a$. The partition only gets finer, so there are at most $n - 1$ splits. Kanellakis and Smolka spend $O(m)$ per split. Paige and Tarjan, like [Hopcroft](/hopcroft-minimization/), split with respect to a block and the *smaller* of its two parts, so each state takes part in $O(\log n)$ splits, and they keep counts of transitions into each block so that splitting with the larger part costs no more. See [partition refinement](/partition-refinement/).

**Similarity.** The algorithm of Henzinger, Henzinger and Kopke keeps for each state $v$ the set $\mathit{sim}(v)$ of candidate simulators, and for each action and state a set of states that must be removed. Each pair is removed at most once, and each removal is charged to transitions, which gives $O(mn)$.

**Trace equivalence.** Determinize both sides by the [subset construction](/subset-construction/) on the fly and search the pairs of subsets reached by the same word. A pair with one empty and one nonempty set gives a shortest distinguishing trace. Antichain methods (De Wulf, Doyen, Henzinger and Raskin, 2006) and bisimulation up to congruence (Bonchi and Pous, 2013) prune this search and are often much faster in practice; the worst case stays exponential.

**The implementation.** The Python code on this site has a fast and a naive version of each check, for bisimilarity, similarity, trace equivalence and divergence-blind stuttering equivalence, and its tests compare them on random systems. The bisimulation code refines by signatures, in the style of Kanellakis and Smolka, not with the Paige-Tarjan bookkeeping.

## Bounds

- **Bisimilarity.** $O(m \log n)$ time (Paige and Tarjan). It is P-complete under log-space reductions (Balcázar, Gabarró and Sántha, 1992), so a fast parallel algorithm, in NC, is unlikely.
- **Similarity.** $O(mn)$ time (Henzinger, Henzinger and Kopke).
- **Branching bisimilarity and stuttering equivalence.** $O(mn)$ time (Groote and Vaandrager); later work by Groote, Jansen, Keiren and Wijs (2017) gives $O(m \log n)$.
- **Trace and failures equivalence.** PSPACE-complete for finite systems (Kanellakis and Smolka, 1990). Trace equivalence is in PSPACE by a nondeterministic search over pairs of subsets, and PSPACE-hard by a reduction from NFA equivalence.
- **Infinite-state systems.** Bisimilarity of Petri nets is undecidable (Jančar, 1995).

These are proved worst-case bounds. Statements that one method is faster than another in practice, such as for antichains, are measured results on benchmarks.

## Reductions

- **Trace equivalence and NFA equivalence.** Trace equivalence is [NFA equivalence](/nfa-equivalence/) with every state accepting. Conversely, NFA equivalence reduces to trace equivalence by trimming and adding a fresh action $\mathit{end}$ after accepting states; see [trace equivalence](/trace-equivalence/).
- **Deterministic systems.** For deterministic systems, bisimilarity, similarity in both directions and trace equivalence coincide, and all reduce to DFA equivalence, decidable in near-linear time by Hopcroft and Karp's union-find method.
- **Weak to strong.** Weak bisimilarity of a system is strong bisimilarity of its $\tau$-saturation, where $s \xRightarrow{a} t$ if $s \xrightarrow{\tau^* a \tau^*} t$.
- **Kripke structures and labelled systems.** A Kripke structure becomes a labelled system by putting the label of the source state on each transition, or by an initial partition by labels, which is what the algorithms above use.
- **Logic.** Bisimilarity is equality of Hennessy-Milner formulas for image-finite systems, and of CTL\* formulas for finite Kripke structures; so the quotient can replace the system in [CTL\* model checking](/ctl-star/).

## Applications

- **State space reduction.** Model checkers minimize a system modulo bisimulation or stuttering equivalence before checking CTL\* or CTL\* without next; the quotient is often much smaller.
- **Specification against implementation.** Process algebra toolsets such as CADP and mCRL2 check that an implementation is branching bisimilar or weakly bisimilar to a specification, after hiding internal actions.
- **Compositional minimization.** Minimizing each component modulo a congruence before composing them keeps the product small; see [compositional verification](/compositional-verification/).
- **Refinement checking.** FDR checks CSP refinement in the trace and failures models.
- **Abstraction.** An abstraction that simulates a system preserves universal properties, and checking the simulation validates the abstraction.

## References
