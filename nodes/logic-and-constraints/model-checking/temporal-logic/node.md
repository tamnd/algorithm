---
tag: 80XZRS
kind: concept
slug: temporal-logic
name: Temporal logic
aliases:
- Modal logic of time
- Temporal logics for verification
area: logic-and-constraints/model-checking
level: intro
summary: Logics that express how a system behaves over time, with operators such as always, eventually and until. LTL is linear, CTL is branching, CTL* holds both, and the mu-calculus holds all three.
prereqs: [kripke-structure]
see_also: [linear-temporal-logic, computation-tree-logic, ctl-star, modal-mu-calculus, safety-property, liveness-property, ctl-model-checking, ltl-model-checking]
sources:
  - paper: doi:10.1109/SFCS.1977.32
    title: Amir Pnueli, The temporal logic of programs, 18th Annual Symposium on Foundations of Computer Science (FOCS), 1977, pages 46 to 57
    locator: the proposal to specify concurrent programs in linear temporal logic
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 5 (LTL), Chapter 6 (CTL, Section 6.3 on the expressiveness of CTL versus LTL, and Section 6.8 on CTL*)
  - paper: "E. Allen Emerson, Temporal and modal logic, in Jan van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier and MIT Press, 1990, pages 995 to 1072"
    locator: the survey of linear and branching time logics, their expressiveness, and the complexity of their satisfiability and model checking problems
  - paper: doi:10.1145/3828.3837
    title: A. Prasad Sistla and Edmund M. Clarke, The complexity of propositional linear temporal logics, Journal of the ACM 32(3), 1985, pages 733 to 749
    locator: PSPACE-completeness of satisfiability and model checking for LTL
---

A temporal logic is a logic whose formulas talk about how truth changes over time. Instead of "$x > 0$" it can say "$x > 0$ from now on", "eventually $x > 0$", or "$x > 0$ until $y = 1$". In computer science the time is the sequence of steps of a system, the model is a [Kripke structure](/kripke-structure/), and the formulas are specifications that a model checker verifies. Pnueli proposed temporal logic for programs in 1977, and Clarke, Emerson, Queille and Sifakis turned it into automatic model checking in the early 1980s.

## In plain words

Normal logic describes one moment. A system, though, runs through many moments, and the interesting questions are about all of them: will this ever go wrong, will that always come back, does this wait until that happens?

Temporal logic adds words for time: always, eventually, next, and until. With them you can write "the two processes are never in the critical section together" or "every request is answered sooner or later" as a short formula.

There are two views of time. In the linear view, a run of the system is one line of moments, and a formula speaks about every run. In the branching view, the future is a tree of choices, and a formula can say "some future" or "every future". The two views give different logics, with different strengths and different costs to check.

## The idea

**Models.** A [Kripke structure](/kripke-structure/) $M = (S, I, R, L)$ gives a set of states, a total transition relation, and the atomic propositions that hold in each state. A *path* is an infinite sequence of states that follows $R$.

**Temporal operators.** On a path $\pi = s_0 s_1 \ldots$, with $\pi^i$ the suffix from $s_i$:

- $\mathsf{X}\,\varphi$ (next): $\varphi$ holds on $\pi^1$.
- $\mathsf{F}\,\varphi$ (eventually): $\varphi$ holds on $\pi^i$ for some $i \ge 0$.
- $\mathsf{G}\,\varphi$ (always): $\varphi$ holds on $\pi^i$ for each $i \ge 0$.
- $\varphi\,\mathsf{U}\,\psi$ (until): $\psi$ holds on some $\pi^j$, and $\varphi$ holds on each $\pi^i$ with $i < j$.

$\mathsf{F}\,\varphi = \mathit{true}\,\mathsf{U}\,\varphi$ and $\mathsf{G}\,\varphi = \neg\mathsf{F}\,\neg\varphi$, so $\mathsf{X}$ and $\mathsf{U}$ are enough.

**Linear time.** [Linear temporal logic](/linear-temporal-logic/) (LTL) uses these operators with no path quantifier. A structure satisfies an LTL formula if every path from an initial state does. So LTL describes sets of infinite words, and it splits naturally into [safety](/safety-property/) and [liveness](/liveness-property/) properties. By Kamp's theorem (1968), LTL has the same power as first-order logic over the natural numbers with $<$.

**Branching time.** [Computation tree logic](/computation-tree-logic/) (CTL) speaks about the computation tree. Each temporal operator must be directly preceded by a path quantifier, $\mathsf{A}$ (on all paths) or $\mathsf{E}$ (on some path). So $\mathsf{AG}\,\mathsf{EF}\,\mathit{reset}$ says that from each reachable state a reset is still possible.

