---
tag: YRWRXC
kind: problem
slug: ltl-model-checking
name: LTL model checking
aliases:
- Linear-time model checking
- LTL verification
area: logic-and-constraints/model-checking
level: core
summary: Decide whether every path of a finite Kripke structure satisfies an LTL formula, and give a lasso-shaped counterexample when one does not. It takes O(|M| 2^O(|φ|)) time and is PSPACE-complete.
prereqs: [linear-temporal-logic, kripke-structure, buchi-automaton]
see_also: [automata-theoretic-approach, ltl-to-buchi-translation, nested-depth-first-search, ltl-model-checking-pspace-completeness, ltl-satisfiability, ctl-model-checking, explicit-state-model-checking, counterexample-generation]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 5, Section 5.2 (automata-based LTL model checking, the product with a Büchi automaton for the negated formula, the complexity analysis and PSPACE-completeness)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 9 (model checking and automata theory) and Chapter 6 (symbolic model checking, including LTL through fair EG on the product with a tableau)
  - paper: doi:10.1145/3828.3837
    title: A. Prasad Sistla and Edmund M. Clarke, The complexity of propositional linear temporal logics, Journal of the ACM 32(3), 1985, pages 733 to 749
    locator: PSPACE-completeness of model checking and satisfiability for LTL, and NP-completeness for the fragment with F only
  - paper: doi:10.1145/318593.318622
    title: Orna Lichtenstein and Amir Pnueli, Checking that finite state concurrent programs satisfy their linear specification, 12th ACM Symposium on Principles of Programming Languages (POPL 1985)
    locator: the tableau algorithm, linear in the size of the program and exponential in the formula
  - paper: "Moshe Y. Vardi and Pierre Wolper, An automata-theoretic approach to automatic program verification, First Symposium on Logic in Computer Science (LICS 1986), IEEE, pages 332 to 344"
    locator: the reduction of LTL model checking to the emptiness of a product with a Büchi automaton
  - paper: doi:10.1006/inco.1994.1092
    title: Moshe Y. Vardi and Pierre Wolper, Reasoning about infinite computations, Information and Computation 115(1), 1994, pages 1 to 37
    locator: the translation of LTL into Büchi automata and its use for satisfiability and model checking
---

LTL model checking asks whether every path of a finite [Kripke structure](/kripke-structure/) $M$ satisfies a [linear temporal logic](/linear-temporal-logic/) formula $\varphi$. The standard algorithm builds a [Büchi automaton](/buchi-automaton/) for $\neg\varphi$, forms its product with $M$, and searches the product for an accepting cycle; it runs in $O(|M| \cdot 2^{O(|\varphi|)})$ time. The problem is [PSPACE](/pspace/)-complete (Sistla and Clarke 1985), but the cost is linear in the size of the system, and the formulas in practice are short. When the answer is no, the algorithm returns a counterexample: a path in the shape of a lasso, a finite stem followed by a cycle that repeats forever.

## In plain words

A system can run in many ways, and each run goes on forever. A property such as "each request is answered later" is a statement about one run. The system is correct when every run has the property.

There are too many runs to test one by one. So the checker turns the question around. It builds a small machine that recognises the bad runs, the runs that break the property. It then runs this machine side by side with the system and looks for a run that both can do. If it finds one, that run is a bug report: a short path to a loop that repeats forever. If there is none, the system is correct.

## Definition

**Input.** A finite Kripke structure $M = (S, I, R, L)$ over a set $AP$ of atomic propositions, with a total transition relation, and an LTL formula $\varphi$ over $AP$. The size is $|M| = |S| + |R|$ and $|\varphi|$ is the number of symbols of $\varphi$.

**Question.** Does $M \models \varphi$ hold, that is, is the trace of every infinite path from an initial state a model of $\varphi$?

**Output of a checker.** "Yes", or "no" with a counterexample. If $M \not\models \varphi$, then some path violates $\varphi$, and then some *lasso* path $u v^\omega$ violates it, where $u$ and $v$ are finite state sequences with $|u| + |v| \le |S| \cdot 2^{O(|\varphi|)}$. A finite lasso is enough because the product of $M$ with a Büchi automaton for $\neg\varphi$ is finite: a non-empty Büchi language contains an ultimately periodic word, and the stem and cycle of a lasso in the product project to a stem and cycle of $M$.

