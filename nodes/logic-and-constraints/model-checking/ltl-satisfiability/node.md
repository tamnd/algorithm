---
tag: H4YT4W
kind: problem
slug: ltl-satisfiability
name: LTL satisfiability
area: logic-and-constraints/model-checking
level: advanced
summary: Decide whether some infinite word satisfies a given LTL formula. The problem is PSPACE-complete, and a satisfiable formula has a lasso model of length 2^O(|φ|).
prereqs: [linear-temporal-logic, buchi-automaton, ltl-to-buchi-translation]
see_also: [ltl-model-checking, ltl-model-checking-pspace-completeness, automata-theoretic-approach, vacuity-checking, predicate-specification-patterns, bounded-model-checking, sat, qbf]
sources:
  - paper: doi:10.1145/3828.3837
    title: A. Prasad Sistla and Edmund M. Clarke, The complexity of propositional linear temporal logics, Journal of the ACM 32(3), 1985, pages 733 to 749
    locator: PSPACE-completeness of satisfiability for LTL, and NP-completeness for the fragment with F only
  - paper: doi:10.1006/inco.1994.1092
    title: Moshe Y. Vardi and Pierre Wolper, Reasoning about infinite computations, Information and Computation 115(1), 1994, pages 1 to 37
    locator: satisfiability of LTL by the emptiness of a Büchi automaton built from the formula
  - paper: "Kristin Y. Rozier and Moshe Y. Vardi, LTL satisfiability checking, SPIN 2007, Lecture Notes in Computer Science 4595, Springer, 2007"
    locator: satisfiability checking as a sanity check of specifications, and the comparison of explicit and symbolic tools on it
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 5, Section 5.2 (satisfiability and validity of LTL by the automaton of the formula, and the complexity of these problems)
---

LTL satisfiability asks whether some infinite sequence of propositional valuations satisfies a given [linear temporal logic](/linear-temporal-logic/) formula. It is decided by building a [Büchi automaton](/buchi-automaton/) for the formula and testing whether it accepts some word. The problem is [PSPACE](/pspace/)-complete (Sistla and Clarke 1985), and a satisfiable formula always has a model in the shape of a lasso, a finite stem followed by a loop that repeats forever. The problem is the dual of LTL validity, and it is the special case of [LTL model checking](/ltl-model-checking/) in which the system can do anything.

## In plain words

A temporal formula describes how a system may behave over time. Before checking a system against such a formula, it is worth asking a simpler question: can anything behave like that at all? If no behaviour fits the formula, the formula is a contradiction, and every system fails it. If every behaviour fits it, the formula says nothing.

The method turns the formula into a small machine that reads behaviours and accepts the ones that fit. The question is then whether the machine accepts at least one. That holds exactly when the machine has a path to a loop that keeps its promises, and the loop gives a sample behaviour. The machine can be very large for a long formula, so the search walks through it a step at a time and does not store all of it.

## Definition

Fix a finite set $AP$ of atomic propositions. A *word* is an infinite sequence $\sigma = \sigma_0 \sigma_1 \ldots \in (2^{AP})^\omega$, and $\sigma \models \varphi$ is the satisfaction relation of [LTL](/linear-temporal-logic/) at position $0$.

- **Input.** An LTL formula $\varphi$ over $AP$, of size $|\varphi|$, the number of its symbols.
- **Question.** Is there a word $\sigma$ with $\sigma \models \varphi$?

Such a $\sigma$ is a *model* of $\varphi$. Only the propositions that occur in $\varphi$ matter, so $AP$ can be taken to be the set $AP_\varphi$ of these propositions. The formula is *valid* if every word is a model, which holds iff $\neg\varphi$ is unsatisfiable.

A model of the form $u\, v^\omega$, with finite words $u$ and $v$ and $v$ not empty, is a *lasso model*, or an ultimately periodic model. Every satisfiable formula has one (see Bounds), so a lasso model is a finite certificate of satisfiability.

## Variants