**Both.** [CTL*](/ctl-star/) allows any mix of path quantifiers and temporal operators. It contains LTL (as the formulas $\mathsf{A}\,\varphi$) and CTL.

**Fixed points.** The [modal mu-calculus](/modal-mu-calculus/) has only the one-step modalities $\Diamond$ and $\Box$, and least and greatest [fixed points](/fixed-point/). It contains CTL*, and its algorithms show that each temporal operator is a fixed point: for example $\mathsf{E}[\varphi\,\mathsf{U}\,\psi] = \mu Z.\, \psi \vee (\varphi \wedge \Diamond Z)$.

**Expressiveness.** LTL and CTL are incomparable:

- $\mathsf{AG}\,\mathsf{EF}\,p$ (a $p$-state stays reachable) is CTL and has no LTL equivalent, because two structures with the same paths can differ on it.
- $\mathsf{F}\mathsf{G}\,p$ (from some point on, always $p$) is LTL and has no CTL equivalent; in particular, it is not the same as $\mathsf{AF}\,\mathsf{AG}\,p$.
- $\mathsf{A}(\mathsf{F}\mathsf{G}\,p \vee \mathsf{AG}\,\mathsf{EF}\,p)$ is CTL* and in neither.

So $\mathrm{LTL} \cup \mathrm{CTL} \subsetneq \mathrm{CTL}^* \subsetneq \mu$-calculus, where the mu-calculus is compared on the properties of computation trees.

**Cost.** The choice of logic is also a choice of algorithm. With $|M|$ the size of the structure and $|\varphi|$ the size of the formula:

| logic | model checking | satisfiability |
|---|---|---|
| CTL | $O(\lvert M\rvert\,\lvert\varphi\rvert)$, P-complete | EXPTIME-complete |
| LTL | $O(\lvert M\rvert\, 2^{O(\lvert\varphi\rvert)})$, PSPACE-complete | PSPACE-complete |
| CTL* | $O(\lvert M\rvert\, 2^{O(\lvert\varphi\rvert)})$, PSPACE-complete | 2EXPTIME-complete |
| mu-calculus | in NP $\cap$ coNP, quasi-polynomial | EXPTIME-complete |

The CTL bound is the [linear-time theorem](/ctl-model-checking-linear-time/), the LTL bounds are Sistla and Clarke (1985), and the mu-calculus results are on the page on [mu-calculus model checking](/mu-calculus-model-checking/). The pages on [CTL model checking](/ctl-model-checking/), [CTL satisfiability](/ctl-satisfiability/) and [CTL*](/ctl-star/) give the others. The exponential in $|\varphi|$ for LTL rarely hurts in practice, because formulas are short and structures are large.

## Examples

On the two-process mutual exclusion structure of the [Kripke structure](/kripke-structure/) page:

- **Safety.** $\mathsf{G}\,\neg(c_1 \wedge c_2)$ in LTL, or $\mathsf{AG}\,\neg(c_1 \wedge c_2)$ in CTL: never both critical. It holds.
- **Liveness.** $\mathsf{G}(w_1 \to \mathsf{F}\,c_1)$ in LTL, or $\mathsf{AG}(w_1 \to \mathsf{AF}\,c_1)$ in CTL: a waiting process eventually enters. It fails, because process 2 can enter again and again; it holds under strong [fairness](/fairness/).
- **Possibility.** $\mathsf{AG}\,\mathsf{EF}\,c_1$: from each reachable state, process 1 can still get into its critical section. It holds. This one has no LTL equivalent; it says what *can* happen, not what *must* happen.
- **Until.** $\mathsf{A}[\neg c_1\,\mathsf{U}\,w_1]$ from $(n, n, 1)$: process 1 does not enter before it has waited. It fails, because on the path where process 1 never moves, $w_1$ never holds. The weaker "unless" form $\mathsf{A}[\neg c_1\,\mathsf{W}\,w_1]$ holds.

## Where it is used

- **Model checking.** Hardware and protocol verifiers check temporal formulas against finite-state models: CTL in SMV and NuSMV, LTL in SPIN, both in many other tools. The [CTL labelling algorithm](/ctl-labelling-algorithm/) and [LTL model checking](/ltl-model-checking/) through [Büchi automata](/buchi-automaton/) are the two basic algorithms.
- **Runtime verification.** Monitors check LTL safety properties on the finite trace of a running program.
- **Synthesis.** Reactive synthesis builds a system from an LTL specification, through games on graphs.
- **Specification languages.** PSL and SVA in hardware, and TLA+ in distributed systems, are temporal logics with extra syntax.
- **Planning.** [Planning as model checking](/planning-as-model-checking/) writes goals as temporal formulas.
- **Philosophy and linguistics.** Temporal logic began as Arthur Prior's tense logic in the 1950s, with past and future operators.

## References