$M \not\models \varphi$ is not the same as $M \models \neg\varphi$; see the example on the [LTL](/linear-temporal-logic/) page. The checker therefore looks for one path that satisfies $\neg\varphi$.

## Variants

- **Existential model checking.** Is there a path from an initial state that satisfies $\varphi$? This is the complement of the universal question for $\neg\varphi$, and has the same complexity.
- **With fairness.** Only fair paths count, for example the paths on which each process that is enabled infinitely often moves infinitely often. Fairness can be written into the formula as $\mathit{fair} \to \varphi$, at a cost in $|\varphi|$, or put into the acceptance condition of the product as a generalized Büchi condition, at a cost linear in the number of fairness sets. See [fairness](/fairness/).
- **Fragments.** For the fragment with only $\mathsf{F}$ and the Boolean connectives, the existential question is NP-complete (Sistla and Clarke 1985). With $\mathsf{U}$, or with $\mathsf{F}$ and $\mathsf{X}$, it is PSPACE-complete again.
- **Fixed formula (program complexity).** For a fixed $\varphi$, the automaton for $\neg\varphi$ is a constant, and the problem is graph reachability of an accepting cycle in the product. It takes linear time and is in NL, since a nondeterministic machine can guess the lasso with a constant number of pointers.
- **Symbolic.** $M$ is given by a Boolean formula over state variables, as for [symbolic model checking](/symbolic-model-checking/). Then $|S|$ can be exponential in the input, and the problem is PSPACE-complete in the size of the circuit too.
- **Bounded.** Is there a counterexample lasso of length at most $k$? This is the question of [bounded model checking](/bounded-model-checking/), solved with SAT.
- **Infinite-state $M$.** For [pushdown systems](/pushdown-system/) the problem stays decidable (EXPTIME-complete); for general programs it is undecidable.

## Examples

**A three-state structure.** Let $S = \{0, 1, 2\}$, $I = \{0\}$, with transitions $0 \to 1$, $1 \to 2$, $2 \to 0$ and $2 \to 2$, and let $p$ hold only in state $1$.

| Formula $\varphi$ | $M \models \varphi$? | Why |
|---|---|---|
| $\mathsf{F}\, p$ | yes | every path starts $0\,1$ |
| $\mathsf{G}\mathsf{F}\, p$ | no | the path $0\,1\,2\,2\,2 \ldots$ loops at 2 forever |
| $\mathsf{G}\mathsf{F}\, \neg p$ | yes | every path leaves 1 at once |
| $\mathsf{G}(p \to \mathsf{X}\, \neg p)$ | yes | the only successor of 1 is 2 |

For $\varphi = \mathsf{G}\mathsf{F}\, p$, the formula $\neg\varphi$ is equivalent to $\mathsf{F}\mathsf{G}\, \neg p$. The tableau construction of the [translation page](/ltl-to-buchi-translation/) gives a generalized Büchi automaton with 5 states and 2 acceptance sets, and a Büchi automaton with 10 states after degeneralization. In the product with $M$, 9 states are reachable from the 2 initial product states, with 12 product transitions, and 3 of the reachable states are accepting. [Nested depth-first search](/nested-depth-first-search/) finds an accepting cycle, and its projection to $M$ is the counterexample $0\,1\,2\,(2)^\omega$. For $\mathsf{G}\mathsf{F}\, \neg p$, the product has 5 reachable states and 7 transitions, and no accepting cycle, so the answer is yes.