- **Validity.** Is every word a model? This is the complement of satisfiability for $\neg\varphi$, and it is also PSPACE-complete.
- **Fragments.** Restricting the operators changes the cost. For formulas with only $\mathsf{F}$ (and so $\mathsf{G}$) and the Boolean connectives, satisfiability is NP-complete, and such a formula has a lasso model of polynomial size (Sistla and Clarke 1985). The fragment with $\mathsf{F}$ and $\mathsf{X}$, and the one with $\mathsf{U}$ only, are PSPACE-complete again.
- **Finite traces.** Over finite words, as in LTLf, satisfiability is again PSPACE-complete; the automaton is an automaton on finite words.
- **Satisfiability in a structure.** Given also a [Kripke structure](/kripke-structure/) $M$, is there a path of $M$ whose trace is a model? This is the complement of model checking for $\neg\varphi$.
- **Realizability.** If the propositions are split between an environment and a system, and the system must choose its values after seeing the environment's, the question is whether a strategy guarantees $\varphi$. This is LTL synthesis, which is 2EXPTIME-complete (Pnueli and Rosner 1989).

## Examples

| Formula | Satisfiable? | Model or reason |
|---|---|---|
| $\mathsf{G}\, p \wedge \mathsf{F} \neg p$ | no | $\mathsf{G}\,p$ makes $p$ true at every position |
| $p\ \mathsf{U}\ q \wedge \mathsf{G} \neg q$ | no | the until needs a position where $q$ holds |
| $\mathsf{G}\mathsf{F}\, p \wedge \mathsf{G}\mathsf{F} \neg p$ | yes | $(\{p\}\ \emptyset)^\omega$ |
| $p \wedge \mathsf{G}(p \leftrightarrow \mathsf{X} \neg p)$ | yes, one model | $(\{p\}\ \emptyset)^\omega$ is the only model |
| $\mathsf{G}(r \to \mathsf{F}\, g) \wedge \mathsf{F}\mathsf{G}\, r \wedge \mathsf{F}\mathsf{G} \neg g$ | no | $r$ from some point on forces infinitely many $g$ |
| $\mathsf{F}\mathsf{G}\, p \wedge \mathsf{G}\mathsf{F} \neg p$ | no | the formulas are negations of each other |

**Long models.** Lasso models can be forced to be long. Take propositions $b_1, \ldots, b_m$, the bits of a binary counter, and let $\varphi_m$ say that all bits are $0$ at the start and that each step adds one modulo $2^m$:

$$\varphi_m = \bigwedge_{i=1}^{m} \neg b_i \wedge \mathsf{G}\Bigl(\bigwedge_{i=1}^{m} \bigl(\mathsf{X}\, b_i \leftrightarrow (b_i \oplus (b_1 \wedge \cdots \wedge b_{i-1}))\bigr)\Bigr),$$

where $\oplus$ is exclusive or, written with $\wedge$ and $\neg$. The size is $O(m^2)$. By induction on positions, the only model is the sequence of the numbers $0, 1, 2, \ldots$ in binary, repeated forever, so every lasso model $u\, v^\omega$ has $|v|$ a multiple of $2^m$. A satisfiable formula can thus need a model of exponential length, and a lasso model is not a polynomial-size certificate. This is one sign that the problem is harder than NP.

## Known algorithms

- **Automata.** Translate $\varphi$ into a generalized Büchi automaton $A_\varphi$ with at most $2^{|\varphi|}$ states ([LTL to Büchi translation](/ltl-to-buchi-translation/)). Then $\varphi$ is satisfiable iff $A_\varphi$ has a reachable cycle that meets every acceptance set. Search with [Tarjan's algorithm](/tarjan-scc/), or with [nested depth-first search](/nested-depth-first-search/) after degeneralization. Time $2^{O(|\varphi|)}$. The accepting lasso, read through the labels of the states, is a lasso model. This is the method of the [automata-theoretic approach](/automata-theoretic-approach/) with no system.
- **On the fly in polynomial space.** Guess the lasso in $A_\varphi$ one state at a time, keeping only the current state, the state where the loop starts, and the set of acceptance sets met so far. This uses $O(|\varphi|)$ space nondeterministically, and $O(|\varphi|^2)$ deterministically by [Savitch's theorem](/savitch-theorem/); see the [PSPACE-completeness proof](/ltl-model-checking-pspace-completeness/).
- **Tableaux.** Build a graph of consistent sets of subformulas, remove the nodes that cannot keep their promises, and test whether an initial node is left (Wolper 1983; Lichtenstein and Pnueli 1985). This is the same graph as the automaton, built by need.
- **Symbolic.** Encode the automaton with BDDs and compute the states with a fair path by a fixed point, as in [symbolic model checking](/symbolic-model-checking/). Rozier and Vardi (2007) compared explicit and symbolic tools on this problem and found the symbolic ones faster on many classes of formulas.
- **Bounded.** Search for lasso models with stem and loop of length at most $k$ with a [SAT](/sat/) solver, as in [bounded model checking](/bounded-model-checking/). A model found is real, but a failure for small $k$ proves nothing, because of formulas like $\varphi_m$.
- **Temporal resolution.** Fisher's clausal resolution for LTL proves unsatisfiability by deriving a contradiction from a normal form of the formula.

## Bounds

| Bound | Value | Source |
|---|---|---|
| complexity | PSPACE-complete | Sistla and Clarke 1985 |
| time | $2^{O(\lvert\varphi\rvert)}$ | by the automaton of the formula |
| space | $O(\lvert\varphi\rvert^2)$ | on-the-fly lasso search and Savitch's theorem |
| size of a lasso model | stem $< 2^{\lvert\varphi\rvert}$, loop $\le (\lvert\varphi\rvert + 1)\, 2^{\lvert\varphi\rvert}$ | from the automaton |
| fragment with F only | NP-complete, models of polynomial size | Sistla and Clarke 1985 |

The size of a lasso model follows from the automaton: a shortest path to the start of the loop has fewer edges than the number of states, and the loop can be made of one simple path to each of the at most $|\varphi|$ acceptance sets and one back. The family $\varphi_m$ above shows that loops of length $2^{\Omega(\sqrt{|\varphi|})}$ are needed in the worst case. The hardness holds already for a fixed set of propositions, since the reduction in the [proof](/ltl-model-checking-pspace-completeness/) uses the letters of one fixed Turing machine.

## Reductions

- **From polynomial-space machines.** For a Turing machine that runs in space $p(n)$, the [proof of PSPACE-hardness](/ltl-model-checking-pspace-completeness/) writes a formula of size $O(p(n)^2)$ whose only model is the computation, with $\mathsf{X}^{p(n)+1}$ linking each cell to the same cell in the next configuration, and adds $\mathsf{F}$ of an accepting letter.
- **To model checking.** $\varphi$ is satisfiable iff $U_{AP} \not\models \neg\varphi$, where $U_{AP}$ is the structure with one state for each subset of $AP_\varphi$, all states initial, and all transitions. This structure is exponential in $|AP_\varphi|$, but the hardness proof needs only a fixed one.
- **From model checking.** For a structure $M = (S, I, R, L)$, add a proposition $\mathit{at}_s$ for each state $s$ and let $\chi_M$ be the conjunction of: some $\mathit{at}_s$ with $s \in I$ holds at position $0$; $\mathsf{G}$ (exactly one $\mathit{at}_s$ holds); $\mathsf{G}(\mathit{at}_s \to \mathsf{X} \bigvee_{t \in R(s)} \mathit{at}_t)$ for each $s$; and $\mathsf{G}(\mathit{at}_s \to$ the literals of $L(s))$ for each $s$. Its models describe exactly the paths of $M$ from $I$, so $M \models \varphi$ iff $\chi_M \wedge \neg\varphi$ is unsatisfiable. The size of $\chi_M$ is polynomial in $|M|$ and $|AP|$.
- **From propositional satisfiability.** A propositional formula is satisfiable iff it is satisfiable as an LTL formula, so [SAT](/sat/) is a special case, and the problem is NP-hard for trivial reasons.

## Applications

- **Sanity checks of specifications.** An unsatisfiable specification is met by no system, and model checking against it fails for a reason that has nothing to do with the system. A valid specification is met by every system. Testing both is cheap compared with model checking, and Rozier and Vardi proposed it as a routine step.
- **Consistency of requirements.** A set of requirements written as LTL formulas, for example with the [specification patterns](/predicate-specification-patterns/), is consistent iff their conjunction is satisfiable. An unsatisfiable core points to the requirements in conflict.
- **Implication between properties.** $\varphi \to \psi$ is valid iff $\varphi \wedge \neg\psi$ is unsatisfiable. This checks whether a new property is already implied by the old ones, and it is the core of some [vacuity](/vacuity-checking/) tests.
- **Witness generation.** A lasso model is an example behaviour that meets the specification, which helps to explain a formula or to produce a test.

## References