**Mutual exclusion.** For two processes that each cycle through the local states non-critical, trying and critical, with a turn variable as in [Peterson's algorithm](/peterson-algorithm/), the typical formulas are $\mathsf{G}\,\neg(c_1 \wedge c_2)$ (safety) and $\mathsf{G}(t_1 \to \mathsf{F}\, c_1)$ (starvation freedom). The second one holds only under a fairness assumption on the scheduler, which is the usual reason to add fairness to the problem.

## Known algorithms

- **The automata-theoretic method** (Vardi and Wolper 1986). Translate $\neg\varphi$ into a Büchi automaton $A_{\neg\varphi}$ with $2^{O(|\varphi|)}$ states ([LTL to Büchi automaton translation](/ltl-to-buchi-translation/)). Build the product $M \otimes A_{\neg\varphi}$, whose states are pairs $(s, q)$ such that the label of $s$ matches $q$. Then $M \models \varphi$ iff the product has no reachable accepting cycle. The emptiness check is [nested depth-first search](/nested-depth-first-search/) or an SCC search such as [Tarjan's algorithm](/tarjan-scc/), both linear in the product. The [automata-theoretic approach](/automata-theoretic-approach/) page treats the method in general.
- **The tableau method** (Lichtenstein and Pnueli 1985). Build the graph of consistent sets of subformulas paired with states, and look for a self-fulfilling strongly connected component: one in which each until formula that must be fulfilled is fulfilled. This is the same product, with the acceptance checked per SCC.
- **On-the-fly search.** The product is built while the emptiness check runs, so a counterexample can be found before the whole state space is built. SPIN works this way; see [on-the-fly model checking](/on-the-fly-model-checking/) and [explicit-state model checking](/explicit-state-model-checking/).
- **Symbolic.** Encode the product with BDDs and compute the fair states with the Emerson-Lei fixed point $\nu Z.\ \bigwedge_i \mathsf{EX}\,\mathsf{E}[Z\ \mathsf{U}\ (Z \wedge F_i)]$; see [symbolic model checking](/symbolic-model-checking/) and the [Emerson-Lei algorithm](/emerson-lei-algorithm/).
- **Bounded and inductive.** [Bounded model checking](/bounded-model-checking/) finds counterexamples up to a length with SAT. The [liveness-to-safety](/liveness-to-safety/) reduction turns the search for an accepting cycle into a reachability question, so that [IC3](/ic3-pdr/) or [k-induction](/k-induction/) can prove the property.

## Bounds

| Bound | Value | Source |
|---|---|---|
| time of the automata-theoretic method | $O(\lvert M\rvert \cdot 2^{O(\lvert\varphi\rvert)})$ | Lichtenstein and Pnueli 1985, Vardi and Wolper 1986 |
| space | polynomial in $\lvert M\rvert + \lvert\varphi\rvert$ | Sistla and Clarke 1985 |
| lower bound | PSPACE-hard, already for a structure of fixed size | Sistla and Clarke 1985 |
| fixed formula | linear time, in NL | from the product construction |
| fragment with F only | coNP-complete (universal), NP-complete (existential) | Sistla and Clarke 1985 |

The exponential factor comes only from the formula. The automaton for $\neg\varphi$ can need $2^{\Omega(|\varphi|)}$ states, as the family of formulas on the [translation](/ltl-to-buchi-translation/) page shows, but the bound counts states of the automaton and not of the product that is reachable. In practice, tools such as SPIN check formulas with a few operators, and the state space of $M$ is the real limit; see [state explosion](/state-explosion-problem/).

## Reductions

- **To emptiness of a Büchi automaton.** $M \models \varphi$ iff $L(A_M) \cap L(A_{\neg\varphi}) = \emptyset$, where $A_M$ accepts the traces of $M$. This is the reduction above, and the special case of [language containment](/language-containment/) $L(A_M) \subseteq L(A_\varphi)$ with a specification given by a formula.
- **From and to satisfiability.** $M \models \varphi$ iff the formula $\psi_M \wedge \neg\varphi$ is unsatisfiable, where $\psi_M$ describes the paths of $M$ with one new proposition per state and has size $O(|M| \cdot |AP|)$. In the other direction, $\varphi$ is satisfiable iff $M_{AP} \not\models \neg\varphi$ for the complete structure $M_{AP}$ on $2^{AP}$ states. Both reductions appear in the proof of [PSPACE-completeness](/ltl-model-checking-pspace-completeness/); the hardness proof there uses a structure of fixed size instead of $M_{AP}$.
- **From reachability.** The [reachability problem](/reachability-problem/) is the case $\varphi = \mathsf{G}\, \neg \mathit{bad}$.

## Applications

- Protocol and concurrent software verification with SPIN, whose input language Promela takes LTL properties directly.
- Hardware verification with LTL or PSL properties in symbolic and SAT-based tools.
- Planning with temporally extended goals; see [planning as model checking](/planning-as-model-checking/).
- Runtime verification, where a monitor for the safety part of an LTL formula checks a running system.

## References
